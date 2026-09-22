# -*- coding: utf-8 -*-
"""TOPPING MODULU -> ISAAC SIM FIZIKLI USD (2. asama) — v4

v1 TESTINDE CIKAN GERCEK HATA: tabla dondu ama ARABA ve 12 MIL KILITLENDI.
Sebep: makinenin kendi parcalari birbirine CARPISIYORDU. Kizak blogu rayi sariyor, helezon
kasetin icinde donuyor, mil kovandan geciyor — gercekte bu temaslari YATAK ve KIZAK tasir,
simulasyonda ise EKLEM tasir. Temas birakilinca parcalar birbirine kenetlenip duruyor.
COZUM: makinenin butun parcalari tek bir CARPISMA GRUBUNA konur ve grup KENDISIYLE carpismaz.
Urun (tepsi, pide, dokulen malzeme) ayri grupta kalir ve makineyle NORMAL carpisir.

v3: SURUCU KUVVET SINIRLARI GERCEK MOTORLARDAN. v2'de X ekseni 2000 N ile suruluyordu (uydurma) —
0,008 s'de tam hiza ciktigi icin atalet sorusu hic sinanmiyordu. Artik:
  X ekseni   NEMA23 1,2 N·m · GT3 60,00 mm/tur -> 125,7 N
  TABLA      NEMA23 pancake i=1               -> 0,9 N·m
  kaset mili NEMA23 1,2 N·m + planet i=10     -> 12 N·m

ISAAC'IN KENDI PYTHON'U ILE CALISIR:
    C:\\isaacsim\\python.bat topping_usd_v1.py

1. asama (topping_fizik_ihrac_v1.py, CadQuery ile) parcalari ag + kutle + grup olarak yazdi.
Bu dosya onu okuyup GERCEK FIZIKLI sahneyi kuruyor:

  /World/TOPPING/SABIT              statik gövde — ucgen ag carpisma (hareket etmez)
  /World/TOPPING/ARABA              rijit cisim + PRIZMATIK eklem (X)  · strok sim_makine.json'dan
  /World/TOPPING/TABLA              rijit cisim + DONER eklem (Y)      · araba'ya bagli
  /World/TOPPING/HELEZON_<yuva>     rijit cisim + DONER eklem (Z)      · 6 adet
  /World/TOPPING/KARISTIRICI_<yuva> rijit cisim + DONER eklem (Z)      · 6 adet

Hareketli parcalarda carpisma KONVEKS AYRISTIRMA (convexDecomposition) — helezon kanadi ve
ormcek gibi ici bos bicimler konveks kabukla yanlis carpisir.
Her eklemde SURUCU (drive) var: hiz modunda, gercek devirlerle.
"""
import json, math, os, sys
import numpy as np

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, PhysxSchema, Gf, Sdf, Vt

KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
GIR = os.path.join(KOK, "otonom", "hat3d", "fizik")
CIKTI = os.path.join(GIR, "TOPPING_fizik_v4.usd")

RENK = {  # tonlar model-viewer'daki paletle ayni kalsin
    "sac": (0.74, 0.77, 0.80), "celik": (0.66, 0.69, 0.73), "koyu": (0.22, 0.24, 0.27),
    "pom": (0.90, 0.90, 0.88), "silikon": (0.95, 0.45, 0.35), "cam": (0.70, 0.85, 0.95),
    "pu": (0.93, 0.90, 0.78), "bakir": (0.72, 0.45, 0.20), "kart": (0.10, 0.45, 0.25),
    "motor": (0.30, 0.32, 0.36),
}


def temiz(s):
    """USD prim adi: harf/rakam/alt cizgi, rakamla baslamaz"""
    tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U", "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"}
    s = "".join(tr.get(c, c) for c in s)
    s = "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in s)
    while "__" in s: s = s.replace("__", "_")
    return ("P_" + s) if (not s or s[0].isdigit()) else s


def main():
    with open(os.path.join(GIR, "topping_fizik_v1.json"), encoding="utf-8") as f:
        M = json.load(f)
    Z = np.load(os.path.join(GIR, "topping_fizik_v1.npz"))
    P = M["parca"]
    print("okundu: %d parca · %d eklem" % (len(P), len(M["eklem"])))

    stage = Usd.Stage.CreateNew(CIKTI)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)      # CAD'imizde Y yukari
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdPhysics.SetStageKilogramsPerUnit(stage, 1.0)

    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())

    # ---- fizik sahnesi
    scn = UsdPhysics.Scene.Define(stage, "/World/physicsScene")
    scn.CreateGravityDirectionAttr(Gf.Vec3f(0.0, -1.0, 0.0))
    scn.CreateGravityMagnitudeAttr(9.81)
    px = PhysxSchema.PhysxSceneAPI.Apply(scn.GetPrim())
    px.CreateEnableGPUDynamicsAttr(True)
    px.CreateSolverTypeAttr("TGS")
    px.CreateTimeStepsPerSecondAttr(240)                  # dozaj 8,5 mm/s — ince adim gerekiyor

    # ---- zemin: makine y=0'da duruyor, zemin onun altinda
    gp = UsdGeom.Mesh.Define(stage, "/World/Zemin")
    s_ = 6.0
    gp.CreatePointsAttr([Gf.Vec3f(-s_, 0, -s_), Gf.Vec3f(s_, 0, -s_), Gf.Vec3f(s_, 0, s_), Gf.Vec3f(-s_, 0, s_)])
    gp.CreateFaceVertexCountsAttr([4]); gp.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    gp.CreateDisplayColorAttr([Gf.Vec3f(0.35, 0.36, 0.38)])
    UsdPhysics.CollisionAPI.Apply(gp.GetPrim())

    kok = UsdGeom.Xform.Define(stage, "/World/TOPPING")

    # ---- CARPISMA GRUPLARI
    # MAKINE grubu KENDISIYLE carpismaz: parcalarin birbirine gore hareketini EKLEMLER tanimliyor,
    # temas degil. (v1'de araba raya, helezon kasete kenetlenip hic donmuyordu.)
    g_mak = UsdPhysics.CollisionGroup.Define(stage, "/World/CarpismaGrubu_MAKINE")
    g_mak.CreateFilteredGroupsRel().SetTargets(["/World/CarpismaGrubu_MAKINE"])
    g_urun = UsdPhysics.CollisionGroup.Define(stage, "/World/CarpismaGrubu_URUN")   # tepsi/pide/malzeme buraya
    mak_col = g_mak.GetCollidersCollectionAPI()

    # ---- gruplari topla
    gruplar = {}
    for i, p in enumerate(P):
        gruplar.setdefault(p["grup"], []).append(i)

    grup_yolu = {}
    for g, idx in sorted(gruplar.items()):
        gy = "/World/TOPPING/" + temiz(g)
        grup_yolu[g] = gy
        xf = UsdGeom.Xform.Define(stage, gy)
        hareketli = (g != "SABIT")
        kutle = sum(P[i]["kutle_kg"] for i in idx)

        if hareketli:
            UsdPhysics.RigidBodyAPI.Apply(xf.GetPrim())
            ma = UsdPhysics.MassAPI.Apply(xf.GetPrim())
            ma.CreateMassAttr(float(max(kutle, 1e-3)))     # ATALET PhysX tarafindan agdan hesaplanir
            prb = PhysxSchema.PhysxRigidBodyAPI.Apply(xf.GetPrim())
            prb.CreateSolverPositionIterationCountAttr(32)
            prb.CreateSolverVelocityIterationCountAttr(1)  # NVIDIA: TGS'de hiz yinelemesi 0-1 olsun

        for i in idx:
            p = P[i]
            mp = gy + "/" + temiz(p["ad"])
            mesh = UsdGeom.Mesh.Define(stage, mp)
            V = Z["V%d" % i]; F = Z["F%d" % i]
            mesh.CreatePointsAttr(Vt.Vec3fArray.FromNumpy(V.astype(np.float32)))
            mesh.CreateFaceVertexIndicesAttr(Vt.IntArray.FromNumpy(F.reshape(-1).astype(np.int32)))
            mesh.CreateFaceVertexCountsAttr(Vt.IntArray.FromNumpy(np.full(len(F), 3, dtype=np.int32)))
            mesh.CreateDisplayColorAttr([Gf.Vec3f(*RENK.get(p["mal"], (0.6, 0.6, 0.6)))])
            mesh.CreateSubdivisionSchemeAttr("none")

            UsdPhysics.CollisionAPI.Apply(mesh.GetPrim())
            mc = UsdPhysics.MeshCollisionAPI.Apply(mesh.GetPrim())
            if hareketli:
                # helezon kanadi / ormcek gibi ici bos bicimler konveks KABUKLA yanlis carpisir
                mc.CreateApproximationAttr("convexDecomposition")
                PhysxSchema.PhysxConvexDecompositionCollisionAPI.Apply(mesh.GetPrim())
            else:
                mc.CreateApproximationAttr("none")          # statikte gercek ucgen ag kullanilabilir
            mak_col.CreateIncludesRel().AddTarget(mp)          # makine grubuna kaydet
        print("  %-24s %3d parca · %8.2f kg · %s" % (g, len(idx), kutle, "HAREKETLI" if hareketli else "statik"))

    # ---- eklemler
    def eklem_kur(e):
        g = e["grup"]
        if g not in grup_yolu: return None
        yol = "/World/TOPPING/EKLEM_" + temiz(e["ad"])
        if e["tip"] == "prizmatik":
            j = UsdPhysics.PrismaticJoint.Define(stage, yol)
            j.CreateAxisAttr(e["eksen"])
            j.CreateLowerLimitAttr(float(e["alt"] - e["baslangic"]))    # eklem yerel: baslangic 0 kabul
            j.CreateUpperLimitAttr(float(e["ust"] - e["baslangic"]))
            tip_s = "linear"
            hedef_hiz = 0.0
            # GERCEK SINIR: NEMA23 1,2 N·m · GT3 kasnak turda 60,00 mm -> F = T·2π/adim
            maxkuv = 1.2 * 2.0 * math.pi / 0.060                        # = 125,7 N
        else:
            j = UsdPhysics.RevoluteJoint.Define(stage, yol)
            j.CreateAxisAttr(e["eksen"])
            tip_s = "angular"
            hedef_hiz = 0.0
            # GERCEK SINIR — ZAYIF HALKA REDUKTOR: motor 1,60 N·m x i=10 = 16 N·m verirdi ama
            # SureGear PGCN23-1025'in NOMINAL cikis torku 5 N·m. Tahrik zincirini redüktör
            # siniriyor, motor degil. Tabla = NEMA23 pancake i=1 -> 0,9 N·m.
            maxkuv = 0.9 if e["ad"] == "TABLA" else 5.0
        # body0 bos = DUNYAYA bagli (SABIT govde zaten statik, ayni sey)
        if e.get("ebeveyn") and e["ebeveyn"] in grup_yolu and e["ebeveyn"] != "SABIT":
            j.CreateBody0Rel().SetTargets([grup_yolu[e["ebeveyn"]]])
        else:
            j.CreateBody0Rel().SetTargets([])               # bos = DUNYAYA sabit (statik govde)
        j.CreateBody1Rel().SetTargets([grup_yolu[g]])
        pv = e.get("pivot", [e.get("baslangic", 0.0), 0.0, 0.0])
        j.CreateLocalPos0Attr(Gf.Vec3f(*[float(v) for v in pv]))
        j.CreateLocalPos1Attr(Gf.Vec3f(*[float(v) for v in pv]))
        j.CreateLocalRot0Attr(Gf.Quatf(1.0)); j.CreateLocalRot1Attr(Gf.Quatf(1.0))

        d = UsdPhysics.DriveAPI.Apply(j.GetPrim(), tip_s)
        d.CreateTypeAttr("force")
        d.CreateStiffnessAttr(0.0)                                      # HIZ modu: sertlik 0, sonumleme yuksek
        d.CreateDampingAttr(1e5 if tip_s == "linear" else 1e3)
        d.CreateTargetVelocityAttr(float(hedef_hiz))
        d.CreateMaxForceAttr(float(maxkuv))
        return yol

    n = 0
    for e in M["eklem"]:
        if eklem_kur(e): n += 1
    print("eklem kuruldu: %d" % n)

    stage.GetRootLayer().Save()
    print("YAZILDI -> %s" % CIKTI)
    print("   boyut: %.1f MB" % (os.path.getsize(CIKTI) / 1048576.0))


main()
app.close()
