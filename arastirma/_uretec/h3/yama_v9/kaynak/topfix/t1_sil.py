# -*- coding: utf-8 -*-
"""TOPFIX 1 · SIL / A BOSALT: m7b kabugu (cep) + eski evaporator penceresi + eski evaporator + 8 pnomatik hortum + KD3/motor kablolari
+ evap fan kablolari · A icindeki kablo/kelepce/kusak/sensor/hava · ana hat A dallari · bos enerji zinciri teknesi · X motoru TOPPING ucuna.
python t1_sil.py giris.glb cikis.glb"""
import sys, json, pickle, numpy as np
from tlib import *
gi, go = sys.argv[1:3]
G = Glb(gi)
ETK = {}
# ---------------- 1 · m7b eklemeleri (indis araliklari v8x_a -> v8x_b; v8zb'de birebir dogrulandi: aralik.py)
AR = {("TOPPING_MODUL__paslanmaz", 0): (18254, 24381), ("TOPPING_MODUL__pu", 0): (3180, 5560), ("TOPPING_MODUL__sac", 0): (13060, 13680), ("A_GOVDE__sac", 0): (68, 652)}
for (ad, pi), (a, b) in AR.items():
    p = [q for q in G.prims if q["name"] == ad and q["pi"] == pi][0]
    m = np.zeros(len(p["T"]), bool); m[a:b] = True
    m1 = np.zeros(len(p["T"]), bool); m1[a] = True
    ETK[ad] = etiket(G, p, m1)
    m &= G.gorunur(p)
    log("SIL m7b araligi", ad, a, b, G.sil(p, m))
# m8'de delik / kenar icin yeniden eklenmis m7b parcalari (kutu ile)
sil_tri(G, "A_GOVDE__sac", (1434.4, 1436.1, 787.9, 2198.6, -830.1, 59.1), not_="A sag levha (m8 delikli surum)")
sil_tri(G, "TOPPING_MODUL__sac", (1435.9, 1437.6, 891.9, 2198.6, -830.1, 39.1), not_="TOPPING dis yan sol (m8 delikli surum)")
for a, b in ((2030.5, 2093.5), (2324.0, 2387.0)):
    sil_tri(G, "TOPPING_MODUL__paslanmaz", (a, b, 1142.3, 1144.1, -116.1, 20.1), not_="raf dil kanali tabani (m8 1142,4)")
# ---------------- 2 · eski evaporator penceresi (soguk oda arka duvari PEN prizmasi)
for ad in ("TOPPING_MODUL__paslanmaz", "TOPPING_MODUL__pu", "TOPPING_MODUL__sac", "TOPPING_MODUL__pom"):
    et, n = sil_tri(G, ad, (1697.9, 2194.1, 1404.9, 1743.1, -630.1, -569.9), not_="eski evap penceresi", bekle=False)
    if et: ETK["pen_" + ad] = et
# ---------------- 3 · eski evaporator kaseti + ici + ayaklar + tahliye hortumu + fan kablolari (fan ve rakor once kopyalanir)
FAN = [al_tri(G, "TOPPING_MODUL__motor", (x0, x0 + 120, 1592, 1712, -726.5, -701.5), e=0.2) for x0 in (1766.0, 1946.0)]
RAKOR = al_tri(G, "ELK_TOPPING__rakor", (1814.5, 1837.5, 1714.4, 1777.1, -725.3, -702.4))
pickle.dump({"fan": FAN, "rakor": RAKOR}, open("kopya.pkl", "wb"))
log("kopya: fan", [sum(len(x[0]) for x in F) for F in FAN], "rakor", sum(len(x[0]) for x in RAKOR))
EV = (1675.9, 2216.1, 1382.9, 1765.1, -826.1, -629.9)
for ad in ("TOPPING_MODUL__sac", "TOPPING_MODUL__pu", "TOPPING_MODUL__pom", "TOPPING_MODUL__celik", "TOPPING_MODUL__motor", "TOPPING_MODUL__koyu", "TOPPING_MODUL__bakir", "TOPPING_MODUL__silikon"):
    et, n = sil_tri(G, ad, EV, not_="eski evaporator", bekle=False)
    if et: ETK["evap_" + ad] = et
for K in ((1690.9, 1721.1, 1349.9, 1383.1, -826.1, -629.9), (2175.9, 2206.1, 1349.9, 1383.1, -826.1, -629.9)):
    sil_tri(G, "TOPPING_MODUL__sac", K, not_="eski evap ayagi")
ETK["tahliye"] = sil_tri(G, "TOPPING_MODUL__silikon", (2095.9, 2115.1, 944.9, 1383.1, -780.1, -754.9), not_="eski tahliye hortumu")[0]
for x in (1823.5, 1972.5):
    ETK["fan_kablo"] = sil_tri(G, "ELK_TOPPING__kablo", (x, x + 5, 1711.9, 1879.9, -716.5, -711.4), not_="eski fan kablosu")[0]
for x in (1814.5, 1963.5):
    ETK["fan_rakor"] = sil_tri(G, "ELK_TOPPING__rakor", (x, x + 23, 1714.4, 1777.1, -725.3, -702.4), not_="eski fan rakoru")[0]
# ---------------- 4 · 8 pnomatik hortum + rakorlari
ETK["hortum"] = sil_tri(G, "TOPPING_MODUL__hava_ana", (1485.0, 2300.0, 1205.0, 1660.0, -830.0, -600.0), not_="8 pnomatik hortum + port rakorlari")[0]
# ---------------- 5 · KD3 kanali + 4 kaset motor kablosu (m7c)
ETK["kd3"] = sil_tri(G, "ELK_TOPPING__kanal", (1470.0, 2400.0, 1240.0, 1270.0, -798.0, -768.0), not_="KD3")[0]
for K in ((2059.0, 2128.0, 1127.0, 1240.0, -810.0, -779.0), (2059.0, 2065.0, 1270.0, 1296.5, -810.0, -779.0),
          (2352.5, 2395.0, 1147.0, 1240.0, -810.0, -779.0), (2352.5, 2358.5, 1252.0, 1265.5, -810.0, -798.0)):
    ETK["motor_kablo"] = sil_tri(G, "ELK_TOPPING__kablo", K, not_="kaset motor kablosu")[0]
# ---------------- 6 · A BOSALT
for K in ((878.0, 1538.5, 917.5, 1879.8, -728.0, -10.5), (883.5, 1532.5, 917.5, 1879.8, -722.5, -10.5), (885.0, 1533.0, 921.5, 1879.8, -778.0, -462.3)):
    c = [x for x in komps(G, "ELK_TOPPING__kablo") if kutu_esit(x[2], x[3], K, 0.6)]
    for p, m, lo, hi, n in c:
        ETK["a_kablo"] = etiket(G, p, m); G.sil(p, m)
    log("SIL A kablosu", K, len(c))
sil_tri(G, "ELK_TOPPING__celik", (736.0, 1436.5, 788.0, 2200.0, -830.0, 60.0), not_="A icindeki kelepce + dil (15)")
for ad, K in (("TOPPING_MODUL__celik", (1047.9, 1064.1, 907.9, 914.1, -35.1, -18.9)), ("TOPPING_MODUL__koyu", (1050.0, 1062.1, 914.0, 926.0, -25.1, -18.9)),
              ("TOPPING_MODUL__celik", (1077.9, 1094.1, 907.9, 914.1, -35.1, -18.9)), ("TOPPING_MODUL__koyu", (1080.0, 1092.1, 914.0, 926.0, -25.1, -18.9))):
    if ad.endswith("celik") and K[0] > 1070: SENS_C = al_tri(G, ad, K)
    if ad.endswith("koyu") and K[0] > 1070: SENS_K = al_tri(G, ad, K)
    e_, n_ = sil_tri(G, ad, K, not_="A ucundaki x sol limit / x sifir sensoru")
pickle.dump({"celik": SENS_C, "koyu": SENS_K}, open("sensor_kopya.pkl", "wb"))
sil_tri(G, "TOPPING_MODUL__koyu", (1063.4, 1108.6, 1279.9, 1474.1, -562.6, -517.4), not_="aciciya bagli hava baglantisi")
sil_tri(G, "A_GOVDE__paslanmaz", (737.4, 752.6, 1279.9, 1320.1, -798.6, 29.1), not_="A sol duvar yatay kusak")
sil_tri(G, "A_GOVDE__paslanmaz", (767.4, 1404.6, 1279.9, 1320.1, -828.6, -813.4), not_="A arka yatay kusak")
for ad, K in (("ELK_ANA_HAT__kablo", (1277.75, 3668.25, 2014.75, 2166.0, -823.45, -411.9)), ("ELK_ANA_HAT__kablo_veri", (1292.65, 3679.35, 2016.65, 2162.2, -823.5, -411.9))):
    c = [x for x in komps(G, ad) if kutu_esit(x[2], x[3], K, 0.6)]
    for p, m, lo, hi, n in c: G.sil(p, m)
    log("SIL ana hat A dali (A_guc / A_veri)", ad, len(c))
# ana hat kanali A'ya girmez: bati ucu x 1250 -> 1440 (TOPPING sol yan sacinin icinde biter)
for p in G.prims:
    if p["name"] != "ELK_ANA_HAT__kanal": continue
    v = np.where(p["X"][:, 0] < 1440.0)[0]
    if len(v):
        p["X"][v, 0] = 1440.0; p["degX"] = True; log("ana hat kanali bati ucu 1440", len(v), "kose")
# bos enerji zinciri teknesi (A'dan geciyordu, ici bos)
ETK["tekne"] = sil_tri(G, "TOPPING_MODUL__sac", (915.9, 2490.1, 893.4, 953.6, -475.1, -414.9), not_="bos enerji zinciri teknesi")[0]
# X motoru + braketi + tahrik kasnagi -> rayin TOPPING ucu; TOPPING ucundaki gergi kasnagi -> A ucu
DX = 2378.4 - 876.1
MOT = [("TOPPING_MODUL__motor", (847.9, 904.1, 895.9, 953.1, -462.1, -397.4)), ("TOPPING_MODUL__sac", (830.9, 921.1, 896.4, 967.1, -397.6, -389.4)),
       ("TOPPING_MODUL__celik", (866.6, 885.6, 915.4, 934.6, -397.6, -352.4))]
GER = [("TOPPING_MODUL__celik", (2356.3, 2400.5, 912.4, 942.1, -385.1, -352.4)), ("TOPPING_MODUL__celik", (2357.3, 2360.5, 936.9, 954.1, -377.1, -365.9)),
       ("TOPPING_MODUL__silikon", (2345.3, 2357.5, 939.8, 949.9, -377.6, -367.4))]
TM = [(ad, tri_kutu(G, ad, K)) for ad, K in MOT]; TG_ = [(ad, tri_kutu(G, ad, K)) for ad, K in GER]
for ad, L in TM:
    for p, m in L: tasi(G, p, m, lambda V: V + np.array([DX, 0, 0]))
    log("TASI X motoru grubu", ad, sum(int(m.sum()) for _, m in L), "+%.1f" % DX)
for ad, L in TG_:
    for p, m in L: tasi(G, p, m, lambda V: V - np.array([DX, 0, 0]))
    log("TASI gergi kasnagi", ad, sum(int(m.sum()) for _, m in L), "-%.1f" % DX)
# ---------------- 7 · cep raf aski burclari geri (+199)
tasi_tri(G, "TOPPING_MODUL__pom", (1238.4, 1296.1, 1110.0, 1560.0, -530.0, -30.0), lambda V: V + np.array([199.0, 0, 0]), not_="raf aski burclari sol +199")
json.dump({k: (list(v) if v else None) for k, v in ETK.items()}, open("t1_etiket.json", "w"), indent=0)
kaydet(G, go)
