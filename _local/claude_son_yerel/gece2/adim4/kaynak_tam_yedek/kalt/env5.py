import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import m8kit
G=m8kit.Glb(S+r"\hat3_v8zd.glb")
q=np.array([float(v) for v in sys.argv[1].split(",")]); r=float(sys.argv[2])
for p in G.prims:
    if p.get("gizli"): continue
    P=p["X"][p["T"]]; a=P.min(1); b=P.max(1)
    m=np.all(b>=q-r,1)&np.all(a<=q+r,1)
    if m.sum():
        # distinct x planes
        xs=np.unique(np.round(P[m][:,:,0],1))
        print("%-30s n%5d xs %s"%(p["name"],m.sum(),xs[:20]))
