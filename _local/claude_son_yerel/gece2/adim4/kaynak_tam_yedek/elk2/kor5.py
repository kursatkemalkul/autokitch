import numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
B=Bolge(EN,(1975,880,-832),(2500,2150,-560))
def chk(Q,r):
    Q=[np.array(q,float) for q in Q]; return [ (round(float(B.mesafe(np.array([a+(b-a)*t for t in np.linspace(0,1,max(2,int(np.linalg.norm(b-a))+1))])).min()),1)) for a,b in zip(Q[:-1],Q[1:])]
for x0 in (2270,2315):
  for zc in (-660,-650,-645):
    for yt,zt in ((2120,-689),(2090,-689)):
      Q=[(x0,920,-812),(x0,935,-812),(x0,935,zc),(2431,935,zc),(2431,yt,zc),(2431,yt,zt),(1980,yt,zt)]
      print(x0,zc,yt,chk(Q,7.5))
import json; PJ=json.load(open('e1c/m8_parca.json',encoding='utf-8'))
for z in range(-812,-640,8):
    p=np.array((2270,935,z),float); d=B.mesafe(p[None])[0]
    if d<10:
        dd,i=EN.seg_mesafe(p,p+0.01,15); q=PJ['parca'][EN.P[i]]; print(z,d,q['ad'],q['lo'],q['hi'])
# serbest y seviyeleri: x 2270 dik cizgi y 920->1300 z -812 ; ve her y'de z yonu
for y in range(930,1300,20):
    zz=[z for z in range(-812,-560,4) if B.mesafe(np.array([(2270,y,z)],float))[0]>=9.5]
    print(y, zz[:3], zz[-3:], len(zz))
