# -*- coding: utf-8 -*-
"""DIJITAL IKIZI GORUNTUYE CEVIR — Kemal baska bir PC'den internetten gorebilsin diye

C:\\isaacsim\\python.bat topping_ikiz_render_v1.py

Isaac Sim'i Kemal'in PC'sinde calistirip cevrimi RTX ile render eder, kareleri PNG yazar.
Kareler siteye konur; boylece hangi bilgisayardan bakarsa baksin calisan ikizi gorur.
"""
import json, math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True, "width": 1280, "height": 720, "renderer": "RayTracedLighting"})

import omni.usd, omni.replicator.core as rep
from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
CIK = os.path.join(KOK, "otonom", "hat", "img", "ikiz")
os.makedirs(CIK, exist_ok=True)

with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

# ---- isik (sahnede yok; RTX icin sart)
UsdLux.DomeLight.Define(st, "/World/Isik_Kubbe").CreateIntensityAttr(900.0)
d = UsdLux.DistantLight.Define(st, "/World/Isik_Gunes")
d.CreateIntensityAttr(2500.0); d.CreateAngleAttr(1.0)
UsdGeom.Xformable(d.GetPrim()).AddRotateXYZOp().Set(Gf.Vec3f(-40.0, 35.0, 0.0))

DT = 1.0 / 120.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=DT)
world.reset()
MY = "/World/MAKINE/TOPPING"


def pos(y):
    return UsdGeom.Xformable(st.GetPrimAtPath(y)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def hiz(ad, tip, v):
    p = st.GetPrimAtPath(MY + "/EKLEM_" + ad)
    if p.IsValid(): p.GetAttribute("drive:%s:physics:targetVelocity" % tip).Set(float(v))


BAS_X = T["baslangic_x"]
def araba_x(): return BAS_X + pos(MY + "/ARABA")[0] * 1000.0


# ---- kamera: makineye 3/4 acidan bakiyor, arabayi takip ediyor
# KAMERA: calisma bolgesine bakar. Modul on yuzu z=0, tabla ekseni z=-170 mm, tepsi y=105 mm,
# kaset agizlari y=160 mm. Onden, hafif yukaridan, 3/4 aci.
kam = rep.create.camera(position=(1.35, 0.42, 0.78), look_at=(0.90, 0.16, -0.17), focal_length=28.0)
urun = rep.create.render_product(kam, (1280, 720))
yazici = rep.WriterRegistry.get("BasicWriter")
yazici.initialize(output_dir=CIK, rgb=True)
yazici.attach([urun])


def kare(n=1):
    for _ in range(n):
        world.step(render=True)


def kamera_takip():
    x = araba_x() / 1000.0
    with kam:
        rep.modify.pose(position=(x + 0.45, 0.42, 0.78), look_at=(x, 0.16, -0.17))


def eksenGit(hedef_mm, hizlim):
    t = 0.0
    while t < 20.0:
        e = (hedef_mm - araba_x()) / 1000.0
        if abs(e) < 0.001: break
        hiz("X", "linear", max(-hizlim, min(hizlim, e * 12.0)))
        global SAYAC
        SAYAC += 1
        if SAYAC % 4 == 0:
            kamera_takip(); rep.orchestrator.step(rt_subframes=1, pause_timeline=False)
        world.step(render=(SAYAC % 4 == 0)); t += DT
    hiz("X", "linear", 0.0)


def temiz(s):
    tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"}
    s = "".join(tr.get(c, c) for c in s)
    return "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in s)


def rYasa(t):
    if t <= T["t_dis"]: return T["r_dis"]
    if t >= T["doz_sn"] - T["t_ic"]: return T["r_ic"]
    tm = T["doz_sn"] - T["t_dis"] - T["t_ic"]; u = (t - T["t_dis"]) / tm
    return math.sqrt(T["r_dis"] ** 2 + (T["r_ic"] ** 2 - T["r_dis"] ** 2) * u)


def dxHesap(r): return math.sqrt(max(0.0, r * r - T["r_ic"] ** 2))


SAYAC = 0
print("render basliyor ->", CIK)
kare(5)

for kod in ("KAŞAR_KABI", "KÜP_SUCUK"):
    y = next(v for v in MAK["yuvalar"] if v["kod"] == kod)
    k = temiz(kod)
    eksenGit(y["x"] - dxHesap(T["r_dis"]), 0.200)
    hiz("TABLA", "angular", T["rpm"] * 6.0)
    hiz(y["grup_doz"] + "_" + k, "angular", y["helezon_rpm"] * 6.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 24.0)
    t = 0.0
    while t < T["doz_sn"]:
        e = (y["x"] - dxHesap(rYasa(t)) - araba_x()) / 1000.0
        hiz("X", "linear", max(-0.05, min(0.05, e * 12.0)))
        SAYAC += 1
        if SAYAC % 4 == 0:
            kamera_takip(); rep.orchestrator.step(rt_subframes=1, pause_timeline=False)
        world.step(render=(SAYAC % 4 == 0)); t += DT
    hiz("X", "linear", 0.0)
    hiz("TABLA", "angular", 0.0)
    hiz(y["grup_doz"] + "_" + k, "angular", 0.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 0.0)
    print("  %s dozu render edildi" % kod)

eksenGit(T["istasyon_x"], 0.200)
rep.orchestrator.wait_until_complete()

n = len([f for f in os.listdir(CIK) if f.endswith(".png")])
print("BITTI · %d kare -> %s" % (n, CIK))
app.close()
