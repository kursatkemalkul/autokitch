import sys, os, time, pickle, numpy as np
S = r"C:/Users/Kemal/AppData/Local/Temp/claude/C--Users-Kemal-Desktop-Kemal-WEBS-TE/f3ef876a-f062-4b29-bb81-775cc8a1a6d8/scratchpad"
sys.path.insert(0, S + "/gece"); sys.path.insert(0, S)
from m8kit import Glb
t = time.time(); g = Glb(S + "/hat3_v9h.glb"); print("yuk", time.time() - t)
D = ["TOPPING_MODUL__aluminyum", "TOPPING_MODUL__paslanmaz__PISTON_SOS", "TOPPING_MODUL__paslanmaz__PISTON_HARC", "TOPPING_MODUL__paslanmaz__PISTON_KUSBASI",
     "TOPPING_MODUL__bakir", "TOPPING_MODUL__silikon", "TOPPING_MODUL__kart", "ELK_QR_KABLO__kablo_sinyal", "B_KASA__pu"]
out = {}
for d in D:
    g.bilesen(d, 0)
    out[d] = [(b["no"], b["lo"].round(2).tolist(), b["hi"].round(2).tolist(), b["kapali"], int(sum(len(t) for _, t in b["parca"]))) for b in g._bc[d]]
    for r in out[d]:
        print(d, *r)
