"""Rebind verified labels after step78 without reusing stale triangle indices.

Match original or explicitly repaired source surfaces one-to-one; retain every
new raw source triangle. Unresolved or ambiguous matches forbid application.
Writes separate step78 artifacts, never overwrites the current step77 cache.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,pickle,hashlib,itertools
import numpy as np
from scipy.spatial import cKDTree
H=Path(__file__).resolve().parent
old=pickle.load((H/'k_parca.pkl').open('rb'))['P'];rawD=pickle.load((H/'k_parca78_raw.pkl').open('rb'));raw=rawD['P']
repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']
def key(t):
 q=np.round(t,4);return min(np.roll(q,i,axis=0).tobytes() for i in range(3))
expected=[];lookup=defaultdict(list)
for a,p in old.items():
 q=repairs[a]['vertices'][repairs[a]['triangles']] if a in repairs else p['V'][p['F']]
 for t in q:
  i=len(expected);expected.append((a,t));lookup[key(t)].append(i)
used=set();pending=[];assignments=[];ambiguous=[]
for a,p in raw.items():
 for i,t in enumerate(p['V'][p['F']]):
  candidates=[j for j in lookup.get(key(t),[]) if j not in used]
  if not candidates:pending.append((a,i,t));continue
  labels={expected[j][0] for j in candidates}
  if len(labels)>1:
   candidates=[j for j in candidates if expected[j][0]==a]
   if not candidates:ambiguous.append({'raw_owner':a,'triangle':i,'candidate_labels':sorted(labels)});continue
  j=min(candidates);used.add(j);assignments.append((a,i,expected[j][0],t,0.))
remaining=[j for j in range(len(expected)) if j not in used]
tree=cKDTree([expected[j][1].mean(0) for j in remaining]) if remaining else None
maximum=0.
for a,i,t in pending:
 candidates=[]
 for index in ([] if tree is None else tree.query_ball_point(t.mean(0),.001)):
  j=remaining[index]
  if j in used:continue
  distance=min(float(np.linalg.norm(t-np.roll(expected[j][1],shift,axis=0),axis=1).max()) for shift in range(3))
  if distance<=.001:candidates.append((distance,j))
 labels={expected[j][0] for _,j in candidates}
 if not candidates or (len(labels)>1 and a not in labels):ambiguous.append({'raw_owner':a,'triangle':i,'candidate_labels':sorted(labels),'precision_match':True});continue
 if len(labels)>1:candidates=[r for r in candidates if expected[r[1]][0]==a]
 distance,j=min(candidates);used.add(j);maximum=max(maximum,distance);assignments.append((a,i,expected[j][0],t,distance))
unmatched_expected=[j for j in range(len(expected)) if j not in used]
report={'raw_parts_sha256':hashlib.sha256((H/'k_parca78_raw.pkl').read_bytes()).hexdigest(),'previous_parts_sha256':hashlib.sha256((H/'k_parca.pkl').read_bytes()).hexdigest(),'repair_payload_sha256':hashlib.sha256((H/'topology_repair_proposal.pkl').read_bytes()).hexdigest(),'raw_triangles':sum(len(p['F']) for p in raw.values()),'expected_triangles':len(expected),'matched_triangles':len(assignments),'maximum_recompression_vertex_distance_mm':maximum,'ambiguous':ambiguous,'unmatched_expected_count':len(unmatched_expected),'unmatched_expected_parts':dict(Counter(expected[j][0] for j in unmatched_expected)),'passed':not ambiguous and not unmatched_expected and len(assignments)==len(expected),'production_release':False}
(H/'step78_ownership_rebind_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('REBIND78',report['passed'],len(assignments),'ambiguous',len(ambiguous),'expected_left',len(unmatched_expected),'maximum_mm',maximum,flush=True)
if not report['passed']:raise SystemExit(2)
source=json.loads((H.parent/'chain73/A/hat3_v10s.json').read_text(encoding='utf-8'))
changes=[];out=defaultdict(list)
for a,i,b,t,distance in assignments:
 out[b].append(t)
 if a!=b:changes.append({'from':a,'triangle':i,'to':b,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest()})
P={}
for a,tri in out.items():
 p=dict(old[a]);v,f=np.unique(np.asarray(tri).reshape(-1,3),axis=0,return_inverse=True);p['V']=v;p['F']=f.reshape(-1,3);P[a]=p
assert set(P)==set(old)
rawD['P']=P;pickle.dump(rawD,(H/'k_parca78_verified.pkl').open('wb'))
(H/'surface_ownership_registry78.json').write_text(json.dumps({'source_model_sha256':source['output_sha256'],'changes':changes,'rebound_from_verified_source_labels':True,'passed':True,'production_release':False},indent=2),encoding='utf-8')
