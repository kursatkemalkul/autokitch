# -*- coding: utf-8 -*-
"""TOPPING v22 X arabasi icin kritik konumlarda gercek kati carpisma denetimi.

Kaset geometrisini degistirmez. Park, donanim limitleri, her kasetin spiral dozaj
baslangic/orta/bitis noktasi ve firina aktarma konumunu kontrol eder.
"""
import io
import json
import math
import os

import cadquery as cq

import topping_cad_v22 as C
import topping_hesap_v6 as H


ARABA_P = (
    "kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi",
    "donus_motoru", "tahrik_lokmasi", "siyirici_apron", "kayis_kolu",
    "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi",
    "x_bayragi", "kilit_burcu_",
)
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_", "calisma_diski", "disk_pimi_")


def hareketli(ad):
    return ad.startswith(ARABA_P) or ad.startswith(TABLA_P)


def bbox_cakis(a, b, pay=0.0):
    return not (
        a.xmax <= b.xmin + pay or b.xmax <= a.xmin + pay
        or a.ymax <= b.ymin + pay or b.ymax <= a.ymin + pay
        or a.zmax <= b.zmin + pay or b.zmax <= a.zmin + pay
    )


def doz_xleri():
    """r^2 dogrusal spiral yasasinin kritik yaricaplarindaki tabla merkezleri."""
    z_ofset = 20.0
    r_orta = math.sqrt((H.R_DIS ** 2 + H.R_IC ** 2) / 2.0)
    yaricap = (("bas", H.R_DIS), ("orta", r_orta), ("bit", H.R_IC))
    sonuc = []
    for ad, x0, x1, _ in C.YUVA:
        agiz_x = (x0 + x1) / 2.0
        for faz, r in yaricap:
            dx = math.sqrt(max(0.0, r * r - z_ofset * z_ofset))
            sonuc.append(("%s_%s" % (ad.replace(" ", "_"), faz), agiz_x - dx))
    return sonuc


def calistir():
    C.PARCALAR[:] = []
    C.modul()
    gercek = [p for p in C.PARCALAR if not p["ad"].startswith("_bom")]
    mov = [p for p in gercek if hareketli(p["ad"])]
    sab = [p for p in gercek if not hareketli(p["ad"])]
    sabit = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in sab]

    konumlar = [
        ("limit_sol", H.X_LIMIT_SOL),
        ("park", H.X_PARK),
        *doz_xleri(),
        ("aktarma", H.X_AKTARMA),
        ("limit_sag", H.X_LIMIT_SAG),
    ]
    # Ayni x'i tek kez tara; tum adlari raporda koru.
    tek = {}
    for ad, x in konumlar:
        tek.setdefault(round(x, 4), []).append(ad)

    bulgu = []
    rapor = []
    for x in sorted(tek):
        delta = x - C.XC_TABLA
        poz_bulgu = []
        for p in mov:
            sh = p["wp"].val().moved(cq.Location(cq.Vector(delta, 0.0, 0.0)))
            bb = sh.BoundingBox()
            for sad, ssh, sbb in sabit:
                if not bbox_cakis(bb, sbb):
                    continue
                try:
                    v = sh.intersect(ssh).Volume()
                except Exception:
                    v = -1.0
                if v > 1.0 or v < 0.0:
                    kayit = dict(x_mm=round(x, 3), faz=tek[x], hareketli=p["ad"], sabit=sad,
                                 ortak_mm3=round(v, 2))
                    poz_bulgu.append(kayit)
                    bulgu.append(kayit)
        rapor.append(dict(x_mm=round(x, 3), faz=tek[x], sonuc="TEMIZ" if not poz_bulgu else "KALDI",
                          bulgu=len(poz_bulgu)))
        print("X %8.2f  %-42s %s" % (x, ",".join(tek[x]), "TEMIZ" if not poz_bulgu else "%d BULGU" % len(poz_bulgu)))

    sonuc = dict(surum="TOPPING v22 / hareket kontrol v1", hareketli_parca=len(mov),
                 sabit_parca=len(sab), kontrol=rapor, bulgu=bulgu,
                 sonuc="GECTI" if not bulgu else "KALDI")
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_hareket_kontrol_v1.json")
    with io.open(yol, "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=2)
    print("HAREKET DENETIMI:", sonuc["sonuc"], "-", len(tek), "kritik konum -", len(bulgu), "bulgu")
    print("YAZILDI", yol)
    assert not bulgu


if __name__ == "__main__":
    calistir()
