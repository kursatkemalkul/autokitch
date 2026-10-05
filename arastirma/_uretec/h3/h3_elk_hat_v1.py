# -*- coding: utf-8 -*-
"""HAT v3.7 · ELEKTRİK · ANA HAT v1 (Claude · YEREL) — U_F ana panosundan (h3_ana_pano_v1) istasyonlara güç + veri omurgası.
v3.4 (1 Eki): zemine gömme yok, makine dışında dikey kanal yok · zemin üstü kanal · ana besleme içeriden (teknik sütun → fırın altı → C kaidesi → TOPPING kuru bölmesi).
v3.6 (1 Eki): ana pano + beyin U_F'de · her istasyon Harting Han 10B fişiyle (TOPPING · DOLAP · K · E · A · F · QR · ROBOT) · alt etekler kalktı.
v3.7 (1–2 Eki · Kemal + koordinatör):
  · KANAL İÇİ KABLOLAR ÇİZİLDİ, GERÇEK ÇAPLA (ana_hat_kablolari): istasyon başına H07RN-F 3G2,5 Ø12,5 + ETHERLINE Cat.6A Ø8,7 (F: LiYCY 7 × 0,5 Ø7,6 + Cat6A) ·
    bina beslemesi H07RN-F 5G6 Ø19,9 · modem Cat6A. Her kanal kesitinde raf (shelf) yerleşimi, köşelerde eksene dik geçiş, kanal duvarından çıkışta delik.
  · KANALLAR DOLULUĞA GÖRE BÜYÜDÜ (≤ %50): U_F + TOPPING üst hattı 60 × 22 → 70 × 62 · gövde kanalı 26 × 40 → 26 × 128 · kuru bölme yükselişi 30 × 40 → 45 × 55 ·
    C kaidesi / teknik bölme yükselişi 30 × 140 · fırın altı 40 × 118 · teknik sütun yükselişi 40 × 58 · toplama kanalı 99 × 38,5 (iki kat: sütun sırasına göre).
  · ANA AYIRICI (EN 60204-1 5.3): bina bağlantı kutusu yerine kilitlenebilir muhafazalı yük ayırıcı 40 A 4P, QR'nin sağ (servis) yanında, kol 1,21 m ·
    bina 5G6 ayırıcıdan dikey kanalla zemin üstü kanala → ana hat → U_F ana panosu (iSW iç ayırıcı olarak kalır).
  · DOLAP Harting zeminden kalktı → teknik sütunun arka bölmesinde DOLAP istasyon kutusu (y 605–725, servis yüksekliği), soket önde.
  · Kablolar: kanal içinde P-kelepçe yok (kanal taşır) · kanal dışı uçlar ER.kelepceler."""
import math
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, boru, rakor

V = cq.Vector
T = 1.5                                                    # kanal sacı
# ---------------- kablo çapları (gerçek · föy) ----------------
R_FAN = 2.4                                                # ÖLFLEX CLASSIC 110 2 × 0,5 Ø4,8 (1119752) · U_F fanları 24 V
UF_TERMOSTAT = (3360.0, 2060.0)                            # STEGO KTS 011 üst yüzü (h3_ust_depo_v2 TERMOSTAT y 2030 ± 30)
UF_FANLAR = [("emis_0", 3711.5, 1981.5, 2040.0, "+"), ("emis_1", 3911.5, 1981.5, 2050.0, "+"), ("atis_0", 2691.5, 2126.5, 2040.0, "-"), ("atis_1", 2871.5, 2126.5, 2050.0, "-")]
R_G, R_D, R_DIO, R_B = 6.25, 4.35, 3.8, 9.95               # H07RN-F 3G2,5 Ø12,5 (Lapp 1600118) · Cat6A Ø8,7 (2170465) · LiYCY 7×0,5 Ø7,6 [VARSAYIM] · 5G6 Ø19,9 (16001313)
# ---------------- kanallar (dış ölçü) ----------------
UF = dict(y=(2105.0, 2166.5), z=(-826.0, -690.0))          # U_F + TOPPING-B üst hattı (kapak 2166,5–2168 · tavan kirişleri y ≥ 2168,5)
# v3.7b · U_F üst hattı 4 kesit (U_F içinde baca x 2920–3280 z ≥ −745,5 · atış fanları x 2577,5–2882,5 y ≤ 2137,5): (ad, x0, x1, y, z) dış
UFS = [("UF1", 3280.0, 3984.0, (2105.0, 2166.5), (-826.0, -690.0)), ("UF2", 2920.0, 3280.0, (2105.0, 2166.5), (-826.0, -748.0)),
       ("UF3", 2575.0, 2920.0, (2138.0, 2166.5), (-826.0, -656.0)), ("UF4", 1993.0, 2575.0, (2105.0, 2166.5), (-826.0, -690.0))]
TA = dict(x=(1250.0, 1993.0), y=(2143.0, 2165.0), z=(-826.0, -766.0))   # TOPPING-A → A (60 × 22, kuru pano üstü 2140,4)
UST_KE = dict(y=(2125.0, 2165.0), z=(-826.0, -766.0))      # U_KE arka 60 × 40 (aynı)
KE_GECIS = dict(y=(2143.0, 2165.0), z=(-826.0, -766.0))
TOPLAMA = dict(x=(3326.0, 3425.0), y=(2138.0, 2176.5), z=(-690.0, -125.0), y_arka=2103.5, z_kirik=-300.0)   # L kesit: ön (soket sütunları) y ≥ 2138 · arka y ≥ 2103,5
GV = dict(x=(2452.0, 2478.0), z=(-826.5, -701.5), y=(1255.0, 2105.0))        # gövde kanalı İÇ (TOPPING sağ cebi, arka)
FB = dict(x=(2422.5, 2478.0), y=(1255.0, 1320.0), z=(-826.5, -632.5))        # FRL üstü bağlantı İÇ
RU = dict(x=(2422.5, 2466.5), y=(1100.0, 1257.0), z=(-686.0, -632.5))        # kuru bölme yükselişi İÇ (soğuk arka sac −630,9)
RL = dict(x=(2422.5, 2449.5), y=(744.0, 1104.0), z=(-698.0, -560.0))   # dış 2451: TOPPING enerji zinciri demetinin P-kelepçesi bu duvara         # C kaidesi + teknik bölme yükselişi İÇ (TOPPING kabloları x ≥ 2453)
FA = dict(x=(2422.5, 4140.0), y=(744.0, 784.0), z=(-760.0, -642.0))          # fırın altı İÇ (ışınım sacı 741 · dolap tavanı 786 · taşıyıcı kiriş −640)
TS = dict(x=(4100.0, 4140.0), y=(124.0, 784.0), z=(-700.0, -642.0))          # teknik sütun yükselişi İÇ (tava ≤ −705 · PLC ≤ −744 · depo PU ≥ −469)
ZU_H = 50.0
ZU = [(5349.0, 5409.0, -195.0, 600.0),                     # koridor kör ucu → QR girişi başlığı
      (4040.0, 5409.0, -195.0, -135.0),                    # E + dolap ön ayak sırasının arkası
      (4040.0, 4150.0, -710.0, -135.0),                    # teknik sütun altı (ana yükseliş çıkışı)
      (5349.0, 5520.0, 540.0, 600.0),                      # v3.7 · bina: kör uç → QR sağ yanı
      (5460.0, 5520.0, 540.0, 990.0)]                      # v3.7 · QR sağ yanı boyunca → ayırıcı dikey kanalı
BV = dict(x=(5466.0, 5516.0), z=(925.0, 975.0), y=(51.5, 1120.0))           # ayırıcı → zemin kanalı dikey kanalı (dış)
AYIRICI = dict(x=(5431.0, 5546.0), y=(1120.0, 1300.0), z=(880.0, 1020.0))   # QR sağ yan sacına (5430,5) · kol +x yüzünde y 1210
# ---------------- istasyon girişleri ----------------
TOPPING_HARTING = (1993.0, 2040.0, -796.0)                 # kuru pano SAĞ yüzü (fiş +x) · L y boyunca
A_KUTU = dict(x=(1240.0, 1400.0), y=(1880.0, 2050.0), z=(-828.5, -728.5))
F_KUTU = dict(x=(2800.0, 2960.0), y=(830.0, 950.0), z=(-828.0, -728.0))
F_INIS = dict(x=2990.0, z=-672.0)
DAV_FAN_KLEMENS = (3460.0, 1490.0, -742.0)                 # FU sözleşmesi (Systemair RS 30-15 klemens kutusu, fan arka yüzü)
F_230V = dict(rakor_arka=(2770.0, 920.0), rakor_sol=(2800.0, 920.0, -790.0), rakor_sag=(2960.0, 900.0, -780.0), z_yol=-780.0)   # F kutusu bina 230 V girişi + davlumbaz fanı çıkışı
D_KUTU = dict(x=(4160.0, 4320.0), y=(605.0, 725.0), z=(-700.0, -610.0))     # v3.7 · DOLAP istasyon kutusu (teknik sütun arka bölmesi · servis yüksekliği 605–725)
D_HARTING = (4240.0, 665.0, -610.0)                        # kutunun ön yüzü (fiş +z)
DOLAP_RIS = dict(x=(4032.0, 4062.0), z=(-826.0, -792.0))


def u_kanal_x(x0, x1, y0, y1, z0, z1, acik="+y"):
    """x boyunca U kanal (acik: kapak yönü) · döner (gövde, kapak)"""
    dis = kut(x0, x1, y0, y1, z0, z1)
    if acik == "+y": return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 + 1, z0 + T, z1 - T)), kut(x0, x1, y1, y1 + T, z0, z1)
    if acik == "+z": return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 - T, z0 + T, z1 + 1)), kut(x0, x1, y0, y1, z1, z1 + T)
    return dis.cut(kut(x0 - 1, x1 + 1, y0 + T, y1 - T, z0 - 1, z1 - T)), kut(x0, x1, y0, y1, z0 - T, z0)


def zu_kanal(kutular, h=ZU_H):
    """ZEMİN ÜSTÜ kanal (y 0…h): kutular [(x0, x1, z0, z1)] birleşik · kapak h…h + T · döner (gövde, kapak)"""
    dis = ic = kp = None
    for x0, x1, z0, z1 in kutular:
        d = kut(x0, x1, 0.0, h, z0, z1); c = kut(x0 + T, x1 - T, T, h + 1.0, z0 + T, z1 - T); k = kut(x0, x1, h, h + T, z0, z1)
        dis = d if dis is None else dis.fuse(d); ic = c if ic is None else ic.fuse(c); kp = k if kp is None else kp.fuse(k)
    return dis.cut(ic).clean(), kp.clean()


def ici_bos(kutular, ici):
    dis = None
    for q in kutular:
        d = kut(*q); dis = d if dis is None else dis.fuse(d)
    for q in ici:
        dis = dis.cut(kut(*q))
    return dis.clean()


def rampa(x0, x1, z0, z1, h, yon):
    pts = [(x0, 0.0), (x0, h), (x1, 0.0)] if yon == "+x" else [(x0, 0.0), (x1, h), (x1, 0.0)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0)).val()


def _kutu(x, y, z, t=1.2):
    x0, x1 = x; y0, y1 = y; z0, z1 = z
    g = kut(x0, x1, y0, y1, z0, z1 - 2.0).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - 1.0))
    return g, kut(x0, x1, y0, y1, z1 - 2.0, z1)


KANAL_ADLARI = []                                          # kablo geçiş deliği açılabilecek (bu üretecin) kanal parçaları


def kur(ekle, DELIKLER, DUSUR):
    B = "ELK_ANA_HAT"

    def kanal_ekle(ad, sh, mal, birim, bom=None):
        ekle(ad, sh, mal, birim, bom); KANAL_ADLARI.append(ad)
    KANAL_ADLARI[:] = []
    # ---------------- 1 · ZEMİN ÜSTÜ KANAL ----------------
    g, k = zu_kanal(ZU)
    k = k.cut(kut(TS["x"][0], TS["x"][1], ZU_H - 1.0, ZU_H + 3.0, TS["z"][0], TS["z"][1]))                  # ana yükseliş çıkışı
    k = k.cut(kut(BV["x"][0] + T, BV["x"][1] - T, ZU_H - 1.0, ZU_H + 3.0, BV["z"][0] + T, BV["z"][1] - T))  # v3.7 · ayırıcı dikey kanalı
    kanal_ekle("zemin_ustu_kanal", g, "paslanmaz", B, bom=("Zemin üstü kablo kanalı 304 1,5 · 60 × 50 (koridor kör ucu · E / dolap ön ayaklarının arkası · QR sağ yanı) · zemine dübelli", 1,
                                                           "lazer + abkant", "gömme YOK · v3.7: içinde QR + ROBOT + modem + bina 5G6 (doluluk %27)"))
    kanal_ekle("zemin_ustu_kanal_kapak", k, "paslanmaz", B, bom=("Kanal kapağı 304 1,5 gözyaşı desenli (basılır)", 1, "", ""))
    for nm, (x0, x1, yon, zr1) in (("sol", (5319.0, 5349.0, "-x", 598.0)), ("sag", (5409.0, 5439.0, "+x", 538.0))):
        ekle("zemin_ustu_kanal_rampa_%s" % nm, rampa(x0, x1, 80.0, zr1, ZU_H + T, yon), "paslanmaz", B,
             bom=("Kanal rampası 304 (koridor kör ucu, 30 × 51,5)", 2, "", "") if nm == "sol" else None)
    x0, x1 = TS["x"]; z0, z1 = TS["z"]
    kanal_ekle("zemin_ustu_cikis_0", ici_bos([(x0 - T, x1 + T, ZU_H, 123.0, z0 - T, z1 + T)], [(x0, x1, ZU_H - 1.0, 124.0, z0, z1)]), "paslanmaz", B,
               bom=("Kanal çıkış kutusu 304 (kanal kapağından dolap tabanına · ana yükseliş)", 1, "", ""))
    kanal_ekle("zemin_ustu_kanal_QR_basligi", ici_bos([(5303.0, 5432.0, 0.0, 86.0, 600.0, 655.0)], [(5303.0 + T, 5432.0 - T, T, 86.0 - T, 600.0 + T, 656.0),
                                                                                                 (5349.0 + T, 5409.0 - T, T, ZU_H, 590.0, 602.0)]), "paslanmaz", B,
               bom=("Kanal başlığı 304 1,5 (QR alt panelindeki kablo giriş plakasını sarar · üst kapak vidalı)", 1, "lazer + abkant", "QR'ye 2 × M5"))
    # ---------------- 1b · v3.7 ANA AYIRICI (QR sağ yanı) + dikey kanal ----------------
    ax0, ax1 = AYIRICI["x"]; ay0, ay1 = AYIRICI["y"]; az0, az1 = AYIRICI["z"]
    kut_ = kut(ax0, ax1, ay0, ay1, az0, az1).cut(kut(ax0 + 2.0, ax1 - 2.0, ay0 + 2.0, ay1 - 2.0, az0 + 2.0, az1 - 2.0))
    rk_, d_ = rakor(((BV["x"][0] + BV["x"][1]) / 2.0, ay0, (BV["z"][0] + BV["z"][1]) / 2.0), "y", R_B + 0.3, 2.0, yon="-", disli=16.0)
    kut_ = kut_.cut(d_)
    rk2_, d2_ = rakor(((BV["x"][0] + BV["x"][1]) / 2.0, ay1, (BV["z"][0] + BV["z"][1]) / 2.0), "y", R_B + 0.3, 2.0, yon="+", disli=16.0)
    kut_ = kut_.cut(d2_)
    ekle("ana_ayirici_kutusu_IP65", kut_, "cihaz_koyu", B,
         bom=("ANA AYIRICI · muhafazalı yük ayırıcı 40 A 4P (AC-23A), kırmızı kol + sarı plaka, 3 asma kilitle AÇIK konumda kilitlenir · IP65", 1,
              "ör. ABB OT40F4 + muhafaza / Schneider TeSys Vario VCF + 4. kutup · kutu 115 × 180 × 140 [VARSAYIM: model + ölçü föyden teyit]",
              "v3.7 · EN 60204-1 5.3: kol 0,6–1,9 m → 1,21 m, kapaksız erişim · QR sağ (servis) yanında, robot alanının dışında · ana panodaki iSW iç ayırıcı"))
    ekle("ana_ayirici_rakoru_alt_M32", rk_, "rakor", B, bom=("Kablo rakoru M32 (ayırıcı ↔ bina / makine 5G6)", 2, "Lapp SKINTOP ST-M 32", ""))
    ekle("ana_ayirici_rakoru_ust_M32", rk2_, "rakor", B)
    hy = 1210.0; hz = (az0 + az1) / 2.0
    ekle("ana_ayirici_kol_plakasi_sari", kut(ax1, ax1 + 3.0, hy - 40.0, hy + 40.0, hz - 40.0, hz + 40.0), "ayirici_sari", B)
    ekle("ana_ayirici_kolu_kirmizi", cq.Solid.makeCylinder(18.0, 22.0, V(ax1 + 3.0, hy, hz), V(1, 0, 0)).fuse(kut(ax1 + 15.0, ax1 + 40.0, hy - 9.0, hy + 9.0, hz - 45.0, hz + 10.0)),
         "ayirici_kirmizi", B)
    g = kut(BV["x"][0], BV["x"][1], BV["y"][0], BV["y"][1], BV["z"][0], BV["z"][1]).cut(
        kut(BV["x"][0] + T, BV["x"][1] - T, BV["y"][0] - 1.0, BV["y"][1] + 1.0, BV["z"][0] + T, BV["z"][1] - T))
    kanal_ekle("ana_ayirici_dikey_kanal", g, "paslanmaz", B, bom=("Dikey kablo kanalı 304 1,5 · 50 × 50 (ayırıcı → zemin üstü kanal)", 1, "lazer + abkant", "QR sağ yan sacına 2 konsol"))
    for i, yk in enumerate((300.0, 900.0)):
        ekle("ana_ayirici_dikey_kanal_konsolu_%d" % i, kut(5430.5, BV["x"][0], yk, yk + 20.0, BV["z"][0] + 15.0, BV["z"][1] - 15.0), "paslanmaz", B)
    # ---------------- 2 · DOLAP: dikey kanal + pano altı kanalı (Secop kablosu + iç tesisat) ----------------
    g = kut(DOLAP_RIS["x"][0], DOLAP_RIS["x"][1], 135.0, 415.0, DOLAP_RIS["z"][0], DOLAP_RIS["z"][1]).cut(
        kut(DOLAP_RIS["x"][0] + T, DOLAP_RIS["x"][1] - T, 134.0, 416.0, DOLAP_RIS["z"][0] + T, DOLAP_RIS["z"][1] + 1.0))
    ekle("dolap_dikey_kanal", g, "kanal", B, bom=("Dikey kablo kanalı PVC 30 × 40 (teknik sütun arka-sol köşe) + kapak", 1, "Hager tehalit BA7A40030", ""))
    ekle("dolap_dikey_kanal_kapak", kut(DOLAP_RIS["x"][0], DOLAP_RIS["x"][1], 135.0, 415.0, DOLAP_RIS["z"][1], DOLAP_RIS["z"][1] + T), "kanal", B)
    g, k = u_kanal_x(DOLAP_RIS["x"][0], 4390.0, 415.0, 450.0, DOLAP_RIS["z"][0], DOLAP_RIS["z"][1], acik="+z")
    ekle("dolap_pano_alti_kanal", g, "kanal", B, bom=("Pano altı kablo kanalı PVC 40 × 40 (+ kapak) · teknik sütun", 1, "Hager tehalit BA7A40040", ""))
    ekle("dolap_pano_alti_kanal_kapak", k, "kanal", B)
    for i, (xk, yk) in enumerate(((4352.0, 625.0), (4200.0, 470.0))):
        ekle("dolap_pano_ucu_%d" % i, boru([(xk, 450.0, -800.0), (xk, yk, -800.0)], 3.5), "kablo", B)
    # ---------------- 3 · ANA BESLEME (v3.7 doluluğa göre): teknik sütun → fırın altı → C kaidesi / teknik bölme → kuru bölme → FRL üstü → gövde → üst hat ----------------
    I = [(TS["x"][0], TS["x"][1], 120.0, TS["y"][1], TS["z"][0], TS["z"][1]),
         (FA["x"][0], FA["x"][1], FA["y"][0], FA["y"][1], FA["z"][0], FA["z"][1]),
         (RL["x"][0], RL["x"][1], RL["y"][0], RL["y"][1], RL["z"][0], RL["z"][1]),
         (RU["x"][0], RU["x"][1], RU["y"][0], RU["y"][1], RU["z"][0], RU["z"][1]),
         (FB["x"][0], FB["x"][1], FB["y"][0], FB["y"][1], FB["z"][0], FB["z"][1]),
         (GV["x"][0], GV["x"][1], GV["y"][0], GV["y"][1] - T, GV["z"][0], GV["z"][1]),
         (GV["x"][0], GV["x"][1], GV["y"][1] - 10.0, GV["y"][1] + 2.0, UF["z"][0] + T, GV["z"][1]),          # üst hatta açılır (yalnız üst hat kesitinde)
         (F_INIS["x"] - 16.0, F_INIS["x"] + 16.0, FA["y"][1] - 1.0, FA["y"][1] + T + 1.0, F_INIS["z"] - 16.0, F_INIS["z"] + 16.0)]   # F çıkışı (kanal tavanı)
    D = [(TS["x"][0] - T, TS["x"][1] + T, 125.5, TS["y"][1] + T, TS["z"][0] - T, TS["z"][1] + T),
         (2421.0, FA["x"][1] + T, FA["y"][0] - T, FA["y"][1] + T, FA["z"][0] - T, FA["z"][1] + T),
         (2421.0, RL["x"][1] + T, RL["y"][0] - T, RL["y"][1] + T, RL["z"][0] - T, RL["z"][1] + T),
         (2421.0, RU["x"][1] + T, RU["y"][0] - T, RU["y"][1], RU["z"][0] - T, -631.0),
         (2421.0, FB["x"][1] + T, FB["y"][0] - T, FB["y"][1] + T, FB["z"][0] - T, -631.0),
         (GV["x"][0] - T, GV["x"][1] + T, GV["y"][0], GV["y"][1], GV["z"][0] - T, GV["z"][1] + T)]
    kanal_ekle("ana_besleme_kanali", ici_bos(D, I), "paslanmaz", B,
               bom=("Ana besleme kanalı 304 1,5 kapalı (v3.7 doluluğa göre: fırın altı 40 × 118 · yükseliş 30 × 140 / 45 × 55 · gövde 26 × 125 · teknik sütun 40 × 58), vidalı kapaklı", 1,
                    "lazer + abkant", "doluluk ≤ %50 · fırın altında kablolar silikon (Lapp ÖLFLEX HEAT 180 SiF) VARSAYIM: boşluk sıcaklığı ölçülecek"))
    ekle("ana_besleme_taban_cercevesi", ici_bos([(TS["x"][0] - 8.0, TS["x"][1] + 8.0, 125.0, 131.0, TS["z"][0] - 4.0, TS["z"][1] + 4.0)],
                                                [(TS["x"][0], TS["x"][1], 124.0, 132.0, TS["z"][0], TS["z"][1])]), "rakor", B,
         bom=("Kablo giriş çerçevesi bölmeli conta · dolap tabanı (ana yükseliş)", 1, "icotek KEL-DPZ 24 sınıfı", "VARSAYIM: çerçeve no. demet çaplarına göre"))
    zl, zh = min(RL["z"][0], FA["z"][0]) - T, max(RL["z"][1], FA["z"][1]) + T
    DELIKLER.append(("SC", "taban_dis_sac", kut(TS["x"][0], TS["x"][1], 120.0, 128.0, TS["z"][0], TS["z"][1]), "ana besleme dolap tabanı girişi"))
    for a_ in ("bolme_4_sac_a", "bolme_4_pu", "bolme_4_sac_b"):
        DELIKLER.append(("SC", a_, kut(3990.0, 4032.0, FA["y"][0] - T, FA["y"][1] + T, FA["z"][0] - T, FA["z"][1] + T), "ana besleme bölme 4 geçişi"))
    DELIKLER.append(("SC", "isi_kalkani_sol_sac", kut(2498.0, 2503.0, FA["y"][0] - T, FA["y"][1] + T, FA["z"][0] - T, FA["z"][1] + T), "ana besleme ısı kalkanı geçişi"))
    DELIKLER.append(("SC", "tavan_pu_T", kut(2421.0 - T, 2503.0, FA["y"][0] - T, 788.5, zl, zh), "ana besleme dolap tavan PU geçişi"))
    DELIKLER.append(("SC", "tavan_dis_sac", kut(2421.0 - T, RL["x"][1] + T, 785.0, 789.0, RL["z"][0] - T, RL["z"][1] + T), "ana besleme dolap tavanı → C kaidesi"))
    DELIKLER.append(("KD", "kaide_C_ust_plaka_4", kut(2421.0 - T, RL["x"][1] + T, 887.0, 893.0, RL["z"][0] - T, RL["z"][1] + T), "ana besleme C kaidesi üst plakası"))
    DELIKLER.append(("TC", "dis_taban", kut(2421.0 - T, RL["x"][1] + T, 891.0, 895.0, RL["z"][0] - T, RL["z"][1] + T), "ana besleme TOPPING tabanı"))
    # ---------------- 4 · ÜST HAT: U_KE (60 × 40) · U_F + TOPPING-B (70 × 62) · TOPPING-A (60 × 22) ----------------
    ys0, ys1 = UST_KE["y"]; zs0, zs1 = UST_KE["z"]
    g, k = u_kanal_x(4016.0, 5200.0, ys0, ys1, zs0, zs1, acik="+y")
    kanal_ekle("ust_hat_U_KE_arka", g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 40 + kapak (U_KE arkası)", 1, "Hager tehalit BA7A40060", "")); kanal_ekle("ust_hat_U_KE_arka_kapak", k, "kanal", B)
    for i, xk in enumerate((4200.0, 4700.0, 5100.0)):
        ekle("ust_hat_U_KE_konsol_%d" % i, kut(xk, xk + 30.0, ys0 - 3.0, ys1, -828.5, zs0), "paslanmaz", B, bom=("Kanal konsolu 304 (arka saca)", 9, "", "") if i == 0 else None)
    yf0, yf1 = UF["y"]; zf0, zf1 = UF["z"]
    ADLAR = {"UF1": "ust_hat_U_F", "UF2": "ust_hat_U_F_baca", "UF3": "ust_hat_U_F_fan", "UF4": "ust_hat_U_F_sol"}
    for nm, a, b, (y0_, y1_), (z0_, z1_) in UFS:
        parcalar = [(ADLAR[nm], a, b)] if nm != "UF4" else [("ust_hat_TOPPING", a, 2468.0), ("ust_hat_U_F_sol", 2516.0, b)]
        for ad_, a_, b_ in parcalar:
            g, k = u_kanal_x(a_, b_, y0_, y1_, z0_, z1_, acik="+y")
            if ad_ == "ust_hat_TOPPING": g = g.cut(kut(GV["x"][0], GV["x"][1], y0_ - 1.0, y0_ + T + 0.5, z0_ + T, GV["z"][1]))      # gövde kanalı aşağıdan girer
            if nm == "UF1": g = g.cut(kut(TOPLAMA["x"][0] + T, TOPLAMA["x"][1] - T, y0_ + T, y1_ + 1.0, z1_ - T - 1.0, z1_ + 1.0))   # toplama kanalı ağzı
            kanal_ekle(ad_, g, "kanal", B, bom=("Üst hat kablo kanalı PVC + kapak (U_F + TOPPING kuru bölmesi · v3.7b 4 kesit: 136 × 62 · baca yanı 78 × 62 · fan üstü 170 × 28,5)", 1,
                                                "OBO LKV / Hager LF sınıfı [VARSAYIM: kesitler katalogdan seçilecek]", "doluluk ≤ %50 (fan üstü %47)") if nm == "UF1" else None)
            kanal_ekle(ad_ + "_kapak", k, "kanal", B)
    for (n1, a1, b1, (ya1, yb1), (za1, zb1)), (n2, a2, b2, (ya2, yb2), (za2, zb2)) in zip(UFS[:-1], UFS[1:]):
        xg = a1                                                                   # kesit değişimi (x): büyük kesitin ucunu küçük kesitin içi dışında kapat
        lev = kut(xg - T / 2.0, xg + T / 2.0, min(ya1, ya2), max(yb1, yb2), min(za1, za2), max(zb1, zb2))
        lev = lev.cut(kut(xg - 2.0, xg + 2.0, max(ya1, ya2) + T, min(yb1, yb2) + 1.0, max(za1, za2) + T, min(zb1, zb2) - T))
        kanal_ekle("ust_hat_kesit_gecis_%s_%s" % (n1, n2), lev, "kanal", B)
    UF_ARALIK = {nm: (y0_, y1_, z0_, z1_) for nm, a, b, (y0_, y1_), (z0_, z1_) in UFS}
    g, k = u_kanal_x(TA["x"][0], TA["x"][1], TA["y"][0], TA["y"][1], TA["z"][0], TA["z"][1], acik="+y")
    kanal_ekle("ust_hat_TOPPING_A", g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 22 + kapak (TOPPING kuru pano üstü → A)", 1, "", "")); kanal_ekle("ust_hat_TOPPING_A_kapak", k, "kanal", B)
    for i, (xk, nm) in enumerate(((2720.0, "UF3"), (3300.0, "UF1"), (3800.0, "UF1"), (2200.0, "UF4"))):
        y0_ = UF_ARALIK[nm][0]
        ekle("ust_hat_U_F_konsol_%d" % i if i < 3 else "ust_hat_TOPPING_konsol_0", kut(xk, xk + 30.0, y0_ - 3.0, yf1, -828.5, zf0), "paslanmaz", B)
    ekle("ust_hat_TOPPING_konsol_1", kut(1700.0, 1730.0, 2140.5, TA["y"][1], -828.5, zf0), "paslanmaz", B)
    ekle("ust_hat_TOPPING_konsol_A", kut(1300.0, 1330.0, TA["y"][0] - 3.0, TA["y"][1], -828.5, zf0), "paslanmaz", B)
    for m_, a_, xa_, xb_ in (("TC", "dis_yan_sol", 1434.0, 1469.0), ("UD", "ust_a_yan_sag", 1418.0, 1437.5)):
        DELIKLER.append((m_, a_, kut(xa_, xb_, TA["y"][0] - 1.0, TA["y"][1] + T + 1.0, TA["z"][0] - 1.0, TA["z"][1] + 1.0), "üst hat TOPPING → A geçişi"))
    for mod, ad, (xa, xb), (ya, yb), (za, zb) in (("UD", "ust_ke_yan_sol", (3984.0, 4016.0), KE_GECIS["y"], KE_GECIS["z"]), ("UD", "ust_f_yan_sag", (3984.0, 4016.0), KE_GECIS["y"], KE_GECIS["z"]),
                                                  ("UD", "ust_f_yan_sol", (2468.0, 2516.0), (yf0, yf1 + T), UF["z"]), ("TC", "dis_yan_sag", (2468.0, 2516.0), (yf0, yf1 + T), UF["z"])):   # UF4 kesiti
        DELIKLER.append((mod, ad, kut(xa - 1.0, xb + 1.0, ya - 1.0, yb + 1.0, za - 1.0, zb + 1.0), "üst hat geçişi"))
    g = kut(3984.0, 4016.0, KE_GECIS["y"][0], KE_GECIS["y"][1], KE_GECIS["z"][0], KE_GECIS["z"][1]).cut(
        kut(3983.0, 4017.0, KE_GECIS["y"][0] + T, KE_GECIS["y"][1] - T, KE_GECIS["z"][0] + T, KE_GECIS["z"][1] - T))
    kanal_ekle("ust_hat_gecis_KE_F", g, "kanal", B, bom=("Duvar geçiş kanalı + lastik çerçeve", 2, "", ""))
    g = kut(2468.0, 2516.0, yf0, yf1 + T, zf0, zf1).cut(kut(2467.0, 2517.0, yf0 + T, yf1, zf0 + T, zf1 - T))
    kanal_ekle("ust_hat_gecis_F_T", g, "kanal", B)
    # toplama kanalı (ana pano solu)
    tx0, tx1 = TOPLAMA["x"]; ty0, ty1 = TOPLAMA["y"]; tz0, tz1 = TOPLAMA["z"]; ya_, zk_ = TOPLAMA["y_arka"], TOPLAMA["z_kirik"]
    gv = ici_bos([(tx0, tx1, ty0, ty1 - T, zk_, tz1), (tx0, tx1, ya_, ty1 - T, tz0, zk_)],
                 [(tx0 + T, tx1 - T, ty0 + T, ty1, zk_ - 1.0, tz1 - T), (tx0 + T, tx1 - T, ya_ + T, ty1, tz0 - 2.0, zk_ + 1.0)])
    kanal_ekle("ana_pano_toplama_kanali", gv, "paslanmaz", B,
               ("Ana pano toplama kanalı 304 1,5 · 99 × 38,5 (U_F tavanı altında, ana panonun solu → üst hatta) + kapak", 1, "lazer + abkant",
                "v3.7 · 12 istasyon kablosu + modem iki katta (sütun sırasına göre: arka sütun alt kat, ön sütun üst kat) + bina 5G6 · doluluk %43"))
    kanal_ekle("ana_pano_toplama_kanali_kapak", kut(tx0, tx1, ty1 - T, ty1, tz0, tz1), "paslanmaz", B)
    for i, zk in enumerate((-700.0, -420.0)):
        ekle("ana_pano_toplama_kanali_askisi_%d" % i, kut(tx0 - 2.0, tx0, ya_ if zk < zk_ else ty0, 2178.5, zk, zk + 25.0), "paslanmaz", B, ("Kanal askısı 304 2 mm (U_F tavanına)", 2, "", "") if i == 0 else None)
    # ---------------- 5 · İNİŞLER K / E (Harting) ----------------
    for nm, xd, mods in (("E", 5100.0, (("UD", "ust_ke_taban_sac"), ("KC", "ust_sac"))), ("K", 4300.0, (("UD", "ust_ke_taban_sac"), ("KS", "ust_sac")))):
        H = EO.harting((xd, 1863.9, -760.0), "+y", "x", t_duvar=3.8)
        for m_, a_ in mods:
            DELIKLER.append((m_, a_, H["kesik"], "%s Harting Han 10B soket kesiği" % nm))
        DELIKLER.append(("UD", "ust_ke_icecek_rafi", kut(xd - 45.0, xd + 45.0, 1890.0, 1898.0, -786.0, -734.0), "%s Harting fişi raf kesiği" % nm))
        ekle("harting_%s_soket" % nm, H["soket"], "rakor", B); ekle("harting_%s_fis" % nm, H["fis"], "rakor", B); ekle("harting_%s_rakoru_M32" % nm, H["rakor"], "rakor", B)
        yk = H["uc"][1] + 3.0
        g = kut(xd - 20.0, xd + 20.0, yk, ys0 + T, -826.0, -750.0).cut(kut(xd - 20.0 + T, xd + 20.0 - T, yk - 1.0, ys0 + T + 1.0, -824.5, -749.0))
        kanal_ekle("inis_%s_kanali" % nm, g, "kanal", B, bom=("İniş kanalı PVC 40 × 75 + kapak (üst hat → Harting fişi)", 2, "", "") if nm == "E" else None)
        kanal_ekle("inis_%s_kanali_kapak" % nm, kut(xd - 20.0, xd + 20.0, yk, ys0 + T, -750.0, -748.5), "kanal", B)
    # ---------------- 6 · TOPPING Harting (kuru pano sağ yüzü) ----------------
    H = EO.harting(TOPPING_HARTING, "+x", "y", t_duvar=1.5)
    DELIKLER.append(("TC", "kuru_pano_kutusu", H["kesik"], "TOPPING Harting Han 10B soket kesiği"))
    ekle("harting_TOPPING_soket", H["soket"], "rakor", B); ekle("harting_TOPPING_fis", H["fis"], "rakor", B); ekle("harting_TOPPING_rakoru_M32", H["rakor"], "rakor", B)


# ================================================================ v3.7 · ANA HAT KABLOLARI (kanal içinden, gerçek çap) ================================================================
EKS = "xyz"


class Kesit:
    """kanal parçası: ax boyunca · rng {eksen: (lo, hi)} iç sınırlar (iki dik eksen) · u/v: raf yerleşiminin satır / istif ekseni (v_ust: istif üstten)"""

    def __init__(s, ad, ax, rng, u, v, v_ust=False):
        s.ad, s.ax, s.rng, s.u, s.v, s.v_ust = ad, ax, rng, u, v, v_ust
        s.poz = {}

    def icerir(s, eksen, deger, r):
        lo, hi = s.rng[eksen]
        return lo + r - 0.01 <= deger <= hi - r + 0.01

    def yerlestir(s, kablolar, sabit=None, bosluk=1.0, sirali=False):
        """kablolar [(ad, r)] · raf: u boyunca sıra, dolunca v'de yeni raf (büyükten küçüğe) · sabit {ad: {eksen: değer}} elle"""
        if sabit:
            s.poz.update(sabit); kablolar = [k for k in kablolar if k[0] not in sabit]
        u0, u1 = s.rng[s.u]; v0, v1 = s.rng[s.v]
        sira = list(kablolar) if sirali else sorted(kablolar, key=lambda k: -k[1])
        cu, raf_v, raf_h = u0, (v1 if s.v_ust else v0), 0.0
        for ad, r in sira:
            if cu + 2 * r + bosluk > u1 + 1e-6:
                raf_v = raf_v - raf_h - bosluk if s.v_ust else raf_v + raf_h + bosluk; cu, raf_h = u0, 0.0
            pu = cu + bosluk + r; cu = pu + r
            raf_h = max(raf_h, 2 * r)
            pv = raf_v - r - 0.5 if s.v_ust else raf_v + r + 0.5
            if not (v0 + r - 0.01 <= pv <= v1 - r + 0.01):
                raise AssertionError("%s kesitine sığmadı: %s (v %.1f, sınır %s)" % (s.ad, ad, pv, (v0, v1)))
            s.poz[ad] = {s.u: pu, s.v: pv}
        return s.poz


def _nokta(ax, deger, capraz):
    p = [0.0, 0.0, 0.0]; p[EKS.index(ax)] = deger
    for e, d in capraz.items(): p[EKS.index(e)] = d
    return tuple(p)


def _dik(a, b, sira):
    """a → b eksen eksen (sira: eksen harfleri) · döner ara noktalar (b dahil)"""
    out, c = [], list(a)
    for e in sira + "".join(x for x in EKS if x not in sira):
        i = EKS.index(e)
        if abs(c[i] - b[i]) > 1e-6:
            c[i] = b[i]; out.append(tuple(c))
    return out


def hat_yolu(ad, r, bas, kesitler, son, sinir, jog_at, bas_sira="", son_sira="", delta=12.0):
    """bas: kanal dışı baş noktaları (son noktası 1. kesitin içinde) · kesitler [Kesit] · son: kanal dışı uç noktaları · sinir {(k1, k2): değer} aynı eksenli geçiş ·
    jog_at {(k1, k2): mutlak koordinat}: köşede üçüncü eksen kaydırması bu koordinatta (k2 ekseni boyunca) · döner nokta listesi"""
    pts = list(bas)
    S0 = kesitler[0]
    cap = [e for e in EKS if e != S0.ax]
    hedef = _nokta(S0.ax, pts[-1][EKS.index(S0.ax)], {e: S0.poz[ad][e] for e in cap})
    pts += _dik(pts[-1], hedef, bas_sira or "".join(cap))
    n = len(kesitler)
    for k in range(n - 1):
        A, Bk = kesitler[k], kesitler[k + 1]
        a, b = A.ax, Bk.ax
        pa, pb = A.poz[ad], Bk.poz[ad]
        prev = pts[-1]
        if a != b:
            c = [e for e in EKS if e not in (a, b)][0]
            P1 = dict(pa); P1[a] = pb[a]
            p1 = _nokta(b, pa[b], {a: pb[a], c: pa[c]})
            if abs(pa[c] - pb[c]) < 1e-6:
                pts.append(p1); continue
            # kesit k+1'in yönü: bir sonraki çıkış koordinatı
            if k + 2 < n:
                C = kesitler[k + 2]
                cik = C.poz[ad][b] if C.ax != b else sinir[(Bk.ad, C.ad)]
            else:
                cik = son[0][EKS.index(b)]
            yon = 1.0 if cik > pa[b] else -1.0
            if (A.ad, Bk.ad) in jog_at:
                je, jv = jog_at[(A.ad, Bk.ad)]
                if je == b:                                                       # köşeden sonra (k+1 içinde) jv'ye in, sonra c
                    q = list(p1); q[EKS.index(b)] = jv
                    pts += [p1, tuple(q)]; q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                else:                                                             # köşeden önce (k içinde) jv'de c, sonra köşe
                    q = list(p1); q[EKS.index(a)] = jv
                    pts.append(tuple(q)); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                    q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            elif Bk.icerir(c, pa[c], r):
                q = list(p1); q[EKS.index(b)] += yon * delta
                pts += [p1, tuple(q)]; q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            elif A.icerir(c, pb[c], r):
                ya = 1.0 if p1[EKS.index(a)] > prev[EKS.index(a)] else -1.0
                q = list(p1); q[EKS.index(a)] -= ya * delta
                pts.append(tuple(q)); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
                q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
            else:
                pts += [p1]; q = list(p1); q[EKS.index(c)] = pb[c]; pts.append(tuple(q))
        else:
            sb = sinir[(A.ad, Bk.ad)]
            yon = 1.0 if sb > prev[EKS.index(a)] else -1.0
            cur = {e: pa[e] for e in EKS if e != a}
            once = [e for e in cur if abs(pa[e] - pb[e]) > 1e-6 and A.icerir(e, pb[e], r)]
            sonra = [e for e in cur if abs(pa[e] - pb[e]) > 1e-6 and e not in once]
            pts.append(_nokta(a, sb - yon * delta, cur))
            for e in once:
                cur[e] = pb[e]; pts.append(_nokta(a, sb - yon * delta, cur))
            pts.append(_nokta(a, sb + yon * delta, cur))
            for e in sonra:
                cur[e] = pb[e]; pts.append(_nokta(a, sb + yon * delta, cur))
    SL = kesitler[-1]
    cap = [e for e in EKS if e != SL.ax]
    E = _nokta(SL.ax, son[0][EKS.index(SL.ax)], {e: SL.poz[ad][e] for e in cap})
    pts.append(E)
    pts += _dik(E, son[0], son_sira or "".join(cap))
    pts += list(son[1:])
    q = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q[-1]) > 0.05: q.append(p)
    return q


SIRALI = True


def ana_hat_kablolari():
    """döner [(ad, r, mal, nokta listesi, istasyon)] · bütün ana hat kabloları (ana pano soketi / rakoru → kanallar → istasyon Harting'i)"""
    import h3_ana_pano_v1 as AP
    SOK = {s[0]: s for s in AP.HARTING_SOKETLERI}
    GIR = {g[0]: g for g in AP.GIRIS_RAKORLARI}
    # ---- kesitler
    K = {}
    K["T"] = Kesit("T", "z", {"x": (TOPLAMA["x"][0] + T, TOPLAMA["x"][1] - T), "y": (TOPLAMA["y_arka"] + T, TOPLAMA["y"][1] - T)}, "x", "y")
    for nm, a, b, (y0_, y1_), (z0_, z1_) in UFS:
        K[nm] = Kesit(nm, "x", {"y": (y0_ + T, y1_), "z": (z0_ + T, z1_ - T)}, "z", "y")
    K["TA"] = Kesit("TA", "x", {"y": (TA["y"][0] + T, TA["y"][1]), "z": (TA["z"][0] + T, TA["z"][1] - T)}, "z", "y")
    K["KE"] = Kesit("KE", "x", {"y": (KE_GECIS["y"][0] + T, KE_GECIS["y"][1] - T), "z": (KE_GECIS["z"][0] + T, KE_GECIS["z"][1] - T)}, "z", "y")
    for nm, xd in (("IK", 4300.0), ("IE", 5100.0)):
        K[nm] = Kesit(nm, "y", {"x": (xd - 20.0 + T, xd + 20.0 - T), "z": (-824.5, -750.0)}, "x", "z")
    K["GV"] = Kesit("GV", "y", {"x": GV["x"], "z": GV["z"]}, "z", "x")
    K["FB"] = Kesit("FB", "z", {"x": FB["x"], "y": FB["y"]}, "x", "y")
    K["RU"] = Kesit("RU", "y", {"x": RU["x"], "z": RU["z"]}, "x", "z")
    K["RL"] = Kesit("RL", "y", {"x": RL["x"], "z": RL["z"]}, "z", "x")
    K["FA"] = Kesit("FA", "x", {"y": FA["y"], "z": FA["z"]}, "z", "y")
    K["TS"] = Kesit("TS", "y", {"x": TS["x"], "z": TS["z"]}, "z", "x")
    zy = (T, ZU_H)
    K["ZT"] = Kesit("ZT", "z", {"x": (4040.0 + T, 4150.0 - T), "y": zy}, "x", "y")
    K["ZF"] = Kesit("ZF", "x", {"z": (-195.0 + T, -135.0 - T), "y": zy}, "z", "y")
    K["ZK"] = Kesit("ZK", "z", {"x": (5349.0 + T, 5409.0 - T), "y": zy}, "x", "y")
    K["ZB1"] = Kesit("ZB1", "x", {"z": (540.0 + T, 600.0 - T), "y": zy}, "z", "y")
    K["ZB2"] = Kesit("ZB2", "z", {"x": (5460.0 + T, 5520.0 - T), "y": zy}, "x", "y")
    K["BV"] = Kesit("BV", "y", {"x": (BV["x"][0] + T, BV["x"][1] - T), "z": (BV["z"][0] + T, BV["z"][1] - T)}, "x", "z")
    SINIR = {("UF4", "TA"): 1993.0, ("UF1", "KE"): 3984.0, ("RU", "RL"): 1102.0, ("RL", "RU"): 1102.0,
             ("UF1", "UF2"): 3280.0, ("UF2", "UF3"): 2920.0, ("UF3", "UF4"): 2575.0, ("UF4", "UF3"): 2575.0, ("UF3", "UF2"): 2920.0, ("UF2", "UF1"): 3280.0}
    JOG = {("UF4", "GV"): ("y", 2088.0), ("GV", "UF4"): ("y", 2088.0), ("KE", "IK"): ("y", 2105.0), ("KE", "IE"): ("y", 2105.0),
           ("T", "UF1"): ("z", -670.0), ("UF1", "T"): ("z", -670.0)}
    # ---- kablolar (ad, r, mal)
    IST = ["TOPPING", "DOLAP", "K", "E", "ROBOT", "QR", "A", "F"]
    KAB = []
    for i_ in IST:
        KAB.append(("%s_guc" % i_, R_DIO if i_ == "F" else R_G, "kablo")); KAB.append(("%s_veri" % i_, R_D, "kablo_veri"))
    KAB += [("modem", R_D, "kablo_veri"), ("bina", R_B, "kablo"), ("fan24", R_FAN, "kablo")]
    RR = {a: r for a, r, m in KAB}
    ASAGI = ["DOLAP", "ROBOT", "QR", "F"]                                     # gövde kanalından aşağı inen istasyonlar
    YOL = {}
    UFA = ["UF1", "UF2", "UF3", "UF4"]
    for i_ in ("TOPPING",): YOL[i_] = ["T"] + UFA
    for i_ in ("K",): YOL[i_] = ["T", "UF1", "KE", "IK"]
    for i_ in ("E",): YOL[i_] = ["T", "UF1", "KE", "IE"]
    YOL["DOLAP"] = ["T"] + UFA + ["GV", "FB", "RU", "RL", "FA", "TS"]
    for i_ in ("ROBOT", "QR"): YOL[i_] = ["T"] + UFA + ["GV", "FB", "RU", "RL", "FA", "TS", "ZT", "ZF", "ZK"]
    YOL["A"] = UFA + ["TA"]
    YOL["F"] = UFA + ["GV", "FB", "RU", "RL", "FA"]
    rota = {}
    for i_ in IST:
        rota["%s_guc" % i_] = YOL[i_]; rota["%s_veri" % i_] = YOL[i_]
    rota["modem"] = YOL["QR"]
    rota["bina"] = ["BV", "ZB2", "ZB1", "ZK", "ZF", "ZT", "TS", "FA", "RL", "RU", "FB", "GV"] + UFA[::-1] + ["T"]
    rota["fan24"] = ["T", "UF1"]
    # ---- toplama kanalı elle (iki kat · sütun sırası) · alt kat: arka sütun (z −240) + modem · üst kat: ön sütun (z −140) + bina
    T_ = K["T"]; x_ = T_.rng["x"][0]; sab = {}
    for ad in ("ROBOT_guc", "ROBOT_veri", "K_guc", "K_veri", "TOPPING_guc", "TOPPING_veri", "modem", "fan24"):
        r = RR[ad]; x_ += 1.5 + r; sab[ad] = {"x": x_, "y": TOPLAMA["y"][0] + T + r + 0.5}; x_ += r
    x_ = T_.rng["x"][0]
    for ad in ("bina", "QR_guc", "QR_veri", "E_guc", "E_veri", "DOLAP_guc", "DOLAP_veri"):
        r = RR[ad]; x_ += 1.5 + r; sab[ad] = {"x": x_, "y": T_.rng["y"][1] - r - 0.5}; x_ += r
    assert x_ <= T_.rng["x"][1], ("toplama kanalı dar", x_)
    # ---- yerleşim
    SIRA = ["fan24", "bina", "QR_guc", "QR_veri", "ROBOT_guc", "ROBOT_veri", "modem", "DOLAP_guc", "DOLAP_veri", "F_guc", "F_veri", "A_guc", "A_veri",
            "TOPPING_guc", "TOPPING_veri", "K_guc", "K_veri", "E_guc", "E_veri"]
    for nm, kes in K.items():
        icinde = [(a, RR[a]) for a in SIRA if nm in rota[a]]
        try:
            kes.yerlestir(icinde, sabit=sab if nm == "T" else None, sirali=SIRALI)
        except AssertionError:
            kes.poz = {}; kes.yerlestir(icinde, sabit=sab if nm == "T" else None, sirali=False)
    # ---- baş / son noktaları
    out = []
    zb_ = TOPLAMA["y"][0]

    def soket_bas(ist, ad, o):
        s = SOK[ist]; xm, ys, zs, yon = s[1], s[2], s[3], s[4]
        if yon == "-x":
            gx = xm - 45.0 - 18.0                                                # fiş 45 + rakor 18 (EO.HAN10B)
            p = T_.poz[ad]
            return [(gx, ys + o, zs), (p["x"], ys + o, zs)], ""
        gz = zs - 45.0 - 18.0
        p = K["UF1"].poz[ad]
        return [(xm + o, ys, gz), (xm + o, ys, gz - 15.0), (xm + o, p["y"], gz - 15.0)], "z"
    for ad, r, mal in KAB:
        if ad == "bina":
            g = GIR["bina_besleme_5G6_M32"]
            bas = [((BV["x"][0] + BV["x"][1]) / 2.0, AYIRICI["y"][0] - 12.0, (BV["z"][0] + BV["z"][1]) / 2.0)]
            son = [(T_.poz[ad]["x"], T_.poz[ad]["y"], g[3]), (T_.poz[ad]["x"], g[2], g[3]), (g[1] - 12.0, g[2], g[3])]
            pts = hat_yolu(ad, r, bas, [K[n] for n in rota[ad]], son, SINIR, JOG, son_sira="")
            out.append((ad, r, mal, pts, "BINA")); continue
        if ad == "fan24":
            g = GIR["fan_24V_M20"]
            bas = [(g[1] - 12.0, g[2], g[3]), (T_.poz[ad]["x"], g[2], g[3])]
            son = [(UF_TERMOSTAT[0], 2140.0, -790.0), (UF_TERMOSTAT[0], UF_TERMOSTAT[1] + 0.1, -790.0)]
            pts = hat_yolu(ad, r, bas, [K[n] for n in rota[ad]], son, SINIR, JOG, son_sira="z")
            out.append((ad, r, mal, pts, "FAN")); continue
        if ad == "modem":
            g = GIR["modem_Cat6A_M20"]
            bas = [(g[1] - 12.0, g[2], g[3]), (T_.poz[ad]["x"], g[2], g[3])]
            ist = "QR"
        else:
            ist, tur = ad.rsplit("_", 1)
            o = -6.0 if tur == "guc" else 7.0
            bas, bsira = soket_bas(ist, ad, o)
        # son (istasyon tarafı)
        if ist in ("ROBOT", "QR") or ad == "modem":
            import h3_elk_qr_v1 as EQ
            bk = {"QR_guc": "guc_QR_3G2_5", "QR_veri": "veri_QR_Cat6A", "ROBOT_guc": "guc_ROBOT_3G2_5", "ROBOT_veri": "veri_ROBOT_Cat6A", "modem": "veri_MODEM_Cat6A"}[ad]
            bx, by = [(q[3], q[4]) for q in EQ.B_KABLOLAR if q[0] == bk][0]
            son = [(bx, by, 615.0), (bx, by, EQ.TEKME["z"][0] - EQ.UC_DIS)]; ss = "yx"
        elif ist == "TOPPING":
            xg = TOPPING_HARTING[0] + 28.0 + 45.0 + 18.0; zg = TOPPING_HARTING[2] + o
            son = [(2110.0, 2120.0, zg), (2110.0, TOPPING_HARTING[1], zg), (xg, TOPPING_HARTING[1], zg)]; ss = "zy"
        elif ist in ("K", "E"):
            xd = 4300.0 if ist == "K" else 5100.0; yg = 1863.9 + 28.0 + 45.0 + 18.0
            son = [(xd + o, yg + 25.0, -760.0), (xd + o, yg, -760.0)]; ss = "zx"
        elif ist == "A":
            xa = (A_KUTU["x"][0] + A_KUTU["x"][1]) / 2.0 - 30.0; za = (A_KUTU["z"][0] + A_KUTU["z"][1]) / 2.0; yg = A_KUTU["y"][1] + 91.0
            son = [(xa + o, TA["y"][0] + 9.0, za), (xa + o, yg, za)]; ss = "zy"
        elif ist == "F":
            xs = F_INIS["x"] + (-5.5 if tur == "guc" else 5.5); yd = 1055.0 if tur == "guc" else 1070.0
            xg = 2840.0 + (7.0 if tur == "guc" else -6.0); yg = F_KUTU["y"][1] + 91.0; zg = (F_KUTU["z"][0] + F_KUTU["z"][1]) / 2.0
            son = [(xs, 770.0, F_INIS["z"]), (xs, yd, F_INIS["z"]), (xs, yd, zg), (xg, yd, zg), (xg, yg, zg)]; ss = "zy"
        elif ist == "DOLAP":
            yc = D_HARTING[1] + o; zg = D_HARTING[2] + 28.0 + 45.0 + 18.0
            son = [(TS["x"][1] - 10.0, yc, -670.0), (4150.0, yc, -670.0), (4150.0, yc, -505.0), (D_HARTING[0], yc, -505.0), (D_HARTING[0], yc, zg)]; ss = "yz"
        pts = hat_yolu(ad, r, bas, [K[n] for n in rota[ad]], son, SINIR, JOG, bas_sira=(bsira if ad != "modem" else ""), son_sira=ss)
        out.append((ad, r, mal, pts, ist))
    return out, K


# ================================================================ İSTASYON KUTULARI + ANA HAT ÇİZİMİ ================================================================
def istasyon_kur(ekle, DELIKLER, DUSUR, ER, RAPOR, PARCALAR=None):
    B = "ELK_ISTASYON"

    def parca(ad, sh, mal, bom=None, birim=B):
        ekle(ad, sh, mal, birim, bom); ER.ekli_ekle(ad, sh)

    def kablo(ad, pts, r, mal="kablo", bom=None, haric=(), kelepce=True, birim=B, denetle=True):
        sh = boru(pts, r)
        if denetle:
            ok, engel = ER.temiz(sh, haric)
            if not ok:
                RAPOR["bulunamadi"].append((ad, pts[0], pts[-1], engel)); return None
        parca(ad, sh, mal, bom, birim)
        if kelepce:
            kl, aski = ER.kelepceler(pts, r, haric=haric)
            for j, (_p, ks) in enumerate(kl): parca("%s_kelepce_%d" % (ad, j), ks, "celik", None, birim)
            RAPOR["askida"] += [(ad,) + tuple(a) for a in aski]
        RAPOR["yol"].append((ad, round(EO.uzunluk(pts)), len(pts) - 1, 0))
        return sh

    def harting_ekle(ad, H, soket=True):
        if soket: parca("harting_%s_soket" % ad, H["soket"], "rakor")
        parca("harting_%s_fis" % ad, H["fis"], "rakor"); parca("harting_%s_rakoru_M32" % ad, H["rakor"], "rakor")

    def din_zarf(ad, x0, w, yc, h, zr, d, bom=None, mal="cihaz", eks="z"):
        if eks == "z": parca(ad, kut(x0, x0 + w, yc - h / 2.0, yc + h / 2.0, zr, zr + d), mal, bom)
        else: parca(ad, kut(x0, x0 + w, yc - h / 2.0, yc + h / 2.0, zr - d, zr), mal, bom)

    KB = ("İstasyon kutusu 304 1,5 · IP65 contalı kapak · 2 mm galvaniz plaka + TS35 ray", 3, "lazer + abkant + kaynak", "A · F · DOLAP (diğer istasyonlarda mevcut panolar kutu sayılır)")
    # ---------------- A ----------------
    g, k = _kutu(A_KUTU["x"], A_KUTU["y"], A_KUTU["z"])
    HA = EO.harting(((A_KUTU["x"][0] + A_KUTU["x"][1]) / 2.0 - 30.0, A_KUTU["y"][1], (A_KUTU["z"][0] + A_KUTU["z"][1]) / 2.0), "+y", "x", t_duvar=1.2)
    parca("A_istasyon_kutusu_160x170x100", g.cut(HA["kesik"]), "pano", KB)
    parca("onyuz_A_istasyon_kutusu_kapagi", k, "pano")
    zr = A_KUTU["z"][0] + 1.2
    parca("A_kutu_din_rayi", kut(A_KUTU["x"][0] + 8.0, A_KUTU["x"][1] - 8.0, 1932.5, 1967.5, zr, zr + 7.5), "din")
    din_zarf("A_sigorta_iC60N_1PN_C16", A_KUTU["x"][1] - 90.0, 36.0, 1950.0, 90.0, zr + 7.5, 75.0,
             bom=("A besleme: iC60N 1P+N C16 + 6 klemens (açıcının kendi kablosu buraya bağlanır, açıcı satın alınır)", 1, "ZARF [VARSAYIM]", "Kemal 1 Eki: açıcı çevresinde başka elektrik yok"))
    for i in range(6):
        din_zarf("A_klemens_%d" % i, A_KUTU["x"][1] - 50.0 + 5.2 * i, 5.2, 1950.0, 60.0, zr + 7.5, 45.0)
    harting_ekle("A", HA)
    # ---------------- F ----------------
    g, k = _kutu(F_KUTU["x"], F_KUTU["y"], F_KUTU["z"])
    HF = EO.harting((2840.0, F_KUTU["y"][1], (F_KUTU["z"][0] + F_KUTU["z"][1]) / 2.0), "+y", "x", t_duvar=1.2)
    rk_, d_ = rakor((F_KUTU["x"][0], 860.0, -800.0), "x", 3.0, 1.2, yon="-", disli=8.0); g = g.cut(d_)
    parca("F_kutu_rakoru_sinyal", rk_, "rakor", ("Kablo rakoru IP68 PA M16 + kontra somun (istasyon kutusu çıkışı)", 1, "Lapp SKINTOP ST-M", ""))
    parca("F_istasyon_kutusu_160x120x100", g.cut(HF["kesik"]).cut(rakor(F_230V["rakor_sol"], "x", 4.8, 1.2, yon="-", disli=9.0)[1]).cut(rakor(F_230V["rakor_sag"], "x", 4.3, 1.2, yon="+", disli=8.0)[1]),
          "pano", None)
    parca("onyuz_F_istasyon_kutusu_kapagi", k, "pano")
    zr = F_KUTU["z"][0] + 1.2
    parca("F_kutu_din_rayi", kut(F_KUTU["x"][0] + 8.0, F_KUTU["x"][1] - 8.0, 867.5, 902.5, zr, zr + 7.5), "din")
    for ad_, p_ in (("230V_bina", F_230V["rakor_sol"]),):
        rk_, d_ = rakor(p_, "x", 4.8, 1.2, yon="-", disli=9.0)
        parca("F_kutu_rakoru_%s" % ad_, rk_, "rakor", ("Kablo rakoru M20 (F kutusu: bina 230 V girişi · davlumbaz fanı çıkışı)", 2, "Lapp SKINTOP ST-M 20", "v3.7b"))
    rk2_, d2_ = rakor(F_230V["rakor_sag"], "x", 4.3, 1.2, yon="+", disli=8.0)
    parca("F_kutu_rakoru_davlumbaz_fani", rk2_, "rakor")
    din_zarf("F_sigorta_iC60N_1PN_C6", F_KUTU["x"][1] - 80.0, 18.0, 885.0, 90.0, zr + 7.5, 75.0,
             bom=("F kutusu: iC60N 1P+N C6 (24 V) + fırın sinyal röleleri + klemens · ana panoda DIO + Ethernet", 1, "ZARF [VARSAYIM]",
                  "fırın 400 V 32 A gücü BİNADAN kendi CEE devresiyle (bina tesisat bandı f_ust_rakor_cee_firin)"))
    din_zarf("F_sigorta_iC60N_1PN_C6_davlumbaz_fani", F_KUTU["x"][1] - 61.0, 18.0, 885.0, 90.0, zr + 7.5, 75.0,
             bom=("F kutusu: iC60N 1P+N C6 davlumbaz fanı (Systemair RS 30-15 sileo 230 V 51 W) · girişi bina 230 V (ayrı devre, arka sactan)", 1, "ZARF [VARSAYIM]",
                  "v3.7b · ana panoda yer yok · fırının CEE devresine bağlanmaz"))
    for i in range(6):
        din_zarf("F_klemens_%d" % i, F_KUTU["x"][1] - 40.0 + 5.2 * i, 5.2, 885.0, 60.0, zr + 7.5, 45.0)
    harting_ekle("F", HF)
    rk_, d_ = rakor((F_INIS["x"], 788.0, F_INIS["z"]), "y", 11.0, 1.5, yon="+", disli=15.0)
    parca("F_ana_hat_tavan_rakoru_M40", rk_, "rakor", ("Rakor M40 + 2 delikli conta (dolap tavanı → fırın altı ana besleme · F: LiYCY + Cat6A)", 1, "Lapp SKINTOP ST-M 40 + DIX-M", ""))
    DELIKLER.append(("SC", "tavan_dis_sac", d_, "F ana hattı dolap tavanı geçişi"))
    # v3.7b · bina 230 V (ayrı devre) → arka sac rakoru → F kutusu sol rakoru · F kutusu C6 → davlumbaz fanı klemensi (davlumbaz kutusunun altından rakorla)
    xr_, yr_ = F_230V["rakor_arka"]; xs_, ys_, zs_ = F_230V["rakor_sol"]
    rk_, d_ = rakor((xr_, yr_, -828.5), "z", 5.1, 1.5, yon="-", disli=9.0)
    parca("F_ust_arka_rakoru_230V_M20", rk_, "rakor", ("Kablo rakoru M20 (F üstü kabin arka sacı · bina 230 V)", 1, "Lapp SKINTOP ST-M 20", "v3.7b"))
    DELIKLER.append(("FU", "f_ust_arka_sac", d_, "v3.7b F kutusu bina 230 V girişi"))
    kablo("F_bina_230V_davlumbaz", [(xr_, yr_, -860.0), (xr_, yr_, zs_), (xs_ - 12.0, yr_, zs_)], 4.8, haric=("F_UST_KABIN|f_ust_arka_sac",), kelepce=False,
          bom=("Bina 230 V 16 A ayrı devre H07RN-F 3G1,5 (Lapp 1600103, Ø9,6) · bina tesisat bandı → F kutusu (davlumbaz fanı C6)", 1, "", "v3.7b · AÇIK: dükkân tesisatında ayrı sigorta"))
    xd_, yd_, zd_ = DAV_FAN_KLEMENS; xo_, yo_, zo_ = F_230V["rakor_sag"]
    rk_, d_ = rakor((xd_, 1315.0, zo_), "y", 4.3, 1.5, yon="-", disli=8.0)
    parca("F_davlumbaz_rakoru_M16", rk_, "rakor", ("Kablo rakoru M16 (davlumbaz kutusu tabanı · fan kablosu)", 1, "Lapp SKINTOP ST-M 16", "v3.7b"))
    DELIKLER.append(("FU", "f_davlumbaz_kutusu", d_, "v3.7b davlumbaz fanı kablosu"))
    kablo("F_davlumbaz_fani_kablosu", [(xo_ + 12.0, yo_, zo_), (xd_, yo_, zo_), (xd_, yd_, zo_), (xd_, yd_, zd_ - 0.1)], 4.0, haric=("F_DAVLUMBAZ|f_davlumbaz_kutusu",),
          bom=("Davlumbaz fanı kablosu ÖLFLEX CLASSIC 110 3G1,5 (1119303, Ø8,1) · F kutusu C6 → fan klemensi", 1, "", "v3.7b"))
    # v3.7b · U_F fanları: STEGO termostatından 4 × 4414 FL'ye (24 V, arka sac önünde P-kelepçeli)
    for nm_, xf_, yf_, yb_, yon_ in UF_FANLAR:
        xt_ = UF_TERMOSTAT[0] + (16.6 if yon_ == "+" else -16.6)
        kablo("UF_fan_%s_kablosu" % nm_, [(xt_, yb_, -790.0), (xf_, yb_, -790.0), (xf_, yf_, -790.0), (xf_, yf_, -793.4)], R_FAN,
              bom=("U_F fan kablosu ÖLFLEX CLASSIC 110 2 × 0,5 (termostat → fan)", 4, "", "v3.7b") if nm_ == "emis_0" else None)
    kablo("F_firin_sinyal", [(F_KUTU["x"][0] - 12.0, 860.0, -800.0), (2560.0, 860.0, -800.0), (2560.0, 860.0, -656.1)], 3.0,
          bom=("Fırın sinyal kablosu (çalışıyor / hazır / bant hızı) LiYCY 7 × 0,5", 1, "Lapp UNITRONIC LiYCY [VARSAYIM]", "TP10 sinyal kutusuna"))
    # ---------------- DOLAP (v3.7 · teknik sütun arka bölmesi, servis yüksekliği) ----------------
    x0, x1 = D_KUTU["x"]; y0, y1 = D_KUTU["y"]; z0, z1 = D_KUTU["z"]
    g = kut(x0, x1, y0, y1, z0 + 2.0, z1 - 2.0).cut(kut(x0 + 1.2, x1 - 1.2, y0 + 1.2, y1 - 1.2, z0 + 1.0, z1 - 3.2))
    HD = EO.harting(D_HARTING, "+z", "x", t_duvar=2.0)
    rk_, d_ = rakor((x1 - 25.0, y0, z0 + 40.0), "y", 4.3, 1.2, yon="-", disli=8.0)
    parca("DOLAP_istasyon_kutusu_160x120x90", g.cut(HD["kesik"]).cut(d_), "pano", KB)
    parca("onyuz_DOLAP_istasyon_kutusu_kapagi", kut(x0, x1, y0, y1, z0, z0 + 2.0), "pano")
    parca("DOLAP_istasyon_kutusu_kapak_on", kut(x0, x1, y0, y1, z1 - 2.0, z1).cut(HD["kesik"]), "pano")
    parca("DOLAP_kutu_rakoru_M20", rk_, "rakor", ("Kablo rakoru M20 (DOLAP kutusu → B panosu)", 1, "Lapp SKINTOP ST-M 20", ""))
    for i, yk in enumerate((y0 + 15.0, y1 - 35.0)):
        parca("DOLAP_kutu_konsolu_%d" % i, kut(TS["x"][1] + T, x0, yk, yk + 20.0, z0 + 20.0, z0 + 60.0), "paslanmaz",
              ("Kutu konsolu 304 2 mm (ana yükseliş kanalına)", 2, "", "v3.7") if i == 0 else None)
    zr = z0 + 2.0
    parca("DOLAP_kutu_din_rayi", kut(x0 + 8.0, x1 - 8.0, 647.5, 682.5, zr, zr + 7.5), "din")
    din_zarf("DOLAP_sigorta_iC60N_1PN_C16", x0 + 12.0, 36.0, 665.0, 90.0, zr + 7.5, 60.0,
             bom=("DOLAP kutusu: iC60N 1P+N C16 + 10 klemens (Harting → B panosu)", 1, "ZARF [VARSAYIM]",
                  "v3.7 · zeminden kalktı (yere yatarak erişim yoktu) · servis: depo çekmecesi + arka sac sökülerek (AÇIK)"))
    for i in range(10):
        din_zarf("DOLAP_klemens_%d" % i, x0 + 56.0 + 5.2 * i, 5.2, 665.0, 60.0, zr + 7.5, 45.0)
    harting_ekle("DOLAP", HD)
    # ---------------- ANA PANO tarafı: soketlere fiş + rakor ----------------
    import h3_ana_pano_v1 as AP
    if not AP.PARCALAR: AP.kur()
    for sk in AP.HARTING_SOKETLERI:
        ist, xm, ys, zs, yon = sk[:5]
        H = EO.harting((xm + 28.0, ys, zs), "-x", "y", kilit=False) if yon == "-x" else EO.harting((xm, ys, zs + 28.0), "-z", "y", kilit=False)   # kilit kolu ana pano soketinde
        parca("harting_ANA_PANO_%s_fis" % ist, H["fis"], "rakor"); parca("harting_ANA_PANO_%s_rakoru_M32" % ist, H["rakor"], "rakor")
    # ---------------- ANA HAT KABLOLARI (kanal içinden) ----------------
    KK, KES = ana_hat_kablolari()
    BOM_ = {"guc": ("Ana hat güç kablosu H07RN-F 3G2,5 (Lapp 1600118, Ø12,5) · ana pano C16 → istasyon Harting", 7, "", "v3.7 · uzunluk modelden"),
            "veri": ("Ana hat veri kablosu Lapp ETHERLINE Cat.6A (2170465, Ø8,7) · switch → istasyon Harting RJ45", 8, "", ""),
            "bina": ("Bina beslemesi H07RN-F 5G6 (Lapp 16001313, Ø19,9) · ayırıcı → zemin üstü kanal → ana hat → ana pano M32", 1, "", "v3.7"),
            "modem": ("Modem Cat6A (QR kilit kartı modemi → ana pano switch)", 1, "", ""),
            "F_guc": ("F kontrol kablosu LiYCY 7 × 0,5 (Ø7,6) · ana pano DIO → F kutusu", 1, "Lapp UNITRONIC LiYCY [VARSAYIM]", ""),
            "fan24": ("U_F fan hattı 24 V ÖLFLEX CLASSIC 110 2 × 0,5 (1119752, Ø4,8) · ana pano fan_24V_M20 → STEGO termostat → 4 × 4414 FL", 5, "", "v3.7b")}
    yeni = []
    for ad, r, mal, pts, ist in KK:
        tur = ad if ad in ("bina", "modem", "F_guc", "fan24") else ad.rsplit("_", 1)[1]
        bom = BOM_.get(tur) if ad in ("TOPPING_guc", "TOPPING_veri", "bina", "modem", "F_guc", "fan24") else None
        sh = boru(pts, r)
        yeni.append((ad, sh, pts, r))
        parca("ana_hat_%s" % ad, sh, mal, bom, "ELK_ANA_HAT")
        RAPOR["yol"].append(("ana_hat_" + ad, round(EO.uzunluk(pts)), len(pts) - 1, 0))
    # makine dökümüne + ana panoya karşı (delik açılan saclar hariç: DELIKLER)
    kes = set(a for m, a, k, n in DELIKLER) | set(a for m, a in DUSUR)
    PANO = [("ANA_PANO|" + p_["ad"], AP.dunya(p_)) for p_ in AP.PARCALAR] if AP.PARCALAR else []
    for ad, sh, pts, r in yeni:
        for ad2, v in EO.cakisma(sh):
            if ad2.split("|", 1)[1] in kes: continue
            RAPOR["bulunamadi"].append(("ana_hat_" + ad, pts[0], pts[-1], "%s %.1f mm³" % (ad2, v)))
        b1 = sh.BoundingBox()
        for ad2, s2 in PANO:
            b2 = s2.BoundingBox()
            if b1.xmin > b2.xmax or b2.xmin > b1.xmax or b1.ymin > b2.ymax or b2.ymin > b1.ymax or b1.zmin > b2.zmax or b2.zmin > b1.zmax: continue
            try: v = sh.intersect(s2).Volume()
            except Exception: v = -1.0
            if v > 0.5 or v < 0: RAPOR["bulunamadi"].append(("ana_hat_" + ad, pts[0], pts[-1], "%s %.1f mm³" % (ad2, v)))
        if ad.startswith("F_"):                                                   # F ucu fırın üstü kabinde boşta (≈ 270 mm) → P-kelepçe
            i0 = [i for i, p_ in enumerate(pts) if p_[1] > 790.0][0] - 1
            kl, aski = ER.kelepceler(pts[i0:], r)
            for j, (_p, ks) in enumerate(kl): parca("ana_hat_%s_kelepce_%d" % (ad, j), ks, "celik", None, "ELK_ANA_HAT")
            RAPOR["askida"] += [("ana_hat_" + ad,) + tuple(a) for a in aski]
    # kanal duvarlarına kablo geçiş delikleri (bu üretecin kanalları)
    if PARCALAR is not None:
        P = {p["ad"]: p for p in PARCALAR}
        delik_say = {}
        for kad in KANAL_ADLARI:
            p = P.get(kad)
            if p is None: continue
            s = p["wp"].val()
            b0 = s.BoundingBox()
            for ad, sh, pts, r in yeni:
                b1 = sh.BoundingBox()
                if b1.xmin > b0.xmax or b0.xmin > b1.xmax or b1.ymin > b0.ymax or b0.ymin > b1.ymax or b1.zmin > b0.zmax or b0.zmin > b1.zmax: continue
                try: v = s.intersect(sh).Volume()
                except Exception: v = 1.0
                if v > 0.5:
                    s = s.cut(boru(pts, r + 1.0)); delik_say.setdefault(kad, []).append(ad)
            p["wp"] = cq.Workplane(obj=s)
        for kad, l in sorted(delik_say.items()):
            print("   kablo geçiş deliği: %-34s ← %s" % (kad, ", ".join(sorted(set(l)))))
    # ---------------- iç kablolar: Harting soketi → istasyon panosu ----------------
    Y_INS = 1863.9 - 3.8 - EO.HAN10B["ins"][2]                                 # K / E soket iç modülünün alt yüzü
    kablo("K_harting_ic_kablo", [(4290.0, Y_INS - 0.3, -755.0), (4290.0, 1823.0, -755.0), (4290.0, 1823.0, -718.0), (4290.0, 1700.0, -718.0), (4148.0, 1700.0, -718.0),
                                 (4148.0, 1700.0, -775.0), (4148.0, 1682.6, -775.0)], R_G, birim="ELK_K",   # K giriş sigortası C10 üst yüzü
          bom=("İstasyon iç kablosu (Harting soketi → istasyon klemensi) H05VV-F 3G2,5 + Cat6A yama", 4, "", "v3.7 · K · E · DOLAP · (TOPPING / A / F / QR / ROBOT soket kutunun kendisinde)"))
    kablo("E_harting_ic_kablo", [(5090.0, Y_INS - 0.3, -770.0), (5090.0, 1817.0, -770.0), (5090.0, 1817.0, -796.9)], R_G, birim="ELK_ANA_HAT")
    kablo("DOLAP_harting_ic_kablo", [(x1 - 25.0, y0 - 12.1, z0 + 40.0), (x1 - 25.0, 580.0, z0 + 40.0), (4350.0, 580.0, z0 + 40.0), (4350.0, 652.0, z0 + 40.0), (4350.0, 652.0, -773.9)], 4.0,
          birim="ELK_DOLAP")
    return []


RK_BOM = ("Kablo rakoru IP68 PA M16 / M25 + kontra somun (istasyon kutusu çıkışı)", 2, "Lapp SKINTOP ST-M", "")
