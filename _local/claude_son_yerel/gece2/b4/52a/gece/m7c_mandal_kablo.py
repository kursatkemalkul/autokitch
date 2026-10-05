# -*- coding: utf-8 -*-
"""M7-C · kaşar / sucuk kaset KİLİT MANDALI kasetin önüne-altına + kaset motor kabloları ve KD3 kanalı yeni motor x'lerine.
python m7c_mandal_kablo.py giris.glb cikis.glb
MANDAL (her kaset 1 adet, kasetin sol-ön köşesinde, kaset genişliği içinde → yan pay kalmaz):
  gövde POM rafın ALTINDA (alt PU'daki cepte, 24 × 34 × 25), yaylı çelik DİL raf yarığından 8 mm yükselir ve kasetin ÖN yüzünü tutar
  (z −199,5…−193,5, kaset ön yüzü −200). Çıkarma: dil parmakla 8 mm bastırılır (omuz rafın altına dayanır, yay gövdede) → kaset önden
  çekilir, dil kasetin altından kayar. Takma: kaset itilir, dil kendiliğinden kalkar.
KABLO: 4 kaset motoru kablosu (sucuk rotor/helezon, kaşar rotor/helezon) yeni motor x'lerinden KD3'e; KD3 kanalı 2360 → 2400 uzar
  (sucuk motoru 2355,5'e geldi) · giriş delikleri yeni x'lerde · braketler aynı.
Üretece taşınacak yer: topping_uno_cad (yuva mandalı) + tgeo.kuru_duzen (SUR, KD3) / h3_elk_ist_v1."""
import os, sys, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "tg"))
import tgeo as TG
from m7kit import Glb
from m7_olcu import DX

K, S_, kes, tekle, bb = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb
gi, go = sys.argv[1], sys.argv[2]
G = Glb(gi)
rap = []

# ================================================================ 1 · MANDAL
MANDAL = {"kasar": (1932.5 + DX["kasar"], 1940.5 + DX["kasar"]), "sucuk": (2244.5 + DX["sucuk"], 2252.5 + DX["sucuk"])}   # kaset sol-ön köşesi (kaset gövdesi içinde, çıkış tüpünün solunda)
Z0, Z1 = -199.5, -193.5
YENI = []
for k, (a, b) in MANDAL.items():
    xc, zc = (a + b) / 2, (Z0 + Z1) / 2
    dil = tekle(K(a, b, 1144.0, 1160.0, Z0, Z1).fuse(K(a - 3.0, b + 3.0, 1144.0, 1149.0, Z0 - 2.0, Z1 + 2.0)))
    govde = kes(K(a - 8.0, b + 8.0, 1124.0, 1149.0, -214.0, -180.0), [K(a - 3.3, b + 3.3, 1126.0, 1150.0, Z0 - 2.3, Z1 + 2.3)])
    yay = S_(3.0, (xc, 1126.0, zc), (xc, 1144.0, zc))
    YENI += [("TOPPING_MODUL__celik", "yuva_%s_kilit_dili" % k, dil), ("TOPPING_MODUL__pom", "yuva_%s_kilit_govdesi" % k, govde),
             ("TOPPING_MODUL__celik", "yuva_%s_kilit_yayi" % k, yay)]

# ================================================================ 2 · KD3 + motor kabloları
def sec_kutu(p, kutu, e=1.0):
    tl, kut = G.komp(p); out = []
    for c, (lo, hi, n) in kut.items():
        if all(abs(v - w) < e for v, w in zip([lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]], kutu)): out.append(c)
    return tl, out


ESKI = {"ELK_TOPPING__kanal": [(1470.0, 2360.0, 1240.0, 1270.0, -798.0, -768.0)],
        "ELK_TOPPING__kablo": [(2059.0, 2128.0, 1127.0, 1240.0, -810.0, -779.0), (2059.0, 2065.0, 1270.0, 1296.5, -810.0, -779.0),
                               (2308.0, 2353.0, 1147.0, 1240.0, -810.0, -779.0), (2308.0, 2314.0, 1252.0, 1265.5, -810.0, -798.0)]}
ETK = {}
for nd, L in ESKI.items():
    p = G.bul(nd)
    for kutu in L:
        tl, cs = sec_kutu(p, kutu)
        assert len(cs) == 1, (nd, kutu, cs)
        m = (tl == cs[0]) & G.gorunur(p); ti = int(np.where(m)[0][0])
        ETK.setdefault(nd, (G.etiket_of(p, ti), G.etiket_of(p, ti, "mek")))
        G.sil(p, m); rap.append("SIL %s %s %d üçgen" % (nd, kutu, m.sum()))

xk, xs = 2062.0 + DX["kasar"], 2311.0 + DX["sucuk"]          # 2074,5 · 2355,5
x0, x1, y0, y1, z0, z1 = 1470.0, 2400.0, 1240.0, 1270.0, -798.0, -768.0
t = 1.5
kan = K(x0, x1, y0, y1, z0, z1).cut(K(x0 - 1, x1 + 1, y0 + t, y1 - t, z0 + t, z1 - t))
XH_K, XH_S = xk + 63.0, 2392.0                                 # helezon kablolarının kanala alttan giriş x'i
giris = [S_(4.5, (xs, 1255.0, z0 - 1), (xs, 1255.0, z0 + t + 1))]
giris += [S_(4.0, (x, y0 - 1, -782.0), (x, y0 + t + 1, -782.0)) for x in (XH_K, XH_S)]
giris += [S_(4.0, (x, y1 - t - 1, -782.0), (x, y1 + 1, -782.0)) for x in (xk, 1482.0, 1515.0, 1548.0, 1581.0)]
YENI.append(("ELK_TOPPING__kanal", "kanal_TOPPING_KD3_motor", kes(kan, giris)))
r = 3.0
YENI += [("ELK_TOPPING__kablo", "kablo_TOPPING_motor_sucuk_rotor", TG.boru([(xs, 1265.5, -807.0), (xs, 1255.0, -807.0), (xs, 1255.0, z0)], r)),
         ("ELK_TOPPING__kablo", "kablo_TOPPING_motor_sucuk_helezon", TG.boru([(xs, 1161.5, -807.0), (xs, 1150.0, -807.0), (xs, 1150.0, -782.0),
                                                                             (XH_S, 1150.0, -782.0), (XH_S, y0, -782.0)], r)),
         ("ELK_TOPPING__kablo", "kablo_TOPPING_motor_kasar_rotor", TG.boru([(xk, 1296.5, -807.0), (xk, 1285.0, -807.0), (xk, 1285.0, -782.0), (xk, y1, -782.0)], r)),
         ("ELK_TOPPING__kablo", "kablo_TOPPING_motor_kasar_helezon", TG.boru([(xk, 1141.5, -807.0), (xk, 1130.0, -807.0), (xk, 1130.0, -782.0),
                                                                             (XH_K, 1130.0, -782.0), (XH_K, y0, -782.0)], r))]


# ================================================================ 3 · tabla boş sensörü (sucuk düşme borusu artık x 2324–2387'de) → z −45 (tabla hâlâ altında)
from m7_etiket import etiketle
R = etiketle(G, ("TOPPING_MODUL",))
DZ = -45.0
for i, (tl, kut, ad_) in R.items():
    p = G.prims[i]
    for c, nm in ad_.items():
        if nm in ("tabla_bos_sensoru", "sensor_braketi_tabla_bos"):
            m = (tl == c) & G.gorunur(p); G.tasi(p, m, lambda V: V + np.array([0, 0, DZ])); rap.append("TASI %s z%+.0f" % (nm, DZ))
p = G.bul("ELK_TOPPING__kablo")
tl, cs = sec_kutu(p, (2360.0, 2496.0, 1068.0, 1072.0, -805.0, -168.0))
assert len(cs) == 1, cs
m = (tl == cs[0]) & G.gorunur(p); vs = np.unique(p["T"][m].reshape(-1)); sel = vs[p["X"][vs, 2] > -176.0]
p["X"][sel, 2] += DZ; p["degX"] = True; rap.append("KABLO tabla boş sensörü: sensör ucu + yatay kol z%+.0f (%d köşe)" % (DZ, len(sel)))
# ================================================================ 5 · sos yayıcı kelepçe kanadı (+x → sucuk kaseti çekme yoluna giriyordu) → arkaya (−z) çevrilir
from m7_olcu import X_R, Z_H
for i, (tl, kut, ad_) in R.items():
    p = G.prims[i]
    for c, nm in ad_.items():
        lo, hi, n = kut[c]
        if lo[0] > X_R + 20 and hi[0] < X_R + 45 and lo[1] > 1200 and hi[1] < 1220 and lo[2] > -180 and hi[2] < -160:
            m = (tl == c) & G.gorunur(p)
            def don(V):
                W = V.copy(); vx = V[:, 0] - X_R; vz = V[:, 2] - Z_H
                W[:, 0] = X_R + vz; W[:, 2] = Z_H - vx; return W
            G.tasi(p, m, don); rap.append("DONDUR sos yayıcı kelepçe kanadı (%s #%d) +x → −z" % (p["name"], c))

REF = {"TOPPING_MODUL__celik": None, "TOPPING_MODUL__pom": None}
for nd, ad, s in YENI:
    p = G.bul(nd)
    if nd in ETK: kt, mk = ETK[nd]
    else: kt, mk = (3, 6) if "kasar" in ad else (3, 7)          # kaset yuvası: kat 3 · mek kaşar 6 / sucuk 7 (eski mandal etiketleri)
    Pp, I = G.ag([s])
    G.ekle_etiket(p, Pp, I, kat=kt, mek=mk)
    rap.append("YENI %-22s %-40s x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f · kat %s mek %s" % (nd, ad, *bb(s), kt, mk))
G.kaydet(go)
open(go.replace(".glb", "_rapor.txt"), "w", encoding="utf-8").write("\n".join(rap))
print("\n".join(rap)); print("yazildi", go)
sys.stdout.flush(); os._exit(0)
