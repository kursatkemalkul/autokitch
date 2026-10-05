import pickle, numpy as np, sys, trimesh
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('b3_parca.pkl','rb')); P=D['P']
LO={a:P[a]['V'].min(0) for a in P}; HI={a:P[a]['V'].max(0) for a in P}
TM={}
def tm(a):
    if a not in TM: TM[a]=trimesh.Trimesh(P[a]['V'],P[a]['F'],process=False)
    return TM[a]
def temas(a, tol=0.6):
    out=[]
    Va=P[a]['V']
    # örnek noktalar: köşeler + yüz merkezleri
    T=Va[P[a]['F']]; S=np.vstack([Va, T.mean(1)])
    for b in P:
        if b==a: continue
        if np.any(LO[b]>HI[a]+tol) or np.any(HI[b]<LO[a]-tol): continue
        Q=S[np.all((S>=LO[b]-tol)&(S<=HI[b]+tol),1)]
        if not len(Q): continue
        cp,d,tid=trimesh.proximity.closest_point(tm(b),Q)
        k=d<tol
        if k.any():
            n=tm(b).face_normals[tid[k]]
            nm=np.round(np.mean(n,0),2)
            out.append((b,int(k.sum()),round(float(d[k].min()),3),nm.tolist()))
    return out
for a in sys.argv[1:]:
    print('==',a, np.round(LO[a],1), np.round(HI[a],1))
    for r in sorted(temas(a), key=lambda r:-r[1])[:12]: print('   ',r)
