// app/routes/app.settings.tsx
import { json, type LoaderFunctionArgs, type HeadersFunction } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export const headers: HeadersFunction = () => ({
  "Content-Security-Policy": "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shop =
    url.searchParams.get("shop") ||
    process.env.DEFAULT_SHOP ||
    "unknown.myshopify.com";

  const base = (process.env.SHOPIFY_APP_URL || url.origin).replace(/\/$/, "");
  const feedSecret = process.env.FEED_SECRET || "demo-secret";

  const onlyTagged = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${feedSecret}`;
  const allProducts = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${feedSecret}`;

  return json({ shop, feedSecret, onlyTagged, allProducts });
}

export default function SettingsMinimal() {
  const data = useLoaderData<typeof loader>();

  const card: React.CSSProperties = { padding: 12, border: "1px solid #ddd", borderRadius: 8 };
  const box: React.CSSProperties = { margin: "16px 0", padding: 12, border: "1px solid #eee", borderRadius: 8 };

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 900 }}>
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>Feed settings (MINIMAL)</h1>

      <div style={box}>
        <b>Färdiga länkar till Prisjakt</b>
        <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr", marginTop: 16 }}>
          <div style={card}>
            <h3 style={{ marginTop: 0 }}>Alternativ A – Endast taggade produkter</h3>
            <p>Tagga valda produkter i Shopify med <code>prisjakt</code>.</p>
            <input readOnly value={data.onlyTagged} style={{ width: "100%", marginBottom: 8 }} />
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => navigator.clipboard.writeText(data.onlyTagged)}>Kopiera länk</button>
              <a href={data.onlyTagged} target="_blank" rel="noreferrer"
                 style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}>
                Öppna i ny flik
              </a>
            </div>
          </div>

          <div style={card}>
            <h3 style={{ marginTop: 0 }}>Alternativ B – ALLA produkter</h3>
            <p>Alla aktiva &amp; publicerade produkter med lager &gt; 0 (inkl. varianter).</p>
            <input readOnly value={data.allProducts} style={{ width: "100%", marginBottom: 8 }} />
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => navigator.clipboard.writeText(data.allProducts)}>Kopiera länk</button>
              <a href={data.allProducts} target="_blank" rel="noreferrer"
                 style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}>
                Öppna i ny flik
              </a>
            </div>
          </div>
        </div>
      </div>

      <p style={{ marginTop: 12, color: "#666" }}>
        Butik: <code>{data.shop}</code> · Kod: <code>{data.feedSecret}</code>
      </p>
    </div>
  );
}
