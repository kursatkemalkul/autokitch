# v8zq: A + B bölgesindeki bütün düğümlerin katı bileşenleri (dünya mm) → pickle
import sys, os, pickle, time, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0, S)
import govde_denetim_dogru as GD
t = time.time()
D = GD.glb_oku(os.path.join(S, "hat3_v8zq.glb"))
print("okundu", len(D), time.time() - t)
BOL = np.array([700.0, -50.0, -900.0]), np.array([4450.0, 2260.0, 120.0])
out = {}
for nd, P in D.items():
    if not len(P): continue
    lo = P.reshape(-1, 3).min(0); hi = P.reshape(-1, 3).max(0)
    if (hi < BOL[0]).any() or (lo > BOL[1]).any(): continue
    # yalnız bölgeye değen üçgenler
    m = ((P.max(1) >= BOL[0]) & (P.min(1) <= BOL[1])).all(1)
    out[nd] = P[m]
print("bölge düğüm", len(out), sum(len(v) for v in out.values()), "üçgen", time.time() - t)
pickle.dump(out, open(os.path.join(S, "gece2", "adim5", "_is", "bolge_tri.pkl"), "wb"))
