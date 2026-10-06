"""Measure catalog bolt length, mounting datum and real blind-bore depth."""
from pathlib import Path
import pickle,json,hashlib
import numpy as np
H=Path(__file__).resolve().parent;path=H/'k_parca_catalog_verified.pkl';P=pickle.loads(path.read_bytes())['P']
scope=json.loads((H.parent/'actuator_catalog_fastener_candidate/source_scope_audit.json').read_text())
assert scope['verified_parts_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
recipe=json.loads((H.parent/'actuator_catalog_fastener_candidate/audit.json').read_text())
plate=P['DGRF_baglanti_plakasi']['V'];body=P['DGRF-C-63-125_govde']['V'];seat=float(plate[:,2].min());entry=float(body[:,2].min());rows=[]
for j in recipe['joins']:
 a=j['id'];x,y,_=j['center_mm'];v=P[a]['V'];tip=float(v[:,2].max());r=np.linalg.norm(body[:,:2]-np.array([x,y]),axis=1)
 ring=body[(r>=4.8)&(r<=5.1)]
 assert len(ring)>=6,(a,len(ring))
 bottom=float(ring[:,2].max());q=ring[np.abs(ring[:,2]-bottom)<.001]
 A=np.column_stack((2*q[:,0],2*q[:,1],np.ones(len(q))))
 fit=np.linalg.lstsq(A,(q[:,:2]*q[:,:2]).sum(1),rcond=None)[0]
 center_error=float(np.linalg.norm(fit[:2]-[x,y]));radius=float(np.sqrt(fit[2]+fit[0]**2+fit[1]**2))
 length=tip-seat;engagement=tip-entry;bottom_clearance=bottom-tip;depth=bottom-entry
 passed=abs(length-35.)<.001 and abs(depth-24.)<.001 and engagement>=10. and bottom_clearance>=1.5 and center_error<=.01 and abs(radius-5.)<=.001
 rows.append({'part':a,'nominal_standard':'ISO4762 M10x35 A2-70','measured_length_mm':length,'measured_mounting_stack_mm':entry-seat,'measured_blind_bore_depth_mm':depth,'measured_engagement_mm':engagement,'measured_bottom_clearance_mm':bottom_clearance,'measured_bore_center_error_mm':center_error,'measured_nominal_thread_representation_radius_mm':radius,'passed':passed,'thread_geometry_representation':'nominal cylindrical thread, not helically meshed teeth'})
r={'source_model_sha256':scope['output_sha256'],'source_parts_sha256':scope['verified_parts_sha256'],'checks':rows,'passed':all(x['passed'] for x in rows),'tool_access_checked':False,'whole_station_connections_verified':False,'production_release':False}
(H/'catalog_fastener_measurements.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('CATALOG_BOLT_MEASUREMENTS',r['passed'],[(x['part'],round(x['measured_engagement_mm'],3),round(x['measured_bottom_clearance_mm'],3)) for x in rows])
assert r['passed']
