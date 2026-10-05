"""Apply surface ownership records to named parts, preserving every source triangle."""
from pathlib import Path
import json,pickle,numpy as np,hashlib
H=Path(__file__).resolve().parent
D=pickle.load((H/'k_parca.pkl').open('rb'));P=D['P'];audit=json.loads((H/'surface_ownership_audit.json').read_text(encoding='utf-8'))
def fingerprint(P):
 Q=np.concatenate([p['V'][p['F']] for p in P.values()]);q=np.sort(Q.reshape(len(Q),9).view('f8'),axis=0) # supplemented below by exact per-face bytes
 return sorted(q.tobytes() for q in Q)
before=fingerprint(P);out={a:[] for a in P}
move={}
for r in audit['changes']:move[(r['from'],r['triangle'])]=r['to']
for a,p in P.items():
 for i,q in enumerate(p['V'][p['F']]):out.setdefault(move.get((a,i),a),[]).append(q)
for a,qs in out.items():
 if not qs:raise AssertionError('Empty source part '+a)
 if a not in P:P[a]=dict(m='sac',tur='sac',ac='K sol elektrik geçişi: 40×40×1,5 mm kaynaklı kapama yaması (kaynak/elk3/e4.py)',dugum='K_GOVDE__kabuk',kpk=False)
 V,F=np.unique(np.array(qs).reshape(-1,3),axis=0,return_inverse=True);P[a]['V']=V;P[a]['F']=F.reshape(-1,3)
assert before==fingerprint(P),'Triangle multiset changed'
backup=H/'k_parca_before_surface.pkl'
if not backup.exists():backup.write_bytes((H/'k_parca.pkl').read_bytes())
pickle.dump(D,(H/'k_parca.pkl').open('wb'))
(H/'surface_ownership_apply_audit.json').write_text(json.dumps({'parts':len(P),'triangles':sum(len(p['F']) for p in P.values()),'reassigned':len(move),'geometry_modified':False,'exact_triangle_multiset_preserved':True,'unresolved_owner_candidates':len(audit['unknown'])},indent=2),encoding='utf-8')
print('Surface ownership applied, exact source triangles preserved:',len(move))
