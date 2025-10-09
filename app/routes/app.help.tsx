// app/routes/app.help.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";
import { Link } from "@remix-run/react";
import { authenticate } from "../shopify.server";

export async function loader({ request }: LoaderFunctionArgs) {
  await authenticate.admin(request);
  return null;
}

export default function HelpPage() {
  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 900 }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Hjälp & FAQ</h1>

      <h3>Vad gör appen?</h3>
      <p>Skapar en XML-feed som Prisjakt läser in. Inget uppdateras i din butik – Prisjakt “hämtar” länken.</p>

      <h3>Hur väljer jag vilka produkter som skickas?</h3>
      <ul>
        <li><b>Alternativ A:</b> Tagga produkter i Shopify med <code>prisjakt</code>.</li>
        <li><b>Alternativ B:</b> Skicka alla aktiva &amp; publicerade produkter med lager &gt; 0.</li>
      </ul>

      <h3>Hur snabbt uppdateras priser/lagersaldo?</h3>
      <p>Feeden speglar dina ändringar inom ca <b>5 min</b> (cache). När Prisjakt läser in igen syns ändringen hos dem.
         Be Prisjakt hämta var <b>30–60 minuter</b>.</p>

      <h3>Vanliga orsaker till tom feed</h3>
      <ul>
        <li>Produkter saknar lager &gt; 0 (i Alternativ B).</li>
        <li>Produkter saknar taggen <code>prisjakt</code> (i Alternativ A).</li>
        <li>Produkten är inte <b>Active</b> och <b>Published</b>.</li>
        <li>Fel “kod” (sig) i länken – rotera koden på <Link to="/app/settings">Feed settings</Link> och ge Prisjakt den nya länken.</li>
      </ul>

      <h3>Behöver du hjälp?</h3>
      <p>Maila support: <a href="mailto:kontakt@nordicaim.se">kontakt@nordicaim.se</a></p>
    </div>
  );
}
