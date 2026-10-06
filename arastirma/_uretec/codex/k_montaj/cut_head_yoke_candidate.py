"""Four M8x25 screws through our10mm adaptor to the factory yoke interface.

The native approximate yoke omitted its catalogue threaded holes. This
candidate makes that omission explicit: nominal bores represent supplied
D2=M8/T1=17 mounting threads, not a shop drilling instruction for Festo.
Outer housing, outline, placement and guide bores are untouched. Grid80x40
is the native drawing's B4/H4 interface; supplier CAD confirmation remains
recorded separately before activation.
"""
from pathlib import Path
source=Path(__file__).with_name('cut_head_weld_candidate.py')
ns=dict(__file__=str(source),__name__='head_weld_definition')
exec(compile(source.read_text(encoding='utf-8').split("r=helper['audit_clamps'](")[0],str(source),'exec'),ns)
helper=ns['helper'];P=ns['P'];PM=ns['PM'];np=ns['np'];cq=ns['cq'];S=ns['ns']['S']
origin=ns['origin'];parts=ns['ns']['pieces'];repairs=ns['ns']['repairs']
joins=ns['ns']['joins'];holes=ns['ns']['holes']
folder=helper['OUT']/'cut_head_yoke_candidate';folder.mkdir(exist_ok=True)
helper['DEST']=folder
def native_or_repaired(name):
    r=repairs.get(name,P[name])
    return PM.solid(np.asarray(r['V']),np.asarray(r['F']),origin)
def solid_shape(sh):
    v,f=PM.mesh(sh);return PM.solid(v,f,origin)

yoke='DGRF_boyunduruk';original_yoke=native_or_repaired(yoke);after_yoke=original_yoke
adaptor=native_or_repaired('kafa_adaptoru');original_adaptor=PM.solid(P['kafa_adaptoru']['V'],P['kafa_adaptoru']['F'],origin)
upper=next(p for p in parts if p['ad']=='k79_kafa_adaptor_ust_plaka_4')
upper_solid=solid_shape(upper['sh'])
for i,(x,z) in enumerate([(4160.,-226.),(4160.,-186.),(4240.,-226.),(4240.,-186.)]):
    clear=solid_shape(helper['cylinder'](x,1244.49,z,4.5,10.02))
    seat=solid_shape(cq.Solid.makeCone(8.05,3.97,4.4,cq.Vector(x,1244.5,z),cq.Vector(0,1,0)))
    adaptor=adaptor-clear-seat;upper_solid=upper_solid-clear
    # Visual nominal thread bore; tapping dimensions are not represented
    # as a helical collision solid, consistent with the other factory M10s.
    supplied=solid_shape(helper['cylinder'](x,1254.49,z,4.05,17.01))
    after_yoke=after_yoke-supplied
    bolt=S.vida('DIN7991','M8',25.,(x,1244.5,z),(0,1,0),ad='k79_kafa_yoke_M8x25_'+str(i),birim='K_KESICI')
    bolt['tur']='baglanti';parts.append(bolt)
    joins.append({'id':'yoke_'+str(i),'screw':bolt['ad'],'axis':[0,1,0],'center_mm':[x,1244.5,z],
        'catalog_standard':'DIN7991','nominal_length_mm':25.,'clamped_stock_mm':10.,
        'engagement_mm':15.,'blind_bottom_clearance_mm':2.,'pitch_mm':1.25,
        'passed_stack':15.>=8. and 2.>=1.25,'tool_checked':False,
        'interface_source':'Festo DGRF-C63PPV datasheet2025/03 pp14-15, D2=M8,T1=17,B4=80,H4=40; native kesme_cad_v8 adapter BOM',
        'supplier_cad_grid_axes_visually_confirmed':False})
    holes.append({'center_mm':[x,1244.5,z],'diameter_mm':9.,'layers':['kafa_adaptoru',upper['ad']],
                  'factory_yoke_nominal_M8_bore_depth_mm':17.,'seat_depth_mm':4.4,'seat_outer_diameter_mm':16.1})
ns['ns']['save_repair']('kafa_adaptoru',adaptor,original_adaptor,'Lower6mm stock, four actual adaptor clearances and flush heads')
ns['ns']['save_repair'](yoke,after_yoke,original_yoke,'Supplied catalogue M8 female mounting interface omitted by native approximate rendering; no supplier shop modification')
replacement=ns['ns']['make_piece'](upper['ad'],upper_solid,4.)
parts[parts.index(upper)]=replacement
r=helper['audit_clamps'](parts,joins,repairs,holes)
r.update(continuous_rod_welds=ns['records'],stock_layers=ns['ns']['stock'],
    supplier_equipment_bodies_changed=True,
    supplier_geometry_correction={'part':yoke,'reason':'Previously omitted as-delivered female threads',
        'housing_and_outer_contour_changed':False,'supplier_manufacturing_modification_required':False,
        'official_document':'https://www.festo.com/media/catalog/204215_documentation.pdf',
        'table_page':15,'D2':'M8','T1_mm':17.,'B4_mm':80.,'H4_mm':40.,
        'supplier_CAD_axes_visually_confirmed':False},
    adaptor_layer_retained_by_four_M8_stacks=True,
    whole_head_connected=False,manufacturing_release=False,production_release=False)
(folder/'audit.json').write_text(ns['ns']['json'].dumps(helper['clean'](r),indent=2),encoding='utf-8')
helper['sys'].stdout.flush();helper['os']._exit(0 if r['passed_geometry_and_stacks'] else 2)
