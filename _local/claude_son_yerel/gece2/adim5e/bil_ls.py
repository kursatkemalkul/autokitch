import sys, numpy as np, pickle, os
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad")
import govde_denetim_dogru as G
D = G.glb_oku(sys.argv[1])
pickle.dump(D, open("D_v9.pkl","wb"))
for nd in sys.argv[2:]:
    for k in D:
        if k != nd: continue
        B = G.bilesenler(k, D[k])
        print("==", k, len(B))
        for b in B:
            print("  [%d] %s..%s kap=%s n=%d" % (b.no, np.round(b.lo,1).tolist(), np.round(b.hi,1).tolist(), b.kapali, len(b.P)))
