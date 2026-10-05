import os, sys, numpy as np
sys.path.insert(0, os.path.abspath('../..'))
import govde_denetim_dogru as G
D = G.glb_oku(sys.argv[1])
for ad, cx, cz in (("TOPPING_MODUL__pom[15]", 2088.5, -150.0), ("TOPPING_MODUL__conta[7]", 2088.5, -150.0), ("TOPPING_MODUL__pom[16]", 2360.5, -152.5), ("TOPPING_MODUL__conta[6]", 2360.5, -152.5)):
    nd, no = ad[:-1].split("["); b = [b for b in G.bilesenler(nd, D[nd]) if b.no == int(no)][0]
    V = b.V; r = np.hypot(V[:, 0] - cx, V[:, 2] - cz)
    m = r < 31
    u, c = np.unique(np.round(r[m], 2), return_counts=True)
    print(ad, np.round(b.lo,1).tolist(), list(zip(u.tolist(), c.tolist()))[:40])
