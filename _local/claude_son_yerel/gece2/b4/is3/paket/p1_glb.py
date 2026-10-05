# -*- coding: utf-8 -*-
"""PAKET 1 · hat3_v8zc -> p1.glb (geometri):
 1 robot QR tarafi: Robot/Elektrik etiketli QR kablolari + robot kutusu Harting'i silinir, ana hat ROBOT_guc + ROBOT_veri (pano -> QR) silinir,
   pano ROBOT fisi + M32 rakoru silinir -> ROBOT soketine Harting koruma kapagi; giris plakasi a KT20 (robot kablosu) + plaka b iki agiz kor tapa;
   QR alt dikey kanal 29x15 agzina kor kapak. (ROBOT_* dugumleri p2'de silinir.)
 4 E cop olugu kapaga: yan duvar braketleri silinir, oluk + dudak kpk (kapakla gizlenir), kapagin ic yuzune 2 vidali sac dil.
 5 kucuk aciklar: x sifir kablosu sag duvar kelepcelerinin icine (kelepce -x 6 mm genis) · ana pano bos A soketine koruma kapagi ·
   A arka-sag kose dikmesi y 2142,9 -> 2168,5 (ust kusak alti) · ana hat kanali TOPPING icinde x 2070'te biter + uc kapak, 1700 askisi silinir.
 2 dukkan hatti: Elektrik/Ana hat ucgenlerinden makine disinda kalanlar (x > 5230 ya da z > 79; kesisenler duzlemde bolunur) -> yeni unite
   'Cevre/Dukkan hatti' (gecici indis 58; p2 sirayi kurar).
python p1_glb.py ../hat3_v8zc.glb zc p1.glb"""
import os, sys, json, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(H)
sys.path.insert(0, os.path.join(S, "topfix"))
from tlib import *
from m8kit import kutu_ucgen, silindir_ucgen, _sh, _fan

gi, cache, go = sys.argv[1:4]
G = Glb(gi)
D = np.load(os.path.join(cache, "m8_onbellek.npz")); PJ = json.load(open(os.path.join(cache, "m8_parca.json"), encoding="utf-8"))
TP = D["P"]
MEKL = G.J["scenes"][0]["extras"]["mekanizmalar"]; MK = {m["kod"]: i for i, m in enumerate(MEKL)}
KT = {k["kod"]: i for i, k in enumerate(G.J["scenes"][0]["extras"]["kategoriler"])}

# ---------------------------------------------------------------- onbellek bilesen -> (prim, ucgen) haritasi (m8_yukle ile ayni gorunurluk kurali)
PR = [q for q in PJ["prim"]]
gp = [p for p in G.prims]
assert len(gp) == len(PR), (len(gp), len(PR))
HAR = {}; base = 0
for p, q in zip(gp, PR):
    assert p["name"] == q["ad"], (p["name"], q["ad"])
    if q["n"] == 0: continue
    T = p["T"]; P = p["X"][T]
    vis = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
    vis &= np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1) > 1e-9
    idx = np.where(vis)[0]
    assert len(idx) == q["n"], (p["name"], len(idx), q["n"])
    c = TP[base:base + len(idx)]; base += len(idx)
    for k in np.unique(c): HAR.setdefault(int(k), []).append((p, idx[c == k]))
assert base == len(TP)
log("harita tamam", len(HAR), "bilesen")

def maske(p, ii):
    m = np.zeros(len(p["T"]), bool); m[ii] = True; return m

def bsil(k, not_=""):
    n = 0
    for p, ii in HAR[k]: n += G.sil(p, maske(p, ii))
    q = PJ["parca"][k]; log("SIL #%d %-30s %4d ucgen %s %s %s" % (k, q["ad"], n, q["lo"], q["hi"], not_))

def etk(k):
    p, ii = HAR[k][0]; return etiket(G, p, maske(p, ii))

def bekle(k, ad, lo, hi, tol=0.6):
    q = PJ["parca"][k]
    ok = q["ad"] == ad and np.abs(np.array(q["lo"]) - lo).max() < tol and np.abs(np.array(q["hi"]) - hi).max() < tol
    assert ok, ("bilesen uymadi", k, q, ad, lo, hi)

def mek_ata(p, m, deger, key="mek"):
    ex = p["pr"].setdefault("extras", {}); L = ex.get(key) or []
    n = len(p["T"]); a = np.full(n, -1, int)
    for i in range(0, len(L) - 2, 3): a[L[i + 1] // 3:(L[i + 1] + L[i + 2]) // 3] = L[i]
    a[m] = deger
    out = []; i = 0
    while i < n:
        j = i
        while j + 1 < n and a[j + 1] == a[i]: j += 1
        out += [int(a[i]), i * 3, (j - i + 1) * 3]; i = j + 1
    ex[key] = out

def kpk_ata(p, m):
    k = G.kpk_maske(p) | m; idx = np.where(k)[0]; runs = []
    if len(idx):
        br = np.where(np.diff(idx) > 1)[0]; st = np.r_[idx[0], idx[br + 1]]; en = np.r_[idx[br], idx[-1]]
        for a, e in zip(st, en): runs += [int(a) * 3, int(e - a + 1) * 3]
    p["pr"].setdefault("extras", {})["kpk"] = runs

def ekle(ad, Pw, kat, mek, kpk=False):
    return ekle_ucgen(G, ad, Pw, kat, mek, kpk)

ELK = KT["ELEKTRIK"]; GOV = KT["GOVDE"]
MEKL.append({"kod": "Çevre/Dükkân hattı", "istasyon": "Çevre", "ad": "Dükkân hattı"}); YENI = len(MEKL) - 1

# ================================================================ 1 · ROBOT (QR / pano tarafi)
bekle(2642, "ELK_ANA_HAT__kablo", [2423.0, 2.0, -785.6], [5408.25, 2152.5, 640.0])
bekle(2654, "ELK_ANA_HAT__kablo_veri", [2423.0, 2.0, -772.3], [5374.35, 2148.7, 640.0])
bsil(2642, "ana hat ROBOT_guc 3G2,5 (pano ROBOT soketi -> QR giris b)")
bsil(2654, "ana hat ROBOT_veri Cat6A")
bekle(2739, "ELK_ISTASYON__rakor", [3450.1, 1884.0, -261.5], [3495.1, 1956.0, -218.5]); bsil(2739, "harting_ANA_PANO_ROBOT_fis")
bekle(2732, "ELK_ISTASYON__rakor", [3432.1, 1900.15, -260.0], [3450.1, 1939.85, -220.58]); bsil(2732, "harting_ANA_PANO_ROBOT_rakoru_M32")
for k, ad in ((2322, "qrk_ana_hat_guc_ROBOT_3G2_5"), (2386, "qrk_guc_ROBOT_3G2_5_giris_b_ucu"), (2387, "qrk_ana_hat_veri_ROBOT_Cat6A"),
              (2392, "qrk_veri_ROBOT_Cat6A_giris_b_ucu"), (2398, "robot kutusu Harting govde + fis"), (2399, "harting_ROBOT_rakoru_M32 (kutu)")):
    assert MEKL[PJ["parca"][k]["mek"]]["kod"] == "Robot/Elektrik", k
    bsil(k, ad)
# giris plakasi a: KT20 robot kablosu modulu -> ana hat cercevesinin parcasi (etiket), robot kablosu agzina kor tapa
bekle(2401, "ELK_QR_KABLO__rakor", [5067.25, 29.0, 653.0], [5108.75, 71.0, 670.0])
for p, ii in HAR[2401]: mek_ata(p, ii, MK["Elektrik/Ana hat"])
log("ETIKET #2401 giris_a_KT_20 -> Elektrik/Ana hat")
# kalan Robot/Elektrik ucgeni (ROBOT_* dugumleri disinda) olmamali
kal = 0
for p in G.prims:
    if p["name"].startswith("ROBOT_") or not p["pr"].get("extras", {}).get("mek"): continue
    vis = G.gorunur(p)
    for t in np.where(vis)[0][:0]: pass
    L = p["pr"]["extras"]["mek"]; a = np.full(len(p["T"]), -1)
    for i in range(0, len(L) - 2, 3): a[L[i + 1] // 3:(L[i + 1] + L[i + 2]) // 3] = L[i]
    kal += int(((a == MK["Robot/Elektrik"]) & vis).sum())
log("ROBOT_* disinda kalan Robot/Elektrik ucgeni:", kal); assert kal == 0
# kor tapalar (kablo yerini doldurur, cerceve kalinligi + ic yuzde 2 mm baslik)
TAPA = [("plaka a KT20 robot kablosu", (5088.1, 50.0), 9.4, 653.0, 670.0),
        ("plaka b ROBOT_guc", (5401.9, 59.0), 5.8, 656.0, 670.0),
        ("plaka b ROBOT_veri", (5369.9, 59.0), 4.0, 656.0, 670.0)]
for ad, (x, y), r, z0, z1 in TAPA:
    Pw = np.concatenate([silindir_ucgen((x, y, z0), (x, y, z1), r, 20), silindir_ucgen((x, y, z1), (x, y, z1 + 2.0), r + 2.0, 20)])
    ekle("ELK_QR_KABLO__rakor", Pw, ELK, YENI); log("KOR TAPA", ad, "r", r)
# QR alt dikey kanal yan saci 29x15 robot kablo agzi -> dis yuzde 1,5 mm kor kapak (her yandan 3 mm bindirme)
kq = etk(2394)
ekle("ELK_QR_KABLO__kanal", kutu_ucgen([4981.5, 283.0, 1035.0], [4983.0, 318.0, 1056.0]), kq[0], kq[1]); log("KOR KAPAK QR alt dikey kanal agzi", kq)
# pano ROBOT soketi: Harting koruma kapagi (fisin yerinde, soket yuzune oturur)
ks = etk(4244)
ekle("ELK_ANA_PANO_UF__harting", kutu_ucgen([3471.1, 1884.0, -261.5], [3489.1, 1956.0, -218.5]), ELK, ks[1]); log("HARTING KAPAK ROBOT soketi")

# ================================================================ 5b · ana pano bos A soketi -> koruma kapagi
ka = etk(4250)
ekle("ELK_ANA_PANO_UF__harting", kutu_ucgen([3646.5, 1985.0, -366.9], [3689.5, 2057.0, -348.9]), ELK, ka[1]); log("HARTING KAPAK A soketi (A'nin elektrigi yok)")

# ================================================================ 4 · E cop olugu kapaga
bekle(3720, "E_COP__sac", [4449.0, 545.5, 0.0], [4609.0, 603.0, 57.5])
bekle(2759, "DUZ_E_OLUK__paslanmaz", [4449.0, 601.5, 57.5], [4609.0, 603.0, 59.0])
bekle(3718, "E_COP__sac", [4421.5, 559.25, 11.0], [4449.0, 589.25, 13.0]); bekle(3719, "E_COP__sac", [4421.5, 559.25, 44.5], [4449.0, 589.25, 46.5])
bsil(3718, "oluk yan duvar braketi alt"); bsil(3719, "oluk yan duvar braketi ust")
for k in (3720, 2759):
    for p, ii in HAR[k]: kpk_ata(p, maske(p, ii))
    log("KPK #%d %s (kapakla birlikte)" % (k, PJ["parca"][k]["ad"]))
ko = etk(3720)
for x0 in (4452.0, 4586.0):
    ekle("E_COP__sac", kutu_ucgen([x0, 578.0, 57.5], [x0 + 20.0, 601.5, 59.0]), ko[0], ko[1], True)                 # olugun on ayagindan bukulu dil, kapak ic yuzune
    ekle("E_COP__sac", silindir_ucgen((x0 + 10.0, 590.0, 55.5), (x0 + 10.0, 590.0, 57.5), 3.5, 16), ko[0], ko[1], True)  # M4 vida basi (somun kapakta)
    log("OLUK DIL + VIDA x", x0)

# ================================================================ 5a · x sifir kablosu kelepce icine (kelepce tepe sacı -6 mm)
for k in (2513, 2514, 2515, 2516):
    assert PJ["parca"][k]["ad"] == "ELK_TOPPING__celik" and abs(PJ["parca"][k]["lo"][0] - 2491.0) < 0.05
    for p, ii in HAR[k]:
        def f(V):
            V = V.copy(); V[V[:, 0] < 2493.0, 0] -= 6.0; return V
        tasi(G, p, maske(p, ii), f)
    log("KELEPCE #%d x 2491 -> 2485 (ic 2486-2497,5: x sifir + sag duvar demeti)" % k)

# ================================================================ 5c · A arka-sag kose dikmesi tam boy
bekle(2193, "A_GOVDE__paslanmaz", [1404.5, 893.5, -828.5], [1434.5, 2142.9, -798.5])
for p, ii in HAR[2193]:
    def f(V):
        V = V.copy(); V[np.abs(V[:, 1] - 2142.9) < 0.05, 1] = 2168.5; return V
    tasi(G, p, maske(p, ii), f)
log("A DIKME y 2142,9 -> 2168,5 (ust kusak alt yuzu, diger dikmelerle ayni)")

# ================================================================ 5d · ana hat kanali TOPPING icinde x 2070'te biter
XK = 2070.0
bekle(2664, "ELK_ANA_HAT__paslanmaz", [1700.0, 2140.5, -828.5], [1730.0, 2165.0, -826.0]); bsil(2664, "kanal askisi x 1700 (kanal artik yok)")
kk = etk(2658); nsil = nek = 0
for p, ii in HAR[2658]:
    Pw = p["X"][p["T"][ii]]; mx = Pw[:, :, 0].max(1); mn = Pw[:, :, 0].min(1)
    tam = ii[mx <= XK + 1e-6]; kes_ = ii[(mn < XK - 1e-6) & (mx > XK + 1e-6)]
    yeni = []
    for t in kes_:
        poly = _sh([q for q in p["X"][p["T"][t]]], 0, XK, False)
        if len(poly) >= 3: yeni += _fan(poly)
    if yeni:
        Q = np.array(yeni); ar = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1); Q = Q[ar > 1e-6]
        for (kt, mk, kp), tt in [(etiket(G, p, maske(p, kes_)), None)]:
            nek += G._ekle_dunya(p, Q, kt, mk, kp)
    nsil += G.sil(p, maske(p, np.concatenate([tam, kes_])))
ekle("ELK_ANA_HAT__kanal", kutu_ucgen([XK - 1.5, 2105.0, -826.0], [XK, 2168.0, -690.0]), kk[0], kk[1])
log("ANA HAT KANALI x 1440 -> %.0f: %d ucgen silindi, %d kesik eklendi + 1,5 mm uc kapak (TOPPING kablolari x 2102,8+ agizdan iner)" % (XK, nsil, nek))

# ================================================================ 2 · dukkan hatti (makine disi ana hat)
XM, ZM = 5230.0, 79.0
nd_ = nk = nb = 0
for p in G.prims:
    ex = p["pr"].get("extras", {})
    if p.get("gizli") or not ex.get("mek") or len(p["T"]) == 0: continue
    L = ex["mek"]; a = np.full(len(p["T"]), -1)
    for i in range(0, len(L) - 2, 3): a[L[i + 1] // 3:(L[i + 1] + L[i + 2]) // 3] = L[i]
    m = (a == MK["Elektrik/Ana hat"]) & G.gorunur(p)
    if not m.any(): continue
    Pw = p["X"][p["T"]]
    disari = lambda Q: (Q[..., 0] > XM + 1e-6) | (Q[..., 2] > ZM + 1e-6)
    ic = lambda Q: (Q[..., 0] < XM - 1e-6) & (Q[..., 2] < ZM - 1e-6)
    tum_dis = m & np.all(~ic(Pw) , 1) & np.any(disari(Pw), 1)
    tum_ic = m & np.all(~disari(Pw), 1)
    kes_ = m & ~tum_dis & ~tum_ic
    if tum_dis.any(): mek_ata(p, tum_dis, YENI); nd_ += int(tum_dis.sum())
    if kes_.any():
        gr = {}
        for t in np.where(kes_)[0]: gr.setdefault(etiket(G, p, maske(p, [t])), []).append(t)
        for (kt, mk, kp), tt in gr.items():
            IC, DIS = [], []
            for t in tt:
                poly = [q for q in Pw[t]]
                sol = _sh(poly, 0, XM, True); sag = _sh(poly, 0, XM, False)
                if len(sag) >= 3: DIS += _fan(sag)
                if len(sol) >= 3:
                    on = _sh(sol, 2, ZM, True); ar = _sh(sol, 2, ZM, False)
                    if len(on) >= 3: IC += _fan(on)
                    if len(ar) >= 3: DIS += _fan(ar)
            for Q, mm in ((IC, mk), (DIS, YENI)):
                if not Q: continue
                Q = np.array(Q); ar_ = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1); Q = Q[ar_ > 1e-6]
                nb += G._ekle_dunya(p, Q, kt, mm, kp)
        nk += G.sil(p, kes_)
    log("  dukkan hatti %-30s tam dis %d · bolunen %d" % (p["name"], int(tum_dis.sum()), int(kes_.sum())))
log("DUKKAN HATTI: %d ucgen yeniden etiket, %d ucgen bolundu -> %d parca" % (nd_, nk, nb))
# ================================================================ 6 · TOPPING teknik bolme on perdesi (z -476,5) tabana kadar: alt 60 mm menfezli serit
from m8kit import delik_ucgenler
assert PJ["parca"][595]["ad"] == "TOPPING_MODUL__sac"
kp = etk(595)
Pw = kutu_ucgen([1437.5, 893.5, -476.5], [2418.5, 953.5, -475.0])
XS = [1437.5 + 8.5 + i * 44.0 for i in range(22)]                     # 22 yarik 36 x 40, adim 44 (acik alan 31 680 mm2)
for x0 in XS: Pw = delik_ucgenler(Pw, 2, [-476.5, -475.0], x0, x0 + 36.0, 903.5, 943.5)
ekle("TOPPING_MODUL__sac", Pw, kp[0], kp[1], kp[2])
log("TOPPING PERDE alt serit y 893,5-953,5 x 1437,5-2418,5 · %d menfez yarigi 36x40 (son yarik x %.1f)" % (len(XS), XS[-1] + 36))
# robot kutusu (rezerv) disiplini ROBOT -> KONTROL (robot yok; Robot dugmesi bos kalmasin)
for p, ii in HAR[4015]: mek_ata(p, ii, KT["KONTROL"], key="kat")
log("KAT robot kutusu (rezerv) ROBOT -> KONTROL")
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
