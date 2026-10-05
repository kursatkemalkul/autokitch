import sys, os, re, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_oku import GLB
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
G = GLB(os.path.join(S, "hat3_v8zq.glb"))
# argv: dugum ax deger c1 c2 [c1 c2 ...]  (ax düzlemi; c1 c2 diğer iki eksen sırasıyla)
nd = sys.argv[1]; ax = "xyz".index(sys.argv[2]); val = float(sys.argv[3]); cs = list(map(float, sys.argv[4:]))
o = [i for i in range(3) if i != ax]
for ni, n in enumerate(G.J["nodes"]):
    if n.get("name") != nd: continue
    for X, T, ex, ok in G.dugum_ucgen(ni):
        V = X[np.unique(T)]; V = V[np.abs(V[:, ax] - val) < 0.02]
        for k in range(0, len(cs), 2):
            c = np.array(cs[k:k + 2]); d = np.linalg.norm(V[:, o] - c, axis=1); d = np.sort(d[d < 60])
            print("%s %s=%.1f merkez %s → en yakın köşeler %s" % (nd, sys.argv[2], val, c, np.round(d[:6], 2)))
