"""Bind a generated plan to the full current model cache; labels cannot change triangles."""
from pathlib import Path
import pickle,json,hashlib,collections,numpy as np
H=Path(__file__).resolve().parent

def digest(path):
 s=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):s.update(chunk)
 return s.hexdigest()

def bind():
 plan=H/'plan_k.pkl';D=pickle.load(plan.open('rb'));B=pickle.load((H/'k_bil.pkl').open('rb'))
 def face_key(q):
  # The inherited naming pipeline explicitly rounds coordinates to 0.0001 mm.
  q=np.round(np.asarray(q,dtype='<f8'),4);q[q==0]=0.;return hashlib.sha256(q.tobytes()).digest()
 max_adjustment=max(float(np.linalg.norm(p['V']-np.round(p['V'],4),axis=1).max()) for p in B['L'])
 assert max_adjustment<.000087,max_adjustment
 part_faces=collections.Counter(face_key(q) for p in D['P'].values() for q in p['V'][p['F']])
 source_faces=collections.Counter(face_key(q) for p in B['L'] for q in p['V'][p['F']])
 assert part_faces==source_faces,'Plan geometry differs from its full source cache'
 manifest=json.loads((H/'k_bil.json').read_text(encoding='utf-8'));model=Path(manifest['source']['path'])
 assert model.stat().st_size==manifest['source']['size'] and model.stat().st_mtime_ns==manifest['source']['mtime_ns'],'Source model changed after extraction'
 D['source_model_sha256']=digest(model);D['source_parts_sha256']=digest(H/'k_parca.pkl');D['source_cache_sha256']=digest(H/'k_bil.pkl');D['full_source_triangle_multiset_verified']=True
 pickle.dump(D,plan.open('wb'))
 report={'source_model_sha256':D['source_model_sha256'],'source_parts_sha256':D['source_parts_sha256'],'source_plan_sha256':digest(plan),'source_triangle_count':sum(source_faces.values()),'assigned_triangle_count':sum(part_faces.values()),'full_source_triangle_multiset_preserved_on_naming_grid':True,'naming_grid_mm':.0001,'max_source_vertex_adjustment_mm':max_adjustment,'production_release':False}
 (H/'plan_source_binding_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('BOUND_PLAN',report['source_model_sha256'],report['source_triangle_count'])
if __name__=='__main__':bind()
