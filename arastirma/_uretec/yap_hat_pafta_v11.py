# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v10 → v11 : pafta montaj v44 ile eşitlenir
B = store_cad_v5 (tam kaplayan kapaklar · yeni dağılım · K4 Secop + PLC + kaşar/sucuk deposu + 2 dar içecek) ·
F tabanı (bulaşık US · temizlik · pizza kutusu yedeği önde; deterjan · robot kontrol · ana pano · UPS arkada) ·
K tabanı (içecek yedeği önde; kompresör · yağ · K kartı arkada) · K üstü boş · hava hattı yeni güzergâh."""
import io
U = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec"
s = io.open(U + r"\teknik_hat_atosa_tablali_v10.py", encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis('''HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 241.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK + TATLI · 2 katlı çekmece"}
CAP = {"hamur": (20, "top"), "lahm": (35, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · yedeği K'de → 4 gün")}
KOLON = [[(6, "hamur")], [(2, "hamur"), (6, "lahm")], [(6, "lahm"), (1, "icecek")]]''',
      '''HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 241.0, "ic1": 126.0, "ic1d": 126.0, "tatli": 71.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "icecek": "İÇECEK + TATLI · 2 katlı çekmece", "ic1": "İÇECEK · tek kat", "ic1d": "İÇECEK · tek kat (dar)", "tatli": "TATLI"}
CAP = {"hamur": (20, "top"), "lahm": (36, "top"), "icecek": (0, "180 kutu 330 ml + 14 tatlı · yedeği K'de → 4 gün"), "ic1": (48, "kutu"), "ic1d": (32, "kutu"), "tatli": (30, "kap")}
KOLON = [[(5, "hamur"), (2, "lahm"), (1, "tatli")], [(3, "hamur"), (5, "lahm")], [(5, "lahm"), (2, "ic1")]]   # v11 · store_cad_v5''')
a0 = s.index("def ciz_B():")
a1 = s.index("# ======================= FIRIN · KESME · KUTU")
s = s[:a0] + '''def ciz_B():
    """v11 · store_cad_v5: TAM KAPLAYAN KAPAKLAR (kolonlar arası 3 · her kolonda ön 126 → 1057)"""
    kabin(X_A, W_B, 0.0, H_B)
    KX = {"K1": (0.0, 698.5), "K2": (701.5, 1353.5), "K3": (1356.5, 2008.5), "K4": (2011.5, 2500.0)}
    for ki, gruplar in enumerate(KOLON):
        kol = KOLON_AD[ki]; a_, b_ = KX[kol]
        pn = []; y = YUZ0 + BIND
        for adet, tip in gruplar:
            for _ in range(adet):
                pn.append([y - BIND, y + HH[tip] + BIND, tip]); y += HH[tip] + 2 * BIND + FUGA
        pn[0][0] = 126.0; pn[-1][1] = 1057.0
        for p0, p1, tip in pn:
            d.rectangle([fx(X_A + a_), fy(p1), fx(X_A + b_), fy(p0)], fill=BG, outline=DOLAP, width=1)
        i = 0
        for adet, tip in gruplar:
            g = pn[i:i + adet]; i += adet
            ym = (fy(g[0][0]) + fy(g[-1][1])) / 2
            cap, br = CAP[tip]
            etiket(fx(X_A + (a_ + b_) / 2), ym - 13, "%s × %d" % (AD[tip], adet), f8, INK, DOLAP)
            etiket(fx(X_A + (a_ + b_) / 2), ym + 13, "%d %s · +3 °C" % (adet * cap, br), f7, DOLAP, DOLAP)
        txt(fx(X_A + (a_ + b_) / 2), fy(Y_ALT) + 14, kol, f7, GRAY, "mm")
        olcu_h(fx(X_A + a_), fx(X_A + b_), fy(0) + 44, sayi(b_ - a_), f8, GRAY)
    a_, b_ = KX["K4"]
    for y0_, y1_ in ((126.0, 420.5), (423.5, 669.5), (672.5, 828.5), (831.5, 1057.0)):
        d.rectangle([fx(X_A + a_), fy(y1_), fx(X_A + b_), fy(y0_)], fill=BG, outline=DOLAP, width=1)
    kesik(X_A, 2052.5, 2402.5, 128.5, 400.5, "SOĞUTMA GRUBU", INK, "Secop CU KLF4.0CND · ızgaralı kapak|arkasında PLC + güç + 25 röle")
    satirlar(fx(X_A + (a_ + b_) / 2), fy(560.0), "KAŞAR + SUCUK DEPOSU · 2 gün|GN 1/1-100 + GN 1/2-100 · +3 °C", f8, INK, 19)
    satirlar(fx(X_A + (a_ + b_) / 2), fy(900.0), "İÇECEK tek kat (dar) × 2|64 kutu · +3 °C", f8, DOLAP, 19)
    txt(fx(X_A + (a_ + b_) / 2), fy(Y_ALT) + 14, "K4", f7, GRAY, "mm")
    olcu_h(fx(X_A + a_), fx(X_A + b_), fy(0) + 44, sayi(b_ - a_), f8, GRAY)
    d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)
    modul_etiketi(X_A, W_B, "MODÜL B · ÇEKMECE MODÜLÜ (store_cad_v5) · tam kaplayan kapaklar · 8 pide + 12 lahmacun + 4 tek kat içecek + tatlı · K4: Secop (arkasında PLC) + kaşar/sucuk deposu",
                  "2500 × 830 × 1060 · ön yüz 126–1057 · aralar 3", DOLAP, 1)


''' + s[a1:]
# ---- K
degis('''    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")
    kesik(X_K, 110.0, 490.0, 540.0, 1030.0, "KOMPRESÖR JUN-AIR OF302-15B", INK, "TOPPING'in havası · yağsız · 15 L · 25 kg|YERİ AÇIK (başka istasyonda)")
    satirlar(fx(X_K + W_K / 2), fy(430.0), "taban dolabı 123–1060|yedek kutu YOK", f7, GRAY, 17)''',
      '''    kapak(X_K, 40.0, 440.0, 130.0, 745.0, "İÇECEK YEDEĞİ|soğutmasız · önde|5 koli × 24 = 120|160 + 120 = 280|= 4 gün", fill=(255, 244, 230))
    kesik(X_K, 40.0, 420.0, 130.0, 640.0, "", GRAY); kesik(X_K, 40.0, 440.0, 650.0, 840.0, "", GRAY); kesik(X_K, 40.0, 260.0, 850.0, 1050.0, "", GRAY)
    satirlar(fx(X_K + 510.0), fy(760.0), "ARKADA:|KOMPRESÖR|JUN-AIR|130–640|yağ kartuşu|650–840|K kartı|850–1050", f7, INK, 17)''')
degis('''    kapak(X_K, 33.0, W_K - 33.0, PL + 355.0, 2028.0, "İÇECEK + TATLI YEDEĞİ · 4 GÜN|97 kutu 330 ml (2 kat × 115) + 8 tatlı|çekmece 180 + yedek 97 = 277 = 4 gün")''',
      '''    kapak(X_K, 33.0, W_K - 33.0, PL + 355.0, 2028.0, "BOŞ|içecek yedeği tabana indi (v11)")''')
# ---- F
degis('''    ciz_F([(60.0, 700.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", "245 × 180 × 45"),
           (60.0, 460.0, 320.0, 670.0, "ANA PANO · PLC · ana şalter", "400 × 350 × 250 · ekran yok → tablet"),
           (480.0, 730.0, 320.0, 670.0, "UPS", "500 VA"),
           (760.0, 1230.0, 135.0, 865.0, "BULAŞIK MAKİNESİ · tezgâh altı", "MEIKO M-iClean UM sınıfı · 460 × 600 × 730|sepet 500 × 500 · giriş 315 · 40 sepet/saat"),
           (1250.0, 1440.0, 135.0, 500.0, "MAKİNE DETERJANI + PARLATICI", "2 × 5 L bidon · seviye şamandıralı"),
           (1250.0, 1440.0, 520.0, 865.0, "BOŞ", "190 × 770 × 345")])''',
      '''    ciz_F([])
    kapak(X_F, 40.0, 500.0, 130.0, 830.0, "BULAŞIK MAKİNESİ|MEIKO M-iClean US|460 × 600 (V) × 700|sepet 400 × 400|giriş 315")
    kapak(X_F, 510.0, 656.0, 130.0, 730.0, "TEMİZLİK|2 × 5 L||arkada:|makine|deterjanı +|parlatıcı", fill=(255, 244, 230))
    kapak(X_F, 510.0, 656.0, 740.0, 1045.0, "bez|eldiven|poşet", fill=(255, 244, 230))
    kapak(X_F, 666.0, 1470.0, 130.0, 1030.0, "PİZZA KUTUSU YEDEĞİ · 553 · önde|804 × 404 × 885 · şarjör 567 + 553 = 1120 = 4 gün", yl=985.0, fill=(252, 240, 215))
    kesik(X_F, 666.0, 1141.0, 130.0, 553.0, "ROBOT KONTROL KUTUSU (arkada)", INK, "yer 475 × 423 × 268 (V)|Fairino kompakt 245 × 180 × 89")
    kesik(X_F, 666.0, 1066.0, 565.0, 915.0, "ANA PANO (arkada)", INK, "PLC · ana şalter|400 × 350 × 250 (V)")
    kesik(X_F, 1076.0, 1191.0, 565.0, 750.0, "UPS", INK, "BX500CI|arkada")''')
# ---- plan
degis('''    dline((fx(2375.0), py(-790.0)), (fx(4300.0), py(-790.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(4300.0), py(-790.0)), (fx(4300.0), py(-380.0)), (60, 110, 200), 3, 10, 6)
    txt(fx(3300.0), py(-790.0) - 14, "HAVA ANA HATTI Ø10 · K tabanı → F tabanı arkası → TOPPING şartlandırıcısı", f7, (60, 110, 200), "mm")''',
      '''    dline((fx(2375.0), py(-790.0)), (fx(4230.0), py(-790.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(4230.0), py(-790.0)), (fx(4230.0), py(-765.0)), (60, 110, 200), 3, 10, 6)
    txt(fx(3300.0), py(-790.0) - 14, "HAVA ANA HATTI Ø10 · K tabanı arkasındaki kompresör → F tabanı arkası → TOPPING şartlandırıcısı", f7, (60, 110, 200), "mm")''')
degis('''    txt(fx(cx + 200), py(-20.0) - 6, "K4 · depo · altta (B)", f7, DOLAP, "mm")''',
      '''    txt(fx(cx + 200), py(-20.0) - 6, "K4 · Secop + PLC · depo · 2 dar içecek (B)", f7, DOLAP, "mm")''')
degis('''    txt(z(-340), fy(560.0), "K1 · TAZE PİDE × 6 · çekmece 680 · açılım 628", f7, DOLAP, "mm")''',
      '''    txt(z(-340), fy(560.0), "K1 · 5 pide + 2 lahmacun + tatlı · çekmece 680 · açılım 628", f7, DOLAP, "mm")''')
# ---- başlık + parça listesi
degis('''TEKNİK RESİM  v10  ·  MONTAJ = hat_montaj_v43  ·''', '''TEKNİK RESİM  v11  ·  MONTAJ = hat_montaj_v44  ·''')
degis('''· E = kutu_cad_v3 · B = store_cad_v4  ·  ALT TABAN 123''', '''· E = kutu_cad_v3 · B = store_cad_v5 (tam kaplama)  ·  ALT TABAN 123''')
degis('''        ("MODÜL B", "ÇEKMECE modülü (store_cad_v4) · 21 motorlu çekmece (Transmotec PD3665 + GT3 kayış + Accuride DZ3832 3 parçalı ray · strok 628) · K4: Secop CU soğutma + 2 × GN depo + temizlik nişi · K1 üstü pano", "1", "2500 × 830 × 1060 · gövde 123'ten (ayak + süpürgelik) · yalıtımlı taban 123–164,5"),''',
      '''        ("MODÜL B", "ÇEKMECE modülü (store_cad_v5) · 25 motorlu çekmece (Transmotec PD3665 + GT3 kayış + Accuride DZ3832 3 parçalı ray · strok 628) · TAM KAPLAYAN KAPAKLAR · içecek tek kat + yaylı itici · K4: Secop + arkasında PLC · kaşar/sucuk deposu · 2 dar içecek", "1", "2500 × 830 × 1060 · ön 126–1057 · soğuk: pide 160 · lahmacun 432 · içecek 160 · tatlı 30"),''')
degis('''        ("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · K taban dolabında · Ø10 ana hat F tabanı arkasından TOPPING'e", "1", "380 × 380 × 510 · 25 kg · AÇIK: yeri (kural: istasyon kendi gövdesinde)"),''',
      '''        ("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · K tabanı ARKADA (130–640), üstünde yağ + K kartı · Ø10 ana hat F tabanı arkasından TOPPING'e", "1", "380 × 380 × 510 · 25 kg · arka sacta ızgara"),''')
degis('''"KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 · aynı anda 4 ürün · taban dolabı: robot kontrol, ana pano, UPS, bulaşık makinesi, deterjan"''',
      '''"KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 · aynı anda 4 ürün · taban dolabı: önde bulaşık + temizlik + pizza kutusu yedeği · arkada deterjan + robot kontrol + ana pano + UPS"''')
degis('''· taban dolabı: yağ kartuşu + K kartı", "1", "600 × 830 × 2030 · plaka üstü 1164 · yedek kutu YOK · E için şart: itici 36 mm içeri kaydırır"),''',
      '''· taban dolabı: önde içecek yedeği · arkada kompresör + yağ + K kartı · üst bölme boş", "1", "600 × 830 × 2030 · plaka üstü 1164 · E için şart: itici 36 mm içeri kaydırır"),''')
degis('''        ("BULAŞIK MAKİNESİ", "TEZGÂH ALTI · MEIKO M-iClean UM sınıfı · sepet 500 × 500 · giriş 315 · 40 sepet/saat", "1", "460 × 600 × 730 · F taban dolabında (123–1060) · KASET YATIRILARAK yıkanır · çalışma diski Ø340 düz yatar"),''',
      '''        ("BULAŞIK MAKİNESİ", "MEIKO M-iClean US · sepet 400 × 400 · giriş 315 (meiko.com)", "1", "460 × 600 (V) × 700 · F taban dolabında önde · KASET YATIRILARAK yıkanır · çalışma diski Ø340 düz yatar · harç haznesi sığmaz (elle)"),''')
degis('''        ("YEDEK STOK", "İÇECEK 97 kutu + 8 tatlı (K üst bölme, 2 kat) · KUTU yedeği YOK: şarjör 567 kutu = 2 gün", "", "robotun erişiminde DEĞİL — eleman günlük olarak ana gözlere aktarır"),''',
      '''        ("YEDEK STOK", "İÇECEK 120 kutu (K tabanı önde, soğutmasız) · PİZZA KUTUSU 553 (F tabanı önde) · kaşar + sucuk 2 gün (B/K4 deposu) → hepsi 4 gün", "", "robotun erişiminde DEĞİL — eleman 2 günde bir ana gözlere aktarır"),''')
degis('''        ("TEMİZLİK", "deterjan · bez · eldiven · poşet: B modülü K4 temizlik nişi (2 × 5 L bidon) · makine deterjanı + parlatıcı: bulaşık makinesinin yanında", "", "dükkânda yalnız LAVABO kalır"),''',
      '''        ("TEMİZLİK", "deterjan · bez · eldiven · poşet: F tabanı önde (2 × 5 L bidon) · makine deterjanı + parlatıcı: arkasında, hortum bulaşık makinesine", "", "dükkânda yalnız LAVABO kalır"),''')
degis('''        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F taban dolabı · TOPPING'in kendi panosu + UPS + güç + soğutma grubu üst bantta, 4 sürücü kuru bölmede · ekran yok (tablet)", "", ""),''',
      '''        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F taban dolabı arkada · B panosu K4'te Secop'un arkasında · TOPPING'in panosu + UPS + güç + soğutma grubu üst bantta · ekran yok (tablet)", "", ""),''')
degis('yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v10_HD.png"', 'yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v11_HD.png"')
degis('k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v10_EKRAN.png", optimize=True)', 'k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v11_EKRAN.png", optimize=True)')
io.open(U + r"\teknik_hat_atosa_tablali_v11.py", "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v11.py yazildi")
