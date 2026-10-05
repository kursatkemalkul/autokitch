# -*- coding: utf-8 -*-
"""itici_cad_v2 → itici_cad_v3 (27 Eyl 2026): FIRIN 79 ÖNE → itme DÜZ x boyunca: C1 = (2507, −170), 170 mm, θ = 0.
Kolsuz silindir gövdesi ürün hattının 42 mm gerisinde sabit z'de (−212): iniş borularına (−150, r 25/24) 18,5 mm, sensöre 23 mm,
ön düzlemi kesmez (TOPPING v9 fitili tam). DESTEK PLAKASI KALKTI (pide diskin z aralığında kalır). Kiriş sağ ucu 2489,5 (zarf 2492)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "itici_cad_v2.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def satir_degis(onek, yeni):
    global s
    i = s.index(onek); assert s.count(onek) == 1, onek
    j = s.index("\n", i)
    s = s[:i] + yeni + s[j:]


d('"""AKTARMA İTİCİSİ v2 · itici_cad_v2 · 26 Eyl 2026 gece (v1 + montaj v49 bulguları: makara/kaldırma pimi −w tarafına, link 26 geniş simetrik)',
  '"""AKTARMA İTİCİSİ v3 · itici_cad_v3 · 27 Eyl 2026 (v2 + FIRIN 79 ÖNE: itme DÜZ x boyunca 170 mm, C1 = (2507, −170), θ = 0; destek plakası KALKTI;\n'
  'kiriş sağ ucu 2489,5). Silindir ekseni z −212: iniş borularına 18,5 mm, tabla boş sensörüne 23 mm, ön düzlemi kesmez. Önceki: itici_cad_v2.py\n'
  'v2 · itici_cad_v2 · 26 Eyl 2026 gece (v1 + montaj v49 bulguları: makara/kaldırma pimi −w tarafına, link 26 geniş simetrik)')
satir_degis("C1 = (2507.0, -249.0)", "C1 = (2507.0, -170.0)                         # v3: itme sonu = disk kenarı, eksen −170 (fırın 79 öne: tünel iç yüzü 0, pidenin ön kenarı −20); ön 89 mm fırın bandında")
d('yerel(kut(S0 - 20.0, S1 + 20.0, TAVAN - 6.0, TAVAN, wa - MY["NW"] / 2.0, wa + MY["NW"] / 2.0))', 'yerel(kut(S0 - 20.0, S1 + 15.0, TAVAN - 6.0, TAVAN, wa - MY["NW"] / 2.0, wa + MY["NW"] / 2.0))')
d('"304 · %.0f mm" % (S1 - S0 + 40.0)', '"304 · %.0f mm" % (S1 - S0 + 35.0)')
i0 = s.index("    # ---- 4 DESTEK PLAKASI"); i1 = s.index("    return PARCALAR", i0)
s = s[:i0] + "    # ---- 4 DESTEK PLAKASI YOK (v3: itme düz, pide diskin z aralığında kalır) ----\n" + s[i1:]
i0 = s.index("BIRIMLER = ["); i1 = s.index("MALZEME = {", i0)
s = s[:i0] + ('BIRIMLER = [("C_ITICI", "Aktarma iticisi (bizim) · SMC MY1B16-250 kolsuz silindir x boyunca DÜZ (v3: fırın 79 öne) · pivotlu çubuk 170 × 30, dönüşte sabit pime rolan makarayla 90° kalkar · pideyi diskten giriş bandına 170 mm iter (2337 → 2507, eksen −170) · silindir ekseni z −212 (iniş borularının gerisinde)")]\n') + s[i1:]
d('= hedef (2540, −249)" % pc_end', '= hedef (2507, −170)" % pc_end')
satir_degis('    sonuc.append(("son konumda pidenin ön kenarı z %.0f ≥ tünel ön duvarı −79 + 20"',
            '    sonuc.append(("son konumda pidenin ön kenarı z %.0f ≤ tünel ön duvarı iç yüzü 0 − 20 (fırın 79 öne)" % (C1[1] + R_PIDE), C1[1] + R_PIDE <= -20.0 + 0.01, ""))')
satir_degis('    sonuc.append(("pide sonda bantlarda:',
            '    sonuc.append(("pide sonda bantlarda: ön kenar %.0f ≥ fırın bandı başı 2568 + 80 · merkez %.0f ≥ giriş bandı burnu 2505 · arka kenar %.0f ≥ disk sol kenarı 2167" % (C1[0] + R_PIDE, C1[0], C1[0] - R_PIDE), C1[0] + R_PIDE >= 2648.0 and C1[0] >= 2505.0 and C1[0] - R_PIDE >= 2167.0, ""))')
d('print("İTİCİ v1 ·', 'print("İTİCİ v3 ·')
io.open(os.path.join(U, "itici_cad_v3.py"), "w", encoding="utf-8").write(s)
print("itici_cad_v3.py yazildi")
