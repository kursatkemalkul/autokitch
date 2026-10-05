# -*- coding: utf-8 -*-
"""q2 · HARTING (iş 4)
ANA PANO: ROBOT soketi (robot yok) + A soketi (A'nın elektriği yok, A hazır alınır) koruma kapaklarıyla birlikte KALDIRILDI;
  pano sol yan sacındaki ROBOT kesiği (y 1890–1950 · z −257,5…−222,5) ve arka sacındaki A kesiği (x 3650,5–3685,5 · y 1991–2051) KAPANDI
  (delik duvarı silinir, iki yüze dolgu → düz sac). Pano içinde bu soketlere bağlı tel yok (kanal x 3548'de başlıyor, soket 3545'te bitiyor).
QR KUTUSU HARTING'i KULLANILIYOR (ana hat QR güç 3G2,5 + QR Cat6A buraya iner, uçları x 4880 / y 2011): KALIR.
  Hata: m8t2 rakorun üstüne kör tapa koymuştu, kablolar tapaya 3 mm kala bitiyordu → tapa silindi, iki kablo ucu rakor ağzına (y 2005) indi.
QR robot Harting'i (QR_KABLO) R1'de zaten silinmişti — QR'da başka boş Harting bloğu yok.
python q2_harting.py giris.glb cikis.glb"""
import sys
from qlib import *
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); R = []
H = "ELK_ANA_PANO_UF__harting"
for ad_, lo, hi in (("ROBOT soketi", (3489.1, 1873.5, -261.7), (3545.0, 1966.5, -218.3)),
                    ("ROBOT koruma kapagi", (3471.1, 1884.0, -261.5), (3489.1, 1956.0, -218.5)),
                    ("A soketi", (3646.3, 1974.5, -348.9), (3689.7, 2067.5, -293.0)),
                    ("A koruma kapagi", (3646.5, 1985.0, -366.9), (3689.5, 2057.0, -348.9))):
    p, m, et = bilesen(G, H, lo, hi)
    R.append(("sil " + ad_, G.sil(p, m)))
pn = prim(G, "ELK_ANA_PANO_UF__pano")
R.append(("pano sol sac ROBOT kesigi kapat", delik_kapat(G, pn, 0, 3518.0, 3519.5, 1890.0, 1950.0, -257.5, -222.5)))
R.append(("pano arka sac A kesigi kapat", delik_kapat(G, pn, 2, -320.0, -318.5, 3650.5, 3685.5, 1991.0, 2051.0)))

# QR kutusu Harting: yanlis kor tapa + kablo uclari
p, m, et = bilesen(G, "ELK_QR_KUTU__rakor", (4868.0, 2005.0, 778.3), (4892.0, 2008.0, 802.3))
R.append(("QR Harting rakoru kor tapasi sil", G.sil(p, m)))
for ad in ("ELK_QR_KABLO__kablo", "ELK_QR_KABLO__kablo_veri"):
    p = prim(G, ad); T = p["T"][G.gorunur(p)]; vs = np.unique(T)
    X = p["X"][vs]
    s = vs[(np.abs(X[:, 1] - 2011.0) < 0.05) & (X[:, 0] > 4870) & (X[:, 0] < 4890) & (X[:, 2] > 770) & (X[:, 2] < 810)]
    assert len(s) >= 8, (ad, len(s))
    p["X"][s, 1] = 2005.0; p["degX"] = True
    R.append(("%s ucu y 2011 -> 2005 (rakor agzi)" % ad, len(s)))
for r in R: print("  %-46s %d" % r)
G.kaydet(go); print("yazildi", go)
