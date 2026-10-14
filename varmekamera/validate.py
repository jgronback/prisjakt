#!/usr/bin/env python3
"""Kontrollerar dist/: HTML-struktur, interna länkar och ankare, JSON-LD, externa länkar (valfritt)."""
import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
CHECK_EXTERNAL = "--external" in sys.argv

VOID = {"meta", "link", "img", "br", "hr", "input", "source"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.hrefs, self.imgs, self.errors, self.ld = [], set(), [], [], [], []
        self.words = 0
        self._in_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.errors.append(f"dubblett-id {a['id']}")
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
            if not a.get("alt"):
                self.errors.append(f"img utan alt: {a.get('src')}")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_script = True
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "script":
            self._in_script = False
        if not self.stack:
            self.errors.append(f"stängtag utan öppning: {tag}")
            return
        if self.stack[-1] != tag:
            # leta närmaste
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.errors.append(f"ostängd <{self.stack.pop()}> före </{tag}>")
                self.stack.pop()
            else:
                self.errors.append(f"oväntad </{tag}> (stack: {self.stack[-3:]})")
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self._in_script:
            self.ld.append(data)
        elif self.stack and self.stack[-1] not in ("script", "style"):
            self.words += len(data.split())


def main():
    files = sorted(f for f in os.listdir(DIST) if f.endswith(".html"))
    pages = {}
    total_err = 0
    for f in files:
        p = P()
        p.feed(open(os.path.join(DIST, f), encoding="utf-8").read())
        if p.stack:
            p.errors.append(f"ostängda taggar vid slut: {p.stack}")
        for s in p.ld:
            try:
                json.loads(s)
            except Exception as e:
                p.errors.append(f"JSON-LD ogiltig: {e}")
        pages[f] = p
    # länkar
    ext_urls = set()
    for f, p in pages.items():
        for h in p.hrefs:
            if h.startswith(("http://", "https://")):
                ext_urls.add(h)
                continue
            if h.startswith("mailto:"):
                continue
            path, _, frag = h.partition("#")
            target = f if path == "" else path
            if target not in pages and not os.path.exists(os.path.join(DIST, target)):
                p.errors.append(f"trasig intern länk: {h}")
            elif frag and target in pages and frag not in pages[target].ids:
                p.errors.append(f"saknat ankare: {h}")
        for img in p.imgs:
            src = img.get("src", "")
            if not src.startswith("http") and not os.path.exists(os.path.join(DIST, src)):
                p.errors.append(f"saknad bild: {src}")
    for f, p in pages.items():
        status = "OK " if not p.errors else "FEL"
        print(f"{status} {f:40s} {p.words:6d} ord  {len(p.hrefs):3d} länkar")
        for e in p.errors:
            print("     -", e)
        total_err += len(p.errors)
    print(f"\nTotalt: {sum(p.words for p in pages.values())} ord, {len(ext_urls)} unika externa URL:er, {total_err} fel")
    if CHECK_EXTERNAL:
        print("\nExterna länkar:")
        bad = 0
        for u in sorted(ext_urls):
            clean = u.replace("&amp;", "&")
            try:
                req = urllib.request.Request(clean, method="GET", headers={"User-Agent": "Mozilla/5.0 (validator)"})
                with urllib.request.urlopen(req, timeout=25) as r:
                    code = r.status
            except urllib.error.HTTPError as e:
                code = e.code
            except Exception as e:
                code = str(e)[:40]
            flag = "" if code == 200 else "  <-- KONTROLLERA"
            if code != 200:
                bad += 1
            print(f"  {code} {clean}{flag}")
            time.sleep(0.6)
        print(f"{bad} externa länkar svarade inte 200")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
