import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elektrik_v1 as EL
EL.yukle()
import collections
c = collections.Counter()
for p in EL.PARCALAR:
    s = EL.dunya(p)
    if p["ad"].startswith("kablo_") and "kelepce" not in p["ad"]:
        n = len(s.Solids()); c[n] += 1
        if p["ad"] in ("kablo_K_EC5000_bant_motoru",) or n > 1:
            b = s.BoundingBox(); print("%-48s %s solids %d vol %.0f  x %.0f %.0f y %.0f %.0f z %.0f %.0f" % (p["ad"], type(s).__name__, n, s.Volume(), b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
print(c)
sys.stdout.flush(); os._exit(0)
