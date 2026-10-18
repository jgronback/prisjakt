#!/usr/bin/env python3
"""Validerar rättningsfiler (corrections/*.json).

Till skillnad från validate.py får siffror och listor ändras, men då krävs källa.
Kontroller: känt id, förbjudna mönster, länkar (relativa, kända mål, max 3),
källa när tekniska värden ändras, metafältsformat, giltig FAQ-JSON.
"""
import json, re, sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "validate.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)

def base_text(pid):
    for f in sorted(os.listdir(os.path.join(HERE, "proposals"))):
        for p in json.load(open(os.path.join(HERE, "proposals", f), encoding="utf-8")):
            if p["id"] == pid and p.get("descriptionHtml"):
                return p["descriptionHtml"]
    return V.nodes[pid]["descriptionHtml"] or ""

def check(c):
    errs = []
    n = V.nodes.get(c.get("id"))
    if not n: return [f"okänt id {c.get('id')}"]
    if c.get("handle") != n["handle"]: errs.append("handle matchar inte id")
    srcs = [s for s in (c.get("sources") or []) if re.match(r"https?://", s)]
    texts = []
    d = c.get("descriptionHtml")
    if d is not None:
        texts.append(("text", d))
        for href in re.findall(r'href="([^"]*)"', d):
            if re.match(r"https?://", href): errs.append(f"extern/absolut länk: {href}"); continue
            if href.split("#")[0].split("?")[0] not in V.targets: errs.append(f"okänt länkmål: {href}")
        if len(re.findall(r"<a\s", d)) > 3: errs.append("fler än 3 länkar")
        if "<strong>" in (n["descriptionHtml"] or "") and "<strong>" not in d: errs.append("fetstil/rubriker borttagna")
        new_nums = V.numbers(d) - V.numbers(base_text(c["id"]))
        if new_nums and not srcs: errs.append(f"nya siffror utan källa: {sorted(new_nums)[:8]}")
    faq = c.get("faq")
    if faq is not None:
        if not (isinstance(faq, list) and all(isinstance(x, dict) and x.get("q") and x.get("a") for x in faq)):
            errs.append("faq måste vara lista av {q,a}")
        else:
            texts.append(("faq", " ".join(x["q"] + " " + x["a"] for x in faq)))
    mf = c.get("metafields") or {}
    for k, val in mf.items():
        if k == "netd" and not re.match(r"^[≤<]\s?\d+ mK$", str(val)): errs.append(f"netd-format: {val}")
        if k == "sensorupplosning" and not re.match(r"^\d+x\d+$", str(val)): errs.append(f"sensor-format: {val}")
        if k in ("artbestamning", "detaljbedomning") and not str(val).isdigit(): errs.append(f"{k} ska vara heltal")
        if k == "laseravstandsmatare" and str(val) not in ("true", "false"): errs.append("lrf ska vara true/false")
    if mf and not srcs and set(mf) - {"netd", "sensorupplosning", "artbestamning", "detaljbedomning"}:
        errs.append("metafält ändrade utan källa")
    for label, t in texts + ([("titel", c["title"])] if c.get("title") else []):
        tt = V.text(t)
        for name, rx in V.BANNED.items():
            if name in ("hr", "tabell"): continue
            if re.search(rx, tt, flags=re.M): errs.append(f"{label}: förbjudet mönster '{name}'")
    if c.get("new_handle") and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", c["new_handle"]): errs.append("ogiltig handle")
    if c.get("new_handle") and not c.get("redirect"): errs.append("ny handle kräver redirect: true")
    if not c.get("changes"): errs.append("changes saknas")
    return errs

if __name__ == "__main__":
    cs = json.load(open(sys.argv[1], encoding="utf-8")); fails = 0
    for c in cs:
        e = check(c)
        if e: fails += 1; print(f"FAIL {c.get('handle')}: " + " | ".join(e))
        else: print(f"PASS {c.get('handle')}")
    print(f"\n{len(cs)} rättningar, {fails} FAIL"); sys.exit(1 if fails else 0)
