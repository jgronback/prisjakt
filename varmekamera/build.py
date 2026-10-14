#!/usr/bin/env python3
"""Statisk sajtgenerator för Värmekamera (systersajt till värmesikte.se).

Kör:  python3 build.py
Utdata hamnar i dist/ och laddas upp som den är till webbhotellet (t.ex. Strato),
på samma sätt som värmesikte.se.

ALLT som beror på domänen styrs av DOMAIN nedan. Byt den när domänen är köpt och
kör om skriptet; canonical, og:url, sitemap, robots, JSON-LD och llms.txt följer med.
"""
from __future__ import annotations

import html
import json
import os
import shutil
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

# ---------------------------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------------------------
# OBS: varmekamera.se och värmekamera.se är redan registrerade av andra (okt 2026).
# Nedan står den ASCII-domän som var ledig vid kontrollen. Byt vid behov.
DOMAIN = "www.varmekameror.se"
BASE_URL = f"https://{DOMAIN}"
SITE_NAME = "Värmekamera"            # så heter sajten i menyer, logotyp och titlar
SITE_TAGLINE = "Så fungerar en värmekamera, och så väljer du rätt"
REF = "varmekamera"                  # ?ref=... på alla länkar till Nordic Aim
NA = "https://nordicaim.se"
NA_NAME = "Nordic Aim AB"
NA_ORGNR = "559529-3126"
NA_MAIL = "kontakt@nordicaim.se"
NA_TEL = "0301-772010"
SISTER = "https://www.varmesikte.se"
UPDATED = date(2026, 10, 14)         # "Senast uppdaterad" på alla sidor
YEAR = UPDATED.year

DIST = os.path.join(HERE, "dist")


# ---------------------------------------------------------------------------
# HJÄLPFUNKTIONER (importeras av innehållsmodulerna)
# ---------------------------------------------------------------------------
def esc(s: str) -> str:
    return html.escape(s, quote=True)


def na(path: str) -> str:
    """Länk till Nordic Aim med ref-parameter."""
    sep = "&" if "?" in path else "?"
    return f"{NA}{path}{sep}ref={REF}"


def ext(href: str, text: str, sponsored: bool = False, cls: str = "", style: str = "") -> str:
    rel = "noopener sponsored" if sponsored else "noopener"
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return f'<a href="{href}" target="_blank" rel="{rel}"{c}{st}>{text}</a>'


def nalink(path: str, text: str, sponsored: bool = False, **kw) -> str:
    return ext(na(path), text, sponsored, **kw)


def eyebrow(text: str) -> str:
    return (f'<span style="font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;'
            f'text-transform:uppercase;color:var(--reticle-700)">{text}</span>')


def page_hero(kicker: str, h1: str, lead: str = "", chips: list[tuple[str, str]] | None = None,
              wide: bool = False) -> str:
    maxw = "1180px" if wide else "820px"
    chip_html = ""
    if chips:
        chip_html = ('<div style="display:flex;gap:8px;flex-wrap:wrap;font-size:14px;font-weight:600">'
                     + "".join(f'<a href="{h}" style="padding:6px 12px;border:1px solid var(--mist-200);'
                               f'border-radius:999px;background:#fff">{t}</a>' for h, t in chips)
                     + "</div>")
    lead_html = (f'<p style="font-size:18px;line-height:1.55;color:var(--text-muted)">{lead}</p>'
                 if lead else "")
    return f'''
    <section style="background:#fff;border-bottom:1px solid var(--mist-200)">
      <div style="max-width:{maxw};margin:0 auto;padding:72px 24px 48px;display:flex;flex-direction:column;gap:16px">
        {eyebrow(kicker)}
        <h1 style="font-size:clamp(32px,4.5vw,48px);font-weight:800;line-height:1.05">{h1}</h1>
        {lead_html}
        {chip_html}
      </div>
    </section>'''


def article_open(gap: int = 56) -> str:
    return (f'<article style="max-width:820px;margin:0 auto;padding:56px 24px 96px;display:flex;'
            f'flex-direction:column;gap:{gap}px;font-size:17px;line-height:1.65">')


def article_close() -> str:
    return "</article>"


def sec(id_: str, h2: str, body: str, h2size: int = 28) -> str:
    return (f'<section id="{id_}" style="display:flex;flex-direction:column;gap:16px">'
            f'<h2 style="font-size:{h2size}px;font-weight:800">{h2}</h2>{body}</section>')


def callout(title: str, body: str, tone: str = "green") -> str:
    bg, bd = {"green": ("var(--reticle-50)", "var(--reticle-100)"),
              "grey": ("var(--mist-100)", "var(--mist-200)"),
              "orange": ("var(--blaze-50)", "#F6C9B2")}[tone]
    return (f'<div style="background:{bg};border:1px solid {bd};border-radius:12px;padding:20px 24px;'
            f'display:flex;flex-direction:column;gap:6px"><strong style="color:var(--text-strong)">{title}</strong>'
            f'<p style="font-size:16px">{body}</p></div>')


def short_answer(text: str) -> str:
    """Kort svar högst upp, för läsare och för AI-sammanfattningar."""
    return (f'<div style="border-left:4px solid var(--reticle-500);background:#fff;padding:16px 20px;'
            f'border-radius:0 12px 12px 0;box-shadow:var(--shadow-sm)">'
            f'<span style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;'
            f'color:var(--reticle-700)">Kort svar</span><p style="margin-top:6px;font-size:17px">{text}</p></div>')


def table(headers: list[str], rows: list[list[str]], caption: str = "", mono_first: bool = True) -> str:
    th = "".join(f'<th style="text-align:left;padding:10px 14px;font-family:var(--font-display);font-size:13px;'
                 f'letter-spacing:.04em;text-transform:uppercase;color:var(--text-muted);background:var(--mist-100);'
                 f'border-bottom:1px solid var(--mist-200)">{h}</th>' for h in headers)
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            font = "font-family:var(--font-mono);font-weight:600;color:var(--text-strong);" if (i == 0 and mono_first) else ""
            tds.append(f'<td style="padding:10px 14px;border-bottom:1px solid var(--mist-200);vertical-align:top;'
                       f'font-size:15px;line-height:1.5;{font}">{c}</td>')
        trs.append("<tr>" + "".join(tds) + "</tr>")
    cap = f'<caption style="text-align:left;font-size:14px;color:var(--text-muted);padding:0 0 8px">{caption}</caption>' if caption else ""
    return (f'<div style="overflow-x:auto;border:1px solid var(--mist-200);border-radius:12px;background:#fff">'
            f'<table style="width:100%;border-collapse:collapse;min-width:520px">{cap}<thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')


def deflist(items: list[tuple[str, str]]) -> str:
    rows = "".join(
        f'<div style="background:#fff;padding:16px 20px;display:grid;grid-template-columns:minmax(110px,180px) 1fr;'
        f'gap:16px;align-items:baseline"><span style="font-family:var(--font-mono);font-weight:700;font-size:14px;'
        f'color:var(--text-strong)">{k}</span><span style="font-size:15px;line-height:1.5">{v}</span></div>'
        for k, v in items)
    return (f'<div class="deflist" style="display:grid;gap:1px;background:var(--mist-200);border:1px solid var(--mist-200);'
            f'border-radius:12px;overflow:hidden">{rows}</div>')


def ul(items: list[str]) -> str:
    return ('<ul style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:8px">'
            + "".join(f"<li>{i}</li>" for i in items) + "</ul>")


def ol(items: list[str]) -> str:
    return ('<ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:10px">'
            + "".join(f"<li>{i}</li>" for i in items) + "</ol>")


def muted(text: str) -> str:
    return f'<p style="font-size:15px;color:var(--text-muted)">{text}</p>'


def product_card(brand: str, kind: str, name: str, text: str, img: str, alt: str,
                 specs: list[str], href: str) -> str:
    chips = "".join(f'<span style="font-family:var(--font-mono);font-size:12px;padding:3px 8px;border:1px solid var(--mist-200);'
                    f'border-radius:6px;background:var(--mist-50)">{s}</span>' for s in specs)
    return f'''
            <article class="h3" style="background:#fff;border:1px solid var(--mist-200);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:transform 120ms,box-shadow 120ms">
              <div style="aspect-ratio:4/3;background:var(--mist-50);display:flex;align-items:center;justify-content:center;padding:16px">
                <img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async" width="600" height="450" style="max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain">
              </div>
              <div style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:10px;flex:1">
                <span style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted)">{brand} · {kind}</span>
                <h3 style="font-size:19px;font-weight:700">{name}</h3>
                <p style="font-size:15px;line-height:1.55;flex:1">{text}</p>
                <div style="display:flex;gap:6px;flex-wrap:wrap">{chips}</div>
                <div style="margin-top:6px">
                  <a class="btn btn-secondary btn-sm btn-full" href="{href}" target="_blank" rel="noopener sponsored">Se hos Nordic Aim</a>
                </div>
              </div>
            </article>'''


def card_grid(cards: list[str], min_px: int = 260) -> str:
    return (f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax({min_px}px,1fr));gap:20px">'
            + "".join(cards) + "</div>")


def faq_details(q: str, a_html: str) -> str:
    return (f'<details style="background:#fff;border:1px solid var(--mist-200);border-radius:12px;padding:0 20px">'
            f'<summary style="cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:16px;'
            f'align-items:center;padding:18px 0;font-weight:700;font-size:17px;color:var(--text-strong)">{q}'
            f'<span style="font-family:var(--font-mono);color:var(--reticle-600);font-size:20px;line-height:1">+</span></summary>'
            f'<div style="padding:0 0 20px;font-size:16px;line-height:1.6;display:flex;flex-direction:column;gap:10px">{a_html}</div></details>')


def problem_card(code: str, tag: str, h2: str, what: str, why: str, need: str, do: str) -> str:
    return f'''
        <article id="{code.lower()}" style="background:#fff;border:1px solid var(--mist-200);border-radius:14px;padding:28px;display:flex;flex-direction:column;gap:14px">
          <div style="display:flex;gap:10px;align-items:center;font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase">
            <span style="color:var(--reticle-700);font-weight:700">{code}</span>
            <span style="color:var(--text-muted)">{tag}</span>
          </div>
          <h2 style="font-size:24px;font-weight:800">{h2}</h2>
          <div style="display:flex;flex-direction:column;gap:8px;font-size:16px">
            <p><strong>Vad som händer.</strong> {what}</p>
            <p><strong>Varför.</strong> {why}</p>
            <p><strong>Vad som krävs.</strong> {need}</p>
          </div>
          <p style="background:var(--reticle-50);border:1px solid var(--reticle-100);border-radius:10px;padding:14px 16px;font-size:16px"><strong>Gör så här.</strong> {do}</p>
        </article>'''


def guide_tiles(items: list[tuple[str, str, str]]) -> str:
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px">'
            + "".join(
                f'<a href="{h}" class="h4" style="background:#fff;border:1px solid var(--mist-200);border-radius:14px;padding:22px;'
                f'display:flex;flex-direction:column;gap:8px;color:inherit;transition:transform 120ms,box-shadow 120ms">'
                f'<h3 style="font-size:19px;font-weight:700">{t}</h3><p style="font-size:15px;line-height:1.5;color:var(--text-body)">{d}</p>'
                f'<span style="font-weight:700;color:var(--reticle-700);font-size:14px">Läs →</span></a>'
                for h, t, d in items) + "</div>")


def fov_deg(pixels: int, pitch_um: float, focal_mm: float) -> float:
    import math
    w = pixels * pitch_um / 1000.0
    return math.degrees(2 * math.atan(w / (2 * focal_mm)))


def width_at(pixels: int, pitch_um: float, focal_mm: float, dist_m: float = 100.0) -> float:
    import math
    return 2 * dist_m * math.tan(math.radians(fov_deg(pixels, pitch_um, focal_mm)) / 2)


def footprint_cm(pitch_um: float, focal_mm: float, dist_m: float = 100.0) -> float:
    return pitch_um / 1000.0 / focal_mm * dist_m * 100.0


def sv(x: float, dec: int = 1) -> str:
    s = f"{x:.{dec}f}".replace(".", ",")
    return s


# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Hem"),
    ("sa-fungerar-en-varmekamera.html", "Så fungerar det"),
    ("sensor-och-upplosning.html", "Sensor"),
    ("optik-och-rackvidd.html", "Optik"),
    ("varmekamera-for-jakt.html", "Jakt"),
    ("kopguide.html", "Köpguide"),
    ("problem.html", "Problem"),
    ("regler.html", "Regler"),
    ("faq.html", "FAQ"),
    ("om.html", "Om oss"),
]

FOOTER_CONTENT = [
    ("sa-fungerar-en-varmekamera.html", "Så fungerar en värmekamera"),
    ("sensor-och-upplosning.html", "Sensor, upplösning och NETD"),
    ("optik-och-rackvidd.html", "Optik, synfält och räckvidd"),
    ("varmekamera-vs-morkerkikare.html", "Värmekamera eller mörkerkikare"),
    ("anvandningsomraden.html", "Användningsområden"),
    ("varmekamera-for-jakt.html", "Värmekamera för jakt"),
    ("kopguide.html", "Köpguide"),
    ("problem.html", "Problem och lösningar"),
    ("regler.html", "Regler i Sverige"),
    ("ordlista.html", "Ordlista"),
    ("faq.html", "Frågor och svar"),
]


def logo_mark() -> str:
    # Enkel "lins + värmesignatur"-symbol i brandfärg, speglar siktet på värmesikte.se
    return ('<span aria-hidden="true" style="width:26px;height:26px;border:2px solid var(--reticle-500);border-radius:50%;'
            'position:relative;display:inline-block;overflow:hidden">'
            '<span style="position:absolute;left:50%;top:50%;width:10px;height:10px;margin:-5px;background:var(--reticle-500);border-radius:50%"></span>'
            '<span style="position:absolute;left:50%;top:50%;width:16px;height:16px;margin:-8px;border:1.5px solid var(--reticle-300);border-radius:50%;opacity:.8"></span>'
            '</span>')


def header(active: str) -> str:
    links = []
    for href, label in NAV:
        if href == active:
            st = "color:var(--text-strong);background:var(--mist-100)"
            cur = ' aria-current="page"'
        else:
            st = "color:var(--text-muted);background:transparent"
            cur = ""
        links.append(f'<a href="{href}"{cur} style="padding:8px 12px;border-radius:8px;{st};text-decoration:none" class="h1">{label}</a>')
    return f'''
  <a href="#main" class="skip">Till innehållet</a>
  <header style="position:sticky;top:0;z-index:20;background:rgba(246,248,249,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--mist-200)">
    <div style="max-width:1180px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:24px;min-height:64px;flex-wrap:wrap">
      <a href="index.html" style="display:flex;align-items:center;gap:10px;color:var(--text-strong);text-decoration:none" aria-label="{SITE_NAME}, startsida">
        {logo_mark()}
        <span style="font-family:var(--font-display);font-weight:800;font-size:18px;letter-spacing:-0.02em">{SITE_NAME}</span>
      </a>
      <nav aria-label="Huvudmeny" style="display:flex;gap:4px;flex-wrap:wrap;margin-left:auto;font-size:14px;font-weight:600">
        {"".join(links)}
      </nav>
    </div>
  </header>'''


def footer() -> str:
    content = "".join(f'<a href="{h}" style="color:var(--mist-300)">{t}</a>' for h, t in FOOTER_CONTENT)
    return f'''
  <footer style="background:var(--gunmetal-900);color:var(--text-on-dark-muted);border-top:3px solid var(--reticle-500)">
    <div style="max-width:1180px;margin:0 auto;padding:48px 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;font-size:14px;line-height:1.6">
      <div style="display:flex;flex-direction:column;gap:10px">
        <span style="font-family:var(--font-display);font-weight:800;font-size:18px;color:#fff">{SITE_NAME}</span>
        <p>Teknisk guide till värmekameror: hur de fungerar, vad specifikationerna betyder och hur du väljer rätt för jakt och spaning. Produkter via {NA_NAME}.</p>
        <p style="font-size:13px">Systersajt: {ext(SISTER + "/", "Värmesikte.se", style="color:var(--mist-300)")} om termiska sikten.</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <span style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mist-500)">Innehåll</span>
        {content}
      </div>
      <div style="display:flex;flex-direction:column;gap:6px">
        <span style="font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mist-500)">Partner</span>
        {nalink("/collections/varmekikare", "Värmekameror och värmekikare hos Nordic Aim", True, style="color:var(--mist-300)")}
        {nalink("/collections/termiska-sikten", "Värmesikten", True, style="color:var(--mist-300)")}
        {nalink("/collections/multispektrala-kikare", "Multispektrala kikare", True, style="color:var(--mist-300)")}
        {nalink("/blogs/nyheter", "Nordic Aims guider", style="color:var(--mist-300)")}
        {nalink("/pages/kontakta-oss", "Personlig rekommendation", style="color:var(--mist-300)")}
        <a href="om.html" style="color:var(--mist-300)">Om oss och samarbetet</a>
      </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,.14)">
      <div style="max-width:1180px;margin:0 auto;padding:16px 24px;font-size:12px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap">
        <span>© {YEAR} {SITE_NAME} · En sajt från {NA_NAME}, org.nr {NA_ORGNR}</span>
        <span style="display:flex;gap:16px;flex-wrap:wrap"><a href="integritet.html" style="color:var(--mist-400)">Integritet</a><span>Innehållet är information, inte juridisk rådgivning.</span></span>
      </div>
    </div>
  </footer>'''


def base_schema() -> list[dict]:
    return [
        {"@type": "WebSite", "@id": f"{BASE_URL}/#website", "name": SITE_NAME, "url": BASE_URL + "/",
         "inLanguage": "sv-SE", "description": "Teknisk guide till värmekameror: hur en värmekamera fungerar, sensor, optik, räckvidd, regler och köpråd för jakt.",
         "publisher": {"@id": f"{BASE_URL}/#org"}},
        {"@type": "Organization", "@id": f"{BASE_URL}/#org", "name": NA_NAME, "legalName": NA_NAME,
         "url": NA + "/", "taxID": NA_ORGNR, "email": NA_MAIL, "telephone": "+46301772010",
         "address": {"@type": "PostalAddress", "addressCountry": "SE"},
         "sameAs": [NA + "/", SISTER + "/"],
         "description": f"{NA_NAME} är en svensk webbutik för jakt- och skytteoptik och står bakom guidesajterna {SITE_NAME} och Värmesikte.se.",
         "knowsAbout": ["värmekamera", "termisk kikare", "värmekikare", "värmesikte", "termisk optik", "NETD", "mikrobolometer"]},
    ]


def breadcrumbs(slug: str, title: str) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Hem", "item": BASE_URL + "/"}]
    if slug != "index.html":
        items.append({"@type": "ListItem", "position": 2, "name": title, "item": f"{BASE_URL}/{slug}"})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def render(p: dict) -> str:
    slug = p["slug"]
    url = BASE_URL + "/" if slug == "index.html" else f"{BASE_URL}/{slug}"
    title = p["title"]
    full_title = title if p.get("raw_title") else f"{title} | {SITE_NAME}"
    desc = p["description"]
    graph = base_schema() + [breadcrumbs(slug, p.get("short", title))]
    if p.get("article", True) and slug != "index.html":
        graph.append({
            "@type": p.get("article_type", "TechArticle"),
            "@id": url + "#article",
            "headline": title, "description": desc, "inLanguage": "sv-SE",
            "url": url, "mainEntityOfPage": url,
            "datePublished": "2026-10-14", "dateModified": UPDATED.isoformat(),
            "author": {"@id": f"{BASE_URL}/#org"}, "publisher": {"@id": f"{BASE_URL}/#org"},
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "about": {"@type": "Thing", "name": "Värmekamera", "sameAs": "https://sv.wikipedia.org/wiki/V%C3%A4rmekamera"},
        })
    graph += p.get("schema", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    updated_line = ""
    if slug not in ("index.html", "404.html"):
        updated_line = (f'<div style="max-width:820px;margin:0 auto;padding:0 24px"><p style="font-size:13px;color:var(--text-faint);'
                        f'padding:14px 0 0">Senast uppdaterad {UPDATED.strftime("%-d %B %Y").replace("October", "oktober")}. '
                        f'Skrivet av redaktionen på {SITE_NAME}, en sajt från {NA_NAME}. <a href="om.html">Så arbetar vi</a>.</p></div>')
    robots = '<meta name="robots" content="noindex,follow">\n' if p.get("noindex") else ""
    og_img = p.get("image", "https://cdn.shopify.com/s/files/1/0949/6553/0964/files/938492-0_7133a141-fdf9-43a0-97a4-6d483ae19eb5.jpg?v=1766941791&width=1200")
    return f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{"website" if slug == "index.html" else "article"}">
<meta property="og:locale" content="sv_SE">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16191D">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/montserrat-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/hanken-grotesk-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<div style="min-height:100vh;display:flex;flex-direction:column">
{header(slug)}
  <main id="main" style="flex:1">
{p["body"]}
{updated_line}
  </main>
{footer()}
</div>
</body>
</html>
'''


EXTRA_CSS = r"""

/* --- Värmekamera: tillägg utöver värmesikte.se --- */
.skip{position:absolute;left:-999px;top:8px;background:var(--gunmetal-900);color:#fff;padding:8px 12px;border-radius:8px;z-index:100}
.skip:focus{left:8px}
table{font-family:var(--font-sans)}
tbody tr:last-child td{border-bottom:none!important}
figure{margin:0}
figcaption{font-size:14px;color:var(--text-muted);margin-top:8px;line-height:1.5}
svg text{font-family:var(--font-sans)}
.diagram{width:100%;height:auto;display:block;background:#fff;border:1px solid var(--mist-200);border-radius:12px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.three-col{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.quick-grid{display:grid;grid-template-columns:1.2fr repeat(4,1fr);gap:16px}
blockquote{margin:0;padding:18px 22px;border-left:4px solid var(--reticle-500);background:#fff;border-radius:0 12px 12px 0;font-size:16px}
blockquote footer{font-size:14px;color:var(--text-muted);margin-top:8px}
@media (max-width:820px){.two-col,.three-col{grid-template-columns:1fr!important}.deflist>div{grid-template-columns:1fr!important;gap:4px!important}}
@media print{header,footer,.btn{display:none!important}body{background:#fff}}
"""


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#16191D"/>'
           '<circle cx="16" cy="16" r="9" fill="none" stroke="#01AE55" stroke-width="2.5"/>'
           '<circle cx="16" cy="16" r="3.5" fill="#01AE55"/></svg>')


def main() -> None:
    import pages_teknik, pages_jakt, pages_stod  # noqa: E402

    pages: list[dict] = []
    for mod in (pages_teknik, pages_jakt, pages_stod):
        pages += mod.pages()

    if os.path.isdir(os.path.join(DIST)):
        for name in os.listdir(DIST):
            if name.endswith((".html", ".xml", ".txt", ".svg")) or name == ".htaccess":
                os.remove(os.path.join(DIST, name))
    os.makedirs(os.path.join(DIST, "css"), exist_ok=True)

    # CSS: Nordic Aims tokens (identiska med värmesikte.se) + tillägg
    with open(os.path.join(HERE, "src", "style.base.css"), encoding="utf-8") as f:
        css = f.read()
    write(os.path.join(DIST, "css", "style.css"), css + EXTRA_CSS)
    write(os.path.join(DIST, "favicon.svg"), FAVICON)

    slugs = []
    for p in pages:
        write(os.path.join(DIST, p["slug"]), render(p))
        if not p.get("noindex") and p["slug"] != "404.html":
            slugs.append(p["slug"])

    # sitemap
    urls = []
    for s in slugs:
        loc = BASE_URL + "/" if s == "index.html" else f"{BASE_URL}/{s}"
        prio = "1.0" if s == "index.html" else ("0.9" if s in ("sa-fungerar-en-varmekamera.html", "kopguide.html", "varmekamera-for-jakt.html") else "0.7")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{UPDATED.isoformat()}</lastmod><priority>{prio}</priority></url>")
    write(os.path.join(DIST, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")

    write(os.path.join(DIST, "robots.txt"),
          f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

    # llms.txt – för AI-sökmotorer (GEO)
    lines = [f"# {SITE_NAME}", "",
             f"> Svensk teknisk guide till värmekameror (termiska kameror): hur en värmekamera fungerar, vad sensor, NETD, "
             f"optik och synfält betyder, skillnad mot mörkerkikare, regler i Sverige och köpråd för jakt. "
             f"Sajten drivs av {NA_NAME} (org.nr {NA_ORGNR}), svensk återförsäljare av termisk optik. Produktlänkar går till nordicaim.se.", "",
             "## Sidor", ""]
    for p in pages:
        if p.get("noindex") or p["slug"] == "404.html":
            continue
        loc = BASE_URL + "/" if p["slug"] == "index.html" else f"{BASE_URL}/{p['slug']}"
        lines.append(f"- [{p['title']}]({loc}): {p['description']}")
    lines += ["", "## Relaterat", "",
              f"- [Värmesikte.se]({SISTER}/): systersajt om termiska sikten för jakt",
              f"- [Nordic Aim, värmekikare]({NA}/collections/varmekikare): sortiment, priser och lagerstatus",
              f"- [Nordic Aim, guider]({NA}/blogs/nyheter): fördjupande artiklar om termisk optik", ""]
    write(os.path.join(DIST, "llms.txt"), "\n".join(lines))

    # .htaccess för Apache-hotell (Strato): www-kanonisering, https, 404, cache
    apex = DOMAIN[4:] if DOMAIN.startswith("www.") else DOMAIN
    write(os.path.join(DIST, ".htaccess"), f"""# {SITE_NAME} – Apache-regler (fungerar på Strato och de flesta delade webbhotell)
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
AddType font/woff2 .woff2
AddType image/svg+xml .svg

<IfModule mod_rewrite.c>
RewriteEngine On
# tvinga https + www så att det bara finns en kanonisk adress
RewriteCond %{{HTTPS}} !=on [OR]
RewriteCond %{{HTTP_HOST}} ^{apex.replace('.', r'\.')}$ [NC]
RewriteRule ^(.*)$ {BASE_URL}/$1 [R=301,L]
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 30 days"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType image/svg+xml "access plus 30 days"
ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
<FilesMatch "\\.(woff2)$">
Header set Access-Control-Allow-Origin "*"
</FilesMatch>
</IfModule>
""")

    print(f"Byggde {len(pages)} sidor till {DIST} för {BASE_URL}")


if __name__ == "__main__":
    main()
