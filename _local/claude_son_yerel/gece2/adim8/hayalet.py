# parca_kutulari'nda olup GLB'de geometrisi olmayan kayıtlar (hayalet): python hayalet.py pk.json ucgen.pkl
import sys, json, pickle, numpy as np, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PK = json.load(open(sys.argv[1], encoding="utf-8")); D = pickle.load(open(sys.argv[2], "rb"))
BY = {}
for nm, lo, hi, P in D:
    b = nm.split("__")[0]; c = (lo + hi) / 2
    BY.setdefault(b, []).append(c)
for b in BY: BY[b] = np.concatenate(BY[b]) if BY[b][0].ndim == 2 else np.array(BY[b])
hay = []
for b, L in PK["parca"].items():
    C = BY.get(b)
    for e in L:
        lo = np.array(e[2::2]) - 0.6; hi = np.array(e[3::2]) + 0.6
        if C is None or not np.any(np.all((C >= lo) & (C <= hi), axis=1)): hay.append((b, e[0]))
print("hayalet", len(hay), "/", sum(len(L) for L in PK["parca"].values()))
from collections import Counter
print(Counter(b for b, _ in hay).most_common(40))
json.dump(hay, open("hayalet.json", "w", encoding="utf-8"), ensure_ascii=False)
