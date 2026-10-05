"""bölge içindeki (GOVDE dışı) bileşenler: python g_yakin.py x0 x1 y0 y1 z0 z1 [haric_desen] [dahil_desen]"""
import sys, os, re, numpy as np, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_oku import GLB, bilesenler
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
ON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_bilesen_v8zq.pkl")
if not os.path.exists(ON):
    G = GLB(os.path.join(S, "hat3_v8zq.glb")); L = []
    for ni, nd in enumerate(G.J["nodes"]):
        if "mesh" not in nd: continue
        for X, T, ex, ok in G.dugum_ucgen(ni):
            if not len(T): continue
            tl = bilesenler(X, T)
            for c in np.unique(tl):
                Q = X[T[tl == c]].reshape(-1, 3); L.append((nd["name"], Q.min(0), Q.max(0), int((tl == c).sum())))
    pickle.dump(L, open(ON, "wb"))
L = pickle.load(open(ON, "rb"))
b = list(map(float, sys.argv[1:7])); har = re.compile(sys.argv[7]) if len(sys.argv) > 7 and sys.argv[7] else None
dah = re.compile(sys.argv[8]) if len(sys.argv) > 8 else None
lo = np.array(b[0::2]); hi = np.array(b[1::2])
for ad, a, z, n in sorted(L, key=lambda r: (r[0], r[1][1])):
    if har and har.search(ad): continue
    if dah and not dah.search(ad): continue
    if (a <= hi).all() and (z >= lo).all():
        print("%-42s x %7.1f–%7.1f y %7.1f–%7.1f z %7.1f…%7.1f (%d)" % (ad, a[0], z[0], a[1], z[1], a[2], z[2], n))
