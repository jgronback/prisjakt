// app/routes/prisjakt.health.ts
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import prisma from "~/db.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const env = {
    HAS_DATABASE_URL: !!process.env.DATABASE_URL,
    SHOPIFY_APP_URL: process.env.SHOPIFY_APP_URL || null,
  };

  const db = { ok: false, error: null as null | string, sessionCount: null as null | number, shopSettingsCount: null as null | number };

  try {
    // enkel ping
    await prisma.$queryRaw`SELECT 1`;
    db.ok = true;

    // tabell-prover (sväljer fel så vi ser om tabellerna saknas)
    try { db.sessionCount = await prisma.session.count(); } catch (e: any) { db.sessionCount = -1; }
    try { db.shopSettingsCount = await prisma.shopSettings.count(); } catch (e: any) { db.shopSettingsCount = -1; }
  } catch (e: any) {
    db.ok = false;
    db.error = e?.message || String(e);
  }

  return json({ env, db }, { headers: { "Cache-Control": "no-store" } });
}
