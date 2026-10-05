# m7b eklemeleri: v8x_a -> v8x_b her primde eklenen ucgen araliklari; v8zb'de ayni mi?
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gece"))
from glbkit import Glb
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
A = Glb(S + "/gece/m7/v8x_a.glb"); B = Glb(S + "/gece/m7/v8x_b.glb"); Z = Glb(S + "/hat3_v8zb.glb")
def key(G): return {(p["name"], p["pi"]): p for p in G.prims}
ka, kb, kz = key(A), key(B), key(Z)
out = {}
for k in ("TOPPING_MODUL__paslanmaz", "TOPPING_MODUL__pu", "TOPPING_MODUL__sac", "A_GOVDE__sac"):
    for kk in kb:
        if kk[0] != k: continue
        na, nb = len(ka[kk]["T"]), len(kb[kk]["T"])
        if nb == na: continue
        pb, pz = kb[kk], kz[kk]
        # ek parcalar: B extras mek son girisleri
        L = pb["pr"]["extras"]["mek"]; ent = [(L[i], L[i+1]//3, L[i+2]//3) for i in range(0, len(L), 3) if L[i+1]//3 >= na]
        print(kk, "a", na, "b", nb, "z", len(pz["T"]), "ek", len(ent))
        for lab, s, n in ent:
            Tb = pb["T"][s:s+n]; Tz = pz["T"][s:s+n]
            Pb = pb["X"][Tb]; Pz = pz["X"][Tz]
            dej = (Tz[:,0]==Tz[:,1])&(Tz[:,1]==Tz[:,2])
            esit = np.all(np.abs(Pb-Pz)<0.01,axis=(1,2))
            lo = Pb.reshape(-1,3).min(0); hi = Pb.reshape(-1,3).max(0)
            print("   [%d +%d] lo %s hi %s  dejenere %d esit %d" % (s, n, lo.round(1), hi.round(1), dej.sum(), esit.sum()))
        out[kk] = (na, nb)
import json; json.dump({"%s|%d" % k: v for k, v in out.items()}, open("m7b_aralik.json", "w"))
