# -*- coding: utf-8 -*-
"""HAT v2 · TC ADAPTÖRÜ (montaj 'import ... as TC' yerine) — topping_cad_v32 arayüzü, parçalar h3_topping_v1'den (iki katlı TOPPING).
Yerel çerçeve v1 ile AYNI (dünya = yerel + (700, 892)): montajdaki X_BC = 700 dokunulmadan kalır; TOPPING'in dünya x'i 1207,5 … 2500."""
import os, sys
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_topping_v1 as T
from topping_cad_v32 import *            # noqa: F401,F403 — sabitler / fonksiyonlar (YUVA, KAS, URUN, KASET_CAD, ET_*, RAKOR_ACICI, x_hareketli, …)
import topping_cad_v32 as _TC0

H = _TC0.H                               # topping_hesap_v7 (X_AKTARMA 1665,4 — aktarma v1 ile aynı dünya x'inde)
XC_TABLA = _TC0.XC_TABLA + T.DXL         # tablanın çizildiği yer = PARK (açıcının altı) · yerel 157,5 → dünya 857,5
Y = T.H_UST - T.DYW                      # 1308 · modül yüksekliği (v1 970) → makine üstü 2200
W = T.XT[1] - T.XT[0]                    # 1292,5 (bilgi · montaj W kullanmaz)
X_SERT = (_TC0.X_SERT[0] + T.DXL, _TC0.X_SERT[1])
ISTASYON_DUNYA = dict(T.ISTASYON)
PARCALAR = []


def modul():
    """v2 parça listesi (yerel çerçeve) — montaj TC.PARCALAR[:] = []; TC.modul() ile çağırır (önbellekli, tekrar kurulmaz)"""
    TCp, _TUp = T.kur()
    PARCALAR[:] = [dict(ad=p["ad"], wp=cq.Workplane(obj=p["sh"].translate(cq.Vector(-T.DXW, -T.DYW, 0.0))), mal=p["mal"], bom=p.get("bom")) for p in TCp + T.eski_tc()]
    return PARCALAR


modul()
_ES = {p["ad"] for p in T.eski_tc()}
assert all(v1_kalir(p["ad"]) for p in PARCALAR if p["ad"] not in _ES), [p["ad"] for p in PARCALAR if p["ad"] not in _ES and not v1_kalir(p["ad"])][:5]   # noqa: F405
_AD = [p["ad"] for p in PARCALAR if not p["ad"].startswith("_bom")]                  # v1'de de iki '_bom_kovan' var (BOM yer tutucusu, çizilmez)
assert len(set(_AD)) == len(_AD)
