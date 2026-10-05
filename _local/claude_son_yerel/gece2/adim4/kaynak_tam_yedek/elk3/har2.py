import numpy as np,sys
h=5.0
for xf in (2500,4000,4400):
    L=np.load("dep2_%d_L.npy"%xf); R=np.load("dep2_%d_R.npy"%xf)
    for nm,M in (("L",L),("R",R)):
        print("== face",xf,nm,"(depth/10mm, 9=>=90.. capped) z cols:", " ".join("%d"%z for z in range(-825,-380,30)))
        for y in range(1850,780,-30):
            iy=int(y/h); row=""
            for z in range(-825,-380,15):
                iz=int((z+830)/h); d=M[iy-2:iy+3, max(iz-1,0):iz+2].min()
                row+=str(min(9,int(d//15)))
            print("%5d %s"%(y,row))
