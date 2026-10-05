import sys, os, re, numpy as np, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_oku import GLB, bilesenler
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
G = GLB(os.path.join(S, "hat3_v8zq.glb"))
desen = re.compile(sys.argv[1])
print("sahne extras anahtarları:", list(G.J["scenes"][0].get("extras", {}).keys()))
for ni, nd in enumerate(G.J["nodes"]):
    if "mesh" not in nd or not desen.search(nd.get("name", "")): continue
    for X, T, ex, ok in G.dugum_ucgen(ni):
        if not len(T): continue
        P = X[T].reshape(-1, 3)
        print("%-40s %6d üçgen  x %.1f–%.1f y %.1f–%.1f z %.1f…%.1f" % (nd["name"], len(T), P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max(), P[:, 2].min(), P[:, 2].max()))
