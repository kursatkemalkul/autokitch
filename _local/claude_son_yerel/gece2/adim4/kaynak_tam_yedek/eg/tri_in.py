import sys, numpy as np
sys.path.insert(0,"."); import govde_denetim_dogru as GD
D=GD.glb_oku(sys.argv[1])
lo=np.array([float(v) for v in sys.argv[2].split(",")]); hi=np.array([float(v) for v in sys.argv[3].split(",")])
for nd,P in D.items():
    if not len(P): continue
    c=P.mean(1); m=((c>lo)&(c<hi)).all(1)
    if m.any():
        Q=P[m].reshape(-1,3); print("%-34s %6d tri  %s %s"%(nd,m.sum(),Q.min(0).round(1).tolist(),Q.max(0).round(1).tolist()))
import os; sys.stdout.flush(); os._exit(0)
