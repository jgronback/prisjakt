"""Jakt, köpguide, värmekamera mot mörkerkikare, användningsområden."""
from build import (na, nalink, ext, eyebrow, page_hero, article_open, article_close, sec, callout,
                   short_answer, table, deflist, ul, ol, muted, product_card, card_grid, SITE_NAME, NA_NAME, SISTER)

CDN = "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/"


def _p(brand, kind, name, text, img, alt, specs, handle):
    return product_card(brand, kind, name, text, CDN + img + "&width=600", alt, specs, na("/products/" + handle))


# ---------------------------------------------------------------------------
# VÄRMEKAMERA FÖR JAKT
# ---------------------------------------------------------------------------
def jakt() -> dict:
    chips = [("#spaning", "Spaning"), ("#atel", "Åtel och vak"), ("#eftersok", "Eftersök"), ("#inventering", "Inventering"), ("#kikare-sikte", "Kikare eller sikte"), ("#teknik", "Teknik i fält")]
    body = page_hero("Värmekamera för jakt", "Värmekamera på jakt: spaning, åtel, eftersök och inventering",
                     "Här går vi igenom vad en handhållen värmekamera (värmekikare) ska klara i varje jaktsituation, och vilka siffror som bara är marknadsföring.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "För jakt används värmekameran framför allt handhållen, för att hitta och bedöma vilt i mörker innan skottet, för att söka av marker och för att lokalisera skadat vilt vid eftersök. Att spana med värmekamera är inte reglerat i jaktförordningen; monterad på vapnet (värmesikte) får den enligt 14 a § bara användas vid jakt på vildsvin, och termiska sikten bara i öppen terräng eller vid åtel. För skog och korta håll räcker 256–384 pixlar och 10–25 mm; för öppna fält behövs 640 pixlar, 35–50 mm och gärna avståndsmätare."
    ) + "</div>"
    body += article_open()
    body += sec("spaning", "Spaning: hitta djuret i mörker", f'''
        <p>Det klassiska användningsområdet. Du sitter på pass eller går sakta i skogskanten, lyfter kameran med jämna mellanrum och söker av terrängen. Ett däggdjur med 37–39 °C kroppstemperatur lyser mot en bakgrund som på hösten ligger 20–30 grader lägre. Du ser rådjuret i dikesrenen hundra meter innan det hade varit möjligt med ögat, och du ser det utan att lysa, prassla eller röra dig.</p>
        <p>Kraven på kameran vid spaning:</p>
        {ul([
            "<strong>Brett synfält</strong> så att du täcker marken med få drag. 384/25 mm (ca 18 m på 100 m) eller 640/35 mm (ca 22 m) är bra kompromisser.",
            "<strong>Låg grundförstoring</strong> (1–2,5×) så att bilden är lätt att orientera sig i och du hittar tillbaka till djuret.",
            "<strong>Snabb start.</strong> Från avstängd eller standby till bild på under två sekunder. Rådjuret väntar inte på att kameran ska starta.",
            "<strong>Enhandsgrepp med handske.</strong> Du håller vapnet i andra handen.",
            "<strong>Lugn bild.</strong> 50 Hz och bra brusreducering gör att du kan hålla kameran uppe länge utan att tröttna.",
        ])}
        <p>Spaningskameran ger också underlag för att avstå: du ser om det står ett andra djur bakom, eller om "grisen" är ett rådjur.</p>
    ''')
    body += sec("atel", "Åtel och vak: bedöma djuret, inte bara hitta det", f'''
        <p>På åteln är avstånden kända och korta (30–80 m). Kameran används för att se vad som kommer, i vilken ordning, och för att avgöra om det är en kulting, en gylta eller en sugga med kultingar bakom sig. Här räcker nästan vilken 384-kamera som helst för själva upptäckten; det som skiljer är bedömningen. Fler pixlar på djuret (640-sensor eller längre brännvidd) ger säkrare bedömning av storlek och kön, och bra bildbehandling gör att du ser spenar och kroppsform i stället för en vit siluett.</p>
        <p>På vak över öppna fält med 100–300 m är kraven de omvända: nu är det brännvidden (50 mm) och avståndsmätaren som gör jobbet, och synfältet blir mindre viktigt eftersom du vet var fältet är.</p>
        {callout("Kameran och vapnet", f"Många jagar med värmekamera i handen och ett vanligt kikarsikte eller digitalt mörkersikte på vapnet. Andra har termiskt sikte på vapnet och spanar med kameran. Spaningskameran är i båda fallen den som används mest, eftersom den har bredare synfält och inte kräver att vapnet lyfts. Reglerna för siktet på vapnet står på sidan <a href='regler.html'>Regler</a>. Jämförelsen mellan de två vägarna finns hos Nordic Aim: {nalink('/blogs/nyheter/varmekikare-eller-varmesikte-forst', 'Värmekikare eller värmesikte först?')}", "grey")}
    ''')
    body += sec("eftersok", "Eftersök: hitta ett skadat djur, och veta när kameran inte räcker", f'''
        <p>Värmekameran har två roller vid eftersök. Den första är att lokalisera ett djur som ligger eller står stilla inom några hundra meter från skottplatsen, ofta det snabbaste sättet att få ett påskjutet djur avfångat utan långt lidande. Den andra är att följa spår: färskt blod håller kroppstemperatur de första minuterna och syns som ljusa fläckar på kall mark, och ett djur som legat lämnar en varm "bädd" en stund efter att det rest sig.</p>
        <p>Begränsningarna är lika viktiga att känna:</p>
        {ul([
            "<strong>Vegetation.</strong> I tät granskog ser kameran bara det som har fri siktlinje. Ett djur två meter in i en ridå är osynligt.",
            "<strong>Tid.</strong> Blod kallnar på några minuter, bädden på en kvart. Kameran är bäst de första tjugo minuterna och sedan är hunden bäst.",
            "<strong>Falska mål.</strong> Solvarma stenar, stubbar, myrstackar och tamdjur lyser också. Ett 'hittat' djur måste alltid bekräftas.",
            "<strong>Avfångningen.</strong> Hur siktet på vapnet får användas vid avfångning följer reglerna för arten, inte för eftersöket. Spaningen med handhållen kamera är fri.",
        ])}
        <p>För eftersök väger brett synfält, låg vikt och snabb start tyngre än räckvidd. En kompakt 384/19–25 mm eller en 640/25 mm är ett bättre eftersöksverktyg än en 50 mm-kamera med 2 km detektion.</p>
        {muted(f"Metod steg för steg: {nalink('/blogs/nyheter/eftersok-med-varmekikare', 'Eftersök med värmekikare')} hos Nordic Aim.")}
    ''')
    body += sec("inventering", "Inventering och viltvård", f'''
        <p>Allt fler jaktlag och markägare använder värmekamera för att räkna vilt, hitta vildsvinsgrupper innan sådd, lokalisera gäss och tranor på vall eller kontrollera att åteln besöks. Här är kraven de omvända mot eftersök: långa brännvidder (50–60 mm), höga upplösningar (640–1280) och gärna stativfäste för att kunna räkna djur på 500 m. Inspelning till internminne och Wi-Fi-överföring till telefon gör det möjligt att dokumentera och dela.</p>
        <p>Drönare med värmekamera används också för inventering, i första hand av yrkesfolk och med egna regler kring flygning och vilt. Se <a href="anvandningsomraden.html#dronare">Användningsområden</a>.</p>
    ''')
    body += sec("kikare-sikte", "Värmekikare, värmesikte eller clip-on: tre sätt att bära samma teknik", f'''
        {table(["", "Handhållen värmekamera", "Värmesikte (tub)", "Clip-on framför kikarsiktet"], [
            ["Används till", "Spana, bedöma, eftersök", "Skottet, på vapnet", "Skottet, med befintligt dagsikte"],
            ["Synfält", "Brett, lätt att söka med", "Smalare, fast grundförstoring", "Beror på kikarsiktet"],
            ["Regler (jakt)", "Spaning oreglerad", "14 a §: vildsvin, öppen terräng/åtel", "14 a §: samma som sikte"],
            ["Byta vapen", "Oberoende av vapen", "Ett sikte per vapen eller ny inskjutning", "Flyttas med adapter"],
            ["Pris", "Från ca 5 000 kr", "Från ca 15 000 kr", "Från ca 20 000 kr"],
        ], mono_first=False)}
        <p>Den handhållna kameran är det naturliga första köpet: mest nytta per krona och fri att använda. Om termiska sikten och clip-on skriver vår systersajt {ext(SISTER + "/", "Värmesikte.se")} i detalj.</p>
    ''')
    body += sec("teknik", "Teknik i fält: tio vanor som ger bättre bild", f'''
        {ol([
            "Ställ dioptrin en gång, i ljus, mot menytexten. Markera ringen.",
            "Lär dig fokusringen med handske på. Avståndet växlar oftare än du tror.",
            "Sätt NUC på manuell och kalibrera när inget händer, inte när grisen kommer.",
            "Prova black hot i fukt och white hot i torr kyla. Red hot när marken är varm på sommaren.",
            "Sänk displayens ljusstyrka. Det sparar batteri och mörkerseende på ögat du inte tittar med.",
            "Håll linsskyddet på tills du behöver bilden. Regn, snö och imma på germanium ger platt bild.",
            "Bär reservbatteriet innanför jackan. Kyla halverar kapaciteten.",
            "Stäng av Wi-Fi när du inte streamar. Det drar mer än displayen.",
            "Bestäm din identifieringsgräns i dagsljus mot kända djur, med din kamera.",
            "Ladda ner inspelningarna. Fullt minne på vaken betyder ingen video när det händer.",
        ])}
        <p>Problem som ändå uppstår, med orsak och lösning, finns på sidan <a href="problem.html">Problem</a>. Vilken kamera som passar, på <a href="kopguide.html">Köpguide</a>.</p>
    ''')
    body += article_close()
    return {
        "slug": "varmekamera-for-jakt.html",
        "title": "Värmekamera för jakt: spaning, åtel, eftersök och vad kameran måste klara",
        "short": "Värmekamera för jakt",
        "description": "Så används värmekamera på jakt: spaning, åtel och vak, eftersök och inventering. Vilka krav varje situation ställer på synfält, brännvidd, sensor och avståndsmätare, och vad reglerna säger.",
        "body": body,
    }


# ---------------------------------------------------------------------------
# KÖPGUIDE
# ---------------------------------------------------------------------------
def kopguide() -> dict:
    chips = [("#prisklasser", "Prisklasser"), ("#checklista", "Checklista"), ("#under-10", "Under 10 000"), ("#10-20", "10 000–20 000"), ("#over-20", "Över 20 000"), ("#multispektral", "Multispektral"), ("#tillbehor", "Tillbehör")]
    body = page_hero("Köpguide", "Köpguide: välja värmekamera för jakt 2026",
                     "Vi rangordnar inte med poäng. Vi beskriver vad varje prisklass köper, vad som faktiskt skiljer modellerna och vilka som passar vilken jakt. Aktuellt pris och lagerstatus ser du hos Nordic Aim.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "Under 10 000 kr får du en kompakt 256- eller 384-kamera med 10–19 mm objektiv som räcker för skog, gården och eftersök på korta håll. Mellan 10 000 och 20 000 kr ligger allroundklassen: 384/25–35 mm eller 640/25 mm med OLED-display och bytbart batteri. Över 20 000 kr köper du 640–1280 pixlar, 35–50 mm, låg NETD och laseravståndsmätare för öppna fält. Välj brännvidd efter din mark först, sensor efter hur mycket du söker av stora ytor, och lägg hellre pengar på optik och display än på räckviddssiffran."
    ) + "</div>"
    body += article_open()
    body += sec("prisklasser", "Vad pengarna köper", f'''
        {table(["Prisklass", "Typisk spec", "Får du", "Får du inte"], [
            ["5 000–10 000 kr", "256×192 eller 384×288, 10–19 mm, inbyggt batteri", "Kompakt, startar snabbt, fokusfri. Bra i skog och på gården. Detektion 400–800 m.", "Detalj på håll, bytbart batteri, LRF. Ofta enklare display."],
            ["10 000–20 000 kr", "384/25–35 mm eller 640/25 mm, OLED, ofta bytbart batteri", "Allround för åtel, skogspass, eftersök och mindre fält. NETD 15–25 mK.", "Riktigt lång räckvidd; LRF bara på vissa modeller."],
            ["20 000–35 000 kr", "640×512 35–50 mm, LRF, NETD ≤20 mK, 1024×768 AMOLED", "Öppna fält, bedömning på 200–300 m, inspelning, modulära batterier.", "Lägre vikt. Dessa väger 400–600 g."],
            ["35 000 kr+", "1024–1280 pixlar, 50 mm+, LRF, multispektral", "Bredast synfält och längst detalj samtidigt. Inventering, stora slätter.", "Nytta i skog. Där räcker en kortare brännvidd."],
        ], mono_first=False)}
        <p>Priserna är ungefärliga intervall för handhållna värmekameror i Sverige hösten 2026. Enskilda modeller kan ligga utanför.</p>
    ''')
    body += sec("checklista", "Checklista innan du bestämmer dig", f'''
        {ol([
            "<strong>Var jagar du mest?</strong> Tät skog → kort brännvidd och brett synfält. Fält → lång brännvidd och LRF. Blandat → 35 mm.",
            "<strong>Hur stora ytor söker du av?</strong> Då betalar 640-sensorn för sig i färre drag och mer zoomutrymme. Annars räcker 384.",
            "<strong>Hur är vädret där du jagar?</strong> Fuktigt kustklimat och dimmiga dalar → prioritera NETD under 20 mK.",
            "<strong>Hur länge sitter du?</strong> Över fyra timmar i kyla → bytbart batteri eller powerbank-stöd är viktigare än timsiffran.",
            "<strong>Enhands?</strong> Prova med handske. Knappar, fokusring och vikt (under 400 g för långa pass).",
            "<strong>Display.</strong> OLED 1024×768 eller mer om du ska titta länge. 640×400 duger för korta titt.",
            "<strong>Bildbehandling.</strong> Titta på en blöt väg i kvällsljus med två kameror sida vid sida. Det säger mer än databladet.",
            "<strong>Kalibrering.</strong> Manuell NUC eller slutarfri om du irriterar dig på klick.",
            "<strong>Inspelning och app.</strong> Internminne, Wi-Fi och stabil app om du vill dela eller dokumentera.",
            "<strong>Support och garanti.</strong> Svensk återförsäljare som skickar från Sverige, öppet köp och svenska manualer. Termisk optik går sönder sällan, men när det händer vill du inte skicka den till ett annat land.",
        ])}
    ''')
    body += sec("under-10", "Under 10 000 kr: fickformat och instegsmodeller", f'''
        <p>Här är kamerorna små, fokusfria eller nästan, och byggda för att alltid ligga i fickan. 256×192 med 9–10 mm objektiv ger ett synfält på runt 30 m på 100 m och artbestämning på vildsvin kring 100 m. 384-modeller med 15–19 mm sträcker det till 150–250 m. Det räcker för skog, åtel på nära håll, hunden i mörkret och eftersök. Det räcker inte för att bedöma djur över en stor åker.</p>
        {card_grid([
            _p("HIKMICRO", "Fickformat", "Lynx LE10 3.0", "256×192 på 12 µm, 9,7 mm f/1.0 fokusfri, 18° synfält, slutarfri drift (HSIS). 64 GB internminne och video med ljud.",
               "800q-01_135695.png?v=1769171478", "HIKMICRO Lynx LE10 3.0 värmekamera", ["256×192", "9,7 mm", "<20 mK"], "hikmicro-lynx-le10-3-0-termisk-monokikare"),
            _p("Guide", "Fickformat", "TE210S", "256×192, NETD 15 mK, 10 mm f/1.0, 31 m synfält på 100 m, 228 g, IP67. En knapp och en ring, går att sköta med handske.",
               "TE210S_1.jpg?v=1791396845", "Guide TE210S värmekikare", ["256×192", "15 mK", "228 g"], "guide-te210s-256x192-10-mm-varmekikare"),
            _p("RIX", "Kompakt 384", "Pocket K3", "384×288 på 12 µm, 15 mm f/1.0, 17,5° synfält och elektronisk bildstabilisering. 384-sensor i fickformat.",
               "K3.jpg?v=1778936911", "RIX Pocket K3 termisk monokikare", ["384×288", "15 mm", "EIS"], "rix-pocket-k3-384x288-termisk-monokikare-med-bildstabilisering"),
            _p("PixFra", "Allround", "Mile M2 384×288 25 mm", "384-sensor, 25 mm f/1.0, OLED 800×600, 320 g och IP67. Det mesta av mellanklassen till instegspris.",
               "PIX-PFI-M425___Pixfra-Mile-2-M425-Thermal-Imaging-Monocular.png?v=1766943659", "PixFra Mile M2 384×288 25 mm värmekikare", ["384×288", "25 mm", "≤25 mK"], "pixfra-mile-m2-384x288-25-mm-varmekamera"),
        ])}
    ''')
    body += sec("10-20", "10 000–20 000 kr: allroundklassen", f'''
        <p>Här hamnar de flesta som jagar både skog och fält. 384 med 25–35 mm eller 640 med 25 mm, OLED-display, ofta bytbart 18650- eller APS-batteri och NETD runt 15–25 mK. Skillnaden mot klassen under är detalj på håll, lugnare bild och batteri som går att byta i mörkret.</p>
        {card_grid([
            _p("Pulsar", "Kompakt allround", "Axion XQ19 Compact", "384×288 (17 µm), 19 mm f/1.0, 19,5° synfält, AMOLED, APS3-batteri och IPX7. Pulsars minsta, med Stream Vision 2.",
               "Axion_XQ19_Compact_0001_d7b2d958-7163-4f11-b809-73eb9cd9cd40.webp?v=1766941790", "Pulsar Axion XQ19 Compact värmekamera", ["384×288", "19 mm", "<18 mK"], "pulsar-axion-xq19-compact-384x288-varmekamera"),
            _p("HIKMICRO", "Allround 384", "Lynx LH25 3.0", "384×288 på 12 µm, 25 mm f/1.0, NETD <15 mK, 1920×1080 AMOLED och slutarfri drift. Bytbart 18650.",
               "800q-01_134887.png?v=1766941202", "HIKMICRO Lynx LH25 3.0 termisk monokikare", ["384×288", "25 mm", "<15 mK"], "hikmicro-lynx-lh25-3-0-thermal-monocular"),
            _p("PixFra", "640 till 384-pris", "Mile M3 640×512 25 mm", "640 på 12 µm bakom 25 mm f/0.9: 17,4° synfält, NETD ≤15 mK, OLED 1920×1080, 290 g. Drygt halva bilden till i sidled jämfört med 384-modellen.",
               "M625-V35.png?v=1789068759", "PixFra Mile M3 640×512 25 mm värmekikare", ["640×512", "25 mm", "≤15 mK"], "pixfra-mile-m3-640x512-25-mm-varmekikare"),
            _p("Nocpix", "384 med LRF", "LUMI L35R", "384×288 VOx, 35 mm f/0.9, 4× grundförstoring, laseravståndsmätare till 800 m och 1024×768 AMOLED. För den som vill veta avståndet.",
               "bvJqouxK0PQGJbXyrPj0nYWqTRLc2JjQ3UkE4vZG.webp?v=1766941595", "Nocpix LUMI L35R värmekikare", ["384×288", "35 mm", "LRF"], "nocpix-lumi-l35r"),
        ])}
        {muted(f"Jämförelse av fabrikaten: {nalink('/blogs/nyheter/hikmicro-nocpix-eller-pulsar', 'HIKMICRO, Nocpix eller Pulsar?')} och {nalink('/blogs/nyheter/hikmicro-lynx-3-0-guide', 'HIKMICRO Lynx 3.0: guide till serien')}.")}
    ''')
    body += sec("over-20", "Över 20 000 kr: öppna fält och lång räckvidd", f'''
        <p>640 eller fler pixlar bakom 35–50 mm, laseravståndsmätare, NETD under 20 mK och stora AMOLED-displayer. Det här är kameror för vak över fält, bedömning av djur på 200–300 m och för den som sitter många långa pass och vill ha en lugn bild. Vikten ligger på 400–600 g; räkna med rem eller stöd.</p>
        {card_grid([
            _p("PixFra", "640 med LRF", "Arc Pro A650P LRF", "640×512 på 12 µm, NETD ≤20 mK, 50 mm f/1.0 och laser till 1 000 m. Detektion 2 600 m, artbestämning kring 570 m på vildsvin.",
               "954682-0.jpg?v=1789068911", "PixFra Arc Pro A650P LRF värmekikare", ["640×512", "50 mm", "LRF"], "pixfra-arc-pro-a650p-lrf-640x512-50-mm-varmekikare-med-laseravstandsmatare"),
            _p("Pulsar", "Öppna fält", "Telos XP50 LRF", "640×480 (17 µm), NETD <18 mK, F50/1.0, laser 1 000 m, AMOLED 1024×768, IPX7 och modulär design med LPS-batteri.",
               "938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791", "Pulsar Telos XP50 LRF värmekamera", ["640×480", "50 mm", "LRF"], "pulsar-telos-xp50-lrf-640x480-varmekamera-med-laseravstandsmatare"),
            _p("Pulsar", "HD-sensor", "Telos XL50 LRF", "1024×768 på 12 µm bakom F50/1.0. Både bredare synfält och längre detalj än XP50, tack vare den mindre pixeln.",
               "947332-0_a2f71263-24ec-4286-a74a-4630c91fdf9f.jpg?v=1766941792", "Pulsar Telos XL50 LRF värmekamera", ["1024×768", "12 µm", "LRF"], "pulsar-telos-xl50-lrf-1074x768-varmekamera-med-laseravstandsmatare"),
        ])}
        {muted(f"Alla modeller: {nalink('/collections/varmekikare', 'värmekikare hos Nordic Aim', True)}. Per fabrikat: {nalink('/collections/pulsar-varmekikare', 'Pulsar', True)}, {nalink('/collections/nocpix-varmekikare', 'Nocpix', True)}, {nalink('/collections/pixfra-varmekikare', 'PixFra', True)}, {nalink('/collections/hikmicro', 'HIKMICRO', True)}, {nalink('/collections/guide', 'Guide', True)}.")}
    ''')
    body += sec("multispektral", "Multispektral: värmekamera och digital nattkikare i samma hus", f'''
        <p>En multispektral kikare har två kanaler: en termisk för att hitta, och en digital dag/natt-kanal (ofta 4K CMOS med IR-belysning) för att se detaljer som fläckar, horn och ansikte. Du söker med värme och växlar till digital bild för att artbestämma. Vissa modeller kan lägga kanalerna ovanpå varandra (fusion). Priset är vikt, storlek och en högre prislapp, men för den som vill identifiera säkert på närmare håll är det ofta mer värt än en större termisk sensor.</p>
        {card_grid([
            _p("HIKMICRO", "Multispektral", "Habrok 4K HE25L 2.0", "256×192 termisk (NETD <18 mK, 25 mm) plus 4K CMOS 3840×2160 med 60 mm optik, laser till 1 000 m. Två kikare i en.",
               "800q-HE25L_202.0_1.png?v=1769171478", "HIKMICRO Habrok 4K HE25L 2.0 multispektral kikare", ["256×192", "4K", "LRF"], "hikmicro-habrok-4k-he25l-2-0-multispektral-kikare"),
        ], 320)}
        {muted(f"Fler modeller under {nalink('/collections/multispektrala-kikare', 'multispektrala kikare', True)}. Hur termiskt och digitalt skiljer sig förklaras på <a href='varmekamera-vs-morkerkikare.html'>Värmekamera eller mörkerkikare</a>.")}
    ''')
    body += sec("tillbehor", "Tillbehör som behövs", f'''
        {ul([
            f"<strong>Extra batteri</strong> av rätt typ (18650, APS, LPS). {nalink('/collections/batterier', 'Batterier hos Nordic Aim', True)}.",
            "<strong>Powerbank med USB-C PD</strong> och kort kabel för kameror som kan drivas externt.",
            "<strong>Bröstrem eller halsrem</strong> med snabbfäste så att kameran hänger rätt när vapnet lyfts.",
            "<strong>Linsduk för germanium</strong> (mjuk mikrofiber) och en burk tryckluft. Aldrig pappersnäsduk på DLC-beläggningen.",
            "<strong>Litet stativ eller bönpåse</strong> för inventering och långa titt på 50 mm.",
        ])}
        <p>Osäker på valet? {nalink('/pages/kontakta-oss', 'Nordic Aim ger personlig rekommendation')} utifrån din mark, din jakt och din budget, utan köpkrav. Nordic Aims egen {nalink('/pages/kopguide-termisk-optik', 'köpguide för termisk optik')} och {nalink('/blogs/nyheter/valja-varmekikare-kopguide-prisklasser', 'guide per prisklass')} går djupare på enskilda modeller.</p>
        {muted(f"Länkarna går till nordicaim.se. {SITE_NAME} drivs av {NA_NAME}; vi tjänar på att du köper via länkarna, och vi skriver det här för att du ska köpa rätt första gången. Mer under <a href='om.html'>Om oss</a>.")}
    ''')
    body += article_close()
    return {
        "slug": "kopguide.html",
        "title": "Köpguide värmekamera för jakt 2026: prisklasser, checklista och modeller",
        "short": "Köpguide",
        "description": "Vilken värmekamera ska du köpa? Prisklasser från 5 000 till 40 000 kr, checklista med tio punkter och modeller sorterade efter användning: skog, allround, öppna fält och multispektral.",
        "body": body,
        "image": CDN + "954682-0.jpg?v=1789068911&width=1200",
    }


# ---------------------------------------------------------------------------
# VÄRMEKAMERA VS MÖRKERKIKARE
# ---------------------------------------------------------------------------
def vs() -> dict:
    chips = [("#tre-tekniker", "Tre tekniker"), ("#jamforelse", "Jämförelse"), ("#nar-vilken", "När vilken"), ("#multispektral", "Multispektral")]
    body = page_hero("Jämförelse", "Värmekamera eller mörkerkikare: vad ser mest, och när?",
                     "Tre tekniker ger bild i mörker: bildförstärkare, digital IR och termisk. De mäter helt olika saker. Här är skillnaderna, fysikaliskt och i fält.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "En värmekamera registrerar objektets egen värmestrålning (8–14 µm) och behöver inget ljus alls; den är bäst på att upptäcka. En mörkerkikare (bildförstärkare eller digital sensor med IR-lampa) förstärker befintligt ljus eller reflekterat nära-infrarött ljus (0,7–1 µm) och ger en fotoliknande bild med detaljer som fläckar, horn och ögon; den är bäst på att identifiera på närmare håll, men ser inget utan ljus och sämre i dimma. Multispektrala kikare kombinerar båda."
    ) + "</div>"
    body += article_open()
    body += sec("tre-tekniker", "Tre tekniker, tre fysikaliska principer", f'''
        {deflist([
            ("Bildförstärkare (analog NV)", "Fotoner från stjärnljus och månsken slår loss elektroner i ett fotokatodrör, elektronerna multipliceras i en mikrokanalplatta och träffar en fosforskärm. Gen 2+/Gen 3-rör ger den klassiska gröna (eller vita) bilden. Mycket ljuskänslig, ingen fördröjning, men dyr, känslig för starkt ljus och ser inget i totalt mörker utan IR-belysning."),
            ("Digital mörkerkikare (digital NV)", "En CMOS-sensor utan IR-filter, ofta med stor pixel och lång exponering, plus en IR-lampa på 850 eller 940 nm som 'belyser' scenen osynligt för ögat. Ger en svartvit eller färgad fotoliknande bild med riktiga detaljer. Räckvidden styrs av lampan, bilden kan släpa vid rörelse, och IR-ljus på 850 nm syns som en svag röd glöd för vilt och människor."),
            ("Värmekamera (termisk)", "Mäter objektets egen strålning i LWIR. Behöver inget ljus och ingen lampa, fungerar lika bra i totalt mörker som i dagsljus, och ser genom rök, lätt dimma och gles vegetation bättre än ögat. Bilden saknar ytdetaljer (fläckar, färg, text) eftersom den visar temperatur, inte reflekterat ljus."),
        ])}
    ''')
    body += sec("jamforelse", "Jämförelse punkt för punkt", f'''
        {table(["", "Värmekamera", "Digital mörkerkikare", "Bildförstärkare"], [
            ["Behöver ljus", "Nej", "Ja, eller IR-lampa", "Ja, lite (stjärnljus) eller IR-lampa"],
            ["Upptäcka djur i skogskant", "Överlägsen", "Bara om lampan når och djuret inte skyms", "Bra vid månljus"],
            ["Identifiera (fläckar, horn, kön)", "Begränsad; siluett och kroppsform", "Bra på lampans räckvidd", "Bra vid tillräckligt ljus"],
            ["Dimma, regn, fukt", "Sämre räckvidd men fungerar", "Lampan reflekteras i dropparna, bilden bländas", "Sämre"],
            ["Genom glas", "Nej", "Ja", "Ja"],
            ["Dagtid", "Fungerar, bilden kan bli platt i värme", "Fungerar som vanlig kamera", "Måste skyddas, kan skadas"],
            ["Upptäcks av viltet", "Inget utsänt", "850 nm-lampa syns som röd glöd; 940 nm nästan inte", "Ingen eller IR-lampa"],
            ["Bedöma kulfång bakom målet", "Bara om bakgrunden har annan temperatur", "Ja, inom lampans räckvidd", "Ja"],
            ["Pris handhållen", "Från ca 5 000 kr", "Från ca 3 000 kr", "Från ca 25 000 kr"],
        ], mono_first=False)}
    ''')
    body += sec("nar-vilken", "När vilken teknik?", f'''
        {ul([
            "<strong>Du vill hitta vilt och se vad som rör sig på marken:</strong> värmekamera. Inget annat upptäcker lika bra.",
            "<strong>Du vill se om bocken bär horn eller om det är rätt gris:</strong> digital mörkerkikare eller multispektral på under 100–150 m, eller en värmekamera med många pixlar på målet (640/50 mm) på längre håll.",
            "<strong>Du spanar från ett torn med glas:</strong> digital. Eller öppna rutan.",
            "<strong>Fuktigt kustklimat:</strong> värmekamera med låg NETD. IR-lampan i en digital kikare bländar i dimma.",
            "<strong>Eftersök:</strong> värmekamera för att lokalisera, pannlampa och hund för resten.",
            "<strong>Begränsad budget:</strong> en bra 384-värmekamera gör mer nytta än en billig digital kikare, eftersom den löser det svåraste problemet: att hitta djuret.",
        ])}
        <p>Många jagar med båda: värmekamera i handen för att hitta, digitalt eller termiskt sikte på vapnet för skottet. Nordic Aim jämför de två siktevarianterna i {nalink('/blogs/nyheter/morkersikte-eller-varmesikte', 'Digitalt mörkersikte eller värmesikte: vad passar din jakt?')}.</p>
    ''')
    body += sec("multispektral", "Multispektral: båda i samma hus", f'''
        <p>De senaste åren har flera tillverkare satt en termisk sensor och en digital 4K-sensor med IR-belysning i samma kikare. Du söker med värme, trycker på en knapp och ser samma scen som digital bild med alla detaljer, eller låter kameran lägga värmesignaturen som en färgad kontur ovanpå den digitala bilden (fusion). Det löser det termiska problemet med identifiering utan att tappa förmågan att upptäcka.</p>
        <p>Kompromisserna är vikt (ofta 600–900 g), pris och att den digitala kanalens räckvidd i mörker fortfarande styrs av IR-lampan. Modeller finns från HIKMICRO (Habrok), Pulsar (Symbion) och PixFra (Draco). Se {nalink('/collections/multispektrala-kikare', 'multispektrala kikare hos Nordic Aim', True)}.</p>
        {muted(f"Termiska <em>sikten</em> mot digitala mörkersikten på vapnet behandlas på systersajten {ext(SISTER + '/faq.html', 'Värmesikte.se')}.")}
    ''')
    body += article_close()
    return {
        "slug": "varmekamera-vs-morkerkikare.html",
        "title": "Värmekamera eller mörkerkikare? Termisk, digital IR och bildförstärkare jämförda",
        "short": "Värmekamera eller mörkerkikare",
        "description": "Skillnaden mellan värmekamera, digital mörkerkikare och bildförstärkare: fysiken, vad varje teknik ser och inte ser, en jämförelsetabell och när du ska välja vilken. Plus multispektrala kikare.",
        "body": body,
    }


# ---------------------------------------------------------------------------
# ANVÄNDNINGSOMRÅDEN
# ---------------------------------------------------------------------------
def anvandning() -> dict:
    chips = [("#jakt", "Jakt och vilt"), ("#raddning", "Räddning och säkerhet"), ("#bygg", "Byggnad och energi"), ("#industri", "Industri och el"), ("#dronare", "Drönare"), ("#mobil", "Mobiltillsatser"), ("#valja", "Olika kameror")]
    body = page_hero("Användningsområden", "Vad en värmekamera används till, och varför kamerorna skiljer sig",
                     "Samma mikrobolometerteknik sitter i jägarens kikare, byggbesiktarens termografikamera och drönarens gimbal. Men kraven är olika, och en kamera byggd för det ena är ofta fel för det andra.", chips)
    body += '<div style="max-width:820px;margin:0 auto;padding:40px 24px 0">' + short_answer(
        "Värmekameror används inom jakt och viltvård (spana, bedöma, eftersök, inventera), räddningstjänst och sjöräddning (hitta personer, se genom rök), byggnadstermografi (köldbryggor, fukt, läckage, värmegolv), industri och el (överhettade kopplingar, lager, isolering), brandövervakning, drönare och fordon. Jaktkameror optimeras för bildfrekvens, synfält och räckvidd på en människostor kropp; termografikameror för temperaturmätning och dokumentation, ofta vid 9 Hz."
    ) + "</div>"
    body += article_open()
    body += sec("jakt", "Jakt, viltvård och eftersök", f'''
        <p>Handhållna värmekameror (värmekikare) för spaning och eftersök, termiska sikten för skottet på vildsvin, och allt oftare kameror för inventering och skadeförebyggande arbete i lantbruket. Kraven: 50 Hz, brett synfält, snabb start, låg vikt, tålighet mot kyla och regn. Temperaturmätning behövs inte och saknas därför oftast.</p>
        <p>Fördjupning: <a href="varmekamera-for-jakt.html">Värmekamera för jakt</a>, <a href="kopguide.html">Köpguide</a> och <a href="regler.html">Regler</a>.</p>
    ''')
    body += sec("raddning", "Räddningstjänst, sjöräddning och säkerhet", f'''
        <p>Brandmän använder värmekamera för att hitta personer i rökfyllda rum, se glödbränder i väggar och tak, och bedöma brandgasernas temperatur. Sjöräddning och polis använder den för att hitta människor i vatten, skog och mörker; en kropp i 10-gradigt vatten syns i minuter, en i skogen i timmar. Här prioriteras tålighet, enkel hantering och ofta en temperaturskala i bilden. Kamerorna liknar jaktkamerorna tekniskt, men är certifierade för värme och fall, och visar ofta absolut temperatur.</p>
    ''')
    body += sec("bygg", "Byggnadstermografi och energi", f'''
        <p>Många som söker på "värmekamera" letar efter en kamera till huset. Med en termografikamera ser du köldbryggor, dålig isolering, otätheter kring fönster, fukt i väggar (fukt kyler genom avdunstning), var golvvärmeslingorna går och om elementet är luftat. Här är kraven nästan de omvända mot jakt: temperaturmätning med ±2 °C noggrannhet, emissivitetsinställning, ofta 9 Hz räcker, brett synfält för att få med en vägg på nära håll, och programvara för rapporter. Upplösningen är ofta låg (160×120 till 320×240) men pixlarna är stora och kalibrerade.</p>
        {callout("Kan jag använda min jaktkamera på huset?", "Du ser köldbryggor och läckage lika bra, ofta bättre tack vare högre upplösning och NETD. Men du får ingen temperaturskala, ingen emissivitetskorrigering och ingen rapportfunktion. För att hitta var det drar räcker den. För en besiktning som ska dokumenteras behövs en termografikamera.", "grey")}
    ''')
    body += sec("industri", "Industri, el och process", f'''
        <p>Förebyggande underhåll: en varm fas i ett elskåp, ett lager som går varmt, en motor med dålig kylning, en ventil som läcker ånga, en isolering med luckor. Fasta värmekameror övervakar bränsledepåer, avfallsanläggningar och sågverk dygnet runt för att larma om självantändning innan det brinner. Processindustrin använder kameror med kalibrerad radiometri för att mäta temperaturer från −20 till över 1 000 °C. Här är mätnoggrannhet, kalibrering, mätområde och integration med styrsystem viktigare än bildfrekvens och synfält.</p>
    ''')
    body += sec("dronare", "Drönare", f'''
        <p>Lätta mikrobolometrar (256–640 pixlar) i gimbal under drönare används för eftersök, inventering av vilt, sök efter försvunna personer, inspektion av solcellsparker och kraftledningar samt brandbevakning. För vilt ger höjden överblick över stora ytor på kort tid, och värmen gör att djur i högt gräs syns tydligt. Kameran ställer samma krav som en jaktkamera på bildfrekvens och NETD, plus lågt vikt och digital överföring. Flygning regleras av Transportstyrelsen (drönarkort, kategorier) och störning av vilt av jaktlagstiftningen; inventering med drönare görs i praktiken av yrkesfolk eller vana piloter.</p>
    ''')
    body += sec("mobil", "Mobiltillsatser och enklaste kamerorna", f'''
        <p>Tillsatser till telefonen (USB-C eller Lightning) och de billigaste handhållna kamerorna har sensorer på 80×60 till 256×192 med 9 Hz och NETD 40–70 mK. De fungerar för att hitta en varm koppling, se var golvvärmen går eller leta efter husdjuret på tomten. För jakt är 9 Hz för hackigt och räckvidden för kort, men som första kontakt med tekniken, och för huset, är de ett bra köp.</p>
    ''')
    body += sec("valja", "Samma teknik, olika kameror", f'''
        {table(["", "Jakt", "Byggnad/termografi", "Industri/process", "Räddning"], [
            ["Bildfrekvens", "50 Hz", "9 Hz räcker", "9–30 Hz", "30–60 Hz"],
            ["Upplösning", "384–1280", "160–640", "320–1280", "320–640"],
            ["Temperaturmätning", "Nej", "Ja, ±2 °C", "Ja, kalibrerad, stort område", "Ja, grov"],
            ["Synfält", "7–20°", "25–50°", "Utbytbara objektiv", "40–60°"],
            ["Okular/display", "Okular, OLED", "Skärm på baksidan", "Skärm, nätverk", "Skärm, stor"],
            ["Viktigast", "Räckvidd, NETD, snabb start", "Noggrannhet, rapport", "Kalibrering, integration", "Tålighet, enkel hantering"],
        ], mono_first=False)}
        <p>{SITE_NAME} skriver i första hand om handhållna värmekameror för jakt och spaning, eftersom det är vad {NA_NAME} säljer och kan. Tekniksidorna, <a href="sa-fungerar-en-varmekamera.html">Så fungerar en värmekamera</a> och <a href="sensor-och-upplosning.html">Sensor och NETD</a>, gäller alla värmekameror oavsett användning.</p>
    ''')
    body += article_close()
    return {
        "slug": "anvandningsomraden.html",
        "title": "Vad används en värmekamera till? Jakt, räddning, byggnad, industri och drönare",
        "short": "Användningsområden",
        "description": "Användningsområden för värmekamera: jakt och eftersök, räddningstjänst, byggnadstermografi, industri och el, drönare och mobiltillsatser. Varför kamerorna skiljer sig och vad som krävs i varje fall.",
        "body": body,
    }


def pages() -> list[dict]:
    return [jakt(), kopguide(), vs(), anvandning()]
