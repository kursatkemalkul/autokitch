# -*- coding: utf-8 -*-
import os, sys, numpy as np, manifold3d as mf, json
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"; sys.path[:0] = [K + r"\gece", K]; os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
g = Glb(sys.argv[1])
def kutu_ile(d, lo, hi, tol=0.6):
    g.bilesen(d, 0); c = [b for b in g._bc[d] if np.all(np.abs(b["lo"] - lo) < tol) and np.all(np.abs(b["hi"] - hi) < tol)]
    assert len(c) == 1, (d, lo, hi, len(c)); return c[0]
def icinde(d, lo, hi):
    g.bilesen(d, 0); return [b for b in g._bc[d] if np.all(b["lo"] >= np.array(lo) - 0.01) and np.all(b["hi"] <= np.array(hi) + 0.01)]
def M(b):
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)
    u, inv = np.unique(np.round(P, 4), axis=0, return_inverse=True)
    return mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
dx = -228.5
sil = kutu_ile("TOPPING_MODUL__aluminyum", np.array([2240.5 + dx, 1594.6, -811.0]), np.array([2277.9 + dx, 1632.4, -672.0]))
cep = icinde("TOPPING_MODUL__sac", (1972.9, 1567.9, -826.1), (2089.1, 1835.1, -639.9))
print("cep sac bileşen", len(cep), [(b["lo"].round(1).tolist(), b["hi"].round(1).tolist()) for b in cep])
ms = M(sil)
for b in cep: print("silindir ↔ cep sacı en küçük aralık mm", round(ms.min_gap(M(b), 50.0), 2))
for nm, lo, hi in (("arka mafsal", (2247.5, 1601.5, -827.0), (2271.5, 1625.5, -811.0)), ("ön boğaz", (2247.5, 1601.6, -672.0), (2271.2, 1625.4, -662.0))):
    b = kutu_ile("TOPPING_MODUL__aluminyum", np.array(lo) + [dx, 0, 0], np.array(hi) + [dx, 0, 0])
    for c in cep: print(" ", nm, "↔ cep sacı", round(M(b).min_gap(M(c), 50.0), 2))
