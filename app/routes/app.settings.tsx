// app/routes/app.settings.tsx
import { json, type HeadersFunction, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

// Tillåt inbäddning i Shopify-admin (CSP)
export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

// Minimal loader – inga beroenden alls
export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shop = url.searchParams.get("shop") || "unknown-shop.myshopify.com";
  const base = (process.env.SHOPIFY_APP_URL || url.origin).replace(/\/$/, "");
  return json({
    marker: "🧪 settings-stub-v1",
    shop,
    onlyTagged: `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt`,
    allProducts: `${base}/public/prisjakt.xml?shop=${shop}&tag=all`,
  });
}

export default function SettingsPage() {
  const data = useLoaderData<typeof loader>();

  // Enbart statiskt UI. INGET health.hasOfflineToken, inga DB-anrop.
  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 900 }}>
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>Feed settings (safe stub)</h1>
      <div style={{ margin: "16px 0", padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
        <div>Marker: <code>{data.marker}</code></div>
        <div>Shop: <code>{data.shop}</code></div>
      </div>

      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr", marginTop: 16 }}>
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Alternativ A – Endast taggade</h3>
          <input readOnly value={data.onlyTagged} style={{ width: "100%", marginBottom: 8 }} />
          <a
            href={data.onlyTagged}
            target="_blank"
            rel="noreferrer"
            style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}
          >
            Öppna i ny flik
          </a>
        </div>

        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Alternativ B – Alla produkter</h3>
          <input readOnly value={data.allProducts} style={{ width: "100%", marginBottom: 8 }} />
          <a
            href={data.allProducts}
            target="_blank"
            rel="noreferrer"
            style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}
          >
            Öppna i ny flik
          </a>
        </div>
      </div>
    </div>
  );
}
