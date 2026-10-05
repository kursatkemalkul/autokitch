import os, sys
sys.path.insert(0, os.getcwd())
import sucuk_cad_v8 as V
V.PARCALAR[:] = []; V.kap(); A = {p["ad"]: p["wp"].val() for p in V.PARCALAR}
for a, b in (("helezon_D", "cikis_tupu"), ("cikis_tupu", "yatak_kapagi")):
    k = A[a].intersect(A[b]); bb = k.BoundingBox()
    print(a, b, "hacim %.2f" % k.Volume(), "kutu x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax), "katı sayısı", len(k.Solids()))
    for s in k.Solids():
        b2 = s.BoundingBox(); print("   ", "%.2f" % s.Volume(), "x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f" % (b2.xmin, b2.xmax, b2.ymin, b2.ymax, b2.zmin, b2.zmax))
sys.stdout.flush(); os._exit(0)
