"""New K foot fasteners: solid intersections, DFM and real stack dimensions."""
from mechanism_mounts import *
import itertools
mounts,r=build_mounts();lower,_,_=build();rows=[];bad=[];allowed=[]
for p in mounts+lower:
    sh=p['sh'];b=sh.BoundingBox();rows.append((p,sh,np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])))
for (a,sa,la,ha),(b,sb,lb,hb) in itertools.combinations(rows,2):
    if a in lower and b in lower:continue
    if np.any(np.minimum(ha,hb)-np.maximum(la,lb)<-1e-5):continue
    volume=sa.intersect(sb).Volume()
    if volume<.01:continue
    is_weld=a.get('tur')=='kaynak' or b.get('tur')=='kaynak'
    entry={'a':a['ad'],'b':b['ad'],'volume_mm3':round(volume,6)}
    if is_weld:allowed.append(dict(entry,reason='TIG penetration at explicit support/spacer joint'))
    else:bad.append(entry)
checks=[{'name':'12 explicit foot connections','passed':len(r['connections'])==12},
 {'name':'Nut thread engagement >= nominal screw diameter','passed':all(x['engagement_mm']>=x['nominal_diameter_mm'] for x in r['connections'])},
 {'name':'Screw protrusions 1..3 threads','passed':all(1<=x['protrusion_threads']<=3 for x in r['connections'])},
 {'name':'All new foot sheets/plaque DFM','passed':all(c['durum']=='GEÇTİ' for p in mounts for c in p.get('dfm',[]))},
 {'name':'All new parts valid CAD solids','passed':all(p['sh'].isValid() for p in mounts)},
 {'name':'Zero non-weld intersection with new lower structure','passed':not bad}]
report={'scope':'new foot mounts + new lower structure; source context and full montage still required','checks':clean(checks),'unexpected_intersections':bad,'weld_intersections':allowed,'passed':all(x['passed'] for x in checks),'full_assembly_release':False}
(OUT/'k72_mount_audit.json').write_text(json.dumps(clean(report),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(clean({'checks':checks,'unexpected':bad}),ensure_ascii=False),flush=True);sys.stdout.flush();os._exit(0 if report['passed'] else 2)
