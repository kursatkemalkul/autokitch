# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK · QR BÖLÜMÜ v1 — ana pano (40 yükseltilmiş, alttan rakorlu) · pano altı kablo tavası · orta dikey kanal · kilit kartı kanalı ·
alt bölme kanalı + yeni güç taban rakoru (robot kablosunun arkasında) · göz cihaz uç kabloları (orta kanala) · göz cihaz braketleri (havada düzeltmesi).
Bütün kablolar KANALDA; kanal dışındaki uçlar ≤ ~250 mm, cihaz / rakor arası. h3_elektrik_v1.kur() bunu çağırır (ekle / DELIKLER / DUSUR oradan).
v3.4 (1 Eki 2026 · Claude · YEREL) — Kemal: "ZEMİNİN ALTINA HİÇBİR ŞEY GÖMÜLMEZ (y < 0 parça yok) · kablolar zeminin üstünden, dolap ayaklarının arasından ·
QR'ye alttan YANDAN / ÖNDEN girer · hiçbir şey yükseltilmez". DEĞİŞENLER:
  · KALKTI: qr_alt_taban_kanali (+ kapak) · qr_guc_taban_rakoru_M40 (taban plakasından zemine iniş) · DELIK taban_plakasi_3 (M40). Eski taban geçişleri
    (qr_cad_v1 GECIS_ROBOT Ø40 + GECIS_GUC Ø30, z 975) üstten 304 kapama sacıyla kapandı.
  · TEKMELİK (plint) 304 1,5 · x 4571,5–5428,5 · y 20–81 · servis kapağı düzleminde (z 670–671,5), taban plakasına oturur, 2 yan kulakla yan saclara perçinli.
    Alt servis kapağı (qr_cad_v1 servis_kapagi_alt, DÜŞER) → kısaltılmış kapak y 84–446 (3 mm aralık) · yarık ızgara y 94–164'e çıktı (alan aynı) ·
    alt menteşe (servis_mentesesi_0 y 50–90, DÜŞER) → y 100–140.
  · GİRİŞ (a) robot kablosu x 5088 · icotek KEL 10|3 V2A (42212.200) bölünmüş çerçeve + KT 20 (41220, Ø20–21) + 2 × BTK kör (41251) → hazır konnektörlü
    kablo kesikten (65 × 36) geçer · dışı robot köprü kanalının (h3_ray_ek_v2) içinde.
  · GİRİŞ (b) makine omurgası x 5308–5428 · icotek KEL-DPZ 16|14 (43816): 4 × H07RN-F 3G2,5 (Lapp 1600118, Ø10,9–14 → 9–16,2 membran) +
    4 × Cat6A (Lapp ETHERLINE Cat.6A 2170465, Ø8,7 → 5–10,2 membran) · 1 + 5 yedek membran. Kablo uçları tekmeliğin 30 mm dışında (z 640) bırakıldı
    (dış zemin üstü kanal BAŞKA ÜRETEÇTE: h3_elk_hat_v1).
  · GİRİŞ (c) bina beslemesi H07RN-F 5G6 (Lapp 16001313, Ø17,5–22,2) KEL-DPZ'nin 16,2 membranına SIĞMAZ → sağ yan sacta, ön köşenin 55 mm gerisinde
    Lapp SKINTOP ST-M 32×1,5 (53111040) · ucu yan sacın 30 mm dışında.
  · İÇ YOL: alt dikey kanal (x 4983–5007) dibinde sağ duvar açıldı → taban kanalı (arka, kangalın arkasında z 1012–1048) → sağ köşe kanalı (x 5379–5427,
    kangal ile sağ yan sac arası) → giriş (b) toplama kutusu (tekmeliğin arkası, kangalın önü) · hepsi 304 1,5, 60 yüksek, üstten kapaklı.
v3.5 (1 Eki 2026 · Claude · YEREL) — ANA PANO CİHAZLARI ÜRETİCİ STEP'İ (Kemal: "motor koy deyince kutu modelleyip bırakıyorsun" → gerçek katalog parçası):
  iSW A9S65440 · iID A9R21440 · NDR-120-24 · RevPi Connect 4 PR100378 (WLAN'sız) · FL SWITCH 1008N 1085256 → h3/katalog_step_v1.py (yön + ray oluğu tablosu,
  görünmeyen iç katılar atılır, dış ölçü aynı) · raylar gerçek genişliklerle yeniden dizildi · iC60N 1P+N C16 (A9F79616) ZARF kaldı (katalog STEP'i bulunamadı)."""
import math
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, boru, kanal, rakor

V = cq.Vector
# ---------------- v3.4 · TEKMELİK + GİRİŞLER (tek kaynak · h3_ray_ek_v2 giriş (a) sabitlerini BURADAN okur) ----------------
TEKME = dict(x=(4571.5, 5428.5), y=(20.0, 81.0), z=(670.0, 671.5), kulak=20.0)     # tekmelik sacı (taban plakası üstü 20 · kapak altı 84)
KAPI_Y = (84.0, 446.0)                                 # kısaltılmış alt servis kapağı (qr_cad_v1: 21–446)
QR_DUSUR = ["servis_kapagi_alt", "servis_mentesesi_0"]  # qr_cad_v1 parçaları (yerine kısa kapak + y 100 menteşe)
# (a) robot kablosu · icotek KEL 10|3: 98 × 58 × 17 (dışta), kesik 65 × 36 · pencere 62,5 × 42: KT 20 (41,5 × 42) solda + 2 × BTK (21 × 21) üst üste sağda
GIRIS_A = dict(x=5088.0, y=50.0, L=98.0, W=58.0, H=17.0, kesik=(65.0, 36.0), pencere=(62.5, 42.0), kt=41.5, r_delik=10.05)
GIRIS_A["xc"] = GIRIS_A["x"] - GIRIS_A["kt"] / 2.0 + GIRIS_A["pencere"][0] / 2.0          # çerçeve merkezi 5098,5
# (b) makine omurgası · icotek KEL-DPZ 16|14: 120 × 58 × 14 (dışta), kesik 86 × 36 · membran yerleşimi VARSAYIM (güç sağda: köşe kanalına düz)
GIRIS_B = dict(x=(5308.0, 5428.0), y=(21.0, 79.0), H=14.0, kesik=(86.0, 36.0))
B_KABLOLAR = [("guc_TOPPING_3G2_5", 6.0, "kablo", 5386.0, 59.0), ("guc_DOLAP_3G2_5", 6.0, "kablo", 5402.0, 59.0),
              ("guc_K_3G2_5", 6.0, "kablo", 5386.0, 41.0), ("guc_E_3G2_5", 6.0, "kablo", 5402.0, 41.0),
              ("veri_TOPPING_Cat6A", 4.35, "kablo_veri", 5354.0, 59.0), ("veri_DOLAP_Cat6A", 4.35, "kablo_veri", 5370.0, 59.0),
              ("veri_K_Cat6A", 4.35, "kablo_veri", 5354.0, 41.0), ("veri_E_Cat6A", 4.35, "kablo_veri", 5370.0, 41.0)]
UC_DIS = 30.0                                          # kablo uçları tekmelik dış yüzünün bu kadar dışında biter (dış kanal arayüzü)
# (c) bina beslemesi 5G6 · sağ yan sac (dış yüz x 5430) · SKINTOP ST-M 32
GIRIS_C = dict(x=5430.0, y=50.0, z=725.0, r=9.95, disli=16.0)
# iç omurga kanalı (304 1,5 · y 20–80 + kapak 80–81,5): ön toplama kutusu · sağ köşe · arka taban
KANAL_B = dict(on=(5322.0, 5427.0, 671.5, 712.0), kose=(5379.0, 5427.0, 710.5, 1048.0), arka=(5007.0, 5427.0, 1012.0, 1048.0), y=(20.0, 80.0), t=1.5)
AP = dict(x=(4595.0, 4995.0), y=(1696.0, 2046.0), z=(675.0, 925.0), t=1.2)   # v3.2 · 38 yükseltildi (altında 43 mm kablo boşluğu)
PL_Z = (895.0, 898.0)
RAY_Z = (887.5, 895.0)
RAY_A_Y, RAY_B_Y = 1993.0, 1828.0
QK = dict(x=(4983.0, 5007.0), z=(930.0, 1080.0))       # orta dikey kanal (göz sütunları arası 4980–5010)
TAVA = dict(x=(4790.0, 5003.0), y=(1655.0, 1690.0), z=(760.0, 1080.0))   # pano altı kablo tavası (üst rafta)
UKN = dict(x=(5003.0, 5390.0), y=(1656.0, 1686.0), z=(995.0, 1035.0))    # kilit kartı kanalı
ALT = dict(x=(4983.0, 5007.0), z=(1000.0, 1080.0))     # alt bölme dikey kanal (kontrol kutusunun arkasında, z > 943)
# v3.4: TABAN_KN + GUC_RAKOR (M40 taban rakoru → zemin kanalı) KALKTI — yerine KANAL_B + GIRIS_B / GIRIS_C (yukarıda)
KABLOLAR = [("bina_besleme_5G6", 9.5, "kablo"), ("guc_TOPPING_3G2_5", 5.5, "kablo"), ("guc_DOLAP_3G2_5", 5.5, "kablo"), ("guc_K_3G2_5", 5.5, "kablo"),
            ("guc_E_3G2_5", 5.5, "kablo"), ("veri_TOPPING_Cat6A", 3.75, "kablo_veri"), ("veri_DOLAP_Cat6A", 3.75, "kablo_veri"), ("veri_K_Cat6A", 3.75, "kablo_veri"),
            ("veri_E_Cat6A", 3.75, "kablo_veri"), ("guc_ROBOT_3G2_5", 5.5, "kablo"), ("veri_ROBOT_Cat6A", 3.75, "kablo_veri"), ("guc_QR_24V", 4.0, "kablo"),
            ("veri_QR_Cat6A", 3.75, "kablo_veri"), ("veri_MODEM_Cat6A", 3.75, "kablo_veri"), ("ups_giris_3G1_5", 4.5, "kablo"), ("ups_cikis_3G1_5", 4.5, "kablo")]


def kur(ekle, DELIKLER, DUSUR, QR):
    """QR: qr_cad_v1 modülü (kur() yapılmış, parçalar dünya) · ekle(ad, sh, mal, birim, bom)"""
    P = {p["ad"]: QR.dunya(p) if hasattr(QR, "dunya") else p["wp"].val() for p in QR.PARCALAR}
    B1, B2, B3 = "ELK_ANA_PANO", "ELK_QR_KABLO", "ELK_QR_MONTAJ"
    x0, x1 = AP["x"]; y0, y1 = AP["y"]; z0, z1 = AP["z"]; t = AP["t"]
    # ---------------- 1 · ANA PANO (yükseltilmiş) ----------------
    DUSUR += [("QR", "ana_pano_400x350x250"), ("QR", "ana_pano_ayak_rayi_0"), ("QR", "ana_pano_ayak_rayi_1")]
    DUSUR += [("QR", a_) for a_ in QR_DUSUR]                                       # v3.4 · alt servis kapağı + alt menteşesi (tekmelik geldi)
    for i, (ax0, ax1) in enumerate(((4610.0, 4640.0), (4700.0, 4730.0))):
        ekle("pano_ayagi_%d" % i, kut(ax0, ax1, 1653.0, y0, 700.0, 900.0).cut(kut(ax0 + 2, ax1 - 2, 1652.0, y0 + 1.0, 702.0, 898.0)), "celik", B1,
             bom=("Pano ayağı 304 kutu profil 30 × 43 × 2 (pano 38 yükseldi: altında kablo tavası)", 2, "üst rafa + panoya M6", "v3.2") if i == 0 else None)
    RK = []
    for r_, (rx, rz) in enumerate([(4800.0 + 26.0 * i, zz) for zz in (805.0, 845.0, 885.0) for i in range(6)][:len(KABLOLAR)]):
        RK.append((rx, rz))
    govde = kut(x0, x1, y0, y1, z0 + 2.0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 + 1.0, z1 - t))
    for i, ((rx, rz), (ad, r, m)) in enumerate(zip(RK, KABLOLAR)):
        rk, d_ = rakor((rx, y0, rz), "y", r, t, yon="-", disli=8.0 if r < 6.0 else 11.0)
        govde = govde.cut(d_)
        ekle("pano_rakoru_%02d" % i, rk, "rakor", B1, bom=("Kablo rakoru PA IP68 M16 / M20 / M25 + somun (Lapp SKINTOP ST-M)", len(RK), "", "alt plaka") if i == 0 else None)
    ekle("pano_ana_govde_400x350x250", govde, "pano", B1,
         bom=("Duvar tipi pano 400 × 350 × 250 RAL 7035 IP66", 1, "Rittal AX sınıfı · ölçü proje sabiti (qr_cad_v1)", "QR üst bölmesi robot tarafı · v3.2: 38 yükseltildi · alt plakada %d rakor" % len(RK)))
    ekle("onyuz_ana_pano_kapagi", kut(x0, x1, y0, y1, z0, z0 + 2.0), "on_seffaf", B1, bom=("Pano kapağı (kilitli)", 1, "gövdeyle", ""))
    ekle("pano_montaj_plakasi", kut(x0 + 10.0, x1 - 10.0, y0 + 10.0, y1 - 10.0, PL_Z[0], PL_Z[1]), "din", B1, bom=("Montaj plakası galvaniz 2 mm", 1, "", ""))
    for i_, (px, py) in enumerate(((x0 + 20, y0 + 20), (x1 - 20, y0 + 20), (x0 + 20, y1 - 20), (x1 - 20, y1 - 20))):
        ekle("pano_plaka_burcu_%d" % i_, sil((px, py, PL_Z[1]), (px, py, z1 - t), 6.0), "celik", B1)
    for nm, yc in (("A", RAY_A_Y), ("B", RAY_B_Y)):
        ekle("din_rayi_%s" % nm, kut(x0 + 12.0, x1 - 12.0, yc - 17.5, yc + 17.5, RAY_Z[0], RAY_Z[1]), "din", B1, bom=("DIN rayı TS35 × 7,5", 2, "", "") if nm == "A" else None)

    def din(ad, xa, w, h, d, yc, mal="cihaz", bom=None):
        ekle(ad, kut(xa, xa + w, yc - h / 2.0, yc + h / 2.0, RAY_Z[0] - d, RAY_Z[0]), mal, B1, bom)
    # v3.5 (1 Eki · Claude · YEREL) · ÜRETİCİ STEP'LERİ: 5 cihaz kutu değil gerçek katı (h3/katalog_step_v1.py · önbellek h3/_katalog_cache) ·
    #   cihazın ray oluğu rayın önüne (RAY_Z[0] 887,5) ve ortasına oturur · sol kenar = verilen x · raylar GERÇEK genişlikle yeniden dizildi (adlar aynı)
    #   dizilim (gerçek genişlik): ray A  iSW 4612,0–4682,8 · iID 4683,8–4755,5 · 6 × iC60N 4756,5–4972,5 (ray 4607–4983)
    #                              ray B  NDR 4612,0–4652,0 · RevPi 4658,0–4703,0 · switch 4709,0–4731,5 · 16 klemens 4739,5–4822,7
    import katalog_step_v1 as KS

    def din_step(ad, kod, xa, yc, mal="cihaz", bom=None):
        """üretici STEP'i (KS.cihaz_step: önü −z, kapağa bakar) · döner: cihazın sağ kenarı (xa + gerçek genişlik)"""
        ekle(ad, KS.cihaz_step(kod, xa, yc, RAY_Z[1], yon=-1), mal, B1, bom)
        return xa + KS.olcu(kod)[0]
    ARALIK_A = 1.0                                         # ray A: Acti9 cihazları arası (gerçek genişlik + 1 ≈ 9 mm modül adımı · iC60N kutuları bitişik, v3.4 gibi)
    ARALIK_B = (6.0, 6.0, 8.0)                             # ray B: v3.4 dizilişindeki boşluklar korunur (NDR | RevPi | switch | klemens)
    xa = x0 + 17.0
    # ---- ray A (y RAY_A_Y): iSW 4P · iID 4P · 6 × iC60N 1P+N
    xs = din_step("ana_salter_iSW_4P_40A", "A9S65440", xa, RAY_A_Y,
                  bom=("Ana şalter Schneider Acti9 iSW 4P 40 A (A9S65440)", 1, KS.bom_kaynak("A9S65440"), "bina beslemesi 400 V 3F"))
    xs = din_step("kacak_akim_iID_4P_40A_30mA", "A9R21440", xs + ARALIK_A, RAY_A_Y,
                  bom=("Kaçak akım Schneider Acti9 iID 4P 40 A 30 mA tip A (A9R21440)", 1, KS.bom_kaynak("A9R21440"), ""))
    SG = ["TOPPING", "DOLAP", "K", "E", "ROBOT", "QR"]
    xg = xs + ARALIK_A
    for i, s in enumerate(SG):
        din("sigorta_iC60N_1PN_C16_%s" % s, xg + 36.0 * i, 36.0, 90.0, 75.0, RAY_A_Y,
            bom=("Sigorta Schneider Acti9 iC60N 1P+N C16 (A9F79616)", len(SG), "ZARF — katalog STEP'i bulunamadı (kod teyit) · kutu 36 × 90 × 75 [VARSAYIM]",
                 "istasyon başına 1 · fazlara dengeli dağıtım") if i == 0 else None)
    # ---- ray B (y RAY_B_Y): NDR-120 · RevPi Connect 4 · FL SWITCH 1008N · 16 klemens
    xb = din_step("guc_24V_NDR-120-24", "NDR-120-24", xa, RAY_B_Y,
                  bom=("Mean Well NDR-120-24", 1, KS.bom_kaynak("NDR-120-24"), "ana bilgisayar + switch + modem (UPS çıkışından)"))
    xb = din_step("hmi_ana_bilgisayar_RevPi_Connect_4", "PR100378", xb + ARALIK_B[0], RAY_B_Y, "cihaz_koyu",
                  bom=("ANA BİLGİSAYAR Kunbus Revolution Pi Connect 4 PR100378 (4 GB RAM · 32 GB eMMC · WLAN'sız · Raspberry Pi CM4 tabanlı endüstriyel, EKRANSIZ, DIN, 24 V, 2 × Ethernet, RTC, WDT)", 1,
                       KS.bom_kaynak("PR100378"),
                       "sipariş sırası + istasyon koordinasyonu + web paneli (iPad / telefon: modemin Wi-Fi'ı ya da uzaktan VPN) · PLC'lerle Ethernet (S7 / Modbus TCP)"))
    xb = din_step("ag_anahtari_FL_SWITCH_1008N", "1085256", xb + ARALIK_B[1], RAY_B_Y, "cihaz_koyu",
                  bom=("Endüstriyel switch Phoenix Contact FL SWITCH 1008N (1085256 · 8 × RJ45)", 1, KS.bom_kaynak("1085256"), "ana bilgisayar · 4 istasyon PLC · robot · QR kartı · modem"))
    xk = xb + ARALIK_B[2]
    for i in range(16):
        din("klemens_PT2_5_%02d" % i, xk + 5.2 * i, 5.2, 60.0, 45.0, RAY_B_Y, bom=("Klemens Phoenix PT 2,5 (+ PE)", 16, "", "") if i == 0 else None)
    for nm, (a, b, c0, c1) in (("yatay_orta", (x0 + 12.0, x1 - 52.0, 1900.0, 1940.0)), ("yatay_alt", (x0 + 12.0, x1 - 12.0, 1706.0, 1746.0))):
        g, k = kanal("x", a, b, c0, c1, PL_Z[0] - 40.0, PL_Z[0], acik="-")
        ekle("pano_kablo_kanali_%s" % nm, g, "kanal", B1, bom=("Pano kablo kanalı PVC 40 × 40 + kapak", 3, "", "") if nm == "yatay_orta" else None)
        ekle("pano_kablo_kanali_%s_kapak" % nm, k, "kanal", B1)
    g, k = kanal("y", 1746.0, 1940.0, x1 - 52.0, x1 - 12.0, PL_Z[0] - 40.0, PL_Z[0], acik="-")
    ekle("pano_kablo_kanali_dikey", g, "kanal", B1); ekle("pano_kablo_kanali_dikey_kapak", k, "kanal", B1)
    # ---------------- 2 · PANO ALTI TAVA · ORTA DİKEY KANAL · KART KANALI · ALT BÖLME ----------------
    tx0, tx1 = TAVA["x"]; ty0, ty1 = TAVA["y"]; tz0, tz1 = TAVA["z"]
    g, k = kanal("x", tx0, tx1, tz0, tz1, ty0, ty1, acik="+")        # kesit z × y · kapak üstte (y +)
    # kanal() x ekseninde (c = y, d = z) bekler → burada tava yatay: c = z değil; elle kur
    g = kut(tx0, tx1, ty0, ty1, tz0, tz1).cut(kut(tx0 + 1.5, tx1 - 1.5, ty0 + 1.5, ty1 + 1.0, tz0 + 1.5, tz1 - 1.5))
    kap = kut(tx0, tx1, ty1, ty1 + 1.5, tz0, tz1)
    for (rx, rz) in RK:                                                # kapakta kablo girişleri (rakorların altında)
        kap = kap.cut(sil((rx, ty1 - 1.0, rz), (rx, ty1 + 3.0, rz), 9.5))
    kap = kap.cut(kut(QK["x"][0], min(tx1, QK["x"][1]), ty1 - 1.0, ty1 + 3.0, QK["z"][0], min(tz1, QK["z"][1])))
    ekle("qr_pano_alti_kablo_tavasi", g, "kanal", B2, bom=("Pano altı kablo tavası 304 1,5 (213 × 35 × 320) + delikli kapak", 1, "lazer + abkant", "üst rafa 4 × perçin · kablolar rakorlara dik girer"))
    ekle("qr_pano_alti_kablo_tavasi_kapak", kap, "kanal", B2)
    DELIKLER.append(("QR", "ust_raf_3", kut(QK["x"][0], QK["x"][1], 1649.0, 1654.0, QK["z"][0], QK["z"][1]), "orta kanal → tava"))
    DELIKLER.append(("QR", "alt_raf_3", kut(QK["x"][0], QK["x"][1], 446.0, 451.0, ALT["z"][0], QK["z"][1]), "orta kanal → alt bölme"))
    g, k = kanal("y", 450.0, 1650.0, QK["x"][0], QK["x"][1], QK["z"][0], QK["z"][1], acik="+")
    ekle("qr_orta_dikey_kanal", g, "kanal", B2, bom=("Yassı kablo kanalı PVC 24 × 150 + kapak (göz sütunları arasında)", 1, "", "göz kasası yan saclarına perçin"))
    ekle("qr_orta_dikey_kanal_kapak", k, "kanal", B2)
    g, k = kanal("y", 21.0, 447.0, ALT["x"][0], ALT["x"][1], ALT["z"][0], ALT["z"][1], acik="+")
    kb_ = KANAL_B; ky0, ky1 = kb_["y"]; kt_ = kb_["t"]
    g = g.cut(kut(ALT["x"][1] - kt_ - 1.0, ALT["x"][1] + 1.0, ky0 + kt_, ky1, kb_["arka"][2] + kt_, kb_["arka"][3] - kt_))   # v3.4 · dipte sağ duvar açık → taban kanalı
    ekle("qr_alt_dikey_kanal", g, "kanal", B2); ekle("qr_alt_dikey_kanal_kapak", k, "kanal", B2)
    # ---------------- 2b · v3.4 İÇ OMURGA KANALI: alt dikey kanal dibi → arka taban kanalı → sağ köşe kanalı → giriş (b) toplama kutusu ----------------
    #   (eski: qr_alt_taban_kanali → qr_guc_taban_rakoru_M40 → taban plakasından ZEMİN KANALINA — KALKTI)
    dis_, ic_, kap_ = None, None, None
    for nm in ("on", "kose", "arka"):
        x0_, x1_, z0_, z1_ = kb_[nm]
        d1 = kut(x0_, x1_, ky0, ky1, z0_, z1_)
        if nm == "on": c1 = kut(x0_ + kt_, x1_ - kt_, ky0 + kt_, ky1 + 1.0, z0_ - 1.0, z1_ - kt_)        # ön yüz açık (tekmeliğin kesiğine)
        elif nm == "kose": c1 = kut(x0_ + kt_, x1_ - kt_, ky0 + kt_, ky1 + 1.0, z0_ - 1.5, z1_ - kt_)    # ön toplama kutusuna açık
        else: c1 = kut(x0_ - 3.0, x1_ - kt_, ky0 + kt_, ky1 + 1.0, z0_ + kt_, z1_ - kt_)                  # sol uç alt dikey kanala açık
        dis_ = d1 if dis_ is None else dis_.fuse(d1); ic_ = c1 if ic_ is None else ic_.fuse(c1)
        k1 = kut(x0_, x1_, ky1, ky1 + kt_, z0_, z1_); kap_ = k1 if kap_ is None else kap_.fuse(k1)
    gk = dis_.cut(ic_).cut(sil((GIRIS_C["x"] - 10.0, GIRIS_C["y"], GIRIS_C["z"]), (GIRIS_C["x"] + 2.0, GIRIS_C["y"], GIRIS_C["z"]), 19.5)).clean()
    ekle("qr_omurga_kanali", gk, "paslanmaz", B2,
         bom=("İç omurga kanalı 304 1,5 · 60 yüksek (toplama kutusu 105 × 40 + sağ köşe 48 × 338 + arka taban 420 × 36) + üst kapak", 1, "lazer + abkant · taban plakasına 6 × perçin",
              "v3.4 · alt dikey kanal → kangalın arkası → kangal ile sağ yan sac arası → tekmelik girişi (b) · kanal içi kablolar çizilmez"))
    ekle("qr_omurga_kanali_kapak", kap_.clean(), "paslanmaz", B2)
    # ---------------- 2c · v3.4 TEKMELİK + KISALTILMIŞ ALT SERVİS KAPAĞI + MENTEŞE ----------------
    tx0_, tx1_ = TEKME["x"]; tey0, tey1 = TEKME["y"]; tz0_, tz1_ = TEKME["z"]; ku = TEKME["kulak"]
    xa_ = GIRIS_A["xc"]; ka_, kh_ = GIRIS_A["kesik"]
    xb_ = (GIRIS_B["x"][0] + GIRIS_B["x"][1]) / 2.0; kbw, kbh = GIRIS_B["kesik"]; yb_ = (GIRIS_B["y"][0] + GIRIS_B["y"][1]) / 2.0
    tk = kut(tx0_, tx1_, tey0, tey1, tz0_, tz1_).fuse(kut(tx0_, tx0_ + 1.5, tey0, tey1, tz1_, tz1_ + ku)).fuse(kut(tx1_ - 1.5, tx1_, tey0, tey1, tz1_, tz1_ + ku))
    tk = tk.cut(kut(xa_ - ka_ / 2.0, xa_ + ka_ / 2.0, GIRIS_A["y"] - kh_ / 2.0, GIRIS_A["y"] + kh_ / 2.0, tz0_ - 1.0, tz1_ + 1.0))
    tk = tk.cut(kut(xb_ - kbw / 2.0, xb_ + kbw / 2.0, yb_ - kbh / 2.0, yb_ + kbh / 2.0, tz0_ - 1.0, tz1_ + 1.0))
    ekle("qr_tekmelik_plint", tk.clean(), "paslanmaz", "ELK_QR_MONTAJ",
         bom=("Tekmelik (plint) sacı AISI 304 1,5 · 857 × 61 + 2 yan kulak 20 · kesikler 65 × 36 (KEL 10) + 86 × 36 (KEL-DPZ 16)", 1, "lazer + abkant · yan saclara 4 × M5 perçin somun",
              "v3.4 · servis kapağı düzleminde, taban plakasına oturur · kapak altı 3 mm"))
    kp = kut(tx0_ + 1.0, tx1_ - 1.0, KAPI_Y[0], KAPI_Y[1], tz0_, tz1_)
    for i in range(8):                                                     # yarık ızgara 8 × 30 × 70 (qr_cad_v1 ile aynı alan · y 40–110 → 94–164)
        kp = kp.cut(kut(5090.0 + 40.0 * i, 5120.0 + 40.0 * i, 94.0, 164.0, tz0_ - 1.0, tz1_ + 1.0))
    kp = kp.cut(sil((5300.0, 350.0, tz0_ - 1.0), (5300.0, 350.0, tz1_ + 1.0), 58.0)).cut(sil((5405.0, 234.0, tz0_ - 1.0), (5405.0, 234.0, tz1_ + 1.0), 11.5))
    ekle("servis_kapagi_alt_kisa", kp.clean(), "on_seffaf", "ELK_QR_MONTAJ",
         bom=("Servis kapağı 1,5 mm DKP boyalı · yarık ızgara 30 × 70 (alt 8 · üst 7) + fan deliği Ø116", 2, "855 × 362 (alt, v3.4 kısaltılmış) + 855 × 393 (üst)",
              "qr_cad_v1 servis_kapagi_alt yerine (tekmelik geldi) · kilit (y 234) ve üst menteşe (y 370) aynı"))
    ekle("servis_mentesesi_0_y100", kut(tx0_, 4590.0, 100.0, 140.0, tz1_, 689.5), "celik", "ELK_QR_MONTAJ",
         bom=("Gizli menteşe (servis kapağı)", 4, "2 kapak × 2 · alt kapağın alt menteşesi y 50 → 100", "VARSAYIM · katalog (qr_cad_v1 ile aynı kalem)"))
    # ---------------- 2d · v3.4 GİRİŞ (a) ROBOT KABLOSU: icotek KEL 10|3 + KT 20 + 2 × BTK (kablo h3_ray_ek_v2'de) ----------------
    pw, ph = GIRIS_A["pencere"]; L_, W_, H_ = GIRIS_A["L"], GIRIS_A["W"], GIRIS_A["H"]; ya_ = GIRIS_A["y"]
    px0 = GIRIS_A["x"] - GIRIS_A["kt"] / 2.0
    ekle("giris_a_KEL_10_3_cerceve", kut(xa_ - L_ / 2.0, xa_ + L_ / 2.0, ya_ - W_ / 2.0, ya_ + W_ / 2.0, tz0_ - H_, tz0_).cut(
        kut(px0, px0 + pw, ya_ - ph / 2.0, ya_ + ph / 2.0, tz0_ - H_ - 1.0, tz0_ + 1.0)), "rakor", B2,
         bom=("Bölünmüş kablo giriş çerçevesi icotek KEL 10|3 V2A (42212.200) · 98 × 58 × 17 · kesik 65 × 36 · paslanmaz vidalı", 1, "icotek.com KEL",
              "v3.4 · robot uzatma kablosu KONNEKTÖRÜYLE geçer (Ø26 < kesik 36) · dışı robot köprü kanalının içinde"))
    ekle("giris_a_KT_20_robot_kablosu", kut(px0, px0 + GIRIS_A["kt"], ya_ - ph / 2.0, ya_ + ph / 2.0, tz0_ - H_, tz0_).cut(
        sil((GIRIS_A["x"], ya_, tz0_ - H_ - 1.0), (GIRIS_A["x"], ya_, tz0_ + 1.0), GIRIS_A["r_delik"])), "rakor", B2,
         bom=("Yarık kablo lastiği icotek KT 20 gy (41220) · Ø20–21", 1, "41,5 × 42", "Fairino uzatma kablosu Ø20 VARSAYIM · çap ölçülüp KT 19 / 21 seçilir"))
    for j, (y0_, y1_) in enumerate(((ya_ - ph / 2.0, ya_), (ya_, ya_ + ph / 2.0))):
        ekle("giris_a_BTK_kor_%d" % j, kut(px0 + GIRIS_A["kt"], px0 + pw, y0_, y1_, tz0_ - H_, tz0_), "rakor", B2,
             bom=("Kör lastik icotek BTK gy (41251) · KT small", 2, "21 × 21", "KEL 10|3'ün boş iki küçük yuvası") if j == 0 else None)
    # ---------------- 2e · v3.4 GİRİŞ (b) MAKİNE OMURGASI: icotek KEL-DPZ 16|14 + kablo uçları (tekmeliğin 30 mm dışına) ----------------
    fb = kut(GIRIS_B["x"][0], GIRIS_B["x"][1], GIRIS_B["y"][0], GIRIS_B["y"][1], tz0_ - GIRIS_B["H"], tz0_)
    for ad, r, m, bx, by in B_KABLOLAR:
        fb = fb.cut(sil((bx, by, tz0_ - GIRIS_B["H"] - 1.0), (bx, by, tz0_ + 1.0), r + 0.05))
    ekle("giris_b_KEL-DPZ_16_14", fb.clean(), "rakor", B2,
         bom=("Çok membranlı kablo giriş plakası icotek KEL-DPZ 16|14 gy (43816) · 120 × 58 × 14 · kesik 86 × 36 · IP66", 1,
              "membran: 4 × 9–16,2 (H07RN-F 3G2,5) · 5 × 5–10,2 (4 × Cat6A + 1 yedek) · 5 × 3,2–6,5 yedek", "v3.4 · membran yerleşimi VARSAYIM (güç sağda) · 4 × M5"))
    for ad, r, m, bx, by in B_KABLOLAR:
        ekle("qrk_%s_giris_b_ucu" % ad, boru([(bx, by, 695.0), (bx, by, tz0_ - UC_DIS)], r), m, B2,
             bom=("İstasyon besleme kablosu H07RN-F 3G2,5 (Lapp 1600118, Ø10,9–14) · QR → TOPPING / DOLAP / K / E", 4, "", "QR pano C16 sigortasından") if ad == "guc_TOPPING_3G2_5" else
             (("Veri kablosu Lapp ETHERLINE Cat.6A (2170465, Ø8,7) · switch → 4 istasyon PLC", 4, "", "uçlar sahada RJ45 (membrandan konnektörsüz geçer)") if ad == "veri_TOPPING_Cat6A" else None))
    # ---------------- 2f · v3.4 GİRİŞ (c) BİNA BESLEMESİ 5G6: sağ yan sac · SKINTOP ST-M 32 ----------------
    rk, d_ = rakor((GIRIS_C["x"], GIRIS_C["y"], GIRIS_C["z"]), "x", GIRIS_C["r"] + 0.05, 1.5, yon="+", disli=GIRIS_C["disli"])
    ekle("giris_c_bina_besleme_rakoru_M32", rk, "rakor", B2,
         bom=("Kablo rakoru Lapp SKINTOP ST-M 32×1,5 RAL 7001 (53111040) + kilit somunu", 1, "sıkma aralığı föyden teyit (5G6 Ø17,5–22,2)",
              "v3.4 · bina beslemesi H07RN-F 5G6 (Lapp 16001313) · KEL-DPZ 16'nın 16,2 membranına sığmaz → sağ yan sac, ön köşenin 55 mm gerisi"))
    DELIKLER.append(("QR", "yan_sac_sag", d_, "v3.4 bina beslemesi 5G6 yan girişi (SKINTOP ST-M 32)"))
    ekle("qrk_bina_besleme_5G6_giris_c_ucu", boru([(5395.0, GIRIS_C["y"], GIRIS_C["z"]), (GIRIS_C["x"] + UC_DIS, GIRIS_C["y"], GIRIS_C["z"])], GIRIS_C["r"]), "kablo", B2,
         bom=("Bina beslemesi H07RN-F 5G6 (Lapp 16001313)", 1, "CEE 32 A · ana şaltere", "v3.4 · zemin kutusu YOK: bina tesisatından zemin üstü kanalla gelir (AÇIK: güzergâh)"))
    # ---------------- 2g · v3.4 eski taban geçişleri (qr_cad_v1 GECIS_ROBOT Ø40 + GECIS_GUC Ø30, z 975) üstten kapanır ----------------
    ekle("qr_taban_gecis_kapama_saci", kut(4755.0, 4840.0, 20.0, 21.5, 950.0, 1000.0), "paslanmaz", B2,
         bom=("Kapama sacı 304 1,5 · 85 × 50 (eski Ø40 + Ø30 taban geçişleri)", 1, "4 × perçin", "v3.4 · zeminden giriş kalmadı"))
    ukx0, ukx1 = UKN["x"]
    g = kut(ukx0, ukx1, UKN["y"][0], UKN["y"][1], UKN["z"][0], UKN["z"][1]).cut(kut(ukx0 - 1.0, ukx1 - 1.5, UKN["y"][0] + 1.5, UKN["y"][1] + 1.0, UKN["z"][0] + 1.5, UKN["z"][1] - 1.5))
    ekle("qr_kart_kanali", g, "kanal", B2, bom=("Kart kanalı PVC 40 × 30 + kapak (tava → kilit kartı)", 1, "", "üst rafa yapışkan tabanlı klips"))
    ekle("qr_kart_kanali_kapak", kut(ukx0, ukx1, UKN["y"][1], UKN["y"][1] + 1.5, UKN["z"][0], UKN["z"][1]), "kanal", B2)
    # ---------------- 3 · KANAL DIŞI UÇLAR (kısa · rakora / cihaza dik) ----------------
    for i, ((rx, rz), (ad, r, m)) in enumerate(zip(RK, KABLOLAR)):
        ekle("qrk_%s_rakor_ucu" % ad, sil((rx, ty1 + 1.5, rz), (rx, y0 + 6.0, rz), r), m, B2)       # tava kapağı → pano rakoru (dik, ≤ 10)
    # kilit kartı uçları (kart kanalından PCB alt kenarındaki klemenslere) · modem
    for i, xk in enumerate((5160.0, 5200.0, 5240.0, 5280.0)):
        ekle("qrk_kart_ucu_%d" % i, boru([(xk, UKN["y"][1], 1015.0), (xk, 1676.0, 1015.0), (xk, 1676.0, 1060.0)], 3.0), "kablo", B2)
    ekle("qrk_modem_ucu", boru([(5320.0, UKN["y"][1], 1015.0), (5320.0, 1900.0, 1015.0), (5320.0, 1900.0, 1060.0)], 3.75), "kablo_veri", B2)
    ekle("qrk_modem_ucu_kelepce", EO.kelepce((5320.0, 1800.0, 1015.0), "y", 3.75, 1060.0, "+z"), "celik", B2)
    # UPS: tavadan UPS'in sol alt yüzüne
    for i, zz in enumerate((820.0, 850.0)):
        ekle("qrk_ups_ucu_%d" % i, boru([(4995.0, ty1 + 1.5, zz), (4995.0, 1700.0, zz), (5005.0, 1700.0, zz)], 4.5), "kablo", B2)
    # robot kontrol kutusu: alt dikey kanaldan kutunun arka yüzüne
    for i, (ad, yy) in enumerate((("guc_ROBOT", 300.0), ("veri_ROBOT", 260.0))):
        ekle("qrk_%s_kutu_ucu" % ad, boru([(4995.0, yy, ALT["z"][0]), (4995.0, yy, 943.0)], 5.5 if ad.startswith("guc") else 3.75), "kablo" if ad.startswith("guc") else "kablo_veri", B2)
    # ---------------- 4 · GÖZ CİHAZLARI: uç kabloları + braketler ----------------
    import re
    gozler = sorted(set(re.match(r"goz_(\d\d)_", a).group(1) for a in P if re.match(r"goz_\d\d_kapak_motoru$", a)))
    kx = (QK["x"][0] + QK["x"][1]) / 2.0
    for g_ in gozler:
        sat, sut = int(g_[0]), int(g_[1])
        mb = P["goz_%s_kapak_motoru" % g_].BoundingBox(); sb = P["goz_%s_kapak_sensoru" % g_].BoundingBox()
        db = P["goz_%s_elektrikli_mandal" % g_].BoundingBox(); ib = P["goz_%s_isitici_ped" % g_].BoundingBox()
        kb = P["goz_%s_kasasi" % g_].BoundingBox()
        kx = (QK["x"][0] + QK["x"][1]) / 2.0                          # 4995 · dikme aralığı 4990–5000 (robot 712–732 · müşteri 1128–1148)
        kz0, kz1 = QK["z"][0] + 1.0, QK["z"][1] - 1.0
        my = (mb.ymin + mb.ymax) / 2.0; sy = (sb.ymin + sb.ymax) / 2.0
        if sut == 0:
            # motor (sol üst köşe) → sıra aralığı (y kasa üstü + 2,5) → orta → kanal · x yolunda yüz sacına P-kelepçe
            yg = kb.ymax + (3.2 if sat == 5 else 2.5); mx = (mb.xmin + mb.xmax) / 2.0
            pts = [(mx, mb.ymax, 691.0), (mx, yg, 691.0), (kx, yg, 691.0), (kx, yg, kz0)]
            ekle("goz_%s_motor_kablosu" % g_, boru(pts, 2.0), "kablo", B2)
            for j, xk in enumerate((mx + 80.0, (mx + kx) / 2.0, kx - 60.0)):
                ekle("goz_%s_motor_kablosu_kelepce_%d" % (g_, j), EO.kelepce((xk, yg, 691.0), "x", 2.0, *((1650.0, "+y") if sat == 5 else (672.0, "-z"))), "celik", B2)
            # sensör (sağ alt) → +x 3 → kanal (kendi yüksekliğinde dikme aralığından)
            ekle("goz_%s_sensor_kablosu" % g_, boru([(sb.xmax, sy, 681.0), (kx, sy, 681.0), (kx, sy, kz0)], 1.75), "kablo", B2)
        else:
            # motor (sol üst köşe, 5012) → −x → kanal
            ekle("goz_%s_motor_kablosu" % g_, boru([(mb.xmin, my, 691.0), (kx, my, 691.0), (kx, my, kz0)], 2.0), "kablo", B2)
            # sensör (sağ alt, 5388–5402) → yukarı (x 5397) → sıra aralığı (kasa üstü + 8) → −x → kanal · yüz sacına P-kelepçe
            yg = kb.ymax + (6.0 if sat == 5 else 8.0); sx = 5397.0
            pts = [(sx, sb.ymax, 681.0), (sx, yg, 681.0), (kx, yg, 681.0), (kx, yg, kz0)]
            ekle("goz_%s_sensor_kablosu" % g_, boru(pts, 1.75), "kablo", B2)
            for j, (p_, ax) in enumerate((((sx, (sb.ymax + yg) / 2.0, 681.0), "y"), ((sx - 100.0, yg, 681.0), "x"), (((sx + kx) / 2.0, yg, 681.0), "x"), ((kx + 60.0, yg, 681.0), "x"))):
                ekle("goz_%s_sensor_kablosu_kelepce_%d" % (g_, j), EO.kelepce(p_, ax, 1.75, *((1650.0, "+y") if (sat == 5 and ax == "x") else (672.0, "-z"))), "celik", B2)
        # mandal (müşteri tarafı, orta) → arkasından müşteri dikme aralığından kanala
        dy = (db.ymin + db.ymax) / 2.0
        ekle("goz_%s_mandal_kablosu" % g_, boru([(kx, dy, db.zmin), (kx, dy, kz1)], 1.75), "kablo", B2)
        # ısıtıcı ped: kasa yan sacındaki lastik bilezikten (ped köşesi) orta boşluktaki kanala
        xw = kb.xmax if sut == 0 else kb.xmin
        xk2 = QK["x"][0] + 0.5 if sut == 0 else QK["x"][1] - 0.5
        ekle("goz_%s_isitici_kablosu" % g_, boru([(xw + (0.5 if sut == 0 else -0.5), kb.ymin + 2.5, 1000.0), (xk2, kb.ymin + 2.5, 1000.0)], 1.25), "kablo", B2)
        # ---- braketler (havada düzeltmesi): motor · sensör · mandal · mil yatağı · kapak kulakları · menteşe ara plakaları
        yz = P["robot_yuzu_goz_saci"]
        bx0, bx1 = (kb.xmin, mb.xmax) if sut == 0 else (kb.xmin, mb.xmax)
        ekle("goz_%s_motor_braketi" % g_, kut(bx0, bx1, mb.ymin, kb.ymax, mb.zmax, kb.zmin).fuse(kut(bx0, bx0 + 1.5, mb.ymin, kb.ymax, mb.zmin, mb.zmax)), "celik", B3,
             bom=("Kapak motoru braketi 304 2 mm (kasaya 2 × M4)", 12, "lazer + abkant", "v3.2 havada düzeltmesi") if g_ == gozler[0] else None)
        ekle("goz_%s_sensor_braketi" % g_, kut(sb.xmin, sb.xmax, sb.ymin, sb.ymax, yz.BoundingBox().zmax, sb.zmin), "celik", B3,
             bom=("Sensör braketi 304 (yüz sacına perçin)", 12, "", "") if g_ == gozler[0] else None)
        dik = P["goz_dikmesi_11"] if sut == 0 else P["goz_dikmesi_21"]
        ekle("goz_%s_mandal_braketi" % g_, kut(db.xmin, db.xmax, db.ymin, db.ymax, dik.BoundingBox().zmax, db.zmin), "celik", B3,
             bom=("Mandal braketi 304 2 mm (dikmeye 2 × M4)", 12, "", "") if g_ == gozler[0] else None)
        yb = P["goz_%s_mil_yatagi" % g_].BoundingBox()
        ekle("goz_%s_mil_yatagi_braketi" % g_, kut(yb.xmin, yb.xmax, yb.ymin, yb.ymax, yz.BoundingBox().zmax, yb.zmin), "celik", B3,
             bom=("Mil yatağı braketi 304 (yüz sacına)", 12, "", "") if g_ == gozler[0] else None)
        mil = P["goz_%s_kapak_mili" % g_].BoundingBox(); kp = P["goz_%s_robot_kapagi" % g_].BoundingBox()
        myc, mzc = (mil.ymin + mil.ymax) / 2.0, (mil.zmin + mil.zmax) / 2.0; mr = (mil.ymax - mil.ymin) / 2.0
        for j, xk in enumerate((kp.xmin + 8.0, kp.xmax - 28.0)):
            ekle("goz_%s_kapak_kulagi_%d" % (g_, j), sil((xk, myc, mzc), (xk + 20.0, myc, mzc), myc - kp.ymax).cut(sil((xk - 1, myc, mzc), (xk + 21.0, myc, mzc), mr)), "celik", B3,
                 bom=("Kapak kulağı (menteşe burcu) 304 · kapağa kaynaklı, mile geçer", 24, "", "") if (g_ == gozler[0] and j == 0) else None)
        for j in (0, 1):
            h = P["goz_%s_mentese_%d" % (g_, j)].BoundingBox()
            ekle("goz_%s_mentese_%d_ara_plakasi" % (g_, j), kut(h.xmin, h.xmax, h.ymin, h.ymax, kb.zmax, h.zmin), "celik", B3,
                 bom=("Menteşe ara plakası 304 10 mm (kasaya 2 × M4)", 24, "", "") if (g_ == gozler[0] and j == 0) else None)
    return dict(RK=RK, gozler=gozler, arayuz=arayuz())


def arayuz():
    """v3.4 · dış kanal arayüzü (h3_elk_hat_v1 buradan alır): kablo uçları (dünya, uç düzlemi z) + çerçeve zarfları"""
    tz0_ = TEKME["z"][0]; zu = tz0_ - UC_DIS
    uc = [(ad, bx, by, zu, 2.0 * r) for ad, r, m, bx, by in B_KABLOLAR]
    xs = [bx - r for ad, r, m, bx, by in B_KABLOLAR] + [bx + r for ad, r, m, bx, by in B_KABLOLAR]
    ys = [by - r for ad, r, m, bx, by in B_KABLOLAR] + [by + r for ad, r, m, bx, by in B_KABLOLAR]
    return dict(b_uclar=uc, b_demet=(min(xs), max(xs), min(ys), max(ys), zu), b_cerceve=(GIRIS_B["x"][0], GIRIS_B["x"][1], GIRIS_B["y"][0], GIRIS_B["y"][1], tz0_ - GIRIS_B["H"], tz0_),
                c_uc=("bina_besleme_5G6", GIRIS_C["x"] + UC_DIS, GIRIS_C["y"], GIRIS_C["z"], 2.0 * GIRIS_C["r"]),
                c_rakor=(GIRIS_C["x"], GIRIS_C["x"] + 12.0, GIRIS_C["y"] - GIRIS_C["disli"] - 3.5, GIRIS_C["y"] + GIRIS_C["disli"] + 3.5,
                         GIRIS_C["z"] - GIRIS_C["disli"] - 3.5, GIRIS_C["z"] + GIRIS_C["disli"] + 3.5),
                a_cerceve=(GIRIS_A["xc"] - GIRIS_A["L"] / 2.0, GIRIS_A["xc"] + GIRIS_A["L"] / 2.0, GIRIS_A["y"] - GIRIS_A["W"] / 2.0, GIRIS_A["y"] + GIRIS_A["W"] / 2.0,
                           tz0_ - GIRIS_A["H"], tz0_), tekmelik=(TEKME["x"], TEKME["y"], TEKME["z"]), kapi_y=KAPI_Y)
