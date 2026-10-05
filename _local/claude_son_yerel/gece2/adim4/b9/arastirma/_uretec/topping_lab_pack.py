"""Whole-hopper, collision-screened initial food. Run using CadQuery Python.

No outlet emitter. These are initial rigid proxies, not calibrated bulk food.
Shelf layers are merely a repeatable loading condition; PhysX settles them.
Surface sampling is conservative (<=0.8 mm cover), backed by exact CAD
point classification. Borderline boxes are rejected, never squeezed to fit.
"""
from pathlib import Path
import importlib, json, hashlib, time
import numpy as np
from scipy.spatial import cKDTree
import cadquery as cq
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
from OCP.TopAbs import TopAbs_IN,TopAbs_ON

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/topping_lab_v1'

def surface_samples(shape):
    vv,ff=shape.copy().tessellate(.08,.12)
    tri=np.array([v.toTuple() for v in vv])[np.array(ff)]
    done=[]
    # Longest-edge bisection: centroid is <0.8 mm from any triangle point.
    while len(tri):
        edge=np.stack([tri[:,1]-tri[:,0],tri[:,2]-tri[:,1],tri[:,0]-tri[:,2]],axis=1)
        ll=np.sum(edge*edge,axis=2);take=ll.max(1)<=.8**2
        if take.any():done.append(tri[take].mean(1))
        tri=tri[~take];idx=ll[~take].argmax(1)
        more=[]
        for e in range(3):
            t=tri[idx==e]
            if not len(t):continue
            a,b,c=t[:,e],t[:,(e+1)%3],t[:,(e+2)%3];mid=(a+b)/2
            more.extend([np.stack([a,mid,c],1),np.stack([mid,b,c],1)])
        tri=np.concatenate(more) if more else np.empty((0,3,3))
    pts=np.concatenate(done)
    # Longest edge <= .8: centroid covering radius <= .534. Keeping one
    # original point per .2-mm voxel adds <= .347, still below .9-mm margin.
    _,idx=np.unique(np.floor(pts/.2).astype(np.int32),axis=0,return_index=True)
    return pts[idx]

def prepare(product):
    cfg=dict(kasar=('kasar_cad_v14','kasar_kabi_v14',1257.5,1100.,.50,8800.),
             sucuk=('sucuk_cad_v7','sucuk_kaseti_v7',1472.5,1000.,.60,2800.))[product]
    mod,folder,xc,rho,bulk,stock=cfg;old=importlib.import_module(mod)
    src=ROOT/'arastirma/3_TOPPING'/folder/'step'
    inner=old.kesit(0,old.Y_DOLUM).extrude(old.ZFI-old.ZBI).translate((0,0,old.ZBI)).val()
    parts=[];disp={};hashes={}
    for file in sorted(src.glob('*.step')):
        if file.stem in ('helezon_TEK_PARCA','tasima_tapasi'):continue
        new=ROOT/'arastirma/3_TOPPING'/f'{product}_v2'/'cad'/(file.stem+('_v15.step' if product=='kasar' else '_v2.step'))
        file=new if new.exists() else file
        shape=cq.importers.importStep(str(file)).val()
        v=shape.intersect(inner).Volume(tol=1e-7)
        if v>.02:
            disp[file.stem]=v;parts.append((file.stem,shape))
            hashes[file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
    free=(inner.Volume(tol=1e-7)-sum(disp.values()))/1e6
    print('PACK_GEOMETRY',product,free,'L',len(parts),'obstacles',flush=True)
    surfaces=[];boxes=[]
    for name,shape in parts:
        pts=surface_samples(shape);surfaces.append(pts)
        b=shape.BoundingBox();boxes.append(([b.xmin,b.ymin,b.zmin],[b.xmax,b.ymax,b.zmax]))
        print('SURFACE',name,len(pts),flush=True)
    tree=cKDTree(np.concatenate(surfaces));boxes=np.array(boxes)
    classifiers=[[BRepClass3d_SolidClassifier(s.wrapped) for s in shape.Solids()] for _,shape in parts]
    inner_classifier=BRepClass3d_SolidClassifier(inner.wrapped)
    def inside(classifier,p):
        classifier.Perform(gp_Pnt(*p),1e-6)
        return classifier.State() in (TopAbs_IN,TopAbs_ON)
    # Generate layers with bounded dimensions; each actual dimension remains
    # variable. Half-width is queried from the exact CAD profile at layer base.
    rng=np.random.default_rng(7);points=[];dims=[];masses=[];rejected=0
    y=old.CY-old.RT+1.;gap=.9
    while y+3 < old.Y_DOLUM-1.:
        # Small layer-height bins avoid wasting a full maximum-height envelope.
        dh=float(rng.uniform(3.5,4.8) if product=='kasar' else rng.uniform(6.5,9.5))
        layerh=dh if product=='kasar' else dh
        if y+layerh>old.Y_DOLUM-1.:break
        lo,hi=0.,old.RB
        for _ in range(18):
            mid=(lo+hi)/2
            if inside(inner_classifier,(mid,y,0)):lo=mid
            else:hi=mid
        hw=lo-1.;z=old.ZBI+1.
        while z+3<old.ZFI-1.:
            depth=float(rng.uniform(8.,12.) if product=='kasar' else dh)
            if z+depth>old.ZFI-1.:break
            x=-hw
            while x+3<hw:
                if product=='kasar':
                    d=np.array([rng.triangular(3.,4.,5.),dh,depth-rng.uniform(0.,2.)])
                else:d=np.full(3,dh-rng.uniform(0.,.5))
                if x+d[0]>hw:break
                p=np.array([x+d[0]/2,y+d[1]/2,z+d[2]/2])
                half=d/2+.9
                ids=tree.query_ball_point(p,float(np.linalg.norm(half)))
                hit=bool(ids) and np.any(np.all(np.abs(tree.data[ids]-p)<=half,axis=1))
                if not hit:
                    possible=np.flatnonzero(np.all(p>=boxes[:,0],axis=1)&np.all(p<=boxes[:,1],axis=1))
                    hit=any(inside(cl,p) for i in possible for cl in classifiers[i])
                if not hit:
                    points.append(p);dims.append(d);masses.append(float(np.prod(d)*rho*1e-9))
                else:rejected+=1
                x+=d[0]+gap
            z+=depth+gap
        y+=layerh+gap
        print('PACK_LAYER',product,round(y,2),len(points),round(sum(masses)*1000,1),'g',flush=True)
    points=np.array(points);dims=np.array(dims);masses=np.array(masses)
    # Sort by height so fill modes select a genuine bottom-to-top charge.
    order=np.argsort(points[:,1],kind='stable');points,dims,masses=points[order],dims[order],masses[order]
    w=(points+np.array([xc,260.,-362.5]))*.001
    w=np.column_stack([w[:,0],-w[:,2],w[:,1]])
    wd=dims[:,[0,2,1]]*.001
    # Verification independent of surface-query packing: sample exact CAD box
    # intersections, including every accepted box nearest an obstacle.
    distance=tree.query(points)[0];checkids=np.unique(np.r_[np.argsort(distance)[:120],rng.choice(len(points),min(120,len(points)),replace=False)])
    maximum=0.
    for i in checkids:
        p,d=points[i],dims[i];b=cq.Solid.makeBox(*d,cq.Vector(*(p-d/2)))
        for k in np.flatnonzero(np.all(p+d/2>=boxes[:,0],axis=1)&np.all(p-d/2<=boxes[:,1],axis=1)):
            ov=b.intersect(parts[k][1]).Volume(tol=1e-6);maximum=max(maximum,ov)
            assert ov<.001,(product,int(i),parts[k][0],ov)
    report=dict(product=product,free_volume_l=free,fill_line_local_y_mm=old.Y_DOLUM,
        fill_line_world_z_m=(old.Y_DOLUM+260)/1000,bulk_density_g_ml_assumption=bulk,
        nominal_full_g=free*bulk*1000,two_day_stock_g=stock,packed_max_g=float(masses.sum()*1000),
        initial_packed_bulk_g_ml=float(masses.sum())/free,
        count=len(points),rejected_boxes=rejected,exact_CAD_sample_count=len(checkids),max_sample_overlap_mm3=maximum,
        surface_cover_mm=.8,exclusion_margin_mm=.9,particle_gap_mm=gap,source_hashes=hashes,
        assumptions=['Rigid food, no adhesion/crushing.','Layered initial charge, then physical settling.',
        'Kasar 3-5 x 6-12 x 3.5-4.8 mm; sucuk 6-9.5 mm variable. Distribution is an assumption.',
        '100% means this physical initial charge up to the safe fill line; settled level may change.',
        'Nominal bulk-density mass is a comparison, not a forced particle mass.'])
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/f'{product}_packing.npz',points=w,dimensions=wd,mass_kg=masses)
    (OUT/f'{product}_packing.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PACK_READY',json.dumps(report),flush=True)
    assert report['packed_max_g']>=stock,'The two-day stock does not fit this initial charge'

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('product',choices=['kasar','sucuk','all']);a=p.parse_args()
    for name in (['kasar','sucuk'] if a.product=='all' else [a.product]):prepare(name)
