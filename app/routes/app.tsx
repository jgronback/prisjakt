// app/routes/app.tsx
import type { HeadersFunction, LoaderFunctionArgs } from "@remix-run/node";
import { Outlet, useLoaderData, useRouteError } from "@remix-run/react";
import { boundary } from "@shopify/shopify-app-remix/server";
import { AppProvider } from "@shopify/shopify-app-remix/react";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";
import { authenticate } from "../shopify.server";

export const links = () => [{ rel: "stylesheet", href: polarisStyles }];

export const loader = async ({ request }: LoaderFunctionArgs) => {
  await authenticate.admin(request);
  return { apiKey: process.env.SHOPIFY_API_KEY || "" };
};

export default function App() {
  const { apiKey } = useLoaderData<typeof loader>();
  return (
    <AppProvider isEmbeddedApp apiKey={apiKey}>
      {/* Viktigt: Admin letar efter <ui-nav-menu> + <a data-discover="true"> */}
      <ui-nav-menu>
  <a rel="home" data-discover="true" href="/app">Hem</a>
  <a data-discover="true" href="/app/settings">Inställningar Feed</a>
  <a data-discover="true" href="/app/help">Hjälp/FAQ</a>
</ui-nav-menu>
      <Outlet />
    </AppProvider>
  );
}

export function ErrorBoundary() {
  return boundary.error(useRouteError());
}
export const headers: HeadersFunction = (args) => boundary.headers(args);
