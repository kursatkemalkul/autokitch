import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
for ad, s, b in EO.dokum():
    if ad == "TOPPING_MODUL|enerji_zinciri_kanali":
        k = s.intersect(EO.kut(2455, 2465, 880, 960, -500, -400))
        for so in k.Solids():
            bb = so.BoundingBox(); print("x %.1f %.1f y %.1f %.1f z %.1f %.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
        for f in k.Faces()[:0]: pass
sys.stdout.flush(); os._exit(0)
