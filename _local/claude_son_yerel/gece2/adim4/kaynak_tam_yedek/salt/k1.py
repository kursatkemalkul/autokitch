# -*- coding: utf-8 -*-
import sys, re, numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S); sys.path.insert(0,S+r"\elk4"); sys.path.insert(0,S+r"\elk2")
import m8kit, ek
G=m8kit.Glb(S+r"\hat3_v8zl.glb")
lo=np.array([3540,1860,-330.]); hi=np.array([3990,2180,-60.])
for p in G.prims:
    if p.get("gizli"): continue
    P=p["X"][p["T"]]; c=P.reshape(-1,3)
    if not (np.all(c.max(0)>=lo) and np.all(c.min(0)<=hi)): continue
    for tri,a,b in ek.komps(G,p):
        if np.all(b>=lo) and np.all(a<=hi):
            if p["name"].startswith("ELK_ANA_PANO_UF") and not (a[0]<3660 and b[0]>3570 and a[1]>2040): 
                if not ('kablo' in p['name']): continue
            print("%-48s n%5d lo %s hi %s et %s"%(p["name"],len(tri),np.round(a,1).tolist(),np.round(b,1).tolist(),G._etiketler(p,int(tri[0]))))
