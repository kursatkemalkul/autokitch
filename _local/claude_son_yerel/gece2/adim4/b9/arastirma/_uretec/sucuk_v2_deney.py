"""Versioned differential experiment, reusing the v8 verified stepping/recording.

Every source transformation is asserted. The v8 source is never edited.
This is an engineering experiment, not a real-machine controller.
"""
from pathlib import Path
import hashlib
RUN_SOURCE_HASHES={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
    [Path(__file__),Path(__file__).with_name('sucuk_v2_sahne.py'),Path(__file__).with_name('sucuk_fizik_deney_v8.py')]}
src=Path(__file__).with_name('sucuk_fizik_deney_v8.py').read_text(encoding='utf-8')
def rep(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a))
    src=src.replace(a,b)

rep("args = ap.parse_args()", """ap.add_argument('--variant', choices=['baseline','candidate','relieved'], default='baseline')
ap.add_argument('--mixed', action='store_true')
ap.add_argument('--stock-g', type=float, default=0.)
ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--stiffness', type=float, default=0.)
ap.add_argument('--dough-stiffness', type=float, default=0.)
ap.add_argument('--mu', type=float, default=.25)
ap.add_argument('--dough-mu', type=float, default=.5)
ap.add_argument('--torque', type=float, default=5.)
ap.add_argument('--law-file', default='')
ap.add_argument('--exit-gui-after-result', action='store_true', help='GUI smoke-test only')
args = ap.parse_args()
assert args.gpu, 'SDF dynamic contacts require this experiment GPU configuration'
assert 0 < args.torque <= 5., 'Preserve catalogue gearbox rating'""")
rep("OUT = ROOT / 'arastirma/3_TOPPING/sucuk_fizik_deney_v8'","OUT = ROOT / 'arastirma/3_TOPPING/sucuk_v2/runs'")
rep("OUT.mkdir(parents=True, exist_ok=True)","OUT.mkdir(parents=True, exist_ok=True)\nassert not (OUT/(args.tag+'.json')).exists(), 'Use a new tag; previous experiment preserved'")
rep("assert UsdGeom.GetStageUpAxis(stage)=='Z'", """assert UsdGeom.GetStageUpAxis(stage)=='Z'
if args.gui:
    import omni.ui as ui
    from isaacsim.core.utils.viewports import set_camera_view
    set_camera_view(eye=np.array([1.93,-.65,.67]),target=np.array([1.46,.26,.31]))
    live_window=ui.Window('SUCUK V2 - PHYSX HESABI',width=400,height=220)
    with live_window.frame:
        with ui.VStack(spacing=8):
            ui.Label('CANLI FIZIK COZULUYOR - KAYIT OYNATMA DEGIL',height=30)
            ui.Label('Gida ve temas parametreleri VARSAYIM.',height=25)
            ui.Label('Sanal gram sayaci: gercek makinede sensor yok.',height=35,word_wrap=True)
            live_status=ui.Label('Hazne yukleniyor ve tabla yerine gidiyor...',height=60,word_wrap=True)""")
rep("    if args.gui: world.render()", "    if args.gui and world.current_time_step_index % 8 == 0: world.render()")
start=src.index("mat = UsdShade.Material.Define")
end=src.index("body_data=None; body_index={}")
src=src[:start]+'''from sucuk_v2_sahne import contact_material,closed_meshes,food_geometry
food_mat=contact_material(stage,'Sucuk',args.mu,args.stiffness,1.6*math.sqrt(args.stiffness*.000512))
machine_mat=contact_material(stage,'Machine',args.mu)
dough_mat=contact_material(stage,'Dough',args.dough_mu,args.dough_stiffness,1.6*math.sqrt(args.dough_stiffness*.000512))
for path in active:
    if 'KUP_SUCUK' in path:
        UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(path)).Bind(machine_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
    if path.startswith('/World/PIDE/'):
        UsdShade.MaterialBindingAPI.Apply(stage.GetPrimAtPath(path)).Bind(dough_mat,UsdShade.Tokens.strongerThanDescendants,'physics')
geometry_audit=closed_meshes(stage,args.variant,machine_mat)
paths,sizes,masses=food_geometry(stage,args,food_mat)
args.count=len(paths); cube_kg=.008**3*1000.;xc=slot['x']/1000
def mass_g(ids):
    return float(masses[list(ids)].sum()*1000) if len(ids) else 0.
stage.GetPrimAtPath(MY+'/EKLEM_HELEZON_KUP_SUCUK').GetAttribute('drive:angular:physics:maxForce').Set(args.torque)
print('V2_GEOMETRY',json.dumps(geometry_audit),flush=True)
print('V2_FOOD',args.count,float(masses.sum()*1000),float(sizes.min()),float(sizes.max()),flush=True)

'''+src[end:]
# Ensure every measured quantity uses individual masses, never nominal cube count.
src=src.replace('len(emitted)*cube_kg*1000','mass_g(emitted)')
src=src.replace('len(preleak)*cube_kg*1000','mass_g(preleak)')
src=src.replace('args.count*cube_kg*1000','float(masses.sum()*1000)')
src=src.replace('int(on.sum())*cube_kg*1000','float(masses[on].sum()*1000)')
src=src.replace("int(((xyz[:,2]<.160)&~on).sum())*cube_kg*1000","float(masses[(xyz[:,2]<.160)&~on].sum()*1000)")
rep("rings=np.histogram(radius[on],edges)[0]", "rings=np.histogram(radius[on],edges,weights=masses[on]*1000)[0]")
rep("pp[2]+.020", "pp[2]+.040")
rep("def target(t):", """radius_law=json.loads(Path(args.law_file).read_text()) if args.law_file else None
def target(t):
    if radius_law is not None:
        r=float(np.interp(np.clip(t/T['doz_sn'],0,1),radius_law['progress_knots'],radius_law['radius_knots_mm']))
        return xc-math.sqrt(max(0,r*r-offset_mm**2))/1000""")
rep("report={'script_sha256':", "report={'run_source_hashes':RUN_SOURCE_HASHES,'variant':args.variant,'geometry_audit':geometry_audit,'material_assumptions':vars(args), 'script_sha256':")
rep("time=times,xyz=frames,quat=rotations,paths=motion_paths", "time=times,xyz=frames,quat=rotations,paths=motion_paths,side_m=sizes,mass_kg=masses")
rep("'equal_area_ring_counts':rings.tolist()", "'equal_area_ring_mass_g':rings.tolist()")
rep("'friction':.25", "'friction':args.mu")
rep("'cassette_contact_friction':.25", "'cassette_contact_friction':args.mu")
rep("'cube_mm':8", "'nominal_cube_side_mm':8,'size_distribution':'triangular 6-10 mm' if args.mixed else 'fixed 8 mm'")
rep("diagnostics.append(diag)", "diagnostics.append(diag)\n        if args.gui: live_status.text='%.1f sn | cikistan %.1f g | pide ustunde %.1f g' % (t,diag['emitted_g'],diag['on_pide_g'])")
# Keep the completed live run visible. Rendering does not advance physics here.
rep("app.close()", """if args.gui:
    import omni.ui as ui
    result_window=ui.Window('SUCUK V2 - CANLI HESAP TAMAMLANDI',width=420,height=230)
    with result_window.frame:
        with ui.VStack(spacing=8):
            ui.Label('PHYSX COZUMU TAMAMLANDI - SON KARE',height=25)
            ui.Label('Pide: %.2f g / hedef 70 g' % report['last']['on_pide_g'],height=25)
            ui.Label('Gida parametreleri VARSAYIM; uretim onayi degil.',height=35,word_wrap=True)
            ui.Label('Sanal cikis sayaci: makinede bu sensor yok.',height=35,word_wrap=True)
    while app.is_running() and not args.exit_gui_after_result:app.update()
app.close()""")
exec(compile(src,__file__,'exec'),globals())
