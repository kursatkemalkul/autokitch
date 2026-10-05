import sys, os, math
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import cadquery as cq
import h3_elk_ortak as EO
pts = [(0,0,0),(0,0.3,0),(100,0.3,0),(100,50,0),(100,50,-40),(100.05,50,-40),(130,50,-40)]
for a, b in zip(pts[:-1], pts[1:]):
    c = EO.sil(a, b, 3.0); print("sil", round(math.dist(a, b), 2), round(c.Volume(), 1), c.isValid())
ss = [EO.sil(a, b, 3.0) for a, b in zip(pts[:-1], pts[1:])] + [cq.Solid.makeSphere(3.0, cq.Vector(*p), angleDegrees1=-90, angleDegrees2=90) for p in pts[1:-1]]
f = ss[0].fuse(*ss[1:]); print("fuse", round(f.Volume(), 1), f.isValid(), len(f.Solids()))
f2 = ss[0]
for q in ss[1:]: f2 = f2.fuse(q)
print("seq", round(f2.Volume(), 1), f2.isValid(), len(f2.Solids()))
sys.stdout.flush(); os._exit(0)
