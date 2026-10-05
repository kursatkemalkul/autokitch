# free depth maps at junction faces
import sys, numpy as np, re
from vox import *
A, B, C, P, ad, kpk = yukle()
nm = ad[P]
ex = np.array([bool(re.match(r"ELK_ZINCIR|ELK_DUVAR|ZEMIN|INSAN", s)) for s in ad])[P]
A, B, C = A[~ex], B[~ex], C[~ex]
h = 5.0
for xf in (2500.0, 4000.0, 4400.0):
    lo = (xf - 300, 0, -830); hi = (xf + 300, 2200, 80)
    occ = vox(A, B, C, lo, hi, h)
    i0 = int(round(300 / h))
    for side, sg in (("L", -1), ("R", 1)):
        # depth from face skipping first 'skip' voxels (wall sheet)
        dep = np.full(occ.shape[1:], 0.0)
        # wall thickness: skip voxels occupied contiguous from face
        for yz in [None]:
            pass
        col = occ[i0::sg] if sg > 0 else occ[i0::-1]
        # skip the first 2 voxels (10 mm) as wall
        c2 = col[2:]
        first = np.where(c2.any(0), c2.argmax(0), c2.shape[0]) * h + 10
        np.save("dep_%d_%s.npy" % (xf, side), first)
    print("face", xf, "done", flush=True)
