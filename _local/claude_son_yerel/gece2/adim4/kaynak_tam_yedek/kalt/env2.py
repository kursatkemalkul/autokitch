import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import glbkit
G=glbkit.Glb(S+r"\hat3_v8zd.glb")
for nm in sys.argv[1].split(","):
  for p in [q for q in G.prims if q["name"]==nm]:
    tl,kut=G.komp(p)
    print("==",nm,p["pi"],len(kut))
    for i,(a,b,n) in sorted(kut.items(),key=lambda t:(t[1][0][1],t[1][0][2],t[1][0][0])):
        if a[1]<float(sys.argv[3]) and b[1]>float(sys.argv[2]) and a[0]>3990 and b[0]<4410:
            print("  %5d n%5d lo %s hi %s"%(i,n,a.round(1),b.round(1)))
