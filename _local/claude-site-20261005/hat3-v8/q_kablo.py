import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elektrik_v1 as EL
EL.yukle()
for p in EL.PARCALAR:
    if p["ad"] in ("kablo_K_urun_sensoru_durus_alici", "kablo_TOPPING_motor_kasar_rotor_surucu_2", "kablo_TOPPING_motor_kasar_helezon_surucu_3", "kablo_TOPPING_motor_sucuk_rotor_surucu_0"):
        s = EL.dunya(p); b = s.BoundingBox()
        print("%-45s solids %d vol %.0f  x %.1f %.1f y %.1f %.1f z %.1f %.1f" % (p["ad"], len(s.Solids()), s.Volume(), b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
sys.stdout.flush(); os._exit(0)
