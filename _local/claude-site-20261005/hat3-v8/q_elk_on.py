import sys, os
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elektrik_v1 as EL
EL.yukle()
for p in EL.PARCALAR:
    b = EL.dunya(p).BoundingBox()
    if b.zmax > 79.5 and not p["birim"].startswith(("ELK_QR", "ELK_ANA_PANO")):
        print("%-14s %-40s x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f" % (p["birim"], p["ad"], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
sys.stdout.flush(); os._exit(0)
