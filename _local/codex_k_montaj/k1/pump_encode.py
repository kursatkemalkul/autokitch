"""Reuse native bend encoding; add actual flat oil mounting stock only.

Current triangle surfaces remain unchanged. Underside pockets and countersinks
are annotated secondary operations; endpoint closure does not certify machining.
"""
from pathlib import Path
import sys,pickle,json,gzip,hashlib
import numpy as np
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
U=ROOT/'arastirma/_uretec/codex/k_montaj';sys.path.insert(0,str(U))
from bend_encode import *
from current_cad import factory_from_source
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
path=H/'k_parca_pump_verified.pkl';P=pickle.loads(path.read_bytes())['P']
source=H.parent/'oil_pump_clamp_candidate'
scope=json.loads((source/'source_scope_audit.json').read_text(encoding='utf-8'))
assert scope['full_triangle_rebind_passed'] and scope['verified_parts_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
base=json.loads((H/'current_sheet_bending_oil_load.json').read_text(encoding='utf-8'))
assert base['passed']
records={r['name']:r for r in base['sheets']}
recipe=json.loads(gzip.decompress((source/'geometry.json.gz').read_bytes()))
factory=factory_from_source(K,OUT)
native={s.ad:s for s in factory.SAC}
checks=[];stock=[]
for name in ():
    rec=encode_sheet(native[name],P[name]['V'][P[name]['F']],[4000,0,0],stock_outline=True)
    rec['target_parts']=[name];records[name]=rec
    checks.append({'name':name,'unclassified_vertices':len(rec['unclassified_vertices']),
                   'endpoint_error_mm':rec['folded_endpoint_max_error_mm'],'passed':rec['endpoint_passed']})
for name,r in recipe['parts'].items():
    if r['tur']!='sac':continue
    p=P[name];lo=p['V'].min(0);hi=p['V'].max(0);span=hi-lo
    axis=int(np.argmin(span));t=float(span[axis])
    assert any(abs(t-v)<.001 for v in (2.,3.)),(name,t)
    if axis==0:O=lo;ex=(0,1,0);ey=(0,0,1);w,h=span[1],span[2]
    elif axis==1:O=(lo[0],lo[1],hi[2]);ex=(1,0,0);ey=(0,0,-1);w,h=span[0],span[2]
    else:O=lo;ex=(1,0,0);ey=(0,1,0);w,h=span[0],span[1]
    flat=S.Sac(name,'braket',t=round(t,3),R=1.5*t,birim='K_YAG')
    flat.taban([(0,0),(w,0),(w,h),(0,h)],O=O,ex=ex,ey=ey)
    rec=encode_sheet(flat,p['V'][p['F']],[0,0,0],stock_outline=True)
    rec['target_parts']=[name];records[name]=rec
    secondary=[]
    if name in ('yag_pompa_rafi','yag_pompa_plakasi'):secondary.append('M5 countersinks2.8mm; actual source bores retained')
    if name=='yag_pompa_rafi':secondary.append('Two underside18x18R2 pockets,1.5mm deep, preserve existing air clip coordinates')
    stock.append({'name':name,'thickness_mm':t,'bounds_mm':[lo.tolist(),hi.tolist()],
                  'flat_sheet_bounds_mm':[float(w),float(h)],'secondary_operations':secondary,
                  'machining_verified':False,'holes_from_current_source_preserved':True})
    checks.append({'name':name,'unclassified_vertices':len(rec['unclassified_vertices']),
                   'endpoint_error_mm':rec['folded_endpoint_max_error_mm'],'passed':rec['endpoint_passed']})
report={'source_model_sha256':scope['output_sha256'],'source_parts_sha256':scope['verified_parts_sha256'],
        'checks':checks,'passed':all(r['passed'] for r in checks),'physical_sheets':len(records),
        'secondary_operations_checked':False,'production_release':False}
(H/'current_sheet_bending_pump.json').write_text(json.dumps(clean({'sheets':list(records.values()),
 'passed':report['passed'],'source_parts_sha256':scope['verified_parts_sha256'],
 'production_release':False}),separators=(',',':')),encoding='utf-8')
(H/'pump_sheet_encoding_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(H/'pump_flat_stock_audit.json').write_text(json.dumps({'parts':stock,'production_release':False},indent=2),encoding='utf-8')
print('OIL_LOAD_SHEETS',report['physical_sheets'],'failed',[r for r in checks if not r['passed']],flush=True)
sys.stdout.flush();os._exit(0 if report['passed'] else 2)
