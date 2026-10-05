# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v18 → v19 (montaj v70 · bantlı tabla). Yalnız değişen çizim/yazı; yapı ve stil v18 ile aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v18.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


d('"""AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v18 · ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (28 Eyl 2026)',
  '"""AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v19 · BANTLI TABLA (29 Eyl 2026) — montaj v70 ile eşit:' + NL +
  '  tabla Ø340 + disk + aktarma iticisi YERİNE kare bant kaseti 310 × 310 (bantli_tabla_cad_v1) · sabit mıknatıslı tahrik TOPPING sağ-arkada ·' + NL +
  '  aktarma 2365,4 · HGR15 ray 2298 (x 200–2498) · fırın v9: yükleme bandı ön odada 2522–2845, ısıtılan 2912–3940 = 1028 (3 ürün) · çıktı klasörleri dosyaya göreli.' + NL +
  'v18: AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v18 · ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (28 Eyl 2026)')
d('import firin_tp10_cad_v8 as FT ', 'import firin_tp10_cad_v9 as FT ')
d('import itici_cad_v5 as IT                    # v18: aktarma iticisi (kotlar v4 ile aynı)',
  'import bantli_tabla_montaj_v1 as BT          # v19: kaset + sabit tahrik + yükleme bandı (itici_cad_v5 KALKTI)' + NL +
  'import topping_hesap_v7 as TH7               # v19: aktarma 1665,4 · ray 1798 · X torku')
d('KLASOR = r"C:\\Users\\Kemal\\Desktop\\Kemal\\WEBSITE\\AUTOKITCH\\arastirma\\FULL_MAKINE".replace("WEBSITE", "WEBS\\u0130TE")',
  'KLASOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "FULL_MAKINE")                       # v19: dosyaya göreli (iş klasörü)')
d('SITE_IMG = r"C:\\Users\\Kemal\\Desktop\\Kemal\\WEBSITE\\AUTOKITCH\\otonom\\hat\\img".replace("WEBSITE", "WEBS\\u0130TE")',
  'SITE_IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "hat", "img")   # v19: dosyaya göreli')
d('AD_DOSYA = "HAT_ATOSA_TABLALI_v18"', 'AD_DOSYA = "HAT_ATOSA_TABLALI_v19"')
# ---- F · yükleme bandı (ön görünüş)
d('    d.rectangle([fx(2509.0), fy(BANT_F), fx(2565.5), fy(BANT_F - 10.0)], fill=EVC, outline=BUZ, width=2)',
  '    d.rectangle([fx(FT.YB_BURUN[0] - 6.35), fy(BT.UST), fx(FT.YB_SON), fy(FT.YB_TAHRIK[1] - FT.YB_TAHRIK[2] - 0.35)], fill=EVC, outline=BUZ, width=2)   # v19: yükleme bandı' + NL +
  '    txt(fx((FT.YB_BURUN[0] + FT.YB_SON) / 2.0), fy(BT.UST + 22.0), "YÜKLEME BANDI %s–%s" % (sayi(round(FT.YB_BURUN[0] - 6.35, 1)), sayi(round(FT.YB_SON, 1))), f7, BUZ, "mm")')
d('"MODÜL F · TP10 FIRIN (firin_tp10_cad_v8) + ÜST KABİN (firin_ust_kabin_cad_v1)"', '"MODÜL F · TP10 FIRIN (firin_tp10_cad_v9 · yükleme bandı ön odada) + ÜST KABİN (firin_ust_kabin_cad_v1)"')
# ---- başlık
d('TEKNİK RESİM  v18  ·  ÖN DÜZLEM +79  ·  derinlik 909 (arka −830 sabit)  ·  montaj v64  ·  her istasyon kapaklı temiz kutu"',
  'TEKNİK RESİM  v19  ·  BANTLI TABLA  ·  ÖN DÜZLEM +79  ·  derinlik 909 (arka −830 sabit)  ·  montaj v70  ·  her istasyon kapaklı temiz kutu"')
d('mekanizma tabanı 892 · disk 1000  ·  QR dolabı', 'mekanizma tabanı 892 · kaset bandı 1000  ·  QR dolabı')
# ---- C · ön görünüş
d('RAY = (200.0, 2485.0, 912.5, 927.5)', 'RAY = (200.0, 700.0 + TH7.RAY_X1, 912.5, 927.5)')
d('    d.rectangle([fx(180.0), fy(P), fx(520.0), fy(989.0)], fill=EVC, outline=BUZ, width=2)' + NL +
  '    d.rectangle([fx(200.0), fy(950.5), fx(500.0), fy(940.5)], fill=ACC, outline=ACC)',
  '    d.rectangle([fx(196.6), fy(P), fx(503.4), fy(978.0)], fill=EVC, outline=BUZ, width=2)                     # v19: kaset (park) · taban 978 · bant üstü 1000' + NL +
  '    d.rectangle([fx(200.0), fy(950.5), fx(480.0), fy(940.5)], fill=ACC, outline=ACC)                          # v19: araba plakası 280')
d('"TABLA ARABASI · strok 1987 (x 350 → 2337) · HGR15 ray 2285 · GT3 kapalı çevrim · tekne 893–923 · tabla Ø340 + disk · üstü %s · z −170" % sayi(P)',
  '"TABLA ARABASI · strok %s (x 350 → %s) · HGR15 ray %s · GT3 kapalı çevrim · tekne 893–923 · KASET 310 × 310 kare bant · üstü %s · z −170" % (sayi(TH7.X_STROK), sayi(round(BT.AKT, 1)), sayi(TH7.RAY_UZUNLUK), sayi(P))')
d('    _i0 = IT.PC[0] + IT.S_STROK0 - IT.MY["Z"] / 2.0; _i1 = IT.PC[0] + IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0' + NL +
  '    d.rectangle([fx(_i0), fy(IT.Y_TABLA_YUZ + IT.MY["H"]), fx(_i1), fy(IT.Y_TABLA_YUZ)], outline=ACC, width=3)' + NL +
  '    _xe = IT.PC[0] + IT.S_END' + NL +
  '    d.rectangle([fx(_xe - 10.0), fy(IT.BAR_Y1), fx(_xe), fy(IT.BAR_Y0)], fill=ACC)' + NL +
  '    d.line([(fx(_xe - 5.0), fy(IT.BAR_Y1)), (fx(_xe - 5.0), fy(IT.Y_TABLA_YUZ))], fill=ACC, width=2)',
  '    _st = [p["sh"].BoundingBox() for p in BT.TAHRIK]                                                           # v19: sabit tahrik (kapak arkasında → kesik)' + NL +
  '    drect(fx(min(b_.xmin for b_ in _st)), fy(max(b_.ymax for b_ in _st)), fx(max(b_.xmax for b_ in _st)), fy(min(b_.ymin for b_ in _st)), ACC, 2)')
d('    etiket(fx(2120.0), fy(1084.0), "AKTARMA İTİCİSİ · MY1B16-250", f7, ACC, ACC)',
  '    etiket(fx(2120.0), fy(1084.0), "SABİT TAHRİK · mıknatıslı · NEMA23", f7, ACC, ACC)')
d('"MODÜL C · TOPPING v2 (topping_uno_cad_v14 + topping_cad_v25) · soğuk kapaklı · 4 UNO + 2 bizim kaset · havalı · itici", "1800 × 909 × %s · dolap üstünde (kaide %s) · disk %s"',
  '"MODÜL C · TOPPING v2 (topping_uno_cad_v15 + topping_cad_v27) · soğuk kapaklı · 4 UNO + 2 bizim kaset · havalı · bantlı tabla", "1800 × 909 × %s · dolap üstünde (kaide %s) · kaset bandı %s"')
# ---- PLAN
d('    d.ellipse([fx(180.0), py(ZT - 170.0), fx(520.0), py(ZT + 170.0)], fill=EVC, outline=BUZ, width=2)' + NL +
  '    txt(fx(350.0), py(ZT - 190.0), "TABLA Ø340 · park · z −170", f7, BUZ, "mm")',
  '    d.rectangle([fx(196.6), py(ZT - 155.0), fx(503.4), py(ZT + 155.0)], fill=EVC, outline=BUZ, width=2)            # v19: kaset 310 × 310 (park)' + NL +
  '    txt(fx(350.0), py(ZT - 175.0), "KASET 310 × 310 · park · z −170 · dönüş Ø%s" % sayi(round(2.0 * BT.H.R_SUP, 1)), f7, BUZ, "mm")')
d('    dline((fx(350.0), py(ZT)), (fx(2337.0), py(ZT)), ACC, 3, 12, 6)', '    dline((fx(350.0), py(ZT)), (fx(BT.AKT), py(ZT)), ACC, 3, 12, 6)')
d('    _i0p = IT.PC[0] + IT.S_STROK0 - IT.MY["Z"] / 2.0; _i1p = IT.PC[0] + IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0' + NL +
  '    for xt in (1957.5, 2337.0):' + NL +
  '        darc(fx(xt), py(ZT), 170.0 * S, 0.0, 360.0, BUZ, 2, 4.0)' + NL +
  '    d.rectangle([fx(_i0p), py(IT.PC[1] + IT.W_AXIS - IT.MY["NW"] / 2.0), fx(_i1p), py(IT.PC[1] + IT.W_AXIS + IT.MY["NW"] / 2.0)], outline=ACC, width=3)' + NL +
  '    d.rectangle([fx(IT.PC[0] + IT.S_END - 10.0), py(IT.PC[1] + IT.BAR_W0), fx(IT.PC[0] + IT.S_END), py(IT.PC[1] + IT.BAR_W1)], fill=ACC)' + NL +
  '    txt(fx(2495.0), py(FT.ZS) + 50, "itici MY1B16-250 · ekseni z −%s · düz 170" % sayi(abs(IT.PC[1] + IT.W_AXIS)), f7, ACC, "rm")' + NL +
  '    d.rectangle([fx(2509.0), py(-341.0), fx(2565.5), py(-10.0)], fill=EVC, outline=BUZ, width=2)',
  '    darc(fx(1957.5), py(ZT), BT.H.R_SUP * S, 0.0, 360.0, BUZ, 2, 4.0)                                            # v19: kasetin dönüş zarfı (kaşar istasyonu)' + NL +
  '    drect(fx(BT.AKT - 153.4), py(ZT - 155.0), fx(BT.AKT + 153.4), py(ZT + 155.0), BUZ, 2)                           # kaset aktarmada' + NL +
  '    drect(fx(min(b_.xmin for b_ in _st)), py(min(b_.zmin for b_ in _st)), fx(max(b_.xmax for b_ in _st)), py(max(b_.zmax for b_ in _st)), ACC, 2)' + NL +
  '    txt(fx(2465.0), py(-560.0), "sabit tahrik", f7, ACC, "mm")' + NL +
  '    d.rectangle([fx(FT.YB_BURUN[0] - 6.35), py(BT.ZE - 148.0), fx(FT.YB_SON), py(BT.ZE + 148.0)], fill=EVC, outline=BUZ, width=2)   # v19: yükleme bandı' + NL +
  '    txt(fx(2684.0), py(-75.0), "YÜKLEME BANDI", f7, BUZ, "mm")')
# ---- KESİT 1
d('"Robot hamur TOPUNU ağızdan çalışma diskinin ortasına bırakır', '"Robot hamur TOPUNU ağızdan kasetin bandının ortasına bırakır')
d('    d.rectangle([z(-340.0), fy(P), z(0.0), fy(989.0)], fill=EVC, outline=BUZ, width=2)' + NL +
  '    txt(z(-200.0), fy(969.0), "tabla Ø340 + disk · üstü %s" % sayi(P), f7, BUZ, "mm")',
  '    d.rectangle([z(-325.0), fy(P), z(-15.0), fy(978.0)], fill=EVC, outline=BUZ, width=2)                                   # v19: kaset kesiti' + NL +
  '    txt(z(-170.0), fy(966.0), "kaset 310 · bant üstü %s" % sayi(P), f7, BUZ, "mm")')
# ---- parça listesi
d('"A x 8–692 · C x 708–2492 · 788–892 → mekanizma tabanı 892 · disk 1000"', '"A x 8–692 · C x 708–2492 · 788–892 → mekanizma tabanı 892 · kaset bandı 1000"')
d('("MODÜL C", "TOPPING v2 (topping_uno_cad_v11 + topping_cad_v24, 168 aşağı',
  '("MODÜL C", "TOPPING v2 (topping_uno_cad_v15 + topping_cad_v27 · bantlı tabla, 168 aşağı')
d('"1800 × 909 × 1074 · dolap üstünde (kaide 104) · disk üstü 1000 · soğuk hacim', '"1800 × 909 × 1074 · dolap üstünde (kaide 104) · kaset bandı 1000 · soğuk hacim')
d('        ("TABLA ARABASI", "Ø340 tabla + ÇALIŞMA DİSKİ Ø340 × 8 (pimli) · HGR15 x kızağı · pancake dönüş motoru · açıcı altı → kasetler → fırın ağzı", "1",' + NL +
  '         "kaldırma YOK · park yeri AÇICININ ALTI · tabla ekseni z −170 · disk üstü 1000"),',
  '        ("KASET (bantlı tabla)", "kare bant kaseti 310 × 310 · Forbo Transilon E 3/1 U0/U2 MT 296 · 2 × Ø12 rulo (SMR115-2RS) · kuyruk yaylı gergi (Century 62266SCS) · burun GT2 20T ↔ rotor 28T (Gates 140-2GT-6) · 6 mıknatıslı rotor · motor/kablo YOK · ayar bileziğine 2 pimle oturur, elle çıkar", "1",' + NL +
  '         "8,45 kg · bant üstü 1000 · dönüş Ø%s · park AÇICININ ALTI · tabla ekseni z −170" % sayi(round(2.0 * BT.H.R_SUP, 1))),')
d('"strok 1987 (x 350 → 2337) · HGR15 ray 2285 (x 200–2485), 2 sıra · tekne 2440 (893–923)"',
  '"strok %s (x 350 → %s) · HGR15 ray %s (x 200–%s), 2 sıra · tekne 2440 (893–923)" % (sayi(TH7.X_STROK), sayi(round(BT.AKT, 1)), sayi(TH7.RAY_UZUNLUK), sayi(700.0 + TH7.RAY_X1))')
d('"1,2 N·m · gereken 0,382 → 3,14 kat pay · sürtünme 10 N VARSAYIM"',
  '"1,2 N·m · gereken %s → %s kat pay (kaset 8,45 kg) · sürtünme 10 N VARSAYIM" % (sayi(round(TH7.X_GEREKEN_TORK, 3)), sayi(round(TH7.X_TORK_PAY, 2)))')
a0 = s.index('        ("AKTARMA İTİCİSİ", "itici_cad_v4')
a1 = s.index('        ("MODÜL F", "TP10 KESİTLİ KONVEYÖR FIRIN')
s = s[:a0] + ('        ("SABİT TAHRİK", "TOPPING sağ-arkasında · pencereli paslanmaz kutu (IP69K yıkama) + NEMA23 STP-MTR-23079 · 6 mıknatıslı disk kasetin rotorunu 4,6 mm\'den dokunmadan kavrar · kasette kilit: rotor mıknatısı 1.4016 pime", "1",' + NL +
              '         "x 2435–2497 · z −356…−508 · y 954–1019 · kayış kirişine braketli"),' + NL +
              '        ("YÜKLEME BANDI", "F ön odasında (bizim) · PTFE 296 · Ø12 burun + Ø30 tahrik · STP-MTR-23079 + GT2 1:1 (teknik bölmede) · kaset burnu %s → bant → fırın bandı %s" % (sayi(round(FT.X_DISK_KENAR, 1)), sayi(FT.BANT_X[0])), "1",' + NL +
              '         "x %s–%s · üstü %s · ayaklar gövde tabanında" % (sayi(round(FT.YB_BURUN[0] - 6.35, 1)), sayi(round(FT.YB_SON, 1)), sayi(BT.UST))),' + NL) + s[a1:]
d('"TP10 KESİTLİ KONVEYÖR FIRIN (firin_tp10_cad_v8) + ÜST KABİN (firin_ust_kabin_cad_v1, 2 düşer kapak) · Sveba Dahlen TP10 kesiti 730 × 517, gövde 1500 ÖZEL SİPARİŞ · kızılötesi üst + alt · ısıtılan 1316 · aynı anda 4 ürün',
  '"TP10 KESİTLİ KONVEYÖR FIRIN (firin_tp10_cad_v9) + ÜST KABİN (firin_ust_kabin_cad_v1, 2 düşer kapak) · Sveba Dahlen TP10 kesiti 730 × 517, gövde 1500 ÖZEL SİPARİŞ · ön oda %s (yükleme bandı) · kızılötesi üst + alt · ısıtılan %s · aynı anda %d ürün" % (sayi(FT.ON_ODA), sayi(FT.ODA), FT.N_URUN) + "')
import re
kalan = re.findall(r"(?<![A-Za-z_])IT\.", s)
assert not kalan, len(kalan)
compile(s, "teknik_hat_atosa_tablali_v19.py", "exec")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v19.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v19.py yazildi")
