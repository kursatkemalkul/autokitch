"""Withdraw coincident context-face candidates rejected by full sheet topology.

Bounded native face agreement alone cannot disambiguate coincident F/context
surfaces. Do not steal them from the source assembly to close a K surface.
"""
from pathlib import Path
import json,pickle,hashlib
from collections import Counter
import numpy as np
from k_yuz_etiket import apply
H=Path(__file__).resolve().parent;path=H/'surface_ownership_registry.json'
R=json.loads(path.read_text(encoding='utf-8'));proposal=json.loads((H/'all_owner_native_proposals.json').read_text(encoding='utf-8'))
assert len(proposal['proposed_changes'])==96
targets={(r['triangle_sha256'],r['to']):r['from'] for r in proposal['proposed_changes']}
withdrawn=[];new=[]
for row in R['changes']:
 key=(row['triangle_sha256'],row['to'])
 if key not in targets:new.append(row);continue
 old=dict(row);destination=targets[key]
 assert destination in ('cevre_F','cevre_diger')
 if row['from']!=destination:new.append(dict(row,to=destination))
 withdrawn.append(old)
assert len(withdrawn)==96,len(withdrawn)
before_sha=hashlib.sha256(path.read_bytes()).hexdigest();R['changes']=new
path.write_text(json.dumps(R,indent=2),encoding='utf-8')
raw=pickle.load((H/'k_parca77_raw.pkl').open('rb'))
before=Counter(t.tobytes() for p in raw['P'].values() for t in p['V'][p['F']])
raw['P']=apply(raw['P']);after=Counter(t.tobytes() for p in raw['P'].values() for t in p['V'][p['F']]);assert before==after
pickle.dump(raw,(H/'k_parca.pkl').open('wb'))
report={'rejected_proposal_sha256':hashlib.sha256((H/'all_owner_native_proposals.json').read_bytes()).hexdigest(),'registry_before_sha256':before_sha,'registry_after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'withdrawn_changes':withdrawn,'reason':'Coincident context surfaces matched old native planes but regress physical wall topology after T-junction resolution. Retain original context ownership.','source_triangles_unchanged':True,'production_release':False}
(H/'context_face_rejection_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CONTEXT_CANDIDATES_WITHDRAWN',len(withdrawn),'registry',len(new),flush=True)
