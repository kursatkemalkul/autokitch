import numpy as np, re, sys
from vox import *
A,B,C,P,ad,kpk=yukle()
ex=np.array([bool(re.match(r"ELK_ZINCIR|ELK_DUVAR|ZEMIN|INSAN|E_KUTU|URUN",s)) for s in ad])[P]
A,B,C=A[~ex],B[~ex],C[~ex]
h=5.0
lo=(4395,0,-835); hi=(5235,1900,85)
occ=vox(A,B,C,lo,hi,h)
np.save("occE.npy",occ)
for y0,y1 in ((130,1460),(130,600),(600,1000),(1000,1460)):
    m=occ[:,int(y0/h):int(y1/h)].any(1)   # (x,z)
    print("== E column free y",y0,y1," rows x 4400..5230 step 20, cols z -830..80 step 20  ('.' free)")
    for x in range(4400,5240,20):
        ix=int((x-lo[0])/h); row=""
        for z in range(-830,85,20):
            iz=int((z-lo[2])/h); row+="#" if m[max(ix-1,0):ix+2,max(iz-1,0):iz+2].any() else "."
        print("%5d %s"%(x,row))
