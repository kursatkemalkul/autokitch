"""Refresh step77 face ownership against native sheet coordinates after remeshing."""
from pathlib import Path
import sys,json,pickle,hashlib,collections,numpy as np,os
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from bend_encode import *
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
from current_cad import factory_from_source
D=pickle.load((H/'k_parca77_raw.pkl').open('rb'));P=D['P'];factory=factory_from_source(K,OUT)
sheets={s.ad:s for s in factory.SAC if s.ad in ('arka_sac','ust_sac','sol_sac_urun_girisi','sag_sac_E_penceresi')}
prior=json.loads((H/'step77_ownership_refresh_audit.json').read_text(encoding='utf-8'))
moves={(r['from'],r['triangle']):r['to'] for r in prior['candidate_changes']};unknown=[];fresh=[]
a='arka_sac';q=P[a]['V'][P[a]['F']]
for i,t in enumerate(q):
 if (a,i) in moves:continue
 if encode_sheet(sheets[a],t[None],[4000,0,0])['endpoint_passed']:continue
 targets=[]
 for b,s in sheets.items():
  if b==a:continue
  r=encode_sheet(s,t[None],[4000,0,0],stock_outline=(b=='ust_sac'))
  if r['endpoint_passed']:targets.append(b)
 if len(targets)==1:moves[(a,i)]=targets[0];fresh.append({'from':a,'triangle':i,'to':targets[0]})
 else:unknown.append({'from':a,'triangle':i,'targets':targets,'centroid':t.mean(0).tolist()})
print('NATIVE77 refresh',len(fresh),'new decisions',len(unknown),'unresolved',flush=True)
changes=[]
for (a,i),b in sorted(moves.items()):
 t=P[a]['V'][P[a]['F'][i]];changes.append({'from':a,'triangle':i,'to':b,'triangle_sha256':hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest()})
report={'source_model_sha256':'5c08c6c90a0724360cdc3764a16a6955ea7023989915eb1f51b7c0bce5ad89f4','changes':changes,'native_refresh':fresh,'unresolved':unknown,'passed':not unknown,'production_release':False}
(H/'surface_ownership_registry77.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if unknown:sys.stdout.flush();os._exit(2)
# Use the same verified geometry-preserving naming pipeline; only its registry path differs.
code=(H/'k_yuz_etiket.py').read_text(encoding='utf-8').replace('surface_ownership_registry.json','surface_ownership_registry77.json');ns={'__file__':str(H/'k_yuz_etiket.py')};exec(code,ns)
before=sorted(t.tobytes() for p in P.values() for t in p['V'][p['F']]);P=ns['apply'](P);after=sorted(t.tobytes() for p in P.values() for t in p['V'][p['F']]);assert before==after
pickle.dump(D,(H/'k_parca77_verified.pkl').open('wb'));print('VERIFIED77',len(P),'source triangles preserved',flush=True);os._exit(0)
