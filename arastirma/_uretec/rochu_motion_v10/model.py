from pathlib import Path
import json,struct,numpy as np
from scipy.spatial.transform import Rotation
H=Path(__file__).parent;ROOT=H.parents[2];OUT=ROOT/'otonom/hat3d/rochu-v9-four'
SOURCE=ROOT/'otonom/hat3d/rochu-sabit-v1'
NATIVE=SOURCE/'analysis_native.glb'
if not NATIVE.exists():NATIVE=ROOT.parent/'codex-rochu-sabit-v1/otonom/hat3d/rochu-sabit-v1/analysis_native.glb'
C=np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],float)
def trs(n):
 if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
 m=np.eye(4);m[:3,:3]=Rotation.from_quat(n.get('rotation',[0,0,0,1])).as_matrix()@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m
class Model:
 def __init__(self):
  b=NATIVE.read_bytes();n=struct.unpack_from('<I',b,12)[0];self.j=json.loads(b[20:20+n]);self.bin=memoryview(b)[28+n:];self.parents={c:i for i,n in enumerate(self.j['nodes']) for c in n.get('children',[])};self.world={};self.shapes=[]
  for i,n in enumerate(self.j['nodes']):
   if 'mesh' not in n:continue
   for p in self.j['meshes'][n['mesh']]['primitives']:
    v=self.acc(p['attributes']['POSITION']).astype(float);f=self.acc(p['indices']).reshape(-1,3).astype(np.int32) if 'indices' in p else np.arange(len(v)).reshape(-1,3)
    used,remap=np.unique(f,return_inverse=True);v=v[used];f=remap.reshape(-1,3)
    w=self.matrix(i);points=v@w[:3,:3].T+w[:3,3]
    material=self.j.get('materials',[])[p.get('material',0)];color=material.get('pbrMetallicRoughness',{}).get('baseColorFactor',[.6,.6,.6,1])
    self.shapes.append(dict(id=i,name=n.get('name',''),vertices=v,faces=f,matrix=w,world=points,bounds=np.array([points.min(0),points.max(0)]),color=color))
 def acc(self,i):
  a=self.j['accessors'][i];v=self.j['bufferViews'][a['bufferView']];dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1',5122:'<i2'}[a['componentType']];size={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];dt=np.dtype(dtype)
  return np.ndarray((a['count'],size),dtype=dtype,buffer=self.bin,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',size*dt.itemsize),dt.itemsize))
 def matrix(self,i):
  if i not in self.world:self.world[i]=(self.matrix(self.parents[i]) if i in self.parents else np.eye(4))@trs(self.j['nodes'][i])
  return self.world[i]
class Kin:
 def __init__(self):
  self.data=json.loads((OUT/'rig.json').read_text());self.edges=self.data['edges'];self.arm=self.data['arm_joints']
  for e in self.edges:
   e['a']=np.array(e['a']);e['bi']=np.linalg.inv(np.array(e['b']))
   if e['name']=='RobotMountJoint':e['a'][1,3]-=.1
   if e['name']=='GroundMountJoint':e['a'][1,3]-=.5
 def worlds(self,q,rail):
  angles=dict(zip(self.arm,q));world={};pending=list(self.edges)
  while pending:
   for e in pending[:]:
    if e['parent'] and e['parent'] not in world:continue
    t=np.eye(4)
    if e['name']=='RailJoint':t[0,3]=rail-self.data['rail_min']
    elif e['type']=='PhysicsRevoluteJoint':t[:3,:3]=Rotation.from_rotvec(np.eye(3)['XYZ'.index(e['axis'])]*angles.get(e['name'],0)).as_matrix()
    world[e['child']]=world.get(e['parent'],np.eye(4))@e['a']@t@e['bi'];pending.remove(e)
  return {k:C@v for k,v in world.items()}
if __name__=='__main__':
 m=Model();result=[]
 for s in m.shapes:
  if any(x in s['name'] for x in ['ACICI','DONER__TABLA','PRODUCT_']):result.append(dict(name=s['name'],bounds=s['bounds'].tolist()))
 (OUT/'source_bounds.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2)[:7500])
