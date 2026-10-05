# -*- coding: utf-8 -*-
"""HAT v3 (v2 adaptörünün kopyası) · TOPPING DOZAJ HESABI ADAPTÖRÜ (montaj 'import topping_v2_hesap_v2 as TH2' yerine): v1 hesabının kendisi, yalnız v2 yerleşimi
(istasyon x'leri TC yerelinde = dünya − 700) · park 157,5 (A +507,5) · yayıcı boruları 90° çevrik (x'te yalnız Ø36 + 2 pay)."""
import os, sys, importlib.util as ilu
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import h3_hesap_v1 as HS

_sp = ilu.spec_from_file_location("TH2_h3", os.path.join(U, "topping_v2_hesap_v2.py"))
_m = ilu.module_from_spec(_sp); _sp.loader.exec_module(_m)
globals().update({k: v for k, v in vars(_m).items() if not k.startswith("__")})

# h3_topping_v1.ISTASYON ile aynı sayılar (burada CAD yüklenmesin diye yazılı; aşağıda assert ile bağlanır)
IST_DUNYA = dict(HS.IST_V3)                    # v3 · sos 1645 · harç 2160 (yayıcılar alt kat dozajlayıcılarının arasında)
for _i in _m.IST:
    _i["x"] = IST_DUNYA[_i["kod"]] - 700.0
X_PARK = _m.X_PARK + HS.DXL                                                           # −350 → 386 (dünya 1086 · açıcının altı)
_m.X_PARK = X_PARK
BORU_X = {i["kod"]: (i["x"] - 18.0 - 2.0, i["x"] + 18.0 + 2.0) for i in _m.IST if i["tip"] == "YAYICI"}   # dağıtıcı boru z boyunca → x'te Ø36 + 2
_m.BORU_X.clear(); _m.BORU_X.update(BORU_X)
IST = _m.IST
import topping_hesap_v7 as _H7
_m.X_AKTARMA = _H7.X_AKTARMA                                                          # montaj da TH2.X_AKTARMA = TC.H.X_AKTARMA yapar (1665,4)
X_AKTARMA = _m.X_AKTARMA
# v3: yayıcı ağzı kaset iniş borularıyla aynı kotta (1047) → pide + malzeme koridorunun (1033) üstünde; dökülen halka her ağzın altından geçer ·
#     v2'nin engel denetimi (yayıcı borusu alçaktaydı, halka altına giremezdi) yerine KORİDOR denetimi
_ENGEL = [(k, HS.Y_AGIZ - 1.0, HS.Y_KORIDOR, HS.Y_AGIZ - 1.0 - HS.Y_KORIDOR >= 10.0) for k in BORU_X]
assert all(r[-1] for r in _ENGEL), _ENGEL


def _bagla():
    """h3_topping_v1 yüklüyse sayılar birebir aynı olmalı"""
    T = sys.modules.get("h3_topping_v1")
    if T is not None:
        assert {k: float(v) for k, v in T.ISTASYON.items()} == IST_DUNYA, (T.ISTASYON, IST_DUNYA)


_bagla()
