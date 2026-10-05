# -*- coding: utf-8 -*-
"""AÇICI ALANI · tedarikçi paftası v1 (28 Eyl 2026) — hamur açma makinesi teklifleri için (çıplak makine bu alana gelecek).
Kemal: "bizim tablayı ve ayırdığımız yeri teknik resim yap, çok basit". Ölçüler acici_kabin_cad_v1.py (A kabini) + itici_cad_v5 (DISK_UST 1000):
A modülü x 0–700 · y 893,5 (kaide sacı üstü) … 1860,5 (üst sac altı) · z −830 (arka) … +79 (ön düzlem); tabla Ø340, üstü 1000, merkezi x 350 · z −170;
robot ağzı x 250–450 · y 960–1160 (ön yüz); tabla sağa (x +) TOPPING'e çıkar (C sol yan sacında yuva y 893–1042 · z −510…+5).
Etiketler İngilizce (tedarikçiye gider). Çıktı: FULL_MAKINE/ACICI_ALANI_v1.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(U), "FULL_MAKINE", "ACICI_ALANI_v1")
assert not os.path.exists(OUT + ".png"), "v1 zaten var"
S = 0.9                                        # px / mm
W_PX, H_PX = 2480, 2420
im = Image.new("RGB", (W_PX, H_PX), "white"); d = ImageDraw.Draw(im)
def F(n, b=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if b else "arial.ttf", n)
    except OSError:
        return ImageFont.load_default()
f10, f12, f14, f18, f24 = F(19), F(22), F(25), F(30, True), F(40, True)
INK, GRAY, BLUE, RED, GRN = (20, 20, 24), (140, 140, 146), (20, 90, 200), (200, 50, 30), (30, 130, 80)
FREE, PLATE, KEEP = (225, 240, 255), (205, 208, 214), (255, 228, 222)

# ---------------- veri (mm, dünya) ----------------
X0, X1 = 0.0, 700.0                           # A modülü
XI0, XI1 = 31.5, 670.0                        # iç dikmeler arası
Y_FLOOR, Y_TOP = 893.5, 1860.5                # alan tabanı (kaide sacı üstü) · üst sac altı
Y_KUSAK = 1830.5                              # üst kuşak altı
Z_BACK, Z_FRONT, Z_IN0, Z_IN1 = -830.0, 79.0, -798.5, 9.0
PLATE_Y, PLATE_T, PLATE_D, PLATE_X, PLATE_Z = 1000.0, 8.0, 340.0, 350.0, -170.0
MOUTH_X, MOUTH_Y = (250.0, 450.0), (960.0, 1160.0)
REST_Y = PLATE_Y + 160.0                      # dinlenme: makine plakanın ≥ 160 üstünde (ağız üstü 1160)
EXIT_Y, EXIT_Z = (893.0, 1042.0), (-510.0, 5.0)

def txt(x, y, s, f=f12, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)
def box(p0, p1, fill=None, outline=INK, w=2):
    d.rectangle([min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])], fill=fill, outline=outline, width=w)
def dash(p0, p1, c=INK, w=2, on=14, off=8):
    import math
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1.0, (i * (on + off) + on) / L)
        d.line([(p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a), (p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b)], fill=c, width=w)
def dim_h(xa, xb, y, s, c=INK):
    d.line([(xa, y), (xb, y)], fill=c, width=2)
    for x in (xa, xb):
        d.line([(x, y - 9), (x, y + 9)], fill=c, width=2)
    txt((xa + xb) / 2, y - 6, s, f10, c, "md")
def dim_v(x, ya, yb, s, c=INK, side="r"):
    d.line([(x, ya), (x, yb)], fill=c, width=2)
    for y in (ya, yb):
        d.line([(x - 9, y), (x + 9, y)], fill=c, width=2)
    txt(x + (8 if side == "r" else -8), (ya + yb) / 2, s, f10, c, "lm" if side == "r" else "rm")

# ---------------- ÖNDEN GÖRÜNÜŞ (x →, y ↑) ----------------
FX, FY = 330, 230                              # sol üst köşe (px) · y ekseni 1862 üstte
fx = lambda x: FX + x * S
fy = lambda y: FY + (1862.0 - y) * S
txt(FX, FY - 150, "FRONT VIEW", f18)
box((fx(XI0), fy(Y_KUSAK)), (fx(XI1), fy(REST_Y)), fill=FREE, outline=BLUE, w=2)          # serbest alan (dinlenme konumu)
box((fx(PLATE_X - PLATE_D / 2), fy(REST_Y)), (fx(PLATE_X + PLATE_D / 2), fy(PLATE_Y + PLATE_T)), fill=FREE, outline=BLUE, w=1)   # çalışırken plakaya iner
box((fx(X0), fy(Y_TOP)), (fx(X1), fy(Y_FLOOR)), outline=INK, w=4)                            # A alanı
box((fx(X0), fy(Y_FLOOR)), (fx(X1), fy(788.0)), fill=(236, 236, 238), outline=GRAY, w=2)    # kaide (bizim)
txt(fx(350), fy(840), "our base / cold cabinet below (not in scope)", f10, GRAY, "mm")
box((fx(X1), fy(1862.0)), (fx(X1 + 160), fy(788.0)), fill=(246, 246, 247), outline=GRAY, w=2)
txt(fx(X1 + 80), fy(1500), "TOPPING", f12, GRAY, "mm"); txt(fx(X1 + 80), fy(1470), "station", f10, GRAY, "mm")
box((fx(PLATE_X - PLATE_D / 2), fy(PLATE_Y + PLATE_T)), (fx(PLATE_X + PLATE_D / 2), fy(PLATE_Y)), fill=PLATE, outline=INK, w=2)
txt(fx(X0) + 12, fy(985), "OUR PLATE Ø340", f10, INK, "lm"); txt(fx(X0) + 12, fy(955), "top 1000 from floor", f10, INK, "lm")
dash((fx(MOUTH_X[0]), fy(MOUTH_Y[0])), (fx(MOUTH_X[0]), fy(MOUTH_Y[1])), RED); dash((fx(MOUTH_X[1]), fy(MOUTH_Y[0])), (fx(MOUTH_X[1]), fy(MOUTH_Y[1])), RED)
dash((fx(MOUTH_X[0]), fy(MOUTH_Y[1])), (fx(MOUTH_X[1]), fy(MOUTH_Y[1])), RED); dash((fx(MOUTH_X[0]), fy(MOUTH_Y[0])), (fx(MOUTH_X[1]), fy(MOUTH_Y[0])), RED)
txt(fx(350), fy(925), "robot loading opening 200 × 200 (front)", f10, RED, "mm")
d.line([(fx(PLATE_X + PLATE_D / 2) + 10, fy(PLATE_Y + 20)), (fx(X1 + 130), fy(PLATE_Y + 20))], fill=GRN, width=4)
d.polygon([(fx(X1 + 130), fy(PLATE_Y + 20) - 10), (fx(X1 + 150), fy(PLATE_Y + 20)), (fx(X1 + 130), fy(PLATE_Y + 20) + 10)], fill=GRN)
txt(fx(X1 + 80), fy(PLATE_Y + 20) - 14, "plate exits →", f10, GRN, "md")
txt(fx(350), fy(1500), "FREE SPACE FOR THE BARE MACHINE", f14, BLUE, "mm")
txt(fx(350), fy(1460), "(rest position: everything ≥ 160 above the plate)", f10, BLUE, "mm")
dim_h(fx(X0), fx(X1), fy(1862) - 40, "700")
dim_h(fx(XI0), fx(XI1), fy(Y_KUSAK) + 26, "638 free", BLUE)
dim_v(fx(X0) - 270, fy(Y_TOP), fy(Y_FLOOR), "967", INK, "l")
dim_v(fx(X0) - 40, fy(Y_KUSAK), fy(PLATE_Y), "830 above plate", BLUE, "l")
dim_v(fx(X0) - 40, fy(PLATE_Y), fy(Y_FLOOR), "106", INK, "l")

# ---------------- YANDAN GÖRÜNÜŞ (z →: arka solda, ön sağda · y ↑) ----------------
SX = fx(X1) + 330
sz = lambda z: SX + (z - Z_BACK) * S
txt(SX, FY - 150, "SIDE VIEW (from the right)", f18)
box((sz(Z_IN0), fy(Y_KUSAK)), (sz(Z_IN1), fy(REST_Y)), fill=FREE, outline=BLUE, w=2)
box((sz(Z_BACK), fy(Y_TOP)), (sz(Z_FRONT), fy(Y_FLOOR)), outline=INK, w=4)
box((sz(Z_BACK), fy(Y_FLOOR)), (sz(Z_FRONT), fy(788.0)), fill=(236, 236, 238), outline=GRAY, w=2)
box((sz(PLATE_Z - PLATE_D / 2), fy(PLATE_Y + PLATE_T)), (sz(PLATE_Z + PLATE_D / 2), fy(PLATE_Y)), fill=PLATE, outline=INK, w=2)
box((sz(59.0), fy(Y_TOP)), (sz(Z_FRONT), fy(Y_FLOOR)), fill=(236, 236, 238), outline=GRAY, w=1)
dash((sz(-170.0), fy(1047.0)), (sz(Z_FRONT + 60), fy(1047.0)), RED, 3)
d.polygon([(sz(-170.0) + 18, fy(1047) - 9), (sz(-170.0), fy(1047)), (sz(-170.0) + 18, fy(1047) + 9)], fill=RED)
txt(sz(-120), fy(1047) - 16, "robot puts the dough ball from the front", f10, RED, "ld")
txt(sz(-395), fy(1500), "FREE SPACE", f14, BLUE, "mm")
dim_h(sz(Z_BACK), sz(Z_FRONT), fy(1862) - 40, "909 (back wall → front face)")
dim_h(sz(Z_IN0), sz(Z_IN1), fy(Y_KUSAK) + 26, "807 free", BLUE)
dim_h(sz(PLATE_Z - PLATE_D / 2), sz(PLATE_Z + PLATE_D / 2), fy(PLATE_Y) + 40, "Ø340")

# ---------------- ÜSTTEN GÖRÜNÜŞ (x →, z ↓: arka üstte, ön altta) ----------------
TY = fy(788.0) + 260
tz = lambda z: TY + (z - Z_BACK) * S
txt(FX, TY - 130, "TOP VIEW", f18)
box((fx(XI0), tz(Z_IN0)), (fx(XI1), tz(Z_IN1)), fill=FREE, outline=BLUE, w=2)
box((fx(X0), tz(Z_BACK)), (fx(X1), tz(Z_FRONT)), outline=INK, w=4)
d.ellipse([fx(PLATE_X - PLATE_D / 2), tz(PLATE_Z - PLATE_D / 2), fx(PLATE_X + PLATE_D / 2), tz(PLATE_Z + PLATE_D / 2)], fill=PLATE, outline=INK, width=2)
d.ellipse([fx(PLATE_X - 140), tz(PLATE_Z - 140), fx(PLATE_X + 140), tz(PLATE_Z + 140)], outline=GRN, width=2)
txt(fx(PLATE_X), tz(PLATE_Z) - 12, "rolled dough", f10, GRN, "mm"); txt(fx(PLATE_X), tz(PLATE_Z) + 14, "Ø280 round", f10, GRN, "mm")
box((fx(X1), tz(Z_BACK)), (fx(X1 + 160), tz(Z_FRONT)), fill=(246, 246, 247), outline=GRAY, w=2)
txt(fx(X1 + 80), tz(-600), "TOPPING", f12, GRAY, "mm")
d.line([(fx(PLATE_X + PLATE_D / 2) + 10, tz(PLATE_Z)), (fx(X1 + 130), tz(PLATE_Z))], fill=GRN, width=4)
d.polygon([(fx(X1 + 130), tz(PLATE_Z) - 10), (fx(X1 + 150), tz(PLATE_Z)), (fx(X1 + 130), tz(PLATE_Z) + 10)], fill=GRN)
d.line([(fx(MOUTH_X[0]), tz(Z_FRONT)), (fx(MOUTH_X[1]), tz(Z_FRONT))], fill=RED, width=6)
txt(fx(350), tz(Z_FRONT) + 12, "robot loading opening (front)", f10, RED, "ma")
txt(fx(350), tz(-700), "FREE SPACE (bare machine)", f12, BLUE, "mm")
dim_h(fx(X0), fx(X1), tz(Z_FRONT) + 70, "700")
dim_v(fx(X0) - 140, tz(Z_BACK), tz(Z_FRONT), "909", INK, "l")
dim_v(fx(X0) - 20, tz(PLATE_Z - PLATE_D / 2), tz(PLATE_Z + PLATE_D / 2), "Ø340", INK, "l")
txt(fx(X0) - 4, tz(Z_BACK) - 10, "back wall (shop wall behind)", f10, GRAY, "ld")

# ---------------- künye ----------------
KX = SX; KY = TY - 20
notes = ["AUTOKITCH · DOUGH OPENING AREA · for the bare rolling machine",
         "All dimensions in mm. Plate = our food-grade plate Ø340 (matt UHMW-PE, 8 mm), it can rotate. It stops under the machine,",
         "the dough is rolled ON it, then the plate moves right to the TOPPING station. No conveyor, no cabinet, no covers needed.",
         "Blue = free space for the machine. Red = robot loading path (must stay free at rest).",
         "Green = product: round Ø280 (pide, pizza, lahmacun).",
         "Controls / drives: in a separate box outside this area (cable ≥ 3 m).",
         "Kemal Kul · Torinoarch Studio · 28.09.2026 · drawing ACICI_ALANI v1"]
for i, s in enumerate(notes):
    txt(KX, KY + i * 34, s, f14 if i == 0 else f12, INK if i == 0 else (60, 60, 66))
im.save(OUT + ".png")
print("yazildi", OUT + ".png", im.size)
