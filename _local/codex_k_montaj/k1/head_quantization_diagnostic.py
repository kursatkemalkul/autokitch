from pathlib import Path
import sys,json,hashlib,numpy as np
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[2]/'_local/claude_son_yerel/gece2/cekmece'))
from glb import G
source=H.parent/'cut_head_yoke_candidate/A/hat3_v10zd.glb'
g=G(str(source));missing=json.loads((H/'head_missing_triangle_diagnostic.json').read_text())
ni=g.byname['K_KESICI__sac__KESICI'];M=g.W[ni]
print('M',M.tolist(),flush=True)
result={}
for a,r in missing.items():
 q=np.asarray(r['triangles']);loc=(q/1000-M[:3,3])@np.linalg.inv(M[:3,:3]).T
 quant=loc.astype(np.float32).astype(float)
 world=(quant@M[:3,:3].T+M[:3,3])*1000
 area=np.linalg.norm(np.cross(world[:,1]-world[:,0],world[:,2]-world[:,0]),axis=1)/2
 repeated=np.any(np.stack([np.all(quant[:,0]==quant[:,1],axis=1),np.all(quant[:,1]==quant[:,2],axis=1),np.all(quant[:,2]==quant[:,0],axis=1)]),axis=0)
 result[a]={'count':len(q),'repeated_vertex_count':int(repeated.sum()),'zero_area_count':int((area<=5e-10).sum()),'nonzero_count':int((area>5e-10).sum()),'maximum_area_mm2':float(area.max()),'maximum_vertex_distance_mm':float(np.linalg.norm(world-q,axis=2).max())}
print(result,flush=True)
(H/'head_quantization_diagnostic.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'node_transform':M.tolist(),'parts':result},indent=2),encoding='utf-8')
