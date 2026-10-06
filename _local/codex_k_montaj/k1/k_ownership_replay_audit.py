"""Replay all current ownership rows from raw cache; verify source faces exactly."""
from pathlib import Path
import json,pickle,hashlib
from collections import Counter
import numpy as np
from k_yuz_etiket import apply
H=Path(__file__).resolve().parent;rawpath=H/'k_parca77_raw.pkl';currentpath=H/'k_parca.pkl';registry=H/'surface_ownership_registry.json'
R=json.loads(registry.read_text(encoding='utf-8'));raw=pickle.load(rawpath.open('rb'))['P'];current=pickle.load(currentpath.open('rb'))['P']
def faces(p):return Counter(hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest() for t in p['V'][p['F']])
before=Counter()
for p in raw.values():before.update(faces(p))
replay=apply(raw);after=Counter();rows=[]
assert set(replay)==set(current)
for a in sorted(replay):
 predicted=faces(replay[a]);actual=faces(current[a]);assert predicted==actual,a
 after.update(actual);rows.append({'part':a,'source_triangles':sum(actual.values()),'replay_exact':True})
assert before==after
report={'source_model_sha256':R['source_model_sha256'],'raw_cache_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'current_parts_sha256':hashlib.sha256(currentpath.read_bytes()).hexdigest(),'registry_sha256':hashlib.sha256(registry.read_bytes()).hexdigest(),'registry_rows':len(R['changes']),'parts':len(rows),'source_triangles':sum(before.values()),'checks':rows,'source_face_multiset_preserved_exactly':True,'current_labels_replay_exactly':True,'geometry_modified':False,'production_release':False}
(H/'ownership_replay_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('OWNERSHIP_REPLAY_EXACT',len(rows),sum(before.values()),len(R['changes']),flush=True)
