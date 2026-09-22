# -*- coding: utf-8 -*-
"""topping_cad_v16 -> v17 : MOTOR DUZELTILDI + SURUCU GERCEK OLDU

Kemal: "bu arkadaki motorlar dogru mu, degilse dogrulariyla degistir."

1) MOTOR YANLISTI. STP-MTRAC-23078'i torkuna bakip secmistim; uretici sayfasinda
   "Optimized for AC-input stepper drives" yaziyor. Yani o motorun sürücüsü
   90-240 VAC girisli STP-DRVAC-24025. O surucunun GERCEK CAD'ini indirdim:
       141,2 x 47,5 x 113,7 mm
   Bizim elektrik bandindaki surucu yuvasi 34 x 75 x 95 mm. Hicbir yone donmuyor,
   12 tanesi de sigmiyor. Yani AC motorda israr edersek elektrik bandi buyuyecek.

   DOGRUSU: ayni NEMA23 govdesinin DC surumu.
       STP-MTR-23079 · DC · 2,8 A · 276 oz-in = 1,95 N·m tutma (ihtiyac 1,2 N·m)
   Govde STEP'te olculdu: 56,1 x 57 x 64,5 mm (eskisi 76 mm idi -> 11,5 mm KISALDI,
   kuru bolmedeki 1,5 mm'lik pay rahatladi). Mil 31,6 mm (eskisi 20) — reduktorun
   icine girdigi icin modelde kesiliyor.

2) SURUCU KUTUYDU, artik gercek: STP-DRV-4830 · 3 A/faz · 12-48 VDC · mikroadim.
   GERCEK CAD olculdu: 60,3 x 45,0 x 28,1 mm. 28 mm'lik yuzleri yan yana gelecek
   sekilde raya diziliyor: 12 x (28 + 5 hava) = 396 mm, elde 460 mm var. SIGIYOR.
   (Motor 2,8 A, surucu 3,0 A — pay %7, sinirda ama gecerli.)

KAYNAK: automationdirect.com urun sayfalari + ftp.automationdirect.com STEP AP214.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v16.py"), encoding="utf-8").read()

# ---------------- 1) MOTOR: AC surum -> DC surum
eski = '''MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtrac-23078.step")'''
yeni = '''MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtr-23079.step")'''
assert eski in s; s = s.replace(eski, yeni, 1)

eski = '''def nema23():
    """STP-MTRAC-23078 gercek katisi. STEP'te: govde z -76..0, mil z 0..+20, kablo +y.
    Bizim modelde motorun mil yuzu zm'de ve govde -z'ye dogru uzuyor — ayni yonelim."""
    if _MOT: return _MOT
    w = cq.importers.importStep(MOTOR_STEP)
    sol = w.val().Solids()
    govde = max(sol, key=lambda s_: s_.Volume())
    kablo = min(sol, key=lambda s_: s_.Volume())'''
yeni = '''def nema23():
    """STP-MTR-23079 gercek katisi (DC surum — v17'de AC surumden degistirildi).
    STEP'te: govde z -64,5..0, mil z 0..+31,6, kablo -y'de 333 mm uzuyor.
    Bizim modelde motorun mil yuzu zm'de ve govde -z'ye dogru uzuyor — ayni yonelim.
    STEP 17 kati tasiyor: govde + iki yatak gobegi + 4 baglama civatasi + kablo telleri."""
    if _MOT: return _MOT
    w = cq.importers.importStep(MOTOR_STEP)
    sol = w.val().Solids()
    # KABLO = motor zarfinin cok disina tasan katilar (teller). Govde = geri kalanin
    # hepsi (ana govde + civatalar + gobekler) — hepsi tek katiya kaynatiliyor.
    _kablolar = [x for x in sol if x.BoundingBox().ymin < -80.0]
    _govdeler = [x for x in sol if x.BoundingBox().ymin >= -80.0]
    govde = _govdeler[0]
    for x in _govdeler[1:]:
        govde = govde.fuse(x)
    kablo = _kablolar[0]
    for x in _kablolar[1:]:
        kablo = kablo.fuse(x)
    _KABLO_YON = -1.0      # yeni motorda kablo -y'ye uzuyor (eskisinde +y idi)'''
assert eski in s; s = s.replace(eski, yeni, 1)

# ---------------- 1b) KABLO GUDUGU: govdeye YAKIN 25 mm alinsin
eski = """    KAB = 25.0
    kb = kablo.BoundingBox()
    _MOT["kablo"] = kablo.intersect(cq.Workplane("XY").box(40, KAB, 40, centered=(True, False, True))
                                    .translate(cq.Vector(0, kb.ymin, (kb.zmin + kb.zmax) / 2)).val())"""
yeni = """    KAB = 25.0
    kb = kablo.BoundingBox()
    # v17 DUZELTME: eski motorda kablo +y'de idi, kb.ymin govdeye en yakin uctu.
    # Yeni motorda kablo -y'ye uzuyor; ayni satir kablonun UZAK ucundan 25 mm kesiyor,
    # gudukc motorun 300 mm otesinde havada kaliyordu (olculdu: y -32,8..-7,8).
    # Artik hangi yone giderse gitsin GOVDEYE YAKIN 25 mm aliniyor.
    _y0 = (kb.ymax - KAB) if kb.ymax <= 1.0 else kb.ymin
    _MOT["kablo"] = kablo.intersect(cq.Workplane("XY").box(40, KAB, 40, centered=(True, False, True))
                                    .translate(cq.Vector(0, _y0, (kb.zmin + kb.zmax) / 2)).val())"""
assert eski in s; s = s.replace(eski, yeni, 1)

# ---------------- 2) SURUCU: kutu -> gercek CAD
eski = '''    for i in range(12):
        xx = 605.0 + i * 38.0
        ekle("surucu_%d" % i, kut(xx, xx + 34.0, TEK[0] + 6.0, TEK[0] + 81.0, -45.0, -140.0), "kart",
             bom=("Step sürücü kartı", 12, "kapalı çevrim, 24 V", "her mile bir sürücü: 6 kaset × 2") if i == 0 else None)'''
yeni = '''    # v17: GERCEK SURUCU. STP-DRV-4830, TraceParts/AutomationDirect STEP AP214.
    # STEP kutusu X -34,8..25,5 · Y -18,5..26,5 · Z -14,1..14,0 (60,3 x 45,0 x 28,1).
    # Raya 28 mm'lik yuzleri yan yana dizilir; hatve 33 mm (28 govde + 5 hava).
    # Bizim eksenlerimiz: X = makine boyu, Y = yukseklik, Z = derinlik.
    # STEP'in 28'lik ekseni Z; onu X'e getirmek icin Y etrafinda 90 derece cevriliyor.
    _drv = cq.importers.importStep(SURUCU_STEP).val()
    _drv = _drv.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0)
    _db = _drv.BoundingBox()
    HATVE = 33.0
    for i in range(12):
        xx = 605.0 + i * HATVE
        # arka yuzu DIN rayin on yuzunde (z -140), oradan one dogru 60,3 mm uzar
        _d = _drv.translate(cq.Vector(xx - _db.xmin, (TEK[0] + 10.0) - _db.ymin, -140.0 - _db.zmin))
        ekle("surucu_%d" % i, cq.Workplane(obj=_d), "kart",
             bom=("Step sürücü · STP-DRV-4830", 12, "3 A/faz · 12-48 VDC · mikroadım · DIN ray",
                  "her mile bir sürücü: 6 kaset × 2; motor 2,8 A, sürücü 3,0 A (GERÇEK CAD)") if i == 0 else None)'''
assert eski in s; s = s.replace(eski, yeni, 1)

# surucu STEP yolu
s = s.replace('_MOT = {}', '''SURUCU_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-drv-4830.step")
_MOT = {}''', 1)

# ---------------- 3) BOM: motor parca numarasi
s = s.replace('"AutomationDirect STP-MTRAC-23078 · NEMA23 · 1,60 N·m tutma · 0,71 A · IP40 (GERÇEK CAD)"',
              '"AutomationDirect STP-MTR-23079 · NEMA23 · 1,95 N·m tutma · 2,8 A · DC · IP40 (GERÇEK CAD)"')
s = s.replace("Step motor NEMA23 · STP-MTRAC-23078", "Step motor NEMA23 · STP-MTR-23079")

io.open(os.path.join(U, "topping_cad_v17.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v17.py yazildi")
