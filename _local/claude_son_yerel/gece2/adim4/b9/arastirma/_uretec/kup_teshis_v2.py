# -*- coding: utf-8 -*-
"""KUPLERI NE TUTUYOR? — asagi isin atip ENGELIN ADINI ogren

C:\\isaacsim\\python.bat kup_teshis_v2.py
"""
import os

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, Gf
from isaacsim.core.api import World
from omni.physx import get_physx_scene_query_interface

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
MY = "/World/MAKINE/TOPPING"
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

world = World(stage_units_in_meters=1.0, physics_dt=1 / 480.0, rendering_dt=1 / 60.0)
world.reset()
for _ in range(60): world.step(render=False)

q = get_physx_scene_query_interface()

print("\n=== HAZNE ICINDE ASAGI ISIN — ne var, hangi kotta? ===")
print("   (helezon bandi y 0,286..0,354 · govde tabani y 0,281)")
print("   %-10s %-10s %-9s %s" % ("x", "z", "carpma y", "parca"))
for x in (1.440, 1.460, 1.472, 1.490, 1.510):
    for z in (-0.450, -0.360, -0.260):
        h = q.raycast_closest(carb_v(x, 0.500, z) if False else [x, 0.500, z], [0.0, -1.0, 0.0], 0.6)
        if h and h.get("hit"):
            print("   %-10.3f %-10.3f %-9.4f %s" % (x, z, h["position"][1], h["rigidBody"] or h.get("collision", "?")))
        else:
            print("   %-10.3f %-10.3f %-9s %s" % (x, z, "-", "ISIN HICBIR SEYE CARPMADI"))

print("\n=== AYNI NOKTALARDA YUKARI ISIN (tavan var mi?) ===")
for x in (1.472,):
    for z in (-0.450, -0.360, -0.260):
        h = q.raycast_closest([x, 0.300, z], [0.0, 1.0, 0.0], 0.4)
        print("   x %.3f z %.3f -> %s" % (x, z, (("%.4f  %s" % (h["position"][1], h["rigidBody"])) if h and h.get("hit") else "tavan yok")))

print("\nBITTI")
app.close()
