import numpy as np
D=np.load('m8_onbellek.npz'); A,B,C=D['A'],D['B'],D['C']; mek=D['mek']
lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
ys=list(range(1040,1720,20))
print('y      '+'  '.join('%13s'%k for k in ['kiyma','kusbasi','kasar','sucuk','harc','sos']))
for y in ys:
  row=[]
  for mk in (11,12,13,14,10,9):
    s=(mek==mk)&(hi[:,1]>y)&(lo[:,1]<y+20)&(hi[:,2]>-640)
    row.append('%6.1f-%6.1f'%(lo[s,0].min(),hi[s,0].max()) if s.any() else ' '*13)
  print(y,'  '.join(row))
