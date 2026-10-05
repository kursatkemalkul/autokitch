import pickle, numpy as np, sys, time
import manifold3d as mf
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('../b3/b3_parca.pkl','rb')); P=D['P']
R=pickle.load(open('bil_v9m.pkl','rb'))
def onar(Pt, r=0.01):
    u,inv=np.unique(np.round(Pt.reshape(-1,3)/r)*r,axis=0,return_inverse=True); F=inv.reshape(-1,3)
    F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
    m=mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32),tri_verts=F.astype(np.uint32)))
    assert m.status()==mf.Error.NoError
    return m
def bul(a):
    lo,hi=P[a]['V'].min(0),P[a]['V'].max(0)
    for d,L in R.items():
        for b in L:
            if np.all(np.abs(b['lo']-lo)<0.3) and np.all(np.abs(b['hi']-hi)<0.3): return d,b
    raise KeyError(a)
def tri(a):
    try: return bul(a)[1]['P']
    except KeyError: return P[a]['V'][np.asarray(P[a]['F'])]
def man(a): return onar(tri(a))
def sweep(a, d, L=1500.0, lo=None, hi=None):
    T=tri(a); dd=np.asarray(d,float)
    if lo is not None:
        Tm=T.min(1); Tx=T.max(1); Tm2=np.minimum(Tm,Tm+dd*L); Tx2=np.maximum(Tx,Tx+dd*L)
        k=np.all(Tx2>=lo-1,1)&np.all(Tm2<=hi+1,1); T=T[k]
    off=dd*L; L_=[]
    for t in T:
        n=np.cross(t[1]-t[0],t[2]-t[0])
        if abs(n@off)<1e-9*np.linalg.norm(n)*L+1e-12: continue
        h=mf.Manifold.hull_points(np.vstack([t,t+off]).tolist())
        if not h.is_empty(): L_.append(h)
    try: L_.append(man(a))
    except Exception: pass
    return mf.Manifold.batch_boolean(L_, mf.OpType.Add)
def rap(ad, m):
    parts=m.decompose()
    print('  %s: %d parça, toplam %.1f mm³'%(ad,len(parts),m.volume()))
    for p in sorted(parts,key=lambda p:-p.volume())[:10]:
        b=p.bounding_box(); print('     %.2f mm³  lo %s hi %s'%(p.volume(),np.round(b[:3],2),np.round(b[3:],2)))
if __name__=='__main__':
    t0=time.time()
    for pu,once,sonra in [('g_pu_sol',['g_dis_taban_1','g_kosebent_sol_alt_1','g_kosebent_sol_alt_2','g_kosebent_sol_alt_3','g_dis_arka_1','g_dis_arka_ek_lamasi','g_dis_sol_yan','gfrp_alt','g_pu_taban_0','g_ic_taban_1','g_pu_arka_yuksek'],
                                ['g_kosebent_sol_ust_1','g_kosebent_sol_ust_2','g_kosebent_sol_ust_3','moduler_cerceve_arka','moduler_cerceve_on']),
                          ('g_pu_arka_yuksek',['g_dis_taban_1','g_dis_arka_1','g_dis_arka_ek_lamasi','g_dis_arka_2','g_pu_taban_0','g_ic_taban_1','g_kosebent_sol_alt_1'],[]),
                          ('g_pu_arka_alcak',['g_dis_taban_2','g_dis_arka_2','g_dis_arka_ek_lamasi','g_pu_taban_0','g_ic_taban_2'],[]),
                          ('g_tk_depo_arka_pu',[],['g_kosebent_sag_ust_2']),('g_tk_depo_sag_pu',[],['g_kosebent_sag_ust_2'])]:
        X=man(pu); bb=X.bounding_box(); lo=np.array(bb[:3]); hi=np.array(bb[3:])
        print('==',pu,'hacim %.0f'%X.volume())
        for o in once:
            r=X^sweep(o,(0,-1,0),1500,lo,hi)
            if r.volume()>1e-3: rap('gölge(üstten) '+o, r)
        for o in sonra:
            r=X^sweep(o,(0,1,0),1500,lo,hi)
            if r.volume()>1e-3: rap('sonra(üstten iner) '+o, r)
    print('%.1f s'%(time.time()-t0))
