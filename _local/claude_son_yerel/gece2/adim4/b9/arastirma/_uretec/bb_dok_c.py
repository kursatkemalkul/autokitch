# -*- coding: utf-8 -*-
"""C istasyonu (TC + TU) bütün parçaların DÜNYA kutuları → bb_dok_c.json (yalnız inceleme, model yazmaz)"""
import json, os, sys, time, importlib, importlib.util as ilu
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
import cadquery as cq
TC_AD = sys.argv[1] if len(sys.argv) > 1 else "topping_cad_v28"
TU_AD = sys.argv[2] if len(sys.argv) > 2 else "topping_uno_cad_v15.py"
CIKTI = sys.argv[3] if len(sys.argv) > 3 else "bb_dok_c.json"
t0 = time.time()
TC = importlib.import_module(TC_AD); TC.PARCALAR[:] = []; TC.modul()
sp = ilu.spec_from_file_location("TUx", os.path.join(U, TU_AD)); TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
L = []
for p in TC.PARCALAR:
    if p["ad"].startswith("_bom"): continue
    v = p["wp"].vals() if hasattr(p["wp"], "vals") else [p["wp"]]
    v = [o for o in v if isinstance(o, cq.Shape)]
    sh = v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    b = sh.BoundingBox()
    L.append(dict(k="TC", ad=p["ad"], eski=bool(TC.eski(p["ad"])), mal=p["mal"], bb=[b.xmin + 700, b.xmax + 700, b.ymin + 892, b.ymax + 892, b.zmin, b.zmax]))
for q in TU.P:
    b = q["sh"].BoundingBox()
    L.append(dict(k="TU", ad=q["ad"], eski=q["ad"].startswith(TC.V3_CIKAN), mal=q["mal"], bb=[b.xmin + 700, b.xmax + 700, b.ymin - 168, b.ymax - 168, b.zmin, b.zmax]))
json.dump(L, open(os.path.join(U, CIKTI), "w", encoding="utf-8"), ensure_ascii=False)
print("yazildi %d parca · %.0f sn" % (len(L), time.time() - t0)); sys.stdout.flush(); os._exit(0)
