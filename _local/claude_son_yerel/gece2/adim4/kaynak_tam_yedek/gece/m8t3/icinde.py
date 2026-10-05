import numpy as np, json
from gap import A,B,C,P,PA
def ic(q, d=(0.0123,1.0,0.0071)):
    """q noktasini iceren (isin paritesi) parcalar; yalniz q'ya 60 mm icindeki parcalar"""
    q=np.asarray(q,float); d=np.asarray(d,float); d/=np.linalg.norm(d)
    lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
    near=np.unique(P[np.all(lo<=q+3,1)&np.all(hi>=q-3,1)])
    out=[]
    for p in near:
        I=np.where(P==p)[0]; a,b,c=A[I],B[I],C[I]
        e1=b-a; e2=c-a; h=np.cross(d,e2); det=(e1*h).sum(1); ok=np.abs(det)>1e-12
        f=1/np.where(ok,det,1); s=q-a; u=f*(s*h).sum(1); qq=np.cross(s,e1); v=f*(qq*d).sum(1)[...,None][:,0] if False else f*(qq@d)
        t=f*(e2*qq).sum(1)
        hit=ok&(u>=0)&(v>=0)&(u+v<=1)&(t>1e-9)
        n=hit.sum()
        if n%2==1: out.append((int(p),PA[p]["ad"]))
    return out
if __name__=="__main__":
    import sys
    for q in json.loads(sys.argv[1]): print(q, ic(q))
