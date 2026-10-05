import os,sys,time,numpy as np
Y=r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9'
sys.path.insert(0,Y); sys.stdout.reconfigure(encoding='utf-8')
import sac_ent as SE
from m8kit import Glb
t=time.time(); g=Glb('../../hat3_v9k.glb'); print('yük',time.time()-t)
def near(d,lo,hi):
    g.bilesen(d,0); return [b for b in g._bc[d] if np.all(b['hi']>=lo) and np.all(b['lo']<=hi)]
for d in ['B_KASA__conta','B_KASA__pu','B_KASA__sac','B_KASA__on_cerceve','B_KASA__paslanmaz']:
    t=time.time(); L=near(d,np.array([1440,430,-800.]),np.array([1520,520,30.]))
    print(d,len(g._bc[d]),'%.0fs'%(time.time()-t))
    for b in L[:12]: print('   no',b['no'],'kapali',b['kapali'],np.round(b['lo'],2),np.round(b['hi'],2), sum(len(t) for p,t in b['parca']))
