# -*- coding: utf-8 -*-
"""python yakin_sorgu.py <_dunya_tam> <cihaz alt dizgesi> ... : cihaza en yakın ELK parçaları + aynı birimde değen parçalar"""
import sys, os, io, json
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More():
    ch.append(cq.Shape.cast(it.Value())); it.Next()
L = [("%s|%s" % (i[0], i[1]), i[0], s) for i, s in zip(idx, ch)]


def d(a, b):
    x = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped)
    return x.Value() if x.IsDone() else 1e9


for q in sys.argv[2:]:
    for a, b, s in L:
        if not a.endswith("|" + q): continue
        bb = s.BoundingBox(); print("==", a, [round(v, 1) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)])
        c = s.Center()
        ad = []
        for a2, b2, s2 in L:
            if a2 == a: continue
            b2b = s2.BoundingBox()
            if b2b.xmin > bb.xmax + 40 or bb.xmin > b2b.xmax + 40 or b2b.ymin > bb.ymax + 40 or bb.ymin > b2b.ymax + 40 or b2b.zmin > bb.zmax + 40 or bb.zmin > b2b.zmax + 40: continue
            ad.append((d(s, s2), a2))
        for v, a2 in sorted(ad)[:10]: print("   %8.2f  %s" % (v, a2))
sys.stdout.flush(); os._exit(0)
