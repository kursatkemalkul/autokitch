# -*- coding: utf-8 -*-
"""GECE2 ADIM 2 · A + B: QR hizalama (x -200, sag dis yuz = E sag dis yuzu 5230) + zemin kanali/kablolar/robot zemin kutusu
QR ile birlikte + zemin doseme delikleri yeniden + tezgah: ince duvar saci + aski + ince duvar kosebendi KALKAR, tezgah 180 derece
doner (dusey eksen, govde merkezi) ve x -620 kayar (on yuz +x, acilma yollari QR govdesine / QR musteri kapisi suprume alanina girmez)
+ siparis animasyonlarinda kutu/urun QR'a giris yolu (son x kaymasi) yeni goz konumuna.
python a1_qr_tezgah.py giris.glb cikis.glb"""
import sys, os, json, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(S, "gece")); sys.path.insert(0, S); sys.path.insert(0, os.path.join(S, "elk2"))
from m8kit import Glb, kutu_ucgen
from elib import KAT as KATD

DX_QR = -200.0          # QR sag dis yuzu 5430 -> 5230 (E sag dis yuzu)
ESIK_ZEMIN = 4400.0     # zemin kanali / kablo: bu x'in sagindaki koseler QR ile birlikte kayar
# tezgah
CX, CZ = (3842.0 + 4505.0) / 2, (1044.0 + 1874.0) / 2     # govde (tabla) merkezi
DX_TZ = -620.0

g = Glb(sys.argv[1]); LOG = []
def log(*a): s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)
MEK = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
QR_M = [i for i, k in enumerate(MEK) if k.startswith("QR/")]
TZ_M = [i for i, k in enumerate(MEK) if k.startswith("Tezgâh/")]
DH = MEK.index("Çevre/Dükkân hattı")


def mek_dizi(p):
    n = len(p["T"]); a = np.full(n, -1, int); L = p["pr"].get("extras", {}).get("mek") or []
    for k in range(0, len(L) - 2, 3): a[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    return a


def normal_yaz(p, vs, f):
    """vs koselerinin NORMAL'ini f(N) ile degistir (BIN icinde, yerinde)"""
    pr = p["pr"]; ai = pr["attributes"]["NORMAL"]
    assert ai not in g.paylasim, ("paylasilan normal", p["name"])
    A = g.J["accessors"][ai]; v = g.J["bufferViews"][A["bufferView"]]
    off = v.get("byteOffset", 0) + A.get("byteOffset", 0)
    N = np.frombuffer(bytes(g.BIN[off:off + A["count"] * 12]), np.float32).reshape(-1, 3).copy()
    N[vs] = f(N[vs]); g.BIN[off:off + N.nbytes] = N.astype(np.float32).tobytes()
    A.pop("min", None); A.pop("max", None)


def tasi_mek(mekler, f, fn=None, ad_filtre=None, kosul_v=None):
    """mek etiketi 'mekler' icinde olan gorunur ucgenlerin koselerini f ile tasi (normaller fn ile). Paylasilan kose olmamali."""
    top = 0; tri_top = 0
    for p in g.prims:
        if p.get("gizli") or "mek" not in p["pr"].get("extras", {}): continue
        if ad_filtre and not ad_filtre(p["name"]): continue
        a = mek_dizi(p); vis = g.gorunur(p)
        m = vis & np.isin(a, mekler)
        if not m.any(): continue
        vs = np.unique(p["T"][m].reshape(-1))
        diger = np.unique(p["T"][vis & ~m].reshape(-1))
        ortak = np.intersect1d(vs, diger)
        if kosul_v is not None:
            vs = vs[kosul_v(p["X"][vs])]
            ortak = np.intersect1d(vs, diger)
        assert not len(ortak), ("paylasilan kose", p["name"], len(ortak))
        if not len(vs): continue
        p["X"][vs] = f(p["X"][vs].copy()); p["degX"] = True
        if fn is not None: normal_yaz(p, vs, fn)
        top += len(vs); tri_top += int(m.sum())
    return top, tri_top


# ---------------------------------------------------------------- A · QR
n, t = tasi_mek(QR_M, lambda X: X + np.array([DX_QR, 0, 0]))
log("QR (tum QR/* mekanizmalari) x %+.0f: kose %d ucgen %d" % (DX_QR, n, t))
# zemin kanali + kablolar + robot zemin kutusu (Cevre/Dukkan hatti, ELK_ZEMIN__*): x > 4400 koseler QR ile birlikte
def zkos(X): return X[:, 0] > ESIK_ZEMIN
n, t = tasi_mek([DH], lambda X: X + np.array([DX_QR, 0, 0]), ad_filtre=lambda a: a.startswith("ELK_ZEMIN__"), kosul_v=zkos)
log("zemin kanali / kapak / kablo / robot zemin kutusu: x>%.0f koseler x %+.0f: kose %d" % (ESIK_ZEMIN, DX_QR, n))

# zemin doseme: delikler = zemin kapak saclarinin ust yuzu (yeniden kurulur)
kp = [p for p in g.dprims("ELK_ZEMIN__kapak") if not p.get("gizli")]
R = []
for p in kp:
    tl, kut = g.komp(p)
    for i, (lo, hi, nn) in kut.items(): R.append((lo[0], hi[0], lo[2], hi[2]))
R = sorted(set((round(a, 2), round(b, 2), round(c, 2), round(d, 2)) for a, b, c, d in R))
log("zemin kapaklari (delik):", R)
zp = [p for p in g.dprims("ZEMIN_DOSEME__zemin_karo") if not p.get("gizli")]
assert len(zp) == 1; zp = zp[0]
Pz = zp["X"][zp["T"][g.gorunur(zp)]]
X0, X1 = Pz[..., 0].min(), Pz[..., 0].max(); Z0, Z1 = Pz[..., 2].min(), Pz[..., 2].max(); Y0 = float(np.median(Pz[..., 1]))
alan0 = 0.5 * np.abs(np.cross(Pz[:, 1] - Pz[:, 0], Pz[:, 2] - Pz[:, 0])[:, 1]).sum()
xs = sorted(set([X0, X1] + [v for r in R for v in r[:2] if X0 < v < X1])); zs = sorted(set([Z0, Z1] + [max(Z0, min(Z1, v)) for r in R for v in r[2:]]))
yeni = []
for xa, xb in zip(xs[:-1], xs[1:]):
    for za, zb in zip(zs[:-1], zs[1:]):
        xm, zm = (xa + xb) / 2, (za + zb) / 2
        if any(r[0] < xm < r[1] and r[2] < zm < r[3] for r in R): continue
        a = np.array([xa, Y0, za]); b = np.array([xb, Y0, za]); c = np.array([xb, Y0, zb]); d = np.array([xa, Y0, zb])
        yeni += [(a, d, c), (a, c, b)]          # ust yuz +y
yeni = np.array(yeni)
nrm = np.cross(yeni[:, 1] - yeni[:, 0], yeni[:, 2] - yeni[:, 0]); assert (nrm[:, 1] > 0).all()
alan1 = 0.5 * np.abs(nrm[:, 1]).sum()
et = g._etiketler(zp, int(np.where(g.gorunur(zp))[0][0]))
g.sil(zp, np.ones(len(zp["T"]), bool)); g._ekle_dunya(zp, yeni, *et)
alan_delik = sum((min(r[1], X1) - max(r[0], X0)) * (min(r[3], Z1) - max(r[2], Z0)) for r in R)
log("zemin doseme yeniden: ucgen %d, alan %.0f (once %.0f) · beklenen %.0f" % (len(yeni), alan1, alan0, (X1 - X0) * (Z1 - Z0) - alan_delik))

# ---------------------------------------------------------------- B · tezgah
SIL = [("DUZ_TEZGAH_DUVAR__paslanmaz", (3800, 990, 1030), (4510, 1710, 1050)),     # ince duvar kaplama saci
       ("TEZGAH_ASKI__paslanmaz", (3900, 1590, 1030), (4500, 1670, 1120)),         # 3 kanca
       ("TEZGAH_ASKI__aluminyum", (3900, 1590, 1030), (4500, 1670, 1120)),         # aski rayi
       ("TEZGAH_GOVDE__paslanmaz", (3890, 825, 1035), (4490, 875, 1072))]          # ince duvar kosebendi
for ad, lo, hi in SIL:
    k = 0
    for p in g.dprims(ad):
        if p.get("gizli"): continue
        m = g.kutu_maske(p, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        k += g.sil(p, m)
    assert k > 0, ad
    log("tezgah sil %-30s ucgen %d" % (ad, k))


def don(X):
    Y = X.copy(); Y[:, 0] = 2 * CX - X[:, 0] + DX_TZ; Y[:, 2] = 2 * CZ - X[:, 2]; return Y


def don_n(N):
    M = N.copy(); M[:, 0] = -N[:, 0]; M[:, 2] = -N[:, 2]; return M


n, t = tasi_mek(TZ_M, don, don_n)
log("tezgah (Govde + Bulasik + Evye + sokak duvar saci) 180 derece (eksen x %.1f z %.1f) + x %+.0f: kose %d ucgen %d" % (CX, CZ, DX_TZ, n, t))

# ---------------------------------------------------------------- animasyon: kutu + urun QR'a giris
J = g.J
def acc_oku(i):
    A = J["accessors"][i]; v = J["bufferViews"][A["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[A["type"]]
    off = v.get("byteOffset", 0) + A.get("byteOffset", 0)
    r = np.frombuffer(bytes(g.BIN[off:off + A["count"] * n * 4]), np.float32).copy()
    return r.reshape(-1, n) if n > 1 else r
ad_ni = {nd.get("name"): i for i, nd in enumerate(J["nodes"])}
KOK = ad_ni["E_KUTU__B_ROOT"]
for an in J["animations"]:
    ch = {(c["target"]["node"], c["target"]["path"]): an["samplers"][c["sampler"]] for c in an["channels"]}
    sk = ch.get((KOK, "translation"))
    if sk is None: continue
    ti = acc_oku(sk["input"]); to = acc_oku(sk["output"])
    # QR'a son yaklasma: kok x'in 4.4'ten ayrildigi ilk kare -> son kare
    x0 = to[0, 0]; ii = np.where(np.abs(to[:, 0] - x0) > 1e-5)[0]
    if not len(ii): log("anim %s: kutu x hareketi yok" % an["name"]); continue
    t_bas = ti[max(ii[0] - 1, 0)]; xs_son = to[-1, 0]; dx_eski = xs_son - x0
    dx_yeni = dx_eski + DX_QR / 1000.0
    def dxt(tq, ti=ti, to=to, x0=x0, dx_eski=dx_eski, dx_yeni=dx_yeni, t_bas=t_bas):
        xb = np.interp(tq, ti, to[:, 0]); f = np.where(tq >= t_bas, (xb - x0) / dx_eski, 0.0)
        return f * (dx_yeni - dx_eski)
    kac = 0
    for (nd, path), sm in ch.items():
        if path != "translation": continue
        nm = J["nodes"][nd]["name"]
        if not (nd == KOK or nm.startswith("URUN__")): continue
        I = acc_oku(sm["input"]); O = acc_oku(sm["output"])
        if np.interp(t_bas, I, O[:, 0]) < 4.3 and nd != KOK: continue      # kutuda olmayan (gizli / baska yerde) urun
        d = dxt(I)
        if np.abs(d).max() < 1e-7: continue
        O2 = O.copy(); O2[:, 0] += d.astype(np.float32)
        sm["output"] = g._ekle_arr(O2.astype(np.float32), "VEC3", None); J["accessors"][sm["output"]].pop("min", None); J["accessors"][sm["output"]].pop("max", None)
        J["bufferViews"][J["accessors"][sm["output"]]["bufferView"]].pop("target", None)
        kac += 1
    log("anim %-20s kutu son x %.3f -> %.3f (giris %.2f s) · kaydirilan kanal %d" % (an["name"], x0 + dx_eski, x0 + dx_yeni, t_bas, kac))

g.kaydet(sys.argv[2])
open(os.path.join(HERE, "a1_log.txt"), "w", encoding="utf-8").write("\n".join(LOG))
print("yazildi", sys.argv[2])
