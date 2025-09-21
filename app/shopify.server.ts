// app/shopify.server.ts
import "@shopify/shopify-app-remix/adapters/node";
import {
  shopifyApp,
  ApiVersion,
  AppDistribution,
  BillingInterval,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

// Plan-namnet måste vara exakt samma som i dina routes (Home/Settings/Billing)
export const BILLING_PLAN = "Prisjakt produktfeed – Månadsvis";

export const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY!,          // måste vara satt i Vercel
  apiSecretKey: process.env.SHOPIFY_API_SECRET!, // måste vara satt i Vercel
  apiVersion: ApiVersion.January25,
  appUrl: process.env.SHOPIFY_APP_URL!,          // t.ex. https://prisjakt.vercel.app
  authPathPrefix: "/auth",
  distribution: AppDistribution.AppStore,
  scopes: (process.env.SHOPIFY_SCOPES || "read_products,read_inventory")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),
  sessionStorage: new PrismaSessionStorage(prisma),

  // 🔑 Aktivera Billing-API i runtime
  billing: {
    [BILLING_PLAN]: {
      amount: 10,
      currencyCode: "USD",
      interval: BillingInterval.Every30Days,
      trialDays: 7,
    },
  },

  future: {
    unstable_newEmbeddedAuthStrategy: true,
    removeRest: true,
  },

  // Valfritt: om du har custom shop-domän
  ...(process.env.SHOP_CUSTOM_DOMAIN
    ? { customShopDomains: [process.env.SHOP_CUSTOM_DOMAIN] }
    : {}),
});

export const authenticate = shopify.authenticate;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;

export default shopify;
