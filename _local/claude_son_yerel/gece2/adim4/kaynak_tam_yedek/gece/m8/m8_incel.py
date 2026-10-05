# -*- coding: utf-8 -*-
"""havada gorunen kumelerin parcalarina kenar ornegi (0,7 mm) ile temas incelemesi; m8_kenar.npy guncellenir"""
import numpy as np, shutil, os, time
import m8_ortak as O, m8_temas as T
if not os.path.exists("m8_kenar_ilk.npy"): shutil.copy("m8_kenar.npy", "m8_kenar_ilk.npy")
for tur in range(3):
    E = np.load("m8_kenar.npy"); O.E = E
    sc = [np.ones(O.N, bool), ~O.pkpk] + [O.pist == s for s in sorted(set(O.pist)) if s != "Çevre"]
    S = set()
    for g in sc:
        der, lab, topr = O.grafik(g)
        for k in np.unique(lab[g]):
            if not topr[k]: S |= set(np.where((lab == k) & g)[0].tolist())
    S = {i for i in S if O.PC[i]["n"] < 60000}
    done = set(np.load("m8_incelenen.npy").tolist()) if os.path.exists("m8_incelenen.npy") else set()
    S -= done
    print("tur", tur, len(S), "parca incelenecek", flush=True)
    if not S: break
    t = time.time()
    pts, pid = T.kenar_ornek(S, adim=0.7); print(len(pts), "ornek", flush=True)
    R = T.temas(pts, pid)
    pa = pid[R[:, 0]]; pb = T.TPc[R[:, 1]]
    E2 = np.stack([np.minimum(pa, pb), np.maximum(pa, pb)], 1)
    En = np.unique(np.vstack([E, E2]), axis=0)
    print("yeni kenar", len(En) - len(E), "%.0f s" % (time.time() - t), flush=True)
    np.save("m8_kenar.npy", En); np.save("m8_incelenen.npy", np.array(sorted(done | S)))
