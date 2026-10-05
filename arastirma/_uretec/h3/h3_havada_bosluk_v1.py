# -*- coding: utf-8 -*-
"""havada_v1.json'daki her bileşenin en yakın ZEMİNE BAĞLI parçaya uzaklığı + en yakın noktalar (konsol / yaslama kararı için)."""
import io, json, os, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import h3_havada_v1 as HV

L = HV.yukle()
ad = {"%s|%s" % (b, a): s for b, a, m, g, s in L}
H = json.load(io.open(os.path.join(HV.DD, "havada_v1.json"), encoding="utf-8"))
havada = set(u for b in H["bilesen"] for u in b["uye"])
bagli = [(k, s, s.BoundingBox()) for k, s in ad.items() if k not in havada]
out = []
for b in H["bilesen"]:
    for u in b["uye"]:
        s = ad[u]; bb = s.BoundingBox(); en = (1e9, None, None, None)
        for k, t, tb in bagli:
            if tb.xmin > bb.xmax + 60 or bb.xmin > tb.xmax + 60 or tb.ymin > bb.ymax + 60 or bb.ymin > tb.ymax + 60 or tb.zmin > bb.zmax + 60 or bb.zmin > tb.zmax + 60: continue
            d = BRepExtrema_DistShapeShape(s.wrapped, t.wrapped)
            if d.IsDone() and d.Value() < en[0]:
                p1, p2 = d.PointOnShape1(1), d.PointOnShape2(1)
                en = (d.Value(), k, (round(p1.X(), 1), round(p1.Y(), 1), round(p1.Z(), 1)), (round(p2.X(), 1), round(p2.Y(), 1), round(p2.Z(), 1)))
        out.append(dict(parca=u, bilesen=b["en"], mesafe=round(en[0], 2), en_yakin=en[1], p_parca=en[2], p_sabit=en[3]))
        if not u.startswith("QR_GOZLER|goz_") or u.startswith(("QR_GOZLER|goz_00_", "QR_GOZLER|goz_51_")):
            print("%-44s %7.2f mm → %-44s %s %s" % (u, en[0], en[1], en[2], en[3]))
json.dump(out, io.open(os.path.join(HV.DD, "havada_bosluk_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
sys.stdout.flush(); os._exit(0)
