import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import kesme_cad_v11 as K
import numpy as np
T = getattr(K, "E_BITIS_K", None)
print("E_BITIS_K", T)
for g in ("KESICI", "ITICI_ARABA", "ITICI_CAPRAZ", "ITICI_KOL", "ITICI_YUZ"):
    M = np.array([K.grup_trs(g, t) for t in np.linspace(0, (T or 60) + 5, 4000)])
    print(g, "min", M.min(axis=0).round(1), "max", M.max(axis=0).round(1))
sys.stdout.flush(); os._exit(0)
