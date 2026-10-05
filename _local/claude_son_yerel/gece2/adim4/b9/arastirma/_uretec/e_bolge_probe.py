# -*- coding: utf-8 -*-
"""E v12: verilen bölgelere (x0 x1 y0 y1 z0 z1) t anlarında giren parçalar (dünya sınır kutusu kesişimi)"""
import sys
import kutu_cad_v12 as K

K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
S = {n: p["wp"].val() for n, p in P.items()}
GRUPSUZ = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")
BOLGE = {
    "NEST_sensor": (395, 470, 800, 900, -240, -170),
    "LIFT_sensor": (440, 500, 1000, 1500, -240, -170),
    "LIFT_sensor_alt": (440, 500, 990, 1100, -240, -170),
}
ANLAR = [0.0, 2.0, 3.0, 3.35, 4.3, 5.0, 6.0, 7.5, 9.0, 9.3, 10.0, 12.0, 15.0, 18.0, 20.0, 22.0, 22.7, 23.0]


def dunya(t):
    W = K.blank_dunya(t)
    return {n: (W[P[n]["grup"]] if P[n]["grup"].startswith("B_") else K.grup_matrisi(P[n]["grup"], t)) for n in S if P[n]["grup"] not in GRUPSUZ}


bulunan = {}
for t in ANLAR:
    M = dunya(t)
    for n in M:
        b = K.uygula(S[n], M[n]).BoundingBox()
        for ad, (x0, x1, y0, y1, z0, z1) in BOLGE.items():
            if b.xmax > x0 and b.xmin < x1 and b.ymax > y0 and b.ymin < y1 and b.zmax > z0 and b.zmin < z1:
                bulunan.setdefault((ad, n), []).append((t, [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
for (ad, n), v in sorted(bulunan.items()):
    print("%-16s %-10s %-40s ilk t %.2f %s · %d an" % (ad, P[n]["grup"], n, v[0][0], v[0][1], len(v)))
print("DONGU", K.DONGU, "Z_ZIMBA", K.Z_ZIMBA, "kafa alt", min(K.kafa(i / 20.0) for i in range(int(K.DONGU * 20))))
