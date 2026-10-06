"""Exact flat-stock encoding for the four permitted cutting-head layers.
No bend is invented for a flat plate. Source holes/countersinks remain exact;
secondary machining and complete station assembly are separate release gates.
"""
from pathlib import Path
import pickle,json,hashlib,numpy as np
H=Path(__file__).resolve().parent
source=H/'k_parca_head_verified.pkl';P=pickle.loads(source.read_bytes())['P']
scope=json.loads((H.parent/'cut_head_yoke_candidate/source_scope_audit.json').read_text())
assert scope['full_triangle_rebind_passed'] and scope['verified_parts_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
base=json.loads((H/'current_sheet_bending_catalog.json').read_text());assert base['passed']
records={r['name']:r for r in base['sheets']};checks=[]
for name,t in [('kafa_plakasi_8',6.),('k79_kafa_ust_plaka_2',2.),('kafa_adaptoru',6.),('k79_kafa_adaptor_ust_plaka_4',4.)]:
 p=P[name];v=p['V'];f=p['F'];lo=v.min(0);hi=v.max(0)
 assert p['tur']=='sac' and abs(hi[1]-lo[1]-t)<.001
 matrix=np.eye(4);matrix[:3,:3]=np.array([[1,0,0],[0,0,1],[0,-1,0]])
 matrix[:3,3]=[lo[0],lo[1],hi[2]]
 local=(v-matrix[:3,3])@matrix[:3,:3]
 restored=local@matrix[:3,:3].T+matrix[:3,3]
 error=float(np.linalg.norm(restored-v,axis=1).max())
 assert error<=.01 and local[:,2].min()>=-.001 and local[:,2].max()<=t+.001
 records[name]={'name':name,'root':matrix.tolist(),'source_offset':[0,0,0],'t':t,'vertices':v.tolist(),'triangles':f.tolist(),'encoded_vertices':[{'panel':0,'point':q.tolist()} for q in local], 'bends':[],'order':[],'classification_surface_tolerance_mm':.01,'unclassified_vertices':[],'folded_endpoint_max_error_mm':error,'endpoint_passed':True,'target_parts':[name]}
 checks.append({'name':name,'thickness_mm':t,'vertices':len(v),'triangles':len(f),'endpoint_error_mm':error,'flat_stock':True,'bends_required':False,'actual_source_holes_preserved':True,'secondary_operations':'Laser exact faceted outer outline and central/clearance holes; countersink lower plates to the measured M8 seating depth4.4mm; deburr and passivate','machining_release':False})
report={'source_model_sha256':scope['output_sha256'],'source_parts_sha256':scope['verified_parts_sha256'],'checks':checks,'physical_sheets':len(records),'passed_endpoint_and_stock':True,'manufacturing_release':False,'production_release':False}
(H/'current_sheet_bending_head.json').write_text(json.dumps({'sheets':list(records.values()),'passed':True,'source_parts_sha256':scope['verified_parts_sha256'],'production_release':False},separators=(',',':')),encoding='utf-8')
(H/'head_sheet_encoding_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('HEAD_FLAT_STOCK',len(records),'new',len(checks),'maximum_endpoint_mm',max(r['endpoint_error_mm'] for r in checks),flush=True)
