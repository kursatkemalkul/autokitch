"""Re-encode CURRENT K triangles through existing native sheet encoder, never replace geometry."""
from pathlib import Path
import sys,pickle,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
U=ROOT/'arastirma/_uretec/codex/k_montaj';sys.path.insert(0,str(U))
from bend_encode import *
from current_cad import factory_from_source
from roof_mounts import build_roof
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];factory=factory_from_source(K,OUT)
_,_,shelf=build();_,_,roof=build_roof();sheets={s.ad:s for s in factory.SAC};sheets['k71_istasyon_rafi']=shelf;sheets['ust_sac']=roof
old=json.loads((OUT/'source_bending_updated.json').read_text(encoding='utf-8'))
aliases={'onyuz_kapak_K':['k_govde_on_seffaf_0','k_govde_on_seffaf_2','k_govde_on_seffaf_3'],'onyuz_kapak_K_ic_tava':['k_govde_on_seffaf_1']}
records=[];audit=[]
for oldrec in old['sheets']:
 name=oldrec['name'];targets=aliases.get(name,[name]);targets=[a for a in targets if a in P]
 if not targets:continue
 triangles=np.concatenate([P[a]['V'][P[a]['F']] for a in targets]);offset=[0,0,0] if name=='k71_istasyon_rafi' else [4000,0,0]
 rec=encode_sheet(sheets[name],triangles,offset);rec['target_parts']=targets
 rows={k:rec[k] for k in ['name','endpoint_passed','unclassified_vertices','folded_endpoint_max_error_mm']};rows['unclassified_examples']=[rec['vertices'][i] for i in rec['unclassified_vertices'][:8]];audit.append(rows)
 print('CURRENT_SHEET',name,'unclassified',len(rows['unclassified_vertices']),'error',rows['folded_endpoint_max_error_mm'],flush=True)
 if rec['endpoint_passed']:records.append(rec)
(HERE/'current_sheet_encoding_audit.json').write_text(json.dumps(clean({'checks':audit,'passed':all(r['endpoint_passed'] for r in audit),'production_release':False}),ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'current_sheet_bending.json').write_text(json.dumps(clean({'sheets':records,'passed':all(r['endpoint_passed'] for r in audit),'production_release':False}),ensure_ascii=False,separators=(',',':')),encoding='utf-8')
sys.stdout.flush();os._exit(0 if all(r['endpoint_passed'] for r in audit) else 2)
