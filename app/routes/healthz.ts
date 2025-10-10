// app/routes/healthz.ts
import type { LoaderFunctionArgs } from "@remix-run/node";
export async function loader({}: LoaderFunctionArgs) {
  return new Response("ok", { headers: { "Content-Type": "text/plain" } });
}
