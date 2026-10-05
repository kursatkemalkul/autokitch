# -*- coding: utf-8 -*-
"""m8t2: kopya rota (eski) GLB'deki ana hat kablolarıyla örtüşüyor mu? + bileşen eşleme -> m8t2/eslem.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import glbkit, m8t2_rota_eski as RE
from scipy.spatial import cKDTree
GLB = sys.argv[1]
G = glbkit.Glb(GLB)
o, K = RE.eski()
comps = []
for p in G.prims:
    if not p["name"].startswith("ELK_ANA_HAT__kablo") and not p["name"].startswith("ELK_ZEMIN"): continue
    tl, kut = G.komp(p)
    for ci, (lo, hi, n) in kut.items():
        comps.append((p["name"], ci, lo, hi, n))
print(len(comps), "bilesen")
for p in G.prims:
    if p["name"].startswith("ELK_ANA_HAT__kablo"):
        print(p["name"], len(p["T"]), p["pr"].get("extras", {}))


def ornek(pts, adim=5.0):
    Q = []
    for a, b in zip(pts[:-1], pts[1:]):
        a = np.array(a); b = np.array(b); L = np.linalg.norm(b - a); n = max(2, int(L / adim))
        for t in np.linspace(0, 1, n): Q.append(a + t * (b - a))
    return np.array(Q)


VS = {}
for p in G.prims:
    if p["name"].startswith("ELK_ANA_HAT__kablo"):
        tl, kut = G.komp(p); vis = G.gorunur(p)
        for ci in kut:
            m = (tl == ci) & vis; VS[(p["name"], ci)] = p["X"][np.unique(p["T"][m])]
TR = {k: cKDTree(v) for k, v in VS.items()}
es = {}
for ad, (r, mal, pts) in o.items():
    Q = ornek(pts)
    best = None
    for k, t in TR.items():
        d, _ = t.query(Q)
        sc = np.mean(np.abs(d - r) < 1.5)
        if best is None or sc > best[0]: best = (sc, k, np.median(d))
    es[ad] = dict(prim=best[1][0], comp=int(best[1][1]), skor=float(best[0]), med=float(best[2]), r=r, mal=mal)
    print("%-14s r%5.2f -> %s#%d skor %.2f med %.2f" % (ad, r, best[1][0], best[1][1], best[0], best[2]))
json.dump(es, open(os.path.join(HERE, "m8t2", "eslem.json"), "w"), indent=1)
