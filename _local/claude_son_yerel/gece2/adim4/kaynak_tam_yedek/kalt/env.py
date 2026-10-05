import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import m8kit
G=m8kit.Glb(S+r"\hat3_v8zd.glb")
for p in G.prims:
    if p.get("gizli"): continue
    P=p["X"][p["T"]]; c=P.mean(1)
    m=(c[:,0]>3950)&(c[:,0]<4450)&(c[:,1]<960)&(c[:,1]>700)
    if m.sum(): 
        Q=P[m].reshape(-1,3); print("%-40s pi%d n%6d lo %s hi %s donuk %s"%(p["name"],p["pi"],m.sum(),Q.min(0).round(1),Q.max(0).round(1),p.get("donuk",False)))
