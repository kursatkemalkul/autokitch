# -*- coding: utf-8 -*-
"""Zincir elektrik geometrisi (dış): fiş panelleri, bağlantılar, kanallar, duvar şalteri, dirsek kutusu, robot rezerv kutusu.
parcalar() -> [(dugum_adi, malzeme_anahtari, P(n,3,3), mek_kodu)]"""
import numpy as np
from elib import kutu, plaka, kanal, silindir, tup, halka
from olcu import *

MAL = {
    "kablo_guc": ("ME2_kablo_guc", (0.753, 0.224, 0.169, 1.0), 0.0, 0.55),
    "kablo_veri": ("ME2_kablo_veri", (0.122, 0.373, 0.749, 1.0), 0.0, 0.55),
    "hava": ("ME2_hava_hortum", (0.20, 0.55, 0.90, 1.0), 0.0, 0.5),
    "paslanmaz": ("ME2_paslanmaz", (0.80, 0.82, 0.84, 1.0), 0.9, 0.30),
    "kanal": ("ME2_kanal", (0.70, 0.72, 0.74, 1.0), 0.8, 0.35),
    "harting": ("ME2_harting_ral7037", (0.48, 0.49, 0.49, 1.0), 0.5, 0.45),
    "kod_kirmizi": ("ME2_kod_kirmizi", (0.80, 0.10, 0.08, 1.0), 0.0, 0.5),
    "kod_mavi": ("ME2_kod_mavi", (0.10, 0.36, 0.80, 1.0), 0.0, 0.5),
    "m12": ("ME2_m12_govde", (0.22, 0.23, 0.25, 1.0), 0.6, 0.4),
    "rakor": ("ME2_rakor", (0.14, 0.14, 0.15, 1.0), 0.0, 0.5),
    "etiket": ("ME2_etiket", (0.95, 0.95, 0.92, 1.0), 0.0, 0.7),
    "salter_kutu": ("ME2_salter_gri", (0.82, 0.83, 0.84, 1.0), 0.0, 0.6),
    "salter_sari": ("ME2_salter_sari", (0.98, 0.80, 0.05, 1.0), 0.0, 0.5),
    "salter_kirmizi": ("ME2_salter_kirmizi", (0.80, 0.08, 0.06, 1.0), 0.0, 0.5),
}
DUG = {"kablo_guc": "ELK_ZINCIR__kablo_guc", "kablo_veri": "ELK_ZINCIR__kablo_veri", "hava": "ELK_ZINCIR__hava", "paslanmaz": "ELK_ZINCIR__paslanmaz",
       "kanal": "ELK_ZINCIR__kanal", "harting": "ELK_ZINCIR__harting", "kod_kirmizi": "ELK_ZINCIR__kod_kirmizi", "kod_mavi": "ELK_ZINCIR__kod_mavi",
       "m12": "ELK_ZINCIR__m12", "rakor": "ELK_ZINCIR__rakor", "etiket": "ELK_ZINCIR__etiket",
       "salter_kutu": "ELK_DUVAR__salter", "salter_sari": "ELK_DUVAR__salter_sari", "salter_kirmizi": "ELK_DUVAR__salter_kirmizi"}
MEK_IST = {"TOPPING": "TOPPING/Elektrik", "F": "F/Elektrik", "K": "K/Elektrik", "B": "B/Elektrik", "E": "E/Elektrik", "QR": "QR/Elektrik"}


def _ax(P, z0, sg):
    """yerel kutu (z: yuzeyden disari 0..h) -> dunya: sg=-1 disari -z (makine arkasi), sg=+1 ..."""
    return P


def panel(ist, out):
    """fiş paneli: dış yüz z0, dışarı yön s (-1: -z). Yerel: d = dışarı mesafe."""
    c = C[ist]
    if ist == "QR": z0, s, yc = 670.0, -1.0, YC["QR"]
    else: z0, s, yc = -832.0 + PANEL_T, -1.0, YC[ist]
    mek = MEK_IST[ist]
    def zz(d0, d1):
        a, b = z0 + s * d0, z0 + s * d1; return min(a, b), max(a, b)
    def K(x0, x1, y0, y1, d0, d1):
        za, zb = zz(d0, d1); return kutu((x0, y0, za), (x1, y1, zb))
    # plaka (yüzeyde, 2 mm) + 4 köşe vida başı yok (sade)
    out.append(("paslanmaz", K(c - PANEL_W / 2, c + PANEL_W / 2, yc - PANEL_H / 2, yc + PANEL_H / 2, 0, PANEL_T), mek))
    d = PANEL_T
    havali = ist in HAVALI
    ust = ist != "B"                    # kapak rakoru aşağı (üst sıra, QR) / yukarı (B)
    for k, dx in DX.items():
        x = c + dx
        if k.startswith("HAVA"):
            if not havali: continue
            za, zb = zz(d, d + HAVA_L)
            out.append(("rakor", silindir((x, yc, z0 + s * d), (x, yc, z0 + s * (d + 6)), 11.0, 6), mek))          # somun (altıgen ~)
            out.append(("rakor", silindir((x, yc, z0 + s * (d + 6)), (x, yc, z0 + s * (d + HAVA_L - 6)), HAVA_R, 16), mek))
            out.append(("kod_mavi", silindir((x, yc, z0 + s * (d + HAVA_L - 6)), (x, yc, z0 + s * (d + HAVA_L)), HAVA_R + 1.0, 16), mek))
            continue
        kapali = (ist == "TOPPING" and "CIKIS" in k)        # sol kolun ucu: çıkış kör kapaklı
        if k.startswith("GUC"):
            gx, gy, gh = HAN_GOV
            out.append(("harting", K(x - gx / 2, x + gx / 2, yc - gy / 2, yc + gy / 2, d, d + gh), mek))
            if kapali:
                out.append(("harting", K(x - gx / 2 + 1, x + gx / 2 - 1, yc - gy / 2 + 5, yc + gy / 2 - 5, d + gh, d + gh + 14), mek))   # koruma kapağı
                out.append(("kod_kirmizi", K(x - gx / 2 + 1, x + gx / 2 - 1, yc - 4, yc + 4, d + gh + 14, d + gh + 15), mek))
                continue
            kx, ky, kh = HAN_KAP
            out.append(("harting", K(x - kx / 2, x + kx / 2, yc - ky / 2, yc + ky / 2, d + gh, d + gh + kh), mek))
            out.append(("kod_kirmizi", K(x - kx / 2 + 4, x + kx / 2 - 4, yc - 10, yc + 18, d + gh + kh, d + gh + kh + 0.8), mek))   # kırmızı kod levhası (kapak sırtında)
            zg = z0 + s * (d + gh + kh / 2)
            if ust: out.append(("rakor", silindir((x, yc - ky / 2, zg), (x, yc - ky / 2 - HAN_RAKOR_L, zg), HAN_RAKOR_R, 20), mek))
            else: out.append(("rakor", silindir((x, yc + ky / 2, zg), (x, yc + ky / 2 + HAN_RAKOR_L, zg), HAN_RAKOR_R, 20), mek))
        else:
            fx, fy, fh = M12_FLANS
            out.append(("m12", K(x - fx / 2, x + fx / 2, yc - fy / 2, yc + fy / 2, d, d + fh), mek))
            if kapali:
                out.append(("m12", silindir((x, yc, z0 + s * (d + fh)), (x, yc, z0 + s * (d + fh + 12)), 9.0, 20), mek))
                out.append(("kod_mavi", silindir((x, yc, z0 + s * (d + fh + 12)), (x, yc, z0 + s * (d + fh + 14)), 9.5, 20), mek))
                continue
            out.append(("kod_mavi", silindir((x, yc, z0 + s * (d + fh)), (x, yc, z0 + s * (d + fh + 4)), M12_FIS_R + 0.8, 20), mek))    # mavi kod halkası
            out.append(("m12", silindir((x, yc, z0 + s * (d + fh + 4)), (x, yc, z0 + s * (d + fh + M12_FIS_L)), M12_FIS_R, 20), mek))
    # etiket levhaları GİRİŞ (sol yarı) / ÇIKIŞ (sağ yarı)
    ye = (yc + PANEL_H / 2 - 13, yc + PANEL_H / 2 - 4)
    for x0, x1 in ((c - 130, c - 20), (c + 20, c + 130)):
        out.append(("etiket", K(x0, x1, ye[0], ye[1], d, d + 0.6), mek))


def kanallar(out):
    t = KANAL["t"]; z0, z1 = KANAL["z"]; y0, y1 = KANAL["y"]; x0, x1 = KANAL["x"]
    A = "Elektrik/Ana hat"
    # üst yüzde ağızlar (üst sıra panelleri + yükseliş), alt yüzde ağızlar (B + iniş)
    ust_ag = []
    for ist in ("TOPPING", "F", "K", "E"):
        c = C[ist]; ust_ag.append((c - 135, c + 135, z0 + t + 0.5, z1 - t - 0.5))
    ust_ag.append((YUKSELIS["x"][0] + t, YUKSELIS["x"][1] - t, z0 + t, z1 - t))
    alt_ag = [(C["B"] - 135, C["B"] + 135, z0 + t + 0.5, z1 - t - 0.5), (INIS["x"][0] + t, INIS["x"][1] - t, z0 + t, z1 - t)]
    out.append(("kanal", kanal(0, x0, x1, (y0, z0), (y1, z1), t, delik={(1, 1): ust_ag, (1, -1): alt_ag}), A))
    # duvar konsolları (304 2 mm, dübelli): ana kanal her ~600 mm · iniş kanalları her ~500 mm
    for xk in np.arange(x0 + 60.0, x1 - 30.0, 600.0):
        out.append(("paslanmaz", kutu((xk - 20, y0 + 10, Z_DUVAR), (xk + 20, y1 - 10, z0)), A))
    for yk in np.arange(YUKSELIS["y"][0] + 250.0, YUKSELIS["y"][1], 500.0):
        out.append(("paslanmaz", kutu((YUKSELIS["x"][0] + 10, yk - 20, Z_DUVAR), (YUKSELIS["x"][1] - 10, yk + 20, z0)), A))
    for yk in (300.0, 600.0):
        out.append(("paslanmaz", kutu((INIS["x"][0] + 10, yk - 20, Z_DUVAR), (INIS["x"][1] - 10, yk + 20, z0)), A))
    # pano iniş (yükseliş) kanalı: x ekseninde değil, y boyunca: kesit (x, z)
    out.append(("kanal", kanal(1, YUKSELIS["y"][0], YUKSELIS["y"][1], (YUKSELIS["x"][0], z0), (YUKSELIS["x"][1], z1), t, uc=(False, False)), A))
    # dirsek kutusu: duvar (z −940) ↔ U arka sacı (z −830), y 2080–2168 · alt yüz yükselişe açık · +z yüz U'ya açık · −z yüz duvarda (bina girişi)
    D = DIRSEK
    out.append(("kanal", kanal(2, D["z"][0] + 2.0, D["z"][1] - 2.0, (D["x"][0], D["y"][0]), (D["x"][1], D["y"][1]), t, uc=(False, False),
                              delik={(1, -1): [(z0 + t, z1 - t, D["x"][0] + t, D["x"][1] - t)]}), A))
    # duvar flanşı (bina girişi, duvar yüzünde 2 mm)
    out.append(("paslanmaz", kutu((D["x"][0] - 15, D["y"][0] - 15, D["z"][0]), (D["x"][1] + 15, D["y"][1] + 5, D["z"][0] + 2.0)), "Çevre/Dükkân hattı"))
    # U arka sacına flanş çerçevesi (dış yüz, 2 mm, ağız çevresi)
    out.append(("paslanmaz", plaka(2, -832.0, -830.0, D["x"][0] - 8, D["x"][1] + 3, D["y"][0] - 8, D["y"][1] + 0,
                                   [(D["x"][0], D["x"][1], D["y"][0], D["y"][1])]), A))
    # E ucu iniş kanalı (zemine)
    out.append(("kanal", kanal(1, INIS["y"][0], INIS["y"][1], (INIS["x"][0], z0), (INIS["x"][1], z1), t, uc=(False, False)), A))
    # zemin kanalı (E altı + koridor) : z boyunca, kesit (x, y) · üst kapak (gözyaşı) · iniş ağzı (üstte, z0..z1)
    Zm = ZEMIN; zm0, zm1 = Zm["z"]
    g = kanal(2, zm0, zm1, (Zm["x"][0], Zm["y"][0]), (Zm["x"][1], Zm["y"][1]), t, uc=(True, False),
              delik={(1, 1): [(z0 + t, z1 - t, INIS["x"][0] + t, INIS["x"][1] - t)],
                     (0, -1): [(ROBOT_KUTU["z"][0] + 10, ROBOT_KUTU["z"][1] - 10, Zm["y"][0] + t, Zm["y"][1] - t)]})
    # makine içi (z < 79) Ana hat, koridor Dükkân hattı: üçgen ağırlık merkezine göre böl
    cz = g.mean(1)[:, 2]
    out.append(("kanal", g[cz < 79.0], A)); out.append(("kanal", g[cz >= 79.0], "Çevre/Dükkân hattı"))
    # QR önü başlık: x 5060–5400 · z 560–668 · üst yüzde QR fiş ağızları
    Hb = ZEMIN_BAS
    ag = [(C["QR"] + DX[k] - 18, C["QR"] + DX[k] + 18, 600.0, 650.0) for k in ("GUC_GIRIS", "VERI_GIRIS", "VERI_CIKIS", "GUC_CIKIS")]
    hb = kanal(0, Hb["x"][0], Hb["x"][1], (Hb["y"][0], Hb["z"][0]), (Hb["y"][1], Hb["z"][1]), t,
               delik={(1, 1): ag, (2, -1): [(Zm["x"][0] + t, Zm["x"][1] - t, Zm["y"][0] + t, Zm["y"][1] - t)]})
    out.append(("kanal", hb, "Çevre/Dükkân hattı"))
    # robot rezerv kutusu (kapaklı GİRİŞ: Han 10B koruma kapaklı + M12 kapaklı) — −x yüzünde
    R = ROBOT_KUTU
    rk = kanal(1, R["y"][0], R["y"][1], (R["x"][0], R["z"][0]), (R["x"][1], R["z"][1]), t,
               delik={(0, 1): [(Zm["y"][0] + t, Zm["y"][1] - t, R["z"][0] + 10, R["z"][1] - 10)]})
    out.append(("paslanmaz", rk, "Çevre/Dükkân hattı"))
    xf = R["x"][0]; zc = (R["z"][0] + R["z"][1]) / 2
    gx, gy, gh = HAN_GOV
    out.append(("harting", kutu((xf - gh, 70 - gy / 2 + 20, zc + 15 - gx / 2), (xf, 70 + gy / 2 - 20, zc + 15 + gx / 2)), "Çevre/Dükkân hattı"))
    out.append(("harting", kutu((xf - gh - 14, 70 - gy / 2 + 25, zc + 15 - gx / 2 + 1), (xf - gh, 70 + gy / 2 - 25, zc + 15 + gx / 2 - 1)), "Çevre/Dükkân hattı"))
    out.append(("kod_kirmizi", kutu((xf - gh - 15, 66, zc + 15 - gx / 2 + 1), (xf - gh - 14, 74, zc + 15 + gx / 2 - 1)), "Çevre/Dükkân hattı"))
    out.append(("m12", kutu((xf - 3, 70 - 13, zc - 40 - 13), (xf, 70 + 13, zc - 40 + 13)), "Çevre/Dükkân hattı"))
    out.append(("m12", silindir((xf - 3, 70, zc - 40), (xf - 15, 70, zc - 40), 9.0, 20), "Çevre/Dükkân hattı"))
    out.append(("kod_mavi", silindir((xf - 15, 70, zc - 40), (xf - 17, 70, zc - 40), 9.5, 20), "Çevre/Dükkân hattı"))
    # panel altı / üstü kısa dik kanallar (fiş cebi): üst sıra y 840–858 · B y 430–740
    for ist in ("TOPPING", "F", "K", "E"):
        c = C[ist]; yt = YC[ist] - HAN_KAP[1] / 2 - HAN_RAKOR_L - 2.0
        out.append(("kanal", kanal(1, y1, yt, (c - 140, z0 + 30), (c + 140, z1), t, uc=(False, False)), A))
    c = C["B"]
    out.append(("kanal", kanal(1, YC["B"] + HAN_KAP[1] / 2 + HAN_RAKOR_L + 2, y0, (c - 140, z0 + 30), (c + 140, z1), t, uc=(False, False)), A))


def salter(out):
    """Eaton P3-63/I4/SVB duvar şalteri: 160 × 240 × 170 — duvara 70 mm gömme (görünen 100), kol makine arkasına 3 mm kala"""
    w, h, dd = SALTER; xc = (3518.0 + 3978.0) / 2; yc = 1600.0
    zf = -850.0                      # ön yüz
    D = "Çevre/Dükkân hattı"
    out.append(("salter_kutu", kutu((xc - w / 2, yc - h / 2, zf - dd), (xc + w / 2, yc + h / 2, zf)), D))
    out.append(("salter_sari", kutu((xc - 45, yc - 45, zf), (xc + 45, yc + 45, zf + 2.0)), D))
    out.append(("salter_kirmizi", silindir((xc, yc, zf + 2.0), (xc, yc, zf + 9.0), 22.0, 24), D))
    out.append(("salter_kirmizi", kutu((xc - 9, yc - 38, zf + 9.0), (xc + 9, yc + 38, zf + 17.0)), D))
    # kilit kulağı (asma kilit) sarı
    out.append(("salter_sari", kutu((xc + 30, yc - 48, zf + 2.0), (xc + 40, yc - 38, zf + 12.0)), D))


def parcalar():
    out = []
    for ist in ("TOPPING", "F", "K", "B", "E", "QR"): panel(ist, out)
    kanallar(out); salter(out)
    return out
