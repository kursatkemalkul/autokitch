# -*- coding: utf-8 -*-
"""topping_cad_v12 -> v13 : GERCEK NEMA23 MOTOR MONTAJA GIRIYOR

TraceParts / AutomationDirect · STP-MTRAC-23078
  NEMA23 · 2 fazli bipolar · 227 oz-in = 1,60 N·m tutma torku · 0,71 A · 1,8 derece
  IP40 · 200 adim/tur
  STEP olculdu: govde 56,40 x 57,51 x 76 mm (z -76..0) · mil z 0..+20 · KABLO +y'de 76 mm

Bizim ihtiyac 1,2 N·m'di; 1,60 N·m secildi, %33 pay var.
(Not: 1,60 TUTMA torku. Gercek tork devirle duser; tork-devir egrisi datasheet'ten
alinip sime konacak. Simdiki sabit tork IYIMSER.)

DEGISEN:
  motor_<yuva>_helezon/rotor (12 adet)  uydurma kutu -> GERCEK motor katisi + KABLOSU
  x_motoru                               uydurma kutu -> ayni motor, Y ekseninde

KABLO — GERCEK BULGU: STEP'teki kablo +y'de DUZ 76 mm uzuyor. Tarama 4 carpisma buldu:
  3 yuvada alt motorun kablosu UST MOTORA giriyor (140'lik kasette miller arasi 104 mm,
  motor 57 -> aralik 47 mm, kablo 76 istiyor) + bir tanesi FANA giriyor.
  Kablo bukulebilir oldugu icin modelde 25 mm guduk birakildi, ama KISIT gercek:
  kablo motordan en cok ~40 mm sonra donmeli -> dirsek konnektor ya da hemen kanal.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v12.py"), encoding="utf-8").read()

anc = "def ekle(ad, wp, mal, bom=None):"
yeni = '''MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtrac-23078.step")
_MOT = {}


def nema23():
    """STP-MTRAC-23078 gercek katisi. STEP'te: govde z -76..0, mil z 0..+20, kablo +y.
    Bizim modelde motorun mil yuzu zm'de ve govde -z'ye dogru uzuyor — ayni yonelim."""
    if _MOT: return _MOT
    w = cq.importers.importStep(MOTOR_STEP)
    sol = w.val().Solids()
    govde = max(sol, key=lambda s_: s_.Volume())
    kablo = min(sol, key=lambda s_: s_.Volume())
    # mili kes: mil redüktörün icine girer, onu redüktör temsil ediyor
    kes = cq.Workplane("XY").box(200, 300, 100, centered=(True, True, False)).val()
    _MOT["govde"] = govde.cut(kes)
    # KABLO: STEP'te DUZ 76 mm uzuyor ve bu haliyle 140'lik kasetlerde ust motora carpiyor
    # (olculdu: 3 yuvada 1.406 mm3 + fan_0'da 1.885 mm3). Iki mil arasi 104 mm, motor 57 —
    # aralik 47 mm. Gercek kablo BUKULEBILIR; modelde 25 mm'lik cikis guduguyle temsil
    # ediliyor. TASARIM KISITI: kablo motordan en cok 40 mm sonra donmeli, yani duz uclu
    # fis degil, DIRSEK KONNEKTOR ya da hemen bukulen kablo kanali gerekiyor.
    KAB = 25.0
    kb = kablo.BoundingBox()
    _MOT["kablo"] = kablo.intersect(cq.Workplane("XY").box(40, KAB, 40, centered=(True, False, True))
                                    .translate(cq.Vector(0, kb.ymin, (kb.zmin + kb.zmax) / 2)).val())
    return _MOT


def nema23_koy(xm, yy, zm):
    """motorun MIL YUZU zm'de olacak sekilde yerlestirir (govde -z'ye uzar)"""
    m = nema23()
    v = cq.Vector(xm, yy, zm)
    return (cq.Workplane(obj=m["govde"].translate(v)), cq.Workplane(obj=m["kablo"].translate(v)))


'''
assert anc in s
s = s.replace(anc, yeni + anc, 1)

# ---- 12 tahrik motoru
eski = '''        ekle("motor_" + k, kut(xm - MO["g"] / 2, xm + MO["g"] / 2, yy - MO["y"] / 2, yy + MO["y"] / 2, zm, zm - MO["z"]), "motor", bom=None)'''
yeni = '''        _g, _kb = nema23_koy(xm, yy, zm)
        ekle("motor_" + k, _g, "motor", bom=None)
        ekle("motor_kablosu_" + k, _kb, "koyu", bom=None)'''
assert eski in s
s = s.replace(eski, yeni, 1)

# ---- X motoru (ekseni Y'de): Z ekseninden Y'ye cevir
eski = '''    ekle("x_motoru", kut(1706.5, 1763.5, 41.5, 117.5, -388.5, -331.5), "motor",'''
yeni = '''    _mg = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0).translate(cq.Vector(1735.0, 41.5, -360.0))
    ekle("x_motoru", cq.Workplane(obj=_mg), "motor",'''
assert eski in s
s = s.replace(eski, yeni, 1)

# ---- BOM: gercek parca numarasi
s = s.replace('"NEMA23 kapalı çevrim step 1,2 N·m"', '"AutomationDirect STP-MTRAC-23078 · NEMA23 · 1,60 N·m tutma · 0,71 A · IP40 (GERÇEK CAD)"')
for eski_b, yeni_b in (
    ("Step motor NEMA23", "Step motor NEMA23 · STP-MTRAC-23078"),
):
    s = s.replace(eski_b, yeni_b)

io.open(os.path.join(U, "topping_cad_v13.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v13.py yazildi")
