# -*- coding: utf-8 -*-
"""motor ↔ adaptör flanşı kesişiminin yeri (yalnız inceleme)"""
import os, sys, math
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import cadquery as cq
import bantli_tabla_montaj_v1 as BT
kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
T = {p["ad"]: p["sh"] for p in BT.TAHRIK}
mb, yb = T["motor_kutusu"].BoundingBox(), T["tahrik_yatak_burcu"].BoundingBox()
xs, ys = (yb.xmin + yb.xmax) / 2.0, (yb.ymin + yb.ymax) / 2.0
mt = T["tahrik_motoru"]
def kes(z_):
    k_ = mt.intersect(kut(xs - 40.0, xs + 40.0, ys - 40.0, ys + 40.0, z_ - 0.005, z_ + 0.005).val())
    return k_.Volume() / 0.01
za, zb = mb.zmax - 12.0, mb.zmax
for i in range(24):
    zm = (za + zb) / 2.0
    if kes(zm) > 2000.0: za = zm
    else: zb = zm
print("yuz z %.4f" % zb)
for r in (19.15, 19.5, 20.0, 21.0):
    ad = kut(mb.xmin + 1.5, mb.xmax - 1.5, mb.ymin + 1.5, mb.ymax - 1.5, zb, mb.zmax).cut(silz(xs, ys, r, zb - 1.0, mb.zmax + 1.0)).val()
    k = mt.intersect(ad)
    v = k.Volume()
    print("r %.2f → kesişim %.3f mm³" % (r, v))
    for s in k.Solids():
        b = s.BoundingBox()
        print("   parça V %.3f x %.2f–%.2f y %.2f–%.2f z %.3f–%.3f (merkeze uzaklık %.2f)" % (s.Volume(), b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, math.hypot((b.xmin + b.xmax) / 2 - xs, (b.ymin + b.ymax) / 2 - ys)))
for dz in (0.0, 0.05, 0.1, 0.2):
    ad = kut(mb.xmin + 1.5, mb.xmax - 1.5, mb.ymin + 1.5, mb.ymax - 1.5, zb + dz, mb.zmax).cut(silz(xs, ys, 19.15, zb - 1.0, mb.zmax + 1.0)).val()
    print("dz %.2f → kesişim %.3f" % (dz, mt.intersect(ad).Volume()))
sys.stdout.flush(); os._exit(0)
