import sys, os, json, numpy as np, pickle
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
g=G(os.path.join(HERE,'hat3_v9l_A.glb'))
MEK=g.MEK
OUT=[]
# all components with any triangle in region around A (x 700-1480, y 600-2260, z -860..100), excluding A nodes
AN=('A_GOVDE__sac','A_GOVDE__paslanmaz','A_GOVDE__conta','A_GOVDE__plastik','KAIDE_A__paslanmaz','KAIDE_A__sac','A_ONYUZ__on_seffaf')
lo0=np.array([700,600,-860.]); hi0=np.array([1480,2260,100.])
for ni,nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    if nd['name'] in AN: continue
    M=g.W[ni]; sc=abs(np.linalg.det(M[:3,:3]))**(1/3)
    if sc<0.01: continue
    for pi,(X,T,mek,mat,ex) in enumerate(g.tris(ni)):
        P=X[T]; c=P.mean(1)
        m=np.all(P.max(1)>=lo0,1)&np.all(P.min(1)<=hi0,1)
        if not m.any(): continue
        ar=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1); m&=ar>1e-9
        Tm=T[m]; mk=mek[m]
        cl=bilesen(X,Tm)
        for k in np.unique(cl):
            Tc=Tm[cl==k]; u,inv=np.unique(Tc.reshape(-1),return_inverse=True); V=X[u]
            OUT.append(dict(dug=nd['name'],pi=pi,mek=int(np.bincount(mk[cl==k]+1).argmax()-1),V=V,F=inv.reshape(-1,3),lo=V.min(0),hi=V.max(0)))
print(len(OUT))
import collections
c=collections.Counter((o['dug'],o['mek']) for o in OUT)
for k,n in sorted(c.items()): 
    L=[o for o in OUT if (o['dug'],o['mek'])==k]; lo=np.min([o['lo'] for o in L],0); hi=np.max([o['hi'] for o in L],0)
    print(n,k,MEK[k[1]]['kod'] if k[1]>=0 else '-',np.round(lo),np.round(hi), sum(len(o['F']) for o in L))
pickle.dump(OUT,open('cevre_bil.pkl','wb'))
