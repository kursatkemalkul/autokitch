# Madde 6 taramasi: kapak (kpk) arkasinda / onunde duran, kpk etiketsiz kucuk parcalar
import sys, numpy as np
sys.path.insert(0, r"@@KOK_W@@\gece")
import glbkit
G = glbkit.Glb(sys.argv[1])
KAP = []   # kapak bilesenleri (buyuk, kpk)
ADAY = []
for p in G.prims:
    vis = G.gorunur(p)
    if not vis.any(): continue
    tl, kut = G.komp(p); kp = G.kpk_maske(p)
    for i, (a, b, n) in kut.items():
        m = (tl == i) & vis; k = kp[m].mean()
        d = b - a
        if k > 0.5 and d[0] > 150 and d[1] > 100: KAP.append((p['name'], a, b))
        if k < 0.5 and d.max() <= 70 and b[2] > 15 and b[2] < 200:
            ADAY.append((p['name'], a, b, n))
print(len(KAP), 'kapak bileseni', len(ADAY), 'aday')
for nm, a, b, n in ADAY:
    for kn, ka, kb in KAP:
        if a[0] >= ka[0] - 30 and b[0] <= kb[0] + 30 and a[1] >= ka[1] - 30 and b[1] <= kb[1] + 30 and b[2] > ka[2] - 25 and a[2] < kb[2]:
            print("%-38s x %7.1f %7.1f y %7.1f %7.1f z %6.1f %6.1f n%4d  <- %s z %.0f..%.0f" % (nm, a[0], b[0], a[1], b[1], a[2], b[2], n, kn, ka[2], kb[2]))
            break
