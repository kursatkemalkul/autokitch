# -*- coding: utf-8 -*-
"""Düzlem kesiti → PNG. python kesit.py glb seg.pkl out.png eksen deger [--ad desen] [--parca desen] [--sinir x0,x1,y0,y1]"""
import sys, pickle, argparse, hashlib
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
sys.path.insert(0, '.')
from glbx import yukle
ap = argparse.ArgumentParser(); ap.add_argument('glb'); ap.add_argument('seg'); ap.add_argument('out'); ap.add_argument('eksen'); ap.add_argument('deger', type=float)
ap.add_argument('--ad', default=''); ap.add_argument('--parca', default=''); ap.add_argument('--sinir', default=''); ap.add_argument('--etiket', type=int, default=1); ap.add_argument('--boy', default='22,14')
a = ap.parse_args()
J, D = yukle(a.glb); R = pickle.load(open(a.seg, 'rb')) if a.seg != '-' else {}
ax_ = 'xyz'.index(a.eksen); u, v = {0: (2, 1), 1: (0, 2), 2: (0, 1)}[ax_]
fig, ax = plt.subplots(figsize=[float(s) for s in a.boy.split(',')])
sn = [float(s) for s in a.sinir.split(',')] if a.sinir else None
for ad, d in D.items():
    if a.ad and not any(s in ad for s in a.ad.split(',')): continue
    X, T, ok = d['X'], d['T'], d['ok']
    P = X[T[ok]]; s = P[..., ax_] - a.deger
    m = (s.min(1) < 0) & (s.max(1) > 0)
    if not m.any(): continue
    L = R.get(ad, np.array([ad] * len(T), dtype=object))[ok][m]
    P = P[m]; s = s[m]
    segs = []
    for e0, e1 in ((0, 1), (1, 2), (2, 0)):
        pass
    # her üçgen için kesişim doğrusu
    pts = []
    for e0, e1 in ((0, 1), (1, 2), (2, 0)):
        a0, a1 = s[:, e0], s[:, e1]
        cr = (a0 * a1) < 0
        t = np.where(cr, a0 / np.where(cr, a0 - a1, 1), np.nan)
        q = P[:, e0] + (P[:, e1] - P[:, e0]) * t[:, None]
        pts.append(np.where(cr[:, None], q, np.nan))
    pts = np.stack(pts, 1)  # n,3,3
    for p in sorted(set(L)):
        if a.parca and not any(s_ in p or s_ in ad for s_ in a.parca.split(',')): continue
        mm = L == p; Q = pts[mm]
        sg = []
        for q in Q:
            w = q[~np.isnan(q[:, 0])]
            if len(w) >= 2: sg.append([(w[0][u], w[0][v]), (w[1][u], w[1][v])])
        if not sg: continue
        h = hashlib.md5((ad + p).encode()).digest(); col = (h[0] / 300, h[1] / 300, h[2] / 300)
        if 'pu' in (ad + p).lower() or 'yalitim' in (ad + p).lower(): col = (0.85, 0.65, 0.0)
        ax.add_collection(LineCollection(sg, colors=[col], linewidths=0.7))
        if a.etiket:
            c = np.array(sg).reshape(-1, 2)
            if sn is None or (sn[0] < c[:, 0].mean() < sn[1] and sn[2] < c[:, 1].mean() < sn[3]):
                ax.text(c[:, 0].mean(), c[:, 1].mean(), p[:30], fontsize=5, color=col)
ax.set_aspect('equal'); ax.autoscale()
if sn: ax.set_xlim(sn[0], sn[1]); ax.set_ylim(sn[2], sn[3])
ax.grid(True, lw=0.2); ax.set_xlabel('xyz'[u]); ax.set_ylabel('xyz'[v])
plt.savefig(a.out, dpi=110, bbox_inches='tight'); print('ok', a.out)
