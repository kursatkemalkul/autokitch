import sys, re, os, json, io
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
idx = json.load(io.open("h3/_dunya/dunya.json", encoding="utf-8"))
G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
x0, x1, y0, y1, z0, z1 = map(float, sys.argv[1:7]); pat = sys.argv[7] if len(sys.argv) > 7 else "."
q = (x0, x1, y0, y1, z0, z1)
for ad, s, b in EO.dokum():
    if EO._ust(q, b, 0.0) and re.search(pat, ad):
        print("%-58s %-8s x %7.1f %7.1f  y %7.1f %7.1f  z %7.1f %7.1f" % (ad, G[ad], *b))
sys.stdout.flush(); os._exit(0)
