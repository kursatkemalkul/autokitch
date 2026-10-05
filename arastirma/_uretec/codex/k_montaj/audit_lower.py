"""Independent pair-volume, hollow section and fastener checks for K step71."""
from lower_support import *
import itertools
p,r,s=build(); rows=[]; overlaps=[]
for part in p:
    shape=part['sh'];b=shape.BoundingBox()
    rows.append((part,shape,np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])))
for (a,sa,la,ha),(b,sb,lb,hb) in itertools.combinations(rows,2):
    if np.any(np.minimum(ha,hb)-np.maximum(la,lb)<-1e-5):continue
    volume=sa.intersect(sb).Volume()
    if volume<.01:continue
    # Only explicitly modelled threaded engagement and TIG penetration are
    # permitted. Every permitted overlap remains visible in the audit report.
    same_support=lambda aa,bb: aa.split('_')[-2:]==bb.split('_')[-2:]
    allowed=False;why=None
    for conn in r['connections']:
        if a['ad'] in conn['parts'] and b['ad'] in conn['parts'] and conn['id'].startswith('top_'):
            allowed=True;why='M5 external/minor thread envelope in tapped cap'
    if a.get('tur')=='kaynak' or b.get('tur')=='kaynak':
        w=a if a.get('tur')=='kaynak' else b; mate=b if w is a else a
        if mate['stage'] in ('support_weld','shelf_weld','shelf_install'):
            allowed=True;why='TIG fillet weld penetration; union at permanent join'
    overlaps.append({'a':a['ad'],'b':b['ad'],'volume_mm3':round(volume,6),'allowed':allowed,'reason':why})
bad=[x for x in overlaps if not x['allowed']]
checks=[{'name':'Shelf DFM including two-bend press sequence','passed':all(x['durum']=='GEÇTİ' for x in r['dfm'])},
 {'name':'Each new manufactured part is a valid solid','passed':all(x['sh'].isValid() and x['sh'].Volume()>0 for x in p)},
 {'name':'Six 40x40x1.5 hollow profiles','passed':len([x for x in p if x.get('tur')=='profil' and x['meta']['kesit'][:3]==[40,40,1.5]])==6},
 {'name':'24 explicit threaded joints; engagement >= diameter','passed':len(r['connections'])==24 and all(x['engagement_mm']>=5 for x in r['connections'])},
 {'name':'12 lower stud protrusions 1..3 M5 threads','passed':all(.8<=x['protrusion_mm']<=2.4 for x in r['connections'] if x['id'].startswith('base_'))},
 {'name':'12 upper screw protrusions 1..3 M5 threads','passed':all(.8<=x['protrusion_mm']<=2.4 for x in r['connections'] if x['id'].startswith('top_'))},
 {'name':'No geometry extends under B interface Y788','passed':min(x[2][1] for x in rows)>=787.999},
 {'name':'Zero unclassified solid overlap within new subassembly','passed':not bad}]
report={'scope':'new lower subassembly only; not whole §5','checks':checks,'intersections':overlaps,'passed':all(x['passed'] for x in checks),'full_assembly_release':False}
report=clean(report)
(OUT/'k71_lower_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(clean({'checks':checks,'unclassified_intersections':bad}),ensure_ascii=False),flush=True)
sys.stdout.flush();os._exit(0 if report['passed'] else 2)
