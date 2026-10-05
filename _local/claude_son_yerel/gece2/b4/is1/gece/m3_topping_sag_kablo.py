# -*- coding: utf-8 -*-
"""MADDE 3 (89.png) · TOPPING sag cep: "T" askilar = P-kelepceler (h3_elk_ist_v1 'kelepceler' otomatigi). Iki sensor kablosu
(x sag limit · tabla bos) birbirinden 4–6 mm ayrik, farkli kotlarda (y 1070 / 1076) ve x'te (2459 / 2455) gidiyordu; kelepceleri 30–36 mm
dikmeyle raf altina asili ya da contanin 3 mm ustunde havada duruyordu (5 adet).
YENI: iki kablo TEK DEMET — sag duvarin ic yuzune (x 2498,5) yaslanir, ust uste (tabla bos y 1070 · x limit y 1074,5 · eksen x 2494),
z boyunca dik ve hizali, arka uçta ayni z'de (−803) birlikte KD1 kanalinin sag yuzune (x 2449,2) girer.
Ortak kelepce: 1 mm paslanmaz U serit (12 mm genis) iki kabloyu birlikte sarar, iki kulakla duvara M4 vidali (z −60 · −300 · −540 · −770).
Eski 2 kablo + 5 kelepce silinir. Kablo ucları ayni cihaz noktalarindan baslar (x limit sensoru 2375/920/−18,7 · tabla bos 2360/1070/−170).
Kullanim: python m3_topping_sag_kablo.py giris.glb cikis.glb"""
import sys, numpy as np
import cadquery as cq
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\b4\is1\gece")
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import glbkit
import h3_elk_ortak as EO

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)
XC = 2494.0; Y_TB = 1070.0; Y_XL = 1074.5; ZK = -803.0; KD1X = 2449.2; R = 2.0


def sec(p, kutular):
    tl, kut = G.komp(p); s = []
    for (x0, x1, y0, y1, z0, z1) in kutular:
        s += [i for i, (a, b, n) in kut.items() if abs(a[0] - x0) < 0.6 and abs(b[0] - x1) < 0.6 and abs(a[1] - y0) < 0.6 and abs(b[1] - y1) < 0.6 and abs(a[2] - z0) < 0.6 and abs(b[2] - z1) < 0.6]
    return np.isin(tl, s), len(s)


p = G.bul("ELK_TOPPING__kablo")
m, n = sec(p, [(2373.0, 2457.0, 918.0, 1078.0, -797.0, 7.0), (2360.0, 2461.0, 1068.0, 1072.0, -810.0, -168.0)])
print("  eski kablo", n, "· ucgen", G.sil(p, m))
p = G.bul("ELK_TOPPING__celik")
m, n = sec(p, [(2447.0, 2463.0, 1045.0, 1079.0, -134.3, -122.3), (2447.0, 2463.0, 1073.0, 1109.0, -627.7, -615.7), (2447.0, 2463.0, 1073.0, 1109.0, -401.0, -389.0),
               (2451.0, 2467.0, 1045.0, 1073.0, -335.5, -323.5), (2451.0, 2467.0, 1067.0, 1073.0, -634.5, -622.5)])
print("  eski kelepce", n, "· ucgen", G.sil(p, m))

XL = [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2375.0, 927.0, -16.0), (2375.0, 927.0, 5.0), (XC, 927.0, 5.0),
      (XC, Y_XL, 5.0), (XC, Y_XL, ZK), (KD1X, Y_XL, ZK)]
TB = [(2360.0, Y_TB, -170.0), (XC, Y_TB, -170.0), (XC, Y_TB, ZK), (KD1X, Y_TB, ZK)]
kab = [EO.boru(XL, R), EO.boru(TB, R)]
Xk, Tk = G.ag(kab, tol=0.05, ang=0.3)
print("  yeni kablo ucgen", G.ekle(G.bul("ELK_TOPPING__kablo"), Xk, Tk))


def kelepce(z):
    t, g = 1.0, 12.0; z0 = z - g / 2
    y0, y1 = Y_TB - R - t, Y_XL + R + t                                     # 1067 … 1077,5
    u = cq.Solid.makeBox(2498.5 - (XC - R - t), y1 - y0, g, cq.Vector(XC - R - t, y0, z0)).cut(
        cq.Solid.makeBox(2499.5 - (XC - R), (y1 - t) - (y0 + t), g + 2, cq.Vector(XC - R, y0 + t, z0 - 1)))
    k1 = cq.Solid.makeBox(t, 10.0, g, cq.Vector(2498.5 - t, y1, z0))       # ust kulak (duvara yasli)
    k2 = cq.Solid.makeBox(t, 10.0, g, cq.Vector(2498.5 - t, y0 - 10.0, z0))
    v1 = cq.Solid.makeCylinder(3.5, 2.0, cq.Vector(2497.5, y1 + 5.0, z), cq.Vector(-1, 0, 0))   # M4 vida basi
    v2 = cq.Solid.makeCylinder(3.5, 2.0, cq.Vector(2497.5, y0 - 5.0, z), cq.Vector(-1, 0, 0))
    return u.fuse(k1).fuse(k2).fuse(v1).fuse(v2).clean()


Xc, Tc = G.ag([kelepce(z) for z in (-60.0, -300.0, -540.0, -770.0)], tol=0.05, ang=0.3)
print("  ortak kelepce ucgen", G.ekle(G.bul("ELK_TOPPING__celik"), Xc, Tc))
G.kaydet(go); print("yazildi", go)
