# python eg/rnd.py glb out.png lo hi az el [haric_regex] [dahil_regex]
import sys, re, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0,"."); import govde_denetim_dogru as GD
glb,out=sys.argv[1],sys.argv[2]
lo=np.array([float(v) for v in sys.argv[3].split(",")]); hi=np.array([float(v) for v in sys.argv[4].split(",")])
az,el=np.radians(float(sys.argv[5])),np.radians(float(sys.argv[6]))
hr=re.compile(sys.argv[7]) if len(sys.argv)>7 and sys.argv[7] else None
dr=re.compile(sys.argv[8]) if len(sys.argv)>8 and sys.argv[8] else None
D=GD.glb_oku(glb)
# camera: direction from target to eye: (sin az, ., cos az) in xz ; y up
e=np.array([np.sin(az)*np.cos(el), np.sin(el), np.cos(az)*np.cos(el)])
r=np.cross([0,1,0],e); r/=np.linalg.norm(r); u=np.cross(e,r)
light=e*0.7+u*0.5+r*0.2; light/=np.linalg.norm(light)
polys=[];cols=[];dep=[]
pal={"on_seffaf":(0.6,0.78,0.95),"kabuk":(0.78,0.8,0.83),"sac":(0.72,0.74,0.78),"celik":(0.85,0.55,0.2),"plastik":(0.3,0.6,0.3),"sensor":(0.2,0.4,0.9),"motor":(0.35,0.35,0.4),"kablo":(0.9,0.2,0.2),"kanal":(0.9,0.8,0.1),"aluminyum":(0.65,0.65,0.7),"uhmw":(0.95,0.95,0.95),"paslanmaz":(0.55,0.6,0.65)}
for nd,P in D.items():
    if not len(P): continue
    if hr and hr.search(nd): continue
    if dr and not dr.search(nd): continue
    c=P.mean(1); m=((c>lo)&(c<hi)).all(1); P=P[m]
    if not len(P): continue
    n=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-9)
    sh=0.35+0.65*np.abs(n@light)
    base=np.array((0.5,0.5,0.5))
    for k,v in pal.items():
        if k in nd.lower(): base=np.array(v)
    if not nd.startswith("E_"): base=base*0.6+0.4
    q=np.stack([P@r,P@u],-1); d=P@e
    polys+=list(q); dep+=list(d.mean(1)); cols+=list(np.clip(base*sh[:,None],0,1))
o=np.argsort(dep)
fig,ax=plt.subplots(figsize=(12,12))
ax.add_collection(PolyCollection([polys[i] for i in o],facecolors=[cols[i] for i in o],edgecolors=[tuple(cols[i]*0.5) for i in o],linewidths=0.2))
ax.autoscale(); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(out,dpi=90,bbox_inches="tight"); print(out, len(polys))
import os; sys.stdout.flush(); os._exit(0)
