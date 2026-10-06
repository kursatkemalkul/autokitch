"""Append measured clip welding to the common-player plan, before cables.
All previous motion/geometry remains unchanged; new joints are source-bound.
"""
from pathlib import Path
import pickle,json,gzip,hashlib,numpy as np
H=Path(__file__).resolve().parent;folder=H.parent/'electrical_clip_weld_candidate'
parent=H/'plan_k_head_supported.pkl';D=pickle.loads(parent.read_bytes())
cache=H/'k_parca_clip_verified.pkl';P=pickle.loads(cache.read_bytes())['P']
payload=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
torch=json.loads((folder/'torch_access_audit.json').read_text())
assert torch['passed_all_preassembly_envelopes']
assert torch['candidate_geometry_sha256']==hashlib.sha256((folder/'geometry.json.gz').read_bytes()).hexdigest()
def end(a):return max([D['GOR'][a]]+[h[1] for h in D['HAR'][a]])
parts=set(payload['parts']);assert set(P)==set(D['P'])|parts
def faces(part):
 q=np.round(np.asarray(part['V'])[np.asarray(part['F'])],4).reshape(-1,9)
 return np.array(sorted(map(tuple,q)),dtype=np.float64)
for a in D['P']:assert np.array_equal(faces(D['P'][a]),faces(P[a])),a
t=max(end(j['clip']) for j in payload['joins'])+.01
wire_times=[D['GOR'][a] for a in D['P'] if D['P'][a].get('dugum','').startswith(('ELK_K__kablo','ELK_K_TARTI__kablo'))]
assert wire_times
records=[]
for join in payload['joins']:
 clip,host=join['clip'],join['host'];assert end(host)<end(clip)<t
 start=t
 for seam in join['seams']:
  D['P'][seam]=P[seam];D['HAR'][seam]=[];D['GOR'][seam]=t;D['MF'][seam]=dict(buyu=[t,t+.6])
  D['OLAY'].append([t,'Kablo kelepçesi ayağı: sürekli TIG kaynak; kablo henüz takılmadı. Dikiş temizlenir ve pasive edilir.'])
  records.append(dict(type='continuous_clip_foot_TIG',part=seam,carriers=[clip,host],t0=t,t1=t+.6,torch_access_report='electrical_clip_weld_candidate/torch_access_audit.json'))
  t+=.6
 warning='UYARI · GEÇİCİ DESTEK: '+clip+' montaj kıskacıyla tutulur; dört çevresel dikiş bitmeden bırakılmaz.'
 D['OLAY'].append([end(clip),warning]);D['OLAY'].append([t,clip+': dört sürekli kaynak tamamlandı, montaj kıskacı bırakılır.'])
 D['TEMPORARY_SUPPORTS'].append(dict(id='clip_foot_hold_'+clip,parts=[clip],t0=end(clip),t1=t,warning=warning,
  release_after_welds=join['seams'],fixture_geometry_verified=False,temporary_support_is_not_a_permanent_join=True))
assert t<min(wire_times)
D['FABRICATION_JOINS'].extend(records);D['OLAY'].sort(key=lambda r:r[0]);D['production_release']=False
dest=H/'plan_k_clip_full.pkl';pickle.dump(D,dest.open('wb'))
# Bind exact full source triangle multiset through the existing shared checker.
source=H/'k_son_kaynak.py';code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_clip_full.pkl'),('k_bil.pkl','k_bil_clip.pkl'),('k_bil.json','k_bil_clip.json'),
 ('k_parca.pkl','k_parca_clip_verified.pkl'),('plan_source_binding_audit.json','clip_plan_source_binding_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
r=dict(parent_plan_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),source_plan_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
 old_geometry_and_motion_unchanged=True,new_source_bound_welds=records,clip_welds_complete_seconds=t,first_cable_install_seconds=min(wire_times),
 temporary_fixture_geometry_verified=False,delta_collision_checked=False,remaining_connection_records=203,production_release=False)
(H/'clip_integration_audit.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CLIP_INTEGRATED',len(parts),'WELDS; SOURCE_BOUND; BEFORE_CABLES',t,min(wire_times),flush=True)
