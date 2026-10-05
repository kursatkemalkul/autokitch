# -*- coding: utf-8 -*-
"""hat_montaj_v56 → hat_montaj_v57 (27 Eyl 2026) — ALÇAK HAT (Kemal: "bu teknik resme göre 3D modelle, sitede her şeyi güncelle, kontrol et").
Kaynak: SPEC_alcak_hat_v57.md (+ "Kesinleşen kararlar") · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4 · keşif (kesif_montaj) + üreteç raporları (denetçi düzeltmeleri geçerli).
Ev kuralı: v56 metnine sayısı denetlenen (count-assert) değiştirmeler + işaretli blok değiştirmeleri; v56 DEĞİŞMEZ, çıktı yalnız hat_montaj_v57.py.
Yeni üreteçler: store_cad_v6 · kesme_cad_v4 · kutu_cad_v5 · firin_tp10_cad_v7 · itici_cad_v4 · qr_cad_v1 · tezgah_cad_v1 · ray_ek_cad_v1 · kaide_cad_v1
(bulaşık bulasik_cad_v1 aynı, yeri KS.BULASIK_YER)."""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v56.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def satir(bas, yeni, n=1):
    """`bas` ile BAŞLAYAN satır(lar) TAM n tane olmalı → satırın tamamı `yeni` (çok satırlı olabilir)"""
    global s
    L = s.split(NL)
    idx = [i for i, l in enumerate(L) if l.startswith(bas)]
    assert len(idx) == n, (len(idx), bas[:110])
    for i in idx:
        L[i] = yeni
    s = NL.join(L)


def once(bas, ek):
    """`bas` ile başlayan TEK satırın ÖNÜNE `ek` (sonunda NL olmalı) eklenir"""
    global s
    L = s.split(NL)
    idx = [i for i, l in enumerate(L) if l.startswith(bas)]
    assert len(idx) == 1, (len(idx), bas[:110])
    L[idx[0]] = ek + L[idx[0]]
    s = NL.join(L)


def blok(a, b, yeni):
    """a (tek) işaretinden b (tek) işaretine kadar (b hariç) → yeni"""
    global s
    assert s.count(a) == 1, (s.count(a), a[:110])
    assert s.count(b) == 1, (s.count(b), b[:110])
    i = s.index(a); j = s.index(b)
    assert i < j, (a[:60], b[:60])
    s = s[:i] + yeni + s[j:]


# ================================================================ 1 · DOCSTRING (değişiklik kaydı) ================================================================
degis('"""v56 (27 Eyl 2026):', '"""v57 (27 Eyl 2026): ALÇAK HAT (Kemal: "bu teknik resme göre 3D modelle" · SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4) — bütün mekanizma 168 aşağı:' + NL +
      '  TEK DÜZ ÇİZGİ 788 = çekmeceli dolap üstü = A/C kabin tabanı = fırın gövdesi altı (basamak yok) · A/C mekanizma 892 (kaide 104, kaide_cad_v1) · disk 1000 ·' + NL +
      '  fırın bandı 998 · K bandı 996 · E tepsisi 936 · makine üstü 1862 · v56\'daki tek H_B (4 anlam) → Y_DUZ 788 + Y_MEK 892 (+ sözleşme assert\'leri) ·' + NL +
      '  B = store_cad_v6 (tek parça 0–4000 × 123–788, 24 çekmece, fırın altı PU 60 + taşıyıcı, robot çöpü şeridi 3810–4000) · F taban dolabı KALKTI (fırın' + NL +
      '  firin_tp10_cad_v7 dolabın üstüne oturur · itici_cad_v4) · K = kesme_cad_v4 (taban 892) + BULAŞIK K altında (KS.BULASIK_YER) + deterjan/parlatıcı ·' + NL +
      '  E = kutu_cad_v5 (şarjör 462, içecek yedeği 6 koli E altında) · TOPPING: TC yerel y 892\'de, TU dünyada BİR KEZ −168 · hava hattı −168 ·' + NL +
      '  YENİ MODÜL S (SERVİS / TESLİM): QR dolabı qr_cad_v1 (860 × 520 × 2050 · 12 göz · robot kontrol + ana pano + UPS içinde) + tezgâh tezgah_cad_v1 ·' + NL +
      '  ray ekleri ray_ek_cad_v1 (zincir oluğu · enerji zinciri robot x 2650\'de SABİT · robot kablosu · zemin kanalı) · yolculuk: K3 pide çekmecesi → … →' + NL +
      '  QR gözü (sütun 1 · satır 3) robot kapağı açılır/kapanır · yeni denetimler: sözleşme, fırın ↔ dolap, kaide ↔ TOPPING/dolap, S + ray ekleri,' + NL +
      '  QR erişim tablosu, kapasite, bulaşık K altında.' + NL +
      'v56 (27 Eyl 2026):')

# ================================================================ 2 · SABİTLER (pafta v7'nin H_B / H_MAK / W_B'si geçersiz) ================================================================
satir('DZ, H_MAK, H_B = _g7["DZ"], _g7["H_MAK"], _g7["H_B"]', '''DZ = _g7["DZ"]                                                                           # 830
# ---- v57 · ALÇAK HAT (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4) · pafta v7'nin taban 1060 / üst 2030 / B genişliği 2500 değerleri GEÇERSİZ ----
# v56'daki tek taban sabiti (1060) dört ayrı şey demekti (B üstü · A/C kabin tabanı · TOPPING CAD orijini · K istasyon tabanı) → ikiye ayrıldı.
# Toptan yeniden adlandırma parçaları sessizce kaydırırdı (keşif riski 1); her kullanım tek tek Y_DUZ / Y_MEK yapıldı.
DY = -168.0                                   # v56 → v57 bütün mekanizma kotlarının farkı (1060 → 892)
Y_DUZ = 788.0                                 # TEK DÜZ ÇİZGİ: çekmeceli dolap üstü = A/C kabin tabanı = fırın gövdesi altı (basamak yok)
Y_MEK = 892.0                                 # A/C mekanizma tabanı (Y_DUZ + kaide 104) = TOPPING CAD (TC, yerel y) orijini = K istasyon tabanı
H_MAK = 1862.0                                # makine üstü (bütün istasyonlar)
W_B = 4000.0                                  # çekmeceli dolap TEK PARÇA 0–4000
assert abs(Y_MEK - (_g7["H_B"] + DY)) < 0.01 and abs(H_MAK - (_g7["H_MAK"] + DY)) < 0.01, "v57: pafta v7 kotlari + DY tutmuyor"


def _gk(ok):
    """v57 · denetim satırının sonucu (açık PASS / FAIL)"""
    return "GECTI [PASS]" if ok else "KALDI [FAIL]"

''')
satir('X_A, W_A, X_BC, W_BC, W_B = _g7["X_A"]', 'X_A, W_A, X_BC, W_BC = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"]                     # A 0-700 · C 700-2500 · v57: W_B yukarıda (4000)')
satir('QRX, QRZ = _g7["QRX"], _g7["QRZ"]', '''# v57: QR yeri ve ölçüsü qr_cad_v1'den (pafta v7'deki QR yer tutucusu kalktı) · S modülü (QR + tezgâh) · ray ekleri · A/C kaidesi — hepsi dünya koordinatı
import qr_cad_v1 as QR, tezgah_cad_v1 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v1 as KD''')
satir('T_KAS = (H_B + TC.KAS[0], H_B + TC.KAS[1])', "T_KAS = (Y_MEK + TC.KAS[0], Y_MEK + TC.KAS[1])    # v35: kaset kotu CAD'den · v57: Y_MEK (ölü sabit — kaset döngüsü boş)")
satir('P = H_B + DISK_UST_Y', 'P = Y_MEK + DISK_UST_Y                            # 1000 (v56: 1168)')
satir('BANT_UST = H_B + 106.0', 'BANT_UST = Y_MEK + 106.0                          # 998 · firin bandi ust kosu (CAD AKT_Y: diskin 2 mm alti) · v56: 1166')
satir('PLAKA = BANT_UST - 2.0', 'PLAKA = BANT_UST - 2.0                            # 996 · kesme plakasi bandin 2 mm ALTINDA: urun hep asagi iner')
satir('TEPSI_Y = PLAKA - 60.0', 'TEPSI_Y = PLAKA - 60.0                            # 936 · kutu tepsisi yuzu (pafta kurali: surec - 60) -> kutu agzi ~981')
satir('F_G1 = BANT_UST + 320.0', 'F_G1 = BANT_UST + 320.0                           # (ölü) firin govdesi ustu (pafta: bant + 320)')
blok('MODUL = [("A", "MODÜL A', '# ---------------------------------------------------------------- KÜTÜK', '''X_S = TZ.X0 - TZ.TASMA                                   # v57 · S modülü solu = tezgâh tablası (3935) … sağı = QR dolabının sağı = hattın ucu (5430)
MODUL = [("A", "MODÜL A · KONİLİ AÇICI (dolap üstünde · kaide 104)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 0–4000)", X_A, W_B),
         ("C", "MODÜL C · TOPPING (dolap üstünde · kaide 104)", X_BC, W_BC), ("D", "MODÜL F · KONVEYÖR FIRIN", X_D, W_D),
         ("K", "MODÜL K · KESME + SPREY (+ taban: bulaşık)", X_K, W_K), ("E", "MODÜL E · KUTU KATLAMA (tek parça)", X_E, W_E),
         ("S", "MODÜL S · SERVİS / TESLİM (QR dolabı + tezgâh)", X_S, HAT_W - X_S)]
MODUL_Y = {"A": (Y_DUZ, H_MAK), "B": (0.0, Y_DUZ), "C": (Y_DUZ, H_MAK), "D": (Y_DUZ, H_MAK), "K": (0.0, H_MAK), "E": (0.0, H_MAK), "S": (QR.Y0, QR.Y0 + QR.H)}

''')
once('# --- C · TOPPING: dozaj kasetleri', '''

def _dis_birim(M, durum, kaynak, sayfa):
    """v57 · dünya koordinatlı yeni üreteçlerin birimleri (bulasik_cad_v1 sözleşmesi: kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL)"""
    for _k, _a in M.BIRIMLER:
        _bb = [M.dunya(_p).BoundingBox() for _p in M.PARCALAR if _p["birim"] == _k]
        assert _bb, "%s: %s biriminin parcasi yok" % (kaynak, _k)
        birim(_k, _a, M.BIRIM_MODUL[_k], durum, (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
              (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", kaynak, sayfa(_k) if callable(sayfa) else sayfa)


''')

# ================================================================ 3 · TOPPING (TC yerel 892 · TU dünyada bir kez −168) + hava ================================================================
degis('(X_BC, X_BC + W_BC), (H_B, H_B + TC.Y), (-DZ, 0.0), "sac", "topping_uno_cad_v11.py + topping_cad_v24.py"',
      '(X_BC, X_BC + W_BC), (Y_MEK, Y_MEK + TC.Y), (-DZ, 0.0), "sac", "topping_uno_cad_v11.py (dünya y −168) + topping_cad_v24.py (yerel y + 892)"')
blok('birim("HAVA_KOMPRESOR",', '# ---- v42 · TOPPING v2 parçaları ----', '''birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · FIRIN ÜSTÜNDE (havalandırmalı raf 1348, ortam sınırı 40 °C, davlumbaz bölmesinin ön yarısı, kutu yedeğinin yanı — TOPPING'in tek istisnası) · Ø10 ana hat y 1809'da fırın üstünden TOPPING teknik cebine → kuru bölme → şartlandırıcı · K'ye dal (MS4 tepesi 1692 + 10)", "D", "GERCEK_HAVA",
      (3600.0, 3980.0), (1348.0, 1858.0), (-420.0, -40.0), "sac", "topping_uno_cad_v11.py", "hat/topping_v2.html")     # v57: y −168 (raf üstü 1348 · sözleşmede ölçülür)
''')
satir('import firin_tp10_cad_v6 as FT', '''# ---- v57 · ALÇAK HAT: TU (topping_uno_cad_v11, DÜNYA y) BİR KEZ −168 kaydırılır — bütün parçalar + dönen grup pivotları (VALF_/PISTON_/HELEZON_/KARISTIRICI_/TABLA).
#      TC (topping_cad_v24, YEREL y) KAYDIRILMAZ: TOPPING_MODUL y0 = Y_MEK ile yerleşir. İkisi karışırsa ya iki kez ya hiç kaymaz (keşif riski 2).
for _q in TU.P:
    _q["sh"] = _q["sh"].translate(cq.Vector(0.0, DY, 0.0))
for _g in list(TU.GRUP):
    if _g != "SABIT":
        TU.GRUP[_g] = (TU.GRUP[_g][0], TU.GRUP[_g][1] + DY, TU.GRUP[_g][2])
TU_YAL_Y0 = TU.YAL_Y0 + DY                                                                # soğuk oda yalıtım altı 1277 → 1109 (aktarma iticisinin kirişi buna bağlanır: IT.TAVAN)
import firin_tp10_cad_v7 as FT                                                          # v57: alçak hat (BANT_UST_HAT 998 · gövde 788–1305 · raf 1348) · v49: havalandırmalı raf''')
satir('import itici_cad_v3 as IT', 'import itici_cad_v4 as IT                                                              # v57: DISK_UST 1000 · TAVAN 1109 · v49: aktarma iticisi (dünya koordinatı)')
satir('KOMP_KAY = (-510.0, 976.0, 0.0)', 'KOMP_KAY = (-510.0, 976.0, 0.0)               # v48: kompresör (TU x 3410–3790 · z −40…−420) → fırın üstü raf: dünya x 3600–3980 · v57: TU −168 kaydırıldığı için AYNI kalır → y 1348–1844 (raf üstü 1348)')
once('# --- B · ÇEKMECE MODÜLÜ (v36', '''# v57 · hava ana hattı TOPPING / fırın / K ile birlikte RİJİT −168: teknik cep 1977 → 1809 · fırın üstü 1335 → 1167 · K dalı ucu 1870 → 1702 (MS4 tepesi 1692 + 10, sözleşmede ölçülür)
ANA_V44 = [(x_, y_ + DY, z_) for x_, y_, z_ in ANA_V44]
ANA_K48 = [(x_, y_ + DY, z_) for x_, y_, z_ in ANA_K48]

''')

# ================================================================ 4 · B · ÇEKMECELİ DOLAP (store_cad_v6) ================================================================
satir('import store_cad_v5 as SC', 'import store_cad_v6 as SC                                  # v57: TEK PARÇA çekmeceli dolap 0–4000 × 123–788 (24 çekmece · fırın altı PU 60 + taşıyıcı · robot çöpü şeridi) · v44: tam kaplayan kapaklar')
blok('_SC_AD = {"B_KASA":', '_TIP_AD = {', '''_SC_AD = {"B_KASA": "ÇEKMECELİ DOLAP gövdesi (tek parça, +3 °C): sandviç kabuk + PU + 6 bölme · 0–4000 × 123–788 · ön çerçeve + plint · fırın altında PU 60 ısı kalkanı (2517–3793 × 728–788)",
          "B_ELEKTRIK": "K4 · Secop'un arkasında pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),
          "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + yatay (K1→K4 703–728 · K4→K6 643–668, bölmelerden geçer)",
          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 6 roll-bond evaporatör + 6 fan (soğutma yükü hesabı AÇIK)",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C · 2 gün (GN 1/1-100 kaşar + GN 1/2-100 sucuk) · 4 günün 2. yarısı",
          "B_TASIYICI": "Fırın taşıyıcı çerçevesi 304: 2 kiriş 40 × 40 × 2 (y 746,5–786,5) + 3 çapraz + 6 dikme (bölmelerin içinde, altlarında ayak) · fırın 200 kg + raf 99 kg (VARSAYIM)",
          "B_COP": "ROBOT ÇÖPÜ şeridi 3810–4000 (soğuk DEĞİL, 3810'da yalıtımlı ara duvar): 15 L kova 165 × 300 × 400 (poşetli, kızaklı) · atma boşluğu · ön yüzde 130 × 130 yaylı klape (y 610–740, menteşe 748)"}
''')
degis('"ic1d": "içecek · tek kat (dar) · yaylı itici", "tatli": "tatlı · 5 şerit"}', '"ic1d": "içecek · tek kat (dar) · yaylı itici", "tatli": "tatlı · 2 şerit"}')
degis('birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v5.py", "")', 'birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v6.py", "")')

# ================================================================ 5 · A kabini + KAİDE · D (fırın üstü) · F · İTİCİ ================================================================
satir('birim("A_KABIN",', '''birim("A_KABIN", "AÇICI modülü kabini (dolap üstünde 788 · mekanizma kaidede 892 · açıcının kendisi TOPPING CAD'inde)", "A", "KUTU", (X_A, X_A + W_A), (Y_DUZ, H_MAK), (-DZ, 0.0), "kabin", "pafta ATOSA TABLALI v7 · v57 alçak hat")
# ---- v57 · A + C MEKANİZMA KAİDESİ 104 (kaide_cad_v1, dünya): dolap üstü 788 → mekanizma tabanı 892 · A: açıcı kolonu + tekne sacı 892–893,5 · C: TOPPING dis_taban ----
KD.kur()
_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v1.py", lambda k_: "hat/press.html" if KD.BIRIM_MODUL[k_] == "A" else "hat/topping_v2.html")''')
blok('# ============================ v35 · TABAN HIZASI', 'FT.kur(ayak=False, plaka=False, uyarla=True)', '''# ============================ v57 · ALÇAK HAT (v35 TABAN HIZASI'nın yerine) ============================
# Kemal 27 Eyl (ALCAK_HAT_RESIM1_v4): TEK DÜZ ÇİZGİ 788 — çekmeceli dolabın üstü = A/C kabin tabanı = fırın gövdesinin altı (basamak yok).
# A/C mekanizmaları kaide 104 üstünde (892) · K istasyon tabanı 892 · E (kutu katlama) KESİLMEZ: yerden 1862'ye tek parça.
# SÜREÇ: disk 1000 > fırın bandı 998 > kesme plakası 996 > kutu ağzı ~981 — ürün hep aşağı iner.
# F TABAN DOLABI KALKTI (yeri dolabın K5, K6 ve şeridi) · temizlik → tezgâh · deterjan → K altı · robot kontrol / ana pano / UPS → QR dolabı · içecek yedeği → E altı.

# --- D · (paftada F) KONVEYOR FIRIN · fırın üstü raf (1305–1348) ---
PIZZA_UST_KUTU = 320                                                                     # fırın üstü raftaki pizza kutusu yedeği (kural 5.5)
birim("D_DAVLUMBAZ", "Egzoz davlumbazı (bizim) · fan · yağ + karbon filtre · fırın üstü bölmenin ARKA yarısı (ön yarıda kutu yedeği + kompresör) · komşu modüllere asılı", "D", "KUTU", (X_D, X_D + W_D), (FT.YG1 + 10.0, H_MAK), (-DZ, -425.0), "kutu", "v48 · v57: 1315–1862")
birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · TEK YER: fırın üstü SOL, rafta %d kutu düz (804 × 404 × 512) · E şarjörü 462 + %d = 782 ≈ 2,8 gün (SPEC · şarjörün kullanılabilir kısmı ≈ 432 → 752, karar Kemal'de) (Kemal 27 Eyl: sola koy)" % (PIZZA_UST_KUTU, PIZZA_UST_KUTU), "D", "KUTU",
      (X_D + 20.0, X_D + 824.0), (FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + 512.0), (-424.0, -20.0), "karton", "v48 · kural 5.5 · v57 raf 1348")
''')
degis('"sac", "firin_tp10_cad_v6.py", "hat/oven.html")', '"sac", "firin_tp10_cad_v7.py", "hat/oven.html")')
blok('# ---- v53 · BULAŞIK MAKİNESİ (gerçek model, dünya koordinatı) ----', '# ---- v49 · AKTARMA İTİCİSİ', '')      # v57: bulaşık K'ye taşındı (aşağıda, KS'den sonra)
degis('"sac", "itici_cad_v3.py", "hat/oven.html#itici")', '"sac", "itici_cad_v4.py", "hat/oven.html#itici")')

# ================================================================ 6 · K (kesme_cad_v4) + BULAŞIK + DETERJAN ================================================================
satir('import kesme_cad_v3 as KS', "import kesme_cad_v4 as KS                                  # v57: alçak hat (taban 892, bant 996, üst 1862) + bulaşık yeri + deterjan/parlatıcı · kutu_cad_v5'i içe alır · v54: tank + pano yukarıda")
degis('taban 123 · istasyon tabanı 1060 · kapılar', 'taban 123 · istasyon tabanı 892 (v57) · kapılar')
degis('      "hava_hortumu_", "sensor_", "kesici_reed")),' + NL + ']',
      '      "hava_hortumu_", "sensor_", "kesici_reed")),' + NL +
      '    ("K_DETERJAN", "Deterjan + parlatıcı kanisterleri 2 × 5 L (190 × 125 × 285 VARSAYIM) · bulaşığın ARKASINDA raf 325–330 · dozaj hortumları MEIKO arkasına (arka pay 25 korunur) · kanister değişimi için bulaşık öne çekilir (AÇIK)",' + NL +
      '     ("deterjan_",)),' + NL + ']')
degis('("K_ELEKTRIK", "Pano (taban arkası): ', '("K_ELEKTRIK", "Pano (arka duvarda, üstte · v57: K tabanının altında bulaşık + deterjan): ')
degis('raise AssertionError("kesme_cad_v3 parcasi birimsiz kaldi: "', 'raise AssertionError("kesme_cad_v4 parcasi birimsiz kaldi: "')
degis('"sac", "kesme_cad_v3.py", "hat/kesme.html")', '"sac", "kesme_cad_v4.py", "hat/kesme.html")')
once('# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---', '''# ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v1 gerçek model · yer kesme_cad_v4'ten KS.BULASIK_YER = (4108,5 · 126 · −20) — denetçi düzeltmesi: makine z −645…−12) ----
# KS.modul() BM'yi kendi içinde kurar ama BM.X0/Y0/Z0 ve PARCALAR'ı geri koyar (denetçi doğruladı) → burada, KS'den SONRA kendi yerine kurulur.
BM.X0, BM.Y0, BM.Z0 = KS.BULASIK_YER
BM.kur()
BM_KOD = {"K_BULASIK": "D_BULASIK"}                                                      # montaj kodu → bulasik_cad_v1 birim kodu · site malzemeden seçer: MK_K_BULASIK
for _k, _a in BM.BIRIMLER:
    _kk = [k_ for k_, v_ in BM_KOD.items() if v_ == _k][0]
    _bb = [BM.dunya(_p).BoundingBox() for _p in BM.PARCALAR if _p["birim"] == _k]
    birim(_kk, "K altında (ön dikmelerin arasında, sağ ön dikmeye yaslı) · " + _a, "K", "GERCEK_BULASIK", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "bulasik_cad_v1.py", "hat/kesme.html")

''')

# ================================================================ 7 · E (kutu_cad_v5) ================================================================
satir('import kutu_cad_v4 as KC', 'import kutu_cad_v5 as KC                                  # v57: alçak hat (tepsi 936, alt raf 618–622, şarjör 462) + içecek yedeği 6 koli · v54: kalıp ayakları alt rafta')
degis('("E_SARJOR", "Şarjör + asansör: 567 kutu (1,6 mm) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3"',
      '("E_SARJOR", "Şarjör + asansör: 462 kutu (1,6 mm · yığın 240–980; kullanılabilir ≈ 432: asansör somunu 935\'te durur, v4\'ten miras — karar Kemal\'de) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3"')
degis('    ("E_PIZZA", "Pizza Ø300 (K plakasından kutuya kayar)", ("pizza_",)),' + NL + ']',
      '    ("E_PIZZA", "Pizza Ø300 (K plakasından kutuya kayar)", ("pizza_",)),' + NL +
      '    ("E_ICECEK_YEDEK", "İçecek yedeği 6 koli (2 sütun × 3 kat · koli 400 × 267 × 123 · 24 kutu) = 144 · E altı önde, soğutmasız · dolaptaki 144 + 144 = 288 (4 gün 277) · kapısız ön sacın arkasında (erişim AÇIK)", ("icecek_",)),' + NL + ']')
degis('raise AssertionError("kutu_cad_v4 parcasi birimsiz kaldi: "', 'raise AssertionError("kutu_cad_v5 parcasi birimsiz kaldi: "')
degis('"sac", "kutu_cad_v4.py", "hat/pack.html")', '"sac", "kutu_cad_v5.py", "hat/pack.html")')

# ================================================================ 8 · RAY EKLERİ + S MODÜLÜ + ALÇAK HAT SÖZLEŞMESİ (model kurulmadan ÖNCE) ================================================================
satir('birim("QR_DOLABI",', '''# ---- v57 · yeni üreteçlerin (kaide · ray ekleri · QR · tezgâh) malzemeleri — store_cad_v6 / kesme_cad_v4 / kutu_cad_v5'ten SONRA kaydedilir:
#      montajda önce olan ad kendi rengini korur (ortak adlar: plastik · sensor · poset — önce kaydedilince dolap / E / K parçalarının rengi değişiyordu, inceleme)
for _M in (KD, RE, QR, TZ):
    for _k, _v in _M.MALZEME.items():
        MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=_v.get("saydam", False)))
# ---- v57 · RAY EKLERİ (ray_ek_cad_v1, modül "-"): zincir oluğu · enerji zinciri (yalnız robot x 2650 için modellendi → animasyonda SABİT) · robot kablosu 4 + 11 m · zemin kanalı ----
RE.kur()
_dis_birim(RE, "GERCEK_RAY", "ray_ek_cad_v1.py", "hat/robot.html")
# ---- v57 · MODÜL S · SERVİS / TESLİM (koridorun karşısında): QR teslim dolabı (qr_cad_v1) + personel tezgâhı (tezgah_cad_v1) ----
# pafta v7 QR yer tutucusu (x 4295–5300, z 900–1340) ve F dolabındaki robot kontrol / ana pano / UPS / temizlik kalktı → hepsi burada.
# DİKKAT (denetçi): QR.X0/Y0/Z0 DEĞİŞTİRİLMEZ — ray_ek_cad_v1 kablo yolunu import anında onlardan hesaplıyor.
QR.kur()
_dis_birim(QR, "GERCEK_QR", "qr_cad_v1.py", "hat/service.html")
TZ.kur()
_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v1.py", "hat/service.html")
GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD}      # dünya koordinatlı yeni üreteçler (bulasik_cad_v1 sözleşmesi)

# ---- v57 · YOLCULUK SEÇİMLERİ (store_cad_v6 ve qr_cad_v1'de VAR olmalı — aşağıda denetlenir) ----
YOL_CEKMECE = "CEK_K3_hamur_3"                                                           # FR5'in hamur topunu aldığı çekmece (K3 pide · açıklık 398,5–473,5)
ISTASYON_SIRA = ("CEK_K3_hamur_3", "CEK_K1_lahm_4", "CEK_K6_ic1_1", "CEK_K5_tatli_1")     # modul_B döngüsü: K3 pide · K1 lahmacun · K6 içecek · K5 tatlı
QR_SUTUN, QR_SATIR = 0, 2                                                                # yolculuğun gözü: sütun 1 (x 4600–4980) · satır 3 (taban 850)
QR_PAY = 20.0                                                                            # çatal çekişi sonunda kutunun QR robot yüzüne payı (mm)
QR_YOL = {}                                                                              # yolculuk() doldurur: kutunun QR yolu + kapak açıklığı (__main__'de GÖZ YOLU denetimi)


def qr_hedef(sutun=None, satir=None):
    """v57 · kutunun QR gözündeki hedefi (dünya) — qr_cad_v1 parçalarından ÖLÇÜLÜR (v56'daki sabit 1215 ve pafta v7 QR kutusu kalktı).
    x: robot kapağının ortası (kapak motoru ağzın sol üst köşesinde → göz ortasından sağda) · y: göz tabanı (alüminyum ısı yayıcı) üstü ·
    z: kutu göz arkasına 5 mm kala (qr_cad_v1 'kapak kapanırken kutuya çarpmaz' denetimiyle aynı VARSAYIM) · kutunun çataldaki yeri kutu_cad_v5'ten (catal_kutu)."""
    sutun = QR_SUTUN if sutun is None else sutun; satir = QR_SATIR if satir is None else satir
    g_ = "%d%d" % (satir, sutun)
    def _bb(ad):
        q_ = [p for p in QR.PARCALAR if p["ad"] == ad]
        assert len(q_) == 1, "qr_cad_v1: %s yok" % ad
        return QR.dunya(q_[0]).BoundingBox()
    kp, tp, ks = _bb("goz_%s_robot_kapagi" % g_), _bb("goz_%s_taban_plakasi" % g_), _bb("goz_%s_kasasi" % g_)
    xk, zk = (KC.BX1 - KC.BX0) / 2.0, (KC.BZ1 - KC.BZ0) / 2.0                          # kutu yarı ölçüleri (320 × 320)
    hk = max(KC.H_YAN, KC.H_ON, KC.H_ARKA)                                              # katlanmış kutunun yüksekliği (en yüksek duvar)
    ck = KC.catal_kutu(KC.Z_CATAL[3] + 1.0)                                             # çatal kaldırıp çektikten sonra kutunun ötelemesi (dy, dz) · kutu_cad_v5: dz 900
    cek_z = KC.ZB + ck[1]                                                                # çatal çekişi sonunda kutu ekseni (E'nin kendi kinematiği: 694)
    bekle_z = min(cek_z, QR.Z0 - QR_PAY - zk)                                           # v57: QR robot yüzü artık z 670 → kutu yüzün QR_PAY önünde bekler (gövdeye girmez)
    kx, ky, kz = (kp.xmin + kp.xmax) / 2.0, tp.ymax, ks.zmax - 1.0 - 5.0 - zk
    gk_ = "GOZ_%s_KAPAK" % g_
    pv = QR.MENTESE[gk_][0]
    R_ = math.hypot(QR.KAPAK_MIL_Y - 6.0, 5.0)                                          # robot kapağının süpürme yarıçapı (qr_cad_v1 denetimi)
    h_ = pv[1] - (ky + hk)
    zmin = pv[2] + math.sqrt(max(0.0, R_ ** 2 - h_ ** 2))                               # kapak kapanırken kutunun robot yüzü bundan geride olmalı
    return dict(sutun=sutun, satir=satir, grup=gk_, mentese=QR.MENTESE[gk_], robot_x=QR.ROBOT_X, kx=kx, ky=ky, kz=kz, yari=zk, hk=hk,
                kutu_x=(kx - xk, kx + xk), kapak_x=(kp.xmin, kp.xmax), zmin=zmin, goz_ust=ks.ymax, cek_z=cek_z, bekle_z=bekle_z,
                geri=bekle_z - cek_z, dx=kx - (X_E + (KC.BX0 + KC.BX1) / 2.0), dy=ky - (KC.TEPSI + ck[0]), dz=kz - bekle_z)


# ============================ v57 · ALÇAK HAT SÖZLEŞMESİ: üreteçler arası kot eşitlikleri (model KURULMADAN önce; biri tutmazsa durur) ============================
_bk0 = {b["kod"]: b for b in B}
_ms4 = [p for p in KS.PARCALAR if p["ad"] == "sartlandirici_MS4"]
assert len(_ms4) == 1, "kesme_cad_v4: sartlandirici_MS4 parcasi yok"
_ms4_ust = _ms4[0]["wp"].val().BoundingBox().ymax
_komp_alt = min(q["sh"].BoundingBox().ymin for q in TU.P if q["ad"].startswith("kompresor_")) + KOMP_KAY[1]
SOZLESME = [
    ("disk: FT.DISK_UST = IT.DISK_UST = Y_MEK + 108 = P = 1000", (FT.DISK_UST, IT.DISK_UST, Y_MEK + DISK_UST_Y, P, 1000.0)),
    ("v56 disk 1168 + DY = P", (1168.0 + DY, P)),
    ("firin bandi: FT.BANT_UST_HAT = KS.FIRIN_BANDI = BANT_UST = 998", (FT.BANT_UST_HAT, KS.FIRIN_BANDI, BANT_UST, 998.0)),
    ("K bandi: FT.K_BANT = KS.BANT = KC.PLAKA_K = PLAKA = 996", (FT.K_BANT, KS.BANT, KC.PLAKA_K, PLAKA, 996.0)),
    ("E tepsisi: KC.TEPSI = TEPSI_Y = 936", (KC.TEPSI, TEPSI_Y, 936.0)),
    ("K istasyon tabani: KS.H_B = Y_MEK = 892", (KS.H_B, Y_MEK, 892.0)),
    ("duz cizgi: SC.H_B = FT.YG0 = KD.Y_DUZ = Y_DUZ = 788", (SC.H_B, FT.YG0, KD.Y_DUZ, Y_DUZ, 788.0)),
    ("mekanizma tabani: KD.Y_MEK = Y_MEK = Y_DUZ + KD.KAIDE_H (104)", (KD.Y_MEK, Y_MEK, Y_DUZ + KD.KAIDE_H)),
    ("makine ustu: KS.H = KC.H = Y_MEK + TC.Y = H_MAK = 1862", (KS.H, KC.H, Y_MEK + TC.Y, H_MAK, 1862.0)),
    ("dolap: SC.W_B = W_B = 4000", (SC.W_B, W_B, 4000.0)),
    ("itici tavani: TU yalitim alti (YAL_Y0 + DY) = IT.TAVAN = 1109", (TU_YAL_Y0, IT.TAVAN, 1109.0)),
    ("alt taban: SC.Y_PLINT = KS.Y_PLINT = KC.Y_PLINT = 123", (SC.Y_PLINT, KS.Y_PLINT, KC.Y_PLINT, 123.0)),
    ("K>E penceresi: KS.E_PENCERE = KC.PENCERE (4 deger, en buyuk fark)", (max(abs(a_ - b_) for a_, b_ in zip(KS.E_PENCERE, KC.PENCERE)), 0.0)),
    ("F>K agzi: KS.URUN_GIRISI y (932-1072) firin bandini (998) icerir (1 = evet)", (float(KS.URUN_GIRISI[0] < BANT_UST < KS.URUN_GIRISI[1]), 1.0)),
    ("hava K dali: ANA_K48 ucu = MS4 ustu + 10 = 1702", (ANA_K48[-1][1], _ms4_ust + 10.0, 1702.0)),
    ("kompresor alti = firin ustu raf ustu = HAVA_KOMPRESOR y0 = 1348", (_komp_alt, FT.UST_RAF_Y[1], _bk0["HAVA_KOMPRESOR"]["y"][0], 1348.0)),
    ("pizza yedegi alti = firin ustu raf ustu", (_bk0["D_PIZZA_YEDEK_UST"]["y"][0], FT.UST_RAF_Y[1])),
    ("davlumbaz alti = firin kalkani 1315", (_bk0["D_DAVLUMBAZ"]["y"][0], FT.ISI_KALKANI_Y[0], 1315.0)),
    ("bulasik x: BM.X0 = KS.BULASIK_YER", (BM.X0, KS.BULASIK_YER[0], 4108.5)),
    ("bulasik y: BM.Y0 = KS.BULASIK_YER", (BM.Y0, KS.BULASIK_YER[1], 126.0)),
    ("bulasik z: BM.Z0 = KS.BULASIK_YER (denetci: -20)", (BM.Z0, KS.BULASIK_YER[2], -20.0)),
    ("robot rayi: QR.RZ = RE.RZ = pafta RZ = 360", (QR.RZ, RE.RZ, RZ, 360.0)),
    ("robot omzu: QR.OMUZ = pafta OMUZ = 970", (QR.OMUZ, OMUZ, 970.0)),
    ("robot erisimi: QR.ERISIM = pafta ERISIM = 779", (QR.ERISIM, ERISIM, 779.0)),
    ("S modulu sag ucu: QR.X0 + QR.W = HAT_W = 5430", (QR.X0 + QR.W, HAT_W, 5430.0)),
    ("E sarjoru: KC.SARJOR_ADET = 462", (float(KC.SARJOR_ADET), 462.0)),
    ("E icecek yedegi: KC.ICECEK_YEDEK kutu = 144", (float(KC.ICECEK_YEDEK["kutu"]), 144.0)),
]
print("ALCAK HAT SOZLESMESI (v57 · %d esitlik · DY %.0f · Y_DUZ %.0f · Y_MEK %.0f · H_MAK %.0f):" % (len(SOZLESME), DY, Y_DUZ, Y_MEK, H_MAK))
_soz_kal = []
for _ad, _v in SOZLESME:
    _ok = max(_v) - min(_v) < 0.01
    print("   %-72s %-34s %s" % (_ad, " = ".join("%g" % v_ for v_ in _v), _gk(_ok)))
    if not _ok: _soz_kal.append(_ad)
assert not _soz_kal, "v57 alcak hat sozlesmesi tutmuyor: %s" % _soz_kal
_cek_kod = {c[1] for c in SC.CEK}
_yok = [k_ for k_ in (YOL_CEKMECE,) + tuple(ISTASYON_SIRA) if k_ not in _cek_kod]
print("   yolculuk + istasyon cekmeceleri store_cad_v6'da (%s): %s" % (", ".join((YOL_CEKMECE,) + tuple(ISTASYON_SIRA)), _gk(not _yok)))
assert not _yok, "v57: store_cad_v6'da olmayan cekmece: %s" % _yok
# ---- KAPASİTE (SPEC · 2 gün kuralı): üreteçlerin kendi sayımından ----
_kap = {}
for _t, _n in SC_OZET.values():
    _kap[_t] = _kap.get(_t, 0) + _n
KAPASITE = [("pide (dolap K3 + K5)", _kap.get("hamur", 0), 160, "2 gun 160"), ("lahmacun (K1 + K2)", _kap.get("lahm", 0), 432, "2 gun 400"),
            ("icecek (dolap K6)", _kap.get("ic1", 0), 144, "2 gun 139"), ("tatli (K5 ust cekmece)", _kap.get("tatli", 0), 12, "2 gun 11"),
            ("icecek yedegi (E alti 6 koli)", KC.ICECEK_YEDEK["kutu"], 144, "dolap + yedek 288 · 4 gun 277"),
            ("pizza kutusu (E sarjoru)", KC.SARJOR_ADET, 462, "+ firin ustu %d = %d · kullanilabilir ≈ 432 + %d = %d (asansor somunu 935'te durur, v4'ten miras, karar Kemal'de)"
             % (PIZZA_UST_KUTU, 462 + PIZZA_UST_KUTU, PIZZA_UST_KUTU, 432 + PIZZA_UST_KUTU))]
print("KAPASITE (v57 · SPEC):")
for _ad, _v, _h, _not in KAPASITE:
    print("   %-32s %4d (beklenen %d · %s)  %s" % (_ad, _v, _h, _not, _gk(_v == _h)))
assert all(_v == _h for _a, _v, _h, _n in KAPASITE), "v57: kapasite SPEC ile tutmuyor"
# ---- QR ERİŞİM TABLOSU (qr_cad_v1.erisim_tablosu) + yolculuğun gözü ----
_et = QR.erisim_tablosu()
print("QR ERISIM (qr_cad_v1 · robot x %.0f · omuz y %.0f · ray ekseni z %.0f · robot yuzu z %.0f · pratik erisim %.0f · bilek = goz tabani + %.0f VARSAYIM):"
      % (QR.ROBOT_X, QR.OMUZ, QR.RZ, QR.Z0, QR.ERISIM, QR.BILEK_PAY))
for _r, _c, _gx, _by, _hy, _d in _et:
    print("   satir %d · sutun %d · x %.0f · goz tabani %.0f · bilek y %.0f · uzaklik %.1f · pay %.1f  %s" % (_r + 1, _c + 1, _gx, _by, _hy, _d, QR.ERISIM - _d, _gk(_d <= QR.ERISIM)))
assert all(e_[5] <= QR.ERISIM for e_ in _et), "v57: QR gozu robot erisiminin disinda"
_qh = qr_hedef()
_qok = (_qh["kapak_x"][0] <= _qh["kutu_x"][0] and _qh["kutu_x"][1] <= _qh["kapak_x"][1] and _qh["kz"] - _qh["yari"] >= _qh["zmin"]
        and _qh["ky"] + _qh["hk"] < _qh["goz_ust"] and _qh["bekle_z"] + _qh["yari"] <= QR.Z0 - QR_PAY + 0.01)
print("QR HEDEF GOZU (yolculuk): sutun %d · satir %d · kutu x %.1f-%.1f (robot kapagi %.1f-%.1f) · kutu alti %.1f (goz tabani ustu) · ustu %.1f < goz %.1f · kutu z %.1f…%.1f (robot yuzu ≥ %.1f: kapak kapanirken carpmaz) · robot x %.0f · kutu otelemesi dx %.1f dy %.1f dz %.1f  %s"
      % (_qh["sutun"] + 1, _qh["satir"] + 1, _qh["kutu_x"][0], _qh["kutu_x"][1], _qh["kapak_x"][0], _qh["kapak_x"][1], _qh["ky"], _qh["ky"] + _qh["hk"], _qh["goz_ust"],
         _qh["kz"] - _qh["yari"], _qh["kz"] + _qh["yari"], _qh["zmin"], _qh["robot_x"], _qh["dx"], _qh["dy"], _qh["dz"], _gk(_qok)))
print("   catal cekisi: kutu_cad_v5 kutuyu z %.0f'ye ceker (on yuzu %.0f > QR robot yuzu %.0f) → montaj %.0f mm geri alir: kutu %.0f…%.0f'de bekler (yuz %.0f − pay %.0f)"
      % (_qh["cek_z"], _qh["cek_z"] + _qh["yari"], QR.Z0, -_qh["geri"], _qh["bekle_z"] - _qh["yari"], _qh["bekle_z"] + _qh["yari"], QR.Z0, QR_PAY))
assert _qok, "v57: QR hedef gozu (kutu kapak agzina / goze sigmiyor ya da kapak kutuya carpar)"
print("   BILGI · QR goz tabani DUZ: catal disleri kutunun altinda kalir, cekilemez (qr_cad_v1 UYARI) — animasyonda kutu tabana oturtuldu; goz tabanina dis yuvasi / kaburga karari Kemal'de")''')

# ================================================================ 9 · ÇIPLAK KUTU listesi ================================================================
satir('CIPLAK_KUTU = (', 'CIPLAK_KUTU = ("A_KABIN", "TOPPING_MODUL", "B_KASA")                            # v57: F taban dolabı + süpürgeliği kalktı')

# ================================================================ 10 · YOLCULUK (ürün animasyonu) ================================================================
degis('TOPPING = makine_kodu_v2 sırası + topping_v2_hesap_v1 · K = kesme_cad_v1 · E = kutu_cad_v3 · B = store_cad_v5 stroku."""',
      'TOPPING = makine_kodu_v2 sırası + topping_v2_hesap_v1 · K = kesme_cad_v4 · E = kutu_cad_v5 · B = store_cad_v6 stroku · QR = qr_cad_v1 (göz robot kapağı).\n    v57 ALÇAK HAT: OY = Y_MEK 892 · transfer P + 47 · QR hedefi parçalardan ölçülür (qr_hedef) · enerji zinciri robot x 2650\'de SABİT."""')
satir('    OX, OY = X_BC, H_B', '    OX, OY = X_BC, Y_MEK                                              # v57: TC orijini = mekanizma tabanı 892 (v56: 1060)')
degis('_cb = [b for b in B if b["kod"] == "CEK_K1_hamur_3"][0]', '_cb = [b for b in B if b["kod"] == YOL_CEKMECE][0]                     # v57: K3 pide çekmecesi (store_cad_v6)')
degis('TOPY.git(4.2, 5.6, 1215.0)', 'TOPY.git(4.2, 5.6, P + 47.0)')
degis('TOPY.git(6.4, 6.9, H_B + 108.0 + TOP_H + 0.5, "ss")', 'TOPY.git(6.4, 6.9, P + TOP_H + 0.5, "ss")')
degis('(T0K + KC.Z_CATAL[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, QR teslim dolabına koyar.")]',
      '(T0K + KC.Z_CATAL[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, rayda QR dolabının önüne (x %.0f) gider." % QR.ROBOT_X)]')
blok('    QR_X = QRX[0] + 15.0 + 240.0;', '    T_J = math.ceil(T0K + 25.5)', '''    QH = qr_hedef()                                                                              # v57: yeni QR dolabı (qr_cad_v1) · göz yeri parçalardan ölçülür (v56 sabit 1215 kalktı)
    TAS = Iz(0.0); TAS.git(T0K + 17.5, T0K + 18.6, 1.0, "s2")                                    # v57: 1) kutu QR yüzünün önünde x + y'de göz ağzına hizalanır (ön yüzü 650'de, gövdeye girmez)
    TAS_Z = Iz(0.0); TAS_Z.git(T0K + 18.6, T0K + 19.9, 1.0, "s2")                                # v57: 2) sonra düz z'de açık kapak ağzından göze girer (açık kapağın altından)
    KAPAK_QR = Iz(0.0); KAPAK_QR.git(T0K + 16.8, T0K + 17.5, 1.0, "ss"); KAPAK_QR.git(T0K + 20.6, T0K + 21.3, 0.0, "ss")   # göz robot kapağı: kutu girmeden açılır, robot çekilince kapanır
    ROB.git(T0K + 17.5, T0K + 19.9, QH["robot_x"]); ROB.git(T0K + 20.5, T0K + 24.5, RX0)
    ADIM.append((T0K + 16.8, "QR DOLABI", "Çatal kutuyu QR robot yüzünün %.0f mm önüne kadar çeker; göz (sütun %d · satır %d, taban %.0f) robot kapağı içeri-yukarı açılır; FR5 x %.0f'de durup kutuyu kapak ağzından göze koyar (göz arkasına 5 mm kala); robot çekilince kapak kapanır, müşteri kendi tarafındaki kapıdan QR ile alır. Enerji zinciri modelde robot x %.0f konumunda sabit (animasyonda hareket etmez)."
                 % (QR_PAY, QH["sutun"] + 1, QH["satir"] + 1, QR.GOZ_TABAN[QH["satir"]], QH["robot_x"], RE.RX_MONTAJ)))
''')
degis('tas = lambda t: ((QR_X - (X_E + 260.0)) * TAS(t), QR_DY * TAS(t), QR_DZ * TAS(t))',
      'tas = lambda t: (QH["dx"] * TAS(t), QH["dy"] * TAS(t), QH["geri"] * KC.ss(KC.Z_CATAL[2], KC.Z_CATAL[3], te(t)) + QH["dz"] * TAS_Z(t))   # v57: çatal çekişi QR yüzünün önünde biter (geri) · sonra kutu E\'den QR gözüne' + NL +
      '    QR_YOL.update(t=(T0K + KC.Z_CATAL[2], T0K + 21.3), kapak=KAPAK_QR, kutu=lambda t: (X_E + (KC.BX0 + KC.BX1) / 2.0 + tas(t)[0], KC.TEPSI + KC.catal_kutu(te(t))[0] + tas(t)[1], KC.ZB + KC.catal_kutu(te(t))[1] + tas(t)[2]))   # v57: kutu tabanı ortası (dünya) · GÖZ YOLU denetimi')
once('    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):', '''    # v57 · QR gözünün ROBOT KAPAĞI (qr_cad_v1 · QR.MENTESE): kendi mil ekseninde duran düğüm (ağ pivota göre yerel) · kutu girerken açık
    _gq = QH["grup"]; _pq, _axq, _acq = QH["mentese"]
    ton = {}
    for a_, m_, mal_ in parcalar:
        if a_.startswith("QR_GOZLER__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == _gq:
            y_ = Mesh(); y_.P = [(q[0] - _pq[0] * MM, q[1] - _pq[1] * MM, q[2] - _pq[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
            ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
    assert ton, "v57: QR gozu %s robot kapagi dugumu bulunamadi" % _gq
    _fTq = lambda t: tuple(c * MM for c in _pq)
    _fRq = lambda t: qax(_axq, _acq * KAPAK_QR(t))
    OZEL_T.append(dict(ad="QR_DONER__" + _gq, ebeveyn=None, T=_fTq(0.0), tonlar=ton))
    kanal("QR_DONER__" + _gq, _fTq)
    kanal("QR_DONER__" + _gq, _fRq, "rotation")
    KONTROL.append(("QR_DONER__" + _gq, _fTq, _fRq, ton))
''')
degis('if a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE"):', 'if a_.startswith(YOL_CEKMECE + "__") and a_.endswith("__CEKMECE"):')
degis('elif a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE_ARA"):', 'elif a_.startswith(YOL_CEKMECE + "__") and a_.endswith("__CEKMECE_ARA"):')

# ================================================================ 11 · GEOMETRİ DÖNGÜSÜ (bulaşık kodu · yeni durumlar) ================================================================
degis('            ps = [p for p in BM.PARCALAR if p["birim"] == b["kod"]]', '            ps = [p for p in BM.PARCALAR if p["birim"] == BM_KOD.get(b["kod"], b["kod"])]   # v57: K_BULASIK ← bulasik_cad_v1 "D_BULASIK"')
once('        elif b["durum"] == "GERCEK":', '''        elif b["durum"] in GERCEK_DIS:                                                       # v57: QR dolabı · tezgâh · ray ekleri · kaide (dünya koordinatı, bulaşık dalı gibi)
            M_ = GERCEK_DIS[b["durum"]]
            ps = [p for p in M_.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=M_.dunya(p))))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
''')

# ================================================================ 12 · DENETİMLER ================================================================
degis('tasan = [b["kod"] for b in B if b["modul"] != "-" and not', 'tasan = [b["kod"] for b in B if b["modul"] not in ("-", "S") and not')
degis('v51: F firin birimleri z +%.0f cikintiya kadar)"', 'v51: F firin birimleri z +%.0f cikintiya kadar; v57: S modulu + R haric — QR 2050 yuksek, koridorun karsisinda)"')
blok('    # ---- v36 · B CEKMECE MODULU ----', '    _ZON = ("HAVA_KOMPRESOR",)', '''    # ---- v36 · B CEKMECE MODULU (v57: store_cad_v6 · tek parça 0–4000 × 123–788) ----
    _bs = [b for b in B if b["durum"] == "GERCEK_STORE"]
    print("B CEKMECE MODULU (store_cad_v6 · alt taban %.0f · ust %.0f · x 0-%.0f · tam kaplama kapaklar): %d birim · %d parca · %d cekmece" % (Y_ALT, Y_DUZ, W_B, len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))
    _bust = max(b["y"][1] for b in _bs)
    print("   B birimleri ustu <= %.0f (en yuksek %.2f): %s" % (Y_DUZ, _bust, _gk(_bust <= Y_DUZ + 0.01)))
    assert all(b["y"][1] <= Y_DUZ + 0.01 for b in _bs), "B tavani %.0f'i asiyor" % Y_DUZ
    # ---- v35 · SUREC KOTU + TABAN HIZASI + CAKISMA (v57: Y_MEK 892 · Y_DUZ 788) ----
    _pp = {p["ad"]: p for p in TC.PARCALAR}
    _cd = _pp["calisma_diski"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()
    print("SUREC KOTU (CAD'den olculdu): disk ustu %.1f · firin bandi %.1f · kesme plakasi %.1f · kutu tepsisi %.1f · tabla ekseni z %.0f"
          % (Y_MEK + _cd.ymax, Y_MEK + _bt.ymax, PLAKA, TEPSI_Y, ZT))
    assert abs(Y_MEK + _cd.ymax - P) < 0.05, "disk ustu %.2f, beklenen %.2f" % (Y_MEK + _cd.ymax, P)
    assert abs(Y_MEK + _bt.ymax - BANT_UST) < 0.05, "bant ustu %.2f, beklenen %.2f" % (Y_MEK + _bt.ymax, BANT_UST)
    assert P > BANT_UST > PLAKA > TEPSI_Y, "urun yukari basamaga carpar"
    _bk = {b["kod"]: b for b in B}
    _kot = [("A_KABIN tabani (dolap ustu)", _bk["A_KABIN"]["y"][0], Y_DUZ), ("TOPPING_MODUL tabani (TC orijini)", _bk["TOPPING_MODUL"]["y"][0], Y_MEK),
            ("B_KASA ustu (duz cizgi)", _bk["B_KASA"]["y"][1], Y_DUZ), ("KAIDE_A alti", _bk["KAIDE_A"]["y"][0], Y_DUZ), ("KAIDE_C alti", _bk["KAIDE_C"]["y"][0], Y_DUZ),
            ("KAIDE_C ustu (mekanizma tabani)", _bk["KAIDE_C"]["y"][1], Y_MEK), ("F_TP10_GOVDE alti (firin dolabin ustunde)", _bk["F_TP10_GOVDE"]["y"][0], Y_DUZ),
            ("E_GOVDE alti (tek parca)", _bk["E_GOVDE"]["y"][0], 0.0), ("E_GOVDE ustu", _bk["E_GOVDE"]["y"][1], H_MAK), ("TOPPING_MODUL ustu", _bk["TOPPING_MODUL"]["y"][1], H_MAK)]
    print("TABAN HIZASI (v57 alcak hat):")
    for ad_, v_, h_ in _kot:
        print("   %-46s %8.2f = %6.0f  %s" % (ad_, v_, h_, _gk(abs(v_ - h_) < 0.01)))
    assert all(abs(v_ - h_) < 0.01 for _a, v_, h_ in _kot), "v57: taban hizasi tutmuyor"
    # v40 · ALT TABAN ÇİZGİSİ: B, K ve E üreteçleri kendi ölçümünü assert ediyor (gövde altı); burada üçünün AYNI çizgide olduğu (v57: F dolabı yok)
    assert abs(SC.Y_PLINT - Y_ALT) < 0.01 and abs(KC.Y_PLINT - Y_ALT) < 0.01, "B ve E alt taban cizgisi farkli: %.1f / %.1f" % (SC.Y_PLINT, KC.Y_PLINT)
    assert abs(KS.Y_PLINT - Y_ALT) < 0.01 and abs(KS.H_B - Y_MEK) < 0.01, "K alt taban / istasyon tabani farkli"      # v45: K kendi denetimini yapar
    assert abs(KS.BANT - PLAKA) < 0.01, "K bandi %.1f · plaka %.1f" % (KS.BANT, PLAKA)
    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    _ge = min(p["wp"].val().BoundingBox().ymin for p in KC.PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "asansor_")))
    assert abs(_gb - Y_ALT) < 0.05 and abs(_ge - Y_ALT) < 0.05, "govde altlari: B %.1f · E %.1f" % (_gb, _ge)
    print("ALT TABAN CIZGISI (v40): B %.1f · E %.1f · K dolabi %.0f -> ayni cizgi %.0f · altlari ayak + supurgelik · v57: F taban dolabi YOK (firin dolabin ustunde) -> GECTI"
          % (_gb, _ge, KS.Y_PLINT, Y_ALT))
    print("E KUTU MODULU (kutu_cad_v5): %d birim · %d parca · %d mentese dugumu · genislik %.0f · hat %.0f"
          % (len([b for b in B if b["durum"] == "GERCEK_KUTU"]), sum(len(v) for v in E_PARCA.values()), len(OZEL), W_E, HAT_W))
    assert not [b for b in B if "KARTON KULE" in b["ad"].upper() or b["kod"].endswith("KUTU_YEDEK")], "yedek karton kutu hala var"   # v48: 'kutu yedeği' metni artık kompresör/davlumbaz adında geçiyor (fırın üstü raf) — eski karton kulesi yok
    print("TABAN HIZASI: tek duz cizgi %.0f (dolap ustu = A/C kabin = firin alti) · A/C mekanizma + K istasyon tabani %.0f (kaide %.0f) · disk %.0f · makine ustu %.0f · E tek parca 0-%.0f -> GECTI"
          % (Y_DUZ, Y_MEK, Y_MEK - Y_DUZ, P, H_MAK, H_MAK))
''')
degis('z_ = ((bb.xmin + X_BC, bb.xmax + X_BC), (bb.ymin + H_B, bb.ymax + H_B), (bb.zmin, bb.zmax))', 'z_ = ((bb.xmin + X_BC, bb.xmax + X_BC), (bb.ymin + Y_MEK, bb.ymax + Y_MEK), (bb.zmin, bb.zmax))')
satir('    _sira = ["CEK_K1_hamur_3"', '    _sira = list(ISTASYON_SIRA)                                                     # v57: store_cad_v6 çekmeceleri (K3 pide · K1 lahmacun · K6 içecek · K5 tatlı)')
degis('print("ANA MONTAJ ANIMASYONU (v56):', 'print("ANA MONTAJ ANIMASYONU (v57):')
degis('cq.Vector(X_BC + _d[0], H_B + _d[1], _d[2])', 'cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2])', n=2)
degis('cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, H_B, 0.0)', 'cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, Y_MEK, 0.0)')
degis('cq.Vector(X_BC + _xk - TC.XC_TABLA, H_B, 0.0)', 'cq.Vector(X_BC + _xk - TC.XC_TABLA, Y_MEK, 0.0)')
once('    # ---- v52 · ŞEFFAF İSTASYON YÜZEYLERİ', '''    # ================= v57 · ALÇAK HAT ARAYÜZ DENETİMLERİ (gerçek katı kesişimi > 1 mm³) =================
    def _kaynak_tek(sh):
        """compound içinde üst üste binen katılar (boru parçaları + dirsek küreleri) → tek katı (OCC kendi-kesişen argüman tuzağı · denetci_yeni_v1)"""
        ss_ = sh.Solids()
        if len(ss_) <= 1: return sh
        r_ = ss_[0]
        for x_ in ss_[1:]: r_ = r_.fuse(x_)
        return r_.clean()
    def _capraz(A_, B_, esik=1.0):
        A_ = [(a_, sa, sa.BoundingBox()) for a_, sa in A_]; B_ = [(c_, sc, sc.BoundingBox()) for c_, sc in B_]
        out = []
        for a_, sa, X_ in A_:
            for c_, sc, Y_ in B_:
                if X_.xmin < Y_.xmax and Y_.xmin < X_.xmax and X_.ymin < Y_.ymax and Y_.ymin < X_.ymax and X_.zmin < Y_.zmax and Y_.zmin < X_.zmax:
                    v_ = _hacim(sa, sc)
                    if v_ > esik or v_ < 0: out.append((round(v_, 1), a_, c_))
        return out
    _SCP = [("B:" + p["birim"] + ":" + p["ad"], _tek(p["wp"])) for p in SC.PARCALAR]
    _SCB = {a_: sb.BoundingBox() for a_, sb in _SCP}
    # 1 · FIRIN ↔ ÇEKMECELİ DOLAP: fırın dolabın düz üstüne (788) oturur, hiçbir dolap parçasına girmez
    _fir_alt = min(sa.BoundingBox().ymin for _a, sa in _F)
    _gov_alt = min(FT.dunya(p).BoundingBox().ymin for p in FT.PARCALAR if p["birim"] == "F_TP10_GOVDE")
    _dol_ust = max(bb_.ymax for bb_ in _SCB.values())
    _c1 = _capraz(_F, [(a_, sb) for a_, sb in _SCP if _SCB[a_].xmax > FT.X_F0 - 1.0 and _SCB[a_].ymax > Y_DUZ - 5.0])
    _ok1 = not _c1 and abs(_gov_alt - Y_DUZ) < 0.05 and _fir_alt >= Y_DUZ - 0.05 and abs(_dol_ust - Y_DUZ) < 0.05
    print("FIRIN ↔ CEKMECELI DOLAP (v57 · firin dolabin duz ustune oturur · %d firin × %d dolap parcasi, cekmeceler kapali): firin en alt %.2f · govde alti %.2f · dolap ustu %.2f (= %.0f) · kesisim %s  %s"
          % (len(_F), len(_SCP), _fir_alt, _gov_alt, _dol_ust, Y_DUZ, "YOK" if not _c1 else "%d BULGU" % len(_c1), _gk(_ok1)))
    for x_ in sorted(_c1, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert _ok1, "v57: firin ↔ cekmeceli dolap"
    print("   BILGI · robot copu klapesi ust kenari %.0f · firin cikintisi alti %.0f (z 0…+%.0f) → robot eli icin %.0f mm (denetci: robot tarafinda bakilacak)" % (SC.KLAPE_AC[3], FT.YG0, FT.ZS, FT.YG0 - SC.KLAPE_AC[3]))
    # 2 · KAİDE ↔ TOPPING (TC + açıcı + tabla aktarmada + TU) ve ↔ ÇEKMECELİ DOLAP
    _KDP = [("KAIDE:" + p["ad"], KD.dunya(p)) for p in KD.PARCALAR]
    _TCT = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]): continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = YARIK_V2 if p["ad"] == "cikis_yarigi_contasi" else p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        _TCT.append(("TOPPING:" + p["ad"], sh))
    for p in _TABLA:
        _TCT.append(("TOPPING(aktarmada):" + p["ad"], p["wp"].val().translate(cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, Y_MEK, 0.0))))
    _TUT = [("TOPPING2:" + q["ad"], q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))) for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
    _c2 = _capraz(_KDP, _TCT + _TUT)
    _c3 = _capraz(_KDP, [(a_, sb) for a_, sb in _SCP if _SCB[a_].ymax > Y_DUZ - 5.0 and _SCB[a_].xmin < X_BC + W_BC])
    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:"))
    _tu_alt = min(sh.BoundingBox().ymin for _a, sh in _TUT)
    _kdb = cq.Compound.makeCompound([sa for _a, sa in _KDP]).BoundingBox()
    _ok2 = not _c2 and not _c3 and _tc_alt >= Y_MEK - 0.05 and _tu_alt > Y_MEK and abs(_kdb.ymin - Y_DUZ) < 0.05
    print("KAIDE (kaide_cad_v1 · %d parca · y %.1f-%.1f) ↔ TOPPING (TC %d parca + tabla aktarmada, acici dahil + TU %d): %s · ↔ CEKMECELI DOLAP: %s · TC en alt %.2f ≥ %.0f · TU en alt %.2f  %s"
          % (len(_KDP), _kdb.ymin, _kdb.ymax, len(_TCT), len(_TUT), "YOK" if not _c2 else "%d BULGU" % len(_c2), "YOK" if not _c3 else "%d BULGU" % len(_c3), _tc_alt, Y_MEK, _tu_alt, _gk(_ok2)))
    for x_ in sorted(_c2 + _c3, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert _ok2, "v57: kaide ↔ TOPPING / dolap"
    # 3 · S MODÜLÜ (QR + tezgâh) + RAY EKLERİ ↔ birbiri + robot / ray birimleri (FR5 montaj konumunda)
    _QRP = [("QR:" + p["ad"], QR.dunya(p)) for p in QR.PARCALAR]
    _TZP = [("TEZGAH:" + p["ad"], TZ.dunya(p)) for p in TZ.PARCALAR]
    _REP = [("RAY_EK:" + p["ad"], _kaynak_tek(RE.dunya(p)) if p["ad"].startswith("robot_kablosu_") else RE.dunya(p)) for p in RE.PARCALAR]
    _ROB = [("KUTU:" + b["kod"], kutu_kat(b).val()) for b in B if b["kod"] in ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL")]
    _c4 = _capraz(_QRP, _TZP + _REP) + _capraz(_TZP, _REP) + _capraz(_QRP + _TZP + _REP, _ROB)
    print("S + RAY EKLERI (QR %d · tezgah %d · ray ekleri %d parca, robot kablosu birlesik) ↔ birbiri + robot/ray birimleri (FR5 x %.0f): %s  %s"
          % (len(_QRP), len(_TZP), len(_REP), RX, "YOK" if not _c4 else "%d BULGU" % len(_c4), _gk(not _c4)))
    for x_ in sorted(_c4, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert not _c4, "v57: QR / tezgah / ray ekleri cakisiyor"
    print("   BILGI · enerji zinciri yalniz robot x %.0f icin modellendi (U kol y 2-342): yolculukta SABIT · dik U zincir ↔ acik cekmeceler (K1 lahm 1-2 erisilemez, 5 cekmece yalniz soldan) ACIK KONU (denetci) — karar Kemal'de" % RE.RX_MONTAJ)
    # 4 · QR GÖZ YOLU: kutu (320 × 320 × en yüksek duvar) çatal çekişinden göze kadar 0,1 s adımla ↔ QR parçaları (göz kapağı animasyondaki açıklıkta)
    _qh = qr_hedef(); _gq = _qh["grup"]; _pv, _ax, _ac = _qh["mentese"]
    _QS = [(p["ad"], QR.dunya(p), p["grup"]) for p in QR.PARCALAR]
    _yol_c, _yol_n, t_ = [], 0, QR_YOL["t"][0]
    while t_ <= QR_YOL["t"][1] + 1e-9:
        cx_, cy_, cz_ = QR_YOL["kutu"](t_)
        kb_ = FT.kut(cx_ - _qh["yari"], cx_ + _qh["yari"], cy_, cy_ + _qh["hk"], cz_ - _qh["yari"], cz_ + _qh["yari"]).val()
        a_ = _ac * QR_YOL["kapak"](t_)
        for ad_, sh_, gr_ in _QS:
            if gr_ == _gq and abs(a_) > 1e-6: sh_ = sh_.rotate(cq.Vector(*_pv), cq.Vector(*_pv) + cq.Vector(*_ax), a_)
            if _bbk(kb_, sh_):
                v_ = _hacim(kb_, sh_)
                if v_ > 1.0 or v_ < 0: _yol_c.append((round(t_, 2), round(v_, 1), ad_))
        t_ += 0.1; _yol_n += 1
    _son = QR_YOL["kutu"](QR_YOL["t"][1])
    print("QR GOZ YOLU (kutu %.0f × %.0f × %.0f · %d an · catal cekisi → x/y hizalama → z ile goze · kapak animasyondaki aciklikta) ↔ QR parcalari: %s · son yer x %.1f · alt %.1f · z %.1f (hedef %.1f / %.1f / %.1f)  %s"
          % (2 * _qh["yari"], _qh["hk"], 2 * _qh["yari"], _yol_n, "YOK" if not _yol_c else "%d BULGU %s" % (len(_yol_c), _yol_c[:6]),
             _son[0], _son[1], _son[2], _qh["kx"], _qh["ky"], _qh["kz"], _gk(not _yol_c and abs(_son[0] - _qh["kx"]) < 0.05 and abs(_son[1] - _qh["ky"]) < 0.05 and abs(_son[2] - _qh["kz"]) < 0.05)))
    assert not _yol_c and abs(_son[0] - _qh["kx"]) < 0.05 and abs(_son[1] - _qh["ky"]) < 0.05 and abs(_son[2] - _qh["kz"]) < 0.05, "v57: kutu QR yolunda carpiyor / hedefe varmiyor"

''')
blok('    SEF_IST = (("A", X_A', '    SEF_AGIZ = {', '''    SEF_IST = (("A", X_A, X_A + W_A, Y_DUZ, H_MAK), ("C", X_BC, X_BC + W_BC, Y_DUZ, H_MAK), ("B", X_A, X_A + W_B, Y_ALT, Y_DUZ),
               ("D", X_D, X_D + W_D, Y_DUZ, H_MAK), ("K", X_K, X_K + W_K, Y_ALT, H_MAK), ("E", X_E, X_E + W_E, Y_ALT, H_MAK))   # v57 alçak hat · S (koridorda) paneli YOK
    _yk = tuple(FT.YARIK_V2[0][2:]); _ka = tuple(KS.URUN_GIRISI)                                            # v57: F→K ağzı kesme_cad_v4'ten (932–1072)
''')
degis('üst 2030 (B: 1060), alt 123 (A/C: 1060)', 'üst 1862 (B: 788), alt 123 (A/C/F: 788 · v57 alçak hat)')
degis('        yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, 0.0)))',
      '        if (m_, "alt") not in SEF_ATLA:                                                  # v57: SEF_ATLA artık alt paneli de atlar (F altı: fırın dolabın üstünde)' + NL +
      '            yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, 0.0)))')
degis('    SEF_ATLA = {("A", "sag"), ("C", "sol")}', '    SEF_ATLA = {("A", "sag"), ("C", "sol"), ("D", "alt")}   # v57: F altı paneli fırın gövdesinin altıyla (788) ve dolabın üst paneliyle çakışırdı')
degis('alt %.0f (A/C %.0f) · on YOK', 'alt %.0f (A/C/F %.0f; F alti yok: firin dolabin ustunde) · on YOK')
degis('% (len(SEF_IST), _sef_n, SEF_T, -DZ, H_MAK, H_B, Y_ALT, H_B))', '% (len(SEF_IST), _sef_n, SEF_T, -DZ, H_MAK, Y_DUZ, Y_ALT, Y_DUZ))')
degis('    _IST = ("ROBOT", "QR", "CEK_", "URUN__", "TOPPING_DONER__KONI")', '    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "CEK_", "URUN__", "TOPPING_DONER__KONI")   # v57: S modülü (QR + tezgâh) ve zemin kanalı koridorda')
degis('v51: FIRIN CIKINTISI +%.0f (x 2500-4000, y 956-1473, Kemal)" % FT.ZS)', 'v51: FIRIN CIKINTISI +%.0f (x 2500-4000, y %.0f-%.0f, Kemal) · v57: QR / TEZGAH / ZEMIN_KANALI / ROBOT koridorda" % (FT.ZS, FT.YG0, FT.YG1))')
blok('    # ---- v53 · BULAŞIK MAKİNESİ: gerçek parçalar', '    # ---- v54 · HAVA ANA HATTI', '''    # ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v1 · BM.X0/Y0/Z0 = KS.BULASIK_YER): gerçek parçalar ↔ K parçaları (deterjan + parlatıcı dahil) + robot çöp kovası · K iç zarfı ----
    _BMP = [(p["ad"], BM.dunya(p)) for p in BM.PARCALAR]
    _KSP = [("K:" + p["ad"], _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))) for p in KS.PARCALAR if p["grup"] not in K_HARIC_GRUP]
    _KOVA = [("B:" + p["ad"], _tek(p["wp"])) for p in SC.PARCALAR if p["birim"] == "B_COP"]
    _bm_cak = []
    for a_, sa in _BMP:
        for c_, sc in _KSP + _KOVA:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _bm_cak.append((round(v_, 1), a_, c_))
    _bmb = cq.Compound.makeCompound([sa for _a, sa in _BMP]).BoundingBox()
    _KIC = ((X_K + 1.5, X_K + W_K - 1.5), (126.0, Y_MEK - 3.0), (-DZ + 1.5, 0.5))      # K iç zarfı: yan saclar arası · K taban sacı üstü 126 … istasyon tabanı altı 889 · arka sacın önü … ön yüz
    # y alt sınırında 1 mm pay: silindirik ayar ayaklarının BoundingBox'ı gevşek (ölçülen 125,5; gerçek katı K alt sacı 123–126 ile çakışmıyor — çakışma denetimi ayrıca TEMİZ)
    _ic = (_KIC[0][0] <= _bmb.xmin and _bmb.xmax <= _KIC[0][1] and _KIC[1][0] - 1.0 <= _bmb.ymin and _bmb.ymax <= _KIC[1][1] and _KIC[2][0] <= _bmb.zmin and _bmb.zmax <= _KIC[2][1])
    _det = [c_ for c_, _s in _KSP if c_.startswith("K:deterjan_")]
    print("BULASIK MAKINESI K altinda (bulasik_cad_v1 · %d parca · yer %s) ↔ K parcalari (%d, deterjan/parlatici %d dahil) + robot cop kovasi (%d): %s · K ic zarfinda (x %.1f-%.1f · y %.1f-%.1f · z %.1f…%.1f ⊂ x %.1f-%.1f · y %.0f-%.0f · z %.1f…%.1f): %s  %s"
          % (len(_BMP), tuple(KS.BULASIK_YER), len(_KSP), len(_det), len(_KOVA), "TEMIZ" if not _bm_cak else "%d BULGU %s" % (len(_bm_cak), _bm_cak[:6]),
             _bmb.xmin, _bmb.xmax, _bmb.ymin, _bmb.ymax, _bmb.zmin, _bmb.zmax, _KIC[0][0], _KIC[0][1], _KIC[1][0], _KIC[1][1], _KIC[2][0], _KIC[2][1], "EVET" if _ic else "HAYIR", _gk(not _bm_cak and _ic)))
    assert not _bm_cak and _ic, "v57: bulasik makinesi K parcalarina / kovaya giriyor ya da K ic zarfindan tasiyor"
    _ap = FT.kut(BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, KS.BULASIK_ARKA_PAY[0], KS.BULASIK_ARKA_PAY[1]).val()
    _ap_k = sorted({c_ for c_, sc in _KSP if _bbk(_ap, sc) and _hacim(_ap, sc) > 1.0})
    print("   BILGI · MEIKO arka payi (z %.0f…%.0f, 25 mm) icinden gecen K parcalari: %s (beklenen: yalniz 2 dozaj hortumu, y ≤ 310)"
          % (KS.BULASIK_ARKA_PAY[0], KS.BULASIK_ARKA_PAY[1], ", ".join(_ap_k) if _ap_k else "YOK"))
''')
blok('    _kx, _ky, _kz = BM.kapi_acik_zarf()', '    print("hat_v56.glb · %d dugum', '''    _kx, _ky, _kz = BM.kapi_acik_zarf()
    _kap = FT.kut(_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1]).val()
    _kap_c = []
    for c_, sc in _KSP + _REP + _QRP + _TZP:
        if _bbk(_kap, sc):
            v_ = _hacim(_kap, sc)
            if v_ > 1.0 or v_ < 0: _kap_c.append((round(v_, 1), c_))
    print("BULASIK KAPAK ACIK ZARFI (x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f · K altinda) ↔ K parcalari + ray ekleri + QR + tezgah (gercek kati, bilgi): %s"
          % (_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1], "SERBEST [PASS]" if not _kap_c else "%d BULGU %s [FAIL]" % (len(_kap_c), _kap_c[:6])))
    for b in B:
        if b["kod"] in ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL"):
            _yz = b["y"][0] < _ky[1] and _ky[0] < b["y"][1] and b["z"][0] < _kz[1] and _kz[0] < b["z"][1]
            _gx = b["x"][1] - b["x"][0]
            print("KAPAK ACIK ZARFI (x %.0f-%.0f · y %.0f-%.0f · z %.0f…%.0f) ↔ %s (y %.0f-%.0f · z %.0f…%.0f): %s"
                  % (_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1], b["kod"], b["y"][0], b["y"][1], b["z"][0], b["z"][1],
                     ("KESISIR (y/z) → robot bu birimiyle x %.0f-%.0f arasindayken kapak ACILMAZ: servis modu kilidi" % (_kx[0] - _gx, _kx[1] + _gx)) if _yz else "SERBEST (robot her konumda)"))
''')
degis('çıkıntı 0…+79 (x 2500–4000, y 956–1473) ----', 'çıkıntı 0…+79 (x 2500–4000, y 788–1305 · v57) ----')
degis('    for mk in ("A", "B", "C", "D", "K", "E", "-"):', '    for mk in ("A", "B", "C", "D", "K", "E", "S", "-"):                                 # v57: + S (SERVİS / TESLİM)')

# ================================================================ 13 · durum.json 'pafta' metni + çıktı adları ================================================================
PAFTA = ("HAT v57 (27 Eyl) · ALCAK HAT (SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4, Kemal onayli): butun mekanizma 168 asagi · "
         "TEK DUZ CIZGI 788 = cekmeceli dolap ustu = A/C kabin tabani = firin alti (basamak yok) · A/C mekanizma tabani 892 (kaide 104, kaide_cad_v1) · disk 1000 · "
         "firin bandi 998 · K bandi 996 · E tepsisi 936 · makine ustu 1862 · B = store_cad_v6: tek parca cekmeceli dolap 0-4000 × 123-788, 24 cekmece "
         "(pide 160 · lahmacun 432 · icecek 144 · tatli 12), firin altinda PU 60 kalkan + tasiyici cerceve, robot copu seridi 3810-4000 (15 L kova + klape) · "
         "F taban dolabi KALKTI: firin (firin_tp10_cad_v7) dolabin ustune oturur · itici_cad_v4 · K = kesme_cad_v4 (taban 892) · K altinda BULASIK MAKINESI "
         "x 4108,5-4568,5 (on dikmelerin arasinda) + arkasinda deterjan/parlatici kanisterleri · E = kutu_cad_v5 (tepsi 936, sarjor 462 kutu; kullanilabilir ≈ 432) "
         "+ icecek yedegi 6 koli E altinda (144 + dolap 144 = 288 = 4 gun) · pizza kutusu 462 + firin ustu 320 = 782 · TOPPING TC yerel 892, TU dunyada bir kez −168 · "
         "hava hatti −168 (K dali MS4 1692 + 10) · YENI MODUL S (SERVIS / TESLIM): QR dolabi qr_cad_v1 860 × 520 × 2050 (12 goz 2 × 6, robot kontrol + ana pano + UPS "
         "+ kilit karti icinde) + personel tezgahi tezgah_cad_v1 · ray ekleri ray_ek_cad_v1 (zincir olugu, enerji zinciri robot x 2650'de sabit, robot kablosu 4 + 11 m, "
         "zemin kanali) · robot rayi z 360 · yolculuk: K3 pide cekmecesi → acici → TOPPING → firin → K → E → QR gozu (sutun 1 · satir 3, robot kapagi acilir/kapanir) · "
         "ACIK: QR goz tabani catal disi yuvasi, dik U enerji zinciri ↔ acik cekmeceler, tezgah onu 390, sarjor 432 kullanilabilir, soguk yuk hesabi")
assert '"' not in PAFTA and "\\" not in PAFTA
degis('pafta="HAT v56 (27 Eyl) ·', 'pafta="' + PAFTA + ' · v56:')
s = s.replace('hat_v56.glb', 'hat_v57.glb').replace('hat_v56.usdz', 'hat_v57.usdz').replace('"hat_v56"', '"hat_v57"')

# v57 son el: v51'de kalkan K giriş çiti animasyon adımlarında hâlâ geçiyordu (sitede adım düğmesi) — metin düzeltmesi, geometri aynı
degis('Çıkışta K bandı üstündeki 20° çit ürünü hat eksenine (−170) geri alır. ', 'Ürün düz −170 ekseninde K bandına geçer (v51: giriş çiti yok). ')
degis('"ÇİT + İTİCİ", "Bant ürünü 200 mm taşır, 20° çit 36 mm içeri kaydırır (kutu ekseni); itici ürünün üstünden geri gelip arkasına iner."', '"K BANDI + İTİCİ", "Bant ürünü 200 mm taşır; itici ürünün üstünden geri gelip arkasına iner ve ürünü kutuya sürer."')

# ================================================================ 14 · SON DENETİM (üretilen metin) ================================================================
_kod = s[s.index('\nimport importlib, io'):]                                   # docstring (tarihçe) hariç
_hb = re.findall(r"(?<![\w.\"])H_B(?![\w\"])", _kod)          # _g7["H_B"] (pafta sözlüğü, yalnız DY denetiminde) hariç
assert not _hb, "v57: ciplak H_B kaldi (%d) — Y_DUZ / Y_MEK olmali" % len(_hb)
for _eski in ("QRX", "QRZ", "QR_X", "QR_DY", "QR_DZ", "CEK_K1_hamur_3", "1215.0", "D_TABAN_KABIN", "D_SUPURGELIK_KABIN", "D_TEMIZLIK", "D_DETERJAN", "D_ROBOT_KONTROL",
              "D_ANA_PANO", "D_UPS", "D_ICECEK_YEDEK", "QR_DOLABI", "(1100.0, 1240.0"):
    assert _eski not in _kod, "v57: eski ad / sabit kaldi: %s" % _eski
for _eski in ("import store_cad_v5", "import kesme_cad_v3", "import kutu_cad_v4", "import firin_tp10_cad_v6", "import itici_cad_v3",
              '"store_cad_v5.py"', '"kesme_cad_v3.py"', '"kutu_cad_v4.py"', '"firin_tp10_cad_v6.py"', '"itici_cad_v3.py"', "hat_v56"):
    assert _eski not in s, "v57: eski uretec / cikti adi kaldi: %s" % _eski
for _yeni in ("import store_cad_v6 as SC", "import kesme_cad_v4 as KS", "import kutu_cad_v5 as KC", "import firin_tp10_cad_v7 as FT", "import itici_cad_v4 as IT",
              "import qr_cad_v1 as QR, tezgah_cad_v1 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v1 as KD", "hat_v57.glb", "hat_v57.usdz"):
    assert _yeni in s, "v57: eksik: %s" % _yeni
compile(s, "hat_montaj_v57.py", "exec")
io.open(os.path.join(U, "hat_montaj_v57.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v57.py yazildi · %d satir" % s.count(NL))
