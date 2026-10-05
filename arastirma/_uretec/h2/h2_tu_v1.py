# -*- coding: utf-8 -*-
"""HAT v2 · TU ADAPTÖRÜ (montajdaki spec_from_file_location('TU11', topping_uno_cad_v19.py) yerine) — soğuk paket + UNO'lar + kasetler (iki katlı).
Çerçeve v1 ile AYNI 'TU dünyası' (dünya = TU + (700, −168)): montaj bütün parçaları ve grup pivotlarını bir kez −168 kaydırır, x'e X_BC (700) ekler."""
import io, json, os, sys
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_topping_v1 as T

_T0 = T.TU0
M = _T0.M                                # + v2 malzemeleri (hortum_gida, gn, kasar_urun, sucuk_urun)
Z_ON = _T0.Z_ON
YAL_Y0 = _T0.YAL_Y0                      # soğuk oda altı 1277 (dünya 1109) — v2'de de aynı
boru = _T0.boru
kut, silx, sily, silz = _T0.kut, _T0.silx, _T0.sily, _T0.silz
DX_DUNYA, DY_DUNYA = _T0.DX_DUNYA, _T0.DY_DUNYA
GRUP = T.grup_pivotlari()
P = []


def _kur():
    _TCp, TUp = T.kur()
    P[:] = [dict(ad=q["ad"], sh=q["sh"].translate(cq.Vector(-DX_DUNYA, -DY_DUNYA, 0.0)), mal=q["mal"], kaynak=q["kaynak"], grup=q["grup"], not_=q.get("not_", ""))
            for q in TUp]
    GRUP.clear(); GRUP.update(T.grup_pivotlari())


_kur()


def den_assert():
    """v2 · TOPPING denetimleri: (1) grup pivotları parçalarıyla aynı ötelendi · (2) ad tekil · (3) statik çakışma raporu (h2_topping_denetim_v1) YENİ = 0 ·
    (4) X süpürmesi raporu (h2_topping_supurme_v1) bulgu = 0 — raporlar üreteçten YENİ olmalı · döner: geçen denetim sayısı"""
    n = 0
    adlar = [q["ad"] for q in P]; assert len(adlar) == len(set(adlar)); n += 1
    for q in P:
        assert q["grup"] in GRUP, (q["ad"], q["grup"])
    n += 1
    kay = T.GRUP_KAYMA
    for g, d in kay.items():
        v0 = _T0.GRUP[g]; v1 = GRUP[g]
        assert all(abs(v1[i] - v0[i] - d[i]) < 1e-9 for i in range(3)), g
    n += 1
    t_uret = os.path.getmtime(T.__file__)
    for ad, anahtar in (("_denetim_topping_v1.json", "yeni"), ("_supurme_topping_v1.json", "bulgu")):
        yol = os.path.join(H2, ad)
        assert os.path.exists(yol), "v2 TOPPING denetim raporu yok: %s (önce h2_topping_denetim_v1 / h2_topping_supurme_v1 çalıştır)" % ad
        assert os.path.getmtime(yol) >= t_uret, "v2 TOPPING denetim raporu üreteçten ESKİ: %s" % ad
        d = json.load(io.open(yol, encoding="utf-8"))
        assert not d[anahtar], "v2 TOPPING %s: %d bulgu" % (ad, len(d[anahtar]))
        n += 1
    hy = T.hava_yolu()                                                                     # v1 hava yolu kuralı (≤ 3,5 m/s · ≥ 250 mm) v2 ölçüsüyle
    assert hy["gecti"], "v2 TOPPING yoğuşma ünitesi hava yolu: %s" % hy
    n += 1
    return n
