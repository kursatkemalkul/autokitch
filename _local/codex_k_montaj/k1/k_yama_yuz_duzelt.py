"""Restore the patch's two mislabelled faces, preserving every source triangle.

Provenance: elk3/e4.py adds a complete 12-triangle 40x40x1.5 box.
The missing two faces have the box's outward -X normal, opposite the
adjoining wall's inner +X normal. No geometry/face creation/duplication.
"""
from pathlib import Path
import json,pickle,hashlib,numpy as np,manifold3d as M
from k_yuz_etiket import apply
H=Path(__file__).resolve().parent;registry=H/'surface_ownership_registry.json'
current=pickle.load((H/'k_parca.pkl').open('rb'));P=current['P']
rawD=pickle.load((H/'k_parca77_raw.pkl').open('rb'));raw=rawD['P']
name='k_e4_sol_yama_40x40';wall='sol_sac_urun_girisi'
q=P[name]['V'][P[name]['F']];lo=q.min((0,1));hi=q.max((0,1))
assert np.max(abs(lo-[4001.5,1789,-790]))<.001 and np.max(abs(hi-[4003,1829,-750]))<.001
source=H.parents[2]/'arastirma/_uretec/h3/yama_v9/kaynak/elk3/e4.py'
code=source.read_text(encoding='utf-8-sig')
assert 'yama("K_GOVDE__kabuk", (4001.5, 1789, -790), (4003.0, 1829, -750)' in code
r=json.loads(registry.read_text(encoding='utf-8'))
if len(q)==12:
 print('PATCH_ALREADY_CLOSED',flush=True);raise SystemExit(0)
assert len(q)==10
w=P[wall]['V'][P[wall]['F']];mask=np.all(w.min(1)>=lo-.001,1)&np.all(w.max(1)<=hi+.001,1);contact=w[mask]
assert len(contact)==2 and np.max(abs(contact[:,:,0]-lo[0]))<.001
changes=[]
for t in contact:
 normal=np.cross(t[1]-t[0],t[2]-t[0]);normal/=np.linalg.norm(normal)
 assert normal[0]<-.999999 and np.max(abs(normal[1:]))<1e-8
 rawq=raw[wall]['V'][raw[wall]['F']];indices=np.flatnonzero(np.all(rawq==t,axis=(1,2)));assert len(indices)==1
 row={'from':wall,'triangle':int(indices[0]),'to':name,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest()}
 assert not any((x['from'],x['triangle'])==(wall,row['triangle']) for x in r['changes'])
 changes.append(row)
# Closure proof on the existing twelve triangles, no guessed surface.
v,f=np.unique(np.concatenate([q,contact]).reshape(-1,3),axis=0,return_inverse=True)
mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f.reshape(-1,3),dtype=np.uint32),tolerance=.001);mesh.merge();solid=M.Manifold(mesh)
assert str(solid.status())=='Error.NoError' and abs(solid.volume()-2400)<1
r['changes']+=changes;r['patch_closed_face_changes']=len(changes)
registry.write_text(json.dumps(r,indent=2),encoding='utf-8')
before=sorted(t.tobytes() for p in raw.values() for t in p['V'][p['F']]);rawD['P']=apply(raw)
after=sorted(t.tobytes() for p in rawD['P'].values() for t in p['V'][p['F']]);assert before==after
pickle.dump(rawD,(H/'k_parca.pkl').open('wb'))
report={'source_model_sha256':r['source_model_sha256'],'source_generator_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changes':changes,'patch_closed':True,'volume_mm3':solid.volume(),'source_triangle_multiset_unchanged':True,'geometry_changed':False,'production_release':False}
(H/'patch_closed_face_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PATCH_CLOSED',solid.volume(),'mm3; two source faces relabelled',flush=True)
