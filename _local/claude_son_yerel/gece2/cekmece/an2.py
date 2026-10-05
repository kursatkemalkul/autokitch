import sys, numpy as np
sys.path.insert(0,'.')
from glb import G, bilesen
g=G(sys.argv[1])
lo=np.array([1400,380,-830.]); hi=np.array([2110,520,100.])
for ni,nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    nm=nd.get('name','')
    if nm.startswith('CEK_K2_lahm_3'): continue
    for X,T,mek,mat,ex in g.tris(ni):
        P=X[T]; c=P.mean(1)
        # tri bbox intersects box
        tl=P.min(1); th=P.max(1)
        m=np.all(th>lo,1)&np.all(tl<hi,1)
        if not m.any(): continue
        Tm=T[m]; cl=bilesen(X,Tm); uc=np.unique(cl)
        sc=np.abs(np.linalg.det(g.W[ni][:3,:3]))
        print('==',ni,nm,'tri',int(m.sum()),'/',len(T),'comp',len(uc),'mek',set(mek[m].tolist()),'det',round(sc,4))
        rows=[]
        for cc in uc:
            k=cl==cc; Q=X[Tm[k]].reshape(-1,3); a=Q.min(0); b=Q.max(0)
            rows.append((tuple(np.round(a,1).tolist()),tuple(np.round(b-a,1).tolist()),int(k.sum())))
        rows.sort()
        for r in rows[:60]: print('   lo',r[0],'sz',r[1],'n',r[2])
        if len(rows)>60: print('   ...',len(rows))
