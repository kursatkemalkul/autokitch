import sys, os
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_topping_sac_v1 as T, h3_sac_v1 as S
T.kur(log=print); L = T.govde_parcalari()
import numpy as np
B = np.array([[p["sh"].BoundingBox().xmin, p["sh"].BoundingBox().xmax, p["sh"].BoundingBox().ymin, p["sh"].BoundingBox().ymax, p["sh"].BoundingBox().zmin, p["sh"].BoundingBox().zmax] for p in L])
print("zarf", B[:,0].min(), B[:,1].max(), B[:,2].min(), B[:,3].max(), B[:,4].min(), B[:,5].max(), "hedef", T.ZARF)
v=[p for p in L if p["ad"].endswith("_vida") and p["ad"].startswith("servis_arka")]
print(len(v), v[0]["bom"])
# gövde içi kesişim: vida ↔ saclar
sac=[p for p in L if p["tur"]=="sac"]
n=0
for e in v:
    for s in sac:
        x=e["sh"].intersect(s["sh"]).Volume()
        if x>1e-3: n+=1; print("kesişim", e["ad"], s["ad"], round(x,3))
print("vida↔sac kesişim", n)
sys.stdout.flush(); os._exit(0)
