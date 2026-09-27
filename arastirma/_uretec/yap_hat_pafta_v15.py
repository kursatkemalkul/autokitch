# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v14 → v15 (27 Eyl 2026): pafta = montaj v54.
TOPPING yalıtımı tek dikdörtgen (kırmızı) + teknik cep ince saçla (mavi L) · teknik zarflar 1701,5'e iner · K: tank + pano yukarıda, taban BOŞ ·
F: bez/eldiven kutusu 740–950 (v14'te 1045'e çıkıp fırına giriyordu — Kemal) · fırın üstü sağ içecek 4 koli + dolapta 5. koli ·
E: alt raf 790 (ayaklar üstünde biter, altı boş) · hava ana hattı yeni yol (üst görünüş)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v14.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


NL = chr(10)
# ---- TOPPING yalıtımı
d('''    d.rectangle([X(90.0), fy(1968.0), X(790.0), fy(1317.0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(790.0), fy(1740.0), X(1710.0), fy(1317.0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([X(95.0), fy(1962.0), X(785.0), fy(1320.0)], fill=BG, outline=LINE, width=1)
    d.rectangle([X(795.0), fy(1680.0), X(1705.0), fy(1320.0)], fill=BG, outline=LINE, width=1)
    txt(X(440.0), fy(1990.0), "SOĞUK HÜCRE · tavan 1968'e yükseldi (sos + harç)", f7, GRAY, "mm")
    txt(X(1250.0), fy(1710.0), "SOĞUK HÜCRE +3 °C · tavan 1680", f7, GRAY, "mm")''',
  '''    d.rectangle([X(33.0), fy(2028.0), X(W_C - 33.0), fy(1277.0)], fill=PUC, outline=GRAY, width=1)          # v15: yalıtım TEK DİKDÖRTGEN (PU 60)
    d.rectangle([X(90.0), fy(1968.0), X(790.0), fy(1317.0)], fill=BG, outline=LINE, width=1)                # soğuk A
    d.rectangle([X(790.0), fy(1690.0), X(1710.0), fy(1317.0)], fill=BG, outline=LINE, width=1)              # soğuk B
    d.rectangle([X(791.5), fy(1968.0), X(1710.0), fy(1691.5)], fill=SOFT, outline=None)                     # teknik cep
    d.line([(X(790.0), fy(1968.0)), (X(790.0), fy(1690.0)), (X(1710.0), fy(1690.0))], fill=ACC, width=4)    # ince ayırma saçı (mavi L)
    txt(X(440.0), fy(1995.0), "YALITIM TEK DİKDÖRTGEN · PU 60 · soğuk hacim +3 °C tek parça · mavi = 1,5 mm saç (teknik cep)", f7, GRAY, "mm")
''')
for a, b in (('kesik(X_C, 850.0, 1150.0, 1772.0, 1992.0, "SOĞUTMA GRUBU", INK)', 'kesik(X_C, 850.0, 1150.0, 1701.5, 1921.5, "SOĞUTMA GRUBU", INK)'),
             ('kesik(X_C, 1180.0, 1580.0, 1772.0, 2012.0, "PANO", INK, "PLC · röleler")', 'kesik(X_C, 1180.0, 1580.0, 1701.5, 1941.5, "PANO", INK, "PLC · röleler")'),
             ('kesik(X_C, 1600.0, 1655.0, 1772.0, 1897.0, "", INK)', 'kesik(X_C, 1600.0, 1655.0, 1701.5, 1826.5, "", INK)'),
             ('txt(fx(X_C + 1627.0), fy(1915.0), "güç", f7, INK, "mm")', 'txt(fx(X_C + 1627.0), fy(1845.0), "güç", f7, INK, "mm")'),
             ('kesik(X_C, 1660.0, 1709.0, 1772.0, 1894.0, "", INK)', 'kesik(X_C, 1660.0, 1709.0, 1701.5, 1823.5, "", INK)'),
             ('txt(fx(X_C + 1684.0), fy(1935.0), "UPS", f7, INK, "mm")', 'txt(fx(X_C + 1684.0), fy(1865.0), "UPS", f7, INK, "mm")'),
             ('    d.rectangle([X(33.0), fy(2027.0), X(W_C - 33.0), fy(1987.0)], fill=PUC, outline=GRAY, width=1)\n', ''),
             ('"MODÜL C · TOPPING v2 (topping_uno_cad_v9 + topping_cad_v24) ·', '"MODÜL C · TOPPING v2 (topping_uno_cad_v10 + topping_cad_v24) ·'),
             ("1680.0, 1772.0, H_MAK))", "1690.0, H_MAK))")):
    d(a, b)
# ---- K
d('''    kapak(X_K, 40.0, 440.0, 130.0, 745.0, "İÇECEK YEDEĞİ|soğutmasız · önde|5 koli × 24 = 120|160 + 120 = 280 = 4 gün", fill=(255, 244, 230))
    kesik(X_K, 40.0, 420.0, 130.0, 640.0, "", GRAY)
    kesik(X_K, 60.0, 220.0, 665.0, 959.0, "TEREYAĞI", RED, "3 L ısıtmalı|basınçlı tank")
    kesik(X_K, 300.0, 565.0, 660.0, 1045.0, "PANO", GRAY, "S7-1200 · STP-DRV|NDR-240 · PNOZ|PWM sprey")''',
  '''    txt(fx(X_K + 300.0), fy(600.0), "TABAN BOŞ (v54)", f8, GRAY, "mm")
    txt(fx(X_K + 300.0), fy(600.0) + 20, "içecek yedeği fırın üstüne · tank + pano yukarıda", f7, GRAY, "mm")
    kesik(X_K, 54.0, 226.0, 1635.0, 1980.0, "TEREYAĞI 3 L", RED, "ısıtmalı basınçlı tank|arkasında MS4 + valf adası")
    kesik(X_K, 300.0, 565.0, 1640.0, 2025.0, "PANO (arkada)", GRAY, "S7-1200 · STP-DRV|NDR-240 · PNOZ|PWM sprey")''')
d('    kesik(X_K, 60.0, 250.0, 1700.0, 1860.0, "HAVA", GRAY, "MS4 + VUVG 4 × 5/2")\n', '')
d('"MODÜL K · KESME + SPREY (kesme_cad_v2)"', '"MODÜL K · KESME + SPREY (kesme_cad_v3)"')
# ---- F
d('kapak(X_F, 510.0, 656.0, 740.0, 1045.0, "bez|eldiven|poşet", fill=(255, 244, 230))', 'kapak(X_F, 510.0, 656.0, 740.0, 950.0, "bez|eldiven|poşet", fill=(255, 244, 230))   # v15: 950 (dolap üstü 956; v14 1045 fırına giriyordu)')
d('txt(fx(X_F + 1068.0), fy(936.0), "BOŞ (v52: kutu yedeği fırın üstüne alındı) · önde 804 × 823 × 404", f7, GRAY, "mm")',
  'kapak(X_F, 670.0, 1070.0, 130.0, 253.0, "İÇECEK · 5. koli · 24", fill=(255, 244, 230))' + NL +
  '    txt(fx(X_F + 1068.0), fy(936.0), "pizza gözü: altta 5. içecek kolisi (fırın üstüne sığmadı) · üstü boş", f7, GRAY, "mm")')
d('    satirlar(fx(2922.0), fy(1800.0), "PİZZA KUTUSU YEDEĞİ · TEK YER|320 kutu düz · 804 × 404 × 512|şarjör 567 + 320 = 887 = 3,1 gün", f8, INK, 20)',
  '    satirlar(fx(2922.0), fy(1800.0), "PİZZA KUTUSU YEDEĞİ · TEK YER|320 kutu düz · 804 × 404 × 512|şarjör 567 + 320 = 887 = 3,1 gün|arkada davlumbaz · raf 4 mm, 10 takoz", f8, INK, 20)' + NL +
  '    d.rectangle([fx(3328.0), fy(2008.0), fx(3595.0), fy(1516.0)], fill=(255, 244, 230), outline=LINE, width=2)' + NL +
  '    for _k in range(1, 4):' + NL +
  '        d.line([(fx(3328.0), fy(1516.0 + _k * 123.0)), (fx(3595.0), fy(1516.0 + _k * 123.0))], fill=LINE, width=1)' + NL +
  '    satirlar(fx(3461.5), fy(1770.0), "İÇECEK|4 koli|96 kutu", f8, INK, 20)')
d('    satirlar(fx(3462.0), fy(1900.0), "DAVLUMBAZ|arka yarıda|fan + filtre", f7, GRAY, 17)\n    satirlar(fx(3462.0), fy(1640.0), "raf 4 mm|10 takoz|99 kg", f7, INK, 17)\n', '')
# ---- E
d('    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KATLAMA (kutu_cad_v3)",',
  '    d.rectangle([fx(X_E + 4.0), fy(790.0), fx(X_E + 800.0), fy(786.0)], fill=INK)' + NL +
  '    txt(fx(X_E + 404.0), fy(790.0) - 12, "ALT RAF 790 · kalıp ayakları burada biter · altı BOŞ (796 × 630 × 348)", f7, INK, "mm")' + NL +
  '    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KATLAMA (kutu_cad_v4)",')
# ---- plan: hava ana hattı yeni yol
d('''    dline((fx(2375.0), py(-790.0)), (fx(3790.0), py(-790.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-790.0)), (fx(3790.0), py(-660.0)), (60, 110, 200), 3, 10, 6)''',
  '''    dline((fx(2340.0), py(-740.0)), (fx(2340.0), py(-432.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(2340.0), py(-432.0)), (fx(3790.0), py(-432.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-432.0)), (fx(3790.0), py(-780.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-780.0)), (fx(4085.0), py(-780.0)), (60, 110, 200), 3, 10, 6)''')
d('"HAVA ANA HATTI Ø10 · fırın üstü raftaki kompresör (sağ) → davlumbaz bölmesi → TOPPING şartlandırıcısı"',
  '"HAVA ANA HATTI Ø10 (üstte, y 1950–1977) · kompresör → yığınların arkası z −432 → TOPPING teknik cebi → şartlandırıcı · K dalı z −780 → MS4"')
# ---- parça listesi + başlık
d('taban: önde içecek yedeği · arkada tereyağı tankı 3 L + pano (kompresör fırın üstünde)"', 'üstte köprünün arkasında tereyağı tankı 3 L + pano · taban dolabı BOŞ (kompresör fırın üstünde)"')
d('"KESME + SPREY (kesme_cad_v2 · ön kapak yok) ·', '"KESME + SPREY (kesme_cad_v3 · ön kapak yok · tank + pano yukarıda) ·')
d('"KUTU KATLAMA (kutu_cad_v3) ·', '"KUTU KATLAMA (kutu_cad_v4 · kalıp ayakları alt rafta 790, altı boş) ·')
d('"İÇECEK 120 kutu (K tabanı önde, soğutmasız) → 4 gün ·', '"İÇECEK 120 kutu soğutmasız: fırın üstü sağ 4 koli (96) + F dolabında 1 koli (24) → 4 gün ·')
d('Ø10 ana hat davlumbaz bölmesinden TOPPING\'e"', 'Ø10 ana hat yığınların arkasından (z −432) TOPPING teknik cebine, K dalı MS4\'e"')
d('"TOPPING v2 (topping_uno_cad_v5 ·', '"TOPPING v2 (topping_uno_cad_v10 · yalıtım tek dikdörtgen PU 60, teknik cep 1,5 mm saçla ayrık ·')
d('tavan sos+harç 1968 · UYARI: tekne sağa 85, kasnak 35 mm taşıyor"', 'soğuk hacim A 1968 / B 1690 · teknik cep 1690–1968 (ince saç → soğuk hücreye ≈ +65 W ısı, VARSAYIM)"')
d('TEKNİK RESİM  v14  ·  MONTAJ v52  ·  F TP10 1500 (79 öne)  ·  TOPPING uno v9 + v24  ·  itici v3  ·  K kesme v2  ·  E kutu v3',
  'TEKNİK RESİM  v15  ·  MONTAJ v54  ·  F TP10 1500 (79 öne)  ·  TOPPING uno v10 + v24  ·  itici v3  ·  K kesme v3  ·  E kutu v4')
d('kompresör + kutu yedeği (320) fırın üstünde', 'fırın üstünde: kutu yedeği 320 (sol) · içecek 96 · kompresör (sağ)')
s = s.replace("HAT_ATOSA_TABLALI_v14_HD.png", "HAT_ATOSA_TABLALI_v15_HD.png").replace("HAT_ATOSA_TABLALI_v14_EKRAN.png", "HAT_ATOSA_TABLALI_v15_EKRAN.png")
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v15.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v15.py yazildi")
