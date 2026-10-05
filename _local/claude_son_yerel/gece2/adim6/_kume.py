# -*- coding: utf-8 -*-
"""ana grup → bağlı bileşen kümeleri (bbox teması 1 mm ile birleşir) · inceleme"""
import sys, pickle, re, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.stdout.reconfigure(encoding='utf-8')


def bilesen(V, F):
    u, inv = np.unique(np.round(V / 2e-5).astype(np.int64), axis=0, return_inverse=True); inv = inv.reshape(-1)
    Ti = inv[F]
    r = np.concatenate([Ti[:, 0], Ti[:, 1]]); c = np.concatenate([Ti[:, 1], Ti[:, 2]])
    k, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(u), len(u))), directed=False)
    return cl[Ti[:, 0]]


def kumele(V, F, tol=0.001):
    tl = bilesen(V, F)
    ids = np.unique(tl)
    lo = np.array([V[F[tl == i]].reshape(-1, 3).min(0) for i in ids]); hi = np.array([V[F[tl == i]].reshape(-1, 3).max(0) for i in ids])
    n = len(ids); par = list(range(n))

    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for i in range(n):
        m = np.all((lo <= hi[i] + tol) & (hi >= lo[i] - tol), axis=1); m[i] = False
        for j in np.where(m)[0]:
            a, b = f(i), f(j)
            if a != b: par[a] = b
    kok = np.array([f(i) for i in range(n)])
    out = []
    for k in np.unique(kok):
        sec = np.isin(tl, ids[kok == k])
        out.append(sec)
    return out


if __name__ == '__main__':
    L = pickle.load(open(sys.argv[1], 'rb')); rx = re.compile(sys.argv[2])
    for g in L:
        key = '%s %s' % (g['dugum'], g['mek_kod'])
        if not rx.search(key): continue
        ks = kumele(g['V'].astype(float), g['F'].astype(np.int64))
        print('==', key, 'K' if g['kpk'] else '', len(g['F']), '→', len(ks), 'küme')
        for s in sorted(ks, key=lambda s: g['V'][g['F'][s]].reshape(-1, 3).min(0)[1])[:40]:
            Q = g['V'][g['F'][s]].reshape(-1, 3); lo = Q.min(0); hi = Q.max(0)
            print('    %6d  x %.3f–%.3f y %.3f–%.3f z %.3f–%.3f' % (s.sum(), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
