# -*- coding: utf-8 -*-
"""dukkan_plani12 → dukkan_plani13 (27 Eyl 2026): pizza kutusu yedeği tek yerde fırın üstü sol (320); dolap pizza gözü boş."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "dukkan_plani12.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""DUKKAN PLANI v12 (27 Eyl 2026)', '"""DUKKAN PLANI v13 (27 Eyl 2026): pizza kutusu yedeği TEK YERDE fırın üstü sol (320), dolap pizza gözü boş (UM+ bulaşık yeri).\nv12 (27 Eyl 2026)')
d('dukkan_plani_v12_hat543_firin_one.png', 'dukkan_plani_v13_hat543_kutu_ustte.png')
d('"fırın üstü: kutu yedeği 55 + kompresör"', '"fırın üstü SOL: kutu yedeği 320 (tek yer) · SAĞ: kompresör"')
d('"AUTOKITCH  ·  DÜKKAN v12 · HAT 543', '"AUTOKITCH  ·  DÜKKAN v13 · HAT 543')
d('    "  ısıtılan 1316, aynı anda 4 ürün; kompresör + kutu yedeği fırın üstünde. FIRIN 79 mm ÖNE (v51):",',
  '    "  ısıtılan 1316, aynı anda 4 ürün; kutu yedeği TEK YERDE fırın üstü sol (320, 3,1 gün) + kompresör sağ. FIRIN 79 mm ÖNE (v51):",')
d('"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v12_hat543_firin_one · 27 Eyl 2026 · üretici _uretec/dukkan_plani12.py"',
  '"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v13_hat543_kutu_ustte · 27 Eyl 2026 · üretici _uretec/dukkan_plani13.py"')
io.open(os.path.join(U, "dukkan_plani13.py"), "w", encoding="utf-8").write(s)
print("dukkan_plani13.py yazildi")
