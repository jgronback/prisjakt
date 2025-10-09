// app/routes/app.settings.tsx
import * as React from "react";
import type { LoaderFunctionArgs, HeadersFunction } from "@remix-run/node";
import { json, redirect } from "@remix-run/node";
import { useLoaderData, Link } from "@remix-run/react";
import { PrismaClient } from "@prisma/client";
import { authenticate } from "~/shopify.server"; // finns i ditt repo

// Minimal CSP här också (root.tsx sätter redan detta, men vi dubblar för säkerhets skull)
export const headers: HeadersFunction = () => ({
  "Content-Security-Policy":
    "frame-ancestors https://admin.shopify.com https://*.myshopify.com;",
});

const prisma =
  (globalThis as any).prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") (globalThis as any).prisma = prisma;

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shopParam = url.searchParams.get("shop") || "";
  const host = url.searchParams.get("host") || "";

  // 1) Försök autentisera (embedded/vanlig)
  try {
    const { session } = await authenticate.admin(request);
    const shop = session.shop;

    // Hämta ev. befintliga settings (valfritt – bara för att visa något)
    const settings = await prisma.shopSettings.findUnique({ where: { shop } }).catch(() => null);

    return json({ shop, hasSettings: !!settings, feedSecretSet: !!settings?.feedSecret });
  } catch {
    // 2) Ingen session => skickas via login
    if (shopParam) {
      // retur efter login till /app/settings
      const ret = `/auth/login?shop=${encodeURIComponent(shopParam)}${host ? `&host=${encodeURIComponent(host)}` : ""}&return_to=${encodeURIComponent("/app/settings")}`;
      throw redirect(ret);
    }
    // helt “kall” öppning – be om shop-domän
    throw redirect("/auth/login");
  }
}

export default function SettingsPage() {
  const data = useLoaderData<typeof loader>();
  return (
    <div style={{ maxWidth: 760, margin: "40px auto", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ marginBottom: 8 }}>Prisjakt – Inställningar</h1>
      <p style={{ color: "#555", marginTop: 0 }}>
        Shop: <strong>{data.shop}</strong>
      </p>

      <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 12, marginTop: 16 }}>
        <p style={{ margin: 0 }}>
          {data.feedSecretSet ? "feedSecret finns sparat." : "Ingen feedSecret hittad ännu."}
          {" "}
          Gå till din befintliga inställningsvy i appen om du har en, annars kan vi lägga till UI här i nästa steg.
        </p>
        <p style={{ margin: "12px 0 0" }}>
          Förhandsvisa feeden via din publika route (om du har satt feedSecret):
        </p>
        <ul style={{ marginTop: 8 }}>
          <li>
            <Link to="/public.prisjakt.xml">/public.prisjakt.xml</Link>{" "}
            (lägg till <code>?shop=&lt;shop&gt;&amp;sig=&lt;secret&gt;&amp;tag=prisjakt</code>)
          </li>
        </ul>
      </div>
    </div>
  );
}

// Hjälper till att visa fel i UI istället för “Unexpected Server Error”
export function ErrorBoundary({ error }: { error: unknown }) {
  const msg = error instanceof Error ? error.message : String(error);
  return (
    <div style={{ maxWidth: 760, margin: "40px auto", fontFamily: "system-ui, sans-serif", color: "#b00020" }}>
      <h2>Inställningar kunde inte laddas</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{msg}</pre>
      <p>Testa att öppna via: <code>/auth/login?shop=&lt;din-shop.myshopify.com&gt;</code> och försök igen.</p>
    </div>
  );
}
