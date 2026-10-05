import sys, numpy as np, glb_oku
J,D=glb_oku.yukle(sys.argv[1])
nd=sys.argv[2]; x0,x1=float(sys.argv[3]),float(sys.argv[4])
X,T=D[nd]; P=X[T]; m=(P[:,:,0].min(1)>=x0-0.01)&(P[:,:,0].max(1)<=x1+0.01)
Q=P[m]
print('tri',m.sum())
print('y',np.unique(np.round(Q[:,:,1],1)))
print('z',np.unique(np.round(Q[:,:,2],1)))
# yz alanı ızgara: hangi hücreler dolu (x=x0 yüzündeki)
ys=np.unique(np.round(Q[:,:,1],1)); zs=np.unique(np.round(Q[:,:,2],1))
F=Q[(np.ptp(Q[:,:,0],axis=1)<0.01)]
for i in range(len(ys)-1):
  row=''
  for j in range(len(zs)-1):
    c=np.array([(zs[j]+zs[j+1])/2,(ys[i]+ys[i+1])/2])
    hit=False
    for t in F:
      a,b,cc=t[:,[2,1]]
      v0=cc-a;v1=b-a;v2=c-a
      d00=v0@v0;d01=v0@v1;d11=v1@v1;d20=v2@v0;d21=v2@v1;den=d00*d11-d01*d01
      if abs(den)<1e-9: continue
      u=(d11*d20-d01*d21)/den; v=(d00*d21-d01*d20)/den
      if u>=-1e-6 and v>=-1e-6 and u+v<=1+1e-6: hit=True;break
    row+='#' if hit else '.'
  print('%7.1f-%7.1f %s'%(ys[i],ys[i+1],row))
