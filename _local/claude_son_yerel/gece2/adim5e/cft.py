import sys, numpy as np
sys.path.insert(0, "is")
import govde_denetim_dogru as G
def B(glb, nodes):
    D = G.glb_oku(glb); return {n: G.bilesenler(n, D[n]) for n in nodes}
for glb in ("is/hat3_v8zq.glb", "is/hat3_v9b.glb"):
    X = B(glb, ["B_MODULER__paslanmaz", "B_KASA__celik"])
    M = X["B_MODULER__paslanmaz"]; C = X["B_KASA__celik"]
    print(glb, len(M))
    for b in M:
        if b.hi[1] < 130 and (b.hi[0]-b.lo[0]) > 2000: 
            print("  sase", b.no, np.round(b.lo,1), np.round(b.hi,1), b.kapali, b.mf() is not False and b.mf() is not None and round(b.mf().volume(),0))
            for c in C:
                r = G.cift(b, c)
                if r and r[0] != "TEMAS": print("     ", c.no, r[:3])
        if b.lo[1] > 700 and (b.hi[0]-b.lo[0]) > 600:
            print("  kiris", b.no, np.round(b.lo,1), np.round(b.hi,1), b.kapali, b.mf() is not False and b.mf() is not None and round(b.mf().volume(),0))
