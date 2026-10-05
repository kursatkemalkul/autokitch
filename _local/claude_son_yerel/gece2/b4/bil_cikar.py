# m8kit ile B düğümlerinin bileşenlerini (kapalı katı) çıkar → pkl
import os, sys, pickle, time, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
IS=os.environ.get('YAMA_IS_KOK') or os.path.abspath('is1'); os.environ['YAMA_IS_KOK']=IS
sys.path.insert(0, r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9')
import sac_ent as SE
from m8kit import Glb
gi=sys.argv[1]; out=sys.argv[2]; dug=sys.argv[3:]
t0=time.time(); g=Glb(gi); print('yük %.0f s'%(time.time()-t0))
R={}
for d in dug:
    g._bc.pop(d,None)
    try: g.bilesen(d,0)
    except Exception as e: print('yok',d,e); continue
    L=[]
    for b in g._bc[d]:
        P=np.concatenate([p['X'][p['T'][t]] for p,t in b['parca']])
        L.append(dict(no=b['no'],lo=b['lo'],hi=b['hi'],kapali=b['kapali'],P=P))
    R[d]=L; print(d,len(L),'kapalı',sum(1 for x in L if x['kapali']))
pickle.dump(R,open(out,'wb'))
