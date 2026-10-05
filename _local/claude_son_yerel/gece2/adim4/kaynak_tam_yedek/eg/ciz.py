import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0,"."); import govde_denetim_dogru as GD
glb,out,mode=sys.argv[1],sys.argv[2],sys.argv[3]
D=GD.glb_oku(glb)
lo=np.array([4380,0,-840.]); hi=np.array([5250,2210,90.])
polys=[];cols=[];dep=[]
light=np.array([0.3,0.5,0.8]); light/=np.linalg.norm(light)
def view(P):
    if mode=="on": return P[...,[0,1]], P[...,2]
    if mode=="iso":
        a=np.radians(35); b=np.radians(25)
        x=P[...,0]*np.cos(a)+P[...,2]*np.sin(a); z=-P[...,0]*np.sin(a)+P[...,2]*np.cos(a)
        y=P[...,1]*np.cos(b)-z*np.sin(b); d=P[...,1]*np.sin(b)+z*np.cos(b)
        return np.stack([x,y],-1), d
for nd,P in D.items():
    if not len(P): continue
    if "kapaksiz" in out and ("on_seffaf" in nd): continue
    if not (nd.startswith(("E_","DUZ_E","U_KE","K_GOVDE","ELK_ANA","ELK_E"))): continue
    m=((P.max(1)>lo)&(P.min(1)<hi)).all(1); P=P[m]
    if not len(P): continue
    n=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-9)
    sh=0.35+0.65*np.abs(n@light)
    base=np.array([0.55,0.75,0.95]) if "on_seffaf" in nd else (np.array([0.85,0.55,0.2]) if "E_GOVDE__celik" in nd or "plastik" in nd else (np.array([0.75,0.77,0.8]) if nd.startswith("E_GOVDE") else np.array([0.5,0.5,0.5])))
    if nd.startswith(("K_GOVDE","U_KE")): base=np.array([0.88,0.88,0.9])
    q,d=view(P); polys+=list(q); dep+=list(d.mean(1)); cols+=list(np.clip(base*sh[:,None],0,1))
o=np.argsort(dep)
fig,ax=plt.subplots(figsize=(10,14))
ax.add_collection(PolyCollection([polys[i] for i in o],facecolors=[cols[i] for i in o],edgecolors=[tuple(cols[i]*0.6) for i in o],linewidths=0.15,alpha=1.0))
ax.autoscale(); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(out,dpi=110,bbox_inches="tight"); print(out)
