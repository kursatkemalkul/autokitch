# -*- coding: utf-8 -*-
"""kutu_cad_v8 · KAPAK KOLU ↔ KAPAK MASASI denetimi: masa tek parça mı, kol bütün çevrim boyunca (β(t), 0,02 s adım) masaya değiyor mu, en yakın mesafe."""
import sys, os, math, time
import cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kutu_cad_v8 as KC

t0 = time.time()
KC.PARCALAR[:] = []
KC.kapak_mekanizmasi()
P = {p["ad"]: p for p in KC.PARCALAR}
kol = P["kapak_kolu"]["wp"].val()
_lv = [P["kapak_masasi_%d" % i]["wp"].val() for i in (0, 1)]
for i, l_ in enumerate(_lv):
    b_ = l_.BoundingBox()
    print("kapak_masasi_%d: %d gövde · %.1f × %.1f × %.1f · z %.1f…%.1f" % (i, len(l_.Solids()), b_.xlen, b_.ylen, b_.zlen, b_.zmin, b_.zmax))
    assert len(l_.Solids()) == 1, "levha tek parça değil"
masa = cq.Compound.makeCompound(_lv)
px, py = KC.KOL_P
T_SON = max(KC.Z_KOL_DON) + 0.5
en_yakin, en_t, kesisim = 1e9, None, []
t = 0.0
betalar = []
while t <= T_SON:
    b = KC.kol_beta(t); betalar.append(b)
    k_ = kol.rotate(cq.Vector(px, py, 0), cq.Vector(px, py, 1), b)
    d = k_.distance(masa)
    if d < en_yakin: en_yakin, en_t = d, (t, b)
    if d < 1e-6:
        v = k_.intersect(masa).Volume()
        if v > 1e-3: kesisim.append((round(t, 2), round(b, 1), round(v, 2)))
    t += 0.02
print("kol β aralığı %.1f…%.1f° · %d konum · en yakın kol ↔ masa %.2f mm (t %.2f s, β %.1f°) · kesişim %d" % (min(betalar), max(betalar), len(betalar), en_yakin, en_t[0], en_t[1], len(kesisim)))
assert not kesisim, kesisim
print("GEÇTİ · %.0f sn" % (time.time() - t0))
