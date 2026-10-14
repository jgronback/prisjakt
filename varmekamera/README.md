# Värmekamera – guidesajt (systersajt till värmesikte.se)

Statisk HTML-sajt om värmekameror, byggd på samma mall och design-tokens som värmesikte.se.
Syfte: ranka på "värmekamera" och närliggande sökningar, länka till Nordic Aims värmekikare.

## Domänläge (kontrollerat 14 okt 2026)

| Domän | Status | Kommentar |
|---|---|---|
| varmekamera.se | **Upptagen** | Live WordPress-sajt, Micro-Epsilon Sensotest AB (industriella IR-kameror) |
| värmekamera.se (xn--vrmekamera-q5a.se) | **Upptagen** | Registrerad, pekar på 109.235.174.3 |
| varmekameror.se | Ledig | Används som platshållare i `build.py` (DOMAIN) |
| varmekamera.com | Ledig | |
| termiskkamera.se | Ledig | |
| varmekameraguide.se / varmekamera-guide.se | Ledig | |
| varmekamerajakt.se | Ledig (ASCII) | OBS: IDN-varianten värmekamerajakt.se är en befintlig konkurrentsajt |
| varmekamera.nu | Okänd | Kunde inte kontrolleras från den här miljön |

Tillgänglighet kontrollerad via Vercels registrar-API och DNS. Verifiera hos registraren innan köp.

Sajtens **namn** är "Värmekamera" oavsett domän (logotyp, menyer, titlar, schema).

## Bygga

```
python3 build.py        # genererar dist/
python3 validate.py     # kontrollerar HTML, interna länkar, ankare, JSON-LD
python3 validate.py --external   # kontrollerar även alla externa länkar (tar ~1 min)
```

Kräver bara Python 3 (standardbibliotek).

## Byta domän

Ändra `DOMAIN` i `build.py` och kör `python3 build.py`. Canonical, og:url, sitemap, robots,
JSON-LD, llms.txt och .htaccess följer med automatiskt.

## Publicera (Strato eller annat Apache-hotell)

1. Ladda upp **hela innehållet i `dist/`** (inklusive `.htaccess`, `css/`, `fonts/`) till webbroten.
2. Aktivera SSL för domänen hos hotellet.
3. `.htaccess` tvingar https + www och pekar 404 till `404.html`.
4. Anmäl `https://<domän>/sitemap.xml` i Google Search Console och Bing Webmaster Tools.
5. Lägg till domänen som egendom i Search Console och verifiera (DNS-TXT eller HTML-tagg i `render()`).

## Struktur

```
build.py            generator, layout, hjälpfunktioner, konfiguration
validate.py         kontroller
src/style.base.css  Nordic Aims design-tokens (identiska med värmesikte.se)
src/diagrams.py     inline-SVG (signalkedja, spektrum, mikrobolometer, synfält)
src/pages_teknik.py Hem, Så fungerar det, Sensor, Optik/räckvidd
src/pages_jakt.py   Jakt, Köpguide, Värmekamera vs mörkerkikare, Användningsområden
src/pages_stod.py   Problem, Regler, Ordlista, FAQ, Om oss, Integritet, 404
dist/               färdig sajt att ladda upp
INLANKAR.md         plan för inlänkar
```

## SEO/GEO-åtgärder som finns inbyggda

- En kanonisk URL per sida, www + https via .htaccess
- Title/description per sida, OG-taggar, Twitter card
- JSON-LD: WebSite, Organization (Nordic Aim AB med org.nr), BreadcrumbList, TechArticle per sida,
  FAQPage (16 frågor), DefinedTermSet (ordlista, 60 termer)
- "Kort svar"-block överst på varje guidesida (för utdrag i AI-sök och featured snippets)
- Tabeller med uträknade värden (synfält, pixelfotavtryck, DRI) i stället för bara prosa
- llms.txt, sitemap.xml, robots.txt
- Senast uppdaterad + författarrad på varje sida, tydlig ägardisclosure (Nordic Aim AB) i footer och Om oss
- Alla länkar till Nordic Aim har `?ref=varmekamera`; produktlänkar har `rel="sponsored"`
- Självhostade typsnitt med preload, ingen JavaScript, inga cookies

## Produktdata

Produktkort (namn, bild, specar) är hämtade från nordicaim.se/collections/varmekikare/products.json
den 14 okt 2026. Priser visas inte på sajten (de ändras), bara "Se hos Nordic Aim".
