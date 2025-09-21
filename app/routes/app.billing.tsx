// app/routes/app.billing.tsx
import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

async function runBilling(request: Request) {
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

  const billingApi: any = (shopify as any).billing;
  if (!billingApi?.request) {
    // Billing-API saknas i runtime → tillbaka till /app med notice
    const back = new URL("/app?billing_unavailable=1", process.env.SHOPIFY_APP_URL || new URL(request.url).origin).toString();
    return new Response(`<!doctype html><script>window.top?window.top.location.href=${JSON.stringify(back)}:window.location.href=${JSON.stringify(back)}</script>`,
      { headers: { "Content-Type": "text/html" } });
  }

  const base = (process.env.SHOPIFY_APP_URL || new URL(request.url).origin).replace(/\/$/, "");
  const returnUrl = `${base}/app`;
  const isTest = true; // dev-store testköp

  const { confirmationUrl } = await billingApi.request({
    session,
    plan: BILLING_PLAN,
    isTest,
    returnUrl,
  });

  return new Response(
    `<!doctype html><script>
       if (window.top) window.top.location.href=${JSON.stringify(confirmationUrl)};
       else window.location.href=${JSON.stringify(confirmationUrl)};
     </script>`,
    { headers: { "Content-Type": "text/html" } }
  );
}

export async function loader(args: LoaderFunctionArgs) {
  return runBilling(args.request);
}
export async function action(args: ActionFunctionArgs) {
  return runBilling(args.request);
}

export default function BillingRedirect() {
  return null;
}
