# -*- coding: utf-8 -*-
"""topping_uno_cad_v8 → topping_uno_cad_v9 (27 Eyl 2026): ÖN FİTİL YİNE TAM (v8'deki 130 mm itici boşluğu kalktı):
fırın 79 öne alındı, aktarma iticisi (itici_cad_v3) x boyunca düz itiyor, gövdesi ön düzlemi kesmiyor."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v8.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v8 · 26 Eyl 2026 gece (v7 + fitil alt şeridinde itici boşluğu 1325–1455)\nv8: ön fitilin alt şeridi yerel x 1325–1455 arasında kesik (aktarma iticisi çapraz hattı ön düzlemi keser; ön kapak yok — Kemal). Önceki: topping_uno_cad_v7.py',
  '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v9 · 27 Eyl 2026 (v8 − fitil boşluğu: fırın 79 öne, itici v3 düz → ön fitil yine TAM)\nv9: ön fitil kesiksiz (aktarma iticisi düz itiyor, ön düzlemi kesmiyor). Önceki: topping_uno_cad_v8.py\nv8: ön fitilin alt şeridi yerel x 1325–1455 arasında kesik (aktarma iticisi çapraz hattı ön düzlemi keser; ön kapak yok — Kemal). Önceki: topping_uno_cad_v7.py')
d("_ftl = _dis.cut(_ic).cut(kut(FITIL_BOSLUK[0], FITIL_BOSLUK[1], YAL_Y0 - FITIL_W - 1.0, YAL_Y0 + 1.0, Z_KAPAK[1] - 1.0, Z_KAPAK[1] + FITIL_T + 1.0))",
  "_ftl = _dis.cut(_ic)                                                                  # v9: boşluk YOK (itici v3 düz, ön düzlemi kesmiyor)")
d("· v8: alt şerit 1325–1455 arasında KESİK (aktarma iticisinin kolsuz silindiri ön düzlemi keser; ön kapak yok — Kemal) ·",
  "· v9: KESİKSİZ (fırın 79 öne, aktarma iticisi v3 x boyunca düz: ön düzlemi kesmiyor; ön kapak yok — Kemal) ·")
d('kontrol("ön fitil alt şeridi %.0f–%.0f arasında kesik (itici geçidi) · hacim %.0f = 0" % (FITIL_BOSLUK[0], FITIL_BOSLUK[1], _ftk), _ftk < 1.0)',
  'kontrol("ön fitil alt şeridi %.0f–%.0f arasında KESİKSİZ (v9: itici düz) · hacim %.0f > 0" % (FITIL_BOSLUK[0], FITIL_BOSLUK[1], _ftk), _ftk > 1.0)')
for a, b in (("topping_uno_v8.glb", "topping_uno_v9.glb"), ("topping_uno_v8.json", "topping_uno_v9.json"), ('surum="topping_uno_cad_v8', 'surum="topping_uno_cad_v9'),
             ('"generator": "AUTOKITCH topping_uno_cad_v8"', '"generator": "AUTOKITCH topping_uno_cad_v9"')):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
io.open(os.path.join(U, "topping_uno_cad_v9.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v9.py yazildi")
