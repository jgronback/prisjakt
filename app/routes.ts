// app/routes.ts
export default [
  // Root
  { path: "", file: "routes/_index.tsx" },

  // App-shell + undersidor
  {
    path: "app",
    file: "routes/app.tsx",
    children: [
      { index: true, file: "routes/app._index.tsx" },        // /app
      { path: "settings", file: "routes/app.settings.tsx" }, // /app/settings
      { path: "billing",  file: "routes/app.billing.tsx" },  // /app/billing
    ],
  },

  // Auth
  { path: "auth/login", file: "routes/auth.login/route.tsx" },
  { path: "auth/:param", file: "routes/auth.$.tsx" },

  // Publikt & util
  { path: "public/prisjakt.xml", file: "routes/public.prisjakt[.]xml.tsx" },
  { path: "api/prisjakt.xml",    file: "routes/api.prisjakt[.]xml.tsx" },
  { path: "prisjakt.health",     file: "routes/prisjakt.health.ts" },
  { path: "admin.prisjakt",      file: "routes/admin.prisjakt.tsx" },

  // Webhooks
  { path: "webhooks/customers/data_request", file: "routes/webhooks.customers.data_request.tsx" },
  { path: "webhooks/customers/redact",       file: "routes/webhooks.customers.redact.tsx" },
  { path: "webhooks/app/scopes_update",      file: "routes/webhooks.app.scopes_update.tsx" },
  { path: "webhooks/app/uninstalled",        file: "routes/webhooks.app.uninstalled.tsx" },
  { path: "webhooks/shop/redact",            file: "routes/webhooks.shop.redact.tsx" },

];
