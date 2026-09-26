# -*- coding: utf-8 -*-
"""firin_tp10_cad_v3 → firin_tp10_cad_v4 (26 Eyl 2026 gece, mühendislik kontrolü):
 FIRIN ÜSTÜ RAF HAVALANDIRMALI: JUN-AIR OF302-15B'nin izin verilen ortam sıcaklığı 0–40 °C (üretici föyü); 400 °C fırının üst
 yüzeyine 5 mm'lik kapalı hava boşluğuyla konan raf ısınır. v4: takozlar 40 mm (Ø16 boru, 6 adet, M6 saplama), altta 0,8 mm 304
 ISI KALKANI (fırın üstünden 10 mm yukarıda, ışınımı keser), üstte 3 mm raf (fırın üstünden 40 mm: yanlardan açık, doğal
 havalandırma). Raf z −15…−420 (davlumbaz −425'ten başlar, 5 mm pay). Raf üstü 1473 + 43 = 1516 → kompresör üstü 1516 + 510 = 2026 ≤ hat 2030 (4 mm). Kutu yedeği 55 (88 mm) 1516–1604.
 Fırın üst yüzey sıcaklığı yine üreticiden istenecek (AÇIK); raf üstü sıcaklık pilotta ölçülecek."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v3.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


d("UST_RAF_Y = (YG1 + 5.0, YG1 + 8.0)                              # 1478–1481 · fırın üstünde havalı raf (5 mm takoz + 3 mm plaka)",
  "UST_RAF_Y = (YG1 + 40.0, YG1 + 43.0)                            # 1513–1516 · fırın üstünde HAVALANDIRMALI raf (40 mm takoz + 3 mm plaka) · v4\n"
  "ISI_KALKANI_Y = (YG1 + 10.0, YG1 + 10.8)                        # 1483–1483,8 · 0,8 mm 304 ışınım kalkanı (fırın üstünden 10 mm)")
d('''    ekle("ust_raf", kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -430.0, -15.0), "sac", "F_UST_RAF",
         bom=("Fırın üstü raf 3 mm", 1, "304 · 1480 × 415", "5 mm takozla gövde üstünde: sıcak yüzeye karton/kompresör değmez · kompresör 25 kg + kutular 8 kg"))''',
  '''    ekle("ust_raf", kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -430.0, -15.0), "sac", "F_UST_RAF",
         bom=("Fırın üstü raf 3 mm", 1, "304 · 1480 × 415", "40 mm takozla gövde üstünde, yanları açık (doğal havalandırma) · altında ışınım kalkanı · kompresör 25 kg + kutular 8 kg · JUN-AIR ortam sınırı 40 °C [föy]"))
    ekle("isi_kalkani", kut(X_F0 + 10.0, X_F1 - 10.0, ISI_KALKANI_Y[0], ISI_KALKANI_Y[1], -430.0, -15.0), "sac", "F_UST_RAF",
         bom=("Isı kalkanı 0,8 mm", 1, "304 · 1480 × 415 · parlak", "fırın üstünden 10 mm yukarıda, takozlara geçme: fırın üst yüzeyinin ışınımını keser, rafla arasında 29 mm hava"))''')
d('''    for i, (x, z) in enumerate(((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -415.0), (XC_TP, -415.0), (X_F1 - 30.0, -415.0))):
        ekle("ust_raf_takozu_%d" % i, sily(x, z, 10.0, YG1, UST_RAF_Y[0]), "pom", "F_UST_RAF")''',
  '''    TAKOZ_XZ = ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -415.0), (XC_TP, -415.0), (X_F1 - 30.0, -415.0))
    for i, (x, z) in enumerate(TAKOZ_XZ):                                                       # v4: iki parça boru takoz (alt 10 · üst 29,2), M6 saplama deliği
        ekle("ust_raf_takozu_alt_%d" % i, sily(x, z, 8.0, YG1, ISI_KALKANI_Y[0]).cut(sily(x, z, 3.3, YG1 - 1.0, ISI_KALKANI_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu alt Ø16 × 10", 6, "304 boru 16 × 1,5 → torna", "fırın üst sacındaki M6 saplamaya geçer · kalkanı taşır") if i == 0 else None)
        ekle("ust_raf_takozu_ust_%d" % i, sily(x, z, 8.0, ISI_KALKANI_Y[1], UST_RAF_Y[0]).cut(sily(x, z, 3.3, ISI_KALKANI_Y[1] - 1.0, UST_RAF_Y[0] + 1.0)), "paslanmaz", "F_UST_RAF",
             bom=("Raf takozu üst Ø16 × 29,2", 6, "304 boru 16 × 1,5 → torna", "kalkan ile raf arasında · rafın üstünden M6 somun") if i == 0 else None)''')
# plakalarda saplama delikleri (Ø6,6) — takozlarla çakışmasın diye kalkan ve raf takoz yerlerinde delinir
d('''    ekle("isi_kalkani", kut(X_F0 + 10.0, X_F1 - 10.0, ISI_KALKANI_Y[0], ISI_KALKANI_Y[1], -430.0, -15.0), "sac", "F_UST_RAF",''',
  '''    _kal = kut(X_F0 + 10.0, X_F1 - 10.0, ISI_KALKANI_Y[0], ISI_KALKANI_Y[1], -430.0, -15.0)
    for x, z in ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -415.0), (XC_TP, -415.0), (X_F1 - 30.0, -415.0)):
        _kal = _kal.cut(sily(x, z, 3.3, ISI_KALKANI_Y[0] - 1.0, ISI_KALKANI_Y[1] + 1.0))
    ekle("isi_kalkani", _kal, "sac", "F_UST_RAF",''')
d('''    ekle("ust_raf", kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -430.0, -15.0), "sac", "F_UST_RAF",''',
  '''    _raf = kut(X_F0 + 10.0, X_F1 - 10.0, UST_RAF_Y[0], UST_RAF_Y[1], -430.0, -15.0)
    for x, z in ((X_F0 + 30.0, -30.0), (XC_TP, -30.0), (X_F1 - 30.0, -30.0), (X_F0 + 30.0, -415.0), (XC_TP, -415.0), (X_F1 - 30.0, -415.0)):
        _raf = _raf.cut(sily(x, z, 3.3, UST_RAF_Y[0] - 1.0, UST_RAF_Y[1] + 1.0))
    ekle("ust_raf", _raf, "sac", "F_UST_RAF",''')
d('''    ("F_UST_RAF", "Fırın üstü havalı raf (bizim) · 3 mm, 5 mm takozlu · üstünde pizza kutusu yedeği 55 + TOPPING kompresörü"),''',
  '''    ("F_UST_RAF", "Fırın üstü HAVALANDIRMALI raf (bizim) · 3 mm raf 40 mm takozlu, altında 0,8 mm ışınım kalkanı (10 mm) · üstünde pizza kutusu yedeği 55 + TOPPING kompresörü (ortam sınırı 40 °C)"),''')
d("Fırın üstüne HAVALI RAF (3 mm, 5 mm takozlu): üstünde pizza kutusu yedeği (55 kutu) + TOPPING kompresörü",
  "Fırın üstüne HAVALANDIRMALI RAF (3 mm, 40 mm takozlu + 0,8 mm ışınım kalkanı — v4): üstünde pizza kutusu yedeği (55 kutu) + TOPPING kompresörü")
for a, b in (("firin_tp10_v3.glb", "firin_tp10_v4.glb"), ("firin_tp10_v3.usdz", "firin_tp10_v4.usdz"), ('"firin_tp10_v3"', '"firin_tp10_v4"')):
    s = s.replace(a, b)
s = s.replace("firin_tp10_cad_v3", "firin_tp10_cad_v4")
# v4 · davlumbaz kutusu −425'ten başlar: raf ve kalkan −420'de biter (5 mm pay), arka takoz sırası −408
s = s.replace("-430.0, -15.0)", "-420.0, -15.0)")
s = s.replace("(X_F0 + 30.0, -415.0), (XC_TP, -415.0), (X_F1 - 30.0, -415.0)", "(X_F0 + 30.0, -408.0), (XC_TP, -408.0), (X_F1 - 30.0, -408.0)")
s = s.replace("304 · 1480 × 415", "304 · 1480 × 405")
io.open(os.path.join(U, "firin_tp10_cad_v4.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v4.py yazildi")
