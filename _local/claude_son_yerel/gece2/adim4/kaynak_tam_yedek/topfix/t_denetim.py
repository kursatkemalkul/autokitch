# -*- coding: utf-8 -*-
"""TOPFIX ek denetimler (npz onbellek, tam donusum): python t_denetim.py zc_dizini cikti.txt
 1 silindir <-> evaporator x bosluklari · 2 acik PU (raster) · 3 kaset onden cekme supurmesi · 4 UNO hunisi cikarma payi · 5 hortum dikligi + bosluk
 6 A ici tarama (A/Govde + A/Acici + tabla gecisi disinda bir sey var mi; kablo/kanal/rakor/kelepce/hortum/sensor)"""
import sys, json, numpy as np
from scipy import ndimage
d, out = sys.argv[1:3]
D = np.load(d + "/m8_onbellek.npz"); J = json.load(open(d + "/m8_parca.json", encoding="utf-8"))
PJ, MEK, KAT = J["parca"], [m["kod"] for m in J["MEK"]], J["KAT"]
A, B, C, P, mek, kat, kpk = D["A"], D["B"], D["C"], D["P"], D["mek"], D["kat"], D["kpk"]
T = np.stack([A, B, C], 1); lo = T.min(1); hi = T.max(1)
AD = np.array([p["ad"] for p in PJ])
L = []
def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
def mk(k): return MEK.index(k)
def kutu(m):
    return lo[m].min(0), hi[m].max(0)
# ======================================================= 1
yaz("== 1 · UST UNO ARKA SILINDIR TAKIMI <-> EVAPORATOR KASETLERI (kuru bolme z < -629)")
ev = (AD[P] == "TOPPING_MODUL__sac") & (lo[:, 0] >= 1757.9) & (hi[:, 0] <= 2223.1) & (lo[:, 1] >= 1382.9) & (hi[:, 1] <= 1835.1) & (hi[:, 2] <= -639.9) & (lo[:, 2] >= -826.1)
el, eh = kutu(ev); yaz("   kasetler (dis sac) x %.1f-%.1f y %.1f-%.1f z %.1f-%.1f" % (el[0], eh[0], el[1], eh[1], el[2], eh[2]))
for u in ("TOPPING/Harç", "TOPPING/Sos"):
    m = (mek == mk(u)) & (hi[:, 2] < -629) & ~kpk
    l, h = kutu(m)
    yo = l[1] < eh[1] and h[1] > el[1]
    dx = (el[0] - h[0]) if h[0] <= el[0] + 1 else (l[0] - eh[0])
    yaz("   %-13s arka takim x %.1f-%.1f y %.1f-%.1f z %.1f-%.1f · y ortusme %s · net x boslugu %.1f mm %s" % (u, l[0], h[0], l[1], h[1], l[2], h[2], "VAR" if yo else "yok", dx, "TAMAM" if dx >= 10 - 0.05 else "YETERSIZ"))
# ======================================================= 2 acik PU
yaz("\n== 2 · ACIK PU (1 mm raster, kapaklar yok)")
TRI = np.where(~kpk)[0]
def raster(eks, isr, bas, ua_ar, va_ar, kut, h=1.0):
    ua, va = [a for a in (0, 1, 2) if a != eks]
    us = np.arange(ua_ar[0] + h / 2, ua_ar[1], h); vs = np.arange(va_ar[0] + h / 2, va_ar[1], h)
    zb = np.full((len(vs), len(us)), 1e18); kim = np.full((len(vs), len(us)), -1)
    dd_ = (T[:, :, eks] - bas) * isr
    m = (~kpk) & (dd_.max(1) > 0) & (hi[:, ua] > ua_ar[0]) & (lo[:, ua] < ua_ar[1]) & (hi[:, va] > va_ar[0]) & (lo[:, va] < va_ar[1])
    for kk in range(3): m &= (hi[:, kk] >= kut[2 * kk]) & (lo[:, kk] <= kut[2 * kk + 1])
    for i in np.where(m)[0]:
        tri = T[i]; P2 = tri[:, [ua, va]]; Dd = (tri[:, eks] - bas) * isr
        (x0, y0), (x1, y1), (x2, y2) = P2
        dd = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(dd) < 1e-9: continue
        ix = np.where((us >= P2[:, 0].min()) & (us <= P2[:, 0].max()))[0]; iy = np.where((vs >= P2[:, 1].min()) & (vs <= P2[:, 1].max()))[0]
        if not len(ix) or not len(iy): continue
        XX, YY = np.meshgrid(us[ix], vs[iy])
        a = ((y1 - y2) * (XX - x2) + (x2 - x1) * (YY - y2)) / dd; b = ((y2 - y0) * (XX - x2) + (x0 - x2) * (YY - y2)) / dd; c = 1 - a - b
        ins = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6); Z = a * Dd[0] + b * Dd[1] + c * Dd[2]; ins &= Z > 0
        sub = zb[np.ix_(iy, ix)]; ks = kim[np.ix_(iy, ix)]; yeni = ins & (Z < sub - 1e-4)
        sub[yeni] = Z[yeni]; ks[yeni] = i; zb[np.ix_(iy, ix)] = sub; kim[np.ix_(iy, ix)] = ks
    isPU = np.array(["__pu" in AD[P[i]] for i in range(0)])
    ac = (kim >= 0) & np.vectorize(lambda i: i >= 0 and "__pu" in AD[P[i]])(kim)
    lab, n = ndimage.label(ac); bol = []
    for j in range(1, n + 1):
        w = np.where(lab == j); bol.append((len(w[0]), us[w[1]].min(), us[w[1]].max(), vs[w[0]].min(), vs[w[0]].max()))
    bol.sort(key=lambda r: -r[0]); return int(ac.sum()), bol, "xyz"[ua], "xyz"[va]
INF = 1e9
GOR = [("onden (kapaklar yok)", 2, -1, 200.0, (1430, 2505), (1040, 2205), (-INF, INF, -INF, INF, -INF, INF)),
       ("oda icinden sola (x 2000 -> -x)", 0, -1, 2000.0, (1152.5, 2139.5), (-569.5, 36.5), (-INF, INF, 1100, 2200, -640, 40)),
       ("oda icinden saga (x 1700 -> +x)", 0, +1, 1700.0, (1152.5, 2139.5), (-569.5, 36.5), (-INF, INF, 1100, 2200, -640, 40)),
       ("oda icinden arkaya (z 0 -> -z)", 2, -1, 0.0, (1496.5, 2439.5), (1152.5, 2139.5), (1430, 2510, 1100, 2200, -INF, INF)),
       ("oda icinden asagi (y 2100 -> -y)", 1, -1, 2100.0, (1496.5, 2439.5), (-569.5, 36.5), (1430, 2510, -INF, INF, -640, 40)),
       ("oda icinden yukari (y 1160 -> +y)", 1, +1, 1160.0, (1496.5, 2439.5), (-569.5, 36.5), (1430, 2510, -INF, INF, -640, 40)),
       ("kuru bolmeden one (z -827 -> +z, evap)", 2, +1, -827.0, (1440, 2497), (1112, 2196), (1430, 2510, 1100, 2200, -INF, -629.0)),
       ("A'nin icinden saga (x 1180 -> +x)", 0, +1, 1180.0, (895, 2197), (-827, 57), (-INF, INF, 890, 2200, -830, 60))]
for ad, eks, isr, bas, ua, va, kut in GOR:
    n, bol, un, vn = raster(eks, isr, bas, ua, va, kut)
    yaz("   %-40s acik PU %6d mm2 · %d bolge %s" % (ad, n, len(bol), "" if not bol else "· " + "; ".join("%d mm2 %s %.0f-%.0f %s %.0f-%.0f" % (r[0], un, r[1], r[2], vn, r[3], r[4]) for r in bol[:5])))
# ======================================================= 3 kaset cekme
yaz("\n== 3 · KASET ONDEN CEKME SUPURMESI (+z 300, govde y >= 1152,5)")
for u in ("TOPPING/Kaşar", "TOPPING/Sucuk"):
    own = (mek == mk(u)) & (lo[:, 1] >= 1152.5) & (lo[:, 2] >= -560)
    l, h = kutu(own)
    # kilavuz disindaki govde (x 4,5 ic)
    sl = np.array([l[0] + 4.8, 1152.6, l[2]]); sh = np.array([h[0] - 4.8, h[1], h[2] + 300])
    m = (~kpk) & (mek != mk(u)) & np.all(hi > sl, 1) & np.all(lo < sh, 1)
    ps = sorted(set(P[m]))
    if not ps: yaz("   %-14s x %.1f-%.1f y %.1f-%.1f z %.1f..+300: yol TEMIZ" % (u, sl[0], sh[0], sl[1], sh[1], sl[2]))
    for p in ps: yaz("   %-14s YOLDA %s %s %s %s" % (u, PJ[p]["ad"], MEK[PJ[p]["mek"]], PJ[p]["lo"], PJ[p]["hi"]))
# ======================================================= 4 UNO huni
yaz("\n== 4 · UNO HUNI CIKARMA (hazne kutusu -> ust / yan bosluk, on agiz x 1496-2440)")
for u, ylo, ust in (("TOPPING/Kıyma", 1279.0, 1534.0), ("TOPPING/Kuşbaşı", 1279.0, 1534.0), ("TOPPING/Harç", 1706.0, 2140.0), ("TOPPING/Sos", 1706.0, 2140.0)):
    m = (mek == mk(u)) & (lo[:, 1] >= ylo) & (lo[:, 2] > -600); l, h = kutu(m)
    yan = (~kpk) & (mek != mk(u)) & (hi[:, 1] > l[1]) & (lo[:, 1] < h[1]) & (hi[:, 2] > l[2]) & (lo[:, 2] < h[2]) & (lo[:, 2] > -600)
    sol = yan & (hi[:, 0] <= l[0] + 0.5); sag = yan & (lo[:, 0] >= h[0] - 0.5)
    ds = l[0] - hi[sol, 0].max() if sol.any() else 999; dr = lo[sag, 0].min() - h[0] if sag.any() else 999
    yaz("   %-15s hazne x %.1f-%.1f y %.1f-%.1f · ust bosluk %.1f · sol %.1f · sag %.1f · on agiz icinde %s" % (u, l[0], h[0], l[1], h[1], ust - h[1], ds, dr, "EVET" if l[0] >= 1496 and h[0] <= 2440 else "HAYIR"))
# ======================================================= 5 hortum
yaz("\n== 5 · UST UNO HORTUMLARI (D32 dis 42)")
for u, x in (("TOPPING/Harç", 1722.0), ("TOPPING/Sos", 2259.5)):
    m = (mek == mk(u)) & (AD[P] == "TOPPING_MODUL__hortum_gida"); l, h = kutu(m)
    yaz("   %-13s hortum x %.1f-%.1f y %.1f-%.1f z %.1f-%.1f · eksen %.1f · dik (x/z genislik %.1f/%.1f = cap)" % (u, l[0], h[0], l[1], h[1], l[2], h[2], (l[0] + h[0]) / 2, h[0] - l[0], h[2] - l[2]))
    ban = (~kpk) & (mek != mk(u)) & (hi[:, 1] > 1216) & (lo[:, 1] < 1539) & (hi[:, 2] > l[2]) & (lo[:, 2] < h[2]) & (hi[:, 0] > x - 120) & (lo[:, 0] < x + 120)
    ban &= ~np.isin(AD[P], ["TOPPING_MODUL__paslanmaz"]) | (lo[:, 1] > 1152)
    sl = ban & (hi[:, 0] <= x); sr = ban & (lo[:, 0] >= x)
    yaz("   %-13s hortum bandinda (y 1216-1539) sol bosluk %.1f · sag bosluk %.1f mm · onunden gecen birim yok: %s" % (u, l[0] - hi[sl, 0].max(), lo[sr, 0].min() - h[0],
        "EVET" if not ((~kpk) & (mek != mk(u)) & (lo[:, 0] < h[0]) & (hi[:, 0] > l[0]) & (lo[:, 1] < 1539) & (hi[:, 1] > 1216) & (lo[:, 2] > h[2])).any() else "HAYIR"))
# ======================================================= 6 A ici
yaz("\n== 6 · A ICI TARAMA (x 737,5-1434,5 · y 893,5-2198,5 · z -828,5..59; kapaklar disinda)")
m = (~kpk) & (lo[:, 0] > 737.4) & (hi[:, 0] < 1434.6) & (lo[:, 1] > 893.4) & (hi[:, 1] < 2198.6) & (lo[:, 2] > -828.6) & (hi[:, 2] < 59.1)
from collections import Counter
c = Counter((MEK[mek[i]], KAT[kat[i]], AD[P[i]]) for i in np.where(m)[0])
for (a, b, n_), v in sorted(c.items()): yaz("   %-16s %-9s %-36s %6d ucgen" % (a, b, n_, v))
yasak = [k for k in c if k[1] in ("ELEKTRIK", "HAVA", "SENSOR", "KONTROL") or any(s in k[2] for s in ("kablo", "kanal", "rakor", "hava", "hortum"))]
yaz("   YASAK (kablo/kanal/rakor/kelepce/hava/sensor/kontrol) : %d tur %s" % (len(yasak), yasak))
tab = m & (mek == mk("TOPPING/Tabla")); l, h = kutu(tab)
yaz("   tabla gecis bolgesi A icinde: x %.1f-%.1f y %.1f-%.1f z %.1f-%.1f" % (l[0], h[0], l[1], h[1], l[2], h[2]))
open(out, "w", encoding="utf-8").write("\n".join(L))
