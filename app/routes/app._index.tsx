// app/routes/app._index.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData, Link } from "@remix-run/react";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;

  // Safe check: om billing saknas i runtime, krascha inte
  let hasActivePayment = false;
  const billingApi: any = (shopify as any).billing;
  if (billingApi?.check) {
    const check = await billingApi.check({ session, plans: [BILLING_PLAN] });
    hasActivePayment = !!check?.hasActivePayment;
  }

  return json({ shop, hasActivePayment, billingAvailable: !!billingApi?.request });
}

export default function Home() {
  const { shop, hasActivePayment, billingAvailable } = useLoaderData<typeof loader>();

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Prisjakt Produktfeed</h1>
      <p style={{ maxWidth: 720, marginBottom: 16 }}>
        Den här appen skapar en <b>XML-produktfeed</b> som Prisjakt kan läsa in. Du kan skicka
        <b> alla aktiva &amp; publicerade produkter med lager</b> – eller endast de du har
        <b> taggat med “prisjakt”</b> i Shopify.
      </p>

      {billingAvailable ? (
        !hasActivePayment ? (
          <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8, marginBottom: 16 }}>
            <h3 style={{ marginTop: 0 }}>Starta din gratis provperiod</h3>
            <p style={{ margin: "8px 0 12px" }}>
              Klicka nedan för att aktivera abonnemanget (Shopifys kassasida öppnas).
            </p>
            <Link to="/app/billing" style={{ display: "inline-block", padding: "10px 14px", background: "#111", color: "#fff", borderRadius: 8, textDecoration: "none" }}>
              Starta provperiod / Köp
            </Link>
          </div>
        ) : (
          <div style={{ padding: 12, border: "1px solid #cdeccd", background: "#f4fff4", borderRadius: 8, marginBottom: 16 }}>
            <b>Abonnemang aktivt</b> – du kan använda appen fullt ut.
          </div>
        )
      ) : (
        <div style={{ padding: 12, border: "1px solid #ffe2a8", background: "#fff8e8", borderRadius: 8, marginBottom: 16 }}>
          <b>Obs:</b> Billing-API saknas i runtime, så sidan kräver inget köp just nu.
          (Appen fungerar ändå medan vi verifierar billing-konfigurationen.)
        </div>
      )}

      <ol style={{ lineHeight: 1.6 }}>
        <li>Gå till <Link to="/app/settings">Feed settings</Link> och kopiera en av dina feed-länkar.</li>
        <li>
          <b>Ge länken till Prisjakt.</b> De hämtar (“crawlar”) den hos sig – <b>inget</b> uppdateras i din butik.
          Rekommendation: låt dem hämta <b>var 30–60 minut</b>.
        </li>
        <li>
          Klart! Dina ändringar i Shopify speglas i nästa hämtning (vi cachar i 5 min för fart).
        </li>
      </ol>

      <p style={{ marginTop: 16, color: "#666" }}>Butik: <code>{shop}</code></p>
    </div>
  );
}
