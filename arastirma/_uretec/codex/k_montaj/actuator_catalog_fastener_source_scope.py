"""Byte determinism and global node scope proof for oil wall mounting candidate."""
from pathlib import Path
import json,gzip,hashlib
helper=Path(__file__).with_name('audit79_geometry.py')
ns=dict(__file__=str(helper),__name__='inventory_helper')
exec(compile(helper.read_text(encoding='utf-8').split("source=root/'A/hat3_v10s.glb'")[0],str(helper),'exec'),ns)
OUT=ns['OUT'];folder=OUT/'actuator_catalog_fastener_candidate';sha=ns['sha'];inventory=ns['inventory']
source=OUT/'oil_fluid_clamp_candidate/A/hat3_v10zb.glb';A=folder/'A/hat3_v10zc.glb';B=folder/'B/hat3_v10zc.glb'
assert sha(A)==sha(B)
recipe=json.loads(gzip.decompress((folder/'source_repair_recipe.json.gz').read_bytes()))
assert sha(source)==recipe['source_model_sha256']
import pickle
P=pickle.loads((OUT/'k1/k_parca_fluid_verified.pkl').read_bytes())['P']
allowed={P[a]['dugum'] for a in recipe['repairs']}
allowed.update(P[r['source_template']]['dugum'] for r in recipe['additional_parts'].values())
before=inventory(source);after=inventory(A)
changed=sorted(n for n in set(before)|set(after) if before.get(n)!=after.get(n))
outside=sorted(set(changed)-allowed)
assert not outside,outside
verified_path=OUT/'k1/k_parca_catalog_verified.pkl'
verified=pickle.loads(verified_path.read_bytes())['P']
rebind_path=OUT/'k1/catalog_ownership_rebind_audit.json'
rebind=json.loads(rebind_path.read_text(encoding='utf-8'))
registry=json.loads((OUT/'k1/surface_ownership_registry_catalog.json').read_text(encoding='utf-8'))
assert registry['source_model_sha256']==sha(A)
assert rebind['passed'] and not rebind['ambiguous'] and rebind['unmatched_expected_count']==0
assert rebind['repair_payload_sha256']==sha(folder/'geometry.json.gz')
assert rebind['previous_parts_sha256']==sha(OUT/'k1/k_parca_fluid_verified.pkl')
assert rebind['raw_parts_sha256']==sha(OUT/'k1/k_parca_catalog_raw.pkl')
assert len(verified)==1009+len(recipe['additional_parts'])
assert sum(len(p['F']) for p in verified.values())==rebind['matched_triangles']==rebind['expected_triangles']==rebind['raw_triangles']
r={'input_sha256':sha(source),'output_sha256':sha(A),'a_b_byte_identical':True,
 'allowed_nodes':sorted(allowed),'changed_nodes':changed,'changed_nodes_outside_scope':outside,
 'matched_source_report_sha256':sha(folder/'A/hat3_v10zc.json'),
 'candidate_recipe_sha256':sha(folder/'geometry.json.gz'),
 'passed_byte_determinism_and_global_scope':True,
 'expected_product_parts':1009+len(recipe['additional_parts']),
 'full_triangle_rebind_passed':True,'verified_parts_sha256':sha(verified_path),
 'triangle_rebind_report_sha256':sha(rebind_path),'matched_triangles':rebind['matched_triangles'],
 'complete_animation_checked':False,'production_release':False,
 'next':'Measure actual joints and integrate the new mounting pieces into the checked assembly plan before source activation.'}
(folder/'source_scope_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('OIL_SOURCE_SCOPE',r['a_b_byte_identical'],r['expected_product_parts'],'outside',outside,flush=True)

import sys,os
sys.stdout.flush();os._exit(0)
