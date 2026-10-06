"""Global scope, byte determinism and actual885part geometry for bottom fixings."""
from pathlib import Path
import pickle,json,gzip,hashlib,numpy as np
helper=Path(__file__).with_name('audit79_geometry.py')
ns=dict(__file__=str(helper),__name__='inventory_helper')
exec(compile(helper.read_text(encoding='utf-8').split("source=root/'A/hat3_v10s.glb'")[0],str(helper),'exec'),ns)
OUT=ns['OUT'];folder=OUT/'belt_bottom_mount_candidate';H=OUT/'k1';sha=ns['sha'];inventory=ns['inventory']
source=OUT/'belt_support_candidate/A/hat3_v10w.glb';A=folder/'A/hat3_v10x.glb';B=folder/'B/hat3_v10x.glb'
assert sha(A)==sha(B)
recipe=json.loads(gzip.decompress((folder/'source_repair_recipe.json.gz').read_bytes()))
assert sha(source)==recipe['source_model_sha256']
rebind=json.loads((H/'bottom_ownership_rebind_audit.json').read_text(encoding='utf-8'))
assert rebind['passed'] and not rebind['ambiguous'] and not rebind['unmatched_expected_count']
assert rebind['previous_parts_sha256']==sha(H/'k_parca_belt_verified.pkl')
assert rebind['repair_payload_sha256']==sha(folder/'geometry.json.gz')
P=pickle.load((H/'k_parca_bottom_verified.pkl').open('rb'))['P']
assert len(P)==885 and all(n not in P for n in recipe['removed_parts'])
previous=pickle.load((H/'k_parca_belt_verified.pkl').open('rb'))['P']
allowed=sorted(set(previous[n]['dugum'] for n in list(recipe['repairs'])+list(recipe['removed_parts'])))
allowed=sorted(set(allowed)|set(previous[r['source_template']]['dugum'] for r in recipe['additional_parts'].values()))
before=inventory(source);after=inventory(A)
changed=[n for n in set(before)|set(after) if before.get(n)!=after.get(n)];outside=sorted(set(changed)-set(allowed));assert not outside,outside
candidate=json.loads((folder/'audit.json').read_text(encoding='utf-8'));rows=[]
for j in candidate['joints']:
 insert=P[j['insert']]['V'];screw=P[j['screw']]['V'];washer=P[j['washer']]['V'];post=P[j['post']]['V']
 ilo,ihi=insert.min(0),insert.max(0);tip=float(screw[:,1].max());engagement=min(tip,ihi[1])-ilo[1];projection=tip-ihi[1]
 row={'id':j['id'],'insert_stock_mm':(ihi-ilo).tolist(),'actual_engagement_mm':float(engagement),'actual_protrusion_mm':float(projection),
      'actual_washer_seat_y_mm':float(washer[:,1].max()),'post_bottom_y_mm':float(post[:,1].min()),'passed':abs(engagement-6)<.002 and 1<=projection<=3 and abs(washer[:,1].max()-889)<.002}
 rows.append(row)
assert all(r['passed'] for r in rows)
report={'input_sha256':sha(source),'output_sha256':sha(A),'a_b_byte_identical':True,'verified_parts_sha256':sha(H/'k_parca_bottom_verified.pkl'),
        'rebind_sha256':sha(H/'bottom_ownership_rebind_audit.json'),'changed_nodes':sorted(changed),'allowed_nodes':allowed,'changed_nodes_outside_scope':outside,
        'parts':len(P),'triangles':sum(len(p['F']) for p in P.values()),'matched_triangles':rebind['matched_triangles'],'removed_parts':list(recipe['removed_parts']),
        'measured_joints':rows,'passed_source_geometry_only':True,'torch_load_manufacturing_verified':False,'full_montage_verified':False,'production_release':False}
(folder/'source_geometry_audit.json').write_text(json.dumps(ns['clean'](report),indent=2),encoding='utf-8')
print('BOTTOM_SOURCE',len(P),report['triangles'],'OUTSIDE',outside,'JOINTS',len(rows),flush=True)

import sys,os
sys.stdout.flush();os._exit(0)
