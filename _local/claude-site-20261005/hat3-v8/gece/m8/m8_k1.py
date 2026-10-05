from m8_ortak import *
import collections
gor = np.ones(N, bool)
der, lab, topr = grafik(gor)
print("etiketsiz parca", (pmek < 0).sum(), "kat yok", (pkat < 0).sum())
print("zemin y min", LO[:, 1].min())
print("== derece 0 ==")
for i in np.where(der == 0)[0]:
    t = tanim(i); print(("HARIC " if haric(i) else "") + "%s %s %s x%s y%s z%s n%d" % (t["dugum"], t["mek"], t["boyut"], t["x"], t["y"], t["z"], t["ucgen"]))
print("== topraksiz kumeler ==")
for k in np.where(~topr)[0]:
    u = np.where((lab == k))[0]
    if len(u) < 1 or (der[u] == 0).all() and len(u) == 1: continue
    hh = all(haric(i) for i in u)
    lo = LO[u].min(0); hi = HI[u].max(0)
    print(("HARIC " if hh else "") + "kume %d parca: %s x %.0f-%.0f y %.0f-%.0f z %.0f-%.0f" % (len(u), collections.Counter(PC[i]["ad"] for i in u).most_common(6), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
