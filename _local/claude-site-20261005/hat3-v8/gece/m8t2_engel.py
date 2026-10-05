# -*- coding: utf-8 -*-
"""m8t2: ana hat dışı kablo/hortum bileşenlerinden eksen segmentleri (engel) -> m8t2/engel.json (serit)"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "m8", "kablo_is"))
import glbkit, serit
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
G = glbkit.Glb(sys.argv[1])
LIN = ('kablo', 'kablo_veri', 'hava_ana', 'hava', 'bakir', 'hortum_gida', 'hortum_yag', 'hortum_orgu')
out = []
for p in G.prims:
    if "__" not in p["name"]: continue
    base, mat = p["name"].split("__", 1)
    if mat not in LIN or base == "ELK_ANA_HAT": continue
    vis = G.gorunur(p); X, T = p["X"], p["T"]
    if not vis.any(): continue
    Pq = np.round(X, 2); u, inv = np.unique(Pq, axis=0, return_inverse=True); inv = inv.reshape(-1); Ti = inv[T]
    r_ = np.concatenate([Ti[vis][:, 0], Ti[vis][:, 1]]); c_ = np.concatenate([Ti[vis][:, 1], Ti[vis][:, 2]])
    k, lab = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(u), len(u))), directed=False)
    tl = lab[Ti[:, 0]]
    for ci in np.unique(tl[vis]):
        m = (tl == ci) & vis
        S = serit.segmentler(X[T[m]])
        for q in S:
            if np.linalg.norm(q["b"] - q["a"]) < 0.5 * q["r"]: continue
            out.append(dict(ad="%s#%d" % (p["name"], ci), r=float(q["r"]), a=q["a"].tolist(), b=q["b"].tolist()))
json.dump(out, open(os.path.join(HERE, "m8t2", "engel.json"), "w"))
print(len(out), "segment")
