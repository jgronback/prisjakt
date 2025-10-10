// app/routes/app.settings.safe.tsx
import {
  json,
  type LoaderFunctionArgs,
  type HeadersFunction,
} from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

type Health = {
  hasOfflineToken: boolean;
  testAll: { ok: boolean; status: number };
  testTagged: { ok: boolean; status: number };
};

export async function loader({ request }: LoaderFunctionArgs) {
  // Inga DB-anrop, inga Shopify-anrop — bara bygg länkar säkert.
  const url = new URL(request.url);
  const shop =
    url.searchParams.get("shop") ||
    process.env.DEFAULT_SHOP ||
    "unknown.myshopify.com";

  const base = (process.env.SHOPIFY_APP_URL || url.origin).replace(/\/$/, "");
  const feedSecret = process.env.FEED_SECRET || "demo-secret";

  const onlyTagged = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${feedSecret}`;
  const allProducts = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${feedSecret}`;

  const health: Health = {
    hasOfflineToken: false,
    testAll: { ok: false, status: 0 },
    testTagged: { ok: false, status: 0 },
  };

  return json({ shop, feedSecret, onlyTagged, allProducts, health });
}

export default function SettingsSafePage() {
  const data = useLoaderData<typeof loader>();
  const { shop, feedSecret, onlyTagged, allProducts, health } = data;

  const card: React.CSSProperties = {
    padding: 12,
    border: "1px solid #ddd",
    borderRadius: 8,
  };
  const note: React.CSSProperties = {
    marginTop: 8,
    padding: 10,
    border: "1px solid #eee",
    borderRadius: 8,
  };
  const box: React.CSSProperties = {
    margin: "16px 0",
    padding: 12,
    border: "1px solid #eee",
    borderRadius: 8,
  };

  return (
    <div
      style={{
        padding: 16,
        fontFamily: "Inter, system-ui, sans-serif",
        maxWidth: 900,
      }}
    >
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>
        Feed settings (SAFE version)
      </h1>

      <div style={box}>
        <b>Hälsokontroller</b>
        <ul style={{ marginTop: 8 }}>
          <li>
            Offline-token:{" "}
            {health.hasOfflineToken ? (
              <span style={{ color: "green" }}>OK</span>
            ) : (
              <span style={{ color: "red" }}>Saknas</span>
            )}
          </li>
          <li>
            Test “Alla produkter”:{" "}
            {health.testAll.ok ? (
              <span style={{ color: "green" }}>
                OK ({health.testAll.status})
              </span>
            ) : (
              <span style={{ color: "red" }}>
                Fel ({health.testAll.status})
              </span>
            )}
          </li>
          <li>
            Test “Endast taggade”:{" "}
            {health.testTagged.ok ? (
              <span style={{ color: "green" }}>
                OK ({health.testTagged.status})
              </span>
            ) : (
              <span style={{ color: "red" }}>
                Fel ({health.testTagged.status})
              </span>
            )}
          </li>
        </ul>
      </div>

      <p style={{ marginTop: 0, color: "#555" }}>
        Här får du <b>färdiga länkar</b> att ge till <b>Prisjakt</b>. Länkarna
        används enbart för inläsning – <b>ingenting</b> uppdateras i din butik.
      </p>

      <div style={note}>
        <b>Hur snabbt uppdateras priser/lagersaldo?</b> Feeden speglar dina
        Shopify-ändringar inom ca <b>5 min</b> (cache). När Prisjakt läser in
        igen syns ändringen hos dem.
      </div>

      <div
        style={{
          display: "grid",
          gap: 16,
          gridTemplateColumns: "1fr 1fr",
          marginTop: 16,
        }}
      >
        <div style={card}>
          <h3 style={{ marginTop: 0 }}>Alternativ A – Endast taggade produkter</h3>
          <p>Tagga valda produkter i Shopify med <code>prisjakt</code>.</p>
          <input readOnly value={onlyTagged} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(onlyTagged)}>
              Kopiera länk
            </button>
            <a
              href={onlyTagged}
              target="_blank"
              rel="noreferrer"
              style={{
                textDecoration: "none",
                padding: "6px 10px",
                border: "1px solid #ccc",
                borderRadius: 6,
              }}
            >
              Öppna i ny flik
            </a>
          </div>
        </div>

        <div style={card}>
          <h3 style={{ marginTop: 0 }}>Alternativ B – ALLA produkter</h3>
          <p>
            Skicka alla aktiva &amp; publicerade produkter med lager &gt; 0
            (inkl. alla varianter).
          </p>
          <input readOnly value={allProducts} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(allProducts)}>
              Kopiera länk
            </button>
            <a
              href={allProducts}
              target="_blank"
              rel="noreferrer"
              style={{
                textDecoration: "none",
                padding: "6px 10px",
                border: "1px solid #ccc",
                borderRadius: 6,
              }}
            >
              Öppna i ny flik
            </a>
          </div>
        </div>
      </div>

      <div style={{ ...box, borderStyle: "dashed" }}>
        <b>Instruktion – Alternativ A (endast taggade)</b>
        <ol style={{ marginTop: 8, marginBottom: 0 }}>
          <li>Tagga önskade produkter i Shopify med <code>prisjakt</code>.</li>
          <li>Kopiera länken under “Alternativ A”.</li>
          <li>
            Logga in på <code>app-business.prisjakt.nu</code> →{" "}
            <b>Data management</b> → <b>Lägg till feed</b>.
          </li>
          <li>
            Klistra in länken i <b>URL*</b>, välj{" "}
            <b>Prisjakt XML (rekommenderad)</b>, klicka <b>Lägg till</b>.
          </li>
        </ol>
      </div>

      <div style={{ ...box, borderStyle: "dashed" }}>
        <b>Instruktion – Alternativ B (alla produkter)</b>
        <ol style={{ marginTop: 8, marginBottom: 0 }}>
          <li>Kopiera länken under “Alternativ B”.</li>
          <li>
            Logga in på <code>app-business.prisjakt.nu</code> →{" "}
            <b>Data management</b> → <b>Lägg till feed</b>.
          </li>
          <li>
            Klistra in länken i <b>URL*</b>, välj{" "}
            <b>Prisjakt XML (rekommenderad)</b>, klicka <b>Lägg till</b>.
          </li>
        </ol>
      </div>

      <div style={box}>
        <div style={{ marginBottom: 8 }}>
          <b>Nuvarande unik kod</b> (env eller default):
        </div>
        <code>{feedSecret}</code>
      </div>

      <p style={{ marginTop: 12, color: "#666" }}>
        Butik: <code>{shop}</code>
      </p>
    </div>
  );
}
