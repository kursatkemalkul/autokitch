# -*- coding: utf-8 -*-
"""ELEKTRİK v3 (İÇERİDEN) · tek ölçü + geometri kaynağı. Dünya mm: x hat boyu, y yukarı, z ön (+).
parcalar() -> [(mal, P(n,3,3), mek, kat, ad)]   ·   kutular() -> [(ad, lo, hi)] (ön çakışma denetimi için kaba kutular)
İSTASYON BİRLEŞİM PANELİ (her birleşimde AYNI): 304 paslanmaz 124 × 134 × 2, duvardan 20 mm burçlu (arkası iç kablo boşluğu),
Harting Han 10B gövde+kapak (güç, kırmızı kod) · M12 X (veri, mavi halka) · Festo QSSF-8 (hava) · alt-önde 66 × 56 contalı geçiş ağzı.
Bant: y 1468–1602 (tüm hat aynı yükseklik). Derinlik: J1 (TOPPING|F) z −777…−653 · J2 (F|K), J3 (K|E) z −677…−553."""
import sys, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5e\is3"
sys.path.insert(0, S + r"\elk2"); sys.path.insert(0, S + r"\gece"); sys.path.insert(0, S)
from elib import kutu, plaka, kanal, silindir, tup, halka

Y0 = 1468.0; ST = 20.0; PW = 62.0; PH = 134.0
R_GUC, R_VERI, R_HAVA, R_BINA = 7.5, 4.35, 4.0, 10.0
PDV = (150.0, 180.0)                  # panel kanalı (PD) y = Y0+150 … Y0+180 = 1618–1648
# birleşimler: ad, duvar düzlemi, sol iç yüz, sağ iç yüz, z merkez, sol istasyon, sağ istasyon, hava?
JN = [dict(ad="J1", xf=2500.0, xl=2498.5, xr=2501.5, c=-715.0, L="TOPPING", R="F", hava=True, giris="L"),
      dict(ad="J2", xf=4000.0, xl=3998.5, xr=4001.5, c=-615.0, L="F", R="K", hava=True, giris="R"),
      dict(ad="J3", xf=4400.0, xl=4398.5, xr=4401.5, c=-615.0, L="K", R="E", hava=True, giris="R")]
MEK = {"TOPPING": "TOPPING/Elektrik", "F": "F/Elektrik", "K": "K/Elektrik", "E": "E/Elektrik", "B": "B/Elektrik", "QR": "QR/Elektrik"}
MEKH = {"TOPPING": "TOPPING/Hava", "F": "F/Hava", "K": "K/Hava", "E": "E/Hava"}
HAT = "Elektrik/Ana hat"; PANO = "Elektrik/Ana pano"; DUK = "Çevre/Dükkân hattı"


class Cer:
    """panel çerçevesi: dünya = (xin + s*n, Y0 + v, c + u)"""
    def __init__(s, xin, sg, c): s.xin, s.sg, s.c = xin, sg, c
    def P(s, u, v, n): return np.array((s.xin + s.sg * n, Y0 + v, s.c + u), float)
    def K(s, u0, u1, v0, v1, n0, n1):
        a, b = s.xin + s.sg * n0, s.xin + s.sg * n1
        return kutu((min(a, b), Y0 + v0, s.c + u0), (max(a, b), Y0 + v1, s.c + u1))
    def Cn(s, u, v, n0, n1, r, k=20): return silindir(s.P(u, v, n0), s.P(u, v, n1), r, k)
    def Cv(s, u, v0, v1, n, r, k=20): return silindir(s.P(u, v0, n), s.P(u, v1, n), r, k)
    def T(s, Q, r): return [s.P(*q) for q in Q]


# ara kablo yolları (panel yerel, ön yüzden duvara)
LANE = dict(guc=[(-36.3, 24.0, ST + 49.9), (-36.3, 16.0, ST + 49.9), (6.0, 16.0, ST + 49.9), (6.0, 16.0, 0.0)],
            veri=[(44.0, 119.0, ST + 48.0), (44.0, 119.0, ST + 56.0), (44.0, 46.0, ST + 56.0), (44.0, 46.0, 0.0)],
            hava=[(26.0, 80.0, ST + 30.0), (26.0, 80.0, ST + 38.0), (26.0, 46.0, ST + 38.0), (26.0, 46.0, 0.0)])
# iç kablolar (panel arkası boşluk, n = 10) -> PD tabanı
ICL = dict(guc=[(-36.3, 80.0, ST), (-36.3, 80.0, 10.0), (-36.3, PDV[0] + 6, 10.0)],
           veri=[(44.0, 119.0, ST), (44.0, 119.0, 10.0), (44.0, 126.0, 10.0), (4.0, 126.0, 10.0), (4.0, PDV[0] + 6, 10.0)],
           hava=[(26.0, 80.0, ST), (26.0, 80.0, 10.0), (-10.0, 80.0, 10.0), (-10.0, PDV[0] + 6, 10.0)])
AGIZ = (-8.0, 58.0, 6.0, 62.0)        # u0,u1,v0,v1


def panel(C, ist, havali, etiket_sol, out):
    mek = MEK[ist]; E = "ELEKTRIK"
    out.append(("paslanmaz", plaka(0, 0, 0, 0, 0, 0, 0) if False else None, mek, E, "x"))
    out.pop()
    # plaka (ağız + arka geçiş delikleri yok: arka bağlantılar plakaya temas eder)
    pl = C.K(-PW, PW, 0, PH, ST, ST + 2)
    # ağız deliği: plakayı 4 parçaya böl
    u0, u1, v0, v1 = AGIZ
    parts = [C.K(-PW, u0, 0, PH, ST, ST + 2), C.K(u1, PW, 0, PH, ST, ST + 2), C.K(u0, u1, 0, v0, ST, ST + 2), C.K(u0, u1, v1, PH, ST, ST + 2)]
    out.append(("paslanmaz", np.concatenate(parts), mek, E, "panel"))
    for (uu, vv) in ((-54, 8), (54, 75), (-54, 126), (54, 98)):
        out.append(("paslanmaz", C.Cn(uu, vv, 0, ST, 5.0, 12), mek, E, "burc"))
    # Han 10B gövde + kapak + kırmızı kod + kapak rakoru (aşağı)
    out.append(("harting", C.K(-58, -14.6, 35, 128, ST + 2, ST + 30.9), mek, E, "han_govde"))
    out.append(("harting", C.K(-57.8, -14.8, 44, 119, ST + 30.9, ST + 68.9), mek, E, "han_kapak"))
    out.append(("kod_kirmizi", C.K(-54, -18.6, 60, 104, ST + 68.9, ST + 69.7), mek, E, "kod"))
    out.append(("rakor", C.Cv(-36.3, 44, 24, ST + 49.9, 15.0), mek, E, "han_rakor"))
    # M12 X
    out.append(("m12", C.K(31, 57, 106, 132, ST + 2, ST + 5), mek, E, "m12_flans"))
    out.append(("kod_mavi", C.Cn(44, 119, ST + 5, ST + 9, 10.8), mek, E, "m12_halka"))
    out.append(("m12", C.Cn(44, 119, ST + 9, ST + 48, 10.0), mek, E, "m12_fis"))
    if havali:
        mh = MEKH[ist]
        out.append(("rakor", C.Cn(26, 80, ST + 2, ST + 8, 11.0, 6), mh, "HAVA", "hava_somun"))
        out.append(("rakor", C.Cn(26, 80, ST + 8, ST + 24, 8.0), mh, "HAVA", "hava_rakor"))
        out.append(("kod_mavi", C.Cn(26, 80, ST + 24, ST + 30, 9.0), mh, "HAVA", "hava_halka"))
    # etiket levhası (GİRİŞ / ÇIKIŞ) — plaka üst sağ köşe
    out.append(("etiket", C.K(14, 58, 136 - 12, 136 - 4, ST + 2, ST + 2.6) if False else C.K(-58, -14, 2, 10, ST + 2, ST + 2.6), mek, E, "etiket"))
    # iç kablolar (arka boşluk) -> PD
    out.append(("kablo_guc", tup(C.T(ICL["guc"], 0), R_GUC, 16), mek, E, "ic_guc"))
    out.append(("kablo_veri", tup(C.T(ICL["veri"], 0), R_VERI, 12), mek, E, "ic_veri"))
    if havali: out.append(("hava", tup(C.T(ICL["hava"], 0), R_HAVA, 12), MEKH[ist], "HAVA", "ic_hava"))


def pd(C, ist, z_arka, out, uc_on=12.0):
    """panelin üstünde duvara yaslı kapaklı kanal (A kolu): n 0–30, v PDV, u (z_arka-c) … uc_on; tabanında iç kablo ağzı"""
    a0, a1 = z_arka, C.c + uc_on
    x0, x1 = sorted((C.xin, C.xin + C.sg * 30.0))
    # taban deliği (iç kablolar): z (C.c-48 … C.c+10), x boşluk bölgesi
    xa, xb = sorted((C.xin + C.sg * 1.5, C.xin + C.sg * 19.0))
    g = kanal(2, a0, a1, (x0, Y0 + PDV[0]), (x1, Y0 + PDV[1]), 1.2, delik={(1, -1): [(C.c - 48.0, C.c + 10.0, xa, xb)]})
    out.append(("kanal", g, MEK[ist], "ELEKTRIK", "pd_" + ist))
    return (x0, x1)


def birlesimler(out):
    for J in JN:
        CL = Cer(J["xl"], -1.0, J["c"]); CR = Cer(J["xr"], 1.0, J["c"])
        panel(CL, J["L"], J["hava"], None, out); panel(CR, J["R"], J["hava"], None, out)
        # contalı geçiş (iki duvar + iki plaka boyunca): x, y Y0+6..62, z c-8..c+58
        u0, u1, v0, v1 = AGIZ
        g = kanal(0, J["xl"] - ST - 2.0, J["xr"] + ST + 2.0, (Y0 + v0, J["c"] + u0), (Y0 + v1, J["c"] + u1), 2.0, uc=(False, False))
        out.append(("conta", g, HAT, "ELEKTRIK", "gecis_" + J["ad"]))
        # ara kablolar
        for k, mal, r in (("guc", "kablo_guc", R_GUC), ("veri", "kablo_veri", R_VERI), ("hava", "hava", R_HAVA)):
            if k == "hava" and not J["hava"]: continue
            Q = CL.T(LANE[k], 0) + CR.T(LANE[k][::-1], 0)
            out.append((mal, tup(Q, r, 16), HAT if k != "hava" else "F/Hava", "ELEKTRIK" if k != "hava" else "HAVA", "ara_%s_%s" % (J["ad"], k)))


# ------------------------------------------------------------------ istasyon iç kanalları (kapaklı 304 kanal, 1,2 mm)
def kbox(out, ad, ist, lo, hi, delik=None, acik=(), uc=(True, True), e=None):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float); e = int(np.argmax(hi - lo)) if e is None else e
    o = [i for i in range(3) if i != e]
    g = kanal(e, lo[e], hi[e], (lo[o[0]], lo[o[1]]), (hi[o[0]], hi[o[1]]), 1.2, delik=delik, acik=acik, uc=uc)
    out.append(("kanal", g, MEK[ist], "ELEKTRIK", ad))


def ic_kanallar(out):
    yA, yB = Y0 + PDV[0], Y0 + PDV[1]
    J1, J2, J3 = JN
    # TOPPING: J1 PD -> mevcut sağ dik kanal (x 2421–2449)
    pd(Cer(J1["xl"], -1, J1["c"]), "TOPPING", -818.0, out)
    kbox(out, "T_pdB", "TOPPING", (2449.5, yA, -818.0), (2468.5, yB, -788.0))
    # F: J1 PD + üst arka yatay kanal H1 + pano inişi V1 + J2 PD + F kutusu inişi V2
    pd(Cer(J1["xr"], 1, J1["c"]), "F", -826.0, out)
    kbox(out, "F_H1", "F", (2531.5, yA, -826.0), (3930.0, yB, -786.0), delik={(1, 1): [(3542.0, 3556.0, -813.0, -799.0)]}, e=0)
    kbox(out, "F_V1", "F", (3930.0, yB, -826.0), (3996.0, 2030.0, -786.0), uc=(False, False), e=1)
    pd(Cer(J2["xl"], -1, J2["c"]), "F", -826.0, out)
    kbox(out, "F_V2", "F", (2890.0, 952.0, -796.0), (2930.0, yA, -756.0), uc=(False, True), e=1)
    # K: J2 PD + B kolu (K kutusunun mevcut kanalına x 4130) · J3 PD + B kolu (x 4255)
    pd(Cer(J2["xr"], 1, J2["c"]), "K", -783.0, out)
    kbox(out, "K_pd2B", "K", (4031.5, yA, -783.0), (4130.0, yB, -753.0), delik={(1, 1): [(4034.0, 4046.0, -782.0, -772.0)]})
    pd(Cer(J3["xl"], -1, J3["c"]), "K", -783.0, out)
    # K kutusu -> J3: sol duvarda dik kanal, K tavanının altında yatay kanal (y 1826–1856), sağ duvarda dik kanal
    kbox(out, "K_V2", "K", (4001.5, yB, -748.0), (4031.5, 1856.0, -718.0), e=1)
    kbox(out, "K_ust", "K", (4031.5, 1826.0, -748.0), (4368.5, 1856.0, -718.0), e=0)
    kbox(out, "K_V3", "K", (4368.5, yB, -748.0), (4398.5, 1856.0, -718.0), e=1)
    # E: J3 PD + B kolu (E arka plakasının mevcut kanalı x 4470, y 1577–1617)
    pd(Cer(J3["xr"], 1, J3["c"]), "E", -822.0, out)
    kbox(out, "E_pd3B", "E", (4431.5, 1600.0, -822.0), (4470.0, 1630.0, -797.0))


# ------------------------------------------------------------------ U_F: pano arkası gömme giriş cebi + pano rakorları + kol kabloları
POCKET = dict(x=(3926.5, 3983.0), y=(2081.5, 2166.5), z=(-830.0, -790.0))
Z_DUVAR = -850.0
PANO_Z = -320.0
GECIS = dict(bina=(3940.0, 2146.0, R_BINA, "guc"), bina_v=(3967.0, 2146.0, R_VERI, "veri"),
             zemin=(3942.0, 2118.0, R_GUC, "guc"), zemin_v=(3966.0, 2118.0, R_VERI, "veri"),
             bos1=(3942.0, 2094.0, R_GUC, None), bos2=(3966.0, 2094.0, R_VERI, None),
             sol=(3942.0, 2070.0, R_GUC, "guc"), sol_v=(3966.0, 2070.0, R_VERI, "veri"),
             sag=(3942.0, 2046.0, R_GUC, "guc"), sag_v=(3966.0, 2046.0, R_VERI, "veri"))
YENI_DELIK = ("sol", "sol_v", "sag", "sag_v")


def pano_giris(out):
    P = POCKET; E = "ELEKTRIK"
    # cep: 4 yan duvar (z −830 … −790) + taban (z −791.5 … −790) 4 delikli
    g = kanal(2, P["z"][0], P["z"][1], (P["x"][0] + 0.0, P["y"][0] + 0.0), (P["x"][1], P["y"][1]), 1.5, uc=(False, False))
    out.append(("paslanmaz", g, PANO, E, "cep"))
    dl = []
    for k in ("bina", "bina_v", "zemin", "zemin_v"):
        x, y, r, _ = GECIS[k]; dl.append((y - r - 1.0, y + r + 1.0, x - r - 1.0, x + r + 1.0))
    out.append(("paslanmaz", plaka(2, P["z"][1] - 1.5, P["z"][1], P["y"][0] + 1.5, P["y"][1] - 1.5, P["x"][0] + 1.5, P["x"][1] - 1.5,
                                   [(d[0], d[1], d[2], d[3]) for d in dl]) if False else
                plaka(2, P["z"][1] - 1.5, P["z"][1], P["x"][0] + 1.5, P["x"][1] - 1.5, P["y"][0] + 1.5, P["y"][1] - 1.5,
                      [(d[2], d[3], d[0], d[1]) for d in dl]), PANO, E, "cep_taban"))
    for k in ("bina", "bina_v", "zemin", "zemin_v"):
        x, y, r, _ = GECIS[k]
        out.append(("rakor", halka((x, y, P["z"][1]), (x, y, P["z"][1] + 14.0), r + 0.3, r + 3.5), PANO, E, "cep_rakor"))
    # pano arka sacı rakorları (dışa, −z)
    for k, (x, y, r, tur) in GECIS.items():
        out.append(("rakor", halka((x, y, PANO_Z), (x, y, PANO_Z - 18.0), r + 0.3, r + 4.0), PANO, E, "pano_rakor"))
        out.append(("rakor", halka((x, y, PANO_Z - 18.0), (x, y, PANO_Z - 24.0), r + 0.3, r + 2.0), PANO, E, "pano_rakor"))
        if tur is None:
            out.append(("rakor", silindir((x, y, PANO_Z - 24.0), (x, y, PANO_Z - 27.0), r + 2.0, 20), PANO, E, "kor_tapa"))
    # bina + zemin kabloları: duvar (z −850) -> cep rakoru -> pano rakoru (düz)
    for k in ("bina", "bina_v", "zemin", "zemin_v"):
        x, y, r, tur = GECIS[k]
        mal = "kablo_guc" if tur == "guc" else "kablo_veri"
        mek = DUK if k.startswith("zemin") else PANO
        out.append((mal, tup([(x, y, Z_DUVAR), (x, y, PANO_Z - 24.0)], r, 16), mek, E, "bina_" + k))
    # kol kabloları: pano rakoru -> geri (−z) -> V1 içine iner
    for k, zd in (("sol", -816.0), ("sol_v", -816.0), ("sag", -796.0), ("sag_v", -796.0)):
        x, y, r, tur = GECIS[k]
        mal = "kablo_guc" if tur == "guc" else "kablo_veri"
        out.append((mal, tup([(x, y, PANO_Z - 24.0), (x, y, zd), (x, 2030.0 - 6.0, zd)], r, 16), PANO, E, "kol_" + k))


# ------------------------------------------------------------------ istasyon dışı bağlantı uçları (istasyon içinde)
def ic_baglar(out):
    E = "ELEKTRIK"
    # F: kompresör çıkışı -> H1 kanalı (2 hortum: J1 ve J2 hava)
    out.append(("hava", tup([(3549.0, 1809.0, -770.0), (3549.0, 1809.0, -806.0), (3549.0, Y0 + PDV[1] - 4.0, -806.0)], R_HAVA, 12), "F/Hava", "HAVA", "F_hava_cikis"))
    # K: J2 PD B kanalından K hava hattı başına (4040, 1809, −770)
    out.append(("hava", tup([(4040.0, Y0 + PDV[1] - 4.0, -777.0), (4040.0, 1809.0, -777.0), (4040.0, 1809.0, -770.3)], R_HAVA, 12), "K/Hava", "HAVA", "K_hava_giris"))
    # TOPPING: mevcut sağ dik kanaldan (x 2421–2449) çıkıp regülatör girişine (2470, 1165, −742) yandan
    out.append(("hava", tup([(2449.6, 1165.0, -805.0), (2480.0, 1165.0, -805.0), (2480.0, 1165.0, -742.0), (2470.5, 1165.0, -742.0)], R_HAVA, 12), "TOPPING/Hava", "HAVA", "T_hava_giris"))
    # F: yükleme bandı motor kablosu artık F kutusundan (kutu sol yüzü -> eski kablonun dirseği)
    out.append(("kablo_guc", tup([(2800.0, 900.0, -790.0), (2780.0, 900.0, -790.0), (2780.0, 1121.0, -790.0), (2780.0, 1121.0, -800.0)], 4.0, 12), "F/Elektrik", E, "F_bant_motor"))
    # F: V2 kanalından F kutusuna (kutu üstü y 950)
    out.append(("kablo_guc", tup([(2905.0, 960.0, -776.0), (2905.0, 950.0, -776.0)], R_GUC, 16), "F/Elektrik", E, "F_kutu_guc"))
    out.append(("kablo_veri", tup([(2920.0, 960.0, -776.0), (2920.0, 950.0, -776.0)], R_VERI, 12), "F/Elektrik", E, "F_kutu_veri"))


# ------------------------------------------------------------------ ZEMİN KOLU (pano -> duvar içi -> zemin kanalı -> B (alttan) -> QR (alttan) -> robot rezerv)
ZK = dict(d=70.0, w=100.0)
B_KOVAN = dict(x=(4065.0, 4115.0), z=(-665.0, -595.0))
QR_KOVAN = dict(x=(4978.0, 5006.0), z=(1005.0, 1045.0))
QRR_KOVAN = dict(x=(4730.0, 4770.0), z=(780.0, 820.0))
ROBOT_KUTU = dict(x=(4690.0, 4810.0), z=(300.0, 420.0), y=(-120.0, 0.0))
KAPAK = []


def zemin(out):
    D = DUK; E = "ELEKTRIK"
    d = ZK["d"]; t = 2.0
    KOV = [B_KOVAN, QR_KOVAN, QRR_KOVAN]
    def oluk(ax, a0, a1, c0, c1, uc=(True, True), delik=None):
        """zemin içi oluk (üstü açık) + kapak sacı (y −2 … 0, oluk duvarlarının arasında, kovan yerleri delik) · ax: 0 (x) / 2 (z)"""
        if ax == 0:
            g = kanal(0, a0, a1, (-d, c0), (0.0, c1), t, acik=[(1, 1)], uc=uc, delik=delik)
            xr, zr = (a0 + t, a1 - t), (c0 + t, c1 - t)
        else:
            g = kanal(2, a0, a1, (c0, -d), (c1, 0.0), t, acik=[(1, 1)], uc=uc, delik=delik)
            xr, zr = (c0 + t, c1 - t), (a0 + t, a1 - t)
        dl = [(K["x"][0], K["x"][1], K["z"][0], K["z"][1]) for K in KOV
              if K["x"][0] >= xr[0] - 1 and K["x"][1] <= xr[1] + 1 and K["z"][0] >= zr[0] - 1 and K["z"][1] <= zr[1] + 1]
        k = plaka(1, -2.0, 0.0, xr[0], xr[1], zr[0], zr[1], dl)
        out.append(("zemin_oluk", g, D, E, "zemin_oluk")); out.append(("zemin_kapak", k, D, E, "zemin_kapak"))
        KAPAK.append((xr, zr))
    # Z1: duvardan (z −850) B girişine ve koridora: x 4040–4140
    oluk(2, -850.0, 950.0, 4040.0, 4140.0, delik={(0, 1): [(852.0, 948.0, -68.0, -2.0)]})
    # Z2: koridor boyunca x: 4140 -> 5045, z 850–950 (Z3 ve Z4 ağızları)
    oluk(0, 4140.0, 5045.0, 850.0, 950.0, uc=(False, True), delik={(2, 1): [(4947.0, 5043.0, -68.0, -2.0)], (2, -1): [(4702.0, 4798.0, -68.0, -2.0)]})
    # Z3: QR altına: x 4945–5045, z 950 -> 1075
    oluk(2, 950.0, 1075.0, 4945.0, 5045.0, uc=(False, True))
    # Z4: robot kontrol kutusu -> robot rezerv kutusu: x 4700–4800, z 420 -> 850
    oluk(2, 420.0, 850.0, 4700.0, 4800.0, uc=(False, False))
    # robot rezerv zemin kutusu (gömme, kapaklı) + kapaklı Han 10B / M12 (kutu içinde)
    R = ROBOT_KUTU
    g = kanal(1, R["y"][0], R["y"][1], (R["x"][0], R["z"][0]), (R["x"][1], R["z"][1]), 2.0, uc=(True, False),
              delik={(2, 1): [(-68.0, -2.0, 4702.0, 4798.0)]})
    out.append(("zemin_oluk", g, D, E, "robot_kutu"))
    out.append(("zemin_kapak", kutu((R["x"][0] + 2, -2.0, R["z"][0] + 2), (R["x"][1] - 2, 0.0, R["z"][1] - 2)), D, E, "robot_kapak"))
    KAPAK.append(((R["x"][0] + 2, R["x"][1] - 2), (R["z"][0] + 2, R["z"][1] - 2)))
    out.append(("harting", kutu((4725.0, -118.0, 330.0), (4768.4, -89.1, 423.0 - 30.0)), D, E, "robot_han"))
    out.append(("harting", kutu((4726.0, -89.1, 335.0), (4767.4, -75.0, 388.0)), D, E, "robot_han_kapak"))
    out.append(("m12", silindir((4790.0, -118.0, 360.0), (4790.0, -100.0, 360.0), 9.0, 20), D, E, "robot_m12"))
    out.append(("kod_mavi", silindir((4790.0, -100.0, 360.0), (4790.0, -98.0, 360.0), 9.5, 20), D, E, "robot_m12_kapak"))
    # zemin kovanları (contalı, dikey): B (oluktan B tabanının 3 mm üstüne), QR, QR robot kontrol
    for ad, K, y1, mek in (("B", B_KOVAN, 128.0, "B/Elektrik"), ("QR", QR_KOVAN, 17.0, "QR/Elektrik"), ("QRR", QRR_KOVAN, 17.0, "QR/Elektrik")):
        g = kanal(1, -15.0, y1, (K["x"][0], K["z"][0]), (K["x"][1], K["z"][1]), 2.0, uc=(False, False))
        out.append(("conta", g, mek, E, "zemin_kovan_" + ad))
    # kablolar (oluk içinde, kapak altında): güç y −50, veri y −30
    def kab(mal, r, Q, mek, ad): out.append((mal, tup(Q, r, 16), mek, E, ad))
    # pano -> duvar içi -> zemin -> B girişi (x 4078 güç / 4102 veri)
    kab("kablo_guc", R_GUC, [(4078.0, -45.0, -847.5), (4078.0, -45.0, -630.0), (4078.0, 140.0, -630.0)], D, "zk_pano_B_guc")
    kab("kablo_veri", R_VERI, [(4102.0, -25.0, -847.5), (4102.0, -25.0, -640.0), (4102.0, 140.0, -640.0)], D, "zk_pano_B_veri")
    # B çıkışı -> QR (B kovanından aşağı, oluk boyunca)
    kab("kablo_guc", R_GUC, [(4078.0, 140.0, -610.0), (4078.0, -50.0, -610.0), (4078.0, -50.0, 900.0), (4995.0, -50.0, 900.0), (4995.0, -50.0, 1032.0), (4995.0, 125.0, 1032.0)], D, "zk_B_QR_guc")
    kab("kablo_veri", R_VERI, [(4102.0, 140.0, -620.0), (4102.0, -25.0, -620.0), (4102.0, -25.0, 880.0), (4985.0, -25.0, 880.0), (4985.0, -25.0, 1019.0), (4995.0, -25.0, 1019.0), (4995.0, 150.0, 1019.0)], D, "zk_B_QR_veri")
    # QR robot kontrol kutusu -> robot rezerv kutusu
    kab("kablo_guc", R_GUC, [(4742.0, 25.0, 800.0), (4742.0, -50.0, 800.0), (4742.0, -50.0, 361.5), (4742.0, -74.5, 361.5)], D, "zk_QR_robot_guc")
    kab("kablo_veri", R_VERI, [(4760.0, 25.0, 805.0), (4760.0, -25.0, 805.0), (4760.0, -25.0, 360.0), (4790.0, -25.0, 360.0), (4790.0, -97.5, 360.0)], D, "zk_QR_robot_veri")
    # B içi: kovan üstünden B panosu altına (y 605) — kanal
    kbox(out, "B_V", "B", (B_KOVAN["x"][0], 128.0, B_KOVAN["z"][0]), (B_KOVAN["x"][1], 575.0, B_KOVAN["z"][1]), uc=(False, False), e=1)
    kbox(out, "B_H", "B", (B_KOVAN["x"][0], 575.0, -665.0), (4200.0, 600.0, -615.0))


def salter(out):
    """Eaton P3-63/I4/SVB duvar şalteri: makinenin SAĞ UCUNUN yanında duvarda (x 5250–5410), duvara 70 mm gömme"""
    w, h, dd = 160.0, 240.0, 170.0; xc = 5330.0; yc = 1600.0; zf = Z_DUVAR + (dd - 70.0)
    D = DUK
    out.append(("salter_kutu", kutu((xc - w / 2, yc - h / 2, zf - dd), (xc + w / 2, yc + h / 2, zf)), D, "ELEKTRIK", "salter"))
    out.append(("salter_sari", kutu((xc - 45, yc - 45, zf), (xc + 45, yc + 45, zf + 2.0)), D, "ELEKTRIK", "salter"))
    out.append(("salter_kirmizi", silindir((xc, yc, zf + 2.0), (xc, yc, zf + 9.0), 22.0, 24), D, "ELEKTRIK", "salter"))
    out.append(("salter_kirmizi", kutu((xc - 9, yc - 38, zf + 9.0), (xc + 9, yc + 38, zf + 17.0)), D, "ELEKTRIK", "salter"))
    out.append(("salter_sari", kutu((xc + 30, yc - 48, zf + 2.0), (xc + 40, yc - 38, zf + 12.0)), D, "ELEKTRIK", "salter"))


def parcalar():
    out = []
    birlesimler(out); ic_kanallar(out); pano_giris(out); ic_baglar(out); zemin(out); salter(out)
    return out


if __name__ == "__main__":
    out = parcalar()
    print(len(out), "parça", sum(len(p[1]) for p in out), "üçgen")
