from pathlib import Path
import struct,json,hashlib
import numpy as np
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[2]
for name in ('modul_E.glb','hat_v85.glb'):
    raw=(root/'otonom/hat3d'/name).read_bytes()
    length,typ=struct.unpack_from('<II',raw,12)
    doc=json.loads(raw[20:20+length])
    nodes=doc['nodes']; result=[]
    for anim in doc.get('animations',[]):
        groups={}
        for ch in anim['channels']:
            target=ch['target']; n=nodes[target['node']].get('name','')
            if any(g in n for g in ('VAC_Y','NEST')) and target['path']=='translation':
                a=doc['accessors'][anim['samplers'][ch['sampler']]['output']]
                view=doc['bufferViews'][a['bufferView']]
                start=28+length+view.get('byteOffset',0)+a.get('byteOffset',0)
                values=struct.unpack_from('<'+'f'*(a['count']*3),raw,start)
                lo=[min(values[i::3]) for i in range(3)]; hi=[max(values[i::3]) for i in range(3)]
                assert max(hi[i]-lo[i] for i in range(3))>.01,(name,n,lo,hi)
                groups[n]={'min':lo,'max':hi,'count':a['count']}
        result.append({'name':anim.get('name'),'new_groups':groups})
    assert result and all(r['new_groups'] for r in result), (name,result)
    print(name,len(raw),'bytes',json.dumps(result,ensure_ascii=False))

def geometry(path):
    raw=path.read_bytes(); length=struct.unpack_from('<I',raw,12)[0]
    d=json.loads(raw[20:20+length]); arrays=[]
    for mesh in d['meshes']:
        for p in mesh['primitives']:
            for index in [p['attributes']['POSITION']]:
                a=d['accessors'][index]; v=d['bufferViews'][a['bufferView']]
                start=28+length+v.get('byteOffset',0)
                values=struct.unpack_from('<'+'f'*(a['count']*3),raw,start+a.get('byteOffset',0))
                arrays.append(np.array(values).reshape(-1,3))
    return d['nodes'],arrays
for module in 'ABCDKRS':
    rel=Path('otonom/hat3d')/f'modul_{module}.glb'
    n,a=geometry(root/rel); m,b=geometry(root.parent/'codex-kutu-main-v84'/rel)
    assert n==m and len(a)==len(b),module
    delta=max(max(cKDTree(x).query(y)[0].max(),cKDTree(y).query(x)[0].max()) for x,y in zip(a,b))
    bounds=max(max(np.abs(x.min(0)-y.min(0)).max(),np.abs(x.max(0)-y.max(0)).max()) for x,y in zip(a,b))
    print('OTHER_MODULE_TESSELLATION',module,'max vertex difference mm',delta*1000,'bounds difference mm',bounds*1000)
    # Tessellation may choose different vertices on an unchanged curved face.
    # This is an envelope check, not a solid-equivalence proof.
    assert bounds<.0005,(module,bounds)
