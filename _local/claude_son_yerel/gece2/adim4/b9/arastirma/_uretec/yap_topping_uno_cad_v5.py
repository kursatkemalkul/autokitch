# -*- coding: utf-8 -*-
"""topping_uno_cad_v4 → v5: yayıcı yarığı HESAPTAN (topping_v2_hesap_v1, q ∝ r) + kaset milleri ayrı döner grup + çıktı v5."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v4.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v4 · 25 Eyl 2026\n',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v5 · 25 Eyl 2026\n'
      'v5 (Kemal: "toppingi de tam hesapla — sos geniş ağzın altına geliyor, ne kadar dökecek, tabla ne kadar dönecek"):\n'
      'YAYICI YARIĞI HESAPTAN (topping_v2_hesap_v1). Dönen tablada r yarıçapındaki halka turda 2πr·dr alan geçirir; düz yarıkla\n'
      'merkez kenardan 12,5 kat kalın kaplanırdı. Yarık artık KAMA: birim boydan çıkan debi r ile orantılı (q ∝ r, power-law n 0,3\n'
      '→ w ∝ r^0,19): sos 2,0 → 3,2 mm · harç 6,0 → 9,6 mm (r 10 → 121). Kaşar + sucuk kasetlerinin helezonu ve karıştırıcısı\n'
      '(+ milleri) AYRI DÖNER GRUP (HELEZON_<kaset> · KARISTIRICI_<kaset>) — simülasyon onları çevirir. Önceki: topping_uno_cad_v4.py\n'
      'v4:\n')
degis("import beldos_cad_v1 as BEL\n", "import beldos_cad_v1 as BEL\nimport topping_v2_hesap_v1 as TH2                  # v5: dozaj hesabı (yarık profili buradan)\n")
# ---- yarık: düz kesik yerine hesaptan kama profil ----
degis('        bor = silx(yb, ZT, 18.0, xb0, xb1).cut(silx(yb, ZT, 16.5, xb0 - 1, xb1 + 1)).cut(kut(xb0 + 4.0, xb1 - 4.0, yb - 20.0, yb - 14.0, ZT - g_ / 2.0, ZT + g_ / 2.0))\n'
      '        ekle("%s_spreader_dagitici_boru" % k, bor, "paslanmaz", "F+V",\n'
      '             not_="altı %.0f mm yarıklı · boy %.0f · alt yüzü %.0f (pideden %.0f)" % (g_, L_ + 8.0, yb - 18.0, yb - 18.0 - PIDE_UST))\n',
      '        # v5 · KAMA YARIK (topping_v2_hesap_v1.yarik_genisligi): q ∝ r → düzgün katman. Yarık değiştirilebilir alt lamda (pilotta ayar).\n'
      '        _r = [TH2.YARIK_R[0] + (TH2.YARIK_R[1] - TH2.YARIK_R[0]) * j / 14.0 for j in range(15)]\n'
      '        _ust = [(cx + r_, ZT + TH2.yarik_genisligi(ad, r_) / 2.0) for r_ in _r]\n'
      '        _alt = [(cx + r_, ZT - TH2.yarik_genisligi(ad, r_) / 2.0) for r_ in reversed(_r)]\n'
      '        _kama = cq.Workplane("XZ", origin=(0, yb - 20.0, 0)).polyline(_ust + _alt).close().extrude(-6.0)\n'
      '        bor = silx(yb, ZT, 18.0, xb0, xb1).cut(silx(yb, ZT, 16.5, xb0 - 1, xb1 + 1)).cut(_kama)\n'
      '        _w0, _w1 = TH2.yarik_genisligi(ad, TH2.YARIK_R[0]), TH2.yarik_genisligi(ad, TH2.YARIK_R[1])\n'
      '        ekle("%s_spreader_dagitici_boru" % k, bor, "paslanmaz", "H",\n'
      '             not_="altı KAMA yarıklı: r %.0f→%.0f mm\'de %.1f→%.1f mm (q ∝ r, topping_v2_hesap_v1) · boy %.0f · alt yüzü %.0f (pideden %.0f)"\n'
      '                  % (TH2.YARIK_R[0], TH2.YARIK_R[1], _w0, _w1, L_ + 8.0, yb - 18.0, yb - 18.0 - PIDE_UST))\n')
# ---- kasetler: dönen parçalar ayrı grup ----
degis('    xc = (x0 + x1) / 2.0\n    for p in [q for q in ps if q["ad"] != "tasima_tapasi"]:\n',
      '    xc = (x0 + x1) / 2.0\n'
      '    KOD = "KASAR" if mod.startswith("kasar") else "SUCUK"                 # v5: sim adları (topping_v2_hesap_v1.IST)\n'
      '    GRUP["HELEZON_" + KOD] = (xc, SOGUK_TABAN + Vm.CY, 0.0)               # alt mil: dozaj helezonu (z ekseninde döner)\n'
      '    GRUP["KARISTIRICI_" + KOD] = (xc, SOGUK_TABAN + Vm.YC, 0.0)           # üst mil: besleme rotoru\n'
      '    for p in [q for q in ps if q["ad"] != "tasima_tapasi"]:\n')
degis('        ekle("%s__%s" % (mod, p["ad"]), sh.translate(V(xc, SOGUK_TABAN, -200.0 - Vm.D / 2.0)), mal, "B",\n'
      '             not_="%s (montaj v41\'deki gibi, Codex parçaları dahil)" % ad)\n',
      '        gr = {"helezon": "HELEZON_" + KOD, "karistirici": "KARISTIRICI_" + KOD}.get(p.get("grup") or "", "SABIT")\n'
      '        ekle("%s__%s" % (mod, p["ad"]), sh.translate(V(xc, SOGUK_TABAN, -200.0 - Vm.D / 2.0)), mal, "B", grup=gr,\n'
      '             not_="%s (montaj v41\'deki gibi, Codex parçaları dahil)%s" % (ad, "" if gr == "SABIT" else " · döner: " + gr))\n')
degis('        ekle("mil_" + tag, silz(xc, yy, 11, -670, -525), "celik", "Ö")\n',
      '        ekle("mil_" + tag, silz(xc, yy, 11, -670, -525), "celik", "Ö", grup=("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD)\n')
# ---- denetim: yarık hesapla aynı ----
degis('kontrol("harç spreader\'ı kıyma istasyonuna değmiyor',
      'for ad in ("SOS", "HARC"):                                                # v5: model yarığı hesaptaki profil mi\n'
      '    _b = bb("%s_spreader_dagitici_boru" % ad.lower())\n'
      '    kontrol("%s kama yarık: merkez %.1f → kenar %.1f mm (hesap q ∝ r)" % (ad, TH2.yarik_genisligi(ad, TH2.YARIK_R[0]), TH2.yarik_genisligi(ad, TH2.YARIK_R[1])),\n'
      '            TH2.yarik_genisligi(ad, TH2.YARIK_R[1]) / TH2.yarik_genisligi(ad, TH2.YARIK_R[0]) > 1.4 and _b.xmax - _b.xmin >= 125.0)\n'
      'for _g in [g for g in GRUP if g.startswith(("HELEZON_", "KARISTIRICI_"))]:\n'
      '    kontrol("kaset döner grubu dolu: %s (%d parça)" % (_g, sum(1 for p in P if p["grup"] == _g)), sum(1 for p in P if p["grup"] == _g) >= 3)\n'
      'kontrol("harç spreader\'ı kıyma istasyonuna değmiyor')
# ---- GLB animasyonu: kaset milleri de dönsün (2 s'de 1 tur) ----
degis('    while off[0] % 4: blob.append(b"\\x00"); off[0] += 1\n    bb_ = b"".join(blob)\n',
      '    for g in [g for g in GRUP if g.startswith(("HELEZON_", "KARISTIRICI_"))]:     # v5: kaset milleri (görsel: 2 s\'de 1 tur)\n'
      '        kanal(g, "rotation", [(0.0, 0.0, math.sin(-math.pi * t / DONGU), math.cos(-math.pi * t / DONGU)) for t in TT], "VEC4")\n'
      '    while off[0] % 4: blob.append(b"\\x00"); off[0] += 1\n    bb_ = b"".join(blob)\n')
degis('"generator": "AUTOKITCH topping_uno_cad_v4"', '"generator": "AUTOKITCH topping_uno_cad_v5"')
degis('    glb_yaz(os.path.join(OUT, "topping_uno_v4.glb"))\n    with open(os.path.join(OUT, "topping_uno_v4.json"), "w", encoding="utf-8") as f:\n'
      '        json.dump(dict(surum="topping_uno_cad_v4 · %s" % time.strftime("%d.%m.%Y %H:%M"),\n',
      '    glb_yaz(os.path.join(OUT, "topping_uno_v5.glb"))\n    with open(os.path.join(OUT, "topping_uno_v5.json"), "w", encoding="utf-8") as f:\n'
      '        json.dump(dict(surum="topping_uno_cad_v5 · %s" % time.strftime("%d.%m.%Y %H:%M"),\n'
      '                       grup={g: list(v) for g, v in GRUP.items()},\n')
io.open(os.path.join(U, "topping_uno_cad_v5.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v5.py yazildi")
