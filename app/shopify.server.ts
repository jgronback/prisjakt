// app/shopify.server.ts
import { shopifyApp, LATEST_API_VERSION } from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

// Behövs för din import i routes: app.settings.tsx
export const BILLING_PLAN = process.env.BILLING_PLAN || "default";

const appUrl =
  process.env.SHOPIFY_APP_URL ||
  process.env.HOST || // fallback om Vite/HOST används
  "https://prisjakt.vercel.app";

const scopes = (process.env.SHOPIFY_SCOPES || process.env.SCOPES || "")
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY!,
  apiSecretKey: process.env.SHOPIFY_API_SECRET!,
  apiVersion: LATEST_API_VERSION,
  appUrl,
  isEmbeddedApp: true,
  scopes,
  // ✅ RÄTT: fält i objektet, inte en separat const
  sessionStorage: new PrismaSessionStorage(prisma),

  // Billing är valfri – din kod i settings kollar “billingApi?.check”
  // och släpper in även om det saknas, så vi utelämnar det här.
  // Vill du aktivera det senare kan du lägga till "billing" här.
});

// Behövs för din import i routes
export const authenticate = shopify.authenticate;

export default shopify;
