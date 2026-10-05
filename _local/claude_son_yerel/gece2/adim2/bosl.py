import sys,re,numpy as np
exec(open("g0.py").read())
sys.path.insert(0,S+r"\gece2\adim2\hava")
from m8kit import Glb, Yuzey
import htas
g=Glb(sys.argv[1])
YS=Yuzey(g,haric=("K_ELEKTRIK__hava","TOPPING_MODUL__hava_ana","HAVA_KOMPRESOR__hava_ana","ELK_ZINCIR__hava","HAVA_IC__kanal"))
for grp,ist,L in htas.GRUP:
    if grp not in sys.argv[2:]: continue
    for ad,lo,hi in L:
        lo=np.array(lo);hi=np.array(hi)
        for ax in range(3):
            for sg in (-1,1):
                d=np.zeros(3);d[ax]=sg;best=None
                u,w=[i for i in range(3) if i!=ax]
                for fu in np.linspace(0.05,0.95,7):
                    for fw in np.linspace(0.1,0.9,3):
                        o=np.zeros(3);o[ax]=hi[ax]+0.01 if sg>0 else lo[ax]-0.01;o[u]=lo[u]+fu*(hi[u]-lo[u]);o[w]=lo[w]+fw*(hi[w]-lo[w])
                        t=YS.isin(o,d,120)
                        if t is not None and (best is None or t<best[0]): best=(t,o.round(0).tolist())
                if best: print(grp,ad,"eksen",ax,"yon",sg,"mesafe %.1f"%best[0],best[1])
