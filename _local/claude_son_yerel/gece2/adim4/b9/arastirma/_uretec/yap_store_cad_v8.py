# -*- coding: utf-8 -*-
"""store_cad_v7.py -> store_cad_v8.py (27/28 Eyl 2026 gece) · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63.md §2.1 · keşif on_duzlem_v63/kesif_B.md)
Kemal: "fırının ön yüzü sınır yüzey, her şeyi o yüzeye getireceğiz, her istasyona ön yüzey ekle aynı çekmecedeki gibi … arka kısımlar sabit …
       önden tertemiz düz yüzeyler … içeride havada kalan parça olmasın … her istasyon kendi başına temiz bir kutu"
  1 · ön katmanlar +79: Z_ON −40/0 → +39/+79 · Z_CON +24/+39 · Z_CER +23/+24 (430 ferritik) · FITIL/KANAL mutlak z +79 · cevre_supur düzlemi Z_ON0
  2 · kabuk: dış sacların ön kenarı +39 (tavan dahil) · ön dönüşler +37,5…+39 · ZP1 +37,5 · arka −830 SABİT (Z_ARKA_DIS, pafta DZ'sinden bağımsız)
  3 · çekmece seçenek (a): kutu öne 79 uzar (Z_TUB0 sabit) · tepsi/içerik kutunun ÖNÜNE göre · raylar Z_CER0 ile kayar · avara −73 SABİT (strok 628)
      · avara kolu 3 mm + ön flanş (−81…+23), avara tek flanşlı · adaptör lamı iç ray boyuyla sınırlı · sensör lamı önde kola, arkada L tırnakla duvara
  4 · K4 = keşif B §6.5 Öneri 1: Secop 180° (kondenser arkada, 4 titreşim pedi), arka plenum + 2 emiş şeridi, kondenser perdesi, taban emiş delikleri,
      plintte emiş ızgarası, atış K4 kapağı ızgarasından · tava K4 önünde altta · gider boruları taban PU'su içinden U-sifon + çek valf · atış kanalı SİLİNDİ
  5 · şerit: dönüş 18 → 40, önler +39…+79, kova/kızak/klape ön düzleme göre · klape menteşe yaprağı pime değer
  6 · plint onyuz_plint +17,5…+19 + yan dönüşler (x 30 / 3970) · GN'ler oturur · damlama teknesi braketleri · ışınım sacına 3. takoz sırası
  7 · denetim: ön düzlem (her ön +39…+79, +79'u geçen yok, arka −830), arka sıra ≥ Z_ON1 + 5, kova/klape/tava yolları, ka_z, ray bağı min(lam, iç ray) − 5,
      emiş/atış alanları, dolabın altı boş, HAVADA PARÇA (denetim_temas_v1, beyaz liste: bilyeli ray ara elemanı) · BOM 1_STORE_v11
Kayıtlı ölçüler DEĞİŞMEZ: çekmece iç ölçüleri, kapasite 160/432/144/12, strok 628, ürün kotları, kova 165 × 300 × 400, klape açıklığı, K4 ara katman kotu.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v7.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140])
    s = s.replace(a, b)


def satir(icerir, yeni, n=1):
    """icerir'i tasiyan satirin TAMAMINI yeni ile degistirir"""
    global s
    L = s.split(NL)
    i_ = [i for i, l in enumerate(L) if icerir in l]
    assert len(i_) == n, (len(i_), icerir[:140])
    for i in reversed(i_):
        L[i:i + 1] = yeni.split(NL)
    s = NL.join(L)


def blok_sil(bas, son):
    """bas'i tasiyan satirdan son'u tasiyan satira kadar (dahil) siler"""
    global s
    L = s.split(NL)
    i = [k for k, l in enumerate(L) if bas in l]; assert len(i) == 1, (len(i), bas)
    j = [k for k, l in enumerate(L) if son in l and k >= i[0]]; assert j, son
    del L[i[0]:j[0] + 1]
    s = NL.join(L)


def once(icerir, ek):
    global s
    L = s.split(NL)
    i = [k for k, l in enumerate(L) if icerir in l]; assert len(i) == 1, (len(i), icerir)
    L[i[0]:i[0]] = ek.split(NL)
    s = NL.join(L)


# ================================================================ 0 · başlık
degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v7 (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v8 (28 Eyl 2026 gece) · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §2.1 · Kemal: "fırının ön yüzü' + NL +
      '    sınır yüzey, her şeyi o yüzeye getireceğiz … önden tertemiz düz yüzeyler … içeride havada kalan parça olmasın")' + NL +
      'v8: bütün önler +39…+79 (fırın ön yüzü düzlemi), arka −830 SABİT → derinlik 909 · çerçeve +23…+24 (430 ferritik) · kabuk ön kenarı +39 · seçenek (a):' + NL +
      '    kutu öne 79 uzar, tepsi kutunun önüne göre, avara −73 sabit → strok 628 · avara kolu 3 mm flanşlı · K4 keşif B §6.5 Öneri 1 (Secop 180°, emiş plintten' + NL +
      '    → taban → arka plenum, atış K4 kapağı ızgarasından, tava K4 önünde, gider PU içinde U-sifon) · dolabın altında ayak + plint dışında parça YOK ·' + NL +
      '    plint onyuz_plint +17,5…+19 + yan dönüşler · şerit dönüşü 40 · havada parça 0 (beyaz liste: bilyeli ray ara elemanı). Önceki: store_cad_v7.py' + NL +
      '    (yap_store_cad_v8.py) · BOM 1_STORE_v11' + NL +
      'v7 (27 Eyl 2026 gece) · SOĞUTMA STANDART DÜZEN')
satir("KOORDİNAT: hat ile aynı",
      "KOORDİNAT: hat ile aynı — x 0..4000 (dolap), y 0..788 (düz çizgi) · v8: z +79 = ÖN DÜZLEM (bütün önlerin dış yüzü = fırın ön yüzü), z 0 = v7 ön yüzü" + NL +
      "           (iç düzen, kutu arkası, motor, evaporatör bu referansta DEĞİŞMEDİ), −830 arka dış yüz (Z_ARKA_DIS) → derinlik 909.")

# ================================================================ 1 · derinlik / ön düzlem sabitleri
satir('H_B, W_B, DZ = 788.0, 4000.0, _g["DZ"]',
      'H_B, W_B = 788.0, 4000.0                       # v6: DÜZ ÇİZGİ 788 · dolap 0–4000 (pafta v7\'deki H_B 1060 / W_B 2500 eski hattın)' + NL +
      'Z_ARKA_DIS = -830.0                             # v8: arka dış yüz SABİT (SPEC_on_duzlem_v63 §1) — pafta DZ\'sinden BAĞIMSIZ (pafta 909 olsa da B\'nin arkası kaymaz)' + NL +
      'DZ = -Z_ARKA_DIS                                # 830: kabuk kodunda arka yüz −DZ (DERİNLİK DEĞİL — derinlik DERINLIK = 909)')
satir("FIRIN_CIKINTI = 79.0",
      "FIRIN_CIKINTI = 79.0                            # firin_tp10_cad ZS: fırın gövdesinin ön yüzü (y ≥ 788) — v8: B'nin ön düzlemi de bu" + NL +
      "Z_ON = FIRIN_CIKINTI                            # v8 · ÖN DÜZLEM +79: bütün ön panellerin / kapakların dış yüzü (montaj sözleşmesi: SC.Z_ON1 = FT.ZS)" + NL +
      "ON_UZAMA = Z_ON                                 # v8: v7'de ön yüz z 0'daydı → her ön katman +79 (iç düzen yerinde)" + NL +
      "DERINLIK = Z_ON - Z_ARKA_DIS                    # 909")
degis('''Z_ON0, Z_ON1 = -40.0, 0.0
Z_CON0, Z_CON1 = -55.0, -40.0
Z_CER0, Z_CER1 = -56.0, -55.0''',
      '''Z_ON0, Z_ON1 = Z_ON - 40.0, Z_ON                # v8: +39 … +79 (v7 −40 … 0) · 40 = dış 304 1,5 + PU 37,5 + iç 304 1,0
Z_CON0, Z_CON1 = Z_ON0 - 15.0, Z_ON0            # v8: +24 … +39 · fitil bandı (geçmeli manyetik profil)
Z_CER0, Z_CER1 = Z_CON0 - 1.0, Z_CON0           # v8: +23 … +24 · ön çerçeve sacı 1,0 — 430 FERRİTİK (manyetik fitil 304'e tutmaz)
ZP1_ON = Z_ON0 - 1.5                            # v8: +37,5 · ön dönüşlerin arka yüzü = PU'nun önü (v7 −41,5)''')
satir("KANAL = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]",
      "KANAL = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]     # kapak iç sacındaki geçme kanalı 6,4 × 8,4" + NL +
      "FITIL = [(u_, z_ + ON_UZAMA) for u_, z_ in FITIL]; KANAL = [(u_, z_ + ON_UZAMA) for u_, z_ in KANAL]   # v8: mutlak z listeleri +79 (fitil +24…+47,3)")

# ================================================================ 2 · şerit sabitleri
satir("KOVA = (3822.5, 3987.5, 126.0, 426.0, -420.0, -20.0)",
      "SERIT_DONUS = 40.0                                       # v8: 18 → 40 · şerit önleri de +39…+79 tava (sol uçla simetri; sağ yan dış sac +39'da biter)" + NL +
      "KOVA = (3822.5, 3987.5, 126.0, 426.0, Z_ON - SERIT_DONUS - 2.0 - 400.0, Z_ON - SERIT_DONUS - 2.0)   # v8: z −363…+37 (önü servis kapağının 2 arkası) · 165 × 300 × 400 ≈ 15 L (ölçü v7 ile aynı)")
satir("SERIT_DONUS = 18.0", "# v8: SERIT_DONUS yukarıda (KOVA'dan önce) tanımlı — 40")
satir("KLAPE_EKSEN = (748.0, -7.0)",
      "KLAPE_EKSEN = (748.0, Z_ON - 7.0)                         # v8: +72 · yaylı menteşe ekseni (y, z) — klape levhasının 4 arkası (SPEC \"klape y ~745\")")
satir("TAKOZ_XZ = [(x_, z_) for x_ in (2700.0, 3000.0, 3350.0, 3650.0)",
      "TAKOZ_XZ = [(x_, z_) for x_ in (2700.0, 3000.0, 3350.0, 3650.0) for z_ in (-700.0, -250.0, 10.0)]   # v8: ışınım sacı +35,5'e uzadı → önde 3. sıra (konsol 25)")

# ================================================================ 3 · K4 sıcak bölme sabitleri (atış kanalı / plint gideri KALKTI)
blok_sil("DR_Z, DR_R, DR_Y = -700.0, 6.0, 75.0", "PLINT_IZGARA = [(2095.0")
once("ARKA_YARIK = [(2540.0", '''# v8 · K4 SICAK BÖLME = keşif B §6.5 ÖNERİ 1 (SPEC §2.1): Secop 180° döner (kondenser ARKADA), arka plenum + iki yan emiş şeridinden emer
#      (taban delikleri ← plint boşluğu ← plint emiş ızgarası), önden K4 soğutma kapağının ızgarasından atar · tava K4 önünde, tabanda · gider boruları
#      taban PU'su İÇİNDEN (U-sifon + ördek gagası çek valf) → dolabın altında ayak + plint dışında HİÇBİR şey yok (v7: atış kanalı + tava + borular plintteydi)
DR_Z, DR_R = -700.0, 6.0                      # gider borusu Ø12: evaporatör teknesinin altından (x, −700) taban PU'suna iner
DR_Y, DR_ZON = 144.0, -60.0                   # borunun PU içindeki ekseni (taban PU 124,5–163,5 ortası) · öne dönüş z (K4 ön bölgesi, tava üstü)
DR_Y_CIK = 186.0                              # bölme PU'sunda yükselip K4'e bu kotta girer (tava ağzı 164,5'in üstü) → U-SİFON (su tutar: sıcak hava / koku kapanı)
DR_X_YUK = {"sol": 2010.0, "sag": 2517.0}     # yükselme x: B3 bölmesi (1993,5–2026,5) · B4 bölmesi (2501–2534) PU'sunun içi
DR_X_UC = {"sol": 2045.0, "sag": 2482.0}      # K4'te çıkış: dirsek aşağı · ucunda ördek gagası çek valf
VALF = (7.0, 10.0)                            # Minivalve DU 120.001 flanşlı ördek gagası (Ø12) + tutucu: zarf Ø14 × 10 [ölçü VARSAYIM · katalogdan teyit]
TAVA = (2031.0, 2496.0, 124.5, 164.5, -100.0, 15.0)   # buharlaştırma tavası (keşif B §6.5): K4 önünde tabanda · kapak açılınca öne çekilir
SECOP_Z = (-554.0, -104.0)                    # Secop CU NLE8.8CN taban 450 boyu (VARSAYIM) · kondenser ARKADA (−554…−494) · kompresör önde
SECOP_X = ((K4X + K4_SAG) / 2.0 - 175.0, (K4X + K4_SAG) / 2.0 + 175.0)   # 2088,75–2438,75 (ortada · iki yanda 59,75'lik emiş şeridi)
PERDE_Z = -655.0                              # pano ↔ emiş plenumu perdesi (arka yüzü) · pano en önü −667 (güç kaynağı) → 12 pay · plenum 101
TAKOZ_H = 4.0                                 # Secop tabanı ↔ K4 taban sacı titreşim pedi (v7'deki 4 mm boşluk; ara katman kotu 433,5 değişmez)
EMIS_DELIK = [(K4X + 4.5, K4_SAG - 4.0, PERDE_Z + 5.0, SECOP_Z[0] - 4.0),                      # plenum altı 464 × 92
              (K4X + 4.5, SECOP_X[0] - 5.75, SECOP_Z[0] + 4.0, SECOP_Z[1] - 6.0),               # sol şerit 51 × 440
              (SECOP_X[1] + 5.75, K4_SAG - 4.5, SECOP_Z[0] + 4.0, SECOP_Z[1] - 6.0)]            # sağ şerit (x0, x1, z0, z1)
PLINT_IZGARA = [(1905.0 + 250.0 * c_, 2148.0 + 250.0 * c_, 21.0 + 13.0 * r_, 31.0 + 13.0 * r_) for c_ in range(3) for r_ in range(7)]   # v8: K4 EMİŞİ 3 × 7 yarık 243 × 10
KOL_T = 3.0                                   # v8: avara kolu 3 mm (v7 modelde 2,5 / BOM 3) — avara iç flanşı kalktı, yer açıldı
KOL_FL = 12.0                                 # v8: avara kolu üst flanşı (L kesit) · kolun üst kenarında, +x yönünde (avara / mıknatıs yolunun üstü)
LAM_H = 6.0                                   # v8: sensör lamı dik kolu (L 6,35 × 8 × 2) — 700 açıklıkta düz lamın sehimi ~3,8 → ~0,2 mm''')

# ---- gider yolu fonksiyonu (modül düzeyi)
once("def profil(k, eks, t=2.0):", '''def gider_yollari():
    """v8 · evaporatör teknesi → Ø12 PVC: iner (taban PU'suna) → öne (z −60) → yana → bölme PU'sunda yükselir (U-sifon) → K4'e girer → aşağı → çek valf.
    Döner {yan: [(kutu, katı), ...]} segment segment: sac / PU yalnız kestiği segmentle kesilir → boru köpük içinde, temas yüzeyi tam"""
    r = DR_R; out = {}
    yv = TAVA[3] + 1.5 + VALF[1]                                              # borunun ucu = valfin üstü (176)
    for yan, e in EVAP.items():
        gx = e["gider"][0]; ty = e["y"][0] - 15.0                             # tekne altı
        xy, xu = DR_X_YUK[yan], DR_X_UC[yan]
        S = [((gx - r, gx + r, DR_Y - r, ty, DR_Z - r, DR_Z + r), sily(gx, DR_Z, r, DR_Y - r, ty))]
        S.append(((gx - r, gx + r, DR_Y - r, DR_Y + r, DR_Z - r, DR_ZON + r), silz(gx, DR_Y, r, DR_Z - r, DR_ZON + r)))
        a_, b_ = min(gx, xy) - r, max(gx, xy) + r
        S.append(((a_, b_, DR_Y - r, DR_Y + r, DR_ZON - r, DR_ZON + r), silx(DR_Y, DR_ZON, r, a_, b_)))
        S.append(((xy - r, xy + r, DR_Y - r, DR_Y_CIK + r, DR_ZON - r, DR_ZON + r), sily(xy, DR_ZON, r, DR_Y - r, DR_Y_CIK + r)))
        a_, b_ = min(xy, xu) - r, max(xy, xu) + r
        S.append(((a_, b_, DR_Y_CIK - r, DR_Y_CIK + r, DR_ZON - r, DR_ZON + r), silx(DR_Y_CIK, DR_ZON, r, a_, b_)))
        S.append(((xu - r, xu + r, yv, DR_Y_CIK + r, DR_ZON - r, DR_ZON + r), sily(xu, DR_ZON, r, yv, DR_Y_CIK + r)))
        out[yan] = S
    return out

''')

# ================================================================ 4 · fitil süpürme düzlemi
degis('yol = cq.Workplane("XY", origin=(0, 0, -40.0))', 'yol = cq.Workplane("XY", origin=(0, 0, Z_ON0))')          # v8: kapak iç yüzü düzlemi (v7 −40)

# ================================================================ 5 · çekmece (seçenek a)
degis("TUB_D = TUB[tip]; Z_TUB1 = Z_CON0 - 2.0; Z_TUB0 = Z_TUB1 - TUB_D      # v2:",
      "TUB_D = TUB[tip] + ON_UZAMA; Z_TUB1 = Z_CON0 - 2.0; Z_TUB0 = Z_TUB1 - TUB_D      # v8 seçenek (a): kutu öne 79 uzar, arkası (Z_TUB0) v7 ile aynı · v2:")
blok_sil('    for ad_, a_, b_ in (("sol", ka, ka + 15.0), ("sag", kb - 15.0, kb)):', 'bom=("Ön bağlantı köşesi", 2,')
once("    # ray adaptör lamları:", '''    # v8: 2 mm U büküm (v7 katı blok) — flanşlarla kutu önüne ve kapak iç sacına
    for ad_, a_, b_, w0_ in (("sol", ka, ka + 15.0, ka), ("sag", kb - 15.0, kb, kb - 2.0)):
        ub = (kut(w0_, w0_ + 2.0, yo + 12.0, kd - 4.0, Z_TUB1, Z_ON0).union(kut(a_, b_, yo + 12.0, kd - 4.0, Z_TUB1, Z_TUB1 + 2.0))
              .union(kut(a_, b_, yo + 12.0, kd - 4.0, Z_ON0 - 2.0, Z_ON0)))
        ekle(kod + "_on_baglanti_" + ad_, ub, "celik", kod, grup=G,
             bom=("Ön bağlantı köşesi · U 2 mm", 2, "304 2 mm büküm · kutu önüne punta, kapak iç sacına 2 × M5 perçin somun", "ön yüz ayar yuvalı · %.0f derin" % (Z_ON0 - Z_TUB1)) if ad_ == "sol" else None)
    LZ0, LZ1 = max(Z_TUB0, Z_CER0 - RAY_L + 2 * RAY_KISA), min(Z_TUB1, Z_CER0 - 2 * RAY_KISA)   # v8: lam = kutu ∩ iç ray (660'lık kutu 739 > iç ray 692 → kutu arkada konsol)''')
degis('ekle(kod + "_ray_adaptor_" + ad_, kut(a_, b_, yo + RAY_Y0, yo + RAY_Y0 + 6.0, Z_TUB0, Z_TUB1)',
      'ekle(kod + "_ray_adaptor_" + ad_, kut(a_, b_, yo + RAY_Y0, yo + RAY_Y0 + 6.0, LZ0, LZ1)')
degis('"ray iç profiline 4 × M4")', '"ray iç profiline 4 × M4 · v8: iç ray boyuyla sınırlı (660\'lık kutuda kutu arkada konsol)")')
satir("    pul_a = pul.cut(silx(ky, 0.0, 2.5, fl0 - 1, fl1 + 1))",
      '''    pul_a = (silx(ky, 0.0, KAS_OD / 2.0, fl0 + 1.5, fl1 - 1.5).union(silx(ky, 0.0, KAS_FL / 2.0, fl1 - 1.5, fl1))
             .cut(silx(ky, 0.0, 2.5, fl0 - 1, fl1 + 1)))                   # v8: avara TEK flanşlı (dış) — iç flanşın yeri 3 mm avara koluna · Ø5 mil''')
degis('bom=("GT3 avara 30 diş · 6 mm · çift rulman", 1, "alüminyum · 2 × 625-2RS", "ön çerçevenin 17 mm arkası")',
      'bom=("GT3 avara 30 diş · 6 mm · tek flanşlı (dış) · çift rulman", 1, "alüminyum · 2 × 625-2RS · v8: iç flanş yok (Gates: iki kasnaklı tahrikte motor kasnağı çift flanşlı → kayış kılavuzu yeter)", "z −73 SABİT (strok 628)")')
degis("silx(ky, Z_AVARA, 2.5, x0 + RAY_T + 2.6, fl1 + 1.0)", "silx(ky, Z_AVARA, 2.5, x0 + RAY_T + 0.1 + KOL_T, fl1 + 1.0)")
blok_sil('    ekle(kod + "_avara_kolu", kut(x0 + RAY_T + 0.1', 'bom=("Avara kolu 3 mm", 1,')
once("    # kayış (üst ve alt koşu, yan bantta)", '''    # v8: avara kolu 3 mm + ön flanş (104 boy: avara −73'te SABİT, çerçeve +23'e geldi) · flanş çerçeve sacının arkasına 2 × M4 perçin somun
    kl0 = x0 + RAY_T + 0.1                                               # iç ray gövdesine 0,1 · avara dişli gövdesine 1,2
    kol = kut(kl0, kl0 + KOL_T, ky - 8.0, y1 + 12.0, Z_AVARA - 8.0, Z_CER0).union(kut(x0 + 1.0, kl0, y1 + 1.0, y1 + 12.0, Z_CER0 - 3.0, Z_CER0))
    kol = kol.union(kut(kl0, kl0 + KOL_FL, y1 + 12.0 - KOL_T, y1 + 12.0, Z_AVARA - 8.0, Z_CER0))   # v8: üst flanş 12 × 3 → L kesit (eksantrik kayış çekişine karşı, denetimde hesap)
    ekle(kod + "_avara_kolu", kol, "celik", kod,
         bom=("Avara kolu 3 mm · L kesit + ön flanş", 1, "304 büküm · gövde 3 + üst flanş 12 × 3 · ön flanş çerçeve sacının arkasına 2 × M4 perçin somun (fitil altında) · v8: 104 boy (−81…+23)", "kayış gergisi burada: 8 mm yuvalı"))''')
satir('    ekle(kod + "_sensor_lami", kut(',
      '''    # v8: lam ÖNDE avara kolunun arka yüzüne değer (−81), ARKADA 2 mm L tırnakla arka iç saca oturur (v7: iki ucu da havadaydı);
    #     yatay kablo kanalına denk gelen lam (K2 üst) kanalın önünde kademeyle kanalın altına iner
    lx0, lx1 = x0 + SEN_X[0] - SEN[2] - 0.6, x0 + SEN_X[0] - 0.6
    ly0, ly1 = my0 + SEN[1], my0 + SEN[1] + 2.0
    lz1, ZT_ = Z_AVARA - 8.0, Z_ARKA + 2.0
    kny = [ku for (xa_, xb_), ku in (((K1X + KAN_X[1], K4X + KAN_X[1]), KAN_UST), ((K4X + KAN_X[1], KOLON_X["K6"] + KAN_X[1]), KAN_UST_F))
           if xa_ < lx1 and lx0 < xb_ and ku[0] < ly1 + 1.0 and ly0 - 1.0 < ku[1]]
    if not kny:
        lam = kut(lx0, lx1, ly0, ly1, ZT_, lz1).union(kut(lx0, lx1, ly1 - 24.0, ly1, Z_ARKA, ZT_)).union(kut(lx0, lx0 + 2.0, ly1, ly1 + LAM_H, ZT_, lz1))
    else:
        yk, zk = kny[0][0] - 4.0, KAN_Z[1] + 2.0                        # kanalın 4 altı · kanalın 2 önü (−763)
        lam = (kut(lx0, lx1, ly0, ly1, zk, lz1).union(kut(lx0, lx1, yk, ly1, zk - 2.0, zk)).union(kut(lx0, lx1, yk, yk + 2.0, ZT_, zk - 2.0))
               .union(kut(lx0, lx1, yk - 22.0, yk + 2.0, Z_ARKA, ZT_)).union(kut(lx0, lx0 + 2.0, ly1, ly1 + LAM_H, zk, lz1)))
    ekle(kod + "_sensor_lami", lam, "celik", kod,
         bom=("Sensör lamı L 6,35 × 8 × 2 + arka tırnak", 1, "304 büküm · reed sensörler altında · önde avara koluna, arkada arka iç saca 2 × M4",
              "kanala denk gelen lam kanalın altından kademeyle geçer" if kny else ""))''')
degis('tz0, tz1 = Z_TUB0 + 5.0, Z_TUB0 + 5.0 + t["td"]',
      'tz1 = Z_TUB1 - 5.0; tz0 = tz1 - t["td"]                          # v8 seçenek (a): tepsi kutunun ÖNÜNE göre (arkada 84 boş) → açıkta arka sıra 79 daha dışarıda')
degis("kut(a - 6.0, a + 6.0, y0 + 2.0, y0 + 8.0, iz0, zb - 12.0)", "kut(a - 6.0, a + 6.0, y0, y0 + 6.0, iz0, zb - 12.0)")

# ================================================================ 6 · kasa · yardımcılar
satir("    ZP0, ZP1 = -DZ + 1.5, -41.5",
      "    ZP0, ZP1 = -DZ + 1.5, ZP1_ON                  # v8: PU derinliği arka dış sacın önü … ön dönüşün arkası (+37,5; v7 −41,5)")
once("    CER, SACK, PUK = [], [], []",
     "    GID = gider_yollari(); GID_L = [g_ for y_ in GID for g_ in GID[y_]]   # v8: gider borusu segmentleri (sac / PU bunlarla kesilir)")
degis("        if ek is not None:\n            w = w.cut(ek)\n        SACK.append(k)",
      "        for c_, s_ in GID_L:\n            if kes_mi(k, c_):\n                w = w.cut(s_)                       # v8: gider borusu sacdan geçer\n"
      "        if ek is not None:\n            w = w.cut(ek)\n        SACK.append(k)")
degis("        if ek is not None:\n            w = w.cut(ek)\n        PUK.append(k)",
      "        for c_, s_ in GID_L:\n            if kes_mi(k, c_):\n                w = w.cut(s_)                       # v8: gider borusu köpüğün İÇİNDE\n"
      "        if ek is not None:\n            w = w.cut(ek)\n        PUK.append(k)")

# ---- plint
blok_sil("    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0)", '    ekle("plint_on_1.5", pl_,')
once("    for i, (ax, az) in enumerate(AYAK_XZ):", '''    PZ = (Z_ON - 61.5, Z_ON - 60.0)                                      # v8: +17,5 … +19 — ön düzlemin 60 gerisinde, bütün hat boyunca tek çizgi (SPEC §1)
    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1])
    for a_, b_, c_, d_ in PLINT_IZGARA:                                  # v8: K4 Secop EMİŞİ (v7: kondenser atışıydı)
        pl_ = pl_.cut(kut(a_, b_, c_, d_, PZ[0] - 1.0, PZ[1] + 1.0))
    ekle("onyuz_plint", pl_, "sac", B, bom=("Plint 1,5 (ön)", 1, "304 fırçalı 1,5 · z +17,5…+19 (ön düzlemin 60 gerisi) · x 30–3970 · K4 önünde emiş ızgarası %d yarık %.0f cm²"
                                             % (len(PLINT_IZGARA), sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in PLINT_IZGARA) / 100.0), "dolabın altında ayak + plint dışında parça yok"))
    for ad_, x_ in (("sol", X_IC0), ("sag", X_IC1 - 1.5)):              # v8: yan dönüşler — dolabın altı yandan da kapalı (v7 x 0–30 / 3970–4000 açıktı)
        ekle("onyuz_plint_donus_" + ad_, kut(x_, x_ + 1.5, 0.0, Y_PLINT, -DZ + 1.5, PZ[0]), "sac", B,
             bom=("Plint yan dönüşü 1,5", 2, "304 · x 30 ve 3970 · plintten arka dış sac hizasına", "%.0f boy" % (PZ[0] + DZ - 1.5)) if ad_ == "sol" else None)''')

# ---- kabuk
satir('    sac("yan_dis_sac_sol", (0.0, 1.5, Y_PLINT, H_B, -DZ, -40.0)',
      '    sac("yan_dis_sac_sol", (0.0, 1.5, Y_PLINT, H_B, -DZ, Z_ON0), bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · ön kenar kapak arkasında (z +39) · v8: iki yan simetrik (şerit dönüşü 40)", ""))')
satir('    sac("yan_dis_sac_sag", (W_B - 1.5, W_B, Y_PLINT, H_B, -DZ, -SERIT_DONUS))',
      '    sac("yan_dis_sac_sag", (W_B - 1.5, W_B, Y_PLINT, H_B, -DZ, Z_ON - SERIT_DONUS))                  # v8: +39')
satir('    sac("tavan_dis_sac", (1.5, W_B - 1.5, H_B - 1.5, H_B, -DZ, -40.0)',
      '    sac("tavan_dis_sac", (1.5, W_B - 1.5, H_B - 1.5, H_B, -DZ, Z_ON0), bom=("Tavan dış sacı", 1, "304 1,5 · A, C ve fırın bunun üstüne oturur (fırın altında taşıyıcı çerçeve) · v8: ön kenar +39 (kaide ön profili ve fırın tam basar)", ""))')
blok_sil("    DR_DELIK = None ", '    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0)')
once("    AY_ = None ", '''    EMIS = None                                                         # v8: K4 emiş delikleri (plenum + 2 şerit) · v7 VENT + gider delikleri kalktı
    for a_, b_, c_, d_ in EMIS_DELIK:
        _k = kut(a_, b_, Y_PLINT - 1.0, Y_PLINT + 3.0, c_, d_)
        EMIS = _k if EMIS is None else EMIS.union(_k)
    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, Z_ON0), ek=EMIS,
        bom=("Taban dış sacı 1,5", 1, "304 · v8: ön kenar +39 · K4 altında emiş delikleri %.0f cm² (paslanmaz elek / filtre [VARSAYIM])"
             % (sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in EMIS_DELIK) / 100.0), "plint boşluğundan Secop'a hava"))''')
satir('    sac("yan_on_donus_sol", (1.5, 30.0, Y_PLINT + 1.5, H_B - 1.5, -41.5, -40.0))',
      '    sac("yan_on_donus_sol", (1.5, 30.0, Y_PLINT + 1.5, H_B - 1.5, ZP1, Z_ON0))')
degis('sac("tavan_ic_sac", (X_IC0S, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5))', 'sac("tavan_ic_sac", (X_IC0S, X_F[0], Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, ZP1))')
degis('sac("tavan_ic_sac_F", (XF0, XB[5], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, -41.5))', 'sac("tavan_ic_sac_F", (XF0, XB[5], Y_TAVAN_F, Y_TAVAN_F + 1.0, Z_ARKA, ZP1))')
degis("TD_A, TD_F = (X_IC0, XF0, Y_TAVAN, H_B - 1.5, -41.5, -40.0), (XF0, XS - 1.0, Y_TAVAN_F, H_B - 1.5, -41.5, -40.0)",
      "TD_A, TD_F = (X_IC0, XF0, Y_TAVAN, H_B - 1.5, ZP1, Z_ON0), (XF0, XS - 1.0, Y_TAVAN_F, H_B - 1.5, ZP1, Z_ON0)")
degis('sac("taban_ic_sac", (X_IC0S, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)',
      'sac("taban_ic_sac", (X_IC0S, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, ZP1))')
degis('sac("taban_k4_kademe_saci", (K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -41.5),',
      'sac("taban_k4_kademe_saci", (K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, ZP1),')
degis('sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), ek=DR_DELIK)',
      'sac("taban_ic_sac_F", (XF0, XB[5], Y_TABAN - 1.0, Y_TABAN, Z_ARKA, ZP1))')
satir('    sac("taban_on_donus", (X_IC0, XS - 1.0, Y_PLINT + 1.5, Y_TABAN, -41.5, -40.0))',
      '    sac("taban_on_donus", (X_IC0, K4X, Y_PLINT + 1.5, Y_TABAN, ZP1, Z_ON0))                    # v8: K4 önünde YOK (tava öne çekilir, keşif B §6.5)' + NL +
      '    sac("taban_on_donus_2", (K4_SAG, XS - 1.0, Y_PLINT + 1.5, Y_TABAN, ZP1, Z_ON0))')
degis('sac("bolme_5_sac_b", (XS - 1.0, XS, Y_PLINT + 1.5, H_B - 1.5, ZP0, -40.0),', 'sac("bolme_5_sac_b", (XS - 1.0, XS, Y_PLINT + 1.5, H_B - 1.5, ZP0, Z_ON0),')
degis('pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)', 'pu("taban_pu", (29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))')
degis('pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1), ek=DR_DELIK)', 'pu("taban_pu_F", (XF0 - 1.0, XB[5] + 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, ZP0, ZP1))')

# ---- soğutma: tekne braketleri, gider (PU içinde), çek valf, tava; atış kanalı SİLİNDİ
once("        yc = (ey0 + ey1) / 2.0", '''        for j_, xb_ in enumerate((300.0, 520.0)):                          # v8: tekne arka iç saca 2 L braketle oturur (v7 yalnız boruya bağlıydı → havada)
            br = kut(cx + xb_, cx + xb_ + 20.0, ey0 - 16.5, ey0 + 10.0, Z_ARKA, Z_ARKA + 1.5).union(kut(cx + xb_, cx + xb_ + 20.0, ey0 - 16.5, ey0 - 15.0, Z_ARKA + 1.5, EV_Z[0] + 30.0))
            ekle("damlama_teknesi_%s_braketi_%d" % (yan, j_ + 1), br, "celik", "B_SOGUTMA",
                 bom=("Damlama teknesi braketi 1,5 · L", 4, "304 büküm · arka iç saca 2 × M5 perçin somun · tekne üstüne oturur", "") if ilk and j_ == 0 else None)''')
blok_sil('        gx, gxs = e["gider"]', '"uç atış kanalında buharlaştırma tavasının üstünde (serbest damlama)") if ilk else None)')
blok_sil("    ak = kut(ATIS[0], ATIS[1], ATIS[2], ATIS[2] + 1.5, ATIS[3], -61.5)", "defrost suyu (günde 4 defrost, VARSAYIM ≤ 1 L)")
once("    # ---------------- K4 (2027,5–2500): SICAK bölme", '''        gb = None
        for _k, _s in GID[yan]:
            gb = _s if gb is None else gb.union(_s)
        ekle("gider_borusu_%s" % yan, gb, "plastik", "B_SOGUTMA",
             bom=("Gider borusu Ø12 × 1", 2, "PVC · v8: teknenin dibinden taban PU'sunun İÇİNDE (köpük içi) öne ve yana, bölme PU'sunda yükselir (U-SİFON: su tutar, sıcak hava / koku kapanı), K4'e girip tavaya iner [VARSAYIM ısıtıcısız: dolap +3 °C]",
                  "dolabın altına hiçbir boru sarkmaz (v7: plintten geçiyordu)") if ilk else None)
        ekle("gider_cek_valfi_%s" % yan, sily(DR_X_UC[yan], DR_ZON, VALF[0], TAVA[3] + 1.5, TAVA[3] + 1.5 + VALF[1]), "silikon", "B_SOGUTMA",
             bom=("Ördek gagası çek valf Minivalve DU 120.001", 2, "silikon · flanşlı · boru ucunda tutucu kapakla [ölçü VARSAYIM: zarf Ø14 × 10 — minivalve.com katalog föyünden teyit]",
                  "sifon kuruyunca sıcak hava / koku geri gelmesin (keşif B §6.5)") if ilk else None)
    ekle("buharlastirma_tavasi", kut(*TAVA).cut(kut(TAVA[0] + 1.5, TAVA[1] - 1.5, TAVA[2] + 1.5, TAVA[3] + 1.0, TAVA[4] + 1.5, TAVA[5] - 1.5)),
         "sac", "B_SOGUTMA", bom=("Buharlaştırma tavası 1,5", 1, "304 · v8: K4 sıcak bölmesinin önünde, tabanda — Secop atış havasının içinde · soğutma kapağı açılınca öne çekilir",
                                  "%.0f × %.0f × %.0f · brüt %.1f L (günde 4 defrost, VARSAYIM ≤ 1 L) · gider uçları çek valfle tava ağzının 1,5 üstünde"
                                  % (TAVA[1] - TAVA[0], TAVA[3] - TAVA[2], TAVA[5] - TAVA[4], (TAVA[1] - TAVA[0] - 3.0) * (TAVA[3] - TAVA[2] - 1.5) * (TAVA[5] - TAVA[4] - 3.0) / 1e6)))
''')

# ---- K4: Secop 180° + pedler + perdeler
blok_sil("    CU = (350.0, 297.0, 450.0)", '    ekle("sogutma_grubu_kompresor",')
once("    s0 = cy0 + CU[1] + 8.0", '''    # v8 · SECOP CU NLE8.8CN 180° DÖNÜK (keşif B §6.5 Öneri 1): kondenser ARKADA (emiş plenumuna bakar), fan önünde, kompresör önde ·
    #      taban 4 titreşim pedinin üstünde (v7: 4 mm havadaydı) · fan Ø254 (föy; v7 Ø230) kondenserin ön yüzüne bağlı
    CU = (350.0, 297.0, 450.0)                                                 # NLE8.8CN 297 yüksek (föy) · taban 350 × 450 VARSAYIM
    cx0, cy0 = SECOP_X[0], Y_PLINT + 1.5 + TAKOZ_H                             # 2088,75 · 128,5 (v7 kotu → ara katman 433,5 değişmez)
    cz0, cz1 = SECOP_Z                                                         # −554 … −104
    for i_, (tx_, tz_) in enumerate([(cx0 + 25.0, cz0 + 25.0), (cx0 + CU[0] - 25.0, cz0 + 25.0), (cx0 + 25.0, cz1 - 25.0), (cx0 + CU[0] - 25.0, cz1 - 25.0)]):
        ekle("sogutma_grubu_takozu_%d" % i_, kut(tx_ - 20.0, tx_ + 20.0, Y_PLINT + 1.5, cy0, tz_ - 20.0, tz_ + 20.0), "koyu", "B_SOGUTMA",
             bom=("Titreşim pedi 40 × 40 × 4 · NBR / neopren 60 ShA", 4, "Secop tabanı ↔ K4 taban sacı · M8 cıvata geçişli [VARSAYIM · üretici seçilmedi; 4 mm = v7'deki boşluk, ara katman kotu korunur]",
                  "Secop montaj deliklerinin altında (yer föyden teyit)") if i_ == 0 else None)
    ekle("sogutma_grubu_taban", kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz0, cz1), "motor", "B_SOGUTMA",
         bom=("Yoğuşturucu ünite Secop CU NLE8.8CN R290", 1, "737 / 688 / 586 W @ −10 °C · 25 / 32 / 43 °C (secop.com föyü) · gereken 552–661 W @ 32 °C",
              "yükseklik 297 (föy) · taban 350 × 450 VARSAYIM (föyden teyit) · v8: 180° dönük — kondenser arkada (arka plenumdan emer), atış önden K4 kapağı ızgarasından"))
    ekle("sogutma_grubu_kondenser", kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + 15.0, cy0 + CU[1], cz0, cz0 + 60.0), "bakir", "B_SOGUTMA")
    ekle("sogutma_grubu_fan", silz(cx0 + CU[0] / 2.0, cy0 + 15.0 + (CU[1] - 15.0) / 2.0, 127.0, cz0 + 60.0, cz0 + 88.0), "motor", "B_SOGUTMA")   # Ø254 · kondenser yüzüne bağlı
    ekle("sogutma_grubu_kompresor", sily(cx0 + CU[0] / 2.0, cz0 + 310.0, 85.0, cy0 + 15.0, cy0 + 15.0 + 162.0), "koyu", "B_SOGUTMA")''')
degis('ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, -522.0, -521.0), "sac", "B_SOGUTMA",',
      'ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, PERDE_Z, PERDE_Z + 1.0), "sac", "B_SOGUTMA",')
degis('bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında", "yoğuşturucu havası panoya gelmez"))',
      'bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında · v8: z −655 = emiş plenumunun arka duvarı", "yoğuşturucu havası panoya gelmez"))')
once("    ZP = Z_ARKA + 2.0 ", '''    # v8 · EMİŞ / ATIŞ AYRIMI: kondenser perdesi (kondenserin ön düzleminde, çevresini kapatır) + Secop yanlarında emiş şeridi yan sacları (önleri kapalı)
    #      emiş: plint ızgarası → plint boşluğu → taban delikleri (plenum + 2 şerit) → arka plenum → kondenser → fan → kompresör üstünden öne → K4 kapağı ızgarası
    ekle("k4_kondenser_perdesi", kut(cx0, cx0 + CU[0], Y_PLINT + 1.5, s0, cz0 + 60.0, cz0 + 61.5)
         .cut(kut(cx0 + 5.0, cx0 + CU[0] - 5.0, cy0 + 15.0, cy0 + CU[1], cz0 + 59.0, cz0 + 62.5))
         .cut(kut(cx0, cx0 + CU[0], cy0, cy0 + 15.0, cz0 + 59.0, cz0 + 62.5)), "sac", "B_SOGUTMA",
         bom=("Kondenser perdesi 1,5", 1, "304 · kondenserin ön düzleminde, çevresini kapatır (emiş ↔ atış ayrımı) · üstteki 8 mm aralık da kapalı", "fan deliği = kondenser yüzü"))
    for ad_, xa_, xb_ in (("sol", cx0 - 1.5, cx0), ("sag", cx0 + CU[0], cx0 + CU[0] + 1.5)):
        ekle("k4_emis_yan_sac_" + ad_, kut(xa_, xb_, Y_PLINT + 1.5, s0, cz0 + 60.0, cz1), "sac", "B_SOGUTMA",
             bom=("Emiş şeridi yan sacı 1,5", 2, "304 · Secop'un yanında, kondenser perdesinden öne (atış tarafını emiş şeridinden ayırır)", "") if ad_ == "sol" else None)
    for ad_, xa_, xb_ in (("sol", kx0, cx0 - 1.5), ("sag", cx0 + CU[0] + 1.5, K4_SAG)):
        ekle("k4_emis_on_kapama_" + ad_, kut(xa_, xb_, Y_PLINT + 1.5, s0, cz1 - 1.5, cz1), "sac", "B_SOGUTMA",
             bom=("Emiş şeridi ön kapaması 1,5", 2, "304 · şeridin önünü kapatır (önü atış bölgesi: tava + ızgara)", "") if ad_ == "sol" else None)''')
degis("    g0 = d0 + 5.0", "    g0 = d0                                                           # v8: GN 1/1 ara sacın üstüne OTURUR (v7 5 mm havadaydı)")
degis("kut(kx0, K4_SAG, g0 + 110.0, g0 + 111.5, Z_ARKA + 32.0, Z_CER0)", "kut(kx0, K4_SAG, d0 + 115.0, d0 + 116.5, Z_ARKA + 32.0, Z_CER0)")
degis("    g1 = g0 + 116.5", "    g1 = d0 + 116.5                                                   # v8: GN 1/2 rafın ÜSTÜNE oturur (raf v7 kotunda 578,5–580)")
degis('("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False, (ON_ALT + BIND, s0 + 12.0 - BIND))',
      '("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False, (ON_ALT, s0 - 2.5))')
satir("    PENCERE = (kx0 + 20.0, kx1 - 20.0, Y_TABAN + 23.0, s0 - 8.0)",
      "    PENCERE = (K4X + 10.0, K4_SAG - 10.0, 165.0, s0 - 3.5)             # v8: ATIŞ ızgarası 452,5 × 265 (keşif B §6.5: 2037,5–2490 × 165–430)")
degis('"hava önden (ızgara) girer, tabandan atış kanalıyla plint önündeki ızgaradan çıkar (v7)"',
      '"v8: Secop ATIŞI bu ızgaradan çıkar (emiş: plint ızgarası → plint boşluğu → K4 taban delikleri → arka plenum)"')
degis("        cer = cer.cut(kut(kx0, kx1, ac[0], ac[1], Z_CER0 - 1, Z_CER1 + 1))",
      "        xa_, xb_ = (kx0, kx1) if _f else (K4X + 2.5, K4_SAG - 2.5)       # v8: soğutma açıklığı 2030–2497,5 × 126–431 (tava öne çekilir)" + NL +
      "        cer = cer.cut(kut(xa_, xb_, ac[0], ac[1], Z_CER0 - 1, Z_CER1 + 1))")
degis('"304 lazer kesim · %d açıklık · fırın altında üst kenar %.0f"',
      '"430 FERRİTİK 1,0 (manyetik fitil 304\'e tutmaz) · lazer kesim · %d açıklık · fırın altında üst kenar %.0f"')

# ---- şerit
degis("-445.0, kf_)", "ke_ - 25.0, kf_)", n=3)
degis("-446.5, -445.0))", "ke_ - 26.5, ke_ - 25.0))")
degis("w = kut(SK0, SK1, y0_, y1_, -SERIT_DONUS, 0.0).cut(kut(SK0 + 1.5, SK1 - 1.5, y0_ + 1.5, y1_ - 1.5, -SERIT_DONUS - 1.0, -1.5))",
      "w = kut(SK0, SK1, y0_, y1_, Z_ON - SERIT_DONUS, Z_ON).cut(kut(SK0 + 1.5, SK1 - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON - SERIT_DONUS - 1.0, Z_ON - 1.5))")
degis("w = w.cut(kut(delik[0], delik[1], delik[2], delik[3], -2.0, 1.0))", "w = w.cut(kut(delik[0], delik[1], delik[2], delik[3], Z_ON - 2.0, Z_ON + 1.0))")
degis("18 dönüş", "40 dönüş", n=2)
degis("KLAPE_AC[2] - 6.0, ky_ - 4.0, -3.0, -1.5)", "KLAPE_AC[2] - 6.0, ky_ - 4.0, Z_ON - 3.0, Z_ON - 1.5)")
degis('ekle("klape_mentese_yapragi", kut(KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0, ky_ + 4.0, ky_ + 22.0, -3.0, -1.5), "celik", C)',
      'ekle("klape_mentese_yapragi", kut(KLAPE_AC[0] + 5.0, KLAPE_AC[1] - 5.0, ky_, ky_ + 22.0, Z_ON - 3.0, Z_ON - 1.5), "celik", C)   # v8: yaprak pime değer (v7 1,7 mm havadaydı)')

# ================================================================ 7 · denetim
degis('print("CEKMECELI DOLAP v7 (sogutma standart duzen) · tek parca', 'print("CEKMECELI DOLAP v8 (on duzlem +79 · arka -830 · derinlik 909) · tek parca')
degis('if not p["ad"].startswith(("ayak_", "plint_on", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))',
      'if not p["ad"].startswith(("ayak_", "onyuz_plint")))')
once("    xs = sorted(KAPAK_X.values())", '''    # ---- v8 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1): her önün dış yüzü Z_ON1, arkası Z_ON0 · +79'u geçen parça YOK · arka −830 · plint 60 geride ----
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
    assert abs(plb.zmax - (Z_ON1 - 60.0)) < 0.01 and abs(plb.xmin - X_IC0) < 0.01 and abs(plb.xmax - X_IC1) < 0.01, "plint +19 / 30-3970 degil"''')
degis("    en = dict(b1=1e9, b2=1e9, bag=1e9)", "    en = dict(b1=1e9, b2=1e9, bag=1e9); kons = 0.0")
degis('            assert bag >= ad_.zlen - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / %.0f)" % (kod, yan, bag, ad_.zlen)',
      '            ic_l = zr["ic"][1] - zr["ic"][0]' + NL +
      '            assert bag >= min(ad_.zlen, ic_l) - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / min(lam %.0f, ic ray %.0f))" % (kod, yan, bag, ad_.zlen, ic_l)' + NL +
      '            kons = max(kons, ad_.zmin - BB["%s_kutu_U_1.0" % kod].zmin)')
degis('ara eleman +%.0f"\n          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK))',
      'ara eleman +%.0f · en uzun kutu arka konsolu %.0f mm (660\'lik kutu, lam ic ray boyunda)"\n          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK, kons))' + NL +
      '    assert abs(STROK - 628.0) < 0.01 and abs(Z_AVARA + 73.0) < 0.01, "strok 628 / avara -73 degil: %.1f" % STROK')
blok_sil("    for tip in TOP:", "          % (arka, FIRIN_CIKINTI, H_B, arka - FIRIN_CIKINTI))")
once("    # ---- ŞERİT · ROBOT ÇÖPÜ ----", '''    for tip in TOP:                                                     # v8: katılardan (tepsi kutunun önüne göre)
        ks_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == tip}
        kenar = min(BB[p["ad"]].zmin for p in PARCALAR if p["birim"] in ks_ and "_top_" in p["ad"]) + STROK
        print("   %s: acilinca arka sira topun arka kenari z %+.1f (on duzlem %+.0f · esik %+.0f · katilardan)" % (tip, kenar, Z_ON1, Z_ON1 + 5.0))
        assert kenar >= Z_ON1 + 5.0, "%s: acik cekmecede arka sira on duzlemin icinde" % tip
    k5_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == "hamur" and k_.startswith("CEK_K5_")}
    arka = min((BB[p["ad"]].zmin + BB[p["ad"]].zmax) / 2.0 for p in PARCALAR if p["birim"] in k5_ and "_top_" in p["ad"]) + STROK
    print("   K5 (firin alti) pide: acilinca arka sira top merkezi z %+.1f · firin on yuzu = on duzlem z %+.0f (y >= %.0f) -> dikey yaklasimda tutucu yaricapi <= %.0f mm (robot tarafi ACIK)"
          % (arka, FIRIN_CIKINTI, H_B, arka - FIRIN_CIKINTI))''')
degis('assert abs(kb.ymin - 126.0) < 0.05 and abs(kb.zmin + 420.0) < 0.05 and abs(kb.zmax + 20.0) < 0.05, "kova yeri SPEC degil"',
      'assert abs(kb.ymin - 126.0) < 0.05 and abs(kb.zmin - KOVA[4]) < 0.05 and abs(kb.zmax - (Z_ON1 - SERIT_DONUS - 2.0)) < 0.05, "kova yeri SPEC degil (v8: onu servis kapaginin 2 arkasi)"')
degis("KLAPE_AC[3], KOVA[5], 0.0).val()", "KLAPE_AC[3], KOVA[5], Z_ON1).val()")
degis("KOVA[4] - 0.5, 450.0).val()", "KOVA[4] - 0.5, Z_ON1 + 450.0).val()")
degis("kova + poset kizakta z +450'ye cekilir -> yolunda %d parca\" % (SERIT_KAPI[0], SERIT_KAPI[1], len(dolu)))",
      "kova + poset kizakta z %+.0f'ye (on duzlem + 450) cekilir -> yolunda %d parca\" % (SERIT_KAPI[0], SERIT_KAPI[1], Z_ON1 + 450.0, len(dolu)))")
degis('k_[5] < 0.0 for a, k_, e in TASIYICI if e == "x"), "kiris firin tabaninin disinda"',
      'k_[5] < FIRIN_CIKINTI for a, k_, e in TASIYICI if e == "x"), "kiris firin tabaninin disinda"')
degis("BOS = kut(X_F[0] + 1.0, BOLME_X[5], Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -41.5).val()",
      "BOS = kut(X_F[0] + 1.0, BOLME_X[5], Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, ZP1_ON).val()")
degis("ka_z = min(-57.0 - TUB[c[2]] for c in ks)", "ka_z = min(Z_CON0 - 2.0 - (TUB[c[2]] + ON_UZAMA) for c in ks)          # v8: = Z_TUB0 (kutu arkası v7 ile aynı)")
degis('· tekne alti %.1f · gider x %.0f -> tava x %.0f"', '· tekne alti %.1f · gider x %.0f -> PU icinde U-sifon -> K4 cikis x %.0f"')
degis('tk_.ymin, e["gider"][0], e["gider"][1]))', 'tk_.ymin, e["gider"][0], DR_X_UC[yan]))')
satir('        assert TAVA[0] < e["gider"][1] - DR_R and',
      '''        vl_ = yb("gider_cek_valfi_%s" % yan)
        assert TAVA[0] + 1.5 < vl_.xmin and vl_.xmax < TAVA[1] - 1.5 and TAVA[4] + 1.5 < vl_.zmin and vl_.zmax < TAVA[5] - 1.5 and vl_.ymin > TAVA[3], "gider cikisi tavanin ustunde degil"
        assert gb_.ymin >= Y_PLINT + 1.5 + 10.0 and DR_Y + DR_R <= Y_TABAN - 1.0 - 10.0, "gider borusu taban PU'sunun icinde degil"''')
blok_sil('    cu_ = yb("sogutma_grubu_kondenser"); at_ = yb("kondenser_atis_kanali")', '          % (cu_.ymax, yb("k4_ara_sac_alt").ymin')
once("    # ---- SOĞUTMA (bilgi · VARSAYIM) · iletimle ısı kazancı kaba tahmini ----", '''    # ---- v8 · K4 SICAK BÖLME (keşif B §6.5 Öneri 1): emiş / atış yolu, tava, dolabın altı (katılardan) ----
    cu_ = yb("sogutma_grubu_kondenser"); ta_ = yb("sogutma_grubu_taban"); fn_ = yb("sogutma_grubu_fan"); tv_ = yb("buharlastirma_tavasi"); pr_ = yb("k4_ara_perde")
    s0_ = yb("k4_ara_sac_alt").ymin
    emis = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in EMIS_DELIK) / 100.0
    pli = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in PLINT_IZGARA) / 100.0
    PEN = (K4X + 10.0, K4_SAG - 10.0, 165.0, s0_ - 3.5)
    atis = ((PEN[1] - PEN[0]) * (PEN[3] - PEN[2]) - sum(BB[a_].xlen * BB[a_].ylen for a_ in BB if a_.startswith("k4_izgara_"))) / 100.0
    Vh = 551.0 / 3600.0                                                  # m³/s · Secop föyü kondenser havası (keşif B)
    print("   SECOP CU NLE8.8CN (180 derece · keşif B Oneri 1): taban x %.2f-%.2f y %.1f (4 ped) · kondenser z %.0f…%.0f (arkada) · fan Ø%.0f z %.0f…%.0f · plenum %.0f (perde z %.0f) · ust aralik %.1f (kondenser perdesiyle kapali)"
          % (ta_.xmin, ta_.xmax, ta_.ymin, cu_.zmin, cu_.zmax, fn_.xlen, fn_.zmin, fn_.zmax, cu_.zmin - pr_.zmax, pr_.zmin, s0_ - cu_.ymax))
    print("   HAVA YOLU (551 m3/h): plint emis izgarasi %.0f cm2 (%.1f m/s) -> taban emis delikleri %.0f cm2 (%.1f m/s) -> plenum + 2 serit -> kondenser -> atis: K4 kapagi izgarasi net %.0f cm2 (%.1f m/s)"
          % (pli, Vh / (pli / 1e4), emis, Vh / (emis / 1e4), atis, Vh / (atis / 1e4)))
    assert cu_.zmin - pr_.zmax >= 95.0 and abs(fn_.zmin - cu_.zmax) < 0.01 and emis >= 800.0 and pli >= 400.0 and atis >= 600.0
    YOL = kut(TAVA[0], TAVA[1], TAVA[2] + 0.5, TAVA[3] + 1.0, TAVA[4], Z_ON1 + (TAVA[5] - TAVA[4]) + 10.0).val()
    dolu = _kesisim(YOL, PARCALAR, haric={"buharlastirma_tavasi", "k4_kapak_sogutma_dis_sac"} | {a_ for a_ in BB if a_.startswith("k4_izgara_")})
    print("   TAVA %.0f × %.1f × %.0f (x %.0f-%.0f · y %.1f-%.1f · z %.0f…%.0f): sogutma kapagi acik, tava one %+.0f'ye cekilir -> yolunda %d parca · cek valf alti %.1f / tava agzi %.1f"
          % (tv_.xlen, tv_.ylen, tv_.zlen, tv_.xmin, tv_.xmax, tv_.ymin, tv_.ymax, tv_.zmin, tv_.zmax, Z_ON1 + tv_.zlen + 10.0, len(dolu),
             min(yb("gider_cek_valfi_%s" % y_).ymin for y_ in EVAP), tv_.ymax))
    assert not dolu, "tava cekme yolunda parca var: %s" % dolu[:5]
    alt_ = [p["ad"] for p in PARCALAR if BB[p["ad"]].ymin < Y_PLINT - 0.01 and not p["ad"].startswith(("ayak_", "onyuz_plint"))]
    print("   DOLABIN ALTI (y < %.0f): ayak %d + plint %d disinda %d parca (v7: atis kanali + tava + gider borulari)"
          % (Y_PLINT, len([a_ for a_ in BB if a_.startswith("ayak_")]), len([a_ for a_ in BB if a_.startswith("onyuz_plint")]), len(alt_)))
    assert not alt_, "dolabin altinda parca: %s" % alt_[:5]''')
degis("    Lz = (-Z_ARKA - 41.5) / 1000.0", "    Lz = (ZP1_ON - Z_ARKA) / 1000.0                                   # v8: iç derinlik +79 uzadı")
degis("    if tarama:\n        cakisma()", "    havada_denetim()\n    if tarama:\n        cakisma()")
once("def _kesis(L1, L2, esik, ayni=True):", '''# v8 · HAVADA PARÇA beyaz listesi (SPEC §1 · §2.1: belgelenmiş istisna)
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

''')

once("    for tip in TOP:                                                     # v8: katılardan", '''    # ---- v8 · AVARA KOLU (104 boy) + AVARA MİLİ + SENSÖR LAMI: dayanım / sehim (kayış ön gerginliği VARSAYIM) ----
    E_ = 193000.0; T0 = 30.0                                            # N · GT3 6 mm kol başına ön gerginlik [VARSAYIM]
    Fs, Ft = 0.853 / (KAS_PD / 2000.0), 5.3 / (KAS_PD / 2000.0)          # sürekli / kısa süreli tepe (sıkışma: sürücü akım sınırı keser)
    h_ = min(HH[c[2]] for c in CEK) + 12.0 - (KY - 8.0)                 # en kısa kol gövdesi (lahmacun) 50
    A1, A2 = KOL_T * h_, KOL_FL * KOL_T
    xg = (A1 * KOL_T / 2.0 + A2 * KOL_FL / 2.0) / (A1 + A2)             # kesit ağırlık merkezi (kolun iç yüzünden x)
    Iy = h_ * KOL_T ** 3 / 12.0 + A1 * (xg - KOL_T / 2.0) ** 2 + KOL_T * KOL_FL ** 3 / 12.0 + A2 * (KOL_FL / 2.0 - xg) ** 2
    ek_ = KX - (RAY_T + 0.1 + xg); Lk = Z_CER0 - Z_AVARA                 # kayış hattının kesite kaçıklığı · flanştan mil eksenine boy
    sap = lambda R: R * ek_ * Lk ** 2 / (2.0 * E_ * Iy)
    I0 = h_ * KOL_T ** 3 / 12.0
    sap0 = lambda R: R * (KX - RAY_T - 0.1 - KOL_T / 2.0) * Lk ** 2 / (2.0 * E_ * I0)
    Rs, Rt = 2.0 * T0 + Fs, 2.0 * T0 + Ft
    km = KX - RAY_T - 0.1 - KOL_T; Wm = math.pi * 5.0 ** 3 / 32.0      # mil konsolu (kol yüzünden kayış hattına) · Ø5 mil
    Ll = (Z_AVARA - 8.0) - (Z_ARKA + 2.0); tl = SEN[2]                   # lam açıklığı · lam genişliği 6,35
    Al1, Al2 = tl * 2.0, 2.0 * LAM_H; yl = (Al1 * 1.0 + Al2 * (2.0 + LAM_H / 2.0)) / (Al1 + Al2)
    Il = tl * 8.0 / 12.0 + Al1 * (yl - 1.0) ** 2 + 2.0 * LAM_H ** 3 / 12.0 + Al2 * (2.0 + LAM_H / 2.0 - yl) ** 2
    wl = 7.9e-6 * 9.81 * (Al1 + Al2); wl0 = 7.9e-6 * 9.81 * Al1
    print("AVARA KOLU v8 (L gövde %.0f × %.0f + flanş %.0f × %.0f, boy %.0f): kayış çekişi kesite %.1f kaçık -> uç sapması sürekli %.3f / tepe %.3f mm (iç raya boşluk 0,1 · düz 3 mm kol olsaydı %.2f / %.2f) · avara mili Ø5 eğilme sürekli %.0f / tepe %.0f MPa (304 akma 205) · sensör lamı L sehim %.2f mm (düz lam %.1f)"
          % (h_, KOL_T, KOL_FL, KOL_T, Lk, ek_, sap(Rs), sap(Rt), sap0(Rs), sap0(Rt), Rs * km / Wm, Rt * km / Wm,
             5.0 * wl * Ll ** 4 / (384.0 * E_ * Il), 5.0 * wl0 * Ll ** 4 / (384.0 * E_ * tl * 8.0 / 12.0)))
    assert sap(Rt) < 0.1 - 0.02, "avara kolu tepe yükte iç raya değiyor"''')

# ================================================================ 8 · BOM
degis(r'(r"^isi_kalkani_takozu_[1-9]$", "Isı köprüsü kesici takoz")', r'(r"^isi_kalkani_takozu_([1-9]|1\d)$", "Isı köprüsü kesici takoz")')
once('    (r"^isi_kalkani_sag_sac$", "Isı kalkanı yan sacı (× 2)"),', r'''    (r"^sogutma_grubu_takozu_[1-3]$", "Titreşim pedi"), (r"^damlama_teknesi_(sol_braketi_2|sag_braketi_[12])$", "Damlama teknesi braketi"),
    (r"^gider_cek_valfi_sag$", "Ördek gagası çek valf"), (r"^k4_emis_(yan_sac|on_kapama)_sag$", "Emiş şeridi sacı (× 2)"), (r"^onyuz_plint_donus_sag$", "Plint yan dönüşü (× 2)"),''')
degis('"poşeti", "Yaylı menteşe"))', '"poşeti", "Yaylı menteşe", "Titreşim pedi", "Minivalve"))')
degis('bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v10"))', 'bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v11"))')

# ================================================================ 9 · v8b · BAĞIMSIZ DENETÇİ DÜZELTMELERİ (28 Eyl sabah · 6 ORTA + 9 KÜÇÜK)
# Aynı dosya store_cad_v8.py yeniden yazılır (bu işin yeni sürümü; eski sürümlere dokunulmaz). Bulgu no → düzeltme on_duzlem_v63/rapor_B.md'de.
satir("    (yap_store_cad_v8.py) · BOM 1_STORE_v11",
      "    (yap_store_cad_v8.py) · BOM 1_STORE_v11" + NL +
      "v8 DENETÇİ DÜZELTMELERİ (28 Eyl sabah · bağımsız denetim 6 ORTA + 9 KÜÇÜK · on_duzlem_v63/rapor_B.md): K4 depo = elle çekilen ÇEKMECE" + NL +
      "    (Accuride DZ3832-TR bas-aç) · K4 soğutma + şerit servis kapağı = gizli klipsli SÖKÜLÜR panel (menteşeli 40'lık kapak 3 mm derzde komşu öne" + NL +
      "    çarpıyordu) · Secop 2 × L 40×40×3 montaj rayında, ayırma saclarına 5 mm + EPDM sünger conta, önden servis yolu · gider SÜREKLİ ≥ %1 eğim" + NL +
      "    (sifon yok, ördek gagası kuru kapan), bölme geçişleri kılıflı · avara kolu 2 mm, iç raya 1,0 · avara 2 × MR126, Ø6 mil · sensör lamı" + NL +
      "    kulak bindirmeli + 16 mm tırnak · klape menteşe kıvrımları · 45° düşme oluğu · K4 paneli lazer yarıklı · plint üst flanşlı, kısa yarıklı" + NL +
      "    ızgara · pano havalandırması · adlar: onyuz_cerceve_saci_1.0, kasa_yan_dis_sac_*, kasa_yan_on_donus_sol")

# ---- 9.1 · sabitler: tava, gider yolu, Secop montajı, emiş pencereleri, yarıklar, kol / lam / avara
satir("TAVA = (2031.0, 2496.0, 124.5, 164.5",
      "TAVA = (2031.0, 2496.0, 124.5, 157.5, -91.0, 24.0)    # v8b: 33 yüksek (gider sürekli eğimi için 7 alçak) · 9 öne (ön Secop rayına 5) · brüt 1,6 L · servis paneli sökülünce öne çekilir")
satir("taban PU'su İÇİNDEN (U-sifon + ördek gagası çek valf)",
      "#      v8b: soğuk bölmelerin arkasından SÜREKLİ EĞİMLE (≥ %1, sifon YOK · ördek gagası = kuru kapan) → dolabın altında ayak + plint dışında HİÇBİR şey yok")
blok_sil("DR_Z, DR_R = -700.0, 6.0", 'DR_X_UC = {"sol": 2045.0, "sag": 2482.0}')
once("VALF = (7.0, 10.0)", '''DR_Z, DR_R, DR_KILIF = -690.0, 6.0, 8.0       # v8b · gider Ø12 PVC: tekne çıkışı z (tekne −756…−660) · kılıf Ø16 (iç Ø12 = boru dış çapı, kayar geçme)
DR_EGIM = 0.010                               # v8b: SÜREKLİ İNİŞ, her koşuda en az %1 (denetçi ORTA 5: v8'de U-sifon köpük içinde, eğim 0, durgun su)
DR_Y0 = {"sol": 191.0, "sag": 190.0}          # tekne altında yatay koşu başı: K3 / K5 en alt çekmecesinin kayışının (alt koşu 197,3) altından ≥ 1 mm
DR_Z_DON, DR_Z_ON = -645.0, -60.0             # bölme içinde öne dönüş sonu (perde −654 önü · B4 dikmesi −635 arkası) · K4'te çıkış z (tava üstü)
DR_X_YUK = {"sol": 2010.0, "sag": 2517.0}     # bölme ortası: B3 (1992,5–2027,5) · B4 (2500–2535) — PU içinde KILIFLI (boru çekilip değiştirilir)
DR_X_UC = {"sol": 2042.0, "sag": 2485.0}      # K4 yan emiş şeridinde öne koşu x · ucunda ördek gagası (tava ağzının 1,5 üstü)''')
blok_sil("TAKOZ_H = 4.0 ", "PLINT_IZGARA = [(1905.0")
satir("KOL_T = 3.0 ", '''TAKOZ_H = 4.0                                 # titreşim pedi 40 × 30 × 4 (Secop tabanı ↔ montaj rayı)
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
SOG_V8 = dict(bos=476.6, dol=585.9, dol_s=641.3, secop_tablo=688.0, secop_foy=661.0)   # v1 aynı koşuda 457 / 566 / 621''')

# ---- 9.2 · gider yolu (modül düzeyi) · K4 depo çekmecesi · klape kıvrımları
blok_sil("def gider_yollari():", "    return out")
once("def profil(k, eks, t=2.0):", '''def gider_noktalari(yan):
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


''')

# ---- 9.3 · çekmece: avara (2 × MR126, Ø6 mil) · avara kolu 2 mm + ön flanş 20 + arka kulak · sensör lamı 16 mm tırnak
degis(".cut(silx(ky, 0.0, 2.5, fl0 - 1, fl1 + 1)))", ".cut(silx(ky, 0.0, AVARA_MIL_R, fl0 - 1, fl1 + 1)))")
degis("alüminyum · 2 × 625-2RS · v8: iç flanş yok", "alüminyum · 2 × MR126-2RS (6 × 12 × 4: 8 ≤ göbek 9,5 — v8'deki 2 × 625 = 10 sığmıyordu) · v8: iç flanş yok")
degis('ekle(kod + "_avara_mili", silx(ky, Z_AVARA, 2.5, x0 + RAY_T + 0.1 + KOL_T, fl1 + 1.0), "celik", kod)',
      'ekle(kod + "_avara_mili", silx(ky, Z_AVARA, AVARA_MIL_R, x0 + RAY_T + KOL_BOS + KOL_T, fl1 + 1.0), "celik", kod,' + NL +
      '         bom=("Avara mili Ø6 · omuzlu", 1, "304 · kola somunla (kolun iç yüzünde) · 2 × MR126-2RS taşır", "v8b: Ø5 → Ø6 (sıkışma tepesinde 182 → ~108 MPa)"))')
blok_sil("    # v8: avara kolu 3 mm + ön flanş (104 boy", 'kayış gergisi burada: 8 mm yuvalı"))')
once("    # kayış (üst ve alt koşu, yan bantta)", '''    # v8b: avara kolu 2 mm sac (denetçi ORTA 3) · iç raya KOL_BOS 1,0, avaraya 1,3 · üst L flanş 12 · ön flanş 20 × 12,7 çerçeve sacının arkasına
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
              "boy 104 (−81…+23), moment kolu 96 · iç raya 1,0 · avaraya 1,3 · kayış gergisi burada: 8 mm yuvalı"))''')
degis("kut(lx0, lx1, ly1 - 24.0, ly1, Z_ARKA, ZT_)", "kut(lx1 - LAM_TIRNAK, lx1, ly1 - 24.0, ly1, Z_ARKA, ZT_)")
degis("kut(lx0, lx1, yk - 22.0, yk + 2.0, Z_ARKA, ZT_)", "kut(lx1 - LAM_TIRNAK, lx1, yk - 22.0, yk + 2.0, Z_ARKA, ZT_)")
degis('"304 büküm · reed sensörler altında · önde avara koluna, arkada arka iç saca 2 × M4",',
      '"304 büküm · reed sensörler altında · önde avara kolunun arka kulağına 20 bindirme 2 × M3 perçin · arkada 16 geniş tırnakla arka iç saca 2 × M4 perçin somun",')

# ---- 9.4 · kasa: gider kılıfları · plint flanşı · adlar · emiş pencereleri + pano yarıkları
satir("    GID = gider_yollari(); GID_L = [g_ for y_ in GID for g_ in GID[y_]]", '''    GID = gider_yollari(); GID_L = []                                   # v8b: bölme sacı / PU yalnız KILIFIN dışıyla kesilir (boru kılıfın içinde kayar)
    for y_ in GID:
        for _a, d_, _k in GID[y_]["kilif"]:
            b_ = d_.val().BoundingBox(); GID_L.append(((b_.xmin, b_.xmax, b_.ymin, b_.ymax, b_.zmin, b_.zmax), d_))''')
satir("    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1])",
      "    pl_ = kut(X_IC0, X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1]).union(kut(X_IC0 + 1.5, X_IC1 - 1.5, Y_PLINT - 1.5, Y_PLINT, PZ[0] - PLINT_FLANS, PZ[0]))   # v8b: üst flanş")
degis('"304 fırçalı 1,5 · z +17,5…+19 (ön düzlemin 60 gerisi) · x 30–3970 · K4 önünde emiş ızgarası %d yarık %.0f cm²"',
      '"304 fırçalı 1,5 · z +17,5…+19 (ön düzlemin 60 gerisi) · x 30–3970 · üst flanş 25: taban dış sacına M5 perçin somun @ 300 · K4 önünde emiş ızgarası %d yarık 120 × 10 (köprü 5 / 8) %.0f cm²"')
degis('ekle("onyuz_plint_donus_" + ad_, kut(x_, x_ + 1.5, 0.0, Y_PLINT, -DZ + 1.5, PZ[0]), "sac", B,',
      'ekle("onyuz_plint_donus_" + ad_, kut(x_, x_ + 1.5, 0.0, Y_PLINT, -DZ + 1.5, PZ[0]).union(kut(x_ + 1.5 if ad_ == "sol" else x_ - 20.0, x_ + 21.5 if ad_ == "sol" else x_,'
      ' Y_PLINT - 1.5, Y_PLINT, -DZ + 1.5, PZ[0] - PLINT_FLANS)), "sac", B,')
degis('"304 · x 30 ve 3970 · plintten arka dış sac hizasına"', '"304 · x 30 ve 3970 · plintten arka dış sac hizasına · üst flanş 20: taban dış sacına M5 perçin somun"')
degis('sac("yan_dis_sac_sol",', 'sac("kasa_yan_dis_sac_sol",')
degis('sac("yan_dis_sac_sag",', 'sac("kasa_yan_dis_sac_sag",')
degis('sac("yan_on_donus_sol",', 'sac("kasa_yan_on_donus_sol",')
once('    sac("taban_dis_sac", (1.5, W_B - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, Z_ON0), ek=EMIS,', '''    for a_, b_ in PANO_YARIK:                                           # v8b: pano bölmesi hava girişi (plint boşluğundan · denetçi KÜÇÜK 14)
        EMIS = EMIS.union(kut(a_, b_, Y_PLINT - 1.0, Y_PLINT + 3.0, PANO_YARIK_Z[0], PANO_YARIK_Z[1]))''')
satir('        bom=("Taban dış sacı 1,5", 1, "304 · v8: ön kenar +39',
      '        bom=("Taban dış sacı 1,5", 1, "304 · v8: ön kenar +39 · K4 altında %d emiş penceresi %.0f cm² (aralarında ≥ 20 köprü · paslanmaz tel elek [VARSAYIM]) + pano girişi %d × 80 × 12"')
satir("plint boşluğundan Secop'a hava", '''             % (len(EMIS_DELIK), sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in EMIS_DELIK) / 100.0, len(PANO_YARIK)), "plint boşluğundan Secop'a ve panoya hava · Secop yükünü montaj rayları taşır, taban sacı taşımaz"))''')
degis('ekle("on_cerceve_saci_1.0", cer,', 'ekle("onyuz_cerceve_saci_1.0", cer,')
degis("        xa_, xb_ = (kx0, kx1) if _f else (K4X + 2.5, K4_SAG - 2.5)",
      "        xa_, xb_ = (K4X, K4_SAG) if _f else (K4X + 2.5, K4_SAG - 2.5)   # v8b: depo çekmecesi açıklığı K4 tam genişlik 2027,5–2500")

# ---- 9.5 · gider borusu + kılıf + kelepçe + çek valf (soğutma döngüsünde)
blok_sil("        gb = None", 'sifon kuruyunca sıcak hava / koku geri gelmesin (keşif B §6.5)") if ilk else None)')
once('    ekle("buharlastirma_tavasi", kut(*TAVA)', '''        gb = GID[yan]["boru"]; P_ = GID[yan]["P"]
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
                  "v8b: KURU KAPAN (buzdolabı gideri gibi): tava buharlaştırdıkça kurur, su kapanı güvenilmez → sıcak hava / koku geri gelmez") if ilk else None)''')

# ---- 9.6 · K4: Secop montaj rayları + pedler + contalar · ara katman kotu sabit · perde yarıkları · depo çekmecesi · servis paneli
blok_sil("    # v8 · SECOP CU NLE8.8CN 180° DÖNÜK", "    s0 = cy0 + CU[1] + 8.0")
once("    # v6: ara katman K4'ün tam genişliğinde (B3 → B4)", '''    # v8b · SECOP CU NLE8.8CN 180° DÖNÜK (keşif B §6.5 Öneri 1) — denetçi ORTA 2: taban 4 pedle 2 × L 40×40×3 MONTAJ RAYINA oturur (raylar uç plakasıyla
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
    assert abs(s0 - (cy0 + CU[1]) - SECOP_BOS) < 0.01, "Secop ustu ara sac boslugu %.1f (5 olmali)" % (s0 - cy0 - CU[1])''')
satir('    ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, PERDE_Z, PERDE_Z + 1.0), "sac", "B_SOGUTMA",', '''    PY_ = None
    for a_, b_ in PANO_YARIK:                                               # v8b: pano havasının çıkışı (üstte) → plenum (Secop fanı çeker)
        _k = kut(a_, b_, PANO_YARIK_Y[0], PANO_YARIK_Y[1], PERDE_Z - 1.0, PERDE_Z + 2.0)
        PY_ = _k if PY_ is None else PY_.union(_k)
    ekle("k4_ara_perde", kut(kx0, K4_SAG, Y_PLINT + 1.5, s0, PERDE_Z, PERDE_Z + 1.0).cut(PY_), "sac", "B_SOGUTMA",''')
satir('bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında · v8: z −655',
      '         bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında · v8: z −655 = emiş plenumunun arka duvarı · v8b: üstte 4 × 80 × 12 havalandırma yarığı (pano → plenum)", "pano tabandan emer, perde üstünden plenuma verir"))')
blok_sil("    # v8 · EMİŞ / ATIŞ AYRIMI: kondenser perdesi", '"304 · şeridin önünü kapatır (önü atış bölgesi: tava + ızgara)", "") if ad_ == "sol" else None)')
once("    ZP = Z_ARKA + 2.0 ", '''    # v8b · EMİŞ / ATIŞ AYRIMI: emiş şeridi yan sacları üniteden 5 mm uzakta (aradaki boşluk taban yanı boyunca sünger conta) · kondenser çevresi
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
             bom=("Emiş şeridi ön kapaması 1,5", 2, "304 · şeridin önünü kapatır (önü atış bölgesi: tava + panel) · ön ray üstünde oyuklu · gider borusu lastik geçişli", "") if ad_ == "sol" else None)''')
blok_sil("    # KAŞAR + SUCUK DEPOSU (4 günün 2. yarısı)", 'ekle("k4_izgara_%02d" % i')
once("    # ---------------- ŞERİT 3810–4000 · ROBOT ÇÖPÜ (soğuk DEĞİL)", '''    # v8b · K4 DEPO = ELLE ÇEKİLEN ÇEKMECE (denetçi ORTA 1: gizli menteşeli 40'lık kapak 3 mm derzde komşu çekmece önüne çarpıyordu) ·
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
             bom=("K4 depo çekmecesi önü 40 · kulpsuz", 1, "dış 304 1,5 + PU 37,5 + iç 304 1,0 (fitil kanallı) · bas-aç (Accuride DZ3832-TR)", "%.0f × %.0f" % (b_ - a_, ON_UST - s0 - 15.0)))
''')

# ---- 9.7 · şerit: servis paneli klipsli · düşme oluğu · klape kıvrımları
degis('"Şerit servis kapağı 1,5 · yalıtımsız"', '"Şerit servis paneli 1,5 · yalıtımsız · sökülür"')
degis('"304 büküm · 40 dönüş · bas-aç mandal + 2 gizli menteşe [VARSAYIM]",',
      '"304 büküm · 40 dönüş · 4 gizli klipsle düz çekilir (menteşe YOK — v8b · denetçi ORTA 1: menteşe 3 mm derzde K6 önüne çarpıyordu)",')
once("    ky_, kz_ = KLAPE_EKSEN", '''    for i_, (xa_, xb_) in enumerate(((SK0 + 1.5, XS - 1.0), (KOVA[1] + 1.0, W_B - 1.5))):     # v8b: servis paneli klipsleri (sol: çerçeve sacı · sağ: yan dış sac)
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
                                                "v8b: atılan parça klapenin arkasındaki 40'lık dönüş rafında kalmaz, kovaya kayar"))''')
degis('ekle("klape_levhasi", kut(KLAPE_AC[0] - 6.0, KLAPE_AC[1] + 6.0, KLAPE_AC[2] - 6.0, ky_ - 4.0, Z_ON - 3.0, Z_ON - 1.5), "sac", C, grup="KLAPE",',
      'ekle("klape_levhasi", klape_levha(ky_, kz_), "sac", C, grup="KLAPE",')
satir('    ekle("klape_mentese_yapragi"', '    ekle("klape_mentese_yapragi", klape_yaprak(ky_, kz_), "celik", C)   # v8b: yaprak kıvrımları pimi sarar (denetçi KÜÇÜK 7)')

# ---- 9.8 · denetim
degis('print("CEKMECELI DOLAP v8 (on duzlem +79 · arka -830 · derinlik 909) · tek parca',
      'print("CEKMECELI DOLAP v8 + denetci duzeltmeleri (on duzlem +79 · arka -830 · derinlik 909) · tek parca')
once("    # ---- RAY: tam açıkta elemanlar birbirinin içinde kalıyor mu", '''    # ---- v8b · K4 DEPO ÇEKMECESİ (elle · bas-aç): ray bindirmesi, kutu ↔ iç ray bağı, açıkken GN 1/1 ön düzlemin dışında (katılardan) ----
    zr = {}
    for el in ("dis", "ara", "ic"):
        bb = BB["k4_depo_ray_%s_sol" % el]; k = {"dis": 0.0, "ara": RAY_ARA_ORAN, "ic": 1.0}[el] * STROK
        zr[el] = (bb.zmin + k, bb.zmax + k)
    b1 = min(zr["dis"][1], zr["ara"][1]) - max(zr["dis"][0], zr["ara"][0]); b2 = min(zr["ara"][1], zr["ic"][1]) - max(zr["ara"][0], zr["ic"][0])
    ku_ = yb("k4_depo_kutu_U_1.5"); bag = min(zr["ic"][1], ku_.zmax + STROK) - max(zr["ic"][0], ku_.zmin + STROK); gn_ = yb("k4_depo_GN11_100")
    print("K4 DEPO CEKMECESI (elle · Accuride DZ3832-TR bas-ac · grup CEKMECE): kutu %.1f × %.1f × %.0f · strok %.0f · bindirme dis-ara %.0f / ara-ic %.0f · kutu-ic ray bagi %.0f · acikken GN 1/1 arkasi z %+.0f (on duzlem %+.0f + 10)"
          % (ku_.xlen, ku_.ylen, ku_.zlen, STROK, b1, b2, bag, gn_.zmin + STROK, Z_ON1))
    assert b1 >= 250.0 and b2 >= 250.0 and bag >= ku_.zlen - 5.0 and gn_.zmin + STROK >= Z_ON1 + 10.0, "K4 depo cekmecesi"''')
blok_sil('    print("AVARA KOLU v8 (L gövde', '    assert sap(Rt) < 0.1 - 0.02, "avara kolu tepe yükte iç raya değiyor"')
once("    for tip in TOP:                                                     # v8: katılardan", '''    av_bos = (KX - KAS_B / 2.0 + 1.5) - (RAY_T + KOL_BOS + KOL_T)       # kol dış yüzü ↔ avara göbeği
    av_gen = KAS_B - 1.5                                                # avara göbek + dış flanş genişliği 9,5
    print("AVARA KOLU v8b (L gövde %.0f × %.0f + flanş %.0f × %.0f · boy 104 (−81…+23), moment kolu %.0f): kayış çekişi kesite %.1f kaçık -> uç sapması sürekli %.3f / tepe %.3f mm (iç raya boşluk %.1f · avaraya %.1f · düz kol olsaydı %.2f / %.2f) · avara mili Ø%.0f eğilme sürekli %.0f / tepe %.0f MPa (304 akma 205) · avara %.1f / 2 × MR126 %.0f · sensör lamı L sehim %.2f mm (düz lam %.1f)"
          % (h_, KOL_T, KOL_FL, KOL_T, Lk, ek_, sap(Rs), sap(Rt), KOL_BOS, av_bos, sap0(Rs), sap0(Rt), 2 * AVARA_MIL_R, Rs * km / Wm, Rt * km / Wm, av_gen, 2 * 4.0,
             5.0 * wl * Ll ** 4 / (384.0 * E_ * Il), 5.0 * wl0 * Ll ** 4 / (384.0 * E_ * tl * 8.0 / 12.0)))
    assert sap(Rt) < KOL_BOS - 0.5 and av_bos >= 1.0 and KOL_BOS >= 1.0 and av_gen >= 8.0, "avara kolu / avara bosluklari"
    assert Rt * km / Wm <= 205.0 / 1.5, "avara mili tepe gerilmesi 205/1,5'u gecti"''')
degis("    ek_ = KX - (RAY_T + 0.1 + xg); Lk = Z_CER0 - Z_AVARA", "    ek_ = KX - (RAY_T + KOL_BOS + xg); Lk = Z_CER0 - Z_AVARA")
degis("    sap0 = lambda R: R * (KX - RAY_T - 0.1 - KOL_T / 2.0) * Lk ** 2 / (2.0 * E_ * I0)", "    sap0 = lambda R: R * (KX - RAY_T - KOL_BOS - KOL_T / 2.0) * Lk ** 2 / (2.0 * E_ * I0)")
degis("    km = KX - RAY_T - 0.1 - KOL_T; Wm = math.pi * 5.0 ** 3 / 32.0", "    km = KX - RAY_T - KOL_BOS - KOL_T; Wm = math.pi * (2.0 * AVARA_MIL_R) ** 3 / 32.0")
blok_sil("    ps_ = yb(\"robot_cop_poseti\")", '    assert not dolu, "atma boslugunda parca var: %s" % dolu[:5]')
once("    GIR = kut(KLAPE_AC[0], KLAPE_AC[1], KLAPE_AC[2], KLAPE_AC[3], KOVA[5], Z_ON1).val()", '''    ps_ = yb("robot_cop_poseti"); ol_ = yb("serit_dusme_olugu")
    AT = kut(KOVA[0], KOVA[1], ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5]).val()
    dolu = _kesisim(AT, PARCALAR, haric=("serit_dusme_olugu",))
    UST = kut(KLAPE_AC[0], KLAPE_AC[1], SERIT_PANEL[0] + 1.5, KLAPE_AC[2], KOVA[5], Z_ON1 - 1.5).val()      # v8b · denetçi KÜÇÜK 8: klape arkası z +37…+77,5
    dolu2 = _kesisim(UST, PARCALAR, haric=("serit_dusme_olugu", "klape_levhasi"))
    ol_ac = math.degrees(math.atan2(1.0, 1.0))
    print("   ATMA BOSLUGU (kova izdusumu, poset agzi %.1f -> klape acikligi ustu %.0f, z %.0f…%.0f): oluk disinda %d parca · klape arkasi (z %+.0f…%+.1f, y %.1f-%.0f) oluk + klape disinda %d parca · DUSME OLUGU %.0f° y %.1f-%.1f z %+.1f…%+.1f (ustu klapeye %.0f, alt kenari kova onunun %.0f gerisi) · ustunde tasiyici kiris %.1f-%.1f"
          % (ps_.ymax, KLAPE_AC[3], KOVA[4], KOVA[5], len(dolu), KOVA[5], Z_ON1 - 1.5, SERIT_PANEL[0] + 1.5, KLAPE_AC[2], len(dolu2), ol_ac, ol_.ymin, ol_.ymax, ol_.zmin, ol_.zmax,
             KLAPE_AC[2] - ol_.ymax, KOVA[5] - ol_.zmin, TK_Y[0], TK_Y[1]))
    assert not dolu and not dolu2 and ol_ac >= 45.0 - 0.01 and ol_.zmin <= KOVA[5] - 10.0, "atma boslugu / klape arkasi: %s %s" % (dolu[:5], dolu2[:5])''')
satir("    cu_ = yb(\"sogutma_grubu_kondenser\"); ta_ = yb(\"sogutma_grubu_taban\")",
      "    cu_ = yb(\"sogutma_grubu_kondenser\"); ta_ = yb(\"sogutma_grubu_taban\"); fn_ = yb(\"sogutma_grubu_fan\"); tv_ = yb(\"buharlastirma_tavasi\"); pr_ = yb(\"k4_ara_perde\")")
blok_sil("    PEN = (K4X + 10.0, K4_SAG - 10.0, 165.0, s0_ - 3.5)", "    atis = ((PEN[1] - PEN[0])")
once("    Vh = 551.0 / 3600.0 ", "    atis = sum((b_ - a_) * (d_ - c_) for a_, b_, c_, d_ in K4_YARIK) / 100.0    # v8b: panel lazer yarıkları (net)")
degis("ust aralik %.1f (kondenser perdesiyle kapali)", "ust aralik %.1f (EPDM sunger contayla kapali)")
degis("    assert cu_.zmin - pr_.zmax >= 95.0 and abs(fn_.zmin - cu_.zmax) < 0.01 and emis >= 800.0 and pli >= 400.0 and atis >= 600.0",
      '''    kop = min([EMIS_DELIK[i + 1][0] - EMIS_DELIK[i][1] for i in (0, 1)] + [EMIS_DELIK[i + 1][2] - EMIS_DELIK[i][3] for i in (3, 4, 6, 7)])
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
    assert dTp <= 10.0, "pano havalandirmasi yetersiz"''')
degis('    print("   HAVA YOLU (551 m3/h): plint emis izgarasi %.0f cm2 (%.1f m/s) -> taban emis delikleri %.0f cm2 (%.1f m/s) -> plenum + 2 serit -> kondenser -> atis: K4 kapagi izgarasi net %.0f cm2 (%.1f m/s)"',
      '    print("   HAVA YOLU (551 m3/h): plint emis izgarasi %.0f cm2 (%.1f m/s) -> taban emis pencereleri %.0f cm2 (%.1f m/s) -> plenum + 2 serit -> kondenser -> atis: K4 paneli lazer yariklari net %.0f cm2 (%.1f m/s)"')
degis("sogutma kapagi acik, tava one %+.0f'ye cekilir", "servis paneli sokulu, tava one %+.0f'ye cekilir")
degis('· tekne alti %.1f · gider x %.0f -> PU icinde U-sifon -> K4 cikis x %.0f"', '· tekne alti %.1f · gider x %.0f -> surekli egim >= %%1 -> K4 cikis x %.0f"')
satir('        assert gb_.ymin >= Y_PLINT + 1.5 + 10.0 and DR_Y + DR_R <= Y_TABAN - 1.0 - 10.0, "gider borusu taban PU\'sunun icinde degil"', '''        P_ = gider_noktalari(yan)
        eg = [(a_[1] - b_[1]) / math.hypot(b_[0] - a_[0], b_[2] - a_[2]) for a_, b_ in zip(P_, P_[1:]) if math.hypot(b_[0] - a_[0], b_[2] - a_[2]) > 1e-6]
        kl_ = sorted(a_ for a_ in BB if a_.startswith("gider_kilifi_%s_" % yan))
        print("      gider %s (denetci ORTA 5): %d dirsek · yatay kosularda egim en az %%%.2f · tekne alti %.1f -> cikis %.1f · en alcak nokta = cikis (sifon YOK, durgun su YOK) · kilif %s · en alt kayis (y %.1f) ile en az %.1f"
              % (yan, len(P_) - 2, 100.0 * min(eg), P_[0][1], P_[-1][1], ", ".join(kl_), YUZ0 + BIND + KY - KAS_OD / 2.0 - KAYIS_T,
                 min(YUZ0 + BIND + KY - KAS_OD / 2.0 - KAYIS_T - (yol_y(P_, xk_, DR_Z) + DR_R) for xk_ in [x_ + KX + s_ * KAYIS_W / 2.0 for x_ in (KOLON_X["K3"], KOLON_X["K5"]) for s_ in (-1.0, 1.0)]
                     if min(P_[1][0], P_[2][0]) <= xk_ <= max(P_[1][0], P_[2][0]))))
        assert min(eg) >= DR_EGIM - 1e-9 and all(b_[1] < a_[1] for a_, b_ in zip(P_, P_[1:])) and len(kl_) >= 1, "gider borusu surekli inmiyor / kilifsiz"''')
degis('print("ISI KALKANI v7 (rapor secenek b)', 'print("ISI KALKANI v8 (rapor secenek b)')
degis('    print("SOGUTMA v7: %d bolge · lamelli evaporator on yuzu %.3f m² · %d fan ebm-papst 4414 FL (%.1f W) · Secop CU NLE8.8CN 737 / 688 / 586 W @ −10 °C (25 / 32 / 43 °C) · gereken 552–661 W @ 32 °C (sogutma_hesabi_v1) · duvar iletimi ~%.0f W (PU k %.3f, ortam %.0f, firin alti %.0f °C VARSAYIM)"\n          % (len(lam), ev, len(fan), 1.2 * len(fan), Q, k_pu, T_ort, T_fir))',
      '    print("SOGUTMA v8: %d bolge · lamelli evaporator on yuzu %.3f m² · %d fan ebm-papst 4414 FL (%.1f W) · Secop CU NLE8.8CN 32 °C: tablo %.0f / foy %.0f W @ −10 °C (CELISKI ACIK) · gereken (sogutma_hesabi_v1 v8 geometrisiyle, 18 sa · %%10 pay) bos gun %.0f · dolum %.0f · dolum + sicak hamur %.0f W -> pay %.0f…%.0f / %.0f…%.0f W · duvar iletimi (bu kaba model) ~%.0f W"\n          % (len(lam), ev, len(fan), 1.2 * len(fan), SOG_V8["secop_tablo"], SOG_V8["secop_foy"], SOG_V8["bos"], SOG_V8["dol"], SOG_V8["dol_s"],\n             SOG_V8["secop_foy"] - SOG_V8["dol"], SOG_V8["secop_tablo"] - SOG_V8["dol"], SOG_V8["secop_foy"] - SOG_V8["dol_s"], SOG_V8["secop_tablo"] - SOG_V8["dol_s"], Q))')

degis('        ust_p = max(BB[p["ad"]].ymax for p in ps if "_on_" not in p["ad"])',
      '        ust_p = max(BB[p["ad"]].ymax for p in ps if "_on_" not in p["ad"] and p["grup"] != "SABIT")' + NL +
      '        ust_s = max(BB[p["ad"]].ymax for p in ps if p["grup"] == "SABIT")          # v8b: sabit parçalar (ray, avara kolu ön flanşı) tavana değmez')
degis('        assert ust_p <= tav - 2.0 and fit <= tav + 0.01, "%s tavana degiyor" % kol', '        assert ust_p <= tav - 2.0 and ust_s <= tav - 0.5 and fit <= tav + 0.01, "%s tavana degiyor" % kol')
degis("· en ust cekmece parcasi %.1f · fitil ustu %.1f · ic tavan %.0f", "· en ust hareketli parca %.1f · en ust sabit parca %.1f · fitil ustu %.1f · ic tavan %.0f")
degis("YIGIN_SINIR[kol] - top_, ust_p, fit, tav))", "YIGIN_SINIR[kol] - top_, ust_p, ust_s, fit, tav))")
# ---- 9.9 · BOM: alt gövde kuralları + satın alma anahtarları
once('    (r"_on_(pu|ic_sac_1\\.0)$", "çekmece önü / kapak katmanı"),', r'''    (r"^k4_depo_ray_(dis_sag|ic_(sol|sag)|ara_(sol|sag))$", "Accuride DZ3832-TR"), (r"^k4_depo_kutu_(arka|on)_1\.5$", "K4 depo çekmece kutusu"),
    (r"^k4_depo_raf_tutucu_sag$", "Raf tutucu köşebent"), (r"^(k4_panel_klipsi_[1-3]|serit_panel_klipsi_\d)$", "Gizli panel klipsi"),
    (r"^sogutma_grubu_montaj_rayi_on$", "Yoğuşturucu montaj rayı"), (r"^k4_emis_yan_conta_sag$", "Sünger conta EPDM"), (r"^sogutma_grubu_taban_contasi$", "Kondenser çevre contası"),
    (r"^gider_kilifi_(sol_B3|sag_B4)$", "Gider kılıfı"), (r"^gider_kelepcesi_(sol_[1-9]|sag_\d)$", "Boru kelepçesi"),''')
degis('(r"^yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)")', '(r"^kasa_yan_dis_sac_sag$", "Yan dış sac 1,5 (× 2)")')
degis('"Titreşim pedi", "Minivalve"))', '"Titreşim pedi", "Minivalve", "Fastmount", "Sünger conta", "Kondenser çevre contası"))')

# ================================================================ son denetim: eski sabitler kalmasın
for yok in ("ATIS[", "GIDER_UC_Z", "DR_DELIK", "VENT[", "-41.5)", "-40.0))", "plint_on_1.5", '"kondenser_atis_kanali"',
            "DR_Y_CIK", "DR_ZON", "PENCERE[", "PENCERE = ", '"on_cerceve_saci', 'sac("yan_dis_sac', 'sac("yan_on_donus', "k4_kondenser_perdesi", "625-2RS", "RAY_T + 0.1"):
    assert yok not in s, "kalinti: %s" % yok
compile(s, "store_cad_v8.py", "exec")
io.open(os.path.join(U, "store_cad_v8.py"), "w", encoding="utf-8").write(s)
print("store_cad_v8.py yazildi · %d satir" % s.count(NL))
