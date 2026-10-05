import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
for ad, s, b in EO.dokum():
    if ad == "TOPPING_MODUL|enerji_zinciri_kanali":
        sl = s.intersect(EO.kut(2459, 2460, 880, 960, -480, -410))
        rows = []
        for y in range(894, 954, 3):
            row = ""
            for z in range(-475, -414, 2):
                v = sl.intersect(EO.kut(2459, 2460, y, y + 1, z, z + 1)).Volume()
                row += "#" if v > 0.3 else "."
            rows.append("%4d %s" % (y, row))
        print("z -475 ... -415 (2 mm)"); print("\n".join(rows[::-1]))
sys.stdout.flush(); os._exit(0)
