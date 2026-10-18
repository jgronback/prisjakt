#!/usr/bin/env python3
"""Bygger JSONL för Shopify bulkOperationRunMutation (productUpdate) av:
  1. proposals/b*.json   (texter, short pitch, länkar)  validerade med validate.py
  2. corrections/c*.json (rättade fakta: text, FAQ, metafält, titel, handle) validerade med validate_corr.py
     En rättning går före förslaget för samma produkt.
  3. Rena stavningsrättningar i titel och pitch ("rödpunktssikte" -> "rödpunktsikte").
  4. Interna länkar till handles som byter namn skrivs om till den nya handlen.

Användning: python3 build_bulk.py <current.json>
  current.json = butikens aktuella läge, samma form som backupen (id, handle, title,
  descriptionHtml, sp{value}, faq{value}), hämtat precis före körning.

Skydd: en produkt hoppas över om dess text eller pitch i butiken har ändrats av någon
annan sedan backupen (dvs. varken = backup eller = vårt förslag).
Utdata: bulk/bulk_vars.jsonl, bulk/bulk_plan.json, bulk/skipped.json
"""
import json, glob, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
V = load("v", "validate.py"); VC = load("vc", "validate_corr.py")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

MF_TYPES = {"artbestamning": "number_integer", "detaljbedomning": "number_integer", "supplier_stock_hint": "number_integer",
            "laseravstandsmatare": "boolean", "belyst": "boolean", "faq": "json", "manual": "url", "supplier_url": "url",
            "short_pitch": "multi_line_text_field"}
mf_type = lambda k: MF_TYPES.get(k, "single_line_text_field")

backup = {n["id"]: n for n in json.load(open(os.path.join(HERE, "backup_2026-10-18.json"), encoding="utf-8"))}
current = {n["id"]: n for n in json.load(open(sys.argv[1], encoding="utf-8"))}

skipped = []
want = {}   # id -> dict(desc, pitch, faq, mf, title, handle)
for f in sorted(glob.glob(os.path.join(HERE, "proposals", "b*.json"))):
    for p in json.load(open(f, encoding="utf-8")):
        if p.get("descriptionHtml") is None and p.get("short_pitch") is None: continue
        e, _ = V.check(p)
        if e: skipped.append({"handle": p["handle"], "why": "förslag fäller validering: " + " | ".join(e)}); continue
        w = want.setdefault(p["id"], {})
        if p.get("descriptionHtml") is not None: w["desc"] = p["descriptionHtml"]
        if p.get("short_pitch"): w["pitch"] = p["short_pitch"]
for f in sorted(glob.glob(os.path.join(HERE, "corrections", "c*.json"))):
    for c in json.load(open(f, encoding="utf-8")):
        e = VC.check(c)
        if e: skipped.append({"handle": c.get("handle"), "why": "rättning fäller validering: " + " | ".join(e)}); continue
        w = want.setdefault(c["id"], {})
        if c.get("descriptionHtml") is not None: w["desc"] = c["descriptionHtml"]
        if c.get("faq") is not None: w["faq"] = c["faq"]
        for k, v in (c.get("metafields") or {}).items():
            v = str(v).lower() if isinstance(v, bool) else str(v)
            if k == "short_pitch": w["pitch"] = v
            elif v.strip() == "": w.setdefault("delete", set()).add(k)
            else: w.setdefault("mf", {})[k] = v
        if c.get("title"): w["title"] = c["title"]
        if c.get("new_handle"): w["handle"] = c["new_handle"]

# stavning i titel och pitch för alla produkter
for pid, n in backup.items():
    t = want.get(pid, {}).get("title") or n["title"]
    if "ödpunktssikte" in t:
        want.setdefault(pid, {})["title"] = t.replace("ödpunktssikte", "ödpunktsikte")
    sp = want.get(pid, {}).get("pitch") or ((n.get("sp") or {}).get("value") or "")
    if "ödpunktssikte" in sp:
        want.setdefault(pid, {})["pitch"] = sp.replace("ödpunktssikte", "ödpunktsikte")

# länkar till gamla handles -> nya
renames = {backup[pid]["handle"]: w["handle"] for pid, w in want.items() if w.get("handle")}
if renames:
    for pid, n in backup.items():
        d = want.get(pid, {}).get("desc", n["descriptionHtml"] or "")
        d2 = d
        for old, new in renames.items(): d2 = d2.replace(f'href="/products/{old}"', f'href="/products/{new}"').replace(f'href="/products/{old}#', f'href="/products/{new}#')
        if d2 != d: want.setdefault(pid, {})["desc"] = d2

lines, plan, deletes = [], [], []
for pid, w in want.items():
    b, c = backup[pid], current.get(pid)
    if c is None: skipped.append({"handle": b["handle"], "why": "inte längre aktiv"}); continue
    cd, bd = norm(c["descriptionHtml"]), norm(b["descriptionHtml"])
    csp = ((c.get("sp") or {}).get("value") or "").strip(); bsp = ((b.get("sp") or {}).get("value") or "").strip()
    if "desc" in w and cd not in (bd, norm(w["desc"])):
        skipped.append({"handle": b["handle"], "why": "texten ändrad i butiken av någon annan sedan backupen"}); continue
    if "pitch" in w and csp not in (bsp, w["pitch"].strip()):
        skipped.append({"handle": b["handle"], "why": "pitchen ändrad i butiken av någon annan sedan backupen"}); continue
    inp = {"id": pid}
    if "desc" in w and w["desc"] != c["descriptionHtml"]: inp["descriptionHtml"] = w["desc"]
    mfs = []
    if "pitch" in w and w["pitch"].strip() != csp:
        mfs.append({"namespace": "custom", "key": "short_pitch", "type": "multi_line_text_field", "value": w["pitch"]})
    if "faq" in w:
        mfs.append({"namespace": "custom", "key": "faq", "type": "json", "value": json.dumps(w["faq"], ensure_ascii=False)})
    for k, v in (w.get("mf") or {}).items():
        mfs.append({"namespace": "custom", "key": k, "type": mf_type(k), "value": v})
    if mfs: inp["metafields"] = mfs
    if w.get("title") and w["title"] != c.get("title"): inp["title"] = w["title"]
    if w.get("handle") and w["handle"] != c.get("handle"): inp["handle"] = w["handle"]; inp["redirectNewHandle"] = True
    for k in sorted(w.get("delete", ())):
        if (c.get(k) if False else True): deletes.append({"ownerId": pid, "namespace": "custom", "key": k})
    if len(inp) == 1: continue
    lines.append(json.dumps({"p": inp}, ensure_ascii=False))
    plan.append({"id": pid, "handle": b["handle"], "fields": sorted(k for k in inp if k != "id"),
                 "metafields": [m["key"] for m in mfs]})

os.makedirs(os.path.join(HERE, "bulk"), exist_ok=True)
open(os.path.join(HERE, "bulk", "bulk_vars.jsonl"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
json.dump(plan, open(os.path.join(HERE, "bulk", "bulk_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(skipped, open(os.path.join(HERE, "bulk", "skipped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(deletes, open(os.path.join(HERE, "bulk", "deletes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"metafält att radera: {len(deletes)}")
from collections import Counter
cnt = Counter(f for p in plan for f in p["fields"]); mcnt = Counter(m for p in plan for m in p["metafields"])
print(f"rader: {len(lines)} | fält: {dict(cnt)} | metafält: {dict(mcnt)} | hoppade över: {len(skipped)}")
print(f"filstorlek: {os.path.getsize(os.path.join(HERE, 'bulk', 'bulk_vars.jsonl'))/1e6:.2f} MB")
for s in skipped[:40]: print("  -", s["handle"], ":", s["why"][:160])
