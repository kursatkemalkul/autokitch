"""Remove abandoned external QR/sink services without changing station geometry."""
from pathlib import Path
import json,struct,hashlib,sys
import numpy as np
from inspect_scene import read
ROOT=Path(__file__).resolve().parents[3]
src=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'_local/claude_son_yerel/hat3_v10l.glb.gz'
g,b=read(src);initial=bytes(b);chunks=[b];offset=len(b);removed=[];trimmed=[]
def append_index(values):
 global offset
 if offset%4:chunks.append(bytes(4-offset%4));offset+=(4-offset%4)
 data=np.asarray(values,dtype='<u4').tobytes();vi=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(data),'target':34963});chunks.append(data);offset+=len(data)
 ai=len(g['accessors']);g['accessors'].append({'bufferView':vi,'componentType':5125,'count':len(values),'type':'SCALAR'});return ai
def acc(i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dt={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];n={'VEC3':3,'SCALAR':1}[a['type']]
 return np.frombuffer(initial,dtype=dt,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
roots=g['scenes'][g.get('scene',0)]['nodes'];keep=[]
for ni in roots:
 n=g['nodes'][ni];name=n.get('name','')
 if name.startswith(('TEZGAH_','DUZ_TEZGAH','QR_','ELK_QR','ELK_ZEMIN','ROBOT_UR10E','ZEMIN_DOSEME')):
  removed.append(name);continue
 # These nodes combine station wiring with the now abandoned external QR runs.
 if name.startswith(('ELK_ANA_HAT','ELK_ZINCIR','ELK_IC')) and 'mesh' in n:
  for pi,p in enumerate(g['meshes'][n['mesh']]['primitives']):
   v=acc(p['attributes']['POSITION']);f=acc(p['indices']).reshape(-1,3)
   live=np.ptp(v[f],axis=1).max(axis=1)>1e-9
   discard=(v[f][:,:,2].mean(axis=1)>.12)&live
   if discard.any():p['indices']=append_index(f[~discard].reshape(-1));trimmed.append({'name':name,'primitive':pi,'removed_triangles':int(discard.sum())})
 keep.append(ni)
g['scenes'][g.get('scene',0)]['nodes']=keep
g['buffers']=[{'byteLength':(offset+3)&~3}]
rawbin=b''.join(chunks);rawbin+=bytes((-len(rawbin))%4)
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
raw=struct.pack('<5I',0x46546c67,2,28+len(j)+len(rawbin),len(j),0x4e4f534a)+j+struct.pack('<2I',len(rawbin),0x004e4942)+rawbin
target=ROOT/'_local/codex_robot_v22/source_cleaned.glb';target.write_bytes(raw)
report={'input':str(src.name),'input_gzip_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(raw).hexdigest(),'removed_nodes':removed,'trimmed_external_services':trimmed,'original_binary_prefix_preserved':rawbin[:len(initial)]==initial,'machine_station_vertex_positions_changed':False,'cut_region':'external service triangle centroids world z > 0.12 m; named ELK_ANA_HAT/ELK_ZINCIR/ELK_IC only'}
(ROOT/'otonom/hat3d/robot-integrated-v22/cleanup.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'removed_nodes':len(removed),'trimmed_groups':len(trimmed),'bytes':len(raw),'geometry_preserved':report['original_binary_prefix_preserved']}))
