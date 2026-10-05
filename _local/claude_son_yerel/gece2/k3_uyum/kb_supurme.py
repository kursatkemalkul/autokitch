# -*- coding: utf-8 -*-
"""adım 54 denetimi: (1) yerinde boşluk hortum hattı ↔ kuşbaşı parçaları (3B en kısa mesafe)
(2) çıkarma süpürmesi: hareketli küme +z (öne) ya da +y (yukarı, raf altına kadar) ötelenir; engel ile x–y (öne) / x–z (yukarı) izdüşümü
    çakışması + süpürülen aralıkta z / y örtüşmesi = temas. İzdüşüm 0,25 mm ızgarada; boşluk = izdüşümler arası en kısa 2B mesafe (EDT)."""
import sys, os, json, numpy as np
Z = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
sys.path.insert(0, os.path.join(Z, "gece")); sys.path.insert(0, Z)
from m8kit import Glb
import trimesh
from scipy import ndimage
gi = sys.argv[1]
g = Glb(gi)
KOD = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
LO = np.array([1690, 1000, -700.0]); HI = np.array([2240, 1560, 50.0])
B = []
for d in sorted(set(p["name"] for p in g.prims if p["name"].startswith("TOPPING"))):
    try: g.bilesen(d, no=0)
    except Exception: continue
    for b in g._bc[d]:
        if np.all(b["hi"] > LO) and np.all(b["lo"] < HI):
            p, t = b["parca"][0]; kat, mek, kpk = g._etiketler(p, t[0])
            P = np.concatenate([q["X"][q["T"][tt]] for q, tt in b["parca"]])
            B.append(dict(ad="%s[%d]" % (d, b["no"]), mek=KOD[mek] if mek is not None else "", lo=b["lo"], hi=b["hi"], P=P))
SABIT_KB = ("TOPPING_MODUL__paslanmaz[44]", "TOPPING_MODUL__paslanmaz[47]", "TOPPING_MODUL__conta[5]", "TOPPING_MODUL__pom[7]")
kb = [b for b in B if b["mek"] == "TOPPING/Kuşbaşı"]
huni = [b for b in kb if np.allclose(b["lo"], [1753, 1284, -560], atol=0.5)]
assert len(huni) == 1, len(huni)
uno = [b for b in kb if b["ad"] not in SABIT_KB]
hortum = [b for b in B if b["mek"] == "TOPPING/Kıyma" and b["hi"][1] <= 1560 and b["lo"][0] > 1880 and b["hi"][0] < 1945]
kasar = [b for b in B if b["mek"] == "TOPPING/Kaşar" and b["lo"][0] < 2000 and b["lo"][1] < 1560]
print("kuşbaşı %d (UNO hareketli %d, sabit %s) · hortum hattı %d · kaşar %d" % (len(kb), len(uno), [b["ad"] for b in kb if b["ad"] in SABIT_KB], len(hortum), len(kasar)))
for b in hortum: print("  hortum hattı:", b["ad"], np.round(b["lo"], 1), np.round(b["hi"], 1))


def tm(L):
    return trimesh.Trimesh(vertices=np.concatenate([b["P"] for b in L]).reshape(-1, 3), faces=np.arange(sum(len(b["P"]) for b in L) * 3).reshape(-1, 3), process=False)


def ornek(L, n=15000):
    m = tm(L); p, _ = trimesh.sample.sample_surface_even(m, n, seed=1) if False else trimesh.sample.sample_surface(m, n, seed=1)
    return np.r_[p, m.vertices]


def min_mesafe(A, Bl):
    """A ile B arasındaki en kısa mesafe (iki yönlü örnek nokta → yüzey)"""
    ma, mb = tm(A), tm(Bl)
    d1 = trimesh.proximity.closest_point(mb, ornek(A))[1].min()
    d2 = trimesh.proximity.closest_point(ma, ornek(Bl))[1].min()
    return float(min(d1, d2))


RAP = dict(girdi=os.path.basename(gi))
# (1) yerinde boşluk
RAP["yerinde"] = {}
for ad, L in (("huni", huni), ("UNO_govde_vana", [b for b in uno if b is not huni[0]]), ("kusbasi_sabit_cikis", [b for b in kb if b["ad"] in SABIT_KB])):
    d = min_mesafe(L, hortum); RAP["yerinde"][ad + "__hortum_hatti"] = round(d, 2)
    d2 = min_mesafe(L, kasar); RAP["yerinde"][ad + "__kasar"] = round(d2, 2)
print("yerinde:", RAP["yerinde"])

H = 0.25


def izdusum(L, i, j, kay=(0.0, 0.0), alan=None):
    """L üçgenlerinin (i, j) eksen izdüşümü ızgarada (kay: ötelenme)"""
    x0, x1, y0, y1 = alan
    nx, ny = int((x1 - x0) / H) + 1, int((y1 - y0) / H) + 1
    G_ = np.zeros((nx, ny), bool)
    for b in L:
        P = b["P"][:, :, [i, j]] + np.array(kay)
        for T in P:
            lo = T.min(0); hi = T.max(0)
            a0, a1 = int((lo[0] - x0) / H), int((hi[0] - x0) / H) + 1
            b0, b1 = int((lo[1] - y0) / H), int((hi[1] - y0) / H) + 1
            if a1 < 0 or b1 < 0 or a0 >= nx or b0 >= ny: continue
            a0, b0 = max(a0, 0), max(b0, 0); a1, b1 = min(a1, nx - 1), min(b1, ny - 1)
            X, Y = np.meshgrid(x0 + H * np.arange(a0, a1 + 1), y0 + H * np.arange(b0, b1 + 1), indexing="ij")
            v0, v1, v2 = T
            d = (v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1])
            if abs(d) < 1e-12:      # dik üçgen (izdüşümü çizgi): uç noktaları ve orta noktayı işaretle
                for q in (v0, v1, v2, (v0 + v1) / 2, (v1 + v2) / 2, (v0 + v2) / 2):
                    ii, jj = int(round((q[0] - x0) / H)), int(round((q[1] - y0) / H))
                    if 0 <= ii < nx and 0 <= jj < ny: G_[ii, jj] = True
                continue
            l1 = ((v1[1] - v2[1]) * (X - v2[0]) + (v2[0] - v1[0]) * (Y - v2[1])) / d
            l2 = ((v2[1] - v0[1]) * (X - v2[0]) + (v0[0] - v2[0]) * (Y - v2[1])) / d
            l3 = 1 - l1 - l2
            e = -H * 0.75 / max(np.abs([d]).max() ** 0.5, 1e-6)
            m = (l1 >= -1e-9 - 0.02) & (l2 >= -0.02) & (l3 >= -0.02)
            G_[a0:a1 + 1, b0:b1 + 1] |= m
    return G_


def supur(ad, M, O, yon, kay_on=0.0, sinir=None):
    """yon 'z' (öne, M izdüşümü x–y) ya da 'y' (yukarı, izdüşüm x–z). Engel yalnız M'nin süpürdüğü aralıkta (yon ekseninde M'nin önünde)."""
    if yon == "z": i, j, k = 0, 1, 2
    else: i, j, k = 0, 2, 1
    mlo = min(b["lo"][k] for b in M)
    mhi = max(b["hi"][k] for b in M)
    ust = sinir if sinir is not None else 1e9
    O2 = [b for b in O if b["hi"][k] > mlo and b["lo"][k] < ust]
    if not O2: return dict(temas=False, bosluk_2B=None, engel=[])
    pts = np.concatenate([b["P"].reshape(-1, 3) for b in M + O2])
    alan = (pts[:, i].min() - 5, pts[:, i].max() + 5, pts[:, j].min() - 5, pts[:, j].max() + 5)
    kay = [0.0, 0.0]
    if yon == "z" and kay_on: kay[1] = kay_on            # öne çekmeden önce yukarı kaldırma (y)
    GM = izdusum(M, i, j, tuple(kay), alan)
    out = dict(temas=False, engel=[])
    dist = ndimage.distance_transform_edt(~GM) * H
    mi = (min(b["lo"][i] for b in M), max(b["hi"][i] for b in M)); mj = (min(b["lo"][j] for b in M) + kay[1], max(b["hi"][j] for b in M) + kay[1])
    for b in O2:
        if b["lo"][i] > mi[1] + 30 or b["hi"][i] < mi[0] - 30 or b["lo"][j] > mj[1] + 30 or b["hi"][j] < mj[0] - 30: continue
        GO = izdusum([b], i, j, (0.0, 0.0), alan)
        if not GO.any(): continue
        ort = (GM & GO).sum() * H * H
        dm = float(dist[GO].min())
        if ort > 0.0625 * 4: out["temas"] = True
        out["engel"].append(dict(ad=b["ad"], mek=b["mek"], ortusme_mm2=round(float(ort), 2), bosluk_2B=round(dm, 2)))
    out["engel"].sort(key=lambda e: (-e["ortusme_mm2"], e["bosluk_2B"]))
    out["bosluk_2B_min"] = min((e["bosluk_2B"] for e in out["engel"] if e["ortusme_mm2"] == 0), default=None)
    print(ad, "temas" if out["temas"] else "TEMAS YOK", out["engel"][:6])
    return out


O_ = hortum + kasar
RAP["supurme"] = {}
RAP["supurme"]["huni_one"] = supur("huni öne", huni, O_, "z")
RAP["supurme"]["huni_yukari_raf_altina"] = supur("huni yukarı", huni, O_, "y", sinir=1534.0)
RAP["supurme"]["UNO_one"] = supur("UNO (huni+gövde+vana) öne", uno, O_, "z")
RAP["supurme"]["UNO_yukari30_one"] = supur("UNO 30 kaldır + öne", uno, O_, "z", kay_on=30.0)
RAP["UNO_parca"] = [[b["ad"], np.round(b["lo"], 1).tolist(), np.round(b["hi"], 1).tolist()] for b in uno]
json.dump(RAP, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kb_supurme_%s.json" % os.path.basename(gi)[:-4]), "w", encoding="utf8"),
          ensure_ascii=False, indent=1, default=float)
