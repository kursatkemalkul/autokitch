# -*- coding: utf-8 -*-
"""AUTOKITCH - TABLALI HAT · ATOSA ENTEGRE TEKNIK RESIM v1 (14 Eyl 2026): ON GORUNUS + UST GORUNUS.
Kemal: Atosa Auto Pizza Artisan'i ozellestirip bizim hatta (HAT_BANTLI_v4) koymusuz gibi; altindaki bosluk sayilmaz, ray + motor payi birakilir;
hazneler Atosa gibi kisa, onde + arkada iki sira; hedef gunlere gore kac hazne gerektigi hesaplanir. Olculer mm.
KAYNAK: Atosa brosuru 1143 x 800 x 991 · sos 26,5 lb (12 kg) · peynir 22 lb (10 kg) · 4 x topping 6 lb (2,72 kg) · pepperoni dilimleyici 6 cubuk;
  Atosa kareleri (tabla kolonlu tasiyicida, ray arka duvarda, hazne arka duvardaki kapline takiliyor, ust kapak aciliyor, tabla bolmesi ~300);
  hedefler (Yindu maili v4): harc 22 kg/gun x 2 · kiyma 3,2 x 3 · kusbasi 2,9 x 3 · kasar 4,4 x 7 · sucuk 1,4 x 7 · her hazne en az 1 gun.
HESAP: hazne sayisi = gunluk x hedef gun / Atosa hazne kg -> harc 4 sos · kiyma 1 sos · kusbasi 4 topping · kasar 4 peynir · sucuk 4 topping = 17 (Atosa standart 6).
VARSAYIM (etiketli): hazne genisligi = hacim / (0,55 x 250 x 360); 0,55 = bizim kasetin dolu hacim orani (12,5 L / 140 x 240 x 680);
  yogunluk harc 1,0 · kasar 0,40 · kusbasi/sucuk 0,58; topping 95 genislik fotograftaki ~108 ile uyumlu.
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_ATOSA_ENTEGRE_v1_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4300, 2800
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
H = 1970.0
ISTASYON = [("PRESS v7", 700.0), ("TOPPING · Atosa uyarlama", 2300.0), ("OVEN v7 · özel konveyör", 1500.0), ("KESME v1", 600.0), ("PACK v5", 700.0)]
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
# --- TOPPING: uyarlanmis Atosa Auto Pizza Artisan (standart 1143 x 800 x 991) -> 2300 boy, kisa hazneler on + arka sira
AW, ATW = 2300.0, 35.0                                  # modul boyu (~2 Atosa govdesi) · yan duvar
AB0, ATOP = 979.0, H                                    # Atosa govde yuksekligi 991
Y_KAPAK = 1920.0                                        # ust kapak 50
Y_HZ0, Y_HZ1 = 1530.0, 1890.0                           # hazne 360
Y_AGIZ = 1490.0                                         # yalitimli taban 1490..1530 · agizlar
Y_DAML = 1150.0                                         # damlama tavasi 1150..1190 · tabla bolmesi 1190..1490
Y_RAY0, Y_RAY1 = 1020.0, 1050.0                         # x kizak rayi (taban alti)
Z_ON0, Z_ON1 = -55.0, -305.0                            # on sira hazne 250
Z_AR0, Z_AR1 = -335.0, -585.0                           # arka sira hazne 250
Z_TAB = -320.0                                          # tabla / agiz hatti (firin bandi merkezi -270, bant 450 icinde)
GEN = {"sos": 245.0, "peynir": 510.0, "topping": 95.0}
KAP = {"sos": "12 kg", "peynir": "10 kg", "topping": "2,7 kg"}
KOL = [("HARÇ", "sos", "HARÇ"), ("HARÇ", "sos", "HARÇ"), ("KIYMA", "sos", None), ("KUŞBAŞI", "topping", "KUŞBAŞI"), ("KUŞBAŞI", "topping", "KUŞBAŞI"),
       ("KAŞAR", "peynir", "KAŞAR"), ("KAŞAR", "peynir", "KAŞAR"), ("SUCUK", "topping", "SUCUK"), ("SUCUK", "topping", "SUCUK")]
HG = 10.0
KOLX, _k = [], X0["TOPPING"] + ATW
for on_, tip_, ar_ in KOL:
    KOLX.append((_k, GEN[tip_], on_, tip_, ar_))
    _k += GEN[tip_] + HG
assert _k - HG <= X0["TOPPING"] + AW - ATW, "hazneler sigmiyor"
PCX = X0["PRESS"] + 350.0                               # pres merkezi
RAY0, RAY1 = X0["PRESS"] + 120.0, X0["TOPPING"] + AW - 40.0
TX_F = X0["TOPPING"] + AW - 180.0                       # tabla firin agzinda
TX_D = KOLX[5][0] + KOLX[5][1] / 2                      # dozaj ornegi: KASAR
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
txt(OX, 70, "AUTOKITCH  ·  TABLALI HAT  ·  ATOSA ENTEGRE  ·  TEKNİK RESİM  v1", f38, INK)
txt(OX, 138, "ön görünüş + üst görünüş  ·  topping = uyarlanmış Atosa Auto Pizza Artisan (standart 1143 × 800 × 991): 2300 boy, kısa hazneler önde + arkada, 17 hazne  ·  tabla presten fırın ağzına tek rayda  ·  830 derin  ·  ölçüler mm  ·  14 Eylül 2026", f13, GRAY)
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
KOLON = [(940.0, [(6, "hamur")]), (900.0, [(6, "hamur")]), (900.0, [(2, "paket"), (4, "lahm")]), (900.0, [(5, "lahm")]), (900.0, [(5, "lahm")])]
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
d.rectangle([fx(TEK0X), fy(900.0), fx(TEK1X), fy(120.0)], fill=SOFT, outline=LINE, width=2)
txt(fx((TEK0X + TEK1X) / 2), fy(660.0) - 24, "TEKNİK", f8, GRAY, "mm")
txt(fx((TEK0X + TEK1X) / 2), fy(660.0), "soğutma grupları", f7, GRAY, "mm")
txt(fx((TEK0X + TEK1X) / 2), fy(660.0) + 22, "fırın + hat panosu", f7, GRAY, "mm")
olcu_h(fx(XI), fx(XI + WO), fy(0) + 44, "620", f8, GRAY)
olcu_h(fx(0), fx(TEK0X), fy(0) + 80, "STORE  %s  ·  %d çekmece  ·  tabla hattı altında" % (sayi(TEK0X), CEK), f11, INK)
# --- KESME plakasi
kx0 = X0["KESME"]
d.rectangle([fx(kx0 + 10), fy(Y_BANT), fx(kx0 + 590), fy(Y_BANT - 100.0)], fill=BG, outline=BANT, width=2)
d.line([(fx(kx0 + 10), fy(Y_BANT)), (fx(kx0 + 590), fy(Y_BANT))], fill=BANT, width=5)
txt(fx(kx0 + 300), fy(Y_BANT - 50.0), "KESME PLAKASI 560 × 450", f8, BANT, "mm")
# --- PRESS: alt govdede tabla + ray gecisi, ORS
px0 = X0["PRESS"] + 30.0
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
for x_, w_, on_, tip_, ar_ in KOLX:
    cx_ = x_ + w_ / 2
    d.rectangle([fx(x_), fy(Y_HZ1), fx(x_ + w_), fy(Y_HZ0)], fill=BG, outline=INK, width=2)
    d.rectangle([fx(cx_ - 15), fy(Y_AGIZ), fx(cx_ + 15), fy(Y_AGIZ - 12.0)], fill=RED)
    txt(fx(cx_), fy(1600.0), KAP[tip_], f7, RED, "mm")
    if w_ > 150:
        txt(fx(cx_), fy(1790.0), on_, f8, INK, "mm")
        txt(fx(cx_), fy(1790.0) + 22, "ön + arka" if ar_ else "ön · arka boş", f7, GRAY, "mm")
    else:
        txt(fx(cx_), fy(1790.0), on_[:3] + ".", f7, INK, "mm")
txt(fx(tx0 + AW / 2), fy(Y_KAPAK - 12.0), "SOĞUK HAZNE BÖLMESİ +3 °C  ·  hazne 360 yüksek × 250 derin  ·  ön sıra görünüyor, arka sıra aynı dizilişte", f7, ACC, "mm")
d.rectangle([fx(tx0 + ATW), fy(Y_AGIZ), fx(tx0 + AW - ATW), fy(Y_DAML + 40.0)], fill=(250, 250, 251), outline=GRAY, width=1)
txt(fx(tx0 + AW - 330), fy(Y_AGIZ - 40.0), "TABLA BÖLMESİ 300", f8, INK, "mm")
txt(fx(tx0 + AW - 330), fy(Y_AGIZ - 40.0) + 22, "ön açık · sağ yanda ürün geçişi", f7, GRAY, "mm")
d.rectangle([fx(tx0 + ATW), fy(Y_DAML + 40.0), fx(tx0 + AW - ATW), fy(Y_DAML)], fill=SOFT, outline=LINE, width=2)
txt(fx(tx0 + 560), fy(Y_DAML + 20.0), "DAMLAMA TAVASI 40 · çekmece, günlük yıkanır", f7, INK, "mm")
d.rectangle([fx(tx0), fy(Y_DAML), fx(tx0 + AW), fy(AB0)], fill=(250, 250, 251), outline=LINE, width=2)
tarali(fx(tx0) + 1, fy(Y_DAML) + 1, fx(tx0 + AW) - 1, fy(AB0) - 1)
d.rectangle([fx(RAY0), fy(Y_RAY1), fx(RAY1), fy(Y_RAY0)], fill=ACC)
_t = "RAY + MOTOR PAYI 171  ·  x kızak motoru, kaldırma + döndürme motoru, kablo zinciri"
_tw = d.textlength(_t, font=f8)
d.rectangle([fx(tx0 + 560) - _tw / 2 - 8, fy(1105.0) - 13, fx(tx0 + 560) + _tw / 2 + 8, fy(1105.0) + 13], fill=BG)
txt(fx(tx0 + 560), fy(1105.0), _t, f8, INK, "mm")
txt(fx(tx0 + 560), fy(Y_RAY0) + 16, "TABLA RAYI · pres altından fırın ağzına", f7, ACC, "mm")
# tabla: dozajda (kaldirilmis, KASAR altinda) + firin agzinda (kesik)
d.rectangle([fx(TX_D - 110), fy(Y_RAY1 + 90.0), fx(TX_D + 110), fy(Y_RAY1)], fill=BG, outline=ACC, width=2)
d.rectangle([fx(TX_D - 12), fy(1430.0), fx(TX_D + 12), fy(Y_RAY1 + 90.0)], fill=(150, 150, 158))
d.rectangle([fx(TX_D - 170), fy(1450.0), fx(TX_D + 170), fy(1430.0)], fill=TABF, outline=ACC, width=3)
d.ellipse([fx(TX_D - 150), fy(1462.0), fx(TX_D + 150), fy(1450.0)], fill=(240, 214, 170), outline=(200, 160, 80), width=2)
txt(fx(TX_D - 190), fy(1400.0), "TABLA Ø340 · dozajda kalkar, döner + kayar", f7, ACC, "rm")
txt(fx(TX_D - 190), fy(1400.0) + 20, "tabla arabası: x kızak · kaldırma · döndürme", f7, ACC, "rm")
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
for yy, ad_ in ((120.0, "120"), (900.0, "900"), (AB0, "979 Atosa alt"), (Y_DAML, "1150 tava"), (Y_BANT, "1300 tabla / bant"), (Y_AGIZ, "1490 ağız"), (FY1, "1620"), (Y_HZ1, "1890 hazne üst"), (H, "1970")):
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
d.rectangle([fx(X0["PRESS"] + 29), py(-788.0), fx(X0["PRESS"] + 669), py(12.0)], fill=BG, outline=INK, width=2)
txt(fx(X0["PRESS"] + 349), py(-600.0), "FERSAH PZP-400", f8, INK, "mm")
txt(fx(X0["PRESS"] + 349), py(-570.0), "640 × 800", f7, GRAY, "mm")
# --- TOPPING · Atosa plan
tx0 = X0["TOPPING"]
d.rectangle([fx(tx0), py(-760.0), fx(tx0 + AW), py(40.0)], fill=BG, outline=INK, width=3)
d.rectangle([fx(tx0), py(-790.0), fx(tx0 + AW), py(-760.0)], fill=(250, 250, 251), outline=GRAY, width=1)
for z0, z1, fl_, ad_ in ((-50.0, 38.0, SOFT, "ÖN PANEL + ÖN SIRA TAHRİKİ 90 · ekran"), (-695.0, -595.0, SOFT, "ARKA SIRA TAHRİKİ 100 · kaplinler arka duvarda"), (-760.0, -695.0, SOGUK, "EVAPORATÖR + FAN 65")):
    d.rectangle([fx(tx0 + ATW), py(z0), fx(tx0 + AW - ATW), py(z1)], fill=fl_, outline=GRAY, width=1)
txt(fx(tx0 + 1150), py(18.0), "ÖN PANEL + ÖN SIRA TAHRİKİ 90 · ekran", f7, INK, "mm")
txt(fx(tx0 + 560), py(-652.0), "ARKA SIRA TAHRİKİ 100 · kaplinler arka duvarda (Atosa gibi)", f7, INK, "mm")
txt(fx(tx0 + 1150), py(-728.0), "EVAPORATÖR + FAN 65 · +3 °C", f7, ACC, "mm")
d.rectangle([fx(tx0 + ATW), py(Z_AR0), fx(tx0 + AW - ATW), py(Z_ON1)], fill=SOGUK)
for x_, w_, on_, tip_, ar_ in KOLX:
    cx_ = x_ + w_ / 2
    for z0, z1, ad_, agz, zl in ((Z_ON1, Z_ON0, on_, Z_ON1 + 16.0, -110.0), (Z_AR1, Z_AR0, ar_, Z_AR0 - 16.0, -530.0)):
        if ad_ is None:
            drect(fx(x_), py(z0), fx(x_ + w_), py(z1), GRAY, 1)
            txt(fx(cx_), py((z0 + z1) / 2), "boş", f7, GRAY, "mm")
            continue
        d.rectangle([fx(x_), py(z0), fx(x_ + w_), py(z1)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(cx_ - 14), py(agz - 14), fx(cx_ + 14), py(agz + 14)], fill=RED)
        txt(fx(cx_), py(zl) - 11, ad_ if w_ > 150 else ad_[:3] + ".", f7, INK, "mm")
        txt(fx(cx_), py(zl) + 11, KAP[tip_], f7, GRAY, "mm")
    d.rectangle([fx(cx_ - 14), py(-38.0), fx(cx_ + 14), py(-10.0)], fill=RED)
    d.rectangle([fx(cx_ - 14), py(-625.0), fx(cx_ + 14), py(-597.0)], fill=RED)
# tabla hatti + ray + tablalar (altta, kesik)
dline((fx(RAY0), py(Z_TAB)), (fx(TX_F), py(Z_TAB)), ACC, 2)
for zz in (-676.0, -688.0):
    dline((fx(RAY0), py(zz)), (fx(RAY1), py(zz)), ACC, 2)
drect(fx(TX_D - 110), py(-690.0), fx(TX_D + 110), py(-300.0), ACC, 1)
for xc_ in (PCX, TX_D, TX_F):
    d.ellipse([fx(xc_ - 170), py(Z_TAB - 170), fx(xc_ + 170), py(Z_TAB + 170)], outline=ACC, width=3)
txt(fx(PCX), py(Z_TAB) - 10, "TABLA Ø340", f7, ACC, "mm")
txt(fx(PCX), py(Z_TAB) + 12, "pres altında · örs", f7, ACC, "mm")
txt(fx(PCX), py(-100.0), "tabla hattı z −320", f7, ACC, "mm")
txt(fx(tx0 + 2150), py(-790.0) - 26, "RAY + tabla arabası taban altında (kesik)", f7, ACC, "mm")
olcu_h(fx(tx0), fx(tx0 + 1143.0), py(-790.0) - 26, "Atosa standart gövde 1143", f8, GRAY)
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
olcu_h(fx(OX0), fx(TUN_IN0), py(-790.0) - 60, "50", f7, GRAY)
olcu_h(fx(HZ0), fx(HZ1), py(-790.0) - 60, "HAZNE 1400", f9, FIRIN)
olcu_h(fx(TUN_OUT1), fx(OX0 + OW), py(-790.0) - 60, "50", f7, GRAY)
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
txt(W_PX - 170, ly + 34, "HAT %s × 1970 × 830  ·  TOPPING Atosa uyarlama 2300 × 800 × 991 · 17 hazne  ·  OVEN 1500 · hazne 1400 = 4 ürün  ·  STORE %d çekmece" % (sayi(HAT), CEK), f9, GRAY, "rm")

assert not os.path.exists(OUT), "entegre v1 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s" % sayi(HAT))
