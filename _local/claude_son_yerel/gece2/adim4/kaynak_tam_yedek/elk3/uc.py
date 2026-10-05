import numpy as np, json
from vox import *
A,B,C,P,ad,kpk=yukle()
PJ=json.load(open(S+r"\elk2\zj\m8_parca.json"))['parca']
def verts(i):
    m=P==i; V=np.concatenate([A[m],B[m],C[m]]); return V
for i in (706,711,3290,3291,418,2691,19,321,3283):
    V=verts(i); print(i,PJ[i]['ad'],len(V))
    for ax in range(3):
        for f in (np.argmin,np.argmax):
            print("   ",['x','y','z'][ax],['min','max'][f is np.argmax], np.round(V[f(V[:,ax])],1).tolist())
# QR cable ends
for nm in ("ELK_QR_KABLO__kablo","ELK_QR_KABLO__kablo_veri"):
    ii=[k for k,q in enumerate(PJ) if q['ad']==nm]
    m=np.isin(P,ii); V=np.concatenate([A[m],B[m],C[m]])
    low=V[V[:,1]<200]; print(nm,"low verts y<200", low[:,1].min() if len(low) else None)
    if len(low):
        for yv in np.unique(np.round(low[:,1])):
            s=low[np.round(low[:,1])==yv]; print("   y",yv,"x",s[:,0].min().round(1),s[:,0].max().round(1),"z",s[:,2].min().round(1),s[:,2].max().round(1),len(s))
