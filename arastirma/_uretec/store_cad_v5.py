# -*- coding: utf-8 -*-
"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v5 (25 Eyl 2026)
v5: TAM KAPLAYAN KAPAKLAR (aralar 3, alt 126 / üst 1057 çizgisi) + ALT KISIM v3 dağılımı (içecek tek kat, tatlı,
    K4 kaşar + sucuk deposu + dar içecek) + PLC Secop'un arkasında. Önceki: store_cad_v4.py (yap_store_cad_v5.py)
v4: ALT TABAN ÇİZGİSİ 123 (Kemal) — yalıtımlı taban en alt çekmecenin 3 mm altına çıktı, gövde yerden 123'te başlar;
    K4 sıcak bölmesinin altı tek sac. Çekmeceler yerinde. Önceki: store_cad_v3.py
v3: ray ÜÇ ELEMANLI teleskop (dış sabit · ara strok/2 · iç strok) — v2'de iç profil açılınca dış profilden
    tamamen çıkıp çekmece havada kalıyordu (Kemal 25 Eyl). Önceki: store_cad_v2.py

Kemal: "fitil (dolap olduğu için her kapakta vardı), çekmecelerin içi, nasıl çalıştığı (otomatik, robot alsın diye
TAM açılacaktı), motor nerede olacaktı — SolidWorks'te tasarlamıştık, o detayların hepsini ekle, adapte et;
üretilebilir, motor vs standart ürünler."

KAYNAK KARARLAR (değiştirilmedi, yalnız ölçüye uyarlandı):
  otonom/hat/cekmece.html (8 Eyl) · 1_STORE/PROBLEMLER.md M8–M22 · sw_store_v4.py · ist1_store6.py (conta tarifi)
  · PC → Modbus TCP → PLC; PLC çekmecenin rölesini çeker, TEK sürücü o motoru döndürür ("aynı anda tek çekmece hareket eder")
  · motor kasada SABİT, çekmecenin arkasındaki boşlukta; kayış çekmecenin YAN yüzündeki pabuca kenetli
  · T4: kayış hattı YAN DUVARDA, ürünün altında değil (v1'de kutunun altındaydı → düzeltildi)
  · kapalı/açık doğrulaması reed sensör + mıknatıs · sıkışmada sürücü akım sınırı
  · fitil: endüstriyel geçmeli manyetik profil 21 × 18,5 (sıkışınca 15) · iç sacdaki kanal 6,3 · geçme dişi 8,3 · aletsiz sökülür

STANDART ÜRÜNLER (üretici datasheet ölçüleriyle modellendi; resmi STEP henüz indirilmedi):
  motor   Transmotec PD3665-24-51-BFEC · Ø36 planet 51:1 · 24 V · 127 d/dk · 0,853 N·m (sürekli 1,77 · kısa 5,3) · enkoder
          (eski karar sonsuz vidalıydı; Ø42 WRD5066 dik çıkışlı, 146 mm boyla 57 mm'lik arka boşluğa sığmıyor)
  ray     Accuride DZ3832-0070 · 700 · tam çekilir (%100) · 45,7 × 12,7 · 45–50 kg · 3 eleman: dış (kasa) · ara · iç (çekmece)
  kasnak  GT3 30 diş · 6 mm (PD 28,65 · çevre 90) · kayış GT3 6 mm kapalı çevrim
  sensör  Littelfuse 59135 reed + 57135 mıknatıs (28,57 × 19,05 × 6,35) · her çekmecede 2: KAPALI + AÇIK
  sürücü  Electromen EM-324C (10–35 V, 4 A, akım sınırı) · seçici röle Phoenix Contact PLC-RSC-24DC/21 (6,2 mm) × 21
  PLC     Siemens S7-1200 CPU 1214C DC/DC/DC 6ES7214-1AG40-0XB0 + 2 × SM1221 DI16 + SM1222 DQ16
  güç     Mean Well NDR-240-24 (24 V 10 A)
  soğutma Secop CU KLF4.0CND R290 (314H6008) · 272 × 350 × 450 · 335 W @ −10 °C / 25 °C
  fan     ebm-papst 4414 FNH (119 × 119 × 25, 24 V) · evaporatör: roll-bond levha (ölçüye üretim)
  ayak    Elesa+Ganter LV.A-SST (paslanmaz) M12
KOORDİNAT: hat ile aynı — x 0..2500 (B), y 0..1060, z 0 = çekmece ön yüzü, −830 arka.
"""
import csv, io, math, os
import cadquery as cq
from kaset_3d_v3 import MALZEME

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
_p = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), encoding="utf-8").read()
_g = {"__name__": "_pafta7", "os": os, "math": math}
exec(_p[_p.index("# ======================= ORTAK VERI (HAT 2 KOL v19) ======================="):_p.index("\nOX, FY_TOP")], _g)
WO, BIND, FUGA, BOLME, XI, YUZ0 = (_g[k] for k in ("WO", "BIND", "FUGA", "BOLME", "XI", "YUZ0"))
HH, CAP, KOLON, KOLON_AD = _g["HH"], _g["CAP"], _g["KOLON"], _g["KOLON_AD"]
# v5 · ALT KISIM v3 (Kemal 25 Eyl: soğukta her şey 2 gün; içecek tek kat → robot her kutuya erişir)
HH = dict(HH); HH.update({"ic1": 126.0, "ic1d": 126.0, "tatli": 71.0})       # kutu 115 / tatlı kabı 60 + 11 taban payı
KOLON = [[(5, "hamur"), (2, "lahm"), (1, "tatli")], [(3, "hamur"), (5, "lahm")], [(5, "lahm"), (2, "ic1")]]
K4_CEK = [(2, "ic1d")]
KAPAK_X = {"K1": (0.0, 698.5), "K2": (701.5, 1353.5), "K3": (1356.5, 2008.5), "K4": (2011.5, 2500.0)}   # tam kaplama, aralar 3
ON_ALT, ON_UST = 126.0, 1057.0                   # bütün kolonlarda ön yüzün alt ve üst çizgisi
GN_H = 230.0                                      # K4 kaşar + sucuk deposu yüksekliği (GN 1/1-100 + raf + GN 1/2-100)
H_B, W_B, DZ = _g["H_B"], _g["W_B"], _g["DZ"]

for _k, _v in {"sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32), "pu": ((0.93, 0.88, 0.72, 1.0), 0.0, 0.85),
               "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45), "kart": ((0.10, 0.35, 0.22, 1.0), 0.1, 0.6),
               "hamur": ((0.94, 0.86, 0.68, 1.0), 0.0, 0.9), "silikon": ((0.86, 0.30, 0.22, 1.0), 0.0, 0.7),
               "kutu_icecek": ((0.78, 0.10, 0.12, 1.0), 0.7, 0.35), "izgara": ((0.30, 0.32, 0.35, 1.0), 0.6, 0.5),
               "conta": ((0.90, 0.90, 0.88, 1.0), 0.0, 0.8), "plastik": ((0.55, 0.57, 0.60, 1.0), 0.0, 0.6),
               "siemens": ((0.23, 0.36, 0.40, 1.0), 0.2, 0.5), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3),
               "bakir": ((0.72, 0.45, 0.20, 1.0), 0.9, 0.35), "kanal": ((0.55, 0.58, 0.62, 1.0), 0.0, 0.7)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2]))

PARCALAR = []
def ekle(ad, wp, mal, birim, bom=None, grup="SABIT"):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, bom=bom, grup=grup))

kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))

# ---------------------------------------------------------------- KOTLAR (v1 ile aynı gövde)
Z_ON0, Z_ON1 = -40.0, 0.0
Z_CON0, Z_CON1 = -55.0, -40.0
Z_CER0, Z_CER1 = -56.0, -55.0
Z_ARKA = -790.0
TABAN_T = 41.5                         # yalıtımlı taban: dış sac 1,5 + PU 39 + iç sac 1,0
Y_TABAN = YUZ0 - FUGA                  # v4: 164,5 — en alt çekmece önünün (167,5) 3 mm altı (v3: 121,5)
Y_PLINT = Y_TABAN - TABAN_T            # v4: 123 = ALT TABAN ÇİZGİSİ, bütün istasyon gövdeleri buradan başlar (v3: 80)
Y_TAVAN = 1000.0
X_IC0, X_IC1 = 30.0, W_B - 30.0
KC = 5.0
KUTU_KENAR = 30.0                      # v2: 16 → 30. Ray (12,7) ile kutu arasında 17,3'lük YAN BANT — kayış burada (T4)
TEPSI_T, CUKUR_H = 10.0, 7.0
Y_OTUR = KC + 1.0 + TEPSI_T - CUKUR_H  # 9
TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=4, ax=105.0, az=130.0, td=520.0),
       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=6, ax=88.0, az=90.0, td=540.0)}
TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0, "ic1": 660.0, "ic1d": 660.0, "tatli": 660.0}
TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6)          # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104
K4_YO = 123.0 + 1.5 + 4.0 + 272.0 + 8.0 + 30.0 + GN_H + 1.0 + 3.0 + 15.0      # K4 ilk dar çekmece açıklığı 687,5
ICECEK_KAT, ICECEK = 115.0, dict(r=33.0, ax=82.0, az=75.0)
# FİTİL — geçmeli manyetik profil (u: açıklıktan DIŞARI, z mutlak). Yol açıklık kenarının 4 mm dışında.
FITIL_G = 4.0
FITIL = [(-2.0, -31.7), (2.0, -31.7), (2.0, -33.0), (3.15, -34.0), (2.0, -35.2), (2.0, -40.0), (6.0, -40.0), (6.0, -42.0), (8.0, -42.0), (8.0, -50.0),
         (10.5, -50.0), (10.5, -55.0), (-10.5, -55.0), (-10.5, -50.0), (-8.0, -50.0), (-8.0, -42.0), (-6.0, -42.0), (-6.0, -40.0), (-2.0, -40.0),
         (-2.0, -35.2), (-3.15, -34.0), (-2.0, -33.0)]
KANAL = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]     # kapak iç sacındaki geçme kanalı 6,4 × 8,4
# RAY Accuride DZ3832-0070
RAY_H, RAY_T, RAY_L, RAY_Y0 = 45.7, 12.7, 700.0, 4.0
# v3 · üç eleman iç içe (datasheet zarfı 45,7 × 12,7 içinde; sac kalınlıkları ve bilye kafesleri sadeleştirildi)
#   w = duvardan çekmeceye doğru mesafe · dış C (gövde w 0–1,2, flanş w 0–8,5) · ara C (gövde 1,7–2,7, flanş 1,7–10,5)
#   · iç C (çekmece tarafı gövde 11,5–12,7, flanş 3,2–12,7) · her eleman bir öncekinden 2 mm kısa, önden 2 mm geride
RAY_DIS_W, RAY_ARA_W, RAY_KISA = 8.5, 10.5, 2.0
RAY_ARA_ORAN = 0.5                     # ara eleman strokun yarısı kadar gelir [VARSAYIM — bilyeli teleskopta olağan; katalogla teyit]
# TAHRİK Transmotec PD3665-24-51-BFEC (datasheet çizimi): mil Ø8 × 20 (7'ye düz) · göbek Ø22 × 2 · redüktör Ø36 × 50,5 · motor Ø36 × 65
MIL_D, MIL_L, GOBEK_D, GOBEK_L, RED_L, MOT_L, MOT_D = 8.0, 20.0, 22.0, 2.0, 50.5, 65.0, 36.0
ENK_L = 20.0                           # enkoder + plastik kapak boyu [VARSAYIM — datasheet'te ölçü yok]
KAS_PD, KAS_OD, KAS_FL, KAS_B = 28.65, 27.9, 34.0, 11.0     # GT3 30 diş · flanşlı
KAYIS_W, KAYIS_T = 6.0, 1.26           # GT3 6 mm · SIRT kalınlığı (dişler kasnak oyuklarına girer, modelde dış çapa oturur)
KX = 21.0                              # kayış merkezi açıklığın sol kenarından (ray 12,7 … kutu 30 arası)
KY = 30.0                              # kasnak ekseni açıklık tabanından
Z_MOTOR, Z_AVARA = -769.0, -73.0       # motor Ø36: −787 … −751 (arka duvar −790, ayak sacı −790 … −787)
PABUC = (-751.0, -721.0)               # kayış çenesi (kasnak flanşının 1 mm önü)
STROK = (Z_AVARA - KAS_FL / 2.0 - 3.0) - PABUC[1]           # çene ön kenarı avara flanşına 3 mm kala durur
SEN = (28.57, 19.05, 6.35)             # Littelfuse 59135 / 57135 (boy z · yükseklik y · kalınlık x)
SEN_X = (KX - 4.0, KX + 2.35)          # mıknatıs çenenin üstünde (x 17 … 23,35)
SEN_Y0 = 50.0                          # ray tepesinin (49,7) üstü
# kablo kanalı
KAN_X, KAN_Z = (190.0, 230.0), (Z_ARKA, Z_ARKA + 25.0)
KAN_UST = (975.0, 1000.0)


def kolonlar():
    out, cx = [], XI
    for ki, gruplar in enumerate(KOLON):
        yo, n = YUZ0 + BIND, {}
        for adet, tip in gruplar:
            for _ in range(adet):
                n[tip] = n.get(tip, 0) + 1
                out.append((KOLON_AD[ki], "CEK_%s_%s_%d" % (KOLON_AD[ki], tip, n[tip]), tip, cx, yo))
                yo += HH[tip] + 2 * BIND + FUGA
        cx += WO + BOLME
    yo, n = K4_YO, {}                                                    # v5 · K4 dar çekmeceler (depo üstünde)
    for adet, tip in K4_CEK:
        for _ in range(adet):
            n[tip] = n.get(tip, 0) + 1
            out.append(("K4", "CEK_K4_%s_%d" % (tip, n[tip]), tip, cx, yo))
            yo += HH[tip] + 2 * BIND + FUGA
    return out, cx


CEK, K4X = kolonlar()
K4W = 400.0
GEN = lambda kol: K4W if kol == "K4" else WO
ALT_KOD = {min((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in ("K1", "K2", "K3")}
UST_KOD = {max((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in ("K1", "K2", "K3", "K4")}
KOLON_X = {KOLON_AD[i]: XI + i * (WO + BOLME) for i in range(len(KOLON))}
K1X = KOLON_X["K1"]


def top_kati(tip):
    t = TOP[tip]
    kure = cq.Workplane("XY").sphere(t["R"]).intersect(kut(-t["R"], t["R"], 0.0, t["R"], -t["R"], t["R"])).translate((0, t["hc"], 0))
    return sily(0.0, 0.0, t["R"], 0.0, t["hc"]).union(kure)


def cevre_supur(ax0, ax1, ay0, ay1, prof):
    """açıklık (ax0..ax1 × ay0..ay1) çevresinde, FITIL_G dışarıdaki yol boyunca profili süpürür (keskin köşe)"""
    g = FITIL_G
    P = [((ax0 + ax1) / 2.0, ay0 - g), (ax1 + g, ay0 - g), (ax1 + g, ay1 + g), (ax0 - g, ay1 + g), (ax0 - g, ay0 - g)]
    yol = cq.Workplane("XY", origin=(0, 0, -40.0)).polyline(P).close()
    pts = [(ay0 - g - u, zz) for u, zz in prof]
    return cq.Workplane("YZ", origin=((ax0 + ax1) / 2.0, 0, 0)).polyline(pts).close().sweep(yol, transition="right")


def kapak_on(ad, a_, b_, c_, d_, bir, acik, grup="SABIT", fitil=True, bom=None):
    """kulpsuz 40'lık ön: dış sac 1,5 (dört kenardan bükülü) + PU + iç sac 1,0; iç sacda fitil kanalı; fitil"""
    ds = kut(a_, b_, c_, d_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
    pu = kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0 + 1.0, Z_ON1 - 1.5)
    ic = kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0, Z_ON0 + 1.0)
    if fitil:
        kn = cevre_supur(acik[0], acik[1], acik[2], acik[3], KANAL)
        pu, ic = pu.cut(kn), ic.cut(kn)
    ekle(ad + "_dis_sac_1.5", ds, "sac", bir, grup=grup, bom=bom)
    ekle(ad + "_pu", pu, "pu", bir, grup=grup)
    ekle(ad + "_ic_sac_1.0", ic, "sac", bir, grup=grup)
    if fitil:
        ekle(ad + "_fitil", cevre_supur(acik[0], acik[1], acik[2], acik[3], FITIL), "conta", bir, grup=grup,
             bom=("Fitil · geçmeli manyetik profil 21 × 18,5", 1, "PVC + şerit mıknatıs · kapak iç sacının 6,4'lük kanalına geçer · aletsiz sökülür",
                  "çevre %.0f mm · köşeler gönye kaynaklı" % (2 * (acik[1] - acik[0] + acik[3] - acik[2] + 4 * FITIL_G))))


def cekmece(kol, kod, tip, x0, yo):
    wo = GEN(kol); h = HH[tip]; x1 = x0 + wo; y1 = yo + h; xc = x0 + wo / 2.0
    TUB_D = TUB[tip]; Z_TUB1 = Z_CON0 - 2.0; Z_TUB0 = Z_TUB1 - TUB_D      # v2: kutu fitil halkasinin ARKASINDA biter (21'lik fitil acikliga 6,5 tasar)
    G = "CEKMECE"
    # ---- ön + fitil (hareketli) ----
    pa, pb = KAPAK_X[kol]                                               # v5 · TAM KAPLAMA
    pc = ON_ALT if kod in ALT_KOD else yo - BIND
    pd = ON_UST if kod in UST_KOD else y1 + BIND
    kapak_on(kod + "_on", pa, pb, pc, pd, kod, (x0, x1, yo, y1), grup=G,
             bom=("Çekmece önü 40 · kulpsuz · tam kaplama", 1, "dış 304 1,5 bükme + PU 37,5 köpük + iç 304 1,0 (fitil kanallı)", "%.0f × %.0f" % (pb - pa, pd - pc)))
    # ---- kutu (hareketli) ----
    ka, kb, kc, kd = x0 + KUTU_KENAR, x1 - KUTU_KENAR, yo + KC, y1 - 10.0
    u = kut(ka, kb, kc, kc + 1.0, Z_TUB0, Z_TUB1).union(kut(ka, ka + 1.0, kc, kd, Z_TUB0, Z_TUB1)).union(kut(kb - 1.0, kb, kc, kd, Z_TUB0, Z_TUB1))
    ekle(kod + "_kutu_U_1.0", u, "sac", kod, grup=G, bom=("Çekmece kutusu U 1,0", 1, "304 lazer + 2 büküm", "%d × %d × %d" % (kb - ka, kd - kc, TUB_D)))
    ekle(kod + "_kutu_arka_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB0, Z_TUB0 + 1.0), "sac", kod, grup=G)
    ekle(kod + "_kutu_on_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB1 - 1.0, Z_TUB1), "sac", kod, grup=G)
    # on ↔ kutu kose baglantilari: fitil halkasinin ICINDEN gecer (halka ic kenari aciklikta 6,5)
    for ad_, a_, b_ in (("sol", ka, ka + 15.0), ("sag", kb - 15.0, kb)):
        ekle(kod + "_on_baglanti_" + ad_, kut(a_, b_, yo + 12.0, kd - 4.0, Z_TUB1, Z_ON0), "celik", kod, grup=G,
             bom=("Ön bağlantı köşesi", 2, "304 2 mm büküm · öne 2 × M5 perçin somun", "ön yüz ayar yuvalı") if ad_ == "sol" else None)
    # ray adaptör lamları: kutu ile ray iç profili arasındaki 17,3'ü köprüler (kayışın ALTINDA kalır)
    for ad_, a_, b_ in (("sol", x0 + RAY_T, ka), ("sag", kb, x1 - RAY_T)):
        ekle(kod + "_ray_adaptor_" + ad_, kut(a_, b_, yo + RAY_Y0, yo + RAY_Y0 + 6.0, Z_TUB0, Z_TUB1), "celik", kod, grup=G,
             bom=("Ray adaptör lamı 6 mm", 2, "304 lama · kutuya punta", "ray iç profiline 4 × M4") if ad_ == "sol" else None)
    # ---- ray (her iki yan) · v3: ÜÇ ELEMANLI TELESKOP — dış (kasa) SABİT · ara strok/2 · iç (çekmece) strok ----
    #      v2'de iç profil kutu boyundaydı ve açılınca dış profilin önünden tamamen çıkıyordu (çekmece havada kalıyordu)
    for ad_, rx0, yon in (("sol", x0, 1.0), ("sag", x1, -1.0)):
        ry0 = yo + RAY_Y0
        def rk(w0, w1, y0_, y1_, z0_, z1_, _r=rx0, _s=yon, _y=ry0):
            return kut(_r + _s * w0, _r + _s * w1, _y + y0_, _y + y1_, z0_, z1_)
        za, zb = Z_CER0 - RAY_L, Z_CER0
        dis = rk(0.0, 1.2, 0.0, RAY_H, za, zb).union(rk(0.0, RAY_DIS_W, 0.0, 1.2, za, zb)).union(rk(0.0, RAY_DIS_W, RAY_H - 1.2, RAY_H, za, zb))
        ekle(kod + "_ray_dis_" + ad_, dis, "celik", kod,
             bom=("Teleskopik ray Accuride DZ3832-0070", 2, "700 · %100 açılır · 3 elemanlı · 45,7 × 12,7 · 45–50 kg (çift)", "dış eleman kolon yan duvarına 4 × M5") if ad_ == "sol" else None)
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ara = rk(1.7, 2.7, 1.7, RAY_H - 1.7, za, zb).union(rk(1.7, RAY_ARA_W, 1.7, 2.7, za, zb)).union(rk(1.7, RAY_ARA_W, RAY_H - 2.7, RAY_H - 1.7, za, zb))
        ekle(kod + "_ray_ara_" + ad_, ara, "celik", kod, grup="CEKMECE_ARA")
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ic = rk(RAY_T - 1.2, RAY_T, 5.0, RAY_H - 5.0, za, zb).union(rk(3.2, RAY_T, 5.0, 6.2, za, zb)).union(rk(3.2, RAY_T, RAY_H - 6.2, RAY_H - 5.0, za, zb))
        ekle(kod + "_ray_ic_" + ad_, ic, "celik", kod, grup=G)
    # ---- TAHRİK (sabit): kasnak — motor — enkoder — M12, arka boşlukta; avara önde; kayış YAN bantta ----
    kx, ky = x0 + KX, yo + KY
    fl0 = kx - KAS_B / 2.0; fl1 = kx + KAS_B / 2.0
    pul = silx(ky, 0.0, KAS_OD / 2.0, fl0 + 1.5, fl1 - 1.5).union(silx(ky, 0.0, KAS_FL / 2.0, fl0, fl0 + 1.5)).union(silx(ky, 0.0, KAS_FL / 2.0, fl1 - 1.5, fl1))
    pul_m = pul.cut(silx(ky, 0.0, MIL_D / 2.0, fl0 - 1, fl1 + 1))          # motor kasnagi: Ø8 mil delikli
    pul_a = pul.cut(silx(ky, 0.0, 2.5, fl0 - 1, fl1 + 1))                  # avara: Ø5 mil (rulmanlar icinde)
    ekle(kod + "_motor_kasnagi", pul_m.translate((0, 0, Z_MOTOR)), "aluminyum", kod,
         bom=("GT3 kasnak 30 diş · 6 mm · flanşlı", 1, "alüminyum · delik Ø8 H7 + düz", "PD 28,65 · çevre 90 mm"))
    mx0 = fl1 + 2.0 + GOBEK_L                        # motor flanş yüzü (mil kasnaktan geçer)
    ekle(kod + "_motor_mili", silx(ky, Z_MOTOR, MIL_D / 2.0, fl0 - 2.0, mx0 - GOBEK_L), "celik", kod)
    ekle(kod + "_motor_gobegi", silx(ky, Z_MOTOR, GOBEK_D / 2.0, mx0 - GOBEK_L, mx0), "celik", kod)
    ekle(kod + "_motor_reduktor", silx(ky, Z_MOTOR, MOT_D / 2.0, mx0, mx0 + RED_L), "motor", kod,
         bom=("Motor Transmotec PD3665-24-51-BFEC", 1, "24 V · planet 51:1 · 127 d/dk · 0,853 N·m · manyetik enkoder · EMC filtreli",
              "Ø36 × 115,5 + enkoder · datasheet: transmotec.com PD3665"))
    ekle(kod + "_motor_govde", silx(ky, Z_MOTOR, MOT_D / 2.0, mx0 + RED_L, mx0 + RED_L + MOT_L), "motor", kod)
    me = mx0 + RED_L + MOT_L
    ekle(kod + "_enkoder_kapagi", silx(ky, Z_MOTOR, 16.0, me, me + ENK_L), "plastik", kod)
    ekle(kod + "_m12_soket", silx(ky, Z_MOTOR, 8.0, me + ENK_L, x0 + KAN_X[0]), "koyu", kod,
         bom=("M12 4 pin soket + kablo", 1, "motor + enkoder tek soket · kasada sabit", "kablo dikey kanala"))
    # motor braketi: 3 mm dik plaka (flanş yüzüne 4 × M3 Ø31) + arka duvara L ayak
    pl = kut(mx0 - 3.0, mx0, ky - 22.0, ky + 22.0, Z_ARKA + 3.0, PABUC[0] - 0.5).cut(silx(ky, Z_MOTOR, GOBEK_D / 2.0 + 0.5, mx0 - 4, mx0 + 1))
    pl = pl.union(kut(mx0 - 3.0, mx0 + 40.0, ky - 22.0, ky + 22.0, Z_ARKA, Z_ARKA + 3.0))
    ekle(kod + "_motor_braketi", pl.cut(silx(ky, Z_MOTOR, MOT_D / 2.0 + 0.2, mx0 + 3.0, mx0 + 41.0)), "celik", kod,
         bom=("Motor braketi 3 mm", 1, "304 lazer + büküm · 4 × M3 (Ø31) + arka duvara 2 × M5", "kasnak hizası buradan"))
    # ön avara (dişli, çift rulmanlı) + çerçeveye bağlanan kol
    ekle(kod + "_avara", pul_a.translate((0, 0, Z_AVARA)), "aluminyum", kod, bom=("GT3 avara 30 diş · 6 mm · çift rulman", 1, "alüminyum · 2 × 625-2RS", "ön çerçevenin 17 mm arkası"))
    ekle(kod + "_avara_mili", silx(ky, Z_AVARA, 2.5, x0 + RAY_T + 2.6, fl1 + 1.0), "celik", kod)
    ekle(kod + "_avara_kolu", kut(x0 + RAY_T + 0.1, x0 + RAY_T + 2.6, ky - 8.0, y1 + 12.0, Z_AVARA - 8.0, Z_CER0), "celik", kod,
         bom=("Avara kolu 3 mm", 1, "304 büküm · ön çerçevenin arkasına 2 × M4 perçin somun", "kayış gergisi burada: 8 mm yuvalı"))
    # kayış (üst ve alt koşu, yan bantta)
    r0, r1 = KAS_OD / 2.0, KAS_OD / 2.0 + KAYIS_T                         # kayis sirti kasnak dis capina oturur
    kay = kut(kx - KAYIS_W / 2, kx + KAYIS_W / 2, ky + r0, ky + r1, Z_MOTOR, Z_AVARA)
    kay = kay.union(kut(kx - KAYIS_W / 2, kx + KAYIS_W / 2, ky - r1, ky - r0, Z_MOTOR, Z_AVARA))
    for zc_, arka_ in ((Z_MOTOR, True), (Z_AVARA, False)):                 # kasnak cevresindeki yarim sarimlar
        halka = silx(ky, zc_, r1, kx - KAYIS_W / 2, kx + KAYIS_W / 2).cut(silx(ky, zc_, r0, kx - KAYIS_W / 2 - 1, kx + KAYIS_W / 2 + 1))
        yari = kut(kx - 10, kx + 10, ky - r1 - 1, ky + r1 + 1, zc_ - r1 - 1, zc_) if arka_ else kut(kx - 10, kx + 10, ky - r1 - 1, ky + r1 + 1, zc_, zc_ + r1 + 1)
        kay = kay.union(halka.intersect(yari))
    L_kay = 2 * (Z_AVARA - Z_MOTOR) + math.pi * KAS_PD
    ekle(kod + "_kayis_GT3", kay, "koyu", kod, bom=("Kayış GT3 6 mm kapalı çevrim", 1, "~%.0f mm (%d diş) · çelik kordlu" % (L_kay, round(L_kay / 3.0)), "tedarikçi boyu doğrulayacak"))
    # kayış çenesi + kol (hareketli): kayışın üst koşusunu alttan/üstten kenetler, kolu kutunun yan duvarına kaynaklı
    yu0, yu1 = ky + r0, ky + r1
    cene = kut(x0 + 17.0, ka, yu1, yu1 + 2.5, PABUC[0], PABUC[1]).union(kut(x0 + 17.0, ka, yu0 - 2.5, yu0, PABUC[0], PABUC[1]))
    cene = cene.union(kut(kx + KAYIS_W / 2, ka, yu0 - 2.5, yu1 + 2.5, PABUC[0], PABUC[1]))          # cene yan plakasi
    cene = cene.union(kut(ka - 3.0, ka, yu0 - 2.5, yu1 + 2.5, PABUC[1], Z_TUB0 + 30.0))              # kol: avara flansinin (x 26,5) DISINDAN gecer
    ekle(kod + "_kayis_cenesi", cene, "celik", kod, grup=G,
         bom=("Kayış çenesi + kolu", 1, "304 · kutunun yan duvarına kaynaklı · dişli çene 2 × M3", "kutunun arkasından kasnağa uzanır (strok için)"))
    # mıknatıs (çenenin üstünde, hareketli) + 2 reed sensör (sabit): KAPALI ve AÇIK konum
    my0 = yo + SEN_Y0
    ekle(kod + "_miknatis_ayagi", kut(x0 + SEN_X[0], x0 + SEN_X[1], yu1 + 2.5, my0, PABUC[0], PABUC[0] + SEN[0]), "celik", kod, grup=G)
    ekle(kod + "_miknatis_57135", kut(x0 + SEN_X[0], x0 + SEN_X[1], my0, my0 + SEN[1], PABUC[0], PABUC[0] + SEN[0]), "plastik", kod, grup=G,
         bom=("Mıknatıs Littelfuse 57135-000", 1, "AlNiCo 5 · flanşlı 28,57 × 19,05 × 6,35", "çenenin üstünde"))
    for ad_, z0_ in (("kapali", PABUC[0]), ("acik", PABUC[0] + STROK)):
        ekle(kod + "_reed_" + ad_, kut(x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6, my0, my0 + SEN[1], z0_, z0_ + SEN[0]), "plastik", kod,
             bom=("Reed sensör Littelfuse 59135-010", 2, "NO · flanşlı 28,57 × 19,05 × 6,35", "KAPALI + AÇIK konum · PLC girişine") if ad_ == "kapali" else None)
    ekle(kod + "_sensor_lami", kut(x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6, my0 + SEN[1], my0 + SEN[1] + 2.0, Z_ARKA, Z_AVARA - 12.0), "celik", kod)
    # ---- içerik (hareketli) ----
    if tip in TOP:
        t = TOP[tip]
        tz0, tz1 = Z_TUB0 + 5.0, Z_TUB0 + 5.0 + t["td"]
        tx0, tx1 = xc - 265.0, xc + 265.0
        ty0 = kc + 1.0
        X = [xc + (i - (t["nx"] - 1) / 2.0) * t["ax"] for i in range(t["nx"])]
        Zc = (tz0 + tz1) / 2.0
        Z = [Zc + (j - (t["nz"] - 1) / 2.0) * t["az"] for j in range(t["nz"])]
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(t["cr"]).extrude(-(CUKUR_H + 1.0)).translate((0, ty0 + TEPSI_T - CUKUR_H, 0))
        ekle(kod + "_tepsi", kut(tx0, tx1, ty0, ty0 + TEPSI_T, tz0, tz1).cut(cuk), "silikon", kod, grup=G,
             bom=("Tepsi · %d çukur Ø%.0f" % (len(X) * len(Z), 2 * t["cr"]), 1, "gıda silikonu 10 mm · çukur 7 · kalıp döküm", "530 × %.0f" % t["td"]))
        tk = top_kati(tip)
        for i, a in enumerate(X):
            for j, b in enumerate(Z):
                ekle("%s_top_%d_%d" % (kod, i, j), tk.translate((a, yo + Y_OTUR, b)), "hamur", kod, grup=G)
        return len(X) * len(Z), yo + Y_OTUR + t["hc"] + t["R"], y1
    if tip in ("ic1", "ic1d", "tatli"):                                   # v5 · TEK KAT, ŞERİTLİ, YAYLI İTİCİLİ
        tat = tip == "tatli"
        r = TATLI["r"] if tat else ICECEK["r"]; hk = TATLI["h"] if tat else ICECEK_KAT
        px = TATLI["ax"] if tat else ICECEK["ax"]; pz = TATLI["az"] if tat else 2.0 * r
        nz = TATLI["nz"] if tat else 8
        ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_TUB1 - 13.0
        nx = int((ix1 - ix0 - 12.0 - 2 * r) // px) + 1
        xm = (ix0 + ix1) / 2.0
        X = [xm + (i - (nx - 1) / 2.0) * px for i in range(nx)]
        Z = [iz1 - 3.0 - r - j * pz for j in range(nz)]                 # itici ürünü öne dayar: robot hep öndekini alır
        y0 = kc + 1.0
        for i in range(nx + 1):
            xd = xm + (i - nx / 2.0) * px
            ekle("%s_serit_bolmesi_%d" % (kod, i), kut(xd - 0.5, xd + 0.5, y0, y0 + 50.0, iz0, iz1), "plastik", kod, grup=G,
                 bom=("Şerit bölmesi + yaylı itici takımı (market tipi)", nx, "standart raf itici sistemi · şerit %.0f · ürünü öne iter" % px,
                      "marka seçilmedi [VARSAYIM] · çekmece başına %d şerit" % nx) if i == 0 else None)
        zb = Z[-1] - r - 3.0
        for i, a in enumerate(X):
            ekle("%s_itici_%d" % (kod, i), kut(a - px / 2.0 + 4.0, a + px / 2.0 - 4.0, y0, y0 + (45.0 if tat else 70.0), zb - 12.0, zb), "plastik", kod, grup=G)
            ekle("%s_itici_yayi_%d" % (kod, i), kut(a - 6.0, a + 6.0, y0 + 2.0, y0 + 8.0, iz0, zb - 12.0), "celik", kod, grup=G)
        urun = sily(0.0, 0.0, r, 0.0, hk)
        n = 0
        for a in X:
            for b in Z:
                ekle("%s_%s_%d" % (kod, "tatli" if tat else "kutu330", n), urun.translate((a, y0, b)), "hamur" if tat else "kutu_icecek", kod, grup=G); n += 1
        return n, y0 + hk, y1
    r = ICECEK["r"]; ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_TUB1 - 13.0
    nx = int((ix1 - ix0 - 12.0 - 2 * r) // ICECEK["ax"]) + 1
    nz = int((iz1 - iz0 - 19.0 - 2 * r) // ICECEK["az"]) + 1
    X = [(ix0 + ix1) / 2.0 + (i - (nx - 1) / 2.0) * ICECEK["ax"] for i in range(nx)]
    Z = [iz1 - 6.0 - r - j * ICECEK["az"] for j in range(nz)]
    kat0 = kc + 1.0
    kat1 = kat0 + ICECEK_KAT + 1.0 + 1.5
    ekle(kod + "_ara_raf_1.5", kut(ka + 1.0, kb - 1.0, kat1 - 1.5, kat1, Z_TUB0 + 1.0, Z_TUB1 - 1.0), "sac", kod, grup=G)
    kutu = sily(0.0, 0.0, r, 0.0, ICECEK_KAT)
    n = 0
    for k_, yk in enumerate((kat0, kat1)):
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(r + 1.0).extrude(-4.0).translate((0, yk + 44.0, 0))
        ekle("%s_hizalama_saci_%d" % (kod, k_), kut(ix0, ix1, yk + 44.0, yk + 45.5, iz0, iz1).cut(cuk), "sac", kod, grup=G)
        for a in X:
            for b in Z:
                ekle("%s_kutu330_%d_%d" % (kod, k_, n), kutu.translate((a, yk, b)), "kutu_icecek", kod, grup=G); n += 1
    return n, kat1 + ICECEK_KAT, y1


def kasa():
    B = "B_KASA"
    ekle("plint_on_1.5", kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0), "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride", ""))
    for i, (ax, az) in enumerate([(60.0, -110.0), (W_B - 60.0, -110.0), (60.0, -760.0), (W_B - 60.0, -760.0), (W_B / 2.0, -110.0), (W_B / 2.0, -760.0)]):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", B,
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 6, "paslanmaz AISI 304 · taban Ø40 · yükseklik 123 (v4)", "elesa-ganter.com LV.A-SST · 123'e uygun diş boyu katalogdan seçilecek") if i == 0 else None)
    W_ = W_B
    for ad_, dis_x, pu_x, ic_x, don_x in (("sol", (0.0, 1.5), (1.5, 29.0), (29.0, 30.0), (1.5, 30.0)),
                                          ("sag", (W_ - 1.5, W_), (W_ - 29.0, W_ - 1.5), (W_ - 30.0, W_ - 29.0), (W_ - 30.0, W_ - 1.5))):
        ekle("yan_dis_sac_" + ad_, kut(dis_x[0], dis_x[1], Y_PLINT, H_B, -DZ, -40.0), "sac", B, bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · ön kenar kapak arkasında (z −40)", "") if ad_ == "sol" else None)
        ekle("yan_pu_" + ad_, kut(pu_x[0], pu_x[1], Y_PLINT + 1.5, H_B - 1.5, -DZ + 1.5, -41.5), "pu", B)
        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN if ad_ == "sol" else Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, -41.5), "sac", B)   # v4: sağda K4 sıcak bölmesinin tabanına iner
        ekle("yan_on_donus_" + ad_, kut(don_x[0], don_x[1], Y_PLINT + 1.5, H_B - 1.5, -41.5, -40.0), "sac", B)
    ekle("tavan_dis_sac", kut(1.5, W_ - 1.5, H_B - 1.5, H_B, -DZ, -40.0), "sac", B, bom=("Tavan dış sacı", 1, "304 1,5 · A ve C bunun üstüne oturur", ""))
    ekle("tavan_pu_57.5", kut(29.0, W_ - 29.0, Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -41.5), "pu", B, bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 27,5 · tavan 57,5 · arka 37,5 · taban 39"))
    ekle("tavan_ic_sac", kut(X_IC0, X_IC1, Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5), "sac", B)
    ekle("tavan_on_donus", kut(X_IC0, X_IC1, Y_TAVAN, H_B - 1.5, -41.5, -40.0), "sac", B)
    # K4 alt bölmesi SICAK (yoğuşturucu): tabanı delik, sıcak hava plinte çıkar
    VENT = (K4X + 60.0, K4X + K4W - 60.0, -500.0, -120.0)
    ekle("taban_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0).cut(kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3])), "sac", B)
    # v4: yalıtımlı taban yalnız K1–K3 (soğuk kolonlar) altında; K4 sıcak bölmesinde taban = dış sac (delikli), PU yok → kovan gereksiz
    ekle("taban_pu", kut(29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -41.5), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), "sac", B)
    ekle("taban_k4_kademe_saci", kut(K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -41.5), "sac", B,
         bom=("Taban kademe sacı 1,0", 1, "304 · yalıtımlı tabanın K4 tarafındaki ucunu kapatır", "v4: K4 sıcak bölmesi 40 mm alçak"))
    ekle("taban_on_donus", kut(X_IC0, X_IC1, Y_PLINT + 1.5, Y_TABAN, -41.5, -40.0), "sac", B)
    ekle("arka_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), "sac", B)
    ekle("arka_pu_37.5", kut(29.0, W_ - 29.0, Y_TABAN - 1.0, Y_TAVAN + 1.0, -DZ + 1.5, Z_ARKA - 1.0), "pu", B)
    ekle("arka_ic_sac", kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)
    # v4: K4 sıcak bölmesi tabana kadar iner → arka PU ve iç sac orada da tabana iner
    ekle("arka_pu_k4_alt", kut(K4X - 1.0, W_ - 29.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, Z_ARKA - 1.0), "pu", B)
    ekle("arka_ic_sac_k4_alt", kut(K4X, X_IC1, Y_PLINT + 1.5, Y_TABAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)
    # kolon bölmeleri 35 sandviç — üst arka köşede KABLO GEÇİŞİ (40 × 25)
    GECIS = lambda x0_: kut(x0_ - 1, x0_ + BOLME + 1, KAN_UST[0], KAN_UST[1] + 1, KAN_Z[0] - 1, KAN_Z[1])
    bx = [KOLON_X[k] + WO for k in KOLON_AD]
    for i, x0_ in enumerate(bx):
        g_ = GECIS(x0_)
        ekle("bolme_%d_sac_a" % i, kut(x0_, x0_ + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0).cut(g_), "sac", B)
        ekle("bolme_%d_pu" % i, kut(x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0).cut(g_), "pu", B)
        ekle("bolme_%d_sac_b" % i, kut(x0_ + BOLME - 1.0, x0_ + BOLME, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0).cut(g_), "sac", B)
    E = "B_ELEKTRIK"                                                 # v5: pano K4'te, Secop'un arkasında (aşağıda)
    # KABLO KANALLARI: her kolonda arka sol dikey 40 × 25 · üstte yatay (bölmelerden geçer)
    Kb = "B_KABLO"
    for kol in KOLON_AD:
        cx = KOLON_X[kol]
        ekle("kablo_kanali_%s" % kol, kut(cx + KAN_X[0], cx + KAN_X[1], Y_TABAN, KAN_UST[0], KAN_Z[0], KAN_Z[1]),
             "kanal", Kb, bom=("Kablo kanalı 40 × 25", 4 + 1, "PVC perfore + kapak", "dikey her kolonda + üstte yatay") if kol == "K1" else None)
    K4KAN = kut(K4X + KAN_X[0], K4X + KAN_X[1], 400.0, KAN_UST[0], KAN_Z[0], KAN_Z[1])            # v5 · PLC'den yukarı
    ekle("kablo_kanali_K4", K4KAN, "kanal", Kb)
    ekle("kablo_kanali_ust", kut(K1X + KAN_X[1], K4X + KAN_X[1], KAN_UST[0], KAN_UST[1], KAN_Z[0], KAN_Z[1]), "kanal", Kb)
    # EVAPORATÖR (roll-bond, arka duvarda) + FAN (ebm-papst 4414 FNH), motor ve kanal bandının dışında
    for kol in ("K1", "K2", "K3"):
        cx = KOLON_X[kol]
        e0, e1 = (300.0, 950.0)                                              # v5: K1'in üstünde teknik bölme yok
        ekle("evaporator_%s" % kol, kut(cx + 250.0, cx + 560.0, e0, e1, Z_ARKA, Z_ARKA + 2.0), "aluminyum", "B_SOGUTMA",
             bom=("Evaporatör roll-bond levha", 4, "alüminyum 1,5 + kanal · ölçüye üretim", "arka duvara yapışık · K1–K3 310 × 650 · K4 140 × 260") if kol == "K1" else None)
        fy0 = (e0 + e1) / 2.0 - 59.5
        ekle("fan_%s" % kol, kut(cx + 345.0, cx + 464.0, fy0, fy0 + 119.0, Z_ARKA + 3.0, Z_ARKA + 28.0), "motor", "B_SOGUTMA",
             bom=("Fan ebm-papst 4414 FNH", 4, "24 V · 119 × 119 × 25", "evaporatör önünde, havayı kolon içine basar") if kol == "K1" else None)
    # v5 · K4 soğuk bölmesi (depo + dar çekmeceler) de soğutulur
    ekle("evaporator_K4", kut(K4X + 240.0, K4X + 380.0, 700.0, 960.0, Z_ARKA, Z_ARKA + 2.0), "aluminyum", "B_SOGUTMA")
    ekle("fan_K4", kut(K4X + 255.0, K4X + 374.0, 770.5, 889.5, Z_ARKA + 3.0, Z_ARKA + 28.0), "motor", "B_SOGUTMA")
    # K4: soğutma grubu (SICAK bölme) + kaşar/sucuk deposu + temizlik nişi
    kx0, kx1 = K4X, K4X + K4W
    CU = (350.0, 272.0, 450.0)
    cx0, cy0, cz1 = kx0 + 25.0, Y_PLINT + 1.5 + 4.0, Z_CER0 - 10.0            # v4: ünite sıcak bölmenin tek sac tabanında (128,5)
    ekle("sogutma_grubu_taban", kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz1 - CU[2], cz1), "motor", "B_SOGUTMA",
         bom=("Yoğuşturucu ünite Secop CU KLF4.0CND R290", 1, "314H6008 · 335 W @ −10/25 °C · 1/6 HP · 15,2 kg", "272 × 350 × 450 · secop.com datasheet"))
    ekle("sogutma_grubu_kondenser", kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + 15.0, cy0 + CU[1], cz1 - 60.0, cz1), "bakir", "B_SOGUTMA")
    ekle("sogutma_grubu_fan", silz(cx0 + CU[0] / 2.0, cy0 + 15.0 + 125.0, 115.0, cz1 - 90.0, cz1 - 62.0), "motor", "B_SOGUTMA")
    ekle("sogutma_grubu_kompresor", sily(cx0 + CU[0] / 2.0, cz1 - 310.0, 85.0, cy0 + 15.0, cy0 + 15.0 + 162.0), "koyu", "B_SOGUTMA")
    s0 = cy0 + CU[1] + 8.0
    ekle("k4_ara_sac_alt", kut(kx0, kx1, s0, s0 + 1.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, kx1, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0).cut(K4KAN), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, kx1, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    # v5 · PANO Secop'un ARKASINDA (K1 üstünden taşındı) · sıcak havadan ara sac perdeyle ayrılır
    ekle("k4_ara_perde", kut(kx0, kx1, Y_PLINT + 1.5, s0, -522.0, -521.0), "sac", "B_SOGUTMA",
         bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında", "yoğuşturucu havası panoya gelmez"))
    ZP = Z_ARKA + 2.0                                                  # montaj plakası arka duvarda, öne bakar
    ekle("pano_montaj_plakasi", kut(kx0 + 10.0, kx1 - 10.0, 132.0, 398.0, Z_ARKA, ZP), "sac", E, bom=("Pano montaj plakası 2 mm", 1, "galvaniz", "K4 · Secop'un arkasında"))
    for i_, yr in enumerate((177.5, 312.5)):
        ekle("din_ray_%d" % i_, kut(kx0 + 12.0, kx1 - 12.0, yr, yr + 35.0, ZP, ZP + 7.5), "celik", E, bom=("DIN ray TS35 × 7,5", 2, "", "") if i_ == 0 else None)
    zd = ZP + 7.5
    x = kx0 + 14.0; ty = 145.0
    ekle("plc_S7-1200_1214C", kut(x, x + 110.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · 14 DI · 10 DQ · PROFINET/Modbus TCP", "110 × 100 × 75")); x += 110.0
    for ad_, kodu in (("SM1221_DI16_a", "6ES7221-1BH32-0XB0"), ("SM1221_DI16_b", "6ES7221-1BH32-0XB0"), ("SM1222_DQ16", "6ES7222-1BH32-0XB0")):
        ekle("plc_" + ad_, kut(x, x + 45.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
             bom=("PLC genişleme %s" % ad_.split("_")[0] + " " + ad_.split("_")[1], 1, kodu, "45 × 100 × 75 · 50 reed + 25 röle")); x += 45.0
    x += 4.0
    ekle("guc_kaynagi_NDR-240-24", kut(x, x + 63.0, 132.5, 257.7, zd, zd + 113.5), "aluminyum", E,
         bom=("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · DIN", "63 × 125,2 × 113,5"))
    x = kx0 + 14.0; ty = 285.0
    ekle("surucu_EM-324C", kut(x, x + 72.0, ty, ty + 85.0, zd, zd + 60.0), "kart", E,
         bom=("DC motor sürücü Electromen EM-324C + DIN taban", 1, "10–35 V · 4 A · akım sınırı · NPN/PNP", "72 genişlik taban [yükseklik/derinlik VARSAYIM]")); x += 76.0
    for i in range(len(CEK)):
        ekle("role_%02d" % (i + 1), kut(x + i * 6.2, x + i * 6.2 + 6.0, ty + 5.0, ty + 85.0, zd, zd + 94.0), "kart", E,
             bom=("Seçici röle Phoenix Contact PLC-RSC-24DC/21", len(CEK), "6,2 mm · 1 değiştirici · 24 V bobin", "hangi çekmecenin motoru sürücüye bağlanacak [boyut VARSAYIM]") if i == 0 else None)
    x += len(CEK) * 6.2 + 4.0
    ekle("klemens_blogu", kut(x, kx1 - 14.0, ty + 15.0, ty + 70.0, zd, zd + 45.0), "plastik", E,
         bom=("Klemens bloğu", 1, "Phoenix UT 2,5 · 25 motor + 50 sensör + güç", "kalan genişlik"))
    d0 = s0 + 30.0; d1 = d0 + GN_H
    # v5 · KAŞAR + SUCUK DEPOSU (4 günün 2. yarısı): GN 1/1-100 (kaşar blok) · raf · GN 1/2-100 (küp sucuk)
    g0 = d0 + 5.0
    ekle("k4_depo_GN11_100", kut(kx0 + 37.5, kx1 - 37.5, g0, g0 + 100.0, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g0 + 1.0, g0 + 101.0, Z_CER0 - 539.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/1-100 kap + kapak", 1, "304 · EN 631 · 530 × 325 × 100", "kaşar blok 2 gün = 8,8 kg (yoğunluk VARSAYIM)"))
    ekle("k4_depo_raf", kut(kx0, kx1, g0 + 110.0, g0 + 111.5, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_DEPO")
    g1 = g0 + 116.5
    ekle("k4_depo_GN12_100", kut(kx0 + 37.5, kx1 - 37.5, g1, g1 + 100.0, Z_CER0 - 275.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g1 + 1.0, g1 + 101.0, Z_CER0 - 274.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/2-100 kap + kapak", 1, "304 · EN 631 · 325 × 265 × 100", "küp sucuk 2 gün = 2,8 kg"))
    KAP = [("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False), ("k4_kapak_depo", s0 + 15.0, d1 + 1.0, "B_DEPO", True)]
    PENCERE = (kx0 + 20.0, kx1 - 20.0, Y_TABAN + 23.0, s0 - 8.0)
    for ad_, y0_, y1_, bir, fit in KAP:
        a_, b_ = KAPAK_X["K4"]                                        # v5 · tam kaplama
        if not fit:                                                   # sıcak bölme: yalıtımsız, fitilsiz, ızgaralı
            ds = kut(a_, b_, y0_, y1_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
            ekle(ad_ + "_dis_sac", ds.cut(kut(PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3], Z_ON0 - 1, Z_ON1 + 1)), "sac", bir,
                 bom=("Yoğuşturucu bölmesi kapağı", 1, "304 1,5 · yalıtımsız · ızgaralı hava penceresi", "hava önden girer, tabandan plinte çıkar"))
            continue
        kapak_on(ad_, a_, b_, y0_, y1_, bir, (kx0, kx1, y0_ + BIND, y1_ - BIND))
    for i in range(int((PENCERE[3] - PENCERE[2] - 14.0) // 16.0)):       # (ızgara penceresi aynı)
        gy = PENCERE[2] + 7.0 + i * 16.0
        ekle("k4_izgara_%02d" % i, kut(PENCERE[0], PENCERE[1], gy, gy + 8.0, Z_ON1 - 1.5, Z_ON1), "izgara", "B_SOGUTMA")
    # v5: K1 teknik kapağı ve K2 üst paneli yok — her kolonun en üst çekmece önü 1057'ye kadar kaplar
    # ön çerçeve sacı 1,0: bütün açıklıklar kesik
    cer = kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_CER0, Z_CER1)
    for kol, kod, tip, x0, yo in CEK:
        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))
    for _a, y0_, y1_, _b, _f in KAP:
        cer = cer.cut(kut(kx0, kx1, y0_ + BIND, y1_ - BIND, Z_CER0 - 1, Z_CER1 + 1))
    ekle("on_cerceve_saci_1.0", cer, "sac", B, bom=("Ön çerçeve sacı 1,0", 1, "304 lazer kesim · %d açıklık" % (len(CEK) + 2), "fitil buna basar"))
    return s0, d0, d1


def modul():
    PARCALAR[:] = []
    k4 = kasa()
    ozet = []
    for kol, kod, tip, x0, yo in CEK:
        n, ust, acik_ust = cekmece(kol, kod, tip, x0, yo)
        ozet.append((kod, tip, n, ust, acik_ust))
    return ozet


def denetim(ozet, tarama=True):
    print("B CEKMECE MODULU v5 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))
    # v4 · ALT TABAN ÇİZGİSİ (katılardan ölçülür)
    yb = lambda ad: [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    alt = yb("taban_dis_sac").ymin
    ic_ust = yb("taban_ic_sac").ymax
    on_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if p["ad"].endswith("_on_dis_sac_1.5") and p["grup"] == "CEKMECE")
    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin
    govde_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    print("ALT TABAN CIZGISI: govde alti %.1f (en alcak govde parcasi %.1f) · ic taban ustu %.1f · en alt on %.1f · K4 kapagi alti %.1f"
          % (alt, govde_alt, ic_ust, on_alt, k4_alt))
    assert abs(alt - 123.0) < 0.05 and abs(govde_alt - alt) < 0.05, "govde alti 123 degil"
    assert abs(on_alt - ON_ALT) < 0.05 and abs(k4_alt - ON_ALT) < 0.05, "on alt kenarlari 126 cizgisinde degil"
    # v5 · ÖN YÜZ IZGARASI: her kolonda önler 126 → 1057 arası 3 mm aralıkla kesintisiz; kolonlar arası 3 mm
    on = [p["wp"].val().BoundingBox() for p in PARCALAR if p["ad"].endswith(("_dis_sac_1.5", "_dis_sac")) and ("CEK_" in p["ad"] or p["ad"].startswith("k4_kapak"))]
    for kol, (pa, pb) in KAPAK_X.items():
        sut = sorted((b for b in on if abs(b.xmin - pa) < 0.05 and abs(b.xmax - pb) < 0.05), key=lambda b: b.ymin)
        assert sut and abs(sut[0].ymin - ON_ALT) < 0.05 and abs(sut[-1].ymax - ON_UST) < 0.05, "%s: on yuz 126-1057 degil" % kol
        for u_, v_ in zip(sut, sut[1:]):
            assert abs(v_.ymin - u_.ymax - FUGA) < 0.05, "%s: onler arasi %.1f (3 olmali)" % (kol, v_.ymin - u_.ymax)
        print("   ON YUZ %s: x %.1f-%.1f · %d parca · %.0f-%.0f · aralar 3" % (kol, pa, pb, len(sut), sut[0].ymin, sut[-1].ymax))
    xs = sorted(KAPAK_X.values())
    assert all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and xs[0][0] == 0.0 and xs[-1][1] == W_B, "kolon onleri arasi 3 degil"
    # v3 · RAY: tam açıkta elemanlar birbirinin içinde kalıyor mu, kutu iç elemana boyunca bağlı mı? (katılardan ölçülür)
    en = dict(b1=1e9, b2=1e9, bag=1e9)
    for kod, tip, _n, _u, _a in ozet:
        for yan in ("sol", "sag"):
            zr = {}
            for el in ("dis", "ara", "ic"):
                bb = [p for p in PARCALAR if p["ad"] == "%s_ray_%s_%s" % (kod, el, yan)][0]["wp"].val().BoundingBox()
                k = {"dis": 0.0, "ara": RAY_ARA_ORAN, "ic": 1.0}[el] * STROK
                zr[el] = (bb.zmin + k, bb.zmax + k)
            ad_ = [p for p in PARCALAR if p["ad"] == "%s_ray_adaptor_%s" % (kod, yan)][0]["wp"].val().BoundingBox()
            b1 = min(zr["dis"][1], zr["ara"][1]) - max(zr["dis"][0], zr["ara"][0])          # dış ↔ ara boyuna örtüşme
            b2 = min(zr["ara"][1], zr["ic"][1]) - max(zr["ara"][0], zr["ic"][0])            # ara ↔ iç
            bag = min(zr["ic"][1], ad_.zmax + STROK) - max(zr["ic"][0], ad_.zmin + STROK)     # iç eleman ↔ kutu adaptör lamı
            assert b1 >= 250.0 and b2 >= 250.0, "%s %s: ray bindirmesi yetersiz (%.0f / %.0f)" % (kod, yan, b1, b2)
            assert bag >= ad_.zlen - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / %.0f)" % (kod, yan, bag, ad_.zlen)
            en = dict(b1=min(en["b1"], b1), b2=min(en["b2"], b2), bag=min(en["bag"], bag))
    print("RAY (3 elemanli teleskop, %d cekmece x 2 yan, tam acik strok %.0f): en az dis-ara bindirme %.0f mm · ara-ic %.0f mm · kutu-ic ray bagi %.0f mm · ara eleman +%.0f"
          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK))
    for kod, tip, n, ust, acik in ozet:
        assert acik - ust >= 2.0, "%s: icerik aciklik ustune %.1f mm kaliyor" % (kod, acik - ust)
    tipler = sorted({t for _k, t, _n, _u, _a in ozet})
    pay = {t: min(a - u for _k, tt, _n, u, a in ozet if tt == t) for t in tipler}
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t in ("ic1", "ic1d")); tat = sum(n for _k, t, n, _u, _a in ozet if t == "tatli")
    print("ICERIK PAYI (acikliga): " + " · ".join("%s %.1f" % (t, pay[t]) for t in tipler) + " mm")
    print("KAPASITE: pide %d top (2 gun = 160) · lahmacun %d top (2 gun = 400) · icecek %d kutu TEK KAT (2 gun = 139) · tatli %d (4 gun = 22)" % (pide, lahm, ice, tat))
    assert pide >= 160 and lahm >= 400 and ice >= 139 and tat >= 22
    ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "CEKMECE" and "_on_" not in p["ad"])
    print("EN UST CEKMECE ICERIGI/KUTUSU %.1f · tavan %.1f" % (ust, Y_TAVAN)); assert ust <= Y_TAVAN - 2.0
    hiz = 127.0 / 60.0 * math.pi * KAS_PD
    print("TAHRIK: PD3665-24-51 127 d/dk × GT3 30 dis (cevre %.1f) = %.0f mm/s · strok %.0f -> %.1f sn · surekli kuvvet %.0f N (0,853 N·m / r %.2f)"
          % (math.pi * KAS_PD, hiz, STROK, STROK / hiz, 0.853 / (KAS_PD / 2000.0), KAS_PD / 2.0))
    for tip in TOP:
        t = TOP[tip]; z_tub0 = Z_CON0 - 2.0 - TUB[tip]
        arka = z_tub0 + 5.0 + t["td"] / 2.0 - (t["nz"] - 1) / 2.0 * t["az"]
        kenar = arka + STROK - t["R"]
        print("   %s: acilinca arka sira topun arka kenari z %+.0f (on yuz 0)" % (tip, kenar))
        assert kenar >= 5.0
    if tarama:
        cakisma()


def _kesis(L1, L2, esik, ayni=True):
    bul, aday = [], 0
    for i, (p, a, A) in enumerate(L1):
        rng = L2[i + 1:] if ayni else L2
        for q, b, Bb in rng:
            if A.xmin >= Bb.xmax - 0.05 or Bb.xmin >= A.xmax - 0.05 or A.ymin >= Bb.ymax - 0.05 or Bb.ymin >= A.ymax - 0.05 or A.zmin >= Bb.zmax - 0.05 or Bb.zmin >= A.zmax - 0.05:
                continue
            aday += 1
            v = a.intersect(b).Volume()
            if v > esik:
                bul.append((v, p["ad"], q["ad"]))
    return sorted(bul, reverse=True), aday


def cakisma(esik=1.0):
    import time as _t
    t0 = _t.time()
    L = [(p, p["wp"].val()) for p in PARCALAR if "_top_" not in p["ad"] and "_kutu330_" not in p["ad"] and "_tatli_" not in p["ad"]]
    L = [(p, v, v.BoundingBox()) for p, v in L]
    bul, aday = _kesis(L, L, esik)
    print("CAKISMA TARAMASI (kapali): %d parca · %d aday · %d gercek kesisim (> %.0f mm3) · %.0f sn" % (len(L), aday, len(bul), esik, _t.time() - t0))
    import re as _re
    tur = {}
    for v, a, b in bul:
        k = tuple(sorted(_re.sub(r"^CEK_K\d_[a-z]+_\d+_", "", x) for x in (a, b)))
        tur[k] = tur.get(k, 0) + 1
    for k, n in sorted(tur.items(), key=lambda kv: -kv[1])[:30]:
        print("    TUR %3d x  %s  <->  %s" % (n, k[0], k[1]))
    for v, a, b in bul[:40]:
        print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
    assert not bul, "kapali konumda %d cakisma" % len(bul)
    # v3: çekmece (strok) + ray ara elemanı (strok × RAY_ARA_ORAN) birlikte gider; yol boyunca 4 konum taranır,
    #     hareketli ↔ hareketli de (kutu/iç ray ile ara ray farklı hızda)
    HAR = {"CEKMECE": 1.0, "CEKMECE_ARA": RAY_ARA_ORAN}
    S = [(p, v, Bb) for p, v, Bb in L if p["grup"] not in HAR]
    for oran in (0.25, 0.5, 0.75, 1.0):
        t0 = _t.time()
        H = [(p, v.translate(cq.Vector(0.0, 0.0, STROK * oran * HAR[p["grup"]]))) for p, v, _B in L if p["grup"] in HAR]
        H = [(p, v, v.BoundingBox()) for p, v in H]
        bul, aday = _kesis(H, S, esik, ayni=False)
        bul2, aday2 = _kesis([h for h in H if h[0]["grup"] == "CEKMECE"], [h for h in H if h[0]["grup"] == "CEKMECE_ARA"], esik, ayni=False)
        bul += bul2
        print("ACIK KONUM TARAMASI (strok %.0f x %.2f, ara ray x %.2f): %d hareketli x %d sabit · %d aday · %d gercek kesisim · %.0f sn"
              % (STROK, oran, oran * RAY_ARA_ORAN, len(H), len(S), aday + aday2, len(bul), _t.time() - t0))
        for v, a, b in bul[:40]:
            print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
        assert not bul, "acik konumda %d cakisma" % len(bul)


def _kalem(p):
    """parcanin siparis/imalat kalemi: BOM tanimi varsa o; yoksa adindan cekmece oneki ve sira no atilir, olcu eklenir"""
    import re as _re
    if p["bom"]:
        return p["bom"][0], p["bom"][1], p["bom"][2], p["bom"][3]
    bb = p["wp"].val().BoundingBox()
    olcu = "%.1f × %.1f × %.1f" % (bb.xlen, bb.ylen, bb.zlen)
    ad = _re.sub(r"^CEK_K\d_[a-z]+_\d+_", "", p["ad"])
    ad = _re.sub(r"_(\d+|sol|sag|a|b)$", "", ad)
    tanim = {"sac": "304 sac · lazer + büküm", "pu": "PU köpük (gövdeyle birlikte enjeksiyon)", "celik": "304 · lazer / lama",
             "aluminyum": "alüminyum", "koyu": "", "plastik": "", "conta": "", "kanal": "PVC", "kart": "", "motor": "", "silikon": "gıda silikonu",
             "bakir": "", "izgara": "304 lama", "pom": ""}.get(p["mal"], p["mal"])
    return ad.replace("_", " "), 1, tanim, "zarf " + olcu


# satin alinan urunun ALT GOVDELERI ve ayni kalemin ikinci ornekleri: BOM.csv'de listelenir, OZET'te SAYILMAZ
# (adet zaten ana kalemde: ray "2 / cekmece", reed "2 / cekmece", role "21", fan "3" ...)
ALT_KURAL = [
    (r"_on_(pu|ic_sac_1\.0)$", "çekmece önü / kapak katmanı"), (r"^(k4_kapak_(depo|nis)|k1_teknik_kapak|k2_ust_panel)_(pu|ic_sac_1\.0)$", "kapak katmanı"),
    (r"_kutu_(arka|on)_1\.0$", "çekmece kutusu"), (r"_on_baglanti_sag$", "ön bağlantı köşesi"), (r"_ray_adaptor_sag$", "ray adaptör lamı"),
    (r"_ray_dis_sag$", "Accuride DZ3832-0070"), (r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç eleman)"), (r"_ray_ara_(sol|sag)$", "Accuride DZ3832-0070 (ara eleman)"), (r"_reed_acik$", "Littelfuse 59135"),
    (r"_motor_(mili|gobegi|govde)$", "Transmotec PD3665"), (r"_enkoder_kapagi$", "Transmotec PD3665"),
    (r"^role_(0[2-9]|1\d|2\d)$", "Phoenix PLC-RSC"), (r"^kablo_kanali_(K2|K3|ust)$", "kablo kanalı"), (r"^evaporator_K[23]$", "roll-bond evaporatör"),
    (r"^fan_K[234]$", "ebm-papst 4414 FNH"), (r"^evaporator_K4$", "roll-bond evaporatör"), (r"^ayak_[1-5]$", "Elesa LV.A-SST"), (r"^din_ray_1$", "DIN ray"),
    (r"_serit_bolmesi_([1-9]|1\d)$", "şerit + itici takımı"), (r"_itici(_yayi)?_\d+$", "şerit + itici takımı"), (r"^kablo_kanali_K4$", "kablo kanalı"),
    (r"^sogutma_grubu_(kondenser|fan|kompresor)$", "Secop CU KLF4.0CND"), (r"^plc_SM1221_DI16_b$", "SM1221"), (r"^yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)"),
    (r"^(yan_pu_(sol|sag)|arka_pu_37\.5|arka_pu_k4_alt|taban_pu|bolme_\d_pu|k1_teknik_raf_pu_38|k4_ara_pu)$", "PU köpük gövde"),
]


def _alt(ad):
    import re as _re
    for kural, ana in ALT_KURAL:
        if _re.search(kural, ad):
            return ana
    return None


def bom_yaz(klasor):
    """BOM.csv = modeldeki HER parca (icerik haric) · BOM_OZET.csv = kalem bazinda toplam (siparis/imalat listesi)"""
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, "BOM.csv")
    satir = []
    for p in PARCALAR:
        if "_top_" in p["ad"] or "_kutu330_" in p["ad"] or "_tatli_" in p["ad"]:
            continue
        if not p["bom"] and any(p["ad"] == q["ad"] for q in PARCALAR if q is not p and q["bom"]):
            continue
        ad, adet, tanim, not_ = _kalem(p)
        ana = _alt(p["ad"])
        if ana:
            satir.append((p["ad"], ad, 0, tanim, "alt gövde → " + ana, p["birim"], "ALT"))
            continue
        satir.append((p["ad"], ad, adet, tanim, not_, p["birim"], _tur(ad) if p["bom"] else "ÜRETİM"))
    with io.open(yol, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["parça (model adı)", "kalem", "adet", "tanım / ürün", "not / ölçü", "birim", "tür"])
        for r_ in satir:
            w.writerow(r_)
    top, bilgi, tur = {}, {}, {}
    for pad, ad, adet, tanim, not_, bir, t in satir:
        if t == "ALT":
            continue
        # BOM tanimi olan kalemlerde adet "cekmece basina" verildi; tanimsiz parcalar tek tek sayilir
        top[ad] = top.get(ad, 0) + (int(adet) if str(adet).isdigit() else 1)
        bilgi.setdefault(ad, (tanim, not_)); tur[ad] = t
    with io.open(os.path.join(klasor, "BOM_OZET.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["tür", "kalem", "toplam adet", "tanım / ürün", "not / ölçü"])
        for ad in sorted(top, key=lambda a: (0 if tur[a] == "SATIN ALMA" else 1, a)):
            w.writerow([tur[ad], ad, top[ad], bilgi[ad][0], bilgi[ad][1]])
    print("BOM: %d parca satiri · %d kalem (%d satin alma · %d uretim)" % (len(satir), len(top), sum(1 for a in top if tur[a] == "SATIN ALMA"), sum(1 for a in top if tur[a] != "SATIN ALMA")))
    return yol


def _tur(ad):
    return "SATIN ALMA" if any(s in ad for s in ("Accuride", "Transmotec", "Littelfuse", "Siemens", "Mean Well", "Electromen", "Phoenix", "Secop", "ebm-papst", "Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC")) else "ÜRETİM"


if __name__ == "__main__":
    oz = modul(); denetim(oz)
    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v8")))
