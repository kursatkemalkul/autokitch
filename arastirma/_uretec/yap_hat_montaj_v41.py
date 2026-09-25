# -*- coding: utf-8 -*-
"""hat_montaj_v40 -> v41 : ISAAC / CODEX KASETLERİ 3B OLARAK + YALNIZ İKİ KASET

Kemal (25 Eyl 2026): "Isaac'te Codex sim yaptı, güzel de çalıştı; kaset tasarımlarını değiştirdi, rayı da tablayı da
değişmiş olabilir — ona bak, kendine adapte et; fazla olan kasetleri şimdilik sil" · "bir şey düzeltme, onları 3D olarak
al, kendine yerleştir, o kadar".
  · Kasetler: yalnız KAŞAR KABI ve KÜP SUCUK (Codex'in deney düzeneğindeki iki kaset). HARÇ 1-2, KIYMA, KUŞBAŞI
    şimdilik modelde yok; yuvaları ve etiketleri TOPPING'de duruyor.
  · Codex'in değiştirdiği parçalar STEP'ten OLDUĞU GİBİ alınır (düzeltme yok), kalan parçalar kasetin kendi üretecinden:
      kaşar  (kasar_cad_v14 + arastirma/3_TOPPING/kasar_v2/cad): helezon_B/C/D_v15 + cikis_tupu_v15
      sucuk  (sucuk_cad_v7  + arastirma/3_TOPPING/sucuk_v2/cad): helezon_D_v2 + cikis_tupu_v2
    Codex'in kendi notu: ikisi de ADAY, üretime serbest değil (kaşar 256 geçti / 9 kaldı, sucuk 61 / 5).
  · Ray ve tabla: Codex'in deney sahnesi TOPPING_IKIZ_v13'ten (22 Eyl; strok −680…+620, tepsi + pide 118–126);
    bizim topping_cad_v22 daha yeni (strok 1987, çalışma diski, pide 108–116) → ray/tabla DEĞİŞMEZ, bizimki kalır.
  · Parçalar aynı yerel koordinatta mı? Montaj her değişen parçada eski/yeni kutuyu karşılaştırır (eksen ve boy tutmalı).
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v40.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""v40 (25 Eyl 2026):', '''"""v41 (25 Eyl 2026): kasetler yalnız KAŞAR + KÜP SUCUK · Codex'in Isaac deneyindeki parçaları 3B (STEP) olarak yerinde · diğer 4 kaset şimdilik yok.
v40 (25 Eyl 2026):''')
degis("ÇIKTI: otonom/hat3d/hat_v40.glb + .usdz", "ÇIKTI: otonom/hat3d/hat_v41.glb + .usdz")

# ---- kasetler: yalnız ikisi ----
degis('''KASET_CAD = {"KAŞAR KABI": ("kasar_cad_v14", "Kaşar kabı v14", "kaset3d/index.html?k=kasar_v14"),
             "KIYMA": ("kiyma_cad_v9", "Kıyma kaseti v9", "kaset3d/index.html?k=kiyma_v9"),
             "KUŞBAŞI": ("kusbasi_cad_v8", "Kuşbaşı kaseti v8", "kaset3d/index.html?k=kusbasi_v8"),
             "KÜP SUCUK": ("sucuk_cad_v7", "Küp sucuk kaseti v7", "kaset3d/index.html?k=sucuk_v7"),
             "HARÇ": ("harc_cad_v4", "Harç / sos ünitesi v4 · pompalı", "kaset3d/index.html?k=harc_v4")}''',
      '''# v41 (Kemal 25 Eyl): YALNIZ Isaac/Codex deneyindeki iki kaset. KIYMA v9 · KUŞBAŞI v8 · HARÇ v4 şimdilik modelde YOK
#      (üreteçleri duruyor, geri almak = bu sözlüğe satırı geri eklemek).
KASET_CAD = {"KAŞAR KABI": ("kasar_cad_v14", "Kaşar kabı v14 + Codex v15 parçaları (helezon B·C·D, çıkış tüpü) · ADAY", "kaset3d/index.html?k=kasar_v14"),
             "KÜP SUCUK": ("sucuk_cad_v7", "Küp sucuk kaseti v7 + Codex V2 parçaları (helezon D, çıkış tüpü) · ADAY", "kaset3d/index.html?k=sucuk_v7")}''')
degis('''    cad = KASET_CAD.get(anahtar)
    birim("KASET_" + urun.replace(" ", "_"),''',
      '''    cad = KASET_CAD.get(anahtar)
    if not cad:
        continue                                                                         # v41: bu yuva şimdilik boş
    birim("KASET_" + urun.replace(" ", "_"),''')

# ---- Codex parçaları: STEP'ten olduğu gibi ----
degis('''def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5)."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    return V, [p for p in V.PARCALAR if alinir(p["ad"])]''',
      '''# v41 · Codex'in Isaac deneyinde değiştirdiği parçalar (STEP, kasetin yerel koordinatında) — DÜZELTİLMEDEN alınır
CODEX_3B = {"kasar_cad_v14": {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                              "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"},
            "sucuk_cad_v7": {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"}}
CODEX_RAPOR = []


def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5) · v41: Codex parçaları yerine konur."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    ps = [p for p in V.PARCALAR if alinir(p["ad"])]
    for ad, yol in CODEX_3B.get(modul, {}).items():
        hedef = [p for p in ps if p["ad"] == ad]
        assert len(hedef) == 1, "%s: %s parcasi bulunamadi" % (modul, ad)
        eski = hedef[0]["wp"].val().BoundingBox()
        yeni_sh = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))
        yeni = yeni_sh.val().BoundingBox()
        # aynı yerel koordinat mı: eksen boyu (z) ve ağırlık bölgesi tutmalı (kanat tur sayısı x/y kutusunu değiştirebilir)
        dz = max(abs(eski.zmin - yeni.zmin), abs(eski.zmax - yeni.zmax))
        assert dz < 3.0, "%s %s: Codex parcasi baska koordinatta (z farki %.1f)" % (modul, ad, dz)
        assert yeni.xmin < eski.xmax and eski.xmin < yeni.xmax and yeni.ymin < eski.ymax and eski.ymin < yeni.ymax, "%s %s: kutular kesismiyor" % (modul, ad)
        hedef[0]["wp"] = yeni_sh
        CODEX_RAPOR.append((modul, ad, yol, (eski.xmin, eski.xmax, eski.ymin, eski.ymax, eski.zmin, eski.zmax), (yeni.xmin, yeni.xmax, yeni.ymin, yeni.ymax, yeni.zmin, yeni.zmax)))
    return V, ps''')
degis('''    print("   kaset sirasi: " + " · ".join("%s %.0f–%.0f" % (b["kod"].replace("KASET_", ""), b["x"][0], b["x"][1]) for b in kas))''',
      '''    print("   kaset sirasi: " + " · ".join("%s %.0f–%.0f" % (b["kod"].replace("KASET_", ""), b["x"][0], b["x"][1]) for b in kas))
    assert sorted(b["kod"] for b in kas) == ["KASET_KAŞAR_KABI", "KASET_KÜP_SUCUK"], "v41: yalniz kasar + kup sucuk olmali"
    print("CODEX 3B (v41): %d parca STEP'ten oldugu gibi · eski -> yeni kutu (kasetin yerel mm):" % len(CODEX_RAPOR))
    for m_, a_, y_, e_, n_ in CODEX_RAPOR:
        print("   %-14s %-11s %-38s x %.0f..%.0f y %.0f..%.0f z %.1f..%.1f  ->  x %.0f..%.0f y %.0f..%.0f z %.1f..%.1f" % ((m_, a_, y_) + e_ + n_))
    assert len(CODEX_RAPOR) == 6, "Codex parcalari eksik yerlesti"''')

# ---- çıktılar ----
degis('''    b1 = glb_yaz(os.path.join(OUT, "hat_v40.glb"), parcalar, dokular, anim=False)''', '''    b1 = glb_yaz(os.path.join(OUT, "hat_v41.glb"), parcalar, dokular, anim=False)''')
degis('''print("hat_v40.glb · %d birim''', '''print("hat_v41.glb · %d birim''')
degis('''usdz_yaz([os.path.join(OUT, "hat_v40.usdz")], "hat_v40",''', '''usdz_yaz([os.path.join(OUT, "hat_v41.usdz")], "hat_v41",''')
degis('''print("hat_v40.usdz · %.0f KB''', '''print("hat_v41.usdz · %.0f KB''')
degis('''· v40 · E = kutu_cad_v3 · B = store_cad_v4 · alt taban 123 ·''', '''· v41 · kasetler kasar + kup sucuk (Codex 3B, aday) · E = kutu_cad_v3 · B = store_cad_v4 · alt taban 123 ·''')
io.open(os.path.join(U, "hat_montaj_v41.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v41.py yazildi")
