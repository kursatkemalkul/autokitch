# -*- coding: utf-8 -*-
# STORE kaset klapesi — 0..90 derece ACILMA YORUNGESI kontrolu (SolidWorks gerekmez).
# Mentese ekseni X boyunca (y = MENT_Y, z = MENT_Z). Klapenin her kosesi bu eksen etrafinda doner.
#   nokta (y,z) -> (dy,dz) = (y-MENT_Y, z-MENT_Z)
#   aci t:  dy' = dy*cos t - dz*sin t ,  dz' = dy*sin t + dz*cos t
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sw_store_v3 as S

MY, MZ = S.MENT_Y, S.MENT_Z
y0k = S.KLAPE_ORNEK[0][1]
H, B = S.KLAPE_H, S.BIND
CELL0 = S.CELL0

# klapenin y-z kesitindeki kose noktalari (alt_bind = 0, ust conta YOK)
KOSE = [("on yuz alt-ic",  y0k,        0.0),
        ("on yuz alt-dis", y0k,        40.0),
        ("on yuz ust-ic",  y0k+H+B,    0.0),
        ("on yuz ust-dis", y0k+H+B,    40.0),
        ("yan conta alt",  y0k,        S.CZ0),
        ("yan conta ust",  y0k+H,      S.CZ0)]

print("MENTESE  y=%.1f  z=%.1f   |  KLAPE  y %.1f..%.1f   H=%.1f" % (MY, MZ, y0k, y0k+H+B, H))
print()
ymin, ymax, zmin, zmax = 1e9, -1e9, 1e9, -1e9
for ad, y, z in KOSE:
    dy, dz = y-MY, z-MZ
    r = math.hypot(dy, dz)
    yy = [MY + dy*math.cos(math.radians(t)) - dz*math.sin(math.radians(t)) for t in range(0, 91)]
    zz = [MZ + dy*math.sin(math.radians(t)) + dz*math.cos(math.radians(t)) for t in range(0, 91)]
    print("  %-16s r=%6.1f | kapali (y%7.1f z%7.1f) -> acik (y%7.1f z%7.1f) | yol: y %7.1f..%7.1f"
          % (ad, r, y, z, yy[-1], zz[-1], min(yy), max(yy)))
    ymin, ymax = min(ymin, min(yy)), max(ymax, max(yy))
    zmin, zmax = min(zmin, min(zz)), max(zmax, max(zz))

print()
print("SUPURME ZARFI:  y %.1f .. %.1f   ·   z %.1f .. %.1f" % (ymin, ymax, zmin, zmax))
print()
# 1) TAM ACIK: klapenin ic yuzu hucre tabani ile ayni duzlemde mi?
ic_acik = MY + MZ
print("1) TAM ACIK ic yuz kotu : %.1f   ·  hucre tabani (CELL0): %.1f   -> %s"
      % (ic_acik, CELL0, "AYNI DUZLEM ✓" if abs(ic_acik-CELL0) < 0.01 else "FARK %.1f mm ✗" % (ic_acik-CELL0)))
# 2) supurme sirasinda ustteki cekmece on yuzune carpiyor mu?
ust = [ (t, x0, y0) for t, x0, y0 in S.ORNEK if x0 == S.XL ]
ust.sort(key=lambda e: e[2])
t, x0, y0 = ust[0]
alt_b = S.ALT_BIND.get(t, S.BIND)
ust_on_alt = y0 - alt_b
print("2) USTTEKI CEKMECE (%s) on yuz alti: %.1f   ·  klape supurme tepesi: %.1f   -> pay %.1f mm  %s"
      % (t, ust_on_alt, ymax, ust_on_alt-ymax, "✓" if ust_on_alt-ymax >= 3.0 else "✗ YETERSIZ"))
# 3) asagi dogru: plint / cerceve alt kenari
print("3) SUPURME EN ALT KOT   : %.1f   ·  on cerceve saci alti (MENT_Y): %.1f  -> %s"
      % (ymin, MY, "kabine girmiyor ✓" if ymin >= MY - 0.01 else "✗ kabine giriyor"))
# 4) kaset yolu: acik klapenin ustunde 15 mm'lik conta esigi var mi?
print("4) ACIK KLAPE UST YUZEYI: duz  (klapede ust/alt conta seridi YOK — ikisi de KABINDE sabit) ✓")
