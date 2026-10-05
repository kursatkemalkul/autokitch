# -*- coding: utf-8 -*-
"""menu7 · onden yerlesim semasi (dunya mm, v9t olculeri + oneri). Salt okuma, modele dokunmaz."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

fig, ax = plt.subplots(figsize=(12, 12.6), dpi=130)
GRI, KOYU, YESIL, KIR, MAVI = "#c9ced6", "#3a3f47", "#1f9d4c", "#d62828", "#2b6cb0"

def kutu(x0, x1, y0, y1, **k): ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **k))
def hazne(x0, x1, yb, yt, ny, nx0, nx1, renk, ad, alt_yazi, tx=None):
    kutu(x0, x1, yb, yt, fc=renk, ec=KOYU, lw=1.2)
    ax.add_patch(Polygon([(x0, yb), (x1, yb), (nx1, ny), (nx0, ny)], fc=renk, ec=KOYU, lw=1.2))
    tx = (x0 + x1) / 2 if tx is None else tx
    ax.text(tx, yt - 22, ad, ha="center", va="top", fontsize=10.5, weight="bold", color=KOYU)
    ax.text(tx, yt - 52, alt_yazi, ha="center", va="top", fontsize=8.3, color=KOYU, linespacing=1.25)
def valf(c, y0, y1):
    kutu(c - 41, c + 41, y0, y1, fc="#aeb4bd", ec=KOYU, lw=0.8)
    kutu(c - 91, c - 41, y0 + 16, y0 + 60, fc="#d9dde3", ec=KOYU, lw=0.6)
def hortum(pts, renk=YESIL, lw=5.5):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=renk, lw=lw, solid_capstyle="butt", solid_joinstyle="round", zorder=5)

# soguk oda ic hacmi + raflar
kutu(1496, 2440, 1152, 2139, fc="#f4f6f8", ec=KOYU, lw=2)
kutu(1496, 2440, 1534, 1575, fc="#8d949e", ec=KOYU, lw=1)                       # ust raf (bukumlu)
kutu(1496, 2440, 1109, 1152, fc="#8d949e", ec=KOYU, lw=1)                       # alt taban / raf
ax.text(2448, 1555, "üst raf\n1534–1575", fontsize=7.5, va="center", color=KOYU)
ax.text(2448, 1130, "taban\n1109–1152", fontsize=7.5, va="center", color=KOYU)
ax.text(2448, 2139, "tavan 2139", fontsize=7.5, va="center", color=KOYU)

# arka (kuru bolme) evaporatorler - kesik cizgi
for (x0, x1, y0, y1, ad) in [(1446, 1670, 1282, 1682, "EVAP L (arkada)"), (1758, 2223, 1383, 1835, "EVAP R (arkada)")]:
    kutu(x0, x1, y0, y1, fill=False, ec=KIR, lw=1.3, ls=(0, (6, 4)), zorder=8)
    ax.text(x0 + 6, y1 - 8, ad, fontsize=7.5, color=KIR, va="top", zorder=8)
kutu(1807, 2174, 1582, 1786, fill=False, ec=KIR, lw=0.8, ls=":", zorder=8)
ax.text(2170, 1790, "R üfleme ağzı", fontsize=6.5, color=KIR, ha="right", va="bottom", zorder=8)

# UST SIRA
hazne(1532, 1912, 1887, 2099, 1707, 1690, 1754, "#f2d0a9", "LAHMACUN HARCI", "380 · brüt 47,0 L\n2 gün 42,0 L  ⚠ sınırda\n(+30 mm → 52,1 L)")
hazne(1931, 2131, 1887, 2099, 1707, 1999, 2063, "#fbe7a1", "PATATES PÜRESİ", "YENİ 200 · brüt 25,1 L\n2 gün 5,7 L  ✓")
hazne(2149.5, 2369.5, 1887, 1992, 1707, 2228, 2291, "#e8b4b0", "KIYMA", "220 · brüt 17,2 L\n2 gün 3,0 L  ✓")
for c in (1722, 2031, 2259.5): valf(c, 1575, 1648); kutu(c - 32, c + 32, 1648, 1707, fc="#d9dde3", ec=KOYU, lw=0.6)
# ALT SIRA
hazne(1501, 1691, 1464, 1499, 1284, 1565, 1627, "#f6d6c8", "TAVUK", "190 · 9,1 L\n2 gün 6,8 L ✓")
hazne(1753, 1943, 1464, 1499, 1284, 1817, 1879, "#e9c2a6", "KUŞBAŞI", "190 · 8,5 L*\n2 gün 3,4 L ✓", tx=1812)
kutu(1879, 1943, 1410, 1499, fc="white", ec=YESIL, lw=1, hatch="////", zorder=4)
ax.plot([1879, 1879], [1284 + 0, 1499], color=YESIL, lw=1, ls="--", zorder=4)
for c in (1596, 1848): valf(c, 1152, 1225); kutu(c - 32, c + 32, 1225, 1284, fc="#d9dde3", ec=KOYU, lw=0.6)
# kasetler
kutu(1948, 2228, 1152, 1504, fc="#dbe9f6", ec=MAVI, lw=1.3)
ax.add_patch(Circle((2088, 1330), 70, fill=False, ec=MAVI, lw=1)); ax.text(2088, 1460, "KAŞAR kaseti", ha="center", fontsize=10, weight="bold", color=MAVI)
ax.text(2088, 1225, "8,8 kg · 2 gün 4,4 kg ✓", ha="center", fontsize=8, color=MAVI)
kutu(2290, 2430, 1152, 1504, fc="#dbe9f6", ec=MAVI, lw=1.3)
ax.text(2360, 1460, "SUCUK", ha="center", fontsize=10, weight="bold", color=MAVI)
ax.text(2360, 1225, "2,8 kg\n2 gün 1,4 kg ✓", ha="center", fontsize=8, color=MAVI)

# pnomatik silindirler (arkada, kuru bolme)
for (c, r) in [(1722, KOYU), (2259.5, KOYU), (2031, KIR)]:
    kutu(c - 19, c + 19, 1595, 1632, fc=r, ec=r, alpha=0.85, zorder=9)
ax.annotate("3. UNO pnömatik silindiri\nEVAP R'nin İÇİNE düşüyor\n(x 2012–2050 · y 1595–1632)", xy=(2050, 1614), xytext=(2452, 1690),
            fontsize=7.8, color=KIR, arrowprops=dict(arrowstyle="->", color=KIR), zorder=10)

# hortumlar
hortum([(1722, 1575), (1722, 1216)])                                  # harc (dik)
hortum([(2259.5, 1575), (2259.5, 1216)])                              # ust sag (dik)
hortum([(2031, 1613), (1911.5, 1613), (1911.5, 1152)])                # 3. UNO: rafin ustunde sola, sonra dik
for x in (1722, 2259.5, 1911.5, 1596, 1848, 2088, 2360):
    ax.plot([x, x], [1109, 1010], color=YESIL if x in (1722, 2259.5, 1911.5) else "#888", lw=1.2, ls=":")
ax.annotate("D42 hortum\nkuşbaşı ↔ kaşar arası\n64,9 mm boşluk (≥ 62 ✓)", xy=(1905, 1180), xytext=(1505, 1060),
            fontsize=7.6, color=YESIL, arrowprops=dict(arrowstyle="->", color=YESIL), zorder=10)
ax.text(1772, 1652, "rafın üstünde\npaslanmaz dirsek", fontsize=7, color=YESIL, va="bottom")

# tabla yolu
ax.plot([1430, 2500], [1000, 1000], color="#b08900", lw=2.5)
ax.text(1435, 985, "tabla / hamur yolu (y ≈ 1000, z −170) — tüm düşme noktaları bunun üstünde", fontsize=7.8, color="#b08900", va="top")

ax.text(1496, 2185, "TOPPING · YENİ MENÜ (PİDE + LAHMACUN) · ÖNDEN ŞEMA", fontsize=13, weight="bold", color=KOYU)
ax.text(1496, 2160, "v9t ölçüleri (dünya mm) · hacimler brüt · 2 gün = 80 pide + 200 lahmacun/gün varsayımı · SOS UNO'SU YOK", fontsize=8.5, color=KOYU)
ax.text(1496, 925, "* kuşbaşı: hortum için yalnız ÖN-SAĞ köşe cebi (taralı, 64 × 81 × 89) → 8,5 L · Kemal'in çizdiği tam dik kenar (yeşil kesik) → 6,1 L\n"
        "kırmızı kesik = arkadaki evaporatörler (kuru bölme) · koyu küçük kutu = UNO pnömatik silindiri (arkada)", fontsize=7.8, color=KOYU, va="top")
ax.set_xlim(1420, 2640); ax.set_ylim(880, 2210); ax.set_aspect("equal"); ax.axis("off")
plt.tight_layout(); plt.savefig("yerlesim.png", dpi=130, facecolor="white")
print("ok")
