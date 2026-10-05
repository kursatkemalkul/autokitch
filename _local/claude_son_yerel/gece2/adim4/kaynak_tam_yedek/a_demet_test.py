import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elektrik_v1 as E, h3_elk_rota as ER, h3_elk_ortak as EO
from h3_elk_ortak import boru, rakor
E.yukle()
for p in E.PARCALAR:
    if not p["ad"].startswith("kablo_A_sensor_demeti"): ER.ekli_ekle(p["ad"], E.dunya(p))
pts = [(1420.0, 1610.3, -24.0), (1420.0, 1625.0, -24.0), (1410.0, 1625.0, -24.0), (1410.0, 1625.0, -680.0), (1410.0, 1520.0, -680.0), (1490.0, 1520.0, -680.0), (1490.0, 1870.0, -680.0), (1490.0, 1870.0, -715.0), (1490.0, 1879.8, -715.0)]
print("demet temiz mi:", ER.temiz(boru(pts, 6.5), ("TOPPING_MODUL|dis_yan_sol",)))
sys.stdout.flush(); os._exit(0)
