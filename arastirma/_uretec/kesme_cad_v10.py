# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + SIVI YAĞ SPREYİ · K400 — ÜRETİM MODELİ v10 (30 Eyl 2026 · Claude)
Kemal (30 Eyl): "bu yağ tenekesi mi, bunu nasıl çıkaracağız oradan … piyasadaki tenekeyi oraya koyup içine koysak, oradan çekme borularını" → "sıvı yağ · modelle".
TEMEL: kesme_cad_v9 (kesme + gıda PulsaJet girişte sabit AYNEN) — yalnız YAĞ BESLEMESİ değişir. Kaynak: _local/k-v10/katalog_kaynaklari_v10.md.

v9 → v10 · SIVI YAĞ + STANDART TENEKE (ısıtma yok, karıştırıcı yok, basınçlı tank yok)
 · YAĞ: rafine ayçiçek yağı (oda sıcaklığında sıvı) · 15 °C ≈ 85 mPa·s · 25 °C ≈ 55 · 40 °C ≈ 30 · yoğunluk 0,915 (Esteban 2012, Tablo 3–6).
   v9'un Walther Pilot MDG 3 tankı (gıda beyanı yok, 2,5 L → her gün eritip dökme; kapağı karıştırıcı + dalma borusuyla tavana 286 mm kala ÇIKMIYORDU),
   ısıtma manşeti + yalıtımı, karıştırıcı 46-200, SSCo 11438-45S, LMT121, Kletti ısıtmalı hortum, nozül ısıtıcısı, tank havası, 3 × E5DC + 2 × G3PE + DC SSR KALKTI.
 · TENEKE: Türkiye standart 18 L kare yağ tenekesi 235 × 235 × 355 (Bantaş) · 32/42 mm bas-geç ağız (Peksan) · brüt ≈ 17,4 kg (Aysan) · günde 0,6–2,3 kg
   (80 pide … 280 ürün × 8 g [V]) → bir teneke 1–4 hafta. Teneke TARTIDA: HBM PW15AH 50 kg tek noktalı yük hücresi (IP68/69K · C3) + Siemens SIWAREX WP231
   (S7-1200 tartı modülü) → ekranda "kalan yağ", değiştirme uyarısı. Değiştirme: kapak açılır, teneke emme borusuyla birlikte öne çekilir (üstte boru boyu yer yok),
   dışarıda boru yeni tenekeye takılır, geri itilir.
 · EMME: ProMinent 1038304 emme borusu (350 mm · 10–30 L kaplar · PVDF + PTFE · dip valfi · 2 kademeli seviye şalteri) + ağız adaptörü (emme + dönüş) [V].
 · POMPA GRUBU (arka, tavada): 10 µm emiş filtresi [V] → Micropump GJ-N21 + EagleDrive (316 SS · PTFE dişli · 0,5–1500 cP · 24 V) → T (ifm PM1704 gıda basınç
   sensörü · 3-A / EC 1935/2004 / FDA) → Swagelok KBP1F0A4A5A20000 geri basınç regülatörü (0–6,8 bar · ≈ 3,1 bar) → fazlası tenekeye DÖNER.
 · HORTUM: SMC PFA TLM1008 (10 × 8 · FDA 177.1550 · bitkisel yağ listede) emiş + basınç · TLM0806 dönüş · basınç hattı v8'in taban rakorundan (x 380, z −600)
   yukarı → y 1210'da −x → nozül dirseği (≈ 2,5 m · 1 L/dk, 15 °C'de ≈ 0,35 bar kayıp).
 · NOZÜL: v9'un gıda PulsaJet'i + TPU11002 AYNEN (ayçiçek yağı ≈ 12 g/s tam açık · PWM ürün hızıyla) · ısıtıcı blok → düz kelepçe bloğu.
KOORDİNAT: v8/v9 ile aynı — x 0…400 (hatta 4000 + x), y yerden, z 0 ön yüz … −830 arka."""
import math
import cadquery as cq
import kesme_cad_v8 as K8
import kesme_cad_v9 as K9
from kesme_cad_v9 import *                      # v9 (ve v8/v7) sabitleri, yardımcıları, PARCALAR, zaman ve denetim işlevleri

KAYNAK_TENEKE = "bantas.com.tr/yag-tenekeleri (235 × 235 × 355) · peksanplastik.com (32/42 mm ağız) · aysanyaglari.com.tr (brüt 17,4 kg)"
KAYNAK_TARTI = "HBM PW15AH veri sayfası B01815_04 s. 1–4 · Siemens 7MH4960-2AA01 (SIWAREX WP231) veri sayfası"
KAYNAK_POMPA = "Micropump GJ + EagleDrive veri sayfası s. 2, 4 (micropump.com)"
KAYNAK_BPR = "Swagelok MS-02-230 s. 24–25 (KBP1F0A4A5A20000)"
KAYNAK_SENSOR = "ifm PM1704-01 veri sayfası (31.07.2023) s. 1–4"
KAYNAK_LANS = "prominent.com 1038304 emme borusu (350 mm · 10–30 L)"
KAYNAK_HORTUM = "SMC TL/TIL katalog s. 501–514 (TLM1008 / TLM0806 · FDA 177.1550 · bitkisel yağ)"
KAYNAK_YAG = "Esteban vd. 2012, Biomass & Bioenergy 42: 164–171, Tablo 3–6 (ayçiçek yağı ρ, ν)"

# ---------------------------------------------------------------- v10 sabitleri ----------------------------------------------------------------
YAG = dict(ad="rafine ayçiçek yağı", rho=0.915, mu15=85.0, mu25=55.0, mu40=30.5)          # g/cm³ · mPa·s
TENEKE = dict(a=235.0, h=355.0, bos_kg=1.05, net_kg=16.35, agiz_r=21.0, agiz_h=15.0)      # Bantaş 235 × 235 × 355 · Peksan Ø42 bas-geç ağız
TNK = dict(x=(82.5, 317.5), z=(-317.5, -82.5), y0=199.0)                                  # tartı platformu üstünde, kapaktan ≈ 140 mm içeride
TNK_AGIZ = (285.0, -290.0)                                                                # ağız: üst yüzün sağ-arka köşesine yakın
LANS = dict(r=10.0, alt=10.0, sam_r=14.0, sam_h=40.0, kap_r=25.0, kap_h=22.0, port=((275.0, "emis"), (295.0, "donus")))   # [V] boru Ø20 · şamandıra · adaptör
TARTI = dict(taban=(70.0, 330.0, 127.0, 135.0, -330.0, -70.0), hucre=(125.0, 275.0, 145.0, 185.0, -212.5, -187.5), takoz_h=10.0, plat=(70.0, 330.0, 195.0, 199.0, -330.0, -70.0))
TAVA10 = (38.0, 362.0, 126.0, 146.0, -620.0, -60.0)                                      # damlama tavası 304 1,0 (bütün yağ sistemi içinde)
POMPA_Y, POMPA_Z = 174.2, -480.0                                                         # pompa ağız ekseni (GJ: tabandan 44,2) · pompa grubu sırası
PG = dict(plaka=(40.0, 360.0, 127.0, 130.0, -560.0, -400.0), filtre=(80.0, 13.0, 130.0, 230.0), pompa=(100.0, 200.3, 130.0, 210.3, -514.05, -445.95),
          t=(215.0, 235.0, 164.2, 184.2, -490.0, -470.0), sensor=(225.0, 15.1, -470.0, -359.0), bpr=(295.0, 27.5, 130.0, 247.0))
H_BASINC = [(225.0, POMPA_Y, -490.0), (225.0, POMPA_Y, -600.0), (380.0, POMPA_Y, -600.0), (380.0, Y_HORTUM, -600.0), (X_NZ, Y_HORTUM, -600.0), (X_NZ, Y_HORTUM, Z_NZ - 22.0)]
H_EMIS = [(LANS["port"][0][0], None, TNK_AGIZ[1]), (LANS["port"][0][0], 700.0, TNK_AGIZ[1]), (80.0, 700.0, TNK_AGIZ[1]), (80.0, 700.0, POMPA_Z), (80.0, 230.0, POMPA_Z)]
H_DONUS = [(295.0, 247.0, POMPA_Z), (295.0, 660.0, POMPA_Z), (295.0, 660.0, TNK_AGIZ[1]), (LANS["port"][1][0], None, TNK_AGIZ[1])]   # dirsek küresi porttan ≥ 11 mm yukarıda
R_1008, R_0806 = 70.0, 50.0                                                               # bükülme · TLM1008 yakın 65 / önerilen 100 · TLM0806 yakın 40 / önerilen 60
TANK_SIL10 = ("yag_tanki_damlama_tavasi",)                                                # v8'den kalan tank tavası (v9 tank parçaları TANK_SIL9 ile)
ISI_SIL10 = ("sicaklik_kontrol_E5DC_0", "sicaklik_kontrol_E5DC_1", "SSR_G3PE_0", "SSR_G3PE_1")   # v8 ısı bölgeleri (tank + hortum) — ısıtma YOK
V10_YENI, V10_DEGISEN = [], []


def ekle10(ad, wp, mal="sac", grup="SABIT", bom=None):
    ekle8(ad, wp, mal, grup, bom)
    V10_YENI.append(ad)


def teneke_ust():
    return TNK["y0"] + TENEKE["h"]                                                        # 554


# ---------------------------------------------------------------- 1 · NOZÜL: ısıtıcı → düz kelepçe · BOM yağa göre ----------------------------------------------------------------
def nozul_v10():
    cikar("nozul_isitici_blogu", "nozul_isitici_kartusu", "nozul_isitici_Pt100")
    x, z = X_NZ, Z_NZ
    xb0, xb1 = x - PJ9["duz"] / 2.0, x + PJ9["duz"] / 2.0
    blok = kut(xb0, xb1, 1160.0, 1190.0, z - 28.0, z + 28.0).cut(sily(x, z, PJ9["r"], 1159.0, 1191.0))
    ekle10("nozul_kelepce_blogu", blok, "aluminyum", "SABIT",
           bom=("Nozül kelepçesi 6082 (iki yarım · gövde düzlüklerini sarar · 2 × M4)", 1, "v10: ısıtıcı yok (sıvı yağ oda sıcaklığında)", "üretim", "ÜRETİM"))
    p = bul("PulsaJet_AAB10000AUH-104210-VIFC"); b = list(p["bom"])
    b[2] = b[2] + " · v10: rafine ayçiçek yağı (15 °C ≈ 85 mPa·s) · ısıtıcı yok"; p["bom"] = tuple(b); V10_DEGISEN.append(p["ad"])
    p = bul("PulsaJet_uc_TPU11002_PWMD"); b = list(p["bom"])
    b[2] = "ayçiçek yağı ≈ 12 g/s tam açık (0,79 L/dk × 0,915 · SG düzeltmesi; viskozite düşürür → tartarak kalibre)"; p["bom"] = tuple(b); V10_DEGISEN.append(p["ad"])
    p = bul("nozul_braketi"); b = list(p["bom"]); b[0] = b[0].replace("ısıtıcı bloğa", "kelepçe bloğuna"); p["bom"] = tuple(b)


# ---------------------------------------------------------------- 2 · TENEKE + TARTI + DAMLAMA TAVASI ----------------------------------------------------------------
def teneke_v10():
    cikar(*TANK_SIL10)
    x0, x1, y0, y1, z0, z1 = TAVA10
    ekle10("yag_damlama_tavasi_10", kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 + 1.0, z0 + 1.0, z1 - 1.0)), "sac", "SABIT",
           bom=("Yağ damlama tavası AISI 304 1,0 (teneke + tartı + pompa grubu altı)", 1, "%.0f × %.0f × %.0f · köşeler kaynaklı · tabana oturur" % (x1 - x0, z1 - z0, y1 - y0),
                "v10 · bütün yağ sistemi tek tavada (sızıntı istasyon tabanına akmaz)", "ÜRETİM"))
    T = TARTI
    ekle10("yag_tarti_taban_plakasi", kut(*T["taban"]), "sac", "SABIT",
           bom=("Tartı taban plakası AISI 304 8 mm", 1, "260 × 260 · tavaya 4 × lastik ayak", "üretim", "ÜRETİM"))
    hx0, hx1, hy0, hy1, hz0, hz1 = T["hucre"]
    ekle10("yag_tarti_alt_takozu", kut(hx0, hx0 + 40.0, hy0 - T["takoz_h"], hy0, hz0, hz1), "sac", "SABIT",
           bom=("Yük hücresi alt takozu 304 (sabit uç · 2 × M6)", 1, "", "üretim", "ÜRETİM"))
    ekle10("yag_tarti_yuk_hucresi_PW15AH", kut(hx0, hx1, hy0, hy1, hz0, hz1), "celik", "SABIT",
           bom=("Tek noktalı yük hücresi HBM PW15AH 50 kg (1-PW15AHC3/50KG-1 · C3 · IP68/IP69K · 1.4545 paslanmaz)", 1,
                "150 × 25 × 40 (çizimden [V: CAD]) · platform ≤ 500 × 400 · dolu teneke 17,4 + platform ≈ 2,1 kg → aralığın %%39'u · doğrulama aralığı 5 g", KAYNAK_TARTI, "SATIN ALMA"))
    ekle10("yag_tarti_ust_takozu", kut(hx1 - 40.0, hx1, hy1, hy1 + T["takoz_h"], hz0, hz1), "sac", "SABIT",
           bom=("Yük hücresi üst takozu 304 (yük ucu · platform 2 × M6)", 1, "", "üretim", "ÜRETİM"))
    ekle10("yag_tarti_platformu", kut(*T["plat"]), "sac", "SABIT",
           bom=("Tartı platformu AISI 304 4 mm (kenarları 5 mm kıvrık · teneke kayarak girer)", 1, "260 × 260 · merkez = yük hücresi merkezi", "üretim", "ÜRETİM"))
    # teneke (kare, üstte ağız) · ağızdan emme borusu (dip valfi + şamandıra) · ağız adaptörü (emme + dönüş portu)
    a, h = TENEKE["a"], TENEKE["h"]
    (tx0, tx1), (tz0, tz1), ty0 = TNK["x"], TNK["z"], TNK["y0"]
    yu = teneke_ust()
    ax, az = TNK_AGIZ
    kab = kut(tx0, tx1, ty0, yu, tz0, tz1).cut(kut(tx0 + 0.3, tx1 - 0.3, ty0 + 0.3, yu - 0.3, tz0 + 0.3, tz1 - 0.3))
    kab = kab.cut(sily(ax, az, TENEKE["agiz_r"] - 2.0, yu - 1.0, yu + 1.0))
    agiz = sily(ax, az, TENEKE["agiz_r"], yu, yu + TENEKE["agiz_h"]).cut(sily(ax, az, TENEKE["agiz_r"] - 2.0, yu - 1.0, yu + TENEKE["agiz_h"] + 1.0))
    ekle10("yag_tenekesi_18L", kab.union(agiz), "celik", "SABIT",
           bom=("Standart 18 L kare yağ tenekesi (piyasa · rafine ayçiçek yağı 16,35 kg net · 17,4 kg brüt)", 1,
                "235 × 235 × 355 · Ø42 bas-geç ağız (Peksan 042.021) · günde 0,6–2,3 kg [V] → 1–4 hafta · tartıda (kalan yağ ekranda)", KAYNAK_TENEKE, "SARF"))
    ly0, ly1 = ty0 + LANS["alt"], yu + TENEKE["agiz_h"]
    lans = sily(ax, az, LANS["r"], ly0, ly1).cut(sily(ax, az, LANS["r"] - 2.0, ly0 + 5.0, ly1 + 1.0))
    lans = lans.union(sily(ax, az, LANS["sam_r"], ly0 + 20.0, ly0 + 20.0 + LANS["sam_h"]).cut(sily(ax, az, LANS["r"], ly0 + 19.0, ly0 + 21.0 + LANS["sam_h"])))
    ekle10("yag_emme_lansi_1038304", lans, "pom", "SABIT",
           bom=("Emme borusu ProMinent 1038304 (350 mm · 10–30 L kap · PVDF + PTFE · dip valfi + süzgeç · 2 kademeli seviye şalteri NC)", 1,
                "dış Ø20 [V] · şalter: 1. kademe 'az kaldı', 2. kademe 'boş' → pompa durur (kuru çalışmaz) · tartının yedeği", KAYNAK_LANS, "SATIN ALMA"))
    kap = sily(ax, az, LANS["kap_r"], ly1, ly1 + LANS["kap_h"]).cut(sily(ax, az, LANS["r"], ly1 - 1.0, ly1 + 5.0))
    for px, _k in LANS["port"]:
        kap = kap.union(sily(px, az, 5.0 if _k == "emis" else 4.0, ly1 + LANS["kap_h"], ly1 + LANS["kap_h"] + 8.0))
    ekle10("yag_agiz_adaptoru", kap, "pom", "SABIT",
           bom=("Teneke ağız adaptörü POM-C (Ø42 bas-geç ağza · emme borusu + dönüş portu · havalandırma filtreli)", 1, "Ø50 × 22 + 2 hortum ucu [V]", "üretim", "ÜRETİM"))


# ---------------------------------------------------------------- 3 · POMPA GRUBU (arka) ----------------------------------------------------------------
def pompa_v10():
    ekle10("yag_pompa_plakasi", kut(*PG["plaka"]), "sac", "SABIT",
           bom=("Pompa grubu plakası AISI 304 3 mm", 1, "320 × 160 · tavaya 4 × M5 (lastik)", "üretim", "ÜRETİM"))
    fx, fr, fy0, fy1 = PG["filtre"]
    ekle10("yag_emis_filtresi", sily(fx, POMPA_Z, fr, fy0, fy1), "celik", "SABIT",
           bom=("Emiş filtresi 10 µm, 316 SS, 1/4\" (pompa girişi · üretici şartı ≤ 10 µm)", 1, "Ø26 × 100 [V: parça no]", "[V]", "SATIN ALMA"))
    ekle10("yag_boru_filtre_pompa", silx(POMPA_Y, POMPA_Z, 3.175, fx + fr, PG["pompa"][0]), "celik", "SABIT")
    px0, px1, py0, py1, pz0, pz1 = PG["pompa"]
    ekle10("yag_pompasi_GJ-N21_EagleDrive", kut(px0, px1, py0, py1, pz0, pz1), "motor", "SABIT",
           bom=("Dişli pompa Micropump GJ-N21 + EagleDrive DEMSE (85222-DEMSE) · 316 SS · PTFE dişli · PTFE conta · 0,316 mL/dev", 1,
                "100,3 × 80,3 · ayak 77,5 × 68,1 · 10–38 VDC (24 V, 2 A) · 0,5–1500 cP · 2,8 bar'da 600 mL/dk @ 3 V (su) · ≤ 5,6 bar fark · ≈ 1 L/dk için ≈ 3170 d/dk · ürün yaklaşınca çalışır",
                KAYNAK_POMPA + " · yağ için gıda beyanı [V]", "SATIN ALMA"))
    tx0, tx1, ty0, ty1, tz0, tz1 = PG["t"]
    ekle10("yag_boru_pompa_T", silx(POMPA_Y, POMPA_Z, 3.175, px1, tx0), "celik", "SABIT")
    ekle10("yag_T_parcasi", kut(tx0, tx1, ty0, ty1, tz0, tz1), "celik", "SABIT",
           bom=("T parçası 316 SS 1/4\" (sensör + basınç hattı + regülatör)", 1, "", "[V]", "SATIN ALMA"))
    sx, sr, sz0, sz1 = PG["sensor"]
    ekle10("yag_basinc_sensoru_PM1704", silz(sx, POMPA_Y, sr, sz0, sz1), "sensor", "SABIT",
           bom=("Gıda basınç sensörü ifm PM1704 (−1…10 bar · 4–20 mA + IO-Link · 3-A · EC 1935/2004 · EHEDG · FDA · IP69K)", 1,
                "Ø30,2 × 111 · G1 Aseptoflex adaptörle [V: adaptör no] · PLC basıncı izler (düşerse: teneke bitti / hortum)", KAYNAK_SENSOR, "SATIN ALMA"))
    bx, br, by0, by1 = PG["bpr"]
    ekle10("yag_boru_T_regulator", silx(POMPA_Y, POMPA_Z, 3.175, tx1, bx - br), "celik", "SABIT")
    ekle10("yag_geri_basinc_regulatoru_KBP", sily(bx, POMPA_Z, br, by0, by1), "celik", "SABIT",
           bom=("Geri basınç regülatörü Swagelok KBP1F0A4A5A20000 (0–6,8 bar · Cv 0,20 · 1/4\" FNPT · 316 SS · FKM)", 1,
                "Ø55 × 117 · 1,1 kg · ≈ 3,1 bar (nozülde ≈ 2,8) · fazlası tenekeye döner · gıda beyanı [V]", KAYNAK_BPR, "SATIN ALMA"))


# ---------------------------------------------------------------- 4 · HORTUMLAR ----------------------------------------------------------------
def _yol(pts):
    ay = teneke_ust() + TENEKE["agiz_h"] + LANS["kap_h"] + 8.0                            # adaptör portlarının ucu
    return [(x, ay if y is None else y, z) for x, y, z in pts]


def hortum_v10():
    ekle10("yag_basinc_hortumu_TLM1008", boru_R(H_BASINC, 5.0, R_1008), "hortum_yag", "SABIT",
           bom=("Basınç hattı SMC TLM1008 PFA 10 × 8 (FDA 177.1550 · bitkisel yağ listede) + LQ rakorlar", 1,
                "≈ %.1f m · 8 mm iç: 1 L/dk, 15 °C'de ≈ 0,14 bar/m → ≈ %.2f bar kayıp · bükülme R %.0f (yakın 65 / önerilen 100) · v8'in taban rakorundan (x 380, z −600)"
                % (_boy(H_BASINC) / 1000.0, 0.14 * _boy(H_BASINC) / 1000.0, R_1008), KAYNAK_HORTUM, "SATIN ALMA"))
    ekle10("yag_emis_hortumu_TLM1008", boru_R(_yol(H_EMIS), 5.0, R_1008), "hortum_yag", "SABIT",
           bom=("Emiş hattı SMC TLM1008 PFA 10 × 8 + CPC PLCD130M10 / PLCD200M10 çabuk bağlantı (teneke değişiminde)", 1,
                "≈ %.1f m · servis halkası: teneke öne çekilirken hortum gerilmez · bükülme R %.0f" % (_boy(_yol(H_EMIS)) / 1000.0, R_1008), KAYNAK_HORTUM + " · CPC PLC katalog s. 44–47", "SATIN ALMA"))
    ekle10("yag_donus_hortumu_TLM0806", boru_R(_yol(H_DONUS), 4.0, R_0806), "hortum_yag", "SABIT",
           bom=("Dönüş hattı SMC TLM0806 PFA 8 × 6 (regülatör → teneke)", 1, "≈ %.1f m · bükülme R %.0f (yakın 40 / önerilen 60)" % (_boy(_yol(H_DONUS)) / 1000.0, R_0806), KAYNAK_HORTUM, "SATIN ALMA"))
    rk = bul("taban_hortum_rakoru")
    rk["bom"] = ("Lapp SKINTOP MS-SC M32 geçiş rakoru (v10: yağ basınç hattı Ø10 PFA · küçültme contası · 2. delik kör tapalı)", 1, "", "lapp.com [V]", "SATIN ALMA")
    V10_DEGISEN.append("taban_hortum_rakoru")


def _boy(pts):
    return sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))


# ---------------------------------------------------------------- 5 · PANO: ısı bölgeleri kalkar · tartı modülü ----------------------------------------------------------------
def pano_v10():
    cikar(*ISI_SIL10)
    zr = K8.Z_PL + 7.5
    ekle10("plc_tarti_modulu_SIWAREX_WP231", kut(260.0, 330.0, 1710.0, 1810.0, zr, zr + 75.0), "siyah", "SABIT",
           bom=("Siemens SIWAREX WP231 tartı modülü 7MH4960-2AA01 (S7-1200 yan modül · 24 V · RS485 / Ethernet)", 1,
                "70 × 100 × 75 · 280 g · PW15AH (2 mV/V, 300–500 Ω) giriş aralığında · E5DC'lerin yerinde", KAYNAK_TARTI, "SATIN ALMA"))


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    K8.modul()
    K9.kafa_v9(); K9.nozul_v9()
    cikar(*TANK_SIL9)                                                                     # v8 tank + ısıtmalı hortum + tank havası (v9'da da kalkıyordu)
    nozul_v10(); teneke_v10(); pompa_v10(); hortum_v10(); pano_v10()
    return PARCALAR


YOGUNLUK.update(hortum_yag=2.15e-6, motor=3.0e-6)                                        # PFA · pompa + sürücü (ortalama)
MALZEME.setdefault("hortum_yag", dict(renk=(0.93, 0.78, 0.32, 0.80), met=0.0, ruf=0.35, saydam=True))   # yağ dolu yarı saydam PFA
MALZEME.setdefault("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45))
