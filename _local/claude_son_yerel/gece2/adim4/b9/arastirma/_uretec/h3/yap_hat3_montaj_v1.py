# -*- coding: utf-8 -*-
"""h2/hat2_montaj_v1.py → h3/hat3_montaj_v1.py (HAT VERSİYON 3 · ilk sürüm) — metin yaması, her değişiklik sayısı denetlenir.
v1 (hat_montaj_vNN) ve v2 (hat2_montaj_v1) DOKUNULMAZ; v3 ayrı dosya, ayrı çıktı klasörü (otonom/hat3d/v3), ayrı sayfa (makine_v3.html)."""
import io, os, re, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
KAYNAK = os.path.join(U, "h2", "hat2_montaj_v1.py"); HEDEF = os.path.join(H3, "hat3_montaj_v1.py")
s = io.open(KAYNAK, encoding="utf-8").read()
N = [0]


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, "yama bulunamadı (%d ≠ %d): %r" % (c, n, a[:140])
    s = s.replace(a, b); N[0] += 1


# ---- 0 · başlık ----
rep('''"""hat2_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 2''',
    '''"""hat3_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 3 — Kemal HAT v2.7 ("bunu da v3 olarak kur · harçla sosun çıkışı sola gitmesin,
direkt aşağıya insin, o aralarından en uygun şekilde · sorunları çöz ama basit çözümler, kompleksleştirmeden temiz"). Kaynak: v2 montajı hat2_montaj_v1
(yap_hat3_montaj_v1.py metin yaması) + h3_* üreteçleri (h3_hesap_v1 tek sayı kaynağı):
  · A 700 AYNI, 736–1436 · TOPPING 1436–2500 (sol duvar kıymanın dibinde) · üst katta YALNIZ sos + harç UNO · sos / harç çıkışı DİK iner: yayıcılar alt kat
    dozajlayıcılarının arasında (sos 1645 · harç 2160), ağız kaset iniş borularıyla aynı kotta (1047, pide koridoru 1033) · hat 4494 (v2 4722,5 · v1 5230)
  · dolap 736–4400: K'nın altına uzar · 21 çekmece (2 gün) + TEKNİK SÜTUN (Secop + pano + kaşar / sucuk soğuk deposu, K'nın altında) · çöp E'nin altında
  · K dolabın üstünde (alt dolap yok) · yağ tenekesi + tartı fırın üstünde sağda (kompresör 241 sola) · pompa grubu K'nın üst önünde

--- v2 başlığı ---
hat2_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 2''')
# ---- 1 · yollar + modüller h2 → h3 ----
rep('''sys.path.insert(0, os.path.join(U, "h2"))   # v2: dosya h2/ içinde''', '''sys.path.insert(0, os.path.join(U, "h3"))   # v3: dosya h3/ içinde''')
rep('''OUT = os.path.join(KOK, "otonom", "hat3d", "v2");''', '''OUT = os.path.join(KOK, "otonom", "hat3d", "v3");''')
for a in ("h2_hesap_v1", "h2_ray_ek_v1", "h2_kaide_v1", "h2_tc_v1", "h2_store_v1", "h2_acici_v1", "h2_ust_depo_v1", "h2_kutu_v1", "h2_moduler_v1", "h2_ist_v1", "h2_topping_v1"):
    n = s.count(a); assert n >= 1, a
    s = s.replace(a, a.replace("h2_", "h3_")); N[0] += 1
rep('''os.path.join(U, "h2", "h2_tu_v1.py")''', '''os.path.join(U, "h3", "h3_tu_v1.py")''')
rep('''os.path.join(U, "h2", "_denetim_topping_v1.json")''', '''os.path.join(U, "h3", "_denetim_topping_v1.json")''')
rep('''os.path.join(U, "h2", "_supurme_topping_v1.json")''', '''os.path.join(U, "h3", "_supurme_topping_v1.json")''')
rep('''"h2/h3_topping_v1.py''', '''"h3/h3_topping_v1.py''')
rep('''import kesme_cad_v11 as KS ''', '''import h3_kesme_v1 as KS ''')
rep('''import firin_ust_kabin_cad_v1 as FU ''', '''import h3_firin_ust_v1 as FU ''')
rep('''import firin_tp10_cad_v10 as FT ''', '''import firin_tp10_cad_v10 as FT
FT.KOMP_ACIKLIK = (HS.KOMP_ACIKLIK_X[0], HS.KOMP_ACIKLIK_X[1], FT.KOMP_ACIKLIK[2], FT.KOMP_ACIKLIK[3])   # v3 · raf açıklığı kompresörle 241 sola (h3_hesap_v1) ''')
# ---- 2 · kompresör + hava hattı (fırın üstünde 241 sola) ----
rep('''KOMP_KAY = (-510.0, 976.0, 0.0) ''', '''KOMP_KAY = (-510.0 + HS.KOMP_DX, 976.0, 0.0)   # v3 · tank 3359–3739 (v2 3600–3980) ''')
rep('''ANA_V44 = [(3090, 1977, -380), (3090, 1977, -740), (1785, 1977, -740)''', '''ANA_V44 = [(3090 + HS.KOMP_DX, 1977, -380), (3090 + HS.KOMP_DX, 1977, -740), (1785, 1977, -740)''')
rep('''ANA_K48 = [(3090, 1977, -432), (3090, 1977, -770), (3294, 1977, -770)]''', '''ANA_K48 = [(3090 + HS.KOMP_DX, 1977, -432), (3090 + HS.KOMP_DX, 1977, -770), (3294, 1977, -770)]   # v3 · kompresör vanası 3549''')
# ---- 3 · K: fırın üstü sağ yan sacında yağ hortumu geçişleri (h3_kesme_v1) ----
rep('''KS.modul()
K_BIRIM = [''', '''KS.modul()
for _fad, _fkes, _fnot in KS.F_DUVAR_DELIKLERI:                                             # v3 · yağ emiş / dönüş hortumu fırın üstü kabinin sağ yan sacından K'ya geçer
    _fp = [p_ for p_ in FU.PARCALAR if p_["ad"] == _fad]; assert len(_fp) == 1, _fad
    _fp[0]["wp"] = cq.Workplane(obj=FU.dunya(_fp[0]).cut(_fkes))
K_BIRIM = [''')
rep('''("K_GOVDE", "KESME istasyonu gövdesi K400: 304 kabuk · köşe dikmeleri · taban 123 · istasyon tabanı 892 · 3 ön kapak (tava 20, ön düzlem +79) · v89: yağ tenekesi + tartı + pompa grubu ALT dolapta",''',
    '''("K_GOVDE", "KESME istasyonu gövdesi K400 (v3: ALT DOLAP YOK — dolabın teknik sütunu üstünde): 304 kabuk · köşe dikmeleri · taban 788 · istasyon tabanı 892 · ön alt bant sacı + 2 ön kapak (tava 20, ön düzlem +79)",''')
rep('''    ("K_YAG", "SIVI YAĞ sistemi (v89): Spraying Systems gıda PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD ÜRÜN GİRİŞİNDE SABİT (ısıtıcı yok) · ALT dolapta standart 18 L yağ tenekesi "''',
    '''    ("K_YAG", "SIVI YAĞ sistemi (v89 · v3 yerleşim): Spraying Systems gıda PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD ÜRÜN GİRİŞİNDE SABİT (ısıtıcı yok) · FIRIN ÜSTÜNDE sağda standart 18 L yağ tenekesi "''')
rep('''"SMC PFA 10 × 8 hortum sağdan nozüle · damlama tavası",''', '''"SMC PFA 10 × 8 hortum sağdan nozüle · damlama tavası · v3: pompa grubu K'nın üst önünde, emiş / dönüş F|K duvarından (y 1828)",''')
# ---- 4 · E altı: robot çöpü (h3_kutu_v1) ----
rep('''E_BIRIM += [(k_, a_, KC.E_ALT_ONEK[k_]) for k_, a_ in (
    ("E_ALT_SOGUTMA", "v2 · B DOLABININ SOĞUTMASI E'nin altında: Secop NLE8.8CN R290 yoğuşma ünitesi + buharlaştırma tavası (dolabın yoğuşma suyu) · önden panjurlu emiş / atış, arada perde · soğutma hatları 2–4,5 m (dolum soğutmacıda)"),
    ("E_ALT_PANO", "v2 · B DOLABININ PANOSU E'nin altında: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + seçici röleler (v1: dolabın K4 kolonu)"))]''',
    '''E_BIRIM += [(k_, a_, KC.E_ALT_ONEK[k_]) for k_, a_, _o in KC.E_ALT_BIRIM]                  # v3 · robot çöpü E'nin sol altında (E_COP)''')
rep('''    if kod in ("B_SOGUTMA", "E_ALT_SOGUTMA"): return "SOGUTMA"                                     # v2: B'nin yoğuşma ünitesi E'nin altında
    if kod == "E_ALT_PANO": return "KONTROL"''', '''    if kod == "B_SOGUTMA": return "SOGUTMA"                                                        # v3: dolabın yoğuşma ünitesi kendi teknik sütununda
    if kod == "E_COP": return "GOVDE"                                                               # v3: robot çöpü E'nin altında (v2 B_COP gibi, adına göre ayrılır)''')
rep('''"K_BANT", "K_KESICI", "F_YUKLEME", "B_COP", "HAVA_KOMPRESOR"))''', '''"K_BANT", "K_KESICI", "F_YUKLEME", "B_COP", "E_COP", "HAVA_KOMPRESOR"))''')
rep('''    ("v58 · B_COP robot copu kapagi + klapesi yerinde (v63: store_cad_v14 13 parca)", (float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])), 13.0)),''',
    '''    ("v3 · robot copu E'nin altinda: E_COP 7 parca (kova + kizak + poset + oluk + klape + mentese + yaprak) · dolapta B_COP 0",
     (float(len([p for p in KC.PARCALAR if p["ad"].startswith("ecop_")])), float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])) + 7.0, 7.0)),''')
# ---- 5 · dolap (h3_store_v1) · istasyon sırası · sözleşme ----
rep('''ISTASYON_SIRA = ("CEK_K3_hamur_3", "CEK_K1_lahm_4", "CEK_K6_ic1_1", "CEK_K5_tatli_1")''', '''ISTASYON_SIRA = ("CEK_K3_hamur_3", "CEK_K1_lahm_4", "CEK_K6_ic1_1", "CEK_K6_tatli_1")   # v3 · tatlı K6'nın altında''')
rep('''    ("v2 · dolap: SC.W_B = W_B = 3492,5 (507,5–4000)", (SC.W_B, W_B, 3492.5)),
    ("v2 · hat boyu: HAT_W - X_A = 4722,5 (v1 5230)", (HAT_W - X_A, HS.HAT_BOY, 4722.5)),''',
    '''    ("v3 · dolap: SC.W_B = W_B = 3664 (736–4400 · K'nın altına uzar)", (SC.W_B, W_B, 3664.0)),
    ("v3 · hat boyu: HAT_W - X_A = 4494 (v2 4722,5 · v1 5230)", (HAT_W - X_A, HS.HAT_BOY, 4494.0)),''')
rep('''("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 507,5–4000 · 21 çekmece)", X_A, W_B)''',
    '''("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 736–4400 · 21 çekmece + K altında teknik sütun)", X_A, W_B)''')
rep('''    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "h3_store_v1.py (store_cad_v14 · K4 dilimi çıktı)", "")''',
    '''    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "h3_store_v1.py (v3 dolap · store_cad_v14 çekmeceleri · teknik sütun K altında)", "")''')
# ---- 6 · TOPPING birimi ----
rep('''birim("TOPPING_MODUL", "TOPPING İKİ KATLI (v2): ALT KAT kıyma · kuşbaşı UNO + kaşar · küp sucuk kaseti · ÜST KAT sos + harç UNO (Ø32 hortumla yayıcılara) + kaşar / sucuk 2 gün yedeği (GN) · "''',
    '''birim("TOPPING_MODUL", "TOPPING İKİ KATLI (v3): ALT KAT kıyma · kuşbaşı UNO + kaşar · küp sucuk kaseti · ÜST KAT YALNIZ sos + harç UNO · sos / harç hortumu DİK iner, yayıcılar alt kat dozajlayıcılarının arasında (sos 1645 · harç 2160) · "''')
rep('''"h3/h3_topping_v1.py (topping_cad_v32 + topping_uno_cad_v19 parçaları, iki katlı)", "hat/makine_v2.html")''',
    '''"h3/h3_topping_v1.py (topping_cad_v32 + topping_uno_cad_v19 parçaları, iki katlı · v3)", "hat/makine_v3.html")''')
rep('''_dis_birim(UD, "GERCEK_UST", "h3_ust_depo_v1.py", "hat/makine_v2.html")''', '''_dis_birim(UD, "GERCEK_UST", "h3_ust_depo_v1.py", "hat/makine_v3.html")''')
rep('''"Yer rayı · tek araba · x %.1f–%.0f (v2: sol ucu A ile 507,5 kısaldı)"''', '''"Yer rayı · tek araba · x %.1f–%.0f (v3: sol ucu A ile 736 kısaldı)"''')
rep('''(istasyon siniri 1207,5)''', '''(istasyon siniri 1436)''')
# ---- 7 · çıktılar ----
for a, b in (("hat2_v1.glb", "hat3_v1.glb"), ("hat2_v1.usdz", "hat3_v1.usdz"), ('"hat2_v1"', '"hat3_v1"')):
    n = s.count(a); assert n >= 1, a
    s = s.replace(a, b); N[0] += 1
rep('''V2_DENETIM = ("Denetim (v2.1): TOPPING statik''', '''V2_DENETIM = ("Denetim (v3.1): TOPPING statik''')
rep('''surum="v2.1", pafta="HAT v2.1 (30 Eyl · Claude · YEREL): VERSİYON 2 — ''',
    '''surum="v3.1", pafta="HAT v3.1 (30 Eyl · Claude · YEREL): VERSİYON 3 — Kemal HAT v2.7: A 700 AYNI (736–1436) · TOPPING 1436–2500, üst katta YALNIZ sos + harç UNO, '''
    '''sos / harç DİK iner (yayıcılar alt kat dozajlayıcılarının arasında, ağız 1047) · dolap 736–4400: 21 çekmece + K altında teknik sütun (Secop + pano + kaşar / sucuk deposu) · '''
    '''robot çöpü E altında · K dolabın üstünde · yağ tenekesi fırın üstünde (kompresör 241 sola), pompa grubu K üstünde · hat 4494 · || v2.1 = VERSİYON 2 — ''')
# ---- 8 · kaset dönüş süpürmesi: UNO nokta istasyonları da dozaj hesabındaki GERÇEK taraftan (TARAF: kıyma +1 sağ · kuşbaşı −1 sol) ----
rep('''        if _i2["tip"] == "NOKTA": _IST.append((_i2["kod"].lower(), _x2 - _d2["r_dis"], _x2 + _d2["r_dis"]))                   # iki yan (v81 ile aynı, temkinli)
''', '''        # v3: NOKTA istasyonları da tabla_x (TARAF) ile — v81'de iki yan temkinli alınıyordu; v3'te TOPPING sol duvarı kıymanın dibinde (1436):
        #     kıymada tabla yalnız SAĞA açılır (1616 → 1708), sola hiç gitmez (makine_kodu / sim aynı TARAF tablosunu kullanır)
''')
rep('''        else: _IST.append((_i2["kod"].lower(), X_BC + _TH2.tabla_x(_i2, _d2["r_dis"]), X_BC + _TH2.tabla_x(_i2, _d2["r_ic"])))''',
    '''        _IST.append((_i2["kod"].lower(), X_BC + _TH2.tabla_x(_i2, _d2["r_dis"]), X_BC + _TH2.tabla_x(_i2, _d2["r_ic"])))''')
io.open(HEDEF, "w", encoding="utf-8").write(s)
print("hat3_montaj_v1.py yazıldı · %d yama" % N[0])
