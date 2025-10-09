import type { HeadersFunction } from "@remix-run/node";
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";

/**
 * Säkerställ att appen kan bäddas in i Shopify-admin.
 * Vi bevarar ev. befintliga headers och lägger endast till frame-ancestors
 * om den inte redan finns.
 */
export const headers: HeadersFunction = ({ loaderHeaders }) => {
  // Behåll alla headers som redan satts av loaders m.m.
  const headers = new Headers(loaderHeaders);

  const existing = headers.get("Content-Security-Policy")?.trim() || "";
  const hasFrameAncestors = /(^|;)\s*frame-ancestors\b/i.test(existing);

  if (!hasFrameAncestors) {
    const needsSemicolon = existing && !existing.trim().endsWith(";");
    const base = existing ? `${existing}${needsSemicolon ? ";" : ""} ` : "";
    const frameAncestors =
      "frame-ancestors https://admin.shopify.com https://*.myshopify.com;";
    headers.set("Content-Security-Policy", `${base}${frameAncestors}`);
  }

  return headers;
};

export default function App() {
  return (
    <html>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1" />
        <link rel="preconnect" href="https://cdn.shopify.com/" />
        <link
          rel="stylesheet"
          href="https://cdn.shopify.com/static/fonts/inter/v4/styles.css"
        />
        <Meta />
        <Links />
      </head>
      <body>
        <Outlet />
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}
