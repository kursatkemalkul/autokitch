# -*- coding: utf-8 -*-
"""KUPLER NEREDE? — 0 g cikmasinin sebebini OLCEREK bul

C:\\isaacsim\\python.bat kup_teshis_v1.py

Varsayim yok: kupleri haznede birak, nerede durduklarini say. Uc ihtimal:
  a) kupler govdenin ICINE hic girmedi (sinirda spawn edildi, disari itildiler)
  b) helezonun ustunde duruyorlar ama kanat araligina GIREMIYORLAR (carpisma bicimi)
  c) gercekten kopruleme var
"""
import json, math, os, random

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
MY = "/World/MAKINE/TOPPING"
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

print("\n=== A · KASET GOVDESININ CARPISMA BICIMI ===")
kg = st.GetPrimAtPath(MY + "/SABIT")
sayim = {}
for c in kg.GetChildren():
    if "KUP_SUCUK" not in c.GetName(): continue
    mc = UsdPhysics.MeshCollisionAPI(c)
    ap = mc.GetApproximationAttr().Get() if mc else None
    sayim[str(ap)] = sayim.get(str(ap), 0) + 1
print("   KÜP SUCUK sabit parcalarinin carpisma bicimi:", sayim)

gov = st.GetPrimAtPath(MY + "/SABIT/KUP_SUCUK_govde")
print("   govde prim:", gov.IsValid())
if gov.IsValid():
    pts = UsdGeom.Mesh(gov).GetPointsAttr().Get()
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
    print("   govde x %.3f..%.3f  y %.3f..%.3f  z %.3f..%.3f  (%d nokta)" % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs), len(pts)))

print("\n=== B · HELEZON PARCALARI ===")
hg = st.GetPrimAtPath(MY + "/HELEZON_KUP_SUCUK")
print("   grup gecerli:", hg.IsValid(), "· rijit:", hg.HasAPI(UsdPhysics.RigidBodyAPI))
for c in hg.GetChildren():
    mc = UsdPhysics.MeshCollisionAPI(c)
    pts = UsdGeom.Mesh(c).GetPointsAttr().Get()
    if not pts: continue
    ys = [p[1] for p in pts]
    print("   %-22s %-20s y %.3f..%.3f" % (c.GetName(), mc.GetApproximationAttr().Get() if mc else "?", min(ys), max(ys)))

print("\n=== C · KUPLERI BIRAK, NEREDE DURDUKLARINI SAY ===")
mp = UsdShade.Material.Define(st, "/World/Malzeme_Sucuk")
m = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
m.CreateStaticFrictionAttr(0.55); m.CreateDynamicFrictionAttr(0.45); m.CreateRestitutionAttr(0.05)
inc = UsdPhysics.CollisionGroup.Get(st, "/World/CarpismaGrubu_URUN").GetCollidersCollectionAPI().CreateIncludesRel()

KUP, YOG = 0.008, 1050.0
KG = KUP ** 3 * YOG
random.seed(3)
N = 60
yollar = []
for i in range(N):
    p = "/World/KUPLER/kup_%03d" % i
    xf = UsdGeom.Xform.Define(st, p)
    xf.AddTranslateOp().Set(Gf.Vec3d(1.440 + (i % 6) * 0.012, 0.400 + (i // 6) * 0.012, -0.360 + random.uniform(-0.02, 0.02)))
    c = UsdGeom.Cube.Define(st, p + "/ag"); c.CreateSizeAttr(KUP)
    c.CreateDisplayColorAttr([Gf.Vec3f(0.55, 0.16, 0.14)])
    UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
    UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(KG))
    UsdPhysics.CollisionAPI.Apply(c.GetPrim())
    UsdShade.MaterialBindingAPI(c.GetPrim()).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
    cc = PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
    cc.CreateContactOffsetAttr(0.0015); cc.CreateRestOffsetAttr(0.0)
    inc.AddTarget(c.GetPath())
    yollar.append(p)

world = World(stage_units_in_meters=1.0, physics_dt=1/480.0, rendering_dt=1/60.0)
world.reset()


def konumlar():
    L = []
    for p in yollar:
        t = UsdGeom.Xformable(st.GetPrimAtPath(p)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
        L.append((t[0], t[1], t[2]))
    return L


k0 = konumlar()
for s in range(5):
    for _ in range(240): world.step(render=False)
    k = konumlar()
    ys = sorted(t[1] for t in k)
    yerde = sum(1 for t in k if t[1] < 0.05)
    helezonda = sum(1 for t in k if 0.286 <= t[1] <= 0.360)
    ustte = sum(1 for t in k if t[1] > 0.360)
    print("   %.1f s · y en dusuk %.3f · ortanca %.3f · en yuksek %.3f | yerde %d · helezon bandinda %d · ustte %d"
          % ((s+1)*0.5, ys[0], ys[len(ys)//2], ys[-1], yerde, helezonda, ustte))

print("\n   baslangic y = 0,400..0,508 · helezon bandi y 0,286..0,354 · govde tabani y 0,281")
kk = konumlar()
disari = sum(1 for t in kk if not (1.402 <= t[0] <= 1.542 and -0.525 <= t[2] <= -0.200))
print("   govde x/z sinirlari DISINDA kalan kup: %d / %d" % (disari, N))
print("\nBITTI")
app.close()
