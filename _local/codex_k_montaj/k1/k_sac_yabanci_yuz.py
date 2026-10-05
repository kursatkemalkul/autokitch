"""Diagnose foreign-owned faces in open sheet bounds, without relabelling.

Coincident sheet contact faces can belong to two distinct physical solids.
A one-to-one triangle ownership change cannot fix both; no face is invented.
"""
from pathlib import Path
import pickle,json,hashlib
from collections import Counter
import numpy as np
H=Path(__file__).resolve().parent
src=H/'k_parca.pkl';P=pickle.load(src.open('rb'))['P']
closure=json.loads((H/'physical_sheet_closure_audit.json').read_text(encoding='utf-8'))
sheets=json.loads((H/'current_sheet_bending.json').read_text(encoding='utf-8'))['sheets']
open_names=set(closure['open_sheets']);bounds={};tris={}
for name,p in P.items():
 q=p['V'][p['F']];tris[name]=q;bounds[name]=(q.min((0,1)),q.max((0,1)))
rows=[]
for r in sheets:
 if r['name'] not in open_names:continue
 v=np.asarray(r['vertices']);lo=v.min(0);hi=v.max(0);owners=set(r['target_parts']);foreign=[]
 for name,(a,b) in bounds.items():
  if name in owners or np.any(b<lo-.001) or np.any(a>hi+.001):continue
  q=tris[name];mask=np.all(q.min(1)>=lo-.001,1)&np.all(q.max(1)<=hi+.001,1)
  ids=np.flatnonzero(mask)
  if len(ids):foreign.append({'owner':name,'triangle_indices':ids.tolist(),'count':len(ids)})
 rows.append({'sheet':r['name'],'fragments':sorted(owners),'foreign_faces_in_bounds':foreign,
              'classification':'candidate_only_requires_native_boundary_proof'})
# Exact minimal case: the 40x40 patch has ten exterior triangles. Its two
# remaining contact triangles currently occur in the adjoining wall label.
name='k_e4_sol_yama_40x40';q=tris[name];lo,hi=bounds[name]
wall='sol_sac_urun_girisi';w=tris[wall]
mask=np.all(w.min(1)>=lo-.001,1)&np.all(w.max(1)<=hi+.001,1)
contact=w[mask]
assert len(q)==10 and len(contact)==2
assert np.all(abs(contact[:,:,0]-lo[0])<.001)
all_faces=Counter(hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest() for qq in tris.values() for t in qq)
proof={'sheet':name,'sheet_triangle_count':10,'contact_owner':wall,'contact_triangle_count':2,
       'source_occurrences':[all_faces[hashlib.sha256(np.asarray(t,dtype='<f8').tobytes()).hexdigest()] for t in contact],
       'contact_face_axis':'X','contact_face_coordinate_mm':float(lo[0]),
       'native_stock_bounds_mm':[lo.tolist(),hi.tolist()],
       'safe_relabel_proven':False,'requires_native_two_solid_boundary_check':True}
out={'source_parts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
     'source_closure_sha256':hashlib.sha256((H/'physical_sheet_closure_audit.json').read_bytes()).hexdigest(),
     'checks':rows,'patch_contact_proof':proof,'geometry_changed':False,'ownership_changed':False,
     'manufacturing_release':False}
(H/'sheet_foreign_face_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('FOREIGN_FACE_DIAGNOSTIC',len(rows),'open sheets; patch shared face requires native proof',flush=True)
