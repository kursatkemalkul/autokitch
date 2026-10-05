import sys,numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
import geo
for mal,P,mek in geo.parcalar(): EN.ekle(P)
B=Bolge(EN,(1975,880,-832),(2500,2150,-600))
def free(a,b,r): return B.seg_ok(np.array(a,float),np.array(b,float),r)
r=7.5
for xs in (2270,2315):
  for zz in range(-812,-700,4):
    for yy in range(990,1260,10):
      if free((xs,935,zz),(xs,yy,zz),r) and free((xs,yy,zz),(2476,yy,zz),r) and free((2476,yy,zz),(2476,yy,-818),r) and free((2476,yy,-818),(2476,2112,-818),r):
        print('BULDU',xs,zz,yy); break
    else: continue
    break
