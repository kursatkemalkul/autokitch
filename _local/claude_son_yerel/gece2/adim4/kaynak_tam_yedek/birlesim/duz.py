# bir bilesenin duzlem gruplari: eksen-hizali duzlemler ve kapsadigi dikdortgen
from _env import *
import m8kit
G=m8kit.Glb(sys.argv[1]); ad=sys.argv[2]; ci=int(sys.argv[3])
p=[q for q in G.prims if q["name"]==ad and not q.get("gizli")][0]
tl,kut=G.komp(p); m=(tl==ci)&G.gorunur(p)
P=p["X"][p["T"][m]]
n=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); ar=np.linalg.norm(n,axis=1)/2; n/=np.maximum(ar[:,None]*2,1e-9)
gr={}
for i in range(len(P)):
    ax=int(np.argmax(np.abs(n[i]))); 
    if abs(n[i][ax])<0.999: key=("egik",)
    else: key=(ax,int(np.sign(n[i][ax])),round(P[i][0][ax],1))
    gr.setdefault(key,[]).append(i)
for k in sorted(gr,key=str):
    Q=P[gr[k]].reshape(-1,3)
    print(k,"n",len(gr[k]),"alan %.0f"%ar[gr[k]].sum(),"lo",Q.min(0).round(1),"hi",Q.max(0).round(1))
