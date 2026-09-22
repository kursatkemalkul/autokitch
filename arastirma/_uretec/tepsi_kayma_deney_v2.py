# -*- coding: utf-8 -*-
"""TEPSI KAYMA DENEYI v2 — IKI TASARIM KARSILASTIRMASI

A) SU ANKI TASARIM : tepsi DUZ tabanli, 3 pim ucuna (Ø10 daire) oturuyor — temas 3 kucuk nokta.
B) CUKURLU TEPSI   : tepsi tablaya TAM oturuyor (pimler cukurlara girmis) — temas Ø340 tam yuzey.
Ayni ivmelerde ikisi de denenir; fark tasarim kararini verir.

Elle hesap: tepsi 1,216 + pide 0,493 = 1,709 kg · mu_d 0,50 -> tutabilecegi kuvvet 8,4 N
-> en cok 4,9 m/s2. Araba gecis hizina 0,033 s'de ciktigi icin ivmesi ~6 m/s2.

C:\\isaacsim\\python.bat tepsi_kayma_deney_v2.py
"""
import math, os

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

mp = UsdShade.Material.Define(st, "/World/FizikMalzeme_Celik")
mat = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
mat.CreateStaticFrictionAttr(0.60)        # kuru celik-celik [V: literatur 0,5-0,8]
mat.CreateDynamicFrictionAttr(0.50)
mat.CreateRestitutionAttr(0.02)

MY = "/World/MAKINE/TOPPING"
hedefler = ["/World/TEPSI/ag", "/World/PIDE/ag", MY + "/TABLA/tabla",
            MY + "/TABLA/merkezleme_pimi_A", MY + "/TABLA/merkezleme_pimi_B", MY + "/TABLA/merkezleme_pimi_C"]
n = 0
for y in hedefler:
    p = st.GetPrimAtPath(y)
    if not p.IsValid():
        print("  YOK:", y); continue
    UsdShade.MaterialBindingAPI(p).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
    c = PhysxSchema.PhysxCollisionAPI.Apply(p)          # mm olcekli parcalarda varsayilan ofset buyuk kalir
    c.CreateContactOffsetAttr(0.002); c.CreateRestOffsetAttr(0.0)
    n += 1
print("surtunme baglanan parca: %d/%d" % (n, len(hedefler)))

DT = 1.0 / 480.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=1.0 / 60.0)
world.reset()
EK = st.GetPrimAtPath(MY + "/EKLEM_X")

_t = UsdGeom.Xformable(st.GetPrimAtPath("/World/TEPSI")).GetOrderedXformOps()[0].Get()
BAS_X, Z_T = _t[0], _t[2]


def pos(y):
    return UsdGeom.Xformable(st.GetPrimAtPath(y)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def hiz(v): EK.GetAttribute("drive:linear:physics:targetVelocity").Set(float(v))
def kuvvet(f): EK.GetAttribute("drive:linear:physics:maxForce").Set(float(f))
def adim(k):
    for _ in range(k): world.step(render=False)


def yerlestir(y_alt):
    UsdGeom.Xformable(st.GetPrimAtPath("/World/TEPSI")).GetOrderedXformOps()[0].Set(Gf.Vec3d(BAS_X, y_alt, Z_T))
    UsdGeom.Xformable(st.GetPrimAtPath("/World/PIDE")).GetOrderedXformOps()[0].Set(Gf.Vec3d(BAS_X, y_alt + 0.0125, Z_T))


print("\ntepsi+pide 1,709 kg · mu_d 0,50 · hesapta esik 4,9 m/s2")
for etiket, y_alt in (("A · pim ucunda  (SU ANKI TASARIM)", 0.1055),
                      ("B · tablaya tam oturmus (CUKURLU)", 0.1005)):
    print("\n  --- %s ---" % etiket)
    print("   %-12s %-15s %-14s %-12s %s" % ("hedef ivme", "ulasilan ivme", "temas kotu", "tepsi kaymasi", "sonuc"))
    for a in (1.0, 2.0, 4.0, 6.0, 8.0):
        world.reset(); yerlestir(y_alt); kuvvet(1.0); hiz(0.0); adim(720)
        y_otur = pos("/World/TEPSI")[1] * 1000
        ar0 = pos(MY + "/ARABA")[0]; bag0 = pos("/World/TEPSI")[0] - ar0
        kuvvet((15.0 + 1.709) * a); hiz(0.200)
        onc, a_olc = ar0, 0.0
        for i in range(int(0.30 / DT)):
            world.step(render=False)
            x = pos(MY + "/ARABA")[0]
            if i > 5: a_olc = max(a_olc, ((x - onc) / DT) / ((i + 1) * DT))
            onc = x
        hiz(0.0); adim(480)
        kay = abs((pos("/World/TEPSI")[0] - pos(MY + "/ARABA")[0]) - bag0) * 1000
        print("   %-12s %-15s %-14s %-12s %s" % ("%.1f m/s2" % a, "%.2f m/s2" % a_olc,
                                                 "%.2f mm" % y_otur, "%.2f mm" % kay,
                                                 "TUTUYOR" if kay < 1.0 else "KAYIYOR"))

print("\nBITTI")
app.close()
