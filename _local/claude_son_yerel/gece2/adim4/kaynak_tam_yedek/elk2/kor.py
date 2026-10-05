import sys,numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
import geo
for mal,P,mek in geo.parcalar(): EN.ekle(P)
B=Bolge(EN,(1975,880,-832),(2500,2150,-680))
D=B.D; h=2.0; lo=B.lo
# her (x,z) sutunu icin y 930..2120 boyunca min mesafe
iy0=int((930-lo[1])/h); iy1=int((2125-lo[1])/h)
col=D[:,iy0:iy1,:].min(1)
xs=lo[0]+np.arange(D.shape[0])*h; zs=lo[2]+np.arange(D.shape[2])*h
ok=np.argwhere(col>=7.5+0.5+1.5)
print('dik serbest sutun sayisi',len(ok))
for i,k in ok[::7][:60]: print(' x %.0f z %.0f d %.1f'%(xs[i],zs[k],col[i,k]))
# y=2112 satirinda x 1995..2480 boyunca z bazinda
for yy in (2112,2100,2080,2125):
  iy=int(round((yy-lo[1])/h)); row=D[int((1995-lo[0])/h):,iy,:]
  m=row.min(0); print('y',yy,'serbest z:',[ (round(zs[k]),round(m[k],1)) for k in range(len(zs)) if m[k]>=9.5][:20])
print('---')
ix0=int((1995-lo[0])/h); ix1=int((2478-lo[0])/h)
for yy in range(2040,2150,6):
  iy=int(round((yy-lo[1])/h)); m=D[ix0:ix1,iy,:].min(0)
  f=[round(zs[k]) for k in range(len(zs)) if m[k]>=9.5]
  if f: print('y',yy,'serbest z', f[:3], '...', f[-3:], len(f))
# alt: y 930 satiri x 2270..2477 ve 2315..2477
for xs0 in (2270,2315):
  for yy in (900,930,960,990):
    iy=int(round((yy-lo[1])/h)); m=D[int((xs0-lo[0])/h):ix1,iy,:].min(0)
    f=[round(zs[k]) for k in range(len(zs)) if m[k]>=9.5]; print('alt x',xs0,'y',yy,f[:4],len(f))
# x 2476 sutununda z -818 icin y araligi
k=int(round((-818-lo[2])/h)); i=int(round((2476-lo[0])/h)); c=D[i,:,k]; ys=lo[1]+np.arange(D.shape[1])*h
print('sutun 2476/-818 min', [ (round(ys[j]),round(c[j],1)) for j in range(0,len(c),25)])
