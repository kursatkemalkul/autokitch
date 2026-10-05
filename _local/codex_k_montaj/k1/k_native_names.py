from pathlib import Path
import sys,json,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
U=ROOT/'arastirma/_uretec';H=U/'h3'
N=ROOT/'_local/claude_son_yerel/gece2/adim4/b9/arastirma/_uretec'
for p in (N,U,H):sys.path.insert(0,str(p))
import h3_kesme_v1 as KS
import topping_cad_v22 as TC
TC.GUC_STEP=str(HERE/'vendor/ndr-240-24.stp')
KS.modul()
records=[]
for p in KS.PARCALAR:
 b=KS._tek(p['wp']).BoundingBox()
 records.append(dict(name=p['ad'],material=p['mal'],group=p.get('grup'),lo=[b.xmin+4000,b.ymin,b.zmin],hi=[b.xmax+4000,b.ymax,b.zmax],bom=p.get('bom'),metadata_only=True))
(HERE/'native_mechanism_names.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print('NATIVE_NAMES',len(records),flush=True)
