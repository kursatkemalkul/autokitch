"""Conservative transformed-AABB broad phase, exact solid intersections.
Checks only the last changed head; all other tools retained the 143-state pass.
"""
from pathlib import Path
import sys,runpy,os,json,itertools,traceback
ROOT=Path(__file__).resolve().parents[2];U=ROOT/'arastirma'/'_uretec'
sys.path.insert(0,str(U))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local'/'kutu-v10'/'validation-head'
ob=R.setup()
import kutu_cad_v10 as K
import cadquery as cq
K.modul()
P={p['ad']:p for p in K.PARCALAR if p['grup'] not in ('PIZZA','CATAL','K_ITICI','SABIT_REF')}
S={n:p['wp'].val() for n,p in P.items()}
assert S['piston_kafasi'].isValid() and len(S['piston_kafasi'].Solids())==1
assert all(s.isValid() for s in S.values())
corners={}
for n,s in S.items():
    b=s.BoundingBox()
    corners[n]=list(itertools.product((b.xmin,b.xmax),(b.ymin,b.ymax),(b.zmin,b.zmax)))
def bounds(n,M):
    v=[tuple(sum(M[i][j]*p[j] for j in range(3))+M[i][3] for i in range(3)) for p in corners[n]]
    return tuple([min(p[i] for p in v),max(p[i] for p in v)] for i in range(3))
def overlap(a,b):return all(min(a[i][1],b[i][1])-max(a[i][0],b[i][0])>1e-5 for i in range(3))
hits=[];tested=0
times=sorted(set([i/20 for i in range(461)]+[7.75,7.8,7.85]))
for t in times:
    W=K.blank_dunya(t)
    M={g:(W[g] if g.startswith('B_') else K.grup_matrisi(g,t)) for g in set(p['grup'] for p in P.values())}
    boxes={n:bounds(n,M[p['grup']]) for n,p in P.items()}
    n='piston_kafasi';a=None
    for m,p in P.items():
        if m==n or p['grup']==P[n]['grup'] or not overlap(boxes[n],boxes[m]):continue
        if a is None:a=K.uygula(S[n],M[P[n]['grup']])
        b=K.uygula(S[m],M[p['grup']]);vol=a.intersect(b).Volume();tested+=1
        if vol>.5:hits.append([t,m,vol])
    if round(t*20)%40==0:print('HEAD',t,'hits',len(hits),flush=True)
result=dict(poses=len(times),interval=.05,exact_pairs=tested,hits=hits,head_solids=1,valid=True)
(ROOT/'_local/kutu-v10/head-final.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(result,flush=True)
ob.ozet();sys.stdout.flush();os._exit(1 if hits else 0)
