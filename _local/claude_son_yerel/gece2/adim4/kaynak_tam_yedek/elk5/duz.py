import json,numpy as np,sys,re
D=np.load("c0/m8_onbellek.npz"); PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
ad=np.array([p["ad"] for p in PJ["parca"]]); nm=ad[D["P"]]
A,B,C=D["A"],D["B"],D["C"]; lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
pat=sys.argv[1]; L=np.array([float(v) for v in sys.argv[2:8]]); amin=float(sys.argv[8]) if len(sys.argv)>8 else 200
m=np.array([bool(re.search(pat,a)) for a in ad])[D["P"]] & np.all(hi>=L[0::2],1)&np.all(lo<=L[1::2],1)
idx=np.where(m)[0]
n=np.cross(B[idx]-A[idx],C[idx]-A[idx]); ar=np.linalg.norm(n,axis=1)/2
g={}
for i,t in enumerate(idx):
    k=np.argmax(np.abs(n[i]))
    if abs(n[i][k])<0.999*np.linalg.norm(n[i]): continue
    key=(k,round(float(A[t][k]),1))
    a=g.setdefault(key,[0,lo[t].copy(),hi[t].copy()]); a[0]+=ar[i]; a[1]=np.minimum(a[1],lo[t]); a[2]=np.maximum(a[2],hi[t])
for (k,v),(a,l,h) in sorted(g.items()):
    if a>=amin: print("xyz"[k],v,"alan %.0f"%a,np.round(l,1).tolist(),np.round(h,1).tolist())
