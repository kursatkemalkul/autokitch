# -*- coding: utf-8 -*-
"""m8t2 · ana hat kablolarının yeni yolları (sabit şerit sırası + kademeli geçiş). Çıktı: m8t2/yollar.json"""
import os, sys, json, random, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m8t2_rota_eski as RE
import m8t2_serit as SR
import m8t2_yol as Y
L = SR.L; RR = RE.RR
O, KES = RE.eski()
ESKI = {a: np.array(p) for a, (r, m, p) in O.items()}
MAL = {a: m for a, (r, m, p) in O.items()}
K = {}


def kab(ad, bas, bacak, gec, son, bas_sira="", son_sira=""):
    K[ad] = dict(r=RR[ad], bas=bas, bacak=bacak, gec=gec, son=son, bas_sira=bas_sira, son_sira=son_sira)


def ep(ad, n):
    return [tuple(q) for q in ESKI[ad][:n]]


EXT = {"GV": ("y", 1255.0, 2105.0), "FB": ("z", -826.5, -632.5), "RU": ("y", 1100.0, 1257.0), "RL": ("y", 744.0, 1104.0), "FA": ("x", 2422.5, 4140.0),
       "TS": ("y", 124.0, 784.0), "ZT": ("z", -708.5, -136.5), "ZF": ("x", 4041.5, 5407.5), "ZK": ("z", -193.5, 598.5), "ZB1": ("x", 5350.5, 5518.5),
       "ZB2": ("z", 541.5, 988.5), "BV": ("y", 51.5, 1120.0)}


def b2(ad, bac, gec):
    """GV bacağından sonrası (bölge 2) · son noktaları döner (son, son_sira)"""
    rota = RE.ROTA[ad] if ad != "bina" else ["GV", "FB", "RU", "RL", "FA", "TS", "ZT", "ZF", "ZK", "ZB1", "ZB2", "BV"]
    i = rota.index("GV")
    onceki = "GV"
    for nm in rota[i + 1:]:
        a = EXT[onceki][0]; b = EXT[nm][0]
        if a == b:
            lo = min(EXT[onceki][1], EXT[nm][1]); hi = max(EXT[onceki][2], EXT[nm][2])
            gec.append(("ayni", lo + 6, hi - 6, -1, {}))
        else:
            gec.append(("kose", onceki, nm))
        bac.append((b, L[nm][ad])); onceki = nm
    if ad.startswith("F_"):
        g_ = ad.endswith("guc"); xs = 2984.5 if g_ else 2995.5; yd = 1055.0 if g_ else 1070.0; xg = 2847.0 if g_ else 2834.0
        yu = 775.0 if g_ else 765.0
        bac.append(("x", {"y": yu, "z": -672.0})); gec.append(("ayni", 2440.0, 2975.0, 1, {"y": (744.0, 784.0), "z": (-760.0, -642.0)}))
        return [(xs, yd, -672.0), (xs, yd, -778.0), (xg, yd, -778.0), (xg, 1041.0, -778.0)], "zy"
    if ad.startswith("DOLAP"):
        yc = 659.0 if ad.endswith("guc") else 672.0
        return [(4130.0, yc, -670.0), (4150.0, yc, -670.0), (4150.0, yc, -505.0), (4240.0, yc, -505.0), (4240.0, yc, -519.0)], "yz"
    if ad == "bina":
        return [(5491.0, 1108.0, 950.0)], "zx"
    bx = {"QR_guc": 5386.0, "QR_veri": 5354.0, "ROBOT_guc": 5402.0, "ROBOT_veri": 5370.0, "modem": 5354.0}[ad]
    by = 41.0 if ad == "modem" else 59.0
    zr = {"QR_veri": 606.0, "ROBOT_veri": 611.0, "QR_guc": 616.0, "ROBOT_guc": 621.0, "modem": 628.0}[ad]
    return [(L["ZK"][ad]["x"], by, zr), (bx, by, zr), (bx, by, 640.0)], "y"


# ---------------- bölge 1 · T + üst hat
T_GEC = ("ayni", -650.0, -330.0, -1, {"x": (3327.5, 3423.5), "y": (2105.0, 2175.0)})
GV_SON = {}
WEST_G = ["QR_guc", "QR_veri", "ROBOT_guc", "ROBOT_veri", "modem", "DOLAP_guc", "DOLAP_veri", "bina"]
for ad in WEST_G + ["TOPPING_guc", "TOPPING_veri", "K_guc", "K_veri", "E_guc", "E_veri", "fan24"]:
    bas = ep(ad, 3) if ad != "bina" else [(3506.0, 1925.0, -190.0), (3338.9, 1925.0, -190.0), (3338.9, 2164.6, -190.0)]
    t0 = {"x": bas[-1][0], "y": bas[-1][1]}
    t1 = {"x": L["T"][ad]["x"], "y": L["T"][ad]["y"]}
    bac = [("z", t0), ("z", t1)]; gec = [T_GEC]
    if ad in WEST_G or ad.startswith("TOPPING"):
        bac.append(("x", L["M"][ad])); gec.append(("kose", 0, 0))
        if ad.startswith("TOPPING"):
            zg = -802.0 if ad.endswith("guc") else -789.0
            bac.append(("x", {"y": 2116.0, "z": zg})); gec.append(("ayni", 2130.0, 2440.0, -1, {"y": (2106.5, 2166.5), "z": (-824.5, -691.5)}))
            bac.append(("y", {"x": 2110.0, "z": zg})); gec.append(("kose", 0, 0))
            kab(ad, bas, bac, gec, [(2110.0, 2040.0, zg), (2084.0, 2040.0, zg)]); continue
        if L["U4"][ad] != L["M"][ad]:
            bac.append(("x", L["U4"][ad])); gec.append(("ayni", 2485.0, 2900.0, -1, {"y": (2106.5, 2139.0), "z": (-786.0, -691.5)}))
        bac.append(("y", L["GV"][ad])); gec.append(("kose", 0, 0))
        son, ss = b2(ad, bac, gec)
        kab(ad, bas, bac, gec, son, son_sira=ss); continue
    if ad.startswith(("K_", "E_")):
        bac.append(("x", L["UK"][ad])); gec.append(("kose", 0, 0))
        bac.append(("x", L["KE"][ad])); gec.append(("ayni", 3850.0, 3975.0, 1, {"y": (2106.5, 2166.5), "z": (-824.5, -691.5)}))
        o = -6.0 if ad.endswith("guc") else 7.0
        xd = (4300.0 if ad.startswith("K") else 5100.0) + o
        bac.append(("y", {"x": xd, "z": L["KE"][ad]["z"]})); gec.append(("kose", 0, 0))
        kab(ad, bas, bac, gec, [(xd, 1979.9, -760.0), (xd, 1954.9, -760.0)]); continue
    if ad == "fan24":
        bac.append(("x", {"y": 2109.4, "z": -821.0})); gec.append(("kose", 0, 0))
        bac.append(("z", {"x": 3360.0, "y": 2109.4})); gec.append(("kose", 0, 0))
        kab(ad, bas, bac, gec, [(3360.0, 2060.1, -790.0)]); continue
# A / F: ön duvar portu -> içeride y -> şerit
for ad in ("A_guc", "A_veri", "F_guc", "F_veri"):
    bas = ep(ad, 3); x0, y0 = bas[-1][0], bas[-1][1]
    r = RR[ad]; zi = -691.5 - r - 0.5
    bac = [("z", {"x": x0, "y": y0}), ("z", {"x": x0, "y": L["M"][ad]["y"]}), ("x", L["M"][ad])]
    gec = [("ayni", zi - 1.0, zi, -1, {"y": (2106.5, 2166.5)}), ("kose", 0, 0)]
    if ad.startswith("F"):
        bac.append(("y", L["GV"][ad])); gec.append(("kose", 0, 0))
        son, ss = b2(ad, bac, gec)
        kab(ad, bas, bac, gec, son, son_sira=ss); continue
    o = -6.0 if ad.endswith("guc") else 7.0; xa = 1290.0 + o
    if ad == "A_veri":
        bac.append(("x", {"y": 2128.0, "z": L["M"][ad]["z"]})); gec.append(("ayni", 2062.0, 2100.0, -1, {"y": (2106.5, 2166.5), "z": (-824.5, -691.5)}))
        bac.append(("x", {"y": 2149.3, "z": -805.6})); gec.append(("ayni", 1998.0, 2030.0, -1, {"y": (2106.5, 2166.5), "z": (-824.5, -691.5)}))
    else:
        bac.append(("x", {"y": 2151.2, "z": -817.2})); gec.append(("ayni", 2032.0, 2060.0, -1, {"y": (2106.5, 2166.5), "z": (-824.5, -691.5)}))
    kab(ad, bas, bac, gec, [(xa, 2141.0, -778.5)], son_sira="zy")


def ilk_param(k, i_kab, rnd=None):
    P = []
    for j, g in enumerate(k["gec"]):
        if g[0] == "ayni":
            lo, hi = g[1], g[2]
            f = (i_kab * 0.137 + j * 0.31) % 1.0 if rnd is None else rnd.random()
            t = lo + f * (hi - lo)
            cr = [e for e in "xyz" if e != k["bacak"][j][0]]
            P.append((t, t, cr[0]))
        else:
            if g[1] in EXT:
                b_ = g[2]; f = (i_kab * 0.173 + j * 0.29) % 1.0
                P.append(("sonra", EXT[b_][1] + 8 + f * (EXT[b_][2] - EXT[b_][1] - 16)))
            else:
                P.append(("sonra", 0.0))
    return P


def yollar(PP):
    return {a: (K[a]["r"], Y.kur(K[a], PP[a])) for a in K}


DW = float(os.environ.get("DW", "5"))
if __name__ == "__main__":
    EN = json.load(open(os.path.join(HERE, "m8t2", "engel.json")))
    ad_list = list(K)
    PP = {a: ilk_param(K[a], i) for i, a in enumerate(ad_list)}
    if len(sys.argv) > 3:
        W = json.load(open(sys.argv[3]))
        for a in PP:
            if a in W and len(W[a]["prm"]) == len(PP[a]): PP[a] = [tuple(p) for p in W[a]["prm"]]
    YL = yollar(PP)
    # engel: yalnız yollara yakın olanlar
    allp = np.vstack([p for r, p in YL.values()]); lo = allp.min(0) - 30; hi = allp.max(0) + 30
    eng = [(e["ad"], e["r"], np.array([e["a"], e["b"]])) for e in EN
           if np.all(np.minimum(e["a"], e["b"]) <= hi) and np.all(np.maximum(e["a"], e["b"]) >= lo)]
    print(len(eng), "engel segmenti")

    def skor(YL, odak=None):
        c = Y.carpisma(YL, eng, odak=odak)
        dis = 0
        for a in (odak or list(YL)):
            n_, q_ = Y.disari(K[a], YL[a][1]); dis += n_
        return sum(d for a, b, m, d in c) + 10 * len(c) + DW * dis, c
    s, c = skor(YL)
    print("ilk", round(s, 1), len(c))
    SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rnd = random.Random(SEED)
    GB = (s, {a: list(PP[a]) for a in PP}); durgun = 0
    for it in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6):
        bad = sorted(set([a for a, b, m, d in c] + [b for a, b, m, d in c]))
        bad = [a for a in bad if not a.startswith("#")]
        bad += [a for a in K if a not in bad and Y.disari(K[a], YL[a][1])[0] > 0]
        if not bad: break
        rnd.shuffle(bad)
        for a in bad:
            k = K[a]; best = (skor(YL, [a])[0], PP[a])
            for j, g in enumerate(k["gec"]):
                if g[0] == "kose" and g[1] in EXT:
                    A_, B_ = EXT[g[1]], EXT[g[2]]
                    for _ in range(16):
                        if rnd.random() < 0.5: P2 = list(best[1]); P2[j] = ("once", A_[1] + 6 + rnd.random() * (A_[2] - A_[1] - 12))
                        else: P2 = list(best[1]); P2[j] = ("sonra", B_[1] + 6 + rnd.random() * (B_[2] - B_[1] - 12))
                        YL2 = dict(YL); YL2[a] = (k["r"], Y.kur(k, P2))
                        s2 = skor(YL2, [a])[0]
                        if s2 < best[0]: best = (s2, P2)
                    continue
                if g[0] != "ayni": continue
                lo, hi = g[1], g[2]
                cr = [e for e in "xyz" if e != k["bacak"][j][0]]
                yon = g[3]; rng = g[4]
                for _ in range(40):
                    ts = sorted([lo + rnd.random() * (hi - lo) for _ in range(3)], reverse=(yon < 0))
                    u = rnd.choice(cr)
                    if rnd.random() < 0.45 and u in rng:
                        a_, b_ = rng[u]; m_ = a_ + k["r"] + 0.5 + rnd.random() * max(0.0, (b_ - a_) - 2 * k["r"] - 1.0)
                        P2 = list(best[1]); P2[j] = (ts[0], ts[1], ts[2], u, m_)
                    else:
                        t2 = ts[0] if rnd.random() < 0.5 else ts[1]
                        P2 = list(best[1]); P2[j] = (ts[0], t2, u)
                    YL2 = dict(YL); YL2[a] = (k["r"], Y.kur(k, P2))
                    s2 = skor(YL2, [a])[0]
                    if s2 < best[0]: best = (s2, P2)
            if best[1] is PP[a] and rnd.random() < 0.08:              # takıldı: rastgele sarsma
                P2 = list(PP[a]); js = [j for j, g in enumerate(k["gec"]) if g[0] == "ayni"] or [0]
                j = rnd.choice(js); g = k["gec"][j]; lo, hi = g[1], g[2]
                cr = [e for e in "xyz" if e != k["bacak"][j][0]]
                ts = sorted([lo + rnd.random() * (hi - lo) for _ in range(3)], reverse=(g[3] < 0))
                P2[j] = (ts[0], ts[1], rnd.choice(cr)); best = (0, P2)
            PP[a] = best[1]; YL[a] = (k["r"], Y.kur(k, PP[a]))
        s, c = skor(YL)
        if s < GB[0] - 1e-6:
            GB = (s, {a: list(PP[a]) for a in PP}); durgun = 0
            json.dump({a: dict(r=K[a]["r"], mal=MAL[a], P=[list(map(float, q)) for q in YL[a][1]], prm=[list(p) for p in PP[a]]) for a in K},
                      open(os.path.join(HERE, "m8t2", "yollar_s%d.json" % SEED), "w"), indent=0)
        else:
            durgun += 1
            if durgun >= 4:
                PP = {a: list(GB[1][a]) for a in GB[1]}; YL = yollar(PP); s, c = skor(YL); durgun = 0
        print("tur", it, round(s, 1), len(c), "en iyi", round(GB[0], 1), flush=True)
    for a in K:
        n_, q_ = Y.disari(K[a], YL[a][1])
        if n_: print("DISARI", a, n_, None if q_ is None else np.round(q_, 1))
    import collections
    cnt = collections.Counter((a, b) for a, b, m, d in c)
    for (a, b), n in cnt.most_common(40):
        ex = [(np.round(m, 1), round(d, 1)) for a2, b2, m, d in c if a2 == a and b2 == b][:2]
        print(a, b, n, ex)
    json.dump({a: dict(r=K[a]["r"], mal=MAL[a], P=[list(map(float, q)) for q in YL[a][1]], prm=[list(p) for p in PP[a]]) for a in K},
              open(os.path.join(HERE, "m8t2", "yollar_b1.json"), "w"), indent=0)
