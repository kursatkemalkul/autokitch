# -*- coding: utf-8 -*-
"""teknik_itici_v1 → teknik_itici_v2 (27 Eyl 2026): itici_cad_v3 (düz itme 170, fırın 79 öne, destek plakası yok)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_itici_v1.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def sil_satir(onek):
    global s
    i = s.index(onek); assert s.count(onek) == 1, onek
    j = s.index("\n", i) + 1
    s = s[:i] + s[j:]


d("import itici_cad_v1 as IT", "import itici_cad_v3 as IT")
d('''    d.rectangle([ux(2500), uz(0), ux(2700), uz(-730)], fill=ODA_R, outline=LINE, width=2)
    d.rectangle([ux(2505), uz(-89), ux(2569), uz(-409)], fill=PASL, outline=INK, width=2)
    d.rectangle([ux(2568), uz(-92.5), ux(2700), uz(-473.5)], fill=(236, 236, 240), outline=INK, width=2)
    d.line([(ux(2564), uz(-79)), (ux(2700), uz(-79))], fill=RED, width=3); d.line([(ux(2564), uz(-485)), (ux(2700), uz(-485))], fill=RED, width=3)
    txt(ux(2610), uz(-60), "tünel ön duvarı −79", f7, RED, "lm"); txt(ux(2610), uz(-500), "tünel arka duvarı −485", f7, RED, "lm")
    txt(ux(2537), uz(-249), "giriş bandı", f7, INK, "mm"); txt(ux(2640), uz(-283), "fırın bandı 381 · eksen −283", f7, INK, "mm")''',
  '''    d.rectangle([ux(2500), uz(79), ux(2700), uz(-651)], fill=ODA_R, outline=LINE, width=2)                    # v2: fırın gövdesi 79 öne (+79…−651)
    d.rectangle([ux(2505), uz(-10), ux(2569), uz(-330)], fill=PASL, outline=INK, width=2)
    d.rectangle([ux(2568), uz(-13.5), ux(2700), uz(-394.5)], fill=(236, 236, 240), outline=INK, width=2)
    d.line([(ux(2564), uz(0)), (ux(2700), uz(0))], fill=RED, width=3); d.line([(ux(2564), uz(-406)), (ux(2700), uz(-406))], fill=RED, width=3)
    txt(ux(2610), uz(24), "tünel ön duvarı iç yüzü 0 (gövde +79 çıkıntı)", f7, RED, "lm"); txt(ux(2610), uz(-421), "tünel arka duvarı −406", f7, RED, "lm")
    txt(ux(2537), uz(-170), "giriş bandı", f7, INK, "mm"); txt(ux(2640), uz(-204), "fırın bandı 381 · eksen −204", f7, INK, "mm")''')
d('txt(ux(1960), UY0 - 60, "ÜST GÖRÜNÜŞ · dünya x–z · tabla aktarma konumunda · itici evde (çubuk kalkık) ve sonda (kesik)", f16, ACC)',
  'txt(ux(1960), UY0 - 120, "ÜST GÖRÜNÜŞ · dünya x–z · tabla aktarma konumunda · itici evde (çubuk kalkık) ve sonda (kesik) · fırın gövdesi +79 çıkıntı", f16, ACC)')
sil_satir('    d.rectangle([ux(2200), uz(-345), ux(2490), uz(-420)], fill=PASL, outline=INK, width=2); txt(ux(2345), uz(-382), "destek plakası')
d('''    olcu_h(ux(cx), ux(ex), uz(60), sayi(ex - cx)); olcu_v(ux(2560), uz(cz), uz(ez), sayi(cz - ez), yon="r")
    olcu_h(ux(2200), ux(2490), uz(-450), "290"); olcu_h(ux(2500), ux(2568), uz(-560), "68")''',
  '''    olcu_h(ux(cx), ux(ex), uz(60), "itme %s · düz" % sayi(ex - cx)); olcu_h(ux(2500), ux(2568), uz(-560), "68")''')
d('''    txt(ux(1960), uz(-540), "SMC MY1B16-250 · gövde %s (mavi, tabanın altında 1243–1271) · ekseni çubuk çizgisinin %s gerisinde, iniş borularının arasından" % (sayi(S1 - S0), sayi(-WA)), f7, INK, "lm")''',
  '''    txt(ux(1960), uz(-540), "SMC MY1B16-250 · gövde %s (mavi, tabanın altında 1243–1271) · ekseni ürün hattının %s gerisinde (z −212): iniş borularına 18,5 · sensöre 23 · ön düzlemi kesmez" % (sayi(S1 - S0), sayi(-WA)), f7, INK, "lm")''')
d('txt(x0, y0 - 38, "PARÇA LİSTESİ (itici_cad_v1 · BOM)", f16, ACC)', 'txt(x0, y0 - 38, "PARÇA LİSTESİ (itici_cad_v3 · BOM)", f16, ACC)')
d('''    for i, s_ in enumerate(("çubuğun pide kenarına basınç dağılımı (30 mm yüzey) — pilot", "destek plakası sürtünmesi (PTFE kaplama seçeneği) — pilot",
                            "SMC MY1B16 STEP'i (föy ölçüleriyle kutu model)", "kaldırma pimi – POM makara aşınması — pilot"), 1):''',
  '''    for i, s_ in enumerate(("çubuğun pide kenarına basınç dağılımı (30 mm yüzey) — pilot",
                            "SMC MY1B16 STEP'i (föy ölçüleriyle kutu model)", "kaldırma pimi – POM makara aşınması — pilot"), 1):''')
d('txt(150, 40, "AUTOKITCH  ·  AKTARMA İTİCİSİ  ·  TOPPING diskinden fırın giriş bandına  ·  TEKNİK RESİM v1", f30, INK)',
  'txt(150, 40, "AUTOKITCH  ·  AKTARMA İTİCİSİ  ·  TOPPING diskinden fırın giriş bandına · DÜZ (fırın 79 öne)  ·  TEKNİK RESİM v2", f30, INK)')
d('''    txt(150, 98, "3B model itici_cad_v1 (tek kaynak) · SMC MY1B16-250 çapraz %s° · itme %s (+%s x · %s z) · pivotlu çubuk 170 × 30, sabit pimle 90° kalkar · destek plakası y 1167 · ana montaj v49 · ölçüler mm"
        % (sayi(IT.THETA), sayi(IT.L_ITME), sayi(IT.C1[0] - IT.C0[0]), sayi(IT.C1[1] - IT.C0[1])), f11, GRAY)''',
  '''    txt(150, 98, "3B model itici_cad_v3 (tek kaynak) · SMC MY1B16-250 x boyunca DÜZ (θ %s°) · itme %s (+%s x · %s z) · pivotlu çubuk 170 × 30, sabit pimle 90° kalkar · destek plakası YOK · ana montaj v51 · ölçüler mm · 27 Eylül 2026"
        % (sayi(abs(IT.THETA)), sayi(IT.L_ITME), sayi(IT.C1[0] - IT.C0[0]), sayi(IT.C1[1] - IT.C0[1])), f11, GRAY)''')
d('yol = os.path.join(KLASOR, "ITICI_v1_teknik.png")', 'yol = os.path.join(KLASOR, "ITICI_v2_teknik.png")')
d('"otonom", "hat", "img", "ITICI_v1_teknik.png")', '"otonom", "hat", "img", "ITICI_v2_teknik.png")')
io.open(os.path.join(U, "teknik_itici_v2.py"), "w", encoding="utf-8").write(s)
print("teknik_itici_v2.py yazildi")
