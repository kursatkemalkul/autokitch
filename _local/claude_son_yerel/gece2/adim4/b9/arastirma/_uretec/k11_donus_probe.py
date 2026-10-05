# -*- coding: utf-8 -*-
"""K v11: dönüş hortumu ↔ KBP kesişiminin yeri"""
import kesme_cad_v11 as K
K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
a = P["yag_geri_basinc_regulatoru_KBP"]["wp"].val(); b = P["yag_donus_hortumu_TLM0806"]["wp"].val()
k = a.intersect(b)
bb = k.BoundingBox()
print("hacim %.2f · kesişim kutusu x %.2f-%.2f y %.2f-%.2f z %.2f-%.2f" % (k.Volume(), bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
print("KBP", [round(v, 2) for v in (a.BoundingBox().xmin, a.BoundingBox().xmax, a.BoundingBox().ymin, a.BoundingBox().ymax, a.BoundingBox().zmin, a.BoundingBox().zmax)])
print("donus", [round(v, 2) for v in (b.BoundingBox().xmin, b.BoundingBox().xmax, b.BoundingBox().ymin, b.BoundingBox().ymax, b.BoundingBox().zmin, b.BoundingBox().zmax)])
print("H_DONUS", K.H_DONUS)
import inspect
print(inspect.getsource(K.boru))
