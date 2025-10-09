import type { LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  const STORE = !!process.env.SHOPIFY_STORE_DOMAIN;
  const TOKEN = !!process.env.SHOPIFY_ADMIN_API_TOKEN;
  const API_VERSION = process.env.SHOPIFY_API_VERSION || "2025-07";

  const summary = { env: { STORE, TOKEN, API_VERSION } };
  if (!STORE || !TOKEN) {
    return new Response(JSON.stringify({ ...summary, ok:false, reason:"missing env" }), { status: 500 });
  }

  try {
    const res = await fetch(`https://${process.env.SHOPIFY_STORE_DOMAIN}/admin/api/${API_VERSION}/graphql.json`, {
      method: "POST",
      headers: {
        "X-Shopify-Access-Token": process.env.SHOPIFY_ADMIN_API_TOKEN!,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ query: "{ shop { name id } }" }),
    });
    const ok = res.ok;
    const code = res.status;
    return new Response(JSON.stringify({ ...summary, ok, code }), { headers: { "Content-Type": "application/json" } });
  } catch (e: any) {
    return new Response(JSON.stringify({ ...summary, ok:false, error:e?.message||String(e) }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
}
