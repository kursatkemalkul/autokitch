import sys, os
sys.path.insert(0, os.getcwd())
import kutu_cad_v14 as E
if not E.PARCALAR: E.modul()
for p in E.PARCALAR:
    w = p["wp"]; s = w.val() if hasattr(w, "val") else w
    b = s.BoundingBox()
    if b.ymin < 790:
        print("%-44s %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f %s" % (p["ad"][:44], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p.get("grup", "")))
