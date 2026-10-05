# ön yüz (z>0 bölgesine uzanan) çubuk/dikme/kayıt adaylarının temas sayısı (BRepExtrema ≤ 0,5 mm)
import sys, os, io, json, time, re
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
DD = sys.argv[1]; OUT = sys.argv[2]
t0 = time.time()
idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
it = TopoDS_Iterator(sh.wrapped); ch = []
while it.More(): ch.append(cq.Shape.cast(it.Value())); it.Next()
BB = [s.BoundingBox() for s in ch]
TOL = 0.5
AD = re.compile(r"dikme|cubuk|çubuk|kayit|kusak|lama|profil|cerceve|mil|omega|kosebent|kosebend|lento|kiris|ray|direk|boru|tutucu|braket|cita|seri", re.I)
aday = []
for i, ((b, a, m, g), bb) in enumerate(zip(idx, BB)):
    if b.startswith(("INSAN", "CEK_", "URUN")): continue
    if bb.zmax < 0.0: continue
    d = sorted([bb.xlen, bb.ylen, bb.zlen])
    uzun = d[2] > 5.0 * max(d[1], 1.0)
    if uzun or AD.search(a):
        aday.append(i)
print("aday", len(aday)); sys.stdout.flush()
res = []
for i in aday:
    bi = BB[i]; kom = []
    for j in range(len(ch)):
        if j == i: continue
        bj = BB[j]
        if bj.xmin > bi.xmax + TOL or bi.xmin > bj.xmax + TOL or bj.ymin > bi.ymax + TOL or bi.ymin > bj.ymax + TOL or bj.zmin > bi.zmax + TOL or bi.zmin > bj.zmax + TOL:
            continue
        try:
            dd = BRepExtrema_DistShapeShape(ch[i].wrapped, ch[j].wrapped); ok = dd.IsDone() and dd.Value() <= TOL
            nsol = dd.NbSolution() if ok else 0
        except Exception:
            ok = True; nsol = -1
        if ok: kom.append((idx[j][0] + "|" + idx[j][1], nsol))
    b, a, m, g = idx[i]
    res.append(dict(ad=b + "|" + a, mal=m, grup=g, bb=[round(v, 1) for v in (bi.xmin, bi.xmax, bi.ymin, bi.ymax, bi.zmin, bi.zmax)], kom=kom))
json.dump(res, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("bitti %.0f sn" % (time.time() - t0))
for r in res:
    if len(r["kom"]) <= 1:
        print("AZ_TEMAS", r["ad"], r["mal"], r["bb"], r["kom"])
sys.stdout.flush(); os._exit(0)
