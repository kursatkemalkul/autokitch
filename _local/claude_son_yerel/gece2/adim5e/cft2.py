import sys, numpy as np
sys.path.insert(0, "is")
import govde_denetim_dogru as G
q = np.array([2120.0, 905.0, -700.0])
for glb in ("is/hat3_v9d.glb", "is/hat3_v9e.glb"):
    D = G.glb_oku(glb); B = G.bilesenler("TOPPING_MODUL__celik", D["TOPPING_MODUL__celik"])
    L = [b for b in B if np.all(b.lo - 1 <= q) and np.all(q <= b.hi + 1)]
    print(glb, [(b.no, np.round(b.lo,1).tolist(), np.round(b.hi,1).tolist(), b.kapali) for b in L])
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            print("   ", L[i].no, L[j].no, G.cift(L[i], L[j])[:3] if G.cift(L[i], L[j]) else None)
