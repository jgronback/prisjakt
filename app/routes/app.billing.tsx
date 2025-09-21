// app/routes/app.billing.tsx
import { redirect, type LoaderFunctionArgs } from "@remix-run/node";
import shopify, { authenticate, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);

  const billingApi: any = (shopify as any).billing;
  if (!billingApi?.request || !billingApi?.check) {
    // Billing saknas i runtime – gå hem utan att krascha
    return redirect("/app");
  }

  const check = await billingApi.check({ session, plans: [BILLING_PLAN] });
  if (check?.hasActivePayment) {
    return redirect("/app");
  }

  const returnUrl = `${(process.env.SHOPIFY_APP_URL || "").replace(/\/$/, "")}/app`;
  const req = await billingApi.request({
    session,
    plan: BILLING_PLAN,
    isTest: process.env.NODE_ENV !== "production",
    returnUrl,
  });

  return redirect(req.confirmationUrl);
}
