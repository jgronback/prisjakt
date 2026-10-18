#!/usr/bin/env python3
"""Validerar förslag på ändrade produkttexter mot backupen.

Användning: python3 validate.py proposals/<batch>.json
Förslagsfil: lista av {"id","handle","descriptionHtml": str|null, "short_pitch": str|null, "change_note": str}
null = fältet lämnas orört. Skriver ut PASS/FAIL per produkt och exit 1 om något FAIL.
"""
import json, re, sys, os, difflib, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
nodes = {n["id"]: n for n in json.load(open(os.path.join(HERE, "backup_2026-10-18.json"), encoding="utf-8"))}
by_handle = {n["handle"]: n for n in nodes.values()}
targets = json.load(open(os.path.join(HERE, "link_targets.json"), encoding="utf-8"))
ART = json.load(open(os.path.join(HERE, "art_table.json"), encoding="utf-8"))

def text(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()
def norm_num(s):
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"(?<=\d) (?=\d{3}\b)", "", s)      # 1 300 -> 1300
    return s.replace(",", ".")
def numbers(s):
    s = norm_num(text(s))
    out = set()
    for m in re.findall(r"\d+(?:\.\d+)?", s):
        out.add(m.rstrip("0").rstrip(".") if "." in m else m)
    return out
def mf_text(n):
    return " ".join(str((n.get(k) or {}).get("value") or "") for k in ("sensor","obj","pitch","lrf","netd","det","forst","faq","sp"))
def section(h, name):
    # Avsnittet slutar där dess lista slutar (</p> eller </ul> efter första punkten),
    # inte vid textens slut: annars räknas den avslutande säljtexten in i "Detta ingår".
    h = h or ""
    i = h.find(name)
    if i < 0: return None
    rest = h[i + len(name):]
    m = re.search(r"(?:•|<li).*?(?:</p>|</ul>)", rest, re.S)
    t = text(rest[:m.end()] if m else rest)
    t = re.split(r"Detta ingår|Teknisk specifikation|Nyckelfunktioner", t)[0]
    return t.strip()[:3000]
def art_numbers(n):
    out = set()
    try:
        p = re.search(r"\d+", (n.get("pitch") or {}).get("value") or "").group(0)
        f = re.search(r"\d+", (n.get("obj") or {}).get("value") or "").group(0)
        row = ART.get(f"{p}/{f}")
        if row: out |= {str(row[0]), str(row[1])}
    except Exception: pass
    return out

BANNED = {
 "em dash": r"—", "svenskt lager": r"svenskt lager|svenska lager",
 "leverantör": r"Astro Sweden|Focus Nordic|Armtac|distribueras av|supportas av",
 "rödpunktssikte": r"rödpunktssikte", "termik": r"\btermik\b", "dual use": r"dual[ -]use",
 "binokulär": r"binokulär", "rigg": r"\b(natt)?rigg\b", "öppet köp": r"öppet köp",
 "oavsett om": r"[Oo]avsett om", "inte bara utan": r"[Ii]nte bara\b[^.]{0,80}\butan (också|även)",
 "nästa nivå": r"nästa nivå", "upplevelse": r"(jakt|skjut|skytte|tittar|använd(ar)?)upplevelse",
 "sömlös": r"sömlös", "helhetslösning": r"helhetslösning|komplett paket",
 "avancerad teknik": r"(avancerad|modern|banbrytande|innovativ) teknik",
 "prestanda-floskel": r"(optimerad|kraftfull|maximal|överlägsen|enastående) prestanda",
 "robust konstruktion": r"robust konstruktion", "superlativ": r"marknadsledande|i särklass|oöverträffad|revolutionerande",
 "designad för att": r"designad för att|utformad för att möta", "full kontroll": r"full kontroll|full frihet",
 "perfekt för": r"[Pp]erfekt (för|val)", "tryggt val": r"ett tryggt val|att lita på",
 "bästa av två världar": r"bästa av två världar", "i en värld": r"[Ii] en värld där",
 "hög kvalitet": r"hög kvalitet|högsta kvalitet|premiumkvalitet", "enkel att använda": r"enkel att använda|användarvänlig",
 "fantastisk": r"[Ff]antastisk|[Oo]trolig|[Ii]mponerande", "förbjudna ord": r"\b(Källa|Enligt tillverkaren|Saknas|Okänt|Ej verifierat|Troligen)\b",
 "retorisk fråga": r"(^|<p>)(Söker du|Letar du)[^?]{0,140}\?", "hr": r"<hr", "tabell": r"<table",
}

def check(p):
    errs, warns = [], []
    n = nodes.get(p.get("id"))
    if not n: return [f"okänt id {p.get('id')}"], []
    if p.get("handle") != n["handle"]: errs.append("handle matchar inte id")
    old_h = n["descriptionHtml"] or ""; old_sp = (n.get("sp") or {}).get("value") or ""
    new_h = p.get("descriptionHtml"); new_sp = p.get("short_pitch")
    linked = []
    if new_h is not None:
        for href in re.findall(r'href="([^"]*)"', new_h):
            if re.match(r"https?://", href):
                errs.append(f"extern/absolut länk: {href}"); continue
            base = href.split("#")[0].split("?")[0]
            if base not in targets: errs.append(f"okänt länkmål: {href}")
            m = re.match(r"/products/(.+)", base)
            if m and m.group(1) in by_handle: linked.append(by_handle[m.group(1)])
        nlinks = len(re.findall(r"<a\s", new_h)); old_links = len(re.findall(r"<a\s", old_h))
        if nlinks > max(3, old_links): errs.append(f"{nlinks} länkar (max 3)")
        for nm in ("Teknisk specifikation", "Detta ingår"):
            a, b = section(old_h, nm), section(new_h, nm)
            if a is not None and a != b: errs.append(f"avsnittet '{nm}' har ändrats")
        ratio = difflib.SequenceMatcher(None, text(old_h), text(new_h), autojunk=False).ratio()
        if ratio < 0.55: errs.append(f"för stor omskrivning (likhet {ratio:.2f} < 0.55)")
        if len(text(new_h)) < 0.8 * len(text(old_h)): warns.append("texten krympte mer än 20 %")
        if "<strong>" in old_h and "<strong>" not in new_h: errs.append("fetstil/rubriker borttagna")
    allowed = numbers(old_h) | numbers(old_sp) | numbers(mf_text(n)) | numbers(n["title"]) | art_numbers(n)
    for s in linked: allowed |= numbers(s["title"]) | numbers(mf_text(s)) | art_numbers(s)
    for label, new in (("text", new_h), ("pitch", new_sp)):
        if new is None: continue
        t = text(new)
        bad = sorted(numbers(new) - allowed, key=lambda x: (len(x), x))
        if bad: errs.append(f"{label}: nya siffror som inte finns i källan: {bad}")
        old_t = text(old_h) + " " + old_sp
        for name, rx in BANNED.items():
            src = new if name in ("hr", "tabell") else t
            if re.search(rx, src, flags=re.M): errs.append(f"{label}: förbjudet mönster '{name}'")
    if new_sp is not None:
        L = len(new_sp)
        if not 80 <= L <= 180: errs.append(f"pitch {L} tecken (80-180)")
        if "\n" in new_sp: errs.append("pitch har radbrytning")
    if new_h is None and new_sp is None: warns.append("inga ändringar")
    return errs, warns

def main(path):
    props = json.load(open(path, encoding="utf-8"))
    fails = 0
    seen = set()
    for p in props:
        if p.get("id") in seen: print(f"FAIL {p.get('handle')}: dubblett"); fails += 1; continue
        seen.add(p.get("id"))
        e, w = check(p)
        if e: fails += 1; print(f"FAIL {p.get('handle')}: " + " | ".join(e))
        elif w: print(f"OK*  {p.get('handle')}: " + " | ".join(w))
        else: print(f"PASS {p.get('handle')}")
    print(f"\n{len(props)} förslag, {fails} FAIL")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main(sys.argv[1])
