import sys, numpy as np, re
sys.path.insert(0, ".")
from ortam4 import Ortam, bolge
O = bolge(Ortam(), (700, -10, -900), (5500, 2300, 1300))
M = O.yapi
for a in sys.argv[1:]:
    v = [float(x) for x in a.split(",")]; lo, hi = v[:3], v[3:]
    c = O.kutu_kesis(lo, hi, M, e=0.1)
    nm = {}
    for i in c:
        q = nm.setdefault(O.nm[i], [0, O.lo[i].copy(), O.hi[i].copy()]); q[0] += 1; q[1] = np.minimum(q[1], O.lo[i]); q[2] = np.maximum(q[2], O.hi[i])
    print(a, "TEMİZ" if not nm else "")
    for k, (n, l, h) in nm.items(): print("    %-30s %4d %s %s" % (k, n, np.round(l, 1).tolist(), np.round(h, 1).tolist()))
