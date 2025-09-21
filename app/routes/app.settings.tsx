// app/routes/app.settings.tsx
import { json, redirect, type LoaderFunctionArgs, type ActionFunctionArgs } from "@remix-run/node";
import { useLoaderData, Form, useNavigation } from "@remix-run/react";
import { PrismaClient } from "@prisma/client";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

const prisma = new PrismaClient();

function randomSecret(len = 40) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;

  // Gate endast om billing-API finns
  const billingApi: any = (shopify as any).billing;
  if (billingApi?.check) {
    const check = await billingApi.check({ session, plans: [BILLING_PLAN] });
    if (!check?.hasActivePayment) return redirect("/app");
  }

  // Se till att butiken har en feed-hemlighet
  let settings = await prisma.shopSettings.findUnique({ where: { shop } });
  if (!settings) settings = await prisma.shopSettings.create({ data: { shop, feedSecret: randomSecret() } });

  const base = (process.env.SHOPIFY_APP_URL || new URL(request.url).origin).replace(/\/$/, "");
  const onlyTagged = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${settings.feedSecret}`;
  const allProducts = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${settings.feedSecret}`;

  return json({ shop, feedSecret: settings.feedSecret, onlyTagged, allProducts });
}

export async function action({ request }: ActionFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;
  const form = await request.formData();

  if (form.get("rotate") === "1") {
    const newSecret = randomSecret();
    await prisma.shopSettings.upsert({
      where: { shop },
      update: { feedSecret: newSecret },
      create: { shop, feedSecret: newSecret },
    });
  }
  return redirect("/app/settings");
}

export default function SettingsPage() {
  const { shop, feedSecret, onlyTagged, allProducts } = useLoaderData<typeof loader>();
  const nav = useNavigation();
  const busy = nav.state !== "idle";

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 900 }}>
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>Feed settings</h1>
      <p style={{ marginTop: 0, color: "#555" }}>
        På den här sidan får du <b>färdiga länkar</b> som du ger till <b>Prisjakt</b>. <br />
        <b>Viktigt:</b> Länkarna används av Prisjakt för att läsa in dina produkter. <b>Ingenting</b> uppdateras i din butik.
      </p>

      <div style={{ marginTop: 8, padding: 10, border: "1px solid #eee", borderRadius: 8 }}>
        <b>Rekommenderad uppdatering hos Prisjakt:</b> låt dem hämta länken <b>var 30–60 minut</b>. <br />
        Feeden speglar alltid din Shopify-data; vi lägger endast på en <b>5 minuters cache</b> för bättre hastighet.
      </div>

      <div style={{ margin: "16px 0", padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
        <div style={{ marginBottom: 8 }}>Nuvarande hemlighet (sig) för den här butiken:</div>
        <code>{feedSecret}</code>
        <Form method="post" replace style={{ marginTop: 10 }}>
          <input type="hidden" name="rotate" value="1" />
          <button type="submit" disabled={busy} style={{ padding: "8px 12px" }}>
            {busy ? "Roterar..." : "Byt hemlighet"}
          </button>
        </Form>
        <div style={{ marginTop: 8, color: "#777" }}>
          Om du byter hemlighet måste du ge Prisjakt den <b>nya</b> länken nedan.
        </div>
      </div>

      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }}>
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Alternativ A – Endast taggade produkter</h3>
          <p style={{ marginTop: 4 }}>
            Skicka bara produkter taggade <code>prisjakt</code>. Ger full kontroll över vad som syns på Prisjakt.
          </p>
          <input readOnly value={onlyTagged} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(onlyTagged)}>Kopiera länk</button>
            <a href={onlyTagged} target="_blank" rel="noreferrer" style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}>
              Öppna i ny flik
            </a>
          </div>
        </div>

        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>Alternativ B – Alla produkter</h3>
          <p style={{ marginTop: 4 }}>
            Skicka <b>alla aktiva &amp; publicerade</b> produkter som har lager &gt; 0 (inkl. alla varianter).
          </p>
          <input readOnly value={allProducts} style={{ width: "100%", marginBottom: 8 }} />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => navigator.clipboard.writeText(allProducts)}>Kopiera länk</button>
            <a href={allProducts} target="_blank" rel="noreferrer" style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #ccc", borderRadius: 6 }}>
              Öppna i ny flik
            </a>
          </div>
        </div>
      </div>

      <div style={{ marginTop: 16, padding: 12, border: "1px dashed #ccc", borderRadius: 8 }}>
        <b>Instruktion (skicka till Prisjakt):</b>
        <ol style={{ marginTop: 8, marginBottom: 0 }}>
          <li>Välj en av länkarna ovan.</li>
          <li>Ge länken till Prisjakt för inläsning i deras system.</li>
          <li>Be dem hämta länken var 30–60 minut.</li>
        </ol>
      </div>

      <p style={{ marginTop: 12, color: "#666" }}>Butik: <code>{shop}</code></p>
    </div>
  );
}
