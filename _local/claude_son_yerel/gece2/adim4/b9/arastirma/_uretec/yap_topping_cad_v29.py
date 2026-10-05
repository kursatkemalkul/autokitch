# -*- coding: utf-8 -*-
"""topping_cad_v28 → topping_cad_v29 (29 Eyl 2026 · YEREL) — Kemal: "yap herşeyi düzgün yap temiz olsun" (TOPPING: "teknik raf havada mı, tek sağ duvardan mı
destekleniyor — structure lazım değil mi · soğutma motoru yeterli mi, düzgün mü"). Soğuk kutu topping_uno_cad_v16 (her yüz 60 sandviç) ile birlikte:
  · TEKNİK CEP: 2 × L 30×30×3 konsol taşıyıcı (yalnız sağ yan saca bağlı, ~160 MPa / ~10 mm uç sehimi) KALKTI → cihazlar soğuk kutunun üstüne (B tavanı
    60 sandviç, dış sacı = teknik taban, dünya 1578) Ø40 × 6 titreşim pedleriyle oturur; B tavanı iki ucundan (L duvarı + sağ duvar) taşınır
  · yoğuşma ünitesi GERÇEK ÖLÇÜDE: Secop CU KLF4.8CND (R290 · 378 W @ −10/32 °C) 307 × 272 × 380, 14,2 kg (v28 zarfı 300 × 220 × 220 sığmıyordu) · üstü tavan sacına 4,5
  · pano / güç kaynağı / UPS / DIN rayları tabana (DIN plakası L bükümlü, tabana M6) · T kapağı teknik tabandan (dünya 1578–1859) · giriş yarıkları alt kaydın üstünde
  · evaporatör + fan + 4 ayak KURU BÖLMEDEN KALKTI (yalıtım dışındaydı: +134 W, yoğuşma) → TU v16'da soğuk odanın içinde (A tavanı)
  · T sol dikme köşebentleri L duvarının yeni dış sacına (dünya x 1550)
  · dünya denetimi: TU v16 · itici yok (v70'ten beri bantlı tabla) · hazne dolum çekmesi 4 haznede (sos + harç eklendi), kaldırma 15 · teknik cep denetimi pedlere göre
Önceki: topping_cad_v28.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v28.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def blok(bas, son, yeni):
    global s
    assert s.count(bas) == 1, ("bas", s.count(bas), bas[:90])
    i = s.index(bas)
    assert s.count(son, i) >= 1, ("son", son[:90])
    j = s.index(son, i) + len(son)
    s = s[:i] + yeni + s[j:]


degis('"""topping_cad_v28 (29 Eyl 2026 · YEREL · yap_topping_cad_v28.py): RAY CIVATALARI',
      '"""topping_cad_v29 (29 Eyl 2026 · YEREL · yap_topping_cad_v29.py): TEKNİK CEP KUTUNUN ÜSTÜNDE — konsol taşıyıcılar kalktı, cihazlar TU v16 soğuk kutusunun B tavanına' + NL +
      '(teknik taban, dünya 1578) titreşim pedleriyle oturur · Secop CU KLF4.8CND gerçek ölçü 307 × 272 × 380 · evaporatör kuru bölmeden kalktı (TU v16: yalıtımın içinde) · T kapağı 1578–1859' + NL +
      'v28 (29 Eyl 2026 · YEREL · yap_topping_cad_v28.py): RAY CIVATALARI')
degis('TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v15.py")', 'TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v16.py")')
degis('"onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0)}', '"onyuz_T_kapagi": (1521.5, 2497.0, 1578.0, 1859.0)}          # v29: T kapağı teknik tabandan (TU v16)')
degis('T_YARIK_Y = (700.0, 860.0)', 'T_YARIK_Y = (720.0, 860.0)          # v29: giriş yarıkları T alt kaydının (686–716) üstünde')
degis('TEK_TASIYICI_Y, TEK_TAKOZ = 1553.5 + 31.0, 10.0   # v25b · teknik cep taşıyıcı üstü (dünya) · titreşim takozu yüksekliği',
      'TEK_TABAN_D, TEK_PED = 1578.0, 6.0   # v29 · teknik cep tabanı (dünya · TU v16 Y_TEK 1746 − 168) · titreşim pedi Ø40 × 6 (v28 konsol L taşıyıcı + Ø20 × 10 takoz)' + NL +
      'CU_KLF = (860.0, 1167.0, 272.0, -40.0, -420.0)     # v29 · Secop CU KLF4.8CND: x (yerel) · yükseklik · z ön / arka (307 × 272 × 380 · sogutma_topping_v1)')

# ---- evaporatör kuru bölmeden kalkar (TU v16'da soğuk odanın içinde)
blok('    ekle("evaporator", kut(EVX[0], EVX[1], EVY[0], EVY[1], EVZ[0], EVZ[1]), "bakir",', 'DNY[1] - DNY[0], DNY[0], DNY[1])))',
     '    # v29 · EVAPORATÖR + FAN + 4 AYAK KURU BÖLMEDEN KALKTI: yalıtımın dışındaydı (+134 W, kuru bölmede yoğuşma · sogutma_topping_v1) → topping_uno_cad_v16' + NL +
     '    #       soğuk odanın İÇİNDE (A tavanı, SOS haznesinin üstü), hatlar L duvarından teknik cepteki yoğuşma ünitesine · EVX / EVY yalnız eski hava perdesi (montaj dışı) için')

# ---- teknik cep: konsol yok, cihazlar kutunun üstünde
blok('    # v25 · TEKNİK CEP (dünya x 1520–2498,5', '"UPS + güç kaynağı raylarını taşır"))',
     '''    # v29 · TEKNİK CEP (Kemal: "havada mı, tek sağ duvardan mı destekleniyor — structure lazım değil mi"): v28'in 2 × L 30×30×3 KONSOL taşıyıcısı KALKTI.
    #       Cihazlar TU v16 soğuk kutusunun B tavanına (60 sandviç, dış sacı = teknik taban, dünya 1578) titreşim pedleriyle oturur. B tavanı iki ucundan
    #       (L duvarı x 1490–1550 · sağ duvar 2440–2500) taşınır: açıklık 950, ~30 kg → sehim ≈ 0,5 mm (PU kayması dahil) · ped basıncı 0,03 MPa < PU 0,15 MPa
    TEK_TABAN = TEK_TABAN_D - DY_D                                               # yerel 686
    _PED = [(880.0, -60.0), (1147.0, -60.0), (880.0, -400.0), (1147.0, -400.0), (1200.0, -60.0), (1560.0, -60.0), (1200.0, -270.0), (1560.0, -270.0)]
    for _i, (_tx, _tz) in enumerate(_PED):
        ekle("teknik_takoz_%d" % _i, sily(_tx, _tz, 20.0, TEK_TABAN, TEK_TABAN + TEK_PED), "silikon",
             bom=("Titreşim pedi Ø40 × 6 · neopren 60 Shore A (yapıştırma + cihaz tabanına M6) — parça no VARSAYIM", 8, "yoğuşma ünitesi 4 + pano 4",
                  "v29 · teknik tabana (TU v16 B tavanının dış sacı) oturur · konsol taşıyıcı yok") if _i == 0 else None)
    _cx0, _cx1, _ch, _cz0, _cz1 = CU_KLF
    ekle("teknik_sogutma_grubu", kut(_cx0, _cx1, TEK_TABAN + TEK_PED, TEK_TABAN + TEK_PED + _ch, _cz1, _cz0), "motor",
         bom=("Yoğuşma ünitesi Secop CU KLF4.8CND (R290) · 314H6001", 1, "307 × 272 × 380 · 14,2 kg · 378 W @ −10/32 °C (43 °C istenirse aynı gövde KLF6.6CND 426 W)",
              "teknik cepte, 4 titreşim pedi üstünde (v29) · gereken 231–326 W @ 32 °C (evaporatör yalıtım içinde, sogutma_topping_v1) · önden T kapağının sol-alt yarıklarından emer, "
              "sağ-üstten atar · hatlar L duvarından A tavanındaki evaporatöre (TU v16) · montaj / gaz dolumu soğutmacı firma"))
    _pd = kut(1180.0, 1580.0, TEK_TABAN + TEK_PED, TEK_TABAN + TEK_PED + 240.0, -40.0, -290.0)
    _pi = kut(1181.5, 1578.5, TEK_TABAN + TEK_PED + 1.5, TEK_TABAN + TEK_PED + 238.5, -41.5, -288.5)
    ekle("teknik_pano_kutusu", _pd.cut(_pi), "sac",
         bom=("TOPPING panosu", 1, "304 · önden kapaklı, IP54", "PLC giriş/çıkış + röleler + sürücü beslemesi · v29: 4 titreşim pedi üstünde teknik tabanda (M6)"))
    _DY = TEK_TABAN + 2.0                                                        # DIN plakasının tabana bükülen kolunun üstü
    ekle("teknik_ups", din_parca(UPS_STEP, 1660.0, _DY, -40.0), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1,
              "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur; teknik tabandaki DIN plakasının rayında (v29)"))
    ekle("teknik_guc_kaynagi", din_parca(GUC_STEP, 1592.0, _DY, -40.0), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1,
              "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W" % H.S["elektrik"]["guc_kaynagi_W"]))
    ekle("teknik_din_rayi_ups", kut(1656.0, 1797.0, _DY, _DY + 35.0, -178.0, -170.5), "sac",
         bom=("DIN ray TS35 × 7,5 · UPS", 1, "EN 60715 · 141 mm", "v29 · DIN plakasında, alt kenarı plakanın bükümünde"))
    ekle("teknik_din_rayi_guc", kut(1590.0, 1654.0, _DY + 10.0, _DY + 45.0, -178.0, -162.8), "sac",
         bom=("DIN ray TS35 × 7,5 + 7,7 mm ara parça · güç kaynağı", 1, "EN 60715 · 64 mm", "güç kaynağı UPS'ten 7,7 mm sığ → ray ara parçayla öne alınır"))
    ekle("teknik_din_plakasi", kut(1588.0, 1797.0, _DY, _DY + 110.0, -180.0, -178.0).union(kut(1588.0, 1797.0, TEK_TABAN, _DY, -180.0, -140.0)), "sac",
         bom=("DIN montaj plakası 304 2 mm · L bükümlü", 1, "209 × 110 + 40 büküm · büküm teknik tabana 2 × M6 (perçin somun, köpük içi takviye)", "UPS + güç kaynağı raylarını taşır (v29: konsol taşıyıcı yok)"))''')

# ---- T kapağı + çerçevesi teknik tabandan · T sol dikme köşebentleri L duvarının dış sacına
degis('MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(1553.5), yl(1859.0))', 'MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(TEK_TABAN_D), yl(1859.0))          # v29: T teknik tabandan (TU v16 · 1578)')
degis('        _L = kut(xl(1521.5), xl(1524.5), _yk, _yk + 40.0, -20.0, Z_CER_C[0]).union(kut(xl(1521.5), xl(1551.5), _yk, _yk + 40.0, Z_CER_C[0] - 3.0, Z_CER_C[0]))',
      '        _L = kut(850.0, 853.0, _yk, _yk + 40.0, -20.0, Z_CER_C[0]).union(kut(xl(1521.5), 853.0, _yk, _yk + 40.0, Z_CER_C[0] - 3.0, Z_CER_C[0]))   # v29: dik kol L duvarının dış sacına (TU v16, dünya x 1550)')

# ---- sabit tahrik bağlantıları (dünya denetimi 'havada': v27'den beri yatak burcu kutuya, motor + motor kutusu tahrik kutusuna BAĞLI DEĞİLDİ)
degis('''        ekle("st_" + _t27["ad"], cq.Workplane(obj=_t27["sh"].translate(cq.Vector(-DX_D, -DY_D, 0.0))), _t27["mal"], bom=_t27["bom"])''',
      '''        ekle("st_" + _t27["ad"], cq.Workplane(obj=_t27["sh"].translate(cq.Vector(-DX_D, -DY_D, 0.0))), _t27["mal"], bom=_t27["bom"])
    # v29 · SABİT TAHRİK BAĞLANTILARI (dünya denetimi 'havada', v27'den beri): yatak burcu tahrik kutusuna (8,5 mm), motor ve motor kutusu tahrik kutusuna
    #       (1,5 mm) bağlı değildi → yatak flanşı (burç buna kaynaklı) + motor adaptör flanşı (işlenmiş; motor 4 × M5, iki kutuya TIG) eklendi
    _TK = {p_["ad"]: p_["sh"] for p_ in BT.TAHRIK}
    _kb_, _mb_, _yb_ = _TK["tahrik_kutusu"].BoundingBox(), _TK["motor_kutusu"].BoundingBox(), _TK["tahrik_yatak_burcu"].BoundingBox()
    _xs_, _ys_ = (_yb_.xmin + _yb_.xmax) / 2.0, (_yb_.ymin + _yb_.ymax) / 2.0
    _mt_ = _TK["tahrik_motoru"]
    def _mkesit(z_):                                                           # motorun z kesit alanı (kare gövde ≈ 3100 · pilot Ø38,1 ≈ 1140)
        k_ = _mt_.intersect(kut(_xs_ - 40.0, _xs_ + 40.0, _ys_ - 40.0, _ys_ + 40.0, z_ - 0.005, z_ + 0.005).val())
        return k_.Volume() / 0.01
    _za, _zb = _mb_.zmax - 12.0, _mb_.zmax                                    # gövde ön yüzü motor kutusunun ağzının ≤ 12 mm gerisinde
    assert _mkesit(_za) > 2000.0 and _mkesit(_zb) < 2000.0, (_mkesit(_za), _mkesit(_zb))
    for _i_ in range(24):
        _zm = (_za + _zb) / 2.0
        if _mkesit(_zm) > 2000.0: _za = _zm
        else: _zb = _zm
    Z_MOTOR_YUZ = _zb + 0.01                                                   # motor flanş yüzü (dünya z) + 0,01 (yüz kesiti ±0,002 mm sayısal · temas payı ≤ 0,05)
    _ad_ = kut(_mb_.xmin + 1.5, _mb_.xmax - 1.5, _mb_.ymin + 1.5, _mb_.ymax - 1.5, Z_MOTOR_YUZ, _mb_.zmax).cut(silz(_xs_, _ys_, 19.15, Z_MOTOR_YUZ - 1.0, _mb_.zmax + 1.0))
    ekle("st_motor_adaptor_flansi", _ad_.translate((-DX_D, -DY_D, 0.0)), "celik",
         bom=("Sabit tahrik motor adaptör flanşı AISI 304 · işlenmiş", 1, "%.0f × %.0f × %.1f · NEMA23 pilot yuvası Ø38,3 · motor 4 × M5" % (_mb_.xlen - 3.0, _mb_.ylen - 3.0, _mb_.zmax - Z_MOTOR_YUZ),
              "v29 · motor kutusunun ağzına + tahrik kutusunun arka kenarına TIG · motor buna oturur (v27–v28 motor ve motor kutusu havadaydı)"))
    _yf_ = kut(_kb_.xmin + 1.5, _kb_.xmax - 1.5, _kb_.ymin + 1.5, _kb_.ymax - 1.5, _yb_.zmin - 3.0, _yb_.zmin).cut(silz(_xs_, _ys_, 10.0, _yb_.zmin - 4.0, _yb_.zmin + 1.0))
    ekle("st_yatak_flansi", _yf_.translate((-DX_D, -DY_D, 0.0)), "celik",
         bom=("Sabit tahrik yatak flanşı AISI 304 3 mm", 1, "%.0f × %.0f · kaplin geçişi Ø20" % (_kb_.xlen - 3.0, _kb_.ylen - 3.0),
              "v29 · tahrik kutusunun içine TIG · yatak burcu buna kaynaklı (v27–v28 burç havadaydı)"))''')

# ---- T kapağı: omega + bas-aç mandal yeni yükseklikte (panel 686–967 · giriş yarıkları 720–794 · çıkış 860–934)
degis('("onyuz_T_kapagi", (xl(1521.5), xl(2497.0), T_Y[0], T_Y[1]), tuple(_yar), "sag", 828.0)]',
      '("onyuz_T_kapagi", (xl(1521.5), xl(2497.0), T_Y[0], T_Y[1]), tuple(_yar), "sag", 827.0)]          # v29: omega iki yarık bandının arasında (807–847)')
degis('        _yb = (yl(1082.5), yl(1102.5)) if "mekanizma" in _a else (_y0 + 108.5, _y0 + 138.5)',
      '        _yb = (yl(1082.5), yl(1102.5)) if "mekanizma" in _a else (_y0 + 162.5, _y0 + 192.5)          # v29: T mandalı omeganın üstünde (848,5–878,5; v28 _y0 + 108,5 omegaya giriyordu)')

# ---- kinematik denetimi: referans v28 (v27'den beri tabla + çalışma diski bantlı tabla kasetinde → v24 karşılaştırması IndexError veriyordu)
degis('''        V24 = importlib.import_module("topping_cad_v24"); V24.PARCALAR[:] = []; V24.modul()
        es = []
        for ad in ("acici_konisi_on", "acici_konisi_arka", "calisma_diski", "tabla", "lineer_ray_on", "araba_plakasi", "doner_yatak"):''',
      '''        V24 = importlib.import_module("topping_cad_v28"); V24.PARCALAR[:] = []; V24.modul()      # v29: referans v28 (v27'den beri tabla + disk bantlı tabla kasetinde)
        es = []
        for ad in ("acici_konisi_on", "acici_konisi_arka", "lineer_ray_on", "lineer_ray_arka", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "st_tahrik_diski", "st_tahrik_kutusu", "st_tahrik_motoru"):''')
degis('k("kinematik v24 ile aynı (koniler, çalışma diski, tabla, ray, araba, döner yatak): en büyük fark kutu %.4f mm · hacim %.3f mm³"',
      'k("v29 · kinematik v28 ile aynı (koniler, 2 ray, araba, döner yatak, ayar bileziği, sabit tahrik diski / kutusu / motoru): en büyük fark kutu %.4f mm · hacim %.3f mm³"')

# ---- dünya denetimi
degis('''    try:
        IT = importlib.import_module(ITICI_MOD); it_ad = ITICI_MOD
    except ImportError:
        IT = importlib.import_module("itici_cad_v4"); it_ad = "itici_cad_v4"
    W_ = dunya_parcalari(TU, IT)''',
      '''    IT = None; it_ad = "yok (v70'ten beri bantlı tabla — aktarma iticisi kalktı)"                   # v29
    W_ = dunya_parcalari(TU, IT)''')
degis('"TC:onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0), "TU:onyuz_K1_dis_sac": (701.5, 1518.5, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1521.5, 2497.0, 1110.5, 1550.5)}',
      '"TC:onyuz_T_kapagi": (1521.5, 2497.0, TEK_TABAN_D, 1859.0), "TU:onyuz_K1_dis_sac": (701.5, 1518.5, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1521.5, 2497.0, 1110.5, TEK_TABAN_D - 3.0)}')
blok('    TEK_BEK = {"TC:teknik_tasiyici_0": 1554.5,', 'max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01)',
     '''    TEK_BEK = {"TC:teknik_sogutma_grubu": TEK_TABAN_D + TEK_PED, "TC:teknik_pano_kutusu": TEK_TABAN_D + TEK_PED, "TC:teknik_din_plakasi": TEK_TABAN_D,
               "TC:teknik_ups": TEK_TABAN_D + 2.0, "TC:teknik_guc_kaynagi": TEK_TABAN_D + 2.0}
    TEK_BEK.update({"TC:teknik_takoz_%d" % i_: TEK_TABAN_D for i_ in range(8)})
    tk = [(a, round(B_[a].ymin, 2), v) for a, v in TEK_BEK.items()]
    _S = dict(W_)
    _mt = lambda a_, c_: (lambda d_: d_.Value() if d_.IsDone() else 99.0)(DSS(_S[a_].wrapped, _S[c_].wrapped))
    _tt = [(a.split(":")[1] + "↔" + c.split(":")[1], round(_mt(a, c), 3)) for a, c in [("TC:teknik_takoz_%d" % i_, "TU:teknik_ayirma_saci_yatay") for i_ in range(8)] +
           [("TC:teknik_takoz_%d" % i_, "TC:teknik_sogutma_grubu") for i_ in range(4)] + [("TC:teknik_takoz_%d" % i_, "TC:teknik_pano_kutusu") for i_ in range(4, 8)] +
           [("TC:teknik_din_plakasi", "TU:teknik_ayirma_saci_yatay"), ("TC:teknik_sogutma_grubu", "TU:sogutma_emis_hatti"), ("TC:teknik_sogutma_grubu", "TU:sogutma_sivi_hatti")]]
    _ust = min(B_["TC:dis_tavan"].ymin - B_[a].ymax for a in ("TC:teknik_sogutma_grubu", "TC:teknik_pano_kutusu", "TC:teknik_ups", "TC:teknik_guc_kaynagi"))
    k("v29 · teknik cep KONSOLSUZ: cihazlar soğuk kutunun üstünde (TU v16 teknik taban %.0f) · yoğuşma ünitesi (Secop CU KLF4.8CND 307 × 272 × 380) + pano Ø40 × 6 pedlerde · DIN plakası tabanda: %s · "
      "temaslar %s · tavan sacına en az %.1f mm · DIN rayları x ≤ 2497 (%.1f)"
      % (TEK_TABAN_D, [(a.split(":")[1], y_) for a, y_, v in tk], [x_ for x_ in _tt if x_[1] > 0.05] or "hepsi ≤ 0,05", _ust, max(B_[a].xmax for a in B_ if "din_rayi" in a)),
      all(abs(y_ - v) < 0.01 for a, y_, v in tk) and all(d_ <= 0.05 for a, d_ in _tt) and _ust >= 2.0 and max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01
      and not [a for a in B_ if a.startswith(("TC:teknik_tasiyici", "TC:evaporator", "TC:fan_0"))])''')
degis('''    # 8d · v25b · HAZNE DOLUM ÇEKMESİ (denetim_C bulgu 13): TC kelepçe sökülür, hazne 20 mm kaldırılır, 0–640 öne (K1 + flipper + K2 açık)
    for kk in ("kiyma", "kusbasi"):''',
      '''    # 8d · v25b · HAZNE DOLUM ÇEKMESİ (denetim_C bulgu 13): TC kelepçe sökülür, hazne 15 mm kaldırılır, 0–640 öne (K1 + flipper + K2 açık)
    #      v29: 4 haznede (sos + harç eklendi · evaporatör SOS'un, hatlar HARÇ'ın üstünde) · kaldırma 20 → 15 (B tavanı 1686; boyun altı çıkış TC kelebeğini 4 mm aşar)
    HAZNE_KALK = 15.0
    for kk in ("sos", "harc", "kiyma", "kusbasi"):''')
degis('                s2 = sh.translate(cq.Vector(0.0, 20.0, dz)); b2 = s2.BoundingBox()', '                s2 = sh.translate(cq.Vector(0.0, HAZNE_KALK, dz)); b2 = s2.BoundingBox()')
degis('k("v25b · %s haznesi DOLUM ÇEKMESİ: TC kelepçe sökülür → hazne 20 mm kaldırılır → 0–640 mm öne (K1 + flipper + K2 açık): serbest (bulgu %d)" % (kk, len(bul_h)), not bul_h, str(bul_h[:6]))',
      'k("v29 · %s haznesi DOLUM ÇEKMESİ: TC kelepçe sökülür → hazne %.0f mm kaldırılır → 0–640 mm öne (K1 + flipper + K2 açık): serbest (bulgu %d)" % (kk, HAZNE_KALK, len(bul_h)), not bul_h, str(bul_h[:6]))')
degis('''           ("IT:montaj_kirisi", "TU:soguk_duvar_sag_alt_profili"), ("TU:soguk_duvar_sag_alt_profili", "TC:dis_yan_sag"),
           ("TU:onyuz_kilavuz_flipper", "TU:tasiyici_raf_3mm"), ("TC:teknik_takoz_0", "TC:teknik_tasiyici_0"), ("TC:teknik_takoz_0", "TC:teknik_sogutma_grubu"),
           ("TC:teknik_takoz_6", "TC:teknik_pano_kutusu"), ("TC:teknik_din_plakasi", "TC:teknik_tasiyici_1"), ("TC:teknik_ups", "TC:teknik_din_rayi_ups"), ("TC:teknik_din_rayi_ups", "TC:teknik_din_plakasi"),''',
      '''           ("TU:raf_askisi_burclari_sol", "TC:dis_yan_sol"), ("TU:raf_askisi_burclari_sag", "TC:dis_yan_sag"), ("TU:kabin_sol_duvar_PU", "TC:dis_yan_sol"), ("TU:kabin_sag_duvar_PU", "TC:dis_yan_sag"),
           ("TU:yalitim_blogu", "TC:dis_tavan"), ("TU:teknik_ayirma_saci_yatay", "TC:dis_yan_sag"), ("TU:teknik_ayirma_saci_dikey", "TC:dis_tavan"), ("TU:soguk_arka_dis_sac", "TC:dis_yan_sol"),
           ("TU:alt_yalitim_saci", "TC:dis_yan_sol"), ("TU:alt_yalitim_saci", "TC:sensor_braketi_tabla_bos"), ("TU:alt_yalitim_saci", "TC:fire_silecegi_silindiri"),
           ("TC:st_yatak_flansi", "TC:st_tahrik_kutusu"), ("TC:st_yatak_flansi", "TC:st_tahrik_yatak_burcu"), ("TC:st_motor_adaptor_flansi", "TC:st_motor_kutusu"),
           ("TC:st_motor_adaptor_flansi", "TC:st_tahrik_motoru"), ("TC:st_motor_adaptor_flansi", "TC:st_tahrik_kutusu"), ("TC:st_tahrik_braketi", "TC:kayis_kirisi"),
           ("TU:onyuz_kilavuz_flipper", "TU:tasiyici_raf_3mm"), ("TC:teknik_takoz_0", "TU:teknik_ayirma_saci_yatay"), ("TC:teknik_takoz_0", "TC:teknik_sogutma_grubu"),
           ("TC:teknik_takoz_6", "TC:teknik_pano_kutusu"), ("TC:teknik_din_plakasi", "TU:teknik_ayirma_saci_yatay"), ("TC:teknik_ups", "TC:teknik_din_rayi_ups"), ("TC:teknik_din_rayi_ups", "TC:teknik_din_plakasi"),''')
degis('k("v25b · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · T köşebendi ↔ dikey sac + dikme · itici kirişi ↔ sağ duvar alt profili ↔ TC yan sacı · kılavuz ↔ raf · takoz · DIN plakası · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"',
      'k("v29 · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · T köşebendi ↔ L dış sacı + dikme · SOĞUK KUTU ↔ TC yan / tavan sacları (yapışık, boşluk yok) · raf burçları ↔ TC yan sacları · alt sac ↔ sensör / silecek askısı · kılavuz ↔ raf · ped ↔ teknik taban · DIN plakası · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"')
degis('        import acici_kabin_cad_v1 as AK, kaide_cad_v2 as KD2', '        import acici_kabin_cad_v1 as AK, kaide_cad_v3 as KD2                  # v29: montaj v81+ kaide v3')
degis('print("TOPPING MODULU v26 · %d parca', 'print("TOPPING MODULU v29 · %d parca')
for a_ in ("TC:teknik_tasiyici", "TEK_TASIYICI_Y", "TEK_TAKOZ,"):
    assert a_ not in s.replace('("TC:teknik_tasiyici", "TC:evaporator", "TC:fan_0")', ""), a_
compile(s, "topping_cad_v29.py", "exec")
io.open(os.path.join(U, "topping_cad_v29.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v29.py yazildi")
