import { verifyShopifyWebhook } from "../utils/verifyShopifyWebhook";

export async function action({ request }: { request: Request }) {
  const raw = await verifyShopifyWebhook(request);
  if (!raw) return new Response("unauthorized", { status: 401 });
  // TODO: hantera om du vill (valfritt)
  return new Response("ok");
}

export function loader() {
  return new Response("Method Not Allowed", { status: 405 });
}
