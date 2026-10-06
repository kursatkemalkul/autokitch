"""Verify exact changed triangle scope and unchanged other nodes on1um grid."""
from lower_support import *
import hashlib,gzip,collections
Y=H/'yama_v9'
for p in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
root=OUT/'chain73';k1=OUT/'k1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(t):
 q=np.rint(np.asarray(t)*1000).astype('<i8')
 start=min(range(3),key=lambda i:tuple(q[i]))
 return q[(start+np.arange(3))%3].tobytes()
def inventory(file):
 g=Glb(str(file));out={}
 for p in g.prims:
  if p.get('gizli') or p['pr'].get('mode',4)!=4:continue
  q=p['X'][p['T']];area=np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1);q=q[area>1e-9]
  dst=out.setdefault(p['name'],collections.Counter())
  rounded=np.rint(q*1000).astype('<i8')
  start=np.lexsort((rounded[:,:,2],rounded[:,:,1],rounded[:,:,0]),axis=1)[:,0]
  ordered=rounded[np.arange(len(rounded))[:,None],(start[:,None]+np.arange(3))%3]
  packed=np.ascontiguousarray(ordered).reshape(-1,9).view(np.dtype('V72')).ravel()
  dst.update(packed.tolist())
 return out
source=root/'A/hat3_v10s.glb';output=root/'A/hat3_v10t.glb';second=root/'B/hat3_v10t.glb'
recipe=json.loads(gzip.decompress((k1/'rounded_post_recipe.json.gz').read_bytes()))
assert sha(source)==recipe['source_model_sha256']
assert sha(output)==sha(second),'Stage79 A/B not identical'
before=inventory(source);after=inventory(output);node='K_ITICI__sac';expected=before[node].copy();removed=0;added=0
for a,r in recipe['repairs'].items():
 for t in r['original_triangles']:
  k=key(t);assert expected[k]>0,(a,'Original face not found');expected[k]-=1;removed+=1
  if not expected[k]:del expected[k]
 v=np.asarray(r['vertices']);f=np.asarray(r['triangles'])
 for t in v[f]:expected[key(t)]+=1;added+=1
changed=[n for n in set(before)|set(after) if n!=node and before.get(n)!=after.get(n)]
missing=expected-after[node];extra=after[node]-expected
rebind=json.loads((k1/'step79_ownership_rebind_audit.json').read_text(encoding='utf-8'))
registry=json.loads((k1/'surface_ownership_registry79.json').read_text(encoding='utf-8'))
extraction=json.loads((k1/'k_bil79.json').read_text(encoding='utf-8'))
assert registry['source_model_sha256']==sha(output)
assert rebind['previous_parts_sha256']==sha(k1/'k_parca.pkl')
assert rebind['repair_payload_sha256']==sha(k1/'rounded_post_recipe.json.gz')
assert rebind['raw_parts_sha256']==sha(k1/'k_parca79_raw.pkl')
assert Path(extraction['source']['path']).resolve()==output.resolve()
assert extraction['source']['size']==output.stat().st_size and extraction['source']['mtime_ns']==output.stat().st_mtime_ns
precision_verified=rebind['passed'] and not rebind['ambiguous'] and rebind['unmatched_expected_count']==0 and rebind['matched_triangles']==rebind['expected_triangles']==rebind['raw_triangles'] and rebind['maximum_recompression_vertex_distance_mm']<=.001
report={'source_model_sha256':sha(source),'output_model_sha256':sha(output),'a_b_byte_identical':True,'comparison_grid_mm':.001,'compared_nodes':len(before),'changed_nodes_outside_declared_scope':changed,'declared_removed_triangles':removed,'declared_added_triangles':added,'rounded_grid_missing_keys':sum(missing.values()),'rounded_grid_extra_keys':sum(extra.values()),'rounded_grid_note':'Rounding-bin differences must pass actual cyclic vertex distance and one-to-one matching; triangle counts alone do not pass.','one_to_one_actual_geometry_rebind_verified':precision_verified,'maximum_actual_vertex_distance_mm':rebind['maximum_recompression_vertex_distance_mm'],'rebind_audit_sha256':sha(k1/'step79_ownership_rebind_audit.json'),'passed':not changed and precision_verified,'production_release':False,'reextraction_and_movement_audits_required':True}
(k1/'stage79_geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('STAGE79_GEOMETRY',report,flush=True)
assert report['passed']
sys.stdout.flush();os._exit(0)
