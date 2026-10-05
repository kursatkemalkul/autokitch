# v8o TOPPING etiketleri: eski (v8n bölütleme) + yeni (yeni_dizin aralıkları) -> pkl
import sys, os, json, pickle, numpy as np
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(H, "tg")); sys.path.insert(0, H)
from glbx import yukle
import topping_govde_yeni as TY
J0, D0 = yukle(os.path.join(H, "hat3_v8n.glb")); J1, D1 = yukle(os.path.join(H, "hat3_v8o.glb"))
R = TY.segment(J0, D0, ["TOPPING_MODUL", "ELK_TOPPING"])
DZ = json.load(open(os.path.join(H, "tg", "cikti", "yeni_dizin.json"), encoding="utf-8"))
L = {}
for nd in D1:
    if nd not in R: continue
    n1 = len(D1[nd]["T"]); a = np.array(["?yeni"] * n1, dtype=object); n0 = len(R[nd]); a[:n0] = R[nd]; L[nd] = a
say = {}
for nd, ad, bb, ntri in DZ["rapor"]["yeni"]:
    b = say.get(nd, len(D0[nd]["T"])); L[nd][b:b + ntri] = ad; say[nd] = b + ntri
pickle.dump(L, open(os.path.join(H, "ba", "etiket_v8o.pkl"), "wb"))
print("ok", {k: len(v) for k, v in L.items()})
