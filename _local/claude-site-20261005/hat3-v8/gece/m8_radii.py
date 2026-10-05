import sys, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__file__))
from m8kit import Glb
g = Glb(sys.argv[1])
for spec in sys.argv[2:]:
    d, n, ax = spec.split(":"); b = g.bilesen(d, int(n)); ax = int(ax)
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)
    u, w = [i for i in range(3) if i != ax]
    c = ((b["lo"] + b["hi"]) / 2)[[u, w]]
    r = np.hypot(P[:, u] - c[0], P[:, w] - c[1])
    print(spec, "merkez", c.round(2), "r:", np.unique(r.round(2))[:12], "...", np.unique(r.round(2))[-4:])
