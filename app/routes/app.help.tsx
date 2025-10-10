// app/routes/app.help.tsx
export default function HelpPage() {
  return (
    <div style={{ padding: 16, fontFamily: "Inter, system-ui, sans-serif", maxWidth: 800 }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Hjälp & FAQ</h1>
      <p>Ge länken från <b>Feed settings</b> till Prisjakt under <i>Data management → Lägg till feed</i>. Välj “Prisjakt XML (rekommenderad)”.</p>
      <ul>
        <li><b>Uppdateringar:</b> Feeden speglar Shopify-ändringar inom ~5 min cache. När Prisjakt läser in igen syns ändringen hos dem.</li>
        <li><b>Taggade produkter:</b> Använd taggen <code>prisjakt</code> om du väljer alternativ A.</li>
        <li><b>Byte av kod:</b> Rotera koden i Settings om Prisjakt får 403. Glöm inte uppdatera URL hos Prisjakt.</li>
      </ul>
    </div>
  );
}
