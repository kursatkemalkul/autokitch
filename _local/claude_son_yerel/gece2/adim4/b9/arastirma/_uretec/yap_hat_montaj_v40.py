# -*- coding: utf-8 -*-
"""hat_montaj_v39 -> v40 : ALT TABAN ÇİZGİSİ 123 + ANA MONTAJ ANİMASYONSUZ

Kemal (25 Eyl 2026): "üstte bant istasyonları hizalı, alt taraf da öyle olmalı; en alt çekmecenin altındaki gereksiz alanı
kaldır, sağdaki istasyonların alt tabanını ona hizala" → "yap. Bir de ana montajda animasyona gerek yok, içine girince oynasın yeter."
  · B = store_cad_v4 (gövde 123'ten, yalıtımlı taban en alt çekmecenin 3 mm altında) · E = kutu_cad_v3 (gövde 123'ten,
    asansör tahriki tabanın altında) · F ve K taban dolapları 123–1060, altlarında ayak + süpürgelik (60 geride).
  · Denetim: B, E, F/K taban dolaplarının alt çizgisi aynı (Y_ALT); üst taraf eskisi gibi (1060 · 1168 · 2030).
  · hat_v40.glb ANİMASYONSUZ: hareketli düğümler döngünün başındaki duruşta (t = 0). Animasyon yalnız istasyon
    modellerinde: modul_B.glb (çekmeceler) ve modul_E.glb (kutu modülü) — sayfaları açınca oynar.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v39.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""v39 (25 Eyl 2026):', '''"""v40 (25 Eyl 2026): ALT TABAN ÇİZGİSİ 123 (B store_cad_v4 · E kutu_cad_v3 · F/K taban dolapları) + ana montaj animasyonsuz (animasyon istasyon modellerinde).
v39 (25 Eyl 2026):''')
degis("ÇIKTI: otonom/hat3d/hat_v39.glb + .usdz", "ÇIKTI: otonom/hat3d/hat_v40.glb + .usdz")

# ---- B = store_cad_v4 ----
degis("import store_cad_v3 as SC                                  # v39: 3 elemanlı ray",
      '''import store_cad_v4 as SC                                  # v40: alt taban 123 (v39: 3 elemanlı ray)
Y_ALT = SC.Y_PLINT                                         # v40 · ALT TABAN ÇİZGİSİ: bütün istasyon gövdeleri yerden buradan başlar (123)''')
degis('''birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v3.py", "")''',
      '''birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v4.py", "")''')
degis('''print("B CEKMECE MODULU (store_cad_v3 · 3 elemanli ray): %d birim''', '''print("B CEKMECE MODULU (store_cad_v4 · alt taban %.0f · 3 elemanli ray): %d birim''')
degis('''% (len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))''', '''% (Y_ALT, len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))''')

# ---- F ve K taban dolapları: 123–1060 + ayak/süpürgelik ----
degis('''birim("D_TABAN_KABIN", "F taban dolabı 0–1060 (pano · UPS · bulaşık makinesi)", "D", "KUTU", (X_D, X_D + W_D), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")''',
      '''birim("D_TABAN_KABIN", "F taban dolabı 123–1060 (pano · UPS · bulaşık makinesi)", "D", "KUTU", (X_D, X_D + W_D), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v40 alt taban çizgisi 123")
birim("D_SUPURGELIK_KABIN", "F taban dolabı · ayak + süpürgelik 0–123 (60 geride)", "D", "KUTU", (X_D + 30.0, X_D + W_D - 30.0), (0.0, Y_ALT), (-DZ + 30.0, -60.0), "kabin", "v40 alt taban çizgisi 123")''')
degis('''birim("K_TABAN_KABIN", "K taban dolabı 0–1060 · yedek kutu KALDIRILDI (Kemal 24 Eyl)", "K", "KUTU", (X_K, X_K + W_K), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")''',
      '''birim("K_TABAN_KABIN", "K taban dolabı 123–1060 · yedek kutu KALDIRILDI (Kemal 24 Eyl)", "K", "KUTU", (X_K, X_K + W_K), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v40 alt taban çizgisi 123")
birim("K_SUPURGELIK_KABIN", "K taban dolabı · ayak + süpürgelik 0–123 (60 geride)", "K", "KUTU", (X_K + 30.0, X_K + W_K - 30.0), (0.0, Y_ALT), (-DZ + 30.0, -60.0), "kabin", "v40 alt taban çizgisi 123")''')

# ---- E = kutu_cad_v3 ----
degis("import kutu_cad_v2 as KC", "import kutu_cad_v3 as KC                                  # v40: alt taban 123, asansör tahriki tabanın altında")
degis('''raise AssertionError("kutu_cad_v2 parcasi birimsiz kaldi: " + _p["ad"])''', '''raise AssertionError("kutu_cad_v3 parcasi birimsiz kaldi: " + _p["ad"])''')
degis('''birim(_k, _a, "E", "GERCEK_KUTU", _x, _y, _z, "sac", "kutu_cad_v2.py", "hat/pack.html")''',
      '''birim(_k, _a, "E", "GERCEK_KUTU", _x, _y, _z, "sac", "kutu_cad_v3.py", "hat/pack.html")''')
degis('''    print("E KUTU MODULU (kutu_cad_v2): %d birim''', '''    print("E KUTU MODULU (kutu_cad_v3): %d birim''')

# ---- denetim: alt taban çizgisi ----
degis('''    assert abs(_bk["E_GOVDE"]["y"][0]) < 0.01 and abs(_bk["E_GOVDE"]["y"][1] - H_MAK) < 0.01, "E kesilmemeli (tek parca 0-2030)"''',
      '''    assert abs(_bk["E_GOVDE"]["y"][0]) < 0.01 and abs(_bk["E_GOVDE"]["y"][1] - H_MAK) < 0.01, "E kesilmemeli (tek parca 0-2030)"
    # v40 · ALT TABAN ÇİZGİSİ: B ve E üreteçleri kendi ölçümünü assert ediyor (gövde altı); burada ikisinin ve dolapların AYNI çizgide olduğu
    assert abs(SC.Y_PLINT - Y_ALT) < 0.01 and abs(KC.Y_PLINT - Y_ALT) < 0.01, "B ve E alt taban cizgisi farkli: %.1f / %.1f" % (SC.Y_PLINT, KC.Y_PLINT)
    for k_ in ("D_TABAN_KABIN", "K_TABAN_KABIN"):
        assert abs(_bk[k_]["y"][0] - Y_ALT) < 0.01, "%s alti %.1f" % (k_, _bk[k_]["y"][0])
    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    _ge = min(p["wp"].val().BoundingBox().ymin for p in KC.PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "asansor_")))
    assert abs(_gb - Y_ALT) < 0.05 and abs(_ge - Y_ALT) < 0.05, "govde altlari: B %.1f · E %.1f" % (_gb, _ge)
    print("ALT TABAN CIZGISI (v40): B %.1f · E %.1f · F dolabi %.0f · K dolabi %.0f -> ayni cizgi %.0f · altlari ayak + supurgelik · ust taraf 1060 / 1168 / 2030 aynen -> GECTI"
          % (_gb, _ge, _bk["D_TABAN_KABIN"]["y"][0], _bk["K_TABAN_KABIN"]["y"][0], Y_ALT))''')

# ---- ana montaj GLB'si animasyonsuz ----
degis('''def glb_yaz(yol, parcalar, dokular, ozel=None):''', '''def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True):''')
degis('''            if ad_ not in ad2node:
                continue
            n_el = 4 if yol_ == "rotation" else 3''',
      '''            if ad_ not in ad2node:
                continue
            if not anim:                                                                  # v40 (Kemal): ana montajda animasyon yok — düğüm döngünün başındaki duruşta
                nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]
                continue
            n_el = 4 if yol_ == "rotation" else 3''')
degis('''    b1 = glb_yaz(os.path.join(OUT, "hat_v39.glb"), parcalar, dokular)''',
      '''    b1 = glb_yaz(os.path.join(OUT, "hat_v40.glb"), parcalar, dokular, anim=False)   # v40: animasyonsuz (istasyon modellerinde oynar)
    print("ANA MONTAJ (v40): animasyonsuz · %d hareketli dugum t = 0 durusunda · animasyon modul_B (cekmeceler) + modul_E (kutu modulu) icinde" % len({a[0] for a in ANIM}))''')
degis('''print("hat_v39.glb · %d birim''', '''print("hat_v40.glb · %d birim''')
degis('''usdz_yaz([os.path.join(OUT, "hat_v39.usdz")], "hat_v39",''', '''usdz_yaz([os.path.join(OUT, "hat_v40.usdz")], "hat_v40",''')
degis('''print("hat_v39.usdz · %.0f KB''', '''print("hat_v40.usdz · %.0f KB''')
degis('''· v39 · E = kutu_cad_v2 · B = store_cad_v3 (3 elemanli ray) ·''', '''· v40 · E = kutu_cad_v3 · B = store_cad_v4 · alt taban 123 ·''')
io.open(os.path.join(U, "hat_montaj_v40.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v40.py yazildi")
