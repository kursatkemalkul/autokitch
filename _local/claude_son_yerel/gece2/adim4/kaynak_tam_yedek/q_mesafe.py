import sys, os, io, json
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
DD = sys.argv[1]; adlar = sys.argv[2:]
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep")); it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
D = {"%s|%s" % (i[0], i[1]): s for i, s in zip(idx, ch)}
for a in adlar:
    m = [k for k in D if k.endswith(a)]
    print(a, "->", m[:3])
ks = [[k for k in D if k.endswith(a)][0] for a in adlar]
s1, s2 = D[ks[0]], D[ks[1]]
d = BRepExtrema_DistShapeShape(s1.wrapped, s2.wrapped); print("mesafe", d.Value())
b = s2.BoundingBox(); print("kablo bbox", b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
b = s1.BoundingBox(); print("cihaz bbox", b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
sys.stdout.flush(); os._exit(0)
