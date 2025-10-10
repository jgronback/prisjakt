// app/routes/app.settings.safe.tsx
import type { HeadersFunction } from "@remix-run/node";

export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

export default function SettingsSafe() {
  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1>Settings – SAFE STUB</h1>
      <p>Marker: <code>🧪 settings-safe-v2</code></p>
      <p>Om du ser denna text så renderas rätt route-fil.</p>
    </div>
  );
}
