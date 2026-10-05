# -*- coding: utf-8 -*-
"""K v8: bütün parçaların sınır kutuları (t 0) + grup — K v9 yerleşimi için"""
import kesme_cad_v8 as K

K.modul()
for p in K.PARCALAR:
    b = p["wp"].val().BoundingBox()
    print("%-12s %-44s %s" % (p["grup"], p["ad"][:44], [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
print("Z_GELIS", K.Z_GELIS, "Z_SPREY", K.Z_SPREY, "Z_KES", K.Z_KES, "Y_KAFA", K.Y_KAFA, "XC ZC", K.XC, K.ZC, "BANT", K.BANT, "PZ_H", K.PZ_H)
for t in (0.0, 0.3, 1.0, 2.3, 2.6, 4.0, 5.4, 6.6, 8.4):
    print("t %.1f" % t, K.state(t), K.urun_merkez(t))
