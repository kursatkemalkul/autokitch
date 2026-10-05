# -*- coding: utf-8 -*-
"""m8 adım 1: GLB'den kablo / hortum / boru bileşenleri -> merkez çizgisi (geodezik dilim), yarıçap, uçlar, ad. SALT OKUMA."""
import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import glbkit, m7_etiket
sys.path.insert(0, HERE)
import serit
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, connected_components
GLB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "hat3_v8x.glb")
LIN = ('kablo', 'kablo_veri', 'hava_ana', 'hava', 'bakir', 'hortum_gida', 'hortum_yag', 'hortum_orgu', 'zincir')
G = glbkit.Glb(GLB)
PK = m7_etiket.pk_yeni([os.path.join(os.path.dirname(os.path.dirname(HERE)), "m7", f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])


def rdp(P, eps):
    if len(P) < 3: return P
    a, b = P[0], P[-1]; ab = b - a; L = np.linalg.norm(ab)
    if L < 1e-9: d = np.linalg.norm(P - a, axis=1)
    else: d = np.linalg.norm(np.cross(P - a, ab / L), axis=1)
    i = int(np.argmax(d))
    if d[i] > eps: return np.vstack([rdp(P[:i + 1], eps)[:-1], rdp(P[i:], eps)])
    return np.vstack([a, b])


def merkez(u, Ti):
    n = len(u)
    e = np.concatenate([Ti[:, [0, 1]], Ti[:, [1, 2]], Ti[:, [2, 0]]]); e = np.unique(np.sort(e, 1), axis=0)
    w = np.linalg.norm(u[e[:, 0]] - u[e[:, 1]], axis=1) + 1e-9
    M = coo_matrix((np.r_[w, w], (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(n, n)).tocsr()
    d0 = dijkstra(M, indices=0); d0[~np.isfinite(d0)] = -1
    A = int(np.argmax(d0)); dA = dijkstra(M, indices=A); dA[~np.isfinite(dA)] = -1; B = int(np.argmax(dA))
    # kaba yarıçap: A ucuna yakın halka
    out = None
    for it in range(2):
        if it == 0: src = [A]
        else:
            src = list(np.where(np.linalg.norm(u - u[A], axis=1) < 1.6 * r0 + 0.5)[0])
        d = dijkstra(M, indices=src, min_only=True); d[~np.isfinite(d)] = np.nan
        Lg = np.nanmax(d); w_ = 2.5 if it == 0 else max(1.5, min(6.0, 0.8 * r0))
        nb = max(1, int(np.ceil(Lg / w_))); bi = np.minimum((np.nan_to_num(d, nan=0) / w_).astype(int), nb - 1)
        C, R = [], []
        for k in range(nb):
            m = bi == k
            if m.sum() < 3: continue
            c = u[m].mean(0); C.append(c); R.append(np.median(np.linalg.norm(u[m] - c, axis=1)))
        if len(C) < 2: C = [u[A], u[B]]; R = [0.0, 0.0]
        C = np.array(C); R = np.array(R)
        r0 = float(np.median(R)) if len(R) else 1.0
    # uç halkaları: A ve B ucunda düz yüz merkezleri
    P = rdp(C, max(1.0, 0.6 * r0))
    return P, r0, R, float(Lg)


def ad_bul(base, lo, hi, e=0.6):
    best, bv = None, 1e30
    for q in PK.get(base, []):
        k = np.array(q[2:8], float)
        if (lo >= k[0::2] - e).all() and (hi <= k[1::2] + e).all():
            v = max(k[1] - k[0], .01) * max(k[3] - k[2], .01) * max(k[5] - k[4], .01)
            if v < bv: bv, best = v, q[0]
    return best


def istasyon(P, base):
    c = P.mean(0); x, y, z = c
    if base.startswith('ELK_QR') or base.startswith('QR'): return 'QR'
    if base.startswith('ROBOT'): return 'ROBOT'
    if base.startswith('TEZGAH'): return 'TEZGAH'
    if base == 'ELK_ANA_HAT' or base == 'ELK_ZEMIN_KANALI': return 'ANA_HAT'
    if base in ('ELK_DOLAP', 'B_SOGUTMA', 'B_KABLO') or y < 788: return 'B'
    if y > 1862: return 'U'
    if x < 1436: return 'A'
    if x < 2500: return 'TOPPING'
    if x < 4000: return 'F'
    if x < 4400: return 'K'
    return 'E'


KAY = []
for pid, p in enumerate(G.prims):
    mat = p['name'].split('__')[1] if '__' in p['name'] else ''
    base = p['name'].split('__')[0]
    if mat not in LIN: continue
    vis = G.gorunur(p)
    X, T = p['X'], p['T']
    Pq = np.round(X, 2); u, inv = np.unique(Pq, axis=0, return_inverse=True); inv = inv.reshape(-1)
    Ti = inv[T]
    r_ = np.concatenate([Ti[vis][:, 0], Ti[vis][:, 1]]); c_ = np.concatenate([Ti[vis][:, 1], Ti[vis][:, 2]])
    k, lab = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(u), len(u))), directed=False)
    tl = lab[Ti[:, 0]]
    for ci in np.unique(tl[vis]):
        m = (tl == ci) & vis
        vs = np.unique(Ti[m]); mp = -np.ones(len(u), int); mp[vs] = np.arange(len(vs))
        uu = u[vs]; TT = mp[Ti[m]]
        lo, hi = uu.min(0), uu.max(0)
        try:
            P, r0, R, Lg = merkez(uu, TT)
        except Exception as ex:
            print('HATA', p['name'], ci, ex); continue
        L = float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1)))
        tup = m.sum() > 12 and L > 4 * r0 and len(R) > 3 and np.percentile(R, 90) < 2.2 * np.median(R) + 1.0
        S = serit.segmentler(X[T[m]])
        S = [q for q in S if np.linalg.norm(q['b'] - q['a']) > 0.8 * q['r']]
        if not S:
            S = [dict(a=P[i], b=P[i + 1], r=r0, d=(P[i + 1] - P[i]) / max(np.linalg.norm(P[i + 1] - P[i]), 1e-9), n=0) for i in range(len(P) - 1)]
            kaynak = 'geodezik'
        else: kaynak = 'serit'
        # serbest uçlar: başka segmentin eksenine (r_i + r_j + 6) mm'den uzak segment ucu (kısa kademeler köprülenir)
        uc = []
        for i, q in enumerate(S):
            for e_, (E, F) in enumerate(((q['a'], q['b']), (q['b'], q['a']))):
                bag = False
                for j, w in enumerate(S):
                    if j == i: continue
                    dv = w['b'] - w['a']; L2 = max(dv @ dv, 1e-9); t = np.clip((E - w['a']) @ dv / L2, 0, 1)
                    if np.linalg.norm(w['a'] + t * dv - E) < q['r'] + w['r'] + 6.0: bag = True; break
                if not bag:
                    v = E - F; v = v / max(np.linalg.norm(v), 1e-9); uc.append((E, v, q['r'], i))
        KAY.append(dict(S=S, uclar=uc, kaynak=kaynak, id="%s#%d" % (p['name'], ci), pid=pid, prim=p['name'], base=base, mat=mat, comp=int(ci), ntri=int(m.sum()),
                        lo=lo, hi=hi, P=P, r=r0, L=L, tup=bool(tup), ad=ad_bul(base, lo, hi), ist=istasyon(P, base), tri_idx=np.where(m)[0]))
print(len(KAY), 'bilesen')
for d in KAY: d['Ls'] = float(sum(np.linalg.norm(q['b'] - q['a']) for q in d['S']))
pickle.dump(KAY, open(os.path.join(HERE, '_kay.pkl'), 'wb'))
for d in KAY:
    print("%-34s %-40s %-7s r%4.1f L%7.0f Ls%7.0f seg%3d uc%2d %s tup%d" % (d['id'], str(d['ad'])[:40], d['ist'], d['r'], d['L'], d['Ls'], len(d['S']), len(d['uclar']), d['kaynak'], d['tup']))
