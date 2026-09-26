# -*- coding: utf-8 -*-
"""topping_uno_cad_v7 → topping_uno_cad_v8 (26 Eyl 2026 gece): ÖN FİTİLİN ALT ŞERİDİNDE 130 mm BOŞLUK (yerel x 1325–1455 = dünya 2025–2155):
aktarma iticisinin (itici_cad_v2) kolsuz silindir gövdesi ve montaj kirişi çapraz hatta soğuk odanın ön düzlemini (fitil −104…−98) burada
keser (montaj v49 denetimi: gövde 5776 mm³ · kiriş 3059 mm³). Kemal: TOPPING'e ön kapak yok → fitil kesintisi kabul; kapak istenirse
itici hattı ve fitil birlikte çözülür."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v7.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d("TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v7 · 26 Eyl 2026 gece",
  "TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v8 · 26 Eyl 2026 gece (v7 + fitil alt şeridinde itici boşluğu 1325–1455)\nv8: ön fitilin alt şeridi yerel x 1325–1455 arasında kesik (aktarma iticisi çapraz hattı ön düzlemi keser; ön kapak yok — Kemal). Önceki: topping_uno_cad_v7.py\nv7:")
d('''ekle("on_fitil", _dis.cut(_ic), "silikon", "H",
     not_="manyetik fitil 21 × 18,5 (sıkışınca 15) kanallı alüminyum profilde · L ağzın çevresi · ön kapak kapanınca buna basar · çekmece fitiliyle aynı profil")''',
  '''FITIL_BOSLUK = (1325.0, 1455.0)                                                       # v8: itici gövdesi/kirişi geçiyor (dünya 2025–2155)
_ftl = _dis.cut(_ic).cut(kut(FITIL_BOSLUK[0], FITIL_BOSLUK[1], YAL_Y0 - FITIL_W - 1.0, YAL_Y0 + 1.0, Z_KAPAK[1] - 1.0, Z_KAPAK[1] + FITIL_T + 1.0))
ekle("on_fitil", _ftl, "silikon", "H",
     not_="manyetik fitil 21 × 18,5 (sıkışınca 15) kanallı alüminyum profilde · L ağzın çevresi · v8: alt şerit 1325–1455 arasında KESİK (aktarma iticisinin kolsuz silindiri ön düzlemi keser; ön kapak yok — Kemal) · çekmece fitiliyle aynı profil")''')
d('''_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]''',
  '''_ftb = bb("on_fitil"); _ftk = [p for p in P if p["ad"] == "on_fitil"][0]["sh"].intersect(kut(FITIL_BOSLUK[0] + 1.0, FITIL_BOSLUK[1] - 1.0, YAL_Y0 - FITIL_W, YAL_Y0, Z_KAPAK[1], Z_KAPAK[1] + FITIL_T).val()).Volume()
kontrol("ön fitil alt şeridi %.0f–%.0f arasında kesik (itici geçidi) · hacim %.0f = 0" % (FITIL_BOSLUK[0], FITIL_BOSLUK[1], _ftk), _ftk < 1.0)
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]''')
for a, b in (("topping_uno_v7.glb", "topping_uno_v8.glb"), ("topping_uno_v7.json", "topping_uno_v8.json"), ('surum="topping_uno_cad_v7', 'surum="topping_uno_cad_v8'),
             ('"generator": "AUTOKITCH topping_uno_cad_v7"', '"generator": "AUTOKITCH topping_uno_cad_v8"')):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
io.open(os.path.join(U, "topping_uno_cad_v8.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v8.py yazildi")
