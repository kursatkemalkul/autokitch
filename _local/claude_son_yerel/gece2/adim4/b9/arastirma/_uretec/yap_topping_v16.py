# -*- coding: utf-8 -*-
"""topping_cad_v15 -> v16 : GERCEK DONER YATAK (Schaeffler XU080149)

TraceParts / Schaeffler (INA) · XU080149 · caprazmakarali doner yatak, disli yok, iki tarafi
kece keceli. STEP olculdu: Ø196,85 x 22,27 mm · 14 kati · celik hacminden 3,27 kg.

BULGU — YATAK TASARIMDAKINDEN BUYUK: modelde yatak Ø160 (ic Ø70) varsayilmisti; gercek
katalog parcasi Ø196,85. Araba plakasi 300 mm genis oldugu icin SIGIYOR ama yatak yuvasi
ve AYAR BILEZIGI buyumek zorunda (bilezik disi Ø170 -> Ø210).

AYRICA NOT (Kemal'e): bu sinif caprazmakarali yatak, tasidigimiz yuk icin FAZLA. Tabla 5,11 +
urun 1,71 = 6,8 kg, devirme momenti 1,7 N·m civari. Bir XU080149 birkac yuz euro; ayni isi
cok daha ucuz bir ince kesit bilyali yatak da gorur. Karar Kemal'in — model gercek parcayla
kuruldu, degistirmek tek satir.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v15.py"), encoding="utf-8").read()

anc = "def ekle(ad, wp, mal, bom=None):"
yeni = '''YATAK_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "xu080149.stp")
_YAT = {}


def xu080149():
    """STEP'te yatak ekseni X boyunca (x 0..22,27). Bizim tablada eksen Y (dusey),
    o yuzden Z etrafinda 90 derece ceviriyoruz: x -> y."""
    if _YAT: return _YAT
    w = cq.importers.importStep(YATAK_STEP)
    _YAT["kati"] = w.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0)
    return _YAT


'''
assert anc in s
s = s.replace(anc, yeni + anc, 1)

eski = '''    dy = sily(Xc, ZT, 80.0, 58.5, 78.5).cut(sily(Xc, ZT, 35.0, 57.5, 79.5))
    ekle("doner_yatak", dy, "celik", bom=("İnce kesit döner yatak (slewing ring)", 1, "4 nokta bilyalı · H20 · iç Ø70 dış Ø160 [V: katalogdan doğrulanacak]",
         "Ø340 konsol tablanın devirme momentini doğrudan alır; iç bilezik plakaya 8 × M5 havşa"))
    ekle("ayar_bilezigi", sily(Xc, ZT, 85.0, 78.5, 86.0).cut(sily(Xc, ZT, 45.0, 77.5, 87.0)), "celik",'''
yeni = '''    # v16: GERCEK katalog yatagi. Ø196,85 x 22,27 — tasarimda Ø160 varsayilmisti.
    _y = xu080149()["kati"].translate(cq.Vector(Xc, 58.5, ZT))
    ekle("doner_yatak", cq.Workplane(obj=_y), "celik",
         bom=("Çapraz makaralı döner yatak", 1, "Schaeffler (INA) XU080149 · Ø196,85 × 22,27 · GERÇEK CAD",
              "Ø340 konsol tablanın devirme momentini doğrudan alır; iç bilezik plakaya cıvatalı"))
    # AYAR BILEZIGI ZATEN BUNUN ICIN VAR (isleme araligi 2-14 mm): yatak 20 yerine 22,27
    # cikinca fazlaligi bilezik yutar, gobek ve tabla YERINDE KALIR. 7,5 -> 5,23 mm islenir.
    ekle("ayar_bilezigi", sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0)), "celik",'''
assert eski in s
s = s.replace(eski, yeni, 1)
s = s.replace('"304 · dış Ø170 iç Ø90 · kalınlık 7,5 (işleme aralığı 2–14)"',
              '"304 · dış Ø210 iç Ø100 · kalınlık 5,23 — yatak Ø197 × 22,27 olunca büyüdü ve İNCELDİ (aralık 2–14)"')

# ---------------- APRON: Ø197 yatagin etrafini acmali (eskiden Ø160'a gore kesilmisti)
eski = """    ekle("siyirici_apron", ap, "sac","""
yeni = """    ap = ap.cut(sily(Xc, ZT, 101.0, 40.0, 95.0))      # v16: Ø197 yatak + 2 mm bosluk
    ekle("siyirici_apron", ap, "sac","""
assert eski in s
s = s.replace(eski, yeni, 1)

# ---------------- HOME SENSORU: yatak buyudu, sensor disari kayiyor (r 97 -> 115)
s = s.replace("sily(Xc, ZT - 97.0, 4.0, 66.5, 76.5)", "sily(Xc, ZT - 128.0, 4.0, 66.5, 76.5)")
s = s.replace("sily(Xc, ZT - 97.0, 10.0, 78.5, 81.5)", "sily(Xc, ZT - 128.0, 10.0, 86.0, 89.0)")
s = s.replace("ayar bileziğine r = 90'da kaynaklı", "ayar bileziğine r = 128'de kaynaklı (yatak Ø197 olunca dışarı kaydı)")

io.open(os.path.join(U, "topping_cad_v16.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v16.py yazildi")
