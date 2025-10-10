// app/routes/prisjakt.health.ts
import { json, type LoaderFunctionArgs } from "@remix-run/node";

export async function loader(_args: LoaderFunctionArgs) {
  return json({
    ok: true,
    service: "prisjakt-app",
    time: new Date().toISOString(),
  });
}
