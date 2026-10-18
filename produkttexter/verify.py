#!/usr/bin/env python3
"""Slutkontroll: jämför butikens läge (återläsning) mot målen i bulk/bulk_vars.jsonl + bulk/final_fix.json.

Användning: python3 verify.py <readback1.json> [readback2.json ...]
  Varje readback-fil är ett graphql_query-svar: data.products.edges[].node med
  id, handle, title, descriptionHtml, mfs{nodes{key value}}.
Text jämförs tecken för tecken efter att taggar strippats och blanktecken normaliserats
(Shopify kan formatera om HTML), plus att länkarna (href) måste vara identiska.
Utdata: bulk/verify_mismatch.json (id, fält, förväntat, faktiskt)
"""
import json, sys, re, html, unicodedata, os
HERE = os.path.dirname(os.path.abspath(__file__))

def txt(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s).replace(" ", " ")
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", s).strip())
hrefs = lambda s: re.findall(r'href="([^"]*)"', s or "")

store = {}
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    d = d.get("data", d)
    for e in d["products"]["edges"]:
        n = e["node"]; n["mf"] = {m["key"]: m["value"] for m in (n.get("mfs") or {}).get("nodes", [])}
        store[n["id"]] = n

want = {}
for line in open(os.path.join(HERE, "bulk", "bulk_vars.jsonl"), encoding="utf-8"):
    if line.strip():
        p = json.loads(line)["p"]; want[p["id"]] = p
ff = json.load(open(os.path.join(HERE, "bulk", "final_fix.json"), encoding="utf-8"))
deletes = json.load(open(os.path.join(HERE, "bulk", "deletes.json"), encoding="utf-8")) + ff.get("deletes", [])

bad, missing = [], [pid for pid in want if pid not in store]
def miss(pid, field, exp, got): bad.append({"id": pid, "handle": store[pid]["handle"], "field": field, "expected": exp, "got": got})
for pid, p in want.items():
    s = store.get(pid)
    if not s: continue
    if "descriptionHtml" in p:
        if txt(p["descriptionHtml"]) != txt(s["descriptionHtml"]): miss(pid, "descriptionHtml", txt(p["descriptionHtml"]), txt(s["descriptionHtml"]))
        elif hrefs(p["descriptionHtml"]) != hrefs(s["descriptionHtml"]): miss(pid, "href", hrefs(p["descriptionHtml"]), hrefs(s["descriptionHtml"]))
    for k in ("title", "handle"):
        if k in p and p[k] != s[k]: miss(pid, k, p[k], s[k])
    for m in p.get("metafields", []):
        k, exp = m["key"], m["value"]
        if k == "short_pitch" and pid in ff["pitch_fixes"]: exp = ff["pitch_fixes"][pid]
        got = s["mf"].get(k)
        ok = (json.loads(exp) == json.loads(got)) if (k == "faq" and got) else (got is not None and unicodedata.normalize("NFC", exp) == unicodedata.normalize("NFC", got))
        if not ok: miss(pid, k, exp, got)
for pid, v in ff["pitch_fixes"].items():
    if pid in store and not any(m["key"] == "short_pitch" for m in want.get(pid, {}).get("metafields", [])):
        if store[pid]["mf"].get("short_pitch") != v: miss(pid, "short_pitch", v, store[pid]["mf"].get("short_pitch"))
for d in deletes:
    if d["ownerId"] in store and d["key"] in store[d["ownerId"]]["mf"]:
        miss(d["ownerId"], "delete:" + d["key"], None, store[d["ownerId"]]["mf"][d["key"]])

json.dump(bad, open(os.path.join(HERE, "bulk", "verify_mismatch.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"i butiken: {len(store)} | mål: {len(want)} | saknas i återläsning: {len(missing)} | avvikelser: {len(bad)}")
from collections import Counter
print(Counter(b["field"] for b in bad))
for b in bad[:30]:
    e, g = str(b["expected"]), str(b["got"])
    i = next((i for i in range(min(len(e), len(g))) if e[i] != g[i]), min(len(e), len(g)))
    print(f"- {b['handle']} [{b['field']}] förv: …{e[max(0,i-40):i+40]}… | fick: …{g[max(0,i-40):i+40]}…")
