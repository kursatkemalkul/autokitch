import sys, os, io, json, collections
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
DD = sys.argv[1]
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
grp = collections.defaultdict(list)
for (b, a, m, g), s in zip(idx, ch):
    bb = s.BoundingBox()
    if bb.xmin > 1430 and bb.xmax < 2505 and bb.zmax < -560 and bb.ymin > 1080 and bb.ymax < 2205 and not a.startswith(("dis_", "soguk_", "yalitim", "kabin")):
        k = a.split("_")[0] + "_" + (a.split("_")[1] if "_" in a else "")
        grp[(b, k)].append((bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
for (b, k), L in sorted(grp.items(), key=lambda t: min(v[2] for v in t[1])):
    x0 = min(v[0] for v in L); x1 = max(v[1] for v in L); y0 = min(v[2] for v in L); y1 = max(v[3] for v in L); z0 = min(v[4] for v in L); z1 = max(v[5] for v in L)
    print("%-13s %-28s n%-3d x %6.0f–%-6.0f y %6.0f–%-6.0f z %6.0f–%-6.0f" % (b[:13], k[:28], len(L), x0, x1, y0, y1, z0, z1))
sys.stdout.flush(); os._exit(0)
