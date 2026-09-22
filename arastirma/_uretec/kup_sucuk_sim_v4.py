# -*- coding: utf-8 -*-
"""KÜP SUCUK DOZAJ SIMULASYONU v4 — DILIMLENMIS HELEZONLA

C:\\isaacsim\\python.bat kup_sucuk_sim_v4.py

v1-v3: 0 g. Sebep olculdu — helezonun konveks carpisma govdesi vidayi masif silindire
cevirmisti (vida boyunca 10 isin, hepsi kanada carpti, hicbir yerde bosluk yok).
v4: helezon kanadi Z'de 2,5 mm dilimlere bolundu (168 dilim). Her dilimin konveks kabugu
komsu dilimin boslugunu dolduramaz. Ayni rijit cisme ait, yani vida yine tek parca doner.

ONCE ISINLA DOGRULA, SONRA OLC. Kanat arasi acilmadiysa dozaj hic calistirilmaz.
"""
import json, math, os, random, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import numpy as np
import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Vt
from isaacsim.core.api import World
from omni.physx import get_physx_scene_query_interface

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
Y = next(v for v in MAK["yuvalar"] if v["kod"] == "KÜP_SUCUK")
K = json.load(open(os.path.join(FIZ, "sucuk_kaset_v1.json"), encoding="utf-8"))
Z = np.load(os.path.join(FIZ, "sucuk_kaset_v1.npz"))
HZ = K["hazne"]
XM = K["kaset_x"] / 1000.0

KUP, YOG = 0.008, 1050.0
KG_KUP = KUP ** 3 * YOG
N_KUP = 400

USD_YOL = os.path.join(FIZ, "SUCUK_KASET_SIM_v1.usd")
st = Usd.Stage.CreateNew(USD_YOL)
UsdGeom.SetStageUpAxis(st, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(st, 1.0)
UsdPhysics.SetStageKilogramsPerUnit(st, 1.0)
UsdGeom.Xform.Define(st, "/World")
st.SetDefaultPrim(st.GetPrimAtPath("/World"))
sc = UsdPhysics.Scene.Define(st, "/World/physicsScene")
sc.CreateGravityDirectionAttr(Gf.Vec3f(0, -1, 0)); sc.CreateGravityMagnitudeAttr(9.81)
px = PhysxSchema.PhysxSceneAPI.Apply(sc.GetPrim())
px.CreateTimeStepsPerSecondAttr(480); px.CreateSolverTypeAttr("TGS")

KASET_YOLLARI = []
RENK = {"sac": (.74, .77, .80), "celik": (.66, .69, .73), "pom": (.90, .90, .88),
        "silikon": (.95, .45, .35), "cam": (.70, .85, .95)}


def mesh(yol, i, renk, hareketli):
    m = UsdGeom.Mesh.Define(st, yol)
    V, F = Z["V%d" % i], Z["F%d" % i]
    m.CreatePointsAttr(Vt.Vec3fArray.FromNumpy(V.astype(np.float32)))
    m.CreateFaceVertexIndicesAttr(Vt.IntArray.FromNumpy(F.reshape(-1).astype(np.int32)))
    m.CreateFaceVertexCountsAttr(Vt.IntArray.FromNumpy(np.full(len(F), 3, dtype=np.int32)))
    m.CreateDisplayColorAttr([Gf.Vec3f(*renk)]); m.CreateSubdivisionSchemeAttr("none")
    UsdPhysics.CollisionAPI.Apply(m.GetPrim())
    mc = UsdPhysics.MeshCollisionAPI.Apply(m.GetPrim())
    mc.CreateApproximationAttr("convexHull" if hareketli else "none")
    KASET_YOLLARI.append(str(m.GetPath()))
    return m


gruplar = {}
for i, p in enumerate(K["parca"]):
    gruplar.setdefault(p["grup"], []).append(i)

for g, idx in gruplar.items():
    gp = "/World/" + g
    xf = UsdGeom.Xform.Define(st, gp)
    kutle = sum(K["parca"][i]["kutle_kg"] for i in idx)
    hareketli = g != "SABIT"
    if hareketli:
        UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
        UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(max(kutle, 1e-3)))
    for i in idx:
        p = K["parca"][i]
        mesh(gp + "/" + p["ad"].replace("-", "_"), i, RENK.get(p["mal"], (.6, .6, .6)), hareketli)
    print("  %-14s %3d parca · %.3f kg · %s" % (g, len(idx), kutle, "DONER" if hareketli else "sabit"))

# ---- CARPISMA GRUBU: kasetin kendi parcalari birbirine carpismaz (yatak/kovan isini
# EKLEM tasir). Bunu unutunca vida govdeye kenetleniyor ve HIC DONMUYOR — bu sahnede
# tam oyle oldu, helezon acisi 11,1 derecede cakili kaldi ve 6 tur boyunca hic donmedi.
g_kaset = UsdPhysics.CollisionGroup.Define(st, "/World/Grup_KASET")
g_kaset.CreateFilteredGroupsRel().SetTargets(["/World/Grup_KASET"])
kaset_col = g_kaset.GetCollidersCollectionAPI()
g_urun = UsdPhysics.CollisionGroup.Define(st, "/World/Grup_URUN")   # kupler: her seyle carpisir

# ---- doner eklemler: kaset milleri Z ekseninde
for g, koty in (("HELEZON", 260.0 + 60.0), ("KARISTIRICI", 260.0 + 164.0)):
    if g not in gruplar: continue
    j = UsdPhysics.RevoluteJoint.Define(st, "/World/EKLEM_" + g)
    j.CreateAxisAttr("Z"); j.CreateBody0Rel().SetTargets([])
    j.CreateBody1Rel().SetTargets(["/World/" + g])
    pv = Gf.Vec3f(float(XM), float(koty / 1000.0), 0.0)
    j.CreateLocalPos0Attr(pv); j.CreateLocalPos1Attr(pv)
    d = UsdPhysics.DriveAPI.Apply(j.GetPrim(), "angular")
    d.CreateTypeAttr("force"); d.CreateStiffnessAttr(0.0); d.CreateDampingAttr(1e3)
    d.CreateMaxForceAttr(12.0); d.CreateTargetVelocityAttr(0.0)

# ---- TEPSI + PIDE: agzin altinda, tabla kotunda
AG_Y = 0.160          # dozaj kovaninin alt ucu
def puk(yol, r, kal, y_alt, kg, renk):
    xf = UsdGeom.Xform.Define(st, yol)
    xf.AddTranslateOp().Set(Gf.Vec3d(XM, y_alt, -0.170))
    m = UsdGeom.Mesh.Define(st, yol + "/ag")
    P, F, n = [], [], 48
    for s_ in (0, 1):
        yy = kal if s_ else 0.0
        for i in range(n):
            a = 2 * math.pi * i / n
            P.append(Gf.Vec3f(r * math.cos(a), yy, r * math.sin(a)))
    for i in range(n):
        jj = (i + 1) % n
        F += [[i, jj, n + jj], [i, n + jj, n + i]]
    for i in range(1, n - 1):
        F += [[n, n + i, n + i + 1], [0, i + 1, i]]
    m.CreatePointsAttr(P); m.CreateFaceVertexIndicesAttr([v for f in F for v in f])
    m.CreateFaceVertexCountsAttr([3] * len(F)); m.CreateDisplayColorAttr([Gf.Vec3f(*renk)])
    UsdPhysics.CollisionAPI.Apply(m.GetPrim())
    UsdPhysics.MeshCollisionAPI.Apply(m.GetPrim()).CreateApproximationAttr("convexHull")
    return xf


puk("/World/TEPSI", 0.170, 0.012, 0.100, 1.216, (.72, .75, .78))
puk("/World/PIDE", 0.140, 0.008, 0.112, 0.493, (.91, .84, .68))
# tepsi/pide sabit dursun (robot tutuyor kabul) — rijit cisim yapmiyoruz, statik carpisma yeter

ki = kaset_col.CreateIncludesRel()
for y_ in KASET_YOLLARI: ki.AddTarget(y_)
print("  kaset carpisma grubuna %d parca" % len(KASET_YOLLARI))

st.GetRootLayer().Save()
print("sahne yazildi ->", USD_YOL)
omni.usd.get_context().open_stage(USD_YOL)
app.update(); app.update()
st = omni.usd.get_context().get_stage()
world = World(stage_units_in_meters=1.0, physics_dt=1/480.0, rendering_dt=1/60.0)
world.reset()
for _ in range(120): world.step(render=False)

# ══════════ ISIN DENETIMI: kanat arasi acildi mi?
q = get_physx_scene_query_interface()
# DIKKAT: isini MIL EKSENINDEN atma — orada cekirdek (Ø8) hep var, her zaman "dolu" cikar.
# Kanat bolgesinden at: cekirdek yaricapi 4 mm, kanat disi 34 mm -> r = 25 mm.
print("\n=== ISIN DENETIMI: kanat yaricapinda (r=25 mm) 24 nokta ===")
# DIKKAT 2: "carpti mi" yetmez — NEYE carptigina bak. Kanadi iskalayan isin govdenin
# tabanina (y~0,289) carpar; bu BOSLUK demektir. Ilk testte bunu da "dolu" saymistim.
bos = carp = 0
for i in range(24):
    z = -0.500 + i * 0.0115
    h = q.raycast_closest([XM + 0.025, 0.352, z], [0, -1, 0], 0.075)
    if h and h.get("hit") and "HELEZON" in str(h["rigidBody"]): carp += 1
    else: bos += 1
print("   kanada carpan %d · KANAT ARASI %d  ->  %s" % (carp, bos,
      "ACIK" if bos >= 6 else "HALA MASIF — dozaji calistirmiyoruz"))
if bos < 6:
    print("\nBITTI"); app.close(); sys.exit(0)

# ══════════ KUPLER
mp = UsdShade.Material.Define(st, "/World/Malzeme_Sucuk")
mm = UsdPhysics.MaterialAPI.Apply(mp.GetPrim())
mm.CreateStaticFrictionAttr(0.55); mm.CreateDynamicFrictionAttr(0.45); mm.CreateRestitutionAttr(0.05)
random.seed(7); a_ = KUP * 1.35
HX0, HX1 = HZ["x"][0]/1000+0.013, HZ["x"][1]/1000-0.013
HZ0, HZ1 = HZ["z"][0]/1000+0.020, HZ["z"][1]/1000-0.020
nx = int((HX1-HX0)/a_); nz = int((HZ1-HZ0)/a_)
yollar = []
for k in range(int(math.ceil(N_KUP/float(nx*nz)))):
    for i in range(nx):
        for j in range(nz):
            if len(yollar) >= N_KUP: break
            p = "/World/KUPLER/kup_%03d" % len(yollar)
            xf = UsdGeom.Xform.Define(st, p)
            xf.AddTranslateOp().Set(Gf.Vec3d(HX0+(i+.5)*a_+random.uniform(-8e-4,8e-4), 0.370+k*a_,
                                             HZ0+(j+.5)*a_+random.uniform(-8e-4,8e-4)))
            xf.AddRotateXYZOp().Set(Gf.Vec3f(random.uniform(0,90), random.uniform(0,90), random.uniform(0,90)))
            c = UsdGeom.Cube.Define(st, p+"/ag"); c.CreateSizeAttr(KUP)
            c.CreateDisplayColorAttr([Gf.Vec3f(.55,.16,.14)])
            UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
            UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(KG_KUP))
            UsdPhysics.CollisionAPI.Apply(c.GetPrim())
            UsdShade.MaterialBindingAPI(c.GetPrim()).Bind(mp, UsdShade.Tokens.weakerThanDescendants, "physics")
            cc = PhysxSchema.PhysxCollisionAPI.Apply(c.GetPrim())
            cc.CreateContactOffsetAttr(0.0015); cc.CreateRestOffsetAttr(0.0)
            UsdPhysics.CollisionGroup.Get(st, '/World/Grup_URUN').GetCollidersCollectionAPI().CreateIncludesRel().AddTarget(c.GetPath())
            yollar.append(p)
print("\nhazneye %d kup = %.1f g · doz hedefi %.0f g" % (len(yollar), len(yollar)*KG_KUP*1000, Y["doz_g"]))
world.reset()


def yof(p):
    return UsdGeom.Xformable(st.GetPrimAtPath(p)).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()


def adim(n):
    for _ in range(n): world.step(render=False)


def sayim():
    cik = pd = 0
    for p in yollar:
        t = yof(p)
        if t[1] < 0.250:
            cik += 1
            if math.hypot(t[0]-XM, t[2]+0.170) < 0.140 and t[1] > 0.100: pd += 1
    return cik, pd


adim(960)
c0, _ = sayim()
print("yerlesme sonrasi cikan: %d" % c0)

print("\n=== DOZAJ: helezon %.0f dev/dk ===" % Y["helezon_rpm"])
YON = -1.0 if "--ters" in sys.argv else 1.0
print("   donus yonu: %s" % ("TERS (-)" if YON < 0 else "duz (+)"))
st.GetPrimAtPath("/World/EKLEM_HELEZON").GetAttribute("drive:angular:physics:targetVelocity").Set(YON*Y["helezon_rpm"]*6.0)
st.GetPrimAtPath("/World/EKLEM_KARISTIRICI").GetAttribute("drive:angular:physics:targetVelocity").Set(24.0)
tur_sn = 60.0/Y["helezon_rpm"]
print("   %-8s %-6s %-8s %-9s %-10s %s" % ("sure", "tur", "cikan", "gram", "g/tur", "pidede"))
def hel_aci():
    import math as _m
    q_ = UsdGeom.Xformable(st.GetPrimAtPath("/World/HELEZON")).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractRotationQuat()
    return _m.degrees(2.0 * _m.atan2(q_.GetImaginary()[2], q_.GetReal()))


a_onc = hel_aci()
for tur in range(1, 7):
    adim(int(tur_sn*480))
    a_ = hel_aci()
    print("      [helezon acisi %.1f -> %.1f derece]" % (a_onc, a_)); a_onc = a_
    c, pd = sayim()
    print("   %-8s %-6s %-8s %-9s %-10s %s" % ("%.1f s" % (tur*tur_sn), tur, c-c0,
          "%.1f" % ((c-c0)*KG_KUP*1000), "%.1f" % ((c-c0)*KG_KUP*1000/tur), pd))
c, pd = sayim()
print("\n=== SONUC ===")
print("   cikan %.1f g · pidede %.1f g · olculen debi %.1f g/tur (tasarim 68 g/tur)"
      % ((c-c0)*KG_KUP*1000, pd*KG_KUP*1000, (c-c0)*KG_KUP*1000/6.0))
print("\nBITTI")
app.close()
