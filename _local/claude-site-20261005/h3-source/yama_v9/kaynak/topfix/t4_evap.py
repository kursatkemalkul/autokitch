# -*- coding: utf-8 -*-
"""TOPFIX 4 · EVAPORATOR IKIYE: alt kaset (alt bolmeyi -kiyma/kusbasi/kasar/sucuk- sogutur) + ust kaset (ust bolme -harc/sos-), ikisi de
harc silindirinin saginda (net 10) / sos silindirinin solunda (net 10,5), aralarinda 10 mm.
Her kaset: dis sac + PU 39 + ic sac · POM isi kesici cerceve · fan bolmesi (Sanyo 9WPA 120, eskisinin kopyasi) | serpantin 204 x 137 x 85 | TXV + emis kollektoru.
Sivi / emis hatlari asagidan (eski uclar x 2134 / 2156, y 1383) yukari: alt kasette T ile alt TXV'ye / alt kollektore, ustte dirsekle ust kasete (paralel).
Tahliye: ust kasetin tavasindan dik boru alt kasetten gecer, alt kasetin tavasinda birlestirme T'si -> tek hortum -> sicak gaz tavasi (eski delik x 2110).
Fan kablolari: ust -> tavan rakoru -> pano tabani (y 1880) · alt -> sol duvar rakoru -> y 1500 -> x 1538 (dik kanal onu) -> pano tabani.
python t4_evap.py giris.glb cikis.glb"""
import os, sys, json, pickle, numpy as np
from tlib import *
import tgeo as TG
from t_olcu import *
Kb, S_, kes, tekle, bb, boru = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb, TG.boru
gi, go = sys.argv[1:3]
G = Glb(gi)
SOG = (kat_no(G, "SOGUTMA"), mek_no(G, "TOPPING/Soğutma"))
ELK = (kat_no(G, "ELEKTRIK"), mek_no(G, "TOPPING/Elektrik"))
KOP = pickle.load(open("kopya.pkl", "rb"))
yA0, yA1 = KASET["alt"]; yU0, yU1 = KASET["ust"]
iA0, iA1 = ic("alt"); iU0, iU1 = ic("ust")
# ---- hat / boru eksenleri
XS, XE, ZH = 2134.0, 2156.0, -700.0          # sivi (r 3,2) · emis (r 6,35)
XT, ZT = 2126.0, -760.0                      # tahliye (r 5)
XK, ZK = 2131.0, -740.0                      # emis kollektoru (r 6,35)
RS, RE, RT = 3.2, 6.35, 5.0
FX = (FAN_X[0] + FAN_X[1]) / 2               # fan ekseni 1860,5
RAK_R = 11.5
YRA, ZRA = 1500.0, -750.0                      # alt fan kablosu rakoru (fanin arkasinda, arka plenumda)


def delikler(k):
    """kaset duvarlarindan gecenler"""
    y0, y1 = KASET[k]; d = []
    for x, z, r in ((XS, ZH, RS + 0.5), (XE, ZH, RE + 0.5), (XT, ZT, RT + 0.5)):
        if k == "alt": d += [S_(r, (x, y0 - 1, z), (x, y0 + W + 1, z)), S_(r, (x, y1 - W - 1, z), (x, y1 + 1, z))]
        else:
            if x == XT or True: d += [S_(r, (x, y0 - 1, z), (x, y0 + W + 1, z))]
    if k == "ust": d += [S_(RAK_R, (FX, y1 - W - 1, -714.0), (FX, y1 + 1, -714.0))]
    else: d += [S_(RAK_R, (X0 - 1, YRA, ZRA), (X0 + W + 1, YRA, ZRA))]
    return d


YENI = []
for k in ("alt", "ust"):
    y0, y1 = KASET[k]; a, b = ic(k); D = delikler(k)
    dis = Kb(X0, X1, y0, y1, Z0, Z1).cut(Kb(X0 + 1, X1 - 1, y0 + 1, y1 - 1, Z0 + 1, Z1 + 1))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_dis_sac" % k, kes(tekle(dis), D), SOG))
    pu = Kb(X0 + 1, X1 - 1, y0 + 1, y1 - 1, Z0 + 1, Z1).cut(Kb(XI0 - 1, XI1 + 1, a - 1, b + 1, ZI0 - 1, Z1 + 1))
    YENI.append(("TOPPING_MODUL__pu", "evap_%s_PU" % k, kes(tekle(pu), D), SOG))
    ics = Kb(XI0 - 1, XI1 + 1, a - 1, b + 1, ZI0 - 1, -631.0).cut(Kb(XI0, XI1, a, b, ZI0, -630.0))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_ic_sac" % k, kes(tekle(ics), D), SOG))
    YENI.append(("TOPPING_MODUL__pom", "evap_%s_isi_kesici_cerceve" % k, tekle(Kb(X0, X1, y0, y1, -640.0, -630.0).cut(Kb(XI0 - 1, XI1 + 1, a - 1, b + 1, -641.0, -629.0))), SOG))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_kollektor_on_kapak" % k, Kb(KOL_X[0], XI1, a, b, -632.0, -631.0), SOG))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_ara_perde_fan" % k, Kb(1922.0, 1923.0, a, b, SER_Z[0], -631.0), SOG))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_ara_perde_kollektor" % k, Kb(2127.0, 2128.0, a, b, SER_Z[0], -632.0), SOG))
    YENI.append(("TOPPING_MODUL__celik", "evap_%s_serpantin_204x137x85" % k, Kb(SER_X[0], SER_X[1], a + 1.0, b - 1.0, SER_Z[0], SER_Z[1]), SOG))
    yc = (a + b) / 2
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_fan_paneli" % k, kes(Kb(FAN_X[0], FAN_X[1], a, b, -701.5, -700.0), [S_(58.0, (FX, yc, -702.0), (FX, yc, -699.0))]), SOG))
    ytx = a + 6.0
    YENI.append(("TOPPING_MODUL__koyu", "evap_%s_TXV_dagitici" % k, Kb(2128.5, 2150.0, ytx, ytx + 30.0, -670.0, -645.0), SOG))
    YENI.append(("TOPPING_MODUL__bakir", "evap_%s_emis_kollektoru" % k, S_(RE, (XK, a + 6.0, ZK), (XK, b - 6.0, ZK)), SOG))
    for xb in (X0 + 20.0, X1 - 50.0):
        YENI.append(("TOPPING_MODUL__sac", "evap_%s_aski_braketi" % k, Kb(xb, xb + 30.0, y0 + 20.0, y0 + 40.0, -828.5, -826.0), SOG))
# ---- sivi / emis hatlari (paralel: alt kasette T, ust kasette dirsek)
tA, tU = iA0 + 6.0 + 15.0, iU0 + 6.0 + 15.0          # TXV ortasi y
eA, eU = 1500.0, 1730.0                               # emis kollektoru baglanti y
YENI += [("TOPPING_MODUL__bakir", "evap_sivi_hatti_yukselen", boru([(XS, yA0, ZH), (XS, tU, ZH), (XS, tU, -670.0)], RS), SOG),
         ("TOPPING_MODUL__bakir", "evap_sivi_T_alt_kol", boru([(XS, tA, ZH), (XS, tA, -670.0)], RS), SOG),
         ("TOPPING_MODUL__bakir", "evap_sivi_T_alt", S_(RS + 1.2, (XS, tA - 6, ZH), (XS, tA + 6, ZH)), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_hatti_yukselen", boru([(XE, yA0, ZH), (XE, eU, ZH), (XE, eU, ZK), (XK, eU, ZK)], RE), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_T_alt_kol", boru([(XE, eA, ZH), (XE, eA, ZK), (XK, eA, ZK)], RE), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_T_alt", S_(RE + 1.5, (XE, eA - 9, ZH), (XE, eA + 9, ZH)), SOG)]
# ---- tahliye (ortak): ust tava -> alt kasetten gecer -> alt tavada birlestirme T'si -> sicak gaz tavasi (x 2110, eski taban deligi)
YENI += [("TOPPING_MODUL__silikon", "evap_ortak_tahliye_hortumu", boru([(XT, iU0, ZT), (XT, 1140.0, ZT), (2110.0, 1140.0, ZT), (2110.0, 945.0, ZT)], RT), SOG),
         ("TOPPING_MODUL__silikon", "evap_tahliye_birlestirme_T", Kb(XT - 8.0, XT + 8.0, iA0, iA0 + 12.0, ZT - 8.0, ZT + 8.0), SOG)]
# ---- fan kablolari
YENI += [("ELK_TOPPING__kablo", "kablo_TOPPING_evap_ust_fan", boru([(FX, iU0 + (iU1 - iU0) / 2 + 60.0, -714.0), (FX, 1879.8, -714.0)], 2.5), ELK),
         ("ELK_TOPPING__kablo", "kablo_TOPPING_evap_alt_fan", boru([(1815.0, YRA, -726.5), (1815.0, YRA, ZRA), (1600.0, YRA, ZRA), (1600.0, YRA, -714.0), (1538.0, YRA, -714.0), (1538.0, 1879.8, -714.0)], 2.5), ELK)]
for nd, ad, s, (kt, mk) in YENI:
    n = ekle_kati(G, nd, [s], kt, mk, False)
    log("YENI %-24s %-34s %s  %d" % (nd.replace("TOPPING_MODUL__", ""), ad, [round(v, 1) for v in bb(s)], n))
# ---- fanlar (eski 2 fanin birebir kopyasi) + rakorlar
FC_ESKI = [(1826.0, 1652.0), (2006.0, 1652.0)]
for (ox, oy), F, k in zip(FC_ESKI, KOP["fan"], ("alt", "ust")):
    a, b = ic(k); d = np.array([FX - ox, (a + b) / 2 - oy, 0.0])
    for Pw, (kt, mk, kp) in F: ekle_ucgen(G, "TOPPING_MODUL__motor", Pw + d, kt, mk, kp)
    log("FAN kopya", k, d)
c_old = np.array([1826.0, 1744.5, -713.835])
for Pw, (kt, mk, kp) in KOP["rakor"]:
    ekle_ucgen(G, "ELK_TOPPING__rakor", Pw + (np.array([FX, iU1 + W / 2, -713.835]) - c_old), kt, mk, kp)       # ust kaset tavani
    v = Pw - c_old; Q = np.stack([-v[..., 1], v[..., 0], v[..., 2]], -1) + np.array([X0 + W / 2, YRA, ZRA])
    ekle_ucgen(G, "ELK_TOPPING__rakor", Q, kt, mk, kp)                                                           # alt kaset sol duvari (x yonunde)
log("RAKOR 2")
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
