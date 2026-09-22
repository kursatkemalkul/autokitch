# -*- coding: utf-8 -*-
"""topping_cad_v11 -> v12 : HIWIN'IN GERCEK CAD'I MONTAJA GIRIYOR

Kemal: "indir montaja ekle, once sunu bir yap."

TraceParts'tan inen HIWIN HGH15CA STEP'i (arastirma/katalog/step/hgh15ca.stp) iki kati
tasiyor ve ikisi de katalogla dogrulandi:
   kati 0 = ARABA  34,00 x 23,70 x 61,40 mm
   kati 1 = RAY    15,00 x 15,00 mm kesit · 150 mm ornek · 27.449 mm3 -> 1,45 kg/m
            (katalogdaki ray agirligiyla BIREBIR — profil gercek)

DEGISEN:
  kizak_blogu_0..3  uydurma kutu  ->  HIWIN'in GERCEK araba katisi
  lineer_ray_on/arka uydurma kutu ->  HIWIN'in GERCEK ray KESITI, 1600 mm'ye uzatilmis
                                      + katalog delik deseni (Ø4,5 gecme · Ø7,5x5,3 havsa
                                      · hatve 60 · uctan 20) — M4x16 civata tutar.

EKSEN CEVIRME: STEP'te ray Z boyunca uzuyor, bizim modelde X boyunca. Y ekseni etrafinda
90 derece cevriliyor: (x,y,z) -> (z, y, -x). Ray tabani STEP'te y=-15, bizde y=20,5 -> dy=35,5.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v11.py"), encoding="utf-8").read()

# ---------------------------------------------------------------- 1) STEP yukleyici
anc = "def ekle(ad, wp, mal, bom=None):"
yeni = '''# ======================= HIWIN GERCEK CAD (TraceParts STEP AP214) =======================
KATALOG_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "hgh15ca.stp")
_HIWIN = {}


def hiwin():
    """HGH15CA STEP'ini bir kez yukler: araba katisi + ray kesiti.
    STEP'te ray Z'de uzuyor; bizim modelde X'te. Y ekseni etrafinda 90 derece ceviriyoruz."""
    if _HIWIN: return _HIWIN
    w = cq.importers.importStep(KATALOG_STEP)
    sol = sorted(w.val().Solids(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    araba = next(s_ for s_ in sol if abs(s_.BoundingBox().zlen - 61.4) < 1.0)
    ray = next(s_ for s_ in sol if abs(s_.BoundingBox().zlen - 150.0) < 1.0)
    DY = 35.5                                                   # STEP ray tabani -15 -> modelde 20,5
    _HIWIN["araba"] = araba.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0).translate(cq.Vector(0, DY, 0))
    _HIWIN["ray_ornek"] = ray.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0).translate(cq.Vector(0, DY, 0))
    return _HIWIN


def hiwin_ray(x0, x1, zc):
    """HIWIN ray KESITINI x0..x1 arasina uzatir + katalog delik desenini acar.
    Katalog (Linear_Guideway-E-1.pdf s.41): WR15 HR15 · gecme d4,5 · havsa D7,5 h5,3
    · hatve P60 · uctan E20 · civata M4x16."""
    orn = hiwin()["ray_ornek"]
    # Ornek ray 150 mm; kesitini alip X boyunca 1600 mm'ye uzatiyoruz. Delik olmayan bir
    # yerden kesiyoruz (delikler uctan 20, hatve 60 -> x=0 ortada, delik yok).
    # Kesit supurme denendi, profilin yalniz bir yuzunu aldi (ray 5,5 mm cikti, 15 olmali).
    # Ornek rayin DELIGI YOK (27.449 mm3 / 150 mm = 183 mm2 profil alani, tam katalog
    # agirligini veriyor). O yuzden 150 mm'lik ornegi uc uca EKLIYORUZ, boya kesiyoruz,
    # sonra KATALOG delik desenini kendimiz aciyoruz.
    boy = x1 - x0
    n_kopya = int(boy // 150.0) + 1
    r = orn.translate(cq.Vector(75.0, 0.0, 0.0))
    for i in range(1, n_kopya):
        r = r.fuse(orn.translate(cq.Vector(75.0 + i * 150.0, 0.0, 0.0)))
    r = r.intersect(cq.Workplane("XY").box(boy, 60.0, 60.0, centered=(False, True, True))
                    .translate(cq.Vector(0.0, 28.0, 0.0)).val())
    r = r.translate(cq.Vector(x0, 0.0, zc))
    w = cq.Workplane(obj=r)
    n = int((x1 - x0 - 40.0) // 60.0) + 1
    for i in range(n):
        xd = x0 + 20.0 + i * 60.0
        if xd > x1 - 20.0: break
        w = w.cut(sily(xd, zc, 2.25, 20.0, 36.0))               # Ø4,5 gecme
        w = w.cut(sily(xd, zc, 3.75, 30.2, 36.0))               # Ø7,5 x 5,3 havsa (ust 35,5)
    return w, n


'''
assert anc in s
s = s.replace(anc, yeni + anc, 1)

# ---------------------------------------------------------------- 2) RAY: gercek kesit
eski = '''        ekle("lineer_ray_%s" % ad_, kut(65.0, 1665.0, 20.5, 35.5, zc_ - 7.5, zc_ + 7.5), "celik",'''
yeni = '''        _r, _n = hiwin_ray(65.0, 1665.0, zc_)
        ekle("lineer_ray_%s" % ad_, _r, "celik",'''
assert eski in s
s = s.replace(eski, yeni, 1)
s = s.replace('"M4 havşa hatve 60, ray başına 27 delik; ayar puluyla 0,05 mm\'ye paralellenir"',
              '"HIWIN HGR15 GERÇEK profil (TraceParts STEP) · M4 havşa hatve 60 · 1,45 kg/m katalogla birebir"')

# ---------------------------------------------------------------- 3) ARABA: gercek kati
eski = '''        ekle("kizak_blogu_%d" % i_, kut(xb - 17.0, xb + 17.0, 20.5, 48.5, zc_ - 30.7, zc_ + 30.7)
             .cut(kut(xb - 18.0, xb + 18.0, 20.0, 35.7, zc_ - 7.7, zc_ + 7.7)), "celik",'''
yeni = '''        ekle("kizak_blogu_%d" % i_,
             cq.Workplane(obj=hiwin()["araba"].translate(cq.Vector(xb, 0.0, zc_))), "celik",'''
assert eski in s
s = s.replace(eski, yeni, 1)
s = s.replace('"paslanmaz · NSF H1 gıda gresi", "hatve 200 mm; araba plakası bunların üstüne 16 × M4 ile bağlanır"',
              '"HIWIN HGH15CA GERÇEK CAD (TraceParts) · 0,18 kg · C 14,7 kN / C0 23,47 kN", "hatve 200 mm; araba plakası 4 × M4×5 dişle bağlanır (katalog B26 × C26)"')

io.open(os.path.join(U, "topping_cad_v12.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v12.py yazildi")
