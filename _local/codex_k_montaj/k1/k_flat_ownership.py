"""Separate threaded cap stock from screw surfaces using their native CAD boundaries."""
from pathlib import Path
import sys,json,pickle,hashlib,numpy as np,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from lower_support import *
HERE=Path(__file__).resolve().parent
parts,_,_=build();native={p['ad']:p['sh'] for p in parts}
D=pickle.load((HERE/'k_parca.pkl').open('rb'));P=D['P'];reg=json.loads((HERE/'surface_ownership_registry.json').read_text(encoding='utf-8'));raw=pickle.load((HERE/'k_parca77_raw.pkl').open('rb'))['P'];extra=[];unknown=[]
for a,p in P.items():
 if not a.startswith('k71_disli_ust_kapak_'):continue
 tag=a.replace('k71_disli_ust_kapak_','');candidates=[n for n in native if n.startswith('k71_ust_havsa_'+tag+'_')]+['k71_istasyon_rafi']
 for i,q in enumerate(p['V'][p['F']]):
  points=list(q)+[q.mean(0)]
  if max(native[a].distance(cq.Vertex.makeVertex(*v)) for v in points)<=.015:continue
  match=[n for n in candidates if max(native[n].distance(cq.Vertex.makeVertex(*v)) for v in points)<=.015]
  if len(match)!=1:unknown.append({'from':a,'triangle':i,'candidates':match,'center':q.mean(0).tolist()});continue
  rtri=raw[a]['V'][raw[a]['F']];idx=[j for j,t in enumerate(rtri) if np.array_equal(t,q)];assert len(idx)==1,(a,i,idx)
  extra.append({'from':a,'triangle':idx[0],'to':match[0],'triangle_sha256':hashlib.sha256(np.asarray(q,dtype='<f8').tobytes()).hexdigest()})
print('FLAT_CAP_OWNERSHIP',len(extra),'moves',len(unknown),'unresolved',flush=True)
(HERE/'flat_cap_ownership_audit.json').write_text(json.dumps({'changes':extra,'unresolved':unknown,'passed':not unknown,'geometry_modified':False,'production_release':False},indent=2),encoding='utf-8')
if unknown:sys.stdout.flush();os._exit(2)
reg['changes']+=extra;reg['flat_cap_boundary_changes']=len(extra);(HERE/'surface_ownership_registry.json').write_text(json.dumps(reg,indent=2),encoding='utf-8')
from k_yuz_etiket import apply
rawD=pickle.load((HERE/'k_parca77_raw.pkl').open('rb'));before=sorted(q.tobytes() for p in rawD['P'].values() for q in p['V'][p['F']]);rawD['P']=apply(rawD['P']);after=sorted(q.tobytes() for p in rawD['P'].values() for q in p['V'][p['F']]);assert before==after
pickle.dump(rawD,(HERE/'k_parca.pkl').open('wb'));print('exact source triangles preserved',flush=True);os._exit(0)
