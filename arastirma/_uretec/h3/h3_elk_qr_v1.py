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
  görünmeyen iç katılar atılır, dış ölçü aynı) · raylar gerçek genişliklerle yeniden dizildi · iC60N 1P+N C16 (A9F79616) ZARF kaldı (katalog STEP'i bulunamadı).
v3.6 (1 Eki 2026 · Claude · YEREL) — Kemal: "ANA PANO + BEYİN QR'da OLMASIN (U_F'de kendi başına ürün: h3_ana_pano_v1) · HER İSTASYON KENDİ BAŞINA ÇALIŞSIN".
  · KALKTI: 400 × 350 × 250 ana pano + bütün iç cihazları (iSW · iID · 6 × iC60N · NDR-120 · RevPi · switch · klemens · pano kanalları · 16 rakor) ·
    giriş (c) bina beslemesi (SKINTOP M32 + yan sac deliği + uç) · istasyon besleme uçları (TOPPING · DOLAP · K · E) · robot kutusu uçları.
  · YENİ: QR İSTASYON KUTUSU 300 × 220 × 200 (eski panonun yerinde): iC60N C10 · NDR-120-24 (göz cihazları 24 V) · FL SWITCH 1008N · 10 klemens ·
    üstte Harting Han 10B (soket + fiş + M32) → ana hat kablosu tavaya iner · altta 3 rakor (göz demeti · kart + modem · UPS). UPS QR kilit kartında KALIR.
  · ROBOT: denetleyici kutusunun (REZERV) arkasında Harting Han 10B → alt dikey kanal.
  · Giriş (b) KEL-DPZ 16|14: 5 kablo (QR güç + veri · ROBOT güç + veri · modem Cat6A → ana panonun modem rakoru).
v3.7 (2 Eki 2026 · Claude · YEREL) — Kemal: "tüm makinede alt etek yok" → QR TEKMELİĞİ KALKTI: alt servis kapağı yine tam boy (y 21–446), iki ÇENTİKLİ ·
  çentiklerde QR'nin kendi küçük GİRİŞ PLAKALARI (a: robot kablosu KEL 10|3 · b: ana hat KEL-DPZ 16|14), taban plakasına oturur (TEKME sabitleri = plaka düzlemi,
  h3_ray_ek_v2 aynı) · ana hat kabloları QR içinde ÇİZİLDİ (giriş → omurga → alt / orta dikey kanal → robot Harting · tava → QR kutusu Harting · modem → kart kanalı)."""
import math
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, boru, kanal, rakor

V = cq.Vector
# ---------------- v3.4 · TEKMELİK + GİRİŞLER (tek kaynak · h3_ray_ek_v2 giriş (a) sabitlerini BURADAN okur) ----------------
TEKME = dict(x=(4571.5, 5428.5), y=(20.0, 81.0), z=(670.0, 671.5), kulak=20.0)     # tekmelik sacı (taban plakası üstü 20 · kapak altı 84)
KAPI_Y = (84.0, 446.0)                                 # v3.7: giriş plakası üstü / çentik (kapak tam boy 21–446 · h3_ray_ek_v2 köprü kontrolü bunu okur)
PLAKA_A = (5040.0, 5157.0); PLAKA_B = (5300.0, 5428.0); PLAKA_Y = 83.6        # v3.7 · giriş plakaları (x) · üstü (çentik 2 mm boşluk)
QR_DUSUR = ["servis_kapagi_alt", "servis_mentesesi_0"]  # qr_cad_v1 parçaları (yerine kısa kapak + y 100 menteşe)
# (a) robot kablosu · icotek KEL 10|3: 98 × 58 × 17 (dışta), kesik 65 × 36 · pencere 62,5 × 42: KT 20 (41,5 × 42) solda + 2 × BTK (21 × 21) üst üste sağda
GIRIS_A = dict(x=5088.0, y=50.0, L=98.0, W=58.0, H=17.0, kesik=(65.0, 36.0), pencere=(62.5, 42.0), kt=41.5, r_delik=10.05)
GIRIS_A["xc"] = GIRIS_A["x"] - GIRIS_A["kt"] / 2.0 + GIRIS_A["pencere"][0] / 2.0          # çerçeve merkezi 5098,5
# (b) makine omurgası · icotek KEL-DPZ 16|14: 120 × 58 × 14 (dışta), kesik 86 × 36 · membran yerleşimi VARSAYIM (güç sağda: köşe kanalına düz)
GIRIS_B = dict(x=(5308.0, 5428.0), y=(21.0, 79.0), H=14.0, kesik=(86.0, 36.0))
B_KABLOLAR = [("guc_QR_3G2_5", 6.25, "kablo", 5386.0, 59.0), ("guc_ROBOT_3G2_5", 6.25, "kablo", 5402.0, 59.0),          # v3.6 · yalnız QR + ROBOT ana hatları + modem
              ("veri_QR_Cat6A", 4.35, "kablo_veri", 5354.0, 59.0), ("veri_ROBOT_Cat6A", 4.35, "kablo_veri", 5370.0, 59.0),
              ("veri_MODEM_Cat6A", 4.35, "kablo_veri", 5354.0, 41.0)]
UC_DIS = 30.0                                          # kablo uçları tekmelik dış yüzünün bu kadar dışında biter (dış kanal arayüzü)
# (c) bina beslemesi 5G6 · sağ yan sac (dış yüz x 5430) · SKINTOP ST-M 32
GIRIS_C = dict(x=5430.0, y=50.0, z=725.0, r=9.95, disli=16.0)
# iç omurga kanalı (304 1,5 · y 20–80 + kapak 80–81,5): ön toplama kutusu · sağ köşe · arka taban
KANAL_B = dict(on=(5322.0, 5427.0, 671.5, 712.0), kose=(5379.0, 5427.0, 710.5, 1048.0), arka=(5007.0, 5427.0, 1012.0, 1048.0), y=(20.0, 80.0), t=1.5)
QB = dict(x=(4640.0, 4940.0), y=(1700.0, 1920.0), z=(675.0, 877.0), t=1.2)   # v3.6 · QR İSTASYON KUTUSU (kapak z 675–677 · gövde 677–877)
PL_Z = (845.0, 848.0)
RAY_Z = (837.5, 845.0)
RAY_Y = 1830.0
QB_HARTING = (4880.0, 1920.0, 790.0)                   # Han 10B soketi kutunun üstünde (L x boyunca · W z boyunca)
QB_RAKOR = [("goz_demeti", 9.0, 4830.0, 800.0), ("kart_modem", 6.0, 4870.0, 800.0), ("ups", 6.0, 4910.0, 800.0)]   # (ad, r, x, z) kutu tabanı → tava
ANA_HAT_QR = [(4880.0, 2011.0, 790.0), (4880.0, 2025.0, 790.0), (4965.0, 2025.0, 790.0), (4965.0, 1680.0, 790.0)]   # Harting rakoru → tava (ana hat QR)
ROBOT_HARTING = (4880.0, 300.0, 943.0)                 # robot denetleyici kutusunun (REZERV) arka yüzü · fiş +z
QK = dict(x=(4983.0, 5007.0), z=(930.0, 1080.0))       # orta dikey kanal (göz sütunları arası 4980–5010)
TAVA = dict(x=(4790.0, 5003.0), y=(1655.0, 1690.0), z=(760.0, 1080.0))   # pano altı kablo tavası (üst rafta)
UKN = dict(x=(5003.0, 5390.0), y=(1656.0, 1686.0), z=(995.0, 1035.0))    # kilit kartı kanalı
ALT = dict(x=(4983.0, 5007.0), z=(1000.0, 1080.0))     # alt bölme dikey kanal (kontrol kutusunun arkasında, z > 943)
# v3.4: TABAN_KN + GUC_RAKOR (M40 taban rakoru → zemin kanalı) KALKTI — yerine KANAL_B + GIRIS_B / GIRIS_C (yukarıda)
# v3.6 · KABLOLAR (eski ana pano rakorları) KALKTI

def kur(ekle, DELIKLER, DUSUR, QR):
    """QR: qr_cad_v1 modülü (kur() yapılmış, parçalar dünya) · ekle(ad, sh, mal, birim, bom)"""
    P = {p["ad"]: QR.dunya(p) if hasattr(QR, "dunya") else p["wp"].val() for p in QR.PARCALAR}
    B1, B2, B3 = "ELK_QR_KUTU", "ELK_QR_KABLO", "ELK_QR_MONTAJ"            # v3.6 · ana pano U_F'de (h3_ana_pano_v1)
    x0, x1 = QB["x"]; y0, y1 = QB["y"]; z0, z1 = QB["z"]; t = QB["t"]
    # ---------------- 1 · v3.6 QR İSTASYON KUTUSU (Kemal 1 Eki: ana pano + beyin QR'da DEĞİL → U_F'de kendi başına ürün, h3_ana_pano_v1) ----------------
    #   QR'de yalnız QR'nin kendi istasyon kutusu: göz cihazları (motor · sensör · mandal · ısıtıcı) + kilit kartı + modem + UPS buraya toplanır ·
    #   ana panoya TEK güç + TEK veri hattı Harting Han 10B fişiyle (kutunun üstünde) · robot denetleyicisi kendi Harting'iyle (2h).
    DUSUR += [("QR", "ana_pano_400x350x250"), ("QR", "ana_pano_ayak_rayi_0"), ("QR", "ana_pano_ayak_rayi_1")]
    DUSUR += [("QR", a_) for a_ in QR_DUSUR]                                       # v3.4 · alt servis kapağı + alt menteşesi (tekmelik geldi)
    for i, (ax0, ax1) in enumerate(((4650.0, 4680.0), (4740.0, 4770.0))):
        ekle("qr_kutu_ayagi_%d" % i, kut(ax0, ax1, 1653.0, y0, 700.0, 860.0).cut(kut(ax0 + 2, ax1 - 2, 1652.0, y0 + 1.0, 702.0, 858.0)), "celik", B1,
             bom=("Kutu ayağı 304 kutu profil 30 × 47 × 2 (altında kablo tavası)", 2, "üst rafa + kutuya M6", "v3.6") if i == 0 else None)
    govde = kut(x0, x1, y0, y1, z0 + 2.0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 + 1.0, z1 - t))
    for ad, r, rx, rz in QB_RAKOR:
        rk, d_ = rakor((rx, y0, rz), "y", r, t, yon="-", disli=8.0 if r < 6.0 else 12.0)
        govde = govde.cut(d_)
        ekle("qr_kutu_rakoru_%s" % ad, rk, "rakor", B1, bom=("Kablo rakoru PA IP68 M20 / M25 + somun (Lapp SKINTOP ST-M · çok delikli conta)", len(QB_RAKOR), "", "kutu tabanı") if ad == QB_RAKOR[0][0] else None)
    H = EO.harting(QB_HARTING, "+y", "x", t_duvar=t)
    govde = govde.cut(H["kesik"])
    ekle("qr_istasyon_kutusu_300x220x200", govde, "pano", B1,
         bom=("QR istasyon kutusu 300 × 220 × 200 · 304 paslanmaz (IP65 contalı kapı, 2 mm galvaniz montaj plakası)", 1, "lazer + abkant + kaynak",
              "v3.6 · eski 400 × 350 × 250 ana panonun yerinde (QR üst bölmesi robot tarafı) · altta %d rakor · üstte Harting Han 10B" % len(QB_RAKOR)))
    ekle("harting_QR_soket", H["soket"], "rakor", B1,
         bom=("Harting Han-Modular 10B anbau gövdesi + menteşeli çerçeve: Han E modülü (güç 16 A) + Han RJ45 modülü (Cat6A) · PE çerçeveden", 8,
              "Harting Han 10B (gövde 19 30 010 xxxx · çerçeve 09 14 010 0303 · Han E 09 14 006 3001 · RJ45 09 45 115 1100) [VARSAYIM: kod + ölçü föyden teyit]",
              "istasyon kutusu tarafı (dişi) · 8 istasyon: A · DOLAP · TOPPING · F · K · E · QR · ROBOT"))
    ekle("harting_QR_fis", H["fis"], "rakor", B1,
         bom=("Harting Han 10B fiş kapağı (hood) üstten çıkışlı M32 + tek kilit kolu · erkek modüller", 16, "Harting Han B hood top entry M32 [VARSAYIM]",
              "ana hat kablosunun iki ucu: istasyon kutusu + ana pano"))
    ekle("harting_QR_rakoru_M32", H["rakor"], "rakor", B1,
         bom=("Kablo rakoru M32 + 2 delikli conta (güç 3G2,5 + Cat6A) · Harting hood girişi", 16, "Lapp SKINTOP ST-M 32 + DIX-M [VARSAYIM]", ""))
    ekle("onyuz_qr_kutu_kapagi", kut(x0, x1, y0, y1, z0, z0 + 2.0), "on_seffaf", B1, bom=("Kutu kapağı (kilitli)", 1, "gövdeyle", ""))
    ekle("qr_kutu_montaj_plakasi", kut(x0 + 10.0, x1 - 10.0, y0 + 10.0, y1 - 10.0, PL_Z[0], PL_Z[1]), "din", B1, bom=("Montaj plakası galvaniz 2 mm", 1, "", ""))
    for i_, (px, py) in enumerate(((x0 + 20, y0 + 20), (x1 - 20, y0 + 20), (x0 + 20, y1 - 20), (x1 - 20, y1 - 20))):
        ekle("qr_kutu_plaka_burcu_%d" % i_, sil((px, py, PL_Z[1]), (px, py, z1 - t), 6.0), "celik", B1)
    ekle("qr_kutu_din_rayi", kut(x0 + 12.0, x1 - 12.0, RAY_Y - 17.5, RAY_Y + 17.5, RAY_Z[0], RAY_Z[1]), "din", B1, bom=("DIN rayı TS35 × 7,5", 1, "", ""))

    def din(ad, xa, w, h, d, yc, mal="cihaz", bom=None):
        ekle(ad, kut(xa, xa + w, yc - h / 2.0, yc + h / 2.0, RAY_Z[0] - d, RAY_Z[0]), mal, B1, bom)
    import katalog_step_v1 as KS

    def din_step(ad, kod, xa, yc, mal="cihaz", bom=None):
        """üretici STEP'i (KS.cihaz_step: önü −z, kapağa bakar) · döner: cihazın sağ kenarı (xa + gerçek genişlik)"""
        ekle(ad, KS.cihaz_step(kod, xa, yc, RAY_Z[1], yon=-1), mal, B1, bom)
        return xa + KS.olcu(kod)[0]
    xa = x0 + 16.0
    din("sigorta_iC60N_1PN_C10_QR", xa, 36.0, 90.0, 75.0, RAY_Y,
        bom=("Sigorta Schneider Acti9 iC60N 1P+N C10 (A9F79610) · QR kutusu girişi", 1, "ZARF — katalog STEP'i bulunamadı · kutu 36 × 90 × 75 [VARSAYIM]", ""))
    xb = din_step("guc_24V_NDR-120-24_QR", "NDR-120-24", xa + 42.0, RAY_Y,
                  bom=("Mean Well NDR-120-24 (QR göz cihazları 24 V: kapak motorları · mandallar · sensörler)", 1, KS.bom_kaynak("NDR-120-24"), "ısıtıcı pedler 230 V röleden"))
    xb = din_step("ag_anahtari_FL_SWITCH_1008N_QR", "1085256", xb + 6.0, RAY_Y, "cihaz_koyu",
                  bom=("Endüstriyel switch Phoenix Contact FL SWITCH 1008N (1085256) · QR: ana hat ↔ kilit kartı", 1, KS.bom_kaynak("1085256"), ""))
    for i in range(10):
        din("qr_klemens_PT2_5_%02d" % i, xb + 8.0 + 5.2 * i, 5.2, 60.0, 45.0, RAY_Y, bom=("Klemens Phoenix PT 2,5 (+ PE)", 10, "", "") if i == 0 else None)
    g, k = kanal("x", x0 + 12.0, x1 - 12.0, y0 + 12.0, y0 + 42.0, PL_Z[0] - 40.0, PL_Z[0], acik="-")
    ekle("qr_kutu_kablo_kanali", g, "kanal", B1, bom=("Kutu içi kablo kanalı PVC 30 × 40 + kapak", 1, "", "")); ekle("qr_kutu_kablo_kanali_kapak", k, "kanal", B1)
    RK = [(rx, rz) for ad, r, rx, rz in QB_RAKOR]
    # ---------------- 2 · PANO ALTI TAVA · ORTA DİKEY KANAL · KART KANALI · ALT BÖLME ----------------
    tx0, tx1 = TAVA["x"]; ty0, ty1 = TAVA["y"]; tz0, tz1 = TAVA["z"]
    g, k = kanal("x", tx0, tx1, tz0, tz1, ty0, ty1, acik="+")        # kesit z × y · kapak üstte (y +)
    # kanal() x ekseninde (c = y, d = z) bekler → burada tava yatay: c = z değil; elle kur
    g = kut(tx0, tx1, ty0, ty1, tz0, tz1).cut(kut(tx0 + 1.5, tx1 - 1.5, ty0 + 1.5, ty1 + 1.0, tz0 + 1.5, tz1 - 1.5))
    g = g.cut(kut(QK["x"][0], tx1 + 1.0, ty0 - 1.0, ty0 + 2.0, QK["z"][0] + 1.5, tz1 - 1.5))                    # v3.7 · orta dikey kanal tavaya açılır
    g = g.cut(kut(tx1 - 2.0, tx1 + 1.0, UKN["y"][0] + 1.5, ty1 + 1.0, UKN["z"][0] + 1.5, UKN["z"][1] - 1.5))     # v3.7 · tava → kart kanalı ağzı
    kap = kut(tx0, tx1, ty1, ty1 + 1.5, tz0, tz1)
    for (rx, rz) in RK:                                                # kapakta kablo girişleri (rakorların altında)
        kap = kap.cut(sil((rx, ty1 - 1.0, rz), (rx, ty1 + 3.0, rz), 9.5))
    kap = kap.cut(kut(QK["x"][0], min(tx1, QK["x"][1]), ty1 - 1.0, ty1 + 3.0, QK["z"][0], min(tz1, QK["z"][1])))
    kap = kap.cut(kut(ANA_HAT_QR[-1][0] - 10.0, ANA_HAT_QR[-1][0] + 10.0, ty1 - 1.0, ty1 + 3.0, ANA_HAT_QR[-1][2] - 17.0, ANA_HAT_QR[-1][2] + 17.0))   # v3.7 · ana hat QR (2 kablo)
    ekle("qr_pano_alti_kablo_tavasi", g, "kanal", B2, bom=("Kutu altı kablo tavası 304 1,5 (213 × 35 × 320) + delikli kapak", 1, "lazer + abkant", "üst rafa 4 × perçin · v3.6 QR kutusunun rakorlarına + ana hat QR"))
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
    gk = dis_.cut(ic_).clean()                                                     # v3.6 · giriş (c) (bina beslemesi) kalktı
    ekle("qr_omurga_kanali", gk, "paslanmaz", B2,
         bom=("İç omurga kanalı 304 1,5 · 60 yüksek (toplama kutusu 105 × 40 + sağ köşe 48 × 338 + arka taban 420 × 36) + üst kapak", 1, "lazer + abkant · taban plakasına 6 × perçin",
              "v3.4 · alt dikey kanal → kangalın arkası → kangal ile sağ yan sac arası → tekmelik girişi (b) · kanal içi kablolar çizilmez"))
    ekle("qr_omurga_kanali_kapak", kap_.clean(), "paslanmaz", B2)
    # ---------------- 2c · v3.7 TEKMELİK KALKTI: tam boy alt servis kapağı (2 çentik) + 2 giriş plakası (QR'nin kendi alt paneli) ----------------
    tx0_, tx1_ = TEKME["x"]; tz0_, tz1_ = TEKME["z"]
    xa_ = GIRIS_A["xc"]; ka_, kh_ = GIRIS_A["kesik"]
    xb_ = (GIRIS_B["x"][0] + GIRIS_B["x"][1]) / 2.0; kbw, kbh = GIRIS_B["kesik"]; yb_ = (GIRIS_B["y"][0] + GIRIS_B["y"][1]) / 2.0
    for nm, (px0_, px1_), (cx_, cw_, ch_, cy_) in (("a", PLAKA_A, (xa_, ka_, kh_, GIRIS_A["y"])), ("b", PLAKA_B, (xb_, kbw, kbh, yb_))):
        pl = kut(px0_, px1_, 20.6, PLAKA_Y, tz0_, tz1_).cut(kut(cx_ - cw_ / 2.0, cx_ + cw_ / 2.0, cy_ - ch_ / 2.0, cy_ + ch_ / 2.0, tz0_ - 1.0, tz1_ + 1.0))
        pl = pl.fuse(kut(px0_, px1_, 20.6, 22.1, tz1_, tz1_ + 20.0))                  # alt kulak (taban plakasına 2 × M5)
        ekle("qr_giris_plakasi_%s" % nm, pl.clean(), "paslanmaz", "ELK_QR_MONTAJ",
             bom=("QR alt kablo giriş plakası 304 1,5 + alt kulak (taban plakasına 2 × M5) · a: %.0f × 63 (KEL 10|3) · b: %.0f × 63 (KEL-DPZ 16|14)" % (PLAKA_A[1] - PLAKA_A[0], PLAKA_B[1] - PLAKA_B[0]),
                  2, "lazer + abkant", "v3.7 · tekmelik (alt etek) kalktı · plaka alt kapağın çentiğinde, kapakla aynı düzlemde") if nm == "a" else None)
    kp = kut(tx0_ + 1.0, tx1_ - 1.0, 21.0, KAPI_Y[1], tz0_, tz1_)
    kp = kp.cut(kut(PLAKA_A[0] - 2.0, PLAKA_A[1] + 2.0, 0.0, PLAKA_Y + 2.0, tz0_ - 1.0, tz1_ + 1.0))
    kp = kp.cut(kut(PLAKA_B[0] - 2.0, tx1_ + 1.0, 0.0, PLAKA_Y + 2.0, tz0_ - 1.0, tz1_ + 1.0))
    for i in range(8):                                                     # yarık ızgara 8 × 30 × 70 (y 94–164)
        kp = kp.cut(kut(5090.0 + 40.0 * i, 5120.0 + 40.0 * i, 94.0, 164.0, tz0_ - 1.0, tz1_ + 1.0))
    kp = kp.cut(sil((5300.0, 350.0, tz0_ - 1.0), (5300.0, 350.0, tz1_ + 1.0), 58.0)).cut(sil((5405.0, 234.0, tz0_ - 1.0), (5405.0, 234.0, tz1_ + 1.0), 11.5))
    ekle("servis_kapagi_alt_centikli", kp.clean(), "on_seffaf", "ELK_QR_MONTAJ",
         bom=("Servis kapağı 1,5 mm DKP boyalı · yarık ızgara 30 × 70 (alt 8 · üst 7) + fan deliği Ø116", 2, "855 × 425 (alt, v3.7 tam boy, 2 kablo giriş çentiği) + 855 × 393 (üst)",
              "qr_cad_v1 servis_kapagi_alt yerine · kilit (y 234) ve üst menteşe (y 370) aynı"))
    ekle("servis_mentesesi_0_y50", kut(tx0_, 4590.0, 50.0, 90.0, tz1_, 689.5), "celik", "ELK_QR_MONTAJ",
         bom=("Gizli menteşe (servis kapağı)", 4, "2 kapak × 2", "VARSAYIM · katalog (qr_cad_v1 ile aynı kalem)"))
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
              "membran: 2 × 9–16,2 (H07RN-F 3G2,5) + 2 kör · 3 × 5–10,2 (Cat6A) + 2 kör · 5 × 3,2–6,5 kör (v3.6)", "v3.4 · membran yerleşimi VARSAYIM (güç sağda) · 4 × M5"))
    for ad, r, m, bx, by in B_KABLOLAR:
        ekle("qrk_%s_giris_b_ucu" % ad, boru([(bx, by, 695.0), (bx, by, tz0_ - UC_DIS)], r), m, B2,
             bom=("Ana hat güç kablosu H07RN-F 3G2,5 (Lapp 1600118, Ø10,9–14) · U_F ana pano → QR / ROBOT (Harting fişli)", 2, "", "v3.6") if ad == "guc_QR_3G2_5" else
             (("Veri kablosu Lapp ETHERLINE Cat.6A (2170465, Ø8,7) · ana pano switch → QR / ROBOT + modem", 3, "", "v3.6 · Harting RJ45 modülü / modem RJ45") if ad == "veri_QR_Cat6A" else None))
    # ---------------- 2f · v3.6 GİRİŞ (c) KALKTI: bina beslemesi QR'ye girmez → zemin üstü kanaldan ana panoya (h3_elk_hat_v1) ----------------
    # ---------------- 2g · v3.4 eski taban geçişleri (qr_cad_v1 GECIS_ROBOT Ø40 + GECIS_GUC Ø30, z 975) üstten kapanır ----------------
    ekle("qr_taban_gecis_kapama_saci", kut(4755.0, 4840.0, 20.0, 21.5, 950.0, 1000.0), "paslanmaz", B2,
         bom=("Kapama sacı 304 1,5 · 85 × 50 (eski Ø40 + Ø30 taban geçişleri)", 1, "4 × perçin", "v3.4 · zeminden giriş kalmadı"))
    ukx0, ukx1 = UKN["x"]
    g = kut(ukx0, ukx1, UKN["y"][0], UKN["y"][1], UKN["z"][0], UKN["z"][1]).cut(kut(ukx0 - 1.0, ukx1 - 1.5, UKN["y"][0] + 1.5, UKN["y"][1] + 1.0, UKN["z"][0] + 1.5, UKN["z"][1] - 1.5))
    ekle("qr_kart_kanali", g, "kanal", B2, bom=("Kart kanalı PVC 40 × 30 + kapak (tava → kilit kartı)", 1, "", "üst rafa yapışkan tabanlı klips"))
    ekle("qr_kart_kanali_kapak", kut(ukx0, ukx1, UKN["y"][1], UKN["y"][1] + 1.5, UKN["z"][0], UKN["z"][1]).cut(sil((5320.0, UKN["y"][1] - 1.0, 1015.0), (5320.0, UKN["y"][1] + 3.0, 1015.0), 5.5)),
         "kanal", B2)                                                                                     # v3.7 · modem kablosu çıkışı
    # ---------------- 3 · KANAL DIŞI UÇLAR (kısa · rakora / cihaza dik) ----------------
    for ad, r, rx, rz in QB_RAKOR:
        ekle("qrk_%s_rakor_ucu" % ad, sil((rx, ty1 + 1.5, rz), (rx, y0 + 6.0, rz), r), "kablo", B2)       # tava kapağı → kutu rakoru (dik)
    # v3.6 · ANA HAT QR: Harting fişinin M32 rakorundan tavaya (kutunun sağ yan yüzüne P-kelepçe)
    # v3.7 · QR İÇİ ANA HAT KABLOLARI (gerçek çap): qr_ici_ana_hat() aşağıda (robot Harting kurulduktan sonra)
    # kilit kartı uçları (kart kanalından PCB alt kenarındaki klemenslere) · modem
    for i, xk in enumerate((5160.0, 5200.0, 5240.0, 5280.0)):
        ekle("qrk_kart_ucu_%d" % i, boru([(xk, UKN["y"][1], 1015.0), (xk, 1676.0, 1015.0), (xk, 1676.0, 1060.0)], 3.0), "kablo", B2)
    # v3.7 · modem ucu: modem kablosu QR içi ana hattın parçası (qr_ici_ana_hat)
    # UPS: tavadan UPS'in sol alt yüzüne
    for i, zz in enumerate((820.0, 850.0)):
        ekle("qrk_ups_ucu_%d" % i, boru([(4995.0, ty1 + 1.5, zz), (4995.0, 1700.0, zz), (5005.0, 1700.0, zz)], 4.5), "kablo", B2)
    # v3.6 · ROBOT: denetleyici kutusunun arka yüzünde Harting Han 10B (robot istasyon girişi) → fiş + rakor → alt dikey kanalın yan yüzüne
    HR = EO.harting(ROBOT_HARTING, "+z", "x", t_duvar=1.5)
    DELIKLER.append(("QR", "robot_kontrol_kutusu_REZERV", HR["kesik"], "v3.6 robot Harting Han 10B (soket kesiği + iç modül cebi)"))
    ekle("harting_ROBOT_soket", HR["soket"], "rakor", B2); ekle("harting_ROBOT_fis", HR["fis"], "rakor", B2); ekle("harting_ROBOT_rakoru_M32", HR["rakor"], "rakor", B2)
    u_ = HR["uc"]
    qr_ici_ana_hat(ekle, B2, u_)
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


def qr_ici_ana_hat(ekle, B2, robot_uc):
    """v3.7 · QR içinde 5 ana hat kablosu (gerçek çap): giriş (b) uçları (z 695) → omurga ön kutu → sağ köşe (z ↑) → arka taban (x ←) → alt dikey kanal (y ↑) →
    ROBOT: y 293 / 307'de sola → robot Harting · QR + modem: alt raf → orta dikey kanal → tava → QR: kutu Harting'ine · modem: kart kanalı → modem"""
    R = {"guc_QR_3G2_5": 6.25, "veri_QR_Cat6A": 4.35, "guc_ROBOT_3G2_5": 6.25, "veri_ROBOT_Cat6A": 4.35, "veri_MODEM_Cat6A": 4.35}
    BX = {q[0]: (q[3], q[4]) for q in B_KABLOLAR}
    # kesit konumları: sağ köşe (x, y) · arka taban (y, z) · alt / orta dikey (z) [x 4995]
    KOSE = {"guc_QR_3G2_5": (5388.0, 28.25), "guc_ROBOT_3G2_5": (5402.0, 28.25), "veri_QR_Cat6A": (5386.0, 39.35), "veri_ROBOT_Cat6A": (5397.0, 39.35),
            "veri_MODEM_Cat6A": (5408.0, 39.35)}
    ARKA_Z = {"guc_QR_3G2_5": 1021.0, "guc_ROBOT_3G2_5": 1036.0, "veri_QR_Cat6A": 1019.0, "veri_ROBOT_Cat6A": 1030.0, "veri_MODEM_Cat6A": 1041.0}
    DIK_Z = {"veri_MODEM_Cat6A": 1007.0, "veri_QR_Cat6A": 1019.0, "guc_QR_3G2_5": 1032.0, "veri_ROBOT_Cat6A": 1046.0, "guc_ROBOT_3G2_5": 1060.0}
    KADEME = {"veri_MODEM_Cat6A": 60.0, "veri_QR_Cat6A": 75.0, "guc_QR_3G2_5": 90.0, "veri_ROBOT_Cat6A": 105.0, "guc_ROBOT_3G2_5": 120.0}   # alt kanalda z kaydırma y'si
    xd = (ALT["x"][0] + ALT["x"][1]) / 2.0
    for i, (ad, r) in enumerate(R.items()):
        bx, by = BX[ad]; kx, ky = KOSE[ad]; za = ARKA_Z[ad]; zd = DIK_Z[ad]
        p = [(bx, by, 695.0), (bx, by, 698.0 + 2.0 * i), (kx, by, 698.0 + 2.0 * i), (kx, ky, 698.0 + 2.0 * i), (kx, ky, za), (xd, ky, za), (xd, KADEME[ad], za), (xd, KADEME[ad], zd)]
        if "ROBOT" in ad:
            yr = 293.0 if ad.startswith("veri") else 307.0
            p += [(xd, yr, zd), (xd, yr, 1045.0), (robot_uc[0], yr, 1045.0), (robot_uc[0], yr, robot_uc[2])]
        elif "MODEM" in ad:
            p += [(xd, 1662.0, zd), (xd, 1662.0, 1015.0), (5320.0, 1662.0, 1015.0), (5320.0, 1900.0, 1015.0), (5320.0, 1900.0, 1060.0)]
        else:
            yt, zt = (1671.0, ANA_HAT_QR[0][2] + 7.0) if ad.startswith("veri") else (1682.65, ANA_HAT_QR[0][2] - 7.0)
            xt = ANA_HAT_QR[-1][0]
            p += [(xd, yt, zd), (xd, yt, zt), (xt, yt, zt), (xt, ANA_HAT_QR[1][1], zt), (ANA_HAT_QR[0][0], ANA_HAT_QR[1][1], zt), (ANA_HAT_QR[0][0], ANA_HAT_QR[0][1], zt)]
        ekle("qrk_ana_hat_%s" % ad, boru(p, r), "kablo_veri" if ad.startswith("veri") else "kablo", B2,
             bom=("QR içi ana hat kabloları (giriş → omurga → dikey kanallar → robot / QR Harting · modem) gerçek çap", 5, "", "v3.7") if i == 0 else None)
        if "QR" in ad:
            for j_, yk in enumerate((1960.0, 1780.0)):
                ekle("qrk_ana_hat_%s_kelepce_%d" % (ad, j_), EO.kelepce((ANA_HAT_QR[-1][0], yk, zt), "y", r, QB["x"][1], "-x"), "celik", B2)
        if "MODEM" in ad:
            ekle("qrk_modem_kelepce", EO.kelepce((5320.0, 1800.0, 1015.0), "y", r, 1060.0, "+z"), "celik", B2)


def arayuz():
    """v3.4 · dış kanal arayüzü (h3_elk_hat_v1 buradan alır): kablo uçları (dünya, uç düzlemi z) + çerçeve zarfları"""
    tz0_ = TEKME["z"][0]; zu = tz0_ - UC_DIS
    uc = [(ad, bx, by, zu, 2.0 * r) for ad, r, m, bx, by in B_KABLOLAR]
    xs = [bx - r for ad, r, m, bx, by in B_KABLOLAR] + [bx + r for ad, r, m, bx, by in B_KABLOLAR]
    ys = [by - r for ad, r, m, bx, by in B_KABLOLAR] + [by + r for ad, r, m, bx, by in B_KABLOLAR]
    return dict(b_uclar=uc, b_demet=(min(xs), max(xs), min(ys), max(ys), zu), b_cerceve=(GIRIS_B["x"][0], GIRIS_B["x"][1], GIRIS_B["y"][0], GIRIS_B["y"][1], tz0_ - GIRIS_B["H"], tz0_),
                a_cerceve=(GIRIS_A["xc"] - GIRIS_A["L"] / 2.0, GIRIS_A["xc"] + GIRIS_A["L"] / 2.0, GIRIS_A["y"] - GIRIS_A["W"] / 2.0, GIRIS_A["y"] + GIRIS_A["W"] / 2.0,
                           tz0_ - GIRIS_A["H"], tz0_), tekmelik=(TEKME["x"], TEKME["y"], TEKME["z"]), kapi_y=KAPI_Y)
