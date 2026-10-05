# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ · K400 — ÜRETİM MODELİ v9 (30 Eyl 2026 · Claude)
Kemal (30 Eyl): "yap işte ne lazımsa" → v8'in açık listesi: PulsaJet gıda uygunluğu · tank gıda + ısıtma · ısıtmalı hortum · seviye sensörü.
TEMEL: kesme_cad_v8 (AYNEN) — yalnız tereyağı sistemi değişir. Kaynak: scratchpad/arastirma_k_sprey.md (Spraying Systems veri sayfası 104210 rev 4,
       Katalog 76 D12, Bülten 711A · Walther Pilot MDG 3 · ifm LMT121 · SSCo 11438-45S · Tempco HEH katalog 11-117).

v8 → v9 · TEREYAĞI SİSTEMİ (gıda sınıfı)
 · v8 bulgusu: PulsaJet -03 + UniJet TG-W KATALOGDA YOK (Katalog 76 s. D4: TG uçları PulsaJet gövdesine takılmaz; TG-2.8W 40 psi'de 0,53 gpm > -03 azamisi 0,47);
   -03'ün gıda beyanı yok (yalnız "CE güvenlik direktifleri"). → Spraying Systems gıda PulsaJet'i AAB10000AUH-104210-VIFC (EC 1935/2004 · FDA Viton ·
   BSPT kodu adlandırma kuralından [V: SSCo teyit]) + UniJet TPU11002 PWMD-SS yassı uç (110° @ 40 psi · 0,20 gpm su → tereyağı ≈ 12 g/s tam açık) +
   CP104218-SS kapak (13/16"). Gövde 38,9 yüksek · 30,1 düzlük · Ø37,8 · kapak + uç 14,4 · 1/8" arka giriş · M8 3 uçlu soket · 24 V 0,36 A · ≤ 93 °C · ≤ 7 bar.
 · YASSI YELPAZE DURAN ÜRÜNÜ ÖRTEMEZ (çizgi) → nozül KAFADAN ALINDI, ÜRÜN GİRİŞİNDE SABİT: yelpaze hattı x 25 (bıçak koruma halkasının dışı, halka x ≥ 46),
   uç ürün üstünden 130 mm yukarıda (110° → 371 mm genişlik > Ø290 ürün), yelpaze z boyunca. Ürün yelpazenin altından BÜTÜNÜYLE geçer: merkez −125 → +175
   (300 mm): son 65 mm fırın bandında (6,27 mm/s · ≈ 10,4 s · ürün ön kenarı K girişine sarkar), kalanı K bandında (0,3 → ≈ 1,9 s). PWM darbe oranı
   ürün hızıyla orantılı (yüzeye düşen doz hızdan bağımsız · hedef ≈ 8 g/ürün [V: deneme]); konum fırın bandı saatinden (sabit hız) + E3Z giriş ışını teyidi.
   Kesim zamanları v8 ile AYNI (4,0'da başlar) — K ↔ E ↔ montaj saatleri değişmez; 2,6–3,8 artık sprey değil, duruş + ışın teyidi.
 · Nozül ısıtması: Spraying Systems'in elektrikli ısıtıcısı YOK (kendi tereyağı sistemleri sıcak su ceketli) → özel alüminyum kelepçe blok + 24 V 20 W
   kartuş ısıtıcı + Pt100 [kartuş ölçüsü V] (hesap kaybı ≈ 2 W · 25 → 45 °C ≈ 140 s).
 · TANK: Walther Pilot MDG 3 **6 bar** sürümü (3 bar yetmez: nozül 2,76 + hortum kaybı + yükseklik ≈ 3,4 bar) · iç Ø125 · gövde Ø129 · flanş Ø173 ·
   toplam 454 (karıştırıcıyla 458) · 3,2 L dolum / 2,5 L kullanılır (2 gün 1,41 L) · pnömatik karıştırıcı tip 46-200 (tereyağı %16–17,5 su → faz ayrılır) ·
   Walther Pilot elektrikli ısıtma manşeti + 20 mm yalıtım [güç V] · hava regülatörü SSCo 11438-45S (316 SS · 1/4" · 0,3–8,5 bar · 69,9 × 38,1).
   v8'de tank 384 yüksek çizilmişti (katalog 454) → düzeltildi.
 · SEVİYE: ifm LMT121 (üreticinin test ortamı listesinde tereyağı · 113 × Ø30 · G1/2 konik · 11 mm prob · FDA / EC 1935/2004 / EHEDG / 3-A) +
   E43300 kaynak adaptörü · gövdenin altına yakın yandan (az kaldı uyarısı).
 · ISITMALI HORTUM: Kletti gıda ısıtmalı hortumu (PTFE FDA iç · silikon dış · Pt100) DN6 — üretici ölçü yayımlamıyor → CAD zarfı Ø28 [V] (K'nın itici
   bölgesinden geçiş 35,5 mm → Ø ≤ 30 şartı · Tempco #4/#6 zarfları Ø35,6/Ø38,1 SIĞMAZ) · bükülme R 80 [V] · 6 mm iç → 12 g/s'de 0,53 bar kayıp (hesap).
   Güzergâh (hep sabit, kafada serbest halka YOK): tank → alt dolap → taban geçişi (x 381, z −540) → sağ duvar boyunca yukarı → y 1210'da −x → sol duvarda
   +z → nozül dirseği.
 · PANO: 3. sıcaklık bölgesi (nozül) → 3. E5DC + DC SSR [V].
KOORDİNAT: v8 ile aynı — x 0…400 (hatta 4000 + x), y yerden, z 0 ön yüz … −830 arka."""
import math
import cadquery as cq
import kesme_cad_v8 as K8
from kesme_cad_v8 import *                      # v8 (ve v7/v6) sabitleri, yardımcıları, PARCALAR, zaman ve denetim işlevleri

KAYNAK_PJ9 = "Spraying Systems veri sayfası 104210 rev 4 + Bülten 711A s. 12–14 (spray.com)"
KAYNAK_UC9 = "Spraying Systems Katalog 76 s. D12 (PWMD) + D4"
KAYNAK_MDG = "walther-pilot.de MDG 3 (ürün sayfası) · karıştırıcı 46-200: modüler tank broşürü s. 2–3"
KAYNAK_LMT = "ifm LMT121 veri sayfası LMT121-01 + kullanma kılavuzu 706158 s. 5 (test ortamları: tereyağı)"
KAYNAK_REG = "Spraying Systems Katalog 76 Aksesuar s. G12–G13 (11438-45S)"

# ---------------------------------------------------------------- v9 sabitleri ----------------------------------------------------------------
PJ9 = dict(duz=30.1, r=18.9, H=38.9, kapak_H=14.4, kapak_af=20.6, uc_r=5.0, uc_L=4.6, m8_ofs=11.1)
X_NZ, Z_NZ = 25.0, -170.0                        # yelpaze hattı (x) · nozül ekseni z (ürün girişte z −170)
Y_UC9 = BANT + PZ_H + 130.0                      # 1141 · uç ürün üstünden 130 (110° → 371 mm yelpaze)
Y_PJ9 = (Y_UC9 + PJ9["kapak_H"], Y_UC9 + PJ9["kapak_H"] + PJ9["H"])    # gövde 1155,4–1194,3
Y_HORTUM = 1210.0                                # ısıtmalı hortum yatay güzergâh ekseni
HORTUM9 = dict(r=14.0, R=80.0)                   # zarf Ø28 [V] · bükülme R 80 [V]
TANK9 = dict(x=200.0, z=-540.0, r_govde=64.5, r_flans=86.5, y0=148.0, h_govde=283.0, h_flans=20.0, h_top=454.0)
X_GECIS9, Z_GECIS9 = 379.5, -540.0               # ısıtmalı hortumun istasyon tabanı geçişi
SPREY_SIL9 = ("PulsaJet_AAB10000AUH-03", "PulsaJet_uc_somunu_CP1325", "PulsaJet_uc_TG-W_2.8W", "PulsaJet_M8_soketi", "PulsaJet_M8_acili_kablo",
              "PulsaJet_giris_dirsegi", "PulsaJet_isitici_ceket", "PulsaJet_braketi", "isitmali_hortum_kafa", "sprey_konisi")
TANK_SIL9 = ("yag_tanki_MDG3", "yag_tanki_kapagi", "yag_tanki_isitici_ceketi", "yag_tanki_regulatoru", "yag_tanki_emniyet_valfi", "yag_tanki_cikis_rakoru",
             "yag_seviye_sensoru", "isitmali_hortum_Ø6", "hortum_baglantisi_kafa", "hortum_baglantisi_askisi", "hava_hortumu_tank", "yag_tanki_ayak_halkasi")
V9_YENI, V9_DEGISEN = [], []


def ekle9(ad, wp, mal="sac", grup="SABIT", bom=None):
    ekle8(ad, wp, mal, grup, bom)
    V9_YENI.append(ad)


def _aci(a, b, c):
    u, w = (a - b).normalized(), (c - b).normalized()
    return math.acos(max(-1.0, min(1.0, u.dot(w))))


def boru_R(pts, r, R, n=6):
    """köşeleri R yarıçaplı yayla yuvarlatılmış boru (yay n parçalı) — esnek hortumun gerçek bükülmesi"""
    V = [cq.Vector(*p) for p in pts]
    yol = [V[0]]
    for i in range(1, len(V) - 1):
        a, b, c = V[i - 1], V[i], V[i + 1]
        u, w = (a - b).normalized(), (c - b).normalized()
        ang = math.acos(max(-1.0, min(1.0, u.dot(w))))                       # iç açı
        if ang > math.pi - 1e-6:
            yol.append(b); continue
        d = R / math.tan(ang / 2.0)
        assert d <= (a - b).Length + 1e-6 and d <= (c - b).Length + 1e-6, ("boru_R: kenar kısa", i, d)
        assert i == 1 or R / math.tan(_aci(V[i - 2], a, b) / 2.0) + d <= (a - b).Length + 1e-6, ("boru_R: ardışık yaylar üst üste", i)
        p1, p2 = b + u * d, b + w * d
        bis = (u + w).normalized()
        mc = b + bis * (R / math.sin(ang / 2.0))                              # yay merkezi
        v1, v2 = p1 - mc, p2 - mc
        th = math.acos(max(-1.0, min(1.0, v1.normalized().dot(v2.normalized()))))
        ax = v1.cross(v2).normalized()
        for k in range(n + 1):
            t = th * k / n
            # Rodrigues: v1'i ax etrafında t döndür
            vr = v1 * math.cos(t) + ax.cross(v1) * math.sin(t) + ax * (ax.dot(v1)) * (1 - math.cos(t))
            yol.append(mc + vr)
    yol.append(V[-1])
    return boru([(p.x, p.y, p.z) for p in yol], r)


# ---------------------------------------------------------------- 1 · KAFADAN SPREY KALKAR ----------------------------------------------------------------
def kafa_v9():
    cikar(*SPREY_SIL9)
    kp = bul("kafa_plakasi_8")                                               # v8'in Ø26 somun deliği kapanır (nozül kafada değil)
    kp["wp"] = kp["wp"].union(sily(XC, ZC, 13.0, Y_KAFA[0], Y_KAFA[1]))
    V9_DEGISEN.append("kafa_plakasi_8")


# ---------------------------------------------------------------- 2 · GİRİŞTE SABİT GIDA NOZÜLÜ ----------------------------------------------------------------
def nozul_v9():
    x, z = X_NZ, Z_NZ
    y0, y1 = Y_PJ9
    gv = sily(x, z, PJ9["r"], y0, y1).intersect(kut(x - PJ9["duz"] / 2.0, x + PJ9["duz"] / 2.0, y0 - 1, y1 + 1, z - 20.0, z + 20.0))
    ekle9("PulsaJet_AAB10000AUH-104210-VIFC", gv, "celik", "SABIT",
          bom=("Gıda sınıfı elektrikli sprey nozülü Spraying Systems AAB10000AUH-104210-VIFC (1/8 BSPT · FDA Viton · EC 1935/2004)", 1,
               "24 VDC 0,36 A · PWM (PLC Q0.0) · ≤ 7 bar · ≤ 93 °C · 0,26 kg · gövde −5° döndürülür (kırlangıç 5° ofset) · BSPT kodu kuraldan [V: SSCo teyit]",
               KAYNAK_PJ9, "SATIN ALMA"))
    ekle9("PulsaJet_kapak_CP104218-SS", hex_y(x, z, PJ9["kapak_af"], Y_UC9 + PJ9["uc_L"], y0), "celik", "SABIT",
          bom=("Uç kapağı Spraying Systems CP104218-SS (13/16\" altıgen · 303 SS)", 1, "kapak yüksekliği [V]", KAYNAK_PJ9, "SATIN ALMA"))
    ekle9("PulsaJet_uc_TPU11002_PWMD", sily(x, z, PJ9["uc_r"], Y_UC9, Y_UC9 + PJ9["uc_L"]), "celik", "SABIT",
          bom=("Yassı uç UniJet TPU11002 PWMD-SS (110° @ 2,76 bar · 0,20 gpm su)", 1, "tereyağı ≈ 12 g/s tam açık (SG düzeltmesi · viskozite düşürür → tartarak kalibre)",
               KAYNAK_UC9, "SATIN ALMA"))
    # M8 soket (arka yüz, eksenden 11,1 +z) + 90° kablo (+z)
    zm = z + PJ9["m8_ofs"]
    ekle9("PulsaJet_M8_soketi_9", sily(x, zm, 4.5, y1, y1 + 8.1), "siyah", "SABIT")
    ekle9("PulsaJet_M8_kablo_9", sily(x, zm, 5.0, y1 + 8.1, y1 + 20.0).union(silz(x, y1 + 15.0, 5.0, zm, zm + 30.0)), "siyah", "SABIT",
          bom=("M8 3 kutuplu 90° dişi kablo 5 m (Spraying Systems 50699-5-S-PUR)", 1, "", KAYNAK_PJ9, "SATIN ALMA"))
    # 1/8 giriş → dirsek → hortum ucu (−z)
    yd = Y_HORTUM
    dirsek = sily(x, z, 6.0, y1, yd).union(silz(x, yd, 6.0, z - 22.0, z)).union(cq.Workplane(obj=cq.Solid.makeSphere(6.0, cq.Vector(x, yd, z))))
    ekle9("PulsaJet_giris_dirsegi_9", dirsek, "celik", "SABIT",
          bom=("Paslanmaz 90° dirsek 1/8 BSPT + süzgeç (SSCo CP12290-7-SS 200 mesh sınıfı)", 1, "", "[V]", "SATIN ALMA"))
    # ısıtıcı kelepçe blok: düzlüklerin arası (x 9,95–40,05) · z ±26 · y 1160–1190 · kartuş (+z) + Pt100 (−z)
    xb0, xb1 = x - PJ9["duz"] / 2.0, x + PJ9["duz"] / 2.0
    kart = silx(1175.0, z + 23.0, 3.25, xb0 + 0.5, xb1 - 0.5)
    pt = silx(1175.0, z - 23.0, 2.0, xb0 + 0.5, xb1 - 0.5)
    blok = kut(xb0, xb1, 1160.0, 1190.0, z - 28.0, z + 28.0).cut(sily(x, z, PJ9["r"], 1159.0, 1191.0)).cut(kart).cut(pt)
    ekle9("nozul_isitici_blogu", blok, "aluminyum", "SABIT",
          bom=("Nozül ısıtıcı kelepçesi 6082 (iki yarım · düzlükleri sarar) + 24 V 20 W kartuş ısıtıcı Ø6,5 × 30 + Pt100 Ø4 × 30", 1,
               "45 °C · kayıp ≈ 2 W (hesap) · E5DC_2 + DC SSR", "üretim + [V: kartuş ölçüsü]", "ÜRETİM"))
    ekle9("nozul_isitici_kartusu", kart, "celik", "SABIT")
    ekle9("nozul_isitici_Pt100", pt, "celik", "SABIT")
    # sol duvara L braket (bloğun −x yüzüne)
    br = kut(1.5, 4.5, 1150.0, 1200.0, z - 30.0, z + 30.0).union(kut(4.5, xb0, 1165.0, 1185.0, z - 30.0, z + 30.0))
    ekle9("nozul_braketi", br, "sac", "SABIT", bom=("Nozül braketi 304 · 3 mm (sol saca 2 × M5 · ısıtıcı bloğa 2 × M4)", 1, "", "üretim", "ÜRETİM"))
    # yassı yelpaze (görsel · yalnız sprey anında): x 25 düzleminde üçgen, uçtan ürün üstüne, 110°
    h = Y_UC9 - (BANT + PZ_H)
    w = h * math.tan(math.radians(55.0))
    fan = cq.Workplane("YZ").polyline([(Y_UC9, z - 3.0), (BANT + PZ_H, z - w), (BANT + PZ_H, z + w), (Y_UC9, z + 3.0)]).close().extrude(4.0).translate((x - 2.0, 0, 0))
    ekle8("sprey_yelpazesi", fan, "sprey", "SPREY")


# ---------------------------------------------------------------- 3 · TANK (alt dolap) ----------------------------------------------------------------
def tank_v9():
    cikar(*TANK_SIL9)
    x, z, y0 = TANK9["x"], TANK9["z"], TANK9["y0"]
    rg, rf = TANK9["r_govde"], TANK9["r_flans"]
    yg1 = y0 + TANK9["h_govde"]                                             # 431 gövde üstü
    yf1 = yg1 + TANK9["h_flans"]                                            # 451 flanş/kapak üstü
    ekle9("yag_tanki_ayak_halkasi_9", sily(x, z, 68.0, 128.0, y0).cut(sily(x, z, 58.0, 127.0, y0 + 1.0)), "sac", "SABIT",
          bom=("Tank oturma halkası 304 · Ø136 / Ø116 × 20 (gövde kenarı üstüne)", 1, "damlama tavasına", "üretim", "ÜRETİM"))
    ys = y0 + 42.0 + 15.0                                                    # seviye sensörü ekseni (y 205)
    xw_o, xw_i = x - rg, x - rg + 2.0                                        # gövde dış / iç yüzü (−x yanı)
    ekle9("yag_tanki_MDG3_6bar", sily(x, z, rg, y0, yg1).cut(sily(x, z, rg - 2.0, y0 + 2.0, yg1 + 1.0)).cut(silx(ys, z, 15.0, xw_o - 1.0, xw_i + 1.0)), "sac", "SABIT",
          bom=("Basınçlı malzeme tankı Walther Pilot MDG 3 · 6 bar sürümü · paslanmaz (1.4404 istenir)", 1,
               "3,2 L dolum / 2,5 L kullanılır (2 gün 1,41 L) · iç Ø125 · flanş Ø173 · toplam 454 · gıda uygunluk beyanı [V: Walther'den istenecek]", KAYNAK_MDG, "SATIN ALMA"))
    ekle9("yag_tanki_kapagi_9", sily(x, z, rf, yg1, yf1), "sac", "SABIT")
    # ısıtma manşeti + yalıtım (gövde çevresi · yandan sensör deliği)
    ym0, ym1 = y0 + 40.0, yg1 - 20.0
    ekle9("yag_tanki_isitma_manseti", sily(x, z, rg + 5.0, ym0, ym1).cut(sily(x, z, rg, ym0 - 1, ym1 + 1)).cut(silx(ys, z, 16.0, xw_o - 10.0, xw_o + 3.0)), "hortum_isi", "SABIT",
          bom=("Walther Pilot elektrikli ısıtma manşeti (termostat + denetleyici) 230 V + Pt100 · 45 °C", 1, "güç [V] · ısınma belirler, tutma ≈ 5–7 W (yalıtımlı)",
               KAYNAK_MDG, "SATIN ALMA"))
    yal = sily(x, z, rg + 25.0, ym0, ym1).cut(sily(x, z, rg + 5.0, ym0 - 1, ym1 + 1))
    yal = yal.cut(silx(ys, z, 16.0, x - rg - 30.0, x - rg + 1.0))
    ekle9("yag_tanki_yalitimi", yal, "yalitim", "SABIT", bom=("Tank yalıtımı: silikon köpük 20 mm (manşet üstü)", 1, "", "[V]", "SATIN ALMA"))
    # seviye: ifm LMT121 (113 = 11 prob içeride + 102 dışarıda) + E43300 kaynak adaptörü (−x yanda, alta yakın · gövde deliğine kaynaklı)
    ekle9("yag_seviye_adaptoru_E43300", silx(ys, z, 15.0, xw_i - 23.0, xw_i).cut(silx(ys, z, 10.0, xw_i - 24.0, xw_i + 1.0)), "celik", "SABIT",
          bom=("ifm E43300 kaynak adaptörü G1/2 – Ø30 (1.4435 · FPM conta)", 1, "adaptör boyu 23 [V]", "ifm E43300 veri sayfası", "SATIN ALMA"))
    lmt = silx(ys, z, 5.5, xw_i, xw_i + 11.0).union(silx(ys, z, 10.0, xw_i - 23.0, xw_i)).union(silx(ys, z, 15.0, xw_i - 79.0, xw_i - 23.0)).union(
        silx(ys, z, 7.0, xw_i - 102.0, xw_i - 79.0))
    ekle9("yag_seviye_sensoru_LMT121", lmt, "sensor", "SABIT",
          bom=("ifm LMT121 nokta seviye sensörü (tereyağı test ortamı · 11 mm prob · G1/2 konik · M12 · IO-Link)", 1,
               "113 × Ø30 · FDA / EC 1935/2004 / EHEDG / 3-A · uç tank duvarından ≥ 15 mm (kılavuz)", KAYNAK_LMT, "SATIN ALMA"))
    # kapak üstü: karıştırıcı (merkez) · regülatör (−x) · emniyet valfi (−z) · çıkış (daldırma borusu, +x) · hava T + akış ayarı (+z)
    ekle9("yag_tanki_karistirici_46-200", sily(x, z, 30.0, yf1, y0 + TANK9["h_top"] + 4.0), "aluminyum", "SABIT",
          bom=("Walther Pilot pnömatik dişli karıştırıcı tip 46-200 (0,16 kW · ≤ 400 d/dk · Ø60 halka pervane)", 1, "faz ayrılmasın (tereyağı %16–17,5 su)",
               KAYNAK_MDG, "SATIN ALMA"))
    reg = kut(x + 32.0, x + 70.1, yf1, yf1 + 38.1, z - 34.95, z + 34.95)
    ekle9("yag_tanki_regulatoru_11438-45S", reg, "celik", "SABIT",
          bom=("Tank hava regülatörü Spraying Systems 11438-45S (316 SS · boşaltmalı · 1/4\" · 0,3–8,5 bar)", 1, "69,9 × 38,1 · 156 g · tank ≈ 3,4 bar", KAYNAK_REG, "SATIN ALMA"))
    ekle9("yag_tanki_manometre", silx(yf1 + 19.05, z, 12.0, x + 70.1, x + 82.0), "celik", "SABIT",
          bom=("Manometre 0–60 psi paslanmaz (SSCo PR00301DFW254D sınıfı)", 1, "", "Spraying Systems ML00MV10HTSYS s. 17 [V]", "SATIN ALMA"))
    ekle9("yag_tanki_emniyet_valfi_9", sily(x, z - 55.0, 8.0, yf1, yf1 + 26.0), "celik", "SABIT",
          bom=("Emniyet valfi (MDG 3 hava giriş takımıyla)", 1, "", KAYNAK_MDG, "SATIN ALMA"))
    ekle9("yag_tanki_cikis_rakoru_9", sily(x - 55.0, z, 8.0, yf1, yf1 + 16.0), "celik", "SABIT",
          bom=("Çıkış rakoru 1/4\" (üst çıkış · daldırma borusu) → hortum ucu", 1, "", KAYNAK_MDG, "SATIN ALMA"))
    ekle9("yag_tanki_hava_T", sily(x, z + 55.0, 7.0, yf1, yf1 + 22.0).union(silx(yf1 + 15.0, z + 55.0, 5.0, x - 30.0, x)), "celik", "SABIT",
          bom=("Hava T + karıştırıcı akış ayar valfi (SMC AS2002F sınıfı)", 1, "karıştırıcı sürekli yavaş döner", "[V]", "SATIN ALMA"))


# ---------------------------------------------------------------- 4 · ISITMALI HORTUM (tank → nozül, sabit) ----------------------------------------------------------------
def hortum_v9():
    x, z, y0 = TANK9["x"], TANK9["z"], TANK9["y0"]
    yf1 = y0 + TANK9["h_govde"] + TANK9["h_flans"]
    r, R = HORTUM9["r"], HORTUM9["R"]
    xo = x - 55.0                                                            # çıkış rakoru (−x)
    yy = 700.0                                                               # alt dolapta yatay geçiş
    pts = [(xo, yf1 + 16.0, z), (xo, yy, z), (X_GECIS9, yy, z), (X_GECIS9, Y_HORTUM, z), (X_NZ, Y_HORTUM, z), (X_NZ, Y_HORTUM, Z_NZ - 22.0)]
    # z = tank ekseni −540 → taban geçişi de −540 (Z_GECIS9)
    assert abs(z - Z_GECIS9) < 1e-9
    ekle9("isitmali_hortum_DN6", boru_R(pts, r, R), "hortum_isi", "SABIT",
          bom=("Isıtmalı gıda hortumu Kletti (PTFE FDA iç · yıkanabilir silikon dış · IP65 · Pt100) DN6", 1,
               "≈ 2,4 m · 45 °C · 12 g/s'de 0,53 bar kayıp (hesap) · CAD zarfı Ø28 / R 80 [V: Kletti çizimi yok — Ø ≤ 30 şartı]", "kletti-gmbh.de [ölçü V]", "SATIN ALMA"))
    # istasyon tabanı geçişi (Ø28 hortum · M40 geçiş)
    tab = bul("istasyon_tabani_3")
    tab["wp"] = tab["wp"].cut(sily(X_GECIS9, Z_GECIS9, r + 2.0, 890.0, 897.0))
    V9_DEGISEN.append("istasyon_tabani_3")
    rk = sily(X_GECIS9, Z_GECIS9, r + 2.0, 895.0, 903.0).union(sily(X_GECIS9, Z_GECIS9, r + 4.0, 885.0, 892.0)).cut(sily(X_GECIS9, Z_GECIS9, r, 884.0, 904.0))
    ekle9("taban_hortum_gecisi_9", rk, "siyah", "SABIT",
          bom=("Lapp SKINTOP MS-SC M40 geçiş rakoru (ısıtmalı hortum · istasyon tabanı)", 1, "", "lapp.com [V]", "SATIN ALMA"))


# ---------------------------------------------------------------- 5 · TANK HAVASI (yeniden güzergâh) ----------------------------------------------------------------
def hava_v9():
    x, z, y0 = TANK9["x"], TANK9["z"], TANK9["y0"]
    yf1 = y0 + TANK9["h_govde"] + TANK9["h_flans"]
    # AW20 çıkışından (manifold öncesi T, v8 ile aynı başlangıç) → arka → sağ duvar (z −596: v8 taban geçişi) → alt dolap → T (kapak, +z)
    ekle9("hava_hortumu_tank_9", boru([(230.0, 1569.6, -792.7), (230.0, 1569.6, -640.0), (230.0, 1398.0, -640.0), (368.0, 1398.0, -640.0), (368.0, 1398.0, -596.0),
                                       (368.0, 630.0, -596.0), (x - 30.0, 630.0, -596.0), (x - 30.0, 630.0, z + 55.0), (x - 30.0, yf1 + 15.0 + 5.0, z + 55.0)], 3.0),
          "hava", "SABIT", bom=("PU hortum Ø6 (Festo PUN-H) · tank + karıştırıcı havası", 1, "", "festo.com PUN-H [V]", "SATIN ALMA"))
    rk = bul("taban_hortum_rakoru")                                         # v8 geçişi: artık yalnız hava (ısıtmalı hortum deliği kalır → kör tapa)
    rk["bom"] = ("Lapp SKINTOP MS-SC M32 çok delikli geçiş rakoru (tank havası · 1 delik kör tapalı)", 1, "", "lapp.com [V]", "SATIN ALMA")


# ---------------------------------------------------------------- 6 · PANO: 3. ısı bölgesi ----------------------------------------------------------------
def pano_v9():
    zr = Z_PL + 7.5
    ekle9("sicaklik_kontrol_E5DC_2", kut(308.0, 330.5, 1712.0, 1808.0, zr, zr + 85.6), "siyah", "SABIT",
          bom=("Omron E5DC DIN ray sıcaklık kontrolcüsü (nozül ısıtıcısı · Pt100)", 1, "22,5 × 96 × 85,6", "omron [V]", "SATIN ALMA"))
    ekle9("SSR_DC_nozul", kut(123.0, 129.0, 1590.0, 1690.0, zr, zr + 80.0), "siyah", "SABIT",
          bom=("DC katı hal rölesi 24 V 2 A (nozül kartuşu 20 W · Omron G3R-ODX02SN sınıfı)", 1, "6 mm ince DIN modül", "[V]", "SATIN ALMA"))
    for ad in ("sicaklik_kontrol_E5DC_0", "SSR_G3PE_0"):
        p = bul(ad)
        b = list(p["bom"]); b[0] = b[0].replace("(tank · hortum)", "(tank manşeti · hortum)").replace("(tank 150 W · hortum)", "(tank manşeti · hortum)"); p["bom"] = tuple(b)


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    K8.modul()
    kafa_v9(); nozul_v9(); tank_v9(); hortum_v9(); hava_v9(); pano_v9()
    return PARCALAR


# ---------------------------------------------------------------- ZAMAN: sprey artık GEÇİŞTE ----------------------------------------------------------------
def _gecis_bitis(xs):
    t = Z_GELIS[0]
    while t < Z_GELIS[1] and state(t)["x"] < xs:
        t += 0.001
    return round(t, 3)


SPREY_X = (X_NZ - 150.0, X_NZ + 150.0)            # ürün merkezi −125 → +175: yelpaze hattının altından bütünüyle geçer (Ø290 + 10 pay)
T_SPREY_FIRIN = round((-60.0 - SPREY_X[0]) / 6.27, 1)   # fırın bandında (6,27 mm/s) −125 → −60: ≈ 10,4 s (K saati 0'dan önce)
Z_SPREY = (Z_GELIS[0], _gecis_bitis(SPREY_X[1]))  # K bandında −60 → +175 (≈ 0,3–1,9 s) · v8: 2,6–3,8 duran üründe (tam koni)
OLAY_ANLARI = tuple(sorted(set(sum((list(a) for a in (Z_GELIS, Z_SPREY, Z_KES, Z_TASI, Z_IN, Z_ITME, Z_DUS, Z_X_DON, Z_Z_DON)), []))))


def sprey_ozeti():
    v_bant = max(abs(state(Z_GELIS[0] + 0.001 * (i + 1))["x"] - state(Z_GELIS[0] + 0.001 * i)["x"]) / 0.001 for i in range(int((Z_SPREY[1] - Z_GELIS[0]) / 0.001)))
    return dict(yelpaze_hatti_x=X_NZ, uc_y=Y_UC9, yukseklik=round(Y_UC9 - BANT - PZ_H, 1), aci=110.0, genislik=round(2 * (Y_UC9 - BANT - PZ_H) * math.tan(math.radians(55)), 1),
                urun_merkez=SPREY_X, firin_bandi_s=T_SPREY_FIRIN, k_bandi=Z_SPREY, k_bandi_tepe_mm_s=round(v_bant, 1),
                pwm_tepe=round(8.0 / (300.0 / v_bant) / 12.0 * 100.0, 1) if v_bant > 0 else None,
                not_="PWM darbe oranı ürün hızıyla orantılı: yüzey dozu sabit (hedef ≈ 8 g/ürün [V])")
