# -*- coding: utf-8 -*-
"""Bir düğüm/parçanın belirli düzlemdeki yüzünü 1 mm ızgarada rasterle → delikler (boş bileşen dikdörtgenleri).
python delik.py glb seg node parca eksen deger [u0,u1,v0,v1]"""
import sys, pickle, numpy as np
from scipy import ndimage
sys.path.insert(0,'.')
from glbx import yukle
g, sg, nd, pa, ek, dg = sys.argv[1:7]; dg=float(dg); ax=' xyz'.index(ek)-1
J,D=yukle(g); R=pickle.load(open(sg,'rb'))
d=D[nd]; X,T,ok=d['X'],d['T'],d['ok']; L=R.get(nd)
m=ok.copy()
if pa!='-': m&=np.isin(L, pa.split('+'))
P=X[T[m]]
on=(np.abs(P[...,ax]-dg)<0.05).all(1)
P=P[on]
u,v={0:(2,1),1:(0,2),2:(0,1)}[ax]
if len(sys.argv)>7: u0,u1,v0,v1=[float(s) for s in sys.argv[7].split(',')]
else: u0,u1,v0,v1=P[...,u].min(),P[...,u].max(),P[...,v].min(),P[...,v].max()
R_=0.5
nu=int((u1-u0)/R_)+1; nv=int((v1-v0)/R_)+1
G=np.zeros((nv,nu),bool)
uc=u0+(np.arange(nu)+0.5)*R_; vc=v0+(np.arange(nv)+0.5)*R_
for t in P:
    a,b,c=t[:,[u,v]]
    i0=max(int((min(a[0],b[0],c[0])-u0)/R_)-1,0); i1=min(int((max(a[0],b[0],c[0])-u0)/R_)+1,nu-1)
    j0=max(int((min(a[1],b[1],c[1])-v0)/R_)-1,0); j1=min(int((max(a[1],b[1],c[1])-v0)/R_)+1,nv-1)
    Xg,Yg=np.meshgrid(uc[i0:i1+1],vc[j0:j1+1])
    den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-12: continue
    l1=((b[1]-c[1])*(Xg-c[0])+(c[0]-b[0])*(Yg-c[1]))/den; l2=((c[1]-a[1])*(Xg-c[0])+(a[0]-c[0])*(Yg-c[1]))/den; l3=1-l1-l2
    G[j0:j1+1,i0:i1+1]|=(l1>=-1e-3)&(l2>=-1e-3)&(l3>=-1e-3)
lab,n=ndimage.label(~G)
print('yuz %s=%.2f  u(%s) %.1f-%.1f  v(%s) %.1f-%.1f  dolu %.0f%%'%(ek,dg,'xyz'[u],u0,u1,'xyz'[v],v0,v1,100*G.mean()))
for i,sl in enumerate(ndimage.find_objects(lab)):
    js,is_=sl
    a0=u0+is_.start*R_; a1=u0+is_.stop*R_; b0=v0+js.start*R_; b1=v0+js.stop*R_
    alan=(lab[sl]==i+1).sum()*R_*R_; dol=alan/((a1-a0)*(b1-b0))
    print('  bos %s %7.1f-%7.1f  %s %7.1f-%7.1f  alan %8.0f  dolgunluk %.2f'%('xyz'[u],a0,a1,'xyz'[v],b0,b1,alan,dol))
