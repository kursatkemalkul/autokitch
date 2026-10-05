# -*- coding: utf-8 -*-
"""m8t2: kablo eksenleri (kapsul) arasi carpisma: segment-segment mesafe < r1 + r2 + bosluk"""
import numpy as np


def segseg(p1, q1, p2, q2):
    d1 = q1 - p1; d2 = q2 - p2; r = p1 - p2
    a = d1 @ d1; e = d2 @ d2; f = d2 @ r
    if a < 1e-12 and e < 1e-12: return np.linalg.norm(p1 - p2), p1, p2
    if a < 1e-12:
        s = 0.0; t = np.clip(f / e, 0, 1)
    else:
        c = d1 @ r
        if e < 1e-12:
            t = 0.0; s = np.clip(-c / a, 0, 1)
        else:
            b = d1 @ d2; den = a * e - b * b
            s = np.clip((b * f - c * e) / den, 0, 1) if den > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0: t = 0.0; s = np.clip(-c / a, 0, 1)
            elif t > 1: t = 1.0; s = np.clip((b - c) / a, 0, 1)
    c1 = p1 + d1 * s; c2 = p2 + d2 * t
    return np.linalg.norm(c1 - c2), c1, c2


def carp(kablolar, bosluk=0.3, sadece=None):
    """kablolar: {ad: (r, pts)} -> [(a, b, nokta, derinlik)]"""
    ad = list(kablolar)
    out = []
    S = {}
    for k in ad:
        r, P = kablolar[k]; P = np.asarray(P, float)
        S[k] = (r, P[:-1], P[1:], np.minimum(P[:-1], P[1:]) - r, np.maximum(P[:-1], P[1:]) + r)
    for i in range(len(ad)):
        for j in range(i + 1, len(ad)):
            a, b = ad[i], ad[j]
            if sadece and a not in sadece and b not in sadece: continue
            ra, A0, A1, alo, ahi = S[a]; rb, B0, B1, blo, bhi = S[b]
            lim = ra + rb + bosluk
            for u in range(len(A0)):
                m = np.all((bhi + bosluk >= alo[u]) & (blo - bosluk <= ahi[u]), axis=1)
                for v in np.where(m)[0]:
                    d, c1, c2 = segseg(A0[u], A1[u], B0[v], B1[v])
                    if d < lim - 1e-6: out.append((a, b, (c1 + c2) / 2, lim - d))
    return out
