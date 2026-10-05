import pickle,numpy as np,trimesh,sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.stdout.reconfigure(encoding='utf-8')
P=pickle.load(open('parca.pkl','rb'))
for a in sys.argv[1:]:
    V=P[a]['V']*1000;F=np.asarray(P[a]['F'])
    n=len(V); r=np.concatenate([F[:,0],F[:,1]]); c=np.concatenate([F[:,1],F[:,2]])
    k,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False)
    print(a,'bileşen',k)
    for i in range(k):
        fm=lab[F[:,0]]==i
        m=trimesh.Trimesh(V,F[fm],process=True)
        print('  wt',m.is_watertight,'bb',np.round(m.bounds,2).tolist(),'vol %.1f'%m.volume, 'tri',fm.sum())
