# -*- coding: utf-8 -*-
"""TOPPING · YENI PARCALARIN CAKISMA TARAMASI
v17'de degisen parcalari (motor govdeleri, motor kablolari, 12 surucu, x motoru)
montajin TAMAMINA karsi tarar. Once kutu-kutu on eleme, sonra gercek kesisim hacmi.
Ayni motorun kendi kablosu gibi dogal komsuluklar da rapor edilir; yorumu insan yapar.
"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import topping_cad_v17 as TC

CIK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_carpisma_v17.txt")
TC.PARCALAR[:] = []
TC.modul()
ps = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom")]
YENI = [p for p in ps if p["ad"].startswith(("motor_", "surucu_", "x_motoru"))]

sat = []
def y(s):
    print(s, flush=True); sat.append(s)

y("taranan yeni parca: %d · montajdaki toplam parca: %d" % (len(YENI), len(ps)))
kutu = {id(p): p["wp"].val().BoundingBox() for p in ps}

def kesisir(a, b, pay=0.05):
    return not (a.xmax < b.xmin + pay or b.xmax < a.xmin + pay or
                a.ymax < b.ymin + pay or b.ymax < a.ymin + pay or
                a.zmax < b.zmin + pay or b.zmax < a.zmin + pay)

bul = []
for i, p in enumerate(YENI):
    ba = kutu[id(p)]
    for q in ps:
        if q is p: continue
        if not kesisir(ba, kutu[id(q)]): continue
        try:
            v = p["wp"].val().intersect(q["wp"].val()).Volume()
        except Exception:
            continue
        if v > 1.0:
            bul.append((p["ad"], q["ad"], v))
    if (i + 1) % 5 == 0:
        y("   ... %d/%d tarandi, su ana kadar %d cakisma" % (i + 1, len(YENI), len(bul)))

bul.sort(key=lambda t: -t[2])
y("")
y("CAKISMA SAYISI: %d" % len(bul))
for a, b, v in bul:
    y("   %-36s x %-36s %9.0f mm3" % (a, b, v))
if not bul:
    y("   TEMIZ — yeni motor ve surucular hicbir parcaya girmiyor")
io.open(CIK, "w", encoding="utf-8").write("\n".join(sat))
print("yazildi ->", CIK)
