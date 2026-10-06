"""Two NS35/7.5 mounting rails with accessible endpoint fixings.

Nominal purchased rail dimensions from Phoenix0801733 drawing. The supplier
must supply the certified rail, cut to310mm (upper) and235mm (lower): this is not a new sheet design.
Factory device clips remain supplier internals, not invented certificates.
Only our mounting plate width and our holes/fasteners are changed.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib
import manifold3d as mf

K1=OUT/'k1';DEST=OUT/'din_mount_candidate';DEST.mkdir(exist_ok=True)
PM.P=pickle.load((K1/'k_parca_panel_verified.pkl').open('rb'))['P']
PM.DEST=DEST
SOURCE=OUT/'panel_mount_candidate/A/hat3_v10u.glb'
RAILS=((0,1760.,4355.,4345.),(1,1640.,4280.,4270.))
RAIL_SOURCE='https://www.phoenixcontact.com/en-us/products/din-rail-ns-35-75-perf-2000mm-0801733'

def rail(index,y,end):
    # Nominal cross-section:35 wide,27 web,7.5 high,1 thick.
    # Corner radii are not dimensioned in the drawing; the factory radius
    # is intentionally an open purchased-CAD item, not a claimed bend test.
    points=[(y-17.5,-810.5),(y-17.5,-811.5),(y-13.5,-811.5),(y-13.5,-818),
            (y+13.5,-818),(y+13.5,-811.5),(y+17.5,-811.5),(y+17.5,-810.5),
            (y+12.5,-810.5),(y+12.5,-817),(y-12.5,-817),(y-12.5,-810.5)]
    wire=cq.Wire.makePolygon([cq.Vector(4045,a,b) for a,b in points],close=True)
    sh=cq.Solid.extrudeLinear(wire,[],cq.Vector(end-4045.,0,0))
    # Stock slots15x6.2,25mm pitch. The left cut opens an unused
    # stock slot; both actual fixing slots are closed, inside the ends.
    for x in np.arange(4045.,end+1.,25.):
        cutter=K.kutu(x-4.4,x+4.4,y-3.1,y+3.1,-819,-816)
        cutter=cutter.fuse(cylinder(x-4.4,y,-819,3.1,3,axis=(0,0,1))).fuse(cylinder(x+4.4,y,-819,3.1,3,axis=(0,0,1)))
        sh=sh.cut(cutter)
    return S._bp(f'din_rayi_{index}',sh,'EN60715 NS35/7.5',f'Phoenix0801733 purchased rail cut{end-4045:g}mm','35x7.5;15x6.2 slots;25 pitch',malzeme='galvanized steel',birim='K_ELEKTRIK',mal='celik')

def build():
    pieces,panel_joins=PM.build((4047.5,4352.5,1467,1857,-822,-818))
    panel=pieces[0]['sh'];joins=[]
    for index,y,end,right in RAILS:
        pieces.append(rail(index,y,end))
        for side,x in enumerate((4067.5,right)):
            tag=f'{index}_{side}'
            panel=panel.cut(cylinder(x,y,-823,2.75,6,axis=(0,0,1)))
            panel=panel.cut(cq.Solid.makeCone(5.,2.45,2.8,cq.Vector(x,y,-822),cq.Vector(0,0,1)))
            screw=S.vida('DIN7991','M5',12,(x,y,-822),(0,0,1),ad=f'k_din_M5x12_havsa_{tag}',birim='K_ELEKTRIK')
            washer=S.pul('DIN125','M5',(x,y,-817),(0,0,1),ad=f'k_din_M5_pul_{tag}',birim='K_ELEKTRIK')
            nut=S.somun('ISO10511','M5',(x,y,-816),(0,0,1),ad=f'k_din_M5_somun_{tag}',birim='K_ELEKTRIK')
            pieces.extend((screw,washer,nut))
            joins.append({'id':f'din_mount_{tag}','centre_mm':[x,y,-822],'axis':[0,0,1],
                          'parts':[screw['ad'],f'din_rayi_{index}',washer['ad'],nut['ad']],
                          'rail_mount_slot_mm':[15,6.2],'panel_hole_diameter_mm':5.5,
                          'nominal_engagement_mm':5.,'nominal_protrusion_mm':1.,'protrusion_threads':1.25,
                          'method':'DIN7991 M5x12 rear flush, ISO7089 washer, ISO10511 nut',
                          'front_socket_radius_mm':6.5,'rear_hex_tool_radius_mm':4.})
    pieces[0]['sh']=panel;pieces[0]['wp']=cq.Workplane('XY').add(panel)
    return pieces,panel_joins,joins

def audit(pieces,panel_joins,joins):
    # Existing candidate audit checks ALL replacement and added-body pairs
    # plus every unchanged source part, not just the four bolts.
    report=PM.audit(pieces,panel_joins)
    recipe=json.loads(gzip.decompress((DEST/'geometry.json.gz').read_bytes()))
    origin=np.array([4200.,1660.,-820.]);blockers=[]
    shapes={a:PM.solid(np.asarray(r['V']),np.asarray(r['F']),origin) for a,r in recipe['replacement_parts'].items()}
    for j in joins:
        x,y,z=j['centre_mm'];m=np.asarray(recipe['replacement_parts'][j['parts'][0]]['V']);n=np.asarray(recipe['replacement_parts'][j['parts'][-1]]['V'])
        mi=m[:,2]-z;fi=n[:,2]-z
        j['measured_engagement_mm']=float(min(mi.max(),fi.max())-max(mi.min(),fi.min()))
        j['measured_protrusion_mm']=float(mi.max()-fi.max())
        j['thread_stack_passed']=j['measured_engagement_mm']>=4.99 and .79<=j['measured_protrusion_mm']<=2.41
        j['tool_blockers']=[]
        for key,z0,z1,radius in (('front_socket',-811.,-788.,6.5),('rear_allen',-882.,-822.,4.)):
            tool=mf.Manifold.cylinder(z1-z0,radius,radius,circular_segments=64).translate((x-origin[0],y-origin[1],z0-origin[2]))
            # Source equipment is not moved. Source context is included on
            # front access; rear service is on the free panel bench.
            for a,p in PM.P.items():
                if a in recipe['replacement_parts']:continue
                if key=='rear_allen' and not a.startswith(('guc_','plc_','sigorta_','klemens_','din_','valf_','sartlandirici_')):continue
                vv=p['V'];lo=vv.min(0);hi=vv.max(0)
                if hi[0]<x-radius or lo[0]>x+radius or hi[1]<y-radius or lo[1]>y+radius or hi[2]<=z0 or lo[2]>=z1:continue
                try:volume=float((tool^PM.solid(vv,p['F'],origin)).volume())
                except AssertionError:
                    tt=vv[p['F']];roi=np.all(tt.max(1)>=[x-radius,y-radius,z0],axis=1)&np.all(tt.min(1)<=[x+radius,y+radius,z1],axis=1)
                    if roi.any():j['tool_blockers'].append({'tool':key,'part':a,'unverified_open_surface':True})
                    continue
                if volume>.02:j['tool_blockers'].append({'tool':key,'part':a,'volume_mm3':volume})
            # Also check new/changed parts, excluding the head/nut being
            # driven and only their own coaxial seated mounting rail.
            for a,solid in shapes.items():
                if a in j['parts']:continue
                if key=='rear_allen' and a=='arka_sac':continue # rear wall not yet on the free panel bench
                volume=float((tool^solid).volume())
                if volume>.02:j['tool_blockers'].append({'tool':key,'part':a,'volume_mm3':volume})
        j['tool_access_passed']=not j['tool_blockers']
        j['front_socket_envelope_mm']={'diameter':13.,'length':23.}
        j['rear_allen_condition']='Rail bolts tightened on free panel bench before mounting panel on rear wall; supplier equipment retained'
        blockers+=j['tool_blockers']
    correct_source=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    report.update(source_parts_sha256=hashlib.sha256((K1/'k_parca_panel_verified.pkl').read_bytes()).hexdigest(),source_model_sha256=correct_source,
                  rail_joints=joins,purchased_rail_source=RAIL_SOURCE,rail_cut_lengths_mm=[310.,235.],panel_size_mm=[305.,390.,4.],
                  supplier_factory_clip_geometry_verified=False,supplier_radius_verified=False,
                  scope='Four panel mounts and four rail endpoint joints; purchased device clips still open',
                  passed=report['passed'] and all(j['thread_stack_passed'] and j['tool_access_passed'] for j in joins))
    report['remaining_checks']+=['supplier rail radii/CAD','each device factory DIN clip proof','rail/panel assembly paths']
    recipe['source_parts_sha256']=report['source_parts_sha256'];recipe['source_model_sha256']=correct_source
    # Do not re-drill/re-tessellate the already verified rear wall, spacers
    # or panel bolts. Tiny repeat booleans on compressed bores create
    # unnecessary sliver faces. Only the widened panel and two rails change.
    changed={'pano_plakasi','din_rayi_0','din_rayi_1'}
    keep=changed|set(report['added_parts'])
    recipe['replacement_parts']={a:r for a,r in recipe['replacement_parts'].items() if a in keep}
    recipe['original_triangles']={a:r for a,r in recipe['original_triangles'].items() if a in changed}
    report['changed_existing_parts']=sorted(changed)
    report['previous_verified_panel_hardware_and_rear_retained']=True
    (DEST/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(recipe,separators=(',',':')).encode(),mtime=0))
    print('DIN_MOUNT_CANDIDATE',report['passed'],'intersections',report['intersections'],'unverified',report['unverified_source_geometry'],'tool',blockers,flush=True)
    return report

if __name__=='__main__':
    parts,pj,j=build();r=audit(parts,pj,j);sys.stdout.flush();os._exit(0 if r['passed'] else 2)
