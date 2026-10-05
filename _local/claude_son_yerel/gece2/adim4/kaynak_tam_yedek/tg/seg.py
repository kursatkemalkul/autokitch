# -*- coding: utf-8 -*-
"""Birleşik GLB düğümlerini parçalara ayır: kaynaklı köşe → bağlı bileşen → parca_kutulari kutusuna (en küçük kapsayan) ata.
python seg.py glb parca_kutulari.json cikis.pkl birim1,birim2 ..."""
import sys, json, pickle
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
sys.path.insert(0, '.')
from glbx import yukle
gi, pk, out, birimler = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(',')
J, D = yukle(gi)
P = json.load(open(pk, encoding='utf-8'))['parca']
R = {}
for ad, d in D.items():
    b = ad.split('__')[0]
    if b not in birimler: continue
    X, T, ok = d['X'], d['T'], d['ok']
    key = np.round(X / 0.02).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    TT = inv[T]
    n = len(T); idx = np.where(ok)[0]
    # üçgen-köşe çizgesi: düğümler = köşeler; bileşen = köşe bileşeni
    nv = inv.max() + 1
    r = np.concatenate([TT[idx, 0], TT[idx, 1]]); c = np.concatenate([TT[idx, 1], TT[idx, 2]])
    g = coo_matrix((np.ones(len(r)), (r, c)), shape=(nv, nv))
    nc, lab = connected_components(g, directed=False)
    tl = np.full(n, -1); tl[idx] = lab[TT[idx, 0]]
    kut = [(p[0], np.array(p[2:8], float)) for p in P.get(b, [])]
    vol = np.array([max((k[1]-k[0]), .01)*max((k[3]-k[2]), .01)*max((k[5]-k[4]), .01) for _, k in kut]) if kut else np.zeros(0)
    ad_t = np.array([''] * n, dtype=object)
    comps = np.unique(tl[idx])
    e = 0.35
    for cc in comps:
        ti = np.where(tl == cc)[0]
        Q = X[T[ti]].reshape(-1, 3); mn = Q.min(0); mx = Q.max(0)
        best = None; bv = 1e30
        for j, (pa, k) in enumerate(kut):
            if mn[0] >= k[0]-e and mx[0] <= k[1]+e and mn[1] >= k[2]-e and mx[1] <= k[3]+e and mn[2] >= k[4]-e and mx[2] <= k[5]+e:
                if vol[j] < bv: bv = vol[j]; best = pa
        ad_t[ti] = best if best else '?%d' % cc
    R[ad] = ad_t
    bil = sum(1 for s in set(ad_t[idx]) if s.startswith('?'))
    print('%-40s %7d üçgen  %5d bileşen  %4d parça  %4d atanamadı' % (ad, n, len(comps), len(set(ad_t[idx])), bil))
pickle.dump(R, open(out, 'wb'))
