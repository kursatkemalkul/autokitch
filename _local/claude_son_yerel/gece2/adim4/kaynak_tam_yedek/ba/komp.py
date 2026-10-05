# bölgedeki bağlı bileşenler (düğüm bazında) - bbox
import sys, os, numpy as np
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(H, "tg"))
from glbx import yukle
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
g = sys.argv[1]; k = [float(v) for v in sys.argv[2].split(',')]; filt = sys.argv[3] if len(sys.argv) > 3 else ""
J, D = yukle(g)
for ad, d in D.items():
    if filt and filt not in ad: continue
    X, T, ok = d['X'], d['T'], d['ok']; P = X[T]
    m = ok & (P[:,:,0].max(1) > k[0]) & (P[:,:,0].min(1) < k[1]) & (P[:,:,1].max(1) > k[2]) & (P[:,:,1].min(1) < k[3]) & (P[:,:,2].max(1) > k[4]) & (P[:,:,2].min(1) < k[5])
    if not m.any(): continue
    _, inv = np.unique(np.round(X / 0.02).astype(np.int64), axis=0, return_inverse=True); inv = inv.ravel()
    TT = inv[T]; idx = np.where(ok)[0]; nv = inv.max() + 1
    gg = coo_matrix((np.ones(2 * len(idx)), (np.concatenate([TT[idx, 0], TT[idx, 1]]), np.concatenate([TT[idx, 1], TT[idx, 2]]))), shape=(nv, nv))
    _, lab = connected_components(gg, directed=False)
    tl = np.full(len(T), -1); tl[idx] = lab[TT[idx, 0]]
    for c in np.unique(tl[m]):
        Q = X[T[tl == c]].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
        print('%-32s c%-6d %5d x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f' % (ad[:32], c, (tl == c).sum(), mn[0], mx[0], mn[1], mx[1], mn[2], mx[2]))
