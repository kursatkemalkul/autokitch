"""Reapply verified triangle-level naming without changing model geometry."""
from pathlib import Path
import json,hashlib,numpy as np
H=Path(__file__).resolve().parent
def apply(P):
 registry=json.loads((H/'surface_ownership_registry.json').read_text(encoding='utf-8'));moves={}
 for r in registry['changes']:
  a=r['from'];i=r['triangle'];q=P[a]['V'][P[a]['F'][i]]
  if hashlib.sha256(np.asarray(q,dtype='<f8').tobytes()).hexdigest()!=r['triangle_sha256']:raise ValueError('Stale K ownership registry: '+a)
  moves[(a,i)]=r['to']
 out={a:[] for a in P}
 for a,p in P.items():
  Q=p['V'][p['F']]
  for i,q in enumerate(Q):out.setdefault(moves.get((a,i),a),[]).append(q)
 for a,qs in out.items():
  if not qs:raise ValueError('Empty part after ownership: '+a)
  if a not in P:P[a]=dict(m='sac',tur='sac',ac='Sol elektrik geçişi: 40×40×1,5 mm kapama yaması (e4.py)',dugum='K_GOVDE__kabuk',kpk=False)
  V,F=np.unique(np.array(qs).reshape(-1,3),axis=0,return_inverse=True);P[a]['V']=V;P[a]['F']=F.reshape(-1,3)
 return P
