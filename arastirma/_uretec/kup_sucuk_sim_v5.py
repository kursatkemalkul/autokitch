# -*- coding: utf-8 -*-
"""KÜP SUCUK DOZAJ SIMULASYONU v5 — DILIMLENMIS HELEZONLU IKIZDE

v1-v4 yolculugu:
  v1/v2: 0 g — helezonun konveks carpisma govdesi vidayi MASIF SILINDIRE ceviriyordu
         (olculdu: vida boyunca 10 isin, hepsi kanada carpti, hicbir yerde bosluk yok)
  v3:    yuksek coznurluklu konveks + SDF denendi; SDF bu kurulumda cookleyemiyor
         ("PhysXGpu dll is incompatible with this version of PhysX")
  v4:    kanat Z'de 2,5 mm dilimlere bolundu -> kanat arasi ACILDI (6 carpma / 18 bosluk)
         ama BAGIMSIZ sahnede eklem hic donmedi (kupsuz, carpismasiz, CPU — hicbiri cozmedi)
  v5:    dilimli helezon, eklemleri ZATEN CALISAN TOPPING IKIZININ icine kondu.
         Dogrulandi: kaset milleri 42/4/26/14 dev/dk, araba 197 mm/s, tabla 35 dev/dk.

KUPLER RIJIT CISIM — parcacik degil. 8 mm kupte en dogru cozum bu (bkz. baslik).

C:\\isaacsim\\python.bat kup_sucuk_sim_v1.py

HANGI COZUM VE NEDEN
  Isaac Sim'de granul icin uc yol var:
    1) PBD parcacik sistemi — hizli ama YAKLASIK. NVIDIA'nin kendi gelistiricisi forumda
       "1 cm parcacik normal yercekiminde oldukca zor / cozucu bu senaryo icin yeterince
       dogru degil" diyor. Bizim kup 8 mm — tam o bandin icinde. KULLANMIYORUZ.
    2) Newton (XPBD/MuJoCo) — ayni parcacik sinifi, ayni kusur.
    3) RIJIT CISIM — her kup GERCEK bir kutu: gercek bicim, gercek surtunme, gercek temas.
  70 g doz / (8 mm kup x 1,05 g/cm3 = 0,538 g) = ~130 kup. 130-400 rijit cisim PhysX icin
  hicbir sey. YANI BU BOYUTTA EN DOGRU COZUM AYNI ZAMANDA EN UCUZU. Yaklasim yok.

NE OLCUYORUZ
  · helezon turu basina kac gram cikiyor  (tasarim hesabi: 68 g/tur)
  · KOPRULEME oluyor mu (akis duruyor mu)
  · kupler pidenin neresine dusuyor, ne kadari tepsi disina kaciyor
"""
import json, math, os, random

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
import numpy as np
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Sdf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"

with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]
Y = next(v for v in MAK["yuvalar"] if v["kod"] == "KÜP_SUCUK")

# ---- URUN: gercek kup sucuk
KUP = 0.008                      # 8 mm kup — urunun kendisi (kopruleme kurali D>=3d bundan cikti)
YOG = 1050.0                     # kg/m3 [V] sucuk
KG_KUP = KUP ** 3 * YOG          # 0,538 g
N_KUP = 400                      # haznede stok (doz 70 g = ~130 kup)
print("kup %.0f mm · %.3f g/kup · doz %.0f g = %.0f kup" % (KUP*1000, KG_KUP*1000, Y["doz_g"], Y["doz_g"]/1000/KG_KUP))

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v4.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

# ---- kup malzemesi: sucuk-celik ve sucuk-sucuk surtunmesi
mp = UsdShade.Material.Define(st, "/World/Malzeme_Sucuk")
m = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
m.CreateStaticFrictionAttr(0.55)      # yagli et urunu - paslanmaz [V]
m.CreateDynamicFrictionAttr(0.45)
m.CreateRestitutionAttr(0.05)

g_urun = UsdPhysics.CollisionGroup.Get(st, "/World/CarpismaGrubu_URUN")
inc = g_urun.GetCollidersCollectionAPI().CreateIncludesRel()

# ---- HAZNE: kasetin govdesi x 1402..1542 · helezon ustu y 354 · z -514..-205
HX0, HX1 = 1.412, 1.532
HY0 = 0.360
HZ0, HZ1 = -0.500, -0.220

kok = UsdGeom.Xform.Define(st, "/World/KUPLER")
random.seed(7)
adim_ = KUP * 1.35
nx = int((HX1 - HX0) / adim_); nz = int((HZ1 - HZ0) / adim_)
kat = int(math.ceil(N_KUP / float(nx * nz)))
say = 0
for k in range(kat):
    for i in range(nx):
        for j in range(nz):
            if say >= N_KUP: break
            p = "/World/KUPLER/kup_%03d" % say
            xf = UsdGeom.Xform.Define(st, p)
            xf.AddTranslateOp().Set(Gf.Vec3d(HX0 + (i + 0.5) * adim_ + random.uniform(-0.0008, 0.0008),
                                             HY0 + k * adim_,
                                             HZ0 + (j + 0.5) * adim_ + random.uniform(-0.0008, 0.0008)))
            xf.AddRotateXYZOp().Set(Gf.Vec3f(random.uniform(0, 90), random.uniform(0, 90), random.uniform(0, 90)))
            c = UsdGeom.Cube.Define(st, p + "/ag")
            c.CreateSizeAttr(KUP)
            c.CreateDisplayColorAttr([Gf.Vec3f(0.55, 0.16, 0.14)])
            UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
            UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(KG_KUP))
            UsdPhysics.CollisionAPI.Apply(c.GetPrim())
            UsdShade.MaterialBindingAPI(c.GetPrim()).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
            cc = PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
            cc.CreateContactOffsetAttr(0.0015); cc.CreateRestOffsetAttr(0.0)
            inc.AddTarget(c.GetPath())
            say += 1
print("hazneye %d kup konuldu (%.1f g)" % (say, say * KG_KUP * 1000))

DT = 1.0 / 480.0                       # 8 mm kup icin ince adim sart
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=1.0 / 60.0)
sc = UsdPhysics.Scene.Get(st, "/World/MAKINE/physicsScene")
if sc: PhysxSchema.PhysxSceneAPI.Apply(sc.GetPrim()).CreateTimeStepsPerSecondAttr(480)
world.reset()

MY = "/World/MAKINE/TOPPING"
BAS_X = T["baslangic_x"]


def pos(y):
    return UsdGeom.Xformable(st.GetPrimAtPath(y)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def araba_x(): return BAS_X + pos(MY + "/ARABA")[0] * 1000.0
def hiz(ad, tip, v):
    p = st.GetPrimAtPath(MY + "/EKLEM_" + ad)
    if p.IsValid(): p.GetAttribute("drive:%s:physics:targetVelocity" % tip).Set(float(v))


def adim(n):
    for _ in range(n): world.step(render=False)


KUPLER = ["/World/KUPLER/kup_%03d" % i for i in range(say)]


def durum():
    """haznede / borudan gecmis / pide uzerinde / kayip"""
    hazne = cikmis = pidede = 0
    pp = pos("/World/PIDE")
    for k in KUPLER:
        t = pos(k)
        if t[1] > 0.250: hazne += 1
        else:
            cikmis += 1
            if abs(t[0] - pp[0]) < 0.145 and abs(t[2] - pp[2]) < 0.145 and t[1] > 0.090: pidede += 1
    return hazne, cikmis, pidede


print("\n=== 1 · KUPLER HAZNEYE YERLESIYOR (2 s) ===")
adim(960)
h, c, p_ = durum()
print("   haznede %d · cikmis %d" % (h, c))

print("\n=== 2 · ARABA KÜP SUCUK YUVASINA GIDIYOR ===")
hedef = Y["x"] - math.sqrt(max(0.0, T["r_dis"]**2 - T["r_ic"]**2))
t = 0.0
while t < 25.0 and abs(hedef - araba_x()) > 0.5:
    e = (hedef - araba_x()) / 1000.0
    hiz("X", "linear", max(-0.2, min(0.2, e * 12.0)))
    adim(1); t += DT
hiz("X", "linear", 0.0); adim(240)
print("   araba x = %.1f mm (hedef %.1f)" % (araba_x(), hedef))

print("\n=== 3 · DOZAJ: helezon %.0f dev/dk · tabla %.0f dev/dk ===" % (Y["helezon_rpm"], T["rpm"]))
hiz("TABLA", "angular", T["rpm"] * 6.0)
hiz("HELEZON_KUP_SUCUK", "angular", Y["helezon_rpm"] * 6.0)
hiz("KARISTIRICI_KUP_SUCUK", "angular", 24.0)

tur_sn = 60.0 / Y["helezon_rpm"]
print("   %-8s %-10s %-10s %-10s %-12s %s" % ("sure", "tur", "cikan", "gram", "g/tur", "pidede"))
t = 0.0
onceki_cikan = 0
while t < 6.0 * tur_sn:
    e = (Y["x"] - araba_x()) / 1000.0
    hiz("X", "linear", max(-0.05, min(0.05, e * 6.0)))
    adim(1); t += DT
    if abs(t % tur_sn) < DT and t > tur_sn * 0.5:
        h, c, pd = durum()
        tur = t / tur_sn
        print("   %-8s %-10s %-10s %-10s %-12s %s" % ("%.1f s" % t, "%.1f" % tur, c, "%.1f" % (c*KG_KUP*1000),
                                                      "%.1f" % (c*KG_KUP*1000/max(tur, 0.01)), pd))
        onceki_cikan = c

hiz("X", "linear", 0.0); hiz("TABLA", "angular", 0.0)
hiz("HELEZON_KUP_SUCUK", "angular", 0.0); hiz("KARISTIRICI_KUP_SUCUK", "angular", 0.0)
adim(480)

h, c, pd = durum()
print("\n=== SONUC ===")
print("   haznede kalan     : %d kup (%.1f g)" % (h, h*KG_KUP*1000))
print("   kasetten cikan    : %d kup (%.1f g)" % (c, c*KG_KUP*1000))
print("   pide uzerinde     : %d kup (%.1f g)" % (pd, pd*KG_KUP*1000))
print("   hedef doz         : %.0f g" % Y["doz_g"])
print("   olculen debi      : %.1f g/tur  (tasarim hesabi 68 g/tur)" % (c*KG_KUP*1000 / 6.0))
print("   KOPRULEME         : %s" % ("YOK — akis surdu" if c > 5 else "VAR — akis durdu ya da hic baslamadi"))
print("\nBITTI")
app.close()
