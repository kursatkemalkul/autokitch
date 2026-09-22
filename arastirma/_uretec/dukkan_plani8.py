# -*- coding: utf-8 -*-
"""DUKKAN PLANI v8 (17 Eyl 2026) — v7 mantigi (hat arkada · onunde robot koridoru · ince duvar · onde kapi + tezgah + servis + teslim dolabi cephede)
HAT_2KOL_v9 ile: hat 350 (A 70 · B/C 140 · D 70 · E 70), 2 sabit kol, karton kulesi hattin ucunda hucre icinde, QR dolabi cephede sag ucta (arkasi koridor kivrimina acik),
mini tezgah 80 x 40 + ust dolap, el lavabosu sol duvarda, kapi disa acilir. Olculer cm. Kural: paftada yalniz gorunus + olcu + parca.
Robot: acik cekmece (700 mm) R1 kaidesine carpmasin diye koridor 120, R1 z 88; QR dolabi cephede oldugu icin R2 de uzak -> IKI KOL DA FR20 (1.854 mm, pratik 167 cm).
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v8.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3400, 2500
S = 3.0                                                     # px / cm
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, SU, DUV, KOR, CAM = (14, 120, 90), (190, 190, 196), (214, 236, 250), (200, 200, 205), (235, 241, 250), (200, 225, 250)
TEZ, AGZ = (250, 238, 220), (253, 244, 243)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(50, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v):
    return ("%g" % v).replace(".", ",")


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def dline(p0, p1, c, w=1, dash=7, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0 = min(1.0, i * (dash + gap) / L)
        t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def darc(cx, cy, r, a0, a1, c, w=2, adim=4.0):
    a = a0
    while a < a1:
        b = min(a1, a + adim)
        d.arc([cx - r, cy - r, cx + r, cy + r], a, b, fill=c, width=w)
        a = b + adim


# ======================= VERI (cm) =======================
HAT_D, KOR_D, DUV_D, ON_D = 83.0, 120.0, 6.0, 84.0           # hat · robot koridoru · ince duvar · on zon (tezgah 30 + gecit 54)
IC_W = 390.0
IC_D = HAT_D + KOR_D + DUV_D + ON_D                          # 293
MOD = [("A · PRESS", 0.0, 70.0), ("B · ÇEKMECE  +  C · TOPPING", 70.0, 210.0), ("D · FIRIN", 210.0, 280.0), ("E · KUTU", 280.0, 350.0)]
KULE = (350.0, 390.0, 3.0, 83.0)                            # karton kulesi 40 x 80, hucre icinde
Y_KOR0, Y_KOR1 = HAT_D, HAT_D + KOR_D                       # 83 .. 203
Y_DUV1 = Y_KOR1 + DUV_D                                     # 209
Y_ON = IC_D                                                 # 293 = cephe
R1 = (105.0, Y_KOR0 + 88.0, "R1 · FR20", "z 88 · açık çekmece 70 + 4 + 10")
R2 = (300.0, Y_KOR0 + 67.0, "R2 · FR20", "fırın · kutu · QR")
ERIS = 167.0                                                # FR20 pratik (cm)
AKT = (190.0, 230.0, Y_KOR0 + 16.0, Y_KOR0 + 56.0)
KAPI = (0.0, 75.0)
TEZ = (75.0, 215.0, Y_ON - 30.0, Y_ON)
PEN = (80.0, 210.0)
MINI = (215.0, 295.0, Y_ON - 40.0, Y_ON)
QR = (304.0, 390.0, Y_ON - 52.0, Y_ON)
LAV = (0.0, 30.0, Y_DUV1 + 6.0, Y_DUV1 + 41.0)             # el lavabosu sol duvarda 30 derin x 35
DUV_X1 = QR[0]                                              # ince duvar 0..304; QR bolgesi koridora acik

OX, OY = 140.0, 330.0


def X(x):
    return OX + x * S


def Y(y):
    return OY + y * S


# ======================= BASLIK =======================
txt(OX, 60, "AUTOKITCH  ·  DÜKKAN v8  ·  PLAN + SOKAK CEPHESİ  ·  HAT 2 KOL v9 ile  ·  iç 390 × 293 = 11,4 m²", f38, INK)
txt(OX, 122, "v7 mantığı: hat arka duvarda · önünde robot koridoru 120 · ince duvar · ön zon 84 = tezgâh 30 + geçit 54 · teslim dolabı cephede sağ uçta, arkası koridor kıvrımına açık · karton kulesi hücre içinde hat ucunda · ölçüler cm · 17 Eylül 2026", f13, GRAY)
d.line([(OX, 160), (W_PX - 140, 160)], fill=LINE, width=3)

# ======================= PLAN =======================
txt(OX, OY - 110, "PLAN (üstten)", f16, ACC)
d.rectangle([X(-12), Y(-12), X(IC_W + 12), Y(IC_D)], fill=DUV, outline=LINE, width=3)         # dis duvar
d.rectangle([X(0), Y(0), X(IC_W), Y(IC_D)], fill=BG, outline=LINE, width=3)
txt(X(IC_W / 2), Y(HAT_D) + 12, "arka duvar boyunca hat · 830 derin", f7, GRAY, "mm")
# hat
for ad, x0, x1 in MOD:
    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_D)], fill=FILL, outline=LINE, width=3)
    txt(X((x0 + x1) / 2), Y(HAT_D / 2), ad, f11, INK, "mm")
    txt(X((x0 + x1) / 2), Y(HAT_D / 2) + 24, "%s × 83" % sayi(x1 - x0), f7, GRAY, "mm")
d.rectangle([X(KULE[0]), Y(KULE[2]), X(KULE[1]), Y(KULE[3])], fill=BG, outline=LINE, width=2)
txt(X(370), Y(38), "KARTON", f7, INK, "mm"); txt(X(370), Y(52), "KULESİ", f7, INK, "mm"); txt(X(370), Y(66), "40 × 80 × 200", f7, GRAY, "mm")
# koridor
d.rectangle([X(0), Y(Y_KOR0), X(IC_W), Y(Y_KOR1)], fill=KOR, outline=None)
d.rectangle([X(DUV_X1), Y(Y_KOR1), X(IC_W), Y(QR[2])], fill=KOR, outline=None)              # kivrim: QR arkasi
txt(X(60), Y(Y_KOR0 + 8), "ROBOT KORİDORU 120 · hücre kapalı, eleman kapısı ince duvarda", f9, ACC, "la")
# aktarma rafi
d.rectangle([X(AKT[0]), Y(AKT[2]), X(AKT[1]), Y(AKT[3])], fill=BG, outline=ACC, width=2)
txt(X(210), Y(AKT[2] + 14), "AKTARMA", f7, ACC, "mm"); txt(X(210), Y(AKT[2] + 28), "RAFI 40 × 40", f7, GRAY, "mm")
# robotlar
lay = Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0))
ld = ImageDraw.Draw(lay)
for rx, ry, ad, alt in (R1, R2):
    a = 0.0
    while a < 360.0:
        ld.arc([X(rx) - ERIS * S, Y(ry) - ERIS * S, X(rx) + ERIS * S, Y(ry) + ERIS * S], a, min(360.0, a + 2.0), fill=ACC + (255,), width=2)
        a += 4.0
box = (int(X(0)) + 2, int(Y(0)) + 2, int(X(IC_W)) - 2, int(Y(IC_D)) - 2)
im.paste(lay.crop(box), box[:2], lay.crop(box))
d = ImageDraw.Draw(im)
for rx, ry, ad, alt in (R1, R2):
    d.rectangle([X(rx - 20), Y(ry - 20), X(rx + 20), Y(ry + 20)], fill=SOFT, outline=ACC, width=1)
    d.ellipse([X(rx) - 10 * S, Y(ry) - 10 * S, X(rx) + 10 * S, Y(ry) + 10 * S], fill=BG, outline=ACC, width=3)
    txt(X(rx), Y(ry - 30), ad, f9, ACC, "mm"); txt(X(rx), Y(ry - 22), alt, f7, GRAY, "mm")
txt(X(20), Y(Y_KOR1 - 10), "kesik daire = FR20 pratik erişim 167 (iç mekâna kırpıldı)", f7, ACC, "la")
# ince duvar (0..304) + eleman kapisi
d.rectangle([X(0), Y(Y_KOR1), X(DUV_X1), Y(Y_DUV1)], fill=DUV, outline=LINE, width=1)
d.rectangle([X(40), Y(Y_KOR1 - 1), X(110), Y(Y_DUV1 + 1)], fill=AGZ, outline=RED, width=2)
txt(X(75), Y(Y_DUV1 + 8), "HÜCRE KAPISI 70 · kilitli", f7, RED, "mm")
d.line([(X(DUV_X1), Y(Y_KOR1)), (X(DUV_X1), Y(QR[2]))], fill=LINE, width=3)                 # QR arkasi bolme duvari
txt(X(347), Y(Y_KOR1 + 18), "koridor kıvrımı 86 × 38", f7, ACC, "mm")
# on zon
txt(X(175), Y(Y_DUV1 + 14), "ELEMAN GEÇİDİ 54", f8, GRAY, "mm")
d.rectangle([X(TEZ[0]), Y(TEZ[2]), X(TEZ[1]), Y(TEZ[3])], fill=TEZ_C if False else (250, 238, 220), outline=INK, width=2)
txt(X(145), Y(TEZ[2] + 15), "TEZGÂH 140 × 30 — sokağa bakar · sürme cam 130", f8, INK, "mm")
d.rectangle([X(PEN[0]), Y(IC_D - 4), X(PEN[1]), Y(IC_D + 2)], fill=CAM, outline=ACC, width=1)
d.rectangle([X(MINI[0]), Y(MINI[2]), X(MINI[1]), Y(MINI[3])], fill=(250, 238, 220), outline=INK, width=2)
d.rectangle([X(255), Y(MINI[2] + 2), X(293), Y(MINI[3] - 2)], fill=SU, outline=ACC, width=1)
txt(X(235), Y(MINI[2] + 14), "DOLDURMA", f7, INK, "mm"); txt(X(235), Y(MINI[2] + 27), "40 × 40", f7, GRAY, "mm")
txt(X(274), Y(MINI[2] + 14), "EVYE", f7, ACC, "mm"); txt(X(274), Y(MINI[2] + 27), "40 × 40", f7, GRAY, "mm")
drect(X(MINI[0]), Y(MINI[3] - 35), X(MINI[1]), Y(MINI[3]), GRAY, 1)
txt(X(255), Y(MINI[2] - 8), "üstünde dolap 80 × 35 · kot 140", f7, GRAY, "mm")
d.rectangle([X(QR[0]), Y(QR[2]), X(QR[1]), Y(QR[3])], fill=FILL, outline=INK, width=3)
txt(X(347), Y(QR[2] + 14), "QR DOLABI 86 × 52", f8, INK, "mm"); txt(X(347), Y(QR[2] + 28), "12 göz · robot arkadan yükler", f7, GRAY, "mm"); txt(X(347), Y(QR[2] + 42), "müşteri cepheden alır · panel cephede", f7, GRAY, "mm")
d.rectangle([X(LAV[0]), Y(LAV[2]), X(LAV[1]), Y(LAV[3])], fill=SU, outline=ACC, width=1)
txt(X(50), Y(LAV[2] + 10), "EL LAVABOSU", f7, ACC, "la"); txt(X(50), Y(LAV[2] + 24), "35 × 30 · duvarda", f7, GRAY, "la")
# kapi (disa acilir)
d.rectangle([X(KAPI[0]), Y(IC_D - 2), X(KAPI[1]), Y(IC_D + 12)], fill=BG, outline=INK, width=2)
d.arc([X(0) - 75 * S, Y(IC_D) - 75 * S + 12, X(0) + 75 * S, Y(IC_D) + 75 * S + 12], 0, 90, fill=GRAY, width=1)
txt(X(37), Y(IC_D + 24), "KAPI 75 · dışa açılır", f7, INK, "mm")
# yangin + kamera
d.rectangle([X(130), Y(Y_KOR1 + 1), X(140), Y(Y_DUV1 - 1)], fill=RED)
d.rectangle([X(145), Y(Y_KOR1 + 1), X(155), Y(Y_DUV1 - 1)], fill=(140, 140, 150))
txt(X(142), Y(Y_DUV1 + 30), "söndürücü ×2", f7, GRAY, "mm")
for cx_, cy_, adk in ((6.0, 6.0, "K1"), (384.0, Y_KOR1 - 6.0, "K2"), (6.0, IC_D - 6.0, "K3"), (300.0, IC_D - 6.0, "K4")):
    d.ellipse([X(cx_) - 6, Y(cy_) - 6, X(cx_) + 6, Y(cy_) + 6], fill=INK)
    txt(X(cx_) + 10, Y(cy_), adk, f7, INK, "lm")
txt(X(IC_W / 2), Y(IC_D) + 50, "KALDIRIM / SOKAK — müşteri burada durur", f9, GRAY, "mm")
# olculer
olcu_v(X(IC_W) + 40, Y(0), Y(HAT_D), "hat 83", f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR0), Y(Y_KOR1), "robot 120", f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR1), Y(Y_DUV1), "6", f7, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_DUV1), Y(IC_D), "ön 84", f8, INK, "r")
olcu_v(X(IC_W) + 120, Y(0), Y(IC_D), sayi(IC_D), f11, INK, "r")
olcu_v(X(0) - 40, Y(Y_DUV1), Y(TEZ[2]), "geçit 54", f7, INK, "l")
olcu_v(X(0) - 40, Y(TEZ[2]), Y(IC_D), "tezgâh 30", f7, INK, "l")
yb = Y(IC_D) + 90
for x0, x1, s_ in ((0, 75, "kapı 75"), (75, 215, "tezgâh 140"), (215, 295, "servis 80"), (295, 304, "9"), (304, 390, "QR 86")):
    olcu_h(X(x0), X(x1), yb, s_, f8, INK)
olcu_h(X(0), X(IC_W), yb + 40, "%s" % sayi(IC_W), f11, INK)
for ad, x0, x1 in MOD:
    olcu_h(X(x0), X(x1), Y(0) - 24, sayi(x1 - x0), f7, GRAY)
olcu_h(X(350), X(390), Y(0) - 24, "40", f7, GRAY)
olcu_h(X(0), X(350), Y(0) - 56, "HAT 350", f9, INK)

# ======================= SOKAK CEPHESI =======================
CY = Y(IC_D) + 260
txt(OX, CY - 60, "SOKAK CEPHESİ (önden) · duvar boyu 300", f16, ACC)
H_C = 300.0


def Yc(z):
    return CY + (H_C - z) * S


d.rectangle([X(0), Yc(H_C), X(IC_W), Yc(0)], fill=SOFT, outline=LINE, width=3)
d.line([(X(-12), Yc(0)), (X(IC_W + 12), Yc(0))], fill=INK, width=4)
d.rectangle([X(0), Yc(210), X(75), Yc(0)], fill=BG, outline=INK, width=2)
d.rectangle([X(66), Yc(108), X(69), Yc(96)], fill=INK)
txt(X(37), Yc(110), "KAPI 75 × 210", f8, INK, "mm"); txt(X(37), Yc(96), "dışa açılır", f7, GRAY, "mm")
d.rectangle([X(PEN[0]), Yc(200), X(PEN[1]), Yc(100)], fill=CAM, outline=ACC, width=2)
d.line([(X(145), Yc(200)), (X(145), Yc(100))], fill=ACC, width=1)
txt(X(145), Yc(155), "PENCERE 130 × 100 · sürme cam · eşik 100", f8, ACC, "mm")
txt(X(145), Yc(85), "tezgâh sokağa bakar", f7, GRAY, "mm")
txt(X(255), Yc(150), "kapalı cephe", f7, GRAY, "mm"); txt(X(255), Yc(136), "(servis arkası)", f7, GRAY, "mm")
d.rectangle([X(QR[0]), Yc(165), X(QR[1]), Yc(0)], fill=FILL, outline=INK, width=3)
for r in range(6):
    z0 = 35.0 + r * 20.0
    for c in range(2):
        d.rectangle([X(QR[0] + 3 + c * 41), Yc(z0 + 19), X(QR[0] + 42 + c * 41), Yc(z0)], fill=BG, outline=INK, width=1)
        d.rectangle([X(QR[0] + 38 + c * 41), Yc(z0 + 11), X(QR[0] + 40 + c * 41), Yc(z0 + 8)], fill=INK)
txt(X(QR[1]) - 6, Yc(176), "QR DOLABI 86 × 165", f8, INK, "ra"); txt(X(QR[1]) - 6, Yc(164), "12 göz · kot 35–155", f7, GRAY, "ra")
d.rectangle([X(QR[0] + 3), Yc(196), X(QR[0] + 25), Yc(156)], fill=BG, outline=ACC, width=2)
txt(X(QR[0] + 14), Yc(190), "PANEL", f7, ACC, "mm"); txt(X(QR[0] + 14), Yc(178), "ekran", f7, GRAY, "mm"); txt(X(QR[0] + 14), Yc(168), "QR · PIN", f7, GRAY, "mm")
txt(X(QR[0] + 14), Yc(150), "kot 156–196", f7, GRAY, "mm")
d.ellipse([X(300) - 6, Yc(290) - 6, X(300) + 6, Yc(290) + 6], fill=INK)
txt(X(300) + 10, Yc(290), "K4 kamera", f7, INK, "lm")
olcu_v(X(IC_W) + 40, Yc(H_C), Yc(0), "300", f9, INK, "r")
for x0, x1, s_ in ((0, 75, "75"), (80, 210, "130"), (304, 390, "86")):
    olcu_h(X(x0), X(x1), Yc(0) + 40, s_, f8, INK)
olcu_h(X(0), X(IC_W), Yc(0) + 80, sayi(IC_W), f11, INK)

# ======================= ALANLAR · ERISIM (sag panel) =======================
PX0 = X(IC_W) + 260
d.rectangle([PX0, OY - 60, PX0 + 1000, OY + 900], fill=BG, outline=LINE, width=3)
txt(PX0 + 30, OY - 20, "ALANLAR · ERİŞİM · KARARLAR", f16, INK)
rows = [("hat (A+B/C+D+E) 350 × 83", "2,9 m²"), ("karton kulesi 40 × 80", "0,3 m²"), ("robot koridoru 390 × 120 + kıvrım 86 × 38", "5,0 m²"),
        ("ince duvar 304 × 6", "0,2 m²"), ("ön zon: geçit + tezgâh + servis", "2,6 m²"), ("QR dolabı 86 × 52", "0,4 m²"), ("İÇ ALAN", "11,4 m²  (v7: 11,1)")]
yy = OY + 30
for a_, b_ in rows:
    txt(PX0 + 30, yy, a_, f9 if a_ != "İÇ ALAN" else f11, INK); txt(PX0 + 960, yy, b_, f9 if a_ != "İÇ ALAN" else f11, INK, "ra")
    yy += 34
d.line([(PX0 + 30, yy - 8), (PX0 + 970, yy - 8)], fill=SOFT, width=2)
yy += 10
NOT = [
    "ROBOTLAR — iki kol da FR20 (1.854 mm, pratik 167 cm). Sebep:",
    " · R1: açık çekmece (70) kaideye çarpmasın → kaide z 88, koridor 120; en uzak",
    "   çekmece köşesi 140, pres plakası 158 → FR10 (125) yetmez.",
    " · R2: QR dolabı cephede, arkası koridor kıvrımında (y 241); (300, 150)'den",
    "   dolap köşesi 128 + göz kotu → 143; fırın üst gözü 162 → FR20 sınırda ✓.",
    "   FR10 ile QR dolabına ancak koridor ucunda dik dururken yetişiyordu",
    "   (SERVİS v4) — o zaman müşteri yüzü yan duvarda kalır, cephede olmaz.",
    "ÇEKMECE: 70 açılır, ön yüzü z 74; kaide z 78–98 → 4 cm boşluk; yazılım kilidi.",
    "KARTON KULESİ hücre içinde hat ucunda: E şarjörü koridordan dolduruluyor.",
    "ÖN ZON 84 (v7 gibi): geçit 54 dar — rahat çalışma için 100 → derinlik 309.",
    "KAPI dışa açılır: sol duvardaki el lavabosuna yer kalsın diye.",
    "MİNİ TEZGÂH 80 × 40: evye 40 × 40 + doldurma 40 × 40; üstünde dolap 80 × 35.",
    "KORİDOR 90 kalırsa (çekmece için başka çözüm): derinlik 263, iç 10,3 m².",
]
for l in NOT:
    txt(PX0 + 30, yy, l, f9 if not l.startswith(" ") else f8, INK if not l.startswith(" ") else GRAY)
    yy += 30

d.line([(OX, H_PX - 80), (W_PX - 140, H_PX - 80)], fill=LINE, width=2)
txt(W_PX - 140, H_PX - 45, "AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v8 · 17 Eyl 2026 · üretici _uretec/dukkan_plani8.py", f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "ic %s x %s" % (sayi(IC_W), sayi(IC_D)))
