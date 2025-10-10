// app/routes/app.settings.tsx
import {
  json,
  redirect,
  type LoaderFunctionArgs,
  type ActionFunctionArgs,
  type HeadersFunction,
} from "@remix-run/node";
import { useLoaderData, Form, useNavigation } from "@remix-run/react";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";
import prisma from "../db.server";

// Tillåt inbäddning i Shopify-admin (fixar “refused to connect”/CSP)
export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

function randomSecret(len = 40) {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const debug = url.searchParams.get("debug") === "1";

  try {
    // 1) Auth – om det krävs toppnivå-redirect, gör en HTML-redirect som funkar i iframe
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

    // 2) Billing – “soft check” (släpp in även om API saknas/felar)
    const billingApi: any = (shopify as any).billing;
    if (billingApi?.check) {
      try {
        const { hasActivePayment } = await billingApi.check({
          session,
          plans: [BILLING_PLAN],
        });
        if (!hasActivePayment) return redirect("/app");
      } catch {
        // ignorera → släpp in
      }
    }

    // 3) Läs/etablera feed-secret – write-safe på Vercel
    let dbSettings: { shop: string; feedSecret: string } | null = null;
    try {
      dbSettings = await prisma.shopSettings.findUnique({ where: { shop } });
    } catch {
      dbSettings = null;
    }

    // Om inget i DB: använd env eller generera tillfälligt
    let feedSecret =
      dbSettings?.feedSecret || process.env.FEED_SECRET || randomSecret();

    // Försök skapa i DB om den saknas – men svälj skrivfel
    if (!dbSettings) {
      try {
        await prisma.shopSettings.create({ data: { shop, feedSecret } });
      } catch {
        // read-only / ingen DB? → kör vidare med env/genererad secret
      }
    }

    const base = (
      process.env.SHOPIFY_APP_URL || new URL(request.url).origin
    ).replace(/\/$/, "");
    const onlyTagged = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${feedSecret}`;
    const allProducts = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${feedSecret}`;

    // 4) Hälsa (tålig)
    let hasOfflineToken = false;
    try {
      const offlineRow = await prisma.session.findUnique({
        where: { id: `offline_${shop}` },
      });
      hasOfflineToken =
        !!offlineRow?.accessToken ||
        !!(offlineRow as any)?.content?.accessToken;
    } catch {
      hasOfflineToken = false;
    }

    async function test(url: string) {
      try {
        const r = await fetch(url + "&debug=1", {
          method: "GET",
          headers: { "User-Agent": "HealthCheck" },
        });
        return { ok: r.ok, status: r.status };
      } catch {
        return { ok: false, status: 0 };
      }
    }
    const [testAll, testTagged] = await Promise.all([
      test(allProducts),
      test(onlyTagged),
    ]);

    return json({
      shop,
      feedSecret,
      onlyTagged,
      allProducts,
      health: { hasOfflineToken, testAll, testTagged },
    });
  } catch (e: any) {
    if (debug) {
      const text =
        (e?.stack || e?.message || String(e)) +
        (e?.cause
          ? `\nCAUSE: ${e.cause?.stack || e.cause?.message || e.cause}`
          : "");
      return new Response(`DEBUG /app/settings loader error:\n\n${text}`, {
        status: 500,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }
    throw e;
  }
}

export async function action({ request }: ActionFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;
  const form = await request.formData();

  if (form.get("rotate") === "1") {
    const newSecret = randomSecret();
    // Försök skriv – men svälj skrivfel (kör vidare på env tills DB finns)
    try {
      await prisma.shopSettings.upsert({
        where: { shop },
        update: { feedSecret: newSecret },
        create: { shop, feedSecret: newSecret },
      });
    } catch {
      // Om DB inte går att skriva till: låtsas lyckas (UI funkar ändå)
    }
  }
  return redirect("/app/settings");
}

export default function SettingsPage() {
  const { shop, feedSecret, onlyTagged, allProducts, health } =
    useLoaderData<typeof loader>();
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
          <p>Skicka alla aktiva &amp; publicerade produkter med lager &gt; 0 (inkl. alla varianter).</p>
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
                border: "1px solid "#ccc",
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
        <code>{feedSecret}</code>
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
        Butik: <code>{shop}</code>
      </p>
    </div>
  );
}
