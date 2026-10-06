"""Measure12 source72 mounting joints and prove nuts precede station load.

This covers only conveyor/pusher feet. It does not certify supplier mounts,
bench fixtures, weld strength, torque, press tooling or the full station.
"""
from pathlib import Path
import json,pickle,hashlib
import numpy as np
H=Path(__file__).resolve().parent
P=pickle.load((H/'k_parca.pkl').open('rb'))['P']
D=pickle.load((H/'plan_k_full.pkl').open('rb'))
source=H.parent/'k72_mounts.json';joins=json.loads(source.read_text(encoding='utf-8'))['connections']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert D['source_parts_sha256']==sha(H/'k_parca.pkl')
def end(a):return max([D['GOR'][a]]+[r[1] for r in D['HAR'][a]])
def axial_fit(a,c,e,d):
 v=P[a]['V']-c;t=v@e;axes=np.where(abs(e)<.5)[0];uv=v[:,axes];r=np.linalg.norm(uv,axis=1)
 uv=np.unique(uv[abs(r-d/2)<.1],axis=0);assert len(uv)>=5,(a,'Insufficient shaft/bore samples')
 fit=np.linalg.lstsq(np.column_stack((2*uv,np.ones(len(uv)))),np.sum(uv*uv,axis=1),rcond=None)[0]
 radius=float(np.sqrt(fit[2]+np.sum(fit[:2]**2)))
 return {'interval_mm':[float(t.min()),float(t.max())],'axis_error_mm':float(np.linalg.norm(fit[:2])),'circular_fit_residual_mm':float(np.max(abs(np.linalg.norm(uv-fit[:2],axis=1)-radius)))}
rows=[]
for j in joins:
 names=j['parts'];c=np.asarray(j['center_mm']);e=np.asarray(j['axis'],float);d=j['nominal_diameter_mm'];pitch=.8 if d==5 else 1.
 male=names[0];female=names[-1];m=axial_fit(male,c,e,d);n=axial_fit(female,c,e,d)
 mi=m['interval_mm'];ni=n['interval_mm'];engagement=max(0,min(mi[1],ni[1])-max(mi[0],ni[0]));protrusion=mi[1]-ni[1]
 x,_,z=c
 if d==6:hosts=[(f'k72_bant_ayak_flansi_{x}_{z}',6.6)];load='bant_yan_-421'
 else:
  px=4040. if x<4200 else 4360.;pz=-755. if z<-700 else -645.
  hosts=[(f'k72_itici_taban_{px}_{pz}',5.5),(f'k72_itici_ust_plaka_{px}_{pz}',5.5)];load='itici_sabit_plaka'
 holes=[]
 for host,diameter in hosts:
  v=P[host]['V']-c;radial=np.linalg.norm(v-np.outer(v@e,e),axis=1);near=radial[abs(radial-diameter/2)<.02]
  holes.append({'host':host,'hole_diameter_mm':diameter,'circular_wall_vertices':len(near),'maximum_radius_error_mm':float(np.max(abs(near-diameter/2))) if len(near) else None,'passed':len(near)>=12})
 completion=max(end(a) for a in names);loaded=end(load)
 passed=engagement>=d-.02 and pitch-.02<=protrusion<=3*pitch+.02 and max(m['axis_error_mm'],n['axis_error_mm'],m['circular_fit_residual_mm'],n['circular_fit_residual_mm'])<.02 and all(h['passed'] for h in holes) and completion<loaded
 row={'id':j['id'],'male':male,'female':female,'male_measurement':m,'female_measurement':n,'actual_engagement_mm':engagement,'actual_protrusion_mm':protrusion,'actual_protrusion_threads':protrusion/pitch,'host_holes':holes,'all_hardware_seated_seconds':completion,'supported_station_load':load,'supported_station_load_seated_seconds':loaded,'load_after_mount_hardware':completion<loaded,'passed':bool(passed)}
 rows.append(row);print('MOUNT_JOIN',j['id'],row['passed'],'engagement',engagement,'threads',protrusion/pitch,'load_margin',loaded-completion,flush=True)
report={'source_parts_sha256':sha(H/'k_parca.pkl'),'source_plan_sha256':sha(H/'plan_k_full.pkl'),'source_join_definitions_sha256':sha(source),'scope':'12 conveyor/pusher mounting bolts only; no full station release','checks':rows,'passed':all(r['passed'] for r in rows),'unresolved':[r['id'] for r in rows if not r['passed']],'production_release':False}
(H/'mount_connection_measured_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert report['passed']
