import sys, os, io, json, collections
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]; x0, x1, ymax = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
say = collections.defaultdict(list)
for (b, a, m, g), s in zip(idx, ch):
    bb = s.BoundingBox()
    if bb.xmax > x0 and bb.xmin < x1 and bb.ymin < ymax and bb.ymax > -1:
        say[b].append((a, [round(v) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]))
for b in sorted(say):
    print("==", b, len(say[b]))
    for a, k in say[b][:25]: print("   ", a, k)
sys.stdout.flush(); os._exit(0)
