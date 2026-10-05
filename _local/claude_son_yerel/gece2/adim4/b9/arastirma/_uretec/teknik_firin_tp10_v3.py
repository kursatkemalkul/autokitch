# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN (AYRI SÜRÜM) · TP10 KESİTİ, GÖVDESİ 1500'E UZATILMIŞ · TEKNİK RESİM v3 (26 Eyl 2026)
v3: ölçüler 3B modelden (firin_tp10_cad_v2 · tek kaynak). Kemal: "gerçek fırının sadece önünü arkasını istediğimiz ölçüye uzat,
bant boş olmasın önünde arkada". Gövde 2500–4000, bant gövde dışına çıkmaz, ısıtılan 1316 (4 ürün), giriş ön odası + TOPPING cebi,
K bandında giriş çiti. (v2: katalog TP10 hatta; v1: uç kutuları yanlış çizilmişti.)
Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
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
PUC, EVC, KOMSU, ODA_R = (255, 240, 200), (220, 235, 255), (150, 150, 158), (246, 240, 232)


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
    d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=RED)
    txt(x, y, str(n), f8b, BG, "mm")


def balon(x0, y0, x1, y1, n):
    d.line([(x0, y0), (x1, y1)], fill=INK, width=1)
    d.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=INK)
    d.ellipse([x1 - 15, y1 - 15, x1 + 15, y1 + 15], fill=BG, outline=INK, width=2)
    txt(x1, y1, str(n), f8b, INK, "mm")


# ============================== VERİ (TEK KAYNAK: firin_tp10_cad_v2) ==============================
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firin_tp10_cad_v2 as FT

X_F0, X_F1, H_MAK, DZ, Y_ALT, H_B = FT.X_F0, FT.X_F1, 2030.0, 830.0, 123.0, 1060.0
BANT_F, PLAKA_K, P_SUREC, ZT = FT.BANT_UST_HAT, 1164.0, 1168.0, FT.ZT
TAB_XC, TAB_R = 700.0 + 1637.0, 170.0
K_KUY, K_KR, K_Z0, K_Z1 = 4037.0, 15.0, -412.0, -12.0
HAVA_Z = (-795.0, -735.0)
YG0, YG1 = FT.YG0, FT.YG1
XC = FT.XC_TP
D0, T0, T1, D1 = FT.X_DUV0, FT.X_TUN0, FT.X_TUN1, FT.X_F1
B0, B1 = FT.BANT_X
RX0, RX1, RY, RR = FT.RULO_X[0], FT.RULO_X[1], FT.RULO_Y, FT.SARIM_R
TUN_Y, TUN_Z, BZ = FT.TUN_Y, FT.TUNEL_Z, FT.BANT_Z
ZB_C = (BZ[0] + BZ[1]) / 2.0
GEC_Y = FT.GECIT_Y
DAV = (YG1 + 10.0, 2028.0)
ADIM, ZUF = FT.ADIM, FT.Z_URUN_FIRIN
N_ICERIDE = FT.N_URUN
CEP = FT.CEP_AGIZ
GBX0, GBX1 = FT.GB_XB - 11.5, FT.GB_XT + 11.5
OLU = FT.OLU_X

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


# ============================== ÖN GÖRÜNÜŞ ==============================
def on():
    txt(FX0, 172, "ÖN GÖRÜNÜŞ (hat önünden · kesik çizgi = gövde içi)", f16, ACC)
    for xx, ad in ((X_F0, "C | F"), (X_F1, "F | K")):
        dline((fx(xx), fy(H_MAK) - 10), (fx(xx), fy(0) + 10), ACC, 2, 12, 6)
        txt(fx(xx), fy(H_MAK) - 24, ad, f7, ACC, "mm")
    d.rectangle([fx(X_F0), fy(H_MAK), fx(X_F1), fy(0)], outline=LINE, width=3)
    d.rectangle([fx(X_F0 + 30), fy(Y_ALT), fx(X_F1 - 30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(X_F0), fy(YG0), fx(X_F1), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    txt(fx(XC), fy((Y_ALT + YG0) / 2), "içerik v47 ile aynı · üstü %s · pizza kutusu yedeği 505" % sayi(YG0), f7, GRAY, "mm")
    balon(fx(XC - 300), fy(600), fx(XC - 420), fy(700), 14)
    d.rectangle([fx(X_F0 + 3), fy(DAV[1]), fx(X_F1 - 3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    txt(fx(XC), fy((DAV[0] + DAV[1]) / 2), "fan + yağ/karbon filtre · komşu modüllere asılı", f7, GRAY, "mm")
    balon(fx(XC - 420), fy(1850), fx(XC - 540), fy(1930), 15)
    # gövde (ön yüz) · içi: ön oda · uç duvarları · oda · ısıtıcılar
    d.rectangle([fx(X_F0), fy(YG1), fx(X_F1), fy(YG0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(X_F0), fy(YG1) + 3, fx(D0), fy(YG0) - 3], fill=(240, 242, 245))
    for a, b in ((D0, T0), (T1, D1)):
        tarali(fx(a), fy(YG1) + 3, fx(b), fy(YG0) - 3, (206, 208, 214), 9)
        drect(fx(a), fy(YG1) + 3, fx(b), fy(YG0) - 3, GRAY, 1)
        d.rectangle([fx(a) + 1, fy(GEC_Y[1]), fx(b) - 1, fy(GEC_Y[0])], fill=(250, 250, 252))
    d.rectangle([fx(T0), fy(TUN_Y[1]), fx(T1), fy(TUN_Y[0])], fill=ODA_R)
    drect(fx(T0), fy(TUN_Y[1]), fx(T1), fy(TUN_Y[0]), GRAY, 1)
    for (ya, yb) in ((TUN_Y[1] - 10.0, TUN_Y[1] - 1.0), (RY - 12.0, RY - 4.0)):
        for (a, b) in ((T0 + 5, XC - 5), (XC + 5, T1 - 5)):
            drect(fx(a), fy(yb), fx(b), fy(ya), TURUNCU, 1, 5, 3)
    txt(fx(XC), fy(TUN_Y[1] - 30.0), "ısıtılan oda (gizli) · üst + alt IR, 2 bölge (şematik)", f7, TURUNCU, "mm")
    balon(fx(T0 + 200), fy(YG1 - 20), fx(T0 + 200) + 40, fy(YG1) - 46, 1)
    balon(fx(T1 - 120), fy(TUN_Y[1] - 5), fx(T1 - 40), fy(YG1) - 46, 2)
    balon(fx((D0 + T0) / 2), fy(1300), fx((D0 + T0) / 2) + 10, fy(YG1) - 46, 4)
    txt(fx((X_F0 + D0) / 2), fy(1450), "ön oda", f7, GRAY, "mm")
    balon(fx((X_F0 + D0) / 2), fy(1430), fx(X_F0) - 40, fy(1478), 5)
    # bant (gizli): üst kol · alt kol · rulolar · 4 ürün
    for xr in (RX0, RX1):
        d.ellipse([fx(xr - RR), fy(RY + RR), fx(xr + RR), fy(RY - RR)], fill=EVC, outline=INK, width=1)
    dline((fx(RX0), fy(BANT_F)), (fx(RX1), fy(BANT_F)), INK, 3, 10, 5)
    dline((fx(RX0), fy(FT.ALT_KOL_Y[0])), (fx(RX1), fy(FT.ALT_KOL_Y[0])), GRAY, 1, 10, 5)
    balon(fx(RX1), fy(RY - RR), fx(RX1) + 40, fy(YG0) + 46, 3)
    for i in range(N_ICERIDE):
        xm = XC + (i - (N_ICERIDE - 1) / 2.0) * ADIM
        drect(fx(xm - 150), fy(BANT_F + 12), fx(xm + 150), fy(BANT_F + 1), (180, 140, 70), 1, 5, 3)
    # ön oda: giriş bandı · motoru · TOPPING cebi
    d.rectangle([fx(GBX0), fy(BANT_F), fx(GBX1), fy(FT.GB_RY - 11.5)], fill=(214, 196, 170), outline=INK, width=1)
    for xr in (FT.GB_XB, FT.GB_XT):
        d.ellipse([fx(xr - 10), fy(FT.GB_RY + 10), fx(xr + 10), fy(FT.GB_RY - 10)], fill=BG, outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), fy(FT.GB_MOTOR[1] + 28.5), fx(FT.GB_MOTOR[0] + 28.5), fy(FT.GB_MOTOR[1] - 28.5), INK, 1, 4, 3)
    dline((fx(FT.GB_XT), fy(FT.GB_RY)), (fx(FT.GB_MOTOR[0]), fy(FT.GB_MOTOR[1])), GRAY, 1, 4, 3)
    balon(fx(FT.GB_MOTOR[0] - 28.5), fy(FT.GB_MOTOR[1]), fx(2462), fy(1300), 7)
    balon(fx((GBX0 + GBX1) / 2), fy(FT.GB_RY - 11.5), fx(GBX0) - 70, fy(FT.GB_RY - 80), 6)
    drect(fx(CEP[0]), fy(CEP[2]), fx(2586), fy(CEP[1]), RED, 1, 5, 3)
    isaret(fx(2586) + 40, fy(1075), 1)
    # komşular: TOPPING tabla + disk aktarmada · ürün diskte · X tahriki · tekne · K bandı · ölü plaka · K giriş çiti
    d.rectangle([fx(TAB_XC - TAB_R), fy(P_SUREC), fx(TAB_XC + TAB_R), fy(1157.0)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(TAB_XC - 140), fy(P_SUREC + 9), fx(TAB_XC + 140), fy(P_SUREC)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X_F0) - 16, fy(1400), "TOPPING tabla + diski aktarmada", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1400) + 20, "kenar x %s · disk üstü %s" % (sayi(TAB_XC + TAB_R), sayi(P_SUREC)), f7, KOMSU, "rm")
    drect(fx(2490), fy(1135), fx(2580), fy(1064.5), KOMSU, 1, 5, 3)
    drect(fx(2400), fy(1091.5), fx(2585), fy(1061.5), KOMSU, 1, 5, 3)
    txt(fx(X_F0) - 16, fy(1010), "TOPPING X tahriki + mekanizma teknesi", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1010) + 20, "F'ye 80–85 mm taşıyor (v47'de de)", f7, RED, "rm")
    d.ellipse([fx(K_KUY - K_KR), fy(PLAKA_K - 2.0), fx(K_KUY + K_KR), fy(PLAKA_K - 2.0 - 2 * K_KR)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(K_KUY), fy(PLAKA_K), fx(4380), fy(PLAKA_K - 4.0)], fill=KOMSU)
    txt(fx(4380), fy(PLAKA_K) - 18, "K bandı %s" % sayi(PLAKA_K), f7, KOMSU, "rm")
    d.rectangle([fx(OLU[0]), fy(PLAKA_K + 1.5), fx(OLU[1]), fy(PLAKA_K - 1.0)], fill=ACC)
    balon(fx((OLU[0] + OLU[1]) / 2), fy(PLAKA_K + 1.5), fx(OLU[1]) + 40, fy(1300), 8)
    d.rectangle([fx(FT.CC_A[0]), fy(FT.CIT_Y[1]), fx(FT.CC_B[0]), fy(FT.CIT_Y[0])], fill=(245, 245, 240), outline=ACC, width=2)
    balon(fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(FT.CIT_Y[1]), fx((FT.CC_A[0] + FT.CC_B[0]) / 2), fy(1380), 9)
    # ölçüler
    olcu_h(fx(T0), fx(T1), fy(YG1) - 100, "ısıtılan %s · aynı anda %d ürün (adım %s)" % (sayi(FT.ODA), N_ICERIDE, sayi(ADIM)), f8, TURUNCU)
    olcu_h(fx(X_F0), fx(D0), fy(YG1) - 140, sayi(FT.ON_ODA), f7, INK)
    olcu_h(fx(D0), fx(T0), fy(YG1) - 140, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(T1), fx(D1), fy(YG1) - 140, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(X_F0), fx(X_F1), fy(YG1) - 180, "gövde %s (TP10 kesiti · boy ÖZEL)" % sayi(FT.L_GOV), f9, INK)
    olcu_h(fx(B0), fx(B1), fy(YG0) + 70, "bant %s × %s uçtan uca · %s – %s · gövde dışına çıkmaz" % (sayi(FT.BANT_W), sayi(B1 - B0), sayi(B0), sayi(B1)), f8, INK)
    for xx in (X_F0, X_F1, D0, T0, T1):
        dline((fx(xx), fy(YG1) - 186), (fx(xx), fy(YG1) - 2), GRAY, 1, 4, 4)
    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "F modülü %s" % sayi(X_F1 - X_F0), f9, ACC)
    olcu_h(fx(TAB_XC + TAB_R), fx(B0), fy(1225), "disk → fırın bandı %s (giriş bandı)" % sayi(B0 - TAB_XC - TAB_R), f7, INK)
    dline((fx(X_F0), fy(H_B)), (fx(X_F1), fy(H_B)), RED, 2, 10, 5)
    txt(fx(T0) + 10, fy(H_B) + 16, "istasyon tabanı kuralı %s (gövde altı %s)" % (sayi(H_B), sayi(YG0)), f7, RED, "lm")
    isaret(fx(T0) + 30 + d.textlength("istasyon tabanı kuralı 1060 (gövde altı 956)", font=f7), fy(H_B) + 16, 2)
    for yy in (0.0, Y_ALT, YG0, H_B, BANT_F, BANT_F + FT.IC_H, YG1, H_MAK):
        c = RED if yy == H_B else INK
        d.line([(fx(4400) - 20, fy(yy)), (fx(4400) - 4, fy(yy))], fill=c, width=2)
        txt(fx(4400), fy(yy), sayi(yy), f7, c, "lm")


# ============================== ÜST GÖRÜNÜŞ ==============================
def ust():
    txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ (ürün yolu: merkez çizgisi · diskte kayma · K bandında çit)", f16, ACC)
    d.rectangle([fx(X_F0), pz(-DZ), fx(X_F1), pz(0)], outline=LINE, width=3)
    txt(fx(X_F0) + 8, pz(0) + 18, "hat ön yüzü (z 0)", f7, GRAY, "lm")
    d.rectangle([fx(2400), pz(HAVA_Z[0]), fx(4300), pz(HAVA_Z[1])], fill=(236, 240, 246), outline=GRAY, width=1)
    txt(fx(2400) + 6, pz(sum(HAVA_Z) / 2), "hava ana hattı (mevcut)", f7, GRAY, "lm")
    # K bandı + K giriş çiti + ölü plaka
    d.rectangle([fx(K_KUY - K_KR - 2), pz(K_Z0), fx(4380), pz(K_Z1)], fill=(240, 240, 243), outline=KOMSU, width=2)
    d.rectangle([fx(4010), pz(K_Z0 - 5), fx(4380), pz(K_Z0 - 2)], fill=KOMSU)
    txt(fx(4380) - 6, pz(K_Z1) + 14, "K bandı 400 · parçaları değişmez", f7, KOMSU, "rm")
    d.rectangle([fx(OLU[0]), pz(FT.GB_Z[0]), fx(OLU[1]), pz(FT.GB_Z[1])], fill=(230, 238, 250), outline=ACC, width=1)
    nx_, nz_ = math.sin(math.radians(20.0)), math.cos(math.radians(20.0))
    pts = [FT.CC_A, FT.CC_B, (FT.CC_B[0] + 10 * nx_, FT.CC_B[1] - 10 * nz_), (FT.CC_A[0] + 10 * nx_, FT.CC_A[1] - 10 * nz_)]
    d.polygon([(fx(p[0]), pz(p[1])) for p in pts], fill=(255, 250, 235), outline=ACC)
    for xb in (4090.0, 4200.0):
        zl = FT.CC_A[1] + (xb - 8.0 - FT.CC_A[0]) * FT.TAN20 - 10.0 / nz_
        d.rectangle([fx(xb - 8), pz(K_Z0 - 8), fx(xb + 8), pz(zl)], fill=FILL, outline=INK, width=1)
    balon(fx(4150), pz(-380), fx(4150), pz(-DZ) - 40, 9)
    # gövde · ön oda · uç duvarları · oda · teknik bölme · ekran · fanlar
    d.rectangle([fx(X_F0), pz(-FT.D_TP), fx(X_F1), pz(0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(D0), pz(-FT.D_TP), fx(X_F1), pz(TUN_Z[0] - 5.5)], fill=(222, 226, 232), outline=INK, width=1)
    d.rectangle([fx(X_F0) + 2, pz(-FT.D_TP) + 2, fx(D0), pz(0) - 2], fill=(240, 242, 245))
    for a, b in ((D0, T0), (T1, D1)):
        tarali(fx(a), pz(TUN_Z[0]), fx(b), pz(TUN_Z[1]), (206, 208, 214), 9)
        drect(fx(a), pz(TUN_Z[0]), fx(b), pz(TUN_Z[1]), GRAY, 1)
    d.rectangle([fx(T0), pz(TUN_Z[0]), fx(T1), pz(TUN_Z[1])], fill=ODA_R)
    drect(fx(T0), pz(TUN_Z[0]), fx(T1), pz(TUN_Z[1]), GRAY, 1)
    d.rectangle([fx(XC - FT.EKRAN[0] / 2), pz(-FT.D_TP) - 2, fx(XC + FT.EKRAN[0] / 2), pz(-FT.D_TP) + 7], fill=INK)
    balon(fx(XC + 60), pz(-FT.D_TP) + 4, fx(XC + 200), pz(-FT.D_TP) + 60, 12)
    for fx_ in (D0 + 76.0, X_F1 - 140.0):
        d.ellipse([fx(fx_ - FT.FAN_R), pz(-FT.D_TP) - 2, fx(fx_ + FT.FAN_R), pz(-FT.D_TP) + 2], outline=INK, width=1)
    # tahrik + gergi (teknik bölmede, gizli)
    drect(fx(RX1 - 32), pz(-586), fx(RX1 + 26), pz(-521), INK, 1, 4, 3)
    drect(fx(RX1 - 170), pz(-583), fx(RX1 - 32), pz(-523), INK, 1, 4, 3)
    balon(fx(RX1 - 100), pz(-553), fx(RX1 - 140), pz(-660), 10)
    drect(fx(2556), pz(-520), fx(RX0 - 18), pz(-500), INK, 1, 4, 3)
    balon(fx(2575), pz(-510), fx(2650), pz(-660), 11)
    # bant (gizli) + giriş bandı + TOPPING cebi
    d.rectangle([fx(B0), pz(BZ[0]), fx(B1), pz(BZ[1])], fill=EVC)
    drect(fx(B0), pz(BZ[0]), fx(B1), pz(BZ[1]), INK, 1, 6, 4)
    for i in range(0, int(B1 - B0), 40):
        d.line([(fx(B0 + i), pz(BZ[0]) + 1), (fx(B0 + i), pz(BZ[1]) - 1)], fill=(190, 205, 225), width=1)
    d.rectangle([fx(GBX0), pz(FT.GB_Z[0]), fx(GBX1), pz(FT.GB_Z[1])], fill=(214, 196, 170), outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), pz(FT.GB_MOTOR[2] - 76), fx(FT.GB_MOTOR[0] + 28.5), pz(FT.GB_MOTOR[2]), INK, 1, 5, 3)
    drect(fx(CEP[0]), pz(CEP[3]), fx(2586), pz(CEP[4]), RED, 1, 5, 3)
    isaret(fx(2586) + 22, pz(-30), 1)
    # TOPPING: disk aktarmada + X tahriki + tekne (gizli)
    d.ellipse([fx(TAB_XC - TAB_R), pz(ZT - TAB_R), fx(TAB_XC + TAB_R), pz(ZT + TAB_R)], outline=KOMSU, width=2)
    drect(fx(2490), pz(-397.5), fx(2580), pz(-389.5), KOMSU, 1, 4, 3)
    drect(fx(2507), pz(-462), fx(2563), pz(-397.5), KOMSU, 1, 4, 3)
    drect(fx(2400), pz(-415), fx(2585), pz(-5), KOMSU, 1, 4, 3)
    d.rectangle([fx(2492), pz(-417), fx(2498.5), pz(-13)], fill=BG, outline=KOMSU, width=1)
    txt(fx(2492) - 6, pz(-430), "TOPPING çıkış yarığı çerçevesi v2 · −417…−13", f7, KOMSU, "rm")
    # ürün yolu: diskte kayma · fırın · K çiti
    d.line([(fx(TAB_XC), pz(ZT)), (fx(TAB_XC), pz(ZUF))], fill=(200, 120, 40), width=3)
    pts = [(fx(x), pz(FT.urun_z(float(x)))) for x in range(int(TAB_XC), 4301, 8)]
    d.line(pts, fill=(200, 120, 40), width=3)
    for xm, zm in ((TAB_XC, ZT), (TAB_XC, ZUF), (XC - 1.5 * ADIM, ZUF), (XC - 0.5 * ADIM, ZUF), (XC + 0.5 * ADIM, ZUF), (XC + 1.5 * ADIM, ZUF), (4300.0, ZT)):
        d.ellipse([fx(xm - 140), pz(zm - 140), fx(xm + 140), pz(zm + 140)], outline=(180, 140, 70), width=2)
    txt(fx(TAB_XC) - 60, pz(ZT - TAB_R - 36), "diskte 79 mm arkaya (itici · AÇIK)", f7, (200, 120, 40), "mm")
    isaret(fx(TAB_XC) - 60 + d.textlength("diskte 79 mm arkaya (itici · AÇIK)", font=f7) / 2 + 24, pz(ZT - TAB_R - 36), 4)
    # eksenler
    eksen((fx(2150), pz(ZT)), (fx(4400), pz(ZT)), ACC)
    txt(fx(2150) + 4, pz(ZT) + 14, "hat ürün ekseni z %s" % sayi(ZT), f7, ACC, "lm")
    eksen((fx(B0), pz(ZB_C)), (fx(B1), pz(ZB_C)), TURUNCU)
    txt(fx(B1) - 6, pz(ZB_C) - 12, "bant ekseni z %s" % sayi(ZB_C), f7, TURUNCU, "rm")
    txt(fx(T0) + 8, pz(-FT.D_TP + 40), "fırında ürün merkezi z %s (ön kenar %s · tünel duvarına 20)" % (sayi(ZUF), sayi(ZUF + 150)), f7, (200, 120, 40), "lm")
    xr = fx(4400) + 30
    olcu_v(xr, pz(-FT.D_TP), pz(0), "%s (föy)" % sayi(FT.D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(-FT.D_TP), sayi(DZ - FT.D_TP), f7, INK, "r")
    olcu_v(fx(T1) - 40, pz(TUN_Z[0]), pz(0), "%s + %s" % (sayi(-TUN_Z[1]), sayi(TUN_Z[1] - TUN_Z[0])), f7, INK, "l")
    olcu_h(fx(X_F0), fx(D0), pz(0) + 40, sayi(FT.ON_ODA), f7, INK)
    olcu_h(fx(D0), fx(T0), pz(0) + 40, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(T0), fx(T1), pz(0) + 40, "ısıtılan %s" % sayi(FT.ODA), f7, TURUNCU)
    olcu_h(fx(T1), fx(D1), pz(0) + 40, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(FT.CC_A[0]), fx(FT.CC_B[0]), pz(-DZ) - 80, "K giriş çiti %s (20°) · %s → %s" % (sayi(FT.CC_B[0] - FT.CC_A[0]), sayi(ZUF), sayi(ZT)), f7, ACC)


# ============================== YAN KESİT ==============================
def yan():
    txt(SX0, 172, "YAN KESİT (x %s · soldan bakış · kesit TP10 föyüyle aynı)" % sayi(XC), f16, ACC)
    d.rectangle([sx(-DZ), fy(H_MAK), sx(0), fy(0)], outline=LINE, width=3)
    d.rectangle([sx(-DZ + 30), fy(Y_ALT), sx(-30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([sx(-DZ), fy(YG0), sx(0), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    balon(sx(-400), fy(600), sx(-300), fy(700), 14)
    dline((sx(-DZ), fy(H_B)), (sx(0), fy(H_B)), RED, 2, 10, 5)
    d.rectangle([sx(-DZ + 3), fy(DAV[1]), sx(-3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    balon(sx(-400), fy(1850), sx(-300), fy(1930), 15)
    d.rectangle([sx(-DZ), fy(YG1 + 10), sx(-DZ + 1.5), fy(YG0)], fill=INK)
    balon(sx(-DZ), fy(1300), sx(-DZ) - 40, fy(1360), 13)
    d.rectangle([sx(HAVA_Z[0]), fy(1252), sx(HAVA_Z[1]), fy(646)], fill=(236, 240, 246), outline=GRAY, width=1)
    # gövde kesiti
    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(0), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(TUN_Z[1]), fy(YG1) + 2, sx(0) - 2, fy(YG0) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(YG1) + 2, sx(TUN_Z[1]), fy(TUN_Y[1]) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(TUN_Y[0]) + 2, sx(TUN_Z[1]), fy(YG0) - 2, (214, 216, 222), 9)
    d.rectangle([sx(-FT.D_TP), fy(YG1), sx(TUN_Z[0] - 5.5), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((-FT.D_TP + TUN_Z[0]) / 2), fy((YG0 + YG1) / 2), sx((-FT.D_TP + TUN_Z[0]) / 2) - 40, fy(YG1) - 40, 12)
    d.rectangle([sx(-FT.D_TP) - 9, fy(YG0 + FT.EKRAN[2] + FT.EKRAN[1]), sx(-FT.D_TP), fy(YG0 + FT.EKRAN[2])], fill=INK)
    d.rectangle([sx(TUN_Z[0]), fy(TUN_Y[1]), sx(TUN_Z[1]), fy(TUN_Y[0])], fill=SICAK, outline=INK, width=1)
    for (ya, yb) in ((TUN_Y[1] - 10.0, TUN_Y[1] - 1.0), (RY - 12.0, RY - 4.0)):
        d.rectangle([sx(BZ[0]), fy(yb), sx(BZ[1]), fy(ya)], fill=(250, 190, 160), outline=TURUNCU, width=1)
    balon(sx(BZ[0] + 60), fy(TUN_Y[1] - 5), sx(BZ[0] + 100), fy(YG1) - 40, 2)
    d.rectangle([sx(BZ[0]), fy(BANT_F), sx(BZ[1]), fy(BANT_F - 6)], fill=INK)
    d.rectangle([sx(BZ[0]), fy(FT.ALT_KOL_Y[1]), sx(BZ[1]), fy(FT.ALT_KOL_Y[0])], fill=GRAY)
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
    olcu_v(xd, fy(YG1), fy(YG0), "%s" % sayi(FT.H_GOV), f7, INK, "r")
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
        ("1", "Fırın gövdesi · TP10 kesiti · paslanmaz · yalıtımlı · boy ÖZEL", "1500 × 730 × 517", "föy kesiti + özel"),
        ("2", "Kızılötesi ısıtıcılar üst + alt · 2 bölge (şematik)", "400 °C · ≈14 kW", "föy ölçekli · VARSAYIM"),
        ("3", "Konveyör · tel örgü bant · rulolar uç duvarı içinde", "381 × 1428 · üst 1166", "VARSAYIM"),
        ("4", "Uç duvarı × 2 · yalıtım · geçit 1108–1251", "60", "hesap"),
        ("5", "Giriş ön odası · ısıtılmaz · TOPPING cebi", "64", "hesap"),
        ("6", "Giriş bandı (bizim) · PTFE 320 · Ø20 burun + tahrik", "%s–%s" % (sayi(GBX0), sayi(GBX1)), "hesap"),
        ("7", "Giriş bandı motoru STP-MTR-23079 + GT2", "NEMA23 · 1:1", "katalog"),
        ("8", "Çıkış ölü plakası (bizim) · 2,5 mm L", "%s–%s" % (sayi(OLU[0]), sayi(OLU[1])), "hesap"),
        ("9", "K giriş çiti 20° (bizim · K bandında) + 2 braket", "−249 → −170 · 231", "hesap"),
        ("10", "Bant tahriki · redüktör + motor (teknik bölmede)", "≈2,6 dev/dk", "VARSAYIM"),
        ("11", "Bant gergisi · M8 (teknik bölmede)", "—", "VARSAYIM"),
        ("12", "Dokunmatik ekran + teknik bölme (arkada)", "≈ 189 × 151 · ≈ 239", "föy"),
        ("13", "F arka sacı (bizim)", "956–1483", "hesap"),
        ("14", "F taban dolabı (bizim) · üst 956", "pizza yedeği 505", "hesap"),
        ("15", "Egzoz davlumbazı (bizim)", "1483–2028", "v47"),
    ]
    kol = (0, 46, 560, 800)
    gen = 960.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("NO", "PARÇA", "ÖLÇÜ", "KAYNAK")):
        txt(x0 + k + 8, y0 + 14, b, f7, INK, "lm")
    y = y0 + 28
    for r in satir:
        d.line([(x0, y + 28), (x0 + gen, y + 28)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            txt(x0 + k + 8, y + 14, v, f7, INK if k < 800 else GRAY, "lm")
        y += 28
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    y += 56
    ya = y
    txt(x0, y, "KOMŞU UYARLAMALARI", f16, ACC); txt(x0, y + 40, "yalnız bu sürümde", f7, GRAY, "lm"); y += 60
    for s_ in ("C · aktarma bandı (420) çıkar → giriş bandı F'nin ön odasında",
               "C · X motoru kaidesi sağ üst köşe pahlanır (1112)",
               "C · çıkış yarığı çerçevesi −417…−13 · alt çıta 1145–1155",
               "C · ürün diskte 79 mm arkaya kaydırılır (itici · AÇIK)",
               "K · parça değişmez · K bandında giriş çiti + ölü plaka",
               "F · taban dolabı 1060 → 956 · davlumbaz 1483"):
        txt(x0, y, s_, f7, INK, "lm"); y += 24
    x2, y = x0 + 500, ya
    txt(x2, y, "AÇIK / KARAR", f16, RED); y += 36
    for i, s_ in enumerate(("TOPPING teknesi + X tahriki F'ye 85 mm taşıyor → cep (ya da TOPPING kısaltılır)",
                            "istasyon tabanı 1060 kuralı F'de 956",
                            "pizza kutusu 4 gün → 3,8 gün (48 kutu)",
                            "tabladan itme + 79 mm arkaya kayma (itici tasarımı)",
                            "boy uzatma özel sipariş (Sveba / yerli IR) · güç ≈14 kW VARSAYIM"), 1):
        isaret(x2 + 15, y, i); txt(x2 + 40, y, s_, f7, INK, "lm"); y += 34
    y = max(y, ya + 36 + 6 * 24) + 20
    txt(x0, y, "kesit ölçüleri föy + çizimden (≈) · boy, oda, ön oda, duvarlar hesap · tam yükte 51,7 ürün/sa = bugünkü model (sim, 2. saat)", f7, GRAY, "lm")


def baslik():
    txt(FX0, 40, "AUTOKITCH  ·  F FIRIN (AYRI SÜRÜM)  ·  TP10 KESİTİ · GÖVDE 1500'E UZATILMIŞ  ·  TEKNİK RESİM v3", f30, INK)
    txt(FX0, 98, "3B model firin_tp10_cad_v2 (tek kaynak) · gövde %s–%s · bant gövde dışına çıkmaz · ısıtılan %s · aynı anda %d ürün · ana makine v47 değişmez · ölçüler mm · 26 Eylül 2026"
        % (sayi(X_F0), sayi(X_F1), sayi(FT.ODA), N_ICERIDE), f11, GRAY)
    d.line([(FX0, 126), (W_PX - 60, 126)], fill=LINE, width=3)


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    baslik(); on(); ust(); yan(); liste()
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "FIRIN_TP10_v3_teknik.png")
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    print("yazildi:", yol, im.size)
    return yol


if __name__ == "__main__":
    ciz()
    os._exit(0)
