# -*- coding: utf-8 -*-
"""TOPPING fizikli USD — CALISIYOR MU? (dogrulama)

C:\\isaacsim\\python.bat topping_usd_test_v1.py

Sahneyi acar, fizigi calistirir ve OLCER:
  1) araba X'te surulunce gercekten kayiyor mu, hangi hizda
  2) tabla ve kaset milleri surulunce gercekten donuyor mu, kac dev/dk
  3) serbest birakilinca sahne kararli mi (parca ucuyor mu, titriyor mu)
"""
import math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, Gf
from isaacsim.core.api import World

USD = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik\TOPPING_fizik_v5.usd"

omni.usd.get_context().open_stage(USD)
app.update(); app.update()
stage = omni.usd.get_context().get_stage()

world = World(stage_units_in_meters=1.0, physics_dt=1.0 / 240.0, rendering_dt=1.0 / 60.0)
world.reset()


def surucu(eklem_adi, tip, hiz):
    p = stage.GetPrimAtPath("/World/TOPPING/EKLEM_" + eklem_adi)
    if not p.IsValid(): return False
    a = p.GetAttribute("drive:%s:physics:targetVelocity" % tip)
    a.Set(float(hiz))
    return True


def konum(grup):
    p = stage.GetPrimAtPath("/World/TOPPING/" + grup)
    m = UsdGeom.Xformable(p).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    t = m.ExtractTranslation()
    r = m.ExtractRotationQuat()
    return t, r


def aci_y(q):
    # Y ekseni etrafindaki donus acisi (derece)
    im = q.GetImaginary()
    return math.degrees(2.0 * math.atan2(im[1], q.GetReal()))


def aci_z(q):
    im = q.GetImaginary()
    return math.degrees(2.0 * math.atan2(im[2], q.GetReal()))


print("\n=== 1 · SERBEST 1 SANIYE (kararlilik) ===")
t0, _ = konum("ARABA")
for _ in range(240): world.step(render=False)
t1, _ = konum("ARABA")
print("araba kayma (surucu kapali): dx=%.4f dy=%.4f dz=%.4f m" % (t1[0]-t0[0], t1[1]-t0[1], t1[2]-t0[2]))

print("\n=== 2 · ARABA X'TE 200 mm/s SURULUYOR ===")
surucu("X", "linear", 0.200)
a0, _ = konum("ARABA")
for _ in range(240): world.step(render=False)
a1, _ = konum("ARABA")
dx = a1[0] - a0[0]
print("1 saniyede x: %.1f mm  (hedef 200 mm)  -> %s" % (dx*1000, "TUTTU" if abs(dx*1000-200) < 25 else "TUTMADI"))
surucu("X", "linear", 0.0)
for _ in range(60): world.step(render=False)

print("\n=== 3 · TABLA 35 dev/dk ===")
w = 35.0 * 6.0        # dev/dk -> derece/s
surucu("TABLA", "angular", w)
_, q0 = konum("TABLA")
for _ in range(240): world.step(render=False)
_, q1 = konum("TABLA")
d = (aci_y(q1) - aci_y(q0)) % 360.0
print("1 saniyede tabla: %.1f derece  (hedef %.1f)  -> %s" % (d, w, "TUTTU" if abs(d-w) < 30 else "TUTMADI"))
surucu("TABLA", "angular", 0.0)

print("\n=== 4 · KASET MILLERI ===")
for g, rpm in (("HELEZON_KASAR_KABI", 42.0), ("KARISTIRICI_KASAR_KABI", 4.0),
               ("KARISTIRICI_HARC_1", 26.0), ("HELEZON_KIYMA", 14.0)):
    if not surucu(g, "angular", rpm*6.0):
        print("  %-24s EKLEM YOK" % g); continue
    _, r0 = konum(g)
    for _ in range(240): world.step(render=False)
    _, r1 = konum(g)
    d = (aci_z(r1) - aci_z(r0)) % 360.0
    olculen = d / 6.0
    print("  %-24s %5.1f dev/dk olculdu (hedef %.1f) -> %s" % (g, olculen, rpm, "TUTTU" if abs(olculen-rpm) < max(3, rpm*0.15) else "TUTMADI"))
    surucu(g, "angular", 0.0)
    for _ in range(30): world.step(render=False)

print("\n=== 5 · ARABA ATALETI: 0 -> 200 mm/s ne kadar surede ===")
surucu("X", "linear", 0.200)
b0, _ = konum("ARABA"); hedef = 0.200
t_ = 0.0
onceki = b0[0]
for i in range(480):
    world.step(render=False); t_ += 1/240.0
    p_, _ = konum("ARABA")
    v = (p_[0] - onceki) * 240.0
    onceki = p_[0]
    if v > 0.95*hedef:
        print("  %.3f s'de %%95 hiza ulasti (%.0f mm/s)" % (t_, v*1000)); break
else:
    print("  2 saniyede %%95 hiza ULASAMADI")
surucu("X", "linear", 0.0)

print("\nTEST BITTI")
app.close()
