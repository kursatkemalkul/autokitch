import numpy as np, re, sys
from vox import *
A,B,C,P,ad,kpk=yukle()
ex=np.array([bool(re.match(r"ELK_ZINCIR|ELK_DUVAR|ZEMIN|INSAN|E_KUTU|URUN",s)) for s in ad])[P]
A,B,C=A[~ex],B[~ex],C[~ex]
h=5.0
lo=(3995,0,-835); hi=(4405,900,85)
occ=vox(A,B,C,lo,hi,h)
np.save("occB.npy",occ)
for y0,y1 in ((5,123),(126,450),(455,745),(748,786),(792,888)):
    m=occ[:,int(y0/h):int(y1/h)].any(1)
    print("== B/K column free y",y0,y1," rows x step 15, cols z -830..80 step 20")
    for x in range(4000,4405,15):
        ix=int((x-lo[0])/h); row=""
        for z in range(-830,85,20):
            iz=int((z-lo[2])/h); row+="#" if m[max(ix-1,0):ix+2,max(iz-1,0):iz+2].any() else "."
        print("%5d %s"%(x,row))
