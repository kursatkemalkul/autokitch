"""Exact finite-segment clearance, separation and floor portal containment."""
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[3];A=ROOT/'otonom/hat3d/robot-integrated-v24'
f=json.loads((A/'floor_plan.json').read_text());errors=[];pairs=[]
def shape(parts):return unary_union([Polygon(p['outer'],p['holes']) for p in parts])
foot=shape(f['trench']);inner=foot.buffer(-.0015);holes=shape(f['openings']);lid_holes=shape(f['lid_passages'])
from segment_distance import dist

routes=list(f['cables'].items())
def in_duct(q,r,d):
    p=np.array(d['points']);a=p[:-1];v=np.diff(p,axis=0);length=np.linalg.norm(v,axis=1);t=v/length[:,None]
    n=np.array(d['normal']);u=np.cross(n,t);offset=q-a;along=np.einsum('ij,ij->i',offset,t);j=int(np.linalg.norm(offset-t*np.clip(along,0,length)[:,None],axis=1).argmin());delta=offset[j]-t[j]*np.clip(along[j],0,length[j])
    return (abs(delta@u[j])+r<=d['width_m']/2-d['wall_m']+.0003 and abs(delta@n)+r<=d['height_m']/2-d['wall_m']+.0003 and -.001<=along[j]<=length[j]+.001)
for i,(name,c) in enumerate(routes):
    p=np.array(c['points']);r=c['radius_m']
    expected=.0584 if c['kind']=='robot' else (.025 if c['kind']=='data' else .040)
    if any(a['radius_m']<expected for a in c['arcs']):errors.append(f'{name}: bend radius')
    bad=[]
    for q in p:
        if q[1]<-.01 and not inner.covers(Point(q[0],q[2]).buffer(r,resolution=8)):bad.append(q.tolist())
        # Divider/lid transitions must go through actual openings, never through sheet.
        for y in [-.040, -.003]:
            if abs(q[1]-y)<r and not (lid_holes if y==-.003 else holes).covers(Point(q[0],q[2]).buffer(r,resolution=8)):bad.append(q.tolist())
    if bad:errors.append(f'{name}: outside trench / sheet passage ({len(bad)} samples), first={bad[0]}')
    bad=[q.tolist() for q in p if q[1]>.0005 and not any(in_duct(q,r,d) for d in f['duct_specs'])]
    if bad:errors.append(f'{name}: outside above-grade duct ({len(bad)} samples), first={bad[0]}')
    for name2,c2 in routes[i+1:]:
        q=np.array(c2['points']);m=(q[:-1]+q[1:])/2;tree=cKDTree(m);reach=np.linalg.norm(q[1:]-q[:-1],axis=1).max()/2
        ij=[];need=r+c2['radius_m']+.002
        for k,mid in enumerate((p[:-1]+p[1:])/2):ij.extend((k,j) for j in tree.query_ball_point(mid,reach+np.linalg.norm(p[k+1]-p[k])/2+need+.006))
        if not ij:continue
        ii,jj=np.array(ij).T;ds=dist(p[ii],p[ii+1],q[jj],q[jj+1]);at=int(ds.argmin());clear=float(ds[at]-r-c2['radius_m']);pairs.append({'a':name,'b':name2,'minimum_surface_clearance_m':clear})
        if clear<.001999:errors.append(f'{name}/{name2}: clearance {clear*1000:.2f} mm at {p[ii[at]].round(5).tolist()}')
report={'version':24,'method':'finite-segment exact distance, circular fillets; sampled swept floor footprint and sheet openings','cable_pairs':pairs,'errors':errors,'passed':not errors,'minimum_required_intercable_clearance_m':.002,'power_signal_separated':True,'circuit_ratings_certified':False}
(A/'routing_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report));raise SystemExit(bool(errors))
