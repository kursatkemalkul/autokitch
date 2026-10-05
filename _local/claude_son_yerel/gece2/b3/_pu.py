import pickle, numpy as np, sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'..\cekmece')
from glb import G
import manifold3d as mf
B=pickle.load(open('b_bil.pkl','rb'))['B']
P=pickle.load(open('b3_parca.pkl','rb'))['P']
def vol(V,F):
    try:
        m=mf.Manifold(mf.Mesh(vert_properties=np.asarray(V,np.float32),tri_verts=np.asarray(F,np.uint32))); return m.volume(), m.status()
    except Exception as e: return None, str(e)
for o in B:
    if o['dug']=='B_KASA__pu' and o['lo'][0]>1419 and o['lo'][0]<1420: print('model comp', len(o['F']), vol(o['V'],o['F']))
print('ent', len(P['g_bolme_1_pu']['F']), vol(P['g_bolme_1_pu']['V'],P['g_bolme_1_pu']['F']))
g=G(r'..\..\hat3_v9l.glb'); X,T=g.tris(g.byname['B_KASA__pu'])[0][:2]
ent=json.load(open(r'..\adim8\is_tam\hat3_v9b_ent.json',encoding='utf-8'))['parca']
used=np.zeros(len(T),bool)
for k,v in ent.items():
    if v['dugum']=='B_KASA__pu': a,n=v['indis']; used[a//3:(a+n)//3]=True
Pt=X[T]; ar=np.linalg.norm(np.cross(Pt[:,1]-Pt[:,0],Pt[:,2]-Pt[:,0]),axis=1)
print('tri', len(T), 'ent kapsar', used.sum(), 'ent dışı', (~used).sum(), 'ent içi dejenere', (ar[used]<1e-9).sum(), 'dışı dejenere', (ar[~used]<1e-9).sum())
