import sys, numpy as np
S = r"C:/Users/Kemal/AppData/Local/Temp/claude/C--Users-Kemal-Desktop-Kemal-WEBS-TE/f3ef876a-f062-4b29-bb81-775cc8a1a6d8/scratchpad"
sys.path.insert(0, S + "/gece"); sys.path.insert(0, S)
from m8kit import Glb
g = Glb(S + "/hat3_v9h.glb")
def yakin(lo, hi, pre=None):
    lo = np.array(lo); hi = np.array(hi); r = {}
    for p in g.prims:
        if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
        if pre and not p["name"].startswith(pre): continue
        P = p["X"][p["T"]]; a = P.min(1); b = P.max(1)
        m = np.all(b >= lo, 1) & np.all(a <= hi, 1)
        if m.any():
            Q = P[m].reshape(-1, 3); r.setdefault(p["name"], []).append((m.sum(), Q.min(0).round(1), Q.max(0).round(1)))
    for k, v in sorted(r.items()):
        for x in v: print("  ", k, *x)
print("B derz 1"); yakin([2085, 735, 0], [2096, 780, 40])
print("B derz 2"); yakin([2085, 130, 0], [2096, 160, 40])
print("QR kablo"); yakin([4770, 445, 990], [4815, 460, 1010])
