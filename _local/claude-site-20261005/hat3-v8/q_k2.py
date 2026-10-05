import sys, os
sys.path.insert(0, os.getcwd())
import kesme_cad_v11 as K
K.modul()
import cadquery as cq
for p in K.PARCALAR:
    if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY"): continue
    b = p["wp"].val().BoundingBox()
    if b.ymax > 1460 and b.zmax > -700 and not p["ad"].startswith(("onyuz_", "kose_dik", "sol_sac", "sag_sac", "ust_sac")):
        print("Q %-44s %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f %s" % (p["ad"][:44], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p.get("grup", "")))
    if p["ad"].startswith(("yag_pompasi", "itici_", "eksen_")):
        print("Q %-44s %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f %s" % (p["ad"][:44], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p.get("grup", "")))
