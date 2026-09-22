# -*- coding: utf-8 -*-
"""AUTOKITCH - BASE HAT TEKNIK RESIM v8 (13 Eyl 2026): ON + UST (PLAN KESITI) + YAN (STORE KESITI). Olculer mm.

v7'den FARKI (Kemal, 13 Eyl): SATIS GUNDE 80 PIDE + 200 LAHMACUN, STOK KURALLARI
  hamur TAM 3 gun · icecek TAM 7 gun (maliyet sayfasi orani: urun basina %25 -> 70 kutu/gun)
  pide mayali  : 1 gun taze +3 (4 cekmece) + 2 gun donmus -18 (8 cekmece), aksam 4 tepsi -18 -> +3 cozulme
  lahmacun     : mayasiz hamur, 3 gun +3 (20 cekmece x 30 = 600)
  icecek       : 9 cekmece x 56 = 504 kutu (7,2 gun)
  STORE v6     : 4 kolon x 620 · bolme 65 (-18|+3) / 35 / 35 · 2740 mm · 43 cekmece
                 K1 8 donmus + ayirici + 2 lahmacun · K2 12 lahmacun · K3 4 taze pide + 6 lahmacun + 2 PAKET · K4 9 icecek
                 PAKET = kasar + sucuk haftalik vakum paketi (eleman her gun kaseti doldurur)
  TOPPING v6   : dis olcu ayni · PLASTIK kaset (bos <= 5,7 kg: robot 16,5 - yarim gunluk harc 10,8)
                 kaset = 1 gunluk (harc yarim gunluk, gunde 2) · harc/kiyma/kusbasi stok 2 gun · sucuk/kasar kasette 2 gun + pakette 5 gun
                 12 kaset / 14 yuva: kat1 KASAR SUCUK · kat2 HARC HARC · kat3 KIYMA KUSBASI · alt1 HARC HARC KIYMA KUSBASI · alt2 SUCUK KASAR BOS BOS
                 (iki harc kaseti de dozaj katinda: gun ortasinda kaset takasi yok)
  PRESS v6 / OVEN v5 / PACK v4 : v7 ile ayni (830)
  HAT 5540 x 1970 x 830.
KAYNAK: teknik_hat_base_v7.py + 13 Eyl stok hesabi (CAP pide 20 / lahmacun 30 / icecek 56 · HH 115 / 88 / 132 · alin 33 · hucre 167,5..1660).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BASE_v8_teknik.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4760, 2800
S = 0.62
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ = (253, 244, 243)


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


def etiket(x, y, s, f=f8, c=INK, cer=GRAY):
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw / 2 - 6, y - 11, x + tw / 2 + 6, y + 11], fill=BG, outline=cer, width=1)
    txt(x, y, s, f, c, "mm")


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


# ======================= VERI =======================
DZ = 830.0                                              # TUM istasyonlar: z -790 .. +40
XI, WO, BOLME = 62.5, 620.0, (65.0, 35.0, 35.0)
CELL0, CELL1, BIND, FUGA, TEK0 = 182.5, 1660.0, 15.0, 3.0, 1720.0
YUZ0 = CELL0 - BIND
HH = {"donmus": 115.0, "hamur": 88.0, "lahm": 88.0, "icecek": 132.0, "paket": 88.0}
AD = {"donmus": "DONMUŞ PİDE", "hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK 330 ml",
      "paket": "KAŞAR + SUCUK PAKETİ"}
CAP = {"donmus": (20, "top"), "hamur": (20, "top"), "lahm": (30, "top"), "icecek": (56, "kutu"), "paket": (None, "vakum")}
KOLON = [[(8, "donmus", "-18"), "ayirici", (2, "lahm", "+3")],
         [(12, "lahm", "+3")],
         [(4, "hamur", "+3"), (6, "lahm", "+3"), (2, "paket", "+3")],
         [(9, "icecek", "+3")]]
KOLON_AD = ("K1 · alt −18 / üst +3", "K2 · +3", "K3 · +3", "K4 · +3")
WS = 2 * XI + len(KOLON) * WO + sum(BOLME)            # 2740

# kolon yuksekligi kontrolu: son cekmecenin ustu hucre tavanini (1660) gecmemeli
for gruplar in KOLON:
    y = YUZ0
    for g in gruplar:
        if g == "ayirici":
            y += 48.0
            continue
        y += g[0] * (HH[g[1]] + 2 * BIND + FUGA)
    assert y - FUGA <= CELL1, "kolon tasiyor: %.1f" % (y - FUGA)

ISTASYON = [("STORE v6", WS, DZ), ("PRESS v6", 700.0, DZ), ("TOPPING v6", 700.0, DZ),
            ("OVEN v5", 700.0, DZ), ("PACK v4", 700.0, DZ)]
HAT = sum(w for _, w, _ in ISTASYON)                   # 5540

# cephe: (tip k=kapak / a=acik agiz, x0, x1, y0, y1, ad, kaset yuvasi, etiket kotu)
CEPHE = {
    "PRESS v6": [("k", 33.0, 667.0, 121.5, 1091.5, "FERSAH PZP-400|640 × 950 × 800", None, 440.0),
                 ("a", 53.0, 647.0, 760.0, 1020.0, "PRES AĞZI", None, None),
                 ("k", 33.0, 667.0, 1094.5, 1392.5, "", None, None),
                 ("a", 53.0, 647.0, 1120.0, 1370.0, "UÇ AĞZI · çatal · pençe · vantuz", None, None),
                 ("k", 33.0, 437.0, 1395.5, 1672.5, "ÇÖP KUTUSU|59 L", None, None),
                 ("k", 33.0, 437.0, 1675.5, 1968.5, "", None, None),
                 ("a", 53.0, 417.0, 1697.0, 1947.0, "ATMA AĞZI", None, None),
                 ("k", 440.0, 667.0, 1395.5, 1968.5, "BOŞ", None, None)],
    "TOPPING v6": [("k", 33.0, 667.0, 210.0, 489.0, "", "alt2", None),
                   ("k", 33.0, 667.0, 492.0, 771.0, "", "alt1", None),
                   ("a", 30.0, 670.0, 774.0, 891.0, "ROBOT AĞZI", None, None),
                   ("k", 33.0, 667.0, 891.0, 1170.0, "", "kat3", None),
                   ("a", 30.0, 670.0, 1173.0, 1290.0, "ROBOT AĞZI", None, None),
                   ("k", 33.0, 667.0, 1290.0, 1569.0, "", "kat2", None),
                   ("a", 30.0, 670.0, 1572.0, 1689.0, "ROBOT AĞZI", None, None),
                   ("k", 33.0, 667.0, 1689.0, 1968.0, "", "kat1", None)],
    "OVEN v5": [("k", 33.0, 667.0, 123.0, 370.0, "YAĞ KABI · PANO", None, None),
                ("a", 30.0, 670.0, 373.0, 533.0, "İŞLEM AĞZI · sprey", None, None),
                ("k", 33.0, 667.0, 536.0, 816.0, "KESİCİ", None, None),
                ("k", 33.0, 667.0, 822.0, 1097.0, "FIRIN HAZNE 1", None, None),
                ("k", 33.0, 667.0, 1102.0, 1377.0, "FIRIN HAZNE 2", None, None),
                ("k", 33.0, 667.0, 1382.0, 1657.0, "FIRIN HAZNE 3", None, None),
                ("k", 33.0, 667.0, 1662.0, 1968.0, "EGZOZ · fan · karbon filtre", None, None)],
    "PACK v4": [("k", 33.0, 667.0, 123.0, 420.0, "PANO", None, None),
                ("k", 33.0, 667.0, 423.0, 695.0, "VAKUM + TAHRİK", None, None),
                ("a", 30.0, 670.0, 698.0, 948.0, "KUTULAMA AĞZI", None, None),
                ("k", 33.0, 667.0, 951.0, 1880.0, "KALIP + ŞARJÖR", None, None),
                ("k", 33.0, 667.0, 1883.0, 1968.0, "", None, None)],
}
YUVA = {"kat1": ("KAŞAR", "SUCUK"), "kat2": ("HARÇ", "HARÇ"), "kat3": ("KIYMA", "KUŞBAŞI"),
        "alt1": ("HARÇ", "HARÇ", "KIYMA", "KUŞBAŞI"), "alt2": ("SUCUK", "KAŞAR", None, None)}
RAF_X = {"kat": (270.0, 430.0), "alt": (125.0, 275.0, 425.0, 575.0)}

# ======================= YERLESIM =======================
OX = 300.0
FY_TOP = 360.0
FY = FY_TOP + 1970.0 * S                                # on gorunus zemin cizgisi
PY_TOP = FY + 300.0                                     # plan: z = -790 cizgisi (arka)
SX = OX + HAT * S + 300.0                               # yan gorunus: z = -790 kenari


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


# ======================= BASLIK =======================
txt(OX, 70, "AUTOKITCH  ·  BASE HAT  ·  TEKNİK RESİM  v8", f38, INK)
txt(OX, 138, "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun  ·  tüm istasyonlar 830 derin  ·  ölçüler mm  ·  13 Eylül 2026", f13, GRAY)
d.line([(OX, 178), (W_PX - 170, 178)], fill=LINE, width=3)

# ======================= ON GORUNUS =======================
txt(OX, FY_TOP - 150, "ÖN GÖRÜNÜŞ", f16, ACC)


def kabin_on(x0mm, w, ad):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(1970), x1, fy(0)], fill=FILL, outline=LINE, width=3)
    d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    txt((x0 + x1) / 2, fy(1970) - 64, ad, f13, INK, "md")


def istasyon_on(x0mm, ad):
    kabin_on(x0mm, 700.0, ad)
    for tip, a, b, y0, y1, et, yv, yl in CEPHE[ad]:
        if tip != "k":
            continue
        d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=BG, outline=LINE, width=2)
        if yv:
            ym = (y0 + y1) / 2.0
            for xc, urun in zip(RAF_X["kat" if yv.startswith("kat") else "alt"], YUVA[yv]):
                drect(fx(x0mm + xc - 70), fy(ym + 120), fx(x0mm + xc + 70), fy(ym - 120), INK if urun else BOSL, 1)
                txt(fx(x0mm + xc), fy(ym) - 10, urun or "BOŞ", f7, INK if urun else GRAY, "mm")
                if urun:
                    txt(fx(x0mm + xc), fy(ym) + 10, "dozaj" if yv.startswith("kat") else "depo", f7, GRAY, "mm")
        elif et:
            satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)
    for tip, a, b, y0, y1, et, yv, yl in CEPHE[ad]:
        if tip != "a":
            continue
        d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
        cy = (fy(y0) + fy(y1)) / 2
        txt(fx(x0mm + (a + b) / 2), cy - 10, et, f8, RED, "mm")
        txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


def store_on(x0mm):
    kabin_on(x0mm, WS, "STORE v6")
    x0, x1 = fx(x0mm), fx(x0mm + WS)
    d.rectangle([fx(x0mm + 30), fy(1968.5), fx(x0mm + WS - 30), fy(TEK0)], fill=SOFT, outline=LINE, width=2)
    txt((x0 + x1) / 2, (fy(1968.5) + fy(TEK0)) / 2, "TEKNİK BÖLME  ·  soğutma grupları · pano · çekmece sürücüleri", f8, GRAY, "mm")
    cx = x0mm + XI
    for ki, gruplar in enumerate(KOLON):
        if ki:
            bw = BOLME[ki - 1]
            d.rectangle([fx(cx - bw), fy(CELL1), fx(cx), fy(YUZ0)], fill=(INK if bw >= 60 else SOFT), outline=LINE, width=1)
        txt(fx(cx + WO / 2), (fy(CELL1) + fy(TEK0)) / 2, KOLON_AD[ki], f7, GRAY, "mm")
        y = YUZ0
        for g in gruplar:
            if g == "ayirici":
                yb = y + 3.0
                d.rectangle([fx(cx + 8), fy(yb + 42), fx(cx + WO - 8), fy(yb)], fill=INK)
                y = yb + 45.0
                continue
            adet, tip, zon = g
            h = HH[tip] + 2 * BIND
            ybas = y
            col = BUZ if zon == "-18" else DOLAP
            for _ in range(adet):
                d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=col, width=1)
                y += h + FUGA
            cap, br = CAP[tip]
            zt = "−18 °C" if zon == "-18" else "+3 °C"
            ikinci = ("%d %s · %s" % (adet * cap, br, zt)) if cap else ("%s paket · %s" % (br, zt))
            ym = (fy(ybas) + fy(y - FUGA)) / 2
            etiket(fx(cx + WO / 2), ym - 13, "%s × %d" % (AD[tip], adet), f8, INK, col)
            etiket(fx(cx + WO / 2), ym + 13, ikinci, f7, col, col)
        ust = y - FUGA
        if CELL1 - ust > 20:
            d.rectangle([fx(cx + 8), fy(CELL1), fx(cx + WO - 8), fy(ust)], fill=(250, 250, 251), outline=BOSL, width=1)
            tarali(fx(cx + 8) + 1, fy(CELL1) + 1, fx(cx + WO - 8) - 1, fy(ust) - 1)
        olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
        cx += WO + (BOLME[ki] if ki < len(BOLME) else 0.0)


x = 0.0
for ad, w, _ in ISTASYON:
    if ad.startswith("STORE"):
        store_on(x)
    else:
        istasyon_on(x, ad)
    olcu_h(fx(x), fx(x + w), fy(1970) - 26, sayi(w), f11, INK)
    x += w
olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
olcu_v(fx(0) - 44, fy(1970), fy(0), "1970", f11, INK, "l")

# ======================= UST GORUNUS (PLAN KESITI) =======================
txt(OX, PY_TOP - 150, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ", f16, ACC)
txt(fx(HAT / 2), py(-790) - 40, "ARKA", f9, GRAY, "mm")
x = 0.0
for ad, w, dz in ISTASYON:
    zb = 40.0 - dz
    d.rectangle([fx(x), py(zb), fx(x + w), py(40.0)], fill=FILL, outline=LINE, width=3)
    if ad.startswith("STORE"):
        for (a_, b_) in ((1.5, 61.5), (w - 61.5, w - 1.5)):
            d.rectangle([fx(x + a_), py(zb + 1.5), fx(x + b_), py(-16.0)], fill=PUC, outline=GRAY, width=1)
        d.rectangle([fx(x + 61.5), py(zb + 1.5), fx(x + w - 61.5), py(zb + 61.5)], fill=PUC, outline=GRAY, width=1)
        cx = x + XI
        for ki in range(len(KOLON)):
            if ki:
                bw = BOLME[ki - 1]
                d.rectangle([fx(cx - bw), py(-727.5), fx(cx), py(-16.0)], fill=(INK if bw >= 60 else SOFT), outline=LINE, width=1)
            d.rectangle([fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0)], fill=BG, outline=DOLAP, width=2)
            d.rectangle([fx(cx - 15), py(0.0), fx(cx + WO + 15), py(40.0)], fill=BG, outline=DOLAP, width=2)
            d.rectangle([fx(cx + 190), py(-725.0), fx(cx + 450), py(-680.0)], fill=EVC, outline=BUZ, width=1)
            d.rectangle([fx(cx + 17), py(-716.0), fx(cx + 67), py(-680.0)], fill=(255, 230, 230), outline=RED, width=1)
            txt(fx(cx + WO / 2), py(-420.0), "K%d" % (ki + 1), f11, GRAY, "mm")
            txt(fx(cx + WO / 2), py(-360.0), "ÇEKMECE 620 × 680", f8, INK, "mm")
            txt(fx(cx + 320), py(-702.5), "EVAPORATÖR", f7, BUZ, "mm")
            txt(fx(cx + 42), py(-698.0), "M", f7, RED, "mm")
            cx += WO + (BOLME[ki] if ki < len(BOLME) else 0.0)
        olcu_v(fx(x) - 44, py(zb), py(40.0), sayi(dz), f11, INK, "l")
    elif ad.startswith("TOPPING"):
        for xc in RAF_X["kat"]:
            d.rectangle([fx(x + xc - 70), py(-695.5), fx(x + xc + 70), py(-15.5)], fill=BG, outline=INK, width=2)
            txt(fx(x + xc), py(-400.0), "PLASTİK", f7, INK, "mm")
            txt(fx(x + xc), py(-372.0), "KASET", f7, INK, "mm")
            txt(fx(x + xc), py(-344.0), "140 × 680", f7, GRAY, "mm")
    elif ad.startswith("PRESS"):
        d.rectangle([fx(x + 29), py(-788.0), fx(x + 669), py(12.0)], fill=BG, outline=INK, width=2)
        txt(fx(x + 349), py(-403.0), "FERSAH PZP-400", f8, INK, "mm")
        txt(fx(x + 349), py(-373.0), "640 × 800", f7, GRAY, "mm")
    elif ad.startswith("OVEN"):
        d.rectangle([fx(x + 30), py(-600.0), fx(x + 670), py(-20.0)], fill=BG, outline=INK, width=2)
        txt(fx(x + 350), py(-325.0), "FIRIN · 3 HAZNE", f8, INK, "mm")
        txt(fx(x + 350), py(-295.0), "640 × 600 × 840", f7, GRAY, "mm")
    elif ad.startswith("PACK"):
        drect(fx(x + 150), py(-785.5), fx(x + 550), py(-25.5), GRAY, 1)
        txt(fx(x + 350), py(-610.0), "BLANK 400 × 760", f7, GRAY, "mm")
        d.rectangle([fx(x + 190), py(-410.0), fx(x + 510), py(-90.0)], fill=BG, outline=INK, width=2)
        txt(fx(x + 350), py(-265.0), "KUTU", f8, INK, "mm")
        txt(fx(x + 350), py(-235.0), "320 × 320", f7, GRAY, "mm")
    txt(fx(x + w / 2), py(40.0) + 30, "%s  ·  %s × %s" % (ad, sayi(w), sayi(dz)), f9, INK, "mm")
    x += w
olcu_h(fx(0), fx(HAT), py(40.0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
txt(fx(HAT / 2), py(40.0) + 150, "ÖN  ·  robot tarafı", f9, GRAY, "mm")


# ======================= YAN GORUNUS (STORE KESITI, K2) =======================
def sz(z):
    return SX + (z + 790.0) * S


txt(SX, FY_TOP - 150, "YAN GÖRÜNÜŞ", f16, ACC)
txt(SX, FY_TOP - 112, "STORE kesiti · K2 kolonu", f9, GRAY)
d.rectangle([sz(-790), fy(1970), sz(40), fy(0)], fill=FILL, outline=LINE, width=3)
d.rectangle([sz(-790), fy(120), sz(40), fy(0)], fill=SOFT, outline=LINE, width=2)                  # plint
d.rectangle([sz(-788.5), fy(TEK0), sz(-728.5), fy(121.5)], fill=PUC, outline=GRAY, width=1)        # arka PU 60
d.rectangle([sz(-727.5), fy(181.5), sz(0.0), fy(121.5)], fill=PUC, outline=GRAY, width=1)          # taban PU
d.rectangle([sz(-727.5), fy(1719.0), sz(0.0), fy(1661.0)], fill=PUC, outline=GRAY, width=1)        # tavan PU
d.rectangle([sz(-788.5), fy(1968.5), sz(38.5), fy(TEK0)], fill=SOFT, outline=LINE, width=2)        # teknik bolme
txt(sz(-375), (fy(1968.5) + fy(TEK0)) / 2, "TEKNİK BÖLME", f8, GRAY, "mm")
d.rectangle([sz(-727.5), fy(CELL1), sz(-680.0), fy(CELL0)], fill=(250, 250, 251), outline=GRAY, width=1)   # plenum
d.rectangle([sz(0.0), fy(TEK0), sz(40.0), fy(121.5)], fill=SOFT, outline=LINE, width=1)            # on sandvic
y0 = CELL0
for i in range(12):
    d.rectangle([sz(-680.0), fy(y0 + 88.0), sz(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
    d.rectangle([sz(0.0), fy(y0 + 88.0 + BIND), sz(40.0), fy(y0 - BIND)], fill=BG, outline=DOLAP, width=1)
    y0 += 88.0 + 2 * BIND + FUGA
txt(sz(-340), fy(915.0), "ÇEKMECE 680", f9, INK, "mm")
txt(sz(-340), fy(915.0) + 26, "LAHMACUN × 12", f7, DOLAP, "mm")
olcu_h(sz(-790), sz(-727.5), fy(1970) - 26, "62,5", f7, INK)
olcu_h(sz(-727.5), sz(-680), fy(1970) - 60, "47,5", f7, INK)
olcu_h(sz(-680), sz(0), fy(1970) - 26, "680", f9, INK)
olcu_h(sz(0), sz(40), fy(1970) - 60, "40", f7, INK)
olcu_h(sz(-790), sz(40), fy(0) + 44, "830", f11, INK)
txt(sz(-790), fy(0) + 84, "arka 62,5 = sac 1,5 + PU 60 + sac 1  ·  plenum 47,5  ·  ön 40", f7, GRAY, "la")
for yy in (120.0, CELL0, CELL1, TEK0, 1970.0):
    d.line([(sz(40) + 6, fy(yy)), (sz(40) + 24, fy(yy))], fill=INK, width=2)
    txt(sz(40) + 30, fy(yy), sayi(yy), f8, INK, "lm")

# ======================= LEJANT =======================
d.line([(OX, H_PX - 130), (W_PX - 170, H_PX - 130)], fill=LINE, width=2)
ly = H_PX - 78
LEJ = [(LINE, BG, "kapak / panel", False), (RED, AGZ, "açık ağız", False), (BUZ, BG, "çekmece −18 °C", False),
       (DOLAP, BG, "çekmece +3 °C", False), (INK, INK, "yalıtımlı bölme 65 / bant 42", False),
       (BOSL, (250, 250, 251), "boş band", False), (GRAY, PUC, "PU yalıtım", False), (INK, BG, "kapak arkası", True)]
xx = OX
for c, fl, a_, kes in LEJ:
    if kes:
        drect(xx, ly - 12, xx + 30, ly + 12, c, 2)
    else:
        d.rectangle([xx, ly - 12, xx + 30, ly + 12], fill=fl, outline=c, width=3)
    txt(xx + 42, ly, a_, f9, INK, "lm")
    xx += 42 + d.textlength(a_, font=f9) + 56
cek = sum(g[0] for K in KOLON for g in K if g != "ayirici")
txt(W_PX - 170, ly, "HAT %s × 1970 × 830  ·  STORE %d çekmece  ·  TOPPING 14 yuva, 12 plastik kaset  ·  OVEN 3 hazne" % (sayi(HAT), cek), f9, GRAY, "rm")

assert not os.path.exists(OUT), "v8 zaten var — yeni numara ver"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("yazildi:", OUT, "· hat %s mm · STORE %s mm · %d cekmece" % (sayi(HAT), sayi(WS), cek))
