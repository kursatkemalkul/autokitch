# -*- coding: utf-8 -*-
"""Zincir kabloları (dış: ana kanal / iniş / zemin) — dik açılı yollar + şerit atamaları. kablolar() -> [dict(ad, tur, r, Q, mek)]"""
import numpy as np
from olcu import *

ZD = -880.0           # fiş çıkış (iniş) düzlemi
QR_ZG = 670.0 - 2.0 - HAN_GOV[2] - HAN_KAP[2] / 2   # QR kapak rakoru z


def bx(ist, k):
    return C[ist] + DX[k]


def ust_cikis(ist, k):
    """üst sıra fiş -> (x, y, ZD) ilk noktalar (aşağı iner)"""
    x = bx(ist, k); yc = YC[ist]
    if k.startswith("GUC"): return [(x, yc - HAN_KAP[1] / 2 - HAN_RAKOR_L, ZD)]
    if k.startswith("VERI"): return [(x, yc, -832 - M12_FLANS[2] - M12_FIS_L), (x, yc, ZD)]
    return [(x, yc, -832 - HAVA_L), (x, yc, ZD)]


def b_cikis(k):
    x = bx("B", k)
    if k.startswith("GUC"): return [(x, YC["B"] + HAN_KAP[1] / 2 + HAN_RAKOR_L, ZD)]
    if k.startswith("VERI"): return [(x, YC["B"], -832 - M12_FLANS[2] - M12_FIS_L), (x, YC["B"], ZD)]
    raise KeyError(k)


def qr_cikis(k):
    x = bx("QR", k)
    if k.startswith("GUC"): return [(x, YC["QR"] - HAN_KAP[1] / 2 - HAN_RAKOR_L, QR_ZG)]
    return [(x, YC["QR"], 668 - M12_FLANS[2] - M12_FIS_L), (x, YC["QR"], QR_ZG - 2)]


def yol(bas, son, ara):
    return [np.array(p, float) for p in list(bas) + list(ara) + list(reversed(son))]


def kablolar():
    K = []
    def ek(ad, tur, Q, mek="Elektrik/Ana hat"):
        r = dict(guc=R_GUC, veri=R_VERI, hava=R_HAVA, bina=R_BINA)[tur]
        K.append(dict(ad=ad, tur=tur, r=r, Q=[np.asarray(q, float) for q in Q], mek=mek))
    # pano çıkışları: (x, y_row) · yükseliş z şeridi
    PX = dict(LP=(3942.0, 2118.0, -925.0), LD=(3966.0, 2118.0, -925.0), RP=(3942.0, 2094.0, -905.0), RD=(3966.0, 2094.0, -905.0))
    ZP = -338.0          # pano arka rakoru dış ucu
    def pano(k, y_lane, x_end, son):
        x, yr, zl = PX[k]
        return [(x, yr, ZP), (x, yr, zl), (x, y_lane, zl), (x_end, y_lane, zl), (x_end, y_lane, ZD)] + list(reversed(son))
    # SOL KOL: pano -> F
    ek("kol_sol_guc pano>F", "guc", pano("LP", 830.0, bx("F", "GUC_GIRIS"), ust_cikis("F", "GUC_GIRIS")))
    ek("kol_sol_veri pano>F", "veri", pano("LD", 812.0, bx("F", "VERI_GIRIS"), ust_cikis("F", "VERI_GIRIS")))
    # SAĞ KOL: pano -> K
    ek("kol_sag_guc pano>K", "guc", pano("RP", 812.0, bx("K", "GUC_GIRIS"), ust_cikis("K", "GUC_GIRIS")))
    ek("kol_sag_veri pano>K", "veri", pano("RD", 830.0, bx("K", "VERI_GIRIS"), ust_cikis("K", "VERI_GIRIS")))

    def ara(a_ist, a_k, b_ist, b_k, y_lane, zl, tur, ad):
        A = ust_cikis(a_ist, a_k) if a_ist != "B" else b_cikis(a_k)
        B = ust_cikis(b_ist, b_k) if b_ist != "B" else b_cikis(b_k)
        xa = A[-1][0]; xb = B[-1][0]
        Q = list(A) + [(xa, y_lane, ZD), (xa, y_lane, zl), (xb, y_lane, zl), (xb, y_lane, ZD)] + list(reversed(B))
        ek(ad, tur, Q)
    ara("F", "GUC_CIKIS", "TOPPING", "GUC_GIRIS", 798.0, -905.0, "guc", "ara F>TOPPING guc")
    ara("F", "VERI_CIKIS", "TOPPING", "VERI_GIRIS", 782.0, -905.0, "veri", "ara F>TOPPING veri")
    ara("F", "HAVA_GIRIS", "TOPPING", "HAVA_GIRIS", 768.0, -905.0, "hava", "hava F>TOPPING")
    ara("K", "GUC_CIKIS", "B", "GUC_GIRIS", 790.0, -905.0, "guc", "ara K>B guc")
    ara("K", "VERI_CIKIS", "B", "VERI_GIRIS", 806.0, -905.0, "veri", "ara K>B veri")
    ara("B", "GUC_CIKIS", "E", "GUC_GIRIS", 760.0, -905.0, "guc", "ara B>E guc")
    ara("B", "VERI_CIKIS", "E", "VERI_GIRIS", 776.0, -905.0, "veri", "ara B>E veri")
    ara("F", "HAVA_CIKIS", "K", "HAVA_GIRIS", 796.0, -905.0, "hava", "hava F>K")
    ara("K", "HAVA_CIKIS", "E", "HAVA_GIRIS", 746.0, -905.0, "hava", "hava K>E")
    # E -> QR (iniş + zemin)
    xi = {"guc": 5085.0, "veri": 5115.0}; yl = {"guc": 12.0, "veri": 10.0}
    for tur, k_e, k_q, y_lane, zl, z_don in (("guc", "GUC_CIKIS", "GUC_GIRIS", 750.0, -905.0, 610.0), ("veri", "VERI_CIKIS", "VERI_GIRIS", 766.0, -905.0, 585.0)):
        A = ust_cikis("E", k_e); xa = A[-1][0]; B = qr_cikis(k_q); xb = B[-1][0]; zq = B[-1][2]
        Q = list(A) + [(xa, y_lane, ZD), (xa, y_lane, zl), (xi[tur], y_lane, zl), (xi[tur], yl[tur], zl), (xi[tur], yl[tur], z_don),
                       (xb, yl[tur], z_don), (xb, yl[tur], zq)] + list(reversed(B))
        ek("ara E>QR %s" % tur, tur, Q)
    # QR çıkışı -> ROBOT rezerv kutusu (zemin kanalı üst seviyesi)
    for tur, k_q, x_k, y_l, z_don, z_kutu in (("guc", "GUC_CIKIS", 5085.0, 31.0, 575.0, 380.0), ("veri", "VERI_CIKIS", 5115.0, 44.0, 590.0, 340.0)):
        A = qr_cikis(k_q); xa = A[-1][0]; za = A[-1][2]
        Q = list(A) + [(xa, y_l, za), (xa, y_l, z_don), (x_k, y_l, z_don), (x_k, y_l, z_kutu), (ROBOT_KUTU["x"][1] - 40.0, y_l, z_kutu)]
        ek("QR>ROBOT rezerv %s" % tur, tur, Q, mek="Çevre/Dükkân hattı")
    return K


def seg_dist(p1, q1, p2, q2):
    d1 = q1 - p1; d2 = q2 - p2; r = p1 - p2; a = d1 @ d1; e = d2 @ d2; f = d2 @ r
    if a < 1e-9 and e < 1e-9: return np.linalg.norm(r)
    if a < 1e-9: s = 0; t = np.clip(f / e, 0, 1)
    else:
        c = d1 @ r
        if e < 1e-9: t = 0; s = np.clip(-c / a, 0, 1)
        else:
            b = d1 @ d2; den = a * e - b * b
            s = np.clip((b * f - c * e) / den, 0, 1) if den > 1e-9 else 0
            t = (b * s + f) / e
            if t < 0: t = 0; s = np.clip(-c / a, 0, 1)
            elif t > 1: t = 1; s = np.clip((b - c) / a, 0, 1)
    return np.linalg.norm(p1 + d1 * s - (p2 + d2 * t))


def kesisme(K, pay=0.5):
    out = []
    for i in range(len(K)):
        for j in range(i + 1, len(K)):
            A, B = K[i], K[j]; lim = A["r"] + B["r"] + pay
            for a0, a1 in zip(A["Q"][:-1], A["Q"][1:]):
                for b0, b1 in zip(B["Q"][:-1], B["Q"][1:]):
                    d = seg_dist(a0, a1, b0, b1)
                    if d < lim: out.append((A["ad"], B["ad"], round(d, 2), lim, a0.round(1).tolist(), b0.round(1).tolist()))
    return out


if __name__ == "__main__":
    K = kablolar()
    for k in K: print(k["ad"], len(k["Q"]), "nokta", round(sum(np.linalg.norm(b - a) for a, b in zip(k["Q"][:-1], k["Q"][1:]))), "mm")
    for o in kesisme(K): print("KESISME", o)
