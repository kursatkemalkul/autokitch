import io, time, weakref
import cadquery as cq
from OCP.BinTools import BinTools
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCP.BOPAlgo import BOPAlgo_GlueEnum
print([m for m in dir(BinTools) if not m.startswith('_')])
print(BinTools.Write_s.__doc__)
print(BinTools.Read_s.__doc__)
op = BRepAlgoAPI_Fuse()
print([m for m in dir(op) if any(k in m for k in ("Fuzzy","Glue","OBB","NonDestr","Parallel","Inverted","Geometry","Tolerance"))])
s = cq.Solid.makeBox(10,20,30); print(weakref.ref(s))
s2 = cq.Workplane().sphere(20).val()
b = io.BytesIO(); BinTools.Write_s(s2.wrapped, b); n0=len(b.getvalue()); s2.tessellate(0.1,0.1)
b = io.BytesIO(); BinTools.Write_s(s2.wrapped, b); print("bin before/after mesh", n0, len(b.getvalue()))
b = io.BytesIO(); BinTools.Write_s(s2.wrapped, b, False, False); print("explicit no tri", len(b.getvalue()))
