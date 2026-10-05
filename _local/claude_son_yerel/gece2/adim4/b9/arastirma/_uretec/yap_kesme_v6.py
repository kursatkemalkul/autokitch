# -*- coding: utf-8 -*-
"""kesme_cad_v5 → kesme_cad_v6 (28 Eyl 2026 gece) — SPEC_on_duzlem_v63 §2.5 (Kemal: "fırının ön yüzü sınır yüzey, her şeyi o yüzeye getireceğiz …
her şeyi extend edip kapak takacaksın, çalışma düzenini bozma … bulaşık makinesi önüne kapak, alt ayaklarını kaldır … içeride havada kalan parça olmasın").
  · ÖN DÜZLEM +79: kabuk (sol, sağ, üst sac, taban_sac_3, istasyon_tabani_3) ön kenarı 0 → +59 (kapak arkası) · arka −830 SABİT → derinlik 909
  · ÖN ÇERÇEVE: 2 kesintisiz dikme (x 1,5–31,5 ve 570–598,5 · z +27…+57 · y 126–1860,5) + 4 kayıt (derz çizgilerinin arkasında) · öndeki
    kesik köşe dikmeleri (0, 1) kalktı · istasyon tabanı dikmelerin çevresinden önden açık çentikli
  · KAPAKLAR (tava panel 304 fırçalı 1,5 · 20 büküm · z +59…+79 · x 4003–4598,5): ALT (bulaşık) 126–883 · ORTA 886–1305 · ÜST 1308–1859 ·
    SOL gizli menteşe EMKA 1046-U5 (90°) · Southco E4 bas-aç · ORTA + ÜST Schmersal AZM40 kilit · ALT + ÜST lazer yarık havalandırma (KARAR varsayım) ·
    her kapak ayrı hareketli grup (KAPAK_ALT / KAPAK_ORTA / KAPAK_UST, kapak_ac()) · glb_yaz GRUPLAR'a eklendi
  · PLİNT plint_on (−61,5…−60) → onyuz_plint (+17,5…+19) + yan dönüşler
  · KÖPRÜ (KRİTİK, v5'te 1 mm havada): kirişler 8 mm uç plakalarına, plakalar yan saclara + ön çerçeve dikmesine
  · BULAŞIK v2 (bulasik_cad_v2): ayaklar kalktı · 2 × 40×20×2 tabla kirişi (yan saclara) + 3 mm tava → makine +13 (BULASIK_YER y 126 → 139, gövde altı 149)
  · HAVADA PARÇALAR bağlandı: pano ara burçları · MS4 + valf montaj sacı · tank köşebendi + rafı · ölü plaka yan levhalara · PulsaJet semeri ·
    DGRF-C iç burçları · sensör braketleri · home sensörü braketi · reed x 375 · ısıtıcı ceketler temaslı · hava hortumları valfe · hava_besleme_K SİLİNDİ (+ delik)
  · DENETİM: ön düzlem / kabuk / plint / derz · v5 ↔ v6 parça parça (değişen / yeni / çıkan listeleri beklenenle birebir) · kinematik v5 ile aynı ·
    kapaklar 0–90° tarama · bulaşık kapak açık zarfı ALT kapak AÇIKKEN · havada parça = 0 (denetim_temas_v1) · köprü / tabla / kapak / ısı hesapları
  · 2. TUR (28 Eyl gece, bağımsız denetçi bulguları → rapor_K.md "DENETÇİ BULGULARI"):
    ORTA-1 kablo_kanali_dikey arka köşe dikmesinin ÖNÜNE (ISTISNA 82 016 mm³ gizliyordu) + TAM İSTİSNASIZ TARAMA bütün parçalar / çevrim boyunca ·
    eski gömülü örtüşmeler delik / yuva ile giderildi (rulo mil yuvaları, yan levha delikleri + gergi yarığı, bıçak göbeği yuvaları, koruma braketi alın kaynağı,
    dirsek PulsaJet ucunda, bant rulo şeridi, DIN klipsi, tank kelepçesi, eksen ayağı) → ISTISNA listesi BOŞ ·
    ORTA-2 lazer yarık VARSAYILAN KAPALI (YARIK_ACIK = False, seçenek; desen ortalı) · ORTA-3 ısı: yarıksız kapalı durum hesabı + karar UYARI ·
    plint y 0–123 · x 0–600 · tam derinlik yan dönüş · üst flanş 15 · AZM40 dili kilit ağzına 8 mm girer · ALT kapak EPDM dayama lastiği (bulaşık kapağı buna dayanır) ·
    bulaşık bağlantılarına taban sacında rakorlu geçiş (3 delik + rakor / lastik) · fırın sözleşmesi firin_tp10_cad_v8 · E ileri uyum kutu_cad_v7 (arayüz + ürün / itici taramaları) ·
    kapaklar 90° açıkken havada YALNIZ kapak grupları (sanal pivot) denetimi
Çıktılar: kesme_v6.glb · kesme_v6.json · 4_KESME_v6/BOM*.csv. Önceki: kesme_cad_v5.py (DEĞİŞMEZ)"""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kesme_cad_v5.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


def blok(a, b, yeni):
    """a (tek) işaretinden b (tek) işaretine kadar (b hariç) → yeni"""
    global s
    assert s.count(a) == 1, (s.count(a), a[:110])
    assert s.count(b) == 1, (s.count(b), b[:110])
    i = s.index(a); j = s.index(b)
    assert i < j, (a[:60], b[:60])
    s = s[:i] + yeni + s[j:]


# ================================================================ 1 · BAŞLIK + İÇE ALMA ================================================================
d('"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v5 (27 Eyl 2026 gece): DETERJAN + PARLATICI KALKTI (Kemal: "deterjanları makinenin',
  '"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v6 (28 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.5 · Kemal:' + NL +
  '"fırının ön yüzü sınır yüzey … her şeyi extend edip kapak takacaksın … bulaşık makinesi önüne kapak, alt ayaklarını kaldır … içeride havada kalan parça olmasın").' + NL +
  'Kabuk ön kenarı +59 · ön çerçeve (2 kesintisiz dikme + 4 kayıt) · 3 tava kapak (304 fırçalı 1,5 · 20 büküm · z +59…+79 · SOL gizli menteşe, bas-aç,' + NL +
  'ORTA + ÜST AZM40 kilitli; önden YALNIZ düz yüzey + derz — lazer yarık yalnız SEÇENEK: YARIK_ACIK) ayrı hareketli gruplar · plint y 0–123 · x 0–600 · +17,5…+19 ·' + NL +
  'köprü kirişleri uç plakalarıyla yan saclara + ön dikmeye · bulaşık bulasik_cad_v2 (ayaksız) 40×20×2 kirişli 3 mm tablaya oturur (+13), bağlantıları taban' + NL +
  'sacındaki rakorlu geçişlerden çıkar · havada kalan 17 bileşen bağlandı (0) · hava_besleme_K silindi · TAM İSTİSNASIZ çakışma taraması 0 (ISTISNA listesi boş).' + NL +
  'Ürün yolu, kotlar, kinematik, E arayüzü v5 ile AYNI (ölçülür; E v7 ileri uyum da). Üretici: yap_kesme_v6.py (2. tur: denetçi düzeltmeleri). Önceki: kesme_cad_v5.py' + NL +
  'v5 (27 Eyl 2026 gece): DETERJAN + PARLATICI KALKTI (Kemal: "deterjanları makinenin')
d("import bulasik_cad_v1 as BM                                # v4: K altındaki bulaşık makinesi (ayrı modül; burada yalnız REF + yer denetimi)",
  "import bulasik_cad_v2 as BM                                # v6: ayaksız (tablaya oturur, +13) · sepet rayları + kol göbek boruları · v4: K altındaki bulaşık makinesi (ayrı modül; burada yalnız REF + yer denetimi)")

# ================================================================ 2 · v6 SABİTLERİ ================================================================
d("URUN_GIRISI = (BANT - 64.0, BANT + 76.0, -420.0, -8.0)  # v4: sol duvardaki fırın bandı / ürün girişi y0 y1 z0 z1 = 932–1072 (v3 1100–1240 sabitti) — montajdaki _ka" + NL,
  "URUN_GIRISI = (BANT - 64.0, BANT + 76.0, -420.0, -8.0)  # v4: sol duvardaki fırın bandı / ürün girişi y0 y1 z0 z1 = 932–1072 (v3 1100–1240 sabitti) — montajdaki _ka" + NL + r'''
# ---------------------------------------------------------------- v6 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1 + §2.5) ----------------------------------------------------------------
Z_ON = 79.0                       # ön düzlem = fırın gövdesinin ön yüzü (montaj sözleşmesi: KS.Z_ON = FT.ZS = 79) — bütün kapakların DIŞ yüzü
Z_ARKA = -D                       # −830 SABİT (arka dış sac yerinde) → gövde derinliği 909
TAVA_T, TAVA_D = 1.5, 20.0        # tava panel: 304 fırçalı 1,5 · kenarlar 20 arkaya bükülü (kuru istasyon kapağı, SPEC §1)
Z_TAVA = (Z_ON - TAVA_D, Z_ON)    # (+59 · +79)
Z_KABUK_ON = Z_TAVA[0]            # kabuk (sol, sağ, üst, taban sacı, istasyon tabanı) ön kenarı +59 = kapak arkası
DERZ = 3.0                        # panel ↔ panel, kapak ↔ kapak, istasyon ↔ istasyon
CER = 30.0                        # ön çerçeve profili 30 × 30 × 2
Z_CER = (Z_TAVA[0] - 2.0 - CER, Z_TAVA[0] - 2.0)   # (+27 · +57): kapak arkasıyla 2 mm = bas-aç mandal stroku
CER_X_SOL = (SAC, SAC + CER)      # 1,5–31,5
CER_X_SAG = (570.0, W - SAC)      # 570–598,5 (SPEC): 28,5 geniş → bükme kutu; bulaşık kapak zarfına (568,5) 1,5 pay
Y_CER = (Y_PLINT + 3.0, H - SAC)  # 126–1860,5 kesintisiz (taban sacı üstü → üst sac altı)
KAYITLAR = (("alt", Y_CER[0], Y_CER[0] + CER), ("883", 862.0, 892.0), ("1306", 1291.5, 1321.5), ("ust", Y_CER[1] - CER, Y_CER[1]))   # derz çizgilerinin arkasında
KAPAK_X = (DERZ, W - DERZ / 2.0)  # 3,0–598,5 (dünya 4003–4598,5): fırın / dolap yüzü 4000 → derz 3 · E kapakları 4601,5 → derz 3
X_E_KAPAK0 = 4601.5               # E kapaklarının sol kenarı (SPEC §1 dikey derzler: E 4601,5–5430)
KAPAKLAR = (("KAPAK_ALT", "alt", Y_PLINT + DERZ, 883.0), ("KAPAK_ORTA", "orta", 886.0, 1305.0), ("KAPAK_UST", "ust", 1308.0, H - DERZ))   # yatay derzler 883/886 · 1305/1308 · üst 1859
KAPAK_GRUP = tuple(k_[0] for k_ in KAPAKLAR)
SABIT_GRUP = ("SABIT",) + KAPAK_GRUP  # makine çalışırken kapaklar KAPALI → çakışma taramasında sabit gibi
MENTESE_EKSEN = (KAPAK_X[0], Z_ON)    # SOL gizli menteşe, sanal pivot = kapağın ön-sol köşesi (x 3, z 79) · dikey eksen
KAPAK_MAX = 90.0                  # EMKA 1046-U5 en çok 90° (emka.com)
MENTESE = dict(x=(8.0, 24.0), boy=79.0)          # EMKA 1046-U5 zarfı: boy ≈ 79 · pim Ø16 (GlobalSpec föyü) · genişlik 16 · kanat derinliği VARSAYIM
MENTESE_Y = {"alt": (226.0, 783.0), "orta": (986.0, 1205.0), "ust": (1408.0, 1759.0)}   # kapak kenarından 100
MANDAL = dict(x=(578.0, 592.0), boy=44.0, derin=14.0)   # Southco E4 dokun-aç mandal zarfı 14 × 44 × 14 VARSAYIM (sağ dikmenin ön yüzünde)
AZM = dict(boy=119.5, en=40.0, kal=20.0)          # Schmersal AZM40 119,5 × 40 × 20 (schmersal.com)
AZM_KAPAK = ("orta", "ust")                       # ORTA: bıçak + itici · ÜST: kılavuz mili uçları, tank (45 °C), pano
AZM_AGIZ = 8.0                    # 2. tur: kilit dili AZM40 giriş ağzına 8 mm girer (v6-1: dil z 59,5'te bitiyordu, kilide 2,5 mm — ulaşmıyordu) · ağız yeri/derinliği VARSAYIM (Schmersal çizimiyle teyit)
YARIK_ACIK = False                # 2. tur (denetçi ORTA-2): SPEC §1 "önden yalnız düz yüzey + derz" → VARSAYILAN YARIKSIZ · True = SEÇENEK (ısı kararıyla birlikte Kemal'e soruldu)
YARIK = dict(en=3.0, boy=40.0, adim=10.0, n=52,   # SEÇENEK: lazer yarık 3 × 40 (ISO 13857: e ≤ 4 → parmak geçmez), adım 10, sırada 52 · desen kapakta ORTALI (x0 44,25; v6-1 40 → 4,25 sola kaymıştı)
             bant={"alt": ((197.0, 237.0), (247.0, 287.0), (722.0, 762.0), (772.0, 812.0)),        # ALT: alt emiş · üst atış · paylar 71 / 71 (üst bant dayama lastiğinin 814–844 altında biter)
                   "ust": ((1330.0, 1370.0), (1380.0, 1420.0), (1747.0, 1787.0), (1797.0, 1837.0))})  # ÜST: paylar 22 / 22
DAYAMA = dict(x=(108.5, 568.5), y=(814.0, 844.0), t=3.0)   # 2. tur (denetçi K-11): ALT kapağın iç yüzünde EPDM dayama lastiği — bulaşık kapağının üst kenarı (x 110,5–566,5) buna dayanır, 1,5 sac değil
U_KAPALI = 5.0                    # W/m²K VARSAYIM (iyimser): kapalı bölmenin ön kapaktan ısı geçişi (doğal taşınım ~4 + ışınım, iç direnç yok sayıldı)
PLINT_FLANS = 15.0                # 2. tur (denetçi K-4): plint üst flanşı 15 (taban sacına M5 perçin somunu)
Z_PLINT = (Z_ON - 60.0 - TAVA_T, Z_ON - 60.0)    # (+17,5 · +19) — ön düzlemin 60 gerisi, bütün hat boyunca tek çizgi
RHO_304 = 7.93e-6                 # kg/mm³
E_304 = 193000.0                  # N/mm²
Q_BULASIK_W = 300.0               # VARSAYIM: MEIKO tezgâh altı makinenin duyulur ısı yayımı (föyde yok) — ısı tahmini için
Q_UST_W = 100.0                   # VARSAYIM: pano (~40) + tank ısıtıcısı ortalaması (~30) + ısıtmalı hortum / nozül (~30) · fırın ağzı sızıntısı BİLİNMİYOR
BULASIK_KG = 90.0                 # VARSAYIM: 70 kg (föy) + su + sepet + yük
V6_DEGISEN = ("taban_sac_3", "istasyon_tabani_3", "ust_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "kopru_kirisi_0", "kopru_kirisi_1", "olu_plaka",
              "yag_tanki_rafi", "yag_tanki_rafi_koseben", "yag_tanki_isitici_ceketi", "PulsaJet_isitici_ceket", "kesici_reed_0", "kesici_reed_1",
              "hava_hortumu_kaldirma", "hava_hortumu_tank",
              # 2. tur (denetçi ORTA-1 + K-9): kanal dikmenin önüne · eski gömülü örtüşmeler delik / yuva ile giderildi (işlev ve zarf aynı)
              "kablo_kanali_dikey", "yag_tanki_kelepcesi", "eksen_ayagi_1", "tahrik_rulosu_RollerDrive_EC5000", "kuyruk_rulosu", "bant_yan_levhasi_0",
              "bant_yan_levhasi_1", "bicak_gobek_halkasi", "sprey_dirsegi", "surucu_STP-DRV-4830") + tuple("koruma_braketi_%d" % _i for _i in range(6))   # + bütün REF_bulasik_ parçaları (+13 y)
              # (bant_PU_2mm de kesildi — 9,3 mm³, dilim_v1'in hacim eşiğinin altında "birebir" sayılır; V6_DELIK denetiminde ölçülür)
V6_DELIK = ("tahrik_rulosu_RollerDrive_EC5000", "kuyruk_rulosu", "bant_yan_levhasi_0", "bant_yan_levhasi_1", "bant_PU_2mm", "bicak_gobek_halkasi", "surucu_STP-DRV-4830",
            "yag_tanki_kelepcesi", "eksen_ayagi_1")    # 2. tur: yalnız delik / yuva / kesim — sınır kutusu v5 ile AYNI, hacim yalnız azalır (denetimde ölçülür)
V6_CIKAN = ("plint_on", "hava_besleme_K", "kose_dikmesi_0", "kose_dikmesi_1") + tuple("REF_bulasik_ayar_ayagi_%d" % _i for _i in range(4))
YENI_V6 = ("onyuz_", "kopru_kirisi_uc_plakasi_", "bulasik_tabla_kirisi_", "bulasik_tavasi", "sensor_braketi_", "PulsaJet_semeri", "DGRF_burcu_", "itici_home_braketi",
           "pano_ara_burcu_", "sartlandirici_montaj_saci", "REF_bulasik_sepet_rayi_", "REF_bulasik_yikama_kolu_gobek_borusu_", "bulasik_gecis_")


def _kati_kes(wp, arac):
    """2. tur: çok katılı (üretici STEP) bileşiği KATI KATI keser — bileşiği tek hamlede kesmek geçersiz katı üretir (OCP; din_parca notu)"""
    a = arac.val() if hasattr(arac, "val") else arac
    A = a.BoundingBox(); ss = []
    for q in wp.val().Solids():
        B_ = q.BoundingBox()
        kes_ = A.xmin < B_.xmax and B_.xmin < A.xmax and A.ymin < B_.ymax and B_.ymin < A.ymax and A.zmin < B_.zmax and B_.zmin < A.zmax
        ss.append(q.cut(a) if kes_ and q.intersect(a).Volume() > 1e-6 else q)
    return cq.Workplane(obj=cq.Compound.makeCompound(ss))
''')
d("KORUMA_ALT = Y_AGIZ_UST + 8.0" + NL,
  "KORUMA_ALT = Y_AGIZ_UST + 8.0" + NL +
  "UC_T = 8.0                        # v6: köprü uç plakası 8 mm (kirişler yan saclara + ön çerçeve dikmesine bu plakayla bağlanır)" + NL +
  "UC_Y = (Y_KIRIS[0] - 20.0, Y_KIRIS[1] + 20.0)" + NL +
  "UC_Z = (-290.0, Z_CER[0])         # arka ucu arka kirişin 20 gerisi · ön ucu ön çerçeve dikmesinin arka yüzü (+27)" + NL)

# ================================================================ 3 · GÖVDE + ÖN ÇERÇEVE + KAPAKLAR ================================================================
blok("def govde():", "# ---------------------------------------------------------------- 2 · K BANDI", r'''def govde():
    for i, (ax, az) in enumerate(((50.0, -110.0), (550.0, -110.0), (50.0, -770.0), (550.0, -770.0))):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik",
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", 4, "paslanmaz · taban Ø40", "elesa-ganter.com LV.A-SST") if i == 0 else None)
    zk = Z_KABUK_ON                                                                    # v6: kabuğun ön kenarı +59 (kapak arkası) · v5: 0 / −1,5
    tsc = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, zk)
    for _k, (gx, gz, gr, _ri, _ro, _h) in GECIS.items():                              # 2. tur (denetçi K-8): bulaşık bağlantılarının rakorlu geçiş delikleri (makinenin arkasında)
        tsc = tsc.cut(sily(gx, gz, gr, Y_PLINT - 1.0, Y_PLINT + 4.0))
    ekle("taban_sac_3", tsc, "sac")
    # v6: plint_on (z −61,5…−60) KALKTI → onyuz_plint (z +17,5…+19) on_cerceve()'de
    ist = kut(SAC, W - SAC, H_B, H_B + 3.0, -D + SAC, zk)
    for x0, x1 in (CER_X_SOL, CER_X_SAG):                                              # ön çerçeve dikmeleri kesintisiz geçer: önden açık çentik (kaynakla birleşir)
        ist = ist.cut(kut(x0, x1, H_B - 1.0, H_B + 4.0, Z_CER[0], zk + 1.0))
    for x0 in (SAC, W - SAC - 30.0):                                                   # v6: arka köşe dikmeleri de çentikten geçer (v5: sac dikmenin içinden geçiyordu, 2 × 672 mm³)
        ist = ist.cut(kut(x0, x0 + 30.0, H_B - 1.0, H_B + 4.0, -D + SAC - 1.0, -D + SAC + 30.0))
    ekle("istasyon_tabani_3", ist, "sac")                                              # v6: hava_besleme_K deliği (x 200–260 · z −800…−760) KALKTI (hortum silindi)
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, zk), "kabuk")
    # sol yan: fırın bandı + ürün girişi (fırın bandı K'ya 15 mm girer) · v6: ön kenar +59, açıklık AYNI
    ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, zk).cut(kut(-1, SAC + 1, URUN_GIRISI[0], URUN_GIRISI[1], URUN_GIRISI[2], URUN_GIRISI[3])), "kabuk")
    ekle("sag_sac_E_penceresi", kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, zk).cut(kut(W - SAC - 1, W + 1, E_PENCERE[0], E_PENCERE[1], E_PENCERE[2], E_PENCERE[3])), "kabuk")
    # köşe dikmeleri 30 × 30 × 2: v6 yalnız ARKA iki dikme (2, 3) — öndeki kesik dikmeler (0, 1) KALKTI, yerine kesintisiz ön çerçeve dikmeleri (on_cerceve)
    for i, (x0, z0) in ((2, (SAC, -D + SAC)), (3, (W - SAC - 30.0, -D + SAC))):
        dik = kut(x0, x0 + 30.0, Y_PLINT + 3.0, H - SAC, z0, z0 + 30.0).cut(kut(x0 + 2, x0 + 28, Y_PLINT + 2, H, z0 + 2, z0 + 28))
        ekle("kose_dikmesi_%d" % i, dik, "sac", bom=("Kare profil 30 × 30 × 2 AISI 304 (arka köşe dikmesi)", 2, "boy %.1f" % (H - SAC - Y_PLINT - 3.0), "lazer + kaynak") if i == 2 else None)
    on_cerceve()


def _profil(x0, x1, y0, y1, z0, z1, eksen, t=2.0):
    """kutu profil (et t) · eksen 'y' dikey, 'x' yatay · uçları açık (kaynakla kapanır)"""
    if eksen == "y":
        return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def on_cerceve():
    """v6 · ön çerçeve (SPEC §2.5): 2 kesintisiz dikme (y 126–1860,5 · z +27…+57) + 4 kayıt (yatay derzlerin arkasında) · plint +17,5…+19"""
    ekle("onyuz_cerceve_dikme_sol", _profil(CER_X_SOL[0], CER_X_SOL[1], Y_CER[0], Y_CER[1], Z_CER[0], Z_CER[1], "y"), "sac",
         bom=("Ön çerçeve dikmesi · kare profil 30 × 30 × 2 AISI 304", 1, "boy %.1f · kesintisiz · sol gizli menteşeler + köprü uç plakası buna" % (Y_CER[1] - Y_CER[0]),
              "üretim · taban sacı + üst sac + yan saca kaynak"))
    ekle("onyuz_cerceve_dikme_sag", _profil(CER_X_SAG[0], CER_X_SAG[1], Y_CER[0], Y_CER[1], Z_CER[0], Z_CER[1], "y"), "sac",
         bom=("Ön çerçeve dikmesi · bükme kutu 28,5 × 30 × 2 AISI 304", 1, "boy %.1f · kesintisiz · bas-aç mandallar + AZM40 + köprü uç plakası buna" % (Y_CER[1] - Y_CER[0]),
              "KARAR (varsayım): SPEC x 570–598,5 → standart 30 × 30 sığmaz; 2 mm sac bükülüp dikiş kaynaklı (bulaşık kapak zarfına 1,5 pay)"))
    for ad_, y0, y1 in KAYITLAR:
        ekle("onyuz_cerceve_kayit_%s" % ad_, _profil(CER_X_SOL[1], CER_X_SAG[0], y0, y1, Z_CER[0], Z_CER[1], "x"), "sac",
             bom=("Ön çerçeve kaydı · kare profil 30 × 30 × 2 AISI 304", len(KAYITLAR), "boy %.1f · derz çizgilerinin arkasında (126 · 883/886 · 1305/1308 · 1860)" % (CER_X_SAG[0] - CER_X_SOL[1]),
                  "üretim · dikmelere kaynak") if ad_ == "alt" else None)
    zp0, zp1 = Z_PLINT
    # 2. tur (denetçi K-4): SPEC §1 y 0–123 (v6-1 10–123) · x 0–600 (v6-1 30–570; E v7 plinti x 0'dan başlar "K ile birleşir" → K + E tek çizgi) ·
    # yan dönüşler TAM DERİNLİK (store_cad_v8 gibi −828,5; v6-1 58 idi — K'nin altı yandan açıktı) · yan sacların altında, ayaklara değmez (ayak tabanı x 30–70 / 530–570)
    pl = kut(0.0, W, 0.0, Y_PLINT, zp0, zp1)
    for xd in (0.0, W - TAVA_T):
        pl = pl.union(kut(xd, xd + TAVA_T, 0.0, Y_PLINT, -D + SAC, zp0))
    pl = pl.union(kut(TAVA_T, W - TAVA_T, Y_PLINT - TAVA_T, Y_PLINT, zp0 - PLINT_FLANS, zp0))       # üst flanş 15: taban sacının altına M5 perçin somunla
    ekle("onyuz_plint", pl, "sac", bom=("Plint 304 fırçalı 1,5 · tam derinlik yan dönüşlü + üst flanşlı", 1,
                                        "600 × 123 · ön yüz z +19 (ön düzlemin 60 gerisi) · yan dönüşler x 0 / 598,5 → z −828,5 · üst flanş %.0f" % PLINT_FLANS,
                                        "v6 · flanş taban sacına M5 perçin somunla (sökülebilir) · E v7 plintiyle x 600'de birleşir"))


def _yarik_x():
    """SEÇENEK yarık deseninin sol kenarları · desen kapak üzerinde ORTALI (2. tur: v6-1 x0 40 → sol pay 37 / sağ 45,5)"""
    n, a, e = YARIK["n"], YARIK["adim"], YARIK["en"]
    x0 = (KAPAK_X[0] + KAPAK_X[1]) / 2.0 - ((n - 1) * a + e) / 2.0
    return [x0 + i * a for i in range(n)]


def _yarik(ad_):
    """SEÇENEK · lazer yarık bandı (havalandırma): dikey yarıklar 3 × 40, adım 10 · yalnız ön sacı keser → (bileşik katı, yarık sayısı)"""
    ss = [cq.Solid.makeBox(YARIK["en"], yb - ya, TAVA_T + 2.0, cq.Vector(x, ya, Z_ON - TAVA_T - 1.0)) for ya, yb in YARIK["bant"][ad_] for x in _yarik_x()]
    return cq.Compound.makeCompound(ss), len(ss)


def _tava(y0, y1):
    x0, x1 = KAPAK_X; z0, z1 = Z_TAVA; t = TAVA_T
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 - t))


def kapaklar():
    """v6 · ÖN KAPAKLAR (SPEC §2.5) — tava panel 304 fırçalı 1,5, kenarlar 20 arkaya bükülü (z +59…+79), x 3–598,5 (dünya 4003–4598,5):
    ALT (bulaşık) y 126–883 · ORTA y 886–1305 · ÜST y 1308–1859 · SOL gizli menteşe (EMKA 1046-U5, sanal pivot x 3 z 79, en çok 90°) ·
    bas-aç mandal (Southco E4, sağ dikmede; strok = kapak arkası 59 ↔ çerçeve 57) · ORTA + ÜST: Schmersal AZM40 emniyet kilidi (gizli, dil ağıza 8 mm girer) ·
    ALT: iç yüzde EPDM dayama lastiği (bulaşık kapağı kilitte buna dayanır) · önden YALNIZ düz yüzey + derz (SPEC §1) — lazer yarık yalnız SEÇENEK (YARIK_ACIK) ·
    panel < 600 geniş → omega takviye YOK (SPEC kuralı)"""
    x0, x1 = KAPAK_X; z0, z1 = Z_TAVA; t = TAVA_T
    mx0, mx1 = MENTESE["x"]; ml = MENTESE["boy"]
    for g, ad_, y0, y1 in KAPAKLAR:
        w = _tava(y0, y1)
        ny = 0
        if YARIK_ACIK and ad_ in YARIK["bant"]:                                         # 2. tur: varsayılan KAPALI (SPEC) — seçenek
            yk, ny = _yarik(ad_)
            w = w.cut(yk)
        kg = w.val().Volume() * RHO_304
        ekle("onyuz_kapak_%s" % ad_, w, "sac", g,
             bom=("Ön kapak %s · tava panel 304 fırçalı 1,5 · kenarlar 20 büküm" % ad_.upper(), 1,
                  "%.1f × %.1f · %.1f kg · 2 gizli menteşe + bas-aç%s%s" % (x1 - x0, y1 - y0, kg, " + AZM40 kilit" if ad_ in AZM_KAPAK else "",
                                                                             " · %d lazer yarık 3 × 40 (havalandırma)" % ny if ny else ""),
                  "lazer + abkant · köşeler kaynaklı taşlanmış · derz 3 · önden yalnız düz yüzey"))
        for j, ym in enumerate(MENTESE_Y[ad_]):
            ekle("onyuz_mentese_govde_%s_%d" % (ad_, j), kut(mx0, mx1, ym - ml / 2.0, ym + ml / 2.0, Z_CER[1], z0), "celik",
                 bom=("Gizli menteşe EMKA 1046-U5 (AISI 304 · 90° · kaynaklı · katalog 4B-130)", 6,
                      "boy ≈ 79 · pim Ø16 (GlobalSpec) · çerçeve kanadı sol dikmeye, kapak kanadı kapak içine kaynak",
                      "emka.com/products/1046-u5 · sanal pivot (kapak ön-sol köşesi) + kanat ölçüleri VARSAYIM — üreticiden teyit") if (ad_, j) == ("alt", 0) else None)
            ekle("onyuz_mentese_kanat_%s_%d" % (ad_, j), kut(mx0, mx1, ym - ml / 2.0, ym + ml / 2.0, z0, z1 - t), "celik", g)
        ym = (y0 + y1) / 2.0
        ekle("onyuz_basac_mandal_%s" % ad_, kut(MANDAL["x"][0], MANDAL["x"][1], ym - MANDAL["boy"] / 2.0, ym + MANDAL["boy"] / 2.0, Z_CER[1], Z_CER[1] + MANDAL["derin"]), "plastik",
             bom=("Dokun-aç mandal Southco E4 (touch latch, gizli)", 3, "sağ çerçeve dikmesinin ön yüzüne · strok 2 (kapak arkası 59 ↔ çerçeve 57)",
                  "southco.com E4 touch latches (ör. E4-10-201-10) · gövde ölçüsü VARSAYIM 14 × 44 × 14") if ad_ == "alt" else None)
        ekle("onyuz_basac_karsilik_%s" % ad_, kut(MANDAL["x"][0], MANDAL["x"][1], ym - MANDAL["boy"] / 2.0, ym + MANDAL["boy"] / 2.0, Z_CER[1] + MANDAL["derin"], z1 - t), "celik", g)
        if ad_ in AZM_KAPAK:
            xa = CER_X_SAG[0]
            azm = kut(xa - AZM["kal"], xa, ym - AZM["boy"] / 2.0, ym + AZM["boy"] / 2.0, Z_CER[1] - AZM["en"], Z_CER[1]).cut(
                kut(xa - AZM["kal"] + 1.0, xa - 1.0, ym - 16.0, ym + 16.0, Z_CER[1] - AZM_AGIZ, Z_CER[1] + 1.0))              # 2. tur: dil giriş ağzı 18 × 32 × 8 (VARSAYIM)
            ekle("onyuz_kilit_AZM40_%s" % ad_, azm, "sari",
                 bom=("Emniyet kilidi Schmersal AZM40 (solenoid, RFID kodlu, IP69) — SPEC'te YOK, Kemal onayı gerekir", 2,
                      "119,5 × 40 × 20 · 2000 N kilitleme · PLe · sağ dikmenin iç yüzüne · dil ağıza 8 mm girer",
                      "schmersal.com/en/azm40 · ORTA (bıçak + itici) + ÜST (kılavuz mili uçları, tank, pano) · PNOZ s3'e · ağız yeri Schmersal çizimiyle teyit") if ad_ == "orta" else None)
            ekle("onyuz_kilit_dili_%s" % ad_, kut(xa - AZM["kal"] + 2.0, xa - 2.0, ym - 15.0, ym + 15.0, Z_CER[1] - AZM_AGIZ, z1 - t), "celik", g)   # 2. tur: z 49 (ağız dibi) … 77,5 (v6-1: 59,5'te bitiyordu)
        if ad_ == "alt":                                                                # 2. tur (denetçi K-11): bulaşık kapağının kilitte dayandığı yer — 1,5 sac yerine EPDM
            ekle("onyuz_dayama_lastigi_alt", kut(DAYAMA["x"][0], DAYAMA["x"][1], DAYAMA["y"][0], DAYAMA["y"][1], z1 - t - DAYAMA["t"], z1 - t), "conta", g,
                 bom=("Dayama lastiği EPDM 3 × 30 (yapışkanlı şerit)", 1, "460 × 30 × 3 · ALT kapağın iç yüzüne · bulaşık kapağının üst kenarı kilitte buna dayanır",
                      "VARSAYIM ölçü · genel katalog EPDM şerit (parça no yok)"))


''')

# ================================================================ 4 · BANT · KESİCİ · SPREY · İTİCİ · ELEKTRİK ================================================================
d('    ekle("olu_plaka", kut(587.0, 597.0, BANT - 6.0, BANT, -380.0, -30.0), "sac")',
  '    ekle("olu_plaka", kut(587.0, 597.0, BANT - 6.0, BANT, z0 - 2.0, z1 + 2.0), "sac",                          # v6: iki bant yan levhasına kadar (v5 −380…−30 havada)' + NL +
  '         bom=("Ölü plaka 10 mm AISI 304 (bant sonu → E köprüsü)", 1, "10 × 6 × 404", "v6: iki yan levhaya M5 × 2"))')
d('''        ekle("kopru_kirisi_%d" % i, kut(SAC + 1.0, W - SAC - 1.0, Y_KIRIS[0], Y_KIRIS[1], za, zb).cut(kut(SAC, W - SAC, Y_KIRIS[0] + 2, Y_KIRIS[1] - 2, za + 2, zb - 2)), "sac",
             bom=("Kare profil 40 × 40 × 2 AISI 304 (köprü)", 2, "boy 595", "üretim") if i == 0 else None)
''', '''        ekle("kopru_kirisi_%d" % i, kut(SAC + UC_T, W - SAC - UC_T, Y_KIRIS[0], Y_KIRIS[1], za, zb).cut(kut(SAC, W - SAC, Y_KIRIS[0] + 2, Y_KIRIS[1] - 2, za + 2, zb - 2)), "sac",
             bom=("Kare profil 40 × 40 × 2 AISI 304 (köprü)", 2, "boy %.0f · v6: uçları 8 mm uç plakalarına kaynaklı" % (W - 2 * SAC - 2 * UC_T), "üretim") if i == 0 else None)
    for i, (x0, x1) in enumerate(((SAC, SAC + UC_T), (W - SAC - UC_T, W - SAC))):            # v6: köprü yan saclara + ön çerçeve dikmesine bağlanır (v5: 1 mm HAVADA — KRİTİK)
        ekle("kopru_kirisi_uc_plakasi_%d" % i, kut(x0, x1, UC_Y[0], UC_Y[1], UC_Z[0], UC_Z[1]), "sac",
             bom=("Köprü uç plakası 8 mm AISI 304", 2, "%.0f × %.0f · yan saca 6 × M6 perçin somun + ön çerçeve dikmesine kaynak" % (UC_Y[1] - UC_Y[0], UC_Z[1] - UC_Z[0]),
                  "v6 · 1870 N kesme tepkisi → yan sac + ön dikme") if i == 0 else None)
''')
d(".cut(silx(yp, ZC, 19.2, 329.0, 396.0))", ".cut(silx(yp, ZC, 19.0, 329.0, 396.0))")            # v6: ceket PulsaJet'e değer (v5: 0,2 boşluk)
d('''    ekle("isitmali_hortum_kafa", boru([(405.0, yp, ZC), (440.0, yp, ZC), (440.0, Y_ON_PL[1] + 35.0, ZC)], 5.0), "hortum_isi", "KESICI")
''', '''    ekle("isitmali_hortum_kafa", boru([(405.0, yp, ZC), (440.0, yp, ZC), (440.0, Y_ON_PL[1] + 35.0, ZC)], 5.0), "hortum_isi", "KESICI")
    # v6 · havada kalmasın: PulsaJet kafa plakasına semerle · DGRF-C milleri gövdeye burçla (DGRF-C'nin iç kılavuz burçları — kayar geçme, idealleştirilmiş temas)
    ekle("PulsaJet_semeri", kut(309.0, 327.0, Y_KAFA[1], yp, ZC - 14.0, ZC + 14.0).cut(silx(yp, ZC, 19.0, 308.0, 328.0)), "sac", "KESICI",
         bom=("Sprey nozülü semeri 304 (kafa plakasına 2 × M5)", 1, "18 × 25 × 28 · R19 oturma", "v6: PulsaJet + nozül grubu havada kalmasın"))
    for i, x in enumerate((245.0, 300.0, 355.0)):
        ekle("DGRF_burcu_%d" % i, sily(x, ZC, 11.0, Y_GOVDE[0], Y_GOVDE[1]).cut(sily(x, ZC, 10.0, Y_GOVDE[0] - 1, Y_GOVDE[1] + 1)), "celik")
''')
d(".cut(sily(x, z, r + 0.2, y0, y1)), \"hortum_isi\",", ".cut(sily(x, z, r, y0, y1)), \"hortum_isi\",")      # v6: ceket tanka değer
d('''    ekle("yag_tanki_rafi", kut(34.0, 290.0, y0 - 5.0, y0, -760.0, -380.0), "sac", bom=("Tank rafı 304 · 5 mm", 1, "256 × 380", "v3: sol duvara köşebentle · hava besleme hortumunun (z −800) önünde biter"))
    ekle("yag_tanki_rafi_koseben", kut(2.0, 34.0, y0 - 35.0, y0 - 5.0, -760.0, -380.0).cut(kut(5.0, 35.0, y0 - 36.0, y0 - 8.0, -761.0, -379.0)), "sac",
         bom=("Köşebent 30 × 30 × 3 AISI 304 (tank rafı)", 1, "boy 380", "sol duvara M6 × 3"))''',
  '''    ekle("yag_tanki_rafi", kut(SAC + 3.0, 290.0, y0 - 5.0, y0, -760.0, -380.0), "sac", bom=("Tank rafı 304 · 5 mm", 1, "285,5 × 380", "v6: köşebendin üst kanadına oturur (v5: 34'ten başlıyordu)"))
    ekle("yag_tanki_rafi_koseben", kut(SAC, 34.0, y0 - 35.0, y0 - 5.0, -760.0, -380.0).cut(kut(SAC + 3.0, 35.0, y0 - 36.0, y0 - 8.0, -761.0, -379.0)), "sac",
         bom=("Köşebent 30 × 30 × 3 AISI 304 (tank rafı)", 1, "boy 380", "sol duvara M6 × 3 · v6: duvara değer (v5: 0,5 boşluk)"))''')
d('    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1827.0, z), (x + 45.0, 1827.0, -760.0), (x + 45.0, 1617.0, -760.0)], 3.0), "hava")',
  '    ekle("hava_hortumu_tank", boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1827.0, z), (x + 45.0, 1827.0, -775.0), (x + 45.0, 1612.0, -775.0)], 3.0), "hava")   # v6: valf adasının üstüne biter (v5: 8,6 boşluk)')
d('    kc(KC.e2e, "itici_home_sensoru", xa + 60.0, Y_EKSEN[1] + 10.0, Z_EKSEN[0] - 20.0, "x")' + NL,
  '    kc(KC.e2e, "itici_home_sensoru", xa + 60.0, Y_EKSEN[1] + 10.0, Z_EKSEN[0] - 20.0, "x")' + NL +
  '    ekle("itici_home_braketi", kut(78.0, 104.0, 960.0, 1000.0, -513.0, -509.0).union(kut(78.0, 104.0, 960.0, 964.0, -509.0, Z_EKSEN[0])), "sac",   # v6: sensör havada kalmasın' + NL +
  '         bom=("Sensör L braketi 304 · 4 mm (home sensörü eksen profiline)", 1, "26 × 40 × 28", "v6"))' + NL)
d('    ekle("pano_plakasi", kut(300.0, 565.0, 1472.0, 1857.0, -826.0, -822.0), "sac")' + NL,
  '    ekle("pano_plakasi", kut(300.0, 565.0, 1472.0, 1857.0, -826.0, -822.0), "sac")' + NL +
  '    for i, (bx, by) in enumerate(((315.0, 1487.0), (550.0, 1487.0), (315.0, 1842.0), (550.0, 1842.0))):   # v6: pano plakası arka saca 4 ara burçla (v5: 2,5 mm havada)' + NL +
  '        ekle("pano_ara_burcu_%d" % i, silz(bx, by, 5.0, -D + SAC, -826.0), "celik", bom=("Ara burç M5 × 2,5 paslanmaz (pano plakası)", 4, "", "katalog") if i == 0 else None)' + NL)
d('bom=("Emniyet rölesi Pilz PNOZ s3", 1, "kapı kilidi + acil stop", "[V] pilz.com"))',
  'bom=("Emniyet rölesi Pilz PNOZ s3", 1, "v6: 2 × AZM40 kapak kilidi (ORTA + ÜST) + hat acil stop zinciri [AÇIK: acil stop yeri]", "[V] pilz.com"))')
d('''         bom=("Valf adası Festo VUVG-L10 · 4 × 5/2 (kesici · itici kaldırma · tank basıncı · yedek)", 1, "24 V", "[V] festo.com VUVG"))
''', '''         bom=("Valf adası Festo VUVG-L10 · 4 × 5/2 (kesici · itici kaldırma · tank basıncı · yedek)", 1, "24 V", "[V] festo.com VUVG"))
    ekle("sartlandirici_montaj_saci", kut(55.0, 255.0, 1527.0, 1697.0, -D + SAC, -826.0), "sac",                      # v6: MS4 + valf adası arka saca (v5: 2,5 mm havada)
         bom=("Montaj sacı 2,5 · 304 (MS4 + valf adası)", 1, "200 × 170", "v6: arka saca 4 × M5 · MS4 ve VUVG buna vidalı"))
''')
d('''    ekle("hava_besleme_K", boru([(230.0, H_B - 20.0, -790.0), (230.0, H_B + 3.0, -790.0), (230.0, 1332.0, -790.0), (85.0, 1332.0, -800.0), (85.0, 1532.0, -800.0)], 5.0), "hava",
         bom=("PU hava hortumu Ø10 · kompresör hattından T ile", 1, "≈ 1 m", "katalog"))
''', '''    # v6: hava_besleme_K SİLİNDİ (SPEC §2.5: MS4 zaten üstten ANA_K48 ile besleniyor — çift besleme) + istasyon tabanındaki deliği
''')
d('    ekle("hava_hortumu_kaldirma", boru([(160.0, 1552.0, -765.0), (160.0, 1152.0, -765.0), (160.0, 1152.0, -470.0)], 3.0), "hava")',
  '    ekle("hava_hortumu_kaldirma", boru([(160.0, 1582.0, -770.0), (160.0, 1582.0, -765.0), (160.0, 1152.0, -765.0), (160.0, 1152.0, -470.0)], 3.0), "hava")   # v6: valfin ön yüzünden çıkar · MGPM\'e spiral hortum AÇIK')
d('''             bom=("Fotosel Omron E3Z-D62 (dağınık yansımalı)", 2, "ürün merkezde · bant sonu", "omron.com E3Z") if x_ < 500 else None)
''', '''             bom=("Fotosel Omron E3Z-D62 (dağınık yansımalı)", 2, "ürün merkezde · bant sonu", "omron.com E3Z") if x_ < 500 else None)
        ekle("sensor_braketi_" + ad_[7:], kut(x_ - 10.0, x_ + 10.0, BANT - BANT_K - 0.5, BANT + 2.0, BANT_Z[0] - 18.0, BANT_Z[0] - 2.0), "sac",   # v6: bant yan levhasına (v5: 4,5 havada)
             bom=("Sensör braketi 304 (bant yan levhasına)", 2, "20 × 4,5 × 16", "v6") if x_ < 500 else None)
''')
d('        ekle("kesici_reed_%d" % i, kut(376.0, 384.0, y, y + 20.0, ZC - 10.0, ZC + 10.0), "sensor",',
  '        ekle("kesici_reed_%d" % i, kut(375.0, 383.0, y, y + 20.0, ZC - 10.0, ZC + 10.0), "sensor",                # v6: gövdeye değer (v5: 1 mm)')

# ---- 4b · 2. TUR (denetçi ORTA-1 + K-9): İSTİSNA LİSTESİNİN GİZLEDİĞİ ÖRTÜŞMELER — gerçek çakışma taşındı, gömülü geçmeler delik / yuva ile modellendi ----
d('    ekle("kablo_kanali_dikey", kut(566.0, 591.0, H_B + 3.0, 1827.0, -822.0, -797.0), "plastik")',
  '    ekle("kablo_kanali_dikey", kut(566.0, 591.0, H_B + 3.0, 1827.0, -D + SAC + 30.0, -D + SAC + 55.0), "plastik")   # 2. tur: arka köşe dikmesinin ÖNÜNE (z −798,5…−773,5) — v5/v6-1 dikmenin içinden geçiyordu (82 016 mm³, ISTISNA gizliyordu)')
d('    ekle("yag_tanki_kelepcesi", sily(x, z, r + 10.0, y1 - 6.0, y1 + 4.0).cut(sily(x, z, r + 1.0, y1 - 7.0, y1 + 5.0)), "celik")',
  '    ekle("yag_tanki_kelepcesi", sily(x, z, r + 10.0, y1 - 6.0, y1 + 4.0).cut(sily(x, z, r, y1 - 7.0, y1 + 5.0)).cut(sily(x, z, r + 8.0, y1, y1 + 5.0)), "celik")   # 2. tur: basamaklı iç yüz — tanka r 80, kapağa r 88 değer (v6-1: kapağın içinden, 14 866 mm³)')
d('        ekle("eksen_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, Y_EKSEN[0], Z_EKSEN[0] + 5.0, Z_EKSEN[1] - 5.0), "sac")',
  '        ekle("eksen_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, Y_EKSEN[0], Z_EKSEN[0] + 5.0, Z_EKSEN[1] - 5.0).cut(                    # 2. tur: uç bloğunun ALTINDA basamaklı (v6-1: bloğa 5 mm giriyordu, 1 500 mm³)' + NL +
  '             kut(xa, xa + 55.0, Y_EKSEN[0] - 5.0, Y_EKSEN[1] + 5.0, Z_EKSEN[0] - 5.0, Z_EKSEN[1] + 5.0)).cut(kut(xb - 55.0, xb, Y_EKSEN[0] - 5.0, Y_EKSEN[1] + 5.0, Z_EKSEN[0] - 5.0, Z_EKSEN[1] + 5.0)), "sac")')
d('        ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, BANT - 64.0, BANT - BANT_K - 0.5, a, b), "sac",',
  '        ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, BANT - 64.0, BANT - BANT_K - 0.5, a, b).cut(silz(X_TAHRIK, Y_TAHRIK, 6.0, a - 1.0, b + 1.0)).cut(   # 2. tur: mil yatak delikleri + gergi yarığı' + NL +
  '             silz(X_KUYRUK, Y_KUYRUK, 4.0, a - 1.0, b + 1.0)).cut(silx(Y_KUYRUK - 10.0, (a + b) / 2.0, 3.0, X_KUYRUK, X_KUYRUK + 40.0)), "sac",')
d('    ekle("tahrik_rulosu_RollerDrive_EC5000", silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 2.0, z1 + 2.0), "aluminyum", "SABIT",',
  '    ekle("tahrik_rulosu_RollerDrive_EC5000", silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 2.0, z1 + 2.0).cut(silz(X_TAHRIK, Y_TAHRIK, 6.0, z0 - 3.0, z1 + 3.0)), "aluminyum", "SABIT",   # 2. tur: mil yuvası (içi dolu modeldi)')
d('    ekle("kuyruk_rulosu", silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 + 2.0, z1 - 2.0), "aluminyum",',
  '    ekle("kuyruk_rulosu", silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 + 2.0, z1 - 2.0).cut(silz(X_KUYRUK, Y_KUYRUK, 4.0, z0 + 1.0, z1 - 1.0)), "aluminyum",   # 2. tur: mil yuvası')
d('    ekle("bant_PU_2mm", ust.union(alt).union(sarim_t).union(sarim_k), "pu_bant",',
  '    ekle("bant_PU_2mm", ust.union(alt).union(sarim_t).union(sarim_k).cut(silz(X_TAHRIK, Y_TAHRIK, R_TAHRIK, z0 - 1.0, z1 + 1.0)).cut(silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 - 1.0, z1 + 1.0)),   # 2. tur: alt kolun rulo içine giren şeridi (9,3 mm³)' + NL +
  '         "pu_bant",')
d('    ekle("sprey_dirsegi", kut(292.0, 306.0, Y_KAFA[1], yp + 8.0, ZC - 7.0, ZC + 7.0), "celik", "KESICI")',
  '    ekle("sprey_dirsegi", kut(292.0, 306.0, Y_KAFA[1], yp + 8.0, ZC - 7.0, ZC + 7.0).cut(silx(yp, ZC, 19.0, 305.0, 405.0)), "celik", "KESICI")   # 2. tur: PulsaJet ucuna oturur (v6-1: 1 mm içindeydi, 372 mm³)')
d('    ekle("bicak_gobek_halkasi", sily(XC, ZC, 20.0, Y_GOBEK - 12.0, Y_GOBEK).cut(sily(XC, ZC, 13.0, Y_GOBEK - 13.0, Y_GOBEK + 1.0)), "celik", "KESICI")',
  '    gob = sily(XC, ZC, 20.0, Y_GOBEK - 12.0, Y_GOBEK).cut(sily(XC, ZC, 13.0, Y_GOBEK - 13.0, Y_GOBEK + 1.0))' + NL +
  '    for i in range(6):                                                                     # 2. tur: bıçak kökleri göbekteki yuvalara oturur (v6-1: 6 × 90 mm³ gömülü)' + NL +
  '        gob = gob.cut(radyal(BICAK_R0, BICAK_R1, BICAK_T, Y_AGIZ_UST, Y_GOBEK, 60.0 * i))' + NL +
  '    ekle("bicak_gobek_halkasi", gob, "celik", "KESICI")')
d('        ekle("koruma_braketi_%d" % i, radyal(110.0, KORUMA_R[1], 12.0, Y_KAFA[0], Y_KAFA[1], phi), "sac", "KESICI")',
  '        ekle("koruma_braketi_%d" % i, radyal(110.0, KORUMA_R[1], 12.0, Y_KAFA[0], Y_KAFA[1], phi).cut(sily(XC, ZC, 115.0, Y_KAFA[0] - 1.0, Y_KAFA[1] + 1.0)), "sac", "KESICI")   # 2. tur: kafa plakası kenarına alın kaynak (v6-1: 5 mm gömülü)')
d('    ekle("surucu_STP-DRV-4830", TC.din_parca(TC.SURUCU_STEP, 450.0, 1692.0, zd + 28.0), "kart",',
  '    ekle("surucu_STP-DRV-4830", _kati_kes(TC.din_parca(TC.SURUCU_STEP, 450.0, 1692.0, zd + 28.0), kut(305.0, 560.0, 1692.0, 1727.0, -822.0, -815.0)), "kart",   # 2. tur: DIN klipsinin raya giren kısmı (11,6 mm³) — klips rayın flanşına değer')
d('MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))' + NL,
  'MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))' + NL +
  'MALZEME.setdefault("conta", dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8))     # v6 2. tur: EPDM dayama lastiği / geçiş lastikleri (store / kutu ile aynı anahtar)' + NL)

# ================================================================ 5 · BULAŞIK (v2) + TABLA ================================================================
d("# solunda önde 77, dikmenin arkasında 107 BOŞ · makinenin bağlantıları (y ≤ 310) altta kalır." + NL,
  "# solunda önde 77, dikmenin arkasında 107 BOŞ · makinenin bağlantıları (y ≤ 310) altta kalır." + NL +
  '# v6 (SPEC_on_duzlem_v63 · Kemal: "bulaşık makinesi önüne kapak, alt ayaklarını kaldır"): bulasik_cad_v2 AYAKSIZ → 2 × 40×20×2 tabla kirişi (yan saclara' + NL +
  "#    kaynaklı, K taban sacına oturur) + 3 mm tava · makine +13 (gövde altı 149) · önünde ALT kapak (y 126–883, SOL menteşe) · bulaşık kapağı ancak ALT kapak açıkken açılır." + NL)
blok("X_K_HAT = 4000.0", "def bulasik_parcalari():", r'''X_K_HAT = 4000.0                                   # K modülünün hattaki x'i (yerel x = dünya − 4000)
TABLA_KIRIS = (40.0, 20.0, 2.0)                    # v6: bulaşık tabla kirişi 40 × 20 × 2 (z × y × et) · yan saclara kaynaklı, K taban sacının üstünde
TAVA_BM = 3.0                                      # v6: tabla tavası 3 mm (makine buna oturur)
Y_TABLA = Y_PLINT + 3.0 + TABLA_KIRIS[1] + TAVA_BM  # 149 = makinenin gövde altı (v5: ayaklar 126'da, gövde 136'da → makine +13)
BULASIK_YER = (4108.5, Y_TABLA - BM.TABAN, -20.0)  # (4108,5 · 139 · −20) bulasik_cad_v2 (X0, Y0, Z0) dünya kökü = kapak ön yüzü — montaj AYNISINI kullanmalı · v6: gövde altı Y0 + 10 = 149 = tava üstü
# denetçi düzeltmesi: kök z −12 değil −20 → makinenin TAMAMI (ışıklı kulp 8 + gövde 600 + arka bağlantılar 25 = 633) SPEC / Resim 1 v4 B–B'deki z −12…−645'e oturur
BULASIK_ZARF = dict(x=(BULASIK_YER[0] - X_K_HAT, BULASIK_YER[0] - X_K_HAT + BM.W), y=(Y_TABLA, BULASIK_YER[1] + BM.H),
                    z=(BULASIK_YER[2] - BM.D - 25.0, BULASIK_YER[2] + 8.0))    # K yereli 108,5–568,5 × 149–839 × −645…−12 (v6: tava üstünden · SPEC: 633 derin = kulp 8 + gövde 600 + arka bağlantılar 25)
BULASIK_ARKA_PAY = (-670.0, -645.0)                # MEIKO föyü: arkada duvar payı 25 — BOŞ (yalnız makinenin arka bağlantı hortumları geçer)
BULASIK_BAGLANTI_UST = 323.0                       # v6: makinenin arka bağlantıları yerden: tahliye 165 + Y0 139 + yarıçap 15 = 319 ≤ 323 (v5 310 + 13, makine +13)
# 2. tur (denetçi K-8): bulaşık bağlantılarının K'den ÇIKIŞI — taban sacında (makinenin arkasındaki 158,5 mm'lik boşlukta, z −750) rakorlu geçiş:
# hortum / kablo bağlantı ucundan (z −645) aşağı iner → taban sacı → plint boşluğu (arkası açık) → duvar / yer gideri. Arka sac TAM kalır (duvara dayalı, rakor çıkıntısı z −830'u aşardı).
# (x K yereli, z, delik r, rakor iç r, flanş dış r, üst yükseklik) — x = bağlantının x'i (föy: soldan 40 / 186 / 313)
GECIS_Z = -750.0
GECIS = {"elektrik": (BULASIK_YER[0] - X_K_HAT + BM.BAG["elektrik"][0], GECIS_Z, 10.25, 4.5, 12.0, 18.0),     # Lapp SKINTOP MS-M 20×1,5 (sıkma 7–13) · delik Ø20,5
         "tahliye": (BULASIK_YER[0] - X_K_HAT + BM.BAG["tahliye"][0], GECIS_Z, 25.0, 20.0, 30.0, 3.0),        # EPDM geçiş lastiği, Ø40 tahliye hortumu · delik Ø50 (VARSAYIM)
         "su": (BULASIK_YER[0] - X_K_HAT + BM.BAG["su"][0], GECIS_Z, 17.5, 13.0, 22.5, 3.0)}                  # EPDM geçiş lastiği, ¾" su hortumu (dış Ø26) · delik Ø35 (VARSAYIM)


''')
d("    \"\"\"bulasik_cad_v1'in katıları montajdaki yerinde (BULASIK_YER), K yerelinde · + kapak açık zarfı (K yereli).",
  "    \"\"\"bulasik_cad_v2'nin (v6; v5: v1) katıları montajdaki yerinde (BULASIK_YER), K yerelinde · + kapak açık zarfı (K yereli).")
blok("def taban():", "# ---------------------------------------------------------------- 8 · ÜRÜN + REFERANSLAR", r'''def taban():
    """v4 · ALÇAK HAT: K tabanının altı — bulaşık makinesi REF (ayrı modül) · v5: kanister rafı + deterjan / parlatıcı + dozaj hortumları KALKTI (Kemal) ·
    v6: bulaşık TABLASI (Kemal: "alt ayaklarını kaldır") — 2 × 40×20×2 kiriş (yan saclara kaynaklı, K taban sacına oturur) + 3 mm tava (makine buna oturur)"""
    for ad_, sh in bulasik_parcalari()[0]:
        ekle("REF_bulasik_" + ad_, cq.Workplane(obj=sh), "referans", "REF")
    yk0 = Y_PLINT + 3.0; kz, ky, kt = TABLA_KIRIS
    for i, zc in enumerate((BULASIK_YER[2] - 30.0, BULASIK_YER[2] - BM.D + 30.0)):          # makinenin eski ayak hatları (z −50 / −590): gövde köşeleri kirişin üstünde
        ekle("bulasik_tabla_kirisi_%d" % i, kut(SAC, W - SAC, yk0, yk0 + ky, zc - kz / 2.0, zc + kz / 2.0).cut(
             kut(SAC - 1.0, W - SAC + 1.0, yk0 + kt, yk0 + ky - kt, zc - kz / 2.0 + kt, zc + kz / 2.0 - kt)), "sac",
             bom=("Tabla kirişi · kutu profil 40 × 20 × 2 AISI 304", 2, "boy %.0f · yan saclara kaynaklı · K taban sacına oturur" % (W - 2 * SAC),
                  "v6 · makine köşeleri (eski ayak hattı z −50 / −590) kirişin üstünde") if i == 0 else None)
    xa, xb = BULASIK_YER[0] - X_K_HAT - 4.0, BULASIK_YER[0] - X_K_HAT + BM.W + 4.0
    za, zb = BULASIK_YER[2] - BM.D - 4.0, BULASIK_YER[2] + 4.0
    tv = kut(xa, xb, Y_TABLA - TAVA_BM, Y_TABLA, za, zb)
    for z0_, z1_ in ((zb - TAVA_BM, zb), (za, za + TAVA_BM)):                                  # ön + arka kenar 15 AŞAĞI bükülü (kirişlerin arasında kalır)
        tv = tv.union(kut(xa, xb, Y_TABLA - TAVA_BM - 15.0, Y_TABLA - TAVA_BM, z0_, z1_))
    ekle("bulasik_tavasi", tv, "sac", bom=("Bulaşık tabla tavası 3 mm AISI 304", 1, "%.0f × %.0f · ön + arka kenar 15 aşağı bükülü" % (xb - xa, zb - za),
                                          "v6 · MEIKO ayaksız buna oturur (+13) · kirişlere kaynak"))
    # 2. tur (denetçi K-8): bağlantı geçişleri — gövde delikte (y 123–126, delik duvarına değer) + üst başlık / flanş taban sacının üstünde
    # (alt dudak / kilit somunu plint boşluğunda ~2 mm — modelde yok: taban çizgisi 123'ün altında yalnız ayak + plint)
    for k_, (gx, gz, gr, ri, ro, hh) in GECIS.items():
        ad_ = ("bulasik_gecis_rakoru_" if k_ == "elektrik" else "bulasik_gecis_lastigi_") + k_
        sh = sily(gx, gz, gr, Y_PLINT, Y_PLINT + 3.0).union(sily(gx, gz, ro, Y_PLINT + 3.0, Y_PLINT + 3.0 + hh)).cut(sily(gx, gz, ri, Y_PLINT - 1.0, Y_PLINT + 4.0 + hh))
        ekle(ad_, sh, "siyah" if k_ == "elektrik" else "conta",
             bom=(("Kablo rakoru Lapp SKINTOP MS-M 20×1,5 (paslanmaz / pirinç, IP68)", 1, "bulaşık besleme kablosu (sıkma 7–13) · taban sacı delik Ø20,5 · kilit somunu altta",
                   "lappgroup.com SKINTOP MS-M · parça no teyit (ör. 53112020) · ölçü VARSAYIM") if k_ == "elektrik" else
                  ("Geçiş lastiği EPDM (grommet) · %s hortumu" % k_, 1, "delik Ø%.0f · iç Ø%.0f · flanş Ø%.0f" % (2 * gr, 2 * ri, 2 * ro),
                   "VARSAYIM ölçü · genel katalog (parça no yok)")))


''')

# ================================================================ 6 · MODÜL + KAPAK KİNEMATİĞİ ================================================================
d("    govde(); bant(); kesici(); sprey_sistemi(); itici(); elektrik(); taban(); urun_ref()",
  "    govde(); kapaklar(); bant(); kesici(); sprey_sistemi(); itici(); elektrik(); taban(); urun_ref()      # v6: kapaklar()")
d('''    if g in ("URUN", "URUN_IZ"): return urun_trs(t)
    return (0.0, 0.0, 0.0)
''', '''    if g in ("URUN", "URUN_IZ"): return urun_trs(t)
    return (0.0, 0.0, 0.0)


def kapak_ac(sh, aci):
    """v6 · kapak grubu katısı (Shape) → SOL gizli menteşenin sanal pivotu (x 3, z 79, dikey eksen) etrafında 'aci' derece AÇIK (öne-sola döner).
    Kapaklar yalnız servis içindir: çevrimde (grup_trs) KAPALI kalır."""
    x, z = MENTESE_EKSEN
    return sh.rotate(cq.Vector(x, 0.0, z), cq.Vector(x, 1.0, z), -aci)
''')

# ================================================================ 7 · DENETİM ================================================================
d('    print("DENETİM (kesme_cad_v5)")', '    print("DENETİM (kesme_cad_v6)")')
d('''        if b.xmin < -0.5 or b.xmax > W + 0.5 or b.ymin < -0.5 or b.ymax > H + 0.5 or b.zmin < -D - 0.5 or b.zmax > 0.5:
            tasan.append(p["ad"])
    kontrol("zarf %.0f × %.0f × %.0f içinde (kulp / acil stop hariç)" % (W, H, D), not tasan, ", ".join(tasan))''',
  '''        if b.xmin < -0.5 or b.xmax > W + 0.5 or b.ymin < -0.5 or b.ymax > H + 0.5 or b.zmin < -D - 0.5 or b.zmax > Z_ON + 0.5:
            tasan.append(p["ad"])
    kontrol("zarf %.0f × %.0f × (%.0f + %.0f) içinde: z −830…+79,5 (v6: ön düzlem +79 · kapaklar kapalı)" % (W, H, D, Z_ON), not tasan, ", ".join(tasan))''')
d('not p["ad"].startswith(("ayak_", "plint_on"))]', 'not p["ad"].startswith(("ayak_", "onyuz_plint"))]')
d("    denetim_v4(H_)" + NL + "    return H_", "    denetim_v6(H_)" + NL + "    return H_")
blok("def denetim_v4(H_):", "# ---------------------------------------------------------------- ÇAKIŞMA TARAMASI", r'''def _sek(ad):
    L = [p for p in PARCALAR if p["ad"] == ad]
    assert len(L) == 1, ad
    return L[0]["wp"].val()


def _mesafe(a, b):
    """gerçek katı aralığı (mm) · OCC BRepExtrema"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    sa = _sek(a) if isinstance(a, str) else a; sb = _sek(b) if isinstance(b, str) else b
    x = BRepExtrema_DistShapeShape(sa.wrapped, sb.wrapped)
    return x.Value() if x.IsDone() else 1e9


def isi_dT(Q, A, h, Cd=0.6, T=298.0):
    """doğal çekiş (baca etkisi) · alt + üst eşit açıklık seri (A_eff = A/√2) · Q = ρ·cp·ΔT·Cd·A_eff·√(2·g·h·ΔT/T) → ΔT [K]"""
    k = 1.2 * 1005.0 * Cd * (A / math.sqrt(2.0)) * math.sqrt(2.0 * 9.81 * h / T)
    return (Q / k) ** (2.0 / 3.0)


def denetim_v6(H_):
    """v6 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §2.5) — hepsi katılardan ölçülür:
    1 kotlar + E arayüzü · 2 v5 ↔ v6 parça parça (değişen / yeni / çıkan listeleri beklenenle birebir) · 3 kinematik v5 ile aynı ·
    4 ön düzlem +79 / kabuk +59 / plint / derz / tava · 5 yük yolu temasları · 6 kapaklar (kinematik + 0–90° tarama) ·
    7 bulaşık v2 (tabla, zarf, kapak açık zarfı ALT kapak AÇIKKEN) · 8 havada parça = 0 · 9 hesaplar (köprü, tabla, kapak, ısı VARSAYIM) · 10 açıklıklar"""
    import dilim_v1 as DL
    import kesme_cad_v5 as V5
    import denetim_temas_v1 as DT
    import firin_tp10_cad_v8 as FT8                                                    # 2. tur (denetçi K-13): güncel fırın sürümü (ZS 79 aynı)
    def kutu_(x, y, z):
        return cq.Solid.makeBox(x[1] - x[0], y[1] - y[0], z[1] - z[0], cq.Vector(x[0], y[0], z[0]))
    def giren(bolge, liste):
        L = []; B_ = bolge.BoundingBox()
        for p, sh in liste:
            if not KC._bb_kesisir(sh.BoundingBox(), B_): continue
            v = sh.intersect(bolge).Volume()
            if v > 0.01: L.append((p["ad"], round(v, 1)))
        return L
    # ---- 1 · kotlar + E arayüzü (v5 ile aynı) ----
    ts = bbx("istasyon_tabani_3"); ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "SABIT")
    H_["taban_ust"] = ts.ymax; H_["bant"] = bbx("bant_PU_2mm").ymax; H_["ust"] = ust
    kontrol("ALÇAK HAT kotları (v5 ile aynı): üst %.1f · istasyon tabanı sacı %.0f–%.0f · K bandı %.1f · fırın bandı %.0f · ürün girişi %.0f–%.0f"
            % (ust, ts.ymin, ts.ymax, H_["bant"], FIRIN_BANDI, URUN_GIRISI[0], URUN_GIRISI[1]),
            abs(ust - 1862.0) < 0.01 and abs(ts.ymin - 892.0) < 0.01 and abs(H_["bant"] - 996.0) < 0.01 and abs(FIRIN_BANDI - 998.0) < 0.01)
    kontrol("E arayüzü kutu_cad_v6: E plakası %.1f = K bandı %.1f · E penceresi %.0f–%.0f = K'deki · E kalıbı %.1f · tepsi %.0f" % (KC.PLAKA_K, BANT, KC.PENCERE[0], KC.PENCERE[1], KC.KALIP, KC.TEPSI),
            KC.__name__ == "kutu_cad_v6" and abs(KC.PLAKA_K - BANT) < 0.01 and all(abs(a - b) < 0.01 for a, b in zip(KC.PENCERE, E_PENCERE)))
    kontrol("ön düzlem sözleşmesi: Z_ON %.1f = firin_tp10_cad_v8.ZS %.1f (fırın gövdesinin ön yüzü, değişmez referans) · arka %.0f → derinlik %.0f" % (Z_ON, FT8.ZS, Z_ARKA, Z_ON - Z_ARKA),
            abs(Z_ON - FT8.ZS) < 1e-9 and abs(Z_ARKA + 830.0) < 1e-9)
    # 2. tur (denetçi K-13): E'nin montaj v63 sürümü kutu_cad_v7 — K'nin kullandığı arayüz sabitleri v6 ile AYNI mı (ürün × E v7 / itici × E v7 taraması __main__'de, e7_ileri)
    try:
        import kutu_cad_v7 as KC7
    except Exception as e_:
        KC7 = None; UYARI.append("E v7 (kutu_cad_v7) yüklenemedi: %s — ileri uyum denetlenemedi" % e_)
    if KC7 is not None:
        ARA_ = ("PLAKA_K", "PENCERE", "KALIP", "TEPSI", "T", "ZB", "Z_PIZZA")
        fk_ = [a_ for a_ in ARA_ if getattr(KC, a_) != getattr(KC7, a_)]
        H_["E_v7_arayuz"] = {a_: [getattr(KC, a_), getattr(KC7, a_)] for a_ in ARA_}
        kontrol("E ileri uyum (kutu_cad_v7 = montaj v63'ün E'si): %s kutu_cad_v6 ile AYNI → K'nin ürün yolu / itici arayüzü değişmez (ürün × E v7 + itici × E v7 taraması: __main__ e7_ileri)"
                % " · ".join(ARA_), not fk_, str(fk_))
    # ---- 2 · v5 ↔ v6 parça parça ----
    V5.modul()
    k = DL.karsilastir(PARCALAR, V5.PARCALAR)
    fark_ad = sorted(set(f.split(":")[0] for f in k["fark"]))
    yeni = sorted(k["yeni_ek"]); cikan = sorted(k["ref_eksik"])
    fark_k = [a for a in fark_ad if not a.startswith("REF_bulasik_")]
    fark_bm = [a for a in fark_ad if a.startswith("REF_bulasik_")]
    bm_ortak = sorted(p["ad"] for p in V5.PARCALAR if p["ad"].startswith("REF_bulasik_") and p["ad"] not in cikan)
    V5P = {p["ad"]: p["wp"].val() for p in V5.PARCALAR}
    dy = BULASIK_YER[1] - V5.BULASIK_YER[1]
    bm_kay = []
    for a in bm_ortak:                                                                 # bulaşık v1 → v2: ortak parçalar tam +13 y (filtre: + göbek deliği)
        b6, b5 = bbx(a), V5P[a].BoundingBox()
        ot = max(abs(b6.xmin - b5.xmin), abs(b6.xmax - b5.xmax), abs(b6.ymin - b5.ymin - dy), abs(b6.ymax - b5.ymax - dy), abs(b6.zmin - b5.zmin), abs(b6.zmax - b5.zmax))
        dv = _sek(a).Volume() - V5P[a].Volume()
        if ot > 0.01 or (abs(dv) > 0.5 and a != "REF_bulasik_miclean_filtre"): bm_kay.append((a, round(ot, 3), round(dv, 1)))
    yeni_x = [a for a in yeni if not a.startswith(YENI_V6)]
    H_["v5_v6"] = dict(v5=len(V5.PARCALAR), v6=len(PARCALAR), ayni=len(k["ayni"]), degisen=fark_ad, yeni=yeni, cikan=cikan, bulasik_dy=dy)
    kontrol("v5 ↔ v6 (dilim_v1.karsilastir: sınır kutusu ±0,01 + hacim): v5 %d → v6 %d parça · birebir %d · değişen %d (K %d + bulaşık REF %d, hepsi +%.0f y) · yeni %d · çıkan %d — listeler beklenenle birebir"
            % (len(V5.PARCALAR), len(PARCALAR), len(k["ayni"]), len(fark_ad), len(fark_k), len(fark_bm), dy, len(yeni), len(cikan)),
            fark_k == sorted(V6_DEGISEN) and cikan == sorted(V6_CIKAN) and not yeni_x and fark_bm == bm_ortak and not bm_kay and abs(dy - 13.0) < 0.01
            and len(k["ayni"]) == len(V5.PARCALAR) - len(cikan) - len(fark_ad),
            "değişen fazla %s eksik %s · çıkan %s · yeni tanımsız %s · bulaşık kayma %s" % (sorted(set(fark_k) - set(V6_DEGISEN)), sorted(set(V6_DEGISEN) - set(fark_k)), cikan, yeni_x, bm_kay))
    print("     v5 → v6 DEĞİŞEN (K, %d): %s" % (len(fark_k), ", ".join(fark_k)))
    print("     v5 → v6 DEĞİŞEN (bulaşık REF +13, %d): %s" % (len(fark_bm), ", ".join(fark_bm)))
    print("     v5 → v6 ÇIKAN (%d): %s" % (len(cikan), ", ".join(cikan)))
    print("     v6 YENİ (%d): %s" % (len(yeni), ", ".join(yeni)))
    dk_, dsum = [], 0.0
    for a in V6_DELIK:
        b6, b5 = bbx(a), V5P[a].BoundingBox()
        ot = max(abs(b6.xmin - b5.xmin), abs(b6.xmax - b5.xmax), abs(b6.ymin - b5.ymin), abs(b6.ymax - b5.ymax), abs(b6.zmin - b5.zmin), abs(b6.zmax - b5.zmax))
        dv = _sek(a).Volume() - V5P[a].Volume(); dsum += dv
        if ot > 0.05 or dv > -0.01: dk_.append((a, round(ot, 3), round(dv, 1)))
    H_["v6_delik"] = {a: round(_sek(a).Volume() - V5P[a].Volume(), 1) for a in V6_DELIK}
    kontrol("2. tur · yalnız DELİK / YUVA / KESİM açılan %d parça (rulo mil yuvaları, yan levha delikleri + gergi yarığı, bant şeridi, göbek yuvaları, DIN klipsi, kelepçe, eksen ayağı): "
            "sınır kutusu v5 ile AYNI (±0,05; göbek yuva ağzı 0,014) · hacim yalnız AZALDI (Σ %.0f mm³) → zarf ve işlev değişmedi" % (len(V6_DELIK), dsum), not dk_, str(dk_ or H_["v6_delik"]))
    kk_ = bbx("kablo_kanali_dikey"); dir_ = bbx("sprey_dirsegi")
    kontrol("2. tur · taşınan / kısalan: kablo_kanali_dikey z %.1f…%.1f (arka köşe dikmesinin önü −798,5; v5 −822…−797 dikmenin içindeydi) · sprey_dirsegi x ≤ %.1f (PulsaJet ucu 305) · koruma braketleri r ≥ 115 (kafa plakası kenarı)"
            % (kk_.zmin, kk_.zmax, dir_.xmax), abs(kk_.zmin - (-D + SAC + 30.0)) < 0.01 and dir_.xmax <= 306.0 + 0.01)
    # ---- 3 · kinematik v5 ile AYNI ----
    fu = max(max(abs(a - b) for a, b in zip(urun_merkez(t), V5.urun_merkez(t))) for t in [i * 0.05 for i in range(401)])
    fg = max(max(abs(a - b) for a, b in zip(grup_trs(g, t), V5.grup_trs(g, t))) for g in ("KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ") for t in [i * 0.1 for i in range(201)])
    kontrol("kinematik v5 ile AYNI: urun_merkez(t) 401 an · en büyük fark %.4f mm · grup_trs(t) 201 an × 5 grup %.4f (kapaklar yalnız servis — çevrimde KAPALI)" % (fu, fg), fu < 1e-9 and fg < 1e-9)
    # ---- 4 · ön düzlem · kabuk · plint · derz · tava ----
    ONG = [p for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    zmx = max(p["wp"].val().BoundingBox().zmax for p in ONG)
    kap = [bbx("onyuz_kapak_%s" % a) for _g, a, _y0, _y1 in KAPAKLAR]
    kontrol("ÖN DÜZLEM: 3 kapağın dış yüzü z %s = Z_ON %.1f · tava 20 → arka kenar z %s · K'nin en ön noktası %.2f ≤ %.1f"
            % ("/".join("%.2f" % b.zmax for b in kap), Z_ON, "/".join("%.2f" % b.zmin for b in kap), zmx, Z_ON + 0.5),
            len(kap) == 3 and all(abs(b.zmax - Z_ON) < 0.01 and abs(b.zmin - Z_TAVA[0]) < 0.01 for b in kap) and zmx <= Z_ON + 0.01)
    on59 = [p for p in ONG if p["wp"].val().BoundingBox().zmax > Z_KABUK_ON + 0.01]
    yab = [p["ad"] for p in on59 if p["grup"] not in KAPAK_GRUP and not p["ad"].startswith("onyuz_basac_mandal_")]
    H_["on59"] = sorted(p["ad"] for p in on59)
    kontrol("+59'un önünde YALNIZ kapak grupları (tava + menteşe kanadı + mandal karşılığı + kilit dili) + kapak boşluğuna giren 3 bas-aç mandalı (z ≤ %.0f): %d parça"
            % (Z_CER[1] + MANDAL["derin"], len(on59)), not yab, str(yab))
    kab = [(a, bbx(a)) for a in ("ust_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "taban_sac_3", "istasyon_tabani_3")]
    kontrol("kabuk ön kenarı +%.0f (kapak arkası): %s · arka sac z %.1f (SABİT) → gövde derinliği %.0f"
            % (Z_KABUK_ON, " · ".join("%s %.2f" % (a, b.zmax) for a, b in kab), bbx("arka_sac").zmin, Z_ON - bbx("arka_sac").zmin),
            all(abs(b.zmax - Z_KABUK_ON) < 0.01 for _a, b in kab) and abs(bbx("arka_sac").zmin + 830.0) < 0.01 and abs(Z_ON - bbx("arka_sac").zmin - 909.0) < 0.01)
    pb = bbx("onyuz_plint"); pv = _sek("onyuz_plint").Volume()
    pv_b = W * Y_PLINT * TAVA_T + 2 * TAVA_T * Y_PLINT * (Z_PLINT[0] + D - SAC) + (W - 2 * TAVA_T) * TAVA_T * PLINT_FLANS
    kontrol("plint onyuz_plint (2. tur): ön yüz z %.1f…%.1f (ön düzlemin %.0f gerisi) · y %.0f–%.0f (SPEC 0–123) · x %.0f–%.0f (E v7 plinti x 600'den devam: tek çizgi) · "
            "yan dönüşler TAM DERİNLİK → z %.1f · üst flanş %.0f · hacim %.0f = beklenen %.0f · eski plint_on YOK"
            % (Z_PLINT[0], pb.zmax, Z_ON - pb.zmax, pb.ymin, pb.ymax, pb.xmin, pb.xmax, pb.zmin, PLINT_FLANS, pv, pv_b),
            abs(pb.zmax - Z_PLINT[1]) < 0.01 and abs(Z_ON - pb.zmax - 60.0) < 0.01 and abs(pb.ymin) < 0.01 and abs(pb.ymax - Y_PLINT) < 0.01 and abs(pb.xmin) < 0.01
            and abs(pb.xmax - W) < 0.01 and abs(pb.zmin + D - SAC) < 0.01 and abs(pv - pv_b) < 1.0 and not [p for p in PARCALAR if p["ad"] == "plint_on"])
    # K'nin altı kapalı mı: önden (z +79 → arka) ve yandan (x −10 → 610) ışın — plint ön yüzüne / yan dönüşüne çarpmalı (v6-1: yan cepler + alttaki 10 mm açıktı)
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    ps_ = _sek("onyuz_plint"); isin = []
    for ad_, a_, b_ in (("ön x 15", (15.0, 60.0, Z_ON), (15.0, 60.0, -D)), ("ön x 585", (585.0, 60.0, Z_ON), (585.0, 60.0, -D)), ("ön y 5", (300.0, 5.0, Z_ON), (300.0, 5.0, -D)),
                        ("yan sol z −400", (-10.0, 60.0, -400.0), (300.0, 60.0, -400.0)), ("yan sağ z −400", (W + 10.0, 60.0, -400.0), (300.0, 60.0, -400.0))):
        e_ = cq.Edge.makeLine(cq.Vector(*a_), cq.Vector(*b_)); x_ = _DSS(ps_.wrapped, e_.wrapped)
        isin.append((ad_, round(x_.Value(), 3)))
    H_["plint_isin"] = isin
    kontrol("K'nin altı KAPALI (ışın testi, 5 ışın): önden x 15 / 585 / y 5 ve yandan x 0 / 600 → hepsi plinte çarpar (aralık 0) · %s" % " · ".join("%s %.2f" % v for v in isin),
            all(v < 1e-6 for _a, v in isin), str(isin))
    ky_ = [(b.ymin, b.ymax) for b in kap]; kx_ = [(b.xmin, b.xmax) for b in kap]
    dz_ = [ky_[i + 1][0] - ky_[i][1] for i in range(len(ky_) - 1)]
    d_f = kx_[0][0]; d_e = X_E_KAPAK0 - (X_K_HAT + kx_[0][1])
    H_["derz"] = dict(yatay=dz_, firin=d_f, E=d_e, kapak_y=ky_, kapak_x_dunya=(X_K_HAT + kx_[0][0], X_K_HAT + kx_[0][1]))
    kontrol("derzler %.0f mm: yatay %s (883/886 · 1305/1308) · alt kenar %.0f · üst kenar %.0f (1862 − 3) · fırın/dolap ↔ K %.1f (x 4000 → %.0f) · K ↔ E %.1f (%.1f → %.1f)"
            % (DERZ, "/".join("%.1f" % v for v in dz_), ky_[0][0], ky_[-1][1], d_f, X_K_HAT + kx_[0][0], d_e, X_K_HAT + kx_[0][1], X_E_KAPAK0),
            all(abs(v - DERZ) < 0.01 for v in dz_) and abs(ky_[0][0] - 126.0) < 0.01 and abs(ky_[-1][1] - (H - DERZ)) < 0.01 and abs(d_f - DERZ) < 0.01 and abs(d_e - DERZ) < 0.01
            and all(abs(a - kx_[0][0]) < 0.01 and abs(b - kx_[0][1]) < 0.01 for a, b in kx_) and abs(ky_[0][1] - 883.0) < 0.01 and abs(ky_[1][1] - 1305.0) < 0.01)
    tv_ = []
    for _g, a, y0, y1 in KAPAKLAR:
        w_, h_ = KAPAK_X[1] - KAPAK_X[0], y1 - y0
        n_ = len(YARIK["bant"].get(a, ())) * len(_yarik_x()) if YARIK_ACIK else 0          # 2. tur: varsayılan YARIKSIZ
        ve = w_ * h_ * TAVA_D - (w_ - 2 * TAVA_T) * (h_ - 2 * TAVA_T) * (TAVA_D - TAVA_T) - n_ * YARIK["en"] * YARIK["boy"] * TAVA_T
        vg = _sek("onyuz_kapak_%s" % a).Volume()
        tv_.append((a, n_, vg, ve, vg * RHO_304))
    H_["kapak"] = {a: dict(yarik=n_, kg=round(kg_, 2)) for a, n_, _vg, _ve, kg_ in tv_}
    kontrol("tava panel katıdan: sac %.1f + büküm %.0f (hacim = dış kutu − iç boşluk − yarıklar) · %s"
            % (TAVA_T, TAVA_D, " · ".join("%s %.2f kg %d yarık" % (a, kg_, n_) for a, n_, _vg, _ve, kg_ in tv_)), all(abs(vg - ve) < 1.0 for _a, _n, vg, ve, _k in tv_),
            str([(a, round(vg - ve, 2)) for a, _n, vg, ve, _k in tv_]))
    # 2. tur (denetçi ORTA-2 + K-10): lazer yarık yalnız SEÇENEK — varsayılan modelde ön sacda kesik YOK; seçenek katıdan ölçülür (ortalı, paylar eşit, dayama lastiğine denk gelmez)
    yok_ = [a for _g, a, _y0, _y1 in KAPAKLAR if H_["kapak"][a]["yarik"]]
    kontrol("ÖNDEN YALNIZ DÜZ YÜZEY + DERZ (SPEC §1): YARIK_ACIK = %s → 3 kapağın ön sacında kesik %s (v6-1: ALT + ÜST'te 416 yarık varsayılandı)" % (YARIK_ACIK, "YOK" if not yok_ else yok_),
            not YARIK_ACIK and not yok_)
    xs_ = _yarik_x(); sol_ = xs_[0] - KAPAK_X[0]; sag_ = KAPAK_X[1] - (xs_[-1] + YARIK["en"])
    pay_ = {a: (YARIK["bant"][a][0][0] - y0, y1 - YARIK["bant"][a][-1][1]) for _g, a, y0, y1 in KAPAKLAR if a in YARIK["bant"]}
    vs_ = {}
    for _g, a, y0, y1 in KAPAKLAR:
        if a in YARIK["bant"]:
            yk_, ns_ = _yarik(a); t_ = _tava(y0, y1).val(); w_ = t_.cut(yk_)
            vs_[a] = (ns_, t_.Volume() - w_.Volume(), ns_ * YARIK["en"] * YARIK["boy"] * TAVA_T, w_.isValid())
    H_["yarik_secenek"] = dict(acik=YARIK_ACIK, sira=len(xs_), sol_pay=sol_, sag_pay=sag_, dikey_pay=pay_, yarik={a: v[0] for a, v in vs_.items()})
    kontrol("SEÇENEK yarık deseni (katıdan, modele girmez): %d yarık/sıra · ORTALI sol pay %.2f = sağ pay %.2f (v6-1 37 / 45,5) · dikey paylar %s · %s · ALT üst bandı ≤ dayama lastiği %.0f"
            % (len(xs_), sol_, sag_, " · ".join("%s %.0f/%.0f" % (a, p0, p1) for a, (p0, p1) in pay_.items()), " · ".join("%s %d yarık" % (a, v[0]) for a, v in vs_.items()), DAYAMA["y"][0]),
            abs(sol_ - sag_) < 0.01 and all(abs(p0 - p1) < 0.01 for p0, p1 in pay_.values()) and all(abs(v - vb) < 0.5 and ok for _n, v, vb, ok in vs_.values())
            and YARIK["bant"]["alt"][-1][1] <= DAYAMA["y"][0], str(vs_))
    # ---- 5 · yük yolu temasları (gerçek katı aralığı ≤ 0,05) ----
    TEMAS = [("onyuz_cerceve_dikme_sol", "sol_sac_urun_girisi"), ("onyuz_cerceve_dikme_sol", "taban_sac_3"), ("onyuz_cerceve_dikme_sol", "ust_sac"),
             ("onyuz_cerceve_dikme_sag", "sag_sac_E_penceresi"), ("onyuz_cerceve_dikme_sag", "taban_sac_3"), ("onyuz_cerceve_dikme_sag", "ust_sac"),
             ("onyuz_cerceve_dikme_sol", "istasyon_tabani_3"), ("onyuz_cerceve_dikme_sag", "istasyon_tabani_3")]
    TEMAS += [("onyuz_cerceve_kayit_%s" % a, "onyuz_cerceve_dikme_%s" % s_) for a, _y0, _y1 in KAYITLAR for s_ in ("sol", "sag")]
    TEMAS += [("kopru_kirisi_%d" % i, "kopru_kirisi_uc_plakasi_%d" % j) for i in range(2) for j in range(2)]
    TEMAS += [("kopru_kirisi_uc_plakasi_0", "sol_sac_urun_girisi"), ("kopru_kirisi_uc_plakasi_1", "sag_sac_E_penceresi"),
              ("kopru_kirisi_uc_plakasi_0", "onyuz_cerceve_dikme_sol"), ("kopru_kirisi_uc_plakasi_1", "onyuz_cerceve_dikme_sag"),
              ("silindir_baglanti_plakasi", "kopru_kirisi_0"), ("silindir_baglanti_plakasi", "kopru_kirisi_1"),
              ("bulasik_tabla_kirisi_0", "sol_sac_urun_girisi"), ("bulasik_tabla_kirisi_0", "sag_sac_E_penceresi"), ("bulasik_tabla_kirisi_1", "sol_sac_urun_girisi"),
              ("bulasik_tabla_kirisi_1", "sag_sac_E_penceresi"), ("bulasik_tabla_kirisi_0", "taban_sac_3"), ("bulasik_tabla_kirisi_1", "taban_sac_3"),
              ("bulasik_tavasi", "bulasik_tabla_kirisi_0"), ("bulasik_tavasi", "bulasik_tabla_kirisi_1"), ("REF_bulasik_govde_cift_cidar", "bulasik_tavasi"),
              ("onyuz_plint", "taban_sac_3")]
    TEMAS += [("onyuz_mentese_govde_%s_%d" % (a, j), "onyuz_cerceve_dikme_sol") for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_mentese_kanat_%s_%d" % (a, j), "onyuz_mentese_govde_%s_%d" % (a, j)) for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_mentese_kanat_%s_%d" % (a, j), "onyuz_kapak_%s" % a) for _g, a, _y0, _y1 in KAPAKLAR for j in range(2)]
    TEMAS += [("onyuz_basac_mandal_%s" % a, "onyuz_cerceve_dikme_sag") for _g, a, _y0, _y1 in KAPAKLAR]
    TEMAS += [("onyuz_kilit_AZM40_%s" % a, "onyuz_cerceve_dikme_sag") for a in AZM_KAPAK]
    # 2. tur: kilit dili ağızda · dayama lastiği · plint dönüşleri yan saclarda · geçişler taban sacında · taşınan kanal / delik-yuva parçaları eşlerine değer
    TEMAS += [("onyuz_kilit_dili_%s" % a, "onyuz_kilit_AZM40_%s" % a) for a in AZM_KAPAK]
    TEMAS += [("onyuz_dayama_lastigi_alt", "onyuz_kapak_alt"), ("onyuz_plint", "sol_sac_urun_girisi"), ("onyuz_plint", "sag_sac_E_penceresi"),
              ("kablo_kanali_dikey", "kose_dikmesi_3"), ("kablo_kanali_dikey", "istasyon_tabani_3"), ("yag_tanki_kelepcesi", "yag_tanki_3L"), ("yag_tanki_kelepcesi", "yag_tanki_kapagi"),
              ("eksen_ayagi_1", "ZLW_uc_blogu_1"), ("eksen_ayagi_1", "ZLW-1040_eksen_profili"), ("tahrik_rulosu_RollerDrive_EC5000", "tahrik_rulosu_mili"),
              ("kuyruk_rulosu", "kuyruk_rulosu_mili"), ("bant_yan_levhasi_0", "tahrik_rulosu_mili"), ("bant_yan_levhasi_1", "kuyruk_rulosu_mili"),
              ("bant_yan_levhasi_0", "bant_gergi_civatasi_0"), ("bant_yan_levhasi_1", "bant_gergi_civatasi_1"), ("bicak_0", "bicak_gobek_halkasi"),
              ("koruma_braketi_0", "kafa_plakasi_8"), ("sprey_dirsegi", "PulsaJet_AA10000AUH_104210"), ("surucu_STP-DRV-4830", "din_rayi_1")]
    TEMAS += [(("bulasik_gecis_rakoru_" if k_ == "elektrik" else "bulasik_gecis_lastigi_") + k_, "taban_sac_3") for k_ in GECIS]
    tm = [(a, b, _mesafe(a, b)) for a, b in TEMAS]
    kotu = [(a, b, round(v, 3)) for a, b, v in tm if v > 0.05]
    kontrol("yük yolu temasları (%d çift, gerçek katı aralığı ≤ 0,05): ön çerçeve ↔ kabuk · kayıt ↔ dikme · köprü kirişi ↔ uç plakası ↔ yan sac + ön dikme · "
            "tabla kirişi ↔ yan sac + taban · tava ↔ kiriş · makine ↔ tava · plint ↔ taban · menteşe / mandal / AZM ↔ çerçeve · menteşe kanadı ↔ kapak" % len(TEMAS), not kotu, str(kotu))
    # ---- 6 · kapaklar: kinematik + 0–90° tarama ----
    kb = kapak_ac(_sek("onyuz_kapak_orta"), KAPAK_MAX).BoundingBox()
    kontrol("kapak kinematiği: SOL menteşe sanal pivotu (x %.1f, z %.1f) · %.0f°'de ORTA kapak x %.1f–%.1f · z %.1f…%.1f (öne-sola açılır, fırın/dolap önüne yaslanır)"
            % (MENTESE_EKSEN + (KAPAK_MAX, kb.xmin, kb.xmax, kb.zmin, kb.zmax)),
            abs(kb.xmin - KAPAK_X[0]) < 0.05 and abs(kb.xmax - (KAPAK_X[0] + TAVA_D)) < 0.05 and abs(kb.zmin - Z_ON) < 0.05 and abs(kb.zmax - (Z_ON + KAPAK_X[1] - KAPAK_X[0])) < 0.05)
    t0 = time.time()
    SAB = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT" or p["ad"].startswith("REF_bulasik_")]
    SAB = [(p, s_, s_.BoundingBox()) for p, s_ in SAB]
    bul, xb, zb, zd_ = {}, [1e9, -1e9], [1e9, -1e9], [1e9]
    ANG = [float(a) for a in range(0, int(KAPAK_MAX) + 1, 5)]
    for g in KAPAK_GRUP:
        dg = SAB + [(p, p["wp"].val(), p["wp"].val().BoundingBox()) for p in PARCALAR if p["grup"] in KAPAK_GRUP and p["grup"] != g]
        kp = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == g]
        for aci in ANG:
            for p, s_ in kp:
                r = kapak_ac(s_, aci); A = r.BoundingBox()
                xb[0] = min(xb[0], A.xmin); xb[1] = max(xb[1], A.xmax); zb[1] = max(zb[1], A.zmax)
                if p["ad"].startswith("onyuz_kilit_dili_"): zd_[0] = min(zd_[0], A.zmin)                 # 2. tur: dil AZM ağzına girer (z 49)
                else: zb[0] = min(zb[0], A.zmin)
                for q, b, B_ in dg:
                    if not KC._bb_kesisir(A, B_): continue
                    v = r.intersect(b).Volume()
                    if v > 1.0: bul[(g, p["ad"], q["ad"])] = (round(v, 1), aci)
    H_["kapak_tarama"] = dict(an=len(ANG), bulgu=len(bul), x=xb, z=zb, kilit_dili_zmin=zd_[0])
    kontrol("kapaklar 0–%.0f° (%d açı × 3 kapak, her 5°) ↔ bütün sabit parçalar + bulaşık + öbür kapaklar (kapalı): %d çakışma · süpürülen x %.1f–%.1f · z %.1f…%.1f (K bandında kalır: fırın/dolap ve E yüzlerine girmez, "
            "+59'un arkasına YALNIZ kilit dili geçer: AZM ağzına z %.1f) · %.0f sn"
            % (KAPAK_MAX, len(ANG), len(bul), xb[0], xb[1], zb[0], zb[1], zd_[0], time.time() - t0),
            not bul and xb[0] >= KAPAK_X[0] - 0.05 and xb[1] <= KAPAK_X[1] + 0.05 and zb[0] >= Z_TAVA[0] - 0.05 and abs(zd_[0] - (Z_CER[1] - AZM_AGIZ)) < 0.05, str(sorted(bul.items())[:5]))
    # 6c · TAM TARAMA — İSTİSNA LİSTESİ YOK, BÜTÜN PARÇALAR (2. tur, denetçi ORTA-1: v6-1 istisnasız taramayı yalnız yeni + değişen 69 parçaya yapıyordu;
    #      ISTISNA kablo_kanali_dikey ↔ kose_dikmesi_3 82 016 mm³ GERÇEK çakışmayı + 25 gömülü örtüşmeyi gizliyordu → hepsi düzeltildi, ISTISNA BOŞ)
    #      (i) sabit + kapaklar (kapalı) + bulaşık kendi aralarında · (ii) her hareketli grup kendi içinde · (iii) hareketliler çevrim boyunca (her 0,1 sn) ↔ sabit + öbür gruplar
    t0 = time.time()
    HARG = ("KESICI", "ITICI_ARABA", "ITICI_KOL")
    SK = [(p, s_, s_.BoundingBox()) for p, s_ in ((p, p["wp"].val()) for p in PARCALAR if p["grup"] in SABIT_GRUP or p["ad"].startswith("REF_bulasik_"))]
    tam, ncift = {}, [0]
    def _yaz_(p, q, a, b, an):
        ncift[0] += 1
        v = a.intersect(b).Volume()
        if v > 0.01:
            k_ = tuple(sorted((p["ad"], q["ad"])))
            if v > tam.get(k_, (0.0, ""))[0]: tam[k_] = (round(v, 2), an)
    for i, (p, a, A) in enumerate(SK):
        for q, b, B_ in SK[i + 1:]:
            if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "sabit")
    HP = [p for p in PARCALAR if p["grup"] in HARG]
    for g in HARG:
        G_ = [(p, p["wp"].val(), p["wp"].val().BoundingBox()) for p in HP if p["grup"] == g]
        for i, (p, a, A) in enumerate(G_):
            for q, b, B_ in G_[i + 1:]:
                if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "grup içi")
    anl = [round(0.1 * k_, 2) for k_ in range(int(DONGU / 0.1) + 1)]
    for t in anl:
        hh = [(p, tasi(p["wp"].val(), grup_trs(p["grup"], t))) for p in HP]
        hh = [(p, a, a.BoundingBox()) for p, a in hh]
        for i, (p, a, A) in enumerate(hh):
            for q, b, B_ in [x for x in hh[i + 1:] if x[0]["grup"] != p["grup"]] + SK:
                if KC._bb_kesisir(A, B_): _yaz_(p, q, a, b, "t=%.1f" % t)
    tl_ = sorted(tam.items(), key=lambda kv: -kv[1][0])
    H_["tam_tarama"] = dict(parca=len(SK) + len(HP), an=len(anl), aday_cift=ncift[0], cakisma=len(tam), bulgu=[[a, b, v, an] for (a, b), (v, an) in tl_[:30]], istisna=len(ISTISNA))
    kontrol("TAM TARAMA İSTİSNASIZ (2. tur): %d parça (sabit + 3 kapak kapalı + bulaşık + %d hareketli) · hareketliler %d an (her 0,1 sn) · %d aday çift · eşik 0,01 mm³ → %d çakışma · ISTISNA listesi %d kalem · %.0f sn"
            % (len(SK) + len(HP), len(HP), len(anl), ncift[0], len(tam), len(ISTISNA), time.time() - t0), not tam and not ISTISNA, str(tl_[:8]))
    # ---- 7 · BULAŞIK v2 (ayrı modül, montajdaki yerinde) ----
    bm, (kx, ky, kz) = bulasik_parcalari()
    ONDE = ("isikli_kulp", "dokunmatik_ekran")
    bmb = cq.Compound.makeCompound([sh for a_, sh in bm if a_ not in ONDE]).BoundingBox()
    bon = max(sh.BoundingBox().zmax for a_, sh in bm if a_ in ONDE)
    bta = cq.Compound.makeCompound([sh for a_, sh in bm]).BoundingBox()
    Z = BULASIK_ZARF; tv = bbx("bulasik_tavasi")
    H_["bulasik"] = dict(x=(bmb.xmin, bmb.xmax), y=(bmb.ymin, bmb.ymax), z=(bmb.zmin, bmb.zmax), dunya_x=(bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT), kulp_onu_z=bon, tam_z=(bta.zmin, bta.zmax),
                         yer=BULASIK_YER, tava_ustu=tv.ymax)
    kontrol("bulaşık (bulasik_cad_v2, kök %s · AYAKSIZ): dünya x %.1f–%.1f · gövde altı y %.1f = tava üstü %.1f (v5: gövde 136 → +%.0f) · üst %.0f · TAMAMI z %.0f…%.0f = zarf · kulp + ekran önü z %.1f (kapak arkasına %.1f)"
            % (BULASIK_YER, bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT, bmb.ymin, tv.ymax, bmb.ymin - 136.0, bmb.ymax, bta.zmin, bta.zmax, bon, Z_TAVA[0] - bon),
            not [a_ for a_, _s in bm if a_.startswith("ayar_ayagi")] and abs(bmb.ymin - tv.ymax) < 0.01 and abs(bmb.ymin - Y_TABLA) < 0.01 and abs(bmb.ymin - 149.0) < 0.01
            and abs(bta.zmin - Z["z"][0]) < 0.01 and abs(bta.zmax - Z["z"][1]) < 0.01 and bmb.xmin >= Z["x"][0] - 0.01 and bmb.xmax <= Z["x"][1] + 0.01
            and bmb.ymin >= Z["y"][0] - 0.01 and bmb.ymax <= Z["y"][1] + 0.01 and bon < Z_CER[0])
    bag = max(sh.BoundingBox().ymax for a_, sh in bm if a_.startswith("baglanti_"))
    kontrol("bulaşık arka bağlantıları üstü y %.1f ≤ %.0f (v6: +13 · föy tahliye 165 + Y0 %.0f + r 15)" % (bag, BULASIK_BAGLANTI_UST, BULASIK_YER[1]), bag <= BULASIK_BAGLANTI_UST + 0.01)
    K_ = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]), K_)
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez (kapaklar kapalı · tava üstü = zarf altı)" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))
    g2 = []
    for p, sh in K_:
        A = sh.BoundingBox()
        for a_, b_ in bm:
            if KC._bb_kesisir(A, b_.BoundingBox()):
                v = sh.intersect(b_).Volume()
                if v > 0.01: g2.append((p["ad"], a_, round(v, 1)))
    kontrol("bulaşık gerçek katıları (%d parça) ↔ K parçaları (kapaklar kapalı) çakışma %d" % (len(bm), len(g2)), not g2, str(g2[:5]))
    ZK = kutu_(kx, ky, kz)
    alt = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "KAPAK_ALT"]
    def alt_hacim(aci):
        v = 0.0
        for _p, s_ in alt:
            r = kapak_ac(s_, aci)
            if KC._bb_kesisir(r.BoundingBox(), ZK.BoundingBox()): v += r.intersect(ZK).Volume()
        return v
    v_kapali = alt_hacim(0.0)
    v60 = alt_hacim(60.0)
    amin = next((a for a in range(60, int(KAPAK_MAX) + 1) if alt_hacim(float(a)) <= 0.01), None)
    SABK = [(p, s_) for p, s_ in K_ if p["grup"] != "KAPAK_ALT"] + [(p, kapak_ac(s_, KAPAK_MAX)) for p, s_ in alt]
    g3 = giren(ZK, SABK)
    ka_ = cq.Compound.makeCompound([kapak_ac(s_, KAPAK_MAX) for _p, s_ in alt]).BoundingBox()
    L_bm = BM.KAPI["y1"] - BM.KAPI["y0"]
    z_day = Z_ON - TAVA_T - DAYAMA["t"]                                                 # 2. tur: EPDM dayama lastiğinin yüzü (74,5) — bulaşık kapağının üst ön kenarı buna değer
    bm_aci = math.degrees(math.asin(min(1.0, (z_day - BULASIK_YER[2]) / L_bm)))
    y_day = BULASIK_YER[1] + BM.KAPI["y0"] + L_bm * math.cos(math.radians(bm_aci))   # temas çizgisinin y'si (menteşe y 384 + 455·cos)
    bmk_ = [sh for a_, sh in bm if a_ == "kapak"][0].BoundingBox()
    H_["bulasik_kapak_zarfi"] = dict(x=kx, y=ky, z=kz, alt_kapak_min_aci=amin, alt_kapali_hacim=round(v_kapali, 0), pay_90=round(kx[0] - ka_.xmax, 1), bulasik_kapak_kilitte_aci=round(bm_aci, 1),
                                     dayama_temas_y=round(y_day, 1), dayama=DAYAMA)
    kontrol("bulaşık kapak açık zarfı (x %.1f–%.1f · y %.0f–%.0f · z %.0f…%.0f) ↔ K sabitleri + ORTA/ÜST (kapalı) + ALT kapak %.0f° AÇIK: %d parça · ALT kapakla pay %.1f mm"
            % (kx + ky + kz + (KAPAK_MAX, len(g3), kx[0] - ka_.xmax)), not g3, str(g3[:5]))
    kontrol("KİLİT (mekanik): ALT kapak kapalıyken zarfta (%.0f mm³) → bulaşık kapağı ≈ %.1f° açılıp ALT kapağın EPDM dayama lastiğine (x %.1f–%.1f · y %.0f–%.0f) y %.1f'de dayanır — 1,5 sac yüklenmez "
            "(kapak x %.1f–%.1f lastiğin içinde) · ALT kapak ≥ %s° açıkken bulaşık kapağı serbest (menteşe en çok %.0f°)"
            % (v_kapali, bm_aci, DAYAMA["x"][0], DAYAMA["x"][1], DAYAMA["y"][0], DAYAMA["y"][1], y_day, bmk_.xmin, bmk_.xmax, amin, KAPAK_MAX),
            v_kapali > 0 and v60 > 0 and amin is not None and amin <= KAPAK_MAX - 5.0 and DAYAMA["y"][0] + 5.0 <= y_day <= DAYAMA["y"][1] - 5.0
            and DAYAMA["x"][0] <= bmk_.xmin and bmk_.xmax <= DAYAMA["x"][1])
    g4 = giren(kutu_(Z["x"], Z["y"], BULASIK_ARKA_PAY), K_)
    kontrol("MEIKO arka payı z %.0f…%.0f BOŞ: hiçbir K parçası girmez (makinenin kendi bağlantıları y ≤ %.0f)" % (BULASIK_ARKA_PAY + (BULASIK_BAGLANTI_UST,)), not g4, str(g4))
    ab = (Z["x"], Z["y"], (bbx("arka_sac").zmax, BULASIK_ARKA_PAY[0]))
    g5 = giren(kutu_(*ab), K_)
    H_["bulasik_arka_bos"] = dict(x=ab[0], y=ab[1], z=ab[2], derinlik=ab[2][1] - ab[2][0])
    kontrol("bulaşığın arkası BOŞ: x %.1f–%.1f · y %.0f–%.0f · z %.1f…%.0f (%.1f mm derin) → K parçası yok" % (ab[0] + ab[1] + ab[2] + (ab[2][1] - ab[2][0],)), not g5, str(g5[:5]))
    ustu = [(p["wp"].val().BoundingBox().ymin, p["ad"]) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")
            and KC._bb_kesisir(p["wp"].val().BoundingBox(), kutu_(Z["x"], (Z["y"][1], H), Z["z"]).BoundingBox())]
    H_["bulasik_ust_bosluk"] = min(ustu)[0] - bmb.ymax
    kontrol("bulaşığın üstü %.0f → ilk K parçası %s %.0f: boşluk %.0f mm (v5: 66 → makine +13)" % (bmb.ymax, min(ustu)[1], min(ustu)[0], H_["bulasik_ust_bosluk"]), H_["bulasik_ust_bosluk"] > 0.0)
    sol = bmb.xmin - bbx("onyuz_cerceve_dikme_sol").xmax; sol_ark = bmb.xmin - bbx("sol_sac_urun_girisi").xmax
    H_["bulasik_sol"] = dict(on=sol, arka=sol_ark)
    print("     bulaşığın solu: sol ön çerçeve dikmesinden %.1f · sol sacdan %.1f → BOŞ (v6: öndeki kesik köşe dikmesi yok)" % (sol, sol_ark))
    # ---- 8 · HAVADA PARÇA (denetim_temas_v1 · hareketliler t = 0 · kapaklar kapalı · bulaşık dahil) ----
    HV = [(p["ad"], p["wp"]) for p in PARCALAR if p["grup"] not in ("URUN", "URUN_IZ", "SPREY") and (p["grup"] != "REF" or p["ad"].startswith("REF_bulasik_"))]
    hv = DT.havada(HV)
    nh = DT.yaz(hv, baslik="HAVADA PARCA (K v6 + bulasik v2 · hareketliler t=0 · kapaklar kapali)")
    BEYAZ = ()                                                                          # beyaz liste: BOŞ (DGRF-C burçları kayar geçme — idealleştirilmiş temas, modelde gerçek parça)
    H_["havada"] = dict(once=dict(bilesen=17, parca=74, not_="kesme v5 + bulaşık v1 (K'deki yerinde, ayaklı) · aynı denetim"), sonra=dict(parca=hv["parca"], bagli=hv["bagli"],
                        bilesen=nh, uye=[d_["uye"] for d_ in hv["bilesen"]]), beyaz_liste=list(BEYAZ))
    kontrol("HAVADA PARÇA (denetim_temas_v1, tol 0,05): %d parça · kök (ayak) %d · zemine bağlı %d · HAVADA %d bileşen · v5: 17 bileşen / 74 parça · beyaz liste BOŞ"
            % (hv["parca"], hv["kok"], hv["bagli"], nh), nh == 0 and hv["bagli"] == hv["parca"])
    HVa = [(p["ad"], (kapak_ac(p["wp"].val(), KAPAK_MAX) if p["grup"] in KAPAK_GRUP else p["wp"])) for p in PARCALAR
           if p["grup"] not in ("URUN", "URUN_IZ", "SPREY") and (p["grup"] != "REF" or p["ad"].startswith("REF_bulasik_"))]
    hva = DT.havada(HVa)
    uy_ = set(u for d_ in hva["bilesen"] for u in d_["uye"]); kap_ = set(p["ad"] for p in PARCALAR if p["grup"] in KAPAK_GRUP)
    H_["havada_kapak_acik"] = dict(bilesen=len(hva["bilesen"]), parca=len(uy_), uye=[d_["uye"] for d_ in hva["bilesen"]])
    kontrol("2. tur · kapaklar %.0f° AÇIK: havada kalan YALNIZ %d kapak grubu (%d parça: tava + menteşe kanadı + karşılık + dil + dayama) — menteşe mekanizması sanal pivot, modelde YOK "
            "(EMKA pivot yeri üreticiden teyit) · kapağa dayanan başka parça YOK" % (KAPAK_MAX, len(hva["bilesen"]), len(uy_)), uy_ <= kap_ and len(hva["bilesen"]) == len(KAPAK_GRUP), str(sorted(uy_ - kap_)))
    UYARI.append("kapaklar AÇIK konumda bağlılık: menteşe kanadı ↔ gövde arası sanal pivot (EMKA 1046-U5 iç mekanizması modelde yok) → açıkken %d kapak grubu havada görünür; kapalı konumda bağlı (havada 0)" % len(hva["bilesen"]))
    # ---- 9 · hesaplar ----
    L_k = (W - SAC - UC_T) - (SAC + UC_T)
    I_k = (40.0 ** 4 - 36.0 ** 4) / 12.0
    P_k = H_["silindir_N"] / 2.0
    d_k = P_k * L_k ** 3 / (48.0 * E_304 * I_k)
    s_k = P_k * L_k / 4.0 / (I_k / 20.0)
    yb_k = 2.0 * P_k / 2.0 / (6 * 6.0 * SAC)
    H_["kopru"] = dict(aciklik=L_k, P_kiris=P_k, sehim=d_k, gerilme=s_k, uc_plaka_yatak=yb_k)
    kontrol("köprü (v6): 2 × 40×40×2 · açıklık %.0f · tepki %.0f N (DGRF-C-63, 6 bar) → kiriş başına %.0f N: sehim %.2f mm (basit mesnet, en kötü; uçlar kaynaklı) · gerilme %.0f MPa (304 akma 205, emniyet %.1f) · uç plakası → yan sac 6 × M6 yatak basıncı %.1f MPa"
            % (L_k, H_["silindir_N"], P_k, d_k, s_k, 205.0 / s_k, yb_k), d_k < 0.5 and s_k < 205.0 / 3.0 and yb_k < 100.0)
    kz, ky, kt = TABLA_KIRIS
    I_t = (kz * ky ** 3 - (kz - 2 * kt) * (ky - 2 * kt) ** 3) / 12.0
    L_t = W - 2 * SAC
    P_t = BULASIK_KG * 9.81 / 4.0
    yuk = [(BULASIK_YER[0] - X_K_HAT + 30.0 - SAC, P_t), (BULASIK_YER[0] - X_K_HAT + BM.W - 30.0 - SAC, P_t)]
    def sehim_t(x):
        s_ = 0.0
        for a_, P_ in yuk:
            b_ = L_t - a_
            s_ += P_ * b_ * x * (L_t ** 2 - b_ ** 2 - x ** 2) / (6 * L_t * E_304 * I_t) if x <= a_ else P_ * a_ * (L_t - x) * (L_t ** 2 - a_ ** 2 - (L_t - x) ** 2) / (6 * L_t * E_304 * I_t)
        return s_
    d_t = max(sehim_t(L_t * i / 200.0) for i in range(201))
    H_["tabla"] = dict(kiris=TABLA_KIRIS, I=I_t, P_kose=P_t, sehim=d_t, kg=BULASIK_KG)
    kontrol("bulaşık tablası: 2 × 40×20×2 kiriş (I %.0f mm⁴, açıklık %.0f, yan saclara kaynaklı) · makine %.0f kg [VARSAYIM] köşe başına %.0f N (köşeler kirişin üstünde) → sehim %.2f mm (basit mesnet, taban sacı desteği yok sayıldı)"
            % (I_t, L_t, BULASIK_KG, P_t, d_t), d_t < 1.0)
    mg = {a: H_["kapak"][a]["kg"] * 9.81 for _g, a, _y0, _y1 in KAPAKLAR}
    mom = {a: mg[a] * (KAPAK_X[1] - KAPAK_X[0]) / 2.0 / (MENTESE_Y[a][1] - MENTESE_Y[a][0]) for a in mg}
    H_["mentese"] = dict(dikey_N=dict((a, round(mg[a] / 2.0, 1)) for a in mg), yatay_N=dict((a, round(mom[a], 1)) for a in mom))
    UYARI.append("menteşe yükü: kapak başına 2 × EMKA 1046-U5 · dikey %s N/menteşe · 90° açıkken yatay kuvvet çifti %s N (kapak ağırlık merkezi 298 mm dışarıda) — EMKA yük değeri föyde yok, üreticiden teyit"
                 % ("/".join("%.0f" % (mg[a] / 2.0) for a in mg), "/".join("%.0f" % mom[a] for a in mom)))
    A_b = 2 * len(_yarik_x()) * YARIK["en"] * YARIK["boy"] / 1e6
    hA = (sum(YARIK["bant"]["alt"][2]) + sum(YARIK["bant"]["alt"][3]) - sum(YARIK["bant"]["alt"][0]) - sum(YARIK["bant"]["alt"][1])) / 4000.0
    hU = (sum(YARIK["bant"]["ust"][2]) + sum(YARIK["bant"]["ust"][3]) - sum(YARIK["bant"]["ust"][0]) - sum(YARIK["bant"]["ust"][1])) / 4000.0
    dTA, dTU = isi_dT(Q_BULASIK_W, A_b, hA), isi_dT(Q_UST_W, A_b, hU)
    A_alt = (KAPAK_X[1] - KAPAK_X[0]) * (KAPAKLAR[0][3] - KAPAKLAR[0][2]) / 1e6; A_ust = (KAPAK_X[1] - KAPAK_X[0]) * (KAPAKLAR[2][3] - KAPAKLAR[2][2]) / 1e6
    dTA0, dTU0 = Q_BULASIK_W / (U_KAPALI * A_alt), Q_UST_W / (U_KAPALI * A_ust)
    H_["isi"] = dict(varsayilan="YARIKSIZ (SPEC §1)", yarik_acik=YARIK_ACIK, kapali=dict(U=U_KAPALI, A_alt=A_alt, A_ust=A_ust, dT_alt=dTA0, dT_ust=dTU0),
                     secenek_yarik=dict(yarik_alan_bant_cm2=A_b * 1e4, alt=dict(Q=Q_BULASIK_W, h=hA, dT=dTA), ust=dict(Q=Q_UST_W, h=hU, dT=dTU), alt_15K_cm2=A_b * 1e4 * (dTA / 15.0) ** 1.5))
    UYARI.append("ISI — KARAR GEREKLİ, montaja almadan önce (VARSAYIM, ölç): varsayılan model SPEC'e uygun YARIKSIZ → kapalı bölme ısıyı yalnız ön kapaktan atar: ALT (bulaşık Q %.0f W) ΔT ≈ %.0f K · "
                 "ÜST (Q %.0f W) ΔT ≈ %.0f K (U %.0f W/m²K iyimser, A %.2f / %.2f m²) → KABUL EDİLEMEZ. Seçenekler: (a) YARIK_ACIK = True: bant başına %.0f cm² → ALT ΔT ≈ %.0f K (baca %.2f m) · "
                 "ÜST ≈ %.0f K; (b) ALT için bant başına ≈ %.0f cm² (ΔT ≤ 15 K); (c) 24 V fan (B dolabındaki ebm-papst 4414 FL) + gizli emiş/atış; (d) MEIKO'ya kapalı niş havalandırma şartı sorulmalı · "
                 "fırın ağzından K'ye sızan sıcak hava BİLİNMİYOR" % (Q_BULASIK_W, dTA0, Q_UST_W, dTU0, U_KAPALI, A_alt, A_ust, A_b * 1e4, dTA, hA, dTU, A_b * 1e4 * (dTA / 15.0) ** 1.5))
    # 2. tur (denetçi K-7 + K-12): ölçülen açık konular
    hk_ = _sek("hava_hortumu_kaldirma"); mg_ = _sek("MGPM20-60_govde")
    hm_ = [(t, _mesafe(hk_, tasi(mg_, grup_trs("ITICI_ARABA", t)))) for t in [k_ * 0.1 for k_ in range(int(DONGU / 0.1) + 1)]]
    H_["kaldirma_hortumu_MGPM"] = dict(t0=hm_[0][1], min=min(v for _t, v in hm_), max=max(v for _t, v in hm_))
    UYARI.append("kaldırma hortumu (AÇIK): valf ucu bağlı, MGPM ucu BOŞTA — t = 0'da %.0f mm, çevrim boyunca %.0f–%.0f mm (itici arabası 365 strok) → spiral hortum (ör. SMC TCU0425 sarmal PU) "
                 "ya da mini enerji zinciri (igus E2 micro) modellenmeli; 'havada 0' yalnız valf ucunun bağlı olmasından" % (H_["kaldirma_hortumu_MGPM"]["t0"], H_["kaldirma_hortumu_MGPM"]["min"], H_["kaldirma_hortumu_MGPM"]["max"]))
    pp_ = bbx("pano_plakasi")
    H_["pano_erisim"] = dict(derinlik=Z_ON - pp_.zmax, y=(pp_.ymin, pp_.ymax), v5_derinlik=0.0 - pp_.zmax)
    UYARI.append("pano erişimi (AÇIK): pano plakasının ön yüzü ön düzlemden %.0f mm derinde (v5: %.0f; +79 ile uzadı), y %.0f–%.0f (1,47–1,86 m) → önden kablolama / servis zor: "
                 "menteşeli / öne çekilir pano plakası ya da servisin arkadan yapılması karar ister (tank dolumu 619 mm derinde, aynı konu)" % (Z_ON - pp_.zmax, -pp_.zmax, pp_.ymin, pp_.ymax))
    # ---- 10 · açıklıklar + temizlik ----
    ac = []
    for a, (y0, y1, z0, z1), x0 in (("sol_sac_urun_girisi", URUN_GIRISI, 0.0), ("sag_sac_E_penceresi", E_PENCERE, W - SAC)):
        ac.append(_sek(a).intersect(kutu_((x0 - 0.1, x0 + SAC + 0.1), (y0 + 0.01, y1 - 0.01), (z0 + 0.01, z1 - 0.01))).Volume())
    kontrol("ürün açıklıkları yan saclarda AYNI ve BOŞ: fırın → K girişi y %.0f–%.0f z %.0f…%.0f · K → E penceresi y %.0f–%.0f z %.0f…%.0f · K ön yüzünde açıklık YOK (ürün ön yüzden geçmez, K'de robot noktası yok)"
            % (URUN_GIRISI + E_PENCERE), all(v < 0.01 for v in ac), str(ac))
    hb = [p["ad"] for p in PARCALAR if p["ad"].startswith("hava_besleme")]
    it = _sek("istasyon_tabani_3").Volume()
    it_b = (W - 2 * SAC) * 3.0 * (D - SAC + Z_KABUK_ON) - sum((x1 - x0) * 3.0 * (Z_KABUK_ON - Z_CER[0]) for x0, x1 in (CER_X_SOL, CER_X_SAG)) - 2 * 30.0 * 3.0 * 30.0
    kontrol("hava_besleme_K YOK (MS4 zaten üstten ANA_K48 ile beslenir) · istasyon tabanında delik YOK (hacim %.0f = düz sac − 2 ön + 2 arka dikme çentiği %.0f mm³)" % (it, it_b), not hb and abs(it - it_b) < 1.0)
    UYARI.append("montaj (hat_montaj_v62 → yeni sürüm): K_BIRIM'e 'onyuz_' + 'bulasik_tabla' + 'bulasik_tavasi' + 'bulasik_gecis' öneki · ÖN YÜZ denetimi z ≤ 79,5 · SOZLESME bulaşık y 126 → %.0f + KS.Z_ON = FT.ZS · "
                 "_IZIN K girdileri sil · _KIC y alt sınırı 1 mm pay gereksiz (ayak yok) · bulaşık kapak zarfı ↔ K yazdırması ALT kapak AÇIK (KS.kapak_ac) ile" % BULASIK_YER[1])
    for u in UYARI:
        print("  UYARI: " + u)
    H_["uyari"] = list(UYARI)


''')

# ================================================================ 8 · ÇAKIŞMA · GLB · BOM · ÇIKTI ================================================================
d('''           ("kose_dikmesi", "arka_sac"), ("istasyon_tabani", "_sac"), ("taban_sac", "_sac"), ("plint_on", "taban_sac")]''',
  '''           ("kose_dikmesi", "arka_sac"), ("istasyon_tabani", "_sac"), ("taban_sac", "_sac"), ("onyuz_plint", "taban_sac"),
           # v6 · ön çerçeve + kapaklar + yeni bağlantı parçaları (hepsi yüz teması; hacim 0 beklenir — sayısal gürültüye karşı)
           ("onyuz_cerceve", "_sac"), ("onyuz_cerceve", "istasyon_tabani"), ("onyuz_cerceve_kayit", "onyuz_cerceve_dikme"), ("kopru_kirisi_uc", "onyuz_cerceve_dikme"),
           ("onyuz_mentese_govde", "onyuz_cerceve_dikme"), ("onyuz_mentese_kanat", "onyuz_mentese_govde"), ("onyuz_mentese_kanat", "onyuz_kapak"),
           ("onyuz_basac_mandal", "onyuz_cerceve_dikme"), ("onyuz_basac_karsilik", "onyuz_kapak"), ("onyuz_basac_karsilik", "onyuz_basac_mandal"),
           ("onyuz_kilit_AZM40", "onyuz_cerceve_dikme"), ("onyuz_kilit_dili", "onyuz_kapak"), ("bulasik_tabla_kirisi", "_sac"), ("bulasik_tavasi", "bulasik_tabla_kirisi"),
           ("sensor_braketi", "bant_yan"), ("sensor_braketi", "sensor_"), ("PulsaJet_semeri", "PulsaJet_AA"), ("PulsaJet_semeri", "kafa_plakasi"), ("DGRF_burcu", "DGRF"),
           ("itici_home_braketi", "ZLW"), ("itici_home_braketi", "itici_home_sensoru"), ("pano_ara_burcu", "pano_plakasi"), ("pano_ara_burcu", "arka_sac"),
           ("sartlandirici_montaj", "arka_sac"), ("sartlandirici_montaj", "sartlandirici_MS4"), ("sartlandirici_montaj", "valf_adasi"), ("hava_hortumu_tank", "valf_adasi")]''')
d('    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]', '    sab = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] in SABIT_GRUP]              # v6: kapaklar KAPALI (sabit gibi)', n=2)
d('    GRUPLAR = ["SABIT", "REF", "KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ", "SPREY"]',
  '    GRUPLAR = ["SABIT", "REF", "KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN", "URUN_IZ", "SPREY"] + list(KAPAK_GRUP)      # v6: 3 kapak düğümü (kapalı; açma KS.kapak_ac)' + NL +
  '    assert set(p["grup"] for p in PARCALAR) <= set(GRUPLAR), sorted(set(p["grup"] for p in PARCALAR) - set(GRUPLAR))')
d('"generator": "AUTOKITCH kesme_cad_v5"', '"generator": "AUTOKITCH kesme_cad_v6"')
d('"koli", "kolisi", "hortum", "Avara", "tank")) else "ÜRETİM"', '"koli", "kolisi", "hortum", "Avara", "tank", "EMKA", "Southco", "Ara burç", "Lapp", "Geçiş lastiği", "Dayama lastiği")) else "ÜRETİM"')
# 2. tur (denetçi ORTA-1): ISTISNA listesi BOŞ — v6-1'deki alt-dizgi listesi gerçek çakışmayı (kablo kanalı ↔ köşe dikmesi 82 016 mm³) ve 25 gömülü örtüşmeyi
# gizliyordu; hepsi geometride giderildi (4b), denetim_v6'daki TAM TARAMA istisnasız 0 → cakisma() da istisnasız çalışır
blok('ISTISNA = [("bant_PU", "rulosu"),', 'def _ist(a, b):', """ISTISNA = []      # v6 2. tur: BOŞ — bütün yüz temasları 0 hacim; gömülü geçmeler delik / yuva olarak modellendi (denetim_v6 · TAM TARAMA İSTİSNASIZ 0).
                  # v5 / v6-1'deki alt-dizgi listesi kablo_kanali_dikey ↔ kose_dikmesi_3 (82 016 mm³) gerçek çakışmasını gizliyordu (denetçi ORTA-1).


""")
d('def json_yaz(yol, H_, cak):', '''def e7_ileri():
    """v6 2. tur (denetçi K-13): ürün yolu + itici × E taramalarını E'nin montaj v63 sürümü kutu_cad_v7 ile çalıştırır (K'nin kendi geometrisi kutu_cad_v6'ya bağlı kalır)"""
    global KC
    try:
        import kutu_cad_v7 as K7
    except Exception as e_:
        print("E v7 yuklenemedi: %s" % e_); return None, None
    esk = KC; KC = K7; _E_ON[:] = []
    try:
        print("E v7 ILERI UYUM (kutu_cad_v7):"); a = urun_cakisma(); b = e_itici_cakisma()
    finally:
        KC = esk; _E_ON[:] = []
    return a, b


def json_yaz(yol, H_, cak):''')
d('        cak["itici_E"] = len(e_itici_cakisma()); sys.stdout.flush()',
  '        cak["itici_E"] = len(e_itici_cakisma()); sys.stdout.flush()' + NL +
  '        a7_, b7_ = e7_ileri(); sys.stdout.flush()                                             # v6 2. tur: E v7 ileri uyum' + NL +
  '        if a7_ is not None: cak["urun_E7"] = len(a7_); cak["itici_E7"] = len(b7_)')
d('    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))',
  '    print("DENETIM: %d madde · %d KALDI · cakisma %s · toplam %.0f sn" % (len(DEN), len(kal), cak, time.time() - t0))')
d('surum="kesme_cad_v5 · %s"', 'surum="kesme_cad_v6 · %s"')
d('''    print("K KESME + SPREY v5 (alcak hat: ust 1862 · taban 892 · bant 996 · altinda yalniz bulasik · deterjan YOK): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''',
  '''    print("K KESME + SPREY v6 (on duzlem +79: 3 tava kapak · on cerceve · kopru uc plakalari · bulasik ayaksiz tablada · havada 0): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''')
for a, b in (('"otonom", "hat3d", "kesme_v5.glb")', '"otonom", "hat3d", "kesme_v6.glb")'), ('"arastirma", "4_KESME_v5")', '"arastirma", "4_KESME_v6")'),
             ('"otonom", "hat3d", "kesme_v5.json")', '"otonom", "hat3d", "kesme_v6.json")')):
    d(a, b)

# ================================================================ 9 · SON DENETİM (üretilen metin) ================================================================
_kod = s[s.index(NL + "import csv, io, json"):]                                  # başlık (değişiklik kaydı) hariç
for _ad in (r'ekle\("hava_besleme_K"', r'ekle\("plint_on"', r"bulasik_cad_v1", r"kesme_v5\.(glb|json)", r"4_KESME_v5", r"AUTOKITCH kesme_cad_v5", r"def denetim_v4",
            r"b\.zmax > 0\.5", r"import kutu_cad_v7 as KC\b", r"kose_dikmesi_[01]\b", r'\("kablo_kanali_dikey", "kose_dikmesi"\)', r"import firin_tp10_cad_v7"):
    assert not re.search(_ad, _kod.replace('("plint_on", "hava_besleme_K", "kose_dikmesi_0", "kose_dikmesi_1")', "")), "v6: eski ad / kalıntı: %s" % _ad
for _yeni in ("import bulasik_cad_v2 as BM", "import kutu_cad_v6 as KC", "def denetim_v6", "def kapak_ac", "def kapaklar", "def on_cerceve", "KAPAK_GRUP", "onyuz_plint",
              "kesme_v6.glb", "kesme_v6.json", "4_KESME_v6", '"generator": "AUTOKITCH kesme_cad_v6"', "kopru_kirisi_uc_plakasi_", "bulasik_tavasi", "Z_ON = 79.0",
              "YARIK_ACIK = False", "ISTISNA = []", "def e7_ileri", "TAM TARAMA İSTİSNASIZ", "bulasik_gecis_", "onyuz_dayama_lastigi_alt", "import firin_tp10_cad_v8 as FT8", "def _kati_kes"):
    assert _yeni in s, "v6: eksik: %s" % _yeni
compile(s, "kesme_cad_v6.py", "exec")
hedef = os.path.join(U, "kesme_cad_v6.py")
assert not os.path.exists(hedef), "kesme_cad_v6.py zaten var — üstüne yazılmaz"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kesme_cad_v6.py yazildi · %d satir" % s.count(NL))
