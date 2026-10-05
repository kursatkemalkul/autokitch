"""Re-encode CURRENT K triangles through existing native sheet encoder, never replace geometry."""
from pathlib import Path
import sys,pickle,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
U=ROOT/'arastirma/_uretec/codex/k_montaj';sys.path.insert(0,str(U))
from bend_encode import *
from current_cad import factory_from_source
from roof_mounts import build_roof
from mechanism_mounts import build_mounts
P=pickle.load((HERE/'k_parca.pkl').open('rb'))['P'];factory=factory_from_source(K,OUT)
lower_parts,_,shelf=build();roof_parts,_,roof=build_roof();mount_parts,_=build_mounts();sheets={s.ad:s for s in factory.SAC};sheets['k71_istasyon_rafi']=shelf;sheets['ust_sac']=roof
old=json.loads((OUT/'source_bending_updated.json').read_text(encoding='utf-8'))
aliases={'onyuz_kapak_K':['k_govde_on_seffaf_0','k_govde_on_seffaf_2','k_govde_on_seffaf_3'],'onyuz_kapak_K_ic_tava':['k_govde_on_seffaf_1']}
patch=S.Sac('k_e4_sol_yama_40x40','dis',t=1.5,R=2.25,birim='K_GOVDE')
patch.taban([(1789,-790),(1829,-790),(1829,-750),(1789,-750)],O=(1.5,0,0),ex=(0,1,0),ey=(0,0,1))
sheets[patch.ad]=patch
old['sheets'].append({'name':patch.ad})
# Two GLB labels are fragments of each physical step72 upper plate.
fragment_audit=json.loads((HERE/'pusher_plate_fragment_audit.json').read_text(encoding='utf-8'));assert fragment_audit['passed']
for row in fragment_audit['checks']:aliases[row['physical_stock']]=[row['physical_stock'],row['fragment']]
# Explicit custom flat stock from our step71/73 CAD, not guessed purchased parts.
flat_rows=[]
for part in lower_parts+roof_parts+mount_parts:
 name=part['ad']
 if name not in P or not name.startswith(('k71_alt_flans_','k71_disli_ust_kapak_','k71_raf_yan_sac_','k73_tavan_baglanti_plakasi_','k72_itici_taban_','k72_itici_ust_plaka_')):continue
 bb=part['sh'].BoundingBox();lo=np.array([bb.xmin,bb.ymin,bb.zmin]);hi=np.array([bb.xmax,bb.ymax,bb.zmax]);span=hi-lo;axis=int(np.argmin(span));t=float(span[axis])
 assert any(abs(t-v)<.001 for v in (.8,1,1.2,1.5,2,3,4,6)),(name,t)
 flat=S.Sac(name,'braket',t=round(t,3),R=1.5*t,birim='K_GOVDE')
 if axis==0:O=lo;ex=(0,1,0);ey=(0,0,1);w,h=span[1],span[2]
 elif axis==1:O=(lo[0],lo[1],hi[2]);ex=(1,0,0);ey=(0,0,-1);w,h=span[0],span[2]
 else:O=lo;ex=(1,0,0);ey=(0,1,0);w,h=span[0],span[1]
 flat.taban([(0,0),(w,0),(w,h),(0,h)],O=O,ex=ex,ey=ey)
 sheets[name]=flat;old['sheets'].append({'name':name})
 flat_rows.append({'name':name,'thickness_mm':t,'normal_axis':'XYZ'[axis],'native_stock_bounds_mm':[lo.tolist(),hi.tolist()],'source':'lower_support.build / roof_mounts.build_roof / mechanism_mounts.build_mounts','holes_from_current_mesh_preserved':True,'machining_verified':False})
(HERE/'custom_flat_stock_audit.json').write_text(json.dumps(clean({'parts':flat_rows,'production_release':False}),indent=2),encoding='utf-8')
records=[];audit=[]
for oldrec in old['sheets']:
 name=oldrec['name'];targets=aliases.get(name,[name]);targets=[a for a in targets if a in P]
 if not targets:continue
 triangles=np.concatenate([P[a]['V'][P[a]['F']] for a in targets]);offset=[0,0,0] if name=='k71_istasyon_rafi' or any(r['name']==name for r in flat_rows) else [4000,0,0]
 rec=encode_sheet(sheets[name],triangles,offset,stock_outline=(name=='ust_sac' or any(r['name']==name for r in flat_rows)));rec['target_parts']=targets
 rows={k:rec[k] for k in ['name','endpoint_passed','unclassified_vertices','folded_endpoint_max_error_mm']};rows['unclassified_examples']=[rec['vertices'][i] for i in rec['unclassified_vertices'][:8]];audit.append(rows)
 print('CURRENT_SHEET',name,'unclassified',len(rows['unclassified_vertices']),'error',rows['folded_endpoint_max_error_mm'],flush=True)
 if rec['endpoint_passed']:records.append(rec)
(HERE/'current_sheet_encoding_audit.json').write_text(json.dumps(clean({'checks':audit,'passed':all(r['endpoint_passed'] for r in audit),'production_release':False}),ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'current_sheet_bending.json').write_text(json.dumps(clean({'sheets':records,'passed':all(r['endpoint_passed'] for r in audit),'production_release':False}),ensure_ascii=False,separators=(',',':')),encoding='utf-8')
sys.stdout.flush();os._exit(0 if all(r['endpoint_passed'] for r in audit) else 2)
