"""Measured limiting TIG tip envelope on the actual preassembled head group."""
import panel_mount_candidate as PM
from lower_support import *
import pickle, hashlib, trimesh
H=OUT/'k1';folder=OUT/'cut_head_yoke_candidate'
source=H/'k_parca_catalog_verified.pkl'
P=pickle.loads(source.read_bytes())['P']
payload=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert payload['source_parts_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
for name,r in payload['parts'].items():
    P[name]={'V':np.asarray(r['V'],float),'F':np.asarray(r['F'],np.int32)}
recipe=json.loads((folder/'audit.json').read_text())
members=['kafa_adaptoru','ara_dikme_0','ara_dikme_1','ara_dikme_2']
meshes={name:trimesh.Trimesh(vertices=P[name]['V'],faces=P[name]['F'],process=False) for name in members}
checks=[]
for record in recipe['continuous_rod_welds']:
    rod=record['rod'];v=P[rod]['V'];top=record['root_y_mm']
    points=np.unique(v[np.abs(v[:,1]-top)<.02][:,[0,2]],axis=0)
    # Top rod outline only: the blind bottom thread does not affect this face.
    center=np.array([v[:,0].max()-8.,(v[:,2].min()+v[:,2].max())/2.])
    points=points[np.linalg.norm(points-center,axis=1)>7.8]
    points=points[np.argsort(np.arctan2(points[:,1]-center[1],points[:,0]-center[0]))]
    cloud=[];radii=[];roots=[]
    for a,b in zip(points,np.roll(points,-1,axis=0)):
        edge=b-a;normal=np.array([edge[1],-edge[0]])/np.linalg.norm(edge)
        axis=np.array([normal[0],-1.,normal[1]])/2**.5
        for u in np.linspace(0.,1.,int(np.ceil(np.linalg.norm(edge)))+1):
            x,z=a+u*edge;root=np.array([x,top,z]);roots.append(root.tolist())
            for s in range(1,51):
                cloud.append(root+s*axis);radii.append(min(6.,.15+.11*s))
    cloud=np.asarray(cloud);radii=np.asarray(radii);local=[]
    for name,mesh in meshes.items():
        _,distance,_=trimesh.proximity.closest_point(mesh,cloud)
        clearance=float(np.min(distance-radii))
        local.append({'part':name,'minimum_surface_clearance_minus_radius_mm':clearance,
                      'sample_count':len(cloud),'passed':clearance>=-.002})
    checks.append({'weld':record['weld'],'root_points_mm':roots,'surface_checks':local,
                   'passed_preassembly_envelope':all(r['passed'] for r in local)})
report={'source_model_sha256':recipe['source_model_sha256'],
        'source_parts_sha256':payload['source_parts_sha256'],
        'candidate_geometry_sha256':hashlib.sha256((folder/'geometry.json.gz').read_bytes()).hexdigest(),
        'stage_members':members,
        'stage_order':'TIG rods onto lower6mm adaptor before upper4mm adaptor, factory yoke and lower knife cassette',
        'intentional_active_weld_deposition_not_a_static_obstacle':True,
        'tool_envelope':{'axis':'45deg outward/down','length_mm':50.,'maximum_radius_mm':6.,
                         'root_step_mm':1.,'axis_step_mm':1.,'root_process_zone_mm':1.},
        'checks':checks,'passed_all_preassembly_envelopes':all(c['passed_preassembly_envelope'] for c in checks),
        'particular_purchased_torch_certified':False,'fixture_model_checked':False,
        'manufacturing_release':False,'production_release':False}
(folder/'torch_access_audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
print('HEAD_TORCH_ACCESS',report['passed_all_preassembly_envelopes'],flush=True)
sys.stdout.flush();os._exit(0 if report['passed_all_preassembly_envelopes'] else 2)
