# -*- coding: utf-8 -*-
"""TEPSI TABLAYA OTURUYOR MU? — teshis

Cevrim testinde tepsi tablanin icinden gecti. Sebebi buluyoruz: carpisma grubu mu,
tablanin carpisma bicimi mi, yoksa tablanin kendisi mi ince kaliyor.

C:\\isaacsim\\python.bat tepsi_temas_teshis_v1.py
"""
import math, os

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

print("\n=== A · CARPISMA GRUPLARI ===")
for p in st.Traverse():
    if p.IsA(UsdPhysics.CollisionGroup):
        cg = UsdPhysics.CollisionGroup(p)
        f = cg.GetFilteredGroupsRel().GetTargets()
        inc = cg.GetCollidersCollectionAPI().GetIncludesRel().GetTargets()
        print("  %-46s filtre=%s · uye=%d" % (p.GetPath(), [str(x) for x in f], len(inc)))
        if inc: print("      ilk uye:", inc[0])

print("\n=== B · TABLA PARCALARI (carpisma) ===")
tb = st.GetPrimAtPath("/World/MAKINE/TOPPING/TABLA")
print("  TABLA prim gecerli:", tb.IsValid(), "· rijit:", tb.HasAPI(UsdPhysics.RigidBodyAPI))
for c in tb.GetChildren():
    mc = UsdPhysics.MeshCollisionAPI(c)
    ap = mc.GetApproximationAttr().Get() if mc else "?"
    m = UsdGeom.Mesh(c)
    pts = m.GetPointsAttr().Get()
    if pts:
        ys = [q[1] for q in pts]
        print("  %-24s carpisma=%-20s y %.4f..%.4f · %d nokta" % (c.GetName(), ap, min(ys), max(ys), len(pts)))

print("\n=== C · TEPSI ===")
tp = st.GetPrimAtPath("/World/TEPSI")
ag = st.GetPrimAtPath("/World/TEPSI/ag")
pts = UsdGeom.Mesh(ag).GetPointsAttr().Get()
ys = [q[1] for q in pts]
print("  tepsi agi yerel y %.4f..%.4f · Xform ofset %s" % (min(ys), max(ys), UsdGeom.Xformable(tp).GetOrderedXformOps()[0].Get()))
print("  carpisma yaklasimi:", UsdPhysics.MeshCollisionAPI(ag).GetApproximationAttr().Get())

print("\n=== D · DUSME DENEYI (surucu kapali, 3 s) ===")
world = World(stage_units_in_meters=1.0, physics_dt=1/240.0, rendering_dt=1/60.0)
world.reset()


def y_of(yol):
    m = UsdGeom.Xformable(st.GetPrimAtPath(yol)).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    return m.ExtractTranslation()[1]


y0 = y_of("/World/TEPSI")
for s in range(6):
    for _ in range(120): world.step(render=False)
    print("  %.1f s  tepsi y = %+8.2f mm   tabla y = %+8.2f mm" % ((s+1)*0.5, y_of("/World/TEPSI")*1000, y_of("/World/MAKINE/TOPPING/TABLA")*1000))

d = (y0 - y_of("/World/TEPSI")) * 1000
print("\n  toplam dusme: %.2f mm  ->  %s" % (d, "OTURDU" if abs(d) < 4 else ("GECTI/DUSTU" if d > 10 else "belirsiz")))
print("\nBITTI")
app.close()
