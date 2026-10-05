import sys, os, collections, numpy as np, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cekmece'))
from glb import G
g = G(sys.argv[1])
print('MEK', [(i, m['kod']) for i, m in enumerate(g.MEK) if 'TOPPING' in m['kod']])
print('KAT', [k['kod'] for k in g.J['scenes'][0]['extras']['kategoriler']])
lo0 = np.array([1380, 700, -880.]); hi0 = np.array([2560, 2300, 160.])
C = collections.Counter(); B = {}
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]; sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    for pi, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        P = X[T]; m = np.all(P.max(1) >= lo0, 1) & np.all(P.min(1) <= hi0, 1)
        if not m.any(): continue
        for k in np.unique(mek[m]):
            kk = (nd['name'], g.MEK[k]['kod'] if k >= 0 else '-', 'gizli' if sc < 0.01 else '')
            C[kk] += int((mek[m] == k).sum())
            Q = P[m & (mek == k)].reshape(-1, 3); lo, hi = Q.min(0), Q.max(0)
            if kk in B: B[kk] = (np.minimum(B[kk][0], lo), np.maximum(B[kk][1], hi))
            else: B[kk] = (lo, hi)
for kk in sorted(C): print('%6d %-40s %-28s %s %s %s' % (C[kk], kk[0], kk[1], kk[2], np.round(B[kk][0]).astype(int).tolist(), np.round(B[kk][1]).astype(int).tolist()))
