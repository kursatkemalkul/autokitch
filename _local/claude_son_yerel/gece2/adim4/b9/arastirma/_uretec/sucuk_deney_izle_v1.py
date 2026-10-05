"""Replay recorded PhysX results, not a live physics solve. ASCII panel."""
import argparse, json, time
from pathlib import Path
import numpy as np

p=argparse.ArgumentParser()
p.add_argument('--tag', default='tam_stok_gpu')
p.add_argument('--version', default='v8', choices=['v2','v3','v4','v5','v6','v7','v8'])
p.add_argument('--headless', action='store_true')
args=p.parse_args()
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/('arastirma/3_TOPPING/sucuk_fizik_deney_'+args.version)
data=np.load(OUT/(args.tag+'.npz'))
report=json.loads((OUT/(args.tag+'.json')).read_text())
from isaacsim import SimulationApp
app=SimulationApp({'headless':args.headless,'width':1600,'height':900})
import omni.usd, omni.ui as ui
from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, Gf
from isaacsim.core.utils.viewports import set_camera_view
from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file

omni.usd.get_context().open_stage(str(OUT/(args.tag+'_initial.usd')))
for _ in range(10):app.update()
stage=omni.usd.get_context().get_stage()
stage.SetEditTarget(stage.GetSessionLayer())
# Never start physics during replay: poses are measured in the experiment.
for prim in stage.Traverse():
    if prim.HasAPI(UsdPhysics.RigidBodyAPI):
        UsdPhysics.RigidBodyAPI(prim).CreateRigidBodyEnabledAttr(False)
    if prim.HasAPI(UsdPhysics.CollisionAPI):
        UsdPhysics.CollisionAPI(prim).CreateCollisionEnabledAttr(False)
    if prim.IsA(UsdPhysics.Joint): UsdPhysics.Joint(prim).CreateJointEnabledAttr(False)
UsdLux.DomeLight.Define(stage,'/World/ReplayLight').CreateIntensityAttr(1200)
paths=data['paths'].tolist(); xyz=data['xyz']; quat=data['quat']; ts=data['time']
ops=[]; parents=[]
for path in paths:
    prim=stage.GetPrimAtPath(path)
    xf=UsdGeom.Xformable(prim)
    xf.ClearXformOpOrder()
    ops.append(xf.AddTransformOp(UsdGeom.XformOp.PrecisionDouble,'recorded'))
    parents.append(prim.GetParent())

state={'play':False,'index':-1,'time':0.,'focused':False}
def frame(index):
    if index==state['index']: return
    cache=UsdGeom.XformCache()
    for j,op in enumerate(ops):
        q=quat[index,j]; v=xyz[index,j]
        m=Gf.Matrix4d(1)
        m.SetRotate(Gf.Quatd(float(q[0]),Gf.Vec3d(*[float(a) for a in q[1:]])))
        m.SetTranslateOnly(Gf.Vec3d(*[float(a) for a in v]))
        op.Set(m*cache.GetLocalToWorldTransform(parents[j]).GetInverse())
    state['index']=index

def camera(close=True):
    set_camera_view(eye=np.array([1.93,-.65,.67]) if close else np.array([2.6,-2.0,1.5]),
                    target=np.array([1.46,.26,.31]) if close else np.array([.9,.3,.4]))

hidden=[]
def focus():
    if hidden:
        for prim,old in hidden: UsdGeom.Imageable(prim).GetVisibilityAttr().Set(old)
        hidden.clear();return
    for prim in stage.Traverse():
        path=str(prim.GetPath())
        if prim.IsA(UsdGeom.Mesh) and '/MAKINE/TOPPING/' in path:
            keep=('KUP_SUCUK' in path or '/TABLA/' in path or '/ARABA/' in path)
            if not keep:
                im=UsdGeom.Imageable(prim);hidden.append((prim,im.GetVisibilityAttr().Get()))
                im.MakeInvisible()

def play():state['play']=not state['play']
def reset():state['play']=False;state['time']=0.;slider.model.set_value(0.)
window=ui.Window('SUCUK - PHYSX DENEY KAYDI',width=410,height=450)
with window.frame:
    with ui.VStack(spacing=8):
        ui.Label('FIZIK DENEYININ KAYDI - CANLI COZUM DEGIL',height=24)
        ui.Label('8 mm kup / yogunluk ve surtunme VARSAYIM',height=24)
        ui.Label('Stok %.1f g | hedef 70 g' % report['initial_stock_g'],height=22)
        ui.Label('Son sonuc %.2f g | yukleme kaybi %.2f g' %
                 (report['last']['on_pide_g'],report['pre_dose_leak_g']),height=24)
        ui.Label('URETIM ONAYI DEGIL - DOZ / TEMAS DOGRULAMASI EKSIK',height=24)
        if report['feedback_is_virtual']:
            ui.Label('SANAL CIKIS SAYACI - MAKINEDE SENSOR YOK',height=24)
        status=ui.Label('',height=42,word_wrap=True)
        with ui.HStack(height=30):
            ui.Button('OYNAT / DURAKLAT',clicked_fn=play)
            ui.Button('BASA AL',clicked_fn=reset)
        slider=ui.FloatSlider(min=0,max=float(ts[-1]),height=28)
        with ui.HStack(height=30):
            ui.Button('KASET YAKIN',clicked_fn=lambda:camera(True))
            ui.Button('TUM MAKINE',clicked_fn=lambda:camera(False))
        ui.Button('DIGER PARCALARI GIZLE / GOSTER',clicked_fn=focus,height=30)
        ui.Label('Hesap kodu: sucuk_fizik_deney_'+args.version+'.py\nTemas ve gida verileri fiziksel deneyle dogrulanmadi.',word_wrap=True,height=48)

camera();frame(0)
last=time.monotonic()
capture=None
while app.is_running():
    now=time.monotonic();delta=min(.1,now-last);last=now
    if state['play']:
        state['time']=min(float(ts[-1]),state['time']+delta)
        slider.model.set_value(state['time'])
        if state['time']>=ts[-1]:state['play']=False
    else:state['time']=slider.model.get_value_as_float()
    idx=min(len(ts)-1,int(np.searchsorted(ts,state['time'])))
    frame(idx)
    row=report['measurements'][idx]
    status.text='%.1f sn | cikistan %.1f g | pide ustunde %.1f g' % (ts[idx],row['emitted_g'],row['on_pide_g'])
    app.update()
    if args.headless:
        focus();frame(len(ts)-1)
        for _ in range(60):app.update()
        capture=capture_viewport_to_file(get_active_viewport(),str(OUT/(args.tag+'_view.png')))
        for _ in range(60):app.update()
        print('REPLAY_VERIFIED',len(paths),len(ts),flush=True)
        break
app.close()
