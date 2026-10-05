import sys, os, json, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g=G(os.path.join(HERE,'..','..','hat3_v9l.glb'))
print([ (i,m) for i,m in enumerate(g.MEK) if str(m.get('kod') if isinstance(m,dict) else m).startswith(('A','TOP'))][:20])
ENT=json.load(open(os.path.join(HERE,'..','adim8','is_tam','hat3_v9a_ent.json'),encoding='utf-8'))['parca']
for n,nd in enumerate(g.J['nodes']):
    nm=nd.get('name','')
    if 'mesh' in nd and (nm.startswith(('A_','KAIDE_A','U_A','ACICI')) or 'ACICI' in nm or 'TABLA' in nm):
        L=g.tris(n); s=sum(len(x[1]) for x in L)
        X=np.vstack([x[0] for x in L]); print(n,nm,len(L),s,np.round(X.min(0)),np.round(X.max(0)))
# validate ent
bad=0
cache={}
for a,v in ENT.items():
    d=v['dugum']
    if d not in cache: cache[d]=g.tris(g.byname[d])[0][:2]
    X,T=cache[d]; s,nn=v['indis']; Tt=T[s//3:(s+nn)//3]; P=X[Tt.reshape(-1)]
    k=np.array(v['kutu']); f=max(np.abs(P.min(0)-k[[0,2,4]]).max(),np.abs(P.max(0)-k[[1,3,5]]).max())
    if f>0.05: bad+=1; print('FARK',a,round(f,3))
print('ent',len(ENT),'bad',bad, {d:len(cache[d][1]) for d in cache})
