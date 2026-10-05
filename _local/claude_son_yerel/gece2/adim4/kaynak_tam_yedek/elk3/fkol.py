import numpy as np, re, sys
from vox import *
A,B,C,P,ad,kpk=yukle()
ex=np.array([bool(re.match(r"ELK_ZINCIR|ELK_DUVAR|ZEMIN|INSAN|E_KUTU|URUN",s)) for s in ad])[P]
A,B,C=A[~ex],B[~ex],C[~ex]
h=5.0
lo=(2495,0,-835); hi=(4005,1870,-400)
occ=vox(A,B,C,lo,hi,h)
np.save("occF.npy",occ)
for y0,y1 in ((5,120),(128,450),(455,783),(793,1312),(1352,1855)):
    m=occ[:,int(y0/h):int(y1/h)].any(1)
    print("== F/B column free y",y0,y1," rows x step 30, cols z -830..-400 step 10")
    for x in range(2500,4005,30):
        ix=int((x-lo[0])/h); row=""
        for z in range(-830,-400,10):
            iz=int((z-lo[2])/h); row+="#" if m[max(ix-1,0):ix+2,max(iz-1,0):iz+2].any() else "."
        print("%5d %s"%(x,row))
