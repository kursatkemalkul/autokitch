import numpy as np, json
Z=np.load("m8_onbellek.npz"); d=json.load(open("m8_parca.json"))
A,B,C=Z["A"],Z["B"],Z["C"]; P=Z["P"]
ad=np.array([p["ad"] for p in d["parca"]])
m=(ad[P]=="ELK_DOLAP__kablo")
T=np.stack([A[m],B[m],C[m]],1); pid=P[m]
E=[];EP=[]
for i,j in ((0,1),(1,2),(2,0)):
    e=T[:,j]-T[:,i]; L=np.linalg.norm(e,axis=1); u=np.abs(e)/np.maximum(L,1e-9)[:,None]
    nz=(L>2.5)&(u.max(1)<0.999)
    E.append(np.where(nz)[0]); 
idx=np.unique(np.concatenate(E))
print("egik kenarli ucgen",len(idx),"/",len(T))
import collections
c=collections.Counter(pid[idx])
for k,n in sorted(c.items()):
    p=d["parca"][k]; Q=T[idx][pid[idx]==k].reshape(-1,3)
    print(k,n,np.round(p["lo"],1).tolist(),np.round(p["hi"],1).tolist()," egik bolge",Q.min(0).round(1).tolist(),Q.max(0).round(1).tolist())
