# -*- coding: utf-8 -*-
"""firin_tp10_cad_v7 → firin_tp10_cad_v8 (27 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63.md §2.4 · keşif on_duzlem_v63/kesif_F.md).
FIRIN GÖVDESİ / ÖN YÜZÜ / ÜRÜN YOLU DEĞİŞMEZ (gövde kabuğu, bant, giriş bandı üstü, ölü plaka üstü, kotlar v7 ile birebir — __main__ parça parça karşılaştırır).
Değişenler:
  · Z_ON = ZS (+79) sabiti: fırın gövdesinin ön yüzü = bütün istasyon önlerinin dış yüzü (diğer üreteçler buradan okur) · KOORDİNAT metni düzeltildi.
  · f_arka_saci + F_ARKA_SAC birimi KALKTI → yerine firin_ust_kabin_cad_v1'in tek parça arka sacı (y 788–1862).
  · İÇ HAVADA PARÇALAR BAĞLANDI (denetim_temas_v1: v7'de 67 bileşen / 77 parça havadaydı):
      – bant üst kolu: 2 × 304 bant kızağı (y 990–992) raya oturur, bant şeritleri kızağa (şeritler raydan 2 mm yukarıdaydı, raylar bant dışında)
      – raylar: 5 + 5 ray braketi tünel kaplamasına (ön 2 mm · arka 1 mm boşluk kapanır)
      – ısıtıcılar: üstler tavana 1 mm askı lamasıyla, altlar raylara braketle (dayanaksızdı)
      – yataklar: ön yatak cepleri yatak ölçüsüne (36 × 32 × 30), yatak / redüktör delikleri Ø20,4 → Ø20 (rulman iç bileziği mile oturur)
      – çıkış tahrik grubu: redüktörden teknik bölme duvarına L konsol (duvarla 9,5 mm arası boştu)
      – giriş bandı: yan sac rulman yuvaları Ø8,4 → Ø8 · taşıyıcı sac U'ya döndü (bandın altına değer, bacakları yan saclara)
      – çıkış ölü plakası: dikey kanadı 944 → 940'a iner, kabuğun sağlam çıkış duvarına (x 3998,5) kaynaklı
      – giriş duvarının x 2564 yüzüne 1 mm 304 sac (taşyünü çıplaktı)
  · __main__: kontrol() listesi · ön düzlem · v7 ↔ v8 parça parça karşılaştırma · havada parça denetimi · GLB yalnız 'glb' argümanıyla (site klasörüne varsayılan yazım YOK).
28 Eyl DENETİM DÜZELTMESİ (on_duzlem_v63/rapor_F.md "DENETÇİ BULGULARI"):
  · #5 yataklar yapıya: ön yataklara flanş plakası + 2 lama kabuğun ön iç yüzüne (yalıtım cebi kabuğa kadar) · arka çıkış yatağına 2 lama teknik bölme duvarına
    (yataklar yalnız mil üzerinden bağlıydı) · denetim: yalıtım + miller hariç yataklar / redüktör / motor yine yapıya bağlı.
  · #6 bant kızağı uçları RULO_X ± 20 (± 10'da ruloya 0,59 mm; 400 °C'de kızak ≈ 9 mm uzar) · bir uç uzun delikli · denetim: kızak ↔ rulo ≥ 4 mm.
  · #4 fırın rafına KOMPRESÖR AÇIKLIĞI (x 3595–3991 · z −385…−75): kompresör tavası (firin_ust_kabin_cad_v1) buraya asılır, tank rafa değmez; raf üstü 1348 ve
    pizza bölgesi DEĞİŞMEDİ (denetim)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v7.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# ---- başlık ----
d('"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v7 (27 Eyl 2026): ALÇAK HAT',
  '"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v8 (27 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.4) — gövde, ön yüz, ürün yolu\n'
  'v7 ile BİREBİR; Z_ON = ZS (+79) sabiti; f_arka_saci + F_ARKA_SAC KALKTI (yerine firin_ust_kabin_cad_v1 tek parça arka sacı 788–1862); iç havada parçalar\n'
  'bağlandı (bant kızakları, ray / ısıtıcı braketleri, yatak cepleri ve delikleri yatak ölçüsüne, çıkış tahrik konsolu, giriş bandı yuvaları + taşıyıcı U,\n'
  'ölü plaka kanadı 940, giriş duvarı 1 mm sac). Önceki: firin_tp10_cad_v7.py (yama: yap_firin_tp10_v8.py)\n'
  'v7 (27 Eyl 2026): ALÇAK HAT')
d("KOORDİNAT: DÜNYA (hat). x hat boyu · y yerden · z 0 = ön yüz, −830 = arka. Fırın gövdesi z 0…−730, arkasında F arka sacı −830.",
  "KOORDİNAT: DÜNYA (hat). x hat boyu · y yerden · v8: ÖN DÜZLEM z = Z_ON = +79 (fırın gövdesinin ön yüzü = bütün istasyon önlerinin dış yüzü) · arka yüz −830.\n"
  "Gövde parçaları yerel z 0…−730 çizilir; ekle() KAYAN birimlerini +ZS (79) taşır → dünya +79…−651. Arkada üst kabinin tek parça arka sacı −830 (firin_ust_kabin_cad_v1).")

# ---- ön düzlem sabiti ----
d('KAYAN = ("F_TP10_GOVDE", "F_TP10_KONVEYOR", "F_GIRIS_BANDI", "F_CIKIS_PLAKA")',
  'Z_ON = ZS                                        # v8 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63): bütün ön panel / kapak dış yüzleri = fırın gövdesinin ön yüzü\n'
  'KAYAN = ("F_TP10_GOVDE", "F_TP10_KONVEYOR", "F_GIRIS_BANDI", "F_CIKIS_PLAKA")')

# ---- yatak cepleri + delikleri ----
d(".cut(kut(rx - 20.0, rx + 20.0, RULO_Y - 18.0, RULO_Y + 18.0, TUNEL_Z[1], -45.0))",
  ".cut(kut(rx - 18.0, rx + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -77.0, -1.5))   # v8: ön yatak cebi = yatak (36 × 32) + yatak konsolu, kabuğun ön iç yüzüne kadar (v7 40 × 36 × 34, 2 mm boştu)")
d(".cut(silz(x, RULO_Y, 10.2, -78.0, -46.0))", ".cut(silz(x, RULO_Y, 10.0, -78.0, -46.0))")          # ön yatak iç bileziği Ø20 = mil
d(".cut(silz(x, RULO_Y, 10.2, -521.0, -499.0))", ".cut(silz(x, RULO_Y, 10.0, -521.0, -499.0))")      # arka yatak
d(".cut(silz(RULO_X[1], RULO_Y, 10.2, -587.0, -520.0))", ".cut(silz(RULO_X[1], RULO_Y, 10.0, -587.0, -520.0))")   # delik milli redüktör

# ---- denetçi #4 · raf: kompresör tavası açıklığı (tank rafa değmez; tava firin_ust_kabin_cad_v1) ----
d("TAKOZ_XZ = tuple((x_, z_) for z_ in (-30.0, -408.0) for x_ in (X_F0 + 30.0, X_F0 + 390.0, XC_TP, X_F0 + 1110.0, X_F1 - 30.0))   # v6: 10 takoz, aralık 360\n",
  "TAKOZ_XZ = tuple((x_, z_) for z_ in (-30.0, -408.0) for x_ in (X_F0 + 30.0, X_F0 + 390.0, XC_TP, X_F0 + 1110.0, X_F1 - 30.0))   # v6: 10 takoz, aralık 360\n"
  "KOMP_ACIKLIK = (3595.0, X_F1 - 9.0, -385.0, -75.0)                  # v8 · denetçi #4: raf açıklığı x 3595–3991 · z −385…−75 (kompresör tavası asılır; takozlar dışında)\n")
d("        _raf = _raf.cut(sily(x, z, 3.3, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0))\n",
  "        _raf = _raf.cut(sily(x, z, 3.3, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0))\n"
  "    _raf = _raf.cut(kut(KOMP_ACIKLIK[0], KOMP_ACIKLIK[1], UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0, KOMP_ACIKLIK[2], KOMP_ACIKLIK[3]))   # v8: kompresör tavası açıklığı\n")
d("SAĞDA kompresör 25 kg = 76 kg · JUN-AIR ortam sınırı 40 °C [föy]\"))",
  "SAĞDA kompresör 25 kg = 76 kg · JUN-AIR ortam sınırı 40 °C [föy] · v8: kompresör altında açıklık 395 × 310 (kompresör tavası firin_ust_kabin_cad_v1 alttan flanşla asılır)\"))")

# ---- iç bağlantılar (firin() sonuna) ----
d('    ekle("tahrik_motoru", silx(RULO_Y, -553.0, 30.0, RULO_X[1] - 170.0, RULO_X[1] - 32.0), "motor", K, kaynak="VARSAYIM Ø60 × 138")\n',
  '    ekle("tahrik_motoru", silx(RULO_Y, -553.0, 30.0, RULO_X[1] - 170.0, RULO_X[1] - 32.0), "motor", K, kaynak="VARSAYIM Ø60 × 138")\n'
  '    # ---- v8 · İÇ HAVADA PARÇALAR BAĞLANIR (SPEC_on_duzlem_v63 §2.4 · denetim_temas_v1: v7\'de 67 bileşen / 77 parça havadaydı) ----\n'
  '    # (1) bant kızakları: tel örgü üst kolun iki kenarı 10 mm 304 kızağa oturur (y RAY üstü 990 … şerit altı 992), kızak rayın üstünde (v7: raylar bandın dışında, şeritler 2 mm havada)\n'
  '    #     x RULO_X ± 20 (denetçi #6: ± 10\'da ruloya 0,59 mm; 400 °C\'de kızak ≈ 9 mm uzar → uç rulonun dışında, çıkış ucu uzun delikli) · geçit içinden geçer\n'
  '    KX = (RULO_X[0] + 20.0, RULO_X[1] - 20.0)\n'
  '    ekle("bant_kizagi_on", kut(KX[0], KX[1], RAY_Y[1], BANT_UST_HAT - BANT_K, BANT_Z[1] - 10.0, -81.0), "paslanmaz", K, kaynak="VARSAYIM",\n'
  '         bom=("Bant kızağı 304 · 2 mm · L 1336", 2, "lazer + büküm", "v8: üst kol kenarları (10 mm) kızağa, kızak raya oturur · 400 °C (UHMW olmaz) · giriş ucu raya sabit, çıkış ucu uzun delikli (ısıl uzama ≈ 9 mm)"))\n'
  '    ekle("bant_kizagi_arka", kut(KX[0], KX[1], RAY_Y[1], BANT_UST_HAT - BANT_K, -484.0, BANT_Z[0] + 10.0), "paslanmaz", K, kaynak="VARSAYIM")\n'
  '    # (2) ray braketleri: ön ray (z −84…−81) → kaplama ön duvarı (−79) 2 mm · arka ray (−484…−481) → kaplama arka duvarı (−485) 1 mm · 5 + 5 adet (aralık 300)\n'
  '    for i, xb in enumerate((2700.0, 3000.0, 3300.0, 3600.0, 3900.0)):\n'
  '        ekle("tunel_ray_braketi_on_%d" % i, kut(xb - 10.0, xb + 10.0, RAY_Y[0], RAY_Y[0] + 15.0, -81.0, TUNEL_Z[1]), "paslanmaz", K, kaynak="VARSAYIM",\n'
  '             bom=("Ray braketi 304 · 20 × 15 (ön 2 mm · arka 1 mm ara parça, kaplamaya punta)", 10, "lazer", "v8: raylar kaplamaya bağlı") if i == 0 else None)\n'
  '        ekle("tunel_ray_braketi_arka_%d" % i, kut(xb - 10.0, xb + 10.0, RAY_Y[0], RAY_Y[0] + 15.0, TUNEL_Z[0], -484.0), "paslanmaz", K, kaynak="VARSAYIM")\n'
  '    # (3) ısıtıcı braketleri: üstler tavana 1 mm askı lamasıyla (2 şerit / ısıtıcı) · altlar bant kenarından (−92,5 / −473,5) raylara (−84 / −481) 8,5 / 7,5 mm lamayla\n'
  '    for i, (a, b) in enumerate(((X_TUN0 + 5.0, xm - 5.0), (xm + 5.0, X_TUN1 - 5.0))):\n'
  '        for j, (za_, zb_) in enumerate(((BANT_Z[0], BANT_Z[0] + 15.0), (BANT_Z[1] - 15.0, BANT_Z[1]))):\n'
  '            ekle("ust_isitici_askisi_%d_%d" % (i + 1, j), kut(a, b, TUN_Y[1] - 1.0, TUN_Y[1], za_, zb_), "paslanmaz", G, kaynak="VARSAYIM",\n'
  '                 bom=("Üst ısıtıcı askı laması 304 · 1 mm × 15", 4, "lazer", "v8: ısıtıcı tavan kaplamasına perçinli (1 mm boştu)") if i == 0 and j == 0 else None)\n'
  '        ekle("alt_isitici_braketi_%d_on" % (i + 1), kut(a, b, RULO_Y - 12.0, RULO_Y - 4.0, BANT_Z[1], -84.0), "paslanmaz", G, kaynak="VARSAYIM",\n'
  '             bom=("Alt ısıtıcı taşıyıcı laması 304 · 8 × 8,5 / 7,5", 4, "lazer", "v8: alt ısıtıcı raylara bağlı (bant kolları arasında dayanaksızdı)") if i == 0 else None)\n'
  '        ekle("alt_isitici_braketi_%d_arka" % (i + 1), kut(a, b, RULO_Y - 12.0, RULO_Y - 4.0, -481.0, BANT_Z[0]), "paslanmaz", G, kaynak="VARSAYIM")\n'
  '    # (4) çıkış tahrik grubu: redüktör üstünden teknik bölme duvarına L konsol 5 mm (redüktör tork kolu) — v7\'de grup duvardan 9,5 mm geride, hiçbir yere bağlı değildi\n'
  '    ekle("tahrik_konsolu", kut(RULO_X[1] - 30.0, RULO_X[1] + 24.0, RULO_Y + 35.0, RULO_Y + 40.0, -586.0, TUNEL_Z[0] - 5.5)\n'
  '         .union(kut(RULO_X[1] - 30.0, RULO_X[1] + 24.0, RULO_Y + 35.0, RULO_Y + 88.0, TUNEL_Z[0] - 10.5, TUNEL_Z[0] - 5.5)), "paslanmaz", K, kaynak="VARSAYIM",\n'
  '         bom=("Tahrik konsolu 304 · L 5 mm · 54 × 95 + 54 × 53", 1, "lazer + büküm", "v8: redüktör → teknik bölme duvarı (M6 × 4) · tork kolu"))\n'
  '    # (5) giriş duvarının ön odaya bakan x 2564 yüzü: 1 mm 304 sac (v7: taşyünü çıplaktı) · geçit (bant + rulo + ağız) açık\n'
  '    ekle("giris_duvari_saci", kut(X_DUV0 - 1.0, X_DUV0, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5)\n'
  '         .cut(kut(X_DUV0 - 2.0, X_DUV0 + 1.0, GECIT_Y[0], GECIT_Y[1], TUNEL_Z[0], TUNEL_Z[1])), "paslanmaz", G, kaynak="VARSAYIM (özel sipariş şartnamesine)",\n'
  '         bom=("Giriş duvarı kaplama sacı 304 · 1 mm", 1, "≈ 514 × 408 · geçit kesikli", "v8: ön oda tarafında yalıtımı örter (kabuk iç yüzlerine punta)"))\n'
  '    # (6) denetçi #5 · ön yataklar yapıya: flanş plakası 3 mm (yatak ön yüzü −47 … −44, Ø22 mil boşluğu) + 2 lama 3 × 32 kabuğun ön iç yüzüne (−44 … −1,5)\n'
  '    for ad_, x_ in (("giris", RULO_X[0]), ("cikis", RULO_X[1])):\n'
  '        _k = kut(x_ - 18.0, x_ + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -47.0, -44.0).cut(silz(x_, RULO_Y, 11.0, -48.0, -43.0))\n'
  '        for xa_ in (x_ - 18.0, x_ + 15.0):\n'
  '            _k = _k.union(kut(xa_, xa_ + 3.0, RULO_Y - 16.0, RULO_Y + 16.0, -44.0, -1.5))\n'
  '        ekle("on_yatak_konsolu_%s" % ad_, _k, "paslanmaz", K, kaynak="VARSAYIM",\n'
  '             bom=("Ön yatak konsolu 304 · flanş plakası 36 × 32 × 3 + 2 lama 3 × 32 × 42,5", 2, "lazer + kaynak", "denetçi #5: yatak kabuğun ön iç yüzüne (M5 × 2) · giriş konsolu x yönünde uzun delikli (gergi)") if ad_ == "giris" else None)\n'
  '    # (7) denetçi #5 · arka çıkış yatağı → teknik bölme duvarı: 2 lama 3 × 32 (yatak ön yüzü −500 … duvar arka yüzü −490,5) · redüktör + motor delik mil üstünde, tork kolu tahrik_konsolu\n'
  '    _k = kut(RULO_X[1] - 18.0, RULO_X[1] - 15.0, RULO_Y - 16.0, RULO_Y + 16.0, -500.0, TUNEL_Z[0] - 5.5).union(\n'
  '        kut(RULO_X[1] + 15.0, RULO_X[1] + 18.0, RULO_Y - 16.0, RULO_Y + 16.0, -500.0, TUNEL_Z[0] - 5.5))\n'
  '    ekle("arka_yatak_konsolu_cikis", _k, "paslanmaz", K, kaynak="VARSAYIM",\n'
  '         bom=("Arka çıkış yatağı konsolu 304 · 2 lama 3 × 32 × 9,5", 1, "lazer", "denetçi #5: yatak teknik bölme duvarına (M5 × 2) · yatak yalnız mile bağlıydı"))\n')

# ---- giriş bandı: rulman yuvaları + taşıyıcı sac ----
d(".cut(silz(XB, RY, 4.2, a - 1, b + 1)).cut(silz(XT, RY, 4.2, a - 1, b + 1))",
  ".cut(silz(XB, RY, 4.0, a - 1, b + 1)).cut(silz(XT, RY, 4.0, a - 1, b + 1))")   # v8: rulman yuvası Ø8 = mil (Ø8,4 boştu)
d('    ekle("giris_tasiyici_sac", kut(XB + 12.0, XT - 12.0, Y - BK - 4.0, Y - BK - 1.0, ZA + 5, ZB_ - 5), "sac", GB)\n',
  '    # v8: taşıyıcı sac U — üst yüzü bandın altına değer (996,5), bacakları iki yan sacın iç yüzüne (v7: 1 mm havada, uçları boş)\n'
  '    _tas = kut(XB + 12.0, XT - 12.0, Y - BK - 3.0, Y - BK, ZA - 5.0, ZB_ + 5.0)\n'
  '    for za_, zb_ in ((ZA - 5.0, ZA - 2.0), (ZB_ + 2.0, ZB_ + 5.0)):\n'
  '        _tas = _tas.union(kut(XB + 12.0, XT - 12.0, RY - 2.0, Y - BK - 3.0, za_, zb_))\n'
  '    ekle("giris_tasiyici_sac", _tas, "sac", GB, bom=("Giriş bandı taşıyıcı sacı 304 · 3 mm U", 1, "lazer + büküm", "v8: bandın altında, bacakları yan saclara vidalı"))\n')

# ---- ölü plaka kanadı ----
d(".union(kut(OLU_X[0], OLU_X[0] + 1.5, GECIT_Y[0] + 4.0, K_BANT - 1.0, ZA, ZB_))",
  ".union(kut(OLU_X[0], OLU_X[0] + 1.5, GECIT_Y[0], K_BANT - 1.0, ZA, ZB_))   # v8: kanat 944 → 940 (geçit tabanı): kabuğun sağlam çıkış duvarına (x 3998,5, y 940–944) kaynaklı")
d("# ---- 3.2 ÇIKIŞ ÖLÜ PLAKASI: fırın bandı ucu 3996 → K bandı 4020 · L: dikey kanadı kabuğun çıkış sacına kaynaklı ----",
  "# ---- 3.2 ÇIKIŞ ÖLÜ PLAKASI: fırın bandı ucu 3996 → K bandı 4020 · L: dikey kanadı kabuğun çıkış sacına kaynaklı (v8: kesiğin altındaki sağlam duvara) ----")

# ---- F arka sacı KALKAR ----
d('    # ---- 3.5 F ARKA SACI (istasyon = kapalı ürün) ----\n'
  '    ekle("f_arka_saci", kut(X_F0, X_F1, YG0, YG1 + 10.0, -830.0, -828.5), "sac", AS,\n'
  '         bom=("F arka sacı 1,5 mm", 1, "304", "%.0f–%.0f · hava ana hattı önünde kalır" % (YG0, YG1 + 10.0)))\n',
  '    # ---- 3.5 v8: F ARKA SACI KALKTI → firin_ust_kabin_cad_v1 "f_ust_arka_sac" (tek parça, y 788–1862, rakorlu + panjurlu) ----\n')
d('    ("F_ARKA_SAC", "F arka sacı (bizim) · 1,5 mm · %.0f–%.0f" % (YG0, YG1 + 10.0)),\n', '')
d("v5: 79 mm ÖNE — ön yüzün önünde çıkıntı 1500 × 517 × 79, F modülü 909 derin · v7 ALÇAK HAT: gövde %.0f–%.0f",
  "v5: 79 mm ÖNE — ön yüzü = ÖN DÜZLEM +79 (v8: bütün istasyon önleri buraya gelir), F modülü 909 derin · v7 ALÇAK HAT: gövde %.0f–%.0f")

# ---- GLB üretici adı ----
d('"generator": "AUTOKITCH firin_tp10_cad_v7"', '"generator": "AUTOKITCH firin_tp10_cad_v8"')

# ---- __main__ YENİ ----
_ana = '\nif __name__ == "__main__":\n'
assert s.count(_ana) == 1
s = s[:s.index(_ana)] + '''
def havada_denetimi(ps=None, yaz=True):
    """v8 · denetim_temas_v1 ile havada parça (zemin = gövde altı 788). Beyaz liste YOK."""
    import denetim_temas_v1 as DT
    ps = ps if ps is not None else PARCALAR
    r = DT.havada([(p["ad"], p["wp"]) for p in ps])
    if yaz:
        DT.yaz(r, en_cok=80, baslik="HAVADA PARCA DENETIMI · firin_tp10_cad_v8")
    return r


# v8 · v7 ↔ v8 parça parça karşılaştırma: bilerek değişen / silinen parçalar (başkası değişirse KALDI)
V8_DEGISEN = ("yalitim_tasyunu", "on_yatak_giris", "on_yatak_cikis", "arka_yatak_giris", "arka_yatak_cikis", "tahrik_reduktoru",
              "giris_yan_saci_0", "giris_yan_saci_1", "giris_tasiyici_sac", "cikis_olu_plakasi", "ust_raf")
V8_SILINEN = ("f_arka_saci",)


if __name__ == "__main__":
    import time, json
    import kaset_3d_v3 as K3
    t0 = time.time()
    ARG = sys.argv[1:]
    DEN = []

    def kontrol(ad, sart, deger=""):
        DEN.append((ad, bool(sart), deger)); print("  %-124s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))

    ps = kur(uyarla=True)
    gecersiz = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("TP10-UZUN v8 · %d parça (fırın %d + uyarlama %d)" % (len(ps), len([p for p in ps if p["birim"].startswith("F_TP10")]),
          len([p for p in ps if not p["birim"].startswith("F_TP10")])))
    print("DENETİM (firin_tp10_cad_v8)")
    kontrol("katılar geçerli (%d parça)" % len(ps), not gecersiz, ", ".join(gecersiz))
    cak = kendi_arasinda(ps)
    for x_ in cak[:30]: print("   %10.1f mm3  %s  <->  %s" % x_)
    kontrol("FIRIN ÇAKIŞMA: kendi arasında gerçek katı kesişimi > 1 mm³ = 0 (TEMİZ)", not cak, "%d bulgu" % len(cak))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps if p["birim"].startswith("F_TP10")]).BoundingBox()
    print("ZARF (fırın): x %.0f…%.0f (%.0f) · y %.0f…%.0f · z %.0f…%.0f" % (bb.xmin, bb.xmax, bb.xlen, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("YERLEŞİM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f · rulolar %.0f / %.0f · aynı anda %d ürün (adım %.0f) · güç ≈%.1f kW (VARSAYIM)"
          % (X_F0, X_F1, X_F0, X_DUV0, X_DUV0, X_TUN0, X_TUN0, X_TUN1, ODA, X_TUN1, X_F1, BANT_X[0], BANT_X[1], RULO_X[0], RULO_X[1], N_URUN, ADIM, GUC))

    def _bbk(birim=None, ad=None):
        _s = [dunya(p) for p in ps if (birim is None or p["birim"] == birim) and (ad is None or p["ad"] == ad)]
        assert _s, (birim, ad)
        return cq.Compound.makeCompound(_s).BoundingBox()
    # ---- KOT (v7 ile aynı hedefler · f_arka_saci satırı kalktı) ----
    for _a, _v, _h in [("fırın gövdesi altı (F_TP10_GOVDE ymin)", _bbk("F_TP10_GOVDE").ymin, 788.0),
                       ("fırın gövdesi üstü (F_TP10_GOVDE ymax)", _bbk("F_TP10_GOVDE").ymax, 1305.0),
                       ("fırın bandı üstü (bant_ust_00 ymax)", _bbk(ad="bant_ust_00").ymax, 998.0),
                       ("giriş bandı üstü (giris_bandi ymax = fırın bandı)", _bbk(ad="giris_bandi").ymax, 998.0),
                       ("çıkış ölü plakası üstü (K bandı 996 + 1,5)", _bbk(ad="cikis_olu_plakasi").ymax, 997.5),
                       ("ışınım kalkanı altı (gövde üstü + 10)", _bbk(ad="isi_kalkani").ymin, 1315.0),
                       ("raf üstü (ust_raf ymax)", _bbk(ad="ust_raf").ymax, 1348.0),
                       ("F_UST_RAF birimi üstü", _bbk("F_UST_RAF").ymax, 1348.0)]:
        kontrol("KOT %-52s %8.2f · hedef %7.1f" % (_a, _v, _h), abs(_v - _h) < 0.01)
    _tb = (DISK_UST - 11.0, DISK_UST)
    _yk_ok = YARIK_V2[1][2] < _tb[0] and YARIK_V2[1][3] > _tb[1] and DISK_UST - 16.0 < _tb[0] and DISK_UST + 42.0 > _tb[1]
    kontrol("YARIK / AĞIZ: yarık açıklığı %.0f–%.0f · kabuk giriş ağzı %.0f–%.0f · tabla + disk %.0f–%.0f içinden geçer"
            % (YARIK_V2[1][2], YARIK_V2[1][3], DISK_UST - 16.0, DISK_UST + 42.0, _tb[0], _tb[1]), _yk_ok)
    _mb = _bbk(ad="giris_bandi_motoru")
    kontrol("GİRİŞ BANDI MOTORU y %.1f–%.1f · gövde %.0f–%.0f içinde" % (_mb.ymin, _mb.ymax, YG0, YG1), YG0 < _mb.ymin and _mb.ymax < YG1)
    # ---- v8 · ÖN DÜZLEM ----
    _kb = _bbk(ad="govde_kabugu")
    kontrol("ÖN DÜZLEM: Z_ON = ZS = %.1f · gövde kabuğu ön yüzü zmax %.2f = Z_ON · x %.1f–%.1f · y %.1f–%.1f (1500 × 517 düz yüz)" % (Z_ON, _kb.zmax, _kb.xmin, _kb.xmax, _kb.ymin, _kb.ymax),
            abs(Z_ON - 79.0) < 1e-9 and abs(_kb.zmax - Z_ON) < 0.01 and abs(_kb.xmin - X_F0) < 0.01 and abs(_kb.xmax - X_F1) < 0.01)
    _zmax = max(dunya(p).BoundingBox().zmax for p in ps); _zmin = min(dunya(p).BoundingBox().zmin for p in ps)
    kontrol("ÖN DÜZLEM: hiçbir fırın parçası +79'u geçmez (en ön %.2f) · arka ≥ −830 (en arka %.2f)" % (_zmax, _zmin), _zmax <= Z_ON + 0.01 and _zmin >= -830.0 - 0.01)
    kontrol("f_arka_saci / F_ARKA_SAC YOK (yerine firin_ust_kabin_cad_v1 f_ust_arka_sac)", not [p for p in ps if p["ad"] == "f_arka_saci" or p["birim"] == "F_ARKA_SAC"]
            and "F_ARKA_SAC" not in [k for k, _a in BIRIMLER])
    kontrol("BIRIMLER ↔ parçalar: her birimin parçası var, parçasız birim yok", all(any(p["birim"] == k for p in ps) for k, _a in BIRIMLER)
            and all(p["birim"] in [k for k, _a in BIRIMLER] for p in ps))
    # ---- v8 · v7 ↔ v8 PARÇA PARÇA ----
    import firin_tp10_cad_v7 as F7
    F7.kur(uyarla=True)
    A7 = {p["ad"]: F7.dunya(p) for p in F7.PARCALAR}; A8 = {p["ad"]: dunya(p) for p in ps}
    _deg = []
    for ad in sorted(set(A7) & set(A8)):
        b7, b8 = A7[ad].BoundingBox(), A8[ad].BoundingBox()
        fark = max(abs(a_ - b_) for a_, b_ in zip((b7.xmin, b7.xmax, b7.ymin, b7.ymax, b7.zmin, b7.zmax), (b8.xmin, b8.xmax, b8.ymin, b8.ymax, b8.zmin, b8.zmax)))
        if fark > 0.005 or abs(A7[ad].Volume() - A8[ad].Volume()) > 0.05:
            _deg.append(ad)
    _sil = sorted(set(A7) - set(A8)); _yeni = sorted(set(A8) - set(A7))
    print("   v7 → v8: ortak %d · DEĞİŞEN %d %s · SİLİNEN %s · YENİ %d %s" % (len(set(A7) & set(A8)), len(_deg), _deg, _sil, len(_yeni), _yeni))
    kontrol("v7 ↔ v8: değişen parçalar YALNIZ bilerek değişenler (%d) · gövde kabuğu, bant, giriş bandı, rulolar, raf, arka yüz BİREBİR" % len(V8_DEGISEN),
            sorted(_deg) == sorted(V8_DEGISEN), str(sorted(set(_deg) ^ set(V8_DEGISEN))))
    kontrol("v7 ↔ v8: silinen yalnız %s" % (V8_SILINEN,), _sil == sorted(V8_SILINEN), str(_sil))
    _uy = [a_ for a_ in ("govde_kabugu", "tunel_kaplamasi", "teknik_bolme_duvari", "giris_bandi", "bant_alt_kol", "rulo_giris", "rulo_cikis", "rulo_mili_giris",
                         "rulo_mili_cikis", "isi_kalkani", "on_ray", "arka_ray", "giris_bandi_motoru") if a_ in _deg]
    kontrol("FIRIN GÖVDESİ + ÜRÜN YOLU DEĞİŞMEDİ (kabuk, kaplama, bant, rulolar, giriş bandı, kalkan, raylar)", not _uy, str(_uy))
    # ---- denetçi #4 · raf: yalnız kompresör açıklığı ----
    _acik = (min(KOMP_ACIKLIK[1], X_F1 - 10.0) - KOMP_ACIKLIK[0]) * (UST_RAF_Y[1] - UST_RAF_Y[0]) * (KOMP_ACIKLIK[3] - KOMP_ACIKLIK[2])
    _pz = kut(2520.0, 3324.0, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0, -424.0, -20.0).val()
    _p7, _p8 = A7["ust_raf"].intersect(_pz).Volume(), A8["ust_raf"].intersect(_pz).Volume()
    _b8 = A8["ust_raf"].BoundingBox()
    kontrol("RAF (denetçi #4): v7 − v8 hacim %.0f = açıklık %.0f mm³ (x %.0f–%.0f · z %.0f…%.0f) · pizza bölgesi v7 %.0f = v8 %.0f · üst %.2f · takozlar açıklığın dışında"
            % (A7["ust_raf"].Volume() - A8["ust_raf"].Volume(), _acik, KOMP_ACIKLIK[0], KOMP_ACIKLIK[1], KOMP_ACIKLIK[2], KOMP_ACIKLIK[3], _p7, _p8, _b8.ymax),
            abs(A7["ust_raf"].Volume() - A8["ust_raf"].Volume() - _acik) < 1.0 and abs(_p7 - _p8) < 0.5 and abs(_b8.ymax - 1348.0) < 0.01
            and all(not (KOMP_ACIKLIK[0] - 8.0 < x_ < KOMP_ACIKLIK[1] + 8.0 and KOMP_ACIKLIK[2] - 8.0 < z_ < KOMP_ACIKLIK[3] + 8.0) for x_, z_ in TAKOZ_XZ))
    # ---- denetçi #6 · kızak ↔ rulo ----
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    _kr = min(_DSS(A8[k_].wrapped, A8[r_].wrapped).Value() for k_ in ("bant_kizagi_on", "bant_kizagi_arka") for r_ in ("rulo_giris", "rulo_cikis", "bant_sarimi_giris", "bant_sarimi_cikis"))
    _kb = A8["bant_kizagi_on"].BoundingBox()
    kontrol("KIZAK (denetçi #6): uçlar x %.0f / %.0f = RULO_X ± 20 · kızak ↔ rulo / sarım en yakın %.1f mm ≥ 4 (400 °C uzama payı)" % (_kb.xmin, _kb.xmax, _kr),
            _kr >= 4.0 and abs(_kb.xmin - RULO_X[0] - 20.0) < 0.01 and abs(_kb.xmax - RULO_X[1] + 20.0) < 0.01)
    # ---- v8 · HAVADA PARÇA ----
    hv = havada_denetimi(ps)
    kontrol("HAVADA PARÇA = 0 (v7: 67 bileşen / 77 parça) · beyaz liste YOK", not hv["bilesen"], "%d bileşen" % len(hv["bilesen"]))
    # ---- denetçi #5 · yatak gövdeleri yapıya bağlı mı (miller + taşyünü HARİÇ: zincir mil üzerinden kurulamasın) ----
    import denetim_temas_v1 as DT
    _hv2 = DT.havada([(p["ad"], p["wp"]) for p in ps if p["mal"] != "yalitim" and not p["ad"].startswith("rulo_mili_")])
    _tas = ("on_yatak_giris", "on_yatak_cikis", "arka_yatak_giris", "arka_yatak_cikis", "tahrik_reduktoru", "tahrik_motoru",
            "on_yatak_konsolu_giris", "on_yatak_konsolu_cikis", "arka_yatak_konsolu_cikis", "tahrik_konsolu")
    _yh = sorted(set(a_ for d_ in _hv2["bilesen"] for a_ in d_["uye"] if a_ in _tas))
    kontrol("YATAKLAR YAPIYA BAĞLI (denetçi #5): miller + taşyünü hariç tutulunca yatak / redüktör / motor / konsollar zemine bağlı · havadaki (mile asılı rulo, bant) %d bileşen"
            % len(_hv2["bilesen"]), not _yh, str(_yh))
    # ---- RAF YÜK HESABI (v6, değişmedi) ----
    _E, _nu, _ro, _g = 193e9, 0.29, 7930.0, 9.81
    _qk = 320 * 0.16 * _g / (0.804 * 0.404)
    for _t, _a, _ad in ((0.004, 0.378, "v6 4 mm · 10 takoz (açıklık 360 × 378)"),):
        _q = _qk + _ro * _g * _t; _D = _E * _t ** 3 / (12.0 * (1.0 - _nu ** 2)); _w = 0.00581 * _q * _a ** 4 / _D * 1000.0
        print("RAF SEHİM %s: yük %.0f Pa → iç panel %.2f mm · kenar ≈%.1f mm" % (_ad, _q, _w, 3.0 * _w))
    _top = 320 * 0.16 + 25.0 + 1.480 * 0.405 * 0.004 * _ro + 1.480 * 0.405 * 0.0008 * _ro
    print("RAF YÜKÜ: kutu 51,2 + kompresör 25 + raf %.1f + kalkan %.1f = %.0f kg → 10 takoz ort. %.1f kg" % (1.480 * 0.405 * 0.004 * _ro, 1.480 * 0.405 * 0.0008 * _ro, _top, _top / 10.0))
    for x in (2400, 2600, 3300, 3990, 4030, 4300):
        print("   ürün merkezi x %4d → z %.1f" % (x, urun_z(x)))
    if "glb" in ARG:                                                                 # v8: yalnız istenirse (site klasörüne varsayılan yazım YOK)
        ton = {}
        for p in ps:
            if not p["birim"].startswith("F_TP10"): continue
            ton.setdefault((p["mal"], p["birim"]), Mesh()).ekle(ag(cq.Workplane(obj=dunya(p).translate(cq.Vector(-XC_TP, -YG0, -ZS)))))
        parca = [("TP10U__%s__%s" % (b, m), msh, m) for (m, b), msh in sorted(ton.items())]
        for _a, msh, _m in parca:
            msh.P = [(-q[0], q[1], -q[2] - D_TP * MM) for q in msh.P]; msh.N = [(-n[0], n[1], -n[2]) for n in msh.N]
        yol = os.path.join(KOK, "otonom", "hat3d", "firin_tp10_v8.glb")
        b1 = glb_yaz(yol, parca)
        print("firin_tp10_v8.glb %.0f KB" % (b1 / 1024.0))
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM (firin_tp10_cad_v8): %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal, [d_[0] for d_ in kal]
    sys.stdout.flush(); os._exit(0)
'''

io.open(os.path.join(U, "firin_tp10_cad_v8.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v8.py yazıldı · %d satır" % s.count("\n"))
