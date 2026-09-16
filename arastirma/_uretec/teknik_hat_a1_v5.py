# -*- coding: utf-8 -*-
"""AUTOKITCH - ROBOT YERLESIMI v5 (16 Eyl 2026): Kemal'in iki secenegi. ON + UST GORUNUS.
SECENEK 1: TEK ROBOT + HAVADAN RAY (tavan kirisi 2300, sarkitma, omuz 1400, FR5 922, strok 4400).
SECENEK 2: IKI SABIT ROBOT (ikisi de makine yuzune 1400 kotunda bagli; robot 1 gunluk cekmece + pres,
           robot 2 kutuyu alir arkasini donup karsi duvardaki 12 gozlu QR dolabina koyar).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda. Olculer mm.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_ROBOT_v5_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 5400, 3500
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (246, 246, 248), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, SOGUK, HAVA, ERIS = (14, 120, 90), (226, 238, 252), (255, 225, 200), (205, 218, 236)
QRC, ICE, TEK = (240, 214, 170), (214, 226, 244), (238, 238, 242)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f8, f9, f11, f13, f16, f20, f34 = F(17), F(19), F(22), F(25), F(29, True), F(34, True), F(50, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


def txt(x, y, s, f=f11, c=INK, a="la"):
    d.text((x, y), s, font=f, fill=c, anchor=a)


def dline(p0, p1, c, w=1, dash=9, gap=6):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0, t1 = min(1.0, i * (dash + gap) / L), min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def dcircle(cx, cy, r, c, w=2, step=5):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 361, step)]
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=c, width=w)


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 16 * math.cos(a + s_), y1 - 16 * math.sin(a + s_))], fill=c, width=w)


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


def kol(px, pz, S, shoulder_x, shoulder_z, hedef_x, hedef_z):
    """basit FR5 silueti: omuzdan dirsege, dirsekten hedefe"""
    mx = (shoulder_x + hedef_x) / 2
    mz = max(shoulder_z, hedef_z) + 330
    d.line([(px(shoulder_x), pz(shoulder_z)), (px(mx), pz(mz))], fill=ACC, width=11)
    d.line([(px(mx), pz(mz)), (px(hedef_x), pz(hedef_z + 120))], fill=ACC, width=11)
    d.line([(px(hedef_x), pz(hedef_z + 120)), (px(hedef_x), pz(hedef_z + 40))], fill=ACC, width=8)
    d.rectangle([px(hedef_x) - 16, pz(hedef_z + 45), px(hedef_x) + 16, pz(hedef_z)], fill=ACC, outline=INK, width=2)


# ======================= ORTAK VERI (mm) =======================
H_MAK, DER, HB = 1915.0, 830.0, 1245.0
BANT0, BANT1 = 600.0, 1700.0          # robotun erisebildigi cekmece bandi
PIDE_A, LAHM_A = 108.0, 93.0

S1_MOD = [("STORE · 3 KOLON", 0.0, 1860.0), ("PRESS", 1860.0, 2530.0), ("TOPPING", 2530.0, 3415.0),
          ("OVEN", 3415.0, 4835.0), ("KESME", 4835.0, 5335.0), ("PACK", 5335.0, 6035.0),
          ("QR DOLABI", 6035.0, 7275.0)]
S2_MOD = [("STORE · DEPO (eleman)", 0.0, 1240.0), ("STORE · GÜNLÜK", 1240.0, 1860.0), ("PRESS", 1860.0, 2530.0),
          ("TOPPING", 2530.0, 3415.0), ("OVEN", 3415.0, 4835.0), ("KESME", 4835.0, 5335.0), ("PACK", 5335.0, 6035.0)]


def on_gorunus(OX, ZY, S, mod, secenek):
    def px(x):
        return OX + x * S

    def pz(z):
        return ZY - z * S

    L = mod[-1][2]
    # gövde
    d.rectangle([px(0), pz(H_MAK), px(L), pz(0)], fill=FILL, outline=LINE, width=2)
    for ad, x0, x1 in mod:
        d.line([(px(x1), pz(H_MAK)), (px(x1), pz(0))], fill=LINE, width=2)
        txt((px(x0) + px(x1)) / 2, pz(260.0), ad, f9, INK, "mm")
        olcu_h(px(x0), px(x1), pz(0) + 42, ("%g" % (x1 - x0)).replace(".", ","))
    d.line([(px(0) - 60, pz(0)), (px(L) + 60, pz(0))], fill=INK, width=3)

    # cekmece kolonlari
    if secenek == 1:
        kolonlar = [(0.0, 620.0, 6, 5), (620.0, 1240.0, 6, 5), (1240.0, 1860.0, 0, 8)]
    else:
        kolonlar = [(1240.0, 1860.0, 4, 6)]
        d.rectangle([px(0) + 3, pz(BANT1), px(1240.0) - 3, pz(BANT0)], fill=SOFT, outline=GRAY, width=1)
        txt((px(0) + px(1240.0)) / 2, pz((BANT0 + BANT1) / 2), "2 GÜNLÜK DEPO", f9, GRAY, "mm")
        txt((px(0) + px(1240.0)) / 2, pz((BANT0 + BANT1) / 2) + 26, "eleman doldurur", f8, GRAY, "mm")
    for x0, x1, n_p, n_l in kolonlar:
        z = BANT0
        for n, h, ad in ((n_p, PIDE_A, "PİDE ×%d" % n_p), (n_l, LAHM_A, "LAHMACUN ×%d" % n_l)):
            if n == 0:
                continue
            z0 = z
            for k in range(n):
                d.rectangle([px(x0 + 20), pz(z + h), px(x1 - 20), pz(z)], fill=SOGUK, outline=DOLAP, width=1)
                z += h
            txt((px(x0) + px(x1)) / 2, (pz(z0) + pz(z)) / 2, ad, f8, DOLAP, "mm")

    # firin + tabla
    fr = [m for m in mod if m[0] == "OVEN"][0]
    d.rectangle([px(fr[1] + 30), pz(HB + 320.0), px(fr[2] - 30), pz(HB - 300.0)], fill=HAVA, outline=LINE, width=1)
    d.line([(px(fr[1] + 30), pz(HB)), (px(fr[2] - 30), pz(HB))], fill=RED, width=3)
    pr = [m for m in mod if m[0] == "PRESS"][0]
    d.line([(px(pr[1] + 40), pz(HB)), (px(pr[2] - 40), pz(HB))], fill=RED, width=3)
    txt((px(pr[1]) + px(pr[2])) / 2, pz(HB) - 22, "TABLA 1245", f8, RED, "mm")

    # icecek cekmeceleri (PACK altinda)
    pk = [m for m in mod if m[0] == "PACK"][0]
    z = BANT0
    for k in range(4):
        d.rectangle([px(pk[1] + 40), pz(z + 165.0), px(pk[2] - 40), pz(z)], fill=ICE, outline=DOLAP, width=1)
        z += 165.0
    txt((px(pk[1]) + px(pk[2])) / 2, (pz(BANT0) + pz(z)) / 2, "İÇECEK ×4", f8, DOLAP, "mm")

    if secenek == 1:
        # QR dolabi hatta
        qr = mod[-1]
        qx0, qz0 = qr[1] + 50.0, 1000.0
        for r in range(4):
            for c in range(3):
                d.rectangle([px(qx0 + c * 380.0), pz(qz0 + (r + 1) * 200.0), px(qx0 + (c + 1) * 380.0 - 10), pz(qz0 + r * 200.0)],
                            fill=QRC, outline=LINE, width=1)
        txt((px(qr[1]) + px(qr[2])) / 2, pz(qz0 + 900.0), "12 GÖZ · 380 × 200", f8, INK, "mm")
        olcu_v(px(qr[2]) + 40, pz(qz0 + 800.0), pz(qz0), "800")
        # ray
        d.rectangle([px(200.0), pz(2360.0), px(L - 200.0), pz(2300.0)], fill=ACC, outline=INK, width=2)
        txt(px(L / 2), pz(2440.0), "HAVADAN RAY · STROK 4400", f11, ACC, "mm")
        cx = 2100.0
        d.rectangle([px(cx - 140.0), pz(2300.0), px(cx + 140.0), pz(2200.0)], fill=SOFT, outline=INK, width=2)
        d.rectangle([px(cx - 45.0), pz(2200.0), px(cx + 45.0), pz(1400.0)], fill=SOFT, outline=INK, width=2)
        txt(px(cx) + 58, pz(1800.0), "SARKITMA 900", f8, GRAY, "lm")
        d.ellipse([px(cx) - 26, pz(1400.0) - 26, px(cx) + 26, pz(1400.0) + 26], fill=ACC, outline=INK, width=2)
        kol(px, pz, S, cx, 1400.0, cx - 700.0, 1150.0)
        dcircle(px(cx), pz(1400.0), 922 * S, ERIS, 2)
        olcu_v(px(0) - 90, pz(2300.0), pz(0), "2300", yon="l")
        olcu_v(px(0) - 190, pz(1400.0), pz(0), "1400 OMUZ", yon="l")
        ok(px(cx + 300.0), pz(2330.0), px(L - 260.0), pz(2330.0), INK, 3)
        ok(px(cx - 300.0), pz(2330.0), px(260.0), pz(2330.0), INK, 3)
    else:
        # iki sabit robot
        for cx, hedef, ad in ((1860.0, (1550.0, 1150.0), "ROBOT 1 · FR5"), (5685.0, (5685.0, 1245.0), "ROBOT 2 · FR5")):
            d.rectangle([px(cx - 60.0), pz(1460.0), px(cx + 60.0), pz(1340.0)], fill=SOFT, outline=INK, width=2)
            d.ellipse([px(cx) - 26, pz(1400.0) - 26, px(cx) + 26, pz(1400.0) + 26], fill=ACC, outline=INK, width=2)
            kol(px, pz, S, cx, 1400.0, hedef[0], hedef[1])
            dcircle(px(cx), pz(1400.0), 922 * S, ERIS, 2)
            txt(px(cx), pz(1960.0), ad, f11, ACC, "mm")
        olcu_v(px(0) - 90, pz(1400.0), pz(0), "1400 OMUZ", yon="l")

    olcu_v(px(L) + 120, pz(H_MAK), pz(0), "1915")
    olcu_v(px(L) + 240, pz(BANT1), pz(BANT0), "BANT 1100")
    olcu_v(px(L) + 360, pz(BANT0), pz(0), "600")


def ust_gorunus(OX, OY, S, mod, secenek):
    def px(x):
        return OX + x * S

    def py(y):
        return OY - y * S

    L = mod[-1][2]
    d.rectangle([px(0), py(DER), px(L), py(0)], fill=FILL, outline=LINE, width=2)
    for ad, x0, x1 in mod:
        d.line([(px(x1), py(DER)), (px(x1), py(0))], fill=LINE, width=1)
        txt((px(x0) + px(x1)) / 2, (py(DER) + py(0)) / 2, ad.split(" · ")[0], f8, INK, "mm")
    olcu_v(px(L) + 40, py(DER), py(0), "830")
    # koridor
    dline((px(0), py(-800.0)), (px(L), py(-800.0)), GRAY, 1)
    olcu_v(px(0) - 60, py(0), py(-800.0), "800", yon="l")
    txt(px(L / 2), py(-400.0), "ROBOT KORİDORU", f9, GRAY, "mm")
    if secenek == 1:
        d.rectangle([px(200.0), py(-270.0), px(L - 200.0), py(-330.0)], fill=ACC, outline=INK, width=1)
        txt(px(L / 2), py(-180.0), "HAVADAN RAY (üstte)", f8, ACC, "mm")
        d.ellipse([px(2100.0) - 20, py(-300.0) - 20, px(2100.0) + 20, py(-300.0) + 20], fill=ACC, outline=INK, width=2)
        txt(px(2100.0), py(-560.0), "ROBOT", f9, ACC, "mm")
        qr = mod[-1]
        ok(px((qr[1] + qr[2]) / 2), py(DER + 620.0), px((qr[1] + qr[2]) / 2), py(DER + 120.0), INK, 3)
        txt(px((qr[1] + qr[2]) / 2), py(DER + 700.0), "MÜŞTERİ", f9, INK, "mm")
    else:
        for cx, ad in ((1860.0, "ROBOT 1"), (5685.0, "ROBOT 2")):
            d.ellipse([px(cx) - 20, py(-400.0) - 20, px(cx) + 20, py(-400.0) + 20], fill=ACC, outline=INK, width=2)
            txt(px(cx), py(-620.0), ad, f9, ACC, "mm")
        d.rectangle([px(5115.0), py(-920.0), px(6255.0), py(-1370.0)], fill=QRC, outline=LINE, width=2)
        for c in range(1, 3):
            d.line([(px(5115.0 + c * 380.0), py(-1370.0)), (px(5115.0 + c * 380.0), py(-920.0))], fill=LINE, width=1)
        txt(px(5685.0), py(-1145.0), "QR DOLABI · 12 GÖZ", f9, INK, "mm")
        olcu_h(px(5115.0), px(6255.0), py(-1450.0), "1140")
        ok(px(5685.0), py(-1880.0), px(5685.0), py(-1450.0), INK, 3)
        txt(px(5685.0), py(-1960.0), "MÜŞTERİ", f9, INK, "mm")
        olcu_v(px(5115.0) - 60, py(-920.0), py(-400.0), "520", yon="l")


# ======================= SAYFA =======================
txt(210, 92, "AUTOKITCH · ROBOT YERLEŞİMİ v5 · İKİ SEÇENEK", f34, INK)
txt(210, 152, "ön görünüş + üst görünüş  ·  ölçüler mm  ·  16 Eylül 2026", f13, GRAY)

SA = 0.34
txt(250, 250, "SEÇENEK 1  ·  TEK ROBOT + HAVADAN RAY", f20, ACC)
on_gorunus(420, 1320, SA, S1_MOD, 1)
ust_gorunus(420, 2320, SA, S1_MOD, 1)

txt(2900, 250, "SEÇENEK 2  ·  İKİ SABİT ROBOT (gövdeye bağlı)", f20, ACC)
on_gorunus(3070, 1320, SA, S2_MOD, 2)
ust_gorunus(3070, 2320, SA, S2_MOD, 2)

# QR detay (secenek 2 · karsi duvar)
QX, QZ = 3070.0, 3230.0
txt(QX, QZ - 900 * SA - 60, "SEÇENEK 2 · KARŞI DUVAR (QR DOLABI) ÖN GÖRÜNÜŞ", f13, ACC)
for r in range(4):
    for c in range(3):
        d.rectangle([QX + c * 380.0 * SA, QZ - (r + 1) * 200.0 * SA, QX + (c + 1) * 380.0 * SA - 6, QZ - r * 200.0 * SA],
                    fill=QRC, outline=LINE, width=1)
olcu_h(QX, QX + 1140.0 * SA, QZ + 40, "1140")
olcu_v(QX - 40, QZ - 800.0 * SA, QZ, "800", yon="l")
txt(QX + 1140.0 * SA + 60, QZ - 400.0 * SA, "12 GÖZ · göz 380 × 200  ·  kutu yatay", f9, INK, "lm")

# ======================= LEJANT =======================
LX, LY = 250, 3330
for i, (fl, oc, ad) in enumerate(((SOGUK, DOLAP, "hamur çekmecesi"), (ICE, DOLAP, "içecek çekmecesi"),
                                  (QRC, LINE, "QR teslim gözü"), (HAVA, LINE, "fırın"),
                                  (SOFT, GRAY, "depo / kaide / araba"), (FILL, LINE, "istasyon modülü"))):
    xx = LX + i * 420
    d.rectangle([xx, LY, xx + 42, LY + 30], fill=fl, outline=oc, width=2)
    txt(xx + 56, LY + 15, ad, f9, INK, "lm")
d.ellipse([LX + 2530, LY + 2, LX + 32 + 2530, LY + 32], fill=ACC, outline=INK, width=2)
txt(LX + 2578, LY + 16, "robot omuz noktası", f9, INK, "lm")
dcircle(LX + 3060, LY + 16, 16, ERIS, 2, 18)
txt(LX + 3100, LY + 16, "robot erişim çemberi (922)", f9, INK, "lm")
txt(LX + 3560, LY + 16, "GÜNLÜK ÇEKMECE: 4 PİDE (80) + 6 LAHMACUN (210)  ·  BANT 600–1700", f9, GRAY, "lm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("OK ->", OUT, im.size)
