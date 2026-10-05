# -*- coding: utf-8 -*-
"""m8 madde 5: GOVDE saclari arasinda 0,2-15 mm aralik (birbirine hic degmeyen sac cifti, en yakin uzaklik)"""
from m8_ortak import *
import m8_temas as T, json, collections
from rtree import index
SAC = ("sac", "paslanmaz", "on_seffaf", "kabuk", "qr_govde", "on_cerceve")
mal = np.array([PC[i]["ad"].split("__", 1)[1] if "__" in PC[i]["ad"] else "" for i in range(N)])
sac = np.array([pkat[i] >= 0 and KAT[pkat[i]] == "GOVDE" and mal[i].startswith(SAC) for i in range(N)])
print(sac.sum(), "sac parca")
ti = np.where(sac[T.TPc])[0]
lo = np.minimum(np.minimum(T.A[ti], T.B[ti]), T.C[ti]); hi = np.maximum(np.maximum(T.A[ti], T.B[ti]), T.C[ti])
p = index.Property(); p.dimension = 3
I = index.Index((np.arange(len(ti), dtype=np.int64), lo, hi), properties=p, interleaved=True)
temas = set(map(tuple, E.tolist()))
pts, pid = T.kenar_ornek(set(np.where(sac)[0].tolist()), adim=3.0)
V = np.concatenate([T.A[ti], T.B[ti], T.C[ti]]); Vp = np.concatenate([T.TPc[ti]] * 3)
pts = np.vstack([pts, V]); pid = np.concatenate([pid, Vp])
print(len(pts), "ornek", flush=True)
R = 15.0; best = {}
for s in range(0, len(pts), 100000):
    q = pts[s:s + 100000]; qp = pid[s:s + 100000]
    ids, cnt = I.intersection_v(q - R, q + R); ids = ids.astype(np.int64); cnt = cnt.astype(np.int64)
    qi = np.repeat(np.arange(len(q)), cnt); tg = ti[ids]; tp = T.TPc[tg]
    ok = tp != qp[qi]; qi = qi[ok]; tg = tg[ok]; tp = tp[ok]
    for s2 in range(0, len(qi), 4000000):
        a = qi[s2:s2 + 4000000]; b = tg[s2:s2 + 4000000]; c = tp[s2:s2 + 4000000]
        d = T.nokta_ucgen(q[a], T.A[b], T.B[b], T.C[b])
        k = d <= R; a = a[k]; c = c[k]; d = d[k]
        pa = qp[a]; key = np.minimum(pa, c) * N + np.maximum(pa, c)
        o = np.lexsort((d, key)); key = key[o]; d = d[o]; a = a[o]
        f = np.r_[True, key[1:] != key[:-1]]
        for kk, dd, aa in zip(key[f], d[f], a[f]):
            if kk not in best or dd < best[kk][0]: best[kk] = (float(dd), q[aa].tolist())
    print(s, len(best), flush=True)
OUT = []
for kk, (d, nok) in best.items():
    a, b = int(kk // N), int(kk % N)
    if (a, b) in temas or d < 0.2 or d > 15: continue
    if pkpk[a] or pkpk[b] or "on_seffaf" in mal[a] or "on_seffaf" in mal[b]: tur = "kapak-gövde derzi (kasıtlı)"
    elif pist[a] != pist[b]: tur = "modüller arası"
    else: tur = "aynı istasyon gövde sacı"
    if nok[2] > 40 and tur != "modüller arası": tur += " · ön yüz"
    OUT.append(dict(aralik_mm=round(d, 2), tur=tur, nokta=[round(v, 1) for v in nok], a=tanim(a), b=tanim(b)))
OUT.sort(key=lambda r: (r["tur"], r["aralik_mm"]))
json.dump(OUT, open("m8_derz.json", "w", encoding="utf-8"), ensure_ascii=False)
print(collections.Counter(r["tur"] for r in OUT))
