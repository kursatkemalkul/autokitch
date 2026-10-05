import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']
K=[o for o in L if o['dug']=='TOPPING_MODUL__koyu' and o['lo'][0]>2010 and o['hi'][0]<2280 and o['hi'][1]<1400 and o['lo'][1]<1100]
for o in K:
    P=o['V'][o['F']]
    for y in (1040,1060,1080,1100,1108,1115,1150,1250,1350):
        m=(P[:,:,1].min(1)<y)&(P[:,:,1].max(1)>y)
        if not m.any(): print(y,'-'); continue
        Q=P[m].reshape(-1,3); print(y, 'x %.1f..%.1f z %.1f..%.1f n%d'%(Q[:,0].min(),Q[:,0].max(),Q[:,2].min(),Q[:,2].max(),m.sum()))
D = pickle.load(open('t3_parca.pkl','rb'))['P']
T=D['kuru_bolme_tabani']; V=T['V']
print('taban verts near kanal', len(V))
import trimesh
m=trimesh.Trimesh(V,T['F'],process=False)
for p in [(2258,1108.3,-699.7),(2140,1108.3,-700),(2050,1108.3,-700),(2265,1108.3,-686)]:
    print(p, m.contains([p])[0])
