"""Interactive two-cassette PhysX laboratory. NOT a trajectory replay.

Same state machine for GUI and headless regression. New loading each START.
No food creation, resizing, mass editing or teleporting after world.reset().
All dosing measurements are explicitly virtual; not a hardware controller.
"""
import argparse,json,time,math,hashlib,traceback
from pathlib import Path
from datetime import datetime
import numpy as np
from topping_lab_config import ROOT,OUT,MY,PRODUCTS,RECIPES,settings,charge,radius_x
SOURCE_HASHES={f:hashlib.sha256((ROOT/'arastirma/_uretec'/f).read_bytes()).hexdigest() for f in
    ['topping_lab_live.py','topping_lab_config.py','topping_lab_scene.py','topping_lab_pack.py']}

ap=argparse.ArgumentParser()
ap.add_argument('--headless',action='store_true');ap.add_argument('--recipe',choices=RECIPES,default='karisik')
ap.add_argument('--mode',choices=['hazne','stok'],default='hazne')
ap.add_argument('--kasar',type=float,default=10.);ap.add_argument('--sucuk',type=float,default=10.)
ap.add_argument('--variant',choices=['candidate','baseline'],default='candidate')
ap.add_argument('--tag',default='');ap.add_argument('--settle',type=float,default=3.)
ap.add_argument('--max-dose-seconds',type=float,default=35.)
ap.add_argument('--settle-only',action='store_true');ap.add_argument('--auto-start',action='store_true')
ap.add_argument('--exit-after-result',action='store_true')
ap.add_argument('--preview-only',action='store_true',help='GUI smoke test and viewport capture; no simulation')
ap.add_argument('--food-layer',default='',help='Reuse an INITIAL charge layer, never a recorded trajectory')
ap.add_argument('--profile-steps',type=int,default=0,help='Diagnostic only: stop after N steps and save a timing profile')
ap.add_argument('--dry-run',action='store_true',help='Empty physical motion test, not a food-dose result')
args=ap.parse_args()
from isaacsim import SimulationApp
app=SimulationApp({'headless':args.headless,'width':1600,'height':950})
import omni.usd,carb,omni.physics.tensors
from pxr import Usd,UsdGeom,UsdPhysics,UsdLux,UsdUtils,PhysxSchema,Gf
from isaacsim.core.api import World
from isaacsim.core.utils.viewports import set_camera_view
from omni.physx import get_physx_interface
from topping_lab_scene import add_food,build

DT=1/480
pending=None;paused=False;cancel=False;world=None;job=None;status_label=None;result_label=None;charge_label=None;engine_active=False
machine_paths=[MY+'/ARABA',MY+'/TABLA']+[MY+'/'+s+v['slot'] for v in PRODUCTS.values() for s in ('HELEZON_','KARISTIRICI_')]+['/World/TEPSI','/World/PIDE']
status_text='HAZIR - CANLI BASLAT yeni fizik hesaplar.'
drive_cache={}

def status(text):
    global status_text
    status_text=text
    if status_label:status_label.text=text
    print('LAB_STATUS',text,flush=True)

def lighting(stage):
    d=UsdLux.DomeLight.Define(stage,'/World/LabLight');d.CreateIntensityAttr(600.)
    k=UsdLux.DistantLight.Define(stage,'/World/LabKey');k.CreateIntensityAttr(1800.)
    if not k.GetOrderedXformOps():k.AddRotateXYZOp().Set(Gf.Vec3f(-35,25,0))
    if not args.headless:set_camera_view(eye=np.array([2.15,-1.30,1.05]),target=np.array([1.0,.30,.32]))

def open_empty(variant):
    drive_cache.clear()
    path=OUT/f'TOPPING_LAB_v1_{variant}.usd'
    if not path.exists():build(variant)
    omni.usd.get_context().open_stage(str(path));app.update();app.update()
    stage=omni.usd.get_context().get_stage();stage.SetEditTarget(stage.GetSessionLayer())
    lighting(stage)
    return stage

def drive(stage,name,kind,value):
    key=(name,kind)
    if key in drive_cache and abs(drive_cache[key]-value)<1e-7:return
    attr=stage.GetPrimAtPath(MY+'/EKLEM_'+name).GetAttribute(f'drive:{kind}:physics:targetVelocity')
    assert attr.IsValid(),name;attr.Set(float(value));drive_cache[key]=float(value)

def stop_motors(stage):
    drive(stage,'X','linear',0);drive(stage,'TABLA','angular',0)
    for p in PRODUCTS.values():
        for s in ('HELEZON_','KARISTIRICI_'):drive(stage,s+p['slot'],'angular',0)

def experiment(cfg,tag):
    global world,paused,cancel,engine_active
    started=time.monotonic();run=OUT/'runs'/tag;run.mkdir(parents=True,exist_ok=False)
    (run/'request.json').write_text(json.dumps(cfg,indent=2),encoding='utf-8')
    if world:
        world.stop();world.clear_instance();world=None
    stage=open_empty(cfg['variant'])
    data={p:charge(p,cfg) for p in PRODUCTS}
    summary={p:d['report'] for p,d in data.items()}
    if charge_label:charge_label.text='YUK: '+ ' | '.join(f'{p} {d["report"]["actual_g"]:.1f} g / {d["report"]["count"]} parca' for p,d in data.items())
    status('YUKLEME: '+ ' | '.join(f'{p} {d["report"]["actual_g"]:.1f} g / {d["report"]["count"]} parca' for p,d in data.items()))
    paths={}
    def progress(p,i,n):
        if cancel:raise InterruptedError('Kullanici iptal etti')
        status(f'CAD haznesine yukleniyor: {p} {i}/{n}');app.update()
    # Author food in an unobserved layer. Hydra must not rebuild its render
    # scene for each of ~83,000 individual body definitions. Geometry/physics
    # are identical; the completed layer is composed once, before reset.
    if args.food_layer:
        food_path=Path(args.food_layer).resolve()
        previous=json.loads((food_path.parent/'request.json').read_text())
        assert all(previous[k]==cfg[k] for k in ['fill_percent','mode','seed']),'Initial charge settings do not match'
        check=Usd.Stage.Open(str(food_path))
        for p in PRODUCTS:
            paths[p]=[f'/World/FOOD_{p}/p_{i:06d}' for i in range(len(data[p]['mass_kg']))]
            for i in [0,len(paths[p])//2,len(paths[p])-1] if paths[p] else []:
                prim=check.GetPrimAtPath(paths[p][i]);assert prim.IsValid()
                assert np.allclose(prim.GetAttribute('xformOp:translate').Get(),data[p]['points'][i])
                assert np.isclose(prim.GetAttribute('physics:mass').Get(),data[p]['mass_kg'][i])
                assert np.allclose(check.GetPrimAtPath(paths[p][i]+'/shape').GetAttribute('xformOp:scale').Get(),data[p]['dimensions'][i])
        status('Hazir BASLANGIC dolumu yuklendi; fizik sifirdan cozulecek.')
    else:
        food_stage=Usd.Stage.CreateInMemory()
        for p in PRODUCTS:
            paths[p]=add_food(food_stage,p,data[p],progress)
            yield
        food_path=run/'food_initial.usdc';food_stage.GetRootLayer().Export(str(food_path))
        del food_stage
    stage.GetSessionLayer().subLayerPaths.append(str(food_path))
    # Save actual charge and experiment layer before any physics steps.
    stage.Flatten().Export(str(run/'initial.usd'))
    world=World(stage_units_in_meters=1.,physics_dt=DT,rendering_dt=1/60,
        physics_prim_path='/World/MAKINE/physicsScene',backend='warp',device='cuda:0')
    world.get_physics_context().enable_gpu_dynamics(flag=True)
    world.get_physics_context().set_broadphase_type('GPU')
    world.get_physics_context().enable_fabric(True)
    # No raycasts are used: tensor positions drive the virtual counters.
    # Skip the separate CPU scene-query acceleration-structure update.
    PhysxSchema.PhysxSceneAPI(stage.GetPrimAtPath('/World/MAKINE/physicsScene')).CreateEnableSceneQuerySupportAttr(False)
    status('PHYSX HAZIRLANIYOR - ilk temaslar hesaplaniyor')
    world.reset();world.step(render=False)
    world.get_physics_context().enable_fabric(True)
    carb.settings.get_settings().set_bool('/physics/updateToUsd',False)
    print('LAB_PHYSICS_SETTINGS',world.get_physics_dt(),carb.settings.get_settings().get('/physics/updateToUsd'),flush=True)
    assert PhysxSchema.PhysxSceneAPI(stage.GetPrimAtPath('/World/MAKINE/physicsScene')).GetEnableGPUDynamicsAttr().Get(),'GPU physics disabled'
    engine_active=True
    sid=UsdUtils.StageCache.Get().GetId(stage).ToLongInt()
    sv=omni.physics.tensors.create_simulation_view('warp',stage_id=sid)
    mv=sv.create_rigid_body_view(machine_paths);mi={p:i for i,p in enumerate(mv.prim_paths)}
    assert set(machine_paths)<=set(mi)
    fv={};fi={}
    for p in PRODUCTS:
        if paths[p]:
            fv[p]=sv.create_rigid_body_view('/World/FOOD_'+p+'/*')
            fi[p]=np.array([int(x.rsplit('_',1)[1]) for x in fv[p].prim_paths])
            assert len(fi[p])==len(paths[p]) and len(set(fi[p]))==len(paths[p])
            actual=fv[p].get_masses().numpy().ravel()
            assert np.allclose(actual,data[p]['mass_kg'][fi[p]],rtol=2e-5),'Physics mass differs from loaded mass'
    md=mv.get_transforms().numpy();food={p:np.empty((0,7)) for p in PRODUCTS}
    prev={p:None for p in PRODUCTS};crossed={p:set() for p in PRODUCTS};phase_cross=set();phase=None
    logs=[];phase_reports=[];tick=0
    initial_pide=md[mi['/World/PIDE'],:3].copy()
    assert abs(.9+md[mi[MY+'/ARABA'],0]-.220)<.002,'Table must start left'
    status('CANLI FIZIK: urunler haznede dengeleniyor')

    def mass(p,indices):
        return float(data[p]['mass_kg'][list(indices)].sum()*1000) if len(indices) else 0.

    def sample():
        nonlocal md,food,prev
        md=mv.get_transforms().numpy().copy();pp=md[mi['/World/PIDE'],:3]
        result={}
        for p in PRODUCTS:
            if p in fv:
                ordered=np.empty((len(paths[p]),7),np.float32);ordered[fi[p]]=fv[p].get_transforms().numpy();food[p]=ordered
            xyz=food[p][:,:3];pc=PRODUCTS[p]
            if prev[p] is not None and len(xyz):
                cross=(prev[p][:,2]>=.160)&(xyz[:,2]<.160)&(abs(xyz[:,0]-pc['x'])<.04)&(abs(xyz[:,1]-pc['nozzle_y'])<.04)
                ids=set(np.flatnonzero(cross).tolist());crossed[p].update(ids)
                if phase==p:phase_cross.update(ids)
            prev[p]=xyz.copy()
            rr=np.linalg.norm(xyz[:,:2]-pp[:2],axis=1)
            on=(rr<.140)&(xyz[:,2]>pp[2])&(xyz[:,2]<pp[2]+.040)
            below=(xyz[:,2]<.160)
            rings=np.histogram(rr[on],np.sqrt(np.linspace(0,.125**2,6)),weights=data[p]['mass_kg'][on]*1000)[0]
            result[p]=dict(on_pide_g=float(data[p]['mass_kg'][on].sum()*1000),
                outside_or_below_g=float(data[p]['mass_kg'][below&~on].sum()*1000),
                crossed_total_g=mass(p,crossed[p]),remaining_above_exit_g=float(data[p]['mass_kg'][~below].sum()*1000),
                ring_mass_g=rings.tolist(),ring_cv_percent=float(rings.std()/rings.mean()*100) if rings.sum() else None)
        vel=mv.get_velocities().numpy()
        rpm={p:float(vel[mi[MY+'/HELEZON_'+pc['slot']],4]*60/(2*math.pi)) for p,pc in PRODUCTS.items()}
        rpm['table']=float(vel[mi[MY+'/TABLA'],5]*60/(2*math.pi))
        return dict(t=tick*DT,phase=phase or 'MOVE_SETTLE',products=result,actual_rpm=rpm,table_x=float(.9+md[mi[MY+'/ARABA'],0]),pide=pp.tolist())

    latest=sample()
    profiler=None
    if args.profile_steps:
        import cProfile
        profiler=cProfile.Profile();profiler.enable()
    def step():
        nonlocal tick,md,latest
        if cancel:raise InterruptedError('Kullanici iptal etti')
        world.step(render=False);tick+=1
        if tick%8==0:md=mv.get_transforms().numpy().copy()
        if tick%24==0:
            latest=sample();logs.append(latest)
        if tick%480==0:
            status(f'{phase or "KONUM/DENGELE"} | sim {tick*DT:.1f} sn / hesap {time.monotonic()-started:.0f} sn | '+ ' | '.join(f'{p}: pide {latest["products"][p]["on_pide_g"]:.1f} g' for p in PRODUCTS))
        if profiler is not None and tick>=args.profile_steps:
            import io,pstats
            profiler.disable();stream=io.StringIO();pstats.Stats(profiler,stream=stream).sort_stats('cumtime').print_stats(35)
            (run/'profile.txt').write_text(stream.getvalue(),encoding='utf-8')
            print('LAB_PROFILE',stream.getvalue(),flush=True)
            raise InterruptedError('PERFORMANCE_PROBE_ONLY - not a dosing result')

    def move(x,limit=.2,seconds=15.):
        for _ in range(round(seconds/DT)):
            error=x-(.9+md[mi[MY+'/ARABA'],0]);drive(stage,'X','linear',np.clip(12*error,-limit,limit))
            step();yield
            if abs(error)<.0005:break
        else:raise RuntimeError('Tabla istenen konuma ulasamadi')
        drive(stage,'X','linear',0)
        for _ in range(120):step();yield

    for _ in range(round(args.settle/DT)):step();yield
    preload=sample()
    if not args.settle_only:
        for p in RECIPES[cfg['recipe']]:
            pc=PRODUCTS[p];target=cfg['doses_g'][p]
            dry=cfg.get('dry_run',False)
            if not dry and data[p]['report']['actual_g']<target:
                phase_reports.append(dict(product=p,status='INSUFFICIENT_STOCK',target_g=target));continue
            yield from move(radius_x(p,0))
            phase=p;phase_cross.clear();begin=tick*DT
            drive(stage,'TABLA','angular',pc['table_rpm']*6)
            drive(stage,'HELEZON_'+pc['slot'],'angular',pc['rpm']*6)
            drive(stage,'KARISTIRICI_'+pc['slot'],'angular',24.)
            status('DOZ: '+p+' - hareket gercek PhysX temasindan olusuyor')
            reason='TIME_LIMIT'
            for _ in range(round(args.max_dose_seconds/DT)):
                delivered=mass(p,phase_cross)
                if dry:
                    delivered=min(target,target*(tick*DT-begin)/10.)
                    if tick*DT-begin>=10.:reason='EMPTY_MOTION_ONLY';break
                if delivered>=target:reason='TARGET_COUNTER';break
                x=radius_x(p,delivered/target)
                drive(stage,'X','linear',np.clip(12*(x-(.9+md[mi[MY+'/ARABA'],0])),-.05,.05))
                step();yield
            for stem in ('HELEZON_','KARISTIRICI_'):drive(stage,stem+pc['slot'],'angular',0.)
            dose_time=tick*DT-begin
            # Continue the position loop while the remaining food falls.
            # Keeping the last velocity command would carry the tray to the
            # rail limit and turn a correct nozzle dose into spilled product.
            for _ in range(round(3/DT)):
                x=radius_x(p,1. if dry else mass(p,phase_cross)/target)
                drive(stage,'X','linear',np.clip(12*(x-(.9+md[mi[MY+'/ARABA'],0])),-.05,.05))
                step();yield
            drive(stage,'X','linear',0);drive(stage,'TABLA','angular',0)
            final_x=float(.9+md[mi[MY+'/ARABA'],0])
            target_x=radius_x(p,1. if dry else mass(p,phase_cross)/target)
            assert abs(final_x-target_x)<.002,'Tray tail-hold position did not converge'
            phase_reports.append(dict(product=p,status=reason,target_g=target,virtual_counter_g=mass(p,phase_cross),dose_seconds=dose_time,table_x=final_x,table_target_x=target_x))
            phase=None
    stop_motors(stage)
    for _ in range(round(.5/DT)):step();yield
    latest=sample();world.pause()
    for p in RECIPES[cfg['recipe']]:
        latest['products'][p]['target_g']=cfg['doses_g'][p]
        latest['products'][p]['dose_error_percent']=None if cfg.get('dry_run') else 100*(latest['products'][p]['on_pide_g']/cfg['doses_g'][p]-1)
    # Store final physical state, not an invented trajectory. CAD/food source
    # hashes and every setting make the next START a reproducible experiment.
    report=dict(settings=cfg,charges=summary,phases=phase_reports,preload=preload,last=latest,
        simulated_seconds=tick*DT,wall_seconds=time.monotonic()-started,dt=DT,
        actual_physics='PhysX GPU rigid body + closed SDF screw',live_not_replay=True,
        initial_food_layer=str(food_path),initial_food_layer_sha256=hashlib.sha256(food_path.read_bytes()).hexdigest(),
        assembly_audit=json.loads((OUT/f'assembly_{cfg["variant"]}.json').read_text()),
        feedback_is_virtual=True,food_is_uncalibrated=True,measurements=logs,
        run_kind='EMPTY_MOTION_ONLY' if cfg.get('dry_run') else 'UNCALIBRATED_FOOD_EXPERIMENT',
        source_hashes=SOURCE_HASHES,
        limitations=['Rigid food: no crushing, adhesion, spoilage or calibration.',
            'Mass counter is virtual, not installed hardware.',
            'Full initial charge does not prove 48 h operation. Settled fill level can decrease.',
            'Assembly fixture excludes refrigeration and structural housing.',
            'Floor catches spills. No escaped food is deleted.',
            'Dough and tray contact approximations need real validation.'])
    arrays={}
    for p in PRODUCTS:arrays.update({p+'_pose':food[p],p+'_mass_kg':data[p]['mass_kg'],p+'_dimensions':data[p]['dimensions']})
    np.savez_compressed(run/'final_state.npz',**arrays,machine_pose=md,machine_paths=mv.prim_paths)
    (run/'result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (OUT/'last_run.json').write_text(json.dumps(dict(tag=tag,path=str(run/'result.json')),indent=2),encoding='utf-8')
    get_physx_interface().update_transformations(True,True,True,False)
    reasons={'TIME_LIMIT':'SURE SINIRI - hedef tamamlanmadi','INSUFFICIENT_STOCK':'STOK YETERSIZ',
             'TARGET_COUNTER':'Sanal cikis hedefi','EMPTY_MOTION_ONLY':'BOS HAREKET TESTI'}
    warnings=[r['product']+': '+reasons.get(r['status'],r['status']) for r in phase_reports
              if r['status'] in ('TIME_LIMIT','INSUFFICIENT_STOCK')]
    status(('DENEY BITTI / '+ '; '.join(warnings) if warnings else 'DENEY BITTI')+' | '+
           ' | '.join(f'{p}: {latest["products"][p]["on_pide_g"]:.1f} g' for p in PRODUCTS))
    if result_label:
        result_label.text='SONUC: '+tag+'\n'+ '\n'.join(
            f'{r["product"]}: pide {latest["products"][r["product"]]["on_pide_g"]:.1f} g / '
            f'hedef {r["target_g"]:.1f} g; {reasons.get(r["status"],r["status"])}' for r in phase_reports)
    print('LAB_RESULT',str(run/'result.json'),flush=True)

def ui_start():
    global pending,cancel,paused
    if job is not None:status('Once mevcut deneyi bitir veya IPTAL et.');return
    try:
        pending=settings(['kasar','sucuk','karisik'][recipe_ui.model.get_item_value_model().as_int],
            ['hazne','stok'][mode_ui.model.get_item_value_model().as_int],fill_ui['kasar'].model.as_float,fill_ui['sucuk'].model.as_float,
            ['candidate','baseline'][variant_ui.model.get_item_value_model().as_int],
            kasar_g=dose_ui['kasar'].model.as_float,sucuk_g=dose_ui['sucuk'].model.as_float)
    except (ValueError,AssertionError) as exc:
        status('GIRIS HATASI: '+str(exc));return
    cancel=False;paused=False

def ui_pause():
    global paused
    if world and job:
        paused=not paused
        if paused:world.pause();status('DURAKLATILDI - fizik zamani ilerlemiyor')
        else:world.play();status('CANLI FIZIK DEVAM')

def ui_cancel():
    global cancel,paused
    cancel=True;paused=False
    if world:world.play()
    status('IPTAL ISTENDI - sonuc basarili sayilmayacak')

def ui_dry_start():
    ui_start()
    if pending is not None:
        pending['dry_run']=True;pending['fill_percent']={p:0. for p in PRODUCTS}

def preset(value,mode=0):
    mode_ui.model.get_item_value_model().set_value(mode)
    for f in fill_ui.values():f.model.set_value(value)

open_empty(args.variant)
if not args.headless:
    import omni.ui as ui
    window=ui.Window('TOPPING LAB V1 - CANLI PHYSX',width=480,height=790)
    fill_ui={};dose_ui={}
    with window.frame,ui.ScrollingFrame():
        with ui.VStack(spacing=7):
            ui.Label('YENI DENEY - KAYIT OYNATMA DEGIL',height=25)
            ui.Label('Yalniz tabla + kasar + kup sucuk. Tabla soldan baslar.',height=35,word_wrap=True)
            ui.Label('Gida temasi VARSAYIM; gram sayaci SANAL. Tam dolum saatler surebilir.',height=35,word_wrap=True)
            recipe_ui=ui.ComboBox(['kasar','sucuk','karisik'].index(args.recipe),'YALNIZ KASAR','YALNIZ SUCUK','KASAR + SUCUK (ayni pide)',height=28)
            mode_ui=ui.ComboBox(['hazne','stok'].index(args.mode),'HAZNE DOLUMU % (baslangic paketleme)','IKI GUNLUK STOK % (8.8 kg / 2.8 kg)',height=28)
            for p in PRODUCTS:
                with ui.HStack(height=25):
                    ui.Label(p.upper()+' DOLULUK %',width=155);fill_ui[p]=ui.FloatField();fill_ui[p].model.set_value(getattr(args,p))
                with ui.HStack(height=25):
                    ui.Label(p.upper()+' HEDEF g',width=155);dose_ui[p]=ui.FloatField();dose_ui[p].model.set_value(PRODUCTS[p]['target_g'])
            with ui.HStack(height=28,spacing=5):
                ui.Button('%10',clicked_fn=lambda:preset(10));ui.Button('%50',clicked_fn=lambda:preset(50));ui.Button('%100 HAZNE',clicked_fn=lambda:preset(100));ui.Button('2 GUN STOK',clicked_fn=lambda:preset(100,1))
            variant_ui=ui.ComboBox(['candidate','baseline'].index(args.variant),'YENI VIDA / CIKIS (V2)','ESKI VIDA REFERANSI (A/B deneyi)',height=28)
            ui.Button('CANLI DENEY BASLAT',height=38,clicked_fn=ui_start)
            ui.Button('BOS HAREKET TESTI (gida yok)',height=28,clicked_fn=ui_dry_start)
            with ui.HStack(height=32,spacing=6):
                ui.Button('DURAKLAT / DEVAM',clicked_fn=ui_pause);ui.Button('IPTAL',clicked_fn=ui_cancel)
            status_label=ui.Label(status_text,height=65,word_wrap=True)
            charge_label=ui.Label('Yuklenen gram ve parca sayisi burada gosterilir.',height=45,word_wrap=True)
            result_label=ui.Label('Henuz yeni deney sonucu yok.',height=100,word_wrap=True)
            ui.Label('UYARI: Gida temaslari VARSAYIM. Ezilme/yapisma ve 48 saat kanitlanmis degil. Gram sayaci SANAL; fiziksel sensor yok.',height=65,word_wrap=True)
            ui.Label('%100: guvenli dolum cizgisine kadar baslangic yuklemesi. Cozuldukce seviye oturabilir. Gercek yuklenen gram ve parca sayisi yazilir. Buyuk dolumlar agir hesaplanir.',height=75,word_wrap=True)
    app.update()
    window.position_x=max(0,ui.Workspace.get_main_window_width()-window.width-15)
    window.position_y=45

if args.headless:pending=settings(args.recipe,args.mode,args.kasar,args.sucuk,args.variant,dry_run=args.dry_run)
elif args.auto_start:
    if args.dry_run:ui_dry_start()
    else:ui_start()
print('LAB_PANEL_READY',flush=True)
if args.preview_only:
    from omni.kit.viewport.utility import get_active_viewport,capture_viewport_to_file
    for _ in range(60):app.update()
    capture=capture_viewport_to_file(get_active_viewport(),str(OUT/'assembly_preview.png'))
    for _ in range(45):app.update()
    assert (OUT/'assembly_preview.png').exists(),'Viewport capture failed'
    assert recipe_ui.model.get_item_value_model().as_int==['kasar','sucuk','karisik'].index(args.recipe)
    assert all(abs(fill_ui[p].model.as_float-getattr(args,p))<1e-5 for p in PRODUCTS)
    # Exercise the same callbacks wired to the user's buttons without starting
    # an expensive physics run. Invalid input cannot queue an experiment.
    fill_ui['kasar'].model.set_value(-1.);ui_start();assert pending is None
    preset(50);recipe_ui.model.get_item_value_model().set_value(2);ui_start()
    assert pending['recipe']=='karisik' and pending['fill_percent']=={'kasar':50.,'sucuk':50.}
    pending=None;preset(100,1);ui_start()
    assert pending['mode']=='stok' and pending['fill_percent']['sucuk']==100.
    pending=None;ui_dry_start()
    assert pending['dry_run'] and pending['fill_percent']=={'kasar':0.,'sucuk':0.}
    pending=None
    print('LAB_UI_SMOKE_PASS',flush=True)
    app.close();raise SystemExit(0)
exit_code=0
try:
    while app.is_running():
        if pending is not None and job is None:
            cfg=pending;pending=None;cancel=False;paused=False;engine_active=False
            tag=args.tag or datetime.now().strftime('%Y%m%d_%H%M%S')
            args.tag=''
            job=experiment(cfg,tag)
        if job is not None and engine_active and world and not world.is_playing() and not paused:
            paused=True;status('ISAAC DURAKLATILDI - panelden DEVAM edebilirsin')
        if job is not None and not paused:
            try:
                # Render/UI cadence follows wall time, not 60 expensive RTX
                # draws per simulated second. Physics dt and contacts do not
                # change. Also keep pause/cancel responsive on heavy loads.
                chunk_start=time.monotonic()
                for _ in range(48):
                    next(job)
                    if not args.headless and time.monotonic()-chunk_start>=.12:break
            except StopIteration:
                job=None;engine_active=False
                if args.headless or args.exit_after_result:break
            except Exception as exc:
                traceback.print_exc();status('DENEY TAMAMLANMADI: '+str(exc));job=None;exit_code=1;engine_active=False
                failure=OUT/'runs'/tag/'aborted.json'
                failure.parent.mkdir(parents=True,exist_ok=True)
                failure.write_text(json.dumps(dict(status='ABORTED',reason=str(exc)),indent=2),encoding='utf-8')
                if world:
                    stop_motors(omni.usd.get_context().get_stage());world.pause()
                if args.headless or args.exit_after_result:break
            if world and not args.headless:world.render()
        else:app.update()
finally:
    if world:world.stop()
    app.close()
raise SystemExit(exit_code)
