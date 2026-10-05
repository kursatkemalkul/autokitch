import sys, numpy as np, json
sys.path.insert(0,'.')
from glb import G, bilesen
g=G(sys.argv[1]); pre=sys.argv[2]
for nm,ni in sorted(g.byname.items(), key=lambda x:x[1]):
    if not nm or not nm.startswith(pre): continue
    nd=g.J['nodes'][ni]
    for X,T,mek,mat,ex in g.tris(ni):
        cl=bilesen(X,T); uc=np.unique(cl)
        P=X[T]
        print('==',ni,nm,'tri',len(T),'comp',len(uc),'mek',set(mek.tolist()),'ex',list(ex.keys()))
        rows=[]
        for c in uc:
            m=cl==c; Q=P[m].reshape(-1,3); lo=Q.min(0); hi=Q.max(0)
            rows.append((tuple(np.round(lo,1)),tuple(np.round(hi-lo,1)),int(m.sum())))
        rows.sort()
        for r in rows[:80]: print('   lo',r[0],'sz',r[1],'n',r[2])
        if len(rows)>80: print('   ...',len(rows))
