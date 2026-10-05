import sys, os, json, numpy as np, manifold3d as mf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(sys.argv[1])
ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']
X, T = g.tris(g.byname['TOPPING_GOVDE__pu'])[0][:2]
for a in ('pu_soguk_duvar', 'pu_raf_esik'):
    s, n = ENT[a]['indis']; Tt = T[s // 3:(s + n) // 3]
    u, inv = np.unique(np.round(X[Tt.reshape(-1)], 4), axis=0, return_inverse=True); F = inv.reshape(-1, 3)
    m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
    print(a, len(F), 'status', m.status(), 'vol', m.volume() if m.status() == mf.Error.NoError else None, 'genus', m.genus() if m.status() == mf.Error.NoError else None)
    # x kesitleri: y-z düzleminde kaç üçgen düşey
    for yy in (1130, 1500, 2160):
        P = u[F]; m2 = (P[:, :, 1].min(1) < yy) & (P[:, :, 1].max(1) > yy)
        print('  y=%d kesen üçgen %d · x aralığı %s z aralığı %s' % (yy, m2.sum(), np.round([P[m2][:, :, 0].min(), P[m2][:, :, 0].max()]), np.round([P[m2][:, :, 2].min(), P[m2][:, :, 2].max()])))
    np.save(a + '.npy', u); np.save(a + '_F.npy', F)
