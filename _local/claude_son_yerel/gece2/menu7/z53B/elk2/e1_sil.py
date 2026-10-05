# -*- coding: utf-8 -*-
"""e1 · ESKİ HAT GENELİ ELEKTRİK SİLİNİR (v8zi -> e1):
 yıldız ana hat (ELK_ANA_HAT tümü: kablolar, kanallar, geçiş plakaları, istasyon Harting soketleri, QR yanı ana ayırıcı + dikey kanalı) ·
 zemin kanalı (ELK_ZEMIN_KANALI) · ana pano Harting soketleri + fişleri + M32 rakorları · F kutusu eski bina 230 V dış kablosu + arka rakoru ·
 K eski Harting → K kutusu iç besleme kablosu · B kutusu ön Harting soketi · QR giriş plakası b + dış kablo uçları + rakorları.
 Boş kalan dikdörtgen sac kesikleri kapanır (delik duvarı silinir, iki yüze dolgu).
python e1_sil.py giris.glb cikis.glb"""
import sys, numpy as np
from elib import *
import m8kit
from qlib import prim, bilesen, delik_kapat, ucgen_kutu
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); R = []
MEK = [m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]


def tum_sil(ad):
    n = 0
    for p in G.dprims(ad): n += G.sil(p, G.gorunur(p))
    R.append(("sil tum " + ad, n))


def mek_sil(ad, kodlar):
    for p in G.dprims(ad):
        ex = p["pr"].get("extras", {}); L = ex.get("mek") or []
        m = np.zeros(len(p["T"]), bool)
        for k in range(0, len(L) - 2, 3):
            if MEK[L[k]] in kodlar: m[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = True
        R.append(("sil %s mek %s" % (ad, "/".join(kodlar)), G.sil(p, m)))


def komp_sil(ad, lo, hi, tol=0.8, n=1):
    p, m, et = bilesen(G, ad, lo, hi, tol=tol, n=n)
    R.append(("sil %s %s" % (ad, np.round(lo).tolist()), G.sil(p, m)))


def kesik_bul_kapat(ad, eksen, lo, hi, kalin=3.5):
    """kutu icindeki dikdortgen kesigin duvarlarini bul -> delik_kapat"""
    p = prim(G, ad); P = p["X"][p["T"]]; vis = G.gorunur(p)
    m = ucgen_kutu(G, p, lo, hi)
    nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-12)
    ext = P.max(1)[:, eksen] - P.min(1)[:, eksen]
    m &= (np.abs(nn[:, eksen]) < 0.01) & (ext < kalin) & (ext > 0.3)
    if m.sum() != 8:
        R.append(("KESIK BULUNAMADI %s (%d duvar ucgeni)" % (ad, int(m.sum())), 0)); return
    Q = P[m].reshape(-1, 3); a = eksen; u, w = [i for i in range(3) if i != a]
    mn = Q.min(0); mx = Q.max(0)
    R.append(("kesik kapat %s %s" % (ad, np.round([mn[u], mx[u], mn[w], mx[w]], 1).tolist()),
              delik_kapat(G, p, a, mn[a], mx[a], mn[u], mx[u], mn[w], mx[w])))


# 1 · yıldız ana hat + zemin kanalı + pano Harting'leri (düğüm olarak)
for ad in ("ELK_ANA_HAT__kablo", "ELK_ANA_HAT__kablo_veri", "ELK_ANA_HAT__kanal", "ELK_ANA_HAT__paslanmaz", "ELK_ANA_HAT__rakor",
           "ELK_ANA_HAT__ayirici_kirmizi", "ELK_ANA_HAT__ayirici_sari", "ELK_ANA_HAT__cihaz_koyu", "ELK_ZEMIN_KANALI__paslanmaz",
           "ELK_ANA_PANO_UF__harting"):
    tum_sil(ad)
# 2 · ana pano fişleri + M32 rakorları, F altı eski ana hat rakoru (ELK_ISTASYON, mek Ana pano / Ana hat)
mek_sil("ELK_ISTASYON__rakor", ("Elektrik/Ana pano", "Elektrik/Ana hat"))
# 3 · QR dış uçlar (Dükkân hattı) + giriş plakası b
mek_sil("ELK_QR_KABLO__kablo", ("Çevre/Dükkân hattı",))
mek_sil("ELK_QR_KABLO__kablo_veri", ("Çevre/Dükkân hattı",))
mek_sil("ELK_QR_KABLO__rakor", ("Çevre/Dükkân hattı",))
p = prim(G, "ELK_QR_MONTAJ__paslanmaz"); R.append(("sil QR giris plakasi b", G.sil(p, ucgen_kutu(G, p, (5290, 15, 660), (5435, 90, 700)))))
# 4 · F kutusu eski bina 230 V dış kablosu + arka rakoru
komp_sil("ELK_ISTASYON__kablo", (2765.2, 915.2, -860.0), (2788.0, 924.8, -785.2))
komp_sil("ELK_ISTASYON__rakor", (2757.5, 907.6, -840.5), (2782.1, 932.4, -819.0))
# 5 · K: eski Harting -> K kutusu iç besleme kablosu
komp_sil("ELK_K__kablo", (4141.8, 1682.6, -781.2), (4296.2, 1829.8, -711.8))
# 6 · B kutusu ön Harting soketi (kpk kapakta) — fiş / kapak
p = prim(G, "ELK_ISTASYON__rakor"); R.append(("sil B kutusu Harting soketi", G.sil(p, ucgen_kutu(G, p, (4195, 630, -645), (4285, 700, -520)))))

G.kaydet(go)
# kesikler ikinci geçişte (sil sonrası yeniden yükle)
G = m8kit.Glb(go)
for (y0, y1, z0, z1) in ((1880, 1960, -170, -110), (1980, 2060, -270, -210), (1980, 2060, -170, -110), (2080, 2160, -270, -210), (2080, 2160, -170, -110)):
    kesik_bul_kapat("ELK_ANA_PANO_UF__pano", 0, (3516, y0, z0), (3522, y1, z1))
kesik_bul_kapat("ELK_ANA_PANO_UF__pano", 2, (3800, 1980, -322), (3856, 2060, -316))
kesik_bul_kapat("TOPPING_MODUL__sac", 0, (1985, 1995, -830), (2000, 2090, -760))
p_ = prim(G, "ELK_ISTASYON__pano")
for v0_, v1_ in ((-612.0, -610.0), (-613.2, -612.0)):
    R.append(("kesik kapat B kutusu kapagi z %.1f" % v0_, delik_kapat(G, p_, 2, v0_, v1_, 4207.0, 4273.0, 647.0, 683.0)))
for r in R: print("  %-70s %d" % r)
G.kaydet(go); print("yazildi", go)
