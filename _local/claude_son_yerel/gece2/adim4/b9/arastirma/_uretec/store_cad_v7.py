# -*- coding: utf-8 -*-
"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v7 (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1 · Kemal: "öğrendiğin yeter,
    cooling'de de onlarla yap" · "hamur fırıncıdan soğuk gelemez")
v7: Secop CU NLE8.8CN (737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C; KLF4.0CND 32 °C'de 309 W, gereken 552–661 W) · 297 yüksek → K4 ara katman +25
    · 6 roll-bond levha + 7 × 4414 FNH KALKTI → 2 bölge × lamelli epoksi kaplı evaporatör + davlumbaz + 2 × ebm-papst 4414 FL (sol: K2 arkası → K1–K3 ·
    sağ: K5 arkası, tatlının altı → K4 depo + K5–K6) · bölmelerde arka hava geçişleri · damlama teknesi → Ø12 gider → plint → kondenser atış kanalında
    buharlaştırma tavası · fırın altında PU 60 yerine HAVA BOŞLUĞU + ayırma sacı + parlak paslanmaz ışınım sacı + arka yarıklar · sol yan PU 27,5 → 60.
    Önceki: store_cad_v6.py (yap_store_cad_v7.py) · BOM 1_STORE_v10
v6 (27 Eyl 2026) · ALÇAK HAT (SPEC_alcak_hat_v57.md · resim teknik_alcak_hat_resim1_v4
    + teknik_qr_tezgah_v4 · Kemal: "bu teknik resme göre 3D modelle, sitede her şeyi güncelle, kontrol et")
v6: TEK PARÇA DOLAP 0–4000 × 830 × 123–788 (+3 °C), üstü DÜZ 788 = A, C ve fırının altı. K1 6 lahmacun · K2 6 lahmacun · K3 5 pide ·
    K4 Secop (önde) + B panosu (arkada) + kaşar/sucuk deposu (v5 ile aynı; dar içecek YOK) · K5 fırın altı 3 pide + tatlı (2 şerit = 12) ·
    K6 fırın altı 3 içecek (48) · fırın altında PU 60 ısı kalkanı (2517–3793 × 728–788) → K5/K6 iç tavanı 668 · TAŞIYICI ÇERÇEVE (304 profil:
    2 kiriş + 3 çapraz ısı kalkanının içinde, 6 dikme B4/B5/B6 bölmelerinde, altlarında ayak) · ŞERİT 3810–4000 soğuk DEĞİL: ROBOT ÇÖPÜ
    15 L (poşetli, kızakta) + atma boşluğu + yaylı klape + servis kapağı · 6 evaporatör + 6 fan · 24 çekmece: pide 160 · lahmacun 432 ·
    içecek 144 · tatlı 12 (2 gün). Önceki: store_cad_v5.py (yap_store_cad_v6.py) · BOM 1_STORE_v9
v5 (25 Eyl 2026)
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
  sürücü  Electromen EM-324C (10–35 V, 4 A, akım sınırı) · seçici röle Phoenix Contact PLC-RSC-24DC/21 (6,2 mm) × 24 (v6: 24 çekmece)
  PLC     Siemens S7-1200 CPU 1214C DC/DC/DC 6ES7214-1AG40-0XB0 + 3 × SM1221 DI16 + SM1222 DQ16 (v6: 48 reed → 62 DI)
  güç     Mean Well NDR-240-24 (24 V 10 A)
  soğutma Secop CU NLE8.8CN R290 · 297 yüksek · 737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C (v7; v6 KLF4.0CND 272 yüksek, 309 W @ 32 °C yetmiyordu)
  fan     ebm-papst 4414 FL (119 × 119 × 25, 24 V, 1,2 W, 94 m³/h) · evaporatör: lamelli Cu/Al, epoksi kaplı (ölçüye üretim) — v7
  ayak    Elesa+Ganter LV.A-SST (paslanmaz) M12
KOORDİNAT: hat ile aynı — x 0..4000 (dolap), y 0..788 (düz çizgi), z 0 = çekmece ön yüzü, −830 arka.
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
# v6 · ALÇAK HAT (27 Eyl 2026 · SPEC_alcak_hat_v57): TEK PARÇA DOLAP 0–4000 · DÜZ ÇİZGİ 788 · soğukta TAM 2 gün:
#      pide 8 çekmece (160) · lahmacun 12 (432; 2 gün 400, 11 = 396 yetmez) · içecek 3 (144; 2 gün 139) · tatlı 1 × 2 şerit (12; 2 gün 11)
HH = dict(HH); HH.update({"ic1": 126.0, "ic1d": 126.0, "tatli": 71.0})       # kutu 115 / tatlı kabı 60 + 11 taban payı
KOLON_AD = ("K1", "K2", "K3", "K5", "K6")                                   # K4 çekmecesiz (Secop + pano + depo)
KOLON = [[(6, "lahm")], [(6, "lahm")], [(5, "hamur")], [(3, "hamur"), (1, "tatli")], [(3, "ic1")]]   # K5 alttan üste: pide, pide, pide, tatlı
KOLON_X = {"K1": XI, "K2": XI + (WO + BOLME), "K3": XI + 2.0 * (WO + BOLME), "K5": 2535.0, "K6": 3190.0}   # 62,5 · 717,5 · 1372,5 · 2535 · 3190 (SPEC)
KOLON_W = {"K6": 585.0}                                                     # K6 3190–3775 (SPEC) · diğerleri WO 620
K4_CEK = []                                                                 # v6: K4'te dar içecek YOK (SPEC)
KAPAK_X = {"K1": (0.0, 698.5), "K2": (701.5, 1353.5), "K3": (1356.5, 2008.5), "K4": (2011.5, 2516.0),
           "K5": (2519.0, 3171.0), "K6": (3174.0, 3791.0), "SERIT": (3794.0, 4000.0)}
# tam kaplama (v5 kuralı): her ön kendi açıklığının 16 dışına taşar, kolon önleri arası 3. SPEC'teki "K4 2011,5–2500" kolonun kendisi;
# K4 önü 2516'ya uzar ki K5 önü de 16 taşsın (2519 = 2535 − 16) — 2500'de bitseydi K5 önü solda 32 taşardı.
H_B, W_B, DZ = 788.0, 4000.0, _g["DZ"]          # v6: DÜZ ÇİZGİ 788 · dolap 0–4000 (pafta v7'deki H_B 1060 / W_B 2500 eski hattın)
ON_ALT, ON_UST = 126.0, H_B - 3.0               # bütün kolonlarda ön yüzün alt ve üst çizgisi: 126 · 785
GN_H = 230.0                                    # K4 kaşar + sucuk deposu yüksekliği (GN 1/1-100 + raf + GN 1/2-100) — v5 ile aynı
BOLME_X = (KOLON_X["K1"] + WO, KOLON_X["K2"] + WO, KOLON_X["K3"] + WO, 2500.0, KOLON_X["K5"] + WO, KOLON_X["K6"] + KOLON_W["K6"])
#           B1 682,5 · B2 1337,5 · B3 1992,5 · B4 2500 (K4 | K5) · B5 3155 · B6 3775 (K6 | şerit = soğuk zarfın sağ duvarı) — hepsi 35
SERIT = (BOLME_X[5] + BOLME, W_B)               # 3810–4000 · soğuk DEĞİL (robot çöpü)
X_F = (2517.0, 3793.0)                          # fırın altı ısı kalkanı x (SPEC) · fırın 2500–4000
FIRIN_CIKINTI = 79.0                            # firin_tp10_cad_v6 ZS: fırın gövdesi ön yüzün 79 önünde (y ≥ 788)

for _k, _v in {"sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32), "pu": ((0.93, 0.88, 0.72, 1.0), 0.0, 0.85),
               "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45), "kart": ((0.10, 0.35, 0.22, 1.0), 0.1, 0.6),
               "hamur": ((0.94, 0.86, 0.68, 1.0), 0.0, 0.9), "silikon": ((0.86, 0.30, 0.22, 1.0), 0.0, 0.7),
               "kutu_icecek": ((0.78, 0.10, 0.12, 1.0), 0.7, 0.35), "izgara": ((0.30, 0.32, 0.35, 1.0), 0.6, 0.5),
               "conta": ((0.90, 0.90, 0.88, 1.0), 0.0, 0.8), "plastik": ((0.55, 0.57, 0.60, 1.0), 0.0, 0.6),
               "siemens": ((0.23, 0.36, 0.40, 1.0), 0.2, 0.5), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3),
               "bakir": ((0.72, 0.45, 0.20, 1.0), 0.9, 0.35), "kanal": ((0.55, 0.58, 0.62, 1.0), 0.0, 0.7),
               "poset": ((0.13, 0.13, 0.14, 1.0), 0.0, 0.8)}.items():
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
Y_TAVAN = H_B - 60.0                   # v6: 728 — K1–K4 iç tavanı (üst 60 = iç sac 1 + PU 57,5 + dış sac 1,5)
Y_TAVAN_F = Y_TAVAN - 60.0             # v6: 668 — fırın altı K5, K6: tavan 60 + ISI KALKANI PU 60 (728–788) = 120 → yığın sınırı L − 290
X_IC0, X_IC1 = 30.0, W_B - 30.0
KC = 5.0
KUTU_KENAR = 30.0                      # v2: 16 → 30. Ray (12,7) ile kutu arasında 17,3'lük YAN BANT — kayış burada (T4)
TEPSI_T, CUKUR_H = 10.0, 7.0
Y_OTUR = KC + 1.0 + TEPSI_T - CUKUR_H  # 9
TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=4, ax=105.0, az=130.0, td=520.0),
       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=6, ax=88.0, az=90.0, td=540.0)}
TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0, "ic1": 660.0, "ic1d": 660.0, "tatli": 660.0}
TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6, nx=2)    # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104 · v6: 2 şerit × 6 = 12 (2 gün 11)
# v6: K4_YO (K4 dar içecek çekmeceleri) kalktı
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
KAN_UST = (Y_TAVAN - 25.0, Y_TAVAN)            # v6: 703–728 · K1 → K4 yatay kanal
KAN_UST_F = (Y_TAVAN_F - 25.0, Y_TAVAN_F)      # v6: 643–668 · K4 → K6 (fırın altı) yatay kanal


def kolonlar():
    out = []
    for ki, gruplar in enumerate(KOLON):
        kol = KOLON_AD[ki]; cx = KOLON_X[kol]
        yo, n = YUZ0 + BIND, {}
        for adet, tip in gruplar:
            for _ in range(adet):
                n[tip] = n.get(tip, 0) + 1
                out.append((kol, "CEK_%s_%s_%d" % (kol, tip, n[tip]), tip, cx, yo))
                yo += HH[tip] + 2 * BIND + FUGA
    return out, BOLME_X[2] + BOLME                                        # v6: K4 = B3 bölmesinin sağı (2027,5)


CEK, K4X = kolonlar()
K4W = 400.0                                                               # Secop + pano + GN genişliği (v5 ile aynı)
K4_SAG = BOLME_X[3]                                                       # v6: K4 iç boşluğu B4 bölmesine (2500) kadar
GEN = lambda kol: K4W if kol == "K4" else KOLON_W.get(kol, WO)
ALT_KOD = {min((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in KOLON_AD}
UST_KOD = {max((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in KOLON_AD}
K1X = KOLON_X["K1"]
TAVAN_KOL = {k: (Y_TAVAN if k in ("K1", "K2", "K3") else Y_TAVAN_F) for k in KOLON_AD}          # iç tavan: 728 · fırın altı 668
YIGIN_SINIR = {k: (H_B - 230.0 if k in ("K1", "K2", "K3") else H_B - 290.0) for k in KOLON_AD}   # Σ(HH + 33), 167,5'ten: 558 · 498 (SPEC)
# v6 · TAŞIYICI ÇERÇEVE: fırın (TP10 1500, 79 öne) + fırın üstü raf yükü düz 788'in üstüne biner; PU sandviç taşıyıcı sayılmaz.
#      Dikmeler bölmelerin (35) ortasında → soğuk hacme girmez; kirişler ısı kalkanının içinde, dış tavan sacının hemen altında.
TD_X = tuple(BOLME_X[i] + BOLME / 2.0 for i in (3, 4, 5))          # 2517,5 · 3172,5 · 3792,5
TD_Z = (-110.0, -620.0)                                             # ön: plintin (−60) arkası · arka: fırın gövdesinin arka yüzünün (−651) önü
TK_Y = (H_B - 1.5 - 40.0, H_B - 1.5)                                # 746,5–786,5
TK_X = (TD_X[0] - 15.0, W_B - 3.5)                                  # 2502,5–3996,5 (fırın 2500–4000'in altı · sağ dış sacına 2)
TASIYICI = ([("tasiyici_kiris_%s" % ("on" if j == 0 else "arka"), (TK_X[0], TK_X[1], TK_Y[0], TK_Y[1], z_ - 20.0, z_ + 20.0), "x") for j, z_ in enumerate(TD_Z)]
            + [("tasiyici_capraz_%d" % i, (x_ - 15.0, x_ + 15.0, TK_Y[0], TK_Y[1], TD_Z[1] + 20.0, TD_Z[0] - 20.0), "z") for i, x_ in enumerate(TD_X)]
            + [("tasiyici_dikme_%d" % (2 * i + j), (x_ - 15.0, x_ + 15.0, Y_PLINT + 1.5, TK_Y[0], z_ - 15.0, z_ + 15.0), "y")
               for i, x_ in enumerate(TD_X) for j, z_ in enumerate(TD_Z)])
M_FIRIN = 200.0         # kg · uzatılmış TP10 1500 ≈ 200 (firin_tp10_cad_v6 VARSAYIM; katalog TP10 160 kg — büyüğü alındı)
M_RAF = 99.0            # kg · fırın üstü raf + 320 kutu + kompresör + kalkan (firin_tp10_cad_v6 RAF YÜKÜ)
ZG_FIRIN = (FIRIN_CIKINTI + (-730.0 + FIRIN_CIKINTI)) / 2.0         # −286 · gövde z +79…−651 ortası [VARSAYIM: ağırlık merkezi ortada]
ZG_RAF = (-420.0 - 15.0) / 2.0                                      # −217,5 · raf z −420…−15 ortası
EMN = 1.5               # yük katsayısı [VARSAYIM]
# v6 · ŞERİT 3810–4000 (soğuk DEĞİL) · ROBOT ÇÖPÜ (teknik_qr_tezgah_v4 · SPEC): robot yalnız yırtık / düşen / 48 saati geçen topu atar
KOVA = (3822.5, 3987.5, 126.0, 426.0, -420.0, -20.0)   # 165 × 300 × 400 (x · y · z) ≈ 15 L · SPEC 3822–3988 (166) ölçü 165 ile çelişiyor → 165 korundu, orta 3905 aynı
KOVA_T = 2.5                                             # PP duvar [VARSAYIM] · taban 3
SERIT_DONUS = 18.0                                       # şerit önlerinin kenar dönüşü (yalıtımsız) · kova önü −20'de 2 mm pay
SERIT_KAPI = (ON_ALT, 560.0)                             # servis kapağı: kova (126–426) öne çekilip çıkarılır
SERIT_PANEL = (563.0, ON_UST)                            # sabit üst panel (klape açıklıklı)
KLAPE_AC = (3840.0, 3970.0, 610.0, 740.0)                # klape açıklığı 130 × 130 [VARSAYIM: Ø95 pide topu + tutucu] · orta 3905 = kova ortası
KLAPE_EKSEN = (748.0, -7.0)                              # yaylı menteşe ekseni (y, z) — SPEC "klape y ~745" · klape bunun altında asılı
KLAPE_MAX = 90.0                                         # derece · içe (−z) açılır · mekanik stop (denetimde 30 / 60 / 90 taranır)
AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in (-110.0, -760.0)] + [(x_, z_) for x_ in TD_X for z_ in TD_Z]
           + [(W_B - 60.0, z_) for z_ in (-110.0, -760.0)])      # 14 · fırın altında dikmelerin tam altında · K4 hava deliğinin (2087,5–2367,5) dışında


# v7 · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1): 2 bölge × lamelli evaporatör + davlumbaz + 2 fan, bölmelerde arka hava geçişi
EVAP = {"sol": dict(kol="K2", y=(250.0, 650.0), gider=(1300.0, 2150.0)),       # K1–K3 · K2 çekmecelerinin arkası (kutu arkası −607)
        "sag": dict(kol="K5", y=(230.0, 495.0), gider=(2790.0, 2340.0))}       # K4 depo + K5–K6 · K5 pide arkası, tatlı kutusunun (511,5) altı
EV_Z = (-752.0, -667.0)          # lamelli blok 85 derin (4 sıra boru VARSAYIM) · arkasında 38 plenum (arka iç sac −790)
FAN_Z = (-641.0, -616.0)         # ebm-papst 4414 FL 25 kalın · lamel yüzüne 26 (rapor: ≥ 25) · K2 kutu arkası −607 → 9 pay
FAN_X = (270.5, 450.5)           # kolonun sol kenarından iki fanın sol kenarı (119 geniş)
HAVA_Z = (-788.0, -760.0)        # bölmelerdeki arka hava geçişi (plenum hizası; raylar −756'dan önde, motorlar kolonun içinde)
HAVA_GECIS = {0: ((190.0, 290.0), (560.0, 660.0)), 1: ((190.0, 290.0), (560.0, 660.0)),    # B1 · B2: K1 ↔ K2 ↔ K3 (sol bölge)
              3: ((480.0, 570.0), (590.0, 635.0)),                                      # B4: K4 depo ↔ K5 (ara katman 433,5–463,5'in üstü · raf 578,5)
              4: ((190.0, 290.0), (400.0, 490.0))}                                      # B5: K5 ↔ K6 · B3 (K3 | K4 sıcak bölme) KAPALI
DR_Z, DR_R, DR_Y = -700.0, 6.0, 75.0          # gider borusu Ø12: tabandan plinte iner, plintte y 75'te K4 altına gider
GIDER_UC_Z = -400.0                           # boru ucu atış kanalının içinde, tavanın üstünde (serbest damlama)
ATIS = (2085.5, 2369.5, 10.0, -502.0)         # kondenser atış kanalı (plintte): x · taban y · arka duvar z → önde plint ızgarası
TAVA = (2100.0, 2355.0, 11.5, 51.5, -480.0, -140.0)
PLINT_IZGARA = [(2095.0, 2360.0, 18.0 + 16.0 * i_, 28.0 + 16.0 * i_) for i_ in range(6)]   # plint önü: kondenser atışı (6 yarık 265 × 10)
ARKA_YARIK = [(2540.0 + 205.0 * i_, 2725.0 + 205.0 * i_) for i_ in range(6)]              # fırın altı hava boşluğu arka yarıkları (185 × 30)
ARKA_YARIK_Y = (748.0, 778.0)
ISINIM_Y = (740.0, 740.8)                     # parlak paslanmaz ışınım sacı 0,8 · takozlar 729–740
TAKOZ_XZ = [(x_, z_) for x_ in (2700.0, 3000.0, 3350.0, 3650.0) for z_ in (-700.0, -250.0)]
X_IC0S = 61.5                                 # v7: sol iç sac 61,5–62,5 (PU 60) · K1 ray duvarı 62,5


def hava_gecis(i, g):
    """v7 · bölme i'nin kesim gövdesine (kablo geçişi g) arka hava geçişlerini ekler"""
    for y0_, y1_ in HAVA_GECIS.get(i, ()):
        g = g.union(kut(BOLME_X[i] - 1.0, BOLME_X[i] + BOLME + 1.0, y0_, y1_, HAVA_Z[0], HAVA_Z[1]))
    return g


def profil(k, eks, t=2.0):
    """içi boş dikdörtgen profil (et t) · eks = profilin boyu hangi eksende"""
    x0, x1, y0, y1, z0, z1 = k
    ic = {"x": (x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t), "y": (x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t),
          "z": (x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 + 1.0)}[eks]
    return kut(*k).cut(kut(*ic))


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
    # v6: lamın arka ucu kablo kanalının önünde biter (K2 üst çekmecesinde lam 716,6–718,6 ↔ yatay kanal 703–728 çakışıyordu);
    #     arka ucu kanalın altından arka duvara L tırnakla bağlanır [VARSAYIM · modelde yok]
    ekle(kod + "_sensor_lami", kut(x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6, my0 + SEN[1], my0 + SEN[1] + 2.0, KAN_Z[1] + 1.0, Z_AVARA - 12.0), "celik", kod)
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
        if tat:
            nx = min(nx, TATLI["nx"])                                   # v6: 2 şerit × 6 = 12 (2 gün 11) · kalan genişlik boş
        xm = (ix0 + ix1) / 2.0
        X = [xm + (i - (nx - 1) / 2.0) * px for i in range(nx)]
        Z = [iz1 - 3.0 - r - j * pz for j in range(nz)]                 # itici ürünü öne dayar: robot hep öndekini alır
        y0 = kc + 1.0
        for i in range(nx + 1):
            xd = xm + (i - nx / 2.0) * px
            ekle("%s_serit_bolmesi_%d" % (kod, i), kut(xd - 0.5, xd + 0.5, y0, y0 + 50.0, iz0, iz1), "plastik", kod, grup=G,
                 bom=("Şerit bölmesi + yaylı itici takımı (market tipi) · şerit %.0f" % px, nx, "standart raf itici sistemi · ürünü öne iter",
                      "marka seçilmedi [VARSAYIM] · çekmece başına %d şerit" % nx) if i == 0 else None)
        zb = Z[-1] - r - 3.0
        for i, a in enumerate(X):
            ekle("%s_itici_%d" % (kod, i), kut(a - px / 2.0 + 4.0, a + px / 2.0 - 4.0, y0, y0 + (45.0 if tat else 70.0), zb - 12.0, zb), "plastik", kod, grup=G)
            ekle("%s_itici_yayi_%d" % (kod, i), kut(a - 6.0, a + 6.0, y0 + 2.0, y0 + 8.0, iz0, zb - 12.0), "celik", kod, grup=G)
        urun = sily(0.0, 0.0, r, 0.0, hk)
        n = 0
        for a in X:
            for b in Z:
                ekle("%s_%s_%d" % (kod, "tatlikabi" if tat else "kutu330", n), urun.translate((a, y0, b)), "hamur" if tat else "kutu_icecek", kod, grup=G); n += 1
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
    """v6 · TEK PARÇA DOLAP 0–4000 × 123–788: sandviç kabuk + PU + 6 bölme + TAŞIYICI ÇERÇEVE + K4 teknik + ŞERİT (robot çöpü).
    PU dolguları sacdan, çelik çerçeveden ve önceki PU'dan KESİLEREK konur → sac ↔ PU ↔ çelik çakışması olamaz."""
    B, T, C, E, Kb = "B_KASA", "B_TASIYICI", "B_COP", "B_ELEKTRIK", "B_KABLO"
    XB = BOLME_X                                   # 682,5 · 1337,5 · 1992,5 · 2500 · 3155 · 3775 (35'lik bölmelerin sol yüzü)
    XF0 = XB[3] + BOLME                            # 2535: fırın altı soğuk bölge (K5) başı
    XS = SERIT[0]                                  # 3810: yalıtımlı ara duvarın şerit yüzü
    ZP0, ZP1 = -DZ + 1.5, -41.5                    # PU derinliği: arka dış sacın önü … ön dönüşün arkası
    CER, SACK, PUK = [], [], []                    # taşıyıcı / sac / PU kutuları (x0, x1, y0, y1, z0, z1)
    kes_mi = lambda a, b: all(a[2 * i] < b[2 * i + 1] - 0.01 and b[2 * i] < a[2 * i + 1] - 0.01 for i in range(3))

    def sac(ad, k, bir=B, bom=None, ek=None):
        w = kut(*k)
        for c in CER:
            if kes_mi(k, c):
                w = w.cut(kut(*c))                  # taşıyıcı dikme / kiriş geçiş deliği
        if ek is not None:
            w = w.cut(ek)
        SACK.append(k)
        ekle(ad, w, "sac", bir, bom=bom)

    def pu(ad, k, bom=None, ek=None):
        w = kut(*k)
        for c in CER + SACK + PUK:
            if kes_mi(k, c):
                w = w.cut(kut(*c))
        if ek is not None:
            w = w.cut(ek)
        PUK.append(k)
        ekle(ad, w, "pu", B, bom=bom)

    # ---------------- TAŞIYICI ÇERÇEVE (fırın + raf yükü · hesap denetimde) ----------------
    for ad_, k_, eks in TASIYICI:
        CER.append(k_)
        bom = {"tasiyici_kiris_on": ("Taşıyıcı kiriş 40 × 40 × 2", 2, "AISI 304 kare profil · ısı kalkanının içinde, dış tavan sacının hemen altında",
                                     "%.0f boy · fırın 2500–4000'in altı · sağ uçta %.0f konsol" % (k_[1] - k_[0], W_B - TD_X[-1])),
               "tasiyici_capraz_0": ("Taşıyıcı çapraz 30 × 40 × 2", len(TD_X), "AISI 304 dikdörtgen profil · kirişlere kaynaklı",
                                     "%.0f boy · B4 / B5 / B6 bölme hizasında" % (k_[5] - k_[4])),
               "tasiyici_dikme_0": ("Taşıyıcı dikme 30 × 30 × 2", len(TD_X) * len(TD_Z), "AISI 304 kare profil · bölmenin PU'su içinde · alt ucunda M12 kaynak somunu → ayak",
                                    "%.0f boy · dış taban sacına oturur" % (k_[3] - k_[2]))}.get(ad_)
        ekle(ad_, profil(k_, eks), "celik", T, bom=bom)

    # ---------------- PLİNT + AYAK ----------------
    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0)
    for a_, b_, c_, d_ in PLINT_IZGARA:                                  # v7: kondenser atış kanalının önü ızgaralı
        pl_ = pl_.cut(kut(a_, b_, c_, d_, -62.5, -59.0))
    ekle("plint_on_1.5", pl_, "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride · v7: K4 altında 6 yarık (kondenser atışı)", ""))
    for i, (ax, az) in enumerate(AYAK_XZ):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", B,
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz AISI 304 · taban Ø40 · yükseklik 123",
                  "elesa-ganter.com LV.A-SST · 123'e uygun diş boyu + taşıma yükü katalogdan seçilecek · fırın altında dikmelerin altında") if i == 0 else None)

    # ---------------- KABUK SACLARI ----------------
    sac("yan_dis_sac_sol", (0.0, 1.5, Y_PLINT, H_B, -DZ, -40.0), bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · sol ön kenar kapak arkasında (z −40) · sağ (şerit) −18'e kadar", ""))
    sac("yan_dis_sac_sag", (W_B - 1.5, W_B, Y_PLINT, H_B, -DZ, -SERIT_DONUS))
    sac("tavan_dis_sac", (1.5, W_B - 1.5, H_B - 1.5, H_B, -DZ, -40.0), bom=("Tavan dış sacı", 1, "304 1,5 · A, C ve fırın bunun üstüne oturur (fırın altında taşıyıcı çerçeve)", ""))
    DR_DELIK = None                                                   # v7: gider borularının taban delikleri Ø14
    for _yan, _e in EVAP.items():
        _d = sily(_e["gider"][0], DR_Z, DR_R + 1.0, Y_PLINT - 1.0, Y_TABAN + 1.0)
        DR_DELIK = _d if DR_DELIK is None else DR_DELIK.union(_d)
    VENT = (K4X + 60.0, K4X + K4W - 60.0, -500.0, -120.0)            # K4 sıcak bölmesi: Secop havası tabandan plinte
    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0), ek=kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3]).union(DR_DELIK))
    AY_ = None                                                          # v7: fırın altı hava boşluğunun arka yarıkları
    for a_, b_ in ARKA_YARIK:
        _k = kut(a_, b_, ARKA_YARIK_Y[0], ARKA_YARIK_Y[1], -DZ - 1.0, -DZ + 2.5)
        AY_ = _k if AY_ is None else AY_.union(_k)
    sac("arka_dis_sac", (1.5, W_B - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), ek=AY_)
    sac("yan_ic_sac_sol", (X_IC0S, X_IC0S + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0))      # v7: PU 60 (v6 29–30 · PU 27,5) · önde çerçeve sacına dayanır
    sac("yan_on_donus_sol", (1.5, 30.0, Y_PLINT + 1.5, H_B - 1.5, -41.5, -40.0))
    # iç tavan: K1–K4 728 · fırın altı (K5, K6) 668 — üstünde ısı kalkanı
    sac("tavan_ic_sac", (X_IC0S, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5))
    sac("tavan_ic_sac_F", (XF0, XB[5], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, -41.5))
    TD_A, TD_F = (X_IC0, XF0, Y_TAVAN, H_B - 1.5, -41.5, -40.0), (XF0, XS - 1.0, Y_TAVAN_F, H_B - 1.5, -41.5, -40.0)
    ekle("tavan_on_donus", kut(*TD_A).union(kut(*TD_F)), "sac", B); SACK.extend([TD_A, TD_F])
    sac("taban_ic_sac", (X_IC0S, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)
    sac("taban_k4_kademe_saci", (K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -41.5),
        bom=("Taban kademe sacı 1,0", 1, "304 · yalıtımlı tabanın K4 tarafındaki ucunu kapatır", "K4 sıcak bölmesi 40 mm alçak"))
    sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)
    sac("taban_on_donus", (X_IC0, XS - 1.0, Y_PLINT + 1.5, Y_TABAN, -41.5, -40.0))
    sac("arka_ic_sac", (X_IC0S, XF0, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA))
    sac("arka_ic_sac_k4_alt", (K4X, XF0, Y_PLINT + 1.5, Y_TABAN, Z_ARKA - 1.0, Z_ARKA))
    sac("arka_ic_sac_F", (XF0, XB[5], Y_TABAN, Y_TAVAN_F, Z_ARKA - 1.0, Z_ARKA))
    # ön çerçevenin kutuları (açıklıklar sonra kesilir) PU'dan önce kayda girer
    CER_A, CER_F = (X_IC0, XF0, Y_TABAN, Y_TAVAN, Z_CER0, Z_CER1), (XF0, XS - 1.0, Y_TABAN, Y_TAVAN_F, Z_CER0, Z_CER1)
    SACK.extend([CER_A, CER_F])

    # ---------------- BÖLMELER 35 (sac 1 + PU 33 + sac 1) · üst arka köşede KABLO GEÇİŞİ 40 × 25 ----------------
    GECIS = lambda x0_, ku: kut(x0_ - 1, x0_ + BOLME + 1, ku[0], ku[1] + 1, KAN_Z[0] - 1, KAN_Z[1])
    for i, x0_ in enumerate(XB[:3]):                                   # B1–B3: K1 | K2 | K3 | K4 · 164,5–728
        g_ = hava_gecis(i, GECIS(x0_, KAN_UST))                          # v7: + arka hava geçişi
        sac("bolme_%d_sac_a" % i, (x0_, x0_ + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=g_)
        sac("bolme_%d_sac_b" % i, (x0_ + BOLME - 1.0, x0_ + BOLME, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=g_)
    g4 = hava_gecis(3, GECIS(XB[3], KAN_UST_F))                                       # B4: K4 | K5 — K4 yanı tabana iner (sıcak bölme), K5 yanı 163,5'ten
    sac("bolme_3_sac_a", (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    sac("bolme_3_sac_b", (XB[3] + BOLME - 1.0, XB[3] + BOLME, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    g5 = hava_gecis(4, GECIS(XB[4], KAN_UST_F))                                       # B5: K5 | K6 · 164,5–668
    sac("bolme_4_sac_a", (XB[4], XB[4] + 1.0, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    sac("bolme_4_sac_b", (XB[4] + BOLME - 1.0, XB[4] + BOLME, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    # B6: K6 | ŞERİT — soğuk zarfın sağ duvarı (3810'da yalıtımlı ara duvar); K6 fitili z −55'e kadar geldiği için PU önde −56'da biter
    sac("bolme_5_sac_a", (XB[5], XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA - 1.0, Z_CER0))
    sac("bolme_5_sac_b", (XS - 1.0, XS, Y_PLINT + 1.5, H_B - 1.5, ZP0, -40.0),
        bom=("Ara duvar sacı 1,0 (soğuk ↔ şerit)", 1, "304 · x 3809–3810 · taşıyıcı kiriş geçiş oyuklu", "şerit tarafı · arkasında PU 33"))

    # ---------------- v7 · FIRIN ALTI ISI KALKANI: PU 60 YOK → hava boşluğu (rapor seçenek b) ----------------
    #   fırın taşıyıcı kirişlere oturur (dış tavan sacı üstünden) · 728'de ayırma sacı (K5/K6 tavan PU'sunun üstü) · takozlar üstünde parlak
    #   paslanmaz ışınım sacı · yanlar sacla kapalı, arkada 6 yarık · önü çekmece önleriyle kapalı (ön yarık konamaz — 785–788 arası 3 mm)
    XG1 = XB[5] + 1.0                                                    # 3776 · sağda B6'nın üst PU'su başlar
    sac("isi_kalkani_ayirma_saci", (X_F[0], XG1, Y_TAVAN, Y_TAVAN + 1.0, ZP0, ZP1),
        bom=("Isı kalkanı ayırma sacı 1,0", 1, "304 · K5/K6 tavan PU'sunun üstü, hava boşluğunun tabanı", "x %.0f–%.0f · y %.0f–%.0f" % (X_F[0], XG1, Y_TAVAN, Y_TAVAN + 1.0)))
    sac("isi_kalkani_sol_sac", (X_F[0], X_F[0] + 1.0, Y_TAVAN + 1.0, H_B - 1.5, ZP0, ZP1),
        bom=("Isı kalkanı yan sacı 1,0", 2, "304 · hava boşluğunu yanlardan kapatır", "kiriş geçiş oyuklu"))
    sac("isi_kalkani_sag_sac", (XB[5], XB[5] + 1.0, Y_TAVAN + 1.0, H_B - 1.5, ZP0, ZP1))
    sac("isi_kalkani_isinim_saci", (X_F[0] + 1.0, XB[5], ISINIM_Y[0], ISINIM_Y[1], ZP0 + 2.0, ZP1 - 2.0),
        bom=("Işınım sacı 0,8 · parlak paslanmaz", 1, "304 BA (ε ≈ 0,1 VARSAYIM) · takozlar üstünde · dikme geçiş delikli",
             "fırın tabanının ışınımını geri yansıtır · üstünde %.0f mm havalandırmalı boşluk (rapor seçenek b)" % (H_B - 1.5 - ISINIM_Y[1])))
    for i_, (tx_, tz_) in enumerate(TAKOZ_XZ):
        ekle("isi_kalkani_takozu_%d" % i_, kut(tx_ - 10.0, tx_ + 10.0, Y_TAVAN + 1.0, ISINIM_Y[0], tz_ - 10.0, tz_ + 10.0), "koyu", B,
             bom=("Isı köprüsü kesici takoz 20 × 20 × 11", len(TAKOZ_XZ), "cam elyaf / PTFE [VARSAYIM]", "ayırma sacı ↔ ışınım sacı") if i_ == 0 else None)

    # ---------------- PU (40 kg/m³ enjeksiyon) — sırayla: her kutu öncekilerden, sacdan ve çelikten kesilir ----------------
    pu("yan_pu_sol", (1.5, X_IC0S, Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_CER0))          # v7: 60 (v6 27,5) — çerçeve sacının arkası
    pu("yan_pu_sol_on", (1.5, 29.0, Y_PLINT + 1.5, H_B - 1.5, Z_CER0, ZP1))              # önde fitil bandı (x 48–69) boş kalır
    pu("tavan_pu_57.5", (29.0, X_F[0], Y_TAVAN + 1.0, H_B - 1.5, ZP0, ZP1),
       bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 60 (v7) · tavan 57,5 (fırın altı 59 + hava boşluğu) · arka 37,5 · taban 39 · bölme 33"))
    pu("bolme_5_pu_ust", (XB[5] + 1.0, XS - 1.0, Y_TAVAN, H_B - 1.5, ZP0, ZP1))
    pu("tavan_pu_F", (XF0, XB[5] + 1.0, Y_TAVAN_F + 1.0, Y_TAVAN, ZP0, ZP1))
    pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)
    pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)
    pu("arka_pu_37.5", (29.0, XF0 - 1.0, Y_PLINT + 1.5, Y_TAVAN + 1.0, ZP0, Z_ARKA - 1.0))
    pu("arka_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN_F + 1.0, ZP0, Z_ARKA - 1.0))
    for i, x0_ in enumerate(XB[:3]):
        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=hava_gecis(i, GECIS(x0_, KAN_UST)))
    pu("bolme_3_pu", (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    pu("bolme_4_pu", (XB[4] + 1.0, XB[4] + BOLME - 1.0, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    pu("bolme_5_pu", (XB[5] + 1.0, XS - 1.0, Y_PLINT + 1.5, Y_TAVAN, ZP0, Z_CER0))

    # ---------------- KABLO KANALLARI: her kolonda arka sol dikey 40 × 25 · üstte 2 yatay (728 ve fırın altı 668 altında) ----------------
    for kol in KOLON_AD:
        cx = KOLON_X[kol]; ku = KAN_UST if kol in ("K1", "K2", "K3") else KAN_UST_F
        ekle("kablo_kanali_%s" % kol, kut(cx + KAN_X[0], cx + KAN_X[1], Y_TABAN, ku[0], KAN_Z[0], KAN_Z[1]),
             "kanal", Kb, bom=("Kablo kanalı 40 × 25", len(KOLON_AD) + 3, "PVC perfore + kapak", "dikey her kolonda (K1–K6) + üstte yatay 2") if kol == "K1" else None)
    K4KAN = kut(K4X + KAN_X[0], K4X + KAN_X[1], 400.0, KAN_UST[0], KAN_Z[0], KAN_Z[1])            # PLC'den yukarı
    ekle("kablo_kanali_K4", K4KAN, "kanal", Kb)
    ekle("kablo_kanali_ust", kut(K1X + KAN_X[1], K4X + KAN_X[1], KAN_UST[0], KAN_UST[1], KAN_Z[0], KAN_Z[1]), "kanal", Kb)
    ekle("kablo_kanali_ust_F", kut(K4X + KAN_X[1], KOLON_X["K6"] + KAN_X[1], KAN_UST_F[0], KAN_UST_F[1], KAN_Z[0], KAN_Z[1]), "kanal", Kb)


    # ---------------- v7 · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1) — 2 bölge ----------------
    #   lamelli + epoksi kaplı evaporatör (maya / asetik asit korozyonu) · önünde davlumbaz + 2 × 4414 FL · arkasında 38 plenum
    #   · hava bölmelerdeki arka geçişlerden komşu kolonlara · altında damlama teknesi → Ø12 gider → plint → buharlaştırma tavası
    for yan, e in EVAP.items():
        cx = KOLON_X[e["kol"]]; ey0, ey1 = e["y"]; ilk = yan == "sol"
        ekle("evaporator_%s_lamel" % yan, kut(cx + 252.0, cx + 588.0, ey0, ey1, EV_Z[0], EV_Z[1]), "aluminyum", "B_SOGUTMA",
             bom=("Evaporatör lamelli · epoksi kaplı Cu/Al", 2, "bakır boru + alüminyum lamel, epoksi kaplı · 4 sıra · lamel aralığı 4,2 [VARSAYIM]",
                  "336 × 400 × 85 (sol, K2 arkası) · 336 × 265 × 85 (sağ, K5 arkası) · iki bölge UA ≈ 60 W/K (sogutma_hesabi_v1) · ölçüye üretim") if ilk else None)
        for s_, (a_, b_) in (("a", (250.0, 252.0)), ("b", (588.0, 590.0))):
            ekle("evaporator_%s_yan_sac_%s" % (yan, s_), kut(cx + a_, cx + b_, ey0, ey1, EV_Z[0], EV_Z[1]), "sac", "B_SOGUTMA")
        for s_, (a_, b_) in (("a", (240.0, 250.0)), ("b", (590.0, 600.0))):
            ekle("evaporator_%s_dirsek_%s" % (yan, s_), kut(cx + a_, cx + b_, ey0 + 8.0, ey1 - 8.0, EV_Z[0] + 7.0, EV_Z[1] - 7.0), "bakir", "B_SOGUTMA")
        for j_, xa_ in enumerate((300.0, 520.0)):
            ekle("evaporator_%s_askisi_%d" % (yan, j_ + 1), kut(cx + xa_, cx + xa_ + 20.0, ey1, ey1 + 2.0, Z_ARKA, EV_Z[1]), "celik", "B_SOGUTMA",
                 bom=("Evaporatör askısı 2 mm", 4, "304 lama · arka iç saca 2 × M5 perçin somun", "lamel bloğu üstten asılı") if ilk and j_ == 0 else None)
        tk = kut(cx + 240.0, cx + 600.0, ey0 - 15.0, ey0 - 3.0, EV_Z[0] - 4.0, EV_Z[1] + 7.0)
        ekle("damlama_teknesi_%s" % yan, tk.cut(kut(cx + 241.5, cx + 598.5, ey0 - 13.5, ey0 - 2.0, EV_Z[0] - 2.5, EV_Z[1] + 5.5)), "sac", "B_SOGUTMA",
             bom=("Damlama teknesi 1,5", 2, "304 büküm · gider ağzına eğimli", "evaporatörün altında · Ø12 gider") if ilk else None)
        yc = (ey0 + ey1) / 2.0
        dv = kut(cx + 245.0, cx + 595.0, ey0, ey1, EV_Z[1], FAN_Z[0]).cut(kut(cx + 246.0, cx + 594.0, ey0 + 1.0, ey1 - 1.0, EV_Z[1] - 1.0, FAN_Z[0] - 1.0))
        for j_, fx in enumerate(FAN_X):
            dv = dv.cut(kut(cx + fx + 3.0, cx + fx + 116.0, yc - 56.5, yc + 56.5, FAN_Z[0] - 2.0, FAN_Z[0] + 1.0))
            ekle("fan_%s_%d" % (yan, j_ + 1), kut(cx + fx, cx + fx + 119.0, yc - 59.5, yc + 59.5, FAN_Z[0], FAN_Z[1]), "motor", "B_SOGUTMA",
                 bom=("Fan ebm-papst 4414 FL", 4, "24 V · 1,2 W · 94 m³/h · 26 dB(A) · 119 × 119 × 25",
                      "bölge başına 2 · davlumbazın önünde (v6: 7 × 4414 FNH 12 W = 84 W ısı → kalktı)") if ilk and j_ == 0 else None)
        ekle("fan_davlumbazi_%s" % yan, dv, "sac", "B_SOGUTMA",
             bom=("Fan davlumbazı 1,0", 2, "304 büküm · 2 fan deliği 113 × 113", "lamel yüzüne 26 mm (rapor ≥ 25)") if ilk else None)
        gx, gxs = e["gider"]
        gb = sily(gx, DR_Z, DR_R, DR_Y - DR_R, ey0 - 15.0).union(silx(DR_Y, DR_Z, DR_R, min(gx, gxs) - DR_R, max(gx, gxs) + DR_R))
        gb = gb.union(silz(gxs, DR_Y, DR_R, DR_Z - DR_R, GIDER_UC_Z))
        ekle("gider_borusu_%s" % yan, gb, "plastik", "B_SOGUTMA",
             bom=("Gider borusu Ø12 × 1", 2, "PVC · teknenin dibinden tabandan plinte, plintte K4 altına [VARSAYIM ısıtıcısız: dolap +3 °C]",
                  "uç atış kanalında buharlaştırma tavasının üstünde (serbest damlama)") if ilk else None)
    ak = kut(ATIS[0], ATIS[1], ATIS[2], ATIS[2] + 1.5, ATIS[3], -61.5)
    ak = ak.union(kut(ATIS[0], ATIS[0] + 1.5, ATIS[2] + 1.5, Y_PLINT, ATIS[3], -61.5)).union(kut(ATIS[1] - 1.5, ATIS[1], ATIS[2] + 1.5, Y_PLINT, ATIS[3], -61.5))
    ak = ak.union(kut(ATIS[0] + 1.5, ATIS[1] - 1.5, ATIS[2] + 1.5, Y_PLINT, ATIS[3], ATIS[3] + 1.5))
    for _yan, _e in EVAP.items():
        ak = ak.cut(silz(_e["gider"][1], DR_Y, DR_R + 1.0, ATIS[3] - 1.0, ATIS[3] + 2.5))
    ekle("kondenser_atis_kanali", ak, "sac", "B_SOGUTMA",
         bom=("Kondenser atış kanalı 1,5", 1, "304 büküm · K4 taban deliğinden plint önündeki ızgaraya", "sıcak hava dolabın altına yayılmaz (emiş K4 kapağı ızgarası)"))
    ekle("buharlastirma_tavasi", kut(TAVA[0], TAVA[1], TAVA[2], TAVA[3], TAVA[4], TAVA[5]).cut(kut(TAVA[0] + 1.5, TAVA[1] - 1.5, TAVA[2] + 1.5, TAVA[3] + 1.0, TAVA[4] + 1.5, TAVA[5] - 1.5)),
         "sac", "B_SOGUTMA", bom=("Buharlaştırma tavası 1,5", 1, "304 · atış kanalında, kondenser sıcak havasının içinde",
                                  "%.0f × %.0f × %.0f · defrost suyu (günde 4 defrost, VARSAYIM ≤ 1 L)" % (TAVA[1] - TAVA[0], TAVA[3] - TAVA[2], TAVA[5] - TAVA[4])))

    # ---------------- K4 (2027,5–2500): SICAK bölme (Secop önde, B panosu arkada) · ara PU · KAŞAR + SUCUK DEPOSU (soğuk) — v5 ile aynı ----------------
    kx0, kx1 = K4X, K4X + K4W
    CU = (350.0, 297.0, 450.0)                                                 # v7: NLE8.8CN 297 yüksek (föy) · taban 350 × 450 VARSAYIM
    cx0, cy0, cz1 = kx0 + 25.0, Y_PLINT + 1.5 + 4.0, Z_CER0 - 10.0            # ünite sıcak bölmenin tek sac tabanında (128,5)
    ekle("sogutma_grubu_taban", kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz1 - CU[2], cz1), "motor", "B_SOGUTMA",
         bom=("Yoğuşturucu ünite Secop CU NLE8.8CN R290", 1, "737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C (secop.com föyü) · gereken 552–661 W @ 32 °C",
              "yükseklik 297 (föy) · taban 350 × 450 VARSAYIM (föyden teyit) · v7: KLF4.0CND 32 °C'de 309 W yetmiyordu; hamur ılık gelir (Kemal) · sogutma_hesabi_v1"))
    ekle("sogutma_grubu_kondenser", kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + 15.0, cy0 + CU[1], cz1 - 60.0, cz1), "bakir", "B_SOGUTMA")
    ekle("sogutma_grubu_fan", silz(cx0 + CU[0] / 2.0, cy0 + 15.0 + 125.0, 115.0, cz1 - 90.0, cz1 - 62.0), "motor", "B_SOGUTMA")
    ekle("sogutma_grubu_kompresor", sily(cx0 + CU[0] / 2.0, cz1 - 310.0, 85.0, cy0 + 15.0, cy0 + 15.0 + 162.0), "koyu", "B_SOGUTMA")
    s0 = cy0 + CU[1] + 8.0
    # v6: ara katman K4'ün tam genişliğinde (B3 → B4); v5'te kx1'de (2427,5) bitiyordu, yan duvara 42,5'lik sıcak hava yarığı kalıyordu
    ekle("k4_ara_sac_alt", kut(kx0, K4_SAG, s0, s0 + 1.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, K4_SAG, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0).cut(K4KAN), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, K4_SAG, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, -522.0, -521.0), "sac", "B_SOGUTMA",
         bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında", "yoğuşturucu havası panoya gelmez"))
    ZP = Z_ARKA + 2.0                                                  # montaj plakası arka duvarda, öne bakar
    ekle("pano_montaj_plakasi", kut(kx0 + 10.0, kx1 - 10.0, 132.0, 398.0, Z_ARKA, ZP), "sac", E, bom=("Pano montaj plakası 2 mm", 1, "galvaniz", "K4 · Secop'un arkasında"))
    for i_, yr in enumerate((177.5, 312.5)):
        ekle("din_ray_%d" % i_, kut(kx0 + 12.0, kx1 - 12.0, yr, yr + 35.0, ZP, ZP + 7.5), "celik", E, bom=("DIN ray TS35 × 7,5", 2, "", "") if i_ == 0 else None)
    zd = ZP + 7.5
    x = kx0 + 14.0; ty = 145.0
    ekle("plc_S7-1200_1214C", kut(x, x + 110.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · 14 DI · 10 DQ · PROFINET/Modbus TCP", "110 × 100 × 75")); x += 110.0
    for ad_, kodu in (("SM1221_DI16_a", "6ES7221-1BH32-0XB0"), ("SM1221_DI16_b", "6ES7221-1BH32-0XB0"), ("SM1221_DI16_c", "6ES7221-1BH32-0XB0"),
                      ("SM1222_DQ16", "6ES7222-1BH32-0XB0")):                                # v6: 48 reed > 14 + 32 DI → 3. SM1221
        ekle("plc_" + ad_, kut(x, x + 45.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
             bom=("PLC genişleme %s" % ad_.split("_")[0] + " " + ad_.split("_")[1], 3 if ad_.startswith("SM1221") else 1, kodu,
                  "45 × 100 × 75 · %d reed + %d röle" % (2 * len(CEK), len(CEK)))); x += 45.0
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
         bom=("Klemens bloğu", 1, "Phoenix UT 2,5 · %d motor + %d sensör + güç" % (len(CEK), 2 * len(CEK)), "kalan genişlik"))
    d0 = s0 + 30.0; d1 = d0 + GN_H
    # KAŞAR + SUCUK DEPOSU (4 günün 2. yarısı): GN 1/1-100 (kaşar blok) · raf · GN 1/2-100 (küp sucuk) — v5 ile aynı yer
    g0 = d0 + 5.0
    ekle("k4_depo_GN11_100", kut(kx0 + 37.5, kx1 - 37.5, g0, g0 + 100.0, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g0 + 1.0, g0 + 101.0, Z_CER0 - 539.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/1-100 kap + kapak", 1, "304 · EN 631 · 530 × 325 × 100", "kaşar blok 2 gün = 8,8 kg (yoğunluk VARSAYIM)"))
    ekle("k4_depo_raf", kut(kx0, K4_SAG, g0 + 110.0, g0 + 111.5, Z_ARKA + 32.0, Z_CER0), "sac", "B_DEPO")   # v7: arkasında 32 hava geçişi (depo sağ bölgeden B4 geçişleriyle soğur)
    g1 = g0 + 116.5
    ekle("k4_depo_GN12_100", kut(kx0 + 37.5, kx1 - 37.5, g1, g1 + 100.0, Z_CER0 - 275.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g1 + 1.0, g1 + 101.0, Z_CER0 - 274.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/2-100 kap + kapak", 1, "304 · EN 631 · 325 × 265 × 100", "küp sucuk 2 gün = 2,8 kg"))
    # K4 önleri (tam kaplama 126 → 785): soğutma (ızgaralı, yalıtımsız) · depo (fitilli) — v6: depo açıklığı 438,5–707,5 (v5 654,5 GN 1/2'nin altındaydı)
    KAP = [("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False, (ON_ALT + BIND, s0 + 12.0 - BIND)),
           ("k4_kapak_depo", s0 + 15.0, ON_UST, "B_DEPO", True, (d0, Y_TAVAN - 20.5))]
    PENCERE = (kx0 + 20.0, kx1 - 20.0, Y_TABAN + 23.0, s0 - 8.0)
    for ad_, y0_, y1_, bir, fit, ac in KAP:
        a_, b_ = KAPAK_X["K4"]
        if not fit:                                                   # sıcak bölme: yalıtımsız, fitilsiz, ızgaralı
            ds = kut(a_, b_, y0_, y1_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
            ekle(ad_ + "_dis_sac", ds.cut(kut(PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3], Z_ON0 - 1, Z_ON1 + 1)), "sac", bir,
                 bom=("Yoğuşturucu bölmesi kapağı", 1, "304 1,5 · yalıtımsız · ızgaralı hava penceresi", "hava önden (ızgara) girer, tabandan atış kanalıyla plint önündeki ızgaradan çıkar (v7)"))
            continue
        kapak_on(ad_, a_, b_, y0_, y1_, bir, (kx0, kx1, ac[0], ac[1]))
    for i in range(int((PENCERE[3] - PENCERE[2] - 14.0) // 16.0)):       # (ızgara penceresi aynı)
        gy = PENCERE[2] + 7.0 + i * 16.0
        ekle("k4_izgara_%02d" % i, kut(PENCERE[0], PENCERE[1], gy, gy + 8.0, Z_ON1 - 1.5, Z_ON1), "izgara", "B_SOGUTMA")

    # ---------------- ŞERİT 3810–4000 · ROBOT ÇÖPÜ (soğuk DEĞİL) ----------------
    ka_, kb_, kc_, kd_, ke_, kf_ = KOVA
    t_ = KOVA_T
    kiz = kut(XS + 4.0, W_B - 4.0, Y_PLINT + 1.5, ON_ALT, -445.0, kf_)
    kiz = kiz.union(kut(XS + 4.0, XS + 5.5, ON_ALT, ON_ALT + 15.0, -445.0, kf_)).union(kut(W_B - 5.5, W_B - 4.0, ON_ALT, ON_ALT + 15.0, -445.0, kf_))
    kiz = kiz.union(kut(XS + 4.0, W_B - 4.0, ON_ALT, ON_ALT + 15.0, -446.5, -445.0))
    ekle("cop_kova_kizagi", kiz, "sac", C, bom=("Kova kızağı 1,5", 1, "304 büküm · yan + arka dudak 15 · dış taban sacına 4 × M5", "kova öne çekilip çıkarılır"))
    ekle("robot_cop_kovasi_15L", kut(ka_, kb_, kc_, kd_, ke_, kf_).cut(kut(ka_ + t_, kb_ - t_, kc_ + 3.0, kd_ + 1.0, ke_ + t_, kf_ - t_)), "plastik", C,
         bom=("Robot çöp kovası 15 L · ince dikdörtgen", 1, "PP · gıda uygun · zarf 165 × 300 × 400 (SPEC) · düz duvar modellendi (gerçek kova konik)",
              "marka seçilmedi [VARSAYIM] · 2 gün fire ≈ 6 L gevşek × 2 pay (teknik_qr_tezgah_v4)"))
    ic_ = (ka_ + t_, kb_ - t_, kc_ + 3.0, kd_, ke_ + t_, kf_ - t_)
    poset = kut(*ic_).cut(kut(ic_[0] + 0.5, ic_[1] - 0.5, ic_[2] + 0.5, kd_ + 1.0, ic_[4] + 0.5, ic_[5] - 0.5))
    kivrim = kut(ka_ - 0.5, kb_ + 0.5, kd_ - 30.0, kd_ + 0.5, ke_ - 0.5, kf_ + 0.5).cut(kut(ka_, kb_, kd_ - 31.0, kd_, ke_, kf_))
    kivrim = kivrim.cut(kut(ic_[0] + 0.5, ic_[1] - 0.5, kd_ - 31.0, kd_ + 1.0, ic_[4] + 0.5, ic_[5] - 0.5))
    ekle("robot_cop_poseti", poset.union(kivrim), "poset", C, bom=("Çöp poşeti 15 L (sarf)", 1, "LDPE 0,5 (modelde) · kova ağzından 30 dışa kıvrılır", "eleman kovayı boşaltırken değiştirir"))
    SK0, SK1 = KAPAK_X["SERIT"]

    def serit_on(ad, y0_, y1_, delik=None, bom=None):
        w = kut(SK0, SK1, y0_, y1_, -SERIT_DONUS, 0.0).cut(kut(SK0 + 1.5, SK1 - 1.5, y0_ + 1.5, y1_ - 1.5, -SERIT_DONUS - 1.0, -1.5))
        if delik:
            w = w.cut(kut(delik[0], delik[1], delik[2], delik[3], -2.0, 1.0))
        ekle(ad, w, "sac", C, bom=bom)
    serit_on("serit_on_kapak", SERIT_KAPI[0], SERIT_KAPI[1],
             bom=("Şerit servis kapağı 1,5 · yalıtımsız", 1, "304 büküm · 18 dönüş · bas-aç mandal + 2 gizli menteşe [VARSAYIM]",
                  "%.0f × %.0f · kova öne çekilerek boşaltılır" % (SK1 - SK0, SERIT_KAPI[1] - SERIT_KAPI[0])))
    serit_on("serit_on_klape_paneli", SERIT_PANEL[0], SERIT_PANEL[1], delik=KLAPE_AC,
             bom=("Şerit klape paneli 1,5", 1, "304 büküm · 18 dönüş · sabit · klape açıklığı %.0f × %.0f" % (KLAPE_AC[1] - KLAPE_AC[0], KLAPE_AC[3] - KLAPE_AC[2]),
                  "%.0f × %.0f" % (SK1 - SK0, SERIT_PANEL[1] - SERIT_PANEL[0])))
    ky_, kz_ = KLAPE_EKSEN
    ekle("klape_levhasi", kut(KLAPE_AC[0] - 6.0, KLAPE_AC[1] + 6.0, KLAPE_AC[2] - 6.0, ky_ - 4.0, -3.0, -1.5), "sac", C, grup="KLAPE",
         bom=("Yaylı klape levhası 1,5", 1, "304 · içe açılır (robot eli iter) · yay kapatır · en çok %.0f° (mekanik stop)" % KLAPE_MAX,
              "%.0f × %.0f · panelin arkasında, açıklığı 6 bindirir" % (KLAPE_AC[1] - KLAPE_AC[0] + 12.0, ky_ - 4.0 - KLAPE_AC[2] + 6.0)))
    ekle("klape_mentesesi", silx(ky_, kz_, 4.0, KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0), "celik", C,
         bom=("Yaylı menteşe Ø8 · yay gövde içinde", 1, "paslanmaz · %.0f boy · kapanma momenti [VARSAYIM]" % (KLAPE_AC[1] - KLAPE_AC[0] - 10.0), "marka seçilmedi [VARSAYIM]"))
    ekle("klape_mentese_yapragi", kut(KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0, ky_ + 4.0, ky_ + 22.0, -3.0, -1.5), "celik", C)

    # ---------------- ÖN ÇERÇEVE SACI 1,0: bütün açıklıklar kesik (fitil buna basar) · fırın altında üst kenar 668 ----------------
    cer = kut(*CER_A).union(kut(*CER_F))
    for kol, kod, tip, x0, yo in CEK:
        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))
    for _a, _y0, _y1, _b, _f, ac in KAP:
        cer = cer.cut(kut(kx0, kx1, ac[0], ac[1], Z_CER0 - 1, Z_CER1 + 1))
    ekle("on_cerceve_saci_1.0", cer, "sac", B, bom=("Ön çerçeve sacı 1,0", 1, "304 lazer kesim · %d açıklık · fırın altında üst kenar %.0f" % (len(CEK) + len(KAP), Y_TAVAN_F), "fitil buna basar"))
    return s0, d0, d1


def modul():
    PARCALAR[:] = []
    k4 = kasa()
    ozet = []
    for kol, kod, tip, x0, yo in CEK:
        n, ust, acik_ust = cekmece(kol, kod, tip, x0, yo)
        ozet.append((kod, tip, n, ust, acik_ust))
    return ozet


def _kesisim(sekil, parcalar, haric=(), esik=1.0):
    """sekil ile parçaların gerçek kesişim hacimleri (> esik mm³)"""
    A = sekil.BoundingBox(); bul = []
    for p in parcalar:
        if p["ad"] in haric:
            continue
        v_ = p["wp"].val(); b = v_.BoundingBox()
        if A.xmin >= b.xmax - 0.05 or b.xmin >= A.xmax - 0.05 or A.ymin >= b.ymax - 0.05 or b.ymin >= A.ymax - 0.05 or A.zmin >= b.zmax - 0.05 or b.zmin >= A.zmax - 0.05:
            continue
        v = v_.intersect(sekil).Volume()
        if v > esik:
            bul.append((v, p["ad"]))
    return sorted(bul, reverse=True)


def denetim(ozet, tarama=True):
    print("CEKMECELI DOLAP v7 (sogutma standart duzen) · tek parca 0-%.0f x %.0f-%.0f · %d parca · %d cekmece · birimler: %s"
          % (W_B, Y_PLINT, H_B, len(PARCALAR), len(CEK), ", ".join(sorted({p["birim"] for p in PARCALAR if not p["birim"].startswith("CEK_")}))))
    BB = {p["ad"]: p["wp"].val().BoundingBox() for p in PARCALAR}
    assert len(BB) == len(PARCALAR), "parca adlari tekil degil"
    yb = lambda ad: BB[ad]
    # ---- ALT TABAN ÇİZGİSİ + DÜZ ÜST (katılardan ölçülür) ----
    alt = yb("taban_dis_sac").ymin
    ic_ust = yb("taban_ic_sac").ymax
    on_alt = min(BB[p["ad"]].ymin for p in PARCALAR if p["ad"].endswith("_on_dis_sac_1.5") and p["grup"] == "CEKMECE")
    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin; sr_alt = yb("serit_on_kapak").ymin
    govde_alt = min(BB[p["ad"]].ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))
    ust = max(b.ymax for b in BB.values())
    print("ALT / UST: govde alti %.1f (en alcak govde parcasi %.1f) · ic taban ustu %.1f · en alt on %.1f · K4 kapagi alti %.1f · serit kapagi alti %.1f · EN UST PARCA %.1f (duz cizgi %.0f)"
          % (alt, govde_alt, ic_ust, on_alt, k4_alt, sr_alt, ust, H_B))
    assert abs(alt - 123.0) < 0.05 and abs(govde_alt - alt) < 0.05, "govde alti 123 degil"
    assert abs(on_alt - ON_ALT) < 0.05 and abs(k4_alt - ON_ALT) < 0.05 and abs(sr_alt - ON_ALT) < 0.05, "on alt kenarlari 126 cizgisinde degil"
    assert abs(ust - H_B) < 0.05, "dolap ustu %.1f (788 olmali)" % ust
    # ---- ÖN YÜZ IZGARASI: her kolonda önler 126 → 785 arası 3 mm aralıkla kesintisiz; kolonlar arası 3; 0 → 4000 ----
    on = [BB[p["ad"]] for p in PARCALAR if (p["ad"].endswith(("_dis_sac_1.5", "_dis_sac")) and ("CEK_" in p["ad"] or p["ad"].startswith("k4_kapak")))
          or p["ad"].startswith("serit_on_")]
    for kol, (pa, pb) in KAPAK_X.items():
        sut = sorted((b for b in on if abs(b.xmin - pa) < 0.05 and abs(b.xmax - pb) < 0.05), key=lambda b: b.ymin)
        assert sut and abs(sut[0].ymin - ON_ALT) < 0.05 and abs(sut[-1].ymax - ON_UST) < 0.05, "%s: on yuz 126-785 degil" % kol
        for u_, v_ in zip(sut, sut[1:]):
            assert abs(v_.ymin - u_.ymax - FUGA) < 0.05, "%s: onler arasi %.1f (3 olmali)" % (kol, v_.ymin - u_.ymax)
        print("   ON YUZ %-5s: x %6.1f-%6.1f · %d parca · %.0f-%.0f · aralar 3" % (kol, pa, pb, len(sut), sut[0].ymin, sut[-1].ymax))
    xs = sorted(KAPAK_X.values())
    assert all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and xs[0][0] == 0.0 and xs[-1][1] == W_B, "kolon onleri arasi 3 degil / 0-4000 degil"
    # ---- YIĞIN + TAVAN: Σ(HH + 33) ≤ sınır (SPEC) · en üst çekmece parçası ≤ iç tavan − 2 · fitil ≤ iç tavan (katılardan) ----
    for kol in KOLON_AD:
        cs = [c for c in CEK if c[0] == kol]
        top_ = sum(HH[c[2]] + 2 * BIND + FUGA for c in cs)
        ps = [p for p in PARCALAR if p["birim"].startswith("CEK_%s_" % kol)]
        ust_p = max(BB[p["ad"]].ymax for p in ps if "_on_" not in p["ad"])
        fit = max(BB[p["ad"]].ymax for p in ps if p["ad"].endswith("_on_fitil"))
        tav = TAVAN_KOL[kol]
        dz = {}
        for c in cs:
            dz[c[2]] = dz.get(c[2], 0) + 1
        print("   YIGIN %s: %s · toplam %.0f / sinir %.0f (bos %.0f) · en ust cekmece parcasi %.1f · fitil ustu %.1f · ic tavan %.0f"
              % (kol, " + ".join("%d %s" % (n_, t_) for t_, n_ in dz.items()), top_, YIGIN_SINIR[kol], YIGIN_SINIR[kol] - top_, ust_p, fit, tav))
        assert top_ <= YIGIN_SINIR[kol] + 0.01, "%s yigini sinirda degil" % kol
        assert ust_p <= tav - 2.0 and fit <= tav + 0.01, "%s tavana degiyor" % kol
    # ---- K4 depo: açıklık fitili tavanın altında · GN 1/2 çekilebilir ----
    dk = yb("k4_kapak_depo_fitil"); g12 = yb("k4_depo_GN12_100"); ac1 = Y_TAVAN - 20.5
    print("K4 DEPO: kapak %.1f-%.1f · aciklik %.1f-%.1f · fitil ustu %.1f / tavan %.0f · GN 1/2 ustu %.1f -> cekme payi %.1f · K4 ara katman %.1f-%.1f x %.1f-%.1f"
          % (yb("k4_kapak_depo_dis_sac_1.5").ymin, yb("k4_kapak_depo_dis_sac_1.5").ymax, yb("k4_ara_sac_ust").ymax, ac1, dk.ymax, Y_TAVAN, g12.ymax, ac1 - g12.ymax,
             yb("k4_ara_sac_alt").ymin, yb("k4_ara_sac_ust").ymax, yb("k4_ara_pu").xmin, yb("k4_ara_pu").xmax))
    assert dk.ymax <= Y_TAVAN + 0.01 and ac1 - g12.ymax >= 20.0 and abs(yb("k4_ara_pu").xmax - K4_SAG) < 0.05
    # ---- RAY: tam açıkta elemanlar birbirinin içinde kalıyor mu, kutu iç elemana boyunca bağlı mı? (katılardan) ----
    en = dict(b1=1e9, b2=1e9, bag=1e9)
    for kod, tip, _n, _u, _a in ozet:
        for yan in ("sol", "sag"):
            zr = {}
            for el in ("dis", "ara", "ic"):
                bb = BB["%s_ray_%s_%s" % (kod, el, yan)]
                k = {"dis": 0.0, "ara": RAY_ARA_ORAN, "ic": 1.0}[el] * STROK
                zr[el] = (bb.zmin + k, bb.zmax + k)
            ad_ = BB["%s_ray_adaptor_%s" % (kod, yan)]
            b1 = min(zr["dis"][1], zr["ara"][1]) - max(zr["dis"][0], zr["ara"][0])
            b2 = min(zr["ara"][1], zr["ic"][1]) - max(zr["ara"][0], zr["ic"][0])
            bag = min(zr["ic"][1], ad_.zmax + STROK) - max(zr["ic"][0], ad_.zmin + STROK)
            assert b1 >= 250.0 and b2 >= 250.0, "%s %s: ray bindirmesi yetersiz (%.0f / %.0f)" % (kod, yan, b1, b2)
            assert bag >= ad_.zlen - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / %.0f)" % (kod, yan, bag, ad_.zlen)
            en = dict(b1=min(en["b1"], b1), b2=min(en["b2"], b2), bag=min(en["bag"], bag))
    print("RAY (3 elemanli teleskop, %d cekmece x 2 yan, tam acik strok %.0f): en az dis-ara bindirme %.0f mm · ara-ic %.0f mm · kutu-ic ray bagi %.0f mm · ara eleman +%.0f"
          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK))
    # ---- İÇERİK + KAPASİTE (2 GÜN KURALI) ----
    for kod, tip, n, ust_, acik in ozet:
        assert acik - ust_ >= 2.0, "%s: icerik aciklik ustune %.1f mm kaliyor" % (kod, acik - ust_)
    tipler = sorted({t for _k, t, _n, _u, _a in ozet})
    pay = {t: min(a - u for _k, tt, _n, u, a in ozet if tt == t) for t in tipler}
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t in ("ic1", "ic1d")); tat = sum(n for _k, t, n, _u, _a in ozet if t == "tatli")
    print("ICERIK PAYI (acikliga): " + " · ".join("%s %.1f" % (t, pay[t]) for t in tipler) + " mm")
    print("KAPASITE (2 gun kurali): pide %d top (>= 160) · lahmacun %d top (>= 400) · icecek %d kutu TEK KAT (>= 139) · tatli %d kap (>= 11) · beklenen 160 / 432 / 144 / 12"
          % (pide, lahm, ice, tat))
    assert pide >= 160 and lahm >= 400 and ice >= 139 and tat >= 11, "2 gun kurali saglanmiyor"
    assert (pide, lahm, ice, tat) == (160, 432, 144, 12), "kapasite SPEC ile ayni degil"
    hiz = 127.0 / 60.0 * math.pi * KAS_PD
    print("TAHRIK: PD3665-24-51 127 d/dk × GT3 30 dis (cevre %.1f) = %.0f mm/s · strok %.0f -> %.1f sn · surekli kuvvet %.0f N (0,853 N·m / r %.2f)"
          % (math.pi * KAS_PD, hiz, STROK, STROK / hiz, 0.853 / (KAS_PD / 2000.0), KAS_PD / 2.0))
    for tip in TOP:
        t = TOP[tip]; z_tub0 = Z_CON0 - 2.0 - TUB[tip]
        arka = z_tub0 + 5.0 + t["td"] / 2.0 - (t["nz"] - 1) / 2.0 * t["az"]
        kenar = arka + STROK - t["R"]
        print("   %s: acilinca arka sira topun arka kenari z %+.0f (on yuz 0)" % (tip, kenar))
        assert kenar >= 5.0
    t = TOP["hamur"]; arka = Z_CON0 - 2.0 - TUB["hamur"] + 5.0 + t["td"] / 2.0 - (t["nz"] - 1) / 2.0 * t["az"] + STROK
    print("   K5 (firin alti) pide: acilinca arka sira top merkezi z %+.0f · firin cikintisi z 0…+%.0f (y >= %.0f) -> dikey yaklasimda tutucu yaricapi <= %.0f mm (robot tarafi ACIK)"
          % (arka, FIRIN_CIKINTI, H_B, arka - FIRIN_CIKINTI))
    # ---- ŞERİT · ROBOT ÇÖPÜ ----
    kb = yb("robot_cop_kovasi_15L")
    ic_l = (kb.xlen - 2 * KOVA_T) * (kb.ylen - 3.0) * (kb.zlen - 2 * KOVA_T) / 1e6
    print("SERIT %.0f-%.0f (soguk degil): kova %.0f × %.0f × %.0f (x · y · z) · x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f · ic hacim (duz duvar) %.1f L · nominal 15 L"
          % (SERIT[0], SERIT[1], kb.xlen, kb.ylen, kb.zlen, kb.xmin, kb.xmax, kb.ymin, kb.ymax, kb.zmin, kb.zmax, ic_l))
    assert abs(kb.xlen - 165.0) < 0.05 and abs(kb.ylen - 300.0) < 0.05 and abs(kb.zlen - 400.0) < 0.05, "kova olcusu 165 × 300 × 400 degil"
    assert abs(kb.ymin - 126.0) < 0.05 and abs(kb.zmin + 420.0) < 0.05 and abs(kb.zmax + 20.0) < 0.05, "kova yeri SPEC degil"
    ps_ = yb("robot_cop_poseti")
    AT = kut(KOVA[0], KOVA[1], ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5]).val()
    dolu = _kesisim(AT, PARCALAR)
    print("   ATMA BOSLUGU (kova izdusumu, poset agzi %.1f -> klape acikligi ustu %.0f, z %.0f…%.0f): %d parca giriyor · ustunde tasiyici kiris %.1f-%.1f"
          % (ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5], len(dolu), TK_Y[0], TK_Y[1]))
    assert not dolu, "atma boslugunda parca var: %s" % dolu[:5]
    GIR = kut(KLAPE_AC[0], KLAPE_AC[1], KLAPE_AC[2], KLAPE_AC[3], KOVA[5], 0.0).val()
    dolu = _kesisim(GIR, PARCALAR, haric=("klape_levhasi",))
    print("   KLAPE ACIKLIGI %.0f × %.0f (x %.0f-%.0f · y %.0f-%.0f): giris yolunda klape levhasi disinda %d parca" % (KLAPE_AC[1] - KLAPE_AC[0], KLAPE_AC[3] - KLAPE_AC[2],
          KLAPE_AC[0], KLAPE_AC[1], KLAPE_AC[2], KLAPE_AC[3], len(dolu)))
    assert not dolu, "klape giris yolunda parca var: %s" % dolu[:5]
    kl = [p for p in PARCALAR if p["grup"] == "KLAPE"]
    S_ = [p for p in PARCALAR if p["grup"] == "SABIT"]
    for aci in (30.0, 60.0, KLAPE_MAX):
        bul = []
        for p in kl:
            v_ = p["wp"].val().rotate(cq.Vector(0.0, KLAPE_EKSEN[0], KLAPE_EKSEN[1]), cq.Vector(1.0, KLAPE_EKSEN[0], KLAPE_EKSEN[1]), aci)
            bul += _kesisim(v_, S_)
        vb = kl[0]["wp"].val().rotate(cq.Vector(0.0, KLAPE_EKSEN[0], KLAPE_EKSEN[1]), cq.Vector(1.0, KLAPE_EKSEN[0], KLAPE_EKSEN[1]), aci).BoundingBox()
        print("   KLAPE %2.0f° ice acik: y %.1f-%.1f · z %.1f…%.1f · sabit parcalarla %d cakisma" % (aci, vb.ymin, vb.ymax, vb.zmin, vb.zmax, len(bul)))
        assert not bul, "klape %.0f derecede carpiyor: %s" % (aci, bul[:5])
    CIK = kut(KOVA[0] - 0.5, KOVA[1] + 0.5, KOVA[2], ps_.ymax, KOVA[4] - 0.5, 450.0).val()
    dolu = _kesisim(CIK, PARCALAR, haric=("robot_cop_kovasi_15L", "robot_cop_poseti", "serit_on_kapak"))
    print("   KOVA BOSALTMA: servis kapagi (%.0f-%.0f) acik, kova + poset kizakta z +450'ye cekilir -> yolunda %d parca" % (SERIT_KAPI[0], SERIT_KAPI[1], len(dolu)))
    assert not dolu, "kova cikis yolunda parca var: %s" % dolu[:5]
    # ---- TAŞIYICI ÇERÇEVE (fırın altı) · yük hesabı [VARSAYIM yükler] ----
    for ad_, k_, _e in TASIYICI:
        b = BB[ad_]
        assert abs(b.xmin - k_[0]) < 0.05 and abs(b.ymax - k_[3]) < 0.05, ad_
    ky0 = min(BB[a].ymin for a, _k, e in TASIYICI if e == "x"); ky1 = max(BB[a].ymax for a, _k, e in TASIYICI if e == "x")
    assert abs(ky1 - (H_B - 1.5)) < 0.05, "kiris ustu dis tavan sacina dayanmiyor"
    assert all(-730.0 + FIRIN_CIKINTI < k_[4] and k_[5] < 0.0 for a, k_, e in TASIYICI if e == "x"), "kiris firin tabaninin disinda"
    for a, k_, e in TASIYICI:
        if e == "y":
            xc_, zc_ = (k_[0] + k_[1]) / 2.0, (k_[4] + k_[5]) / 2.0
            assert any(abs(xc_ - ax) < 0.05 and abs(zc_ - az) < 0.05 for ax, az in AYAK_XZ), "%s altinda ayak yok" % a
    g_ = 9.81; F = EMN * (M_FIRIN + M_RAF) * g_
    zg = (M_FIRIN * ZG_FIRIN + M_RAF * ZG_RAF) / (M_FIRIN + M_RAF)
    pay_on = (zg - TD_Z[1]) / (TD_Z[0] - TD_Z[1])
    w = F * max(pay_on, 1.0 - pay_on) / (W_B - 2500.0)                   # N/mm · fırın boyu 1500'e yayılı
    acik = [TD_X[1] - TD_X[0], TD_X[2] - TD_X[1]]; L_ = max(acik); a_k = W_B - TD_X[2]
    M_ = max(w * L_ ** 2 / 8.0, w * a_k ** 2 / 2.0)
    E_ = 193000.0; I_ = (40.0 ** 4 - 36.0 ** 4) / 12.0; W_ = I_ / 20.0
    sig = M_ / W_; seh = 5.0 * w * L_ ** 4 / (384.0 * E_ * I_)
    R = 1.25 * w * (acik[0] + acik[1]) / 2.0
    A_d = 30.0 ** 2 - 26.0 ** 2; I_d = (30.0 ** 4 - 26.0 ** 4) / 12.0; L_d = TK_Y[0] - (Y_PLINT + 1.5)
    Pcr = math.pi ** 2 * E_ * I_d / L_d ** 2
    print("TASIYICI CERCEVE: kiris %.1f-%.1f × y %.1f-%.1f · dikme x %s z %s · yuk %.0f kg firin + %.0f kg raf × %.1f = %.0f N · agirlik merkezi z %.0f -> on kiris payi %.0f %%"
          % (TK_X[0], TK_X[1], ky0, ky1, "/".join("%.1f" % x_ for x_ in TD_X), "/".join("%.0f" % z_ for z_ in TD_Z), M_FIRIN, M_RAF, EMN, F, zg, 100 * pay_on))
    print("   kiris 40×40×2 (304): w %.2f N/mm · aciklik %.0f · konsol %.0f · M %.0f N·mm · gerilme %.1f MPa (304 akma 205 / 1,5 = %.0f) · sehim %.2f mm (L/500 = %.1f)"
          % (w, L_, a_k, M_, sig, 205.0 / 1.5, seh, L_ / 500.0))
    print("   dikme 30×30×2: en yuklu %.0f N · %.1f MPa · Euler Pcr %.0f kN (boy %.0f) · ayak basina %.0f N (Elesa LV.A-SST tasima yuku KATALOGDAN TEYIT)"
          % (R, R / A_d, Pcr / 1000.0, L_d, R))
    assert sig <= 205.0 / 1.5 and seh <= L_ / 500.0 and R <= Pcr / 3.0
    # ---- v7 · FIRIN ALTI ISI KALKANI: PU yok, hava boşluğu (katılardan) ----
    ay_ = yb("isi_kalkani_ayirma_saci"); isn = yb("isi_kalkani_isinim_saci"); ts_ = yb("tavan_dis_sac")
    BOS = kut(X_F[0] + 1.0, BOLME_X[5], Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -41.5).val()
    pu_ic = _kesisim(BOS, [p for p in PARCALAR if p["mal"] == "pu"])
    yar = sum((b_ - a_) * (ARKA_YARIK_Y[1] - ARKA_YARIK_Y[0]) for a_, b_ in ARKA_YARIK) / 100.0
    print("ISI KALKANI v7 (rapor secenek b): PU 60 YOK · ayirma saci y %.0f-%.0f (x %.0f-%.0f) · isinim saci y %.1f-%.1f (%d takoz) · isinim saci ustu hava %.1f mm (dis tavan saci %.1f) · arka %d yarik %.0f cm² · bosluktaki PU %d parca · firin altinda yalitim = K5/K6 tavan PU %.0f"
          % (ay_.ymin, ay_.ymax, ay_.xmin, ay_.xmax, isn.ymin, isn.ymax, len(TAKOZ_XZ), ts_.ymin - isn.ymax, ts_.ymin, len(ARKA_YARIK), yar, len(pu_ic), Y_TAVAN - Y_TAVAN_F - 1.0))
    assert not pu_ic, "firin alti hava boslugunda PU var: %s" % pu_ic[:3]
    assert abs(ay_.ymin - Y_TAVAN) < 0.05 and isn.ymin > ay_.ymax and ts_.ymin - isn.ymax >= 40.0
    # ---- v7 · SOĞUTMA BÖLGELERİ (katılardan) ----
    for yan, e in EVAP.items():
        L_ = yb("evaporator_%s_lamel" % yan); dv_ = yb("fan_davlumbazi_%s" % yan)
        fb = [yb("fan_%s_%d" % (yan, j_ + 1)) for j_ in range(len(FAN_X))]
        fy0, fy1, fz0, fz1 = min(b.ymin for b in fb), max(b.ymax for b in fb), min(b.zmin for b in fb), max(b.zmax for b in fb)
        ks = [c for c in CEK if c[0] == e["kol"] and c[4] < fy1 and c[4] + HH[c[2]] > fy0]
        ka_z = min(-57.0 - TUB[c[2]] for c in ks)
        gb_ = yb("gider_borusu_%s" % yan); tk_ = yb("damlama_teknesi_%s" % yan)
        print("   SOGUTMA %s (%s arkasi): lamel %.0f × %.0f × %.0f (x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f) · plenum %.0f · fan–lamel %.0f (>= 25) · fan onu %.0f / kutu arkasi %.0f (pay %.0f) · tekne alti %.1f · gider x %.0f -> tava x %.0f"
              % (yan, e["kol"], L_.xlen, L_.ylen, L_.zlen, L_.xmin, L_.xmax, L_.ymin, L_.ymax, L_.zmin, L_.zmax, L_.zmin - Z_ARKA, fz0 - L_.zmax, fz1, ka_z, ka_z - fz1,
                 tk_.ymin, e["gider"][0], e["gider"][1]))
        assert fz0 - L_.zmax >= 25.0 and ka_z - fz1 >= 5.0 and abs(gb_.ymax - tk_.ymin) < 0.05
        assert TAVA[0] < e["gider"][1] - DR_R and e["gider"][1] + DR_R < TAVA[1] and TAVA[4] < GIDER_UC_Z < TAVA[5] and gb_.ymin > TAVA[3]
    for i_, gl in HAVA_GECIS.items():
        for y0_, y1_ in gl:
            dol = _kesisim(kut(BOLME_X[i_] - 0.5, BOLME_X[i_] + BOLME + 0.5, y0_ + 1.0, y1_ - 1.0, HAVA_Z[0] + 1.0, HAVA_Z[1] - 1.0).val(), PARCALAR)
            assert not dol, "B%d hava gecisi (%.0f-%.0f) kapali: %s" % (i_ + 1, y0_, y1_, dol[:3])
    print("   HAVA GECISLERI (arka, z %.0f…%.0f, acik oldugu katidan olculdu): %s · B3 (K3 | K4 sicak) kapali"
          % (HAVA_Z[0], HAVA_Z[1], " · ".join("B%d %s" % (i_ + 1, " + ".join("%.0f-%.0f" % g for g in gl)) for i_, gl in sorted(HAVA_GECIS.items()))))
    cu_ = yb("sogutma_grubu_kondenser"); at_ = yb("kondenser_atis_kanali")
    print("   SECOP CU NLE8.8CN: kondenser ustu %.1f · K4 ara katman %.1f-%.1f · atis kanali x %.1f-%.1f y %.1f-%.1f z %.1f…%.1f (VENT x %.1f-%.1f) · plint izgarasi %d yarik"
          % (cu_.ymax, yb("k4_ara_sac_alt").ymin, yb("k4_ara_sac_ust").ymax, at_.xmin, at_.xmax, at_.ymin, at_.ymax, at_.zmin, at_.zmax, K4X + 60.0, K4X + K4W - 60.0, len(PLINT_IZGARA)))
    # ---- SOĞUTMA (bilgi · VARSAYIM) · iletimle ısı kazancı kaba tahmini ----
    k_pu, T_ic, T_ort, T_fir, T_sic = 0.024, 3.0, 25.0, 60.0, 35.0     # W/m·K PU [VARSAYIM] · +3 °C · ortam · fırın tabanı · Secop bölmesi [VARSAYIM]
    Lz = (-Z_ARKA - 41.5) / 1000.0
    xa, xk, xf = (K4X - X_IC0S - 1.0) / 1000.0, (K4_SAG - K4X) / 1000.0, (BOLME_X[5] - BOLME_X[3] - BOLME) / 1000.0
    ha, hk, hf, hs = (Y_TAVAN - Y_TABAN) / 1000.0, (Y_TAVAN - yb("k4_ara_sac_ust").ymax) / 1000.0, (Y_TAVAN_F - Y_TABAN) / 1000.0, (yb("k4_ara_sac_alt").ymin - Y_TABAN) / 1000.0
    yuz = [("on kapaklar", xa * ha + xk * hk + xf * hf, 0.0375, T_ort), ("arka", xa * ha + xk * hk + xf * hf, 0.0375, T_ort),
           ("tavan K1-K4", (xa + xk) * Lz, 0.0575, T_ort), ("tavan firin alti (hava boslugu altinda)", xf * Lz, 0.059, T_fir),
           ("taban K1-K3", xa * Lz, 0.039, T_ort), ("K4 depo tabani (Secop ustu)", xk * Lz, 0.028, T_sic), ("taban K5-K6", xf * Lz, 0.039, T_ort),
           ("sol yan", ha * Lz, 0.060, T_ort), ("B6 (serit)", hf * Lz, 0.033, T_ort), ("B3 + B4 (Secop bolmesi yanlari)", 2 * hs * Lz, 0.033, T_sic)]
    Q = sum(k_pu * A_ * (Td - T_ic) / t_ for _a, A_, t_, Td in yuz)
    import re as _re
    lam = [p for p in PARCALAR if _re.match(r"^evaporator_(sol|sag)_lamel$", p["ad"])]; fan = [p for p in PARCALAR if _re.match(r"^fan_(sol|sag)_\d$", p["ad"])]
    ev = sum(BB[p["ad"]].xlen * BB[p["ad"]].ylen for p in lam) / 1e6
    print("SOGUTMA v7: %d bolge · lamelli evaporator on yuzu %.3f m² · %d fan ebm-papst 4414 FL (%.1f W) · Secop CU NLE8.8CN 737 / 688 / 586 W @ −10 °C (25 / 32 / 43 °C) · gereken 552–661 W @ 32 °C (sogutma_hesabi_v1) · duvar iletimi ~%.0f W (PU k %.3f, ortam %.0f, firin alti %.0f °C VARSAYIM)"
          % (len(lam), ev, len(fan), 1.2 * len(fan), Q, k_pu, T_ort, T_fir))
    assert len(lam) == 2 and len(fan) == 4 and not [p for p in PARCALAR if p["ad"].startswith(("fan_K", "evaporator_K"))]
    di = 14 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1221")]); dq = 10 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1222")])
    reed = len([p for p in PARCALAR if p["ad"].endswith(("_reed_kapali", "_reed_acik"))]); role = len([p for p in PARCALAR if p["ad"].startswith("role_")])
    print("PLC G/C: reed %d / DI %d · role %d + surucu 2 (yon + etkin VARSAYIM) / DQ %d" % (reed, di, role, dq))
    assert reed <= di and role + 2 <= dq
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
    L = [(p, p["wp"].val()) for p in PARCALAR if "_top_" not in p["ad"] and "_kutu330_" not in p["ad"] and "_tatlikabi_" not in p["ad"]]
    L = [(p, v, v.BoundingBox()) for p, v in L]
    bul, aday = _kesis(L, L, esik)
    print("CAKISMA TARAMASI (kapali): %d parca · %d aday · %d gercek kesisim (> %.0f mm3) · %.0f sn" % (len(L), aday, len(bul), esik, _t.time() - t0))
    import re as _re
    tur = {}
    for v, a, b in bul:
        k = tuple(sorted(_re.sub(r"^CEK_K\d_[a-z0-9]+_\d+_", "", x) for x in (a, b)))
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
    ad = _re.sub(r"^CEK_K\d_[a-z0-9]+_\d+_", "", p["ad"])
    ad = _re.sub(r"_(\d+|sol|sag|a|b)$", "", ad)
    tanim = {"sac": "304 sac · lazer + büküm", "pu": "PU köpük (gövdeyle birlikte enjeksiyon)", "celik": "304 · lazer / lama",
             "aluminyum": "alüminyum", "koyu": "", "plastik": "", "conta": "", "kanal": "PVC", "kart": "", "motor": "", "silikon": "gıda silikonu",
             "bakir": "", "izgara": "304 lama", "pom": "", "poset": "LDPE"}.get(p["mal"], p["mal"])
    return ad.replace("_", " "), 1, tanim, "zarf " + olcu


# satin alinan urunun ALT GOVDELERI ve ayni kalemin ikinci ornekleri: BOM.csv'de listelenir, OZET'te SAYILMAZ
# (adet zaten ana kalemde: ray "2 / cekmece", reed "2 / cekmece", role "24", fan "6" ...)
ALT_KURAL = [
    (r"_on_(pu|ic_sac_1\.0)$", "çekmece önü / kapak katmanı"), (r"^k4_kapak_depo_(pu|ic_sac_1\.0)$", "kapak katmanı"),
    (r"_kutu_(arka|on)_1\.0$", "çekmece kutusu"), (r"_on_baglanti_sag$", "ön bağlantı köşesi"), (r"_ray_adaptor_sag$", "ray adaptör lamı"),
    (r"_ray_dis_sag$", "Accuride DZ3832-0070"), (r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç eleman)"), (r"_ray_ara_(sol|sag)$", "Accuride DZ3832-0070 (ara eleman)"), (r"_reed_acik$", "Littelfuse 59135"),
    (r"_motor_(mili|gobegi|govde)$", "Transmotec PD3665"), (r"_enkoder_kapagi$", "Transmotec PD3665"),
    (r"^role_(0[2-9]|[1-9]\d)$", "Phoenix PLC-RSC"), (r"^kablo_kanali_(K[2-6]|ust|ust_F)$", "kablo kanalı"),
    (r"^evaporator_sag_lamel$", "Evaporatör lamelli"), (r"^evaporator_(sol|sag)_(yan_sac|dirsek)_[ab]$", "Evaporatör lamelli"),
    (r"^evaporator_(sol_askisi_2|sag_askisi_[12])$", "Evaporatör askısı"), (r"^damlama_teknesi_sag$", "Damlama teknesi"), (r"^fan_davlumbazi_sag$", "Fan davlumbazı"),
    (r"^fan_(sol_2|sag_[12])$", "ebm-papst 4414 FL"), (r"^gider_borusu_sag$", "Gider borusu"), (r"^isi_kalkani_takozu_[1-9]$", "Isı köprüsü kesici takoz"),
    (r"^isi_kalkani_sag_sac$", "Isı kalkanı yan sacı (× 2)"),
    (r"^ayak_([1-9]|1\d)$", "Elesa LV.A-SST"), (r"^din_ray_1$", "DIN ray"),
    (r"_serit_bolmesi_([1-9]|1\d)$", "şerit + itici takımı"), (r"_itici(_yayi)?_\d+$", "şerit + itici takımı"),
    (r"^sogutma_grubu_(kondenser|fan|kompresor)$", "Secop CU NLE8.8CN"), (r"^plc_SM1221_DI16_[bc]$", "SM1221"), (r"^yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)"),
    (r"^(yan_pu_sol|yan_pu_sol_on|arka_pu_37\.5|arka_pu_F|taban_pu|taban_pu_F|tavan_pu_F|bolme_\d_pu|bolme_5_pu_ust|k4_ara_pu)$", "PU köpük gövde"),
    (r"^tasiyici_kiris_arka$", "Taşıyıcı kiriş 40 × 40 × 2"), (r"^tasiyici_capraz_[1-9]$", "Taşıyıcı çapraz 30 × 40 × 2"), (r"^tasiyici_dikme_[1-9]$", "Taşıyıcı dikme 30 × 30 × 2"),
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
        if "_top_" in p["ad"] or "_kutu330_" in p["ad"] or "_tatlikabi_" in p["ad"]:
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
    return "SATIN ALMA" if any(s in ad for s in ("Accuride", "Transmotec", "Littelfuse", "Siemens", "Mean Well", "Electromen", "Phoenix", "Secop", "ebm-papst", "Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC", "çöp kovası", "poşeti", "Yaylı menteşe")) else "ÜRETİM"


if __name__ == "__main__":
    oz = modul(); denetim(oz)
    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v10")))
