# -*- coding: utf-8 -*-
"""TOPPING DIJITAL IKIZI — TAM SAHNE v2 (modul + robot + GERCEK tepsi + pide)

C:\\isaacsim\\python.bat topping_ikiz_v1.py

ICERIK
  · TOPPING_fizik_v6.usd        makinenin kendisi (534 parca, 14 eklem, gercek kutleler)
  · UR10e                       Isaac varlik kutuphanesinden GERCEK robot kolu
                                (1300 mm erisim · 12,5 kg yuk — bizim tepsi+urun ~1,9 kg)
  · TEPSI                       Ø340 · 1,5 mm sac + 12 mm kenar (ONEMLI NOT asagida)
  · PIDE                        Ø280 · 8 mm hamur
  · URUN carpisma grubu         tepsi/pide makineyle NORMAL carpisir; makinenin kendi
                                parcalari birbirine carpismaz (yatak/kizak isini eklem yapar)

v1'DE CIKAN IKI GERCEK BULGU:
 1) TEPSI KUTLESI. Hesapta TEPSI_K = 12 mm yaziyor; 12 mm DOLU paslanmaz Ø340 tepsi 8,6 kg
    eder — ne robot tasir ne tabla dondurur. Gercegi: 1,5 mm sac taban + 12 mm KENAR = 1,2 kg.
 2) TEPSI TABLAYA OTURMADI. 3 merkezleme pimi tablanin 5 mm ustunde; duz disk tepsi onlarin
    icine giriyordu, fizik tepsiyi asagi itip tablanin ALTINA kacirdi. Tepsinin pimlere oturan
    CUKURLARI olmak zorunda. v2'de tepsi urun_fizik_ihrac_v1.py ile CUKURLU uretiliyor.
"""
import json, math, os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import omni.usd
from isaacsim.storage.native import get_assets_root_path
from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema, Gf, Sdf, Vt
import numpy as np

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
MAKINE = os.path.join(FIZ, "TOPPING_fizik_v6.usd")
CIKTI = os.path.join(FIZ, "TOPPING_IKIZ_v6.usd")

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


UR_JSON = json.load(open(os.path.join(FIZ, "urun_fizik_v1.json"), encoding="utf-8"))

# CARPISMA GOVDESI = BASIT KONVEKS PUL, kutle = GERCEK SAC KUTLESI.
# Neden: tepsi 1,5 mm sac + kenar; boyle INCE KABUK bir govdenin konveks AYRISTIRMASI
# guvenilir degil (denendi: tepsi 137 mm yukari firladi). Carpisma icin disi onemli —
# Ø340 x 12 mm pul, tepsinin zarfinin AYNISI. Kutle CadQuery'nin olctugu gercek sac kutlesi.
def puk(yol, r, kal, kg, renk, x, y_alt, z):
    xf = UsdGeom.Xform.Define(stage, yol)
    xf.AddTranslateOp().Set(Gf.Vec3d(x, y_alt, z))
    m = UsdGeom.Mesh.Define(stage, yol + "/ag")
    P, F, n = [], [], 64
    for s_ in (0, 1):
        y = kal if s_ else 0.0
        for i in range(n):
            a = 2 * math.pi * i / n
            P.append(Gf.Vec3f(r * math.cos(a), y, r * math.sin(a)))
    for i in range(n):
        j = (i + 1) % n
        F += [[i, j, n + j], [i, n + j, n + i]]
    for i in range(1, n - 1):
        F += [[n, n + i, n + i + 1], [0, i + 1, i]]
    m.CreatePointsAttr(P)
    m.CreateFaceVertexIndicesAttr([v for f in F for v in f])
    m.CreateFaceVertexCountsAttr([3] * len(F))
    m.CreateDisplayColorAttr([Gf.Vec3f(*renk)])
    m.CreateSubdivisionSchemeAttr("none")
    UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
    UsdPhysics.MassAPI.Apply(xf.GetPrim()).CreateMassAttr(float(kg))
    UsdPhysics.CollisionAPI.Apply(m.GetPrim())
    UsdPhysics.MeshCollisionAPI.Apply(m.GetPrim()).CreateApproximationAttr("convexHull")
    urun_col.CreateIncludesRel().AddTarget(m.GetPath())
    print("  %-6s %.3f kg" % (yol.split("/")[-1], kg))
    return xf


# ---- TEPSI + PIDE
# SU ANKI TASARIM: 3 merkezleme pimi tabla ustunde y 100..105; tepsi DUZ tabanli, yani
# tablaya degil PIM UCLARINA oturuyor. Ikizi tam boyle kuruyoruz ki "tepsi kayiyor mu"
# sorusu gercek tasarim uzerinde olculsun.
KG = {p["ad"]: p["kutle_kg"] for p in UR_JSON["parca"]}
y_pim_ust = 0.105
puk("/World/TEPSI", 0.170, 0.012, KG["TEPSI"], (0.72, 0.75, 0.78), BASLANGIC, y_pim_ust + 0.0005, PIVOT[2])
puk("/World/PIDE", 0.140, 0.008, KG["PIDE"], (0.91, 0.84, 0.68), BASLANGIC, y_pim_ust + 0.0130, PIVOT[2])

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
