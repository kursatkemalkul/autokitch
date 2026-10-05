"""K roof pack audit; includes measured source U shaft lengths, not invented."""
from roof_mounts import *
import itertools
p,r,s=build_roof(); measurements=json.loads((OUT/'roof_bolt_measurement.json').read_text(encoding='utf8'))
checks=[];bad=[];rows=[]
for x in (4100.,4300.):
    measured=next(m for m in measurements if m['x']==x)
    checks.append({'name':f'Existing U shaft measured at {x}', 'passed':measured['shaft_y']==[1847.5,1863.5]})
    bolt=S.vida('ISO4762','M8',16,(x,1863.5,-700),(0,-1,0),ad=f'external_U_screw_{x}')
    p.append(bolt)
for part in p:
    sh=part['sh'];b=sh.BoundingBox();rows.append((part,sh,np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])))
for (a,sa,la,ha),(b,sb,lb,hb) in itertools.combinations(rows,2):
    if np.any(np.minimum(ha,hb)-np.maximum(la,lb)<-1e-5):continue
    v=sa.intersect(sb).Volume()
    if v<.01:continue
    weld=a.get('tur')=='kaynak' or b.get('tur')=='kaynak'
    threaded=('external_U_screw_' in a['ad'] and 'k73_tavan_baglanti_plakasi_' in b['ad']) or ('external_U_screw_' in b['ad'] and 'k73_tavan_baglanti_plakasi_' in a['ad'])
    if not weld and not threaded:bad.append({'a':a['ad'],'b':b['ad'],'volume_mm3':v})
dfm=r['roof_dfm']+[c for part in p for c in part.get('dfm',[])]
checks += [{'name':'All roof and reinforcement DFM','passed':all(c['durum']=='GEÇTİ' for c in dfm)},
 {'name':'All new roof solids valid','passed':all(part['sh'].isValid() for part in p)},
 {'name':'M8 engagement >=8mm, protrusion 1..3 threads','passed':all(j['engagement_mm']>=8 and 1<=j['protrusion_threads']<=3 for j in r['connections'])},
 {'name':'Unclassified solid overlap zero','passed':not bad},
 {'name':'U geometry unchanged by definition','passed':not r['external_U_geometry_modified']}]
report={'scope':'K roof pack; whole motion and assembly not certified','checks':checks,'unexpected_intersections':bad,'passed':all(c['passed'] for c in checks),'full_assembly_release':False}
(OUT/'k73_roof_audit.json').write_text(json.dumps(clean(report),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(clean(report),ensure_ascii=False),flush=True);sys.stdout.flush();os._exit(0 if report['passed'] else 2)
