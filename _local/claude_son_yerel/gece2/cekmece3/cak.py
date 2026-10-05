# B çekmece bölgesi çakışma denetimi: her çekmecenin mekanizma bölgelerinde kapalı bileşen çiftleri (manifold kesişim hacmi)
import os,sys,json,numpy as np,time
sys.path.insert(0,r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9')
sys.stdout.reconfigure(encoding='utf-8')
import sac_ent as SE
from m8kit import Glb
yol=sys.argv[1]; out=sys.argv[2]
g=Glb(yol)
NODES=sorted(set(p['name'] for p in g.prims if p['name'].startswith(('CEK_','B_KASA','B_MODULER','B_SOGUTMA','B_KABLO','ELK_IC','ELK_DOLAP'))))
t=time.time()
ALL=[]
for d in NODES:
    try: g.bilesen(d,0)
    except Exception as e: continue
    for b in g._bc[d]:
        ALL.append((d,b))
print('bileşen',len(ALL),'%.0fs'%(time.time()-t))
CK=sorted(set(n.split('__')[0] for n in NODES if n.startswith('CEK_')))
bolge=[]
for ck in CK:
    rl=sorted([b for d,b in ALL if d==ck+'__celik' and np.all(np.abs((b['hi']-b['lo'])-[8.5,45.7,700])<0.1)],key=lambda b:b['lo'][0])
    R,Rr=rl[0]['lo'],rl[1]['lo']
    bolge.append((ck,np.array([R[0]-12,R[1]-25,-800]),np.array([R[0]+75,R[1]+100,30])))
    bolge.append((ck,np.array([Rr[0]-40,Rr[1]-25,-800]),np.array([Rr[0]+20,Rr[1]+100,30])))
MF={}
def mfk(i):
    if i not in MF:
        d,b=ALL[i]; P=np.concatenate([p['X'][p['T'][t]] for p,t in b['parca']]); MF[i]=SE.mf_ucgen(P) if b['kapali'] else None
    return MF[i]
SON=set()
for ck,lo,hi in bolge:
    I=[i for i,(d,b) in enumerate(ALL) if np.all(b['hi']>=lo) and np.all(b['lo']<=hi) and np.max(b['hi']-b['lo'])<1500]
    for a in range(len(I)):
        for c in range(a+1,len(I)):
            i,j=I[a],I[c]; bi,bj=ALL[i][1],ALL[j][1]
            if not (np.all(bi['hi']>bj['lo']+0.01) and np.all(bj['hi']>bi['lo']+0.01)): continue
            mi,mj=mfk(i),mfk(j)
            if mi is None or mj is None: continue
            v=(mi^mj).volume()
            if v>0.05:
                SON.add((ALL[i][0],tuple(np.round(bi['lo'],1)),ALL[j][0],tuple(np.round(bj['lo'],1)),round(v,2)))
L=sorted(SON)
json.dump([list(map(lambda x: list(x) if isinstance(x,tuple) else x,r)) for r in L],open(out,'w',encoding='utf-8'),ensure_ascii=False)
print('çakışma',len(L),'%.0fs'%(time.time()-t))
