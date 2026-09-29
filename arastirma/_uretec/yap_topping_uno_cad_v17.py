# -*- coding: utf-8 -*-
"""topping_uno_cad_v16 → topping_uno_cad_v17 (29 Eyl 2026 · YEREL) — Kemal: "o teknik kısmını görmeyelim; sanayi tipi buzdolaplarında önüne panel koyuyor,
sacdan delikleri olan, oradan geliyor hava".
  · EVAPORATÖR KAPAĞI: A tavanındaki evaporatörün önü ve altı AISI 304 1,0 yarıklı kapakla kapandı (sanayi dolabı düzeni) — içeriden yalnız düz, delikli sac
    görünür · ön ızgara = üfleme (63 yarık 60 × 6) · alt sacın arka yarısı = dönüş ızgarası (45 yarık 60 × 6) · kapak 4 × M4 ile sökülür (servis)
  · içi hava yoluna göre düzenlendi: dönüş bölmesi arkada (z −559…−400) → lamel paketi −400…−260 → fan −260…−210 → üfleme kanalı → ön ızgara
  · SOĞUTMA HATLARI ODADAN ÇIKTI: v16'da A tavanı boyunca (HARÇ haznesinin üstünden) L duvarına gidiyordu → artık evaporatörün arkasından arka duvardaki POM bloktan
    kuru bölmeye, oradan teknik cepteki yoğuşma ünitesinin ARKA yüzüne · L duvarı yine deliksiz · soğuk odada görünen teknik parça yok
  · tek başına çalışınca GLB klasörü yoksa açılır. Başka değişiklik yok. Önceki: topping_uno_cad_v16.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v16.py"), encoding="utf-8").read()
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


degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v16 · 29 Eyl 2026 · YEREL (v15 + SOĞUK KUTU KÖPÜK DOLGULU SANDVİÇ, HER YÜZ 60 · EVAPORATÖR İÇERİDE · yap_topping_uno_cad_v16.py)',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v17 · 29 Eyl 2026 · YEREL (v16 + EVAPORATÖR KAPAĞI (yarıklı paslanmaz ızgara) + SOĞUTMA HATLARI ARKA DUVARDAN · yap_topping_uno_cad_v17.py)' + NL +
      'v17: Kemal "o teknik kısmını görmeyelim — sanayi dolaplarında önüne delikli sac panel konur, hava oradan gelir": ön ızgara (üfleme) + alt dönüş ızgarası · hatlar odadan çıktı' + NL +
      'v16: topping_uno_cad_v16 · 29 Eyl 2026 · YEREL (v15 + SOĞUK KUTU KÖPÜK DOLGULU SANDVİÇ, HER YÜZ 60 · EVAPORATÖR İÇERİDE · yap_topping_uno_cad_v16.py)')

# ---- evaporatör: gövde (üst + yanlar + arka) + KAPAK (ön ızgara + alt sac, arka yarısı dönüş ızgarası) · içi hava yoluna göre
blok('_g = _g.union(kut(_ex0, _ex1, _ey0, _ey0 + 1.0, -322.0, _ez1))                        # ön-alt sac (fan + üfleme kanalının altı)',
     'eğimle sol-arka köşedeki Ø8 çıkışa")',
     '''ekle("evaporator_govdesi", _g, "paslanmaz", "V",
     not_="v17 · evaporatör gövdesi AISI 304 1,0 (üst + yanlar + arka) · 260 × 208 × 500 · A tavan kaplamasına 4 × M6 perçin somun (köpük içi takviye lama) · önü ve altı yarıklı KAPAKLA kapalı · YER ZARFI (soğutmacı firma)")
# v17 · EVAPORATÖR KAPAĞI (Kemal: "teknik kısmı görmeyelim — sanayi dolaplarında önüne delikli sac panel konur, hava oradan gelir"): ön ızgara + alt sac tek parça
#       (L büküm) · lazer yarık 60 × 6, hatve 9 · üfleme öndeki yarıklardan tavan boyunca kapıya, dönüş alt sacın arka yarısındaki yarıklardan · 4 × M4 ile sökülür
EV_Q = 300.0 / (1.2 * 1005.0 * 4.0)                                                   # m³/s · 300 W, hava ΔT 4 K (sogutma_topping_v1 yükü) → ≈0,062
EV_KOL = [(_ex0 + _ex1) / 2.0 + d_ for d_ in (-80.0, 0.0, 80.0)]                      # yarık kolonları (60 genişlik)
EV_ON_Y = [1771.0 + 9.0 * i_ for i_ in range(21)]                                     # ön ızgara sıraları (y · 6 yükseklik)
EV_DON_Z = [-553.0 + 9.0 * i_ for i_ in range(15)]                                    # dönüş ızgarası sıraları (z · 6 derinlik) → −553…−421
_kp = kut(_ex0 + 1.0, _ex1 - 1.0, _ey0 + 1.0, _ey1 - 1.0, _ez1 - 1.0, _ez1).union(kut(_ex0 + 1.0, _ex1 - 1.0, _ey0, _ey0 + 1.0, _ez0 + 1.0, _ez1))
for _xk in EV_KOL:
    for _yr in EV_ON_Y:
        _kp = _kp.cut(kut(_xk - 30.0, _xk + 30.0, _yr, _yr + 6.0, _ez1 - 2.0, _ez1 + 1.0))
    for _zr in EV_DON_Z:
        _kp = _kp.cut(kut(_xk - 30.0, _xk + 30.0, _ey0 - 1.0, _ey0 + 2.0, _zr, _zr + 6.0))
_kp = _kp.cut(sily(90.0, -392.0, 4.5, _ey0 - 1.0, _ey0 + 2.0))                      # tahliye hortumu geçişi (hortum Ø8, delik Ø9)
EV_ACIK = (len(EV_KOL) * len(EV_ON_Y) * 360.0, len(EV_KOL) * len(EV_DON_Z) * 360.0)   # mm² · üfleme / dönüş açık alanı
ekle("evaporator_kapagi", _kp, "paslanmaz", "V",
     not_="v17 · EVAPORATÖR KAPAĞI AISI 304 1,0 L büküm (ön + alt) · lazer yarık 60 × 6 hatve 9 · ön ızgara %d yarık = %.0f mm² (üfleme %.1f m/s @ %.3f m³/s) · alt dönüş ızgarası %d yarık = %.0f mm² (%.1f m/s) · "
          "içeriden yalnız düz yarıklı sac görünür (sanayi dolabı düzeni) · 4 × M4 ile sökülür"
          % (len(EV_KOL) * len(EV_ON_Y), EV_ACIK[0], EV_Q / (EV_ACIK[0] * 1e-6), EV_Q, len(EV_KOL) * len(EV_DON_Z), EV_ACIK[1], EV_Q / (EV_ACIK[1] * 1e-6)))
ekle("evaporator_lamel_paketi", kut(_ex0 + 1.0, _ex1 - 1.0, 1790.0, 1965.0, -400.0, -260.0), "aluminyum", "V",
     not_="v17 · lamel paketi (Al kanat / Cu boru) 258 × 175 × 140 · hava arkadan öne (dönüş bölmesi z −559…−400 → paket → fan) · 300–380 W @ −10 °C (gereken 231–326 W @ 32 °C · sogutma_topping_v1) · uç plakaları gövde yan saclarına · YER ZARFI")
ekle("evaporator_fani", kut(_ex0 + 55.0, _ex0 + 205.0, 1802.0, 1952.0, -260.0, -210.0), "motor", "V",
     not_="v17 · eksenel fan 150 × 150 × 50 (EC 24 V) · lamel paketinin ön çerçevesine 4 × M4 · paketten çekip ön ızgaradan tavan boyunca kapıya üfler · model / debi soğutmacı firma")
ekle("evaporator_damlama_tavasi", kut(_ex0 + 1.0, _ex1 - 1.0, 1766.0, 1790.0, -408.0, -252.0).cut(kut(_ex0 + 2.0, _ex1 - 2.0, 1767.0, 1791.0, -407.0, -253.0)), "paslanmaz", "V",
     not_="v17 · damlama tavası 304 1,0 · lamel paketinin altında · %1 eğimle sol-arka köşedeki Ø8 çıkışa")''')
degis('TAHLIYE = [(90.0, 1766.0, -470.0), (90.0, 1754.0, -470.0), (90.0, 1754.0, -660.0), (90.0, 1745.0, -660.0)]',
      'TAHLIYE = [(90.0, 1766.0, -392.0), (90.0, 1754.0, -392.0), (90.0, 1754.0, -660.0), (90.0, 1745.0, -660.0)]   # v17: tava öne geldi (arka kenarı −408)')
degis('not_="v16 · yoğuşma tahliyesi Ø8 silikon · tavadan SOS haznesinin solundan (x 86–94 < 100) arka duvara,',
      'not_="v17 · yoğuşma tahliyesi Ø8 silikon · tavadan kapağın deliğinden aşağı, SOS haznesinin solundan (x 86–94 < 100) arka duvara,')

# ---- soğutma hatları: L duvarından değil, evaporatörün arkasından arka duvardaki bloktan kuru bölmeye → teknik cepteki ünitenin arka yüzüne
blok('HAT_GECIS = (BAY_A[1], X_TEK, 1885.0, 1955.0, -425.0, -375.0)', 'not_="v16 · sıvı hattı Cu Ø6,35 · genleşme valfi / kılcal evaporatör girişinde (soğutmacı firma)")',
     '''# v17 · SOĞUTMA HATLARI ODADAN ÇIKTI (Kemal: "teknik kısmını görmeyelim"): evaporatörün arka yüzünden (z −560) arka duvardaki POM bloktan kuru bölmeye (z −660),
#       kuru bölmede sağa (x 1000), oradan teknik cepteki yoğuşma ünitesinin ARKA yüzüne (topping_cad_v29 CU, z −420) · L duvarı deliksiz · v16: A tavanı boyunca L duvarına
HAT_X, HAT_Z_KURU, HAT_X_UNITE, HAT_Z_UNITE = 290.0, -660.0, 1000.0, -420.0
HAT = {"sogutma_emis_hatti": (1935.0, 15.5), "sogutma_sivi_hatti": (1900.0, 3.2)}
HAT_GECIS = (HAT_X - 25.0, HAT_X + 25.0, 1885.0, 1955.0, Z_BOLME[1], Z_BOLME[0])      # arka duvar hat geçişi (kaplama + PU + arka dış sac)
_hg = kut(*HAT_GECIS)
for _hy, _hr in HAT.values():
    _hg = _hg.cut(silz(HAT_X, _hy, _hr, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0))
kutu_delik(kut(HAT_GECIS[0], HAT_GECIS[1], HAT_GECIS[2], HAT_GECIS[3], Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ARKA3)
ekle("sogutma_hat_gecis_blogu", _hg, "pom", "V", not_="v17 · POM-C hat geçiş bloğu 50 × 70 × 60 · ARKA duvarı boydan geçer (evaporatörün arkasında, görünmez) · iki hat deliği hat çapında (silikonla sızdırmaz)")
for _ha, (_hy, _hr) in HAT.items():
    ekle(_ha, boru([(HAT_X, _hy, _ez0), (HAT_X, _hy, HAT_Z_KURU), (HAT_X_UNITE, _hy, HAT_Z_KURU), (HAT_X_UNITE, _hy, HAT_Z_UNITE)], _hr), "koyu" if "emis" in _ha else "celik", "V",
         not_=("v17 · emiş hattı Cu Ø12,7 + Armaflex 9 mm (dış Ø31)" if "emis" in _ha else "v17 · sıvı hattı Cu Ø6,35 · genleşme valfi / kılcal evaporatör girişinde (soğutmacı firma)") +
              " · evaporatörün arkasından arka duvar bloğundan kuru bölmeye (z −660), kuru bölmede sağa, teknik cepteki yoğuşma ünitesinin arka yüzüne · soğuk odada görünmez")''')

# ---- denetim
degis('''kontrol("v16 · soğutma hatları (emiş Ø31 yalıtımlı + sıvı Ø6,35) L duvarındaki POM bloktan teknik cebe (x %.0f → %.0f) · HARÇ haznesinin üstünden: hat altı %.1f > hazne dolumda %.0f · tavan altı %.1f < %.0f"
        % (_eh.xmin, _eh.xmax, min(_eh.ymin, _sv.ymin), _hh.ymax + 15.0, max(_eh.ymax, _sv.ymax), TAVAN_A),
        _eh.xmax >= X_TEK and min(_eh.ymin, _sv.ymin) > _hh.ymax + 15.0 and max(_eh.ymax, _sv.ymax) < TAVAN_A)''',
      '''_oda_h = sum(p["sh"].intersect(_kutu2(*ODA, Z_SOGUK[1], Z_ZARF).val()).Volume() for p in P if p["ad"] in HAT)          # L biçimli soğuk oda (teknik cep hariç)
_oda_g = sum(p["sh"].intersect(kut(_ex0, _ex1, _ey0, _ey1, Z_SOGUK[1], _ez0).val()).Volume() for p in P if p["ad"] in HAT)
kontrol("v17 · soğutma hatları ODADA GÖRÜNMEZ: soğuk odadaki hat hacmi %.0f mm³ = evaporatörün arkasındaki 10 mm aralıkta %.0f mm³ (başka yerde 0) · arka duvar bloğundan kuru bölmeye (z %.0f) → teknik cep, ünitenin arka yüzü (x %.0f · z %.0f) · L duvarı deliksiz"
        % (_oda_h, _oda_g, HAT_Z_KURU, HAT_X_UNITE, HAT_Z_UNITE), abs(_oda_h - _oda_g) < 1.0 and max(_eh.zmax, _sv.zmax) <= HAT_Z_UNITE + 0.01 + 15.5)
_kb_ = bb("evaporator_kapagi")
kontrol("v17 · evaporatör KAPALI: kapak ön yüzü z %.1f (gövde önü %.0f) · alt sac y %.1f · kapak x %.0f–%.0f = gövde içi · ön ızgara %d yarık %.0f mm² (%.1f m/s) · dönüş ızgarası %d yarık %.0f mm² (%.1f m/s) @ %.3f m³/s"
        % (_kb_.zmax, _ez1, _kb_.ymin, _kb_.xmin, _kb_.xmax, len(EV_KOL) * len(EV_ON_Y), EV_ACIK[0], EV_Q / (EV_ACIK[0] * 1e-6), len(EV_KOL) * len(EV_DON_Z), EV_ACIK[1], EV_Q / (EV_ACIK[1] * 1e-6), EV_Q),
        abs(_kb_.zmax - _ez1) < 0.01 and abs(_kb_.ymin - _ey0) < 0.01 and abs(_kb_.xmin - _ex0 - 1.0) < 0.01 and abs(_kb_.xmax - _ex1 + 1.0) < 0.01 and EV_Q / (EV_ACIK[0] * 1e-6) < 4.0 and EV_Q / (EV_ACIK[1] * 1e-6) < 4.0)''')
degis('("sogutma_hat_gecis_blogu", "soguk_ic_kaplama"), ("sogutma_emis_hatti", "sogutma_hat_gecis_blogu"), ("sogutma_sivi_hatti", "sogutma_hat_gecis_blogu"),',
      '("sogutma_hat_gecis_blogu", "soguk_ic_kaplama"), ("sogutma_emis_hatti", "sogutma_hat_gecis_blogu"), ("sogutma_sivi_hatti", "sogutma_hat_gecis_blogu"), ("evaporator_kapagi", "evaporator_govdesi"),')
degis('assert not kal, "topping_uno_cad_v16 denetimi KALDI: %s" % kal', 'assert not kal, "topping_uno_cad_v17 denetimi KALDI: %s" % kal')
degis('"generator": "AUTOKITCH topping_uno_cad_v16"', '"generator": "AUTOKITCH topping_uno_cad_v17"')
degis('    _od = OUT if "--site" in sys.argv else os.path.join(U, "on_duzlem_v63")', '    _od = OUT if "--site" in sys.argv else os.path.join(U, "on_duzlem_v63"); os.makedirs(_od, exist_ok=True)   # v17: klasör yoksa aç')
degis('glb_yaz(os.path.join(_od, "topping_uno_v16.glb"))', 'glb_yaz(os.path.join(_od, "topping_uno_v17.glb"))')
degis('with open(os.path.join(_od, "topping_uno_v16.json"), "w", encoding="utf-8") as f:', 'with open(os.path.join(_od, "topping_uno_v17.json"), "w", encoding="utf-8") as f:')
degis('json.dump(dict(surum="topping_uno_cad_v16 · %s"', 'json.dump(dict(surum="topping_uno_cad_v17 · %s"')
assert "silx(1935.0, -400.0, 15.5" not in s and "teknik_ayirma_saci_dikey\"))" not in s.split("HAT_GECIS")[1][:400]
compile(s, "topping_uno_cad_v17.py", "exec")
io.open(os.path.join(U, "topping_uno_cad_v17.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v17.py yazildi")
