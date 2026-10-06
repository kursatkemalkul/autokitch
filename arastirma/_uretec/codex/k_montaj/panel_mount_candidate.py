"""Actual K panel mounting candidate; no source activation or release.

Retains device coordinates. Four flush M5x20 bolts clamp a 4mm panel,
6.5mm bored spacers, 1.5mm rear wall, rear washers and ISO10511 nuts.
Bottom fixings move down5mm so a3mm Allen tool can pass the devices.
The panel alone extends down5mm. Purchased equipment is unchanged.
"""
from lower_support import *
import pickle, hashlib
import manifold3d as mf
import trimesh
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as YD

K1=OUT/'k1'
DEST=OUT/'panel_mount_candidate'
DEST.mkdir(exist_ok=True)
P=pickle.load((K1/'k_parca.pkl').open('rb'))['P']
CENTRES=((4080.,1477.),(4320.,1477.),(4080.,1690.),(4320.,1690.))

def mesh(sh):
    vertices,faces=sh.tessellate(.002,.05)
    return np.asarray([v.toTuple() for v in vertices]),np.asarray(faces,dtype=np.int32)

def solid(v,f,origin):
    # CAD tessellation duplicates shared vertices at face seams. Merge only
    # identical local float32 coordinates; do not heal/move source surfaces.
    vv,inverse=np.unique(np.asarray(v-origin,dtype=np.float32),axis=0,return_inverse=True)
    ff=inverse[np.asarray(f,dtype=np.int32)]
    s=mf.Manifold(mf.Mesh(vert_properties=vv,tri_verts=np.asarray(ff,dtype=np.uint32)))
    assert str(s.status())=='Error.NoError',str(s.status())
    return s

def build(panel_bounds=(4067.5,4332.5,1467,1857,-822,-818)):
    panel=K.kutu(*panel_bounds)
    pieces=[];joins=[]
    for i,(x,y) in enumerate(CENTRES):
        panel=panel.cut(cylinder(x,y,-823,2.75,6,axis=(0,0,1)))
        # Match the existing DIN7991 factory head mesh, not a bbox recess.
        panel=panel.cut(cq.Solid.makeCone(5.,2.45,2.8,cq.Vector(x,y,-818),cq.Vector(0,0,-1)))
        tube=cylinder(x,y,-828.5,5.,6.5,axis=(0,0,1)).cut(cylinder(x,y,-829.5,2.75,8.5,axis=(0,0,1)))
        spacer=S._bp(f'pano_ara_burcu_{i}',tube,'turned spacer','AISI304 bored panel spacer','OD10 ID5.5 L6.5',malzeme='AISI304',birim='K_ELEKTRIK',uretim=True,mal='celik')
        screw=S.vida('DIN7991','M5',20,(x,y,-818),(0,0,-1),ad=f'k_pano_M5x20_havsa_{i}',birim='K_ELEKTRIK')
        washer=S.pul('DIN125','M5',(x,y,-830),(0,0,-1),ad=f'k_pano_M5_pul_{i}',birim='K_ELEKTRIK')
        nut=S.somun('ISO10511','M5',(x,y,-831),(0,0,-1),ad=f'k_pano_M5_somun_{i}',birim='K_ELEKTRIK')
        pieces.extend((spacer,screw,washer,nut))
        joins.append({'id':f'panel_mount_{i}','centre_mm':[x,y,-818],'axis':[0,0,-1],
                      'parts':[screw['ad'],spacer['ad'],washer['ad'],nut['ad']],
                      'clearance_diameter_mm':5.5,'nominal_engagement_mm':5.,
                      'nominal_protrusion_mm':2.,'protrusion_threads':2.5,
                      'head_flush':True,'tool_hex_mm':3.,'minimum_tool_envelope_radius_mm':4.,
                      'method':'DIN7991 M5x20, bored spacer, ISO7089 washer, ISO10511 nut'})
    pieces.insert(0,S._bp('pano_plakasi',panel,'laser plate 304','K panel mounting plate',f'{panel_bounds[1]-panel_bounds[0]:g}x{panel_bounds[3]-panel_bounds[2]:g}x4',malzeme='AISI304',birim='K_ELEKTRIK',uretim=True,mal='sac'))
    return pieces,joins

def audit(pieces,joins):
    origin=np.array([4200.,1660.,-820.])
    replacements={p['ad']:dict(zip(('V','F'),mesh(p['sh']))) for p in pieces}
    v=P['arka_sac']['V'];f=P['arka_sac']['F']
    rear=solid(v,f,origin)
    original_rear=rear
    for x,y in CENTRES:
        hole=mf.Manifold.cylinder(18.,2.75,2.75,circular_segments=96).translate((x-origin[0],y-origin[1],-836-origin[2]))
        rear=rear-hole
    assert str(rear.status())=='Error.NoError'
    rear_added_volume=float((rear-original_rear).volume())
    assert rear_added_volume<.0001,'Rear drilling must not add any material'
    m=rear.to_mesh()
    replacements['arka_sac']={'V':np.asarray(m.vert_properties[:,:3],float)+origin,'F':np.asarray(m.tri_verts,int)}
    solids={a:solid(r['V'],r['F'],origin) for a,r in replacements.items()}
    clashes=[];unverified=[];baseline_contacts=[];open_surface_checks=[]
    # Test every changed/added body against every intersecting source bbox,
    # replacing the old panel/spacers/rear with this candidate's geometry.
    for a,r in replacements.items():
        # Four bored holes only subtract rear-wall material. Non-increasing
        # solid is stronger evidence of no new interference than rerunning
        # inherited rear-wall/PEM contacts or environment proxy bboxes.
        if a=='arka_sac':continue
        lo=r['V'].min(0);hi=r['V'].max(0)
        for b,p in P.items():
            if b in replacements:continue
            bv=p['V'];blo=bv.min(0);bhi=bv.max(0)
            if np.any(np.minimum(hi,bhi)-np.maximum(lo,blo)<=.0005):continue
            try:other=solid(bv,p['F'],origin)
            except AssertionError as exc:
                # Open environment/cable meshes require triangle tests;
                # distance to vertices alone is not an intersection test.
                bt=bv[p['F']]
                crop=np.all(bt.max(1)>=lo-.01,axis=1)&np.all(bt.min(1)<=hi+.01,axis=1)
                bt=bt[crop]
                if not len(bt):
                    open_surface_checks.append({'candidate':a,'source_part':b,'roi_triangles':0,'passed':True})
                    continue
                crossings=int(YD.poz_kesisim(np.asarray(r['V'][r['F']],float),np.asarray(bt,float),.002).sum())
                vertices=np.unique(bt.reshape(-1,3),axis=0)
                candidate=trimesh.Trimesh(r['V'],r['F'],process=False)
                inside=int((trimesh.proximity.signed_distance(candidate,vertices)>.01).sum())
                row={'candidate':a,'source_part':b,'roi_triangles':len(bt),'crossing_pairs':crossings,'source_vertices_inside_candidate':inside,'passed':not crossings and not inside}
                open_surface_checks.append(row)
                if not row['passed']:unverified.append(row)
                continue
            volume=float((solids[a]^other).volume())
            if volume>.02:
                if a=='arka_sac':
                    old=solid(P[a]['V'],P[a]['F'],origin)
                    before=float((old^other).volume())
                    if abs(before-volume)<.002:
                        baseline_contacts.append({'a':a,'b':b,'before_mm3':before,'after_mm3':volume,'delta_mm3':volume-before})
                        continue
                clashes.append({'a':a,'b':b,'volume_mm3':volume})
    names=list(replacements)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            volume=float((solids[a]^solids[b]).volume())
            if volume>.02:clashes.append({'a':a,'b':b,'volume_mm3':volume})
    for j in joins:
        x,y,z=j['centre_mm'];screw=replacements[j['parts'][0]]['V'];nut=replacements[j['parts'][-1]]['V']
        shaft=-screw[:,2];female=-nut[:,2]
        overlap=min(shaft.max(),female.max())-max(shaft.min(),female.min())
        protrusion=shaft.max()-female.max()
        j['measured_engagement_mm']=float(overlap);j['measured_protrusion_mm']=float(protrusion)
        j['thread_stack_passed']=bool(overlap>=4.99 and .79<=protrusion<=2.41)
        tool=mf.Manifold.cylinder(80,4.,4.,circular_segments=48).translate((x-origin[0],y-origin[1],-818-origin[2]))
        blocked=[]
        for a,p in P.items():
            if a in replacements:continue
            vv=p['V'];lo=vv.min(0);hi=vv.max(0)
            if hi[0]<x-4 or lo[0]>x+4 or hi[1]<y-4 or lo[1]>y+4 or hi[2]<-818 or lo[2]>-738:continue
            try:vol=float((tool^solid(vv,p['F'],origin)).volume())
            except AssertionError:
                # Conservative2mm-sampled swept4mm sphere envelope around
                # the tool axis, evaluated against actual source triangles.
                samples=np.column_stack((np.full(41,x),np.full(41,y),np.linspace(-818,-738,41)))
                tt=vv[p['F']]
                roi=np.all(tt.max(1)>=[x-4.13,y-4.13,-822.13],axis=1)&np.all(tt.min(1)<=[x+4.13,y+4.13,-733.87],axis=1)
                if not roi.any():continue
                # Crop triangles only; this is a surface-distance query,
                # not a closed-volume reinterpretation of the proxy.
                sm=trimesh.Trimesh(vv,np.asarray(p['F'])[roi],process=False)
                distance=float(trimesh.proximity.closest_point(sm,samples)[1].min())
                if distance<4.13:blocked.append({'part':a,'sampled_tool_axis_surface_distance_mm':distance})
                continue
            if vol>.02:blocked.append({'part':a,'volume_mm3':vol})
        j['front_tool_blockers']=blocked
        j['front_tool_access_passed']=not blocked
        # Machine is pulled off the shop wall for rear service (Kemal's
        # standing decision). Check the actual K station's obstruction,
        # not the parked-shop wall that is absent during that operation.
        socket=mf.Manifold.cylinder(60,6.5,6.5,circular_segments=64).translate((x-origin[0],y-origin[1],-896-origin[2]))
        rear_blocked=[]
        for a,p in P.items():
            if a in replacements or a.startswith('cevre_'):continue
            vv=p['V'];lo=vv.min(0);hi=vv.max(0)
            if hi[0]<x-6.5 or lo[0]>x+6.5 or hi[1]<y-6.5 or lo[1]>y+6.5 or hi[2]<-896 or lo[2]>-836:continue
            try:vol=float((socket^solid(vv,p['F'],origin)).volume())
            except AssertionError:
                rear_blocked.append({'part':a,'unverified_geometry':True});continue
            if vol>.02:rear_blocked.append({'part':a,'volume_mm3':vol})
        j['rear_socket_clearance_envelope_diameter_mm']=13.
        j['rear_tool_blockers']=rear_blocked
        j['rear_tool_access_passed']=not rear_blocked
        j['rear_service_condition']='Machine pulled forward before rear service; shop wall excluded, K station geometry retained'
    report={'source_parts_sha256':hashlib.sha256((K1/'k_parca.pkl').read_bytes()).hexdigest(),
            'source_model_sha256':json.loads((K1/'current_source_manifest.json').read_text())['source_model_sha256'],
            'units':'mm','scope':'Candidate panel mounts only, not whole-station release',
            'joints':joins,'intersections':clashes,'unverified_source_geometry':unverified,'open_mesh_surface_checks':open_surface_checks,
            'rear_added_volume_mm3':rear_added_volume,'rear_change_is_subtractive_only':True,
            'changed_existing_parts':['pano_plakasi','arka_sac']+[f'pano_ara_burcu_{i}' for i in range(4)],
            'added_parts':[p['ad'] for p in pieces if p['ad'] not in P],
            'device_coordinates_unchanged':True,'purchased_equipment_unchanged':True,
            'passed':not clashes and not unverified and all(j['thread_stack_passed'] and j['front_tool_access_passed'] and j['rear_tool_access_passed'] for j in joins),
            'production_release':False,'source_activation':False,
            'remaining_checks':['install/remove path','panel load/overhang check','assembly ordering','source-chain A/B replay','re-extraction and whole-station audits']}
    (DEST/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    # Portable exact candidate geometry, not a misleading production gate.
    recipe={'source_parts_sha256':report['source_parts_sha256'],'source_model_sha256':report['source_model_sha256'],
            'replacement_parts':{a:{k:w.tolist() for k,w in r.items()} for a,r in replacements.items()},
            'original_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in replacements if a in P},
            'added_parts':report['added_parts']}
    (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(recipe,separators=(',',':')).encode(),mtime=0))
    S.glb_yaz(str(DEST/'panel_mount.glb'),pieces,tol=.015,aci=.12)
    print('PANEL_MOUNT_CANDIDATE',report['passed'],'intersections',clashes,'tool',[(j['id'],j['front_tool_blockers']) for j in joins],flush=True)
    return report

if __name__=='__main__':
    parts,joins=build();report=audit(parts,joins)
    sys.stdout.flush();os._exit(0 if report['passed'] else 2)
