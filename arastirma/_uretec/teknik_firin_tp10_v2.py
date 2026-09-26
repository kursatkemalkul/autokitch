# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN DENEMESİ (AYRI SÜRÜM) · Sveba Dahlen TP10 · TEKNİK RESİM v2 (26 Eyl 2026)
v2: ölçüler 3B modelden (firin_tp10_cad_v1 · tek kaynak) · uç kutuları ekran tarafında YAN KUTU (v1 bandı saran kutu sanmıştı) ·
hatta uyarlanmış hali: x 2514–4064 · giriş bandı · 2 çit · destek sacları · K/TOPPING uyarlamaları.
(v1 başlığı:) AUTOKITCH · F FIRIN · GERÇEK KATALOG FIRINI · Sveba Dahlen TP Infinity TP10 · TEKNİK RESİM v1 (26 Eyl 2026)
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
W_PX, H_PX, S = 3370, 2930, 0.8
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


# ============================== VERİ (TEK KAYNAK: firin_tp10_cad_v1 — 3B model ile aynı sayılar) ==============================
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firin_tp10_cad_v1 as FT

X_F0, X_F1, H_MAK, DZ, Y_ALT, H_B = 2500.0, 4000.0, 2030.0, 830.0, 123.0, 1060.0
BANT_F, PLAKA_K, P_SUREC, ZT = FT.BANT_UST_HAT, 1164.0, 1168.0, FT.ZT
TAB_XC, TAB_R = 700.0 + 1637.0, 170.0
K_KUY, K_KR, K_Z0, K_Z1, K_LEV = 4037.0, 15.0, -412.0, -12.0, 4018.0      # K kuyruk rulosu · bant · yan levha başı (TP10 sürümünde 18)
HAVA_Z = (-795.0, -735.0)
YG0, YG1 = FT.YG0, FT.YG1
X0, X1 = FT.X0, FT.X0 + FT.L_TOP
G0, G1 = FT.GOV_X
B0, B1 = FT.BANT_X
H0, H1 = FT.ODA_X
XC = FT.XC_TP
UCY = (YG0 + FT.UC_Y[0], YG0 + FT.UC_Y[1])
UCZ = FT.UC_Z
TUN_Y = (YG0 + FT.TUNEL_Y[0], YG0 + FT.TUNEL_Y[1])
TUN_Z = FT.TUNEL_Z
BZ = FT.BANT_Z
ZB_C = (BZ[0] + BZ[1]) / 2.0
RX0, RX1, RY = FT.hx(-FT.RULO_X), FT.hx(FT.RULO_X), YG0 + FT.RULO_Y
RR = FT.RULO_R + FT.BANT_K
DAV = (YG1 + 10.0, 2028.0)
ADIM = FT.ADIM
N_ICERIDE = FT.ODA / ADIM
ZUF = FT.Z_URUN_FIRIN

# ============================== YERLEŞİM ==============================
FX0, FXM = 150.0, 2150.0
FY = 300.0 + H_MAK * S
PY0 = FY + 250.0
SX0 = FX0 + (4400.0 - FXM) * S + 330.0
LX0 = SX0 - 60.0
LY0 = FY + 150.0


def fx(x): return FX0 + (x - FXM) * S
def fy(y): return FY - y * S
def pz(z): return PY0 + (z + DZ) * S
def sx(z): return SX0 + (z + DZ) * S


def balon(x0, y0, x1, y1, n):
    d.line([(x0, y0), (x1, y1)], fill=INK, width=1)
    d.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=INK)
    d.ellipse([x1 - 15, y1 - 15, x1 + 15, y1 + 15], fill=BG, outline=INK, width=2)
    txt(x1, y1, str(n), f8b, INK, "mm")


def cit_ciz_on(A, B_, c):
    """çiti ön görünüşte y 1167–1192 şeridi olarak"""
    d.rectangle([fx(min(A[0], B_[0])), fy(BANT_F + 26.0), fx(max(A[0], B_[0])), fy(BANT_F + 1.0)], fill=(245, 245, 240), outline=c, width=2)


# ============================== ÖN GÖRÜNÜŞ ==============================
def on():
    txt(FX0, 172, "ÖN GÖRÜNÜŞ (hat önünden · kesik çizgi = gövde içi / arkada)", f16, ACC)
    for xx, ad in ((X_F0, "C | F"), (X_F1, "F | K")):
        dline((fx(xx), fy(H_MAK) - 10), (fx(xx), fy(0) + 10), ACC, 2, 12, 6)
        txt(fx(xx), fy(H_MAK) - 24, ad, f7, ACC, "mm")
    d.rectangle([fx(X_F0), fy(H_MAK), fx(X_F1), fy(0)], outline=LINE, width=3)
    d.rectangle([fx(X_F0 + 30), fy(Y_ALT), fx(X_F1 - 30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(X_F0), fy(YG0), fx(X_F1), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    txt(fx(XC), fy((Y_ALT + YG0) / 2), "içerik v47 ile aynı · üstü %s · pizza kutusu yedeği 505" % sayi(YG0), f7, GRAY, "mm")
    balon(fx(XC - 300), fy(600), fx(XC - 420), fy(700), 13)
    d.rectangle([fx(X_F0 + 3), fy(DAV[1]), fx(X_F1 - 3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    txt(fx(XC), fy((DAV[0] + DAV[1]) / 2), "fan + yağ/karbon filtre · komşu modüllere asılı", f7, GRAY, "mm")
    balon(fx(XC - 420), fy(1850), fx(XC - 540), fy(1930), 14)
    # uç kutuları (ARKADA, ekran tarafı) — görünür (gövdenin iki yanında)
    for ux0, ux1, kx in ((X0, G0, X0 + FT.DUGME_X[0]), (G1, X1, X1 - FT.DUGME_X[1])):
        d.rectangle([fx(ux0), fy(UCY[1]), fx(ux1), fy(UCY[0])], fill=(236, 238, 241), outline=INK, width=2)
        d.rectangle([fx(kx - 15), fy(UCY[1] + 46), fx(kx + 15), fy(UCY[1])], fill=FILL, outline=INK, width=1)
    txt(fx((X0 + G0) / 2), fy(UCY[1]) + 14, "uç kutusu (arkada)", f7, GRAY, "mm")
    # gövde (ekransız ön yüz) + gizli tünel / oda / ısıtıcılar
    d.rectangle([fx(G0), fy(YG1), fx(G1), fy(YG0)], fill=PASL, outline=INK, width=3)
    drect(fx(G0), fy(TUN_Y[1]), fx(G1), fy(TUN_Y[0]), GRAY, 1)
    drect(fx(H0), fy(TUN_Y[1] - 1), fx(H1), fy(BANT_F), TURUNCU, 2)
    for (ya, yb) in ((TUN_Y[1] - 10.0, TUN_Y[1] - 1.0), (RY - 12.0 + FT.RULO_R - FT.RULO_R, RY - 4.0)):
        drect(fx(H0 + 5), fy(yb), fx(H1 - 5), fy(ya), TURUNCU, 1, 5, 3)
    txt(fx(XC), fy(TUN_Y[1] - 30.0), "ısıtılan oda (gizli) · üst + alt IR, 2 bölge (şematik)", f7, TURUNCU, "mm")
    balon(fx(G0 + 30), fy(YG1 - 40), fx(G0 + 30) - 60, fy(YG1) - 40, 1)
    balon(fx(H1 - 120), fy(TUN_Y[1] - 5), fx(H1 - 60), fy(YG1) - 40, 2)
    # bant + rulolar (bant uçları gövde dışında görünür)
    for xr in (RX0, RX1):
        d.ellipse([fx(xr - RR), fy(RY + RR), fx(xr + RR), fy(RY - RR)], fill=EVC, outline=INK, width=2)
    d.line([(fx(B0), fy(BANT_F)), (fx(G0), fy(BANT_F))], fill=INK, width=4)
    d.line([(fx(G1), fy(BANT_F)), (fx(B1), fy(BANT_F))], fill=INK, width=4)
    dline((fx(G0), fy(BANT_F)), (fx(G1), fy(BANT_F)), INK, 2, 10, 5)
    balon(fx(RX1), fy(RY), fx(RX1) + 30, fy(YG0) + 40, 3)
    n = int(round(N_ICERIDE))
    for i in range(n):
        xm = XC + (i - (n - 1) / 2.0) * ADIM
        drect(fx(xm - 150), fy(BANT_F + 12), fx(xm + 150), fy(BANT_F + 1), (180, 140, 70), 1, 5, 3)
    # giriş bandı + motoru · destek sacı · çit
    d.rectangle([fx(FT.GB_XB - 11.5), fy(BANT_F), fx(FT.GB_XT + 11.5), fy(FT.GB_RY - 11.5)], fill=(214, 196, 170), outline=INK, width=1)
    for xr in (FT.GB_XB, FT.GB_XT):
        d.ellipse([fx(xr - 10), fy(FT.GB_RY + 10), fx(xr + 10), fy(FT.GB_RY - 10)], fill=BG, outline=INK, width=1)
    d.rectangle([fx(FT.GB_XT - 28.5), fy(1234.5), fx(FT.GB_XT + 28.5), fy(1177.5)], fill=(60, 62, 68), outline=INK, width=1)
    balon(fx(FT.GB_XT - 20), fy(1234), fx(FT.GB_XT - 60), fy(1380), 6)
    balon(fx(FT.GB_XB), fy(FT.GB_RY), fx(FT.GB_XB - 70), fy(FT.GB_RY - 90), 5)
    cit_ciz_on(FT.GC_A, FT.GC_B, ACC)
    cit_ciz_on(FT.CC_A, FT.CC_B, ACC)
    balon(fx((FT.GC_A[0] + FT.GC_B[0]) / 2), fy(BANT_F + 26), fx((FT.GC_A[0] + FT.GC_B[0]) / 2), fy(BANT_F + 150), 8)
    balon(fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(BANT_F + 26), fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(BANT_F + 150), 9)
    d.line([(fx(B0 + 2), fy(BANT_F - 1)), (fx(G0 - 2), fy(BANT_F - 1))], fill=ACC, width=2)
    d.line([(fx(G1 + 2), fy(BANT_F - 1)), (fx(B1 - 2), fy(BANT_F - 1))], fill=ACC, width=2)
    # komşular: TOPPING diski aktarmada · X tahriki (gizli) · K bandı
    d.rectangle([fx(TAB_XC - TAB_R), fy(P_SUREC), fx(TAB_XC + TAB_R), fy(P_SUREC - 22.0)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(TAB_XC - 140), fy(P_SUREC + 9), fx(TAB_XC + 140), fy(P_SUREC)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X_F0) - 16, fy(1400), "TOPPING diski aktarmada", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1400) + 20, "kenar x %s · üst %s" % (sayi(TAB_XC + TAB_R), sayi(P_SUREC)), f7, KOMSU, "rm")
    drect(fx(2490), fy(1135), fx(2580), fy(1064.5), KOMSU, 1, 5, 3)
    txt(fx(X_F0) - 16, fy(1030), "TOPPING X tahriki (altta)", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1030) + 20, "kaide köşesi pahlı", f7, RED, "rm")
    d.ellipse([fx(K_KUY - K_KR), fy(PLAKA_K - 2.0), fx(K_KUY + K_KR), fy(PLAKA_K - 2.0 - 2 * K_KR)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(K_KUY), fy(PLAKA_K), fx(4380), fy(PLAKA_K - 4.0)], fill=KOMSU)
    txt(fx(4380), fy(PLAKA_K) - 18, "K bandı %s" % sayi(PLAKA_K), f7, KOMSU, "rm")
    # ölçüler
    olcu_h(fx(H0), fx(H1), fy(YG1) - 100, "ısıtılan ≈ %s · aynı anda ≈ %s ürün (adım %s)" % (sayi(round(FT.ODA)), sayi(round(N_ICERIDE, 1)), sayi(ADIM)), f8, TURUNCU)
    olcu_h(fx(G0), fx(G1), fy(YG1) - 140, "gövde ≈ %s" % sayi(FT.L_GOV), f8, INK)
    olcu_h(fx(X0), fx(X1), fy(YG1) - 180, "TP10  %s  (föy)" % sayi(FT.L_TOP), f9, INK)
    olcu_h(fx(B0), fx(B1), fy(YG0) + 70, "bant %s × %s (föy) · %s – %s" % (sayi(FT.BANT_W), sayi(FT.BANT_L), sayi(B0), sayi(B1)), f8, INK)
    for xx in (X0, X1, G0, G1):
        dline((fx(xx), fy(YG1) - 186), (fx(xx), fy(UCY[1]) - 2 if xx in (X0, X1) else fy(YG1) - 2), GRAY, 1, 4, 4)
    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "F modülü %s" % sayi(X_F1 - X_F0), f9, ACC)
    olcu_h(fx(X_F1), fx(X1), fy(UCY[1]) - 40, sayi(X1 - X_F1), f7, RED)
    isaret(fx(X1) + 24, fy(UCY[1]) - 40, 1)
    olcu_h(fx(X_F1), fx(B1), fy(BANT_F) - 40, sayi(B1 - X_F1), f7, RED)
    isaret(fx(B1) + 20, fy(BANT_F) - 40, 1)
    olcu_h(fx(TAB_XC + TAB_R), fx(B0), fy(1262), "disk → TP10 bandı %s" % sayi(B0 - TAB_XC - TAB_R), f7, INK)
    dline((fx(X_F0), fy(H_B)), (fx(X_F1), fy(H_B)), RED, 2, 10, 5)
    txt(fx(G0) + 10, fy(H_B) + 16, "istasyon tabanı kuralı %s (gövde altı %s)" % (sayi(H_B), sayi(YG0)), f7, RED, "lm")
    isaret(fx(G0) + 30 + d.textlength("istasyon tabanı kuralı 1060 (gövde altı 956)", font=f7), fy(H_B) + 16, 2)
    for yy in (0.0, Y_ALT, YG0, H_B, BANT_F, BANT_F + FT.IC_H, YG1, H_MAK):
        c = RED if yy == H_B else INK
        d.line([(fx(4400) - 20, fy(yy)), (fx(4400) - 4, fy(yy))], fill=c, width=2)
        txt(fx(4400), fy(yy), sayi(yy), f7, c, "lm")


# ============================== ÜST GÖRÜNÜŞ ==============================
def ust():
    txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ (ürün yolu: merkez çizgisi · çitler ürünü iter)", f16, ACC)
    d.rectangle([fx(X_F0), pz(-DZ), fx(X_F1), pz(0)], outline=LINE, width=3)
    txt(fx(X_F0) + 8, pz(0) + 18, "hat ön yüzü (z 0)", f7, GRAY, "lm")
    d.rectangle([fx(2400), pz(HAVA_Z[0]), fx(4300), pz(HAVA_Z[1])], fill=(236, 240, 246), outline=GRAY, width=1)
    txt(fx(2400) + 6, pz(sum(HAVA_Z) / 2), "hava ana hattı (mevcut)", f7, GRAY, "lm")
    # K bandı + itici ekseni
    d.rectangle([fx(K_KUY - K_KR), pz(K_Z0), fx(4380), pz(K_Z1)], fill=(240, 240, 243), outline=KOMSU, width=2)
    d.rectangle([fx(K_LEV), pz(K_Z0 - 5), fx(4380), pz(K_Z0 - 2)], fill=KOMSU)
    d.rectangle([fx(4016), pz(-490), fx(4380), pz(-440)], fill=(232, 234, 238), outline=KOMSU, width=1)
    txt(fx(4380) - 6, pz(-465), "K itici ekseni (motor sağ uca)", f7, KOMSU, "rm")
    txt(fx(4380) - 6, pz(K_Z1) + 14, "K bandı 400 · yan levha 18'den", f7, KOMSU, "rm")
    # gövde · tünel · teknik bölme · ekran
    d.rectangle([fx(G0), pz(-FT.D_TP), fx(G1), pz(0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(G0), pz(-FT.D_TP), fx(G1), pz(TUN_Z[0] - 5.5)], fill=(222, 226, 232), outline=INK, width=1)
    drect(fx(G0), pz(TUN_Z[0]), fx(G1), pz(TUN_Z[1]), GRAY, 1)
    d.rectangle([fx(XC - FT.EKRAN[0] / 2), pz(-FT.D_TP) - 2, fx(XC + FT.EKRAN[0] / 2), pz(-FT.D_TP) + 7], fill=INK)
    balon(fx(XC + 60), pz(-FT.D_TP) + 4, fx(XC + 200), pz(-FT.D_TP) + 60, 4)
    # uç kutuları (arkada)
    for ux0, ux1 in ((X0, G0), (G1, X1)):
        d.rectangle([fx(ux0), pz(UCZ[1]), fx(ux1), pz(UCZ[0])], fill=FILL, outline=INK, width=2)
    balon(fx(X1 - 60), pz(-600), fx(X1 + 60), pz(-560), 3)
    # bant + çitler + destek sacları + giriş bandı
    d.rectangle([fx(B0), pz(BZ[0]), fx(B1), pz(BZ[1])], fill=EVC, outline=INK, width=1)
    for i in range(0, int(FT.BANT_L), 40):
        d.line([(fx(B0 + i), pz(BZ[0]) + 1), (fx(B0 + i), pz(BZ[1]) - 1)], fill=(190, 205, 225), width=1)
    drect(fx(H0), pz(BZ[0] - 8), fx(H1), pz(BZ[1] + 8), TURUNCU, 2)
    d.rectangle([fx(B0 + 2), pz(-80), fx(G0 - 2), pz(-12)], fill=(250, 250, 250), outline=ACC, width=1)
    d.rectangle([fx(G1 + 2), pz(-80), fx(B1 - 2), pz(-12)], fill=(250, 250, 250), outline=ACC, width=1)
    balon(fx(2700), pz(-40), fx(2700), pz(0) + 50, 7)
    for A, B_, yon in ((FT.GC_A, FT.GC_B, 1.0), (FT.CC_A, FT.CC_B, -1.0)):
        nx_, nz_ = math.sin(math.radians(20.0)), math.cos(math.radians(20.0))
        pts = [A, B_, (B_[0] + 10 * nx_, B_[1] + yon * 10 * nz_), (A[0] + 10 * nx_, A[1] + yon * 10 * nz_)]
        d.polygon([(fx(p[0]), pz(p[1])) for p in pts], fill=(255, 250, 235), outline=ACC)
    d.rectangle([fx(FT.GB_XB - 11.5), pz(-345.0), fx(FT.GB_XT + 11.5), pz(-25.0)], fill=(214, 196, 170), outline=INK, width=1)
    drect(fx(FT.GB_XT - 28.5), pz(-432.5), fx(FT.GB_XT + 28.5), pz(-368.0), INK, 1, 5, 3)
    # TOPPING diski aktarmada + X tahriki (altta)
    d.ellipse([fx(TAB_XC - TAB_R), pz(ZT - TAB_R), fx(TAB_XC + TAB_R), pz(ZT + TAB_R)], outline=KOMSU, width=2)
    drect(fx(2490), pz(-397.5), fx(2580), pz(-389.5), KOMSU, 1, 4, 3)
    drect(fx(2507), pz(-462), fx(2563), pz(-397.5), KOMSU, 1, 4, 3)
    # ürün yolu + ürünler
    pts = [(fx(x), pz(FT.urun_z(float(x)))) for x in range(2337, 4301, 8)]
    d.line(pts, fill=(200, 120, 40), width=3)
    for xm in (2337.0, 2690.0, XC - ADIM, XC, XC + ADIM, 3890.0, 4300.0):
        zm = FT.urun_z(xm)
        d.ellipse([fx(xm - 140), pz(zm - 140), fx(xm + 140), pz(zm + 140)], outline=(180, 140, 70), width=2)
    # eksenler
    eksen((fx(2150), pz(ZT)), (fx(4400), pz(ZT)), ACC)
    txt(fx(2150) + 4, pz(ZT) + 14, "hat ürün ekseni z %s" % sayi(ZT), f7, ACC, "lm")
    eksen((fx(B0), pz(ZB_C)), (fx(B1), pz(ZB_C)), TURUNCU)
    txt(fx(B1) - 6, pz(ZB_C) - 12, "TP10 bant ekseni z %s" % sayi(ZB_C), f7, TURUNCU, "rm")
    txt(fx(G0) + 8, pz(-FT.D_TP + 40) , "fırında ürün merkezi z %s (ön kenar %s · tünel duvarına 20)" % (sayi(ZUF), sayi(ZUF + 150)), f7, (200, 120, 40), "lm")
    xr = fx(4400) + 30
    olcu_v(xr, pz(-FT.D_TP), pz(0), "%s (föy)" % sayi(FT.D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(-FT.D_TP), sayi(DZ - FT.D_TP), f7, INK, "r")
    olcu_v(fx(G1) - 40, pz(TUN_Z[0]), pz(0), "≈ %s + %s" % (sayi(-TUN_Z[1]), sayi(TUN_Z[1] - TUN_Z[0])), f7, INK, "l")


# ============================== YAN KESİT ==============================
def yan():
    txt(SX0, 172, "YAN KESİT (x %s · soldan bakış)" % sayi(XC), f16, ACC)
    d.rectangle([sx(-DZ), fy(H_MAK), sx(0), fy(0)], outline=LINE, width=3)
    d.rectangle([sx(-DZ + 30), fy(Y_ALT), sx(-30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([sx(-DZ), fy(YG0), sx(0), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    balon(sx(-400), fy(600), sx(-300), fy(700), 13)
    dline((sx(-DZ), fy(H_B)), (sx(0), fy(H_B)), RED, 2, 10, 5)
    d.rectangle([sx(-DZ + 3), fy(DAV[1]), sx(-3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    balon(sx(-400), fy(1850), sx(-300), fy(1930), 14)
    d.rectangle([sx(-DZ), fy(YG1 + 10), sx(-DZ + 1.5), fy(YG0)], fill=INK)
    balon(sx(-DZ), fy(1300), sx(-DZ) - 40, fy(1360), 12)
    d.rectangle([sx(HAVA_Z[0]), fy(1252), sx(HAVA_Z[1]), fy(646)], fill=(236, 240, 246), outline=GRAY, width=1)
    # gövde kesiti
    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(0), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(TUN_Z[1]), fy(YG1) + 2, sx(0) - 2, fy(YG0) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(YG1) + 2, sx(TUN_Z[1]), fy(TUN_Y[1]) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(TUN_Y[0]) + 2, sx(TUN_Z[1]), fy(YG0) - 2, (214, 216, 222), 9)
    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(TUN_Z[0] - 5.5), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((-FT.D_TP + TUN_Z[0]) / 2), fy((YG0 + YG1) / 2), sx((-FT.D_TP + TUN_Z[0]) / 2) - 40, fy(YG1) - 40, 4)
    d.rectangle([sx(-FT.D_TP) - 9, fy(YG0 + FT.EKRAN[2] + FT.EKRAN[1]), sx(-FT.D_TP), fy(YG0 + FT.EKRAN[2])], fill=INK)
    d.rectangle([sx(TUN_Z[0]), fy(TUN_Y[1]), sx(TUN_Z[1]), fy(TUN_Y[0])], fill=SICAK, outline=INK, width=1)
    for (ya, yb) in ((TUN_Y[1] - 10.0, TUN_Y[1] - 1.0), (YG0 + FT.RULO_Y - 12.0, YG0 + FT.RULO_Y - 4.0)):
        d.rectangle([sx(BZ[0]), fy(yb), sx(BZ[1]), fy(ya)], fill=(250, 190, 160), outline=TURUNCU, width=1)
    balon(sx(BZ[0] + 60), fy(TUN_Y[1] - 5), sx(BZ[0] + 100), fy(YG1) - 40, 2)
    d.rectangle([sx(BZ[0]), fy(BANT_F), sx(BZ[1]), fy(BANT_F - 6)], fill=INK)
    d.rectangle([sx(BZ[0]), fy(RY - 20), sx(BZ[1]), fy(RY - 26)], fill=GRAY)
    balon(sx(BZ[0] + 40), fy(BANT_F - 3), sx(BZ[0] + 80), fy(YG0) + 40, 3)
    d.rectangle([sx(ZUF - 140), fy(BANT_F + 12), sx(ZUF + 140), fy(BANT_F + 1)], fill=URUN, outline=(180, 140, 70), width=1)
    drect(sx(ZUF - 150), fy(BANT_F + 28), sx(ZUF + 150), fy(BANT_F + 1), (180, 140, 70), 1, 4, 3)
    # ölçüler
    olcu_h(sx(-FT.D_TP), sx(0), fy(H_MAK) - 30, "%s (föy)" % sayi(FT.D_TP), f8, INK)
    olcu_h(sx(-DZ), sx(-FT.D_TP), fy(H_MAK) - 30, sayi(DZ - FT.D_TP), f7, INK)
    olcu_h(sx(-DZ), sx(0), fy(H_MAK) - 70, "F %s" % sayi(DZ), f8, ACC)
    olcu_h(sx(-FT.D_TP), sx(TUN_Z[0] - 5.5), fy(YG0) + 90, "≈ 239", f7, INK)
    olcu_h(sx(TUN_Z[0]), sx(TUN_Z[1]), fy(YG0) + 90, "≈ %s" % sayi(TUN_Z[1] - TUN_Z[0]), f7, INK)
    olcu_h(sx(TUN_Z[1]), sx(0), fy(YG0) + 90, "≈ %s" % sayi(-TUN_Z[1]), f7, INK)
    olcu_h(sx(BZ[0]), sx(BZ[1]), fy(YG0) + 130, "bant %s" % sayi(FT.BANT_W), f7, INK)
    olcu_h(sx(ZUF - 150), sx(ZUF + 150), fy(BANT_F + 28) - 26, "ürün Ø300 z %s" % sayi(ZUF), f7, (180, 140, 70))
    xd = sx(0) + 110
    olcu_v(xd, fy(YG1), fy(YG0), "≈ %s" % sayi(FT.H_GOV), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F), fy(YG0), "≈ %s" % sayi(FT.BANT_Y), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F + FT.IC_H), fy(BANT_F), "%s (föy)" % sayi(FT.IC_H), f7, INK, "r")
    for yy in (Y_ALT, YG0, H_B, BANT_F, BANT_F + FT.IC_H, YG1, H_MAK):
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
        ("1", "TP10 gövdesi · paslanmaz · yalıtımlı · tünel ≈406 × 274", "≈ 960 × 730 × 517", "föy + çizim"),
        ("2", "Kızılötesi ısıtıcılar üst + alt · 2 bölge (şematik)", "400 °C · 9,5 kW", "föy"),
        ("3", "Uç kutusu × 2 (arkada, ekran tarafı) + konveyör", "≈ 295 × 237 × 167", "çizim"),
        ("4", "Dokunmatik ekran + teknik bölme (arkada)", "≈ 189 × 151 · ≈ 239", "çizim"),
        ("5", "Giriş bandı (bizim) · PTFE 320 · Ø20 burun", "70 · disk kenarına 2", "hesap"),
        ("6", "Giriş bandı motoru STP-MTR-23079 + GT2", "NEMA23 · 1:1", "katalog"),
        ("7", "Destek sacı × 2 (bizim) · 2 mm PTFE kaplı", "üstü 1166", "hesap"),
        ("8", "Giriş çiti 20° · POM 10 × 25 (bizim)", "−170 → −249", "hesap"),
        ("9", "Çıkış çiti 20° · POM 10 × 25 (bizim)", "−249 → −170", "hesap"),
        ("10", "Ayak 82–120 · SÖKÜLÜR", "—", "föy"),
        ("11", "Giriş/çıkış plakası · TAKILMAZ", "max 390", "föy"),
        ("12", "F arka sacı (bizim)", "956–1483", "hesap"),
        ("13", "F taban dolabı (bizim) · üst 956", "pizza yedeği 505", "hesap"),
        ("14", "Egzoz davlumbazı (bizim)", "1483–2028", "v47"),
    ]
    kol = (0, 46, 520, 780)
    gen = 960.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("NO", "PARÇA", "ÖLÇÜ", "KAYNAK")):
        txt(x0 + k + 8, y0 + 14, b, f7, INK, "lm")
    y = y0 + 28
    for r in satir:
        d.line([(x0, y + 28), (x0 + gen, y + 28)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            txt(x0 + k + 8, y + 14, v, f7, INK if k < 780 else GRAY, "lm")
        y += 28
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    y += 56
    ya = y
    txt(x0, y, "KOMŞU UYARLAMALARI", f16, ACC); txt(x0, y + 26, "yalnız bu sürümde", f7, GRAY, "lm"); y += 50
    for s_ in ("C · aktarma bandı (420) çıkar → giriş bandı",
               "C · X motoru kaidesi sağ üst köşe pahlanır",
               "K · bant yan levhaları 10 → 18'den",
               "K · itici motoru eksenin sağ ucuna",
               "K · sol sacta pencere −485'e + uç kutusu cebi",
               "F · taban dolabı 1060 → 956 · davlumbaz 1483"):
        txt(x0, y, s_, f7, INK, "lm"); y += 24
    x2, y = x0 + 500, ya
    txt(x2, y, "AÇIK / KARAR", f16, RED); y += 36
    for i, s_ in enumerate(("aynı anda ≈2,9 ürün · 3,5 dk'da 49,3/sa (2. saat)",
                            "istasyon tabanı 1060 kuralı F'de 956",
                            "pizza kutusu 4 gün → 3,8 gün (48 kutu)",
                            "gerilim · bant kotu · iç ölçüler üreticiden",
                            "tabladan banda itme (mevcut tasarımda da açık)"), 1):
        isaret(x2 + 15, y, i); txt(x2 + 40, y, s_, f7, INK, "lm"); y += 34
    y = max(y, ya + 36 + 6 * 24) + 20
    txt(x0, y, "≈ : föy çiziminden ölçekle · şematik : iç yerleşim föyde yok · v1 düzeltmesi: uç kutuları bandı SARMAZ, ekran tarafında yan kutu", f7, GRAY, "lm")


def baslik():
    txt(FX0, 40, "AUTOKITCH  ·  F FIRIN DENEMESİ (AYRI SÜRÜM)  ·  Sveba Dahlen TP10  ·  TEKNİK RESİM v2", f30, INK)
    txt(FX0, 98, "hatta uyarlanmış hali = 3B model firin_tp10_cad_v1 (tek kaynak) · x %s–%s · bant %s · ekran arkada · ana makine v47 değişmez · ölçüler mm · 26 Eylül 2026" % (sayi(X0), sayi(X1), sayi(BANT_F)), f11, GRAY)
    d.line([(FX0, 126), (W_PX - 60, 126)], fill=LINE, width=3)


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    baslik(); on(); ust(); yan(); liste()
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "FIRIN_TP10_v2_teknik.png")
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    print("yazildi:", yol, im.size)
    return yol


if __name__ == "__main__":
    ciz()
    os._exit(0)
