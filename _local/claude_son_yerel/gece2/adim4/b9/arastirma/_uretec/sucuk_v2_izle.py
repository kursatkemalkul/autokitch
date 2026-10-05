"""Separate V2 viewer. Explicitly recorded PhysX results, not a fresh solve."""
from pathlib import Path
src=Path(__file__).with_name('sucuk_deney_izle_v1.py').read_text(encoding='utf-8')
def rep(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a));src=src.replace(a,b)
rep("default='tam_stok_gpu'","default='full_candidate_balanced_03'")
rep("args=p.parse_args()","p.add_argument('--top',action='store_true')\nargs=p.parse_args()")
rep("OUT=ROOT/('arastirma/3_TOPPING/sucuk_fizik_deney_'+args.version)","OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2/runs'")
rep("'SUCUK - PHYSX DENEY KAYDI'","'SUCUK V2 - AYRI DENEY'")
rep("height=450)","height=485)")
rep("'8 mm kup / yogunluk ve surtunme VARSAYIM'","'6-10 mm / sonumlu temas / gida verileri VARSAYIM'")
rep("status=ui.Label('',height=42,word_wrap=True)","ui.Label('Kayit dozaj bolumudur; dolum/gecis kayit disi.',height=25)\n        status=ui.Label('',height=42,word_wrap=True)")
rep("'Hesap kodu: sucuk_fizik_deney_'+args.version+'.py\\nTemas ve gida verileri fiziksel deneyle dogrulanmadi.'", "'Hesap: sucuk_v2_deney.py\\nYeni vida ucu / SDF temas. Ezilme testi degildir.'")
rep("keep=('KUP_SUCUK' in path or '/TABLA/' in path or '/ARABA/' in path)",
    "keep=('KUP_SUCUK' in path or '/TABLA/' in path or '/ARABA/' in path or '/V2_candidate_tube' in path)")
rep("def camera(close=True):\n    set_camera_view", "def camera(close=True):\n    state['top_mode']=False\n    if hidden:focus()\n    set_camera_view")
rep("def play():", """def top_view():
    state['top_mode']=True
    state['play']=False;state['time']=float(ts[-1]);slider.model.set_value(state['time'])
    frame(len(ts)-1)
    p=data['xyz'][-1,paths.index('/World/PIDE')]
    set_camera_view(eye=np.array([p[0],p[1]-.001,.80]),target=np.array([p[0],p[1],p[2]]))
    # Occluding machine body is hidden only for this inspection view.
    if not hidden:focus()
    for prim in stage.Traverse():
        if prim.IsA(UsdGeom.Mesh) and '/MAKINE/TOPPING/' in str(prim.GetPath()):
            im=UsdGeom.Imageable(prim)
            if im.GetVisibilityAttr().Get()!='invisible':
                hidden.append((prim,im.GetVisibilityAttr().Get()));im.MakeInvisible()
    for j,path in enumerate(paths):
        if '/SUCUK_CUBES/' in path and xyz[-1,j,2]>.160:
            im=UsdGeom.Imageable(stage.GetPrimAtPath(path))
            if im.GetVisibilityAttr().Get()!='invisible':
                hidden.append((im.GetPrim(),im.GetVisibilityAttr().Get()));im.MakeInvisible()

def play():""")
rep("def play():state['play']=not state['play']", "def play():\n    if state.get('top_mode'):camera(True);focus()\n    state['play']=not state['play']")
rep("camera();frame(0)", "camera();frame(0)\nif args.top:top_view()\nelif not args.headless:focus()")
rep("ui.Button('DIGER PARCALARI GIZLE / GOSTER',clicked_fn=focus,height=30)",
    "ui.Button('DIGER PARCALARI GIZLE / GOSTER',clicked_fn=focus,height=30)\n        ui.Button('SONUCU USTTEN GOSTER',clicked_fn=top_view,height=30)")
rep("focus();frame(len(ts)-1)","\n        if not args.top:focus()\n        frame(len(ts)-1)")
rep("args.tag+'_view.png'","args.tag+('_top.png' if args.top else '_view.png')")
exec(compile(src,__file__,'exec'),globals())
