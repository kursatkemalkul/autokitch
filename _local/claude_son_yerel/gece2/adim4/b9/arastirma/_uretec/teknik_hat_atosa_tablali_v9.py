# -*- coding: utf-8 -*-
"""AUTOKITCH · BANTLI HAT v6 + ATOSA TABLALI HAT v2 · TEKNIK RESIM (18 Eyl 2026)
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

# ===================== HD KATMANI =====================
# Cizimin TAMAMI K katina olceklenir: koordinatlar, cizgi kalinliklari ve fontlar.
# Boylece sabit piksel kaydirmalari (yaziyi cizginin 26 px altina koy gibi) da
# olcekleniyor ve duzen birebir korunuyor.
K_HD = 2.2


def _ol(v):
    """koordinat dizisini/sayisini olcekle"""
    if isinstance(v, (int, float)):
        return v * K_HD
    if isinstance(v, (list, tuple)):
        return [_ol(x) for x in v]
    return v


class HDraw:
    """ImageDraw sarmalayicisi — her cagriyi K_HD katina cikarir"""

    def __init__(self, im):
        self.d = ImageDraw.Draw(im)
        self._font = {}

    def _f(self, f):
        if f is None:
            return None
        k = id(f)
        if k not in self._font:
            try:
                yol = f.path
                boy = f.size
                self._font[k] = ImageFont.truetype(yol, max(1, int(round(boy * K_HD))))
            except Exception:
                self._font[k] = f
        return self._font[k]

    def _w(self, kw):
        if "width" in kw and isinstance(kw["width"], (int, float)):
            kw["width"] = max(1, int(round(kw["width"] * K_HD)))
        if "font" in kw:
            kw["font"] = self._f(kw["font"])
        return kw

    def text(self, xy, s, **kw):
        return self.d.text(_ol(xy), s, **self._w(kw))

    def line(self, xy, **kw):
        return self.d.line(_ol(xy), **self._w(kw))

    def rectangle(self, xy, **kw):
        return self.d.rectangle(_ol(xy), **self._w(kw))

    def ellipse(self, xy, **kw):
        return self.d.ellipse(_ol(xy), **self._w(kw))

    def polygon(self, xy, **kw):
        return self.d.polygon(_ol(xy), **self._w(kw))

    def arc(self, xy, *a, **kw):
        return self.d.arc(_ol(xy), *a, **self._w(kw))

    def textlength(self, s, font=None, **kw):
        # olceklenmemis (cizim koordinat sisteminde) uzunluk dondur
        return self.d.textlength(s, font=self._f(font), **kw) / K_HD
# ======================================================

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
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · yedeği K'de → 4 gün")}
KOLON = [[(6, "hamur")], [(2, "hamur"), (6, "lahm")], [(6, "lahm"), (1, "icecek")]]
KOLON_AD = ("K1", "K2", "K3")
H_B, H_MAK = 1060.0, 2030.0
X_A, W_A, X_C, W_C, W_B = 0.0, 700.0, 700.0, 1800.0, 2500.0
X_F, W_F, X_K, W_K, X_E, W_E = 2500.0, 1500.0, 4000.0, 600.0, 4600.0, 830.0   # v8: E 830 (kutu_cad_v3)
HAT = X_E + W_E                                              # 5430
Y_ALT, B_TABAN = 123.0, 164.5                                # v8: ALT TABAN ÇİZGİSİ · B iç taban üstü (en alt çekmece önü 167,5 − 3)
P_SUREC, BANT_F, PLAKA_K, TEPSI_E = 1168.0, 1166.0, 1164.0, 1104.0   # v8: çalışma diski · fırın bandı · kesme plakası · kutu tepsisi
ZT = -170.0                                                  # v8: tabla / ürün ekseni (topping_cad_v22)
HAZNE, ADIM = 1400.0, 350.0                                  # firin: pisirme haznesi · urun adimi (4 urun)
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
    if y0 == 0.0:                                                   # v8: gövde 123'ten, altı ayak + süpürgelik (60 geride)
        d.rectangle([x0, fy(y1), x1, fy(Y_ALT)], fill=FILL, outline=LINE, width=4)
        d.rectangle([fx(x0mm + 30.0), fy(Y_ALT), fx(x0mm + w - 30.0), fy(0)], fill=SOFT, outline=LINE, width=2)
    else:
        d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
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
        _n = alt.count("|")
        satirlar(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10 + 8.5 * _n, alt, f7, GRAY, 17)


def modul_etiketi(x0mm, w, ad, olcu, renk=ACC, sira=0):
    x0, x1 = fx(x0mm) + 6, fx(x0mm + w) - 6
    yb = fy(0) + 126 + sira * 50
    d.rectangle([x0, yb, x1, yb + 46], fill=renk)
    txt((x0 + x1) / 2, yb + 14, ad, f8, BG, "mm")
    txt((x0 + x1) / 2, yb + 34, olcu, f7, BG, "mm")


# ======================= MODUL B (v8 · store_cad_v4) =======================
def ciz_B():
    kabin(X_A, W_B, 0.0, H_B)
    K4X, K4W = X_A + XI + 3 * (WO + BOLME), 400.0                                      # 2027,5
    d.rectangle([fx(X_A + 30), fy(H_B - 60.0), fx(X_A + W_B - 30), fy(B_TABAN)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_A + 30), fy(B_TABAN), fx(K4X - 1.0), fy(Y_ALT + 1.5)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_A + 1000), fy((Y_ALT + B_TABAN) / 2), "yalıtımlı taban 41,5 · en alt çekmece önünün 3 mm altı · gövde 123'ten", f7, GRAY, "mm")
    d.rectangle([fx(X_A + 30), fy(H_B - 1.5), fx(X_A + W_B - 30), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_A + W_B / 2), fy(H_B - 30.0), "tavan PU 60 · üstüne MODÜL A ve C oturur · çekmece önü 40 PU + fitil · çekmece başına Transmotec PD3665 + GT3 kayış · Accuride DZ3832 3 parçalı ray · strok 628", f7, GRAY, "mm")
    cx = X_A + XI
    for ki, gruplar in enumerate(KOLON):
        if ki:
            d.rectangle([fx(cx - BOLME), fy(H_B - 60.0), fx(cx), fy(B_TABAN)], fill=SOFT, outline=LINE, width=1)
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
    # K4 · soğutma bölmesi SICAK: tabanı tek sac (PU yok) · Secop 128,5 · ara PU 408,5–438,5 · GN depo · temizlik nişi
    d.rectangle([fx(K4X - BOLME), fy(H_B - 60.0), fx(K4X), fy(B_TABAN)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(K4X), fy(H_B - 60.0), fx(K4X + K4W), fy(Y_ALT + 1.5)], fill=BG, outline=LINE, width=2)
    for y0_, y1_ in ((167.5, 420.5), (423.5, 739.5), (742.5, 997.0)):
        kapak(X_A, K4X - X_A - 15.0, K4X - X_A + K4W + 15.0, y0_, y1_)
    kesik(X_A, K4X - X_A + 25.0, K4X - X_A + 375.0, 128.5, 400.5, "SOĞUTMA GRUBU", INK, "Secop CU KLF4.0CND|350 × 272 × 450")
    satirlar(fx(K4X + K4W / 2), fy(590.0), "DEPO · 2 × GN 1/1-150|kaşar blok / sucuk · +3 °C", f8, INK, 19)
    satirlar(fx(K4X + K4W / 2), fy(870.0), "TEMİZLİK NİŞİ|2 × 5 L bidon", f8, INK, 19)
    # K1 üstü kuru teknik bölme + pano · K2 üstü sabit panel
    K1X = X_A + XI
    kapak(X_A, K1X - X_A - 15.0, K1X - X_A + WO + 15.0, 815.5, 997.0)
    kesik(X_A, K1X - X_A + 14.0, K1X - X_A + 300.0, 878.0, 978.0, "PLC S7-1200 1214C", INK, "+ 2 × SM1221 + SM1222")
    kesik(X_A, K1X - X_A + 310.0, K1X - X_A + 606.0, 878.0, 978.0, "NDR-240-24 · EM-324C", INK, "21 seçici röle · klemens")
    K2X = K1X + WO + BOLME
    kapak(X_A, K2X - X_A - 15.0, K2X - X_A + WO + 15.0, 941.5, 997.0)
    olcu_h(fx(K4X), fx(K4X + K4W), fy(0) + 44, "400", f8, GRAY)
    d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)
    modul_etiketi(X_A, W_B, "MODÜL B · ÇEKMECE MODÜLÜ (store_cad_v4) · 8 pide + 12 lahmacun + içecek/tatlı · K4: Secop soğutma + GN depo + temizlik nişi · K1 üstü: pano · gövde 123'ten",
                  "2500 × 830 × 1060", DOLAP, 1)


# ======================= FIRIN · KESME · KUTU (v8 · montaj v41'den) =======================
def ciz_F(taban_parcalar):
    G0, G1 = H_B, 1486.0                                      # gövde 1060–1486 (taban hizası) · bant üstü 1166
    kabin(X_F, W_F, 0.0, H_MAK, "F · KONVEYÖR FIRIN · özel · elektrikli · 4 ürün")
    kapak(X_F, 33.0, W_F - 33.0, Y_ALT + 3.0, G0 - 3.0)
    for a, b, y0, y1, et, alt in taban_parcalar:
        kesik(X_F, a, b, y0, y1, et, INK, alt)
    d.rectangle([fx(X_F + 3), fy(G1), fx(X_F + W_F - 3), fy(G0)], fill=PUC, outline=LINE, width=2)
    tarali(fx(X_F + 3), fy(G1), fx(X_F + W_F - 3), fy(G0), (226, 214, 190), 11)
    d.rectangle([fx(X_F + 50), fy(BANT_F + 270.0), fx(X_F + 50 + HAZNE), fy(G0 + 20.0)], fill=SICAK, outline=TURUNCU, width=2)
    for i in range(7):
        xx = X_F + 50.0 + 100.0 + i * 200.0
        d.rectangle([fx(xx - 40), fy(BANT_F + 130.0), fx(xx + 40), fy(BANT_F + 60.0)], fill=BG, outline=TURUNCU, width=1)
    txt(fx(X_F + W_F / 2), fy(BANT_F + 215.0), "ÜST PLENUM · hava parmakları × 7 · taşyünü 50", f7, TURUNCU, "mm")
    drect(fx(X_F + 60), fy(BANT_F - 70.0), fx(X_F + 50 + HAZNE - 10), fy(G0 + 25.0), RED, 1)
    txt(fx(X_F + W_F / 2), fy((G0 + BANT_F) / 2 - 12.0), "ALT ISITMA · bant altı pay 106 → ince rezistans / taş VARSAYIM (AÇIK)", f7, RED, "mm")
    d.line([(fx(X_F - 40), fy(BANT_F)), (fx(X_F + W_F + 30), fy(BANT_F))], fill=TURUNCU, width=4)
    for i in range(4):
        xx = X_F + 50.0 + ADIM / 2 + i * ADIM
        d.ellipse([fx(xx - 150), fy(BANT_F + 28.0), fx(xx + 150), fy(BANT_F + 2.0)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X_F + W_F / 2), fy(BANT_F + 45.0), "PİŞİRME HAZNESİ %s · bant üstü %s · aynı anda 4 ürün (adım %s)" % (sayi(HAZNE), sayi(BANT_F), sayi(ADIM)), f7, TURUNCU, "mm")
    olcu_h(fx(X_F + 50.0), fx(X_F + 50.0 + HAZNE), fy(G1) - 18, "HAZNE %s" % sayi(HAZNE), f8, TURUNCU)
    kapak(X_F, 33.0, W_F - 33.0, G1 + 10.0, 2028.0, "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre|fırın kartı + SSR + kontaktör (F'nin kendi panosu) · ~18 kW (tahmin)")
    modul_etiketi(X_F, W_F, "MODÜL F · KONVEYÖR FIRIN", "1500 × 830 × 2030 · taban dolabı 123–1060 · gövde %s–%s · bant %s" % (sayi(G0), sayi(G1), sayi(BANT_F)))
    olcu_h(fx(X_F), fx(X_F + W_F), fy(H_MAK) - 26, sayi(W_F), f11, INK)


def ciz_K():
    PL = PLAKA_K
    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME · SPREY")
    kapak(X_K, 33.0, W_K - 33.0, Y_ALT + 3.0, H_B - 3.0)
    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")
    satirlar(fx(X_K + W_K / 2), fy(690.0), "taban dolabı 123–1060|yedek kutu YOK (Kemal 24 Eyl)", f7, GRAY, 17)
    d.line([(fx(X_K), fy(H_B)), (fx(X_K + W_K), fy(H_B))], fill=LINE, width=4)
    d.rectangle([fx(X_K + 20), fy(PL), fx(X_K + W_K - 20), fy(PL - 14.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_K + W_K / 2), fy(PL - 34.0), "KESME PLAKASI 560 × 450 · üstü %s" % sayi(PL), f7, BUZ, "mm")
    d.rectangle([fx(X_K + 24), fy(PL + 50.0), fx(X_K + 64), fy(PL + 2.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_K + 44), fy(PL + 66.0), "İTİCİ", f7, INK, "mm")
    kesik(X_K, 110.0, 490.0, PL + 90.0, PL + 340.0, "YILDIZ BIÇAK Ø300 · 6 dilim", INK, "piston 100 strok")
    d.ellipse([fx(X_K + 520) - 6, fy(PL + 120.0) - 6, fx(X_K + 520) + 6, fy(PL + 120.0) + 6], fill=RED)
    txt(fx(X_K + 520), fy(PL + 150.0), "SPREY", f7, RED, "mm")
    kapak(X_K, 33.0, W_K - 33.0, PL + 355.0, 2028.0, "İÇECEK + TATLI YEDEĞİ · 4 GÜN|97 kutu 330 ml (2 kat × 115) + 8 tatlı|çekmece 180 + yedek 97 = 277 = 4 gün")
    modul_etiketi(X_K, W_K, "MODÜL K · KESME", "600 × 830 × 2030 · plaka %s" % sayi(PL))
    olcu_h(fx(X_K), fx(X_K + W_K), fy(H_MAK) - 26, sayi(W_K), f11, INK)


def ciz_E():
    """kutu_cad_v3 · E-yerel x 0..830 · kotlar mutlak"""
    a0, a1 = 1085.0, 1330.0                                   # ön alt kapak üstü · ağız üst kirişi altı
    kabin(X_E, W_E, 0.0, H_MAK, "E · KUTU KATLAMA · standart 32 × 32 × 4,2 kutu")
    kapak(X_E, 2.0, W_E - 2.0, Y_ALT + 3.0, a0)
    kesik(X_E, 8.0, 812.0, 240.0, 1148.0, "KUTU ŞARJÖRÜ · arkada · asansörlü", INK,
          "açılım 804 × 404 · yığın 908 = 567 kutu (1,6 mm) · 504 (1,8)|Tr16×4 vida + NEMA 23 · dolum sağ yan kapaktan|tahrik tabanın altında (koruyuculu)")
    agiz(X_E, 2.0, W_E - 2.0, a0, a1, "KUTULAMA AĞZI · robot çatalı tepsiden alır")
    d.rectangle([fx(X_E + 100), fy(TEPSI_E), fx(X_E + 420), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(X_E + 100), fy(TEPSI_E + 42.0), fx(X_E + 420), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(fx(X_E + 260), fy(TEPSI_E + 21.0), "kutu 320 × 42 · tepsi %s (4 çubuk)" % sayi(TEPSI_E), f7, INK, "mm")
    kesik(X_E, 440.0, 800.0, 797.0, 1148.0, "KAPAK MASASI + U FLAP KATLAYICI", INK, "kapak kolu R166 · SureGear 10:1")
    txt(fx(X_E + 46), fy(1188.0), "PİZZA", f7, RED, "mm"); txt(fx(X_E + 46), fy(1170.0), "sol duvar", f7, RED, "mm")
    drect(fx(X_E + 1), fy(1230.0), fx(X_E + 12), fy(1146.0), RED, 2)
    kapak(X_E, 2.0, W_E - 2.0, 1345.0, 2028.0)
    kesik(X_E, 100.0, 828.0, 1472.0, 1540.0, "BESLEYİCİ İTİCİ · 1500 · strok 411", INK)
    kesik(X_E, 112.0, 408.0, 1560.0, 2010.0, "PİSTON SFU1610", INK, "taban · kilit · kapak bastırma")
    kesik(X_E, 450.0, 780.0, 1565.0, 2025.0, "PANO · arkada", INK, "S7-1200|7 step sürücü")
    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KATLAMA (kutu_cad_v3)", "830 × 830 × 2030 · tepsi %s · ağız %s–%s" % (sayi(TEPSI_E), sayi(a0), sayi(a1)))
    olcu_h(fx(X_E), fx(X_E + W_E), fy(H_MAK) - 26, sayi(W_E), f11, INK)
    return a0, a1, 908.0


# ======================= PLAN · ORTAK =======================
def plan_ortak(P, mod):
    txt(OX, PY_TOP - 110, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  ray, robotlar, QR dolabı", f16, ACC)
    txt(fx(HAT / 2), py(-790) - 30, "ARKA", f9, GRAY, "mm")
    zb = 40.0 - DZ
    for x0m, w, ad in ((X_A, W_A, "A · AÇICI (B üstünde)"), (X_C, W_C, "C · TOPPING (B üstünde)"), (X_F, W_F, "F · KONVEYÖR FIRIN"), (X_K, W_K, "K · KESME"), (X_E, W_E, "E · KUTU")):
        d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(40.0)], fill=FILL, outline=LINE, width=3)
        txt(fx(x0m + w / 2), py(40.0) + 26, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DZ)), f8, INK, "mm")
    # A
    d.rectangle([fx(X_A + 29), py(-788.0), fx(X_A + 669), py(12.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_A + 350), py(-745.0), "KONİLİ AÇICI KAFASI · 2 koni + 2 motor", f8, INK, "mm")
    # B cekmeceler (kesik)
    cx = X_A + XI
    for ki in range(3):
        drect(fx(cx + 16), py(-680.0), fx(cx + WO - 16), py(0.0), DOLAP, 2)
        txt(fx(cx + WO / 2), py(-20.0) - 6, "K%d · 620 × 680 · altta (B)" % (ki + 1), f7, DOLAP, "mm")
        cx += WO + BOLME
    drect(fx(cx + 8), py(-788.0), fx(cx + 392), py(0.0), DOLAP, 1)
    txt(fx(cx + 200), py(-20.0) - 6, "K4 · depo · altta (B)", f7, DOLAP, "mm")
    # F
    x0 = X_F + 50.0
    d.rectangle([fx(X_F + 3), py(-788.0), fx(X_F + W_F - 3), py(38.0)], fill=PUC, outline=LINE, width=1)
    tarali(fx(X_F + 3), py(-788.0), fx(X_F + W_F - 3), py(38.0), (226, 214, 190), 11)
    d.rectangle([fx(x0), py(-730.0), fx(x0 + HAZNE), py(-520.0)], fill=SICAK, outline=TURUNCU, width=2)
    txt(fx(X_F + W_F / 2), py(-625.0), "ARKA PLENUM 210 · fan Ø200 × 2 · rezistans", f7, TURUNCU, "mm")
    d.rectangle([fx(x0), py(-520.0), fx(x0 + HAZNE), py(-20.0)], fill=SICAK, outline=TURUNCU, width=2)
    for i in range(4):
        xx = x0 + ADIM / 2 + i * ADIM
        d.ellipse([fx(xx - 150), py(-420.0), fx(xx + 150), py(-120.0)], fill=URUN, outline=(180, 140, 70), width=1)
        txt(fx(xx), py(-270.0), "Ø300", f7, (140, 100, 40), "mm")
    txt(fx(X_F + W_F / 2), py(-45.0), "derinlik: ön duvar 60 + hazne 500 (bant 450) + plenum 210 + arka duvar 60 = 830", f7, TURUNCU, "mm")
    olcu_h(fx(x0), fx(x0 + HAZNE), py(-790) - 58, "HAZNE %s" % sayi(HAZNE), f8, TURUNCU)
    # K (v8 · montaj: plaka z −470…−20, bıçak ve sprey ürün ekseninde z −170)
    d.rectangle([fx(X_K + 20), py(-470.0), fx(X_K + 580), py(-20.0)], fill=EVC, outline=BUZ, width=2)
    d.ellipse([fx(X_K + 300 - 150), py(ZT - 150.0), fx(X_K + 300 + 150), py(ZT + 150.0)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - 150 * S * math.cos(a), py(ZT) - 150 * S * math.sin(a)), (fx(X_K + 300) + 150 * S * math.cos(a), py(ZT) + 150 * S * math.sin(a))], fill=INK, width=1)
    txt(fx(X_K + 300), py(-520.0), "KESME PLAKASI 560 × 450 · yıldız bıçak Ø300", f7, BUZ, "mm")
    d.rectangle([fx(X_K + 26), py(ZT - 40.0), fx(X_K + 62), py(ZT + 40.0)], fill=BG, outline=INK, width=2)
    d.line([(fx(X_K + 470), py(ZT)), (fx(X_K + 560), py(-206.0)), (fx(X_E + 90), py(-206.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 90), py(-206.0)), (fx(X_E + 70), py(-206.0) - 7), (fx(X_E + 70), py(-206.0) + 7)], fill=INK)
    txt(fx(X_K + 600), py(40.0) + 52, "K itici pizzayı 36 mm içeri kaydırıp E'ye iter (ürün ekseni −170 → kutu ekseni −206)", f7, RED, "mm")
    # E (v8 · kutu_cad_v3)
    drect(fx(X_E + 8), py(-819.0), fx(X_E + 812), py(-415.0), GRAY, 1)
    txt(fx(X_E + 410), py(-617.0), "ŞARJÖR · açılım 804 × 404 · 567 kutu · y 240–1148", f7, GRAY, "mm")
    d.rectangle([fx(X_E + 100), py(-366.0), fx(X_E + 420), py(-46.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_E + 260), py(-219.0), "KUTU", f8, INK, "mm")
    txt(fx(X_E + 260), py(-192.0), "320 × 320 × 42", f7, GRAY, "mm")
    drect(fx(X_E + 440), py(-368.0), fx(X_E + 800), py(-26.0), GRAY, 1)
    txt(fx(X_E + 620), py(-197.0), "kapak masası", f7, GRAY, "mm")
    d.line([(fx(X_E + 1), py(-372.0)), (fx(X_E + 1), py(-24.0))], fill=RED, width=4)
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
    d.rectangle([z(-790), fy(h1), z(40), fy(max(h0, Y_ALT) if plint else h0)], fill=FILL, outline=LINE, width=4)
    if plint:                                                        # v8: süpürgelik 60 geride, gövde 123'ten
        d.rectangle([z(-760), fy(Y_ALT), z(-20), fy(0)], fill=SOFT, outline=LINE, width=2)


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
    txt(SX2, FY_TOP - 162, "Robot kapalı kutuyu tepsinin çubukları arasından çatalla alır, QR gözüne koyar · E: kutu_cad_v3", f9, GRAY)
    govde(z, 0.0, H_MAK, True)
    d.rectangle([z(-819.0), fy(1148.0), z(-415.0), fy(240.0)], fill=BG, outline=GRAY, width=1)
    satirlar(z(-617.0), fy(700.0), "KUTU ŞARJÖRÜ|567 kutu · y 240–1148|asansör Tr16 + NEMA 23", f7, GRAY, 16)
    drect(z(-430.0), fy(Y_ALT), z(-354.0), fy(100.0), ACC, 1)
    txt(z(-392.0), fy(80.0), "tahrik · tabanın altında", f7, ACC, "mm")
    d.line([(z(-819.0), fy(1500.0)), (z(-408.0), fy(1500.0))], fill=INK, width=3)
    d.polygon([(z(-408.0), fy(1500.0)), (z(-428.0), fy(1500.0) - 7), (z(-428.0), fy(1500.0) + 7)], fill=INK)
    txt(z(-614.0), fy(1500.0) - 16, "besleyici 1500 · strok 411", f7, INK, "mm")
    d.rectangle([z(-374.0), fy(1150.0), z(-32.0), fy(1140.0)], fill=SOFT, outline=INK, width=1)
    d.rectangle([z(-366.0), fy(TEPSI_E), z(-46.0), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([z(-366.0), fy(TEPSI_E + 42.0), z(-46.0), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(z(-206.0), fy(TEPSI_E + 21.0), "kutu 320 × 42", f7, INK, "mm")
    d.rectangle([z(-10.0), fy(a1), z(40.0), fy(a0)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(a1) - 14, "KUTULAMA AĞZI %s–%s" % (sayi(a0), sayi(a1)), f7, RED, "rm")
    drect(z(-394.0), fy(2010.0), z(-58.0), fy(1560.0), GRAY, 1)
    txt(z(-226.0), fy(1785.0), "PİSTON SFU1610", f7, GRAY, "mm")
    drect(z(-826.0), fy(2025.0), z(-740.0), fy(1565.0), GRAY, 1)
    txt(z(-783.0), fy(2045.0), "pano", f7, GRAY, "mm")
    ty = TEPSI_E - 9.0
    D = robot_kesit(z, 230.0, ty + 20.0, -206.0, ty, "ROBOT")
    d.line([(z(-366.0), fy(ty)), (z(-46.0), fy(ty))], fill=ACC, width=4)
    txt(z(-206.0), fy(ty) + 16, "çatal · tepsi çubukları arasında · kutu ekseni z −206", f7, ACC, "mm")
    d.rectangle([z(QRZ[0]), fy(2000.0), z(QRZ[1]), fy(0.0)], fill=FILL, outline=LINE, width=4)
    for yy in QR_SATIR:
        d.rectangle([z(QRZ[0]), fy(yy + 190.0), z(QRZ[0] + 440.0), fy(yy)], fill=EVC, outline=BUZ, width=1)
        txt(z(QRZ[0] + 220.0), fy(yy + 95.0), "göz · y %s" % sayi(yy), f7, BUZ, "mm")
    txt(z((QRZ[0] + QRZ[1]) / 2), fy(2000.0) - 16, "QR DOLABI · 6 satır", f8, INK, "mm")
    olcu_h(z(40), z(QRZ[0]), fy(0) + 84, "koridor + pay %s" % sayi(QRZ[0] - 40.0), f8, GRAY)
    for yy in (Y_ALT, 240.0, a0, TEPSI_E, 1148.0, a1, 1500.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    return D


def parca_listesi(satirlar_):
    x0, y0 = SX1, PY_TOP - 60.0
    txt(x0, y0 - 46, "MODÜLLER (lego · cıvatalı flanşla birleşir)  ·  PARÇA LİSTESİ", f16, ACC)
    kol = (0, 250, 1560, 1660)
    gen = 2790
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
def bantli():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    P = 1150.0
    PZP = (1060.0, 2010.0)
    T_AGZ, T_BAS, T_KAS, T_SOG = (1070.0, 1180.0), (1183.0, 1317.0), (1320.0, 1680.0), (1690.0, 2028.5)
    baslik("AUTOKITCH  ·  BANTLI HAT  ·  TEKNİK RESİM  v6  ·  A + B + C = HAT 2 KOL v19  ·  ROBOT AĞZI YERİNE BANT  ·  HAT 5300 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  ürün tepsisiz: pres → bant → konveyör fırın → kesme plakası → kutu  ·  robot yalnız hamur + kutu + içecek taşır  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  tüm modüller 830 derin  ·  ölçüler mm  ·  18 Eylül 2026")
    # A
    kabin(X_A, W_A, H_B, H_MAK, "A · PRESS")
    kapak(X_A, 33.0, 667.0, PZP[0] + 3.0, PZP[1])
    kesik(X_A, 40.0, 660.0, PZP[0] + 8.0, P - 12.0, "", GRAY)
    d.ellipse([fx(X_A + 180), fy(P) - 4, fx(X_A + 520), fy(P) + 4], outline=INK, width=2)
    txt(fx(X_A + 300), fy(P) + 18, "alt plaka Ø340 ısıtmalı · kot %s" % sayi(P), f7, GRAY, "mm")
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "PRES AĞZI · robot hamuru bırakır")
    kesik(X_A, 205.0, 495.0, P + 225.0, P + 275.0, "üst plaka Ø290", INK)
    kesik(X_A, 40.0, 660.0, P + 280.0, PZP[1] - 5.0, "PRES GÖVDESİ · MOTOR ÜSTTE", INK, "motor + rezistans + 2 kolon · 3,5 kW · 640 × 800")
    modul_etiketi(X_A, W_A, "MODÜL A · PRESS", "700 × 830 × 970 · B üstünde")
    olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)
    ciz_B("YEDEK BÖLME|385 × 305 · boş")
    # C
    kabin(X_C, W_C, H_B, H_MAK, "C · ATOSA (YINDU) DOZAJ ÜNİTESİ · ALTINDA ADIMLI BANT")
    d.rectangle([fx(X_C + 30), fy(T_AGZ[1]), fx(X_C + W_C - 30), fy(T_AGZ[0])], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_C - 60.0), fy(P), fx(X_F + 40.0), fy(P - 60.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_C + W_C / 2), fy(P - 30.0), "TOPPING BANDI 400 · adımlı · bant üstü kot %s = pres alt plakası = fırın bandı · sol uçta PRES → BANT GEÇİŞİ (kırmızı ok)" % sayi(P), f7, BUZ, "mm")
    for urun, gw, xc in YUVA19[::2]:
        d.ellipse([fx(X_C + xc - 150), fy(P + 28.0), fx(X_C + xc + 150), fy(P + 2.0)], fill=URUN, outline=(180, 140, 70), width=1)
    d.line([(fx(X_A + 530), fy(P + 12.0)), (fx(X_C - 40.0), fy(P + 12.0))], fill=RED, width=3)
    d.polygon([(fx(X_C - 40.0), fy(P + 12.0)), (fx(X_C - 60.0), fy(P + 12.0) - 7), (fx(X_C - 60.0), fy(P + 12.0) + 7)], fill=RED)
    kapak(X_C, 33.0, 1767.0, T_BAS[0], T_BAS[1], "DOZAJ BAŞLIĞI × 6 · 300 geniş · bant boyunca geçen ürünü tam kaplar|harç: piston pompa · kıyma / kuşbaşı: vida · kaşar: karıştırıcı + vida · sucuk: şarjör + bıçak")
    kapak(X_C, 33.0, 1767.0, T_KAS[0], T_KAS[1])
    for urun, gw, xc in YUVA19:
        kesik(X_C, xc - gw / 2 + 6, xc + gw / 2 - 6, T_KAS[0] + 8, T_KAS[1] - 8)
        satirlar(fx(X_C + xc), fy(1510.0) - 4, urun, f7, INK, 16)
        txt(fx(X_C + xc), fy(1510.0) + 22, ("%s × 400 × 360" % sayi(gw)) if gw >= 280 else ("180 × 400" if "SUCUK" in urun else "140"), f7, GRAY, "mm")
    txt(fx(X_C + W_C / 2), fy(T_KAS[1]) - 14, "HAZNE SIRASI · +3 °C · önden kaset takılır · kaset tabanı kot 1320", f7, INK, "mm")
    kapak(X_C, 33.0, 1767.0, T_SOG[0], T_SOG[1])
    kesik(X_C, 60.0, 360.0, T_SOG[0] + 60.0, T_SOG[0] + 280.0, "SOĞUTMA GRUBU", INK, "300 × 250 × 220 · 1/5 HP")
    kesik(X_C, 380.0, 630.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "EVAPORATÖR + FAN", INK, "250 × 150")
    kesik(X_C, 650.0, 900.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "DOZAJ SÜRÜCÜLERİ", INK, "6 kart + bant sürücüsü")
    kesik(X_C, 920.0, 1070.0, T_SOG[0] + 60.0, T_SOG[0] + 210.0, "C KARTI", INK)
    d.line([(fx(X_C + 1085.0), fy(T_SOG[1] - 8)), (fx(X_C + 1085.0), fy(T_SOG[0] + 8))], fill=LINE, width=2)
    kesik(X_C, 1100.0, 1500.0, T_SOG[0] + 40.0, T_SOG[0] + 290.0, "ANA PANO · PLC · ana şalter", INK, "400 × 350 × 250 · ekran yok → tablet")
    kesik(X_C, 1520.0, 1765.0, T_SOG[0] + 40.0, T_SOG[0] + 290.0, "UPS", GRAY, "500 VA")
    modul_etiketi(X_C, W_C, "MODÜL C · TOPPING-BANT (kendi soğutucusu üstte)", "1800 × 830 × 970 · B üstünde")
    olcu_h(fx(X_C), fx(X_C + W_C), fy(H_MAK) - 26, sayi(W_C), f11, INK)
    # F K E
    ciz_F(P, [(60.0, 700.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", "245 × 180 × 45 · kablo → zemin → ray zinciri"),
              (760.0, 1440.0, 135.0, 780.0, "BOŞ", "680 × 770 × 645")])
    ciz_K(P)
    a0, a1, yig = ciz_E(P)
    birlesimler()
    kot_cizgileri((120.0, 850.0, H_B, P, 1320.0, 1470.0, 1680.0, H_MAK))
    # PLAN
    plan_ortak(P, "bant")
    d.ellipse([fx(X_A + 180), py(-610.0), fx(X_A + 520), py(-270.0)], outline=GRAY, width=2)
    txt(fx(X_A + 350), py(-440.0), "alt plaka Ø340 · z −440", f7, GRAY, "mm")
    for urun, gw, xc in YUVA19:
        d.rectangle([fx(X_C + xc - gw / 2 + 6), py(-470.0), fx(X_C + xc + gw / 2 - 6), py(-70.0)], fill=BG, outline=INK, width=2)
        satirlar(fx(X_C + xc), py(-330.0), urun, f7, INK, 16)
    drect(fx(X_C - 140.0), py(-470.0), fx(X_F + 40.0), py(-70.0), BUZ, 2)
    txt(fx(X_C + W_C / 2), py(-560.0), "TOPPING BANDI 400 (z −470 … −70) haznelerin altında · bant ekseni z −270 = fırın bandı ekseni", f7, BUZ, "mm")
    d.line([(fx(X_A + 520), py(-440.0)), (fx(X_C - 140.0), py(-300.0))], fill=RED, width=3)
    txt(fx(X_A + 600), py(-250.0), "pres → bant geçişi", f7, RED, "mm")
    d.rectangle([fx(X_C + 30), py(-780.0), fx(X_C + W_C - 30), py(-740.0)], fill=EVC, outline=BUZ, width=1)
    txt(fx(X_C + W_C / 2), py(-760.0), "EVAPORATÖR · hazne kabini · dozaj pompaları haznelerin arkasında (z −470 … −740)", f7, BUZ, "mm")
    # KESIT 1
    z = sec(SX1)
    txt(SX1, FY_TOP - 200, "KESİT 1 · A + B (K1) + ROBOT", f16, ACC)
    txt(SX1, FY_TOP - 162, "Robot hamur topunu pres ağzından alt plakanın ortasına bırakır", f9, GRAY)
    govde(z, 0.0, H_B)
    d.rectangle([z(-790), fy(120.0), z(40), fy(0)], fill=SOFT, outline=LINE, width=2)
    cekmeceler(z, KOLON[0], YUZ0)
    txt(z(-340), fy(560.0), "K1 · TAZE PİDE × 6 · çekmece 680 · açılım 700", f7, DOLAP, "mm")
    govde(z, H_B, H_MAK)
    drect(z(-770.0), fy(PZP[1] - 5), z(30.0), fy(PZP[0] + 8), INK, 1)
    d.line([(z(-610.0), fy(P)), (z(-270.0), fy(P))], fill=INK, width=3)
    txt(z(-440.0), fy(P) + 14, "alt plaka Ø340 · kot %s" % sayi(P), f7, GRAY, "mm")
    d.rectangle([z(-585.0), fy(P + 275.0), z(-295.0), fy(P + 225.0)], fill=SOFT, outline=INK, width=1)
    d.rectangle([z(-10.0), fy(P + 220.0), z(40.0), fy(P)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(P + 235.0), "PRES AĞZI %s–%s" % (sayi(P), sayi(P + 220.0)), f7, RED, "rm")
    txt(z(-375.0), fy(P + 560.0), "pres gövdesi · motor + rezistans ÜSTTE", f7, INK, "mm")
    D1 = robot_kesit(z, -440.0 + 232.5, P + 100.0, -440.0, P + 100.0, "ROBOT")
    d.ellipse([z(-440.0) - 47.5 * S, fy(P + 100.0) - 47.5 * S, z(-440.0) + 47.5 * S, fy(P + 100.0) + 47.5 * S], fill=URUN, outline=(180, 140, 70), width=2)
    for yy in (120.0, H_B, P, P + 220.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    D2 = kesit_E(P, a0, a1)
    parca_listesi([
        ("MODÜL A", "PRESS · Fersah PZP-400 tam makine · pres ağzı aşağıda, motor üstte · HAT 2 KOL v19 ile aynı", "1", "700 × 830 × 970 · 170 kg · alt plaka kot 1150 (VARSAYIM)"),
        ("MODÜL B", "ÇEKMECE modülü · 20 hamur çekmecesi + 2 katlı içecek/tatlı çekmecesi + K4 depo kolonu · v19 ile aynı", "1", "2500 × 830 × 1060 · tepsi nişi boş kalır"),
        ("MODÜL C", "TOPPING-BANT · Atosa (Yindu) dozaj, 6 hazne tek sıra · robot ağzının yerinde adımlı bant 400", "1", "1800 × 830 × 970 · bant üstü kot 1150"),
        ("DOZAJ BAŞLIĞI", "300 geniş yayıcı başlık · hazne başına 1 (v19'daki nokta nozulun yerine)", "6", "AÇIK · yeniden tasarım ister"),
        ("PRES → BANT", "basılmış tabanı pres alt plakasından banda aktaran düzenek", "1", "AÇIK · çözülmedi"),
        ("MODÜL F", "KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 × bant 450 · aynı anda 4 ürün · ayarlı sıcaklık + bant hızı", "1", "1500 × 830 × 2030 · gövde 850–1470 · tabanında robot kontrol kutusu"),
        ("MODÜL K", "KESME · sabit plaka 560 × 450 + yıldız bıçak Ø300 6 dilim + tereyağı spreyi + itici", "1", "600 × 830 × 2030 · plaka kot 1150"),
        ("MODÜL E", "KUTU KATLAYAN · şarjör altta (alttan kaldırmalı) · katlama üstte · kutu 320 × 320 × 45", "1", "700 × 830 × 2030 · şarjör %s mm = %d–%d kutu" % (sayi(yig), int(yig / 1.8), int(yig / 1.5))),
        ("KUTU TEPSİSİ", "Ø340 soketli tepsi (v19 tepsisi) · kutu dolum konumunda bekler, açık kutu üstünde dolar · robot tepsiyi QR dolabına götürüp ağza geri bırakır", "1 + 1", "tepsi yüzü = süreç kotu − 60 · z −270 · yedek serviste"),
        ("ROBOT", "Fairino FR5 · TEK ROBOT · yer rayında · omuz 970 · hamur: çekmece → pres · kutu → QR · içecek + tatlı", "1", "bilek mesafesi: pres %d · kutu %d (sınır %d)" % (round(D1), round(D2), round(ERISIM))),
        ("RAY", "yer rayı · tek araba · ekseni hat yüzünden 360", "1", "araba merkezi x 200 – 5100"),
        ("QR DOLABI", "2 × 6 göz · göz 480 × 190 × 440 · koridorun karşısında, hattın sağ ucunda", "1", "x 4295–5300 · ayrıntı SERVİS_TESLİM paftası"),
        ("KONTROL", "ana pano PLC + UPS: C üst bandı · robot kontrol kutusu: F tabanı, ray yanında · ekran yok (tablet)", "", ""),
    ])
    lejant()
    yol = KLASOR + r"\HAT_BANTLI_v6_teknik.png"
    im.save(yol, dpi=(int(200 * K_HD), int(200 * K_HD))); print("yazildi:", yol, "· hat", sayi(HAT), "· bilek", round(D1), round(D2))


# =====================================================================
#                          ATOSA TABLALI HAT v2
# =====================================================================
def tablali():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    P = P_SUREC                                              # çalışma diski üstü 1168 = süreç kotu (topping_cad_v22: 1060 + 108)
    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v9 · ÖNERİ  ·  TOPPING = 4 UNO çekirdeği + kaşar/sucuk kaseti (teknik_topping_satinalma_v2) · E = kutu_cad_v3 · B = store_cad_v4  ·  ALT TABAN 123 · SÜREÇ 1168  ·  HAT 5430 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  bütün gövdeler yerden 123'te başlar, istasyon tabanları 1060  ·  ürün tepsisiz: hamur topu çalışma diskinde KONİLİ AÇICI ile açılır, dozajlanır, bıçak burunlu bant fırına çeker → kesme plakası → kutu  ·  TOPPING: sos · harç · kıyma · kuşbaşı = UNO çekirdeği (Beldos valf + silindir, bizim hazne + step) · kaşar + küp sucuk = bizim kaset  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  ölçüler mm  ·  25 Eylül 2026")
    # ---- A · AÇICI (topping_cad_v22: kolon x 290–410 · koniler 1176–1264 · kafa plakası 1310–1322)
    kabin(X_A, W_A, H_B, H_MAK, "A · KONİLİ DÖNER AÇICI · tabla altında bekler")
    kapak(X_A, 33.0, 667.0, H_B + 3.0, 2010.0)
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot TOP halinde bırakır")
    _kx = X_A + 350.0
    for _y in (1.0, -1.0):
        d.polygon([(fx(_kx), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 96.0))], outline=INK)
    kesik(X_A, 270.0, 430.0, 1310.0, 1322.0, "", INK)
    drect(fx(X_A + 290.0), fy(1440.0), fx(X_A + 410.0), fy(H_B), INK, 1)
    satirlar(fx(X_A + 350.0), fy(1700.0), "AÇICI · kolon x 290–410 · 1060–1440|kafa plakası 160 × 680 × 12 · kot 1310|Z kızağı strok 60 · Ø32 pnömatik|2 KONİ · boy 140 · taban Ø90 · yarım açı 17,82°|2 × NEMA23 + planet · ters yönde döner", f7, INK, 17)
    modul_etiketi(X_A, W_A, "MODÜL A · KONİLİ AÇICI", "700 × 830 × 970 · B üstünde")
    olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)
    ciz_B()
    # ---- C · TOPPING (topping_cad_v22 · modül yereli + 700 = hat, + 1060 = kot)
    kabin(X_C, W_C, H_B, H_MAK, "C · TOPPING · 4 UNO + 2 kaset (öneri)")
    TEK = (145.0, 2585.0, 1061.5, 1091.5); RAY = (200.0, 2485.0, 1080.5, 1095.5); KAS = (165.0, 2535.0)
    d.rectangle([fx(TEK[0]), fy(TEK[3]), fx(TEK[1]), fy(TEK[2])], fill=SOFT, outline=LINE, width=2)
    d.rectangle([fx(RAY[0]), fy(RAY[3]), fx(RAY[1]), fy(RAY[2])], fill=BG, outline=INK, width=2)
    for _kx in KAS:
        d.ellipse([fx(_kx) - 9.55 * S, fy(1093.0) - 9.55 * S, fx(_kx) + 9.55 * S, fy(1093.0) + 9.55 * S], fill=BG, outline=ACC, width=2)
    d.rectangle([fx(2507.0), fy(1121.0), fx(2563.0), fy(1064.0)], fill=BG, outline=INK, width=2)
    txt(fx(2535.0), fy(1140.0), "X MOTORU", f7, INK, "mm")
    d.rectangle([fx(180.0), fy(P), fx(520.0), fy(1157.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(200.0), fy(1118.5), fx(500.0), fy(1108.5)], fill=ACC, outline=ACC)
    txt(fx(1250.0), fy(1128.0), "TABLA ARABASI · strok 1987 (x 350 → 2337) · HGR15 ray 2285 · GT3 kapalı çevrim · tekne 1061–1091 · tabla Ø340 + çalışma diski · üstü %s · ekseni z −170" % sayi(P), f7, ACC, "mm")
    d.rectangle([fx(2504.0), fy(BANT_F), fx(2926.0), fy(1103.0)], fill=EVC, outline=BUZ, width=1)
    txt(fx(2715.0), fy(1088.0), "AKTARMA BANDI · bıçak burunlu", f7, BUZ, "mm")
    # v9 · YENİ TOPPING: 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + 2 bizim kaset (kaşar · küp sucuk) — teknik_topping_satinalma_v2
    UNO9 = [("SOS", 100.0, 320.0, 1737.0, "15 L (V)", True), ("HARÇ", 340.0, 780.0, 1832.0, "45 L", True),
            ("KIYMA", 800.0, 990.0, 1667.0, "8 L", False), ("KUŞBAŞI", 1010.0, 1200.0, 1667.0, "8 L", False)]
    KAS9 = [("KAŞAR", 1220.0, 1502.0, "bizim rende|8,8 kg"), ("KÜP SUCUK", 1522.0, 1664.0, "bizim kaset|2,8 kg")]
    X = lambda l: fx(X_C + l)
    d.rectangle([X(90.0), fy(1968.0), X(790.0), fy(1317.0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(790.0), fy(1740.0), X(1710.0), fy(1317.0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(95.0), fy(1962.0), X(785.0), fy(1320.0)], fill=BG, outline=LINE, width=1)
    d.rectangle([X(795.0), fy(1680.0), X(1705.0), fy(1320.0)], fill=BG, outline=LINE, width=1)
    txt(X(440.0), fy(1990.0), "SOĞUK HÜCRE · tavan 1968'e yükseldi (sos + harç)", f7, GRAY, "mm")
    txt(X(1250.0), fy(1710.0), "SOĞUK HÜCRE +3 °C · tavan 1680", f7, GRAY, "mm")
    for ad, a0, a1, ust, hz, yassi in UNO9:
        c = (a0 + a1) / 2.0; hw = (a1 - a0) / 2.0
        d.rectangle([X(c - 41), fy(1392.6), X(c + 41), fy(1320.0)], fill=BG, outline=INK, width=2)
        d.rectangle([X(c + 41), fy(1380.5), X(c + 91), fy(1336.5)], fill=BG, outline=ACC, width=2)
        d.rectangle([X(c - 32), fy(1452.0), X(c + 32), fy(1392.6)], fill=BG, outline=INK, width=2)
        d.polygon([(X(c - 32), fy(1452.0)), (X(c + 32), fy(1452.0)), (X(c + hw), fy(1632.0)), (X(c + hw), fy(ust)), (X(c - hw), fy(ust)), (X(c - hw), fy(1632.0))], fill=BG, outline=ACC)
        d.line([(X(c - 32), fy(1452.0)), (X(c - hw), fy(1632.0)), (X(c - hw), fy(ust)), (X(c + hw), fy(ust)), (X(c + hw), fy(1632.0)), (X(c + 32), fy(1452.0))], fill=ACC, width=3)
        uc = 1184.0 if yassi else 1216.0
        d.rectangle([X(c - 18), fy(1340.0), X(c + 18), fy(uc + (40.0 if yassi else 0.0))], fill=BG, outline=INK, width=2)
        if yassi:
            d.polygon([(X(c - 18), fy(1224.0)), (X(c + 18), fy(1224.0)), (X(c + 25), fy(1184.0)), (X(c - 25), fy(1184.0))], fill=BG, outline=INK)
        satirlar(X(c), fy(ust) + 16, "%s|UNO · %s" % (ad, hz), f7, INK, 16)
    for ad, a0, a1, alt in KAS9:
        c = (a0 + a1) / 2.0
        d.rectangle([X(a0 + 2), fy(1680.0), X(a1 - 2), fy(1330.0)], fill=BG, outline=INK, width=3)
        d.rectangle([X(c - 22), fy(1330.0), X(c + 22), fy(1216.0)], fill=BG, outline=INK, width=2)
        satirlar(X(c), fy(1560.0), "%s|%s" % (ad.replace(" ", "|") if a1 - a0 < 200 else ad, alt), f7, INK, 16)
    txt(X(900.0), fy(1200.0), "ağızlar tabla ekseninde (z −170) · yassı uç 1184 (sos · harç) · yuvarlak uç 1216 · pide üstü 1176", f7, INK, "mm")
    # teknik bant yalnız x 850–1710 (yerel): soğutma + pano + güç + UPS · 12 sürücü kuru bölmeye iner
    kesik(X_C, 850.0, 1150.0, 1772.0, 1992.0, "SOĞUTMA GRUBU", INK)
    kesik(X_C, 1180.0, 1580.0, 1772.0, 2012.0, "PANO", INK, "PLC · röleler")
    kesik(X_C, 1600.0, 1655.0, 1772.0, 1897.0, "", INK)
    txt(fx(X_C + 1627.0), fy(1915.0), "güç", f7, INK, "mm")
    kesik(X_C, 1660.0, 1709.0, 1772.0, 1894.0, "", INK)
    txt(fx(X_C + 1684.0), fy(1935.0), "UPS", f7, INK, "mm")
    d.rectangle([X(33.0), fy(2027.0), X(W_C - 33.0), fy(1987.0)], fill=PUC, outline=GRAY, width=1)
    modul_etiketi(X_C, W_C, "MODÜL C · TOPPING v9 öneri · 4 UNO çekirdeği + 2 bizim kaset", "1800 × 830 × 970 · B üstünde · disk %s" % sayi(P))
    olcu_h(fx(X_C), fx(X_C + W_C), fy(H_MAK) - 26, sayi(W_C), f11, INK)
    # ---- F K E
    ciz_F([(60.0, 700.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", "245 × 180 × 45"),
           (60.0, 460.0, 320.0, 670.0, "ANA PANO · PLC · ana şalter", "400 × 350 × 250 · ekran yok → tablet"),
           (480.0, 730.0, 320.0, 670.0, "UPS", "500 VA"),
           (760.0, 1230.0, 135.0, 865.0, "BULAŞIK MAKİNESİ · tezgâh altı", "MEIKO M-iClean UM sınıfı · 460 × 600 × 730|sepet 500 × 500 · giriş 315 · 40 sepet/saat"),
           (1250.0, 1440.0, 135.0, 500.0, "MAKİNE DETERJANI + PARLATICI", "2 × 5 L bidon · seviye şamandıralı"),
           (1250.0, 1440.0, 520.0, 865.0, "BOŞ", "190 × 770 × 345")])
    ciz_K()
    a0, a1, yig = ciz_E()
    birlesimler()
    kot_cizgileri((Y_ALT, H_B, TEPSI_E, P, 1320.0, 1486.0, 1680.0, 1772.0, H_MAK))
    # ---- PLAN
    plan_ortak(P, "tabla")
    d.ellipse([fx(180.0), py(ZT - 170.0), fx(520.0), py(ZT + 170.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(350.0), py(ZT - 190.0), "TABLA Ø340 · park · z −170", f7, BUZ, "mm")
    d.rectangle([fx(790.0), py(-630.0), fx(2410.0), py(-104.0)], outline=GRAY, width=1)
    for ad, a0, a1, ust, hz, yassi in UNO9:
        c = X_C + (a0 + a1) / 2.0; hw = (a1 - a0) / 2.0
        drect(fx(c - hw), py(-560.0), fx(c + hw), py(-120.0), ACC, 2)
        d.rectangle([fx(c - 41), py(-428.0), fx(c + 41), py(-346.0)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 18), py(-346.0), fx(c + 18), py(-170.0 + 18)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 29), py(-559.0), fx(c + 29), py(-428.0)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 30), py(-820.0), fx(c + 30), py(-640.0)], fill=BG, outline=ACC, width=2)
        satirlar(fx(c), py(-470.0), "%s|UNO" % ad, f7, INK, 16)
    for ad, a0, a1, alt in KAS9:
        d.rectangle([fx(X_C + a0 + 2), py(-525.0), fx(X_C + a1 - 2), py(-200.0)], fill=BG, outline=INK, width=2)
        satirlar(fx(X_C + (a0 + a1) / 2), py(-380.0), "%s|bizim" % ad.replace(" ", "|"), f7, INK, 16)
    txt(fx(1600.0), py(-630.0) - 14, "UNO: valf + ürün silindiri soğuk hücrede (z −346…−559) · mil yalıtımdan keçeyle geçer · step tahrik kuru bölmede (z −640…−820)", f7, GRAY, "mm")
    dline((fx(350.0), py(ZT)), (fx(2337.0), py(ZT)), ACC, 3, 12, 6)
    for xt in (1957.5, 2337.0):
        darc(fx(xt), py(ZT), 170.0 * S, 0.0, 360.0, BUZ, 2, 4.0)
    drect(fx(2504.0), py(-315.0), fx(2926.0), py(-25.0), BUZ, 2)
    txt(fx(2715.0), py(-5.0) + 14, "aktarma bandı", f7, BUZ, "mm")
    txt(fx(1350.0), py(ZT) + 24, "TABLA HATTI z −170 = fırın bandı ekseni · park x 350 → fırın ağzı x 2337 · HGR15 ray x 200–2485 (tabanın altında)", f7, ACC, "mm")
    txt(fx(1350.0), py(-790.0) - 40, "UYARI · tekne modül C'nin sağ kenarını 85 mm, sağ kasnak 35 mm aşıyor; sol ucu modül A'nın içinde (x 145) — İSTASYON = KAPALI ÜRÜN kuralına aykırı, KARAR BEKLİYOR", f7, RED, "mm")
    # ---- KESİT 1 · A + B (K1) + ROBOT
    z = sec(SX1)
    txt(SX1, FY_TOP - 200, "KESİT 1 · A + B (K1) + ROBOT", f16, ACC)
    txt(SX1, FY_TOP - 162, "Robot hamur TOPUNU ağızdan çalışma diskinin ortasına bırakır · kafa iner, koniler döner, hamur Ø280'e açılır", f9, GRAY)
    govde(z, 0.0, H_B, True)
    d.rectangle([z(-760), fy(B_TABAN), z(-2), fy(Y_ALT + 1.5)], fill=PUC, outline=GRAY, width=1)
    cekmeceler(z, KOLON[0], YUZ0)
    txt(z(-340), fy(560.0), "K1 · TAZE PİDE × 6 · çekmece 680 · açılım 628", f7, DOLAP, "mm")
    govde(z, H_B, H_MAK)
    d.rectangle([z(-415.0), fy(1091.5), z(-5.0), fy(1061.5)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([z(-315.0), fy(1118.5), z(-25.0), fy(1108.5)], fill=ACC, outline=ACC)
    d.rectangle([z(-340.0), fy(P), z(0.0), fy(1157.0)], fill=EVC, outline=BUZ, width=2)
    txt(z(-170.0), fy(1040.0), "tabla Ø340 + disk · üstü %s · z −170 · altında araba + ray + tekne" % sayi(P), f7, BUZ, "mm")
    d.polygon([(z(-324.0), fy(1176.0)), (z(-16.0), fy(1176.0)), (z(-16.0), fy(1264.0)), (z(-324.0), fy(1264.0))], outline=INK)
    txt(z(-170.0), fy(1220.0), "2 koni", f7, INK, "mm")
    d.rectangle([z(-500.0), fy(1322.0), z(180.0), fy(1310.0)], fill=SOFT, outline=RED, width=2)
    d.rectangle([z(88.0), fy(1308.0), z(167.0), fy(1235.0)], fill=BG, outline=RED, width=2)
    drect(z(-660.0), fy(1440.0), z(-490.0), fy(H_B), INK, 1)
    txt(z(-575.0), fy(1460.0), "açıcı kolonu · Z kızağı 60", f7, INK, "mm")
    satirlar(z(-160.0), fy(1900.0), "UYARI · açıcının kafa plakası ve ön koni motoru|gövdenin 180 mm önüne taşıyor (modeldeki hali)", f7, RED, 17)
    d.rectangle([z(-10.0), fy(P + 220.0), z(40.0), fy(P)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(P + 235.0), "HAMUR AĞZI %s–%s" % (sayi(P), sayi(P + 220.0)), f7, RED, "rm")
    D1 = robot_kesit(z, -170.0 + 232.5, P + 100.0, -170.0, P + 100.0, "ROBOT")
    d.ellipse([z(-170.0) - 47.5 * S, fy(P + 100.0) - 47.5 * S, z(-170.0) + 47.5 * S, fy(P + 100.0) + 47.5 * S], fill=URUN, outline=(180, 140, 70), width=2)
    for yy in (Y_ALT, B_TABAN, H_B, P, P + 220.0, 1440.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    D2 = kesit_E(P, a0, a1)
    parca_listesi([
        ("MODÜL A", "KONİLİ DÖNER AÇICI · 2 koni (boy 140 · taban Ø90 · yarım açı 17,82°) · 2 × NEMA23 + planet · Z kızağı strok 60 · Ø32 pnömatik", "1", "700 × 830 × 970 · 40–160 N · örs YOK · UYARI: kafa plakası + ön motor gövdenin 180 mm önünde"),
        ("MODÜL B", "ÇEKMECE modülü (store_cad_v4) · 21 motorlu çekmece (Transmotec PD3665 + GT3 kayış + Accuride DZ3832 3 parçalı ray · strok 628) · K4: Secop CU soğutma + 2 × GN depo + temizlik nişi · K1 üstü pano", "1", "2500 × 830 × 1060 · gövde 123'ten (ayak + süpürgelik) · yalıtımlı taban 123–164,5"),
        ("MODÜL C", "TOPPING v9 öneri · 4 UNO çekirdeği (sos 15 L V · harç 45 L · kıyma 8 L · kuşbaşı 8 L) + kaşar kaseti 280 + küp sucuk kaseti 140 · 1764 / 1800 · tavan sos+harç üstünde 1968", "1", "1800 × 830 × 970 · disk üstü 1168 · UYARI: tekne sağa 85, kasnak 35 mm taşıyor"),
        ("TABLA ARABASI", "Ø340 tabla + ÇALIŞMA DİSKİ Ø340 × 8 (pimli) · HGR15 x kızağı · pancake dönüş motoru · açıcı altı → kasetler → fırın ağzı", "1", "kaldırma YOK · park yeri AÇICININ ALTI · tabla ekseni z −170"),
        ("X TAHRİK", "GT3 KAPALI ÇEVRİM kayış · 2 × 20 diş kasnak x 165 ve 2535 · araba bütün strokta kayışa bağlı · gergi sol kasnak plakasından", "1", "strok 1987 (x 350 → 2337) · HGR15 ray 2285 (x 200–2485), 2 sıra · tekne 2440"),
        ("X MOTORU", "NEMA23 kapalı çevrim step, TEKNENİN ARKASINDA · mili servis cebinden sağ kasnağa girer", "1", "1,2 N·m · gereken 0,382 → 3,14 kat pay · sürtünme 10 N VARSAYIM"),
        ("BANDA AKTARMA", "BIÇAK BURUNLU · bant Ø20 burun silindirine dolanır, üst yüzü diskin 2 mm altı (1166) · pide boşluğu kendi gövdesiyle köprüler", "1", "itici ve köprü YOK · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf bant"),
        ("MODÜL F", "KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 · aynı anda 4 ürün · taban dolabı: robot kontrol, ana pano, UPS, bulaşık makinesi, deterjan", "1", "1500 × 830 × 2030 · gövde 1060–1486 · bant 1166 · AÇIK: bant altı pay 106 (alt ısıtma)"),
        ("MODÜL K", "KESME · plaka 560 × 450 (z −470…−20) + yıldız bıçak Ø300 6 dilim + tereyağı spreyi + itici · taban dolabı: yağ kartuşu + K kartı", "1", "600 × 830 × 2030 · plaka üstü 1164 · yedek kutu YOK · E için şart: itici 36 mm içeri kaydırır"),
        ("MODÜL E", "KUTU KATLAMA (kutu_cad_v3) · standart 32 × 32 × 4,2 E-dalga · şarjör arkada, asansörlü · besleyici 1500 · zımba kalıbı + 4 çubuklu tepsi · köprü · piston SFU1610 · devirme parmağı · U flap katlayıcı · kapak kolu · 7 × NEMA 23", "1", "830 × 830 × 2030 · gövde 123'ten · tepsi 1104 · şarjör 567 kutu (2 gün = 560)"),
        ("ROBOT", "Fairino FR5 · TEK ROBOT · yer rayında · omuz 970 · hamur: çekmece → tabla · kutu (çatal) → QR · içecek + tatlı", "1", "bilek mesafesi: tabla %d · kutu %d (sınır %d)" % (round(D1), round(D2), round(ERISIM))),
        ("RAY", "yer rayı · tek araba · ekseni hat yüzünden 360", "1", "araba merkezi x 200 – %s" % sayi(HAT - 200.0)),
        ("QR DOLABI", "2 × 6 göz · göz 480 × 190 × 440 · koridorun karşısında, hattın sağ ucunda", "1", "x %s–%s · ayrıntı SERVİS_TESLİM paftası" % (sayi(QRX[0]), sayi(QRX[1]))),
        ("BULAŞIK MAKİNESİ", "TEZGÂH ALTI · MEIKO M-iClean UM sınıfı · sepet 500 × 500 · giriş 315 · 40 sepet/saat", "1", "460 × 600 × 730 · F taban dolabında (123–1060) · KASET YATIRILARAK yıkanır · çalışma diski Ø340 düz yatar"),
        ("YEDEK STOK", "İÇECEK 97 kutu + 8 tatlı (K üst bölme, 2 kat) · KUTU yedeği YOK: şarjör 567 kutu = 2 gün", "", "robotun erişiminde DEĞİL — eleman günlük olarak ana gözlere aktarır"),
        ("TEMİZLİK", "deterjan · bez · eldiven · poşet: B modülü K4 temizlik nişi (2 × 5 L bidon) · makine deterjanı + parlatıcı: bulaşık makinesinin yanında", "", "dükkânda yalnız LAVABO kalır"),
        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F taban dolabı · TOPPING'in kendi panosu üst bantta · ekran yok (tablet)", "", ""),
    ])
    lejant()
    yol = KLASOR + r"\HAT_ATOSA_TABLALI_v9_HD.png"
    im.save(yol, dpi=(int(200 * K_HD), int(200 * K_HD))); print("yazildi:", yol, "· hat", sayi(HAT), "· bilek", round(D1), round(D2))
    return yol


if __name__ == "__main__":
    yol = tablali()
    hd = Image.open(yol)
    k = hd.resize((7990, int(hd.size[1] * 7990 / hd.size[0])), Image.LANCZOS)
    k.save(KLASOR + r"\HAT_ATOSA_TABLALI_v9_EKRAN.png", optimize=True); print("yazildi EKRAN", k.size)
