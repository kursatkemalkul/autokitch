import sys, os
sys.path.insert(0, os.getcwd())
import kesme_cad_v11 as K
K.modul()
for p in K.PARCALAR:
    if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY"): continue
    s = p["wp"].val(); b = s.BoundingBox()
    if b.ymax > 892:
        print("%-44s %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f %s" % (p["ad"][:44], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p.get("grup", "")))
