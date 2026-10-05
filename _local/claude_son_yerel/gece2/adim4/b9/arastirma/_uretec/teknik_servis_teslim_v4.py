# -*- coding: utf-8 -*-
"""AUTOKITCH - SERVIS + TESLIM PAFTASI v4 (17 Eyl 2026). v3 Kemal: tezgah cok buyuk, bildigin kadar kucult; UPS ne ise yarar -> 3 kVA kalkti, 500 VA mini (PLC + modem + QR kilit). v2 Kemal: servis duvari mutfak gibi (alt dolap + tezgah + ust dolap, solda uzun dolap yok); stok 4 gun (hat 2 gun tasir). v1 Kemal: QR dolabinda icecek/sogutucu YOK, dolap kisa ve en kucuk;
PIN ya da QR ile acma; bulasik makinesi gerekli mi (kaldirildi, evyede elde yikama); servis dolabi tek kapakli kucuk;
en kucuk evye + el lavabosu; kaset doldurma tezgahi. Her sey en kucuk / en optimum. Olculer mm.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\SERVIS_TESLIM_v4_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5300, 3850
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200)
AGZ, SU = (253, 244, 243), (214, 236, 250)


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
# QR TESLIM DOLABI (sogutucu yok, icecek yok): 860 x 520 x 1650 · koridor ucunda hatta dik; robot yuzu -x, musteri yuzu sokak
Q_W, Q_D, Q_H = 860.0, 520.0, 1650.0
Q_ALT = (100.0, 340.0)                            # elektronik: kilit surucusu, 12 robot kapak motoru, guc, modem
Q_GOZ = (350.0, 200.0, 6)                         # 12 goz 2 x 6 · 190 yuksek · 380 genis · 440 derin (kutu 320 + kapaklar)
Q_UST = (1560.0, 1648.5)
# SERVIS DUVARI: servis dolabi 600 + tezgah 1000 = 1600
SV_W = 1200.0                                     # karton kulesi 400 + mini tezgah 800
HAT, R2X, RZ, KOR, ERISIM_P = 3500.0, 2800.0, 380.0, 800.0, 1250.0
QX = HAT + 50.0

OX = 260.0
FY_TOP = 420.0
FY = FY_TOP + 2000.0 * S
PY_TOP = FY + 320.0


def Y(y):
    return FY - y * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  SERVİS + TESLİM PAFTASI  v4  ·  QR DOLABI 860 × 520 × 1650  ·  KARTON KULESİ 400 + MİNİ TEZGÂH 800  ·  4 GÜNLÜK STOK", f38, INK)
txt(OX, 138, "QR / PIN ile açma  ·  bulaşık makinesi yok, evyede elde yıkama  ·  karton kulesi 400 × 800 × 2000 (1.120 blank tek yığın) + mini tezgâh 800 × 600 (evye + doldurma) + üst dolap 800 × 350  ·  UPS 3 kVA yok  ·  hat 2 gün taşır, burada 4 gün  ·  yangın · kamera · UPS  ·  ölçüler mm  ·  17 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= 1 · QR DOLABI · robot tarafi =======================
def Xq(x):
    return OX + x * S


txt(OX, FY_TOP - 190, "1 · QR DOLABI · robot tarafı", f16, ACC)
txt(OX, FY_TOP - 152, "koridor ucunda hatta dik · 12 göz · kapaklar motorlu", f9, GRAY)
d.rectangle([Xq(0), Y(Q_H), Xq(Q_W), Y(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([Xq(0), Y(100.0), Xq(Q_W), Y(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([Xq(33), Y(Q_ALT[1]), Xq(Q_W - 33), Y(Q_ALT[0] + 3.0)], fill=BG, outline=LINE, width=2)
kesik(Xq, 60.0, 330.0, 120.0, 320.0, "KİLİT + KAPAK KARTI", INK, "24 göz sürücüsü")
kesik(Xq, 350.0, 560.0, 120.0, 320.0, "GÜÇ 24 V", INK, "150 W")
kesik(Xq, 580.0, 800.0, 120.0, 320.0, "MODEM · PLC", INK, "sipariş kodu")
for r in range(Q_GOZ[2]):
    y0 = Q_GOZ[0] + r * Q_GOZ[1]
    for c in range(2):
        d.rectangle([Xq(30 + c * 410), Y(y0 + 190.0), Xq(420 + c * 410), Y(y0)], fill=AGZ if r == 0 else BG, outline=INK, width=2)
        d.rectangle([Xq(60 + c * 410), Y(y0 + 175.0), Xq(390 + c * 410), Y(y0 + 15.0)], fill=BG, outline=RED, width=1)
        if r == 5:
            txt(Xq(225 + c * 410), Y(y0 + 110.0), "GÖZ 380 × 190 × 440", f7, INK, "mm")
            txt(Xq(225 + c * 410), Y(y0 + 80.0), "robot kapağı motorlu", f7, GRAY, "mm")
d.rectangle([Xq(33), Y(Q_UST[1]), Xq(Q_W - 33), Y(Q_UST[0])], fill=BG, outline=LINE, width=2)
txt(Xq(Q_W / 2), Y((Q_UST[0] + Q_UST[1]) / 2), "ısıtıcı kartı · kablo kanalı", f7, INK, "mm")
olcu_h(Xq(0), Xq(Q_W), Y(Q_H) - 26, sayi(Q_W), f11, INK)
olcu_v(Xq(0) - 44, Y(Q_H), Y(0), sayi(Q_H), f11, INK, "l")
for yy in (100.0, Q_ALT[1], Q_GOZ[0], Q_GOZ[0] + 6 * Q_GOZ[1] - 10.0, Q_UST[0]):
    d.line([(Xq(Q_W) + 6, Y(yy)), (Xq(Q_W) + 24, Y(yy))], fill=INK, width=2)
    txt(Xq(Q_W) + 30, Y(yy), sayi(yy), f8, INK, "lm")
txt(Xq(Q_W / 2), Y(0) + 40, "12 göz: pik 35 sipariş/sa × ~10 dk ≈ 6 dolu, ×2 pay", f7, GRAY, "mm")


# ======================= 2 · QR DOLABI · musteri tarafi (sokak) =======================
MX0 = Xq(Q_W) + 220.0


def Xm(x):
    return MX0 + x * S


txt(MX0, FY_TOP - 190, "2 · QR DOLABI · müşteri tarafı (sokak)", f16, ACC)
txt(MX0, FY_TOP - 152, "QR okut ya da sipariş PIN'ini gir → göz kapağı açılır", f9, GRAY)
d.rectangle([Xm(0), Y(Q_H), Xm(Q_W), Y(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([Xm(0), Y(100.0), Xm(Q_W), Y(0)], fill=SOFT, outline=LINE, width=2)
for r in range(Q_GOZ[2]):
    y0 = Q_GOZ[0] + r * Q_GOZ[1]
    for c in range(2):
        d.rectangle([Xm(30 + c * 410), Y(y0 + 190.0), Xm(420 + c * 410), Y(y0)], fill=BG, outline=INK, width=2)
        d.rectangle([Xm(380 + c * 410), Y(y0 + 105.0), Xm(400 + c * 410), Y(y0 + 85.0)], fill=INK)
        txt(Xm(225 + c * 410), Y(y0 + 95.0), "%02d" % (r * 2 + c + 1), f9, GRAY, "mm")
        if r == 5:
            txt(Xm(225 + c * 410), Y(y0 + 150.0), "elektrikli mandal · it-aç", f7, GRAY, "mm")
d.rectangle([Xm(33), Y(Q_UST[1]), Xm(Q_W - 33), Y(Q_UST[0])], fill=BG, outline=LINE, width=2)
d.rectangle([Xm(300), Y(Q_UST[1] - 10.0), Xm(560), Y(Q_UST[0] + 10.0)], fill=INK)
txt(Xm(430), Y((Q_UST[0] + Q_UST[1]) / 2), "AUTOKITCH", f8, BG, "mm")
# okuyucu paneli: gozlerin arasinda degil, sag ust kosede ayri panel
d.rectangle([Xm(Q_W) + 20, Y(1400.0), Xm(Q_W) + 20 + 220 * S, Y(1000.0)], fill=BG, outline=ACC, width=2)
txt(Xm(Q_W) + 20 + 110 * S, Y(1360.0), "PANEL", f7, ACC, "mm")
d.rectangle([Xm(Q_W) + 20 + 40 * S, Y(1330.0), Xm(Q_W) + 20 + 180 * S, Y(1230.0)], fill=SOFT, outline=INK, width=1)
txt(Xm(Q_W) + 20 + 110 * S, Y(1280.0), "7\" ekran", f7, INK, "mm")
d.rectangle([Xm(Q_W) + 20 + 40 * S, Y(1215.0), Xm(Q_W) + 20 + 180 * S, Y(1150.0)], fill=SOFT, outline=INK, width=1)
txt(Xm(Q_W) + 20 + 110 * S, Y(1182.0), "QR okuyucu", f7, INK, "mm")
d.rectangle([Xm(Q_W) + 20 + 40 * S, Y(1135.0), Xm(Q_W) + 20 + 180 * S, Y(1030.0)], fill=SOFT, outline=INK, width=1)
txt(Xm(Q_W) + 20 + 110 * S, Y(1082.0), "PIN tuş takımı", f7, INK, "mm")
txt(Xm(Q_W) + 20 + 110 * S, Y(980.0), "220 × 400 · yan yüzde", f7, GRAY, "mm")
txt(Xm(Q_W) + 20 + 110 * S, Y(950.0), "kot 1000–1400", f7, GRAY, "mm")
olcu_h(Xm(0), Xm(Q_W), Y(Q_H) - 26, sayi(Q_W), f11, INK)
olcu_v(Xm(0) - 44, Y(Q_GOZ[0]), Y(0), "350", f8, INK, "l")
olcu_v(Xm(0) - 44, Y(Q_GOZ[0] + 6 * Q_GOZ[1] - 10.0), Y(Q_GOZ[0]), "1190", f8, INK, "l")


# ======================= 3 · QR DOLABI · yan kesit =======================
KX0 = Xm(Q_W) + 220 * S + 260.0


def Xk(z):
    return KX0 + z * S


txt(KX0, FY_TOP - 190, "3 · QR DOLABI · yan kesit", f16, ACC)
txt(KX0, FY_TOP - 152, "sol robot · sağ müşteri · 520 derin", f9, GRAY)
d.rectangle([Xk(0), Y(Q_H), Xk(Q_D), Y(0)], fill=FILL, outline=LINE, width=4)
d.rectangle([Xk(0), Y(100.0), Xk(Q_D), Y(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([Xk(30), Y(Q_ALT[1]), Xk(Q_D - 30), Y(Q_ALT[0] + 3.0)], fill=BG, outline=LINE, width=1)
txt(Xk(Q_D / 2), Y(220.0), "elektronik", f7, GRAY, "mm")
for r in range(Q_GOZ[2]):
    y0 = Q_GOZ[0] + r * Q_GOZ[1]
    d.rectangle([Xk(40), Y(y0 + 190.0), Xk(480), Y(y0)], fill=BG, outline=INK, width=2)
    d.rectangle([Xk(0), Y(y0 + 190.0), Xk(40), Y(y0)], fill=AGZ, outline=RED, width=1)
    d.rectangle([Xk(480), Y(y0 + 190.0), Xk(520), Y(y0)], fill=AGZ, outline=RED, width=1)
    d.line([(Xk(70), Y(y0 + 25.0)), (Xk(450), Y(y0 + 25.0))], fill=RED, width=2)
    if r == 2:
        d.rectangle([Xk(100), Y(y0 + 70.0), Xk(420), Y(y0 + 25.0)], fill=SOFT, outline=INK, width=1)
        txt(Xk(260), Y(y0 + 48.0), "kutu 320 × 45", f7, INK, "mm")
txt(Xk(260), Y(Q_GOZ[0] + 6 * Q_GOZ[1] + 40.0), "göz 440 derin · taban ısıtıcı 60 °C", f7, INK, "mm")
txt(Xk(0) - 14, Y(950.0), "ROBOT", f8, RED, "rm"); txt(Xk(Q_D) + 14, Y(950.0), "MÜŞTERİ", f8, RED, "lm")
txt(Xk(0) - 14, Y(920.0), "motorlu kapak", f7, GRAY, "rm"); txt(Xk(Q_D) + 14, Y(920.0), "elektrikli mandal", f7, GRAY, "lm")
olcu_h(Xk(0), Xk(Q_D), Y(0) + 44, sayi(Q_D), f11, INK)


# ======================= 4 · PLAN · hat ucu + koridor + QR dolabi =======================
def Xp(x):
    return OX + (x - 2100.0) * S


def Zp(z):
    return PY_TOP + (z + 790.0) * S


txt(OX, PY_TOP - 150, "4 · PLAN · hat ucu + robot koridoru + QR dolabı", f16, ACC)
d.rectangle([Xp(2100.0), Zp(-790.0), Xp(2800.0), Zp(40.0)], fill=FILL, outline=LINE, width=3)
txt(Xp(2450.0), Zp(-375.0), "D · FIRIN", f9, INK, "mm")
d.rectangle([Xp(2800.0), Zp(-790.0), Xp(3500.0), Zp(40.0)], fill=FILL, outline=LINE, width=3)
txt(Xp(3150.0), Zp(-375.0), "E · KUTU", f9, INK, "mm")
d.line([(Xp(2100.0), Zp(40.0 + KOR)), (Xp(3500.0), Zp(40.0 + KOR))], fill=GRAY, width=1)
txt(Xp(2800.0), Zp(40.0 + KOR) + 22, "robot koridoru 800", f8, GRAY, "mm")
d.rectangle([Xp(QX), Zp(-30.0), Xp(QX + Q_D), Zp(Q_W - 30.0)], fill=FILL, outline=LINE, width=3)
for c in range(2):
    d.rectangle([Xp(QX + 40), Zp(0.0 + c * 410), Xp(QX + 480), Zp(390.0 + c * 410)], fill=BG, outline=INK, width=2)
    txt(Xp(QX + 260), Zp(195.0 + c * 410) - 8, "GÖZ × 6", f7, INK, "mm")
    txt(Xp(QX + 260), Zp(195.0 + c * 410) + 8, "440 × 380", f7, GRAY, "mm")
d.rectangle([Xp(QX + Q_D), Zp(Q_W - 30.0 - 220.0), Xp(QX + Q_D + 40), Zp(Q_W - 30.0)], fill=BG, outline=ACC, width=1)
txt(Xp(QX + Q_D) + 14, Zp(Q_W + 30.0), "PANEL · yan yüz", f7, ACC, "lm")
txt(Xp(QX + Q_D) + 14, Zp(400.0), "SOKAK · müşteri", f9, RED, "lm")
txt(Xp(QX) - 14, Zp(400.0), "robot kapakları", f7, RED, "rm")
cxp, cyp = Xp(R2X), Zp(RZ)
d.rectangle([Xp(R2X - 200), Zp(RZ - 200), Xp(R2X + 200), Zp(RZ + 200)], fill=SOFT, outline=ACC, width=1)
d.ellipse([cxp - 100 * S, cyp - 100 * S, cxp + 100 * S, cyp + 100 * S], fill=BG, outline=ACC, width=3)
darc(cxp, cyp, ERISIM_P * S, 270.0, 450.0, ACC, 2, 3.0)
txt(cxp, Zp(RZ + 200) + 22, "R2 · FR10 · pratik erişim 1250", f9, ACC, "mm")
txt(Xp(QX + 260), Zp(Q_W + 70.0), "en uzak göz: dx 750 · dz 420 · dy 700 → 1110 ✓", f7, ACC, "mm")
olcu_h(Xp(2800.0), Xp(3500.0), Zp(40.0) + 60, "700", f8, INK)
olcu_h(Xp(QX), Xp(QX + Q_D), Zp(40.0) + 60, sayi(Q_D), f8, INK)
olcu_v(Xp(QX + Q_D) + 150, Zp(-30.0), Zp(Q_W - 30.0), sayi(Q_W), f8, INK, "r")
txt(Xp(2100.0), Zp(-790.0) - 30, "ARKA", f9, GRAY, "la")


# ======================= 5 · SERVIS · on gorunus (en kucuk) =======================
SX0 = KX0 + Q_D * S + 420.0


def Xs(x):
    return SX0 + x * S


H_S = 2000.0
txt(SX0, FY_TOP - 190, "5 · SERVİS · ön görünüş · en küçük", f16, ACC)
txt(SX0, FY_TOP - 152, "karton kulesi 400 + mini tezgâh 800 = 1200 mm duvar · 4 günlük stok · elde yıkama · kaset doldurma", f9, GRAY)
# karton kulesi 400 x 800 x 2000
d.rectangle([Xs(0), Y(H_S), Xs(400), Y(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([Xs(0), Y(100.0), Xs(400), Y(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([Xs(25), Y(H_S - 25.0), Xs(375), Y(110.0)], fill=BG, outline=LINE, width=2)
d.rectangle([Xs(340), Y(1100.0), Xs(352), Y(1000.0)], fill=INK)
kesik(Xs, 45.0, 355.0, 130.0, 1950.0, "", INK)
for i in range(18):
    d.line([(Xs(55), Y(160.0 + i * 100.0)), (Xs(345), Y(160.0 + i * 100.0))], fill=BOSL, width=1)
txt(Xs(200), Y(1060.0) - 10, "KARTON BLANK", f8, INK, "mm")
txt(Xs(200), Y(1060.0) + 12, "400 × 760 · tek yığın 1.820", f7, GRAY, "mm")
txt(Xs(200), Y(1060.0) + 32, "= 1.010 (1,8 mm) – 1.210 (1,5 mm)", f7, GRAY, "mm")
txt(Xs(200), Y(1060.0) + 52, "4 gün = 1.120 → blank ≤ 1,6 mm", f7, GRAY, "mm")
txt(Xs(200), Y(H_S) - 64, "KARTON KULESİ", f13, INK, "md")
olcu_h(Xs(0), Xs(400), Y(H_S) - 26, "400", f11, INK)
txt(Xs(200), Y(40.0), "tek kapak · 400 × 800 × 2000", f7, GRAY, "mm")
# mini tezgah 800 x 600 x 850
d.rectangle([Xs(400), Y(850.0), Xs(1200), Y(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([Xs(400), Y(100.0), Xs(1200), Y(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([Xs(390), Y(890.0), Xs(1210), Y(850.0)], fill=SOFT, outline=LINE, width=2)
txt(Xs(800), Y(H_S) - 64, "MİNİ TEZGÂH", f13, INK, "md")
olcu_h(Xs(400), Xs(1200), Y(H_S) - 26, "800", f11, INK)
d.rectangle([Xs(420), Y(830.0), Xs(790), Y(110.0)], fill=BG, outline=LINE, width=2)
d.rectangle([Xs(750), Y(520.0), Xs(762), Y(420.0)], fill=INK)
kesik(Xs, 450.0, 730.0, 560.0, 800.0, "TEMİZLİK", INK, "kimyasal · bez · fırça")
kesik(Xs, 450.0, 730.0, 300.0, 540.0, "SARF", INK, "eldiven · poşet · sachet")
kesik(Xs, 450.0, 730.0, 130.0, 280.0, "YEDEK", INK, "tepsi × 6 · pençe · bıçak")
d.rectangle([Xs(800), Y(830.0), Xs(1180), Y(110.0)], fill=BG, outline=LINE, width=2)
d.rectangle([Xs(812), Y(520.0), Xs(824), Y(420.0)], fill=INK)
kesik(Xs, 840.0, 1160.0, 130.0, 560.0, "ÇÖP 60 L", GRAY, "evye altı")
kesik(Xs, 840.0, 1160.0, 600.0, 800.0, "sifon", GRAY)
d.rectangle([Xs(420), Y(910.0), Xs(780), Y(890.0)], fill=BG, outline=INK, width=1)
txt(Xs(600), Y(990.0) - 8, "DOLDURMA YÜZEYİ 360 × 600", f8, INK, "mm"); txt(Xs(600), Y(990.0) + 12, "kaset dolar → hatta", f7, GRAY, "mm")
d.rectangle([Xs(800), Y(890.0), Xs(1200), Y(600.0)], fill=SU, outline=BUZ, width=2)
txt(Xs(1000), Y(745.0) - 8, "EVYE 400 × 400 × 250", f8, BUZ, "mm"); txt(Xs(1000), Y(745.0) + 12, "kaset · tepsi · kap", f7, GRAY, "mm")
# ust dolap 800 x 350 x 700
d.rectangle([Xs(400), Y(2100.0), Xs(1200), Y(1400.0)], fill=FILL, outline=LINE, width=3)
txt(Xs(800), Y(2100.0) + 34, "ÜST DOLAP 800 × 350 × 700", f8, GRAY, "mm")
d.rectangle([Xs(420), Y(2080.0), Xs(1180), Y(1420.0)], fill=BG, outline=LINE, width=2)
d.rectangle([Xs(1140), Y(1800.0), Xs(1152), Y(1700.0)], fill=INK)
kesik(Xs, 450.0, 1150.0, 1450.0, 2050.0, "İÇECEK 4 GÜN · 280 kutu", INK, "12 shrink 24'lü · 400 × 270 × 125 · 0,16 m³ · oda sıcaklığı")
# el lavabosu duvarda
d.rectangle([Xs(1260), Y(1150.0), Xs(1610), Y(900.0)], fill=SU, outline=BUZ, width=2)
txt(Xs(1435), Y(1025.0) - 8, "EL LAVABOSU", f8, BUZ, "mm"); txt(Xs(1435), Y(1025.0) + 12, "350 × 300 duvar tipi · ayrı", f7, GRAY, "mm")
d.rectangle([Xs(1310), Y(1400.0), Xs(1560), Y(1200.0)], fill=BG, outline=GRAY, width=1)
txt(Xs(1435), Y(1300.0) - 8, "sabun · kâğıt havlu", f7, GRAY, "mm"); txt(Xs(1435), Y(1300.0) + 8, "hijyen listesi", f7, GRAY, "mm")
# duvar: mini UPS + NVR + yangin + kamera
d.rectangle([Xs(1260), Y(1800.0), Xs(1460), Y(1500.0)], fill=BG, outline=INK, width=1)
txt(Xs(1360), Y(1650.0) - 8, "MİNİ UPS 500 VA", f7, INK, "mm"); txt(Xs(1360), Y(1650.0) + 8, "200 × 300 · PLC + modem + kilit", f7, GRAY, "mm")
d.rectangle([Xs(1480), Y(1800.0), Xs(1680), Y(1500.0)], fill=BG, outline=INK, width=1)
txt(Xs(1580), Y(1650.0) - 8, "NVR + MODEM", f7, INK, "mm"); txt(Xs(1580), Y(1650.0) + 8, "duvarda · 200 × 300", f7, GRAY, "mm")
d.rectangle([Xs(1760), Y(1500.0), Xs(1880), Y(1100.0)], fill=RED, outline=INK, width=1)
txt(Xs(1820), Y(1560.0), "6 kg ABC", f7, RED, "mm")
d.rectangle([Xs(1920), Y(1500.0), Xs(2040), Y(1100.0)], fill=(140, 140, 150), outline=INK, width=1)
txt(Xs(1980), Y(1560.0), "5 kg CO₂", f7, INK, "mm")
txt(Xs(1900), Y(1050.0), "askı kotu 900", f7, GRAY, "mm")
d.ellipse([Xs(1820) - 14, Y(2300.0) - 14, Xs(1820) + 14, Y(2300.0) + 14], fill=BG, outline=INK, width=2)
txt(Xs(1820), Y(2360.0), "duman dedektörü", f7, INK, "mm")
d.rectangle([Xs(1940), Y(2320.0), Xs(2020), Y(2280.0)], fill=INK)
txt(Xs(1980), Y(2360.0), "kamera", f7, INK, "mm")
olcu_h(Xs(0), Xs(SV_W), Y(0) + 44, "SERVİS  %s" % sayi(SV_W), f13, INK)
olcu_h(Xs(1260), Xs(1610), Y(0) + 44, "el lavabosu 350", f7, GRAY)
olcu_v(Xs(0) - 44, Y(H_S), Y(0), sayi(H_S), f11, INK, "l")
for yy in (100.0, 850.0, 1400.0, 2100.0):
    d.line([(Xs(1200) + 6, Y(yy)), (Xs(1200) + 24, Y(yy))], fill=INK, width=2)
    txt(Xs(1200) + 30, Y(yy), sayi(yy), f8, INK, "lm")

# ======================= 6 · SERVIS · plan =======================
txt(SX0, PY_TOP - 150, "6 · SERVİS · plan", f16, ACC)


def Zs(z):
    return PY_TOP + 40 + z * S


d.rectangle([Xs(0), Zs(0), Xs(400), Zs(800)], fill=FILL, outline=LINE, width=3)
drect(Xs(20), Zs(20), Xs(380), Zs(780), INK, 1)
txt(Xs(200), Zs(400) - 8, "KARTON KULESİ", f7, INK, "mm"); txt(Xs(200), Zs(400) + 8, "400 × 800 · blank 760", f7, GRAY, "mm")
d.rectangle([Xs(400), Zs(0), Xs(1200), Zs(350)], fill=SOFT, outline=GRAY, width=1)
txt(Xs(800), Zs(175), "ÜST DOLAP 800 × 350 (tezgâh üstünde)", f7, GRAY, "mm")
d.rectangle([Xs(400), Zs(0), Xs(1200), Zs(600)], fill=FILL, outline=LINE, width=3)
drect(Xs(420), Zs(20), Xs(780), Zs(580), INK, 1)
txt(Xs(600), Zs(450) - 8, "DOLDURMA", f7, INK, "mm"); txt(Xs(600), Zs(450) + 8, "360 × 600", f7, GRAY, "mm")
d.rectangle([Xs(800), Zs(100), Xs(1200), Zs(500)], fill=SU, outline=BUZ, width=2)
txt(Xs(1000), Zs(300), "EVYE 400 × 400", f7, BUZ, "mm")
d.rectangle([Xs(1260), Zs(0), Xs(1610), Zs(300)], fill=SU, outline=BUZ, width=2)
txt(Xs(1435), Zs(150), "EL LAVABOSU 350 × 300", f7, BUZ, "mm")
d.line([(Xs(-60), Zs(0)), (Xs(2100), Zs(0))], fill=INK, width=4)
txt(Xs(800), Zs(0) - 22, "DUVAR", f9, GRAY, "mm")
d.line([(Xs(-60), Zs(800 + 900)), (Xs(2100), Zs(800 + 900))], fill=GRAY, width=1)
txt(Xs(800), Zs(800 + 900) + 22, "eleman geçişi 900", f8, GRAY, "mm")
olcu_v(Xs(2100) + 60, Zs(0), Zs(800), "800", f8, INK, "r")
olcu_v(Xs(2100) + 60, Zs(800), Zs(1700), "900", f8, INK, "r")
olcu_h(Xs(0), Xs(400), Zs(1700) + 60, "400", f8, INK)
olcu_h(Xs(400), Xs(1200), Zs(1700) + 60, "800", f8, INK)
olcu_h(Xs(1260), Xs(1610), Zs(1700) + 60, "350", f8, INK)
txt(Xs(800), Zs(0) - 60, "KAMERA 4: koridor · servis · teslim cephesi · giriş → NVR (duvarda)", f7, GRAY, "mm")

# ======================= PARCA LISTESI =======================
TX, TY = OX, PY_TOP + 1200
txt(TX, TY - 60, "PARÇA LİSTESİ · servis + teslim v3", f16, ACC)
PARCA = [
    ("QR DOLABI", "12 ısıtmalı göz 380 × 190 × 440 · robot kapağı motorlu · müşteri mandalı elektrikli", "1", "860 × 520 × 1650 · soğutucu yok · Çin 3.300 $ sınıfı"),
    ("QR DOLABI", "yan yüz paneli: 7\" ekran + QR okuyucu + PIN tuş takımı", "1", "220 × 400 · kot 1000–1400 · sokak tarafı"),
    ("QR DOLABI", "kilit/kapak kartı · 24 V güç 150 W · modem · PLC bağlantısı", "1 set", "alt bölme 100–340"),
    ("SERVİS", "karton kulesi 400 × 800 × 2000 · tek kapak · tek yığın 1.820", "1", "1.010–1.210 blank · 4 gün 1.120 → blank ≤ 1,6 mm"),
    ("SERVİS", "mini tezgâh 800 × 600 × 850 · evye 400 × 400 × 250 · doldurma 360 · altı temizlik/sarf/yedek/çöp", "1", "elde yıkama + kaset doldurma"),
    ("SERVİS", "üst dolap 800 × 350 × 700", "1", "içecek 4 gün 280 kutu (12 shrink)"),
    ("SERVİS", "el yıkama lavabosu duvar tipi 350 × 300 · sıcak-soğuk · sabun · kâğıt havlu", "1", "evyeden ayrı · hijyen yönetmeliği"),
    ("SERVİS", "mini UPS 500 VA · 200 × 300 · duvarda", "1", "yalnız PLC + modem + QR kilitleri (elektrik kesilince sipariş/teslim kilitlenmesin) · 3 kVA kalktı"),
    ("GÜVENLİK", "kamera 4 + NVR 1 TB (tezgâh altı)", "1", "30 gün · mobil izleme"),
    ("YANGIN", "6 kg ABC + 5 kg CO₂ · askı 900 · duman dedektörü · D içinde aerosol", "1 set", "Binaların Yangından Korunması Yön."),
    ("KALDIRILAN", "bulaşık makinesi · içecek soğutucu · UPS 3 kVA · 1800'lük tezgâh", "—", "yıkama elde · içecek soğuk stoğu kararı açık"),
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
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "kapak (robot / müşteri)", False), (BUZ, SU, "su", False), (INK, BG, "kapak arkası parça", True), (ACC, BG, "robot · erişim · panel", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "QR dolabı 860 × 520 × 1650 · 12 göz · QR/PIN  ·  karton kulesi 400 + mini tezgâh 800 + üst dolap + duvar lavabosu 350  ·  4 gün stok (karton 1.120 · içecek 280)  ·  bulaşık makinesi yok · UPS 3 kVA yok  ·  UPS 3 kVA  ·  4 kamera  ·  2 söndürücü + aerosol", f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT)
