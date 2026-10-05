import io, time, hashlib
import cadquery as cq
from OCP.BRepTools import BRepTools
from OCP.BinTools import BinTools
s = cq.Solid.makeBox(10,20,30).fuse(cq.Solid.makeCylinder(3,50))
b = io.BytesIO(); s.exportBrep(b); print(len(b.getvalue()))
b2 = io.BytesIO(); BinTools.Write_s(s.wrapped, b2); print("bin", len(b2.getvalue()))
s.tessellate(0.1,0.2)
b3 = io.BytesIO(); s.exportBrep(b3); print("after mesh", len(b3.getvalue()))
r = cq.Shape.importBrep(io.BytesIO(b3.getvalue()))
print(r.BoundingBox().xmin, s.BoundingBox().xmin)
