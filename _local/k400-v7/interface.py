from pathlib import Path
import sys,os,json
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'arastirma/_uretec'))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local/k400-v7'
os.environ['AUTOKITCH_SEED_EXTRA']=str(ROOT.parent/'codex-kutu-main-v85/_local/kutu-v11/cache')
ob=R.setup()
import kesme_cad_v7 as K
import kutu_cad_v11 as E
import cadquery as cq
K.modul();E.modul()
hits={}
times=[0,4,6.6,7.8,8.4,8.5,9,9.8,10,10.5,11,11.5,12,12.5,12.8,13.2,13.6,14,14.5,15.3]
def ov(a,b):
    return min(a.xmax,b.xmax)-max(a.xmin,b.xmin)>.05 and min(a.ymax,b.ymax)-max(a.ymin,b.ymin)>.05 and min(a.zmax,b.zmax)-max(a.zmin,b.zmin)>.05
for t in times:
    w=E.blank_dunya(K.e_time(t))
    es=[]
    for p in E.PARCALAR:
        if p['grup'] in ('PIZZA','CATAL','K_ITICI','SABIT_REF') or p['ad'].startswith(('REF_','robot_')):continue
        matrix=w[p['grup']] if p['grup'].startswith('B_') else E.grup_matrisi(p['grup'],K.e_time(t))
        b=p['wp'].val().BoundingBox()
        lo=min(matrix[0][0]*x+matrix[0][1]*y+matrix[0][2]*z+matrix[0][3] for x in (b.xmin,b.xmax) for y in (b.ymin,b.ymax) for z in (b.zmin,b.zmax))
        if lo>112:continue
        s=E.uygula(p['wp'].val(),matrix).translate(cq.Vector(400,0,0))
        es.append((p['ad'],s,s.BoundingBox()))
    for p in K.PARCALAR:
        if p['grup'] in ('REF','SPREY','URUN','URUN_IZ'):continue
        s=p['wp'].translate(K.grup_trs(p['grup'],t)).val();b=s.BoundingBox()
        if b.xmax<399:continue
        for n,q,c in es:
            if ov(b,c):
                v=s.intersect(q).Volume()
                if v>.5:hits.setdefault((p['ad'],n),[]).append((t,round(v,2)))
    print(t,'interface pairs',len(hits),flush=True)
print(json.dumps([[*k,v] for k,v in hits.items()],indent=2),flush=True)
ob.ozet();sys.stdout.flush();os._exit(int(bool(hits)))
