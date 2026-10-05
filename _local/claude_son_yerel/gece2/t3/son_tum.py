import sys, os, pickle, numpy as np, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import manifold3d as mf
D = pickle.load(open('plan_t3.pkl', 'rb')); P = D['P']
ads = [a for a in P if not a.startswith('cevre')]
t0 = time.time()
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=np.asarray(P[a]['F']), tur=P[a]['tur']) for a in ads}
SON = Y.son_kesisim(Pm, ads, 3e-4)
def man(a):
    m = mf.Manifold(mf.Mesh(vert_properties=P[a]['V'].astype(np.float32), tri_verts=np.asarray(P[a]['F']).astype(np.uint32)))
    return m if m.status() == mf.Error.NoError else None
R = {}
for (a, b), n in sorted(SON.items()):
    ma, mb = man(a), man(b); v = None
    if ma is not None and mb is not None: v = (ma ^ mb).volume()
    R[(a, b)] = (n, v)
    print('%-34s ↔ %-34s %5d üçgen · kesişim hacmi %s' % (a, b, n, 'açık ağ' if v is None else '%.2f mm³' % v))
pickle.dump(R, open('son_tum.pkl', 'wb')); print(len(R), 'çift', round(time.time() - t0), 's')
