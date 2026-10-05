# -*- coding: utf-8 -*-
"""hat_montaj_v60 → hat_montaj_v61 (27 Eyl 2026 gece) — Kemal: "yalıtım sağ solda neden daha derin, üstle aynı olsun" ·
"ön çekmeceleri gizle" → "tüm kapakları kaldır ya da ön kapakları şeffaf yap, çekmeceleri de" · "soluna çok basit 180'lik insan figürü koy":
  · TOPPING = topping_uno_cad_v13 (yan PU 60, ön/arka düzlemi üst yalıtımla aynı)
  · ÖN KAPAKLAR ŞEFFAF (yalnız görünüm; parçalar ve denetimler aynı): dolap çekmece önleri + fitilleri, K4 kapakları + ızgara, şerit önleri + klape,
    QR servis kapakları + müşteri panelleri + müşteri kapıları, tezgâh kapağı + çekmece önü, E üst ön kapak + şarjör yan kapısı
  · makinenin SOLUNDA 180 cm basit insan figürü (ölçek için; denetimlere girmez)
  · çıktılar hat_v61. Başka davranış DEĞİŞMEZ."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v60.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v60 (27 Eyl 2026 gece):',
      '"""v61 (27 Eyl 2026 gece): ÖN KAPAKLAR ŞEFFAF + 180 cm İNSAN FİGÜRÜ + TOPPING yan yalıtımı üstle aynı (topping_uno_cad_v13) · çıktılar hat_v61.' + NL +
      'v60 (27 Eyl 2026 gece):')
i = s.index('\nimport importlib, io')
assert s[i:].count("topping_uno_cad_v12") >= 3
s = s[:i] + s[i:].replace("topping_uno_cad_v12", "topping_uno_cad_v13")
# ---- ön kapaklar şeffaf: bütün modüller kurulduktan sonra (TZ.kur'dan hemen sonra) malzeme değişir
degis('''TZ.kur()
_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v1.py", "hat/service.html")''',
      '''TZ.kur()
_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v1.py", "hat/service.html")
# ---- v61 · ÖN KAPAKLAR ŞEFFAF (Kemal: "ön kapakları şeffaf yap, çekmeceleri de") — yalnız görünüm, parça ve denetim aynı
import re as _re61
MALZEME["on_seffaf"] = dict(renk=(0.70, 0.82, 0.95, 0.16), met=0.1, ruf=0.15, saydam=True)
ON_SEFFAF = _re61.compile(r"^(CEK_K\\d_[a-z0-9]+_\\d+_on_(dis_sac|pu|ic_sac|fitil)|k4_kapak_|k4_izgara_|serit_on_|klape_levhasi$|servis_kapagi_|"
                          r"musteri_(alt|ust)_panel$|goz_\\d\\d_musteri_kapisi$|on_kapak$|cekmece_onu$|on_ust_kapak$|sarjor_yan_kapisi$)")
_ON61 = {}
for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR)):
    for _p61 in _L61:
        if ON_SEFFAF.match(_p61["ad"]):
            _p61["mal"] = "on_seffaf"; _ON61[_ad61] = _ON61.get(_ad61, 0) + 1
print("v61 · ON KAPAKLAR SEFFAF (yalniz gorunum): " + " · ".join("%s %d parca" % kv for kv in sorted(_ON61.items())))
assert all(_ON61.get(k_, 0) > 0 for k_ in ("B", "QR", "TEZGAH", "E")), _ON61''')
# ---- 180 cm insan figürü (GLB'ye, denetim dışı)
degis('''    b1 = glb_yaz(os.path.join(OUT, "hat_v60.glb"),''',
      '''    # v61 · ÖLÇEK: makinenin SOLUNDA 180 cm basit insan figürü (Kemal) — denetimlere girmez, yalnız GLB
    MALZEME["insan_180"] = dict(renk=(0.20, 0.45, 0.80, 1.0), met=0.0, ruf=0.8, saydam=False)
    _hx, _hz = -550.0, -300.0
    _ins = cq.Workplane("XY").sphere(115.0).translate((_hx, 1685.0, _hz))                                   # baş · tepe 1800
    for _sx in (-95.0, 95.0):
        _ins = _ins.union(cq.Workplane("XZ").circle(70.0).extrude(-850.0).translate((_hx + _sx, 0.0, _hz)))            # bacaklar 0–850
        _ins = _ins.union(cq.Workplane("XZ").circle(45.0).extrude(-600.0).translate((_hx + 2.5 * _sx, 820.0, _hz)))    # kollar 820–1420
    _ins = _ins.union(cq.Workplane("XY").box(380.0, 620.0, 220.0).translate((_hx, 850.0 + 310.0, _hz)))            # gövde 850–1470
    _ins = _ins.union(cq.Workplane("XZ").circle(55.0).extrude(-110.0).translate((_hx, 1460.0, _hz)))               # boyun 1460–1570
    _ib = _ins.val().BoundingBox()
    assert abs(_ib.ymax - 1800.0) < 0.5 and abs(_ib.ymin) < 0.5, "insan figuru 180 cm degil: %.0f" % (_ib.ymax - _ib.ymin)
    _im = Mesh(); _im.ekle(TC_AG(_ins))
    parcalar.append(("INSAN_180cm__insan_180", _im, "insan_180"))
    print("v61 · INSAN FIGURU 180 cm: x %.0f…%.0f (makinenin solunda) · y %.0f–%.0f · z %.0f…%.0f" % (_ib.xmin, _ib.xmax, _ib.ymin, _ib.ymax, _ib.zmin, _ib.zmax))
    b1 = glb_yaz(os.path.join(OUT, "hat_v61.glb"),''')
degis('print("ALCAK HAT SOZLESMESI (v60 ·', 'print("ALCAK HAT SOZLESMESI (v61 ·')
degis('pafta="HAT v60 (27 Eyl gece) ·',
      'pafta="HAT v61 (27 Eyl gece) · ON KAPAKLAR SEFFAF (yalniz gorunum) + solda 180 cm insan figuru + TOPPING yan yalitimi ustle ayni (topping_uno_cad_v13: 60 kalin, on yuz -104) · v60:')
for a_ in ("hat_v60.usdz", '"hat_v60"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v60", "v61"))
s = s.replace("hat_v60.glb", "hat_v61.glb")
_kod = s[s.index('\nimport importlib, io'):]
for _eski in ("topping_uno_cad_v12", "hat_v60.glb", "hat_v60.usdz"):
    assert _eski not in _kod, "v61: eski kaldi: %s" % _eski
compile(s, "hat_montaj_v61.py", "exec")
io.open(os.path.join(U, "hat_montaj_v61.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v61.py yazildi · %d satir" % s.count(NL))
