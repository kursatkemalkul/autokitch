"""Our cutting-head stock and three real bottom M8 seats; not activated.

Split native 8/10 mm plates into permitted 6+2/6+4 stock while retaining
their exact faceted outlines. Supplier actuator is never modified. The
upper mounting/weld operation and layer retention remain open.
"""
from pathlib import Path
source = Path(__file__).with_name('oil_fluid_clamp_candidate.py')
ns = dict(__file__=str(source), __name__='clamp_helpers')
exec(compile(source.read_text(encoding='utf-8').split("if __name__=='__main__':")[0], str(source), 'exec'), ns)
P = ns['pickle'].loads((ns['K1'] / 'k_parca_catalog_verified.pkl').read_bytes())['P']
DEST = ns['OUT'] / 'cut_head_mount_candidate'
DEST.mkdir(exist_ok=True)
ns.update(P=P, BASE=ns['OUT']/'actuator_catalog_fastener_candidate/A/hat3_v10zc.glb', DEST=DEST)
fn = source.read_text(encoding='utf-8').split('def audit_clamps(')[1].split("if __name__=='__main__':")[0]
exec(compile('def audit_clamps('+fn.replace('k_parca_pump_verified.pkl', 'k_parca_catalog_verified.pkl'), str(source), 'exec'), ns)
np, PM, S, cq = (ns[k] for k in ('np', 'PM', 'S', 'cq'))
import manifold3d as mf
import json
ORIGIN = np.array([4200., 1200., -206.])
repairs, pieces, joins, holes = {}, [], [], []
stock = []

def solid_shape(shape):
    v, f = PM.mesh(shape)
    return PM.solid(v, f, ORIGIN)

def save_repair(name, after, before, purpose):
    m = after.to_mesh()
    added = float((after-before).volume())
    assert added < .001
    repairs[name] = {'V':np.asarray(m.vert_properties)[:,:3]+ORIGIN,
        'F':np.asarray(m.tri_verts, dtype=np.int32), 'tur':'sac',
        'original_triangles':P[name]['V'][P[name]['F']],
        'added_material_mm3':added, 'removed_material_mm3':float((before-after).volume()),
        'purpose':purpose}

def make_piece(name, solid, thickness):
    m = solid.to_mesh()
    v = np.asarray(m.vert_properties)[:,:3]+ORIGIN
    f = np.asarray(m.tri_verts, dtype=np.int32)
    # Make a CAD shell from the exact manifold facets, avoiding outline refits.
    faces = []
    for tri in v[f]:
        wire = cq.Wire.makePolygon([cq.Vector(*point) for point in tri], close=True)
        faces.append(cq.Face.makeFromWires(wire))
    sh = cq.Solid.makeSolid(cq.Shell.makeShell(faces))
    item = S._bp(name, sh, 'laser plate AISI304', 'Cutting head stock layer',
                 str(thickness)+'mm native outline', malzeme='AISI304', birim='K_KESICI', uretim=True, mal='sac')
    item['tur'] = 'sac'
    return item

centres = []
for i in range(3):
    name = 'ara_dikme_'+str(i)
    v = P[name]['V']
    # Native 12-sided cylinders have a vertex at +X but not always at -X.
    # Radius/phase comes from the source, not the asymmetric bbox midpoint.
    z = float((v[:,2].min()+v[:,2].max())/2.)
    x = float(v[:,0].max()-8.)
    centres.append((x,z))

for name, split, extra, lower_t, upper_t in [
    ('kafa_plakasi_8',1172.5,'k79_kafa_ust_plaka_2',6.,2.),
    ('kafa_adaptoru',1250.5,'k79_kafa_adaptor_ust_plaka_4',6.,4.)]:
    before = PM.solid(P[name]['V'], P[name]['F'], ORIGIN)
    lo = float(P[name]['V'][:,1].min()); hi = float(P[name]['V'][:,1].max())
    assert abs(split-lo-lower_t) < .001 and abs(hi-split-upper_t) < .001
    box = mf.Manifold.cube((500.,split-lo,500.)).translate((-250.,lo-ORIGIN[1],-250.))
    lower, upper = before ^ box, before-box
    original_volume = before.volume()
    assert abs((lower+upper).volume()-original_volume) < .01
    if name == 'kafa_plakasi_8':
        for x,z in centres:
            tool = solid_shape(ns['cylinder'](x,1165.5,z,4.5,10.))
            lower, upper = lower-tool, upper-tool
            # 0.05mm radial machining clearance from the nominal16mm head.
            seat = solid_shape(cq.Solid.makeCone(8.05,3.97,4.4,cq.Vector(x,1166.5,z),cq.Vector(0,1,0)))
            lower = lower-seat
            holes.append({'center_mm':[x,1166.5,z], 'diameter_mm':9., 'layers':[name,extra], 'seat_depth_mm':4.4, 'seat_outer_diameter_mm':16.1})
    save_repair(name, lower, before, 'Permitted lower6mm stock; original faceted outline retained')
    pieces.append(make_piece(extra, upper, upper_t))
    stock.append({'original':name,'lower_mm':lower_t,'upper':extra,'upper_mm':upper_t,
                  'split_y_mm':split,'native_outline_retained':True,'layer_retention_verified':False})

for i,(x,z) in enumerate(centres):
    name = 'ara_dikme_'+str(i)
    before = PM.solid(P[name]['V'], P[name]['F'], ORIGIN)
    assert abs(P[name]['V'][:,1].min()-1174.5) < .001
    bore = solid_shape(ns['cylinder'](x,1174.49,z,4.05,16.01))
    save_repair(name,before-bore,before,'Bottom M8 blind thread; nominal cosmetic bore8.1, tap drill6.8, depth16')
    repairs[name]['tur'] = 'mek'  # Turned rod, not a sheet blank.
    bolt = S.vida('DIN7991','M8',20.,(x,1166.5,z),(0,1,0),ad='k79_kafa_alt_M8x20_'+str(i),birim='K_KESICI')
    bolt['tur']='baglanti'; pieces.append(bolt)
    joins.append({'id':name,'screw':bolt['ad'],'axis':[0,1,0],'center_mm':[x,1166.5,z],
        'catalog_standard':'DIN7991','nominal_length_mm':20.,'clamped_stock_mm':8.,
        'engagement_mm':12.,'blind_bottom_clearance_mm':4.,'pitch_mm':1.25,
        'passed_stack':12.>=8. and 4.>=1.25,'tool_checked':False,
        'upper_rod_and_actuator_attachment_verified':False})

r = ns['audit_clamps'](pieces,joins,repairs,holes)
r.update(stock_layers=stock, supplier_equipment_bodies_changed=False,
         whole_head_connected=False, stock_layer_retention_verified=False,
         note='Geometry candidate only. Upper rod weld/yoke fasteners, layer retention, and actual tool paths remain open.')
(DEST/'audit.json').write_text(json.dumps(ns['clean'](r),indent=2),encoding='utf-8')
ns['sys'].stdout.flush()
ns['os']._exit(0 if r['passed_geometry_and_stacks'] else 2)
