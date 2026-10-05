# -*- coding: utf-8 -*-
"""TEPSI KAYMA DENEYI — araba hizlanirken tepsi tabla uzerinde kayiyor mu?

C:\\isaacsim\\python.bat tepsi_kayma_deney_v1.py

SU ANKI TASARIM: 3 merkezleme pimi tablanin ustunde y 100..105, uclari Ø10 DUZ daire.
Tepsi duz tabanli, yani bu UC DAIRE uzerinde duruyor. Tepsiyi arabanin ivmesine karsi
tutan tek sey SURTUNME.

Elle hesap: tepsi 1,216 + pide 0,493 = 1,709 kg · mu 0,5 -> tutabilecegi kuvvet
0,5 x 1,709 x 9,81 = 8,4 N -> en cok 4,9 m/s2 ivme. Araba gecis hizina 0,033 s'de
ciktigi icin ivme ~6 m/s2. YANI HESAPTA KAYIYOR. Simdi olcerek dogruluyoruz ve
hangi ivmede durdugunu buluyoruz.
"""
import json, math, os

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Sdf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

# ---- FIZIK MALZEMESI: dogru yoldan (UsdShade.Material + MaterialBindingAPI, purpose=physics)
mp = UsdShade.Material.Define(st, "/World/FizikMalzeme_Celik")
mat = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
mat.CreateStaticFrictionAttr(0.60)       # kuru celik-celik [V: literatur 0,5-0,8]
mat.CreateDynamicFrictionAttr(0.50)
mat.CreateRestitutionAttr(0.02)

hedefler = ["/World/TEPSI/ag", "/World/PIDE/ag",
            "/World/MAKINE/TOPPING/TABLA/merkezleme_pimi_A",
            "/World/MAKINE/TOPPING/TABLA/merkezleme_pimi_B",
            "/World/MAKINE/TOPPING/TABLA/merkezleme_pimi_C",
            "/World/MAKINE/TOPPING/TABLA/tabla"]
n_bag = 0
for y in hedefler:
    p = st.GetPrimAtPath(y)
    if not p.IsValid(): print("  YOK:", y); continue
    UsdShade.MaterialBindingAPI(p).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
    # mm olcekli parcalarda VARSAYILAN temas ofseti cok buyuk kalir
    c = PhysxSchema.PhysxCollisionAPI.Apply(p)
    c.CreateContactOffsetAttr(0.002); c.CreateRestOffsetAttr(0.0)
    n_bag += 1
print("surtunme baglanan parca: %d/%d" % (n_bag, len(hedefler)))

DT = 1.0 / 480.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=1.0 / 60.0)
world.reset()

MY = "/World/MAKINE/TOPPING"
EK = st.GetPrimAtPath(MY + "/EKLEM_X")


def pos(y):
    return UsdGeom.Xformable(st.GetPrimAtPath(y)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def hiz(v): EK.GetAttribute("drive:linear:physics:targetVelocity").Set(float(v))
def kuvvet(f): EK.GetAttribute("drive:linear:physics:maxForce").Set(float(f))
def sonum(d): EK.GetAttribute("drive:linear:physics:damping").Set(float(d))


def adim(n):
    for _ in range(n): world.step(render=False)


print("\n=== A · TEMAS DOGRULAMASI (2 s bekleme) ===")
t0 = pos("/World/TEPSI"); adim(960); t1 = pos("/World/TEPSI")
print("   tepsi y: %.3f -> %.3f mm (oturma %.3f mm)" % (t0[1]*1000, t1[1]*1000, (t0[1]-t1[1])*1000))

print("\n=== B · KAYMA ESIGI: arabayi farkli ivmelerle hizlandir ===")
print("   tepsi+pide 1,709 kg · pim ucu 3 x Ø10 · mu_d 0,50")
print("   %-14s %-16s %-14s %s" % ("hedef ivme", "ulasilan ivme", "tepsi kaymasi", "sonuc"))

for a_hedef in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
    world.reset(); adim(240)
    sonum(1e5); kuvvet(15.0 * 1.0)           # once dursun
    ar0 = pos(MY + "/ARABA")[0]; tp0 = pos("/World/TEPSI")[0]
    bag0 = tp0 - ar0
    # ivmeyi surucu kuvvetiyle veriyoruz: F = (araba 15,0 kg + tepsi 1,7) x a  (tepsi takip ederse)
    kuvvet((15.0 + 1.709) * a_hedef)
    hiz(0.200)
    onc = ar0; vmax = 0.0; a_olc = 0.0
    for i in range(int(0.30 / DT)):
        world.step(render=False)
        x = pos(MY + "/ARABA")[0]
        v = (x - onc) / DT; onc = x
        if i > 5: a_olc = max(a_olc, v / ((i + 1) * DT))
        vmax = max(vmax, v)
    hiz(0.0); adim(240)
    tp1 = pos("/World/TEPSI")[0]; ar1 = pos(MY + "/ARABA")[0]
    kay = abs((tp1 - ar1) - bag0) * 1000
    print("   %-14s %-16s %-14s %s" % ("%.1f m/s2" % a_hedef, "%.2f m/s2" % a_olc,
                                       "%.2f mm" % kay, "TUTUYOR" if kay < 1.0 else "KAYIYOR"))

print("\nBITTI")
app.close()
