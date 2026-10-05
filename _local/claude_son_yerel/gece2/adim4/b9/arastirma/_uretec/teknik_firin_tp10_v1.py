# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN · GERÇEK KATALOG FIRINI · Sveba Dahlen TP Infinity TP10 · TEKNİK RESİM v1 (26 Eyl 2026)
Kemal: "bana internetten ölçülerini bulduğun bir fırın çizimi yap, konveyör bantlı, bize uyan; senin fırın çok basit,
teknik istiyorum; bize bakan köşesinde çıkıntılar yapmışsın, fırının dışına çıkmış parçalar".
Seçim: 87 kayıt tarandı (Middleby/CTX/LongWave, Lincoln, Star, Blodgett, XLT, TurboChef, Ovention, Moretti, Zanolli,
Senoven/Öztiryakiler...). 830 derinliğe sığıp tek şeritte en uzun ısıtılan boyu veren TP10 (0,34 m² / 381 bant = 892).
KAYNAK: Sveba Dahlen broşür 990004-002 (Oca 2024) s.6 ölçü çizimi + ürün sayfası + opsiyon föyü 990004-002-2 (Ara 2025).
  https://sveba.com/sites/default/files/2024-02/TP%20Pizza-Series_990004-002_EN.pdf
  https://sveba.com/en/products/ovens/tunnel-pizza-oven-tp-infinity
Föyde YAZILI: toplam 1550 · derinlik 730 · yükseklik 599–637 (ayak 82–120) · bant 381 × 1450 · iç yükseklik 85 · 9,5 kW ·
  25 A · 160 kg · 400 °C · 0,34 m² · plaka max 390. "≈" işaretli olanlar föy çiziminden ölçekle/hesapla (üreticiden teyit).
Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda. 3B modele DOKUNULMADI (Kemal onayı bekleniyor).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

K_HD = 2.0


def _ol(v):
    if isinstance(v, (int, float)):
        return v * K_HD
    if isinstance(v, (list, tuple)):
        return [_ol(x) for x in v]
    return v


class HDraw:
    def __init__(self, im):
        self.d = ImageDraw.Draw(im); self._font = {}

    def _f(self, f):
        if f is None:
            return None
        k = id(f)
        if k not in self._font:
            try:
                self._font[k] = ImageFont.truetype(f.path, max(1, int(round(f.size * K_HD))))
            except Exception:
                self._font[k] = f
        return self._font[k]

    def _w(self, kw):
        if "width" in kw and isinstance(kw["width"], (int, float)):
            kw["width"] = max(1, int(round(kw["width"] * K_HD)))
        if "font" in kw:
            kw["font"] = self._f(kw["font"])
        return kw

    def text(self, xy, s, **kw): return self.d.text(_ol(xy), s, **self._w(kw))
    def line(self, xy, **kw): return self.d.line(_ol(xy), **self._w(kw))
    def rectangle(self, xy, **kw): return self.d.rectangle(_ol(xy), **self._w(kw))
    def ellipse(self, xy, **kw): return self.d.ellipse(_ol(xy), **self._w(kw))
    def polygon(self, xy, **kw): return self.d.polygon(_ol(xy), **self._w(kw))
    def textlength(self, s, font=None, **kw): return self.d.textlength(s, font=self._f(font), **kw) / K_HD


KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX, S = 3330, 2930, 0.8
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
PASL, SICAK, TURUNCU, URUN = (232, 234, 238), (255, 226, 214), (200, 90, 30), (240, 214, 170)
PUC, EVC, KOMSU = (255, 240, 200), (220, 235, 255), (150, 150, 158)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f30 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(44, True)
f8b = F(16, True)
im = d = None


def txt(x, y, s, f=None, c=INK, a="la"):
    d.text((x, y), s, font=f or f11, fill=c, anchor=a)


def sayi(v):
    return ("%g" % round(v, 1)).replace(".", ",")


def olcu_h(x0, x1, y, s, f=None, c=INK):
    f = f or f9
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 5, y - 12, (x0 + x1) / 2 + tw / 2 + 5, y + 12], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=None, c=INK, yon="r"):
    f = f or f9
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (10 if yon == "r" else -10), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def dline(p0, p1, c, w=1, dash=7, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0 = min(1.0, i * (dash + gap) / L); t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1, dash=7, gap=4):
    dline((x0, y0), (x1, y0), c, w, dash, gap); dline((x1, y0), (x1, y1), c, w, dash, gap)
    dline((x1, y1), (x0, y1), c, w, dash, gap); dline((x0, y1), (x0, y0), c, w, dash, gap)


def eksen(p0, p1, c):
    dline(p0, p1, c, 1, 22, 5)


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=10):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def isaret(x, y, n):
    """kırmızı daire içinde çakışma numarası"""
    d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=RED)
    txt(x, y, str(n), f8b, BG, "mm")


def etiket(x, y, s, f=None, c=INK, a="mm", cer=None):
    f = f or f7
    tw = d.textlength(s, font=f)
    ox = {"mm": -tw / 2, "lm": 0, "rm": -tw}[a]
    d.rectangle([x + ox - 5, y - 10, x + ox + tw + 5, y + 10], fill=BG, outline=cer)
    txt(x, y, s, f, c, a)


def cagir(x0, y0, x1, y1, s, f=None, c=INK, a="lm"):
    """ok çizgisi + etiket (parça adı)"""
    d.line([(x0, y0), (x1, y1)], fill=c, width=1)
    d.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=c)
    txt(x1 + (6 if a == "lm" else -6), y1, s, f or f7, c, a)


# ============================== VERİ ==============================
# Hat (pafta v12 = montaj v46)
X_F0, X_F1, H_MAK, DZ, Y_ALT, H_B = 2500.0, 4000.0, 2030.0, 830.0, 123.0, 1060.0
BANT_F, PLAKA_K, P_SUREC, ZT = 1166.0, 1164.0, 1168.0, -170.0
# TOPPING (topping_cad_v22 + topping_hesap_v6, dünya = yerel + 700): tabla aktarma konumu, çalışma diski Ø340
TAB_XC, TAB_R, AKT_X0, AKT_X1 = 700.0 + 1637.0, 170.0, 700.0 + 1815.0 - 11.5, 700.0 + 2195.0 + 31.5   # bant dış uçları: burun Ø20 + tahrik Ø60 + bant 1,5
# K (kesme_cad_v1, dünya = yerel + 4000): kuyruk rulosu x 37 Ø30 · PU bant 400 (z −412…−12) · üst 1164
K_KUY, K_KR, K_Z0, K_Z1 = 4000.0 + 37.0, 15.0, -412.0, -12.0
# HAVA ana hattı (montaj v46 ölçümü): z −735…−795 · y 646…1252
HAVA_Z, HAVA_Y = (-795.0, -735.0), (646.0, 1252.0)

# TP10 (föy + ≈ föy çiziminden)
L_TOP, D_TP, H_GOV, BANT_W, BANT_L, ODA, AGIZ = 1550.0, 730.0, 517.0, 381.0, 1450.0, 892.0, 85.0
L_GOV = 960.0                       # ≈ çizimden 952–964 · TP10/20 sehpası 960 × 730
UC = (L_TOP - L_GOV) / 2.0          # ≈ 295 uç kutusu
BANT_GOV = 203.0                    # ≈ bant üstü gövde altından (föyde yok, ±20)
UC_Y = (107.0, 277.0)               # ≈ uç kutusu alt/üst (gövde altından, çizimden)
ON_DUVAR, ODA_D, PANEL_D = 69.0, 422.0, 239.0   # ≈ uç görünüşü: ekran olmayan yan duvar · oda · teknik bölme
CERCEVE = 431.0                     # ≈ konveyör çerçeve genişliği (bant 381 + 2 × 25) VARSAYIM
FAN_D, FAN_X, FAN_Y = 133.0, 148.0, 194.0   # ≈ uç kutusu fanı (ekran tarafı)
EKRAN = (189.0, 240.0, 391.0)       # ≈ dokunmatik ekran genişlik · alt · üst (gövde altından)
ADIM = 310.0                        # ürün adımı (Ø300 + 10) [hat kuralı]

# Yerleşim (F'de ORTALI, ayaksız, ekran ARKADA → bant hat yüzüne en yakın)
XC = (X_F0 + X_F1) / 2.0
X0, X1 = XC - L_TOP / 2.0, XC + L_TOP / 2.0            # 2475 … 4025
G0, G1 = XC - L_GOV / 2.0, XC + L_GOV / 2.0            # 2770 … 3730
B0, B1 = XC - BANT_L / 2.0, XC + BANT_L / 2.0          # 2525 … 3975
H0, H1 = XC - ODA / 2.0, XC + ODA / 2.0                # 2804 … 3696
YG0 = BANT_F - BANT_GOV                                # 963 gövde altı
YG1 = YG0 + H_GOV                                      # 1480 gövde üstü
Z_ON, Z_ARKA = 0.0, -D_TP                              # 0 … −730
ZB_C = -(ON_DUVAR + ODA_D / 2.0)                        # −280 bant ekseni
ZB0, ZB1 = ZB_C + BANT_W / 2.0, ZB_C - BANT_W / 2.0     # −89,5 … −470,5
ZC0, ZC1 = ZB_C + CERCEVE / 2.0, ZB_C - CERCEVE / 2.0   # −64,5 … −495,5
Z_PANEL = -(ON_DUVAR + ODA_D)                           # −491
DAV = (YG1 + 10.0, 2028.0)
N_ICERIDE = ODA / ADIM

# ============================== YERLEŞİM ==============================
FX0, FXM = 150.0, 2150.0                 # ön görünüş: x mm 2150 … 4350
FY = 300.0 + H_MAK * S                   # y=0 çizgisi
PY0 = FY + 250.0                         # üst görünüş: z = −830 buradan
SX0 = FX0 + (4350.0 - FXM) * S + 330.0   # yan kesit: z = −830 buradan
LX0 = SX0 - 60.0                         # parça listesi: yan kesitin altında
LY0 = FY + 150.0


def fx(x): return FX0 + (x - FXM) * S
def fy(y): return FY - y * S
def pz(z): return PY0 + (z + DZ) * S     # üst görünüş: arka yukarıda, ön (z 0) aşağıda
def sx(z): return SX0 + (z + DZ) * S     # yan kesit (soldan bakış): arka solda, ön sağda


def balon(x0, y0, x1, y1, n):
    """parça numarası balonu (parça listesine bağlanır)"""
    d.line([(x0, y0), (x1, y1)], fill=INK, width=1)
    d.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=INK)
    d.ellipse([x1 - 15, y1 - 15, x1 + 15, y1 + 15], fill=BG, outline=INK, width=2)
    txt(x1, y1, str(n), f8b, INK, "mm")


def urun_x():
    n = int(round(N_ICERIDE))
    return [XC + (i - (n - 1) / 2.0) * ADIM for i in range(n)]


# ============================== ÖN KESİT A-A ==============================
def on_kesit():
    txt(FX0, 172, "ÖN GÖRÜNÜŞ · KESİT A-A (bant ekseni z %s)" % sayi(ZB_C), f16, ACC)
    for xx, ad in ((X_F0, "C | F"), (X_F1, "F | K")):
        dline((fx(xx), fy(H_MAK) - 10), (fx(xx), fy(0) + 10), ACC, 2, 12, 6)
        txt(fx(xx), fy(H_MAK) - 24, ad, f7, ACC, "mm")
    d.rectangle([fx(X_F0), fy(H_MAK), fx(X_F1), fy(0)], outline=LINE, width=3)
    # süpürgelik + taban dolabı (üst 963)
    d.rectangle([fx(X_F0 + 30), fy(Y_ALT), fx(X_F1 - 30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(X_F0), fy(YG0), fx(X_F1), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    txt(fx(XC), fy((Y_ALT + YG0) / 2), "içerik v12 ile aynı · üstü %s" % sayi(YG0), f7, GRAY, "mm")
    balon(fx(XC - 300), fy(600), fx(XC - 420), fy(700), 11)
    # davlumbaz (bizim)
    d.rectangle([fx(X_F0 + 3), fy(DAV[1]), fx(X_F1 - 3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    txt(fx(XC), fy((DAV[0] + DAV[1]) / 2), "fan + yağ/karbon filtre · TP10 için üretici davlumbazı yok", f7, GRAY, "mm")
    balon(fx(XC - 420), fy(1850), fx(XC - 540), fy(1930), 12)
    # ---- TP10 gövdesi (kesit) ----
    d.rectangle([fx(G0), fy(YG1), fx(G1), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(fx(G0) + 2, fy(YG1) + 2, fx(G1) - 2, fy(YG0) - 2, (214, 216, 222), 9)
    oy0, oy1 = BANT_F - 16.0, BANT_F + AGIZ
    d.rectangle([fx(H0), fy(YG1 - 60.0), fx(H1), fy(YG0 + 60.0)], fill=BG, outline=GRAY, width=1)
    d.rectangle([fx(G0), fy(oy1), fx(G1), fy(oy0)], fill=SICAK, outline=None)
    for (ya, yb) in ((oy1 + 10.0, oy1 + 30.0), (oy0 - 34.0, oy0 - 14.0)):
        d.rectangle([fx(H0 + 20), fy(yb), fx(H1 - 20), fy(ya)], fill=(250, 190, 160), outline=TURUNCU, width=1)
        for i in range(12):
            xx = H0 + 50.0 + i * (ODA - 100.0) / 11.0
            d.line([(fx(xx), fy(yb) + 2), (fx(xx), fy(ya) - 2)], fill=TURUNCU, width=1)
    txt(fx(XC), fy(oy1 + 48.0), "şematik (föyde iç yerleşim yok)", f7, TURUNCU, "mm")
    # bant + rulolar
    RR = 18.0
    for xr in (B0 + RR, B1 - RR):
        d.ellipse([fx(xr - RR), fy(BANT_F), fx(xr + RR), fy(BANT_F - 2 * RR)], fill=EVC, outline=INK, width=2)
    d.line([(fx(B0 + RR), fy(BANT_F)), (fx(B1 - RR), fy(BANT_F))], fill=INK, width=4)
    d.line([(fx(B0 + RR), fy(BANT_F - 2 * RR)), (fx(B1 - RR), fy(BANT_F - 2 * RR))], fill=GRAY, width=2)
    for xm in urun_x():
        d.rectangle([fx(xm - 150), fy(BANT_F + 12), fx(xm + 150), fy(BANT_F + 1)], fill=URUN, outline=(180, 140, 70), width=1)
    # uç kutuları + gergi düğmeleri
    for ux0, ux1 in ((X0, G0), (G1, X1)):
        d.rectangle([fx(ux0), fy(YG0 + UC_Y[1]), fx(ux1), fy(YG0 + UC_Y[0])], outline=INK, width=2)
        kx = ux0 + 78.0 if ux0 < XC else ux1 - 84.0
        d.rectangle([fx(kx - 15), fy(YG0 + UC_Y[1] + 46), fx(kx + 15), fy(YG0 + UC_Y[1])], fill=FILL, outline=INK, width=1)
    # balonlar
    balon(fx(G0 + 30), fy(YG1 - 40), fx(G0 + 30) - 60, fy(YG1) - 40, 1)
    balon(fx(H0 + 120), fy(BANT_F + 60), fx(H0 + 60), fy(YG1) - 40, 2)
    balon(fx(H1 - 120), fy(oy1 + 20), fx(H1 - 60), fy(YG1) - 40, 3)
    balon(fx(XC + 200), fy(BANT_F), fx(XC + 260), fy(YG0) + 30, 4)
    balon(fx(G1 + 200), fy(YG0 + UC_Y[0] + 20), fx(G1 + 150), fy(YG0) + 30, 5)
    balon(fx(X1 - 84), fy(YG0 + UC_Y[1] + 46), fx(X1 - 30), fy(YG1) - 40, 6)
    # ölçüler
    olcu_h(fx(H0), fx(H1), fy(YG1) - 100, "ısıtılan boy ≈ %s  ·  aynı anda ≈ %s ürün (adım %s)" % (sayi(ODA), sayi(round(N_ICERIDE, 1)), sayi(ADIM)), f8, TURUNCU)
    olcu_h(fx(G0), fx(G1), fy(YG1) - 140, "gövde ≈ %s" % sayi(L_GOV), f8, INK)
    olcu_h(fx(X0), fx(X1), fy(YG1) - 180, "TP10  %s  (föy)" % sayi(L_TOP), f9, INK)
    for xx in (X0, X1, G0, G1):
        dline((fx(xx), fy(YG1) - 186), (fx(xx), fy(YG0 + UC_Y[1]) - 2 if xx in (X0, X1) else fy(YG1) - 2), GRAY, 1, 4, 4)
    olcu_h(fx(X0), fx(G0), fy(YG0 + UC_Y[1]) - 70, "≈ %s" % sayi(UC), f7, INK)
    olcu_h(fx(G1), fx(X1), fy(YG0 + UC_Y[1]) - 70, "≈ %s" % sayi(UC), f7, INK)
    olcu_h(fx(B0), fx(B1), fy(YG0) + 80, "bant %s × %s (föy)" % (sayi(BANT_W), sayi(BANT_L)), f8, INK)
    for xx in (B0, B1):
        dline((fx(xx), fy(BANT_F) + 4), (fx(xx), fy(YG0) + 86), GRAY, 1, 4, 4)
    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "F modülü %s" % sayi(X_F1 - X_F0), f9, ACC)
    olcu_h(fx(X0), fx(X_F0), fy(YG0) + 130, "25", f7, RED)
    olcu_h(fx(X_F1), fx(X1), fy(YG0) + 130, "25", f7, RED)
    isaret(fx(X0) - 24, fy(YG0) + 130, 1); isaret(fx(X1) + 24, fy(YG0) + 130, 1)
    # istasyon tabanı kuralı
    dline((fx(X_F0), fy(H_B)), (fx(X_F1), fy(H_B)), RED, 2, 10, 5)
    txt(fx(X_F0) + 10, fy(H_B) + 16, "istasyon tabanı kuralı %s" % sayi(H_B), f7, RED, "lm")
    isaret(fx(X_F0) + 30 + d.textlength("istasyon tabanı kuralı 1060", font=f7), fy(H_B) + 16, 2)
    # kot ölçüleri (sağda)
    for yy in (0.0, Y_ALT, YG0, H_B, BANT_F, BANT_F + AGIZ, YG1, H_MAK):
        c = RED if yy == H_B else INK
        d.line([(fx(4350) - 20, fy(yy)), (fx(4350) - 4, fy(yy))], fill=c, width=2)
        txt(fx(4350), fy(yy), sayi(yy), f7, c, "lm")
    # ---- KOMŞULAR ----
    d.rectangle([fx(TAB_XC - TAB_R), fy(P_SUREC), fx(TAB_XC + TAB_R), fy(P_SUREC - 22.0)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(TAB_XC - 140), fy(P_SUREC + 9), fx(TAB_XC + 140), fy(P_SUREC)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X0) - 16, fy(1320), "TOPPING çalışma diski Ø340", f7, KOMSU, "rm")
    txt(fx(X0) - 16, fy(1320) + 20, "aktarma konumu · kenar x %s" % sayi(TAB_XC + TAB_R), f7, KOMSU, "rm")
    drect(fx(AKT_X0), fy(BANT_F), fx(AKT_X1), fy(BANT_F - 62.0), RED, 2)
    txt(fx(X0) - 16, fy(BANT_F - 62.0) + 4, "mevcut aktarma bandı", f7, RED, "rm")
    txt(fx(X0) - 16, fy(BANT_F - 62.0) + 24, "x %s–%s" % (sayi(AKT_X0), sayi(AKT_X1)), f7, RED, "rm")
    isaret(fx(TAB_XC + TAB_R) - 4, fy(P_SUREC) - 40, 4)
    kx1 = 4330.0
    d.ellipse([fx(K_KUY - K_KR), fy(PLAKA_K - 2.0), fx(K_KUY + K_KR), fy(PLAKA_K - 2.0 - 2 * K_KR)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(K_KUY), fy(PLAKA_K), fx(kx1), fy(PLAKA_K - 4.0)], fill=KOMSU)
    txt(fx(kx1), fy(PLAKA_K) - 18, "K bandı %s" % sayi(PLAKA_K), f7, KOMSU, "rm")
    isaret(fx(K_KUY) + 44, fy(PLAKA_K - 2.0 - 2 * K_KR) + 24, 5)
    yo = fy(YG0 + UC_Y[1]) - 30
    olcu_h(fx(B1), fx(K_KUY), yo, sayi(K_KUY - B1), f7, INK)
    dline((fx(B1), yo), (fx(B1), fy(BANT_F)), GRAY, 1, 4, 4)
    dline((fx(K_KUY), yo), (fx(K_KUY), fy(PLAKA_K)), GRAY, 1, 4, 4)


# ============================== ÜST GÖRÜNÜŞ ==============================
def ust():
    txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ", f16, ACC)
    d.rectangle([fx(X_F0), pz(-DZ), fx(X_F1), pz(0)], outline=LINE, width=3)
    txt(fx(X_F0) + 8, pz(0) + 18, "hat ön yüzü (z 0)", f7, GRAY, "lm")
    d.rectangle([fx(K_KUY - K_KR), pz(K_Z0), fx(4330), pz(K_Z1)], fill=(240, 240, 243), outline=KOMSU, width=2)
    txt(fx(4330) - 6, pz(K_Z0) + 14, "K bandı 400", f7, KOMSU, "rm")
    d.rectangle([fx(2400), pz(HAVA_Z[0]), fx(4300), pz(HAVA_Z[1])], fill=(236, 240, 246), outline=GRAY, width=1)
    txt(fx(2400) + 6, pz(sum(HAVA_Z) / 2), "hava ana hattı (mevcut)", f7, GRAY, "lm")
    d.rectangle([fx(G0), pz(Z_ARKA), fx(G1), pz(Z_ON)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(G0), pz(Z_ARKA), fx(G1), pz(Z_PANEL)], fill=(222, 226, 232), outline=INK, width=1)
    d.rectangle([fx(XC - EKRAN[0] / 2), pz(Z_ARKA) - 2, fx(XC + EKRAN[0] / 2), pz(Z_ARKA) + 7], fill=INK)
    balon(fx(XC + 60), pz(Z_ARKA) + 4, fx(XC + 200), pz(Z_ARKA) + 60, 7)
    balon(fx(XC - 200), pz(Z_PANEL + 120), fx(XC - 300), pz(Z_PANEL + 60), 8)
    for ux0, ux1 in ((X0, G0), (G1, X1)):
        d.rectangle([fx(ux0), pz(ZC1), fx(ux1), pz(ZC0)], fill=FILL, outline=INK, width=2)
        fx_ = ux0 + FAN_X if ux0 < XC else ux1 - FAN_X
        d.rectangle([fx(fx_ - FAN_D / 2), pz(ZC1) - 3, fx(fx_ + FAN_D / 2), pz(ZC1) + 5], fill=GRAY)
    balon(fx(X1 - 60), pz(ZC0 - 20), fx(X1 + 40), pz(ZC0) + 40, 5)
    d.rectangle([fx(B0), pz(ZB1), fx(B1), pz(ZB0)], fill=EVC, outline=INK, width=1)
    for i in range(0, int(BANT_L), 40):
        d.line([(fx(B0 + i), pz(ZB1) + 1), (fx(B0 + i), pz(ZB0) - 1)], fill=(190, 205, 225), width=1)
    drect(fx(H0), pz(ZB1 - 10), fx(H1), pz(ZB0 + 10), TURUNCU, 2)
    for xm in urun_x():
        d.ellipse([fx(xm - 150), pz(ZB_C - 150), fx(xm + 150), pz(ZB_C + 150)], outline=(180, 140, 70), width=2)
    eksen((fx(2150), pz(ZT)), (fx(4350), pz(ZT)), ACC)
    txt(fx(4330) - 6, pz(ZT) + 14, "hat ürün ekseni z %s" % sayi(ZT), f7, ACC, "rm")
    eksen((fx(X0 - 40), pz(ZB_C)), (fx(X1 + 40), pz(ZB_C)), TURUNCU)
    txt(fx(4330) - 6, pz(ZB_C) - 14, "TP10 bant ekseni z %s" % sayi(ZB_C), f7, TURUNCU, "rm")
    olcu_v(fx(G0 + 70), pz(ZB_C), pz(ZT), sayi(ZT - ZB_C), f8b, RED, "r")
    isaret(fx(G0 + 70) + 70, pz((ZT + ZB_C) / 2), 3)
    d.ellipse([fx(TAB_XC - TAB_R), pz(ZT - TAB_R), fx(TAB_XC + TAB_R), pz(ZT + TAB_R)], outline=KOMSU, width=2)
    d.ellipse([fx(TAB_XC - 140), pz(ZT - 140), fx(TAB_XC + 140), pz(ZT + 140)], outline=(180, 140, 70), width=1)
    drect(fx(AKT_X0), pz(ZT - 145), fx(AKT_X1), pz(ZT + 145), RED, 2)
    isaret(fx(TAB_XC + TAB_R) - 4, pz(ZT - TAB_R) - 18, 4)
    isaret(fx(K_KUY) + 40, pz(K_Z0) - 18, 5)
    # ölçüler (sağda)
    xr = fx(4350) + 30
    olcu_v(xr, pz(Z_ARKA), pz(Z_ON), "%s (föy)" % sayi(D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(Z_ARKA), sayi(DZ - D_TP), f7, INK, "r")
    olcu_v(fx(B1 - 30), pz(ZB1), pz(ZB0), sayi(BANT_W), f7, INK, "l")
    olcu_v(fx(G1) - 40, pz(Z_PANEL), pz(Z_ON), "≈ %s + %s" % (sayi(ON_DUVAR), sayi(ODA_D)), f7, INK, "l")
    olcu_v(fx(G1) - 40, pz(Z_ARKA), pz(Z_PANEL), "≈ %s" % sayi(PANEL_D), f7, INK, "l")


# ============================== YAN KESİT B-B ==============================
def yan():
    txt(SX0, 172, "YAN KESİT B-B (x %s · soldan bakış)" % sayi(XC), f16, ACC)
    d.rectangle([sx(-DZ), fy(H_MAK), sx(0), fy(0)], outline=LINE, width=3)
    d.rectangle([sx(-DZ + 30), fy(Y_ALT), sx(-30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([sx(-DZ), fy(YG0), sx(0), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    balon(sx(-400), fy(600), sx(-300), fy(700), 11)
    dline((sx(-DZ), fy(H_B)), (sx(0), fy(H_B)), RED, 2, 10, 5)
    d.rectangle([sx(-DZ + 3), fy(DAV[1]), sx(-3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    balon(sx(-400), fy(1850), sx(-300), fy(1930), 12)
    d.rectangle([sx(HAVA_Z[0]), fy(HAVA_Y[1]), sx(HAVA_Z[1]), fy(HAVA_Y[0])], fill=(236, 240, 246), outline=GRAY, width=1)
    txt(sx(sum(HAVA_Z) / 2), fy(HAVA_Y[0]) + 16, "hava hattı", f7, GRAY, "mm")
    # gövde
    d.rectangle([sx(Z_ARKA), fy(YG1), sx(Z_ON), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(Z_ON - ON_DUVAR), fy(YG1) + 2, sx(Z_ON) - 2, fy(YG0) - 2, (214, 216, 222), 9)
    d.rectangle([sx(Z_ARKA), fy(YG1), sx(Z_PANEL), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((Z_ARKA + Z_PANEL) / 2), fy((YG0 + YG1) / 2), sx((Z_ARKA + Z_PANEL) / 2) - 40, fy(YG1) - 40, 8)
    d.rectangle([sx(Z_ARKA) - 7, fy(EKRAN[2] + YG0), sx(Z_ARKA) + 2, fy(EKRAN[1] + YG0)], fill=INK)
    balon(sx(Z_ARKA) - 4, fy(YG0 + EKRAN[2] - 30), sx(-DZ) - 40, fy(YG0 + EKRAN[2] + 60), 7)
    oy0, oy1 = BANT_F - 16.0, BANT_F + AGIZ
    d.rectangle([sx(Z_PANEL), fy(oy1), sx(Z_ON - ON_DUVAR), fy(oy0)], fill=SICAK)
    for (ya, yb) in ((oy1 + 10.0, oy1 + 30.0), (oy0 - 34.0, oy0 - 14.0)):
        d.rectangle([sx(Z_PANEL + 15), fy(yb), sx(Z_ON - ON_DUVAR - 15), fy(ya)], fill=(250, 190, 160), outline=TURUNCU, width=1)
    balon(sx(Z_PANEL + 60), fy(oy1 + 20), sx(Z_PANEL + 100), fy(YG1) - 40, 3)
    d.rectangle([sx(ZB1), fy(BANT_F), sx(ZB0), fy(BANT_F - 6)], fill=INK)
    balon(sx(ZB1 + 40), fy(BANT_F - 3), sx(ZB1 + 80), fy(YG0) + 40, 4)
    d.rectangle([sx(ZB_C - 150), fy(BANT_F + 12), sx(ZB_C + 150), fy(BANT_F + 1)], fill=URUN, outline=(180, 140, 70), width=1)
    drect(sx(ZT - 150), fy(BANT_F + 12), sx(ZT + 150), fy(BANT_F + 1), RED, 2, 5, 3)
    isaret(sx(ZT), fy(BANT_F + 12) - 26, 3)
    # ölçüler
    olcu_h(sx(Z_ARKA), sx(Z_ON), fy(H_MAK) - 30, "%s (föy)" % sayi(D_TP), f8, INK)
    olcu_h(sx(-DZ), sx(Z_ARKA), fy(H_MAK) - 30, sayi(DZ - D_TP), f7, INK)
    olcu_h(sx(-DZ), sx(0), fy(H_MAK) - 70, "F %s" % sayi(DZ), f8, ACC)
    olcu_h(sx(Z_ARKA), sx(Z_PANEL), fy(YG0) + 90, "≈ %s" % sayi(PANEL_D), f7, INK)
    olcu_h(sx(Z_PANEL), sx(Z_ON - ON_DUVAR), fy(YG0) + 90, "≈ %s" % sayi(ODA_D), f7, INK)
    olcu_h(sx(Z_ON - ON_DUVAR), sx(Z_ON), fy(YG0) + 90, "≈ %s" % sayi(ON_DUVAR), f7, INK)
    olcu_h(sx(ZB1), sx(ZB0), fy(YG0) + 130, "bant %s" % sayi(BANT_W), f7, INK)
    for zz in (Z_ARKA, Z_PANEL, Z_ON - ON_DUVAR, ZB1, ZB0):
        dline((sx(zz), fy(YG0) + 4), (sx(zz), fy(YG0) + (136 if zz in (ZB1, ZB0) else 96)), GRAY, 1, 4, 4)
    xd = sx(0) + 110
    olcu_v(xd, fy(YG1), fy(YG0), "≈ %s" % sayi(H_GOV), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F), fy(YG0), "≈ %s" % sayi(BANT_GOV), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F + AGIZ), fy(BANT_F), "%s (föy)" % sayi(AGIZ), f7, INK, "r")
    for yy in (Y_ALT, YG0, H_B, BANT_F, BANT_F + AGIZ, YG1, H_MAK):
        c = RED if yy == H_B else INK
        d.line([(sx(0) + 6, fy(yy)), (sx(0) + 22, fy(yy))], fill=c, width=2)
        txt(sx(0) + 28, fy(yy), sayi(yy), f7, c, "lm")
    isaret(sx(0) + 330, fy((H_B + YG0) / 2), 2)
    txt(sx(-DZ), fy(0) + 26, "arka (z −830)", f7, GRAY, "lm")
    txt(sx(0), fy(0) + 26, "ön (z 0)", f7, GRAY, "rm")


# ============================== LİSTE + BAŞLIK ==============================
def liste():
    x0, y0 = LX0, LY0
    txt(x0, y0 - 38, "PARÇA LİSTESİ", f16, ACC)
    satir = [
        ("1", "TP10 gövdesi · paslanmaz · yalıtımlı", "≈ 960 × 730 × 517", "föy + çizim"),
        ("2", "Pişirme odası · kızılötesi · fansız", "≈ 892 × 422 · ağız 85", "föy"),
        ("3", "Üst + alt IR ısıtıcı · 2 bölge", "400 °C · 9,5 kW", "föy"),
        ("4", "Konveyör bandı", "381 × 1450", "föy"),
        ("5", "Uç kutusu × 2 (bant ucu + fan)", "≈ 295 · fan ≈ Ø133", "çizim"),
        ("6", "Bant gergi düğmesi × 2", "—", "çizim"),
        ("7", "Dokunmatik ekran · arka yüz", "≈ 189 × 151", "çizim"),
        ("8", "Teknik bölme (sürücü · kontaktör)", "≈ 239", "çizim"),
        ("9", "Ayak 82–120 · SÖKÜLÜR", "—", "föy"),
        ("10", "Giriş/çıkış plakası · TAKILMAZ", "max 390", "föy"),
        ("11", "F taban dolabı (bizim)", "üst 963", "hesap"),
        ("12", "Egzoz davlumbazı (bizim)", "1490–2028", "pafta v12"),
    ]
    kol = (0, 46, 480, 760)
    gen = 960.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("NO", "PARÇA", "ÖLÇÜ", "KAYNAK")):
        txt(x0 + k + 8, y0 + 14, b, f7, INK, "lm")
    y = y0 + 28
    for r in satir:
        d.line([(x0, y + 28), (x0 + gen, y + 28)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            txt(x0 + k + 8, y + 14, v, f7, INK if k < 760 else GRAY, "lm")
        y += 28
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    y += 56
    ya = y
    txt(x0, y, "TEKNİK VERİ (föy)", f16, ACC); y += 36
    for a, b in (("Üretici", "Sveba Dahlen, İsveç (Middleby)"), ("Model", "TP Infinity TP10 · 1 kat"),
                 ("Isıtma", "kızılötesi · üst/alt ayrı · fansız"), ("Sıcaklık", "en çok 400 °C"),
                 ("Güç · sigorta", "9,5 kW · 25 A"), ("Gerilim", "föyde yok · 3N 400 V VARSAYIM"),
                 ("Pişirme alanı", "0,34 m²"), ("Ağırlık", "160 kg"), ("Föy", "990004-002 · Ocak 2024")):
        txt(x0, y, a, f7, GRAY, "lm"); txt(x0 + 150, y, b, f7, INK, "lm"); y += 24
    x2, y = x0 + 470, ya
    txt(x2, y, "ÇAKIŞMALAR", f16, RED); y += 36
    for i, s in enumerate(("TP10 1550 > F 1500: komşulara 25 + 25",
                           "gövde altı 963 < istasyon tabanı 1060",
                           "bant ekseni −280 ↔ hat ürün ekseni −170",
                           "uç kutusu 2475 ↔ disk kenarı 2507 + aktarma bandı",
                           "uç kutusu 4025 ↔ K rulosu 4022 · ürün 18 taşar"), 1):
        isaret(x2 + 15, y, i); txt(x2 + 40, y, s, f7, INK, "lm"); y += 34
    y = max(y, ya + 36 + 9 * 24) + 20
    txt(x0, y, "≈ : föy çiziminden ölçekle / hesapla · üreticiden teyit  ·  şematik : iç ısıtıcı yerleşimi föyde yok", f7, GRAY, "lm")


def baslik():
    txt(FX0, 40, "AUTOKITCH  ·  F FIRIN  ·  Sveba Dahlen TP Infinity TP10  ·  TEKNİK RESİM v1", f30, INK)
    txt(FX0, 98, "gerçek katalog fırını F modülünde (1500 × 830 × 2030) · ortalı · ayaksız · bant %s · ekran arkada (servis tarafı) · ölçüler mm · 26 Eylül 2026" % sayi(BANT_F), f11, GRAY)
    d.line([(FX0, 126), (W_PX - 60, 126)], fill=LINE, width=3)


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    baslik(); on_kesit(); ust(); yan(); liste()
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "FIRIN_TP10_v1_teknik.png")
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    print("yazildi:", yol, im.size)
    print("TP10 x %s…%s · gövde %s…%s · bant %s…%s · oda %s…%s · gövde y %s…%s · bant ekseni z %s · içeride %.2f ürün"
          % (X0, X1, G0, G1, B0, B1, H0, H1, YG0, YG1, ZB_C, N_ICERIDE))
    return yol


if __name__ == "__main__":
    ciz()
