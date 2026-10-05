# -*- coding: utf-8 -*-
"""BELDOS MINI-FILL · MODUL C'YE SIGMA KONTROLU v1 (24 Eyl 2026)

Kemal: "Oyle bir teknik resim yapsana, onlarin cizimleriyle nasil birsey cikiyor bizim kurguyla goreyim."

NE CIZILIYOR
  Modul C (tablali, teknik_hat_atosa_tablali_v7) GERCEK olculeriyle; hazne sirasinda kasetlerin yerine
  Beldos Mini-fill Electric 260 W uniteleri BROSURDEKI olcuyle. Kasar kaseti kalir (rende pompadan gecmez).
  Tasarim DEGISTIRILMEDI: tabla bolmesi tavani 1490, modul ustu 2030, hazne sirasi x 200-1500 aynen.

KAYNAK OLCULER  [Beldos Mini-fill brosuru EN 2021, s.6]
  govde 477 x 296 x 228 · hazne 3 L O160 x 316 · 8 L O256 x 376 · 15 L O256 x 495 · hazne ayagi 149
VARSAYIMLAR (brosurde olcu yok)
  govde 90 derece cevrik (296 genislik hat boyunca) · govde tabani = tabla bolmesi tavani 1490
  hazne ekseni govdenin on ucundan 130 (Ø256 govdeden tasmasin) · agiz govde on yuzunden 40 ileri, 90 derece asagi
  agiz ucu tabla ekseninde z -270 (ZORUNLU: doz yasasi eksenden serer) · agiz ucu kotu 1396 (pide ustu 1356 + 40)
"""
import os
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "MINIFILL_SIGMA_v1_teknik.png")

S = 2.0
W, H = 6500, 4920
BG, INK, GRAY, LINE = (255, 255, 255), (28, 28, 28), (120, 120, 120), (175, 175, 175)
BLUE, BLUE_F = (0, 88, 170), (222, 234, 248)
RED, RED_F = (200, 30, 30), (252, 226, 226)
GRN, GRN_F = (20, 120, 80), (224, 242, 232)
TBL, TBL_F = (60, 110, 190), (235, 242, 252)

F = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
f_t, f_h, f_l, f_s, f_d = F(52, True), F(40, True), F(28), F(24), F(26)

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

# ----------------------------------------------------------------- olculer
W_C, D_C = 1800.0, 830.0
Y0, Y1 = 1060.0, 2030.0                  # modul C tabani / ustu
RAY_T, DAM, BOLM = (1060.0, 1210.0), (1210.0, 1240.0), (1240.0, 1490.0)
P = 1340.0                               # tabla ustu
PIDE_UST = 1356.0                        # tabla 1340 + disk 8 + pide 8
AGIZ_Y = PIDE_UST + 40.0                 # 1396
Z_EKSEN = -270.0
GOV_L, GOV_B, GOV_H = 477.0, 296.0, 228.0
HZ = {3: (160.0, 316.0), 8: (256.0, 376.0), 15: (256.0, 495.0)}
HZ_SEC = 15
GOV_Y0 = 1490.0
GOV_Y1 = GOV_Y0 + GOV_H                  # 1718
AGIZ_ONE, HZ_ARKA = 40.0, 130.0
GOV_Z0 = Z_EKSEN + AGIZ_ONE              # govde on yuzu z -230
GOV_Z1 = GOV_Z0 - GOV_L                  # -707
HZ_Z = GOV_Z0 - HZ_ARKA                  # hazne ekseni z -340
ARA = 10.0
X_BAS = 200.0                            # mevcut hazne sirasi baslangici
KASAR_W, KASAR_Z = 280.0, (-200.0, -525.0)
T_BAS, T_KAS = (1490.0, 1624.0), (1627.0, 1987.0)

SIRA = [("HARÇ 1", "mf", "3 loblu"), ("HARÇ 2", "mf", "3 loblu"), ("KIYMA", "mf", "2 loblu"),
        ("KUŞBAŞI", "mf", "2 loblu"), ("KAŞAR", "kaset", ""), ("SUCUK", "mf", "2 loblu")]
yer, x = [], X_BAS
for ad, tip, pompa in SIRA:
    w = GOV_B if tip == "mf" else KASAR_W
    yer.append((ad, tip, pompa, x, x + w))
    x += w + ARA
X_SON = yer[-1][4]

# ----------------------------------------------------------------- yerlesim
M = 150
OXF = M + 120
FY_TOP = 330
Y_UST = 2260.0
FY = lambda y: FY_TOP + (Y_UST - y) * S
FX = lambda xm: OXF + xm * S
OXS = OXF + 2100.0 * S + 150
SZ = lambda z: OXS + (-z) * S
PY_TOP = FY(Y0) + 330
PZ = lambda z: PY_TOP + (z + D_C) * S


def rect(x0, y0, x1, y1, fill=None, out=INK, w=3):
    d.rectangle([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=fill, outline=out, width=w)


def drect(x0, y0, x1, y1, col=GRAY, w=2, on=18, off=10):
    for a, b, c, e in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        dline(a, b, c, e, col, w, on, off)


def dline(x0, y0, x1, y1, col=GRAY, w=2, on=18, off=10):
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if L == 0:
        return
    ux, uy, t = (x1 - x0) / L, (y1 - y0) / L, 0.0
    while t < L:
        t2 = min(t + on, L)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)], fill=col, width=w)
        t = t2 + off


def txt(x, y, s, f=f_l, col=INK, an="mm"):
    d.text((x, y), s, font=f, fill=col, anchor=an)


def ok(x, y, yon, col):
    k = 14
    if yon == "l":
        d.polygon([(x, y), (x + k, y - 6), (x + k, y + 6)], fill=col)
    elif yon == "r":
        d.polygon([(x, y), (x - k, y - 6), (x - k, y + 6)], fill=col)
    elif yon == "u":
        d.polygon([(x, y), (x - 6, y + k), (x + 6, y + k)], fill=col)
    else:
        d.polygon([(x, y), (x - 6, y - k), (x + 6, y - k)], fill=col)


def olcu_h(x0, x1, y, s, col=INK, f=f_d):
    d.line([(x0, y), (x1, y)], fill=col, width=2)
    ok(x0, y, "l", col); ok(x1, y, "r", col)
    for xx in (x0, x1):
        d.line([(xx, y - 14), (xx, y + 14)], fill=col, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 17, (x0 + x1) / 2 + tw / 2 + 6, y + 17], fill=BG)
    txt((x0 + x1) / 2, y, s, f, col)


def olcu_v(x, y0, y1, s, col=INK, f=f_d, sag=True):
    d.line([(x, y0), (x, y1)], fill=col, width=2)
    ok(x, min(y0, y1), "u", col); ok(x, max(y0, y1), "d", col)
    for yy in (y0, y1):
        d.line([(x - 14, yy), (x + 14, yy)], fill=col, width=2)
    txt(x + (16 if sag else -16), (y0 + y1) / 2, s, f, col, "lm" if sag else "rm")


def kot(xx, y, s, col=GRAY):
    d.line([(xx - 30, FY(y)), (xx, FY(y))], fill=col, width=2)
    txt(xx - 38, FY(y), s, f_s, col, "rm")


# ================================================================= BASLIK
txt(M, 70, "AUTOKITCH  ·  BELDOS MINI-FILL · MODÜL C'YE SIĞMA KONTROLÜ  v1", f_t, INK, "lm")
txt(M, 140, "modül C = HAT_ATOSA_TABLALI v7 ölçüleri (değiştirilmedi)  ·  Mini-fill Electric 260 W ölçüleri Beldos broşüründen (EN 2021, s.6)  ·  "
    "kaşar kaseti yerinde kalır  ·  hazne 15 L çizili  ·  ölçüler mm  ·  24 Eylül 2026", f_l, GRAY, "lm")
txt(M, 190, "VARSAYIM: gövde 90° çevrik · gövde tabanı = tabla bölmesi tavanı 1490 · hazne ekseni gövde ön ucundan 130 · "
    "ağız ön yüzden 40 ileri, ucu tabla ekseninde (z −270) ve pide üstünden 40 yukarıda (1396)", f_l, RED, "lm")
d.line([(M, 230), (W - M, 230)], fill=INK, width=3)

# ================================================================= ÖN GÖRÜNÜŞ
txt(OXF, FY_TOP - 30, "ÖN GÖRÜNÜŞ", f_h, BLUE, "ls")
# modul C govdesi
rect(FX(0), FY(Y1), FX(W_C), FY(Y0), None, INK, 5)
rect(FX(0), FY(RAY_T[1]), FX(W_C), FY(RAY_T[0]), (244, 244, 244), LINE, 2)
txt(FX(W_C / 2), FY((RAY_T[0] + RAY_T[1]) / 2), "tabla rayı + araba · tekne (v7 ile aynı)", f_s, GRAY)
rect(FX(0), FY(BOLM[1]), FX(W_C), FY(BOLM[0]), None, LINE, 2)
txt(FX(20), FY(BOLM[0]) - 22, "TABLA BÖLMESİ · tavan 1490", f_s, GRAY, "lm")
# tabla + pide (KIYMA altinda, gecerken)
_ky = [e for e in yer if e[0] == "KIYMA"][0]
_tx = (_ky[3] + _ky[4]) / 2
rect(FX(_tx - 170), FY(P), FX(_tx + 170), FY(P - 12), TBL_F, TBL, 3)
rect(FX(_tx - 140), FY(PIDE_UST), FX(_tx + 140), FY(P + 8), (246, 226, 190), (170, 130, 70), 2)
txt(FX(_tx), FY(P - 12) + 26, "tabla Ø340 · pide üstü 1356", f_s, TBL)
# uniteler
for ad, tip, pompa, x0, x1 in yer:
    xc = (x0 + x1) / 2
    tasti = x1 > 1500.0
    if tip == "mf":
        rect(FX(x0), FY(GOV_Y1), FX(x1), FY(GOV_Y0), BLUE_F, RED if tasti else BLUE, 4)
        hc, hh = HZ[HZ_SEC]
        rect(FX(xc - hc / 2), FY(GOV_Y1 + hh), FX(xc + hc / 2), FY(GOV_Y1), (250, 252, 255), RED if tasti else BLUE, 3)
        d.line([(FX(xc), FY(GOV_Y0)), (FX(xc), FY(AGIZ_Y))], fill=BLUE, width=7)
        txt(FX(xc), FY(GOV_Y1 + hh) - 34, ad, f_l, INK)
        txt(FX(xc), FY((GOV_Y0 + GOV_Y1) / 2) - 14, "Mini-fill", f_s, BLUE)
        txt(FX(xc), FY((GOV_Y0 + GOV_Y1) / 2) + 18, pompa, f_s, BLUE)
        txt(FX(xc), FY(GOV_Y1 + hh / 2), "15 L", f_s, GRAY)
    else:
        rect(FX(x0), FY(T_KAS[1]), FX(x1), FY(T_KAS[0]), GRN_F, GRN, 4)
        rect(FX(x0), FY(T_BAS[1]), FX(x1), FY(T_BAS[0]), (240, 248, 243), GRN, 2)
        txt(FX(xc), FY(T_KAS[1]) - 34, ad, f_l, INK)
        txt(FX(xc), FY((T_KAS[0] + T_KAS[1]) / 2) - 14, "bizim kaset", f_s, GRN)
        txt(FX(xc), FY((T_KAS[0] + T_KAS[1]) / 2) + 18, "280 × 400 × 360", f_s, GRN)
        txt(FX(xc), FY((T_BAS[0] + T_BAS[1]) / 2), "kendi başlığı", f_s, GRN)
# hazne sirasi siniri + tasma
dline(FX(1500.0), FY(2260.0), FX(1500.0), FY(1060.0), RED, 3, 22, 12)
txt(FX(1500.0) + 10, FY(2240.0), "mevcut hazne sırası sonu x 1500", f_s, RED, "lm")
d.rectangle([FX(W_C), FY(2260.0), FX(X_SON + 30), FY(Y0)], outline=RED, width=2)
txt(FX((W_C + X_SON) / 2 + 15), FY(1150.0), "MODÜL F", f_s, RED)
# yukseklik tasmasi
d.line([(FX(-60), FY(Y1)), (FX(X_SON + 60), FY(Y1))], fill=RED, width=2)
for n_, (hc, hh) in HZ.items():
    yy = GOV_Y1 + hh
    dline(FX(0), FY(yy), FX(X_BAS), FY(yy), RED, 2, 12, 8)
    txt(FX(8), FY(yy) - 18, "%d L · %d (%+d)" % (n_, yy, yy - Y1), f_s, RED, "lm")
# olculer
olcu_h(FX(0), FX(W_C), FY(Y0) + 70, "1800 · modül C")
olcu_h(FX(X_BAS), FX(1500.0), FY(Y0) + 130, "1300 · mevcut hazne sırası")
olcu_h(FX(X_BAS), FX(X_SON), FY(Y0) + 190, "%d · 5 Mini-fill (296 + 10 ara) + kaşar kaseti 280" % (X_SON - X_BAS), RED)
olcu_h(FX(1500.0), FX(X_SON), FY(Y0) + 250, "+%d hazne sırasını aşıyor" % (X_SON - 1500.0), RED)
olcu_h(FX(W_C), FX(X_SON), FY(Y0) + 310, "+%d modülü aşıyor" % (X_SON - W_C), RED)
_e = yer[0]
olcu_v(FX(_e[3]) - 40, FY(GOV_Y1), FY(GOV_Y0), "228", INK, f_d, False)
olcu_v(FX(_e[3]) - 40, FY(GOV_Y1 + HZ[15][1]), FY(GOV_Y1), "495", INK, f_d, False)
olcu_h(FX(_e[3]), FX(_e[4]), FY(GOV_Y0) + 30, "296", INK)
olcu_v(FX(_e[4]) + 26, FY(GOV_Y0), FY(AGIZ_Y), "94 ağız", BLUE, f_s)
_kx = FX(W_C) + 70 + (X_SON - W_C) * S
for yy in (Y0, BOLM[0], P, AGIZ_Y, GOV_Y0, GOV_Y1, Y1, GOV_Y1 + HZ[15][1]):
    kot(FX(0) - 20, yy, "%d" % yy)

# ================================================================= YAN GÖRÜNÜŞ
txt(OXS, FY_TOP - 30, "YAN GÖRÜNÜŞ · KESİT z (ön solda)", f_h, BLUE, "ls")
rect(SZ(0), FY(Y1), SZ(-D_C), FY(Y0), None, INK, 5)
rect(SZ(0), FY(RAY_T[1]), SZ(-D_C), FY(RAY_T[0]), (244, 244, 244), LINE, 2)
rect(SZ(0), FY(BOLM[1]), SZ(-D_C), FY(BOLM[0]), None, LINE, 2)
rect(SZ(-100), FY(P), SZ(-440), FY(P - 12), TBL_F, TBL, 3)
rect(SZ(-130), FY(PIDE_UST), SZ(-410), FY(P + 8), (246, 226, 190), (170, 130, 70), 2)
dline(SZ(Z_EKSEN), FY(1290.0), SZ(Z_EKSEN), FY(2250.0), TBL, 2, 16, 10)
txt(SZ(Z_EKSEN), FY(1290.0) + 24, "tabla ekseni z −270", f_s, TBL)
rect(SZ(GOV_Z0), FY(GOV_Y1), SZ(GOV_Z1), FY(GOV_Y0), BLUE_F, BLUE, 4)
txt(SZ((GOV_Z0 + GOV_Z1) / 2), FY((GOV_Y0 + GOV_Y1) / 2), "gövde 477 × 228", f_s, BLUE)
hc, hh = HZ[15]
rect(SZ(HZ_Z + hc / 2), FY(GOV_Y1 + hh), SZ(HZ_Z - hc / 2), FY(GOV_Y1), (250, 252, 255), RED, 3)
txt(SZ(HZ_Z), FY(GOV_Y1 + hh / 2), "15 L Ø256", f_s, GRAY)
d.line([(SZ(GOV_Z0 + 5), FY(GOV_Y0 + 60)), (SZ(Z_EKSEN), FY(GOV_Y0 + 60))], fill=BLUE, width=7)
d.line([(SZ(Z_EKSEN), FY(GOV_Y0 + 60)), (SZ(Z_EKSEN), FY(AGIZ_Y))], fill=BLUE, width=7)
txt(SZ(Z_EKSEN) - 12, FY(AGIZ_Y + 30), "ağız 90° · ucu 1396", f_s, BLUE, "rm")
d.line([(SZ(20), FY(Y1)), (SZ(-D_C - 20), FY(Y1))], fill=RED, width=2)
olcu_v(SZ(-D_C) + 60, FY(GOV_Y1 + hh), FY(Y1), "+%d" % (GOV_Y1 + hh - Y1), RED, f_d)
olcu_h(SZ(0), SZ(-D_C), FY(Y0) + 70, "830")
olcu_h(SZ(GOV_Z0), SZ(GOV_Z1), FY(GOV_Y0) + 40, "477", BLUE)
olcu_h(SZ(0), SZ(GOV_Z0), FY(GOV_Y0) + 40, "230", GRAY)
olcu_h(SZ(GOV_Z1), SZ(-D_C), FY(GOV_Y0) + 40, "%d" % (GOV_Z1 + D_C), GRAY)
txt(SZ(0), FY(Y0) + 120, "ÖN · robot", f_s, GRAY, "lm")
txt(SZ(-D_C), FY(Y0) + 120, "ARKA", f_s, GRAY, "rm")

# ================================================================= ÜST GÖRÜNÜŞ
txt(OXF, PY_TOP - 30, "ÜST GÖRÜNÜŞ", f_h, BLUE, "ls")
rect(FX(0), PZ(-D_C), FX(W_C), PZ(0), None, INK, 5)
d.rectangle([FX(0), PZ(-440), FX(W_C), PZ(-100)], fill=TBL_F)
dline(FX(0), PZ(Z_EKSEN), FX(X_SON + 40), PZ(Z_EKSEN), TBL, 3, 22, 12)
txt(FX(20), PZ(-100) - 22, "tabla yolu z −100 … −440 · eksen z −270", f_s, TBL, "lm")
for ad, tip, pompa, x0, x1 in yer:
    xc = (x0 + x1) / 2
    tasti = x1 > 1500.0
    if tip == "mf":
        rect(FX(x0), PZ(GOV_Z1), FX(x1), PZ(GOV_Z0), BLUE_F, RED if tasti else BLUE, 4)
        r = HZ[15][0] / 2 * S
        d.ellipse([FX(xc) - r, PZ(HZ_Z) - r, FX(xc) + r, PZ(HZ_Z) + r], fill=(250, 252, 255), outline=RED if tasti else BLUE, width=3)
        d.ellipse([FX(xc) - 12, PZ(Z_EKSEN) - 12, FX(xc) + 12, PZ(Z_EKSEN) + 12], fill=BLUE)
        txt(FX(xc), PZ(GOV_Z1) + 30, ad, f_s, INK)
    else:
        rect(FX(x0), PZ(KASAR_Z[1]), FX(x1), PZ(KASAR_Z[0]), GRN_F, GRN, 4)
        txt(FX(xc), PZ((KASAR_Z[0] + KASAR_Z[1]) / 2), ad, f_s, GRN)
d.rectangle([FX(W_C), PZ(-D_C), FX(X_SON + 30), PZ(0)], outline=RED, width=2)
dline(FX(1500.0), PZ(-D_C) - 20, FX(1500.0), PZ(0) + 20, RED, 3, 22, 12)
olcu_h(FX(0), FX(W_C), PZ(0) + 60, "1800")
olcu_v(FX(X_SON) + 60, PZ(GOV_Z1), PZ(GOV_Z0), "477", BLUE, f_d, True)
olcu_v(FX(0) - 50, PZ(-D_C), PZ(0), "", INK, f_d, False)
txt(FX(0) - 120, PZ(-D_C / 2), "830", f_d, INK, "rm")
txt(FX(W_C / 2), PZ(0) + 110, "ÖN · robot koridoru", f_s, GRAY)
txt(FX(W_C / 2), PZ(-D_C) - 24, "ARKA", f_s, GRAY)

# ================================================================= PARÇA LİSTESİ
PX, PYL = OXS, PY_TOP + 20
txt(PX, PYL - 50, "PARÇA LİSTESİ", f_h, BLUE, "ls")
satir = [("ÜNİTE", "ADET", "ÖLÇÜ", "NOT"),
         ("Mini-fill Electric 260 W", "5", "477 × 296 × 228", "harç 1-2 · kıyma · kuşbaşı · sucuk"),
         ("hazne 15 L (tek çıkış)", "5", "Ø256 × 495", "8 L Ø256×376 → 2094 · 3 L Ø160×316 → 2034"),
         ("pompa 2 loblu", "3", "parça ≤ 15 mm", "kıyma · kuşbaşı · küp sucuk"),
         ("pompa 3 loblu", "2", "parça ≤ 10 mm", "harç 1 · harç 2"),
         ("ağız 90°", "5", "VARSAYIM", "ucu tabla ekseninde z −270"),
         ("kaşar kaseti (bizim)", "1", "280 × 400 × 360", "rende pompadan geçmez"),
         ("soğutma ceketi (Beldos)", "5", "—", "yoksa gövde +3 °C hücrede kalır")]
kol = [0, 620, 740, 1080, 1760]
for i, r_ in enumerate(satir):
    yy = PYL + 20 + i * 62
    for j, c in enumerate(r_):
        txt(PX + kol[j] + 10, yy + 31, c, F(26, i == 0), INK if i else BLUE, "lm")
    d.line([(PX, yy + 62), (PX + kol[-1], yy + 62)], fill=LINE, width=2)
d.rectangle([PX, PYL + 20, PX + kol[-1], PYL + 20 + len(satir) * 62], outline=INK, width=3)

im.save(CIKTI, dpi=(254, 254))
print("yazildi:", CIKTI, im.size, "· X_SON", X_SON, "· 15L ust", GOV_Y1 + HZ[15][1])
