# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK · ANA HAT v1 — QR ana panosundan makineye güç + veri omurgası (bütün kablolar kapaklı kanalda; açıkta yalnız rakor ↔ klemens kısa uçları).
  ZEMİN: mevcut zemin kanalının GÜÇ bölmesi (x 4801–4838) QR altında 60 uzar (yeni taban rakoru z 1030) · ray + zincir oluğunun ALTINDAN makine önüne
         (z 100) iner · iki kol: DOLAP (x 4032–4072, makinenin altından teknik sütunun arka-sol köşesine) · E (x 5232–5292 dış dikey kanalın tabanına).
  DOLAP: taban sacından rakorla teknik sütunun arka hava odasına · dikey kanal 30 × 34 (arka-sol köşe, tava ve gider hattının arkasında) → pano altı kanalı.
  E DIŞ DİKEY KANAL 60 × 60 paslanmaz (E sağ yan yüzünde, şarjör kapısının önünde, z −40…+20) · 0 → 2160 · U_KE sağ yan sacından içeri.
  ÜST HAT: U_KE arkası 60 × 40 (y 2125–2165) → U_F arkası + TOPPING kuru bölmesi 60 × 22 (y 2143–2165: U_F tavan kirişleri 2168,5 altı · TOPPING panosu 2140 üstü)
         · inişler: E panosu (x 5100) · K panosu (x 4300) · TOPPING panosu (x 1950) — rakorlu.
  Kablo taşıma: kanal tabanı arka duvara / tabana vidalı konsollarla (her 600 mm), kanal içindeki kablolar çizilmez (pano imalatı standardı)."""
import math
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, boru, rakor

V = cq.Vector
T = 1.5                                                    # kanal sacı
ZK = dict(y=(-60.0, 0.0))                                  # zemin kanalı (gömülü, kapak zemin hizasında)
Z_ON_SERIT = (80.0, 120.0)                                 # makine önü zemin şeridi (makine +79 · ray ≥ 240)
DOLAP_KOL_X = (4032.0, 4072.0)
E_RISER = dict(x=(5232.0, 5292.0), z=(-40.0, 20.0), y=(0.0, 2160.0))
UST_KE = dict(y=(2125.0, 2165.0), z=(-826.0, -766.0))
UST_FT = dict(y=(2143.0, 2165.0), z=(-826.0, -766.0))
DOLAP_RIS = dict(x=(4032.0, 4062.0), z=(-826.0, -792.0))   # teknik sütun arka-sol köşe (tava −785 · gider −748 · boyuna şase −790'ın arkası)


def u_kanal_x(x0, x1, y0, y1, z0, z1, acik="+y"):
    """x boyunca U kanal (acik: kapak yönü '+y' | '-z' …) · döner (gövde, kapak)"""
    dis = kut(x0, x1, y0, y1, z0, z1)
    if acik == "+y": return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 + 1, z0 + T, z1 - T)), kut(x0, x1, y1, y1 + T, z0, z1)
    if acik == "-y": return dis.cut(kut(x0 - 1, x1 + 1, y0 - 1, y1 - T, z0 + T, z1 - T)), kut(x0, x1, y0 - T, y0, z0, z1)
    if acik == "+z": return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 - T, z0 + T, z1 + 1)), kut(x0, x1, y0, y1, z1, z1 + T)
    return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 - T, z0 - 1, z1 - T)), kut(x0, x1, y0, y1, z0 - T, z0)


def zemin_kanal(noktalar, gen=40.0):
    """zemin kanalı: xz düzleminde köşeli yol (her segment x ya da z) · 40 geniş · y −60…0 · döner (gövde, kapak) tek katı"""
    y0, y1 = ZK["y"]; h = gen / 2.0; gv, kp = None, None
    for (xa, za), (xb, zb) in zip(noktalar[:-1], noktalar[1:]):
        if abs(za - zb) < 1e-6:
            x0, x1 = min(xa, xb) - h, max(xa, xb) + h; z0, z1 = za - h, za + h
        else:
            z0, z1 = min(za, zb) - h, max(za, zb) + h; x0, x1 = xa - h, xa + h
        dis = kut(x0, x1, y0, y1 - T, z0, z1); ic = kut(x0 + T, x1 - T, y0 + T, y1, z0 + T, z1 - T)
        gv = dis if gv is None else gv.fuse(dis); kp = kut(x0, x1, y1 - T, y1, z0, z1) if kp is None else kp.fuse(kut(x0, x1, y1 - T, y1, z0, z1))
        gv = gv.cut(ic) if False else gv
    ic_top = None
    for (xa, za), (xb, zb) in zip(noktalar[:-1], noktalar[1:]):
        if abs(za - zb) < 1e-6: x0, x1 = min(xa, xb) - h + T, max(xa, xb) + h - T; z0, z1 = za - h + T, za + h - T
        else: z0, z1 = min(za, zb) - h + T, max(za, zb) + h - T; x0, x1 = xa - h + T, xa + h - T
        c = kut(x0, x1, y0 + T, y1, z0, z1); ic_top = c if ic_top is None else ic_top.fuse(c)
    return gv.cut(ic_top).clean(), kp.clean()


def kur(ekle, DELIKLER, DUSUR):
    B = "ELK_ANA_HAT"
    # ---------------- 1 · ZEMİN: QR altı uzantı + makine kolu (ray altından) + DOLAP / E kolları ----------------
    g, k = zemin_kanal([(4819.5, 1018.5), (4819.5, 1058.0)], gen=37.0)
    ekle("zemin_kanali_guc_uzatma_QR", g, "paslanmaz", B, bom=("Zemin kanalı uzantısı 304 1,5 (güç bölmesi, QR altı 60 mm)", 1, "gömme · kapak QR taban plakası", "yeni taban rakoru z 1030"))
    DELIKLER.append(("RE", "kanal_uc_qr", kut(4801.0, 4838.0, -58.5, -3.0, 997.0, 1001.0), "güç bölmesi QR altına uzar"))
    DELIKLER.append(("RE", "kanal_uc_hat", kut(4801.0, 4838.0, -58.5, -3.0, 489.0, 493.0), "güç bölmesi makineye iner"))
    yol = [(4819.5, 469.0), (4819.5, 100.0), (4052.0, 100.0), (4052.0, -826.0)]
    g, k = zemin_kanal(yol, gen=40.0)
    ekle("zemin_kanali_makine_kolu_dolap", g, "paslanmaz", B, bom=("Zemin kanalı 304 1,5 · 40 × 60 gömme (ray + zincir oluğu altından makine önüne, dolabın altına)", 1, "gömme, zemine ankraj",
                                                                "ray ve oluk üstünden geçer · makine ayakları arasında"))
    ekle("zemin_kanali_makine_kolu_dolap_kapak", k, "paslanmaz", B)
    g, k = zemin_kanal([(4819.5, 100.0), (5262.0, 100.0), (5262.0, -10.0)], gen=40.0)
    ekle("zemin_kanali_makine_kolu_E", g, "paslanmaz", B, bom=("Zemin kanalı 304 · 40 × 60 (E dış dikey kanalına)", 1, "", ""))
    ekle("zemin_kanali_makine_kolu_E_kapak", k, "paslanmaz", B)
    # ---------------- 2 · DOLAP: taban rakoru + arka-sol köşe dikey kanal + pano altı kanalı ----------------
    rx, rz = (DOLAP_RIS["x"][0] + DOLAP_RIS["x"][1]) / 2.0, (DOLAP_RIS["z"][0] + DOLAP_RIS["z"][1]) / 2.0
    rk, d_ = rakor((rx, 123.0, rz), "y", 9.0, 1.5, yon="-", disli=12.0)          # taban dış sacı 123–124,5
    ekle("dolap_taban_rakoru_M25", rk, "rakor", B, bom=("Taban rakoru M25 (güç 3G2,5 + Cat6A)", 1, "Lapp SKINTOP MS-M", "teknik sütun arka hava odası"))
    DELIKLER.append(("SC", "taban_dis_sac", d_, "dolap besleme rakoru"))
    ekle("dolap_zemin_cikis_kablosu", boru([(4052.0, -40.0, -809.0), (rx, -40.0, rz), (rx, 123.0, rz)], 7.0), "kablo", B)
    g = kut(DOLAP_RIS["x"][0], DOLAP_RIS["x"][1], 135.0, 415.0, DOLAP_RIS["z"][0], DOLAP_RIS["z"][1]).cut(
        kut(DOLAP_RIS["x"][0] + T, DOLAP_RIS["x"][1] - T, 134.0, 416.0, DOLAP_RIS["z"][0] + T, DOLAP_RIS["z"][1] + 1.0))
    ekle("dolap_dikey_kanal", g, "kanal", B, bom=("Dikey kablo kanalı PVC 30 × 34 (teknik sütun arka-sol köşe) + kapak", 1, "arka sacına perçin", ""))
    ekle("dolap_dikey_kanal_kapak", kut(DOLAP_RIS["x"][0], DOLAP_RIS["x"][1], 135.0, 415.0, DOLAP_RIS["z"][1], DOLAP_RIS["z"][1] + T), "kanal", B)
    g, k = u_kanal_x(DOLAP_RIS["x"][0], 4390.0, 415.0, 450.0, DOLAP_RIS["z"][0], DOLAP_RIS["z"][1], acik="+z")
    ekle("dolap_pano_alti_kanal", g, "kanal", B, bom=("Pano altı kablo kanalı PVC 35 × 34 (+ kapak) · teknik sütun", 1, "arka sacına perçin", "B panosu (PLC + röleler) klemensine kısa uçlar"))
    ekle("dolap_pano_alti_kanal_kapak", k, "kanal", B)
    for i, (xk, yk, zk) in enumerate(((4352.0, 625.0, -790.0), (4200.0, 470.0, -780.0))):
        ekle("dolap_pano_ucu_%d" % i, boru([(xk, 450.0, -800.0), (xk, 452.0 + 0.0, -800.0), (xk, yk, -800.0)], 3.5), "kablo", B)
    # ---------------- 3 · E DIŞ DİKEY KANAL (60 × 60 paslanmaz) + konsollar ----------------
    x0, x1 = E_RISER["x"]; z0, z1 = E_RISER["z"]; y0, y1 = E_RISER["y"]
    g = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + T, x1 - T, y0 - 1.0, y1 + 1.0, z0 + T, z1))
    ekle("E_dis_dikey_kablo_kanali", g, "paslanmaz", B, bom=("Dış dikey kablo kanalı 304 1,5 · 60 × 60 × 2160 + önden vidalı kapak", 1, "abkant",
                                                          "E sağ yan yüzüne 4 konsolla · zemin kanalından U_KE'ye · şarjör yan kapısının (z ≤ −414) önünde"))
    ekle("E_dis_dikey_kablo_kanali_kapak", kut(x0, x1, y0, y1, z1, z1 + T), "paslanmaz", B)
    for i, yk in enumerate((300.0, 900.0, 1500.0, 2050.0)):
        ekle("E_dis_kanal_konsolu_%d" % i, kut(5230.0, x0 + T, yk, yk + 40.0, z0 + 5.0, z1 - 5.0), "paslanmaz", B,
             bom=("Kanal konsolu 304 3 mm (E yan sacına 2 × M6 perçin somun)", 4, "", "") if i == 0 else None)
    # U_KE'ye giriş: yan sac kesiği + kanal dirseği (içeride)
    DELIKLER.append(("UD", "ust_ke_yan_sag", kut(5210.0, 5233.0, 2110.0, 2158.0, z0 + 3.0, z1 - 3.0), "dış dikey kanal girişi (kapak dahil)"))
    g, k = u_kanal_x(5140.0, x0 + T, 2112.0, 2158.0, z0 + 3.0, z1 - 3.0, acik="-y")
    ekle("U_KE_giris_kanali", g, "kanal", B); ekle("U_KE_giris_kanali_kapak", k, "kanal", B)
    # ---------------- 4 · ÜST HAT: U_KE (60 × 40) → U_F + TOPPING (60 × 22) ----------------
    # U_KE: girişten arkaya (sağ yan boyunca z −766'ya) + arka boyunca 4000'e
    ys0, ys1 = UST_KE["y"]; zs0, zs1 = UST_KE["z"]
    g = kut(5140.0, 5200.0, ys0, ys1, zs1, z0 + 3.0).cut(kut(5140.0 + T, 5200.0 - T, ys0 + T, ys1 + 1.0, zs1 - 1.0, z0 + 4.0))
    ekle("ust_hat_U_KE_yan", g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 40 + kapak (U_KE)", 1, "arka / yan saca konsollu", ""))
    ekle("ust_hat_U_KE_yan_kapak", kut(5140.0, 5200.0, ys1, ys1 + T, zs1, z0 + 3.0), "kanal", B)
    g, k = u_kanal_x(4016.0, 5200.0, ys0, ys1, zs0, zs1, acik="+y")
    ekle("ust_hat_U_KE_arka", g, "kanal", B); ekle("ust_hat_U_KE_arka_kapak", k, "kanal", B)
    for i, xk in enumerate((4200.0, 4700.0, 5100.0)):
        ekle("ust_hat_U_KE_konsol_%d" % i, kut(xk, xk + 30.0, ys0 - 3.0, ys1, -828.5, zs0), "paslanmaz", B,
             bom=("Kanal konsolu 304 (arka saca)", 3, "", "") if i == 0 else None)
    # U_F + TOPPING kuru bölme (60 × 22)
    yf0, yf1 = UST_FT["y"]
    for nm, (a, b) in (("U_F", (2516.0, 3984.0)), ("TOPPING", (1993.0, 2468.0))):
        g, k = u_kanal_x(a, b, yf0, yf1, zs0, zs1, acik="+y")
        ekle("ust_hat_%s" % nm, g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 22 + kapak (%s)" % nm, 1, "arka saca konsollu", "") if nm == "U_F" else None)
        ekle("ust_hat_%s_kapak" % nm, k, "kanal", B)
    for i, xk in enumerate((2700.0, 3300.0, 3800.0)):
        ekle("ust_hat_U_F_konsol_%d" % i, kut(xk, xk + 30.0, yf0 - 3.0, yf1, -828.5, zs0), "paslanmaz", B)
    ekle("ust_hat_TOPPING_konsol_0", kut(2200.0, 2230.0, yf0 - 3.0, yf1, -828.5, zs0), "paslanmaz", B)
    # duvar geçişleri (U_KE|U_F · U_F|TOPPING) — kanal geçiş parçası + sac kesikleri
    for nm, (xa, xb), mod, ad in (("KE_F", (3984.0, 4016.0), "UD", "ust_ke_yan_sol"), ("F_KE", (3984.0, 4016.0), "UD", "ust_f_yan_sag"),
                                  ("F_T", (2468.0, 2516.0), "UD", "ust_f_yan_sol"), ("T_F", (2468.0, 2516.0), "TC", "dis_yan_sag")):
        DELIKLER.append((mod, ad, kut(xa - 1.0, xb + 1.0, yf0 - 1.0, yf1 + 1.0, zs0 - 1.0, zs1 + 1.0), "üst hat geçişi"))
    for nm, (xa, xb) in (("KE_F", (3984.0, 4016.0)), ("F_T", (2468.0, 2516.0))):
        g = kut(xa, xb, yf0, yf1, zs0, zs1).cut(kut(xa - 1.0, xb + 1.0, yf0 + T, yf1 - T, zs0 + T, zs1 - T))
        ekle("ust_hat_gecis_%s" % nm, g, "kanal", B, bom=("Duvar geçiş kanalı + lastik çerçeve", 2, "", "") if nm == "KE_F" else None)
    # ---------------- 5 · İNİŞLER (rakorlu) ----------------
    # E panosu: U_KE arka kanalından (x 5100) aşağı → U_KE tabanı + E tavanı → E pano kanalı üstüne (y 1837)
    for nm, xd, yalt, zd, mods in (("E", 5100.0, 1840.0, -805.0, (("UD", "ust_ke_taban_sac"), ("KC", "ust_sac"))), ("K", 4300.0, 1830.0, -775.0, (("UD", "ust_ke_taban_sac"), ("KS", "ust_sac")))):
        g = kut(xd - 20.0, xd + 20.0, 1896.0, ys0, zd, zd + 30.0).cut(kut(xd - 20.0 + T, xd + 20.0 - T, 1895.0, ys0 + 1.0, zd + T, zd + 31.0))
        DELIKLER.append(("UD", "ust_ke_icecek_rafi", sil((xd, 1890.0, zd + 15.0), (xd, 1898.0, zd + 15.0), 9.0), "iniş %s kablo geçişi (lastik bilezik)" % nm))
        ekle("inis_%s_raf_bilezigi" % nm, sil((xd, 1895.0, zd + 15.0), (xd, 1897.0, zd + 15.0), 11.0).cut(sil((xd, 1894.0, zd + 15.0), (xd, 1898.0, zd + 15.0), 6.0)), "rakor", B)
        ekle("inis_%s_kanali" % nm, g, "kanal", B, bom=("İniş kanalı PVC 40 × 30 + kapak" if nm == "E" else None, 2, "", "") if nm == "E" else None)
        ekle("inis_%s_kanali_kapak" % nm, kut(xd - 20.0, xd + 20.0, 1896.0, ys0, zd + 30.0, zd + 30.0 + T), "kanal", B)
        rk_, d_ = rakor((xd, 1863.5, zd + 15.0), "y", 6.0, 3.0, yon="+", disli=12.0)
        ekle("inis_%s_rakoru" % nm, rk_, "rakor", B, bom=("Rakor M25 çift delikli conta (güç + veri) · U tabanı + istasyon tavanı", 3, "Lapp SKINTOP", "") if nm == "E" else None)
        for m_, a_ in mods:
            DELIKLER.append((m_, a_, d_, "iniş rakoru %s" % nm))
        ekle("inis_%s_besleme_demeti" % nm, boru([(xd, 1897.0, zd + 15.0), (xd, yalt, zd + 15.0)], 5.5), "kablo", B,
             bom=("İstasyon besleme demeti (3G2,5 H07RN-F + Cat6A S/FTP, spiral sargılı)" if nm == "E" else None, 3, "", "") if nm == "E" else None)
    # TOPPING panosu: kuru bölme kanalından pano kutusunun üstüne (y 2140) rakorla
    rk_, d_ = rakor((1950.0, 2140.0, zs0 + 30.0), "y", 6.0, 1.5, yon="+", disli=12.0)
    ekle("inis_TOPPING_rakoru", rk_, "rakor", B)
    DELIKLER.append(("TC", "kuru_pano_kutusu", d_, "TOPPING pano üst rakoru"))
    ekle("inis_TOPPING_kablolari", boru([(1993.0, yf0 + 11.0, zs0 + 30.0), (1950.0, yf0 + 11.0, zs0 + 30.0), (1950.0, 2140.0, zs0 + 30.0)], 5.5), "kablo", B)
