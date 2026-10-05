# -*- coding: utf-8 -*-
"""hat_montaj_v92.py → hat2_montaj_v1.py (HAT VERSİYON 2 · ilk sürüm) — metin yaması, her değişiklik sayısı denetlenir.
v1 zinciri (hat_montaj_vNN) DOKUNULMAZ; v2 ayrı dosya, ayrı çıktı klasörü (otonom/hat3d/v2), ayrı sayfa (makine_v2.html)."""
import io, os, sys
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
KAYNAK = os.path.join(U, "hat_montaj_v92.py"); HEDEF = os.path.join(H2, "hat2_montaj_v1.py")   # v2 montajı h2/ içinde (iş kapsamı)
s = io.open(KAYNAK, encoding="utf-8").read()
N = [0]


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, "yama bulunamadı (%d ≠ %d): %r" % (c, n, a[:120])
    s = s.replace(a, b); N[0] += 1


# ---- 0 · başlık ----
rep('''"""hat_montaj_v92 (30 Eyl 2026 · Claude · base = topping v32 üstü v91)''',
    '''"""hat2_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 2 — İKİ KATLI TOPPING, DAR HAT (4722,5 · v1 5230) · makine üstü 2200.
Kemal: "bu birinci versiyon olsun … daha az geniş ve biraz daha yüksek … versiyon iki … topping istasyonunu iki raflı yaptık ki azalsın genişlik …
içecek yedeklerini yukarı taşıyabilirsin … çekmeceleri iki günlük ihtiyaca göre … saçma sapan mantık hataları yapma". Kaynak: v1 montajı hat_montaj_v92
(yap_hat2_montaj_v1.py metin yaması) + h2_* üreteçleri (h2_hesap_v1 tek sayı kaynağı). SAĞ TARAF (F · K · E · QR · robot evi) v1 ile AYNI dünya x'inde;
SOL TARAF 507,5 sağa (A 507,5–1207,5 · TOPPING 1207,5–2500 · dolap 507,5–4000: K4 kolonu çıktı). Yeni: E altında B soğutması + panosu, üstte ÜST DEPO (U).

--- v1 başlığı ---
hat_montaj_v92 (30 Eyl 2026 · Claude · base = topping v32 üstü v91)''')
# ---- 1 · yollar + çıktı klasörü ----
rep('''U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d"); STEP = os.path.join(KOK, "arastirma", "FULL_MAKINE")''',
    '''U = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U); sys.path.insert(0, os.path.join(U, "h2"))   # v2: dosya h2/ içinde, U = _uretec
OUT = os.path.join(KOK, "otonom", "hat3d", "v2"); STEP = os.path.join(KOK, "arastirma", "FULL_MAKINE")   # v2: ayrı klasör (v1 hat3d'ye DOKUNMAZ)
import h2_hesap_v1 as HS''')
# ---- 2 · kotlar + genişlikler ----
rep('''H_MAK = 1862.0                                # makine üstü (bütün istasyonlar)
W_B = 4000.0                                  # çekmeceli dolap TEK PARÇA 0–4000''',
    '''H_MAK = 1862.0                                # istasyon üstü (A · F · K · E) — v2: makine üstü H_UST
H_UST = HS.H_UST                              # v2 · makine üstü 2200 = iki katlı TOPPING = üst depo (U) üstü
W_B = HS.W_B                                  # v2 · çekmeceli dolap TEK PARÇA 507,5–4000 (3492,5 · K4 kolonu çıktı)''')
rep('''X_A, W_A, X_BC, W_BC = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"]                     # A 0-700 · C 700-2500 · v57: W_B yukarıda (4000)''',
    '''X_A, W_A, X_BC, W_BC = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"]                     # A 0-700 · C 700-2500 · v57: W_B yukarıda (4000)
X_A = HS.A_X[0]                                                                          # v2 · A 507,5–1207,5 · X_BC 700 = TOPPING ÇERÇEVE ORİJİNİ (TC / TU yerel) OLARAK KALIR
X_C0 = HS.C_X[0]                                                                         # v2 · TOPPING'in dünya solu 1207,5 (1292,5 geniş)''')
rep('''MODUL = [("A", "MODÜL A · KONİLİ AÇICI (dolap üstünde · kaide 104)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 0–4000)", X_A, W_B),
         ("C", "MODÜL C · TOPPING (dolap üstünde · kaide 104)", X_BC, W_BC), ("D", "MODÜL F · KONVEYÖR FIRIN", X_D, W_D),''',
    '''MODUL = [("A", "MODÜL A · KONİLİ AÇICI (dolap üstünde · kaide 104)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 507,5–4000 · 21 çekmece)", X_A, W_B),
         ("C", "MODÜL C · TOPPING İKİ KATLI (dolap üstünde · kaide 104 · 2200)", X_C0, HS.C_X[1] - X_C0), ("D", "MODÜL F · KONVEYÖR FIRIN", X_D, W_D),''')
rep('''         ("S", "MODÜL S · SERVİS / TESLİM (QR dolabı + tezgâh)", X_S, QR.X0 + QR.W - X_S)]''',
    '''         ("S", "MODÜL S · SERVİS / TESLİM (QR dolabı + tezgâh)", X_S, QR.X0 + QR.W - X_S),
         ("U", "MODÜL U · ÜST DEPO (A · fırın · K + E üstünde, 1862–2200)", X_A, X_E + W_E - X_A)]''')
rep('''MODUL_Y = {"A": (Y_DUZ, H_MAK), "B": (0.0, Y_DUZ), "C": (Y_DUZ, H_MAK),''', '''MODUL_Y = {"A": (Y_DUZ, H_MAK), "B": (0.0, Y_DUZ), "C": (Y_DUZ, H_UST), "U": (H_MAK, H_UST),''')
# ---- 3 · üreteçler → v2 adaptörleri ----
rep('''import qr_cad_v1 as QR, tezgah_cad_v2 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v4 as KD''', '''import qr_cad_v1 as QR, tezgah_cad_v2 as TZ, h2_ray_ek_v1 as RE, h2_kaide_v1 as KD''')
rep('''import topping_hesap_v7 as TH, topping_cad_v32 as TC ''', '''import topping_hesap_v7 as TH, h2_tc_v1 as TC ''')
rep('''_sp = _ilu.spec_from_file_location("TU11", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v19.py"))''',
    '''_sp = _ilu.spec_from_file_location("TU11", os.path.join(U, "h2", "h2_tu_v1.py"))   # v2 · iki katlı soğuk paket''')
rep('''    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), modul + ".py")''', '''    yol = os.path.join(U, modul + ".py")''')
rep('''import store_cad_v14 as SC ''', '''import h2_store_v1 as SC ''')
rep('''import acici_kabin_cad_v1 as AK ''', '''import h2_acici_v1 as AK ''')
rep('''import kutu_cad_v14 as KC ''', '''import h2_kutu_v1 as KC ''')
rep('''import types as _ty, moduler_montaj_v4 as MOD72 ''', '''import types as _ty, h2_moduler_v1 as MOD72 ''')
rep('''    import topping_v2_hesap_v2 as TH2 ''', '''    import h2_ist_v1 as TH2 ''')
rep('''    import topping_v2_hesap_v2 as _TH2 ''', '''    import h2_ist_v1 as _TH2 ''')
# ---- 4 · TOPPING birimi + çizimi (çerçeve orijini X_BC) ----
rep('''birim("TOPPING_MODUL", "TOPPING v2 (UNO'lu): 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + kaşar ve küp sucuk kaseti + hava tesisatı · tabla mekanizması v1'den", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (Y_MEK, Y_MEK + TC.Y), (-DZ, FT_ZS_ON), "sac", "topping_uno_cad_v19.py (dünya y −168) + topping_cad_v32.py (yerel y + 892)", "hat/topping_v2.html")''',
    '''birim("TOPPING_MODUL", "TOPPING İKİ KATLI (v2): ALT KAT kıyma · kuşbaşı UNO + kaşar · küp sucuk kaseti · ÜST KAT sos + harç UNO (Ø32 hortumla yayıcılara) + kaşar / sucuk 2 gün yedeği (GN) · "
      "evaporatör kaseti dönüşü alt kattan, üflemesi üst kata · tabla mekanizması v1'den (kısaldı)", "C", "GERCEK_MODUL",
      (X_C0, HS.C_X[1]), (Y_MEK, Y_MEK + TC.Y), (-DZ, FT_ZS_ON), "sac", "h2/h2_topping_v1.py (topping_cad_v32 + topping_uno_cad_v19 parçaları, iki katlı)", "hat/makine_v2.html")''')
rep('''                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))''',
    '''                sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], b["y"][0] + _d[1], _d[2]))   # v2: çerçeve orijini X_BC (birim solu 1207,5)''')
rep('''                sh = q["sh"].translate(cq.Vector(b["x"][0], 0.0, 0.0))''', '''                sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))   # v2: çerçeve orijini X_BC''')
rep('''for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)''', '''for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
V1_TASI = {}                                  # v2 · TC parçaları h2_topping_v1'de SON yerlerinde (v1 düzeltme ötelemeleri uygulanmaz)''')
rep('''ANA_V44 = [(3090, 1977, -380), (3090, 1977, -740), (1640, 1977, -740), (1640, 1335, -740), (1650, 1335, -740)]''',
    '''ANA_V44 = [(3090, 1977, -380), (3090, 1977, -740), (1785, 1977, -740), (1785, 1335, -740), (1770, 1335, -740)]   # v2: kaset (1790–2330 × 1383–1765) sağından iner → FRL'nin (2420–2470) SAĞ portu''')
# ---- 5 · E altı (B soğutması + panosu) · içecek yedeği üst depoda ----
rep('''assert _ION["on"] == [] and not _ION["sutun"][0]["engel"] and not _ION["sutun"][1]["engel"], "v63: icecek yedeginin onunde (kapak acikken) engel var: %s" % _ION''',
    '''assert KC.ICECEK_YEDEK["kutu"] == 0, "v2: E altinda icecek yedegi kalmamali (ust depoya cikti)"   # v2 · içecek yedeği U'da''')
rep('''     % (_ION["net"][1] - _ION["net"][0], _ION["sutun"][0]["bindirme"], _ION["sutun"][1]["bindirme"]), ("icecek_",)),
]''', '''     % (_ION["net"][1] - _ION["net"][0], _ION["sutun"][0]["bindirme"], _ION["sutun"][1]["bindirme"]), ("icecek_",)),
]
E_BIRIM = [e_ for e_ in E_BIRIM if e_[0] != "E_ICECEK_YEDEK"]                                  # v2 · içecek yedeği E'den ÇIKTI (üst depoda U_ICECEK_YEDEK)
E_BIRIM += [(k_, a_, KC.E_ALT_ONEK[k_]) for k_, a_ in (
    ("E_ALT_SOGUTMA", "v2 · B DOLABININ SOĞUTMASI E'nin altında: Secop NLE8.8CN R290 yoğuşma ünitesi + buharlaştırma tavası (dolabın yoğuşma suyu) · önden panjurlu emiş / atış, arada perde · soğutma hatları 2–4,5 m (dolum soğutmacıda)"),
    ("E_ALT_PANO", "v2 · B DOLABININ PANOSU E'nin altında: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + seçici röleler (v1: dolabın K4 kolonu)"))]''')
rep('''    ("E icecek yedegi: KC.ICECEK_YEDEK kutu = 144", (float(KC.ICECEK_YEDEK["kutu"]), 144.0)),''',
    '''    ("v2 · icecek yedegi UST DEPODA: UD.ICECEK_YEDEK kutu = 144 · E altinda 0", (float(UD.ICECEK_YEDEK["kutu"]), float(KC.ICECEK_YEDEK["kutu"]) + 144.0, 144.0)),''')
rep('''            ("icecek yedegi (E alti 6 koli)", KC.ICECEK_YEDEK["kutu"], 144, "dolap + yedek 288 · 4 gun 277"),''',
    '''            ("icecek yedegi (v2: UST DEPO K+E ustu, 6 koli)", UD.ICECEK_YEDEK["kutu"], 144, "dolap + yedek 288 · 4 gun 277"),''')
# ---- 6 · A + robot ----
rep('''birim("ROBOT_RAY", "Yer rayı · tek araba · x 200–5100", "-", "KATALOG", (200.0, 5100.0),''',
    '''birim("ROBOT_RAY", "Yer rayı · tek araba · x %.1f–%.0f (v2: sol ucu A ile 507,5 kısaldı)" % HS.ROBOT_RAY_X, "-", "KATALOG", HS.ROBOT_RAY_X,''')
rep('''    X_ROB_AC = 700.0 ''', '''    X_ROB_AC = HS.X_ROB_AC ''')
rep('''_dis_birim(AK, "GERCEK_ACICI", "acici_kabin_cad_v1.py", "hat/press.html")''',
    '''_dis_birim(AK, "GERCEK_ACICI", "h2_acici_v1.py", "hat/press.html")
import h2_ust_depo_v1 as UD                                                             # v2 · ÜST DEPO (U): A · fırın · K + E üstünde 1862–2200, içecek yedeği + fırın bacası
UD.kur()
_dis_birim(UD, "GERCEK_UST", "h2_ust_depo_v1.py", "hat/makine_v2.html")''')
rep('''for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR), ("K", KS.PARCALAR), ("A", AK.PARCALAR), ("D", FU.PARCALAR), ("BULASIK", BM.PARCALAR), ("TU", TU.P)):''',
    '''for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR), ("K", KS.PARCALAR), ("A", AK.PARCALAR), ("D", FU.PARCALAR), ("BULASIK", BM.PARCALAR), ("TU", TU.P), ("U", UD.PARCALAR)):''')
rep('''GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD, "GERCEK_ACICI": AK, "GERCEK_FIRIN_UST": FU}''',
    '''GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD, "GERCEK_ACICI": AK, "GERCEK_FIRIN_UST": FU, "GERCEK_UST": UD}   # v2: + üst depo''')
# ---- 7 · sözleşme ----
rep('''    ("makine ustu: KS.H = KC.H = Y_MEK + TC.Y = H_MAK = 1862", (KS.H, KC.H, Y_MEK + TC.Y, H_MAK, 1862.0)),
    ("dolap: SC.W_B = W_B = 4000", (SC.W_B, W_B, 4000.0)),''',
    '''    ("istasyon ustu: KS.H = KC.H = H_MAK = 1862", (KS.H, KC.H, H_MAK, 1862.0)),
    ("v2 · makine ustu: Y_MEK + TC.Y = UD.H_UST = H_UST = 2200", (Y_MEK + TC.Y, UD.H_UST, H_UST, 2200.0)),
    ("v2 · dolap: SC.W_B = W_B = 3492,5 (507,5–4000)", (SC.W_B, W_B, 3492.5)),
    ("v2 · hat boyu: HAT_W - X_A = 4722,5 (v1 5230)", (HAT_W - X_A, HS.HAT_BOY, 4722.5)),''')
rep('''    ("v63 · on duzlem: SC / KS / KC / TC / TU / AK / FU Z_ON = FT.ZS = 79", (SC.Z_ON, KS.Z_ON, KC.Z_ON, TC.Z_ON, TU.Z_ON, AK.Z_ON, FU.Z_ON, FT.ZS, FT_ZS_ON, 79.0)),''',
    '''    ("v63 · on duzlem: SC / KS / KC / TC / TU / AK / FU / UD Z_ON = FT.ZS = 79", (SC.Z_ON, KS.Z_ON, KC.Z_ON, TC.Z_ON, TU.Z_ON, AK.Z_ON, FU.Z_ON, UD.Z_ON, FT.ZS, FT_ZS_ON, 79.0)),''')
# ---- 8 · kategori: yeni birimler ----
rep('''    if kod in ("E_PIZZA", "E_KUTU", "E_ICECEK_YEDEK", "D_PIZZA_YEDEK_UST") or kod.startswith("URUN"): return "URUN"''',
    '''    if kod in ("E_PIZZA", "E_KUTU", "E_ICECEK_YEDEK", "D_PIZZA_YEDEK_UST", "U_ICECEK_YEDEK") or kod.startswith("URUN"): return "URUN"''')
rep('''    if kod == "B_SOGUTMA": return "SOGUTMA"''', '''    if kod in ("B_SOGUTMA", "E_ALT_SOGUTMA"): return "SOGUTMA"                                     # v2: B'nin yoğuşma ünitesi E'nin altında
    if kod == "E_ALT_PANO": return "KONTROL"''')
# ---- 9 · zarf + taban hizası + sef panelleri + A komşuluk ----
rep('''-1 <= b["y"][0] and b["y"][1] <= H_MAK + 1 and''', '''-1 <= b["y"][0] and b["y"][1] <= H_UST + 1 and''')
rep('''("TOPPING_MODUL ustu", _bk["TOPPING_MODUL"]["y"][1], H_MAK)]''', '''("TOPPING_MODUL ustu (v2 iki katli)", _bk["TOPPING_MODUL"]["y"][1], H_UST)]''')
rep('''    SEF_IST = (("A", X_A, X_A + W_A, Y_DUZ, H_MAK), ("C", X_BC, X_BC + W_BC, Y_DUZ, H_MAK), ("B", X_A, X_A + W_B, Y_ALT, Y_DUZ),''',
    '''    SEF_IST = (("A", X_A, X_A + W_A, Y_DUZ, H_MAK), ("C", X_C0, HS.C_X[1], Y_DUZ, H_UST), ("B", X_A, X_A + W_B, Y_ALT, Y_DUZ),''')
rep('''if sc.BoundingBox().xmax > 580.0]
    _KOM += [("A_MODULER:" + p["name"], p["shape"]) for p in MODULER_YENI if p["module"] == "A" and p["shape"].BoundingBox().xmax > 580.0]''',
    '''if sc.BoundingBox().xmax > 580.0 + HS.DXL]
    _KOM += [("A_MODULER:" + p["name"], p["shape"]) for p in MODULER_YENI if p["module"] == "A" and p["shape"].BoundingBox().xmax > 580.0 + HS.DXL]''')
rep('''(istasyon siniri 700)''', '''(istasyon siniri 1207,5)''')
rep('''        if sh.BoundingBox().xmin < 710.0: _tc72.append(''', '''        if sh.BoundingBox().xmin < 710.0 + HS.DXL: _tc72.append(''')   # v2: A|C sınırı 1207,5
rep('''        _ad = _SC_AD.get(_kod, _kod)
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v14.py", "")''', '''        _ad = getattr(SC, "BIRIM_AD", {}).get(_kod, _SC_AD.get(_kod, _kod))                  # v2: dolap birim metinleri h2_store_v1'den (K4 yok)
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "h2_store_v1.py (store_cad_v14 · K4 dilimi çıktı)", "")''')
rep('''KC.modul()
assert (KC.DONGU_GERCEK''', '''KC.modul()
for _kad, _kes, _knot in KC.K_DUVAR_DELIKLERI:                                             # v2 · B'nin yoğuşma suyu gideri K'nın iki yan sacından geçer (h2_kutu_v1)
    _kp = [p_ for p_ in KS.PARCALAR if p_["ad"] == _kad]; assert len(_kp) == 1, _kad
    _kp[0]["wp"] = cq.Workplane(obj=_kp[0]["wp"].val().cut(_kes.val() if hasattr(_kes, "val") else _kes))
assert (KC.DONGU_GERCEK''')
# ---- 10 · çıktılar ----
rep('''os.path.join(OUT, "hat_v92.glb")''', '''os.path.join(OUT, "hat2_v1.glb")''')
rep('''os.path.join(OUT, "hat_v92.usdz")], "hat_v92"''', '''os.path.join(OUT, "hat2_v1.usdz")], "hat2_v1"''')
rep('''print("hat_v92.glb · %d dugum''', '''print("hat2_v1.glb · %d dugum''')
rep('''print("hat_v92.usdz · %.0f KB''', '''print("hat2_v1.usdz · %.0f KB''')
rep('''KAT_OZET.get("hat_v92.glb", dict(kategori={}, birim={}))''', '''KAT_OZET.get("hat2_v1.glb", dict(kategori={}, birim={}))''')
rep('''print("v91 · KATEGORILER (hat_v92.glb ucgen): "''', '''print("v91 · KATEGORILER (hat2_v1.glb ucgen): "''')
rep('''    for mk in ("A", "B", "C", "D", "K", "E", "S", "-"): ''', '''    for mk in ("A", "B", "C", "D", "K", "E", "S", "U", "-"): ''')
rep('''hat=dict(w=HAT_W, h=H_MAK, d=DZ + FT.ZS, arka=-DZ, on=FT.ZS, pafta="HAT v92 (30 Eyl · Claude · YEREL): ''',
    '''hat=dict(w=HAT_W, x0=X_A, h=H_UST, h_istasyon=H_MAK, d=DZ + FT.ZS, arka=-DZ, on=FT.ZS, surum="v2.1", pafta="HAT v2.1 (30 Eyl · Claude · YEREL): VERSİYON 2 — İKİ KATLI TOPPING (üst kat sos + harç UNO + kaşar / sucuk yedeği · alt kat kıyma / kuşbaşı + kasetler) · hat 4722,5 (v1 5230, −507,5) · üst 2200 · dolap 21 çekmece (K4 çıktı: Secop + pano E altında, kaşar / sucuk yedeği TOPPING üst katında) · ÜST DEPO: içecek yedeği K + E üstünde, fırın bacası U'dan geçer · || v1 = ''')
rep('''    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:
        json.dump(dict(kutu_denetim=KUTU_DENETIM_V82, hat=dict(''', '''    import h2_topping_v1 as _T2
    _dj = json.load(io.open(os.path.join(U, "h2", "_denetim_topping_v1.json"), encoding="utf-8")); _sj = json.load(io.open(os.path.join(U, "h2", "_supurme_topping_v1.json"), encoding="utf-8"))
    _hy = _T2.hava_yolu()
    V2_DENETIM = ("Denetim (v2.1): TOPPING statik çakışma %d yeni (v1 iç geçmeleri %d) · tabla X süpürmesi %d bulgu (%d aday çift, 5 mm adım) · soğutma grubu havası emiş %.1f m/s (ön + arka pencere) / "
                  "atış %.1f m/s (≤ 3,5), yarık arası %.0f mm (≥ 250) · montajın kendi denetimleri (sözleşme, kategoriler, ön yüz, ürün yolu, dönüş süpürmesi, hava hattı) GEÇTİ."
                  % (len(_dj["yeni"]), len(_dj["eski"]), len(_sj["bulgu"]), _sj["aday"], _hy["v_emis"], _hy["v_atis"], _hy["ara"]))
    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:
        json.dump(dict(kutu_denetim=KUTU_DENETIM_V82, hat=dict(v2_denetim=V2_DENETIM, ''')
io.open(HEDEF, "w", encoding="utf-8").write(s)
print("hat2_montaj_v1.py yazıldı · %d yama" % N[0])
