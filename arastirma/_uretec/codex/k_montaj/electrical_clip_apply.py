"""Append four source-bound clip perimeter joints to a private K prototype.
Does not register shared chain steps or alter supplier geometry.
"""
from lower_support import *
import pickle,hashlib,gzip
import k79_bound_removal_writer as W
folder=OUT/'electrical_clip_weld_candidate'
payload_path=folder/'geometry.json.gz'
payload=json.loads(gzip.decompress(payload_path.read_bytes()))
torch=json.loads((folder/'torch_access_audit.json').read_text())
assert torch['passed_all_preassembly_envelopes']
assert torch['candidate_geometry_sha256']==hashlib.sha256(payload_path.read_bytes()).hexdigest()
cache=OUT/'k1/k_parca_head_verified.pkl';P=pickle.loads(cache.read_bytes())['P']
assert payload['source_parts_sha256']==hashlib.sha256(cache.read_bytes()).hexdigest()
source=Path(sys.argv[1]);dest=Path(sys.argv[2]);source_audit=json.loads((OUT/'cut_head_yoke_candidate/source_scope_audit.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_audit['output_sha256']
repairs={};extra={};entries={}
for join in payload['joins']:
 a=join['clip'];old=P[a]
 repairs[a]=dict(original_triangles=old['V'][old['F']].tolist(),vertices=old['V'].tolist(),triangles=old['F'].tolist(),
  proof=dict(part=a,closed_status='Error.NoError',maximum_declared_precision_adjustment_mm=0.,purpose='Unchanged exact cable clip template; add only own foot welds'))
 for seam in join['seams']:
  r=payload['parts'][seam];extra[seam]=dict(source_template=a,vertices=r['V'],triangles=r['F'])
  v=np.asarray(r['V']);lo=v.min(0);hi=v.max(0)
  entries[seam]=dict(dugum=old['dugum'],tur='kaynak',bom=r['description'],kutu=[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]])
recipe=folder/'source_repair_recipe.json.gz'
recipe.write_bytes(gzip.compress(json.dumps(dict(source_model_sha256=source_audit['output_sha256'],repairs=repairs,additional_parts=extra),separators=(',',':')).encode(),mtime=0))
dest.parent.mkdir(exist_ok=True)
W.apply(source,dest,recipe,expected_names=set(repairs),step=79,source_nodes=sorted({P[a]['dugum'] for a in repairs}),additional_parts=extra)
dest.with_name(dest.stem+'_ent.json').write_text(json.dumps(clean(dict(adim=79,prototype='Private clip welding extension; NOT a shared registered step',parca=entries,production_release=False)),indent=2),encoding='utf-8')
print('CLIP_PRIVATE_SOURCE',dest,'SEAMS',len(extra),flush=True)
sys.stdout.flush();os._exit(0)
