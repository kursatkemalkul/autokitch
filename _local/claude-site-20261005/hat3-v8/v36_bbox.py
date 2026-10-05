import sys, os, io, json, time
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]
t0 = time.time()
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
out = []
for (b, a, m, g), s in zip(idx, ch):
    bb = s.BoundingBox()
    out.append([b, a, m, g, [round(v, 1) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]])
json.dump(out, io.open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(len(out), time.time() - t0)
sys.stdout.flush(); os._exit(0)
