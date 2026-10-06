"""Validate new actual cable/duct meshes and flush lid modules from native GLB."""
from pathlib import Path
import json
import numpy as np
import trimesh
from shapely.geometry import Polygon
from inspect_scene import read
ROOT=Path(__file__).resolve().parents[3];A=ROOT/'otonom/hat3d/robot-integrated-v23'
f=json.loads((A/'floor_plan.json').read_text());g,bin=read(ROOT/'_local/codex_robot_v23/combined_native.glb')
targets={'ROBOT23_'+d['name'] for d in f['duct_specs']}|{'ROBOT23_'+n for n in f['cables']}|{'ROBOT23_UR_HIGH_FLEX_ARABA'}
errors=[];rows=[]
def acc(i):
    a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];n={'VEC3':3,'SCALAR':1}[a['type']];dt={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']]
    return np.frombuffer(bin,dtype=dt,count=a['count']*n,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,n)
for n in g['nodes']:
    if n.get('name') not in targets:continue
    p=g['meshes'][n['mesh']]['primitives'][0];m=trimesh.Trimesh(acc(p['attributes']['POSITION']),acc(p['indices']).reshape(-1,3),process=False)
    ok=bool(m.is_watertight and m.is_winding_consistent and abs(m.volume)>1e-12)
    if not ok:errors.append(n['name']+' open/nonmanifold/zero volume')
    rows.append({'name':n['name'],'watertight':bool(m.is_watertight),'consistent_winding':bool(m.is_winding_consistent),'volume_m3':float(abs(m.volume))})
if len(rows)!=len(targets):errors.append('Missing actual meshes')
for typ in ['lids','walls']:
    polys=[Polygon(p['outer'],p['holes']) for p in f[typ]]
    for i,p in enumerate(polys):
        if not p.is_valid:errors.append(typ+' invalid polygon')
        for q in polys[i+1:]:
            if p.intersection(q).area>1e-10:errors.append(typ+' overlapping module')
report={'version':23,'cable_duct_meshes':rows,'butt_cut_wall_and_lid_modules_checked':True,'errors':errors,'passed':not errors,'scope':'closed swept new cable/duct geometry, winding, wall/lid non-overlap; full moving robot collision not certified'}
(A/'geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'meshes':len(rows),'errors':errors,'passed':not errors}));raise SystemExit(bool(errors))
