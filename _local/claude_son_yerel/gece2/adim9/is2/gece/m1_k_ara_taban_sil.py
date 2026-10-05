# -*- coding: utf-8 -*-
"""MADDE 1 (87.png) · K kesme istasyonu ARA RAFI (istasyon_tabani 892–895 saci + on/arka kayit_877 profilleri + kaynaklari) SILINIR.
Gorevi: bant ayaklarini ve itici taban plakalarini 892 kotunda tasimakti. Yan duvar boyunca giden istasyon_tabani_tasiyici_20/380
(30 × 30, kose dikmelerine kaynakli) KALIR (yan tutamak: M8 K↔F/E civatasi, tapalar ve itici plakalari bunun ustunde).
  · K_BANT 4 bant ayagi: alt yuz 895 → 791 (asil taban saci; ayak 37,5 → 141,5 mm · bant kotu 932,5 DEGISMEZ)
  · K_ITICI 4 itici taban plakasi 895–903 → 892–900 (dogrudan yan tasiyici ustune, −3) · eksen ayagi alt yuzu 903 → 900 (itici 958 DEGISMEZ)
  · ara taban saci icindeki PEM somunlari (bant M6 ×4 · itici M5 ×8) sacla birlikte kalkar (bant ayagi ve itici plakasi
    asil tabana / tasiyiciya vida + percin somunuyla: delikler uretecte — ACIK)
Kullanim: python m1_k_ara_taban_sil.py giris.glb cikis.glb"""
import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim9\is2\gece")
import glbkit

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)
R = []


def kutular(kut, x0, x1, y0, y1, z0, z1, e=0.06):
    return [i for i, (a, b, n) in kut.items() if a[0] >= x0 - e and b[0] <= x1 + e and a[1] >= y0 - e and b[1] <= y1 + e and a[2] >= z0 - e and b[2] <= z1 + e]


def ucgen_kutu(p, x0, x1, y0, y1, z0, z1, e=0.06):
    P = p["X"][p["T"]]
    return G.gorunur(p) & (P[:, :, 0].min(1) >= x0 - e) & (P[:, :, 0].max(1) <= x1 + e) & (P[:, :, 1].min(1) >= y0 - e) & (P[:, :, 1].max(1) <= y1 + e) & (P[:, :, 2].min(1) >= z0 - e) & (P[:, :, 2].max(1) <= z1 + e)


# 1 · K_GOVDE__sac: istasyon_tabani saci (+delik kaynaklari) · on/arka kayit_877 · kayit orta kaynaklari · taban-dikme kaynaklari
p = G.bul("K_GOVDE__sac")
m = ucgen_kutu(p, 4001.4, 4398.6, 891.9, 895.1, -828.6, 59.1)                 # istasyon_tabani saci
m |= ucgen_kutu(p, 4000, 4400, 894.9, 897.1, -830, 60)                          # sac-dikme kaynaklari (895–897)
m |= ucgen_kutu(p, 4034.9, 4365.1, 859.9, 892.1, 26.9, 57.1)                    # on kayit_877 + orta kaynaklari
m |= ucgen_kutu(p, 4034.9, 4365.1, 859.9, 892.1, -815.1, -784.9)                # arka kayit_877 + orta kaynaklari
m |= ucgen_kutu(p, 4060, 4340, 891.9, 895.1, -810, 50)                          # delik kaynaklari
m |= ucgen_kutu(p, 4015, 4025, 891.9, 895.1, -400, -130) | ucgen_kutu(p, 4375, 4385, 891.9, 895.1, -400, -130)
R.append(("K_GOVDE__sac ara raf", 0, G.sil(p, m)))

# 2 · K_GOVDE__celik: ara saca gomulu PEM'ler (bant M6 ×4, itici M5 ×8)
p = G.bul("K_GOVDE__celik"); tl, kut = G.komp(p)
pem = kutular(kut, 4049, 4351, 889.9, 894.4, -780, 5)
R.append(("PEM sil", len(pem), G.sil(p, np.isin(tl, pem))))

# 3 · K_BANT__sac: 4 ayak alt yuzu 895 → 791
def uzat_y(eski, yeni):
    def f(V):
        V[np.abs(V[:, 1] - eski) < 0.05, 1] = yeni; return V
    return f
p = G.bul("K_BANT__sac"); tl, kut = G.komp(p)
ay = kutular(kut, 4054, 4076, 894.9, 932.6, -432, 8) + kutular(kut, 4324, 4346, 894.9, 932.6, -432, 8)
R.append(("bant ayagi 895→791", len(ay), G.tasi(p, np.isin(tl, ay) & G.gorunur(p), uzat_y(895.0, 791.0))))

# 4 · K_ITICI__sac: taban plakalari −3 (yan tasiyici ustu 892), eksen ayaklari alt yuzu 903 → 900
p = G.bul("K_ITICI__sac"); tl, kut = G.komp(p)
tb = kutular(kut, 4021, 4059, 894.9, 903.1, -774, -626) + kutular(kut, 4341, 4379, 894.9, 903.1, -774, -626)
ea = kutular(kut, 4029, 4051, 902.9, 958.1, -766, -634) + kutular(kut, 4349, 4371, 902.9, 958.1, -766, -634)
R.append(("itici taban −3", len(tb), G.tasi(p, np.isin(tl, tb) & G.gorunur(p), lambda V: V + [0, -3, 0])))
R.append(("eksen ayagi 903→900", len(ea), G.tasi(p, np.isin(tl, ea) & G.gorunur(p), uzat_y(903.0, 900.0))))

for r in R: print("  %-28s bilesen %3d · %d" % r)
G.kaydet(go); print("yazildi", go)
