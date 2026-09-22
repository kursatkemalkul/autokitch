# -*- coding: utf-8 -*-
"""DIJITAL IKIZI EKRANDA AC VE CALISTIR

C:\\isaacsim\\python.bat ikiz_ac.py

Isaac Sim'i PENCEREYLE acar, TOPPING ikizini yukler ve uretim cevrimini SUREKLI dondurur.
Kemal ekrandan izler: fareyle cevirir, yakinlasir, istedigi parcaya bakar.
  sol tus suruk  : dondur      ·  orta tus : kaydir     ·  tekerlek : yakinlas
Kapatmak icin pencereyi kapat ya da Ctrl+C.
"""
import json, math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": False, "width": 1600, "height": 900})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v7.usd"))
for _ in range(20): app.update()
st = omni.usd.get_context().get_stage()

# sahnede isik yok — RTX icin ekle
if not st.GetPrimAtPath("/World/Isik_Kubbe").IsValid():
    UsdLux.DomeLight.Define(st, "/World/Isik_Kubbe").CreateIntensityAttr(1200.0)
    d = UsdLux.DistantLight.Define(st, "/World/Isik_Gunes")
    d.CreateIntensityAttr(3000.0)
    UsdGeom.Xformable(d.GetPrim()).AddRotateXYZOp().Set(Gf.Vec3f(-45.0, 35.0, 0.0))

DT = 1.0 / 120.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=DT)
world.reset()

MY = "/World/MAKINE/TOPPING"
BAS_X = T["baslangic_x"]


def pos(p):
    return UsdGeom.Xformable(st.GetPrimAtPath(p)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def araba_x(): return BAS_X + pos(MY + "/ARABA")[0] * 1000.0


def hiz(ad, tip, v):
    p = st.GetPrimAtPath(MY + "/EKLEM_" + ad)
    if p.IsValid(): p.GetAttribute("drive:%s:physics:targetVelocity" % tip).Set(float(v))


def adim(n=1):
    for _ in range(n): world.step(render=True)


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


def eksenGit(hedef_mm, hizlim=0.200):
    t = 0.0
    while t < 30.0 and app.is_running():
        e = (hedef_mm - araba_x()) / 1000.0
        if abs(e) < 0.001: break
        hiz("X", "linear", max(-hizlim, min(hizlim, e * 12.0)))
        adim(); t += DT
    hiz("X", "linear", 0.0)


def dozla(kod):
    y = next(v for v in MAK["yuvalar"] if v["kod"] == kod)
    k = temiz(kod)
    print("   ▶ %s — %.0f g" % (y["urun"], y["doz_g"]))
    eksenGit(y["x"] - dxHesap(T["r_dis"]))
    hiz("TABLA", "angular", T["rpm"] * 6.0)
    hiz(y["grup_doz"] + "_" + k, "angular", y["helezon_rpm"] * 6.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 24.0)
    t = 0.0
    while t < T["doz_sn"] and app.is_running():
        e = (y["x"] - dxHesap(rYasa(t)) - araba_x()) / 1000.0
        hiz("X", "linear", max(-0.05, min(0.05, e * 12.0)))
        adim(); t += DT
    hiz("X", "linear", 0.0); hiz("TABLA", "angular", 0.0)
    hiz(y["grup_doz"] + "_" + k, "angular", 0.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 0.0)


RECETE = [("Kaşarlı pide", ["KAŞAR_KABI"]),
          ("Sucuklu pide", ["KAŞAR_KABI", "KÜP_SUCUK"]),
          ("Kıymalı pide", ["KIYMA"]),
          ("Kuşbaşılı pide", ["KUŞBAŞI"]),
          ("Lahmacun", ["HARÇ_1"]),
          ("Pizza", ["HARÇ_2", "KAŞAR_KABI", "KÜP_SUCUK"])]

print("\n" + "=" * 70)
print("TOPPING DIJITAL IKIZI — EKRANDA CALISIYOR")
print("  sol tus suruk: dondur · orta tus: kaydir · tekerlek: yakinlas")
print("  kapatmak icin pencereyi kapat")
print("=" * 70)
adim(120)

i = 0
while app.is_running():
    ad, adimlar = RECETE[i % len(RECETE)]
    print("\n═ %s" % ad)
    eksenGit(T["istasyon_x"])
    for kod in adimlar:
        if not app.is_running(): break
        dozla(kod)
    eksenGit(T["istasyon_x"])
    print("  ✔ %s bitti — fırına" % ad)
    i += 1

app.close()
