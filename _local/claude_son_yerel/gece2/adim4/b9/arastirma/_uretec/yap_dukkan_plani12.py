# -*- coding: utf-8 -*-
"""dukkan_plani11 → dukkan_plani12 (27 Eyl 2026): FIRIN 79 mm ÖNE → F modülü 8 cm koridora çıkıntı (y 96–147 cm); robot koridoru 90 korunur → iç derinlik 263 → 271."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "dukkan_plani11.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""DUKKAN PLANI v11 (26 Eyl 2026 gece)', '"""DUKKAN PLANI v12 (27 Eyl 2026): FIRIN 79 mm ÖNE (montaj v51) → F modülü koridora 8 cm çıkıntı (y 96–147), robot koridoru 90 korundu → iç 570 × 271.\nv11 (26 Eyl 2026 gece)')
d('dukkan_plani_v11_hat543.png', 'dukkan_plani_v12_hat543_firin_one.png')
d('IC_D = HAT_D + KOR_D + DUV_D + ON_D                          # 263',
  'F_CIK = 7.9                                                 # v12: fırın gövdesi 79 mm öne → F modülü koridora çıkıntı (yalnız fırın bandı y 96–147)\nIC_D = HAT_D + F_CIK + KOR_D + DUV_D + ON_D                  # 270,9 ≈ 271 (koridor 90 çıkıntıdan ölçülür)')
d('Y_KOR0, Y_KOR1 = HAT_D, HAT_D + KOR_D', 'Y_KOR0, Y_KOR1 = HAT_D + F_CIK, HAT_D + F_CIK + KOR_D       # v12: koridor çıkıntının önünden başlar')
d('''    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_D)], fill=SICAK if ad.startswith("F") else FILL, outline=LINE, width=3)
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 - 10), ad, f9 if x1 - x0 < 100 else f11, INK, "mm")
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 + 8), "%s × 83" % sayi(x1 - x0), f7, GRAY, "mm")''',
  '''    _dF = F_CIK if ad.startswith("F") else 0.0
    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_D + _dF)], fill=SICAK if ad.startswith("F") else FILL, outline=LINE, width=3)
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 - 10), ad, f9 if x1 - x0 < 100 else f11, INK, "mm")
    txt(X((x0 + x1) / 2), Y(HAT_D / 2 + 8), ("%s × 83 + 8 çıkıntı (fırın bandı y 96–147)" if _dF else "%s × 83") % sayi(x1 - x0), f7, GRAY, "mm")
    if _dF:
        d.rectangle([X(x0), Y(HAT_D), X(x1), Y(HAT_D + _dF)], fill=(255, 238, 170), outline=RED, width=2)''')
d('txt(OX, 60, "AUTOKITCH  ·  DÜKKAN v11 · HAT 543  ·  A 70 · B/C 180 · F 150 · K 60 · E 83  ·  tek FR5 rayda 20–510  ·  QR sağ uçta  ·  iç 570 × 263", f38, INK)',
  'txt(OX, 60, "AUTOKITCH  ·  DÜKKAN v12 · HAT 543  ·  A 70 · B/C 180 · F 150 (+8 çıkıntı) · K 60 · E 83  ·  tek FR5 rayda 20–510  ·  QR sağ uçta  ·  iç 570 × 271", f38, INK)')
d('txt(OX, 122, "v10\'a göre: hat 350 → 543 (fırın TP10 kesitli 1500, kesme 600, kutu 830), iç genişlik 390 → 570, karton kulesi yok (kutular E şarjörü + F dolabı + fırın üstü), B\'de 4 kolon · ölçüler cm · 26 Eyl',
  'txt(OX, 122, "v11\'e göre: fırın 79 mm öne (montaj v51) → F modülü koridora 8 cm çıkıntı, robot koridoru 90 korundu, iç derinlik 263 → 271; hat 543, iç genişlik 570 aynı · ölçüler cm · 27 Eyl')
d('olcu_v(X(IC_W) + 40, Y(0), Y(HAT_D), "hat 83", f8, INK, "r")', 'olcu_v(X(IC_W) + 40, Y(0), Y(HAT_D), "hat 83", f8, INK, "r")\nolcu_v(X(IC_W) + 40, Y(HAT_D), Y(HAT_D + F_CIK), "F +8", f7, RED, "r")')
d('    "HAT 543 × 83 × 203 (montaj v48): A açıcı 70 · B çekmece 250 (altta 106) + C TOPPING 180 (üstte) ·",',
  '    "HAT 543 × 83 × 203 (montaj v51): A açıcı 70 · B çekmece 250 (altta 106) + C TOPPING 180 (üstte) ·",')
d('    "  ısıtılan 1316, aynı anda 4 ürün; kompresör + kutu yedeği fırın üstünde.",',
  '    "  ısıtılan 1316, aynı anda 4 ürün; kompresör + kutu yedeği fırın üstünde. FIRIN 79 mm ÖNE (v51):",\n    "  gövde koridora 8 cm çıkıntı (y 96–147), ürün hattı mağazadan kesiciye düz.",')
d('    "DÜKKÂN: iç 570 × 263 (v10: 390 × 263). Robot koridoru 90, ince duvar 6, ön zon 84 aynı.",',
  '    "DÜKKÂN: iç 570 × 271 (v11: 570 × 263). Robot koridoru 90 çıkıntıdan ölçülür, ince duvar 6, ön zon 84 aynı.",')
d('"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v11_hat543 · 26 Eyl 2026 · üretici _uretec/dukkan_plani11.py"',
  '"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v12_hat543_firin_one · 27 Eyl 2026 · üretici _uretec/dukkan_plani12.py"')
io.open(os.path.join(U, "dukkan_plani12.py"), "w", encoding="utf-8").write(s)
print("dukkan_plani12.py yazildi")
