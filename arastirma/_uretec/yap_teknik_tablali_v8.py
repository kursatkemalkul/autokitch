# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v7 -> v8 : PAFTA MODELE (montaj v41) EŞİTLENDİ

Kemal (25 Eyl 2026): "teknik resmi de buna göre güncelle, siteye update et."
v7, 24 Eylül öğleden sonraki TOPPING'i gösteriyordu; o günden beri model değişti ve pafta geride kaldı:
  · E KUTU KATLAMA = kutu_cad_v3: modül 830 (hat 5300 → 5430), standart 32 × 32 × 4,2 kutu, şarjör arkada 567 kutu,
    besleyici 1500, tepsi 1104, kutulama ağzı 1085–1330, pano arka üstte. Eski vantuzlu kutu açıcı ve KUTU TEPSİSİ kalktı.
  · ALT TABAN ÇİZGİSİ 123: bütün gövdeler yerden 123'te başlar (ayak + süpürgelik 60 geride); B yalıtımlı tabanı 123–164,5.
  · SÜREÇ KOTU 1168 (taban hizası, 24 Eyl): istasyon tabanları 1060, çalışma diski üstü 1168, fırın bandı 1166,
    kesme plakası 1164, kutu tepsisi 1104. v7'deki 1340 / 1490 / 1627 Atosa varsayım kotları kalktı.
  · TOPPING iç kotları topping_cad_v22'den: tabla mekanizması 1060–1168, soğuk kabin 1250–1760, kaset sırası 1320–1680,
    nozullar 1220'ye iner, pano + soğutma bandı 1772–2012. Tabla ekseni z −170 (v7'de −270 çiziliydi).
  · KASETLER (montaj v41): yalnız KAŞAR KABI (v14 + Codex v15 aday) ve KÜP SUCUK (v7 + Codex V2 aday) takılı;
    HARÇ 1–2, KIYMA, KUŞBAŞI yuvaları şimdilik boş (kesik).
  · B = store_cad_v4 (K4: Secop CU + GN depo + temizlik nişi, K1 üstü pano), F gövdesi 1060–1486, K plakası 560 × 450
    (z −470…−20), K'de yedek kutu yok.
  · Açıcının ön motoru ve kafa plakası modelde gövdenin 180 mm önüne taşıyor → KESİT 1'de gerçek haliyle gösterilir (uyarı).
Yalnız TABLALI pafta üretilir (bantlı pafta v6 ayrı, ona dokunulmaz).
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


def blok_degis(bas, son, yeni):
    """bas satırından (dahil) son satırına (hariç) kadar olan bloğu değiştirir"""
    global s
    i = s.index(bas); j = s.index(son, i)
    assert s.count(bas) == 1
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 1) ortak veri: E 830 + v8 sabitleri
degis('''X_F, W_F, X_K, W_K, X_E, W_E = 2500.0, 1500.0, 4000.0, 600.0, 4600.0, 700.0
HAT = X_E + W_E                                              # 5300''',
      '''X_F, W_F, X_K, W_K, X_E, W_E = 2500.0, 1500.0, 4000.0, 600.0, 4600.0, 830.0   # v8: E 830 (kutu_cad_v3)
HAT = X_E + W_E                                              # 5430
Y_ALT, B_TABAN = 123.0, 164.5                                # v8: ALT TABAN ÇİZGİSİ · B iç taban üstü (en alt çekmece önü 167,5 − 3)
P_SUREC, BANT_F, PLAKA_K, TEPSI_E = 1168.0, 1166.0, 1164.0, 1104.0   # v8: çalışma diski · fırın bandı · kesme plakası · kutu tepsisi
ZT = -170.0                                                  # v8: tabla / ürün ekseni (topping_cad_v22)''')

# ---------------------------------------------------------------- 2) kabin + govde: süpürgelik 123
degis('''    d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
    if y0 == 0.0:
        d.rectangle([x0, fy(120), x1, fy(0)], fill=SOFT, outline=LINE, width=2)''',
      '''    if y0 == 0.0:                                                   # v8: gövde 123'ten, altı ayak + süpürgelik (60 geride)
        d.rectangle([x0, fy(y1), x1, fy(Y_ALT)], fill=FILL, outline=LINE, width=4)
        d.rectangle([fx(x0mm + 30.0), fy(Y_ALT), fx(x0mm + w - 30.0), fy(0)], fill=SOFT, outline=LINE, width=2)
    else:
        d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)''')
degis('''    d.rectangle([z(-790), fy(h1), z(40), fy(h0)], fill=FILL, outline=LINE, width=4)
    if plint:
        d.rectangle([z(-790), fy(120), z(40), fy(0)], fill=SOFT, outline=LINE, width=2)''',
      '''    d.rectangle([z(-790), fy(h1), z(40), fy(max(h0, Y_ALT) if plint else h0)], fill=FILL, outline=LINE, width=4)
    if plint:                                                        # v8: süpürgelik 60 geride, gövde 123'ten
        d.rectangle([z(-760), fy(Y_ALT), z(-20), fy(0)], fill=SOFT, outline=LINE, width=2)''')

# ---------------------------------------------------------------- 3) B · F · K · E istasyonları (modelden)
blok_degis("# ======================= MODUL B (v19 ile ayni) =======================", "# ======================= PLAN · ORTAK =======================", r'''# ======================= MODUL B (v8 · store_cad_v4) =======================
def ciz_B():
    kabin(X_A, W_B, 0.0, H_B)
    K4X, K4W = X_A + XI + 3 * (WO + BOLME), 400.0                                      # 2027,5
    d.rectangle([fx(X_A + 30), fy(H_B - 60.0), fx(X_A + W_B - 30), fy(B_TABAN)], fill=BG, outline=LINE, width=2)
    d.rectangle([fx(X_A + 30), fy(B_TABAN), fx(K4X - 1.0), fy(Y_ALT + 1.5)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_A + 1000), fy((Y_ALT + B_TABAN) / 2), "yalıtımlı taban 41,5 · en alt çekmece önünün 3 mm altı · gövde 123'ten", f7, GRAY, "mm")
    d.rectangle([fx(X_A + 30), fy(H_B - 1.5), fx(X_A + W_B - 30), fy(H_B - 60.0)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_A + W_B / 2), fy(H_B - 30.0), "tavan PU 60 · üstüne MODÜL A ve C oturur · çekmece önü 40 PU + fitil · çekmece başına Transmotec PD3665 + GT3 kayış · Accuride DZ3832 3 parçalı ray · strok 628", f7, GRAY, "mm")
    cx = X_A + XI
    for ki, gruplar in enumerate(KOLON):
        if ki:
            d.rectangle([fx(cx - BOLME), fy(H_B - 60.0), fx(cx), fy(B_TABAN)], fill=SOFT, outline=LINE, width=1)
        y = YUZ0
        for adet, tip in gruplar:
            h = HH[tip] + 2 * BIND
            ybas = y
            for _ in range(adet):
                d.rectangle([fx(cx + 8), fy(y + h), fx(cx + WO - 8), fy(y)], fill=BG, outline=DOLAP, width=(2 if tip == "icecek" else 1))
                if tip == "icecek":
                    d.line([(fx(cx + 8), fy(y + h / 2)), (fx(cx + WO - 8), fy(y + h / 2))], fill=DOLAP, width=2)
                y += h + FUGA
            cap, br = CAP[tip]
            ym = (fy(ybas) + fy(y - FUGA)) / 2
            etiket(fx(cx + WO / 2), ym - 13, ("%s × %d" % (AD[tip], adet)) if cap else AD[tip], f8, INK, DOLAP)
            etiket(fx(cx + WO / 2), ym + 13, ("%d %s · +3 °C" % (adet * cap, br)) if cap else (br + " · +3 °C"), f7, DOLAP, DOLAP)
        txt(fx(cx + WO / 2), fy(H_B - 60.0) + 14, KOLON_AD[ki], f7, GRAY, "mm")
        olcu_h(fx(cx), fx(cx + WO), fy(0) + 44, "620", f8, GRAY)
        cx += WO + BOLME
    # K4 · soğutma bölmesi SICAK: tabanı tek sac (PU yok) · Secop 128,5 · ara PU 408,5–438,5 · GN depo · temizlik nişi
    d.rectangle([fx(K4X - BOLME), fy(H_B - 60.0), fx(K4X), fy(B_TABAN)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([fx(K4X), fy(H_B - 60.0), fx(K4X + K4W), fy(Y_ALT + 1.5)], fill=BG, outline=LINE, width=2)
    for y0_, y1_ in ((167.5, 420.5), (423.5, 739.5), (742.5, 997.0)):
        kapak(X_A, K4X - X_A - 15.0, K4X - X_A + K4W + 15.0, y0_, y1_)
    kesik(X_A, K4X - X_A + 25.0, K4X - X_A + 375.0, 128.5, 400.5, "SOĞUTMA GRUBU", INK, "Secop CU KLF4.0CND|350 × 272 × 450")
    satirlar(fx(K4X + K4W / 2), fy(590.0), "DEPO · 2 × GN 1/1-150|kaşar blok / sucuk · +3 °C", f8, INK, 19)
    satirlar(fx(K4X + K4W / 2), fy(870.0), "TEMİZLİK NİŞİ|2 × 5 L bidon", f8, INK, 19)
    # K1 üstü kuru teknik bölme + pano · K2 üstü sabit panel
    K1X = X_A + XI
    kapak(X_A, K1X - X_A - 15.0, K1X - X_A + WO + 15.0, 815.5, 997.0)
    kesik(X_A, K1X - X_A + 14.0, K1X - X_A + 300.0, 878.0, 978.0, "PLC S7-1200 1214C", INK, "+ 2 × SM1221 + SM1222")
    kesik(X_A, K1X - X_A + 310.0, K1X - X_A + 606.0, 878.0, 978.0, "NDR-240-24 · EM-324C", INK, "21 seçici röle · klemens")
    K2X = K1X + WO + BOLME
    kapak(X_A, K2X - X_A - 15.0, K2X - X_A + WO + 15.0, 941.5, 997.0)
    olcu_h(fx(K4X), fx(K4X + K4W), fy(0) + 44, "400", f8, GRAY)
    d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)
    modul_etiketi(X_A, W_B, "MODÜL B · ÇEKMECE MODÜLÜ (store_cad_v4) · 8 pide + 12 lahmacun + içecek/tatlı · K4: Secop soğutma + GN depo + temizlik nişi · K1 üstü: pano · gövde 123'ten",
                  "2500 × 830 × 1060", DOLAP, 1)


# ======================= FIRIN · KESME · KUTU (v8 · montaj v41'den) =======================
def ciz_F(taban_parcalar):
    G0, G1 = H_B, 1486.0                                      # gövde 1060–1486 (taban hizası) · bant üstü 1166
    kabin(X_F, W_F, 0.0, H_MAK, "F · KONVEYÖR FIRIN · özel · elektrikli · 4 ürün")
    kapak(X_F, 33.0, W_F - 33.0, Y_ALT + 3.0, G0 - 3.0)
    for a, b, y0, y1, et, alt in taban_parcalar:
        kesik(X_F, a, b, y0, y1, et, INK, alt)
    d.rectangle([fx(X_F + 3), fy(G1), fx(X_F + W_F - 3), fy(G0)], fill=PUC, outline=LINE, width=2)
    tarali(fx(X_F + 3), fy(G1), fx(X_F + W_F - 3), fy(G0), (226, 214, 190), 11)
    d.rectangle([fx(X_F + 50), fy(BANT_F + 270.0), fx(X_F + 50 + HAZNE), fy(G0 + 20.0)], fill=SICAK, outline=TURUNCU, width=2)
    for i in range(7):
        xx = X_F + 50.0 + 100.0 + i * 200.0
        d.rectangle([fx(xx - 40), fy(BANT_F + 130.0), fx(xx + 40), fy(BANT_F + 60.0)], fill=BG, outline=TURUNCU, width=1)
    txt(fx(X_F + W_F / 2), fy(BANT_F + 215.0), "ÜST PLENUM · hava parmakları × 7 · taşyünü 50", f7, TURUNCU, "mm")
    drect(fx(X_F + 60), fy(BANT_F - 70.0), fx(X_F + 50 + HAZNE - 10), fy(G0 + 25.0), RED, 1)
    txt(fx(X_F + W_F / 2), fy((G0 + BANT_F) / 2 - 12.0), "ALT ISITMA · bant altı pay 106 → ince rezistans / taş VARSAYIM (AÇIK)", f7, RED, "mm")
    d.line([(fx(X_F - 40), fy(BANT_F)), (fx(X_F + W_F + 30), fy(BANT_F))], fill=TURUNCU, width=4)
    for i in range(4):
        xx = X_F + 50.0 + ADIM / 2 + i * ADIM
        d.ellipse([fx(xx - 150), fy(BANT_F + 28.0), fx(xx + 150), fy(BANT_F + 2.0)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(X_F + W_F / 2), fy(BANT_F + 45.0), "PİŞİRME HAZNESİ %s · bant üstü %s · aynı anda 4 ürün (adım %s)" % (sayi(HAZNE), sayi(BANT_F), sayi(ADIM)), f7, TURUNCU, "mm")
    olcu_h(fx(X_F + 50.0), fx(X_F + 50.0 + HAZNE), fy(G1) - 18, "HAZNE %s" % sayi(HAZNE), f8, TURUNCU)
    kapak(X_F, 33.0, W_F - 33.0, G1 + 10.0, 2028.0, "EGZOZ DAVLUMBAZI · fan · yağ + karbon filtre|fırın kartı + SSR + kontaktör (F'nin kendi panosu) · ~18 kW (tahmin)")
    modul_etiketi(X_F, W_F, "MODÜL F · KONVEYÖR FIRIN", "1500 × 830 × 2030 · taban dolabı 123–1060 · gövde %s–%s · bant %s" % (sayi(G0), sayi(G1), sayi(BANT_F)))
    olcu_h(fx(X_F), fx(X_F + W_F), fy(H_MAK) - 26, sayi(W_F), f11, INK)


def ciz_K():
    PL = PLAKA_K
    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME · SPREY")
    kapak(X_K, 33.0, W_K - 33.0, Y_ALT + 3.0, H_B - 3.0)
    kesik(X_K, 60.0, 300.0, 140.0, 330.0, "YAĞ KARTUŞU", INK, "4 L × 2 · ısıtma")
    kesik(X_K, 320.0, 540.0, 140.0, 330.0, "K KARTI", INK, "tahrik")
    satirlar(fx(X_K + W_K / 2), fy(690.0), "taban dolabı 123–1060|yedek kutu YOK (Kemal 24 Eyl)", f7, GRAY, 17)
    d.line([(fx(X_K), fy(H_B)), (fx(X_K + W_K), fy(H_B))], fill=LINE, width=4)
    d.rectangle([fx(X_K + 20), fy(PL), fx(X_K + W_K - 20), fy(PL - 14.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_K + W_K / 2), fy(PL - 34.0), "KESME PLAKASI 560 × 450 · üstü %s" % sayi(PL), f7, BUZ, "mm")
    d.rectangle([fx(X_K + 24), fy(PL + 50.0), fx(X_K + 64), fy(PL + 2.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_K + 44), fy(PL + 66.0), "İTİCİ", f7, INK, "mm")
    kesik(X_K, 110.0, 490.0, PL + 90.0, PL + 340.0, "YILDIZ BIÇAK Ø300 · 6 dilim", INK, "piston 100 strok")
    d.ellipse([fx(X_K + 520) - 6, fy(PL + 120.0) - 6, fx(X_K + 520) + 6, fy(PL + 120.0) + 6], fill=RED)
    txt(fx(X_K + 520), fy(PL + 150.0), "SPREY", f7, RED, "mm")
    kapak(X_K, 33.0, W_K - 33.0, PL + 355.0, 2028.0, "İÇECEK + TATLI YEDEĞİ · 4 GÜN|97 kutu 330 ml (2 kat × 115) + 8 tatlı|çekmece 180 + yedek 97 = 277 = 4 gün")
    modul_etiketi(X_K, W_K, "MODÜL K · KESME", "600 × 830 × 2030 · plaka %s" % sayi(PL))
    olcu_h(fx(X_K), fx(X_K + W_K), fy(H_MAK) - 26, sayi(W_K), f11, INK)


def ciz_E():
    """kutu_cad_v3 · E-yerel x 0..830 · kotlar mutlak"""
    a0, a1 = 1085.0, 1330.0                                   # ön alt kapak üstü · ağız üst kirişi altı
    kabin(X_E, W_E, 0.0, H_MAK, "E · KUTU KATLAMA · standart 32 × 32 × 4,2 kutu")
    kapak(X_E, 2.0, W_E - 2.0, Y_ALT + 3.0, a0)
    kesik(X_E, 8.0, 812.0, 240.0, 1148.0, "KUTU ŞARJÖRÜ · arkada · asansörlü", INK,
          "açılım 804 × 404 · yığın 908 = 567 kutu (1,6 mm) · 504 (1,8)|Tr16×4 vida + NEMA 23 · dolum sağ yan kapaktan|tahrik tabanın altında (koruyuculu)")
    agiz(X_E, 2.0, W_E - 2.0, a0, a1, "KUTULAMA AĞZI · robot çatalı tepsiden alır")
    d.rectangle([fx(X_E + 100), fy(TEPSI_E), fx(X_E + 420), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(X_E + 100), fy(TEPSI_E + 42.0), fx(X_E + 420), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(fx(X_E + 260), fy(TEPSI_E + 21.0), "kutu 320 × 42 · tepsi %s (4 çubuk)" % sayi(TEPSI_E), f7, INK, "mm")
    kesik(X_E, 440.0, 800.0, 797.0, 1148.0, "KAPAK MASASI + U FLAP KATLAYICI", INK, "kapak kolu R166 · SureGear 10:1")
    txt(fx(X_E + 46), fy(1188.0), "PİZZA", f7, RED, "mm"); txt(fx(X_E + 46), fy(1170.0), "sol duvar", f7, RED, "mm")
    drect(fx(X_E + 1), fy(1230.0), fx(X_E + 12), fy(1146.0), RED, 2)
    kapak(X_E, 2.0, W_E - 2.0, 1345.0, 2028.0)
    kesik(X_E, 100.0, 828.0, 1472.0, 1540.0, "BESLEYİCİ İTİCİ · 1500 · strok 411", INK)
    kesik(X_E, 112.0, 408.0, 1560.0, 2010.0, "PİSTON SFU1610", INK, "taban · kilit · kapak bastırma")
    kesik(X_E, 450.0, 780.0, 1565.0, 2025.0, "PANO · arkada", INK, "S7-1200|7 step sürücü")
    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KATLAMA (kutu_cad_v3)", "830 × 830 × 2030 · tepsi %s · ağız %s–%s" % (sayi(TEPSI_E), sayi(a0), sayi(a1)))
    olcu_h(fx(X_E), fx(X_E + W_E), fy(H_MAK) - 26, sayi(W_E), f11, INK)
    return a0, a1, 908.0


''')

# ---------------------------------------------------------------- 4) plan: K ve E modelden, tabla ekseni −170
degis('''    # K
    d.rectangle([fx(X_K + 20), py(-495.0), fx(X_K + 580), py(-45.0)], fill=EVC, outline=BUZ, width=2)
    d.ellipse([fx(X_K + 300 - 150), py(-420.0), fx(X_K + 300 + 150), py(-120.0)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - 150 * S * math.cos(a), py(-270.0) - 150 * S * math.sin(a)), (fx(X_K + 300) + 150 * S * math.cos(a), py(-270.0) + 150 * S * math.sin(a))], fill=INK, width=1)
    txt(fx(X_K + 300), py(-540.0), "KESME PLAKASI 560 × 450 · yıldız bıçak Ø300", f7, BUZ, "mm")
    d.rectangle([fx(X_K + 26), py(-310.0), fx(X_K + 62), py(-230.0)], fill=BG, outline=INK, width=2)
    d.line([(fx(X_K + 470), py(-270.0)), (fx(X_E + 170), py(-270.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 170), py(-270.0)), (fx(X_E + 150), py(-270.0) - 7), (fx(X_E + 150), py(-270.0) + 7)], fill=INK)
    # E
    drect(fx(X_E + 150), py(-785.5), fx(X_E + 550), py(-25.5), GRAY, 1)
    txt(fx(X_E + 350), py(-700.0), "BLANK 400 × 760 · altta", f7, GRAY, "mm")
    d.rectangle([fx(X_E + 190), py(-430.0), fx(X_E + 510), py(-110.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_E + 350), py(-285.0), "KUTU", f8, INK, "mm")
    txt(fx(X_E + 350), py(-258.0), "320 × 320 × 45", f7, GRAY, "mm")''',
      '''    # K (v8 · montaj: plaka z −470…−20, bıçak ve sprey ürün ekseninde z −170)
    d.rectangle([fx(X_K + 20), py(-470.0), fx(X_K + 580), py(-20.0)], fill=EVC, outline=BUZ, width=2)
    d.ellipse([fx(X_K + 300 - 150), py(ZT - 150.0), fx(X_K + 300 + 150), py(ZT + 150.0)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - 150 * S * math.cos(a), py(ZT) - 150 * S * math.sin(a)), (fx(X_K + 300) + 150 * S * math.cos(a), py(ZT) + 150 * S * math.sin(a))], fill=INK, width=1)
    txt(fx(X_K + 300), py(-520.0), "KESME PLAKASI 560 × 450 · yıldız bıçak Ø300", f7, BUZ, "mm")
    d.rectangle([fx(X_K + 26), py(ZT - 40.0), fx(X_K + 62), py(ZT + 40.0)], fill=BG, outline=INK, width=2)
    d.line([(fx(X_K + 470), py(ZT)), (fx(X_K + 560), py(-206.0)), (fx(X_E + 90), py(-206.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 90), py(-206.0)), (fx(X_E + 70), py(-206.0) - 7), (fx(X_E + 70), py(-206.0) + 7)], fill=INK)
    txt(fx(X_K + 600), py(40.0) + 52, "K itici pizzayı 36 mm içeri kaydırıp E'ye iter (ürün ekseni −170 → kutu ekseni −206)", f7, RED, "mm")
    # E (v8 · kutu_cad_v3)
    drect(fx(X_E + 8), py(-819.0), fx(X_E + 812), py(-415.0), GRAY, 1)
    txt(fx(X_E + 410), py(-617.0), "ŞARJÖR · açılım 804 × 404 · 567 kutu · y 240–1148", f7, GRAY, "mm")
    d.rectangle([fx(X_E + 100), py(-366.0), fx(X_E + 420), py(-46.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_E + 260), py(-219.0), "KUTU", f8, INK, "mm")
    txt(fx(X_E + 260), py(-192.0), "320 × 320 × 42", f7, GRAY, "mm")
    drect(fx(X_E + 440), py(-368.0), fx(X_E + 800), py(-26.0), GRAY, 1)
    txt(fx(X_E + 620), py(-197.0), "kapak masası", f7, GRAY, "mm")
    d.line([(fx(X_E + 1), py(-372.0)), (fx(X_E + 1), py(-24.0))], fill=RED, width=4)''')

# ---------------------------------------------------------------- 5) KESİT 2 · E (kutu_cad_v3)
blok_degis("def kesit_E(P, a0, a1):", "def parca_listesi(satirlar_):", r'''def kesit_E(P, a0, a1):
    z = sec(SX2)
    txt(SX2, FY_TOP - 200, "KESİT 2 · E + ROBOT + QR DOLABI", f16, ACC)
    txt(SX2, FY_TOP - 162, "Robot kapalı kutuyu tepsinin çubukları arasından çatalla alır, QR gözüne koyar · E: kutu_cad_v3", f9, GRAY)
    govde(z, 0.0, H_MAK, True)
    d.rectangle([z(-819.0), fy(1148.0), z(-415.0), fy(240.0)], fill=BG, outline=GRAY, width=1)
    satirlar(z(-617.0), fy(700.0), "KUTU ŞARJÖRÜ|567 kutu · y 240–1148|asansör Tr16 + NEMA 23", f7, GRAY, 16)
    drect(z(-430.0), fy(Y_ALT), z(-354.0), fy(100.0), ACC, 1)
    txt(z(-392.0), fy(80.0), "tahrik · tabanın altında", f7, ACC, "mm")
    d.line([(z(-819.0), fy(1500.0)), (z(-408.0), fy(1500.0))], fill=INK, width=3)
    d.polygon([(z(-408.0), fy(1500.0)), (z(-428.0), fy(1500.0) - 7), (z(-428.0), fy(1500.0) + 7)], fill=INK)
    txt(z(-614.0), fy(1500.0) - 16, "besleyici 1500 · strok 411", f7, INK, "mm")
    d.rectangle([z(-374.0), fy(1150.0), z(-32.0), fy(1140.0)], fill=SOFT, outline=INK, width=1)
    d.rectangle([z(-366.0), fy(TEPSI_E), z(-46.0), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([z(-366.0), fy(TEPSI_E + 42.0), z(-46.0), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(z(-206.0), fy(TEPSI_E + 21.0), "kutu 320 × 42", f7, INK, "mm")
    d.rectangle([z(-10.0), fy(a1), z(40.0), fy(a0)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(a1) - 14, "KUTULAMA AĞZI %s–%s" % (sayi(a0), sayi(a1)), f7, RED, "rm")
    drect(z(-394.0), fy(2010.0), z(-58.0), fy(1560.0), GRAY, 1)
    txt(z(-226.0), fy(1785.0), "PİSTON SFU1610", f7, GRAY, "mm")
    drect(z(-826.0), fy(2025.0), z(-740.0), fy(1565.0), GRAY, 1)
    txt(z(-783.0), fy(2045.0), "pano", f7, GRAY, "mm")
    ty = TEPSI_E - 9.0
    D = robot_kesit(z, 230.0, ty + 20.0, -206.0, ty, "ROBOT")
    d.line([(z(-366.0), fy(ty)), (z(-46.0), fy(ty))], fill=ACC, width=4)
    txt(z(-206.0), fy(ty) + 16, "çatal · tepsi çubukları arasında · kutu ekseni z −206", f7, ACC, "mm")
    d.rectangle([z(QRZ[0]), fy(2000.0), z(QRZ[1]), fy(0.0)], fill=FILL, outline=LINE, width=4)
    for yy in QR_SATIR:
        d.rectangle([z(QRZ[0]), fy(yy + 190.0), z(QRZ[0] + 440.0), fy(yy)], fill=EVC, outline=BUZ, width=1)
        txt(z(QRZ[0] + 220.0), fy(yy + 95.0), "göz · y %s" % sayi(yy), f7, BUZ, "mm")
    txt(z((QRZ[0] + QRZ[1]) / 2), fy(2000.0) - 16, "QR DOLABI · 6 satır", f8, INK, "mm")
    olcu_h(z(40), z(QRZ[0]), fy(0) + 84, "koridor + pay %s" % sayi(QRZ[0] - 40.0), f8, GRAY)
    for yy in (Y_ALT, 240.0, a0, TEPSI_E, 1148.0, a1, 1500.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    return D


''')

# ---------------------------------------------------------------- 6) TABLALI pafta gövdesi (A · B · C · F · K · E · plan · kesit 1 · liste)
blok_degis("def tablali():", 'if __name__ == "__main__":', r'''def tablali():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    P = P_SUREC                                              # çalışma diski üstü 1168 = süreç kotu (topping_cad_v22: 1060 + 108)
    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v8 · HD  ·  MONTAJ = hat_montaj_v41  ·  TOPPING = topping_cad_v22 · E = kutu_cad_v3 · B = store_cad_v4  ·  ALT TABAN 123 · SÜREÇ 1168  ·  HAT 5430 × 2030 × 830",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  2 gün stok  ·  her istasyon kapalı ürün  ·  bütün gövdeler yerden 123'te başlar, istasyon tabanları 1060  ·  ürün tepsisiz: hamur topu çalışma diskinde KONİLİ AÇICI ile açılır, dozajlanır, bıçak burunlu bant fırına çeker → kesme plakası → kutu  ·  TOPPING'de şimdilik 2 kaset: kaşar + küp sucuk (Codex adayları)  ·  TEK Fairino FR5 yer rayında · omuz 970 · ray ekseni hat yüzünden 360  ·  ölçüler mm  ·  25 Eylül 2026")
    # ---- A · AÇICI (topping_cad_v22: kolon x 290–410 · koniler 1176–1264 · kafa plakası 1310–1322)
    kabin(X_A, W_A, H_B, H_MAK, "A · KONİLİ DÖNER AÇICI · tabla altında bekler")
    kapak(X_A, 33.0, 667.0, H_B + 3.0, 2010.0)
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot TOP halinde bırakır")
    _kx = X_A + 350.0
    for _y in (1.0, -1.0):
        d.polygon([(fx(_kx), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 96.0))], outline=INK)
    kesik(X_A, 270.0, 430.0, 1310.0, 1322.0, "", INK)
    drect(fx(X_A + 290.0), fy(1440.0), fx(X_A + 410.0), fy(H_B), INK, 1)
    satirlar(fx(X_A + 350.0), fy(1700.0), "AÇICI · kolon x 290–410 · 1060–1440|kafa plakası 160 × 680 × 12 · kot 1310|Z kızağı strok 60 · Ø32 pnömatik|2 KONİ · boy 140 · taban Ø90 · yarım açı 17,82°|2 × NEMA23 + planet · ters yönde döner", f7, INK, 17)
    modul_etiketi(X_A, W_A, "MODÜL A · KONİLİ AÇICI", "700 × 830 × 970 · B üstünde")
    olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)
    ciz_B()
    # ---- C · TOPPING (topping_cad_v22 · modül yereli + 700 = hat, + 1060 = kot)
    kabin(X_C, W_C, H_B, H_MAK, "C · TOPPING · tablalı dozaj (topping_cad_v22)")
    TEK = (145.0, 2585.0, 1061.5, 1091.5); RAY = (200.0, 2485.0, 1080.5, 1095.5); KAS = (165.0, 2535.0)
    d.rectangle([fx(TEK[0]), fy(TEK[3]), fx(TEK[1]), fy(TEK[2])], fill=SOFT, outline=LINE, width=2)
    d.rectangle([fx(RAY[0]), fy(RAY[3]), fx(RAY[1]), fy(RAY[2])], fill=BG, outline=INK, width=2)
    for _kx in KAS:
        d.ellipse([fx(_kx) - 9.55 * S, fy(1093.0) - 9.55 * S, fx(_kx) + 9.55 * S, fy(1093.0) + 9.55 * S], fill=BG, outline=ACC, width=2)
    d.rectangle([fx(2507.0), fy(1121.0), fx(2563.0), fy(1064.0)], fill=BG, outline=INK, width=2)
    txt(fx(2535.0), fy(1140.0), "X MOTORU", f7, INK, "mm")
    d.rectangle([fx(180.0), fy(P), fx(520.0), fy(1157.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(200.0), fy(1118.5), fx(500.0), fy(1108.5)], fill=ACC, outline=ACC)
    txt(fx(1250.0), fy(1128.0), "TABLA ARABASI · strok 1987 (x 350 → 2337) · HGR15 ray 2285 · GT3 kapalı çevrim · tekne 1061–1091 · tabla Ø340 + çalışma diski · üstü %s · ekseni z −170" % sayi(P), f7, ACC, "mm")
    d.rectangle([fx(2504.0), fy(BANT_F), fx(2926.0), fy(1103.0)], fill=EVC, outline=BUZ, width=1)
    txt(fx(2715.0), fy(1088.0), "AKTARMA BANDI · bıçak burunlu", f7, BUZ, "mm")
    # soğuk kabin (PU 1250–1760) + kaset sırası 1320–1680 + nozullar 1220–1310
    d.rectangle([fx(730.0), fy(1760.0), fx(2470.0), fy(1250.0)], fill=PUC, outline=GRAY, width=1)
    d.rectangle([fx(790.0), fy(1700.0), fx(2410.0), fy(1310.0)], fill=BG, outline=LINE, width=2)
    txt(fx(1600.0), fy(1730.0), "SOĞUK KABİN +3 °C · PU 60 · ön kapak 1294–1706 (modelde açık) · kaset tabanı 1320", f7, GRAY, "mm")
    TAKILI = {"KAŞAR KABI": "Codex v15|ADAY", "KÜP SUCUK": "Codex V2|ADAY"}
    YV = [("HARÇ 1", 956.5, 1238.5, 280), ("HARÇ 2", 1241.5, 1523.5, 280), ("KIYMA", 1526.5, 1668.5, 140),
          ("KUŞBAŞI", 1671.5, 1813.5, 140), ("KAŞAR KABI", 1816.5, 2098.5, 280), ("KÜP SUCUK", 2101.5, 2243.5, 140)]
    NOZ = {"HARÇ 1": (1086.0, 1394.0), "KIYMA": (1578.0, 1617.0), "KUŞBAŞI": (1713.0, 1772.0), "KAŞAR KABI": (1932.0, 1983.0), "KÜP SUCUK": (2148.0, 2197.0)}
    for ad, x0, x1, g in YV:
        if ad in TAKILI:
            d.rectangle([fx(x0 + 4), fy(1680.0), fx(x1 - 4), fy(1320.0)], fill=BG, outline=INK, width=3)
            satirlar(fx((x0 + x1) / 2), fy(1540.0), "%s|%s" % (ad.replace(" ", "|") if g < 200 else ad, TAKILI[ad]), f7, INK, 16)
        else:
            drect(fx(x0 + 4), fy(1680.0), fx(x1 - 4), fy(1320.0), GRAY, 1)
            satirlar(fx((x0 + x1) / 2), fy(1520.0), "%s|boş" % ad, f7, GRAY, 16)
        if ad in NOZ:
            n0, n1 = NOZ[ad]
            (d.rectangle([fx(n0), fy(1310.0), fx(n1), fy(1220.0)], fill=BG, outline=INK, width=2) if ad in TAKILI
             else drect(fx(n0), fy(1310.0), fx(n1), fy(1220.0), GRAY, 1))
    txt(fx(1600.0), fy(1200.0), "nozullar yalıtımdan 1220'ye iner · kaşar 1932–1983 · sucuk 2148–2197 · pide üstü 1176", f7, INK, "mm")
    # üst bant 1772–2012: soğutma · güç · sürücüler · pano · UPS · evaporatör arkada
    kesik(X_C, 60.0, 360.0, 1772.0, 1992.0, "SOĞUTMA GRUBU", INK)
    kesik(X_C, 400.0, 463.0, 1772.0, 1897.0, "", INK)
    txt(fx(X_C + 431.0), fy(1915.0), "güç", f7, INK, "mm")
    kesik(X_C, 605.0, 996.0, 1776.0, 1821.0, "SÜRÜCÜLER × 12", INK)
    kesik(X_C, 1100.0, 1500.0, 1772.0, 2012.0, "PANO", INK, "PLC · röleler")
    kesik(X_C, 1520.0, 1569.0, 1772.0, 1894.0, "", INK)
    txt(fx(X_C + 1545.0), fy(1912.0), "UPS", f7, INK, "mm")
    d.rectangle([fx(X_C + 33), fy(2027.0), fx(X_C + W_C - 33), fy(1987.0)], fill=PUC, outline=GRAY, width=1)
    txt(fx(X_C + W_C / 2), fy(2007.0), "üst kapak PU 40", f7, GRAY, "mm")
    modul_etiketi(X_C, W_C, "MODÜL C · TOPPING (tablalı · 6 yuva, şimdilik 2 kaset: kaşar + küp sucuk)", "1800 × 830 × 970 · B üstünde · disk %s" % sayi(P))
    olcu_h(fx(X_C), fx(X_C + W_C), fy(H_MAK) - 26, sayi(W_C), f11, INK)
    # ---- F K E
    ciz_F([(60.0, 700.0, 135.0, 270.0, "ROBOT KONTROL KUTUSU · ray yanında", "245 × 180 × 45"),
           (60.0, 460.0, 320.0, 670.0, "ANA PANO · PLC · ana şalter", "400 × 350 × 250 · ekran yok → tablet"),
           (480.0, 730.0, 320.0, 670.0, "UPS", "500 VA"),
           (760.0, 1230.0, 135.0, 865.0, "BULAŞIK MAKİNESİ · tezgâh altı", "MEIKO M-iClean UM sınıfı · 460 × 600 × 730|sepet 500 × 500 · giriş 315 · 40 sepet/saat"),
           (1250.0, 1440.0, 135.0, 500.0, "MAKİNE DETERJANI + PARLATICI", "2 × 5 L bidon · seviye şamandıralı"),
           (1250.0, 1440.0, 520.0, 865.0, "BOŞ", "190 × 770 × 345")])
    ciz_K()
    a0, a1, yig = ciz_E()
    birlesimler()
    kot_cizgileri((Y_ALT, H_B, TEPSI_E, P, 1320.0, 1486.0, 1680.0, 1772.0, H_MAK))
    # ---- PLAN
    plan_ortak(P, "tabla")
    d.ellipse([fx(180.0), py(ZT - 170.0), fx(520.0), py(ZT + 170.0)], fill=EVC, outline=BUZ, width=2)
    txt(fx(350.0), py(ZT - 190.0), "TABLA Ø340 · park · z −170", f7, BUZ, "mm")
    d.rectangle([fx(730.0), py(-630.0), fx(2470.0), py(-104.0)], outline=GRAY, width=1)
    for ad, x0, x1, g in YV:
        if ad in TAKILI:
            d.rectangle([fx(x0 + 4), py(-525.0), fx(x1 - 4), py(-200.0)], fill=BG, outline=INK, width=2)
            satirlar(fx((x0 + x1) / 2), py(-380.0), "%s|%s" % (ad, TAKILI[ad].split(" · ")[0]), f7, INK, 16)
        else:
            drect(fx(x0 + 4), py(-525.0), fx(x1 - 4), py(-200.0), GRAY, 1)
            satirlar(fx((x0 + x1) / 2), py(-380.0), "%s|boş" % ad, f7, GRAY, 16)
    txt(fx(1600.0), py(-630.0) - 14, "soğuk kabin (z −104…−630) · kasetler z −200…−525 · tahrik motorları arkada kuru bölmede (z −630…−830)", f7, GRAY, "mm")
    dline((fx(350.0), py(ZT)), (fx(2337.0), py(ZT)), ACC, 3, 12, 6)
    for xt in (1957.5, 2337.0):
        darc(fx(xt), py(ZT), 170.0 * S, 0.0, 360.0, BUZ, 2, 4.0)
    drect(fx(2504.0), py(-315.0), fx(2926.0), py(-25.0), BUZ, 2)
    txt(fx(2715.0), py(-5.0) + 14, "aktarma bandı", f7, BUZ, "mm")
    txt(fx(1350.0), py(ZT) + 24, "TABLA HATTI z −170 = fırın bandı ekseni · park x 350 → fırın ağzı x 2337 · HGR15 ray x 200–2485 (tabanın altında)", f7, ACC, "mm")
    txt(fx(1350.0), py(-790.0) - 40, "UYARI · tekne modül C'nin sağ kenarını 85 mm, sağ kasnak 35 mm aşıyor; sol ucu modül A'nın içinde (x 145) — İSTASYON = KAPALI ÜRÜN kuralına aykırı, KARAR BEKLİYOR", f7, RED, "mm")
    # ---- KESİT 1 · A + B (K1) + ROBOT
    z = sec(SX1)
    txt(SX1, FY_TOP - 200, "KESİT 1 · A + B (K1) + ROBOT", f16, ACC)
    txt(SX1, FY_TOP - 162, "Robot hamur TOPUNU ağızdan çalışma diskinin ortasına bırakır · kafa iner, koniler döner, hamur Ø280'e açılır", f9, GRAY)
    govde(z, 0.0, H_B, True)
    d.rectangle([z(-760), fy(B_TABAN), z(-2), fy(Y_ALT + 1.5)], fill=PUC, outline=GRAY, width=1)
    cekmeceler(z, KOLON[0], YUZ0)
    txt(z(-340), fy(560.0), "K1 · TAZE PİDE × 6 · çekmece 680 · açılım 628", f7, DOLAP, "mm")
    govde(z, H_B, H_MAK)
    d.rectangle([z(-415.0), fy(1091.5), z(-5.0), fy(1061.5)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([z(-315.0), fy(1118.5), z(-25.0), fy(1108.5)], fill=ACC, outline=ACC)
    d.rectangle([z(-340.0), fy(P), z(0.0), fy(1157.0)], fill=EVC, outline=BUZ, width=2)
    txt(z(-170.0), fy(1040.0), "tabla Ø340 + disk · üstü %s · z −170 · altında araba + ray + tekne" % sayi(P), f7, BUZ, "mm")
    d.polygon([(z(-324.0), fy(1176.0)), (z(-16.0), fy(1176.0)), (z(-16.0), fy(1264.0)), (z(-324.0), fy(1264.0))], outline=INK)
    txt(z(-170.0), fy(1220.0), "2 koni", f7, INK, "mm")
    d.rectangle([z(-500.0), fy(1322.0), z(180.0), fy(1310.0)], fill=SOFT, outline=RED, width=2)
    d.rectangle([z(88.0), fy(1308.0), z(167.0), fy(1235.0)], fill=BG, outline=RED, width=2)
    drect(z(-660.0), fy(1440.0), z(-490.0), fy(H_B), INK, 1)
    txt(z(-575.0), fy(1460.0), "açıcı kolonu · Z kızağı 60", f7, INK, "mm")
    satirlar(z(-160.0), fy(1900.0), "UYARI · açıcının kafa plakası ve ön koni motoru|gövdenin 180 mm önüne taşıyor (modeldeki hali)", f7, RED, 17)
    d.rectangle([z(-10.0), fy(P + 220.0), z(40.0), fy(P)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(P + 235.0), "HAMUR AĞZI %s–%s" % (sayi(P), sayi(P + 220.0)), f7, RED, "rm")
    D1 = robot_kesit(z, -170.0 + 232.5, P + 100.0, -170.0, P + 100.0, "ROBOT")
    d.ellipse([z(-170.0) - 47.5 * S, fy(P + 100.0) - 47.5 * S, z(-170.0) + 47.5 * S, fy(P + 100.0) + 47.5 * S], fill=URUN, outline=(180, 140, 70), width=2)
    for yy in (Y_ALT, B_TABAN, H_B, P, P + 220.0, 1440.0, H_MAK):
        d.line([(z(-790) - 24, fy(yy)), (z(-790) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-790) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    D2 = kesit_E(P, a0, a1)
    parca_listesi([
        ("MODÜL A", "KONİLİ DÖNER AÇICI · 2 koni (boy 140 · taban Ø90 · yarım açı 17,82°) · 2 × NEMA23 + planet · Z kızağı strok 60 · Ø32 pnömatik", "1", "700 × 830 × 970 · 40–160 N · örs YOK · UYARI: kafa plakası + ön motor gövdenin 180 mm önünde"),
        ("MODÜL B", "ÇEKMECE modülü (store_cad_v4) · 21 motorlu çekmece (Transmotec PD3665 + GT3 kayış + Accuride DZ3832 3 parçalı ray · strok 628) · K4: Secop CU soğutma + 2 × GN depo + temizlik nişi · K1 üstü pano", "1", "2500 × 830 × 1060 · gövde 123'ten (ayak + süpürgelik) · yalıtımlı taban 123–164,5"),
        ("MODÜL C", "TOPPING (topping_cad_v22) · 6 kaset yuvası, şimdilik 2 kaset takılı: KAŞAR KABI (v14 + Codex v15 aday) + KÜP SUCUK (v7 + Codex V2 aday) · soğuk kabin 1250–1760 · altında tabla arabası", "1", "1800 × 830 × 970 · disk üstü 1168 · UYARI: tekne sağa 85, kasnak 35 mm taşıyor"),
        ("TABLA ARABASI", "Ø340 tabla + ÇALIŞMA DİSKİ Ø340 × 8 (pimli) · HGR15 x kızağı · pancake dönüş motoru · açıcı altı → kasetler → fırın ağzı", "1", "kaldırma YOK · park yeri AÇICININ ALTI · tabla ekseni z −170"),
        ("X TAHRİK", "GT3 KAPALI ÇEVRİM kayış · 2 × 20 diş kasnak x 165 ve 2535 · araba bütün strokta kayışa bağlı · gergi sol kasnak plakasından", "1", "strok 1987 (x 350 → 2337) · HGR15 ray 2285 (x 200–2485), 2 sıra · tekne 2440"),
        ("X MOTORU", "NEMA23 kapalı çevrim step, TEKNENİN ARKASINDA · mili servis cebinden sağ kasnağa girer", "1", "1,2 N·m · gereken 0,382 → 3,14 kat pay · sürtünme 10 N VARSAYIM"),
        ("BANDA AKTARMA", "BIÇAK BURUNLU · bant Ø20 burun silindirine dolanır, üst yüzü diskin 2 mm altı (1166) · pide boşluğu kendi gövdesiyle köprüler", "1", "itici ve köprü YOK · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf bant"),
        ("MODÜL F", "KONVEYÖR FIRIN · özel · elektrikli · hazne 1400 · aynı anda 4 ürün · taban dolabı: robot kontrol, ana pano, UPS, bulaşık makinesi, deterjan", "1", "1500 × 830 × 2030 · gövde 1060–1486 · bant 1166 · AÇIK: bant altı pay 106 (alt ısıtma)"),
        ("MODÜL K", "KESME · plaka 560 × 450 (z −470…−20) + yıldız bıçak Ø300 6 dilim + tereyağı spreyi + itici · taban dolabı: yağ kartuşu + K kartı", "1", "600 × 830 × 2030 · plaka üstü 1164 · yedek kutu YOK · E için şart: itici 36 mm içeri kaydırır"),
        ("MODÜL E", "KUTU KATLAMA (kutu_cad_v3) · standart 32 × 32 × 4,2 E-dalga · şarjör arkada, asansörlü · besleyici 1500 · zımba kalıbı + 4 çubuklu tepsi · köprü · piston SFU1610 · devirme parmağı · U flap katlayıcı · kapak kolu · 7 × NEMA 23", "1", "830 × 830 × 2030 · gövde 123'ten · tepsi 1104 · şarjör 567 kutu (2 gün = 560)"),
        ("ROBOT", "Fairino FR5 · TEK ROBOT · yer rayında · omuz 970 · hamur: çekmece → tabla · kutu (çatal) → QR · içecek + tatlı", "1", "bilek mesafesi: tabla %d · kutu %d (sınır %d)" % (round(D1), round(D2), round(ERISIM))),
        ("RAY", "yer rayı · tek araba · ekseni hat yüzünden 360", "1", "araba merkezi x 200 – %s" % sayi(HAT - 200.0)),
        ("QR DOLABI", "2 × 6 göz · göz 480 × 190 × 440 · koridorun karşısında, hattın sağ ucunda", "1", "x %s–%s · ayrıntı SERVİS_TESLİM paftası" % (sayi(QRX[0]), sayi(QRX[1]))),
        ("BULAŞIK MAKİNESİ", "TEZGÂH ALTI · MEIKO M-iClean UM sınıfı · sepet 500 × 500 · giriş 315 · 40 sepet/saat", "1", "460 × 600 × 730 · F taban dolabında (123–1060) · KASET YATIRILARAK yıkanır · çalışma diski Ø340 düz yatar"),
        ("YEDEK STOK", "İÇECEK 97 kutu + 8 tatlı (K üst bölme, 2 kat) · KUTU yedeği YOK: şarjör 567 kutu = 2 gün", "", "robotun erişiminde DEĞİL — eleman günlük olarak ana gözlere aktarır"),
        ("TEMİZLİK", "deterjan · bez · eldiven · poşet: B modülü K4 temizlik nişi (2 × 5 L bidon) · makine deterjanı + parlatıcı: bulaşık makinesinin yanında", "", "dükkânda yalnız LAVABO kalır"),
        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: F taban dolabı · TOPPING'in kendi panosu üst bantta · ekran yok (tablet)", "", ""),
    ])
    lejant()
    yol = KLASOR + r"\HAT_ATOSA_TABLALI_v8_HD.png"
    im.save(yol, dpi=(int(200 * K_HD), int(200 * K_HD))); print("yazildi:", yol, "· hat", sayi(HAT), "· bilek", round(D1), round(D2))
    return yol


''')

# ---------------------------------------------------------------- 7) yalnız tablalı pafta + ekran/site kopyaları
s = s[:s.index('if __name__ == "__main__":')]
degis("    gen = 2860", "    gen = 2790")
s = s.rstrip() + '''


if __name__ == "__main__":
    import os
    # v8: yalnız TABLALI pafta (bantlı v6'ya dokunulmaz) · HD + ekran (7990) + site (4200) kopyaları
    yol = tablali()
    hd = Image.open(yol)
    for gen, hedef in ((7990, KLASOR + r"\\HAT_ATOSA_TABLALI_v8_EKRAN.png"),
                       (4200, os.path.join(KLASOR, "..", "..", "otonom", "hat", "img", "HAT_ATOSA_TABLALI_v8_teknik.png"))):
        k = hd.resize((gen, int(hd.size[1] * gen / hd.size[0])), Image.LANCZOS)
        k.save(os.path.normpath(hedef), optimize=True); print("yazildi:", os.path.normpath(hedef), k.size)
'''
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v8.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v8.py yazildi")
