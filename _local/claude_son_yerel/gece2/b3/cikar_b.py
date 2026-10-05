# -*- coding: utf-8 -*-
"""B istasyonu (mek: B/*) tüm bileşenleri hat3_v9l.glb'den çıkarır → b_bil.pkl (mm): her bileşen = (düğüm, prim, mek, V, F)"""
import sys, os, pickle, numpy as np, time
sys.path.insert(0, r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
t0=time.time()
g = G(r'..\..\hat3_v9l.glb')
MEK = g.MEK
print([ (i,m) for i,m in enumerate(MEK) if (m.get('kod') if isinstance(m,dict) else str(m)).startswith('B') ] if isinstance(MEK,list) else MEK)
BM = [i for i,m in enumerate(MEK) if str(m.get('kod') if isinstance(m,dict) else m).startswith('B')]
print('B mek', BM, [MEK[i] for i in BM])
OUT = []
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]; sc = abs(np.linalg.det(M[:3,:3]))**(1/3)
    if sc < 0.01: continue
    for pi,(X,T,mek,mat,ex) in enumerate(g.tris(ni)):
        sel = np.isin(mek, BM)
        if not sel.any(): continue
        for mk in np.unique(mek[sel]):
            Tm = T[mek == mk]
            P = X[Tm]; ar = np.linalg.norm(np.cross(P[:,1]-P[:,0], P[:,2]-P[:,0]), axis=1); Tm = Tm[ar > 1e-9]
            if not len(Tm): continue
            cl = bilesen(X, Tm)
            for c in np.unique(cl):
                Tc = Tm[cl == c]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
                V = X[u]; F = inv.reshape(-1,3)
                OUT.append(dict(dug=nd['name'], pi=pi, mek=int(mk), V=V, F=F, lo=V.min(0), hi=V.max(0)))
print(len(OUT), 'bileşen', round(time.time()-t0,1),'s')
import collections
c = collections.Counter((o['dug'], o['mek']) for o in OUT)
for k,n in sorted(c.items()): print(n, k)
pickle.dump(dict(MEK=MEK, B=OUT), open('b_bil.pkl','wb'))
