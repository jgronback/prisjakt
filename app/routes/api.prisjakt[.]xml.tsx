import type { LoaderFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";

const ADMIN_VERSION = "2025-04";

function esc(s = "") {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
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
    if (!link) break;
    const next = link.split(",").find(p => p.includes('rel="next"'));
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
  const url = new URL(request.url);
  const tag = (url.searchParams.get("tag") || "prisjakt").toLowerCase();
  const sig = url.searchParams.get("sig");

  // FEED_SECRET ligger i din .env i projektroten
  if (!sig || !process.env.FEED_SECRET || sig !== process.env.FEED_SECRET) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Hämta shop + token via din admin-session (kräver att du är inloggad i admin)
  const { session } = await authenticate.admin(request);
  const shop = session.shop;
  const token = session.accessToken;

  // Om base inte skickas använder vi butikens myshopify-domän automatiskt
  const base = (url.searchParams.get("base") || `https://${shop}`).replace(/\/$/, "");

  const products = await fetchAllProducts(shop, token);

  const filtered = products.filter((p: any) => {
    const tags = (p.tags || "").toLowerCase().split(",").map((t: string) => t.trim()).filter(Boolean);
    const hasTag = tags.includes(tag);
    const isActive = p.status === "active";
    const isPublished = !!p.published_at;
    const hasVariant = Array.isArray(p.variants) && p.variants.length > 0;
    return hasTag && isActive && isPublished && hasVariant;
  });

  const variants = filtered.map((p: any) => p.variants[0]);
  const itemIds = variants.map((v: any) => v.inventory_item_id).filter(Boolean);
  const levels = await fetchInventoryLevels(shop, token, itemIds);

  const itemsXml = filtered.map((p: any) => {
    const v = p.variants[0] || {};
    const price = v.price || "0";
    const image = p.images?.[0]?.src || p.images?.[0]?.url || "";
    const link = `${base}/products/${p.handle}`;
    const brand = p.vendor || "Brand";
    const gtin = v.barcode || "";
    const sku = v.sku || String(p.id);
    const productType = p.product_type || "";
    const available = Number(levels.get(Number(v.inventory_item_id)) || 0);
    const availability = available > 0 ? "in_stock" : "out_of_stock";

    return `
      <item>
        <g:id><![CDATA[${esc(sku)}]]></g:id>
        <g:title><![CDATA[${p.title || ""}]]></g:title>
        <g:description><![CDATA[${p.body_html || ""}]]></g:description>
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

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:pj="https://schema.prisjakt.nu/ns/1.0" xmlns:g="http://base.google.com/ns/1.0" version="3.0">
  <channel>
    <title>${esc(shop)} Prisjakt Feed</title>
    <description>Automatisk feed från Shopify</description>
    <link>${esc(base)}</link>
${itemsXml}
  </channel>
</rss>`;

  return new Response(rss, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
}
