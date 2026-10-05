# -*- coding: utf-8 -*-
"""E GÖVDESİ (yeni) EK DENETİMLERİ — çakışma govde_denetim_dogru.py ile ayrıca (E=E_GOVDE__ kümesi ↔ bütün üçgenler).
  (b) BOŞLUK 0,2–15 mm: E gövde bileşeni ↔ E gövde / komşu gövde (K, U_KE, B, QR, TEZGAH) bileşenleri, manifold min_gap · amaçlı derzler ayrı listelenir
  (c) HAVADA: her E gövde bileşeni en az bir başka bileşene ≤ 0,05 mm
  (d) KAPAK AÇILMA 10–100° (10° adım): E alt sol / alt sağ / üst sol / üst sağ + K kapağı (dikey eksen, z 79) ↔ bütün kapalı bileşenler
      (kendi kapak grubu hariç) · govde_denetim_dogru.cift (manifold hacim + 0,6 mm örnekleme + derinlik)
  (e) E MEKANİZMASI HAREKET YOLLARI (kutu_cad_v14 stroklarının uç değerleri, 0–20 s döngüsü taranarak) ↔ yeni E gövde parçaları
Kullanım: python e_govde_denetim.py model.glb cikti_klasoru"""
import os, sys, json, time
import numpy as np
import manifold3d as mf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import govde_denetim_dogru as GD
import struct
_raw = open(sys.argv[1], "rb").read(); GJ = json.loads(_raw[20:20 + struct.unpack("<I", _raw[12:16])[0]])

g1, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "ek_denetim.txt"), "w", encoding="utf-8")


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n"); LOG.flush(); sys.stdout.flush()


t0 = time.time()
D = GD.glb_oku(g1)
ZARF = np.array([3900.0, -10.0, -900.0]), np.array([5700.0, 2300.0, 1300.0])
TUM = []
for nd, P in D.items():
    if not len(P): continue
    lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
    if (hi < ZARF[0]).any() or (lo > ZARF[1]).any(): continue
    TUM += GD.bilesenler(nd, P)
EG = [b for b in TUM if b.dugum.startswith("E_GOVDE__")]
yaz("model %s · bölgede %d bileşen · E gövde %d (kapalı %d) · %.0f s" % (os.path.basename(g1), len(TUM), len(EG), sum(b.kapali for b in EG), time.time() - t0))
LO = np.array([b.lo for b in TUM]); HI = np.array([b.hi for b in TUM])
KOMSU_GOVDE = ("E_GOVDE__", "K_GOVDE__", "U_KE_GOVDE__", "B_", "QR_GOVDE__", "TEZGAH_GOVDE__", "E_MODULER__")


def ad_b(b):
    c = (b.lo + b.hi) / 2
    return "%s[%d] (%.0f,%.0f,%.0f)" % (b.dugum, b.no, c[0], c[1], c[2])


def gap(A, B, lim=15.0):
    ma, mb = A.mf(), B.mf()
    if ma and mb:
        return float(ma.min_gap(mb, lim))
    # açık ağ: köşe örneği ↔ diğer yüzey
    Q = A.P.reshape(-1, 3)
    if B.kapali:
        return float(GD.yuzey_uzaklik(B.yz(), Q).min())
    return lim


import vtk


def arasi_bos(A, B, g):
    """A ile B'nin en yakın noktaları arasındaki doğru parçası (orta 3 nokta) başka bir kapalı bileşenin içinden geçiyor mu → geçmiyorsa boşluk gerçek"""
    lo = np.maximum(A.lo, B.lo - g - 0.5); hi = np.minimum(A.hi, B.hi + g + 0.5)
    Q, _ = GD.ornekle(A.P, lo, hi, adim=3.0, sinir=200000)
    if not len(Q) or not B.kapali: return True, None
    f = vtk.vtkImplicitPolyDataDistance(); f.SetInput(B.yz())
    en, pa, pb = 1e9, None, None
    for q in Q[np.linspace(0, len(Q) - 1, min(len(Q), 3000)).astype(int)]:
        c = [0.0, 0.0, 0.0]; d = abs(f.EvaluateFunctionAndGetClosestPoint(q.tolist(), c))
        if d < en: en, pa, pb = d, q, np.array(c)
    for t in (0.25, 0.5, 0.75):
        m = pa + t * (pb - pa)
        for C in TUM:
            if C is A or C is B or not C.kapali: continue
            if (m < C.lo - 1e-6).any() or (m > C.hi + 1e-6).any(): continue
            if GD.icerde(C.yz(), m[None])[0]: return False, (pa, pb)
    return True, (pa, pb)


# (b) + (c)
bos, derz, hav = [], [], []
for A in EG:
    m = ((LO <= A.hi + 15.0) & (HI >= A.lo - 15.0)).all(1)
    en = 1e9; en_ad = None
    for j in np.where(m)[0]:
        B = TUM[j]
        if B is A: continue
        g = gap(A, B)
        if g < en: en, en_ad = g, B
        if 0.2 < g < 15.0 and B.dugum.startswith(KOMSU_GOVDE):
            if id(A) < id(B) or not B.dugum.startswith("E_GOVDE__"):
                bosmu, nk = arasi_bos(A, B, g)
                if not bosmu: continue
                (derz if (A.dugum.endswith("on_seffaf") and B.dugum.endswith("on_seffaf")) else bos).append((ad_b(A), ad_b(B), round(g, 2)))
    if en > 0.05: hav.append((ad_b(A), round(en, 2), ad_b(en_ad) if en_ad else "-"))
yaz("\n(b) BOŞLUK 0,2–15 mm (E gövde ↔ E gövde / komşu gövde): %d · kapak ↔ kapak (derz) %d · %.0f s" % (len(bos), len(derz), time.time() - t0))
for r in sorted(bos, key=lambda r: r[2]): yaz("     %-58s ↔ %-58s %.2f mm" % r)
for r in sorted(derz, key=lambda r: r[2]): yaz("     derz %-53s ↔ %-58s %.2f mm" % r)
yaz("(c) HAVADA (hiçbir bileşene ≤ 0,05 mm değmeyen E gövde bileşeni): %s" % ("YOK" if not hav else "%d BULGU" % len(hav)))
for r in hav: yaz("     %-58s en yakın %.2f mm → %s" % r)


# (d) kapak açılma
def roty(P, piv, a):
    a = np.radians(a); c, s = np.cos(a), np.sin(a); R = P - piv
    x = R[..., 0] * c + R[..., 2] * s; z = -R[..., 0] * s + R[..., 2] * c
    return np.stack([x, R[..., 1], z], -1) + piv


KAP = []
for ad_k, x0, x1, y0, y1, px in (("E alt sol", 4401.9, 4860.1, 125.9, 785.1, 4402.0), ("E alt sağ", 4862.9, 5230.1, 125.9, 785.1, 5230.0),
                                  ("E üst sol", 4401.9, 4860.1, 787.9, 2197.1, 4402.0), ("E üst sağ", 4862.9, 5230.1, 787.9, 2197.1, 5230.0)):
    g = [b for b in EG if b.dugum == "E_GOVDE__on_seffaf" and b.lo[0] >= x0 and b.hi[0] <= x1 + 0.0 and b.lo[1] >= y0 and b.hi[1] <= y1]
    g += [b for b in TUM if b.dugum in ("E_COP__sac", "E_COP__celik", "DUZ_E_OLUK__paslanmaz") and ad_k == "E alt sol" and
          not (b.dugum == "E_COP__sac" and b.hi[2] < 30.0 and b.lo[1] < 500)]                          # klape + oluk kanatla döner (kızak hariç)
    KAP.append((ad_k, g, np.array([px, 0.0, 79.0])))
KAP.append(("K", [b for b in TUM if b.dugum in ("K_GOVDE__on_seffaf",)] +
            [b for b in TUM if b.dugum == "K_GOVDE__siyah" and False], np.array([4003.0, 0.0, 79.0])))
sup = []
for ad_k, grp, piv in KAP:
    # açılma yönü: grubun ağırlık merkezi +z'ye gitmeli
    c = np.concatenate([b.P.reshape(-1, 3) for b in grp]).mean(0)
    sg = 1.0 if roty(c[None], piv, 30.0)[0, 2] > c[2] else -1.0
    ids = set(id(b) for b in grp); nb = 0
    for a in range(10, 101, 10):
        RB = []
        for b in grp:
            P2 = roty(b.P, piv, sg * a)
            RB += GD.bilesenler(b.dugum + "@%d" % a, P2.reshape(-1, 3, 3))
        lo = np.min([r.lo for r in RB], 0); hi = np.max([r.hi for r in RB], 0)
        m = ((LO <= hi + 0.06) & (HI >= lo - 0.06)).all(1)
        for j in np.where(m)[0]:
            B = TUM[j]
            if id(B) in ids: continue
            for r in RB:
                if (r.lo > B.hi + 0.06).any() or (r.hi < B.lo - 0.06).any(): continue
                q = GD.cift(r, B)
                if q and q[0] == "CAKISMA":
                    sup.append((ad_k, a, r.dugum, ad_b(B), q[1])); nb += 1
    yaz("     %-10s %2d bileşen · eksen x %.0f z 79 · 10–100° · %s" % (ad_k, len(grp), piv[0], "temiz" if not nb else "%d bulgu" % nb))
yaz("(d) KAPAK AÇILMA SÜPÜRMESİ: %s · %.0f s" % ("TEMİZ" if not sup else "%d BULGU" % len(sup), time.time() - t0))
for r in sup[:60]: yaz("     %s %3d° %s ↔ %s derinlik %.2f" % r)

# (e) mekanizma hareket yolları ↔ yeni E gövdesi
sys.path.insert(0, os.path.join(HERE, "b3", "arastirma", "_uretec"))
import kutu_cad_v14 as KC
ts = np.linspace(0.0, KC.DONGU, 401)
TR = {"ITICI": lambda t: (0, 0, KC.feed_z(t)), "VAC_Y": lambda t: tuple(KC.vacuum_trs(t)), "NEST": lambda t: (0, KC.nest_dy(t), 0),
      "PISTON": lambda t: (0, KC.kafa(t) - KC.H_UST, 0), "KOPRU": lambda t: (0, KC.kopru_dy(t), 0), "KATLAYICI": lambda t: (0, KC.katlayici_dy(t), 0),
      "CNR_LIFT": lambda t: tuple(KC.corner_translation(t)), "FRONT_Y": lambda t: (0, KC.front_dy(t), 0)}
ROT = ("E_KAPAK__KOL", "E_PARMAK__PARMAK", "E_KOSE__CNR_MF", "E_KOSE__CNR_MB", "E_KOSE__CNR_PF", "E_KOSE__CNR_PB")
GOV = [b for b in EG if b.kapali and b.mf()]
mek = []
for nd, P in D.items():
    if not nd.startswith("E_"): continue
    suf = nd.split("__")[-1]
    if suf in TR:
        dd = np.array([TR[suf](t) for t in ts], float)
        dd = np.unique(np.round(dd, 1), axis=0)
        for b in GD.bilesenler(nd, P):
            lo = b.lo + dd.min(0); hi = b.hi + dd.max(0)
            for G in GOV:
                if (lo > G.hi + 0.06).any() or (hi < G.lo - 0.06).any(): continue
                ma = b.mf(); en = 0.0
                for d in dd[np.linspace(0, len(dd) - 1, min(len(dd), 60)).astype(int)]:
                    if ma:
                        v = (ma.translate(tuple(d)) ^ G.mf()).volume()
                    else:
                        v = 0.0
                    en = max(en, v)
                if en > 0.5: mek.append((nd, b.no, ad_b(G), round(en, 1)))
    elif nd in ROT:
        nod = [n for n in GJ["nodes"] if n.get("name") == nd][0]
        T0 = np.array(nod.get("translation", [0, 0, 0])) * 1000.0; R0 = GD._quat(nod.get("rotation", [0, 0, 0, 1]))
        Q0 = (P.reshape(-1, 3) - T0) @ R0                                         # düğüm yereli (R0ᵀ (p − T0))
        Fl = P.shape[0]
        if nd == "E_KAPAK__KOL": fT = lambda t: (0, 0, 0); fR = lambda t: KC.quat("z", KC.kol_beta(t))
        elif nd == "E_PARMAK__PARMAK": fT = lambda t: (0, KC.front_dy(t), 0); fR = lambda t: KC.quat("z", KC.parmak_psi(t))
        else:
            g_ = nd.split("__")[-1]; fT = lambda t: KC.corner_translation(t); fR = lambda t, g_=g_: KC.corner_quat(g_, t)
        en = {}
        for t in ts[::2]:
            Pt = (Q0 @ GD._quat(fR(t)).T + T0 + np.array(fT(t), float)).reshape(-1, 3, 3)
            for bb in GD.bilesenler(nd + "@t", Pt):
                for G in GOV:
                    if (bb.lo > G.hi + 0.06).any() or (bb.hi < G.lo - 0.06).any(): continue
                    q = GD.cift(bb, G)
                    if q and q[0] == "CAKISMA": en[ad_b(G)] = max(en.get(ad_b(G), 0.0), q[1])
        for k, v in en.items(): mek.append((nd, "dönme", k, round(v, 2)))
# kutu (katlanan blank) robot çatalıyla ağızdan öne çıkar · pizza K'dan pencereden girer → zarf (z +200'e / x 4820'ye uzatılmış) gövdeyle kesişir mi
for onek, lo, hi in (("katlanmış kutu + çatal (BX 4500–4820 · tepsi 936 → ağız üstü 1062) robotla öne", np.array([KC.BX0 + 4400.0, KC.TEPSI, -819.0]),
                      np.array([KC.BX1 + 4400.0, 1062.0, 200.0])),):
    import cadquery as cq
    zm = mf.Manifold.cube(tuple((hi - lo).tolist())).translate(tuple(lo.tolist()))
    for G in GOV:
        if (lo > G.hi).any() or (hi < G.lo).any(): continue
        v = (zm ^ G.mf()).volume()
        if v > 0.5: mek.append((onek + " yol zarfı", -1, ad_b(G), round(v, 1), "zarf %s–%s" % (np.round(lo, 1).tolist(), np.round(hi, 1).tolist())))
yaz("(e) MEKANİZMA HAREKET YOLLARI (ITICI 0–411 z · VAC_Y · NEST · PISTON 1310→937,6 · KÖPRÜ 30 · KATLAYICI 37,6 · CNR_LIFT −338,8…+60 · FRONT_Y −372,4 · "
    "KOL / PARMAK / köşe kanatları dönme zarfı) ↔ yeni E gövdesi: %s · %.0f s" % ("TEMİZ" if not mek else "%d BULGU" % len(mek), time.time() - t0))
for r in mek: yaz("     ", r)
json.dump(dict(bosluk=bos, derz=derz, havada=hav, kapak=sup, mekanizma=[list(map(str, r)) for r in mek]), open(os.path.join(OUT, "ek_denetim.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
yaz("BİTTİ %.0f s" % (time.time() - t0))
LOG.close(); sys.stdout.flush(); os._exit(0)
