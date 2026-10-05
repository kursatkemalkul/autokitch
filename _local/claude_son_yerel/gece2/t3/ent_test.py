import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(sys.argv[1])
ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']
NT = {}
kotu = 0
for a, v in ENT.items():
    d = v['dugum']
    if d not in g.byname: print('YOK düğüm', d); kotu += 1; continue
    if d not in NT: NT[d] = g.tris(g.byname[d])
    pr = NT[d]
    X, T = pr[0][0], pr[0][1]
    s, n = v['indis']; Tt = T[s // 3:(s + n) // 3]
    if len(Tt) * 3 != n: print('KISA', a, len(Tt) * 3, n); kotu += 1; continue
    V = X[Tt.reshape(-1)]; lo, hi = V.min(0), V.max(0); k = np.array(v['kutu'])
    f = max(np.abs(lo - k[[0, 2, 4]]).max(), np.abs(hi - k[[1, 3, 5]]).max())
    if f > 0.02: print('FARK', a, d, round(f, 3)); kotu += 1
for d in NT:
    son = max(v['indis'][0] + v['indis'][1] for v in ENT.values() if v['dugum'] == d) // 3
    print(d, 'prim', len(NT[d]), 'üçgen', len(NT[d][0][1]), 'ent sonu', son)
print('KÖTÜ', kotu, '/', len(ENT))
