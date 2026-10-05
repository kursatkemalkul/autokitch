import sys, os, io, json, collections
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]; x0, x1 = float(sys.argv[2]), float(sys.argv[3]); y0 = float(sys.argv[4]) if len(sys.argv) > 4 else 788.0
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
say = collections.defaultdict(list)
for (b, a, m, g), s in zip(idx, ch):
    bb = s.BoundingBox()
    if bb.xmin >= x0 - 1 and bb.xmax <= x1 + 1 and bb.ymax > y0:
        say[b].append((a, [round(v) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)], g))
for b in sorted(say):
    print("==", b, len(say[b]))
    for a, k, g in (say[b] if len(sys.argv) <= 5 else [q for q in say[b] if sys.argv[5] in q[0] or sys.argv[5] in b]): print("   ", a, k, g)
sys.stdout.flush(); os._exit(0)
