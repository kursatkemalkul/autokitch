# -*- coding: utf-8 -*-
"""elk4 ek işler (Kemal): 1 yayıcı döner aktüatörleri + 4 yayıcı hortumu kalkar (yayıcı sabit) · 2 ana şalter ana pano kapağında (kapı tipi döner kollu)
· 3 hava hortumları YEŞİL. b4.py içinden çağrılır: calistir(G, KAY, rapor, Yeni-nesnesi, MEKL)"""
import re, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from elib import kutu, silindir

SPR = {"harc": 1722.0, "sos": 2259.5}; SPR_Y = 1194.05
HORTUM_KAY = (8, 9, 15, 16)                       # harç A/B (x 1745), sos A/B (x 2228/2239)
GECIS = {"harc": 1745.0, "sos": 2239.0}           # soğuk oda duvar geçiş kovanı (silikon) x
YESIL = [0.027, 0.34, 0.078, 1.0]                 # sRGB #2e9e4f -> doğrusal


def komps(G, p):
    vis = G.gorunur(p); idx = np.where(vis)[0]
    if not len(idx): return []
    P = p["X"][p["T"][idx]]
    Pq = np.round(P.reshape(-1, 3), 2); u, inv = np.unique(Pq, axis=0, return_inverse=True); Ti = inv.reshape(-1, 3)
    rr = np.r_[Ti[:, 0], Ti[:, 1]]; cc = np.r_[Ti[:, 1], Ti[:, 2]]
    _, lab = connected_components(coo_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(u), len(u))), directed=False); tl = lab[Ti[:, 0]]
    out = []
    for c in np.unique(tl):
        m = tl == c; Q = P[m].reshape(-1, 3); out.append((idx[m], Q.min(0), Q.max(0)))
    return out


def sil_kutu_ici(G, ad_re, lo, hi, rapor, etiket, maxboy=None):
    n = 0
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    for p in G.prims:
        if p.get("gizli") or not re.match(ad_re, p["name"]): continue
        for tri, a, b in komps(G, p):
            if np.all(a >= lo) and np.all(b <= hi) and (maxboy is None or np.max(b - a) <= maxboy):
                m = np.zeros(len(p["T"]), bool); m[tri] = True; n += G.sil(p, m)
    rapor("sil %s %s" % (etiket, np.round(lo).tolist()), n)
    return n


def seg_uzak(P, segs):
    best = 1e9
    for a, b, r in segs:
        v = b - a; L2 = max(v @ v, 1e-9); t = np.clip((P - a) @ v / L2, 0, 1); best = min(best, np.linalg.norm(a + t * v - P) - r)
    return best


def calistir(G, KAY, rapor, Y, MEKL, KAT):
    # ---------------------------------------------------------------- 1 · yayıcı aktüatörleri + hortumları
    hsegs = []
    for ci in HORTUM_KAY:
        d = KAY[ci]; p = G.prims[d["pi"]]; assert p["name"] == "TOPPING_MODUL__hava_ana"
        m = np.zeros(len(p["T"]), bool); m[d["tri"]] = True
        rapor("sil yayıcı hortumu #%d" % ci, G.sil(p, m)); hsegs += [(q["a"], q["b"], q["r"]) for q in d["S"]]
    for nm, xc in SPR.items():
        sil_kutu_ici(G, r"TOPPING_MODUL__(aluminyum|celik|paslanmaz)$", (xc - 16, 1176, -151), (xc + 16, 1216, -105), rapor, "%s CRB2 aktüatör + plaka + kaplin + vida" % nm)
        sil_kutu_ici(G, r"TOPPING_MODUL__hava_ana$", (xc - 25, 1170, -126), (xc + 25, 1220, -100), rapor, "%s aktüatör M5 rakorları" % nm)
    # hortum P-kelepçeleri (hortum ekseninden ≤ 6 mm) + KD3 lamaları (çift kelepçe, perçin)
    n = 0
    for p in G.prims:
        if p.get("gizli") or p["name"] != "TOPPING_MODUL__celik": continue
        for tri, a, b in komps(G, p):
            if np.max(b - a) > 40: continue
            if seg_uzak((a + b) / 2, hsegs) < 6.0:
                m = np.zeros(len(p["T"]), bool); m[tri] = True; n += G.sil(p, m)
    rapor("sil yayıcı hortumu P-kelepçeleri", n)
    for xk in (2100.0, 2190.0):
        sil_kutu_ici(G, r"TOPPING_MODUL__celik$", (xk - 11, 1249, -769), (xk + 11, 1286, -718), rapor, "KD3 lama + çift kelepçe x %d" % xk)
    # ada uç rakorları (hortum ucundaki itmeli rakor gövdeleri)
    for lo, hi in (((1739, 1239, -756), (1751, 1252, -682)), ((1996, 1272, -756), (2012, 1284, -716))):
        sil_kutu_ici(G, r"TOPPING_MODUL__hava_ana$", lo, hi, rapor, "yayıcı hortumu ada rakoru")
    # soğuk oda duvar geçiş kovanları -> sil, delik kapanır (paslanmaz + PU + paslanmaz yama)
    for nm, xg in GECIS.items():
        ps = [p for p in G.prims if p["name"] == "TOPPING_MODUL__silikon" and not p.get("gizli")]
        lo = np.array([xg - 6, 1150, -632]); hi = np.array([xg + 6, 1178, -568]); fo = None
        for p in ps:
            for tri, a, b in komps(G, p):
                if np.all(a >= lo) and np.all(b <= hi):
                    m = np.zeros(len(p["T"]), bool); m[tri] = True; G.sil(p, m)
                    fo = (np.minimum(fo[0], a), np.maximum(fo[1], b)) if fo else (a, b)
        rapor("sil %s duvar geçiş kovanı" % nm, 0 if fo is None else 1)
        if fo is None: continue
        x0, x1, y0, y1 = fo[0][0], fo[1][0], fo[0][1], fo[1][1]
        for ad, z0, z1 in (("TOPPING_MODUL__paslanmaz", -630.0, -628.5), ("TOPPING_MODUL__pu", -628.5, -571.0), ("TOPPING_MODUL__paslanmaz", -571.0, -570.0)):
            p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
            P = p["X"][p["T"]]; c = P.mean(1); d_ = np.linalg.norm(c - np.array([xg + 30, 1190, (z0 + z1) / 2]), axis=1); d_[~G.gorunur(p)] = 1e18
            et = G._etiketler(p, int(np.argmin(d_)))
            G._ekle_dunya(p, kutu((x0, y0, z0), (x1, y1, z1)), *et)
        rapor("yama %s duvar deliği x %.0f–%.0f y %.0f–%.0f" % (nm, x0, x1, y0, y1), 3)
    # sabit paslanmaz bağlantı parçası (kaplin yerine, valf mili sabitlenir): Ø12 × 8 tapa + Ø16 × 2 flanş
    MALP = ("ME4_paslanmaz_sabit", (0.80, 0.81, 0.82, 1.0), 0.9, 0.3)
    for nm, xc in SPR.items():
        mk = MEKL.index("TOPPING/Harç" if nm == "harc" else "TOPPING/Sos")
        g = np.concatenate([silindir((xc, SPR_Y, -144.0), (xc, SPR_Y, -136.0), 6.0, 24), silindir((xc, SPR_Y, -136.0), (xc, SPR_Y, -134.0), 8.0, 24)])
        Y.ekle("TOPPING_MODUL__yayici_sabit_baglanti", MALP, g, KAT["MEKANIZMA"], mk)
        rapor("yeni %s yayıcı sabit paslanmaz bağlantı (Ø12×8 + Ø16×2 flanş)" % nm, len(g))
    # ---------------------------------------------------------------- 2 · ana şalter: ana pano KAPAĞINDA kapı tipi döner kollu ayırıcı
    mk = MEKL.index("Elektrik/Ana pano"); E = KAT["ELEKTRIK"]
    xc, yc = 3745.0, 2110.0
    govde = kutu((xc - 45, yc - 40, -185.0), (xc + 45, yc + 35, -91.0))           # şalter gövdesi (kapağın iç yüzüne montaj, 90 × 90 × 95)
    mil = silindir((xc, yc, -91.0), (xc, yc, -87.0), 6.0, 20)                       # kapak geçiş mili
    sari = kutu((xc - 37, yc - 37, -87.0), (xc + 37, yc + 37, -85.0))               # sarı ön plaka (74 × 74)
    kir = np.concatenate([silindir((xc, yc, -85.0), (xc, yc, -75.0), 24.0, 32), kutu((xc - 9, yc - 33, -75.0), (xc + 9, yc + 33, -63.0))])
    Y.ekle("ELK_ANA_PANO_UF__salter__KAPAK_ANA_PANO", ("ME4_salter_gri", (0.55, 0.56, 0.58, 1.0), 0.2, 0.6), np.concatenate([govde, mil]), E, mk)
    Y.ekle("ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO", ("ME4_salter_sari", (0.95, 0.75, 0.05, 1.0), 0.0, 0.5), sari, E, mk)
    Y.ekle("ELK_ANA_PANO_UF__salter_kirmizi__KAPAK_ANA_PANO", ("ME4_salter_kirmizi", (0.80, 0.05, 0.05, 1.0), 0.0, 0.5), kir, E, mk)
    from m8kit import delik_ucgenler
    for p in G.prims:
        if p["name"] in ("ELK_ANA_PANO_UF__pano__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__conta__KAPAK_ANA_PANO") and not p.get("gizli"):
            P = p["X"][p["T"]]; vis = G.gorunur(p)
            mm = vis & np.all(P.max(1) >= [xc - 8, yc - 8, -91], 1) & np.all(P.min(1) <= [xc + 8, yc + 8, -86], 1)
            nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1)[:, None], 1e-12)
            mm &= (np.abs(nn[:, 2]) > 0.999)
            if not mm.any(): continue
            duz = sorted(set(np.round(P[mm][:, 0, 2], 3).tolist())); gr = {}
            for t in np.where(mm)[0]: gr.setdefault(G._etiketler(p, t), []).append(t)
            for et, tt in gr.items():
                Q = P[np.array(tt)]
                for dz in duz: Q = delik_ucgenler(Q, 2, [dz], xc - 6.5, xc + 6.5, yc - 6.5, yc + 6.5)
                mk = np.zeros(len(P), bool); mk[np.array(tt)] = True; G.sil(p, mk); G._ekle_dunya(p, Q, *et)
            rapor("kapak mil deliği %s" % p["name"], int(mm.sum()))
    rapor("yeni ana şalter (kapı tipi döner kollu ayırıcı) ana pano kapağında x %.0f y %.0f" % (xc, yc), 1)
    # ---------------------------------------------------------------- 3 · hava hortumları yeşil
    J = G.J
    J["materials"].append({"name": "ME4_hava_yesil", "pbrMetallicRoughness": {"baseColorFactor": YESIL, "metallicFactor": 0.0, "roughnessFactor": 0.55}, "doubleSided": True})
    mi = len(J["materials"]) - 1; n = 0
    for p in G.prims:
        if re.search(r"__(hava|hava_ana)$", p["name"]):
            p["pr"]["material"] = mi; n += 1
    rapor("hava hortumu primitifleri yeşil (#2e9e4f)", n)
