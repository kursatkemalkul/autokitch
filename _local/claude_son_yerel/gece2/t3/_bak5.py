import pickle, numpy as np, sys, trimesh
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('t3_parca.pkl','rb'))['P']
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
for a,ys in (('kondenser_kanali',(1090,1100,1105,1108,1112,1130)),('kuru_bolme_tabani',(1108.2,))):
    m = trimesh.Trimesh(D[a]['V'], D[a]['F'], process=False)
    for y in ys:
        s = m.section(plane_origin=[0,y,0], plane_normal=[0,1,0])
        if s is None: print(a,y,'yok'); continue
        V = s.vertices; E = np.array([e.points for e in s.entities])
        n, cl = connected_components(coo_matrix((np.ones(len(E)), (E[:,0], E[:,1])), shape=(len(V),len(V))), directed=False)
        for k in range(n):
            P = V[cl==k]
            if len(P)<2: continue
            print(a, y, 'x %.1f..%.1f z %.1f..%.1f' % (P[:,0].min(), P[:,0].max(), P[:,2].min(), P[:,2].max()))
