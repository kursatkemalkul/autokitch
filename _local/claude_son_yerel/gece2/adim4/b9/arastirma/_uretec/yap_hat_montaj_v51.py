# -*- coding: utf-8 -*-
"""hat_montaj_v50 → hat_montaj_v51 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal: "fırını taşı, hizalanma olsun, doğrusu öyle").
 1 · firin_tp10_cad_v5: gövde + konveyör + giriş bandı + ölü plaka +79 z (çıkıntı 1500 × 517 × 79, F modülü 909); K giriş çiti YOK; ürün −170.
 2 · itici_cad_v3: itme düz x boyunca 170 mm; destek plakası YOK.
 3 · topping_uno_cad_v9: ön fitil yine tam.
 4 · Denetimler: zarf (F fırın birimleri +79'a kadar), ön yüz (fırın çıkıntısı izinli), ürün yolu düz −170, robot ↔ çıkıntı payı.
 Çıktılar hat_v51 · durum.json pafta HAT v51."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v50.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v50 (26 Eyl 2026 gece): v49 + itici_cad_v2 (makara/kaldırma pimi −w) + topping_uno_cad_v8 (fitil boşluğu) + yavaş çubuk kalkışı',
      '"""v51 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal) — firin_tp10_cad_v5 (gövde + konveyör + giriş bandı + ölü plaka +79 z: çıkıntı 1500 × 517 × 79, F modülü 909; K giriş çiti YOK; ürün fırında −170) + itici_cad_v3 (düz itme 170, destek plakası YOK) + topping_uno_cad_v9 (fitil tam) + kesme_cad_v2 (ön kapaklar YOK) · ürün hattı mağazadan kesiciye −170, E −206' + NL +
      'v50 (26 Eyl 2026 gece): v49 + itici_cad_v2 (makara/kaldırma pimi −w) + topping_uno_cad_v8 (fitil boşluğu) + yavaş çubuk kalkışı')
degis('import itici_cad_v2 as IT', 'import itici_cad_v3 as IT')
degis('import firin_tp10_cad_v4 as FT', 'import firin_tp10_cad_v5 as FT')
degis('_sp = _ilu.spec_from_file_location("TU8", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v8.py"))   # v50: fitil boşluğu',
      '_sp = _ilu.spec_from_file_location("TU9", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v9.py"))   # v51: fitil tam')
degis('"topping_uno_cad_v8.py + topping_cad_v24.py", "hat/topping_v2.html")', '"topping_uno_cad_v9.py + topping_cad_v24.py", "hat/topping_v2.html")')
degis('(-420.0, -40.0), "sac", "topping_uno_cad_v8.py", "hat/topping_v2.html")', '(-420.0, -40.0), "sac", "topping_uno_cad_v9.py", "hat/topping_v2.html")')
degis('"sac", "itici_cad_v2.py", "hat/oven.html#itici")', '"sac", "itici_cad_v3.py", "hat/oven.html#itici")')
degis('"sac", "firin_tp10_cad_v4.py", "hat/oven.html")', '"sac", "firin_tp10_cad_v5.py", "hat/oven.html")')
# zarf denetimi: fırın birimleri çıkıntıya kadar
degis('and -DZ - 1 <= b["z"][0] and b["z"][1] <= 1)]', 'and -DZ - 1 <= b["z"][0] and b["z"][1] <= (FT.ZS + 1 if b["kod"] in FT.KAYAN else 1))]   # v51: fırın birimleri çıkıntıya (+79) kadar')
degis('print("ZARF DENETIMI: %s" % ("hepsi hattin icinde (%.0f x %.0f x %.0f)" % (HAT_W, H_MAK, DZ) if not tasan else "TASAN: " + ", ".join(tasan)))',
      'print("ZARF DENETIMI: %s" % ("hepsi hattin icinde (%.0f x %.0f x %.0f; v51: F firin birimleri z +%.0f cikintiya kadar)" % (HAT_W, H_MAK, DZ, FT.ZS) if not tasan else "TASAN: " + ", ".join(tasan)))')
# ürün yolu metinleri
degis('diskte kayma + yarik + on oda + firin + K citi → 4300): %s"', 'DUZ −170: disk + yarik + on oda + firin + K → 4300 · v51 kayma yok, cit yok): %s"')
degis('inik çubuk itme süpürmesi %d konum · ürün yolu çapraz (18 + bantlar)"', 'inik çubuk itme süpürmesi %d konum · ürün yolu düz −170 (18 + bantlar)"')
degis(' · gövde y %.0f–%.0f · K çiti %.0f → %.0f"', ' · gövde y %.0f–%.0f · v51: fırın +%.0f z (çıkıntı 0…+%.0f, F modülü %.0f derin) · K çiti YOK"')
degis('FT.RULO_X[0], FT.RULO_X[1], FT.YG0, FT.YG1, FT.CC_A[0], FT.CC_B[0]))', 'FT.RULO_X[0], FT.RULO_X[1], FT.YG0, FT.YG1, FT.ZS, FT.ZS, DZ + FT.ZS))')
# ön yüz denetimi: fırın çıkıntısı izinli
degis('        if zm > _IZIN.get(a_, 0.5):', '        if zm > (FT.ZS + 0.5 if a_.startswith(("F_TP10_", "F_GIRIS_BANDI", "F_CIKIS_PLAKA")) else _IZIN.get(a_, 0.5)):   # v51: fırın çıkıntısı +79')
degis('print("   izinli dis elemanlar (islevsel): K kapi mentesesi +22 · K acil stop +16 · E kapi kulpu +18 · acici kafasi +180 (acik konu)")',
      'print("   izinli dis elemanlar (islevsel): K kapi mentesesi +22 · K acil stop +16 · E kapi kulpu +18 · acici kafasi +180 (acik konu) · v51: FIRIN CIKINTISI +%.0f (x 2500-4000, y 956-1473, Kemal)" % FT.ZS)')
degis('print("ON YUZ DENETIMI (z <= 0,5 mm; acici kafasi haric): %s"', 'print("ON YUZ DENETIMI (z <= 0,5 mm; acici kafasi ve firin cikintisi haric): %s"')
degis('''    assert not _on, "makinenin on yuzunden tasan parca var"''',
      '''    assert not _on, "makinenin on yuzunden tasan parca var"
    # ---- v51 · ROBOT ↔ FIRIN ÇIKINTISI: robot birimleri (ray, kaide, kol zarfı) hattın önünde; çıkıntı 0…+79 (x 2500–4000, y 956–1473) ----
    _rz = [b for b in B if b["kod"] in ("ROBOT_1", "ROBOT_1_KOL", "ROBOT_RAY")]
    _rzmin = min(b["z"][0] for b in _rz)
    print("ROBOT ↔ FIRIN CIKINTISI: robot birimlerinin en on z'si %.0f · cikinti +%.0f → pay %.0f mm (%s; kol zarfi kutu, gercek kol modeli yok)" % (_rzmin, FT.ZS, _rzmin - FT.ZS, "SERBEST" if _rzmin >= FT.ZS + 50.0 else "DAR"))
    assert _rzmin >= FT.ZS + 50.0, "robot birimi firin cikintisina 50 mm'den yakin"
    _cik = FT.kut(FT.X_F0, FT.X_F1, FT.YG0, FT.YG1, 0.0, FT.ZS).val()
    _cik_cak = []
    for p in FT.PARCALAR:                                                                  # çıkıntı bandında yalnız fırın kabuğu/yalıtımı/bandı olmalı; başka modül parçası girmemeli (K, TOPPING x sınırları)
        pass
    for c_, sc in _DG:
        if c_.startswith("D:"): continue
        if _bbk(_cik, sc):
            v_ = _hacim(_cik, sc)
            if v_ > 1.0 or v_ < 0: _cik_cak.append((round(v_, 1), c_))
    print("FIRIN CIKINTISI ↔ KOMSU PARCALAR (TOPPING/K/hava, gercek kati kesisimi): %s" % ("TEMIZ" if not _cik_cak else "%d BULGU %s" % (len(_cik_cak), _cik_cak[:6])))
    assert not _cik_cak, "cikinti bandina komsu parca giriyor"''')
degis('import kesme_cad_v1 as KS', 'import kesme_cad_v2 as KS')
degis('"sac", "kesme_cad_v1.py", "hat/kesme.html")', '"sac", "kesme_cad_v2.py", "hat/kesme.html")')
degis('raise AssertionError("kesme_cad_v1 parcasi birimsiz kaldi: "', 'raise AssertionError("kesme_cad_v2 parcasi birimsiz kaldi: "')
degis(' · K = kesme_cad_v1 · 1 tam animasyon', ' · K = kesme_cad_v2 (on kapaklar YOK) · 1 tam animasyon')
degis('        if xc - R_ <= 2492.0: return P + 0.5', '        if xc - R_ <= 2507.0: return P + 0.5                                        # v51: rijit ürün arka kenarı DİSK KENARINI (2507) geçene kadar diskte (v50: 2492 = çerçeve; düz yolda disk sliverine giriyordu)')
degis('print("ANA MONTAJ ANIMASYONU (v50):', 'print("ANA MONTAJ ANIMASYONU (v51):')
s = s.replace('hat_v50.glb', 'hat_v51.glb').replace('hat_v50.usdz', 'hat_v51.usdz').replace('"hat_v50"', '"hat_v51"')
degis('pafta="HAT v50 (26 Eyl gece) · AKTARMA ITICISI itici_cad_v2 (SMC MY1B16-250 capraz 24,9°, pivotlu cubuk, sabit pimle kalkar, destek plakasi) · F = TP10 kesitli 1500 firin v4 (havalandirmali raf) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 + v2 v8 (katalog yay/pim, hac 7,0, fitil boslugu)',
      'pafta="HAT v51 (27 Eyl) · FIRIN 79 ONE: F = TP10 kesitli 1500 firin v5, govde + konveyor + giris bandi +79 z (cikinti 1500 × 517 × 79, F modulu 909) · urun hatti magazadan kesiciye −170, E −206 · K giris citi YOK · AKTARMA ITICISI itici_cad_v3 (SMC MY1B16-250 DUZ 170, pivotlu cubuk, sabit pimle kalkar; destek plakasi YOK) · havalandirmali raf · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 + v2 v9 (katalog yay/pim, hac 7,0, fitil TAM)')
io.open(os.path.join(U, "hat_montaj_v51.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v51.py yazildi")
