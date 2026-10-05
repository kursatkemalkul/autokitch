import sys, os, io, json
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]; on = tuple(sys.argv[2].split(","))
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
for (b, a, m, g), s in zip(idx, ch):
    if b.startswith(on):
        bb = s.BoundingBox(); print(b, a, [round(v) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)])
sys.stdout.flush(); os._exit(0)
