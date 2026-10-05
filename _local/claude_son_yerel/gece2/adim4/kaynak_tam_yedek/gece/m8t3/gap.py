# -*- coding: utf-8 -*-
"""gap.py: aday nokta q cevresinde iki parca adi (dugum adi) arasindaki en yakin nokta cifti, ucgen normalleri, araya giren ucuncu parcalar"""
import json, sys, numpy as np
Z = np.load("m8_onbellek.npz"); A, B, C, P = Z["A"], Z["B"], Z["C"], Z["P"]
J = json.load(open("m8_parca.json", encoding="utf-8")); PA = J["parca"]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
AD = np.array([p["ad"] for p in PA])
def pt_tri(p, a, b, c):
    # Ericson closest point on triangle, vectorized over triangles
    ab = b - a; ac = c - a; ap = p - a
    d1 = (ab * ap).sum(1); d2 = (ac * ap).sum(1)
    bp = p - b; d3 = (ab * bp).sum(1); d4 = (ac * bp).sum(1)
    cp = p - c; d5 = (ab * cp).sum(1); d6 = (ac * cp).sum(1)
    va = d3 * d6 - d5 * d4; vb = d5 * d2 - d1 * d6; vc = d1 * d4 - d3 * d2
    den = np.where(np.abs(va + vb + vc) < 1e-18, 1e-18, va + vb + vc)
    v = vb / den; w = vc / den
    res = a + ab * v[:, None] + ac * w[:, None]
    m = (d1 <= 0) & (d2 <= 0); res[m] = a[m]
    m = (d3 >= 0) & (d4 <= d3); res[m] = b[m]
    m = (d6 >= 0) & (d5 <= d6); res[m] = c[m]
    m = (vc <= 0) & (d1 >= 0) & (d3 <= 0); t = d1 / np.where(d1 - d3 == 0, 1, d1 - d3); res[m] = (a + ab * t[:, None])[m]
    m = (vb <= 0) & (d2 >= 0) & (d6 <= 0); t = d2 / np.where(d2 - d6 == 0, 1, d2 - d6); res[m] = (a + ac * t[:, None])[m]
    m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); t = (d4 - d3) / np.where((d4 - d3) + (d5 - d6) == 0, 1, (d4 - d3) + (d5 - d6)); res[m] = (b + (c - b) * t[:, None])[m]
    return res
def yakin(q, e=6.0):
    return np.where(np.all(lo <= q + e, 1) & np.all(hi >= q - e, 1))[0]
def en_yakin(ia, ib):
    best = (1e9, None, None, None, None)
    for X, Y in ((ia, ib), (ib, ia)):
        V = np.unique(np.concatenate([A[X], B[X], C[X]]), axis=0)
        # edge sample points too
        E = np.concatenate([(A[X] + B[X]) / 2, (B[X] + C[X]) / 2, (A[X] + C[X]) / 2])
        V = np.vstack([V, E])
        for v in V:
            r = pt_tri(v[None, :].repeat(len(Y), 0), A[Y], B[Y], C[Y]); d = np.linalg.norm(r - v, axis=1); k = d.argmin()
            if d[k] < best[0]: best = (d[k], v, r[k], X is ia, Y[k])
    return best
def nrm(t):
    n = np.cross(B[t] - A[t], C[t] - A[t]); return n / (np.linalg.norm(n) + 1e-12)
def analiz(q, a, b, e=6.0):
    q = np.asarray(q, float); I = yakin(q, e)
    ia = I[AD[P[I]] == a]; ib = I[AD[P[I]] == b]
    out = []
    # parcaya gore ayir: her (pa,pb) parca cifti
    pas = np.unique(P[ia]); pbs = np.unique(P[ib])
    for pa in pas:
        for pb in pbs:
            if pa == pb: continue
            d, v, r, a_side, tk = en_yakin(ia[P[ia] == pa], ib[P[ib] == pb])
            pv, pr = (v, r) if a_side else (r, v)
            out.append((d, pa, pb, pv, pr))
    out.sort(key=lambda x: x[0])
    return out[:3]
def araya(p1, p2, haric, pad=0.05):
    l = np.minimum(p1, p2) - 0.3; h = np.maximum(p1, p2) + 0.3
    # sikistir gap ekseninde
    m = np.all(lo <= h, 1) & np.all(hi >= l, 1)
    ids = set(np.unique(P[m]).tolist()) - set(haric)
    return [(i, PA[i]["ad"]) for i in ids]
if __name__ == "__main__":
    for job in json.loads(open(sys.argv[1], encoding="utf-8").read()):
        q, a, b = job
        print("=== ", a, "<->", b, q)
        for d, pa, pb, v, r in analiz(q, a, b):
            print("  d=%.3f  #%d %s..%s  |  #%d %s..%s" % (d, pa, np.round(PA[pa]["lo"], 1).tolist(), np.round(PA[pa]["hi"], 1).tolist(), pb, np.round(PA[pb]["lo"], 1).tolist(), np.round(PA[pb]["hi"], 1).tolist()))
            print("     pa_nokta %s  pb_nokta %s  fark %s" % (np.round(v, 2).tolist(), np.round(r, 2).tolist(), np.round(r - v, 2).tolist()))
            print("     araya:", araya(v, r, [pa, pb])[:8])
