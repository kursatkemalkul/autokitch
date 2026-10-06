"""Apply proven opposite-normal contact labels; preserve source triangles."""
from pathlib import Path
import pickle,json,hashlib,sys
from collections import defaultdict
import numpy as np,manifold3d as M
from k_yuz_etiket import apply
H=Path(__file__).resolve().parent;src=H/'k_parca.pkl';proposal=H/(sys.argv[1] if len(sys.argv)>1 else 'support_contact_face_proposals.json')
C=json.loads(proposal.read_text(encoding='utf-8'))
assert not any(r['from'].startswith('cevre_') for r in C['proposed_changes']), 'Coincident context candidates require separate evidence; do not relabel them as K stock.'
assert C['source_parts_sha256']==hashlib.sha256(src.read_bytes()).hexdigest()
if 'physical_sheet_checks' in C:
 assert all(r['after']['status']=='Error.NoError' for r in C['physical_sheet_checks'])
 assert all(r['after']['status']=='Error.NoError' for r in C['checks'] if r['before']['status']=='Error.NoError')
elif 'native_planes' in C:
 assert not C['ambiguous']
 assert all(r['after']['status']=='Error.NoError' for r in C['checks'] if r['before']['status']=='Error.NoError')
 assert all(r['maximum_native_face_distance_mm']<=.001 for r in C['proposed_changes'])
else:assert all(r['after']['status']=='Error.NoError' for r in C['checks'])
rawpath=H/'k_parca77_raw.pkl'
manifest=H/'current_source_manifest.json'
if manifest.exists():rawpath=H/json.loads(manifest.read_text(encoding='utf-8'))['raw_parts_file']
D=pickle.load(src.open('rb'));rawD=pickle.load(rawpath.open('rb'));P=D['P'];raw=rawD['P']
regpath=H/'surface_ownership_registry.json';R=json.loads(regpath.read_text(encoding='utf-8'))
old={(r['from'],r['triangle']):r for r in R['changes']};lookup=defaultdict(list)
def digest(t):return hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest()
for a,p in raw.items():
 for i,t in enumerate(p['V'][p['F']]):lookup[digest(t)].append((a,i))
added=[];affected=set();equivalent_origins=[]
for change in C['proposed_changes']:
 a=change['from'];t=P[a]['V'][P[a]['F'][change['current_triangle']]];sha=digest(t);assert sha==change['triangle_sha256']
 origins=[(r,i) for r,i in lookup[sha] if old.get((r,i),{}).get('to',r)==a]
 assert origins,(a,sha,origins)
 # Exactly coincident occurrences in the SAME current label have identical
 # geometry and the classifier gives them the same destination. Consume a
 # stable raw occurrence each time; never discard either source triangle.
 if len(origins)>1:equivalent_origins.append({'owner':a,'triangle_sha256':sha,'equivalent_raw_occurrences':sorted(origins),'destination':change['to']})
 origin,index=min(origins);row={'from':origin,'triangle':index,'to':change['to'],'triangle_sha256':sha}
 old[(origin,index)]=row;added.append(row);affected.update((a,change['to']))
R['changes']=[old[k] for k in sorted(old)];R['support_contact_normal_changes']=len(added)
before=sorted(t.tobytes() for p in raw.values() for t in p['V'][p['F']])
regpath.write_text(json.dumps(R,indent=2),encoding='utf-8');rawD['P']=apply(raw)
after=sorted(t.tobytes() for p in rawD['P'].values() for t in p['V'][p['F']]);assert before==after
checks=[]
for a in sorted(affected):
 p=rawD['P'][a];m=M.Mesh64(np.ascontiguousarray(p['V']),np.ascontiguousarray(p['F'],dtype=np.uint32),tolerance=.001);m.merge();s=M.Manifold(m)
 checks.append({'part':a,'status':str(s.status()),'volume_mm3':s.volume() if str(s.status())=='Error.NoError' else None})
required={r['part'] for r in C['checks'] if r['after']['status']=='Error.NoError'}
assert all(r['status']=='Error.NoError' for r in checks if r['part'] in required)
pickle.dump(rawD,src.open('wb'))
report={'source_model_sha256':R['source_model_sha256'],'proposal_sha256':hashlib.sha256(proposal.read_bytes()).hexdigest(),'source_triangle_multiset_unchanged':True,'applied_changes':len(added),'registry_total':len(R['changes']),'checks':checks,'coincident_same_label_occurrences':equivalent_origins,'geometry_changed':False,'production_release':False}
(H/(sys.argv[2] if len(sys.argv)>2 else 'post_end_face_audit.json' if 'physical_sheet_checks' in C else 'native_plane_face_audit.json' if 'native_planes' in C else 'support_contact_face_audit.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SUPPORT_FACE_LABELS_APPLIED',len(added),'registry',len(R['changes']),flush=True)
for r in checks:print(r['part'],r['status'],r['volume_mm3'],flush=True)
