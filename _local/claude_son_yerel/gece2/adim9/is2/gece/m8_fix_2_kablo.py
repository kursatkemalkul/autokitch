# -*- coding: utf-8 -*-
"""MADDE 8 · adim 2 · kablo kopukluk / deliksiz gecis / havada kelepce (kablo.md kritik + orta).
python m8_fix_2_kablo.py giris.glb cikis.glb"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, delik_ucgenler, kenetle, esle, kutu_ucgen, silindir_ucgen, tup, Yuzey
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
def nokta(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).reshape(-1, 3)

# ---------- bilesenleri once cozumle ----------
KLF = g.bul_nokta("ELK_TOPPING__kablo", (1700, 1090, -805))
X_MOTOR = g.bul_nokta("ELK_TOPPING__kablo", (888, 924.5, -700))
X_KEL = g.bul_nokta("ELK_TOPPING__celik", (888, 905, -621))
KART = [g.bul_nokta("ELK_QR_KABLO__kablo", (x, 1680, 1050)) for x in (5160, 5200, 5240, 5280)]
KART_KANAL = g.bul_nokta("ELK_QR_KABLO__kanal", (5100, 1670, 1034))
UPS = [g.bul_nokta("ELK_QR_KABLO__kablo", (4998, 1698, z)) for z in (820, 850)]
KANAL0 = g.bul_nokta("ELK_QR_KABLO__kanal", (4900, 1670, 800))
KANAL2 = g.bul_nokta("ELK_QR_KABLO__kanal", (4995, 1000, 1000))
g.bilesen("ELK_QR_KABLO__kablo", 0)
ISITICI = [b for b in g._bc["ELK_QR_KABLO__kablo"] if (b["hi"] - b["lo"]).max() < 5 and 990 < b["lo"][2] < 1002 and (4979 < b["lo"][0] < 4985 or 5005 < b["lo"][0] < 5011)]
log("isitici uc:", len(ISITICI))
KELEPCE = [("ELK_QR_KABLO__celik", (4956.0, 1960.0, 783.0)), ("ELK_QR_KABLO__celik", (4955.2, 1960.0, 797.0)),
           ("ELK_TOPPING__celik", (2201.7, 1295.0, -732.7)), ("ELK_K__celik", (4193.0, 1110.0, -39.1)), ("ELK_K__celik", (4374.0, 1189.0, -727.6)),
           ("ELK_DOLAP__celik", (3477.5, 476.1, -768.5)), ("ELK_ISTASYON__celik", (3510.3, 2047.9, -790.0)), ("K_ELEKTRIK__celik", (4001.0, 1809.1, -770.0))]
KEL = []
for d, q in KELEPCE:
    try: KEL.append((d, g.bul_nokta(d, q, tol=0.3)))
    except KeyError as e: log("kelepce bulunamadi", e)
PJ = []
for q in ((4025.0, 1174.8, -170.0), (4025.0, 1150.5, -170.0), (4025.1, 1143.3, -170.0)):
    try: PJ.append(g.bul_nokta("K_YAG__celik", q, tol=0.3))
    except KeyError as e: log("pulsajet", e)
YS = Yuzey(g, haric=("ROBOT", "INSAN", "ZEMIN", "URUN"))

# ---------- A . x sol limit + x sifir sensor kablolari (v7'de vardi, kayipti). v7 yolu y 1612'de harc silindirine giriyordu (m7 harc 1497'ye
# tasindi) -> yatay hat silindirin altinda y 1580 / 1585,5; A sag levha + TOPPING sol yan sacta kablo agzi; pano inisi x 1530 / 1536 ----------
R = 2.5
lim = [(1056, 920, -19), (1056, 920, -13), (886, 920, -13), (886, 1580, -13), (886, 1580, -720), (1530, 1580, -720), (1530, 1879.8, -720)]
hom = [(1086, 920, -19), (1086, 920, -13), (1086, 925.5, -13), (880.5, 925.5, -13), (880.5, 1585.5, -13), (880.5, 1585.5, -725.5),
       (1536, 1585.5, -725.5), (1536, 1879.8, -725.5)]
n = g.ekle_dugum("ELK_TOPPING__kablo", np.concatenate([tup(lim, R), tup(hom, R)]), ornek=X_MOTOR)
log("A x sensor kablolari", n)
ASAG = g.bul_nokta("A_GOVDE__sac", (1435.2, 1500, -700)); TSOL = g.bul_nokta("TOPPING_MODUL__sac", (1436.8, 1500, -700))
g.donustur(ASAG, lambda P: delik_ucgenler(P, 0, [1434.5, 1436.0], 1575.0, 1591.0, -731.0, -714.5))
g.donustur(TSOL, lambda P: delik_ucgenler(P, 0, [1436.0, 1437.5], 1575.0, 1591.0, -731.0, -714.5))
log("A sag levha + TOPPING sol yan kablo agzi")
# halka kelepceler (demet kutusu + 1,5 et, boyuna 12) + en yakin yapi yuzune dil
KH = [  # (eksen, merkez, demet lo, demet hi)
    (1, 1093.0, (877.5, -16.0), (889.0, -10.0)),            # dikey (y) hat, x/z
    (1, 1439.0, (877.5, -16.0), (889.0, -10.0)),
    (2, -190.0, (877.5, 1577.5), (889.0, 1588.0)),          # z hatti, x/y
    (2, -543.0, (877.5, 1577.5), (889.0, 1588.0)),
    (0, 1029.0, (1577.5, -728.0), (1588.0, -717.5)),        # x hatti, y/z
    (0, 1300.0, (1577.5, -728.0), (1588.0, -717.5)),
]
KLP = []
for ax, m, dlo, dhi in KH:
    u, w = [i for i in range(3) if i != ax]
    lo = np.zeros(3); hi = np.zeros(3); lo[ax] = m - 6; hi[ax] = m + 6
    lo[u], hi[u] = dlo[0] - 1.5, dhi[0] + 1.5; lo[w], hi[w] = dlo[1] - 1.5, dhi[1] + 1.5
    T = delik_ucgenler(kutu_ucgen(lo, hi), ax, [m - 6, m + 6], dlo[0], dhi[0], dlo[1], dhi[1])
    g.ekle_dugum("ELK_TOPPING__celik", T, ornek=X_KEL); KLP.append((lo, hi, ax))
# ---------- C . KLF6.6 kablo ucu cihazin arka yuzune (klemens kutusu) ----------
g.ekle_dugum("ELK_TOPPING__kablo", tup([(1700, 1087, -805), (1700, 1060, -805), (1700, 1060, -786.0)], 4.1), ornek=KLF)
log("C KLF ucu")

# ---------- D . QR kilit karti uclari x4: kanal ust sacinda parmak yuvasi + uc kart yuzune (z 1070) ----------
DL = []
for b in KART:
    P = nokta(b); sl = P[P[:, 2] > 1050]
    lo, hi = sl.min(0), sl.max(0); DL.append((lo[0] - 1, hi[0] + 1, lo[1] - 1, min(hi[1] + 1, 1685.5)))
    g.donustur(b, lambda P: esle(P, 2, 1060.0, 1070.0, tol=0.05))
def kart_kanal(P):
    for d in DL: P = delik_ucgenler(P, 2, [1033.5, 1035.0], *d)
    return P
g.donustur(KART_KANAL, kart_kanal)
log("D kart uclari", DL)

# ---------- E . UPS uclari x2: UPS yan yuzunden kanal#0 yan sacina dik (delikli) ----------
U0 = g.etiket_b(UPS[0])
for b in UPS: g.sil_b(b)
for z in (820.0, 850.0):
    g.ekle_dugum("ELK_QR_KABLO__kablo", silindir_ucgen((5005.0, 1672.0, z), (5000.0, 1672.0, z), 4.5, 12), None, *U0)
g.donustur(KANAL0, lambda P: delik_ucgenler(delik_ucgenler(P, 0, [5001.5, 5003.0], 1666.5, 1677.5, 814.5, 825.5), 0, [5001.5, 5003.0], 1666.5, 1677.5, 844.5, 855.5))
log("E UPS uclari")

# ---------- F . goz isitici kablolari x12: kanal#2 yan sacindan (delikli) kanal icine ----------
DK = []
for b in ISITICI:
    c = (b["lo"] + b["hi"]) / 2; et = g.etiket_b(b); r = 1.5
    if c[0] < 4995:
        a, e = (b["lo"][0], c[1], c[2]), (4992.0, c[1], c[2]); DK.append(([4983.0, 4984.5], c))
    else:
        a, e = (b["hi"][0], c[1], c[2]), (4998.0, c[1], c[2]); DK.append(([5005.5, 5007.0], c))
    g.ekle_dugum("ELK_QR_KABLO__kablo", silindir_ucgen(a, e, r, 10), None, *et)
def kanal2(P):
    for pl, c in DK: P = delik_ucgenler(P, 0, pl, c[1] - 2.5, c[1] + 2.5, c[2] - 2.5, c[2] + 2.5)
    return P
g.donustur(KANAL2, kanal2)
log("F isitici", len(DK))

# ---------- G . havada kelepceler: dil en yakin YAPI yuzune (M4 percin somunu); ilk carpan kablo/hortum/rakor ise o yon gecersiz ----------
YAPI_DISI = r"kablo|__hava|hortum|rakor|__conta|__on_seffaf"
def dil(lo, hi, dugum, ornek, genis=10.0, kal=1.5, haric_eksen=None, maxd=170.0):
    c = (lo + hi) / 2
    icinde = lambda P: np.all((P.mean(1) >= lo - 0.5) & (P.mean(1) <= hi + 0.5), axis=1)
    best = None
    for ax in range(3):
        if ax == haric_eksen: continue
        u, w = [i for i in range(3) if i != ax]
        gu = min(genis, hi[u] - lo[u]); gw = min(kal, hi[w] - lo[w])
        for sg in (-1, 1):
            d = np.zeros(3); d[ax] = sg
            o = c.copy(); o[ax] = hi[ax] if sg > 0 else lo[ax]
            t = YS.isin(o, d, maxd, atla=icinde, haric_ad=YAPI_DISI + "|^" + dugum + "$")
            if t is None or t < 0.3: continue
            ok = True
            for du in (-gu / 2 - 0.3, 0, gu / 2 + 0.3):
                for dw in (-gw / 2 - 0.3, 0, gw / 2 + 0.3):
                    q = o.copy(); q[u] += du; q[w] += dw
                    ta = YS.isin(q, d, t + 0.5, atla=icinde, haric_ad="^" + dugum + "$")
                    if ta is not None and ta < t - 0.05: ok = False
            if ok and (best is None or t < best[0]): best = (t, ax, sg, o)
    if best is None: return None
    t, ax, sg, o = best
    a = o.copy(); e = o.copy(); e[ax] = o[ax] + sg * t
    u, w = [i for i in range(3) if i != ax]
    lo2 = np.minimum(a, e); hi2 = np.maximum(a, e)
    gu = min(genis, hi[u] - lo[u]); gw = min(kal, hi[w] - lo[w])
    lo2[u] = c[u] - gu / 2; hi2[u] = c[u] + gu / 2
    lo2[w] = c[w] - gw / 2; hi2[w] = c[w] + gw / 2
    g.ekle_dugum(dugum, kutu_ucgen(lo2, hi2), ornek=ornek)
    return round(t, 1), "xyz"[ax], sg
for lo, hi, ax in KLP: log("A kelepce dili", lo.round(0), dil(lo, hi, "ELK_TOPPING__celik", X_KEL, haric_eksen=ax))
for d, b in KEL:
    if d == "K_ELEKTRIK__celik": log("G", d, "hava giris rakoru: modul arasi duvar gecisi, kelepce degil -> dokunulmadi"); continue
    log("G kelepce dili", d, b["lo"].round(0), dil(b["lo"], b["hi"], d, b))

# H . PulsaJet: nozul_braketi + kelepce bloklari + giris dirsegi zaten var (tarayici yanlis pozitif) -> dokunulmadi
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
