import sys, os, json, numpy as np
sys.path.insert(0, os.path.join('..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g=G('../b4/51a/hat3_v9s.glb')
ENT=json.load(open('../adim8/is_tam/hat3_v9c_ent.json',encoding='utf-8'))['parca']
cache={}; bad=0
for a,v in ENT.items():
    d=v['dugum']
    if d not in cache: cache[d]=g.tris(g.byname[d])
    L=cache[d]; X,T=L[0][0],L[0][1]
    s,n=v['indis']; Tt=T[s//3:(s+n)//3]; P=X[Tt.reshape(-1)]
    k=np.array(v['kutu']); f=max(np.abs(P.min(0)-k[[0,2,4]]).max(),np.abs(P.max(0)-k[[1,3,5]]).max())
    if f>0.05: bad+=1; print('FARK',a,round(f,3))
print('ent',len(ENT),'bad',bad,{d:(len(cache[d]),[len(x[1]) for x in cache[d]], max(v['indis'][0]+v['indis'][1] for v in ENT.values() if v['dugum']==d)//3) for d in cache})
