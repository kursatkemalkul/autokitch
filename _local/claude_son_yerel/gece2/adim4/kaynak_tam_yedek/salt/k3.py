# -*- coding: utf-8 -*-
import sys, re, numpy as np
S=r"@@KOK_W@@"
for d in (r"\gece",r"",r"\elk4",r"\elk2"): sys.path.insert(0,S+d)
import m8kit, ek
G=m8kit.Glb(S+r"\hat3_v8zl.glb")
lo=np.array([3700,2030,-330.]); hi=np.array([3990,2180,-60.])
from collections import defaultdict
for p in G.prims:
    if p.get("gizli") or not p["name"].startswith("ELK_ANA_PANO"): continue
    P=p["X"][p["T"]]; c=P.reshape(-1,3)
    if not (np.all(c.max(0)>=lo) and np.all(c.min(0)<=hi)): continue
    for tri,a,b in ek.komps(G,p):
        if np.all(b>=lo) and np.all(a<=hi) and np.max(b-a)<450:
            print("%-48s n%5d lo %s hi %s"%(p["name"],len(tri),np.round(a,1).tolist(),np.round(b,1).tolist()))
