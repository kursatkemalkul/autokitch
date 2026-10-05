# -*- coding: utf-8 -*-
"""kutu_cad_v6 → kutu_cad_v7 (28 Eyl 2026 gece) — SPEC_on_duzlem_v63 §2.6: E KUTU KATLAMA ön düzlem +79, temiz kutu.
  · Z_ON = 79 (montaj sözleşmesi KC.Z_ON = FT.ZS) · arka −830 SABİT → derinlik 909 · iç düzen (z 0 referanslı) AYNEN.
  · gövde: sol / sağ / üst sac ön kenarı +59, taban +57,5, plint onyuz_plint +17,5…+19 (x 0–800 + hat sonu dönüşü), +2 orta ayak.
  · ön yüz (onyuz): tam boy ön dikmeler (sol: koli bandında 1,0 lam → koli yolu serbest) + 2 kayıt · 6 tava panel (304 fırçalı 1,5 · 20 büküm,
    z +59…+79, derz 3): ALT 2 kanat (içecek yedeği) · ORTA sol sabit panel (ROBOT AĞZI x 85–440 · y 886–1062 kesikli) + sağ servis kapağı ·
    ÜST 2 kanat · 10 gizli menteşe + 5 bas-aç (içte). on_ust_kapak + kulbu, ön köşe dikmeleri, yan kapı kulbu KALKTI.
  · havada parçalar bağlandı (v6: 26 bileşen / 126 parça) · NEMA 23 motorlar STEP'in TAMAMIYLA (TC.nema23 flanşı kesiyordu).
  · kinematik (kafa(t), blank açıları, çatal, pizza) v6 ile BİREBİR — olcum_v7 ölçer.
  · denetim: olcum_v7 (v6↔v7 parça listesi · kinematik · ön düzlem · ızgara · koli yolu · kapak açılışı · robot ağzı taraması · havada · asansör stroku · hesaplar)
  · çıktılar: kutu_modulu_v7.glb · 5_PACK_kutu_v7/BOM*.csv (yalnız "glb" / "bom" / "hepsi" argümanıyla)
  · v7b (28 Eyl sabah, bağımsız denetim bulguları — rapor_E.md §8): (1) menteşe = SIFIR ÇIKINTILI 155° (sanal eksen kapak kenarının 20 dışında):
    ≥ 90°'de ALT kanat koli yolunun (ön düzlemin önünde koli boyu 267 dahil) DIŞINDA · (2) kaplin delikli (NBK MDS-25C-6.35-10 aday, Ø25 × 26),
    köprü + flap motorları 8,5 aşağı → mil göbeğe 10,1 dalar, pilot kaplinden uzak, kaplin istisnaları KALKTI · (3) eşik: diş ayakları tabana +
    iki yanda köşebent yan saca · (4) ALT kanatlar kutu kesit (+1,0 iç sac) + 3. menteşe + taban önünde dayama dudağı · (5) braketler L / delikli sac
    (≥ 10 mm bindirme, temas yaması ölçülür) · (7) derz katılardan, ızgara derz çizgilerini de örnekler, kapak 1°…155°.
Önceki: kutu_cad_v6.py (DEĞİŞMEZ)"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v6.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas (dahil) … son (hariç) arası → yeni · ikisi de tam 1 kez geçmeli, sıra bas < son"""
    global s
    assert s.count(bas) == 1 and s.count(son) == 1, (s.count(bas), s.count(son), bas[:60], son[:60])
    i, j = s.index(bas), s.index(son)
    assert i < j, (bas[:60], son[:60])
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 1 · başlık ----------------------------------------------------------------
d('"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v6 (27 Eyl 2026 gece)',
  '"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v7 (28 Eyl 2026 gece) — ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.6, Kemal: "her istasyon kendi' + NL +
  '  başına temiz bir kutu, önden tertemiz düz yüzeyler, içeride havada kalan parça olmasın, robotun gireceği yerlerde boşluk"). Z_ON = 79 (fırın ön yüzü),' + NL +
  '  arka −830 SABİT → derinlik 909; iç düzen z 0 referanslı AYNEN. Ön: tam boy çerçeve + 6 tava panel (304 fırçalı 1,5 · 20 büküm · +59…+79 · derz 3):' + NL +
  '  ALT 2 kanat (içecek yedeği, ≥ 110°) · ORTA sol sabit panel + ROBOT AĞZI (x 85–440 · y 886–1062) + sağ servis kapağı · ÜST 2 kanat (yarım kanat:' + NL +
  '  QR yüzü z 670\'e çarpmaz) · gizli menteşe + bas-aç, kulp yok. Havada parçalar bağlandı; NEMA 23 motorlar STEP\'in tamamıyla. Kinematik v6 ile BİREBİR' + NL +
  '  (olcum_v7). Üretici: yap_kutu_v7.py. Önceki: kutu_cad_v6.py' + NL +
  'AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v6 (27 Eyl 2026 gece)')
d('KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..1862 zeminden (v5 alçak hat) · z 0 ön yüz, −830 arka.',
  'KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..1862 zeminden (v5 alçak hat) · z 0 eski ön yüz (iç düzen referansı), −830 arka ·\n'
  '  v7: ÖN DÜZLEM z +79 (Z_ON) — ön panellerin dış yüzü.')

# ---------------------------------------------------------------- 2 · malzeme (SPEC: pu + conta glb listesinde) ----------------------------------------------------------------
d('MALZEME.setdefault("kabuk", dict(renk=(0.78, 0.81, 0.85, 0.14), met=0.3, ruf=0.4, saydam=True))     # dış sac: GLB\'de saydam (mekanizma görünsün)' + NL,
  'MALZEME.setdefault("kabuk", dict(renk=(0.78, 0.81, 0.85, 0.14), met=0.3, ruf=0.4, saydam=True))     # dış sac: GLB\'de saydam (mekanizma görünsün)' + NL +
  'MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))        # v7 (SPEC_on_duzlem_v63): tek başına GLB çıktısında KeyError olmasın' + NL +
  'MALZEME.setdefault("conta", dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8))' + NL)

# ---------------------------------------------------------------- 3 · v7 sabitleri ----------------------------------------------------------------
d('KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 980,8)' + NL,
  'KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 980,8)' + NL + r'''# ---- v7 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1 + §2.6) — iç düzen z 0 referanslı ve arka −830 AYNEN kalır; yalnız öne 79 uzama ----
Z_ON = 79.0                     # bütün ön panellerin DIŞ yüzü = fırın gövdesinin ön yüzü (montaj sözleşmesi: KC.Z_ON = FT.ZS) · derinlik D + Z_ON = 909
TAVA, TAVA_T = 20.0, 1.5        # kuru istasyon kapağı / sabit panel: 304 fırçalı 1,5 sac, kenarlar 20 arkaya bükülü (tava panel)
Z_PANEL = Z_ON - TAVA           # +59 · tava panellerin arka kenarı = sol / sağ / üst sacın ön kenarı
Z_TABAN_ON = Z_ON - 21.5        # +57,5 · taban sacının ön kenarı (SPEC)
Z_CERCEVE = (Z_PANEL - 30.0, Z_PANEL)       # +29 … +59 · ön çerçeve (dikme + kayıt): ön yüzü kapak arkasına yaslanır (kapak dayaması)
Z_PLINT = (Z_ON - 61.5, Z_ON - 60.0)        # +17,5 … +19 · plint ön düzlemin 60 gerisinde (hat boyunca tek çizgi)
PLINT_GERI = 30.0               # hat sonunda (x 830) plint dönüşü 30 içeride (B'nin x 30 / 3970 dönüşleriyle aynı mantık)
DERZ = 3.0
Y_ALT = (Y_PLINT + DERZ, 883.0)             # ALT kanatlar (içecek yedeği) y 126–883
Y_ORTA = (886.0, 1305.0)                    # ORTA bant: sol sabit panel + ROBOT AĞZI + sağ servis kapağı
Y_UST = (1308.0, H - DERZ)                  # ÜST kanatlar y 1308–1859
X_ORTA_DERZ = (414.5, 417.5)                # iki kanat arası derz (hat x 5014,5–5017,5)
AGIZ = dict(x=(85.0, 440.0), y=(Y_ORTA[0], 1062.0))   # ROBOT AĞZI (hat x 4685–5040): çatal + kutu yolu t 13,9–17,3 (SPEC)
LAM = 1.0                       # sol dikmenin koli bandındaki lamı x 1,5–2,5 → sol sütun kolisi (x 3–403) ile 0,5 mm pay
Y_DIKME_SOL = 520.0             # sol dikmenin kutu profili bunun üstünde (koli üstü 499 + 21)
QR_Z = 670.0                    # QR teslim dolabının robot yüzü (qr_cad_v1.py:27) — kanatlar açılınca buraya çarpmamalı
AYAK_XZ = ((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0), (415.0, -40.0), (415.0, -300.0))   # v7: +2 orta ayak (taban açıklığı 827 → 413)
KAPI_ADLARI = ("onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag", "onyuz_orta_servis_kapagi", "onyuz_ust_kanat_sol", "onyuz_ust_kanat_sag")
# ---- v7b (bağımsız denetim 28 Eyl) ----
MENTESE_OFSET = TAVA            # SIFIR ÇIKINTILI (zero protrusion) gizli menteşe: sanal dönme ekseni kapağın menteşe kenarının TAVA (20) DIŞINDA, ön düzlemde →
                                #   90°'de kapağın iç yüzü yan sacın iç yüzüne (sol x 1,5) gelir; koli yolu (x 3–805) kapakla kesişmez. Aday Blum CLIP top 155° zero protrusion
KAPI_MAX_ACI = 155.0            # menteşe açılış sınırı (Blum 71B7550 ailesi: 155°)
KOLI_ACI = 90.0                 # ALT kanat bu açıdan itibaren koli çekme yolu (ön düzlemin önünde koli boyu 267 dahil) SERBEST — işletme açısı
KUTU_KANAT = ("onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag")   # ALT kanatlar KUTU KESİT: tava + 1,0 iç kapatma sacı (burulma: menteşeler koli bandının üstünde kalmak zorunda)
IC_SAC = 1.0
KAPLIN = dict(d=25.0, L=26.0, gobek=11.0, pay_ust=2.0)          # aday NBK MDS-25C-6.35-10 (tek diskli sıkma) · Ø25 · boy 26 + göbek 11 VARSAYIM (föy açılamadı) · üstte yatağa 2 pay
MIL_UCU = 31.557 - 10.973       # STP-MTR-23079 STEP: mil ucu flanş yüzünden 20,584 (ölçüldü)
MOTOR_INDIR = 8.5               # köprü + flap katlayıcı motorları 8,5 aşağı → mil kaplinin motor göbeğine 10,1 dalar (≤ göbek 11), pilot kaplinden 9 uzak
ESIK_DIS = ((X_BL0, 188.0), (222.0, 383.0), (417.0, 578.0), (612.0, X_BL1))   # şarjör eşiği tarağının 4 dişi (X_TIRNAK ± 2 yarıkları arası)
ESIK_AYAK = 12.5                # diş ayağı: eşiğin önüne (z −411,5 → −399) bükülü 3 mm · tabana 2 × M5 (taban delikleri z −397'den başlar)
ESIK_KOS_Y = (880.0, 930.0)     # eşik köşebentleri (sol + sağ yan saca): üst köşebentlerin (940) altında, blank yolunun (981,6) altında
FOTOSEL_BRAKET_BOM = ("Fotosel braketi Al · L 3 mm", 1, "Omron E3Z 2 × M3 ile · yan saca 27 × 20 kol, 2 × M4", "v7b · üretim (v7 ilk: 3 mm kenarla yan saca — denetim bulgusu 5)")
SENSOR_BRAKET_BOM = ("Sensör braketi · delikli sac (Ø8, M8 endüktif) + L / Z kol", 1, "sensör deliğe 2 × M8 somunla (iki ucu açık) · taşıyıcıya ≥ 10 mm bindirme, 2 × M4",
                     "v7b · üretim (v7 ilk: düz lam / teğet temas — denetim bulgusu 5)")
''')

# ---------------------------------------------------------------- 4 · NEMA 23: STEP'in tamamı ----------------------------------------------------------------
blok('def nema23(ad, P, eksen, yukari, grup="SABIT"):', 'def pgcn23(ad, P, eksen, yukari, grup="SABIT"):', r'''Z_FLANS_STEP = 10.973           # v7: STP-MTR-23079 STEP'inde flanşın ön yüzü (ölçüldü: düzlem yüz z 10,973 · pilot Ø38,1 üstü 12,497 · mil Ø6,35 ucu 31,557)
_MOT_TAM = {}


def _nema23_tam():
    """v7 · STEP'in TAMAMI. TC.nema23() gövdeyi STEP z 0'dan kesiyor → gerçek motorun ön 11 mm'si (flanş) + pilot + mil modelde yoktu
    (gövde 64,5 görünüyordu; katalog 23079 ≈ 79). Burada flanş ön yüzü z 0: gövde −z (75,5), pilot Ø38,1 × 1,5 + mil Ø6,35 +z (ucu +20,6).
    Kablo telleri hariç (TC ile aynı ayrım: ymin < −80 olan katılar)."""
    if "g" not in _MOT_TAM:
        w = cq.importers.importStep(TC.MOTOR_STEP)
        gov = [x for x in w.val().Solids() if x.BoundingBox().ymin >= -80.0]
        g = gov[0]
        for x in gov[1:]:
            g = g.fuse(x)
        _MOT_TAM["g"] = g.translate(cq.Vector(0.0, 0.0, -Z_FLANS_STEP))
    return _MOT_TAM["g"]


def nema23(ad, P, eksen, yukari, grup="SABIT"):
    """AutomationDirect SureStep STP-MTR-23079 · gerçek STEP (v7: tam boy) · P = flanş ön yüzü (mil yüzü), gövde −eksen yönünde, mil +eksen"""
    # kanonik: mil +z, gövde −z
    ex = capraz(yukari, eksen)
    ekle(ad, cq.Workplane(obj=tasi(_nema23_tam(), eksen_matrisi(ex, yukari, eksen, P))), "motor", grup,
         ("Step motor AutomationDirect SureStep STP-MTR-23079", 1, "NEMA 23 · 1,95 N·m (276 oz-in) · 2,8 A · gövde 75,5 + pilot Ø38,1 + mil Ø6,35 × 20,6 (STEP ölçüsü, v7)",
          "automationdirect.com STP-MTR-23079 · TraceParts STEP"))


''')

# ---------------------------------------------------------------- 4b · kaplin: delikli, katalog adayı (v7b · denetim bulgusu 2) ----------------------------------------------------------------
d('''def kaplin(ad, x, y, z, eksen="y", grup="SABIT"):
    k = sily(x, z, 12.5, y, y + 30.0) if eksen == "y" else (silz(x, y, 12.5, z, z + 30.0) if eksen == "z" else silx(y, z, 12.5, x, x + 30.0))
    ekle(ad, k, "aluminyum", grup, ("Kaplin (kavramalı) Ø25 × 30", 1, "8 × 12 / 8 × 10 delik", "MISUMI MCKL / Ruland · katalog"))''',
  '''def kaplin(ad, x, y, z, eksen="y", grup="SABIT"):
    """v7b · tek diskli sıkma kaplin Ø25 × L (aday NBK MDS-25C-6.35-10) · y = ALT (motor tarafı) yüzü, dikey eksen.
    Motor göbeği Ø6,4 delik (mil Ø6,35 oturur, katı bindirmesi YOK) · vida göbeği Ø10 delik (BK12 uç muylusu) · ortada disk bölgesi dolu.
    v7 ilk hali: dolu Ø25 × 30 motor flanşından başlıyordu → Ø38,1 pilota 1,5 biniyordu ve istisna listesi bunu gizliyordu (denetim bulgusu 2)."""
    assert eksen == "y", "v7b: kaplin yalnız dikey eksen"
    L_, gb = KAPLIN["L"], KAPLIN["gobek"]
    k = sily(x, z, KAPLIN["d"] / 2.0, y, y + L_).cut(sily(x, z, 3.2, y - 1.0, y + gb)).cut(sily(x, z, 5.0, y + L_ - gb, y + L_ + 1.0))
    ekle(ad, k, "aluminyum", grup, ("Kaplin tek diskli sıkma Ø25 × %.0f (aday NBK MDS-25C-6.35-10)" % L_, 1,
                                    "delik 6,35 (motor) × 10 (vida muylusu) · motor mili göbeğe ≈ 10 dalar (göbek %.0f, olcum_v7 ölçer)" % gb,
                                    "nbk1560.com MDS-25C (parça no mevcut) · boy / göbek VARSAYIM (föy açılamadı)"))''')
d('''    kaplin("kopru_kaplini", 47.0, 784.5, ZB)
    nema23("kopru_motoru", (47.0, 784.5, ZB), (0, 1, 0), (0, 0, 1))
    ekle("kopru_motor_braketi", kut(17.0, 77.0, 784.5, 790.5, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, 783, 792)), "aluminyum")''',
  '''    Y_KM = 784.5 - MOTOR_INDIR          # v7b: motor flanşı 776 (v7 ilk 784,5) — mil ucu 796,6 kaplinin motor göbeğinde (786,5–797,5)
    kaplin("kopru_kaplini", 47.0, 814.5 - KAPLIN["pay_ust"] - KAPLIN["L"], ZB)     # v7b: BK12 altı 814,5 − 2 − 26 = 786,5
    nema23("kopru_motoru", (47.0, Y_KM, ZB), (0, 1, 0), (0, 0, 1))
    ekle("kopru_motor_braketi", kut(17.0, 77.0, Y_KM, Y_KM + 6.0, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, Y_KM - 1.5, Y_KM + 7.5)), "aluminyum")''')
d('''    nema23("flap_katlayici_motoru", (750.0, 694.0, -300.0), (0, 1, 0), (0, 0, 1))
    kaplin("flap_katlayici_kaplini", 750.0, 694.0, -300.0)
    ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, 694.0, 700.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, 693, 701)), "aluminyum")''',
  '''    Y_FM = 694.0 - MOTOR_INDIR          # v7b: motor flanşı 685,5 (v7 ilk 694) — gövde alt raf kesiğinden geçer, raf köşebendinde çentik
    nema23("flap_katlayici_motoru", (750.0, Y_FM, -300.0), (0, 1, 0), (0, 0, 1))
    kaplin("flap_katlayici_kaplini", 750.0, 724.0 - KAPLIN["pay_ust"] - KAPLIN["L"], -300.0)    # v7b: yatak braketi altı 724 − 2 − 26 = 696
    ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, Y_FM, Y_FM + 6.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, Y_FM - 1.0, Y_FM + 7.0)), "aluminyum")''')
d('''    ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, 694.0, 826.0, -330.0, -270.0), "aluminyum")''',
  '''    ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, Y_FM, 826.0, -330.0, -270.0), "aluminyum")''')
d('''    ("_kaplini", "_motoru"), ("_kaplini", "_vidasi_mil"), ("_kaplini", "_BK12"),
''', '''    # v7b: ("_kaplini", "_motoru" | "_vidasi_mil" | "_BK12") istisnaları KALKTI — kaplin delikli, hiçbir parçaya binmiyor (olcum_v7 ölçer)
''')
d('''# Ön köşe dikmeleri (z −21,5…−1,5) ve kablo_kanali_dikey_alt (x 801–826 · z −50…−25) önde olduğu için koliler geride: z −350…−83.''',
  '''# v6 gerekçesi: ön köşe dikmeleri (z −21,5…−1,5) ve kablo_kanali_dikey_alt (x 801–826 · z −50…−25) önde olduğu için koliler geride: z −350…−83.
# v7: ön köşe dikmeleri KALKTI, dikey kanal x 806–826; koli yeri AYNI (kayıtlı ölçü) — önünde ALT kanatlar (kapak açıkken koli yolu serbest, olcum_v7).''')

# ---------------------------------------------------------------- 5 · gövde + ön yüz ----------------------------------------------------------------
blok("def govde():", "# ---------------------------------------------------------------- ŞARJÖR + ASANSÖR", r'''def govde():
    # ayaklar + taban · v7: +2 orta ayak x 415 (z −40 / −300): 3 mm taban 827 açıklıkta içecek yedeği altında ~33 mm sehim → ~2 mm (olcum_v7 hesabı)
    for i, (ax, az) in enumerate(AYAK_XZ):   # v3: ön ayaklar süpürgeliğin arkasında
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik",
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz · taban Ø40 · v7: 4 köşe + 2 orta", "elesa-ganter.com LV.A-SST") if i == 0 else None)
    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, Z_TABAN_ON).cut(sily(405.0, -392.0, 8.0, Y_PLINT - 1, Y_PLINT + 4))   # v3: vida alt ucu (Ø12) için Ø16 delik · v7: ön kenar +57,5
    taban = taban.cut(sily(480.0, -392.0, 5.0, Y_PLINT - 1, Y_PLINT + 4))      # v7: asansör motor mili ucu (STEP tam boy: flanştan 20,6 → y 124,6) için Ø10 delik
    ekle("taban_sac_3", taban, "sac")
    # kabuk · v7: sol / sağ / üst sac ön kenarı Z_PANEL (+59 = tava kapakların arkası) · arka −830 SABİT
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, Z_PANEL), "kabuk")
    sol = kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, Z_PANEL).cut(kut(-1, SAC + 1, PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3]))   # pizza penceresi (v5 978–1062)
    ekle("sol_sac_pizza_penceresi", sol, "kabuk")
    sag = kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, Z_PANEL).cut(kut(W - SAC - 1, W + 1, 232.0, 988.0, -822.0, -412.0))  # şarjör yan kapısı (v5 üstü 1156 − 168)
    ekle("sag_sac", sag, "kabuk")
    ekle("sarjor_yan_kapisi", kut(W - SAC, W, 234.0, 986.0, -820.0, -414.0), "kabuk")
    # v7: yan kapı MENTEŞESİZ + dış kulplu idi (v6: havada; kulp 22 mm dışarıda) → arka kenarda 2 gizli menteşe + ön kenarda bas-aç (ikisi de İÇTE), kulp KALKTI.
    #     Sağ kılavuz (UHMW + taşıyıcı) KAPIDA kalır: kapı açılınca yığının sağ yanı tamamen açılır (yan yükleme) — KARAR (varsayım)
    for i, yc in enumerate((300.0, 900.0)):
        ekle("sarjor_yan_kapisi_mentese_%d" % i, kut(W - SAC - 8.5, W - SAC, yc - 25.0, yc + 25.0, -826.0, -814.0), "celik",
             bom=("Gizli menteşe · yan kapı (içte, 1,5 sac kapı)", 1, "arka kenar · kapı ↔ yan sac kesim kenarı", "VARSAYIM ölçü 8,5 × 50 × 12 · üretici / parça no BULUNAMADI"))
    ekle("sarjor_yan_kapisi_basac", kut(W - SAC - 8.5, W - SAC, 590.0, 630.0, -418.0, -406.0), "plastik",
         bom=("Bas-aç mandalı (push-to-open, mıknatıslı)", 1, "yan kapı ön kenarı · içte", "VARSAYIM ölçü · Southco push-to-open ailesi, parça no BULUNAMADI"))
    # ağız üst kirişi (ön kose plow'larını tasir) — kapak dik dururken onun ONUNDE (z > -46,5)
    ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1162.0, 1177.0, -40.0, -20.0), "celik")
    # v7: on_ust_kapak + kulbu + ön köşe dikmeleri (L 20, y 126–917) KALKTI → onyuz(): tam boy ön çerçeve + tava paneller (+59…+79)


# ---------------------------------------------------------------- ÖN YÜZ (v7 · SPEC_on_duzlem_v63 §2.6) ----------------------------------------------------------------
def kutu_profil(x0, x1, y0, y1, z0, z1, et=2.0, eksen="y"):
    """v7 · dikdörtgen kutu profil (304, et kalınlığı), boyu 'eksen' yönünde (y ya da x), uçları açık"""
    if eksen == "y":
        return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + et, x1 - et, y0 - 1.0, y1 + 1.0, z0 + et, z1 - et))
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + et, y1 - et, z0 + et, z1 - et))


def tava(x0, x1, y0, y1, kes=None):
    """v7 · TAVA PANEL (SPEC §1 kuru istasyon kapağı): 304 fırçalı 1,5 sac, dört kenar 20 arkaya bükülü → z Z_PANEL…Z_ON.
    kes = kenardan açılan dikdörtgen kesik (x0, x1, y0, y1): kesik kenarları da 20 arkaya bükülü (çapaksız)"""
    dis = kut(x0, x1, y0, y1, Z_PANEL, Z_ON)
    ic = kut(x0 + TAVA_T, x1 - TAVA_T, y0 + TAVA_T, y1 - TAVA_T, Z_PANEL - 1.0, Z_ON - TAVA_T)
    if kes:
        a, b, c, d_ = kes
        dis = dis.cut(kut(a, b, c, d_, Z_PANEL - 1.0, Z_ON + 1.0))
        ic = ic.cut(kut(a - TAVA_T, b + TAVA_T, c - TAVA_T, d_ + TAVA_T, Z_PANEL - 2.0, Z_ON + 2.0))
    return dis.cut(ic)


ON_PANEL = (   # ad, x0, x1, y0, y1, menteşe tarafı ("sol" / "sag" · None = sabit panel), kenardan kesik — hepsi tava 20, z +59…+79, derz 3
    ("onyuz_alt_kanat_sol", SAC, X_ORTA_DERZ[0], Y_ALT[0], Y_ALT[1], "sol", None),
    ("onyuz_alt_kanat_sag", X_ORTA_DERZ[1], W, Y_ALT[0], Y_ALT[1], "sag", None),
    ("onyuz_orta_sabit_panel", SAC, AGIZ["x"][1], Y_ORTA[0], Y_ORTA[1], None, (AGIZ["x"][0], AGIZ["x"][1] + 1.0, Y_ORTA[0] - 1.0, AGIZ["y"][1])),
    ("onyuz_orta_servis_kapagi", AGIZ["x"][1] + DERZ, W, Y_ORTA[0], Y_ORTA[1], "sag", None),
    ("onyuz_ust_kanat_sol", SAC, X_ORTA_DERZ[0], Y_UST[0], Y_UST[1], "sol", None),
    ("onyuz_ust_kanat_sag", X_ORTA_DERZ[1], W, Y_UST[0], Y_UST[1], "sag", None),
)
# menteşe yükseklikleri: ALT kanatlarda koli bandının (y 130–499) ÜSTÜNDE — menteşe gövdesi koli yoluna girmez ·
# v7b: ALT kanatlar kutu kesit (≈ 6,7 kg) → 3 menteşe (Blum kılavuzu: ≤ 900 mm kapakta 15 lb / 6,8 kg üstü 3 menteşe — okuma VARSAYIM)
MENTESE_Y = {"onyuz_alt_kanat_sol": (560.0, 680.0, 800.0), "onyuz_alt_kanat_sag": (560.0, 680.0, 800.0), "onyuz_orta_servis_kapagi": (950.0, 1230.0),
             "onyuz_ust_kanat_sol": (1390.0, 1780.0), "onyuz_ust_kanat_sag": (1390.0, 1780.0)}
BASAC_YER = (("onyuz_alt_kanat_sol", X_ORTA_DERZ[0] - 20.0, X_ORTA_DERZ[0], Y_ALT[1] - 60.0, Y_ALT[1] - 30.0),      # orta kayıtın altında
             ("onyuz_alt_kanat_sag", X_ORTA_DERZ[1], X_ORTA_DERZ[1] + 20.0, Y_ALT[1] - 60.0, Y_ALT[1] - 30.0),
             ("onyuz_orta_servis_kapagi", AGIZ["x"][1] + DERZ, AGIZ["x"][1] + DERZ + 20.0, Y_ORTA[1] - 60.0, Y_ORTA[1] - 30.0),   # üst kayıtın altında
             ("onyuz_ust_kanat_sol", X_ORTA_DERZ[0] - 20.0, X_ORTA_DERZ[0], Y_ORTA[1], Y_ORTA[1] + 30.0),                          # üst kayıtın üstünde
             ("onyuz_ust_kanat_sag", X_ORTA_DERZ[1], X_ORTA_DERZ[1] + 20.0, Y_ORTA[1], Y_ORTA[1] + 30.0))
MENTESE_KAPI = {}               # menteşe parçası → kapak (kapak açılış denetimi kendi menteşesini saymaz)


def onyuz():
    """v7 · ÖN YÜZ (SPEC_on_duzlem_v63 §2.6): ön çerçeve (2 tam boy dikme + 2 kayıt, z +29…+59) · 6 tava panel (z +59…+79, derz 3) ·
    10 gizli menteşe + 5 bas-aç (içte) · plint (+17,5…+19). Önden yalnız düz yüzey + derz + ROBOT AĞZI görünür (kulp / vida / menteşe yok)."""
    zc0, zc1 = Z_CERCEVE
    # ön çerçeve — sol dikme: koli bandında (y 126–520) sol yan saca kaynaklı 1,0 lam (x 1,5–2,5 → sol sütun kolisinin yolu x ≥ 3 serbest),
    # üstünde 20 × 30 × 2 kutu profil · sağ dikme tam boy kutu profil x 808,5–828,5 (sağ sütun kolisi x ≤ 805, kablo kanalı x 806–826 z −50…−25)
    d_ = kut(SAC, SAC + LAM, Y_ALT[0], Y_DIKME_SOL, zc0, zc1).union(kutu_profil(SAC, SAC + 20.0, Y_DIKME_SOL, H - SAC, zc0, zc1))
    ekle("onyuz_dikme_sol", d_, "sac", bom=("Ön dikme sol · 304 kutu profil 20 × 30 × 2 + 1,0 lam", 1,
         "profil y %.0f–%.1f · lam y %.0f–%.0f (koli bandı: yol serbest) · yan saca kaynaklı" % (Y_DIKME_SOL, H - SAC, Y_ALT[0], Y_DIKME_SOL), "v7 · üretim"))
    ekle("onyuz_dikme_sag", kutu_profil(W - SAC - 20.0, W - SAC, Y_ALT[0], H - SAC, zc0, zc1), "sac",
         bom=("Ön dikme sağ · 304 kutu profil 20 × 30 × 2", 1, "y %.0f–%.1f · yan saca kaynaklı" % (Y_ALT[0], H - SAC), "v7 · üretim"))
    for ad_, y1 in (("onyuz_kayit_orta", Y_ALT[1]), ("onyuz_kayit_ust", Y_ORTA[1])):
        ekle(ad_, kutu_profil(SAC + 20.0, W - SAC - 20.0, y1 - 30.0, y1, zc0, zc1, eksen="x"), "sac",
             bom=("Ön kayıt · 304 kutu profil 30 × 30 × 2", 1, "boy %.0f · derz arkasında (üst yüzü y %.0f) · dikmelere kaynaklı" % (W - 2 * SAC - 40.0, y1), "v7 · üretim"))
    # tava paneller · v7b: ALT kanatlar KUTU KESİT — tavanın içine 1,0 kapatma sacı (z +59…+60, bükümlere kaynaklı, menteşe yerlerinde pencere):
    #   açık tava (J ≈ 505 mm⁴) burulmada yumuşaktı; menteşeler koli bandının üstünde kalmak zorunda olduğundan alt serbest köşe 404 mm konsol (denetim bulgusu 4)
    xm = {"sol": SAC + 20.0, "sag": W - SAC - 40.0}           # menteşe gövdesinin x başlangıcı (dikme iç yüzü)
    for ad_, x0, x1, y0, y1, taraf, kes in ON_PANEL:
        sh_ = tava(x0, x1, y0, y1, kes)
        if ad_ in KUTU_KANAT:
            ic_ = kut(x0 + TAVA_T, x1 - TAVA_T, y0 + TAVA_T, y1 - TAVA_T, Z_PANEL, Z_PANEL + IC_SAC)
            for yc in MENTESE_Y[ad_]:
                ic_ = ic_.cut(kut(xm[taraf] - 1.0, xm[taraf] + 21.0, yc - 31.0, yc + 31.0, Z_PANEL - 1.0, Z_PANEL + IC_SAC + 1.0))
            sh_ = sh_.union(ic_)
        ekle(ad_, sh_, "sac",
             bom=("Tava %s 304 fırçalı 1,5 · 20 büküm%s" % ("kapak" if taraf else "sabit panel", " + 1,0 iç kapatma sacı (kutu kesit)" if ad_ in KUTU_KANAT else ""), 1,
                  "%.1f × %.1f · %s" % (x1 - x0, y1 - y0, ("gizli menteşe %s (sıfır çıkıntılı 155°) · bas-aç · kulpsuz" % taraf) if taraf else
                                        "ROBOT AĞZI kesikli (x %.0f–%.0f · y %.0f–%.0f, kenarları bükülü) · arkadan kaynaklı M5 saplamalı" % (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1])),
                  "v7 · SPEC_on_duzlem_v63"))
    # gizli menteşeler: dikmenin iç yüzü (x 21,5 | 808,5) ↔ kapağın iç ön yüzü (z +77,5) · v7b: SIFIR ÇIKINTILI — sanal eksen kapak kenarının 20 DIŞINDA (kapi_matrisi)
    MENTESE_KAPI.clear()
    n = 0
    for ad_, x0, x1, y0, y1, taraf, kes in ON_PANEL:
        if not taraf:
            continue
        xa = xm[taraf]
        for yc in MENTESE_Y[ad_]:
            m_ = "onyuz_mentese_%d" % n
            ekle(m_, kut(xa, xa + 20.0, yc - 30.0, yc + 30.0, Z_PANEL - 10.0, Z_ON - TAVA_T), "celik",
                 bom=("Gizli menteşe · sıfır çıkıntılı 155°, tam bindirme (aday Blum CLIP top 71B7550 ailesi; bas-aç için yaysız sürüm)", 1,
                      "90°'de kapak iç yüzü yan sac iç yüzünde → koli / servis yolu açık · kılavuz: ≤ 900 mm kapakta 6,8 kg'a kadar 2, üstü 3 menteşe (okuma VARSAYIM)",
                      "blum.com 71B7550 (155° zero protrusion, kapak ≤ 24 mm) · sac kapakta Ø35 kap yuvası kaynaklı · yaysız parça no + ölçü VARSAYIM 20 × 60 × 28,5"))
            MENTESE_KAPI[m_] = ad_
            n += 1
    # v7b · ALT dayama dudağı: taban ön kenarında 304 lama (y 126–129 · z +45…+59) — ALT kanatların alt bükümü + iç sacı buna yaslanır (içe dayama);
    #   koli tabanı 130 (altlık üstü) → koli yolunun 1 mm altında, yolu kapatmaz · lam (x 2,5) ile sağ dikme (x 808,5) arasında
    ekle("onyuz_alt_dayama_dudagi", kut(SAC + LAM, W - SAC - 20.0, Y_ALT[0], Y_ALT[0] + 3.0, Z_PANEL - 14.0, Z_PANEL), "sac",
         bom=("ALT kanat dayama dudağı 304 lama 3 × 14", 1, "x %.1f–%.1f · tabana kaynaklı · ALT kanatların alt kenarı yaslanır (koli yolunun 1 mm altında)" % (SAC + LAM, W - SAC - 20.0), "v7b · üretim"))
    for i, (ad_, x0, x1, y0, y1) in enumerate(BASAC_YER):
        ekle("onyuz_basac_%d" % i, kut(x0, x1, y0, y1, Z_PANEL - 20.0, Z_PANEL - 2.0), "plastik",
             bom=("Bas-aç mandalı (push-to-open, mıknatıslı)", 1, "%s serbest kenarı · kayıta vidalı · pim kapak kenar bükümüne basar (2 mm)" % ad_,
                  "VARSAYIM ölçü 20 × 30 × 18 · Southco push-to-open ailesi, parça no BULUNAMADI"))
    # plint: x 0 (K ile birleşir) … 800 + hat sonu dönüşü (x 798,5–800, 30 içeride) · klipsli, sökülür (asansör tahrikine servis)
    pl = kut(0.0, W - PLINT_GERI, 0.0, Y_PLINT, Z_PLINT[0], Z_PLINT[1]).union(kut(W - PLINT_GERI - SAC, W - PLINT_GERI, 0.0, Y_PLINT, -D + PLINT_GERI, Z_PLINT[0]))
    ekle("onyuz_plint", pl, "sac", bom=("Plint (süpürgelik) 304 fırçalı 1,5", 1, "ön x 0–%.0f · z +%.1f…+%.1f (ön düzlemin 60 gerisi) + hat sonu dönüşü · klipsli, sökülür"
                                        % (W - PLINT_GERI, Z_PLINT[0], Z_PLINT[1]), "v7"))


''')

# ---------------------------------------------------------------- 6 · şarjör: eşik tabana, ray plakası tabana + üst köşebentler, sensör braketi ----------------------------------------------------------------
d('''    kapi = kut(X_BL0, X_BL1, 244.0, Y_KAPI_UST, Z_KAPI0, Z_KAPI1)
    for x0, x1 in X_TIRNAK:
        kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, 243.0, 944.0, Z_KAPI0 - 1, Z_KAPI1 + 1))''',
  '''    kapi = kut(X_BL0, X_BL1, Y_PLINT + 3.0, Y_KAPI_UST, Z_KAPI0, Z_KAPI1)      # v7: eşik tabana iner (v6: y 244'te başlıyor, hiçbir yere değmiyordu) — 4 dişli tarak
    for x0, x1 in X_TIRNAK:
        kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, Y_PLINT + 2.0, 944.0, Z_KAPI0 - 1, Z_KAPI1 + 1))   # v7: asansör çatalı yarıkları alttan açık (platform en altta y 229)
    for x0, x1 in ESIK_DIS:     # v7b: her dişin altında ÖNE bükülü 3 mm ayak (tabana 2 × M5) — v7 ilk halinde tabana yalnız 3 mm'lik alt kenarıyla değiyordu (denetim bulgusu 3)
        kapi = kapi.union(kut(x0 + 5.0, x1 - 5.0, Y_PLINT + 3.0, Y_PLINT + 6.0, Z_KAPI1, Z_KAPI1 + ESIK_AYAK))''')
d('''    ekle("sarjor_kapi_esigi", kapi, "sac")''',
  '''    ekle("sarjor_kapi_esigi", kapi, "sac", bom=("Şarjör eşiği 304 · 3 mm tarak (4 diş) + diş ayakları", 1, "804 × 855 · üst kenar 980,8 (2. blankı tutar) · ayaklar tabana 8 × M5 · "
                                                "iki yanda köşebentle yan saca", "v7b · üretim"))
    # v7b · eşik yan köşebentleri: eşiğin ön yüzüne (z −411,5) bindirme 32 × 50 + yan saca 50 × 31,5 (M5) — eşik iki ucundan mesnetli (olcum_v7 sehim hesabı)
    for ad_, x0, x1, xd0, xd1 in (("sol", SAC, X_BL0 + 32.0, SAC, SAC + 3.0), ("sag", X_BL1 - 32.0, W - SAC, W - SAC - 3.0, W - SAC)):
        k_ = kut(x0, x1, ESIK_KOS_Y[0], ESIK_KOS_Y[1], Z_KAPI1, Z_KAPI1 + 3.0).union(kut(xd0, xd1, ESIK_KOS_Y[0], ESIK_KOS_Y[1], Z_KAPI1, Z_KAPI1 + 31.5))
        ekle("sarjor_kapi_esigi_kosebendi_" + ad_, k_, "sac",
             bom=("Eşik köşebendi 304 · L 3 mm (bükümlü)", 1, "eşik ön yüzü ↔ yan sac · 2 + 2 × M5", "v7b · üretim"))''')
d('''    ekle("asansor_ray_plakasi", kut(200.0, 600.0, 150.0, 972.0, -378.0, -374.0), "sac")''',
  '''    ekle("asansor_ray_plakasi", kut(200.0, 600.0, Y_PLINT + 3.0, 972.0, -378.0, -374.0), "sac")     # v7: tabana iner (v6: y 150'de havadaydı)
    # v7b: flanş L (yatay kol tabanda 400 × 20 · dik kol plakanın ön yüzünde 400 × 24) — v7 ilk halinde plakaya yalnız 3 mm'lik kenarıyla değiyordu
    ekle("asansor_ray_plakasi_flansi", kut(200.0, 600.0, Y_PLINT + 3.0, Y_PLINT + 6.0, -374.0, -354.0).union(kut(200.0, 600.0, Y_PLINT + 6.0, 150.0, -374.0, -371.0)), "sac",
         bom=("Ray plakası taban flanşı 304 · L 3 mm", 1, "400 × 20 tabana 4 × M6 · dik kol plakaya 4 × M5", "v7b: plakanın alt mesnedi"))
    # v7b: üst köşebentler plakanın ARKA yüzüne 30 mm bindirir (v7 ilk: aynı düzlemde uç uca 32 × 4) + yan saca dik kol (32 × 26) — L 4 mm + dik kol
    for ad_, x0, x1, xb0, xb1, xd0, xd1 in (("sol", SAC, 230.0, SAC, 230.0, SAC, SAC + 3.0), ("sag", 570.0, W - SAC, 570.0, W - SAC, W - SAC - 3.0, W - SAC)):
        k_ = kut(xb0, xb1, 940.0, 972.0, -382.0, -378.0).union(kut(x0, x1, 968.0, 972.0, -404.0, -382.0)).union(kut(xd0, xd1, 940.0, 972.0, -404.0, -378.0))
        ekle("asansor_ray_plakasi_ust_kosebendi_" + ad_, k_, "sac",
             bom=("Ray plakası üst köşebendi 304 · L 32 × 26 · 4 mm + yan saca dik kol", 1, "plakaya 30 mm bindirme (2 × M5) · yan saca 2 × M5 · yığın momenti", "v7b · üretim"))''')
d('''    e2e("asansor_alt_sensor", 610.0, 150.0, -386.0, "y")''',
  '''    e2e("asansor_alt_sensor", 610.0, 150.0, -386.0, "y")
    # v7b: delikli sensör sacı (Ø8 + 2 somun, iki uç açık) + plakanın arka yüzüne 30 × 13 bindirme (v7 ilk: 4 × 3 mm temas, sensörün alt yüzünü kapatıyordu)
    ekle("asansor_alt_sensor_braketi", kut(570.0, 618.0, 160.0, 163.0, -394.0, -378.0).cut(sily(610.0, -386.0, 4.02, 159.0, 164.0))
         .union(kut(570.0, 600.0, 150.0, 163.0, -381.0, -378.0)), "sac", bom=SENSOR_BRAKET_BOM)''')

# ---------------------------------------------------------------- 7 · besleyici: +2 askı, sensör braketi ----------------------------------------------------------------
d('''    e2e("besleyici_arka_sensor", 600.0, Y_BES_PL - 18.0, -828.0 + 7.5, "z")''',
  '''    e2e("besleyici_arka_sensor", 600.0, Y_BES_PL - 18.0, -828.0 + 7.5, "z")
    for i, xr in enumerate((150.0, 650.0)):      # v7: plaka iki askıyla tek z hattında (−590) asılıydı (öne-arkaya devrilir) → önde 2 askı daha
        ekle("besleyici_plaka_askisi_%d" % (i + 2), kut(xr - 10.0, xr + 10.0, Y_BES_PL + 5.0, H - SAC, -420.0, -400.0), "aluminyum")
    # v7b: delikli sensör sacı (z −812…−809) + plakanın altına 20 × 22 kol (v7 ilk: sensöre teğet çizgiyle değen blok)
    ekle("besleyici_arka_sensor_braketi", kut(590.0, 610.0, Y_BES_PL - 26.0, Y_BES_PL, -812.0, -809.0).cut(silz(600.0, Y_BES_PL - 18.0, 4.02, -813.0, -808.0))
         .union(kut(590.0, 610.0, Y_BES_PL - 3.0, Y_BES_PL, -812.0, -790.0)), "aluminyum", bom=SENSOR_BRAKET_BOM)''')

# ---------------------------------------------------------------- 8 · kalıp: raf kesiği, köşebent sol duvara, sağ takoz ----------------------------------------------------------------
d('''    ekle("kalip_alt_rafi", kut(4.0, 800.0, ALT_RAF_Y[0], ALT_RAF_Y[1], -372.0, -24.0), "sac",''',
  '''    ekle("kalip_alt_rafi", kut(4.0, 800.0, ALT_RAF_Y[0], ALT_RAF_Y[1], -372.0, -24.0).cut(kut(720.0, 780.0, ALT_RAF_Y[0] - 1.0, ALT_RAF_Y[1] + 1.0, -330.0, -270.0)), "sac",   # v7: flap katlayıcı motoru (STEP tam boy, alt ucu 618,5) için 60 × 60 kesik''')
d('''    ekle("kalip_alt_rafi_koseben_sol", kut(2.0, 32.0, _y0 - 30.0, _y0, -372.0, -24.0).cut(kut(5.0, 33.0, _y0 - 31.0, _y0 - 3.0, -373.0, -23.0)), "sac",''',
  '''    ekle("kalip_alt_rafi_koseben_sol", kut(SAC, 32.0, _y0 - 30.0, _y0, -372.0, -24.0).cut(kut(SAC + 3.0, 33.0, _y0 - 31.0, _y0 - 3.0, -373.0, -23.0)), "sac",   # v7: sol yan saca oturur (v6: 0,5 mm havada)''')
d('''    ekle("kalip_alt_rafi_koseben_sag", kut(770.0, 800.0, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(769.0, 797.0, _y0 - 31.0, _y0 - 3.0, -373.0, -54.0)), "sac")''',
  '''    ekle("kalip_alt_rafi_koseben_sag", kut(770.0, 800.0, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(769.0, 797.0, _y0 - 31.0, _y0 - 3.0, -373.0, -54.0))
         .cut(kut(719.0, 781.0, _y0 - 31.0, _y0 + 1.0, -331.0, -269.0)), "sac")   # v7b: yatay kolda flap katlayıcı motoru çentiği (motor 8,5 indi, alt ucu 610)
    ekle("kalip_alt_rafi_duvar_takozu_sag", kut(800.0, W - SAC, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(802.0, W - SAC - 2.0, _y0 - 28.0, _y0 - 2.0, -373.0, -54.0)), "sac",
         bom=("Duvar takozu 304 kutu profil 28,5 × 30 × 2", 1, "sağ köşebent ↔ sağ yan sac (v6: 28,5 mm havada) · kablo kanalının arkasında biter (z −55)", "v7 · üretim"))''')

# ---------------------------------------------------------------- 9 · köprü: tutucu dudağı, motor askısı, sensör braketi ----------------------------------------------------------------
d('''    ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 832.0, 853.0, BZ0 + 20.0, BZ1 - 20.0), "aluminyum")''',
  '''    ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 832.0, 853.0, BZ0 + 20.0, BZ1 - 20.0).union(kut(16.0, 20.0, 847.0, 853.0, BZ0 + 20.0, BZ1 - 20.0)), "aluminyum")   # v7: üst dudak burç plakasına uzar (v6: 4 mm havada) · BK12'nin üstünden geçer''')
d('''    ekle("kopru_motor_askisi", kut(SAC, 16.0, 784.5, 832.0, ZB - 30.0, ZB + 30.0), "aluminyum")''',
  '''    ekle("kopru_motor_askisi", kut(SAC, 17.0, Y_KM, 832.0, ZB - 30.0, ZB + 30.0), "aluminyum")   # v7: motor braketine + BK12'ye değer (v6: 1 mm havada) · v7b: braketle 8,5 iner''')
d('''    e2e("kopru_alt_sensor", 72.0, 862.0, ZB + 34.0, "y")''',
  '''    e2e("kopru_alt_sensor", 72.0, 862.0, ZB + 34.0, "y")
    # v7b: Z büküm — ayak burç plakasının üstüne (15 × 20), dik kol, delikli sensör sacı (y 870–873) · v7 ilk: sensörün alt yüzünü kapatan blok
    ekle("kopru_alt_sensor_braketi", kut(50.0, 65.0, 853.0, 856.0, ZB + 24.0, ZB + 44.0).union(kut(62.0, 65.0, 856.0, 873.0, ZB + 24.0, ZB + 44.0))
         .union(kut(62.0, 86.0, 870.0, 873.0, ZB + 24.0, ZB + 44.0).cut(sily(72.0, ZB + 34.0, 4.02, 869.0, 874.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)''')

# ---------------------------------------------------------------- 10 · piston: sensör braketi, eksen plakası bağları ----------------------------------------------------------------
d('''    e2e("piston_ust_sensor", 385.0, 1782.0, -389.0 + 2.0, "z")''',
  '''    e2e("piston_ust_sensor", 385.0, 1782.0, -389.0 + 2.0, "z")
    # v7b: U büküm — arka kol eksen plakasının ARKA yüzüne (30 × 24), kenarı dolanır, ön kol delikli sensör sacı (v7 ilk: 3 × 5 mm kenar teması)
    ekle("piston_ust_sensor_braketi", kut(340.0, 373.0, 1770.0, 1794.0, -397.0, -394.0).union(kut(370.0, 373.0, 1770.0, 1794.0, -397.0, -380.0))
         .union(kut(370.0, 395.0, 1770.0, 1794.0, -383.0, -380.0).cut(silz(385.0, 1782.0, 4.02, -384.0, -379.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)
    for ad_, x0 in (("sol", 180.0), ("sag", 320.0)):      # v7: eksen plakası besleyici plakasına bağlanır (v6: yalnız üstteki 13,5 mm bloktan asılı) ·
        # v7b: L köşebent — yatay kol besleyici plakasının üstünde (40 × 20 bindirme, cebin arkasında), dik kol eksen plakasının arka yüzünde (40 × 40) · v7 ilk: 5 mm küp
        ekle("piston_eksen_plakasi_bagi_" + ad_, kut(x0, x0 + 40.0, Y_BES_PL + 5.0, Y_BES_PL + 8.0, -420.0, -394.0).union(kut(x0, x0 + 40.0, Y_BES_PL + 8.0, Y_BES_PL + 45.0, -397.0, -394.0)),
             "aluminyum", bom=("Köşebent 6082 · L 3 mm (piston eksen plakası ↔ besleyici plakası)", 1, "2 + 2 × M5", "v7b · üretim"))''')

# ---------------------------------------------------------------- 11 · parmak: redüktör flanş plakası, sensör braketi ----------------------------------------------------------------
d('''    e2e("parmak_sensor", px + 22.0, py + 20.0, -400.0, "z")''',
  '''    e2e("parmak_sensor", px + 22.0, py + 20.0, -400.0, "z")
    ekle("parmak_red_flans_plakasi", kut(px - 29.0, px + 29.0, py - 29.0, py + 45.0, -425.0, -421.0).cut(silz(px, py, 12.0, -426.0, -420.0)), "aluminyum")   # v7: redüktör çıkış flanşı bu plakaya, plaka brakete (v6: 0,42 mm değmiyordu) · v7b: brakete 16 mm bindirir (ilk: 4)
    # v7b: delikli sensör sacı (z −392…−389) + yatak askısının yan yüzüne (x 104) 20 × 22 dik kol, sensörün ÜSTÜNDE (sensör x 106'dan başlar) · v7 ilk: sensöre teğet lam
    ekle("parmak_sensor_braketi", kut(104.0, 107.0, py + 28.0, py + 48.0, -392.0, -370.0).union(kut(104.0, 122.0, py + 8.0, py + 32.0, -392.0, -389.0).cut(silz(px + 22.0, py + 20.0, 4.02, -393.0, -388.0))),
         "aluminyum", bom=SENSOR_BRAKET_BOM)''')

# ---------------------------------------------------------------- 12 · kapak mekanizması: +2 ayak, sensör braketleri, kol redüktör plakası ----------------------------------------------------------------
d('''    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, BZ1, BZ1 + 20.0), "aluminyum")''',
  '''    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, BZ1, BZ1 + 20.0), "aluminyum")
    for i, (z0, z1) in enumerate(((-368.0, -348.0), (BZ1, BZ1 + 20.0))):   # v7: kalıp tarafında 2 ayak daha (v6: plaka x 440–800 yalnız sağ ayaklarda, 340 mm konsol)
        ekle("kapak_alt_plaka_ayagi_%d" % (i + 2), kut(440.0, 460.0, ALT_RAF_Y[1], 826.0, z0, z1), "aluminyum")''')
d('''    e2e("flap_katlayici_sensor", 700.0, 862.0, -300.0, "y")''',
  '''    e2e("flap_katlayici_sensor", 700.0, 862.0, -300.0, "y")
    # v7b: Z büküm — ayak kapak alt plakasının üstüne (15 × 20), dik kol, delikli sensör sacı (y 870–873) · v7 ilk: sensörün alt yüzünü kapatan sütun
    ekle("flap_katlayici_sensor_braketi", kut(709.0, 724.0, 832.0, 835.0, -310.0, -290.0).union(kut(709.0, 712.0, 835.0, 873.0, -310.0, -290.0))
         .union(kut(690.0, 712.0, 870.0, 873.0, -310.0, -290.0).cut(sily(700.0, -300.0, 4.02, 869.0, 874.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)''')
d('''    ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 832.0, py - 29.0, -150.0, -140.0), "aluminyum")''',
  '''    ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 832.0, py - 29.0, -150.0, -140.0), "aluminyum")
    ekle("kol_red_flans_plakasi", kut(px - 30.0, px + 30.0, 870.0, py + 30.0, -154.0, -150.0).cut(silz(px, py, 12.0, -155.0, -149.0)), "aluminyum")   # v7: redüktör çıkış flanşı bu plakaya, plaka brakete (v6: 0,42 mm değmiyordu)''')
d('''    e2e("kol_sensor", px + 30.0, py - 40.0, ZB + 12.0, "z")''',
  '''    e2e("kol_sensor", px + 30.0, py - 40.0, ZB + 12.0, "z")
    # v7b: delikli sensör sacı (z −170…−167) + kol yatak ayağının yan yüzüne (x 578) 24 × 10 dik kol (v7 ilk: sensöre teğet blok)
    ekle("kol_sensor_braketi", kut(px + 18.0, px + 21.0, py - 52.0, py - 28.0, -170.0, -160.0).union(kut(px + 18.0, px + 40.0, py - 52.0, py - 28.0, -170.0, -167.0)
         .cut(silz(px + 30.0, py - 40.0, 4.02, -171.0, -166.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)''')

# ---------------------------------------------------------------- 13 · elektrik: pano burçları, dikey kanallar x 806, sensör braketleri ----------------------------------------------------------------
d('''    ekle("pano_plakasi", kut(60.0, 780.0, 1397.0, 1857.0, -826.0, -822.0), "sac")''',
  '''    ekle("pano_plakasi", kut(60.0, 780.0, 1397.0, 1857.0, -826.0, -822.0), "sac")
    for i, (xb, yb) in enumerate(((80.0, 1417.0), (760.0, 1417.0), (80.0, 1837.0), (760.0, 1837.0))):   # v7: pano plakası arka saca 4 burçla (v6: 2,5 mm havada)
        ekle("pano_plakasi_burcu_%d" % i, silz(xb, yb, 6.0, -D + SAC, -826.0), "celik", bom=("Mesafe burcu M5 · Ø12 × 2,5 paslanmaz", 1, "pano plakası ↔ arka sac", "katalog"))''')
d('''bom=("Kablo kanalı 40 × 25", 4, "pano 2 + dikey 2", "katalog") if i == 0 else None)''',
  '''bom=("Kablo kanalı 40 × 25", 2, "pano", "katalog") if i == 0 else None)''')
d('''    ekle("kablo_kanali_dikey_alt", kut(801.0, 826.0, Y_PLINT + 3.0, 1157.0, -50.0, -25.0), "plastik")   # v3: tabandan başlar
    ekle("kablo_kanali_dikey_ust", kut(801.0, 826.0, 1177.0, 1827.0, -50.0, -25.0), "plastik")''',
  '''    ekle("kablo_kanali_dikey_alt", kut(806.0, 826.0, Y_PLINT + 3.0, 1157.0, -50.0, -25.0), "plastik",   # v3: tabandan başlar · v7: x 801 → 806 (sağ sütun kolisinin düz yolu serbest)
         bom=("Kablo kanalı 20 × 25 (dikey)", 2, "sağ ön köşe · x 806–826", "katalog ölçüsü VARSAYIM"))
    ekle("kablo_kanali_dikey_ust", kut(806.0, 826.0, 1177.0, 1827.0, -50.0, -25.0), "plastik")''')
d('''    e3z("sensor_kutu_dolu", SAC + 1.0, 1068.0, -250.0)''',
  '''    e3z("sensor_kutu_dolu", SAC + 1.0, 1068.0, -250.0)
    # v7: 3 fotoselin braketi yoktu (havada) → üstlerinde lam, yan saca (mercek yüzleri açık kalır) · v7b: L — yan saca 27 × 20 dik kol (v7 ilk: 3 mm kenarla 1,5 saca)
    ekle("sensor_yigin_ustu_braketi", kut(770.0, W - SAC, 1053.0, 1056.0, -800.0, -780.0).union(kut(W - SAC - 3.0, W - SAC, 1056.0, 1080.0, -800.0, -780.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)
    ekle("sensor_blank_var_braketi", kut(790.0, W - SAC, 1053.0, 1056.0, -216.0, -196.0).union(kut(W - SAC - 3.0, W - SAC, 1056.0, 1080.0, -216.0, -196.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)
    ekle("sensor_kutu_dolu_braketi", kut(SAC, SAC + 11.8, 1099.0, 1102.0, -250.0, -230.0).union(kut(SAC, SAC + 3.0, 1102.0, 1130.0, -250.0, -230.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)''')

# ---------------------------------------------------------------- 14 · içecek yedeği notu ----------------------------------------------------------------
d('''    """v5: içecek yedeği — soğutmasız, önde · E_SARJOR'un önü, alt rafın altı · v6: önü AÇIK (ön alt sac kalktı)"""''',
  '''    """v5: içecek yedeği — soğutmasız, önde · E_SARJOR'un önü, alt rafın altı · v6: önü AÇIK (ön alt sac kalktı) ·
    v7: önünde ALT tava kanatlar (2 × 413 · ≥ 110°); kapak açıkken koli önü → ön düzlem (+79) yolu SERBEST (olcum_v7)"""''')

# ---------------------------------------------------------------- 15 · olcum(): ön düzlem, zarf, alt taban ----------------------------------------------------------------
d('''    print("DUZ ACILIM (kalipta): %.0f x %.0f mm · x %.1f..%.1f · z %.1f..%.1f (on yuz 0: %.1f mm iceride)" % (d.xlen, d.zlen, d.xmin, d.xmax, d.zmin, d.zmax, -d.zmax))
    assert d.zmax <= -2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"''',
  '''    print("DUZ ACILIM (kalipta): %.0f x %.0f mm · x %.1f..%.1f · z %.1f..%.1f (v7 on cerceve arkasi +%.0f: %.1f mm iceride)" % (d.xlen, d.zlen, d.xmin, d.xmax, d.zmin, d.zmax, Z_CERCEVE[0], Z_CERCEVE[0] - d.zmax))
    assert d.zmax <= Z_CERCEVE[0] - 2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"''')
d('''        if p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_") or "_kulp" in p["ad"]:
            continue
        bb = p["wp"].val().BoundingBox()
        if bb.xmin < -0.5 or bb.xmax > W + 0.5 or bb.ymin < -0.5 or bb.ymax > H + 0.5 or bb.zmin < -D - 0.5 or bb.zmax > 0.5:
            tasan.append(p["ad"])
    print("ZARF (modul %.0f x %.0f x %.0f, tutamaklar haric): %s" % (W, H, D, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))''',
  '''        if p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_"):     # v7: tutamak istisnası YOK (kulp kalmadı)
            continue
        bb = p["wp"].val().BoundingBox()
        if bb.xmin < -0.5 or bb.xmax > W + 0.5 or bb.ymin < -0.5 or bb.ymax > H + 0.5 or bb.zmin < -D - 0.5 or bb.zmax > Z_ON + 0.5:
            tasan.append(p["ad"])
    print("ZARF (modul %.0f x %.0f x %.0f · z -%.0f..+%.0f, istisnasiz): %s" % (W, H, D + Z_ON, D, Z_ON, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))''')
d('''    ALTTA_SERBEST = ("ayak_", "plint_on", "asansor_kasnak_",''', '''    ALTTA_SERBEST = ("ayak_", "onyuz_plint", "asansor_kasnak_",''')

# ---------------------------------------------------------------- 16 · olcum_v5 + olcum_v6 çıkar · icecek_on_olcum v7 · olcum_v7 ----------------------------------------------------------------
blok("def olcum_v5():", "# ---------------------------------------------------------------- GLB (hiyerarşik", r'''# v7: olcum_v5 (v4 dilim eşdeğerliği) ve olcum_v6 (v5 ↔ v6) ÇIKARILDI — ikisi de v6 ön yüzüne (ön köşe dikmeleri, on_ust_kapak) bağlıydı;
#     v6 ↔ v7 parça parça karşılaştırma + kinematik birebirlik olcum_v7'de. (Geçmiş: kutu_cad_v6.py'de aynen duruyor.)


def icecek_on_olcum():
    """v6 · İÇECEK YEDEĞİNİN ÖNÜ — v7: bölge koli önünden ÖN DÜZLEME (+79) kadar; kapak kanatları AÇIK kabul edilir (KAPI_ADLARI hariç) ·
    katılardan ölçer, modul()'den SONRA çağrılır (montaj E_ICECEK_YEDEK metni de buradan) · dönüş biçimi v6 ile aynı.
    on: kolilerin önünden ön düzleme kadar olan bölgeye giren gövde parçaları · net: kolilerin yüksekliğinde öndeki soldaki son engel ile
    sağdaki ilk engel arası (x) · sutun: her sütunun DÜZ çekme yoluna (koli izdüşümü, koli önü → ön düzlem) binen parçalar + x bindirmesi (mm) ·
    sag_bos: sağ sütunun sağında (koli yüksekliği ve derinliğinde) ilk engele kadar boşluk · ara: iki sütun arası."""
    X_, Y_, Z_ = ICECEK_YEDEK["x"], ICECEK_YEDEK["y"], ICECEK_YEDEK["z"]
    G_ = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR") and not p["ad"].startswith("icecek_") and p["ad"] not in KAPI_ADLARI]

    def kesen(x0, x1, y0, y1, z0, z1):
        b0 = kut(x0, x1, y0, y1, z0, z1).val(); B0 = b0.BoundingBox(); L = []
        for ad, sh in G_:
            b_ = sh.BoundingBox()
            if _bb_kesisir(B0, b_) and sh.intersect(b0).Volume() > 0.5:
                L.append((ad, b_))
        return L
    ZK = Z_ON + KOLI["z"]           # v7b (denetim bulgusu 1): koli TAMAMEN çıkana kadar — ön düzlemin önünde bir koli boyu (+79 … +346)
    on = kesen(X_[0], X_[1], Y_[0], Y_[1], Z_[1], ZK)
    orta = (X_[0] + X_[1]) / 2.0
    net = (max([b_.xmax for _a, b_ in on if b_.xmax <= orta] + [SAC]), min([b_.xmin for _a, b_ in on if b_.xmin >= orta] + [W - SAC]))
    sut = []
    for x0, x1 in ICECEK_X:
        eng = [(a, round(min(x1, b_.xmax) - max(x0, b_.xmin), 2)) for a, b_ in kesen(x0, x1, Y_[0], Y_[1], Z_[1], ZK)]
        sut.append(dict(x=(x0, x1), engel=eng, bindirme=max([v for _a, v in eng] + [0.0])))
    sag = kesen(X_[1], W, Y_[0], Y_[1], Z_[0], Z_[1])
    return dict(on=sorted({a for a, _b in on}), net=net, sutun=sut, sag_bos=min([b_.xmin for _a, b_ in sag] + [W]) - X_[1], ara=ICECEK_X[1][0] - ICECEK_X[0][1])


# ---- v7 · beyan: v6 → v7 parça listesi (olcum_v7 katılardan ölçüp bununla karşılaştırır) ----
V7_CIKAN = ("plint_on", "on_ust_kapak", "on_ust_kapak_kulp", "kose_dikme_on_0", "kose_dikme_on_1", "sarjor_yan_kapisi_kulp")
V7_DEGISEN = ("taban_sac_3", "ust_sac", "sol_sac_pizza_penceresi", "sag_sac", "sarjor_kapi_esigi", "asansor_ray_plakasi", "kalip_alt_rafi",
              "kalip_alt_rafi_koseben_sol", "kopru_plaka_tutucu", "kopru_motor_askisi", "kablo_kanali_dikey_alt", "kablo_kanali_dikey_ust",
              "asansor_motoru", "besleyici_motoru", "kopru_motoru", "piston_motoru", "parmak_motoru", "flap_katlayici_motoru", "kol_motoru",
              # v7b: kaplin delikli + yeri · köprü / flap motor braketi 8,5 aşağı · raf köşebendinde motor çentiği
              "kopru_kaplini", "flap_katlayici_kaplini", "kopru_motor_braketi", "flap_katlayici_motor_braketi", "flap_katlayici_braket_ayagi",
              "kalip_alt_rafi_koseben_sag")
V7_YENI = tuple(["onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust"] + [q[0] for q in ON_PANEL] +
                ["onyuz_mentese_%d" % i for i in range(12)] + ["onyuz_basac_%d" % i for i in range(5)] +
                ["onyuz_alt_dayama_dudagi", "sarjor_kapi_esigi_kosebendi_sol", "sarjor_kapi_esigi_kosebendi_sag"] +
                ["onyuz_plint", "ayak_4", "ayak_5", "sarjor_yan_kapisi_mentese_0", "sarjor_yan_kapisi_mentese_1", "sarjor_yan_kapisi_basac",
                 "asansor_ray_plakasi_flansi", "asansor_ray_plakasi_ust_kosebendi_sol", "asansor_ray_plakasi_ust_kosebendi_sag", "asansor_alt_sensor_braketi",
                 "besleyici_plaka_askisi_2", "besleyici_plaka_askisi_3", "besleyici_arka_sensor_braketi", "kalip_alt_rafi_duvar_takozu_sag",
                 "kopru_alt_sensor_braketi", "piston_ust_sensor_braketi", "piston_eksen_plakasi_bagi_sol", "piston_eksen_plakasi_bagi_sag",
                 "parmak_red_flans_plakasi", "parmak_sensor_braketi", "kapak_alt_plaka_ayagi_2", "kapak_alt_plaka_ayagi_3",
                 "flap_katlayici_sensor_braketi", "kol_red_flans_plakasi", "kol_sensor_braketi"] +
                ["pano_plakasi_burcu_%d" % i for i in range(4)] + ["sensor_yigin_ustu_braketi", "sensor_blank_var_braketi", "sensor_kutu_dolu_braketi"])
# havada denetimi: taşınan ürün / robot aleti / K referansı E'nin parçası değil (montajdan düşer ya da üründür)
HAVADA_DIS = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")          # + "B_*" (kutu blank'ı: kalıp raylarının 0,1 üstünde kayar)
BEYAZ = (   # idealleştirilmiş temas (SPEC §3: bilyeli ray, rulman burcu gibi) — (ad parçası a, ad parçası b, en çok aralık mm, gerekçe)
    ("_kayisi", "_kasnak_", 0.40, "GT3 kayış hatve dairesinde modellendi, kasnak dış çapı 0,38 küçük (gerçekte dişler kavraşır)"),
    ("_vidasi_somun", "_vidasi_mil", 0.25, "bilyalı somun ↔ vida mili (bilyeler modellenmedi · 0,2)"),
    ("kopru_kilavuz_mili", "kopru_burcu", 0.15, "LM12UU lineer burç ↔ Ø12 mil (bilyeler modellenmedi · 0,1)"),
)


def kapi_matrisi(ad, aci):
    """kanat açılışı · v7b: SIFIR ÇIKINTILI gizli menteşe — sanal eksen kapağın menteşe kenarının MENTESE_OFSET (20) DIŞINDA, ön düzlemde
    (sol: x0 − 20 · sağ: x1 + 20, z Z_ON). 90°'de kapağın iç yüzü yan sacın iç yüzünde: koli yolu kapakla kesişmez. Sabit eksen = gerçek çok mafsallı
    hareketin sadeleştirmesi (VARSAYIM; Blum 155° zero protrusion ailesi). v7 ilk: eksen kapağın dış köşesindeydi → 20'lik büküm koli yoluna dönüyordu
    (denetim bulgusu 1). aci derece, 0 = kapalı, en çok KAPI_MAX_ACI."""
    k = [q for q in ON_PANEL if q[0] == ad][0]
    xp = k[1] - MENTESE_OFSET if k[5] == "sol" else k[2] + MENTESE_OFSET
    fi = -aci if k[5] == "sol" else aci
    return mm4(mm4(tr4((xp, 0.0, Z_ON)), rot4("y", fi)), tr4((-xp, 0.0, -Z_ON)))


def havada_v7():
    """denetim_temas_v1 + beyaz liste: ham bileşenlerden, beyaz listedeki bir çiftle (aralık ≤ pay) zemine bağlı bir parçaya değenler bağlı sayılır"""
    import denetim_temas_v1 as DT
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    ps = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] not in HAVADA_DIS and not p["grup"].startswith("B_")]
    s = DT.havada(ps)
    S = dict(ps)
    yuzen = {a for d_ in s["bilesen"] for a in d_["uye"]}
    bagli = [a for a, _sh in ps if a not in yuzen]
    kalan, beyaz = list(s["bilesen"]), []
    degisti = True
    while degisti:
        degisti = False
        for d_ in list(kalan):
            bul = None
            for a in d_["uye"]:
                for p_, q_, pay, neden in BEYAZ:
                    for b in bagli:
                        if not ((p_ in a and q_ in b) or (q_ in a and p_ in b)):
                            continue
                        x = BRepExtrema_DistShapeShape(S[a].wrapped, S[b].wrapped)
                        if x.IsDone() and x.Value() <= pay:
                            bul = (a, b, x.Value(), neden)
                            break
                    if bul:
                        break
                if bul:
                    break
            if bul:
                kalan.remove(d_); bagli += d_["uye"]; beyaz.append(dict(uye=d_["uye"], cift=bul)); degisti = True
    return dict(ham=s, kalan=kalan, beyaz=beyaz)


def on_yuz_izgarasi(adim=10.0):
    """ön düzlem ızgarası (z Z_ON − 0,75: ön sacın içi) — her nokta ya bir panelin İÇİNDE (katı sınıflandırma, BRepClass3d), ya derzde,
    ya ROBOT AĞZINDA olmalı; ağızda panel olmamalı, derzde panel olmamalı"""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN
    pan = []
    for q in ON_PANEL:
        sh = [p for p in PARCALAR if p["ad"] == q[0]][0]["wp"].val()
        pan.append((q[0], sh, sh.BoundingBox()))
    zc = Z_ON - TAVA_T / 2.0

    def derz(x, y):
        if x < SAC or y > Y_UST[1] or y < Y_ALT[0]:
            return True
        if Y_ALT[1] < y < Y_ORTA[0] or Y_ORTA[1] < y < Y_UST[0]:
            return True
        if X_ORTA_DERZ[0] < x < X_ORTA_DERZ[1] and not (Y_ORTA[0] <= y <= Y_ORTA[1]):
            return True
        if AGIZ["x"][1] < x < AGIZ["x"][1] + DERZ and Y_ORTA[0] <= y <= Y_ORTA[1]:
            return True
        return False
    say = dict(panel=0, derz=0, agiz=0); hata = []
    for i in range(int(W / adim)):
        x = adim * (i + 0.37)                  # ızgara kenar çizgilerine (85, 415 …) denk gelmesin
        for j in range(int((H - Y_ALT[0]) / adim)):
            y = Y_ALT[0] + adim * (j + 0.37)
            icinde = []
            for a, sh, b in pan:
                if b.xmin <= x <= b.xmax and b.ymin <= y <= b.ymax:
                    if BRepClass3d_SolidClassifier(sh.wrapped, gp_Pnt(x, y, zc), 1e-6).State() == TopAbs_IN:
                        icinde.append(a)
            agiz = AGIZ["x"][0] < x < AGIZ["x"][1] and AGIZ["y"][0] <= y < AGIZ["y"][1]
            if agiz:
                say["agiz"] += 1
                if icinde:
                    hata.append((x, y, "ağızda panel", icinde))
            elif icinde:
                say["panel"] += 1
                if len(icinde) > 1 or derz(x, y):
                    hata.append((x, y, "çift / derzde panel", icinde))
            elif derz(x, y):
                say["derz"] += 1
            else:
                hata.append((x, y, "BOŞ", []))
    # v7b (denetim bulgusu 7): 10 mm ızgara (x = 10(i + 0,37)) hiçbir derz bandına düşmüyordu → derz ORTA ÇİZGİLERİ ayrıca 5 mm'de örneklenir; hiçbir panel içermemeli
    def ara(a, b, adim=5.0):
        return [a + adim * k for k in range(int((b - a) / adim) + 1)]
    xd, xs = (X_ORTA_DERZ[0] + X_ORTA_DERZ[1]) / 2.0, AGIZ["x"][1] + DERZ / 2.0
    cz = [(xd, y) for y in ara(Y_ALT[0] + 1.0, Y_ALT[1] - 1.0)] + [(xd, y) for y in ara(Y_UST[0] + 1.0, Y_UST[1] - 1.0)] + [(xs, y) for y in ara(Y_ORTA[0] + 1.0, Y_ORTA[1] - 1.0)]
    for yd in ((Y_ALT[1] + Y_ORTA[0]) / 2.0, (Y_ORTA[1] + Y_UST[0]) / 2.0, (Y_UST[1] + H) / 2.0):
        cz += [(x, yd) for x in ara(SAC + 1.0, W - 1.0)]
    cz += [(SAC / 2.0, y) for y in ara(Y_ALT[0] + 1.0, Y_UST[1] - 1.0)]            # K ile arasındaki derzin E yarısı (x 0–1,5)
    say["derz_cizgi"] = 0
    for x, y in cz:
        icinde = [a for a, sh, b in pan if b.xmin <= x <= b.xmax and b.ymin <= y <= b.ymax
                  and BRepClass3d_SolidClassifier(sh.wrapped, gp_Pnt(x, y, zc), 1e-6).State() == TopAbs_IN]
        say["derz_cizgi"] += 1
        if icinde:
            hata.append((x, y, "derz çizgisinde panel", icinde))
    return say, hata


def derz_olcum():
    """v7b (denetim bulgusu 7) · derzler PANEL KATILARININ sınır kutularından (sabitlerden değil) · dönüş {derz adı: açıklık mm}"""
    B = {q[0]: [p for p in PARCALAR if p["ad"] == q[0]][0]["wp"].val().BoundingBox() for q in ON_PANEL}
    a_s, a_g, u_s, u_g = B["onyuz_alt_kanat_sol"], B["onyuz_alt_kanat_sag"], B["onyuz_ust_kanat_sol"], B["onyuz_ust_kanat_sag"]
    o_s, o_g = B["onyuz_orta_sabit_panel"], B["onyuz_orta_servis_kapagi"]
    D = {"ALT kanatlar arası (x)": a_g.xmin - a_s.xmax, "ÜST kanatlar arası (x)": u_g.xmin - u_s.xmax, "ORTA sabit ↔ servis (x)": o_g.xmin - o_s.xmax,
         "ALT sol ↔ ORTA sabit (y)": o_s.ymin - a_s.ymax, "ALT sağ ↔ ORTA servis (y)": o_g.ymin - a_g.ymax,
         "ORTA sabit ↔ ÜST sol (y)": u_s.ymin - o_s.ymax, "ORTA servis ↔ ÜST sağ (y)": u_g.ymin - o_g.ymax,
         "ÜST ↔ tavan 1862 (y)": H - max(u_s.ymax, u_g.ymax), "ALT ↔ alt taban 123 (y)": min(a_s.ymin, a_g.ymin) - Y_PLINT,
         "K ↔ E derzinin E yarısı (x, K yarısıyla 3)": min(b.xmin for b in B.values()) * 2.0}
    hiza = max(abs(a_s.ymin - a_g.ymin), abs(a_s.ymax - a_g.ymax), abs(u_s.ymin - u_g.ymin), abs(u_s.ymax - u_g.ymax), abs(o_s.ymin - o_g.ymin), abs(o_s.ymax - o_g.ymax))
    return D, hiza


KAPI_ACILARI = (1, 2, 3) + tuple(range(5, int(KAPI_MAX_ACI) + 1, 5))      # v7b: 1°…155° (v7 ilk: 10°…120° — 180°'ye kadar bakılmıyordu, denetim bulgusu 7)


def kapi_acilma_olcum(acilar=KAPI_ACILARI):
    """her kanat 1°…155°: en uç z (QR yüzü 670'e çarpmamalı) · E'nin SABİT + ASANSÖR parçalarıyla çakışma (kendisi + kendi menteşeleri hariç) ·
    koli yolu prizmalarıyla çakışan açılar (v7b: prizma koli önü −83 → ön düzlemin önünde bir koli boyu, +346) — ≥ KOLI_ACI'da HİÇ olmamalı ·
    x taşması (sol kanatlar K'nın önüne, sağlar hat sonuna döner — z > +79'da)"""
    koli = [kut(x0, x1, ICECEK_Y0, ICECEK_YEDEK["y"][1], ICECEK_Z[1], Z_ON + KOLI["z"]).val() for x0, x1 in ICECEK_X]
    sab = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR")]
    sab = [(a, sh, sh.BoundingBox()) for a, sh in sab]
    R = {}
    for ad in KAPI_ADLARI:
        kap = [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val()
        haric = {ad} | {m for m, k in MENTESE_KAPI.items() if k == ad}
        r = dict(zmax=-1e9, xmin=1e9, xmax=-1e9, cak=[], koli=[], zmin_x_disi=1e9)
        for aci in acilar:
            sh = uygula(kap, kapi_matrisi(ad, aci)); B = sh.BoundingBox()
            r["zmax"] = max(r["zmax"], B.zmax); r["xmin"] = min(r["xmin"], B.xmin); r["xmax"] = max(r["xmax"], B.xmax)
            if B.xmin < 0.0 or B.xmax > W:                  # modül dışına dönen kısmın en arka z'si (komşu kapağın ön yüzü +79'u geçmemeli)
                dis = sh.intersect(kut(-2000.0, 0.0, -10.0, H + 10.0, -D, 2000.0).val() if B.xmin < 0.0 else kut(W, W + 2000.0, -10.0, H + 10.0, -D, 2000.0).val())
                if dis.Volume() > 0.01:
                    r["zmin_x_disi"] = min(r["zmin_x_disi"], dis.BoundingBox().zmin)
            for a, s_, b in sab:
                if a in haric or not _bb_kesisir(B, b):
                    continue
                v = sh.intersect(s_).Volume()
                if v > 0.5:
                    r["cak"].append((aci, a, round(v, 1)))
            for kb in koli:
                if _bb_kesisir(B, kb.BoundingBox()) and sh.intersect(kb).Volume() > 0.01:
                    r["koli"].append(aci)
                    break
        r["koli_serbest_min"] = min([a_ for a_ in acilar if all(b_ not in r["koli"] for b_ in acilar if b_ >= a_)] + [999])
        R[ad] = r
    return R


def robot_agzi_taramasi(adim=0.05, esik=0.5, yakin=30.0):
    """robot çatalı + kutu (t 13,9–17,3, adım 0,05 sn) × E'nin BÜTÜN SABİT parçaları (çakışma) · ön parçalara en küçük aralık (pay)"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    t0 = time.time()
    sab = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
    sab = [(a, sh, sh.BoundingBox()) for a, sh in sab]
    on_ad = set([q[0] for q in ON_PANEL] + ["onyuz_kayit_orta", "onyuz_kayit_ust", "onyuz_dikme_sol", "onyuz_dikme_sag"])
    anlar = [round(Z_CATAL[0] + adim * i, 3) for i in range(int(round((Z_CATAL[3] - Z_CATAL[0]) / adim)) + 1)]
    bul, pay = {}, {}
    for t in anlar:
        W_ = blank_dunya(t)
        hare = [(p["ad"], uygula(p["wp"].val(), grup_matrisi("CATAL", t))) for p in PARCALAR if p["grup"] == "CATAL"]
        hare += [(p["ad"], uygula(p["wp"].val(), W_[p["grup"]])) for p in PARCALAR if p["grup"].startswith("B_")]
        for a, sh in hare:
            A = sh.BoundingBox()
            for q, s_, b in sab:
                if _bb_kesisir(A, b):
                    v = sh.intersect(s_).Volume()
                    if v > esik and (a, q) not in bul:
                        bul[(a, q)] = (round(v, 1), t)
                if q in on_ad and not (A.xmin > b.xmax + yakin or b.xmin > A.xmax + yakin or A.ymin > b.ymax + yakin or b.ymin > A.ymax + yakin
                                       or A.zmin > b.zmax + yakin or b.zmin > A.zmax + yakin):
                    dd = BRepExtrema_DistShapeShape(sh.wrapped, s_.wrapped).Value()
                    if q not in pay or dd < pay[q][0]:
                        pay[q] = (dd, a, t)
    return dict(an=len(anlar), bul=bul, pay=pay, sure=time.time() - t0)


def asansor_strok_taramasi(adim=10.0, esik=0.5):
    """ASANSÖR grubu (platform, çatallar, araba, HGH15 arabaları, somun) 0 → somun üst yatağa değene kadar yukarı · × v7'de yeni / değişen SABİT parçalar
    (GLB animasyonunda asansör hareket etmiyor — bu tarama o boşluğu kapatır)"""
    def bb(ad):
        return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    strok = bb("asansor_ust_yatak").ymin - bb("asansor_somunu").ymax
    asan = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "ASANSOR"]
    hed = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT" and (p["ad"] in V7_YENI or p["ad"] in V7_DEGISEN)]
    hed = [(a, sh, sh.BoundingBox()) for a, sh in hed]
    n = int(strok / adim)
    bul = {}
    for i in range(n + 2):
        dy = min(strok, i * adim)
        for a, sh in asan:
            s2 = sh.translate(cq.Vector(0.0, dy, 0.0)); A = s2.BoundingBox()
            for q, s_, b in hed:
                if _bb_kesisir(A, b):
                    v = s2.intersect(s_).Volume()
                    if v > esik and (a, q) not in bul:
                        bul[(a, q)] = (round(v, 1), dy)
    return dict(strok=strok, adim=n + 2, hedef=len(hed), bul=bul)


def _kesit_I(dik):
    """dikdörtgenler (u0, u1, v0, v1) → (alan, I_u ekseni etrafında [v yönü eğilme], I_v) — ağırlık merkezine göre"""
    A = sum((u1 - u0) * (v1 - v0) for u0, u1, v0, v1 in dik)
    uc = sum((u1 - u0) * (v1 - v0) * (u0 + u1) / 2.0 for u0, u1, v0, v1 in dik) / A
    vc = sum((u1 - u0) * (v1 - v0) * (v0 + v1) / 2.0 for u0, u1, v0, v1 in dik) / A
    Iu = sum((u1 - u0) * (v1 - v0) ** 3 / 12.0 + (u1 - u0) * (v1 - v0) * ((v0 + v1) / 2.0 - vc) ** 2 for u0, u1, v0, v1 in dik)
    Iv = sum((v1 - v0) * (u1 - u0) ** 3 / 12.0 + (u1 - u0) * (v1 - v0) * ((u0 + u1) / 2.0 - uc) ** 2 for u0, u1, v0, v1 in dik)
    cv = max(max(abs(v0 - vc), abs(v1 - vc)) for u0, u1, v0, v1 in dik)
    cu = max(max(abs(u0 - uc), abs(u1 - uc)) for u0, u1, v0, v1 in dik)
    return A, Iu, Iv, cv, cu


def _sek(ad):
    return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val()


def temas_alani(a, b, d=0.1):
    """v7b · iki katı arasındaki en büyük DÜZLEMSEL temas yaması: b altı eksen yönünde d kaydırılıp a ile kesiştirilir → alan = hacim / d (mm²) ·
    ikinci dönüş: yamanın kısa kenarı (kesişimin sınır kutusunun ortanca boyu, mm) — bindirme ≥ 10 mm denetimi için"""
    en = (0.0, 0.0)
    for v in ((d, 0, 0), (-d, 0, 0), (0, d, 0), (0, -d, 0), (0, 0, d), (0, 0, -d)):
        c = a.intersect(b.translate(cq.Vector(*v)))
        V = c.Volume()
        if V > 1e-6 and V / d > en[0]:
            bb_ = c.BoundingBox()
            en = (V / d, sorted([bb_.xlen, bb_.ylen, bb_.zlen])[1])
    return en


# v7b · denetim bulgusu 5: bağlantı elemanı olarak ölçülen temaslar — (parça, taşıyıcı): düzlemsel temas ≥ 100 mm² ve kısa kenar ≥ 9,9 mm (cıvatalı bindirme)
BAGLANTI_V7B = (
    ("asansor_alt_sensor_braketi", "asansor_ray_plakasi"), ("besleyici_arka_sensor_braketi", "besleyici_plakasi"), ("kopru_alt_sensor_braketi", "kopru_burc_plakasi"),
    ("piston_ust_sensor_braketi", "piston_eksen_plakasi"), ("parmak_sensor_braketi", "parmak_yatak_askisi"), ("flap_katlayici_sensor_braketi", "kapak_alt_plakasi"),
    ("kol_sensor_braketi", "kol_yatak_ayagi_1"), ("sensor_yigin_ustu_braketi", "sag_sac"), ("sensor_blank_var_braketi", "sag_sac"),
    ("sensor_kutu_dolu_braketi", "sol_sac_pizza_penceresi"),
    ("piston_eksen_plakasi_bagi_sol", "besleyici_plakasi"), ("piston_eksen_plakasi_bagi_sol", "piston_eksen_plakasi"),
    ("piston_eksen_plakasi_bagi_sag", "besleyici_plakasi"), ("piston_eksen_plakasi_bagi_sag", "piston_eksen_plakasi"),
    ("parmak_red_flans_plakasi", "parmak_red_braketi"), ("kol_red_flans_plakasi", "kol_reduktor_braketi"),
    ("asansor_ray_plakasi_ust_kosebendi_sol", "asansor_ray_plakasi"), ("asansor_ray_plakasi_ust_kosebendi_sol", "sol_sac_pizza_penceresi"),
    ("asansor_ray_plakasi_ust_kosebendi_sag", "asansor_ray_plakasi"), ("asansor_ray_plakasi_ust_kosebendi_sag", "sag_sac"),
    ("asansor_ray_plakasi_flansi", "asansor_ray_plakasi"), ("asansor_ray_plakasi_flansi", "taban_sac_3"),
    ("sarjor_kapi_esigi", "taban_sac_3"), ("sarjor_kapi_esigi_kosebendi_sol", "sarjor_kapi_esigi"), ("sarjor_kapi_esigi_kosebendi_sol", "sol_sac_pizza_penceresi"),
    ("sarjor_kapi_esigi_kosebendi_sag", "sarjor_kapi_esigi"), ("sarjor_kapi_esigi_kosebendi_sag", "sag_sac"),
    ("onyuz_alt_dayama_dudagi", "taban_sac_3"), ("kalip_alt_rafi_duvar_takozu_sag", "sag_sac"),
    ("besleyici_plaka_askisi_2", "besleyici_plakasi"), ("besleyici_plaka_askisi_3", "besleyici_plakasi"),
    ("kapak_alt_plaka_ayagi_2", "kalip_alt_rafi"), ("kapak_alt_plaka_ayagi_3", "kalip_alt_rafi"),
)
# M8 endüktif sensörler delikli saçta (Ø8,04 delik: katı bindirmesi yok, aralık ≤ 0,05 = değer)
SENSOR_DELIK = (("asansor_alt_sensor", "asansor_alt_sensor_braketi"), ("besleyici_arka_sensor", "besleyici_arka_sensor_braketi"),
                ("kopru_alt_sensor", "kopru_alt_sensor_braketi"), ("piston_ust_sensor", "piston_ust_sensor_braketi"), ("parmak_sensor", "parmak_sensor_braketi"),
                ("flap_katlayici_sensor", "flap_katlayici_sensor_braketi"), ("kol_sensor", "kol_sensor_braketi"))


def olcum_v7(tam=True):
    """v7 · ÖN DÜZLEM +79 — iddiaları ÖLÇER, bozulursa durur (assert). tam=False: süpürme taramaları (kapak, robot ağzı, asansör) atlanır.
    Dönüş: ölçülen değerler sözlüğü (rapor ve montaj için)."""
    import dilim_v1 as DL
    import kutu_cad_v6 as V6
    O = {}
    SAY = [0]

    def yaz(ad, sart, deger=""):
        SAY[0] += 1
        print("  %-110s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); sys.stdout.flush()
        assert sart, ad

    def bb(ad):
        return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    print("OLCUM v7 (on duzlem +%.0f · derinlik %.0f · SPEC_on_duzlem_v63 §2.6)" % (Z_ON, D + Z_ON))
    # 1 · v6 ↔ v7 parça parça (sınır kutusu ±0,01 + hacim) — beyan edilen listelerle AYNI olmalı
    V6.modul()
    k = DL.karsilastir(PARCALAR, V6.PARCALAR)
    fark_ad = sorted({f.split(":")[0] for f in k["fark"]})
    O["v6_v7"] = dict(v6=len(V6.PARCALAR), v7=len(PARCALAR), ayni=len(k["ayni"]), degisen=fark_ad, cikan=sorted(k["ref_eksik"]), yeni=sorted(k["yeni_ek"]))
    yaz("v6 ↔ v7: v6 %d → v7 %d parça · birebir %d · değişen %d · çıkan %d · yeni %d (beyan edilen listelerle aynı)"
        % (len(V6.PARCALAR), len(PARCALAR), len(k["ayni"]), len(fark_ad), len(k["ref_eksik"]), len(k["yeni_ek"])),
        set(fark_ad) == set(V7_DEGISEN) and set(k["ref_eksik"]) == set(V7_CIKAN) and set(k["yeni_ek"]) == set(V7_YENI),
        "fark: değişen %s · çıkan %s · yeni %s" % (sorted(set(fark_ad) ^ set(V7_DEGISEN)), sorted(set(k["ref_eksik"]) ^ set(V7_CIKAN)), sorted(set(k["yeni_ek"]) ^ set(V7_YENI))))
    print("     değişen: %s" % ", ".join(fark_ad))
    print("     çıkan: %s" % ", ".join(sorted(k["ref_eksik"])))
    print("     yeni: %s" % ", ".join(sorted(k["yeni_ek"])))
    # 2 · KİNEMATİK v6 ile BİREBİR (çatal / kutu yolu, kafa(t), blank açıları, pizza, itici, köprü, katlayıcı, kol, parmak)
    SABITLER = ("W", "H", "D", "SAC", "Y_PLINT", "TEPSI", "KALIP", "YB", "T", "PLAKA_K", "PENCERE", "BX0", "BX1", "ZB", "BZ0", "BZ1", "ALT_RAF_Y", "X_BL0", "X_BL1",
                "Z_BL0", "Z_BL1", "BESLE", "ZS0", "ZS1", "Y_PLAT", "SARJOR_ADET", "H_UST", "KOL_P", "KOL_R", "KMER", "X_CATAL", "X_BAR", "CATAL_DIS", "Z_CATAL",
                "KAPAK_BASKI", "H_BEKLE", "Y_VURUS2", "ICECEK_X", "ICECEK_Z", "ICECEK_Y0", "ICECEK_KAT", "KOLI", "DONGU", "PARMAK_P", "PARMAK_R", "U_MAX")
    g_ = globals()
    dif = [n for n in SABITLER if g_[n] != getattr(V6, n)]
    yaz("kaydedilmiş ölçüler + kinematik sabitleri (%d: tepsi, kalıp, blank, şarjör, çatal, içecek yedeği, döngü …) v6 ile aynı" % len(SABITLER), not dif, str(dif))
    f = 0.0
    TT = [i * 0.01 for i in range(int(round(DONGU / 0.01)) + 1)]
    for t in TT:
        f = max(f, abs(kafa(t) - V6.kafa(t)), abs(u_zimba(t) - V6.u_zimba(t)), abs(parmak_psi(t) - V6.parmak_psi(t)), abs(kapak_alfa(t) - V6.kapak_alfa(t)),
                abs(kol_beta(t) - V6.kol_beta(t)), abs(katlayici_dy(t) - V6.katlayici_dy(t)), abs(kopru_dy(t) - V6.kopru_dy(t)), abs(itici_dz(t) - V6.itici_dz(t)))
        for a_, b_ in ((catal_trs(t), V6.catal_trs(t)), (catal_kutu(t), V6.catal_kutu(t)), (pizza_trs(t), V6.pizza_trs(t)), (k_itici_trs(t), V6.k_itici_trs(t))):
            f = max(f, max(abs(x - y) for x, y in zip(a_, b_)))
        k0, A0 = blank_acilar(t); k1, A1 = V6.blank_acilar(t)
        f = max(f, max(abs(x - y) for x, y in zip(k0, k1)), max(abs(A0[g] - A1[g]) for g in A0))
    fm = 0.0
    for t in KUTU_ANLARI + GECIS_ANLARI + tuple(round(Z_CATAL[0] + 0.1 * i, 2) for i in range(35)):
        M7, M6 = blank_dunya(t), V6.blank_dunya(t)
        fm = max(fm, max(abs(M7[g][i][j] - M6[g][i][j]) for g in M7 for i in range(4) for j in range(4)))
    O["kinematik_fark"] = (f, fm)
    yaz("kinematik: %d an (0,01 sn) · kafa(t) · blank_acilar(t) · çatal · kutu · pizza · K itici · kol · parmak · köprü · katlayıcı · itici → en büyük fark %.1e · blank_dunya %.1e"
        % (len(TT), f, fm), f < 1e-12 and fm < 1e-12)
    # 3 · ÖN DÜZLEM
    zs = [(q[0], bb(q[0])) for q in ON_PANEL]
    O["on_panel"] = {a: (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax) for a, b in zs}
    yaz("ön paneller %d (6 tava): hepsinin dış yüzü z +%.1f, arka kenarı +%.1f (20 büküm) · kalınlık 1,5" % (len(zs), Z_ON, Z_PANEL),
        len(zs) == 6 and all(abs(b.zmax - Z_ON) < 0.01 and abs(b.zmin - Z_PANEL) < 0.01 for _a, b in zs))
    urun = lambda p: p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_")
    en_on = max((p["wp"].val().BoundingBox().zmax, p["ad"]) for p in PARCALAR if not urun(p))
    en_arka = min(p["wp"].val().BoundingBox().zmin for p in PARCALAR if not urun(p))
    O["zarf_z"] = (en_arka, en_on[0])
    yaz("zarf: en öndeki parça %s z +%.2f ≤ +%.1f (ön düzlem + 0,5) · en arka %.1f ≥ −%.1f · kulp / tutamak YOK" % (en_on[1], en_on[0], Z_ON + 0.5, en_arka, D + 0.5),
        en_on[0] <= Z_ON + 0.5 and en_arka >= -D - 0.5 and not [p for p in PARCALAR if "_kulp" in p["ad"]])
    kn = {a: bb(a) for a in ("sol_sac_pizza_penceresi", "sag_sac", "ust_sac", "taban_sac_3", "arka_sac", "onyuz_plint", "onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust")}
    yaz("gövde kenarları: sol / sağ / üst sac ön kenarı +%.1f · taban +%.1f · arka sac −%.1f…−%.1f (SABİT) · çerçeve +%.0f…+%.0f · plint +%.1f…+%.1f"
        % (Z_PANEL, Z_TABAN_ON, D, D - SAC, Z_CERCEVE[0], Z_CERCEVE[1], Z_PLINT[0], Z_PLINT[1]),
        all(abs(kn[a].zmax - Z_PANEL) < 0.01 for a in ("sol_sac_pizza_penceresi", "sag_sac", "ust_sac")) and abs(kn["taban_sac_3"].zmax - Z_TABAN_ON) < 0.01
        and abs(kn["arka_sac"].zmin + D) < 0.01 and all(abs(kn[a].zmax - Z_CERCEVE[1]) < 0.01 and abs(kn[a].zmin - Z_CERCEVE[0]) < 0.01
                                                         for a in ("onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust"))
        and abs(kn["onyuz_plint"].zmax - Z_PLINT[1]) < 0.01 and abs(kn["onyuz_plint"].ymin) < 0.01 and abs(kn["onyuz_plint"].ymax - Y_PLINT) < 0.01)
    yaz("ön çerçeve tam boy: dikmeler y %.0f–%.1f (sol + sağ) · kayıtlar derz arkasında (üst yüzleri %.0f / %.0f)" % (Y_ALT[0], H - SAC, Y_ALT[1], Y_ORTA[1]),
        all(abs(kn[a].ymin - Y_ALT[0]) < 0.01 and abs(kn[a].ymax - (H - SAC)) < 0.01 for a in ("onyuz_dikme_sol", "onyuz_dikme_sag"))
        and abs(kn["onyuz_kayit_orta"].ymax - Y_ALT[1]) < 0.01 and abs(kn["onyuz_kayit_ust"].ymax - Y_ORTA[1]) < 0.01)
    iz, iz_h = on_yuz_izgarasi()
    O["izgara"] = iz
    yaz("ön yüz ızgarası (10 mm, katı sınıflandırma): panel %d · robot ağzı %d nokta → boş %d · ağızda panel %d · v7b derz ORTA ÇİZGİLERİ %d nokta (5 mm) → panel içeren %d"
        % (iz["panel"], iz["agiz"], len([h for h in iz_h if h[2] == "BOŞ"]), len([h for h in iz_h if h[2] == "ağızda panel"]), iz["derz_cizgi"],
           len([h for h in iz_h if h[2] in ("derz çizgisinde panel", "çift / derzde panel")])), not iz_h and iz["derz_cizgi"] > 1000, str(iz_h[:4]))
    dz_, hz_ = derz_olcum()
    O["derz"] = dz_
    yaz("derzler PANEL KATILARINDAN (v7b): %s · satır hizası sapma %.2f · omega takviye gerekmez (en geniş panel %.1f ≤ 600)"
        % (" · ".join("%s %.2f" % (k_, v_) for k_, v_ in dz_.items()), hz_, max(q[2] - q[1] for q in ON_PANEL)),
        all(abs(v_ - DERZ) < 0.01 for v_ in dz_.values()) and hz_ < 0.01 and max(q[2] - q[1] for q in ON_PANEL) <= 600.0)
    # 4 · İÇECEK YEDEĞİ: 6 koli yeri AYNI · kapak açıkken koli önü → ön düzlem yolu SERBEST
    kol = [bb("icecek_yedek_koli_%d%d" % (a, b_)) for a in range(len(ICECEK_X)) for b_ in range(ICECEK_KAT)]
    kol6 = [p["wp"].val().BoundingBox() for p in V6.PARCALAR if p["ad"].startswith("icecek_yedek_koli_")]
    yaz("içecek yedeği 6 koli yeri v6 ile aynı (x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f)" % (min(b.xmin for b in kol), max(b.xmax for b in kol), min(b.ymin for b in kol),
        max(b.ymax for b in kol), min(b.zmin for b in kol), max(b.zmax for b in kol)),
        len(kol) == 6 and sorted((b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax) for b in kol) == sorted((b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax) for b in kol6))
    ion = icecek_on_olcum()
    O["icecek_on"] = ion
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    kpay = []
    for x0, x1 in ICECEK_X:
        pr = kut(x0, x1, ICECEK_Y0, ICECEK_YEDEK["y"][1], ICECEK_Z[1], Z_ON + KOLI["z"]).val()
        m_ = min((BRepExtrema_DistShapeShape(pr.wrapped, p["wp"].val().wrapped).Value() for p in PARCALAR
                 if p["grup"] in ("SABIT", "ASANSOR") and not p["ad"].startswith("icecek_") and p["ad"] not in KAPI_ADLARI
                 and _bb_kesisir(pr.BoundingBox(), p["wp"].val().BoundingBox(), pay=-5.0)), default=99.0)
        kpay.append(round(m_, 2))
    O["koli_yolu_pay"] = kpay
    yaz("koli yolu (kapak açık, koli önü z %.0f → ön düzlemin önünde bir koli boyu +%.0f): engel %d · net açıklık x %.1f–%.1f · sütun bindirmeleri %s · en yakın parçaya pay %s mm"
        % (ICECEK_Z[1], Z_ON + KOLI["z"], len(ion["on"]), ion["net"][0], ion["net"][1], [s_["bindirme"] for s_ in ion["sutun"]], kpay),
        not ion["on"] and all(s_["bindirme"] == 0.0 for s_ in ion["sutun"]) and min(kpay) > 0.0)
    # 5 · KAPAK AÇILIŞI (v7b: 1°…155°, sıfır çıkıntılı menteşe · yarım kanat: QR yüzü z 670)
    ag_ = {a: bb(a) for a in KAPI_ADLARI}
    kutle = {a: [p for p in PARCALAR if p["ad"] == a][0]["wp"].val().Volume() * 7.93e-6 for a in [q[0] for q in ON_PANEL]}
    O["panel_kg"] = kutle
    if tam:
        R = kapi_acilma_olcum()
        O["kapak"] = R
        for a in KAPI_ADLARI:
            r = R[a]
            koli_ok = r["koli_serbest_min"] <= KOLI_ACI if a in KUTU_KANAT else not r["koli"]
            yaz("%-26s %d°…%.0f° (%d açı): en uç z +%.1f < QR %.0f (pay %.0f) · E parçalarıyla çakışma %d · koli yolu (−83 → +%.0f) %s · modül dışı kısım z ≥ +%.1f · %.1f kg"
                % (a, KAPI_ACILARI[0], KAPI_MAX_ACI, len(KAPI_ACILARI), r["zmax"], QR_Z, QR_Z - r["zmax"], len(r["cak"]), Z_ON + KOLI["z"],
                   ("≥ %.0f°'de SERBEST (kesişen açılar %s)" % (r["koli_serbest_min"], r["koli"][-3:] if r["koli"] else "yok")) if a in KUTU_KANAT else "ilgisiz (koli bandı dışında)",
                   r["zmin_x_disi"], kutle[a]),
                r["zmax"] < QR_Z and not r["cak"] and koli_ok and r["zmin_x_disi"] >= Z_ON - 0.01, str(r["cak"][:3]))
        # E sol ALT kanadı işletme açısında (90°) K'nın önünde kapladığı bölge → K ALT kapağıyla SIRA KURALI (ikisi aynı anda açılmaz)
        shk = uygula([p for p in PARCALAR if p["ad"] == "onyuz_alt_kanat_sol"][0]["wp"].val(), kapi_matrisi("onyuz_alt_kanat_sol", KOLI_ACI)).BoundingBox()
        O["k_onu_90"] = (shk.xmin, min(shk.xmax, 0.0), shk.zmin, shk.zmax)
        print("     SIRA KURALI: E sol ALT kanadı %.0f°'de x %.1f…%.1f (hat %.1f…%.1f) · z +%.1f…+%.1f → K'nın ALT (bulaşık) kapağının serbest kenarı (hat 4598,5) bu bölgeden döner:"
              " iki kapak AYNI ANDA AÇILMAZ (önce biri kapanır)" % (KOLI_ACI, shk.xmin, shk.xmax, 4600.0 + shk.xmin, 4600.0 + shk.xmax, shk.zmin, shk.zmax))
    # 5b · v7b · ALT kanat kutu kesit + dayama dudağı (denetim bulgusu 4) · kanat ↔ dudak temas yaması (kapalı konum)
    for a in KUTU_KANAT:
        t_, kk_ = temas_alani(_sek(a), _sek("onyuz_alt_dayama_dudagi"))
        O.setdefault("alt_dayama", {})[a] = t_
        yaz("%s: kutu kesit (tava 1,5 + iç sac 1,0 · %d menteşe · %.1f kg) · alt kenarı dayama dudağına yaslanır: temas %.0f mm² (kısa kenar %.1f)"
            % (a, len(MENTESE_Y[a]), kutle[a], t_, kk_), t_ >= 100.0 and len(MENTESE_Y[a]) == 3)
    bd_ = _sek("onyuz_alt_dayama_dudagi").BoundingBox()
    yaz("dayama dudağı y %.0f–%.0f < koli tabanı %.0f (koli yolunu kapatmaz) · z +%.0f…+%.0f (kanat arka kenarı +%.0f)" % (bd_.ymin, bd_.ymax, ICECEK_Y0, bd_.zmin, bd_.zmax, Z_PANEL),
        bd_.ymax < ICECEK_Y0 and abs(bd_.zmax - Z_PANEL) < 0.01)
    # 6 · ROBOT AĞZI
    yaz("ROBOT AĞZI x %.0f–%.0f (hat %.0f–%.0f) · y %.0f–%.0f · derinlik z 0…+%.0f boş (çerçeve / kayıt / panel yok)"
        % (AGIZ["x"][0], AGIZ["x"][1], 4600.0 + AGIZ["x"][0], 4600.0 + AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], Z_ON),
        not [p["ad"] for p in PARCALAR if p["grup"] == "SABIT" and _bb_kesisir(kut(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], 0.0, Z_ON).val().BoundingBox(), p["wp"].val().BoundingBox())
             and p["wp"].val().intersect(kut(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], 0.0, Z_ON).val()).Volume() > 0.01])
    if tam:
        ra = robot_agzi_taramasi()
        O["robot_agzi"] = dict(an=ra["an"], cakisma=len(ra["bul"]), pay={q: round(v[0], 1) for q, v in ra["pay"].items()})
        yaz("robot ağzı taraması: çatal (5) + kutu (14 panel) × E SABİT parçaları · %d an (t %.1f–%.1f, 0,05 sn) · çakışma %d · %.0f sn"
            % (ra["an"], Z_CATAL[0], Z_CATAL[3], len(ra["bul"]), ra["sure"]), not ra["bul"], str(sorted(ra["bul"].items())[:4]))
        print("     ağız payları (en küçük aralık, mm): " + " · ".join("%s %.1f (%s t=%.2f)" % (q, v[0], v[1], v[2]) for q, v in sorted(ra["pay"].items(), key=lambda kv: kv[1][0])))
    # 7 · HAVADA PARÇA
    hv = havada_v7()
    O["havada"] = dict(ham=len(hv["ham"]["bilesen"]), ham_parca=sum(len(d_["uye"]) for d_ in hv["ham"]["bilesen"]), kalan=len(hv["kalan"]), beyaz=hv["beyaz"])
    yaz("havada parça (denetim_temas_v1, tol 0,05): %d parça · zemine bağlı %d · ham bileşen %d → beyaz listeyle %d · KALAN %d"
        % (hv["ham"]["parca"], hv["ham"]["bagli"], len(hv["ham"]["bilesen"]), len(hv["beyaz"]), len(hv["kalan"])), not hv["kalan"],
        " | ".join("%s (%d)" % (d_["en"], len(d_["uye"])) for d_ in hv["kalan"][:6]))
    for b_ in hv["beyaz"]:
        print("     BEYAZ LİSTE: %s … (%d parça) ← %s ~ %s %.3f mm · %s" % (b_["uye"][0], len(b_["uye"]), b_["cift"][0], b_["cift"][1], b_["cift"][2], b_["cift"][3]))
    # 7b · v7b · BAĞLANTI YAMALARI (denetim bulgusu 5): braket / köşebent ↔ taşıyıcı düzlemsel temas + sensör ↔ delik
    kotu, sat = [], []
    for a, b in BAGLANTI_V7B:
        t_, kk_ = temas_alani(_sek(a), _sek(b))
        sat.append("%s↔%s %.0f/%.0f" % (a, b, t_, kk_))
        if t_ < 100.0 or kk_ < 9.9:
            kotu.append((a, b, round(t_, 1), round(kk_, 2)))
    O["baglanti"] = dict(cift=len(BAGLANTI_V7B), kotu=kotu)
    yaz("bağlantı yamaları: %d braket / köşebent çifti · hepsi düzlemsel temas ≥ 100 mm² ve kısa kenar ≥ 10 mm (cıvatalı bindirme) · kötü %d"
        % (len(BAGLANTI_V7B), len(kotu)), not kotu, str(kotu))
    print("     (alan mm² / kısa kenar mm) " + " · ".join(sat))
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    sd_ = []
    for a, b in SENSOR_DELIK:
        A_, B_ = _sek(a), _sek(b)
        sd_.append((a, A_.intersect(B_).Volume(), _DSS(A_.wrapped, B_.wrapped).Value()))
    yaz("M8 sensörler delikli sacta (%d): katı bindirmesi en çok %.3f mm³ · aralık en çok %.3f mm (≤ 0,05 = değer) · iki ucu açık"
        % (len(sd_), max(v for _a, v, _d in sd_), max(d_ for _a, _v, d_ in sd_)), all(v < 0.01 and d_ <= 0.05 for _a, v, d_ in sd_), str(sd_))
    # 7c · v7b · KAPLİN (denetim bulgusu 2): delikli, motora / yatağa binmiyor, mil göbekte, istisna yok
    kp_ = []
    for kap, mot, yat in (("kopru_kaplini", "kopru_motoru", "kopru_BK12"), ("flap_katlayici_kaplini", "flap_katlayici_motoru", "flap_katlayici_yatak_braketi")):
        K_, M_, Y_ = _sek(kap), _sek(mot), _sek(yat)
        kb_, mb_ = K_.BoundingBox(), M_.BoundingBox()
        dal = mb_.ymax - kb_.ymin                           # mil ucu (motorun en üst noktası) − kaplinin alt yüzü
        pilot_pay = kb_.ymin - (mb_.ymax - MIL_UCU + (12.497 - 10.973))   # kaplin altı − pilot üstü
        kp_.append((kap, K_.intersect(M_).Volume(), _DSS(K_.wrapped, M_.wrapped).Value(), dal, pilot_pay, Y_.BoundingBox().ymin - kb_.ymax, K_.intersect(Y_).Volume()))
    O["kaplin"] = kp_
    yaz("kaplin (aday NBK MDS-25C-6.35-10 · Ø25 × %.0f): motorla katı bindirmesi %s mm³ · mil ↔ delik aralığı %s · mil göbeğe dalar %s ≤ göbek %.0f · pilottan pay %s · yatağa pay %s"
        % (KAPLIN["L"], "/".join("%.3f" % q[1] for q in kp_), "/".join("%.3f" % q[2] for q in kp_), "/".join("%.1f" % q[3] for q in kp_), KAPLIN["gobek"],
           "/".join("%.1f" % q[4] for q in kp_), "/".join("%.1f" % q[5] for q in kp_)),
        all(q[1] < 0.01 and q[2] <= 0.05 and 8.0 <= q[3] <= KAPLIN["gobek"] - 0.5 and q[4] >= 2.0 and q[5] >= 1.5 and q[6] < 0.01 for q in kp_))
    yaz("çakışma istisna listesinde kaplin çifti YOK (v7 ilk: (_kaplini, _motoru) pilota binmeyi gizliyordu)", not [q for q in ISTISNA if "_kaplini" in q[0] or "_kaplini" in q[1]])
    # 8 · ASANSÖR STROKU × yeni / değişen parçalar
    if tam:
        at = asansor_strok_taramasi()
        O["asansor_strok"] = dict(strok=at["strok"], cakisma=len(at["bul"]))
        yaz("asansör stroku 0…%.0f mm (somun üst yatağa değene kadar, %d konum) × v7 yeni / değişen %d parça → çakışma %d" % (at["strok"], at["adim"], at["hedef"], len(at["bul"])),
            not at["bul"], str(sorted(at["bul"].items())[:4]))
    # 9 · HESAPLAR (kaba — iddiaların sayısal dayanağı)
    E_ = 193000.0
    koli_kg = len(ICECEK_X) * ICECEK_KAT * 8.7                                      # VARSAYIM: 24 × 330 ml kutu ≈ 8,4 kg + karton ≈ 8,7 kg/koli
    q_ = koli_kg * 9.81 / ((ICECEK_X[-1][1] - ICECEK_X[0][0]) * (ICECEK_Z[1] - ICECEK_Z[0]))        # N/mm²
    serit = lambda L: (5.0 * q_ * L ** 4 / (384.0 * E_ * 3.0 ** 3 / 12.0), q_ * L ** 2 / 8.0 / (3.0 ** 2 / 6.0))
    d6, s6 = serit(W - 2.0 * SAC); d7, s7 = serit(AYAK_XZ[4][0] - SAC)
    O["taban"] = dict(kg=koli_kg, v6=(d6, s6), v7=(d7, s7))
    print("     HESAP · taban 3 mm (içecek yedeği %.0f kg → %.0f Pa, şerit yaklaşımı · kaba): v6 açıklık %.0f → sehim %.1f mm · σ %.0f MPa  |  v7 orta ayak → açıklık %.0f → %.1f mm · σ %.0f MPa (304 akma ≈ 215)"
          % (koli_kg, q_ * 1e6, W - 2 * SAC, d6, s6, AYAK_XZ[4][0] - SAC, d7, s7))
    m_y = (Y_YIGIN_UST - Y_PLAT) / 1.6 * 0.160 + 10.0
    e_ = abs((ZS0 + ZS1) / 2.0 - (-376.0))
    M_ = m_y * 9.81 * e_
    L_ = 972.0 - (Y_PLINT + 3.0)
    Hk = M_ / L_
    A_, Iu, Iv, cv, cu = _kesit_I(((-382.0, -378.0, 940.0, 972.0), (-404.0, -382.0, 968.0, 972.0)))     # u = z, v = y (köşebent kesiti · v7b: L 4 mm, plakanın arkasında)
    kol_ = 200.0 - SAC + 30.0
    sz = (Hk / 2.0) * kol_ * cu / Iv; sy = (m_y * 9.81 / 2.0) * kol_ * cv / Iu
    O["ray_plakasi"] = dict(kg=m_y, e=e_, M=M_, H=Hk, s_yatay=sz, s_duzey=sy)
    print("     HESAP · ray plakası: yığın + platform %.0f kg · dışmerkezlik %.0f mm → moment %.0f N·m · v7 alt (taban flanşı) + üst (2 köşebent) mesnet: yatay tepki %.0f N ·"
          " köşebent (konsol %.0f) σ yatay %.0f MPa · taban sehim ederse düşey yükün tamamıyla σ %.0f MPa (akma ≈ 215) · v6: plaka havadaydı (mesnetsiz)"
          % (m_y, e_, M_ / 1000.0, Hk, kol_, sz, sy))
    gk = max(kutle[a] for a in KAPI_ADLARI)
    msay = {a: len(MENTESE_Y[a]) for a in KAPI_ADLARI}
    sinir = {a: 6.8 * (msay[a] - 1) for a in KAPI_ADLARI}      # Blum kılavuzu (≤ 900 mm kapak): 2 menteşe < 15 lb (6,8 kg), 3 menteşe < 30 lb (13,6 kg) — okuma VARSAYIM
    print("     HESAP · kanat kütleleri (304 · 7,93 g/cm³): %s · menteşe sayısı / sınır (Blum kılavuzu, ≤ 900 mm): %s"
          % (" · ".join("%s %.1f" % (a[6:], kutle[a]) for a in KAPI_ADLARI), " · ".join("%s %d / %.1f kg" % (a[6:], msay[a], sinir[a]) for a in KAPI_ADLARI)))
    # v7b · ALT kanat burulması (denetim bulgusu 4): alt serbest köşe, en alttaki menteşenin altında L konsol · F köşede (VARSAYIM 20 N: koli / el)
    G_ = 77000.0
    b_k = X_ORTA_DERZ[0] - SAC - TAVA_T                     # kesit orta çizgisi genişliği
    h_k = TAVA - TAVA_T / 2.0 - IC_SAC / 2.0                # ön sac ↔ iç sac orta çizgileri arası
    J_kutu = 4.0 * (b_k * h_k) ** 2 / (b_k / TAVA_T + b_k / IC_SAC + 2.0 * h_k / TAVA_T)     # Bredt (kapalı ince cidar)
    J_acik = (b_k * TAVA_T ** 3 + 2.0 * h_k * TAVA_T ** 3) / 3.0                                # açık tava (v7 ilk)
    L_k = min(MENTESE_Y["onyuz_alt_kanat_sol"]) - 30.0 - Y_ALT[0]
    F_k = 20.0
    dk = F_k * (X_ORTA_DERZ[0] - SAC) ** 2 * L_k / (G_ * J_kutu); da = F_k * (X_ORTA_DERZ[0] - SAC) ** 2 * L_k / (G_ * J_acik)
    O["alt_kanat_burulma"] = dict(J_kutu=J_kutu, J_acik=J_acik, L=L_k, d_kutu=dk, d_acik=da)
    print("     HESAP · ALT kanat burulması: alt serbest köşe en alttaki menteşenin %.0f mm altında · köşede %.0f N (VARSAYIM) → açık tava J %.0f mm⁴: %.1f mm (v7 ilk) ·"
          " kutu kesit J %.0f mm⁴: %.2f mm (v7b) + içe dayama dudağı" % (L_k, F_k, J_acik, da, J_kutu, dk))
    # v7b · şarjör eşiği (denetim bulgusu 3): üst bant iki uçtan köşebentle mesnetli kiriş · yük = 2. blanka üstteki blankın sürtünmesi
    mu_, m_b = 0.5, 0.160                                   # VARSAYIM: karton–karton μ 0,5 · blank 0,16 kg (asansör hesabıyla aynı)
    F_e = mu_ * m_b * 9.81
    L_e = ((X_BL1 - 16.0) - (X_BL0 + 16.0))                 # köşebent bindirmelerinin ortaları arası
    I_e = (Y_KAPI_UST - 944.0) * 3.0 ** 3 / 12.0            # yalnız üst bant (dişler + ayaklar ihmal: güvenli taraf)
    de = 5.0 * F_e * L_e ** 3 / (384.0 * E_ * I_e)
    O["esik"] = dict(F=F_e, L=L_e, I=I_e, d=de)
    print("     HESAP · şarjör eşiği: 2. blanka sürtünme %.2f N (μ %.1f VARSAYIM) · üst bant %.0f × 3 (I %.0f mm⁴) iki köşebent arası %.0f mm yayılı yük → sehim %.2f mm"
          " < 2. blank kenarına pay 0,5 (üst kenar 980,8 yerinde kalır) · v7 ilk: eşik yalnız 3 mm alt kenarıyla tabanda duruyordu (mesnetsiz)" % (F_e, mu_, Y_KAPI_UST - 944.0, I_e, L_e, de))
    A_yuzey = 2.0 * (W * H + (D + Z_ON) * H + W * (D + Z_ON)) * 1e-6
    kayip = 7 * 4.0 + 3 * 10.0 + 3 * 7.0 + 10.0                                    # VARSAYIM: sürücü bekleme 4 W · aynı anda 3 eksen × 10 W · NDR-240 kaybı ~7 W · PLC 10 W
    O["isi"] = dict(W_=kayip, A=A_yuzey, dT=kayip / (5.5 * A_yuzey))
    print("     HESAP · ısı: pano + sürücü kaybı ≈ %.0f W (VARSAYIM) · kabuk yüzeyi %.1f m² × 5,5 W/m²K (doğal taşınım + ışınım, VARSAYIM) → iç sıcaklık artışı ≈ %.1f K"
          " → havalandırma yarığı gerekmez (robot ağzı %.0f × %.0f ayrıca açık)" % (kayip, A_yuzey, kayip / (5.5 * A_yuzey), AGIZ["x"][1] - AGIZ["x"][0], AGIZ["y"][1] - AGIZ["y"][0]))
    yaz("hesap sınırları: taban σ %.0f < 107 (akma/2) · köşebent σ %.0f / %.0f < 107 · kanatlar menteşe sınırında (en ağır %.1f kg) · ΔT %.1f < 10 K · "
        "ALT kanat köşesi %.2f < 0,5 mm · eşik sehimi %.2f < 0,5 mm" % (s7, sz, sy, gk, O["isi"]["dT"], dk, de),
        s7 < 107.0 and sz < 107.0 and sy < 107.0 and all(kutle[a] <= sinir[a] for a in KAPI_ADLARI) and O["isi"]["dT"] < 10.0 and dk < 0.5 and de < 0.5)
    O["denetim_sayisi"] = SAY[0]
    print("OLCUM v7: %d denetim · hepsi GEÇTİ" % SAY[0])
    return O


''')

# ---------------------------------------------------------------- 17 · GLB · BOM · modül · ana ----------------------------------------------------------------
d('"generator": "AUTOKITCH kutu_cad_v6"', '"generator": "AUTOKITCH kutu_cad_v7"')
d('"UHMW", "Pizza kutusu", "FR5", "İçecek kolisi")) else "ÜRETİM"', '"UHMW", "Pizza kutusu", "FR5", "İçecek kolisi",\n'
  '                                                  "Gizli menteşe", "Bas-aç", "Mesafe burcu")) else "ÜRETİM"')
d('ALT_KURAL = [r"^asansor_vidasi_alt_ucu$", r"^ayak_[1-3]$",', 'ALT_KURAL = [r"^asansor_vidasi_alt_ucu$", r"^ayak_[1-5]$",')
d('r"^kablo_kanali_(1|dikey_alt|dikey_ust)$",', 'r"^kablo_kanali_(1|dikey_ust)$",')
d('    govde(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); icecek_yedegi(); blank(); catal_pizza()',
  '    govde(); onyuz(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); icecek_yedegi(); blank(); catal_pizza()')
assert s.count('if __name__ == "__main__":') == 1
s = s[:s.index('if __name__ == "__main__":')] + r'''if __name__ == "__main__":
    t0 = time.time()
    arg = sys.argv[1:]
    modul()
    print("E KUTU MODULU v7 (on duzlem +79 · derinlik 909 · tava paneller + robot agzi · ic duzen ve kinematik v6 ile ayni): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    olcum(); sys.stdout.flush()
    olcum_v7(tam="hizli" not in arg); sys.stdout.flush()
    if "hizli" not in arg:
        b1 = cakisma(); sys.stdout.flush()
        b2 = kutu_cakisma(); sys.stdout.flush()
        b4 = pizza_cakisma(); sys.stdout.flush()
        b3 = kutu_cakisma(anlar=GECIS_ANLARI, etiket="gecis") if "gecis" in arg else {}
        sys.stdout.flush()
        print("CAKISMA OZETI v7: makine %d · kutu duragan %d · pizza %d · kutu gecis %s" % (len(b1), len(b2), len(b4), len(b3) if "gecis" in arg else "-"))
        assert not b1 and not b2 and not b4 and not b3, "v7: cakisma var"
    if "glb" in arg or "hepsi" in arg:
        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v7.glb")); sys.stdout.flush()
    if "bom" in arg or "hepsi" in arg:
        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v7"))
    print("toplam %.0f sn" % (time.time() - t0))
    sys.stdout.flush()
    os._exit(0)
'''

# ---------------------------------------------------------------- 18 · son denetim (üretilen metin) ----------------------------------------------------------------
for _eski in ('ekle("plint_on"', 'ekle("on_ust_kapak"', 'ekle("on_ust_kapak_kulp"', 'ekle("kose_dikme_on_%d"', 'ekle("sarjor_yan_kapisi_kulp"', "def olcum_v5():", "def olcum_v6():",
              "olcum_v5(); sys.stdout.flush()", "olcum_v6(); sys.stdout.flush()", "kutu_modulu_v6.glb", '"5_PACK_kutu_v6"', "AUTOKITCH kutu_cad_v6\"", 'm["govde"]',
              "kut(801.0, 826.0", '("_kaplini", "_motoru")', "Sugatsune HES3D-70", "kut(596.0, 618.0, 147.0, 150.0"):
    assert _eski not in s, "v7: eski metin kaldi: %s" % _eski
for _yeni in ("Z_ON = 79.0", "def onyuz():", "def tava(", "def olcum_v7(", "def havada_v7(", "def kapi_acilma_olcum(", "def robot_agzi_taramasi(", "def asansor_strok_taramasi(",
              "def on_yuz_izgarasi(", "govde(); onyuz(); sarjor()", "olcum_v7(tam=", "kutu_modulu_v7.glb", "5_PACK_kutu_v7", "_nema23_tam()", 'MALZEME.setdefault("pu"',
              "MENTESE_OFSET = TAVA", "def derz_olcum(", "BAGLANTI_V7B = (", "def temas_alani(", "onyuz_alt_dayama_dudagi", "sarjor_kapi_esigi_kosebendi_", "KAPLIN = dict("):
    assert _yeni in s, "v7: eksik: %s" % _yeni
compile(s, "kutu_cad_v7.py", "exec")
hedef = os.path.join(U, "kutu_cad_v7.py")
assert not os.path.exists(hedef), "kutu_cad_v7.py zaten var — üstüne yazılmaz (yeniden üretmek için önce elle sil)"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kutu_cad_v7.py yazildi (%d satir)" % s.count(NL))
