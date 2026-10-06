"""Conservative frame-by-frame mesh bounds of the existing eight robot records."""
from pathlib import Path
import json, mmap, struct, itertools, sys
import numpy as np
from scipy.spatial.transform import Rotation
ROOT=Path(__file__).resolve().parents[3]
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'codex-kanal-birlesim-v23/_local/codex_robot_v23/combined_native.glb'
with SOURCE.open('rb') as f:
    data=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    size=struct.unpack_from('<I',data,12)[0];g=json.loads(data[20:20+size]);base=28+size
    def acc(i):
        a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
        dt={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];item=np.dtype(dt).itemsize
        return np.ndarray((a['count'],n),dtype=dt,buffer=data,offset=base+v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',item*n),item))
    def matrix(n):
        if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
        m=np.eye(4);m[:3,:3]=Rotation.from_quat(n.get('rotation',[0,0,0,1])).as_matrix()@np.diag(n.get('scale',[1,1,1]));m[:3,3]=n.get('translation',[0,0,0]);return m
    def mesh_corners(n,referenced=False):
        if 'mesh' not in n:return np.empty((0,3))
        pts=[]
        for p in g['meshes'][n['mesh']]['primitives']:
            a=g['accessors'][p['attributes']['POSITION']]
            if referenced:
                v=acc(p['attributes']['POSITION']);v=v[acc(p['indices']).reshape(-1)] if 'indices' in p else v
                if len(v):pts.extend(itertools.product(*zip(v.min(axis=0),v.max(axis=0))))
            else:pts.extend(itertools.product(*zip(a['min'],a['max'])))
        return np.array(pts)
    def descend(i,m,referenced=False):
        n=g['nodes'][i];p=mesh_corners(n,referenced);out=[]
        if len(p):out.append(p@m[:3,:3].T+m[:3,3])
        for c in n.get('children',[]):out+=descend(c,m@matrix(g['nodes'][c]),referenced)
        return out
    bodies={i:np.vstack(descend(i,np.eye(4))) for i,n in enumerate(g['nodes']) if n.get('name','').startswith('UR10E_body_') and not n.get('name','').endswith('mesh') and ('mesh' in n or n.get('children'))}
    roots=set(g['scenes'][g.get('scene',0)]['nodes'])
    static=[]
    for i in roots:
        n=g['nodes'][i]
        if n.get('name','').startswith('QR62_'):
            p=mesh_corners(n);p=p@matrix(n)[:3,:3].T+matrix(n)[:3,3]
            if len(p):static.append(p)
    qr=np.vstack(static);records=[];all_max=[];panel_max=[];column_max=[];product_max=[]
    products={i:np.vstack(descend(i,np.eye(4),True)) for i,n in enumerate(g['nodes']) if n.get('name','').startswith(('ROBOT23_PRODUCT_','ROBOT24_PRODUCT_'))}
    for clip in g['animations']:
        if not clip['name'].startswith('siparis_birlesik_'):continue
        ch={(c['target']['node'],c['target']['path']):c['sampler'] for c in clip['channels']}
        xs=[];pxs=[];bounds={}
        for i,corners in bodies.items():
            if (i,'translation') not in ch:continue
            ts=acc(clip['samplers'][ch[(i,'translation')]]['output']);rs=Rotation.from_quat(acc(clip['samplers'][ch[(i,'rotation')]]['output'])).as_matrix()
            p=np.einsum('nij,kj->nki',rs,corners)+ts[:,None,:]
            # Isaac Z-up to main scene Y-up.
            p=p[:,:,[0,2,1]];p[:,:,2]*=-1
            bounds[g['nodes'][i]['name']]=[p.min(axis=(0,1)).tolist(),p.max(axis=(0,1)).tolist()]
            xs.append(float(p[:,:,0].max()))
            # A rotated local bounding box intersection with panel's Y/Z span.
            lo=p.min(axis=1);hi=p.max(axis=1);live=(hi[:,1]>=1.)&(lo[:,1]<=1.7)&(hi[:,2]>=.66)&(lo[:,2]<=1.26)
            if live.any():pxs.append(float(hi[live,0].max()))
            col=(hi[:,1]>=0)&(lo[:,1]<=2.050)&(hi[:,2]>=1.750)&(lo[:,2]<=2.125)
            if col.any():column_max.append(float(hi[col,0].max()))
        for i,corners in products.items():
            if (i,'translation') not in ch:continue
            ts=acc(clip['samplers'][ch[(i,'translation')]]['output']);rs=Rotation.from_quat(acc(clip['samplers'][ch[(i,'rotation')]]['output'])).as_matrix()
            p=np.einsum('nij,kj->nki',rs,corners)+ts[:,None,:];lo=p.min(axis=1);hi=p.max(axis=1)
            product_max.append(float(hi[:,0].max()))
            panel=(hi[:,1]>=1.)&(lo[:,1]<=1.7)&(hi[:,2]>=.66)&(lo[:,2]<=1.26)
            if panel.any():panel_max.append(float(hi[panel,0].max()))
            col=(hi[:,1]>=0)&(lo[:,1]<=2.050)&(hi[:,2]>=1.750)&(lo[:,2]<=2.125)
            if col.any():column_max.append(float(hi[col,0].max()))
        records.append({'clip':clip['name'],'maximum_x_m':max(xs),'maximum_x_in_panel_band_m':max(pxs),'body_bounds':bounds});all_max+=xs;panel_max+=pxs
    maximum=max(all_max);in_panel=max(panel_max)
    wall=np.ceil(max(5.23+.10,5.16+.10,maximum+.10,in_panel+.284+.10,5.07+.16+.05)*100)/100
    out={'method':'Every recorded body/product translation/quaternion frame; conservative transformed accessor bounding boxes','source_native':SOURCE.name,'robot_maximum_x_m':maximum,'product_maximum_x_m':max(product_max),'panel_band_robot_or_product_maximum_x_m':in_panel,'right_wall_inner_x_m':float(wall),'wall_clearance_m':float(wall-max(maximum,max(product_max))),'panel_clearance_m':float(wall-.284-in_panel),'new_qr_column_left_x_m':5.230,'qr_column_clearance_m':float(5.230-max(column_max)),'qr_bounds':[qr.min(axis=0).tolist(),qr.max(axis=0).tolist()],'records':records,'full_path_collision_certified':False}
    (ROOT/'otonom/hat3d/robot-integrated-v24/layout_scan.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))
