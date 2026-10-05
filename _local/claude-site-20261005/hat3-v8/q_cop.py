import sys, os
sys.path.insert(0, os.getcwd())
import store_cad_v14 as S
S.modul()
print("KLAPE_AC", S.KLAPE_AC)
for p in S.PARCALAR:
    if p["birim"] == "B_COP":
        b = p["wp"].val().BoundingBox() if hasattr(p["wp"], "val") else p["wp"].BoundingBox()
        print("%-40s %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f %s" % (p["ad"], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p.get("grup")))
