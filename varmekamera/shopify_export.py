#!/usr/bin/env python3
"""Exporterar sajtens sidor till Shopify-blogginlägg (JSON per artikel i shopify/).

Körs efter build.py. Tar <main>-innehållet, plockar bort sajtens hero-rubrik och
"senast uppdaterad"-rad, skriver om interna länkar till /blogs/nyheter/<handle> och
länkar till nordicaim.se till relativa länkar utan ref-parameter.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "src"))
DIST = os.path.join(HERE, "dist")
OUT = os.path.join(HERE, "shopify")
BLOG_ID = "gid://shopify/Blog/117794898260"   # Nyheter
CDN = "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/"

# slug -> (handle, titel, taggar, bild, alt)
ARTICLES = {
    "sa-fungerar-en-varmekamera.html": ("sa-fungerar-en-varmekamera",
        "Så fungerar en värmekamera, steg för steg", ["Guide", "Värmekamera", "Värmekikare", "Teknik"],
        CDN + "938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791", "Pulsar Telos XP50 LRF värmekamera, så fungerar en värmekamera"),
    "sensor-och-upplosning.html": ("varmekamera-sensor-upplosning-netd",
        "Värmekamera: sensor, upplösning, pixelstorlek och NETD förklarat", ["Guide", "Värmekamera", "NETD", "Teknik"],
        None, None),
    "optik-och-rackvidd.html": ("varmekamera-optik-synfalt-rackvidd",
        "Värmekamera: brännvidd, synfält och räckvidd i meter", ["Guide", "Värmekamera", "Teknik"],
        None, None),
    "varmekamera-vs-morkerkikare.html": ("varmekamera-eller-morkerkikare",
        "Värmekamera eller mörkerkikare: vad ser mest, och när?", ["Guide", "Värmekamera", "Mörkerkikare", "Köpguide"],
        CDN + "800q-HE25L_202.0_1.png?v=1769171478", "HIKMICRO Habrok 4K HE25L 2.0 multispektral kikare, värmekamera eller mörkerkikare"),
    "varmekamera-for-jakt.html": ("varmekamera-for-jakt",
        "Värmekamera för jakt: spaning, åtel, eftersök och inventering", ["Guide", "Värmekamera", "Värmekikare", "Vildsvin", "Eftersök"],
        CDN + "954682-0.jpg?v=1789068911", "PixFra Arc Pro A650P LRF värmekikare, värmekamera för jakt"),
    "kopguide.html": ("kopguide-varmekamera-jakt-2026",
        "Köpguide: välja värmekamera för jakt 2026", ["Köpguide", "Värmekamera", "Värmekikare"],
        CDN + "PIX-PFI-M425___Pixfra-Mile-2-M425-Thermal-Imaging-Monocular.png?v=1766943659", "PixFra Mile M2 värmekikare, köpguide värmekamera för jakt 2026"),
    "problem.html": ("varmekamera-problem-och-losningar",
        "Värmekamera: 13 vanliga problem och vad som hjälper", ["Guide", "Värmekamera", "Värmekikare", "Felsökning"],
        None, None),
    "regler.html": ("regler-varmekamera-jakt",
        "Får man använda värmekamera på jakt i Sverige? Regler med källa", ["Regler", "Värmekamera", "Värmesikte", "Vildsvin"],
        None, None),
    "ordlista.html": ("ordlista-varmekamera",
        "Ordlista: värmekamerans begrepp från AGC till Wien", ["Guide", "Värmekamera", "Ordlista"],
        None, None),
    "anvandningsomraden.html": ("varmekamera-anvandningsomraden",
        "Vad används en värmekamera till? Jakt, räddning, byggnad, industri och drönare", ["Guide", "Värmekamera"],
        None, None),
    "faq.html": ("vanliga-fragor-varmekamera",
        "Vanliga frågor om värmekameror: 15 korta svar", ["FAQ", "Värmekamera", "Värmekikare"],
        None, None),
}
LINKMAP = {s: f"/blogs/nyheter/{h}" for s, (h, *_r) in ARTICLES.items()}
LINKMAP.update({
    "index.html": "/blogs/nyheter/sa-fungerar-en-varmekamera",
    "om.html": "/pages/om-oss",
    "integritet.html": "/policies/privacy-policy",
})

# Formuleringar som förutsätter en fristående sajt -> så som Nordic Aim själv skriver
REPL = [
    ("Se hos Nordic Aim", "Se produkten"),
    ("hos Nordic Aim AB", "hos oss"),
    ("hos Nordic Aim", "hos oss"),
    ("Nordic Aim AB har en egen genomgång", "Vi har en egen genomgång"),
    ("Nordic Aim AB räknar på samma sätt", "Vi räknar på samma sätt"),
    ("Nordic Aim AB skriver på varje produktsida", "Vi skriver på varje produktsida"),
    ("Nordic Aim AB uppdaterar sin genomgång", "Vi uppdaterar vår genomgång"),
    ("Nordic Aim AB svarar på produktfrågor", "Vi svarar på produktfrågor"),
    ("Nordic Aim ger personlig rekommendation", "Vi ger personlig rekommendation"),
    ("Nordic Aim förklarar sin räkning", "Vi förklarar räkningen"),
    ("Nordic Aim jämför de två siktevarianterna", "Vi jämför de två siktevarianterna"),
    ("Nordic Aims egen <a", "Vår <a"),
    ("Nordic Aims produktsidor", "våra produktsidor"),
    ("Nordic Aims term för", "Vår term för"),
    ("Nordic Aims kunder", "våra kunder"),
    ("av Nordic Aims kunder", "av våra kunder"),
    ("Nordic Aims guider", "våra guider"),
    ("Fördjupning hos oss:", "Fördjupning:"),
    ("Metod steg för steg: ", "Metod steg för steg: "),
    ("på sidan <a", "i <a"),
    ("vår systersajt", "vår sajt"),
    ("på systersajten", "på"),
    ("Värmekamera skriver i första hand om", "Den här guiden handlar i första hand om"),
    ("eftersom det är vad Nordic Aim AB säljer och kan", "eftersom det är vad vi säljer och kan"),
    ("Hittar du inte svaret? Vi svarar", "Hittar du inte svaret? Vi svarar"),
    ("och har en egen <a", "och vi har en <a"),
    ("Saknar du ett begrepp? Skriv till", "Saknar du ett begrepp? Skriv till"),
    ('och märk mejlet "Värmekamera"', "och skriv Ordlista i ämnesraden"),
    ("Osäker på valet? Vi ger personlig rekommendation utifrån din mark, din jakt och din budget, utan köpkrav.",
     "Osäker på valet? Vi ger personlig rekommendation utifrån din mark, din jakt och din budget, utan köpkrav."),
    ("var(--text-faint)", "#7E8A91"),
    ("var(--blaze-50)", "#FCEDE6"),
]


def convert(slug: str) -> dict:
    handle, title, tags, image, alt = ARTICLES[slug]
    src = open(os.path.join(DIST, slug), encoding="utf-8").read()
    desc = re.search(r'<meta name="description" content="([^"]*)"', src).group(1)
    main = re.search(r'<main id="main"[^>]*>(.*?)</main>', src, re.S).group(1)

    # hero: ta bort kicker + h1, behåll ingress och ankarchips
    main = re.sub(r'<span style="font-family:var\(--font-mono\);font-size:12px;letter-spacing:\.14em;[^>]*>[^<]*</span>\s*<h1[^>]*>.*?</h1>', '', main, count=1, flags=re.S)
    # hero-sektionens vita bakgrund och padding blir ett vanligt block
    main = main.replace('<section style="background:#fff;border-bottom:1px solid var(--mist-200)">\n      <div style="max-width:820px;margin:0 auto;padding:72px 24px 48px;display:flex;flex-direction:column;gap:16px">',
                        '<section style="margin:0 0 24px"><div style="display:flex;flex-direction:column;gap:16px">', 1)
    main = main.replace('<section style="background:#fff;border-bottom:1px solid var(--mist-200)">\n      <div style="max-width:1180px;margin:0 auto;padding:72px 24px 48px;display:flex;flex-direction:column;gap:16px">',
                        '<section style="margin:0 0 24px"><div style="display:flex;flex-direction:column;gap:16px">', 1)
    # senast uppdaterad-raden
    main = re.sub(r'<div style="max-width:820px;margin:0 auto;padding:0 24px"><p style="font-size:13px;color:[^"]*;\s*padding:14px 0 0">Senast uppdaterad.*?</p></div>', '', main, flags=re.S)
    # "länkarna går till nordicaim.se ..."-rader
    main = re.sub(r'<p style="font-size:15px;color:var\(--text-muted\)">Länkarna går till nordicaim\.se\..*?</p>', '', main, flags=re.S)
    # enkla citattecken i href -> dubbla, så att länkmappningen nedan fungerar
    main = re.sub(r"href='([^']*)'", r'href="\1"', main)
    # interna länkar
    for s, target in LINKMAP.items():
        for q in ('"', "'"):
            main = main.replace(f'href={q}{s}{q}', f'href="{target}"').replace(f'href={q}{s}#', f'href="{target}#')
    # länkar till nordicaim.se: relativa, utan ref, utan target/rel
    main = re.sub(r'href="https://nordicaim\.se(/[^"?]*)\?ref=varmekamera" target="_blank" rel="noopener(?: sponsored)?"', r'href="\1"', main)
    main = re.sub(r'href="https://nordicaim\.se/\?ref=varmekamera" target="_blank" rel="noopener(?: sponsored)?"', 'href="/"', main)
    # yttre container-padding (sajtens 820px-kolumn) -> temats artikelbredd
    main = main.replace('max-width:820px;margin:0 auto;padding:56px 24px 96px;', 'margin:0;padding:0;')
    main = main.replace('max-width:820px;margin:0 auto;padding:40px 24px 0', 'margin:0 0 32px')
    main = main.replace('max-width:820px;margin:0 auto;padding:48px 24px 96px;', 'margin:0;padding:0;')
    main = main.replace('max-width:820px;margin:0 auto;padding:40px 24px 96px;', 'margin:0;padding:0;')
    main = main.replace('max-width:820px;margin:0 auto;padding:32px 24px 0;', 'margin:0 0 24px;')
    main = re.sub(r'<(?=\d)', '&lt;', main)  # '<20 mK' -> '&lt;20 mK'
    for a, b in REPL:
        main = main.replace(a, b)
    main = re.sub(r'<details[^>]*>\s*<summary[^>]*>Vem står bakom den här sajten\?.*?</details>', '', main, flags=re.S)
    main = re.sub(r'>\s+<', '><', main)
    main = re.sub(r'\s{2,}', ' ', main).strip()

    leftovers = sorted(set(re.findall(r'[^.]{0,40}(?:Nordic Aim|sajt|Värmekamera drivs)[^.]{0,40}', re.sub(r'<[^>]+>', ' ', main))))
    return {
        "slug": slug, "handle": handle, "title": title, "tags": tags,
        "summary": f"<p>{html.escape(desc, quote=False)}</p>",
        "image": ({"url": image, "altText": alt} if image else None),
        "body": main, "leftovers": leftovers,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in ARTICLES:
        a = convert(slug)
        with open(os.path.join(OUT, a["handle"] + ".json"), "w", encoding="utf-8") as f:
            json.dump({"blogId": BLOG_ID, "handle": a["handle"], "title": a["title"], "tags": a["tags"],
                       "summary": a["summary"], "image": a["image"], "body": a["body"],
                       "author": {"name": "Nordic Aim"}, "isPublished": False, "templateSuffix": "article"},
                      f, ensure_ascii=False, indent=1)
        print(f"{a['handle']:40s} {len(a['body']):6d} tecken  kvar att granska: {len(a['leftovers'])}")
        for l in a["leftovers"]:
            print("    ·", l.strip())


if __name__ == "__main__":
    main()
