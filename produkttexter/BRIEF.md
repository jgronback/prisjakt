# Uppdrag: förbättra befintliga produkttexter på nordicaim.se

Du arbetar med en batch produkter i Shopify-butiken nordicaim.se (Nordic Aim AB, jakt- och skytteoptik).
Mappen är `/home/user/prisjakt/produkttexter/`. Läs hela denna fil innan du börjar.

## Läs först (obligatoriskt)

1. Skillen för produkttexter: `/root/.claude/skills/synced/ac475608-598e-43d1-bbc9-9ef4f0777037_b0f96d8f-7d58-478e-80fb-5c984414f24c/nordicaim-produkttext/SKILL.md`. Avsnitten TON OCH STIL, TEXTEN FÅR INTE LÅTA AI-SKRIVEN, KUNDNYTTA FÖRST, ABSOLUTA REGLER, NORDIC AIM-SPECIFIKA HÅRDA REGLER och TERMINOLOGI gäller fullt ut.
2. Din batchfil `batches/bXX.json` (nummer anges i ditt uppdrag). Varje rad har `id`, `handle`, nuvarande `descriptionHtml`, `short_pitch`, `short_pitch_metafield_id`, metafält och pris.
3. `catalog_index.json` när du letar syskonmodeller att länka till (alla 1 047 aktiva produkter: handle, titel, sensor, objektiv, pixelstorlek, LRF, pris, artbestämning).

## Vad du ska göra per produkt

Ändra så lite som möjligt för att uppnå detta. Texterna är ofta redan bra. **Riktade ändringar, inte omskrivningar.**

1. **Ta bort AI-slop.** Skriv om bara de meningar som innehåller: "oavsett om", "inte bara ... utan också", "perfekt för/perfekt val", "enkel att använda/användarvänlig", "designad för att", "robust konstruktion", "fantastisk/otrolig/imponerande", "hög kvalitet", "ett tryggt val/att lita på", "sömlös", "helhetslösning/komplett paket", "avancerad/modern teknik", "X-upplevelse", "nästa nivå", "full kontroll", em dash (—), "rödpunktssikte" (ska vara rödpunktsikte), "binokulär" (dubbelkikare), "termik", "dual use", "rigg", "öppet köp", leverantörsnamn (Astro Sweden, Focus Nordic, Armtac), retoriska öppningsfrågor. Ersätt med det konkreta: siffran, funktionen, användningsfallet som redan står i texten. Kan meningen inte bli konkret: stryk den.
2. **Avslutande säljtext** (sista stycket efter "Detta ingår", eller sista stycket om strukturen saknas): gör den mer säljande, ungefär 20–30 % starkare, utan att bli skrikig. Den ska: (a) sammanfatta den viktigaste verkliga nyttan med en siffra som redan finns i texten, (b) gärna säga vem produkten passar och när en syskonmodell passar bättre, med länk, (c) högst en kort trygghetsdel ("Fraktfritt inom Sverige", "vi hjälper dig välja") och aldrig som enda innehåll. Godkänd ton: "Det ljusstarka 50 mm-objektivet gör att du ser viltet längre in i skymningen." Bannlyst: "ett sikte att lita på", "ta nästa steg", tomma utrop.
3. **Short pitch** (`short_pitch`): gör befintlig pitch 20–30 % mer säljande. Öppna med kundens utfall eller situation, inte med en specifikationslista. Behåll de verkliga specarna. 110–170 tecken (80 tecken går för små tillbehör). En mening eller två korta. Ingen radbrytning, ingen em dash. Variera öppningarna inom serien.
   Exempel. Före: "640-sensorns breda överblick i fickformat: NETD ≤25 mK, detektion upp till 1300 m och skarp OLED, i ett IP67-hus på 320 g." Efter: "Sveper av åkerkanten på färre drag: 640-sensor, NETD ≤25 mK och detektion upp till 1300 m i ett IP67-hus på 320 g som ryms i fickan."
   Saknas pitch helt och produkttexten har minst 400 tecken: skriv en ny med fakta ur texten. Saknas pitch och texten är kortare: lämna `short_pitch` som null.
4. **Interna länkar** (där det hjälper kunden välja): länka till en syskonmodell (annat objektiv, med/utan LRF, 384/640, föregångare/efterföljare) eller till serie-/kategorikollektion eller en relevant guide. Max 3 länkar totalt i texten, alltid relativa: `/products/<handle>`, `/collections/<handle>`, `/blogs/nyheter/<handle>`. Bara mål som finns i `link_targets.json`. Absoluta länkar till `https://nordicaim.se/...` i befintlig text ska göras relativa. Externa länkar ska bort. Anger du en skillnad mot syskonmodellen ska siffran komma ur `catalog_index.json` för den modellen (t.ex. artbestämning 280 m mot 400 m), aldrig gissas.

## Rör inte

- Avsnitten **Teknisk specifikation** och **Detta ingår**: byte för byte oförändrade.
- Inga nya tekniska siffror. Varje siffra i ny text måste redan finnas i produktens text, pitch, FAQ, metafält, titel eller hos en länkad syskonprodukt. Validatorn kontrollerar detta.
- Titel, pris, FAQ, SEO-fält, taggar, lager, `inventoryPolicy`, kanaler, bilder.
- Produkter med text under 400 tecken: skriv inte ny produkttext (det kräver verifierade data). Rätta bara förbjudna mönster om de finns, och förbättra pitch om den finns. Lista dem i din rapport.
- Är en text redan bra och har en bra avslutning och pitch: sätt `descriptionHtml` och/eller `short_pitch` till null. Att lämna orört är ett giltigt utfall.
- HTML-strukturen: behåll `<p>`, `<strong>`, `<br>`, `•`-listor som de är.


## Facit från piloten (läs innan du skriver)

`proposals/b00.json` är godkänd av huvudsessionen och är facit för ton och nivå: titta på 3 av avslutningarna och pitcharna där innan du börjar. Kännetecken:
- Pitchen öppnar med kundens situation ("Slipp gissa håll i skymningen:", "Sveper av åkerkanten på färre drag:") och följer med 2–4 riktiga specar.
- Avslutningen har en verklig siffra (ofta artbestämning) och 1–2 syskonlänkar med skillnaden i siffror, plus högst en kort trygghetsmening som inte står likadant på alla produkter.
- Gamla standardmeningen "Fraktfritt inom Sverige, och vi hjälper dig gärna välja rätt modell" ska inte stå kvar ordagrant på varje produkt. Variera eller stryk.
- Priser anges aldrig som belopp i text, bara "till lägre pris" o.d.

## Tillbehör och små produkter

Fästen, ringar, adaptrar, batterier, väskor och andra tillbehör: lätt hand. Rätta förbjudna mönster, gör pitchen tydligare om vad den passar till (modell, footprint, mått som redan står i texten), och länka gärna till den produkt eller kollektion tillbehöret hör till. Lägg inte tid på syskonresonemang som för sikten.

## Kända datakonflikter

Hittar du konflikter mellan text, specifikation, metafält och FAQ (som på A650P i piloten): rör dem inte, lista dem i rapporten.

## Arbetsgång

1. Skriv förslagen till `proposals/bXX.json`: en lista av
   `{"id": "...", "handle": "...", "descriptionHtml": "<hela nya HTML:en>" eller null, "short_pitch": "..." eller null, "change_note": "kort: vad du ändrade"}`.
   Ta med alla produkter i batchen, även de du lämnar orörda (båda fälten null).
   Skriv filen med ett Python-skript (json.dump, ensure_ascii=False) så att citattecken och å/ä/ö blir rätt.
2. Kör `python3 validate.py proposals/bXX.json`. Rätta varje FAIL och kör igen tills 0 FAIL. Strunta inte i en FAIL genom att sätta fältet till null om produkten faktiskt behöver rättas, försök först rätta. "OK*"-varningar är tillåtna men titta på dem.
3. Läs dina ändringar en gång till med strykningstestet ur skillen: överlever varje ny mening (siffra, verifierat faktum eller konkret användningsfall)? Låter avslutningarna i serien likadant? Variera.
4. **Applicera** (hoppa över om ditt uppdrag säger "endast förslag"). Ladda Shopify-verktygen med ToolSearch (`select:mcp__Shopify__graphql_mutation,mcp__Shopify__graphql_query`). För varje produkt med ändring:
   - Text: `mutation($p: ProductUpdateInput!) { productUpdate(product: $p) { product { id } userErrors { field message } } }` med `{"p": {"id": "<id>", "descriptionHtml": "<ny HTML>"}}`.
   - Pitch: samla upp till 25 per anrop: `mutation($m: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $m) { metafields { id } userErrors { field message } } }` med `{"ownerId": "<produkt-id>", "namespace": "custom", "key": "short_pitch", "type": "multi_line_text_field", "value": "<pitch>"}`.
   - Läs tillbaka varje ändrad produkt (`product(id:) { descriptionHtml metafield(namespace:"custom", key:"short_pitch"){value} }`, gärna flera via `nodes(ids: [...])`) och jämför textinnehållet (blanktecken normaliserade) med ditt förslag.
   - Skriv logg till `applied/bXX.json`: `[{"id","handle","desc_applied": true/false, "pitch_applied": true/false, "readback_ok": true/false, "error": null eller text}]`.
5. Rör inga andra produkter än de i din batch. Gör inga andra mutationer än de två ovan.

## Rapport tillbaka (kort, på svenska)

- Antal produkter: text ändrad / pitch ändrad / ny pitch / orörda / applicerade / återläsning OK.
- Produkter med text under 400 tecken (handles), så de kan få nya texter senare.
- Allt du var osäker på eller som borde granskas av en människa.
