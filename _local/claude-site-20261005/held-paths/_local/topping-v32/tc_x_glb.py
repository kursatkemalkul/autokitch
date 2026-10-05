# -*- coding: utf-8 -*-
"""TOPPING X ekseni bölgesini (tekne + kirişler + raylar + örtü + araba + tabla) ayrı GLB'ye yazar: python tc_x_glb.py <modul> <cikti.glb>"""
import sys, os, importlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "b89", "arastirma", "_uretec"))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b89", "arastirma", "_uretec"))
import cadquery as cq
T = importlib.import_module(sys.argv[1]); T.PARCALAR[:] = []; T.modul()
OUT = sys.argv[2]
KES = float(sys.argv[3]) if len(sys.argv) > 3 else None          # x kesiti: yalnız x >= KES kalır
RENK = dict(celik=(0.62, 0.64, 0.68), sac=(0.80, 0.82, 0.85), koyu=(0.16, 0.16, 0.18), motor=(0.22, 0.22, 0.25), pom=(0.93, 0.93, 0.90), silikon=(0.25, 0.5, 0.85), pu=(0.9, 0.85, 0.7))
asm = cq.Assembly(name="x")
n = 0
for p in T.PARCALAR:
    a = p["ad"]
    if a.startswith("_bom") or T.eski(a): continue
    if a.startswith(("acici_", "onyuz_", "dis_", "st_", "bant", "kaide", "yukleme")): continue
    sh = p["wp"].val(); b = sh.BoundingBox()
    if b.ymin > 115 or b.zmin < -430 or b.zmax > 10 or b.xmin < -620 or b.xmax > 1810: continue
    if b.ymax > 300: continue
    if KES is not None:
        if b.xmax <= KES: continue
        if b.xmin < KES:
            try: sh = sh.intersect(cq.Workplane("XY").box(3000, 400, 600, centered=False).translate((KES, -50, -500)).val())
            except Exception: continue
            if sh.Volume() < 1e-3: continue
    r = RENK.get(p["mal"], (0.7, 0.7, 0.7))
    if a.startswith("ray_ortu"): r = (0.95, 0.58, 0.20)                        # anlatım rengi: ray örtüsü / çatısı turuncu
    elif a.endswith("_ayagi"): r = (0.22, 0.52, 0.86)                          # kızak ayağı mavi
    elif a.startswith("kizak_blogu"): r = (0.25, 0.26, 0.28)                   # blok koyu
    elif a.startswith("lineer_ray") and not a.endswith("civatalari"): r = (0.55, 0.57, 0.60)
    asm.add(sh, name="%s__%s" % (a, p["mal"]), color=cq.Color(*r, 1.0)); n += 1
asm.save(OUT, exportType="GLTF", tolerance=0.05, angularTolerance=0.2)
print("ok", n, OUT)
sys.stdout.flush(); os._exit(0)
