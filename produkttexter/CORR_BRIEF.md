# Uppdrag: rätta felaktiga produktdata på nordicaim.se

Jonas har bett: "Uppdatera alla felaktigheter till korrekta värden." Du får en del av listan i
`/home/user/prisjakt/produkttexter/GRANSKA.md` (avsnitten anges i ditt uppdrag). Mappen är
`/home/user/prisjakt/produkttexter/`.

## Läs först
1. Skillen `/root/.claude/skills/synced/ac475608-598e-43d1-bbc9-9ef4f0777037_b0f96d8f-7d58-478e-80fb-5c984414f24c/nordicaim-produkttext/SKILL.md`: VIKTIGASTE PRINCIPEN, TILLÅTNA KÄLLOR, AVSTÅND (artbestämning/detaljbedömning), ABSOLUTA REGLER, TERMINOLOGI. Samt `references/metafalt.md` (format) och `references/kallforbehall.md` (kända källfel per märke).
2. Dina avsnitt i GRANSKA.md.
3. För varje produkt: aktuell text = förslaget i `proposals/bXX.json` om `descriptionHtml` inte är null, annars originalet i `backup_2026-10-18.json`. Bygg alltid vidare på den versionen, så att förbättringarna från genomgången inte går förlorade.

## Hur du avgör vad som är rätt
- Sanningen hämtas från tillverkarens officiella produktsida eller datablad/manual (WebSearch + WebFetch). Officiell distributör godtas i andra hand. Aldrig återförsäljare, Prisjakt, forum.
- Spara URL:en för varje värde du ändrar.
- Hittar du inte en officiell källa: ändra INTE värdet. Lägg punkten under "ej verifierat" i rapporten.
- Rena språk- och formfel kräver ingen källa: stavfel, "binokulär" → dubbelkikare, "rödpunktssikte" → rödpunktsikte, "hög kvalitet" o.d. i Detta ingår, prisbelopp i text/FAQ ("1 000 kronor") → strykes eller "till lägre pris", ChatGPT-omslag (`<article>`, `<div data-...>`, tomma `<h1>`), platshållare som "[X cm]", "Höjd: 0 cm", "Vikt: 0 g", "uppgift saknas" (raden tas bort om rätt värde inte kan verifieras), ihopklistrad text utan mellanslag, metafältsformat (`netd` ska ha ≤, `sensor` litet x).
- Avslutningar som tidigare var låsta och innehåller AI-slop: skriv om enligt BRIEF.md (siffra ur texten, 1–2 relativa syskonlänkar, ingen floskel).

## Vad du får ändra
- `descriptionHtml`: hela texten inklusive Teknisk specifikation och Detta ingår, men bara de rader som är fel. Detta ingår ändras bara mot officiell packlista.
- `faq` (custom.faq, JSON-array av {"q","a"}): rätta fel svar, förbjudna ord och prisbelopp.
- Metafält: `custom.sensorupplosning`, `netd`, `pixelstorlek`, `objektiv`, `forstoring`, `detektionsrackvidd`, `laseravstandsmatare` (true/false), `artbestamning`, `detaljbedomning` (enligt tabellen i skillen), `vikt` m.fl. Format enligt metafalt.md.
- `title`: om titeln är verifierat fel (fel brännvidd, fel upplösning, "Dual Use", saknat märke).
- `handle`: bara om handlen innehåller ett faktafel (t.ex. "1074x768", "256x162", "15 mm" när det är 9 mm). Sätt då `"redirect": true`, så Shopify skapar en omdirigering från den gamla adressen.

## Vad du inte får ändra
- Pris, lager, inventoryPolicy, kanaler, bilder, taggar, produkttyp.
- Dubbletter: rapportera, ta inte bort.
- Inga mutationer i Shopify. Du skriver bara en fil. Huvudsessionen lägger in allt med en massuppdatering.
- Läs gärna produkter i Shopify (graphql_query) om du behöver aktuell FAQ eller metafält, men aldrig mutation.

## Utdata
`corrections/<ditt namn>.json`: lista av
```
{"id": "gid://shopify/Product/...", "handle": "nuvarande-handle",
 "descriptionHtml": "<hela nya HTML:en>" | null,
 "faq": [{"q":"...","a":"..."}] | null,
 "metafields": {"netd": "≤20 mK", "sensorupplosning": "640x512"} | null,
 "title": "..." | null, "new_handle": "..." | null, "redirect": true | false,
 "sources": ["https://..."],
 "changes": ["kort beskrivning per ändring: fält, gammalt → nytt, källa"]}
```
Skriv filen med ett Python-skript (json.dump, ensure_ascii=False). Använd hjälpfiler i `scratchpad/<ditt namn>/`.

Kör `python3 validate_corr.py corrections/<ditt namn>.json` tills 0 FAIL.

## Rapport (kort, svenska)
- Rättat: antal produkter, och per produkt en rad: vad, gammalt → nytt, källa.
- Ej verifierat (lämnat orört): produkt och varför.
- Kräver Jonas beslut: priser, dubbletter, packlistor utan källa.
