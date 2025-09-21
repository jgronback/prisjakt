import "@shopify/shopify-app-remix/adapters/node";
import {
  ApiVersion,
  AppDistribution,
  shopifyApp,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";


const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET || "",
  apiVersion: ApiVersion.January25,
  scopes: process.env.SCOPES?.split(","),
  appUrl: process.env.SHOPIFY_APP_URL || "",
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
});

export default shopify;
export const apiVersion = ApiVersion.January25;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const authenticate = shopify.authenticate;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;
export const sessionStorage = shopify.sessionStorage;


// app/shopify.server.ts (visa bara relevanta rader/ändringar)
import { shopifyApp, BillingInterval } from "@shopify/shopify-app-remix/server";
// ...dina befintliga imports (Prisma session storage etc.)

export const BILLING_PLAN = "Prisjakt produktfeed – Månadsvis";

export const shopify = shopifyApp({
  // ...dina befintliga options: apiKey, apiSecretKey, appUrl, scopes, sessionStorage, etc.
  billing: {
    [BILLING_PLAN]: {
      amount: 10.0,               // månadspris
      currencyCode: "USD",       // håll dig till USD för enkelhet
      interval: BillingInterval.Every30Days,
      trialDays: 7,              // gratis provperiod
    },
  },
});

// exportera ev. shopify själv också om du inte redan gör det:
export { shopify };
