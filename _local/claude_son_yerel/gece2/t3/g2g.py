# -*- coding: utf-8 -*-
"""v2 gövde ↔ gövde OCC kesişim listesi (hızlı) — yalnız yeni / değişen parçaları içeren çiftler"""
import os, sys, time, re
W = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec"
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(W, "h3", "yama_v9", "sac_standart"))
sys.path.insert(0, os.path.join(W, "h3")); sys.path.insert(0, W)
sys.stdout.reconfigure(encoding="utf-8")
import h3_topping_sac_v2 as T
T.kur(log=lambda *a: None)
L = T.dunya_listesi(T.govde_parcalari()) + T.dunya_listesi([dict(p, tur="arayuz") for p in T.G.ARAYUZ])
YENI = re.compile(r'^(servis_arka|astar|evaporator_ay|kanal_|derz_|pu_levha|yapistirici|dis_(yan|tavan|taban|arka)|on_cerceve|kuru_bolme|arayuz_kb)')
bb = [p["sh"].BoundingBox() for p in L]
def ic(a, b): return a.xmin < b.xmax and b.xmin < a.xmax and a.ymin < b.ymax and b.ymin < a.ymax and a.zmin < b.zmax and b.zmin < a.zmax
out = []
for i in range(len(L)):
    for j in range(i + 1, len(L)):
        if not (YENI.match(L[i]["ad"]) or YENI.match(L[j]["ad"])): continue
        if not ic(bb[i], bb[j]): continue
        try: v = L[i]["sh"].intersect(L[j]["sh"]).Volume()
        except Exception: v = -1
        if v > 0.1 or v < 0: out.append((round(v, 3), L[i]["ad"], L[j]["ad"]))
out.sort(reverse=True)
print(len(out))
for o in out: print(o)
sys.stdout.flush(); os._exit(0)
