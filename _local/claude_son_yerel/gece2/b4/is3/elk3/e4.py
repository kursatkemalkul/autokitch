# -*- coding: utf-8 -*-
"""e4 · ELEKTRİK İÇERİDEN (v8zj -> e4): dışarıdaki bütün zincir elektriği silinir (arka kanallar, iniş/zemin üstü kanal, dışa monte fiş
panelleri, ara kablolar, duvar konsolları, dirsek kutusu, robot kutusu, duvar şalteri), duvar geçişli eski F→TOPPING / F→K hava hortumları
ve TOPPING sürücüsünden F'ye duvardan geçen bant motor kablosu kalkar · yeni: birleşim panelleri (yan duvarlarda içeride), contalı
geçişler, iç kanallar, pano arkası gömme giriş cebi, zemin içi kanal (B, QR, robot rezerv), şalter makinenin sağ ucunda duvarda.
python e4.py giris.glb cikis.glb"""
import sys, json, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\b4\is3"
sys.path.insert(0, S + r"\elk2"); sys.path.insert(0, S + r"\gece"); sys.path.insert(0, S + r"\birlesim"); sys.path.insert(0, S)
from elib import *
import m8kit
from m8kit import delik_ucgenler
from qlib import prim, ucgen_kutu
import tasarim as T
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); R = []
MEKL = [m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]
MK = lambda kod: MEKL.index(kod)


def rapor(a, n=0): R.append((a, n)); print("  %-90s %s" % (a, n), flush=True)


# ================================================================== 1 SİL
def sil_kutu(ad, lo, hi, kosul=None, etiket=""):
    n = 0
    for p in G.dprims(ad):
        if p.get("gizli"): continue
        m = ucgen_kutu(G, p, lo, hi)
        if kosul is not None: m &= kosul(p)
        n += G.sil(p, m)
    rapor("sil %s %s %s" % (ad, etiket, np.round(lo).tolist()), n)


def merkez(p):
    return p["X"][p["T"]].mean(1)


# 1a · ELK_ZINCIR + ELK_DUVAR tümü (QR içindeki kilit kartı veri hattı + rakoru hariç)
for p in G.prims:
    if p.get("gizli"): continue
    if p["name"].startswith("ELK_DUVAR__"):
        rapor("sil " + p["name"], G.sil(p, G.gorunur(p)))
    elif p["name"].startswith("ELK_ZINCIR__"):
        c = merkez(p); kal = (c[:, 2] > 760.0) & (c[:, 1] > 1800.0) & (c[:, 0] > 4900.0)
        rapor("sil " + p["name"] + " (QR kart hattı kalır %d)" % int((kal & G.gorunur(p)).sum()), G.sil(p, G.gorunur(p) & ~kal))
# 1b · eski hava hortumları (duvar geçişli): F→TOPPING (706), F→K (711), K duvar rakoru (3283) + kısa hortum (3290), duvar contaları (418, 2691)
sil_kutu("HAVA_KOMPRESOR__hava_ana", (2465, 1155, -750), (3560, 1820, -730), etiket="F→TOPPING hortum")
sil_kutu("HAVA_KOMPRESOR__hava_ana", (3540, 1800, -780), (3995, 1820, -760), etiket="F→K hortum")
sil_kutu("K_ELEKTRIK__celik", (3993, 1801, -778), (4009, 1817, -762), etiket="K duvar hava rakoru")
sil_kutu("K_ELEKTRIK__hava", (4007, 1804, -775), (4045, 1814, -765), etiket="K duvar hava kısa hortum")
sil_kutu("TOPPING_MODUL__koyu", (2496, 1801, -748), (2501, 1817, -732), etiket="TOPPING duvar hava contası")
sil_kutu("F_UST_KABIN__conta", (2499, 1797, -752), (2503, 1821, -728), etiket="F duvar hava contası")
# 1c · F yükleme bandı motor kablosu: TOPPING sürücüsünden duvar geçişli bölüm (x < 2772) + duvar rakoru + kelepçe
for p in G.dprims("ELK_TOPPING__kablo"):
    if p.get("gizli"): continue
    Pq = p["X"][p["T"]]; lo_, hi_ = Pq.min(1), Pq.max(1)
    m = G.gorunur(p) & (lo_[:, 0] < 2772) & (hi_[:, 0] > 2445) & (lo_[:, 1] > 1100) & (hi_[:, 1] < 1140) & (lo_[:, 2] > -815) & (hi_[:, 2] < -780)
    rapor("sil ELK_TOPPING__kablo bant motor kablosu duvar geçişi (x 2449–2772)", G.sil(p, m))
sil_kutu("ELK_TOPPING__rakor", (2459, 1109, -812), (2529, 1134, -787), etiket="bant motor duvar rakoru")
sil_kutu("ELK_TOPPING__celik", (2608, 1113, -829), (2622, 1131, -794), etiket="bant motor kelepçesi")


# ================================================================== 2 DELİKLER
def delik_dugum(ad, eksen, lo, hi, rect, dz=None):
    """ad düğümünün kutu (lo,hi) içindeki eksen-düzlemli üçgenlerinde dikdörtgen delik (rect = u0,u1,w0,w1; u<w eksen sırası)"""
    n = 0
    for p in G.dprims(ad):
        if p.get("gizli"): continue
        P = p["X"][p["T"]]; vis = G.gorunur(p)
        m = vis & np.all(P.max(1) >= np.asarray(lo), 1) & np.all(P.min(1) <= np.asarray(hi), 1)
        nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); L = np.linalg.norm(nn, axis=1); nn /= np.maximum(L[:, None], 1e-12)
        m &= (np.abs(nn[:, eksen]) > 0.999) & (np.ptp(P[:, :, eksen], axis=1) < 0.01)
        if not m.any(): continue
        duz = sorted(set(np.round(P[m][:, 0, eksen], 3).tolist()))
        ii = np.where(m)[0]
        gr = {}
        for t in ii: gr.setdefault(G._etiketler(p, t), []).append(t)
        for et, tt in gr.items():
            tt = np.array(tt); Q = P[tt]
            for rc in (rect if isinstance(rect[0], (tuple, list)) else [rect]):
                if len(duz) <= 2: Q = delik_ucgenler(Q, eksen, duz, *rc)
                else:
                    for dd in duz: Q = delik_ucgenler(Q, eksen, [dd], *rc)
            mm = np.zeros(len(P), bool); mm[tt] = True
            G.sil(p, mm); G._ekle_dunya(p, Q, *et); n += 1
        rapor("delik %s eksen %d düzlem %s rect %s" % (ad, eksen, duz, np.round(rect, 1).tolist()), int(m.sum()))
    return n


Y0 = T.Y0
for J in T.JN:
    u0, u1, v0, v1 = T.AGIZ
    rect = (Y0 + v0, Y0 + v1, J["c"] + u0, J["c"] + u1)        # eksen 0: u = y, w = z
    lo = (J["xf"] - 3.0, rect[0] - 1, rect[2] - 1); hi = (J["xf"] + 3.0, rect[1] + 1, rect[3] + 1)
    for ad in ("TOPPING_MODUL__sac", "F_UST_KABIN__sac", "K_GOVDE__kabuk", "E_GOVDE__kabuk"):
        delik_dugum(ad, 0, lo, hi, rect)
# F: H1 kanalı ara bölme profilinden (x 3326–3356) geçer · V1 U_F tabanı + F tavanı · V2 F ara tablası
delik_dugum("F_UST_KABIN__paslanmaz", 0, (3320, 1617, -827), (3362, 1649, -785), (1618.0, 1648.0, -826.0, -786.0))
for ad in ("U_F_GOVDE__sac", "F_UST_KABIN__sac"):
    delik_dugum(ad, 1, (3929, 1850, -827), (3997, 1875, -785), (3930.0, 3996.0, -826.0, -786.0))
for ad in ("F_UST_KABIN__sac", "F_UST_KABIN__yalitim"):
    delik_dugum(ad, 1, (2889, 1320, -797), (2931, 1350, -755), (2890.0, 2930.0, -796.0, -756.0))
# pano arka sacı: 4 yeni kol geçişi
RC = [(T.GECIS[k][0] - T.GECIS[k][2] - 1, T.GECIS[k][0] + T.GECIS[k][2] + 1, T.GECIS[k][1] - T.GECIS[k][2] - 1, T.GECIS[k][1] + T.GECIS[k][2] + 1) for k in T.YENI_DELIK]
delik_dugum("ELK_ANA_PANO_UF__pano", 2, (3900, 2020, -321), (3990, 2090, -318), RC)
# B tabanı (B kovanı) + QR tabanı (2 kovan)
K = T.B_KOVAN
for ad in ("B_KASA__sac", "B_KASA__pu", "B_KASA__celik", "B_MODULER__paslanmaz"):
    delik_dugum(ad, 1, (K["x"][0] - 1, 60, K["z"][0] - 1), (K["x"][1] + 1, 130, K["z"][1] + 1), (K["x"][0], K["x"][1], K["z"][0], K["z"][1]))
RC = [(K["x"][0], K["x"][1], K["z"][0], K["z"][1]) for K in (T.QR_KOVAN, T.QRR_KOVAN)]
delik_dugum("QR_GOVDE__qr_govde", 1, (4700, -1, 770), (5030, 30, 1050), RC)
delik_dugum("ELK_QR_KABLO__kanal", 1, (4982, 15, 1000), (5008, 30, 1050), (4985.0, 5005.0, 1008.0, 1043.0))
K = T.QRR_KOVAN
delik_dugum("QR_ROBOT_KONTROL__robot_kutu", 1, (K["x"][0] - 1, 15, K["z"][0] - 1), (K["x"][1] + 1, 30, K["z"][1] + 1), (K["x"][0], K["x"][1], K["z"][0], K["z"][1]))


# ================================================================== 3 KAPAMALAR (yama sacları + eski delikler)
def yama(ad, lo, hi, ornek_lo, ornek_hi):
    p = [q for q in G.dprims(ad) if not q.get("gizli")][0]
    m = ucgen_kutu(G, p, ornek_lo, ornek_hi) if ornek_lo is not None else None
    P = p["X"][p["T"]]
    if m is None or not m.any():
        c = P.mean(1); vis = G.gorunur(p)
        d = np.linalg.norm(c - (np.asarray(lo) + np.asarray(hi)) / 2, axis=1); d[~vis] = 1e18; t0 = int(np.argmin(d))
    else: t0 = int(np.where(m)[0][0])
    et = G._etiketler(p, t0)
    G._ekle_dunya(p, kutu(lo, hi), *et); rapor("yama %s %s" % (ad, np.round(lo).tolist()), 12)


# eski duvar geçiş delikleri (hava 2500/1809/−740, motor 2500/1121/−800, hava 4000/1809/−770): iki tarafın iç yüzüne 40×40 yama
yama("TOPPING_MODUL__sac", (2497.0, 1789, -760), (2498.5, 1829, -720), None, None)
yama("F_UST_KABIN__sac", (2501.5, 1789, -760), (2503.0, 1829, -720), None, None)
yama("TOPPING_MODUL__sac", (2497.0, 1101, -820), (2498.5, 1141, -780), None, None)
yama("F_UST_KABIN__sac", (2501.5, 1101, -820), (2503.0, 1141, -780), None, None)
yama("F_UST_KABIN__sac", (3997.0, 1789, -790), (3998.5, 1829, -750), None, None)
yama("K_GOVDE__kabuk", (4001.5, 1789, -790), (4003.0, 1829, -750), None, None)
# U_F arka sacındaki eski dirsek ağzı -> gömme cebin ağzı olarak KALIR (cep duvarları ağzın içinde)
# QR alt servis kapağındaki eski fiş sacı çentiği -> kapak tamamlanır
yama("ELK_QR_MONTAJ__on_seffaf", (5088.0, 21.0, 670.0), (5428.0, 182.0, 671.5), None, None)
# QR dikey kanalının yan sacındaki eski geçiş deliği
yama("ELK_QR_KABLO__kanal", (5007.0, 112.0, 1011.0), (5008.0, 161.0, 1044.0), None, None)

# ================================================================== 4 YENİ PARÇALAR
MAL = dict(__import__("geo").MAL)
MAL.update({"conta": ("ME3_conta_epdm", (0.10, 0.10, 0.11, 1.0), 0.0, 0.8),
            "zemin_oluk": ("ME3_zemin_oluk", (0.62, 0.64, 0.66, 1.0), 0.8, 0.4),
            "zemin_kapak": ("ME3_zemin_kapak", (0.70, 0.72, 0.74, 1.0), 0.85, 0.35)})
DUG = {"salter_kutu": "ELK_DUVAR__salter", "salter_sari": "ELK_DUVAR__salter_sari", "salter_kirmizi": "ELK_DUVAR__salter_kirmizi",
       "zemin_oluk": "ELK_ZEMIN__oluk", "zemin_kapak": "ELK_ZEMIN__kapak"}
Y = Yeni(); KAT = dict(GOVDE=0, MEKANIZMA=1, MOTOR=2, SENSOR=3, HAVA=4, SOGUTMA=5, ELEKTRIK=6, KONTROL=7, GIDA=8, ROBOT=9, URUN=10, DUKKAN=11)
say = {}
for mal, P, mek, kat, ad in T.parcalar():
    dug = DUG.get(mal, "ELK_ZINCIR__" + mal)
    if mal.startswith("zemin") or ad.startswith("zk_") or ad.startswith("robot") or ad.startswith("zemin"):
        dug = DUG.get(mal, "ELK_ZEMIN__" + mal)
    Y.ekle(dug, MAL[mal], P, KAT[kat], MK(mek)); say[ad] = say.get(ad, 0) + len(P)
for k, v in sorted(say.items()): rapor("yeni " + k, v)
# zemin döşemesinde kapak yerleri açılır (kapak sacı zemin yüzüdür)
delik_dugum("ZEMIN_DOSEME__zemin_karo", 1, (3000, -1, -900), (5500, 1, 1200), [(xr[0], xr[1], zr[0], zr[1]) for xr, zr in T.KAPAK])
Y.yaz(G)
G.kaydet(go)
print("yazildi", go)
