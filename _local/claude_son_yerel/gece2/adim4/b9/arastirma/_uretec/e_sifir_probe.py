# -*- coding: utf-8 -*-
"""E v12: 7 eksenin (4 köşe parmağı, köşe çerçevesi, ön dil, destek tablası) hareketli parçaları + komşuları — dünya sınır kutuları, t anlarında"""
import sys, json
import kutu_cad_v12 as K

K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
S = {n: p["wp"].val() for n, p in P.items()}
GRUPSUZ = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")


def dunya(t):
    W = K.blank_dunya(t)
    return {n: (W[P[n]["grup"]] if P[n]["grup"].startswith("B_") else K.grup_matrisi(P[n]["grup"], t)) for n in S if P[n]["grup"] not in GRUPSUZ}


def bb(n, M):
    b = K.uygula(S[n], M[n]).BoundingBox()
    return [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]


gruplar = {}
for n, p in P.items():
    gruplar.setdefault(p["grup"], []).append(n)
print("GRUPLAR:", {g: len(v) for g, v in sorted(gruplar.items())})
ilgili = [g for g in gruplar if g.startswith("CNR") or g in ("PISTON", "FRONT_Y", "PARMAK", "NEST")]
anlar = [float(a) for a in sys.argv[1:]] or [0.0]
for t in anlar:
    M = dunya(t)
    print("=== t = %.2f · kafa %.1f · köşe açısı %.1f · kaldırma %.1f · parmak %.1f · nest %.1f" % (t, K.kafa(t), K.corner_angle(t), K.corner_lift(t), K.parmak_psi(t), K.nest_dy(t)))
    for g in sorted(ilgili):
        for n in sorted(gruplar[g]):
            print("  %-10s %-44s %s" % (g, n, bb(n, M)))
