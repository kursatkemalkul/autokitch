# -*- coding: utf-8 -*-
"""AUTOKITCH - TABLALI HAT · OPTIMUM v4 (14 Eyl 2026): ON + UST GORUNUS. Olculer mm. BASTAN HESAPLANMIS YERLESIM.
Kemal: "en bastan dogru, tum kurallarla, belki hat asagida; matematiksel optimum".
KURALLAR: tam 3 gun (pide 240 · lahmacun 600 · icecek 210 · Atosa 1 gunluk set + 2 gunluk dolu yedek hazne seti) · 60 urun/saat 4'lu firin,
  onu arkasi bos yok · 830 derin · cekmece ayri + motorlu + robot ustten alir + top etrafi el payi · conta alini 33 · Atosa alti ray/motor payi.
DEGISKEN: tabla/bant kotu Hb. Hat ustu modullerin en alcak tabani firin (Hb - 300, havalandirma 40) -> STORE ustu Hb - 400,
  kullanilir yukseklik U = Hb - 520; hat yuksekligi Hb + 670.
YIGIN (cekmece v2 adimlari): pide 12 x 108 + lahmacun 18 x 93 + icecek 4 x 165 + yedek raf 3 x 418 = 4884.
BOY: ust sira 670 + 885 + 1420 + 500 + 700 = 4175 + TEKNIK 485 = 4660 · alt sira 655 x kolon + 730 (sarjor 700 + 30).
KUTU YERLESTIRME (tam arama): 6 kolonda en yuksek kolon 820 (karisik) / pratik dizilim 836 -> Hb 1360, hat 2030 -> BOY 4660.
  5 kolon: en yuksek 978 -> Hb 1498, hat 2168, TEKNIK hat altina 4520 (yukseklik +138, Atosa kapagi 2,17 m) -> secilmedi.
  hat asagi (Hb 1000): alt 5 kolon x 480 yetmez -> 2 kolon dolap kulesi -> boy ~5485 -> daha uzun.
DIZILIM (pratik): K1 raf1+raf2 (insan) · K2 raf3 + 4 lahm · K3 6 pide + 2 lahm · K4 6 pide + 2 lahm · K5 1 icecek + 7 lahm · K6 3 icecek + 3 lahm.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_OPTIMUM_v4_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4000, 2800
S, S2 = 0.62, 0.80
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
DOLAP, BOSL, PUC = (14, 120, 90), (190, 190, 196), (255, 240, 200)
BANT, FIRIN, KAS, HEAD, HAVA = (0, 120, 160), (200, 90, 30), (236, 240, 246), (222, 228, 240), (255, 225, 200)
AGZ, YUN = (253, 244, 243), (250, 236, 210)
TABF, SOGUK = (214, 226, 244), (226, 238, 252)


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
H = 2030.0
ISTASYON = [("PRESS v7", 670.0), ("TOPPING · Atosa uyarlama", 885.0), ("OVEN v8 · özel konveyör", 1420.0), ("KESME v2", 500.0), ("PACK v5", 700.0)]
YW = 485.0                                              # yedek kaset dolabi 620 + bolme 35 (hat basinda)
X0, _x = {}, YW
for ad, w in ISTASYON:
    X0[ad.split()[0].split("-")[0]] = _x
    _x += w
HAT = _x                                                # 5100
Y_BANT = 1360.0
ZC = -270.0                                             # bant merkezi
TB0, TB1 = ZC - 200.0, ZC + 200.0                       # topping bandi 400: -470..-70
FB0, FB1 = ZC - 225.0, ZC + 225.0                       # firin bandi 450: -495..-45
CH0, CH1 = -520.0, -20.0                                # hazne ici 500
PL0, PL1 = -730.0, -520.0                               # arka plenum 210
ON_D, ARKA_D = 60.0, 60.0                               # on / arka duvar (sac 1,5 + tasyunu 50 + sac 1 + bosluk)
HAZNE, TUNEL, DUVAR_X = 1320.0, 0.0, 50.0
OW = 1420.0                                             # OVEN modul boyu = 50 + 1400 + 50
OX0 = X0["OVEN"]
TUN_IN0 = OX0 + DUVAR_X                                 # 1750
HZ0 = TUN_IN0 + TUNEL                                   # 2050
HZ1 = HZ0 + HAZNE                                       # 3450
TUN_OUT1 = HZ1 + TUNEL                                  # 3750
FY0, FY1 = 1060.0, 1680.0                               # firin govdesi
ISO = 50.0
IC_Y0, IC_Y1 = FY0 + ISO, FY1 - ISO                     # ic 1050..1570
# --- TOPPING: Atosa Auto Pizza Artisan standart govde 1143 x 800 x 991 · icinde yalniz 1 gunluk hazneler (7)
AW, ATW = 885.0, 35.0
AB0, ATOP = 1039.0, H
Y_KAPAK = 1980.0
Y_HZ0, Y_HZ1 = 1590.0, 1950.0
Y_AGIZ = 1550.0
Y_DAML = 1210.0
Y_RAY0, Y_RAY1 = 1080.0, 1110.0
Z_ON0, Z_ON1 = -55.0, -305.0
Z_AR0, Z_AR1 = -335.0, -585.0
Z_TAB = -320.0
GEN = {"sos": 245.0, "peynir": 510.0, "topping": 95.0}
KAP = {"sos": "12 kg", "peynir": "10 kg", "topping": "2,7 kg"}
HG = 10.0
ON_SIRA = [("KAŞAR", "peynir"), ("HARÇ", "sos")]
AR_SIRA = [("HARÇ", "sos"), ("KIYMA", "sos"), ("KUŞBAŞI", "topping"), ("KUŞBAŞI", "topping"), ("SUCUK", "topping")]


def dizi(sira):
    out, k = [], X0["TOPPING"] + ATW
    for ad_, tip_ in sira:
        out.append((k, GEN[tip_], ad_, tip_))
        k += GEN[tip_] + HG
    assert k - HG <= X0["TOPPING"] + AW - ATW, "hazneler sigmiyor"
    return out


ONX, ARX = dizi(ON_SIRA), dizi(AR_SIRA)
# --- YEDEK DOLAP: 2 gunluk set (14 hazne) · her hazne tam 1 gunluk dolu · raf adimi 385 · ustte TEKNIK
YEDEK = [("raf 1", [("HARÇ", "sos"), ("HARÇ", "sos")], [("HARÇ", "sos"), ("HARÇ", "sos")]), ("raf 2", [("KIYMA", "sos"), ("KIYMA", "sos")], [("KAŞAR", "peynir")]),
         ("raf 3", [("KAŞAR", "peynir")], [("KUŞBAŞI", "topping")] * 4 + [("SUCUK", "topping")] * 2)]
RAF_P, RAF_T, YH = 385.0, 15.0, 1295.0
assert 80.0 + len(YEDEK) * RAF_P + 60.0 == YH
DOLUM = {"HARÇ": "11 kg", "KIYMA": "3,2 kg", "KUŞBAŞI": "1,45 kg", "KAŞAR": "4,4 kg", "SUCUK": "1,4 kg"}   # hazne basi tam 1 gun
PCX = X0["PRESS"] + 335.0
RAY0, RAY1 = X0["PRESS"] + 120.0, X0["TOPPING"] + AW - 40.0
TX_F = X0["TOPPING"] + AW - 180.0
TX_D = ONX[0][0] + ONX[0][1] / 2                        # dozaj ornegi: 2. HARC
CELL0, BIND, FUGA, HH = 130.0, 10.0, 3.0, 88.0
PITCH = 330.0
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
txt(OX, 70, "AUTOKITCH  ·  TABLALI HAT  ·  OPTİMUM  ·  v4", f38, INK)
txt(OX, 138, "ön görünüş + üst görünüş  ·  hat 4660 × 2030 × 830  ·  tam 3 gün stok  ·  tabla / bant 1360 = hesaplanmış en düşük kot  ·  STORE 6 kolon, çekmece v2 (alın 33)  ·  ölçüler mm  ·  14 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 150, "ÖN GÖRÜNÜŞ  ·  MONTAJ HÂLİ  ·  robot tarafından", f16, ACC)
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    d.rectangle([fx(x0), fy(H), fx(x0 + w), fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([fx(x0), fy(80), fx(x0 + w), fy(0)], fill=SOFT, outline=LINE, width=2)
    txt(fx(x0 + w / 2), fy(H) - 64, ad, f13, INK, "md")
    olcu_h(fx(x0), fx(x0 + w), fy(H) - 26, sayi(w), f11, INK)
# --- STORE (alt kat): 6 kolon · kullanilir 120..960 = 840 · cekmece v2 adimlari (alin 33): pide 108 · lahmacun 93 · icecek 165 · yedek raf 418
XI, WO, BOL, STORE_TOP = 35.0, 620.0, 35.0, 960.0
ADIM2 = {"pide": 108.0, "lahm": 93.0, "icecek": 165.0}
RAF2 = 418.0
ADET = {"pide": 20, "lahm": 35, "icecek": 56}
ADK = {"pide": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK"}
BRK = {"pide": "top", "lahm": "top", "icecek": "kutu"}
RAFAD = ["raf 1 · HARÇ ×4", "raf 2 · KIYMA ×2 + KAŞAR", "raf 3 · KAŞAR + KUŞ. ×4 + SUC. ×2"]
KOLON = [[("raf", 0), ("raf", 1)], [("raf", 2), (4, "lahm")], [(6, "pide"), (2, "lahm")], [(6, "pide"), (2, "lahm")], [(1, "icecek"), (7, "lahm")], [(3, "icecek"), (3, "lahm")]]
cx, CEK = XI, 0
SAY = {"pide": 0, "lahm": 0, "icecek": 0}
for ki, kol in enumerate(KOLON):
    if ki:
        d.rectangle([fx(cx - BOL), fy(STORE_TOP), fx(cx), fy(120.0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(cx), fy(STORE_TOP + 60.0), fx(cx + WO), fy(STORE_TOP)], fill=PUC, outline=GRAY, width=1)
    y = 120.0
    for it in kol:
        if it[0] == "raf":
            d.rectangle([fx(cx + 8), fy(y + RAF2 - 3), fx(cx + WO - 8), fy(y)], fill=BG, outline=INK, width=2)
            txt(fx(cx + WO / 2), fy(y + RAF2 / 2) - 12, "YEDEK HAZNE RAFI · kızaklı", f8, INK, "mm")
            txt(fx(cx + WO / 2), fy(y + RAF2 / 2) + 12, RAFAD[it[1]], f7, GRAY, "mm")
            y += RAF2
            continue
        n, tip = it
        h = ADIM2[tip]
        ybas = y
        for _ in range(n):
            d.rectangle([fx(cx + 8), fy(y + h - 3), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=1)
            y += h
        CEK += n
        SAY[tip] += n
        ym = (fy(ybas) + fy(y)) / 2
        for k_, (ss, ff, cc) in enumerate(((("%s × %d" % (ADK[tip], n)), f8, INK), ("%d %s/çekmece · adım %s" % (ADET[tip], BRK[tip], sayi(h)), f7, DOLAP))):
            tw = d.textlength(ss, font=ff)
            yy = ym + (-12 if k_ == 0 else 12)
            d.rectangle([fx(cx + WO / 2) - tw / 2 - 5, yy - 11, fx(cx + WO / 2) + tw / 2 + 5, yy + 11], fill=BG, outline=DOLAP, width=1)
            txt(fx(cx + WO / 2), yy, ss, ff, cc, "mm")
    assert y <= STORE_TOP + 0.5, ("kolon tasiyor", ki + 1, y)
    if STORE_TOP - y > 20:
        d.rectangle([fx(cx + 8), fy(STORE_TOP), fx(cx + WO - 8), fy(y)], fill=(250, 250, 251), outline=BOSL, width=1)
        tarali(fx(cx + 8) + 1, fy(STORE_TOP) + 1, fx(cx + WO - 8) - 1, fy(y) - 1)
    txt(fx(cx + WO / 2), fy(120.0) + 12, "K%d · üst %s" % (ki + 1, sayi(y)), f7, GRAY, "mm")
    cx += WO + BOL
assert SAY == {"pide": 12, "lahm": 18, "icecek": 4}, SAY
TEK0X = cx - BOL
assert TEK0X <= X0["PACK"] - 30.0, "STORE PACK altina tasiyor"
olcu_h(fx(XI), fx(XI + WO), fy(0) + 44, "620", f8, GRAY)
olcu_h(fx(0), fx(TEK0X), fy(0) + 80, "STORE  %s  ·  %d çekmece + 3 yedek hazne rafı  ·  kullanılır 120–960" % (sayi(TEK0X), CEK), f11, INK)
# --- TEKNIK (hat basi, K1 ustunde, 485 x 1010 x 830): sogutma grubu + hat/firin panosu
d.rectangle([fx(0), fy(80.0), fx(YW), fy(0)], fill=SOFT, outline=LINE, width=2)
d.rectangle([fx(0), fy(H), fx(YW), fy(STORE_TOP + 60.0)], fill=SOFT, outline=LINE, width=3)
d.rectangle([fx(25), fy(H - 30.0), fx(YW - 25), fy(1595.0)], fill=BG, outline=INK, width=2)
txt(fx(YW / 2), fy(1805.0) - 12, "HAT PANOSU", f8, INK, "mm")
txt(fx(YW / 2), fy(1805.0) + 12, "PLC · fırın kontaktörleri", f7, GRAY, "mm")
d.rectangle([fx(25), fy(1555.0), fx(YW - 25), fy(STORE_TOP + 95.0)], fill=BG, outline=INK, width=2)
txt(fx(YW / 2), fy(1295.0) - 12, "SOĞUTMA GRUBU", f8, INK, "mm")
txt(fx(YW / 2), fy(1295.0) + 12, "STORE + yedek raflar", f7, GRAY, "mm")
txt(fx(YW / 2), fy(H) - 64, "TEKNİK", f13, INK, "md")
olcu_h(fx(0), fx(YW), fy(H) - 26, sayi(YW), f11, INK)
# --- KESME plakasi
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 10), fy(Y_BANT), fx(kx0 + 490), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(fx(kx0 + 10), fy(Y_BANT)), (fx(kx0 + 490), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(kx0 + 250), fy(Y_BANT - 50.0), "KESME PLAKASI 460 × 450", f8, BANT, "mm")
# --- PRESS: alt govdede tabla + ray gecisi, ORS
px0 = X0["PRESS"] + 15.0
d.rectangle([fx(px0), fy(FY0 + 950.0), fx(px0 + 640.0), fy(FY0)], fill=BG, outline=INK, width=2)
txt(fx(px0 + 320), fy(FY0 + 820.0) - 12, "FERSAH PZP-400", f9, INK, "mm")
txt(fx(px0 + 320), fy(FY0 + 820.0) + 12, "640 × 950 × 800", f7, GRAY, "mm")
d.rectangle([fx(px0 + 20), fy(Y_BANT + 260.0), fx(px0 + 620), fy(FY0)], fill=AGZ, outline=RED, width=3)
txt(fx(PCX), fy(Y_BANT + 205.0), "PRES AĞZI + TABLA / RAY GEÇİŞİ", f8, RED, "mm")
txt(fx(PCX), fy(Y_BANT + 205.0) + 22, "Fersah uyarlaması · alt tabla yerine örs", f7, RED, "mm")
d.rectangle([fx(PCX - 150), fy(Y_BANT - 20.0), fx(PCX + 150), fy(Y_BANT - 120.0)], fill=(150, 150, 158), outline=INK, width=2)
txt(fx(PCX), fy(Y_BANT - 70.0), "ÖRS", f8, BG, "mm")
drect(fx(PCX - 170), fy(Y_BANT), fx(PCX + 170), fy(Y_BANT - 20.0), ACC, 2)
# --- TOPPING · uyarlanmis Atosa (on panel kaldirilmis: on sira hazneler gorunur)
tx0 = X0["TOPPING"]
d.rectangle([fx(tx0), fy(ATOP), fx(tx0 + AW), fy(AB0)], fill=BG, outline=INK, width=3)
d.rectangle([fx(tx0), fy(ATOP), fx(tx0 + AW), fy(Y_KAPAK)], fill=SOFT, outline=INK, width=2)
txt(fx(tx0 + AW / 2), fy((ATOP + Y_KAPAK) / 2), "ÜST KAPAK 50 · yukarı açılır · hazneler üstten takılır", f7, INK, "mm")
d.rectangle([fx(tx0 + ATW), fy(Y_KAPAK), fx(tx0 + AW - ATW), fy(Y_AGIZ + 40.0)], fill=SOGUK, outline=ACC, width=2)
d.rectangle([fx(tx0 + ATW), fy(Y_AGIZ + 40.0), fx(tx0 + AW - ATW), fy(Y_AGIZ)], fill=YUN, outline=GRAY, width=1)
for x_, w_, ad_, tip_ in ONX:
    cx_ = x_ + w_ / 2
    d.rectangle([fx(x_), fy(Y_HZ1), fx(x_ + w_), fy(Y_HZ0)], fill=BG, outline=INK, width=2)
    d.rectangle([fx(cx_ - 15), fy(Y_AGIZ), fx(cx_ + 15), fy(Y_AGIZ - 12.0)], fill=RED)
    txt(fx(cx_), fy(1850.0), ad_, f8, INK, "mm")
    txt(fx(cx_), fy(1850.0) + 22, "ön sıra", f7, GRAY, "mm")
    txt(fx(cx_), fy(1660.0), DOLUM[ad_], f7, RED, "mm")
txt(fx(tx0 + AW / 2), fy(Y_KAPAK - 12.0), "SOĞUK BÖLME +3 °C  ·  arka sıra: HARÇ · KIYMA · KUŞ. ×2 · SUC.", f7, ACC, "mm")
d.rectangle([fx(tx0 + ATW), fy(Y_AGIZ), fx(tx0 + AW - ATW), fy(Y_DAML + 40.0)], fill=(250, 250, 251), outline=GRAY, width=1)
txt(fx(tx0 + AW - 230), fy(Y_AGIZ - 40.0), "TABLA BÖLMESİ 300", f8, INK, "mm")
txt(fx(tx0 + AW - 230), fy(Y_AGIZ - 40.0) + 22, "ön açık · sağ yanda ürün geçişi", f7, GRAY, "mm")
d.rectangle([fx(tx0 + ATW), fy(Y_DAML + 40.0), fx(tx0 + AW - ATW), fy(Y_DAML)], fill=SOFT, outline=LINE, width=2)
txt(fx(tx0 + 560), fy(Y_DAML + 20.0), "DAMLAMA TAVASI 40 · çekmece, günlük yıkanır", f7, INK, "mm")
d.rectangle([fx(tx0), fy(Y_DAML), fx(tx0 + AW), fy(AB0)], fill=(250, 250, 251), outline=LINE, width=2)
tarali(fx(tx0) + 1, fy(Y_DAML) + 1, fx(tx0 + AW) - 1, fy(AB0) - 1)
d.rectangle([fx(RAY0), fy(Y_RAY1), fx(RAY1), fy(Y_RAY0)], fill=ACC)
for _i, _t in enumerate(("RAY + MOTOR PAYI 171", "x kızak · kaldırma · döndürme · kablo zinciri")):
    _f = f8 if _i == 0 else f7
    _tw = d.textlength(_t, font=_f)
    _yy = fy(1182.0) + _i * 22
    d.rectangle([fx(tx0 + 640) - _tw / 2 - 6, _yy - 11, fx(tx0 + 640) + _tw / 2 + 6, _yy + 11], fill=BG)
    txt(fx(tx0 + 640), _yy, _t, _f, INK, "mm")
txt(fx(tx0 + 640), fy(Y_RAY0) + 16, "TABLA RAYI · pres altından fırın ağzına", f7, ACC, "mm")
# tabla: dozajda (kaldirilmis, KASAR altinda) + firin agzinda (kesik)
d.rectangle([fx(TX_D - 110), fy(Y_RAY1 + 90.0), fx(TX_D + 110), fy(Y_RAY1)], fill=BG, outline=ACC, width=2)
d.rectangle([fx(TX_D - 12), fy(1490.0), fx(TX_D + 12), fy(Y_RAY1 + 90.0)], fill=(150, 150, 158))
d.rectangle([fx(TX_D - 170), fy(1510.0), fx(TX_D + 170), fy(1490.0)], fill=TABF, outline=ACC, width=3)
d.ellipse([fx(TX_D - 150), fy(1522.0), fx(TX_D + 150), fy(1510.0)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
txt(fx(tx0 + 600), fy(1420.0), "TABLA Ø340 · dozajda kalkar, döner + kayar", f7, ACC, "mm")
txt(fx(tx0 + 600), fy(1420.0) + 20, "tabla arabası: x kızak · kaldırma · döndürme", f7, ACC, "mm")
drect(fx(TX_F - 170), fy(Y_BANT), fx(TX_F + 170), fy(Y_BANT - 20.0), ACC, 2)
ok(fx(TX_F + 120), fy(Y_BANT + 30.0), fx(tx0 + AW + 60), fy(Y_BANT + 30.0), FIRIN, 3)
txt(fx(TX_F), fy(Y_BANT - 45.0), "fırın ağzı · itici", f7, ACC, "mm")
ok(fx(PCX + 190), fy(Y_BANT + 30.0), fx(tx0 + 150), fy(Y_BANT + 30.0), ACC, 3)
# --- OVEN on gorunus (govde, yalitim, plenumlar, parmaklar, tuneller)
yalitim(fx(OX0), fy(FY1), fx(OX0 + OW), fy(FY1 - ISO))
yalitim(fx(OX0), fy(FY0 + ISO), fx(OX0 + OW), fy(FY0))
yalitim(fx(OX0), fy(FY1), fx(OX0 + DUVAR_X), fy(FY0))
yalitim(fx(OX0 + OW - DUVAR_X), fy(FY1), fx(OX0 + OW), fy(FY0))
d.rectangle([fx(OX0 + DUVAR_X), fy(IC_Y1), fx(OX0 + OW - DUVAR_X), fy(IC_Y0)], fill=BG, outline=FIRIN, width=2)
d.rectangle([fx(HZ0), fy(IC_Y1), fx(HZ1), fy(1480.0)], fill=HAVA, outline=FIRIN, width=1)
d.rectangle([fx(HZ0), fy(1290.0), fx(HZ1), fy(IC_Y0)], fill=HAVA, outline=FIRIN, width=1)
for k in range(7):
    xa = HZ0 + 60.0 + k * 185.0
    d.rectangle([fx(xa), fy(1480.0), fx(xa + 80.0), fy(1430.0)], fill=BG, outline=FIRIN, width=1)
    d.rectangle([fx(xa), fy(1320.0), fx(xa + 80.0), fy(1290.0)], fill=BG, outline=FIRIN, width=1)
    for j in range(3):
        d.line([(fx(xa + 15 + j * 25), fy(1430.0)), (fx(xa + 15 + j * 25), fy(1405.0))], fill=FIRIN, width=1)
        d.line([(fx(xa + 15 + j * 25), fy(1320.0)), (fx(xa + 15 + j * 25), fy(1335.0))], fill=FIRIN, width=1)
drect(fx(HZ0), fy(IC_Y1) + 2, fx(HZ1), fy(IC_Y0) - 2, FIRIN, 3)
for xa, xb in ((OX0, OX0 + DUVAR_X), (OX0 + OW - DUVAR_X, OX0 + OW)):
    d.rectangle([fx(xa), fy(1405.0), fx(xb), fy(1310.0)], fill=BG, outline=FIRIN, width=1)
d.line([(fx(OX0 - 10), fy(Y_BANT)), (fx(OX0 + OW + 10.0), fy(Y_BANT))], fill=FIRIN, width=5)
for k in range(4):
    cx_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(cx_ - 150), fy(Y_BANT + 34.0), fx(cx_ + 150), fy(Y_BANT + 2.0)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
txt(fx(HZ0 + 660.0), fy(1555.0), "ÜST PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 660.0), fy(1200.0), "ALT PLENUM · hava parmakları × 7", f8, FIRIN, "mm")
txt(fx(HZ0 + 660.0), fy(1135.0), "PİŞİRME HAZNESİ 1320  ·  gövde 620  ·  aynı anda 4 ürün  ·  adım 330, bant 5,5 mm/s (pide 240 s)", f8, FIRIN, "mm")
txt(fx(OX0 + OW / 2), fy(FY1 - 25.0), "taşyünü 50 · fan ve rezistanslar arka plenumda (bkz. üst görünüş)", f7, GRAY, "mm")
d.rectangle([fx(OX0), fy(FY0), fx(OX0 + OW), fy(1020.0)], fill=BG, outline=GRAY, width=1)
txt(fx(OX0 + OW / 2), fy(1040.0), "havalandırma boşluğu 40", f7, GRAY, "mm")
d.rectangle([fx(OX0 + 33), fy(2028.0), fx(OX0 + OW - 33), fy(1720.0)], fill=BG, outline=LINE, width=2)
d.rectangle([fx(HZ1 - 120.0), fy(1720.0), fx(HZ1), fy(FY1)], fill=SOFT, outline=LINE, width=1)
txt(fx(OX0 + OW / 2), fy(1874.0), "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre", f9, INK, "mm")
olcu_h(fx(OX0), fx(TUN_IN0), fy(FY1) - 26, "50", f7, GRAY)
olcu_h(fx(HZ0), fx(HZ1), fy(FY1) - 26, "HAZNE 1320", f9, FIRIN)
olcu_h(fx(TUN_OUT1), fx(OX0 + OW), fy(FY1) - 26, "50", f7, GRAY)
# --- KESME
d.rectangle([fx(kx0 + 40), fy(Y_BANT + 400.0), fx(kx0 + 460), fy(Y_BANT + 60.0)], fill=BG, outline=INK, width=2)
txt(fx(kx0 + 250), fy(Y_BANT + 250.0) - 12, "KESİCİ · 8 bıçak", f8, INK, "mm")
txt(fx(kx0 + 250), fy(Y_BANT + 250.0) + 12, "sprey memesi · itici", f7, GRAY, "mm")
d.rectangle([fx(kx0 + 33), fy(2028.0), fx(kx0 + 467), fy(Y_BANT + 430.0)], fill=BG, outline=LINE, width=2)
txt(fx(kx0 + 250), fy((2028.0 + Y_BANT + 430.0) / 2), "TAHRİK · YAĞ KABI", f8, INK, "mm")
# --- PACK
pk0 = X0["PACK"]
d.rectangle([fx(pk0 + 33), fy(1260.0), fx(pk0 + 667), fy(123.0)], fill=BG, outline=INK, width=2)
txt(fx(pk0 + 350), fy(660.0) - 12, "ŞARJÖR · 506 blank", f8, INK, "mm")
txt(fx(pk0 + 350), fy(660.0) + 12, "alttan kaldırmalı", f7, GRAY, "mm")
d.rectangle([fx(pk0 + 30), fy(Y_BANT + 300.0), fx(pk0 + 670), fy(Y_BANT - 50.0)], fill=AGZ, outline=RED, width=3)
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) - 10, "KUTULAMA AĞZI", f8, RED, "mm")
txt(fx(pk0 + 350), fy(Y_BANT + 125.0) + 12, "y %s – %s" % (sayi(Y_BANT - 50), sayi(Y_BANT + 300)), f7, RED, "mm")
d.rectangle([fx(pk0 + 33), fy(2028.0), fx(pk0 + 667), fy(Y_BANT + 330.0)], fill=BG, outline=LINE, width=2)
txt(fx(pk0 + 350), fy((2028.0 + Y_BANT + 330.0) / 2), "KALIP · TAHRİK · PANO", f8, INK, "mm")
# --- genel olculer
olcu_h(fx(0), fx(HAT), fy(0) + 116, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(H), fy(0), "2030", f11, INK, "l")
for yy, ad_ in ((80.0, "80"), (960.0, "960 çekmece üst"), (Y_DAML, "1210 tava"), (Y_BANT, "1360 tabla / bant"), (Y_AGIZ, "1550 ağız"), (FY1, "1680"), (Y_HZ1, "1950 hazne üst"), (H, "2030")):
    d.line([(fx(HAT) + 6, fy(yy)), (fx(HAT) + 24, fy(yy))], fill=INK, width=2)
    txt(fx(HAT) + 30, fy(yy), ad_, f8, INK, "lm")

# ======================= UST GORUNUS =======================
txt(OX, PY_TOP - 110, "ÜST GÖRÜNÜŞ  ·  kapaklar kaldırılmış  ·  topping: hazne bölmesi, tabla ve ray altta (kesik)", f16, ACC)
txt(fx(350.0), py(-790.0) - 34, "ARKA", f9, GRAY, "mm")
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    d.rectangle([fx(x0), py(-790.0), fx(x0 + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    txt(fx(x0 + w / 2), py(40.0) + 30, "%s  ·  %s" % (ad, sayi(w)), f9, INK, "mm")
# --- PRESS
d.rectangle([fx(X0["PRESS"] + 14), py(-788.0), fx(X0["PRESS"] + 654), py(12.0)], fill=BG, outline=INK, width=2)
txt(fx(X0["PRESS"] + 334), py(-600.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X0["PRESS"] + 334), py(-570.0), "640 × 800", f7, GRAY, "mm")
# --- TEKNIK plan
d.rectangle([fx(0), py(-790.0), fx(YW), py(40.0)], fill=SOFT, outline=LINE, width=3)
d.rectangle([fx(40), py(-700.0), fx(YW - 40), py(-260.0)], fill=BG, outline=INK, width=2)
txt(fx(YW / 2), py(-480.0), "SOĞUTMA GRUBU", f8, INK, "mm")
d.rectangle([fx(40), py(-180.0), fx(YW - 40), py(0.0)], fill=BG, outline=INK, width=2)
txt(fx(YW / 2), py(-90.0), "HAT PANOSU", f8, INK, "mm")
txt(fx(YW / 2), py(40.0) + 30, "TEKNİK  ·  485", f9, INK, "mm")
olcu_h(fx(0), fx(YW), py(40.0) + 60, "485", f8, GRAY)
# --- TOPPING · Atosa plan
tx0 = X0["TOPPING"]
d.rectangle([fx(tx0), py(-760.0), fx(tx0 + AW), py(40.0)], fill=BG, outline=INK, width=3)
d.rectangle([fx(tx0), py(-790.0), fx(tx0 + AW), py(-760.0)], fill=(250, 250, 251), outline=GRAY, width=1)
for z0, z1, fl_, ad_ in ((-50.0, 38.0, SOFT, "ÖN PANEL + ÖN SIRA TAHRİKİ 90 · ekran"), (-695.0, -595.0, SOFT, "ARKA SIRA TAHRİKİ 100 · kaplinler arka duvarda"), (-760.0, -695.0, SOGUK, "EVAPORATÖR + FAN 65")):
    d.rectangle([fx(tx0 + ATW), py(z0), fx(tx0 + AW - ATW), py(z1)], fill=fl_, outline=GRAY, width=1)
txt(fx(tx0 + AW / 2), py(18.0), "ÖN PANEL + ÖN SIRA TAHRİKİ 90 · ekran", f7, INK, "mm")
txt(fx(tx0 + 300), py(-652.0), "ARKA SIRA TAHRİKİ 100", f7, INK, "mm")
txt(fx(tx0 + AW / 2), py(-728.0), "EVAPORATÖR + FAN 65 · +3 °C", f7, ACC, "mm")
d.rectangle([fx(tx0 + ATW), py(Z_AR0), fx(tx0 + AW - ATW), py(Z_ON1)], fill=SOGUK)
for sira, z0, z1, agz, zl, pz0 in ((ONX, Z_ON1, Z_ON0, Z_ON1 + 16.0, -110.0, -38.0), (ARX, Z_AR1, Z_AR0, Z_AR0 - 16.0, -530.0, -625.0)):
    for x_, w_, ad_, tip_ in sira:
        cx_ = x_ + w_ / 2
        d.rectangle([fx(x_), py(z0), fx(x_ + w_), py(z1)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(cx_ - 14), py(agz - 14), fx(cx_ + 14), py(agz + 14)], fill=RED)
        d.rectangle([fx(cx_ - 14), py(pz0), fx(cx_ + 14), py(pz0 + 28.0)], fill=RED)
        txt(fx(cx_), py(zl) - 11, ad_ if w_ > 150 else ad_[:3] + ".", f7, INK, "mm")
        txt(fx(cx_), py(zl) + 11, DOLUM[ad_], f7, GRAY, "mm")
_bx = ARX[-1][0] + ARX[-1][1] + HG
if tx0 + AW - ATW - _bx > 60:
    drect(fx(_bx), py(Z_AR1), fx(tx0 + AW - ATW), py(Z_AR0), GRAY, 1)
    txt(fx(_bx + 120.0), py(-550.0), "boş %s" % sayi(tx0 + AW - ATW - _bx), f7, GRAY, "mm")
# tabla hatti + ray + tablalar (altta, kesik)
dline((fx(RAY0), py(Z_TAB)), (fx(TX_F), py(Z_TAB)), ACC, 2)
for zz in (-676.0, -688.0):
    dline((fx(RAY0), py(zz)), (fx(RAY1), py(zz)), ACC, 2)
drect(fx(TX_F - 110), py(-695.0), fx(TX_F + 110), py(-600.0), ACC, 1)
for xc_ in (PCX, TX_F):
    d.ellipse([fx(xc_ - 170), py(Z_TAB - 170), fx(xc_ + 170), py(Z_TAB + 170)], outline=ACC, width=3)
txt(fx(PCX), py(Z_TAB) - 10, "TABLA Ø340", f7, ACC, "mm")
txt(fx(PCX), py(Z_TAB) + 12, "pres altında · örs", f7, ACC, "mm")
txt(fx(PCX), py(-100.0), "tabla hattı z −320", f7, ACC, "mm")
txt(fx(tx0 + AW / 2), py(-790.0) - 26, "RAY + tabla arabası taban altında (kesik)", f7, ACC, "mm")
# --- OVEN plan
# duvarlar (yalitimli)
yalitim(fx(OX0), py(-790.0), fx(OX0 + OW), py(-730.0))                          # arka duvar
yalitim(fx(OX0), py(-20.0), fx(OX0 + OW), py(40.0))                             # on duvar
yalitim(fx(OX0), py(-730.0), fx(OX0 + DUVAR_X), py(-20.0))                          # sol uc duvari (bant gecis yarigi haric)
yalitim(fx(OX0 + OW - DUVAR_X), py(-730.0), fx(OX0 + OW), py(-20.0))       # sag uc duvari
# plenum
d.rectangle([fx(OX0 + DUVAR_X), py(PL0), fx(OX0 + OW - DUVAR_X), py(PL1)], fill=HAVA, outline=FIRIN, width=2)
for cx_ in (HZ0 + 330.0, HZ0 + 990.0):
    d.ellipse([fx(cx_ - 100), py(-625.0 - 100), fx(cx_ + 100), py(-625.0 + 100)], outline=FIRIN, width=3)
    txt(fx(cx_), py(-625.0) - 10, "FAN", f8, FIRIN, "mm")
    txt(fx(cx_), py(-625.0) + 12, "Ø200", f7, FIRIN, "mm")
for cx_ in (HZ0 + 660.0,):
    for zz in (-560.0, -610.0, -660.0):
        d.line([(fx(cx_ - 250), py(zz)), (fx(cx_ + 250), py(zz))], fill=RED, width=3)
    txt(fx(cx_), py(-700.0), "REZİSTANS ≈ 18 kW (tahmin)", f7, RED, "mm")
txt(fx(HZ0 + 660.0), py(-543.0), "ARKA PLENUM 210", f7, FIRIN, "mm")
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
    xa = HZ0 + 60.0 + k * 185.0
    drect(fx(xa), py(CH0 + 20), fx(xa + 80.0), py(CH1 - 20), FIRIN, 2)
txt(fx(HZ0 + 660.0), py(-468.0), "ÜST HAVA PARMAKLARI × 7 (kesikli)  ·  altta × 7", f7, FIRIN, "mm")
# urunler: haznede 4 adet
for k in range(4):
    cx_ = HZ0 + PITCH / 2 + k * PITCH
    d.ellipse([fx(cx_ - 150), py(ZC - 150), fx(cx_ + 150), py(ZC + 150)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
    txt(fx(cx_), py(ZC), "Ø300", f7, (160, 120, 50), "mm")
ok(fx(OX0 + 60.0), py(ZC + 190), fx(OX0 + 200.0), py(ZC + 190), FIRIN, 3)
txt(fx(HZ0 + 660.0), py(-62.0), "PİŞİRME HAZNESİ 1320 × iç 500  ·  4 ürün, adım 330  ·  bant 450, 5,5 mm/s  ·  derinlik 60 + 500 + 210 + 60 = 830", f8, FIRIN, "mm")
d.rectangle([fx(OX0 + OW - DUVAR_X - 120), py(-720.0), fx(OX0 + OW - DUVAR_X - 20), py(-640.0)], fill=BG, outline=INK, width=2)
txt(fx(OX0 + OW - DUVAR_X - 70), py(-680.0), "TAHRİK", f7, INK, "mm")
# olculer: x
olcu_h(fx(OX0), fx(TUN_IN0), py(-790.0) - 60, "50", f7, GRAY)
olcu_h(fx(HZ0), fx(HZ1), py(-790.0) - 60, "HAZNE 1320", f9, FIRIN)
olcu_h(fx(TUN_OUT1), fx(OX0 + OW), py(-790.0) - 60, "50", f7, GRAY)
# olculer: z (derinlik butcesi) — sol tunel bolgesinde
txt(fx(OX0 + OW / 2), py(-760.0), "ARKA DUVAR 60 · taşyünü 50", f7, GRAY, "mm")
txt(fx(OX0 + OW / 2), py(10.0), "ÖN DUVAR 60 · taşyünü 50", f7, GRAY, "mm")
# --- KESME plan
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 20), py(FB0), fx(kx0 + 480), py(FB1)], fill=(232, 244, 250), outline=BANT, width=2)
d.ellipse([fx(kx0 + 90), py(ZC - 160), fx(kx0 + 410), py(ZC + 160)], outline=INK, width=2)
for k in range(4):
    a = k * math.pi / 4
    d.line([(fx(kx0 + 250) - 160 * S * math.cos(a), py(ZC) - 160 * S * math.sin(a)),
            (fx(kx0 + 250) + 160 * S * math.cos(a), py(ZC) + 160 * S * math.sin(a))], fill=INK, width=1)
txt(fx(kx0 + 250), py(-560.0), "KESİCİ Ø320 · 8 bıçak", f7, INK, "mm")
txt(fx(kx0 + 250), py(-600.0), "KESME PLAKASI 460 × 450", f7, BANT, "mm")
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
ok(fx(kx0 + 440), py(ZC), fx(pk0 + 50), py(ZC), INK, 2)
# genel olculer + kesit isaretleri
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
for ad, w in ISTASYON:
    x0 = X0[ad.split()[0].split("-")[0]]
    olcu_h(fx(x0), fx(x0 + w), py(40.0) + 60, sayi(w), f8, GRAY)
olcu_v(fx(0) - 44, py(-790.0), py(40.0), "830", f11, INK, "l")
txt(fx(HAT / 2), py(40.0) + 150, "ÖN  ·  robot tarafı  ·  Atosa derinliği: ön panel 90 + ön sıra 250 + ağız hattı 30 + arka sıra 250 + tahrik 100 + evaporatör 65 = 800  ·  arkada servis 30", f9, GRAY, "mm")



# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız", False), (GRAY, YUN, "taşyünü 50 yalıtım", False), (FIRIN, HAVA, "sıcak hava plenum / parmak", False),
       (FIRIN, (255, 236, 220), "fırın bandı", False), (ACC, TABF, "tabla / ray", False), (ACC, SOGUK, "soğuk hazne bölmesi +3 °C", False), (DOLAP, BG, "çekmece +3 °C", False),
       (GRAY, PUC, "PU yalıtım (STORE)", False), (RED, RED, "hazne ağzı / tahrik", False), (GRAY, BG, "boş hazne yeri", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
txt(W_PX - 170, ly + 34, "HAT %s × 2030 × 830  ·  TEKNİK 485  ·  TOPPING Atosa uyarlama 885 · 7 hazne (1 gün)  ·  OVEN 1420 · 4 ürün  ·  STORE %d çekmece + 3 yedek raf (14 hazne, 2 gün)" % (sayi(HAT), CEK), f9, GRAY, "rm")

assert not os.path.exists(OUT), "optimum v4 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s" % sayi(HAT))
