# -*- coding: utf-8 -*-
"""store_cad_v6.py -> store_cad_v7.py (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN
Kemal: "ya tamam öğrendiğin yeter, cooling'de de onlarla yap işte" · "hamur fırıncıdan soğuk gelemez" · "durdur kendi yap"
Kaynak: _local/sogutma_hesabi_v1.html (standart uygulama + yük hesabı). Kayıtlı parça ölçüleri (çekmece, kova, GN, fırın kotu) DEĞİŞMEZ.
  1 · Secop CU KLF4.0CND (309 W @ −10/32 °C, gereken 552–661 W) -> CU NLE8.8CN (737 / 688 / 586 W) · 297 yüksek -> K4 ara katman +25
  2 · 6 roll-bond levha + 7 × 4414 FNH (72 W ısı) KALKTI -> 2 bölge × lamelli epoksi kaplı evaporatör + davlumbaz + 2 × 4414 FL
      (sol K2 arkası -> K1–K3 · sağ K5 arkası, tatlı çekmecesinin altı -> K4 depo + K5–K6) · bölmelerde arka hava geçişleri
  3 · damlama teknesi -> Ø12 gider -> tabandan plinte -> K4 altındaki kondenser ATIŞ KANALINDA buharlaştırma tavası; plint önünde ızgara
  4 · fırın altı ısı kalkanı PU 60 -> hava boşluğu + ayırma sacı + parlak paslanmaz ışınım sacı (takozlu) + arka yarıklar (rapor seçenek b)
  5 · sol yan PU 27,5 -> 60 (iç sac x 62,5; K1 rayları duvara oturur, çekmece ölçüsü aynı)
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v6.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


def satir(icerir, yeni, n=1):
    """icerir'i tasiyan satirin TAMAMINI yeni ile degistirir"""
    global s
    L = s.split(NL)
    i_ = [i for i, l in enumerate(L) if icerir in l]
    assert len(i_) == n, (len(i_), icerir[:120])
    for i in reversed(i_):
        L[i:i + 1] = yeni.split(NL)
    s = NL.join(L)


def blok_sil(bas, son):
    """bas'i tasiyan satirdan son'u tasiyan satira kadar (dahil) siler"""
    global s
    L = s.split(NL)
    i = [k for k, l in enumerate(L) if bas in l]; assert len(i) == 1, bas
    j = [k for k, l in enumerate(L) if son in l and k >= i[0]]; assert j, son
    del L[i[0]:j[0] + 1]
    s = NL.join(L)


def once(icerir, ek):
    global s
    L = s.split(NL)
    i = [k for k, l in enumerate(L) if icerir in l]; assert len(i) == 1, icerir
    L[i[0]:i[0]] = ek.split(NL)
    s = NL.join(L)


# ================================================================ 0 · başlık
degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v6 (27 Eyl 2026) · ALÇAK HAT',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v7 (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1 · Kemal: "öğrendiğin yeter,' + NL +
      '    cooling\'de de onlarla yap" · "hamur fırıncıdan soğuk gelemez")' + NL +
      'v7: Secop CU NLE8.8CN (737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C; KLF4.0CND 32 °C\'de 309 W, gereken 552–661 W) · 297 yüksek → K4 ara katman +25' + NL +
      '    · 6 roll-bond levha + 7 × 4414 FNH KALKTI → 2 bölge × lamelli epoksi kaplı evaporatör + davlumbaz + 2 × ebm-papst 4414 FL (sol: K2 arkası → K1–K3 ·' + NL +
      '    sağ: K5 arkası, tatlının altı → K4 depo + K5–K6) · bölmelerde arka hava geçişleri · damlama teknesi → Ø12 gider → plint → kondenser atış kanalında' + NL +
      '    buharlaştırma tavası · fırın altında PU 60 yerine HAVA BOŞLUĞU + ayırma sacı + parlak paslanmaz ışınım sacı + arka yarıklar · sol yan PU 27,5 → 60.' + NL +
      '    Önceki: store_cad_v6.py (yap_store_cad_v7.py) · BOM 1_STORE_v10' + NL +
      'v6 (27 Eyl 2026) · ALÇAK HAT')
satir("  soğutma Secop CU KLF4.0CND R290 (314H6008)",
      "  soğutma Secop CU NLE8.8CN R290 · 297 yüksek · 737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C (v7; v6 KLF4.0CND 272 yüksek, 309 W @ 32 °C yetmiyordu)")
satir("  fan     ebm-papst 4414 FNH (119 × 119 × 25, 24 V)",
      "  fan     ebm-papst 4414 FL (119 × 119 × 25, 24 V, 1,2 W, 94 m³/h) · evaporatör: lamelli Cu/Al, epoksi kaplı (ölçüye üretim) — v7")

# ================================================================ 1 · v7 sabitleri (AYAK_XZ'den sonra)
once("def profil(k, eks, t=2.0):", '''# v7 · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1): 2 bölge × lamelli evaporatör + davlumbaz + 2 fan, bölmelerde arka hava geçişi
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

''')

# ================================================================ 2 · kabuk: plint ızgarası, taban gider delikleri, sol yan PU 60, arka yarıklar
satir('    ekle("plint_on_1.5", kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0), "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride", ""))',
      '''    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0)
    for a_, b_, c_, d_ in PLINT_IZGARA:                                  # v7: kondenser atış kanalının önü ızgaralı
        pl_ = pl_.cut(kut(a_, b_, c_, d_, -62.5, -59.0))
    ekle("plint_on_1.5", pl_, "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride · v7: K4 altında 6 yarık (kondenser atışı)", ""))''')
once('    VENT = (K4X + 60.0, K4X + K4W - 60.0, -500.0, -120.0)',
     '''    DR_DELIK = None                                                   # v7: gider borularının taban delikleri Ø14
    for _yan, _e in EVAP.items():
        _d = sily(_e["gider"][0], DR_Z, DR_R + 1.0, Y_PLINT - 1.0, Y_TABAN + 1.0)
        DR_DELIK = _d if DR_DELIK is None else DR_DELIK.union(_d)''')
satir('    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0), ek=kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3]))',
      '    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0), ek=kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3]).union(DR_DELIK))')
satir('    sac("arka_dis_sac", (1.5, W_B - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5))',
      '''    AY_ = None                                                          # v7: fırın altı hava boşluğunun arka yarıkları
    for a_, b_ in ARKA_YARIK:
        _k = kut(a_, b_, ARKA_YARIK_Y[0], ARKA_YARIK_Y[1], -DZ - 1.0, -DZ + 2.5)
        AY_ = _k if AY_ is None else AY_.union(_k)
    sac("arka_dis_sac", (1.5, W_B - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), ek=AY_)''')
satir('    sac("yan_ic_sac_sol", (29.0, 30.0, Y_TABAN, Y_TAVAN, Z_ARKA, -41.5))',
      '    sac("yan_ic_sac_sol", (X_IC0S, X_IC0S + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0))      # v7: PU 60 (v6 29–30 · PU 27,5) · önde çerçeve sacına dayanır')
satir('    sac("tavan_ic_sac", (X_IC0, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5))',
      '    sac("tavan_ic_sac", (X_IC0S, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5))')
satir('    sac("taban_ic_sac", (X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5))',
      '    sac("taban_ic_sac", (X_IC0S, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)')
satir('    sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5))',
      '    sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)')
satir('    sac("arka_ic_sac", (X_IC0, XF0, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA))',
      '    sac("arka_ic_sac", (X_IC0S, XF0, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA))')

# ================================================================ 3 · bölmelerde arka hava geçişleri
degis("        g_ = GECIS(x0_, KAN_UST)\n", "        g_ = hava_gecis(i, GECIS(x0_, KAN_UST))                          # v7: + arka hava geçişi\n")
degis("    g4 = GECIS(XB[3], KAN_UST_F)", "    g4 = hava_gecis(3, GECIS(XB[3], KAN_UST_F))")
degis("    g5 = GECIS(XB[4], KAN_UST_F)", "    g5 = hava_gecis(4, GECIS(XB[4], KAN_UST_F))")
degis('        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=GECIS(x0_, KAN_UST))',
      '        pu("bolme_%d_pu" % i, (x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), ek=hava_gecis(i, GECIS(x0_, KAN_UST)))')

# ================================================================ 4 · fırın altı: PU 60 yerine hava boşluğu + ayırma sacı + ışınım sacı (sac'lar PU'dan ÖNCE)
once("    # ---------------- PU (40 kg/m³ enjeksiyon)", '''    # ---------------- v7 · FIRIN ALTI ISI KALKANI: PU 60 YOK → hava boşluğu (rapor seçenek b) ----------------
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
''')
blok_sil('    pu("isi_kalkani_pu_60", (X_F[0], X_F[1], Y_TAVAN, H_B - 1.5, ZP0, ZP1),', '"fırın altında toplam 120: kalkan 60 + tavan 60')
satir('    pu("yan_pu_sol", (1.5, 29.0, Y_PLINT + 1.5, H_B - 1.5, ZP0, ZP1))',
      '''    pu("yan_pu_sol", (1.5, X_IC0S, Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_CER0))          # v7: 60 (v6 27,5) — çerçeve sacının arkası
    pu("yan_pu_sol_on", (1.5, 29.0, Y_PLINT + 1.5, H_B - 1.5, Z_CER0, ZP1))              # önde fitil bandı (x 48–69) boş kalır''')
degis('"yan 27,5 · tavan 57,5 (fırın altı 117,5) · arka 37,5 · taban 39 · bölme 33"',
      '"yan 60 (v7) · tavan 57,5 (fırın altı 59 + hava boşluğu) · arka 37,5 · taban 39 · bölme 33"')
satir('    pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))',
      '    pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)')
satir('    pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))',
      '    pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)')

# ================================================================ 5 · 6 roll-bond + 7 fan → 2 bölge lamelli evaporatör
blok_sil("    # ---------------- EVAPORATÖR (roll-bond, arka duvarda) + FAN (ebm-papst 4414 FNH)", '    ekle("fan_K4", kut(K4X + 255.0')
once("    # ---------------- K4 (2027,5–2500): SICAK bölme", '''    # ---------------- v7 · SOĞUTMA STANDART DÜZEN (_local/sogutma_hesabi_v1) — 2 bölge ----------------
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
''')

# ================================================================ 6 · Secop NLE8.8CN (297 yüksek) · K4 kapak metni
degis("    CU = (350.0, 272.0, 450.0)", "    CU = (350.0, 297.0, 450.0)                                                 # v7: NLE8.8CN 297 yüksek (föy) · taban 350 × 450 VARSAYIM")
satir('         bom=("Yoğuşturucu ünite Secop CU KLF4.0CND R290", 1, "314H6008 · 335 W @ −10/25 °C · 1/6 HP · 15,2 kg",',
      '         bom=("Yoğuşturucu ünite Secop CU NLE8.8CN R290", 1, "737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C (secop.com föyü) · gereken 552–661 W @ 32 °C",')
satir('              "272 × 350 × 450 · secop.com datasheet · v6: 6 evaporatör (v5: 4) → soğutma yükü hesabı AÇIK [VARSAYIM]"))',
      '              "yükseklik 297 (föy) · taban 350 × 450 VARSAYIM (föyden teyit) · v7: KLF4.0CND 32 °C\'de 309 W yetmiyordu; hamur ılık gelir (Kemal) · sogutma_hesabi_v1"))')
degis('"hava önden girer, tabandan plinte çıkar"', '"hava önden (ızgara) girer, tabandan atış kanalıyla plint önündeki ızgaradan çıkar (v7)"')
degis("# v6: arka ucu K4 evaporatör/fanının önünde (−758)", "# v7: arkasında 32 hava geçişi (depo sağ bölgeden B4 geçişleriyle soğur)")

# ================================================================ 7 · denetim
degis('    print("CEKMECELI DOLAP v6 · tek parca', '    print("CEKMECELI DOLAP v7 (sogutma standart duzen) · tek parca')
degis('if not p["ad"].startswith(("ayak_", "plint_on")))', 'if not p["ad"].startswith(("ayak_", "plint_on", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))')
blok_sil('    # ---- ISI KALKANI ----', '    assert abs(ik.xmin - X_F[0]) < 0.05 and abs(ik.xmax - X_F[1]) < 0.05 and abs(ik.ymin - Y_TAVAN) < 0.05')
once('    # ---- SOĞUTMA (bilgi · VARSAYIM) · iletimle ısı kazancı kaba tahmini ----', '''    # ---- v7 · FIRIN ALTI ISI KALKANI: PU yok, hava boşluğu (katılardan) ----
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
          % (cu_.ymax, yb("k4_ara_sac_alt").ymin, yb("k4_ara_sac_ust").ymax, at_.xmin, at_.xmax, at_.ymin, at_.ymax, at_.zmin, at_.zmax, K4X + 60.0, K4X + K4W - 60.0, len(PLINT_IZGARA)))''')
degis("    xa, xk, xf = (K4X - X_IC0) / 1000.0,", "    xa, xk, xf = (K4X - X_IC0S - 1.0) / 1000.0,")
degis('("tavan firin alti", xf * Lz, 0.1175, T_fir)', '("tavan firin alti (hava boslugu altinda)", xf * Lz, 0.059, T_fir)')
degis('("sol yan", ha * Lz, 0.0275, T_ort)', '("sol yan", ha * Lz, 0.060, T_ort)')
blok_sil('    ev = sum(BB[p["ad"]].xlen * BB[p["ad"]].ylen for p in PARCALAR if p["ad"].startswith("evaporator_")) / 1e6',
         '          % (len([p for p in PARCALAR if p["ad"].startswith("evaporator_")]), ev, len([p for p in PARCALAR if p["ad"].startswith("fan_K")]), Q, k_pu, T_ort, T_fir))')
once("    di = 14 + 16 * len([p for p in PARCALAR if p[\"ad\"].startswith(\"plc_SM1221\")])", '''    import re as _re
    lam = [p for p in PARCALAR if _re.match(r"^evaporator_(sol|sag)_lamel$", p["ad"])]; fan = [p for p in PARCALAR if _re.match(r"^fan_(sol|sag)_\\d$", p["ad"])]
    ev = sum(BB[p["ad"]].xlen * BB[p["ad"]].ylen for p in lam) / 1e6
    print("SOGUTMA v7: %d bolge · lamelli evaporator on yuzu %.3f m² · %d fan ebm-papst 4414 FL (%.1f W) · Secop CU NLE8.8CN 737 / 688 / 586 W @ −10 °C (25 / 32 / 43 °C) · gereken 552–661 W @ 32 °C (sogutma_hesabi_v1) · duvar iletimi ~%.0f W (PU k %.3f, ortam %.0f, firin alti %.0f °C VARSAYIM)"
          % (len(lam), ev, len(fan), 1.2 * len(fan), Q, k_pu, T_ort, T_fir))
    assert len(lam) == 2 and len(fan) == 4 and not [p for p in PARCALAR if p["ad"].startswith(("fan_K", "evaporator_K"))]''')

# ================================================================ 8 · BOM gruplama
degis('''    (r"^evaporator_K[2-6]$", "roll-bond evaporatör"), (r"^fan_K[2-6]$", "ebm-papst 4414 FNH"),''',
      '''    (r"^evaporator_sag_lamel$", "Evaporatör lamelli"), (r"^evaporator_(sol|sag)_(yan_sac|dirsek)_[ab]$", "Evaporatör lamelli"),
    (r"^evaporator_(sol_askisi_2|sag_askisi_[12])$", "Evaporatör askısı"), (r"^damlama_teknesi_sag$", "Damlama teknesi"), (r"^fan_davlumbazi_sag$", "Fan davlumbazı"),
    (r"^fan_(sol_2|sag_[12])$", "ebm-papst 4414 FL"), (r"^gider_borusu_sag$", "Gider borusu"), (r"^isi_kalkani_takozu_[1-9]$", "Isı köprüsü kesici takoz"),
    (r"^isi_kalkani_sag_sac$", "Isı kalkanı yan sacı (× 2)"),''')
degis('"Secop CU KLF4.0CND"), (r"^plc_SM1221', '"Secop CU NLE8.8CN"), (r"^plc_SM1221')
degis("(r\"^(yan_pu_sol|arka_pu_37", "(r\"^(yan_pu_sol|yan_pu_sol_on|arka_pu_37")
degis('bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v9"))', 'bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v10"))')

assert "isi_kalkani_pu_60" not in s and "evaporator_%s\" % kol" not in s and "KLF4.0CND R290\", 1" not in s
io.open(os.path.join(U, "store_cad_v7.py"), "w", encoding="utf-8").write(s)
print("store_cad_v7.py yazildi · %d satir" % s.count(NL))
