import sys,numpy as np
S=r"@@KOK_W@@"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S)
import glbkit
G=glbkit.Glb(S+r"\hat3_v8zd.glb")
for nm,ids in (("K_GOVDE__celik",[11,1015]),("K_GOVDE__sac",[6,982,21])):
  p=G.bul(nm); tl,kut=G.komp(p)
  for i in ids:
    m=(tl==i)&G.gorunur(p); V=p["X"][np.unique(p["T"][m])]
    c=(V.min(0)+V.max(0))/2
    for x0 in np.unique(np.round(V[:,0],1)):
        w=V[np.abs(V[:,0]-x0)<0.05]; rr=np.hypot(w[:,1]-c[1],w[:,2]-c[2])
        print(nm,i,"x",x0,"r",rr.min().round(2),rr.max().round(2), "c",c.round(1))
