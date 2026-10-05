import numpy as np, json, sys, os
DIR=os.environ.get('DIR','zc')
D=np.load(DIR+'/m8_onbellek.npz'); PJ=json.load(open(DIR+'/m8_parca.json',encoding='utf-8'))
A,B,C,P=D['A'],D['B'],D['C'],D['P']; MEK=[m['kod'] for m in PJ['MEK']]
def pts(i):
    s=P==i; return np.concatenate([A[s],B[s],C[s]])
def near(q,r=40,ex=()):
    q=np.array(q,float); out=[]
    for i,p in enumerate(PJ['parca']):
        lo=np.array(p['lo']);hi=np.array(p['hi'])
        d=np.maximum(0,np.maximum(lo-q,q-hi)); dd=np.linalg.norm(d)
        if dd<r and i not in ex: out.append((round(dd,1),i,MEK[p['mek']],p['ad'],p['n'],p['lo'],p['hi']))
    return sorted(out)
lo_=np.minimum(np.minimum(A,B),C); hi_=np.maximum(np.maximum(A,B),C)
def kutuda(K, ex=(), e=0.05):
    m=(hi_[:,0]>K[0]+e)&(lo_[:,0]<K[1]-e)&(hi_[:,1]>K[2]+e)&(lo_[:,1]<K[3]-e)&(hi_[:,2]>K[4]+e)&(lo_[:,2]<K[5]-e)
    out=[]
    for i in np.unique(P[m]):
        if i in ex: continue
        mm=m&(P==i); out.append((int(i),MEK[PJ['parca'][i]['mek']],PJ['parca'][i]['ad'],int(mm.sum()),lo_[mm].min(0).round(2).tolist(),hi_[mm].max(0).round(2).tolist()))
    return out
