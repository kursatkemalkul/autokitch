# -*- coding: utf-8 -*-
"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v11 (29 Eyl 2026 · yap_store_cad_v11.py): FIRIN ALTI AYAKLARI KENARDA (soldaki gibi z −110 / −760) · K4|K5 BÖLMESİNİN ÖNÜ KAPALI (kademe sacı aynası)
v10: ÜRETİM MODELİ v10 (29 Eyl 2026 · yap_store_cad_v10.py): STROK 700 · HER ŞEY TEPSİDE (robot parmakla alır, itici yok) · 21 çekmece (lahmacun 10 × 42 · pide 7 × 25 · içecek 3 × 48 · tatlı 1 × 12) · SİMETRİ: K1–K3 5'er aynı çizgide, K5–K6 3'er aynı çizgide · kutular 540
v9: ÜRETİM MODELİ v9 (28 Eyl 2026 akşam · yap_store_cad_v9.py): KAPAK İÇ SACI TEK PARÇA (kanal dışı halka = dış sacın arka dönüşü) · ISI KALKANI SOL SACI TEK PARÇA (x 2534, taşıyıcı çerçevenin dışında) · BOM 1_STORE_v12 · önceki store_cad_v8.py
v8: ÜRETİM MODELİ v8 (28 Eyl 2026 gece) · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §2.1 · Kemal: "fırının ön yüzü
    sınır yüzey, her şeyi o yüzeye getireceğiz … önden tertemiz düz yüzeyler … içeride havada kalan parça olmasın")
v8: bütün önler +39…+79 (fırın ön yüzü düzlemi), arka −830 SABİT → derinlik 909 · çerçeve +23…+24 (430 ferritik) · kabuk ön kenarı +39 · seçenek (a):
    kutu öne 79 uzar, tepsi kutunun önüne göre, avara −73 sabit → strok 628 · avara kolu 3 mm flanşlı · K4 keşif B §6.5 Öneri 1 (Secop 180°, emiş plintten
    → taban → arka plenum, atış K4 kapağı ızgarasından, tava K4 önünde, gider PU içinde U-sifon) · dolabın altında ayak + plint dışında parça YOK ·
    plint onyuz_plint +17,5…+19 + yan dönüşler · şerit dönüşü 40 · havada parça 0 (beyaz liste: bilyeli ray ara elemanı). Önceki: store_cad_v7.py
    (yap_store_cad_v8.py) · BOM 1_STORE_v11
v8 DENETÇİ DÜZELTMELERİ (28 Eyl sabah · bağımsız denetim 6 ORTA + 9 KÜÇÜK · on_duzlem_v63/rapor_B.md): K4 depo = elle çekilen ÇEKMECE
    (Accuride DZ3832-TR bas-aç) · K4 soğutma + şerit servis kapağı = gizli klipsli SÖKÜLÜR panel (menteşeli 40'lık kapak 3 mm derzde komşu öne
    çarpıyordu) · Secop 2 × L 40×40×3 montaj rayında, ayırma saclarına 5 mm + EPDM sünger conta, önden servis yolu · gider SÜREKLİ ≥ %1 eğim
    (sifon yok, ördek gagası kuru kapan), bölme geçişleri kılıflı · avara kolu 2 mm, iç raya 1,0 · avara 2 × MR126, Ø6 mil · sensör lamı
    kulak bindirmeli + 16 mm tırnak · klape menteşe kıvrımları · 45° düşme oluğu · K4 paneli lazer yarıklı · plint üst flanşlı, kısa yarıklı
    ızgara · pano havalandırması · adlar: onyuz_cerceve_saci_1.0, kasa_yan_dis_sac_*, kasa_yan_on_donus_sol
v7 (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1 · Kemal: "öğrendiğin yeter,
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
KOORDİNAT: hat ile aynı — x 0..4000 (dolap), y 0..788 (düz çizgi) · v8: z +79 = ÖN DÜZLEM (bütün önlerin dış yüzü = fırın ön yüzü), z 0 = v7 ön yüzü
           (iç düzen, kutu arkası, motor, evaporatör bu referansta DEĞİŞMEDİ), −830 arka dış yüz (Z_ARKA_DIS) → derinlik 909.
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
KOLON = [[(5, "lahm")], [(5, "lahm")], [(5, "hamur")], [(2, "hamur"), (1, "tatli")], [(3, "ic1")]]   # v10: K5 alttan üste: pide, pide, tatlı
# v10 · SİMETRİ (Kemal): kolon grubunda HER çekmecenin açıklığı aynı → ön çizgileri kolonlar arasında hizalı. En alt ve en üst ön eşit olacak şekilde başlangıç kotu:
#       K1–K3: 5 × (75 + 33) = 540 ≤ 558 → başlangıç 200,5 (alt ön 164,5 · orta 105 · üst 167,5) · K5–K6: 3 × (130 + 33) = 489 ≤ 498 → 191,5 (üstü fırın ısı kalkanı: 60 fazla)
HH_KOL = {"K1": 75.0, "K2": 75.0, "K3": 75.0, "K5": 130.0, "K6": 130.0}
Y0_KOL = {"K1": 200.5, "K2": 200.5, "K3": 200.5, "K5": 191.5, "K6": 191.5}
KOLON_X = {"K1": XI, "K2": XI + (WO + BOLME), "K3": XI + 2.0 * (WO + BOLME), "K5": 2535.0, "K6": 3190.0}   # 62,5 · 717,5 · 1372,5 · 2535 · 3190 (SPEC)
KOLON_W = {"K6": 585.0}                                                     # K6 3190–3775 (SPEC) · diğerleri WO 620
K4_CEK = []                                                                 # v6: K4'te dar içecek YOK (SPEC)
KAPAK_X = {"K1": (0.0, 698.5), "K2": (701.5, 1353.5), "K3": (1356.5, 2008.5), "K4": (2011.5, 2516.0),
           "K5": (2519.0, 3171.0), "K6": (3174.0, 3791.0), "SERIT": (3794.0, 4000.0)}
# tam kaplama (v5 kuralı): her ön kendi açıklığının 16 dışına taşar, kolon önleri arası 3. SPEC'teki "K4 2011,5–2500" kolonun kendisi;
# K4 önü 2516'ya uzar ki K5 önü de 16 taşsın (2519 = 2535 − 16) — 2500'de bitseydi K5 önü solda 32 taşardı.
H_B, W_B = 788.0, 4000.0                       # v6: DÜZ ÇİZGİ 788 · dolap 0–4000 (pafta v7'deki H_B 1060 / W_B 2500 eski hattın)
Z_ARKA_DIS = -830.0                             # v8: arka dış yüz SABİT (SPEC_on_duzlem_v63 §1) — pafta DZ'sinden BAĞIMSIZ (pafta 909 olsa da B'nin arkası kaymaz)
DZ = -Z_ARKA_DIS                                # 830: kabuk kodunda arka yüz −DZ (DERİNLİK DEĞİL — derinlik DERINLIK = 909)
ON_ALT, ON_UST = 126.0, H_B - 3.0               # bütün kolonlarda ön yüzün alt ve üst çizgisi: 126 · 785
GN_H = 230.0                                    # K4 kaşar + sucuk deposu yüksekliği (GN 1/1-100 + raf + GN 1/2-100) — v5 ile aynı
BOLME_X = (KOLON_X["K1"] + WO, KOLON_X["K2"] + WO, KOLON_X["K3"] + WO, 2500.0, KOLON_X["K5"] + WO, KOLON_X["K6"] + KOLON_W["K6"])
#           B1 682,5 · B2 1337,5 · B3 1992,5 · B4 2500 (K4 | K5) · B5 3155 · B6 3775 (K6 | şerit = soğuk zarfın sağ duvarı) — hepsi 35
SERIT = (BOLME_X[5] + BOLME, W_B)               # 3810–4000 · soğuk DEĞİL (robot çöpü)
X_F = (2534.0, 3793.0)                          # v9: 2517 → 2534 — sol sac taşıyıcı dikme / çapraz düzleminin (2502,5–2532,5) dışında, B4 sağ sacının üstü (tek parça) · fırın 2500–4000
FIRIN_CIKINTI = 79.0                            # firin_tp10_cad ZS: fırın gövdesinin ön yüzü (y ≥ 788) — v8: B'nin ön düzlemi de bu
Z_ON = FIRIN_CIKINTI                            # v8 · ÖN DÜZLEM +79: bütün ön panellerin / kapakların dış yüzü (montaj sözleşmesi: SC.Z_ON1 = FT.ZS)
ON_UZAMA = Z_ON                                 # v8: v7'de ön yüz z 0'daydı → her ön katman +79 (iç düzen yerinde)
DERINLIK = Z_ON - Z_ARKA_DIS                    # 909

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
Z_ON0, Z_ON1 = Z_ON - 40.0, Z_ON                # v8: +39 … +79 (v7 −40 … 0) · 40 = dış 304 1,5 + PU 37,5 + iç 304 1,0
Z_CON0, Z_CON1 = Z_ON0 - 15.0, Z_ON0            # v8: +24 … +39 · fitil bandı (geçmeli manyetik profil)
Z_CER0, Z_CER1 = Z_CON0 - 1.0, Z_CON0           # v8: +23 … +24 · ön çerçeve sacı 1,0 — 430 FERRİTİK (manyetik fitil 304'e tutmaz)
ZP1_ON = Z_ON0 - 1.5                            # v8: +37,5 · ön dönüşlerin arka yüzü = PU'nun önü (v7 −41,5)
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
TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=5, ax=105.0, az=120.0, td=600.0),     # v10: 5 × 5 = 25 (v9 5 × 4 · 130) · aralık yan 10 / ön-arka 25
       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=7, ax=88.0, az=85.0, td=600.0)}      # v10: 6 × 7 = 42 (v9 6 × 6 · 90) · aralık yan 13 / ön-arka 10
# v10 · kutu ve tatlı da TEPSİDE (robot parmakla alır; v9 şerit + yaylı itici KALKTI): silindir ürün, çukur r + 1
SIL = {"ic1": dict(r=33.0, h=115.0, cr=34.0, nx=6, nz=8, ax=82.0, az=76.0, td=608.0, ad="kutu330"),   # 6 × 8 = 48 · aralık yan 16 / ön-arka 10
       "tatli": dict(r=47.5, h=60.0, cr=50.0, nx=4, nz=3, ax=105.0, az=120.0, td=600.0, ad="tatlikabi")}   # 4 × 3 = 12 (2 gün 11) · pide tepsisi hatvesi
TUB = {"hamur": 540.0, "lahm": 540.0, "icecek": 540.0, "ic1": 540.0, "ic1d": 540.0, "tatli": 540.0}   # v10: TEK KUTU (iç 618) · arka −597 · K2/K5 fan önü 19
TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6, nx=2)    # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104 · v6: 2 şerit × 6 = 12 (2 gün 11)
# v6: K4_YO (K4 dar içecek çekmeceleri) kalktı
ICECEK_KAT, ICECEK = 115.0, dict(r=33.0, ax=82.0, az=75.0)
# FİTİL — geçmeli manyetik profil (u: açıklıktan DIŞARI, z mutlak). Yol açıklık kenarının 4 mm dışında.
FITIL_G = 4.0
FITIL = [(-2.0, -31.7), (2.0, -31.7), (2.0, -33.0), (3.15, -34.0), (2.0, -35.2), (2.0, -40.0), (6.0, -40.0), (6.0, -42.0), (8.0, -42.0), (8.0, -50.0),
         (10.5, -50.0), (10.5, -55.0), (-10.5, -55.0), (-10.5, -50.0), (-8.0, -50.0), (-8.0, -42.0), (-6.0, -42.0), (-6.0, -40.0), (-2.0, -40.0),
         (-2.0, -35.2), (-3.15, -34.0), (-2.0, -33.0)]
KANAL = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]     # kapak iç sacındaki geçme kanalı 6,4 × 8,4
FITIL = [(u_, z_ + ON_UZAMA) for u_, z_ in FITIL]; KANAL = [(u_, z_ + ON_UZAMA) for u_, z_ in KANAL]   # v8: mutlak z listeleri +79 (fitil +24…+47,3)
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
Z_MOTOR, Z_AVARA = -769.0, -1.0        # motor Ø36: −787 … −751 (arka duvar −790, ayak sacı −790 … −787)
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
        yo, n = Y0_KOL[kol], {}                                          # v10 (v9: YUZ0 + BIND = 182,5)
        for adet, tip in gruplar:
            for _ in range(adet):
                n[tip] = n.get(tip, 0) + 1
                out.append((kol, "CEK_%s_%s_%d" % (kol, tip, n[tip]), tip, cx, yo))
                yo += HH_KOL[kol] + 2 * BIND + FUGA                         # v10: kolon başına tek açıklık
    return out, BOLME_X[2] + BOLME                                        # v6: K4 = B3 bölmesinin sağı (2027,5)


CEK, K4X = kolonlar()
HH_C = {c[1]: HH_KOL[c[0]] for c in CEK}                                  # v10: çekmece kodu → açıklık yüksekliği
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
SERIT_DONUS = 40.0                                       # v8: 18 → 40 · şerit önleri de +39…+79 tava (sol uçla simetri; sağ yan dış sac +39'da biter)
KOVA = (3822.5, 3987.5, 126.0, 426.0, Z_ON - SERIT_DONUS - 2.0 - 400.0, Z_ON - SERIT_DONUS - 2.0)   # v8: z −363…+37 (önü servis kapağının 2 arkası) · 165 × 300 × 400 ≈ 15 L (ölçü v7 ile aynı)
KOVA_T = 2.5                                             # PP duvar [VARSAYIM] · taban 3
# v8: SERIT_DONUS yukarıda (KOVA'dan önce) tanımlı — 40
SERIT_KAPI = (ON_ALT, 560.0)                             # servis kapağı: kova (126–426) öne çekilip çıkarılır
SERIT_PANEL = (563.0, ON_UST)                            # sabit üst panel (klape açıklıklı)
KLAPE_AC = (3840.0, 3970.0, 610.0, 740.0)                # klape açıklığı 130 × 130 [VARSAYIM: Ø95 pide topu + tutucu] · orta 3905 = kova ortası
KLAPE_EKSEN = (748.0, Z_ON - 7.0)                         # v8: +72 · yaylı menteşe ekseni (y, z) — klape levhasının 4 arkası (SPEC "klape y ~745")
KLAPE_MAX = 90.0                                         # derece · içe (−z) açılır · mekanik stop (denetimde 30 / 60 / 90 taranır)
AYAK_Z = (-110.0, -760.0)                                            # v11: BÜTÜN ayaklar bu iki sırada (Kemal: fırın altı da soldaki gibi kenarda)
AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in AYAK_Z] + [(x_, z_) for x_ in TD_X for z_ in AYAK_Z]
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
# v8 · K4 SICAK BÖLME = keşif B §6.5 ÖNERİ 1 (SPEC §2.1): Secop 180° döner (kondenser ARKADA), arka plenum + iki yan emiş şeridinden emer
#      (taban delikleri ← plint boşluğu ← plint emiş ızgarası), önden K4 soğutma kapağının ızgarasından atar · tava K4 önünde, tabanda · gider boruları
#      v8b: soğuk bölmelerin arkasından SÜREKLİ EĞİMLE (≥ %1, sifon YOK · ördek gagası = kuru kapan) → dolabın altında ayak + plint dışında HİÇBİR şey yok
DR_Z, DR_R, DR_KILIF = -690.0, 6.0, 8.0       # v8b · gider Ø12 PVC: tekne çıkışı z (tekne −756…−660) · kılıf Ø16 (iç Ø12 = boru dış çapı, kayar geçme)
DR_EGIM = 0.010                               # v8b: SÜREKLİ İNİŞ, her koşuda en az %1 (denetçi ORTA 5: v8'de U-sifon köpük içinde, eğim 0, durgun su)
DR_Y0 = {"sol": 191.0, "sag": 190.0}          # tekne altında yatay koşu başı: K3 / K5 en alt çekmecesinin kayışının (alt koşu 197,3) altından ≥ 1 mm
DR_Z_DON, DR_Z_ON = -645.0, -60.0             # bölme içinde öne dönüş sonu (perde −654 önü · B4 dikmesi −635 arkası) · K4'te çıkış z (tava üstü)
DR_X_YUK = {"sol": 2010.0, "sag": 2517.0}     # bölme ortası: B3 (1992,5–2027,5) · B4 (2500–2535) — PU içinde KILIFLI (boru çekilip değiştirilir)
DR_X_UC = {"sol": 2042.0, "sag": 2485.0}      # K4 yan emiş şeridinde öne koşu x · ucunda ördek gagası (tava ağzının 1,5 üstü)
VALF = (7.0, 10.0)                            # Minivalve DU 120.001 flanşlı ördek gagası (Ø12) + tutucu: zarf Ø14 × 10 [ölçü VARSAYIM · katalogdan teyit]
TAVA = (2031.0, 2496.0, 124.5, 157.5, -91.0, 24.0)    # v8b: 33 yüksek (gider sürekli eğimi için 7 alçak) · 9 öne (ön Secop rayına 5) · brüt 1,6 L · servis paneli sökülünce öne çekilir
SECOP_Z = (-554.0, -104.0)                    # Secop CU NLE8.8CN taban 450 boyu (VARSAYIM) · kondenser ARKADA (−554…−494) · kompresör önde
SECOP_X = ((K4X + K4_SAG) / 2.0 - 175.0, (K4X + K4_SAG) / 2.0 + 175.0)   # 2088,75–2438,75 (ortada · iki yanda 59,75'lik emiş şeridi)
PERDE_Z = -655.0                              # pano ↔ emiş plenumu perdesi (arka yüzü) · pano en önü −667 (güç kaynağı) → 12 pay · plenum 101
TAKOZ_H = 4.0                                 # titreşim pedi 40 × 30 × 4 (Secop tabanı ↔ montaj rayı)
SECOP_RAY_T = 3.0                             # v8b · Secop montaj rayı L 40×40×3, yatay kol y 124,5–127,5 (denetçi ORTA 2: yük yolu raylar → B3 / B4 duvarları)
SECOP_BOS = 5.0                               # v8b · ünite ↔ ayırma sacları / ara sac boşluğu — EPDM sünger contayla kapalı, RİJİT TEMAS YOK
S0_K4 = Y_PLINT + 1.5 + TAKOZ_H + 297.0 + 8.0 # 433,5 · K4 ARA KATMAN KOTU (v7 ile aynı, DEĞİŞMEZ) → rayın 3 mm'sini üst boşluk karşılar (8 → 5)
SECOP_Y0 = Y_PLINT + 1.5 + SECOP_RAY_T + TAKOZ_H   # 131,5 · Secop taban altı
RAY_SEC = {"arka": (SECOP_Z[0] - SECOP_BOS - SECOP_RAY_T, SECOP_Z[0] - SECOP_BOS - SECOP_RAY_T + 40.0, -1),   # z −562…−522 · dik kol arkada (−562…−559)
           "on": (SECOP_Z[1] + SECOP_BOS + SECOP_RAY_T - 40.0, SECOP_Z[1] + SECOP_BOS + SECOP_RAY_T, 1)}     # z −136…−96 · dik kol önde · SERVİSTE SÖKÜLÜR
PED_Z = {"arka": (SECOP_Z[0] + 2.0, SECOP_Z[0] + 32.0), "on": (SECOP_Z[1] - 30.0, SECOP_Z[1])}    # ped 40 × 30: taban içinde, rayın yatay kolu üstünde


def _pencereler(a, b, n, kopru):
    w = (b - a - (n - 1) * kopru) / n
    return [(a + i * (w + kopru), a + i * (w + kopru) + w) for i in range(n)]


EMIS_KOPRU = 20.0                             # v8b: emiş pencereleri arası en az 20 köprü (denetçi ORTA 2: v8'de Secop altındaki ada 2 × 8 mm'ye asılıydı)
_ES = (RAY_SEC["arka"][1] + 4.0, RAY_SEC["on"][0] - 4.0)          # şerit pencereleri z −518…−140 (rayların altı dolu)
EMIS_DELIK = ([(x0_, x1_, PERDE_Z + 5.0, RAY_SEC["arka"][0] - 4.0) for x0_, x1_ in _pencereler(K4X + 4.5, K4_SAG - 4.5, 3, EMIS_KOPRU)]            # plenum altı
              + [(K4X + 4.5, SECOP_X[0] - SECOP_BOS - 1.5 - 4.0, z0_, z1_) for z0_, z1_ in _pencereler(_ES[0], _ES[1], 3, EMIS_KOPRU)]             # sol şerit
              + [(SECOP_X[1] + SECOP_BOS + 1.5 + 4.0, K4_SAG - 4.5, z0_, z1_) for z0_, z1_ in _pencereler(_ES[0], _ES[1], 3, EMIS_KOPRU)])          # sağ şerit
PANO_YARIK = [(2070.0 + 100.0 * i_, 2150.0 + 100.0 * i_) for i_ in range(4)]   # v8b · pano havalandırması (denetçi KÜÇÜK 14): 4 × 80 × 12 tabanda + perde üstünde
PANO_YARIK_Z, PANO_YARIK_Y = (-731.0, -719.0), (405.0, 417.0)
PLINT_IZGARA = [(1819.75 + 128.0 * c_, 1939.75 + 128.0 * c_, 21.0 + 15.0 * r_, 31.0 + 15.0 * r_) for c_ in range(7) for r_ in range(6)]   # v8b: 6 × 7 yarık 120 × 10 · köprü 5 / 8 (denetçi KÜÇÜK 11)
PLINT_FLANS = 25.0                            # v8b: plint üst flanşı (taban dış sacına M5 perçin somun) — v8'de yalnız 1,5 kenar temasıydı
K4_YARIK = [(2038.25 + 153.0 * c_, 2183.25 + 153.0 * c_, 165.0 + 13.0 * r_, 173.0 + 13.0 * r_) for c_ in range(3) for r_ in range(20)]    # v8b · K4 paneli lazer yarık 145 × 8 · köprü 5 / 8 (denetçi KÜÇÜK 9)
DEPO_KUTU_D, DEPO_KUTU_UST = 545.0, 600.0     # v8b · K4 depo çekmece kutusu boyu (GN 1/1 530 + pay) · yan duvar üstü (raf tutucuları taşır)
KLAPE_KIVRIM = ((0.0, 24.0), (48.0, 72.0), (96.0, 120.0))   # v8b · klape levhasının menteşe kıvrımları (pim başından) · yaprağınkiler aralarında, 0,5 boşlukla
KOL_T = 2.0                                   # v8b: avara kolu 2 mm sac (denetçi ORTA 3: 3 mm'de iç raya 0,1 kalıyordu) · L flanş + ön flanş + arka kulak aynı sactan
KOL_BOS = 1.0                                 # v8b: kol ↔ iç ray boşluğu (kol ↔ avara 1,3)
KOL_FLANS_Y = 20.0                            # v8b: ön flanş 20 (y) × 12,7 — 2 × PEM FH4-M3 gömme başlı saplama (denetçi KÜÇÜK 10) · tavanın 1 altında biter
KOL_KULAK = 20.0                              # v8b: kolun arka kulağı (z −101…−81) sensör lamının üstüne biner, 2 × M3 perçin (denetçi ORTA 4)
AVARA_MIL_R = 3.0                             # v8b: avara mili Ø6 (v8 Ø5, tepe 182 MPa) · avara 2 × MR126-2RS 6 × 12 × 4 (2 × 625 = 10, 9,5'lik göbeğe sığmıyordu)
LAM_TIRNAK = 16.0                             # v8b: sensör lamı arka tırnağı 16 geniş (v8 6,35: 2 × M4 deliğe kenar 0,9 kalıyordu)
# v8b · soğutma yükü: _local/sogutma_hesabi_v1 v8 geometrisiyle (iç derinlik +79, kutular +79, sol yan PU 60, 4 × 4414 FL, fırın altı hava boşluğu) yeniden
#       koşuldu (on_duzlem_v63/sogutma_B_v8.py) — 32 °C gereken (18 sa · %10 pay): boş gün · dolum günü · dolum + sıcak hamur
SOG_V8 = dict(bos=476.6, dol=585.9, dol_s=641.3, secop_tablo=688.0, secop_foy=661.0)   # v1 aynı koşuda 457 / 566 / 621
KOL_FL = 12.0                                 # v8: avara kolu üst flanşı (L kesit) · kolun üst kenarında, +x yönünde (avara / mıknatıs yolunun üstü)
LAM_H = 6.0                                   # v8: sensör lamı dik kolu (L 6,35 × 8 × 2) — 700 açıklıkta düz lamın sehimi ~3,8 → ~0,2 mm
ARKA_YARIK = [(2540.0 + 205.0 * i_, 2725.0 + 205.0 * i_) for i_ in range(6)]              # fırın altı hava boşluğu arka yarıkları (185 × 30)
ARKA_YARIK_Y = (748.0, 778.0)
ISINIM_Y = (740.0, 740.8)                     # parlak paslanmaz ışınım sacı 0,8 · takozlar 729–740
TAKOZ_XZ = [(x_, z_) for x_ in (2700.0, 3000.0, 3350.0, 3650.0) for z_ in (-700.0, -250.0, 10.0)]   # v8: ışınım sacı +35,5'e uzadı → önde 3. sıra (konsol 25)
X_IC0S = 61.5                                 # v7: sol iç sac 61,5–62,5 (PU 60) · K1 ray duvarı 62,5


def hava_gecis(i, g):
    """v7 · bölme i'nin kesim gövdesine (kablo geçişi g) arka hava geçişlerini ekler"""
    for y0_, y1_ in HAVA_GECIS.get(i, ()):
        g = g.union(kut(BOLME_X[i] - 1.0, BOLME_X[i] + BOLME + 1.0, y0_, y1_, HAVA_Z[0], HAVA_Z[1]))
    return g




def gider_noktalari(yan):
    """v8b · gider borusu ekseni: tekne altı → soğuk bölme arkası (z −690, en alt kayışın altı) → bölme (kılıflı) → K4 emiş şeridi → çek valf.
    Her adımda en az DR_EGIM iner (sifon YOK — durgun su kalmaz; kuru kapan: ördek gagası)"""
    e = EVAP[yan]; gx = e["gider"][0]; ty = e["y"][0] - 15.0
    xy, xu = DR_X_YUK[yan], DR_X_UC[yan]
    P = [(gx, ty, DR_Z), (gx, DR_Y0[yan], DR_Z)]
    for x_, z_ in ((xy, DR_Z), (xy, DR_Z_DON), (xu, DR_Z_DON), (xu, DR_Z_ON)):
        x0_, y0_, z0_ = P[-1]
        P.append((x_, y0_ - DR_EGIM * math.hypot(x_ - x0_, z_ - z0_), z_))
    P.append((xu, TAVA[3] + 1.5 + VALF[1], DR_Z_ON))
    return P


def yol_y(P, x, z):
    """eksen üstünde (x, z) noktasının y'si (x ya da z boyunca koşan eğimli parçada doğrusal)"""
    for a, b in zip(P, P[1:]):
        if abs(a[2] - b[2]) < 1e-6 and abs(a[2] - z) < 1e-6 and abs(a[0] - b[0]) > 1e-6 and min(a[0], b[0]) - 1e-6 <= x <= max(a[0], b[0]) + 1e-6:
            return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
        if abs(a[0] - b[0]) < 1e-6 and abs(a[0] - x) < 1e-6 and abs(a[2] - b[2]) > 1e-6 and min(a[2], b[2]) - 1e-6 <= z <= max(a[2], b[2]) + 1e-6:
            return a[1] + (b[1] - a[1]) * (z - a[2]) / (b[2] - a[2])
    raise ValueError("eksende degil: %s" % str((x, z)))


def yol_kati(P, r):
    """v8b · eksen noktalarından boru katısı: silindirler + iç köşelerde küre (sürekli dirsek)"""
    s = None
    for a, b in zip(P, P[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        c = cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v)
        s = c if s is None else s.fuse(c)
    for p in P[1:-1]:
        s = s.fuse(cq.Workplane("XY").sphere(r).translate(p).val())
    return cq.Workplane("XY").add(s.clean())


def gider_yollari():
    """v8b · {yan: dict(P, boru, kilif=[(bölme, dış katı, kılıf)])} — kılıf yalnız bölme içinde; bölme sacı ve PU kılıfın dışıyla kesilir"""
    out = {}
    for yan in EVAP:
        P = gider_noktalari(yan)
        boru = yol_kati(P, DR_R); dis = yol_kati(P, DR_KILIF)
        kl = []
        for ad_, i_ in {"sol": (("B2", 1), ("B3", 2)), "sag": (("B4", 3),)}[yan]:
            d_ = dis.intersect(kut(BOLME_X[i_], BOLME_X[i_] + BOLME, Y_TABAN - 20.0, Y_TABAN + 80.0, DR_Z - 30.0, DR_Z_DON + 30.0))
            kl.append((ad_, d_, d_.cut(boru)))
        out[yan] = dict(P=P, boru=boru, kilif=kl)
    return out


def k4_depo_cekmecesi(d0):
    """v8b · K4 kaşar + sucuk deposu = ELLE ÇEKİLEN ÇEKMECE (denetçi ORTA 1) · açıklık K4 tam genişlik · Accuride DZ3832-TR (bas-aç) · strok 628
    kutu U 1,5 + sökülür raf (tutuculara oturur) · GN 1/1 kutunun tabanında, GN 1/2 rafın üstünde (raf ve GN 1/2 kotları v8 ile aynı)"""
    B_, G_ = "B_DEPO", "CEKMECE"
    x0, x1, yo = K4X, K4_SAG, d0
    Z1 = Z_CON0 - 2.0; Z0 = Z1 - DEPO_KUTU_D                                # 22 … −523 (kutu fitil halkasının arkasında biter)
    ka, kb, kc, kd = x0 + RAY_T, x1 - RAY_T, yo + 3.0, DEPO_KUTU_UST
    u = kut(ka, kb, kc, kc + 1.5, Z0, Z1).union(kut(ka, ka + 1.5, kc, kd, Z0, Z1)).union(kut(kb - 1.5, kb, kc, kd, Z0, Z1))
    ekle("k4_depo_kutu_U_1.5", u, "sac", B_, grup=G_, bom=("K4 depo çekmece kutusu U 1,5", 1, "304 lazer + 2 büküm · yanları iç raya 4 × M4 · ön + arka 1,5",
                                                          "%.0f × %.0f × %.0f" % (kb - ka, kd - kc, DEPO_KUTU_D)))
    ekle("k4_depo_kutu_arka_1.5", kut(ka + 1.5, kb - 1.5, kc + 1.5, kd, Z0, Z0 + 1.5), "sac", B_, grup=G_)
    ekle("k4_depo_kutu_on_1.5", kut(ka + 1.5, kb - 1.5, kc + 1.5, kd, Z1 - 1.5, Z1), "sac", B_, grup=G_)
    for ad_, a_, b_, w0_ in (("sol", ka + 1.5, ka + 16.5, ka + 1.5), ("sag", kb - 16.5, kb - 1.5, kb - 3.5)):
        ub = (kut(w0_, w0_ + 2.0, yo + 12.0, kd - 4.0, Z1, Z_ON0).union(kut(a_, b_, yo + 12.0, kd - 4.0, Z1, Z1 + 2.0))
              .union(kut(a_, b_, yo + 12.0, kd - 4.0, Z_ON0 - 2.0, Z_ON0)))
        ekle("k4_depo_on_baglanti_" + ad_, ub, "celik", B_, grup=G_,
             bom=("Ön bağlantı köşesi · U 2 mm", 2, "304 2 mm büküm · kutu önüne punta, kapak iç sacına 2 × M5 perçin somun", "K4 depo çekmecesi") if ad_ == "sol" else None)
    for ad_, rx0, yon in (("sol", x0, 1.0), ("sag", x1, -1.0)):
        ry0 = yo + RAY_Y0
        def rk(w0, w1, y0_, y1_, z0_, z1_, _r=rx0, _s=yon, _y=ry0):
            return kut(_r + _s * w0, _r + _s * w1, _y + y0_, _y + y1_, z0_, z1_)
        za, zb = Z_CER0 - RAY_L, Z_CER0
        dis = rk(0.0, 1.2, 0.0, RAY_H, za, zb).union(rk(0.0, RAY_DIS_W, 0.0, 1.2, za, zb)).union(rk(0.0, RAY_DIS_W, RAY_H - 1.2, RAY_H, za, zb))
        ekle("k4_depo_ray_dis_" + ad_, dis, "celik", B_,
             bom=("Teleskopik ray Accuride DZ3832-TR (bas-aç) · 700", 2, "%100 açılır · touch release: kapalıyken itince açılır (kulpsuz) · 45,7 × 12,7",
                  "K4 depo · dış eleman bölme sacına 4 × M5 · accuride-europe.com DZ3832-TR [700 boy + yük katalogdan teyit]") if ad_ == "sol" else None)
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ara = rk(1.7, 2.7, 1.7, RAY_H - 1.7, za, zb).union(rk(1.7, RAY_ARA_W, 1.7, 2.7, za, zb)).union(rk(1.7, RAY_ARA_W, RAY_H - 2.7, RAY_H - 1.7, za, zb))
        ekle("k4_depo_ray_ara_" + ad_, ara, "celik", B_, grup="CEKMECE_ARA")
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ic = rk(RAY_T - 1.2, RAY_T, 5.0, RAY_H - 5.0, za, zb).union(rk(3.2, RAY_T, 5.0, 6.2, za, zb)).union(rk(3.2, RAY_T, RAY_H - 6.2, RAY_H - 5.0, za, zb))
        ekle("k4_depo_ray_ic_" + ad_, ic, "celik", B_, grup=G_)
    RZ0 = Z_CER0 - 285.0                                                      # −262: raf GN 1/2'nin (−252…+13) 10 arkasına kadar · arkası açık (GN 1/1'e hava)
    for ad_, a_ in (("sol", ka + 1.5), ("sag", kb - 11.5)):
        ekle("k4_depo_raf_tutucu_" + ad_, kut(a_, a_ + 10.0, d0 + 105.0, d0 + 115.0, RZ0, Z1 - 1.5), "celik", B_, grup=G_,
             bom=("Raf tutucu köşebent 10 × 10 × 1,5", 2, "304 · kutu yanına punta", "") if ad_ == "sol" else None)
    ekle("k4_depo_raf", kut(ka + 2.0, kb - 2.0, d0 + 115.0, d0 + 116.5, RZ0, Z1 - 2.0), "sac", B_, grup=G_,
         bom=("K4 depo rafı 1,5 · sökülür", 1, "304 · tutuculara oturur · GN 1/2'nin altında, arkası açık (GN 1/1'e hava)", "raf kotu v7 ile aynı 578,5–580"))
    gx0, gx1 = x0 + 37.5, x0 + K4W - 37.5
    ekle("k4_depo_GN11_100", kut(gx0, gx1, kc + 1.5, kc + 101.5, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(gx0 + 1.0, gx1 - 1.0, kc + 2.5, kc + 102.5, Z_CER0 - 539.0, Z_CER0 - 11.0)),
         "sac", B_, grup=G_, bom=("GN 1/1-100 kap + kapak", 1, "304 · EN 631 · 530 × 325 × 100", "kaşar blok 2 gün = 8,8 kg (yoğunluk VARSAYIM) · çekmece kutusunun tabanında"))
    g1 = d0 + 116.5
    ekle("k4_depo_GN12_100", kut(gx0, gx1, g1, g1 + 100.0, Z_CER0 - 275.0, Z_CER0 - 10.0).cut(kut(gx0 + 1.0, gx1 - 1.0, g1 + 1.0, g1 + 101.0, Z_CER0 - 274.0, Z_CER0 - 11.0)),
         "sac", B_, grup=G_, bom=("GN 1/2-100 kap + kapak", 1, "304 · EN 631 · 325 × 265 × 100", "küp sucuk 2 gün = 2,8 kg · sökülür rafın üstünde"))


def _kivrimlar():
    a0 = KLAPE_AC[0] + 5.0
    lev = [(a0 + p, a0 + q) for p, q in KLAPE_KIVRIM]
    return lev, [(lev[i][1] + 0.5, lev[i + 1][0] - 0.5) for i in range(len(lev) - 1)]


def klape_levha(ky, kz):
    """v8b · klape levhası + üst kenarında pimi saran kıvrımlar (denetçi KÜÇÜK 7: levha pime 1,66 mm uzaktı, yalnız panele yaslanıyordu)"""
    w = kut(KLAPE_AC[0] - 6.0, KLAPE_AC[1] + 6.0, KLAPE_AC[2] - 6.0, ky - 4.0, Z_ON - 3.0, Z_ON - 1.5)
    for a, b in _kivrimlar()[0]:
        w = w.union(kut(a, b, ky - 4.0, ky, Z_ON - 3.0, Z_ON - 1.5)).union(silx(ky, kz, 5.5, a, b).cut(silx(ky, kz, 4.0, a - 1.0, b + 1.0)))
    for a, b in _kivrimlar()[1]:                                         # yaprak kıvrımlarının önünde levha kenarı 2 geri (dönerken ≥ 1,7 boşluk)
        w = w.cut(kut(a - 0.5, b + 0.5, ky - 6.0, ky - 3.0, Z_ON - 4.0, Z_ON - 0.5))
    return w


def klape_yaprak(ky, kz):
    """v8b · menteşe yaprağı: levha kıvrımlarının arasında pimi saran kıvrımlar · levha kıvrımlarının önünde 7 mm oyuk"""
    a0, a1 = KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0
    w = kut(a0, a1, ky + 7.0, ky + 22.0, Z_ON - 3.0, Z_ON - 1.5)
    for a, b in _kivrimlar()[1]:
        w = w.union(kut(a, b, ky, ky + 7.0, Z_ON - 3.0, Z_ON - 1.5)).union(silx(ky, kz, 5.5, a, b).cut(silx(ky, kz, 4.0, a - 1.0, b + 1.0)))
    return w



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
    yol = cq.Workplane("XY", origin=(0, 0, Z_ON0)).polyline(P).close()
    pts = [(ay0 - g - u, zz) for u, zz in prof]
    return cq.Workplane("YZ", origin=((ax0 + ax1) / 2.0, 0, 0)).polyline(pts).close().sweep(yol, transition="right")


def kapak_on(ad, a_, b_, c_, d_, bir, acik, grup="SABIT", fitil=True, bom=None):
    """kulpsuz 40'lık ön: dış sac 1,5 (dört kenardan bükülü + arkada kanal kenarına kadar DÖNÜŞ) + PU + iç panel 1,0 (kanalın içi); fitil kanalı dönüş ile panel arası; fitil"""
    ds = kut(a_, b_, c_, d_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
    pu = kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0 + 1.0, Z_ON1 - 1.5)
    ic = kut(a_ + 1.5, b_ - 1.5, c_ + 1.5, d_ - 1.5, Z_ON0, Z_ON0 + 1.0)
    if fitil:
        kn = cevre_supur(acik[0], acik[1], acik[2], acik[3], KANAL)
        pu, ic = pu.cut(kn), ic.cut(kn)
        # v9 · kanalın DIŞINDAKİ halka = dış sacın ARKA DÖNÜŞÜ (1,5) · iç sac = yalnız kanalın İÇİNDEKİ panel (v8: 1,0 iç sac kanalla ikiye bölünüyordu)
        _pl = kut(a_ + 1.0, b_ - 1.0, c_ + 1.0, d_ - 1.0, Z_ON0, Z_ON0 + 1.5).cut(kn)
        _pp = sorted(_pl.solids().vals(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(_pp) == 2, "%s: kanal dış halkası %d parça" % (ad, len(_pp))
        _halka = cq.Workplane(obj=_pp[0])
        ds = ds.union(_halka)
        pu = pu.cut(_halka)
        _ip = sorted(ic.solids().vals(), key=lambda s_: s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(_ip) == 2, "%s: iç sac %d parça" % (ad, len(_ip))
        ic = cq.Workplane(obj=_ip[0])
        assert len(ds.solids().vals()) == 1, "%s: dış sac tek parça değil" % ad
    ekle(ad + "_dis_sac_1.5", ds, "sac", bir, grup=grup, bom=bom)
    ekle(ad + "_pu", pu, "pu", bir, grup=grup)
    ekle(ad + "_ic_sac_1.0", ic, "sac", bir, grup=grup)
    if fitil:
        ekle(ad + "_fitil", cevre_supur(acik[0], acik[1], acik[2], acik[3], FITIL), "conta", bir, grup=grup,
             bom=("Fitil · geçmeli manyetik profil 21 × 18,5", 1, "PVC + şerit mıknatıs · kapak iç sacının 6,4'lük kanalına geçer · aletsiz sökülür",
                  "çevre %.0f mm · köşeler gönye kaynaklı" % (2 * (acik[1] - acik[0] + acik[3] - acik[2] + 4 * FITIL_G))))


def cekmece(kol, kod, tip, x0, yo):
    wo = GEN(kol); h = HH_C[kod]; x1 = x0 + wo; y1 = yo + h; xc = x0 + wo / 2.0
    TUB_D = TUB[tip] + ON_UZAMA; Z_TUB1 = Z_CON0 - 2.0; Z_TUB0 = Z_TUB1 - TUB_D      # v8 seçenek (a): kutu öne 79 uzar, arkası (Z_TUB0) v7 ile aynı · v2: kutu fitil halkasinin ARKASINDA biter (21'lik fitil acikliga 6,5 tasar)
    G = "CEKMECE"
    # ---- ön + fitil (hareketli) ----
    pa, pb = KAPAK_X[kol]                                               # v5 · TAM KAPLAMA
    pc = ON_ALT if kod in ALT_KOD else yo - BIND
    pd = ON_UST if kod in UST_KOD else y1 + BIND
    kapak_on(kod + "_on", pa, pb, pc, pd, kod, (x0, x1, yo, y1), grup=G,
             bom=("Çekmece önü 40 · kulpsuz · tam kaplama", 1, "dış 304 1,5 bükme (4 kenar + arkada kanal kenarına dönüş) + PU 37,5 köpük + iç panel 304 1,0 · fitil dişi dönüş ile panel arasındaki 6,4 kanala geçer", "%.0f × %.0f" % (pb - pa, pd - pc)))
    # ---- kutu (hareketli) ----
    ka, kb, kc, kd = x0 + KUTU_KENAR, x1 - KUTU_KENAR, yo + KC, y1 - 10.0
    u = kut(ka, kb, kc, kc + 1.0, Z_TUB0, Z_TUB1).union(kut(ka, ka + 1.0, kc, kd, Z_TUB0, Z_TUB1)).union(kut(kb - 1.0, kb, kc, kd, Z_TUB0, Z_TUB1))
    ekle(kod + "_kutu_U_1.0", u, "sac", kod, grup=G, bom=("Çekmece kutusu U 1,0", 1, "304 lazer + 2 büküm", "%d × %d × %d" % (kb - ka, kd - kc, TUB_D)))
    ekle(kod + "_kutu_arka_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB0, Z_TUB0 + 1.0), "sac", kod, grup=G)
    ekle(kod + "_kutu_on_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB1 - 1.0, Z_TUB1), "sac", kod, grup=G)
    # on ↔ kutu kose baglantilari: fitil halkasinin ICINDEN gecer (halka ic kenari aciklikta 6,5)
    # v8: 2 mm U büküm (v7 katı blok) — flanşlarla kutu önüne ve kapak iç sacına
    for ad_, a_, b_, w0_ in (("sol", ka, ka + 15.0, ka), ("sag", kb - 15.0, kb, kb - 2.0)):
        ub = (kut(w0_, w0_ + 2.0, yo + 12.0, kd - 4.0, Z_TUB1, Z_ON0).union(kut(a_, b_, yo + 12.0, kd - 4.0, Z_TUB1, Z_TUB1 + 2.0))
              .union(kut(a_, b_, yo + 12.0, kd - 4.0, Z_ON0 - 2.0, Z_ON0)))
        ekle(kod + "_on_baglanti_" + ad_, ub, "celik", kod, grup=G,
             bom=("Ön bağlantı köşesi · U 2 mm", 2, "304 2 mm büküm · kutu önüne punta, kapak iç sacına 2 × M5 perçin somun", "ön yüz ayar yuvalı · %.0f derin" % (Z_ON0 - Z_TUB1)) if ad_ == "sol" else None)
    LZ0, LZ1 = max(Z_TUB0, Z_CER0 - RAY_L + 2 * RAY_KISA), min(Z_TUB1, Z_CER0 - 2 * RAY_KISA)   # v8: lam = kutu ∩ iç ray (660'lık kutu 739 > iç ray 692 → kutu arkada konsol)
    # ray adaptör lamları: kutu ile ray iç profili arasındaki 17,3'ü köprüler (kayışın ALTINDA kalır)
    for ad_, a_, b_ in (("sol", x0 + RAY_T, ka), ("sag", kb, x1 - RAY_T)):
        ekle(kod + "_ray_adaptor_" + ad_, kut(a_, b_, yo + RAY_Y0, yo + RAY_Y0 + 6.0, LZ0, LZ1), "celik", kod, grup=G,
             bom=("Ray adaptör lamı 6 mm", 2, "304 lama · kutuya punta", "ray iç profiline 4 × M4 · v8: iç ray boyuyla sınırlı (660'lık kutuda kutu arkada konsol)") if ad_ == "sol" else None)
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
    pul_a = (silx(ky, 0.0, KAS_OD / 2.0, fl0 + 1.5, fl1 - 1.5).union(silx(ky, 0.0, KAS_FL / 2.0, fl1 - 1.5, fl1))
             .cut(silx(ky, 0.0, AVARA_MIL_R, fl0 - 1, fl1 + 1)))                   # v8: avara TEK flanşlı (dış) — iç flanşın yeri 3 mm avara koluna · Ø5 mil
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
    ekle(kod + "_avara", pul_a.translate((0, 0, Z_AVARA)), "aluminyum", kod, bom=("GT3 avara 30 diş · 6 mm · tek flanşlı (dış) · çift rulman", 1, "alüminyum · 2 × MR126-2RS (6 × 12 × 4: 8 ≤ göbek 9,5 — v8'deki 2 × 625 = 10 sığmıyordu) · v8: iç flanş yok (Gates: iki kasnaklı tahrikte motor kasnağı çift flanşlı → kayış kılavuzu yeter)", "z −1 SABİT (v10 strok 700; v9 −73 / 628)"))
    ekle(kod + "_avara_mili", silx(ky, Z_AVARA, AVARA_MIL_R, x0 + RAY_T + KOL_BOS + KOL_T, fl1 + 1.0), "celik", kod,
         bom=("Avara mili Ø6 · omuzlu", 1, "304 · kola somunla (kolun iç yüzünde) · 2 × MR126-2RS taşır", "v8b: Ø5 → Ø6 (sıkışma tepesinde 182 → ~108 MPa)"))
    # v8b: avara kolu 2 mm sac (denetçi ORTA 3) · iç raya KOL_BOS 1,0, avaraya 1,3 · üst L flanş 12 · ön flanş 20 × 12,7 çerçeve sacının arkasına
    #      2 × PEM FH4-M3 gömme başlı saplama (çerçevenin önü düz, fitil bandı temiz — KÜÇÜK 10) · ARKA KULAK sensör lamının üstüne 20 biner (ORTA 4)
    kl0 = x0 + RAY_T + KOL_BOS
    lkx0, lky1 = x0 + SEN_X[0] - SEN[2] - 0.6, yo + SEN_Y0 + SEN[1] + 2.0           # sensör lamının iç kenarı · üst yüzü (lam aşağıda)
    kol = kut(kl0, kl0 + KOL_T, ky - 8.0, y1 + 12.0, Z_AVARA - 8.0, Z_CER0)
    kol = kol.union(kut(x0 + 1.0, kl0, y1 + 1.0, min(y1 + 1.0 + KOL_FLANS_Y, TAVAN_KOL[kod.split("_")[1]] - 1.0), Z_CER0 - KOL_T, Z_CER0))   # ön flanş (çerçeve sacının arkasına · tavanın 1 altı)
    kol = kol.union(kut(kl0, kl0 + KOL_FL, y1 + 12.0 - KOL_T, y1 + 12.0, Z_AVARA - 8.0, Z_CER0))                     # üst flanş → L kesit
    kol = kol.union(kut(kl0, kl0 + KOL_T, lky1, lky1 + 8.0, Z_AVARA - 8.0 - KOL_KULAK, Z_AVARA - 8.0))               # arka kulak (dik)
    kol = kol.union(kut(lkx0 + 2.0, kl0 + KOL_T, lky1, lky1 + KOL_T, Z_AVARA - 8.0 - KOL_KULAK, Z_AVARA - 8.0))      # kulak flanşı: lamın üstüne yatar
    ekle(kod + "_avara_kolu", kol, "celik", kod,
         bom=("Avara kolu 2 mm · L kesit + ön flanş + arka kulak", 1, "304 2 mm büküm · üst flanş 12 · ön flanş 20 × 12,7 (K1 / K2 üst çekmecede tavan nedeniyle 18,5): çerçeve sacına 2 × PEM FH4-M3-10 gömme başlı saplama + somun (çerçevenin önü düz, fitil bandı temiz) · arka kulak: sensör lamına 20 bindirme, 2 × M3 perçin",
              "boy 104 (−81…+23), moment kolu 96 · iç raya 1,0 · avaraya 1,3 · kayış gergisi burada: 8 mm yuvalı"))
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
    # v8: lam ÖNDE avara kolunun arka yüzüne değer (−81), ARKADA 2 mm L tırnakla arka iç saca oturur (v7: iki ucu da havadaydı);
    #     yatay kablo kanalına denk gelen lam (K2 üst) kanalın önünde kademeyle kanalın altına iner
    lx0, lx1 = x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6
    ly0, ly1 = my0 + SEN[1], my0 + SEN[1] + 2.0
    lz1, ZT_ = Z_AVARA - 8.0, Z_ARKA + 2.0
    kny = [ku for (xa_, xb_), ku in (((K1X + KAN_X[1], K4X + KAN_X[1]), KAN_UST), ((K4X + KAN_X[1], KOLON_X["K6"] + KAN_X[1]), KAN_UST_F))
           if xa_ < lx1 and lx0 < xb_ and ku[0] < ly1 + 1.0 and ly0 - 1.0 < ku[1]]
    if not kny:
        lam = kut(lx0, lx1, ly0, ly1, ZT_, lz1).union(kut(lx1 - LAM_TIRNAK, lx1, ly1 - 24.0, ly1, Z_ARKA, ZT_)).union(kut(lx0, lx0 + 2.0, ly1, ly1 + LAM_H, ZT_, lz1))
    else:
        yk, zk = kny[0][0] - 4.0, KAN_Z[1] + 2.0                        # kanalın 4 altı · kanalın 2 önü (−763)
        lam = (kut(lx0, lx1, ly0, ly1, zk, lz1).union(kut(lx0, lx1, yk, ly1, zk - 2.0, zk)).union(kut(lx0, lx1, yk, yk + 2.0, ZT_, zk - 2.0))
               .union(kut(lx1 - LAM_TIRNAK, lx1, yk - 22.0, yk + 2.0, Z_ARKA, ZT_)).union(kut(lx0, lx0 + 2.0, ly1, ly1 + LAM_H, zk, lz1)))
    ekle(kod + "_sensor_lami", lam, "celik", kod,
         bom=("Sensör lamı L 6,35 × 8 × 2 + arka tırnak", 1, "304 büküm · reed sensörler altında · önde avara kolunun arka kulağına 20 bindirme 2 × M3 perçin · arkada 16 geniş tırnakla arka iç saca 2 × M4 perçin somun",
              "kanala denk gelen lam kanalın altından kademeyle geçer" if kny else ""))
    # ---- içerik (hareketli) · v10: HEPSİ TEPSİDE (silikon 10, çukur 7) — robot parmakla alır ----
    if tip in TOP or tip in SIL:
        t = TOP[tip] if tip in TOP else SIL[tip]
        tz1 = Z_TUB1 - 5.0; tz0 = tz1 - t["td"]                          # tepsi kutunun önüne göre (kutu iç arkası −596)
        tw = min(265.0, (kb - ka) / 2.0 - 2.0)                           # v10: dar kolonda (K6 585) tepsi kutuya sığar
        tx0, tx1 = xc - tw, xc + tw
        ty0 = kc + 1.0
        X = [xc + (i - (t["nx"] - 1) / 2.0) * t["ax"] for i in range(t["nx"])]
        Zc = (tz0 + tz1) / 2.0
        Z = [Zc + (j - (t["nz"] - 1) / 2.0) * t["az"] for j in range(t["nz"])]
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(t["cr"]).extrude(-(CUKUR_H + 1.0)).translate((0, ty0 + TEPSI_T - CUKUR_H, 0))
        ekle(kod + "_tepsi", kut(tx0, tx1, ty0, ty0 + TEPSI_T, tz0, tz1).cut(cuk), "silikon", kod, grup=G,
             bom=("Tepsi · %d çukur Ø%.0f" % (len(X) * len(Z), 2 * t["cr"]), 1, "gıda silikonu 10 mm · çukur 7 · kalıp döküm", "%.0f × %.0f" % (tx1 - tx0, t["td"])))
        if tip in TOP:
            tk, ust, adk, mal = top_kati(tip), t["hc"] + t["R"], "top", "hamur"
        else:
            tk, ust, adk, mal = sily(0.0, 0.0, t["r"], 0.0, t["h"]), t["h"], t["ad"], ("hamur" if tip == "tatli" else "kutu_icecek")
        for i, a in enumerate(X):
            for j, b in enumerate(Z):
                ekle("%s_%s_%d_%d" % (kod, adk, i, j), tk.translate((a, yo + Y_OTUR, b)), mal, kod, grup=G)
        return len(X) * len(Z), yo + Y_OTUR + ust, y1
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
    ZP0, ZP1 = -DZ + 1.5, ZP1_ON                  # v8: PU derinliği arka dış sacın önü … ön dönüşün arkası (+37,5; v7 −41,5)
    GID = gider_yollari(); GID_L = []                                   # v8b: bölme sacı / PU yalnız KILIFIN dışıyla kesilir (boru kılıfın içinde kayar)
    for y_ in GID:
        for _a, d_, _k in GID[y_]["kilif"]:
            b_ = d_.val().BoundingBox(); GID_L.append(((b_.xmin, b_.xmax, b_.ymin, b_.ymax, b_.zmin, b_.zmax), d_))
    CER, SACK, PUK = [], [], []                    # taşıyıcı / sac / PU kutuları (x0, x1, y0, y1, z0, z1)
    kes_mi = lambda a, b: all(a[2 * i] < b[2 * i + 1] - 0.01 and b[2 * i] < a[2 * i + 1] - 0.01 for i in range(3))

    def sac(ad, k, bir=B, bom=None, ek=None):
        w = kut(*k)
        for c in CER:
            if kes_mi(k, c):
                w = w.cut(kut(*c))                  # taşıyıcı dikme / kiriş geçiş deliği
        for c_, s_ in GID_L:
            if kes_mi(k, c_):
                w = w.cut(s_)                       # v8: gider borusu sacdan geçer
        if ek is not None:
            w = w.cut(ek)
        SACK.append(k)
        ekle(ad, w, "sac", bir, bom=bom)

    def pu(ad, k, bom=None, ek=None):
        w = kut(*k)
        for c in CER + SACK + PUK:
            if kes_mi(k, c):
                w = w.cut(kut(*c))
        for c_, s_ in GID_L:
            if kes_mi(k, c_):
                w = w.cut(s_)                       # v8: gider borusu köpüğün İÇİNDE
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
    PZ = (Z_ON - 61.5, Z_ON - 60.0)                                      # v8: +17,5 … +19 — ön düzlemin 60 gerisinde, bütün hat boyunca tek çizgi (SPEC §1)
    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1]).union(kut(X_IC0 + 1.5, X_IC1 - 1.5, Y_PLINT - 1.5, Y_PLINT, PZ[0] - PLINT_FLANS, PZ[0]))   # v8b: üst flanş
    for a_, b_, c_, d_ in PLINT_IZGARA:                                  # v8: K4 Secop EMİŞİ (v7: kondenser atışıydı)
        pl_ = pl_.cut(kut(a_, b_, c_, d_, PZ[0] - 1.0, PZ[1] + 1.0))
    ekle("onyuz_plint", pl_, "sac", B, bom=("Plint 1,5 (ön)", 1, "304 fırçalı 1,5 · z +17,5…+19 (ön düzlemin 60 gerisi) · x 30–3970 · üst flanş 25: taban dış sacına M5 perçin somun @ 300 · K4 önünde emiş ızgarası %d yarık 120 × 10 (köprü 5 / 8) %.0f cm²"
                                             % (len(PLINT_IZGARA), sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in PLINT_IZGARA) / 100.0), "dolabın altında ayak + plint dışında parça yok"))
    for ad_, x_ in (("sol", X_IC0), ("sag", X_IC1 - 1.5)):              # v8: yan dönüşler — dolabın altı yandan da kapalı (v7 x 0–30 / 3970–4000 açıktı)
        ekle("onyuz_plint_donus_" + ad_, kut(x_, x_ + 1.5, 0.0, Y_PLINT, -DZ + 1.5, PZ[0]).union(kut(x_ + 1.5 if ad_ == "sol" else x_ - 20.0, x_ + 21.5 if ad_ == "sol" else x_, Y_PLINT - 1.5, Y_PLINT, -DZ + 1.5, PZ[0] - PLINT_FLANS)), "sac", B,
             bom=("Plint yan dönüşü 1,5", 2, "304 · x 30 ve 3970 · plintten arka dış sac hizasına · üst flanş 20: taban dış sacına M5 perçin somun", "%.0f boy" % (PZ[0] + DZ - 1.5)) if ad_ == "sol" else None)
    for i, (ax, az) in enumerate(AYAK_XZ):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", B,
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz AISI 304 · taban Ø40 · yükseklik 123",
                  "elesa-ganter.com LV.A-SST · 123'e uygun diş boyu + taşıma yükü katalogdan seçilecek · fırın altında dikmelerin altında") if i == 0 else None)

    # ---------------- KABUK SACLARI ----------------
    sac("kasa_yan_dis_sac_sol", (0.0, 1.5, Y_PLINT, H_B, -DZ, Z_ON0), bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · ön kenar kapak arkasında (z +39) · v8: iki yan simetrik (şerit dönüşü 40)", ""))
    sac("kasa_yan_dis_sac_sag", (W_B - 1.5, W_B, Y_PLINT, H_B, -DZ, Z_ON - SERIT_DONUS))                  # v8: +39
    sac("tavan_dis_sac", (1.5, W_B - 1.5, H_B - 1.5, H_B, -DZ, Z_ON0), bom=("Tavan dış sacı", 1, "304 1,5 · A, C ve fırın bunun üstüne oturur (fırın altında taşıyıcı çerçeve) · v8: ön kenar +39 (kaide ön profili ve fırın tam basar)", ""))
    EMIS = None                                                         # v8: K4 emiş delikleri (plenum + 2 şerit) · v7 VENT + gider delikleri kalktı
    for a_, b_, c_, d_ in EMIS_DELIK:
        _k = kut(a_, b_, Y_PLINT - 1.0, Y_PLINT + 3.0, c_, d_)
        EMIS = _k if EMIS is None else EMIS.union(_k)
    for a_, b_ in PANO_YARIK:                                           # v8b: pano bölmesi hava girişi (plint boşluğundan · denetçi KÜÇÜK 14)
        EMIS = EMIS.union(kut(a_, b_, Y_PLINT - 1.0, Y_PLINT + 3.0, PANO_YARIK_Z[0], PANO_YARIK_Z[1]))
    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, Z_ON0), ek=EMIS,
        bom=("Taban dış sacı 1,5", 1, "304 · v8: ön kenar +39 · K4 altında %d emiş penceresi %.0f cm² (aralarında ≥ 20 köprü · paslanmaz tel elek [VARSAYIM]) + pano girişi %d × 80 × 12"
             % (len(EMIS_DELIK), sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in EMIS_DELIK) / 100.0, len(PANO_YARIK)), "plint boşluğundan Secop'a ve panoya hava · Secop yükünü montaj rayları taşır, taban sacı taşımaz"))
    AY_ = None                                                          # v7: fırın altı hava boşluğunun arka yarıkları
    for a_, b_ in ARKA_YARIK:
        _k = kut(a_, b_, ARKA_YARIK_Y[0], ARKA_YARIK_Y[1], -DZ - 1.0, -DZ + 2.5)
        AY_ = _k if AY_ is None else AY_.union(_k)
    sac("arka_dis_sac", (1.5, W_B - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), ek=AY_)
    sac("yan_ic_sac_sol", (X_IC0S, X_IC0S + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0))      # v7: PU 60 (v6 29–30 · PU 27,5) · önde çerçeve sacına dayanır
    sac("kasa_yan_on_donus_sol", (1.5, 30.0, Y_PLINT + 1.5, H_B - 1.5, ZP1, Z_ON0))
    # iç tavan: K1–K4 728 · fırın altı (K5, K6) 668 — üstünde ısı kalkanı
    sac("tavan_ic_sac", (X_IC0S, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, ZP1))
    sac("tavan_ic_sac_F", (XF0, XB[5], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, ZP1))
    TD_A, TD_F = (X_IC0, XF0, Y_TAVAN, H_B - 1.5, ZP1, Z_ON0), (XF0, XS - 1.0, Y_TAVAN_F, H_B - 1.5, ZP1, Z_ON0)
    ekle("tavan_on_donus", kut(*TD_A).union(kut(*TD_F)), "sac", B); SACK.extend([TD_A, TD_F])
    sac("taban_ic_sac", (X_IC0S, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, ZP1))
    sac("taban_k4_kademe_saci", (K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, ZP1),
        bom=("Taban kademe sacı 1,0", 1, "304 · yalıtımlı tabanın K4 tarafındaki ucunu kapatır", "K4 sıcak bölmesi 40 mm alçak"))
    sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, ZP1))
    sac("taban_on_donus", (X_IC0, K4X, Y_PLINT + 1.5, Y_TABAN, ZP1, Z_ON0))                    # v8: K4 önünde YOK (tava öne çekilir, keşif B §6.5)
    sac("taban_on_donus_2", (K4_SAG, XS - 1.0, Y_PLINT + 1.5, Y_TABAN, ZP1, Z_ON0))
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
    _K3 = (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TABAN, Z_CER0, ZP1)     # v11: tabanda ön dönüşe kadar (sol K4 kademe sacının aynası) · tek parça
    assert PARCALAR[-1]["ad"] == "bolme_3_sac_a"; PARCALAR[-1]["wp"] = PARCALAR[-1]["wp"].union(kut(*_K3)); SACK.append(_K3)
    sac("bolme_3_sac_b", (XB[3] + BOLME - 1.0, XB[3] + BOLME, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    g5 = hava_gecis(4, GECIS(XB[4], KAN_UST_F))                                       # B5: K5 | K6 · 164,5–668
    sac("bolme_4_sac_a", (XB[4], XB[4] + 1.0, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    sac("bolme_4_sac_b", (XB[4] + BOLME - 1.0, XB[4] + BOLME, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    # B6: K6 | ŞERİT — soğuk zarfın sağ duvarı (3810'da yalıtımlı ara duvar); K6 fitili z −55'e kadar geldiği için PU önde −56'da biter
    sac("bolme_5_sac_a", (XB[5], XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA - 1.0, Z_CER0))
    sac("bolme_5_sac_b", (XS - 1.0, XS, Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_ON0),
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
    pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))
    pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))
    pu("arka_pu_37.5", (29.0, XF0 - 1.0, Y_PLINT + 1.5, Y_TAVAN + 1.0, ZP0, Z_ARKA - 1.0))
    pu("arka_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN_F + 1.0, ZP0, Z_ARKA - 1.0))
    for i, x0_ in enumerate(XB[:3]):
        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=hava_gecis(i, GECIS(x0_, KAN_UST)))
    pu("bolme_3_pu", (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    _P3 = (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TABAN, Z_CER0, ZP1)   # v11: ön cep PU ile dolu (ön dönüşün arkası)
    assert PARCALAR[-1]["ad"] == "bolme_3_pu"; PARCALAR[-1]["wp"] = PARCALAR[-1]["wp"].union(kut(*_P3)); PUK.append(_P3)
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
        for j_, xb_ in enumerate((300.0, 520.0)):                          # v8: tekne arka iç saca 2 L braketle oturur (v7 yalnız boruya bağlıydı → havada)
            br = kut(cx + xb_, cx + xb_ + 20.0, ey0 - 16.5, ey0 + 10.0, Z_ARKA, Z_ARKA + 1.5).union(kut(cx + xb_, cx + xb_ + 20.0, ey0 - 16.5, ey0 - 15.0, Z_ARKA + 1.5, EV_Z[0] + 30.0))
            ekle("damlama_teknesi_%s_braketi_%d" % (yan, j_ + 1), br, "celik", "B_SOGUTMA",
                 bom=("Damlama teknesi braketi 1,5 · L", 4, "304 büküm · arka iç saca 2 × M5 perçin somun · tekne üstüne oturur", "") if ilk and j_ == 0 else None)
        yc = (ey0 + ey1) / 2.0
        dv = kut(cx + 245.0, cx + 595.0, ey0, ey1, EV_Z[1], FAN_Z[0]).cut(kut(cx + 246.0, cx + 594.0, ey0 + 1.0, ey1 - 1.0, EV_Z[1] - 1.0, FAN_Z[0] - 1.0))
        for j_, fx in enumerate(FAN_X):
            dv = dv.cut(kut(cx + fx + 3.0, cx + fx + 116.0, yc - 56.5, yc + 56.5, FAN_Z[0] - 2.0, FAN_Z[0] + 1.0))
            ekle("fan_%s_%d" % (yan, j_ + 1), kut(cx + fx, cx + fx + 119.0, yc - 59.5, yc + 59.5, FAN_Z[0], FAN_Z[1]), "motor", "B_SOGUTMA",
                 bom=("Fan ebm-papst 4414 FL", 4, "24 V · 1,2 W · 94 m³/h · 26 dB(A) · 119 × 119 × 25",
                      "bölge başına 2 · davlumbazın önünde (v6: 7 × 4414 FNH 12 W = 84 W ısı → kalktı)") if ilk and j_ == 0 else None)
        ekle("fan_davlumbazi_%s" % yan, dv, "sac", "B_SOGUTMA",
             bom=("Fan davlumbazı 1,0", 2, "304 büküm · 2 fan deliği 113 × 113", "lamel yüzüne 26 mm (rapor ≥ 25)") if ilk else None)

        gb = GID[yan]["boru"]; P_ = GID[yan]["P"]
        ekle("gider_borusu_%s" % yan, gb, "plastik", "B_SOGUTMA",
             bom=("Gider borusu Ø12 × 1", 2, "PVC · v8b: tekne dibinden SÜREKLİ EĞİMLE (her koşu ≥ %1, sifon YOK — durgun su kalmaz): soğuk bölmenin arkasından (z −690) en alt kayışın altından, bölmeyi kılıfla geçer, K4 emiş şeridinde öne gelir, tavanın üstünde ördek gagası",
                  "bölme geçişleri Ø16 kılıf içinde (boru çekilip değiştirilir) · dolabın altına hiçbir boru sarkmaz") if ilk else None)
        for ad_, _d, k_ in GID[yan]["kilif"]:
            ekle("gider_kilifi_%s_%s" % (yan, ad_), k_, "plastik", "B_SOGUTMA",
                 bom=("Gider kılıfı Ø16 × 2 PVC", 3, "bölme PU'su içinde köpükle birlikte · içinden Ø12 boru kayar", "B2 · B3 · B4 geçişleri") if ilk and ad_ == "B2" else None)
        kel = []
        if yan == "sol":                                                  # K3 arkası: taban iç sacına oturan eyer (B2 ↔ B3 açıklığı 620)
            kel.append(kut(1677.0, 1687.0, Y_TABAN, yol_y(P_, 1682.0, DR_Z), DR_Z - 8.0, DR_Z + 8.0))
        xw_ = K4X if yan == "sol" else K4_SAG
        for zk_ in (-430.0, -250.0):                                      # K4 emiş şeridi: bölme sacına konsol kelepçe
            yk_ = yol_y(P_, DR_X_UC[yan], zk_)
            kel.append(kut(min(xw_, DR_X_UC[yan]), max(xw_, DR_X_UC[yan]), yk_ - 8.0, yk_ + 8.0, zk_ - 8.0, zk_ + 8.0))
        for j_, k_ in enumerate(kel):
            ekle("gider_kelepcesi_%s_%d" % (yan, j_), k_.cut(gb), "plastik", "B_SOGUTMA",
                 bom=("Boru kelepçesi Ø12 + konsol", 5, "PA kelepçe + 304 konsol · taban iç sacına / bölme sacına perçin", "K3 arkasında 1 eyer · K4 şeritlerinde 4 konsol") if ilk and j_ == 0 else None)
        ekle("gider_cek_valfi_%s" % yan, sily(DR_X_UC[yan], DR_Z_ON, VALF[0], TAVA[3] + 1.5, TAVA[3] + 1.5 + VALF[1]), "silikon", "B_SOGUTMA",
             bom=("Ördek gagası çek valf Minivalve DU 120.001", 2, "silikon · flanşlı · boru ucunda tutucu kapakla [ölçü VARSAYIM: zarf Ø14 × 10 — minivalve.com katalog föyünden teyit]",
                  "v8b: KURU KAPAN (buzdolabı gideri gibi): tava buharlaştırdıkça kurur, su kapanı güvenilmez → sıcak hava / koku geri gelmez") if ilk else None)
    ekle("buharlastirma_tavasi", kut(*TAVA).cut(kut(TAVA[0] + 1.5, TAVA[1] - 1.5, TAVA[2] + 1.5, TAVA[3] + 1.0, TAVA[4] + 1.5, TAVA[5] - 1.5)),
         "sac", "B_SOGUTMA", bom=("Buharlaştırma tavası 1,5", 1, "304 · v8: K4 sıcak bölmesinin önünde, tabanda — Secop atış havasının içinde · soğutma kapağı açılınca öne çekilir",
                                  "%.0f × %.0f × %.0f · brüt %.1f L (günde 4 defrost, VARSAYIM ≤ 1 L) · gider uçları çek valfle tava ağzının 1,5 üstünde"
                                  % (TAVA[1] - TAVA[0], TAVA[3] - TAVA[2], TAVA[5] - TAVA[4], (TAVA[1] - TAVA[0] - 3.0) * (TAVA[3] - TAVA[2] - 1.5) * (TAVA[5] - TAVA[4] - 3.0) / 1e6)))

    # ---------------- K4 (2027,5–2500): SICAK bölme (Secop önde, B panosu arkada) · ara PU · KAŞAR + SUCUK DEPOSU (soğuk) — v5 ile aynı ----------------
    kx0, kx1 = K4X, K4X + K4W
    # v8b · SECOP CU NLE8.8CN 180° DÖNÜK (keşif B §6.5 Öneri 1) — denetçi ORTA 2: taban 4 pedle 2 × L 40×40×3 MONTAJ RAYINA oturur (raylar uç plakasıyla
    #       B3 kademe / B4 bölme sacına; ön ray B4'te taşıyıcı dikme hizasında) · ayırma saclarına + ara saca 5 mm, EPDM sünger conta (rijit temas YOK) ·
    #       kondenser perdesi SACI kalktı (deliği kondenser yüzüne eşitti: ünite takılıp sökülemiyordu) · servis: panel + tava + ön ray sökülür, ünite öne çekilir
    CU = (350.0, 297.0, 450.0)                                                 # NLE8.8CN 297 yüksek (föy) · taban 350 × 450 VARSAYIM
    cx0, cy0 = SECOP_X[0], SECOP_Y0                                            # 2088,75 · 131,5
    cz0, cz1 = SECOP_Z                                                         # −554 … −104
    for ad_, (rz0, rz1, dk) in RAY_SEC.items():
        rd = (rz0, rz0 + SECOP_RAY_T) if dk < 0 else (rz1 - SECOP_RAY_T, rz1)
        ray_ = kut(K4X, K4_SAG, Y_PLINT + 1.5, Y_PLINT + 1.5 + SECOP_RAY_T, rz0, rz1).union(kut(K4X, K4_SAG, Y_PLINT + 1.5, Y_PLINT + 41.5, rd[0], rd[1]))
        ekle("sogutma_grubu_montaj_rayi_" + ad_, ray_, "celik", "B_SOGUTMA",
             bom=("Yoğuşturucu montaj rayı L 40×40×3", 2, "AISI 304 köşebent · %.1f boy · uçlarında 3 mm uç plakası: B3 kademe sacına / B4 bölme sacına 2 × M6 perçin somun (ön ray B4'te taşıyıcı dikme hizası; arka ray gömülü takviye sacına [VARSAYIM])" % (K4_SAG - K4X),
                  "ön ray SÖKÜLÜR (servis: ünite öne çekilir)") if ad_ == "arka" else None)
    i_ = 0
    for ad_ in ("arka", "on"):
        for tx_ in (cx0 + 25.0, cx0 + CU[0] - 25.0):
            ekle("sogutma_grubu_takozu_%d" % i_, kut(tx_ - 20.0, tx_ + 20.0, Y_PLINT + 1.5 + SECOP_RAY_T, cy0, PED_Z[ad_][0], PED_Z[ad_][1]), "koyu", "B_SOGUTMA",
                 bom=("Titreşim pedi 40 × 30 × 4 · NBR / neopren 60 ShA", 4, "Secop tabanı ↔ montaj rayı · M8 cıvata geçişli [VARSAYIM · üretici seçilmedi]",
                      "Secop montaj deliklerinin altında (yer föyden teyit)") if i_ == 0 else None)
            i_ += 1
    ekle("sogutma_grubu_taban", kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz0, cz1), "motor", "B_SOGUTMA",
         bom=("Yoğuşturucu ünite Secop CU NLE8.8CN R290", 1, "−10 °C'de 25 / 32 / 43 °C: 737 / 688 / 586 W (hızlı başvuru tablosu) · föy 314H5000 32 °C'de 661 W — ÇELİŞKİ AÇIK · gereken (v8, 32 °C, 18 sa, %%10 pay) boş %.0f · dolum %.0f · dolum + sıcak hamur %.0f W"
                                    % (SOG_V8["bos"], SOG_V8["dol"], SOG_V8["dol_s"]),
              "yükseklik 297 (föy) · taban 350 × 450 VARSAYIM · 17,9 kg · 180° dönük: kondenser arkada (arka plenumdan emer), atış önden K4 panelinin yarıklarından"))
    ekle("sogutma_grubu_taban_contasi", kut(cx0, cx0 + CU[0], Y_PLINT + 1.5, cy0, cz0 + 50.0, cz0 + 60.0), "conta", "B_SOGUTMA")   # taban altı conta (ünitenin tabanına yapışık, onunla çıkar)
    ekle("sogutma_grubu_kondenser", kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + 15.0, cy0 + CU[1], cz0, cz0 + 60.0), "bakir", "B_SOGUTMA")
    ekle("sogutma_grubu_fan", silz(cx0 + CU[0] / 2.0, cy0 + 15.0 + (CU[1] - 15.0) / 2.0, 127.0, cz0 + 60.0, cz0 + 88.0), "motor", "B_SOGUTMA")   # Ø254 · kondenser yüzüne bağlı
    ekle("sogutma_grubu_kompresor", sily(cx0 + CU[0] / 2.0, cz0 + 310.0, 85.0, cy0 + 15.0, cy0 + 15.0 + 162.0), "koyu", "B_SOGUTMA")
    s0 = S0_K4
    assert abs(s0 - (cy0 + CU[1]) - SECOP_BOS) < 0.01, "Secop ustu ara sac boslugu %.1f (5 olmali)" % (s0 - cy0 - CU[1])
    # v6: ara katman K4'ün tam genişliğinde (B3 → B4); v5'te kx1'de (2427,5) bitiyordu, yan duvara 42,5'lik sıcak hava yarığı kalıyordu
    ekle("k4_ara_sac_alt", kut(kx0, K4_SAG, s0, s0 + 1.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, K4_SAG, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0).cut(K4KAN), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, K4_SAG, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    PY_ = None
    for a_, b_ in PANO_YARIK:                                               # v8b: pano havasının çıkışı (üstte) → plenum (Secop fanı çeker)
        _k = kut(a_, b_, PANO_YARIK_Y[0], PANO_YARIK_Y[1], PERDE_Z - 1.0, PERDE_Z + 2.0)
        PY_ = _k if PY_ is None else PY_.union(_k)
    ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, PERDE_Z, PERDE_Z + 1.0).cut(PY_), "sac", "B_SOGUTMA",
         bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında · v8: z −655 = emiş plenumunun arka duvarı · v8b: üstte 4 × 80 × 12 havalandırma yarığı (pano → plenum)", "pano tabandan emer, perde üstünden plenuma verir"))
    # v8b · EMİŞ / ATIŞ AYRIMI: emiş şeridi yan sacları üniteden 5 mm uzakta (aradaki boşluk taban yanı boyunca sünger conta) · kondenser çevresi
    #       (sol / sağ / üst) kondenser ön yüzünün 10 gerisinde EPDM sünger conta · taban altı contası ünitede · şerit önleri kapalı (ön ray üstünde)
    gb_s, gb_g = GID["sol"]["boru"], GID["sag"]["boru"]
    RY_ON = kut(K4X, K4_SAG, Y_PLINT + 1.5, Y_PLINT + 1.5 + SECOP_RAY_T, RAY_SEC["on"][0], RAY_SEC["on"][1])
    zc0, zc1 = cz0 + 50.0, cz0 + 60.0                                          # conta düzlemi z −504…−494
    for ad_, xa_, xb_, ca_, cb_ in (("sol", cx0 - SECOP_BOS - 1.5, cx0 - SECOP_BOS, cx0 - SECOP_BOS, cx0),
                                   ("sag", cx0 + CU[0] + SECOP_BOS, cx0 + CU[0] + SECOP_BOS + 1.5, cx0 + CU[0], cx0 + CU[0] + SECOP_BOS)):
        ekle("k4_emis_yan_sac_" + ad_, kut(xa_, xb_, Y_PLINT + 1.5, s0, zc0, cz1).cut(RY_ON), "sac", "B_SOGUTMA",
             bom=("Emiş şeridi yan sacı 1,5", 2, "304 · ünitenin yanında 5 mm (sünger contayla) · conta düzleminden öne — emiş şeridini atış tarafından ayırır · ön ray üstünde oyuklu", "") if ad_ == "sol" else None)
        ekle("k4_emis_yan_conta_" + ad_, kut(ca_, cb_, Y_PLINT + 1.5, cy0 + 15.0, zc1, cz1).cut(RY_ON), "conta", "B_SOGUTMA",
             bom=("Sünger conta EPDM 5 × 22 yapışkanlı", 2, "ünite tabanı ↔ emiş yan sacı · 390 boy", "titreşim geçmez, hava kısa devre yapmaz") if ad_ == "sol" else None)
    kc_ = (kut(cx0 - SECOP_BOS, cx0 + 5.0, cy0 + 15.0, s0, zc0, zc1).union(kut(cx0 + CU[0] - 5.0, cx0 + CU[0] + SECOP_BOS, cy0 + 15.0, s0, zc0, zc1))
           .union(kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + CU[1], s0, zc0, zc1)))
    ekle("k4_kondenser_contasi", kc_, "conta", "B_SOGUTMA",
         bom=("Kondenser çevre contası EPDM sünger 10 × 5…10", 1, "kondenserin sol / sağ / üst çevresi (yan saclara ve ara sac altına yapışık) + taban altı şeridi (ünitenin tabanına yapışık)",
              "v8b: kondenser perdesi SACI kalktı (deliği kondenser yüzüne eşitti, sıfır boşluk)"))
    for ad_, xa_, xb_ in (("sol", kx0, cx0 - SECOP_BOS - 1.5), ("sag", cx0 + CU[0] + SECOP_BOS + 1.5, K4_SAG)):
        ekle("k4_emis_on_kapama_" + ad_, kut(xa_, xb_, Y_PLINT + 1.5, s0, cz1 - 1.5, cz1).cut(RY_ON).cut(gb_s).cut(gb_g), "sac", "B_SOGUTMA",
             bom=("Emiş şeridi ön kapaması 1,5", 2, "304 · şeridin önünü kapatır (önü atış bölgesi: tava + panel) · ön ray üstünde oyuklu · gider borusu lastik geçişli", "") if ad_ == "sol" else None)
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

    # v8b · K4 DEPO = ELLE ÇEKİLEN ÇEKMECE (denetçi ORTA 1: gizli menteşeli 40'lık kapak 3 mm derzde komşu çekmece önüne çarpıyordu) ·
    #       K4 SOĞUTMA = SÖKÜLÜR SERVİS PANELİ (lazer yarıklı, 4 gizli klips — düz çekilir) · ikisi de ön düzleme dik hareket eder, dönmez
    k4_depo_cekmecesi(d0)
    KAP = [("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False, (ON_ALT, s0 - 2.5)),
           ("k4_kapak_depo", s0 + 15.0, ON_UST, "B_DEPO", True, (d0, Y_TAVAN - 20.5))]
    a_, b_ = KAPAK_X["K4"]
    ds = kut(a_, b_, ON_ALT, s0 + 12.0, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, ON_ALT + 1.5, s0 + 12.0 - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
    for xa_, xb_, ya_, yb_ in K4_YARIK:
        ds = ds.cut(kut(xa_, xb_, ya_, yb_, Z_ON1 - 2.0, Z_ON1 + 1.0))
    ekle("k4_kapak_sogutma_dis_sac", ds, "sac", "B_SOGUTMA",
         bom=("Yoğuşturucu bölmesi servis paneli 1,5 · lazer yarıklı", 1, "304 fırçalı 1,5 tava 40 · %d lazer yarık 145 × 8 (köprü 5 / 8) net %.0f cm² · 4 gizli klipsle sökülür (düz çekilir, menteşe YOK)"
                                    % (len(K4_YARIK), sum((q - p) * (t - r) for p, q, r, t in K4_YARIK) / 100.0),
              "v8b: Secop ATIŞI yarıklardan çıkar · v8 ızgara lamaları (452,5 açıklık, 10 N'da 11 mm sehim) kalktı"))
    for i_, (xa_, xb_) in enumerate(((a_ + 1.5, K4X + 1.5), (K4_SAG - 2.0, b_ - 1.5))):
        for j_, yc_ in enumerate((200.0, 400.0)):
            ekle("k4_panel_klipsi_%d" % (2 * i_ + j_), kut(xa_, xb_, yc_ - 10.0, yc_ + 10.0, Z_CER1, Z_ON0 + 6.0), "celik", "B_SOGUTMA",
                 bom=("Gizli panel klipsi Fastmount paslanmaz · erkek + dişi", 8, "çerçeve sacına / yan saca perçin · panelin kenar dönüşüne vida · düz çekince çıkar [tip VARSAYIM: Fastmount Very Low Profile, fastmount.com]",
                      "K4 soğutma paneli 4 + şerit servis paneli 4") if i_ == 0 and j_ == 0 else None)
    kapak_on("k4_kapak_depo", a_, b_, s0 + 15.0, ON_UST, "B_DEPO", (K4X, K4_SAG, d0, Y_TAVAN - 20.5), grup="CEKMECE",
             bom=("K4 depo çekmecesi önü 40 · kulpsuz", 1, "dış 304 1,5 (arkada kanal kenarına dönüş) + PU 37,5 + iç panel 304 1,0 (fitil kanalı dönüş ile panel arası) · bas-aç (Accuride DZ3832-TR)", "%.0f × %.0f" % (b_ - a_, ON_UST - s0 - 15.0)))

    # ---------------- ŞERİT 3810–4000 · ROBOT ÇÖPÜ (soğuk DEĞİL) ----------------
    ka_, kb_, kc_, kd_, ke_, kf_ = KOVA
    t_ = KOVA_T
    kiz = kut(XS + 4.0, W_B - 4.0, Y_PLINT + 1.5, ON_ALT, ke_ - 25.0, kf_)
    kiz = kiz.union(kut(XS + 4.0, XS + 5.5, ON_ALT, ON_ALT + 15.0, ke_ - 25.0, kf_)).union(kut(W_B - 5.5, W_B - 4.0, ON_ALT, ON_ALT + 15.0, ke_ - 25.0, kf_))
    kiz = kiz.union(kut(XS + 4.0, W_B - 4.0, ON_ALT, ON_ALT + 15.0, ke_ - 26.5, ke_ - 25.0))
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
        w = kut(SK0, SK1, y0_, y1_, Z_ON - SERIT_DONUS, Z_ON).cut(kut(SK0 + 1.5, SK1 - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON - SERIT_DONUS - 1.0, Z_ON - 1.5))
        if delik:
            w = w.cut(kut(delik[0], delik[1], delik[2], delik[3], Z_ON - 2.0, Z_ON + 1.0))
        ekle(ad, w, "sac", C, bom=bom)
    serit_on("serit_on_kapak", SERIT_KAPI[0], SERIT_KAPI[1],
             bom=("Şerit servis paneli 1,5 · yalıtımsız · sökülür", 1, "304 büküm · 40 dönüş · 4 gizli klipsle düz çekilir (menteşe YOK — v8b · denetçi ORTA 1: menteşe 3 mm derzde K6 önüne çarpıyordu)",
                  "%.0f × %.0f · kova öne çekilerek boşaltılır" % (SK1 - SK0, SERIT_KAPI[1] - SERIT_KAPI[0])))
    serit_on("serit_on_klape_paneli", SERIT_PANEL[0], SERIT_PANEL[1], delik=KLAPE_AC,
             bom=("Şerit klape paneli 1,5", 1, "304 büküm · 40 dönüş · sabit · klape açıklığı %.0f × %.0f" % (KLAPE_AC[1] - KLAPE_AC[0], KLAPE_AC[3] - KLAPE_AC[2]),
                  "%.0f × %.0f" % (SK1 - SK0, SERIT_PANEL[1] - SERIT_PANEL[0])))
    for i_, (xa_, xb_) in enumerate(((SK0 + 1.5, XS - 1.0), (KOVA[1] + 1.0, W_B - 1.5))):     # v8b: servis paneli klipsleri (sol: çerçeve sacı · sağ: yan dış sac)
        for j_, yc_ in enumerate((210.0, 490.0)):
            ekle("serit_panel_klipsi_%d" % (2 * i_ + j_), kut(xa_, xb_, yc_ - 10.0, yc_ + 10.0, Z_CER1 if i_ == 0 else Z_ON0 - 19.0, Z_ON0 + 6.0), "celik", C)
    # v8b · DÜŞME OLUĞU (denetçi KÜÇÜK 8: servis paneli + klape paneli dönüşleri klapenin arkasında 40 mm raf yapıyordu) — 45° paslanmaz oluk:
    #       üst kenarı klape açıklığının 7 altında panele kaynaklı, alt yüzü panel dönüşünün arka-üst köşesinden (564,5 ; +39) geçer, alt kenarı z +20
    OLY, OLZ = KLAPE_AC[2] - 7.0, 20.0                                   # üst kenar y 603 · alt kenar z +20 (kova önü +37'nin 17 gerisi)
    c_lo = (SERIT_PANEL[0] + 1.5) - Z_ON0; c_up = c_lo + 1.5 * math.sqrt(2.0)   # alt yüz y − z = 525,5 · üst yüz 527,62 (45°)
    OX0, OX1 = KOVA[0] + 2.5, KOVA[1] - 2.5                              # 3825 … 3985 (klape 3840–3970 · kova içi)
    olk = cq.Workplane("YZ", origin=(OX0, 0, 0)).polyline([(OLY, OLY - c_lo), (OLY, OLY - c_up), (OLZ + c_up, OLZ), (OLZ + c_lo, OLZ)]).close().extrude(OX1 - OX0)
    yk_ = [(OLY, OLY - c_up), (OLY, OLY - c_up - 20.0 * math.sqrt(2.0)), (OLZ + c_up + 20.0 * math.sqrt(2.0), OLZ), (OLZ + c_up, OLZ)]
    for xk_ in (OX0, OX1 - 1.5):
        olk = olk.union(cq.Workplane("YZ", origin=(xk_, 0, 0)).polyline(yk_).close().extrude(1.5))
    ekle("serit_dusme_olugu", olk, "sac", C, bom=("Düşme oluğu 1,5 · 45°", 1, "304 · yan kenarları 20 · üst kenarı klape panelinin arkasına kaynaklı, alt yüzü panelin alt dönüşüne dayanır",
                                                "v8b: atılan parça klapenin arkasındaki 40'lık dönüş rafında kalmaz, kovaya kayar"))
    ky_, kz_ = KLAPE_EKSEN
    ekle("klape_levhasi", klape_levha(ky_, kz_), "sac", C, grup="KLAPE",
         bom=("Yaylı klape levhası 1,5", 1, "304 · içe açılır (robot eli iter) · yay kapatır · en çok %.0f° (mekanik stop)" % KLAPE_MAX,
              "%.0f × %.0f · panelin arkasında, açıklığı 6 bindirir" % (KLAPE_AC[1] - KLAPE_AC[0] + 12.0, ky_ - 4.0 - KLAPE_AC[2] + 6.0)))
    ekle("klape_mentesesi", silx(ky_, kz_, 4.0, KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0), "celik", C,
         bom=("Yaylı menteşe Ø8 · yay gövde içinde", 1, "paslanmaz · %.0f boy · kapanma momenti [VARSAYIM]" % (KLAPE_AC[1] - KLAPE_AC[0] - 10.0), "marka seçilmedi [VARSAYIM]"))
    ekle("klape_mentese_yapragi", klape_yaprak(ky_, kz_), "celik", C)   # v8b: yaprak kıvrımları pimi sarar (denetçi KÜÇÜK 7)

    # ---------------- ÖN ÇERÇEVE SACI 1,0: bütün açıklıklar kesik (fitil buna basar) · fırın altında üst kenar 668 ----------------
    cer = kut(*CER_A).union(kut(*CER_F))
    for kol, kod, tip, x0, yo in CEK:
        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH_C[kod], Z_CER0 - 1, Z_CER1 + 1))
    for _a, _y0, _y1, _b, _f, ac in KAP:
        xa_, xb_ = (K4X, K4_SAG) if _f else (K4X + 2.5, K4_SAG - 2.5)   # v8b: depo çekmecesi açıklığı K4 tam genişlik 2027,5–2500       # v8: soğutma açıklığı 2030–2497,5 × 126–431 (tava öne çekilir)
        cer = cer.cut(kut(xa_, xb_, ac[0], ac[1], Z_CER0 - 1, Z_CER1 + 1))
    ekle("onyuz_cerceve_saci_1.0", cer, "sac", B, bom=("Ön çerçeve sacı 1,0", 1, "430 FERRİTİK 1,0 (manyetik fitil 304'e tutmaz) · lazer kesim · %d açıklık · fırın altında üst kenar %.0f" % (len(CEK) + len(KAP), Y_TAVAN_F), "fitil buna basar"))
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
    print("CEKMECELI DOLAP v8 + denetci duzeltmeleri (on duzlem +79 · arka -830 · derinlik 909) · tek parca 0-%.0f x %.0f-%.0f · %d parca · %d cekmece · birimler: %s"
          % (W_B, Y_PLINT, H_B, len(PARCALAR), len(CEK), ", ".join(sorted({p["birim"] for p in PARCALAR if not p["birim"].startswith("CEK_")}))))
    BB = {p["ad"]: p["wp"].val().BoundingBox() for p in PARCALAR}
    assert len(BB) == len(PARCALAR), "parca adlari tekil degil"
    yb = lambda ad: BB[ad]
    # ---- ALT TABAN ÇİZGİSİ + DÜZ ÜST (katılardan ölçülür) ----
    alt = yb("taban_dis_sac").ymin
    ic_ust = yb("taban_ic_sac").ymax
    on_alt = min(BB[p["ad"]].ymin for p in PARCALAR if p["ad"].endswith("_on_dis_sac_1.5") and p["grup"] == "CEKMECE")
    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin; sr_alt = yb("serit_on_kapak").ymin
    govde_alt = min(BB[p["ad"]].ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "onyuz_plint")))
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
    # ---- v8 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1): her önün dış yüzü Z_ON1, arkası Z_ON0 · +79'u geçen parça YOK · arka −830 · plint 60 geride ----
    GR = {p["ad"]: p["grup"] for p in PARCALAR}
    onz = [p["ad"] for p in PARCALAR if (p["ad"].endswith(("_dis_sac_1.5", "_dis_sac")) and ("CEK_" in p["ad"] or p["ad"].startswith("k4_kapak"))) or p["ad"].startswith("serit_on_")]
    for a_ in onz:
        assert abs(BB[a_].zmax - Z_ON1) < 0.01 and abs(BB[a_].zmin - Z_ON0) < 0.01, "%s: on %.2f…%.2f (+39…+79 olmali)" % (a_, BB[a_].zmin, BB[a_].zmax)
    z79 = {a_ for a_, b_ in BB.items() if abs(b_.zmax - Z_ON1) < 0.01}
    izl = {a_ for a_ in BB if a_.startswith("k4_izgara_")}
    zmx = max(b_.zmax for b_ in BB.values()); zmn = min(b_.zmin for b_ in BB.values())
    sab = sorted(a_ for a_ in z79 if GR[a_] == "SABIT" and a_ not in izl)
    plb = yb("onyuz_plint")
    print("ON DUZLEM: %d on panelin dis yuzu z %+.1f, arkasi %+.1f · z %+.1f'daki parcalar = on paneller + %d izgara lamasi · en one parca %+.1f · arka dis yuz %+.1f · derinlik %.0f · plint on yuzu %+.1f (%.0f geride) · en ondeki SABIT onler: %s"
          % (len(onz), Z_ON1, Z_ON0, Z_ON1, len(izl), zmx, zmn, zmx - zmn, plb.zmax, Z_ON1 - plb.zmax, ", ".join(sab)))
    assert z79 == set(onz) | izl, "z +79'da on panel olmayan parca: %s" % sorted(z79 - set(onz) - izl)[:5]
    assert abs(zmx - Z_ON1) < 0.01 and abs(zmn - Z_ARKA_DIS) < 0.01 and abs(zmx - zmn - DERINLIK) < 0.01, "on duzlem / arka / derinlik tutmuyor"
    assert abs(plb.zmax - (Z_ON1 - 60.0)) < 0.01 and abs(plb.xmin - X_IC0) < 0.01 and abs(plb.xmax - X_IC1) < 0.01, "plint +19 / 30-3970 degil"
    xs = sorted(KAPAK_X.values())
    assert all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and xs[0][0] == 0.0 and xs[-1][1] == W_B, "kolon onleri arasi 3 degil / 0-4000 degil"
    # ---- YIĞIN + TAVAN: Σ(HH + 33) ≤ sınır (SPEC) · en üst çekmece parçası ≤ iç tavan − 2 · fitil ≤ iç tavan (katılardan) ----
    for kol in KOLON_AD:
        cs = [c for c in CEK if c[0] == kol]
        top_ = sum(HH_C[c[1]] + 2 * BIND + FUGA for c in cs) + (Y0_KOL[kol] - (YUZ0 + BIND))   # v10: başlangıç kotu farkı da yığına
        ps = [p for p in PARCALAR if p["birim"].startswith("CEK_%s_" % kol)]
        ust_p = max(BB[p["ad"]].ymax for p in ps if "_on_" not in p["ad"] and p["grup"] != "SABIT")
        ust_s = max(BB[p["ad"]].ymax for p in ps if p["grup"] == "SABIT")          # v8b: sabit parçalar (ray, avara kolu ön flanşı) tavana değmez
        fit = max(BB[p["ad"]].ymax for p in ps if p["ad"].endswith("_on_fitil"))
        tav = TAVAN_KOL[kol]
        dz = {}
        for c in cs:
            dz[c[2]] = dz.get(c[2], 0) + 1
        print("   YIGIN %s: %s · toplam %.0f / sinir %.0f (bos %.0f) · en ust hareketli parca %.1f · en ust sabit parca %.1f · fitil ustu %.1f · ic tavan %.0f"
              % (kol, " + ".join("%d %s" % (n_, t_) for t_, n_ in dz.items()), top_, YIGIN_SINIR[kol], YIGIN_SINIR[kol] - top_, ust_p, ust_s, fit, tav))
        assert top_ <= YIGIN_SINIR[kol] + 0.01, "%s yigini sinirda degil" % kol
        assert ust_p <= tav - 2.0 and ust_s <= tav - 0.5 and fit <= tav + 0.01, "%s tavana degiyor" % kol
    # ---- K4 depo: açıklık fitili tavanın altında · GN 1/2 çekilebilir ----
    dk = yb("k4_kapak_depo_fitil"); g12 = yb("k4_depo_GN12_100"); ac1 = Y_TAVAN - 20.5
    print("K4 DEPO: kapak %.1f-%.1f · aciklik %.1f-%.1f · fitil ustu %.1f / tavan %.0f · GN 1/2 ustu %.1f -> cekme payi %.1f · K4 ara katman %.1f-%.1f x %.1f-%.1f"
          % (yb("k4_kapak_depo_dis_sac_1.5").ymin, yb("k4_kapak_depo_dis_sac_1.5").ymax, yb("k4_ara_sac_ust").ymax, ac1, dk.ymax, Y_TAVAN, g12.ymax, ac1 - g12.ymax,
             yb("k4_ara_sac_alt").ymin, yb("k4_ara_sac_ust").ymax, yb("k4_ara_pu").xmin, yb("k4_ara_pu").xmax))
    assert dk.ymax <= Y_TAVAN + 0.01 and ac1 - g12.ymax >= 20.0 and abs(yb("k4_ara_pu").xmax - K4_SAG) < 0.05
    # ---- v8b · K4 DEPO ÇEKMECESİ (elle · bas-aç): ray bindirmesi, kutu ↔ iç ray bağı, açıkken GN 1/1 ön düzlemin dışında (katılardan) ----
    zr = {}
    for el in ("dis", "ara", "ic"):
        bb = BB["k4_depo_ray_%s_sol" % el]; k = {"dis": 0.0, "ara": RAY_ARA_ORAN, "ic": 1.0}[el] * STROK
        zr[el] = (bb.zmin + k, bb.zmax + k)
    b1 = min(zr["dis"][1], zr["ara"][1]) - max(zr["dis"][0], zr["ara"][0]); b2 = min(zr["ara"][1], zr["ic"][1]) - max(zr["ara"][0], zr["ic"][0])
    ku_ = yb("k4_depo_kutu_U_1.5"); bag = min(zr["ic"][1], ku_.zmax + STROK) - max(zr["ic"][0], ku_.zmin + STROK); gn_ = yb("k4_depo_GN11_100")
    print("K4 DEPO CEKMECESI (elle · Accuride DZ3832-TR bas-ac · grup CEKMECE): kutu %.1f × %.1f × %.0f · strok %.0f · bindirme dis-ara %.0f / ara-ic %.0f · kutu-ic ray bagi %.0f · acikken GN 1/1 arkasi z %+.0f (on duzlem %+.0f + 10)"
          % (ku_.xlen, ku_.ylen, ku_.zlen, STROK, b1, b2, bag, gn_.zmin + STROK, Z_ON1))
    assert b1 >= 250.0 and b2 >= 250.0 and bag >= ku_.zlen - 5.0 and gn_.zmin + STROK >= Z_ON1 + 10.0, "K4 depo cekmecesi"
    # ---- RAY: tam açıkta elemanlar birbirinin içinde kalıyor mu, kutu iç elemana boyunca bağlı mı? (katılardan) ----
    en = dict(b1=1e9, b2=1e9, bag=1e9); kons = 0.0
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
            ic_l = zr["ic"][1] - zr["ic"][0]
            assert bag >= min(ad_.zlen, ic_l) - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / min(lam %.0f, ic ray %.0f))" % (kod, yan, bag, ad_.zlen, ic_l)
            kons = max(kons, ad_.zmin - BB["%s_kutu_U_1.0" % kod].zmin)
            en = dict(b1=min(en["b1"], b1), b2=min(en["b2"], b2), bag=min(en["bag"], bag))
    print("RAY (3 elemanli teleskop, %d cekmece x 2 yan, tam acik strok %.0f): en az dis-ara bindirme %.0f mm · ara-ic %.0f mm · kutu-ic ray bagi %.0f mm · ara eleman +%.0f · en uzun kutu arka konsolu %.0f mm (660'lik kutu, lam ic ray boyunda)"
          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK, kons))
    assert abs(STROK - 700.0) < 0.01 and abs(Z_AVARA + 1.0) < 0.01, "v10: strok 700 / avara -1 degil: %.1f" % STROK
    assert STROK <= RAY_L + 0.01, "strok ray boyunu (%%100 acilir) gecti"
    # ---- İÇERİK + KAPASİTE (2 GÜN KURALI) ----
    for kod, tip, n, ust_, acik in ozet:
        assert acik - ust_ >= 2.0, "%s: icerik aciklik ustune %.1f mm kaliyor" % (kod, acik - ust_)
    tipler = sorted({t for _k, t, _n, _u, _a in ozet})
    pay = {t: min(a - u for _k, tt, _n, u, a in ozet if tt == t) for t in tipler}
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t in ("ic1", "ic1d")); tat = sum(n for _k, t, n, _u, _a in ozet if t == "tatli")
    print("ICERIK PAYI (acikliga): " + " · ".join("%s %.1f" % (t, pay[t]) for t in tipler) + " mm")
    print("KAPASITE (2 gun kurali): pide %d top (>= 160) · lahmacun %d top (>= 400) · icecek %d kutu TEPSIDE (>= 139) · tatli %d kap (>= 11) · beklenen v10 175 / 420 / 144 / 12"
          % (pide, lahm, ice, tat))
    assert pide >= 160 and lahm >= 400 and ice >= 139 and tat >= 11, "2 gun kurali saglanmiyor"
    assert (pide, lahm, ice, tat) == (175, 420, 144, 12) and len(CEK) == 21, "v10 kapasite: pide 175 · lahmacun 420 · icecek 144 · tatli 12 · 21 cekmece"
    for g_ in (("K1", "K2", "K3"), ("K5", "K6")):                                          # v10 · SİMETRİ: grupta ön çizgileri aynı
        cz = [sorted((c[4], HH_C[c[1]]) for c in CEK if c[0] == k_) for k_ in g_]
        assert all(c_ == cz[0] for c_ in cz), "v10: %s on cizgileri ayni degil" % (g_,)
    print("SIMETRI v10: K1-K3 %d cekmece x acik %.0f (on cizgileri ayni) · K5-K6 %d x %.0f (ayni)" % (len([c for c in CEK if c[0] == "K1"]), HH_KOL["K1"], len([c for c in CEK if c[0] == "K6"]), HH_KOL["K6"]))
    hiz = 127.0 / 60.0 * math.pi * KAS_PD
    print("TAHRIK: PD3665-24-51 127 d/dk × GT3 30 dis (cevre %.1f) = %.0f mm/s · strok %.0f -> %.1f sn · surekli kuvvet %.0f N (0,853 N·m / r %.2f)"
          % (math.pi * KAS_PD, hiz, STROK, STROK / hiz, 0.853 / (KAS_PD / 2000.0), KAS_PD / 2.0))
    # ---- v8 · AVARA KOLU (104 boy) + AVARA MİLİ + SENSÖR LAMI: dayanım / sehim (kayış ön gerginliği VARSAYIM) ----
    E_ = 193000.0; T0 = 30.0                                            # N · GT3 6 mm kol başına ön gerginlik [VARSAYIM]
    Fs, Ft = 0.853 / (KAS_PD / 2000.0), 5.3 / (KAS_PD / 2000.0)          # sürekli / kısa süreli tepe (sıkışma: sürücü akım sınırı keser)
    h_ = min(HH_C[c[1]] for c in CEK) + 12.0 - (KY - 8.0)                 # en kısa kol gövdesi (lahmacun) 50
    A1, A2 = KOL_T * h_, KOL_FL * KOL_T
    xg = (A1 * KOL_T / 2.0 + A2 * KOL_FL / 2.0) / (A1 + A2)             # kesit ağırlık merkezi (kolun iç yüzünden x)
    Iy = h_ * KOL_T ** 3 / 12.0 + A1 * (xg - KOL_T / 2.0) ** 2 + KOL_T * KOL_FL ** 3 / 12.0 + A2 * (KOL_FL / 2.0 - xg) ** 2
    ek_ = KX - (RAY_T + KOL_BOS + xg); Lk = Z_CER0 - Z_AVARA                 # kayış hattının kesite kaçıklığı · flanştan mil eksenine boy
    sap = lambda R: R * ek_ * Lk ** 2 / (2.0 * E_ * Iy)
    I0 = h_ * KOL_T ** 3 / 12.0
    sap0 = lambda R: R * (KX - RAY_T - KOL_BOS - KOL_T / 2.0) * Lk ** 2 / (2.0 * E_ * I0)
    Rs, Rt = 2.0 * T0 + Fs, 2.0 * T0 + Ft
    km = KX - RAY_T - KOL_BOS - KOL_T; Wm = math.pi * (2.0 * AVARA_MIL_R) ** 3 / 32.0      # mil konsolu (kol yüzünden kayış hattına) · Ø5 mil
    Ll = (Z_AVARA - 8.0) - (Z_ARKA + 2.0); tl = SEN[2]                   # lam açıklığı · lam genişliği 6,35
    Al1, Al2 = tl * 2.0, 2.0 * LAM_H; yl = (Al1 * 1.0 + Al2 * (2.0 + LAM_H / 2.0)) / (Al1 + Al2)
    Il = tl * 8.0 / 12.0 + Al1 * (yl - 1.0) ** 2 + 2.0 * LAM_H ** 3 / 12.0 + Al2 * (2.0 + LAM_H / 2.0 - yl) ** 2
    wl = 7.9e-6 * 9.81 * (Al1 + Al2); wl0 = 7.9e-6 * 9.81 * Al1
    av_bos = (KX - KAS_B / 2.0 + 1.5) - (RAY_T + KOL_BOS + KOL_T)       # kol dış yüzü ↔ avara göbeği
    av_gen = KAS_B - 1.5                                                # avara göbek + dış flanş genişliği 9,5
    print("AVARA KOLU v8b (L gövde %.0f × %.0f + flanş %.0f × %.0f · boy 104 (−81…+23), moment kolu %.0f): kayış çekişi kesite %.1f kaçık -> uç sapması sürekli %.3f / tepe %.3f mm (iç raya boşluk %.1f · avaraya %.1f · düz kol olsaydı %.2f / %.2f) · avara mili Ø%.0f eğilme sürekli %.0f / tepe %.0f MPa (304 akma 205) · avara %.1f / 2 × MR126 %.0f · sensör lamı L sehim %.2f mm (düz lam %.1f)"
          % (h_, KOL_T, KOL_FL, KOL_T, Lk, ek_, sap(Rs), sap(Rt), KOL_BOS, av_bos, sap0(Rs), sap0(Rt), 2 * AVARA_MIL_R, Rs * km / Wm, Rt * km / Wm, av_gen, 2 * 4.0,
             5.0 * wl * Ll ** 4 / (384.0 * E_ * Il), 5.0 * wl0 * Ll ** 4 / (384.0 * E_ * tl * 8.0 / 12.0)))
    assert sap(Rt) < KOL_BOS - 0.5 and av_bos >= 1.0 and KOL_BOS >= 1.0 and av_gen >= 8.0, "avara kolu / avara bosluklari"
    assert Rt * km / Wm <= 205.0 / 1.5, "avara mili tepe gerilmesi 205/1,5'u gecti"
    for tip, adk in [(t_, "_top_") for t_ in TOP] + [(t_, "_%s_" % SIL[t_]["ad"]) for t_ in SIL]:   # v10: kutu + tatlı da tepside
        ks_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == tip}
        kenar = min(BB[p["ad"]].zmin for p in PARCALAR if p["birim"] in ks_ and adk in p["ad"]) + STROK
        print("   %s: acilinca arka sira topun arka kenari z %+.1f (on duzlem %+.0f · esik %+.0f · katilardan)" % (tip, kenar, Z_ON1, Z_ON1 + 5.0))
        assert kenar >= Z_ON1 + 5.0, "%s: acik cekmecede arka sira on duzlemin icinde" % tip
    k5_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == "hamur" and k_.startswith("CEK_K5_")}
    arka = min((BB[p["ad"]].zmin + BB[p["ad"]].zmax) / 2.0 for p in PARCALAR if p["birim"] in k5_ and "_top_" in p["ad"]) + STROK
    print("   K5 (firin alti) pide: acilinca arka sira top merkezi z %+.1f · firin on yuzu = on duzlem z %+.0f (y >= %.0f) -> dikey yaklasimda tutucu yaricapi <= %.0f mm (robot tarafi ACIK)"
          % (arka, FIRIN_CIKINTI, H_B, arka - FIRIN_CIKINTI))
    # ---- ŞERİT · ROBOT ÇÖPÜ ----
    kb = yb("robot_cop_kovasi_15L")
    ic_l = (kb.xlen - 2 * KOVA_T) * (kb.ylen - 3.0) * (kb.zlen - 2 * KOVA_T) / 1e6
    print("SERIT %.0f-%.0f (soguk degil): kova %.0f × %.0f × %.0f (x · y · z) · x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f · ic hacim (duz duvar) %.1f L · nominal 15 L"
          % (SERIT[0], SERIT[1], kb.xlen, kb.ylen, kb.zlen, kb.xmin, kb.xmax, kb.ymin, kb.ymax, kb.zmin, kb.zmax, ic_l))
    assert abs(kb.xlen - 165.0) < 0.05 and abs(kb.ylen - 300.0) < 0.05 and abs(kb.zlen - 400.0) < 0.05, "kova olcusu 165 × 300 × 400 degil"
    assert abs(kb.ymin - 126.0) < 0.05 and abs(kb.zmin - KOVA[4]) < 0.05 and abs(kb.zmax - (Z_ON1 - SERIT_DONUS - 2.0)) < 0.05, "kova yeri SPEC degil (v8: onu servis kapaginin 2 arkasi)"
    ps_ = yb("robot_cop_poseti"); ol_ = yb("serit_dusme_olugu")
    AT = kut(KOVA[0], KOVA[1], ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5]).val()
    dolu = _kesisim(AT, PARCALAR, haric=("serit_dusme_olugu",))
    UST = kut(KLAPE_AC[0], KLAPE_AC[1], SERIT_PANEL[0] + 1.5, KLAPE_AC[2], KOVA[5], Z_ON1 - 1.5).val()      # v8b · denetçi KÜÇÜK 8: klape arkası z +37…+77,5
    dolu2 = _kesisim(UST, PARCALAR, haric=("serit_dusme_olugu", "klape_levhasi"))
    ol_ac = math.degrees(math.atan2(1.0, 1.0))
    print("   ATMA BOSLUGU (kova izdusumu, poset agzi %.1f -> klape acikligi ustu %.0f, z %.0f…%.0f): oluk disinda %d parca · klape arkasi (z %+.0f…%+.1f, y %.1f-%.0f) oluk + klape disinda %d parca · DUSME OLUGU %.0f° y %.1f-%.1f z %+.1f…%+.1f (ustu klapeye %.0f, alt kenari kova onunun %.0f gerisi) · ustunde tasiyici kiris %.1f-%.1f"
          % (ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5], len(dolu), KOVA[5], Z_ON1 - 1.5, SERIT_PANEL[0] + 1.5, KLAPE_AC[2], len(dolu2), ol_ac, ol_.ymin, ol_.ymax, ol_.zmin, ol_.zmax,
             KLAPE_AC[2] - ol_.ymax, KOVA[5] - ol_.zmin, TK_Y[0], TK_Y[1]))
    assert not dolu and not dolu2 and ol_ac >= 45.0 - 0.01 and ol_.zmin <= KOVA[5] - 10.0, "atma boslugu / klape arkasi: %s %s" % (dolu[:5], dolu2[:5])
    GIR = kut(KLAPE_AC[0], KLAPE_AC[1], KLAPE_AC[2], KLAPE_AC[3], KOVA[5], Z_ON1).val()
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
    CIK = kut(KOVA[0] - 0.5, KOVA[1] + 0.5, KOVA[2], ps_.ymax, KOVA[4] - 0.5, Z_ON1 + 450.0).val()
    dolu = _kesisim(CIK, PARCALAR, haric=("robot_cop_kovasi_15L", "robot_cop_poseti", "serit_on_kapak"))
    print("   KOVA BOSALTMA: servis kapagi (%.0f-%.0f) acik, kova + poset kizakta z %+.0f'ye (on duzlem + 450) cekilir -> yolunda %d parca" % (SERIT_KAPI[0], SERIT_KAPI[1], Z_ON1 + 450.0, len(dolu)))
    assert not dolu, "kova cikis yolunda parca var: %s" % dolu[:5]
    # ---- TAŞIYICI ÇERÇEVE (fırın altı) · yük hesabı [VARSAYIM yükler] ----
    for ad_, k_, _e in TASIYICI:
        b = BB[ad_]
        assert abs(b.xmin - k_[0]) < 0.05 and abs(b.ymax - k_[3]) < 0.05, ad_
    ky0 = min(BB[a].ymin for a, _k, e in TASIYICI if e == "x"); ky1 = max(BB[a].ymax for a, _k, e in TASIYICI if e == "x")
    assert abs(ky1 - (H_B - 1.5)) < 0.05, "kiris ustu dis tavan sacina dayanmiyor"
    assert all(-730.0 + FIRIN_CIKINTI < k_[4] and k_[5] < FIRIN_CIKINTI for a, k_, e in TASIYICI if e == "x"), "kiris firin tabaninin disinda"
    for a, k_, e in TASIYICI:
        if e == "y":
            xc_, zc_ = (k_[0] + k_[1]) / 2.0, (k_[4] + k_[5]) / 2.0
            # v11: ayak dikmenin x'inde, iki sırada (−110 / −760) → dikme o x'teki enine alt şase profilinin üstünde (Codex modüler v1: her ayak x'inde enine profil)
            assert any(abs(xc_ - ax) < 0.05 and abs(zc_ - az) < 0.05 for ax, az in AYAK_XZ) or (
                any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[0]) < 0.05 for ax, az in AYAK_XZ) and any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[1]) < 0.05 for ax, az in AYAK_XZ)
                and AYAK_Z[1] < zc_ < AYAK_Z[0]), "%s altinda ayak / enine profil yok" % a
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
    print("   v11 AYAKLAR: %d adet · hepsi z %s (firin alti dahil, soldaki gibi kenarda) · arka dikme z %.0f enine alt sase profilinin ustunde (ayaklar arasi %.0f)"
          % (len(AYAK_XZ), " / ".join("%.0f" % z_ for z_ in AYAK_Z), TD_Z[1], AYAK_Z[0] - AYAK_Z[1]))
    assert {round(z_, 1) for _x, z_ in AYAK_XZ} == {round(z_, 1) for z_ in AYAK_Z}, "v11: ayak sirasi kenarda degil"
    print("   dikme 30×30×2: en yuklu %.0f N · %.1f MPa · Euler Pcr %.0f kN (boy %.0f) · ayak basina %.0f N (Elesa LV.A-SST tasima yuku KATALOGDAN TEYIT)"
          % (R, R / A_d, Pcr / 1000.0, L_d, R))
    assert sig <= 205.0 / 1.5 and seh <= L_ / 500.0 and R <= Pcr / 3.0
    # ---- v11 · K4 | K5 bölmesinin önü: x 2500–2535 · y 124,5–164,5 · z +23…+37,5 cebi dolu mu (katılardan) ----
    _cep = kut(BOLME_X[3] + 0.2, BOLME_X[3] + BOLME - 0.2, Y_PLINT + 1.7, Y_TABAN - 0.2, Z_CER0 + 0.2, ZP1_ON - 0.2).val()
    _dol = sum(_cep.intersect(p["wp"].val()).Volume() for p in PARCALAR if p["ad"] in ("bolme_3_sac_a", "bolme_3_pu", "taban_pu_F"))   # taban PU'su 2534'ten başlar (cebin son 0,8 mm'si)
    print("K4|K5 BOLME ONU (v11): cep %.0f mm3 · dolu %.0f mm3 (sac + PU) -> %s" % (_cep.Volume(), _dol, "KAPALI" if _dol >= 0.99 * _cep.Volume() else "ACIK"))
    assert _dol >= 0.99 * _cep.Volume(), "v11: K4|K5 bolme onunde cep var"
    # ---- v7 · FIRIN ALTI ISI KALKANI: PU yok, hava boşluğu (katılardan) ----
    ay_ = yb("isi_kalkani_ayirma_saci"); isn = yb("isi_kalkani_isinim_saci"); ts_ = yb("tavan_dis_sac")
    BOS = kut(X_F[0] + 1.0, BOLME_X[5], Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, ZP1_ON).val()
    pu_ic = _kesisim(BOS, [p for p in PARCALAR if p["mal"] == "pu"])
    yar = sum((b_ - a_) * (ARKA_YARIK_Y[1] - ARKA_YARIK_Y[0]) for a_, b_ in ARKA_YARIK) / 100.0
    print("ISI KALKANI v8 (rapor secenek b): PU 60 YOK · ayirma saci y %.0f-%.0f (x %.0f-%.0f) · isinim saci y %.1f-%.1f (%d takoz) · isinim saci ustu hava %.1f mm (dis tavan saci %.1f) · arka %d yarik %.0f cm² · bosluktaki PU %d parca · firin altinda yalitim = K5/K6 tavan PU %.0f"
          % (ay_.ymin, ay_.ymax, ay_.xmin, ay_.xmax, isn.ymin, isn.ymax, len(TAKOZ_XZ), ts_.ymin - isn.ymax, ts_.ymin, len(ARKA_YARIK), yar, len(pu_ic), Y_TAVAN - Y_TAVAN_F - 1.0))
    assert not pu_ic, "firin alti hava boslugunda PU var: %s" % pu_ic[:3]
    assert abs(ay_.ymin - Y_TAVAN) < 0.05 and isn.ymin > ay_.ymax and ts_.ymin - isn.ymax >= 40.0
    # ---- v7 · SOĞUTMA BÖLGELERİ (katılardan) ----
    for yan, e in EVAP.items():
        L_ = yb("evaporator_%s_lamel" % yan); dv_ = yb("fan_davlumbazi_%s" % yan)
        fb = [yb("fan_%s_%d" % (yan, j_ + 1)) for j_ in range(len(FAN_X))]
        fy0, fy1, fz0, fz1 = min(b.ymin for b in fb), max(b.ymax for b in fb), min(b.zmin for b in fb), max(b.zmax for b in fb)
        ks = [c for c in CEK if c[0] == e["kol"] and c[4] < fy1 and c[4] + HH_C[c[1]] > fy0]
        ka_z = min(Z_CON0 - 2.0 - (TUB[c[2]] + ON_UZAMA) for c in ks)          # v8: = Z_TUB0 (kutu arkası v7 ile aynı)
        gb_ = yb("gider_borusu_%s" % yan); tk_ = yb("damlama_teknesi_%s" % yan)
        print("   SOGUTMA %s (%s arkasi): lamel %.0f × %.0f × %.0f (x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f) · plenum %.0f · fan–lamel %.0f (>= 25) · fan onu %.0f / kutu arkasi %.0f (pay %.0f) · tekne alti %.1f · gider x %.0f -> surekli egim >= %%1 -> K4 cikis x %.0f"
              % (yan, e["kol"], L_.xlen, L_.ylen, L_.zlen, L_.xmin, L_.xmax, L_.ymin, L_.ymax, L_.zmin, L_.zmax, L_.zmin - Z_ARKA, fz0 - L_.zmax, fz1, ka_z, ka_z - fz1,
                 tk_.ymin, e["gider"][0], DR_X_UC[yan]))
        assert fz0 - L_.zmax >= 25.0 and ka_z - fz1 >= 5.0 and abs(gb_.ymax - tk_.ymin) < 0.05
        vl_ = yb("gider_cek_valfi_%s" % yan)
        assert TAVA[0] + 1.5 < vl_.xmin and vl_.xmax < TAVA[1] - 1.5 and TAVA[4] + 1.5 < vl_.zmin and vl_.zmax < TAVA[5] - 1.5 and vl_.ymin > TAVA[3], "gider cikisi tavanin ustunde degil"
        P_ = gider_noktalari(yan)
        eg = [(a_[1] - b_[1]) / math.hypot(b_[0] - a_[0], b_[2] - a_[2]) for a_, b_ in zip(P_, P_[1:]) if math.hypot(b_[0] - a_[0], b_[2] - a_[2]) > 1e-6]
        kl_ = sorted(a_ for a_ in BB if a_.startswith("gider_kilifi_%s_" % yan))
        print("      gider %s (denetci ORTA 5): %d dirsek · yatay kosularda egim en az %%%.2f · tekne alti %.1f -> cikis %.1f · en alcak nokta = cikis (sifon YOK, durgun su YOK) · kilif %s · en alt kayis (y %.1f) ile en az %.1f"
              % (yan, len(P_) - 2, 100.0 * min(eg), P_[0][1], P_[-1][1], ", ".join(kl_), YUZ0 + BIND + KY - KAS_OD / 2.0 - KAYIS_T,
                 min(YUZ0 + BIND + KY - KAS_OD / 2.0 - KAYIS_T - (yol_y(P_, xk_, DR_Z) + DR_R) for xk_ in [x_ + KX + s_ * KAYIS_W / 2.0 for x_ in (KOLON_X["K3"], KOLON_X["K5"]) for s_ in (-1.0, 1.0)]
                     if min(P_[1][0], P_[2][0]) <= xk_ <= max(P_[1][0], P_[2][0]))))
        assert min(eg) >= DR_EGIM - 1e-9 and all(b_[1] < a_[1] for a_, b_ in zip(P_, P_[1:])) and len(kl_) >= 1, "gider borusu surekli inmiyor / kilifsiz"
    for i_, gl in HAVA_GECIS.items():
        for y0_, y1_ in gl:
            dol = _kesisim(kut(BOLME_X[i_] - 0.5, BOLME_X[i_] + BOLME + 0.5, y0_ + 1.0, y1_ - 1.0, HAVA_Z[0] + 1.0, HAVA_Z[1] - 1.0).val(), PARCALAR)
            assert not dol, "B%d hava gecisi (%.0f-%.0f) kapali: %s" % (i_ + 1, y0_, y1_, dol[:3])
    print("   HAVA GECISLERI (arka, z %.0f…%.0f, acik oldugu katidan olculdu): %s · B3 (K3 | K4 sicak) kapali"
          % (HAVA_Z[0], HAVA_Z[1], " · ".join("B%d %s" % (i_ + 1, " + ".join("%.0f-%.0f" % g for g in gl)) for i_, gl in sorted(HAVA_GECIS.items()))))
    # ---- v8 · K4 SICAK BÖLME (keşif B §6.5 Öneri 1): emiş / atış yolu, tava, dolabın altı (katılardan) ----
    cu_ = yb("sogutma_grubu_kondenser"); ta_ = yb("sogutma_grubu_taban"); fn_ = yb("sogutma_grubu_fan"); tv_ = yb("buharlastirma_tavasi"); pr_ = yb("k4_ara_perde")
    s0_ = yb("k4_ara_sac_alt").ymin
    emis = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in EMIS_DELIK) / 100.0
    pli = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in PLINT_IZGARA) / 100.0
    atis = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in K4_YARIK) / 100.0    # v8b: panel lazer yarıkları (net)
    Vh = 551.0 / 3600.0                                                  # m³/s · Secop föyü kondenser havası (keşif B)
    print("   SECOP CU NLE8.8CN (180 derece · keşif B Oneri 1): taban x %.2f-%.2f y %.1f (4 ped) · kondenser z %.0f…%.0f (arkada) · fan Ø%.0f z %.0f…%.0f · plenum %.0f (perde z %.0f) · ust aralik %.1f (EPDM sunger contayla kapali)"
          % (ta_.xmin, ta_.xmax, ta_.ymin, cu_.zmin, cu_.zmax, fn_.xlen, fn_.zmin, fn_.zmax, cu_.zmin - pr_.zmax, pr_.zmin, s0_ - cu_.ymax))
    print("   HAVA YOLU (551 m3/h): plint emis izgarasi %.0f cm2 (%.1f m/s) -> taban emis pencereleri %.0f cm2 (%.1f m/s) -> plenum + 2 serit -> kondenser -> atis: K4 paneli lazer yariklari net %.0f cm2 (%.1f m/s)"
          % (pli, Vh / (pli / 1e4), emis, Vh / (emis / 1e4), atis, Vh / (atis / 1e4)))
    kop = min([EMIS_DELIK[i + 1][0] - EMIS_DELIK[i][1] for i in (0, 1)] + [EMIS_DELIK[i + 1][2] - EMIS_DELIK[i][3] for i in (3, 4, 6, 7)])
    print("   EMIS PENCERELERI: %d pencere · aralarinda en az %.0f mm kopru (>= 20) · Secop yukunu montaj raylari tasir · plint yarik koprusu %.0f / %.0f · K4 panel yarik koprusu %.0f / %.0f"
          % (len(EMIS_DELIK), kop, PLINT_IZGARA[1][2] - PLINT_IZGARA[0][3], PLINT_IZGARA[6][0] - PLINT_IZGARA[0][1], K4_YARIK[1][2] - K4_YARIK[0][3], K4_YARIK[20][0] - K4_YARIK[0][1]))
    assert cu_.zmin - pr_.zmax >= 95.0 and abs(fn_.zmin - cu_.zmax) < 0.01 and emis >= 1.25 * pli and pli >= 450.0 and atis >= 600.0 and kop >= 20.0 - 0.01
    # ---- v8b · SECOP MONTAJI (denetçi ORTA 2): ünite yalnız pedlere ve süngerlere değer · ayırma saclarına ≥ 5 · montaj rayı hesabı · servis yolu ----
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    VV = {p["ad"]: p["wp"].val() for p in PARCALAR}
    UNITE = ("sogutma_grubu_taban", "sogutma_grubu_kondenser", "sogutma_grubu_fan", "sogutma_grubu_kompresor")
    YUMUSAK = ("sogutma_grubu_takozu_", "sogutma_grubu_taban_contasi", "k4_kondenser_contasi", "k4_emis_yan_conta_") + UNITE
    tem = set()
    for u_ in UNITE:
        bu = BB[u_]
        for a_, b_ in BB.items():
            if a_.startswith(YUMUSAK) or bu.xmin > b_.xmax + 0.1 or b_.xmin > bu.xmax + 0.1 or bu.ymin > b_.ymax + 0.1 or b_.ymin > bu.ymax + 0.1 or bu.zmin > b_.zmax + 0.1 or b_.zmin > bu.zmax + 0.1:
                continue
            if _DSS(VV[u_].wrapped, VV[a_].wrapped).Value() <= 0.05:
                tem.add((u_, a_))
    ara_ = {(u_, a_): _DSS(VV[u_].wrapped, VV[a_].wrapped).Value() for u_, a_ in (("sogutma_grubu_taban", "k4_emis_yan_sac_sol"), ("sogutma_grubu_taban", "k4_emis_yan_sac_sag"),
                                                                                 ("sogutma_grubu_kondenser", "k4_ara_sac_alt"), ("sogutma_grubu_taban", "taban_dis_sac"))}
    m_cu = 17.9; P_ped = m_cu * 9.81 / 4.0 * 2.0                          # N · ped başına · dinamik ×2 [VARSAYIM]
    a_r = SECOP_X[0] + 25.0 - K4X; L_r = K4_SAG - K4X
    Ay1, Ay2 = 40.0 * SECOP_RAY_T, SECOP_RAY_T * (40.0 - SECOP_RAY_T); yc_ = (Ay1 * SECOP_RAY_T / 2.0 + Ay2 * (SECOP_RAY_T + (40.0 - SECOP_RAY_T) / 2.0)) / (Ay1 + Ay2)
    I_r = 40.0 * SECOP_RAY_T ** 3 / 12.0 + Ay1 * (yc_ - SECOP_RAY_T / 2.0) ** 2 + SECOP_RAY_T * (40.0 - SECOP_RAY_T) ** 3 / 12.0 + Ay2 * (SECOP_RAY_T + (40.0 - SECOP_RAY_T) / 2.0 - yc_) ** 2
    sig_r = P_ped * a_r / (I_r / (40.0 - yc_)); del_r = P_ped * a_r * (3 * L_r ** 2 - 4 * a_r ** 2) / (24.0 * 193000.0 * I_r)
    print("   SECOP MONTAJI: 4 ped 40×30×4 -> 2 × L 40×40×3 ray (%.1f aciklik, uclari B3 / B4) · ped basina %.0f N (dinamik ×2) · ray gerilme %.1f MPa · sehim %.3f mm · rijit temas (ped / sunger disi) %d · bosluklar: taban-yan sac %.1f / %.1f · kondenser-ara sac %.1f · taban-taban saci %.1f"
          % (L_r, P_ped, sig_r, del_r, len(tem), ara_[("sogutma_grubu_taban", "k4_emis_yan_sac_sol")], ara_[("sogutma_grubu_taban", "k4_emis_yan_sac_sag")],
             ara_[("sogutma_grubu_kondenser", "k4_ara_sac_alt")], ara_[("sogutma_grubu_taban", "taban_dis_sac")]))
    assert not tem, "Secop rijit temas: %s" % sorted(tem)[:6]
    assert min(ara_.values()) >= SECOP_BOS - 0.01 and sig_r <= 205.0 / 3.0 and del_r <= L_r / 1000.0
    SERVIS_SOKULEN = {"sogutma_grubu_montaj_rayi_on", "buharlastirma_tavasi", "k4_kapak_sogutma_dis_sac"} | {a_ for a_ in BB if a_.startswith("k4_panel_klipsi_")}
    UN_ = set(UNITE) | {"sogutma_grubu_taban_contasi"} | {a_ for a_ in BB if a_.startswith("sogutma_grubu_takozu_")}
    sab_ = [p for p in PARCALAR if p["grup"] == "SABIT" and p["ad"] not in UN_ and p["ad"] not in SERVIS_SOKULEN]
    bul_s = []
    for d_ in (100.0, 250.0, 400.0, 550.0, 700.0):
        for p in PARCALAR:
            if p["ad"] in UN_:
                bul_s += [(d_, p["ad"], b) for _v, b in _kesisim(VV[p["ad"]].translate(cq.Vector(0.0, 0.0, d_)), sab_)]
    print("   SECOP SERVIS YOLU: panel + klipsler + tava + on ray sokulur, unite pedleriyle one %.0f'e cekilir (5 konum) -> %d cakisma" % (700.0, len(bul_s)))
    assert not bul_s, "Secop servis yolunda: %s" % bul_s[:5]
    for ad_, kl_ in (("k4_kapak_sogutma_dis_sac", "k4_panel_klipsi_"), ("serit_on_kapak", "serit_panel_klipsi_")):
        sab_ = [p for p in PARCALAR if p["grup"] == "SABIT" and p["ad"] != ad_ and not p["ad"].startswith(kl_)]
        bul_p = [(d_, b) for d_ in (15.0, 40.0, 80.0) for _v, b in _kesisim(VV[ad_].translate(cq.Vector(0.0, 0.0, d_)), sab_)]
        print("   SOKULUR PANEL %s: 4 gizli klips · duz one 15 / 40 / 80 cekilir -> %d cakisma (menteşe yok, donmez)" % (ad_, len(bul_p)))
        assert not bul_p, "%s sokme yolunda: %s" % (ad_, bul_p[:5])
    # ---- v8b · PANO BÖLMESİ ISI (denetçi KÜÇÜK 14): tabandan emer, perde üstünden plenuma verir — Secop fanının emişi çeker [kayıplar VARSAYIM] ----
    PANO_W = {"S7-1200 1214C": 12.0, "3 × SM1221": 4.5, "SM1222": 1.5, "NDR-240 kaybı (~%93, ~60 W çıkış)": 4.5, "EM-324C boşta": 1.0, "röle (1 aktif)": 0.5}
    Pp = sum(PANO_W.values()); A_py = len(PANO_YARIK) * 80.0 * 12.0 * 1e-6
    dp_ = 0.5 * 1.2 * (Vh / (0.6 * emis / 1e4)) ** 2                      # Pa · taban emiş pencerelerindeki düşüm = plint boşluğu ↔ plenum farkı
    Qp = 0.6 * A_py * math.sqrt(dp_ / 1.2); dTp = Pp / (1.2 * 1005.0 * Qp)
    print("   PANO BOLMESI: %.0f W (VARSAYIM) · giris taban %d × 80 × 12 + cikis perde %d × 80 × 12 = %.0f cm² × 2 · surucu fark %.1f Pa -> %.1f m3/h · pano havasi ortamin %.1f K ustu (S7-1200 yatay 55 °C: 43 °C ortamda %.0f °C)"
          % (Pp, len(PANO_YARIK), len(PANO_YARIK), A_py * 1e4, dp_, Qp * 3600.0, dTp, 43.0 + dTp))
    assert dTp <= 10.0, "pano havalandirmasi yetersiz"
    YOL = kut(TAVA[0], TAVA[1], TAVA[2] + 0.5, TAVA[3] + 1.0, TAVA[4], Z_ON1 + (TAVA[5] - TAVA[4]) + 10.0).val()
    dolu = _kesisim(YOL, PARCALAR, haric={"buharlastirma_tavasi", "k4_kapak_sogutma_dis_sac"} | {a_ for a_ in BB if a_.startswith("k4_izgara_")})
    print("   TAVA %.0f × %.1f × %.0f (x %.0f-%.0f · y %.1f-%.1f · z %.0f…%.0f): servis paneli sokulu, tava one %+.0f'ye cekilir -> yolunda %d parca · cek valf alti %.1f / tava agzi %.1f"
          % (tv_.xlen, tv_.ylen, tv_.zlen, tv_.xmin, tv_.xmax, tv_.ymin, tv_.ymax, tv_.zmin, tv_.zmax, Z_ON1 + tv_.zlen + 10.0, len(dolu),
             min(yb("gider_cek_valfi_%s" % y_).ymin for y_ in EVAP), tv_.ymax))
    assert not dolu, "tava cekme yolunda parca var: %s" % dolu[:5]
    alt_ = [p["ad"] for p in PARCALAR if BB[p["ad"]].ymin < Y_PLINT - 0.01 and not p["ad"].startswith(("ayak_", "onyuz_plint"))]
    print("   DOLABIN ALTI (y < %.0f): ayak %d + plint %d disinda %d parca (v7: atis kanali + tava + gider borulari)"
          % (Y_PLINT, len([a_ for a_ in BB if a_.startswith("ayak_")]), len([a_ for a_ in BB if a_.startswith("onyuz_plint")]), len(alt_)))
    assert not alt_, "dolabin altinda parca: %s" % alt_[:5]
    # ---- SOĞUTMA (bilgi · VARSAYIM) · iletimle ısı kazancı kaba tahmini ----
    k_pu, T_ic, T_ort, T_fir, T_sic = 0.024, 3.0, 25.0, 60.0, 35.0     # W/m·K PU [VARSAYIM] · +3 °C · ortam · fırın tabanı · Secop bölmesi [VARSAYIM]
    Lz = (ZP1_ON - Z_ARKA) / 1000.0                                   # v8: iç derinlik +79 uzadı
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
    print("SOGUTMA v8: %d bolge · lamelli evaporator on yuzu %.3f m² · %d fan ebm-papst 4414 FL (%.1f W) · Secop CU NLE8.8CN 32 °C: tablo %.0f / foy %.0f W @ −10 °C (CELISKI ACIK) · gereken (sogutma_hesabi_v1 v8 geometrisiyle, 18 sa · %%10 pay) bos gun %.0f · dolum %.0f · dolum + sicak hamur %.0f W -> pay %.0f…%.0f / %.0f…%.0f W · duvar iletimi (bu kaba model) ~%.0f W"
          % (len(lam), ev, len(fan), 1.2 * len(fan), SOG_V8["secop_tablo"], SOG_V8["secop_foy"], SOG_V8["bos"], SOG_V8["dol"], SOG_V8["dol_s"],
             SOG_V8["secop_foy"] - SOG_V8["dol"], SOG_V8["secop_tablo"] - SOG_V8["dol"], SOG_V8["secop_foy"] - SOG_V8["dol_s"], SOG_V8["secop_tablo"] - SOG_V8["dol_s"], Q))
    assert len(lam) == 2 and len(fan) == 4 and not [p for p in PARCALAR if p["ad"].startswith(("fan_K", "evaporator_K"))]
    di = 14 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1221")]); dq = 10 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1222")])
    reed = len([p for p in PARCALAR if p["ad"].endswith(("_reed_kapali", "_reed_acik"))]); role = len([p for p in PARCALAR if p["ad"].startswith("role_")])
    print("PLC G/C: reed %d / DI %d · role %d + surucu 2 (yon + etkin VARSAYIM) / DQ %d" % (reed, di, role, dq))
    assert reed <= di and role + 2 <= dq
    havada_denetim()
    if tarama:
        cakisma()


# v8 · HAVADA PARÇA beyaz listesi (SPEC §1 · §2.1: belgelenmiş istisna)
BEYAZ_LISTE = ((r"_ray_ara_(sol|sag)$", "bilyeli ray ARA elemani: dis ve ic elemanla bilye kafesi uzerinden yuvarlanma temasi (modelde 0,5 mm idealize bosluk)"),)


def havada_denetim():
    """v8 · SPEC §1: her parça zemine DEĞEN parçalar zinciriyle bağlı (denetim_temas_v1 · kapalı konum) — beyaz liste açık yazılı"""
    import re as _re
    import denetim_temas_v1 as DT
    bl = {p["ad"] for p in PARCALAR if any(_re.search(k_, p["ad"]) for k_, _g in BEYAZ_LISTE)}
    son = DT.havada([(p["ad"], p["wp"]) for p in PARCALAR], haric=bl)
    n = DT.yaz(son, baslik="HAVADA PARCA DENETIMI v8 (kapali konum · beyaz liste %d parca: %s)" % (len(bl), "; ".join(g_ for _k, g_ in BEYAZ_LISTE)))
    assert n == 0, "havada %d bilesen var" % n
    return son


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
    (r"^k4_depo_ray_(dis_sag|ic_(sol|sag)|ara_(sol|sag))$", "Accuride DZ3832-TR"), (r"^k4_depo_kutu_(arka|on)_1\.5$", "K4 depo çekmece kutusu"),
    (r"^k4_depo_raf_tutucu_sag$", "Raf tutucu köşebent"), (r"^(k4_panel_klipsi_[1-3]|serit_panel_klipsi_\d)$", "Gizli panel klipsi"),
    (r"^sogutma_grubu_montaj_rayi_on$", "Yoğuşturucu montaj rayı"), (r"^k4_emis_yan_conta_sag$", "Sünger conta EPDM"), (r"^sogutma_grubu_taban_contasi$", "Kondenser çevre contası"),
    (r"^gider_kilifi_(sol_B3|sag_B4)$", "Gider kılıfı"), (r"^gider_kelepcesi_(sol_[1-9]|sag_\d)$", "Boru kelepçesi"),
    (r"_on_(pu|ic_sac_1\.0)$", "çekmece önü / kapak katmanı"), (r"^k4_kapak_depo_(pu|ic_sac_1\.0)$", "kapak katmanı"),
    (r"_kutu_(arka|on)_1\.0$", "çekmece kutusu"), (r"_on_baglanti_sag$", "ön bağlantı köşesi"), (r"_ray_adaptor_sag$", "ray adaptör lamı"),
    (r"_ray_dis_sag$", "Accuride DZ3832-0070"), (r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç eleman)"), (r"_ray_ara_(sol|sag)$", "Accuride DZ3832-0070 (ara eleman)"), (r"_reed_acik$", "Littelfuse 59135"),
    (r"_motor_(mili|gobegi|govde)$", "Transmotec PD3665"), (r"_enkoder_kapagi$", "Transmotec PD3665"),
    (r"^role_(0[2-9]|[1-9]\d)$", "Phoenix PLC-RSC"), (r"^kablo_kanali_(K[2-6]|ust|ust_F)$", "kablo kanalı"),
    (r"^evaporator_sag_lamel$", "Evaporatör lamelli"), (r"^evaporator_(sol|sag)_(yan_sac|dirsek)_[ab]$", "Evaporatör lamelli"),
    (r"^evaporator_(sol_askisi_2|sag_askisi_[12])$", "Evaporatör askısı"), (r"^damlama_teknesi_sag$", "Damlama teknesi"), (r"^fan_davlumbazi_sag$", "Fan davlumbazı"),
    (r"^fan_(sol_2|sag_[12])$", "ebm-papst 4414 FL"), (r"^gider_borusu_sag$", "Gider borusu"), (r"^isi_kalkani_takozu_([1-9]|1\d)$", "Isı köprüsü kesici takoz"),
    (r"^sogutma_grubu_takozu_[1-3]$", "Titreşim pedi"), (r"^damlama_teknesi_(sol_braketi_2|sag_braketi_[12])$", "Damlama teknesi braketi"),
    (r"^gider_cek_valfi_sag$", "Ördek gagası çek valf"), (r"^k4_emis_(yan_sac|on_kapama)_sag$", "Emiş şeridi sacı (× 2)"), (r"^onyuz_plint_donus_sag$", "Plint yan dönüşü (× 2)"),
    (r"^isi_kalkani_sag_sac$", "Isı kalkanı yan sacı (× 2)"),
    (r"^ayak_([1-9]|1\d)$", "Elesa LV.A-SST"), (r"^din_ray_1$", "DIN ray"),
    (r"_serit_bolmesi_([1-9]|1\d)$", "şerit + itici takımı"), (r"_itici(_yayi)?_\d+$", "şerit + itici takımı"),
    (r"^sogutma_grubu_(kondenser|fan|kompresor)$", "Secop CU NLE8.8CN"), (r"^plc_SM1221_DI16_[bc]$", "SM1221"), (r"^kasa_yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)"),
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
    return "SATIN ALMA" if any(s in ad for s in ("Accuride", "Transmotec", "Littelfuse", "Siemens", "Mean Well", "Electromen", "Phoenix", "Secop", "ebm-papst", "Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC", "çöp kovası", "poşeti", "Yaylı menteşe", "Titreşim pedi", "Minivalve", "Fastmount", "Sünger conta", "Kondenser çevre contası")) else "ÜRETİM"


if __name__ == "__main__":
    oz = modul(); denetim(oz)
    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v13")))   # v10: yerel derleme ağacında kalır (Kemal: BOM işi yok)
