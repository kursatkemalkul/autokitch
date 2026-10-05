"""verilen kutuya giren parçalar: python bolge_bos.py DD x0 x1 y0 y1 z0 z1"""
import sys, os, io, json
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]; q = [float(v) for v in sys.argv[2:8]]
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
K = cq.Solid.makeBox(q[1]-q[0], q[3]-q[2], q[5]-q[4], cq.Vector(q[0], q[2], q[4]))
for (b, a, m, g), s in zip(idx, ch):
    bb = s.BoundingBox()
    if bb.xmax < q[0] or bb.xmin > q[1] or bb.ymax < q[2] or bb.ymin > q[3] or bb.zmax < q[4] or bb.zmin > q[5]: continue
    try: v = s.intersect(K).Volume()
    except Exception: v = -1
    if abs(v) > 0.5: print("%-14s %-40s %8.0f mm3  %s" % (b, a, v, [round(t) for t in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]))
sys.stdout.flush(); os._exit(0)
