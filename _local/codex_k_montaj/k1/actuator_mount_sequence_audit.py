"""Check four bottom clamps before any supported pusher mechanism is installed."""
from pathlib import Path
import json,pickle,hashlib
H=Path(__file__).resolve().parent
path=H/'plan_k_actuator_full.pkl'
D=pickle.load(path.open('rb'))
definition=json.loads((H.parent/'belt_bottom_mount_candidate/audit.json').read_text(encoding='utf-8'))
def end(a):return max([D['GOR'][a]]+[h[1] for h in D['HAR'][a]])
frame=end('bant_yan_-421')
rows=[]
for j in definition['joints']:
    washer=end(j['washer']);screw=end(j['screw'])
    loads=[a for a in D['P'] if a.startswith(('itici_X_','itici_Z_')) or a=='itici_sabit_plaka']
    # Arrival rather than spawn time: a part may be travelling separately
    # while the frame is being fixed; it cannot be seated before tightening.
    first=min(end(a) for a in loads)
    row={'id':j['id'],'frame_seated_seconds':frame,'washer_seated_seconds':washer,
         'screw_seated_seconds':screw,'first_subsequent_mechanism_seated_seconds':first,
         'load_margin_seconds':first-screw,'passed':frame<=washer<=screw<=first}
    rows.append(row)
report={'source_model_sha256':D['source_model_sha256'],
        'source_plan_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'scope':'four station clamps before subsequent pusher loads; bench fixtures are separate',
        'checks':rows,'passed':len(rows)==4 and all(r['passed'] for r in rows),
        'fixtures_verified':False,'production_release':False}
(H/'actuator_mount_sequence_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('BOTTOM_CLAMP_LOAD_ORDER',report['passed'],flush=True)
assert report['passed']
