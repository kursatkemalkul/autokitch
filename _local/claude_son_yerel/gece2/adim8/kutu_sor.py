# -*- coding: utf-8 -*-
"""v9d: verilen kutularin icine giren ucgenler -> dugum + bilesen kutusu. SALT OKUMA.
kullanim: python kutu_sor.py "ad:x0,x1,y0,y1,z0,z1" ..."""
import sys, os, io, pickle, numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, os.path.join(S, "gece2", "adim5"))
from g_oku import GLB, bilesenler
ON = os.path.join(S, "gece2", "adim8", "_v9f_ucgen.pkl")
if os.path.exists(ON):
    D = pickle.load(open(ON, "rb"))
else:
    G = GLB(os.path.join(S, "gece2", "adim5e", "is5", "hat3_v9f.glb"))
    D = []
    for ni, nd in enumerate(G.J["nodes"]):
        if "mesh" not in nd or ni not in G.W: continue
        for X, T, ex, ok in G.dugum_ucgen(ni):
            if not len(T): continue
            P = X[T]
            D.append((nd["name"], P.min(1).astype(np.float32), P.max(1).astype(np.float32), P.astype(np.float32)))
    pickle.dump(D, open(ON, "wb"), protocol=4)
for arg in sys.argv[1:]:
    ad, k = arg.split(":"); q = [float(v) for v in k.split(",")]
    print("==", ad, q)
    for nm, lo, hi, P in D:
        m = (hi[:, 0] > q[0]) & (lo[:, 0] < q[1]) & (hi[:, 1] > q[2]) & (lo[:, 1] < q[3]) & (hi[:, 2] > q[4]) & (lo[:, 2] < q[5])
        if not m.any(): continue
        Q = P[m]
        # bilesen ayir
        X = Q.reshape(-1, 3).astype(float); T = np.arange(len(X)).reshape(-1, 3)
        tl = bilesenler(X, T, tol=0.05)
        for c in np.unique(tl):
            R = Q[tl == c].reshape(-1, 3)
            print("   %-40s %5d üçg  x %7.1f–%7.1f  y %7.1f–%7.1f  z %7.1f…%7.1f" % (nm, (tl == c).sum(), *[v for a in zip(R.min(0), R.max(0)) for v in a]))
