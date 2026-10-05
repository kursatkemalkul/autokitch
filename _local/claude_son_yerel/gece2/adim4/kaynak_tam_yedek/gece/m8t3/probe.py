# -*- coding: utf-8 -*-
import json, sys, numpy as np
Z = np.load("m8_onbellek.npz"); A, B, C, P = Z["A"], Z["B"], Z["C"], Z["P"]
J = json.load(open("m8_parca.json", encoding="utf-8")); PA = J["parca"]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
def probe(q, e=4.0):
    q = np.asarray(q, float)
    m = np.all(lo <= q + e, 1) & np.all(hi >= q - e, 1)
    ids = np.unique(P[m]); out = []
    for i in ids:
        mm = m & (P == i)
        tl, th = lo[mm].min(0), hi[mm].max(0)
        p = PA[i]; out.append((i, p["ad"], p["kpk"], np.round(p["lo"], 2), np.round(p["hi"], 2), np.round(tl, 2), np.round(th, 2)))
    return out
if __name__ == "__main__":
    pts = json.loads(sys.argv[1]); e = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    for q in pts:
        print("== q", q)
        for i, ad, kpk, plo, phi, tl, th in probe(q, e):
            print("  #%d %-34s kpk=%d  parca %s..%s  yerel %s..%s" % (i, ad, kpk, plo.tolist(), phi.tolist(), tl.tolist(), th.tolist()))
