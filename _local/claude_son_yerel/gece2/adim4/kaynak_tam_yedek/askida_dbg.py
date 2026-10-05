# -*- coding: utf-8 -*-
"""askıda kelepçe noktaları teşhisi: python askida_dbg.py (b3/arastirma/_uretec içinden)"""
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elektrik_v1 as E, h3_elk_rota as ER, h3_elk_ortak as EO
E.yukle()
for p in E.PARCALAR: ER.ekli_ekle(p["ad"], E.dunya(p))
TEST = [("x_home", (983.0, 902.0, -13.0), "x", 2.0)]
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import cadquery as cq
def yakin(p, ad_):
    for a, s, sb in EO.dokum():
        if a == ad_:
            d = BRepExtrema_DistShapeShape(cq.Vertex.makeVertex(*p).wrapped, s.wrapped)
            q = d.PointOnShape2(1); return d.Value(), (round(q.X(),2), round(q.Y(),2), round(q.Z(),2))
print("tekne en yakın:", yakin((983.0, 902.0, -13.0), "TOPPING_MODUL|mekanizma_teknesi"))
for e in E.PARCALAR:
    if e["ad"] == "kablo_K_EC5000_bant_motoru": print("EC5000 noktalar:", e.get("pts") or e.get("yol"))
import json
J = json.load(open("h3/_elk/elk.json", encoding="utf-8"))
print(type(J), list(J)[:5] if isinstance(J, dict) else J[0].keys() if J else None)
for nm, p, eks, r in TEST:
    print("==", nm, p)
    # EC5000 için kablo yolunu bul
    if eks is None:
        for q in E.PARCALAR:
            if q["ad"] == "kablo_K_EC5000_bant_motoru":
                b = E.dunya(q).BoundingBox(); print("   kablo kutusu", [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)])
        continue
    ax = "xyz".index(eks)
    for bx in [i for i in range(3) if i != ax]:
        for sg in (+1, -1):
            lo = [p[i] - r for i in range(3)]; hi = [p[i] + r for i in range(3)]
            if sg > 0: lo[bx], hi[bx] = p[bx] + r, p[bx] + 200
            else: lo[bx], hi[bx] = p[bx] - 200, p[bx] - r
            q = (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
            ad = [(a, s.BoundingBox()) for a, s in ER._engeller(q, ())]
            for a, b in ad[:6]:
                print("   %s%s  %s  %s" % ("+" if sg > 0 else "-", "xyz"[bx], a, [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
    y = ER.kelepce_yeri(p, eks, r)
    print("   kelepce_yeri:", y)
    if y:
        ks = EO.kelepce(p, eks, r, y[0], y[1]); print("   temiz:", ER.temiz(ks))
sys.stdout.flush(); os._exit(0)
