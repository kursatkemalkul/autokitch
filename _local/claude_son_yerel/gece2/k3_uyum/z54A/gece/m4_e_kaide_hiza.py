# -*- coding: utf-8 -*-
"""MADDE 4 (90.png "kapak hatti duz olsun merdivenli degil") · onden gorunuste kapaklarin altindaki KAIDE (moduler sasi, y 63–123)
B'de 60 × 60 profil, on yuzu z −80, govdeyle bas basa (x 737,5–4398,5); E'de 40 × 40 profil, on yuzu z −90 ve govdeden iki uctan 40 mm
iceride (x 4440–5190) → B|E sinirinda ve E sag ucunda basamak (merdiven) goruntusu.
YENI: E moduler sasisi B ile ayni: 60 × 60 profil · on yuz z −80 · arka ray z −790…−730 · x 4401,5–4228,5 (govde ucu, B ile 3 mm derz).
Uc raylar 60 genislige: sol 4401,5–4461,5 · sag 5168,5–5228,5 (civata halkalari ray ortasina oteleme ile tasinir, sekli bozulmaz).
Ayaklar (E_GOVDE__celik, 6 adet) ray ortalarina: x −28,5 / 0 / +28,5 · arka ayaklar z +10.
Kullanim: python m4_e_kaide_hiza.py giris.glb cikis.glb"""
import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\k3_uyum\z54A\gece")
import glbkit

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)


def esle_x(x):
    x = x.copy(); o = x.copy()
    for a, b, d in ((4440.0, 4443.0, -38.5), (4477.0, 4480.0, -18.5), (5150.0, 5153.0, 18.5), (5187.0, 5190.0, 38.5)):
        m = (o >= a - 0.01) & (o <= b + 0.01); x[m] = o[m] + d
    m = (o > 4443.01) & (o < 4476.99); x[m] = o[m] - 28.5
    m = (o > 5153.01) & (o < 5186.99); x[m] = o[m] + 28.5
    return x


def esle_z(z):
    z = z.copy(); o = z.copy()
    for a, b, d in ((-130.0, -127.0, -10.0), (-93.0, -90.0, 10.0), (-753.0, -750.0, 20.0)):
        m = (o >= a - 0.01) & (o <= b + 0.01); z[m] = o[m] + d
    m = (o > -786.99) & (o < -753.01); z[m] = o[m] + 10.0                   # arka ray ici (civata halkalari) ortaya
    return z


p = G.bul("E_MODULER__paslanmaz"); vis = G.gorunur(p)
n = G.tasi(p, vis, lambda V: np.c_[esle_x(V[:, 0]), V[:, 1], esle_z(V[:, 2])])
print("  E_MODULER kose", n)
U = np.unique(p["T"][vis].reshape(-1)); V = p["X"][U]
print("  yeni sasi x %.1f–%.1f · z %.1f–%.1f" % (V[:, 0].min(), V[:, 0].max(), V[:, 2].min(), V[:, 2].max()))

p = G.bul("E_GOVDE__celik"); tl, kut = G.komp(p)
for (x0, x1, z0, z1), d in (((4440, 4480, -790, -750), (-28.5, 10)), ((4440, 4480, -130, -90), (-28.5, 0)), ((4795, 4835, -790, -750), (0, 10)),
                            ((4795, 4835, -130, -90), (0, 0)), ((5150, 5190, -790, -750), (28.5, 10)), ((5150, 5190, -130, -90), (28.5, 0))):
    s = [i for i, (a, b, n_) in kut.items() if abs(a[0] - x0) < 0.2 and abs(b[0] - x1) < 0.2 and abs(a[2] - z0) < 0.2 and abs(b[2] - z1) < 0.2 and a[1] < 1 and b[1] < 124]
    assert len(s) == 1, (x0, z0, s)
    if d != (0, 0): G.tasi(p, np.isin(tl, s) & G.gorunur(p), lambda V, d=d: V + [d[0], 0, d[1]])
    print("  ayak x%.0f z%.0f → %+.1f / %+.0f" % (x0, z0, d[0], d[1]))
G.kaydet(go); print("yazildi", go)
