import pickle, numpy as np, sys
import manifold3d as mf
sys.stdout.reconfigure(encoding='utf-8')
R=pickle.load(open('bil_v9n_pu.pkl','rb'))
def onar(Pt, r=0.01):
    for rr in (1e-4,r):
        u,inv=np.unique(np.round(Pt.reshape(-1,3)/rr)*rr,axis=0,return_inverse=True); F=inv.reshape(-1,3)
        F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
        m=mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32),tri_verts=F.astype(np.uint32)))
        if m.status()==mf.Error.NoError: return m
def bul(lo,hi,dug=None):
    for d,L in R.items():
        if dug and d!=dug: continue
        for b in L:
            if np.all(np.abs(b['lo']-lo)<0.3) and np.all(np.abs(b['hi']-hi)<0.3): return b
    raise KeyError((lo,hi))
def supur(T,d,L,lo,hi):
    dd=np.asarray(d,float); off=dd*L
    Tm=np.minimum(T.min(1),T.min(1)+off); Tx=np.maximum(T.max(1),T.max(1)+off)
    T=T[np.all(Tx>=lo-1,1)&np.all(Tm<=hi+1,1)]; out=[]
    for t in T:
        n=np.cross(t[1]-t[0],t[2]-t[0])
        if abs(n@off)<1e-9*(np.linalg.norm(n)*L)+1e-12: continue
        h=mf.Manifold.hull_points(np.vstack([t,t+off]).tolist())
        if not h.is_empty(): out.append(h)
    return mf.Manifold.batch_boolean(out,mf.OpType.Add)
print('B_KASA__pu bileşen', len(R['B_KASA__pu']), 'kapalı', sum(b['kapali'] for b in R['B_KASA__pu']))
for b in R['B_KASA__pu']: print('  ', b['no'], b['kapali'], np.round(b['lo'],2).tolist(), np.round(b['hi'],2).tolist())
K={'alt1':((737.5,124.5,-822),(762.5,149.5,-722.5)),'alt2':((737.5,124.5,-689.5),(762.5,149.5,-126.5)),'alt3':((737.5,124.5,-93.5),(762.5,149.5,21)),
   'ust1':((737.5,761.5,-822),(762.5,786.5,-722.5)),'ust2':((737.5,761.5,-689.5),(762.5,786.5,-126.5)),'ust3':((737.5,761.5,-93.5),(762.5,786.5,21)),
   'sag2':((4373.5,761.5,-467.5),(4398.5,786.5,21)),'arka1':((736,124.5,-830),(2090.75,786.5,-805))}
def T(k): return bul(np.array(K[k][0]),np.array(K[k][1]))['P']
main=bul(np.array([737.5,124.5,-827.0]),np.array([797.3,786.5,23.0]),"B_KASA__pu"); X=onar(main['P'])
bb=X.bounding_box(); lo=np.array(bb[:3]); hi=np.array(bb[3:])
for k in ['alt1','alt2','alt3','arka1']: print('pu_sol ana ∩ gölge',k, round((X^supur(T(k),(0,-1,0),1500,lo,hi)).volume(),3))
for k in ['ust1','ust2','ust3']: print('pu_sol ana ∩ iniş yolu',k, round((X^supur(T(k),(0,1,0),1500,lo,hi)).volume(),3))
for lo_,hi_ in [((4028.5,463.5,-469),(4398.5,786.5,-441)),((4338.5,463.5,-441),(4398.5,786.5,23))]:
    X=onar(bul(np.array(lo_),np.array(hi_),'B_KASA__pu')['P'])
    print('tk ana ∩ sag2 yolu', round((X^supur(T('sag2'),(0,1,0),1500,np.array(lo_),np.array(hi_))).volume(),3))
