# -*- coding: utf-8 -*-
"""kaide_cad_v3 → v4 (29 Eyl 2026 gece · YEREL). YALNIZ C KAİDESİ değişir (A aynen):
  · 3. enine profil 2046 → 2120: 3. göz 1620–2100 (TOPPING v30 soğutma grubu cebi + sağında atış boşluğu) · 4. göz 2140–2460
  · 4 gözde ön profil + boyuna profil HAVA PENCERESİ (y 800–876): 1.–2. göz EMİŞ, 3.–4. göz ATIŞ (sanayi dolabı gibi önden, kanatların alt bandından)
  · üst plakada: 1.–2. göz arka yarısı EMİŞ açıklığı · 4. göz arka yarısı ATIŞ açıklığı · 3. gözde ünite cebi + atış açıklığı (tek kesik)
  · TOPPING denetimi TC v30 + TU v18 ile · ünite grubu kaideye gömülü (892'nin altına iner) — cep içinde, profillere değmez
Yalnız okur: kaide_cad_v3.py · yazar: kaide_cad_v4.py"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kaide_cad_v3.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


degis('"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v3 (29 Eyl 2026 · yap_kaide_cad_v3.py)',
      '"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v4 (29 Eyl 2026 gece · yap_kaide_cad_v4.py): C KAİDESİNDE SOĞUTMA GRUBU CEBİ + HAVA PENCERELERİ (TOPPING v30)\n'
      'v4: Kemal "soğutma grubunu alta (arka köşe), sağ köşedekileri kaldır": 3. enine 2046 → 2120 (3. göz 1620–2100: ünite cebi + atış boşluğu) · 4 gözde ön + boyuna\n'
      '    profil penceresi (y 800–876 · 1.–2. EMİŞ, 3.–4. ATIŞ) · üst plakada hava açıklıkları + ünite cebi · A kaidesi AYNI\n'
      'v3: AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v3 (29 Eyl 2026 · yap_kaide_cad_v3.py)')
degis("C_ENINE = (1154.0, 1600.0, 2046.0)        # C enine profil eksenleri (aralık ≈ 446)",
      "C_ENINE = (1154.0, 1600.0, 2120.0)        # v4: 3. enine 2046 → 2120 (3. göz 1620–2100 = ünite cebi + atış boşluğu · B bölmeleriyle hizalı DEĞİLDİ, yük boyuna profillerle) · v3 aralık ≈ 446\n"
      "# v4 · HAVA PENCERELERİ + AÇIKLIKLAR (TOPPING v30 soğutma grubu, sanayi dolabı gibi önden): dünya x · pencere y · açıklık z\n"
      "C_PENCERE_Y = (800.0, 866.0)                                   # profil 788–888 (et 2) → altında 10, üstünde 20 mm gövde + 2 mm et (üst şerit eğilmesi: 76 yüksekte σ 131 MPa → 66 yüksekte 40 MPa)\n"
      "C_PENCERE_X = {\"emis\": ((750.0, 1124.0), (1184.0, 1570.0)), \"atis\": ((1630.0, 2090.0), (2150.0, 2450.0))}   # 1.–2. göz EMİŞ · 3.–4. göz ATIŞ\n"
      "C_PLAKA_KESIK = [(745.0, 1129.0, -785.0, -480.0), (1179.0, 1575.0, -785.0, -480.0),        # 1.–2. göz arka yarısı: emiş (teknik bölmenin altı)\n"
      "                 (1628.0, 2095.0, -790.0, -477.0),                                         # 3. göz: ünite cebi (1628–2018) + sağında atış (2018–2095) · önü TC perdesinin arkası\n"
      "                 (2145.0, 2415.0, -785.0, -480.0)]                                         # 4. göz arka yarısı: atış (teknik bölmenin sağ perdesi 2420)")
degis('("KAIDE_C", "C mekanizma kaidesi 104 · x 700–2500 (v3: TOPPING yan sacları ve fırınla aynı hiza) · y 788–892 · z −830…+35 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur · v2 ön düzlem +79"),',
      '("KAIDE_C", "C mekanizma kaidesi 104 · x 700–2500 (v3: TOPPING yan sacları ve fırınla aynı hiza) · y 788–892 · z −830…+35 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur · v2 ön düzlem +79 · v4: SOĞUTMA GRUBU CEBİ (3. göz 1620–2100) + 4 gözde ön / boyuna profil hava pencereleri 66 yüksek (y 800–866) + plakada emiş / atış açıklıkları (TOPPING v30)"),')
# cerceve(): C kaidesinde pencere + plaka kesikleri (A için boş)
degis("def cerceve(b, on, x0, x1, enine, boyuna_z, kz=None):\n    kz = kz or KZ; bw = PR[\"b\"]; zf, zb = kz[1] - bw, kz[0] + bw                # v3: birim başına z (A / C)",
      "def cerceve(b, on, x0, x1, enine, boyuna_z, kz=None, pencere=(), plaka_kesik=()):\n    kz = kz or KZ; bw = PR[\"b\"]; zf, zb = kz[1] - bw, kz[0] + bw                # v3: birim başına z (A / C) · v4: pencere (x0, x1) · plaka_kesik (x0, x1, z0, z1)")
degis('    ekle(on + "_on_profil", profil_x(x0, x1, zf, kz[1]), "paslanmaz", b, bom=bom_())',
      '    _op = profil_x(x0, x1, zf, kz[1])\n'
      '    for _a, _b in pencere:                                                     # v4 · hava penceresi (iki et birden)\n'
      '        _op = _op.cut(kut(_a, _b, C_PENCERE_Y[0], C_PENCERE_Y[1], zf - 1.0, kz[1] + 1.0))\n'
      '    ekle(on + "_on_profil", _op, "paslanmaz", b, bom=bom_())')
degis('        ekle(on + "_boyuna_profil_%d" % (i // 2), profil_x(xs[i], xs[i + 1], boyuna_z[0], boyuna_z[1]), "paslanmaz", b)',
      '        _bp = profil_x(xs[i], xs[i + 1], boyuna_z[0], boyuna_z[1])\n'
      '        for _a, _b in pencere:                                                 # v4 · hava penceresi (bu segmentin içindekiler)\n'
      '            if _a >= xs[i] and _b <= xs[i + 1]:\n'
      '                _bp = _bp.cut(kut(_a, _b, C_PENCERE_Y[0], C_PENCERE_Y[1], boyuna_z[0] - 1.0, boyuna_z[1] + 1.0))\n'
      '        ekle(on + "_boyuna_profil_%d" % (i // 2), _bp, "paslanmaz", b)')
degis('    ekle(on + "_ust_plaka_4", kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, kz[0], kz[1]), "paslanmaz", b,\n'
      '         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f" % (x1 - x0, kz[1] - kz[0]), "üretim (lazer) · mekanizma tabanına M6 perçin somunlu", "ÜRETİM"))',
      '    _pl = kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, kz[0], kz[1])\n'
      '    for _a, _b, _z0, _z1 in plaka_kesik:                                       # v4 · hava açıklıkları + ünite cebi\n'
      '        _pl = _pl.cut(kut(_a, _b, Y_DUZ + PR["h"] - 1.0, Y_MEK + 1.0, _z0, _z1))\n'
      '    ekle(on + "_ust_plaka_4", _pl, "paslanmaz", b,\n'
      '         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f%s" % (x1 - x0, kz[1] - kz[0], (" · v4: %d lazer kesik (hava açıklıkları + soğutma grubu cebi)" % len(plaka_kesik)) if plaka_kesik else ""), "üretim (lazer) · mekanizma tabanına M6 perçin somunlu", "ÜRETİM"))')
degis('    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z, kz=KZ_C)',
      '    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z, kz=KZ_C, pencere=C_PENCERE_X["emis"] + C_PENCERE_X["atis"], plaka_kesik=C_PLAKA_KESIK)\n'
      '    ekle("kaide_C_tepsi_kosebendi", kut(1640.0, 2006.0, Y_DUZ + 2.0, 806.0, C_BOYUNA_Z[0] - 3.0, C_BOYUNA_Z[0]).union(kut(1640.0, 2006.0, 803.0, 806.0, C_BOYUNA_Z[0] - 33.0, C_BOYUNA_Z[0] - 3.0)), "paslanmaz", "KAIDE_C",\n'
      '         bom=("Soğutma grubu tepsisi ön köşebendi L 30 × 18 × 3 AISI 304", 1, "366 boy · 3. gözün boyuna profilinin arka yüzüne pencerenin ALTINDAN kaynak (790–800)", '
      '"v4 · TOPPING v30 soğutma grubu tepsisinin ön kenarı buna oturur (2 × M5) · arka kenarı TC askılarında", "ÜRETİM"))')
# TOPPING denetimi: TC v30 + TU v18 · ünite grubu cepte
degis('    for ad in ("topping_cad_v25", "topping_cad_v24"):', '    for ad in ("topping_cad_v30", "topping_cad_v29", "topping_cad_v25", "topping_cad_v24"):          # v4: v30 (soğutma grubu kaidede)')
degis('    raise RuntimeError("topping_cad_v24/v25 yok")', '    raise RuntimeError("topping_cad_v24/v25/v29/v30 yok")')
degis('    for ad in ("topping_uno_cad_v14", "topping_uno_cad_v13"):', '    for ad in ("topping_uno_cad_v18", "topping_uno_cad_v17", "topping_uno_cad_v14", "topping_uno_cad_v13"):   # v4: v18 (dikdörtgen soğuk kutu)')
degis('    raise RuntimeError("topping_uno_cad_v13/v14 yok")', '    raise RuntimeError("topping_uno_cad_v13/v14/v17/v18 yok")')
degis('    _mek = [(B.ymin, a) for a, _s, B in TCD if not a.startswith("onyuz_")]\n'
      '    kontrol("TC mekanizma parçaları (%d, onyuz_ ön yüz hariç) %.0f\'nin altına inmez (en alçak %s %.1f)" % (len(_mek), Y_MEK, min(_mek)[1], min(_mek)[0]), min(_mek)[0] >= Y_MEK - 0.01)',
      '    _mek = [(B.ymin, a) for a, _s, B in TCD if not a.startswith(("onyuz_", "sogutma_grubu"))]\n'
      '    kontrol("TC mekanizma parçaları (%d, onyuz_ ön yüz + soğutma grubu cebi hariç) %.0f\'nin altına inmez (en alçak %s %.1f)" % (len(_mek), Y_MEK, min(_mek)[1], min(_mek)[0]), min(_mek)[0] >= Y_MEK - 0.01)\n'
      '    _cg = [(a, B) for a, _s, B in TCD if a.startswith("sogutma_grubu")]                 # v4 · TOPPING v30 soğutma grubu kaide cebinde\n'
      '    if _cg:\n'
      '        _gx0, _gx1 = min(B.xmin for a, B in _cg if not a.endswith("cep_perdesi")), max(B.xmax for a, B in _cg)\n'
      '        _cgk = [(a, B) for a, B in _cg if a.startswith(("sogutma_grubu_KLF", "sogutma_grubu_tepsisi", "sogutma_grubu_pedi"))]   # kaideye gömülen gövde (askıların yatay kolları taban sacının üstünde)\n'
      '        _gy0 = min(B.ymin for a, B in _cg); _gz0, _gz1 = min(B.zmin for a, B in _cgk), max(B.zmax for a, B in _cgk)\n'
      '        _ck = [k_ for k_ in C_PLAKA_KESIK if k_[0] <= _gx0 and _gx1 <= k_[1]]\n'
      '        kontrol("v4 · soğutma grubu (%d parça) kaide CEBİNDE: x %.1f–%.1f ⊂ 3. göz %.0f–%.0f · plaka kesiği içinde (%s) · en alt y %.1f − dolap üstü %.0f = %.1f mm hava (≥ 15, B tavanına ısı köprüsü yok) · gömülü kısım z %.1f…%.1f ⊂ arka yarı %.0f…%.0f"\n'
      '                % (len(_cg), _gx0, _gx1, C_ENINE[1] + PR["b"] / 2.0, C_ENINE[2] - PR["b"] / 2.0, "evet" if _ck else "HAYIR", _gy0, Y_DUZ, _gy0 - Y_DUZ, _gz0, _gz1, KZ_C[0] + PR["b"], C_BOYUNA_Z[0]),\n'
      '                bool(_ck) and _gx0 >= C_ENINE[1] + PR["b"] / 2.0 and _gx1 <= C_ENINE[2] - PR["b"] / 2.0 and _gy0 - Y_DUZ >= 15.0 and _gz0 >= KZ_C[0] + PR["b"] and _gz1 <= C_BOYUNA_Z[0])')
# denetim: plaka paneli (Roark) — kesiksiz ön yarılar; pencere çevresi eğilme
degis('    a_ = (C_ENINE[1] - C_ENINE[0]) - PR["b"]; b_ = (C_BOYUNA_Z[0] - (KZ[0] + PR["b"]))\n    b_ = max(b_, (KZ[1] - PR["b"]) - C_BOYUNA_Z[1])',
      '    _xs4 = [C_X[0] + PR["b"]] + [v for xc in C_ENINE for v in (xc - PR["b"] / 2.0, xc + PR["b"] / 2.0)] + [C_X[1] - PR["b"]]\n'
      '    a_ = max(_xs4[i_ + 1] - _xs4[i_] for i_ in range(0, len(_xs4), 2))      # v4: en geniş göz (3. göz 480) · arka yarılar kesikli → ön yarı (kesiksiz) panel\n'
      '    b_ = (KZ[1] - PR["b"]) - C_BOYUNA_Z[1]')
degis('    kontrol("C üst plaka en büyük panel %.0f × %.0f · yayılı %.0f Pa → sehim %.2f mm ≤ 1 (Roark, E 193 GPa)" % (max(a_, b_), min(a_, b_), q_, w), w <= 1.0)',
      '    _ar = max(a_, b_) / min(a_, b_); _al = 0.0616 + (0.0770 - 0.0616) * min(1.0, max(0.0, (_ar - 1.2) / 0.2)) if _ar <= 1.4 else 0.0906   # Roark 4 kenar basit mesnet α (a/b 1,2 · 1,4 · 1,6)\n'
      '    w = _al * q_ * kb ** 4 / (193e9 * (PL / 1000.0) ** 3) * 1000.0\n'
      '    kontrol("C üst plaka en büyük KESİKSİZ panel (ön yarı) %.0f × %.0f · a/b %.2f · α %.4f · yayılı %.0f Pa → sehim %.2f mm ≤ 1 (Roark, E 193 GPa)" % (max(a_, b_), min(a_, b_), _ar, _al, q_, w), w <= 1.0)\n'
      '    # v4 · pencere üstündeki profil şeridi (kanal: üst et 40 × 2 + 2 × gövde 10 × 2) iki ucu ankastre kiriş gibi · yük: plakanın göz derinliği kadar şeridi\n'
      '    _Lp = max(b__ - a__ for a__, b__ in C_PENCERE_X["emis"] + C_PENCERE_X["atis"]) / 1000.0\n'
      '    _qp = q_ * ((KZ[1] - KZ[0]) / 2.0 / 1000.0)                                    # N/m · yarı derinlik şeridi (VARSAYIM: yükün yarısı bu profile)\n'
      '    _hs = PR["h"] - 2.0 - (C_PENCERE_Y[1] - Y_DUZ)                                 # pencere üstündeki gövde yüksekliği (10)\n'
      '    _A = 40.0 * 2.0 + 2.0 * 2.0 * _hs; _yc = (40.0 * 2.0 * (_hs + 1.0) + 2.0 * 2.0 * _hs * _hs / 2.0) / _A\n'
      '    _I = 40.0 * 2.0 ** 3 / 12.0 + 40.0 * 2.0 * (_hs + 1.0 - _yc) ** 2 + 2.0 * (2.0 * _hs ** 3 / 12.0 + 2.0 * _hs * (_hs / 2.0 - _yc) ** 2)\n'
      '    _S = _I / max(_yc, _hs + 2.0 - _yc); _M = _qp * _Lp ** 2 / 12.0 * 1000.0      # N·mm\n'
      '    kontrol("v4 · pencere üstü profil şeridi (kanal 40 × %.0f, I %.0f mm⁴) %.0f mm açıklık · %.0f N/m → M %.0f N·mm · σ %.0f MPa ≤ 205/2 (304 akma, emniyet 2 · plaka taşımasını saymadan)" % (_hs + 2.0, _I, _Lp * 1000.0, _qp, _M, _M / _S, ), _M / _S <= 102.5)\n'
      '    _kp = [(b__ - a__) * (z1__ - z0__) / 1e6 for a__, b__, z0__, z1__ in C_PLAKA_KESIK]\n'
      '    kontrol("v4 · plaka kesikleri %d (emiş %.3f + ünite cebi / atış %.3f + atış %.3f m²) · pencereler %d × %.0f yüksek (emiş %.0f · atış %.0f mm boy) — hepsi profil kenarından ≥ 5 mm içeride"\n'
      '            % (len(C_PLAKA_KESIK), _kp[0] + _kp[1], _kp[2], _kp[3], len(C_PENCERE_X["emis"]) + len(C_PENCERE_X["atis"]), C_PENCERE_Y[1] - C_PENCERE_Y[0],\n'
      '               sum(b__ - a__ for a__, b__ in C_PENCERE_X["emis"]), sum(b__ - a__ for a__, b__ in C_PENCERE_X["atis"])),\n'
      '            all(any(xs_ + 5.0 <= a__ and b__ <= xe_ - 5.0 for xs_, xe_ in zip(_xs4[::2], _xs4[1::2])) for a__, b__ in C_PENCERE_X["emis"] + C_PENCERE_X["atis"]))')
degis('    print("KAİDE v3 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))\n    print("DENETİM (kaide_cad_v3)")',
      '    print("KAİDE v4 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))\n    print("DENETİM (kaide_cad_v4)")')
degis('    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · kaide_cad_v2")', '    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · kaide_cad_v4")')
degis('BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v3")', 'BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v4")')
compile(s, "kaide_cad_v4.py", "exec")
io.open(os.path.join(U, "kaide_cad_v4.py"), "w", encoding="utf-8").write(s)
print("kaide_cad_v4.py yazıldı · %d satır" % s.count("\n"))
