import sys,re,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S); sys.path.insert(0,S+r"\gece\m8\kablo_is"); sys.path.insert(0,S+r"\elk4"); sys.path.insert(0,S+r"\elk2"); sys.path.insert(0,S+r"irlesim")
import m8kit, serit, ek
G=m8kit.Glb(sys.argv[1]); pat=sys.argv[2]; L=np.array([float(v) for v in sys.argv[3:9]])
for pi,p in enumerate(G.prims):
    if p.get("gizli") or not re.search(pat,p["name"]): continue
    for tri,a,b in ek.komps(G,p):
        if np.any(b<L[0::2]) or np.any(a>L[1::2]): continue
        Sg=serit.segmentler(p["X"][p["T"][tri]])
        print(p["name"],pi,len(tri),np.round(a).astype(int).tolist(),np.round(b).astype(int).tolist())
        for q in Sg: print("    ",np.round(q['a'],1).tolist(),np.round(q['b'],1).tolist(),"r%.1f"%q['r'])
