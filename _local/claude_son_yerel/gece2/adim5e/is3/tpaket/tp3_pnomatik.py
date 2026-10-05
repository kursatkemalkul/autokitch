# -*- coding: utf-8 -*-
"""TP3 · PNOMATIK: yayici (spreader) kesme valfi aktuatorleri + valf adasindan 12 hortum (rakor, dik acili yol, kelepce).
 - harc / sos yayicisindaki yer tutucu POM govde + kapak + siyah rakor + ince valf braketi silinir
 - yerine SMC CRB2BW10-90S kanatli doner aktuator (govde O29 x 15, on mil O4 D=14, arka mil C=8, yan port M5 x 2) + kaplin (valf mili <-> aktuator mili)
   + 3 mm on montaj plakasi (3-M3, P 24) ve plakadan giris kelepcesine L kol
 - 8 UNO hortumu (eski yollar korunur, harc seridi x 1684'e alinir) + 4 yayici hortumu (harc: ada alt yuzu x 1745 -> duvar gecis kovani x 1745;
   sos: ada sag yuzu -> x 2239 -> duvar gecis kovani x 2239) · her uca itmeli rakor · uzun duz parcalara P-kelepce + yapiya dil
python tp3_pnomatik.py giris.glb cikis.glb"""
import os, sys, numpy as np
TPD = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(TPD)
gi, go = [os.path.abspath(a) for a in sys.argv[1:3]]
sys.path.insert(0, os.path.join(S, "topfix")); sys.path.insert(0, TPD)
from tlib import *
from m8kit import Yuzey, silindir_ucgen
import tgeo as TG
from tp_olcu import *
Kb, S_, kes, tekle, bb, boru = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb, TG.boru
G = Glb(gi)
HAVA = kat_no(G, "HAVA")
MH, MHAR, MSOS = mek_no(G, "TOPPING/Hava"), mek_no(G, "TOPPING/Harç"), mek_no(G, "TOPPING/Sos")
# ================================================================ 1 · silinenler
for K in ((1587.4, 1595.6, 1209.4, 1214.6, -692.1, -683.9), (1588.4, 1703.1, 1214.4, 1250.1, -691.1, -684.9), (1597.4, 1605.6, 1209.4, 1214.6, -799.1, -790.9),
          (1598.4, 1713.1, 1214.4, 1250.1, -798.1, -746.9), (1674.9, 1728.1, 1286.9, 1658.1, -798.1, -678.9), (1682.9, 1722.1, 1271.9, 1651.1, -691.1, -666.9),
          (1714.9, 1723.1, 1632.4, 1637.6, -692.1, -683.9), (1720.9, 1729.1, 1632.4, 1637.6, -799.1, -790.9), (1839.4, 1847.6, 1209.4, 1214.6, -692.1, -683.9),
          (1840.4, 1846.6, 1214.4, 1250.1, -691.1, -684.9), (1849.4, 1857.6, 1209.4, 1214.6, -799.1, -790.9), (1850.4, 1856.6, 1214.4, 1250.1, -798.1, -746.9),
          (1997.9, 2310.1, 1261.9, 1658.1, -798.1, -672.9), (1997.9, 2300.1, 1298.9, 1651.1, -691.1, -666.9), (2252.4, 2260.6, 1632.4, 1637.6, -692.1, -683.9),
          (2258.4, 2266.6, 1632.4, 1637.6, -799.1, -790.9)):
    sil_tri(G, "TOPPING_MODUL__hava_ana", K, not_="eski hortum / port blogu")
for nm, xc in (("harc", 1722.0), ("sos", 2259.5)):
    sil_tri(G, "TOPPING_MODUL__pom", (xc - 15.0, xc + 15.0, 1161.9, 1216.1, -145.1, -115.3), not_="%s yer tutucu govde + kapak" % nm)
    sil_tri(G, "TOPPING_MODUL__siyah", (xc - 26.1, xc + 26.1, 1193.9, 1202.1, -134.1, -126.0), not_="%s yer tutucu hava rakoru" % nm)
    sil_tri(G, "TOPPING_MODUL__paslanmaz", (xc - 2.1, xc + 2.1, 1184.4, 1203.6, -151.6, -129.9), not_="%s ince valf braketi" % nm)
# ================================================================ 2 · aktuator (SMC CRB2BW10-90S) + kaplin + montaj
YENI = []
for nm, d in SPR.items():
    xc = d["x"]; mk = MHAR if nm == "harc" else MSOS; yc = SPR_Y; zf, zb = SPR_ZF, SPR_ZB
    govde = S_(14.5, (xc, yc, zb), (xc, yc, zf))
    YENI += [("TOPPING_MODUL__aluminyum", "%s_spreader_aktuator_CRB2BW10_govde" % nm, govde, (HAVA, mk)),
             ("TOPPING_MODUL__celik", "%s_spreader_aktuator_on_gobek_O9" % nm, S_(4.5, (xc, yc, zf), (xc, yc, zf - 3.0)), (HAVA, mk)),
             ("TOPPING_MODUL__celik", "%s_spreader_aktuator_on_mil_O4" % nm, S_(2.0, (xc, yc, zf - 3.0), (xc, yc, zf - 14.0)), (HAVA, mk)),
             ("TOPPING_MODUL__celik", "%s_spreader_aktuator_arka_gobek" % nm, S_(4.5, (xc, yc, zb), (xc, yc, zb + 1.0)), (HAVA, mk)),
             ("TOPPING_MODUL__celik", "%s_spreader_aktuator_arka_mil" % nm, S_(2.0, (xc, yc, zb + 1.0), (xc, yc, zb + 8.0)), (HAVA, mk)),
             ("TOPPING_MODUL__paslanmaz", "%s_spreader_kaplin_O12" % nm, S_(6.0, (xc, yc, -149.0), (xc, yc, -137.0)), (HAVA, mk))]
    plaka = kes(Kb(xc - 14.5, xc + 14.5, yc - 14.5, yc + 14.5, zf - 3.0, zf), [S_(5.0, (xc, yc, zf - 4), (xc, yc, zf + 1))] +
                [S_(1.7, (xc + 12 * np.cos(a), yc + 12 * np.sin(a), zf - 4), (xc + 12 * np.cos(a), yc + 12 * np.sin(a), zf + 1)) for a in np.radians([90, 210, 330])])
    kx0, kx1 = (xc - 3.5, xc + 6.5) if nm == "sos" else (xc - 6.5, xc + 3.5)      # kol port rakorunun karsi tarafinda
    kol = Kb(kx0, kx1, yc + 14.5, yc + 17.5, -145.7, zf - 3.0)
    YENI += [("TOPPING_MODUL__paslanmaz", "%s_spreader_aktuator_montaj_plakasi" % nm, plaka, (HAVA, mk)),
             ("TOPPING_MODUL__paslanmaz", "%s_spreader_aktuator_montaj_kolu" % nm, kol, (HAVA, mk))]
    for a in np.radians([90, 210, 330]):
        p = (xc + 12 * np.cos(a), yc + 12 * np.sin(a))
        YENI.append(("TOPPING_MODUL__celik", "%s_spreader_aktuator_M3_vida" % nm, S_(2.75, (p[0], p[1], zf - 3.0), (p[0], p[1], zf - 5.0)), (HAVA, mk)))
# ================================================================ 3 · hortum yollari
R_H = 3.0
UST_A, UST_U = 1209.5, 1632.5          # alt / ust UNO silindir port ust yuzu


def port_ucu(x, y_ust, z):
    """silindir ustu itmeli rakor (M5 -> O6): govde 8 x 5 x 8 + kilit halkasi"""
    return [kutu_ucgen([x - 4, y_ust, z - 4], [x + 4, y_ust + 5.0, z + 4]), silindir_ucgen((x, y_ust + 5.0, z), (x, y_ust + 8.0, z), 4.5, 16)]


H = {}
H["kiyma_on"] = [(1700, 1240, -688), (1700, 1225, -688), (1591.5, 1225, -688), (1591.5, UST_A + 8, -688)]
H["kiyma_arka"] = [(1710, 1240, -750), (1710, 1225, -750), (1710, 1225, -795), (1601.5, 1225, -795), (1601.5, UST_A + 8, -795)]
H["kusbasi_on"] = [(1843.5, 1240, -688), (1843.5, UST_A + 8, -688)]
H["kusbasi_arka"] = [(1853.5, 1240, -750), (1853.5, 1225, -750), (1853.5, 1225, -795), (1853.5, UST_A + 8, -795)]
H["harc_on"] = [(X_SERIT, 1283, -670), (X_SERIT, 1648, -670), (1719, 1648, -670), (1719, 1648, -688), (1719, UST_U + 8, -688)]
H["harc_arka"] = [(X_SERIT, 1298, -682), (X_SERIT, 1658, -682), (1725, 1658, -682), (1725, 1658, -795), (1725, UST_U + 8, -795)]
H["sos_on"] = [(2008, 1302, -670), (2297, 1302, -670), (2297, 1648, -670), (2256.5, 1648, -670), (2256.5, 1648, -688), (2256.5, UST_U + 8, -688)]
H["sos_arka"] = [(2008, 1265, -676), (2307, 1265, -676), (2307, 1658, -676), (2262.5, 1658, -676), (2262.5, 1658, -795), (2262.5, UST_U + 8, -795)]
# yayici: aktuator portlari (yan, M5, arka yuzden 5 mm, iki port arasi 25) -> 8 mm duz rakor -> serit
ZP = SPR_ZB - 5.0
SPR_UC = {}
for nm, d in SPR.items():
    sg = d["port_yon"]; xc = d["x"]; sx = d["serit_x"]
    for k, sy in (("A", -1), ("B", +1)):
        pp = np.array([xc + sg * 7.35, SPR_Y + sy * 12.5, ZP]); dr = np.array([sg * 7.35, sy * 12.5, 0.0]) / 14.5
        SPR_UC[(nm, k)] = (pp, pp + 8.0 * dr)
for nm in ("harc", "sos"):
    sx = SPR[nm]["serit_x"]
    (pa, oa), (pb, ob) = SPR_UC[(nm, "A")], SPR_UC[(nm, "B")]
    soguk_A = [tuple(oa), (sx, oa[1], ZP), (sx, Y_HAT_A, ZP), (sx, Y_HAT_A, -630.0)]
    soguk_B = [tuple(ob), (ob[0], ob[1], ZP - 12.0), (sx, ob[1], ZP - 12.0), (sx, Y_HAT_B, ZP - 12.0), (sx, Y_HAT_B, -630.0)]
    if nm == "harc":
        H["harc_spreader_A"] = soguk_A + [(sx, Y_HAT_A, -750), (sx, 1240, -750)]
        H["harc_spreader_B"] = soguk_B + [(sx, Y_HAT_B, -688), (sx, 1240, -688)]
    else:
        # kuru taraf: sivi hatti (x 2236, z -660) ve emis yalitimi (x 2241-2273) arasindan kacmak icin z -645'te x 2228'e kayar; ada sag yuzune y 1278 (A z -750, B z -722)
        H["sos_spreader_A"] = soguk_A + [(sx, Y_HAT_A, -645), (2228.0, Y_HAT_A, -645), (2228.0, Y_HAT_A, -750), (2228.0, 1278, -750), (2008, 1278, -750)]
        H["sos_spreader_B"] = soguk_B + [(sx, Y_HAT_B, -645), (2228.0, Y_HAT_B, -645), (2228.0, Y_HAT_B, -722), (2228.0, 1278, -722), (2008, 1278, -722)]
# ================================================================ 4 · rakorlar (ada ucu: itmeli duz rakor O6, govde O10 x 10)
EK = []
def ada_rakoru(p, yon):
    p = np.array(p, float); yon = np.array(yon, float); q = p + 10.0 * yon
    return [silindir_ucgen(p, q, 5.0, 16)]
ADA = {"kiyma_on": (0, 1, 0), "kiyma_arka": (0, 1, 0), "kusbasi_on": (0, 1, 0), "kusbasi_arka": (0, 1, 0), "harc_spreader_A": (0, 1, 0), "harc_spreader_B": (0, 1, 0),
       "harc_on": (1, 0, 0), "harc_arka": (1, 0, 0), "sos_on": (-1, 0, 0), "sos_arka": (-1, 0, 0), "sos_spreader_A": (-1, 0, 0), "sos_spreader_B": (-1, 0, 0)}
for k, pts in H.items():
    if k.endswith("spreader_A") or k.endswith("spreader_B"):
        ada = pts[-1]; yon = ADA[k]
    else:
        ada = pts[0]; yon = ADA[k]
    if k in ("harc_on", "harc_arka"):        # dirsek rakor: ada sol yuzu (x 1690) -> x 1684 -> yukari
        y0 = ada[1] - 8.0; EK += [silindir_ucgen((1690.0, y0, ada[2]), (X_SERIT, y0, ada[2]), 5.0, 16), silindir_ucgen((X_SERIT, y0 - 5.0, ada[2]), (X_SERIT, y0 + 8.0, ada[2]), 5.0, 16)]
    else:
        EK += ada_rakoru(ada, yon)       # ada yuzunden hortum ucuna 10 mm
    if "spreader" not in k:
        x, y, z = pts[-1]; EK += port_ucu(x, (UST_A if y < 1400 else UST_U), z)
for (nm, k), (pp, oo) in SPR_UC.items():
    EK.append(silindir_ucgen(pp - 0.5 * (oo - pp) / 8.0, oo, 4.0, 16))     # M5 duz rakor (aktuator yan portu)
for T_ in EK: ekle_ucgen(G, "TOPPING_MODUL__hava_ana", T_, HAVA, MH, False)
for k, pts in H.items():
    ekle_ucgen(G, "TOPPING_MODUL__hava_ana", tup(pts, R_H, 12), HAVA, MH, False)
    log("hortum %-16s %s -> %s  %d nokta" % (k, pts[0], pts[-1], len(pts)))
for nd, ad, s, (kt, mk) in YENI:
    n = ekle_kati(G, nd, [s], kt, mk, False)
    log("YENI %-24s %-44s %s  %d" % (nd.replace("TOPPING_MODUL__", ""), ad, [round(v, 1) for v in bb(s)], n))
def halka(p0, p1, ri, ro, n=16):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); a = p1 - p0; a /= np.linalg.norm(a)
    u = np.cross(a, [1, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(a, u)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False); C = [np.cos(t) * u + np.sin(t) * w for t in th]; out = []
    for i in range(n):
        j = (i + 1) % n
        Ao, Bo, A1o, B1o = p0 + C[i] * ro, p0 + C[j] * ro, p1 + C[i] * ro, p1 + C[j] * ro
        Ai, Bi, A1i, B1i = p0 + C[i] * ri, p0 + C[j] * ri, p1 + C[i] * ri, p1 + C[j] * ri
        out += [(Ao, Bo, B1o), (Ao, B1o, A1o), (Ai, B1i, Bi), (Ai, A1i, B1i), (Ao, Ai, Bi), (Ao, Bi, Bo), (A1o, B1i, A1i), (A1o, B1o, B1i)]
    return np.array(out)


# ================================================================ 5 · P-kelepceler (>= 180 mm duz parca ortasi, en yakin yapi yuzeyine dil)
YS = Yuzey(G, haric=("ELK_ANA_HAT", "URUN", "INSAN"))
YAPI = r"__sac|__paslanmaz|__kanal|__aluminyum$|__celik$|__pom$"
import re
nk = 0
for k, pts in H.items():
    P = [np.array(p, float) for p in pts]
    for a, b in zip(P[:-1], P[1:]):
        L = np.linalg.norm(b - a)
        if L < 180.0: continue
        m = (a + b) / 2; ax = int(np.argmax(np.abs(b - a))); best = None
        sogukB = k.endswith("spreader_B") and ax == 2 and abs(a[1] - Y_HAT_B) < 0.1 and a[2] > -630
        sogukA = k.endswith("spreader_A") and ax == 2 and abs(a[1] - Y_HAT_A) < 0.1 and a[2] > -630
        if sogukB: continue
        if k.endswith("spreader") or (("spreader" in k) and a[1] > 1270 and b[1] > 1270): pass
        for d_ in range(3):
            if d_ == ax: continue
            for sg in (-1, 1):
                dv = np.zeros(3); dv[d_] = sg
                t = YS.isin(m + dv * 4.6, dv, 70.0, haric_ad=r"^(?!.*(__sac|__paslanmaz|__kanal))|PISTON|ARABA|ACICI|DONER")
                if t is not None and (best is None or t < best[0]): best = (t, dv)
        if best is None: log("   kelepce YOK (yapi > 70 mm)", k, a, b); continue
        t, dv = best
        u = [i for i in range(3) if i != ax]
        ring = halka(m - (b - a) / L * 4, m + (b - a) / L * 4, 3.05, 4.6)
        dil_lo = np.minimum(m + dv * 4.0, m + dv * (4.6 + t)); dil_hi = np.maximum(m + dv * 4.0, m + dv * (4.6 + t))
        w = [i for i in range(3) if i != ax and dv[i] == 0][0]
        dil_lo[ax] = m[ax] - 4.0; dil_hi[ax] = m[ax] + 4.0; dil_lo[w] = m[w] - 0.75; dil_hi[w] = m[w] + 0.75
        ekle_ucgen(G, "TOPPING_MODUL__celik", np.concatenate([ring, kutu_ucgen(dil_lo, dil_hi)]), HAVA, MH, False)
        if sogukA:     # cift kelepce: B hortumu (y 1169) ayni z'de, halkalar arasi dil
            mB = m.copy(); mB[1] = Y_HAT_B
            ekle_ucgen(G, "TOPPING_MODUL__celik", np.concatenate([halka(mB - np.array([0, 0, 4.0]), mB + np.array([0, 0, 4.0]), 3.05, 4.6),
                       kutu_ucgen([m[0] - 0.75, Y_HAT_A + 4.0, m[2] - 4.0], [m[0] + 0.75, Y_HAT_B - 4.0, m[2] + 4.0])]), HAVA, MH, False)
            log("   cift kelepce B", mB.round(1))
        nk += 1; log("   P-kelepce %-16s %s dil %s %.1f mm" % (k, m.round(1), dv, t))
# sos yayici hortumlari (ada -> x 2239, y 1285 / 1296): 70 mm icinde yapi yok -> KD3 on yuzune (z -768) percinli dik lama + 2 P-kelepce
for xk in (2100.0, 2190.0):
    lama = kutu_ucgen([xk - 10.0, 1250.0, -768.0], [xk + 10.0, 1284.0, -766.5])
    parca = [lama]
    parca.append(halka((xk - 4.0, 1278.0, -750.0), (xk + 4.0, 1278.0, -750.0), 3.05, 4.6))
    parca.append(kutu_ucgen([xk - 4.0, 1277.25, -766.5], [xk + 4.0, 1278.75, -754.0]))
    parca.append(halka((xk - 4.0, 1278.0, -722.0), (xk + 4.0, 1278.0, -722.0), 3.05, 4.6))
    parca.append(kutu_ucgen([xk - 4.0, 1277.25, -746.0], [xk + 4.0, 1278.75, -726.0]))
    for yr in (1256.0, 1264.0):
        parca.append(silindir_ucgen((xk, yr, -766.5), (xk, yr, -765.0), 2.5, 12))    # percin basi
    ekle_ucgen(G, "TOPPING_MODUL__celik", np.concatenate(parca), HAVA, MH, False); nk += 2
    log("   KD3 lamasi + 2 P-kelepce x", xk)
log("kelepce", nk)
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
