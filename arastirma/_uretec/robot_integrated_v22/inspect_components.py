import sys,json
from pathlib import Path
import numpy as np,trimesh
from inspect_scene import read
g,b=read(sys.argv[1]);out=[]
def acc(i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];typ={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];n={'VEC3':3,'SCALAR':1}[a['type']]
 return np.frombuffer(b,dtype=typ,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
for ni,n in enumerate(g['nodes']):
 if not any(s in n.get('name','') for s in sys.argv[3:]) or 'mesh' not in n:continue
 for pi,p in enumerate(g['meshes'][n['mesh']]['primitives']):
  mesh=trimesh.Trimesh(acc(p['attributes']['POSITION']),acc(p['indices']).reshape(-1,3),process=False)
  mesh.merge_vertices(digits_vertex=6)
  groups=trimesh.graph.connected_components(mesh.face_adjacency,nodes=np.arange(len(mesh.faces)),engine='scipy')
  for ci,faces in enumerate(groups):
   vertices=mesh.vertices[mesh.faces[faces].reshape(-1)]
   out.append({'node':n['name'],'node_id':ni,'primitive':pi,'component':ci,'box':np.round([vertices.min(0),vertices.max(0)],6).tolist(),'faces':len(faces)})
Path(sys.argv[2]).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([r for r in out if r['box'][1][2]>.12],ensure_ascii=False))
