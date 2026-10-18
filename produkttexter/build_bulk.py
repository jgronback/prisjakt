#!/usr/bin/env python3
"""Bygger JSONL för Shopify bulkOperationRunMutation av alla validerade förslag.

Användning:
  python3 build_bulk.py <current.json>
    current.json = aktuellt läge hämtat ur butiken precis före körning:
    lista av {"id","descriptionHtml","sp":{"value"}} (samma form som backupen).

Regler:
  - Bara förslag som går igenom validate.py tas med.
  - En produkt tas med bara om butikens nuvarande text och pitch är antingen
    oförändrade sedan backupen eller redan identiska med förslaget (agenter som
    hann applicera). Annars har någon annan ändrat den: hoppa över och rapportera.
  - Varje rad sätter både descriptionHtml och custom.short_pitch där förslaget
    har ett värde. Att skicka om en redan inlagd text är ofarligt och rättar
    de skrivfel som uppstod när agenter skrev in text för hand.
Utdata: bulk/bulk_vars.jsonl, bulk/bulk_plan.json, bulk/skipped.json
"""
import json, glob, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "validate.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

backup = {n["id"]: n for n in json.load(open(os.path.join(HERE, "backup_2026-10-18.json"), encoding="utf-8"))}
current = {n["id"]: n for n in json.load(open(sys.argv[1], encoding="utf-8"))}

lines, plan, skipped = [], [], []
for f in sorted(glob.glob(os.path.join(HERE, "proposals", "b*.json"))):
    for p in json.load(open(f, encoding="utf-8")):
        d, sp = p.get("descriptionHtml"), p.get("short_pitch")
        if d is None and sp is None:
            continue
        errs, _ = V.check(p)
        if errs:
            skipped.append({"handle": p["handle"], "why": "validering: " + " | ".join(errs)}); continue
        b, c = backup[p["id"]], current.get(p["id"])
        if c is None:
            skipped.append({"handle": p["handle"], "why": "finns inte längre som aktiv produkt"}); continue
        cd, bd = norm(c["descriptionHtml"]), norm(b["descriptionHtml"])
        csp = ((c.get("sp") or {}).get("value") or "").strip()
        bsp = ((b.get("sp") or {}).get("value") or "").strip()
        if d is not None and cd not in (bd, norm(d)):
            skipped.append({"handle": p["handle"], "why": "texten ändrad i butiken av någon annan sedan backupen"}); continue
        if sp is not None and csp not in (bsp, sp.strip()):
            skipped.append({"handle": p["handle"], "why": "pitchen ändrad i butiken av någon annan sedan backupen"}); continue
        inp = {"id": p["id"]}
        if d is not None and norm(d) != cd or (d is not None and d != c["descriptionHtml"] and norm(d) == cd and False):
            inp["descriptionHtml"] = d
        elif d is not None and d != c["descriptionHtml"]:
            inp["descriptionHtml"] = d  # samma text men annan HTML, t.ex. skrivfel rättade via whitespace
        if sp is not None and sp.strip() != csp:
            inp["metafields"] = [{"namespace": "custom", "key": "short_pitch", "type": "multi_line_text_field", "value": sp}]
        if len(inp) == 1:
            continue  # redan exakt inlagt
        lines.append(json.dumps({"p": inp}, ensure_ascii=False))
        plan.append({"id": p["id"], "handle": p["handle"], "text": "descriptionHtml" in inp, "pitch": "metafields" in inp, "batch": os.path.basename(f)})

os.makedirs(os.path.join(HERE, "bulk"), exist_ok=True)
open(os.path.join(HERE, "bulk", "bulk_vars.jsonl"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
json.dump(plan, open(os.path.join(HERE, "bulk", "bulk_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(skipped, open(os.path.join(HERE, "bulk", "skipped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"rader: {len(lines)} | text: {sum(x['text'] for x in plan)} | pitch: {sum(x['pitch'] for x in plan)} | hoppade över: {len(skipped)}")
print(f"filstorlek: {os.path.getsize(os.path.join(HERE, 'bulk', 'bulk_vars.jsonl'))/1e6:.1f} MB")
for s in skipped[:30]:
    print("  -", s["handle"], ":", s["why"][:150])
