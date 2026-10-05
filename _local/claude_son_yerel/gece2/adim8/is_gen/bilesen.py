# düğüm üçgenlerini bağlı bileşenlere ayır (konum yuvarlama ile), bbox yaz
import sys, numpy as np, glb_oku
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def bilesenler(X, T):
    P = np.round(X, 2)
    u, inv = np.unique(P, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    Ti = inv[T]
    n = len(u)
    r = np.concatenate([Ti[:,0], Ti[:,1]]); c = np.concatenate([Ti[:,1], Ti[:,2]])
    g = coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n))
    k, lab = connected_components(g, directed=False)
    tl = lab[Ti[:,0]]
    out = []
    for i in np.unique(tl):
        m = tl == i
        Q = u[np.unique(Ti[m])]
        out.append((Q.min(0), Q.max(0), int(m.sum())))
    return out
if __name__ == "__main__":
    J, D = glb_oku.yukle(sys.argv[1])
    for nd in sys.argv[2:]:
        X, T = D[nd]
        B = bilesenler(X, T)
        print("==", nd, len(B))
        for a, b, n in sorted(B, key=lambda t: (t[0][0], t[0][1], t[0][2])):
            print("  x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %d" % (a[0], b[0], a[1], b[1], a[2], b[2], n))
