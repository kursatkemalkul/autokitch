"""Measure24 lower-support joints in the actual mesh and current timeline.

Source-specified tapped6mm caps use their actual4.2mm core bore; it is not
reinterpreted as a clearance hole. No weld strength/fixture release is given.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np
H=Path(__file__).resolve().parent
P=pickle.load((H/'k_parca.pkl').open('rb'))['P'];D=pickle.load((H/'plan_k_full.pkl').open('rb'))
source=H.parent/'k71_lower.json';joins=json.loads(source.read_text(encoding='utf-8'))['connections']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert D['source_parts_sha256']==sha(H/'k_parca.pkl')
def end(a):return max([D['GOR'][a]]+[r[1] for r in D['HAR'][a]])
def measure(name,centre,axis,radius):
 v=P[name]['V']-centre;axial=v@axis;q=v-np.outer(axial,axis);r=np.linalg.norm(q,axis=1)
 selected=v[abs(r-radius)<.02];assert len(selected)>=12,(name,'Missing circular bore/shaft')
 axes=np.where(abs(axis)<.5)[0];uv=np.unique(selected[:,axes],axis=0)
 fit=np.linalg.lstsq(np.column_stack((2*uv,np.ones(len(uv)))),np.sum(uv*uv,axis=1),rcond=None)[0]
 radial=float(np.sqrt(fit[2]+np.sum(fit[:2]**2)))
 return {'axial_interval_mm':[float((selected@axis).min()),float((selected@axis).max())],'axis_error_mm':float(np.linalg.norm(fit[:2])),'radius_fit_error_mm':abs(radial-radius),'bore_or_shaft_vertices':len(selected)}
rows=[]
for j in joins:
 names=j['parts'];base=j['id'].startswith('base_')
 male=names[0];female=names[3] if base else names[1]
 e=np.array([0,1.,0]) if base else np.array([0,-1.,0])
 # Use source receiver centre, with actual source circular surfaces to fit it.
 v=P[female]['V'];centre=(v.min(0)+v.max(0))/2
 if base:
  # Odd-sided nut outer hex tessellation is not its shaft centre.
  tag=j['id'].split('_');centre[0]=float(tag[1]);centre[2]=-float(tag[2])+float(tag[3])
 else:
  tag=j['id'].split('_');centre[0]=float(tag[1])+float(tag[3]);centre[2]=-float(tag[2])
 # h3_sac_v1.pem_saplama explicitly models nominal M5 shaft radius
 # as2.5-.03mm; use that declared proxy instead of relaxing fit tolerance.
 # h3_sac_v1.vida uses nominal diameter*.98 for the rendered shaft.
 mm=measure(male,centre,e,2.47 if base else 2.45);fm=measure(female,centre,e,2.5 if base else 2.1)
 mi=mm['axial_interval_mm'];fi=fm['axial_interval_mm'];engagement=max(0,min(mi[1],fi[1])-max(mi[0],fi[0]));protrusion=mi[1]-fi[1]
 host=names[1] if base else names[2];hm=measure(host,centre,e,2.75)
 completion=max(end(n) for n in names)
 if base:load='k71_istasyon_rafi'
 else:load=min((a for a in P if a.startswith(('k72_itici_taban_','k72_bant_ayak_flansi_'))),key=end)
 loaded=end(load)
 passed=engagement>=5-.02 and .8-.02<=protrusion<=2.4+.02 and max(mm['axis_error_mm'],fm['axis_error_mm'],hm['axis_error_mm'],mm['radius_fit_error_mm'],fm['radius_fit_error_mm'],hm['radius_fit_error_mm'])<.02 and completion<loaded
 row={'id':j['id'],'male':male,'female':female,'female_type':'ISO10511 nut' if base else 'source-defined tapped6mm AISI304 cap,4.2mm core','male_measurement':mm,'female_measurement':fm,'clearance_hole_measurement':hm,'measured_engagement_mm':engagement,'measured_protrusion_mm':protrusion,'measured_protrusion_threads':protrusion/.8,'all_joint_parts_seated_seconds':completion,'supported_station_load':load,'supported_station_load_seated_seconds':loaded,'passed':bool(passed)}
 rows.append(row);print('LOWER_JOIN',j['id'],row['passed'],'engagement',engagement,'protrusion',protrusion,'load_margin',loaded-completion,flush=True)
report={'source_parts_sha256':sha(H/'k_parca.pkl'),'source_plan_sha256':sha(H/'plan_k_full.pkl'),'source_join_definitions_sha256':sha(source),'scope':'24 lower-support base/cap joints only; no full-station release','checks':rows,'passed':all(r['passed'] for r in rows),'unresolved':[r['id'] for r in rows if not r['passed']],'production_release':False}
(H/'lower_connection_measured_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert report['passed']
