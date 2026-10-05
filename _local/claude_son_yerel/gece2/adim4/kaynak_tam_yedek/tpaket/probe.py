import numpy as np, json, sys
from collections import Counter
D=np.load('ze/m8_onbellek.npz'); P=D['P']; T=np.stack([D['A'],D['B'],D['C']],1)
J=json.load(open('ze/m8_parca.json',encoding='utf-8'))['parca']; AD=np.array([p['ad'] for p in J])
lo=T.min(1); hi=T.max(1)
for nm,K in (('L',(1497,1640,1325,1645)),('R',(1790,2190,1420,1800)),('S1',(1700,1745,1152,1200)),('S2',(2240,2280,1152,1200))):
    m=(hi[:,0]>K[0])&(lo[:,0]<K[1])&(hi[:,1]>K[2])&(lo[:,1]<K[3])&(hi[:,2]>-631)&(lo[:,2]<-569)
    flat=m&(hi[:,2]-lo[:,2]<0.01)
    c=Counter((AD[P[i]],round(float(lo[i,2]),2)) for i in np.where(flat)[0])
    ins=m&(lo[:,0]>=K[0])&(hi[:,0]<=K[1])&(lo[:,1]>=K[2])&(hi[:,1]<=K[3])&(lo[:,2]>=-630.05)&(hi[:,2]<=-569.95)
    c2=Counter(AD[P[i]] for i in np.where(ins)[0])
    print(nm,'flat planes',sorted(c.items())); print('   fully inside',c2)
    nf=m&~ins; c3=Counter((AD[P[i]],J[P[i]]['mek']) for i in np.where(nf)[0]); print('   crossing',c3)
