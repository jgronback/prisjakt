// app/routes.ts
// OBS: Ingen import här. Remix kallar default-exporten med "route"-funktionen.

export default function (route: any) {
  // Root
  route("", "routes/_index.tsx"); // "/"

  // App-shell + undersidor
  route("app", "routes/app.tsx", () => {
    route("", "routes/app._index.tsx");           // /app
    route("settings", "routes/app.settings.tsx"); // /app/settings
    route("billing", "routes/app.billing.tsx");   // /app/billing
    route("help", "routes/app.help/route.tsx");   // /app/help
  });

  // Auth
  route("auth/login", "routes/auth.login/route.tsx"); // /auth/login
  route("auth/:param", "routes/auth.$.tsx");          // /auth/<dynamic>

  // Publika/praktiska endpoints
  route("public/prisjakt.xml", "routes/public.prisjakt[.]xml.tsx");
  route("api/prisjakt.xml", "routes/api.prisjakt[.]xml.tsx");
  route("prisjakt.health", "routes/prisjakt.health.ts");
  route("admin.prisjakt", "routes/admin.prisjakt.tsx"); // (kan redirecta till /app/settings)

  // Webhooks
  route("webhooks/customers/data_request", "routes/webhooks.customers.data_request.tsx");
  route("webhooks/customers/redact", "routes/webhooks.customers.redact.tsx");
  route("webhooks/app/scopes_update", "routes/webhooks.app.scopes_update.tsx");
  route("webhooks/app/uninstalled", "routes/webhooks.app.uninstalled.tsx");
  route("webhooks/shop/redact", "routes/webhooks.shop.redact.tsx");
}
