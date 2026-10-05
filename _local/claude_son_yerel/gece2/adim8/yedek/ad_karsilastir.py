# -*- coding: utf-8 -*-
# python ad_karsilastir.py <eski|yeni> <cikti.json> : E, U, TOPPING arayüz adları + sac kesik sayıları
import os, sys, json
H3 = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3"
Y = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(H3, "yama_v9", "sac_standart"))
os.environ["ADIM5"] = os.path.join(H3, "yama_v9", "veri")
sys.path.insert(0, os.path.dirname(H3)); sys.path.insert(0, H3)
if sys.argv[1] == "eski": sys.path.insert(0, Y)
import h3_e_sac_v1 as E, h3_u_sac_v1 as U, h3_topping_sac_v1 as T
print(E.__file__, U.__file__, T.__file__)
q = lambda *a: None
out = {}
g = E.kur(log=q); out["E"] = dict(ad=[p["ad"] for p in g.ARAYUZ], kesik={s.ad: len(sum([pp.kesikler for pp in s.paneller], [])) for s in g.SAC} if hasattr(g.SAC[0], "paneller") else {})
r = U.kur(log=q)
gs = list(r.values()) if isinstance(r, dict) else (r if isinstance(r, (list, tuple)) else [r])
for gg in gs:
    if hasattr(gg, "ARAYUZ"): out["U_" + gg.birim] = dict(ad=[p["ad"] for p in gg.ARAYUZ])
G = T.kur(log=q); out["T"] = dict(ad=[p["ad"] for p in G.ARAYUZ])
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=0)
print({k: len(v["ad"]) for k, v in out.items()})
