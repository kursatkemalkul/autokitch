# -*- coding: utf-8 -*-
"""AÇICI ALANI · tedarikçi çizimi v2 (28 Eyl 2026) — Kemal: "robot itiyor falan diye yazma, hatta tek bir 3D çizim olsun, basitçe kare".
Tek izometrik kutu: ayrılan alan 700 × 909 × 967 (A kabini içi: x 0–700 · z −830…+79 · y 893,5…1860,5) + bizim çalışma diskimiz Ø340
(üstü 1000 → kutu tabanından 106,5; merkez ön yüzden 249) + diskin çıkış yönü. Ölçüler acici_kabin_cad_v1 + itici_cad_v5 (DISK_UST).
v1 (3 görünüş) yerinde kalır. Çıktı: FULL_MAKINE/ACICI_ALANI_v2.png
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
TR = "tr" in sys.argv                                # Türkçe etiketli kopya (Kemal okusun) → ACICI_ALANI_v2_TR.png
DL = (lambda en, tr: tr if TR else en)
OUT = os.path.join(os.path.dirname(U), "FULL_MAKINE", "ACICI_ALANI_v2_TR.png" if TR else "ACICI_ALANI_v2.png")
assert not os.path.exists(OUT), "v2 zaten var"
W, D, H = 700.0, 909.0, 967.0                       # genişlik · derinlik (arka duvar → ön yüz) · yükseklik
PX, PD, PY, PR, PT = 350.0, D - 249.0, 106.5, 170.0, 8.0   # disk merkezi x · arkadan d · kutu tabanından üst yüz · yarıçap · kalınlık
S, C30, S30 = 1.0, math.cos(math.radians(30)), 0.5
W_PX, H_PX = 2200, 2250
OX, OY = 1040, 1330                                  # (x=0, d=0, y=0) arka-sol-alt köşenin ekrandaki yeri
def P(x, d, y): return (OX + (x - d) * C30 * S, OY + ((x + d) * S30 - y) * S)

im = Image.new("RGB", (W_PX, H_PX), "white"); g = ImageDraw.Draw(im)
def F(n, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", n)
    except OSError:
        return ImageFont.load_default()
f22, f26, f34 = F(26), F(30), F(40, True)
INK, GRAY, BLUE, GRN = (20, 20, 24), (130, 130, 136), (20, 90, 200), (30, 130, 80)

def line(a, b, c=INK, w=3): g.line([P(*a), P(*b)], fill=c, width=w)
def dash(a, b, c=GRAY, w=2, on=16, off=10):
    pa, pb = P(*a), P(*b); L = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
    t = 0.0
    while t < L:
        t1 = min(L, t + on)
        g.line([(pa[0] + (pb[0] - pa[0]) * t / L, pa[1] + (pb[1] - pa[1]) * t / L), (pa[0] + (pb[0] - pa[0]) * t1 / L, pa[1] + (pb[1] - pa[1]) * t1 / L)], fill=c, width=w)
        t += on + off
def txt(p, s, f=f22, c=INK, a="mm"): g.text(p, s, font=f, fill=c, anchor=a)

# yüzler (açık mavi, görünen üç yüz)
g.polygon([P(0, D, 0), P(W, D, 0), P(W, D, H), P(0, D, H)], fill=(236, 244, 255))       # ön
g.polygon([P(W, D, 0), P(W, 0, 0), P(W, 0, H), P(W, D, H)], fill=(226, 237, 252))       # sağ
g.polygon([P(0, 0, H), P(W, 0, H), P(W, D, H), P(0, D, H)], fill=(245, 249, 255))       # üst
# gizli kenarlar (arka-sol-alt köşe)
for a, b in (((0, 0, 0), (W, 0, 0)), ((0, 0, 0), (0, D, 0)), ((0, 0, 0), (0, 0, H))):
    dash(a, b)
# disk (yatay daire → elips; önce alt kenar, sonra üst yüz)
def halka(y, n=120): return [P(PX + PR * math.cos(t), PD + PR * math.sin(t), y) for t in (2 * math.pi * i / n for i in range(n))]
g.polygon(halka(PY - PT), fill=(150, 154, 162))
g.polygon(halka(PY), fill=(200, 204, 212), outline=INK)
g.polygon([P(PX + 140 * math.cos(t), PD + 140 * math.sin(t), PY) for t in (2 * math.pi * i / 120 for i in range(120))], outline=GRN)
# disk çıkış oku (sağa, x +)
a0, a1 = P(PX + PR + 30, PD, PY + 4), P(W + 120, PD, PY + 4)
g.line([a0, a1], fill=GRN, width=6)
ux, uy = (a1[0] - a0[0]), (a1[1] - a0[1]); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
g.polygon([(a1[0] + ux * 26, a1[1] + uy * 26), (a1[0] - uy * 13, a1[1] + ux * 13), (a1[0] + uy * 13, a1[1] - ux * 13)], fill=GRN)
txt((a1[0] + 34, a1[1] - 6), DL("plate moves out", "tabla dışarı çıkar"), f22, GRN, "lm")
# görünen kenarlar
for a, b in (((0, D, 0), (W, D, 0)), ((W, D, 0), (W, 0, 0)), ((0, D, 0), (0, D, H)), ((W, D, 0), (W, D, H)), ((W, 0, 0), (W, 0, H)),
             ((0, D, H), (W, D, H)), ((W, D, H), (W, 0, H)), ((W, 0, H), (0, 0, H)), ((0, 0, H), (0, D, H))):
    line(a, b, INK, 4)

# ölçüler (kenarlara paralel, dışarıda)
def olcu(a, b, off, s, c=INK):
    pa, pb = P(*a), P(*b)
    qa, qb = (pa[0] + off[0], pa[1] + off[1]), (pb[0] + off[0], pb[1] + off[1])
    g.line([qa, qb], fill=c, width=2)
    for p, q in ((pa, qa), (pb, qb)):
        g.line([p, (q[0] + off[0] * 0.15, q[1] + off[1] * 0.15)], fill=c, width=1)
    txt(((qa[0] + qb[0]) / 2 + off[0] * 0.6, (qa[1] + qb[1]) / 2 + off[1] * 0.6), s, f26, c)
olcu((0, D, 0), (W, D, 0), (-40, 70), "700")
olcu((W, D, 0), (W, 0, 0), (45, 70), "909")
olcu((0, D, 0), (0, D, H), (-90, 0), "967")
# disk yüksekliği: kutu tabanından disk üstüne (disk merkezinin altında dikey)
dash((PX, D, 0), (PX, PD, 0), BLUE, 2)
txt(P(PX + 18, (D + PD) / 2, 0), "249", f22, BLUE, "lm")
pc = P(PX, PD, PY)
txt((pc[0], pc[1] - 34), DL("OUR PLATE Ø340", "BİZİM TABLA Ø340"), f26, INK, "mm")
txt((pc[0], pc[1] + 2), DL("dough rolled here to Ø280", "hamur burada Ø280 açılır"), f22, GRN, "mm")

# başlık + kısa not
txt((80, 90), DL("SPACE FOR THE BARE ROLLING MACHINE", "ÇIPLAK HAMUR AÇMA MAKİNESİ İÇİN AYRILAN ALAN"), f34, INK, "lm")
for i, s in enumerate([DL("All dimensions in mm. Box = the space we reserved (inside dimensions). Front = the face toward you.", "Ölçüler mm. Kutu = ayırdığımız alan (iç ölçüler). Ön = size bakan yüz."),
                       DL("Our plate Ø340 (food-grade, can rotate) stops here, the dough is rolled on it, then the plate moves out to the right.", "Tablamız Ø340 (gıdaya uygun, dönebilir) burada durur, hamur tablanın üstünde açılır, sonra tabla sağa çıkar."),
                       DL("At rest the machine must be ≥ 160 mm above the plate. Plate top: 106 mm above the box floor = 1000 mm from the shop floor.", "Beklerken makinenin her parçası tablanın en az 160 mm üstünde. Tabla üstü: kutu tabanından 106 mm = yerden 1000 mm."),
                       "Kemal Kul · 28.09.2026 · ACICI_ALANI v2"]):
    txt((80, 150 + i * 40), s, f22, GRAY if i == 3 else (60, 60, 66), "lm")
fr = P(W / 2, D, H / 2)
txt(fr, DL("FRONT", "ÖN"), f26, GRAY, "mm")
im.save(OUT)
print("yazildi", OUT, im.size)
