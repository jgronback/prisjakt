"""Tekniksidor: Hem, Så fungerar en värmekamera, Sensor, Optik & räckvidd."""
from build import (na, nalink, ext, eyebrow, page_hero, article_open, article_close, sec, callout,
                   short_answer, table, deflist, ul, ol, muted, product_card, card_grid, guide_tiles,
                   fov_deg, width_at, footprint_cm, sv, SITE_NAME, NA_NAME, SISTER)
import diagrams as D


# ---------------------------------------------------------------------------
# HEM
# ---------------------------------------------------------------------------
def index() -> dict:
    hero_img = "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791&width=1200"
    body = f'''
  <div>
    <section style="background:#fff;border-bottom:1px solid var(--mist-200)">
      <div class="hero-grid" style="max-width:1180px;margin:0 auto;padding:72px 24px 56px">
        <div style="display:flex;flex-direction:column;gap:20px">
          {eyebrow("Teknisk guide till värmekameror")}
          <h1 style="font-size:clamp(36px,5vw,58px);font-weight:800;line-height:1.02">Värmekamera.<br>Så fungerar den, på riktigt.</h1>
          <p style="font-size:19px;line-height:1.55;color:var(--text-muted)">En värmekamera ser temperatur i stället för ljus. Här förklarar vi exakt hur det går till, från strålningen som lämnar djuret till bilden i okularet, och vad varje siffra i databladet betyder i skogen.</p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
            <a class="btn btn-primary btn-lg" href="sa-fungerar-en-varmekamera.html">Läs stora guiden</a>
            <a href="kopguide.html" class="h2" style="padding:12px 16px;border-radius:8px;font-weight:600;color:var(--text-strong)">Köpguide för jakt →</a>
          </div>
          <p style="font-size:14px;color:var(--text-faint)">En sajt från {NA_NAME}. Produktlänkar går till nordicaim.se. <a href="om.html">Läs om samarbetet</a>.</p>
        </div>
        <div>
          <div style="position:relative;border-radius:18px;overflow:hidden;background:var(--gunmetal-800);min-height:360px;display:flex;align-items:center;justify-content:center;padding:24px">
            <img src="{hero_img}" alt="Pulsar Telos XP50 LRF värmekamera med 640×480-sensor och laseravståndsmätare" width="900" height="675" style="max-width:100%;height:auto;object-fit:contain;filter:drop-shadow(0 18px 40px rgba(0,0,0,.45))" fetchpriority="high">
            <a href="{na('/products/pulsar-telos-xp50-lrf-640x480-varmekamera-med-laseravstandsmatare')}" target="_blank" rel="noopener sponsored" style="position:absolute;left:16px;bottom:16px;background:rgba(14,19,22,.85);color:#fff;padding:10px 14px;border-radius:10px;display:flex;flex-direction:column;font-size:13px;text-decoration:none">
              <span style="font-weight:700">Pulsar Telos XP50 LRF</span><span style="color:var(--mist-400)">640×480 · 17 µm · NETD &lt;18 mK · Se hos Nordic Aim →</span>
            </a>
          </div>
        </div>
      </div>
      <div style="height:6px;background:var(--thermal-ironbow)"></div>
    </section>

    <section style="max-width:1180px;margin:0 auto;padding:48px 24px 8px">
      {short_answer("En värmekamera registrerar den infraröda strålning (8–14 µm) som alla föremål avger på grund av sin temperatur. En germaniumlins fokuserar strålningen på en mikrobolometer, en sensor med tusentals element som ändrar elektrisk resistans när de värms. Skillnaderna läses av 50 gånger per sekund, bildbehandlas och visas som gråskala eller färgpalett. Kameran behöver inget ljus, men ser inte genom glas, vatten eller tät vegetation.")}
    </section>

    <section style="max-width:1180px;margin:0 auto;padding:40px 24px">
      <div class="quick-grid">
        <div style="display:flex;flex-direction:column;gap:8px">
          {eyebrow("Har du bråttom?")}
          <h2 style="font-size:26px;font-weight:800">Fyra siffror som styr vad du ser</h2>
          <a href="kopguide.html" style="font-weight:600">Till köpguiden →</a>
        </div>
        <div style="background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:6px"><strong>Brännvidd</strong><span style="font-size:14px;line-height:1.5">Avgör hur långt bort du kan avgöra vad du ser. 25 mm för skog, 35 mm allround, 50 mm för öppna fält.</span></div>
        <div style="background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:6px"><strong>Sensor</strong><span style="font-size:14px;line-height:1.5">384 eller 640 pixlar avgör hur brett du ser vid samma objektiv, och hur mycket zoom bilden tål.</span></div>
        <div style="background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:6px"><strong>NETD</strong><span style="font-size:14px;line-height:1.5">Känslighet i millikelvin. Under 20 mK märks i dimma, regn och rimfrost. Jämför inom samma fabrikat.</span></div>
        <div style="background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:6px"><strong>Pixelstorlek</strong><span style="font-size:14px;line-height:1.5">12 µm ger mer detalj per millimeter brännvidd än 17 µm. Det är därför nya 35 mm slår gamla 50 mm.</span></div>
      </div>
    </section>

    <section style="background:var(--gunmetal-900);color:var(--text-on-dark)">
      <div style="max-width:1180px;margin:0 auto;padding:14px 24px;display:flex;gap:24px;flex-wrap:wrap;justify-content:center;font-size:13px;font-family:var(--font-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--mist-400)">
        <span>Teknik förklarad från grunden</span><span>Siffror med formler, inte tyckande</span><span>Regler med källa</span><span>Produkter via Nordic Aim</span>
      </div>
    </section>

    <section style="max-width:1180px;margin:0 auto;padding:64px 24px;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start" class="two-col">
      <div style="display:flex;flex-direction:column;gap:16px;font-size:17px;line-height:1.65">
        {eyebrow("Så fungerar tekniken")}
        <h2 style="font-size:30px;font-weight:800">En värmekamera ser temperatur, inte ljus</h2>
        <p>Allt som är varmare än absoluta nollpunkten strålar. Vid kroppstemperatur ligger strålningens topp runt 9,4 µm, mitt i det långvågiga infraröda band (8–14 µm) som värmekameran är byggd för. Ett vildsvin på 38 °C mot en höståker på 8 °C ger en kontrast som elektroniken utan problem gör om till en tydlig bild, i totalt mörker.</p>
        <p>Sensorn heter mikrobolometer. Varje element är ett tunt membran som hänger fritt i vakuum och värms upp en aning av strålningen som träffar det. Uppvärmningen ändrar membranets resistans, resistansen läses av, och skillnaden mellan elementen blir bilden. Inget ljus behövs. Men glas, vatten och tät vegetation stoppar strålningen lika effektivt som en vägg.</p>
        <a href="sa-fungerar-en-varmekamera.html" style="font-weight:700">Hela genomgången i stora guiden →</a>
        {muted(f"Fördjupning hos Nordic Aim: {nalink('/blogs/nyheter/tekniken-bakom-varmekameror-forklarat-enkelt', 'tekniken bakom termiska enheter')} och {nalink('/blogs/nyheter/netd-mk-i-termisk-optik-vad-det-betyder-och-hur-du-valjer-ratt-varmesikte', 'NETD förklarat')}.")}
      </div>
      <div>
        {deflist([
            ("Mikrobolometer", "Sensortypen i alla handhållna värmekameror för jakt. Okyld, vanadinoxid eller amorft kisel, 12 eller 17 µm pixlar."),
            ("NETD", "Noise Equivalent Temperature Difference. Den minsta temperaturskillnad sensorn skiljer från brus, i millikelvin."),
            ("Brännvidd", "9, 19, 25, 35 eller 50 mm. Längre brännvidd ger mer detalj på håll och smalare synfält."),
            ("Synfält", "Bildbredd i meter på 100 m. Styrs av brännvidd och sensorns fysiska storlek."),
            ("NUC", "Kalibreringen som ger klicket. Slutaren täcker sensorn så att alla element kan nollställas mot samma temperatur."),
            ("Palett", "White hot, black hot, red hot, ironbow. Samma data, olika sätt att visa dem."),
        ])}
      </div>
    </section>

    <section style="background:#fff;border-top:1px solid var(--mist-200);border-bottom:1px solid var(--mist-200)">
      <div style="max-width:1180px;margin:0 auto;padding:64px 24px;display:flex;flex-direction:column;gap:28px">
        <div style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:end">
          <div style="display:flex;flex-direction:column;gap:8px;max-width:720px">
            {eyebrow("Det som strular i fält")}
            <h2 style="font-size:30px;font-weight:800">Problem från användare, med förklaring och lösning</h2>
            <p style="font-size:17px;color:var(--text-muted)">Vi utgår från situationer som jägare och eftersöksfolk beskriver. Varje problem får en fysikalisk förklaring, ett krav på lösningen och ett konkret råd.</p>
          </div>
          <a href="problem.html" style="font-weight:700;white-space:nowrap">Alla problem och lösningar →</a>
        </div>
        <div class="three-col">
          <div style="border:1px solid var(--mist-200);border-radius:12px;padding:20px;display:flex;flex-direction:column;gap:6px"><span style="font-family:var(--font-mono);font-size:12px;color:var(--reticle-700);font-weight:700">P01</span><h3 style="font-size:18px">Bilden blir platt när det regnar</h3><p style="font-size:15px;color:var(--text-muted)">Vatten i luften dämpar strålningen och blöta ytor får samma temperatur. Låg NETD och black hot hjälper, men räckvidden sjunker alltid.</p></div>
          <div style="border:1px solid var(--mist-200);border-radius:12px;padding:20px;display:flex;flex-direction:column;gap:6px"><span style="font-family:var(--font-mono);font-size:12px;color:var(--reticle-700);font-weight:700">P05</span><h3 style="font-size:18px">Den ser inte genom tornfönstret</h3><p style="font-size:15px;color:var(--text-muted)">Glas är ogenomskinligt för långvågigt infrarött. Du ser rutans egen temperatur och en svag spegelbild av dig själv.</p></div>
          <div style="border:1px solid var(--mist-200);border-radius:12px;padding:20px;display:flex;flex-direction:column;gap:6px"><span style="font-family:var(--font-mono);font-size:12px;color:var(--reticle-700);font-weight:700">P08</span><h3 style="font-size:18px">Det klickar och bilden fryser</h3><p style="font-size:15px;color:var(--text-muted)">Slutaren stänger för kalibrering (NUC). Sätt den på manuell eller välj en modell med slutarfri korrigering.</p></div>
        </div>
      </div>
    </section>

    <section style="max-width:1180px;margin:0 auto;padding:64px 24px;display:flex;flex-direction:column;gap:28px">
      <div style="display:flex;flex-direction:column;gap:8px;max-width:760px">
        {eyebrow("Modeller vi hänvisar till")}
        <h2 style="font-size:30px;font-weight:800">Värmekameror sorterade efter hur du använder dem</h2>
        <p style="font-size:17px;color:var(--text-muted)">Aktuellt pris, fullständiga specifikationer och lagerstatus ser du hos Nordic Aim. Här beskriver vi vad varje modell är byggd för. Fler modeller och resonemanget bakom finns i <a href="kopguide.html">köpguiden</a>.</p>
      </div>
      {card_grid([
          product_card("HIKMICRO", "Fickformat", "Lynx LE10 3.0",
                       "Skogskanten, gården, hunden i mörkret. 256×192 med 9,7 mm objektiv ger 18° synfält utan fokusering. Slutarfri, så inga klick.",
                       "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/800q-01_135695.png?v=1769171478&width=600", "HIKMICRO Lynx LE10 3.0 värmekamera",
                       ["256×192", "9,7 mm", "<20 mK"], na("/products/hikmicro-lynx-le10-3-0-termisk-monokikare")),
          product_card("PixFra", "Allround", "Mile M2 384×288 25 mm",
                       "Mellanklassens arbetshäst: 384-sensor, 25 mm f/1.0, 320 g och IP67. Räcker till åtel, skog och eftersök utan att kosta som en 640.",
                       "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/PIX-PFI-M425___Pixfra-Mile-2-M425-Thermal-Imaging-Monocular.png?v=1766943659&width=600", "PixFra Mile M2 384×288 25 mm värmekikare",
                       ["384×288", "25 mm", "≤25 mK"], na("/products/pixfra-mile-m2-384x288-25-mm-varmekamera")),
          product_card("Pulsar", "Öppna fält", "Telos XP50 LRF",
                       "640×480 med 17 µm, F50/1.0 och laseravståndsmätare till 1 000 m. Modulär design, bytbart batteri, −25 °C.",
                       "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791&width=600", "Pulsar Telos XP50 LRF värmekamera",
                       ["640×480", "50 mm", "LRF"], na("/products/pulsar-telos-xp50-lrf-640x480-varmekamera-med-laseravstandsmatare")),
          product_card("Pulsar", "Längst räckvidd", "Telos XL50 LRF",
                       "1024×768 på 12 µm bakom 50 mm optik. Ser både bredare och längre än XP50, och visar varför pixelstorleken spelar roll.",
                       "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/947332-0_a2f71263-24ec-4286-a74a-4630c91fdf9f.jpg?v=1766941792&width=600", "Pulsar Telos XL50 LRF värmekamera",
                       ["1024×768", "12 µm", "LRF"], na("/products/pulsar-telos-xl50-lrf-1074x768-varmekamera-med-laseravstandsmatare")),
      ])}
      <div style="display:flex;gap:24px;flex-wrap:wrap;font-weight:600">
        {nalink('/collections/varmekikare', 'Alla värmekameror hos Nordic Aim →', True)}
        {nalink('/blogs/nyheter/valja-varmekikare-kopguide-prisklasser', 'Nordic Aim: välja värmekikare efter prisklass →')}
        {nalink('/blogs/nyheter/hikmicro-nocpix-eller-pulsar', 'HIKMICRO, Nocpix eller Pulsar? →')}
      </div>
      {muted(f"Länkarna går till nordicaim.se. {SITE_NAME} drivs av {NA_NAME}, läs mer under <a href='om.html'>Om oss</a>.")}
    </section>

    <section style="background:#fff;border-top:1px solid var(--mist-200)">
      <div style="max-width:1180px;margin:0 auto;padding:64px 24px;display:flex;flex-direction:column;gap:24px">
        <div style="display:flex;flex-direction:column;gap:8px">
          {eyebrow("Fördjupning")}
          <h2 style="font-size:30px;font-weight:800">Guider</h2>
        </div>
        {guide_tiles([
            ("sa-fungerar-en-varmekamera.html", "Så fungerar en värmekamera", "Strålning, lins, mikrobolometer, kalibrering, bildbehandling och display. Hela kedjan."),
            ("sensor-och-upplosning.html", "Sensor, upplösning och NETD", "256, 384, 640 och 1024 pixlar, 12 mot 17 µm, bildfrekvens och vad mK-talet mäter."),
            ("optik-och-rackvidd.html", "Optik, synfält och räckvidd", "Brännvidd, f-tal, synfält i meter och hur man räknar om räckvidd till något användbart."),
            ("varmekamera-vs-morkerkikare.html", "Värmekamera eller mörkerkikare", "Termiskt mot bildförstärkare och digital IR. När vilket ser mest, och vad multispektral betyder."),
            ("varmekamera-for-jakt.html", "Värmekamera för jakt", "Spaning, åtel, eftersök och inventering. Vad som krävs av kameran i varje situation."),
            ("kopguide.html", "Köpguide", "Prisklasser, checklista och modeller sorterade efter användning."),
            ("anvandningsomraden.html", "Användningsområden", "Jakt, eftersök, räddning, byggnadstermografi, industri och drönare. Olika krav, olika kameror."),
            ("regler.html", "Regler i Sverige", "Vad jaktförordningen säger om värmekamera, med källor."),
            ("ordlista.html", "Ordlista", "Över 50 begrepp från AGC till VOx, förklarade utan reklamspråk."),
        ])}
      </div>
    </section>
  </div>'''
    return {
        "slug": "index.html",
        "title": "Värmekamera: så fungerar den och så väljer du rätt | Värmekamera",
        "raw_title": True,
        "short": "Hem",
        "description": "Så fungerar en värmekamera, förklarat från strålning till bild. Sensor, NETD, optik, räckvidd, regler i Sverige och köpguide för jakt. En sajt från Nordic Aim AB.",
        "body": body,
        "article": False,
    }


# ---------------------------------------------------------------------------
# STORA GUIDEN
# ---------------------------------------------------------------------------
def guide() -> dict:
    chips = [("#stralning", "Strålningen"), ("#optik", "Optiken"), ("#sensor", "Sensorn"), ("#utlasning", "Utläsning"),
             ("#kalibrering", "Kalibrering"), ("#bildbehandling", "Bildbehandling"), ("#display", "Display"),
             ("#begransningar", "Begränsningar"), ("#kyld", "Kyld mot okyld")]
    body = page_hero("Stora guiden", "Så fungerar en värmekamera, steg för steg",
                     "Från värmestrålningen som lämnar djuret till bilden i okularet. Läs i ordning eller hoppa till avsnittet du behöver. Varje steg förklarar också varför en siffra i databladet ser ut som den gör.",
                     chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "En värmekamera fungerar så här: alla föremål avger infraröd strålning vars styrka beror på temperaturen. En lins av germanium fokuserar strålningen i bandet 8–14 µm på en mikrobolometer. Varje element i mikrobolometern värms upp olika mycket och ändrar sin elektriska resistans. En utläsningskrets mäter resistansen i varje element 50 gånger per sekund, en processor korrigerar skillnader mellan elementen (NUC), fördelar kontrasten (AGC) och färglägger bilden (palett), som sedan visas på en liten OLED-display bakom ett okular. Kameran ser alltså temperaturskillnader, inte ljus."
    ) + "</div>"
    body += article_open()

    body += sec("stralning", "1. Strålningen: allt som har temperatur lyser i infrarött", f'''
        <p>Ett föremåls atomer rör sig, och rörelsen sänder ut elektromagnetisk strålning. Hur mycket, och vid vilka våglängder, bestäms av temperaturen. Det är samma fysik som gör att en glödande spik lyser rött: vid 700 °C hamnar en liten del av strålningen i det synliga. Vid de temperaturer som finns i skogen, från −30 till +40 °C, ligger praktiskt taget all strålning i det infraröda, osynlig för ögat.</p>
        <p>Två samband styr allt en värmekamera gör:</p>
        {ul([
            "<strong>Wiens förskjutningslag</strong> säger var strålningen är som starkast: våglängden för toppen är 2898 µm·K delat med temperaturen i kelvin. Ett vildsvin på 38 °C (311 K) strålar som mest vid ungefär 9,3 µm. En frostig åker på −2 °C vid 10,7 µm. Båda ligger i bandet 8–14 µm, det långvågiga infraröda (LWIR).",
            "<strong>Stefan–Boltzmanns lag</strong> säger hur mycket: den totala utstrålningen växer med temperaturen upphöjt till fyra. Kring 0–40 °C betyder det att utstrålningen ökar med drygt en procent per grad. Det är de procenten sensorn mäter. En skillnad på 30 grader mellan djur och mark är enkel. En skillnad på 0,5 grad mellan blöt päls och blöt mark är svår, och där avgörs allt av sensorns känslighet (NETD).",
        ])}
        <figure>{D.spectrum()}<figcaption>Mörkerkikare arbetar strax över synligt ljus (NIR) och behöver ljus eller en IR-lampa. Värmekameran arbetar vid tio gånger längre våglängder, där strålningen kommer från objektet självt.</figcaption></figure>
        <p><strong>Emissivitet</strong> är den tredje parametern. Den anger hur effektivt en yta strålar jämfört med en ideal "svart kropp" (emissivitet 1,0). Päls, hud, trä, jord, löv och vatten ligger kring 0,90–0,98 och beter sig som man väntar. Blank metall ligger kring 0,05–0,2: en plåtstolpe strålar nästan ingenting av sin egen värme utan speglar omgivningen, och ser därför ofta "kall" ut även om den är solvarm. Glas har hög emissivitet och är samtidigt ogenomskinligt i LWIR, så en bilruta visar sin egen yttemperatur, inte vad som finns bakom.</p>
        {callout("Varför bilden ser olika ut i juli och oktober",
                 "Kameran visar alltid skillnaden mellan varmast och kallast i bilden, inte absoluta temperaturer. En sommarnatt när marken håller 22 °C och djuret 38 °C är skillnaden 16 grader och fördelas över hela gråskalan. En oktobernatt med mark på 4 °C är skillnaden 34 grader. Samma kamera, dubbla kontrasten. Lägg till att fuktig mark håller nästan lufttemperatur och att regn i luften stjäl strålning på vägen, så förstår du varför november ofta ger sämre bild än mars trots att det är kallare.")}
    ''')

    body += sec("optik", "2. Optiken: en lins som inte är av glas", f'''
        <p>Vanligt glas släpper igenom synligt ljus men absorberar nästan allt vid 8–14 µm. Linsen i en värmekamera görs därför av <strong>germanium</strong>, ett halvmetalliskt grundämne som är ogenomskinligt för ögat men släpper igenom långvågigt infrarött. Germanium är dyrt och mjukt, så frontlinsen får en hård diamantliknande kolbeläggning (DLC) och antireflexskikt. Billigare kameror använder ibland kalkogenidglas, som är lättare att gjuta i serie men har sämre genomsläpp.</p>
        <p>Objektivet beskrivs med två tal, precis som på en vanlig kamera:</p>
        {ul([
            "<strong>Brännvidd</strong> i millimeter (9,7, 19, 25, 35, 50, 60 mm). Längre brännvidd ger större bild av objektet på sensorn, alltså mer detalj på håll, men ett smalare synfält. Det är den siffra som avgör på vilket avstånd du kan avgöra vad du tittar på.",
            "<strong>F-tal</strong>, brännvidd delat med linsens diameter. f/1.0 är standard i jaktkameror, f/0.9 förekommer. Ett lägre f-tal släpper in mer strålning per pixel, vilket ger lägre brus. En sensors NETD anges nästan alltid vid f/1.0; samma sensor bakom f/1.2 presterar sämre än databladet.",
        ])}
        <p>De flesta objektiv från 19 mm och uppåt har <strong>manuellt fokus</strong>, eftersom skärpedjupet vid f/1.0 är litet. Ett föremål på 30 m och ett på 300 m kan inte vara skarpa samtidigt. Kameror med mycket korta brännvidder (9–10 mm) säljs som fokusfria: allt från några meter till oändligt är tillräckligt skarpt. Det är praktiskt i skog men begränsar detaljen på håll.</p>
        <p>Hur synfältet beräknas, och vad brännvidden betyder i meter, går vi igenom på sidan <a href="optik-och-rackvidd.html">Optik, synfält och räckvidd</a>.</p>
    ''')

    body += sec("sensor", "3. Sensorn: en mikrobolometer mäter uppvärmning, inte ljus", f'''
        <p>Hjärtat i kameran är en <strong>mikrobolometer</strong>, en matris av små element (256×192, 384×288, 640×512, 1024×768 eller 1280×1024 stycken) tillverkad på en kiselbricka. Varje element är ett membran, ungefär 12 eller 17 µm i sida och en bråkdels mikrometer tjockt, som hänger på två smala ben över ett vakuumgap. Membranet är belagt med ett material vars resistans ändras kraftigt med temperaturen, oftast <strong>vanadinoxid (VOx)</strong> eller <strong>amorft kisel (a-Si)</strong>.</p>
        <figure>{D.bolometer()}<figcaption>Benen är medvetet dåliga värmeledare och elementet sitter i vakuum, så den värme som strålningen tillför stannar kvar i membranet länge nog att mätas. Reflektorn under membranet gör att strålning som passerat rakt igenom får en chans till.</figcaption></figure>
        <p>När infraröd strålning träffar membranet absorberas den och membranet blir några tusendels grad varmare. Resistansen ändras, och den ändringen är signalen. Det är därför sensorn kallas <em>okyld</em>: den behöver inte kylas till kryogena temperaturer som fotondetektorer, utan arbetar vid rumstemperatur och mäter rena temperaturförändringar i sig själv.</p>
        <p>Tre egenskaper hos elementen avgör vad kameran kan:</p>
        {ul([
            "<strong>Termisk tidskonstant.</strong> Membranet måste hinna värmas och svalna mellan två bildrutor. Typiska värden på 5–15 ms gör 50 Hz möjligt. Pressas tidskonstanten för hårt blir elementet mindre känsligt.",
            "<strong>Känslighet (NETD).</strong> Hur liten temperaturskillnad i scenen som ger en resistansändring större än bruset. Anges i millikelvin. Moderna VOx-sensorer ligger på 15–25 mK vid f/1.0.",
            "<strong>Pixelstorlek (pitch).</strong> 17 µm var länge standard, 12 µm dominerar nu och 10 µm finns. Mindre element ger mer detalj per millimeter brännvidd, men samlar också mindre strålning var för sig, vilket ställer högre krav på optik och bildbehandling.",
        ])}
        <p>Mer om upplösning, pixelstorlek och vad NETD faktiskt mäter finns på sidan <a href="sensor-och-upplosning.html">Sensor, upplösning och NETD</a>.</p>
    ''')

    body += sec("utlasning", "4. Utläsningen: från resistans till siffror", f'''
        <p>Under membranen, i kiselbrickan, sitter en <strong>utläsningskrets (ROIC, Read-Out Integrated Circuit)</strong>. Den skickar en liten mätström genom varje element i tur och ordning, förstärker spänningen, och omvandlar den till ett tal, typiskt 14 eller 16 bitar per pixel. En 640×512-sensor ger drygt 327 000 sådana mätvärden per bildruta, 50 gånger i sekunden.</p>
        <p>Mätströmmen värmer också elementet (självuppvärmning), och elementen är aldrig exakt lika stora, tjocka eller lika väl isolerade. Därför ger två element som tittar på samma temperatur olika råvärden. Det är det nästa steg rättar till.</p>
        {callout("Varför 50 Hz och inte mer",
                 "Bildfrekvensen begränsas av membranets tidskonstant och av hur fort kretsen hinner läsa alla element med tillräckligt låg brusnivå. 50 Hz (ibland 60) är standard i jaktkameror och ger följsam bild på rörliga djur. Enklare kameror för byggnadstermografi, och de flesta mobiltillsatser, är begränsade till 9 Hz, vilket räcker för stillbilder av en vägg men känns hackigt när ett djur rör sig.", "grey")}
    ''')

    body += sec("kalibrering", "5. Kalibreringen: klicket som gör alla pixlar lika", f'''
        <p>Råbilden från en mikrobolometer är ful: ett mönster av ljusare och mörkare pixlar och stråk, ovanpå den riktiga scenen. Orsaken är spridningen mellan elementen, och den driver dessutom när kamerahuset byter temperatur. Lösningen heter <strong>NUC, Non-Uniformity Correction</strong>. Kameran fäller in en liten slutare (en plåtbit med jämn temperatur) framför sensorn, läser av vad varje element visar när alla ser samma sak, och sparar skillnaden som en korrektionstabell. Tabellen dras sedan ifrån varje bildruta tills nästa kalibrering.</p>
        <p>Det är slutaren du hör som ett klick, och det är därför bilden fryser en bråkdels sekund. Fabriksinställningen är ofta automatisk NUC efter tid eller temperaturdrift, men nästan alla kameror kan ställas på manuell eller halvautomatisk så att du själv utlöser den i ett lugnt ögonblick. Vissa tillverkare, till exempel HIKMICRO med HSIS, räknar fram korrektionen ur bildinnehållet och klarar sig utan slutare. Fördelen är tyst, oavbruten bild; priset är en mer avancerad algoritm som kan behöva lite bildrörelse för att konvergera.</p>
        <p>Utöver NUC finns en fabrikskalibrering som kompenserar för sensorns och optikens temperatur (så att kameran visar rätt när den tas från en varm bil ut i −15 °C), och en tabell över döda pixlar som ersätts med medelvärdet av grannarna.</p>
    ''')

    body += sec("bildbehandling", "6. Bildbehandlingen: 16 bitar data blir 8 bitar bild", f'''
        <p>Sensorn levererar tal med stort omfång (tusentals nivåer), men displayen visar 256 gråtoner, och ditt öga skiljer ännu färre. Bildprocessorn måste alltså välja vilka temperaturskillnader som ska få kontrast. Det görs i flera steg, och det är här fabrikaten skiljer sig mest även med samma sensor:</p>
        {ol([
            "<strong>AGC, automatisk förstärkningsreglering.</strong> Bestämmer vilket temperaturintervall som ska spännas ut över gråskalan. Enklaste varianten mappar bildens kallaste punkt till svart och varmaste till vitt. Bättre varianter använder histogramutjämning: de ger mest kontrast där flest pixlar ligger, så att en sval skog får struktur utan att ett varmt djur bränns ut.",
            "<strong>DDE, digital detaljförstärkning.</strong> Ett lokalt kontrastfilter som lyfter kanter och små temperaturskillnader utan att förstärka bruset i jämna ytor. För mycket DDE ger en tecknad bild med glorior runt djuret; för lite ger en mjuk, platt bild.",
            "<strong>Brusreducering</strong> i tid (medelvärde över flera bildrutor) och rum (filter som jämnar ut pixelbrus). Tidsfiltret ger lugnare bild i stillhet men kan ge släpande spår på snabba djur.",
            "<strong>Palett.</strong> Gråskalan översätts till färger. White hot (varmt = vitt) är standard, black hot ger ofta bäst konturer i fukt, red hot/sepia markerar bara de varmaste delarna och ironbow visar hela intervallet i färg. Paletten tillför ingen information; den väljer vad ögat lätt ser.",
            "<strong>Digital zoom och uppskalning.</strong> Bilden beskärs och skalas upp till displayens upplösning. Vid 2× på en 384-sensor återstår 192×144 riktiga pixlar. Interpolering och så kallade superupplösningsalgoritmer gör bilden mjukare, inte mer informativ.",
        ])}
        <p>När du jämför två kameror i butik är det ofta det här steget du bedömer, inte sensorn. Två kameror med identisk mikrobolometer kan se mycket olika ut beroende på hur AGC och DDE är avvägda.</p>
    ''')

    body += sec("display", "7. Displayen och okularet: där bilden faktiskt blir till", f'''
        <p>Bilden visas på en mikrodisplay, oftast <strong>AMOLED/OLED</strong> med 1024×768 eller 1920×1080 pixlar och några millimeters diagonal, som du tittar på genom ett förstorande okular. OLED ger riktigt svart och hög kontrast, vilket passar termiska bilder, och drar lite ström. LCOS förekommer i enklare modeller.</p>
        <p>Okularet har en <strong>dioptrijustering</strong> så att displayen blir skarp för just ditt öga. Det är ett separat fokus från objektivets, och den vanligaste orsaken till "suddig kamera" är att bara det ena är rätt inställt: ställ dioptrin tills menytexten är knivskarp, ställ sedan objektivet på avståndet till det du tittar på.</p>
        <p>Grundförstoringen (till exempel 2,5×) är ett resultat av brännvidd, sensorstorlek och okularets förstoring. Den säger hur stort ett föremål ser ut jämfört med blotta ögat, men inte hur mycket detalj som finns, det avgör pixlarna på målet.</p>
        <figure>{D.pipeline()}<figcaption>Hela kedjan. Felsök i samma ordning: lins ren och i fokus, sensor kalibrerad, kontrast/palett rimligt inställd, dioptri rätt.</figcaption></figure>
    ''')

    body += sec("begransningar", "8. Vad en värmekamera inte kan", f'''
        {ul([
            "<strong>Se genom glas.</strong> Fönster, bilrutor och glasögon är ogenomskinliga i LWIR. Tornfönstret måste vara öppet.",
            "<strong>Se genom vatten, dimma och tät vegetation.</strong> Vatten absorberar långvågigt infrarött effektivt. Regn och dimma sänker räckvidden kraftigt, en blöt granridå är en vägg. Gles vegetation och högt gräs släpper igenom en del, och där ser kameran ofta mer än ögat.",
            "<strong>Mäta avstånd.</strong> Bilden är tvådimensionell och ger inga djupledtrådar. Det som står bakom djuret syns bara om det har en annan temperatur. Därför har många modeller laseravståndsmätare.",
            "<strong>Identifiera.</strong> Att upptäcka något varmt går på många hundra meter. Att se att det är ett djur, vilket djur, och om det är en sugga med kultingar kräver många fler pixlar på målet. Mer om det under <a href='optik-och-rackvidd.html#dri'>räckvidd</a>.",
            "<strong>Fungera genom en varm lins.</strong> Immar eller fryser frontlinsen ser kameran sin egen is. Handvärme, regn och snö på linsen ger samma effekt. Håll linsskyddet på tills du behöver bilden.",
        ])}
    ''')

    body += sec("kyld", "9. Kyld eller okyld, och varför jaktkameror alltid är okylda", f'''
        <p>Det finns två familjer av värmekameror. <strong>Fotondetektorer</strong> (InSb, MCT, T2SL) räknar infraröda fotoner direkt och ger extremt låg NETD och hög bildfrekvens, men bara om de kyls till runt −200 °C med en liten Stirlingkylare. De används i militära system, flyg och forskning, kostar från några hundra tusen kronor och drar mycket ström.</p>
        <p><strong>Okylda mikrobolometrar</strong> mäter uppvärmning i stället för fotoner och fungerar vid rumstemperatur. De är billigare, tystare, tåligare och drar lite ström, till priset av högre NETD och begränsad bildfrekvens. Sedan 2010-talet har de blivit så bra att de täcker praktiskt taget allt civilt bruk: jakt, byggnadstermografi, industri, räddningstjänst, bilar och drönare.</p>
        {table(["", "Okyld (mikrobolometer)", "Kyld (fotondetektor)"], [
            ["Våglängd", "8–14 µm (LWIR)", "3–5 µm (MWIR), ibland LWIR"],
            ["NETD", "15–40 mK", "&lt;20 mK, ofta under 10"],
            ["Uppstart", "Sekunder", "Flera minuter (nedkylning)"],
            ["Ström", "1–3 W", "10–20 W"],
            ["Livslängd", "Ingen rörlig del utom slutaren", "Kylaren slits, byts efter tusentals timmar"],
            ["Pris", "Från några tusen kronor", "Från några hundra tusen"],
            ["Användning", "Jakt, bygg, industri, räddning, drönare", "Militär, flyg, gasdetektion, forskning"],
        ])}
        <p>Fortsättning: <a href="sensor-och-upplosning.html">Sensor, upplösning och NETD</a> → <a href="optik-och-rackvidd.html">Optik, synfält och räckvidd</a> → <a href="varmekamera-for-jakt.html">Värmekamera för jakt</a>.</p>
        {muted(f"{NA_NAME} har en egen genomgång med fokus på databladet: {nalink('/blogs/nyheter/tekniken-bakom-varmekameror-forklarat-enkelt', 'Tekniken bakom termiska enheter, förklarat enkelt')}. Om termiska <em>sikten</em>, alltså värmekameror monterade på vapnet, skriver vår systersajt {ext(SISTER + '/guide.html', 'Värmesikte.se')}.")}
    ''')
    body += article_close()
    return {
        "slug": "sa-fungerar-en-varmekamera.html",
        "title": "Så fungerar en värmekamera: från strålning till bild, steg för steg",
        "short": "Så fungerar en värmekamera",
        "description": "Exakt hur en värmekamera fungerar: infraröd strålning, germaniumlins, mikrobolometer, utläsning, NUC-kalibrering, bildbehandling och display. Med diagram och formler.",
        "body": body,
        "image": "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791&width=1200",
    }


# ---------------------------------------------------------------------------
# SENSOR
# ---------------------------------------------------------------------------
def sensor() -> dict:
    sensors = [(256, 192), (384, 288), (640, 512), (1024, 768), (1280, 1024)]
    rows = []
    for w, h in sensors:
        rows.append([f"{w}×{h}", f"{w * h / 1000:.0f} 000".replace(".", ","),
                     f"{sv(fov_deg(w, 12, 35))}°", f"{sv(width_at(w, 12, 35))} m",
                     f"{sv(fov_deg(w, 12, 50))}°", f"{sv(width_at(w, 12, 50))} m"])
    zoom_rows = []
    for w, h in sensors[:4]:
        zoom_rows.append([f"{w}×{h}", f"{w // 2}×{h // 2}", f"{w // 4}×{h // 4}", f"{w // 8}×{h // 8}"])
    chips = [("#upplosning", "Upplösning"), ("#pitch", "Pixelstorlek"), ("#netd", "NETD"), ("#hz", "Bildfrekvens"), ("#material", "VOx mot a-Si"), ("#datablad", "Läsa databladet")]
    body = page_hero("Sensor", "Sensor, upplösning och NETD: vad siffrorna betyder",
                     "384 eller 640? 12 eller 17 µm? 18 eller 25 mK? Här är vad varje tal gör med bilden, med uträknade exempel i stället för tyckande.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "Sensorns upplösning (384×288, 640×512) avgör hur brett du ser vid ett givet objektiv och hur mycket digital zoom bilden tål. Pixelstorleken (12 eller 17 µm) tillsammans med brännvidden avgör hur mycket detalj du får per meter avstånd. NETD (i millikelvin, lägre är bättre) avgör hur små temperaturskillnader som syns, vilket märks mest i fukt och dåligt väder. Bildfrekvens 50 Hz är standard för jakt."
    ) + "</div>"
    body += article_open()
    body += sec("upplosning", "Upplösning: fler pixlar ger bredare bild, inte längre", f'''
        <p>En mikrobolometer med 640×512 element är fysiskt större än en med 384×288, om pixlarna är lika stora. Bakom samma objektiv täcker den större sensorn en större del av bilden som linsen ritar upp, alltså ett bredare synfält. Detaljen per pixel, det som avgör hur långt bort du kan avgöra vad du ser, är däremot identisk, eftersom den bara beror på pixelstorlek och brännvidd.</p>
        <figure>{D.fov_compare()}<figcaption>Samma objektiv, fyra sensorer. Det är synfältet som växer med upplösningen.</figcaption></figure>
        {table(["Sensor", "Pixlar", "Synfält 35 mm", "Bredd på 100 m", "Synfält 50 mm", "Bredd på 100 m"], rows,
               caption="Beräknat med 12 µm pixlar. Formel: synfält = 2·arctan(pixlar × pixelstorlek / (2 × brännvidd)).")}
        <p>Det bredare synfältet är värt pengar när du söker av marker eller går eftersök: färre drag med kameran, och lättare att hålla reda på var djuret tog vägen. Den andra vinsten är <strong>digital zoom</strong>. Zoom beskär bilden, så antalet riktiga pixlar som är kvar sjunker snabbt:</p>
        {table(["Sensor", "Vid 2×", "Vid 4×", "Vid 8×"], zoom_rows, caption="Kvarvarande riktiga pixlar vid digital zoom. Allt därutöver är uppskalning.")}
        <p>Tumregel: en 384-sensor är användbar till ungefär 2× digital zoom, en 640 till ungefär 4×. En 640 vid 4× visar lika många riktiga pixlar som en 384 vid 2,4×, med samma objektiv. Fler pixlar köper alltså zoomutrymme, inte räckvidd.</p>
        {muted(f"{NA_NAME} räknar på samma sätt, med fältexempel, i {nalink('/blogs/nyheter/varmesikte_384vs640', '384 mot 640: skillnaden i praktiken')}.")}
    ''')
    body += sec("pitch", "Pixelstorlek: 12 µm mot 17 µm", f'''
        <p>Pixelstorleken (pixel pitch) är avståndet mellan två elements mittpunkter på sensorn, i mikrometer. Den bestämmer tillsammans med brännvidden hur stor bit av verkligheten varje pixel täcker:</p>
        <p style="font-family:var(--font-mono);font-size:15px;background:#fff;border:1px solid var(--mist-200);border-radius:10px;padding:14px 18px">en pixel täcker = pixelstorlek ÷ brännvidd × avstånd</p>
        {table(["Objektiv", "Pixelstorlek", "En pixel täcker på 100 m", "På 300 m"], [
            ["25 mm", "12 µm", f"{sv(footprint_cm(12, 25))} cm", f"{sv(footprint_cm(12, 25, 300))} cm"],
            ["35 mm", "12 µm", f"{sv(footprint_cm(12, 35))} cm", f"{sv(footprint_cm(12, 35, 300))} cm"],
            ["50 mm", "12 µm", f"{sv(footprint_cm(12, 50))} cm", f"{sv(footprint_cm(12, 50, 300))} cm"],
            ["35 mm", "17 µm", f"{sv(footprint_cm(17, 35))} cm", f"{sv(footprint_cm(17, 35, 300))} cm"],
            ["50 mm", "17 µm", f"{sv(footprint_cm(17, 50))} cm", f"{sv(footprint_cm(17, 50, 300))} cm"],
        ])}
        <p>Ett 50 mm-objektiv med 17 µm-pixlar ger alltså samma detalj som ett 35 mm med 12 µm. Den mindre pixeln "köper" 15 mm brännvidd, och det är skälet till att nya kompakta kameror med 35 mm ofta ser lika långt som äldre med 50 mm, med bredare synfält och lägre vikt på köpet.</p>
        <p>Baksidan: ett mindre element fångar mindre strålning. Allt annat lika ger 12 µm något sämre känslighet än 17 µm, vilket tillverkarna kompenserar med bättre membranmaterial, f/0.9-optik och mer bildbehandling. Jämför därför aldrig NETD mellan en 12- och en 17 µm-sensor rakt av.</p>
    ''')
    body += sec("netd", "NETD: känsligheten, i millikelvin", f'''
        <p><strong>NETD, Noise Equivalent Temperature Difference</strong>, är den temperaturskillnad i scenen som ger en signal lika stor som sensorns eget brus. Ligger skillnaden under NETD drunknar den i bruset; ligger den klart över syns den. Enheten är millikelvin (tusendels grad). Mäts normalt mot en svartkropp vid 25–30 °C, genom f/1.0-optik, vid 50 Hz. Ändras någon av de förutsättningarna ändras värdet, och det är därför tal från olika tillverkare sällan går att jämföra.</p>
        {table(["NETD", "Nivå", "När du märker det"], [
            ["Under 20 mK", "Mycket känslig", "Håller ihop bilden i dimma, duggregn, rimfrost och mot blöt mark"],
            ["20–25 mK", "Bra", "Räcker i de flesta svenska jaktkvällar"],
            ["25–40 mK", "Enklare", "Fungerar bra i klar, torr luft; tappar struktur när luftfuktigheten stiger"],
            ["Över 40 mK", "Byggnads- och mobilkameror", "Ser en vägg eller en människa, men inte päls mot våt mark"],
        ])}
        <p>Tre fallgropar:</p>
        {ul([
            "<strong>Sensor-NETD mot system-NETD.</strong> Vissa anger sensorns värde från chiptillverkaren, andra det uppmätta värdet efter optik och bildbehandling (Pulsar skriver 'sNETD'). Samma kamera kan ha 40 mK sensor och 20 mK system. Jämför tal av samma sort.",
            "<strong>'Under' och 'cirka'.</strong> '&lt;25 mK' är ett tak, inte ett uppmätt värde. Två kameror med '&lt;25 mK' kan ligga på 18 respektive 24.",
            "<strong>NETD är inte allt.</strong> En låg siffra hjälper bara om optiken släpper in strålningen och bildbehandlingen inte filtrerar bort den. En 18 mK-sensor bakom ett billigt objektiv kan ge sämre bild än 25 mK bakom bra glas.",
        ])}
        {callout("Praktiskt test", "Titta på en blöt grusväg en fuktig kväll. En kamera med bra NETD visar hjulspår, pölar och stenar som separata nyanser. En sämre visar en jämngrå yta. Det är exakt den skillnaden som avgör om du ser grisen som ligger stilla i den blöta rågen.")}
        {muted(f"Fördjupning: {nalink('/blogs/nyheter/netd-mk-i-termisk-optik-vad-det-betyder-och-hur-du-valjer-ratt-varmesikte', 'NETD och mK i termisk optik: vad det betyder')}.")}
    ''')
    body += sec("hz", "Bildfrekvens: 50 Hz, 25 Hz eller 9 Hz", f'''
        <p>Bildfrekvensen anger hur många gånger per sekund sensorn läses av. 50 Hz är standard i jaktkameror och ger följsam bild när ett djur rör sig eller när du själv panorerar. 25–30 Hz märks som en lätt hackighet. 9 Hz, som gäller för de flesta mobiltillsatser och många byggnadstermografikameror, är begränsningen från exportregler för termisk teknik och räcker för stillbilder av en vägg men inte för att följa vilt.</p>
        <p>Hög bildfrekvens kräver kort termisk tidskonstant i elementen, vilket i sin tur står i konflikt med känsligheten. Det är en av anledningarna till att en bra 50 Hz-sensor kostar mer än en 9 Hz med samma upplösning.</p>
    ''')
    body += sec("material", "Vanadinoxid eller amorft kisel", f'''
        <p>Membranets material avgör hur mycket resistansen ändras per grad (temperaturkoefficienten, TCR) och hur mycket brus materialet själv ger. <strong>Vanadinoxid (VOx)</strong> har hög TCR och lågt 1/f-brus och dominerar i de bättre jaktkamerorna; de flesta tillverkare som anger "VOx" gör det som ett kvalitetsargument. <strong>Amorft kisel (a-Si)</strong> är enklare att tillverka i stora serier och finns i många prisvärda sensorer; skillnaden i färdig bild är i dag mindre än den var för tio år sedan, eftersom bildbehandlingen kompenserar mycket.</p>
        <p>Viktigare än materialet är tillverkarens erfarenhet av att göra jämna matriser med få döda pixlar, och hur väl kamerans NUC hanterar driften. Det syns inte i databladet, men i bilden efter en timme i kyla.</p>
    ''')
    body += sec("datablad", "Så läser du ett datablad på en minut", f'''
        {ol([
            "<strong>Pixelstorlek och brännvidd</strong> → hur mycket detalj på håll. Räkna cm per pixel på 100 m med formeln ovan.",
            "<strong>Upplösning</strong> → hur brett, och hur mycket zoom bilden tål.",
            "<strong>NETD</strong>, och vilken sort → hur mycket struktur som finns kvar i fukt.",
            "<strong>Bildfrekvens</strong> → 50 Hz för jakt, annars hackig bild.",
            "<strong>Display</strong>: typ och upplösning → OLED 1024×768 eller mer för långa pass utan trötthet.",
            "<strong>Batteri</strong>: bytbart eller inbyggt, timmar vid vilken temperatur → kyla halverar ofta siffran.",
            "<strong>Detektionsräckvidd</strong> → ett marknadsföringstal. Läs <a href='optik-och-rackvidd.html#dri'>hur det räknas</a> innan du jämför.",
        ])}
        <p>Nästa sida: <a href="optik-och-rackvidd.html">Optik, synfält och räckvidd</a>.</p>
    ''')
    body += article_close()
    return {
        "slug": "sensor-och-upplosning.html",
        "title": "Värmekamera: sensor, upplösning, pixelstorlek och NETD förklarat",
        "short": "Sensor, upplösning och NETD",
        "description": "Vad 256, 384, 640 och 1024 pixlar betyder i en värmekamera, skillnaden mellan 12 och 17 µm, vad NETD mäter och varför 50 Hz spelar roll. Med uträknade tabeller.",
        "body": body,
    }


# ---------------------------------------------------------------------------
# OPTIK OCH RÄCKVIDD
# ---------------------------------------------------------------------------
def optik() -> dict:
    # DRI enligt Johnsons kriterier för ett vildsvin med kritisk dimension 1,0 m (kroppslängd), 12 µm
    def dri_rows(pitch):
        rows = []
        for f in (10, 19, 25, 35, 50):
            foot_m_per_m = pitch / 1000.0 / f  # m per m avstånd
            # pixlar över målet = 0.75 / (foot * D)  => D = 0.75 / (px * foot)
            det = 1.0 / (2 * foot_m_per_m)
            rec = 1.0 / (8 * foot_m_per_m)
            idn = 1.0 / (13 * foot_m_per_m)
            rows.append([f"{f} mm", f"{det:,.0f} m".replace(",", " "), f"{rec:,.0f} m".replace(",", " "), f"{idn:,.0f} m".replace(",", " ")])
        return rows

    chips = [("#brannvidd", "Brännvidd"), ("#ftal", "F-tal"), ("#synfalt", "Synfält"), ("#forstoring", "Förstoring"), ("#dri", "Räckvidd (DRI)"), ("#lrf", "Avståndsmätare"), ("#val", "Välja objektiv")]
    body = page_hero("Optik och räckvidd", "Objektiv, synfält och räckvidd: räkna om siffrorna till meter",
                     "Brännvidden är den enskilt viktigaste siffran på en värmekamera. Här går vi igenom vad den gör, hur synfältet beräknas och vad 'detektion upp till 1 800 m' faktiskt betyder.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "Brännvidden (t.ex. 25, 35 eller 50 mm) avgör tillsammans med pixelstorleken hur mycket detalj värmekameran ger på ett givet avstånd, och tillsammans med sensorstorleken hur brett synfältet blir. Tillverkarnas räckvidd gäller nästan alltid detektion, alltså att se att något varmt finns, och bygger på ett standardmål under goda förhållanden. Avståndet där du kan avgöra art ligger typiskt på en fjärdedel av detektionsavståndet, och identifiering av individ på ungefär en sjättedel."
    ) + "</div>"
    body += article_open()
    body += sec("brannvidd", "Brännvidd: den viktigaste siffran", f'''
        <p>Brännvidden är avståndet från linsens optiska centrum till sensorn när ett avlägset objekt är i fokus. Längre brännvidd ritar upp objektet större på sensorn. Eftersom sensorns pixlar har fast storlek betyder större bild fler pixlar över djuret, alltså mer detalj. Samtidigt får en mindre del av scenen plats på sensorn: synfältet smalnar.</p>
        {table(["Brännvidd", "Typisk användning", "Synfält 384×288/12 µm", "Synfält 640×512/12 µm"], [
            ["9–10 mm", "Fickkamera, skog, hund, gården. Fokusfri.", f"{sv(width_at(384, 12, 10))} m på 100 m", f"{sv(width_at(640, 12, 10))} m"],
            ["15–19 mm", "Kompakt allround i skog och på korta pass", f"{sv(width_at(384, 12, 19))} m", f"{sv(width_at(640, 12, 19))} m"],
            ["25 mm", "Allround: skog, åtel, eftersök", f"{sv(width_at(384, 12, 25))} m", f"{sv(width_at(640, 12, 25))} m"],
            ["35 mm", "Allround med mer räckvidd; vanligaste valet", f"{sv(width_at(384, 12, 35))} m", f"{sv(width_at(640, 12, 35))} m"],
            ["50 mm", "Öppna fält, långa håll, bedömning av djur", f"{sv(width_at(384, 12, 50))} m", f"{sv(width_at(640, 12, 50))} m"],
            ["60 mm+", "Specialist: stora fält, inventering", f"{sv(width_at(384, 12, 60))} m", f"{sv(width_at(640, 12, 60))} m"],
        ], caption="Bildbredd på 100 m. Beräknat, avrundat. Tillverkarnas egna värden kan avvika någon decimeter.")}
    ''')
    body += sec("ftal", "F-tal: hur mycket strålning som når sensorn", f'''
        <p>F-talet är brännvidden delat med linsens fria diameter. F50/1.0 betyder 50 mm brännvidd och 50 mm öppning. Ett lägre f-tal (f/0.9) samlar mer strålning per pixel och ger lägre brus, vilket i praktiken sänker system-NETD. Ett högre (f/1.2) gör linsen billigare och lättare men sensorn presterar sämre än på databladet, som nästan alltid är mätt vid f/1.0.</p>
        <p>Till skillnad från en dagkikare finns ingen vinst i att "blända ner". Linsen används alltid fullt öppen, och skärpedjupet är därför litet. Det är därför objektiv från cirka 19 mm och uppåt har fokusring, och varför du måste vrida på den när avståndet ändras från 40 till 200 m.</p>
    ''')
    body += sec("synfalt", "Synfält: så räknas det", f'''
        <p>Synfältet beror på två saker: sensorns fysiska bredd (pixlar × pixelstorlek) och brännvidden.</p>
        <p style="font-family:var(--font-mono);font-size:15px;background:#fff;border:1px solid var(--mist-200);border-radius:10px;padding:14px 18px">synfält (grader) = 2 × arctan( pixlar × pixelstorlek ÷ (2 × brännvidd) )<br>bildbredd på 100 m ≈ 200 × tan( synfält ÷ 2 )</p>
        <p>Exempel: 384 × 12 µm = 4,61 mm sensorbredd. Med 35 mm brännvidd ger det 2·arctan(4,61/70) = {sv(fov_deg(384, 12, 35))}°, alltså {sv(width_at(384, 12, 35))} m på 100 m. Samma sensor med 17 µm är 6,53 mm bred och ger {sv(fov_deg(384, 17, 35))}°. Två kameror med "384 och 35 mm" kan alltså ha olika synfält, och två med olika brännvidd kan ha samma. Jämför alltid grader eller meter på 100 m, inte brännvidd.</p>
    ''')
    body += sec("forstoring", "Grundförstoring och digital zoom", f'''
        <p>Grundförstoringen (1,5×, 2,5×, 4×) anger hur mycket större ett föremål ser ut i okularet än med blotta ögat. Den följer av brännvidd, sensorstorlek och okular, och säger inget om detaljnivån. En 2,5× med 640-sensor visar samma detalj per meter som en 4× med 384 bakom samma objektiv; 384-kameran har bara mindre synfält som okularet förstorar mer.</p>
        <p>Låg grundförstoring (1–2×) gör det lätt att gå med kameran uppe och att hitta tillbaka till ett djur som rört sig. Hög (4×+) ger lugnare detaljbedömning på håll men kräver stöd. Digital zoom lägger till 2×, 4×, 8× ovanpå, till priset av färre riktiga pixlar, se <a href="sensor-och-upplosning.html#upplosning">sensorsidan</a>.</p>
    ''')
    body += sec("dri", "Räckvidd: detektion, igenkänning, identifiering", f'''
        <p>"Detektion upp till 1 800 m" är det tal som säljer, och det sämst definierade. Branschen använder <strong>Johnsons kriterier</strong>, en metod från 1950-talet som anger hur många linjepar (par av ljusa och mörka pixelrader) som måste täcka ett måls kritiska dimension för att en observatör ska klara en uppgift med 50 % sannolikhet:</p>
        {table(["Uppgift", "Linjepar över målet", "≈ pixlar", "Vad du kan säga"], [
            ["Detektion", "1,0 (±0,25)", "2", "Något varmt finns där"],
            ["Orientering", "1,4", "3", "Åt vilket håll det är vänt"],
            ["Igenkänning", "4,0 (±0,8)", "8", "Vilken klass: hjortdjur, vildsvin, hund, människa"],
            ["Identifiering", "6,4 (±1,5)", "13", "Vilket djur: sugga, galt, kulting, kronhind mot dovhind"],
        ], caption="Johnsons kriterier. Sannolikheten är 50 % vid angivet värde; för säker bedömning behövs ungefär det dubbla.")}
        <p>Med formeln för pixelfotavtryck får vi avstånden. För ett vuxet vildsvin sett från sidan, kritisk dimension 1,0 m (kroppslängd), och 12 µm-pixlar:</p>
        {table(["Objektiv (12 µm)", "Detektion (2 px)", "Igenkänning (8 px)", "Identifiering (13 px)"], dri_rows(12),
               caption="Teoretiska värden i klar luft, 50 % sannolikhet. Verkliga avstånd blir kortare i fukt, lägre kontrast och för en trött observatör.")}
        <p>Lägg märke till relationen: igenkänning sker på ungefär en fjärdedel av detektionsavståndet och identifiering på en sjättedel. Det stämmer väl med vad tillverkarna själva anger när de är ärliga. {NA_NAME} skriver på varje produktsida ut tre tal, detektion, artbestämning och detaljbedömning, räknade på samma sätt, så att modellerna går att jämföra med varandra.</p>
        {callout("Varför tillverkarnas tal spretar",
                 "Olika tillverkare räknar på olika mål (en människa 1,8×0,5 m, ett 'standardmål' 0,5 m, ibland en bil) och ibland med 1,5 pixel i stället för 2. Samma kamera kan därför ha 1 300 m i ett datablad och 1 800 m i ett annat. Räkna själv med pixelstorlek och brännvidd, så får du ett tal du kan använda på din egen mark.", "grey")}
        {muted(f"Nordic Aim förklarar sin räkning i {nalink('/blogs/nyheter/detektionsavstand-varmesikte', 'Detektionsavstånd: hur långt ser den egentligen?')}.")}
    ''')
    body += sec("lrf", "Laseravståndsmätare (LRF)", f'''
        <p>Eftersom en termisk bild saknar djup är inbyggd laseravståndsmätare en av de funktioner som gör störst praktisk skillnad: du vet om grisen står på 80 eller 140 m, och du kan avgöra om det du ser i kanten av fältet är ett rådjur på 200 m eller en hare på 60. Lasern är osynlig (905 nm klass 1) och mäter normalt till 600–1 000 m med ±1 m. Den fungerar sämre mot små mål, gles vegetation och i kraftigt regn, och den läggs till i vikt och storlek på huset.</p>
        <p>Modeller med och utan LRF finns i de flesta serier. Jagar du på åtel med kända avstånd är den sällan värd pengarna; på vak över öppen mark och vid eftersök är den ofta det första du saknar.</p>
    ''')
    body += sec("val", "Välja objektiv efter mark", f'''
        {table(["Du jagar mest", "Brännvidd", "Sensor", "Kommentar"], [
            ["Tät skog, drev, hund, gården", "9–19 mm", "256–384", "Brett synfält och fokusfritt slår räckvidd. Lätt och billig."],
            ["Skogspass, åtel 40–100 m, eftersök", "25 mm", "384 eller 640", "Allround. 640 om du ofta söker av stora ytor."],
            ["Blandat: skog och mindre fält", "35 mm", "384 eller 640", "Det vanligaste valet. 35/640 är sweet spot för många."],
            ["Öppna fält, vak 150–300 m, bedömning", "50 mm", "640 eller mer", "Lägg till LRF. Kräver stöd vid hög zoom."],
            ["Inventering, stora slätter", "50–60 mm", "640–1280", "Specialist. Tung, dyr, överlägsen på håll."],
        ], mono_first=False)}
        <p>Nästa steg: <a href="varmekamera-for-jakt.html">Värmekamera för jakt</a> och <a href="kopguide.html">Köpguiden</a>. Osäker? {nalink('/pages/kontakta-oss', 'Nordic Aim ger personlig rekommendation')} utifrån hur du jagar.</p>
    ''')
    body += article_close()
    return {
        "slug": "optik-och-rackvidd.html",
        "title": "Värmekamera: brännvidd, synfält och räckvidd (detektion, igenkänning, identifiering)",
        "short": "Optik, synfält och räckvidd",
        "description": "Så påverkar brännvidd och f-tal en värmekamera. Formler för synfält, tabeller för 10–60 mm och Johnsons kriterier för detektion, igenkänning och identifiering i meter.",
        "body": body,
    }


def pages() -> list[dict]:
    return [index(), guide(), sensor(), optik()]
