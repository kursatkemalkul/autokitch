# -*- coding: utf-8 -*-
"""v18 flipper ↔ K2 fitil çakışmasının yeri (geçici ölçüm, üretime girmez)"""
import sys, io, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ad = sys.argv[1] if len(sys.argv) > 1 else "topping_uno_cad_v18.py"
sp = importlib.util.spec_from_file_location("TUx", ad); TU = importlib.util.module_from_spec(sp)
try:
    sp.loader.exec_module(TU)
except AssertionError:
    pass
P = {p["ad"]: p["sh"] for p in TU.P}
fl = P["onyuz_flipper_on_sac"]; ft = P["onyuz_K2_fitil"]
print("flipper on sac bb", fl.BoundingBox().xmin + 700, fl.BoundingBox().xmax + 700, fl.BoundingBox().ymin, fl.BoundingBox().ymax, fl.BoundingBox().zmin, fl.BoundingBox().zmax)
for aci in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0):
    m = TU.flipper_don(fl, aci)
    k = m.intersect(ft)
    v = k.Volume()
    if v > 1e-6:
        b = k.BoundingBox()
        print("aci %.2f · hacim %.2f · x %.1f–%.1f (dünya) · y %.1f–%.1f · z %.2f…%.2f" % (aci, v, b.xmin + 700, b.xmax + 700, b.ymin, b.ymax, b.zmin, b.zmax))
    else:
        print("aci %.2f · temiz" % aci)
