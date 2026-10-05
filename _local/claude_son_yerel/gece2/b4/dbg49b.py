import os, sys, numpy as np
sys.path.insert(0, r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9')
import sac_ent as SE
from m8kit import Glb
g=Glb('hat3_v9p.glb')
def bc(d):
    g._bc.pop(d,None); g.bilesen(d,0); return g._bc[d]
L=bc('B_KASA__sac'); T=[b for b in L if np.all(np.abs(b['lo']-[797.3,163.3,-791.2])<0.3)][0]
p=g.dprims('B_KASA__sac')[0]; n0=len(p['T'])
labs=set(g._etiketler(pp,int(t)) for pp,tri in T['parca'] for t in tri); print('etiket grupları', labs)
P=np.concatenate([pp['X'][pp['T'][t]] for pp,t in T['parca']])
m=SE.mf_ucgen(P); print('mf', m is not None, m.volume() if m else None)
Pn=SE.mf_P(m); print('Pn', Pn.shape)
ilk=[True]
def f(_):
    if ilk[0]: ilk[0]=False; return Pn
    return None
r=g.donustur(T,f); print('donustur dönüş', r, 'tri', n0, '→', len(g.dprims('B_KASA__sac')[0]['T']))
L=bc('B_KASA__sac'); print('var mı', len([b for b in L if np.all(np.abs(b['lo']-[797.3,163.3,-791.2])<0.3)]))
p=g.dprims('B_KASA__sac')[0]
Q=p['X'][p['T'][-92:]]; print('son 92 kutu', Q.reshape(-1,3).min(0), Q.reshape(-1,3).max(0), p.get('donuk'), p['t'])
print(len(g.dprims('B_KASA__sac')))
P=p['X'][p['T']]; c=P.mean(1)
for lo,hi in [((0.7,0.1,-1),(2.2,0.2,0.1)), ((797,163,-792),(2109,165,24))]:
    k=np.all((c>lo)&(c<hi),1); print(lo, k.sum())
ar=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1); print('dejenere', (ar<1e-9).sum())
k=np.all((c>[797,163,-792])&(c<[2109,165,24]),1); print(np.where(k)[0][:20], ar[k][:20])
