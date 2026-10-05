# -*- coding: utf-8 -*-
"""topping_cad_v26 → topping_cad_v27 (29 Eyl 2026) — BANTLI TABLA ANA MONTAJA (Kemal: "montaja adapte et").
Ayarlar bantli_tabla_hesap_v1 / bantli_tabla_cad_v1 (D4b a–f uygulanmış hali 0 çakışma) ile birebir:
  a · orta dikme tabla hizasında (dünya y 965–1012) kesilir → iki parça (alt / üst), kesik uçlarına 2 mm kaynaklı tapa
  c · çıkış yarığı: alt kenar 987 → 965, ön kenar −13 → −8 (YARIK_V2)
  d · ray sağ ucu 1785 → 1798 (topping_hesap_v7) · limit+ sensörü 1647 → 1675 · sağ tampon + plakası +28,4 · araba plakası sağ kenarı −20 (300 → 280)
  e · göbek + Ø340 tabla + çalışma diski + 3 disk pimi KALKAR · ayar bileziğine 2 × Ø8 konum pimi (delikleri bilezikte) · tahrik lokması pimleri 74 → 90,5 (dünya 982,5)
  f · SABİT TAHRİK (mıknatıslı, NEMA23 STP-MTR-23079) TOPPING sağ-arkasında, kayış kirişine braketli — bantli_tabla_cad_v1 bölüm 4 (dünya → yerel)
  + KASET (elle çıkar, 8,45 kg): bantli_tabla_cad_v1 bölüm 1–2 (taban, yatak, yan saclar, rulolar, gergi, rotor, mıknatıslar) + kaset bandı ve GT2 kayış GERÇEK KATI
    → parça adları "bk_" önekli, tabla ekseninde (park) yerel koordinatta; montaj bunları TABLA grubunda döndürür.
Başka hiçbir parça değişmez."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v26.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('import topping_hesap_v6 as H',
      'import topping_hesap_v7 as H                                                            # v27: aktarma 1665,4 · ray 1798 · limit+ 1688 (bantlı tabla)' + NL +
      'import bantli_tabla_montaj_v1 as BT                                                     # v27: kaset + sabit tahrik + konum pimleri (tek kaynak bantli_tabla_cad_v1)')
degis('MALZEME.setdefault("plastik", dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6))',
      'MALZEME.setdefault("plastik", dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6))' + NL +
      'MALZEME.setdefault("bant", dict(renk=(0.93, 0.94, 0.92, 1.0), met=0.0, ruf=0.8))         # v27: Forbo Transilon beyaz' + NL +
      'MALZEME.setdefault("miknatis", dict(renk=(0.55, 0.57, 0.62, 1.0), met=0.9, ruf=0.35))     # v27: NdFeB (kapak altında)' + NL +
      'MALZEME.setdefault("uhmw", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.45))')
degis('def ekle(ad, wp, mal, bom=None): PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, bom=bom))',
      'KALKAN_V27 = ("tabla_gobegi", "tabla", "calisma_diski", "disk_pimi_A", "disk_pimi_B", "disk_pimi_C")   # v27 (e): kaset bunların yerine ayar bileziğine oturur' + NL +
      'def ekle(ad, wp, mal, bom=None):' + NL +
      '    if ad in KALKAN_V27: return' + NL +
      '    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, bom=bom))')
# d · araba plakası sağ kenarı −20
degis('    apl = kut(Xc - 150.0, Xc + 150.0, 48.5, 58.5, -25.0, -315.0).cut(sily(Xc, ZT, 23.0, 47.0, 60.0))',
      '    apl = kut(Xc - 150.0, Xc + 130.0, 48.5, 58.5, -25.0, -315.0).cut(sily(Xc, ZT, 23.0, 47.0, 60.0))   # v27 (d): sağ kenar −20 (aktarma +28,4\'te fırın kabuğuna değmesin)')
degis('ekle("araba_plakasi", apl, "celik", bom=("Araba plakası 300 × 290 × 10"',
      'ekle("araba_plakasi", apl, "celik", bom=("Araba plakası 280 × 290 × 10"')
# e · ayar bileziğine konum pimleri (delik) + pimler · kaset
degis('    _ab = sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0))',
      '    _ab = sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0))' + NL +
      '    _PIM27 = [p for p in BT.PARCALAR if p["grup"] == "DONER" and p["ad"].startswith("ayar_konum_pimi_")]      # v27 (e)' + NL +
      '    for _p27 in _PIM27:' + NL +
      '        _ab = _ab.cut(cq.Workplane(obj=_p27["sh"].translate(cq.Vector(Xc, -DY_D, ZT))))                     # pres geçme deliği = pim')
degis('    ekle("tabla_gobegi", gb,',
      '    for _p27 in _PIM27:                                                                                   # v27 (e): 2 × Ø8 konum pimi, bileziğe presli' + NL +
      '        ekle(_p27["ad"], cq.Workplane(obj=_p27["sh"].translate(cq.Vector(Xc, -DY_D, ZT))), "celik", bom=_p27["bom"])' + NL +
      '    _yer = cq.Vector(Xc, -DY_D, ZT)                                                                         # v27: KASET (elle çıkar) park konumunda' + NL +
      '    for _k27 in BT.KASET:' + NL +
      '        ekle("bk_" + _k27["ad"], cq.Workplane(obj=_k27["sh"].translate(_yer)), _k27["mal"], bom=_k27["bom"])' + NL +
      '    for _t27 in BT.TAHRIK:                                                                                  # v27 (f): sabit tahrik (dünya → yerel)' + NL +
      '        ekle("st_" + _t27["ad"], cq.Workplane(obj=_t27["sh"].translate(cq.Vector(-DX_D, -DY_D, 0.0))), _t27["mal"], bom=_t27["bom"])' + NL +
      '    ekle("tabla_gobegi", gb,')
degis('        lk = lk.union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.0, 66.0, 74.0))',
      '        lk = lk.union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.0, 66.0, 74.0)).union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 3.95, 74.0, BT.H.Y_TABAN[1] - 1.5 - DY_D))   # v27 (e): pim kaset tabanı burcuna (dünya 982,5)')
# d · limit+ sensörü ve sağ tampon
degis('("limit_sag", 1647.0)):            # v24: limit+ 1647 (tampon 1650)',
      '("limit_sag", 1675.0)):            # v27 (d): limit+ 1647 → 1675 (aktarma +28,4) · v24: limit+ 1647 (tampon 1650)')
degis('"home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1647.0))',
      '"home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1675.0))')
degis('silx(_yc + 9.5, -372.5, 5.0, 1617.0, 1629.0)', 'silx(_yc + 9.5, -372.5, 5.0, 1645.4, 1657.4)')
degis('kut(1629.0, 1632.0, 45.0, 62.0, -377.0, -366.0), "celik",   # v25: braketin üst yüzüne oturur (v24: 1 mm)',
      'kut(1657.4, 1660.4, 45.0, 62.0, -377.0, -366.0), "celik",   # v27 (d): +28,4 (gergi braketi 1628–1672 önünde kalır) · v25: braketin üst yüzüne oturur')
# a · orta dikme iki parça
degis('           ("onyuz_cerceve_mek_orta_dikme", boru_y(xl(1584.25), xl(1614.25), Z_CER_C[0], Z_CER_C[1], MEK_Y[0] + 30.0, MEK_Y[1] - 30.0)),',
      '           ("onyuz_cerceve_mek_orta_dikme_alt", boru_y(xl(1584.25), xl(1614.25), Z_CER_C[0], Z_CER_C[1], MEK_Y[0] + 30.0, yl(965.0))'
      '.union(kut(xl(1584.25), xl(1614.25), yl(965.0) - 2.0, yl(965.0), Z_CER_C[0], Z_CER_C[1]))),   # v27 (a): tabla hizasında 47 mm boşluk · kesik ucu 2 mm tapa' + NL +
      '           ("onyuz_cerceve_mek_orta_dikme_ust", boru_y(xl(1584.25), xl(1614.25), Z_CER_C[0], Z_CER_C[1], yl(1012.0), MEK_Y[1] - 30.0)'
      '.union(kut(xl(1584.25), xl(1614.25), yl(1012.0), yl(1012.0) + 2.0, Z_CER_C[0], Z_CER_C[1]))),')
# c · çıkış yarığı
degis('YARIK_V2 = ((2492.0, 2498.5, 977.0, 1042.0, -417.0, -5.0), (2491.0, 2499.5, 987.0, 1038.0, -409.0, -13.0))    # firin_tp10_cad_v7.YARIK_V2 (montaj cikis_yarigi_contasi yerine)',
      'YARIK_V2 = ((2492.0, 2498.5, 955.0, 1042.0, -417.0, 0.0), (2491.0, 2499.5, 965.0, 1038.0, -409.0, -8.0))    # v27 (c): alt 987 → 965 (rotor kabı sucukta 970) · ön −13 → −8 · = firin_tp10_cad_v9.YARIK_V2')
# araba aktarmada (montaj v70 BANTLI TABLA DENETİMİ bulguları — v69'da araba aktarmada denetlenmiyordu)
degis('    ap = kut(Xc - 190.0, Xc + 190.0, 58.5, 60.5, -5.0, -340.0)',
      '    ap = kut(Xc - 190.0, Xc + 130.0, 58.5, 60.5, -5.0, -340.0)   # v27: sağ kenar plaka kenarında (Xc + 190 aktarmada fırın kabuğuna 1005 mm³ giriyordu)')
degis('("Sıyırıcı apron 380 × 335 × 2"', '("Sıyırıcı apron 320 × 335 × 2"')
degis('XK_SOL, XK_SAG = -560.0, 1650.0', 'XK_SOL, XK_SAG = -560.0, 1678.4   # v27: avara + gergi braketi +28,4 (aktarma +28,4 → kayış kolu brakete 130 mm³ giriyordu; tampon yine kolun 10 mm önünde)')
degis('v24: SAĞ uçta (1650)', 'v27: SAĞ uçta (1678,4)')
s = s.replace('"""', '"""topping_cad_v27 (29 Eyl 2026): BANTLI TABLA — kaset + sabit tahrik + ayarlar a, c, d, e, f (yap_topping_cad_v27.py).\n', 1)
compile(s, "topping_cad_v27.py", "exec")
io.open(os.path.join(U, "topping_cad_v27.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v27.py yazildi · %d satir" % s.count(NL))
