import sys, os, numpy as np
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
g = Glb(sys.argv[1]); c = np.array(list(map(float, sys.argv[2].split(",")))); r = float(sys.argv[3])
for d in sorted(set(p["name"] for p in g.prims)):
    try: g.bilesen(d, no=0)
    except Exception: continue
    for b in g._bc[d]:
        if np.all(b["hi"] > c - r) and np.all(b["lo"] < c + r): print("%-30s %4d lo %s hi %s" % (d, b["no"], np.round(b["lo"], 2), np.round(b["hi"], 2)))
