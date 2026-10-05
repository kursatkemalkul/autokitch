# -*- coding: utf-8 -*-
"""hat_montaj_v58 → hat_montaj_v59 (27 Eyl 2026 gece) — SOĞUTMA STANDART DÜZEN (Kemal: "öğrendiğin yeter, cooling'de de onlarla yap" ·
"hamur fırıncıdan soğuk gelemez"). B = store_cad_v7 (yap_store_cad_v7). Montajda yalnız B kaynağı, B birim metinleri, sözleşmeye 1 eşitlik,
pafta metni ve çıktı adları değişir; başka davranış DEĞİŞMEZ. v58 DEĞİŞMEZ, çıktı yalnız hat_montaj_v59.py."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v58.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# 1 · tarihçe başı
degis('"""v58 (27 Eyl 2026 gece):',
      '"""v59 (27 Eyl 2026 gece): SOĞUTMA STANDART DÜZEN — B = store_cad_v7 (Kemal: "öğrendiğin yeter, cooling\'de de onlarla yap" · "hamur fırıncıdan soğuk gelemez"):' + NL +
      '  Secop CU NLE8.8CN (297 yüksek, K4 ara katman +25) · 6 roll-bond + 7 FNH fan yerine 2 bölge lamelli epoksi kaplı evaporatör + 4 × 4414 FL · bölmelerde' + NL +
      '  arka hava geçişi · damlama teknesi → Ø12 gider → plintte kondenser atış kanalı + buharlaştırma tavası · fırın altında PU 60 yerine hava boşluğu +' + NL +
      '  parlak paslanmaz ışınım sacı + arka yarıklar · sol yan PU 60. Montajda yalnız B kaynağı + metinler + çıktı adları (hat_v59) değişti.' + NL +
      'v58 (27 Eyl 2026 gece):')
# 2 · kod gövdesinde store_cad_v6 → store_cad_v7 (tarihçe olduğu gibi kalır)
i = s.index('\nimport importlib, io')
n6 = s[i:].count("store_cad_v6"); assert n6 >= 10, n6
s = s[:i] + s[i:].replace("store_cad_v6", "store_cad_v7")
# 3 · B birim metinleri
degis("fırın altında PU 60 ısı kalkanı (2517–3793 × 728–788)",
      "sol yan PU 60 · fırın altında HAVA BOŞLUKLU ısı kalkanı (v59: PU yok — ayırma sacı 728 + parlak paslanmaz ışınım sacı 740 + arka 6 yarık · fırın kirişlere oturur)")
degis('"B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 6 roll-bond evaporatör + 6 fan (soğutma yükü hesabı AÇIK)"',
      '"B_SOGUTMA": "Soğutma (v59 standart düzen · sogutma_hesabi_v1): Secop CU NLE8.8CN R290 688 W @ −10/32 °C (gereken 552–661 W) K4 altında ızgaralı kapak arkasında · '
      '2 bölge lamelli epoksi kaplı evaporatör (sol K2 arkası → K1–K3 · sağ K5 arkası → K4 depo + K5–K6) + davlumbaz + 4 × ebm-papst 4414 FL · bölmelerde arka hava geçişleri · '
      'damlama teknesi → Ø12 gider → plintte kondenser atış kanalı + buharlaştırma tavası"')
# 4 · sözleşme: iki bölge / dört fan
degis('''    ("v58 · E on_alt_sac parcasi = 0 (kutu_cad_v6 · icecek yedeginin onu acik)",''',
      '''    ("v59 · B lamelli evaporator + 4414 FL fan = 2 + 4 (store_cad_v7 · sogutma standart duzen)", (float(len([p for p in SC.PARCALAR if p["ad"] in ("evaporator_sol_lamel", "evaporator_sag_lamel")])
      + len([p for p in SC.PARCALAR if p["ad"] in ("fan_sol_1", "fan_sol_2", "fan_sag_1", "fan_sag_2")])), 6.0)),
    ("v58 · E on_alt_sac parcasi = 0 (kutu_cad_v6 · icecek yedeginin onu acik)",''')
degis('print("ALCAK HAT SOZLESMESI (v58 ·', 'print("ALCAK HAT SOZLESMESI (v59 ·')
# v59: plintteki soğutma parçaları (atış kanalı, buharlaştırma tavası, gider) ayak gibi gövdenin ALTINDA — gövde altı ölçümüne girmez
degis('''    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))''',
      '''    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))''')
# 5 · pafta metni + çıktı adları
degis('pafta="HAT v58 (27 Eyl gece) ·',
      'pafta="HAT v59 (27 Eyl gece) · SOGUTMA STANDART DUZEN (Kemal: ogrendigin yeter, coolingde de onlarla yap · hamur firincidan soguk gelemez): B = store_cad_v7 '
      '(Secop CU NLE8.8CN 688 W @ -10/32 C · 2 bolge lamelli evaporator + 4 fan 4414 FL · bolmelerde arka hava gecisi · damlama -> gider -> plintte atis kanali + '
      'buharlastirma tavasi · firin alti PU yerine hava boslugu + isinim saci · sol yan PU 60) · ACIK: sogutucu hatlari, cerceve isiticisi, havalandirma debisi olcum · v58:')
for a_ in ("hat_v58.glb", "hat_v58.usdz", '"hat_v58"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v58", "v59"))
_kod = s[s.index('\nimport importlib, io'):]
for _eski in ("import store_cad_v6", '"store_cad_v6.py"', "hat_v58.glb", "hat_v58.usdz", "KLF4.0CND R290 (K4 altı"):
    assert _eski not in _kod, "v59: eski ad kaldi: %s" % _eski
for _yeni in ("import store_cad_v7 as SC", '"store_cad_v7.py"', "hat_v59.glb", "hat_v59.usdz", 'pafta="HAT v59', "v59 · B lamelli evaporator"):
    assert _yeni in s, "v59: eksik: %s" % _yeni
compile(s, "hat_montaj_v59.py", "exec")
io.open(os.path.join(U, "hat_montaj_v59.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v59.py yazildi · %d satir" % s.count(NL))
