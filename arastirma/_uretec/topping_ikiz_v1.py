# -*- coding: utf-8 -*-
"""TOPPING DIJITAL IKIZI — TAM SAHNE (modul + robot + tepsi + pide + urun)

C:\\isaacsim\\python.bat topping_ikiz_v1.py

ICERIK
  · TOPPING_fizik_v3.usd        makinenin kendisi (534 parca, 14 eklem, gercek kutleler)
  · UR10e                       Isaac varlik kutuphanesinden GERCEK robot kolu
                                (1300 mm erisim · 12,5 kg yuk — bizim tepsi+urun ~1,9 kg)
  · TEPSI                       Ø340 · 1,5 mm sac + 12 mm kenar (ONEMLI NOT asagida)
  · PIDE                        Ø280 · 8 mm hamur
  · URUN carpisma grubu         tepsi/pide makineyle NORMAL carpisir; makinenin kendi
                                parcalari birbirine carpismaz (yatak/kizak isini eklem yapar)

TEPSI KUTLESI — GERCEK BIR BULGU: hesapta TEPSI_K = 12 mm yaziyor. 12 mm DOLU paslanmaz
Ø340 tepsi 8,6 kg eder; boyle bir tepsiyi ne robot tasir ne tabla dondurur. Gercek pide
tepsisi 1,5 mm sactan olur, 12 mm o sacin KENAR yuksekligidir. Burada oyle modellendi:
taban 1,5 mm + kenar 12 mm -> ~1,3 kg. Kemal'in onayi gerekiyor.
"""
import json, math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from isaacsim.storage.native import get_assets_root_path
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, Gf, Sdf, Vt
import numpy as np

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
MAKINE = os.path.join(FIZ, "TOPPING_fizik_v3.usd")
CIKTI = os.path.join(FIZ, "TOPPING_IKIZ_v1.usd")

with open(os.path.join(FIZ, "topping_fizik_v1.json"), encoding="utf-8") as f:
    M = json.load(f)
EK = {e["ad"]: e for e in M["eklem"]}
ISTASYON = EK["X"]["istasyon"]          # m — tepsinin birakildigi x (Kemal: en soldan)
BASLANGIC = EK["X"]["baslangic"]        # m — arabanin MODELDE cizildigi x; tabla su an ORADA.
# DIKKAT: tepsi tablanin UZERINE konmali. Istasyon x'ine koyulursa tabla orada olmadigi icin
# tepsi bosluga dusuyor (ilk denemede oyle oldu). Cevrim basinda araba zaten istasyona gidiyor.
PIVOT = EK["TABLA"]["pivot"]            # m — tabla ekseni (modul yereli)

# ---- sahne: makineyi REFERANS olarak al, uzerine ekle
stage = Usd.Stage.CreateNew(CIKTI)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdPhysics.SetStageKilogramsPerUnit(stage, 1.0)
w = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(w.GetPrim())

mk = stage.OverridePrim("/World/MAKINE")
mk.GetReferences().AddReference(MAKINE.replace("\\", "/"), "/World")

# ---- URUN carpisma grubu (makine grubu MAKINE referansinin icinde geldi)
g_urun = UsdPhysics.CollisionGroup.Define(stage, "/World/CarpismaGrubu_URUN")
urun_col = g_urun.GetCollidersCollectionAPI()


def silindir_ag(stage, yol, r, kal, ym, renk, dilim=64):
    """yatay disk agi — merkez (PIVOT[0], ym, PIVOT[2]); kendi yerel eksenine gore"""
    m = UsdGeom.Mesh.Define(stage, yol)
    P, F = [], []
    for s_ in (0, 1):
        y = ym + (kal / 2 if s_ else -kal / 2)
        for i in range(dilim):
            a = 2 * math.pi * i / dilim
            P.append(Gf.Vec3f(r * math.cos(a), y, r * math.sin(a)))
    ust0, alt0 = dilim, 0
    for i in range(dilim):
        j = (i + 1) % dilim
        F += [[alt0 + i, alt0 + j, ust0 + j], [alt0 + i, ust0 + j, ust0 + i]]       # yan yuz
    for i in range(1, dilim - 1):
        F += [[ust0, ust0 + i, ust0 + i + 1], [alt0, alt0 + i + 1, alt0 + i]]       # kapaklar
    m.CreatePointsAttr(P)
    m.CreateFaceVertexIndicesAttr([v for f in F for v in f])
    m.CreateFaceVertexCountsAttr([3] * len(F))
    m.CreateDisplayColorAttr([Gf.Vec3f(*renk)])
    m.CreateSubdivisionSchemeAttr("none")
    return m


def urun_cisim(yol, r, kal, ym, kg, renk, x, z):
    xf = UsdGeom.Xform.Define(stage, yol)
    xf.AddTranslateOp().Set(Gf.Vec3d(x, 0.0, z))
    mesh = silindir_ag(stage, yol + "/ag", r, kal, ym, renk)
    UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
    UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(kg))
    UsdPhysics.CollisionAPI.Apply(mesh.GetPrim())
    UsdPhysics.MeshCollisionAPI.Apply(mesh.GetPrim()).CreateApproximationAttr("convexHull")
    urun_col.CreateIncludesRel().AddTarget(mesh.GetPath())
    return xf


# ---- TEPSI: 1,5 mm sac taban + 12 mm kenar (DOLU 12 mm DEGIL — bkz. baslik notu)
R_TEPSI, R_PIDE = 0.170, 0.140
kg_tepsi = math.pi * R_TEPSI ** 2 * 0.0015 * 7900 + 2 * math.pi * R_TEPSI * 0.012 * 0.0015 * 7900
kg_pide = math.pi * R_PIDE ** 2 * 0.008 * 1000.0                       # ham hamur ~1000 kg/m3 [V]
print("TEPSI %.3f kg · PIDE %.3f kg" % (kg_tepsi, kg_pide))

y_tabla_ust = 0.100        # tabla ust yuzu (CAD: y=100 mm)
urun_cisim("/World/TEPSI", R_TEPSI, 0.012, y_tabla_ust + 0.0075, kg_tepsi, (0.72, 0.75, 0.78), BASLANGIC, PIVOT[2])
urun_cisim("/World/PIDE", R_PIDE, 0.008, y_tabla_ust + 0.0175, kg_pide, (0.91, 0.84, 0.68), BASLANGIC, PIVOT[2])

# ---- ROBOT: UR10e, istasyonun onunde yerde
kok = get_assets_root_path()
UR = kok + "/Isaac/Robots/UniversalRobots/ur10e/ur10e.usd"
# DIKKAT: referans verilen prim'e dogrudan xformOp eklenemiyor (referans kendi op sirasini
# getiriyor). O yuzden once bos bir KONUM Xform'u kurulup robot onun ICINE referanslaniyor.
rk = UsdGeom.Xform.Define(stage, "/World/ROBOT")
rk.AddTranslateOp().Set(Gf.Vec3d(ISTASYON, 0.0, 0.70))     # istasyonun 700 mm onunde, yerde
rk.AddRotateYOp().Set(180.0)                                # makineye donuk
rb = stage.OverridePrim("/World/ROBOT/ur10e")
rb.GetReferences().AddReference(UR)
print("robot:", UR)

stage.GetRootLayer().Save()
print("YAZILDI ->", CIKTI, "%.2f MB" % (os.path.getsize(CIKTI) / 1048576.0))

# ---- hizli saglama: sahne aciliyor mu, robot eklemleri var mi
omni.usd.get_context().open_stage(CIKTI)
app.update(); app.update()
st = omni.usd.get_context().get_stage()
n_ek = sum(1 for p in st.Traverse() if p.IsA(UsdPhysics.RevoluteJoint) or p.IsA(UsdPhysics.PrismaticJoint))
n_rb = sum(1 for p in st.Traverse() if p.HasAPI(UsdPhysics.RigidBodyAPI))
print("SAHNE: %d eklem · %d rijit cisim" % (n_ek, n_rb))
rp = st.GetPrimAtPath("/World/ROBOT/ur10e")
print("robot prim gecerli:", rp.IsValid(), "· alt prim:", len(list(rp.GetChildren())) if rp.IsValid() else 0)
app.close()
