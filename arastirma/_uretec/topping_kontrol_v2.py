# -*- coding: utf-8 -*-
"""TOPPING MAKINE KONTROL YAZILIMI — ISAAC SIM SURUMU

C:\\isaacsim\\python.bat topping_kontrol_v1.py

Bu, otonom/hat/makine_kodu.js'in AYNISIDIR — ayni yordamlar, ayni tabla yasasi, ayni sayilar
(hepsi sim_makine.json'dan). Tek fark SURUCU KATI: orada 3B sahnenin eksen degerlerine yaziyordu,
burada USD eklem surucusune yaziyor. Yarin gercek makinede Modbus'a yazacak.

VE BURADA OLCUYORUZ — tarayici simulasyonunun soramadiklari:
  · tepsi tabla uzerinde KAYIYOR MU (3 merkezleme pimi tepsiye cukur acilmasini gerektiriyor,
    su an tepsi duz bir disk — surtunme tutuyor mu?)
  · gercek fizikle cevrim suresi ne
  · araba dozaj boyunca hedefi tutuyor mu
"""
import json, math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, Gf, Sdf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"

with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v2.usd"))
app.update(); app.update()
stage = omni.usd.get_context().get_stage()

# ---- celik-celik surtunmesi: tepsi tabla uzerinde kaymasin diye DEFAULT'a birakilmaz
mat = UsdPhysics.MaterialAPI.Apply(stage.DefinePrim("/World/FizikMalzeme_Celik", "Material"))
mat.CreateStaticFrictionAttr(0.60)        # kuru celik-celik [V: literatur 0,5-0,8]
mat.CreateDynamicFrictionAttr(0.50)
mat.CreateRestitutionAttr(0.05)
for yol in ("/World/TEPSI/ag", "/World/PIDE/ag"):
    p = stage.GetPrimAtPath(yol)
    if p.IsValid():
        UsdShadeBind = Usd.ModelAPI  # noqa (yalnizca okunabilirlik)
        rel = p.CreateRelationship("material:binding:physics", False)
        rel.SetTargets(["/World/FizikMalzeme_Celik"])

DT = 1.0 / 240.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=1.0 / 60.0)
world.reset()

MAKINE_YOL = "/World/MAKINE/TOPPING"


def eklem(ad): return stage.GetPrimAtPath(MAKINE_YOL + "/EKLEM_" + ad)


def temiz(s):
    tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"}
    s = "".join(tr.get(c, c) for c in s)
    return "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in s)


def hedef_hiz(ad, tip, v):
    p = eklem(ad)
    if not p.IsValid(): return False
    p.GetAttribute("drive:%s:physics:targetVelocity" % tip).Set(float(v))
    return True


def konum(yol):
    m = UsdGeom.Xformable(stage.GetPrimAtPath(yol)).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
    return m.ExtractTranslation()


BAS_X = T["baslangic_x"]      # mm — eklemin sifiri modelde arabanin cizildigi yer
def araba_x():
    """MAKINE koordinatinda araba x'i (mm). Eklem yerel sifiri BAS_X'e denk geliyor."""
    return BAS_X + konum(MAKINE_YOL + "/ARABA")[0] * 1000.0
def tepsi_p():   return konum("/World/TEPSI")
def tabla_p():   return konum(MAKINE_YOL + "/TABLA")


def adim(n=1):
    for _ in range(n): world.step(render=False)


# ══════════════════════════════════════════════════════════════════════ SURUCU KATI
def eksenGit(hedef_mm, mod="gecis"):
    """makine_kodu.js · eksenGit — P denetimli hiz komutu (gercek surucude de boyle)"""
    hiz = (T["x_doz_hiz"] if mod == "doz" else T["x_gecis_hiz"]) / 1000.0
    t = 0.0
    while t < 30.0:
        e = (hedef_mm - araba_x()) / 1000.0
        if abs(e) < 0.0005: break
        hedef_hiz("X", "linear", max(-hiz, min(hiz, e * 12.0)))
        adim(); t += DT
    hedef_hiz("X", "linear", 0.0); adim(8)
    return t


def rYasa(t):
    if t <= T["t_dis"]: return T["r_dis"]
    if t >= T["doz_sn"] - T["t_ic"]: return T["r_ic"]
    tm = T["doz_sn"] - T["t_dis"] - T["t_ic"]; u = (t - T["t_dis"]) / tm
    return math.sqrt(T["r_dis"] ** 2 + (T["r_ic"] ** 2 - T["r_dis"] ** 2) * u)


def dxHesap(r): return math.sqrt(max(0.0, r * r - T["r_ic"] ** 2))


def dozla(kod, izle=None):
    y = next(v for v in MAK["yuvalar"] if v["kod"] == kod)
    k = temiz(kod)
    doz_m = (y["grup_doz"] + "_" + k)
    kar_m = (y["grup_karis"] + "_" + k)

    x0 = y["x"] - dxHesap(T["r_dis"])
    t_gecis = eksenGit(x0, "gecis")

    hedef_hiz("TABLA", "angular", T["rpm"] * 6.0)
    hedef_hiz(doz_m, "angular", y["helezon_rpm"] * 6.0)
    hedef_hiz(kar_m, "angular", 4.0 * 6.0)

    t = 0.0; hata_max = 0.0
    while t < T["doz_sn"]:
        hx = y["x"] - dxHesap(rYasa(t))
        e = (hx - araba_x()) / 1000.0
        hata_max = max(hata_max, abs(e))
        hedef_hiz("X", "linear", max(-0.05, min(0.05, e * 12.0)))
        adim(); t += DT
        if izle: izle(t)
    hedef_hiz("X", "linear", 0.0)
    hedef_hiz(doz_m, "angular", 0.0); hedef_hiz(kar_m, "angular", 0.0)
    hedef_hiz("TABLA", "angular", 0.0)
    adim(24)
    return t_gecis, hata_max


# ══════════════════════════════════════════════════════════════════════ OLCUM
print("\n" + "=" * 74)
print("TOPPING DIJITAL IKIZ — GERCEK FIZIKLE CEVRIM")
print("=" * 74)

# tepsinin tablaya gore baslangic bagi
tp0 = tepsi_p(); tb0 = tabla_p()
bag0 = (tp0[0] - tb0[0], tp0[2] - tb0[2])
print("baslangic: araba x = %.1f mm (makine koordinati) · tepsi bagil (%.1f, %.1f, %.1f) mm" % (araba_x(), tp0[0]*1000, tp0[1]*1000, tp0[2]*1000))

adim(240)
tp = tepsi_p()
print("1 s bekleme sonrasi tepsi y = %.1f mm (dusme %.2f mm)" % (tp[1]*1000, (tp0[1]-tp[1])*1000))

import time
recete = [("KAŞAR_KABI", "Kaşar"), ("KÜP_SUCUK", "Küp sucuk")]   # sucuklu pide: kasar ONCE
toplam = 0.0
kayma_max = 0.0


def kayma_olc(_t=None):
    global kayma_max
    tp_, tb_ = tepsi_p(), tabla_p()
    d = math.hypot((tp_[0]-tb_[0]) - bag0[0], (tp_[2]-tb_[2]) - bag0[1])
    kayma_max = max(kayma_max, d)


for kod, ad in recete:
    t0 = 0.0
    tg, hata = dozla(kod, izle=kayma_olc)
    sure = tg + T["doz_sn"]
    toplam += sure
    print("  %-12s gecis %.2f s + doz %.1f s = %.2f s · araba izleme hatasi en cok %.2f mm"
          % (ad, tg, T["doz_sn"], sure, hata*1000))

t_don = eksenGit(T["istasyon_x"], "gecis")
toplam += t_don
print("  istasyona donus %.2f s" % t_don)
print("\nCEVRIM (sucuklu pide, 2 doz): %.1f s -> saatte %.0f tepsi" % (toplam, 3600.0/toplam))

tp1, tb1 = tepsi_p(), tabla_p()
kayma = math.hypot((tp1[0]-tb1[0]) - bag0[0], (tp1[2]-tb1[2]) - bag0[1])
print("\nTEPSI TABLA UZERINDE KAYDI MI?")
print("   cevrim sonu kayma : %.2f mm" % (kayma*1000))
print("   cevrim boyu en cok: %.2f mm" % (kayma_max*1000))
print("   -> %s" % ("KABUL EDILIR (< 3 mm)" if kayma_max*1000 < 3 else "KAYIYOR — MERKEZLEME PIMI SART"))

print("\nBITTI")
app.close()
