# -*- coding: utf-8 -*-
"""hat_montaj_v62 → hat_montaj_v63 (28 Eyl 2026) — ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (SPEC_on_duzlem_v63.md · Kemal 27 Eyl gece:
"fırının ön yüzü sınır yüzey, her şeyi o yüzeye getireceğiz, her istasyona ön yüzey ekle aynı çekmecedeki gibi … her istasyon kendi başına temiz bir kutu").
Yeni üreteçler: store_cad_v8 · acici_kabin_cad_v1 (A gerçek kabin) · kaide_cad_v2 · topping_uno_cad_v14 · topping_cad_v25 · itici_cad_v5 · firin_tp10_cad_v8 ·
firin_ust_kabin_cad_v1 (fırın üstü kabin + davlumbaz + kompresör tavası) · kesme_cad_v6 · bulasik_cad_v2 (ayaksız, tablada) · kutu_cad_v7.
Montajda: A_KABIN ve D_DAVLUMBAZ KUTU yer tutucuları → gerçek birimler · ön yüz / zarf denetimleri +79 · şeffaf yüzeyler +79 · ön kapaklar (onyuz_) şeffaf
gösterim bütün modüllerde · fırın kabuğu ön saclarla aynı ton · hat derinliği 909 (arka −830 SABİT) · parça etiketi E-yerel kayıt hatası düzeldi."""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v62.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# 0 · tarihçe
degis('"""v62 (27 Eyl 2026 gece):',
      '"""v63 (28 Eyl 2026): ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (SPEC_on_duzlem_v63) — bütün ön yüzler fırın ön yüzü düzleminde (z +79), arka −830 sabit, derinlik 909;' + NL +
      '  A gerçek kabin (acici_kabin_cad_v1) · fırın üstü kabin (firin_ust_kabin_cad_v1) · her istasyon kapaklı · bulaşık ayaksız tablada · çıktılar hat_v63.' + NL +
      'v62 (27 Eyl 2026 gece):')
# 1 · kod gövdesinde üreteç sürümleri
i = s.index('\nimport importlib, io')
kod = s[i:]
for a, b in (("store_cad_v7", "store_cad_v8"), ("kesme_cad_v5", "kesme_cad_v6"), ("kutu_cad_v6", "kutu_cad_v7"), ("topping_uno_cad_v13", "topping_uno_cad_v14"),
             ("topping_cad_v24", "topping_cad_v25"), ("itici_cad_v4", "itici_cad_v5"), ("firin_tp10_cad_v7", "firin_tp10_cad_v8"), ("kaide_cad_v1", "kaide_cad_v2"),
             ("bulasik_cad_v1", "bulasik_cad_v2")):
    assert kod.count(a) >= 1, a
    kod = kod.replace(a, b)
s = s[:i] + kod

# 2 · TOPPING birim zarfı ön +79
degis('(X_BC, X_BC + W_BC), (Y_MEK, Y_MEK + TC.Y), (-DZ, 0.0), "sac",', '(X_BC, X_BC + W_BC), (Y_MEK, Y_MEK + TC.Y), (-DZ, FT_ZS_ON), "sac",')
degis('birim("TOPPING_MODUL", ', 'FT_ZS_ON = 79.0                                           # v63 · ön düzlem (fırın gövdesinin ön yüzü; FT.ZS ile sözleşmede eşitlenir)\nbirim("TOPPING_MODUL", ')

# 3 · A: KUTU yer tutucu yerine gerçek kabin (acici_kabin_cad_v1)
degis('birim("A_KABIN", "AÇICI modülü kabini (dolap üstünde 788 · mekanizma kaidede 892 · açıcının kendisi TOPPING CAD\'inde)", "A", "KUTU", (X_A, X_A + W_A), (Y_DUZ, H_MAK), (-DZ, 0.0), "kabin", "pafta ATOSA TABLALI v7 · v57 alçak hat")\n',
      '# v63: A_KABIN KUTU yer tutucusu kalktı → acici_kabin_cad_v1 (A_GOVDE + A_ONYUZ, aşağıda KD.kur() sonrası)\n')
degis('_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v2.py", lambda k_: "hat/press.html" if KD.BIRIM_MODUL[k_] == "A" else "hat/topping_v2.html")',
      '_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v2.py", lambda k_: "hat/press.html" if KD.BIRIM_MODUL[k_] == "A" else "hat/topping_v2.html")\n'
      'import acici_kabin_cad_v1 as AK                                                         # v63: A gerçek kabin (dünya · 304 1,5 · ön tava 20 · robot ağzı · ışık perdesi)\n'
      'AK.kur()\n'
      '_dis_birim(AK, "GERCEK_ACICI", "acici_kabin_cad_v1.py", "hat/press.html")')

# 4 · D: davlumbaz KUTU yer tutucusu yerine fırın üstü kabin (firin_ust_kabin_cad_v1)
degis('birim("D_DAVLUMBAZ", "Egzoz davlumbazı (bizim) · fan · yağ + karbon filtre · fırın üstü bölmenin ARKA yarısı (ön yarıda kutu yedeği + kompresör) · komşu modüllere asılı", "D", "KUTU", (X_D, X_D + W_D), (FT.YG1 + 10.0, H_MAK), (-DZ, -425.0), "kutu", "v48 · v57: 1315–1862")\n',
      'import firin_ust_kabin_cad_v1 as FU                                                     # v63: fırın üstü kabin (yanlar + üst + tek parça arka + düşer kapaklar) + davlumbaz sac kutusu + kompresör tavası\n'
      'FU.kur()\n'
      '_dis_birim(FU, "GERCEK_FIRIN_UST", "firin_ust_kabin_cad_v1.py", "hat/oven.html")\n')
degis('    ("davlumbaz alti = firin kalkani 1315", (_bk0["D_DAVLUMBAZ"]["y"][0], FT.ISI_KALKANI_Y[0], 1315.0)),',
      '    # v63: davlumbaz artık firin_ust_kabin_cad_v1 (F_DAVLUMBAZ, köşebentleri 1275\'ten) — kendi denetimi üreteçte')
degis('_HV_ATLA = ("HAVA_KOMPRESOR", "D_DAVLUMBAZ")', '_HV_ATLA = ("HAVA_KOMPRESOR", "F_DAVLUMBAZ", "F_UST_KABIN", "F_KOMP_AYAK", "F_UST_KAPAK")   # v63: hat üst kabinin yan saclarındaki rakorlardan geçer')
degis('GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD}',
      'GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD, "GERCEK_ACICI": AK, "GERCEK_FIRIN_UST": FU}   # v63: + A kabini + fırın üstü kabin')

# 5 · sözleşme
degis('    ("bulasik y: BM.Y0 = KS.BULASIK_YER", (BM.Y0, KS.BULASIK_YER[1], 126.0)),',
      '    ("bulasik y: BM.Y0 = KS.BULASIK_YER (v63: ayaksız, tabla üstü 139)", (BM.Y0, KS.BULASIK_YER[1], 139.0)),')
degis('    ("v58 · B_COP = 8 parca (store_cad_v8 · robot copu kapagi + klapesi yerinde, Kemal)", (float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])), 8.0)),',
      '    ("v63 · on duzlem: SC / KS / KC / TC / TU / AK / FU Z_ON = FT.ZS = 79", (SC.Z_ON, KS.Z_ON, KC.Z_ON, TC.Z_ON, TU.Z_ON, AK.Z_ON, FU.Z_ON, FT.ZS, FT_ZS_ON, 79.0)),\n'
      '    ("v58 · B_COP robot copu kapagi + klapesi yerinde (v63: store_cad_v8 13 parca)", (float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])), 13.0)),')
degis('assert _ION["on"] == ["kablo_kanali_dikey_alt", "kose_dikme_on_0"] and [e_[0] for e_ in _ION["sutun"][0]["engel"]] == ["kose_dikme_on_0"] \\\n'
      '    and [e_[0] for e_ in _ION["sutun"][1]["engel"]] == ["kablo_kanali_dikey_alt"], "v58: icecek yedeginin onu beklenen gibi degil: %s" % _ION',
      'assert _ION["on"] == [] and not _ION["sutun"][0]["engel"] and not _ION["sutun"][1]["engel"], "v63: icecek yedeginin onunde (kapak acikken) engel var: %s" % _ION')

# 6 · birim önekleri (K, E yeni ön parçaları ve bulaşık tablası)
degis('("ayak_", "taban_sac", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "taban_kapisi", "ust_kapi", "kapi_kilidi", "acil_stop")),',
      '("ayak_", "taban_sac", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "taban_kapisi", "ust_kapi", "kapi_kilidi", "acil_stop",\n'
      '      "onyuz_", "bulasik_")),   # v63: ön çerçeve + 3 kapak (tava 20) + bulaşık tablası / geçiş lastikleri')
degis('"sarjor_yan_kapisi", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_")),',
      '"sarjor_yan_kapisi", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_", "onyuz_")),   # v63: ön çerçeve + kapaklar')
degis('ön kapak YOK (kesme v2 · v58: ön taraflara kapak yok, Kemal)', 'v63: 3 kapak (alt bulaşık · orta · üst, tava 20, ön düzlem +79) + ön çerçeve')

# 7 · ön kapaklar şeffaf gösterim — bütün modüllerde onyuz_ önekli parçalar
degis('ON_SEFFAF = _re61.compile(r"^(CEK_K\\d_[a-z0-9]+_\\d+_on_(dis_sac|pu|ic_sac|fitil)|k4_kapak_|k4_izgara_|serit_on_|klape_levhasi$|servis_kapagi_|"',
      'ON_SEFFAF = _re61.compile(r"^(onyuz_|CEK_K\\d_[a-z0-9]+_\\d+_on_(dis_sac|pu|ic_sac|fitil)|k4_kapak_|k4_izgara_|serit_on_|klape_levhasi$|servis_kapagi_|"')
degis('for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR)):',
      'for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR), ("K", KS.PARCALAR), ("A", AK.PARCALAR), ("D", FU.PARCALAR), ("BULASIK", BM.PARCALAR), ("TU", TU.P)):')
degis('            TC.PARCALAR[:] = []; TC.modul()\n',
      '            TC.PARCALAR[:] = []; TC.modul()\n'
      '            for _p63 in TC.PARCALAR:                                               # v63: TOPPING ön kapakları (TC yeniden kurulunca) şeffaf gösterim\n'
      '                if ON_SEFFAF.match(_p63["ad"]): _p63["mal"] = "on_seffaf"\n')
# fırın kabuğu ön saclarla aynı ton
degis('FT.kur(ayak=False, plaka=False, uyarla=True)',
      'FT.kur(ayak=False, plaka=False, uyarla=True)\n'
      'for _p63 in FT.PARCALAR:                                                               # v63: fırın ön kabuğu ön saclarla aynı ton (SPEC: tek ön malzeme)\n'
      '    if _p63["ad"] == "govde_kabugu": _p63["mal"] = "sac"')

# 8 · denetimler +79
degis('and -DZ - 1 <= b["z"][0] and b["z"][1] <= (FT.ZS + 1 if b["kod"] in FT.KAYAN else 1))]   # v51: fırın birimleri çıkıntıya (+79) kadar',
      'and -DZ - 1 <= b["z"][0] and b["z"][1] <= FT.ZS + 1)]   # v63: bütün istasyonlar ön düzleme (+79) kadar')
degis('    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "CEK_", "URUN__", "TOPPING_DONER__KONI")',
      '    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "URUN__")                          # v63: açıcı / koni / çekmece istisnaları KALKTI — hepsi +79 içinde')
degis('    _IZIN = {"K_GOVDE__celik": 22.5, "K_GOVDE__kirmizi": 16.5, "E_GOVDE__celik": 18.5}', '    _IZIN = {}                                                                          # v63: kulp / menteşe / acil stop dışarı çıkmaz')
degis('        if a_.startswith(_IST) or "__ACICI" in a_ or a_ in HARIC_T or not m_.P:', '        if a_.startswith(_IST) or a_ in HARIC_T or not m_.P:')
degis('        if zm > (FT.ZS + 0.5 if a_.startswith(("F_TP10_", "F_GIRIS_BANDI", "F_CIKIS_PLAKA")) else _IZIN.get(a_, 0.5)):   # v51: fırın çıkıntısı +79',
      '        if zm > FT.ZS + 0.5:                                                                     # v63: tek ön düzlem +79')
degis('    print("ON YUZ DENETIMI (z <= 0,5 mm; acici kafasi ve firin cikintisi haric): %s"', '    print("ON YUZ DENETIMI (v63: butun makine z <= +79,5 · istisna yok): %s"')
degis('("A_KABIN tabani (dolap ustu)", _bk["A_KABIN"]["y"][0], Y_DUZ)', '("A_GOVDE tabani (dolap ustu · v63 gercek kabin)", _bk["A_GOVDE"]["y"][0], Y_DUZ)')
# şeffaf istasyon yüzeyleri ön düzleme kadar
degis('            yz.append((taraf, _sef_panel(xa, xb, y0 + SEF_T, y1 - SEF_T, Z0 + SEF_T, 0.0, d_)))', '            yz.append((taraf, _sef_panel(xa, xb, y0 + SEF_T, y1 - SEF_T, Z0 + SEF_T, FT.ZS, d_)))')
degis('        yz.append(("ust", _sef_panel(x0, x1, y1 - SEF_T, y1, Z0 + SEF_T, 0.0)))', '        yz.append(("ust", _sef_panel(x0, x1, y1 - SEF_T, y1, Z0 + SEF_T, FT.ZS)))')
degis('            yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, 0.0)))', '            yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, FT.ZS)))')
degis('                d_.append((xa - 1.0, xb + 1.0, FT.YG0, FT.YG1, -FT.D_TP + FT.ZS, 1.0))', '                d_.append((xa - 1.0, xb + 1.0, FT.YG0, FT.YG1, -FT.D_TP + FT.ZS, FT.ZS + 1.0))')

# 9 · durum.json derinlik + parça etiketi hatası
degis('json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ, pafta="HAT v62 (27 Eyl gece) ·',
      'json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ + FT.ZS, arka=-DZ, on=FT.ZS, pafta="HAT v63 (28 Eyl) · ON DUZLEM +79 · TEMIZ KUTU ISTASYONLAR (SPEC_on_duzlem_v63): butun on yuzler firin on yuzu duzleminde, arka -830 sabit, derinlik 909 · A gercek kabin + robot agzi · firin ustu kabin + duser kapak · TOPPING / K / E kapakli · bulasik ayaksiz tablada · v62:')
degis('        json.dump(dict(birim={b["kod"]: dict(ad=b["ad"], mal=mal_ad(b)) for b in B}, parca=PARCA_KUTU), f, ensure_ascii=False, separators=(",", ":"))',
      '        _PK63 = {k_: ([r_ for r_ in v_ if r_[2] >= X_E - 5.0] if k_.startswith("E_") else v_) for k_, v_ in PARCA_KUTU.items()}   # v63: E-yerel (menteşe düğümü) yinelenen kayıtlar süzülür\n'
      '        json.dump(dict(birim={b["kod"]: dict(ad=b["ad"], mal=mal_ad(b)) for b in B}, parca=_PK63), f, ensure_ascii=False, separators=(",", ":"))')
degis('print("ALCAK HAT SOZLESMESI (v62 ·', 'print("ALCAK HAT SOZLESMESI (v63 ·')
for a_ in ("hat_v62.glb", "hat_v62.usdz", '"hat_v62"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v62", "v63"))
compile(s, "hat_montaj_v63.py", "exec")
io.open(os.path.join(U, "hat_montaj_v63.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v63.py yazildi · %d satir" % s.count(NL))

# 10 · (koşu düzeltmesi) gövde altı ölçümü: yeni plintler onyuz_plint (ayak gibi gövdenin altında, 60 geride)
s = io.open(os.path.join(U, "hat_montaj_v63.py"), encoding="utf-8").read()
degis('if not p["ad"].startswith(("ayak_", "plint_on", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))',
      'if not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))')
degis('if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "asansor_")))',
      'if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "asansor_")))')
compile(s, "hat_montaj_v63.py", "exec")
io.open(os.path.join(U, "hat_montaj_v63.py"), "w", encoding="utf-8").write(s)
print("duzeltme 10 yazildi")

# 11 · (koşu düzeltmesi) kaide denetimi: TOPPING ön kapakları (onyuz_, ön düzlemde 791'e iner) mekanizma tabanı ölçümüne girmez
s = io.open(os.path.join(U, "hat_montaj_v63.py"), encoding="utf-8").read()
degis('    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:"))',
      '    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:") and not a_.startswith("TOPPING:onyuz_"))   # v63: ön kapaklar kaide bandını örter')
compile(s, "hat_montaj_v63.py", "exec")
io.open(os.path.join(U, "hat_montaj_v63.py"), "w", encoding="utf-8").write(s)
print("duzeltme 11 yazildi")

# 12 · (koşu düzeltmesi) bulaşığın arka payı: K v6'nın bilinçli bağlantı geçişleri (bulasik_gecis_* rakor / lastik — su, tahliye, elektrik) sayılmaz
s = io.open(os.path.join(U, "hat_montaj_v63.py"), encoding="utf-8").read()
degis('''    _ab_k = []
    for c_, sc in _KSP:
        if _bbk(_ab, sc):''',
      '''    _ab_k = []
    for c_, sc in _KSP:
        if c_.startswith("K:bulasik_gecis_"): continue                                   # v63: makinenin bağlantı geçişleri (kesme_cad_v6) arka payda olmalı
        if _bbk(_ab, sc):''')
compile(s, "hat_montaj_v63.py", "exec")
io.open(os.path.join(U, "hat_montaj_v63.py"), "w", encoding="utf-8").write(s)
print("duzeltme 12 yazildi")
