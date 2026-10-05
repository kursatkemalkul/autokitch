import os, sys, numpy as np
sys.path.insert(0, r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9')
sys.path.insert(0, r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9\veri')
import sac_ent as SE
from m8kit import Glb
import bag47 as B
g=Glb('hat3_v9p.glb')
def bc(d):
    g._bc.pop(d,None); g.bilesen(d,0); return g._bc[d]
L=bc('B_KASA__sac'); T=[b for b in L if np.all(np.abs(b['lo']-[797.3,163.3,-791.2])<0.3)]; print('TAB1', len(T), T[0]['kapali'], [ (p['name'],len(t)) for p,t in T[0]['parca']])
K=SE.Karsi(g, haric_onek=("B_KASA__pu",), acik_dene=True)
el=B.kor_percin((1430,0,-500),(0,-1,0),-165.7,5.4,'test',d=4,dk=8,k=1.3,bulb=6)
print(K.delik_ac([el]))
L=bc('B_KASA__sac'); print('sonra', len([b for b in L if np.all(np.abs(b['lo']-[797.3,163.3,-791.2])<0.3)]), [ (np.round(b['lo'],1).tolist(),np.round(b['hi'],1).tolist()) for b in L if b['lo'][0]<800 and b['lo'][1]<170])
p=[q for q in g.dprims('B_KASA__sac')][0]
print('prim tri', len(p['T']), 'X', p['X'].shape, p['X'].dtype)
P=p['X'][p['T']]; ar=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1)
c=P.mean(1); k=(c[:,0]>797)&(c[:,0]<2109)&(c[:,1]>163)&(c[:,1]<165)&(ar>1e-9)
print('TAB1 bölgesi üçgen', k.sum())
import govde_denetim_dogru as G
bb=G.bilesenler('x', P[k])
print([(round(b.lo[0],1),round(b.lo[1],1),round(b.hi[0],1),round(b.hi[1],1),b.kapali, len(b.P)) for b in bb][:10])
