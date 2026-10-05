# -*- coding: utf-8 -*-
"""HAT v2 · TOPPING DOZAJ HESABI ADAPTÖRÜ (montaj 'import topping_v2_hesap_v2 as TH2' yerine): v1 hesabının kendisi, yalnız v2 yerleşimi
(istasyon x'leri TC yerelinde = dünya − 700) · park 157,5 (A +507,5) · yayıcı boruları 90° çevrik (x'te yalnız Ø36 + 2 pay)."""
import os, sys, importlib.util as ilu
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import h2_hesap_v1 as HS

_sp = ilu.spec_from_file_location("TH2_h2", os.path.join(U, "topping_v2_hesap_v2.py"))
_m = ilu.module_from_spec(_sp); _sp.loader.exec_module(_m)
globals().update({k: v for k, v in vars(_m).items() if not k.startswith("__")})

# h2_topping_v1.ISTASYON ile aynı sayılar (burada CAD yüklenmesin diye yazılı; aşağıda assert ile bağlanır)
IST_DUNYA = {"SOS": 1396.0, "HARC": 1466.0, "KIYMA": 1596.0, "KUSBASI": 1806.0, "KASAR": 2062.0, "SUCUK": 2311.0}
for _i in _m.IST:
    _i["x"] = IST_DUNYA[_i["kod"]] - 700.0
X_PARK = _m.X_PARK + HS.DXL                                                           # −350 → 157,5 (açıcının altı)
_m.X_PARK = X_PARK
BORU_X = {i["kod"]: (i["x"] - 18.0 - 2.0, i["x"] + 18.0 + 2.0) for i in _m.IST if i["tip"] == "YAYICI"}   # dağıtıcı boru z boyunca → x'te Ø36 + 2
_m.BORU_X.clear(); _m.BORU_X.update(BORU_X)
IST = _m.IST
import topping_hesap_v7 as _H7
_m.X_AKTARMA = _H7.X_AKTARMA                                                          # montaj da TH2.X_AKTARMA = TC.H.X_AKTARMA yapar (1665,4)
X_AKTARMA = _m.X_AKTARMA
_ENGEL = _m.engel_denetimi()
assert all(r[-1] for r in _ENGEL), [r for r in _ENGEL if not r[-1]]                 # pidenin dökülen halkası yayıcı borularının altına girmez


def _bagla():
    """h2_topping_v1 yüklüyse sayılar birebir aynı olmalı"""
    T = sys.modules.get("h2_topping_v1")
    if T is not None:
        assert {k: float(v) for k, v in T.ISTASYON.items()} == IST_DUNYA, (T.ISTASYON, IST_DUNYA)


_bagla()
