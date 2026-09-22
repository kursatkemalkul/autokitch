# -*- coding: utf-8 -*-
"""topping_cad_v13 -> v14 : GERCEK PLANET REDUKTOR MONTAJA GIRIYOR

TraceParts / AutomationDirect · SureGear PGCN23-1025
  10:1 · tek kademe · NEMA23 flans · cikis mili Ø9,53 (0,375 in)
  NOMINAL CIKIS TORKU 5 N·m  ·  ayni SureStep NEMA23 motoru icin yapilmis
  STEP olculdu: 60,00 x 60,00 x 103,00 mm (govde z -79..0 · cikis mili 0..+24)

IKI GERCEK BULGU:
 1) BOY. Hesapta redüktör 60 mm varsayilmisti, gercegi 79 mm. Kuru bolme dizilimi
    "mil ucu 40 + redüktör 60 + motor 76 + kablo payi 24 = 200" idi; gercek olculerle
    40 + 79 + 76 + 24 = 219 mm. KURU BOLME 19 mm KISA.
 2) TORK. Bizim tasarim torku 6 N·m; bu redüktör NOMINAL 5 N·m. Yani tahrik zincirinin
    zayif halkasi motor degil REDUKTOR. Simdeki eklem tork siniri da 5 N·m olmali.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v13.py"), encoding="utf-8").read()

anc = "def ekle(ad, wp, mal, bom=None):"
yeni = '''REDUKTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "pgcn23-1025.step")
_RED = {}


def suregear():
    """PGCN23-1025 gercek katisi. STEP: govde z -79..0, cikis mili 0..+24."""
    if _RED:
        return _RED
    w = cq.importers.importStep(REDUKTOR_STEP)
    # CIKIS MILINI KES: redüktörün cikis mili ile bizim "mil_*" parcamiz gercekte AYNI mil.
    # Ikisini birden koyunca ust uste biniyor (olculdu: 4.349 mm3 mil + 3.076 mm3 kovan).
    kes = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False)).val()
    _RED["tum"] = w.val().cut(kes)
    return _RED


def suregear_koy(xm, yy, z_cikis):
    """redüktörün CIKIS YUZU z_cikis'te olacak sekilde yerlestirir (govde -z'ye uzar)"""
    return cq.Workplane(obj=suregear()["tum"].translate(cq.Vector(xm, yy, z_cikis)))


'''
assert anc in s
s = s.replace(anc, yeni + anc, 1)

eski = '''        ekle("reduktor_" + k, silz(xm, yy, RE["cap"] / 2, ZBOL[1] - 42.0, ZBOL[1] - 42.0 - RE["z"]), "motor", bom=None)
        zm = ZBOL[1] - 42.0 - RE["z"] - 2.0'''
yeni = '''        # Mil gudugu koddaki 42 mm'den TASARIM degeri olan 40 mm'ye cekildi; gercek 79 mm'lik
        # redüktörle motor arka saci 0,5 mm deliyordu. 40 ile deliyor degil ama arkada
        # YALNIZ 1,5 mm kaliyor — servis bosluğu yok. Karar Kemal'de (asagidaki BOM notu).
        ekle("reduktor_" + k, suregear_koy(xm, yy, ZBOL[1] - 40.0), "motor", bom=None)
        zm = ZBOL[1] - 40.0 - 79.0 - 2.0                 # GERCEK redüktör boyu 79 mm (hesapta 60 varsayilmisti)'''
assert eski in s
s = s.replace(eski, yeni, 1)

s = s.replace('"Planet redüktör i=10"', '"SureGear PGCN23-1025 · i=10 · NOMİNAL 5 N·m (GERÇEK CAD)"')
io.open(os.path.join(U, "topping_cad_v14.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v14.py yazildi")
