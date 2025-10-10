// app/routes/app.settings.tsx
import {
  json,
  redirect,
  type LoaderFunctionArgs,
  type ActionFunctionArgs,
  type HeadersFunction,
} from "@remix-run/node";
import { useLoaderData, Form, useNavigation } from "@remix-run/react";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";

// Tillåt inbäddning i Shopify-admin
export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

function randomSecret(len = 40) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

export async function loader({ request }: LoaderFunctionArgs) {
  // Auth – hantera toppnivå-redirect i iframe
  let session;
  try {
    ({ session } = await authenticate.admin(request));
  } catch (err: any) {
    if (err instanceof Response && err.status >= 300 && err.status < 400) {
      const loc = err.headers.get("Location") || "/auth/login";
      const abs = new URL(
        loc,
        process.env.SHOPIFY_APP_URL || new URL(request.url).origin
      ).toString();
      return new Response(
        `<!doctype html><html><body><script>
           if (window.top) window.top.location.href=${JSON.stringify(abs)};
           else window.location.href=${JSON.stringify(abs)};
         </script></body></html>`,
        { headers: { "Content-Type": "text/html" } }
      );
    }
    throw err;
  }

  const shop = session.shop;

  // Läs/etablera feed-secret (tål DB-fel)
  let feedSecret: string | null = null;
  try {
    const row = await prisma.shopSettings.findUnique({ where: { shop } });
    feedSecret = row?.feedSecret ?? null;
  } catch {
    feedSecret = null;
  }
  if (!feedSecret) {
    feedSecret = process.env.FEED_SECRET || randomSecret();
    try {
      await prisma.shopSettings.upsert({
        where: { shop },
        update: { feedSecret },
        create: { shop, feedSecret },
      });
    } catch {
      // Ignorera skrivfel – vi använder feedSecret i minnet/env
    }
  }

  const base = (process.env.SHOPIFY_APP_URL || new URL(request.url).origin).replace(/\/$/, "");
  const onlyTagged = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${feedSecret}`;
  const allProducts = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${feedSecret}`;

  return json({ shop, feedSecret, onlyTagged, allProducts });
}

export async function action({ request }: ActionFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;
  const form = await request.formData();

  if (form.get("rotate") === "1") {
    const newSecret = randomSecret();
    try {
      await prisma.shopSettings.upsert({
        where: { shop },
        update: { feedSecret: newSecret },
        create: { shop, feedSecret: newSecret },
      });
    } catch {
      // Om DB inte går att skriva: ignorera – UI kommer fortsätta funka
    }
  }
  return redirect("/app/settings");
}

export default function SettingsPage() {
  const data = useLoaderData<typeof loader>();
  const nav = useNavigation();
  const busy = nav.state !== "idle";

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
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>Feed settings</h1>

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
          <input readOnly value={data.onlyTagged} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(data.onlyTagged)}>
              Kopiera länk
            </button>
            <a
              href={data.onlyTagged}
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
          <p>Skicka alla aktiva &amp; publicerade produkter med lager &gt; 0 (inkl. alla varianter).</p>
          <input readOnly value={data.allProducts} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(data.allProducts)}>
              Kopiera länk
            </button>
            <a
              href={data.allProducts}
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
          <b>Nuvarande unik kod</b> för den här butiken:
        </div>
        <code>{data.feedSecret}</code>
        <Form method="post" replace style={{ marginTop: 10 }}>
          <input type="hidden" name="rotate" value="1" />
          <button type="submit" disabled={busy} style={{ padding: "8px 12px" }}>
            {busy ? "Roterar..." : "Byt kod (om Prisjakt inte kan läsa in)"}
          </button>
        </Form>
        <div style={{ marginTop: 8, color: "#777" }}>
          Om du byter kod måste du ge Prisjakt <b>ny</b> länk (A eller B).
        </div>
      </div>

      <p style={{ marginTop: 12, color: "#666" }}>
        Butik: <code>{data.shop}</code>
      </p>
    </div>
  );
}
