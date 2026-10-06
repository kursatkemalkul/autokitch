"""Add explicit temporary-support warning/release events without changing motion.
Writes a separate plan, leaving any live CCD source immutable. The warning is
mandatory even for short intervals. Fixture geometry remains a separate gate.
"""
from pathlib import Path
import pickle,json,hashlib
H=Path(__file__).resolve().parent;source=H/'plan_k_head_full.pkl';dest=H/'plan_k_head_supported.pkl'
D=pickle.loads(source.read_bytes())
def arrival(a):return max([D['GOR'][a]]+[h[1] for h in D['HAR'][a]])
rows=[]
for name,members,bolts,description in [
 ('head_upper_stock_hold',['k79_kafa_adaptor_ust_plaka_4','kafa_adaptoru'],['k79_kafa_yoke_M8x25_'+str(i) for i in range(4)],'Üst4mm ara plaka ve kaynaklı adaptör montaj fikstüründe tutulur; dört M8x25 sıkılmadan destek bırakılmaz.'),
 ('head_lower_cassette_hold',['kafa_plakasi_8','k79_kafa_ust_plaka_2'],['k79_kafa_alt_M8x20_'+str(i) for i in range(3)],'Alt6mm+üst2mm kafa kaseti geçici montaj fikstüründe tutulur; üç M8x20 sıkılmadan destek bırakılmaz.')]:
 t0=min(arrival(a) for a in members);t1=max(arrival(a) for a in bolts)
 assert t1>t0
 rows.append({'id':name,'parts':members,'t0':t0,'t1':t1,'release_after_fasteners':bolts,'warning':description,'fixture_geometry_verified':False,'temporary_support_is_not_a_permanent_join':True})
 D['OLAY'].append([t0,'UYARI · GEÇİCİ DESTEK: '+description])
 D['OLAY'].append([t1,'Geçici destek bırakılır: '+', '.join(bolts)+' bağlantıları tamamlandı.'])
D['TEMPORARY_SUPPORTS']=rows;D['OLAY'].sort(key=lambda r:r[0])
D['support_event_parent_plan_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
pickle.dump(D,dest.open('wb'))
original=pickle.loads(source.read_bytes());check=pickle.loads(dest.read_bytes())
fields=['P','HAR','GOR','MF','FRAMES','ROT','ISTISNA','HARIC_PLAN','HARIC_NEDEN','FABRICATION_JOINS']
import numpy as np
def exact(a,b):
 if isinstance(a,np.ndarray):return isinstance(b,np.ndarray) and a.dtype==b.dtype and np.array_equal(a,b)
 if isinstance(a,dict):return isinstance(b,dict) and a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
 if isinstance(a,(list,tuple)):return type(a)==type(b) and len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
 return type(a)==type(b) and bool(a==b)
assert all(exact(original[k],check[k]) for k in fields)
report={'source_model_sha256':D['source_model_sha256'],'source_parts_sha256':D['source_parts_sha256'],'parent_plan_sha256':D['support_event_parent_plan_sha256'],'supported_plan_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'identical_geometry_and_motion_fields':fields,'geometry_and_motion_unchanged':True,'support_records':rows,'full_ccd_parent_report':'full_ccd_plan_k_head_full.json','full_ccd_parent_must_pass_before_inheritance':True,'fixture_geometry_verified':False,'manufacturing_release':False,'production_release':False}
(H/'head_support_event_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('HEAD_SUPPORT_EVENTS',len(rows),'GEOMETRY_AND_MOTION_UNCHANGED',flush=True)
