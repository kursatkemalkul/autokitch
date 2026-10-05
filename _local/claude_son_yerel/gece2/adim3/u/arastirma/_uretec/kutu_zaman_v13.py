

# ================================================================ E v13 (30 Eyl 2026 · Claude) ================================================================
# kutu_cad_v13 = kutu_cad_v12 + bu ek (yap_kutu_cad_v13.py). Kemal (30 Eyl): "yap işte ne lazımsa" → v12'nin açık listesi:
#  1 · 7 step eksenin SIFIR SENSÖRÜ (4 köşe parmağı · köşe çerçevesi · ön dil · destek tablası) — yerleşim + bayrak + braket, bütün döngüde çakışma yok
#  2 · düşey baskı kafası DÜŞMESİN (SFU1610 geri döner) — frenli motor
#  3 · 13 eksen hareket denetimi (S7-1200'ün 4 PTO'su yetmez) — gerçek denetleyici + sürücüler panoda
#  4 · karton açınımı FEFCO kontrolü (hesap · karton ölçüsü değişmez)
#  (kafa enerji zinciri: Kemal kuralı — enerji zinciri Isaac'ta; burada yalnız "açık — Isaac")
# Kinematik v12 ile BİREBİR (hiçbir hareket süresi değişmez) → K v8/v9 arayüzü (E_HAZIR_GERCEK, DONGU_GERCEK, Z_CATAL_GERCEK) aynı.

M8_SOMUN = dict(af=13.0, t=3.0)                     # Omron E2E-X2MF1 ile gelen M8 somun: 13 anahtar × 3 (araştırma: omron E2E veri sayfası)


def _yon_sil(p0, yon, r, L):
    """p0'dan birim yon (±x/±y/±z) boyunca r yarıçaplı, L boylu silindir"""
    x, y, z = p0
    ax = [i for i in range(3) if abs(yon[i]) > 0.5]
    assert len(ax) == 1, yon
    i = ax[0]; s = 1.0 if yon[i] > 0 else -1.0
    a, b = sorted((p0[i], p0[i] + s * L))
    if i == 0: return silx(y, z, r, a, b)
    if i == 1: return sily(x, z, r, a, b)
    return silz(x, y, r, a, b)


def _yon_altigen(p0, yon, af, L):
    """p0'dan yon boyunca altıgen (anahtar ağzı af) · M8 somun"""
    x, y, z = p0
    i = [k for k in range(3) if abs(yon[k]) > 0.5][0]; s = 1.0 if yon[i] > 0 else -1.0
    a, b = sorted((p0[i], p0[i] + s * L))
    h = cq.Workplane("XY").polygon(6, af / math.cos(math.radians(30))).extrude(b - a)      # z boyunca
    if i == 2: return h.translate((x, y, a))
    if i == 1: return h.rotate((0, 0, 0), (1, 0, 0), -90).translate((x, a, z))
    return h.rotate((0, 0, 0), (0, 1, 0), 90).translate((a, y, z))


SENSOR_V13 = dict(r=4.0, L=30.0, r_bas=3.05, L_bas=6.0, r_kilif=3.0, L_kilif=7.0)
# Omron E2E-X2MF1 (M8 · KORUMASIZ · 2 mm · PNP NO — Beckhoff EL7062 girişleri PNP ister; E2E-X2ME1 NPN): yüzden 6 mm dişsiz baş Ø6,1, sonra M8×1 diş (30'a kadar),
# arkada 7 mm kablo koruması (Ø V). Korumasız sensör: baş metalden ≥ 6 mm çıkık, önünde (hedef dışında) ≥ 8 mm metal yok, yan yana ≥ 60 mm.
SIFIR_BOM = ("Endüktif sıfır sensörü Omron E2E-X2MF1 (M8 · 2 mm · PNP NO · 2 m kablo)", 7, "7 step eksenin referansı (v13) · ayar mesafesi 0–1,6 mm",
             "Omron E2E veri sayfası (araştırma: scratchpad arastirma_e_kontrol.md §4)", "SATIN ALMA")


def _sensor_v13(ad, yuz, yon, grup, plaka=None, bom=None):
    """yüz = algılama yüzünün merkezi · yon = yüzden gövdeye (dışa) · plaka = (yüzden plakanın iç yüzüne uzaklık, kalınlık): iki somun plakayı sıkar
    (iç somun dişli bölgede olmalı: uzaklık ≥ 6 + 3)"""
    if plaka is not None:
        assert plaka[0] - M8_SOMUN["t"] >= SENSOR_V13["L_bas"] - 1e-9, (ad, "iç somun dişsiz başa düşüyor")
    S_ = SENSOR_V13
    govde = _yon_sil(yuz, yon, S_["r_bas"], S_["L_bas"])
    govde = govde.union(_yon_sil(tuple(yuz[k] + yon[k] * S_["L_bas"] for k in range(3)), yon, S_["r"], S_["L"] - S_["L_bas"]))
    govde = govde.union(_yon_sil(tuple(yuz[k] + yon[k] * S_["L"] for k in range(3)), yon, S_["r_kilif"], S_["L_kilif"]))
    ekle(ad, govde, "sensor", grup, bom)
    if plaka is not None:
        d_ic, t_pl = plaka                              # yüzden plakanın iç yüzüne uzaklık, plaka kalınlığı
        for j, d in enumerate((d_ic - M8_SOMUN["t"], d_ic + t_pl)):
            p0 = tuple(yuz[k] + yon[k] * d for k in range(3))
            som = _yon_altigen(p0, yon, M8_SOMUN["af"], M8_SOMUN["t"]).cut(_yon_sil(p0, yon, SENSOR_V13["r"], M8_SOMUN["t"]))
            ekle(ad + "_somun_%d" % j, som, "celik", grup)


def sifir_destek_v13():
    """NEST (destek tablası · Tr16×8 · 45,6 strok): EV = ÜST (nest_dy 45,6 · t 0). Traversin sağ ucuna 2 mm çelik bayrak (x 405–407);
    sensör x ekseninde yandan bakar (yüz x 408 · 1 mm boşluk) — tabla inince bayrak y'de sensörün önünden AŞAĞI çekilir, hiç yaklaşmaz.
    Braket: destek_burc_govde_3'ün sağ yüzüne (x 409,5) L köşebent · dik kolda Ø8,2 delik."""
    y_ev, z_s = 868.6, -206.0                           # travers 865,6–871,6 (evde · NEST dünya = dinlenme + nest_dy, evde 45,6)
    ekle("destek_sifir_bayragi", kut(405.0, 407.0, 865.6 - U_MAX, 871.6 - U_MAX, -214.0, -198.0), "celik", "NEST",
         bom=("Sıfır bayrağı S235 2 mm (travers ucuna 2 × M3)", 1, "E2E algılar: çelik (alüminyum travers ~%50 mesafe verir)", "üretim", "ÜRETİM"))
    br = kut(409.5, 424.0, 877.0, 880.0, -222.0, -190.0).union(kut(421.0, 424.0, 858.0, 880.0, -222.0, -190.0))     # yatay kol somunun (y ≤ 876,1) üstünde
    br = br.cut(silx(y_ev, z_s, 4.1, 420.0, 425.0))
    ekle("destek_sifir_braketi", br, "aluminyum", "SABIT",
         bom=("Sensör köşebendi 6082 · L 3 mm (burç gövdesinin yan yüzüne 2 × M4)", 1, "", "üretim", "ÜRETİM"))
    _sensor_v13("destek_sifir_sensoru", (408.0, y_ev, z_s), (1, 0, 0), "SABIT", plaka=(13.0, 3.0), bom=SIFIR_BOM)


def sifir_kaldirma_v13():
    """CNR_LIFT (köşe çerçevesi · Tr8×8 · 0…60): EV = 0 (alt). Sağ burç gövdesinin dış yüzüne 2 mm çelik bayrak (x 450–452);
    sensör köprüden (PISTON) inen askıda (dik kol x 461–464), yüz x 453 · 1 mm; iç somun x 457–461. Çerçeve kalkınca bayrak y'de yukarı kayar
    (x'te hep ≥ 1 mm). Askı hareketli çerçevenin (x ≤ 444) ve burç gövdesinin (x ≤ 450) DIŞINDA → kaldırma boyunca temas yok."""
    y = H_UST
    y_s, z_s = y + 80.0, -206.0                         # burç gövdesi y+64…+97 (evde)
    ekle("kose_takim_sifir_bayragi", kut(450.0, 452.0, y + 72.0, y + 88.0, -214.0, -198.0), "celik", "CNR_LIFT",
         bom=("Sıfır bayrağı S235 2 mm (burç gövdesine 2 × M3)", 1, "", "üretim", "ÜRETİM"))
    aski = kut(444.0, 465.0, y + 180.0, y + 186.0, -222.0, -190.0).union(kut(462.0, 465.0, y + 70.0, y + 186.0, -222.0, -190.0))
    aski = aski.cut(silx(y_s, z_s, 4.1, 461.0, 466.0))
    ekle("kose_takim_sifir_askisi", aski, "aluminyum", "PISTON",
         bom=("Sensör askısı 6082 · 3 mm (sabit köprünün sağ ucuna 2 × M4)", 1, "", "üretim", "ÜRETİM"))
    _sensor_v13("kose_takim_sifir_sensoru", (453.0, y_s, z_s), (1, 0, 0), "PISTON", plaka=(9.0, 3.0), bom=None)


KOSE_SENSOR_YANI = {'CNR_MF': 1, 'CNR_MB': 1, 'CNR_PF': -1, 'CNR_PB': 1}   # PF dış yanda ön dil küreğinin çubuğu (x 79–83) → iç yan


def sifir_koseler_v13():
    """4 köşe parmağı (NEMA 23 doğrudan kaplinle · EV = −15°, dışa park): kaplinin üstüne sıkma bilezik + radyal çelik bayrak (r 11 → 17 · eksen 96–104);
    sensör motor kelepçesinin yan plakasına (yerel X 24–30, 6 mm, M8 DİŞLİ) vidalanır + dışta kontra somun; yüz r 18 (1 mm) · dişsiz baş r 18–24 (plakadan 6 çıkık). Bayrak evde +X'e bakar, katlamada 105° döner
    (r ≤ 17, yan plakalar r ≥ 24 → temas yok). Parçalar grubun dinlenme konumunda çizilir: evdeki açıya göre geri döndürülür."""
    for g, c in CORNER.items():
        P = c['P']; axis = c['axis']; ex = (c['end'], 0, 0)
        yan = KOSE_SENSOR_YANI[g]                              # +1 dış yan plaka (yerel +X) · −1 iç (yerel −X)
        a0 = c['sign'] * corner_angle(0.0)                     # t 0'da grubun dönüşü (derece · sağ el · eksen c['axis'])
        Pv = cq.Vector(*P); Av = cq.Vector(*axis)

        def dinlenme(wp, Pv=Pv, Av=Av, a0=a0):
            return wp.rotate(Pv, Pv + Av, -a0)
        bil = boru_y(0, 0, 10.0, 8.0, 96.0, 104.0).union(kut(10.0, 17.0, 96.0, 104.0, -1.5, 1.5) if yan > 0 else kut(-17.0, -10.0, 96.0, 104.0, -1.5, 1.5))   # bilezik r 10: yüzden 8 mm (korumasız sensör kuralı)
        ekle('kose_' + g + '_sifir_bayragi', dinlenme(_v10_place(bil, ex, axis, P)), 'celik', g,
             bom=("Sıfır bileziği + bayrak S235 (kaplin üstüne sıkma · r 17)", 4, "köşe parmağı referansı", "üretim", "ÜRETİM") if g == 'CNR_MF' else None)
        kel = next(p for p in PARCALAR if p['ad'] == 'kose_' + g + '_motor_kelepcesi')
        kel['wp'] = kel['wp'].cut(_v10_place(silx(100.0, 0.0, 4.1, 23.0, 31.0) if yan > 0 else silx(100.0, 0.0, 4.1, -31.0, -23.0), ex, axis, P))
        V13_DEGISEN.append(kel['ad'])
        S_ = SENSOR_V13; sg = 1.0 if yan > 0 else -1.0
        def _ar(a, b):
            return (a, b) if sg > 0 else (-b, -a)
        sen = silx(100.0, 0.0, S_["r_bas"], *_ar(18.0, 18.0 + S_["L_bas"])).union(silx(100.0, 0.0, S_["r"], *_ar(18.0 + S_["L_bas"], 18.0 + S_["L"]))).union(
            silx(100.0, 0.0, S_["r_kilif"], *_ar(18.0 + S_["L"], 18.0 + S_["L"] + S_["L_kilif"])))
        ekle('kose_' + g + '_sifir_sensoru', _v10_place(sen, ex, axis, P), 'sensor', 'CNR_LIFT')
        for j, (x0, x1) in enumerate((_ar(30.0, 30.0 + M8_SOMUN["t"]),)):
            som = cq.Workplane("YZ").polygon(6, M8_SOMUN["af"] / math.cos(math.radians(30))).extrude(x1 - x0).translate((x0, 100.0, 0.0))
            som = som.cut(silx(100.0, 0.0, SENSOR_V13["r"], x0 - 1.0, x1 + 1.0))
            ekle('kose_' + g + '_sifir_sensoru_somun_%d' % j, _v10_place(som, ex, axis, P), 'celik', 'CNR_LIFT')


PARMAK_SIFIR = dict(mil_r=3.175, mil_L=15.0, disk_r=15.0, disk_t=1.5, disk_z=8.0, yuz=16.0, yon=0.0)


def sifir_parmak_v13():
    """ÖN DİL katlayıcı (psi −180…0 · EV = −90°) · GT3 20T:20T 1:1 → motor mili = kürek açısı (180° < 360°: tek referans).
    Motor çift milli sürüm: AutomationDirect STP-MTR-23079D (arka mil Ø6,35 [boy V]) · arka mile YARIM DAİRE çelik kam disk (r 15 · 1,5 mm · modelde dönme zarfı:
    tam disk) · E2E-X2MF1 radyal (+x), yüz r 16 (1 mm) · braket motor braketinin dik şeridinden (x 371–377) arkaya. Kürek bölgesine (kolun süpürdüğü alan,
    karton) HİÇ girmez; motorla birlikte FRONT_Y (kafa ötelemesi)."""
    mx, my = 340.0, H_UST + 200.0                         # parmak motoru ekseni (v11: mx, my = 340, H_UST + 200)
    mot = next(q for q in PARCALAR if q["ad"] == "parmak_motoru")
    _ms = mot["wp"].val()
    _kes = _ms.intersect(silz(mx, my, PARMAK_SIFIR["mil_r"], _ms.BoundingBox().zmin - 1.0, _ms.BoundingBox().zmax + 1.0).val())
    zr = _kes.BoundingBox().zmin                          # motor arka yüzü, mil ekseninde (STEP'ten ölçülür)
    b = list(mot["bom"]) if mot["bom"] else ["", 1, "", ""]
    mot["bom"] = ("Step motor AutomationDirect SureStep STP-MTR-23079D (ÇİFT MİLLİ · arka mil sıfır kamı için)", 1, b[2] if len(b) > 2 else "",
                  "automationdirect.com STP-MTR-23079D (arka mil ölçüsü V)")
    V13_DEGISEN.append("parmak_motoru")
    P_ = PARMAK_SIFIR
    z_m1 = zr - P_["mil_L"]
    ekle("parmak_motoru_arka_mili", silz(mx, my, P_["mil_r"], z_m1, zr), "celik", "FRONT_Y")
    zd0 = zr - P_["disk_z"]
    kam = silz(mx, my, P_["disk_r"], zd0 - P_["disk_t"], zd0).union(silz(mx, my, 6.0, zd0 - P_["disk_t"] - 4.0, zd0 + 2.0)).cut(silz(mx, my, P_["mil_r"], z_m1 - 1, zr + 1))
    ekle("parmak_sifir_kami", kam, "celik", "FRONT_Y",
         bom=("Sıfır kamı: arka mile sıkma göbek + YARIM DAİRE S235 1,5 mm r 15 (modelde dönme zarfı)", 1, "ön dil referansı · kenar evde sensörde", "üretim", "ÜRETİM"))
    zs = zd0 - P_["disk_t"] / 2.0
    S_ = SENSOR_V13; f_ = mx + P_["yuz"]
    sen = silx(my, zs, S_["r_bas"], f_, f_ + S_["L_bas"]).union(silx(my, zs, S_["r"], f_ + S_["L_bas"], f_ + S_["L"])).union(
        silx(my, zs, S_["r_kilif"], f_ + S_["L"], f_ + S_["L"] + S_["L_kilif"]))
    ekle("parmak_sifir_sensoru", sen, "sensor", "FRONT_Y", bom=None)
    xb0 = 368.5                                           # braket kolu: motor gövdesinin (x ≤ 368,2) dışında · yüzden 12,5–18,5 (M8 dişli 6 mm) · kontra somun dışta
    br = kut(xb0, xb0 + 6.0, my - 10.0, my + 10.0, zs - 10.0, -5.0).cut(silx(my, zs, S_["r"], xb0 - 1.0, xb0 + 7.0))   # önde motor braketi şeridine/plakasına (z −5) dayanır
    ekle("parmak_sifir_braketi", br, "aluminyum", "FRONT_Y",
         bom=("Sensör kolu 6082 · 6 mm (M8 dişli · motor braketi şeridine 2 × M4)", 1, "", "üretim", "ÜRETİM"))
    som = cq.Workplane("YZ").polygon(6, M8_SOMUN["af"] / math.cos(math.radians(30))).extrude(M8_SOMUN["t"]).translate((xb0 + 6.0, my, zs))
    som = som.cut(silx(my, zs, S_["r"], xb0 + 5.0, xb0 + 10.0))
    ekle("parmak_sifir_sensoru_somun", som, "celik", "FRONT_Y")


def sifir_sensorleri_v13():
    sifir_destek_v13()
    sifir_kaldirma_v13()
    sifir_koseler_v13()
    sifir_parmak_v13()


# ---------------------------------------------------------------- v13 · 13 EKSEN HAREKET DENETİMİ (Beckhoff) ----------------------------------------------------------------
# S7-1200 1214C: en çok 8 konumlama ekseni, yalnız 4'ü darbe/yön; G2: 10 → 13 eksen İÇİN YETMEZ (Siemens veri sayfaları · araştırma §1.1).
# Beckhoff CX9240-0215 (TwinCAT NC PTP · TC1250 + TF5010 ≤ 25 eksen) + EL6631-0010 (PROFINET cihaz → 1214C'nin altında) + 7 × EL7062 (2 eksen · 8–48 V ·
# ≤ 5 A/kanal · 6 A toplam: 2 × 2,8 = 5,6 A) + EL9011 son kapak · STP-MTR-23079 motorlar AYNI · 13 × STP-DRV-4830 KALKAR. Üst DIN rayında x 90'dan.
BECKHOFF_V13 = [("beckhoff_CX9240", 84.0, 91.0, ("Gömülü PC Beckhoff CX9240-0215 (TwinCAT 3 · RT Linux) + TC1250 + TF5010 lisansı", 1,
                                                 "84 × 100 × 91 · 24 V 7 W · E-bus 2 A (yük 1625 mA) · NC PTP ≤ 25 eksen", "beckhoff.com CX9240 · infosys", "SATIN ALMA")),
                ("beckhoff_EL6631-0010", 24.0, 52.0, ("PROFINET cihaz terminali Beckhoff EL6631-0010 (1 kB / 1 kB)", 1, "24 × 100 × 52 · istasyon 1214C = IO denetleyici",
                                                      "beckhoff.com EL6631-0010", "SATIN ALMA"))]
BECKHOFF_V13 += [("beckhoff_EL7062_%d" % i, 24.0, 68.0, ("2 eksen step terminali Beckhoff EL7062 (8–48 V · 5 A/kanal · 6 A toplam · fren çıkışı 24 V 0,5 A)", 7,
                                                        "24 × 100 × 68 · 14 kanal / 13 kullanılır · motor 48 V ön klemensten (2 × NDR-240-48)", "Beckhoff el7062_en.pdf s. 10–11", "SATIN ALMA") if i == 0 else None)
                 for i in range(7)]
BECKHOFF_V13 += [("beckhoff_EL9011", 5.0, 68.0, ("Beckhoff EL9011 son kapak", 1, "5 mm (derinlik V)", "beckhoff.com EL9011", "SATIN ALMA"))]
MALZEME.setdefault('beckhoff', dict(renk=(0.72, 0.73, 0.74, 1.0), met=0.0, ruf=0.6))


def hareket_denetimi_v13():
    n0 = len(PARCALAR)
    PARCALAR[:] = [p for p in PARCALAR if not p["ad"].startswith("surucu_STP-DRV-4830_")]
    assert n0 - len(PARCALAR) == 13, n0 - len(PARCALAR)
    yr0, yr1 = 1697.0, 1732.0                            # üst DIN rayı (din_rayi_1)
    yc = (yr0 + yr1) / 2.0
    z0 = -815.0                                          # ray ön yüzü
    x = 90.0
    for ad, gen, der, bom in BECKHOFF_V13:
        g = kut(x, x + gen, yc - 50.0, yc + 50.0, z0, z0 + der)
        if ad.startswith("beckhoff_EL70") or ad.startswith("beckhoff_EL66"):
            g = g.union(kut(x + 2.0, x + gen - 2.0, yc - 44.0, yc + 44.0, z0 + der, z0 + der + 1.0))      # ön etiket / LED yüzü
        ekle(ad, g, "beckhoff", "SABIT", bom)
        x += gen
    p = next(p for p in PARCALAR if p["ad"] == "plc_S7-1200_1214C")
    p["bom"] = ("PLC Siemens S7-1200 CPU 1214C DC/DC/DC (istasyon denetçisi · PROFINET IO denetleyici)", 1,
                "6ES7214-1AG40-0XB0 · 13 eksen Beckhoff CX9240 + 7 × EL7062 üzerinden (v13)", "110 × 100 × 75", "SATIN ALMA")
    V13_DEGISEN.append("plc_S7-1200_1214C")


# ---------------------------------------------------------------- v13 · KAFA FRENİ (frenli motor) ----------------------------------------------------------------
# SFU1610 (hatve 10) geri döner: kafa (≈ 12 kg [V]) enerji kesilince düşer. Tutma: T = m·g·p / (2π·η) = 12 × 9,81 × 0,01 / (2π × 0,9) = 0,208 N·m · ×2 → 0,42.
# AutomationDirect SureStep'te frenli motor YOK → Oriental Motor PKP268D28M2 (NEMA 23 · 2,8 A · 2,5 N·m · güç kesilince etkin fren 0,8 N·m (× 3,8) ·
# 24 V 0,23 A · EL7062 fren çıkışından · L1 110,5 · mil Ø8 → kasnak deliği 8). Kayış koparsa fren tutmaz (açık).
PKP268 = dict(kare=56.4, pilot_r=19.05, pilot_h=1.6, L1=110.5, L2=92.3, mil_r=4.0, mil_L=20.0, kose=5.0)


def fren_v13():
    ad = "piston_motoru"
    p = next(p for p in PARCALAR if p["ad"] == ad)
    PARCALAR.remove(p)
    x, y, z = 340.0, 1822.0, -318.0                      # flanş ön yüzü (v12 ile aynı) · mil +y · gövde −y
    k = PKP268["kare"] / 2.0
    gov = kut(x - k, x + k, y - PKP268["L2"], y, z - k, z + k).edges("|Y").fillet(PKP268["kose"])
    fren = kut(x - k + 1.0, x + k - 1.0, y - PKP268["L1"], y - PKP268["L2"] + 0.5, z - k + 1.0, z + k - 1.0).edges("|Y").fillet(PKP268["kose"])
    govde = gov.union(fren).union(sily(x, z, PKP268["pilot_r"], y, y + PKP268["pilot_h"])).union(sily(x, z, PKP268["mil_r"], y + PKP268["pilot_h"], y + PKP268["mil_L"]))
    kas = next(q for q in PARCALAR if q["ad"] == "piston_kasnak_motor")
    govde = govde.cut(kas["wp"])                          # mil kasnağın içinde (kasnak deliği Ø8)
    ekle(ad, govde, "motor", "SABIT",
         ("Frenli step motor Oriental Motor PKP268D28M2 (NEMA 23 · 2,5 N·m · fren 0,8 N·m güç kesilince etkin · 24 V 0,23 A)", 1,
          "L1 110,5 (frenli) · mil Ø8 · 1,3 kg · tutma ihtiyacı 0,208 N·m (12 kg [V]) → güvenlik × 3,8", "Oriental Motor PKP katalog s. 37 + 64", "SATIN ALMA"))
    V13_DEGISEN.append(ad)
    kas["bom"] = ("GT3 20T kasnak Ø8 delik (frenli motor mili)", 1, "", "v13", "SATIN ALMA")


# ---------------------------------------------------------------- v13 · VAKUM BESLEME: gerçek parçalar ----------------------------------------------------------------
# araştırma (scratchpad arastirma_e_vakum.md): SMC CDQ2B16-20DZ · 4 × SMC ZP3C-T32CFS-MF-A8 (karton için · düz · yığın üstü sabit YB'de) · SMC ZK2G15K5RWA-08 ·
# Pepperl+Fuchs UDC-18GM-400-3E3 (çift karton, iki kafa, 40–45 mm karşılıklı). Tutma: 4 × 13,9 N = 55,6 N ≫ 7,89 N gerekli (1 g + 4 m/s², μ 0,6, × 2).
def vakum_v13():
    ad = {p["ad"]: p for p in PARCALAR}
    # 1 · silindir CDQ2B16-20DZ: 29 × 29 (köşe pahlı) × 50,5 · mil Ø8 (geri 3,5 çıkık) · M4 · 2 × M5
    cyl = ad["vakum_Z_silindir"]
    cx, cz, cy0 = 410.0, -792.0, 1080.0
    gov = kut(cx - 14.5, cx + 14.5, cy0, cy0 + 50.5, cz - 14.5, cz + 14.5).edges("|Y").chamfer(2.8).cut(sily(cx, cz, 4.1, cy0 - 1, cy0 + 51.5))
    for dd in (-14.0, 14.0):
        gov = gov.cut(sily(cx + dd * 0.707, cz + dd * 0.707, 1.75, cy0 - 1, cy0 + 52))
    gov = gov.union(silx(cy0 + 12.0, cz, 3.0, cx + 14.5, cx + 19.5)).union(silx(cy0 + 38.5, cz, 3.0, cx + 14.5, cx + 19.5))     # M5 portlar
    cyl["wp"] = gov
    cyl["bom"] = ("Kompakt silindir SMC CDQ2B16-20DZ (Ø16 · strok 20 · mıknatıslı · çift etkili)", 1, "29 × 29 × 50,5 · mil Ø8 M4 · 2 × M5 · 87 g · 0,5 MPa 100 N",
                  "SMC CQ2 katalog (araştırma §1)", "SATIN ALMA")
    V13_DEGISEN.append("vakum_Z_silindir")
    mil = ad["vakum_Z_mil_piston"]                        # VAC_Y: M4 uzatma + Ø8 mil (evde en altta · vakum 0)
    mil["wp"] = sily(cx, cz, 4.0, cy0 - 3.5 - VAC_STROKE, cy0 + 20.0).union(sily(cx, cz, 5.0, 1018.0, cy0 - 3.5 - VAC_STROKE))
    mil["bom"] = ("Silindir mili Ø8 + M4 → Ø10 uzatma (başlığa)", 1, "", "SMC + üretim", "SATIN ALMA")
    V13_DEGISEN.append("vakum_Z_mil_piston")
    # 2 · vantuzlar ZP3C-T32CFS-MF-A8: dudak Ø33 (yığın üstü 983,2) · 27,5 yükseklik · M8 × 6,5 diş başlığa (2,3 mm pul)
    for i, (x, z) in enumerate(VAC_POINTS):
        c = ad["vakum_vantuz_%d" % i]
        y0 = VAC_Y0
        hx = cq.Workplane("XY").polygon(6, 14.0 / math.cos(math.radians(30))).extrude(7.0).rotate((0, 0, 0), (1, 0, 0), -90).translate((x, y0 + 20.5, z))
        v = sily(x, z, 16.5, y0, y0 + 6.0).union(sily(x, z, 10.0, y0 + 6.0, y0 + 20.5)).union(hx)
        v = v.cut(sily(x, z, 13.0, y0 - 1.0, y0 + 4.0))
        c["wp"] = v
        c["bom"] = ("Vantuz SMC ZP3C-T32CFS-MF-A8 (Ø32 düz · karton için · aşınmaya dayanıklı · toz süzgeçli)", 4, "dudak Ø33 · 27,5 + M8×6,5 · −60 kPa'da 13,9 N",
                    "SMC ZP3C katalog (araştırma §2)", "SATIN ALMA") if i == 0 else None
        V13_DEGISEN.append(c["ad"])
        s_ = ad["vakum_vantuz_sapi_%d" % i]                # sap yerine: 2,3 mm pul + başlıktaki M8 diş (vantuz başlığa vidalı)
        s_["wp"] = sily(x, z, 8.0, y0 + 27.5, 1013.0).cut(sily(x, z, 4.0, y0 + 26.5, 1014.0))
        s_["bom"] = ("Pul M8 · 2,3 mm (vantuz ↔ başlık)", 4, "", "katalog", "SATIN ALMA") if i == 0 else None
        V13_DEGISEN.append(s_["ad"])
    # dağıtım hattı: dikey kollar başlığın ÜSTÜNDE biter (vantuz M8'in içinden emer) — v12'de başlığı delip 1003'e iniyordu
    tube = silx(1023.0, -765.0, 2.0, 200.0, 650.0)
    for x, z in VAC_POINTS:
        tube = tube.union(silz(x, 1023.0, 2.0, -765.0, z)).union(sily(x, z, 2.0, 1018.0, 1023.0))
    ad["vakum_dagitim_hatti"]["wp"] = tube
    V13_DEGISEN.append("vakum_dagitim_hatti")
    # 3 · vakum ünitesi ZK2G15K5RWA-08: 139 × 15 × 82,9 · traversin üstünde, dik
    vb = ad["vakum_valf_sensor_blogu"]
    vb["wp"] = kut(440.0, 579.0, 1080.0, 1080.0 + 82.9, -815.0, -800.0)
    vb["bom"] = ("Vakum ünitesi SMC ZK2G15K5RWA-08 (ejektör Ø1,5 · besleme + bırakma valfi · vakum anahtarı PNP · sessiz susturucu)", 1,
                 "139 × 15 × 82,9 · −91 kPa · 83 L/dk emme · 0,4 MPa'da 90 L/dk hava · Ø8 vakum portu · 149 g", "SMC ZK2 katalog (araştırma §3)", "SATIN ALMA")
    V13_DEGISEN.append("vakum_valf_sensor_blogu")
    # 4 · çift karton: v12'deki kutu (arabada tek gövde) gerçek bir algılayıcı DEĞİL → kalkar. P+F UDC-18GM-400-3E3 iki kafa ister (karton aralarından
    #     geçmeli, 20–60 mm); şarjör önünde asansör köşebentleri (y 940–972) + kapı eşiği, üstte vakum başlığı bütün taşıma alanını süpürür → AÇIK
    PARCALAR[:] = [q for q in PARCALAR if q["ad"] not in ("vakum_tek_karton_sensor", "vakum_sensor_baglantisi")]


# ---------------------------------------------------------------- v13 · AÇIK ----------------------------------------------------------------
FEFCO_V13 = dict(kod="FEFCO 0426", L=320.0, W=320.0, H=42.0, t=1.6)
FEFCO_V13["acinim"] = (round(2 * FEFCO_V13["W"] + 4 * FEFCO_V13["H"] + 10.8 * FEFCO_V13["t"], 1), round(FEFCO_V13["L"] + 2 * FEFCO_V13["H"] + 4 * FEFCO_V13["t"], 1))
ACIK_V13 = [
    "KARTON AÇINIMI (FEFCO 0426 · EngView şablonu): 320 × 320 × 42 · t 1,6 → %.0f × %.0f; modeldeki 804 × 404 %.0f × %.0f mm KÜÇÜK (katlama payları + kilit dili yok). "
    "Şarjör iç genişliği 827 → 825 açınıma kılavuz payı 1 mm: tedarikçi bıçak izi ŞART; gerekirse E modülü ~850 (hat +20) — KARAR KEMAL'DE"
    % (FEFCO_V13["acinim"][0], FEFCO_V13["acinim"][1], FEFCO_V13["acinim"][0] - 804.0, FEFCO_V13["acinim"][1] - 404.0),
    "kafa üstündeki 6 motorun kablosu: enerji zinciri — AÇIK · Isaac (Kemal kuralı)",
    "karton: gerçek bıçak izi + katlama sonrası geri yaylanma + vakumun gerçek kartonda tuttuğu seviye (sızıntı) fiziksel denenecek",
    "PKP268D28M2 ve STP-MTR-23079'un 48 V · 1500 d/dk torku (kafa 250 mm/s) katalog eğrisinde yok (24 V eğrisi ~900'de biter) — Oriental'den eğri",
    "kayış koparsa motor freni kafayı tutmaz: vida freni (Mayr ROBA-stop-M 2) seçenek",
    "ÇİFT KARTON algılayıcı (P+F UDC-18GM-400-3E3 · iki M18 kafa · karton arada 20–60 mm): şarjör önünde asansör köşebentleri + kapı eşiği, üstte vakum başlığı "
    "taşıma alanını süpürüyor → yer yok; v12'deki arabadaki kutu gerçek algılayıcı değildi, KALDIRILDI — yerleşim fiziksel denemeyle (şimdilik vakum anahtarı + yığın sayacı)",
    "STP-MTR-23079D arka mil boyu (15 V) + ön dil kamının yarım daire kesiti (modelde dönme zarfı tam disk)",
]


_v12_modul_v13 = modul
V13_YENI, V13_DEGISEN = [], []                      # denetim: v13'te eklenen / değişen parçalar (durağan çakışma bunlarda aynı grup dahil taranır)


def modul():
    r = _v12_modul_v13()
    once = set(q["ad"] for q in PARCALAR)
    sifir_sensorleri_v13()
    hareket_denetimi_v13()
    fren_v13()
    vakum_v13()
    V13_YENI[:] = [q["ad"] for q in PARCALAR if q["ad"] not in once and q["ad"] not in V13_DEGISEN]
    return r
