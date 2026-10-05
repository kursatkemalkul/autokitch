import sys, numpy as np
sys.path.insert(0, r"@@KOK_W@@\gece")
import glbkit
G = glbkit.Glb(sys.argv[1])
x0, x1, y0, y1, zmin = map(float, sys.argv[2:7])
for p in G.prims:
    X = p['X']; vis = G.gorunur(p)
    if not vis.any(): continue
    U = np.unique(p['T'][vis].reshape(-1)); V = X[U]
    if V[:, 0].max() < x0 or V[:, 0].min() > x1 or V[:, 2].max() < zmin: continue
    tl, kut = G.komp(p); kp = G.kpk_maske(p)
    for i, (a, b, n) in kut.items():
        d = b - a
        if d.max() <= 70 and a[0] >= x0 and b[0] <= x1 and a[1] >= y0 and b[1] <= y1 and b[2] >= zmin:
            m = (tl == i) & vis
            print("%-40s x %7.1f %7.1f y %7.1f %7.1f z %6.1f %6.1f n%4d kpk %d" % (p['name'], a[0], b[0], a[1], b[1], a[2], b[2], n, int(kp[m].mean() * 100)))
