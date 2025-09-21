import { json, redirect, type LoaderFunctionArgs, type ActionFunctionArgs } from "@remix-run/node";
import { useLoaderData, Form, useNavigation } from "@remix-run/react";
import { PrismaClient } from "@prisma/client";
import { authenticate } from "../shopify.server";

const prisma = new PrismaClient();

function randomSecret(len = 40) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;

  let settings = await prisma.shopSettings.findUnique({ where: { shop } });
  if (!settings) {
    settings = await prisma.shopSettings.create({
      data: { shop, feedSecret: randomSecret() },
    });
  }

  const base = process.env.SHOPIFY_APP_URL?.replace(/\/$/, "") || new URL(request.url).origin;
  const feedUrl = `${base}/public/prisjakt.xml?shop=${shop}&tag=prisjakt&sig=${settings.feedSecret}`;
  const feedUrlAll = `${base}/public/prisjakt.xml?shop=${shop}&tag=all&sig=${settings.feedSecret}`;

  return json({ shop, feedSecret: settings.feedSecret, feedUrl, feedUrlAll });
}

export async function action({ request }: ActionFunctionArgs) {
  const { session } = await authenticate.admin(request);
  const shop = session.shop;
  const form = await request.formData();
  if (form.get("rotate") === "1") {
    const newSecret = randomSecret();
    await prisma.shopSettings.upsert({
      where: { shop },
      update: { feedSecret: newSecret },
      create: { shop, feedSecret: newSecret },
    });
  }
  return redirect("/app/settings");
}

export default function SettingsPage() {
  const { shop, feedSecret, feedUrl, feedUrlAll } = useLoaderData<typeof loader>();
  const nav = useNavigation();
  const busy = nav.state !== "idle";

  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 20, marginBottom: 12 }}>Prisjakt feed – inställningar</h1>
      <div style={{ marginBottom: 12 }}>Butik: <b>{shop}</b></div>

      <div style={{ marginBottom: 8 }}>
        <div>Nuvarande hemlighet (sig):</div>
        <code>{feedSecret}</code>
      </div>

      <Form method="post" replace>
        <input type="hidden" name="rotate" value="1" />
        <button type="submit" disabled={busy} style={{ padding: "8px 12px" }}>
          {busy ? "Rotera..." : "Rotera hemlighet"}
        </button>
      </Form>

      <hr style={{ margin: "16px 0" }} />

      <div style={{ marginBottom: 8 }}>Feed-URL (taggade med <code>prisjakt</code>):</div>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input id="feed1" readOnly value={feedUrl} style={{ width: "100%" }} />
        <button onClick={() => navigator.clipboard.writeText(feedUrl)}>Kopiera</button>
      </div>

      <div style={{ marginTop: 12, marginBottom: 8 }}>Feed-URL (alla aktiva/publicerade med lager):</div>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input id="feed2" readOnly value={feedUrlAll} style={{ width: "100%" }} />
        <button onClick={() => navigator.clipboard.writeText(feedUrlAll)}>Kopiera</button>
      </div>

      <p style={{ marginTop: 12, color: "#666" }}>
        Ge den här länken till Prisjakt. Uppdatering var 30–60 min är lagom.
      </p>
    </div>
  );
}
