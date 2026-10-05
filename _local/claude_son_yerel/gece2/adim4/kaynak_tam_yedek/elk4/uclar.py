import sys, pickle, numpy as np
S = r"@@KOK_W@@"
sys.path.insert(0, S + r"\elk4")
from ortam4 import Ortam, bolge
from sar import IST, D, ucler, O0
ist = sys.argv[1]; lo, hi = IST[ist]
O = bolge(O0, np.array(lo) - 100, np.array(hi) + 100)
from trimesh.triangles import closest_point
for ci, d in enumerate(D['KAY']):
    if d['ist'] != ist or not d['S']: continue
    if 'hava' in d['prim'] and len(sys.argv) < 3: continue
    E = ucler(d['S'])
    s = []
    for P in E:
        c = O.aday(P - 25, P + 25, O.yapi)
        if len(c):
            cp = closest_point(np.stack([O.A[c], O.B[c], O.C[c]], 1), np.repeat(P[None], len(c), 0)); dd = np.linalg.norm(cp - P, axis=1); i = np.argmin(dd)
            s.append("%s @%s -> %s %.1f" % ("", np.round(P).astype(int).tolist(), O.nm[c[i]], dd[i]))
        else: s.append("@%s -> -" % np.round(P).astype(int).tolist())
    print("#%d %s r%.1f L%.0f | %s" % (ci, d['prim'].split('__')[1], d['r'], d['L'], " | ".join(s)))
