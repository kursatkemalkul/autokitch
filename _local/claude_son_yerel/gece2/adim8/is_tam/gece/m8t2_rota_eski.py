# -*- coding: utf-8 -*-
"""m8t2: h3_elk_hat_v1.ana_hat_kablolari mantiginin SALT KOPYASI (uretec calistirilmaz) -> eski yollar (GLB ile karsilastirma icin)."""
import math
T = 1.5
R_FAN = 2.4; UF_TERMOSTAT = (3360.0, 2060.0)
R_G, R_D, R_DIO, R_B = 6.25, 4.35, 3.8, 9.95
UFS = [("UF1", 3280.0, 3984.0, (2105.0, 2166.5), (-826.0, -690.0)), ("UF2", 2920.0, 3280.0, (2105.0, 2166.5), (-826.0, -748.0)),
       ("UF3", 2575.0, 2920.0, (2138.0, 2166.5), (-826.0, -656.0)), ("UF4", 1993.0, 2575.0, (2105.0, 2166.5), (-826.0, -690.0))]
TA = dict(x=(1250.0, 1993.0), y=(2143.0, 2165.0), z=(-826.0, -766.0))
UST_KE = dict(y=(2125.0, 2165.0), z=(-826.0, -766.0))
KE_GECIS = dict(y=(2143.0, 2165.0), z=(-826.0, -766.0))
TOPLAMA = dict(x=(3326.0, 3425.0), y=(2138.0, 2176.5), z=(-690.0, -125.0), y_arka=2103.5, z_kirik=-300.0)
GV = dict(x=(2452.0, 2478.0), z=(-826.5, -701.5), y=(1255.0, 2105.0))
FB = dict(x=(2422.5, 2478.0), y=(1255.0, 1320.0), z=(-826.5, -632.5))
RU = dict(x=(2422.5, 2466.5), y=(1100.0, 1257.0), z=(-686.0, -632.5))
RL = dict(x=(2422.5, 2449.5), y=(744.0, 1104.0), z=(-698.0, -560.0))
FA = dict(x=(2422.5, 4140.0), y=(744.0, 784.0), z=(-760.0, -642.0))
TS = dict(x=(4100.0, 4140.0), y=(124.0, 784.0), z=(-700.0, -642.0))
ZU_H = 50.0
BV = dict(x=(5466.0, 5516.0), z=(925.0, 975.0), y=(51.5, 1120.0))
AYIRICI = dict(x=(5431.0, 5546.0), y=(1120.0, 1300.0), z=(880.0, 1020.0))
TOPPING_HARTING = (1993.0, 2040.0, -796.0)
A_KUTU = dict(x=(1240.0, 1400.0), y=(1880.0, 2050.0), z=(-828.5, -728.5))
F_KUTU = dict(x=(2800.0, 2960.0), y=(830.0, 950.0), z=(-828.0, -728.0))
F_INIS = dict(x=2990.0, z=-672.0)
D_HARTING = (4240.0, 665.0, -610.0)
XS = 3518.0 - 3.0 - 25.9
SOK = {"TOPPING": ("TOPPING", XS, 2122.0, -240.0, "-x"), "DOLAP": ("DOLAP", XS, 2122.0, -140.0, "-x"), "K": ("K", XS, 2021.0, -240.0, "-x"),
       "E": ("E", XS, 2021.0, -140.0, "-x"), "ROBOT": ("ROBOT", XS, 1920.0, -240.0, "-x"), "QR": ("QR", XS, 1920.0, -140.0, "-x"),
       "A": ("A", 3668.0, 2021.0, -320.0 - 28.9, "-z"), "F": ("F", 3828.0, 2021.0, -320.0 - 28.9, "-z")}
GIR = {"bina_besleme_5G6_M32": ("bina_besleme_5G6_M32", 3518.0, 1925.0, -190.0), "modem_Cat6A_M20": ("modem_Cat6A_M20", 3518.0, 2021.0, -190.0),
       "fan_24V_M20": ("fan_24V_M20", 3518.0, 2117.0, -190.0)}
B_KABLOLAR = {"guc_QR_3G2_5": (5386.0, 59.0), "guc_ROBOT_3G2_5": (5402.0, 59.0), "veri_QR_Cat6A": (5354.0, 59.0), "veri_ROBOT_Cat6A": (5370.0, 59.0), "veri_MODEM_Cat6A": (5354.0, 41.0)}
TEKME_Z0 = 670.0; UC_DIS = 30.0
EKS = "xyz"


class Kesit:
    def __init__(s, ad, ax, rng, u, v, v_ust=False):
        s.ad, s.ax, s.rng, s.u, s.v, s.v_ust = ad, ax, rng, u, v, v_ust
        s.poz = {}

    def icerir(s, eksen, deger, r):
        lo, hi = s.rng[eksen]
        return lo + r - 0.01 <= deger <= hi - r + 0.01

    def yerlestir(s, kablolar, sabit=None, bosluk=1.0, sirali=False):
        if sabit:
            s.poz.update(sabit); kablolar = [k for k in kablolar if k[0] not in sabit]
        u0, u1 = s.rng[s.u]; v0, v1 = s.rng[s.v]
        sira = list(kablolar) if sirali else sorted(kablolar, key=lambda k: -k[1])
        cu, raf_v, raf_h = u0, (v1 if s.v_ust else v0), 0.0
        for ad, r in sira:
            if cu + 2 * r + bosluk > u1 + 1e-6:
                raf_v = raf_v - raf_h - bosluk if s.v_ust else raf_v + raf_h + bosluk; cu, raf_h = u0, 0.0
            pu = cu + bosluk + r; cu = pu + r
            raf_h = max(raf_h, 2 * r)
            pv = raf_v - r - 0.5 if s.v_ust else raf_v + r + 0.5
            if not (v0 + r - 0.01 <= pv <= v1 - r + 0.01):
                raise AssertionError("%s kesitine sigmadi: %s" % (s.ad, ad))
            s.poz[ad] = {s.u: pu, s.v: pv}
        return s.poz


def _nokta(ax, deger, capraz):
    p = [0.0, 0.0, 0.0]; p[EKS.index(ax)] = deger
    for e, d in capraz.items(): p[EKS.index(e)] = d
    return tuple(p)


def _dik(a, b, sira):
    out, c = [], list(a)
    for e in sira + "".join(x for x in EKS if x not in sira):
        i = EKS.index(e)
        if abs(c[i] - b[i]) > 1e-6:
            c[i] = b[i]; out.append(tuple(c))
    return out


def hat_yolu(ad, r, bas, kesitler, son, sinir, jog_at, bas_sira="", son_sira="", delta=12.0):
    pts = list(bas)
    S0 = kesitler[0]
    cap = [e for e in EKS if e != S0.ax]
    hedef = _nokta(S0.ax, pts[-1][EKS.index(S0.ax)], {e: S0.poz[ad][e] for e in cap})
    pts += _dik(pts[-1], hedef, bas_sira or "".join(cap))
    n = len(kesitler)
    for k in range(n - 1):
        A, Bk = kesitler[k], kesitler[k + 1]
        a, b = A.ax, Bk.ax
        pa, pb = A.poz[ad], Bk.poz[ad]
        prev = pts[-1]
        if a != b:
            c = [e for e in EKS if e not in (a, b)][0]
            p1 = _nokta(b, pa[b], {a: pb[a], c: pa[c]})
            if abs(pa[c] - pb[c]) < 1e-6:
                pts.append(p1); continue
            if k + 2 < n:
                C = kesitler[k + 2]
                cik = C.poz[ad][b] if C.ax != b else sinir[(Bk.ad, C.ad)]
            else:
                cik = son[0][EKS.index(b)]
            yon = 1.0 if cik > pa[b] else -1.0
            if (A.ad, Bk.ad) in jog_at:
                je, jv = jog_at[(A.ad, Bk.ad)]
                if je == b:
                    q = list(p1); q[EKS.index(b)] = jv
                    pts += [p1, tuple(q)]; q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                else:
                    q = list(p1); q[EKS.index(a)] = jv
                    pts.append(tuple(q)); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                    q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            elif Bk.icerir(c, pa[c], r):
                q = list(p1); q[EKS.index(b)] += yon * delta
                pts += [p1, tuple(q)]; q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            elif A.icerir(c, pb[c], r):
                ya = 1.0 if p1[EKS.index(a)] > prev[EKS.index(a)] else -1.0
                q = list(p1); q[EKS.index(a)] -= ya * delta
                pts.append(tuple(q)); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            else:
                pts += [p1]; q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
        else:
            sb = sinir[(A.ad, Bk.ad)]
            yon = 1.0 if sb > prev[EKS.index(a)] else -1.0
            cur = {e: pa[e] for e in EKS if e != a}
            once = [e for e in cur if abs(pa[e] - pb[e]) > 1e-6 and A.icerir(e, pb[e], r)]
            sonra = [e for e in cur if abs(pa[e] - pb[e]) > 1e-6 and e not in once]
            pts.append(_nokta(a, sb - yon * delta, cur))
            for e in once:
                cur[e] = pb[e]; pts.append(_nokta(a, sb - yon * delta, cur))
            pts.append(_nokta(a, sb + yon * delta, cur))
            for e in sonra:
                cur[e] = pb[e]; pts.append(_nokta(a, sb + yon * delta, cur))
    SL = kesitler[-1]
    cap = [e for e in EKS if e != SL.ax]
    E = _nokta(SL.ax, son[0][EKS.index(SL.ax)], {e: SL.poz[ad][e] for e in cap})
    pts.append(E)
    pts += _dik(E, son[0], son_sira or "".join(cap))
    pts += list(son[1:])
    q = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q[-1]) > 0.05: q.append(p)
    return q


def kesitler():
    K = {}
    K["T"] = Kesit("T", "z", {"x": (TOPLAMA["x"][0] + T, TOPLAMA["x"][1] - T), "y": (TOPLAMA["y_arka"] + T, TOPLAMA["y"][1] - T)}, "x", "y")
    for nm, a, b, (y0_, y1_), (z0_, z1_) in UFS:
        K[nm] = Kesit(nm, "x", {"y": (y0_ + T, y1_), "z": (z0_ + T, z1_ - T)}, "z", "y")
    K["TA"] = Kesit("TA", "x", {"y": (TA["y"][0] + T, TA["y"][1]), "z": (TA["z"][0] + T, TA["z"][1] - T)}, "z", "y")
    K["KE"] = Kesit("KE", "x", {"y": (KE_GECIS["y"][0] + T, KE_GECIS["y"][1] - T), "z": (KE_GECIS["z"][0] + T, KE_GECIS["z"][1] - T)}, "z", "y")
    for nm, xd in (("IK", 4300.0), ("IE", 5100.0)):
        K[nm] = Kesit(nm, "y", {"x": (xd - 20.0 + T, xd + 20.0 - T), "z": (-824.5, -750.0)}, "x", "z")
    K["GV"] = Kesit("GV", "y", {"x": GV["x"], "z": GV["z"]}, "z", "x")
    K["FB"] = Kesit("FB", "z", {"x": FB["x"], "y": FB["y"]}, "x", "y")
    K["RU"] = Kesit("RU", "y", {"x": RU["x"], "z": RU["z"]}, "x", "z")
    K["RL"] = Kesit("RL", "y", {"x": RL["x"], "z": RL["z"]}, "z", "x")
    K["FA"] = Kesit("FA", "x", {"y": FA["y"], "z": FA["z"]}, "z", "y")
    K["TS"] = Kesit("TS", "y", {"x": TS["x"], "z": TS["z"]}, "z", "x")
    zy = (T, ZU_H)
    K["ZT"] = Kesit("ZT", "z", {"x": (4040.0 + T, 4150.0 - T), "y": zy}, "x", "y")
    K["ZF"] = Kesit("ZF", "x", {"z": (-195.0 + T, -135.0 - T), "y": zy}, "z", "y")
    K["ZK"] = Kesit("ZK", "z", {"x": (5349.0 + T, 5409.0 - T), "y": zy}, "x", "y")
    K["ZB1"] = Kesit("ZB1", "x", {"z": (540.0 + T, 600.0 - T), "y": zy}, "z", "y")
    K["ZB2"] = Kesit("ZB2", "z", {"x": (5460.0 + T, 5520.0 - T), "y": zy}, "x", "y")
    K["BV"] = Kesit("BV", "y", {"x": (BV["x"][0] + T, BV["x"][1] - T), "z": (BV["z"][0] + T, BV["z"][1] - T)}, "x", "z")
    return K


SINIR = {("UF4", "TA"): 1993.0, ("UF1", "KE"): 3984.0, ("RU", "RL"): 1102.0, ("RL", "RU"): 1102.0,
         ("UF1", "UF2"): 3280.0, ("UF2", "UF3"): 2920.0, ("UF3", "UF4"): 2575.0, ("UF4", "UF3"): 2575.0, ("UF3", "UF2"): 2920.0, ("UF2", "UF1"): 3280.0}
JOG = {("UF4", "GV"): ("y", 2088.0), ("GV", "UF4"): ("y", 2088.0), ("KE", "IK"): ("y", 2105.0), ("KE", "IE"): ("y", 2105.0),
       ("T", "UF1"): ("z", -670.0), ("UF1", "T"): ("z", -670.0)}
IST = ["TOPPING", "DOLAP", "K", "E", "ROBOT", "QR", "A", "F"]
KAB = []
for i_ in IST:
    KAB.append(("%s_guc" % i_, R_DIO if i_ == "F" else R_G, "kablo")); KAB.append(("%s_veri" % i_, R_D, "kablo_veri"))
KAB += [("modem", R_D, "kablo_veri"), ("bina", R_B, "kablo"), ("fan24", R_FAN, "kablo")]
RR = {a: r for a, r, m in KAB}
UFA = ["UF1", "UF2", "UF3", "UF4"]
YOL = {"TOPPING": ["T"] + UFA, "K": ["T", "UF1", "KE", "IK"], "E": ["T", "UF1", "KE", "IE"],
       "DOLAP": ["T"] + UFA + ["GV", "FB", "RU", "RL", "FA", "TS"]}
for i_ in ("ROBOT", "QR"): YOL[i_] = ["T"] + UFA + ["GV", "FB", "RU", "RL", "FA", "TS", "ZT", "ZF", "ZK"]
YOL["A"] = UFA + ["TA"]
YOL["F"] = UFA + ["GV", "FB", "RU", "RL", "FA"]
ROTA = {}
for i_ in IST:
    ROTA["%s_guc" % i_] = YOL[i_]; ROTA["%s_veri" % i_] = YOL[i_]
ROTA["modem"] = YOL["QR"]
ROTA["bina"] = ["BV", "ZB2", "ZB1", "ZK", "ZF", "ZT", "TS", "FA", "RL", "RU", "FB", "GV"] + UFA[::-1] + ["T"]
ROTA["fan24"] = ["T", "UF1"]
SIRA = ["fan24", "bina", "QR_guc", "QR_veri", "ROBOT_guc", "ROBOT_veri", "modem", "DOLAP_guc", "DOLAP_veri", "F_guc", "F_veri", "A_guc", "A_veri",
        "TOPPING_guc", "TOPPING_veri", "K_guc", "K_veri", "E_guc", "E_veri"]


def toplama_sabit(K):
    T_ = K["T"]; x_ = T_.rng["x"][0]; sab = {}
    for ad in ("ROBOT_guc", "ROBOT_veri", "K_guc", "K_veri", "TOPPING_guc", "TOPPING_veri", "modem", "fan24"):
        r = RR[ad]; x_ += 1.5 + r; sab[ad] = {"x": x_, "y": TOPLAMA["y"][0] + T + r + 0.5}; x_ += r
    x_ = T_.rng["x"][0]
    for ad in ("bina", "QR_guc", "QR_veri", "E_guc", "E_veri", "DOLAP_guc", "DOLAP_veri"):
        r = RR[ad]; x_ += 1.5 + r; sab[ad] = {"x": x_, "y": T_.rng["y"][1] - r - 0.5}; x_ += r
    return sab


def uclar(K):
    """her kablo: (bas, bas_sira, son, son_sira) -- generator ile ayni"""
    T_ = K["T"]; out = {}

    def soket_bas(ist, ad, o):
        s = SOK[ist]; xm, ys, zs, yon = s[1], s[2], s[3], s[4]
        if yon == "-x":
            gx = xm - 45.0 - 18.0
            p = T_.poz[ad]
            return [(gx, ys + o, zs), (p["x"], ys + o, zs)], ""
        gz = zs - 45.0 - 18.0
        p = K["UF1"].poz[ad]
        return [(xm + o, ys, gz), (xm + o, ys, gz - 15.0), (xm + o, p["y"], gz - 15.0)], "z"
    for ad, r, mal in KAB:
        if ad == "bina":
            g = GIR["bina_besleme_5G6_M32"]
            bas = [((BV["x"][0] + BV["x"][1]) / 2.0, AYIRICI["y"][0] - 12.0, (BV["z"][0] + BV["z"][1]) / 2.0)]
            son = [(T_.poz[ad]["x"], T_.poz[ad]["y"], g[3]), (T_.poz[ad]["x"], g[2], g[3]), (g[1] - 12.0, g[2], g[3])]
            out[ad] = (bas, "", son, ""); continue
        if ad == "fan24":
            g = GIR["fan_24V_M20"]
            bas = [(g[1] - 12.0, g[2], g[3]), (T_.poz[ad]["x"], g[2], g[3])]
            son = [(UF_TERMOSTAT[0], 2140.0, -790.0), (UF_TERMOSTAT[0], UF_TERMOSTAT[1] + 0.1, -790.0)]
            out[ad] = (bas, "", son, "z"); continue
        bsira = ""
        if ad == "modem":
            g = GIR["modem_Cat6A_M20"]
            bas = [(g[1] - 12.0, g[2], g[3]), (T_.poz[ad]["x"], g[2], g[3])]
            ist = "QR"; tur = None
        else:
            ist, tur = ad.rsplit("_", 1)
            o = -6.0 if tur == "guc" else 7.0
            bas, bsira = soket_bas(ist, ad, o)
        if ist in ("ROBOT", "QR") or ad == "modem":
            bk = {"QR_guc": "guc_QR_3G2_5", "QR_veri": "veri_QR_Cat6A", "ROBOT_guc": "guc_ROBOT_3G2_5", "ROBOT_veri": "veri_ROBOT_Cat6A", "modem": "veri_MODEM_Cat6A"}[ad]
            bx, by = B_KABLOLAR[bk]
            son = [(bx, by, 615.0), (bx, by, TEKME_Z0 - UC_DIS)]; ss = "yx"
        elif ist == "TOPPING":
            xg = TOPPING_HARTING[0] + 28.0 + 45.0 + 18.0; zg = TOPPING_HARTING[2] + o
            son = [(2110.0, 2120.0, zg), (2110.0, TOPPING_HARTING[1], zg), (xg, TOPPING_HARTING[1], zg)]; ss = "zy"
        elif ist in ("K", "E"):
            xd = 4300.0 if ist == "K" else 5100.0; yg = 1863.9 + 28.0 + 45.0 + 18.0
            son = [(xd + o, yg + 25.0, -760.0), (xd + o, yg, -760.0)]; ss = "zx"
        elif ist == "A":
            xa = (A_KUTU["x"][0] + A_KUTU["x"][1]) / 2.0 - 30.0; za = (A_KUTU["z"][0] + A_KUTU["z"][1]) / 2.0; yg = A_KUTU["y"][1] + 91.0
            son = [(xa + o, TA["y"][0] + 9.0, za), (xa + o, yg, za)]; ss = "zy"
        elif ist == "F":
            xs = F_INIS["x"] + (-5.5 if tur == "guc" else 5.5); yd = 1055.0 if tur == "guc" else 1070.0
            xg = 2840.0 + (7.0 if tur == "guc" else -6.0); yg = F_KUTU["y"][1] + 91.0; zg = (F_KUTU["z"][0] + F_KUTU["z"][1]) / 2.0
            son = [(xs, 770.0, F_INIS["z"]), (xs, yd, F_INIS["z"]), (xs, yd, zg), (xg, yd, zg), (xg, yg, zg)]; ss = "zy"
        elif ist == "DOLAP":
            yc = D_HARTING[1] + o; zg = D_HARTING[2] + 28.0 + 45.0 + 18.0
            son = [(TS["x"][1] - 10.0, yc, -670.0), (4150.0, yc, -670.0), (4150.0, yc, -505.0), (D_HARTING[0], yc, -505.0), (D_HARTING[0], yc, zg)]; ss = "yz"
        out[ad] = (bas, bsira if ad != "modem" else "", son, ss)
    return out


def eski():
    K = kesitler(); sab = toplama_sabit(K)
    for nm, kes in K.items():
        icinde = [(a, RR[a]) for a in SIRA if nm in ROTA[a]]
        try:
            kes.yerlestir(icinde, sabit=sab if nm == "T" else None, sirali=True)
        except AssertionError:
            kes.poz = {}; kes.yerlestir(icinde, sabit=sab if nm == "T" else None, sirali=False)
    U = uclar(K); out = {}
    for ad, r, mal in KAB:
        bas, bs, son, ss = U[ad]
        out[ad] = (r, mal, hat_yolu(ad, r, bas, [K[n] for n in ROTA[ad]], son, SINIR, JOG, bas_sira=bs, son_sira=ss))
    return out, K


if __name__ == "__main__":
    o, K = eski()
    for ad, (r, mal, pts) in o.items():
        print(ad, r, len(pts), [tuple(round(c, 1) for c in p) for p in pts[:3]], "...", tuple(round(c, 1) for c in pts[-1]))
    for nm in ("UF1", "UF2", "UF3", "UF4", "GV", "FB", "RU", "RL", "FA", "TS", "ZT"):
        print(nm, {a: {k: round(v, 1) for k, v in d.items()} for a, d in K[nm].poz.items()})
