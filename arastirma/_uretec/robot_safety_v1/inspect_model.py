"""Read-only inspection of the exact remote step61 model; no machine edits."""
from pathlib import Path
import subprocess, gzip, json, struct, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
REPO=ROOT.parents[2]/'AUTOKITCH'
OUT=ROOT/'_local/codex_robot_safety_v2'
OUT.mkdir(parents=True,exist_ok=True)
def blob(ref,p):
    return subprocess.check_output(['git','-c',f'safe.directory={REPO.as_posix()}','-C',str(REPO),'show',f'{ref}:{p}'])
raw=gzip.decompress(blob('origin/claude/standart-makine','_local/claude_son_yerel/hat3_v10c.glb.gz'))
(OUT/'hat3_v10c.glb').write_bytes(raw)
n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);binary=raw[28+n:]
def acc(i):
    a=g['accessors'][i];v=g['bufferViews'][a['bufferView']]
    assert 'extensions' not in v, 'Compressed mesh needs decoder'
    k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    off=v.get('byteOffset',0)+a.get('byteOffset',0)
    return np.ndarray((a['count'],k),dtype=dt,buffer=binary,offset=off,
      strides=(v.get('byteStride',np.dtype(dt).itemsize*k),np.dtype(dt).itemsize))
rows=[]
for node in g['nodes']:
    name=node.get('name','')
    if not any(s in name.upper() for s in ['QR','ROBOT','HUCRE','HÜCRE','KAPI']):continue
    if 'mesh' not in node:continue
    for p in g['meshes'][node['mesh']]['primitives']:
        if 'POSITION' not in p['attributes']:continue
        x=acc(p['attributes']['POSITION']);idx=acc(p['indices']).ravel();x=x[np.unique(idx)]
        rows.append({'node':name,'local_min_mm':(x.min(0)*1000).tolist(),'local_max_mm':(x.max(0)*1000).tolist(),
          'node_transform':{k:node[k] for k in ['translation','rotation','scale','matrix'] if k in node},
          'triangles':len(idx)//3,'extras':p.get('extras',{})})
(OUT/'model_inspection.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
metadata={'source_branch':'claude/standart-makine','step':61,
  'source_commit':subprocess.check_output(['git','-c',f'safe.directory={REPO.as_posix()}',
      '-C',str(REPO),'rev-parse','origin/claude/standart-makine'],text=True).strip(),
  'source_sha256':hashlib.sha256(raw).hexdigest(),'nodes':len(g['nodes']),'bytes':len(raw),
  'customer_doors':[r['node'] for r in rows if r['node'].startswith('QR_GOZLER__on_seffaf__GOZ_')],
  'robot_cell_door_present':False,'qr_layout':'2 columns x 6 rows',
  'machine_modified':False,'pending_decisions':['QR 2x6 versus robot QR 3x4','cell door location']}
(OUT/'source.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(metadata,ensure_ascii=False))
