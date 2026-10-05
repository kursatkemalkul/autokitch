import sys, re, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
import json, io
idx = json.load(io.open("h3/_dunya/dunya.json", encoding="utf-8"))
G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
pat = sys.argv[1]
for ad, s, b in EO.dokum():
    if re.search(pat, ad, re.I):
        print("%-55s %-8s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f" % (ad, G[ad], *b))
