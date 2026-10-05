# -*- coding: utf-8 -*-
"""sabit tahrik parçalarının z kesitleri (yalnız inceleme)"""
import os, sys
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import cadquery as cq
import bantli_tabla_montaj_v1 as BT
from OCP.BRepExtrema import BRepExtrema_DistShapeShape as DSS
T = {p["ad"]: p["sh"] for p in BT.TAHRIK}
for a, s in T.items():
    b = s.BoundingBox(); print("%-22s x %.2f–%.2f y %.2f–%.2f z %.2f–%.2f V %.0f" % (a, b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, s.Volume()))
m = T["tahrik_motoru"]; b = m.BoundingBox()
z = b.zmin + 0.25
son = None
while z < b.zmax:
    k = m.intersect(cq.Workplane("XY").box(200, 200, 0.1).translate((2465.8, 988.0, z)).val())
    bk = k.BoundingBox() if k.Volume() > 1e-6 else None
    tan = (round(bk.xlen, 1), round(bk.ylen, 1)) if bk else None
    if tan != son: print("  motor kesit z %.2f → %s" % (z, tan)); son = tan
    z += 1.0
for a in ("tahrik_kutusu", "tahrik_yatak_burcu", "kaplin", "tahrik_mili", "tahrik_rulmani_0", "tahrik_braketi", "motor_kutusu"):
    for c in ("tahrik_kutusu", "motor_kutusu", "tahrik_motoru", "tahrik_yatak_burcu", "tahrik_braketi", "kaplin", "tahrik_mili"):
        if a < c:
            d = DSS(T[a].wrapped, T[c].wrapped); print("  mesafe %-20s ↔ %-20s %.3f" % (a, c, d.Value() if d.IsDone() else -1))
sys.stdout.flush(); os._exit(0)
