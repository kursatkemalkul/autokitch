import sys, json, numpy as np, collections
sys.path.insert(0, r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(r'..\..\hat3_v9l.glb')
d = json.load(open(r'..\adim8\is_tam\hat3_v9b_ent.json', encoding='utf-8'))['parca']
by = collections.defaultdict(list)
for k, v in d.items(): by[v['dugum']].append((k, v))
for dug, L in by.items():
    ni = g.byname[dug]; tr = g.tris(ni)
    X, T = tr[0][0], tr[0][1]
    tot = sum(v['indis'][1] for k, v in L)
    bad = 0; worst = 0
    for k, v in L:
        a, n = v['indis']; Tt = T[a // 3:(a + n) // 3]
        if not len(Tt): bad += 1; continue
        P = X[Tt].reshape(-1, 3); lo, hi = P.min(0), P.max(0); kb = np.array(v['kutu'])
        f = max(np.abs(lo - kb[[0, 2, 4]]).max(), np.abs(hi - kb[[1, 3, 5]]).max()); worst = max(worst, f)
        if f > 0.05: bad += 1
    print(dug, 'prims', len(tr), 'tri', len(T), 'ent toplam', tot, 'kötü', bad, '/', len(L), 'en kötü', round(worst, 3))
