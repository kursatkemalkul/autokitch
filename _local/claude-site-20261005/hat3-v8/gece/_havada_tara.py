# Kapaklar gizliyken (kpk ucgenleri yok sayilarak) baska hicbir seye degmeyen kucuk parcalar.
# kullanim: python _havada_tara.py glb x0 x1 y0 y1 z0 z1 [maxboyut]
import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece")
import glbkit
G = glbkit.Glb(sys.argv[1])
R = list(map(float, sys.argv[2:8])); MX = float(sys.argv[8]) if len(sys.argv) > 8 else 120.0
LO, HI, OWN = [], [], []
ADAY = []
for pid, p in enumerate(G.prims):
    vis = G.gorunur(p)
    if not vis.any(): continue
    kp = G.kpk_maske(p); ok = vis & ~kp
    P = p['X'][p['T'][ok]]
    lo = P.min(1); hi = P.max(1)
    sel = (hi[:, 0] >= R[0] - 200) & (lo[:, 0] <= R[1] + 200) & (hi[:, 1] >= R[2] - 200) & (lo[:, 1] <= R[3] + 200) & (hi[:, 2] >= R[4] - 200) & (lo[:, 2] <= R[5] + 200)
    if not sel.any(): continue
    tl, kut = G.komp(p)
    tlo = tl[ok]
    LO.append(lo[sel]); HI.append(hi[sel]); OWN.append(np.stack([np.full(sel.sum(), pid), tlo[sel]], 1))
    for i, (a, b, n) in kut.items():
        if (b - a).max() > MX: continue
        if a[0] < R[0] or b[0] > R[1] or a[1] < R[2] or b[1] > R[3] or a[2] < R[4] or b[2] > R[5]: continue
        m = (tl == i) & vis
        if kp[m].mean() > 0.5: continue
        ADAY.append((pid, i, a, b, n))
LO = np.vstack(LO); HI = np.vstack(HI); OWN = np.vstack(OWN)
print(len(ADAY), 'aday ·', len(LO), 'ucgen')
e = 0.6
for pid, i, a, b, n in ADAY:
    m = (HI[:, 0] >= a[0] - e) & (LO[:, 0] <= b[0] + e) & (HI[:, 1] >= a[1] - e) & (LO[:, 1] <= b[1] + e) & (HI[:, 2] >= a[2] - e) & (LO[:, 2] <= b[2] + e)
    m &= ~((OWN[:, 0] == pid) & (OWN[:, 1] == i))
    if not m.any():
        print("HAVADA %-38s x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f n%d" % (G.prims[pid]['name'], a[0], b[0], a[1], b[1], a[2], b[2], n))
