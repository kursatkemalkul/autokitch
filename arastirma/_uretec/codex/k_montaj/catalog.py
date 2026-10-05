exec(open(__file__.replace('catalog.py','inspect_source.py'),encoding='utf-8-sig').read().split('g=K.kur();')[0])
import numpy as np
from collections import Counter
g=K.kur(); parts=K.govde_parcalari(); records=[]
for p in parts:
 sh=p['wp'].val(); b=sh.BoundingBox()
 records.append({'name':p['ad'],'type':p['tur'],'lo':[b.xmin+4000,b.ymin,b.zmin],'hi':[b.xmax+4000,b.ymax,b.zmax],'bom':clean(p.get('bom')),'meta':clean(p.get('meta')),'origin':'legacy CAD; requires match to source61'})
(OUT/'legacy_catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
actual=json.loads((OUT/'source_components.json').read_text(encoding='utf8'))['components']; matches=[]
for p in records:
 cand=[(max(abs(np.array(p['lo'])-q['lo']).max(),abs(np.array(p['hi'])-q['hi']).max()),q) for q in actual if q['node'].startswith('K_GOVDE')]
 e,q=min(cand,key=lambda x:x[0]);matches.append({'legacy_name':p['name'],'source_component':q['id'],'bbox_error_mm':float(e),'bbox_unique_match':bool(e<=.01),'surface_equality_verified':False})
(OUT/'source_matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding='utf8')
print('bbox matches',sum(m['bbox_unique_match'] for m in matches),'/',len(matches),flush=True)
print('Unmatched:',[m['legacy_name'] for m in matches if not m['bbox_unique_match']],flush=True)
sys.stdout.flush();os._exit(0)

