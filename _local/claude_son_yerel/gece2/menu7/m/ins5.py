# -*- coding: utf-8 -*-
"""bileşen(ler)in köşe koordinatlarının benzersiz değerleri + hacim (manifold)"""
import os, sys, json
import numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
K = S + r"\gece2\b4\52a"
sys.path[:0] = [K + r"\gece", K, os.path.dirname(os.path.abspath(__file__))]
os.environ["YAMA_IS_KOK"] = K
from m8kit import Glb
import manifold3d as mf
g = Glb(os.environ.get("GLB", K + r"\hat3_v9t.glb"))
for a in sys.argv[1:]:
    d, no = a.rsplit(":", 1)
    b = g.bilesen(d, int(no))
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    V = P.reshape(-1, 3)
    print("==", a, "tri", len(P), "lo", b["lo"].round(2), "hi", b["hi"].round(2), "kapali", b["kapali"])
    for k, nm in enumerate("xyz"):
        u = np.unique(np.round(V[:, k], 1))
        print("  ", nm, len(u), u[:40] if len(u) <= 40 else np.r_[u[:20], u[-20:]])
    R = np.round(V, 4); u, inv = np.unique(R, axis=0, return_inverse=True)
    try:
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
        print("   hacim", round(m.volume(), 1), "status", m.status())
    except Exception as e:
        print("   manifold yok", e)
