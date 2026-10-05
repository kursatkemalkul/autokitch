# -*- coding: utf-8 -*-
"""e2 · YENİ ELEKTRİK: duvar şalteri + gizli bina girişi (dirsek kutusu → U → ana pano arkası) · pano iniş kanalı · makinenin arkasında
tek düz ana kanal · istasyon fiş panelleri (Harting Han 10B güç kırmızı kod · M12 X veri mavi kod · Festo QSSF-8 hava) · zincir ara kabloları ·
E ucu iniş + zemin kanalı (E altından) → QR alt fiş paneli → robot rezerv kutusu · istasyon içi panel → istasyon kutusu kabloları.
python e2_zincir.py e1.glb e1c/m8_onbellek.npz e2.glb"""
import sys, json, numpy as np
from elib import *
import m8kit
from m8kit import delik_ucgenler
from qlib import prim, ucgen_kutu
import geo, kablolar as KB
from olcu import *
gi, npz, go = sys.argv[1:4]
G = m8kit.Glb(gi); Y = Yeni(); R = []
MK = lambda kod: mekno(G, kod)
EL = KAT["ELEKTRIK"]


def ekle(mal, P, mek, kat=EL):
    Y.ekle(geo.DUG[mal], geo.MAL[mal], P, kat, MK(mek))


# ---------------------------------------------------------------- 1 dış geometri
for mal, P, mek in geo.parcalar(): ekle(mal, P, mek)


# ---------------------------------------------------------------- 2 delikler (U arka sacı, ana pano arka sacı) + QR kapak çentiği
def delik(ad, eksen, duz, u0, u1, w0, w1, sinir_lo, sinir_hi, coklu=None):
    p = prim(G, ad); m = ucgen_kutu(G, p, sinir_lo, sinir_hi)
    P = p["X"][p["T"]][m]; t0 = int(np.where(m)[0][0]); et = G._etiketler(p, t0)
    for (a0, a1, b0, b1) in (coklu or [(u0, u1, w0, w1)]):
        P = delik_ucgenler(P, eksen, duz, a0, a1, b0, b1)
    G.sil(p, m); G._ekle_dunya(p, P, *et); R.append(("delik %s %s" % (ad, coklu or [u0, u1, w0, w1]), len(P)))


D = DIRSEK
delik("U_F_GOVDE__sac", 2, [-830.0, -828.5], D["x"][0] + 1.5, 3983.0, D["y"][0] + 1.5, D["y"][1] - 1.5, (2490, 1850, -830.2), (4001, 2201, -828.3))
# pano arka sacı: her kablo için kare geçiş (r + 1)
PANO_GECIS = [(3940.0, 2146.0, R_BINA), (3967.0, 2146.0, R_VERI), (3942.0, 2118.0, R_GUC), (3966.0, 2118.0, R_VERI), (3942.0, 2094.0, R_GUC), (3966.0, 2094.0, R_VERI)]
delik("ELK_ANA_PANO_UF__pano", 2, [-320.0, -318.5], 0, 0, 0, 0, (3500, 1850, -320.2), (3990, 2190, -318.3),
      coklu=[(x - r - 1, x + r + 1, y - r - 1, y + r + 1) for x, y, r in PANO_GECIS])
for x, y, r in PANO_GECIS:
    ekle("rakor", halka((x, y, -320.0), (x, y, -338.0), r + 0.3, r + 4.0), "Elektrik/Ana pano")
    ekle("rakor", halka((x, y, -338.0), (x, y, -344.0), r + 0.3, r + 2.0), "Elektrik/Ana pano")
# QR alt servis kapağında fiş paneli çentiği + sabit montaj sacı
cq = C["QR"]
p_ = prim(G, "ELK_QR_MONTAJ__on_seffaf"); m_ = ucgen_kutu(G, p_, (5087.9, 21.0, 669.9), (5428.1, Y_QR + 61.9, 671.6))
P_ = p_["X"][p_["T"]]; nz_ = np.abs(np.cross(P_[:, 1] - P_[:, 0], P_[:, 2] - P_[:, 0])[:, 2]) > 1e-9
R.append(("QR kapak çentik içi yarık duvarları silindi", G.sil(p_, m_ & ~nz_)))
delik("ELK_QR_MONTAJ__on_seffaf", 2, [670.0, 671.5], 5088.0, 5428.0, 21.0, Y_QR + 62, (4560, 15, 669.8), (5440, 460, 672.2))
ekle("paslanmaz", kutu((5089.0, 22.0, 670.0), (5427.0, Y_QR + 61, 671.4)), "QR/Elektrik")     # QR alt sabit fiş sacı (kapak bu köşede kısaldı)

# ---------------------------------------------------------------- 3 QR iç besleme kablolarının alt ucu (eski alt giriş) kesilir, kart veri hattı yeniden
def komp_bul(ad, lo, hi, tol=1.0):
    p = prim(G, ad); tl, kut = G.komp(p)
    s = [i for i, (a, b, n) in kut.items() if np.all(np.abs(a - lo) < tol) and np.all(np.abs(b - hi) < tol)]
    assert len(s) == 1, (ad, lo, len(s))
    return p, (tl == s[0]) & G.gorunur(p)


QR_UC = {}
for ad, lo, hi, anah in (("ELK_QR_KABLO__kablo", (4873.8, 22.0, 691.7), (5394.2, 2031.2, 1038.2), "guc"),
                         ("ELK_QR_KABLO__kablo_veri", (4875.6, 35.0, 695.0), (5390.4, 2029.4, 1023.4), "veri")):
    p, m = komp_bul(ad, np.array(lo), np.array(hi))
    P = p["X"][p["T"]]; cy = P.mean(1)[:, 1]
    alt = m & (cy < 110.0)
    G.sil(p, alt)
    kal = m & ~alt
    V = P[kal].reshape(-1, 3); y0 = V[:, 1].min()
    uc = V[V[:, 1] < y0 + 0.5]; QR_UC[anah] = (uc.mean(0), float(np.ptp(uc[:, 0]) / 2), float(np.ptp(uc[:, 2]) / 2))
    R.append(("QR %s alt ucu kesildi -> uc %s" % (anah, np.round(QR_UC[anah][0], 1).tolist()), int(alt.sum())))
p, m = komp_bul("ELK_QR_KABLO__kablo_veri", np.array((4990.6, 35.0, 695.0)), np.array((5412.4, 1904.4, 1060.0)))
R.append(("QR kart veri hattı (eski alt giriş) silindi", G.sil(p, m)))
p, m = komp_bul("ELK_QR_KABLO__kablo_veri", np.array((5349.6, 36.7, 640.0)), np.array((5358.2, 45.3, 695.0)))
R.append(("QR eski dış veri ucu (yetim) silindi", G.sil(p, m)))
p, m = komp_bul("ELK_QR_KABLO__celik", np.array((5312.0, 1794.0, 1009.6)), np.array((5328.0, 1806.0, 1060.0)))
R.append(("QR eski kart hattı kelepçesi (boşta) silindi", G.sil(p, m)))

# ---------------------------------------------------------------- 4 dış kablolar
KAB = KB.kablolar()
# bina (duvardan, dirsek kutusundan, gizli) + pano kol başları (kablolar() içinde)
KAB.append(dict(ad="bina 5G6", tur="bina", r=R_BINA, Q=[np.array((3940.0, 2146.0, -938.0)), np.array((3940.0, 2146.0, -344.0))], mek="Elektrik/Ana pano"))
KAB.append(dict(ad="bina Cat6A", tur="veri", r=R_VERI, Q=[np.array((3967.0, 2146.0, -938.0)), np.array((3967.0, 2146.0, -344.0))], mek="Elektrik/Ana pano"))
for k in KAB:
    if k["ad"].startswith("kol_"): k["Q"][0] = np.array((k["Q"][0][0], k["Q"][0][1], -344.0))
for o in KB.kesisme(KAB): R.append(("DIS KESISME %s" % (o,), 0))
MALK = dict(guc="kablo_guc", bina="kablo_guc", veri="kablo_veri", hava="hava")
for k in KAB:
    P = tup(k["Q"], k["r"], 16)
    cz = P.mean(1)[:, 2]
    if k["mek"] == "Elektrik/Ana hat":
        ekle(MALK[k["tur"]], P[cz < 79.0], "Elektrik/Ana hat"); ekle(MALK[k["tur"]], P[cz >= 79.0], "Çevre/Dükkân hattı")
    else: ekle(MALK[k["tur"]], P, k["mek"])

# ---------------------------------------------------------------- 5 istasyon içi: panel -> istasyon kutusu (yol arayıcı)
EN = Engel(npz)
for mal, P, mek in geo.parcalar(): EN.ekle(P)
ICK = []


def yol_ara(S, S1, E1, E, r, vias):
    best = None
    cand = []
    for Q in dik_yollar(S1, E1): cand.append([S] + Q + [E])
    for v in vias:
        for Qa in dik_yollar(S1, v):
            for Qb in dik_yollar(v, E1): cand.append([S] + Qa + Qb[1:] + [E])
    cand = [sade(Q) for Q in cand]
    cand.sort(key=lambda Q: (sum(np.linalg.norm(b - a) for a, b in zip(Q[:-1], Q[1:])) + 30 * len(Q)))
    for Q in cand:
        ok = True
        for a, b in zip(Q[1:-2], Q[2:-1]):          # uç parçalar (sac / kutu yüzü temas) hariç
            if not BOL.seg_ok(a, b, r): ok = False; break
        if ok:
            # önceden çizilen iç kablolarla
            for k in ICK:
                for a0, a1 in zip(Q[:-1], Q[1:]):
                    for b0, b1 in zip(k["Q"][:-1], k["Q"][1:]):
                        if KB.seg_dist(a0, a1, b0, b1) < r + k["r"] + 0.5: ok = False
            if ok: return Q
    return None


BOLGE = dict(TOPPING=((1975, 880, -832), (2500, 2150, -560)), F=((2740, 880, -832), (2820, 960, -760)), K=((4000, 880, -832), (4400, 1210, -680)),
             B=((4040, 290, -832), (4360, 480, -700)), E=((4660, 880, -832), (4960, 1440, -680)), QR=((4970, 10, 670), (5410, 260, 1080)))
BOLC = {}


def ic(ist, k, E, E_on, vias=(), r=None):
    global BOL
    if ist not in BOLC: BOLC[ist] = Bolge(EN, *BOLGE[ist]); print("bolge", ist, BOLC[ist].n, flush=True)
    BOL = BOLC[ist]
    x = C[ist] + DX[k]; yc = Y_B if ist == "B" else (Y_QR if ist == "QR" else Y_UST)
    r = r or (R_GUC if k.startswith("GUC") else R_VERI)
    if ist == "QR": S = np.array((x, yc, 672.0)); S1 = np.array((x, yc, 690.0))
    else: S = np.array((x, yc, -828.5)); S1 = np.array((x, yc, -812.0))
    Q = yol_ara(S, S1, np.asarray(E_on, float), np.asarray(E, float), r, [np.asarray(v, float) for v in vias])
    if Q is None:
        M = izgara_yol(BOL, S1, np.asarray(E_on, float), r)
        if M is not None:
            Q = sade([S] + M + [np.asarray(E, float)])
            for k2 in ICK:
                for a0, a1 in zip(Q[:-1], Q[1:]):
                    for b0, b1 in zip(k2["Q"][:-1], k2["Q"][1:]):
                        if KB.seg_dist(a0, a1, b0, b1) < r + k2["r"] + 0.5: R.append(("IC KESISME %s %s" % (ist, k2["ad"]), 0))
    if Q is None: R.append(("ICERDE YOL YOK %s %s" % (ist, k), 0)); return
    ICK.append(dict(ad="%s %s" % (ist, k), r=r, Q=Q, tur="guc" if k.startswith("GUC") else "veri"))
    ekle("kablo_guc" if k.startswith("GUC") else "kablo_veri", tup(Q, r, 16), geo.MEK_IST[ist])
    R.append(("ic %s %s %d nokta %d mm" % (ist, k, len(Q), sum(np.linalg.norm(b - a) for a, b in zip(Q[:-1], Q[1:]))), 0))


def via_grid(xs, ys, zs):
    return [(x, y, z) for x in xs for y in ys for z in zs]


# TOPPING: teknik bölmeden (panel arkası) sağ bölme duvarındaki geçişten (x 2420) sağ cebe → dik → kuru pano ÖN yüzü (z −708) rakorları
def elle(ist, k, Q, r, rakor=None):
    Q = [np.asarray(q, float) for q in Q]
    ICK.append(dict(ad="%s %s" % (ist, k), r=r, Q=Q, tur="guc" if k.startswith("GUC") else "veri"))
    ekle("kablo_guc" if k.startswith("GUC") else "kablo_veri", tup(Q, r, 16), geo.MEK_IST[ist])
    R.append(("ic (elle) %s %s %d mm" % (ist, k, sum(np.linalg.norm(b - a) for a, b in zip(Q[:-1], Q[1:]))), 0))
# TOPPING / K / E: panel istasyon elektrik kutusunun (kuru pano · K kutusu · E elektrik plakası) tam sırtında → bağlantılar arka sactan doğrudan kutuya (iç kablo yok)
# F: giriş gücü kutunun sol rakoruna (eski bina 230 V rakoru); diğerleri kutunun arkasına doğrudan
ic("F", "GUC_GIRIS", (2788.0, 920.0, -790.0), (2776.0, 920.0, -790.0), [])
# B: Siemens (B elektrik plakası) alt yüzü y 470
VB = via_grid([4115.0, 4160.0, 4240.0, 4285.0], [380.0, 440.0, 455.0], [-812.0, -800.0, -790.0, -780.0])
for k in ("GUC_GIRIS", "VERI_GIRIS", "VERI_CIKIS", "GUC_CIKIS"):
    x = C["B"] + DX[k]
    ic("B", k, (x, 470.0, -800.0), (x, 455.0, -800.0), VB)
# QR: alt fiş paneli -> QR dikey kanalının (x 4983–5007) yan sacındaki geçişten eski kanal kablolarının ucuna (uçlar y 125 / 150'ye kısaltıldı)
for anah, yk in (("guc", 125.0), ("veri", 150.0)):
    ad = "ELK_QR_KABLO__kablo" if anah == "guc" else "ELK_QR_KABLO__kablo_veri"
    p = prim(G, ad); u = QR_UC[anah][0]
    vs = np.unique(p["T"][G.gorunur(p)].reshape(-1)); X = p["X"][vs]
    rr = R_GUC if anah == "guc" else R_VERI
    sel = vs[(X[:, 1] < u[1] + 2 * rr + 1.5) & (np.abs(X[:, 0] - u[0]) < 14) & (np.abs(X[:, 2] - u[2]) < 14)]
    cx, cz = p["X"][sel, 0].mean(), p["X"][sel, 2].mean()
    p["X"][sel, 1] = yk; p["degX"] = True
    R.append(("QR %s kablo alt ucu y %.1f -> %.0f (%d kose, merkez x %.1f z %.1f)" % (anah, u[1], yk, len(sel), cx, cz), 0))
    QR_UC[anah] = (np.array((cx, yk, cz)),)
xp, xd = C["QR"] + DX["GUC_GIRIS"], C["QR"] + DX["VERI_GIRIS"]
up = QR_UC["guc"][0]; ud = QR_UC["veri"][0]
elle("QR", "GUC_GIRIS", [(xp, Y_QR, 672), (xp, Y_QR, 690), (xp, up[1], 690), (xp, up[1], up[2]), tuple(up)], R_GUC)
elle("QR", "VERI_GIRIS", [(xd, Y_QR, 672), (xd, Y_QR, 700), (xd, ud[1], 700), (xd, ud[1], ud[2]), tuple(ud)], R_VERI)
# QR kilit kartı veri hattı: QR kutusu (yönetilmeyen anahtar) sağ yüzü -> kart üst kenarı (eski alt girişli hat yerine)
elle("QR", "VERI_kart", [(4940.0, 1875.0, 840.0), (5250.0, 1875.0, 840.0), (5250.0, 1860.0, 840.0), (5250.0, 1860.0, 1079.0), (5250.0, 1850.0, 1079.0)], R_VERI)
ekle("rakor", halka((4940.0, 1875.0, 840.0), (4950.0, 1875.0, 840.0), R_VERI + 0.3, R_VERI + 4.0), "QR/Elektrik")
delik("ELK_QR_KABLO__kanal", 0, [5005.5, 5007.0], 113.0, 160.0, 1012.0, 1043.0, (5005.3, 20.0, 999.0), (5007.2, 450.0, 1083.0))

for r in R: print("  %-80s %s" % r)
Y.yaz(G)
G.kaydet(go)
json.dump([dict(ad=k["ad"], r=k["r"], Q=[q.tolist() for q in k["Q"]]) for k in KAB + ICK], open(go + ".kablo.json", "w"), ensure_ascii=False)
print("yazildi", go)
