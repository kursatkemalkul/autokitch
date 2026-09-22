# -*- coding: utf-8 -*-
"""AUTOKITCH - BANTLI HAT TEKNIK RESIM v4 (13 Eyl 2026): ON GORUNUS (montaj hali) + UST GORUNUS (bant kotu plan kesiti). TUNELSIZ FIRIN.
v4: Kemal 'firinin onunde arkasinda bos alan olmasin, topping'den ciktigi gibi hazneye girsin' -> tunel 0, OVEN 2100 -> 1500, hat 4500.
Olculer mm. Kemal: "onden ve ustten gorunus, detayli, anlasilir; firini 830'a sigdir". v2 plani aynen, kesitler yerine on gorunus.

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

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BANTLI_v4_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3800, 2800
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
ISTASYON = [("PRESS v7", 700.0), ("TOPPING-BANT v2", 1000.0), ("OVEN v7 · özel konveyör", 1500.0), ("KESME v1", 600.0), ("PACK v5", 700.0)]
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
HAZNE, TUNEL, DUVAR_X = 1400.0, 0.0, 50.0
OW = 1500.0                                             # OVEN modul boyu = 50 + 1400 + 50
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
FY_TOP = 360.0
FY = FY_TOP + H * S
PY_TOP = FY + 330.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  BANTLI HAT  ·  TEKNİK RESİM  v4", f38, INK)
txt(OX, 138, "ön görünüş (montaj hâli) + üst görünüş (bant kotu plan kesiti)  ·  4 ürünlük özel konveyör fırın, tünelsiz: ürün topping bandından doğrudan hazneye  ·  830 derin  ·  ölçüler mm  ·  13 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 150, "ÖN GÖRÜNÜŞ  ·  MONTAJ HÂLİ  ·  robot tarafından", f16, ACC)
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    d.rectangle([fx(x0), fy(H), fx(x0 + w), fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([fx(x0), fy(120), fx(x0 + w), fy(0)], fill=SOFT, outline=LINE, width=2)
    txt(fx(x0 + w / 2), fy(H) - 64, ad, f13, INK, "md")
    olcu_h(fx(x0), fx(x0 + w), fy(H) - 26, sayi(w), f11, INK)
# --- STORE (alt kat): 5 kolon
XI, WO, BOL = 62.5, 620.0, 35.0
HHK = {"hamur": 88.0, "lahm": 88.0, "paket": 88.0}
ADK = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "paket": "KAŞAR + SUCUK PAKETİ"}
CAPK = {"hamur": (20, "top"), "lahm": (30, "top"), "paket": (None, "vakum")}
KOLON = [(940.0, [(6, "hamur")]), (1140.0, [(6, "hamur"), (1, "paket")]), (900.0, [(1, "paket"), (4, "lahm")]), (900.0, [(5, "lahm")]), (900.0, [(5, "lahm")])]
cx = XI
for ki, (top, gruplar) in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOL), fy(top), fx(cx), fy(CELL0 - BIND)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(cx), fy(top + 60.0), fx(cx + WO), fy(top)], fill=PUC, outline=GRAY, width=1)
    y = CELL0 - BIND
    for n, tip in gruplar:
        h = HHK[tip] + 2 * BIND
        ybas = y
        for _ in range(n):
            d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=1)
            y += h + FUGA
        cap, br = CAPK[tip]
        ikinci = ("%d %s · +3 °C" % (n * cap, br)) if cap else ("%s · +3 °C" % br)
        ym = (fy(ybas) + fy(y - FUGA)) / 2
        for k_, (ss, ff, cc) in enumerate(((("%s × %d" % (ADK[tip], n)), f8, INK), (ikinci, f7, DOLAP))):
            tw = d.textlength(ss, font=ff)
            yy = ym + (-13 if k_ == 0 else 13)
            d.rectangle([fx(cx + WO / 2) - tw / 2 - 6, yy - 11, fx(cx + WO / 2) + tw / 2 + 6, yy + 11], fill=BG, outline=DOLAP, width=1)
            txt(fx(cx + WO / 2), yy, ss, ff, cc, "mm")
    ust = y - FUGA
    if top - ust > 20:
        d.rectangle([fx(cx + 8), fy(top), fx(cx + WO - 8), fy(ust)], fill=(250, 250, 251), outline=BOSL, width=1)
        tarali(fx(cx + 8) + 1, fy(top) + 1, fx(cx + WO - 8) - 1, fy(ust) - 1)
    txt(fx(cx + WO / 2), fy(CELL0 - BIND) + 20, "K%d · tavan %s" % (ki + 1, sayi(top)), f7, GRAY, "mm")
    cx += WO + BOL
CEK = sum(n for _, g in KOLON for n, _ in g)
TEK0X, TEK1X = cx - BOL, X0["PACK"] - 30.0
d.rectangle([fx(TEK0X), fy(1140.0), fx(TEK1X), fy(120.0)], fill=SOFT, outline=LINE, width=2)
txt(fx((TEK0X + TEK1X) / 2), fy(660.0) - 24, "TEKNİK", f8, GRAY, "mm")
txt(fx((TEK0X + TEK1X) / 2), fy(660.0), "soğutma grupları", f7, GRAY, "mm")
txt(fx((TEK0X + TEK1X) / 2), fy(660.0) + 22, "fırın + hat panosu", f7, GRAY, "mm")
olcu_h(fx(XI), fx(XI + WO), fy(0) + 44, "620", f8, GRAY)
olcu_h(fx(0), fx(TEK0X), fy(0) + 80, "STORE  %s  ·  %d çekmece  ·  bant altında" % (sayi(TEK0X), CEK), f11, INK)
# --- bant hatti: TOPPING cercevesi, kesme plakasi
d.rectangle([fx(X0["TOPPING"] + 10), fy(Y_BANT), fx(OX0 + 10), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(fx(X0["TOPPING"] + 10), fy(Y_BANT)), (fx(OX0 + 10), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(X0["TOPPING"] + 250), fy(Y_BANT - 50.0), "DOZAJ BAŞLIĞI × 6 · 300 geniş", f8, BANT, "mm")
txt(fx(X0["TOPPING"] + 750), fy(Y_BANT - 50.0), "TOPPING BANDI 400 · adımlı", f8, BANT, "mm")
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 10), fy(Y_BANT), fx(kx0 + 590), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(fx(kx0 + 10), fy(Y_BANT)), (fx(kx0 + 590), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(kx0 + 300), fy(Y_BANT - 50.0), "KESME PLAKASI 560 × 450", f8, BANT, "mm")
# --- PRESS
px0 = X0["PRESS"] + 30.0
d.rectangle([fx(px0), fy(FY0 + 950.0), fx(px0 + 640.0), fy(FY0)], fill=BG, outline=INK, width=2)
txt(fx(px0 + 320), fy(FY0 + 700.0) - 12, "FERSAH PZP-400", f9, INK, "mm")
txt(fx(px0 + 320), fy(FY0 + 700.0) + 12, "640 × 950 × 800", f7, GRAY, "mm")
d.rectangle([fx(px0 + 20), fy(Y_BANT + 260.0), fx(px0 + 620), fy(Y_BANT)], fill=AGZ, outline=RED, width=3)
txt(fx(px0 + 320), fy(Y_BANT + 130.0) - 10, "PRES AĞZI", f8, RED, "mm")
txt(fx(px0 + 320), fy(Y_BANT + 130.0) + 12, "tabla %s · banda geçiş" % sayi(Y_BANT), f7, RED, "mm")
ok(fx(px0 + 620), fy(Y_BANT + 40.0), fx(X0["TOPPING"] + 40), fy(Y_BANT + 40.0), BANT, 3)
# --- TOPPING: basliklar, dozaj ve depo kasetleri
for i, kx in enumerate(KX):
    d.rectangle([fx(kx), fy(Y_HEAD1), fx(kx + KW), fy(Y_HEAD0)], fill=HEAD, outline=BANT, width=2)
    d.rectangle([fx(kx), fy(Y_DOZ1), fx(kx + KW), fy(Y_DOZ0)], fill=KAS, outline=INK, width=2)
    txt(fx(kx + KW / 2), fy((Y_DOZ0 + Y_DOZ1) / 2) - 12, URUN[i], f7, INK, "mm")
    txt(fx(kx + KW / 2), fy((Y_DOZ0 + Y_DOZ1) / 2) + 12, "dozaj", f7, GRAY, "mm")
    d.rectangle([fx(kx), fy(Y_DEP1), fx(kx + KW), fy(Y_DEP0)], fill=KAS, outline=INK, width=2)
    txt(fx(kx + KW / 2), fy((Y_DEP0 + Y_DEP1) / 2) - 12, URUN[i], f7, INK, "mm")
    txt(fx(kx + KW / 2), fy((Y_DEP0 + Y_DEP1) / 2) + 12, "depo", f7, GRAY, "mm")
d.line([(fx(X0["TOPPING"] + 20), fy(Y_DEP0 - 10)), (fx(X0["TOPPING"] + 980), fy(Y_DEP0 - 10))], fill=LINE, width=3)
# --- OVEN on gorunus (govde, yalitim, plenumlar, parmaklar, tuneller)
yalitim(fx(OX0), fy(FY1), fx(OX0 + OW), fy(FY1 - ISO))
yalitim(fx(OX0), fy(FY0 + ISO), fx(OX0 + OW), fy(FY0))
yalitim(fx(OX0), fy(FY1), fx(OX0 + DUVAR_X), fy(FY0))
yalitim(fx(OX0 + OW - DUVAR_X), fy(FY1), fx(OX0 + OW), fy(FY0))
d.rectangle([fx(OX0 + DUVAR_X), fy(IC_Y1), fx(OX0 + OW - DUVAR_X), fy(IC_Y0)], fill=BG, outline=FIRIN, width=2)
d.rectangle([fx(HZ0), fy(IC_Y1), fx(HZ1), fy(1420.0)], fill=HAVA, outline=FIRIN, width=1)
d.rectangle([fx(HZ0), fy(1230.0), fx(HZ1), fy(IC_Y0)], fill=HAVA, outline=FIRIN, width=1)
for k in range(7):
    xa = HZ0 + 60.0 + k * 200.0
    d.rectangle([fx(xa), fy(1420.0), fx(xa + 80.0), fy(1370.0)], fill=BG, outline=FIRIN, width=1)
    d.rectangle([fx(xa), fy(1260.0), fx(xa + 80.0), fy(1230.0)], fill=BG, outline=FIRIN, width=1)
    for j in range(3):
        d.line([(fx(xa + 15 + j * 25), fy(1370.0)), (fx(xa + 15 + j * 25), fy(1345.0))], fill=FIRIN, width=1)
        d.line([(fx(xa + 15 + j * 25), fy(1260.0)), (fx(xa + 15 + j * 25), fy(1275.0))], fill=FIRIN, width=1)
drect(fx(HZ0), fy(IC_Y1) + 2, fx(HZ1), fy(IC_Y0) - 2, FIRIN, 3)
for xa, xb in ((OX0, OX0 + DUVAR_X), (OX0 + OW - DUVAR_X, OX0 + OW)):
    d.rectangle([fx(xa), fy(1345.0), fx(xb), fy(1250.0)], fill=BG, outline=FIRIN, width=1)
d.line([(fx(OX0 - 10), fy(Y_BANT)), (fx(OX0 + OW + 10.0), fy(Y_BANT))], fill=FIRIN, width=5)
for k in range(4):
    cx_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(cx_ - 150), fy(Y_BANT + 34.0), fx(cx_ + 150), fy(Y_BANT + 2.0)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
txt(fx(HZ0 + 700.0), fy(1495.0), "ÜST PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 700.0), fy(1140.0), "ALT PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 700.0), fy(1075.0), "PİŞİRME HAZNESİ 1400  ·  gövde 620  ·  aynı anda 4 ürün  ·  bant 450, 5,8 mm/s (pide 240 s)", f8, FIRIN, "mm")
txt(fx(OX0 + OW / 2), fy(FY1 - 25.0), "taşyünü 50 · fan ve rezistanslar arka plenumda (bkz. üst görünüş)", f7, GRAY, "mm")
d.rectangle([fx(OX0), fy(FY0), fx(OX0 + OW), fy(960.0)], fill=BG, outline=GRAY, width=1)
txt(fx(OX0 + OW / 2), fy(980.0), "havalandırma boşluğu 40", f7, GRAY, "mm")
d.rectangle([fx(OX0 + 33), fy(1968.0), fx(OX0 + OW - 33), fy(1660.0)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(HZ1 - 120.0), fy(1660.0), fx(HZ1), fy(FY1)], fill=SOFT, outline=LINE, width=1)
txt(fx(OX0 + OW / 2), fy(1814.0), "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre", f9, INK, "mm")
olcu_h(fx(OX0), fx(TUN_IN0), fy(FY1) - 26, "50", f7, GRAY)
olcu_h(fx(HZ0), fx(HZ1), fy(FY1) - 26, "HAZNE 1400", f9, FIRIN)
olcu_h(fx(TUN_OUT1), fx(OX0 + OW), fy(FY1) - 26, "50", f7, GRAY)
# --- KESME
d.rectangle([fx(kx0 + 40), fy(Y_BANT + 400.0), fx(kx0 + 560), fy(Y_BANT + 60.0)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 300), fy(Y_BANT + 250.0) - 12, "KESİCİ · 8 bıçak", f8, INK, "mm")
txt(fx(kx0 + 300), fy(Y_BANT + 250.0) + 12, "sprey memesi · itici", f7, GRAY, "mm")
d.rectangle([fx(kx0 + 33), fy(1968.0), fx(kx0 + 567), fy(Y_BANT + 430.0)], fill=BG, outline=LINE, width=2)
txt(fx(kx0 + 300), fy((1968.0 + Y_BANT + 430.0) / 2), "TAHRİK · YAĞ KABI", f8, INK, "mm")
# --- PACK
pk0 = X0["PACK"]
d.rectangle([fx(pk0 + 33), fy(1200.0), fx(pk0 + 667), fy(123.0)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 350), fy(660.0) - 12, "ŞARJÖR · 506 blank", f8, INK, "mm")
txt(fx(pk0 + 350), fy(660.0) + 12, "alttan kaldırmalı", f7, GRAY, "mm")
d.rectangle([fx(pk0 + 30), fy(Y_BANT + 300.0), fx(pk0 + 670), fy(Y_BANT - 50.0)], fill=AGZ, outline=RED, width=3)
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) - 10, "KUTULAMA AĞZI", f8, RED, "mm")
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) + 12, "y %s – %s" % (sayi(Y_BANT - 50), sayi(Y_BANT + 300)), f7, RED, "mm")
d.rectangle([fx(pk0 + 33), fy(1968.0), fx(pk0 + 667), fy(Y_BANT + 330.0)], fill=BG, outline=LINE, width=2)
txt(fx(pk0 + 350), fy((1968.0 + Y_BANT + 330.0) / 2), "KALIP · TAHRİK · PANO", f8, INK, "mm")
# --- genel olculer
olcu_h(fx(0), fx(HAT), fy(0) + 116, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(H), fy(0), "1970", f11, INK, "l")
for yy, ad_ in ((120.0, "120"), (900.0, "900"), (FY0, "1000"), (Y_BANT, "1300 bant"), (FY1, "1620"), (1660.0, "1660"), (H, "1970")):
    d.line([(fx(HAT) + 6, fy(yy)), (fx(HAT) + 24, fy(yy))], fill=INK, width=2)
    txt(fx(HAT) + 30, fy(yy), ad_, f8, INK, "lm")

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
yalitim(fx(OX0), py(-790.0), fx(OX0 + OW), py(-730.0))                          # arka duvar
yalitim(fx(OX0), py(-20.0), fx(OX0 + OW), py(40.0))                             # on duvar
yalitim(fx(OX0), py(-730.0), fx(OX0 + DUVAR_X), py(-20.0))                          # sol uc duvari (bant gecis yarigi haric)
yalitim(fx(OX0 + OW - DUVAR_X), py(-730.0), fx(OX0 + OW), py(-20.0))       # sag uc duvari
# plenum
d.rectangle([fx(OX0 + DUVAR_X), py(PL0), fx(OX0 + OW - DUVAR_X), py(PL1)], fill=HAVA, outline=FIRIN, width=2)
for cx_ in (HZ0 + 350.0, HZ0 + 1050.0):
    d.ellipse([fx(cx_ - 100), py(-625.0 - 100), fx(cx_ + 100), py(-625.0 + 100)], outline=FIRIN, width=3)
    txt(fx(cx_), py(-625.0) - 10, "FAN", f8, FIRIN, "mm")
    txt(fx(cx_), py(-625.0) + 12, "Ø200", f7, FIRIN, "mm")
for cx_ in (HZ0 + 700.0,):
    for zz in (-560.0, -610.0, -660.0):
        d.line([(fx(cx_ - 250), py(zz)), (fx(cx_ + 250), py(zz))], fill=RED, width=3)
    txt(fx(cx_), py(-700.0), "REZİSTANS ≈ 18 kW (tahmin)", f7, RED, "mm")
txt(fx(HZ0 + 700.0), py(-543.0), "ARKA PLENUM 210", f7, FIRIN, "mm")
# hazne ici + tuneller
d.rectangle([fx(OX0 + DUVAR_X), py(CH0), fx(OX0 + OW - DUVAR_X), py(CH1)], fill=BG, outline=FIRIN, width=2)
drect(fx(HZ0), py(CH0) + 2, fx(HZ1), py(CH1) - 2, FIRIN, 3)
# yarik: uc duvarlarinda bant gecisi
for xa, xb in ((OX0, OX0 + DUVAR_X), (OX0 + OW - DUVAR_X, OX0 + OW)):
    d.rectangle([fx(xa), py(FB0 - 20), fx(xb), py(FB1 + 20)], fill=BG, outline=FIRIN, width=1)
# bant
d.rectangle([fx(OX0 + 20.0), py(FB0), fx(OX0 + OW - 20.0), py(FB1)], fill=(255, 236, 220), outline=FIRIN, width=2)
for xx in range(int(OX0 + 40), int(OX0 + OW - 20), 60):
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
txt(fx(HZ0 + 700.0), py(-62.0), "PİŞİRME HAZNESİ 1400 × iç 500  ·  aynı anda 4 ürün (adım 350)  ·  bant 450 sürekli, 5,8 mm/s  ·  derinlik 60 + 500 + 210 + 60 = 830", f8, FIRIN, "mm")
d.rectangle([fx(OX0 + OW - DUVAR_X - 120), py(-720.0), fx(OX0 + OW - DUVAR_X - 20), py(-640.0)], fill=BG, outline=INK, width=2)
txt(fx(OX0 + OW - DUVAR_X - 70), py(-680.0), "TAHRİK", f7, INK, "mm")
# olculer: x
olcu_h(fx(OX0), fx(TUN_IN0), py(-790.0) - 26, "50", f7, GRAY)
olcu_h(fx(HZ0), fx(HZ1), py(-790.0) - 26, "HAZNE 1400", f9, FIRIN)
olcu_h(fx(TUN_OUT1), fx(OX0 + OW), py(-790.0) - 26, "50", f7, GRAY)
# olculer: z (derinlik butcesi) — sol tunel bolgesinde
txt(fx(OX0 + OW / 2), py(-760.0), "ARKA DUVAR 60 · taşyünü 50", f7, GRAY, "mm")
txt(fx(OX0 + OW / 2), py(10.0), "ÖN DUVAR 60 · taşyünü 50", f7, GRAY, "mm")
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



# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız", False), (GRAY, YUN, "taşyünü 50 yalıtım", False), (FIRIN, HAVA, "sıcak hava plenum / parmak", False),
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
txt(W_PX - 170, ly + 34, "HAT %s × 1970 × 830  ·  OVEN 1500 × 830 × 620 gövde · tünelsiz  ·  hazne 1400 = 4 ürün  ·  tavan 60/saat  ·  STORE %d çekmece" % (sayi(HAT), CEK), f9, GRAY, "rm")

assert not os.path.exists(OUT), "v4 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s" % sayi(HAT))
