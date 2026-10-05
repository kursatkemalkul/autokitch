# -*- coding: utf-8 -*-
"""U gövdesi ortak: üçgen örnekleme (≤ ADIM barisentrik ızgara) — topping_govde_denetim.ornekle ile aynı yöntem."""
import numpy as np
ADIM = 4.0


def _W(k):
    a, b = np.meshgrid(np.arange(k + 1), np.arange(k + 1), indexing="ij"); m = (a + b) <= k
    a, b = a[m] / k, b[m] / k
    return np.stack([1 - a - b, a, b], axis=1)


def ornekle(P, zarf=None, adim=ADIM, kmax=None):
    def suz(Q, s):
        if zarf is None: return Q, s
        m = (Q[:, 0] > zarf[0]) & (Q[:, 0] < zarf[1]) & (Q[:, 1] > zarf[2]) & (Q[:, 1] < zarf[3]) & (Q[:, 2] > zarf[4]) & (Q[:, 2] < zarf[5])
        return Q[m], s[m]
    out, src = [], []
    for Q, s in ((P.reshape(-1, 3), np.repeat(np.arange(len(P)), 3)), (P.mean(axis=1), np.arange(len(P)))):
        Q, s = suz(Q, s); out.append(Q); src.append(s)
    L = np.max(np.linalg.norm(P[:, [1, 2, 0]] - P, axis=2), axis=1); n = np.maximum(1, np.ceil(L / adim)).astype(int)
    alan = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); h = 2 * alan / np.maximum(L, 1e-9)
    ince = (h < adim) & (n > 1)
    for e0, e1 in ((0, 1), (1, 2), (2, 0)):
        ii = np.where(ince)[0]
        if not len(ii): break
        Le = np.linalg.norm(P[ii, e1] - P[ii, e0], axis=1); ne = np.maximum(1, np.ceil(Le / adim)).astype(int)
        for k in np.unique(ne):
            jj = ii[ne == k]; tt = np.linspace(0, 1, k + 1)[:, None, None]
            Q = (P[jj, e0][None] + tt * (P[jj, e1] - P[jj, e0])[None]).reshape(-1, 3); s_ = np.tile(jj, k + 1)
            Q, s_ = suz(Q, s_); out.append(Q); src.append(s_)
    n[ince] = 1
    if kmax: n = np.minimum(n, kmax)
    for k in np.unique(n):
        if k == 1: continue
        ii = np.where(n == k)[0]; W = _W(int(k)); parti = max(1, int(2e6 // len(W)))
        for c in range(0, len(ii), parti):
            jj = ii[c:c + parti]
            Q = np.einsum("wk,tkd->twd", W, P[jj]).reshape(-1, 3); s = np.repeat(jj, len(W))
            Q, s = suz(Q, s); out.append(Q); src.append(s)
    return np.concatenate(out), np.concatenate(src)
