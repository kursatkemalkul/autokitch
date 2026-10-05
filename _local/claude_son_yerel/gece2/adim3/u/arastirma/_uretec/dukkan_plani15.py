# -*- coding: utf-8 -*-
"""DUKKAN PLANI v15 (28 Eyl 2026): ÖN DÜZLEM +79 (montaj v64) — bütün istasyonlar fırın ön yüzüne (z +79) uzadı, hat derinliği 90,9 düz;
  kırmızı çıkıntı bandı yok · çekmece önleri +79 (açık K1 önü 153,7) · K deterjan rafı yok, bulaşık tablada · ölçüler ön yüzden (ray 28,1 · QR 59,1).
v14 (27 Eyl 2026): ALÇAK HAT (montaj v57 · SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4 · QR_TEZGAH_v4).
  Makine üstü 203 → 186,2; B çekmeceli dolap 0–400 TEK PARÇA (yerden 12,3–78,8), A · C · F onun üstünde; F 79 öne (çıkıntı 8) aynı.
  QR dolabı 86 × 52 × 205 (x 457–543, robot yüzü hat yüzünden 67 = z 670, müşteri yüzü z 1190); ray ekseni z 36 (3D modeldeki 360 —
  v13'teki "koridordan 25" = z 329 kullanılmaz); zincir oluğu ray boyunca, zemin kanalı QR altından oluğa; robot çöpü şeritte (fırın altı);
  personel tezgâhı 60 × 45 ön duvarda (x 395–455); erişim tablosu qr_cad_v1.erisim_tablosu() + store_cad_v6 çekmece kotlarından.
  Yeni: KESİT A–A (x 480) · KESİT B–B (x 435) · QR robot / müşteri tarafı. Ölçüler modüllerden okunur (store_cad_v6, qr_cad_v1,
  ray_ek_cad_v1, tezgah_cad_v1, kesme_cad_v4, kutu_cad_v5, firin_tp10_cad_v7, itici_cad_v4, kaide_cad_v1 — yalnız sabitler, parça kurulmaz).
v13 (27 Eyl 2026): pizza kutusu yedeği TEK YERDE fırın üstü sol (320), dolap pizza gözü boş (UM+ bulaşık yeri).
v12 (27 Eyl 2026): FIRIN 79 mm ÖNE (montaj v51) → F modülü koridora 8 cm çıkıntı (y 96–147), robot koridoru 90 korundu → iç 570 × 271.
v11 (26 Eyl 2026 gece) — Kemal: "en baştaki dükkân ölçüleri hâlâ eski; dükkân bu yeni makineyle genişlemiş olmalı, orayı da hep güncelle".
v10 → v11: HAT 350 → 543 cm (A açıcı 70 · B çekmece 250 altta + C TOPPING 180 üstte · F fırın 150 · K kesme 60 · E kutu 83) → iç genişlik 390 → 570.
Tek FR5 yer rayında x 20–510 (kural 4), QR dolabı koridorun karşısında sağ uçta (457–543). Ölçüler cm.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import store_cad_v8 as SC          # çekmeceli dolap (0–4000 × 788) · çekmece kotları · çöp kovası
import qr_cad_v1 as QR             # QR dolabı + erişim tablosu
import ray_ek_cad_v1 as RE         # ray · zincir oluğu · enerji zinciri · zemin kanalı
import tezgah_cad_v1 as TZ         # personel tezgâhı
import kesme_cad_v6 as KS          # K: taban 892, bant 996, bulaşık tablada (deterjan rafı yok)
import kutu_cad_v7 as KU           # E: tepsi 936, alt raf, içecek yedeği
import firin_tp10_cad_v8 as FT     # F: gövde 788–1305, çıkıntı 79
import itici_cad_v5 as IT          # disk 1000
import kaide_cad_v2 as KD          # A/C kaide 788–892

OUT = os.path.join(os.path.dirname(U), "FULL_MAKINE", "dukkan_plani_v15_on_duzlem.png")
W_PX, H_PX = 3800, 2600
S = 2.6
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT, GRN = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234), (14, 120, 90)
SU, DUV, KOR, CAM, TEZ, AGZ = (214, 236, 250), (200, 200, 205), (235, 241, 250), (200, 225, 250), (250, 238, 220), (253, 244, 243)
SICAK = (255, 232, 220)
RAYC = (205, 222, 244)                      # ray bandı (açık mavi)
ZINC = (40, 40, 44)                         # enerji zinciri


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(50, True)
f7b = F(14, True)
im = Image.new("RGB", (W_PX, H_PX), BG)
d = ImageDraw.Draw(im)


_YAZI = []                                                     # yazı kutuları (--denetle: üst üste binen yazı çiftlerini listeler)


def txt(x, y, s, f=f11, c=INK, a="la"):
    if s:
        _YAZI.append((d.textbbox((x, y), s, font=f, anchor=a), s))
    d.text((x, y), s, font=f, fill=c, anchor=a)


def txtb(x, y, s, f=f11, c=INK, a="la", bg=BG, pad=3):
    """zemini boyalı yazı (altındaki kesik çizgi / erişim yayı yazıyı kesmesin)"""
    b = d.textbbox((x, y), s, font=f, anchor=a)
    d.rectangle([b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad], fill=bg)
    if s:
        _YAZI.append((b, s))
    d.text((x, y), s, font=f, fill=c, anchor=a)


def sayi(v, n=1):
    v = round(v, n)
    return ("%g" % v).replace(".", ",")


def olcu_h(x0, x1, y, s, f=f9, c=INK):
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=f9, c=INK, yon="r"):
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


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


def darc(cx, cy, r, a0, a1, c, w=1, adim=4.0, dolu=2.0):
    a = a0
    while a < a1:
        d.arc([cx - r, cy - r, cx + r, cy + r], a, min(a1, a + dolu), fill=c, width=w)
        a += adim


# ======================= VERI (cm; dünya mm → cm, hat yüzü z 0 → plan y = HAT_D + z/10) =======================
cm = lambda v: v / 10.0
HAT_W, HAT_D = 543.0, cm(SC.DZ)                              # 543 × 83
H_MAK = cm(KS.H)                                             # 186,2 (bütün istasyonların üstü)
H_B = cm(SC.H_B)                                             # 78,8 (çekmeceli dolap üstü = A, C, F altı)
Y_PL = cm(SC.Y_PLINT)                                        # 12,3 plint
KOR_D, DUV_D, ON_D = 90.0, 6.0, 84.0                         # v13 geometrisi (koridor çıkıntıdan ölçülür · ince duvar · ön zon)
IC_W = 570.0
F_CIK = cm(FT.ZS)                                            # 7,9
HAT_ON = HAT_D + F_CIK                                       # 90,9 v15: bütün istasyonların ön yüzü (z +79)
IC_D = HAT_D + F_CIK + KOR_D + DUV_D + ON_D                  # 270,9
MOD = [("A · AÇICI", 0.0, 70.0), ("C · TOPPING", 70.0, 250.0), ("F · FIRIN", 250.0, 400.0), ("K · KESME", 400.0, 460.0), ("E · KUTU", 460.0, 543.0)]
KOLS = ["K1", "K2", "K3", "K4", "K5", "K6", "SERIT"]
KOL_ET = {"K1": "K1 · 6 lahm", "K2": "K2 · 6 lahm", "K3": "K3 · 5 pide", "K4": "K4 Secop·depo", "K5": "K5 · 3 pide + tatlı", "K6": "K6 · 3 içecek", "SERIT": "Ş"}
Y_KOR0, Y_KOR1 = HAT_D + F_CIK, HAT_D + F_CIK + KOR_D        # 90,9 · 180,9
Y_DUV1 = Y_KOR1 + DUV_D                                      # 186,9
pz = lambda z_mm: HAT_D + z_mm / 10.0                        # dünya z (mm) → plan y (cm)
RZ, OMUZ, ERIS_MM = QR.RZ, QR.OMUZ, QR.ERISIM                # 360 · 970 · 779
RAY_Y = pz(RZ)                                               # 119
ERIS = cm(ERIS_MM)                                           # 77,9
RAY_X = (cm(RE.RAY_X[0]), cm(RE.RAY_X[1]))                   # 20 · 510
RAY_B = (pz(RE.RAY_Z[0]), pz(RE.RAY_Z[1]))                   # 107 · 131
OLUK_X, OLUK_B = (cm(RE.OLUK["x"][0]), cm(RE.OLUK["x"][1])), (pz(RE.OLUK["z"][0]), pz(RE.OLUK["z"][1]))   # 20–510 · 131,5–140,5
ZNC_B = (pz(RE.ZC - RE.Z_H["bA"] / 2.0), pz(RE.ZC + RE.Z_H["bA"] / 2.0))                                  # zincir genişliği 49,8–56,2
ZNC_UST = (cm(RE.Y_UST - RE.Z_H["hG"] / 2.0), cm(RE.Y_UST + RE.Z_H["hG"] / 2.0))                           # üst kol 30,2–34,2 yüksek
XF = cm(RE.XF)                                               # 265 sabit uç
X_MIN = cm(RE.x_min_etkin())                                 # 50,8 robotun zincirle gidebildiği en sol
KAN_X, KAN_B = (cm(RE.KANAL["x"][0]), cm(RE.KANAL["x"][1])), (pz(RE.KANAL["z"][0]), pz(RE.KANAL["z"][1]))   # 476–484 · 132–183
KAN_D = cm(RE.KANAL["y"][0])                                 # −6


def zincir_x(xm_cm):
    """robot x (cm) için zincirin planda kapladığı x aralığı: büküm dış kenarı … max(sabit uç, robot)"""
    xc = cm(RE.donus_x(xm_cm * 10.0))
    return xc - cm(RE.Z_H["R"] + RE.Z_H["hG"] / 2.0), xc, max(XF, xm_cm)


QR_X = (cm(QR.X0), cm(QR.X0 + QR.W))                          # 457 · 543
QR_Y = (pz(QR.Z0), pz(QR.Z0 + QR.D))                          # 150 · 202
QR_H = cm(QR.H)                                               # 205
QRX = cm(QR.ROBOT_X)                                          # 500
TZ_X = (cm(TZ.X0), cm(TZ.X0 + TZ.W))                          # 395 · 455
TZ_Y = (pz(TZ.Z0), pz(TZ.Z0 + TZ.D))                          # 225,9 · 270,9
TZ_TAB = (cm(TZ.X0 - TZ.TASMA), cm(TZ.X0 + TZ.W + TZ.TASMA), pz(TZ.Z0 - TZ.TASMA))   # 393,5 · 456,5 · 224,4
TZ_CEK_ON = TZ_Y[0] - cm(TZ.CEKMECE["strok"])                 # 195,9 açık çekmece önü
TZ_KULP = TZ_CEK_ON - cm(TZ.KULP_CIKINTI)                     # 193,6
DUVAR_PAY = TZ_Y[0] - Y_DUV1                                  # 39
KAPI_W = cm(TZ.W - 2 * 1.7)                                   # 59,7 tek kapak
KAPI_ACI = math.degrees(math.asin(min(1.0, DUVAR_PAY / KAPI_W)))   # ≈ 41°
BUL = KS.BULASIK_ZARF
BUL_X, BUL_Y, BUL_H = (cm(BUL["x"][0]) + 400.0, cm(BUL["x"][1]) + 400.0), (pz(BUL["z"][0]), pz(BUL["z"][1])), (cm(BUL["y"][0]), cm(BUL["y"][1]))
KOVA = SC.KOVA
KOVA_X, KOVA_Y, KOVA_H = (cm(KOVA[0]), cm(KOVA[1])), (pz(KOVA[4]), pz(KOVA[5])), (cm(KOVA[2]), cm(KOVA[3]))
IY = KU.ICECEK_YEDEK
ICY_X, ICY_Y = [(cm(a) + 460.0, cm(b) + 460.0) for a, b in KU.ICECEK_X], (pz(IY["z"][0]), pz(IY["z"][1]))
E_KUTU_X = cm(4600.0 + (KU.X_CATAL[0][0] + KU.X_CATAL[-1][1]) / 2.0)                  # 486 kutu çıkışı (çatal ortası)
LAV = (0.0, 30.0, Y_DUV1 + 6.0, Y_DUV1 + 41.0)
KAPI = (0.0, 75.0)
TEZ_ = (75.0, 215.0, IC_D - 30.0, IC_D)
PEN = (80.0, 210.0)
MINI = (215.0, 295.0, IC_D - 40.0, IC_D)
BEK = (295.0, TZ_X[0])                                        # v13: 295–457 → tezgâh 395'te başlar
NIS_DUV = (QR_X[0] - 6.0, QR_X[0])                           # v13 niş yan duvarı 451–457
KES_A, KES_B = 480.0, 435.0                                  # kesit düzlemleri (x cm): A–A zemin kanalı + QR · B–B tezgâh + bulaşık
OX, OY = 140.0, 330.0


def X(x):
    return OX + x * S


def Y(y):
    return OY + y * S


# ======================= ERİŞİM HESABI (mm) =======================
KAIDE_PAY = 95.0                              # robot tabanı ±90 + 5 (denetle_yeni · denetci_zincir_cekmece)
ZINCIR_CARPAR = {"CEK_K1_lahm_1", "CEK_K1_lahm_2"}          # denetci_zincir_cekmece: sağdan zincir çarpar, solda robot duramaz
ZINCIR_SAGDAN = {"CEK_K2_lahm_1", "CEK_K2_lahm_2", "CEK_K3_hamur_2", "CEK_K5_hamur_2", "CEK_K6_ic1_1"}   # yalnız soldan


def icerik(kol, kod, tip, x0, yo):
    """açık çekmecede robotun aldığı ürünlerin taban noktaları (x, y, z) · store_cad_v6.cekmece() ile aynı yerleşim"""
    wo = SC.GEN(kol); x1 = x0 + wo; xc = x0 + wo / 2.0
    Z_TUB1 = SC.Z_CON0 - 2.0; Z_TUB0 = Z_TUB1 - SC.TUB[tip]
    ka, kb, kc = x0 + SC.KUTU_KENAR, x1 - SC.KUTU_KENAR, yo + SC.KC
    if tip in SC.TOP:
        t = SC.TOP[tip]
        tz0 = Z_TUB0 + 5.0; Zc = tz0 + t["td"] / 2.0
        pts = [(xc + (i - (t["nx"] - 1) / 2.0) * t["ax"], yo + SC.Y_OTUR, Zc + (j - (t["nz"] - 1) / 2.0) * t["az"])
               for i in range(t["nx"]) for j in range(t["nz"])]
    else:                                                     # şeritli (içecek / tatlı): itici ürünü öne dayar, robot öndekini alır
        tat = tip == "tatli"
        r = SC.TATLI["r"] if tat else SC.ICECEK["r"]; px_ = SC.TATLI["ax"] if tat else SC.ICECEK["ax"]
        ix0, ix1, iz1 = ka + 3.0, kb - 3.0, Z_TUB1 - 13.0
        nx = int((ix1 - ix0 - 12.0 - 2 * r) // px_) + 1
        if tat:
            nx = min(nx, SC.TATLI["nx"])
        xm = (ix0 + ix1) / 2.0
        pts = [(xm + (i - (nx - 1) / 2.0) * px_, kc + 1.0, iz1 - 3.0 - r) for i in range(nx)]
    return [(a, y, z + SC.STROK) for a, y, z in pts]


def mesafe(rx, p):
    return math.sqrt((p[0] - rx) ** 2 + (p[1] + QR.BILEK_PAY - OMUZ) ** 2 + (p[2] - RZ) ** 2)


XMIN_MM = RE.x_min_etkin()
CEK_SONUC = {}                                               # kod → (kol, sıra, taban cm, n, N, robot x, max, min, durum)
_sira = {}
for kol, kod, tip, x0, yo in SC.CEK:
    _sira[kol] = _sira.get(kol, 0) + 1
    pts = icerik(kol, kod, tip, x0, yo)
    pa, pb = SC.KAPAK_X[kol]
    yanlar = []
    if pa - KAIDE_PAY >= XMIN_MM:
        yanlar.append(pa - KAIDE_PAY)
    if kod not in ZINCIR_SAGDAN and kod not in ZINCIR_CARPAR:
        yanlar.append(pb + KAIDE_PAY)
    en = None
    for rx in yanlar:
        ds = [mesafe(rx, p) for p in pts]
        n = sum(1 for v in ds if v <= ERIS_MM)
        if en is None or n > en[0]:
            en = (n, rx, max(ds), min(ds), max(zip(ds, pts))[1])
    durum = "zincir" if not yanlar else ("OK" if en[0] == len(pts) else "kısmen")
    CEK_SONUC[kod] = (kol, _sira[kol], tip, cm(pts[0][1]), en[0] if en else 0, len(pts), cm(en[1]) if en else None,
                      cm(en[2]) if en else None, cm(en[3]) if en else None, durum, en[4] if en else None)
QR_ET = QR.erisim_tablosu()                                  # (satır, sütun, gx, göz tabanı, bilek y, mesafe mm)
# açıcı tablası (pafta v16 robot_kesit D1: bilek z = ürün ekseni −170 + 232,5, y = disk + 100) · robot zincir sınırında
D1_B = (350.0, IT.DISK_UST + 100.0, FT.ZT + 232.5)
D1_R = XMIN_MM
D1 = math.sqrt((D1_B[0] - D1_R) ** 2 + (D1_B[1] - OMUZ) ** 2 + (D1_B[2] - RZ) ** 2)
# E kutu tepsisi (pafta v16 kesit_E D2: bilek z 230, y = tepsi − 9 + 20) · robot kutu çıkışı hizasında
D2_B = (E_KUTU_X * 10.0, KU.TEPSI - 9.0 + 20.0, 230.0)
D2 = math.sqrt((D2_B[1] - OMUZ) ** 2 + (D2_B[2] - RZ) ** 2)

# ======================= BASLIK =======================
txt(OX, 60, "AUTOKITCH  ·  DÜKKÂN v15 · ÖN DÜZLEM · HAT 543 × 90,9 × 186  ·  B dolap altta  ·  FR5 rayda 20–510  ·  QR 86 × 52 × 205  ·  iç 570 × 271", f38, INK)
txt(OX, 122, "v14'e göre (montaj v64): bütün istasyonların ön yüzü fırın ön yüzüyle aynı düzlemde (z +79), arka yüz yerinde → hat 90,9 derin, çıkıntı yok; çekmece önleri +79; K deterjan rafı yok; "
             "ön yüzden: ray ekseni 28,1 · QR robot yüzü 59,1; dükkân iç ölçüsü aynı (570 × 271) · ölçüler cm · 28 Eylül 2026", f13, GRAY)
d.line([(OX, 160), (W_PX - 140, 160)], fill=LINE, width=3)

# ======================= PLAN =======================
txt(OX, OY - 138, "PLAN (üstten) · raylı · alçak hat", f16, ACC)
d.rectangle([X(-12), Y(-12), X(IC_W + 12), Y(IC_D)], fill=DUV, outline=LINE, width=3)
d.rectangle([X(0), Y(0), X(IC_W), Y(IC_D)], fill=BG, outline=LINE, width=3)
# koridor
d.rectangle([X(0), Y(Y_KOR0), X(IC_W), Y(Y_KOR1)], fill=KOR, outline=None)
# modüller (üstten görünen: A, C, F dolabın üstünde; K, E yerden)
for ad, x0, x1 in MOD:
    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_ON)], fill=SICAK if ad.startswith("F") else FILL, outline=LINE, width=3)
# B çekmeceli dolap (altta, kesik) · kolonlar
for k in KOLS[:-1]:                                           # şerit: robot çöpü kutusu (aşağıda) gösterir
    a, b = SC.KAPAK_X[k]
    drect(X(cm(a)), Y(HAT_ON - 20), X(cm(b)), Y(HAT_ON), GRN, 1)
    txt(X((cm(a) + cm(b)) / 2), Y(HAT_ON - 8), KOL_ET[k], f7, GRN, "mm")
d.rectangle([X(253), Y(40), X(378), Y(51)], fill=BG, outline=RED, width=1)
txt(X(315.5), Y(45.5), "fırın üstü: kutu yedeği 320 · kompresör", f7, RED, "mm")
# K altı: bulaşık (tablada) · F altı şerit: robot çöpü · E altı: içecek yedeği
drect(X(BUL_X[0]), Y(BUL_Y[0]), X(BUL_X[1]), Y(BUL_Y[1]), ACC, 1)
txtb(X((BUL_X[0] + BUL_X[1]) / 2), Y(44), "bulaşık", f7, ACC, "mm", FILL, 1); txtb(X((BUL_X[0] + BUL_X[1]) / 2), Y(51), "(altta)", f7, ACC, "mm", FILL, 1)
drect(X(KOVA_X[0]), Y(KOVA_Y[0]), X(KOVA_X[1]), Y(KOVA_Y[1]), RED, 2)
txt(X((KOVA_X[0] + KOVA_X[1]) / 2), Y(58), "çöp", f7, RED, "mm")
for a, b in ICY_X:
    drect(X(a), Y(ICY_Y[0]), X(b), Y(ICY_Y[1]), GRN, 1)
txtb(X(501.5), Y(56), "içecek yedeği 6 koli", f7, GRN, "mm", FILL, 2)
for ad, x0, x1 in MOD:
    bg_ = SICAK if ad[0] == "F" else FILL
    txtb(X((x0 + x1) / 2), Y(20), ad, f9 if x1 - x0 < 100 else f11, INK, "mm", bg_, 2)
    alt = {"A": "70 × 90,9 · dolap üstünde", "C": "180 × 90,9 · dolap üstünde (kaide %s)" % sayi(cm(KD.KAIDE_H)), "F": "150 × 90,9 · dolap üstünde",
           "K": "60 × 90,9", "E": "83 × 90,9"}[ad[0]]
    txtb(X((x0 + x1) / 2), Y(30), alt, f7, GRAY, "mm", bg_, 2)
# (denetçi) "B · ÇEKMECELİ DOLAP", "ZİNCİR OLUĞU" ve "ZEMİN KANALI" yazıları erişim daireleri yapıştırıldıktan SONRA yazılır (daireler yazıyı kesiyordu)
# ray + zincir oluğu + zemin kanalı
d.rectangle([X(RAY_X[0]), Y(RAY_B[0]), X(RAY_X[1]), Y(RAY_B[1])], fill=RAYC, outline=ACC, width=2)
dline((X(RAY_X[0]), Y(RAY_Y)), (X(RAY_X[1]), Y(RAY_Y)), ACC, 1, 14, 6)
txtb(X(300), Y(RAY_B[0] + 5), "YER RAYI x %s–%s · eksen z %s (hat yüzünden)" % (sayi(RAY_X[0]), sayi(RAY_X[1]), sayi(cm(RZ))), f8, ACC, "mm", RAYC, 2)
d.rectangle([X(OLUK_X[0]), Y(OLUK_B[0]), X(OLUK_X[1]), Y(OLUK_B[1])], fill=SOFT, outline=ACC, width=1)
for xx in KAN_X:
    dline((X(xx), Y(OLUK_B[1])), (X(xx), Y(KAN_B[1])), ACC, 2, 9, 5)
dline((X(KAN_X[0]), Y(KAN_B[1])), (X(KAN_X[1]), Y(KAN_B[1])), ACC, 2, 9, 5)
# açık K1 + robot K1'in sağında + zincir (robot bu konumdayken)
K1a, K1b = cm(SC.KAPAK_X["K1"][0]), cm(SC.KAPAK_X["K1"][1])
AC_ON = HAT_ON + cm(SC.STROK)                                 # 153,7 açık çekmece önü (v15: çekmece önü +79)
d.rectangle([X(K1a), Y(HAT_ON), X(K1b), Y(AC_ON)], fill=(235, 250, 242), outline=GRN, width=2)
txtb(X(K1b / 2), Y(HAT_ON + 10), "K1 AÇIK · %s" % sayi(cm(SC.STROK)), f8, GRN, "mm", (235, 250, 242), 2)
RX1 = cm(SC.KAPAK_X["K1"][1] + KAIDE_PAY)                     # 79,4
zx0, zxc, zx1 = zincir_x(RX1)
d.rectangle([X(zx0), Y(ZNC_B[0]), X(zx1), Y(ZNC_B[1])], fill=ZINC)
d.ellipse([X(XF) - 7, Y((ZNC_B[0] + ZNC_B[1]) / 2) - 7, X(XF) + 7, Y((ZNC_B[0] + ZNC_B[1]) / 2) + 7], fill=BG, outline=ZINC, width=3)
txt(X(XF), Y(OLUK_B[1] + 4), "zincir sabit ucu x 265", f7, ZINC, "ma")
d.rectangle([X(zx0), Y(ZNC_B[0]) - 3, X(K1b), Y(ZNC_B[1]) + 3], outline=RED, width=3)
d.rectangle([X(RX1 - cm(KAIDE_PAY - 5.0)), Y(RAY_B[0]), X(RX1 + cm(KAIDE_PAY - 5.0)), Y(RAY_B[1])], fill=SOFT, outline=ACC, width=2)   # taban ±9 (açık K1'e 0,5 kalır)
d.ellipse([X(RX1) - 9 * S, Y(RAY_Y) - 9 * S, X(RX1) + 9 * S, Y(RAY_Y) + 9 * S], fill=BG, outline=ACC, width=3)
# erişim daireleri (iç mekâna kırpılı)
lay = Image.new("RGBA", (W_PX, H_PX), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
a = 0.0
while a < 360.0:
    ld.arc([X(RX1) - ERIS * S, Y(RAY_Y) - ERIS * S, X(RX1) + ERIS * S, Y(RAY_Y) + ERIS * S], a, min(360.0, a + 2.0), fill=ACC + (255,), width=2)
    a += 4.0
a = 0.0
while a < 360.0:
    ld.arc([X(QRX) - ERIS * S, Y(RAY_Y) - ERIS * S, X(QRX) + ERIS * S, Y(RAY_Y) + ERIS * S], a, min(360.0, a + 2.0), fill=(150, 150, 160, 255), width=1)
    a += 5.0
box = (int(X(0)) + 2, int(Y(0)) + 2, int(X(IC_W)) - 2, int(Y(IC_D)) - 2)
im.paste(lay.crop(box), box[:2], lay.crop(box)); d = ImageDraw.Draw(im)
txtb(X(160), Y(51), "B · ÇEKMECELİ DOLAP 0–400 (altta) · yerden 12,3–78,8", f7, GRN, "mm", FILL, 2)
txtb(X(390), Y((OLUK_B[0] + OLUK_B[1]) / 2), "ZİNCİR OLUĞU %s–%s · z %s–%s" % (sayi(OLUK_X[0]), sayi(OLUK_X[1]), sayi(OLUK_B[0] - HAT_D), sayi(OLUK_B[1] - HAT_D)),
     f7, ACC, "mm", SOFT, 1)
txtb(X(KAN_X[0]) - 12, Y(147), "ZEMİN KANALI %s (zeminde) → QR altı" % sayi(KAN_X[1] - KAN_X[0]), f7, ACC, "rm", KOR, 2)
for px_ in (E_KUTU_X, QRX):
    d.ellipse([X(px_) - 6, Y(RAY_Y) - 6, X(px_) + 6, Y(RAY_Y) + 6], fill=(150, 150, 160))
txtb(X(E_KUTU_X) - 4, Y(RAY_B[0] - 5), "E kutu x 486", f7, GRAY, "rm", KOR, 2)
txtb(X(QRX) + 4, Y(RAY_B[0] - 5), "QR x 500", f7, GRAY, "lm", KOR, 2)
txtb(X(RX1) + 30, Y(152), "FR5 · x %s (K1 yanında)" % sayi(RX1, 0), f8, ACC, "lm", KOR, 2)
txtb(X(RX1) + 30, Y(160), "zincir dönüşü açık K1'in altında (kırmızı) · 1.–2. çekmece çarpar", f7, RED, "lm", KOR, 2)
txtb(X(RX1) + 30, Y(169), "mavi daire: FR5 pratik erişim %s · gri: QR önünde (x %s)" % (sayi(ERIS), sayi(QRX)), f7, ACC, "lm", KOR, 2)
# QR önü göz çizgileri + ROBOT KORİDORU etiketi
for gx in (cm(QR.X0 + QR.GOZ_X[0] + QR.GOZ_W / 2), cm(QR.X0 + QR.GOZ_X[1] + QR.GOZ_W / 2)):
    dline((X(QRX), Y(RAY_Y)), (X(gx), Y(QR_Y[0])), GRN, 2, 8, 5)
txtb(X(175), Y(99), "ROBOT KORİDORU 90", f9, ACC, "mm", KOR, 2)
# ince duvar + hücre kapısı
d.rectangle([X(0), Y(Y_KOR1), X(QR_X[0]), Y(Y_DUV1)], fill=DUV, outline=LINE, width=1)
d.rectangle([X(40), Y(Y_KOR1 - 1), X(110), Y(Y_DUV1 + 1)], fill=AGZ, outline=RED, width=2)
txtb(X(75), Y(Y_DUV1 + 8), "HÜCRE KAPISI 70", f7, RED, "mm", BG, 2)
# cephe nişi + niş yan duvarı
d.rectangle([X(QR_X[0]), Y(QR_Y[1]), X(IC_W), Y(IC_D)], fill=(236, 236, 240), outline=LINE, width=2)
txt(X(513), Y(QR_Y[1] + 24), "CEPHE NİŞİ 113 × 69", f8, GRAY, "mm"); txt(X(513), Y(QR_Y[1] + 36), "müşteri buradan alır", f7, GRAY, "mm")
txt(X(513), Y(QR_Y[1] + 46), "panel 166–177 (dolap yüzünde)", f7, GRAY, "mm")
d.rectangle([X(NIS_DUV[0]), Y(Y_KOR1), X(NIS_DUV[1]), Y(IC_D)], fill=DUV, outline=LINE, width=1)
# ön zon (v13)
txt(X(175), Y(Y_DUV1 + 14), "ELEMAN GEÇİDİ 54", f8, GRAY, "mm")
d.rectangle([X(TEZ_[0]), Y(TEZ_[2]), X(TEZ_[1]), Y(TEZ_[3])], fill=TEZ, outline=INK, width=2)
txt(X(145), Y(TEZ_[2] + 15), "TEZGÂH 140 × 30 · sürme cam 130", f8, INK, "mm")
d.rectangle([X(PEN[0]), Y(IC_D - 4), X(PEN[1]), Y(IC_D + 2)], fill=CAM, outline=ACC, width=1)
d.rectangle([X(MINI[0]), Y(MINI[2]), X(MINI[1]), Y(MINI[3])], fill=TEZ, outline=INK, width=2)
d.rectangle([X(255), Y(MINI[2] + 2), X(293), Y(MINI[3] - 2)], fill=SU, outline=ACC, width=1)
txt(X(235), Y(MINI[2] + 14), "DOLDURMA", f7, INK, "mm"); txt(X(274), Y(MINI[2] + 14), "EVYE", f7, ACC, "mm")
drect(X(BEK[0] + 6), Y(Y_DUV1 + 30), X(BEK[1] - 6), Y(IC_D - 6), GRAY, 1)
txt(X((BEK[0] + BEK[1]) / 2), Y(Y_DUV1 + 48), "BEKLEME · MENÜ", f8, GRAY, "mm"); txt(X((BEK[0] + BEK[1]) / 2), Y(Y_DUV1 + 60), "EKRANI %s × 78" % sayi(BEK[1] - BEK[0]), f8, GRAY, "mm")
# personel tezgâhı: tabla + gövde + tek kapak (~41°) + çekmece (strok 30) + duvar askısı
d.rectangle([X(TZ_TAB[0]), Y(TZ_TAB[2]), X(TZ_TAB[1]), Y(TZ_Y[1])], fill=TEZ, outline=GRAY, width=1)
d.rectangle([X(TZ_X[0]), Y(TZ_Y[0]), X(TZ_X[1]), Y(TZ_Y[1])], fill=TEZ, outline=INK, width=2)
d.rectangle([X(NIS_DUV[0]), Y(TZ_TAB[2]), X(TZ_TAB[1]), Y(IC_D)], outline=RED, width=3)
txt(X((TZ_X[0] + TZ_X[1]) / 2 - 2), Y(TZ_Y[0] + 12), "TEZGÂH (personel)", f7b, INK, "mm")
txt(X((TZ_X[0] + TZ_X[1]) / 2 - 2), Y(TZ_Y[0] + 20), "60 × 45 × 90", f7, INK, "mm")
txt(X((TZ_X[0] + TZ_X[1]) / 2 - 2), Y(TZ_Y[0] + 28), "askı 165 duvarda", f7, GRAY, "mm")
txt(X((TZ_X[0] + TZ_X[1]) / 2 - 2), Y(TZ_Y[0] + 38), "çakışma: niş duvarı", f7, RED, "mm")
drect(X(TZ_X[0] + 0.2), Y(TZ_KULP), X(TZ_X[1] - 0.2), Y(TZ_Y[0]), INK, 1)
txt(X(436), Y(205), "çekmece", f7, INK, "mm"); txt(X(436), Y(212), "strok %s" % sayi(cm(TZ.CEKMECE["strok"])), f7, INK, "mm")
hx, hy = X(TZ_X[0] + 0.2), Y(TZ_Y[0])
darc(hx, hy, KAPI_W * S, 360.0 - KAPI_ACI, 360.0, INK, 1, 5.0, 2.5)
d.line([(hx, hy), (hx + KAPI_W * S * math.cos(math.radians(KAPI_ACI)), hy - KAPI_W * S * math.sin(math.radians(KAPI_ACI)))], fill=INK, width=2)
olcu_v(X(TZ_X[0]) - 18, Y(Y_DUV1), Y(TZ_Y[0]), sayi(DUVAR_PAY), f8, INK, "l")
txt(X(430), Y(219.3), "kapak %d°" % round(KAPI_ACI), f7, INK, "mm")      # (denetçi) kapak açısı süpürme kamasının içinde — bekleme kutusunun içinden çıkarıldı
# QR dolabı
d.rectangle([X(QR_X[0]), Y(QR_Y[0]), X(QR_X[1]), Y(QR_Y[1])], fill=FILL, outline=INK, width=3)
txt(X(500), Y(QR_Y[0] + 12), "QR DOLABI 86 × 52 × 205", f8, INK, "mm")
txt(X(500), Y(QR_Y[0] + 23), "12 göz 2 × 6", f7, GRAY, "mm")
txt(X(500), Y(QR_Y[0] + 32), "robot yüzü ön yüzden %s" % sayi(QR_Y[0] - HAT_ON), f7, GRAY, "mm")
txt(X(500), Y(QR_Y[0] + 41), "müşteri yüzü z 119", f7, GRAY, "mm")
# el lavabosu, kapı, sokak
d.rectangle([X(LAV[0]), Y(LAV[2]), X(LAV[1]), Y(LAV[3])], fill=SU, outline=ACC, width=1)
txt(X(40), Y(LAV[2] + 12), "EL LAVABOSU", f7, ACC, "la")
d.rectangle([X(KAPI[0]), Y(IC_D - 2), X(KAPI[1]), Y(IC_D + 12)], fill=BG, outline=INK, width=2)
txt(X(37), Y(IC_D + 24), "KAPI 75 · dışa açılır", f7, INK, "mm")
txt(X(IC_W / 2), Y(IC_D) + 50, "KALDIRIM / SOKAK", f9, GRAY, "mm")
# kesit işaretleri (cephe altında)
for xk, ad in ((KES_A, "A"), (KES_B, "B")):
    xs = X(xk)
    d.line([(xs, Y(IC_D) + 16), (xs, Y(IC_D) + 40)], fill=INK, width=4)
    d.polygon([(xs + 26, Y(IC_D) + 28), (xs + 6, Y(IC_D) + 21), (xs + 6, Y(IC_D) + 35)], fill=INK)     # bakış +x yönünde
    txt(xs + 32, Y(IC_D) + 28, ad, f9, INK, "lm")
# ölçüler
olcu_v(X(IC_W) + 40, Y(0), Y(HAT_ON), "hat %s" % sayi(HAT_ON), f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR0), Y(Y_KOR1), "robot 90", f8, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_KOR1), Y(Y_DUV1), "6", f7, INK, "r")
olcu_v(X(IC_W) + 40, Y(Y_DUV1), Y(IC_D), "ön 84", f8, INK, "r")
olcu_v(X(IC_W) + 120, Y(0), Y(IC_D), sayi(IC_D), f11, INK, "r")
olcu_v(X(0) - 40, Y(HAT_ON), Y(RAY_Y), "ray %s" % sayi(RAY_Y - HAT_ON), f7, INK, "l")
olcu_v(X(0) - 40, Y(RAY_Y), Y(RAY_Y + 0.001), "", f7, INK, "l")
olcu_v(X(556.5), Y(HAT_ON), Y(QR_Y[0]), sayi(QR_Y[0] - HAT_ON), f8, INK, "l")
yb = Y(IC_D) + 90
for x0, x1, s_ in ((0, 75, "kapı 75"), (75, 215, "tezgâh 140"), (215, 295, "servis 80"), (295, TZ_X[0], "bekleme %s" % sayi(BEK[1] - BEK[0])),
                   (TZ_X[0], TZ_X[1], "tezgâh 60"), (TZ_X[1], QR_X[0], ""), (QR_X[0], QR_X[1], "QR 86"), (QR_X[1], IC_W, "27")):
    olcu_h(X(x0), X(x1), yb, s_, f8, INK)
txt(X((TZ_X[1] + QR_X[0]) / 2), yb - 16, "2", f7, INK, "md")
olcu_h(X(0), X(IC_W), yb + 40, sayi(IC_W), f11, INK)
olcu_h(X(0), X(HAT_W), Y(0) - 30, "HAT %s" % sayi(HAT_W), f9, INK)
for x0, x1 in ((0, 70), (70, 250), (250, 400), (400, 460), (460, 543)):
    olcu_h(X(x0), X(x1), Y(0) - 62, sayi(x1 - x0), f7, GRAY)
olcu_h(X(0), X(400), Y(0) - 94, "B dolap 400 (altta)", f7, GRN)

# ======================= CEKMECE DIZISI (3 kare) =======================
DX0, DY0 = OX, Y(IC_D) + 220
txt(DX0, DY0 - 50, "ÇEKMECE DİZİSİ · K1 (plan, x 1 cm = 2 px, derinlik yarı ölçek)", f16, ACC)
s2 = 2.0
KW = 250 * s2 + 60


def kare(i, baslik, robot_x, acik, ok_txt, uyari=""):
    x0 = DX0 + i * (KW + 40)
    y0 = DY0
    d.rectangle([x0, y0, x0 + KW, y0 + 250], fill=BG, outline=LINE, width=2)
    txt(x0 + 10, y0 + 12, baslik, f9, INK)
    bx = x0 + 30; by = y0 + 40
    def px(x): return bx + x * s2
    def py(z): return by + z * s2
    d.rectangle([px(0), py(0), px(250), py(HAT_D * 0.5)], fill=FILL, outline=LINE, width=2)
    for k in ("K1", "K2", "K3", "K4"):
        a_, b_ = cm(SC.KAPAK_X[k][0]), min(250.0, cm(SC.KAPAK_X[k][1]))
        d.rectangle([px(a_), py(10), px(b_), py(HAT_D * 0.5)], fill=BG, outline=GRN, width=1)
    if acik:
        d.rectangle([px(K1a), py(HAT_D * 0.5), px(K1b), py(HAT_D * 0.5 + cm(SC.STROK) * 0.5)], fill=(235, 250, 242), outline=GRN, width=2)
        txt(px(K1b / 2), py(HAT_D * 0.5 + 8), "K1 açık %s" % sayi(cm(SC.STROK)), f7, GRN, "mm")
    ry = HAT_D * 0.5 + 18.0                                            # ray ekseni z 36 → yarı ölçek
    d.rectangle([px(RAY_X[0]), py(ry - 6), px(250), py(ry + 6)], fill=RAYC, outline=ACC, width=1)
    oy = HAT_D * 0.5 + (OLUK_B[0] + OLUK_B[1] - 2 * HAT_D) * 0.25    # oluk ortası (yarı ölçek)
    zx0_, zxc_, zx1_ = zincir_x(robot_x)
    d.rectangle([px(zx0_), py(oy) - 3, px(min(250.0, zx1_)), py(oy) + 3], fill=ZINC)
    if acik and zx0_ < K1b:
        d.rectangle([px(zx0_), py(oy) - 7, px(K1b), py(oy) + 7], outline=RED, width=2)
    d.ellipse([px(robot_x) - 15, py(ry) - 15, px(robot_x) + 15, py(ry) + 15], fill=BG, outline=ACC, width=3)
    txt(px(robot_x) + 20, py(ry), "FR5 x %s" % sayi(robot_x), f7, ACC, "lm")
    txt(x0 + 10, y0 + 204, ok_txt, f8, GRAY)
    if uyari:
        txt(x0 + 10, y0 + 226, uyari, f8, RED)


D_UST = CEK_SONUC["CEK_K1_lahm_6"]
D_3 = CEK_SONUC["CEK_K1_lahm_3"]
kare(0, "1 · robot K1 önünde, çekmece kapalı", X_MIN, False, "x %s = zincirle gidebildiği en sol (büküm oluk ucunda)" % sayi(X_MIN))
kare(1, "2 · robot K1'in sağına (x %s), K1 açılır, yandan alır" % sayi(RX1, 0), RX1, True, "6. çekmece %d/%d · 3. çekmece %d/%d top erişilir" % (D_UST[4], D_UST[5], D_3[4], D_3[5]),
     "zincir dönüşü açık K1'in altında → 1.–2. çekmece ÇARPAR")
kare(2, "3 · çekmece kapanır, robot açıcıya döner", X_MIN, False, "açıcı tablası (disk %s) bilek %s / %s %s" % (sayi(cm(IT.DISK_UST)), sayi(cm(D1)), sayi(ERIS), "OK" if D1 <= ERIS_MM else "YOK"))

# ======================= ERİŞİM TABLOSU + ÇEKMECE MATRİSİ (sağ panel) =======================
PX0 = X(IC_W) + 260
PW = W_PX - 140 - PX0
d.rectangle([PX0, OY - 60, PX0 + PW, OY + 840], fill=BG, outline=LINE, width=3)
txt(PX0 + 30, OY - 20, "FR5 RAYDA — ERİŞİM KONTROLÜ (omuz %s, ray ekseni z %s, pratik %s) · v15" % (sayi(cm(OMUZ)), sayi(cm(RZ)), sayi(ERIS)), f16, INK)
txt(PX0 + 30, OY + 18, "bilek hedefi: QR ve çekmecede ürün tabanı + 10 (VARSAYIM, qr_cad_v1) · açıcı ve E tepsisi pafta v16 D1 / D2 gibi", f8, GRAY)
TAB = [("Hedef", "robot x", "dx", "dy", "dz", "mesafe", "FR5 %s" % sayi(ERIS))]
TAB.append(("Açıcı tablası (disk 100 · bilek z +6)", sayi(cm(D1_R)), sayi(cm(abs(D1_B[0] - D1_R))), sayi(cm(D1_B[1] - OMUZ)), sayi(cm(abs(D1_B[2] - RZ))), sayi(cm(D1), 1), "OK" if D1 <= ERIS_MM else "YOK"))
TAB.append(("E kutu tepsisi (%s)" % sayi(cm(KU.TEPSI)), sayi(E_KUTU_X), "0", sayi(cm(D2_B[1] - OMUZ)), sayi(cm(abs(D2_B[2] - RZ))), sayi(cm(D2), 1), "OK" if D2 <= ERIS_MM else "YOK"))
for r, et in ((0, "QR alt göz (taban 45)"), (2, "QR orta göz (taban 85)"), (5, "QR üst göz (taban 145)")):
    sat = [s_ for s_ in QR_ET if s_[0] == r]
    enk = max(sat, key=lambda s_: s_[5])
    TAB.append((et, sayi(QRX), sayi(cm(abs(enk[2] - QR.ROBOT_X))), sayi(cm(enk[4] - OMUZ)), sayi(cm(QR.Z0 - RZ)), sayi(cm(enk[5]), 1), "OK" if enk[5] <= ERIS_MM else "YOK"))
for kod, et in (("CEK_K1_lahm_6", "K1 lahm 6. (üst · taban %s) en uzak top"), ("CEK_K1_lahm_3", "K1 lahm 3. (taban %s) en uzak top"),
                ("CEK_K2_lahm_1", "K2 lahm 1. (alt · taban %s) en uzak top"), ("CEK_K3_hamur_1", "K3 pide 1. (alt · taban %s) en uzak top")):
    c = CEK_SONUC[kod]; p = c[10]
    TAB.append((et % sayi(c[3]), sayi(c[6]), sayi(cm(abs(p[0] - c[6] * 10))), sayi(cm(p[1] + QR.BILEK_PAY - OMUZ)), sayi(cm(abs(p[2] - RZ))), sayi(c[7], 1),
                "OK" if c[4] == c[5] else "YOK · %d/%d" % (c[4], c[5])))
TAB.append(("Fırın · kesme: robot DOKUNMAZ (konveyör + itici)", "—", "—", "—", "—", "—", "—"))
yy = OY + 62
cols = (0, 500, 610, 690, 775, 860, 960)
for i, row in enumerate(TAB):
    for cx_, s_ in zip(cols, row):
        c_ = INK
        if i and s_.startswith("OK"):
            c_ = GRN
        if i and s_.startswith("YOK"):
            c_ = RED
        txt(PX0 + 30 + cx_, yy, s_, f9 if i else f8, c_ if i else GRAY)
    yy += 32
    if i == 0:
        d.line([(PX0 + 30, yy - 8), (PX0 + 1110, yy - 8)], fill=SOFT, width=2)
d.line([(PX0 + 30, yy - 4), (PX0 + 1110, yy - 4)], fill=SOFT, width=2)
# çekmece matrisi
MX0, MY0 = PX0 + 1160, OY + 62
LW = 96
txt(MX0, MY0 - 44, "ÇEKMECE ERİŞİMİ · açık %s · robot yanda" % sayi(cm(SC.STROK)), f9, INK)
txt(MX0, MY0 - 16, "erişilen / toplam (alttan 1 → 6) · kot = ürün tabanı", f7, GRAY)
CW, RH = 76, 50
for j in range(6):
    txt(MX0 + LW + j * CW + CW / 2, MY0 + 12, "%d." % (j + 1), f8, GRAY, "mm")
sat_k = [("K1", "lahmacun"), ("K2", "lahmacun"), ("K3", "pide"), ("K5", "pide + tatlı"), ("K6", "içecek")]
for r_, (kol, tur) in enumerate(sat_k):
    y0 = MY0 + 30 + r_ * RH
    txt(MX0, y0 + RH / 2 - 8, kol, f9, INK, "lm"); txt(MX0, y0 + RH / 2 + 10, tur, f7, GRAY, "lm")
    hucre = [v for k_, v in CEK_SONUC.items() if v[0] == kol]
    hucre.sort(key=lambda v: v[1])
    for v in hucre:
        j = v[1] - 1
        x0 = MX0 + LW + j * CW
        dur = v[9]
        fc = (232, 246, 238) if dur == "OK" else ((252, 232, 230) if dur == "zincir" else (255, 244, 222))
        d.rectangle([x0 + 2, y0 + 2, x0 + CW - 2, y0 + RH - 2], fill=fc, outline=SOFT, width=1)
        txt(x0 + CW / 2, y0 + 14, sayi(v[3]), f7, GRAY, "mm")
        s_ = "zincir" if dur == "zincir" else "%d/%d" % (v[4], v[5])
        txt(x0 + CW / 2, y0 + 33, s_, f8, GRN if dur == "OK" else RED, "mm")
yy = max(yy, MY0 + 30 + len(sat_k) * RH) + 20
txt(MX0, MY0 + 30 + len(sat_k) * RH + 10, "robot çekmecenin yanında (taban payı 9,5) · K1 yalnız sağdan (x 79)", f7, GRAY)
txt(MX0, MY0 + 30 + len(sat_k) * RH + 28, "içecek / tatlı: şeritte öndeki ürün (itici öne dayar)", f7, GRAY)
KARAR = [
    "HAT 543 × 90,9 × 186 (montaj v64 · ön düzlem +79, arka yüz yerinde): B çekmeceli dolap 0–400 tek parça, yerden 12,3–78,8 (24 çekmece + K4 Secop/depo + şerit) ·",
    "  A açıcı 70 + C TOPPING 180 + F fırın 150 dolabın üstünde (A/C kaide 10,4, disk 100) · K 60 · E 83 yerden. Çıkıntı yok: her istasyon ön yüzü fırınla aynı düzlemde, kapaklı temiz kutu.",
    "  F altı: K5, K6 + şeritte robot çöpü 15 L · K altı: bulaşık MEIKO ayaksız tablada, önünde K alt kapağı · E altı: içecek yedeği 6 koli.",
    "DÜKKÂN: iç 570 × 271 aynı (hat 90,9 + koridor 90 + ince duvar 6 + ön zon 84). Ray ekseni z 36 = ön yüzden 28,1 (3D model).",
    "ROBOT: tek FR5 yer rayında x 20–510, omuz 97, pratik 77,9. Zincir oluğu rayın koridor tarafında (z 48,5–57,5), sabit uç x 265;",
    "  zemin kanalı (8 × 6, zeminde) x 476–484 QR altından oluğa. Robot zincirle x 50,8'den sola gidemez.",
    "QR DOLABI 86 × 52 × 205, x 457–543: robot yüzü z 67 = ön yüzden 59,1 (koridora 31 girer), müşteri yüzü z 119 → cephe nişi 113 × 69. 12 göz (taban 45–145) hepsi OK.",
    "TEZGÂH (personel) 60 × 45 × 90, x 395–455, ön duvara yaslı: ince duvara yalnız 39 → kapak ~41° açılır, çekmece strok 30 (açıkken 6,7 kalır).",
    "HÂLÂ AÇIK: (1) enerji zinciri U döngüsü 34 yüksek, 6'lık oluğa sığmaz; dönüşü açık K1'in altına girer (K1 1.–2. çekmece) ·",
    "  (2) alçak çekmecede erişim: alt sıralarda topların bir kısmı 77,9 dışında (matris) · (3) niş duvarı 451–457 ile tezgâh (tabla 456,5) çakışır ·",
    "  (4) bekleme / menü 162 → 100 (tezgâh yeri) · (5) QR müşteri paneli 166–177 (tekerlekli sandalye ≤ 122 değil) · (6) QR göz tabanında çatal yarığı yok.",
]
yy = OY + 480
for l in KARAR:
    txt(PX0 + 30, yy, l, f9 if not l.startswith(" ") else f8, INK if not l.startswith(" ") else GRAY)
    yy += 30

# ======================= KESİTLER (yan görünüş, ortak zemin · 1 cm = 3,2 px) =======================
SK = 3.2
DUVAR_UST = 214.0
ZEM = DY0 + 250 + 110 + DUVAR_UST * SK                         # zemin çizgisi (px): çekmece dizisinin altında başlık + duvar üstü
HH_ = lambda h: ZEM - h * SK
MOR = (110, 60, 150)


def duvar(uf, u0, u1, ust=DUVAR_UST):
    x0, x1 = uf(u0), uf(u1)
    d.rectangle([x0, HH_(ust), x1, ZEM], fill=DUV, outline=None)
    d.line([(x0, HH_(ust)), (x0, ZEM)], fill=LINE, width=2); d.line([(x1, HH_(ust)), (x1, ZEM)], fill=LINE, width=2)
    m = (x0 + x1) / 2                                           # kesik (üstü devam eder)
    d.line([(x0 - 6, HH_(ust) + 4), (m - 3, HH_(ust) - 4), (m + 3, HH_(ust) + 8), (x1 + 6, HH_(ust))], fill=LINE, width=2)


def kot(uf, u, h, s_, c=INK, a="lm", f=f7):
    txt(uf(u), HH_(h), s_, f, c, a)


def modul_yan(uf, ad):
    d.rectangle([uf(3), HH_(Y_PL), uf(HAT_ON - 6.0), ZEM], fill=SOFT, outline=LINE, width=2)       # plint (ön yüzden 6 geride)
    d.rectangle([uf(0), HH_(H_MAK), uf(HAT_ON), HH_(Y_PL)], fill=FILL, outline=LINE, width=3)
    txt((uf(0) + uf(HAT_ON)) / 2, HH_(H_MAK) + 18, ad, f9, INK, "mm")


def ray_oluk(uf):
    d.rectangle([uf(RAY_B[0]), HH_(6), uf(RAY_B[1]), ZEM], fill=RAYC, outline=ACC, width=2)
    d.rectangle([uf(OLUK_B[0]), HH_(6), uf(OLUK_B[1]), ZEM], fill=SOFT, outline=ACC, width=1)


def zemin(uf, u0, u1):
    d.line([(uf(u0), ZEM), (uf(u1), ZEM)], fill=INK, width=4)


# ---- KESİT A–A · x 480 ----
KA0 = OX + 100 + 12 * SK
ua = lambda u: KA0 + u * SK
txt(OX, HH_(DUVAR_UST) - 56, "KESİT A–A · x %d · E + robot + zemin kanalı + QR" % KES_A, f16, ACC)
duvar(ua, -12, 0)
modul_yan(ua, "E · KUTU")
for k_ in range(3):                                            # içecek yedeği 3 kat (koli 12,3)
    h0 = cm(IY["y"][0] + k_ * KU.KOLI["y"])
    d.rectangle([ua(ICY_Y[0]), HH_(h0 + cm(KU.KOLI["y"])), ua(ICY_Y[1]), HH_(h0)], fill=(232, 246, 238), outline=GRN, width=1)
kot(ua, ICY_Y[0] - 1.5, cm(IY["y"][0]) + 18, "içecek yedeği", GRN, "rm")
d.line([(ua(1), HH_(cm(KU.ALT_RAF_Y[1]))), (ua(HAT_D - 1), HH_(cm(KU.ALT_RAF_Y[1])))], fill=LINE, width=3)
kot(ua, 3, cm(KU.ALT_RAF_Y[1]) + 4, "alt raf %s" % sayi(cm(KU.ALT_RAF_Y[1])), GRAY, "lm")
d.line([(ua(pz(-360)), HH_(cm(KU.TEPSI))), (ua(HAT_D - 0.5), HH_(cm(KU.TEPSI)))], fill=INK, width=3)
kot(ua, pz(-360) - 1.5, cm(KU.TEPSI), "kutu tepsisi %s" % sayi(cm(KU.TEPSI)), INK, "rm")
ray_oluk(ua)
# robot (x 500, 2 cm arkada): kaide + omuz + erişim yayı + QR alt / üst göz bilek hedefleri
KAI_UST = cm(OMUZ - 152.0)
d.rectangle([ua(RAY_Y - 11), HH_(KAI_UST), ua(RAY_Y + 11), HH_(6)], fill=BG, outline=ACC, width=2)
kot(ua, RAY_Y, KAI_UST / 2 + 3, "FR5", ACC, "mm")
kot(ua, RAY_Y, KAI_UST / 2 - 4, "kaide", ACC, "mm")
om = (ua(RAY_Y), HH_(cm(OMUZ)))
darc(om[0], om[1], ERIS * SK, 250.0, 440.0, ACC, 1, 4.0, 2.0)                # (denetçi) 450 → 440: yay FR5 kaide kutusunun içine girmesin
for r in (0, 5):
    sat = [s_ for s_ in QR_ET if s_[0] == r]
    enk = max(sat, key=lambda s_: s_[5])
    hp = (ua(QR_Y[0]), HH_(cm(enk[4])))
    d.line([om, hp], fill=ACC, width=3)
    d.ellipse([hp[0] - 5, hp[1] - 5, hp[0] + 5, hp[1] + 5], fill=ACC)
d.ellipse([om[0] - 8, om[1] - 8, om[0] + 8, om[1] + 8], fill=BG, outline=ACC, width=3)
kot(ua, RAY_Y - 4, cm(OMUZ), "omuz %s" % sayi(cm(OMUZ)), ACC, "rm")
kot(ua, RAY_Y - 2, cm(OMUZ) + ERIS + 3, "erişim %s" % sayi(ERIS), ACC, "rm")
# zincir üst kolu (robot x 500'deyken x 262–500 arası) + zemin kanalı
d.rectangle([ua(ZNC_B[0]), HH_(ZNC_UST[1]), ua(ZNC_B[1]), HH_(ZNC_UST[0])], fill=ZINC)
kot(ua, (RAY_Y + 11 + QR_Y[0]) / 2, ZNC_UST[1] + 9, "zincir", ZINC, "mm")
kot(ua, (RAY_Y + 11 + QR_Y[0]) / 2, ZNC_UST[1] + 4, sayi(ZNC_UST[0], 0) + "–" + sayi(ZNC_UST[1], 0), RED, "mm")
d.rectangle([ua(KAN_B[0]), ZEM, ua(KAN_B[1]), ZEM - KAN_D * SK], fill=SOFT, outline=ACC, width=2)
# QR (x 480 kesiti): ayak, robot kontrol, raflar, 6 göz, ana pano, müşteri paneli
qx0, qx1 = ua(QR_Y[0]), ua(QR_Y[1])
d.rectangle([qx0, HH_(QR_H), qx1, ZEM], fill=BG, outline=INK, width=3)
d.rectangle([qx0 + 2, HH_(cm(QR.TABAN[1])), qx1 - 2, ZEM], fill=SOFT)
uq = lambda z_loc: ua(pz(QR.Z0 + z_loc))
uqm = lambda a_, b_: (pz(QR.Z0 + a_) + pz(QR.Z0 + b_)) / 2
d.rectangle([uq(QR.KONTROL["z"][0]), HH_(cm(QR.KONTROL["y"][1])), uq(QR.KONTROL["z"][1]), HH_(cm(QR.KONTROL["y"][0]))], fill=(225, 236, 250), outline=ACC, width=2)
kot(ua, uqm(*QR.KONTROL["z"]), cm(sum(QR.KONTROL["y"]) / 2) + 3, "robot", ACC, "mm")
kot(ua, uqm(*QR.KONTROL["z"]), cm(sum(QR.KONTROL["y"]) / 2) - 3, "kontrol", ACC, "mm")
for ry_ in (QR.ALT_RAF, QR.UST_RAF):
    d.rectangle([qx0, HH_(cm(ry_[1])), qx1, HH_(cm(ry_[0]))], fill=LINE)
for by_ in QR.GOZ_TABAN:
    d.rectangle([uq(QR.GOZ_Z[0]), HH_(cm(by_ + QR.GOZ_H)), uq(QR.GOZ_Z[1]), HH_(cm(by_))], fill=(246, 246, 248), outline=INK, width=1)
kot(ua, uqm(*QR.GOZ_Z), cm(QR.GOZ_TABAN[2] + QR.GOZ_H / 2), "göz %s derin" % sayi(cm(QR.GOZ_D)), GRAY, "mm")
d.rectangle([uq(QR.ANA_PANO["z"][0]), HH_(cm(QR.ANA_PANO["y"][1])), uq(QR.ANA_PANO["z"][1]), HH_(cm(QR.ANA_PANO["y"][0]))], fill=(240, 232, 248), outline=MOR, width=2)
kot(ua, uqm(*QR.ANA_PANO["z"]), cm(sum(QR.ANA_PANO["y"]) / 2) + 3, "ana", MOR, "mm")
kot(ua, uqm(*QR.ANA_PANO["z"]), cm(sum(QR.ANA_PANO["y"]) / 2) - 3, "pano", MOR, "mm")
PAN_Y = (cm(QR.PANEL_PENCERE["ekran"][2]) - 0.5, cm(QR.PANEL_PENCERE["ekran"][3]) + 0.5)   # müşteri paneli 166,3–177,3
d.rectangle([uq(QR.D - 47.0), HH_(PAN_Y[1]), uq(QR.D) - 1, HH_(PAN_Y[0])], fill=CAM, outline=ACC, width=2)
kot(ua, QR_Y[1] + 2, sum(PAN_Y) / 2 + 2.5, "müşteri paneli", ACC, "lm")
kot(ua, QR_Y[1] + 2, sum(PAN_Y) / 2 - 2.5, "%s–%s" % (sayi(PAN_Y[0]), sayi(PAN_Y[1])), ACC, "lm")
kot(ua, (QR_Y[0] + QR_Y[1]) / 2, QR_H + 5, "QR 86 × 52 × 205", INK, "mm", f8)
kot(ua, (QR_Y[1] + IC_D) / 2 + 4, 24, "cephe nişi", GRAY, "mm", f8)
kot(ua, (QR_Y[1] + IC_D) / 2 + 4, 17, "müşteri", GRAY, "mm")
zemin(ua, -12, IC_D + 14)
kot(ua, IC_D + 2, 3, "kaldırım", GRAY, "lm")
txt(ua(KAN_B[0]) - 6, ZEM + 12, "zemin kanalı z 49–100 (zeminde)", f7, ACC, "rm")
# ölçüler A–A
ya = ZEM + 50
for u0, u1, s_ in ((0, HAT_ON, "hat %s" % sayi(HAT_ON)), (HAT_ON, RAY_Y, sayi(RAY_Y - HAT_ON)), (RAY_Y, QR_Y[0], "31"), (QR_Y[0], QR_Y[1], "QR 52"), (QR_Y[1], IC_D, "niş 69")):
    olcu_h(ua(u0), ua(u1), ya, s_, f8, INK)
olcu_h(ua(0), ua(IC_D), ya + 40, sayi(IC_D), f9, INK)
olcu_v(ua(-12) - 30, HH_(H_MAK), ZEM, sayi(H_MAK), f8, INK, "l")
olcu_v(ua(IC_D + 14) + 24, HH_(QR_H), ZEM, sayi(QR_H), f8, INK, "r")

# ---- KESİT B–B · x 435 ----
KB0 = ua(IC_D + 14) + 190 + 12 * SK
ub = lambda u: KB0 + u * SK
txt(KB0 - 12 * SK - 60, HH_(DUVAR_UST) - 56, "KESİT B–B · x %d · K + bulaşık + ince duvar + tezgâh" % KES_B, f16, ACC)
duvar(ub, -12, 0)
modul_yan(ub, "K · KESME")
KT_ = cm(KS.H_B)
d.rectangle([ub(0), HH_(KT_ + 0.3), ub(HAT_ON - 4.0), HH_(KT_)], fill=LINE)          # K taban sacı 892–895 · önde kapak payı (kapak 20 + fitil)
kot(ub, 2, KT_ + 3, "K tabanı %s" % sayi(KT_), GRAY, "lm")
d.line([(ub(pz(FT.K_BANT_Z[0])), HH_(cm(KS.BANT))), (ub(HAT_D - 0.5), HH_(cm(KS.BANT)))], fill=INK, width=3)
kot(ub, pz(FT.K_BANT_Z[0]) - 1.5, cm(KS.BANT), "K bandı %s" % sayi(cm(KS.BANT)), INK, "rm")
d.rectangle([ub(BUL_Y[0]), HH_(BUL_H[1]), ub(BUL_Y[1]), HH_(BUL_H[0])], fill=SU, outline=ACC, width=2)
kot(ub, (BUL_Y[0] + BUL_Y[1]) / 2, (BUL_H[0] + BUL_H[1]) / 2 + 3, "BULAŞIK", ACC, "mm", f8)
kot(ub, (BUL_Y[0] + BUL_Y[1]) / 2, (BUL_H[0] + BUL_H[1]) / 2 - 3.5, "MEIKO 46 × 63 × 70", ACC, "mm")
d.rectangle([ub(BUL_Y[0]), HH_(cm(KS.Y_TABLA)), ub(BUL_Y[1]), HH_(cm(KS.Y_PLINT + 3.0))], fill=LINE)      # v15: bulaşık tablası (40 × 20 kiriş + tava), ayak yok
kot(ub, (BUL_Y[0] + BUL_Y[1]) / 2, (BUL_H[0] + BUL_H[1]) / 2 - 10, "ayaksız · tabla %s" % sayi(cm(KS.Y_TABLA)), ACC, "mm")
d.rectangle([ub(HAT_ON - 2.0), HH_(cm(KS.KAPAKLAR[0][3])), ub(HAT_ON), HH_(cm(KS.KAPAKLAR[0][2]))], fill=INK)            # K alt kapağı (tava 20)
kot(ub, HAT_ON + 1.5, cm(KS.KAPAKLAR[0][3]) - 4, "K alt kapağı", INK, "lm")
ray_oluk(ub)
kot(ub, RAY_Y, 9.5, "ray", ACC, "mm"); kot(ub, (OLUK_B[0] + OLUK_B[1]) / 2 + 1.5, 9.5, "oluk", ACC, "mm")
duvar(ub, Y_KOR1, Y_DUV1)
kot(ub, Y_KOR1 - 1.5, 120, "ince duvar", GRAY, "rm")
# tezgâh (x 435): plint, gövde, tabla, raf, çöp 10 L, çekmece (kapalı + açık), askı
tzb = lambda z_loc: ub(pz(TZ.Z0 + z_loc))
d.rectangle([tzb(0), HH_(cm(TZ.H - TZ.TABLA)), tzb(TZ.D), HH_(cm(TZ.PLINT))], fill=TEZ, outline=INK, width=2)
d.rectangle([tzb(50.0), HH_(cm(TZ.PLINT)), tzb(TZ.D), ZEM], fill=SOFT, outline=LINE, width=1)
d.rectangle([tzb(-TZ.TASMA), HH_(cm(TZ.H)), tzb(TZ.D), HH_(cm(TZ.H - TZ.TABLA))], fill=(230, 230, 234), outline=INK, width=2)
d.rectangle([tzb(0), HH_(cm(TZ.CEKMECE["y"][1])), tzb(TZ.CEKMECE["strok"]), HH_(cm(TZ.CEKMECE["y"][0]))], fill=BG, outline=INK, width=1)
drect(tzb(-TZ.CEKMECE["strok"] - TZ.KULP_CIKINTI), HH_(cm(TZ.CEKMECE["y"][1])), tzb(0), HH_(cm(TZ.CEKMECE["y"][0])), RED, 2)
kot(ub, (TZ_KULP + TZ_Y[0]) / 2, cm(sum(TZ.CEKMECE["y"]) / 2) + 2.5, "açık", RED, "mm")
kot(ub, (TZ_KULP + TZ_Y[0]) / 2, cm(sum(TZ.CEKMECE["y"]) / 2) - 2.5, "strok %s" % sayi(cm(TZ.CEKMECE["strok"])), RED, "mm")
d.rectangle([tzb(20.0), HH_(cm(TZ.RAF_Y[2])), tzb(441.0), HH_(cm(TZ.RAF_Y[1]))], fill=LINE)
d.rectangle([tzb(240.0), HH_(cm(668.0)), tzb(440.0), HH_(cm(TZ.RAF_Y[2]))], fill=(236, 226, 214), outline=GRAY, width=1)
kot(ub, pz(TZ.Z0 + 340.0), cm(543.0), "çöp 10 L", GRAY, "mm")
kot(ub, TZ_KULP, cm(TZ.H) + 6, "TEZGÂH 60 × 45 × 90", INK, "lm", f8)
d.rectangle([ub(IC_D - 7.0), HH_(cm(TZ.ASKI_Y) + 1), ub(IC_D), HH_(cm(TZ.ASKI_Y) - 1)], fill=INK)
kot(ub, IC_D - 8.5, cm(TZ.ASKI_Y), "askı %s" % sayi(cm(TZ.ASKI_Y)), INK, "rm")
duvar(ub, IC_D, IC_D + 12.0)
kot(ub, IC_D + 13.5, 120, "ön duvar", GRAY, "lm")
zemin(ub, -12, IC_D + 12)
# ölçüler B–B
yb2 = ZEM + 50
for u0, u1, s_ in ((0, HAT_ON, "hat %s" % sayi(HAT_ON)), (HAT_ON, RAY_Y, sayi(RAY_Y - HAT_ON)), (RAY_Y, Y_KOR1, sayi(Y_KOR1 - RAY_Y)), (Y_KOR1, Y_DUV1, "6"), (Y_DUV1, TZ_Y[0], sayi(DUVAR_PAY)), (TZ_Y[0], IC_D, "45")):
    olcu_h(ub(u0), ub(u1), yb2, s_, f8, INK)
olcu_h(ub(0), ub(IC_D), yb2 + 40, sayi(IC_D), f9, INK)
_hy = HH_(cm(TZ.CEKMECE["y"][0])) + 26
d.line([(ub(Y_DUV1), _hy), (ub(TZ_KULP), _hy)], fill=RED, width=2)
for _u in (Y_DUV1, TZ_KULP):
    d.line([(ub(_u), _hy - 7), (ub(_u), _hy + 7)], fill=RED, width=2)
txt(ub(TZ_KULP) + 6, _hy, sayi(TZ_KULP - Y_DUV1), f7, RED, "lm")
olcu_v(ub(IC_D + 12) + 40, HH_(cm(TZ.H)), ZEM, sayi(cm(TZ.H)), f8, INK, "r")
olcu_v(ub(-12) - 30, HH_(H_MAK), ZEM, sayi(H_MAK), f8, INK, "l")

# ---- QR DOLABI · robot tarafı / müşteri tarafı (aynı zemin, aynı ölçek) ----
QW = cm(QR.W)
QRB0 = ub(IC_D + 12) + 170
QMU0 = QRB0 + QW * SK + 200


def qr_gorunus(x0, ayna, baslik):
    qx = (lambda lx: x0 + (QW - cm(lx)) * SK) if ayna else (lambda lx: x0 + cm(lx) * SK)
    txt(x0 - 10, HH_(DUVAR_UST) - 56, baslik, f16, ACC)
    d.rectangle([x0, HH_(QR_H), x0 + QW * SK, ZEM], fill=FILL, outline=INK, width=3)
    d.rectangle([x0 + 3, HH_(cm(QR.TABAN[1])), x0 + QW * SK - 3, ZEM], fill=SOFT)
    for ry_ in (QR.ALT_RAF, QR.UST_RAF):
        d.rectangle([x0, HH_(cm(ry_[1])), x0 + QW * SK, HH_(cm(ry_[0]))], fill=LINE)
    for gx in QR.GOZ_X:
        for by_ in QR.GOZ_TABAN:
            a_, b_ = sorted((qx(gx), qx(gx + QR.GOZ_W)))
            d.rectangle([a_, HH_(cm(by_ + QR.GOZ_H)), b_, HH_(cm(by_))], fill=BG, outline=INK, width=1)
            txt((a_ + b_) / 2, (HH_(cm(by_ + QR.GOZ_H)) + HH_(cm(by_))) / 2, "göz 38 × 19", f7, GRAY, "mm")
    txt(x0, ZEM + 14, "x %d" % (543 if ayna else 457), f7, GRAY, "la")
    txt(x0 + QW * SK, ZEM + 14, "x %d" % (457 if ayna else 543), f7, GRAY, "ra")
    return qx


qx = qr_gorunus(QRB0, True, "QR DOLABI · robot tarafı")
for kut_, ad_, c_ in ((QR.KONTROL, ("ROBOT", "KONTROL", "47,5 × 42,3"), ACC), (QR.ANA_PANO, ("ANA", "PANO", "40 × 35"), MOR),
                      (dict(x=QR.KART["x"], y=QR.KART["y"]), ("kilit", "kartı", ""), MOR)):
    a_, b_ = sorted((qx(kut_["x"][0]), qx(kut_["x"][1])))
    d.rectangle([a_, HH_(cm(kut_["y"][1])), b_, HH_(cm(kut_["y"][0]))], fill=BG, outline=c_, width=2)
    ym = (HH_(cm(kut_["y"][1])) + HH_(cm(kut_["y"][0]))) / 2
    for k_, s_ in enumerate(ad_):
        if s_:
            txt((a_ + b_) / 2, ym + (k_ - 1) * 17, s_, f7, c_, "mm")
a_, b_ = sorted((qx(QR.UPS["x"][0]), qx(QR.UPS["x"][1])))
d.rectangle([a_, HH_(cm(QR.UPS["y"][1])), b_, HH_(cm(QR.UPS["y"][0]))], fill=BG, outline=MOR, width=2)
txt((a_ + b_) / 2, HH_(cm(QR.UPS["y"][1])) - 12, "UPS", f7, MOR, "mm")
kg = QR.KANGAL
a_, b_ = sorted((qx(kg["xc"] - kg["r_dis"]), qx(kg["xc"] + kg["r_dis"])))
_kg_ust = kg["y0"] + RE.kablo_hesabi()["N"] * RE.KABLO_D                              # ray_ek kangal: 10,07 sarım × Ø20 → y 20–221
drect(a_, HH_(cm(_kg_ust)), b_, HH_(cm(kg["y0"])), ACC, 2)
txt((a_ + b_) / 2, (HH_(cm(_kg_ust)) + HH_(cm(kg["y0"]))) / 2 - 9, "kablo", f7, ACC, "mm")
txt((a_ + b_) / 2, (HH_(cm(_kg_ust)) + HH_(cm(kg["y0"]))) / 2 + 9, "kangalı", f7, ACC, "mm")
xr = QRB0 + QW * SK
olcu_v(xr + 24, HH_(cm(QR.ALT_RAF[1])), ZEM, sayi(cm(QR.ALT_RAF[1])), f8, INK, "r")
olcu_v(xr + 24, HH_(cm(QR.UST_RAF[0])), HH_(cm(QR.ALT_RAF[1])), sayi(cm(QR.UST_RAF[0] - QR.ALT_RAF[1])), f8, INK, "r")
olcu_v(xr + 24, HH_(QR_H), HH_(cm(QR.UST_RAF[0])), sayi(QR_H - cm(QR.UST_RAF[0])), f8, INK, "r")
olcu_v(xr + 100, HH_(QR_H), ZEM, sayi(QR_H), f8, INK, "r")
olcu_h(QRB0, xr, ZEM + 50, sayi(QW), f8, INK)

qm = qr_gorunus(QMU0, False, "QR DOLABI · müşteri tarafı")
PP = QR.PANEL_PENCERE
drect(qm(PP["ekran"][0]) - 6, HH_(PAN_Y[1]) - 6, qm(PP["pin"][1]) + 6, HH_(PAN_Y[0]) + 6, ACC, 1)
for k_, ad_ in (("ekran", "ekran"), ("okuyucu", "QR"), ("pin", "PIN")):
    p0, p1, h0, h1 = PP[k_]
    d.rectangle([qm(p0), HH_(cm(h1)), qm(p1), HH_(cm(h0))], fill=CAM, outline=ACC, width=2)
    txt((qm(p0) + qm(p1)) / 2, HH_(PAN_Y[1]) - 18, ad_, f7, ACC, "mm")
txt(QMU0 + QW * SK / 2, (HH_(cm(QR.ALT_RAF[0])) + ZEM) / 2, "kapalı panel", f7, GRAY, "mm")
xm_ = QMU0 + QW * SK
olcu_v(xm_ + 24, HH_(PAN_Y[0]), ZEM, sayi(PAN_Y[0]), f8, ACC, "r")
olcu_v(xm_ + 24, HH_(PAN_Y[1]), HH_(PAN_Y[0]), sayi(PAN_Y[1] - PAN_Y[0]), f7, ACC, "r")
olcu_v(xm_ + 110, HH_(cm(QR.GOZ_TABAN[-1] + QR.GOZ_H)), HH_(cm(QR.GOZ_TABAN[0])),
       "göz %s–%s" % (sayi(cm(QR.GOZ_TABAN[0])), sayi(cm(QR.GOZ_TABAN[-1] + QR.GOZ_H))), f7, INK, "r")
olcu_h(QMU0, xm_, ZEM + 50, sayi(QW), f8, INK)
d.line([(QRB0 - 40, ZEM), (xm_ + 60, ZEM)], fill=INK, width=4)

d.line([(OX, H_PX - 80), (W_PX - 140, H_PX - 80)], fill=LINE, width=2)
txt(W_PX - 140, H_PX - 45, "AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v15_on_duzlem · 28 Eyl 2026 · üretici _uretec/dukkan_plani15.py", f9, GRAY, "rm")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
assert not os.path.exists(OUT) or "--uzerine" in sys.argv, "v15 zaten var: " + OUT
im.save(OUT)
print("yazildi:", OUT)
print("erişim: açıcı %.1f · E %.1f · QR en uzak %.1f · çekmece:" % (D1, D2, max(s_[5] for s_ in QR_ET)))
for k_, v in sorted(CEK_SONUC.items(), key=lambda kv: (kv[1][0], kv[1][1])):
    print("  %-16s taban %5.1f  %2d/%2d  robot x %s  max %s  %s" % (k_, v[3], v[4], v[5], v[6], v[7], v[9]))
if "--denetle" in sys.argv:
    n_ = 0
    for i, (b1, s1) in enumerate(_YAZI):
        for b2, s2 in _YAZI[i + 1:]:
            ox_ = min(b1[2], b2[2]) - max(b1[0], b2[0]); oy_ = min(b1[3], b2[3]) - max(b1[1], b2[1])
            if ox_ > 1 and oy_ > 1:
                n_ += 1; print("  ÜST ÜSTE: %r ↔ %r (%d × %d px)" % (s1, s2, ox_, oy_))
    print("yazı %d · üst üste binen çift %d" % (len(_YAZI), n_))
sys.stdout.flush()
os._exit(0)                                                    # OCP/cadquery kapanışta çöküyor (139) — çizim yazıldıktan sonra temiz çık
