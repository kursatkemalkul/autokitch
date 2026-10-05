# -*- coding: utf-8 -*-
"""v8zo ON YUZ DERZ HIZASI. python derz_hiza.py giris.glb cikis.glb
1) K6 cekmece onleri + B soguk depo / sogutma menfez paneli arasindaki dikey derz 4009.5|4012.5 -> 4000|4003 (ustteki F|K derzi ile tek cizgi)
2) K / B ile E arasindaki dikey derz: K 4398 (4 mm), B 4400 (2 mm) -> ikisi de 4399 | E 4402 (3 mm, tek cizgi)
Yalniz kapak/panel kenarlari (kose kaydirma); govde, mekanizma, firin, E dokunulmaz."""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(S, "gece"))
from m8kit import Glb

g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)


def isle(dugum, lo, hi, kural, yalniz_kpk=True):
    """dugum primlerinde tum koseleri [lo,hi] kutusunda olan ucgenler -> kural(x dizisi) -> yeni x"""
    lo = np.array(lo, float); hi = np.array(hi, float); top = 0
    for p in g.dprims(dugum):
        if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
        T = p["T"]; P = p["X"][T]
        vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
        m = vis & np.all(P.min(1) >= lo - 0.01, 1) & np.all(P.max(1) <= hi + 0.01, 1)
        if yalniz_kpk and p["pr"].get("extras", {}).get("kpk") is not None:
            m &= g.kpk_maske(p)
        tri = np.where(m)[0]
        if not len(tri): continue
        def f(Q):
            Q = Q.copy(); Q[..., 0] = kural(Q[..., 0]); return Q
        g.donustur(dict(parca=[(p, tri)]), f); top += len(tri)
        once = P[tri][..., 0]; sonra = kural(once.copy())
        log("%-38s ucgen %4d  x %.2f-%.2f -> %.2f-%.2f" % (dugum, len(tri), once.min(), once.max(), sonra.min(), sonra.max()))
    assert top > 0, dugum
    return top


def kenar(sol=None, sag=None, orta=None):
    """sol=(esik, d): x<=esik -> +d ; sag=(esik, d): x>=esik -> +d ; orta=(a, b, d): a<x<b -> +d"""
    def k(x):
        y = x.copy()
        if sol: y[x <= sol[0] + 0.01] += sol[1]
        if sag: y[x >= sag[0] - 0.01] += sag[1]
        if orta: y[(x > orta[0]) & (x < orta[1])] += orta[2]
        return y
    return k


# 1) K6 cekmece onleri (on sac + conta): sag yari -9.5 (sol kenar 3402.5 sabit, K5 ile hizali)
for ad, y0, y1 in (("CEK_K6_tatli_1__on_seffaf__CEKMECE", 125, 291), ("CEK_K6_ic1_1__on_seffaf__CEKMECE", 293, 454),
                   ("CEK_K6_ic1_2__on_seffaf__CEKMECE", 456, 786)):
    isle(ad, (3400, y0, 20), (4010, y1, 80), kenar(sag=(3705.75, -9.5)))

# 2) B sogutma menfez paneli: sol kenar -9.5, sag kenar -1, panjur grubu ortalanir (+1.5: 40.5 | 40.5 kenar payi)
isle("B_SOGUTMA__sac", (4012.4, 125.9, 38.9), (4400.1, 453.6, 79.1), kenar(sol=(4014.0, -9.5), sag=(4398.5, -1.0), orta=(4030, 4370, 1.5)))
#    panel tespit civatalari (kapakla birlikte)
isle("B_SOGUTMA__celik", (4013.9, 189.9, 23.9), (4030.1, 410.1, 45.1), lambda x: x - 9.5)
isle("B_SOGUTMA__celik", (4371.4, 189.9, 23.9), (4398.6, 410.1, 45.1), lambda x: x - 1.0)

# 3) B soguk depo cekmece onu (sac + pu): sol kenar -9.5, sag kenar -1
isle("B_DEPO__sac__CEKMECE", (4012.4, 456.4, 38.9), (4400.1, 785.1, 79.1), kenar(sol=(4014.0, -9.5), sag=(4398.5, -1.0)))
isle("B_DEPO__pu__CEKMECE", (4013.9, 457.9, 39.9), (4398.6, 783.6, 77.6), kenar(sol=(4014.0, -9.5), sag=(4398.5, -1.0)))

# 4) K on kapagi: sag kenar +1 (4398 -> 4399); ic tava + kose parcalari birlikte. Mandal plakalari (<=4388) sabit
isle("K_GOVDE__on_seffaf", (4002.9, 786, 58.9), (4400, 2199, 79.1), lambda x: np.where(x > 4390, x + 1.0, x))
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.join(HERE, "derz_hiza_log.txt"), "w", encoding="utf-8").write("\n".join(LOG))
