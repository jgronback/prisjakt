"""Stödsidor: Problem, Regler, Ordlista, FAQ, Om oss, Integritet, 404."""
from build import (na, nalink, ext, eyebrow, page_hero, article_open, article_close, sec, callout,
                   short_answer, table, deflist, ul, ol, muted, faq_details, problem_card, SITE_NAME, NA_NAME,
                   NA_ORGNR, NA_MAIL, NA_TEL, SISTER, BASE_URL)


# ---------------------------------------------------------------------------
# PROBLEM
# ---------------------------------------------------------------------------
PROBLEMS = [
    ("P01", "Väder", "Platt, grå bild i regn och dimma",
     "En fuktig höstnatt blir bilden mjölkig. Djur på håll smälter ihop med bakgrunden, och grusvägen är en jämn yta.",
     "Vattendroppar i luften absorberar och sprider långvågig infraröd strålning, så mindre når linsen. Blöta ytor får dessutom nästan lufttemperatur genom avdunstning, och kontrasten mellan mark, sten och päls försvinner.",
     "En sensor med låg NETD (under 20 mK), manuella reglage för kontrast och ljusstyrka, och realistiska förväntningar på räckvidd.",
     "Byt till black hot, som ofta ger tydligare konturer i fukt. Sänk ljusstyrkan och höj kontrasten manuellt. Räkna med halverad praktisk räckvidd och sök av marken oftare på kortare håll. Vid nästa köp: prioritera NETD om du jagar i fuktigt klimat."),
    ("P02", "Väder", "Sommarnätter: marken lyser lika mycket som djuret",
     "I juli lyser hela åkern. Vildsvinen är svåra att skilja från bakgrunden. I oktober är samma kamera kristallklar.",
     "Solvarm mark, sten och stubbar kan hålla djurtemperatur långt in på natten. Kamerans AGC fördelar kontrasten över hela temperaturspannet i bilden, och när spannet är litet blir allt medelgrått.",
     "En palett som lyfter fram de varmaste punkterna, och tålamod.",
     "Vänta tills marken kylts av, ofta efter midnatt. Använd red hot eller en palett som färgar bara de varmaste zonerna. Sänk ljusstyrkan. Titta mot norrsluttningar och skuggsidor där marken svalnat först."),
    ("P03", "Bild", "Bilden är suddig fast djuret är nära",
     "Kanterna flyter. Riktmärket eller menyn är skarp men djuret är oskarpt, eller tvärtom.",
     "Två separata fokus: objektivets för avståndet till målet och dioptrin för ditt öga mot displayen. Många ställer bara det ena. Vid f/1.0 är skärpedjupet litet, så fokus på 40 m ger oskärpa på 150.",
     "Lättåtkomlig fokusring och en dioptri som går att låsa.",
     "Ställ dioptrin först, i ljus, tills menytexten är knivskarp. Markera läget. Ställ sedan objektivfokus på det avstånd du väntar vilt, och vrid när avståndet ändras. Fokusfria kameror (9–10 mm) slipper problemet men har mindre detalj på håll."),
    ("P04", "Bild", "Immig eller frusen lins ger platt bild",
     "Efter en stund i kyla eller när kameran tas ut ur varm bil blir bilden grå och mjuk, trots att vädret är klart.",
     "Kondens eller rimfrost på germaniumlinsen. Kameran ser då sin egen iskristall, som har samma temperatur som luften, i stället för scenen bakom. Handvärme på huset kan också värma linsens kant och ge en gradient i bilden.",
     "Linsskydd, och att låta kameran acklimatisera.",
     "Håll linsskyddet på tills du behöver bilden. Låt kameran acklimatisera i ytterfickan, inte innanför jackan. Torka med mikrofiberduk, aldrig med papper eller handske mot DLC-beläggningen. Blås bort snö med andedräkten på avstånd, inte direkt på linsen."),
    ("P05", "Fysik", "Den ser inte genom tornfönstret",
     "Från jakttornet är bilden en jämn grå yta med en svag spegelbild av dig själv. Utanför, med rutan öppen, ser du allt.",
     "Glas är ogenomskinligt för strålning vid 8–14 µm. Kameran visar rutans egen yttemperatur, och eftersom glas också reflekterar en del LWIR ser du dig själv svagt. Samma gäller bilrutor, glasögon och plexiglas.",
     "Ett öppet fönster. Inget kamerabyte löser det.",
     "Öppna rutan eller luckan innan du behöver bilden. Tänk på det när du bygger torn: en lucka som går att öppna tyst är värd mer än ett stort fönster. Tunn polyetenfilm (som en ren fryspåse) släpper igenom en del LWIR om du behöver vindskydd."),
    ("P06", "Ström", "Batteriet dör mitt i passet",
     "Tillverkaren anger åtta timmar. En kall natt i januari är det slut efter tre.",
     "Litiumbatterier tappar kapacitet när cellen är kall, och timsiffran är mätt i rumstemperatur. Display på hög ljusstyrka, inspelning, Wi-Fi och LRF drar mer än viloläge.",
     "Bytbart batteri eller extern matning, och möjlighet att stänga av strömtjuvar.",
     "Välj kamera med bytbart batteri eller USB-C-drift från powerbank. Bär reservbatteriet innanför jackan och byt när kapaciteten sjunker. Stäng av Wi-Fi, sänk displayens ljusstyrka och ställ kortare tid till standby. Ladda fullt kvällen före, litiumceller självurladdar lite men mår inte bra av att ligga tomma."),
    ("P07", "Säkerhet", "En varm fläck är inte ett lovligt vilt",
     "Något varmt lyser i åkerkanten på 180 m. Formen är otydlig och det ligger stilla.",
     "Detektionsräckvidden är många gånger längre än avståndet där du kan identifiera art, kön och ålder. Solvarma stenar, hö, myrstackar och tamdjur ger också värmesignatur. Vid 2 pixlar över målet ser en hare och en stubbe likadana ut.",
     "Tillräckligt många pixlar på målet för identifiering, och tålamod att vänta på rörelse.",
     "Sätt en egen gräns för identifieringsavstånd med din kamera, i dagsljus mot kända djur. Zooma in, vänta på rörelse, mät avståndet. Avstå om du inte är säker. Fler pixlar (640) och längre brännvidd flyttar gränsen, men tar inte bort den."),
    ("P08", "Bild", "Det klickar och bilden fryser",
     "Med jämna mellanrum hörs ett klick och bilden står stilla en bråkdels sekund, ibland precis när djuret rör sig.",
     "Sensorn kalibrerar (NUC): en slutare täcker sensorn så att alla element kan nollställas mot samma temperatur. I automatiskt läge väljer kameran själv tidpunkten, oftast efter tid eller temperaturdrift.",
     "Kontroll över när kalibreringen sker.",
     "Sätt NUC på manuell eller halvautomatisk och utlös den själv när inget händer. Gör det efter att kameran acklimatiserat, så behöver den färre omkalibreringar. Irriterar klicket: välj en modell med slutarfri korrigering (t.ex. HIKMICRO HSIS)."),
    ("P09", "Bild", "Stråk, ränder eller en fast fläck i bilden",
     "Ett vertikalt stråk, ett rutmönster eller en ljus fläck som ligger kvar oavsett vart du riktar kameran.",
     "Drift mellan sensorns element efter temperaturändring (behöver ny NUC), smuts eller vatten på linsen, eller i sällsynta fall en skadad pixel eller ett inbränt mönster efter att kameran riktats mot solen.",
     "Ny kalibrering, ren lins, och att aldrig rikta kameran mot solen.",
     "Kalibrera manuellt. Kontrollera och rengör linsen. Rikta aldrig kameran mot solen, inte heller med linsskydd av tunn plast; solen kan ge en permanent 'bränd' fläck i mikrobolometern. Kvarstår felet efter kalibrering och rengöring: kontakta återförsäljaren."),
    ("P10", "Handhavande", "Digital zoom lurar avståndsbedömningen",
     "På 4× ser grisen ut att stå på 60 m. Den stod på 130.",
     "Digital zoom ändrar bildens storlek men inte din vana att bedöma avstånd efter hur stort djuret ser ut. I en termisk bild saknas dessutom de djupledtrådar (skärpa, färg, skuggor) som ögat använder.",
     "Avståndsinformation oberoende av zoom.",
     "Mät i förväg: pinna ut åteln eller lär dig avstånden i kartappen. På varierande avstånd är inbyggd LRF den funktion som gör störst skillnad. Spana på grundförstoring och zooma bara för att bedöma, inte för att leta."),
    ("P11", "Handhavande", "Bilden släpar eller är hackig vid rörelse",
     "När du panorerar eller djuret springer blir bilden suddig, eller rör sig i ryck.",
     "Antingen en kamera med låg bildfrekvens (9 eller 25 Hz), eller tidsbaserad brusreducering som medelvärdesbildar flera bildrutor och ger spår efter rörliga objekt.",
     "50 Hz och en brusreducering som går att sänka.",
     "Kontrollera bildfrekvensen i databladet; 9 Hz-kameror är inte byggda för rörligt vilt. Sänk brusreducering/'smooth'-läge i menyn om kameran har det. Panorera långsammare än du tror behövs."),
    ("P12", "Köp", "Höga siffror, dålig bild",
     "En kamera med 640-sensor och lågt mK-tal ger ändå sämre bild än kompisens äldre 384.",
     "Sensorupplösning, displayupplösning, objektivkvalitet och bildbehandling är separata led. En billig display eller ett enkelt objektiv drar ner hela kedjan. NETD mäts olika av olika tillverkare, och 'sensor-NETD' säger inte vad kameran levererar.",
     "En bedömning av hela kedjan, i mörker, mot verkliga djur.",
     "Jämför inom samma tillverkare, läs oberoende bildjämförelser och prova om du kan. Fråga återförsäljaren vilka modeller de själva jagar med och varför. Lägg hellre pengar på objektiv och display än på räckviddssiffran."),
    ("P13", "App", "Appen tappar kontakten eller streamar hackigt",
     "Telefonen hittar inte kameran, eller bilden i appen laggar så att den är oanvändbar för att visa passkompisen.",
     "Kamerans Wi-Fi är en egen accesspunkt med begränsad räckvidd och bandbredd. Telefonen hoppar gärna tillbaka till mobilnät eller hemmanätet. 2,4 GHz störs av annan utrustning, 5 GHz har kortare räckvidd.",
     "Stabil app, 5 GHz-stöd och rätt telefoninställningar.",
     "Stäng av mobildata och automatisk anslutning till andra nät medan du är ansluten. Välj 5 GHz om kameran har det och du är inom några meter. Uppdatera kamerans firmware; app- och Wi-Fi-stabilitet är det som förbättras mest mellan versioner. Spela in i kameran och överför efteråt i stället för att streama när bilden spelar roll."),
]


def problem() -> dict:
    body = page_hero("Problem och lösningar", "Det användare brottas med, och vad som hjälper",
                     "Varje kort följer samma ordning: vad som händer, varför (fysiken bakom), vad som krävs och vad du kan göra. Där en funktion i kameran hjälper säger vi vilken. Där svaret är kunskap, en inställning eller att avstå säger vi det.")
    toc = " · ".join(f'<a href="#{c.lower()}">{c}</a>' for c, *_ in PROBLEMS)
    body += f'<div style="max-width:820px;margin:0 auto;padding:32px 24px 0;font-family:var(--font-mono);font-size:13px;color:var(--text-muted)">Hoppa till: {toc}</div>'
    body += '<section style="max-width:820px;margin:0 auto;padding:40px 24px 96px;display:flex;flex-direction:column;gap:24px">'
    for code, tag, h2, what, why, need, do in PROBLEMS:
        body += problem_card(code, tag, h2, what, why, need, do)
    body += muted("Problemen bygger på situationer som beskrivs i svenska jaktforum, i tillverkarnas manualer och av Nordic Aims kunder. Urvalet är inte en enkät och säger inget om hur vanligt ett problem är eller om ett visst fabrikat.")
    body += f'<p style="font-size:16px">Fler problem i fält, om kameran sitter på vapnet: {ext(SISTER + "/problem.html", "Värmesikte.se: problem från jägare")}.</p>'
    body += "</section>"
    return {
        "slug": "problem.html",
        "title": "Värmekamera: vanliga problem och lösningar (dimma, glas, klick, batteri, suddig bild)",
        "short": "Problem och lösningar",
        "description": "13 vanliga problem med värmekamera förklarade: platt bild i regn, ser inte genom glas, klick och frusen bild (NUC), suddig bild, batteri i kyla, stråk, zoom och avstånd. Orsak och lösning för varje.",
        "body": body,
    }


# ---------------------------------------------------------------------------
# REGLER
# ---------------------------------------------------------------------------
def regler() -> dict:
    body = page_hero("Regler i Sverige", "Får man använda värmekamera på jakt i Sverige?",
                     "Kort svar: ja, handhållen värmekamera för att spana är inte reglerad. Monterad på vapnet gäller 14 a § jaktförordningen. Nedan står vad författningen säger, med källa. Reglerna kan ändras, kontrollera alltid aktuell lydelse innan jakt.")
    body += article_open(40)
    body += sec("lagtext", "Vad jaktförordningen säger", f'''
        <blockquote>"Elektronisk bildförstärkare, elektronisk bildomvandlare, värmekamera eller rörlig belysning får användas i nära anslutning till jaktvapnet vid jakt efter vildsvin. Termiska sikten får dock endast användas vid jakt i öppen terräng eller vid åtelplatser."
          <footer>14 a § jaktförordningen (1987:905), införd genom förordning 2019:174. Lydelse kontrollerad mot riksdagen.se den 14 oktober 2026.</footer></blockquote>
        <p>Bestämmelsen gäller hjälpmedel <em>i nära anslutning till jaktvapnet</em>, alltså sikten och clip-on. Den infördes 2019 och ersatte det tidigare kravet på dispens. Den gäller jakt efter vildsvin. För termiska sikten tillkommer platskravet: öppen terräng eller anordnad åtelplats. Vad som räknas som öppen terräng är inte definierat i förordningen; är du osäker, behandla platsen som skog.</p>
    ''')
    body += sec("praktik", "Vad det betyder i praktiken", f'''
        {ul([
            "<strong>Handhållen värmekamera för att spana, bedöma och söka av marken:</strong> omfattas inte av 14 a §, som gäller hjälpmedel vid vapnet. Enligt Naturvårdsverkets svar till Jakt &amp; Jägare (2023) finns inget förbud mot att spana termiskt, oavsett tid på dygnet och oavsett art. Det är därför den handhållna kameran är det enklaste första köpet.",
            "<strong>Värmekamera som sikte på vapnet (värmesikte, clip-on) vid vildsvinsjakt på åtel eller öppen mark:</strong> tillåtet utan särskilt tillstånd.",
            "<strong>Värmesikte vid vildsvinsjakt i skog utanför åtel:</strong> inte tillåtet. Digitalt mörkersikte (bildförstärkare/bildomvandlare) omfattas inte av platskravet.",
            "<strong>Värmesikte vid jakt på andra arter (räv, mårdhund, hjort, älg):</strong> inte tillåtet med stöd av 14 a §. Undantag kan beslutas av Naturvårdsverket eller länsstyrelsen i enskilda fall, till exempel vid skyddsjakt.",
            "<strong>Eftersök:</strong> att lokalisera skadat vilt med handhållen värmekamera är spaning. Hur siktet på vapnet får användas vid själva avfångningen följer av reglerna för arten.",
            "<strong>Belysning:</strong> belysning vid åtel regleras separat i jaktförordningen. Värmekameran sänder inget ljus och berörs inte av de reglerna.",
        ])}
    ''')
    body += sec("sakerhet", "Säkerhet är fortfarande ditt ansvar", f'''
        <p>Enligt 27 § jaktlagen ska jakt bedrivas så att viltet inte utsätts för onödigt lidande och så att människor och egendom inte utsätts för fara. En termisk bild är tvådimensionell och visar bara temperaturskillnader: kulfång, vägar, hus och människor bakom målet syns bara om de har annan temperatur än omgivningen. Svenska Jägareförbundet avrådde i remissen 2019 från termiska sikten av just det skälet. Identifiera djuret, bedöm kulfånget i dagsljus i förväg och avstå när bilden inte räcker. Se <a href="problem.html#p07">P07</a>.</p>
    ''')
    body += sec("oversyn", "Pågående översyn", f'''
        <p>Naturvårdsverket redovisade i juni 2024 (NV-02007-24) att det inte behövs ytterligare tekniska hjälpmedel för vildsvinsjakt, men att reglerna för när termiska sikten får användas bör förtydligas, och att det finns behov av utbildning. Riksdagens miljö- och jordbruksutskott behandlade frågan i betänkande 2024/25:MJU7. Följ Naturvårdsverket för besked om eventuella ändringar. {NA_NAME} uppdaterar sin genomgång löpande: {nalink('/blogs/nyheter/regler-varmesikte-morkersikte-2026', 'Regler för värmesikten och mörkersikten 2026')}.</p>
    ''')
    body += sec("ovrigt", "Utanför jakten", f'''
        {ul([
            "<strong>Privat bruk</strong> av värmekamera (huset, tomten, friluftsliv) är inte reglerat.",
            "<strong>Drönare</strong> med värmekamera lyder under Transportstyrelsens drönarregler (registrering, drönarkort, kategorier) och kameraövervakningslagstiftning om du filmar platser där människor vistas. Att störa vilt med drönare är inte tillåtet; inventering görs av yrkesfolk med erfarenhet.",
            "<strong>Export</strong>: termiska kameror med bildfrekvens över 9 Hz kan omfattas av exportkontroll som produkter med dubbla användningsområden. Det påverkar dig som privatperson bara om du tar kameran utanför EU; kontrollera reglerna i destinationslandet.",
        ])}
    ''')
    body += sec("kallor", "Källor", f'''
        {ul([
            'Jaktförordning (1987:905), 14 och 14 a §§. <a href="https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/jaktforordning-1987905_sfs-1987-905/" target="_blank" rel="noopener">riksdagen.se</a>',
            'Jaktlag (1987:259), 27 och 30 §§. <a href="https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/jaktlag-1987259_sfs-1987-259/" target="_blank" rel="noopener">riksdagen.se</a>',
            'Miljö- och jordbruksutskottets betänkande 2024/25:MJU7, Jakt och viltvård. <a href="https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/jakt-och-viltvard_hc01mju7/html/" target="_blank" rel="noopener">riksdagen.se</a>',
            'Svensk Jakt, "Naturvårdsverket förordar värmekameror vid vildsvinsjakt". <a href="https://svenskjakt.se/start/nyhet/naturvardsverket-forordar-varmekameror-vid-vildsvinsjakt/" target="_blank" rel="noopener">svenskjakt.se</a>',
            'Svensk Jakt, "Regeringen tillåter mörkersikten vid vildsvinsjakt" (2019). <a href="https://svenskjakt.se/start/nyhet/regeringen-tillater-morkersikten-vid-vildsvinsjakt/" target="_blank" rel="noopener">svenskjakt.se</a>',
            'Jakt &amp; Jägare, "Termisk teknik i dagsljus" (2023). <a href="https://www.jaktojagare.se/utrustning/termisk-teknik-i-dagsljus/" target="_blank" rel="noopener">jaktojagare.se</a>',
            'Länsstyrelsen Västra Götaland, Vildsvinsförvaltning. <a href="https://www.lansstyrelsen.se/vastra-gotaland/djur/jakt-och-vilt/vildsvinsforvaltning.html" target="_blank" rel="noopener">lansstyrelsen.se</a>',
        ])}
        <p>Lagtexten kontrollerad oktober 2026. Detta är information, inte juridisk rådgivning. Reglerna för sikten på vapnet behandlas mer i detalj på {ext(SISTER + "/regler.html", "Värmesikte.se")}.</p>
    ''')
    body += article_close()
    return {
        "slug": "regler.html",
        "title": "Regler för värmekamera på jakt i Sverige: vad jaktförordningen säger",
        "short": "Regler i Sverige",
        "description": "Får man använda värmekamera på jakt? Handhållen spaning är oreglerad; på vapnet gäller 14 a § jaktförordningen: vildsvin, och termiska sikten bara i öppen terräng eller vid åtel. Lagtext, praktik och källor.",
        "body": body,
    }


# ---------------------------------------------------------------------------
# ORDLISTA
# ---------------------------------------------------------------------------
TERMS = [
    ("AGC", "Automatic Gain Control. Bildbehandlingen som bestämmer vilket temperaturintervall som spänns ut över gråskalan. Avgör om en sval skog får struktur eller blir medelgrå."),
    ("AMOLED / OLED", "Displaytyp där varje pixel lyser själv. Ger riktigt svart, hög kontrast och låg strömförbrukning. Vanlig i jaktkameror, 1024×768 eller 1920×1080."),
    ("Amorft kisel (a-Si)", "Membranmaterial i mikrobolometrar. Enklare att tillverka än vanadinoxid, något sämre temperaturkoefficient."),
    ("Artbestämning", "Nordic Aims term för avståndet där du kan se vilken art det är (motsvarar ungefär igenkänning i Johnsons kriterier). Ligger typiskt på en fjärdedel av detektionsavståndet."),
    ("Atmosfäriskt fönster", "Våglängdsband där luften släpper igenom infraröd strålning: 3–5 µm (MWIR) och 8–14 µm (LWIR). Mellan dem absorberar vattenånga och koldioxid."),
    ("Bildfrekvens", "Antal bildrutor per sekund, i hertz. 50 Hz är standard för jakt. 9 Hz förekommer i byggnads- och mobilkameror på grund av exportregler."),
    ("Bildförstärkare", "Analog mörkerkikarteknik (Gen 2+, Gen 3) som förstärker svagt ljus i ett fotokatodrör. Behöver ljus eller IR-lampa, till skillnad från värmekamera."),
    ("Black hot", "Palett där varmt visas svart och kallt vitt. Ger ofta tydligare konturer i fukt och är skonsam för ögat."),
    ("Brännvidd", "Objektivets fokallängd i millimeter (10, 19, 25, 35, 50). Avgör tillsammans med pixelstorleken hur mycket detalj du får på håll, och tillsammans med sensorstorleken synfältet."),
    ("Clip-on", "Termisk tillsats som monteras framför ett vanligt kikarsikte. Räknas som värmekamera 'i nära anslutning till jaktvapnet' enligt 14 a §."),
    ("DDE", "Digital Detail Enhancement. Lokalt kontrastfilter som förstärker kanter och små temperaturskillnader utan att höja bruset i jämna ytor."),
    ("Detektion", "Att se att något varmt finns. Kräver ungefär 2 pixlar över målets kritiska dimension (Johnsons kriterier). Det avstånd tillverkarna anger som räckvidd."),
    ("Detaljbedömning", "Nordic Aims term för avståndet där du kan bedöma kön, ålder och storlek (motsvarar identifiering). Ungefär en sjättedel av detektionsavståndet."),
    ("Dioptri", "Okularets justering för ditt ögas synfel. Separat från objektivets fokus. Ställs mot menytexten."),
    ("DLC", "Diamond-Like Carbon. Hård beläggning på germaniumlinsens framsida som skyddar mot repor och ger antireflex. Rengörs bara med mikrofiber."),
    ("DRI", "Detection, Recognition, Identification. Branschens tre räckviddsnivåer enligt Johnsons kriterier."),
    ("Emissivitet", "Hur effektivt en yta strålar jämfört med en ideal svart kropp (1,0). Päls, hud, trä och vatten ≈0,95. Blank metall ≈0,1, och ser därför 'kall' ut."),
    ("f-tal", "Brännvidd delat med linsöppningens diameter. f/1.0 är standard, f/0.9 släpper in mer strålning. NETD anges normalt vid f/1.0."),
    ("FFC", "Flat Field Correction. Annat namn för NUC, kalibreringen mot slutaren."),
    ("Fokusfri", "Objektiv med så kort brännvidd (9–10 mm) att allt från några meter är tillräckligt skarpt utan fokusring."),
    ("FOV", "Field of View, synfält. Anges i grader eller som bildbredd i meter på 100 m. Beräknas ur sensorbredd och brännvidd."),
    ("Fusion", "Bildläge i multispektrala kikare där den termiska bilden läggs som färgade konturer ovanpå den digitala bilden."),
    ("Germanium", "Grundämnet som termiska linser görs av. Ogenomskinligt för ögat, genomskinligt för 8–14 µm. Dyrt, mjukt, beläggs med DLC."),
    ("Grundförstoring", "Hur mycket större ett föremål ser ut i okularet än för blotta ögat, utan digital zoom (1,5×, 2,5×, 4×). Säger inget om detaljnivå."),
    ("HSIS", "HIKMICROs slutarfria korrigering. Ersätter NUC-slutaren med en algoritm; inga klick, ingen frusen bild."),
    ("Identifiering", "Att kunna säga vilket djur det är (sugga, galt, kronhind). Kräver ungefär 13 pixlar över målets kritiska dimension för 50 % säkerhet."),
    ("Igenkänning", "Att kunna säga vilken klass (vildsvin, hjortdjur, hund, människa). Ungefär 8 pixlar över målet."),
    ("IP67 / IPX7", "Kapslingsklass. 6 = damm­tät, 7 = tål nedsänkning i 1 m vatten i 30 minuter. X = damm inte testat."),
    ("IR-lampa / IR-belysning", "Osynlig belysning på 850 eller 940 nm som digitala mörkerkikare använder. Behövs inte för värmekamera."),
    ("Ironbow", "Palett som visar hela temperaturintervallet i färg från mörklila (kallt) via rött och orange till gult/vitt (varmt)."),
    ("Johnsons kriterier", "Metod från 1950-talet som anger hur många linjepar över ett mål som krävs för detektion (1), igenkänning (4) och identifiering (6,4) med 50 % sannolikhet."),
    ("Kritisk dimension", "Målets minsta utsträckning som används i räckviddsberäkning, för ett vildsvin från sidan ofta 1,0 m (kroppslängd), från framsidan 0,5 m."),
    ("Kyld värmekamera", "Fotondetektor (InSb, MCT) kyld till ca −200 °C. Extremt känslig, dyr, militär och industriell. Jaktkameror är okylda."),
    ("LRF", "Laser Range Finder, inbyggd laseravståndsmätare. Osynlig laser (905 nm, klass 1), mäter 600–1 000 m med ±1 m."),
    ("LWIR", "Long-Wave Infrared, 8–14 µm. Bandet där föremål vid jordiska temperaturer strålar som mest, och där alla okylda värmekameror arbetar."),
    ("Mikrobolometer", "Sensortypen i alla okylda värmekameror. En matris av tunna membran som värms av strålningen och ändrar resistans. 256×192 till 1280×1024 element."),
    ("mK", "Millikelvin, tusendels grad. Enheten för NETD."),
    ("Multispektral", "Kikare med både termisk sensor och digital dag/natt-sensor med IR-belysning i samma hus. Sök med värme, identifiera med digital bild."),
    ("MWIR", "Mid-Wave Infrared, 3–5 µm. Används av kylda kameror. Bättre i mycket hög luftfuktighet, sämre kontrast vid låga temperaturer."),
    ("NETD", "Noise Equivalent Temperature Difference. Den temperaturskillnad som ger signal lika stor som bruset. Lägre är bättre: &lt;20 mK mycket bra, 20–25 bra, &gt;40 enklare kameror. Jämför bara inom samma mätmetod."),
    ("NIR", "Near Infrared, 0,7–1 µm. Bandet mörkerkikare och IR-lampor arbetar i. Reflekterat ljus, inte egen strålning."),
    ("NUC", "Non-Uniformity Correction. Kalibreringen där en slutare täcker sensorn så att skillnader mellan elementen kan nollställas. Ger klicket och den korta frysningen."),
    ("Okyld värmekamera", "Värmekamera med mikrobolometer som arbetar i rumstemperatur. Alla jakt-, bygg- och de flesta industrikameror."),
    ("Palett", "Färgschema som gråskalan översätts till: white hot, black hot, red hot, ironbow, rainbow. Tillför ingen information, väljer vad ögat lätt ser."),
    ("PiP", "Picture in Picture. Ett förstorat utsnitt visas i en liten ruta överst i bilden samtidigt som hela synfältet behålls."),
    ("Pixelstorlek (pitch)", "Avståndet mellan två elements mittpunkter på sensorn: 17 µm (äldre), 12 µm (standard), 10 µm (nyast). Mindre ger mer detalj per mm brännvidd."),
    ("Radiometrisk", "Kamera som är kalibrerad för att mäta absolut temperatur i varje pixel. Byggnads- och industrikameror; jaktkameror är det normalt inte."),
    ("Red hot", "Palett som visar bilden i gråskala men färgar de varmaste zonerna röda. Bra när marken är varm på sommaren."),
    ("ROIC", "Read-Out Integrated Circuit. Kretsen under mikrobolometern som mäter varje elements resistans och omvandlar till digitala värden."),
    ("Stefan–Boltzmanns lag", "Utstrålad effekt ∝ T⁴. Vid jordiska temperaturer ökar strålningen drygt en procent per grad; det är de procenten kameran mäter."),
    ("SWIR", "Short-Wave Infrared, 1–3 µm. Används i specialkameror; inte i jaktoptik."),
    ("Synfält", "Se FOV."),
    ("Termisk tidskonstant", "Hur snabbt ett mikrobolometerelement värms och svalnar, några millisekunder. Begränsar bildfrekvensen."),
    ("Termografi", "Mätning och avbildning av yttemperaturer med värmekamera, oftast i byggnad och industri."),
    ("Vanadinoxid (VOx)", "Det vanligaste membranmaterialet i bra mikrobolometrar. Hög temperaturkoefficient och lågt brus."),
    ("Värmekikare", "Svensk handelsterm för handhållen värmekamera (termisk monokikare eller dubbelkikare) för jakt och spaning."),
    ("Värmesikte", "Värmekamera byggd som kikarsikte med riktmedel, monterad på vapnet. Regleras av 14 a § jaktförordningen. Se Värmesikte.se."),
    ("White hot", "Standardpalett: varmt visas vitt, kallt svart."),
    ("Wiens förskjutningslag", "Våglängden för strålningstoppen = 2898 µm·K ÷ temperaturen i kelvin. 37 °C ger ≈9,3 µm, mitt i LWIR."),
]


def ordlista() -> dict:
    body = page_hero("Ordlista", "Ordlista: värmekamerans begrepp från AGC till Wien",
                     f"{len(TERMS)} begrepp från datablad, menyer och forum, förklarade kort och utan reklamspråk. Alfabetisk ordning.")
    body += article_open(32)
    body += deflist(TERMS)
    body += f'<p>Saknar du ett begrepp? Skriv till <a href="mailto:{NA_MAIL}">{NA_MAIL}</a> och märk mejlet "{SITE_NAME}". Fördjupning finns på <a href="sa-fungerar-en-varmekamera.html">Så fungerar en värmekamera</a>, <a href="sensor-och-upplosning.html">Sensor och NETD</a> och <a href="optik-och-rackvidd.html">Optik och räckvidd</a>.</p>'
    body += article_close()
    schema = [{
        "@type": "DefinedTermSet", "@id": f"{BASE_URL}/ordlista.html#termset", "name": "Ordlista för värmekamera",
        "inLanguage": "sv-SE",
        "hasDefinedTerm": [{"@type": "DefinedTerm", "name": k, "description": _strip(v), "inDefinedTermSet": f"{BASE_URL}/ordlista.html#termset"} for k, v in TERMS],
    }]
    return {
        "slug": "ordlista.html",
        "title": f"Ordlista värmekamera: {len(TERMS)} begrepp förklarade (NETD, NUC, mikrobolometer, LWIR med flera)",
        "short": "Ordlista",
        "description": f"{len(TERMS)} begrepp om värmekameror förklarade: AGC, DDE, emissivitet, germanium, Johnsons kriterier, LWIR, mikrobolometer, NETD, NUC, palett, pixelstorlek, VOx med flera.",
        "body": body,
        "schema": schema,
    }


def _strip(s: str) -> str:
    import re, html as _h
    return _h.unescape(re.sub(r"<[^>]+>", "", s)).replace("­", "")


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
FAQ = [
    ("Hur fungerar en värmekamera?",
     "Den registrerar den infraröda strålning (8–14 µm) som alla föremål avger på grund av sin temperatur. En germaniumlins fokuserar strålningen på en mikrobolometer, en sensor vars element värms upp och ändrar resistans. Skillnaderna mellan elementen läses av 50 gånger per sekund, korrigeras, kontrastfördelas och visas som gråskala eller färgpalett. Den behöver inget ljus, men ser inte genom glas, vatten eller tät vegetation.",
     'Hela kedjan steg för steg: <a href="sa-fungerar-en-varmekamera.html">Så fungerar en värmekamera</a>.'),
    ("Vad är skillnaden mellan värmekamera och mörkerkikare?",
     "En värmekamera mäter objektets egen värmestrålning och behöver inget ljus; den är bäst på att upptäcka. En mörkerkikare förstärker befintligt ljus eller reflekterat IR-ljus från en lampa och ger en fotoliknande bild med detaljer; den är bäst på att identifiera på närmare håll men ser inget utan ljus och sämre i dimma.",
     'Jämförelse punkt för punkt: <a href="varmekamera-vs-morkerkikare.html">Värmekamera eller mörkerkikare</a>.'),
    ("Får man använda värmekamera på jakt i Sverige?",
     "Handhållen värmekamera för att spana är inte reglerad i jaktförordningen. Monterad på vapnet (värmesikte eller clip-on) får den enligt 14 a § jaktförordningen användas vid jakt efter vildsvin, och termiska sikten bara i öppen terräng eller vid åtelplatser. För andra arter krävs särskilt beslut.",
     'Lagtext och källor: <a href="regler.html">Regler i Sverige</a>.'),
    ("Vad är skillnaden mellan värmekamera och värmekikare?",
     "Ingen teknisk. 'Värmekikare' är den svenska handelstermen för en handhållen värmekamera med okular, byggd för jakt och spaning. 'Värmekamera' används bredare och omfattar också termografikameror för byggnad och industri, drönarkameror och mobiltillsatser.",
     'Olika kameror för olika bruk: <a href="anvandningsomraden.html">Användningsområden</a>.'),
    ("Hur långt ser en värmekamera?",
     "Tillverkarnas räckvidd (till exempel 1 800 m) gäller detektion, alltså att se att något varmt finns, under goda förhållanden. Avståndet där du kan avgöra art är ungefär en fjärdedel av det, och identifiering av individ ungefär en sjättedel. Det styrs av brännvidd och pixelstorlek: 12 µm och 35 mm ger artbestämning kring 350–400 m på vildsvin, 50 mm kring 550 m.",
     'Formler och tabeller: <a href="optik-och-rackvidd.html#dri">Räckvidd (DRI)</a>.'),
    ("Räcker 384 pixlar eller behöver jag 640?",
     "384×288 räcker för skog, åtel och eftersök på normala avstånd. 640×512 ger bredare synfält vid samma objektiv och tål digital zoom till cirka 4× i stället för 2×. Fler pixlar ger inte längre räckvidd; det gör brännvidd och pixelstorlek.",
     'Räkneexempel: <a href="sensor-och-upplosning.html#upplosning">Sensor och upplösning</a>.'),
    ("Vad betyder NETD?",
     "Noise Equivalent Temperature Difference, i millikelvin. Den minsta temperaturskillnad sensorn skiljer från sitt eget brus. Under 20 mK är mycket bra, 20–25 bra, över 40 typiskt för bygg- och mobilkameror. Skillnaden märks mest i dimma, regn och mot blöt mark. Jämför bara tal mätta på samma sätt; 'sensor-NETD' och 'system-NETD' är olika saker.",
     'Fallgropar: <a href="sensor-och-upplosning.html#netd">NETD</a>.'),
    ("Varför ser värmekameran inte genom glas?",
     "Glas är ogenomskinligt för långvågig infraröd strålning (8–14 µm), trots att det släpper igenom synligt ljus. Kameran visar rutans egen yttemperatur och en svag spegelbild. Tornfönstret måste vara öppet. Samma gäller bilrutor, glasögon och plexiglas.",
     'Fler fysikaliska begränsningar: <a href="sa-fungerar-en-varmekamera.html#begransningar">Vad en värmekamera inte kan</a>.'),
    ("Fungerar värmekamera i dimma och regn?",
     "Sämre, men den fungerar. Vatten i luften absorberar strålningen och blöta ytor får nästan lufttemperatur, så kontrasten sjunker och räckvidden halveras ofta. Kameror med låg NETD klarar det bättre. Black hot-palett och manuell kontrast hjälper. Regn på själva linsen ger platt bild; håll linsskyddet på.",
     'Problem P01: <a href="problem.html#p01">Platt bild i regn och dimma</a>.'),
    ("Varför klickar kameran och fryser bilden?",
     "Det är kalibreringen (NUC). En slutare täcker sensorn så att alla element kan nollställas mot samma temperatur, för att ta bort stråk och fläckar. Sätt den på manuell och utlös den själv när inget händer, eller välj en modell med slutarfri korrigering.",
     'Problem P08: <a href="problem.html#p08">Det klickar och bilden fryser</a>.'),
    ("Fungerar en värmekamera på dagen?",
     "Ja. Den mäter temperatur, inte ljus, och fungerar lika bra i solsken. Bilden kan däremot bli platt mitt på dagen i sommarvärme när mark och djur håller liknande temperatur. Rikta aldrig kameran mot solen; det kan ge en permanent fläck i sensorn.",
     ""),
    ("Vad kostar en bra värmekamera för jakt?",
     "Under 10 000 kr får du en kompakt 256- eller 384-kamera för skog och korta håll. 10 000–20 000 kr är allroundklassen med 384/25–35 mm eller 640/25 mm. Över 20 000 kr köper du 640 pixlar, 35–50 mm, låg NETD och laseravståndsmätare för öppna fält. Priser hösten 2026, handhållna modeller.",
     'Modeller per prisklass: <a href="kopguide.html">Köpguide</a>.'),
    ("Behöver jag laseravståndsmätare?",
     "På åtel med kända avstånd sällan. På vak över öppen mark, vid eftersök och när du ska bedöma om det du ser är ett rådjur på 200 m eller en hare på 60, är inbyggd LRF den funktion som gör störst praktisk skillnad, eftersom en termisk bild saknar djup.",
     'Mer: <a href="optik-och-rackvidd.html#lrf">Laseravståndsmätare</a>.'),
    ("Kan jag använda jaktkameran för att hitta köldbryggor i huset?",
     "Ja, du ser köldbryggor, läckage och var golvvärmen går, ofta bättre än med en billig termografikamera tack vare högre upplösning och NETD. Men du får ingen temperaturskala, ingen emissivitetsinställning och ingen rapportfunktion. För en besiktning som ska dokumenteras behövs en radiometrisk termografikamera.",
     'Skillnaderna: <a href="anvandningsomraden.html#bygg">Byggnadstermografi</a>.'),
    ("Hur sköter jag linsen?",
     "Germaniumlinsen har en hård men inte reptålig DLC-beläggning. Blås bort sand och snö först, torka sedan med ren mikrofiberduk, aldrig papper, handske eller tröja. Imma och rimfrost: låt kameran acklimatisera i ytterfickan och håll linsskyddet på tills du behöver bilden.",
     'Problem P04: <a href="problem.html#p04">Immig eller frusen lins</a>.'),
    ("Vem står bakom den här sajten?",
     f"{SITE_NAME} drivs av {NA_NAME} (org.nr {NA_ORGNR}), en svensk webbutik för jakt- och skytteoptik. Produktlänkar går till nordicaim.se. Vi är inte neutrala i valet av vilka produkter som visas, men tekniken, fysiken och reglerna beskriver vi som de är, med källor.",
     'Mer: <a href="om.html">Om oss</a>.'),
]


def faq() -> dict:
    body = page_hero("Frågor och svar", "Vanliga frågor om värmekameror", "Korta svar. Följ länkarna för fördjupning.")
    body += '<section style="max-width:820px;margin:0 auto;padding:48px 24px 96px;display:flex;flex-direction:column;gap:12px">'
    for q, a, more in FAQ:
        extra = f'<p style="font-size:15px;color:var(--text-muted)">{more}</p>' if more else ""
        body += faq_details(q, f"<p>{a}</p>{extra}")
    body += (f'<p style="margin-top:20px;font-size:16px">Hittar du inte svaret? {NA_NAME} svarar på produktfrågor på <a href="mailto:{NA_MAIL}">{NA_MAIL}</a> eller {NA_TEL}, '
             f'och har en egen {nalink("/pages/vanliga-fragor", "FAQ")} och {nalink("/pages/kopguide-termisk-optik", "köpguide för termisk optik")}. '
             f'Frågor om termiska sikten besvaras på {ext(SISTER + "/faq.html", "Värmesikte.se")}.</p>')
    body += "</section>"
    schema = [{"@type": "FAQPage", "@id": f"{BASE_URL}/faq.html#faq",
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in FAQ]}]
    return {
        "slug": "faq.html",
        "title": f"Vanliga frågor om värmekamera: {len(FAQ)} korta svar",
        "short": "Frågor och svar",
        "description": "Hur fungerar en värmekamera, hur långt ser den, får man jaga med den, 384 eller 640, vad är NETD, varför ser den inte genom glas, vad kostar en bra kamera. Korta svar med länkar till fördjupning.",
        "body": body,
        "schema": schema,
        "article": False,
    }


# ---------------------------------------------------------------------------
# OM OSS
# ---------------------------------------------------------------------------
def om() -> dict:
    body = page_hero("Om oss", f"Vem som står bakom {SITE_NAME}")
    body += article_open(32)
    body += f'''
      <section style="display:flex;flex-direction:column;gap:14px">
        <h2 style="font-size:26px;font-weight:800">Vad sajten är</h2>
        <p>{SITE_NAME} är en teknisk guide till värmekameror, med tyngdpunkt på handhållna kameror för jakt och spaning i Sverige. Vi förklarar fysiken bakom tekniken, vad siffrorna i databladen betyder och hur de översätts till vad du ser i skogen. Vi läser tillverkarnas dokumentation, manualer, forskningsöversikter och svenska jaktforum, och väver in erfarenheter från Nordic Aims kunder och personal.</p>
        <p>Vi skriver inte "bäst i test"-listor med poäng. Vi beskriver vad en modell är byggd för och var den har sina begränsningar, och vi visar formlerna så att du kan räkna själv.</p>
      </section>
      <section style="display:flex;flex-direction:column;gap:14px;background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:28px">
        <h2 style="font-size:22px">En sajt från Nordic Aim</h2>
        <p style="font-size:16px">{SITE_NAME} ägs och drivs av {ext(na("/"), NA_NAME)} (org.nr {NA_ORGNR}), en svensk webbutik för jakt- och skytteoptik som skickar från Sverige. När vi länkar till produkter går länkarna till nordicaim.se. Det påverkar vilka produkter vi visar med bild och länk: vi visar det vi säljer. Det påverkar inte hur vi beskriver tekniken, fysiken, reglerna eller problemen, och vi skriver ut begränsningar också hos produkter vi säljer.</p>
        <p style="font-size:16px">Köper du något via en länk härifrån hanteras köp, leverans, öppet köp och support av Nordic Aim enligt deras villkor. Vi driver också {ext(SISTER + "/", "Värmesikte.se")}, en motsvarande guide om termiska sikten.</p>
        <p style="font-size:16px">Frågor om en produkt, montage eller leverans: <a href="mailto:{NA_MAIL}">{NA_MAIL}</a>, {NA_TEL}. Synpunkter på innehållet här: samma adress, märk mejlet "{SITE_NAME}". Hittar du ett sakfel rättar vi det och noterar ändringen.</p>
      </section>
      <section style="display:flex;flex-direction:column;gap:14px">
        <h2 style="font-size:26px;font-weight:800">Hur vi arbetar med källor</h2>
        {ul([
            "Fysikaliska påståenden bygger på etablerad strålningsfysik (Planck, Wien, Stefan–Boltzmann) och på publicerade översikter av mikrobolometerteknik. Formler visas så att du kan räkna själv.",
            "Regler hänvisas till författningstext och myndighet, med länk och datum för kontroll.",
            "Problem i fält kommer från forum, manualer och kunder. Vi skriver inte 'de flesta' eller 'vanligast' utan data.",
            "Tekniska påståenden om en modell kontrolleras mot aktuellt produktblad. Tillverkarens 'upp till' är inte ett uppmätt värde, och det skriver vi.",
            "Vi hittar inte på tester eller kundcitat. Saknar vi underlag säger vi det.",
            "Varje sida har ett datum för senaste uppdatering. Priser och sortiment ändras; kontrollera alltid hos Nordic Aim.",
        ])}
      </section>
      <section style="display:flex;flex-direction:column;gap:14px">
        <h2 style="font-size:26px;font-weight:800">Länka gärna</h2>
        <p>Sajten får citeras och länkas fritt med källangivelse. Diagram och tabeller får återanvändas i icke-kommersiella sammanhang (jaktlag, utbildning, forum) om {SITE_NAME} anges som källa. För annan användning, hör av dig.</p>
      </section>'''
    body += article_close()
    return {
        "slug": "om.html",
        "title": f"Om {SITE_NAME} och Nordic Aim AB",
        "short": "Om oss",
        "description": f"Vem som står bakom {SITE_NAME}: Nordic Aim AB, svensk återförsäljare av termisk optik. Hur vi arbetar med källor, vad länkarna betyder och hur du kontaktar oss.",
        "body": body,
        "article": False,
    }


# ---------------------------------------------------------------------------
# INTEGRITET
# ---------------------------------------------------------------------------
def integritet() -> dict:
    body = page_hero("Integritet", "Integritet och cookies")
    body += article_open(24)
    body += f'''
      <p>{SITE_NAME} är en statisk informationssajt. Vi sätter inga cookies, använder inga analysverktyg och samlar inte in personuppgifter på sajten. Webbhotellet lagrar vanliga serverloggar (IP-adress, tidpunkt, hämtad sida) under begränsad tid för drift och säkerhet.</p>
      <p>Länkar till nordicaim.se innehåller parametern <code>ref={__import__("build").REF}</code> så att Nordic Aim kan se att besöket kom härifrån. När du klickar på en sådan länk gäller {nalink("/policies/privacy-policy", "Nordic Aims integritetspolicy")}. Produktbilder hämtas från Nordic Aims bildserver (Shopify CDN), som då ser din IP-adress.</p>
      <p>Personuppgiftsansvarig för sajten är {NA_NAME}, org.nr {NA_ORGNR}, <a href="mailto:{NA_MAIL}">{NA_MAIL}</a>.</p>'''
    body += article_close()
    return {
        "slug": "integritet.html",
        "title": "Integritet och cookies",
        "short": "Integritet",
        "description": f"Integritetsinformation för {SITE_NAME}: inga cookies, inga analysverktyg, serverloggar hos webbhotellet, ref-parameter på länkar till Nordic Aim.",
        "body": body,
        "article": False,
        "noindex": True,
    }


def notfound() -> dict:
    body = page_hero("404", "Sidan finns inte", "Adressen kan vara felstavad eller sidan flyttad.")
    body += article_open(16)
    body += f'<p>Börja om på <a href="index.html">startsidan</a>, eller gå direkt till <a href="sa-fungerar-en-varmekamera.html">Så fungerar en värmekamera</a>, <a href="kopguide.html">Köpguiden</a> eller <a href="faq.html">Frågor och svar</a>.</p>'
    body += article_close()
    return {"slug": "404.html", "title": "Sidan finns inte", "short": "404", "description": "Sidan finns inte.", "body": body, "article": False, "noindex": True}


def pages() -> list[dict]:
    return [problem(), regler(), ordlista(), faq(), om(), integritet(), notfound()]
