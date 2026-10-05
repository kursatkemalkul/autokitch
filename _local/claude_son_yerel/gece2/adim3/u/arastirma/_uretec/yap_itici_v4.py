# -*- coding: utf-8 -*-
"""itici_cad_v3 → itici_cad_v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57.md · resim ALCAK_HAT_RESIM1_v4, Kemal onaylı).
Disk üstü 1168 → 1000 (TOPPING mekanizma tabanı 892 + 108); v3'teki bütün mutlak y'ler DISK_UST'e bağlandı (tokenize taraması: y rolünde yalnız bunlar):
  · PIDE_UST 1196 / TOP_UST 1201      → DISK_UST + 28 / + 33
  · TAVAN 1277                        → DISK_UST + 109   (TU soğuk oda yalıtımı altı = SOGUK_TABAN − 43; alçak hatta 1152 − 43 = 1109)
  · Y_SERBEST 1210                    → DISK_UST + 42
  · BAR_Y0 / BAR_Y1 1170 / 1200       → DISK_UST + 2 / + 32
  · PIVOT_Y 1224                      → Y_TABLA_YUZ − 3 − 7 (taban plakasının 7 altı; = DISK_UST + 56)
  · MAKARA y 1214                     → PIVOT_Y − 10
  · denetim: kaşar/sucuk iniş boruları 1216–1305 → DISK_UST + 48…+137 · tabla boş sensörü 1210–1250 → DISK_UST + 42…+82
x, z (C0, C1, PC, THETA, W_AXIS), ölçüler, katalog parçaları, parça adları, gruplar, fonksiyonlar v3 ile aynı. Metinler biçimli yazıldı;
denetime ALÇAK HAT kot satırı eklendi."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "itici_cad_v3.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""AKTARMA İTİCİSİ v3 · itici_cad_v3 · 27 Eyl 2026 (v2 + FIRIN 79 ÖNE:',
  '"""AKTARMA İTİCİSİ v4 · itici_cad_v4 · 27 Eyl 2026 (v3 + ALÇAK HAT: bütün kotlar 168 aşağı, disk üstü 1168 → 1000; her y artık DISK_UST\'e bağlı —\n'
  'PIDE_UST, TOP_UST, TAVAN, Y_SERBEST, BAR_Y0/1, PIVOT_Y, MAKARA y ve denetimdeki boru/sensör kotları; x, z, ölçüler, katalog parçaları v3 ile aynı).\n'
  'Önceki: itici_cad_v3.py\n'
  'v3 · itici_cad_v3 · 27 Eyl 2026 (v2 + FIRIN 79 ÖNE:')
d("DISK_UST, PIDE_UST, TOP_UST = 1168.0, 1196.0, 1201.0      # disk üstü · pide üstü · topping üstü (kaşar katmanı)",
  "DISK_UST = 1000.0                             # v4 ALÇAK HAT (v3 1168 − 168) · TOPPING çalışma diski üstü (mekanizma tabanı 892 + 108) · bütün y'ler buna bağlı\n"
  "PIDE_UST, TOP_UST = DISK_UST + 28.0, DISK_UST + 33.0      # 1028 · 1033 · pide üstü · topping üstü (kaşar katmanı)")
d("TAVAN = 1277.0                                # soğuk oda yalıtımının alt yüzü (montaj düzlemi)",
  "TAVAN = DISK_UST + 109.0                      # 1109 (v3 1277) · soğuk oda yalıtımının alt yüzü (montaj düzlemi) · TU: SOGUK_TABAN − 43 (alçak hatta 1152 − 43)")
d("# pidenin x boyunca geliş koridoru (z) — bu koridorda 1210'un altında sabit parça olamaz",
  "# pidenin x boyunca geliş koridoru (z) — bu koridorda Y_SERBEST'in (1042) altında sabit parça olamaz")
d("Y_SERBEST = 1210.0                            # gelen pidenin (topping 1201) üstünde bırakılan boşluk çizgisi",
  "Y_SERBEST = DISK_UST + 42.0                   # 1042 (v3 1210) · gelen pidenin (topping 1033) üstünde bırakılan boşluk çizgisi (topping + 9)")
d("BAR_Y0, BAR_Y1 = 1170.0, 1200.0               # çubuk yüzü kotları (diskin 2 mm üstünden pide üstüne)",
  "BAR_Y0, BAR_Y1 = DISK_UST + 2.0, DISK_UST + 32.0   # 1002 · 1032 çubuk yüzü kotları (diskin 2 mm üstünden pide üstüne)")
d('Y_TABLA_YUZ = TAVAN - 6.0 - MY["H"]           # 1234 · kızak', 'Y_TABLA_YUZ = TAVAN - 6.0 - MY["H"]           # 1066 · kızak')
d("PIVOT_Y = 1224.0                              # pivot ekseni (w yönünde), taban plakasının 7 altı; çatal kulakları 1219'a iner",
  "PIVOT_Y = Y_TABLA_YUZ - 3.0 - 7.0             # 1056 (v3 1224) · pivot ekseni (w yönünde), taban plakasının (3 mm) 7 altı; çatal kulakları PIVOT_Y − 5'e (1051) iner")
d('MAKARA = dict(s=-7.5, y=1214.0, r=4.0, w=-37.0)', 'MAKARA = dict(s=-7.5, y=PIVOT_Y - 10.0, r=4.0, w=-37.0)')
d("sucuk borusunun gerisinde); altı 1210", "sucuk borusunun gerisinde); altı PIVOT_Y − 14 = Y_SERBEST (1042)")
d('link 90° kalkar · altı 1210 (pide üstü 1201)"))',
  'link 90° kalkar · altı %.0f (pide üstü %.0f)" % (Y_SERBEST, TOP_UST)))')
d("(1217'ye kadar)", "(PIVOT_Y − 7 = 1049'a kadar)")
d("kalkınca en alt 1212", "kalkınca en alt PIVOT_Y − 12 = 1044")
d('"pide kenarını 30 mm boyunca iter · POM burçla pivot pimine · kalkınca 1222–1226\'da yatar"))',
  '"pide kenarını 30 mm boyunca iter · POM burçla pivot pimine · kalkınca y %.0f–%.0f aralığında yatar" % (PIVOT_Y - 2.0, PIVOT_Y + 2.0)))')
# ---- denetim: başka modüllerin parça kopyaları (TU iniş boruları, TC sensör) disk kotuna bağlı ----
d('BORU_KASAR = ("sil", 2061.0, -150.0, 25.0, 1216.0, 1305.0)                # kaşar iniş borusu Ø50 (TU6 ölçüldü)',
  'BORU_KASAR = ("sil", 2061.0, -150.0, 25.0, DISK_UST + 48.0, DISK_UST + 137.0)   # kaşar iniş borusu Ø50 (TU6 ölçüldü) · v4: 1048–1137 (v3 1216–1305)')
d('BORU_SUCUK = ("sil", 2310.0, -150.0, 24.0, 1216.0, 1305.0)                # sucuk iniş borusu Ø48',
  'BORU_SUCUK = ("sil", 2310.0, -150.0, 24.0, DISK_UST + 48.0, DISK_UST + 137.0)   # sucuk iniş borusu Ø48 · v4: 1048–1137')
d('SENSOR = ("kut", 2341.0, 2359.0, 1210.0, 1250.0, -179.0, -161.0)          # tabla boş sensörü (TC24)',
  'SENSOR = ("kut", 2341.0, 2359.0, DISK_UST + 42.0, DISK_UST + 82.0, -179.0, -161.0)   # tabla boş sensörü (TC24) · v4: 1042–1082 (v3 1210–1250)')
d("# koridor kuralı: ev konumunda 1210'un altında hiçbir itici parçası pide koridorunda olamaz",
  "# koridor kuralı: ev konumunda Y_SERBEST'in altında hiçbir itici parçası pide koridorunda olamaz")
d('sonuc.append(("EV (kalkık) · pide koridorunda (z −320…−20) 1210\'un altında parça yok", not ihlal, str(ihlal)))',
  'sonuc.append(("EV (kalkık) · pide koridorunda (z −320…−20) Y_SERBEST %.0f altında parça yok" % Y_SERBEST, not ihlal, str(ihlal)))')
d("# zarf: modül içinde (x ≤ 2492 sağ dış sac, z ≤ −5, y ≤ 1277)", "# zarf: modül içinde (x ≤ 2492 sağ dış sac, z ≤ −5, y ≤ TAVAN)")
d('sonuc.append(("%s · zarf: x ≤ 2492 (%.0f) · z ≤ −5 (%.0f) · y ≤ 1277 (%.0f)" % (ad, max(b.xmax for b in b_all), max(b.zmax for b in b_all), max(b.ymax for b in b_all)),',
  'sonuc.append(("%s · zarf: x ≤ 2492 (%.0f) · z ≤ −5 (%.0f) · y ≤ %.0f (%.0f)" % (ad, max(b.xmax for b in b_all), max(b.zmax for b in b_all), TAVAN, max(b.ymax for b in b_all)),')
# ---- v4: ALÇAK HAT kot denetimi (SPEC_alcak_hat_v57: disk 1000; kiriş üstü = TAVAN; ev konumunda en alt parça Y_SERBEST'in üstünde) ----
KOT_KOD = '''    # v4 · ALÇAK HAT: disk üstü SPEC 1000 · ev (kalkık) konumunda ÖLÇÜLEN en üst = TAVAN (kiriş üstü) · en alt ≥ Y_SERBEST
    P = kur(S_HOME, True); _b = [dunya(p).BoundingBox() for p in P]
    _ymax, _ymin = max(b.ymax for b in _b), min(b.ymin for b in _b)
    sonuc.append(("ALÇAK HAT (SPEC v57) · disk üstü %.0f = 1000 · EV (kalkık) ölçülen y %.1f…%.1f: üst = TAVAN %.0f, alt ≥ Y_SERBEST %.0f" % (DISK_UST, _ymin, _ymax, TAVAN, Y_SERBEST),
                  abs(DISK_UST - 1000.0) < 0.01 and abs(_ymax - TAVAN) < 0.01 and _ymin >= Y_SERBEST - 0.01, ""))
    return sonuc
'''
d('    return sonuc\n', KOT_KOD)
d('print("İTİCİ v3 ·', 'print("İTİCİ v4 ·')
# v3 denetimleri bitirip yorumlayıcı kapanırken OCC erişim ihlaliyle (Windows, çıkış kodu 127) düşüyordu → fırın modülündeki gibi temiz çıkış
d('    assert not kal, kal\n', '    assert not kal, kal\n    sys.stdout.flush(); os._exit(0)                                                    # v4: kapanıştaki OCC erişim ihlalini atla (v3\'te çıkış 127)\n')
io.open(os.path.join(U, "itici_cad_v4.py"), "w", encoding="utf-8").write(s)
print("itici_cad_v4.py yazildi")
