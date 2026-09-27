# -*- coding: utf-8 -*-
"""store_cad_v5 -> v6 (27 Eyl 2026): ALÇAK HAT · TEK PARÇA ÇEKMECELİ DOLAP 0–4000 × 830 × 123–788 (SPEC_alcak_hat_v57.md)
Kemal: "bu teknik resme göre 3D modelle, sitede her şeyi güncelle, kontrol et" (teknik_alcak_hat_resim1_v4 + teknik_qr_tezgah_v4).
  · DÜZ ÇİZGİ 788 (eski B üstü 1060): A, C ve fırın bu düz üstün üstüne oturur. Plint 0–123 ve en alt ön 126 aynı.
  · DAĞILIM: K1 6 lahmacun · K2 6 lahmacun · K3 5 pide · K4 Secop + B panosu (arkada) + kaşar/sucuk deposu (v5 ile aynı, dar içecek YOK)
    · K5 (fırın altı) alttan üste 3 pide + tatlı (2 şerit = 12) · K6 (fırın altı, 585 geniş) 3 içecek (48) → 24 çekmece:
    pide 160 · lahmacun 432 · içecek 144 · tatlı 12 (2 gün kuralı 160 / 400 / 139 / 11).
  · FIRIN ALTI: PU 60 ısı kalkanı (2517–3793 × 728–788) → K5/K6 iç tavanı 668 (yığın sınırı L − 290 = 498; K1–K3 L − 230 = 558).
  · TAŞIYICI ÇERÇEVE: fırın (≈200 kg) + fırın üstü raf yükü (99 kg) düz 788'e biner → 304 profil 2 kiriş + 3 çapraz ısı kalkanının
    içinde, 6 dikme B4 / B5 / B6 bölmelerinin içinde, dikmelerin altında ayak. Yük hesabı denetimde (VARSAYIM yükler).
  · ŞERİT 3810–4000 (soğuk DEĞİL, 3810'da yalıtımlı ara duvar): ROBOT ÇÖPÜ 15 L (165 × 400 × 300, poşetli, kızakta) + atma boşluğu
    + yaylı klape (üst panelde, robot eli içe iter) + servis kapağı (kova öne çekilerek boşaltılır).
  · SOĞUTMA: 6 soğuk kolon (K1, K2, K3, K4 depo, K5, K6) → 6 evaporatör + 6 fan (v5: 4) · Secop kapasitesi hesabı AÇIK (VARSAYIM).
  · PLC: 24 çekmece × 2 reed = 48 > 46 DI → 3. SM1221 DI16.
  · v5 hataları düzeltildi: tatlı çekmecesinin bütün parçaları çakışma taramasından ve BOM'dan düşüyordu ("_tatli_" süzgeci) ·
    ic1 çekmecelerinde BOM adı öneki silinmiyordu ([a-z]+) · SM1221 BOM'da 1 sayılıyordu · K4 ara PU'su yan duvara kadar gitmiyordu ·
    K4 depo açıklığı GN 1/2'nin üstünden alçaktı (kap çekilemiyordu).
  · BOM 1_STORE_v9.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v5.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:100])
    s = s.replace(a, b)


def blok(bas, son, yeni, son_dahil=False):
    """bas … son arasını (son hariç / dahil) yeni metinle değiştirir; iki işaret de TEK olmalı"""
    global s
    assert s.count(bas) == 1 and s.count(son) == 1, "isaret YOK/COK: %s / %s" % (bas[:60], son[:60])
    a0 = s.index(bas); a1 = s.index(son) + (len(son) if son_dahil else 0)
    assert a1 > a0
    s = s[:a0] + yeni + s[a1:]


# ================================================================ başlık
degis('''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v5 (25 Eyl 2026)''',
      '''"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v6 (27 Eyl 2026) · ALÇAK HAT (SPEC_alcak_hat_v57.md · resim teknik_alcak_hat_resim1_v4
    + teknik_qr_tezgah_v4 · Kemal: "bu teknik resme göre 3D modelle, sitede her şeyi güncelle, kontrol et")
v6: TEK PARÇA DOLAP 0–4000 × 830 × 123–788 (+3 °C), üstü DÜZ 788 = A, C ve fırının altı. K1 6 lahmacun · K2 6 lahmacun · K3 5 pide ·
    K4 Secop (önde) + B panosu (arkada) + kaşar/sucuk deposu (v5 ile aynı; dar içecek YOK) · K5 fırın altı 3 pide + tatlı (2 şerit = 12) ·
    K6 fırın altı 3 içecek (48) · fırın altında PU 60 ısı kalkanı (2517–3793 × 728–788) → K5/K6 iç tavanı 668 · TAŞIYICI ÇERÇEVE (304 profil:
    2 kiriş + 3 çapraz ısı kalkanının içinde, 6 dikme B4/B5/B6 bölmelerinde, altlarında ayak) · ŞERİT 3810–4000 soğuk DEĞİL: ROBOT ÇÖPÜ
    15 L (poşetli, kızakta) + atma boşluğu + yaylı klape + servis kapağı · 6 evaporatör + 6 fan · 24 çekmece: pide 160 · lahmacun 432 ·
    içecek 144 · tatlı 12 (2 gün). Önceki: store_cad_v5.py (yap_store_cad_v6.py) · BOM 1_STORE_v9
v5 (25 Eyl 2026)''')
degis('''KOORDİNAT: hat ile aynı — x 0..2500 (B), y 0..1060, z 0 = çekmece ön yüzü, −830 arka.''',
      '''KOORDİNAT: hat ile aynı — x 0..4000 (dolap), y 0..788 (düz çizgi), z 0 = çekmece ön yüzü, −830 arka.''')

# ================================================================ dağılım + ana ölçüler
blok('''# v5 · ALT KISIM v3 (Kemal 25 Eyl''', '''H_B, W_B, DZ = _g["H_B"], _g["W_B"], _g["DZ"]\n''', r'''# v6 · ALÇAK HAT (27 Eyl 2026 · SPEC_alcak_hat_v57): TEK PARÇA DOLAP 0–4000 · DÜZ ÇİZGİ 788 · soğukta TAM 2 gün:
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
''', son_dahil=True)
degis('''"bakir": ((0.72, 0.45, 0.20, 1.0), 0.9, 0.35), "kanal": ((0.55, 0.58, 0.62, 1.0), 0.0, 0.7)}.items():''',
      '''"bakir": ((0.72, 0.45, 0.20, 1.0), 0.9, 0.35), "kanal": ((0.55, 0.58, 0.62, 1.0), 0.0, 0.7),
               "poset": ((0.13, 0.13, 0.14, 1.0), 0.0, 0.8)}.items():''')

# ================================================================ kotlar
degis('''Y_TAVAN = 1000.0''',
      '''Y_TAVAN = H_B - 60.0                   # v6: 728 — K1–K4 iç tavanı (üst 60 = iç sac 1 + PU 57,5 + dış sac 1,5)
Y_TAVAN_F = Y_TAVAN - 60.0             # v6: 668 — fırın altı K5, K6: tavan 60 + ISI KALKANI PU 60 (728–788) = 120 → yığın sınırı L − 290''')
degis('''TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6)          # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104''',
      '''TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6, nx=2)    # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104 · v6: 2 şerit × 6 = 12 (2 gün 11)''')
degis('''K4_YO = 123.0 + 1.5 + 4.0 + 272.0 + 8.0 + 30.0 + GN_H + 1.0 + 3.0 + 15.0      # K4 ilk dar çekmece açıklığı 687,5''',
      '''# v6: K4_YO (K4 dar içecek çekmeceleri) kalktı''')
degis('''KAN_UST = (975.0, 1000.0)''',
      '''KAN_UST = (Y_TAVAN - 25.0, Y_TAVAN)            # v6: 703–728 · K1 → K4 yatay kanal
KAN_UST_F = (Y_TAVAN_F - 25.0, Y_TAVAN_F)      # v6: 643–668 · K4 → K6 (fırın altı) yatay kanal''')

# ================================================================ kolonlar + v6 sabitleri (çerçeve, şerit, ayak, yük)
blok('''def kolonlar():''', '''K1X = KOLON_X["K1"]\n''', r'''def kolonlar():
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


def profil(k, eks, t=2.0):
    """içi boş dikdörtgen profil (et t) · eks = profilin boyu hangi eksende"""
    x0, x1, y0, y1, z0, z1 = k
    ic = {"x": (x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t), "y": (x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t),
          "z": (x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 + 1.0)}[eks]
    return kut(*k).cut(kut(*ic))
''', son_dahil=True)

# ================================================================ çekmece: tatlı 2 şerit · tatlı kabı adı · sensör lamı
degis('''        nx = int((ix1 - ix0 - 12.0 - 2 * r) // px) + 1''',
      '''        nx = int((ix1 - ix0 - 12.0 - 2 * r) // px) + 1
        if tat:
            nx = min(nx, TATLI["nx"])                                   # v6: 2 şerit × 6 = 12 (2 gün 11) · kalan genişlik boş''')
degis('''                ekle("%s_%s_%d" % (kod, "tatli" if tat else "kutu330", n), urun.translate((a, y0, b)), "hamur" if tat else "kutu_icecek", kod, grup=G); n += 1''',
      '''                ekle("%s_%s_%d" % (kod, "tatlikabi" if tat else "kutu330", n), urun.translate((a, y0, b)), "hamur" if tat else "kutu_icecek", kod, grup=G); n += 1''')
degis('''    ekle(kod + "_sensor_lami", kut(x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6, my0 + SEN[1], my0 + SEN[1] + 2.0, Z_ARKA, Z_AVARA - 12.0), "celik", kod)''',
      '''    # v6: lamın arka ucu kablo kanalının önünde biter (K2 üst çekmecesinde lam 716,6–718,6 ↔ yatay kanal 703–728 çakışıyordu);
    #     arka ucu kanalın altından arka duvara L tırnakla bağlanır [VARSAYIM · modelde yok]
    ekle(kod + "_sensor_lami", kut(x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6, my0 + SEN[1], my0 + SEN[1] + 2.0, KAN_Z[1] + 1.0, Z_AVARA - 12.0), "celik", kod)''')

degis('''                 bom=("Şerit bölmesi + yaylı itici takımı (market tipi)", nx, "standart raf itici sistemi · şerit %.0f · ürünü öne iter" % px,''',
      '''                 bom=("Şerit bölmesi + yaylı itici takımı (market tipi) · şerit %.0f" % px, nx, "standart raf itici sistemi · ürünü öne iter",''')

# ================================================================ gövde (kasa) — baştan
blok('''def kasa():''', '''def modul():''', r'''def kasa():
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
    ekle("plint_on_1.5", kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0), "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride", ""))
    for i, (ax, az) in enumerate(AYAK_XZ):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", B,
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz AISI 304 · taban Ø40 · yükseklik 123",
                  "elesa-ganter.com LV.A-SST · 123'e uygun diş boyu + taşıma yükü katalogdan seçilecek · fırın altında dikmelerin altında") if i == 0 else None)

    # ---------------- KABUK SACLARI ----------------
    sac("yan_dis_sac_sol", (0.0, 1.5, Y_PLINT, H_B, -DZ, -40.0), bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · sol ön kenar kapak arkasında (z −40) · sağ (şerit) −18'e kadar", ""))
    sac("yan_dis_sac_sag", (W_B - 1.5, W_B, Y_PLINT, H_B, -DZ, -SERIT_DONUS))
    sac("tavan_dis_sac", (1.5, W_B - 1.5, H_B - 1.5, H_B, -DZ, -40.0), bom=("Tavan dış sacı", 1, "304 1,5 · A, C ve fırın bunun üstüne oturur (fırın altında taşıyıcı çerçeve)", ""))
    VENT = (K4X + 60.0, K4X + K4W - 60.0, -500.0, -120.0)            # K4 sıcak bölmesi: Secop havası tabandan plinte
    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0), ek=kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3]))
    sac("arka_dis_sac", (1.5, W_B - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5))
    sac("yan_ic_sac_sol", (29.0, 30.0, Y_TABAN, Y_TAVAN, Z_ARKA, -41.5))
    sac("yan_on_donus_sol", (1.5, 30.0, Y_PLINT + 1.5, H_B - 1.5, -41.5, -40.0))
    # iç tavan: K1–K4 728 · fırın altı (K5, K6) 668 — üstünde ısı kalkanı
    sac("tavan_ic_sac", (X_IC0, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5))
    sac("tavan_ic_sac_F", (XF0, XB[5], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, -41.5))
    TD_A, TD_F = (X_IC0, XF0, Y_TAVAN, H_B - 1.5, -41.5, -40.0), (XF0, XS - 1.0, Y_TAVAN_F, H_B - 1.5, -41.5, -40.0)
    ekle("tavan_on_donus", kut(*TD_A).union(kut(*TD_F)), "sac", B); SACK.extend([TD_A, TD_F])
    sac("taban_ic_sac", (X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5))
    sac("taban_k4_kademe_saci", (K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -41.5),
        bom=("Taban kademe sacı 1,0", 1, "304 · yalıtımlı tabanın K4 tarafındaki ucunu kapatır", "K4 sıcak bölmesi 40 mm alçak"))
    sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5))
    sac("taban_on_donus", (X_IC0, XS - 1.0, Y_PLINT + 1.5, Y_TABAN, -41.5, -40.0))
    sac("arka_ic_sac", (X_IC0, XF0, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA))
    sac("arka_ic_sac_k4_alt", (K4X, XF0, Y_PLINT + 1.5, Y_TABAN, Z_ARKA - 1.0, Z_ARKA))
    sac("arka_ic_sac_F", (XF0, XB[5], Y_TABAN, Y_TAVAN_F, Z_ARKA - 1.0, Z_ARKA))
    # ön çerçevenin kutuları (açıklıklar sonra kesilir) PU'dan önce kayda girer
    CER_A, CER_F = (X_IC0, XF0, Y_TABAN, Y_TAVAN, Z_CER0, Z_CER1), (XF0, XS - 1.0, Y_TABAN, Y_TAVAN_F, Z_CER0, Z_CER1)
    SACK.extend([CER_A, CER_F])

    # ---------------- BÖLMELER 35 (sac 1 + PU 33 + sac 1) · üst arka köşede KABLO GEÇİŞİ 40 × 25 ----------------
    GECIS = lambda x0_, ku: kut(x0_ - 1, x0_ + BOLME + 1, ku[0], ku[1] + 1, KAN_Z[0] - 1, KAN_Z[1])
    for i, x0_ in enumerate(XB[:3]):                                   # B1–B3: K1 | K2 | K3 | K4 · 164,5–728
        g_ = GECIS(x0_, KAN_UST)
        sac("bolme_%d_sac_a" % i, (x0_, x0_ + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=g_)
        sac("bolme_%d_sac_b" % i, (x0_ + BOLME - 1.0, x0_ + BOLME, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=g_)
    g4 = GECIS(XB[3], KAN_UST_F)                                       # B4: K4 | K5 — K4 yanı tabana iner (sıcak bölme), K5 yanı 163,5'ten
    sac("bolme_3_sac_a", (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    sac("bolme_3_sac_b", (XB[3] + BOLME - 1.0, XB[3] + BOLME, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    g5 = GECIS(XB[4], KAN_UST_F)                                       # B5: K5 | K6 · 164,5–668
    sac("bolme_4_sac_a", (XB[4], XB[4] + 1.0, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    sac("bolme_4_sac_b", (XB[4] + BOLME - 1.0, XB[4] + BOLME, Y_TABAN, Y_TAVAN_F, Z_ARKA, Z_CER0), ek=g5)
    # B6: K6 | ŞERİT — soğuk zarfın sağ duvarı (3810'da yalıtımlı ara duvar); K6 fitili z −55'e kadar geldiği için PU önde −56'da biter
    sac("bolme_5_sac_a", (XB[5], XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN, Z_ARKA - 1.0, Z_CER0))
    sac("bolme_5_sac_b", (XS - 1.0, XS, Y_PLINT + 1.5, H_B - 1.5, ZP0, -40.0),
        bom=("Ara duvar sacı 1,0 (soğuk ↔ şerit)", 1, "304 · x 3809–3810 · taşıyıcı kiriş geçiş oyuklu", "şerit tarafı · arkasında PU 33"))

    # ---------------- PU (40 kg/m³ enjeksiyon) — sırayla: her kutu öncekilerden, sacdan ve çelikten kesilir ----------------
    pu("yan_pu_sol", (1.5, 29.0, Y_PLINT + 1.5, H_B - 1.5, ZP0, ZP1))
    pu("isi_kalkani_pu_60", (X_F[0], X_F[1], Y_TAVAN, H_B - 1.5, ZP0, ZP1),
       bom=("Isı kalkanı PU 60 · fırın altı", 1, "PU 40 kg/m³ · gövdeyle aynı enjeksiyon · x %.0f–%.0f · y %.0f–%.0f (dış sacla 60)" % (X_F[0], X_F[1], Y_TAVAN, H_B),
            "fırın altında toplam 120: kalkan 60 + tavan 60 → K5/K6 iç tavanı %.0f · taşıyıcı kirişler bunun içinde" % Y_TAVAN_F))
    pu("tavan_pu_57.5", (29.0, X_F[0], Y_TAVAN + 1.0, H_B - 1.5, ZP0, ZP1),
       bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 27,5 · tavan 57,5 (fırın altı 117,5) · arka 37,5 · taban 39 · bölme 33"))
    pu("bolme_5_pu_ust", (XB[5] + 1.0, XS - 1.0, Y_TAVAN, H_B - 1.5, ZP0, ZP1))
    pu("tavan_pu_F", (XF0, XB[5] + 1.0, Y_TAVAN_F + 1.0, Y_TAVAN, ZP0, ZP1))
    pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))
    pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))
    pu("arka_pu_37.5", (29.0, XF0 - 1.0, Y_PLINT + 1.5, Y_TAVAN + 1.0, ZP0, Z_ARKA - 1.0))
    pu("arka_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_TABAN - 1.0, Y_TAVAN_F + 1.0, ZP0, Z_ARKA - 1.0))
    for i, x0_ in enumerate(XB[:3]):
        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=GECIS(x0_, KAN_UST))
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

    # ---------------- EVAPORATÖR (roll-bond, arka duvarda) + FAN (ebm-papst 4414 FNH) — 6 soğuk kolon ----------------
    for kol in KOLON_AD:
        cx = KOLON_X[kol]
        e0, e1 = 200.0, (KAN_UST[0] if kol in ("K1", "K2", "K3") else KAN_UST_F[0]) - 3.0     # 200–700 · fırın altı 200–640 [VARSAYIM yükseklik]
        ekle("evaporator_%s" % kol, kut(cx + 250.0, cx + 560.0, e0, e1, Z_ARKA, Z_ARKA + 2.0), "aluminyum", "B_SOGUTMA",
             bom=("Evaporatör roll-bond levha", len(KOLON_AD) + 1, "alüminyum 1,5 + kanal · ölçüye üretim",
                  "arka duvara yapışık · K1–K3 310 × 500 · K5–K6 310 × 440 · K4 140 × 195 · alan ve Secop kapasitesi VARSAYIM (yük hesabı AÇIK)") if kol == "K1" else None)
        fy0 = (e0 + e1) / 2.0 - 59.5
        ekle("fan_%s" % kol, kut(cx + 345.0, cx + 464.0, fy0, fy0 + 119.0, Z_ARKA + 3.0, Z_ARKA + 28.0), "motor", "B_SOGUTMA",
             bom=("Fan ebm-papst 4414 FNH", len(KOLON_AD) + 1, "24 V · 119 × 119 × 25", "evaporatör önünde, havayı kolon içine basar") if kol == "K1" else None)
    ekle("evaporator_K4", kut(K4X + 240.0, K4X + 380.0, 445.0, KAN_UST_F[0] - 3.0, Z_ARKA, Z_ARKA + 2.0), "aluminyum", "B_SOGUTMA")   # depo: 445–640
    ekle("fan_K4", kut(K4X + 255.0, K4X + 374.0, 483.0, 602.0, Z_ARKA + 3.0, Z_ARKA + 28.0), "motor", "B_SOGUTMA")

    # ---------------- K4 (2027,5–2500): SICAK bölme (Secop önde, B panosu arkada) · ara PU · KAŞAR + SUCUK DEPOSU (soğuk) — v5 ile aynı ----------------
    kx0, kx1 = K4X, K4X + K4W
    CU = (350.0, 272.0, 450.0)
    cx0, cy0, cz1 = kx0 + 25.0, Y_PLINT + 1.5 + 4.0, Z_CER0 - 10.0            # ünite sıcak bölmenin tek sac tabanında (128,5)
    ekle("sogutma_grubu_taban", kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz1 - CU[2], cz1), "motor", "B_SOGUTMA",
         bom=("Yoğuşturucu ünite Secop CU KLF4.0CND R290", 1, "314H6008 · 335 W @ −10/25 °C · 1/6 HP · 15,2 kg",
              "272 × 350 × 450 · secop.com datasheet · v6: 6 evaporatör (v5: 4) → soğutma yükü hesabı AÇIK [VARSAYIM]"))
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
    ekle("k4_depo_raf", kut(kx0, K4_SAG, g0 + 110.0, g0 + 111.5, Z_ARKA + 32.0, Z_CER0), "sac", "B_DEPO")   # v6: arka ucu K4 evaporatör/fanının önünde (−758)
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
                 bom=("Yoğuşturucu bölmesi kapağı", 1, "304 1,5 · yalıtımsız · ızgaralı hava penceresi", "hava önden girer, tabandan plinte çıkar"))
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


''')

# ================================================================ denetim — baştan
blok('''def denetim(ozet, tarama=True):''', '''def _kesis(L1, L2, esik, ayni=True):''', r'''def _kesisim(sekil, parcalar, haric=(), esik=1.0):
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
    print("CEKMECELI DOLAP v6 · tek parca 0-%.0f x %.0f-%.0f · %d parca · %d cekmece · birimler: %s"
          % (W_B, Y_PLINT, H_B, len(PARCALAR), len(CEK), ", ".join(sorted({p["birim"] for p in PARCALAR if not p["birim"].startswith("CEK_")}))))
    BB = {p["ad"]: p["wp"].val().BoundingBox() for p in PARCALAR}
    assert len(BB) == len(PARCALAR), "parca adlari tekil degil"
    yb = lambda ad: BB[ad]
    # ---- ALT TABAN ÇİZGİSİ + DÜZ ÜST (katılardan ölçülür) ----
    alt = yb("taban_dis_sac").ymin
    ic_ust = yb("taban_ic_sac").ymax
    on_alt = min(BB[p["ad"]].ymin for p in PARCALAR if p["ad"].endswith("_on_dis_sac_1.5") and p["grup"] == "CEKMECE")
    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin; sr_alt = yb("serit_on_kapak").ymin
    govde_alt = min(BB[p["ad"]].ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
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
    # ---- ISI KALKANI ----
    ik = yb("isi_kalkani_pu_60")
    print("ISI KALKANI PU 60: x %.0f-%.0f · y %.0f-%.1f (+ dis sac 1,5 = %.0f) · firin altinda ust katman %.0f (ic sac 1 + PU %.1f + dis sac 1,5; K5/K6 ic tavani %.0f) · K1-K4 ust katman %.0f (tavan %.0f)"
          % (ik.xmin, ik.xmax, ik.ymin, ik.ymax, H_B, H_B - Y_TAVAN_F, H_B - Y_TAVAN_F - 2.5, Y_TAVAN_F, H_B - Y_TAVAN, Y_TAVAN))
    assert abs(ik.xmin - X_F[0]) < 0.05 and abs(ik.xmax - X_F[1]) < 0.05 and abs(ik.ymin - Y_TAVAN) < 0.05
    # ---- SOĞUTMA (bilgi · VARSAYIM) · iletimle ısı kazancı kaba tahmini ----
    k_pu, T_ic, T_ort, T_fir, T_sic = 0.024, 3.0, 25.0, 60.0, 35.0     # W/m·K PU [VARSAYIM] · +3 °C · ortam · fırın tabanı · Secop bölmesi [VARSAYIM]
    Lz = (-Z_ARKA - 41.5) / 1000.0
    xa, xk, xf = (K4X - X_IC0) / 1000.0, (K4_SAG - K4X) / 1000.0, (BOLME_X[5] - BOLME_X[3] - BOLME) / 1000.0
    ha, hk, hf, hs = (Y_TAVAN - Y_TABAN) / 1000.0, (Y_TAVAN - yb("k4_ara_sac_ust").ymax) / 1000.0, (Y_TAVAN_F - Y_TABAN) / 1000.0, (yb("k4_ara_sac_alt").ymin - Y_TABAN) / 1000.0
    yuz = [("on kapaklar", xa * ha + xk * hk + xf * hf, 0.0375, T_ort), ("arka", xa * ha + xk * hk + xf * hf, 0.0375, T_ort),
           ("tavan K1-K4", (xa + xk) * Lz, 0.0575, T_ort), ("tavan firin alti", xf * Lz, 0.1175, T_fir),
           ("taban K1-K3", xa * Lz, 0.039, T_ort), ("K4 depo tabani (Secop ustu)", xk * Lz, 0.028, T_sic), ("taban K5-K6", xf * Lz, 0.039, T_ort),
           ("sol yan", ha * Lz, 0.0275, T_ort), ("B6 (serit)", hf * Lz, 0.033, T_ort), ("B3 + B4 (Secop bolmesi yanlari)", 2 * hs * Lz, 0.033, T_sic)]
    Q = sum(k_pu * A_ * (Td - T_ic) / t_ for _a, A_, t_, Td in yuz)
    ev = sum(BB[p["ad"]].xlen * BB[p["ad"]].ylen for p in PARCALAR if p["ad"].startswith("evaporator_")) / 1e6
    print("SOGUTMA: %d evaporator (%.2f m² roll-bond) + %d fan · Secop CU KLF4.0CND 335 W @ −10/25 °C · iletim kazanci ~%.0f W (PU k %.3f, ortam %.0f, firin tabani %.0f °C VARSAYIM) · kapi acma + urun yuku HESAPLANMADI -> kapasite hesabi ACIK"
          % (len([p for p in PARCALAR if p["ad"].startswith("evaporator_")]), ev, len([p for p in PARCALAR if p["ad"].startswith("fan_K")]), Q, k_pu, T_ort, T_fir))
    di = 14 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1221")]); dq = 10 + 16 * len([p for p in PARCALAR if p["ad"].startswith("plc_SM1222")])
    reed = len([p for p in PARCALAR if p["ad"].endswith(("_reed_kapali", "_reed_acik"))]); role = len([p for p in PARCALAR if p["ad"].startswith("role_")])
    print("PLC G/C: reed %d / DI %d · role %d + surucu 2 (yon + etkin VARSAYIM) / DQ %d" % (reed, di, role, dq))
    assert reed <= di and role + 2 <= dq
    if tarama:
        cakisma()


''')

# ================================================================ çakışma + BOM
degis('''"_tatli_" not in p["ad"]]''', '''"_tatlikabi_" not in p["ad"]]''')
degis('''or "_tatli_" in p["ad"]:''', '''or "_tatlikabi_" in p["ad"]:''')
degis(r'''r"^CEK_K\d_[a-z]+_\d+_"''', r'''r"^CEK_K\d_[a-z0-9]+_\d+_"''', n=2)
degis('''             "bakir": "", "izgara": "304 lama", "pom": ""}.get(p["mal"], p["mal"])''',
      '''             "bakir": "", "izgara": "304 lama", "pom": "", "poset": "LDPE"}.get(p["mal"], p["mal"])''')
blok('''ALT_KURAL = [''', '''def _alt(ad):''', r'''ALT_KURAL = [
    (r"_on_(pu|ic_sac_1\.0)$", "çekmece önü / kapak katmanı"), (r"^k4_kapak_depo_(pu|ic_sac_1\.0)$", "kapak katmanı"),
    (r"_kutu_(arka|on)_1\.0$", "çekmece kutusu"), (r"_on_baglanti_sag$", "ön bağlantı köşesi"), (r"_ray_adaptor_sag$", "ray adaptör lamı"),
    (r"_ray_dis_sag$", "Accuride DZ3832-0070"), (r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç eleman)"), (r"_ray_ara_(sol|sag)$", "Accuride DZ3832-0070 (ara eleman)"), (r"_reed_acik$", "Littelfuse 59135"),
    (r"_motor_(mili|gobegi|govde)$", "Transmotec PD3665"), (r"_enkoder_kapagi$", "Transmotec PD3665"),
    (r"^role_(0[2-9]|[1-9]\d)$", "Phoenix PLC-RSC"), (r"^kablo_kanali_(K[2-6]|ust|ust_F)$", "kablo kanalı"),
    (r"^evaporator_K[2-6]$", "roll-bond evaporatör"), (r"^fan_K[2-6]$", "ebm-papst 4414 FNH"),
    (r"^ayak_([1-9]|1\d)$", "Elesa LV.A-SST"), (r"^din_ray_1$", "DIN ray"),
    (r"_serit_bolmesi_([1-9]|1\d)$", "şerit + itici takımı"), (r"_itici(_yayi)?_\d+$", "şerit + itici takımı"),
    (r"^sogutma_grubu_(kondenser|fan|kompresor)$", "Secop CU KLF4.0CND"), (r"^plc_SM1221_DI16_[bc]$", "SM1221"), (r"^yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)"),
    (r"^(yan_pu_sol|arka_pu_37\.5|arka_pu_F|taban_pu|taban_pu_F|tavan_pu_F|bolme_\d_pu|bolme_5_pu_ust|k4_ara_pu)$", "PU köpük gövde"),
    (r"^tasiyici_kiris_arka$", "Taşıyıcı kiriş 40 × 40 × 2"), (r"^tasiyici_capraz_[1-9]$", "Taşıyıcı çapraz 30 × 40 × 2"), (r"^tasiyici_dikme_[1-9]$", "Taşıyıcı dikme 30 × 30 × 2"),
]


''')
degis('''"Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC")) else "ÜRETİM"''',
      '''"Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC", "çöp kovası", "poşeti", "Yaylı menteşe")) else "ÜRETİM"''')
degis('''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v8")))''',
      '''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v9")))''')

# ================================================================ denetçi düzeltmesi (27 Eyl): v5'ten kalan eski adet metinleri (başlık + ALT_KURAL yorumu)
degis('''seçici röle Phoenix Contact PLC-RSC-24DC/21 (6,2 mm) × 21''',
      '''seçici röle Phoenix Contact PLC-RSC-24DC/21 (6,2 mm) × 24 (v6: 24 çekmece)''')
degis('''6ES7214-1AG40-0XB0 + 2 × SM1221 DI16 + SM1222 DQ16''',
      '''6ES7214-1AG40-0XB0 + 3 × SM1221 DI16 + SM1222 DQ16 (v6: 48 reed → 62 DI)''')
degis('''role "21", fan "3" ...)''', '''role "24", fan "6" ...)''')

io.open(os.path.join(U, "store_cad_v6.py"), "w", encoding="utf-8").write(s)
print("store_cad_v6.py yazildi")
