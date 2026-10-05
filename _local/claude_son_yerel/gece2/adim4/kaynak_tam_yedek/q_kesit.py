import sys, re
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import cadquery as cq
import h3_elk_ortak as EO
pat, z = sys.argv[1], float(sys.argv[2])
for ad, s, b in EO.dokum():
    if re.search(pat, ad):
        sl = s.intersect(EO.kut(b[0]-1, b[1]+1, b[2]-1, b[3]+1, z, z + 1.0))
        for f in sl.Solids():
            bb = f.BoundingBox(); print(ad, "x %.1f %.1f y %.1f %.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax))
