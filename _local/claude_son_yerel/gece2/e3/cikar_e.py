# -*- coding: utf-8 -*-
"""E istasyonu (mek 31–38) tüm bileşenleri hat3_v9s.glb'den (tam düğüm dönüşümüyle) → e_bil.pkl (mm)"""
import sys, os, pickle, numpy as np, time, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
t0 = time.time()
g = G(sys.argv[1] if len(sys.argv) > 1 else '../b4/51a/hat3_v9s.glb')
EM = [i for i, m in enumerate(g.MEK) if m['kod'].startswith('E/')]
OUT = []; ATLA = []
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]; sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    for pi, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        sel = np.isin(mek, EM)
        if not sel.any(): continue
        if sc < 0.01: ATLA.append((nd['name'], int(sel.sum()))); continue
        for mk in np.unique(mek[sel]):
            Tm = T[mek == mk]
            P = X[Tm]; ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); Tm = Tm[ar > 1e-9]
            if not len(Tm): continue
            cl = bilesen(X, Tm)
            for c in np.unique(cl):
                Tc = Tm[cl == c]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
                V = X[u]; F = inv.reshape(-1, 3)
                OUT.append(dict(dug=nd['name'], ni=ni, pi=pi, mek=int(mk), V=V, F=F, lo=V.min(0), hi=V.max(0), mat=mat, donusum=not np.allclose(M, np.eye(4))))
print(len(OUT), 'bileşen', round(time.time() - t0, 1), 's · ölçek 0 atlanan', ATLA)
c = collections.Counter((o['dug'], o['mek']) for o in OUT)
for k, n in sorted(c.items(), key=lambda x: x[0][1]):
    L = [o for o in OUT if (o['dug'], o['mek']) == k]
    print('%4d %-34s %-18s %s %s dön=%d' % (n, k[0], g.MEK[k[1]]['kod'], np.round(np.min([o['lo'] for o in L], 0)), np.round(np.max([o['hi'] for o in L], 0)), L[0]['donusum']))
pickle.dump(dict(MEK=g.MEK, E=OUT), open('e_bil.pkl', 'wb'))
