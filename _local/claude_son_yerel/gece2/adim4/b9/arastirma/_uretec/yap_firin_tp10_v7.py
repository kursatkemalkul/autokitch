# -*- coding: utf-8 -*-
"""firin_tp10_cad_v6 → firin_tp10_cad_v7 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57.md · resim ALCAK_HAT_RESIM1_v4, Kemal onaylı).
Fırının her şeyi 168 aşağı: BANT_UST_HAT 1166 → 998 → gövde 788–1305, raf üstü 1348, giriş bandı 998, çıkış plakası K bandı 996'ya.
v6'da BANT_UST_HAT'a bağlı OLMAYAN mutlak y sabitleri (tokenize taraması: 3–4 haneli bütün sayılar tek tek sınıflandı, y rolünde yalnız bunlar)
bağıl yapıldı:
  · GB_MOTOR y 1290            → BANT_UST_HAT + 124     (1122)
  · YARIK_V2 1145/1210 · 1155/1206 → DISK_UST −23/+42 · −13/+38   (DISK_UST = BANT_UST_HAT + 2 = 1000, yeni ad)
  · K_BANT 1164                → BANT_UST_HAT − 2       (996 = kesme_cad_v4 BANT)
  · giriş ağzı kesiği 1152–1210 → DISK_UST −16…+42      (984–1042)
  · plaka_ayagi 1220–1240      → motor y − 70 … − 50     (1052–1072)
Metinler (BOM · BIRIMLER · yorum) yeni kotlarla / biçimli yazıldı; F_UST_RAF birim metni v6 gerçeğine (4 mm, 10 takoz, 320 kutu) düzeltildi.
__main__: v7 KOT DENETİMİ (parçalardan ölçülür) eklendi; GLB/USDZ yeni adla (firin_tp10_v7). Ad, fonksiyon, birim, grup DEĞİŞMEDİ."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v6.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# ---- başlık ----
d('"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v6 (27 Eyl 2026): KUTU YEDEĞİ TEK YERDE',
  '"""AUTOKITCH · F FIRIN · TP10 KESİTİ · 1500 · v7 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57 · resim ALCAK_HAT_RESIM1_v4) — fırının HER ŞEYİ 168 aşağı:\n'
  'bant 1166 → 998 · gövde 788–1305 · raf üstü 1348 · çıkış plakası K bandı 996\'ya. v6\'nın mutlak y sabitleri (GB_MOTOR 1290, YARIK_V2, K_BANT 1164,\n'
  'giriş ağzı kesiği 1152–1210, plaka ayağı 1220–1240) artık BANT_UST_HAT / DISK_UST\'e bağlı; x, z, ölçüler, parça adları, birimler, gruplar v6 ile aynı.\n'
  'Önceki: firin_tp10_cad_v6.py\n'
  'v6 (27 Eyl 2026): KUTU YEDEĞİ TEK YERDE')

# ---- kot zinciri ----
d("BANT_UST_HAT = 1166.0                            # kot zinciri: disk 1168 → fırın bandı 1166 → K 1164",
  "BANT_UST_HAT = 998.0                             # v7 ALÇAK HAT (v6 1166 − 168) · kot zinciri: disk 1000 → fırın bandı 998 → K 996\n"
  "DISK_UST = BANT_UST_HAT + 2.0                    # 1000 · v7: TOPPING çalışma diski üstü (mekanizma tabanı 892 + 108) · TOPPING'e bakan kotlar buna bağlı")
d("# 956 gövde altı (F taban dolabının üstü)", "# 788 gövde altı (v7: çekmeceli dolabın üstü = düz çizgi 788)")
d("# 1473 gövde üstü", "# 1305 gövde üstü")
d("# 989 · 1263 tünel boşluğu", "# 821 · 1095 tünel boşluğu")
d("# 1166 · 1251 ağız", "# 998 · 1083 ağız")
d("RULO_Y = BANT_UST_HAT - BANT_K - RULO_R          # 1140", "RULO_Y = BANT_UST_HAT - BANT_K - RULO_R          # 972")
d("# 1114 · 1120", "# 946 · 952")
d("# 1108 · 1251 uç duvarı geçidi", "# 940 · 1083 uç duvarı geçidi")
d("# 1110 · 1158", "# 942 · 990")
d("# 1154,5 giriş bandı rulo ekseni", "# 986,5 giriş bandı rulo ekseni")

# ---- MUTLAK → BAĞIL 1: giriş bandı motoru ----
d("GB_MOTOR = (2530.0, 1290.0, -431.0)              # NEMA23 (mil yüzü z) · ağzın üstünde, ön odanın içinde",
  "GB_MOTOR = (2530.0, BANT_UST_HAT + 124.0, -431.0)   # 1122 (v6 1290) · NEMA23 (mil yüzü z) · ağzın üstünde, ön odanın içinde · v7: bant kotuna bağlı")
d("muafiyeti gizliyordu.)\n# v3: CEP YOK",
  "muafiyeti gizliyordu.)\n# v7: yukarıdaki ölçüler v6 kotlarıdır (TOPPING tabanı 1060); alçak hatta TOPPING ile fırın birlikte 168 aşağı → bağıl konum aynı.\n# v3: CEP YOK")
d("# 1512–1516 · fırın üstünde HAVALANDIRMALI raf", "# 1344–1348 · fırın üstünde HAVALANDIRMALI raf")
d("# 1483–1483,8 · 0,8 mm 304 ışınım kalkanı", "# 1315–1315,8 · 0,8 mm 304 ışınım kalkanı")

# ---- MUTLAK → BAĞIL 2: TOPPING çıkış yarığı çerçevesi (disk kotuna bağlı) ----
d("tabla 1157–1160 + disk 1160–1168 aktarmada x 2507'ye kadar geldiği için alt çıta 1155'in altında",
  "tabla 989–992 + disk 992–1000 (v6 1157–1168) aktarmada x 2507'ye kadar geldiği için alt çıta 987'nin altında · v7: y'ler DISK_UST'e bağlı (dış −23…+42 · açıklık −13…+38)")
d("YARIK_V2 = ((2492.0, 2498.5, 1145.0, 1210.0, -417.0, -5.0), (2491.0, 2499.5, 1155.0, 1206.0, -409.0, -13.0))",
  "YARIK_V2 = ((2492.0, 2498.5, DISK_UST - 23.0, DISK_UST + 42.0, -417.0, -5.0), (2491.0, 2499.5, DISK_UST - 13.0, DISK_UST + 38.0, -409.0, -13.0))")

# ---- MUTLAK → BAĞIL 3: K bandı ----
d("K_BANT, K_BANT_Z = 1164.0, (-412.0, -12.0)       # kesme_cad_v1: K bandı üstü · genişlik 400",
  "K_BANT, K_BANT_Z = BANT_UST_HAT - 2.0, (-412.0, -12.0)   # 996 (v6 1164) · K bandı üstü = kesme_cad_v4 BANT (kot zinciri: fırın bandı − 2) · genişlik 400")

# ---- MUTLAK → BAĞIL 4: kabuğun giriş ağzı kesiği ----
d("kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, 1152.0, 1210.0, -341.0 - ZS, -10.0 - ZS))",
  "kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, DISK_UST - 16.0, DISK_UST + 42.0, -341.0 - ZS, -10.0 - ZS))   # v7: 984–1042 (disk −16…+42; v6 1152–1210)")

# ---- MUTLAK → BAĞIL 5: motor plakası ayağı ----
d('ekle("plaka_ayagi", kut(2526.0, 2534.0, 1220.0, 1240.0, TUNEL_Z[0] - 4.0, MZF), "sac", GB)',
  'ekle("plaka_ayagi", kut(2526.0, 2534.0, MY - 70.0, MY - 50.0, TUNEL_Z[0] - 4.0, MZF), "sac", GB)   # v7: motor kotuna bağlı (1052–1072; v6 1220–1240)')

# ---- BOM metinleri (biçimli) ----
d('"381 × 1428 uçtan uca (özel boy)", "üstü 1166 · uçları gövde içinde") if j == 0 else None)',
  '"381 × 1428 uçtan uca (özel boy)", "üstü %.0f · uçları gövde içinde" % BANT_UST_HAT) if j == 0 else None)')
d('"üst yüz 1166 = fırın bandı · ekseni −249 (fırındaki ürün ekseni)"))',
  '"üst yüz %.0f = fırın bandı · ekseni dünyada −170 (fırındaki ürün ekseni; yerel −249 + 79)" % BANT_UST_HAT))')
d('"üstü 1165,5: fırın bandı 1166 → K bandı 1164"))',
  '"üstü %s: fırın bandı %.0f → K bandı %.0f" % (("%.1f" % (K_BANT + 1.5)).replace(".", ","), BANT_UST_HAT, K_BANT)))')
d('"956–1483 · hava ana hattı önünde kalır"))',
  '"%.0f–%.0f · hava ana hattı önünde kalır" % (YG0, YG1 + 10.0)))')

# ---- BIRIMLER ----
d('F modülü 909 derin"),',
  'F modülü 909 derin · v7 ALÇAK HAT: gövde %.0f–%.0f" % (YG0, YG1)),')
d('uçtan uca · üstü 1166 · rulolar uç duvarlarının içinde (boş bant yok) · tahrik + gergi teknik bölmede"),',
  'uçtan uca · üstü %.0f · rulolar uç duvarlarının içinde (boş bant yok) · tahrik + gergi teknik bölmede" % BANT_UST_HAT),')
d('("F_UST_RAF", "Fırın üstü HAVALANDIRMALI raf (bizim) · 3 mm raf 40 mm takozlu, altında 0,8 mm ışınım kalkanı (10 mm) · üstünde pizza kutusu yedeği 55 + TOPPING kompresörü (ortam sınırı 40 °C)"),',
  '("F_UST_RAF", "Fırın üstü HAVALANDIRMALI raf (bizim) · 4 mm raf %.0f–%.0f, 10 takozlu (Ø16, aralık 360; gövde üstünden 39), altında 0,8 mm ışınım kalkanı (10 mm) · üstünde SOLDA pizza kutusu yedeği 320 + SAĞDA TOPPING kompresörü (ortam sınırı 40 °C)" % UST_RAF_Y),')
d('("F_ARKA_SAC", "F arka sacı (bizim) · 1,5 mm · 956–1483"),',
  '("F_ARKA_SAC", "F arka sacı (bizim) · 1,5 mm · %.0f–%.0f" % (YG0, YG1 + 10.0)),')

# ---- __main__: v7 KOT DENETİMİ (parçalardan ölçülür; hedefler SPEC_alcak_hat_v57 tablosundan) ----
KOT_KOD = '''    # v7 · ALÇAK HAT KOT DENETİMİ — hedefler SPEC_alcak_hat_v57 "Kotlar" tablosu; değerler PARÇALARDAN ölçülür
    def _bbk(birim=None, ad=None):
        _s = [dunya(p) for p in ps if (birim is None or p["birim"] == birim) and (ad is None or p["ad"] == ad)]
        assert _s, (birim, ad)
        return cq.Compound.makeCompound(_s).BoundingBox()
    _kot = [("fırın gövdesi altı (F_TP10_GOVDE ymin)", _bbk("F_TP10_GOVDE").ymin, 788.0),
            ("fırın gövdesi üstü (F_TP10_GOVDE ymax)", _bbk("F_TP10_GOVDE").ymax, 1305.0),
            ("fırın bandı üstü (bant_ust_00 ymax)", _bbk(ad="bant_ust_00").ymax, 998.0),
            ("giriş bandı üstü (giris_bandi ymax = fırın bandı)", _bbk(ad="giris_bandi").ymax, 998.0),
            ("çıkış ölü plakası üstü (K bandı 996 + 1,5)", _bbk(ad="cikis_olu_plakasi").ymax, 997.5),
            ("ışınım kalkanı altı (gövde üstü + 10)", _bbk(ad="isi_kalkani").ymin, 1315.0),
            ("raf üstü (ust_raf ymax)", _bbk(ad="ust_raf").ymax, 1348.0),
            ("F arka sacı (y üst = kalkan)", _bbk(ad="f_arka_saci").ymax, 1315.0),
            ("F_UST_RAF birimi üstü", _bbk("F_UST_RAF").ymax, 1348.0)]
    _kalan = []
    for _a, _v, _h in _kot:
        _ok = abs(_v - _h) < 0.01
        if not _ok: _kalan.append(_a)
        print("   v7 KOT %-52s %8.2f · hedef %7.1f  %s" % (_a, _v, _h, "GEÇTİ" if _ok else "** KALDI **"))
    _tb = (DISK_UST - 11.0, DISK_UST)                                                           # TOPPING tabla altı … disk üstü (TC yerel 97–108)
    _yk_ok = YARIK_V2[1][2] < _tb[0] and YARIK_V2[1][3] > _tb[1] and DISK_UST - 16.0 < _tb[0] and DISK_UST + 42.0 > _tb[1]
    print("   v7 YARIK / AĞIZ: yarık açıklığı %.0f–%.0f · kabuk giriş ağzı %.0f–%.0f · tabla + disk %.0f–%.0f içinden geçer: %s"
          % (YARIK_V2[1][2], YARIK_V2[1][3], DISK_UST - 16.0, DISK_UST + 42.0, _tb[0], _tb[1], "GEÇTİ" if _yk_ok else "** KALDI **"))
    if not _yk_ok: _kalan.append("yarık/ağız")
    _mb = _bbk(ad="giris_bandi_motoru")
    _m_ok = YG0 < _mb.ymin and _mb.ymax < YG1
    print("   v7 GİRİŞ BANDI MOTORU y %.1f–%.1f · gövde %.0f–%.0f içinde: %s" % (_mb.ymin, _mb.ymax, YG0, YG1, "GEÇTİ" if _m_ok else "** KALDI **"))
    if not _m_ok: _kalan.append("motor")
    assert not _kalan, "v7 kot denetimi: %s" % _kalan
'''
d('    # v6 · RAF YÜK HESABI', KOT_KOD + '    # v6 · RAF YÜK HESABI')

# ---- çıktı adları ----
for a, b, n in (("firin_tp10_v6.glb", "firin_tp10_v7.glb", 2), ('"firin_tp10_v6"', '"firin_tp10_v7"', 1),
                ('"generator": "AUTOKITCH firin_tp10_cad_v6"', '"generator": "AUTOKITCH firin_tp10_cad_v7"', 1),
                ('print("TP10-UZUN v6 ·', 'print("TP10-UZUN v7 ·', 1),
                ('"uzatılmış fırın · AUTOKITCH v6 (79 öne, raf 4 mm)"', '"uzatılmış fırın · AUTOKITCH v7 (alçak hat: bant 998)"', 1),
                ('"ana makine v52"', '"ana makine v57"', 1)):
    d(a, b, n)
io.open(os.path.join(U, "firin_tp10_cad_v7.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v7.py yazildi")
