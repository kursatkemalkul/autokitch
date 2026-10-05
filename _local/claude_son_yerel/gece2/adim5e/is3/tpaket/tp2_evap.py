# -*- coding: utf-8 -*-
"""TP2 · EVAPORATOR YAN YANA + SURUCU KARTLARI + KLF KABLOSU.
 - eski 2 kaset (ust uste, x 1758-2223) + ici + bakir + ortak tahliye + 2 fan kablosu + alt fan rakoru silinir
 - L kaset (x 1446-1670, y 1282-1682) ve R kaset (x 1758-2223, y 1383-1835): dis sac + PU 39 + ic sac + POM cerceve, serpantin altta,
   fan ustte (Sanyo 9WPA 120, kaset basina 1), on bolme perdesi, R'de kollektor seridi; harc takimi (1696-1748) ikisinin arasinda
 - bakir: sivi/emis yukselenleri (x 2134/2156, y 1383) R'ye girer; R altinda T ile L koluna (arka plenumda, z -742 / -775) -> L TXV + L emis kollektoru (paralel)
 - tahliye: R (x 2126) + L (x 1625) -> y 1140'ta T -> tek hortum -> sicak gaz tavasi (x 2110, eski)
 - surucu kartlari (4) + DIN rayi + 2 ayak: x +804, y +268 (sos takiminin ustu, KD1'in yani; TOPPING kuru bolmesi icinde)
   motor kablolari -> KD1 sol yuzu (x 2421) · pano kablolari -> KD2 (pano alti kanal) alt yuzu
 - eski dik surucu kanali (x 1523-1553) y 1692'den baslar (L kasetin ustu; UPS/guc kaynagi arasinda kalir)
 - KLF6.6 kablosu x 1700 -> y 1140'ta x 1684 seridine -> pano tabani; 2 duvar kelepcesi +14 x
python tp2_evap.py giris.glb cikis.glb"""
import os, sys, numpy as np
TPD = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(TPD)
gi, go = [os.path.abspath(a) for a in sys.argv[1:3]]
sys.path.insert(0, os.path.join(S, "topfix")); sys.path.insert(0, TPD)
from tlib import *
import tgeo as TG
from tp_olcu import *
Kb, S_, kes, tekle, bb, boru = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb, TG.boru
G = Glb(gi)
SOG = (kat_no(G, "SOGUTMA"), mek_no(G, "TOPPING/Soğutma"))
ELK = (kat_no(G, "ELEKTRIK"), mek_no(G, "TOPPING/Elektrik"))
MS = mek_no(G, "TOPPING/Soğutma")


def mek_dizi(p):
    L = p["pr"].get("extras", {}).get("mek") or []; a = np.full(len(p["T"]), -1, int)
    for k in range(0, len(L) - 2, 3): a[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    return a


def sil_mek(ad, K, mek, not_=""):
    n = 0
    for p, m in tri_kutu(G, ad, K, e=0.05):
        m = m & (mek_dizi(p) == mek); n += G.sil(p, m)
    log("SIL-MEK %-24s %s %d ucgen %s" % (ad, [round(v, 1) for v in K], n, not_))


# ================================================================ 0 · kopyalar (fan, rakor)
FAN = al_tri(G, "TOPPING_MODUL__motor", (1800.0, 1921.0, 1433.0, 1554.0, -727.0, -701.0))
RAK = al_tri(G, "ELK_TOPPING__rakor", (1848.9, 1872.1, 1784.4, 1847.1, -725.3, -702.4))
log("kopya fan %d parca %d ucgen · rakor %d" % (len(FAN), sum(len(a) for a, _ in FAN), sum(len(a) for a, _ in RAK)))
# ================================================================ 1 · silinenler
EV = (1757.0, 2224.0, 1382.95, 1836.0, -829.0, -629.0)
for ad in ("TOPPING_MODUL__sac", "TOPPING_MODUL__pu", "TOPPING_MODUL__pom", "TOPPING_MODUL__celik", "TOPPING_MODUL__koyu",
           "TOPPING_MODUL__bakir", "TOPPING_MODUL__motor", "TOPPING_MODUL__silikon"):
    sil_mek(ad, EV, MS, "eski kasetler")
sil_mek("TOPPING_MODUL__silikon", (2104.0, 2135.0, 944.0, 1656.0, -769.0, -751.0), MS, "eski ortak tahliye + T")
sil_tri(G, "ELK_TOPPING__kablo", (1535.0, 1818.0, 1497.0, 1880.5, -753.0, -711.0), not_="eski alt fan kablosu")
sil_tri(G, "ELK_TOPPING__kablo", (1857.5, 1863.5, 1784.0, 1880.5, -717.0, -711.0), not_="eski ust fan kablosu")
sil_tri(G, "ELK_TOPPING__rakor", (1745.9, 1808.6, 1488.5, 1511.5, -761.4, -738.6), not_="eski alt fan rakoru")
MK, _ = sil_tri(G, "ELK_TOPPING__kablo", (1476.0, 1587.0, 1268.0, 1537.0, -811.0, -680.0), not_="surucu kablolari (8)")
KLF, _ = sil_tri(G, "ELK_TOPPING__kablo", (1665.0, 1705.0, 1086.9, 1880.0, -810.0, -800.0), not_="KLF kablosu ust kismi")
log("etiket surucu kablo", MK, "KLF", KLF)
# ================================================================ 2 · tasinanlar
D = np.array(D_KART)
tasi_tri(G, "TOPPING_MODUL__kart", (1467.0, 1596.0, 1431.0, 1478.0, -761.0, -699.0), lambda V: V + D, not_="4 surucu karti")
tasi_tri(G, "TOPPING_MODUL__sac", (1457.9, 1605.1, 1436.9, 1472.1, -767.6, -759.9), lambda V: V + D, not_="surucu DIN rayi")
for x0 in (1465.9, 1566.9):
    tasi_tri(G, "TOPPING_MODUL__celik", (x0, x0 + 30.2, 1439.4, 1469.6, -828.6, -767.4), lambda V: V + D, not_="DIN rayi ayagi")
for y0 in (1493.9, 1793.9):
    tasi_tri(G, "ELK_TOPPING__celik", (1665.3, 1674.7, y0, y0 + 12.2, -828.6, -798.9), lambda V: V + np.array([X_SERIT - 1670.0, 0, 0]), not_="KLF duvar kelepcesi")
def kisalt(V):
    V = V.copy(); V[:, 1] = np.maximum(V[:, 1], 1692.0); return V
tasi_tri(G, "ELK_TOPPING__kanal", (1522.9, 1553.1, 1534.9, 1879.6, -816.1, -775.9), kisalt, not_="dik surucu kanali y >= 1692")
# KD2 (pano alti yatay kanal) alt yuzu
kd2 = [p["X"][p["T"][m]] for p, m in tri_kutu(G, "ELK_TOPPING__kanal", (1889.9, 2449.1, 1321.4, 1880.0, -828.4, -788.4))]
V = np.concatenate([q.reshape(-1, 3) for q in kd2]); Y_KD2 = float(V[V[:, 0] < 2400.0, 1].min())
log("KD2 alt yuzu y", Y_KD2)
# ================================================================ 3 · kasetler


def delikler(k):
    (x0, x1), (y0, y1) = KAS[k]["x"], KAS[k]["y"]; d = []
    if k == "R":
        for x, z, r in ((XS, ZH, RS + 0.5), (XE, ZH, RE + 0.5), (XT_R, ZT_R, RT + 0.5)):
            d.append(S_(r, (x, y0 - 1, z), (x, y0 + W + 1, z)))
        for y, z, r in ((Y_SIVI_KOL, Z_SIVI_KOL, RS + 0.5), (Y_EMIS_KOL, Z_EMIS_KOL, RE + 0.5)):
            d.append(S_(r, (x0 - 1, y, z), (x0 + W + 1, y, z)))
        d.append(S_(11.5, (KAS[k]["fan"][0], y1 - W - 1, Z_FAN), (KAS[k]["fan"][0], y1 + 1, Z_FAN)))
    else:
        d.append(S_(RT + 0.5, (XT_L, y0 - 1, ZT_L), (XT_L, y0 + W + 1, ZT_L)))
        for y, z, r in ((Y_SIVI_KOL, Z_SIVI_KOL, RS + 0.5), (Y_EMIS_KOL, Z_EMIS_KOL, RE + 0.5), (KAS["L"]["fan"][1], Z_FAN, 11.5)):
            d.append(S_(r, (x1 - W - 1, y, z), (x1 + 1, y, z)))
    return d


YENI = []
for k in ("L", "R"):
    d = KAS[k]; (X0_, X1_), (y0, y1) = d["x"], d["y"]; XI0_, XI1_, a, b = ic(k); DL = delikler(k)
    dis = Kb(X0_, X1_, y0, y1, Z0, Z1).cut(Kb(X0_ + 1, X1_ - 1, y0 + 1, y1 - 1, Z0 + 1, Z1 + 1))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_dis_sac" % k, kes(tekle(dis), DL), SOG))
    pu = Kb(X0_ + 1, X1_ - 1, y0 + 1, y1 - 1, Z0 + 1, Z1).cut(Kb(XI0_ - 1, XI1_ + 1, a - 1, b + 1, ZI0 - 1, Z1 + 1))
    YENI.append(("TOPPING_MODUL__pu", "evap_%s_PU" % k, kes(tekle(pu), DL), SOG))
    ics = Kb(XI0_ - 1, XI1_ + 1, a - 1, b + 1, ZI0 - 1, -631.0).cut(Kb(XI0_, XI1_, a, b, ZI0, -630.0))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_ic_sac" % k, kes(tekle(ics), DL), SOG))
    YENI.append(("TOPPING_MODUL__pom", "evap_%s_isi_kesici_cerceve" % k, tekle(Kb(X0_, X1_, y0, y1, -640.0, -630.0).cut(Kb(XI0_ - 1, XI1_ + 1, a - 1, b + 1, -641.0, -629.0))), SOG))
    sx0, sx1, sy0, sy1 = d["ser"]
    YENI.append(("TOPPING_MODUL__celik", "evap_%s_serpantin_%dx%dx85" % (k, sx1 - sx0, sy1 - sy0), Kb(sx0, sx1, sy0, sy1, SER_Z[0], SER_Z[1]), SOG))
    py = d["perde_y"]
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_on_bolme_perdesi" % k, Kb(XI0_, XI1_, py, py + 1.0, SER_Z[0], -631.0), SOG))
    fx, fy = d["fan"]
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_fan_paneli" % k, kes(Kb(XI0_, XI1_, py + 1.0, b, FAN_PZ[0], FAN_PZ[1]), [S_(58.0, (fx, fy, -702.0), (fx, fy, -699.0))]), SOG))
    YENI.append(("TOPPING_MODUL__sac", "evap_%s_damlama_tavasi" % k, kes(Kb(XI0_, XI1_, a, a + 1.0, ZI0, -631.0), DL), SOG))
    for xb in (X0_ + 20.0, X1_ - 50.0):
        YENI.append(("TOPPING_MODUL__sac", "evap_%s_aski_braketi" % k, Kb(xb, xb + 30.0, y0 + 20.0, y0 + 40.0, -828.5, -826.0), SOG))
# R kollektor seridi
XI0_, XI1_, a, b = ic("R"); KX = KAS["R"]["kol_x"]; PY = KAS["R"]["perde_y"]
YENI += [("TOPPING_MODUL__sac", "evap_R_kollektor_ayirma_saci", Kb(KX, KX + 1.0, a + 1.0, PY, SER_Z[0], -632.0), SOG),
         ("TOPPING_MODUL__sac", "evap_R_kollektor_on_kapak", Kb(KX + 1.0, XI1_, a + 1.0, PY, -632.0, -631.0), SOG),
         ("TOPPING_MODUL__koyu", "evap_R_TXV_dagitici", Kb(2128.5, 2150.0, 1465.0, 1495.0, -670.0, -645.0), SOG),
         ("TOPPING_MODUL__bakir", "evap_R_emis_kollektoru", S_(RE, (XK_R, 1440.0, ZK_R), (XK_R, 1560.0, ZK_R)), SOG),
         ("TOPPING_MODUL__koyu", "evap_L_TXV_dagitici", Kb(XTXV_L[0], XTXV_L[1], YTXV_L[0], YTXV_L[1], Z_SIVI_KOL - 10.0, Z_SIVI_KOL + 10.0), SOG),
         ("TOPPING_MODUL__bakir", "evap_L_emis_kollektoru", S_(RE, (XK_L, Y_EMIS_KOL, Z_EMIS_KOL), (XK_L, 1495.0, Z_EMIS_KOL)), SOG)]
# ================================================================ 4 · bakir hatlar (paralel: R'ye dirsek, L'ye T)
a_R = ic("R")[2]
YENI += [("TOPPING_MODUL__bakir", "evap_sivi_hatti_R", boru([(XS, 1383.0, ZH), (XS, 1480.0, ZH), (XS, 1480.0, -670.0)], RS), SOG),
         ("TOPPING_MODUL__bakir", "evap_sivi_hatti_L_kolu", boru([(XS, Y_SIVI_KOL, ZH), (XS, Y_SIVI_KOL, Z_SIVI_KOL), (1612.0, Y_SIVI_KOL, Z_SIVI_KOL), (1612.0, YTXV_L[0], Z_SIVI_KOL)], RS), SOG),
         ("TOPPING_MODUL__bakir", "evap_sivi_T", S_(RS + 1.2, (XS, Y_SIVI_KOL - 6, ZH), (XS, Y_SIVI_KOL + 6, ZH)), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_hatti_R", boru([(XE, 1383.0, ZH), (XE, 1500.0, ZH), (XK_R, 1500.0, ZH), (XK_R, 1500.0, ZK_R)], RE), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_hatti_L_kolu", boru([(XE, Y_EMIS_KOL, ZH), (XE, Y_EMIS_KOL, Z_EMIS_KOL), (XK_L, Y_EMIS_KOL, Z_EMIS_KOL)], RE), SOG),
         ("TOPPING_MODUL__bakir", "evap_emis_T", S_(RE + 1.5, (XE, Y_EMIS_KOL - 9, ZH), (XE, Y_EMIS_KOL + 9, ZH)), SOG)]
# ================================================================ 5 · tahliye (ortak): R + L -> T (2110, 1140) -> sicak gaz tavasi
a_L = ic("L")[2]
YENI += [("TOPPING_MODUL__silikon", "evap_tahliye_R", boru([(XT_R, a_R, ZT_R), (XT_R, Y_TAH, ZT_R), (2110.0, Y_TAH, ZT_R), (2110.0, 945.0, ZT_R)], RT), SOG),
         ("TOPPING_MODUL__silikon", "evap_tahliye_L", boru([(XT_L, a_L, ZT_L), (XT_L, Y_TAH, ZT_L), (2110.0, Y_TAH, ZT_L), (2110.0, Y_TAH, ZT_R + RT)], RT), SOG),
         ("TOPPING_MODUL__silikon", "evap_tahliye_birlestirme_T", Kb(2110.0 - 8.0, 2110.0 + 8.0, Y_TAH - 8.0, Y_TAH + 8.0, ZT_R - 8.0, ZT_R + 8.0), SOG)]
# ================================================================ 6 · kablolar
FL, FR = KAS["L"]["fan"], KAS["R"]["fan"]
YENI += [("ELK_TOPPING__kablo", "kablo_TOPPING_evap_fani_R", boru([(FR[0], FR[1] + 60.0, Z_FAN), (FR[0], Y_PANO, Z_FAN)], 2.5), ELK),       # fan cercevesi ust kenarindan
         ("ELK_TOPPING__kablo", "kablo_TOPPING_evap_fani_L", boru([(FL[0] + 60.0, FL[1], Z_FAN), (X_SERIT, FL[1], Z_FAN), (X_SERIT, Y_PANO, Z_FAN)], 2.5), ELK),
]
for i in range(4):
    x = 2286.0 + 33.0 * i; ly = 1690.0 - 8.0 * i
    YENI.append(("ELK_TOPPING__kablo", "kablo_TOPPING_motor_surucu_%d" % i, boru([(x, 1723.0, -699.65), (x, 1723.0, -684.0), (x, ly, -684.0), (x, ly, -808.0), (2421.0, ly, -808.0)], 3.0), MK[:2] if MK else ELK))
    YENI.append(("ELK_TOPPING__kablo", "kablo_TOPPING_surucu_%d_pano" % i, boru([(x, 1745.0, -729.9), (x, 1765.0, -729.9), (x, 1765.0, -808.0), (x, Y_KD2, -808.0)], 4.2), MK[:2] if MK else ELK))
for nd, ad, s, (kt, mk) in YENI:
    n = ekle_kati(G, nd, [s], kt, mk, False)
    log("YENI %-24s %-40s %s  %d" % (nd.replace("TOPPING_MODUL__", ""), ad, [round(v, 1) for v in bb(s)], n))
KT = KLF[:2] if KLF else ELK
ekle_ucgen(G, "ELK_TOPPING__kablo", tup([(1700.0, 1087.0, Z_KLF), (1700.0, Y_TAH, Z_KLF), (X_SERIT, Y_TAH, Z_KLF), (X_SERIT, Y_PANO, Z_KLF)], 4.05, 16), KT[0], KT[1], False)
log("YENI kablo_TOPPING_sogutma_grubu_KLF66 (tup) x 1700 -> 1684, y 1087 -> 1879.8")
# ================================================================ 7 · fanlar + L fan rakoru
for k, (fx, fy) in (("R", FR), ("L", FL)):
    d = np.array([fx - 1860.5, fy - 1493.5, 0.0])
    for Pw, (kt, mk, kp) in FAN: ekle_ucgen(G, "TOPPING_MODUL__motor", Pw + d, kt, mk, kp)
    log("FAN", k, d)
c_old = np.array([1860.5, 1814.5, -713.85]); c_new = np.array([KAS["L"]["x"][1] - W / 2, KAS["L"]["fan"][1], -713.85])
for Pw, (kt, mk, kp) in RAK:
    v = Pw - c_old; Q = np.stack([v[..., 1], -v[..., 0], v[..., 2]], -1) + c_new
    ekle_ucgen(G, "ELK_TOPPING__rakor", Q, kt, mk, kp)
log("RAKOR L sag duvar", c_new)
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
