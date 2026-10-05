import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elektrik_v1 as E, h3_elk_rota as ER
from h3_elk_ortak import boru, kut
E.yukle()
for p in E.PARCALAR:
    if not p["ad"].startswith(("kablo_TOPPING_surucu_",)): ER.ekli_ekle(p["ad"], E.dunya(p))
T = 1.5
kan = kut(1523.0, 1553.0, 1535.0, 1879.5, -816.0, -776.0).cut(kut(1524.5, 1551.5, 1534.0, 1880.5, -814.5, -777.5))
print("kanal", ER.temiz(kan))
ER.ekli_ekle("kanal_TOPPING_surucu_dikey", kan)
for i, (xs, yj, xd, zd) in enumerate(((1482.0, 1500.0, 1530.5, -806.0), (1515.0, 1490.0, 1545.5, -806.0), (1548.0, 1510.0, 1530.5, -786.0), (1581.0, 1520.0, 1545.5, -786.0))):
    sh = boru([(xs, 1477.0, -730.0), (xs, yj, -730.0), (xs, yj, zd), (xd, yj, zd), (xd, 1536.5, zd)], 4.45)
    print(i, ER.temiz(sh)); ER.ekli_ekle("kablo_%d" % i, sh)
sys.stdout.flush(); os._exit(0)
