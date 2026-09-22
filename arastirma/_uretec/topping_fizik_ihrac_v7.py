# -*- coding: utf-8 -*-
"""TOPPING MODULU -> FIZIK IHRACI (1. asama)

Kemal: "sirada bizim seyi oraya koy topping seyini ... dijital twin kuruyoruz unutma, hersey olmali."

BU DOSYA NE YAPAR: uretim modelini (topping_cad_v11 + 6 kaset) alir, her parcayi
  - agina (ucgen) cevirir              -> Isaac Sim'de gorunur ve CARPISIR
  - hangi HAREKETLI PAKETE ait bulur   -> ARABA / TABLA / HELEZON_x / KARISTIRICI_x / SABIT
  - HACMINI olcer ve KUTLESINI hesaplar-> fizik icin sart (tork, atalet, rampa)
ve tek bir .npz + .json yazar. Ikinci asama (Isaac'in kendi Python'u) bunu okuyup
UsdPhysics eklemli sahneyi kurar.

KUTLE: parcanin gercek hacmi x malzeme yogunlugu. KATALOG parcalarinda (motor, redüktor,
kizak, doner yatak) gövde ici bos oldugu icin hacim x yogunluk YANLIS olur; onlarin kutlesi
KATALOG_KUTLE tablosundan gelir ve JSON'da "kaynak" alaniyla isaretlenir:
    olculdu  = CAD hacminden hesaplandi
    katalog  = uretici/katalog degeri
    VARSAYIM = ne olculdu ne katalog — DEGISTIRILECEK
(bkz. feedback: 'motor koy deyince kutu modelleyip birakiyorsun')
"""
import io, json, math, os, sys
import numpy as np
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d", "fizik")
os.makedirs(OUT, exist_ok=True)

import topping_cad_v16 as TC
import topping_hesap_v4 as H

# ---------------------------------------------------------------- malzeme yogunluklari (kg/m3)
YOGUNLUK = {
    "sac": 7900.0,       # 304 paslanmaz
    "celik": 7900.0,     # 304 / A4 civata
    "koyu": 7900.0,      # kararmis celik parcalar
    "pom": 1410.0,       # POM-C
    "silikon": 1150.0,   # gida silikonu
    "cam": 1200.0,       # PC / PETG seffaf
    "pu": 40.0,          # poliuretan kopuk
    "bakir": 8960.0,
    "kart": 1850.0,      # FR4 elektronik kart
    "motor": 7900.0,     # YER TUTUCU — asagida katalog tablosu eziyor
}

# ---------------------------------------------------------------- katalog kutleleri (kg)
# Not: bunlar parca SECILINCE gercek katalog degeriyle degistirilecek. Simdilik sinif tipik degeri.
KATALOG_KUTLE = [
    # (ad basi,                 kutle kg, kaynak, not)
    ("kizak_blogu_",            0.18, "katalog",
     "HIWIN HGH15CA · GERCEK CAD (TraceParts STEP AP214) modelde · katalog agirligi 0,18 kg "
     "(STEP'in dolu hacmi 0,289 kg verir; gercek arabanin ici bilya yolu ve plastik kapak, katalog degeri esas)"),
    ("motor_kablosu_",          0.02, "olculdu", "0,71 A kablo gudugu"),
    ("motor_",                  1.10, "katalog",
     "AutomationDirect STP-MTRAC-23078 · NEMA23 · 1,60 N·m tutma · 0,71 A · IP40 · GERCEK CAD modelde"),
    ("donus_motoru",            0.50, "katalog sinifi",
     "NEMA23 pancake 57x57x41 · katalogda 0,6 N·m / 0,88 A · kutle gövde boyundan (57x57x56 = 0,7 kg) olceklendi"),
    # doner yatak artik GERCEK CAD (Schaeffler XU080149) — kutlesi hacminden dogru cikiyor,
    # katalog satirina gerek yok. (Eski varsayim 2,50 kg idi; gercegi 3,27 kg.)
    ("reduktor_",               0.90, "katalog",
     "AutomationDirect SureGear PGCN23-1025 · i=10 · 60x60x79 mm · NOMINAL CIKIS TORKU 5 N·m · GERCEK CAD"),
    # --- SATIN ALINAN BIRIMLER: zarf dogru, kutle KATALOGDAN (masif kutu olarak
    #     olculunce sacma cikiyordu: sogutma 114,7 · evaporator 90,3 (masif bakir!) · UPS 49,5 kg)
    ("sogutma_grubu",          26.0, "katalog sinifi",
     "1/5 HP hermetik hava sogutmali kondenser unitesi · sinif tipigi (Embraco/Tecumseh boyu)"),
    ("evaporator",              7.0, "katalog sinifi",
     "400x180x190 fanli unit cooler · alu lamel + bakir boru, ici BOS — masif bakir degil"),
    ("fan_0",                   1.2, "katalog sinifi", "Ø200 eksenel fan 24 V"),
    ("ups",                     8.5, "katalog sinifi", "500 VA hat ici UPS (aku dahil)"),
    ("guc_kaynagi",             0.9, "katalog sinifi", "24 V 154 W DIN ray guc kaynagi"),
    ("x_motoru",                1.10, "katalog",
     "AutomationDirect STP-MTRAC-23078 · NEMA23 · 1,60 N·m tutma (GERCEK CAD)"),
]


def katalog_kutle(ad):
    for k in KATALOG_KUTLE:
        bas, kg, kaynak, aciklama = k
        if ad.startswith(bas) and kg > 0:
            return kg, kaynak, aciklama
    return None, None, None


# ---------------------------------------------------------------- hareketli paket ayrimi (hat_montaj_v18 ile AYNI)
ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi",
           "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi")
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_")


def grup_modul(ad):
    if ad.startswith(TABLA_P) and ad not in ("tabla_home_sensoru", "tabla_home_bayragi"): return "TABLA"
    if ad.startswith(ARABA_P): return "ARABA"
    return "SABIT"


# ---------------------------------------------------------------- aglama
def ag(sh, tol=0.12, aci=0.35):
    """CadQuery katisindan (V,F) — METRE cinsinden, cunku Isaac sahnesi metre calisiyor"""
    vs, ts = sh.tessellate(tol, aci)
    V = np.array([[v.x * 1e-3, v.y * 1e-3, v.z * 1e-3] for v in vs], dtype=np.float32)
    F = np.array(ts, dtype=np.int32)
    return V, F


def hacim(sh):
    try: return abs(sh.Volume()) * 1e-9          # mm3 -> m3
    except Exception: return 0.0


def kur():
    parcalar = []

    # ---- 1) MODUL (on kapak dahil: dijital ikizde kapak da var, ama acik konumda cizilecek)
    TC.PARCALAR[:] = []; TC.modul()
    ps = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom")]
    print("modul parcasi: %d" % len(ps))
    for p in ps:
        sh = p["wp"].val()
        V, F = ag(sh)
        if not len(F): continue
        h = hacim(sh)
        kg, kaynak, aciklama = katalog_kutle(p["ad"])
        if kg is None:
            kg, kaynak, aciklama = h * YOGUNLUK.get(p["mal"], 7900.0), "olculdu", "CAD hacmi x %s yogunlugu" % p["mal"]
        parcalar.append(dict(ad=p["ad"], birim="TOPPING_MODUL", grup=grup_modul(p["ad"]),
                             mal=p["mal"], hacim_m3=h, kutle_kg=kg, kaynak=kaynak, not_=aciklama, V=V, F=F))

    # ---- 2) KASETLER — her biri kendi yuvasina tasinir
    import importlib
    for ad, x0, x1, gen in TC.YUVA:
        mod = importlib.import_module(TC.KASET_CAD[ad])
        mod.PARCALAR[:] = []; mod.kap()
        xm, z0 = (x0 + x1) / 2.0, TC.ZK[0] - mod.D / 2.0
        k = ad.replace(" ", "_")
        n = 0
        for p in mod.PARCALAR:
            if p["ad"] == "tasima_tapasi": continue
            sh = p["wp"].val().translate(cq.Vector(xm, TC.KAS[0], z0))
            V, F = ag(sh)
            if not len(F): continue
            gr = p.get("grup")
            grup = "SABIT" if not gr else (("HELEZON_" if gr == "helezon" else "KARISTIRICI_") + k)
            h = hacim(sh)
            # HELEZON KANADI DILIMLENIR. Konveks carpisma govdesi helis bosluklarini DOLDURUP
            # vidayi masif silindire ceviriyordu (olculdu: vida boyunca 10 isin, hepsi kanada
            # carpti). Z'de 2,5 mm dilimlere bolununce her dilimin kabugu komsunun boslugunu
            # dolduramiyor; dilimler ayni rijit cisimde, vida yine tek parca doner.
            if gr == "helezon" and p["ad"].startswith("helezon_") and not p["ad"].endswith("cekirdek"):
                bb = sh.BoundingBox(); DZ = 2.5
                nd = max(1, int(math.ceil((bb.zmax - bb.zmin) / DZ)))
                for q in range(nd):
                    za, zb = bb.zmin + q * DZ, min(bb.zmax, bb.zmin + (q + 1) * DZ)
                    if zb - za < 0.2: continue
                    kutu = cq.Workplane("XY").box(bb.xlen + 20, bb.ylen + 20, zb - za,
                                                  centered=(True, True, False)).translate(
                                                  ((bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, za))
                    try: par = sh.intersect(kutu.val())
                    except Exception: continue
                    if par is None or abs(par.Volume()) < 1.0: continue
                    Vq, Fq = ag(par)
                    if not len(Fq): continue
                    parcalar.append(dict(ad="%s__%s_d%02d" % (k, p["ad"], q), birim="KASET_" + k, grup=grup,
                                         mal=p["mal"], hacim_m3=abs(par.Volume()) * 1e-9,
                                         kutle_kg=abs(par.Volume()) * 1e-9 * YOGUNLUK.get(p["mal"], 7900.0),
                                         kaynak="olculdu", not_="helezon kanadi dilimi (carpisma icin)", V=Vq, F=Fq))
                    n += 1
                continue
            parcalar.append(dict(ad="%s__%s" % (k, p["ad"]), birim="KASET_" + k, grup=grup,
                                 mal=p["mal"], hacim_m3=h, kutle_kg=h * YOGUNLUK.get(p["mal"], 7900.0),
                                 kaynak="olculdu", not_="CAD hacmi x malzeme yogunlugu", V=V, F=F))
            n += 1
        print("  kaset %-12s %3d parca" % (ad, n))

    return parcalar


def yaz(parcalar):
    # ---- eklem tanimlari: makinenin gercek hareket eksenleri
    # X arabasi prizmatik; tabla Y ekseninde doner; kaset milleri Z ekseninde doner.
    # strok, istasyon ve pivot sim_makine.json'dan OKUNUR (kontrol yazilimiyla ayni kaynak)
    with io.open(os.path.join(os.path.dirname(OUT), "sim_makine.json"), encoding="utf-8") as f:
        SM = json.load(f)
    T = SM["tabla"]
    eklem = [dict(ad="X", tip="prizmatik", grup="ARABA", eksen="X",
                  alt=T["strok"][0] * 1e-3, ust=T["strok"][1] * 1e-3,
                  baslangic=T["baslangic_x"] * 1e-3, istasyon=T["istasyon_x"] * 1e-3,
                  hiz_mm_s=T["x_gecis_hiz"], doz_hiz_mm_s=T["x_doz_hiz"]),
             dict(ad="TABLA", tip="doner", grup="TABLA", eksen="Y",
                  pivot=[v * 1e-3 for v in T["pivot"]], rpm=T["rpm"], ebeveyn="ARABA")]
    for a_, x0, x1, gen in TC.YUVA:
        k = a_.replace(" ", "_")
        mod = sys.modules[TC.KASET_CAD[a_]]
        xm = (x0 + x1) / 2.0
        y_ = next(v for v in SM["yuvalar"] if v["kod"] == k)
        for rol, g, kot in (("doz", y_["grup_doz"] + "_" + k, TC.KAS[0] + (mod.CY if y_["grup_doz"] == "HELEZON" else mod.YC)),
                            ("karis", y_["grup_karis"] + "_" + k, TC.KAS[0] + (mod.CY if y_["grup_karis"] == "HELEZON" else mod.YC))):
            eklem.append(dict(ad=g, tip="doner", grup=g, eksen="Z", rol=rol,
                              pivot=[xm * 1e-3, kot * 1e-3, 0.0], ebeveyn="SABIT",
                              rpm=(y_["helezon_rpm"] if rol == "doz" else 4.0)))

    grup_kutle = {}
    for p in parcalar:
        grup_kutle[p["grup"]] = grup_kutle.get(p["grup"], 0.0) + p["kutle_kg"]

    meta = dict(
        modul=dict(w=TC.W, y=TC.Y, d=TC.D, agz=list(TC.AGZ), kas=list(TC.KAS), zk=list(TC.ZK)),
        olcek="metre (CAD mm / 1000)",
        parca=[{k: v for k, v in p.items() if k not in ("V", "F")} for p in parcalar],
        eklem=eklem,
        grup_kutle_kg={k: round(v, 3) for k, v in sorted(grup_kutle.items())},
    )
    with io.open(os.path.join(OUT, "topping_fizik_v1.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)

    d = {}
    for i, p in enumerate(parcalar):
        d["V%d" % i] = p["V"]; d["F%d" % i] = p["F"]
    np.savez_compressed(os.path.join(OUT, "topping_fizik_v1.npz"), **d)

    ucgen = sum(len(p["F"]) for p in parcalar)
    print("\nPARCA %d · UCGEN %d" % (len(parcalar), ucgen))
    print("GRUP KUTLELERI (kg):")
    for g, kg in sorted(grup_kutle.items()):
        print("   %-24s %8.2f" % (g, kg))
    v = [p for p in parcalar if p["kaynak"] == "VARSAYIM"]
    print("KUTLESI VARSAYIM OLAN %d parca: %s" % (len(v), ", ".join(sorted({x["ad"] for x in v}))[:160]))
    print("yazildi -> %s" % OUT)


if __name__ == "__main__":
    yaz(kur())
