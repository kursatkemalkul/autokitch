import sys, json, pickle, numpy as np
sys.path.insert(0, r"@@KOK_F@@/tg")
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from glbx import yukle
PK=r"@@PK_V7_F@@"
J,D=yukle(sys.argv[1]); P=json.load(open(PK,encoding='utf-8'))['parca']
nodes=[n for n in D if n.split('__')[0] in sys.argv[2].split(',')]
R={}
for ad in nodes:
    d=D[ad]; b=ad.split('__')[0]
    X,T,ok=d['X'],d['T'],d['ok']
    _,inv=np.unique(np.round(X/0.02).astype(np.int64),axis=0,return_inverse=True); inv=inv.ravel()
    TT=inv[T]; idx=np.where(ok)[0]; nv=inv.max()+1
    g=coo_matrix((np.ones(2*len(idx)),(np.concatenate([TT[idx,0],TT[idx,1]]),np.concatenate([TT[idx,1],TT[idx,2]]))),shape=(nv,nv))
    _,lab=connected_components(g,directed=False)
    tl=np.full(len(T),-1); tl[idx]=lab[TT[idx,0]]
    kut=[(p[0],np.array(p[2:8],float)) for p in P.get(b,[])]
    vol=[max(k[1]-k[0],.01)*max(k[3]-k[2],.01)*max(k[5]-k[4],.01) for _,k in kut]
    at=np.array(['']*len(T),dtype=object)
    print("==",ad, "kpk", d['ex'].get('kpk'))
    for cc in np.unique(tl[idx]):
        ti=np.where(tl==cc)[0]; Q=X[T[ti]].reshape(-1,3); mn,mx=Q.min(0),Q.max(0); e=0.35
        best,bv=None,1e30
        for j,(pa,k) in enumerate(kut):
            if (mn>=k[0::2]-e).all() and (mx<=k[1::2]+e).all() and vol[j]<bv: bv,best=vol[j],pa
        at[ti]=best if best else '?%d'%cc
        print("   %-34s tri %5d [%d..%d] x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f"%(at[ti[0]],len(ti),ti.min(),ti.max(),mn[0],mx[0],mn[1],mx[1],mn[2],mx[2]))
    R[ad]=at
pickle.dump(R,open(sys.argv[3],'wb'))
