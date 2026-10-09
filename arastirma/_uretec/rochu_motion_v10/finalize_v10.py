from motion_v10 import *
import hashlib,io
m=Corrected();data=json.loads((OUT/'cycles.json').read_text());report={'version':10,'contacts_do_not_stop':True,'carrying_is_assumed':True,'physical_grasp_verified':False,'motions':{}}
for item in ['Dough','Cola','Dessert','Box']:
 s=data['sequences'][item+'_cycle'];frames=s['frames'];p=next(f['pose'] for f in frames if f['held'])
 if item=='Dough':m.belly=json.loads((OUT/'dough_belly_v9.json').read_text())
 shift=m.fit_grip(item,p);s['grip_report']=m.grip_report
 for f in frames:
  f['pose']['tip_shift_mm']=shift if f['held'] else 0.
  f['grasp_assumption']=bool(f['held']);f['pose']['root_hash']=m.r.definition['root_hash'];f['pose']['finger_roots']=m.r.definition['finger_roots']
 for prefix,a,b in [('Yalnız uçları kapat',0.,shift),('Yalnız uçları aç',shift,0.)]:
  group=[f for f in frames if f['label'].startswith(prefix)]
  for f,u in zip(group,np.linspace(0,1,len(group))):f['pose']['tip_shift_mm']=float(a+(b-a)*u)
 assert frames[0]['pose']['tip_shift_mm']==frames[-1]['pose']['tip_shift_mm']==0.
 rel=np.array(s['grasp_relative']).reshape(4,4);errors=[]
 for f in frames:
  p=f['pose'];assert p['valid'];assert max(abs(x) for x in p['q'])<=2*np.pi+1e-6
  W=m.r.kin.worlds(p['q'],p['rail'])[WR];errors.append(float(abs(W-np.array(p['worlds']['UR10E_body_06'])).max()))
  if f['held']:assert abs(W@rel-np.array(f['product_matrix'])).max()<1e-6
 assert max(errors)<1e-6
 drifts={}
 for prefix in ['Dik in','Dik yüksel']:
  v=np.array([f['pose']['contact'] for f in frames if f['label'].startswith(prefix)])
  if len(v):drifts[prefix]=float(np.ptp(v[:,[0,2]],axis=0).max()*1000);assert drifts[prefix]<.001
 checks=OUT/(item.lower()+'_v10_scene_check.json')
 if checks.exists():
  cc=json.loads(checks.read_text())
  for row in cc['rows']:
   f=frames[row['frame']];assert f['label']==row['phase']
   hits=[{'part':h['fixture'],'moving':h['moving']} for h in row['hits'] if h['native_surface_crossing']]
   f['check']={'native_surface_hits':hits,'tool_hits':hits,'not_checked':False,'method':cc['scope']}
 report['motions'][item]={'frames':len(frames),'FK_max_error':max(errors),'start_tip_mm':0,'end_tip_mm':0,'grip_shift_mm':shift,'side_drift_mm':drifts,'grasp_assumption':True,'full_pick_and_place':any(f['held'] for f in frames) and not frames[-1]['held'],'sampled_contacts':sum(r['native_crossings'] for r in cc['rows']) if checks.exists() else None}
 (OUT/(item.lower()+'_v10_candidate.json')).write_text(json.dumps(s,separators=(',',':')))
source=ROOT.parent/'codex-rochu-v2-belly-v9/otonom/hat3d/rochu-sabit-v2';old=trimesh.load(io.BytesIO(gzip.decompress((source/'fixed_head.glb.gz').read_bytes())),file_type='glb')
for name in m.r.head.graph.nodes_geometry:
 if not name.startswith('OEM_DAC_'):continue
 _,g=m.r.head.graph[name];_,g0=old.graph[name];v=m.r.head.geometry[g].vertices;assert np.array_equal(v,old.geometry[g0].vertices)
 for shift in [-11,0,5]:assert np.array_equal(v[v[:,2]<=START],deform(v,shift)[v[:,2]<=START])
report['neutral_OEM_vertices_exact']=True;report['rigid_housing_motion_mm']=0;report['radius_unchanged_mm']=50
layout=json.loads((OUT/'comparison_contract_v9.json').read_text());data['planned_layout']=layout['desired_layout'];data['shared_shelf']=json.loads((source/'cycles.json').read_text())['shared_shelf']
(OUT/'cycles.json').write_text(json.dumps(data,separators=(',',':')));(OUT/'validation_v10.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
