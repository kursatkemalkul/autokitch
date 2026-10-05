import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
x, y, z0, z1 = map(float, sys.argv[1:5])
q = EO.kut(x - 1, x + 1, y - 1, y + 1, z0, z1)
for ad, s, b in EO.dokum():
    if EO._ust((x - 1, x + 1, y - 1, y + 1, z0, z1), b):
        k = s.intersect(q)
        for so in k.Solids():
            bb = so.BoundingBox(); print("%-50s z %8.1f %8.1f" % (ad, bb.zmin, bb.zmax))
sys.stdout.flush(); os._exit(0)
