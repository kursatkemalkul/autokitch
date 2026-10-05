"""Check closed physical sheet topology, aggregating GLB fragments of one sheet."""
from pathlib import Path
import json,pickle,numpy as np,manifold3d as mf
H=Path(__file__).resolve().parent;P=pickle.load((H/'k_parca.pkl').open('rb'))['P'];records=json.loads((H/'current_sheet_bending.json').read_text(encoding='utf-8'))['sheets'];rows=[]
for r in records:
 names=r['target_parts'];q=np.concatenate([P[a]['V'][P[a]['F']] for a in names]);V,idx=np.unique(np.round(q.reshape(-1,3),3),axis=0,return_inverse=True);F=idx.reshape(-1,3);F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
 edges=np.sort(np.concatenate((F[:,[0,1]],F[:,[1,2]],F[:,[2,0]])),axis=1);u,c=np.unique(edges,axis=0,return_counts=True);bad=c!=2
 solid=mf.Manifold(mf.Mesh(vert_properties=V.astype(np.float32),tri_verts=F.astype(np.uint32)));ok=solid.status()==mf.Error.NoError and not solid.is_empty()
 row={'name':r['name'],'parts':names,'triangles':len(F),'non_two_face_edges':int(bad.sum()),'manifold_status':str(solid.status()),'closed':bool(ok),'diagnostic_grid_mm':.001}
 if bad.any():row['edge_examples_mm']=V[u[bad][:8]].tolist()
 rows.append(row)
print('PHYSICAL_SHEETS',len(rows),'closed',sum(r['closed'] for r in rows),'open',[(r['name'],r['non_two_face_edges']) for r in rows if not r['closed']])
(H/'sheet_topology_audit.json').write_text(json.dumps({'checks':rows,'passed':all(r['closed'] for r in rows),'production_release':False},indent=2),encoding='utf-8')
