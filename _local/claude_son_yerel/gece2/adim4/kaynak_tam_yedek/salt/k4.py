# -*- coding: utf-8 -*-
import sys, re, numpy as np
S=r"@@KOK_W@@"
for d in (r"\gece",r"",r"\elk4",r"\elk2"): sys.path.insert(0,S+d)
import m8kit, ek
G=m8kit.Glb(S+r"\hat3_v8zl.glb")
# yol koridoru kutulari: arka bosluk + bosalan yuva + on yatay
K=[((3600,2034,-321),(3952,2158,-288)),((3600,2034,-300),(3626,2158,-139)),((3600,2038,-162),(3757,2062,-138)),((3733,2038,-162),(3757,2072,-138))]
for p in G.prims:
    if p.get("gizli"): continue
    P=p["X"][p["T"]]; c=P.reshape(-1,3)
    if not (np.all(c.max(0)>=[3500,1800,-400]) and np.all(c.min(0)<=[4100,2300,0])): continue
    for tri,a,b in ek.komps(G,p):
        for i,(lo,hi) in enumerate(K):
            if np.all(b>=lo) and np.all(a<=hi):
                if p["name"]=="ELK_ANA_PANO_UF__cihaz" and a[0]>=3576.9 and b[0]<=3647.9: continue
                print(i,"%-44s n%5d lo %s hi %s"%(p["name"],len(tri),np.round(a,1).tolist(),np.round(b,1).tolist()))
