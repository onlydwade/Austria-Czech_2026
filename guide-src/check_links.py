# -*- coding: utf-8 -*-
"""Check that every in-page link (href="#...") in index.html points to an existing id."""
import os, re, sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
s = open(path, encoding="utf-8").read()
ids = set(re.findall(r'id="([^"]+)"', s))
broken = sorted({h for h in re.findall(r'href="#([^"]+)"', s) if h not in ids})
if broken:
    print("Broken in-page links:", ", ".join(broken))
    sys.exit(1)
print("OK:", len(re.findall(r'href="#', s)), "in-page links,", len(ids), "ids")
