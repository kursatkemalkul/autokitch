# -*- coding: utf-8 -*-
"""hat_montaj_v82 (Codex: E kutu v9, head 396acd9) → hat_montaj_v83 (29 Eyl 2026 · YEREL) — Kemal: "yap herşeyi düzgün yap temiz olsun" (TOPPING soğuk kutusu):
· topping_uno_cad_v16: soğuk kutu köpük dolgulu sandviç, HER YÜZ 60 (iç 304 + PU 57,5 + dış 1,5) · yan dış kabuk = TC yan sacı (28,5 boşluk + Z profil yok) ·
  iç kaplama tek parça · taban 43 (UNO ağzı sınırı) · evaporatör yalıtımın İÇİNDE (A tavanı) · yayıcı kesme valfi tabanın altında
· topping_cad_v29: teknik cep konsolsuz — cihazlar kutunun üstünde titreşim pedlerinde · Secop CU KLF4.8CND gerçek ölçü · kuru bölmedeki çıplak evaporatör kalktı
· topping_v2_hesap_v2: sucuk spirali r 30'da biter → kaset dönüş süpürmesi ↔ yükleme bandı 4,7 → ≈27 mm (istasyon aralıkları artık hesaptan)
· TU modül denetimi montajda da zorunlu (den_assert). Çıktılar hat_v83."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v82.py"), encoding="utf-8-sig").read()
NL = chr(10)


def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)


degis('pafta="HAT v82 (29 Eyl · YEREL) ·', 'pafta="HAT v83 (29 Eyl · YEREL) · TOPPING SOGUK KUTU HER YUZ 60 SANDVIC (ic 304 + PU + dis sac · yan dis kabuk = istasyon saci, bosluk / Z profil yok · taban 43) · TEKNIK CIHAZLAR KUTU USTUNDE (konsol yok, Secop CU KLF4.8CND) · EVAPORATOR YALITIM ICINDE (A tavani) · SUCUK SPIRALI r 30 (yukleme bandina ~27 mm) · v82:')
degis('print("ALCAK HAT SOZLESMESI (v82 ·', 'print("ALCAK HAT SOZLESMESI (v83 ·')
for a_ in ("hat_v82.glb", "hat_v82.usdz", '"hat_v82"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v82", "v83"))
degis('import topping_hesap_v7 as TH, topping_cad_v28 as TC ', 'import topping_hesap_v7 as TH, topping_cad_v29 as TC ')        # v83: teknik cep kutunun üstünde
degis('"sac", "topping_uno_cad_v15.py (dünya y −168) + topping_cad_v27.py (yerel y + 892)", "hat/topping_v2.html")',
      '"sac", "topping_uno_cad_v16.py (dünya y −168) + topping_cad_v29.py (yerel y + 892)", "hat/topping_v2.html")')
degis('(-420.0, -40.0), "sac", "topping_uno_cad_v15.py", "hat/topping_v2.html")', '(-420.0, -40.0), "sac", "topping_uno_cad_v16.py", "hat/topping_v2.html")')
degis('_sp = _ilu.spec_from_file_location("TU11", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v15.py"))',
      '_sp = _ilu.spec_from_file_location("TU11", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v16.py"))   # v83: soğuk kutu 60 sandviç + evaporatör içeride')
degis('TU = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TU)',
      'TU = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TU)' + NL +
      '_n_tu = TU.den_assert(); print("v83 · TU topping_uno_cad_v16 modul denetimi %d / %d GECTI (den_assert zorunlu)" % (_n_tu, _n_tu))')
degis('("v60 · TOPPING yalitimi modelde: yan PU 2 + alt sac + alt PU = 4 (topping_uno_cad_v15)"', '("v60 · TOPPING yalitimi modelde: yan PU 2 + alt sac + alt PU = 4 (topping_uno_cad_v16)"')
degis('    import topping_v2_hesap_v1 as TH2', '    import topping_v2_hesap_v2 as TH2                                             # v83: sucuk spirali r 30')
degis('''    _IST = [("sos", 910.0, 910.0), ("harc", 1260.0, 1260.0), ("kiyma", 1483.0, 1707.0), ("kusbasi", 1693.0, 1917.0), ("kasar", 1956.0, 2061.0), ("sucuk", 2187.0, 2293.0)]   # bantli_tabla_cad_v1 ISTASYON (dünya, tabla ekseni x)''',
      '''    import topping_v2_hesap_v2 as _TH2                                                   # v83: istasyon aralıkları dozaj hesabından (sucuk r_ic 30 → tabla 22,4 mm erken durur)
    _IST = []
    for _i2 in _TH2.IST:
        _x2 = X_BC + _i2["x"]
        if _i2["tip"] == "YAYICI":
            _IST.append((_i2["kod"].lower(), _x2, _x2)); continue
        _d2 = _TH2.spiral(_i2, 100.0)
        if _i2["tip"] == "NOKTA": _IST.append((_i2["kod"].lower(), _x2 - _d2["r_dis"], _x2 + _d2["r_dis"]))                   # iki yan (v81 ile aynı, temkinli)
        else: _IST.append((_i2["kod"].lower(), X_BC + _TH2.tabla_x(_i2, _d2["r_dis"]), X_BC + _TH2.tabla_x(_i2, _d2["r_ic"])))
    _IST = [(a_, round(min(u_, v_), 1), round(max(u_, v_), 1)) for a_, u_, v_ in _IST]
    print("   v83 · kaset donus istasyonlari (dunya tabla ekseni x, topping_v2_hesap_v2): %s" % _IST)''')
s = s.replace('"""', '"""hat_montaj_v83 (29 Eyl 2026 · YEREL · Codex v82 üstüne): TOPPING soğuk kutu 60 sandviç (TU v16) · teknik cep kutu üstünde (TC v29) · evaporatör içeride · sucuk r_ic 30 (TH2 v2) — yap_hat_montaj_v82.py.\n', 1)
compile(s, "hat_montaj_v83.py", "exec")
io.open(os.path.join(U, "hat_montaj_v83.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v83.py yazildi")
