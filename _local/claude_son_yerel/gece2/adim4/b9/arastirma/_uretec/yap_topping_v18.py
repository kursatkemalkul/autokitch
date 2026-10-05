# -*- coding: utf-8 -*-
"""topping_cad_v17 -> v18 : GUC KAYNAGI ve UPS GERCEK CAD OLDU

1) GUC KAYNAGI  MEAN WELL NDR-240-24 (TraceParts STEP AP214)
   Neden 240 W: motor faz akimini 2,0 A varsaymistim; gercek motorun (STP-MTR-23079)
   uretici tablosunda 2,8 A. Kemal'in formuluyle 24 x 2,8 x 2 x 1,6 = 215 W -> bir ust
   standart boy 240 W. (topping_hesap_v5)
   GERCEK OLCU: 125,2 (yukseklik) x 63,0 (ray boyunca) x 122,8 (derinlik)
   Yer tutucu 160 x 100 x 100 idi; 122,8 derinlik 100'e sigmiyordu, yuva buyutuldu.
   Teknik bantta 250 mm derinlik var, X'te yer KAZANILDI (160 -> 63).

2) UPS  PULS UB10.242 · DIN ray UPS · 24 V (TraceParts STEP AP214)
   GERCEK BULGU: BOM'daki "500 VA hat ici UPS"in gercek karsiligi Eaton 5P650i;
   CAD'ini indirdim, 150 x 233 x 357 mm. Teknik bant 240 yuksek / 250 derin, X'te de
   UPS'e ayrilan yer 220 mm. UCUNCU EKSENDE DE SIGMIYOR — kule UPS bu module girmiyor.
   Isin gercegi zaten kule UPS gerekmiyordu: BOM'un kendi gerekcesi "elektrik
   kesintisinde kaset konumlari ve saat korunur", yani KONTROLCUYU ayakta tutmak.
   Onu DIN ray 24 V UPS yapar: UB10.242, 121,7 x 49,0 x 130,5 mm, raya oturur.
   Kule UPS'in STEP'i diskte duruyor (5p650i.stp); Kemal "kule olsun" derse yuva
   buyutulur ya da UPS modulun disina alinir.
   ACIK IS: UB10.242 KONTROL birimidir, yaninda AKU MODULU ister (PULS UZK sinifi,
   benzer boyda). Henuz modelde YOK.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v17.py"), encoding="utf-8").read()

# yeni STEP yollari
s = s.replace('SURUCU_STEP = os.path.join', '''GUC_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "ndr-240-24.stp")
UPS_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "ub10-242.stp")


def din_parca(yol, x0, y0, z0):
    """DIN ray cihazini STEP'ten alir ve bizim eksenlere oturtur.
    STEP'te: X = yukseklik, Y = ray boyunca genislik, Z = derinlik.
    Bizde:   X = makine boyu (ray yonu), Y = yukseklik, Z = derinlik.
    Z etrafinda 90 derece cevirince X<-genislik, Y<-yukseklik oluyor.
    x0,y0 = sol-alt kose; z0 = ON yuz (parca -z'ye, makinenin icine dogru uzar)."""
    sh = cq.importers.importStep(yol).val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0)
    b = sh.BoundingBox()
    return cq.Workplane(obj=sh.translate(cq.Vector(x0 - b.xmin, y0 - b.ymin, z0 - b.zmax)))


SURUCU_STEP = os.path.join''', 1)

# ---- GUC KAYNAGI
eski = '''    ekle("guc_kaynagi", kut(400.0, 560.0, TEK[0] + 6.0, TEK[0] + 106.0, -40.0, -140.0), "sac",
         bom=("Güç kaynağı 24 V %d W" % H.S["elektrik"]["guc_kaynagi_W"], 1, "DIN raya", "aynı anda en çok 2 mil döner"))'''
yeni = '''    ekle("guc_kaynagi", din_parca(GUC_STEP, 400.0, TEK[0] + 6.0, -40.0), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1,
              "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W" % H.S["elektrik"]["guc_kaynagi_W"]))'''
assert eski in s; s = s.replace(eski, yeni, 1)

# ---- UPS
eski = '''    ekle("ups", kut(1520.0, 1740.0, TEK[0] + 6.0, TEK[0] + 156.0, -40.0, -230.0), "koyu", bom=("UPS 500 VA", 1, "hat içi", "elektrik kesintisinde kaset konumları ve saat korunur"))'''
yeni = '''    # UPS artik DIN ray cihazi (kule UPS 150x233x357, teknik banda hicbir yone sigmiyor)
    ekle("ups", din_parca(UPS_STEP, 1520.0, TEK[0] + 6.0, -40.0), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1,
              "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur; kule UPS (Eaton 5P650i 150×233×357) bu modüle sığmıyor"))
    ekle("ups_rayi", kut(1500.0, 1680.0, TEK[0] + 26.0, TEK[0] + 41.0, -170.0, -177.0), "sac",
         bom=("DIN ray 35 mm · UPS", 1, "standart", "UPS ve akü modülü bu rayda"))'''
assert eski in s; s = s.replace(eski, yeni, 1)

# hesap v5'e gec
s = s.replace("import topping_hesap_v4 as H", "import topping_hesap_v5 as H")

io.open(os.path.join(U, "topping_cad_v18.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v18.py yazildi")
