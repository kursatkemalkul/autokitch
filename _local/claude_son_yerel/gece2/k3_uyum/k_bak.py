import sys, os, numpy as np, collections
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
g = Glb(sys.argv[1])
for d in sys.argv[2:]:
    g.bilesen(d, no=0); c = collections.Counter()
    for b in g._bc[d]:
        s = tuple(np.round(np.sort(b["hi"] - b["lo"]), 1))
        if s[2] < 40: c[s] += 1
    print(d, len(g._bc[d])); [print("  ", k, v) for k, v in sorted(c.items(), key=lambda kv: -kv[1])[:40]]
