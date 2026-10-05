# -*- coding: utf-8 -*-
"""qpaket ortak: bilesen bul (kutuyla, assert), sil, kutu/kapak ekle, delik kapat."""
import sys, numpy as np
from _env import *
import m8kit, glbkit
from m8kit import kutu_ucgen, silindir_ucgen, tup


def prim(G, ad):
    r = [q for q in G.prims if q["name"] == ad and not q.get("gizli")]
    assert r, ad
    return r[0]


def bilesen(G, ad, lo, hi, tol=0.6, n=1):
    """ad primindeki kutusu (lo,hi) ±tol olan bagli bilesen(ler) -> (p, ucgen maskesi, etiket(kat,mek,kpk))"""
    p = prim(G, ad); tl, kut = G.komp(p); vis = G.gorunur(p)
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    sec = [i for i, (a, b, k) in kut.items() if np.all(np.abs(a - lo) < tol) and np.all(np.abs(b - hi) < tol)]
    assert len(sec) == n, (ad, lo, hi, len(sec))
    m = np.isin(tl, sec) & vis
    t0 = int(np.where(m)[0][0])
    return p, m, G._etiketler(p, t0)


def icinde(G, ad, lo, hi, e=0.05):
    """kutunun TAMAMEN icindeki bilesenler"""
    p = prim(G, ad); tl, kut = G.komp(p); vis = G.gorunur(p)
    sec = [i for i, (a, b, k) in kut.items() if np.all(a >= np.asarray(lo) - e) and np.all(b <= np.asarray(hi) + e)]
    return p, np.isin(tl, sec) & vis, sec


def ucgen_kutu(G, p, lo, hi, e=0.02):
    """ucgenlerin TUM koseleri kutu icinde olanlar"""
    P = p["X"][p["T"]]; vis = G.gorunur(p)
    return vis & np.all(P.min(1) >= np.asarray(lo) - e, 1) & np.all(P.max(1) <= np.asarray(hi) + e, 1)


def ekle(G, ad, Pw, et, kpk=None):
    kat, mek, kp = et
    p = prim(G, ad)
    return G._ekle_dunya(p, np.asarray(Pw, float), kat, mek, kp if kpk is None else kpk)


def dortgen(a, b, c, d, nrm):
    """a,b,c,d (sirali) dikdortgen -> 2 ucgen, normal nrm yonunde"""
    T = np.array([[a, b, c], [a, c, d]], float)
    n = np.cross(T[0, 1] - T[0, 0], T[0, 2] - T[0, 0])
    if n @ np.asarray(nrm) < 0: T = T[:, [0, 2, 1]]
    return T


def delik_kapat(G, p, eksen, v0, v1, u0, u1, w0, w1):
    """sacdaki dikdortgen delik (eksen normalli, kalinlik v0..v1, delik [u0,u1]x[w0,w1]; u,w artan eksen sirasi):
    delik duvari ucgenlerini sil + iki yuze dolgu dortgeni ekle (ayni etiket)"""
    a = eksen; u, w = [i for i in range(3) if i != a]
    lo = np.zeros(3); hi = np.zeros(3)
    lo[a], hi[a] = v0, v1; lo[u], hi[u] = u0, u1; lo[w], hi[w] = w0, w1
    P = p["X"][p["T"]]; vis = G.gorunur(p)
    m = ucgen_kutu(G, p, lo, hi)
    # yalniz delik duvarlari (normal a eksenine dik)
    nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-12)
    m &= np.abs(nn[:, a]) < 0.01
    assert m.sum() == 8, ("delik duvari", int(m.sum()))
    t0 = int(np.where(m)[0][0]); et = G._etiketler(p, t0)
    G.sil(p, m)
    def pt(uu, ww, vv):
        q = np.zeros(3); q[a] = vv; q[u] = uu; q[w] = ww; return q
    Pw = []
    for vv, sg in ((v0, -1), (v1, 1)):
        nr = np.zeros(3); nr[a] = sg
        Pw.append(dortgen(pt(u0, w0, vv), pt(u1, w0, vv), pt(u1, w1, vv), pt(u0, w1, vv), nr))
    G._ekle_dunya(p, np.concatenate(Pw), *et)
    return 8
