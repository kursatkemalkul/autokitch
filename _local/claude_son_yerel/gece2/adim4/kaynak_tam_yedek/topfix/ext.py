import numpy as np, json
D=np.load('m8_onbellek.npz'); A,B,C=D['A'],D['B'],D['C']; mek=D['mek']
lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
for mk in range(9,15):
  m=mek==mk
  for (y0,y1,z0,z1,t) in [(1040,1560,-205,-135,'hortum dilimi'),(1040,1560,-640,40,'tum'),(1152,1560,-640,40,'raf ustu')]:
    s=m&(hi[:,1]>y0)&(lo[:,1]<y1)&(hi[:,2]>z0)&(lo[:,2]<z1)
    if s.any(): print(mk,t,round(lo[s,0].min(),1),round(hi[s,0].max(),1))
