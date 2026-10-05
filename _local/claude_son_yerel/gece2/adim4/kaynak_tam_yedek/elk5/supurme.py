# -*- coding: utf-8 -*-
"""hareketli dugum supurmesi (bolgesel): tum animasyonlarin anahtar karelerinde dugum ucgenleri tasinir; kutu kesisimi SAT.
S=Supurme(glb, cache, lo, hi); S.kesis(lo,hi) -> [(dugum, kare isabet, kare)]"""
import json, struct, numpy as np, re
from ortam_sat import tri_kutu
def _q2R(q):
    x, y, z, w = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def _TRS(t, r):
    M = np.eye(4); M[:3, :3] = _q2R(r); M[:3, 3] = t; return M
class Supurme:
    def __init__(s, glb, cache, lo, hi, pay=600):
        raw = open(glb, 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]; J = json.loads(raw[20:20+jl]); BIN = raw[28+jl:]
        def acc(i):
            a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; n = {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4}[a['type']]
            off = v.get('byteOffset', 0)+a.get('byteOffset', 0); return np.frombuffer(BIN[off:off+a['count']*n*4], np.float32).reshape(-1, n)
        D = np.load(cache + "/m8_onbellek.npz"); PJ = json.load(open(cache + "/m8_parca.json", encoding="utf-8"))
        ad = np.array([p["ad"] for p in PJ["parca"]])
        A, B, C, P = D["A"], D["B"], D["C"], D["P"]
        lo = np.asarray(lo, float) - pay; hi = np.asarray(hi, float) + pay
        L = np.minimum(np.minimum(A, B), C); H = np.maximum(np.maximum(A, B), C)
        rm = np.all(H >= lo, 1) & np.all(L <= hi, 1)
        idx = np.where(rm)[0]; nm = ad[P[idx]]
        ch = {}
        for an in J['animations']:
            g = {}
            for c in an['channels']:
                sm = an['samplers'][c['sampler']]
                g.setdefault(c['target']['node'], {})[c['target']['path']] = (acc(sm['input'])[:, 0], acc(sm['output']))
            for nd, d in g.items(): ch.setdefault(nd, []).append(d)
        s.N = []
        for nd, grp in ch.items():
            name = J['nodes'][nd]['name']; m = nm == name
            if not m.any(): continue
            ii = idx[m]; Q = np.stack([A[ii], B[ii], C[ii]], 1)
            t0 = np.array(J['nodes'][nd].get('translation', [0, 0, 0]), float); r0 = J['nodes'][nd].get('rotation', [0, 0, 0, 1])
            M0i = np.linalg.inv(_TRS(t0, r0)); U = {}
            for g in grp:
                ts = sorted(set(np.concatenate([v[0] for v in g.values()]).tolist()))
                for tq in ts:
                    tt = t0; rr = r0
                    if 'translation' in g:
                        t, o = g['translation']; tt = np.array([np.interp(tq, t, o[:, k]) for k in range(3)])
                    if 'rotation' in g:
                        t, o = g['rotation']; i = int(np.clip(np.searchsorted(t, tq), 0, len(t)-1)); rr = o[i] / np.linalg.norm(o[i])
                    M = _TRS(tt, rr) @ M0i; U[tuple(np.round(M[:3], 4).ravel())] = M
            s.N.append(dict(ad=name, P=Q, M=list(U.values())))
    def kesis(s, lo, hi, e=0.05, haric=None):
        out = []
        lo = np.asarray(lo, float)+e; hi = np.asarray(hi, float)-e
        for n in s.N:
            if haric and re.search(haric, n['ad']): continue
            k = 0
            for M in n['M']:
                Q = ((n['P']/1000.0) @ M[:3, :3].T + M[:3, 3])*1000.0
                c = np.all(Q.max(1) >= lo, 1) & np.all(Q.min(1) <= hi, 1)
                if c.any() and tri_kutu(Q[c], lo, hi).any(): k += 1
            if k: out.append((n['ad'], k, len(n['M'])))
        return out
    def seg(s, segs, haric=None):
        """kablo parcalari [(a,b,r)] -> eksen hizali kutu yaklasimi (yalniz dik parcalar)"""
        out = []
        for a, b, r in segs:
            a = np.asarray(a, float); b = np.asarray(b, float)
            h = s.kesis(np.minimum(a, b)-r*0.7, np.maximum(a, b)+r*0.7, e=0, haric=haric)
            if h: out.append((np.round(a).tolist(), np.round(b).tolist(), h))
        return out
