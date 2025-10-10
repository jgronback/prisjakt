// app/shopify.server.ts
import { shopifyApp, LATEST_API_VERSION } from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

export const BILLING_PLAN = "DEFAULT_PLAN"; // används av din settings-route vid check

const SCOPES =
  (process.env.SHOPIFY_SCOPES || process.env.SCOPES || "read_products,read_product_listings,read_inventory")
    .split(",")
    .map(s => s.trim())
    .filter(Boolean);

const shopify = shopifyApp({
  api: { apiVersion: LATEST_API_VERSION },
  apiKey: process.env.SHOPIFY_API_KEY!,
  apiSecretKey: process.env.SHOPIFY_API_SECRET!,
  appUrl: process.env.SHOPIFY_APP_URL!, // ex: https://prisjakt.vercel.app
  scopes: SCOPES,

  // sessions i Postgres via Prisma (Neon)
  sessionStorage: new PrismaSessionStorage(prisma),

  // Billing kan vara avstängt – din kod kollar redan billing?.check defensivt
  billing: undefined,
});

export default shopify;

// Exponera exakt det som routes importerar
export const { authenticate, login, addDocumentResponseHeaders } = shopify;
