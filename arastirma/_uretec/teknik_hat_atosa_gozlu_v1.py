# -*- coding: utf-8 -*-
"""AUTOKITCH · C SECENEGI · ATOSA TABLALI + 3 KAPAKLI GOZ · TEKNIK RESIM v1 (20 Eyl 2026)
Kemal 20 Eyl: kalan uc secenekten C. Konveyor firin yerine 3 kapakli goz; robot urunu tabladan kurekle alip
goze surer, pisince alip kesme plakasina birakir. Firin kolonu 650 mm oldugu icin K ve E 700 mm sola kaydi: HAT 4600.
Olculer 3D simden (otonom/sim3d_bant_tabla, ?hat=goz&goz=3): goz ici 360x360, ic yukseklik 100, govde 165,
3 goz 700-1195, tabla ucu 2560 (topping modulunun disinda), icecek cekmecesi K modulunde 3320-3880.
OLCULEN KAPASITE: 1 robot 31 iceceksiz / 26 icecekli · 2 robot 42 / 35 (tam yuk, 2. saat).
ESKI BASLIK:
Kemal: "bunu 3d sim olarak kurdurucam ama once son guncellemelerle o iki hattin teknik resmini ciz".
Onceki paftalar: HAT_BANTLI_v5_3gun (14 Eyl) · HAT_ATOSA_3GUN_v1 'TABLALI HAT v1' (14 Eyl).
SON GUNCELLEMELER (HAT 2 KOL v19'dan aynen): 830 derin · hat 2030 · her istasyon kapali urun · MODUL B (2500 x 1060:
20 contali motorlu cekmece 8 pide + 12 lahm, icecek + tatli 2 katli cekmece K3 ustu, K4 sogutma grubu + kasar/sucuk deposu,
K1 ustu B karti + suruculer) · PRES agzi asagida, motor ustte · 6 hazne tek sira (2 harc 280, kiyma, kusbasi, kasar kabi 280,
sucuk dilimleyici) · makinede ekran yok (tablet) · robot kontrol kutusu ray yaninda · yildiz bicak Ø300 6 dilim ·
kutu 320 x 320 x 45 · 2 gun stok · FR5 yer rayinda, omuz 970, ray ekseni hat yuzunden 360 · QR dolabi koridorun karsisinda.
BANTLI: A + B + C v19 ile ayni; robot agzi (1070-1180) yerine adimli bant (ust kot 1150 = pres alt plakasi).
TABLALI: B v19 ile ayni; ustunde tabla arabasi (ray 150 + damlama 30 + tabla bolmesi 250) -> hazne sirasi 290 yukari,
C teknik bandi yan bolmelere, ana pano + UPS F tabanina. Kotlar VARSAYIM (Atosa cevabi yok).
Kural: paftada yalniz gorunus + olcu + parca adi; aciklama mesajda.
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX, S = 6600, 3400, 0.56
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ, SICAK, TURUNCU, URUN = (253, 244, 243), (255, 226, 214), (200, 90, 30), (240, 214, 170)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(54, True)
im = d = None


def txt(x, y, s, f=None, c=INK, a="la"):
    d.text((x, y), s, font=f or f11, fill=c, anchor=a)


def satirlar(x, y, s, f, c, adim=20):
    ls = s.split("|")
    y0 = y - adim * (len(ls) - 1) / 2.0
    for i, l in enumerate(ls):
        txt(x, y0 + i * adim, l, f if i == 0 else f7, c if i == 0 else GRAY, "mm")


def sayi(v):
    return ("%g" % v).replace(".", ",")


def etiket(x, y, s, f=None, c=INK, cer=GRAY):
    f = f or f8
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw / 2 - 6, y - 11, x + tw / 2 + 6, y + 11], fill=BG, outline=cer, width=1)
    txt(x, y, s, f, c, "mm")


def olcu_h(x0, x1, y, s, f=None, c=INK):
    f = f or f11
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=None, c=INK, yon="r"):
    f = f or f11
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


def darc(cx, cy, r, a0, a1, c, w=2, adim=4.0):
    a = a0
    while a < a1:
        b = min(a1, a + adim)
        d.arc([cx - r, cy - r, cx + r, cy + r], a, b, fill=c, width=w)
        a = b + adim


# ======================= ORTAK VERI (HAT 2 KOL v19) =======================
DZ = 830.0
WO, BIND, FUGA, BOLME, XI = 620.0, 15.0, 3.0, 35.0, 62.5
YUZ0 = 167.5
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 241.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK + TATLI · 2 katlı çekmece"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · 2,6 gün")}
KOLON = [[(6, "hamur")], [(2, "hamur"), (6, "lahm")], [(6, "lahm"), (1, "icecek")]]
KOLON_AD = ("K1", "K2", "K3")
H_B, H_MAK = 1060.0, 2030.0
X_A, W_A, X_C, W_C, W_B = 0.0, 700.0, 700.0, 1800.0, 2500.0
X_F, W_F, X_K, W_K, X_E, W_E = 2500.0, 800.0, 3300.0, 600.0, 3900.0, 700.0   # C: firin kolonu 650 + servis payi
HAT = X_E + W_E                                              # 5300
GOZ_N, GOZ_H, GOZ_Y0 = 3, 165.0, 700.0                       # 3 kapakli goz · govde 165 · taban 700 -> ust 1195
GOZ_IC, GOZ_IC_H = 360.0, 100.0                              # goz ici 360 x 360 · ic yukseklik 100 (urun 25 + ust bosluk 75)
GOZ_X0, GOZ_X1 = 2600.0, 3250.0                              # goz kolonu (F modulunun icinde)
TABLA_UC = 2560.0                                            # tabla firin ucu: TOPPING modulunun (2500) disinda
PISME = {'pide': 240.0, 'lahmacun': 120.0}                   # her goze ayri isi ve sure
KOR, RZ, OMUZ, A2, A3 = 800.0, 360.0, 970.0, 425.0, 395.0    # koridor · ray ekseni · FR5 omuz kotu · kol boylari
ERISIM = 779.0                                               # FR5 pratik bilek erisimi (820 x 0,95)
RX = 2650.0                                                  # TEK ROBOT (Kemal 19 Eyl): cizimde hattin ortasinda gosterilir
QRX, QRZ = (HAT - 1005.0, HAT), (900.0, 1340.0)
QR_SATIR = (410.0, 610.0, 810.0, 1010.0, 1210.0, 1410.0)
YUVA19 = [("HARÇ", 280.0, 370.0), ("HARÇ", 280.0, 650.0), ("KIYMA", 140.0, 860.0), ("KUŞBAŞI", 140.0, 1000.0),
          ("KAŞAR KABI", 280.0, 1210.0), ("SUCUK|DİLİMLEYİCİ", 180.0, 1440.0)]

OX, FY_TOP = 300.0, 420.0
FY = FY_TOP + H_MAK * S
PY_TOP = FY + 360.0
SX1 = OX + HAT * S + 270.0
SEC_W = (790.0 + 1390.0) * S
SX2 = SX1 + SEC_W + 190.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 790.0) * S


def kabin(x0mm, w, y0, y1, ad=""):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
    if y0 == 0.0:
        d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)
    if ad:
        txt((x0 + x1) / 2, fy(H_MAK) - 64, ad, f13, INK, "md")


def kapak(x0mm, a, b, y0, y1, et="", yl=None, fill=None):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(fill or BG), outline=LINE, width=2)
    if et:
        satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)


def agiz(x0mm, a, b, y0, y1, et, kot=True):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
    cy = (fy(y0) + fy(y1)) / 2
    txt(fx(x0mm + (a + b) / 2), cy - (10 if kot else 0), et, f8, RED, "mm")
    if kot:
        txt(fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm")


def kesik(x0mm, a, b, y0, y1, et="", c=INK, alt=""):
    drect(fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0), c, 1)
    if et:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) - (8 if alt else 0), et, f7, c, "mm")
    if alt:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10, alt, f7, GRAY, "mm")


def modul_etiketi(x0mm, w, ad, olcu, renk=ACC, sira=0):
    x0, x1 = fx(x0mm) + 6, fx(x0mm + w) - 6
    yb = fy(0) + 126 + sira * 50
    d.rectangle([x0, yb, x1, yb + 46], fill=renk)
    txt((x0 + x1) / 2, yb + 14, ad, f8, BG, "mm")
    txt((x0 + x1) / 2, yb + 34, olcu, f7, BG, "mm")


# ======================= MODUL B (v19 ile ayni) =======================
def ciz_B(nis_etiket):
    kabin(X_A, W_B, 0.0, H_B)
    d.rectangle([fx(X_A + 30), fy(H_B - 60.0), fx(X_A + W_B - 30), fy(121.5)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_A + 30), fy(H_B - 1.5), fx(X_A + W_B - 30), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_A + W_B / 2), fy(H_B - 30.0), "tavan PU 60 · üstüne MODÜL A ve C oturur · çekmece önü 40 PU + conta · her çekmecede 24 V lineer motor 700 strok", f7, GRAY, "mm")
    cx = X_A + XI
    for ki, gruplar in enumerate(KOLON):
        if ki:
            d.rectangle([fx(cx - BOLME), fy(H_B - 60.0), fx(cx), fy(YUZ0 - BIND)], fill=SOFT, outline=LINE, width=1)
        y = YUZ0
        for adet, tip in gruplar:
            h = HH[tip] + 2 * BIND
            ybas = y
            for _ in range(adet):
                d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=(2 if tip == "icecek" else 1))
                if tip == "icecek":
                    d.line([(fx(cx + 8), fy(y + h / 2)), (fx(cx + WO - 8), fy(y + h / 2))], fill=DOLAP, width=2)
                y += h + FUGA
            cap, br = CAP[tip]
            ym = (fy(ybas) + fy(y - FUGA)) / 2
            etiket(fx(cx + WO / 2), ym - 13, ("%s × %d" % (AD[tip], adet)) if cap else AD[tip], f8, INK, DOLAP)
            etiket(fx(cx + WO / 2), ym + 13, ("%d %s · +3 °C" % (adet * cap, br)) if cap else (br + " · +3 °C"), f7, DOLAP, DOLAP)
        txt(fx(cx + WO / 2), fy(H_B - 60.0) + 14, KOLON_AD[ki], f7, GRAY, "mm")
        olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
        cx += WO + BOLME
    K4X, K4W = cx, 400.0
    d.rectangle([fx(K4X - BOLME), fy(H_B - 60.0), fx(K4X), fy(YUZ0 - BIND)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(K4X), fy(H_B - 60.0), fx(K4X + K4W), fy(121.5)], fill=BG, outline=LINE, width=2)
    kapak(X_A, K4X - X_A + 8.0, K4X - X_A + K4W - 8.0, 130.0, 368.0)
    kesik(X_A, K4X - X_A + 20.0, K4X - X_A + K4W - 20.0, 140.0, 360.0, "SOĞUTMA GRUBU", INK, "400 × 300 × 220 · ⅓ HP")
    d.rectangle([fx(K4X + 8), fy(675.0), fx(K4X + K4W - 8), fy(375.0)], fill=BG, outline=DOLAP, width=3)
    satirlar(fx(K4X + K4W / 2), fy(525.0), "KAŞAR + SUCUK|DEPOSU · kapaklı · +3 °C|400 × 830 × 300 · 4 gün", f8, INK, 19)
    kapak(X_A, K4X - X_A + 8.0, K4X - X_A + K4W - 8.0, 690.0, 995.0, nis_etiket)
    K1X = X_A + XI
    d.rectangle([fx(K1X + 8), fy(995.0), fx(K1X + WO - 8), fy(815.5)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(K1X + 8), fy(855.5), fx(K1X + WO - 8), fy(815.5)], fill=PUC, outline=GRAY, width=1)
    txt(fx(K1X + WO / 2), fy(835.5), "PU 40 · üstü kuru teknik bölme", f7, GRAY, "mm")
    kesik(X_A, K1X - X_A + 60.0, K1X - X_A + 260.0, 880.0, 965.0, "B KARTI", INK)
    kesik(X_A, K1X - X_A + 300.0, K1X - X_A + 560.0, 880.0, 965.0, "20 MOTOR", INK, "SÜRÜCÜSÜ")
    olcu_h(fx(K4X), fx(K4X + K4W), fy(0) + 44, "400", f8, GRAY)
    d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)
    modul_etiketi(X_A, W_B, "MODÜL B · ÇEKMECE MODÜLÜ · 8 pide + 12 lahmacun + içecek/tatlı 2 katlı çekmece (K3 üstü) · K4: soğutma grubu + kaşar/sucuk deposu · K1 üstü: B kartı + sürücüler · HAT 2 KOL v19 ile aynı",
                  "2500 × 830 × 1060", DOLAP, 1)


# ======================= FIRIN · KESME · KUTU (iki hatta ortak, kot P'ye gore) =======================
def ciz_F(P, taban_parcalar):
    """C SECENEGI · 3 KAPAKLI GOZ · robot urunu kurekle goze surer, pisince alir."""
    kabin(X_F, W_F, 0.0, H_MAK, "F · 3 KAPAKLI GÖZ FIRIN · özel · elektrikli")
    gx0, gx1 = GOZ_X0 - X_F, GOZ_X1 - X_F                     # modul icindeki goz kolonu
    kapak(X_F, 33.0, W_F - 33.0, 123.0, GOZ_Y0 - 60.0)
    for a, b, y0, y1, et, alt in taban_parcalar:
        kesik(X_F, a, b, y0, y1, et, INK, alt)
    # govde
    d.rectangle([fx(X_F + gx0 - 40), fy(GOZ_Y0 + GOZ_N * GOZ_H + 60.0), fx(X_F + gx1 + 40), fy(GOZ_Y0 - 50.0)],
                fill=PUC, outline=LINE, width=3)
    tarali(fx(X_F + gx0 - 40), fy(GOZ_Y0 + GOZ_N * GOZ_H + 60.0), fx(X_F + gx1 + 40), fy(GOZ_Y0 - 50.0), (226, 214, 190), 11)
    for g in range(GOZ_N):
        y0 = GOZ_Y0 + g * GOZ_H
        y1 = y0 + GOZ_H
        # sicak hacim + tas
        d.rectangle([fx(X_F + gx0), fy(y1 - 20.0), fx(X_F + gx1), fy(y0 + 20.0)], fill=SICAK, outline=TURUNCU, width=2)
        d.rectangle([fx(X_F + gx0 + 10), fy(y0 + 52.0), fx(X_F + gx1 - 10), fy(y0 + 22.0)], fill=(198, 166, 122), outline=(150, 118, 80), width=1)
        txt(fx(X_F + (gx0 + gx1) / 2), fy(y0 + 34.0), "pişirme taşı 30", f7, INK, "mm")
        # urun
        d.ellipse([fx(X_F + (gx0 + gx1) / 2 - 150), fy(y0 + 78.0), fx(X_F + (gx0 + gx1) / 2 + 150), fy(y0 + 54.0)],
                  fill=URUN, outline=(180, 140, 70), width=1)
        # giyotin kapak
        d.rectangle([fx(X_F + gx0 - 34), fy(y1 - 8.0), fx(X_F + gx1 + 34), fy(y1 - 26.0)], fill=BG, outline=RED, width=2)
        txt(fx(X_F + gx1 + 46), fy(y0 + GOZ_H / 2), "GÖZ %d · kot %s–%s" % (g + 1, sayi(y0), sayi(y1)), f7, INK, "lm")
        olcu_v(fx(X_F + gx0) - 22, fy(y1), fy(y0), sayi(GOZ_H), f7, GRAY, "l")
    ust = GOZ_Y0 + GOZ_N * GOZ_H
    txt(fx(X_F + (gx0 + gx1) / 2), fy(GOZ_Y0 - 32.0),
        "GÖZ İÇİ %s × %s · iç yükseklik %s (ürün 25 + üst boşluk 75) · gövde %s · giyotin kapak" % (sayi(GOZ_IC), sayi(GOZ_IC), sayi(GOZ_IC_H), sayi(GOZ_H)), f7, TURUNCU, "mm")
    txt(fx(X_F + (gx0 + gx1) / 2), fy(ust + 26.0),
        "her göze AYRI ısı ve süre · pide %d s · lahmacun %d s · tavan 3 × 3600 / 143 ≈ 90 ürün/saat" % (PISME["pide"], PISME["lahmacun"]), f7, TURUNCU, "mm")
    kapak(X_F, 33.0, W_F - 33.0, ust + 70.0, 2028.0, "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre|fırın kartı + SSR + kontaktör (F'nin kendi panosu) · ~12 kW (tahmin)")
    olcu_h(fx(X_F + gx0), fx(X_F + gx1), fy(ust + 60.0), "GÖZ KOLONU %s" % sayi(GOZ_X1 - GOZ_X0), f8, TURUNCU)
    modul_etiketi(X_F, W_F, "MODÜL F · 3 KAPAKLI GÖZ", "%s × 830 × 2030 · gözler %s–%s · robot kürekle koyar/alır" % (sayi(W_F), sayi(GOZ_Y0), sayi(ust)))
    olcu_h(fx(X_F), fx(X_F + W_F), fy(H_MAK) - 26, sayi(W_F), f11, INK)


def ciz_K(P):
    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME · SPREY")
    kapak(X_K, 33.0, W_K - 33.0, 123.0, P - 60.0)
    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")
    d.rectangle([fx(X_K + 20), fy(P), fx(X_K + W_K - 20), fy(P - 14.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_K + W_K / 2), fy(P - 34.0), "KESME PLAKASI 560 × 450 · kot %s" % sayi(P), f7, BUZ, "mm")
    d.rectangle([fx(X_K + 24), fy(P + 50.0), fx(X_K + 64), fy(P + 2.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_K + 44), fy(P + 66.0), "İTİCİ", f7, INK, "mm")
    kesik(X_K, 110.0, 490.0, P + 90.0, P + 340.0, "YILDIZ BIÇAK Ø300 · 6 dilim", INK, "piston 100 strok")
    d.ellipse([fx(X_K + 520) - 6, fy(P + 120.0) - 6, fx(X_K + 520) + 6, fy(P + 120.0) + 6], fill=RED)
    txt(fx(X_K + 520), fy(P + 150.0), "SPREY", f7, RED, "mm")
    kapak(X_K, 33.0, W_K - 33.0, P + 355.0, 2028.0, "BOŞ")
    modul_etiketi(X_K, W_K, "MODÜL K · KESME", "600 × 830 × 2030")
    olcu_h(fx(X_K), fx(X_K + W_K), fy(H_MAK) - 26, sayi(W_K), f11, INK)


def ciz_E(P):
    a0, a1 = P - 90.0, P + 160.0                                # sim ile ayni: kutu tepsisi yuzu P-60, kutu ustu P-10
    m0, m1 = 123.0, a0 - 10.0
    kabin(X_E, W_E, 0.0, H_MAK, "E · KUTU KATLAYAN")
    kapak(X_E, 33.0, W_E - 33.0, m0, m1)
    kesik(X_E, 150.0, 550.0, m0 + 20.0, m1 - 20.0, "", INK)
    n = int((m1 - m0 - 60.0) // 80)
    for i in range(n):
        yy = m0 + 50.0 + i * 80.0
        d.line([(fx(X_E + 160), fy(yy)), (fx(X_E + 540), fy(yy))], fill=BOSL, width=1)
    yig = m1 - m0 - 40.0
    satirlar(fx(X_E + 350), fy((m0 + m1) / 2), "KUTU ŞARJÖRÜ · alttan kaldırmalı|blank 400 × 760 yatay yığın · %s mm|= %d (1,8 mm) – %d (1,5 mm) kutu · 2 gün 560" % (sayi(yig), int(yig / 1.8), int(yig / 1.5)), f8, INK)
    agiz(X_E, 30.0, W_E - 30.0, a0, a1, "KUTULAMA AĞZI · kutu 320 × 320 × 45")
    txt(fx(X_E + W_E / 2), (fy(a0) + fy(a1)) / 2 + 34, "kutu tepsisi dolum konumunda bekler (yüzü %s · z −270) · açık kutu üstünde dolar, kapanır" % sayi(P - 60.0), f7, RED, "mm")
    kapak(X_E, 33.0, W_E - 33.0, a1 + 10.0, 2028.0)
    ust = a1 + 10.0
    kesik(X_E, 60.0, 400.0, ust + 20.0, min(ust + 320.0, 2010.0), "KALIP + PLUNGER · vantuz", INK, "strok 250")
    kesik(X_E, 420.0, 640.0, ust + 20.0, ust + 160.0, "VAKUM POMPASI", INK)
    kesik(X_E, 420.0, 640.0, ust + 175.0, min(ust + 320.0, 2010.0), "E KONTROL KARTI", INK, "tahrik")
    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KOLONU", "700 × 830 × 2030 · ağız %s–%s" % (sayi(a0), sayi(a1)))
    olcu_h(fx(X_E), fx(X_E + W_E), fy(H_MAK) - 26, sayi(W_E), f11, INK)
    return a0, a1, yig


# ======================= PLAN · ORTAK =======================
def plan_ortak(P, mod):
    txt(OX, PY_TOP - 110, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  ray, robotlar, QR dolabı", f16, ACC)
    txt(fx(HAT / 2), py(-790) - 30, "ARKA", f9, GRAY, "mm")
    zb = 40.0 - DZ
    for x0m, w, ad in ((X_A, W_A, "A · PRESS (B üstünde)"), (X_C, W_C, "C · TOPPING (B üstünde)"), (X_F, W_F, "F · 3 KAPAKLI GÖZ"), (X_K, W_K, "K · KESME"), (X_E, W_E, "E · KUTU")):
        d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)
        txt(fx(x0m + w / 2), py(40.0) + 26, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f8, INK, "mm")
    # A
    d.rectangle([fx(X_A + 29), py(-788.0), fx(X_A + 669), py(12.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_A + 350), py(-745.0), "FERSAH PZP-400 · 640 × 800", f8, INK, "mm")
    # B cekmeceler (kesik)
    cx = X_A + XI
    for ki in range(3):
        drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
        txt(fx(cx + WO / 2), py(-20.0) - 6, "K%d · 620 × 680 · altta (B)" % (ki + 1), f7, DOLAP, "mm")
        cx += WO + BOLME
    drect(fx(cx + 8), py(-788.0), fx(cx + 392), py(0.0), DOLAP, 1)
    txt(fx(cx + 200), py(-20.0) - 6, "K4 · depo · altta (B)", f7, DOLAP, "mm")
    # F · 3 kapakli goz (plan: gozler ust uste oldugu icin planda tek kolon gorunur)
    d.rectangle([fx(X_F + 3), py(-788.0), fx(X_F + W_F - 3), py(38.0)], fill=PUC, outline=LINE, width=1)
    tarali(fx(X_F + 3), py(-788.0), fx(X_F + W_F - 3), py(38.0), (226, 214, 190), 11)
    d.rectangle([fx(GOZ_X0), py(-700.0), fx(GOZ_X1), py(-540.0)], fill=SICAK, outline=TURUNCU, width=2)
    txt(fx((GOZ_X0 + GOZ_X1) / 2), py(-620.0), "ARKA PLENUM 160", f7, TURUNCU, "mm")
    d.rectangle([fx(GOZ_X0), py(-540.0), fx(GOZ_X1), py(-170.0)], fill=SICAK, outline=TURUNCU, width=2)
    d.ellipse([fx((GOZ_X0 + GOZ_X1) / 2 - 150), py(-505.0), fx((GOZ_X0 + GOZ_X1) / 2 + 150), py(-205.0)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx((GOZ_X0 + GOZ_X1) / 2), py(-355.0), "Ø300", f7, (140, 100, 40), "mm")
    txt(fx((GOZ_X0 + GOZ_X1) / 2), py(-140.0), "GÖZ AĞZI · robot küreği buradan girer", f7, RED, "mm")
    txt(fx(X_F + W_F / 2), py(-45.0), "derinlik: ön duvar 60 + göz içi 360 + izolasyon + plenum 160 + arka duvar 60 = 830", f7, TURUNCU, "mm")
    olcu_h(fx(GOZ_X0), fx(GOZ_X1), py(-790) - 58, "GÖZ KOLONU %s · 3 göz üst üste" % sayi(GOZ_X1 - GOZ_X0), f8, TURUNCU)
    # K
    d.rectangle([fx(X_K + 20), py(-495.0), fx(X_K + 580), py(-45.0)], fill=EVC, outline=BUZ, width=2)
    d.ellipse([fx(X_K + 300 - 150), py(-420.0), fx(X_K + 300 + 150), py(-120.0)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - 150 * S * math.cos(a), py(-270.0) - 150 * S * math.sin(a)), (fx(X_K + 300) + 150 * S * math.cos(a), py(-270.0) + 150 * S * math.sin(a))], fill=INK, width=1)
    txt(fx(X_K + 300), py(-540.0), "KESME PLAKASI 560 × 450 · yıldız bıçak Ø300", f7, BUZ, "mm")
    d.rectangle([fx(X_K + 26), py(-310.0), fx(X_K + 62), py(-230.0)], fill=BG, outline=INK, width=2)
    d.line([(fx(X_K + 470), py(-270.0)), (fx(X_E + 170), py(-270.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 170), py(-270.0)), (fx(X_E + 150), py(-270.0) - 7), (fx(X_E + 150), py(-270.0) + 7)], fill=INK)
    # E
    drect(fx(X_E + 150), py(-785.5), fx(X_E + 550), py(-25.5), GRAY, 1)
    txt(fx(X_E + 350), py(-700.0), "BLANK 400 × 760 · altta", f7, GRAY, "mm")
    d.rectangle([fx(X_E + 190), py(-430.0), fx(X_E + 510), py(-110.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_E + 350), py(-285.0), "KUTU", f8, INK, "mm")
    txt(fx(X_E + 350), py(-258.0), "320 × 320 × 45", f7, GRAY, "mm")
    # olcu + koridor + ray + robotlar + QR
    olcu_h(fx(0), fx(HAT), py(QRZ[1]) + 118, "HAT  %s" % sayi(HAT), f13, INK)
    olcu_v(fx(0) - 44, py(-790), py(40.0), sayi(DZ), f11, INK, "l")
    olcu_v(fx(0) - 44, py(40.0), py(40.0 + KOR), "koridor %s" % sayi(KOR), f8, GRAY, "l")
    d.line([(fx(-60), py(40.0 + KOR)), (fx(HAT + 60), py(40.0 + KOR))], fill=GRAY, width=1)
    d.rectangle([fx(200.0 - 200), py(RZ - 60), fx(HAT - 200.0 + 200), py(RZ + 60)], fill=SOFT, outline=LINE, width=1)
    d.line([(fx(200.0), py(RZ)), (fx(HAT - 200.0), py(RZ))], fill=ACC, width=2)
    txt(fx(1250.0), py(RZ) + 0, "YER RAYI · ekseni hat yüzünden %s · araba merkezi x 200 – %s" % (sayi(RZ), sayi(HAT - 200.0)), f7, ACC, "mm")
    for rx, ad, alt in ((RX, "R · FR5 · TEK ROBOT", "hamur: çekmece → pres · kutu → QR · içecek + tatlı"),):
        cxp, cyp = fx(rx), py(RZ)
        d.rectangle([fx(rx - 200), py(RZ - 200), fx(rx + 200), py(RZ + 200)], fill=BG, outline=ACC, width=2)
        d.ellipse([cxp - 75 * S, cyp - 75 * S, cxp + 75 * S, cyp + 75 * S], fill=BG, outline=ACC, width=3)
        darc(cxp, cyp, ERISIM * S, 0.0, 360.0, ACC, 2, 3.0)
        txt(cxp, py(RZ + 200) + 18, ad + " · araba 400 × 400", f8, ACC, "mm")
        txt(cxp, py(RZ + 200) + 38, alt, f7, GRAY, "mm")
    txt(fx(0) - 50, py(40.0 + KOR) + 24, "kesik daire: FR5 pratik bilek erişimi %s (820 × 0,95)" % sayi(ERISIM), f7, ACC, "la")
    d.rectangle([fx(QRX[0]), py(QRZ[0]), fx(QRX[1]), py(QRZ[1])], fill=FILL, outline=LINE, width=3)
    for k0 in (QRX[0] + 15.0, QRX[0] + 515.0):
        d.rectangle([fx(k0), py(QRZ[0]), fx(k0 + 480.0), py(QRZ[0] + 440.0)], fill=EVC, outline=BUZ, width=1)
    txt(fx((QRX[0] + QRX[1]) / 2), py((QRZ[0] + QRZ[1]) / 2) - 10, "QR DOLABI · 2 × 6 göz · göz 480 × 190 × 440", f8, INK, "mm")
    txt(fx((QRX[0] + QRX[1]) / 2), py((QRZ[0] + QRZ[1]) / 2) + 12, "robot yüzü z %s · müşteri arkadan alır" % sayi(QRZ[0]), f7, GRAY, "mm")
    olcu_h(fx(QRX[0]), fx(QRX[1]), py(QRZ[1]) + 40, "1005", f8, GRAY)
    txt(fx(HAT / 2), py(QRZ[1]) + 74, "ÖN · robot koridoru · tek robot rayın tamamını kullanır", f9, GRAY, "mm")


# ======================= KESITLER =======================
def sec(sx):
    return lambda v: sx + (v + 790.0) * S


def govde(z, h0, h1, plint=False):
    d.rectangle([z(-790), fy(h1), z(40), fy(h0)], fill=FILL, outline=LINE, width=4)
    if plint:
        d.rectangle([z(-790), fy(120), z(40), fy(0)], fill=SOFT, outline=LINE, width=2)


def robot_kesit(z, wz, wy, tz, ty, ad):
    """ray + araba + FR5 (omuz 970) · bilek (wz,wy) · uc (tz,ty)"""
    d.rectangle([z(RZ - 200), fy(60), z(RZ + 200), fy(0)], fill=SOFT, outline=LINE, width=2)
    d.rectangle([z(RZ - 110), fy(OMUZ - 120.0), z(RZ + 110), fy(60)], fill=BG, outline=ACC, width=2)
    txt(z(RZ), fy(420.0), "KAİDE", f7, ACC, "mm")
    dz, dy = wz - RZ, wy - OMUZ
    D = math.hypot(dz, dy)
    Dk = min(D, A2 + A3 - 1.0)
    th = math.atan2(dy, dz)
    al = math.acos(max(-1.0, min(1.0, (A2 * A2 + Dk * Dk - A3 * A3) / (2 * A2 * Dk))))
    cand = [(RZ + A2 * math.cos(th + s * al), OMUZ + A2 * math.sin(th + s * al)) for s in (1.0, -1.0)]
    ez, ey = max(cand, key=lambda p: p[1])                     # dirsek yukari
    d.line([(z(RZ), fy(OMUZ)), (z(ez), fy(ey))], fill=ACC, width=9)
    d.line([(z(ez), fy(ey)), (z(wz), fy(wy))], fill=ACC, width=7)
    d.line([(z(wz), fy(wy)), (z(tz), fy(ty))], fill=INK, width=5)
    for pz, pyy, r in ((RZ, OMUZ, 11), (ez, ey, 9), (wz, wy, 8)):
        d.ellipse([z(pz) - r, fy(pyy) - r, z(pz) + r, fy(pyy) + r], fill=BG, outline=ACC, width=3)
    txt(z(RZ) + 16, fy(OMUZ) + 22, "omuz %s" % sayi(OMUZ), f7, ACC, "la")
    txt(z(ez), fy(ey) - 22, "%s · bilek mesafesi %d / %d" % (ad, round(D), round(ERISIM)), f7, ACC, "mm")
    d.line([(z(40), fy(0)), (z(1390), fy(0))], fill=INK, width=3)
    olcu_h(z(40), z(RZ), fy(0) + 44, sayi(RZ - 40.0) + " + 40", f8, ACC)
    olcu_h(z(-790), z(40), fy(0) + 44, "830", f11, INK)
    return D


def cekmeceler(z, gruplar, y0):
    for adet, tip in gruplar:
        h = HH[tip] + 2 * BIND
        for _ in range(adet):
            d.rectangle([z(-680.0), fy(y0 + h), z(0.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
            d.rectangle([z(0.0), fy(y0 + h), z(40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
            d.line([(z(2.0), fy(y0 + 6.0)), (z(2.0), fy(y0 + h - 6.0))], fill=RED, width=2)
            d.rectangle([z(-760.0), fy(y0 + h / 2 + 10.0), z(-690.0), fy(y0 + h / 2 - 10.0)], fill=(255, 230, 230), outline=RED, width=1)
            y0 += h + FUGA
    return y0


def kesit_E(P, a0, a1):
    z = sec(SX2)
    txt(SX2, FY_TOP - 200, "KESİT 2 · E + ROBOT + QR DOLABI", f16, ACC)
    txt(SX2, FY_TOP - 162, "Robot kapalı kutuyu tepsiyle alır, 180° dönüp QR gözüne koyar, tepsiyi ağza geri bırakır", f9, GRAY)
    govde(z, 0.0, H_MAK, True)
    d.rectangle([z(-785.5), fy(a0 - 30.0), z(-25.5), fy(143.0)], fill=BG, outline=GRAY, width=1)
    txt(z(-405.0), fy((143.0 + a0) / 2), "KUTU ŞARJÖRÜ · blank 760 derin", f7, GRAY, "mm")
    d.rectangle([z(-10.0), fy(a1), z(40.0), fy(a0)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(a1) - 14, "KUTULAMA AĞZI %s–%s" % (sayi(a0), sayi(a1)), f7, RED, "rm")
    d.rectangle([z(-430.0), fy(P - 10.0), z(-110.0), fy(P - 55.0)], fill=BG, outline=INK, width=2)
    txt(z(-270.0), fy(P - 32.0), "kutu 320 × 45", f7, INK, "mm")
    d.rectangle([z(-760.0), fy(2010.0), z(10.0), fy(a1 + 30.0)], fill=BG, outline=GRAY, width=1)
    txt(z(-375.0), fy((a1 + 2040.0) / 2), "KALIP + PLUNGER · vakum · E kartı", f7, GRAY, "mm")
    ty = P - 60.0
    D = robot_kesit(z, 230.0, ty + 20.0, -270.0, ty, "ROBOT")
    d.line([(z(-440.0), fy(ty)), (z(-100.0), fy(ty))], fill=ACC, width=4)
    d.line([(z(-100.0), fy(ty + 20.0)), (z(50.0), fy(ty + 20.0))], fill=ACC, width=3)
    txt(z(-270.0), fy(ty) + 16, "kutu tepsisi Ø340 · yüzü %s · z −270 · sapı öne bakar" % sayi(ty), f7, ACC, "mm")
    d.rectangle([z(QRZ[0]), fy(2000.0), z(QRZ[1]), fy(0.0)], fill=FILL, outline=LINE, width=4)
    for yy in QR_SATIR:
        d.rectangle([z(QRZ[0]), fy(yy + 190.0), z(QRZ[0] + 440.0), fy(yy)], fill=EVC, outline=BUZ, width=1)
        txt(z(QRZ[0] + 220.0), fy(yy + 95.0), "göz · y %s" % sayi(yy), f7, BUZ, "mm")
    txt(z((QRZ[0] + QRZ[1]) / 2), fy(2000.0) - 16, "QR DOLABI · 6 satır", f8, INK, "mm")
    olcu_h(z(40), z(QRZ[0]), fy(0) + 84, "koridor + pay %s" % sayi(QRZ[0] - 40.0), f8, GRAY)
    for yy in (120.0, a0, a1, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    return D


def parca_listesi(satirlar_):
    x0, y0 = SX1, PY_TOP - 60.0
    txt(x0, y0 - 46, "MODÜLLER (lego · cıvatalı flanşla birleşir)  ·  PARÇA LİSTESİ", f16, ACC)
    kol = (0, 250, 1560, 1660)
    gen = 2860
    d.rectangle([x0, y0, x0 + gen, y0 + 30], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
        txt(x0 + k + 10, y0 + 15, b, f7, INK, "lm")
    y = y0 + 30
    for r in satirlar_:
        d.line([(x0, y + 34), (x0 + gen, y + 34)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            txt(x0 + k + 10, y + 17, v, f7, INK if k < 1560 else GRAY, "lm")
        y += 34
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)


def lejant():
    y = H_PX - 110
    d.line([(OX, y - 40), (W_PX - 170, y - 40)], fill=LINE, width=2)
    x = OX
    for fill, out, ad, kes in ((BG, LINE, "kapak / panel", False), (AGZ, RED, "açık ağız · robot girer", False), (BG, DOLAP, "çekmece +3 °C", False),
                               (SICAK, TURUNCU, "pişirme haznesi / sıcak hava", False), (PUC, GRAY, "PU · taşyünü yalıtım", False), (EVC, BUZ, "bant · tabla · plaka", False),
                               (BG, INK, "kapak arkası parça", True), (BG, ACC, "robot · ray", False)):
        if kes:
            drect(x, y - 12, x + 30, y + 12, out, 1)
        else:
            d.rectangle([x, y - 12, x + 30, y + 12], fill=fill, outline=out, width=2)
        txt(x + 42, y, ad, f8, INK, "lm")
        x += 70 + d.textlength(ad, font=f8) + 40


def kot_cizgileri(kotlar):
    olcu_v(fx(0) - 52, fy(H_MAK), fy(0), sayi(H_MAK), f11, INK, "l")
    for yy in kotlar:
        d.line([(fx(HAT) + 8, fy(yy)), (fx(HAT) + 26, fy(yy))], fill=INK, width=2)
        txt(fx(HAT) + 32, fy(yy), sayi(yy), f7, INK, "lm")


def birlesimler():
    for xj, et, yb in ((X_C, "A | C", H_B), (X_F, "B·C | F", 0.0), (X_K, "F | K", 0.0), (X_E, "K | E", 0.0)):
        dline((fx(xj), fy(H_MAK) - 12), (fx(xj), fy(yb) + 12), ACC, 3, 10, 6)
        txt(fx(xj), fy(H_MAK) - 122, "BİRLEŞİM", f7, ACC, "mm")
        txt(fx(xj), fy(H_MAK) - 106, et, f7, GRAY, "mm")
    for rx, ad in ((RX, "R · FR5 · TEK ROBOT"),):
        d.polygon([(fx(rx), fy(0) + 4), (fx(rx) - 14, fy(0) + 30), (fx(rx) + 14, fy(0) + 30)], fill=ACC)
        txt(fx(rx), fy(0) + 66, ad + " · koridorda, rayda · z +%s" % sayi(RZ), f8, ACC, "mm")
    olcu_h(fx(0), fx(HAT), fy(0) + 96, "HAT  %s" % sayi(HAT), f13, INK)
    txt(fx(0) - 12, fy(0) + 149, "ÜST", f8, ACC, "rm")
    txt(fx(0) - 12, fy(0) + 199, "ALT", f8, ACC, "rm")


def baslik(ad, alt):
    txt(OX, 70, ad, f38, INK)
    txt(OX, 140, alt, f13, GRAY)
    d.line([(OX, 182), (W_PX - 170, 182)], fill=LINE, width=3)
    txt(OX, FY_TOP - 200, "ÖN GÖRÜNÜŞ", f16, ACC)
    txt(OX, FY_TOP - 162, "kesik çizgi = kapak arkası parça · robotlar koridorda önde, konumları zeminde işaretli", f9, GRAY)


# =====================================================================
#                               BANTLI HAT v6
# =====================================================================
def gozlu():
    global im, d
    im = Image.new("RGB", (W_PX, H_PX), BG); d = ImageDraw.Draw(im)
    RAY_T, DAM, BOLM = (1060.0, 1210.0), (1210.0, 1240.0), (1240.0, 1490.0)
    P = 1340.0                                               # tabla seyir kotu = firin bandi = kesme plakasi
    T_BAS, T_KAS, T_KPK = (1490.0, 1624.0), (1627.0, 1987.0), (1987.0, 2027.0)
    YUVA = [(u, g, x - 30.0) for u, g, x in YUVA19]           # hazne sirasi 200–1500 → sagda 267'lik teknik bolme
    baslik("AUTOKITCH  ·  C SEÇENEĞİ  ·  ROBOT KOLLU  ·  ATOSA TABLASI + 3 KAPAKLI GÖZ  ·  TEKNİK RESİM  v1  ·  HAT 4600 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  ürün tepsisiz: tabla üstünde basılır ve dozajlanır, ROBOT KÜREKLE ALIP GÖZE SÜRER, pişince alıp kesme plakasına bırakır → bıçak · sprey · itici · kutu  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  ölçülen kapasite 31 ürün/saat içeceksiz · 26 içecekli (tam yük, 2. saat)  ·  tabla kotları VARSAYIM (Atosa cevabı yok)  ·  ölçüler mm  ·  20 Eylül 2026")
    # A
    kabin(X_A, W_A, H_B, H_MAK, "A · PRES KAFASI · tabla üstüne basar")
    kapak(X_A, 33.0, 667.0, H_B + 3.0, 2010.0)
    kesik(X_A, 180.0, 520.0, RAY_T[1] + 10.0, P - 14.0, "SABİT ÖRS", INK, "pres kuvveti örste")
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot tablaya bırakır")
    kesik(X_A, 205.0, 495.0, P + 225.0, P + 275.0, "üst plaka Ø290", INK)
    kesik(X_A, 40.0, 660.0, P + 280.0, 2005.0, "PRES KAFASI · MOTOR ÜSTTE", INK, "Fersah PZP-400 uyarlaması · alt tabla yerine örs")
    modul_etiketi(X_A, W_A, "MODÜL A · PRES KAFASI", "700 × 830 × 970 · B üstünde")
    olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)
    ciz_B("YEDEK BÖLME|385 × 305 · boş")
    # C
    kabin(X_C, W_C, H_B, H_MAK, "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · TABLALI")
    d.rectangle([fx(X_A + 33), fy(RAY_T[1]), fx(X_C + W_C - 33), fy(RAY_T[0] + 3.0)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_A + 90), fy(RAY_T[0] + 60.0), fx(X_C + W_C - 40), fy(RAY_T[0] + 25.0)], fill=ACC, outline=ACC)
    txt(fx(X_C + 760), fy(RAY_T[0] + 105.0), "TABLA RAYI + ARABA 150 · x kızak · kaldırma · döndürme · pres altından robot alma noktasına (x 90 – %s)" % sayi(TABLA_UC), f7, ACC, "mm")
    d.rectangle([fx(X_C + 33), fy(DAM[1]), fx(X_C + W_C - 33), fy(DAM[0])], fill=SOFT, outline=LINE, width=1)
    txt(fx(X_C + W_C / 2), fy((DAM[0] + DAM[1]) / 2), "DAMLAMA TAVASI 30 · çekmece, günlük yıkanır", f7, GRAY, "mm")
    d.rectangle([fx(X_C + 33), fy(BOLM[1]), fx(X_C + W_C - 33), fy(BOLM[0])], fill=BG, outline=LINE, width=2)
    txt(fx(X_C + 420), fy(BOLM[0] + 125.0), "TABLA BÖLMESİ 250 · önü kapaklı", f7, INK, "mm")
    for xt, kes_ in ((X_A + 350.0, False), (X_C + YUVA[4][2], True), (X_C + W_C - 170.0, True)):
        yt = P
        if kes_:
            drect(fx(xt - 170), fy(yt), fx(xt + 170), fy(yt - 12.0), BUZ, 2)
        else:
            d.rectangle([fx(xt - 170), fy(yt), fx(xt + 170), fy(yt - 12.0)], fill=EVC, outline=BUZ, width=2)
        d.line([(fx(xt), fy(yt - 12.0)), (fx(xt), fy(RAY_T[0] + 60.0))], fill=GRAY, width=5)
    txt(fx(X_C + YUVA[4][2]), fy(P - 40.0), "TABLA Ø340 · seyir kotu %s · dozajda +100 kalkar, döner + kayar" % sayi(P), f7, BUZ, "mm")
    txt(fx(X_C + W_C - 210.0), fy(P + 40.0), "tabla ucu · ROBOT KÜREKLE ALIR", f7, BUZ, "mm")
    kapak(X_C, 200.0 - 6.0, 1500.0 + 6.0, T_BAS[0], T_BAS[1], "DOZAJ BAŞLIKLARI · nokta nozul, tabla döner + kayar|harç: piston pompa · kıyma / kuşbaşı: vida · kaşar: karıştırıcı + vida · sucuk: şarjör + bıçak")
    kapak(X_C, 200.0 - 6.0, 1500.0 + 6.0, T_KAS[0], T_KAS[1])
    for urun, gw, xc in YUVA:
        kesik(X_C, xc - gw / 2 + 6, xc + gw / 2 - 6, T_KAS[0] + 8, T_KAS[1] - 8)
        satirlar(fx(X_C + xc), fy(1815.0) - 4, urun, f7, INK, 16)
        txt(fx(X_C + xc), fy(1815.0) + 22, ("%s × 400 × 360" % sayi(gw)) if gw >= 280 else ("180 × 400" if "SUCUK" in urun else "140"), f7, GRAY, "mm")
    txt(fx(X_C + 850), fy(T_KAS[1]) - 14, "HAZNE SIRASI · +3 °C · önden kaset takılır · kaset tabanı kot 1627", f7, INK, "mm")
    d.rectangle([fx(X_C + 33), fy(T_KPK[1]), fx(X_C + W_C - 33), fy(T_KPK[0])], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_C + W_C / 2), fy((T_KPK[0] + T_KPK[1]) / 2), "üst kapak PU 40", f7, GRAY, "mm")
    kapak(X_C, 33.0, 188.0, T_BAS[0], T_KAS[1])
    kesik(X_C, 45.0, 176.0, 1510.0, 1730.0, "C KARTI", INK)
    kesik(X_C, 45.0, 176.0, 1745.0, 1975.0, "SÜRÜCÜLER", INK, "dozaj + tabla")
    kapak(X_C, 1512.0, 1767.0, T_BAS[0], T_KAS[1])
    kesik(X_C, 1518.0, 1762.0, 1510.0, 1730.0, "SOĞUTMA GRUBU", INK, "1/5 HP · 250 × 220")
    kesik(X_C, 1518.0, 1762.0, 1745.0, 1975.0, "EVAPORATÖR", INK, "+ fan · 250 × 150")
    modul_etiketi(X_C, W_C, "MODÜL C · TOPPING (tablalı · soğutucusu sağ yan bölmede)", "1800 × 830 × 970 · B üstünde")
    olcu_h(fx(X_C), fx(X_C + W_C), fy(H_MAK) - 26, sayi(W_C), f11, INK)
    # F K E
    ciz_F(P, [(60.0, 700.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", "245 × 180 × 45"),
              (60.0, 460.0, 320.0, 670.0, "ANA PANO · PLC · ana şalter", "400 × 350 × 250 · ekran yok → tablet"),
              (480.0, 730.0, 320.0, 670.0, "UPS", "500 VA"),
              (760.0, 1440.0, 135.0, 970.0, "BOŞ", "680 × 770 × 835")])
    ciz_K(P)
    a0, a1, yig = ciz_E(P)
    birlesimler()
    kot_cizgileri((120.0, H_B, RAY_T[1], P, 1490.0, 1627.0, 1660.0, 1987.0, H_MAK))
    # PLAN
    plan_ortak(P, "tabla")
    d.ellipse([fx(X_A + 180), py(-440.0), fx(X_A + 520), py(-100.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_A + 350), py(-270.0), "TABLA Ø340 · pres altında · z −270", f7, BUZ, "mm")
    for urun, gw, xc in YUVA:
        d.rectangle([fx(X_C + xc - gw / 2 + 6), py(-470.0), fx(X_C + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
        satirlar(fx(X_C + xc), py(-420.0), urun, f7, INK, 16)
    dline((fx(X_A + 90), py(-270.0)), (fx(X_C + W_C - 40), py(-270.0)), ACC, 3, 12, 6)
    for xt in (X_C + YUVA[4][2], X_C + W_C - 170.0):
        darc(fx(xt), py(-270.0), 170.0 * S, 0.0, 360.0, BUZ, 2, 4.0)
    txt(fx(X_C + 760), py(-600.0), "TABLA HATTI z −270 = fırın bandı ekseni · ray tabanın altında (kesik) · hazne ağızları tabla hattının üstünde", f7, ACC, "mm")
    d.rectangle([fx(X_C + 30), py(-780.0), fx(X_C + W_C - 30), py(-740.0)], fill=EVC, outline=BUZ, width=1)
    txt(fx(X_C + W_C / 2), py(-760.0), "dozaj pompaları haznelerin arkasında (z −470 … −740) · soğutma grubu sağ yan bölmede", f7, BUZ, "mm")
    # KESIT 1
    z = sec(SX1)
    txt(SX1, FY_TOP - 200, "KESİT 1 · A + B (K1) + ROBOT", f16, ACC)
    txt(SX1, FY_TOP - 162, "Robot hamur topunu ağızdan tablanın ortasına bırakır · tabla örse iner, pres basar", f9, GRAY)
    govde(z, 0.0, H_B)
    d.rectangle([z(-790), fy(120.0), z(40), fy(0)], fill=SOFT, outline=LINE, width=2)
    cekmeceler(z, KOLON[0], YUZ0)
    txt(z(-340), fy(560.0), "K1 · TAZE PİDE × 6 · çekmece 680 · açılım 700", f7, DOLAP, "mm")
    govde(z, H_B, H_MAK)
    d.rectangle([z(-760.0), fy(RAY_T[0] + 60.0), z(-100.0), fy(RAY_T[0] + 25.0)], fill=ACC, outline=ACC)
    txt(z(-430.0), fy(RAY_T[0] + 90.0), "tabla rayı + araba", f7, ACC, "mm")
    drect(z(-440.0), fy(P - 14.0), z(-100.0), fy(RAY_T[1] + 10.0), INK, 1)
    txt(z(-270.0), fy(RAY_T[1] + 55.0), "ÖRS", f7, INK, "mm")
    d.rectangle([z(-440.0), fy(P), z(-100.0), fy(P - 12.0)], fill=EVC, outline=BUZ, width=2)
    txt(z(-270.0), fy(P) + 22, "tabla Ø340 · kot %s · z −270" % sayi(P), f7, BUZ, "mm")
    d.rectangle([z(-415.0), fy(P + 275.0), z(-125.0), fy(P + 225.0)], fill=SOFT, outline=INK, width=1)
    d.rectangle([z(-10.0), fy(P + 220.0), z(40.0), fy(P)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(P + 235.0), "HAMUR AĞZI %s–%s" % (sayi(P), sayi(P + 220.0)), f7, RED, "rm")
    drect(z(-760.0), fy(2005.0), z(20.0), fy(P + 280.0), GRAY, 1)
    txt(z(-375.0), fy(P + 480.0), "pres kafası · motor + rezistans ÜSTTE", f7, INK, "mm")
    D1 = robot_kesit(z, -270.0 + 232.5, P + 100.0, -270.0, P + 100.0, "ROBOT")
    d.ellipse([z(-270.0) - 47.5 * S, fy(P + 100.0) - 47.5 * S, z(-270.0) + 47.5 * S, fy(P + 100.0) + 47.5 * S], fill=URUN, outline=(180, 140, 70), width=2)
    for yy in (120.0, H_B, RAY_T[1], P, P + 220.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    D2 = kesit_E(P, a0, a1)
    parca_listesi([
        ("MODÜL A", "PRES KAFASI · Fersah PZP-400 uyarlaması · alt tabla yerine sabit örs · pres tablanın üstüne basar", "1", "700 × 830 × 970 · kafa yüksekliği ≤ 385 (VARSAYIM · Fersah'a sorulacak)"),
        ("MODÜL B", "ÇEKMECE modülü · 20 hamur çekmecesi + 2 katlı içecek/tatlı çekmecesi + K4 depo kolonu · v19 ile aynı", "1", "2500 × 830 × 1060 · tepsi nişi boş kalır"),
        ("MODÜL C", "TOPPING · Atosa (Yindu) dozaj, 6 hazne tek sıra · altında tabla arabası (ray 150 + damlama 30 + bölme 250)", "1", "1800 × 830 × 970 · hazne sırası v19'a göre 290 yukarıda"),
        ("TABLA ARABASI", "Ø340 tabla · x kızak + kaldırma 100 + döndürme · pres altı → 6 hazne → fırın ağzı · itici ürünü banda iter", "1", "tur ≤ 60 sn (Atosa: bir pizza en fazla 1 dk) · kotlar VARSAYIM"),
        ("MODÜL F", "KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 × bant 450 · aynı anda 4 ürün · ayarlı sıcaklık + bant hızı", "1", "1500 × 830 × 2030 · gövde 1040–1660 · tabanında ana pano + UPS + robot kontrol kutusu"),
        ("MODÜL K", "KESME · sabit plaka 560 × 450 + yıldız bıçak Ø300 6 dilim + tereyağı spreyi + itici", "1", "600 × 830 × 2030 · plaka kot 1340"),
        ("MODÜL E", "KUTU KATLAYAN · şarjör altta (alttan kaldırmalı) · katlama üstte · kutu 320 × 320 × 45", "1", "700 × 830 × 2030 · şarjör %s mm = %d–%d kutu" % (sayi(yig), int(yig / 1.8), int(yig / 1.5))),
        ("KUTU TEPSİSİ", "Ø340 soketli tepsi (v19 tepsisi) · kutu dolum konumunda bekler, açık kutu üstünde dolar · robot tepsiyi QR dolabına götürüp ağza geri bırakır", "1 + 1", "tepsi yüzü = süreç kotu − 60 · z −270 · yedek serviste"),
        ("ROBOT", "Fairino FR5 · TEK ROBOT · yer rayında · omuz 970 · hamur: çekmece → tabla · kutu → QR · içecek + tatlı", "1", "bilek mesafesi: tabla %d · kutu %d (sınır %d)" % (round(D1), round(D2), round(ERISIM))),
        ("RAY", "yer rayı · tek araba · ekseni hat yüzünden 360", "1", "araba merkezi x 200 – 5100"),
        ("QR DOLABI", "2 × 6 göz · göz 480 × 190 × 440 · koridorun karşısında, hattın sağ ucunda", "1", "x 4295–5300 · ayrıntı SERVİS_TESLİM paftası"),
        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F tabanı, ray yanında (C üst bandı hazne sırasına gitti) · ekran yok (tablet)", "", ""),
    ])
    lejant()
    yol = KLASOR + r"\HAT_ATOSA_GOZLU_v1_teknik.png"
    im.save(yol, dpi=(200, 200)); print("yazildi:", yol, "· hat", sayi(HAT), "· bilek", round(D1), round(D2))


if __name__ == "__main__":
    gozlu()
