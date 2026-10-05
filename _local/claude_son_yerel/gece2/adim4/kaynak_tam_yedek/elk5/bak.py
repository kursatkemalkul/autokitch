import json,numpy as np,sys,re
D=np.load("c0/m8_onbellek.npz"); PJ=json.load(open("c0/m8_parca.json",encoding="utf-8"))
ad=np.array([p["ad"] for p in PJ["parca"]]); nm=ad[D["P"]]
A,B,C=D["A"],D["B"],D["C"]; lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
pat=sys.argv[1]; L=np.array([float(v) for v in sys.argv[2:8]])
m=np.array([bool(re.search(pat,a)) for a in ad])[D["P"]] & np.all(hi>=L[0::2],1)&np.all(lo<=L[1::2],1)
V=np.concatenate([A[m],B[m],C[m]])
for k in range(3): print("xyz"[k],sorted(set(np.round(V[:,k],1).tolist()))[:60])
