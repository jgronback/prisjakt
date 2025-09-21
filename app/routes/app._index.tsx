// app/routes/app._index.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData, Link } from "@remix-run/react";
import { authenticate } from "../shopify.server";
import { shopify, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;

  // Kolla om butiken redan betalar
  const check = await shopify.billing.check({
    session,
    plans: [BILLING_PLAN],
  });

  return json({ shop, hasActivePayment: check.hasActivePayment });
}

export default function Home() {
  const { shop, hasActivePayment } = useLoaderData<typeof loader>();

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Prisjakt Produktfeed</h1>
      <p style={{ maxWidth: 720, marginBottom: 16 }}>
        Den här appen skapar en <b>XML-produktfeed</b> som Prisjakt kan läsa in. Du kan välja
        att skicka antingen <b>alla aktiva &amp; publicerade produkter med lager</b>, eller
        endast de produkter som du <b>taggat med “prisjakt”</b> i Shopify.
      </p>

      {!hasActivePayment ? (
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8, marginBottom: 16 }}>
          <h3 style={{ marginTop: 0 }}>Starta din gratis provperiod</h3>
          <p style={{ margin: "8px 0 12px" }}>
            Klicka nedan för att aktivera abonnemanget. Du skickas till Shopifys
            kassasida och kommer tillbaka hit automatiskt.
          </p>
          <Link to="/app/billing" style={{ display: "inline-block", padding: "10px 14px", background: "#111", color: "#fff", borderRadius: 8, textDecoration: "none" }}>
            Starta provperiod / Köp
          </Link>
        </div>
      ) : (
        <div style={{ padding: 12, border: "1px solid #cdeccd", background: "#f4fff4", borderRadius: 8, marginBottom: 16 }}>
          <b>Abonnemang aktivt</b> – du kan använda appen fullt ut.
        </div>
      )}

      <ol style={{ lineHeight: 1.6 }}>
        <li>
          Gå till <Link to="/app/settings">Feed settings</Link> och kopiera en av dina feed-länkar.
        </li>
        <li>
          Ge länken till Prisjakt. De <b>hämtar länken hos sig</b> (inget uppdateras i din butik).
          Rekommendation: låt dem hämta <b>var 30–60 minut</b>.
        </li>
        <li>
          Klart! Alla ändringar du gör i Shopify (pris, lager, bilder, beskrivningar) slår igenom automatiskt i
          nästa hämtning (vi cachar i 5 min för snabbhet).
        </li>
      </ol>

      <p style={{ marginTop: 16, color: "#666" }}>
        Butik: <code>{shop}</code>
      </p>
    </div>
  );
}
