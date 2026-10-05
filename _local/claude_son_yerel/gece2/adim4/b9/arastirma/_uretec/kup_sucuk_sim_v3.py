# -*- coding: utf-8 -*-
"""KÜP SUCUK DOZAJ SIMULASYONU v3 — carpisma gövdeleri DÜZELTİLMİŞ

C:\\isaacsim\\python.bat kup_sucuk_sim_v3.py

v1/v2'DE 0 g CIKTI — SEBEBI OLCULDU (kup_teshis_v2.py, asagi isin):
  Haznenin icinde y=0,500'den asagi atilan isinlarin neredeyse hepsi y~0,43'te
  KARISTIRICI_KUP_SUCUK'e carpiyordu. Yani karistirici "orumcegi"nin KONVEKS
  ayristirmasi, halkali/cubuklu bicimi DOLU BIR PLAKAYA cevirmis ve hazneyi
  kapak gibi kapatmis. Kupler helezona hic ulasamiyor.
  BU BIR TASARIM BULGUSU DEGIL, SIMULASYON KURULUM HATASI.

DÜZELTME — konkav parcalar icin dogru carpisma:
  1) SDF (isaretli uzaklik alani): donen konkav rijit cisim icin PhysX 5'in dogru araci.
  2) Yuksek coznurluklu konveks ayristirma (voxelResolution + maxConvexHulls + shrinkWrap)
     — SDF cookleme GPU istiyor; bu kurulumda "PhysXGpu dll is incompatible" uyarisi
     cikiyor, o yuzden yedek olarak bu da kuruluyor.
Once ISINLA DOGRULUYORUZ: hazneden asagi atilan isin helezona/tabana ulasiyor mu?
Ulasmiyorsa dozaji hic calistirmiyoruz — yanlis sayi uretmektense hic uretmeyiz.
"""
import json, math, os, random, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf
from isaacsim.core.api import World
from omni.physx import get_physx_scene_query_interface

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
MY = "/World/MAKINE/TOPPING"

with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]
Y = next(v for v in MAK["yuvalar"] if v["kod"] == "KÜP_SUCUK")

KUP, YOG = 0.008, 1050.0
KG_KUP = KUP ** 3 * YOG
N_KUP = 400

omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v3.usd"))
app.update(); app.update()
st = omni.usd.get_context().get_stage()

# ══════════ 1 · KASET ICI DONEN PARCALARIN CARPISMASI
SDF = "--sdf" in sys.argv
n = 0
for g in ("HELEZON_KUP_SUCUK", "KARISTIRICI_KUP_SUCUK"):
    gp = st.GetPrimAtPath(MY + "/" + g)
    if not gp.IsValid(): continue
    for c in gp.GetChildren():
        mc = UsdPhysics.MeshCollisionAPI(c)
        if not mc: continue
        if SDF:
            mc.CreateApproximationAttr("sdf")
            s_ = PhysxSchema.PhysxSDFMeshCollisionAPI.Apply(c.GetPrim())
            s_.CreateSdfResolutionAttr(256)
        else:
            mc.CreateApproximationAttr("convexDecomposition")
            d_ = PhysxSchema.PhysxConvexDecompositionCollisionAPI.Apply(c.GetPrim())
            d_.CreateVoxelResolutionAttr(2000000)     # varsayilan cok kaba: halkayi dolduruyor
            d_.CreateMaxConvexHullsAttr(64)
            d_.CreateErrorPercentageAttr(0.5)
            d_.CreateShrinkWrapAttr(True)
        n += 1
print("carpisma gövdesi yeniden kuruldu: %d parca (%s)" % (n, "SDF" if SDF else "yuksek coznurluklu konveks"))

world = World(stage_units_in_meters=1.0, physics_dt=1 / 480.0, rendering_dt=1 / 60.0)
world.reset()
for _ in range(120): world.step(render=False)

# ══════════ 2 · ISINLA DOGRULAMA — hazne gercekten acik mi?
q = get_physx_scene_query_interface()
acik = tikali = 0
print("\n=== ISIN DENETIMI: hazneden asagi 25 isin ===")
for x in (1.430, 1.450, 1.472, 1.495, 1.515):
    for z in (-0.480, -0.420, -0.360, -0.300, -0.240):
        h = q.raycast_closest([x, 0.500, z], [0.0, -1.0, 0.0], 0.6)
        if h and h.get("hit"):
            yv = h["position"][1]; rb = str(h["rigidBody"])
            if "KARISTIRICI" in rb and yv > 0.39: tikali += 1
            else: acik += 1
        else: acik += 1
print("   helezona/tabana ulasan: %d · karistiriciya takilan: %d" % (acik, tikali))
if tikali > acik:
    print("\n   HAZNE HALA KAPALI — dozaji CALISTIRMIYORUZ.")
    print("   Yanlis bir debi sayisi uretmektense hic uretmemek dogrusu.")
    print("   Sonraki adim: SDF ile dene (--sdf) ya da karistiriciyi cubuk cubuk modelle.")
    print("\nBITTI"); app.close(); sys.exit(0)

# ══════════ 3 · KUPLER
mp = UsdShade.Material.Define(st, "/World/Malzeme_Sucuk")
m = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
m.CreateStaticFrictionAttr(0.55); m.CreateDynamicFrictionAttr(0.45); m.CreateRestitutionAttr(0.05)
inc = UsdPhysics.CollisionGroup.Get(st, "/World/CarpismaGrubu_URUN").GetCollidersCollectionAPI().CreateIncludesRel()

random.seed(7)
a_ = KUP * 1.35
HX0, HX1, HY0, HZ0, HZ1 = 1.415, 1.529, 0.365, -0.500, -0.225
nx = int((HX1 - HX0) / a_); nz = int((HZ1 - HZ0) / a_)
yollar = []
for k in range(int(math.ceil(N_KUP / float(nx * nz)))):
    for i in range(nx):
        for j in range(nz):
            if len(yollar) >= N_KUP: break
            p = "/World/KUPLER/kup_%03d" % len(yollar)
            xf = UsdGeom.Xform.Define(st, p)
            xf.AddTranslateOp().Set(Gf.Vec3d(HX0 + (i + .5) * a_ + random.uniform(-8e-4, 8e-4),
                                             HY0 + k * a_,
                                             HZ0 + (j + .5) * a_ + random.uniform(-8e-4, 8e-4)))
            xf.AddRotateXYZOp().Set(Gf.Vec3f(random.uniform(0, 90), random.uniform(0, 90), random.uniform(0, 90)))
            c = UsdGeom.Cube.Define(st, p + "/ag"); c.CreateSizeAttr(KUP)
            c.CreateDisplayColorAttr([Gf.Vec3f(0.55, 0.16, 0.14)])
            UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
            UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(KG_KUP))
            UsdPhysics.CollisionAPI.Apply(c.GetPrim())
            UsdShade.MaterialBindingAPI(c.GetPrim()).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
            cc = PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
            cc.CreateContactOffsetAttr(0.0015); cc.CreateRestOffsetAttr(0.0)
            inc.AddTarget(c.GetPath())
            yollar.append(p)
print("\nhazneye %d kup (%.1f g) · doz hedefi %.0f g" % (len(yollar), len(yollar)*KG_KUP*1000, Y["doz_g"]))
world.reset()


def pos(y):
    return UsdGeom.Xformable(st.GetPrimAtPath(y)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def hiz(ad, tip, v):
    p = st.GetPrimAtPath(MY + "/EKLEM_" + ad)
    if p.IsValid(): p.GetAttribute("drive:%s:physics:targetVelocity" % tip).Set(float(v))


def adim(k):
    for _ in range(k): world.step(render=False)


def sayim():
    cik = pd = 0
    pp = pos("/World/PIDE")
    for p in yollar:
        t = pos(p)
        if t[1] < 0.250:
            cik += 1
            if abs(t[0]-pp[0]) < 0.145 and abs(t[2]-pp[2]) < 0.145 and t[1] > 0.090: pd += 1
    return cik, pd


adim(960)
c0, _ = sayim()
print("yerlesme sonrasi cikan: %d" % c0)

BAS_X = T["baslangic_x"]
hedef = Y["x"]
t = 0.0
while t < 25.0 and abs(hedef - (BAS_X + pos(MY + "/ARABA")[0]*1000)) > 0.6:
    e = (hedef - (BAS_X + pos(MY + "/ARABA")[0]*1000)) / 1000.0
    hiz("X", "linear", max(-0.2, min(0.2, e*12))); adim(1); t += 1/480.0
hiz("X", "linear", 0.0); adim(240)

print("\n=== DOZAJ: helezon %.0f dev/dk ===" % Y["helezon_rpm"])
hiz("TABLA", "angular", T["rpm"]*6.0)
hiz("HELEZON_KUP_SUCUK", "angular", Y["helezon_rpm"]*6.0)
hiz("KARISTIRICI_KUP_SUCUK", "angular", 24.0)
tur_sn = 60.0 / Y["helezon_rpm"]
print("   %-8s %-7s %-8s %-9s %-10s %s" % ("sure", "tur", "cikan", "gram", "g/tur", "pidede"))
for tur in range(1, 7):
    adim(int(tur_sn * 480))
    c, pd = sayim()
    print("   %-8s %-7s %-8s %-9s %-10s %s" % ("%.1f s" % (tur*tur_sn), tur, c-c0, "%.1f" % ((c-c0)*KG_KUP*1000),
                                               "%.1f" % ((c-c0)*KG_KUP*1000/tur), pd))
hiz("TABLA", "angular", 0.0); hiz("HELEZON_KUP_SUCUK", "angular", 0.0); hiz("KARISTIRICI_KUP_SUCUK", "angular", 0.0)
adim(480)
c, pd = sayim()
print("\n=== SONUC ===")
print("   cikan %d kup = %.1f g · pidede %d kup = %.1f g" % (c-c0, (c-c0)*KG_KUP*1000, pd, pd*KG_KUP*1000))
print("   olculen debi : %.1f g/tur   (tasarim hesabi 68 g/tur)" % ((c-c0)*KG_KUP*1000/6.0))
print("\nBITTI")
app.close()
