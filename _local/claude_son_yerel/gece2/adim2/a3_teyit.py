# -*- coding: utf-8 -*-
"""GECE2 ADIM 2 · EK (teyit.md): 1) ana salter ABB OT40F4N2 48 x 68 x 56 (G x Y x D; govde onu plaka + 45, kaplin + 11), OHYS2AJ kol on 66,
kapaktan one 34 + arkada O40 x 14; kapak deligi 22,5 + 3,2 mm kama centigi; mil OXS6X160 (160 mm; L 193,5). Bina kablosu salterin
UST klemensine ustten girer -> plaka gecidi y 2146 -> 2154,5 (govde ust yuzu 2141 + 3,5).
2) QR musteri paneli gercek urun olculeri: ekran RPi Touch Display 2 190 x 120 x 15 · okuyucu Newland FM430 42 x 25 x 50 (G x Y x D) ·
tus takimi Storm 1000 82,5 x 82,5 (derinlik 30 korundu); panel kablolari yeni arka yuzlere.
3) tezgah ayri bina hatti (zincire bagli degil): 2 zemin gomme bina buati (kapakli, rakorlu) tezgahin arka altinda; EIL 3 -> priz IP44,
MEIKO -> elektrik baglantisi; eski arka 'hat_elektrik' (nis duvarina) kalkar. Zemin doseme delikleri yeniden.
python a3_teyit.py giris.glb cikis.glb"""
import sys, os, json, numpy as np, re
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
for q in (os.path.join(S, "elk5"), os.path.join(S, "elk2"), os.path.join(S, "gece"), S): sys.path.insert(0, q)
from m8kit import Glb, kutu_ucgen, silindir_ucgen, tup, delik_ucgenler
from elib import Yeni, KAT as KATD

g = Glb(sys.argv[1]); LOG = []
def log(*a): s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)
MEKL = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
Y = Yeni(); E = KATD["ELEKTRIK"]


def sil_kutu(ad, lo, hi, tam=True):
    """dugum ucgenleri: tam=True -> tamamen kutu icinde olanlar; donus: (silinen, etiket)"""
    n = 0; et = None
    for p in g.dprims(ad):
        if p.get("gizli"): continue
        P = p["X"][p["T"]]; vis = g.gorunur(p)
        m = vis & (np.all(P.min(1) >= np.array(lo) - 0.01, 1) & np.all(P.max(1) <= np.array(hi) + 0.01, 1) if tam else
                   np.all(P.max(1) >= np.array(lo), 1) & np.all(P.min(1) <= np.array(hi), 1))
        if m.any():
            if et is None: et = (p, g._etiketler(p, int(np.where(m)[0][0])))
            n += g.sil(p, m)
    return n, et


def ekle(ad, P, et):
    p, e = et; return g._ekle_dunya(p, np.asarray(P, float), *e)


# ================================================================ 1 · ana salter
xc, yc = 3612.0, 2107.0; ZP = -280.5; ZK = -87.0          # montaj plakasi on yuzu · kapak dis yuzu (ic -89)
n, et = sil_kutu("ELK_ANA_PANO_UF__salter", (3587, 2078, -274), (3637, 2136, -204)); assert n == 12, n
govde = np.concatenate([kutu_ucgen((xc - 24, yc - 34, -273.0), (xc + 24, yc + 34, ZP + 45)),                 # ray onunde govde
                        kutu_ucgen((xc - 24, yc - 34, ZP), (xc + 24, 2091.3, -273.0)),                      # ray alti ayak
                        kutu_ucgen((xc - 24, 2126.7, ZP), (xc + 24, yc + 34, -273.0)),                      # ray ustu ayak
                        kutu_ucgen((xc - 7, yc - 7, ZP + 45), (xc + 7, yc + 7, ZP + 56))])                   # kaplin
log("ana salter OT40F4N2 48 x 68 x 56: govde z %.1f..%.1f, kaplin ..%.1f" % (ZP, ZP + 45, ZP + 56), ekle(None, govde, et) if False else g._ekle_dunya(et[0], govde, *et[1]))
n, et = sil_kutu("ELK_ANA_PANO_UF__salter_mil", (3608, 2103, -206), (3616, 2111, -86)); assert n == 12, n
g._ekle_dunya(et[0], kutu_ucgen((xc - 3, yc - 3, ZP + 56), (xc + 3, yc + 3, ZK - 16)), *et[1])
log("mil OXS6X160: z %.1f..%.1f (160 mm; plaka-kapak L = %.1f)" % (ZP + 45, ZP + 205, ZK - ZP))
for ad in ("ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__salter_kirmizi__KAPAK_ANA_PANO"):
    n, e_ = sil_kutu(ad, (3570, 2060, -90), (3655, 2150, -30))
    if ad.endswith("sari__KAPAK_ANA_PANO"): ets = e_
    else: etk = e_
    log("sil eski kol", ad, n)
g._ekle_dunya(ets[0], kutu_ucgen((xc - 33, yc - 33, ZK), (xc + 33, yc + 33, ZK + 7)), *ets[1])
kol = np.concatenate([silindir_ucgen((xc, yc, ZK + 7), (xc, yc, ZK + 21), 22.0, 32), kutu_ucgen((xc - 9, yc - 30, ZK + 21), (xc + 9, yc + 30, ZK + 34))])
g._ekle_dunya(etk[0], kol, *etk[1])
Y.ekle("ELK_ANA_PANO_UF__salter_somun__KAPAK_ANA_PANO", ("ME5_tapa_gri", (0.25, 0.25, 0.27, 1.0), 0.0, 0.7),
       silindir_ucgen((xc, yc, ZK - 2 - 14), (xc, yc, ZK - 2), 20.0, 32), E, MEKL.index("Elektrik/Ana pano"))
log("OHYS2AJ: sari plaka 66 x 66 x 7 + kirmizi secici (on 34) + kapak arkasi O40 x 14 somun")
# kapak deligine 3,2 mm kama centigi (delik 22,5 kare kesimi ustune, 2 mm)
for ad in ("ELK_ANA_PANO_UF__pano__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__conta__KAPAK_ANA_PANO"):
    for p in g.dprims(ad):
        if p.get("gizli"): continue
        P = p["X"][p["T"]]; vis = g.gorunur(p)
        mm = vis & np.all(P.max(1) >= [xc - 3, yc + 10, -91], 1) & np.all(P.min(1) <= [xc + 3, yc + 14, -86], 1)
        nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1)[:, None], 1e-12); mm &= np.abs(nn[:, 2]) > 0.999
        if not mm.any(): continue
        duz = sorted(set(np.round(P[mm][:, 0, 2], 3).tolist())); gr = {}
        for t in np.where(mm)[0]: gr.setdefault(g._etiketler(p, t), []).append(t)
        for e_, tt in gr.items():
            Q = P[np.array(tt)]
            for dz in duz: Q = delik_ucgenler(Q, 2, [dz], xc - 1.6, xc + 1.6, yc + 11.25 - 0.5, yc + 13.25)
            m2 = np.zeros(len(P), bool); m2[np.array(tt)] = True; g.sil(p, m2); g._ekle_dunya(p, Q, *e_)
        log("kapak kama centigi 3,2 x 2", ad, int(mm.sum()))
# montaj plakasi kablo gecidi y 2146 -> 2154,5
YG = 2154.5
n, et = sil_kutu("ELK_ANA_PANO_UF__din", (3598.9, 2132.9, -282.6), (3625.1, 2170.1, -280.4)); log("plaka gecit bolgesi sil", n)
g._ekle_dunya(et[0], np.concatenate([kutu_ucgen((3599, 2133, -282.5), (3625, YG - 13, -280.5)), kutu_ucgen((3599, YG + 13, -282.5), (3625, 2170, -280.5))]), *et[1])
p = [q for q in g.dprims("ELK_ANA_PANO_UF__lastik_gecit") if not q.get("gizli")][0]
vs = np.unique(p["T"][g.gorunur(p)].reshape(-1)); p["X"][vs, 1] += YG - 2146.0; p["degX"] = True
log("lastik gecit + plaka deligi y 2146 -> %.1f" % YG)
# bina kablosu (pano ici): eski 5 noktali yol -> ustten ust klemense
done = False
for p in g.dprims("ELK_ZINCIR__kablo_guc"):
    if p.get("gizli"): continue
    tl, kut = g.komp(p)
    for i, (lo, hi, nn) in kut.items():
        if lo[0] > 3590 and lo[0] < 3605 and hi[0] > 3945 and hi[0] < 3955 and lo[2] > -330 and hi[2] < -230:
            m = (tl == i) & g.gorunur(p); e_ = g._etiketler(p, int(np.where(m)[0][0])); g.sil(p, m)
            Q = [(3940, 2146, -318.5), (3940, 2146, -305), (3940, YG, -305), (xc, YG, -305), (xc, YG, -258), (xc, yc + 34.2 + 10, -258)]
            g._ekle_dunya(p, tup(Q, 10.0, 16), *e_); done = True
            log("bina kablosu pano ici yeniden:", Q)
assert done

# ================================================================ 2 · QR musteri paneli (QR x -200 sonrasi)
PAN = {"ekran_cam": ((4627.5, 1658.0, 1173.0), (4817.5, 1778.0, 1188.0)),
       "plastik": ((4859.0, 1687.5, 1138.0), (4901.0, 1712.5, 1188.0)),
       "paslanmaz": ((4951.75, 1676.75, 1158.6), (5034.25, 1759.25, 1188.0))}
for k, (lo, hi) in PAN.items():
    n, et = sil_kutu("QR_MUSTERI_PANELI__" + k, (4620, 1655, 1135), (5045, 1780, 1190)); assert n == 12, (k, n)
    g._ekle_dunya(et[0], kutu_ucgen(lo, hi), *et[1]); log("QR panel", k, lo, hi)
# kablolar: ekran 1163 -> 1173 (uzar), okuyucu 1143 -> 1138 (kisalir)
for ad in ("ELK_QR_KABLO__kablo_sinyal", "ELK_QR_KABLO__kablo"):
    for p in g.dprims(ad):
        if p.get("gizli"): continue
        tl, kut = g.komp(p)
        for i, (lo, hi, nn) in kut.items():
            c = (lo + hi) / 2
            if not (abs(lo[2] - 1109.2 + (hi[0] - lo[0]) / 2) < 4 or abs(lo[2] - 1109.2) < 4) or hi[1] > 1700 or lo[1] < 1670: continue
            for x0, z1, z2 in ((4720, 1163, 1173), (4735, 1163, 1173), (4880, 1143, 1138), (4895, 1143, 1138)):
                if abs(c[0] - x0) < 1 and abs(hi[2] - z1) < 4:
                    r = (hi[0] - lo[0]) / 2; m = (tl == i) & g.gorunur(p); e_ = g._etiketler(p, int(np.where(m)[0][0])); g.sil(p, m)
                    g._ekle_dunya(p, tup([(x0, c[1], 1109.2), (x0, c[1], z2)], r, 16), *e_)
                    log("QR panel kablosu x %.0f r %.1f: ucu z %.0f -> %.0f" % (x0, r, z1, z2))

# ================================================================ 3 · tezgah ayri bina hatti
MT = MEKL.index("Tezgâh/Gövde"); MB = MEKL.index("Tezgâh/Bulaşık makinesi"); MEV = MEKL.index("Tezgâh/Evye")
n, _ = sil_kutu("TEZGAH_BULASIK__celik", (3210, 50, 1818), (3246, 70, 1838)); log("eski bulasik hat_elektrik (nis duvarina) sil", n)
BUAT = [("evye", (3200.0, 1100.0, 3270.0, 1170.0), (3232.0, 1135.0)), ("bulasik", (3200.0, 1760.0, 3270.0, 1830.0), (3232.0, 1795.0))]
for ad, (x0, z0, x1, z1), (cx, cz) in BUAT:
    kut = np.concatenate([kutu_ucgen((x0, -2, z0), (x1, 0, z1)),                          # kapak saci (zeminle ayni yuz)
                          kutu_ucgen((x0 + 3, -80, z0 + 3), (x1 - 3, -2, z1 - 3))])          # gomme kutu
    Y.ekle("TEZGAH_BINA_HATTI__paslanmaz", ("MS_TEZGAH_BINA", (0.72, 0.73, 0.74, 1.0), 0.8, 0.35), kut, E, MT)
    Y.ekle("TEZGAH_BINA_HATTI__rakor", ("ME5_tapa_gri", (0.25, 0.25, 0.27, 1.0), 0.0, 0.7), silindir_ucgen((cx, 0, cz), (cx, 14, cz), 9.0, 24), E, MT)
r = 4.5
Q1 = [(3232.0, 14.0, 1135.0), (3232.0, 760.0, 1135.0)]                                   # EIL 3 -> priz IP44 (alt yuzu)
Q2 = [(3232.0, 14.0, 1795.0), (3232.0, 60.0, 1795.0), (3232.0, 60.0, 1828.0), (3245.0, 60.0, 1828.0)]   # MEIKO elektrik baglantisi
Y.ekle("TEZGAH_BINA_HATTI__kablo", ("MS_TEZGAH_KABLO", (0.12, 0.12, 0.12, 1.0), 0.0, 0.8), tup(Q1, r, 16), E, MEV)
Y.ekle("TEZGAH_BINA_HATTI__kablo", ("MS_TEZGAH_KABLO", (0.12, 0.12, 0.12, 1.0), 0.0, 0.8), tup(Q2, r, 16), E, MB)
log("tezgah bina hatti: 2 gomme buat + rakor, kablo EIL3 %s · MEIKO %s" % (Q1, Q2))
# evye dolabi tabanina kablo gecis deligi (y 100-101,2)
for p in g.dprims("TEZGAH_GOVDE__paslanmaz"):
    if p.get("gizli"): continue
    P = p["X"][p["T"]]; vis = g.gorunur(p)
    mm = vis & np.all(P.max(1) >= [3222, 99.9, 1040], 1) & np.all(P.min(1) <= [3250, 101.3, 1180], 1) & (np.ptp(P[:, :, 1], axis=1) < 0.01)
    if not mm.any(): continue
    duz = sorted(set(np.round(P[mm][:, 0, 1], 3).tolist())); gr = {}
    for t in np.where(mm)[0]: gr.setdefault(g._etiketler(p, t), []).append(t)
    for e_, tt in gr.items():
        Qd = P[np.array(tt)]
        Qd = delik_ucgenler(Qd, 1, duz[:2] if len(duz) >= 2 else duz, 3232 - 6.5, 3232 + 6.5, 1135 - 6.5, 1135 + 6.5)
        m2 = np.zeros(len(P), bool); m2[np.array(tt)] = True; g.sil(p, m2); g._ekle_dunya(p, Qd, *e_)
    log("evye dolabi tabani kablo deligi 13 x 13 duzlemler", duz)

# zemin doseme: delikler = zemin kanali kapaklari + tezgah buatlari
kp = [p for p in g.dprims("ELK_ZEMIN__kapak") if not p.get("gizli")]
R = []
for p in kp:
    tl, kut = g.komp(p)
    for i, (lo, hi, nn) in kut.items(): R.append((lo[0], hi[0], lo[2], hi[2]))
R += [(b[1][0], b[1][2], b[1][1], b[1][3]) for b in BUAT]
R = sorted(set((round(a, 2), round(b, 2), round(c, 2), round(d, 2)) for a, b, c, d in R))
zp = [p for p in g.dprims("ZEMIN_DOSEME__zemin_karo") if not p.get("gizli")][0]
Pz = zp["X"][zp["T"][g.gorunur(zp)]]
X0, X1 = Pz[..., 0].min(), Pz[..., 0].max(); Z0, Z1 = Pz[..., 2].min(), Pz[..., 2].max(); Y0 = float(np.median(Pz[..., 1]))
xs = sorted(set([X0, X1] + [v for r_ in R for v in r_[:2] if X0 < v < X1])); zs = sorted(set([Z0, Z1] + [max(Z0, min(Z1, v)) for r_ in R for v in r_[2:]]))
yeni = []
for xa, xb in zip(xs[:-1], xs[1:]):
    for za, zb in zip(zs[:-1], zs[1:]):
        xm, zm = (xa + xb) / 2, (za + zb) / 2
        if any(r_[0] < xm < r_[1] and r_[2] < zm < r_[3] for r_ in R): continue
        a = np.array([xa, Y0, za]); b = np.array([xb, Y0, za]); c = np.array([xb, Y0, zb]); d = np.array([xa, Y0, zb])
        yeni += [(a, d, c), (a, c, b)]
et = g._etiketler(zp, int(np.where(g.gorunur(zp))[0][0]))
g.sil(zp, np.ones(len(zp["T"]), bool)); g._ekle_dunya(zp, np.array(yeni), *et)
log("zemin doseme yeniden (delik %d): ucgen %d" % (len(R), len(yeni)))
Y.yaz(g)
g.kaydet(sys.argv[2])
open(os.path.join(HERE, "a3_log.txt"), "w", encoding="utf-8").write("\n".join(LOG))
print("yazildi", sys.argv[2])
