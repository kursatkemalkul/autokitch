import sys, os, pickle, numpy as np
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(H, "tg"))
from glbx import yukle
g = sys.argv[1]; k = [float(v) for v in sys.argv[2].split(',')]
J, D = yukle(g); L = pickle.load(open(os.path.join(H, "ba", "etiket_v8o.pkl"), "rb"))
for ad, d in D.items():
    X, T, ok = d['X'], d['T'], d['ok']; P = X[T]
    m = ok & (P[:,:,0].max(1) > k[0]) & (P[:,:,0].min(1) < k[1]) & (P[:,:,1].max(1) > k[2]) & (P[:,:,1].min(1) < k[3]) & (P[:,:,2].max(1) > k[4]) & (P[:,:,2].min(1) < k[5])
    if not m.any(): continue
    if ad in L and len(L[ad]) == len(T):
        for p in sorted(set(L[ad][m])):
            ti = np.where(ok & (L[ad] == p))[0]; Q = X[T[ti]].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
            print('%-30s %-44s %6d x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f' % (ad[:30], p, len(ti), mn[0], mx[0], mn[1], mx[1], mn[2], mx[2]))
    else:
        Q = P[m].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
        print('%-30s %-44s %6d x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f  (bölgedeki)' % (ad[:30], '-', m.sum(), mn[0], mx[0], mn[1], mx[1], mn[2], mx[2]))
