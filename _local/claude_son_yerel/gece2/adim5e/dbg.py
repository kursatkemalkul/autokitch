import os, sys, re, numpy as np
sys.path.insert(0, os.environ["YAMA_URETEC"] + "/h3/yama_v9")
import sac_ent as SE
from m8kit import Glb
import h3_e_sac_v1 as E
g_ = E.kur(log=lambda *a: None)
AR = SE.dunya_arayuz(g_)
g = Glb("hat3_v9b.glb"); K = SE.Karsi(g, haric_onek=("E_GOVDE__", "E_MODULER__"))
for p in AR:
    if p["ad"] not in ("arayuz_mek_sol_7", "arayuz_mek_arka_21", "arayuz_mek_taban_38"): continue
    print(p["ad"], p["arayuz"]["karsi"], p.get("meta"))
    m, P = SE.kesici(p)
    for d, b, v in K.tara(p, m, P): print("   ", d, b["no"], np.round(b["lo"], 1).tolist(), np.round(b["hi"], 1).tolist(), round(v, 1))
sys.stdout.flush(); os._exit(0)
