import type { HeadersFunction } from "@remix-run/node";
import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";

// ✅ Tvinga rätt CSP globalt + neutralisera X-Frame-Options
export const headers: HeadersFunction = () => ({
  // Tillåt inbäddning i Shopify-admin
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com https://*.shopify.com;",
  // Neutralisera ev. strikt header från annan middleware/proxy
  // (Chrome ignorerar ogiltigt värde; om flera headers finns brukar den sista vinna)
  "X-Frame-Options": "ALLOWALL",
});

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
