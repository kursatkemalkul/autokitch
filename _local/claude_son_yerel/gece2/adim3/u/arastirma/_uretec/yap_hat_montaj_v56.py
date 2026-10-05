# -*- coding: utf-8 -*-
"""hat_montaj_v55 → hat_montaj_v56 (27 Eyl 2026) — Kemal: "tamam yalıtım sadece hacmi sarsın" + "koliyi aşağı taşı içeceği".
TOPPING = topping_uno_cad_v11 (yalıtım yalnız soğuk hacmi sarar, teknik cep dışarıda) · yan PU duvarlar görünür (yarı saydam) ·
hava ana hattı teknik cepte y 1977'de düz (zarflar 1731,5–1971,5'e çıktı) · İÇECEK 5 koli F dolabında (fırın üstünden indi): sol sütun 3 + sağ sütun 2."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v55.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v55 (27 Eyl 2026):', '"""v56 (27 Eyl 2026): TOPPING yalıtımı YALNIZ SOĞUK HACMİ SARAR (uno v11, teknik cep dışarıda) · yan PU duvarlar görünür · içecek 5 koli F dolabında (fırın üstünden indi)' + NL + 'v55 (27 Eyl 2026):')
s = s.replace('"topping_uno_cad_v10.py + topping_cad_v24.py"', '"topping_uno_cad_v11.py + topping_cad_v24.py"').replace('"sac", "topping_uno_cad_v10.py", "hat/topping_v2.html")', '"sac", "topping_uno_cad_v11.py", "hat/topping_v2.html")')
degis('_sp = _ilu.spec_from_file_location("TU10", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v10.py"))',
      '_sp = _ilu.spec_from_file_location("TU11", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v11.py"))   # v56: yalıtım yalnız soğuk hacmi sarar')
degis('ANA_V44 = [(3090, 1977, -380), (3090, 1977, -432), (1830, 1977, -432), (1830, 1950, -432), (1640, 1950, -432), (1640, 1950, -740), (1640, 1335, -740), (1650, 1335, -740)]',
      'ANA_V44 = [(3090, 1977, -380), (3090, 1977, -432), (1640, 1977, -432), (1640, 1977, -740), (1640, 1335, -740), (1650, 1335, -740)]   # v56: teknik cepte 1977 düz (zarflar 1731,5–1971,5)')
degis('''    elif _q["ad"].startswith("teknik_ayirma_saci"):
        _q["mal"] = "ayirma_saci"''', '''    elif _q["ad"].startswith("teknik_ayirma_saci"):
        _q["mal"] = "ayirma_saci"
    elif _q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU"):                       # v56: yan PU duvarlar da görünür
        _q["mal"] = "yalitim_gorunur"''')
degis('"kabin_sol_duvar", "kabin_sag_duvar", ', '')
i = s.index('birim("D_ICECEK_YEDEK_UST",'); j = s.index('birim("D_PIZZA_YEDEK_UST",')
s = s[:i] + '''birim("D_ICECEK_YEDEK_A", "İçecek yedeği · F dolabı pizza gözü önde SOL sütun · 3 koli × 24 = 72 · koli 400 × 267 × 123 · soğutmasız (Kemal 27 Eyl: aşağı taşı)", "D", "KUTU",
      (3170.0, 3570.0), (130.0, 499.0), (-287.0, -20.0), "karton", "v56 · kural 5.3")
birim("D_ICECEK_YEDEK_B", "İçecek yedeği · F dolabı pizza gözü önde SAĞ sütun · 2 koli × 24 = 48 · toplam 120: soğuk 160 + 120 = 280 = 4 gün", "D", "KUTU",
      (3570.0, 3970.0), (130.0, 376.0), (-287.0, -20.0), "karton", "v56 · kural 5.3")
''' + s[j:]
degis('pafta="HAT v55 (27 Eyl) ·', 'pafta="HAT v56 (27 Eyl) · TOPPING yalitimi yalniz soguk hacmi sarar (uno v11, teknik cep disarida, L PU 30) · icecek 5 koli F dolabinda (3 + 2) · v55:')
degis('print("ANA MONTAJ ANIMASYONU (v55):', 'print("ANA MONTAJ ANIMASYONU (v56):')
s = s.replace('hat_v55.glb', 'hat_v56.glb').replace('hat_v55.usdz', 'hat_v56.usdz').replace('"hat_v55"', '"hat_v56"')
io.open(os.path.join(U, "hat_montaj_v56.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v56.py yazildi")
