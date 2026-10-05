# -*- coding: utf-8 -*-
"""q3 · QR GÖVDE TEMİZLİK (iş 1 + 3c QR kelepçeleri + 3d QR boş delikleri). Göz ölçüleri / sayısı / dış ölçü DEĞİŞMEDİ.
 1 robot kontrol kutusu (rezerv): Harting'i kalkmış kutunun üst yüzündeki 66×36×32,5 cep kapandı → düz kutu 475×423×268 (ölçü aynı)
 2 giriş plakası a (robot KT20 + kör tapası, iç flanş) KALDIRILDI; arka alt kapaktaki 121×64,6 plaka-a kesiği kapandı (kapak düz)
    plaka b (QR güç/veri, bina, modem) KALIR — üstündeki 2 eski robot ağzı KT kör tapalı (standart kör grommet)
 3 QR alt dikey kanal yan sacındaki 29×15 robot ağzı + kör kapağı → sac düz (kapak silindi, delik kapandı)
 4 QR taban sacındaki iki eski kablo deliği (Ø40 + Ø30, x 4760–4835) + üstündeki örtü sacı → taban düz tek sac
 5 QR güç + veri kablosunun üst 2 kelepçesi (y 1954–1966) havadaydı → QR kutusu üstüne L braket (paslanmaz 3 mm, M4)
python q3_qr.py giris.glb cikis.glb"""
import sys
from qlib import *
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); R = []
# 1 robot kutusu
p, m, et = bilesen(G, "QR_ROBOT_KONTROL__robot_kutu", (4595.0, 20.0, 675.0), (5070.0, 443.0, 943.0))
R.append(("robot kutusu cepli -> sil", G.sil(p, m)))
R.append(("robot kutusu duz kutu", ekle(G, "QR_ROBOT_KONTROL__robot_kutu", kutu_ucgen((4595.0, 20.0, 675.0), (5070.0, 443.0, 943.0)), et)))
# 2 plaka a
for ad, lo, hi in (("ELK_QR_MONTAJ__paslanmaz", (5040.0, 20.6, 670.0), (5157.0, 83.6, 691.5)),
                   ("ELK_QR_KABLO__rakor", (5049.5, 21.0, 653.0), (5147.5, 79.0, 670.0)),
                   ("ELK_QR_KABLO__rakor", (5076.7, 38.6, 653.0), (5099.5, 61.4, 672.0))):
    p, m, et = bilesen(G, ad, lo, hi); R.append(("plaka a sil " + ad, G.sil(p, m)))
# arka alt kapak (kpk) cegi: x 5038-5159, y 21-85.6, z 670-671.5
p = prim(G, "ELK_QR_MONTAJ__on_seffaf")
P = p["X"][p["T"]]; vis = G.gorunur(p)
nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-12)
mn = P.min(1); mx = P.max(1)
duv = vis & (((np.abs(mn[:, 0] - 5038) < .01) & (np.abs(mx[:, 0] - 5038) < .01)) | ((np.abs(mn[:, 0] - 5159) < .01) & (np.abs(mx[:, 0] - 5159) < .01)) |
             ((np.abs(mn[:, 1] - 85.6) < .01) & (np.abs(mx[:, 1] - 85.6) < .01) & (mn[:, 0] >= 5037.9) & (mx[:, 0] <= 5159.1))) & (mx[:, 1] <= 85.7)
assert duv.sum() in (5, 6), int(duv.sum())
t0 = int(np.where(duv)[0][0]); etk = G._etiketler(p, t0)
G.sil(p, duv)
Q = [dortgen((5038, 21, 670), (5159, 21, 670), (5159, 85.6, 670), (5038, 85.6, 670), (0, 0, -1)),
     dortgen((5038, 21, 671.5), (5159, 21, 671.5), (5159, 85.6, 671.5), (5038, 85.6, 671.5), (0, 0, 1)),
     dortgen((5038, 21, 670), (5159, 21, 670), (5159, 21, 671.5), (5038, 21, 671.5), (0, -1, 0))]
G._ekle_dunya(p, np.concatenate(Q), *etk); R.append(("arka alt kapak plaka-a kesigi kapandi", int(duv.sum())))
# 3 alt dikey kanal 29x15 agzi
p, m, et = bilesen(G, "ELK_QR_KABLO__kanal", (4981.5, 283.0, 1035.0), (4983.0, 318.0, 1056.0))
R.append(("kanal agzi kor kapagi sil", G.sil(p, m)))
R.append(("kanal yan saci delik kapat", delik_kapat(G, prim(G, "ELK_QR_KABLO__kanal"), 0, 4983.0, 4984.5, 286.0, 315.0, 1038.0, 1053.0)))
# 4 taban sacı delikleri + ortu
p, m, et = bilesen(G, "ELK_QR_KABLO__paslanmaz", (4755.0, 20.0, 950.0), (4840.0, 21.5, 1000.0))
R.append(("taban delik ortu saci sil", G.sil(p, m)))
p = prim(G, "QR_GOVDE__qr_govde"); tl, kut = G.komp(p); vis = G.gorunur(p)
P = p["X"][p["T"]]; mn = P.min(1); mx = P.max(1)
kab = [i for i, (a, b, k) in kut.items() if np.allclose(a, (4570, 17, 670), atol=.1) and np.allclose(b, (5430, 2050, 1190), atol=.1)]
assert len(kab) == 1
k0 = vis & (tl == kab[0])
yuz = k0 & (((np.abs(mn[:, 1] - 17) < .01) & (np.abs(mx[:, 1] - 17) < .01)) | ((np.abs(mn[:, 1] - 20) < .01) & (np.abs(mx[:, 1] - 20) < .01) & (mn[:, 2] >= 670 - .01)
       & (mx[:, 0] - mn[:, 0] > 0) & (mx[:, 2] - mn[:, 2] > 0)))
# y=20 duzleminde yalniz taban ust yuzu (yukari bakan) -- asagi bakan kenar yuzleri (4 ucgen) kalsin
nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
yuz &= ~((np.abs(mn[:, 1] - 20) < .01) & (nn[:, 1] < 0))
del_ = k0 & (mx[:, 1] <= 20.01) & (mn[:, 1] >= 16.99) & (mn[:, 0] > 4755) & (mx[:, 0] < 4840) & (mn[:, 2] > 950) & (mx[:, 2] < 1000)   # delik duvarlari
sec = yuz | del_
print("   taban: yuz %d, delik duvari %d" % (int(yuz.sum()), int((del_ & ~yuz).sum())))
t0 = int(np.where(yuz)[0][0]); etk = G._etiketler(p, t0)
G.sil(p, sec)
Q = [dortgen((4570, 17, 670), (5430, 17, 670), (5430, 17, 1190), (4570, 17, 1190), (0, -1, 0)),
     dortgen((4570, 20, 670), (5430, 20, 670), (5430, 20, 1190), (4570, 20, 1190), (0, 1, 0))]
G._ekle_dunya(p, np.concatenate(Q), *etk); R.append(("taban saci duz (delikler kapandi)", int(sec.sum())))
# 5 L braket QR kutusu ustu -> ust kelepceler
et = bilesen(G, "ELK_QR_KABLO__celik", (4940.0, 1954.0, 775.0), (4972.1, 1966.0, 791.0), tol=0.3)[2]
Pw = np.concatenate([kutu_ucgen((4924.0, 1920.0, 772.0), (4940.0, 1922.0, 808.0)),        # ayak: QR kutusu ust yuzunde (M4 perçin somunu)
                     kutu_ucgen((4937.0, 1922.0, 772.0), (4940.0, 1967.0, 808.0))])       # dik kol: kelepce dilleri x 4940 yuzune
R.append(("L braket (QR ust kelepceler)", ekle(G, "ELK_QR_KABLO__celik", Pw, et)))
for r in R: print("  %-44s %d" % r)
G.kaydet(go); print("yazildi", go)
