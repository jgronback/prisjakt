import crypto from "crypto";

export async function verifyShopifyWebhook(request: Request): Promise<string | null> {
  const hmac = request.headers.get("x-shopify-hmac-sha256") || "";
  const secret = process.env.SHOPIFY_API_SECRET || "";
  const raw = await request.text(); // läs rå body
  const digest = crypto.createHmac("sha256", secret).update(raw, "utf8").digest("base64");
  if (crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(hmac))) {
    return raw;
  }
  return null;
}
