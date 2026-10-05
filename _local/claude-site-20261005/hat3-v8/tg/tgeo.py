# -*- coding: utf-8 -*-
"""TOPPING GÖVDESİ YENİ — GEOMETRİ (CadQuery, dünya mm: x hat · y yukarı · z koridora; ön +79, arka −830).
Kemal 2 Eki, 7 madde (67–73). Ayrıntı: topping_govde_yeni.py başlığı."""
import numpy as np
import cadquery as cq

V = cq.Vector
T_D, T_I, T_C = 1.5, 1.2, 1.0              # dış · iç · ön çerçeve (430)
X0, X1 = 1436.0, 2500.0
XI0, XI1 = X0 + T_D, X1 - T_D              # 1437,5 · 2498,5
YB, YT = 892.0, 2200.0
YBI, YTI = YB + T_D, YT - T_D              # 893,5 · 2198,5
ZA, ZAI = -830.0, -828.5
ZF = 39.0                                   # gövde ön düzlemi = kapak arkası
ZFC = ZF - T_C                              # 38 · çerçeve arkası = PU önü
Y_SO = 1109.0                               # soğuk oda alt sacı altı · kuru bölme tabanı üstü
Z_SA = -630.0                               # soğuk arka dış sacı arkası
LIN = (1495.0, 2441.0, 1110.5, 2141.0, -571.0)   # astar dış yüzleri (x0, x1, y0, ytop, z arka)
ACIK = (1496.0, 2440.0, 1152.0, 2140.0)          # soğuk oda ağzı (astar iç yüzleri · raf üstü)
YARIK_X = [(2030.5, 2093.5), (2279.5, 2342.5)]   # kaset dili kanalları (kaset ön dudağı 2031–2093 × 1143–1152 + 0,5 boşluk)
K1X, K2X = (1437.5, 1965.75), (1968.75, 2497.0) # kanatlar
KY0, KY1 = 788.0, 2197.0
ZK0, ZK1 = 39.0, 79.0


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(r, p0, p1):
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; L = float(np.linalg.norm(d))
    return cq.Solid.makeCylinder(r, L, V(*p0), V(*(d / L)))


def tekle(r):
    try: r = r.clean()
    except Exception: pass
    ss = r.Solids()
    return ss[0] if len(ss) == 1 else r


def kes(s, aletler):
    al = [a for a in aletler if a is not None]
    if not al: return s
    return tekle(s.cut(*al))


def yarik_alani(u0, u1, v0, v1, w0, w1, eksen, gen=5.0, boy=60.0, adim=12.0, satir_ara=20.0):
    """lazer yarık alanı (kesici kutular): eksen = sacın normali · eksen y → (u=x, v=z) · z → (u=x, v=y) · x → (u=z, v=y); yarık v yönünde uzun"""
    out = []
    n = int((u1 - u0 - gen) // adim) + 1
    bas = u0 + ((u1 - u0) - ((n - 1) * adim + gen)) / 2 + gen / 2
    uu = [bas + i * adim for i in range(n)]
    nsat = max(1, int((v1 - v0 + satir_ara) // (boy + satir_ara)))
    toplam = nsat * boy + (nsat - 1) * satir_ara; vb = v0 + (v1 - v0 - toplam) / 2
    for j in range(nsat):
        va = vb + j * (boy + satir_ara)
        for u in uu:
            if eksen == "y": out.append(kutu(u - gen / 2, u + gen / 2, w0, w1, va, va + boy))
            elif eksen == "z": out.append(kutu(u - gen / 2, u + gen / 2, va, va + boy, w0, w1))
            else: out.append(kutu(w0, w1, va, va + boy, u - gen / 2, u + gen / 2))
    return out


def boru(noktalar, r):
    """kablo / hortum: ortogonal çoklu çizgi · köşeler küre"""
    P = [np.array(p, float) for p in noktalar]
    s = None
    for a, b in zip(P[:-1], P[1:]):
        if np.linalg.norm(b - a) < 1e-6: continue
        c = silindir(r, a, b); s = c if s is None else s.fuse(c)
    for p in P[1:-1]:
        s = s.fuse(cq.Solid.makeSphere(r, V(*p), angleDegrees1=-90, angleDegrees2=90))
    return tekle(s)


def _bb(s):
    b = s.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def _kesisir_bb(a, b, e=0.01):
    return a[0] < b[1] - e and b[0] < a[1] - e and a[2] < b[3] - e and b[2] < a[3] - e and a[4] < b[5] - e and b[4] < a[5] - e


# ======================================================================================= SOĞUTMA GRUBU CEBİ (kaide C 3. gözü)
CEP = (1629.5, 2093.5, -788.5, -477.5)      # dış ölçü x0, x1, z0, z1 (kaide plaka kesiği 1628–2095 × −790…−477 içinde)
Y_CEP = 806.0                                # cep tabanı altı
AV = [(1658.0, -760.0), (1988.0, -760.0), (1658.0, -503.0), (1988.0, -503.0)]


# ======================================================================================= DIŞ KABUK
def dis_kabuk():
    S = {}
    sol = [kutu(X0 - 1, XI0 + 1, YBI, 1042.0, -510.0, 5.0), kutu(X0 - 1, XI0 + 1, 2142.0, 2167.5, -827.0, -765.0)]
    sol += [silindir(8.2, (X0 - 1, yc, -720.1), (XI0 + 1, yc, -720.1)) for yc in (1612.0, 1640.0)]
    sag = [kutu(XI1 - 1, X1 + 1, YBI, 1042.0, -510.0, 5.0), kutu(XI1 - 1, X1 + 1, 2104.0, 2169.0, -827.0, -689.0),
           silindir(8.2, (XI1 - 1, 1121.5, -799.9), (X1 + 1, 1121.5, -799.9)), silindir(6.95, (XI1 - 1, 1809.0, -739.9), (X1 + 1, 1809.0, -739.9))]
    S["dis_yan_sol"] = kes(kutu(X0, XI0, YB, YTI, ZA, ZF), sol)
    S["dis_yan_sag"] = kes(kutu(XI1, X1, YB, YTI, ZA, ZF), sag)
    ust = yarik_alani(1470.0, 2465.0, -815.0, -645.0, YTI - 1, YT + 1, "y", gen=5.0, boy=70.0, adim=12.0, satir_ara=24.0)
    S["dis_tavan"] = kes(kutu(X0, X1, YTI, YT, ZA, ZF), ust)
    S["dis_arka"] = kes(kutu(XI0, XI1, YBI, YTI, ZA, ZAI), [kutu(1447.0, 1624.5, 905.0, 1099.5, ZA - 1, ZAI + 1)])
    al = yarik_alani(1481.0, 1614.0, -785.0, -480.5, YB - 1, YBI + 1, "y")
    al += yarik_alani(2145.0, 2415.0, -785.0, -480.5, YB - 1, YBI + 1, "y")
    al += [kutu(CEP[0], CEP[1], YB - 1, YBI + 1, CEP[2], CEP[3]), kutu(2419.5, 2451.0, YB - 1, YBI + 1, -699.5, -558.5)]
    S["dis_taban"] = kes(kutu(XI0, XI1, YB, YBI, ZAI, ZF), al)
    return S


def cep():
    S, A = {}, {}
    x0, x1, z0, z1 = CEP
    yt = Y_CEP + T_D
    S["cep_tabani"] = kutu(x0, x1, Y_CEP, yt, z0, z1)
    S["cep_arka_duvar"] = kutu(x0 + T_D, x1 - T_D, yt, YBI, z0, z0 + T_D)
    S["cep_on_duvar"] = kutu(x0 + T_D, x1 - T_D, yt, YBI, z1 - T_D, z1)
    S["cep_sag_duvar"] = kutu(x1 - T_D, x1, yt, YBI, z0, z1)
    sl = yarik_alani(z0 + 15.0, z1 - 15.0, 815.0, 885.0, x0 - 1, x0 + T_D + 1, "x", gen=5.0, boy=62.0, adim=12.0)
    sol = kes(kutu(x0, x0 + T_D, yt, YBI, z0, z1), sl).fuse(kutu(x0, x0 + T_D, YBI, Y_SO, ZAI, -476.5))
    sol = sol.cut(kutu(x0 - 1, x0 + T_D + 1, Y_SO - T_D, Y_SO + 1, ZAI - 1, Z_SA))                 # kuru bölme tabanı üstte (tabana dayanır)
    S["cep_sol_duvar_ayirma_perdesi"] = tekle(sol)
    for i, (x, z) in enumerate(AV):
        A["sogutma_grubu_titresim_takozu_%d" % i] = silindir(20.0, (x, yt, z), (x, 815.0, z))
    return S, A


def teknik():
    S = {}
    S["teknik_bolme_on_perdesi"] = kutu(XI0, 2420.0, 953.5, Y_SO, -476.5, -475.0)
    S["teknik_bolme_sag_perdesi"] = kes(kutu(2418.5, 2420.0, YBI, Y_SO, ZAI, -476.5), [kutu(2417.0, 2421.0, Y_SO - T_D, Y_SO + 1, ZAI - 1, Z_SA)])
    d = [silindir(8.2, (1700.0, Y_SO - 2, -804.9), (1700.0, Y_SO + 2, -804.9)),
         silindir(7.0, (2110.0, Y_SO - 2, -760.0), (2110.0, Y_SO + 2, -760.0)),
         silindir(4.2, (2236.0, Y_SO - 2, -659.9), (2236.0, Y_SO + 2, -659.9)),
         silindir(16.4, (2258.0, Y_SO - 2, -699.75), (2258.0, Y_SO + 2, -699.75))]
    S["kuru_bolme_tabani"] = kes(kutu(XI0, 2420.0, Y_SO - T_D, Y_SO, ZAI, Z_SA), d)
    return S


# ======================================================================================= MENTEŞE / BAS-AÇ + ÖN ÇERÇEVE
MENTESE_Y = [(893.5, 963.5), (1500.0, 1570.0), (2060.0, 2130.0)]
MENTESE_X = {"K1": (1437.5, 1465.0), "K2": (2471.0, 2498.5)}          # gövde yarısı yan sacın iç yüzüne dayalı
MENTESE_XK = {"K1": (1439.0, 1465.0), "K2": (2471.0, 2495.5)}         # kanat yarısı kanat dönüşüne dayalı
BASAC = {"K1": (1927.0, 1957.0), "K2": (1977.0, 2007.0)}
BASAC_Y = (2160.0, 2190.0)


def menteseler():
    G, K = {}, {}
    for kn, (x0, x1) in MENTESE_X.items():
        for i, (y0, y1) in enumerate(MENTESE_Y):
            G["onyuz_%s_mentese_govde_%d" % (kn, i)] = kutu(x0, x1, y0, y1, 26.0, ZF)
            xa, xb = MENTESE_XK[kn]
            K["onyuz_%s_mentese_kanat_%d" % (kn, i)] = kutu(xa, xb, max(y0, KY0 + 1.5), y1, ZF, 62.0)
    for kn, (x0, x1) in BASAC.items():
        G["onyuz_basac_govde_%s" % kn] = kutu(x0, x1, BASAC_Y[0], BASAC_Y[1], 26.0, ZF)
        K["onyuz_basac_karsilik_%s" % kn] = kutu(x0, x1, BASAC_Y[0], BASAC_Y[1], ZF, 42.0)
    return G, K


def on_cerceve(G):
    ac = [kutu(ACIK[0], ACIK[1], ACIK[2], ACIK[3], ZFC - 1, ZF + 1), kutu(1467.5, 2468.5, YBI - 1, Y_SO, ZFC - 1, ZF + 1)]
    ac += [kutu(a, b, 1142.5, ACIK[2] + 1, ZFC - 1, ZF + 1) for a, b in YARIK_X]
    ac += [kutu(*_bb(g)[:4], ZFC - 1, ZF + 1) for g in G.values()]
    return kes(kutu(XI0, XI1, YBI, YTI, ZFC, ZF), ac)


def pu_duvar(gomulu):
    s = kutu(XI0, XI1, LIN[2], YTI, Z_SA + T_D, ZFC).cut(kutu(LIN[0], LIN[1], LIN[2] - 1, LIN[3], LIN[4], ZFC + 1))
    bas = []
    for g in gomulu or []:
        try:
            if not g.isValid(): raise ValueError("geçersiz")
            r = s.cut(g)
            if r.isNull() or r.Volume() <= 0: raise ValueError("boş")
            s = tekle(r)
        except Exception as e:
            b = _bb(g); s = tekle(s.cut(kutu(*b))); bas.append(("kutu", b, str(e)))
    pu_duvar.bas = bas
    return s


# ======================================================================================= KANATLAR
def _fitil(kn):
    x0, x1 = (1481.5, 1961.8) if kn == "K1" else (1971.0, 2454.5)
    y0, y1, w, d = 1121.5, 2154.5, 16.0, 4.0
    return tekle(kutu(x0, x1, y0, y1, ZK0, ZK0 + d).cut(kutu(x0 + w, x1 - w, y0 + w, y1 - w, ZK0 - 1, ZK0 + d + 1)))


def kanat(kn, cepler):
    x0, x1 = K1X if kn == "K1" else K2X
    y0, y1, z0, z1 = KY0, KY1, ZK0, ZK1
    t, ti = T_D, 1.0
    out = {}
    dis = kutu(x0, x1, y0, y1, z1 - t, z1)
    dis = dis.fuse(kutu(x0, x0 + t, y0, y1, z0, z1 - t), kutu(x1 - t, x1, y0, y1, z0, z1 - t),
                   kutu(x0 + t, x1 - t, y0, y0 + t, z0, z1 - t), kutu(x0 + t, x1 - t, y1 - t, y1, z0, z1 - t))
    dis = tekle(dis)
    ic = kutu(x0 + t, x1 - t, y0 + t, y1 - t, z0, z0 + ti)
    yar = []
    for a, b in [(1490.0, 1610.0), (1634.0, 2086.0), (2154.0, 2446.0)]:
        a, b = max(a, x0 + 8.0), min(b, x1 - 8.0)
        if b - a > 20: yar += yarik_alani(a, b, 803.0, 863.0, z0 - 1, z1 + 1, "z")
    perde = kutu(x0 + t, x1 - t, Y_SO - T_D, Y_SO, z0 + ti, z1 - t)
    pu = kutu(x0 + t, x1 - t, Y_SO, y1 - t, z0 + ti, z1 - t)
    fitil = _fitil(kn)
    kc = [f for f in cepler if _kesisir_bb(_bb(f), (x0, x1, y0, y1, z0, z1))]
    out["onyuz_%s_dis_tava" % kn] = kes(dis, yar + kc)
    out["onyuz_%s_ic_tava" % kn] = kes(ic, yar + kc + [fitil])
    out["onyuz_%s_kopuk_perdesi" % kn] = kes(perde, kc)
    out["onyuz_%s_pu" % kn] = kes(pu, kc + [fitil])
    out["onyuz_%s_fitil" % kn] = fitil
    if kn == "K1":
        out["onyuz_K1_emis_filtresi"] = kutu(1492.0, 1608.0, 798.0, 868.0, z0 + ti, z0 + ti + 8.0)
    return out


# ======================================================================================= KURU BÖLME DÜZENİ (madde 7)
SUR = [("sucuk_rotor", 0, (2311.0, 1265.5, -807.0), 1581.0), ("sucuk_helezon", 1, (2311.0, 1161.5, -807.0), 1548.0),
       ("kasar_rotor", 2, (2062.0, 1296.5, -807.0), 1515.0), ("kasar_helezon", 3, (2062.0, 1141.5, -807.0), 1482.0)]
KD3 = (1470.0, 2360.0, 1240.0, 1270.0, -798.0, -768.0)


def kuru_duzen():
    K, C, R, H = {}, {}, {}, {}
    x0, x1, y0, y1, z0, z1 = KD3
    t = 1.5
    kan = kutu(x0, x1, y0, y1, z0, z1).cut(kutu(x0 - 1, x1 + 1, y0 + t, y1 - t, z0 + t, z1 - t))
    giris = [silindir(4.5, (2311.0, 1255.0, z0 - 1), (2311.0, 1255.0, z0 + t + 1))]
    giris += [silindir(4.0, (x, y0 - 1, -782.0), (x, y0 + t + 1, -782.0)) for x in (2125.0, 2350.0)]
    giris += [silindir(4.0, (x, y1 - t - 1, -782.0), (x, y1 + 1, -782.0)) for x in (2062.0, 1482.0, 1515.0, 1548.0, 1581.0)]
    R["kanal_TOPPING_KD3_motor"] = kes(kan, giris)
    for i, xb in enumerate((1500.0, 1950.0, 2330.0)):
        C["kanal_TOPPING_KD3_braket_%d" % i] = kutu(xb - 5.0, xb + 5.0, 1245.0, 1265.0, ZAI, z0)
    r = 3.0
    for nm, i, S, xs in SUR:
        sx, sy, sz = S
        if nm == "sucuk_rotor":
            P = [S, (sx, 1255.0, sz), (sx, 1255.0, z0)]
        elif nm == "sucuk_helezon":
            P = [S, (sx, 1150.0, sz), (sx, 1150.0, -782.0), (2350.0, 1150.0, -782.0), (2350.0, y0, -782.0)]
        elif nm == "kasar_rotor":
            P = [S, (sx, 1285.0, sz), (sx, 1285.0, -782.0), (sx, y1, -782.0)]
        else:
            P = [S, (sx, 1130.0, sz), (sx, 1130.0, -782.0), (2125.0, 1130.0, -782.0), (2125.0, y0, -782.0)]
        K["kablo_TOPPING_motor_%s_surucu_%d" % (nm, i)] = boru(P, r)
        K["kablo_TOPPING_motor_%s_surucu_%d_surucu_ucu" % (nm, i)] = boru(
            [(xs, y1, -782.0), (xs, 1420.0, -782.0), (xs, 1420.0, -684.0), (xs, 1452.0, -684.0), (xs, 1452.0, -699.5)], r)
    K["kablo_TOPPING_sogutma_grubu_KLF66"] = boru([(1700.0, 1087.0, -804.9), (1700.0, 1300.0, -804.9), (1670.0, 1300.0, -804.9),
                                                   (1670.0, 1879.8, -804.9)], 4.05)
    for i, yk in enumerate((1500.0, 1800.0)):
        kl = kutu(1666.0, 1674.0, yk - 6.0, yk + 6.0, ZAI, -809.5).fuse(
            kutu(1665.4, 1674.6, yk - 6.0, yk + 6.0, -810.0, -799.0).cut(silindir(4.15, (1670.0, yk - 7, -804.9), (1670.0, yk + 7, -804.9))))
        C["kablo_TOPPING_sogutma_grubu_KLF66_kelepce_%d" % i] = tekle(kl)
    H["evap_kaseti_tahliye_hortumu"] = boru([(2101.0, 1425.0, -775.0), (2101.0, 1370.0, -775.0), (2110.0, 1370.0, -775.0),
                                             (2110.0, 1370.0, -760.0), (2110.0, 945.0, -760.0)], 5.0)
    return K, C, R, H


# ======================================================================================= EVAPORATÖR PENCERESİ TAPASI (soğuk oda arka duvarı, madde 1 + 3)
PEN = [(1698.0, 2194.0, 1405.0, 1507.5), (1698.0, 2123.0, 1507.5, 1743.0)]     # eski astar / arka sac penceresi (iki dikdörtgen)
KAN = [(1726.0, 2106.0, 1450.0, 1572.0), (1726.0, 2106.0, 1592.0, 1702.0)]     # dönüş (alt) · üfleme (üst) hava kanalları (dış)
AGIZ = [(1729.0, 2103.0, 1453.0, 1569.0), (1729.0, 2103.0, 1595.0, 1699.0)]    # kanal ağızları (eski ızgara yerleri)
ZP0, ZP1 = -628.5, -571.2


def pencere_prizma(z0, z1):
    a = kutu(PEN[0][0], PEN[0][1], PEN[0][2], PEN[0][3], z0, z1)
    return tekle(a.fuse(kutu(PEN[1][0], PEN[1][1], PEN[1][2], PEN[1][3], z0, z1)))


def evap_penceresi():
    S, P = {}, {}
    yar = []
    for x0, x1, y0, y1 in AGIZ:
        yar += yarik_alani(x0 + 2.0, x1 - 2.0, y0 + 4.0, y1 - 4.0, ZP1 - 1, -569.0, "z", gen=6.0, boy=y1 - y0 - 8.0, adim=12.0)
    on = kes(pencere_prizma(ZP1, -570.0), yar)
    S["evap_penceresi_on_sac_lazer_yarik"] = on
    S["evap_penceresi_arka_sac"] = kes(pencere_prizma(-630.0, ZP0), [kutu(x0, x1, y0, y1, -631.0, ZP0 + 1) for x0, x1, y0, y1 in KAN])
    for i, (x0, x1, y0, y1) in enumerate(KAN):
        S["evap_hava_kanali_kovani_%s" % ("donus_alt" if i == 0 else "ufleme_ust")] = tekle(
            kutu(x0, x1, y0, y1, ZP0, ZP1).cut(kutu(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, ZP0 - 1, ZP1 + 1)))
    P["evap_penceresi_PU"] = kes(pencere_prizma(ZP0, ZP1), [kutu(x0, x1, y0, y1, ZP0 - 1, ZP1 + 1) for x0, x1, y0, y1 in KAN])
    return S, P


# ======================================================================================= SOĞUK ODA TABANI GEÇİŞ KOVANLARI (alt PU deliklerinin çeperi, 304 1,0)
def _rect_birlesim(rs, e=0.0, y0=1110.5, y1=1149.0):
    s = None
    for x0, x1, z0, z1 in rs:
        b = kutu(x0 - e, x1 + e, y0, y1, z0 - e, z1 + e); s = b if s is None else s.fuse(b)
    return tekle(s)


TABAN_GECIS = {"kiyma": [(1577.0, 1615.0, -189.0, -151.0)], "kusbasi": [(1787.0, 1825.0, -189.0, -151.0)],
               "kasar": [(2023.0, 2101.0, -161.0, -139.0), (2029.0, 2095.0, -182.5, -117.0)],
               "sucuk": [(2272.0, 2350.0, -161.0, -139.0), (2278.0, 2344.0, -182.5, -117.0)]}
TABAN_YUVARLAK = {"sos": (1644.75, -169.75, 15.25), "harc": (2190.0, -169.5, 15.5)}


def taban_kovanlari():
    S, D = {}, []
    for k, rs in TABAN_GECIS.items():
        e = 2.0 if k in ("kiyma", "kusbasi") else 1.0                 # kıyma / kuşbaşı: raf deliği ağızdan 1,85 geniş → kovan çeperi 2,0
        dis = _rect_birlesim(rs, e); ic = _rect_birlesim(rs, 0.0, 1109.0, 1151.0)
        S["soguk_taban_gecis_kovani_%s" % k] = tekle(dis.cut(ic)); D.append(dis)
    for k, (x, z, r) in TABAN_YUVARLAK.items():
        dis = silindir(r + 1.0, (x, 1110.5, z), (x, 1149.0, z))
        S["soguk_taban_gecis_kovani_%s" % k] = tekle(dis.cut(silindir(r, (x, 1109.0, z), (x, 1151.0, z)))); D.append(dis)
    return S, D


# ======================================================================================= SOĞUK ODA ÖN EŞİĞİ (raf önü z 23 → 38: kapağa kadar yalıtım, madde 1)
ZE0, ZE1 = 23.0, 38.0


def esik():
    S, P = {}, {}
    t = T_I
    ust = kutu(ACIK[0], ACIK[1], 1152.0 - t, 1152.0, ZE0, ZE1 - t)
    on = kutu(ACIK[0], ACIK[1], LIN[2], 1152.0, ZE1 - t, ZE1)
    pu = kutu(ACIK[0], ACIK[1], LIN[2], 1152.0 - t, ZE0, ZE1 - t)
    oyuk = [kutu(a, b, 1142.5, 1153.0, ZE0 - 1, ZE1 + 1) for a, b in YARIK_X]
    dis = [kutu(a - 1.0, b + 1.0, 1141.5, 1153.0, ZE0 - 1, ZE1 + 1) for a, b in YARIK_X]
    S["soguk_esik_ust_sac"] = kes(ust, dis)
    S["soguk_esik_on_sac"] = kes(on, oyuk + [kutu(a - 1.0, b + 1.0, 1141.5, 1153.0, ZE1 - t - 1, ZE1 + 1) for a, b in YARIK_X])
    P["soguk_esik_PU"] = kes(pu, dis)
    for (a, b), nm in zip(YARIK_X, ("kasar", "sucuk")):
        S["soguk_esik_dil_kanali_%s" % nm] = tekle(kutu(a - 1.0, b + 1.0, 1141.5, 1152.0 - t, ZE0, ZE1).cut(kutu(a, b, 1142.5, 1153.0, ZE0 - 1, ZE1 + 1)))
    # raf altındaki dil kanalı tabanı (eski alt PU çentiği 1143'te açıktı; dil 1144'te → 1 mm hava) · z −117 … 20 (20–23 arası raf bükümü çentiği)
    for (a, b), nm in zip([(2032.0, 2092.0), (2281.0, 2341.0)], ("kasar", "sucuk")):
        S["soguk_raf_dil_kanali_tabani_%s" % nm] = kutu(a, b, 1143.0, 1144.0, -116.0, 20.0)   # dil bu sacın üstünde kayar
    return S, P
