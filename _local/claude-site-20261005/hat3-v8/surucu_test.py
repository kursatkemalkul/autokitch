import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elektrik_v1 as E, h3_elk_rota as ER
from h3_elk_ortak import boru
E.yukle()
for p in E.PARCALAR:
    if not p["ad"].startswith("kablo_TOPPING_surucu_"): ER.ekli_ekle(p["ad"], E.dunya(p))
for i, (xs, xl, yj) in enumerate(((1482.0, 1522.0, 1500.0), (1515.0, 1531.0, 1490.0), (1548.0, 1540.0, 1490.0), (1581.0, 1549.0, 1500.0))):
    pts = [(xs, 1477.0, -730.0), (xs, yj, -730.0), (xl, yj, -730.0), (xl, yj, -812.0), (xl, 1879.8, -812.0)]
    print(i, ER.temiz(boru(pts, 4.45)))
sys.stdout.flush(); os._exit(0)
