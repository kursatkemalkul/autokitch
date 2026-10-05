# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · TEKNİK RESİM v6 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4) — model firin_tp10_cad_v7.
Bütün y kotları v5'ten −168: gövde 788–1305 · bant 998 · raf 1305–1348 (üstü 1348) · ışınım kalkanı 1315 · disk 1000 → giriş bandı → fırın bandı 998 →
çıkış plakası 997,5 → K bandı 996 · fırın üstünde pizza kutusu yedeği 320 (1348–1860) + kompresör (1348–1858) · davlumbaz arka yarı 1315–1862 ·
fırın altı: F taban dolabı YOK → çekmeceli dolap (store_cad_v6) üstü 788, içinde PU 60 ısı kalkanı + taşıyıcı çerçeve.
Sayılar modüllerden: firin_tp10_cad_v7 · store_cad_v6 · kesme_cad_v4 · kaide_cad_v1 · itici_cad_v4 · kutu_cad_v5 (sabitler; parça kurulmaz).
Hava ana hattı (v46 ölçüsü z −795…−735) çizimden çıktı: alçak hatta yolu montaj v57'de, dolabın içinden geçemez.
Önceki: teknik_firin_tp10_v5.py (v5: kutu yedeği tek yerde fırın üstü sol 320, raf 4 mm + 10 takoz · v4: FIRIN 79 mm ÖNE — çıkıntı 0…+79, ürün −170 düz).
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
    def textbbox(self, xy, s, font=None, anchor="la"):
        b = self.d.textbbox(_ol(xy), s, font=self._f(font), anchor=anchor)
        return tuple(v / K_HD for v in b)


KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX, S = 3370, 2930, 0.8
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
PASL, SICAK, TURUNCU, URUN = (232, 234, 238), (255, 226, 214), (200, 90, 30), (240, 214, 170)
PUC, EVC, KOMSU, ODA_R = (255, 240, 200), (220, 235, 255), (150, 150, 158), (246, 240, 232)
KARTON, KARTON_C, ONYUZ = (236, 218, 184), (180, 140, 70), (250, 250, 251)


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
KAYIT = []                                                                                  # v6: yazı + balon kutuları → örtüşme denetimi


def txt(x, y, s, f=None, c=INK, a="la"):
    f = f or f11
    d.text((x, y), s, font=f, fill=c, anchor=a)
    KAYIT.append(d.textbbox((x, y), s, font=f, anchor=a) + (s,))


def sayi(v):
    return ("%g" % round(v, 1)).replace(".", ",").replace("-", "−")


def olcu_h(x0, x1, y, s, f=None, c=INK):
    f = f or f9
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 5, y - 12, (x0 + x1) / 2 + tw / 2 + 5, y + 12], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def etiket(x, y, s, f=None, c=INK, a="la"):
    """v6: çizgilerin üstüne düşen yazı — arkasına beyaz kutu"""
    f = f or f11
    b = d.textbbox((x, y), s, font=f, anchor=a)
    d.rectangle([b[0] - 4, b[1] - 3, b[2] + 4, b[3] + 3], fill=BG)
    txt(x, y, s, f, c, a)


def olcu_v(x, y0, y1, s, f=None, c=INK, yon="r", bg=False):
    f = f or f9
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    (etiket if bg else txt)(x + (10 if yon == "r" else -10), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


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
    KAYIT.append((x - 15, y - 15, x + 15, y + 15, "<isaret %d>" % n))
    d.text((x, y), str(n), font=f8b, fill=BG, anchor="mm")


def balon(x0, y0, x1, y1, n):
    d.line([(x0, y0), (x1, y1)], fill=INK, width=1)
    d.ellipse([x0 - 3, y0 - 3, x0 + 3, y0 + 3], fill=INK)
    d.ellipse([x1 - 15, y1 - 15, x1 + 15, y1 + 15], fill=BG, outline=INK, width=2)
    KAYIT.append((x1 - 15, y1 - 15, x1 + 15, y1 + 15, "<balon %d>" % n))
    d.text((x1, y1), str(n), font=f8b, fill=INK, anchor="mm")


# ============================== VERİ (TEK KAYNAK: 3B modüllerin sabitleri) ==============================
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firin_tp10_cad_v7 as FT                                                           # fırın (alçak hat)
import store_cad_v6 as SC                                                                # çekmeceli dolap 0–4000 × 123–788
import kesme_cad_v4 as KS                                                                # K: bant 996 · makine üstü 1862
import kaide_cad_v1 as KD                                                                # A/C kaidesi 788–892
import itici_cad_v4 as IT                                                                # disk 1000
import kutu_cad_v5 as KT                                                                 # pizza kutusu kalınlığı 1,6 · şarjör 462
import ray_ek_cad_v1 as RE                                                               # robot rayı z 240–480 (ekseni 360 DEĞİŞMEZ)

X_F0, X_F1, H_MAK, DZ, Y_ALT = FT.X_F0, FT.X_F1, KS.H, SC.DZ, SC.Y_PLINT                    # 2500 · 4000 · 1862 · 830 · 123
Y_DUZ = KD.Y_DUZ                                                                         # 788 düz çizgi = dolap üstü = fırın altı
BANT_F, PLAKA_K, P_SUREC, ZT = FT.BANT_UST_HAT, KS.BANT, IT.DISK_UST, FT.ZT              # 998 · 996 · 1000 · −170
assert Y_DUZ == FT.YG0 == SC.H_B == 788.0 and H_MAK == 1862.0
assert FT.K_BANT == KS.BANT == 996.0 and KS.FIRIN_BANDI == BANT_F == 998.0 and FT.DISK_UST == P_SUREC == KD.Y_MEK + 108.0 == 1000.0
assert RE.RZ == 360.0 and RE.RAY_Z[0] == 240.0                                            # SPEC v57: ray ekseni z 360 KALIR
TAB_R = 170.0; TAB_XC = FT.X_DISK_KENAR - TAB_R                                          # 2337 · TOPPING tabla aktarma konumu (700 + 1637)
TABLA_Y = (P_SUREC - 11.0, P_SUREC)                                                      # 989–1000: tabla 989–992 + disk 992–1000 (FT YARIK_V2 notu)
TEKNE_Y = (KD.Y_MEK + 1.5, KD.Y_MEK + 31.5)                                              # 893,5–923,5 TOPPING v24 mekanizma teknesi (v5: 1060 + 1,5…31,5)
K_KUY, K_KR, K_KY = KS.X_K_HAT + KS.X_KUYRUK, KS.R_KUYRUK, KS.Y_KUYRUK                   # 4037 · 15 · 979 K kuyruk rulosu
K_Z0, K_Z1 = KS.BANT_Z
YG0, YG1 = FT.YG0, FT.YG1
XC = FT.XC_TP
D0, T0, T1, D1 = FT.X_DUV0, FT.X_TUN0, FT.X_TUN1, FT.X_F1
B0, B1 = FT.BANT_X
RX0, RX1, RY, RR = FT.RULO_X[0], FT.RULO_X[1], FT.RULO_Y, FT.SARIM_R
TUN_Y, TUN_Z, BZ = FT.TUN_Y, FT.TUNEL_Z_D, FT.BANT_Z_D                                   # DÜNYA (79 öne kaymış)
ZB_C = (BZ[0] + BZ[1]) / 2.0
GEC_Y = FT.GECIT_Y
ADIM, ZUF = FT.ADIM, FT.Z_URUN_FIRIN_D
N_ICERIDE = FT.N_URUN
ZS = FT.ZS; DTP0, DTP1 = ZS, -FT.D_TP + ZS                                                 # gövde ön yüzü +79 · arka yüzü −651
GBZ = (FT.GB_Z[0] + ZS, FT.GB_Z[1] + ZS); GBMZ = FT.GB_MOTOR[2] + ZS
GBX0, GBX1 = FT.GB_XB - 11.5, FT.GB_XT + 11.5
OLU = FT.OLU_X
# ---- fırın üstü: raf + kalkan + takozlar (FT) · kutu yedeği + kompresör + davlumbaz (SPEC v57 = montaj v56 birimleri −168) ----
RAF_X, RAF_Z = (X_F0 + 10.0, X_F1 - 10.0), (-420.0, -15.0)                               # firin_tp10_cad_v7 ust_raf / isi_kalkani (1480 × 405)
TAKOZ_X = sorted({x for x, z in FT.TAKOZ_XZ}); TAKOZ_Z = sorted({z for x, z in FT.TAKOZ_XZ})
KUTU_N = 320
KUTU_X, KUTU_Y, KUTU_Z = (X_F0 + 20.0, X_F0 + 824.0), (FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + KUTU_N * KT.T), (-424.0, -20.0)   # 2520–3324 × 1348–1860
KOMP_X, KOMP_Y, KOMP_Z = (3600.0, 3980.0), (FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + 510.0), (-420.0, -40.0)                     # JUN-AIR OF302-15B zarfı
DAV, DAV_Z = (FT.ISI_KALKANI_Y[0], H_MAK), (-DZ, -425.0)                                  # montaj D_DAVLUMBAZ (FT.YG1 + 10 … H_MAK) · arka yarı
assert KUTU_Y[1] == 1860.0 and KOMP_Y[1] == 1858.0 and DAV[0] == 1315.0 and FT.UST_RAF_Y[1] == 1348.0
# ---- fırın altı: çekmeceli dolap (store_cad_v6) ----
PU_X, PU_Y = SC.X_F, (SC.Y_TAVAN, SC.H_B)                                                 # 2517–3793 × 728–788 ısı kalkanı PU 60
TAVAN_F = SC.Y_TAVAN_F                                                                   # 668 K5/K6 iç tavanı
ZP = (-DZ + 1.5, -41.5)                                                                  # store_cad_v6 kasa(): PU derinliği ZP0 … ZP1
TASIYICI = SC.TASIYICI


def _onler(kolonlar):
    """çekmece önleri (x0, x1, y0, y1, kod) — store_cad_v6 cekmece(): tam kaplama"""
    out = []
    for kol, kod, tip, x0, yo in SC.CEK:
        if kol not in kolonlar:
            continue
        pa, pb = SC.KAPAK_X[kol]
        pc = SC.ON_ALT if kod in SC.ALT_KOD else yo - SC.BIND
        pd = SC.ON_UST if kod in SC.UST_KOD else yo + SC.HH[tip] + SC.BIND
        out.append((pa, pb, pc, pd, kod))
    return out


K56_ON = _onler(("K5", "K6"))
K6_ON = _onler(("K6",))
_K4_S0 = SC.Y_PLINT + 1.5 + 4.0 + 272.0 + 8.0                                             # 408,5 · store_cad_v6 kasa(): s0 = cy0 + CU[1] + 8
K4_ON = [(X_F0, SC.KAPAK_X["K4"][1], SC.ON_ALT, _K4_S0 + 12.0, "k4_sogutma"), (X_F0, SC.KAPAK_X["K4"][1], _K4_S0 + 15.0, SC.ON_UST, "k4_depo")]
SK = SC.KAPAK_X["SERIT"]
SERIT_ON = [(SK[0], SK[1], SC.SERIT_KAPI[0], SC.SERIT_KAPI[1], "serit_kapak"), (SK[0], SK[1], SC.SERIT_PANEL[0], SC.SERIT_PANEL[1], "serit_panel")]
KL = SC.KLAPE_AC; KL_Y = SC.KLAPE_EKSEN[0]

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
    txt(FX0, 172, "ÖN GÖRÜNÜŞ (hat önünden · kesik çizgi = gizli)", f16, ACC)
    for xx, ad, dx, an in ((X_F0, "C | F", -4, "rm"), (X_F1, "F | K", 4, "lm")):
        dline((fx(xx), fy(H_MAK) - 10), (fx(xx), fy(0) + 10), ACC, 2, 12, 6)
        txt(fx(xx) + dx, fy(H_MAK) - 24, ad, f7, ACC, an)
    d.rectangle([fx(X_F0), fy(H_MAK), fx(X_F1), fy(0)], outline=LINE, width=3)
    # ---- çekmeceli dolap (store_cad_v6): plint · gövde · önler (K4 kenarı, K5, K6, şerit) · klape ----
    d.rectangle([fx(X_F0 + 30), fy(Y_ALT), fx(X_F1 - 30), fy(0)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(X_F0), fy(Y_DUZ), fx(X_F1), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    for a, b, y0, y1, _k in K4_ON + K56_ON + SERIT_ON:
        d.rectangle([fx(a), fy(y1), fx(b), fy(y0)], fill=ONYUZ, outline=LINE, width=1)
    d.rectangle([fx(KL[0]), fy(KL[3]), fx(KL[1]), fy(KL[2])], fill=SOFT, outline=INK, width=1)
    dline((fx(KL[0] - 6.0), fy(KL_Y)), (fx(KL[1] + 6.0), fy(KL_Y)), GRAY, 1, 4, 3)
    for xa, xb, s_ in ((SC.KAPAK_X["K5"][0], SC.KAPAK_X["K5"][1], "K5 · 3 pide + tatlı"), (SC.KAPAK_X["K6"][0], SC.KAPAK_X["K6"][1], "K6 · 3 içecek"),
                       (SK[0], SK[1], "şerit · robot çöpü")):
        txt(fx((xa + xb) / 2.0), fy(200.0), s_, f7, GRAY, "mm")                                   # denetçi: plintten en alt öne
    # ---- gizli: ısı kalkanı PU 60 · taşıyıcı çerçeve ----
    drect(fx(PU_X[0]), fy(PU_Y[1]) + 2, fx(PU_X[1]), fy(PU_Y[0]), TURUNCU, 1, 5, 3)
    for ad_, k, eks in TASIYICI:
        drect(fx(k[0]), fy(k[3]), fx(k[1]), fy(k[2]), INK, 1, 4, 3)
    balon(fx(2750), fy(560), fx(2690), fy(640), 14)
    balon(fx(3000), fy(PU_Y[0]), fx(2930), fy(655), 19)
    balon(fx(TASIYICI[7][1][1]), fy(470), fx(3260), fy(530), 20)                              # dikme_2 (x 3157,5–3187,5)
    isaret(fx(3260) + 36, fy(530), 6)
    olcu_v(fx(3985), fy(Y_DUZ), fy(KL[3]), sayi(Y_DUZ - KL[3]), f7, RED, "l")
    isaret(fx(X_F1) + 34, fy((Y_DUZ + KL[3]) / 2.0), 4)
    # ---- fırın üstü: davlumbaz (arkada) · kalkan · takozlar · raf · kutu yedeği · kompresör ----
    d.rectangle([fx(X_F0 + 3), fy(DAV[1]), fx(X_F1 - 3), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    d.line([(fx(RAF_X[0]), fy(FT.ISI_KALKANI_Y[0])), (fx(RAF_X[1]), fy(FT.ISI_KALKANI_Y[0]))], fill=INK, width=1)
    for x_ in TAKOZ_X:
        d.rectangle([fx(x_ - 8.0), fy(FT.UST_RAF_Y[0]), fx(x_ + 8.0), fy(YG1)], fill=SOFT, outline=INK, width=1)
    d.rectangle([fx(RAF_X[0]), fy(FT.UST_RAF_Y[1]), fx(RAF_X[1]), fy(FT.UST_RAF_Y[0])], fill=INK)
    d.rectangle([fx(KUTU_X[0]), fy(KUTU_Y[1]), fx(KUTU_X[1]), fy(KUTU_Y[0])], fill=KARTON, outline=KARTON_C, width=2)
    txt(fx(sum(KUTU_X) / 2.0), fy(sum(KUTU_Y) / 2.0), "pizza kutusu yedeği · %d kutu" % KUTU_N, f8, INK, "mm")
    balon(fx(KUTU_X[0] + 120.0), fy(1720), fx(KUTU_X[0] + 60.0), fy(1790), 17)
    isaret(fx(sum(KUTU_X) / 2.0), fy(sum(KUTU_Y) / 2.0) + 36, 3)
    d.rectangle([fx(KOMP_X[0]), fy(KOMP_Y[1]), fx(KOMP_X[1]), fy(KOMP_Y[0])], fill=EVC, outline=INK, width=2)
    txt(fx(sum(KOMP_X) / 2.0), fy(sum(KOMP_Y) / 2.0), "kompresör", f8, INK, "mm")
    balon(fx(KOMP_X[1] - 60.0), fy(1720), fx(X_F1) + 50, fy(1760), 18)
    txt(fx((KUTU_X[1] + KOMP_X[0]) / 2.0), fy(1640), "davlumbaz", f7, GRAY, "mm")
    txt(fx((KUTU_X[1] + KOMP_X[0]) / 2.0), fy(1640) + 20, "(arka yarı) · önü boş", f7, GRAY, "mm")
    balon(fx((KUTU_X[1] + KOMP_X[0]) / 2.0), fy(1760), fx((KUTU_X[1] + KOMP_X[0]) / 2.0) + 50, fy(1800), 15)
    balon(fx(RAF_X[1] - 2.0), fy(FT.UST_RAF_Y[1] - 2.0), fx(X_F1) + 50, fy(1420), 16)
    yr = fy(H_MAK) - 56
    for xx in (KUTU_X[0], KUTU_X[1], KOMP_X[0], KOMP_X[1]):
        dline((fx(xx), yr - 6), (fx(xx), fy(KUTU_Y[1]) - 4), GRAY, 1, 4, 4)
    olcu_h(fx(KUTU_X[0]), fx(KUTU_X[1]), yr, sayi(KUTU_X[1] - KUTU_X[0]), f7, INK)
    olcu_h(fx(KUTU_X[1]), fx(KOMP_X[0]), yr, "boş %s" % sayi(KOMP_X[0] - KUTU_X[1]), f7, INK)
    olcu_h(fx(KOMP_X[0]), fx(KOMP_X[1]), yr, sayi(KOMP_X[1] - KOMP_X[0]), f7, INK)
    # ---- gövde (ön yüz) · içi: ön oda · uç duvarları · oda · ısıtıcılar ----
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
    balon(fx(T0 + 230), fy(1150), fx(T0 + 300), fy(1195), 1)
    balon(fx(T1 - 120), fy(TUN_Y[1] - 5), fx(T1 - 180), fy(1195), 2)
    balon(fx((D0 + T0) / 2), fy(1150), fx(2700), fy(1160), 4)
    txt(fx((X_F0 + D0) / 2), fy(1180), "ön oda", f7, GRAY, "mm")
    balon(fx((X_F0 + D0) / 2), fy(1225), fx(2700), fy(1240), 5)
    # bant (gizli): üst kol · alt kol · rulolar · 4 ürün
    for xr in (RX0, RX1):
        d.ellipse([fx(xr - RR), fy(RY + RR), fx(xr + RR), fy(RY - RR)], fill=EVC, outline=INK, width=1)
    dline((fx(RX0), fy(BANT_F)), (fx(RX1), fy(BANT_F)), INK, 3, 10, 5)
    dline((fx(RX0), fy(FT.ALT_KOL_Y[0])), (fx(RX1), fy(FT.ALT_KOL_Y[0])), GRAY, 1, 10, 5)
    balon(fx(RX1), fy(RY - RR), fx(X_F1) + 50, fy(900), 3)
    for i in range(N_ICERIDE):
        xm = XC + (i - (N_ICERIDE - 1) / 2.0) * ADIM
        drect(fx(xm - 150), fy(BANT_F + 12), fx(xm + 150), fy(BANT_F + 1), (180, 140, 70), 1, 5, 3)
    # ön oda: giriş bandı · motoru
    d.rectangle([fx(GBX0), fy(BANT_F), fx(GBX1), fy(FT.GB_RY - 11.5)], fill=(214, 196, 170), outline=INK, width=1)
    for xr in (FT.GB_XB, FT.GB_XT):
        d.ellipse([fx(xr - 10), fy(FT.GB_RY + 10), fx(xr + 10), fy(FT.GB_RY - 10)], fill=BG, outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), fy(FT.GB_MOTOR[1] + 28.5), fx(FT.GB_MOTOR[0] + 28.5), fy(FT.GB_MOTOR[1] - 28.5), INK, 1, 4, 3)
    dline((fx(FT.GB_XT), fy(FT.GB_RY)), (fx(FT.GB_MOTOR[0]), fy(FT.GB_MOTOR[1])), GRAY, 1, 4, 3)
    balon(fx(FT.GB_MOTOR[0] - 28.5), fy(FT.GB_MOTOR[1]), fx(2462), fy(1170), 7)
    balon(fx((GBX0 + GBX1) / 2), fy(FT.GB_RY - 11.5), fx(2440), fy(960), 6)
    # komşular: C kaidesi · TOPPING tabla + disk aktarmada · ürün diskte · tekne · K bandı · ölü plaka
    d.rectangle([fx(FXM), fy(KD.Y_MEK), fx(KD.C_X[1]), fy(KD.Y_DUZ)], fill=BG, outline=KOMSU, width=2)
    txt(fx((FXM + KD.C_X[1]) / 2.0), fy((KD.Y_MEK + KD.Y_DUZ) / 2.0), "C kaidesi %s–%s" % (sayi(KD.Y_DUZ), sayi(KD.Y_MEK)), f7, KOMSU, "mm")
    d.rectangle([fx(TAB_XC - TAB_R), fy(TABLA_Y[1]), fx(TAB_XC + TAB_R), fy(TABLA_Y[0])], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(TAB_XC - 140), fy(P_SUREC + 9), fx(TAB_XC + 140), fy(P_SUREC)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X_F0) - 16, fy(1260), "TOPPING tabla + diski aktarmada", f7, KOMSU, "rm")
    txt(fx(X_F0) - 16, fy(1260) + 20, "kenar x %s · disk üstü %s" % (sayi(TAB_XC + TAB_R), sayi(P_SUREC)), f7, KOMSU, "rm")
    drect(fx(2400), fy(TEKNE_Y[1]), fx(2500), fy(TEKNE_Y[0]), KOMSU, 1, 5, 3)
    txt(fx(2400) - 8, fy(sum(TEKNE_Y) / 2.0), "TOPPING mekanizma teknesi (v24) · 2500'de biter", f7, KOMSU, "rm")
    d.ellipse([fx(K_KUY - K_KR), fy(K_KY + K_KR), fx(K_KUY + K_KR), fy(K_KY - K_KR)], fill=EVC, outline=KOMSU, width=2)
    d.rectangle([fx(K_KUY), fy(PLAKA_K), fx(4380), fy(PLAKA_K - 4.0)], fill=KOMSU)
    txt(fx(4380), fy(PLAKA_K) - 18, "K bandı %s" % sayi(PLAKA_K), f7, KOMSU, "rm")
    d.rectangle([fx(OLU[0]), fy(PLAKA_K + 1.5), fx(OLU[1]), fy(PLAKA_K - 1.0)], fill=ACC)
    balon(fx((OLU[0] + OLU[1]) / 2), fy(PLAKA_K + 1.5), fx(X_F1) + 50, fy(1070), 8)
    # ölçüler
    yo_ = fy(1275)
    olcu_h(fx(X_F0), fx(D0), yo_, sayi(FT.ON_ODA), f7, INK)
    olcu_h(fx(D0), fx(T0), yo_, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(T0), fx(T1), yo_, "ısıtılan %s · aynı anda %d ürün (adım %s)" % (sayi(FT.ODA), N_ICERIDE, sayi(ADIM)), f8, TURUNCU)
    olcu_h(fx(T1), fx(D1), yo_, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(B0), fx(B1), fy(880), "bant %s × %s uçtan uca · %s – %s · gövde dışına çıkmaz" % (sayi(FT.BANT_W), sayi(B1 - B0), sayi(B0), sayi(B1)), f8, INK)
    olcu_h(fx(X_F0), fx(X_F1), fy(0) + 44, "gövde = F modülü %s (TP10 kesiti · boy ÖZEL) · derinlik 830 + çıkıntı %s = %s" % (sayi(X_F1 - X_F0), sayi(ZS), sayi(DZ + ZS)), f9, ACC)
    yd = fy(BANT_F + 59.0)
    d.line([(fx(TAB_XC + TAB_R), yd), (fx(B0), yd)], fill=INK, width=2)
    for xx in (TAB_XC + TAB_R, B0):
        d.line([(fx(xx), yd - 8), (fx(xx), yd + 8)], fill=INK, width=2)
    txt(fx(TAB_XC + TAB_R) - 10, yd, "disk → fırın bandı %s (giriş bandı)" % sayi(B0 - TAB_XC - TAB_R), f7, INK, "rm")
    for yy in (0.0, Y_ALT, PU_Y[0], YG0, BANT_F, BANT_F + FT.IC_H, YG1, FT.UST_RAF_Y[1], H_MAK):
        d.line([(fx(4400) - 20, fy(yy)), (fx(4400) - 4, fy(yy))], fill=INK, width=2)
        txt(fx(4400), fy(yy), sayi(yy), f7, INK, "lm")


# ============================== ÜST GÖRÜNÜŞ ==============================
def ust():
    txt(FX0, PY0 - 60, "ÜST GÖRÜNÜŞ (fırın üstü raf + davlumbaz kaldırılmış · ürün yolu DÜZ z −170 · fırın 79 öne)", f16, ACC)
    d.rectangle([fx(X_F0), pz(-DZ), fx(X_F1), pz(0)], outline=LINE, width=3)
    # K bandı + ölü plaka
    d.rectangle([fx(K_KUY - K_KR - 2), pz(K_Z0), fx(4380), pz(K_Z1)], fill=(240, 240, 243), outline=KOMSU, width=2)
    d.rectangle([fx(4010), pz(K_Z0 - 5), fx(4380), pz(K_Z0 - 2)], fill=KOMSU)
    txt(fx(4380) - 6, pz(K_Z1) + 14, "K bandı %s (kesme_cad_v4)" % sayi(K_Z1 - K_Z0), f7, KOMSU, "rm")
    d.rectangle([fx(OLU[0]), pz(GBZ[0]), fx(OLU[1]), pz(GBZ[1])], fill=(230, 238, 250), outline=ACC, width=1)
    # gövde · ön oda · uç duvarları · oda · teknik bölme · ekran · fanlar
    d.rectangle([fx(X_F0), pz(DTP1), fx(X_F1), pz(DTP0)], fill=PASL, outline=INK, width=3)
    d.rectangle([fx(D0), pz(DTP1), fx(X_F1), pz(TUN_Z[0] - 5.5)], fill=(222, 226, 232), outline=INK, width=1)
    d.rectangle([fx(X_F0) + 2, pz(DTP1) + 2, fx(D0), pz(DTP0) - 2], fill=(240, 242, 245))
    d.rectangle([fx(X_F0), pz(0), fx(X_F1), pz(DTP0)], outline=RED, width=3)                                   # ÇIKINTI
    txt(fx(XC), pz(DTP0 / 2.0), "ÇIKINTI %s · gövde ön yüzün önünde · y %s–%s" % (sayi(ZS), sayi(YG0), sayi(YG1)), f8, RED, "mm")
    txt(fx(X_F0) + 8, pz(0) + 18, "hat ön yüzü (z 0)", f7, GRAY, "lm")                              # denetçi: gövde dolgusunun ÜSTÜNE (v5/v6 ilk: altında, görünmüyordu)
    for a, b in ((D0, T0), (T1, D1)):
        tarali(fx(a), pz(TUN_Z[0]), fx(b), pz(TUN_Z[1]), (206, 208, 214), 9)
        drect(fx(a), pz(TUN_Z[0]), fx(b), pz(TUN_Z[1]), GRAY, 1)
    d.rectangle([fx(T0), pz(TUN_Z[0]), fx(T1), pz(TUN_Z[1])], fill=ODA_R)
    drect(fx(T0), pz(TUN_Z[0]), fx(T1), pz(TUN_Z[1]), GRAY, 1)
    d.rectangle([fx(XC - FT.EKRAN[0] / 2), pz(DTP1) - 2, fx(XC + FT.EKRAN[0] / 2), pz(DTP1) + 7], fill=INK)
    balon(fx(XC + 60), pz(DTP1) + 4, fx(XC + 200), pz(DTP1) + 60, 12)
    for fx_ in (D0 + 76.0, X_F1 - 140.0):
        d.ellipse([fx(fx_ - FT.FAN_R), pz(DTP1) - 2, fx(fx_ + FT.FAN_R), pz(DTP1) + 2], outline=INK, width=1)
    # tahrik + gergi (teknik bölmede, gizli)
    drect(fx(RX1 - 32), pz(-586 + ZS), fx(RX1 + 26), pz(-521 + ZS), INK, 1, 4, 3)
    drect(fx(RX1 - 170), pz(-583 + ZS), fx(RX1 - 32), pz(-523 + ZS), INK, 1, 4, 3)
    balon(fx(RX1 - 100), pz(-553 + ZS), fx(RX1 - 140), pz(-660 + ZS), 10)
    drect(fx(2556), pz(-520 + ZS), fx(RX0 - 18), pz(-500 + ZS), INK, 1, 4, 3)
    balon(fx(2575), pz(-510 + ZS), fx(2650), pz(-660 + ZS), 11)
    # bant (gizli) + giriş bandı
    d.rectangle([fx(B0), pz(BZ[0]), fx(B1), pz(BZ[1])], fill=EVC)
    drect(fx(B0), pz(BZ[0]), fx(B1), pz(BZ[1]), INK, 1, 6, 4)
    for i in range(0, int(B1 - B0), 40):
        d.line([(fx(B0 + i), pz(BZ[0]) + 1), (fx(B0 + i), pz(BZ[1]) - 1)], fill=(190, 205, 225), width=1)
    d.rectangle([fx(GBX0), pz(GBZ[0]), fx(GBX1), pz(GBZ[1])], fill=(214, 196, 170), outline=INK, width=1)
    drect(fx(FT.GB_MOTOR[0] - 28.5), pz(GBMZ - 76), fx(FT.GB_MOTOR[0] + 28.5), pz(GBMZ), INK, 1, 5, 3)
    # TOPPING: disk aktarmada + tekne (gizli) + çıkış yarığı çerçevesi
    d.ellipse([fx(TAB_XC - TAB_R), pz(ZT - TAB_R), fx(TAB_XC + TAB_R), pz(ZT + TAB_R)], outline=KOMSU, width=2)
    drect(fx(2400), pz(-415), fx(2500), pz(-5), KOMSU, 1, 4, 3)                                               # tekne 2500'de biter
    YK = FT.YARIK_V2[0]
    d.rectangle([fx(YK[0]), pz(YK[4]), fx(YK[1]), pz(YK[5])], fill=BG, outline=KOMSU, width=1)
    txt(fx(YK[0]) - 6, pz(-430), "TOPPING çıkış yarığı çerçevesi · z %s…%s · y %s–%s" % (sayi(YK[4]), sayi(YK[5]), sayi(YK[2]), sayi(YK[3])), f7, KOMSU, "rm")
    # ürün yolu: diskte · fırın · K
    pts = [(fx(x), pz(FT.urun_z(float(x)))) for x in range(int(TAB_XC), 4301, 8)]                          # düz −170
    d.line(pts, fill=(200, 120, 40), width=3)
    for xm, zm in ((TAB_XC, ZT), (TAB_XC, ZUF), (XC - 1.5 * ADIM, ZUF), (XC - 0.5 * ADIM, ZUF), (XC + 0.5 * ADIM, ZUF), (XC + 1.5 * ADIM, ZUF), (4300.0, ZT)):
        d.ellipse([fx(xm - 140), pz(zm - 140), fx(xm + 140), pz(zm + 140)], outline=(180, 140, 70), width=2)
    txt(fx(2400) - 6, pz(ZT - TAB_R - 36), "aktarma iticisi DÜZ 170 (itici_cad_v4) · kayma yok", f7, (200, 120, 40), "rm")
    # eksenler
    eksen((fx(2150), pz(ZT)), (fx(4400), pz(ZT)), ACC)
    etiket(fx(2150) + 4, pz(ZT) + 16, "hat ürün ekseni z %s" % sayi(ZT), f7, ACC, "lm")
    eksen((fx(B0), pz(ZB_C)), (fx(B1), pz(ZB_C)), TURUNCU)
    etiket(fx(T1) - 56, pz(ZB_C) - 14, "bant ekseni z %s" % sayi(ZB_C), f7, TURUNCU, "rm")
    txt(fx(T0) + 8, pz(DTP1 + 40), "fırında ürün merkezi z %s (ön kenar %s · tünel iç yüzü 0 → 20 pay) = tabla ekseni" % (sayi(ZUF), sayi(ZUF + 150)), f7, (200, 120, 40), "lm")
    xr = fx(4400) + 30
    olcu_v(xr, pz(DTP1), pz(DTP0), "%s (föy)" % sayi(FT.D_TP), f8, INK, "r")
    olcu_v(xr, pz(-DZ), pz(DTP1), sayi(DZ + DTP1), f7, INK, "r")
    olcu_v(xr, pz(0), pz(DTP0), "çıkıntı %s" % sayi(ZS), f8, RED, "r")
    olcu_v(fx(T1) - 40, pz(TUN_Z[0]), pz(DTP0), "%s + %s" % (sayi(DTP0 - TUN_Z[1]), sayi(TUN_Z[1] - TUN_Z[0])), f7, INK, "l", bg=True)
    yb = pz(DTP0) + 34                                                                                      # v6: çıkıntının ALTINDA (v5'te yazıya biniyordu)
    for xx in (X_F0, D0, T0, T1, D1):
        dline((fx(xx), pz(DTP0) + 2), (fx(xx), yb + 8), GRAY, 1, 4, 4)
    olcu_h(fx(X_F0), fx(D0), yb, sayi(FT.ON_ODA), f7, INK)
    olcu_h(fx(D0), fx(T0), yb, sayi(FT.DUVAR), f7, INK)
    olcu_h(fx(T0), fx(T1), yb, "ısıtılan %s" % sayi(FT.ODA), f7, TURUNCU)
    olcu_h(fx(T1), fx(D1), yb, sayi(FT.DUVAR), f7, INK)


# ============================== YAN KESİT ==============================
def yan():
    txt(SX0, 172, "YAN KESİT (x %s · soldan bakış · kesit TP10 föyüyle aynı)" % sayi(XC), f16, ACC)
    d.rectangle([sx(-DZ), fy(H_MAK), sx(0), fy(0)], outline=LINE, width=3)
    d.rectangle([sx(-DZ + 30), fy(Y_ALT), sx(-30), fy(0)], fill=SOFT, outline=LINE, width=1)
    # ---- çekmeceli dolap kesiti (K6): tavan 668–728 · ısı kalkanı PU 60 728–788 · kirişler (kesik) · dikmeler (arkada, gizli) · K6 önleri ----
    d.rectangle([sx(-DZ), fy(Y_DUZ), sx(0), fy(Y_ALT)], fill=FILL, outline=LINE, width=2)
    tarali(sx(ZP[0]), fy(PU_Y[0]), sx(ZP[1]), fy(TAVAN_F), (214, 216, 222), 9)
    d.rectangle([sx(ZP[0]), fy(PU_Y[0]), sx(ZP[1]), fy(TAVAN_F)], outline=GRAY, width=1)
    d.rectangle([sx(ZP[0]), fy(PU_Y[1]) + 2, sx(ZP[1]), fy(PU_Y[0])], fill=(255, 240, 232))
    tarali(sx(ZP[0]), fy(PU_Y[1]) + 2, sx(ZP[1]), fy(PU_Y[0]), (238, 176, 146), 7)
    d.rectangle([sx(ZP[0]), fy(PU_Y[1]) + 2, sx(ZP[1]), fy(PU_Y[0])], outline=TURUNCU, width=1)
    for ad_, k, eks in TASIYICI:
        if eks == "x":
            d.rectangle([sx(k[4]), fy(k[3]), sx(k[5]), fy(k[2])], fill=BG, outline=INK, width=2)
        elif eks == "y" and k[0] > XC:
            drect(sx(k[4]), fy(k[3]), sx(k[5]), fy(k[2]), INK, 1, 4, 3)
    for a, b, y0, y1, _k in K6_ON:
        d.rectangle([sx(SC.Z_ON0), fy(y1), sx(SC.Z_ON1), fy(y0)], fill=ONYUZ, outline=LINE, width=1)
    balon(sx(-520), fy(430), sx(-580), fy(360), 14)
    balon(sx(-300), fy(PU_Y[0] + 30.0), sx(-270), fy(640), 19)
    balon(sx(TASIYICI[0][1][4] + 20.0), fy(TASIYICI[0][1][2]), sx(-170), fy(640), 20)
    # ---- fırın üstü: davlumbaz (arka yarı) · kutu yedeği (kesik) · raf · kalkan · takozlar ----
    d.rectangle([sx(DAV_Z[0] + 3), fy(DAV[1]), sx(DAV_Z[1]), fy(DAV[0])], fill=BG, outline=LINE, width=2)
    txt(sx(sum(DAV_Z) / 2.0), fy(1580), "davlumbaz · arka yarı", f7, GRAY, "mm")
    txt(sx(sum(DAV_Z) / 2.0), fy(1580) + 20, "fan + yağ/karbon filtre", f7, GRAY, "mm")
    balon(sx(-700), fy(1700), sx(-760), fy(1780), 15)
    d.rectangle([sx(KUTU_Z[0]), fy(KUTU_Y[1]), sx(KUTU_Z[1]), fy(KUTU_Y[0])], fill=KARTON, outline=KARTON_C, width=2)
    txt(sx(sum(KUTU_Z) / 2.0), fy(1580), "pizza kutusu yedeği", f8, INK, "mm")
    txt(sx(sum(KUTU_Z) / 2.0), fy(1580) + 22, "%d × %s = %s" % (KUTU_N, sayi(KT.T), sayi(KUTU_N * KT.T)), f7, INK, "mm")
    balon(sx(-300), fy(1700), sx(-360), fy(1780), 17)
    d.line([(sx(RAF_Z[0]), fy(FT.ISI_KALKANI_Y[0])), (sx(RAF_Z[1]), fy(FT.ISI_KALKANI_Y[0]))], fill=INK, width=1)
    for z_ in TAKOZ_Z:
        d.rectangle([sx(z_ - 8.0), fy(FT.UST_RAF_Y[0]), sx(z_ + 8.0), fy(YG1)], fill=SOFT, outline=INK, width=1)
    d.rectangle([sx(RAF_Z[0]), fy(FT.UST_RAF_Y[1]), sx(RAF_Z[1]), fy(FT.UST_RAF_Y[0])], fill=INK)
    balon(sx(RAF_Z[1] - 2.0), fy(FT.UST_RAF_Y[1] - 2.0), sx(40), fy(1420), 16)
    # ---- F arka sacı ----
    d.rectangle([sx(-DZ), fy(FT.ISI_KALKANI_Y[0]), sx(-DZ + 1.5), fy(YG0)], fill=INK)
    balon(sx(-DZ), fy(1100), sx(-DZ) - 40, fy(1160), 13)
    # ---- gövde kesiti ----
    d.rectangle([sx(DTP1), fy(YG1), sx(DTP0), fy(YG0)], fill=PASL, outline=INK, width=3)
    tarali(sx(TUN_Z[1]), fy(YG1) + 2, sx(DTP0) - 2, fy(YG0) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(YG1) + 2, sx(TUN_Z[1]), fy(TUN_Y[1]) - 2, (214, 216, 222), 9)
    tarali(sx(TUN_Z[0] - 4), fy(TUN_Y[0]) + 2, sx(TUN_Z[1]), fy(YG0) - 2, (214, 216, 222), 9)
    d.rectangle([sx(DTP1), fy(YG1), sx(TUN_Z[0] - 5.5), fy(YG0)], fill=(222, 226, 232), outline=INK, width=1)
    balon(sx((DTP1 + TUN_Z[0]) / 2), fy((YG0 + YG1) / 2), sx((DTP1 + TUN_Z[0]) / 2) - 30, fy(1230), 12)
    d.rectangle([sx(DTP1) - 9, fy(YG0 + FT.EKRAN[2] + FT.EKRAN[1]), sx(DTP1), fy(YG0 + FT.EKRAN[2])], fill=INK)
    d.rectangle([sx(0), fy(YG1), sx(DTP0), fy(YG0)], outline=RED, width=3)                                      # çıkıntı
    txt(sx(DTP0) + 8, fy(1200), "çıkıntı %s" % sayi(ZS), f8, RED, "lm")
    d.rectangle([sx(TUN_Z[0]), fy(TUN_Y[1]), sx(TUN_Z[1]), fy(TUN_Y[0])], fill=SICAK, outline=INK, width=1)
    for (ya, yb) in ((TUN_Y[1] - 10.0, TUN_Y[1] - 1.0), (RY - 12.0, RY - 4.0)):
        d.rectangle([sx(BZ[0]), fy(yb), sx(BZ[1]), fy(ya)], fill=(250, 190, 160), outline=TURUNCU, width=1)
    balon(sx(BZ[0] + 60), fy(TUN_Y[1] - 5), sx(BZ[0] + 100), fy(1230), 2)
    d.rectangle([sx(BZ[0]), fy(BANT_F), sx(BZ[1]), fy(BANT_F - 6)], fill=INK)
    d.rectangle([sx(BZ[0]), fy(FT.ALT_KOL_Y[1]), sx(BZ[1]), fy(FT.ALT_KOL_Y[0])], fill=GRAY)
    balon(sx(BZ[0] + 40), fy(BANT_F - 3), sx(BZ[0] + 90), fy(880), 3)
    d.rectangle([sx(ZUF - 140), fy(BANT_F + 12), sx(ZUF + 140), fy(BANT_F + 1)], fill=URUN, outline=(180, 140, 70), width=1)
    drect(sx(ZUF - 150), fy(BANT_F + 28), sx(ZUF + 150), fy(BANT_F + 1), (180, 140, 70), 1, 4, 3)
    # ---- ölçüler ----
    olcu_h(sx(DTP1), sx(DTP0), fy(H_MAK) - 30, "%s (föy)" % sayi(FT.D_TP), f8, INK)
    olcu_h(sx(-DZ), sx(DTP1), fy(H_MAK) - 30, sayi(DZ + DTP1), f7, INK)
    olcu_h(sx(-DZ), sx(DTP0), fy(H_MAK) - 70, "F %s + çıkıntı %s = %s" % (sayi(DZ), sayi(ZS), sayi(DZ + ZS)), f8, ACC)
    isaret(sx(DTP0) + 40, fy(H_MAK) - 70, 2)
    ya_, yb_ = fy(560), fy(515)                                                                              # v6: dolap kesitinde, ısı kalkanının altında
    for zz, yy in ((DTP1, ya_), (TUN_Z[0] - 5.5, ya_), (TUN_Z[0], ya_), (TUN_Z[1], ya_), (DTP0, ya_), (BZ[0], yb_), (BZ[1], yb_)):
        dline((sx(zz), fy(YG0) + 2), (sx(zz), yy + 8), GRAY, 1, 4, 4)
    olcu_h(sx(DTP1), sx(TUN_Z[0] - 5.5), ya_, "≈ 239", f7, INK)
    olcu_h(sx(TUN_Z[0]), sx(TUN_Z[1]), ya_, "≈ %s" % sayi(TUN_Z[1] - TUN_Z[0]), f7, INK)
    olcu_h(sx(TUN_Z[1]), sx(DTP0), ya_, "≈ %s" % sayi(DTP0 - TUN_Z[1]), f7, INK)
    olcu_h(sx(BZ[0]), sx(BZ[1]), yb_, "bant %s" % sayi(FT.BANT_W), f7, INK)
    olcu_h(sx(ZUF - 150), sx(ZUF + 150), fy(BANT_F + 28) - 26, "ürün Ø300 z %s" % sayi(ZUF), f7, (180, 140, 70))
    xd = sx(DTP0) + 110
    olcu_v(xd, fy(YG1), fy(YG0), "%s" % sayi(FT.H_GOV), f7, INK, "r")
    olcu_v(xd, fy(FT.UST_RAF_Y[1]), fy(YG1), "%s" % sayi(FT.UST_RAF_Y[1] - YG1), f7, INK, "r")
    olcu_v(xd, fy(KUTU_Y[1]), fy(KUTU_Y[0]), "%s (%d kutu)" % (sayi(KUTU_Y[1] - KUTU_Y[0]), KUTU_N), f7, INK, "r")
    olcu_v(xd, fy(Y_DUZ), fy(Y_ALT), "%s dolap" % sayi(Y_DUZ - Y_ALT), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F), fy(YG0), "≈ %s" % sayi(FT.BANT_Y), f7, INK, "r")
    olcu_v(xd + 90, fy(BANT_F + FT.IC_H), fy(BANT_F), "%s (föy)" % sayi(FT.IC_H), f7, INK, "r")
    olcu_v(xd + 90, fy(PU_Y[1]), fy(PU_Y[0]), "PU %s" % sayi(PU_Y[1] - PU_Y[0]), f7, TURUNCU, "r")
    for yy in (Y_ALT, PU_Y[0], YG0, BANT_F, BANT_F + FT.IC_H, YG1, FT.UST_RAF_Y[1], H_MAK):
        d.line([(sx(DTP0) + 6, fy(yy)), (sx(DTP0) + 22, fy(yy))], fill=INK, width=2)
        txt(sx(DTP0) + 28, fy(yy), sayi(yy), f7, INK, "lm")
    txt(sx(-DZ), fy(0) + 26, "arka (z −830)", f7, GRAY, "lm")
    txt(sx(0), fy(0) + 26, "ön (z 0) · gövde +%s" % sayi(ZS), f7, GRAY, "rm")


# ============================== LİSTE + BAŞLIK ==============================
def liste():
    x0, y0 = LX0, LY0
    txt(x0, y0 - 38, "PARÇA LİSTESİ", f16, ACC)
    ch = [t for a, k, t in TASIYICI]
    satir = [
        ("1", "Fırın gövdesi · TP10 kesiti · paslanmaz · yalıtımlı · boy ÖZEL · 79 mm ÖNE", "1500 × 730 × 517 · y %s–%s · z +79…−651" % (sayi(YG0), sayi(YG1)), "föy kesiti + özel · Kemal 27 Eyl"),
        ("2", "Kızılötesi ısıtıcılar üst + alt · 2 bölge (şematik)", "400 °C · ≈14 kW", "föy ölçekli · VARSAYIM"),
        ("3", "Konveyör · tel örgü bant · rulolar uç duvarı içinde", "381 × 1428 · üst %s" % sayi(BANT_F), "VARSAYIM"),
        ("4", "Uç duvarı × 2 · yalıtım · geçit %s–%s" % (sayi(GEC_Y[0]), sayi(GEC_Y[1])), sayi(FT.DUVAR), "hesap"),
        ("5", "Giriş ön odası · ısıtılmaz", sayi(FT.ON_ODA), "hesap"),
        ("6", "Giriş bandı (bizim) · PTFE 320 · Ø20 burun + tahrik · disk %s → bant %s" % (sayi(P_SUREC), sayi(BANT_F)), "%s–%s · üst %s" % (sayi(GBX0), sayi(GBX1), sayi(BANT_F)), "hesap"),
        ("7", "Giriş bandı motoru STP-MTR-23079 + GT2", "NEMA23 · 1:1 · y %s" % sayi(FT.GB_MOTOR[1]), "katalog"),
        ("8", "Çıkış ölü plakası (bizim) · 2,5 mm L · → K bandı %s" % sayi(PLAKA_K), "%s–%s · üst %s" % (sayi(OLU[0]), sayi(OLU[1]), sayi(PLAKA_K + 1.5)), "hesap"),
        ("9", "Çıkıntı: gövde ön yüzün önünde (x %s–%s · y %s–%s)" % (sayi(X_F0), sayi(X_F1), sayi(YG0), sayi(YG1)), sayi(ZS), "Kemal 27 Eyl"),
        ("10", "Bant tahriki · redüktör + motor (teknik bölmede)", "≈2,6 dev/dk", "VARSAYIM"),
        ("11", "Bant gergisi · M8 (teknik bölmede)", "—", "VARSAYIM"),
        ("12", "Dokunmatik ekran + teknik bölme (arkada)", "≈ 189 × 151 · ≈ 239", "föy"),
        ("13", "F arka sacı (bizim)", "%s–%s" % (sayi(YG0), sayi(FT.ISI_KALKANI_Y[0])), "hesap"),
        ("14", "Çekmeceli dolap · fırın altı: K5 (3 pide + tatlı) · K6 (3 içecek) · şerit", "%s–%s · üstü düz %s" % (sayi(Y_ALT), sayi(Y_DUZ), sayi(Y_DUZ)), "store_cad_v6"),
        ("15", "Egzoz davlumbazı (bizim) · arka yarı · fan + yağ/karbon filtre · komşulara asılı", "%s–%s · z %s…%s" % (sayi(DAV[0]), sayi(DAV[1]), sayi(DAV_Z[0]), sayi(DAV_Z[1])), "v47"),
        ("16", "Üst raf 4 mm · 10 takoz Ø16 · altında ışınım kalkanı 0,8 (%s)" % sayi(FT.ISI_KALKANI_Y[0]), "%s–%s" % (sayi(FT.UST_RAF_Y[0]), sayi(FT.UST_RAF_Y[1])), "hesap · 99 kg"),
        ("17", "Pizza kutusu yedeği · fırın üstü SOL · %d kutu" % KUTU_N, "%s × %s × %s · %s–%s" % (sayi(KUTU_X[1] - KUTU_X[0]), sayi(KUTU_Z[1] - KUTU_Z[0]), sayi(KUTU_Y[1] - KUTU_Y[0]), sayi(KUTU_Y[0]), sayi(KUTU_Y[1])), "Kemal 27 Eyl"),
        ("18", "Kompresör JUN-AIR OF302-15B · fırın üstü SAĞ · zarf", "%s × %s × %s · %s–%s" % (sayi(KOMP_X[1] - KOMP_X[0]), sayi(KOMP_Z[1] - KOMP_Z[0]), sayi(KOMP_Y[1] - KOMP_Y[0]), sayi(KOMP_Y[0]), sayi(KOMP_Y[1])), "montaj · 25 kg"),
        ("19", "Isı kalkanı PU 60 · dolabın içinde, fırın altında", "%s–%s × %s–%s" % (sayi(PU_X[0]), sayi(PU_X[1]), sayi(PU_Y[0]), sayi(PU_Y[1])), "store_cad_v6"),
        ("20", "Taşıyıcı çerçeve 304 · %d kiriş 40 × 40 · %d çapraz · %d dikme 30 × 30" % (ch.count("x"), ch.count("z"), ch.count("y")),
         "kiriş %s–%s · dikme %s–%s" % (sayi(SC.TK_Y[0]), sayi(SC.TK_Y[1]), sayi(TASIYICI[5][1][2]), sayi(TASIYICI[5][1][3])), "store_cad_v6 · hesap"),
    ]
    kol = (0, 46, 560, 870)
    gen = 1088.0                                                                         # tablo sağ kenarı başlık çizgisiyle aynı (W_PX − 62)
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("NO", "PARÇA", "ÖLÇÜ", "KAYNAK")):
        txt(x0 + k + 8, y0 + 14, b, f7, INK, "lm")
    y = y0 + 28
    for r in satir:
        d.line([(x0, y + 28), (x0 + gen, y + 28)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            txt(x0 + k + 8, y + 14, v, f7, INK if k < kol[3] else GRAY, "lm")
        y += 28
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    TABLO = (x0, y0, x0 + gen, y, kol)
    y += 56
    ya = y
    txt(x0, y, "KOMŞU UYARLAMALARI", f16, ACC); txt(x0, y + 40, "yalnız bu sürümde", f7, GRAY, "lm"); y += 60
    YK = FT.YARIK_V2
    for s_ in ("C · giriş bandı F'nin ön odasında (bizim) · ekseni −170",
               "C · çıkış yarığı çerçevesi z %s…%s · alt çıta %s–%s" % (sayi(YK[0][4]), sayi(YK[0][5]), sayi(YK[0][2]), sayi(YK[1][2])),
               "C · aktarma iticisi DÜZ 170 (itici_cad_v4) · disk %s" % sayi(P_SUREC),
               "A / C · kaide %s–%s (kaide_cad_v1) · mekanizma tabanı %s" % (sayi(KD.Y_DUZ), sayi(KD.Y_MEK), sayi(KD.Y_MEK)),
               "K · kesme_cad_v4 · taban %s · bant %s · giriş çiti YOK" % (sayi(KS.H_B), sayi(KS.BANT)),
               "B · dolap store_cad_v6 · F taban dolabı YOK · PU 60 + çerçeve",
               "F · 79 öne: çıkıntı 1500 × 517 × 79 · modül 909 derin · altı %s" % sayi(Y_DUZ)):
        txt(x0, y, s_, f7, INK, "lm"); y += 24
    x2, y = x0 + 500, ya
    txt(x2, y, "AÇIK / KARAR", f16, RED); y += 46
    for i, s_ in enumerate(("çıkıntı 79: üretici ince duvar (60) + pay 10 verirse 50'ye iner [V]",
                            "830 derinlik kuralı F'de 909 (çıkıntı 79)",
                            "kutu stoğu %d + %d = %d ≈ 2,8 gün · asansörle alınabilen ≈ 432 + 320 → 2,7 gün" % (KT.SARJOR_ADET, KUTU_N, KT.SARJOR_ADET + KUTU_N),
                            "robot: klape üstü %s → çıkıntı altı %s = %s · K5 topu çıkıntı altında (tutucu r ≤ 32)" % (sayi(KL[3]), sayi(Y_DUZ), sayi(Y_DUZ - KL[3])),
                            "boy uzatma özel sipariş (Sveba / yerli IR) · güç ≈14 kW VARSAYIM",
                            "fırın ≈200 kg düz tabanla %s'e oturur (kiriş üstü %s) → üretici teyidi [V]" % (sayi(Y_DUZ), sayi(SC.TK_Y[1])),
                            "robot kol zarfı kutu (gerçek model yok) · ray önü z %s → çıkıntı +%s: yatay pay %s" % (sayi(RE.RAY_Z[0]), sayi(ZS), sayi(RE.RAY_Z[0] - ZS))), 1):
        isaret(x2 + 15, y, i); txt(x2 + 40, y, s_, f7, INK, "lm"); y += 34
    y = max(y, ya + 60 + 7 * 24) + 20
    txt(x0, y, "kesit ölçüleri föy + çizimden (≈) · boy, oda, ön oda, duvarlar hesap · z kotları DÜNYA (gövde +79 kaymış) · y kotları ALÇAK HAT (v5'ten −168)", f7, GRAY, "lm")
    return TABLO


def baslik():
    txt(FX0, 40, "AUTOKITCH  ·  F FIRIN  ·  TP10 KESİTİ · GÖVDE 1500  ·  79 mm ÖNE  ·  ALÇAK HAT  ·  TEKNİK RESİM v6", f30, INK)
    txt(FX0, 98, "3B model firin_tp10_cad_v7 (tek kaynak) · gövde %s–%s × %s–%s · disk %s → fırın bandı %s → K bandı %s · ürün −170 düz · ısıtılan %s · aynı anda %d ürün · ana makine v57 · ölçüler mm · 27 Eylül 2026"
        % (sayi(X_F0), sayi(X_F1), sayi(YG0), sayi(YG1), sayi(P_SUREC), sayi(BANT_F), sayi(PLAKA_K), sayi(FT.ODA), N_ICERIDE), f11, GRAY)
    d.line([(FX0, 126), (W_PX - 60, 126)], fill=LINE, width=3)


def ortusme(tablo):
    """yazı/balon kutuları birbirine biniyor mu · sayfa dışına taşıyor mu · tablo hücresinden taşan yazı"""
    B = [(x0 + 0.5, y0 + 0.5, x1 - 0.5, y1 - 0.5, s) for x0, y0, x1, y1, s in KAYIT]
    bul = []
    for i in range(len(B)):
        a = B[i]
        if a[0] < 4 or a[1] < 4 or a[2] > W_PX - 4 or a[3] > H_PX - 4:
            bul.append(("SAYFA DIŞI", a[4], None))
        for j in range(i + 1, len(B)):
            b = B[j]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                bul.append(("ÖRTÜŞME", a[4], b[4]))
    x0, y0, x1, y1, kol = tablo
    sinir = [x0 + k for k in kol[1:]] + [x1]
    for a in B:
        if y0 <= a[1] and a[3] <= y1:
            for k0, k1 in zip([x0 + k for k in kol], sinir):
                if k0 <= a[0] < k1 and a[2] > k1 - 4:
                    bul.append(("HÜCRE TAŞIYOR", a[4], None))
    return bul


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    del KAYIT[:]
    baslik(); on(); ust(); yan(); tablo = liste()
    bul = ortusme(tablo)
    print("YAZI ÖRTÜŞME DENETİMİ (%d yazı/balon): %s" % (len(KAYIT), "TEMİZ" if not bul else "%d BULGU" % len(bul)))
    for b in bul:
        print("   ", b)
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "FIRIN_TP10_v6_teknik.png")
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    im.resize((int(W_PX * 0.6), int(H_PX * 0.6)), Image.LANCZOS).save(os.path.join(KLASOR, "..", "..", "otonom", "hat", "img", "FIRIN_TP10_v6_teknik.png"), optimize=True)
    print("yazildi:", yol, im.size)
    return yol


if __name__ == "__main__":
    ciz()
    os._exit(0)
