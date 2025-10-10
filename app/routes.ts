// app/routes.ts
import { defineRoutes } from "@remix-run/dev/config/routes";

export default defineRoutes((route) => {
  // Root
  route("", "routes/_index.tsx"); // "/" (root)

  // App-shell + undersidor (utan inledande slash)
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
  route("admin.prisjakt", "routes/admin.prisjakt.tsx"); // (redirectar du till /app/settings)

  // Webhooks
  route("webhooks/customers/data_request", "routes/webhooks.customers.data_request.tsx");
  route("webhooks/customers/redact", "routes/webhooks.customers.redact.tsx");
  route("webhooks/app/scopes_update", "routes/webhooks.app.scopes_update.tsx");
  route("webhooks/app/uninstalled", "routes/webhooks.app.uninstalled.tsx");
  route("webhooks/shop/redact", "routes/webhooks.shop.redact.tsx");
});
