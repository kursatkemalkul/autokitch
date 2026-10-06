"""Bind step78 deterministic output, exact label rebind and 67 sheet solids."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;O=H.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=O/'chain73/A/hat3_v10s.glb';b=O/'chain73/B/hat3_v10s.glb';A=read(a.with_suffix('.json'));B=read(b.with_suffix('.json'))
rebind=read(H/'step78_ownership_rebind_audit.json');closed=read(H/'physical_sheet_closure_audit78.json');encoded=read(H/'current_sheet_encoding_audit78.json');other=read(O/'k78_unrelated_geometry_audit.json');registry=read(H/'surface_ownership_registry78.json')
assert sha(a)==sha(b)==A['output_sha256']==B['output_sha256']==registry['source_model_sha256']
assert rebind['passed'] and rebind['raw_parts_sha256']==sha(H/'k_parca78_raw.pkl')
assert closed['source_encoding_sha256']==sha(H/'current_sheet_bending78.json') and closed['passed_closure_only'] and closed['physical_sheet_count']==67
assert encoded['passed'] and other['passed']
report={'step':78,'source_model_sha256':sha(a),'two_runs_byte_identical':True,'raw_source_triangles':rebind['raw_triangles'],'source_face_label_rebind_passed':True,'maximum_recompression_vertex_distance_mm':rebind['maximum_recompression_vertex_distance_mm'],'physical_sheets':67,'closed_sheets':67,'native_bend_encoding_endpoint_passed':True,'unrelated_nodes_compared':other['compared_nodes'],'unrelated_nodes_unchanged':True,'registry_sha256':sha(H/'surface_ownership_registry78.json'),'encoded_sheets_sha256':sha(H/'current_sheet_bending78.json'),'rebound_parts_sha256':sha(H/'k_parca78_verified.pkl'),'new_source_montage_path_checked':False,'connection_release':False,'manufacturing_release':False,'registered_chain_step':False,'production_release':False,'k_completed':False,'u_started':False}
(H/'step78_source_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SOURCE78_BOUND',report['source_model_sha256'],'closed',67,'release',False,flush=True)
