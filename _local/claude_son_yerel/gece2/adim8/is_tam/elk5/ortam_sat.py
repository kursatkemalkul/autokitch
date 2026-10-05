import numpy as np
def tri_kutu(V, lo, hi):
    """V (n,3,3) ucgenler; kutu ile SAT kesisim maskesi"""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); cen = (lo+hi)/2; h = (hi-lo)/2
    V = V - cen; n = len(V); ok = np.ones(n, bool)
    for i in range(3): ok &= ~((V[:, :, i].min(1) > h[i]) | (V[:, :, i].max(1) < -h[i]))
    E = [V[:, 1]-V[:, 0], V[:, 2]-V[:, 1], V[:, 0]-V[:, 2]]
    for i in range(3):
        a = np.eye(3)[i]
        for ed in E:
            ax = np.cross(a[None], ed); p = np.einsum('nkj,nj->nk', V, ax); r = np.abs(ax) @ h
            ok &= ~((p.min(1) > r+1e-9) | (p.max(1) < -r-1e-9))
    nn = np.cross(E[0], -E[2]); p0 = np.einsum('nj,nj->n', nn, V[:, 0]); r = np.abs(nn) @ h
    ok &= np.abs(p0) <= r+1e-9
    return ok
