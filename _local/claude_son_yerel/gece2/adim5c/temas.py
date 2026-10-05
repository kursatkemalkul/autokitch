# -*- coding: utf-8 -*-
"""v8zq: TOPPING gövde düzlemlerine değen (±0,06) kalan bileşenler + dönüş (flanş) hacimlerine giren bileşenler"""
import pickle, re, sys, json, numpy as np
B = pickle.load(open(r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5\_is\bil_hepsi.pkl", "rb"))
SAC_R = set([30, 17, 20, 19, 18, 21, 22, 23, 24, 25, 26, 27, 28, 98, 99] + list(range(31, 82)))
PAS_R = set(range(105, 156))
PU_R = set(list(range(0, 8)) + [10, 11])
KAIDE_R = set(range(0, 12))


def degisen(b):
    a, n = b["ad"], b["no"]
    if a == "TOPPING_MODUL__sac": return n in SAC_R
    if a == "TOPPING_MODUL__paslanmaz": return n in PAS_R
    if a == "TOPPING_MODUL__pu": return n in PU_R
    if a == "KAIDE_C__paslanmaz": return True
    return False


KAL = [b for b in B if not degisen(b) and not b["ad"].startswith("URUN")]
HARIC_AD = re.compile(r"^(A_GOVDE|A_ONYUZ|KAIDE_A|B_KASA|B_MODULER|B_TASIYICI|F_UST_KABIN__(sac|paslanmaz|yalitim)|F_TP10_GOVDE__sac|U_F_GOVDE)")


def temas(ax, d, sg, lo2, hi2, tol=0.06):
    """ax düzlemi d · sg: bileşen hangi tarafta (+1: d'den büyük tarafta) · lo2/hi2 bölge (3B, ax hariç kullanılır)"""
    out = []
    for b in KAL:
        if HARIC_AD.search(b["ad"]): continue
        lo, hi = b["lo"], b["hi"]
        yuz = lo[ax] if sg > 0 else hi[ax]
        if abs(yuz - d) > tol: continue
        o = [i for i in range(3) if i != ax]
        if all(lo[i] < hi2[i] - 0.01 and hi[i] > lo2[i] + 0.01 for i in o):
            out.append((b["ad"], b["no"], np.round(lo, 2).tolist(), np.round(hi, 2).tolist()))
    return out


def giren(lo2, hi2, pay=0.3):
    out = []
    for b in KAL:
        if HARIC_AD.search(b["ad"]): continue
        lo, hi = b["lo"], b["hi"]
        if all(lo[i] < hi2[i] + pay and hi[i] > lo2[i] - pay for i in range(3)):
            out.append((b["ad"], b["no"], np.round(lo, 2).tolist(), np.round(hi, 2).tolist()))
    return out


if __name__ == "__main__":
    D = {
        "yan_sol": (0, 1437.5, +1, [0, 892, -830], [0, 2200, 39]),
        "yan_sag": (0, 2498.5, -1, [0, 892, -830], [0, 2200, 39]),
        "taban": (1, 893.5, +1, [1437.5, 0, -828.5], [2498.5, 0, 39]),
        "tavan": (1, 2198.5, -1, [1437.5, 0, -828.5], [2498.5, 0, 39]),
        "arka": (2, -828.5, +1, [1437.5, 892, 0], [2498.5, 2200, 0]),
        "soguk_arka_dis_kuru": (2, -630.0, -1, [1437.5, 1109, 0], [2498.5, 2198.5, 0]),
        "astar_sol": (0, 1496.0, +1, [0, 1110.5, -570], [0, 2140, 38]),
        "astar_sag": (0, 2440.0, -1, [0, 1110.5, -570], [0, 2140, 38]),
        "astar_tavan": (1, 2140.0, -1, [1496, 0, -570], [2440, 0, 38]),
        "astar_arka": (2, -570.0, +1, [1496, 1110.5, 0], [2440, 2140, 0]),
        "raf_ust": (1, 1152.0, +1, [1496, 0, -570], [2440, 0, 23]),
        "ust_raf_ust": (1, 1575.0, +1, [1496, 0, -570], [2440, 0, -50]),
        "ust_raf_alt": (1, 1534.0, -1, [1496, 0, -570], [2440, 0, -50]),
        "alt_sac_alt": (1, 1109.0, -1, [1437.5, 0, -628.5], [2498.5, 0, 38]),
        "kuru_taban_ust": (1, 1109.0, +1, [1437.5, 0, -828.5], [2420, 0, -630]),
        "kuru_taban_alt": (1, 1107.5, -1, [1437.5, 0, -828.5], [2420, 0, -630]),
        "on_perde_on": (2, -475.0, +1, [1437.5, 893.5, 0], [2420, 1109, 0]),
        "on_perde_arka": (2, -476.5, -1, [1437.5, 893.5, 0], [2420, 1109, 0]),
        "sag_perde_sag": (0, 2420.0, +1, [0, 893.5, -828.5], [0, 1109, -476.5]),
        "sag_perde_sol": (0, 2418.5, -1, [0, 893.5, -828.5], [0, 1109, -476.5]),
        "cep_taban": (1, 807.5, +1, [1629.5, 0, -788.5], [2093.5, 0, -477.5]),
        "ayirma_sag": (0, 1631.0, +1, [0, 807.5, -828.5], [0, 1109, -476.5]),
        "ayirma_sol": (0, 1629.5, -1, [0, 807.5, -828.5], [0, 1109, -476.5]),
        "kaide_plaka_ust": (1, 892.0, +1, [1436, 0, -830], [2500, 0, 35]),
        "cerceve_on": (2, 39.0, +1, [1437.5, 893.5, 0], [2498.5, 2198.5, 0]),
    }
    R = {}
    for k, (ax, d, sg, lo2, hi2) in D.items():
        t = temas(ax, d, sg, np.array(lo2, float), np.array(hi2, float))
        R[k] = t
        print("== %s (%d)" % (k, len(t)))
        for x in t: print("   %-38s %3d %s %s" % x)
    json.dump(R, open("temas.json", "w"), indent=0)
