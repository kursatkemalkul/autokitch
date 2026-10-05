# -*- coding: utf-8 -*-
"""store_cad_v4 -> v5 (25 Eyl 2026): ALT KISIM v3 DAĞILIMI + TAM KAPLAYAN KAPAKLAR
Kemal: "çekmeceleri genişlet, kapaklarını, kapalı gözüksün temiz · bu şekilde en son halini tekrar modelle" ·
"soğukta her şey 2 gün · kaşar + sucuk 4 gün saklanır (depo silinmez)".
  · KAPAKLAR TAM KAPLAMA: kolon kapakları arası 3 mm, B'nin iki yanı ve bölmeler kapak arkasında kalır; her kolonda
    en alt ön 126'dan, en üst ön 1057'ye iner/çıkar → bütün kolonlar aynı alt ve üst çizgide. Gövde ön kenarları
    (yan, tavan, taban) z −40'a çekildi (kapak z −40…0 onların önünde). Kolon sınırları 700 / 1355 / 2010 (A|C 700 ile aynı).
  · DAĞILIM (pafta ALT_KISIM_v3): K1 5 pide + 2 lahmacun + tatlı · K2 3 pide + 5 lahmacun · K3 5 lahmacun + 2 içecek
    (tek kat) · K4 Secop (arkasında PLC) · ara PU · KAŞAR + SUCUK DEPOSU (GN 1/1-100 + GN 1/2-100) · 2 dar içecek.
  · İÇECEK TEK KAT (robot her kutuya erişir): şerit + yaylı market iticisi, geniş 6 × 8 = 48 · dar 4 × 8 = 32.
    TATLI: 5 şerit × 6 = 30 (kap Ø95 × 60 VARSAYIM).
  · PLC + güç + sürücü + röle (25) K1 üstünden K4'e, Secop'un ARKASINA (ara sac perde ile ayrılır).
  · K1 teknik bölmesi, K2 üst paneli, temizlik nişi (F tabanına gitti) kalktı. K4 soğuk bölmesine 4. roll-bond evaporatör + fan.
  · BOM 1_STORE_v8.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v4.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:100])
    s = s.replace(a, b)


degis('''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v4 (25 Eyl 2026)''',
      '''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v5 (25 Eyl 2026)
v5: TAM KAPLAYAN KAPAKLAR (aralar 3, alt 126 / üst 1057 çizgisi) + ALT KISIM v3 dağılımı (içecek tek kat, tatlı,
    K4 kaşar + sucuk deposu + dar içecek) + PLC Secop'un arkasında. Önceki: store_cad_v4.py (yap_store_cad_v5.py)''')
# ---- dağılım
degis('''HH, CAP, KOLON, KOLON_AD = _g["HH"], _g["CAP"], _g["KOLON"], _g["KOLON_AD"]''',
      '''HH, CAP, KOLON, KOLON_AD = _g["HH"], _g["CAP"], _g["KOLON"], _g["KOLON_AD"]
# v5 · ALT KISIM v3 (Kemal 25 Eyl: soğukta her şey 2 gün; içecek tek kat → robot her kutuya erişir)
HH = dict(HH); HH.update({"ic1": 126.0, "ic1d": 126.0, "tatli": 71.0})       # kutu 115 / tatlı kabı 60 + 11 taban payı
KOLON = [[(5, "hamur"), (2, "lahm"), (1, "tatli")], [(3, "hamur"), (5, "lahm")], [(5, "lahm"), (2, "ic1")]]
K4_CEK = [(2, "ic1d")]
KAPAK_X = {"K1": (0.0, 698.5), "K2": (701.5, 1353.5), "K3": (1356.5, 2008.5), "K4": (2011.5, 2500.0)}   # tam kaplama, aralar 3
ON_ALT, ON_UST = 126.0, 1057.0                   # bütün kolonlarda ön yüzün alt ve üst çizgisi
GN_H = 230.0                                      # K4 kaşar + sucuk deposu yüksekliği (GN 1/1-100 + raf + GN 1/2-100)''')
degis('''TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0}''',
      '''TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0, "ic1": 660.0, "ic1d": 660.0, "tatli": 660.0}
TATLI = dict(r=47.5, h=60.0, ax=104.0, az=97.0, nz=6)          # tatlı kabı Ø95 × 60 [VARSAYIM] · şerit 104
K4_YO = 123.0 + 1.5 + 4.0 + 272.0 + 8.0 + 30.0 + GN_H + 1.0 + 3.0 + 15.0      # K4 ilk dar çekmece açıklığı 687,5''')
degis('''        cx += WO + BOLME
    return out, cx''',
      '''        cx += WO + BOLME
    yo, n = K4_YO, {}                                                    # v5 · K4 dar çekmeceler (depo üstünde)
    for adet, tip in K4_CEK:
        for _ in range(adet):
            n[tip] = n.get(tip, 0) + 1
            out.append(("K4", "CEK_K4_%s_%d" % (tip, n[tip]), tip, cx, yo))
            yo += HH[tip] + 2 * BIND + FUGA
    return out, cx''')
degis('''CEK, K4X = kolonlar()
K4W = 400.0''',
      '''CEK, K4X = kolonlar()
K4W = 400.0
GEN = lambda kol: K4W if kol == "K4" else WO
ALT_KOD = {min((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in ("K1", "K2", "K3")}
UST_KOD = {max((c for c in CEK if c[0] == k), key=lambda c: c[4])[1] for k in ("K1", "K2", "K3", "K4")}''')
# ---- çekmece: genişlik + tam kaplama ön
degis('''    h = HH[tip]; x1 = x0 + WO; y1 = yo + h; xc = x0 + WO / 2.0''',
      '''    wo = GEN(kol); h = HH[tip]; x1 = x0 + wo; y1 = yo + h; xc = x0 + wo / 2.0''')
degis('''    kapak_on(kod + "_on", x0 - BIND, x1 + BIND, yo - BIND, y1 + BIND, kod, (x0, x1, yo, y1), grup=G,
             bom=("Çekmece önü 40 · kulpsuz", 1, "dış 304 1,5 bükme + PU 37,5 köpük + iç 304 1,0 (fitil kanallı)", "%d × %d" % (WO + 2 * BIND, h + 2 * BIND)))''',
      '''    pa, pb = KAPAK_X[kol]                                               # v5 · TAM KAPLAMA
    pc = ON_ALT if kod in ALT_KOD else yo - BIND
    pd = ON_UST if kod in UST_KOD else y1 + BIND
    kapak_on(kod + "_on", pa, pb, pc, pd, kod, (x0, x1, yo, y1), grup=G,
             bom=("Çekmece önü 40 · kulpsuz · tam kaplama", 1, "dış 304 1,5 bükme + PU 37,5 köpük + iç 304 1,0 (fitil kanallı)", "%.0f × %.0f" % (pb - pa, pd - pc)))''')
# ---- içerik: tek kat içecek / tatlı (şerit + yaylı itici)
degis('''    r = ICECEK["r"]; ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_TUB1 - 13.0''',
      '''    if tip in ("ic1", "ic1d", "tatli"):                                   # v5 · TEK KAT, ŞERİTLİ, YAYLI İTİCİLİ
        tat = tip == "tatli"
        r = TATLI["r"] if tat else ICECEK["r"]; hk = TATLI["h"] if tat else ICECEK_KAT
        px = TATLI["ax"] if tat else ICECEK["ax"]; pz = TATLI["az"] if tat else 2.0 * r
        nz = TATLI["nz"] if tat else 8
        ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_TUB1 - 13.0
        nx = int((ix1 - ix0 - 12.0 - 2 * r) // px) + 1
        xm = (ix0 + ix1) / 2.0
        X = [xm + (i - (nx - 1) / 2.0) * px for i in range(nx)]
        Z = [iz1 - 3.0 - r - j * pz for j in range(nz)]                 # itici ürünü öne dayar: robot hep öndekini alır
        y0 = kc + 1.0
        for i in range(nx + 1):
            xd = xm + (i - nx / 2.0) * px
            ekle("%s_serit_bolmesi_%d" % (kod, i), kut(xd - 0.5, xd + 0.5, y0, y0 + 50.0, iz0, iz1), "plastik", kod, grup=G,
                 bom=("Şerit bölmesi + yaylı itici takımı (market tipi)", nx, "standart raf itici sistemi · şerit %.0f · ürünü öne iter" % px,
                      "marka seçilmedi [VARSAYIM] · çekmece başına %d şerit" % nx) if i == 0 else None)
        zb = Z[-1] - r - 3.0
        for i, a in enumerate(X):
            ekle("%s_itici_%d" % (kod, i), kut(a - px / 2.0 + 4.0, a + px / 2.0 - 4.0, y0, y0 + (45.0 if tat else 70.0), zb - 12.0, zb), "plastik", kod, grup=G)
            ekle("%s_itici_yayi_%d" % (kod, i), kut(a - 6.0, a + 6.0, y0 + 2.0, y0 + 8.0, iz0, zb - 12.0), "celik", kod, grup=G)
        urun = sily(0.0, 0.0, r, 0.0, hk)
        n = 0
        for a in X:
            for b in Z:
                ekle("%s_%s_%d" % (kod, "tatli" if tat else "kutu330", n), urun.translate((a, y0, b)), "hamur" if tat else "kutu_icecek", kod, grup=G); n += 1
        return n, y0 + hk, y1
    r = ICECEK["r"]; ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_TUB1 - 13.0''')
# ---- gövde ön kenarları z −40'a (kapaklar önlerinde)
degis('''        ekle("yan_dis_sac_" + ad_, kut(dis_x[0], dis_x[1], Y_PLINT, H_B, -DZ, 0.0), "sac", B, bom=("Yan dış sac 1,5", 2, "304 lazer + büküm", "") if ad_ == "sol" else None)
        ekle("yan_pu_" + ad_, kut(pu_x[0], pu_x[1], Y_PLINT + 1.5, H_B - 1.5, -DZ + 1.5, -1.5), "pu", B)
        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN if ad_ == "sol" else Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, -1.5), "sac", B)   # v4: sağda K4 sıcak bölmesinin tabanına iner
        ekle("yan_on_donus_" + ad_, kut(don_x[0], don_x[1], Y_PLINT + 1.5, H_B - 1.5, -1.5, 0.0), "sac", B)''',
      '''        ekle("yan_dis_sac_" + ad_, kut(dis_x[0], dis_x[1], Y_PLINT, H_B, -DZ, -40.0), "sac", B, bom=("Yan dış sac 1,5", 2, "304 lazer + büküm · ön kenar kapak arkasında (z −40)", "") if ad_ == "sol" else None)
        ekle("yan_pu_" + ad_, kut(pu_x[0], pu_x[1], Y_PLINT + 1.5, H_B - 1.5, -DZ + 1.5, -41.5), "pu", B)
        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN if ad_ == "sol" else Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, -41.5), "sac", B)   # v4: sağda K4 sıcak bölmesinin tabanına iner
        ekle("yan_on_donus_" + ad_, kut(don_x[0], don_x[1], Y_PLINT + 1.5, H_B - 1.5, -41.5, -40.0), "sac", B)''')
degis('''    ekle("tavan_dis_sac", kut(1.5, W_ - 1.5, H_B - 1.5, H_B, -DZ, 0.0), "sac", B, bom=("Tavan dış sacı", 1, "304 1,5 · A ve C bunun üstüne oturur", ""))
    ekle("tavan_pu_57.5", kut(29.0, W_ - 29.0, Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -1.5), "pu", B, bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 27,5 · tavan 57,5 · arka 37,5 · taban 39"))
    ekle("tavan_ic_sac", kut(X_IC0, X_IC1, Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -1.5), "sac", B)
    ekle("tavan_on_donus", kut(X_IC0, X_IC1, Y_TAVAN, H_B - 1.5, -1.5, 0.0), "sac", B)''',
      '''    ekle("tavan_dis_sac", kut(1.5, W_ - 1.5, H_B - 1.5, H_B, -DZ, -40.0), "sac", B, bom=("Tavan dış sacı", 1, "304 1,5 · A ve C bunun üstüne oturur", ""))
    ekle("tavan_pu_57.5", kut(29.0, W_ - 29.0, Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -41.5), "pu", B, bom=("PU köpük gövde", 1, "40 kg/m³ enjeksiyon · sac kabuk içine", "yan 27,5 · tavan 57,5 · arka 37,5 · taban 39"))
    ekle("tavan_ic_sac", kut(X_IC0, X_IC1, Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -41.5), "sac", B)
    ekle("tavan_on_donus", kut(X_IC0, X_IC1, Y_TAVAN, H_B - 1.5, -41.5, -40.0), "sac", B)''')
degis('''    ekle("taban_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, 0.0).cut(kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3])), "sac", B)''',
      '''    ekle("taban_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, -40.0).cut(kut(VENT[0], VENT[1], Y_PLINT - 1, Y_PLINT + 3, VENT[2], VENT[3])), "sac", B)''')
degis('''    ekle("taban_pu", kut(29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -1.5), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -1.5), "sac", B)
    ekle("taban_k4_kademe_saci", kut(K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -1.5), "sac", B,''',
      '''    ekle("taban_pu", kut(29.0, K4X - 1.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -41.5), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, K4X - 1.0, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -41.5), "sac", B)
    ekle("taban_k4_kademe_saci", kut(K4X - 1.0, K4X, Y_PLINT + 1.5, Y_TABAN, Z_ARKA, -41.5), "sac", B,''')
degis('''    ekle("taban_on_donus", kut(X_IC0, X_IC1, Y_PLINT + 1.5, Y_TABAN, -1.5, 0.0), "sac", B)''',
      '''    ekle("taban_on_donus", kut(X_IC0, X_IC1, Y_PLINT + 1.5, Y_TABAN, -41.5, -40.0), "sac", B)''')
# ---- K1 teknik bölmesi → kalkar (PLC K4'e, Secop'un arkasına)
a0 = s.index("    # K1 üstü KURU TEKNİK BÖLME")
a1 = s.index("    # KABLO KANALLARI: her kolonda arka sol dikey 40 × 25 · üstte yatay (bölmelerden geçer)")
s = s[:a0] + "    E = \"B_ELEKTRIK\"                                                 # v5: pano K4'te, Secop'un arkasında (aşağıda)\n" + s[a1:]
degis('''    for kol in KOLON_AD:
        cx = KOLON_X[kol]
        ekle("kablo_kanali_%s" % kol, kut(cx + KAN_X[0], cx + KAN_X[1], Y_TABAN, KAN_UST[0], KAN_Z[0], KAN_Z[1]),
             "kanal", Kb, bom=("Kablo kanalı 40 × 25", 3 + 1, "PVC perfore + kapak", "dikey her kolonda + üstte yatay") if kol == "K1" else None)
    ekle("kablo_kanali_ust", kut(K1X + KAN_X[1], KOLON_X["K3"] + KAN_X[1], KAN_UST[0], KAN_UST[1], KAN_Z[0], KAN_Z[1]), "kanal", Kb)''',
      '''    for kol in KOLON_AD:
        cx = KOLON_X[kol]
        ekle("kablo_kanali_%s" % kol, kut(cx + KAN_X[0], cx + KAN_X[1], Y_TABAN, KAN_UST[0], KAN_Z[0], KAN_Z[1]),
             "kanal", Kb, bom=("Kablo kanalı 40 × 25", 4 + 1, "PVC perfore + kapak", "dikey her kolonda + üstte yatay") if kol == "K1" else None)
    K4KAN = kut(K4X + KAN_X[0], K4X + KAN_X[1], 400.0, KAN_UST[0], KAN_Z[0], KAN_Z[1])            # v5 · PLC'den yukarı
    ekle("kablo_kanali_K4", K4KAN, "kanal", Kb)
    ekle("kablo_kanali_ust", kut(K1X + KAN_X[1], K4X + KAN_X[1], KAN_UST[0], KAN_UST[1], KAN_Z[0], KAN_Z[1]), "kanal", Kb)''')
degis('''    for kol in ("K1", "K2", "K3"):
        cx = KOLON_X[kol]
        e0, e1 = (250.0, 780.0) if kol == "K1" else (300.0, 950.0)''',
      '''    for kol in ("K1", "K2", "K3"):
        cx = KOLON_X[kol]
        e0, e1 = (300.0, 950.0)                                              # v5: K1'in üstünde teknik bölme yok''')
degis('''             bom=("Evaporatör roll-bond levha", 3, "alüminyum 1,5 + kanal · ölçüye üretim", "arka duvara yapışık · 310 × 530..650") if kol == "K1" else None)''',
      '''             bom=("Evaporatör roll-bond levha", 4, "alüminyum 1,5 + kanal · ölçüye üretim", "arka duvara yapışık · K1–K3 310 × 650 · K4 140 × 260") if kol == "K1" else None)''')
degis('''             bom=("Fan ebm-papst 4414 FNH", 3, "24 V · 119 × 119 × 25", "evaporatör önünde, havayı kolon içine basar") if kol == "K1" else None)''',
      '''             bom=("Fan ebm-papst 4414 FNH", 4, "24 V · 119 × 119 × 25", "evaporatör önünde, havayı kolon içine basar") if kol == "K1" else None)
    # v5 · K4 soğuk bölmesi (depo + dar çekmeceler) de soğutulur
    ekle("evaporator_K4", kut(K4X + 240.0, K4X + 380.0, 700.0, 960.0, Z_ARKA, Z_ARKA + 2.0), "aluminyum", "B_SOGUTMA")
    ekle("fan_K4", kut(K4X + 255.0, K4X + 374.0, 770.5, 889.5, Z_ARKA + 3.0, Z_ARKA + 28.0), "motor", "B_SOGUTMA")''')
# ---- K4: depo GN 1/1-100 + GN 1/2-100 · temizlik nişi kalkar · PLC Secop'un arkasında · ara perde
degis('''    ekle("k4_ara_sac_alt", kut(kx0, kx1, s0, s0 + 1.0, Z_ARKA, Z_CER0), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, kx1, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, kx1, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0), "sac", "B_SOGUTMA")
    d0 = s0 + 30.0; d1 = d0 + 300.0
    for j in range(2):
        gy = d0 + 5.0 + j * 150.0
        ekle("k4_depo_GN11_%d" % j, kut(kx0 + 37.5, kx1 - 37.5, gy, gy + 140.0, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, gy + 1.0, gy + 141.0, Z_CER0 - 539.0, Z_CER0 - 11.0)),
             "sac", "B_DEPO", bom=("GN 1/1-150 kap", 2, "304 · EN 631", "kaşar blok / sucuk (içerik VARSAYIM)") if j == 0 else None)
    ekle("k4_depo_raf", kut(kx0, kx1, d0 + 150.0, d0 + 151.5, Z_ARKA, Z_CER0), "sac", "B_DEPO")
    ekle("k4_nis_raf", kut(kx0, kx1, d1 + 3.0, d1 + 4.5, Z_ARKA, Z_CER0), "sac", "B_TEMIZLIK")
    for j in range(2):
        ekle("bidon_5L_%d" % j, sily(kx0 + 110.0 + j * 180.0, Z_CER0 - 180.0, 85.0, d1 + 4.5, d1 + 4.5 + 250.0), "pom", "B_TEMIZLIK",
             bom=("Temizlik bidonu 5 L", 2, "deterjan / dezenfektan", "") if j == 0 else None)
    KAP = [("k4_kapak_sogutma", Y_TABAN + 3.0, s0 + 12.0, "B_SOGUTMA", False), ("k4_kapak_depo", s0 + 15.0, d1 + 1.0, "B_DEPO", True),
           ("k4_kapak_nis", d1 + 4.0, Y_TAVAN - 3.0, "B_TEMIZLIK", True)]''',
      '''    ekle("k4_ara_sac_alt", kut(kx0, kx1, s0, s0 + 1.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, kx1, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0).cut(K4KAN), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, kx1, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_SOGUTMA")
    # v5 · PANO Secop'un ARKASINDA (K1 üstünden taşındı) · sıcak havadan ara sac perdeyle ayrılır
    ekle("k4_ara_perde", kut(kx0, kx1, Y_PLINT + 1.5, s0, -522.0, -521.0), "sac", "B_SOGUTMA",
         bom=("Ara sac perde 1,0", 1, "304 · Secop ile pano arasında", "yoğuşturucu havası panoya gelmez"))
    ZP = Z_ARKA + 2.0                                                  # montaj plakası arka duvarda, öne bakar
    ekle("pano_montaj_plakasi", kut(kx0 + 10.0, kx1 - 10.0, 132.0, 398.0, Z_ARKA, ZP), "sac", E, bom=("Pano montaj plakası 2 mm", 1, "galvaniz", "K4 · Secop'un arkasında"))
    for i_, yr in enumerate((177.5, 312.5)):
        ekle("din_ray_%d" % i_, kut(kx0 + 12.0, kx1 - 12.0, yr, yr + 35.0, ZP, ZP + 7.5), "celik", E, bom=("DIN ray TS35 × 7,5", 2, "", "") if i_ == 0 else None)
    zd = ZP + 7.5
    x = kx0 + 14.0; ty = 145.0
    ekle("plc_S7-1200_1214C", kut(x, x + 110.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · 14 DI · 10 DQ · PROFINET/Modbus TCP", "110 × 100 × 75")); x += 110.0
    for ad_, kodu in (("SM1221_DI16_a", "6ES7221-1BH32-0XB0"), ("SM1221_DI16_b", "6ES7221-1BH32-0XB0"), ("SM1222_DQ16", "6ES7222-1BH32-0XB0")):
        ekle("plc_" + ad_, kut(x, x + 45.0, ty, ty + 100.0, zd, zd + 75.0), "siemens", E,
             bom=("PLC genişleme %s" % ad_.split("_")[0] + " " + ad_.split("_")[1], 1, kodu, "45 × 100 × 75 · 50 reed + 25 röle")); x += 45.0
    x += 4.0
    ekle("guc_kaynagi_NDR-240-24", kut(x, x + 63.0, 132.5, 257.7, zd, zd + 113.5), "aluminyum", E,
         bom=("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · DIN", "63 × 125,2 × 113,5"))
    x = kx0 + 14.0; ty = 285.0
    ekle("surucu_EM-324C", kut(x, x + 72.0, ty, ty + 85.0, zd, zd + 60.0), "kart", E,
         bom=("DC motor sürücü Electromen EM-324C + DIN taban", 1, "10–35 V · 4 A · akım sınırı · NPN/PNP", "72 genişlik taban [yükseklik/derinlik VARSAYIM]")); x += 76.0
    for i in range(len(CEK)):
        ekle("role_%02d" % (i + 1), kut(x + i * 6.2, x + i * 6.2 + 6.0, ty + 5.0, ty + 85.0, zd, zd + 94.0), "kart", E,
             bom=("Seçici röle Phoenix Contact PLC-RSC-24DC/21", len(CEK), "6,2 mm · 1 değiştirici · 24 V bobin", "hangi çekmecenin motoru sürücüye bağlanacak [boyut VARSAYIM]") if i == 0 else None)
    x += len(CEK) * 6.2 + 4.0
    ekle("klemens_blogu", kut(x, kx1 - 14.0, ty + 15.0, ty + 70.0, zd, zd + 45.0), "plastik", E,
         bom=("Klemens bloğu", 1, "Phoenix UT 2,5 · 25 motor + 50 sensör + güç", "kalan genişlik"))
    d0 = s0 + 30.0; d1 = d0 + GN_H
    # v5 · KAŞAR + SUCUK DEPOSU (4 günün 2. yarısı): GN 1/1-100 (kaşar blok) · raf · GN 1/2-100 (küp sucuk)
    g0 = d0 + 5.0
    ekle("k4_depo_GN11_100", kut(kx0 + 37.5, kx1 - 37.5, g0, g0 + 100.0, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g0 + 1.0, g0 + 101.0, Z_CER0 - 539.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/1-100 kap + kapak", 1, "304 · EN 631 · 530 × 325 × 100", "kaşar blok 2 gün = 8,8 kg (yoğunluk VARSAYIM)"))
    ekle("k4_depo_raf", kut(kx0, kx1, g0 + 110.0, g0 + 111.5, Z_ARKA, Z_CER0).cut(K4KAN), "sac", "B_DEPO")
    g1 = g0 + 116.5
    ekle("k4_depo_GN12_100", kut(kx0 + 37.5, kx1 - 37.5, g1, g1 + 100.0, Z_CER0 - 275.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, g1 + 1.0, g1 + 101.0, Z_CER0 - 274.0, Z_CER0 - 11.0)),
         "sac", "B_DEPO", bom=("GN 1/2-100 kap + kapak", 1, "304 · EN 631 · 325 × 265 × 100", "küp sucuk 2 gün = 2,8 kg"))
    KAP = [("k4_kapak_sogutma", ON_ALT, s0 + 12.0, "B_SOGUTMA", False), ("k4_kapak_depo", s0 + 15.0, d1 + 1.0, "B_DEPO", True)]''')
degis('''        a_, b_ = kx0 - BIND, kx1 + BIND''', '''        a_, b_ = KAPAK_X["K4"]                                        # v5 · tam kaplama''')
degis('''    for i in range(int((PENCERE[3] - PENCERE[2] - 14.0) // 16.0)):''', '''    for i in range(int((PENCERE[3] - PENCERE[2] - 14.0) // 16.0)):       # (ızgara penceresi aynı)''')
# ---- K1 teknik kapak + K2 üst panel kalkar; çerçeve açıklıkları kolon genişliğiyle
degis('''    # K1 teknik bölme kapağı (kuru: fitilsiz) + K2 üstü sabit panel
    k2_ust = max(yo + HH[t] + BIND for kol, _k, t, x0, yo in CEK if kol == "K2")
    kapak_on("k1_teknik_kapak", K1X - BIND, K1X + WO + BIND, ry0, Y_TAVAN - 3.0, E, None, fitil=False)
    kapak_on("k2_ust_panel", KOLON_X["K2"] - BIND, KOLON_X["K2"] + WO + BIND, k2_ust + 3.0, Y_TAVAN - 3.0, B, None, fitil=False)
''', '''    # v5: K1 teknik kapağı ve K2 üst paneli yok — her kolonun en üst çekmece önü 1057'ye kadar kaplar
''')
degis('''        cer = cer.cut(kut(x0, x0 + WO, yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))''',
      '''        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))''')
degis('''    cer = cer.cut(kut(K1X, K1X + WO, ry0 + BIND, Y_TAVAN - 3.0 - BIND, Z_CER0 - 1, Z_CER1 + 1))
''', '')
degis('''bom=("Ön çerçeve sacı 1,0", 1, "304 lazer kesim · %d açıklık" % (len(CEK) + 4), "fitil buna basar"))''',
      '''bom=("Ön çerçeve sacı 1,0", 1, "304 lazer kesim · %d açıklık" % (len(CEK) + 2), "fitil buna basar"))''')
# ---- denetim
degis('''    print("B CEKMECE MODULU v4 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))''',
      '''    print("B CEKMECE MODULU v5 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))''')
degis('''    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin
    govde_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    bidon = max(yb("bidon_5L_0").ymax, yb("bidon_5L_1").ymax)
    print("ALT TABAN CIZGISI: govde alti %.1f (en alcak govde parcasi %.1f) · ic taban ustu %.1f · en alt cekmece onu %.1f (aralik %.1f) · K4 kapagi alti %.1f · bidon ustu %.1f / tavan %.1f"
          % (alt, govde_alt, ic_ust, on_alt, on_alt - ic_ust, k4_alt, bidon, Y_TAVAN))
    assert abs(alt - 123.0) < 0.05 and abs(govde_alt - alt) < 0.05, "govde alti 123 degil"
    assert abs(on_alt - ic_ust - FUGA) < 0.05 and abs(k4_alt - on_alt) < 0.05, "on alt kenarlari hizali degil"
    assert bidon <= Y_TAVAN - 3.0, "K4 nisinde bidon tavana degiyor"''',
      '''    k4_alt = yb("k4_kapak_sogutma_dis_sac").ymin
    govde_alt = min(p["wp"].val().BoundingBox().ymin for p in PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    print("ALT TABAN CIZGISI: govde alti %.1f (en alcak govde parcasi %.1f) · ic taban ustu %.1f · en alt on %.1f · K4 kapagi alti %.1f"
          % (alt, govde_alt, ic_ust, on_alt, k4_alt))
    assert abs(alt - 123.0) < 0.05 and abs(govde_alt - alt) < 0.05, "govde alti 123 degil"
    assert abs(on_alt - ON_ALT) < 0.05 and abs(k4_alt - ON_ALT) < 0.05, "on alt kenarlari 126 cizgisinde degil"
    # v5 · ÖN YÜZ IZGARASI: her kolonda önler 126 → 1057 arası 3 mm aralıkla kesintisiz; kolonlar arası 3 mm
    on = [p["wp"].val().BoundingBox() for p in PARCALAR if p["ad"].endswith(("_dis_sac_1.5", "_dis_sac")) and ("CEK_" in p["ad"] or p["ad"].startswith("k4_kapak"))]
    for kol, (pa, pb) in KAPAK_X.items():
        sut = sorted((b for b in on if abs(b.xmin - pa) < 0.05 and abs(b.xmax - pb) < 0.05), key=lambda b: b.ymin)
        assert sut and abs(sut[0].ymin - ON_ALT) < 0.05 and abs(sut[-1].ymax - ON_UST) < 0.05, "%s: on yuz 126-1057 degil" % kol
        for u_, v_ in zip(sut, sut[1:]):
            assert abs(v_.ymin - u_.ymax - FUGA) < 0.05, "%s: onler arasi %.1f (3 olmali)" % (kol, v_.ymin - u_.ymax)
        print("   ON YUZ %s: x %.1f-%.1f · %d parca · %.0f-%.0f · aralar 3" % (kol, pa, pb, len(sut), sut[0].ymin, sut[-1].ymax))
    xs = sorted(KAPAK_X.values())
    assert all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and xs[0][0] == 0.0 and xs[-1][1] == W_B, "kolon onleri arasi 3 degil"''')
degis('''    pay = {t: min(a - u for _k, tt, _n, u, a in ozet if tt == t) for t in ("hamur", "lahm", "icecek")}
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t == "icecek")
    print("ICERIK PAYI (acikliga): pide %.1f · lahmacun %.1f · icecek %.1f mm" % (pay["hamur"], pay["lahm"], pay["icecek"]))
    print("KAPASITE: pide %d top (2 gun = 160) · lahmacun %d top (2 gun = 400) · icecek %d kutu (pafta 180)" % (pide, lahm, ice))
    assert pide >= 160 and lahm >= 400''',
      '''    tipler = sorted({t for _k, t, _n, _u, _a in ozet})
    pay = {t: min(a - u for _k, tt, _n, u, a in ozet if tt == t) for t in tipler}
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t in ("ic1", "ic1d")); tat = sum(n for _k, t, n, _u, _a in ozet if t == "tatli")
    print("ICERIK PAYI (acikliga): " + " · ".join("%s %.1f" % (t, pay[t]) for t in tipler) + " mm")
    print("KAPASITE: pide %d top (2 gun = 160) · lahmacun %d top (2 gun = 400) · icecek %d kutu TEK KAT (2 gun = 139) · tatli %d (4 gun = 22)" % (pide, lahm, ice, tat))
    assert pide >= 160 and lahm >= 400 and ice >= 139 and tat >= 22
    ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "CEKMECE" and "_on_" not in p["ad"])
    print("EN UST CEKMECE ICERIGI/KUTUSU %.1f · tavan %.1f" % (ust, Y_TAVAN)); assert ust <= Y_TAVAN - 2.0''')
degis('''    L = [(p, p["wp"].val()) for p in PARCALAR if "_top_" not in p["ad"] and "_kutu330_" not in p["ad"]]''',
      '''    L = [(p, p["wp"].val()) for p in PARCALAR if "_top_" not in p["ad"] and "_kutu330_" not in p["ad"] and "_tatli_" not in p["ad"]]''')
degis('''        if "_top_" in p["ad"] or "_kutu330_" in p["ad"]:
            continue''', '''        if "_top_" in p["ad"] or "_kutu330_" in p["ad"] or "_tatli_" in p["ad"]:
            continue''')
degis('''    (r"^fan_K[23]$", "ebm-papst 4414 FNH"), (r"^ayak_[1-5]$", "Elesa LV.A-SST"), (r"^bidon_5L_1$", "bidon"), (r"^k4_depo_GN11_1$", "GN 1/1"),''',
      '''    (r"^fan_K[234]$", "ebm-papst 4414 FNH"), (r"^evaporator_K4$", "roll-bond evaporatör"), (r"^ayak_[1-5]$", "Elesa LV.A-SST"), (r"^din_ray_1$", "DIN ray"),
    (r"_serit_bolmesi_([1-9]|1\\d)$", "şerit + itici takımı"), (r"_itici(_yayi)?_\\d+$", "şerit + itici takımı"), (r"^kablo_kanali_K4$", "kablo kanalı"),''')
degis('''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v7")))''',
      '''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v8")))''')
degis('''"Elesa", "GT3", "M12", "Fitil", "GN 1/1", "DIN", "Klemens", "Kablo kanalı", "bidonu", "PLC")) else "ÜRETİM"''',
      '''"Elesa", "GT3", "M12", "Fitil", "GN 1/", "DIN", "Klemens", "Kablo kanalı", "itici", "PLC")) else "ÜRETİM"''')
io.open(os.path.join(U, "store_cad_v5.py"), "w", encoding="utf-8").write(s)
print("store_cad_v5.py yazildi")
