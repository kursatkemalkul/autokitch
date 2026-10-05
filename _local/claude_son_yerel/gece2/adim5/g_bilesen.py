import sys, os, re, numpy as np, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_oku import GLB, bilesenler
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
G = GLB(os.path.join(S, "hat3_v8zq.glb"))
desen = re.compile(sys.argv[1]); birles = len(sys.argv) > 2
for ni, nd in enumerate(G.J["nodes"]):
    if "mesh" not in nd or not desen.search(nd.get("name", "")): continue
    for X, T, ex, ok in G.dugum_ucgen(ni):
        if not len(T): continue
        tl = bilesenler(X, T)
        R = []
        for c in np.unique(tl):
            Q = X[T[tl == c]].reshape(-1, 3); R.append((Q.min(0), Q.max(0), int((tl == c).sum())))
        R.sort(key=lambda r: (round(r[0][1]), round(r[0][0]), round(r[0][2])))
        print("== %s · %d bileşen · extras %s" % (nd["name"], len(R), {k: (v[:6] if isinstance(v, list) else v) for k, v in ex.items()}))
        for lo, hi, n in R:
            print("   x %8.1f–%8.1f  y %7.1f–%7.1f  z %7.1f…%7.1f  (%d)" % (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], n))
