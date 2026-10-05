import sys, pickle, numpy as np, importlib
sys.path.insert(0, '.')
import supurme
from b5lib import seg_list, kesisim
out = []
for spn, lo, hi, pkl in (("k5", (4000, 790, -830), (4400, 1860, 60), "sup_K.pkl"), ("qr5", (4560, 0, 660), (5440, 2060, 1200), None), ("b5", (736, 0, -832), (4400, 788, 80), None), ("p5", (3480, 1840, -860), (4010, 2200, -60), None)):
    sp = importlib.import_module(spn)
    S = pickle.load(open(pkl, "rb")) if pkl else supurme.Supurme("../hat3_v8zm.glb", "c0", lo, hi)
    S.N = [n for n in S.N if not n["ad"].startswith(("E_", "F_DONER"))]
    hit = []
    for k in sp.KAN:
        h = S.kesis(k["lo"], k["hi"])
        if h: hit.append((k["ad"], h))
    for ci in sp.YOL:
        h = S.seg(seg_list(ci, sp.YOL))
        if h: hit.append(("#%d" % ci, h))
    for Q, r, *_ in (getattr(sp, "PYOL", {}).values() if hasattr(sp, "PYOL") else []):
        h = S.seg([(a, b, r) for a, b in zip(Q[:-1], Q[1:])])
        if h: hit.append(("pano", h))
    print(spn, "hareketli dugum", len(S.N), "-> supurme kesisimi:", hit if hit else "YOK", flush=True)
# pano kablo-kablo
import p5
L = {k: [(np.asarray(a, float), np.asarray(b, float), r) for a, b in zip(Q[:-1], Q[1:])] for k, (Q, r, t, y) in p5.PYOL.items()}
L["bina_ust"] = [(np.array([3940., 2146, -850]), np.array([3940., 2146, -344]), 10)]
L["zemin_guc"] = [(np.array([3942., 2118, -850]), np.array([3942., 2118, -344]), 7.5)]
L["zemin_veri"] = [(np.array([3966., 2118, -850]), np.array([3966., 2118, -344]), 4.3)]
L["bina_veri"] = [(np.array([3967., 2146, -850]), np.array([3967., 2146, -344]), 4.3)]
L["bina_ic"] = [(np.array(a, float), np.array(b, float), 10) for a, b in zip([(3940, 2146, -318.5), (3940, 2146, -300), (3612, 2146, -300), (3612, 2146, -245)], [(3940, 2146, -300), (3612, 2146, -300), (3612, 2146, -245), (3612, 2137, -245)])]
ks = list(L); n = 0
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        h = kesisim(L[ks[i]], L[ks[j]], pay=0.0)
        if h: n += 1; print("  KESISME", ks[i], ks[j], h[:2])
print("pano kablo-kablo kesisme:", n)
