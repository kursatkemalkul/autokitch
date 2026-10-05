import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import cadquery as cq
import h3_elk_ortak as EO, h3_elk_rota as ER
rk, d_ = EO.rakor((1700.0, 1109.0, -805.0), "y", 5.3, 1.5, yon="+", disli=8.0)
ER.ekli_ekle("rakor_G2", rk)
c = EO.sil((1700.0, 1087.0, -805.0), (1700.0, 1140.0, -805.0), 5.0)
for ad, s in ER._engeller((1694, 1706, 1087, 1140, -811, -799), ("TOPPING_MODUL|kuru_bolme_tabani",)):
    try: v = c.intersect(s).Volume()
    except Exception as e: v = -1
    print(ad, round(v, 2))
sys.stdout.flush(); os._exit(0)
