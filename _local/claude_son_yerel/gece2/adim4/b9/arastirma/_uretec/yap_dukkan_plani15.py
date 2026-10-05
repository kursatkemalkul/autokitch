# -*- coding: utf-8 -*-
"""dukkan_plani14 → dukkan_plani15 (28 Eyl 2026) — ÖN DÜZLEM +79 (montaj v63/v64):
  bütün istasyonların ön yüzü fırın ön yüzüyle aynı düzlemde (z +79) → hat derinliği 83 + 8 çıkıntı yerine düz 90,9, kırmızı çıkıntı bandı yok ·
  çekmece önleri +79'da (açık K1 önü 90,9 + 62,8 = 153,7) · K: deterjan/parlatıcı rafı yok (kesme_cad_v6), bulaşık ayaksız tablada ·
  ölçü zinciri ön yüzden: ray ekseni 28,1 · QR robot yüzü 59,1 · istasyon üreteçleri v63 sürümleri. Dükkân iç ölçüsü (570 × 271) değişmez:
  koridor v13'ten beri çıkıntıdan (90,9) ölçülüyordu."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "dukkan_plani14.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""DUKKAN PLANI v14 (27 Eyl 2026):',
      '"""DUKKAN PLANI v15 (28 Eyl 2026): ÖN DÜZLEM +79 (montaj v64) — bütün istasyonlar fırın ön yüzüne (z +79) uzadı, hat derinliği 90,9 düz;' + NL +
      '  kırmızı çıkıntı bandı yok · çekmece önleri +79 (açık K1 önü 153,7) · K deterjan rafı yok, bulaşık tablada · ölçüler ön yüzden (ray 28,1 · QR 59,1).' + NL +
      'v14 (27 Eyl 2026):')
# istasyon üreteçleri (v63 sürümleri)
degis("import store_cad_v6 as SC ", "import store_cad_v8 as SC ")
degis("import kesme_cad_v4 as KS          # K: taban 892, bant 996, bulaşık yeri, deterjan",
      "import kesme_cad_v6 as KS          # K: taban 892, bant 996, bulaşık tablada (deterjan rafı yok)")
degis("import kutu_cad_v5 as KU ", "import kutu_cad_v7 as KU ")
degis("import firin_tp10_cad_v7 as FT ", "import firin_tp10_cad_v8 as FT ")
degis("import itici_cad_v4 as IT ", "import itici_cad_v5 as IT ")
degis("import kaide_cad_v1 as KD ", "import kaide_cad_v2 as KD ")
degis('"dukkan_plani_v14_alcak_hat.png"', '"dukkan_plani_v15_on_duzlem.png"')
# ön düzlem
degis("F_CIK = cm(FT.ZS)                                            # 7,9",
      "F_CIK = cm(FT.ZS)                                            # 7,9\nHAT_ON = HAT_D + F_CIK                                       # 90,9 v15: bütün istasyonların ön yüzü (z +79)")
# deterjan kanisterleri kalktı (kesme_cad_v6)
degis("KAN_DET = [(cm(a) + 400.0, cm(b) + 400.0) for _n, a, b in KS.KANISTER_X]                 # 406–425 · 427–446" + NL, "")
degis("KAN_DET_Y, KAN_DET_H = (pz(KS.KANISTER_Z[0]), pz(KS.KANISTER_Z[1])), (cm(KS.KANISTER_Y0), cm(KS.KANISTER_Y0 + KS.KANISTER[\"y\"]))" + NL, "")
degis("# K altı: bulaşık + deterjan/parlatıcı · F altı şerit", "# K altı: bulaşık (tablada) · F altı şerit")
degis("for a, b in KAN_DET:" + NL + "    drect(X(a), Y(KAN_DET_Y[0]), X(b), Y(KAN_DET_Y[1]), ACC, 1)" + NL, "")
# başlık
degis('"AUTOKITCH  ·  DÜKKÂN v14 · ALÇAK HAT 543 × 83 × 186  ·',
      '"AUTOKITCH  ·  DÜKKÂN v15 · ÖN DÜZLEM · HAT 543 × 90,9 × 186  ·')
degis('"v13\'e göre: makine alçak hat (montaj v57 · SPEC v57): üst 203 → 186, B çekmeceli dolap 0–400 tek parça (üstü 78,8), fırın 79 öne aynı; "',
      '"v14\'e göre (montaj v64): bütün istasyonların ön yüzü fırın ön yüzüyle aynı düzlemde (z +79), arka yüz yerinde → hat 90,9 derin, çıkıntı yok; '
      'çekmece önleri +79; K deterjan rafı yok; "')
degis('"QR 86 × 52 × 205 (robot yüzü z 67); ray ekseni z 36 (3D model); personel tezgâhı 60 × 45 ön duvarda · ölçüler cm · 27 Eylül 2026"',
      '"ön yüzden: ray ekseni 28,1 · QR robot yüzü 59,1; dükkân iç ölçüsü aynı (570 × 271) · ölçüler cm · 28 Eylül 2026"')
# plan: modüller ön düzleme, kırmızı bant yok
degis("""    _dF = F_CIK if ad.startswith("F") else 0.0
    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_D + _dF)], fill=SICAK if ad.startswith("F") else FILL, outline=LINE, width=3)
    if _dF:
        d.rectangle([X(x0), Y(HAT_D), X(x1), Y(HAT_D + _dF)], fill=(255, 238, 170), outline=RED, width=2)
""", """    d.rectangle([X(x0), Y(0), X(x1), Y(HAT_ON)], fill=SICAK if ad.startswith("F") else FILL, outline=LINE, width=3)
""")
degis("drect(X(cm(a)), Y(HAT_D - 20), X(cm(b)), Y(HAT_D), GRN, 1)", "drect(X(cm(a)), Y(HAT_ON - 20), X(cm(b)), Y(HAT_ON), GRN, 1)")
degis("txt(X((cm(a) + cm(b)) / 2), Y(HAT_D - 8), KOL_ET[k], f7, GRN, \"mm\")", "txt(X((cm(a) + cm(b)) / 2), Y(HAT_ON - 8), KOL_ET[k], f7, GRN, \"mm\")")
degis('"A": "70 × 83 · dolap üstünde", "C": "180 × 83 · dolap üstünde (kaide %s)" % sayi(cm(KD.KAIDE_H)), "F": "150 × 83 + 8 çıkıntı · dolap üstünde",',
      '"A": "70 × 90,9 · dolap üstünde", "C": "180 × 90,9 · dolap üstünde (kaide %s)" % sayi(cm(KD.KAIDE_H)), "F": "150 × 90,9 · dolap üstünde",')
degis('"K": "60 × 83", "E": "83 × 83"}[ad[0]]', '"K": "60 × 90,9", "E": "83 × 90,9"}[ad[0]]')
# açık K1: ön yüz +79'dan strok 628
degis("AC_ON = HAT_D + cm(SC.STROK)                                  # 145,8 açık çekmece önü",
      "AC_ON = HAT_ON + cm(SC.STROK)                                 # 153,7 açık çekmece önü (v15: çekmece önü +79)")
degis("d.rectangle([X(K1a), Y(HAT_D), X(K1b), Y(AC_ON)], fill=(235, 250, 242), outline=GRN, width=2)",
      "d.rectangle([X(K1a), Y(HAT_ON), X(K1b), Y(AC_ON)], fill=(235, 250, 242), outline=GRN, width=2)")
degis('txtb(X(K1b / 2), Y(HAT_D + 10), "K1 AÇIK', 'txtb(X(K1b / 2), Y(HAT_ON + 10), "K1 AÇIK')
degis('txt(X(500), Y(QR_Y[0] + 32), "robot yüzü z 67", f7, GRAY, "mm")', 'txt(X(500), Y(QR_Y[0] + 32), "robot yüzü ön yüzden %s" % sayi(QR_Y[0] - HAT_ON), f7, GRAY, "mm")')
# plan ölçüleri
degis('olcu_v(X(IC_W) + 40, Y(0), Y(HAT_D), "hat 83", f8, INK, "r")' + NL +
      'olcu_v(X(IC_W) + 40, Y(HAT_D), Y(HAT_D + F_CIK), "F +8", f7, RED, "r")' + NL,
      'olcu_v(X(IC_W) + 40, Y(0), Y(HAT_ON), "hat %s" % sayi(HAT_ON), f8, INK, "r")' + NL)
degis('olcu_v(X(0) - 40, Y(HAT_D), Y(RAY_Y), "ray 36", f7, INK, "l")', 'olcu_v(X(0) - 40, Y(HAT_ON), Y(RAY_Y), "ray %s" % sayi(RAY_Y - HAT_ON), f7, INK, "l")')
degis('olcu_v(X(556.5), Y(HAT_D), Y(QR_Y[0]), "67", f8, INK, "l")', 'olcu_v(X(556.5), Y(HAT_ON), Y(QR_Y[0]), sayi(QR_Y[0] - HAT_ON), f8, INK, "l")')
degis('pratik %s) · v14"', 'pratik %s) · v15"')
# notlar
degis('"ALÇAK HAT 543 × 83 × 186 (montaj v57): B çekmeceli dolap',
      '"HAT 543 × 90,9 × 186 (montaj v64 · ön düzlem +79, arka yüz yerinde): B çekmeceli dolap')
degis("K 60 · E 83 yerden. F 79 öne (çıkıntı 8, gövde 78,8–130,5).\",",
      "K 60 · E 83 yerden. Çıkıntı yok: her istasyon ön yüzü fırınla aynı düzlemde, kapaklı temiz kutu.\",")
degis("K altı: bulaşık MEIKO + arkasında deterjan / parlatıcı · E altı", "K altı: bulaşık MEIKO ayaksız tablada, önünde K alt kapağı · E altı")
degis('"DÜKKÂN: iç 570 × 271 aynı (hat 83 + F 8 + koridor 90 + ince duvar 6 + ön zon 84). Ray ekseni z 36 = 3D model (v13 planı 25 cm = z 33 idi).",',
      '"DÜKKÂN: iç 570 × 271 aynı (hat 90,9 + koridor 90 + ince duvar 6 + ön zon 84). Ray ekseni z 36 = ön yüzden 28,1 (3D model).",')
degis("robot yüzü z 67 (koridora 31 girer)", "robot yüzü z 67 = ön yüzden 59,1 (koridora 31 girer)")
# kesitler: istasyon kutusu ön düzleme, plint 6 geride
degis("d.rectangle([uf(3), HH_(Y_PL), uf(77), ZEM], fill=SOFT, outline=LINE, width=2)       # plint (önden 6 geride)",
      "d.rectangle([uf(3), HH_(Y_PL), uf(HAT_ON - 6.0), ZEM], fill=SOFT, outline=LINE, width=2)       # plint (ön yüzden 6 geride)")
degis("d.rectangle([uf(0), HH_(H_MAK), uf(HAT_D), HH_(Y_PL)], fill=FILL, outline=LINE, width=3)",
      "d.rectangle([uf(0), HH_(H_MAK), uf(HAT_ON), HH_(Y_PL)], fill=FILL, outline=LINE, width=3)")
degis("txt((uf(0) + uf(HAT_D)) / 2, HH_(H_MAK) + 18, ad, f9, INK, \"mm\")", "txt((uf(0) + uf(HAT_ON)) / 2, HH_(H_MAK) + 18, ad, f9, INK, \"mm\")")
degis('for u0, u1, s_ in ((0, HAT_D, "hat 83"), (HAT_D, RAY_Y, "36"), (RAY_Y, QR_Y[0], "31"),',
      'for u0, u1, s_ in ((0, HAT_ON, "hat %s" % sayi(HAT_ON)), (HAT_ON, RAY_Y, sayi(RAY_Y - HAT_ON)), (RAY_Y, QR_Y[0], "31"),')
degis('for u0, u1, s_ in ((0, HAT_D, "hat 83"), (HAT_D, RAY_Y, "36"), (RAY_Y, Y_KOR1,',
      'for u0, u1, s_ in ((0, HAT_ON, "hat %s" % sayi(HAT_ON)), (HAT_ON, RAY_Y, sayi(RAY_Y - HAT_ON)), (RAY_Y, Y_KOR1,')
# K kesiti: taban sacı ön yüze, raf + deterjan yerine bulaşık tablası
degis("d.rectangle([ub(0), HH_(KT_ + 0.3), ub(HAT_D), HH_(KT_)], fill=LINE)          # (denetçi) K taban sacı 892–895 (kesme_cad_v4), 889–892 değil",
      "d.rectangle([ub(0), HH_(KT_ + 0.3), ub(HAT_ON - 4.0), HH_(KT_)], fill=LINE)          # K taban sacı 892–895 · önde kapak payı (kapak 20 + fitil)")
degis("""d.rectangle([ub(pz(KS.RAF_Z[0])), HH_(cm(KS.RAF_Y[1])), ub(pz(KS.RAF_Z[1])), HH_(cm(KS.RAF_Y[0]))], fill=LINE)
d.rectangle([ub(KAN_DET_Y[0]), HH_(KAN_DET_H[1]), ub(KAN_DET_Y[1]), HH_(KAN_DET_H[0])], fill=(225, 236, 250), outline=ACC, width=1)
_um = (KAN_DET_Y[0] + KAN_DET_Y[1]) / 2
d.line([(ub(_um), HH_(KAN_DET_H[1])), (ub(_um), HH_(83.5))], fill=ACC, width=1)
kot(ub, 1.5, 85.6, "deterjan + parlatıcı arkada", ACC, "lm")
""", """d.rectangle([ub(BUL_Y[0]), HH_(cm(KS.Y_TABLA)), ub(BUL_Y[1]), HH_(cm(KS.Y_PLINT + 3.0))], fill=LINE)      # v15: bulaşık tablası (40 × 20 kiriş + tava), ayak yok
kot(ub, (BUL_Y[0] + BUL_Y[1]) / 2, (BUL_H[0] + BUL_H[1]) / 2 - 10, "ayaksız · tabla %s" % sayi(cm(KS.Y_TABLA)), ACC, "mm")
d.rectangle([ub(HAT_ON - 2.0), HH_(cm(KS.KAPAKLAR[0][3])), ub(HAT_ON), HH_(cm(KS.KAPAKLAR[0][2]))], fill=INK)            # K alt kapağı (tava 20)
kot(ub, HAT_ON + 1.5, cm(KS.KAPAKLAR[0][3]) - 4, "K alt kapağı", INK, "lm")
""")
degis('"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v14_alcak_hat · 27 Eyl 2026 · üretici _uretec/dukkan_plani14.py"',
      '"AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v15_on_duzlem · 28 Eyl 2026 · üretici _uretec/dukkan_plani15.py"')
degis('"v14 zaten var: "', '"v15 zaten var: "')
assert "KAN_DET" not in s and "KS.RAF_" not in s and "KANISTER" not in s
compile(s, "dukkan_plani15.py", "exec")
io.open(os.path.join(U, "dukkan_plani15.py"), "w", encoding="utf-8").write(s)
print("dukkan_plani15.py yazildi · %d satir" % s.count(NL))
