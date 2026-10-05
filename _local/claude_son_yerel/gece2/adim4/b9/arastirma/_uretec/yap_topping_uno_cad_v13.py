# -*- coding: utf-8 -*-
"""topping_uno_cad_v12.py -> topping_uno_cad_v13.py (27 Eyl 2026 gece) · YAN YALITIM = ÜST YALITIM
Kemal: "yalıtım neden sağ solda daha derin, üstle aynı olsun; derinlik ön yüzeyleri aynı planda olsun, kalınlıkları da üstle aynı".
v12'de yan PU duvarlar 90 kalın ve z 0 … −830 (tam derinlik) idi; üst yalıtım (A tavanı) 60 kalın, z −104 … −630.
v13: iki yan duvar 60 kalın (iç yüzleri soğuk oda sınırında: x 30–90 · 1710–1770), z −104 … −630 (ön yüz üstle aynı düzlemde),
sol duvarın üstü üst PU'nun üstüyle aynı (YUST − 1,5). Soğuk oda iç ölçüsü DEĞİŞMEZ.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v12.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v12 · 27 Eyl 2026 gece (v11 + SOĞUK ODANIN ALTINA YALITIM',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v13 · 27 Eyl 2026 gece (v12 + YAN YALITIM = ÜST YALITIM — Kemal: "ön yüzeyleri aynı planda, kalınlıkları üstle aynı")' + NL +
      'v13: yan PU duvarlar 90 → 60 kalın (x 30–90 · 1710–1770), z 0…−830 → −104…−630 (üst yalıtımla aynı ön ve arka düzlem); soğuk oda iç ölçüsü aynı.' + NL +
      '    Önceki: topping_uno_cad_v12.py (yap_topping_uno_cad_v13.py)' + NL +
      'v12 (27 Eyl gece): (v11 + SOĞUK ODANIN ALTINA YALITIM')
# yan duvarlar: üst yalıtımla aynı kalınlık (A tavanı 60) ve aynı ön / arka düzlem (Z_KAPAK[1] … Z_BOLME[1])
degis('ekle("kabin_sol_duvar_PU", kut(0, 90, 1277.0, YUST, 0, -D), "pu", "V",',
      'YAN_T = YUST - 1.5 - TAVAN_A                                                              # v13: üst yalıtımın kalınlığı (60,5 ≈ 60) → yanlar da bu\n'
      'ekle("kabin_sol_duvar_PU", kut(BAY_A[0] - 60.0, BAY_A[0], 1277.0, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "pu", "V",')
degis('ekle("kabin_sag_duvar_PU", kut(W - 90, W, 1277.0, Y_TEK, 0, -D), "pu", "V",',
      'ekle("kabin_sag_duvar_PU", kut(BAY_B[1], BAY_B[1] + 60.0, 1277.0, Y_TEK, Z_KAPAK[1], Z_BOLME[1]), "pu", "V",')
degis('not_="sac + PU 60 · v7: 1277\'den başlar', 'not_="v13: PU 60 · ön yüz −104 / arka −630 = üst yalıtımla aynı düzlem · v7: 1277\'den başlar')
degis('not_="v11: yalnız soğuk hacim yüksekliği 1277–1720 (üstü teknik cep, yalıtımsız)"',
      'not_="v13: PU 60 · ön yüz −104 / arka −630 = üst yalıtımla aynı · v11: yalnız soğuk hacim yüksekliği 1277–1720 (üstü teknik cep, yalıtımsız)"')
# denetim
degis('kontrol("kabin yan PU duvarları 1277\'den başlıyor (mekanizma bölgesi serbest)", all(p["sh"].BoundingBox().ymin >= 1276.99 for p in _sd))',
      '''kontrol("kabin yan PU duvarları 1277'den başlıyor (mekanizma bölgesi serbest)", all(p["sh"].BoundingBox().ymin >= 1276.99 for p in _sd))
_ust = bb("yalitim_blogu")
for p in _sd:
    b_ = p["sh"].BoundingBox()
    kontrol("v13 · %s: kalınlık %.0f (üst %.1f) · ön yüz z %.0f = üst ön yüz %.0f · arka z %.0f = üst arka %.0f · iç yüz soğuk oda sınırında"
            % (p["ad"], b_.xlen, YAN_T, b_.zmax, _ust.zmax, b_.zmin, _ust.zmin),
            abs(b_.xlen - 60.0) < 0.01 and abs(b_.zmax - _ust.zmax) < 0.01 and abs(b_.zmin - _ust.zmin) < 0.01 and (abs(b_.xmax - BAY_A[0]) < 0.01 or abs(b_.xmin - BAY_B[1]) < 0.01))''')
for a_ in ('glb_yaz(os.path.join(OUT, "topping_uno_v12.glb"))', 'open(os.path.join(OUT, "topping_uno_v12.json"), "w"', 'surum="topping_uno_cad_v12 · %s"'):
    degis(a_, a_.replace("v12", "v13"))
io.open(os.path.join(U, "topping_uno_cad_v13.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v13.py yazildi")
