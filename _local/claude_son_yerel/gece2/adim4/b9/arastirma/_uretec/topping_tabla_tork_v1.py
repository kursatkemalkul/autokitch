# -*- coding: utf-8 -*-
"""TABLA MOTORU YETIYOR MU? — Isaac Sim'de olculur

Bu, tarayici simulasyonunun ASLA cevaplayamadigi soru: Ø340 tabla + tepsi + urun, pancake
NEMA23 (0,9 N·m, i=1) ile 35 dev/dk'ya kac saniyede cikar, ve cikabilir mi?
Hesapta "gereken 0,169 N·m" yaziyordu ama o RAMPA ataletini icermiyordu.

C:\\isaacsim\\python.bat topping_tabla_tork_v1.py
"""
import math

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom
from isaacsim.core.api import World

USD = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik\TOPPING_fizik_v3.usd"
omni.usd.get_context().open_stage(USD); app.update(); app.update()
stage = omni.usd.get_context().get_stage()
world = World(stage_units_in_meters=1.0, physics_dt=1.0 / 480.0, rendering_dt=1.0 / 60.0)
world.reset()

EK = "/World/TOPPING/EKLEM_TABLA"
DT = 1.0 / 480.0


def tork_ayarla(nm):
    stage.GetPrimAtPath(EK).GetAttribute("drive:angular:physics:maxForce").Set(float(nm))


def hedef(dps):
    stage.GetPrimAtPath(EK).GetAttribute("drive:angular:physics:targetVelocity").Set(float(dps))


def aci():
    m = UsdGeom.Xformable(stage.GetPrimAtPath("/World/TOPPING/TABLA")).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    q = m.ExtractRotationQuat()
    return math.degrees(2.0 * math.atan2(q.GetImaginary()[1], q.GetReal()))


def dene(nm, sure=4.0):
    tork_ayarla(nm); hedef(0.0)
    for _ in range(240): world.step(render=False)
    hedef(35.0 * 6.0)
    onc, t, t95, en_yuksek = aci(), 0.0, None, 0.0
    n = int(sure / DT)
    for i in range(n):
        world.step(render=False); t += DT
        a = aci()
        w = ((a - onc + 540) % 360 - 180) / DT
        onc = a
        if i > 20:
            en_yuksek = max(en_yuksek, w)
            if t95 is None and w > 0.95 * 210.0: t95 = t
    hedef(0.0)
    for _ in range(120): world.step(render=False)
    return t95, en_yuksek


print("\n   tabla 5,11 kg · Ø340 · hedef 35 dev/dk (210 derece/s)")
print("   %-12s %-16s %-18s %s" % ("motor torku", "%95'e cikis", "ulasilan devir", "sonuc"))
for nm in (0.30, 0.50, 0.90, 1.50, 3.00):
    t95, w = dene(nm)
    print("   %-12s %-16s %-18s %s" % (
        "%.2f N·m" % nm,
        ("%.3f s" % t95) if t95 else "ULASAMADI",
        "%.1f dev/dk" % (w / 6.0),
        "YETER" if t95 and t95 < 0.5 else ("SINIRDA" if t95 else "YETMEZ")))

print("\nBITTI")
app.close()
