// app/shopify.server.ts
import { shopifyApp, LATEST_API_VERSION } from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

export const BILLING_PLAN = process.env.BILLING_PLAN || "default";

const appUrl =
  process.env.SHOPIFY_APP_URL ||
  process.env.HOST ||
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
  sessionStorage: new PrismaSessionStorage(prisma),
});

// Dessa två används av din app:
export const authenticate = shopify.authenticate;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;

export default shopify;
