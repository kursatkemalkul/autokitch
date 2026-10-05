# -*- coding: utf-8 -*-
"""AUTOKITCH · KK DENEME · KESME + SPREY + KUTU KATLAMA TEK İSTASYONDA — BASİT KAVRAM MODELİ v1 (27 Eyl 2026)
Kemal: "daha basit bir modelle mantığını animasyon yap hızlıca; kafama yatarsa doğru bir modellemesini yaparsın."

FİKİR: K modülü kalkar. E'nin (kutu_cad_v3) kutu mekanizması aynen kalır (şarjör arkada, itici, kalıp, piston kafası, kol). Üstüne:
  1 · kalıp bölgesinin üstünde, x boyunca GERİ ÇEKİLEN BURUNLU BANT (paketlemede "drop loader"): burun kutunun üstüne 342 mm uzar,
      ürün fırından bantla gelir, bantta kesilir, burun geri kaçarken bant aynı hızda ileri koşar → ürün olduğu yerde kutuya iner.
  2 · E piston kafasının içinde GERİ ÇEKİLEN BIÇAK YILDIZI (Ø296, 46 mm iner) + ortada PulsaJet nozülü (kutunun içine sprey).
  3 · tereyağı tankı E'nin boş alt dolabında.
  İstasyon 830 (= E). Hat 5430 → 4830.
BASİT MODEL: parçalar prizma/silindir. Kutunun flapları, köşe tırnakları, iç ön panel, parmak, U çerçeve, asansör, pano, burun tahriki,
  bandın dönüş kolu YOK. Kotlar: kutu tabanı 1090 (E'de 1104; bant 1164'ün altından geçsin diye 14 aşağı), bant üstü 1164 (fırın 1166 − 2),
  burun bıçak ağzı Ø10 → bant altı 1150, kutu duvarı üstü 1133,6 (pay 16,4).
KOORDİNAT: istasyon yereli x 0..830 (hatta 4000 + x), y yerden, z 0 ön yüz, −830 arka.
"""
import json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
from kaset_3d_v3 import Mesh, MM, MALZEME

for _k, _v in {"sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3),
               "celik": ((0.55, 0.57, 0.60, 1.0), 0.9, 0.35), "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45),
               "plastik": ((0.55, 0.57, 0.60, 1.0), 0.0, 0.6), "karton": ((0.74, 0.57, 0.38, 1.0), 0.0, 0.9),
               "karton_yigin": ((0.66, 0.50, 0.33, 1.0), 0.0, 0.95), "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85),
               "sos": ((0.80, 0.30, 0.16, 1.0), 0.0, 0.7), "robot": ((0.96, 0.62, 0.10, 1.0), 0.2, 0.45),
               "pu_bant": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.55), "kesik": ((0.35, 0.22, 0.12, 1.0), 0.0, 0.9),
               "hortum_isi": ((0.85, 0.20, 0.15, 1.0), 0.0, 0.6), "pom": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.42),
               "mavi": ((0.20, 0.45, 0.90, 1.0), 0.1, 0.5), "yesil": ((0.15, 0.60, 0.35, 1.0), 0.1, 0.5)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2]))
MALZEME.setdefault("kabuk", dict(renk=(0.78, 0.81, 0.85, 0.14), met=0.3, ruf=0.4, saydam=True))
MALZEME.setdefault("referans", dict(renk=(0.62, 0.66, 0.72, 0.28), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("sprey", dict(renk=(0.98, 0.88, 0.45, 0.30), met=0.0, ruf=0.6, saydam=True))

kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))

# ================================================================ ÖLÇÜLER (istasyon yereli, mm) ================================================================
W, H, D = 830.0, 2030.0, 830.0
SAC = 1.5; Y_PLINT = 123.0
DY = -14.0                                   # kutu bölgesi E'ye göre 14 aşağı (bant kutu duvarlarının üstünden geçsin)
TEPSI = 1104.0 + DY                          # 1090 · kutu tabanının oturduğu yüz
T = 1.6
KALIP = 1149.5 + DY                          # 1135,5
YB = 1149.6 + DY                             # 1135,6 · düz blankın alt yüzü
H_UST = 1478.0                               # piston kafası altı (dinlenme)
BX0, BX1 = 100.0, 420.0
ZB = -206.0                                  # kutu ekseni (E ile aynı)
BZ0, BZ1 = ZB - 160.0, ZB + 160.0
H_YAN, H_ON, H_ARKA = 42.0, 42.0, 44.0
L_KAP, W_KAP, H_KF = 312.0, 315.0, 36.0
ZL0, ZL1 = ZB - W_KAP / 2.0, ZB + W_KAP / 2.0
X_BL0 = BX0 - H_ON                           # 58 (basit: tek ön duvar)
X_BL1 = BX1 + H_ARKA + L_KAP + H_KF          # 812
Z_BL0, Z_BL1 = BZ0 - H_YAN, BZ1 + H_YAN
BESLE = 411.0
ZS0, ZS1 = Z_BL0 - BESLE, Z_BL1 - BESLE      # şarjör −819 … −415
Y_PLAT = 240.0
U_MAX = YB - TEPSI                           # 45,6
KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)       # kapak menteşesi (420 · 1134,8)
KOL_P = (560.0, 1080.0 + DY); KOL_R = 166.0
KM_UST = TEPSI + H_ARKA                      # 1134 kapak masası üstü
KAPAK_BASKI = KMER[1] + T / 2.0 + 0.2        # 1135,8
H_BEKLE = 1467.0 + DY                        # 1453
X_CATAL = ((157.0, 183.0), (247.0, 273.0), (337.0, 363.0))
X_BAR = ((BX0, 155.0), (185.0, 245.0), (275.0, 335.0), (365.0, BX1))
CATAL_DIS = 700.0
# ---- geri çekilen burunlu bant ----
BANT = 1164.0; BANT_K = 2.0; PL_K = 10.0
BANT_Z = (-402.0, -36.0)                     # 366 geniş (ürün −56…−356)
X_KUYRUK, R_KUYRUK = 45.0, 25.0              # Interroll RollerDrive EC5000 Ø50 (tahrik kuyrukta)
Y_KUYRUK = BANT - BANT_K - R_KUYRUK          # 1137
X_BURUN_GERI, X_BURUN_ILERI = 88.0, 430.0    # burun ekseni: geri (kafanın 24 mm solunda) · ileri (kutunun üstünde)
R_BURUN = 5.0                                # bıçak ağzı burun çubuğu Ø10
Y_BURUN = BANT - BANT_K - R_BURUN            # 1157 → bant altı 1150
X_PL0 = X_KUYRUK + R_KUYRUK                  # 70 · üst kol plakasının başı
L0 = 400.0
Y_DANS_GERI, Y_DANS_ILERI = 758.0, 1100.0    # dansçı makara: burun geride → aşağıda (bant fazlası), ileride → yukarıda
Y_TAIL_ALT = Y_KUYRUK - R_KUYRUK             # 1112
# ---- ürün ----
PZ_R, PZ_H = 150.0, 15.0
PIDE0 = (-300.0, 1166.0, -249.0)             # fırın bandında bekler (fırın ekseni −249)
XC = (BX0 + BX1) / 2.0                       # 260 · kesme = kutu merkezi
ZC = ZB
# ---- kafa (E piston kafası + bıçak yıldızı + nozül) ----
PK_X = (112.0, 408.0); PK_Z = (-354.0, -58.0)
BICAK_R0, BICAK_R1, BICAK_H, BICAK_T = 15.0, 148.0, 45.0, 1.5
BICAK_STROK = 46.0
Y_KES_PLAKA = BANT + 0.5 + BICAK_H           # 1209,5 · kesimde kafa plakası altı (bıçak ağzı bandın 0,5 üstünde)
Y_SPREY_PLAKA = TEPSI + T + PZ_H + 150.0 + 12.0  # 1268,6 · nozül ucu (plakanın 12 altı) pideden 150 mm
PARCALAR = []


def ekle(ad, wp, mal, grup="SABIT"):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup))


def radyal(r0, r1, t, y0, y1, phi):
    b = kut(r0, r1, y0, y1, -t / 2.0, t / 2.0)
    return b.rotate((0, 0, 0), (0, 1, 0), -phi).translate((XC, 0, ZC))


# ================================================================ GÖVDE + FIRIN ÇIKIŞI (referans) ================================================================
def govde():
    for i, (ax, az) in enumerate(((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0))):
        ekle("ayak_%d" % i, sily(ax, az, 6.0, 0.0, Y_PLINT), "celik")
    ekle("taban_sac", kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, -SAC), "sac")
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, 0), "kabuk")
    ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, 1100.0, 1240.0, -420.0, -8.0)), "kabuk")
    ekle("sag_sac", kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, 0), "kabuk")
    ekle("on_alt_sac", kut(SAC, W - SAC, Y_PLINT + 3.0, 1085.0 + DY, -SAC, 0), "kabuk")
    ekle("on_ust_kapak", kut(SAC, W - SAC, 1345.0 + DY, H - SAC, -SAC, 0), "kabuk")
    ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1330.0 + DY, 1345.0 + DY, -40.0, -20.0), "celik")
    # fırın çıkışı (F modülünün son 300 mm'si, referans)
    ekle("REF_firin_govdesi", kut(-300.0, 0.0, 956.0, 1473.0, -730.0, 0.0), "referans")
    ekle("REF_firin_bandi", kut(-300.0, -4.0, 1160.0, 1166.0, -473.5, -92.5), "celik")
    ekle("REF_olu_plaka", kut(-3.0, 18.0, 1164.5, 1166.0, -399.0, -99.0), "sac")
    # tereyağı tankı (alt dolap)
    ekle("yag_tanki_3L", sily(140.0, -540.0, 80.0, 665.0, 945.0), "sac")
    ekle("yag_tanki_kapagi", sily(140.0, -540.0, 88.0, 945.0, 959.0), "sac")
    ekle("yag_tanki_rafi", kut(40.0, 290.0, 660.0, 665.0, -700.0, -380.0), "sac")


# ================================================================ E MEKANİZMASI (basit) ================================================================
def sarjor_ve_itici():
    ekle("karton_yigini", kut(X_BL0, X_BL1, Y_PLAT, YB - T, ZS0, ZS1), "karton_yigin")
    ekle("asansor_platformu", kut(X_BL0, X_BL1, Y_PLAT - 3.0, Y_PLAT, ZS0, ZS1), "aluminyum")
    ekle("besleyici_plakasi", kut(100.0, 721.0, 1500.0 + DY, 1505.0 + DY, -828.0, -367.0), "aluminyum")
    ekle("itici_cubugu", kut(10.0, 810.0, YB + 0.6, YB + 7.0, -826.0, -819.5), "celik", "ITICI")
    ekle("itici_kirisi", kut(10.0, 810.0, YB + 7.0, YB + 27.0, -826.0, -819.5), "aluminyum", "ITICI")
    for i, xr in enumerate((150.0, 650.0)):
        ekle("itici_asma_plakasi_%d" % i, kut(xr - 20.0, xr + 20.0, YB + 27.0, 1500.0 + DY - 34.0, -826.0, -818.0), "aluminyum", "ITICI")


def kalip():
    ekle("kalip_tablasi", kut(90.0, 430.0, 1080.0 + DY, 1086.0 + DY, -372.5, -32.0), "sac")
    for i, (xp, zp) in enumerate(((110.0, -340.0), (410.0, -340.0), (110.0, -70.0), (410.0, -70.0))):
        ekle("kalip_ayagi_%d" % i, kut(xp - 20.0, xp + 20.0, Y_PLINT + 3.0, 1080.0 + DY, zp - 20.0, zp + 20.0), "aluminyum")
    for i, (x0, x1) in enumerate(X_BAR):
        ekle("tepsi_cubugu_%d" % i, kut(x0, x1, 1096.0 + DY, TEPSI, BZ0, BZ1), "sac")
    ekle("kalip_rayi_arka", kut(BX0, 405.0, 1086.0 + DY, KALIP, BZ0 - T - 6.0, BZ0 - T - 0.5), "sac")
    for i, (x0, x1) in enumerate(X_BAR):
        ekle("kalip_taragi_on_%d" % i, kut(max(x0, BX0), min(x1, 405.0), 1086.0 + DY, KALIP, BZ1 + T + 0.5, BZ1 + T + 6.5), "sac")
    ekle("kalip_on_x_rayi", kut(93.4, 97.9, 1086.0 + DY, 1129.5 + DY, BZ0, BZ1), "sac")
    ekle("kalip_arka_x_dayagi", kut(BX1 + T + 0.5, BX1 + T + 6.5, 1086.0 + DY, TEPSI + 8.0, BZ0, BZ1), "sac")
    # kapak masası + kol
    m = kut(466.0, 730.0, KM_UST - 3.0, KM_UST, ZL0 + 1.5, ZL1 - 1.5).cut(kut(465.0, 745.0, KM_UST - 4.0, KM_UST + 1.0, ZB - 13.0, ZB + 13.0))
    ekle("kapak_masasi", m, "sac")
    for i, zc in enumerate((ZB - 110.0, ZB + 110.0)):
        ekle("kapak_masasi_diregi_%d" % i, sily(600.0, zc, 8.0, 1000.0, KM_UST - 3.0), "celik")
    px, py = KOL_P
    kol = kut(px, px + KOL_R, py - 6.0, py + 6.0, ZB - 10.0, ZB + 10.0).union(silz(px, py, 14.0, ZB - 10.0, ZB + 10.0))
    kol = kol.union(silz(px + KOL_R, py, 10.0, ZB - 12.0, ZB + 12.0))
    ekle("kapak_kolu", kol, "celik", "KOL")
    ekle("kapak_kolu_mili", silz(px, py, 6.0, ZB - 26.0, -150.0), "celik")
    ekle("kol_reduktor_motor", kut(px - 28.0, px + 28.0, py - 28.0, py + 28.0, -150.0, -1.0), "motor")
    ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 1000.0, py - 29.0, -150.0, -140.0), "aluminyum")


def kafa():
    """E piston kafası: plaka 296 × 296 × 20 + kaburgalar + bağlantı plakası; içinde bıçak yıldızı (BICAK) ve nozül (sabit)"""
    h = H_UST
    pl = kut(PK_X[0], PK_X[1], h, h + 20.0, PK_Z[0], PK_Z[1])
    for i in range(6):
        pl = pl.cut(radyal(BICAK_R0 - 2.0, BICAK_R1 + 2.0, BICAK_T + 1.0, h - 1.0, h + 21.0, 60.0 * i))
    pl = pl.cut(sily(XC, ZC, 11.0, h - 1.0, h + 21.0))
    ekle("piston_kafasi", pl, "aluminyum", "KAFA")
    for i, xc_ in enumerate((200.0, 320.0)):
        ekle("piston_kaburgasi_%d" % i, kut(xc_ - 4.0, xc_ + 4.0, h + 20.0, h + 70.0, PK_Z[0] + 5.0, PK_Z[1] - 5.0), "aluminyum", "KAFA")
    ekle("piston_baglanti_plakasi", kut(170.0, 370.0, h + 20.0, h + 535.0, -361.0, -351.0), "aluminyum", "KAFA")
    for i, xr in enumerate((200.0, 340.0)):
        for j, yc in enumerate((h + 440.0, h + 500.0)):
            ekle("piston_arabasi_%d%d" % (i, j), kut(xr - 17.0, xr + 17.0, yc - 20.0, yc + 20.0, -389.0, -361.0), "celik", "KAFA")
        ekle("piston_rayi_%d" % i, kut(xr - 7.5, xr + 7.5, 1500.0, 2015.0, -389.0, -374.0), "celik")
    ekle("piston_eksen_plakasi", kut(170.0, 370.0, 1500.0, 2015.0, -394.0, -389.0), "aluminyum")
    ekle("piston_eksen_askisi", kut(170.0, 370.0, 2015.0, H - SAC, -394.0, -380.0), "aluminyum")
    ekle("piston_motoru", kut(312.0, 368.0, 1990.0, 2028.0, -346.0, -290.0), "motor")
    # bıçak yıldızı: geri çekilmiş konumda plakanın içinde (h+1 … h+46); kesimde 46 aşağı
    ekle("bicak_gobek_halkasi", sily(XC, ZC, 20.0, h + 1.0, h + 13.0).cut(sily(XC, ZC, 13.0, h, h + 14.0)), "celik", "BICAK")
    for i in range(6):
        ekle("bicak_%d" % i, radyal(BICAK_R0, BICAK_R1, BICAK_T, h + 1.0, h + 1.0 + BICAK_H, 60.0 * i), "celik", "BICAK")
    ekle("bicak_silindiri_CDQ2B50-50", sily(XC + 60.0, ZC + 60.0, 25.0, h + 20.0, h + 92.0), "aluminyum", "KAFA")
    ekle("bicak_tasiyici_capraz", kut(XC - 90.0, XC + 90.0, h + 46.0, h + 52.0, ZC - 6.0, ZC + 6.0).union(kut(XC - 6.0, XC + 6.0, h + 46.0, h + 52.0, ZC - 90.0, ZC + 90.0)), "celik", "BICAK")
    # nozül (sabit, kafada) + PulsaJet
    ekle("UniJet_nozul_govdesi", sily(XC, ZC, 10.0, h - 6.0, h + 30.0), "celik", "KAFA")
    ekle("sprey_ucu_TG", sily(XC, ZC, 7.0, h - 12.0, h - 6.0), "pom", "KAFA")
    ekle("PulsaJet_AA10000AUH", silx(h + 50.0, ZC, 19.0, XC + 5.0, XC + 105.0), "celik", "KAFA")
    ekle("sprey_dirsegi", kut(XC - 7.0, XC + 7.0, h + 30.0, h + 58.0, ZC - 7.0, ZC + 7.0), "celik", "KAFA")
    ekle("isitmali_hortum", silx(h + 50.0, ZC, 5.0, XC + 105.0, 372.0), "hortum_isi", "KAFA")
    # sprey konisi (görsel; kafa ile iner)
    ekle("sprey_konisi", cq.Workplane(obj=cq.Solid.makeCone(145.0, 3.0, 150.0, cq.Vector(XC, h - 12.0 - 150.0, ZC), cq.Vector(0, 1, 0))), "sprey", "SPREY")


def bant():
    """geri çekilen burunlu bant: kuyruk (RollerDrive) sabit · üst kol plakası + bant burunla uzar (ölçek) · dansçı makara aşağı-yukarı"""
    z0, z1 = BANT_Z
    ekle("kuyruk_rulosu_RollerDrive_EC5000", silz(X_KUYRUK, Y_KUYRUK, R_KUYRUK, z0 - 10.0, z1 + 10.0), "aluminyum")
    ekle("kuyruk_rulosu_mili", silz(X_KUYRUK, Y_KUYRUK, 6.0, z0 - 30.0, z1 + 30.0), "celik")
    for i, zz in enumerate((z0 - 20.0, z1 + 20.0)):
        ekle("kuyruk_yatagi_%d" % i, kut(X_KUYRUK - 15.0, X_KUYRUK + 15.0, Y_KUYRUK - 20.0, Y_KUYRUK + 20.0, zz - 6.0, zz + 6.0), "celik")
    ekle("bant_ust_kolu_plaka", kut(X_PL0, X_PL0 + L0, BANT - BANT_K - PL_K, BANT - BANT_K, z0, z1), "sac", "BANT_UST")
    ekle("bant_ust_kolu_PU", kut(X_PL0, X_PL0 + L0, BANT - BANT_K, BANT, z0, z1), "pu_bant", "BANT_UST")
    # burun arabası: bıçak ağzı çubuğu + iki yan araba (MGN12) + alt köprü
    xn = X_BURUN_GERI
    ekle("burun_cubugu_Ø10", silz(xn, Y_BURUN, R_BURUN, z0, z1), "celik", "BURUN")
    for i, (za, zb) in enumerate(((-33.0, -6.0), (-450.0, -424.0))):
        ekle("burun_arabasi_MGN12_%d" % i, kut(xn - 80.0, xn + 10.0, 1160.0, 1173.0, za, zb), "celik", "BURUN")
    ekle("burun_alt_koprusu", kut(xn - 60.0, xn - 50.0, 1145.0, 1152.0, -450.0, -6.0), "aluminyum", "BURUN")
    for i, (za, zb) in enumerate(((-25.0, -13.0), (-443.0, -431.0))):
        ekle("burun_rayi_MGN12_%d" % i, kut(20.0, 470.0, 1160.0, 1168.0, za, zb), "celik")
        ekle("burun_ray_askisi_%d" % i, kut(20.0, 470.0, 1168.0, 1176.0, za - 4.0, zb + 4.0), "aluminyum")
    # dansçı makara + iki şerit (bant fazlası)
    ekle("dansci_makara", silz(X_KUYRUK, Y_DANS_GERI, 15.0, z0, z1), "aluminyum", "DANSCI")
    ekle("dansci_kizagi", kut(X_KUYRUK - 4.0, X_KUYRUK + 4.0, 740.0, 1120.0, z0 - 20.0, z0 - 12.0), "celik")
    for i, xx in enumerate((X_KUYRUK - R_KUYRUK, X_KUYRUK + R_KUYRUK - 2.0)):
        ekle("dansci_seridi_%d" % i, kut(xx, xx + 2.0, Y_DANS_GERI, Y_TAIL_ALT, z0, z1), "pu_bant", "DANS_SERIT")
    # giriş çiti (ürünü −249'dan −206'ya alır): bandın arka kenarında 20°
    pts = [(0.0, -402.0), (150.0, -359.0), (470.0, -359.0), (470.0, -356.0), (150.0, -356.0), (0.0, -399.0)]
    ekle("giris_citi_20", cq.Workplane("XZ", origin=(0, BANT + 1.0, 0)).polyline(pts).close().extrude(-20.0), "pom")
    for i, x in enumerate((60.0, 300.0, 440.0)):
        ekle("cit_braketi_%d" % i, kut(x - 6.0, x + 6.0, BANT + 21.0, BANT + 26.0, -431.0, -356.0), "sac")


def urun_ve_catal():
    x, y, z = PIDE0
    ekle("pide_hamur", sily(x, z, PZ_R, y, y + 11.0), "hamur", "PIDE")
    ekle("pide_ustu", sily(x, z, 142.0, y + 11.0, y + PZ_H, "sos", "PIDE") if False else sily(x, z, 142.0, y + 11.0, y + PZ_H), "sos", "PIDE")
    for i in range(6):
        b = kut(15.0, 142.0, y + PZ_H - 0.5, y + PZ_H + 0.6, -1.5, 1.5).rotate((0, 0, 0), (0, 1, 0), -60.0 * i).translate((x, 0, z))
        ekle("kesik_%d" % i, b, "kesik", "KESIK")
    for i, (x0, x1) in enumerate(X_CATAL):
        ekle("robot_catal_disi_%d" % i, kut(x0, x1, 1094.0 + DY, 1102.0 + DY, BZ0 + 2.0 + CATAL_DIS, 60.0 + CATAL_DIS), "robot", "CATAL")
    ekle("robot_catal_govdesi", kut(140.0, 380.0, 1080.0 + DY, 1112.0 + DY, 60.0 + CATAL_DIS, 76.0 + CATAL_DIS), "robot", "CATAL")


def blank():
    def panel(x0, x1, z0, z1): return kut(x0, x1, YB, YB + T, z0, z1)
    ekle("B_TABAN", panel(BX0, BX1, BZ0, BZ1), "karton", "B_ROOT")
    ekle("B_YAN_ARKA", panel(BX0 + T, BX1 - T, Z_BL0, BZ0), "karton", "B_SWM")
    ekle("B_YAN_ON", panel(BX0 + T, BX1 - T, BZ1, Z_BL1), "karton", "B_SWP")
    ekle("B_ON_DUVAR", panel(X_BL0, BX0, BZ0, BZ1), "karton", "B_FO")
    ekle("B_ARKA_MENTESE", panel(BX1, BX1 + H_ARKA, BZ0, BZ1), "karton", "B_BW")
    xk0 = BX1 + H_ARKA
    ekle("B_KAPAK", panel(xk0 + 0.2, xk0 + L_KAP, ZL0, ZL1), "karton", "B_LID")
    ekle("B_KAPAK_ON_FLAP", panel(xk0 + L_KAP + 0.2, X_BL1, ZL0 + 3.0, ZL1 - 3.0), "karton", "B_LID")


DUGUM = {
    "B_ROOT": (None, (0.0, 0.0, 0.0), None),
    "B_SWM": ("B_ROOT", (0.0, YB + T, BZ0), "x"),
    "B_SWP": ("B_ROOT", (0.0, YB + T, BZ1), "x"),
    "B_FO": ("B_ROOT", (BX0, YB + T, 0.0), "z"),
    "B_BW": ("B_ROOT", (BX1, YB + T / 2.0, 0.0), "z"),
    "B_LID": ("B_BW", (BX1 + H_ARKA, YB + T / 2.0, 0.0), "z"),
}

# ================================================================ ZAMAN ÇİZELGESİ (20 sn) ================================================================
DONGU = 20.0
Z_BESLE = (0.5, 1.7); Z_ITICI_DON = (1.8, 2.8)
Z_INIS = (1.9, 2.7); Z_ZIMBA = (2.7, 3.3); Z_KALK1 = (3.3, 4.0)
Z_BURUN_UZA = (4.2, 5.2)
Z_GELIS = (5.2, 6.6)
Z_BICAK_AC = (6.0, 6.5); Z_KES_IN = (6.8, 7.5); Z_KES = (7.5, 7.9); Z_KES_UP = (7.9, 8.4); Z_BICAK_KAPA = (8.4, 8.9)
Z_BURUN_CEK = (8.6, 9.7); Z_DUS = (9.05, 9.5)
Z_SPREY_IN = (9.9, 10.3); Z_SPREY = (10.3, 11.5); Z_SPREY_UP = (11.5, 11.9)
Z_KOL = (11.8, 12.1, 12.9); Z_KAFA_HAZIR = (12.9, 13.2); Z_YATIR = (13.2, 13.5)
Z_KAPAT = (13.5, 14.5, 14.8, 15.4); Z_KOL_DON = (13.55, 14.4)
Z_CATAL = (15.6, 16.7, 17.1, 18.6); Z_GIZLE = (19.6, 19.98)


def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    x = (t - a) / (b - a); return x * x * (3.0 - 2.0 * x)


def lin(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    return (t - a) / (b - a)


def u_zimba(t):
    if t < Z_ZIMBA[0]: return 0.0
    if t < Z_ZIMBA[1]: return U_MAX * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    return U_MAX


def kapak_acisi_kafa(h):
    s = (h - (KMER[1] + T / 2.0 + 1.5)) / L_KAP
    s = max(-1.0, min(1.0, s))
    return 180.0 - math.degrees(math.asin(s))


def kol_icin_beta(alfa):
    a = math.radians(alfa); hx, hy = KMER
    def f(b):
        cx = KOL_P[0] + KOL_R * math.cos(b); cy = KOL_P[1] + KOL_R * math.sin(b)
        return math.sin(a) * (cx - hx) - math.cos(a) * (cy - hy) - (10.0 + T / 2.0)
    lo, hi = 0.0, math.radians(175.0); flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2.0; fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return math.degrees((lo + hi) / 2.0)


BETA_TEMAS = kol_icin_beta(0.0); BETA_100 = kol_icin_beta(100.0)


def kafa_y(t):
    """kafa plakası alt yüzü"""
    if t < Z_INIS[0]: return H_UST
    if t < Z_INIS[1]: return H_UST + (YB + T - H_UST) * ss(Z_INIS[0], Z_INIS[1], t)
    if t < Z_ZIMBA[1]: return (YB + T) + (TEPSI + T - (YB + T)) * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    if t < Z_KALK1[1]: return (TEPSI + T) + (H_UST - (TEPSI + T)) * ss(Z_KALK1[0], Z_KALK1[1], t)
    if t < Z_KES_IN[0]: return H_UST
    if t < Z_KES_IN[1]: return H_UST + (Y_KES_PLAKA + 30.0 - H_UST) * ss(Z_KES_IN[0], Z_KES_IN[1], t)
    if t < Z_KES[1]: return Y_KES_PLAKA + 30.0 - 30.0 * lin(Z_KES[0], Z_KES[1], t)
    if t < Z_KES_UP[1]: return Y_KES_PLAKA + (H_UST - Y_KES_PLAKA) * ss(Z_KES_UP[0], Z_KES_UP[1], t)
    if t < Z_SPREY_IN[0]: return H_UST
    if t < Z_SPREY_IN[1]: return H_UST + (Y_SPREY_PLAKA - H_UST) * ss(Z_SPREY_IN[0], Z_SPREY_IN[1], t)
    if t < Z_SPREY_UP[0]: return Y_SPREY_PLAKA
    if t < Z_SPREY_UP[1]: return Y_SPREY_PLAKA + (H_UST - Y_SPREY_PLAKA) * ss(Z_SPREY_UP[0], Z_SPREY_UP[1], t)
    if t < Z_KAFA_HAZIR[0]: return H_UST
    if t < Z_KAFA_HAZIR[1]: return H_UST + (H_BEKLE - H_UST) * ss(Z_KAFA_HAZIR[0], Z_KAFA_HAZIR[1], t)
    if t < Z_KAPAT[0]: return H_BEKLE
    if t < Z_KAPAT[1]: return H_BEKLE + (KAPAK_BASKI - H_BEKLE) * ss(Z_KAPAT[0], Z_KAPAT[1], t)
    if t < Z_KAPAT[2]: return KAPAK_BASKI
    if t < Z_KAPAT[3]: return KAPAK_BASKI + (H_UST - KAPAK_BASKI) * ss(Z_KAPAT[2], Z_KAPAT[3], t)
    return H_UST


def bicak_dy(t):
    return -BICAK_STROK * (ss(Z_BICAK_AC[0], Z_BICAK_AC[1], t) - ss(Z_BICAK_KAPA[0], Z_BICAK_KAPA[1], t))


def sprey_olcek(t):
    return max(1e-4, ss(Z_SPREY[0], Z_SPREY[0] + 0.15, t) - ss(Z_SPREY[1] - 0.15, Z_SPREY[1], t))


def burun_oran(t):
    return ss(Z_BURUN_UZA[0], Z_BURUN_UZA[1], t) - ss(Z_BURUN_CEK[0], Z_BURUN_CEK[1], t)


def burun_x(t): return X_BURUN_GERI + (X_BURUN_ILERI - X_BURUN_GERI) * burun_oran(t)
def dansci_y(t): return Y_DANS_GERI + (Y_DANS_ILERI - Y_DANS_GERI) * burun_oran(t)
def itici_dz(t): return BESLE * (ss(Z_BESLE[0], Z_BESLE[1], t) - ss(Z_ITICI_DON[0], Z_ITICI_DON[1], t))


def kapak_alfa(t):
    if t < Z_KOL[1]: return 0.0
    if t < Z_KOL[2]: return 85.0 * ss(Z_KOL[1], Z_KOL[2], t)
    if t < Z_YATIR[0]: return 85.0
    if t < Z_YATIR[1]: return 85.0 + 15.0 * ss(Z_YATIR[0], Z_YATIR[1], t)
    if t < Z_KAPAT[1] + 0.05: return min(180.0, max(100.0, kapak_acisi_kafa(kafa_y(t))))
    return 180.0


def kol_beta(t):
    if t < Z_KOL[0]: return 0.0
    if t < Z_KOL[1]: return BETA_TEMAS * ss(Z_KOL[0], Z_KOL[1], t)
    if t < Z_YATIR[1]: return kol_icin_beta(kapak_alfa(t))
    return BETA_100 * (1.0 - ss(Z_KOL_DON[0], Z_KOL_DON[1], t))


def catal_trs(t):
    dz = -CATAL_DIS * ss(Z_CATAL[0], Z_CATAL[1], t) + 900.0 * ss(Z_CATAL[2], Z_CATAL[3], t)
    dy = 55.0 * ss(Z_CATAL[1], Z_CATAL[2], t)
    return (0.0, dy, dz)


def catal_kutu(t):
    if t < Z_CATAL[1]: return (0.0, 0.0)
    c = catal_trs(t); return (c[1], c[2] + CATAL_DIS)


def urun_trs(t):
    """pide merkezi (alt yüz): fırın bandından (x −300, −249) çitle −206'ya, bantta x 260'a; burun geri kaçınca kutuya iner"""
    x = PIDE0[0] + (XC - PIDE0[0]) * ss(Z_GELIS[0], Z_GELIS[1], t)
    z = PIDE0[2] + (ZB - PIDE0[2]) * ss(0.0, 150.0, x)
    y = 1166.0 if x < -4.0 else BANT
    y = y + (TEPSI + T - y) * ss(Z_DUS[0], Z_DUS[1], t)
    dy_c, dz_c = catal_kutu(t)
    return (x - PIDE0[0], y - PIDE0[1] + dy_c, z - PIDE0[2] + dz_c)


def blank_acilar(t):
    u = u_zimba(t)
    dz = -BESLE * (1.0 - ss(Z_BESLE[0], Z_BESLE[1], t))
    dy = -u
    dy_c, dz_c = catal_kutu(t); dy += dy_c; dz += dz_c
    th_s = 90.0 * ss(0.0, U_MAX, u)
    th_f = 90.0 * ss(8.0, U_MAX, u)
    th_bw = math.degrees(math.asin(min(u, H_ARKA - 0.001) / H_ARKA)) if u < H_ARKA else 90.0
    gam = kapak_alfa(t) - th_bw
    return (0.0, dy, dz), {"B_SWM": th_s, "B_SWP": -th_s, "B_FO": -th_f, "B_BW": th_bw, "B_LID": gam}


def gorunur(t):
    return 1e-4 if Z_GIZLE[0] <= t < Z_GIZLE[1] else 1.0


def quat(eksen, derece):
    a = math.radians(derece) / 2.0; s = math.sin(a)
    v = {"x": (s, 0.0, 0.0), "y": (0.0, s, 0.0), "z": (0.0, 0.0, s)}[eksen]
    return (v[0], v[1], v[2], math.cos(a))


# ================================================================ GLB ================================================================
def _ag(wp):
    import kiyma_cad_v6 as _K
    return _K.ag(wp, 0.4, 0.6)


PIVOT = {"KAFA": (XC, H_UST, ZC), "BICAK": (XC, H_UST, ZC), "SPREY": (XC, H_UST - 12.0, ZC), "PIDE": PIDE0, "KESIK": PIDE0,
         "BANT_UST": (X_PL0, 0.0, 0.0), "DANS_SERIT": (0.0, Y_TAIL_ALT, 0.0), "KOL": (KOL_P[0], KOL_P[1], 0.0)}
EBEVEYN = {"BICAK": "KAFA", "SPREY": "KAFA", "KESIK": "PIDE"}


def glb_yaz(yol, adim=1.0 / 15.0):
    GRUPLAR = ["SABIT", "ITICI", "KAFA", "BICAK", "SPREY", "PIDE", "KESIK", "BURUN", "BANT_UST", "DANSCI", "DANS_SERIT", "KOL", "CATAL"] + list(DUGUM.keys())
    mesh_g = {g: {} for g in GRUPLAR}
    for p in PARCALAR:
        mesh_g[p["grup"]].setdefault(p["mal"], Mesh()).ekle(_ag(p["wp"]))
    def pivot(g):
        if g in PIVOT: return PIVOT[g]
        if g in DUGUM: return DUGUM[g][1]
        return (0.0, 0.0, 0.0)
    def parent(g):
        if g in EBEVEYN: return EBEVEYN[g]
        if g in DUGUM: return DUGUM[g][0]
        return None
    nodes, idx = [], {}
    for g in GRUPLAR:
        P = pivot(g); par = parent(g); Pp = pivot(par) if par else (0.0, 0.0, 0.0)
        idx[g] = len(nodes); nodes.append({"name": g, "translation": [(P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM]})
    for g in GRUPLAR:
        if parent(g): nodes[idx[parent(g)]].setdefault("children", []).append(idx[g])
    kok = [idx[g] for g in GRUPLAR if not parent(g)]
    blob, views, accs, meshes, mats, mat_idx = [], [], [], [], [], {}
    off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    def mat(k):
        if k not in mat_idx:
            d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
            m_ = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": True}
            if d.get("saydam"): m_["alphaMode"] = "BLEND"
            mat_idx[k] = len(mats); mats.append(m_)
        return mat_idx[k]
    ucgen = 0
    for g in GRUPLAR:
        if not mesh_g[g]: continue
        P = pivot(g); prims = []
        for k, m in sorted(mesh_g[g].items()):
            pts = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]
            vp = gomu(struct.pack("<%df" % (3 * len(pts)), *[c for q in pts for c in q]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for q in m.N for c in q]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(q[i] for q in pts) for i in range(3)]; mx = [max(q[i] for q in pts) for i in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(pts), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": mat(k)})
            ucgen += len(m.I) // 3
        meshes.append({"name": g, "primitives": prims}); nodes[idx[g]]["mesh"] = len(meshes) - 1
    N = int(round(DONGU / adim)) + 1
    TT = [min(DONGU, i * adim) for i in range(N)]
    sm, ch = [], []
    def kanal(dugum, yol_, degerler, tip):
        ti = gomu(struct.pack("<%df" % len(TT), *TT))
        accs.append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        n = 4 if tip == "VEC4" else 3
        vo = gomu(struct.pack("<%df" % (n * len(degerler)), *[c for v in degerler for c in v]))
        accs.append({"bufferView": vo, "componentType": 5126, "count": len(degerler), "type": tip})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": idx[dugum], "path": yol_}})
    def trs(g, f):
        P = nodes[idx[g]]["translation"]
        kanal(g, "translation", [(P[0] + f(t)[0] * MM, P[1] + f(t)[1] * MM, P[2] + f(t)[2] * MM) for t in TT], "VEC3")
    trs("ITICI", lambda t: (0.0, 0.0, itici_dz(t)))
    trs("KAFA", lambda t: (0.0, kafa_y(t) - H_UST, 0.0))
    trs("BICAK", lambda t: (0.0, bicak_dy(t), 0.0))
    trs("PIDE", urun_trs)
    trs("BURUN", lambda t: (burun_x(t) - X_BURUN_GERI, 0.0, 0.0))
    trs("DANSCI", lambda t: (0.0, dansci_y(t) - Y_DANS_GERI, 0.0))
    trs("CATAL", catal_trs)
    trs("B_ROOT", lambda t: blank_acilar(t)[0])
    kanal("BANT_UST", "scale", [((burun_x(t) - X_PL0) / L0, 1.0, 1.0) for t in TT], "VEC3")
    kanal("DANS_SERIT", "scale", [(1.0, (Y_TAIL_ALT - dansci_y(t)) / (Y_TAIL_ALT - Y_DANS_GERI), 1.0) for t in TT], "VEC3")
    kanal("SPREY", "scale", [(sprey_olcek(t),) * 3 for t in TT], "VEC3")
    kanal("KESIK", "scale", [(max(1e-4, ss(Z_KES[1], Z_KES[1] + 0.05, t)),) * 3 for t in TT], "VEC3")
    kanal("KOL", "rotation", [quat("z", kol_beta(t)) for t in TT], "VEC4")
    for d_ in DUGUM:
        if DUGUM[d_][0]: kanal(d_, "rotation", [quat(DUGUM[d_][2], blank_acilar(t)[1][d_]) for t in TT], "VEC4")
    for g in ("B_ROOT", "PIDE"):
        kanal(g, "scale", [(gorunur(t),) * 3 for t in TT], "VEC3")
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kk_basit_v1"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
          "animations": [{"name": "kk_dongusu", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    print("GLB: %s · %d KB · %d dugum · %d ucgen · %d kanal · %d kare" % (os.path.basename(yol), (len(bb) + len(js)) // 1024, len(nodes), ucgen, len(ch), N))


ADIM = [
    (0.5, "Blank kalıba", "itici en üstteki düz kartonu şarjörden 411 mm öne, kalıbın üstüne sürer (E'nin bugünkü besleyicisi)"),
    (1.9, "Zımba", "kafa iner: taban 45,6 mm kalıba girer, yan duvarlar, ön duvar ve menteşe duvarı kalkar (E ile aynı; parmak ve 2. vuruş basit modelde yok)"),
    (4.2, "Burun uzar", "geri çekilen burunlu bant kutunun üstüne 342 mm uzar (bant altı 1150, kutu duvarı üstü 1133,6 → 16 mm pay); dansçı makara yukarı çıkar"),
    (5.2, "Ürün gelir", "pide fırın bandından (1166, eksen −249) 1164'teki banda geçer; 20° çit onu kutu eksenine (−206) alır; bant ürünü kesme merkezine (260 = kutu merkezi) getirir"),
    (6.0, "Kes", "bıçak yıldızı kafanın plakasından 46 mm çıkar, kafa iner, ağız bandın 0,5 mm üstünde durur (K'nin yöntemi); 6 dilim izi"),
    (8.6, "Burun geri, ürün kutuya", "burun 342 mm geri kaçarken bant aynı hızda ileri koşar: ürün x'te yerinde kalır, 72 mm aşağıdaki kutuya iner"),
    (9.9, "Sprey", "kafa kutunun üstüne iner (nozül pideden 150), PulsaJet 1,2 s tereyağı püskürtür; mist kutunun içinde kalır"),
    (11.8, "Kapak kalkar", "kol kapağı 85° kaldırır, sonra 100° yatırır (E ile aynı; flaplar basit modelde yok)"),
    (13.5, "Kapak kapanır", "kafa (bıçaklar içeride) kapağı kapatır ve bastırır"),
    (15.6, "Robot alır", "FR5 çatalı önden tepsi çubuklarının arasına girer, 55 mm kaldırır, kutuyu çeker"),
]


def kontrol():
    K = []
    K.append(("burun altı (bant sarımı) − kutu duvarı üstü", (Y_BURUN - R_BURUN - BANT_K) - (TEPSI + T + H_YAN), ">= 10"))
    K.append(("kafa plakası − geri çekilmiş burun arabası (x)", PK_X[0] - (X_BURUN_GERI + 10.0), ">= 10"))
    K.append(("bant üstü − fırın bandı", BANT - 1166.0, "= -2"))
    K.append(("ürün arka kenarı − bant arka kenarı (giriş, −249)", (PIDE0[2] - PZ_R) - BANT_Z[0], ">= 0"))
    K.append(("ürün ön kenarı − bant ön kenarı (kutu ekseni −206)", BANT_Z[1] - (ZB + PZ_R), ">= 0"))
    K.append(("bıçak ucu − kutu iç yarım genişliği (kesim bantta, kutu dışında)", 160.0 - T - BICAK_R1, ">= 0 (bilgi)"))
    K.append(("burun ileri ucu − kapak masası", 466.0 - (X_BURUN_ILERI + R_BURUN + 10.0), ">= 10"))
    K.append(("düşme yüksekliği (bant üstü − kutu tabanı üstü)", BANT - (TEPSI + T), "bilgi (E'de 46)"))
    K.append(("sprey nozül ucu − pide üstü", (Y_SPREY_PLAKA - 12.0) - (TEPSI + T + PZ_H), "= 150"))
    K.append(("kesimde kafa plakası altı − pide üstü", Y_KES_PLAKA - (BANT + PZ_H), ">= 20"))
    K.append(("dansçı stroku = burun stroku", (Y_DANS_ILERI - Y_DANS_GERI) - (X_BURUN_ILERI - X_BURUN_GERI), "= 0"))
    print("KONTROL (basit model):")
    for ad, v, hedef in K:
        print("   %-62s %8.1f   (%s)" % (ad, v, hedef))
    return [dict(ad=ad, deger=round(v, 1), hedef=hedef) for ad, v, hedef in K]


if __name__ == "__main__":
    t0 = time.time()
    govde(); sarjor_ve_itici(); kalip(); kafa(); bant(); urun_ve_catal(); blank()
    print("KK BASIT v1: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    kk = kontrol()
    out = os.path.join(KOK, "otonom", "hat3d")
    glb_yaz(os.path.join(out, "kk_basit_v1.glb"))
    J = dict(surum="kk_basit_v1", tarih="27 Eyl 2026", animasyon=dict(sure=DONGU, adim=[dict(t=t, ad=a, not_=n) for t, a, n in ADIM]),
             olcu=dict(istasyon=[W, H, D], hat_x=[4000, 4830], kutu_tabani=TEPSI, bant_ustu=BANT, burun_stroku=X_BURUN_ILERI - X_BURUN_GERI,
                       kutu_ekseni=ZB, urun_giris_ekseni=PIDE0[2], bicak_stroku=BICAK_STROK, dusme=BANT - (TEPSI + T)),
             kontrol=kk)
    with open(os.path.join(out, "kk_basit_v1.json"), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print("JSON yazildi · toplam %.0f sn" % (time.time() - t0)); sys.stdout.flush()
    os._exit(0)
