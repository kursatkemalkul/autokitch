import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import m8kit
G=m8kit.Glb(S+r"\hat3_v8zd.glb")
lo=np.array([4004,700,-585.]);hi=np.array([4030,1900,-465.])
for p in G.prims:
    if p.get("gizli"): continue
    P=p["X"][p["T"]]; a=P.min(1); b=P.max(1)
    m=np.all(b>=lo,1)&np.all(a<=hi,1)
    m&=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1)>1e-9
    if m.sum():
        Q=P[m].reshape(-1,3); print("%-40s n%6d lo %s hi %s"%(p["name"],m.sum(),Q.min(0).round(1),Q.max(0).round(1)))
J=G.J
print([n["name"] for n in J["nodes"] if n.get("name","").startswith(("K","ELK_K"))][:80])
