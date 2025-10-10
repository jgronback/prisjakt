// app/routes/public.prisjakt[.]xml.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import prisma from "../db.server";

function esc(str = "") {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shop = url.searchParams.get("shop") || "";
  const tag = (url.searchParams.get("tag") || "prisjakt").toLowerCase();
  const sig = url.searchParams.get("sig") || "";
  if (!shop || !sig) {
    return new Response("<error>Missing shop or sig</error>", { status: 400, headers: { "Content-Type": "application/xml; charset=utf-8" } });
  }

  // Verify signature against DB
  const settings = await prisma.shopSettings.findUnique({ where: { shop } });
  if (!settings || settings.feedSecret !== sig) {
    return new Response("<error>Forbidden</error>", { status: 403, headers: { "Content-Type": "application/xml; charset=utf-8" } });
  }

  // Get offline token for the shop
  const offline = await prisma.session.findUnique({ where: { id: `offline_${shop}` } });
  let accessToken = offline?.accessToken as string | undefined;
  if (!accessToken && (offline as any)?.content) {
    try {
      const parsed = JSON.parse((offline as any).content);
      accessToken = parsed?.accessToken;
    } catch {}
  }
  if (!accessToken) {
    return new Response("<error>No offline token for shop</error>", { status: 503, headers: { "Content-Type": "application/xml; charset=utf-8" } });
  }

  const ADMIN = `https://${shop}/admin/api/2025-07`;

  async function shopifyGET(path: string) {
    const res = await fetch(`${ADMIN}${path}`, {
      headers: { "X-Shopify-Access-Token": accessToken!, "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error(`Shopify ${res.status} ${path}`);
    return res.json();
  }

  // Fetch all products (paginated)
  const allProducts: any[] = [];
  let pageInfo: string | null = null;
  let urlPath = `/products.json?limit=250&fields=id,title,body_html,product_type,vendor,tags,images,variants,handle,status,published_at`;
  do {
    const res = await fetch(`${ADMIN}${urlPath}`, { headers: { "X-Shopify-Access-Token": accessToken!, "Content-Type": "application/json" } });
    if (!res.ok) throw new Error(`Shopify ${res.status} products`);
    const data = await res.json();
    allProducts.push(...(data.products || []));
    const link = res.headers.get("link");
    if (link && link.includes('rel="next"')) {
      const m = link.split(",").find((p) => p.includes('rel="next"'))?.match(/<([^>]+)>/);
      urlPath = m ? m[1].replace(`https://${shop}/admin/api/2025-07`, "") : null;
    } else {
      urlPath = null;
    }
  } while (urlPath);

  // Filter
  const filtered = allProducts.filter((p) => {
    const isActive = p.status === "active";
    const isPublished = !!p.published_at;
    const hasVariant = Array.isArray(p.variants) && p.variants.length > 0;
    const tags = (p.tags || "").toLowerCase().split(",").map((t: string) => t.trim()).filter(Boolean);
    const include =
      tag === "all"
        ? isActive && isPublished && hasVariant
        : tags.includes("prisjakt") && isActive && isPublished && hasVariant;
    return include;
  });

  // Inventory levels for first variant per product (simple)
  const firstVariants = filtered.map((p) => p.variants[0]).filter(Boolean);
  const itemIds = firstVariants.map((v: any) => v.inventory_item_id).filter(Boolean);

  async function fetchInventoryLevels(ids: number[]) {
    const out = new Map<number, number>();
    for (let i = 0; i < ids.length; i += 50) {
      const chunk = ids.slice(i, i + 50).join(",");
      const data = await shopifyGET(`/inventory_levels.json?inventory_item_ids=${chunk}`);
      for (const lvl of data.inventory_levels || []) {
        const id = lvl.inventory_item_id;
        out.set(id, (out.get(id) || 0) + (lvl.available ?? 0));
      }
    }
    return out;
  }
  const levelMap = itemIds.length ? await fetchInventoryLevels(itemIds) : new Map<number, number>();

  // Build items
  const itemsXml = filtered
    .map((p) => {
      const v = p.variants?.[0] || {};
      const price = v.price || "0";
      const image = (p.images?.[0]?.src || p.images?.[0]?.url || "");
      const link = `https://${shop}/products/${p.handle}`;
      const brand = p.vendor || shop;
      const gtin = v.barcode || "";
      const sku = v.sku || String(p.id);
      const productType = p.product_type || "";
      const available = levelMap.get(v.inventory_item_id) ?? 0;
      const availability = available > 0 ? "in_stock" : "out_of_stock";

      return `
      <item>
        <g:id><![CDATA[ ${esc(sku)} ]]></g:id>
        <g:title><![CDATA[ ${p.title || ""} ]]></g:title>
        <g:description><![CDATA[ ${(p.body_html || "").toString()} ]]></g:description>
        <g:link>${esc(link)}</g:link>
        ${image ? `<g:image_link>${esc(image)}</g:image_link>` : ""}
        <g:price>${esc(price)} SEK</g:price>
        <g:condition>new</g:condition>
        <g:availability>${availability}</g:availability>
        ${brand ? `<g:brand><![CDATA[ ${brand} ]]></g:brand>` : ""}
        ${gtin ? `<g:gtin>${esc(gtin)}</g:gtin>` : ""}
        <g:mpn><![CDATA[ ${esc(sku)} ]]></g:mpn>
        ${productType ? `<g:product_type><![CDATA[ ${productType} ]]></g:product_type>` : ""}
        <g:shipping><g:country>SE</g:country><g:price>0 SEK</g:price></g:shipping>
      </item>`;
    })
    .join("");

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:pj="https://schema.prisjakt.nu/ns/1.0" xmlns:g="http://base.google.com/ns/1.0" version="3.0">
  <channel>
    <title>${esc(shop)} Prisjakt Feed</title>
    <description>Automatisk feed från Shopify</description>
    <link>https://${esc(shop)}</link>
${itemsXml}
  </channel>
</rss>`;

  return new Response(rss, {
    status: 200,
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=300",
    },
  });
}

export default function PublicFeed() { return null; }
