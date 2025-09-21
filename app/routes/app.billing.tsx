// app/routes/app.billing.tsx
import { redirect, type LoaderFunctionArgs } from "@remix-run/node";
import { authenticate, shopify, BILLING_PLAN } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);

  // Har butiken redan ett aktivt köp? Skicka hem.
  const check = await shopify.billing.check({ session, plans: [BILLING_PLAN] });
  if (check.hasActivePayment) {
    return redirect("/app");
  }

  // Annars: be Shopify skapa en checkout-länk
  const req = await shopify.billing.request({
    session,
    plan: BILLING_PLAN,
    isTest: process.env.NODE_ENV !== "production",      // dev-butiker = test charges
    returnUrl: `${process.env.SHOPIFY_APP_URL?.replace(/\/$/, "") || ""}/app`,
  });

  // Skicka användaren till Shopifys confirm-sida
  return redirect(req.confirmationUrl);
}
