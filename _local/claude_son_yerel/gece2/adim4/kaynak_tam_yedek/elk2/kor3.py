import numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
import geo
for mal,P,mek in geo.parcalar(): EN.ekle(P)
B=Bolge(EN,(1975,880,-832),(2500,2150,-600))
D=B.D; lo=B.lo; h=2
xs=lo[0]+np.arange(D.shape[0])*h; ys=lo[1]+np.arange(D.shape[1])*h; zs=lo[2]+np.arange(D.shape[2])*h
for r in (7.5,4.35):
  need=r+0.5+1.5
  iy0=int((935-lo[1])/h)
  # her sutun icin y935'ten yukari kesintisiz serbest yukseklik
  ok=D[:,iy0:,:]>=need
  # kumulatif: ilk engel
  first=np.where(ok.all(1), D.shape[1]-iy0, np.argmin(ok,axis=1))
  ymax=lo[1]+(iy0+first)*h
  i,k=np.unravel_index(np.argsort(-ymax,axis=None)[:15],ymax.shape)
  print('r',r,[(round(xs[a]),round(zs[b]),round(ymax[a,b])) for a,b in zip(i,k)])
  # x 2260..2330 araliginda
  sub=[(round(xs[a]),round(zs[b]),round(ymax[a,b])) for a in range(len(xs)) for b in range(len(zs)) if 2255<=xs[a]<=2330 and ymax[a,b]>1100]
  print('  2255-2330:',sorted(sub,key=lambda t:-t[2])[:10])
