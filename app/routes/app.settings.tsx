// app/routes/app.settings.tsx
import type { HeadersFunction } from "@remix-run/node";

export const headers: HeadersFunction = () => ({
  // tillåt inbäddning i Shopify-admin
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

export default function SettingsSmokeTest() {
  // visa vilken build som faktiskt körs på Vercel
  const sha =
    (typeof process !== "undefined" && process.env.VERCEL_GIT_COMMIT_SHA) || "";
  const shortSha = sha ? sha.slice(0, 7) : "local";

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1>Settings – smoke test</h1>
      <p>Den här sidan har ingen loader, ingen DB, ingen Shopify-kod.</p>
      <p>Om du ser detta renderar servern den nya filen.</p>
      <pre>
        build: {shortSha} | {new Date().toISOString()}
      </pre>
    </div>
  );
}
