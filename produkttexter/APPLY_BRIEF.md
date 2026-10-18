# Uppdrag: skicka färdiga uppdateringspaket till Shopify

Jonas har godkänt att produkttexterna läggs in, och han godkänner varje anrop i sin klient.
Paketen är färdigbyggda och validerade i `/home/user/prisjakt/produkttexter/bulk/chunks/cXX.json`.
Varje fil innehåller `query` (en GraphQL-mutation med flera aliasade productUpdate) och `variables`.

## Gör så här, för varje paket du har fått, ett i taget
1. Ladda verktyget: ToolSearch `select:mcp__Shopify__graphql_mutation`.
2. Läs filen (`cat` eller Read). Skicka `query` och `variables` EXAKT som de står i filen till
   `mcp__Shopify__graphql_mutation`. Ändra ingenting: inga ord, inga tecken, ingen formatering.
   Om filen är för stor för ett anrop: dela variablerna i två halvor med motsvarande del av mutationen
   (alias och variabeldeklarationer u0..uN / $p0..$pN), men ändra aldrig innehållet i ett variabelvärde.
3. Kontrollera svaret: alla `uN.userErrors` ska vara tomma. Notera varje fel med paket, alias, produkt-id och felmeddelande.
4. Skriv logg till `/home/user/prisjakt/produkttexter/applied/chunks_<ditt namn>.json`:
   `[{"chunk":"c00","ok":true/false,"errors":[{"alias":"u3","id":"...","message":"..."}]}]`
5. Om ett anrop nekas av Jonas eller av en spärr: försök inte runt det, logga och gå vidare till nästa paket.

## Gör inte
- Inga andra mutationer än de i paketen.
- Ändra inte i paketfilerna.
- Läs inte tillbaka produkter, huvudsessionen gör en fullständig kontroll efteråt.

## Rapport
Kort: vilka paket som gick igenom, antal produkter, alla userErrors ordagrant.
