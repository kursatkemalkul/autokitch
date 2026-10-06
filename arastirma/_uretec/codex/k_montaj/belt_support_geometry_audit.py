"""Measure actual recompressed foot/cap/weld surfaces; audit all other nodes."""
from pathlib import Path
helper=Path(__file__).with_name('audit79_geometry.py');code=helper.read_text(encoding='utf-8').split("source=root/'A/hat3_v10s.glb'")[0]
ns={'__file__':str(helper),'__name__':'belt_geometry_helpers'};exec(compile(code,str(helper),'exec'),ns)
inventory,sha,OUT=ns['inventory'],ns['sha'],ns['OUT']
import json,pickle,numpy as np,math
import panel_mount_candidate as PM
import manifold3d as mf
FOLDER=OUT/'belt_support_candidate';H=OUT/'k1'
source=OUT/'din_mount_candidate/A/hat3_v10v.glb';a=FOLDER/'A/hat3_v10w.glb';b=FOLDER/'B/hat3_v10w.glb'
audit=json.loads((FOLDER/'audit.json').read_text(encoding='utf-8'));r=json.loads((H/'belt_ownership_rebind_audit.json').read_text(encoding='utf-8'))
assert audit['passed'] and audit['source_model_sha256']==sha(source) and sha(a)==sha(b)
assert r['passed'] and not r['ambiguous'] and not r['unmatched_expected_count']
assert r['previous_parts_sha256']==sha(H/'k_parca.pkl') and r['raw_parts_sha256']==sha(H/'k_parca_belt_raw.pkl') and r['repair_payload_sha256']==sha(FOLDER/'geometry.json.gz')
before=inventory(source);after=inventory(a);changed=sorted(n for n in set(before)|set(after) if before.get(n)!=after.get(n));outside=sorted(set(changed)-{'K_BANT__sac'})
P=pickle.load((H/'k_parca_belt_verified.pkl').open('rb'))['P'];original=pickle.load((H/'k_parca.pkl').open('rb'))['P']
origin=np.array([4200.,920.,-220.]);rows=[]
for j in audit['joints']:
 post=P[j['post']];cap=P[j['cap']];plate=P[j['plate']]
 x=(post['V'][:,0].min()+post['V'][:,0].max())/2;z=(post['V'][:,2].min()+post['V'][:,2].max())/2
 bodies={n:PM.solid(P[n]['V'],P[n]['F'],origin) for n in [j['post'],j['cap'],j['plate'],j['cap_weld']]+j['plate_welds']}
 box=mf.Manifold.cube([20,.1,8]).translate((x-10-origin[0],932.45-origin[1],z-4-origin[2]))
 cap_slice=float((bodies[j['cap']]^box).volume());plate_slice=float((bodies[j['plate']]^box).volume())
 cap_expected=(400-(4-math.pi)*16)*2
 section=(400-(4-math.pi)*16)-(256-(4-math.pi)*4)
 post_expected=section*35.5
 perimeter=48+8*math.pi;leg=1.4
 weld_expected=(leg*leg/2)*perimeter+2*math.pi*(leg**3/6)
 weld_volume=float(bodies[j['cap_weld']].volume());top_seams=[]
 for name in j['plate_welds']:
  vv=P[name]['V'];lo=vv.min(0);hi=vv.max(0)
  top_seams.append({'part':name,'length_mm':float(hi[0]-lo[0]),'measured_leg_y_mm':float(hi[1]-lo[1]),'measured_leg_z_mm':float(hi[2]-lo[2]),'actual_volume_mm3':float(bodies[name].volume()),'passed':bool(abs(hi[0]-lo[0]-20)<.001 and abs(hi[1]-lo[1]-1.4)<.001 and abs(hi[2]-lo[2]-1.4)<.001 and abs(lo[1]-932.5)<.001)})
 radial=post['V'][:,[0,2]]-[x,z];absxy=np.abs(radial)
 corner=(absxy[:,0]>6.001)&(absxy[:,1]>6.001)
 radii=np.linalg.norm(absxy[corner]-[6,6],axis=1)
 radius_error=float(np.minimum(abs(radii-4),abs(radii-2)).max()) if len(radii) else 999.
 row={'id':j['id'],'post_bottom_y_mm':float(post['V'][:,1].min()),'post_top_y_mm':float(post['V'][:,1].max()),'cap_bottom_y_mm':float(cap['V'][:,1].min()),'cap_top_y_mm':float(cap['V'][:,1].max()),'actual_seat_gap_mm':float(plate['V'][:,1].min()-cap['V'][:,1].max()),'profile_corner_radius_error_mm':radius_error,'post_volume_mm3':float(bodies[j['post']].volume()),'analytic_post_volume_mm3':post_expected,'cap_volume_mm3':float(bodies[j['cap']].volume()),'analytic_cap_volume_mm3':cap_expected,'continuous_cap_weld_volume_mm3':weld_volume,'analytic_continuous_cap_weld_volume_mm3':weld_expected,'cap_seat_slice_mm3':cap_slice,'plate_seat_slice_mm3':plate_slice,'plate_seams':top_seams}
 row['passed']=bool(abs(row['post_bottom_y_mm']-895)<.001 and abs(row['post_top_y_mm']-930.5)<.001 and abs(row['cap_bottom_y_mm']-930.5)<.001 and abs(row['cap_top_y_mm']-932.5)<.001 and abs(row['actual_seat_gap_mm'])<.001 and radius_error<.001 and abs(row['post_volume_mm3']-post_expected)/post_expected<.002 and abs(row['cap_volume_mm3']-cap_expected)/cap_expected<.002 and abs(weld_volume-weld_expected)/weld_expected<.003 and abs(cap_slice-8)<.03 and abs(plate_slice-6)<.03 and all(t['passed'] for t in top_seams))
 rows.append(row)
report={'input_sha256':sha(source),'output_sha256':sha(a),'a_b_byte_identical':True,'candidate_audit_sha256':sha(FOLDER/'audit.json'),'rebind_sha256':sha(H/'belt_ownership_rebind_audit.json'),'verified_parts_sha256':sha(H/'k_parca_belt_verified.pkl'),'parts':len(P),'triangles':sum(len(p['F']) for p in P.values()),'changed_nodes':changed,'changed_nodes_outside_scope':outside,'matched_triangles':r['matched_triangles'],'measured_joints':rows,'passed':not outside and len(P)==len(original)+16 and all(t['passed'] for t in rows),'source_activation':False,'manufacturing_release':False,'production_release':False,'remaining':['Foot/cap bench order and actual temporary support','Plate weld sequence before supplier roller/belt insertion','Weld torch access/load check','Whole-station motions and shared-chain replay']}
(FOLDER/'source_geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('BELT_SOURCE',report['passed'],len(P),report['triangles'],'outside',outside,flush=True)
for row in rows:print('BELT_JOIN',row['id'],row['passed'],'radius_error',row['profile_corner_radius_error_mm'],'weld_volume',row['continuous_cap_weld_volume_mm3'],row['analytic_continuous_cap_weld_volume_mm3'],flush=True)
assert report['passed'];ns['sys'].stdout.flush();ns['os']._exit(0)
