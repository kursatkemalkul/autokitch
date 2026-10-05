# bos kablo deligi taramasi: sac/kanal ici dairesel delik duvarlari -> icinden gecen kablo/rakor/hortum/tapa var mi
import numpy as np, json, sys, re
from scipy.cluster.hierarchy import fcluster, linkage
Z=np.load("m8_onbellek.npz"); d=json.load(open("m8_parca.json"))
A,B,C=Z["A"],Z["B"],Z["C"]; P=Z["P"]
ad=np.array([p["ad"] for p in d["parca"]])
T=np.stack([A,B,C],1)
pat=re.compile(sys.argv[1] if len(sys.argv)>1 else r"^(ELK_TOPPING|TOPPING_MODUL__sac|TOPPING_MODUL__paslanmaz|ELK_QR|QR_|ELK_ANA_PANO|ELK_ANA_HAT__paslanmaz|ELK_ANA_HAT__kanal)")
gec=re.compile(r"kablo|rakor|hortum|tapa|hava|bakir|silikon")
sel=np.array([bool(pat.search(a)) and not gec.search(a) for a in ad])[P]
nn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); ar=np.linalg.norm(nn,axis=1); nn/=np.maximum(ar,1e-12)[:,None]
mn=T.min(1); mx=T.max(1); ext=mx-mn
TG=gec.pattern
gm=np.array([bool(gec.search(a)) for a in ad])[P]
GT=T[gm]; gmn=GT.min(1); gmx=GT.max(1); gad=ad[P[gm]]
out=[]
for ax in range(3):
    u,w=[i for i in range(3) if i!=ax]
    m=sel&(np.abs(nn[:,ax])<0.02)&(ext[:,ax]>0.4)&(ext[:,ax]<6.1)&(ext[:,u]<8)&(ext[:,w]<8)
    idx=np.where(m)[0]
    if len(idx)<8: continue
    cen=T[idx].mean(1)
    # gruplama: ayni duzlem araligi + yakinlik
    key=np.round(mn[idx,ax],1)*1000+np.round(mx[idx,ax],1)
    for kv in np.unique(key):
        ii=idx[key==kv]
        if len(ii)<8: continue
        cc=T[ii].mean(1)
        if len(ii)>20000: continue
        L=fcluster(linkage(cc[:,[u,w]],'single'),3.0,'distance') if len(ii)>1 else np.array([1])
        for l in np.unique(L):
            jj=ii[L==l]
            if len(jj)<8: continue
            V=T[jj].reshape(-1,3)[:,[u,w]]
            c0=(V.min(0)+V.max(0))/2; r=np.linalg.norm(V-c0,axis=1)
            if r.mean()<1.5 or r.mean()>30 or r.std()>0.25*r.mean() : continue
            # tam daire mi: acilar kapsami
            an=np.arctan2(V[:,1]-c0[1],V[:,0]-c0[0]); h=np.histogram(an,bins=12,range=(-np.pi,np.pi))[0]
            if (h>0).sum()<11: continue
            v0,v1=mn[jj,ax].min(),mx[jj,ax].max(); R=r.mean()
            # icinden gecen var mi
            lo=np.zeros(3);hi=np.zeros(3); lo[ax]=v0-0.1;hi[ax]=v1+0.1; lo[u]=c0[0]-R*0.7;hi[u]=c0[0]+R*0.7; lo[w]=c0[1]-R*0.7;hi[w]=c0[1]+R*0.7
            g=np.all(gmx>lo,1)&np.all(gmn<hi,1)
            pc=P[jj[0]]
            out.append((ad[pc],"xyz"[ax],(v0,v1),c0,R,len(jj),sorted(set(gad[g]))))
bos=[o for o in out if not o[6]]
print("delik",len(out),"bos",len(bos))
for o in bos: 
    c=np.zeros(3); a="xyz".index(o[1]); u,w=[i for i in range(3) if i!=a]; c[a]=(o[2][0]+o[2][1])/2; c[u]=o[3][0]; c[w]=o[3][1]
    print("BOS %-28s eksen %s duz %.2f..%.2f merkez %s r %.2f n%d"%(o[0],o[1],o[2][0],o[2][1],np.round(c,1).tolist(),o[4],o[5]))
