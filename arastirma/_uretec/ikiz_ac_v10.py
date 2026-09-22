# -*- coding: utf-8 -*-
# DIJITAL IKIZ + KUMANDA PANELI (v10)
#   C:\isaacsim\python.bat ikiz_ac_v10.py
# v5'ten farki: KESIT ARACI acildi (omni.kit.window.section — Isaac'ta kurulu ama
# bu profilde kapaliydi) + panele GIZLE dugmeleri geldi: dis kabuk, kaset govdesi,
# motor paketi, pano/sogutma tek tikla kaybolur, tekrar basinca geri gelir.
# v4'ten farki: HIC TURKCE HARF YOK. Ne panelde ne konsolda. Kemal: "turkce
# karakter kullanma, u yerine u yap gibi". Robot yok, zemin gorunmez.
import json, math, os, sys, time

_T0 = time.time()


def sure(s):
    print("[%6.1f sn] %s" % (time.time() - _T0, s), flush=True)


from isaacsim import SimulationApp
app = SimulationApp({"headless": False, "width": 1600, "height": 900})

# KESIT ARACI: Isaac'in Section Tool eklentisi kurulu ama base profilde kapali.
# Aciyoruz; Window menusunde "Section" olarak cikar, viewport'a kesme duzlemi koyar.
from isaacsim.core.utils.extensions import enable_extension
_KESIT = enable_extension("omni.kit.window.section")

import omni.usd
import omni.ui as ui
from pxr import Usd, UsdGeom, UsdLux, Gf
from isaacsim.core.api import World

FIZ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat3d\fizik"
KOK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
with open(os.path.join(KOK, "otonom", "hat3d", "sim_makine.json"), encoding="utf-8") as f:
    MAK = json.load(f)
T = MAK["tabla"]

sure("kesit araci: %s" % ("ACIK" if _KESIT else "ACILAMADI"))
sure("sahne aciliyor")
omni.usd.get_context().open_stage(os.path.join(FIZ, "TOPPING_IKIZ_v13.usd"))
for _ in range(20): app.update()
st = omni.usd.get_context().get_stage()
sure("sahne acildi")

if not st.GetPrimAtPath("/World/Isik_Kubbe").IsValid():
    UsdLux.DomeLight.Define(st, "/World/Isik_Kubbe").CreateIntensityAttr(1200.0)
    d = UsdLux.DistantLight.Define(st, "/World/Isik_Gunes")
    d.CreateIntensityAttr(3000.0)
    UsdGeom.Xformable(d.GetPrim()).AddRotateXYZOp().Set(Gf.Vec3f(-45.0, 35.0, 0.0))

DT = 1.0 / 120.0
world = World(stage_units_in_meters=1.0, physics_dt=DT, rendering_dt=DT)
sure("fizik kuruluyor")
world.reset()
sure("fizik hazir")

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


# yuva kodlari JSON'da turkce; PANELDE yalniz ASCII yaziyoruz
RECETE = [("KASARLI PIDE", ["KAŞAR_KABI"]),
          ("SUCUKLU PIDE", ["KAŞAR_KABI", "KÜP_SUCUK"]),
          ("KIYMALI PIDE", ["KIYMA"]),
          ("KUSBASILI PIDE", ["KUŞBAŞI"]),
          ("LAHMACUN", ["HARÇ_1"]),
          ("PIZZA", ["HARÇ_2", "KAŞAR_KABI", "KÜP_SUCUK"])]
ASCII_AD = {"KAŞAR_KABI": "kasar", "KÜP_SUCUK": "kup sucuk", "KIYMA": "kiyma",
            "KUŞBAŞI": "kusbasi", "HARÇ_1": "lahmacun harci", "HARÇ_2": "pizza sosu"}

D = {"kuyruk": [], "bos": 0, "surekli": False, "dur": False, "durum": "hazir", "sayac": 0}


def sec(ad):
    D["kuyruk"].append(ad); D["dur"] = False


def surekli_degis(v):
    D["surekli"] = bool(v)
    if v: D["kuyruk"] = []


def durdur():
    D["dur"] = True; D["surekli"] = False; D["kuyruk"] = []


# ---- GIZLE: ici gorunsun diye parca obeklerini kapatip acar
def _yollar(kosul):
    y = []
    for p in st.Traverse():
        if p.IsA(UsdGeom.Mesh) and kosul(p.GetName(), p.GetPath().pathString):
            y.append(p)
    return y


OBEK = {}


def obek_kur():
    kabuk = ("dis_arka", "dis_taban", "dis_tavan", "dis_yan_sag", "dis_yan_sol",
             "ic_kabuk", "pu_arka", "pu_sag", "pu_sol", "pu_taban", "pu_tavan")
    OBEK["DIS KABUK"] = _yollar(lambda a, y: a in kabuk)
    OBEK["KASET GOVDESI"] = _yollar(lambda a, y: a == "govde" or a.endswith("__govde") or a == "pompa_govdesi")
    OBEK["MOTOR PAKETI"] = _yollar(lambda a, y: a.startswith(("motor_", "reduktor_", "soket_", "surucu")))
    OBEK["PANO / SOGUTMA"] = _yollar(lambda a, y: a.startswith(("pano_kutusu", "sogutma_grubu", "evaporator", "ups", "guc_kaynagi", "fan")))


GIZLI = set()


def gizle_degis(ad, kapali):
    if kapali: GIZLI.add(ad)
    else: GIZLI.discard(ad)
    for p in OBEK.get(ad, []):
        im = UsdGeom.Imageable(p)
        if kapali: im.MakeInvisible()
        else: im.MakeVisible()
    print("%s: %s (%d parca)" % (ad, "gizli" if kapali else "gorunur", len(OBEK.get(ad, []))), flush=True)


obek_kur()


sure("panel kuruluyor")
pencere = ui.Window("AUTOKITCH TOPPING", width=330, height=640)
with pencere.frame:
    with ui.VStack(spacing=7, height=0):
        ui.Spacer(height=4)
        ui.Label("URUN SEC", height=22, style={"font_size": 18})
        for _ad, _ in RECETE:
            ui.Button(_ad, height=33, clicked_fn=lambda a=_ad: sec(a))
        ui.Spacer(height=6)
        with ui.HStack(height=26, spacing=8):
            _cb = ui.CheckBox(width=22)
            _cb.model.add_value_changed_fn(lambda m: surekli_degis(m.get_value_as_bool()))
            ui.Label("surekli uret")
        ui.Button("DURDUR", height=28, clicked_fn=durdur)
        ui.Spacer(height=10)
        ui.Label("GIZLE (icini gor)", height=22, style={"font_size": 15})
        for _ob in ("DIS KABUK", "KASET GOVDESI", "MOTOR PAKETI", "PANO / SOGUTMA"):
            with ui.HStack(height=24, spacing=8):
                _g = ui.CheckBox(width=22)
                _g.model.add_value_changed_fn(
                    lambda m, o=_ob: gizle_degis(o, m.get_value_as_bool()))
                ui.Label("%s (%d)" % (_ob, len(OBEK.get(_ob, []))))
        ui.Spacer(height=8)
        l_durum = ui.Label("hazir", height=22, style={"font_size": 16})
        l_sayac = ui.Label("uretilen: 0", height=20)
        l_eksen = ui.Label("", height=20)
sure("panel kuruldu")


def yaz(s):
    D["durum"] = s
    l_durum.text = s
    l_sayac.text = "uretilen: %d" % D["sayac"]
    l_eksen.text = "araba X = %.0f mm" % araba_x()


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
    yaz("%s  %.0f g" % (ASCII_AD.get(kod, k), y["doz_g"]))
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
    print("== " + ad, flush=True)
    eksenGit(T["istasyon_x"])
    for kod in adimlar:
        if not app.is_running() or D["dur"]: break
        dozla(kod)
    eksenGit(T["istasyon_x"])
    if not D["dur"]:
        D["sayac"] += 1
        print("   bitti - firina", flush=True)
    yaz("hazir")


adim(60)
yaz("hazir")
sure("HAZIR - soldaki AUTOKITCH panelinden urun sec")

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
