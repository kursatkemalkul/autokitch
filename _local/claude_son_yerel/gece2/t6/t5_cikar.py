# -*- coding: utf-8 -*-
"""TOPPING v5: hat3_v9w (zincir 00-55) → t5_bil.pkl (mm, dünya). mek TOPPING/* olan tüm üçgenler (kutu dışı dahil: X ekseni A içine uzanır) + bölgedeki diğerleri (çevre)."""
import sys, os, pickle, numpy as np, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
t0 = time.time(); g = G(sys.argv[1]); MEK = g.MEK
TOP = np.array([i for i, m in enumerate(MEK) if m['kod'].startswith('TOPPING/')])
lo0 = np.array([1380, 700, -880.]); hi0 = np.array([2560, 2300, 160.])
OUT = []
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]; sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    if sc < 0.01: continue
    for pi, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        P = X[T]
        m = (np.all(P.max(1) >= lo0, 1) & np.all(P.min(1) <= hi0, 1)) | np.isin(mek, TOP)
        if not m.any(): continue
        ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); m &= ar > 1e-9
        idx = np.where(m)[0]; Tm = T[idx]; mk = mek[idx]
        if not len(Tm): continue
        cl = bilesen(X, Tm)
        for k in np.unique(cl):
            sel = cl == k; Tc = Tm[sel]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True); V = X[u]
            OUT.append(dict(dug=nd['name'], pi=pi, mek=int(np.bincount(mk[sel] + 1).argmax() - 1), ti=idx[sel], V=V, F=inv.reshape(-1, 3), lo=V.min(0), hi=V.max(0)))
print(len(OUT), 'bileşen', round(time.time() - t0, 1), 's')
c = collections.Counter((o['dug'], o['mek']) for o in OUT)
for k, n in sorted(c.items()):
    L = [o for o in OUT if (o['dug'], o['mek']) == k]; lo = np.min([o['lo'] for o in L], 0); hi = np.max([o['hi'] for o in L], 0)
    print(n, k, MEK[k[1]]['kod'] if k[1] >= 0 else '-', np.round(lo), np.round(hi), sum(len(o['F']) for o in L))
pickle.dump(dict(MEK=MEK, L=OUT), open(sys.argv[2], 'wb'))
