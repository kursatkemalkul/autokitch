# -*- coding: utf-8 -*-
r"""DIJITAL IKIZ + KUMANDA PANELI  (v3)

C:\isaacsim\python.bat ikiz_ac_v3.py

v2'den farki: Isaac Sim'in ICINDE omni.ui paneli var — tipki sitedeki gibi urun
secilir. "Kasarli pide" dersin, makine onu yapar. SUREKLI dugmesi acikken
receteleri sirayla dondurur.
  sol tus suruk : dondur  ·  orta tus : kaydir  ·  tekerlek : yakinlas
"""
import json, math, os

from isaacsim import SimulationApp
app = SimulationApp({"headless": False, "width": 1600, "height": 900})

import omni.usd
import omni.ui as ui
from pxr import Usd, UsdGeom, UsdLux, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v8.usd"))
for _ in range(20): app.update()
st = omni.usd.get_context().get_stage()

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

# ------------------------------------------------------------------ makine
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


# ------------------------------------------------------------------ panel
RECETE = [("Kaşarlı pide", ["KAŞAR_KABI"]),
          ("Sucuklu pide", ["KAŞAR_KABI", "KÜP_SUCUK"]),
          ("Kıymalı pide", ["KIYMA"]),
          ("Kuşbaşılı pide", ["KUŞBAŞI"]),
          ("Lahmacun", ["HARÇ_1"]),
          ("Pizza", ["HARÇ_2", "KAŞAR_KABI", "KÜP_SUCUK"])]

D = {"kuyruk": [], "bos": 0, "surekli": False, "dur": False, "durum": "hazır", "sayac": 0}


def sec(ad):
    D["kuyruk"].append(ad)
    D["dur"] = False


def surekli_degis(v):
    D["surekli"] = v
    if v: D["kuyruk"].clear()


def durdur():
    D["dur"] = True
    D["surekli"] = False
    D["kuyruk"].clear()
    if sw_surekli: sw_surekli.model.set_value(False)


pencere = ui.Window("AUTOKITCH · TOPPING", width=330, height=470)
sw_surekli = None
with pencere.frame:
    with ui.VStack(spacing=8, height=0):
        ui.Spacer(height=4)
        ui.Label("ÜRÜN SEÇ", height=22, style={"font_size": 18, "color": 0xFFD0D0D0})
        for _ad, _ in RECETE:
            ui.Button(_ad, height=34, clicked_fn=lambda a=_ad: sec(a))
        ui.Spacer(height=6)
        with ui.HStack(height=26, spacing=8):
            sw_surekli = ui.CheckBox(width=22)
            sw_surekli.model.add_value_changed_fn(lambda m: surekli_degis(m.get_value_as_bool()))
            ui.Label("sürekli üret (hepsini sırayla)")
        ui.Button("DURDUR", height=30, clicked_fn=durdur)
        ui.Spacer(height=8)
        l_durum = ui.Label("hazır", height=22, style={"font_size": 16, "color": 0xFF7FD4A0})
        l_sayac = ui.Label("üretilen: 0", height=20, style={"color": 0xFFA0A0A0})
        l_eksen = ui.Label("", height=20, style={"color": 0xFFA0A0A0})


def yaz(s):
    D["durum"] = s
    l_durum.text = s
    l_sayac.text = "üretilen: %d" % D["sayac"]
    l_eksen.text = "araba X = %.0f mm" % araba_x()


# ------------------------------------------------------------------ hareket
def eksenGit(hedef_mm, hizlim=0.200):
    t = 0.0
    while t < 30.0 and app.is_running() and not D["dur"]:
        e = (hedef_mm - araba_x()) / 1000.0
        if abs(e) < 0.001: break
        hiz("X", "linear", max(-hizlim, min(hizlim, e * 12.0)))
        adim(); t += DT
        if int(t * 120) % 12 == 0: yaz(D["durum"])
    hiz("X", "linear", 0.0)


def dozla(kod):
    y = next(v for v in MAK["yuvalar"] if v["kod"] == kod)
    k = temiz(kod)
    yaz("%s — %.0f g" % (y["urun"], y["doz_g"]))
    eksenGit(y["x"] - dxHesap(T["r_dis"]))
    if D["dur"]: return
    hiz("TABLA", "angular", T["rpm"] * 6.0)
    hiz(y["grup_doz"] + "_" + k, "angular", y["helezon_rpm"] * 6.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 24.0)
    t = 0.0
    while t < T["doz_sn"] and app.is_running() and not D["dur"]:
        e = (y["x"] - dxHesap(rYasa(t)) - araba_x()) / 1000.0
        hiz("X", "linear", max(-0.05, min(0.05, e * 12.0)))
        adim(); t += DT
        if int(t * 120) % 12 == 0: yaz(D["durum"])
    hiz("X", "linear", 0.0); hiz("TABLA", "angular", 0.0)
    hiz(y["grup_doz"] + "_" + k, "angular", 0.0)
    hiz(y["grup_karis"] + "_" + k, "angular", 0.0)


def uret(ad):
    adimlar = next(a for n, a in RECETE if n == ad)
    print("\n═ %s" % ad)
    eksenGit(T["istasyon_x"])
    for kod in adimlar:
        if not app.is_running() or D["dur"]: break
        dozla(kod)
    eksenGit(T["istasyon_x"])
    if not D["dur"]:
        D["sayac"] += 1
        print("  ✔ %s bitti — fırına" % ad)
    yaz("hazır")


print("\n" + "=" * 70)
print("TOPPING DIJITAL IKIZI — soldaki AUTOKITCH panelinden ürün seç")
print("=" * 70)
adim(120)
yaz("hazır")

i = 0
while app.is_running():
    if D["kuyruk"]:
        uret(D["kuyruk"].pop(0))
    elif D["surekli"]:
        uret(RECETE[i % len(RECETE)][0]); i += 1
    else:
        adim(4)
        D["bos"] += 1
        if D["bos"] % 30 == 0: yaz(D["durum"])

app.close()
