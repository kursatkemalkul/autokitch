# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v15 → v16 (27 Eyl 2026): pafta = montaj v56 · TOPPING yalıtımı yalnız soğuk hacmi sarar (uno v11), teknik cep dışarıda ·
içecek 5 koli F dolabında (3 + 2), fırın üstünden kalktı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v15.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


NL = chr(10)
d('''    d.rectangle([X(33.0), fy(2028.0), X(W_C - 33.0), fy(1277.0)], fill=PUC, outline=GRAY, width=1)          # v15: yalıtım TEK DİKDÖRTGEN (PU 60)
    d.rectangle([X(90.0), fy(1968.0), X(790.0), fy(1317.0)], fill=BG, outline=LINE, width=1)                # soğuk A
    d.rectangle([X(790.0), fy(1690.0), X(1710.0), fy(1317.0)], fill=BG, outline=LINE, width=1)              # soğuk B
    d.rectangle([X(791.5), fy(1968.0), X(1710.0), fy(1691.5)], fill=SOFT, outline=None)                     # teknik cep
    d.line([(X(790.0), fy(1968.0)), (X(790.0), fy(1690.0)), (X(1710.0), fy(1690.0))], fill=ACC, width=4)    # ince ayırma saçı (mavi L)
    txt(X(440.0), fy(1995.0), "YALITIM TEK DİKDÖRTGEN · PU 60 · soğuk hacim +3 °C tek parça · mavi = 1,5 mm saç (teknik cep)", f7, GRAY, "mm")''',
  '''    _pu = [(33.0, 1277.0), (33.0, 2028.0), (820.0, 2028.0), (820.0, 1720.0), (W_C - 33.0, 1720.0), (W_C - 33.0, 1277.0)]   # v16: yalıtım YALNIZ soğuk hacmi sarar
    d.polygon([(X(x_), fy(y_)) for x_, y_ in _pu], fill=PUC, outline=GRAY)
    d.rectangle([X(90.0), fy(1968.0), X(790.0), fy(1317.0)], fill=BG, outline=LINE, width=1)                # soğuk A
    d.rectangle([X(790.0), fy(1690.0), X(1710.0), fy(1317.0)], fill=BG, outline=LINE, width=1)              # soğuk B
    d.rectangle([X(821.5), fy(2027.0), X(W_C - 33.0), fy(1721.5)], fill=SOFT, outline=None)                 # teknik cep (yalıtımsız)
    d.line([(X(821.0), fy(2027.0)), (X(821.0), fy(1721.0)), (X(W_C - 33.0), fy(1721.0))], fill=ACC, width=4)   # saç (teknik tarafı)
    txt(X(440.0), fy(1995.0), "YALITIM YALNIZ SOĞUK HACMİ SARAR · PU 60 / L 30 · teknik cep dışarıda, havalandırmalı", f7, GRAY, "mm")''')
for a, b in (('kesik(X_C, 850.0, 1150.0, 1701.5, 1921.5, "SOĞUTMA GRUBU", INK)', 'kesik(X_C, 850.0, 1150.0, 1731.5, 1951.5, "SOĞUTMA GRUBU", INK)'),
             ('kesik(X_C, 1180.0, 1580.0, 1701.5, 1941.5, "PANO", INK, "PLC · röleler")', 'kesik(X_C, 1180.0, 1580.0, 1731.5, 1971.5, "PANO", INK, "PLC · röleler")'),
             ('kesik(X_C, 1600.0, 1655.0, 1701.5, 1826.5, "", INK)', 'kesik(X_C, 1600.0, 1655.0, 1731.5, 1856.5, "", INK)'),
             ('txt(fx(X_C + 1627.0), fy(1845.0), "güç", f7, INK, "mm")', 'txt(fx(X_C + 1627.0), fy(1875.0), "güç", f7, INK, "mm")'),
             ('kesik(X_C, 1660.0, 1709.0, 1701.5, 1823.5, "", INK)', 'kesik(X_C, 1660.0, 1709.0, 1731.5, 1853.5, "", INK)'),
             ('txt(fx(X_C + 1684.0), fy(1865.0), "UPS", f7, INK, "mm")', 'txt(fx(X_C + 1684.0), fy(1895.0), "UPS", f7, INK, "mm")'),
             ('"MODÜL C · TOPPING v2 (topping_uno_cad_v10 + topping_cad_v24) ·', '"MODÜL C · TOPPING v2 (topping_uno_cad_v11 + topping_cad_v24) ·'),
             ("1690.0, H_MAK))", "1690.0, 1720.0, H_MAK))")):
    d(a, b)
# içecek: fırın üstünden kalktı → dolapta 3 + 2
d('''    d.rectangle([fx(3328.0), fy(2008.0), fx(3595.0), fy(1516.0)], fill=(255, 244, 230), outline=LINE, width=2)
    for _k in range(1, 4):
        d.line([(fx(3328.0), fy(1516.0 + _k * 123.0)), (fx(3595.0), fy(1516.0 + _k * 123.0))], fill=LINE, width=1)
    satirlar(fx(3461.5), fy(1770.0), "İÇECEK|4 koli|96 kutu", f8, INK, 20)''', '')
d('    kapak(X_F, 670.0, 1070.0, 130.0, 253.0, "İÇECEK · 5. koli · 24", fill=(255, 244, 230))' + NL, '')
d('    kesik(X_F, 1076.0, 1191.0, 565.0, 750.0, "UPS", INK, "BX500CI|arkada")',
  '    kesik(X_F, 1076.0, 1191.0, 565.0, 750.0, "UPS", INK, "BX500CI|arkada")' + NL +
  '    kapak(X_F, 670.0, 1070.0, 130.0, 499.0, "İÇECEK · önde|3 koli · 72", fill=(255, 244, 230))' + NL +
  '    kapak(X_F, 1070.0, 1470.0, 130.0, 376.0, "İÇECEK · önde|2 koli · 48", fill=(255, 244, 230))')
d('"içecek yedeği fırın üstüne · tank + pano yukarıda"', '"içecek yedeği F dolabında · tank + pano yukarıda"')
d('"pizza gözü: altta 5. içecek kolisi (fırın üstüne sığmadı) · üstü boş"', '"pizza gözü: içecek 5 koli (3 + 2) = 120 · 4 gün · üstü boş"')
# başlık + parça listesi
d('TEKNİK RESİM  v15  ·  MONTAJ v54  ·  F TP10 1500 (79 öne)  ·  TOPPING uno v10 + v24', 'TEKNİK RESİM  v16  ·  MONTAJ v56  ·  F TP10 1500 (79 öne)  ·  TOPPING uno v11 + v24')
d('fırın üstünde: kutu yedeği 320 (sol) · içecek 96 · kompresör (sağ)', 'fırın üstünde kutu yedeği 320 + kompresör · içecek 5 koli F dolabında')
d('"İÇECEK 120 kutu soğutmasız: fırın üstü sağ 4 koli (96) + F dolabında 1 koli (24) → 4 gün ·', '"İÇECEK 120 kutu soğutmasız: F dolabının pizza gözünde 5 koli (3 + 2) → 4 gün ·')
d('"TOPPING v2 (topping_uno_cad_v10 · yalıtım tek dikdörtgen PU 60, teknik cep 1,5 mm saçla ayrık ·', '"TOPPING v2 (topping_uno_cad_v11 · yalıtım yalnız soğuk hacmi sarar: A tavanı 60 + L 30 + arka bölme, teknik cep dışarıda ·')
d('teknik cep 1690–1968 (ince saç → soğuk hücreye ≈ +65 W ısı, VARSAYIM)"', 'teknik cep 820–1800 × 1720–2028 dışarıda (L PU 30 → soğuğa ≈ 14 W, VARSAYIM)"')
s = s.replace("HAT_ATOSA_TABLALI_v15_HD.png", "HAT_ATOSA_TABLALI_v16_HD.png").replace("HAT_ATOSA_TABLALI_v15_EKRAN.png", "HAT_ATOSA_TABLALI_v16_EKRAN.png")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v16.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v16.py yazildi")
