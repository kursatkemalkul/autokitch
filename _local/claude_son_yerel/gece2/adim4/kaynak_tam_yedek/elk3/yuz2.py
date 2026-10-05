import sys, numpy as np, re
from vox import *
A, B, C, P, ad, kpk = yukle()
ex = np.array([bool(re.match(r"ELK_ZINCIR|ELK_DUVAR|ZEMIN|INSAN", s)) for s in ad])
for i in (706, 707,708,711, 3283, 3290): ex[i] = True
ex = ex[P]
A, B, C = A[~ex], B[~ex], C[~ex]
h = 5.0
for xf in (2500.0, 4000.0, 4400.0):
    lo = (xf - 300, 0, -830); hi = (xf + 300, 2200, 80)
    occ = vox(A, B, C, lo, hi, h)
    i0 = int(round(300 / h))
    np.save("occ_%d.npy"%xf, occ)
    for side, sg in (("L", -1), ("R", 1)):
        col = occ[i0::sg] if sg > 0 else occ[i0::-1]
        c2 = col[2:]
        first = np.where(c2.any(0), c2.argmax(0), c2.shape[0]) * h + 10
        np.save("dep2_%d_%s.npy" % (xf, side), first)
