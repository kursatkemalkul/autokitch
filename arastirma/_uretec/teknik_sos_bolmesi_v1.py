# -*- coding: utf-8 -*-
"""TOPPING · SOS / HARÇ BÖLMESİ v1 — ÖN + ÜST GÖRÜNÜŞ (öneri pafta) · 25 Eyl 2026

Kemal: "bir teknik yapmamız lazım, önden üstten sadece o alanı gösteren".
Öneri (sohbette anlatıldı): TOPPING'in sol ucu, iki HARÇ yuvasının yeri → Mini-fill (pizza sosu, 90° çevrik, gövde
tabla yolunun üstünde) + Beltop UNO çekirdeği (lahmacun harcı, derinliğe doğru, valf + silindir soğuk hücrede,
itici kuru bölmede, üstünde bizim 45 L hazne). Ölçüler: topping_hesap_v6 (zonlar, tabla ekseni), pafta v8
(süreç 1168), beldos_cad_v1 (makine ölçüleri). Pafta sade: yalnız görünüş + ölçü + parça adı; açıklama mesajda.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "SOS_BOLMESI_v1_teknik.png")

# ---------------------------------------------------------------- ölçüler (mm)
Y0, YUST = 1060.0, 2030.0                  # modül C taban / üst
AGIZ_R = (1070.0, 1180.0)                  # robot ağzı
TEKNE = (1061.5, 1091.5)                   # tabla teknesi (mevcut)
DISK = (1154.0, 1168.0); PIDE = (1168.0, 1176.0)
UC = 1184.0                                # yassı ağız ucu: pide üstü + 8
ZT = -170.0                                # tabla / ürün ekseni
ZON = [("ön niş", 0.0, -84.0), ("kapak", -84.0, -104.0), ("soğuk hücre", -104.0, -565.0), ("yalıtım", -565.0, -630.0), ("kuru bölme", -630.0, -830.0)]
DUVAR = 90.0                               # sol dış sac + PU
BOLME_X1 = 987.0                           # sol bölmenin sonu (kalan 4 kaset 723 mm sağda)
KIYMA = (990.0, 1130.0)
SOGUK_TABAN = 1320.0; YAL_TABAN = (1183.0, 1317.0); KASET_TAVAN = 1680.0; TEK = (1766.0, 2022.0)
TAVAN_IC = YUST - 62.0                     # yükseltilmiş bölme tavanı (PU 60 + sac)
# Mini-fill (90° çevrik: ön yüzü +x'e bakar, sol ucu modül önüne)
MF_X = (110.0, 406.0)                      # gövde (296) hat boyunca
MF_Z = (-100.0, -577.0)                    # gövde (477) derinlikte
MF_ALT = 1196.0; MF_UST = 1413.0; MF_TOPUZ = 1424.0
MF_HZ_X, MF_HZ_Z = 406.0 - 119.0, -100.0 - 136.5     # hazne ekseni (287, -236.5)
HZ0 = MF_ALT + 135.0                       # dolum ünitesi altı
MF_PROFIL = [(34.0, 77.0), (34.0, 98.3), (113.0, 143.7), (121.0, 152.0), (126.0, 163.0), (128.0, 177.8), (128.0, 478.0), (129.5, 478.0), (129.5, 488.0), (45.0, 488.0), (30.0, 494.0), (0.0, 495.5)]
MF_PORT_Y = MF_ALT + 197.8
MF_AGIZ_X = 451.0                          # sos durağı (ağız, tabla ekseninde)
MF_YAL = (1424.0, 1484.0)                  # hazne bölümünde soğuk taban yalıtımı (hazne boynu içinden geçer)
# UNO çekirdeği (derinliğe doğru; ağız önde)
UX = 730.0                                 # harç durağı (ağız, tabla ekseninde)
VZ = -387.0                                # valf ekseni z
VB = 41.0
V_ALT = SOGUK_TABAN; V_EKSEN = SOGUK_TABAN + 38.5; V_UST = SOGUK_TABAN + 72.6
HZ_X = (510.0, 950.0); HZ_Z = (-120.0, -560.0)       # bizim 45 L hazne (440 × 440)
HZ_HUNI = (1452.0, 1632.0); HZ_UST = 1832.0
V_HUNI = 180.0 / 3.0 * (64.0 ** 2 + 440.0 ** 2 + 64.0 * 440.0) / 1e6
V_DUZ = 440.0 * 440.0 * (HZ_UST - HZ_HUNI[1]) / 1e6
HZ_BRUT = V_HUNI + V_DUZ

# ---------------------------------------------------------------- çizim düzeni
S = 1.5
XA, XB = -20.0, 1090.0
FA, FB = 1040.0, 2050.0
ML, MR, MT = 330, 470, 210
GAP = 200
W = int(ML + (XB - XA) * S + MR)
FH = int((FB - FA) * S)
TH = int(840.0 * S)
H = int(MT + FH + GAP + TH + 150)
FX = lambda x: ML + (x - XA) * S
FY = lambda y: MT + (FB - y) * S
PT = MT + FH + GAP
TZ = lambda z: PT + (z + 835.0) * S

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
F_BELDOS, F_BIZ, F_TABLA, F_SOGUK, F_YAL = (228, 231, 236), (214, 230, 250), (250, 226, 196), (236, 245, 252), (238, 238, 238)
MAVI = (30, 90, 170)
im = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
f_bas, f_gor, f_et, f_ol = fn(40, True), fn(30, True), fn(22), fn(20)


def kesik(p0, p1, renk=INK, w=2, a=14, b=8):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        t1 = min(L, t + a)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w)
        t = t1 + b


def kutu(x0, x1, y0, y1, fill=None, renk=INK, w=2, gizli=False):
    X0, X1 = sorted((x0, x1)); Y0_, Y1_ = sorted((y0, y1))
    if fill: d.rectangle([X0, Y0_, X1, Y1_], fill=fill)
    if gizli:
        for p, q in (((X0, Y0_), (X1, Y0_)), ((X1, Y0_), (X1, Y1_)), ((X1, Y1_), (X0, Y1_)), ((X0, Y1_), (X0, Y0_))):
            kesik(p, q, renk, w)
    else:
        d.rectangle([X0, Y0_, X1, Y1_], outline=renk, width=w)


def taralı(x0, x1, y0, y1, adim=12):
    X0, X1 = sorted((x0, x1)); Y0_, Y1_ = sorted((y0, y1))
    d.rectangle([X0, Y0_, X1, Y1_], fill=F_YAL)
    k = X0 - (Y1_ - Y0_)
    while k < X1:
        a = (max(k, X0), Y1_ - (max(k, X0) - k)); b = (min(k + (Y1_ - Y0_), X1), Y1_ - (min(k + (Y1_ - Y0_), X1) - k))
        d.line([a, b], fill=ACIK, width=1); k += adim
    d.rectangle([X0, Y0_, X1, Y1_], outline=GRI, width=1)


def cember(cx, cy, r, fill=None, renk=INK, w=2, gizli=False):
    if fill: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    if gizli:
        n = max(24, int(r / 3))
        for i in range(0, n, 2):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            d.line([(cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=renk, width=w)
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=renk, width=w)


def ok(x, y, dx, dy, renk=INK):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * 16 - uy * 5, y - uy * 16 + ux * 5), (x - ux * 16 + uy * 5, y - uy * 16 - ux * 5)], fill=renk)


def olcu_y(x_px, y0_px, y1_px, yazi, renk=INK, sag=True):
    d.line([(x_px, y0_px), (x_px, y1_px)], fill=renk, width=2)
    ok(x_px, y0_px, 0, -1 if y0_px < y1_px else 1, renk); ok(x_px, y1_px, 0, 1 if y1_px > y0_px else -1, renk)
    tw = d.textlength(yazi, font=f_ol)
    d.text((x_px + 8 if sag else x_px - 8 - tw, (y0_px + y1_px) / 2 - 11), yazi, font=f_ol, fill=renk)


def olcu_x(y_px, x0_px, x1_px, yazi, renk=INK):
    d.line([(x0_px, y_px), (x1_px, y_px)], fill=renk, width=2)
    ok(x0_px, y_px, -1, 0, renk); ok(x1_px, y_px, 1, 0, renk)
    tw = d.textlength(yazi, font=f_ol)
    d.rectangle([(x0_px + x1_px) / 2 - tw / 2 - 4, y_px - 25, (x0_px + x1_px) / 2 + tw / 2 + 4, y_px - 3], fill=(255, 255, 255))
    d.text(((x0_px + x1_px) / 2 - tw / 2, y_px - 25), yazi, font=f_ol, fill=renk)


def kot(y_mm, yazi=None, x_mm=XA):
    y = FY(y_mm)
    d.line([(FX(x_mm) - 10, y), (FX(x_mm) + 4, y)], fill=GRI, width=2)
    t = yazi or ("%.0f" % y_mm)
    tw = d.textlength(t, font=f_ol)
    d.text((FX(x_mm) - 16 - tw, y - 11), t, font=f_ol, fill=INK)


def etiket(px, py, hx, hy, yazi, renk=INK):
    d.line([(px, py), (hx, hy)], fill=GRI, width=1)
    cember(px, py, 3, fill=GRI, renk=GRI, w=1)
    tw = d.textlength(yazi, font=f_et)
    x = hx + 6 if hx >= px else hx - 6 - tw
    d.rectangle([x - 3, hy - 14, x + tw + 3, hy + 13], fill=(255, 255, 255))
    d.text((x, hy - 13), yazi, font=f_et, fill=renk)


def kirik_x(x_mm, y0, y1):
    x = FX(x_mm); ys = [y0 + (y1 - y0) * i / 16.0 for i in range(17)]
    pts = [(x + (8 if i % 2 else -8), y) for i, y in enumerate(ys)]
    d.line(pts, fill=GRI, width=2)


# ================================================================ BAŞLIK
d.text((ML, 40), "TOPPING · SOS / HARÇ BÖLMESİ v1 — ÖN + ÜST GÖRÜNÜŞ (öneri)", font=f_bas, fill=INK)
d.text((ML, 96), "ölçüler mm · kotlar yerden · x: modül C'nin sol ucundan · z: modülün ön yüzünden (arkaya −) · Beldos makine ölçüleri broşürden (beldos_cad_v1)",
       font=f_et, fill=GRI)

# ================================================================ ÖN GÖRÜNÜŞ
d.text((ML, MT - 10 - 34), "ÖN GÖRÜNÜŞ", font=f_gor, fill=INK)
# modül dış hattı + sol duvar + kırık
kutu(FX(0), FX(1060), FY(Y0), FY(YUST), renk=INK, w=3)
taralı(FX(0), FX(DUVAR), FY(Y0), FY(YUST))
kirik_x(1060, FY(Y0) - 10, FY(YUST) + 10)
# tabla teknesi, disk, pide (sos durağında), 2. durak kesik
kutu(FX(DUVAR), FX(1060), FY(TEKNE[0]), FY(TEKNE[1]), fill=F_YAL, renk=GRI, w=1)
for cx, gz in ((MF_AGIZ_X, False), (UX, True)):
    kutu(FX(cx - 170), FX(cx + 170), FY(DISK[0]), FY(DISK[1]), fill=None if gz else F_TABLA, renk=INK, w=2, gizli=gz)
    kutu(FX(cx - 140), FX(cx + 140), FY(PIDE[0]), FY(PIDE[1]), fill=None if gz else (240, 200, 150), renk=INK, w=1, gizli=gz)
for y in AGIZ_R:
    kesik((FX(DUVAR), FY(y)), (FX(1060), FY(y)), GRI, 1)
# kaset tarafı: yalıtım tabanı, soğuk hücre, kıyma kaseti, teknik bant
taralı(FX(480), FX(1060), FY(YAL_TABAN[0]), FY(YAL_TABAN[1]))
kutu(FX(BOLME_X1), FX(1060), FY(SOGUK_TABAN), FY(KASET_TAVAN), fill=F_SOGUK, renk=GRI, w=1)
kutu(FX(KIYMA[0]), FX(1060), FY(SOGUK_TABAN + 10), FY(SOGUK_TABAN + 360), fill=(245, 245, 245), renk=INK, w=2)
taralı(FX(BOLME_X1), FX(1060), FY(KASET_TAVAN), FY(KASET_TAVAN + 60))
kutu(FX(BOLME_X1), FX(1060), FY(TEK[0]), FY(TEK[1]), fill=(250, 250, 250), renk=GRI, w=1)
taralı(FX(BOLME_X1 - 60), FX(BOLME_X1), FY(KASET_TAVAN), FY(TAVAN_IC))
# yükseltilmiş bölme: tavan yalıtımı + soğuk hacim
taralı(FX(DUVAR), FX(BOLME_X1), FY(TAVAN_IC), FY(YUST - 1.5))
kutu(FX(480), FX(BOLME_X1 - 60), FY(SOGUK_TABAN), FY(TAVAN_IC), fill=F_SOGUK, renk=GRI, w=1)
d.rectangle([FX(BOLME_X1 - 61), FY(KASET_TAVAN), FX(BOLME_X1 + 1), FY(SOGUK_TABAN) - 1], fill=F_SOGUK)
kutu(FX(DUVAR), FX(480), FY(MF_YAL[1]), FY(TAVAN_IC), fill=F_SOGUK, renk=GRI, w=1)
taralı(FX(DUVAR), FX(MF_HZ_X - 118), FY(MF_YAL[0]), FY(MF_YAL[1]))
taralı(FX(MF_HZ_X + 118), FX(480), FY(MF_YAL[0]), FY(MF_YAL[1]))
taralı(FX(460), FX(480), FY(SOGUK_TABAN), FY(MF_YAL[1]))
# --- Mini-fill (sol ucu görünüyor)
kutu(FX(MF_X[0]), FX(MF_X[1]), FY(MF_ALT + 17), FY(MF_UST), fill=F_BELDOS, renk=INK, w=3)
kutu(FX(MF_X[0] + 4), FX(MF_X[1] - 4), FY(MF_ALT + 17), FY(MF_ALT + 45), fill=(60, 60, 64), renk=INK, w=1)
for x in (MF_X[0] + 30, MF_X[1] - 30):
    kutu(FX(x - 15), FX(x + 15), FY(MF_ALT), FY(MF_ALT + 17), fill=(60, 60, 64), renk=INK, w=1)
kutu(FX(212 - 12), FX(212 + 12), FY(MF_UST), FY(MF_TOPUZ), fill=(60, 60, 64), renk=INK, w=1)
kutu(FX(MF_X[1] - 174), FX(MF_X[1]), FY(HZ0), FY(MF_UST), gizli=True, renk=GRI)                  # pompa cebi
kutu(FX(MF_X[1] - 157), FX(MF_X[1] - 9), FY(HZ0), FY(HZ0 + 77), fill=(225, 238, 246), renk=MAVI, w=2)   # şeffaf pompa bloğu
pts = [(FX(MF_HZ_X + r), FY(HZ0 + z)) for r, z in MF_PROFIL] + [(FX(MF_HZ_X - r), FY(HZ0 + z)) for r, z in reversed(MF_PROFIL)]
d.polygon(pts, fill=(247, 247, 247), outline=INK)
d.line(pts + [pts[0]], fill=INK, width=2)
# çıkış ağzı → yatay boru → dik → yassı ağız
kutu(FX(MF_X[1] - 9), FX(MF_X[1] + 14), FY(MF_PORT_Y - 19.5), FY(MF_PORT_Y + 19.5), fill=(225, 238, 246), renk=MAVI, w=2)
kutu(FX(MF_X[1] + 14), FX(MF_AGIZ_X + 10), FY(MF_PORT_Y - 10), FY(MF_PORT_Y + 10), fill=F_BELDOS, renk=INK, w=2)
kutu(FX(MF_AGIZ_X - 10), FX(MF_AGIZ_X + 10), FY(UC + 40), FY(MF_PORT_Y + 10), fill=F_BELDOS, renk=INK, w=2)
d.polygon([(FX(MF_AGIZ_X - 10), FY(UC + 40)), (FX(MF_AGIZ_X + 10), FY(UC + 40)), (FX(MF_AGIZ_X + 25), FY(UC)), (FX(MF_AGIZ_X - 25), FY(UC))], fill=F_BELDOS, outline=INK)
# --- UNO çekirdeği (ağız ucu görünüyor) + bizim hazne
kutu(FX(UX - VB), FX(UX + VB), FY(V_ALT), FY(V_UST), fill=F_BELDOS, renk=INK, w=3)
kutu(FX(UX - VB - 25), FX(UX - VB), FY(V_EKSEN - 20), FY(V_EKSEN + 20), fill=(60, 60, 64), renk=INK, w=1)
kutu(FX(UX + VB), FX(UX + VB + 50), FY(V_EKSEN - 22), FY(V_EKSEN + 22), fill=F_BIZ, renk=MAVI, w=2)
cember(FX(UX), FY(V_EKSEN), 29.5 * S, fill=F_BELDOS, renk=INK, w=2)
cember(FX(UX), FY(V_EKSEN), 18 * S, fill=(214, 216, 220), renk=INK, w=2)
kutu(FX(UX - 18), FX(UX + 18), FY(UC + 40), FY(V_EKSEN - 18), fill=F_BELDOS, renk=INK, w=2)
d.polygon([(FX(UX - 18), FY(UC + 40)), (FX(UX + 18), FY(UC + 40)), (FX(UX + 25), FY(UC)), (FX(UX - 25), FY(UC))], fill=F_BELDOS, outline=INK)
kutu(FX(UX - 32), FX(UX + 32), FY(V_UST), FY(HZ_HUNI[0]), fill=F_BELDOS, renk=INK, w=2)
kutu(FX(UX - 45.5), FX(UX + 45.5), FY(V_UST + 18), FY(V_UST + 35), fill=F_BELDOS, renk=INK, w=2)
d.polygon([(FX(UX - 32), FY(HZ_HUNI[0])), (FX(UX + 32), FY(HZ_HUNI[0])), (FX(HZ_X[1]), FY(HZ_HUNI[1])), (FX(HZ_X[1]), FY(HZ_UST)),
           (FX(HZ_X[0]), FY(HZ_UST)), (FX(HZ_X[0]), FY(HZ_HUNI[1]))], fill=F_BIZ, outline=MAVI)
d.line([(FX(UX - 32), FY(HZ_HUNI[0])), (FX(HZ_X[0]), FY(HZ_HUNI[1])), (FX(HZ_X[0]), FY(HZ_UST)), (FX(HZ_X[1]), FY(HZ_UST)),
        (FX(HZ_X[1]), FY(HZ_HUNI[1])), (FX(UX + 32), FY(HZ_HUNI[0]))], fill=MAVI, width=3)
# --- kotlar
for y, t in [(Y0, None), (SOGUK_TABAN, "1320 soğuk taban"), (MF_UST, "1413"), (TAVAN_IC, "1968 bölme tavanı"), (YUST, None)]:
    kot(y, t)


def kot_yigin(liste, y_bas):
    for i, (y_mm, t) in enumerate(liste):
        yt = y_bas + i * 28
        d.line([(FX(XA) - 10, FY(y_mm)), (FX(XA) + 4, FY(y_mm))], fill=GRI, width=2)
        d.line([(FX(XA) - 14, yt), (FX(XA) - 10, FY(y_mm))], fill=GRI, width=1)
        tw = d.textlength(t, font=f_ol)
        d.text((FX(XA) - 18 - tw, yt - 11), t, font=f_ol, fill=INK)


kot_yigin([(MF_ALT, "1196 Mini-fill altı"), (UC, "1184 ağız ucu"), (AGIZ_R[1], "1180 robot ağzı üstü"), (PIDE[1], "1176 pide üstü"), (DISK[1], "1168 süreç")], FY(MF_ALT) - 40)
kot_yigin([(HZ_UST, "1832 harç haznesi"), (HZ0 + 495.5, "1826 Mini-fill haznesi")], FY(HZ_UST) - 20)
# --- ölçüler (alt)
yb = FY(FA) + 14
olcu_x(yb + 10, FX(MF_X[0]), FX(MF_X[1]), "296")
olcu_x(yb + 48, FX(0), FX(MF_AGIZ_X), "451")
olcu_x(yb + 86, FX(0), FX(UX), "730")
olcu_x(yb + 124, FX(DUVAR), FX(BOLME_X1), "bölme 897")
olcu_x(FY(HZ_UST) - 26, FX(HZ_X[0]), FX(HZ_X[1]), "440")
# --- parça adları (ön)
R = FX(1060) + 40
etiket(FX(MF_HZ_X + 60), FY(1700), R - 700, FY(1990), "Mini-fill 15 L hazne (sos)")
etiket(FX(MF_X[0] + 40), FY(1300), FX(XA) + 40, FY(1560), "Mini-fill güç ünitesi · 90° çevrik")
etiket(FX(MF_X[1] - 80), FY(HZ0 + 40), FX(XA) + 40, FY(1500), "şeffaf pompa bloğu (2/3 lob)")
etiket(FX(MF_AGIZ_X + 20), FY(UC + 10), FX(MF_AGIZ_X) - 60, FY(1110), "yassı ağız (Mini-fill layering spout)")
etiket(FX(HZ_X[1] - 60), FY(1740), R, FY(1880), "harç haznesi 45 L (bizim, soğuk hücrede)", MAVI)
etiket(FX(UX + VB + 30), FY(V_EKSEN), R, FY(1480), "valf döndürme tahriki (bizim)", MAVI)
etiket(FX(UX - VB + 10), FY(V_ALT + 20), R, FY(1420), "UNO valf bloğu (Beldos)")
etiket(FX(UX + 20), FY(UC + 12), R, FY(1230), "yassı ağız (Beltop spreader)")
etiket(FX(1040), FY(1500), R, FY(1600), "KIYMA kaseti (kalan 4 kasetin ilki)")
etiket(FX(1040), FY(1900), R, FY(1960), "teknik bant (kasetlerin üstünde)")
etiket(FX(900), FY(1250), R, FY(1300), "yalıtım tabanı (mevcut)")
etiket(FX(1000), FY(1076), R, FY(1100), "tabla teknesi + ray (mevcut)")
etiket(FX(UX + 150), FY(DISK[0] + 7), R, FY(1150), "tabla Ø340 · 2. durak (harç)")

# ================================================================ ÜST GÖRÜNÜŞ
d.text((ML, PT - 10 - 34), "ÜST GÖRÜNÜŞ", font=f_gor, fill=INK)
kutu(FX(0), FX(1060), TZ(0), TZ(-830), renk=INK, w=3)
taralı(FX(0), FX(DUVAR), TZ(-830), TZ(0))
kirik_x(1060, TZ(-830) - 10, TZ(0) + 10)
for ad, z0, z1 in ZON:
    d.line([(FX(DUVAR), TZ(z1)), (FX(1060), TZ(z1))], fill=ACIK, width=1)
taralı(FX(480), FX(1060), TZ(-565), TZ(-630))
# tabla ekseni + tablalar
x = FX(DUVAR)
while x < FX(1060):
    d.line([(x, TZ(ZT)), (min(x + 26, FX(1060)), TZ(ZT))], fill=GRI, width=2); x += 38
for cx, gz in ((MF_AGIZ_X, False), (UX, True)):
    cember(FX(cx), TZ(ZT), 170 * S, fill=None, renk=(200, 140, 70), w=2, gizli=gz)
    cember(FX(cx), TZ(ZT), 140 * S, fill=None, renk=(200, 140, 70), w=1, gizli=True)
# Mini-fill
kutu(FX(MF_X[0]), FX(MF_X[1]), TZ(MF_Z[0]), TZ(MF_Z[1]), fill=F_BELDOS, renk=INK, w=3)
kutu(FX(MF_X[1] - 174), FX(MF_X[1]), TZ(-159.0), TZ(-314.0), gizli=True, renk=GRI)
kutu(FX(MF_X[1] - 157), FX(MF_X[1] - 9), TZ(-162.0), TZ(-311.0), fill=(225, 238, 246), renk=MAVI, w=2)
kutu(FX(406 - 189), FX(406 - 55), TZ(-375.0), TZ(-559.0), fill=(200, 200, 204), renk=INK, w=1)
cember(FX(MF_HZ_X), TZ(MF_HZ_Z), 128 * S, renk=INK, w=2, gizli=True)
cember(FX(212), TZ(-176.0), 12 * S, fill=(60, 60, 64), renk=INK, w=1)
d.line([(FX(MF_X[1] + 10), TZ(MF_HZ_Z)), (FX(MF_AGIZ_X), TZ(ZT))], fill=INK, width=int(20 * S))
d.line([(FX(MF_X[1] + 10), TZ(MF_HZ_Z)), (FX(MF_AGIZ_X), TZ(ZT))], fill=F_BELDOS, width=int(20 * S) - 4)
kutu(FX(MF_AGIZ_X - 25), FX(MF_AGIZ_X + 25), TZ(ZT + 4), TZ(ZT - 4), fill=INK, renk=INK, w=1)
# UNO + bizim hazne + tahrik
kutu(FX(HZ_X[0]), FX(HZ_X[1]), TZ(HZ_Z[0]), TZ(HZ_Z[1]), renk=MAVI, w=2, gizli=True)
for cx, cz in ((HZ_X[0], HZ_Z[0]), (HZ_X[1], HZ_Z[0]), (HZ_X[0], HZ_Z[1]), (HZ_X[1], HZ_Z[1])):
    kesik((FX(cx), TZ(cz)), (FX(UX + (32 if cx > UX else -32)), TZ(VZ + (32 if cz > VZ else -32))), MAVI, 1)
kutu(FX(UX - VB), FX(UX + VB), TZ(VZ + VB), TZ(VZ - VB), fill=F_BELDOS, renk=INK, w=3)
kutu(FX(UX - VB - 25), FX(UX - VB), TZ(VZ + 20), TZ(VZ - 20), fill=(60, 60, 64), renk=INK, w=1)
kutu(FX(UX + VB), FX(UX + VB + 50), TZ(VZ + 25), TZ(VZ - 25), fill=F_BIZ, renk=MAVI, w=2)
kutu(FX(UX - 18), FX(UX + 18), TZ(VZ + VB), TZ(-251.0), fill=F_BELDOS, renk=INK, w=2)
kutu(FX(UX - 29.5), FX(UX + 29.5), TZ(-251.0), TZ(-227.0), fill=F_BELDOS, renk=INK, w=2)
kutu(FX(UX - 18), FX(UX + 18), TZ(-227.0), TZ(ZT - 18), fill=F_BELDOS, renk=INK, w=2)
kutu(FX(UX - 25), FX(UX + 25), TZ(ZT + 4), TZ(ZT - 4), fill=INK, renk=INK, w=1)
kutu(FX(UX - 29), FX(UX + 29), TZ(VZ - VB), TZ(-559.0), fill=(232, 236, 242), renk=INK, w=2)
kutu(FX(UX - 6), FX(UX + 6), TZ(-559.0), TZ(-640.0), fill=F_BELDOS, renk=INK, w=1)
kutu(FX(UX - 30), FX(UX + 30), TZ(-640.0), TZ(-820.0), fill=F_BIZ, renk=MAVI, w=2)
kutu(FX(UX + 40), FX(UX + 97), TZ(-650.0), TZ(-726.0), fill=F_BIZ, renk=MAVI, w=2)
kutu(FX(KIYMA[0]), FX(1060), TZ(-200.0), TZ(-525.0), fill=(245, 245, 245), renk=INK, w=2)
# ölçüler (üst)
xr = FX(1060) + 30
for z, t in [(0, "0 ön yüz"), (-84, "−84"), (-104, "−104"), (ZT, "−170 tabla ekseni"), (VZ, "−387 valf"), (-565, "−565"), (-630, "−630"), (-830, "−830")]:
    d.line([(FX(1060) + 4, TZ(z)), (xr, TZ(z))], fill=GRI, width=1)
    d.text((xr + 6, TZ(z) - 11), t, font=f_ol, fill=INK)
olcu_y(FX(MF_X[0]) - 30, TZ(MF_Z[0]), TZ(MF_Z[1]), "477", sag=False)
olcu_y(FX(MF_X[0]) - 90, TZ(0), TZ(MF_Z[0]), "100", sag=False)
olcu_x(TZ(HZ_Z[0]) - 12, FX(HZ_X[0]), FX(HZ_X[1]), "440")
# parça adları (üst)
L_ = FX(XA) + 20
etiket(FX(MF_X[0] + 60), TZ(-450.0), L_, TZ(-470.0), "Mini-fill güç ünitesi")
etiket(FX(300), TZ(-470.0), L_, TZ(-420.0), "dokunmatik ekran")
etiket(FX(MF_X[1] - 60), TZ(-240.0), L_, TZ(-300.0), "pompa bloğu + çıkış")
etiket(FX(UX + 25), TZ(-500.0), xr + 190, TZ(-490.0), "ürün silindiri Ø52 (Beldos)")
etiket(FX(UX + 20), TZ(-730.0), xr + 190, TZ(-700.0), "step motor + vidalı mil (bizim)", MAVI)
etiket(FX(UX + 6), TZ(-600.0), xr + 190, TZ(-600.0), "mil · yalıtımdan keçeli geçiş")
etiket(FX(UX + 60), TZ(-300.0), xr + 190, TZ(-260.0), "90° ağız + TC kelepçe")
etiket(FX(MF_AGIZ_X + 160), TZ(ZT + 60), xr + 190, TZ(-40.0), "tabla Ø340 · pide Ø280")
d.text((xr + 190, TZ(-150.0) - 60), "", font=f_et, fill=INK)
# ağız durakları işareti
for cx, t in ((MF_AGIZ_X, "SOS"), (UX, "HARÇ")):
    tw = d.textlength(t, font=f_gor)
    d.text((FX(cx) - tw / 2, TZ(0) + 16), t, font=f_gor, fill=INK)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
print("PNG", CIKTI, im.size)
print("harç haznesi: huni %.1f L + düz %.1f L = brüt %.1f L (45 L = %%%.0f doluluk)" % (V_HUNI, V_DUZ, HZ_BRUT, 45.0 / HZ_BRUT * 100))
