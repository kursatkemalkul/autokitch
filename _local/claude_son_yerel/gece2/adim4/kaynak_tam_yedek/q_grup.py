import sys, os, json, io, collections
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
idx = json.load(io.open("h3/_dunya/dunya.json", encoding="utf-8"))
G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
B = collections.defaultdict(lambda: [1e9, -1e9, 1e9, -1e9, 1e9, -1e9]); C = collections.Counter(); U = collections.defaultdict(set)
for ad, s, b in EO.dokum():
    g = G[ad]
    if g == "SABIT": continue
    k = g if not g.startswith("CEKMECE") else g
    q = B[k]; C[k] += 1; U[k].add(ad.split("|")[0][:14])
    for i in range(3):
        q[2 * i] = min(q[2 * i], b[2 * i]); q[2 * i + 1] = max(q[2 * i + 1], b[2 * i + 1])
for k in sorted(B):
    print("%-22s %4d  x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f  %s" % (k, C[k], *B[k], sorted(U[k])[:4]))
sys.stdout.flush(); os._exit(0)
