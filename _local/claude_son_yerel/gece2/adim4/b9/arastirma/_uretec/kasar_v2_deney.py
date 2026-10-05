"""Kasar V2 physical differential experiment. Reuses tested v8 stepping only.

55 g is the prior approved cheese target. sim_makine.json's conflicting 100 g
is reported, not silently changed. The virtual counter is NOT real hardware.
"""
from pathlib import Path
import hashlib
RUN_SOURCE_HASHES={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
    [Path(__file__),Path(__file__).with_name('kasar_v2_sahne.py'),Path(__file__).with_name('sucuk_fizik_deney_v8.py')]}
src=Path(__file__).with_name('sucuk_fizik_deney_v8.py').read_text(encoding='utf-8')
def rep(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a));src=src.replace(a,b)

rep('args = ap.parse_args()',"""ap.add_argument('--variant',choices=['baseline','candidate'],default='baseline')
ap.add_argument('--stock-g',type=float,default=500.)
ap.add_argument('--seed',type=int,default=7)
ap.add_argument('--stiffness',type=float,default=2000.)
ap.add_argument('--dough-stiffness',type=float,default=1000.)
ap.add_argument('--mu',type=float,default=.35)
ap.add_argument('--dough-mu',type=float,default=.5)
ap.add_argument('--torque',type=float,default=5.)
ap.add_argument('--mixer-rpm',type=float,default=4.)
ap.add_argument('--settle',type=float,default=3.)
ap.add_argument('--law-file',default='')
ap.add_argument('--exit-gui-after-result',action='store_true')
args = ap.parse_args()
assert args.gpu and 0<args.torque<=5 and args.stock_g>0""")
rep("default=8)","default=42)")
rep("default=70)","default=53)")
rep("default=30)","default=25)")
rep("OUT = ROOT / 'arastirma/3_TOPPING/sucuk_fizik_deney_v8'","OUT = ROOT / 'arastirma/3_TOPPING/kasar_v2/runs'")
rep('OUT.mkdir(parents=True, exist_ok=True)',"OUT.mkdir(parents=True, exist_ok=True)\nassert not (OUT/(args.tag+'.json')).exists(),'Use a new run tag'")
rep("y['cad']=='sucuk_cad_v7'","y['cad']=='kasar_cad_v14'")
rep("T=dict(T, rpm=args.table_rpm, t_dis=args.outer_dwell, t_ic=args.inner_dwell)",
    "original_slot_target=slot['doz_g']\nslot=dict(slot,doz_g=55.)\nT=dict(T,rpm=args.table_rpm,t_dis=args.outer_dwell,t_ic=args.inner_dwell)")
src=src.replace('KUP_SUCUK','KASAR_KABI').replace("'SUCUK' in s","'KASAR' in s")
rep('px.CreateEnableCCDAttr(True)','px.CreateEnableCCDAttr(False)')
rep('px.CreateTimeStepsPerSecondAttr(240)','px.CreateTimeStepsPerSecondAttr(480)')
rep('    if args.gui: world.render()', '    if args.gui and world.current_time_step_index%8==0: world.render()')
start=src.index('mat = UsdShade.Material.Define');end=src.index('body_data=None; body_index={}')
src=src[:start]+'''from kasar_v2_sahne import contact_material,closed_meshes,food_geometry
food_mat=contact_material(stage,'Kasar',args.mu,args.stiffness,1.6*math.sqrt(args.stiffness*.000176))
machine_mat=contact_material(stage,'KasarMachine',args.mu)
dough_mat=contact_material(stage,'KasarDough',args.dough_mu,args.dough_stiffness,1.6*math.sqrt(args.dough_stiffness*.000176))
for path in active:
    if 'KASAR' in path:UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(path)).Bind(machine_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
    if path.startswith('/World/PIDE/'):UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(path)).Bind(dough_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
geometry_audit=closed_meshes(stage,args.variant,machine_mat)
paths,sizes,masses=food_geometry(stage,args,food_mat)
args.count=len(paths);xc=slot['x']/1000
def mass_g(ids):return float(masses[list(ids)].sum()*1000) if len(ids) else 0.
stage.GetPrimAtPath(MY+'/EKLEM_HELEZON_KASAR_KABI').GetAttribute('drive:angular:physics:maxForce').Set(args.torque)
print('KASAR_GEOMETRY',json.dumps(geometry_audit),flush=True)
print('KASAR_FOOD',args.count,float(masses.sum()*1000),flush=True)
print('TARGET_CONFLICT',original_slot_target,'experiment_target',slot['doz_g'],flush=True)
'''+src[end:]
for a,b in [('len(emitted)*cube_kg*1000','mass_g(emitted)'),('len(preleak)*cube_kg*1000','mass_g(preleak)'),('args.count*cube_kg*1000','float(masses.sum()*1000)'),('int(on.sum())*cube_kg*1000','float(masses[on].sum()*1000)'),("int(((xyz[:,2]<.160)&~on).sum())*cube_kg*1000","float(masses[(xyz[:,2]<.160)&~on].sum()*1000)")]:src=src.replace(a,b)
rep("drive('KARISTIRICI_KASAR_KABI','angular',args.direction*24)","drive('KARISTIRICI_KASAR_KABI','angular',args.direction*args.mixer_rpm*6)")
rep('for _ in range(round(2/dt)): step()','for _ in range(round(args.settle/dt)): step()')
rep('rings=np.histogram(radius[on],edges)[0]','rings=np.histogram(radius[on],edges,weights=masses[on]*1000)[0]')
rep('def target(t):',"""radius_law=json.loads(Path(args.law_file).read_text()) if args.law_file else None
radius_law_sha256=hashlib.sha256(Path(args.law_file).read_bytes()).hexdigest() if args.law_file else None
def target(t):
    if radius_law is not None:
        r=float(np.interp(np.clip(t/T['doz_sn'],0,1),radius_law['progress_knots'],radius_law['radius_knots_mm']))
        return xc-math.sqrt(max(0,r*r-offset_mm**2))/1000""")
rep("report={'script_sha256':","report={'run_source_hashes':RUN_SOURCE_HASHES,'radius_law':radius_law,'radius_law_sha256':radius_law_sha256,'geometry_audit':geometry_audit,'material_assumptions':vars(args),'variant':args.variant,'original_scene_target_g':original_slot_target,'script_sha256':")
rep("'equal_area_ring_counts':rings.tolist()","'equal_area_ring_mass_g':rings.tolist()")
rep("'cube_mm':8,'density_kg_m3':1000,'friction':.25", "'shred_mm':'3-5 x 6-14 x 3-5 triangular; mode 4x10x4','density_kg_m3':1100,'friction':args.mu,'adhesion_model':False")
rep("'cassette_contact_friction':.25","'cassette_contact_friction':args.mu")
rep('time=times,xyz=frames,quat=rotations,paths=motion_paths','time=times,xyz=frames,quat=rotations,paths=motion_paths,dimensions_m=sizes,mass_kg=masses')
rep('app.close()',"""if args.gui:
    import omni.ui as ui
    w=ui.Window('KASAR V2 - CANLI HESAP SONUCU',width=430,height=200)
    with w.frame:
        with ui.VStack(spacing=8):
            ui.Label('Pide %.2f g / hedef 55 g' % report['last']['on_pide_g'])
            ui.Label('Gida parametreleri VARSAYIM. Sanal sayac, gercek sensor degil.',word_wrap=True)
            ui.Label('Kismi stok deneyi. 8.8 kg ve 48 saat dogrulanmadi.',word_wrap=True)
    while app.is_running() and not args.exit_gui_after_result:app.update()
app.close()""")
exec(compile(src,__file__,'exec'),globals())
