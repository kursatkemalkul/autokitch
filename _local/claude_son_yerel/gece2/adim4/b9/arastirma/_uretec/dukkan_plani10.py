# -*- coding: utf-8 -*-
"""DUKKAN PLANI v10 (17 Eyl 2026) — v9 Kemal: QR dolabini robota yanastir (arkasi y 150, cephede 61 nis), ust raflara erisim: elektronik uste, altta 40 bosluk, gozler 40-160; kutuyla birlikte icecek + tatli da goze -> E altinda sogutmali cekmece.
v9: — Kemal: "ray olsun, FR5 erisebilecegi kadar yakin; cekmece acilirken robot saga/sola kayar, alir, cekmece kapanir, prese gider — ciz, oluyor mu?"
v8 dukkan mantigi (hat arkada, koridor, ince duvar, on zon 84, QR cephede) + TEK FR5 YER RAYINDA (eksen z 25). Koridor 90'a iner.
Pafta: plan + cekmece dizisi (3 kare) + erisim tablosu. Olculer cm. Robot: FR5 922 mm, pratik 83 cm; omuz 100.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v10_ray.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3400, 2750
S = 3.0
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT, GRN = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234), (14, 120, 90)
SU, DUV, KOR, CAM, TEZ, AGZ = (214, 236, 250), (200, 200, 205), (235, 241, 250), (200, 225, 250), (250, 238, 220), (253, 244, 243)


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


# ======================= VERI (cm) =======================
HAT_D, KOR_D, DUV_D, ON_D = 83.0, 90.0, 6.0, 84.0
IC_W = 390.0
IC_D = HAT_D + KOR_D + DUV_D + ON_D                          # 263
MOD = [("A · PRESS", 0.0, 70.0), ("B · ÇEKMECE  +  C · TOPPING", 70.0, 210.0), ("D · FIRIN", 210.0, 280.0), ("E · KUTU + İÇECEK", 280.0, 350.0)]
KOLONX = [(76.25, 138.25), (141.75, 203.75), (145.0 + 62.25, 145.0 + 124.25)]   # K1 K2 K3 on yuz araligi (mm/10) — B icinde 3 kolon
KOLONX = [(70.0 + 6.25, 70.0 + 68.25), (70.0 + 71.75, 70.0 + 133.75), (70.0 + 137.25, 70.0 + 199.25)]
KULE = (350.0, 390.0, 3.0, 83.0)
Y_KOR0, Y_KOR1 = HAT_D, HAT_D + KOR_D
Y_DUV1 = Y_KOR1 + DUV_D
Y_ON = IC_D
RAY_Z = 25.0                                                # ray ekseni hattin onunden
RAY_Y = Y_KOR0 + RAY_Z
RAY_X = (10.0, 380.0)
ROB_X = 105.0                                               # cizimde robotun durdugu yer (K1 onu)
ERIS = 83.0                                                 # FR5 pratik
AKT = (190.0, 230.0, Y_KOR0 + 48.0, Y_KOR0 + 88.0)          # aktarma rafi koridorun dis kenarinda (rayin arkasi)
KAPI = (0.0, 75.0)
TEZ_ = (75.0, 215.0, Y_ON - 30.0, Y_ON)
PEN = (80.0, 210.0)
MINI = (215.0, 295.0, Y_ON - 40.0, Y_ON)
QR = (304.0, 390.0, 150.0, 202.0)                          # robota yanastirildi: arkasi y 150 (koridora 23 girer), yuzu y 202, cephe 263 -> nis 61
QRX = (QR[0] + QR[1]) / 2.0                                  # robot bu hizada durur (x 347)
LAV = (0.0, 30.0, Y_DUV1 + 6.0, Y_DUV1 + 41.0)
DUV_X1 = QR[0]
OX, OY = 140.0, 330.0


def X(x):
    return OX + x * S


def Y(y):
    return OY + y * S


# ======================= BASLIK =======================
txt(OX, 60, "AUTOKITCH  ·  DÜKKAN v10 · RAYLI  ·  QR DOLABI ROBOTA YANAŞTI (cephede 61 niş)  ·  E ALTINDA İÇECEK + TATLI  ·  iç 390 × 263", f38, INK)
txt(OX, 122, "tek FR5 yer rayında (z 25, omuz 100, pratik 83) · QR dolabı arkası koridora 23 girer, robot dolabın ortasında durup 12 gözün hepsine yetişir · gözler 40–160, elektronik üstte, altta 40 boşluk · kutu + içecek + tatlı aynı göze · ölçüler cm · 17 Eylül 2026", f13, GRAY)
d.line([(OX, 160), (W_PX - 140, 160)], fill=LINE, width=3)

# ======================= PLAN =======================
txt(OX, OY - 110, "PLAN (üstten) · raylı", f16, ACC)
d.rectangle([X(-12), Y(-12), X(IC_W + 12), Y(IC_D)], fill=DUV, outline=LINE, width=3)
d.rectangle([X(0), Y(0), X(IC_W), Y(IC_D)], fill=BG, outline=LINE, width=3)
for ad, x0, x1 in MOD:
    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_D)], fill=FILL, outline=LINE, width=3)
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 - 10), ad, f11, INK, "mm")
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 + 8), "%s × 83" % sayi(x1 - x0), f7, GRAY, "mm")
for i, (kx0, kx1) in enumerate(KOLONX):
    drect(X(kx0), Y(HAT_D - 68), X(kx1), Y(HAT_D), GRN, 1)
    txt(X((kx0 + kx1) / 2), Y(HAT_D - 8), "K%d" % (i + 1), f7, GRN, "mm")
drect(X(284.0), Y(HAT_D - 68), X(346.0), Y(HAT_D), GRN, 1)
txt(X(315), Y(HAT_D - 8), "İÇ+TATLI", f7, GRN, "mm")
d.rectangle([X(KULE[0]), Y(KULE[2]), X(KULE[1]), Y(KULE[3])], fill=BG, outline=LINE, width=2)
txt(X(370), Y(38), "KARTON", f7, INK, "mm"); txt(X(370), Y(52), "KULESİ", f7, INK, "mm"); txt(X(370), Y(66), "40 × 80", f7, GRAY, "mm")
d.rectangle([X(0), Y(Y_KOR0), X(IC_W), Y(Y_KOR1)], fill=KOR, outline=None)
txt(X(IC_W - 6), Y(Y_KOR0 + 8), "ROBOT KORİDORU 90", f9, ACC, "ra")
# ray
d.rectangle([X(RAY_X[0]), Y(RAY_Y - 6), X(RAY_X[1]), Y(RAY_Y + 6)], fill=ACC, outline=INK, width=1)
txt(X(250), Y(RAY_Y + 16), "YER RAYI · strok 370 · eksen z 25", f8, ACC, "mm")
# acik cekmece K1 (robot yana kaymis)
d.rectangle([X(KOLONX[0][0]), Y(HAT_D), X(KOLONX[0][1]), Y(HAT_D + 70)], fill=BG, outline=GRN, width=2)
txt(X(107), Y(HAT_D + 30), "K1 AÇIK · 70", f8, GRN, "mm"); txt(X(107), Y(HAT_D + 44), "ön sıra robota", f7, GRAY, "mm")
# robot: K1'in saginda, rayda
RX = KOLONX[0][1] + 10.0 + 15.0                              # cekmece kenari + 10 pay + kaide yaricapi 15 -> x 163
d.rectangle([X(RX - 20), Y(RAY_Y - 15), X(RX + 20), Y(RAY_Y + 15)], fill=SOFT, outline=ACC, width=1)
d.ellipse([X(RX) - 10 * S, Y(RAY_Y) - 10 * S, X(RX) + 10 * S, Y(RAY_Y) + 10 * S], fill=BG, outline=ACC, width=3)
txt(X(RX), Y(RAY_Y + 26), "FR5 · rayda", f8, ACC, "mm"); txt(X(RX), Y(RAY_Y + 36), "araba 40 × 30 · kaide 82", f7, GRAY, "mm")
# erisim yaylari (ic mekana kirpili) — robot burada
lay = Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
a = 0.0
while a < 360.0:
    ld.arc([X(RX) - ERIS * S, Y(RAY_Y) - ERIS * S, X(RX) + ERIS * S, Y(RAY_Y) + ERIS * S], a, min(360.0, a + 2.0), fill=ACC + (255,), width=2)
    a += 4.0
for px in (35.0, QRX):                                      # pres onu ve QR onu
    a = 0.0
    while a < 360.0:
        ld.arc([X(px) - ERIS * S, Y(RAY_Y) - ERIS * S, X(px) + ERIS * S, Y(RAY_Y) + ERIS * S], a, min(360.0, a + 2.0), fill=(150, 150, 160, 255), width=1)
        a += 5.0
box = (int(X(0)) + 2, int(Y(0)) + 2, int(X(IC_W)) - 2, int(Y(IC_D)) - 2)
im.paste(lay.crop(box), box[:2], lay.crop(box)); d = ImageDraw.Draw(im)
for px, et in ((35.0, "pres önünde"),):
    d.ellipse([X(px) - 6, Y(RAY_Y) - 6, X(px) + 6, Y(RAY_Y) + 6], fill=(150, 150, 160))
    txt(X(px), Y(RAY_Y - 14), et, f7, GRAY, "mm")
txt(X(6), Y(Y_KOR1 - 10), "mavi daire: FR5 pratik erişim 83 (robot K1 yanında) · gri: pres önünde ve QR dolabı önünde", f7, ACC, "la")
# aktarma rafi
d.rectangle([X(AKT[0]), Y(AKT[2]), X(AKT[1]), Y(AKT[3])], fill=BG, outline=ACC, width=2)
txt(X(210), Y(AKT[2] + 14), "AKTARMA", f7, ACC, "mm"); txt(X(210), Y(AKT[2] + 28), "RAFI · ray arkası", f7, GRAY, "mm")
# ince duvar + kapi
d.rectangle([X(0), Y(Y_KOR1), X(DUV_X1), Y(Y_DUV1)], fill=DUV, outline=LINE, width=1)
d.rectangle([X(40), Y(Y_KOR1 - 1), X(110), Y(Y_DUV1 + 1)], fill=AGZ, outline=RED, width=2)
txt(X(75), Y(Y_DUV1 + 8), "HÜCRE KAPISI 70", f7, RED, "mm")
d.rectangle([X(DUV_X1), Y(QR[3]), X(IC_W), Y(IC_D)], fill=(236, 236, 240), outline=LINE, width=2)
txt(X(347), Y(QR[3] + 24), "CEPHE NİŞİ 86 × 61", f8, GRAY, "mm"); txt(X(347), Y(QR[3] + 38), "müşteri buradan alır · panel dolap yüzünde", f7, GRAY, "mm")
d.rectangle([X(DUV_X1 - 6), Y(Y_KOR1), X(DUV_X1), Y(IC_D)], fill=DUV, outline=LINE, width=1)
# on zon
txt(X(175), Y(Y_DUV1 + 14), "ELEMAN GEÇİDİ 54", f8, GRAY, "mm")
d.rectangle([X(TEZ_[0]), Y(TEZ_[2]), X(TEZ_[1]), Y(TEZ_[3])], fill=TEZ, outline=INK, width=2)
txt(X(145), Y(TEZ_[2] + 15), "TEZGÂH 140 × 30 · sürme cam 130", f8, INK, "mm")
d.rectangle([X(PEN[0]), Y(IC_D - 4), X(PEN[1]), Y(IC_D + 2)], fill=CAM, outline=ACC, width=1)
d.rectangle([X(MINI[0]), Y(MINI[2]), X(MINI[1]), Y(MINI[3])], fill=TEZ, outline=INK, width=2)
d.rectangle([X(255), Y(MINI[2] + 2), X(293), Y(MINI[3] - 2)], fill=SU, outline=ACC, width=1)
txt(X(235), Y(MINI[2] + 14), "DOLDURMA", f7, INK, "mm"); txt(X(274), Y(MINI[2] + 14), "EVYE", f7, ACC, "mm")
d.rectangle([X(QR[0]), Y(QR[2]), X(QR[1]), Y(QR[3])], fill=FILL, outline=INK, width=3)
txt(X(347), Y(QR[2] + 14), "QR DOLABI 86 × 52 × 200", f8, INK, "mm"); txt(X(347), Y(QR[2] + 28), "arkası y 150 · robot yükler", f7, GRAY, "mm"); txt(X(347), Y(QR[2] + 42), "yüzü y 202 · müşteri", f7, GRAY, "mm")
d.rectangle([X(LAV[0]), Y(LAV[2]), X(LAV[1]), Y(LAV[3])], fill=SU, outline=ACC, width=1)
txt(X(40), Y(LAV[2] + 12), "EL LAVABOSU", f7, ACC, "la")
d.rectangle([X(KAPI[0]), Y(IC_D - 2), X(KAPI[1]), Y(IC_D + 12)], fill=BG, outline=INK, width=2)
txt(X(37), Y(IC_D + 24), "KAPI 75 · dışa açılır", f7, INK, "mm")
txt(X(IC_W / 2), Y(IC_D) + 50, "KALDIRIM / SOKAK", f9, GRAY, "mm")
# QR erisim cizgisi: ray ucundan dolap arkasina
d.ellipse([X(QRX) - 6, Y(RAY_Y) - 6, X(QRX) + 6, Y(RAY_Y) + 6], fill=(150, 150, 160))
txt(X(QRX), Y(RAY_Y - 14), "QR önünde", f7, GRAY, "mm")
for gx in (QR[0] + 22.5, QR[1] - 22.5):
    dline((X(QRX), Y(RAY_Y)), (X(gx), Y(QR[2])), GRN, 2, 8, 5)
txt(X(QRX), Y(QR[2] - 10), "dz 42 · dx 21 → üst göz (160) 82 OK · alt göz (40) 79 OK", f7, GRN, "mm")
# olculer
olcu_v(X(IC_W) + 40, Y(0), Y(HAT_D), "hat 83", f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR0), Y(Y_KOR1), "robot 90", f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR1), Y(Y_DUV1), "6", f7, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_DUV1), Y(IC_D), "ön 84", f8, INK, "r")
olcu_v(X(IC_W) + 120, Y(0), Y(IC_D), sayi(IC_D), f11, INK, "r")
olcu_v(X(0) - 40, Y(Y_KOR0), Y(RAY_Y), "ray 25", f7, INK, "l")
yb = Y(IC_D) + 90
for x0, x1, s_ in ((0, 75, "kapı 75"), (75, 215, "tezgâh 140"), (215, 295, "servis 80"), (304, 390, "QR 86")):
    olcu_h(X(x0), X(x1), yb, s_, f8, INK)
olcu_h(X(0), X(IC_W), yb + 40, sayi(IC_W), f11, INK)
olcu_h(X(0), X(350), Y(0) - 30, "HAT 350", f9, INK)

# ======================= CEKMECE DIZISI (3 kare) =======================
DX0, DY0 = OX, Y(IC_D) + 210
txt(DX0, DY0 - 50, "ÇEKMECE DİZİSİ · K1 (plan, 1 cm = 2 px)", f16, ACC)
s2 = 2.0
KW = 300 * s2 + 60


def kare(i, baslik, robot_x, acik, ok_txt):
    x0 = DX0 + i * (KW + 40)
    y0 = DY0
    d.rectangle([x0, y0, x0 + KW, y0 + 220], fill=BG, outline=LINE, width=2)
    txt(x0 + 10, y0 + 12, baslik, f9, INK)
    bx = x0 + 30; by = y0 + 40
    def px(x): return bx + x * s2
    def py(z): return by + z * s2
    d.rectangle([px(0), py(0), px(210), py(HAT_D * 0.5)], fill=FILL, outline=LINE, width=2)    # hat (derinlik yari)
    for kx0, kx1 in KOLONX:
        d.rectangle([px(kx0 - 70), py(10), px(kx1 - 70), py(41)], fill=BG, outline=GRN, width=1)
    if acik:
        d.rectangle([px(KOLONX[0][0] - 70), py(41), px(KOLONX[0][1] - 70), py(41 + 35)], fill=(235, 250, 242), outline=GRN, width=2)
        txt(px(KOLONX[0][0] - 70 + 31), py(58), "K1 açık 70", f7, GRN, "mm")
    d.rectangle([px(0), py(41 + 12.5 - 3), px(210), py(41 + 12.5 + 3)], fill=ACC)          # ray z 25 -> yari olcek
    d.ellipse([px(robot_x - 70) - 15, py(41 + 12.5) - 15, px(robot_x - 70) + 15, py(41 + 12.5) + 15], fill=BG, outline=ACC, width=3)
    txt(px(robot_x - 70), py(41 + 12.5) + 30, "FR5", f7, ACC, "mm")
    txt(x0 + 10, y0 + 200, ok_txt, f8, GRAY)


kare(0, "1 · robot K1 önünde, çekmece kapalı", 107.0, False, "ray x 107 · kaide çekmecenin önünde")
kare(1, "2 · robot 56 sağa kayar, K1 açılır, yandan alır", 163.0, True, "kaide çekmece kenarından 10 uzakta · en uzak top 86 → YOK (83)")
kare(2, "3 · çekmece kapanır, robot prese gider", 35.0, False, "pres önü x 35 · plaka kot ~164 → 92 YOK")
# QR dolabi on gorunus (robot tarafi), 1 cm = 2 px
QX0, QY0 = DX0 + 3 * (KW + 40) + 40, DY0 + 90
txt(QX0, QY0 - 50, "QR DOLABI · robot tarafı (1 cm = 2 px)", f16, ACC)
def qx(x): return QX0 + x * 2.0
def qy(z): return QY0 + (200.0 - z) * 2.0
d.rectangle([qx(0), qy(200), qx(86), qy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([qx(3), qy(200), qx(83), qy(165)], fill=BG, outline=LINE, width=2)
txt(qx(43), qy(182), "ELEKTRONİK · kilit · güç · modem", f7, INK, "mm")
for r in range(6):
    z0 = 40.0 + r * 20.0
    for c in range(2):
        d.rectangle([qx(3 + c * 41), qy(z0 + 19), qx(42 + c * 41), qy(z0)], fill=BG, outline=INK, width=1)
txt(qx(43), qy(0) + 52, "12 GÖZ 38 × 19 × 44 · kot 40–160", f7, INK, "mm")
d.rectangle([qx(3), qy(40), qx(83), qy(0)], fill=SOFT, outline=LINE, width=1)
txt(qx(43), qy(20), "BOŞLUK 40", f7, GRAY, "mm")
olcu_v(qx(86) + 20, qy(200), qy(165), "35", f7, INK, "r"); olcu_v(qx(86) + 20, qy(160), qy(40), "120", f7, INK, "r"); olcu_v(qx(86) + 20, qy(40), qy(0), "40", f7, INK, "r")
olcu_h(qx(0), qx(86), qy(0) + 30, "86", f8, INK)

# ======================= ERISIM TABLOSU + KARAR (sag panel) =======================
PX0 = X(IC_W) + 260
d.rectangle([PX0, OY - 60, PX0 + 1050, OY + 960], fill=BG, outline=LINE, width=3)
txt(PX0 + 30, OY - 20, "FR5 RAYDA — ERİŞİM KONTROLÜ (omuz 100, ray z 25) · v10", f16, INK)
TAB = [("Hedef", "dx", "dy", "dz", "mesafe", "FR5 83"),
       ("K1–K3 üst çekmece topu (yandan)", "55", "5", "35", "65", "OK"),
       ("K1–K3 alt çekmece topu (yandan)", "55", "57", "35", "87", "YOK"),
       ("K1–K3 alt çekmece — dolu yarı, dx 31", "31", "57", "35", "74", "OK (yarım)"),
       ("Topping ağzı (taban kot 107–118)", "0", "12", "60", "61", "OK"),
       ("Pres plakası — PZP B üstünde, kot ~164", "0", "70", "60", "92", "YOK"),
       ("Pres plakası — tezgâh üstü pres, kot ≤ 115", "0", "15", "60", "62", "OK"),
       ("Fırın üst göz (taban 172)", "0", "75", "60", "96", "YOK"),
       ("Fırın orta göz (taban 139)", "0", "42", "60", "73", "OK"),
       ("Fırın alt göz (taban 107)", "0", "10", "60", "61", "OK"),
       ("Kesici · yağ ağzı (kot 60–110)", "0", "40", "55", "68", "OK"),
       ("Kutu ağzı (kot 43–68)", "0", "45", "50", "67", "OK"),
       ("Aktarma rafı (ray arkası, kot 90–130)", "0", "0", "48", "48", "OK"),
       ("E içecek + tatlı çekmecesi (yandan, kutu üstü 54)", "55", "44", "35", "78", "OK"),
       ("QR üst göz 160 (robot dolap ortasında x 347)", "21", "60", "42", "76", "OK"),
       ("QR alt göz 40", "21", "60", "42", "76", "OK"),
       ("QR dolabı cephede kalsaydı (arkası y 211)", "38", "5", "103", "110", "YOK")]
yy = OY + 30
cols = (0, 470, 560, 640, 720, 840)
for i, row in enumerate(TAB):
    for cx_, s_ in zip(cols, row):
        c_ = INK
        if i and s_.startswith("OK"):
            c_ = GRN
        if i and s_.startswith("YOK"):
            c_ = RED
        txt(PX0 + 30 + cx_, yy, s_, f9 if i else f8, c_ if i else GRAY)
    yy += 32
    if i == 0:
        d.line([(PX0 + 30, yy - 8), (PX0 + 1020, yy - 8)], fill=SOFT, width=2)
d.line([(PX0 + 30, yy - 4), (PX0 + 1020, yy - 4)], fill=SOFT, width=2)
yy += 14
KARAR = [
    "QR DOLABI: arkası koridora 23 girdi (y 150); robot dolabın ortasında durur → 12 gözün hepsi OK (dz 42, dx ≤ 21, dy ≤ 60).",
    "  gözler 40–160 (alt boşluk 40, robot üst limiti 160 → 6 sıra × 20) · elektronik üstte 165–200 · dolap 86 × 52 × 200.",
    "  Cephede 61 derinliğinde niş: müşteri nişe girip alır; panel dolap yüzünde. Kapı/tezgâh cephesi düz kalır.",
    "  Göz 38 × 19 × 44: kutu 32 × 32 × 4,5 + yanına içecek (Ø6,6 × 11,5 yatık) + tatlı → 32 + 6,6 = 38,6 ≤ 44 OK.",
    "E · KUTU + İÇECEK: altta kendi 1/5 HP soğutucusu (0–24) + 2 katlı içecek çekmecesi 62 × 68 (180 kutu, 2,6 gün, tatlı köşede)",
    "  28,7–56; katlayıcı 57–74; kutu ağzı 75–100; şarjör 101–203 = 570–680 kutu (2 gün OK). Robot yandan alır (78 OK).",
    "HÂLÂ AÇIK (FR5 için): pres plakası PZP B üstündeyken 92 YOK → tezgâh üstü pres; fırın üst gözü 172 → 96 YOK → gözler alta.",
    "KAPASİTE: tek robot ~34/saat (105 s/ürün); günlük 280 OK, akşam piki 55 YOK. 2. robot sonra, ray hazır.",
    "RAY: 3,7 m strok · eksen z 25 · araba 40 × 30 · kapaklı · hız ≥ 1 m/s · fiyat Logorob'dan bekleniyor.",
]
for l in KARAR:
    txt(PX0 + 30, yy, l, f9 if not l.startswith(" ") else f8, INK if not l.startswith(" ") else GRAY)
    yy += 30

d.line([(OX, H_PX - 80), (W_PX - 140, H_PX - 80)], fill=LINE, width=2)
txt(W_PX - 140, H_PX - 45, "AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v10_ray · 17 Eyl 2026 · üretici _uretec/dukkan_plani10.py", f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT)
