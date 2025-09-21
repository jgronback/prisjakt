// app/routes/app.help/route.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { authenticate } from "../../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  await authenticate.admin(request);
  return null;
}

export default function HelpPage() {
  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 900 }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Hjälp & FAQ</h1>

      <h3>Vad gör appen?</h3>
      <p>Skapar en XML-produktfeed som Prisjakt läser in. Inget uppdateras i din butik.</p>

      <h3>Hur väljer jag vilka produkter som skickas?</h3>
      <ul>
        <li><b>Alternativ A:</b> Tagga produkter i Shopify med <code>prisjakt</code>.</li>
        <li><b>Alternativ B:</b> Skicka alla <b>aktiva &amp; publicerade</b> med lager &gt; 0.</li>
      </ul>

      <h3>Hur snabbt uppdateras det på Prisjakt?</h3>
      <p>Feeden speglar dina ändringar inom ca <b>5 min</b> (cache). Prisjakt bör läsa in var <b>30–60 min</b>.</p>

      <h3>Vanliga orsaker till tom feed</h3>
      <ul>
        <li>Ingen lagerstatus &gt; 0 (i “Alla produkter”).</li>
        <li>Saknar taggen <code>prisjakt</code> (i “Endast taggade”).</li>
        <li>Produkten är inte <b>Active</b> och <b>Published</b>.</li>
        <li>Fel “kod” (sig) i länken – byt kod på <code>Feed settings</code> och ge Prisjakt den nya länken.</li>
      </ul>

      <h3>Support</h3>
      <p>Maila: <a href="mailto:kontakt@nordicaim.se">kontakt@nordicaim.se</a></p>
    </div>
  );
}
