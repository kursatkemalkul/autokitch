"""bir düğümün eksene dik düzlemsel yüzlerini listele (alan>esik): python g_kesit.py dugum_desen [kutu x0 x1 y0 y1 z0 z1]"""
import sys, os, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_oku import GLB
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
G = GLB(os.path.join(S, "hat3_v8zq.glb")); d = re.compile(sys.argv[1])
kb = list(map(float, sys.argv[2:8])) if len(sys.argv) >= 8 else None
for ni, nd in enumerate(G.J["nodes"]):
    if "mesh" not in nd or not d.search(nd.get("name", "")): continue
    for X, T, ex, ok in G.dugum_ucgen(ni):
        P = X[T]
        if kb:
            c = P.mean(1); m = ((c >= np.array(kb[0::2])) & (c <= np.array(kb[1::2]))).all(1); P = P[m]
        n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); A = np.linalg.norm(n, axis=1) / 2; n = n / np.maximum(2 * A, 1e-12)[:, None]
        D = {}
        for i in range(len(P)):
            ax = int(np.argmax(np.abs(n[i])))
            if abs(n[i][ax]) < 0.999: continue
            k = ("xyz"[ax], "+" if n[i][ax] > 0 else "-", round(P[i, 0, ax], 2))
            lo, hi = P[i].min(0), P[i].max(0)
            if k in D: D[k] = [np.minimum(D[k][0], lo), np.maximum(D[k][1], hi), D[k][2] + A[i]]
            else: D[k] = [lo, hi, A[i]]
        print("==", nd["name"])
        for k in sorted(D, key=lambda k: (k[0], k[2])):
            lo, hi, a = D[k]
            if a < 1: continue
            print("  %s%s %9.2f  alan %10.0f  x %.1f–%.1f y %.1f–%.1f z %.1f…%.1f" % (k[1], k[0], k[2], a, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
