"""Actual permanent attachment of four source-bound cable feet; not release.
Temporary fixtures and whole-station manufacturing remain separate gates.
"""
from pathlib import Path
import pickle,json,hashlib,gzip,numpy as np,trimesh
H=Path(__file__).resolve().parent;folder=H.parent/'electrical_clip_weld_candidate'
plan=H/'plan_k_clip_full.pkl';D=pickle.loads(plan.read_bytes());P=D['P']
payload=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
ccd=json.loads((H/'clip_delta_ccd.json').read_text());binding=json.loads((H/'clip_plan_source_binding_audit.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert ccd['source_plan_sha256']==binding['source_plan_sha256']==sha(plan)
assert ccd['whole_rigid_path_passed'] and binding['full_source_triangle_multiset_preserved_on_naming_grid']
torch=json.loads((folder/'torch_access_audit.json').read_text())
assert torch['passed_all_preassembly_envelopes'] and torch['candidate_geometry_sha256']==sha(folder/'geometry.json.gz')
def end(a):return max([D['GOR'][a]]+[h[1] for h in D['HAR'][a]])
wire_times=[D['GOR'][a] for a in P if P[a].get('dugum','').startswith(('ELK_K__kablo','ELK_K_TARTI__kablo'))]
assert wire_times
contacts=[];closed=[]
for j in payload['joins']:
 for seam in j['seams']:
  operation=next(r for r in D['FABRICATION_JOINS'] if r.get('part')==seam)
  assert end(j['clip'])<=operation['t0'] and end(j['host'])<=operation['t0']
  assert operation['t1']<min(wire_times)
  for carrier in (j['clip'],j['host']):
   mesh=trimesh.Trimesh(P[carrier]['V'],P[carrier]['F'],process=False)
   _,d,_=trimesh.proximity.closest_point(mesh,P[seam]['V'])
   assert float(d.min())<.001
   contacts.append(dict(seam=seam,carrier=carrier,min_surface_distance_mm=float(d.min())))
 hold=next(r for r in D['TEMPORARY_SUPPORTS'] if r['id']=='clip_foot_hold_'+j['clip'])
 assert hold['release_after_welds']==j['seams'] and hold['t1']>=max(D['MF'][a]['buyu'][1] for a in j['seams'])
 assert hold['t1']<min(wire_times)
 closed.append(j['clip'])
previous=json.loads((H/'head_join_evidence.json').read_text());remaining=[r for r in previous['remaining_unresolved'] if r['part'] not in closed]
assert len(remaining)==previous['remaining_count']-4
r=dict(source_model_sha256=D['source_model_sha256'],source_parts_sha256=D['source_parts_sha256'],source_plan_sha256=sha(plan),
 closed_previous_clip_records=closed,permanent_mount_contacts=contacts,clip_mounts_fixed_before_cables=True,
 remaining_unresolved=remaining,remaining_count=len(remaining),previous_evidence_preserved_via_exact_parent_geometry_and_motion=True,
 temporary_fixture_geometry_verified=False,whole_station_connections_verified=False,manufacturing_release=False,production_release=False)
(H/'clip_join_evidence.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CLIP_PERMANENT_MOUNTS',len(closed),'CONTACTS',len(contacts),'REMAINING',len(remaining),flush=True)
