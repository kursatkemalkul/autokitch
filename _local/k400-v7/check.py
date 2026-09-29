from pathlib import Path
import sys,os,json,runpy
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'arastirma/_uretec'))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local/k400-v7'
os.environ['AUTOKITCH_SEED_EXTRA']=str(ROOT.parent/'codex-kutu-main-v85/_local/kutu-v11/cache')
ob=R.setup()
import kesme_cad_v7 as K
K.modul()
out={'parts':len(K.PARCALAR),'invalid':[p['ad'] for p in K.PARCALAR if not p['wp'].val().isValid()]}
moving=[p for p in K.PARCALAR if p['grup'].startswith('ITICI')]
out['moving_bounds']=[]
for t in (0,5.4,8.4,9.8,10,11,12.5,13.2,14,15.3):
    bs=[p['wp'].val().translate(__import__('cadquery').Vector(*K.grup_trs(p['grup'],t))).BoundingBox() for p in moving]
    out['moving_bounds'].append([t,min(b.xmin for b in bs),max(b.xmax for b in bs),min(b.zmin for b in bs),max(b.zmax for b in bs)])
print(json.dumps(out,indent=2),flush=True)
def ov(a,b):
    return min(a.xmax,b.xmax)-max(a.xmin,b.xmin)>.05 and min(a.ymax,b.ymax)-max(a.ymin,b.ymin)>.05 and min(a.zmax,b.zmax)-max(a.zmin,b.zmin)>.05
hits={}
for t in (i/10 for i in range(154)):
    ps=[(p,p['wp'].translate(K.grup_trs(p['grup'],t)).val()) for p in K.PARCALAR if p['grup'] not in ('REF','SPREY','URUN','URUN_IZ')]
    for i,(p,a) in enumerate(ps):
        for q,b in ps[i+1:]:
            if p['grup']==q['grup']:continue
            if not ov(a.BoundingBox(),b.BoundingBox()):continue
            v=a.intersect(b).Volume()
            if v>.5:hits.setdefault((p['ad'],q['ad']),[]).append((t,round(v,2)))
print('INTERSECTIONS',json.dumps([[*k,v] for k,v in hits.items()]),flush=True)
assert not hits,hits
assert not out['invalid']
ob.ozet();sys.stdout.flush();os._exit(0)
