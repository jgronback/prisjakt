// app/routes/app._index.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  let session;
  try {
    ({ session } = await authenticate.admin(request));
  } catch (err: any) {
    if (err instanceof Response && err.status >= 300 && err.status < 400) {
      const abs = new URL(err.headers.get("Location") || "/auth/login", process.env.SHOPIFY_APP_URL || new URL(request.url).origin).toString();
      return new Response(`<!doctype html><script>window.top?window.top.location.href=${JSON.stringify(abs)}:window.location.href=${JSON.stringify(abs)}</script>`,
        { headers: { "Content-Type": "text/html" } });
    }
    throw err;
  }

  const shop = session.shop;

  // Försök läsa billing-status (blockera inte sidan om det misslyckas)
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
  const { shop, hasActivePayment, billingAvailable } = useLoaderData<typeof loader>();

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Prisjakt Produktfeed</h1>

      {!hasActivePayment && (
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8, marginBottom: 16 }}>
          <h3 style={{ marginTop: 0 }}>Starta din gratis provperiod</h3>
          {!billingAvailable && (
            <p style={{ margin: "8px 0 12px", background: "#fff8e8", border: "1px solid #ffe2a8", padding: 8, borderRadius: 6 }}>
              Obs: Billing-API saknas i runtime — testa ändå att starta köpet nedan.
            </p>
          )}
          <form method="post" action="/app/billing">
            <button type="submit" style={{ padding: "10px 14px", background: "#111", color: "#fff", borderRadius: 8, border: 0 }}>
              Starta provperiod / Köp
            </button>
          </form>
        </div>
      )}

      <p style={{ maxWidth: 720 }}>
        Den här appen skapar en <b>XML-produktfeed</b> som Prisjakt läser in.
        Du kan skicka <b>alla aktiva &amp; publicerade produkter med lager &gt; 0</b> eller endast
        de du <b>taggat med “prisjakt”</b>. Gå till <a href="/app/settings">Feed settings</a> för att kopiera länk.
      </p>

      <p style={{ marginTop: 16, color: "#666" }}>Butik: <code>{shop}</code></p>
    </div>
  );
}
