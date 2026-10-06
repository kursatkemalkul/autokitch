"""Four explicitly documented factory interfaces; no waiver for external mounts."""
from pathlib import Path
import pickle,json,hashlib
H=Path(__file__).resolve().parent;path=H/'plan_k_catalog_full.pkl';D=pickle.loads(path.read_bytes())
previous=H/'catalog_specific_mount_evidence.json';r=json.loads(previous.read_text())
assert r['source_plan_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
open_names={x['part'] for x in r['remaining_unresolved']}
requested=[
 ('DGRF_sensor_rayi','DGRF-C-63-125_govde','https://www.festo.com/media/catalog/204215_documentation.pdf','2025/03 p6 type code R; p16 modular ordering notes: A/R present for piston diameters32..63. Current native drive is63mm; rail is delivered with that drive. This does not cover our incorrectly named SMT-8M proximity sensors or their mounting kit.'),
 ('PulsaJet_M8_soketi_9','PulsaJet_AAB10000AUH-104210-VIFC','https://www.spray.com/-/media/dam/industrial/usa/technical-documentation/product-data-sheet/10000auh-104210.pdf','DS10000AUH-104210 revision4 defines integral three-pole male M8 receptacle. Only the integral socket is accepted, not the cable strain relief or our nozzle mount.'),
 ('itici_X_blok_-755','itici_X_ray_-755','https://hiwin.com/products/linear-guideways/','MG miniature guideways operate by recirculating rolling elements between profiled rail and bearing block. Native K assembly supplies this rail/block pair together; attachment of rail to frame and block to our bridge still requires real fasteners.'),
 ('itici_X_blok_-645','itici_X_ray_-645','https://hiwin.com/products/linear-guideways/','Same explicitly named second delivered rail/block pair; no acceptance of its external mounting.')]
rows=[]
for child,unit,doc,note in requested:
 assert child in open_names and child in D['P'] and unit in D['P']
 assert D['HAR'][child]==D['HAR'][unit] and D['GOR'][child]==D['GOR'][unit]
 rows.append({'part':child,'supplier_unit':unit,'supplier_document':doc,'evidence':note,'same_motion_and_visibility_as_native_delivered_unit':True,'external_unit_mount_verified':False})
accepted={x['part'] for x in rows}
out={'source_parts_sha256':r['source_parts_sha256'],'source_plan_sha256':r['source_plan_sha256'],'source_model_sha256':r['source_model_sha256'],'previous_report_sha256':hashlib.sha256(previous.read_bytes()).hexdigest(),'explicit_factory_interface_records':rows,'resolved_named_records':len(rows),'remaining_unresolved':[x for x in r['remaining_unresolved'] if x['part'] not in accepted],'remaining_count':r['remaining_count']-len(rows),'whole_station_connections_verified':False,'production_release':False}
(H/'catalog_supplier_interfaces.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('EXPLICIT_FACTORY_INTERFACES',len(rows),'REMAINING',out['remaining_count'])
