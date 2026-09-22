# -*- coding: utf-8 -*-
"""AUTOKITCH - SERVIS + TESLIM PAFTASI v1 (17 Eyl 2026). Hattin (HAT_2KOL_v8) disinda kalan her sey:
QR teslim dolabi (koridor ucunda, R2 erisiminde, altinda 2 gunluk icecek), servis duvari (bulasik makinesi, evye + el yikama lavabosu,
servis dolabi: 4 gunluk karton + icecek + temizlik + UPS + NVR), yangin ve kamera. Olculer mm. Kural: paftada yalniz gorunus + olcu + parca.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\SERVIS_TESLIM_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5200, 3700
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ, SICAK, SU = (253, 244, 243), (255, 226, 214), (214, 236, 250)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(54, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def satirlar(x, y, s, f, c, adim=20):
    ls = s.split("|")
    y0 = y - adim * (len(ls) - 1) / 2.0
    for i, l in enumerate(ls):
        txt(x, y0 + i * adim, l, f if i == 0 else f7, c if i == 0 else GRAY, "mm")


def sayi(v):
    return ("%g" % v).replace(".", ",")


def olcu_h(x0, x1, y, s, f=f11, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f11, c=INK, yon="r"):
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


def kesik(X, a, b, y0, y1, et="", c=INK, alt=""):
    drect(X(a), Y(y1), X(b), Y(y0), c, 1)
    if et:
        txt(X((a + b) / 2), Y((y0 + y1) / 2) - (8 if alt else 0), et, f7, c, "mm")
    if alt:
        txt(X((a + b) / 2), Y((y0 + y1) / 2) + 10, alt, f7, GRAY, "mm")


# ======================= VERI =======================
# QR TESLIM DOLABI: koridor ucunda, hatta dik (yuzu -x, robot tarafi); arkasi sokak. 860 genis x 830 derin x 1970.
Q_W, Q_D, Q_H = 860.0, 830.0, 1970.0
Q_TABAN = 240.0                                   # sogutma grubu 1/5 HP (icecek cekmeceleri)
Q_CEK = (297.5, 165.0, 2)                         # 2 icecek cekmecesi 620 x 680: y0, adim, adet -> 90 + 90 = 180 kutu = 2,6 gun
Q_GOZ = (640.0, 200.0, 6)                         # 12 goz: 2 kolon x 6 sira, 190 yuksek, 380 genis, 750 derin, isitmali 60 C
Q_PANO = (1840.0, 1968.5)
# SERVIS DUVARI (koridor disinda, eleman tarafi): soldan saga
SV = [("BULAŞIK MAKİNESİ", 600.0), ("TEZGÂH · EVYE + EL LAVABOSU", 1400.0), ("SERVİS DOLABI", 1200.0)]
SV_W = sum(w for _, w in SV)                      # 3200
# Hat ucu (HAT_2KOL_v8): E kutu 2800-3500, koridor 800, R2 x 2800 z +380
HAT, X_E, R2X, RZ, KOR = 3500.0, 2800.0, 2800.0, 380.0, 800.0
ERISIM_P = 1250.0
QX = HAT + 50.0                                   # dolabin robot yuzu x = 3550

OX = 260.0
FY_TOP = 420.0
FY = FY_TOP + Q_H * S
PY_TOP = FY + 300.0


def Y(y):
    return FY - y * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  SERVİS + TESLİM PAFTASI  v1  ·  QR DOLABI (KORİDOR UCU)  ·  SERVİS DUVARI  ·  YANGIN · KAMERA · UPS", f38, INK)
txt(OX, 138, "hattın (HAT 2 KOL v8) dışında kalan her şey  ·  6 günlük ikmal döngüsü: karton + içecek + temizlik  ·  2 günlük yıkama  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= 1 · QR DOLABI ON GORUNUS (robot tarafi) =======================
QX0 = OX


def QXp(x):
    return QX0 + x * S


txt(QX0, FY_TOP - 190, "1 · QR TESLİM DOLABI · ön görünüş (robot tarafı)", f16, ACC)
txt(QX0, FY_TOP - 152, "koridor ucunda hatta dik durur; arkası sokak cephesi · kendi soğutucusu altta · gözler ısıtmalı · kendi panosu üstte", f9, GRAY)
d.rectangle([QXp(0), Y(Q_H), QXp(Q_W), Y(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([QXp(33), Y(Q_TABAN), QXp(Q_W - 33), Y(20)], fill=SOFT, outline=LINE, width=2)
kesik(QXp, 70.0, 370.0, 30.0, 230.0, "SOĞUTMA GRUBU ⅕ HP", INK, "300 × 250 × 220")
kesik(QXp, 390.0, 640.0, 30.0, 230.0, "Q KARTI · 24 V", INK)
kesik(QXp, 660.0, 800.0, 30.0, 230.0, "hava", GRAY)
d.rectangle([QXp(33), Y(Q_GOZ[0] - 10.0), QXp(Q_W - 33), Y(Q_TABAN + 1.5)], fill=BG, outline=LINE, width=2)
y = Q_CEK[0]
for i in range(Q_CEK[2]):
    d.rectangle([QXp(120 + 8), Y(y + 162.0), QXp(120 + 620 - 8), Y(y)], fill=BG, outline=DOLAP, width=1)
    d.rectangle([QXp(120 + 18), Y(y + 60.0), QXp(120 + 58), Y(y + 30.0)], fill=(255, 230, 230), outline=RED, width=1)
    txt(QXp(430), Y(y + 81.0), "İÇECEK 330 ml × 90 · 9 × 10 · +3 °C" if i == 0 else "İÇECEK 330 ml × 90 · tatlı 14 köşede", f7, DOLAP, "mm")
    y += Q_CEK[1]
txt(QXp(Q_W / 2), Y(Q_GOZ[0] - 22.0), "2 çekmece = 180 kutu = 2,6 gün · robot alır, göze koyar", f7, GRAY, "mm")
for r in range(Q_GOZ[2]):
    y0 = Q_GOZ[0] + r * Q_GOZ[1]
    for c in range(2):
        d.rectangle([QXp(30 + c * 410), Y(y0 + 190.0), QXp(420 + c * 410), Y(y0)], fill=BG, outline=INK, width=2)
        d.line([(QXp(60 + c * 410), Y(y0 + 30.0)), (QXp(390 + c * 410), Y(y0 + 30.0))], fill=RED, width=2)
        if r == 5:
            txt(QXp(225 + c * 410), Y(y0 + 110.0), "QR GÖZÜ 380 × 190 × 750", f7, INK, "mm")
            txt(QXp(225 + c * 410), Y(y0 + 80.0), "taban ısıtıcı 60 °C · çift kapak", f7, GRAY, "mm")
d.rectangle([QXp(33), Y(Q_PANO[1]), QXp(Q_W - 33), Y(Q_PANO[0])], fill=BG, outline=LINE, width=2)
txt(QXp(Q_W / 2), Y((Q_PANO[0] + Q_PANO[1]) / 2), "PANO · kilit + ısıtıcı kartı · ekran/QR okuyucu sürücüsü (sokak tarafı)", f7, INK, "mm")
olcu_h(QXp(0), QXp(Q_W), Y(Q_H) - 26, sayi(Q_W), f11, INK)
olcu_v(QXp(0) - 44, Y(Q_H), Y(0), sayi(Q_H), f11, INK, "l")
for yy in (Q_TABAN, Q_CEK[0] + 2 * Q_CEK[1] - 3.0, Q_GOZ[0], Q_GOZ[0] + 6 * Q_GOZ[1] - 10.0, Q_PANO[0]):
    d.line([(QXp(Q_W) + 6, Y(yy)), (QXp(Q_W) + 24, Y(yy))], fill=INK, width=2)
    txt(QXp(Q_W) + 30, Y(yy), sayi(yy), f8, INK, "lm")
txt(QXp(Q_W / 2), Y(0) + 40, "12 göz: pik 35 sipariş/saat × ~10 dk bekleme ≈ 6 dolu göz, ×2 pay → 12", f7, GRAY, "mm")

# ======================= 2 · QR DOLABI YAN KESIT =======================
KX0 = QXp(Q_W) + 260.0


def KXp(z):
    return KX0 + z * S


txt(KX0, FY_TOP - 190, "2 · QR DOLABI · yan kesit", f16, ACC)
txt(KX0, FY_TOP - 152, "sol: robot tarafı (koridor) · sağ: sokak", f9, GRAY)
d.rectangle([KXp(0), Y(Q_H), KXp(Q_D), Y(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([KXp(0), Y(Q_TABAN), KXp(Q_D), Y(0)], fill=SOFT, outline=LINE, width=2)
drect(KXp(300), Y(230), KXp(600), Y(30), INK, 1)
txt(KXp(450), Y(130) - 8, "SOĞUTMA GRUBU", f7, INK, "mm"); txt(KXp(450), Y(130) + 8, "hava: robot tarafı ızgara", f7, GRAY, "mm")
d.rectangle([KXp(61.5), Y(Q_GOZ[0] - 10.0), KXp(Q_D - 61.5), Y(Q_TABAN + 61.5)], fill=BG, outline=LINE, width=1)
d.rectangle([KXp(1.5), Y(Q_GOZ[0] - 10.0), KXp(61.5), Y(Q_TABAN + 1.5)], fill=PUC, outline=GRAY, width=1)
d.rectangle([KXp(Q_D - 61.5), Y(Q_GOZ[0] - 10.0), KXp(Q_D - 1.5), Y(Q_TABAN + 1.5)], fill=PUC, outline=GRAY, width=1)
y = Q_CEK[0]
for i in range(Q_CEK[2]):
    d.rectangle([KXp(40), Y(y + 162.0), KXp(720), Y(y)], fill=BG, outline=DOLAP, width=1)
    d.rectangle([KXp(0), Y(y + 162.0), KXp(40), Y(y)], fill=BG, outline=DOLAP, width=1)
    y += Q_CEK[1]
txt(KXp(380), Y(Q_CEK[0] + 165.0), "içecek çekmecesi 680 · robota açılır", f7, DOLAP, "mm")
for r in range(Q_GOZ[2]):
    y0 = Q_GOZ[0] + r * Q_GOZ[1]
    d.rectangle([KXp(40), Y(y0 + 190.0), KXp(790), Y(y0)], fill=BG, outline=INK, width=2)
    d.rectangle([KXp(0), Y(y0 + 190.0), KXp(40), Y(y0)], fill=AGZ, outline=RED, width=1)
    d.rectangle([KXp(790), Y(y0 + 190.0), KXp(830), Y(y0)], fill=AGZ, outline=RED, width=1)
    d.line([(KXp(90), Y(y0 + 30.0)), (KXp(740), Y(y0 + 30.0))], fill=RED, width=2)
txt(KXp(415), Y(1240.0) - 10, "GÖZ 750 · kutu 320 × 320 × 45 · 4 kutu üst üste sığar", f7, INK, "mm")
txt(KXp(415), Y(1240.0) + 12, "robot kapağı motorlu · müşteri kapağı QR kilitli", f7, GRAY, "mm")
txt(KXp(0) - 14, Y(1240.0), "ROBOT", f8, RED, "rm"); txt(KXp(Q_D) + 14, Y(1240.0), "MÜŞTERİ", f8, RED, "lm")
d.rectangle([KXp(61.5), Y(Q_PANO[1]), KXp(Q_D - 61.5), Y(Q_PANO[0])], fill=BG, outline=LINE, width=1)
drect(KXp(700), Y(1800.0), KXp(820), Y(1200.0), ACC, 1)
txt(KXp(760), Y(1500.0) - 8, "EKRAN", f7, ACC, "mm"); txt(KXp(760), Y(1500.0) + 8, "QR okuyucu", f7, GRAY, "mm")
olcu_h(KXp(0), KXp(Q_D), Y(0) + 44, sayi(Q_D), f11, INK)

# ======================= 3 · PLAN: HAT UCU + KORIDOR + QR DOLABI =======================
PX0 = OX
PZ0 = PY_TOP


def PXp(x):
    return PX0 + (x - 2000.0) * S


def PZp(z):
    return PZ0 + (z + 790.0) * S


txt(PX0, PY_TOP - 150, "3 · PLAN · hat ucu + robot koridoru + QR dolabı (R2 erişimi)", f16, ACC)
d.rectangle([PXp(2000.0), PZp(-790.0), PXp(2800.0), PZp(40.0)], fill=FILL, outline=LINE, width=3)
txt(PXp(2400.0), PZp(-375.0), "D · FIRIN", f9, INK, "mm")
d.rectangle([PXp(2800.0), PZp(-790.0), PXp(3500.0), PZp(40.0)], fill=FILL, outline=LINE, width=3)
txt(PXp(3150.0), PZp(-375.0), "E · KUTU", f9, INK, "mm")
txt(PXp(3150.0), PZp(-330.0), "hat ucu x 3500", f7, GRAY, "mm")
d.line([(PXp(1900.0), PZp(40.0 + KOR)), (PXp(3500.0), PZp(40.0 + KOR))], fill=GRAY, width=1)
txt(PXp(2700.0), PZp(40.0 + KOR) + 22, "robot koridoru 800", f8, GRAY, "mm")
# QR dolabi: dik, x 3550-4380, z -30..830
d.rectangle([PXp(QX), PZp(-30.0), PXp(QX + Q_D), PZp(Q_W - 30.0)], fill=FILL, outline=LINE, width=3)
for c in range(2):
    d.rectangle([PXp(QX + 40), PZp(0.0 + c * 410), PXp(QX + 790), PZp(390.0 + c * 410)], fill=BG, outline=INK, width=2)
    txt(PXp(QX + 415), PZp(195.0 + c * 410) - 8, "QR GÖZÜ × 6", f7, INK, "mm")
    txt(PXp(QX + 415), PZp(195.0 + c * 410) + 8, "750 × 380", f7, GRAY, "mm")
txt(PXp(QX + 415), PZp(-45.0), "altta: 2 içecek çekmecesi (robota açılır)", f7, DOLAP, "mm")
txt(PXp(QX + Q_D) + 14, PZp(400.0), "SOKAK", f9, RED, "lm")
txt(PXp(QX + Q_D) + 14, PZp(430.0), "müşteri kapakları · ekran", f7, GRAY, "lm")
txt(PXp(QX) - 14, PZp(400.0), "robot kapakları", f7, RED, "rm")
# R2
cxp, cyp = PXp(R2X), PZp(RZ)
d.rectangle([PXp(R2X - 200), PZp(RZ - 200), PXp(R2X + 200), PZp(RZ + 200)], fill=SOFT, outline=ACC, width=1)
d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
darc(cxp, cyp, ERISIM_P * S, 270.0, 450.0, ACC, 2, 3.0)
txt(cxp, PZp(RZ + 200) + 22, "R2 · FR10 · pratik erişim 1250", f9, ACC, "mm")
txt(PXp(QX + 415), PZp(Q_W + 60.0), "en uzak göz: dx 750 · dz 420 · dy 800 → 1175 ✓", f7, ACC, "mm")
olcu_h(PXp(2800.0), PXp(3500.0), PZp(40.0) + 60, "700", f8, INK)
olcu_h(PXp(QX), PXp(QX + Q_D), PZp(40.0) + 60, sayi(Q_D), f8, INK)
olcu_h(PXp(3500.0), PXp(QX), PZp(40.0) + 60, "50", f7, INK)
olcu_v(PXp(QX + Q_D) + 120, PZp(-30.0), PZp(Q_W - 30.0), sayi(Q_W), f8, INK, "r")
txt(PXp(2000.0), PZp(-790.0) - 30, "ARKA", f9, GRAY, "la")

# ======================= 4 · SERVIS DUVARI ON GORUNUS =======================
SX0 = KX0 + Q_D * S + 420.0


def SXp(x):
    return SX0 + x * S


H_S = 2000.0
txt(SX0, FY_TOP - 190, "4 · SERVİS DUVARI · ön görünüş", f16, ACC)
txt(SX0, FY_TOP - 152, "koridor dışında, eleman tarafı · 2 günlük yıkama + 6 günlük stok · yangın ve kamera duvarda", f9, GRAY)
x = 0.0
for ad, w in SV:
    d.rectangle([SXp(x), Y(H_S if "DOLABI" in ad else 850.0), SXp(x + w), Y(0)], fill=FILL, outline=LINE, width=3)
    txt(SXp(x + w / 2), Y(H_S) - 64, ad, f13, INK, "md")
    olcu_h(SXp(x), SXp(x + w), Y(H_S) - 26, sayi(w), f11, INK)
    x += w
# bulasik makinesi
d.rectangle([SXp(30), Y(820.0), SXp(570), Y(120.0)], fill=BG, outline=LINE, width=2)
kesik(SXp, 60.0, 540.0, 260.0, 760.0, "TEZGÂH ALTI BULAŞIK MAKİNESİ", INK, "600 × 600 × 820 · sepet 500 × 500")
txt(SXp(300), Y(190.0), "2 günde: 6 kaset + kaşar kabı + 6 tepsi + uçlar ≈ 3 sepet", f7, GRAY, "mm")
d.rectangle([SXp(0), Y(120.0), SXp(SV_W), Y(0)], fill=SOFT, outline=LINE, width=2)
# tezgah + evye + el lavabosu
d.rectangle([SXp(600), Y(880.0), SXp(2000), Y(850.0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([SXp(640), Y(850.0), SXp(1240), Y(450.0)], fill=SU, outline=BUZ, width=2)
txt(SXp(940), Y(650.0) - 8, "EVYE · ekipman / gıda", f8, BUZ, "mm"); txt(SXp(940), Y(650.0) + 12, "600 × 500 × 300 · sıcak-soğuk su", f7, GRAY, "mm")
d.rectangle([SXp(1400), Y(850.0), SXp(1900), Y(560.0)], fill=SU, outline=BUZ, width=2)
txt(SXp(1650), Y(705.0) - 8, "EL YIKAMA LAVABOSU", f8, BUZ, "mm"); txt(SXp(1650), Y(705.0) + 12, "500 × 400 · ayrı · sabun + kâğıt havlu · zorunlu", f7, GRAY, "mm")
kesik(SXp, 640.0, 1240.0, 140.0, 430.0, "altı: temizlik kimyasalı dolabı", GRAY)
kesik(SXp, 1300.0, 1960.0, 140.0, 540.0, "altı: çöp 60 L × 2 (ayrışım)", GRAY)
d.rectangle([SXp(1500), Y(1300.0), SXp(1800), Y(900.0)], fill=BG, outline=GRAY, width=1)
txt(SXp(1650), Y(1100.0) - 8, "DUVAR: sabunluk · havluluk", f7, GRAY, "mm"); txt(SXp(1650), Y(1100.0) + 8, "hijyen listesi", f7, GRAY, "mm")
# servis dolabi
d.rectangle([SXp(2030), Y(H_S - 30.0), SXp(3170), Y(120.0)], fill=BG, outline=LINE, width=2)
d.line([(SXp(2600), Y(H_S - 30.0)), (SXp(2600), Y(120.0))], fill=LINE, width=2)
for yy in (500.0, 1000.0, 1500.0):
    d.line([(SXp(2030), Y(yy)), (SXp(3170), Y(yy))], fill=LINE, width=1)
kesik(SXp, 2060.0, 2570.0, 1520.0, 1940.0, "TEMİZLİK · SARF", INK, "eldiven · poşet · sachet · kâğıt")
kesik(SXp, 2630.0, 3140.0, 1520.0, 1940.0, "YEDEK ÜRÜN", INK, "tepsi × 6 · pençe · filtre · bıçak")
kesik(SXp, 2060.0, 2570.0, 520.0, 1480.0, "KARTON KUTU BLANK", INK, "400 × 760 yığın 900 = 500 kutu")
kesik(SXp, 2630.0, 3140.0, 520.0, 1480.0, "KARTON KUTU BLANK", INK, "400 × 760 yığın 900 = 500 kutu")
txt(SXp(2600), Y(500.0) + 14, "dolap 1.000 + makine şarjörü 710 = 1.710 kutu ≥ 6 gün (1.680)", f7, GRAY, "mm")
kesik(SXp, 2060.0, 2570.0, 140.0, 480.0, "İÇECEK 4 GÜN", INK, "240 kutu = 10 shrink 24'lü · oda sıcaklığı")
kesik(SXp, 2630.0, 2880.0, 140.0, 480.0, "UPS 3 kVA", INK, "440 × 600 × 250")
kesik(SXp, 2900.0, 3140.0, 140.0, 480.0, "NVR + modem", INK, "kamera kayıt 30 gün")
# duvar: yangin + kamera + dedektor
d.rectangle([SXp(3260), Y(1500.0), SXp(3380), Y(1100.0)], fill=RED, outline=INK, width=1)
txt(SXp(3320), Y(1560.0), "6 kg ABC", f7, RED, "mm")
d.rectangle([SXp(3420), Y(1500.0), SXp(3540), Y(1100.0)], fill=(140, 140, 150), outline=INK, width=1)
txt(SXp(3480), Y(1560.0), "5 kg CO₂", f7, INK, "mm")
txt(SXp(3400), Y(1050.0), "askı kotu 900 (tüp altı)", f7, GRAY, "mm")
d.ellipse([SXp(3300) - 14, Y(1900.0) - 14, SXp(3300) + 14, Y(1900.0) + 14], fill=BG, outline=INK, width=2)
txt(SXp(3300), Y(1960.0), "duman dedektörü", f7, INK, "mm")
d.rectangle([SXp(3460), Y(1920.0), SXp(3540), Y(1880.0)], fill=INK)
txt(SXp(3500), Y(1960.0), "kamera 1/4", f7, INK, "mm")
olcu_h(SXp(0), SXp(SV_W), Y(0) + 44, "SERVİS DUVARI  %s" % sayi(SV_W), f13, INK)
olcu_v(SXp(0) - 44, Y(H_S), Y(0), sayi(H_S), f11, INK, "l")
for yy in (120.0, 850.0, 1000.0, 1500.0, H_S):
    d.line([(SXp(SV_W) + 6, Y(yy)), (SXp(SV_W) + 24, Y(yy))], fill=INK, width=2)
    txt(SXp(SV_W) + 30, Y(yy), sayi(yy), f8, INK, "lm")

# ======================= 5 · SERVIS DUVARI PLAN =======================
txt(SX0, PY_TOP - 150, "5 · SERVİS DUVARI · plan", f16, ACC)
SPZ = PY_TOP + 40


def SPp(z):
    return SPZ + z * S


x = 0.0
for ad, w in SV:
    dz = 600.0
    d.rectangle([SXp(x), SPp(0), SXp(x + w), SPp(dz)], fill=FILL, outline=LINE, width=3)
    x += w
d.rectangle([SXp(640), SPp(60), SXp(1240), SPp(560)], fill=SU, outline=BUZ, width=2)
txt(SXp(940), SPp(310), "EVYE 600 × 500", f7, BUZ, "mm")
d.rectangle([SXp(1400), SPp(100), SXp(1900), SPp(500)], fill=SU, outline=BUZ, width=2)
txt(SXp(1650), SPp(310), "EL LAVABOSU 500 × 400", f7, BUZ, "mm")
txt(SXp(300), SPp(310), "BULAŞIK 600 × 600", f7, INK, "mm")
drect(SXp(2060), SPp(20), SXp(2570), SPp(580), GRAY, 1)
drect(SXp(2630), SPp(20), SXp(3140), SPp(580), GRAY, 1)
txt(SXp(2600), SPp(310), "SERVİS DOLABI 1200 × 600 × 2000 · blank 760 derinliğe sığar", f7, INK, "mm")
d.line([(SXp(-60), SPp(0)), (SXp(SV_W + 60), SPp(0))], fill=INK, width=4)
txt(SXp(SV_W / 2), SPp(0) - 22, "DUVAR", f9, GRAY, "mm")
d.line([(SXp(-60), SPp(600 + 900)), (SXp(SV_W + 60), SPp(600 + 900))], fill=GRAY, width=1)
txt(SXp(SV_W / 2), SPp(600 + 900) + 22, "eleman geçişi 900 · koridor kapısı bu tarafta", f8, GRAY, "mm")
olcu_v(SXp(SV_W) + 60, SPp(0), SPp(600), "600", f8, INK, "r")
olcu_v(SXp(SV_W) + 60, SPp(600), SPp(1500), "900", f8, INK, "r")
for i, (xx, ad) in enumerate(((300.0, "K1 koridor"), (1650.0, "K2 servis"), (2900.0, "K3 teslim cephesi"))):
    d.rectangle([SXp(xx) - 8, SPp(0) - 8, SXp(xx) + 8, SPp(0) + 8], fill=INK)
    txt(SXp(xx), SPp(0) - 40, ad, f7, INK, "mm")
txt(SXp(SV_W / 2), SPp(0) - 60, "KAMERA 4: koridor · servis · teslim cephesi · giriş → NVR", f7, GRAY, "mm")

# ======================= PARCA LISTESI =======================
TX, TY = PX0, PY_TOP + 1130
txt(TX, TY - 60, "PARÇA LİSTESİ · servis + teslim", f16, ACC)
PARCA = [
    ("QR DOLABI", "ısıtmalı QR teslim dolabı 860 × 830 × 1970 · 12 göz 380 × 190 × 750 · çift kapak", "1", "koridor ucu, hatta dik · sokak cephesi · Çin 3.300 $ / Hatco ref."),
    ("QR DOLABI", "içecek çekmecesi 620 × 680 · contalı · lineer motor · 90 kutu", "2", "2,6 gün · soğutma grubu ⅕ HP altta"),
    ("SERVİS", "tezgâh altı bulaşık makinesi 600 × 600 × 820 · sepet 500 × 500", "1", "2 günde ~3 sepet · Öztiryakiler / Empero sınıfı"),
    ("SERVİS", "tezgâh 1400 × 600 × 850 · evye 600 × 500 + el yıkama lavabosu 500 × 400", "1", "el lavabosu ayrı ve zorunlu (hijyen yönetmeliği)"),
    ("SERVİS", "servis dolabı 1200 × 600 × 2000 · 4 raf · kilitli", "1", "karton 1.000 · içecek 240 · temizlik · yedek"),
    ("SERVİS", "UPS 3 kVA online · 440 × 600 × 250", "1", "robot + PLC + soğutma kontrolü 15 dk"),
    ("GÜVENLİK", "kamera 4 (koridor, servis, teslim cephesi, giriş) + NVR 1 TB", "1", "30 gün kayıt · mobilden izleme"),
    ("YANGIN", "6 kg ABC + 5 kg CO₂ taşınabilir söndürücü · askı 900", "2", "Binaların Yangından Korunması Yön."),
    ("YANGIN", "otomatik aerosol söndürücü (fırın kolonu D + pano) · duman/ısı dedektörü · alarm merkeze", "1 set", "D modülü içinde · elektrik kesme rölesi"),
    ("SARF", "6 günlük ikmal: karton 1.680 · içecek 420 · kaşar 26,4 kg · sucuk 8,4 kg · tatlı 39", "—", "kaşar + sucuk B'de kapaklı bölmede (HAT v8)"),
]
kol = (0, 130, 900, 990)
th = 30
d.rectangle([TX, TY, TX + 1540, TY + th * (len(PARCA) + 1)], fill=BG, outline=LINE, width=2)
d.rectangle([TX, TY, TX + 1540, TY + th], fill=SOFT, outline=LINE, width=1)
for cx_, h_ in zip(kol, ("GRUP", "PARÇA", "ADET", "NOT")):
    txt(TX + cx_ + 10, TY + th / 2, h_, f8, INK, "lm")
for i, (a_, b_, c_, e_) in enumerate(PARCA):
    yy = TY + th * (i + 1)
    d.line([(TX, yy), (TX + 1540, yy)], fill=SOFT, width=1)
    for cx_, s_ in zip(kol, (a_, b_, c_, e_)):
        txt(TX + cx_ + 10, yy + th / 2, s_, f8 if cx_ != 990 else f7, INK if cx_ != 990 else GRAY, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "kapak (robot / müşteri)", False), (DOLAP, BG, "çekmece +3 °C", False),
       (BUZ, SU, "su", False), (INK, BG, "kapak arkası parça", True), (ACC, BG, "robot · erişim", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "QR dolabı 860 × 830 × 1970 (12 göz + 180 içecek)  ·  servis duvarı 3200 × 600  ·  bulaşık 2 gün  ·  karton + içecek + temizlik 6 gün  ·  UPS 3 kVA  ·  4 kamera  ·  2 söndürücü + aerosol", f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT)
