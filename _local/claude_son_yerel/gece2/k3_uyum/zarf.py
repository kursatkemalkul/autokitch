import sys, os, numpy as np, re
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
g = Glb(sys.argv[1])
D = {}
for p in g.prims:
    if p.get("gizli"): continue
    n = p["name"]
    if not re.match(r"^(A_GOVDE|KAIDE_|TOPPING_GOVDE|F_TP10_GOVDE|F_UST_KABIN|U_F_GOVDE|U_KE_GOVDE|K_GOVDE|E_GOVDE|B_KASA|B_MODULER|E_MODULER)__(sac|kabuk|cerceve|paslanmaz|celik)$", n): continue
    X = p["X"][np.unique(p["T"])]
    lo, hi = X.min(0), X.max(0)
    if n in D: D[n] = (np.minimum(D[n][0], lo), np.maximum(D[n][1], hi))
    else: D[n] = (lo, hi)
for n in sorted(D, key=lambda k: D[k][0][0]):
    lo, hi = D[n]; print("%-26s x %8.2f–%8.2f  y %8.2f–%8.2f  z %8.2f–%7.2f" % (n, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
