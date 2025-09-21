import type { LoaderFunctionArgs } from "@remix-run/node";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const ADMIN_VERSION = "2025-04";

// 5-min cache per (shop|tag)
type CacheVal = { xml: string; exp: number };
const cache = new Map<string, CacheVal>();
const TTL_MS = 5 * 60 * 1000;

function esc(s = "") {
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

async function getOfflineToken(shopDomain: string) {
  const id = `offline_${shopDomain}`;
  const row: any = await prisma.session.findUnique({ where: { id } });
  const token = row?.accessToken ?? row?.content?.accessToken;
  if (!token) throw new Error("No offline token for shop");
  return token as string;
}

async function fetchAllProducts(shop: string, token: string) {
  let url = `https://${shop}/admin/api/${ADMIN_VERSION}/products.json?limit=250&fields=id,title,body_html,product_type,vendor,tags,images,variants,handle,status,published_at`;
  const all: any[] = [];
  while (url) {
    const res = await fetch(url, { headers: { "X-Shopify-Access-Token": token } });
    if (!res.ok) throw new Error(`Shopify ${res.status}`);
    const data = await res.json();
    all.push(...(data.products || []));
    const link = res.headers.get("link");
    const next = link?.split(",").find((p) => p.includes('rel="next"'));
    url = next ? next.match(/<([^>]+)>/)?.[1] ?? null : null;
  }
  return all;
}

async function fetchInventoryLevels(shop: string, token: string, ids: number[]) {
  const map = new Map<number, number>();
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const url = `https://${shop}/admin/api/${ADMIN_VERSION}/inventory_levels.json?inventory_item_ids=${chunk.join(",")}`;
    const res = await fetch(url, { headers: { "X-Shopify-Access-Token": token } });
    if (!res.ok) throw new Error(`Shopify ${res.status}`);
    const data = await res.json();
    for (const lvl of data.inventory_levels || []) {
      const id = Number(lvl.inventory_item_id);
      map.set(id, (map.get(id) || 0) + (lvl.available ?? 0));
    }
  }
  return map;
}

export async function loader({ request }: LoaderFunctionArgs) {
  try {
    const url = new URL(request.url);
    const shop = url.searchParams.get("shop") || "";
    const tagParam = (url.searchParams.get("tag") || "prisjakt").toLowerCase();
    const sig = url.searchParams.get("sig") || "";
    const base = (url.searchParams.get("base") || `https://${shop}`).replace(/\/$/, "");
    const debug = url.searchParams.get("debug") === "1";

    if (!shop) return new Response("Missing shop", { status: 400 });

    // 1) Signatur per butik (fallback till FEED_SECRET om rad saknas)
    const settings = await prisma.shopSettings.findUnique({ where: { shop } });
    const expectedSig = settings?.feedSecret || process.env.FEED_SECRET;
    if (!expectedSig || sig !== expectedSig) return new Response("Unauthorized", { status: 401 });

    const cacheKey = `${shop}|${tagParam}`;
    const now = Date.now();
    if (!debug) {
      const hit = cache.get(cacheKey);
      if (hit && hit.exp > now) {
        return new Response(hit.xml, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
      }
    }

    // 2) Token + produkter
    const token = await getOfflineToken(shop);
    const products = await fetchAllProducts(shop, token);

    // 3) Filtrera produkter
    const filtered = products.filter((p: any) => {
      const tags = (p.tags || "").toLowerCase().split(",").map((t: string) => t.trim()).filter(Boolean);
      const tagAll = tagParam === "all";
      const hasTag = tagAll || tags.includes(tagParam);
      const isActive = p.status === "active";
      const isPublished = !!p.published_at;
      const hasVariants = Array.isArray(p.variants) && p.variants.length > 0;
      return hasTag && isActive && isPublished && hasVariants;
    });

    // 4) Hämta lager för ALLA varianter
    const allVariantIds = filtered.flatMap((p: any) => (p.variants || []).map((v: any) => v.inventory_item_id)).filter(Boolean);
    const levels = await fetchInventoryLevels(shop, token, allVariantIds);

    // 5) Bygg XML – ETT <item> PER VARIANT
    const itemsXml = filtered.map((p: any) => {
      const image = p.images?.[0]?.src || p.images?.[0]?.url || "";
      const brand = p.vendor || "Brand";
      const productType = p.product_type || "";
      const productTitle = p.title || "";
      const productDesc = p.body_html || "";

      return (p.variants || []).map((v: any) => {
        const price = v.price || "0";
        const sku = v.sku || `${p.id}-${v.id}`;
        const gtin = v.barcode || "";
        const available = Number(levels.get(Number(v.inventory_item_id)) || 0);
        const availability = available > 0 ? "in_stock" : "out_of_stock";
        const link = `${base}/products/${p.handle}?variant=${v.id}`;

        return `
      <item>
        <g:id><![CDATA[${esc(sku)}]]></g:id>
        <g:title><![CDATA[${productTitle}]]></g:title>
        <g:description><![CDATA[${productDesc}]]></g:description>
        <g:link>${esc(link)}</g:link>
        ${image ? `<g:image_link>${esc(image)}</g:image_link>` : ""}
        <g:price>${esc(price)} SEK</g:price>
        <g:condition>new</g:condition>
        <g:availability>${availability}</g:availability>
        ${brand ? `<g:brand><![CDATA[${brand}]]></g:brand>` : ""}
        ${gtin ? `<g:gtin>${esc(gtin)}</g:gtin>` : ""}
        <g:mpn><![CDATA[${esc(sku)}]]></g:mpn>
        ${productType ? `<g:product_type><![CDATA[${productType}]]></g:product_type>` : ""}
        <g:shipping><g:country>SE</g:country><g:price>0 SEK</g:price></g:shipping>
      </item>`;
      }).join("");
    }).join("");

    const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:pj="https://schema.prisjakt.nu/ns/1.0" xmlns:g="http://base.google.com/ns/1.0" version="3.0">
  <channel>
    <title>${esc(shop)} Prisjakt Feed</title>
    <description>Automatisk feed från Shopify</description>
    <link>${esc(base)}</link>
${itemsXml}
  </channel>
</rss>`;

    // 6) Cache i 5 min
    cache.set(cacheKey, { xml: rss, exp: now + TTL_MS });

    return new Response(rss, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
  } catch (e: any) {
    return new Response(`Error: ${e?.message ?? "unknown"}`, { status: 500 });
  }
}
