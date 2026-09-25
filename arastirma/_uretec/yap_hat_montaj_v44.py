# -*- coding: utf-8 -*-
"""hat_montaj_v43 -> v44 : ALT KISIM v3 (Kemal 25 Eyl "bu şekilde en son halini tekrar modelle")
  · B = store_cad_v5 (tam kaplayan kapaklar · K1 5 pide + 2 lah + tatlı · K2 3 pide + 5 lah · K3 5 lah + 2 tek kat içecek ·
    K4 Secop + arkasında PLC + kaşar/sucuk deposu + 2 dar içecek)
  · F tabanı: önde bulaşık makinesi (MEIKO M-iClean US) + temizlik + pizza kutusu yedeği (553); arkada makine deterjanı +
    robot kontrol kutusu + ana pano + UPS (APC BX500CI)
  · K tabanı: önde içecek yedeği (5 koli, soğutmasız); arkada kompresör (JUN-AIR) + yağ kartuşu + K kartı · K üstü boşaldı
  · kompresör K tabanının önünden arkasına indi; Ø10 ana hat yeniden (K arkası → F arkası → TOPPING)
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v43.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v43 (25 Eyl 2026):', '"""v44 (25 Eyl 2026): ALT KISIM v3 — B store_cad_v5 (tam kaplayan kapaklar, içecek tek kat, K4 depo) · F/K tabanları yeniden · kompresör K tabanı arkasında.\nv43 (25 Eyl 2026):')
degis("ÇIKTI: otonom/hat3d/hat_v43.glb + .usdz", "ÇIKTI: otonom/hat3d/hat_v44.glb + .usdz")
degis("import store_cad_v4 as SC                                  # v40: alt taban 123 (v39: 3 elemanlı ray)",
      "import store_cad_v5 as SC                                  # v44: tam kaplayan kapaklar + alt kısım v3 dağılımı")
degis('''          "B_ELEKTRIK": "K1 üstü pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),''',
      '''          "B_ELEKTRIK": "K4 · Secop'un arkasında pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),''')
degis('''          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 3 roll-bond evaporatör + ebm-papst fan",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C (içerik VARSAYIM)",
          "B_TEMIZLIK": "K4 temizlik malzemesi nişi · kapaklı"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı"}''',
      '''          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 4 roll-bond evaporatör + ebm-papst fan",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C · 2 gün (GN 1/1-100 kaşar + GN 1/2-100 sucuk) · 4 günün 2. yarısı"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı", "ic1": "içecek · tek kat · yaylı itici",
           "ic1d": "içecek · tek kat (dar) · yaylı itici", "tatli": "tatlı · 5 şerit"}
_BIRIM_AD = {"hamur": "top", "lahm": "top", "icecek": "kutu", "ic1": "kutu", "ic1d": "kutu", "tatli": "kap"}''')
degis('''            _kol, _TIP_AD[_t], _kod.rsplit("_", 1)[1], _n, "kutu" if _t == "icecek" else "top", SC.STROK)''',
      '''            _kol, _TIP_AD[_t], _kod.rsplit("_", 1)[1], _n, _BIRIM_AD[_t], SC.STROK)''')
degis('''    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v4.py", "")''',
      '''    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v5.py", "")''')
# ---- F tabanı
a0 = s.index('birim("D_TABAN_KABIN"')
a1 = s.index('birim("D_FIRIN_GOVDE"')
s = s[:a0] + '''birim("D_TABAN_KABIN", "F taban dolabı 123–1060 · önde bulaşık + temizlik + pizza kutusu yedeği · arkada deterjan + robot kontrol + ana pano + UPS", "D", "KUTU", (X_D, X_D + W_D), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v44 alt kısım v3")
birim("D_SUPURGELIK_KABIN", "F taban dolabı · ayak + süpürgelik 0–123 (60 geride)", "D", "KUTU", (X_D + 30.0, X_D + W_D - 30.0), (0.0, Y_ALT), (-DZ + 30.0, -60.0), "kabin", "v40 alt taban çizgisi 123")
for kod_, ad_, (a_, b_), (y0_, y1_), (z0_, z1_), kat_, kay_ in (
        ("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US · 460 × 600 (V) × 700 · sepet 400 × 400 · giriş 315 · önde", (40.0, 500.0), (130.0, 830.0), (-620.0, -20.0), True, "meiko.com M-iClean U teknik veri · derinlik VARSAYIM"),
        ("D_TEMIZLIK", "Temizlik · 2 × 5 L bidon (deterjan / dezenfektan) + üstte bez · eldiven · poşet · önde", (510.0, 656.0), (130.0, 1045.0), (-210.0, -20.0), False, "B'nin K4 nişinden taşındı · bidon 130 × 190 × 290 VARSAYIM"),
        ("D_DETERJAN", "Makine deterjanı + parlatıcı 2 × 5 L · temizliğin arkasında · hortum bulaşık makinesine", (510.0, 656.0), (130.0, 730.0), (-410.0, -220.0), False, "VARSAYIM"),
        ("D_PIZZA_YEDEK", "Pizza kutusu yedeği · 553 kutu düz (804 × 404 × 885 + taban 15) · şarjör 567 + 553 = 1120 = 4 gün · önde", (666.0, 1470.0), (130.0, 1030.0), (-424.0, -20.0), False, "kutu 1,6 mm (kutu_cad_v3) · 1,8 mm olursa 517"),
        ("D_ROBOT_KONTROL", "Robot kontrol kutusu (FR5) · yer: UR sınıfı 475 × 423 × 268 · Fairino kompakt 245 × 180 × 89 · arkada", (666.0, 1141.0), (130.0, 553.0), (-702.0, -434.0), True, "VARSAYIM — Fairino'ya teyit"),
        ("D_ANA_PANO", "Ana pano · PLC · ana şalter · ekran yok (tablet) · arkada, robot kutusunun üstünde", (666.0, 1066.0), (565.0, 915.0), (-684.0, -434.0), False, "400 × 350 × 250 VARSAYIM"),
        ("D_UPS", "UPS APC Back-UPS BX500CI 500 VA · 115 × 213 × 185 · arkada", (1076.0, 1191.0), (565.0, 750.0), (-647.0, -434.0), True, "schneider-electric.com BX500CI")):
    birim(kod_, ad_, "D", "KATALOG" if kat_ else "KUTU", (X_D + a_, X_D + b_), (y0_, y1_), (z0_, z1_), "katalog" if kat_ else "kutu", kay_)
''' + s[a1:]
# ---- K tabanı
degis('''birim("K_TABAN_KABIN", "K taban dolabı 123–1060 · yedek kutu KALDIRILDI (Kemal 24 Eyl)", "K", "KUTU", (X_K, X_K + W_K), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v40 alt taban çizgisi 123")''',
      '''birim("K_TABAN_KABIN", "K taban dolabı 123–1060 · önde içecek yedeği · arkada kompresör + yağ + K kartı", "K", "KUTU", (X_K, X_K + W_K), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v44 alt kısım v3")''')
degis('''birim("K_YAG", "Yağ kartuşu 4 L × 2 · ısıtmalı", "K", "KUTU", (X_K + 60.0, X_K + 300.0), (140.0, 330.0), (-420.0, -20.0), "kutu", "pafta v7")
birim("K_KART", "K kontrol kartı · tahrik", "K", "KUTU", (X_K + 320.0, X_K + 540.0), (140.0, 330.0), (-220.0, -20.0), "kutu", "pafta v7")''',
      '''birim("K_ICECEK_YEDEK", "İçecek yedeği · soğutmasız · 5 koli × 24 = 120 kutu (soğuk 160 + 120 = 280 = 4 gün) · önde", "K", "KUTU", (X_K + 40.0, X_K + 440.0), (130.0, 745.0), (-287.0, -20.0), "kutu", "koli 400 × 267 × 123 VARSAYIM")
birim("K_YAG", "Yağ kartuşu 4 L × 2 · ısıtmalı · arkada, kompresörün üstünde", "K", "KUTU", (X_K + 40.0, X_K + 440.0), (650.0, 840.0), (-665.0, -425.0), "kutu", "pafta v7")
birim("K_KART", "K kontrol kartı · tahrik · arkada, yağın üstünde", "K", "KUTU", (X_K + 40.0, X_K + 260.0), (850.0, 1050.0), (-615.0, -425.0), "kutu", "pafta v7")''')
degis('''birim("K_ICECEK_YEDEK", "İçecek + tatlı yedeği · 4 gün (97 kutu 330 ml + 8 tatlı)", "K", "KUTU", (X_K + 33.0, X_K + W_K - 33.0), (PLAKA + 355.0, H_MAK - 2.0), (-800.0, -30.0), "kutu", "pafta v7")
''', '''# v44: K'nin üst bölmesi boşaldı (içecek yedeği K tabanının önüne indi)
''')
# ---- hava: kompresör K tabanının arkasına, ana hat yeniden
degis('''birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L) + Ø10 ana hat · K tabanı → F tabanı arkası → TOPPING", "K", "GERCEK_HAVA",''',
      '''birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · K tabanı ARKADA (130–640) + Ø10 ana hat · K arkası → F arkası → TOPPING", "K", "GERCEK_HAVA",''')
degis('''V3_HAVA = ("kompresor_", "hava_ana_hatti")''',
      '''V3_HAVA = ("kompresor_", "hava_ana_hatti")
KOMP_KAY = (-70.0, -390.0, -385.0)            # v44: kompresör K tabanının önünden (y 520–1030, z −40…−420) arkasına (130–640, −425…−805)
ANA_V44 = [(3530, 646, -765), (3530, 1040, -765), (3530, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]''')
degis('''            _hv = [q for q in TU.P if q["ad"].startswith(V3_HAVA)]
            for q in _hv:
                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))), False))''',
      '''            _hv = [q for q in TU.P if q["ad"].startswith("kompresor_")]
            for q in _hv:
                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=q["sh"].translate(cq.Vector(X_BC + KOMP_KAY[0], KOMP_KAY[1], KOMP_KAY[2]))), False))
            _ana = TU.boru(ANA_V44, 5.0)                                        # v44 · yeni güzergâh
            _ana = _ana.val() if hasattr(_ana, "val") else _ana
            ton.setdefault(("hava_ana", "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=_ana.translate(cq.Vector(X_BC, 0.0, 0.0))), False))''')
# ---- çıktılar
degis('''    print("B CEKMECE MODULU (store_cad_v4 · alt taban %.0f · 3 elemanli ray)''', '''    print("B CEKMECE MODULU (store_cad_v5 · alt taban %.0f · tam kaplama kapaklar)''')
degis('''    b1 = glb_yaz(os.path.join(OUT, "hat_v43.glb"), parcalar, dokular, anim=False)''', '''    b1 = glb_yaz(os.path.join(OUT, "hat_v44.glb"), parcalar, dokular, anim=False)''')
degis('''print("hat_v43.glb · %d birim''', '''print("hat_v44.glb · %d birim''')
degis('''usdz_yaz([os.path.join(OUT, "hat_v43.usdz")], "hat_v43",''', '''usdz_yaz([os.path.join(OUT, "hat_v44.usdz")], "hat_v44",''')
degis('''print("hat_v43.usdz · %.0f KB''', '''print("hat_v44.usdz · %.0f KB''')
degis('''· v43 · TOPPING v2 UNO'lu (topping_uno_cad_v4 · 3 mm raf) · kompresor K tabaninda · E = kutu_cad_v3 · B = store_cad_v4 ·''',
      '''· v44 · alt kisim v3 · B = store_cad_v5 (tam kaplama kapaklar) · kompresor K tabani arkasinda · TOPPING v2 UNO'lu (topping_uno_cad_v4) · E = kutu_cad_v3 ·''')
degis('    _ZON = ("D_FIRIN_GOVDE",)', '    _ZON = ("D_FIRIN_GOVDE", "HAVA_KOMPRESOR")')
degis('_sira = ["CEK_K1_hamur_3", "CEK_K2_lahm_4", "CEK_K3_icecek_1", "CEK_K3_lahm_2"]', '_sira = ["CEK_K1_hamur_3", "CEK_K2_lahm_4", "CEK_K3_ic1_1", "CEK_K4_ic1d_2"]')
io.open(os.path.join(U, "hat_montaj_v44.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v44.py yazildi")
