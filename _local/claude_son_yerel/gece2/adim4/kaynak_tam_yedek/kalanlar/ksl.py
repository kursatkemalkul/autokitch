import numpy as np, json, sys
from scipy.cluster.hierarchy import fcluster, linkage
Z=np.load("m8_onbellek.npz"); d=json.load(open("m8_parca.json"))
A,B,C=Z["A"],Z["B"],Z["C"]; P=Z["P"]
def kes(k,ax,v):
    m=P==k; T=np.stack([A[m],B[m],C[m]],1); out=[]
    for i,j in ((0,1),(1,2),(2,0)):
        a=T[:,i];b=T[:,j]; s=(a[:,ax]-v)*(b[:,ax]-v)<0
        t=(v-a[s,ax])/(b[s,ax]-a[s,ax]); out.append(a[s]+t[:,None]*(b[s]-a[s]))
    Q=np.concatenate(out)
    if len(Q)<3: return []
    L=fcluster(linkage(Q,'single'),1.0,'distance')
    return [(Q[L==l].mean(0).round(2).tolist(), (Q[L==l].max(0)-Q[L==l].min(0)).round(2).tolist()) for l in np.unique(L)]
k=int(sys.argv[1]); ax=int(sys.argv[2])
for v in map(float,sys.argv[3:]): print(v, kes(k,ax,v))
