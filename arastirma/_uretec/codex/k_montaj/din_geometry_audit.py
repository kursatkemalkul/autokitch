"""Actual source measurements after both accessible DIN rail mounts."""
from pathlib import Path
helper=Path(__file__).with_name('audit79_geometry.py')
code=helper.read_text(encoding='utf-8').split("source=root/'A/hat3_v10s.glb'")[0]
ns=dict(__file__=str(helper),__name__='din_helpers');exec(compile(code,str(helper),'exec'),ns)
inventory,sha,OUT=ns['inventory'],ns['sha'],ns['OUT']
import json,pickle,numpy as np,trimesh

folder=OUT/'din_mount_candidate';k1=OUT/'k1'
source=OUT/'panel_mount_candidate/A/hat3_v10u.glb'
a=folder/'A/hat3_v10v.glb';b=folder/'B/hat3_v10v.glb'
candidate=json.loads((folder/'audit.json').read_text());rebind=json.loads((k1/'din_ownership_rebind_audit.json').read_text())
assert candidate['passed'] and candidate['source_model_sha256']==sha(source)
assert sha(a)==sha(b)
assert rebind['passed'] and rebind['previous_parts_sha256']==sha(k1/'k_parca_panel_verified.pkl')
assert rebind['raw_parts_sha256']==sha(k1/'k_parca_din_raw.pkl')
assert rebind['repair_payload_sha256']==sha(folder/'geometry.json.gz')
before=inventory(source);after=inventory(a)
changed=sorted(n for n in set(before)|set(after) if before.get(n)!=after.get(n))
outside=sorted(set(changed)-{'K_ELEKTRIK__sac','K_ELEKTRIK__celik'})
P=pickle.load((k1/'k_parca_din_verified.pkl').open('rb'))['P'];rows=[]
for j in candidate['joints']+candidate['rail_joints']:
    c=np.asarray(j['centre_mm']);e=np.asarray(j['axis'],float)
    m=(P[j['parts'][0]]['V']-c)@e;n=(P[j['parts'][-1]]['V']-c)@e
    engagement=min(m.max(),n.max())-max(m.min(),n.min());protrusion=m.max()-n.max()
    holes=[];rail=j['id'].startswith('din_')
    for name in (('pano_plakasi',) if rail else ('pano_plakasi','arka_sac',j['parts'][1])):
        v=P[name]['V']-c;t=v@e;r=np.linalg.norm(v-np.outer(t,e),axis=1)
        sampled=int((abs(r-2.75)<.01).sum())
        holes.append({'part':name,'bore_vertices':sampled,'passed':sampled>=12})
    clearance=None
    if rail:
        name=j['parts'][1];r=P[name];point=[c[0],c[1],-817.5]
        mesh=trimesh.Trimesh(r['V'],r['F'],process=False)
        wall_distance=float(trimesh.proximity.closest_point(mesh,np.asarray([point]))[1][0])
        clearance=wall_distance-2.75
        holes.append({'part':name,'opening':'supplier stock15x6.2 slot','measured_axis_to_slot_wall_mm':wall_distance,
                      'clearance_around_nominal5.5mm_passage_mm':clearance,'passed':clearance>=.3})
    rows.append({'id':j['id'],'measured_engagement_mm':float(engagement),'measured_protrusion_mm':float(protrusion),
                 'hosts':holes,'passed':bool(engagement>=4.99 and .79<=protrusion<=2.41 and all(h['passed'] for h in holes))})
report={'scope':'Four panel mounting joints and four DIN endpoint joints, not purchased device clip certification',
        'input_sha256':sha(source),'output_sha256':sha(a),'a_b_byte_identical':True,
        'candidate_audit_sha256':sha(folder/'audit.json'),'rebind_sha256':sha(k1/'din_ownership_rebind_audit.json'),
        'verified_parts_sha256':sha(k1/'k_parca_din_verified.pkl'),'parts':len(P),'triangles':sum(len(p['F']) for p in P.values()),
        'changed_nodes':changed,'changed_nodes_outside_scope':outside,'actual_one_to_one_triangles_matched':rebind['matched_triangles'],
        'maximum_actual_recompression_vertex_distance_mm':rebind['maximum_recompression_vertex_distance_mm'],
        'joints':rows,'passed':not outside and all(j['passed'] for j in rows),
        'source_activation':False,'manufacturing_release':False,'production_release':False,'remaining_checks':candidate['remaining_checks']}
(folder/'source_geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('DIN_SOURCE',report['passed'],'parts',len(P),'triangles',report['triangles'],'outside',outside,flush=True)
assert report['passed']
ns['sys'].stdout.flush();ns['os']._exit(0)
