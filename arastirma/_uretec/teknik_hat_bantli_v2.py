# -*- coding: utf-8 -*-
"""AUTOKITCH - BANTLI HAT TEKNIK RESIM v2 (13 Eyl 2026): UST GORUNUS (bant kotu plan kesiti) + A-A FIRIN KESITI + B-B TOPPING KESITI.
Olculer mm. Kemal: "sadece ust ve yan gorunus, detayli, anlasilir; firini 830'a sigdir".

v1'den FARKI: PS536 (1010 derin) yerine OZEL ELEKTRIKLI KONVEYOR FIRIN, 4 urun haznede:
  hazne 1400 · tunel 2 x 300 · tek bant 450 · modul 2100 x 830 x govde 620 (y 1000..1620)
  derinlik butcesi (z +40 .. -790 = 830): on duvar 60 | hazne ici 500 | arka plenum (fan + rezistans) 210 | arka duvar 60
  bant merkezi z -270 (topping bandi 400: -470..-70 · firin bandi 450: -495..-45 · kesme plakasi 450)
  hat: PRESS 700 · TOPPING-BANT 1000 · OVEN 2100 · KESME 600 · PACK 700 = 5100
KAYNAK / DAYANAK: TurboChef HhC 1618 406 bant 805 derin (830'a sigdigi kanit) · PS536 508 bant 1010 derin, tunel 2 x 305
  · PS640/670 tunel 2 x 457 · yalitim tasyunu 50 (OVEN v5 ile ayni) · kaset 140 x 240 x 680 (KAP_DETAY) · cekmece HH 88, alin 33.
VARSAYIM (etiketli): plenum/fan/rezistans yerlesimi sematik, guc ~18 kW (OKF1500 10 kW / 0,34 m2 oraniyla), bant kotu 1300.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BANTLI_v2_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3800, 3050
S, S2 = 0.62, 0.80
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, PUC = (14, 120, 90), (190, 190, 196), (255, 240, 200)
BANT, FIRIN, KAS, HEAD, HAVA = (0, 120, 160), (200, 90, 30), (236, 240, 246), (222, 228, 240), (255, 225, 200)
AGZ, YUN = (253, 244, 243), (250, 236, 210)


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


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=12):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def yalitim(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=YUN, outline=GRAY, width=1)
    tarali(x0 + 1, y0 + 1, x1 - 1, y1 - 1, (215, 190, 150), 9)


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


def ok(x0, y0, x1, y1, c, w=3):
    d.line([(x0, y0), (x1, y1)], fill=c, width=w)
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 14 * math.cos(a + s_), y1 - 14 * math.sin(a + s_))], fill=c, width=w)


def kesit_isareti(x, y0, y1, harf, yon=1):
    d.line([(x, y0), (x, y1)], fill=ACC, width=3)
    for yy, sg in ((y0, -1), (y1, 1)):
        d.line([(x, yy), (x + 22 * yon, yy)], fill=ACC, width=3)
        txt(x + (30 if yon > 0 else -30), yy + sg * 4, harf, f13, ACC, "mm")


# ======================= VERI =======================
H = 1970.0
ISTASYON = [("PRESS v7", 700.0), ("TOPPING-BANT v2", 1000.0), ("OVEN v7 · özel konveyör", 2100.0), ("KESME v1", 600.0), ("PACK v5", 700.0)]
X0, _x = {}, 0.0
for ad, w in ISTASYON:
    X0[ad.split()[0].split("-")[0]] = _x
    _x += w
HAT = _x                                                # 5100
Y_BANT = 1300.0
ZC = -270.0                                             # bant merkezi
TB0, TB1 = ZC - 200.0, ZC + 200.0                       # topping bandi 400: -470..-70
FB0, FB1 = ZC - 225.0, ZC + 225.0                       # firin bandi 450: -495..-45
CH0, CH1 = -520.0, -20.0                                # hazne ici 500
PL0, PL1 = -730.0, -520.0                               # arka plenum 210
ON_D, ARKA_D = 60.0, 60.0                               # on / arka duvar (sac 1,5 + tasyunu 50 + sac 1 + bosluk)
HAZNE, TUNEL, DUVAR_X = 1400.0, 300.0, 50.0
OX0 = X0["OVEN"]
TUN_IN0 = OX0 + DUVAR_X                                 # 1750
HZ0 = TUN_IN0 + TUNEL                                   # 2050
HZ1 = HZ0 + HAZNE                                       # 3450
TUN_OUT1 = HZ1 + TUNEL                                  # 3750
FY0, FY1 = 1000.0, 1620.0                               # firin govdesi
ISO = 50.0
IC_Y0, IC_Y1 = FY0 + ISO, FY1 - ISO                     # ic 1050..1570
KW, KH = 140.0, 240.0
KX = [X0["TOPPING"] + 40.0 + i * 160.0 for i in range(6)]
KZ0, KZ1 = -695.5, -15.5
URUN = ("KAŞAR", "SUCUK", "HARÇ", "HARÇ", "KIYMA", "KUŞBAŞI")
HB0, HB1 = ZC - 150.0, ZC + 150.0                       # dozaj basligi 300
Y_HEAD0, Y_HEAD1 = Y_BANT + 20.0, Y_BANT + 150.0
Y_DOZ0, Y_DOZ1 = Y_HEAD1, Y_HEAD1 + KH
Y_DEP0, Y_DEP1 = 1720.0, 1960.0
CELL0, BIND, FUGA, HH = 182.5, 15.0, 3.0, 88.0
PITCH = 350.0
assert ON_D + (CH1 - CH0) + (PL1 - PL0) + ARKA_D == 830.0
assert FB0 >= CH0 + 25 and FB1 <= CH1 - 25, "bant hazneye sigmiyor"

# ======================= YERLESIM =======================
OX = 300.0
PY_TOP = 330.0
SEC_TOP = PY_TOP + 830.0 * S + 330.0
FY2 = SEC_TOP + H * S2
SXA = OX + 120.0
SXB = SXA + 830.0 * S2 + 520.0


def fx(x):
    return OX + x * S


def py(z):
    return PY_TOP + (z + 790.0) * S


def fy2(y):
    return FY2 - y * S2


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  BANTLI HAT  ·  TEKNİK RESİM  v2", f38, INK)
txt(OX, 138, "üst görünüş (bant kotu plan kesiti) + A-A fırın kesiti + B-B topping kesiti  ·  4 ürünlük özel konveyör fırın 830 derinliğe sığdırıldı  ·  ölçüler mm  ·  13 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= UST GORUNUS =======================
txt(OX, PY_TOP - 110, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ · bant kotu 1300", f16, ACC)
txt(fx(350.0), py(-790.0) - 34, "ARKA", f9, GRAY, "mm")
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    d.rectangle([fx(x0), py(-790.0), fx(x0 + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0 + w / 2), py(40.0) + 30, "%s  ·  %s" % (ad, sayi(w)), f9, INK, "mm")
# --- PRESS
d.rectangle([fx(X0["PRESS"] + 29), py(-788.0), fx(X0["PRESS"] + 669), py(12.0)], fill=BG, outline=INK, width=2)
txt(fx(X0["PRESS"] + 349), py(-430.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X0["PRESS"] + 349), py(-400.0), "640 × 800 · tabla 1300", f7, GRAY, "mm")
txt(fx(X0["PRESS"] + 349), py(-100.0), "pres → bant geçişi", f7, RED, "mm")
# --- TOPPING: bant, kasetler, basliklar
d.rectangle([fx(X0["TOPPING"] + 10), py(TB0), fx(X0["OVEN"] + 20), py(TB1)], fill=(232, 244, 250), outline=BANT, width=2)
for i, kx in enumerate(KX):
    d.rectangle([fx(kx), py(KZ0), fx(kx + KW), py(KZ1)], outline=INK, width=2)
    d.rectangle([fx(kx - 6), py(-797.5), fx(kx + KW + 6), py(KZ0)], fill=(255, 230, 230), outline=RED, width=1)
    drect(fx(kx - 10), py(HB0), fx(kx + KW + 10), py(HB1), BANT, 2)
    d.rectangle([fx(kx + 47.5), py(-80.0), fx(kx + 92.5), py(-30.0)], fill=RED)
    txt(fx(kx + KW / 2), py(-660.0), URUN[i], f7, INK, "mm")
    txt(fx(kx + KW / 2), py(-600.0), "kaset", f7, GRAY, "mm")
ok(fx(X0["TOPPING"] + 60), py(ZC), fx(X0["TOPPING"] + 200), py(ZC), BANT, 3)
txt(fx(X0["TOPPING"] + 760), py(-525.0), "TOPPING BANDI 400 · adımlı", f8, BANT, "mm")
txt(fx(X0["TOPPING"] + 90), py(-905.0), "kaset motor paketi 102 · z −797,5 (830'a sığmıyor)", f7, RED, "mm")
olcu_h(fx(KX[0]), fx(KX[1]), py(-838.0), "160", f8, INK)
olcu_h(fx(KX[5]), fx(KX[5] + KW), py(-838.0), "140", f7, GRAY)
olcu_v(fx(X0["TOPPING"]) - 40, py(KZ0), py(KZ1), "680", f8, INK, "l")
txt(fx(KX[2] + KW / 2), py(-105.0), "ağız 45 × 50", f7, RED, "mm")
# --- OVEN plan
# duvarlar (yalitimli)
yalitim(fx(OX0), py(-790.0), fx(OX0 + 2100.0), py(-730.0))                          # arka duvar
yalitim(fx(OX0), py(-20.0), fx(OX0 + 2100.0), py(40.0))                             # on duvar
yalitim(fx(OX0), py(-730.0), fx(OX0 + DUVAR_X), py(-20.0))                          # sol uc duvari (bant gecis yarigi haric)
yalitim(fx(OX0 + 2100.0 - DUVAR_X), py(-730.0), fx(OX0 + 2100.0), py(-20.0))       # sag uc duvari
# plenum
d.rectangle([fx(OX0 + DUVAR_X), py(PL0), fx(OX0 + 2100.0 - DUVAR_X), py(PL1)], fill=HAVA, outline=FIRIN, width=2)
for cx_ in (HZ0 + 350.0, HZ0 + 1050.0):
    d.ellipse([fx(cx_ - 100), py(-625.0 - 100), fx(cx_ + 100), py(-625.0 + 100)], outline=FIRIN, width=3)
    txt(fx(cx_), py(-625.0) - 10, "FAN", f8, FIRIN, "mm")
    txt(fx(cx_), py(-625.0) + 12, "Ø200", f7, FIRIN, "mm")
for cx_ in (HZ0 + 700.0,):
    for zz in (-560.0, -610.0, -660.0):
        d.line([(fx(cx_ - 250), py(zz)), (fx(cx_ + 250), py(zz))], fill=RED, width=3)
    txt(fx(cx_), py(-700.0), "REZİSTANS ≈ 18 kW (tahmin)", f7, RED, "mm")
txt(fx(HZ0 + 1200.0), py(-700.0), "ARKA PLENUM 210", f8, FIRIN, "mm")
# hazne ici + tuneller
d.rectangle([fx(OX0 + DUVAR_X), py(CH0), fx(OX0 + 2100.0 - DUVAR_X), py(CH1)], fill=BG, outline=FIRIN, width=2)
drect(fx(HZ0), py(CH0) + 2, fx(HZ1), py(CH1) - 2, FIRIN, 3)
# yarik: uc duvarlarinda bant gecisi
for xa, xb in ((OX0, OX0 + DUVAR_X), (OX0 + 2100.0 - DUVAR_X, OX0 + 2100.0)):
    d.rectangle([fx(xa), py(FB0 - 20), fx(xb), py(FB1 + 20)], fill=BG, outline=FIRIN, width=1)
# bant
d.rectangle([fx(OX0 + 20.0), py(FB0), fx(OX0 + 2080.0), py(FB1)], fill=(255, 236, 220), outline=FIRIN, width=2)
for xx in range(int(OX0 + 40), int(OX0 + 2080), 60):
    d.line([(fx(xx), py(FB0)), (fx(xx), py(FB1))], fill=(235, 200, 170), width=1)
# ust hava parmaklari (bantin ustunde, kesikli): hazne boyunca 7 sira
for k in range(7):
    xa = HZ0 + 60.0 + k * 200.0
    drect(fx(xa), py(CH0 + 20), fx(xa + 80.0), py(CH1 - 20), FIRIN, 2)
txt(fx(HZ0 + 700.0), py(-468.0), "ÜST HAVA PARMAKLARI × 7 (kesikli)  ·  altta × 7", f7, FIRIN, "mm")
# urunler: haznede 4 adet
for k in range(4):
    cx_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(cx_ - 150), py(ZC - 150), fx(cx_ + 150), py(ZC + 150)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
    txt(fx(cx_), py(ZC), "Ø300", f7, (160, 120, 50), "mm")
ok(fx(OX0 + 60.0), py(ZC + 190), fx(OX0 + 200.0), py(ZC + 190), FIRIN, 3)
txt(fx(HZ0 - 150.0), py(-140.0), "TÜNEL", f7, FIRIN, "mm")
txt(fx(HZ1 + 150.0), py(-140.0), "TÜNEL", f7, FIRIN, "mm")
txt(fx(HZ0 + 700.0), py(-140.0), "PİŞİRME HAZNESİ 1400  ·  aynı anda 4 ürün (adım 350)  ·  bant 450 sürekli, 5,8 mm/s (pide 240 s)", f8, FIRIN, "mm")
d.rectangle([fx(OX0 + 2100.0 - DUVAR_X - 120), py(-720.0), fx(OX0 + 2100.0 - DUVAR_X - 20), py(-640.0)], fill=BG, outline=INK, width=2)
txt(fx(OX0 + 2100.0 - DUVAR_X - 70), py(-680.0), "TAHRİK", f7, INK, "mm")
# olculer: x
olcu_h(fx(OX0), fx(TUN_IN0), py(-790.0) - 26, "50", f7, GRAY)
olcu_h(fx(TUN_IN0), fx(HZ0), py(-790.0) - 26, "300", f8, INK)
olcu_h(fx(HZ0), fx(HZ1), py(-790.0) - 26, "HAZNE 1400", f9, FIRIN)
olcu_h(fx(HZ1), fx(TUN_OUT1), py(-790.0) - 26, "300", f8, INK)
olcu_h(fx(TUN_OUT1), fx(OX0 + 2100.0), py(-790.0) - 26, "50", f7, GRAY)
# olculer: z (derinlik butcesi) — sol tunel bolgesinde
xz = fx(TUN_IN0 + 150.0)
olcu_v(xz, py(-790.0), py(-730.0), "60", f7, INK, "r")
olcu_v(xz, py(-730.0), py(-520.0), "210", f7, INK, "r")
olcu_v(xz, py(-520.0), py(-20.0), "iç 500", f8, INK, "r")
olcu_v(xz, py(-20.0), py(40.0), "60", f7, INK, "r")
olcu_v(fx(TUN_OUT1 - 120.0), py(FB0), py(FB1), "bant 450", f8, FIRIN, "l")
# --- KESME plan
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 20), py(FB0), fx(kx0 + 580), py(FB1)], fill=(232, 244, 250), outline=BANT, width=2)
d.ellipse([fx(kx0 + 140), py(ZC - 160), fx(kx0 + 460), py(ZC + 160)], outline=INK, width=2)
for k in range(4):
    a = k * math.pi / 4
    d.line([(fx(kx0 + 300) - 160 * S * math.cos(a), py(ZC) - 160 * S * math.sin(a)),
            (fx(kx0 + 300) + 160 * S * math.cos(a), py(ZC) + 160 * S * math.sin(a))], fill=INK, width=1)
txt(fx(kx0 + 300), py(-560.0), "KESİCİ Ø320 · 8 bıçak", f7, INK, "mm")
txt(fx(kx0 + 300), py(-600.0), "KESME PLAKASI 560 × 450", f7, BANT, "mm")
d.rectangle([fx(kx0 + 40), py(ZC - 60), fx(kx0 + 100), py(ZC + 60)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 70), py(-120.0), "İTİCİ", f7, INK, "mm")
d.ellipse([fx(kx0 + 20) - 6, py(-620.0) - 6, fx(kx0 + 20) + 6, py(-620.0) + 6], fill=RED)
txt(fx(kx0 + 60), py(-660.0), "SPREY", f7, RED, "mm")
ok(fx(kx0 + 110), py(ZC), fx(kx0 + 130), py(ZC), INK, 2)
# --- PACK plan
pk0 = X0["PACK"]
d.rectangle([fx(pk0 + 50), py(ZC - 160), fx(pk0 + 370), py(ZC + 160)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 210), py(ZC) - 12, "KUTU 320 × 320", f8, INK, "mm")
txt(fx(pk0 + 210), py(ZC) + 12, "plaka kotunda", f7, GRAY, "mm")
drect(fx(pk0 + 150), py(-785.5), fx(pk0 + 550), py(-25.5), GRAY, 1)
txt(fx(pk0 + 350), py(-700.0), "BLANK 400 × 760 · şarjör altta", f7, GRAY, "mm")
ok(fx(kx0 + 540), py(ZC), fx(pk0 + 50), py(ZC), INK, 2)
# genel olculer + kesit isaretleri
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    olcu_h(fx(x0), fx(x0 + w), py(40.0) + 60, sayi(w), f8, GRAY)
olcu_v(fx(0) - 44, py(-790.0), py(40.0), "830", f11, INK, "l")
txt(fx(HAT / 2), py(40.0) + 150, "ÖN  ·  robot tarafı  ·  kaset değişimi önden  ·  STORE bant altında (kesitlerde)", f9, GRAY, "mm")
kesit_isareti(fx(HZ0 + 175.0), py(-790.0) - 70, py(40.0) + 20, "A", 1)
kesit_isareti(fx(KX[2] + KW / 2), py(-790.0) - 70, py(40.0) + 20, "B", -1)


# ======================= KESITLER =======================
def kabin_kesit(sx, baslik, alt):
    def sz(z):
        return sx + (z + 790.0) * S2
    txt(sx, SEC_TOP - 110, baslik, f16, ACC)
    txt(sx, SEC_TOP - 72, alt, f9, GRAY)
    d.rectangle([sz(-790), fy2(H), sz(40), fy2(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([sz(-790), fy2(120), sz(40), fy2(0)], fill=SOFT, outline=LINE, width=2)
    return sz


def store_kesit(sz, top, n, ad):
    d.rectangle([sz(-788.5), fy2(top), sz(-728.5), fy2(121.5)], fill=PUC, outline=GRAY, width=1)      # arka PU 60
    d.rectangle([sz(-727.5), fy2(181.5), sz(0.0), fy2(121.5)], fill=PUC, outline=GRAY, width=1)         # taban PU
    d.rectangle([sz(-727.5), fy2(top + 60.0), sz(0.0), fy2(top)], fill=PUC, outline=GRAY, width=1)      # tavan PU
    d.rectangle([sz(-727.5), fy2(top), sz(-680.0), fy2(CELL0)], fill=(250, 250, 251), outline=GRAY, width=1)
    y0 = CELL0
    for i in range(n):
        d.rectangle([sz(-680.0), fy2(y0 + HH), sz(0.0), fy2(y0)], fill=BG, outline=DOLAP, width=1)
        d.rectangle([sz(0.0), fy2(y0 + HH + BIND), sz(40.0), fy2(y0 - BIND)], fill=BG, outline=DOLAP, width=1)
        y0 += HH + 2 * BIND + FUGA
    txt(sz(-340), fy2((CELL0 + top) / 2) - 12, "ÇEKMECE 680 × %d" % n, f9, INK, "mm")
    txt(sz(-340), fy2((CELL0 + top) / 2) + 14, ad, f7, DOLAP, "mm")


# ---- A-A: FIRIN
sz = kabin_kesit(SXA, "A-A  ·  FIRIN KESİTİ", "1. ürün ekseninden (hazne girişi + 175) · K4 kolonu üstü · özel elektrikli konveyör fırın")
store_kesit(sz, 900.0, 5, "LAHMACUN × 5 · +3 °C")
d.rectangle([sz(-790), fy2(FY0), sz(40), fy2(960.0)], fill=BG, outline=GRAY, width=1)
txt(sz(-375), fy2(980.0), "havalandırma boşluğu 40", f7, GRAY, "mm")
# govde yalitimi
yalitim(sz(-790), fy2(FY1), sz(40), fy2(FY1 - ISO))                       # ust
yalitim(sz(-790), fy2(FY0 + ISO), sz(40), fy2(FY0))                       # alt
yalitim(sz(-790), fy2(FY1), sz(-730), fy2(FY0))                           # arka duvar 60
yalitim(sz(-20), fy2(FY1), sz(40), fy2(FY0))                              # on duvar 60
d.rectangle([sz(-790), fy2(FY1), sz(40), fy2(FY0)], outline=INK, width=3)
# plenum
d.rectangle([sz(PL0), fy2(IC_Y1), sz(PL1), fy2(IC_Y0)], fill=HAVA, outline=FIRIN, width=2)
d.ellipse([sz(-625 - 100), fy2(Y_BANT + 100), sz(-625 + 100), fy2(Y_BANT - 100)], outline=FIRIN, width=3)
txt(sz(-625), fy2(Y_BANT) - 10, "FAN", f8, FIRIN, "mm"); txt(sz(-625), fy2(Y_BANT) + 12, "Ø200", f7, FIRIN, "mm")
for yy in (1120.0, 1500.0):
    d.line([(sz(-700), fy2(yy)), (sz(-550), fy2(yy))], fill=RED, width=4)
txt(sz(-625), fy2(1080.0), "rezistans", f7, RED, "mm"); txt(sz(-625), fy2(1540.0), "rezistans", f7, RED, "mm")
# hazne ici: ust/alt plenum + parmaklar + bant + urun
d.rectangle([sz(CH0), fy2(IC_Y1), sz(CH1), fy2(IC_Y0)], fill=BG, outline=FIRIN, width=2)
d.rectangle([sz(CH0), fy2(IC_Y1), sz(CH1), fy2(1420.0)], fill=HAVA, outline=FIRIN, width=1)     # ust plenum
d.rectangle([sz(CH0), fy2(1230.0), sz(CH1), fy2(IC_Y0)], fill=HAVA, outline=FIRIN, width=1)     # alt plenum
for zz in range(-470, -60, 90):
    d.rectangle([sz(zz), fy2(1420.0), sz(zz + 50), fy2(1370.0)], fill=BG, outline=FIRIN, width=1)   # ust parmak
    d.rectangle([sz(zz), fy2(1260.0), sz(zz + 50), fy2(1230.0)], fill=BG, outline=FIRIN, width=1)   # alt parmak
    for k in range(3):
        d.line([(sz(zz + 10 + k * 15), fy2(1370.0)), (sz(zz + 10 + k * 15), fy2(1345.0))], fill=FIRIN, width=1)
        d.line([(sz(zz + 10 + k * 15), fy2(1260.0)), (sz(zz + 10 + k * 15), fy2(1275.0))], fill=FIRIN, width=1)
txt(sz(ZC), fy2(1495.0), "ÜST PLENUM · hava parmakları", f7, FIRIN, "mm")
txt(sz(ZC), fy2(1140.0), "ALT PLENUM · hava parmakları", f7, FIRIN, "mm")
d.rectangle([sz(FB0), fy2(Y_BANT), sz(FB1), fy2(Y_BANT - 12.0)], fill=(255, 236, 220), outline=FIRIN, width=2)
txt(sz(ZC), fy2(Y_BANT - 30.0), "BANT 450 · tel örgü, sökülür", f7, FIRIN, "mm")
d.rectangle([sz(ZC - 150), fy2(Y_BANT + 20.0), sz(ZC + 150), fy2(Y_BANT)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
txt(sz(ZC), fy2(Y_BANT + 40.0), "ürün Ø300", f7, (160, 120, 50), "mm")
# on duvar: gozetleme cami
d.rectangle([sz(-20), fy2(1400.0), sz(40), fy2(1250.0)], fill=(225, 240, 255), outline=ACC, width=1)
txt(sz(-40), fy2(1460.0), "gözetleme camı · opsiyon", f7, ACC, "rm")
# egzoz
d.rectangle([sz(-788.5), fy2(1968.0), sz(38.5), fy2(1660.0)], fill=BG, outline=LINE, width=2)
d.rectangle([sz(-330), fy2(1660.0), sz(-210), fy2(FY1)], fill=SOFT, outline=LINE, width=1)
txt(sz(-375), fy2(1830.0), "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre", f8, INK, "mm")
txt(sz(-270), fy2(1640.0), "kanal", f7, GRAY, "mm")
# olculer
olcu_h(sz(-790), sz(40), fy2(0) + 44, "830", f11, INK)
olcu_h(sz(-790), sz(-730), fy2(0) + 82, "60", f7, INK)
olcu_h(sz(-730), sz(-520), fy2(0) + 82, "plenum 210", f8, INK)
olcu_h(sz(-520), sz(-20), fy2(0) + 82, "hazne içi 500", f8, INK)
olcu_h(sz(-20), sz(40), fy2(0) + 82, "60", f7, INK)
olcu_h(sz(FB0), sz(FB1), fy2(0) + 118, "bant 450", f8, FIRIN)
for yy, ad_ in ((120.0, "120"), (900.0, "900"), (FY0, "1000"), (Y_BANT, "1300 bant"), (FY1, "1620"), (1660.0, "1660"), (H, "1970")):
    d.line([(sz(40) + 6, fy2(yy)), (sz(40) + 24, fy2(yy))], fill=INK, width=2)
    txt(sz(40) + 30, fy2(yy), ad_, f8, INK, "lm")
olcu_v(sz(-790) - 44, fy2(FY1), fy2(FY0), "gövde 620", f8, INK, "l")
olcu_v(sz(-790) - 44, fy2(IC_Y1), fy2(IC_Y0), "iç 520", f7, GRAY, "l")
txt(sz(-375), fy2(1590.0), "taşyünü 50 her yüzde", f7, GRAY, "mm")

# ---- B-B: TOPPING
sz = kabin_kesit(SXB, "B-B  ·  TOPPING KESİTİ", "3. kaset ekseninden · K2 kolonu üstü")
store_kesit(sz, 1140.0, 7, "TAZE PİDE 6 + PAKET 1 · +3 °C")
d.rectangle([sz(TB0), fy2(Y_BANT), sz(TB1), fy2(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(sz(TB0), fy2(Y_BANT)), (sz(TB1), fy2(Y_BANT))], fill=BANT, width=5)
txt(sz(ZC), fy2(Y_BANT - 50.0), "BANT 400", f7, BANT, "mm")
d.rectangle([sz(ZC - 150), fy2(Y_BANT + 20.0), sz(ZC + 150), fy2(Y_BANT)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
d.rectangle([sz(HB0), fy2(Y_HEAD1), sz(HB1), fy2(Y_HEAD0)], fill=HEAD, outline=BANT, width=2)
txt(sz(ZC), fy2((Y_HEAD0 + Y_HEAD1) / 2), "DOZAJ BAŞLIĞI 300", f7, BANT, "mm")
d.rectangle([sz(KZ0), fy2(Y_DOZ1), sz(KZ1), fy2(Y_DOZ0)], fill=KAS, outline=INK, width=2)
d.rectangle([sz(-797.5), fy2(Y_DOZ1 - 20), sz(KZ0), fy2(Y_DOZ0 + 20)], fill=(255, 230, 230), outline=RED, width=1)
txt(sz(-355), fy2((Y_DOZ0 + Y_DOZ1) / 2) - 12, "DOZAJ KASETİ 140 × 240 × 680", f8, INK, "mm")
txt(sz(-355), fy2((Y_DOZ0 + Y_DOZ1) / 2) + 12, "helezon Ø70 · ağız 45 × 50 önde", f7, GRAY, "mm")
d.rectangle([sz(-80.0), fy2(Y_DOZ0), sz(-30.0), fy2(Y_DOZ0 - 50.0)], fill=RED)
dline((sz(-55.0), fy2(Y_DOZ0 - 50.0)), (sz(HB1), fy2(Y_HEAD1)), RED, 2)
txt(sz(-140.0), fy2(1425.0), "oluk", f7, RED, "mm")
d.line([(sz(KZ0 - 10), fy2(Y_DEP0 - 10)), (sz(KZ1 + 10), fy2(Y_DEP0 - 10))], fill=LINE, width=3)
d.rectangle([sz(KZ0), fy2(Y_DEP1), sz(KZ1), fy2(Y_DEP0)], fill=KAS, outline=INK, width=2)
txt(sz(-355), fy2((Y_DEP0 + Y_DEP1) / 2), "DEPO KASETİ · raf %s" % sayi(Y_DEP0), f8, INK, "mm")
d.rectangle([sz(0.0), fy2(1968.0), sz(40.0), fy2(Y_BANT - 110.0)], fill=SOFT, outline=LINE, width=1)
txt(sz(20), fy2(1600.0), "K", f7, GRAY, "mm")
olcu_h(sz(-790), sz(40), fy2(0) + 44, "830", f11, INK)
olcu_h(sz(TB0), sz(TB1), fy2(0) + 82, "bant 400", f8, BANT)
olcu_h(sz(-797.5), sz(KZ0), fy2(0) + 118, "102", f7, RED)
olcu_h(sz(KZ0), sz(KZ1), fy2(0) + 118, "kaset 680", f8, INK)
for yy, ad_ in ((120.0, "120"), (1140.0, "1140"), (Y_BANT, "1300 bant"), (Y_DOZ0, "1450"), (Y_DOZ1, "1690"), (Y_DEP0, "1720"), (H, "1970")):
    d.line([(sz(40) + 6, fy2(yy)), (sz(40) + 24, fy2(yy))], fill=INK, width=2)
    txt(sz(40) + 30, fy2(yy), ad_, f8, INK, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (GRAY, YUN, "taşyünü 50 yalıtım", False), (FIRIN, HAVA, "sıcak hava plenum / parmak", False),
       (FIRIN, (255, 236, 220), "fırın bandı", False), (BANT, (232, 244, 250), "topping bandı / plaka", False), (DOLAP, BG, "çekmece +3 °C", False),
       (GRAY, PUC, "PU yalıtım (STORE)", False), (RED, (255, 230, 230), "motor paketi · 830 dışı", False), (BANT, BG, "dozaj başlığı izi", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly, "HAT %s × 1970 × 830  ·  OVEN 2100 × 830 × 620 gövde  ·  hazne 1400 = 4 ürün  ·  tavan 60/saat" % sayi(HAT), f9, GRAY, "rm")

assert not os.path.exists(OUT), "v2 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s" % sayi(HAT))
