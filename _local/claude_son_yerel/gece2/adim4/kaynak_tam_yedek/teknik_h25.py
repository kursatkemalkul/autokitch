# -*- coding: utf-8 -*-
"""HAT v2.5 ÖNERİ · Kemal: üst katta yalnız 2 UNO (sağda), nozullar yan yana, çöp + teneke kalkar, çekmeceler sağa. A 700 sabit."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
OUT = sys.argv[1]
plt.rcParams["font.family"] = "Arial"
K, G, R, M, YS = "#111111", "#8a8f96", "#d0021b", "#1f6feb", "#1e9e4a"
F1, F2, F3, FB = "#eef0f3", "#dfe3e8", "#f7e7c6", "#f4f9ff"
Y_PL, Y_DUZ, Y_MEK, H_IST, H_UST = 123.0, 788.0, 892.0, 1862.0, 2200.0
X0E = 507.5
X0, XA1, XC1, XF1, XK1, XE1 = 736.0, 1436.0, 2500.0, 4000.0, 4400.0, 5230.0
P = X0 + 350.0
fig = plt.figure(figsize=(24, 11), dpi=110)
ax = fig.add_axes([0.02, 0.04, 0.96, 0.9]); ax.set_aspect("equal"); ax.axis("off")


def kutu(x0, x1, y0, y1, fc=F1, ec=K, lw=1.2, ls="-", z=2, hatch=None):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z, hatch=hatch))


def yaz(x, y, t, s=9, c=K, ha="center", va="center", w="normal", rot=0):
    ax.text(x, y, t, fontsize=s, color=c, ha=ha, va=va, fontweight=w, rotation=rot, zorder=9)


def ox(x0, x1, y, t, c=M, s=9, dy=30.0, ext=None):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=c, lw=0.9, shrinkA=0, shrinkB=0), zorder=8)
    if ext is not None:
        for xx in (x0, x1): ax.plot([xx, xx], [ext, y], color=c, lw=0.5)
    if t: yaz((x0 + x1) / 2, y + dy, t, s, c)


def oy(x, y0, y1, t, c=M, s=9):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=c, lw=0.9, shrinkA=0, shrinkB=0), zorder=8)
    yaz(x - 25, (y0 + y1) / 2, t, s, c, ha="right")


def hazne(xc, w, y0, h, koni):
    ax.add_patch(Polygon([(xc - 32, y0), (xc + 32, y0), (xc + w / 2, y0 + koni), (xc + w / 2, y0 + h), (xc - w / 2, y0 + h), (xc - w / 2, y0 + koni)],
                         closed=True, fc=F3, ec=K, lw=1.0, zorder=4))


ax.plot([X0E - 150, XE1 + 150], [0, 0], color=K, lw=1.6)
kutu(X0E, X0, 0, H_UST, fc="none", ec=R, lw=1.0, ls=(0, (5, 4)), z=1, hatch="//")
yaz((X0E + X0) / 2, 2280, "kalkan\n228,5", 9, R, w="bold")
# ---------------- DOLAP (çöp + teneke yok, hepsi sağa) ----------------
kutu(X0, XK1, 0, Y_PL, fc=F2, lw=0.8)
kutu(X0, XK1, Y_PL, Y_DUZ, fc=F1, lw=1.4, ec=R)
S5 = [126, 296.5, 404.5, 512.5, 620.5, 785]; S4 = [126, 296.5, 404.5, 512.5, 785]; S3 = [126, 342.5, 505.5, 785]
KOL = [("K1", 798.5, 1418.5, S5, ["lahmacun"] * 5), ("K2", 1453.5, 2073.5, S5, ["lahmacun"] * 5),
       
       ("K3", 2108.5, 2728.5, S4, ["pide"] * 4), ("K5", 2763.5, 3383.5, S4, ["pide", "pide", "pide", "tatlı"]),
       ("K6", 3418.5, 4003.5, S3, ["içecek"] * 3), ("KD", 4038.5, 4398.5, [126, 330, 785], ["2 · sucuk\nyedeği 2 gün", "1 · kaşar\nyedeği 2 gün"])]
for kod, a0, a1, sira, ic in KOL:
    for i, t in enumerate(ic):
        kutu(a0, a1, sira[i] + 1.5, sira[i + 1] - 1.5, fc="#ffffff", ec=R, lw=0.9, z=3)
        yaz((a0 + a1) / 2, (sira[i] + sira[i + 1]) / 2 - (10 if i == len(ic) - 1 else 0), t, 7.5, G if t != "boş" else "#bbbbbb")
    yaz(a0 + 25, sira[-1] - 38, kod, 10, R, ha="left", w="bold")
    ox(a0, a1, Y_PL - 45, "%.1f" % (a1 - a0) if (a1 - a0) % 1 else "%d" % (a1 - a0), M, 7.5, dy=18)
ax.plot([XF1, XF1], [Y_PL, Y_DUZ], color=G, lw=0.7, ls=":")
ax.plot([XC1, XC1], [Y_PL, Y_DUZ], color=G, lw=0.7, ls=":")
# ---------------- A (700, değişmez) ----------------
kutu(X0, XA1, Y_DUZ, H_IST); kutu(X0, XA1, Y_DUZ, Y_MEK, fc=F2, lw=0.8)
yaz(P, 1500, "A\nAÇICI\n700 (aynı)", 11, K, w="bold")
kutu(P - 160, P + 153, 978, 1000, fc="#b9bec6", lw=0.7, z=4)
kutu(X0, XA1, H_IST, H_UST, fc="#f3f4f6", lw=1.0)
# ---------------- TOPPING 1294–2500 ----------------
kutu(XA1, XC1, Y_DUZ, H_UST, lw=1.4); ax.plot([XA1, XA1], [Y_DUZ, H_UST], color=R, lw=2.0, zorder=6)
kutu(XA1, XC1, Y_DUZ, Y_MEK, fc=F2, lw=0.8); yaz(1900, 840, "kaide · soğutma grubu", 7.5, G)
kutu(XA1 + 60, 2440, 1152, 2140, fc=FB, lw=0.9)
kutu(XA1 + 60, 2440, 1572, 1575, fc=K, lw=0.5, z=5)
# üst kat: YALNIZ 2 UNO (sağda)
for xc in (1880.0, 2215.0):
    kutu(xc - 41, xc + 41, 1575, 1647, fc="#c9ced6", lw=0.8, z=4); kutu(xc - 32, xc + 32, 1647, 1707, fc="#c9ced6", lw=0.6, z=4)
hazne(1880.0, 220.0, 1707.0, 285.0, 130.0); hazne(2215.0, 440.0, 1707.0, 380.0, 190.0)
yaz(1880, 1935, "sos\n2 gün\n17 L", 8, R); yaz(2215, 2030, "harç · 2 gün · 51 L", 8.5, R)
yaz(1630, 1850, "boş", 9, G)
# alt kat (aynı)
for xc in (1596.0, 1806.0):
    kutu(xc - 41, xc + 41, 1152, 1225, fc="#c9ced6", lw=0.8, z=4); kutu(xc - 30, xc + 30, 1225, 1284, fc="#c9ced6", lw=0.5, z=4)
hazne(1596.0, 190.0, 1284.0, 215.0, 120.0); hazne(1806.0, 190.0, 1284.0, 215.0, 120.0)
yaz(1596, 1420, "kıyma", 7.5); yaz(1806, 1420, "kuşbaşı", 7.5)
kutu(1922, 2202, 1152, 1504, fc=F3, lw=0.9, z=4); yaz(2062, 1330, "kaşar\nkaseti", 8)
kutu(2241, 2381, 1152, 1504, fc=F3, lw=0.9, z=4); yaz(2311, 1330, "küp\nsucuk", 8)
# hortumlar: UNO'dan önden dik iner, yayıcılar diğer nozulların yanında
ax.plot([1880, 1880, 1930, 1930], [1612, 1560, 1520, 1050], color=YS, lw=3.0, zorder=6)
ax.plot([2215, 2215, 2160, 2160], [1612, 1560, 1520, 1050], color=YS, lw=3.0, zorder=6)
# nozullar tabla üstünde yan yana
for x_, c_, t_ in ((1596, "#8a6a2a", "kıyma"), (1806, "#8a6a2a", "kuşbaşı"), (1930, YS, "sos"), (2062, "#8a6a2a", "kaşar"), (2160, YS, "harç"), (2311, "#8a6a2a", "sucuk")):
    kutu(x_ - 18, x_ + 18, 1014, 1060, fc=c_, ec=K, lw=0.6, z=6)
    yaz(x_, 955, "%s\n%d" % (t_, x_), 7, c_ if c_ == YS else K, va="top")
kutu(P - 250, 2495, 990, 1000, fc="#b9bec6", ec=G, lw=0.5, z=3)
yaz(2100, 1110, "TOPPING · İKİ KAT", 10, K, w="bold")
# ---------------- F · K · E ----------------
kutu(XC1, XF1, Y_DUZ, H_IST); kutu(XC1, XF1, Y_DUZ, 1305, fc=F2, lw=0.8); yaz(3250, 1050, "F · FIRIN", 12, K, w="bold")
kutu(2520, 3324, 1348, 1840, fc=F3, lw=0.8, z=3); yaz(2922, 1600, "pizza kutusu yedeği 320", 8)
kutu(3600, 3980, 1348, 1838, fc="#c9d8e8", lw=0.8, z=3); yaz(3790, 1600, "kompresör", 8)
kutu(XC1, XF1, H_IST, H_UST, fc="#f3f4f6", lw=1.0); kutu(2920, 3280, H_IST, H_UST, fc="#fff", ec=G, lw=0.8, z=3); yaz(3100, 2031, "baca", 7, G)
kutu(XF1, XK1, Y_DUZ, H_IST); yaz(4200, 1330, "K\nKESME", 11, K, w="bold")
yaz(4218, 820, "teneke + tartı\n(arkada)", 7.5, R)
kutu(XK1, XE1, Y_PL, H_IST); yaz(4815, 1330, "E\nKUTU", 12, K, w="bold")
kutu(4410, 5220, 130, 515, fc=F2, ec=G, lw=0.8, z=3); yaz(4815, 322, "dolap soğutma grubu + B panosu", 7.5, G)
kutu(XF1, XE1, H_IST, H_UST, fc="#f3f4f6", lw=1.0)
for j in range(3): kutu(4010 + j * 405, 4410 + j * 405, H_IST + 33, H_IST + 156, fc=F3, lw=0.7, z=4)
yaz(4615, H_UST - 55, "üst depo · içecek yedeği 6 koli", 7.5)
# ---------------- ölçüler ----------------
for a, b, t, c in ((X0, XA1, "A 700", M), (XA1, XC1, "TOPPING 1064", R), (XC1, XF1, "F 1500", M), (XF1, XK1, "K 400", M), (XK1, XE1, "E 830", M)):
    ox(a, b, H_UST + 95, t, c, 9.5, ext=H_UST)
ox(X0, XE1, -150, "HAT 4494   (v2.1: 4722,5 → −228,5)", R, 11, dy=-45, ext=0)
oy(X0E - 60, 0, H_UST, "2200")
ax.set_xlim(300, 5500); ax.set_ylim(-330, 2560)
yaz(300, 2555, "HAT v2.5 ÖNERİ · ÖN GÖRÜNÜŞ", 13, K, ha="left", va="top", w="bold")
yaz(300, 2485, "kırmızı = v2.1'e göre değişen · TOPPING sol duvarı kıymanın dibinde · kaşar / sucuk yedeği + teneke K altında · çöp yok · ölçüler mm", 9, G, ha="left", va="top")
fig.savefig(OUT, dpi=110, facecolor="white")
print("ok")
