// app/shopify.server.ts
import "@shopify/shopify-app-remix/adapters/node";
import {
  ApiVersion,
  AppDistribution,
  shopifyApp,
  BillingInterval,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

// Namn på din plan som visas i Shopifys checkout
export const BILLING_PLAN = "Prisjakt produktfeed – Månadsvis";

// OBS: exakt EN shopifyApp-konfiguration
export const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY!,               // lägg i Vercel
  apiSecretKey: process.env.SHOPIFY_API_SECRET || "", // lägg i Vercel
  apiVersion: ApiVersion.January25,
  // Använd SHOPIFY_SCOPES (eller fallback till SCOPES om du råkar ha det)
  scopes: (process.env.SHOPIFY_SCOPES || process.env.SCOPES || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),                                  // t.ex. "read_products,read_inventory"
  appUrl: process.env.SHOPIFY_APP_URL || "",           // t.ex. https://prisjakt.vercel.app
  authPathPrefix: "/auth",
  sessionStorage: new PrismaSessionStorage(prisma),
  distribution: AppDistribution.AppStore,
  future: {
    unstable_newEmbeddedAuthStrategy: true,
    removeRest: true,
  },
  ...(process.env.SHOP_CUSTOM_DOMAIN
    ? { customShopDomains: [process.env.SHOP_CUSTOM_DOMAIN] }
    : {}),

  // ← Billing inuti samma objekt
  billing: {
    [BILLING_PLAN]: {
      amount: 10.0,                      // månadspris
      currencyCode: "USD",
      interval: BillingInterval.Every30Days,
      trialDays: 7,                      // gratis provperiod
    },
  },
});

export default shopify;
export const apiVersion = ApiVersion.January25;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const authenticate = shopify.authenticate;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;
export const sessionStorage = shopify.sessionStorage;
