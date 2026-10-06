"""Add three continuous real fillet rings between our rods and adaptor.

Native rod facet phase is retained at the weld roots. Supplier yoke and
housing are unchanged; their mounting and the adaptor layer fastening are
still open. No production release is claimed.
"""
from pathlib import Path
source = Path(__file__).with_name('cut_head_mount_candidate.py')
ns = dict(__file__=str(source), __name__='cut_head_definition')
code = source.read_text(encoding='utf-8').split("r = ns['audit_clamps'](")[0]
exec(compile(code,str(source),'exec'),ns)
np, PM, cq, mf = (ns[k] for k in ('np','PM','cq','mf'))
P, origin = ns['P'], ns['ORIGIN']
helper = ns['ns']
destination = helper['OUT']/'cut_head_weld_candidate'
destination.mkdir(exist_ok=True)
helper['DEST']=destination
records=[]
for index,(x,z) in enumerate(ns['centres']):
    name='ara_dikme_'+str(index)
    v=P[name]['V']
    top=float(v[:,1].max())
    ring=np.unique(v[np.abs(v[:,1]-top)<.001][:,[0,2]],axis=0)
    ring=ring[np.linalg.norm(ring-np.array([x,z]),axis=1)>7.8]
    ring=ring[np.argsort(np.arctan2(ring[:,1]-z,ring[:,0]-x))]
    n=len(ring); assert n>=8
    # Offset each true polygon edge by2mm, intersecting adjacent offset lines.
    edges=np.roll(ring,-1,axis=0)-ring
    outward=np.column_stack((edges[:,1],-edges[:,0]))
    outward/=np.linalg.norm(outward,axis=1)[:,None]
    outer=[]
    for i in range(n):
        normals=np.vstack((outward[i-1],outward[i]))
        outer.append(ring[i]+np.linalg.solve(normals,np.array([2.,2.])))
    outer=np.asarray(outer)
    verts=np.vstack((np.column_stack((ring[:,0],np.full(n,top),ring[:,1])),
                     np.column_stack((outer[:,0],np.full(n,top),outer[:,1])),
                     np.column_stack((ring[:,0],np.full(n,top-2.),ring[:,1]))))
    faces=[]
    for i in range(n):
        j=(i+1)%n
        for a,b,c,d in ((i,j,j+n,i+n),(i+n,j+n,j+2*n,i+2*n),(i+2*n,j+2*n,j,i)):
            faces.extend(((a,b,c),(a,c,d)))
    import trimesh
    mesh=trimesh.Trimesh(vertices=verts,faces=np.asarray(faces),process=False)
    mesh.fix_normals()
    assert mesh.is_watertight and mesh.volume>0
    weld=PM.solid(mesh.vertices,mesh.faces,origin)
    item=ns['make_piece']('k79_kafa_dikme_TIG_'+str(index),weld,2.)
    item['tur']='kaynak';item['mal']='kaynak'
    ns['pieces'].append(item)
    records.append({'rod':name,'adaptor':'kafa_adaptoru','weld':item['ad'],
        'process':'Continuous TIG141 ER308LSi; finished fillet leg2mm; passivate',
        'root_y_mm':top,'native_outline_segments':n,
        'continuous_closed_root':True,'leg_mm':2.,'throat_mm':2./2**.5,
        'weld_volume_mm3':float(weld.volume()),
        'bench_sequence':'Weld rods to lower6mm adaptor before upper4mm layer or supplier yoke is fitted; finish and passivate; bolt6+2mm head stack from below',
        'supplier_body_modified':False,'torch_access_checked':False})
r=helper['audit_clamps'](ns['pieces'],ns['joins'],ns['repairs'],ns['holes'])
r.update(continuous_rod_welds=records,stock_layers=ns['stock'],
         adaptor_layer_fastening_verified=False,supplier_yoke_mount_verified=False,
         whole_head_connected=False,production_release=False)
(destination/'audit.json').write_text(ns['json'].dumps(helper['clean'](r),indent=2),encoding='utf-8')
helper['sys'].stdout.flush()
helper['os']._exit(0 if r['passed_geometry_and_stacks'] else 2)
