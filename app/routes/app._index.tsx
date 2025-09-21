// app/routes/app._index.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData, Link } from "@remix-run/react";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
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

  // Försök läsa billing-status, men blockera inte Home om det saknas
  let hasActivePayment = false;
  const billingApi: any = (shopify as any).billing;
  if (billingApi?.check) {
    try {
      const check = await billingApi.check({ session, plans: [BILLING_PLAN] });
      hasActivePayment = !!check?.hasActivePayment;
    } catch {}
  }

  return json({
    shop,
    hasActivePayment,
    billingAvailable: !!billingApi?.request,
  });
}

export default function Home() {
  const { shop, hasActivePayment, billingAvailable } =
    useLoaderData<typeof loader>();

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Prisjakt Produktfeed</h1>

      {!hasActivePayment && (
        <div
          style={{
            padding: 12,
            border: "1px solid #ddd",
            borderRadius: 8,
            marginBottom: 16,
          }}
        >
          <h3 style={{ marginTop: 0 }}>Starta din gratis provperiod</h3>
          {!billingAvailable && (
            <p
              style={{
                margin: "8px 0 12px",
                background: "#fff8e8",
                border: "1px solid #ffe2a8",
                padding: 8,
                borderRadius: 6,
              }}
            >
              Obs: Billing-API saknas i runtime — du kan ändå testa att starta
              köpet nedan.
            </p>
          )}
          <Link
            to="/app/billing"
            style={{
              display: "inline-block",
              padding: "10px 14px",
              background: "#111",
              color: "#fff",
              borderRadius: 8,
              textDecoration: "none",
            }}
          >
            Starta provperiod / Köp
          </Link>
        </div>
      )}

      <p style={{ maxWidth: 720 }}>
        Den här appen skapar en <b>XML-produktfeed</b> som Prisjakt läser in.
        Du kan skicka <b>alla aktiva &amp; publicerade produkter med lager &gt; 0</b>{" "}
        eller endast de du <b>taggat med “prisjakt”</b>. Gå till{" "}
        <Link to="/app/settings">Feed settings</Link> för att kopiera länk.
      </p>

      <p style={{ marginTop: 16, color: "#666" }}>
        Butik: <code>{shop}</code>
      </p>
    </div>
  );
}
