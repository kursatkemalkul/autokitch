import sys, numpy as np
sys.path.insert(0,"."); import govde_denetim_dogru as GD
D=GD.glb_oku(sys.argv[1])
for nd,P in D.items():
    if not len(P): continue
    Q=P.reshape(-1,3)
    if Q[:,0].max()<5000 or Q[:,0].min()>5700: continue
    for b in GD.bilesenler(nd,P):
        d=b.hi-b.lo
        if d[1]>900 and d[0]<80 and d[2]<80 and b.hi[0]>5000 and b.lo[0]<5700:
            print("%-34s [%3d] lo %s hi %s"%(nd,b.no,b.lo.round(1).tolist(),b.hi.round(1).tolist()))
import os; sys.stdout.flush(); os._exit(0)
