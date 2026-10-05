# -*- coding: utf-8 -*-
"""m8 ortam: tüm görünür üçgenler + sahip (prim, bileşen) + rtree. Yardımcılar: segment-üçgen kesişimi, nokta-en yakın üçgen. SALT OKUMA."""
import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import glbkit, m7_etiket
from rtree import index as rindex
from trimesh.triangles import closest_point as tri_cp
GLB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "hat3_v8x.glb")
G = glbkit.Glb(GLB)
PK = m7_etiket.pk_yeni([os.path.join(os.path.dirname(os.path.dirname(HERE)), "m7", f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])
TRI = []; OWN = []; KPK = []
KOMP = {}
for pid, p in enumerate(G.prims):
    vis = G.gorunur(p)
    if not vis.any(): continue
    tl, kut = G.komp(p); KOMP[pid] = (tl, kut)
    kp = G.kpk_maske(p)
    TRI.append(p['X'][p['T'][vis]]); OWN.append(np.stack([np.full(vis.sum(), pid), tl[vis]], 1)); KPK.append(kp[vis])
TRI = np.concatenate(TRI); OWN = np.concatenate(OWN); KPK = np.concatenate(KPK)
LO = TRI.min(1); HI = TRI.max(1)
print('ucgen', len(TRI))


def _gen():
    for i in range(len(TRI)): yield (i, (LO[i, 0], LO[i, 1], LO[i, 2], HI[i, 0], HI[i, 1], HI[i, 2]), None)


pr = rindex.Property(); pr.dimension = 3
TREE = rindex.Index(_gen(), properties=pr)
print('agac tamam')
_AD = {}


def ad(pid, c):
    k = (int(pid), int(c))
    if k in _AD: return _AD[k]
    p = G.prims[pid]; base = p['name'].split('__')[0]
    lo, hi, n = KOMP[pid][1][int(c)]
    best, bv = None, 1e30
    for q in PK.get(base, []):
        kk = np.array(q[2:8], float)
        if (lo >= kk[0::2] - 0.6).all() and (hi <= kk[1::2] + 0.6).all():
            v = max(kk[1] - kk[0], .01) * max(kk[3] - kk[2], .01) * max(kk[5] - kk[4], .01)
            if v < bv: bv, best = v, q[0]
    _AD[k] = "%s/%s" % (p['name'], best or ('#%d' % c))
    return _AD[k]


def kutu(pid, c): return KOMP[pid][1][int(c)]


def aday(lo, hi):
    return np.fromiter(TREE.intersection((lo[0], lo[1], lo[2], hi[0], hi[1], hi[2])), dtype=np.int64)


def seg_kesis(a, b, haric=None):
    """a→b doğru parçasını kesen üçgenler: [(t, tri)]"""
    lo = np.minimum(a, b) - 1e-3; hi = np.maximum(a, b) + 1e-3
    c = aday(lo, hi)
    if len(c) == 0: return []
    if haric is not None: c = c[~haric(OWN[c])]
    if len(c) == 0: return []
    V0, V1, V2 = TRI[c, 0], TRI[c, 1], TRI[c, 2]
    d = b - a; e1 = V1 - V0; e2 = V2 - V0
    h = np.cross(d, e2); det = np.einsum('ij,ij->i', e1, h)
    ok = np.abs(det) > 1e-12; f = np.zeros_like(det); f[ok] = 1.0 / det[ok]
    s = a - V0; u = f * np.einsum('ij,ij->i', s, h)
    q = np.cross(s, e1); v = f * (q @ d); t = f * np.einsum('ij,ij->i', e2, q)
    m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t >= 0) & (t <= 1)
    return list(zip(t[m], c[m]))


def en_yakin(P, rad, haric=None):
    """nokta P'ye rad içindeki en yakın üçgen: (mesafe, tri, nokta) ya da None"""
    c = aday(P - rad, P + rad)
    if haric is not None and len(c): c = c[~haric(OWN[c])]
    if len(c) == 0: return None
    cp = tri_cp(TRI[c], np.repeat(P[None], len(c), 0)); d = np.linalg.norm(cp - P, axis=1)
    d = np.where(np.isfinite(d), d, 1e9)
    i = int(np.argmin(d))
    if d[i] > rad: return None
    return float(d[i]), int(c[i]), cp[i]
