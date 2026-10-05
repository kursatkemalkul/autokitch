# -*- coding: utf-8 -*-
"""h3_topping_sac_v2 hızlı deneme: kur + govde_parcalari + yeni parçaların temel denetimi (birbirine kesişim, PU açık, dimple)"""
import os, sys, time, pickle
W = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec"
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(W, "h3", "yama_v9", "sac_standart"))
sys.path.insert(0, os.path.join(W, "h3")); sys.path.insert(0, W)
sys.stdout.reconfigure(encoding="utf-8")
import h3_topping_sac_v2 as T
t0 = time.time()
T.kur()
L = T.govde_parcalari()
print("parça", len(L), "%.0f s" % (time.time() - t0))
for n in T.G.NOT: print("NOT", n[:250])
import numpy as np
ad = [p["ad"] for p in L]
for k in ("astar_", "pu_levha", "yapistirici", "derz_", "evaporator_ayag", "kanal_", "servis_arka", "astar_percin"):
    print(k, sum(1 for a in ad if a.startswith(k)))
out = {}
for p in L + T.dunya_listesi(T.G.ARAYUZ):
    sh = p["sh"]
    try:
        vs, fs = sh.tessellate(0.05, 0.3)
        out[p["ad"]] = (np.array([[v.x, v.y, v.z] for v in vs]), np.array(fs), p.get("tur"), p.get("mal"), sh.Volume())
    except Exception as e:
        print("TESS HATA", p["ad"], e)
pickle.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "v2_parca.pkl", "wb"))
print("bitti %.0f s" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
