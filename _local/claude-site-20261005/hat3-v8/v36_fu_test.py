import sys, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"
sys.path[:0] = [H3, os.path.dirname(H3)]
os.chdir(H3)
import cadquery as cq
import h3_firin_ust_v1 as FU
FU.kur()
exec(open(sys.argv[1], encoding="utf-8").read())
yeni = [p for p in FU.PARCALAR if p["ad"].startswith("onyuz_f_ust_ust_kayit")]
for p in yeni:
    s = FU.dunya(p); b = s.BoundingBox(); print(p["ad"], [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)])
    for q in FU.PARCALAR:
        if q is p: continue
        t = FU.dunya(q)
        try:
            v = s.intersect(t).Volume()
        except Exception:
            v = -1
        if abs(v) > 0.01: print("   CAKISMA", q["ad"], round(v, 2))
kb = FU.dunya([q for q in FU.PARCALAR if q["ad"] == "f_ust_tavan_kirisi"][0]).BoundingBox()
print("kiris", [round(v, 1) for v in (kb.xmin, kb.xmax, kb.ymin, kb.ymax, kb.zmin, kb.zmax)])
sys.stdout.flush(); os._exit(0)
