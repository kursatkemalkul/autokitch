# -*- coding: utf-8 -*-
"""AÇICI ALANI · tedarikçi paftası v4 (28 Eyl 2026) — Kemal: "mavi iki kutuyu birleştir, tek kutu, kullanılabilir alan de" → Z1 + Z2 tek mavi L alan.
v3 (28 Eyl 2026) — Kemal: "teknik resim anlaşılmaz; üst, alt, yan çizimi de koy, kullanabileceği yerleri
ölçüleriyle. Bizim tablanın kayacağı yerde olamaz, o alan boş olmalı."
ÖNDEN + YANDAN + ÜSTTEN görünüş + küçük 3D. Bölgeler (dünya mm; montaj v64 parca_kutulari.json'dan ölçüldü):
  Z1 KULLANILABİLİR ÜST HACİM  x 31,5–670 · y 1160–1830,5 · z −505…+9   (dikmeler/üst kuşak arası; tabla üstünden 160 yukarısı)
  Z2 KULLANILABİLİR ARKA HACİM x 31,5–670 · y 893,5–1830,5 · z −798,5…−505 (mekanizma bandının ve enerji zincirinin arkası; bugün açıcı kolonu burada)
  Z3 YALNIZ AÇARKEN            x 180–520 · y 1000–1160 · z −340…0 (tabla üstü; açma bitince Z1'e çekilir)
  BOŞ KALMALI                  tabla mekanizması x 31,5–700 · y 893,5–1000 · z −505…+9 (mekanizma teknesi, raylar, araba, x motoru, enerji zinciri)
                               + tabla kayma yolu x 180–700 · y 1000–1042 · z −350…+9 (disk + hamur + boşluk; tabla sağa TOPPING'e çıkar)
Çalıştır: python teknik_acici_alani_v3.py [tr]  → FULL_MAKINE/ACICI_ALANI_v3.png (İngilizce, tedarikçiye) · ACICI_ALANI_v3_TR.png (Kemal)
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
TR = "tr" in sys.argv
DL = (lambda en, tr: tr if TR else en)
OUT = os.path.join(os.path.dirname(U), "FULL_MAKINE", "ACICI_ALANI_v4_TR.png" if TR else "ACICI_ALANI_v4.png")
assert not os.path.exists(OUT), "zaten var: " + OUT

# ---------------- veri (dünya mm) ----------------
X0, X1, XI0, XI1 = 0.0, 700.0, 31.5, 670.0
Y_KAIDE, Y_FL, Y_TOP, Y_KUS = 788.0, 893.5, 1860.5, 1830.5
Z_B, Z_F, Z_BI, Z_FI = -830.0, 79.0, -798.5, 9.0
Z_MEK = -505.0                                   # mekanizma bandı + enerji zinciri arkası (enerji_zinciri_kanali z −500, x motoru −462)
Y_PLATE, PLATE = 1000.0, (180.0, 520.0, -340.0, 0.0)   # disk üstü · x0 x1 z0 z1 (Ø340, merkez x 350 · z −170)
Y_YOL, Y_REST = 1042.0, 1160.0                   # tabla yolu üst sınırı (disk + hamur + boşluk) · beklerken makinenin altı
Z1 = (XI0, XI1, Y_REST, Y_KUS, Z_MEK, Z_FI)
Z2 = (XI0, XI1, Y_FL, Y_KUS, Z_BI, Z_MEK)
Z3 = (PLATE[0], PLATE[1], Y_PLATE, Y_REST, PLATE[2], PLATE[3])
MEK = (XI0, X1, Y_FL, Y_PLATE, Z_MEK, Z_FI)
YOL = (PLATE[0], X1, Y_PLATE, Y_YOL, -350.0, Z_FI)

S = 0.9
W_PX, H_PX = 2600, 2660
im = Image.new("RGBA", (W_PX, H_PX), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
def F(n, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", n)
    except OSError:
        return ImageFont.load_default()
f9, f10, f12, f14, f18, f30 = F(17), F(19), F(22), F(25), F(30, True), F(38, True)
INK, GRAY, BLUE, RED, GRN = (20, 20, 24), (130, 130, 136), (20, 90, 200), (205, 40, 30), (30, 130, 80)
C_Z1, C_Z2, C_RED, C_GRAY, C_PL = (205, 226, 255), (225, 237, 255), (255, 214, 208), (228, 228, 231), (190, 194, 202)

def txt(p, s, f=f10, c=INK, a="mm"): d.text(p, s, font=f, fill=c, anchor=a)
def rect(p0, p1, fill=None, out=None, w=2):
    d.rectangle([min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])], fill=fill, outline=out, width=w)
def dash(p0, p1, c=INK, w=2, on=12, off=8):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); t = 0.0
    while t < L:
        t1 = min(L, t + on)
        d.line([(p0[0] + (p1[0] - p0[0]) * t / L, p0[1] + (p1[1] - p0[1]) * t / L), (p0[0] + (p1[0] - p0[0]) * t1 / L, p0[1] + (p1[1] - p0[1]) * t1 / L)], fill=c, width=w)
        t += on + off
def drect(p0, p1, c=INK, w=2):
    x0, x1, y0, y1 = min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1])
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        dash(a, b, c, w)
def dim_h(xa, xb, y, s, c=INK, f=None):
    d.line([(xa, y), (xb, y)], fill=c, width=2)
    for x in (xa, xb):
        d.line([(x, y - 8), (x, y + 8)], fill=c, width=2)
    txt(((xa + xb) / 2, y - 5), s, f or f9, c, "md")
def dim_v(x, ya, yb, s, c=INK, side="r", f=None):
    d.line([(x, ya), (x, yb)], fill=c, width=2)
    for y in (ya, yb):
        d.line([(x - 8, y), (x + 8, y)], fill=c, width=2)
    txt((x + (7 if side == "r" else -7), (ya + yb) / 2), s, f or f9, c, "lm" if side == "r" else "rm")
def n(v): return ("%.1f" % v).rstrip("0").rstrip(".").replace(".", "," if TR else ".")

# ---------------- başlık + gösterim ----------------
txt((80, 70), DL("SPACE FOR THE BARE DOUGH ROLLING MACHINE", "ÇIPLAK HAMUR AÇMA MAKİNESİ İÇİN AYRILAN ALAN"), f30, INK, "lm")
txt((80, 118), DL("All dimensions in mm. Heights from the shop floor. Front = side where the operator stands.",
                  "Ölçüler mm. Yükseklikler dükkân zemininden. Ön = operatörün durduğu taraf."), f12, (70, 70, 76), "lm")
LEG = [(C_Z1, BLUE, None, DL("BLUE = USABLE SPACE for the machine", "MAVİ = KULLANILABİLİR ALAN (makine burayı kullanabilir)")),
       (None, BLUE, "dash", DL("DASHED = only while rolling (the roller comes down onto our plate), then back up", "KESİKLİ = yalnız hamuru açarken (merdane tablamıza iner), sonra yukarı çekilir")),
       (C_RED, RED, None, DL("RED = MUST STAY EMPTY: our plate moves through here + our plate mechanism", "KIRMIZI = BOŞ KALMALI: tablamızın kaydığı yol + tabla mekanizmamız")),
       (C_GRAY, GRAY, None, DL("GRAY = our cabinet (posts, front panel) and our base", "GRİ = bizim gövde (dikmeler, ön kapak) ve altındaki kaide"))]
for i, (fc, oc, st, s) in enumerate(LEG):
    y = 165 + i * 36; x = 80
    if st == "dash":
        drect((x, y - 11), (x + 44, y + 11), oc, 2)
    else:
        rect((x, y - 11), (x + 44, y + 11), fc, oc, 2)
    txt((x + 60, y), s, f12, INK, "lm")

# ======================= ÖNDEN (x →, y ↑) =======================
FX, FY = 300, 420
fx = lambda x: FX + x * S
fy = lambda y: FY + (1862.0 - y) * S
def fbox(b, fill=None, out=None, w=2, dashed=False):
    p0, p1 = (fx(b[0]), fy(b[2])), (fx(b[1]), fy(b[3]))
    if dashed:
        drect(p0, p1, out, w)
    else:
        rect(p0, p1, fill, out, w)
txt((FX, FY - 95), DL("FRONT VIEW", "ÖNDEN GÖRÜNÜŞ"), f18, INK, "lm")
rect((fx(X0), fy(Y_FL)), (fx(X1), fy(Y_KAIDE)), C_GRAY, GRAY, 2)                                 # kaide
txt((fx(350), fy(840)), DL("our base", "bizim kaide"), f9, GRAY)
rect((fx(XI0), fy(Y_KUS)), (fx(XI1), fy(Y_FL)), C_Z1, BLUE, 2)                                  # v4: tek mavi alan                                     # Z2 (arkada) — önden bakınca alt kısmı
fbox(MEK, C_RED, RED, 2); fbox(YOL, C_RED, RED, 2)
rect((fx(PLATE[0]), fy(Y_PLATE)), (fx(PLATE[1]), fy(Y_PLATE - 8)), C_PL, INK, 2)
fbox(Z3, None, BLUE, 3, dashed=True)
for xa, xb in ((X0, XI0), (XI1, X1)):
    rect((fx(xa), fy(Y_TOP)), (fx(xb), fy(Y_FL)), C_GRAY, GRAY, 1)
rect((fx(XI0), fy(Y_TOP)), (fx(XI1), fy(Y_KUS)), C_GRAY, GRAY, 1)
rect((fx(X0), fy(Y_TOP)), (fx(X1), fy(Y_FL)), None, INK, 4)
txt((fx(350), fy(1500)), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)
txt((fx(350), fy(1330)), DL("(below 1160 only in the back part, see side view)", "(1160 altında yalnız arka kısım, yan görünüşe bak)"), f9, BLUE)
txt((fx(350), fy(1080)), DL("only while rolling", "yalnız açarken"), f9, BLUE)
txt((fx(105), fy(955)), DL("our mechanism", "mekanizmamız"), f9, RED)
txt((fx(610), fy(1020)), DL("plate path →", "tabla yolu →"), f9, RED)
txt((fx(350), fy(Y_PLATE - 8) + 16), DL("our plate Ø340", "tablamız Ø340"), f9, INK)
d.line([(fx(X1) + 4, fy(1021)), (fx(X1) + 70, fy(1021))], fill=GRN, width=4)
d.polygon([(fx(X1) + 70, fy(1021) - 9), (fx(X1) + 88, fy(1021)), (fx(X1) + 70, fy(1021) + 9)], fill=GRN)
txt((fx(X1) + 46, fy(1021) + 24), "TOPPING", f9, GRN)
# ölçüler — önden
dim_h(fx(X0), fx(X1), fy(1862) - 30, "700")
yb = fy(Y_KAIDE) + 40
for a, b in ((X0, XI0), (XI0, PLATE[0]), (PLATE[0], PLATE[1]), (PLATE[1], XI1), (XI1, X1)):
    dim_h(fx(a), fx(b), yb, n(b - a))
dim_h(fx(XI0), fx(XI1), yb + 44, "638", BLUE)
xr = fx(X1) + 120
for a, b, c in ((Y_FL, Y_PLATE, RED), (Y_PLATE, Y_YOL, RED), (Y_YOL, Y_REST, BLUE), (Y_REST, Y_KUS, BLUE), (Y_KUS, Y_TOP, INK)):
    dim_v(xr, fy(a), fy(b), n(b - a), c)
xr2 = xr + 110
for yv in (Y_FL, Y_PLATE, Y_YOL, Y_REST, Y_KUS):
    txt((xr2, fy(yv)), n(yv), f9, GRAY, "lm")
txt((xr2, fy(Y_TOP) - 18), DL("height", "yükseklik"), f9, GRAY, "lm")

# ======================= YANDAN (sağdan bakış: z →, arka solda · y ↑) =======================
SX = xr2 + 190
sz = lambda z: SX + (z - Z_B) * S
def sbox(b, fill=None, out=None, w=2, dashed=False):
    p0, p1 = (sz(b[4]), fy(b[2])), (sz(b[5]), fy(b[3]))
    if dashed:
        drect(p0, p1, out, w)
    else:
        rect(p0, p1, fill, out, w)
txt((SX, FY - 95), DL("SIDE VIEW (from the right)", "YANDAN GÖRÜNÜŞ (sağdan)"), f18, INK, "lm")
rect((sz(Z_B), fy(Y_FL)), (sz(Z_F), fy(Y_KAIDE)), C_GRAY, GRAY, 2)
d.polygon([(sz(Z_BI), fy(Y_FL)), (sz(Z_MEK), fy(Y_FL)), (sz(Z_MEK), fy(Y_REST)), (sz(Z_FI), fy(Y_REST)), (sz(Z_FI), fy(Y_KUS)), (sz(Z_BI), fy(Y_KUS))], fill=C_Z1, outline=BLUE, width=2)                                                  # v4: tek L alan
sbox(MEK, C_RED, RED, 2); sbox(YOL, C_RED, RED, 2)
rect((sz(PLATE[2]), fy(Y_PLATE)), (sz(PLATE[3]), fy(Y_PLATE - 8)), C_PL, INK, 2)
sbox(Z3, None, BLUE, 3, dashed=True)
rect((sz(Z_B), fy(Y_TOP)), (sz(Z_BI), fy(Y_FL)), C_GRAY, GRAY, 1)
rect((sz(Z_FI), fy(Y_TOP)), (sz(Z_F), fy(Y_FL)), C_GRAY, GRAY, 1)
rect((sz(Z_BI), fy(Y_TOP)), (sz(Z_FI), fy(Y_KUS)), C_GRAY, GRAY, 1)
rect((sz(Z_B), fy(Y_TOP)), (sz(Z_F), fy(Y_FL)), None, INK, 4)
txt((sz(-395), fy(1500)), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)
txt((sz(-250), fy(950)), DL("our plate mechanism", "tabla mekanizmamız"), f9, RED)
txt((sz(-170), fy(1080)), DL("only while rolling", "yalnız açarken"), f9, BLUE)
txt((sz(44), fy(1500)), DL("front", "ön"), f9, GRAY); txt((sz(44), fy(1470)), DL("panel", "kapak"), f9, GRAY)
# ölçüler — yandan
dim_h(sz(Z_B), sz(Z_F), fy(1862) - 30, "909")
yb2 = fy(Y_KAIDE) + 40
for a, b in ((Z_B, Z_BI), (Z_BI, Z_MEK), (Z_MEK, PLATE[2]), (PLATE[2], PLATE[3]), (PLATE[3], Z_FI), (Z_FI, Z_F)):
    dim_h(sz(a), sz(b), yb2, n(b - a))
dim_h(sz(Z_BI), sz(Z_MEK), yb2 + 44, n(Z_MEK - Z_BI), BLUE)
dim_h(sz(Z_MEK), sz(Z_FI), yb2 + 44, n(Z_FI - Z_MEK), BLUE)
dim_v(sz(Z_BI) - 34, fy(Y_FL), fy(Y_KUS), n(Y_KUS - Y_FL), BLUE, "l")

# ======================= ÜSTTEN (x →, z ↓: arka üstte) =======================
TY = yb + 190
tz = lambda z: TY + (z - Z_B) * S
def tbox(b, fill=None, out=None, w=2, dashed=False):
    p0, p1 = (fx(b[0]), tz(b[4])), (fx(b[1]), tz(b[5]))
    if dashed:
        drect(p0, p1, out, w)
    else:
        rect(p0, p1, fill, out, w)
txt((FX, TY - 80), DL("TOP VIEW", "ÜSTTEN GÖRÜNÜŞ"), f18, INK, "lm")
rect((fx(XI0), tz(Z_BI)), (fx(XI1), tz(Z_FI)), C_Z1, BLUE, 2)                                  # v4: tek mavi alan
tbox(YOL, None, RED, 3, dashed=True)
d.ellipse([fx(PLATE[0]), tz(PLATE[2]), fx(PLATE[1]), tz(PLATE[3])], fill=C_PL, outline=INK, width=2)
d.ellipse([fx(350 - 140), tz(-170 - 140), fx(350 + 140), tz(-170 + 140)], outline=GRN, width=2)
rect((fx(X0), tz(Z_B)), (fx(XI0), tz(Z_F)), C_GRAY, GRAY, 1); rect((fx(XI1), tz(Z_B)), (fx(X1), tz(Z_F)), C_GRAY, GRAY, 1)
rect((fx(XI0), tz(Z_FI)), (fx(XI1), tz(Z_F)), C_GRAY, GRAY, 1); rect((fx(XI0), tz(Z_B)), (fx(XI1), tz(Z_BI)), C_GRAY, GRAY, 1)
rect((fx(X0), tz(Z_B)), (fx(X1), tz(Z_F)), None, INK, 4)
d.line([(fx(PLATE[1]) + 6, tz(-170)), (fx(X1) + 70, tz(-170))], fill=GRN, width=4)
d.polygon([(fx(X1) + 70, tz(-170) - 9), (fx(X1) + 88, tz(-170)), (fx(X1) + 70, tz(-170) + 9)], fill=GRN)
txt((fx(X1) + 46, tz(-170) + 24), "TOPPING", f9, GRN)
txt((fx(350), tz(-700) - 12), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)
txt((fx(350), tz(-700) + 20), DL("back 293.5: full height 893.5–1830.5 · front: above 1160", "arka 293,5: tam boy 893,5–1830,5 · ön: 1160 üstü"), f9, BLUE)
txt((fx(350), tz(-170) - 10), DL("our plate Ø340", "tablamız Ø340"), f9, INK)
txt((fx(350), tz(-170) + 16), DL("dough Ø280", "hamur Ø280"), f9, GRN)
txt((fx(610), tz(-40)), DL("plate path", "tabla yolu"), f9, RED)
txt((fx(610), tz(-16)), DL("(below 1042)", "(1042 altı)"), f9, RED)
txt((fx(350), tz(Z_F) + 22), DL("FRONT", "ÖN"), f10, GRAY)
dim_h(fx(X0), fx(X1), tz(Z_F) + 70, "700")
xl = fx(X0) - 40
for a, b, c in ((Z_B, Z_BI, INK), (Z_BI, Z_MEK, BLUE), (Z_MEK, PLATE[2], INK), (PLATE[2], PLATE[3], INK), (PLATE[3], Z_F, INK)):
    dim_v(xl, tz(a), tz(b), n(b - a), c, "l")
dim_v(xl - 130, tz(Z_B), tz(Z_F), "909", INK, "l")

# ======================= 3D (küçük) =======================
IS, C30 = 0.45, math.cos(math.radians(30))
IX, IY = SX + 520, TY + 470
def P(x, z, y):                                   # x dünya, z dünya (ön +), y dünya
    dd = z - Z_B                                  # arkadan öne
    return (IX + (x - dd) * C30 * IS, IY + ((x + dd) * 0.5 - (y - Y_FL)) * IS)
def kutu3(b, fill, out, a=110, w=2):
    x0, x1, y0, y1, z0, z1 = b
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for poly in ([P(x0, z1, y0), P(x1, z1, y0), P(x1, z1, y1), P(x0, z1, y1)],     # ön
                 [P(x1, z1, y0), P(x1, z0, y0), P(x1, z0, y1), P(x1, z1, y1)],     # sağ
                 [P(x0, z0, y1), P(x1, z0, y1), P(x1, z1, y1), P(x0, z1, y1)]):    # üst
        g.polygon(poly, fill=fill + (a,))
    im.alpha_composite(lay)
    for p, q in ((P(x0, z1, y0), P(x1, z1, y0)), (P(x1, z1, y0), P(x1, z0, y0)), (P(x0, z1, y0), P(x0, z1, y1)), (P(x1, z1, y0), P(x1, z1, y1)),
                 (P(x1, z0, y0), P(x1, z0, y1)), (P(x0, z1, y1), P(x1, z1, y1)), (P(x1, z1, y1), P(x1, z0, y1)), (P(x1, z0, y1), P(x0, z0, y1)), (P(x0, z0, y1), P(x0, z1, y1))):
        d.line([p, q], fill=out, width=w)
txt((SX, TY - 80), DL("3D", "3D"), f18, INK, "lm")
kutu3(MEK, C_RED, RED); kutu3(YOL, C_RED, RED)
pl = [P(350 + 170 * math.cos(t), -170 + 170 * math.sin(t), Y_PLATE) for t in (2 * math.pi * i / 90 for i in range(90))]
d.polygon(pl, fill=C_PL, outline=INK)
def kutuL(fill, out, a=110, w=2):
    x0, x1 = XI0, XI1; zb, zm, zf = Z_BI, Z_MEK, Z_FI; y0, ym, yt = Y_FL, Y_REST, Y_KUS
    yuz = [[P(x0, zb, yt), P(x1, zb, yt), P(x1, zf, yt), P(x0, zf, yt)],
           [P(x1, zb, y0), P(x1, zm, y0), P(x1, zm, ym), P(x1, zf, ym), P(x1, zf, yt), P(x1, zb, yt)],
           [P(x0, zf, ym), P(x1, zf, ym), P(x1, zf, yt), P(x0, zf, yt)],
           [P(x0, zm, y0), P(x1, zm, y0), P(x1, zm, ym), P(x0, zm, ym)]]
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    for poly in yuz:
        g.polygon(poly, fill=fill + (a,))
    im.alpha_composite(lay)
    for poly in yuz:
        d.line(poly + [poly[0]], fill=out, width=w)
kutuL(C_Z1, BLUE)
kutu3((X0, X1, Y_FL, Y_TOP, Z_B, Z_F), (255, 255, 255), INK, 0, 3)
a0, a1 = P(560, -170, Y_PLATE + 20), P(X1 + 160, -170, Y_PLATE + 20)
d.line([a0, a1], fill=GRN, width=4)
txt((a1[0] + 10, a1[1] + 18), "TOPPING", f9, GRN, "lm")
fr = P(350, Z_F, 1600); txt(fr, DL("FRONT", "ÖN"), f10, GRAY)

d.line([(80, H_PX - 70), (W_PX - 80, H_PX - 70)], fill=(220, 220, 224), width=2)
txt((W_PX - 80, H_PX - 40), "Kemal Kul · 28.09.2026 · ACICI_ALANI v4", f9, GRAY, "rm")
im.convert("RGB").save(OUT)
print("yazildi", OUT, im.size)
