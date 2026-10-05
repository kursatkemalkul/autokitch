"""Check each complete CURRENT physical sheet as an oriented manifold solid.
Diagnostic Mesh64 merge tolerance is recorded; original render/source geometry
is never changed. A nonzero closed solid alone is not a manufacturing release.
"""
from pathlib import Path
import json,time,hashlib
import numpy as np
import manifold3d as M
H=Path(__file__).resolve().parent;path=H/'current_sheet_bending.json';D=json.loads(path.read_text(encoding='utf-8'));rows=[];T=time.time()
for r in D['sheets']:
 v=np.asarray(r['vertices'],dtype=np.float64);f=np.asarray(r['triangles'],dtype=np.uint32)
 mesh=M.Mesh64(np.ascontiguousarray(v),np.ascontiguousarray(f),tolerance=.001)
 merged=mesh.merge();solid=M.Manifold(mesh);status=str(solid.status());volume=solid.volume() if status=='Error.NoError' else 0.
 row={'physical_sheet':r['name'],'fragments':r['target_parts'],'vertices':len(v),'triangles':len(f),'analysis_merge_tolerance_mm':.001,'merge_helper_used':bool(merged),'manifold_status':status,'volume_mm3':volume,'closed_nonempty_solid':status=='Error.NoError' and volume>1e-6}
 rows.append(row);print('SHEET_CLOSED',r['name'],status,round(volume,3),flush=True)
report={'source_encoding_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':rows,'physical_sheet_count':len(rows),'passed_closure_only':all(r['closed_nonempty_solid'] for r in rows),'open_sheets':[r['physical_sheet'] for r in rows if not r['closed_nonempty_solid']],'original_geometry_changed':False,'production_release':False,'elapsed_seconds':time.time()-T}
(H/'physical_sheet_closure_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('CLOSURE_COMPLETE',len(rows),'OPEN',report['open_sheets'],flush=True)
