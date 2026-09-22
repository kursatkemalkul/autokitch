# -*- coding: utf-8 -*-
"""AUTOKITCH · TOPPING MODÜLÜ — HESAP v1 (22 Eyl 2026)
Kemal: "bunlar niye bu kadar önde, birde arka kısımlarını o motor yerlerini — bu TOPPING'i full tasarla, üretime yönelik."
1 numaralı kural: her şey hesaplanacak. Model (topping_cad_v8.py) bu dosyadan OKUR, sayı iki yerde yazılmaz.

KAYNAKLI olanlar satır sonunda [K], varsayımlar [V] ile işaretli.

v2 (22 Eyl 2026) — Kemal: "kasetleri geri it, arkada bosluk olmasin; kalinliklari dogru ayarla;
sadece kasetlerin oldugu kisim sogutuculu; kablolar motorun yanindan gider."
Kuru bolme 320 -> 200 (gercek tahrik zinciri + kablo payi). Acilan 120 mm one gecti: ON NIS.
Kaset 120 mm geriye gitti, cikis agzi o kadar iceri geldi. Nis YALITIMSIZ, sogutulan hacme girmiyor.
v3 (22 Eyl 2026): urun dusme mesafesi hesaba girdi (huni bacasi), kaset alti bosluk 20 -> 10.
v4 (22 Eyl 2026): DONER TABLA hesabi eklendi — x ekseni stroku/hizi, tabla devri, dikey dizilim.
"""
import io, json, math, os

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))

# ---------------------------------------------------------------- 1 · DERİNLİK DİZİLİMİ (Kemal: "niye bu kadar önde") ----------------------------------------------------------------
# Kaset ÖN YÜZÜ z = 0'daydı; kulp öne 48 mm taştığı için kaset kabinden dışarı fırlıyordu. Üretimde kapak kapanmaz.
# Yeni dizilim (z = 0 modülün ön yüzü, içeri doğru eksi):
ON_KAPAK = 20.0          # kaset ağzını kapatan ön kapak: sandviç 1,5 sac + 17 PU + 1,5 sac [V]
TUP_TASMA = 84.0              # kasetin CIKIS TUPU on yuzden bu kadar tasiyor [kusbasi_cad_v4: TUP_Z1 246,5 - D/2 162,5]
KULP_BOS = TUP_TASMA + 12.0   # v2: 60 mm yazilmisti ama TUP 84 tasiyor - agiz on kapagin icine giriyordu (cakisma taramasi yakaladi)
KASET_D = 325.0          # kaset derinliği (dört kasette de aynı)
KAVRAMA = 40.0           # kasetin arkasındaki haç kavrama + yaylı soketin yolu [V: soket kursu 12]
ARKA_PU = 65.0           # soğuk hücrenin arka yalıtımı: 1,5 sac + 60 PU + 1,0 sac + 2,5 pay
DZ = 830.0
# z dizilimi bölüm 2'nin sonunda kurulur: kuru bölmenin derinliği motor + redüktör ölçüsünden ÇIKAR,
# yuvarlak bir sayı olarak kabul edilmez (Kemal: "arkada boşluk olmasın").

# ---------------------------------------------------------------- 2 · TAHRİK: motor seçimi ----------------------------------------------------------------
# Her kasette İKİ mil döner: helezon (dozaj) + besleme rotoru (karıştırıcı). Devirler kasetlerin kendi akış modellerinden:
DEVIR = {"KAŞAR KABI": (42.0, 6.0), "KIYMA": (14.0, 4.0), "KUŞBAŞI": (13.0, 4.0), "SUCUK": (8.0, 4.0), "HARÇ": (14.0, 4.0)}   # (helezon, rotor) dev/dk
T_CALISMA = 0.25         # ölçülen/hesaplanan çalışma torku, N·m — kuşbaşı modelinde 0,23 [K: kusbasi_akis_model]
T_SIKISMA = 3.0          # sıkışmada akım sınırı — bunun üstüne çıkmamalı [V, kuşbaşı modelinden]
EMNIYET = 2.0            # tasarım emniyet katsayısı [V]
T_TASARIM = T_SIKISMA * EMNIYET                                               # 6 N·m çıkışta
ORAN = 10.0              # planet redüktör i = 10 [katalog PLF60/PLE60 sınıfı]
VERIM = 0.90             # planet redüktör verimi [K: planet redüktör tipik %90-97]
T_MOTOR = T_TASARIM / ORAN / VERIM                                            # motorda gereken tork
RPM_MAX = max(v[0] for v in DEVIR.values())                                   # 42 dev/dk çıkış
RPM_MOTOR = RPM_MAX * ORAN                                                    # 420 dev/dk motor
GUC = T_TASARIM * (RPM_MAX * 2 * math.pi / 60.0)                              # W (çıkışta)

# NEDEN PLANET, NEDEN SONSUZ VİDA DEĞİL:
#   NMRV030 sonsuz vida redüktörde giriş ekseni çıkışa DİKTİR → motor yana/yukarı taşar. İki motor yana bakınca 131 mm
#   yer ister, 140'lık kasetin arkasında komşuya giriyordu (eski açık iş). Planet redüktör EŞ EKSENLİDİR: motor mille
#   aynı hizada, arkaya doğru dizilir; 140 mm genişliğe iki katı da sığar.
MOTOR = dict(ad="NEMA23 kapalı çevrim step", g=57.0, y=57.0, z=76.0, tork=1.2)     # [katalog: NEMA23 57 mm gövde, 1,2 N·m]
REDUKTOR = dict(ad="Planet redüktör i=10", cap=60.0, z=60.0)                        # [katalog: PLF60/PLE60 sınıfı]
YATAK = dict(cap_dis=42.0, cap_ic=22.0, z=12.0)                                     # 6004 sınıfı [katalog]
KECE = dict(cap_dis=35.0, cap_ic=22.0, z=7.0)                                       # 22×35×7 mil keçesi [katalog]
TAHRIK_Z = KAVRAMA + 18.0 + YATAK["z"] + KECE["z"] + ARKA_PU + 25.0 + REDUKTOR["z"] + MOTOR["z"]   # toplam derinlik ihtiyacı

# ---------------------------------------------------------------- 2b · DERİNLİK DİZİLİMİ (v2) ----------------------------------------------------------------
# KURU BÖLME artık ölçülerek çıkıyor: yalıtımdan çıkan mil ucu + redüktör + motor + kablo payı.
# v1'de 320 mm yazılmıştı, motorun arkasında 142 mm boşluk kalıyordu (Kemal gördü).
MIL_UCU = 40.0           # arka PU'dan çıkan mil + yatak/keçe kovanı [V: kovan 38 + 2 pay]
KABLO_PAY = 24.0         # motor arkası: konnektör + kablo kıvrımı. Kablolar motorun YANINDAN gider (Kemal) [V]
KURU_D = MIL_UCU + REDUKTOR["z"] + MOTOR["z"] + KABLO_PAY                     # 40 + 60 + 76 + 24 = 200
# Artan derinlik ÖNE geçer: kaset geriye gider, önünde açık NİŞ kalır → çıkış ağzı modülün içine girer.
ON_NIS = DZ - (ON_KAPAK + KULP_BOS + KASET_D + KAVRAMA + ARKA_PU + KURU_D)    # 830 − 710 = 120
assert ON_NIS >= 0.0, "derinlik dizilimi 830'a sığmıyor: %.0f mm taşıyor" % (-ON_NIS)
Z_NIS = (0.0, -ON_NIS)                                                        #    0 … −120  YALITIMSIZ (soğuk değil)
Z_KAPAK = (Z_NIS[1], Z_NIS[1] - ON_KAPAK)                                     # −120 … −140
Z_KASET = (Z_KAPAK[1] - KULP_BOS, Z_KAPAK[1] - KULP_BOS - KASET_D)            # −200 … −525
Z_KAVRAMA = (Z_KASET[1], Z_KASET[1] - KAVRAMA)                                # −525 … −565
Z_BOLME = (Z_KAVRAMA[1], Z_KAVRAMA[1] - ARKA_PU)                              # −565 … −630   (soğuk / kuru ayırıcı)
Z_KURU = (Z_BOLME[1], -DZ)                                                    # −630 … −830   kuru makine bölmesi (200 mm)
# Mil eksenleri kasetin kendi eksenleridir (kaset üreteçlerinden okunur): 140 sınıfı CY 60 / YC 164 · kaşar CY 40 / YC 195

# ---------------------------------------------------------------- 2c · ÜRÜN DÜŞME MESAFESİ (v3) ----------------------------------------------------------------
# Kemal: "nozzle uzun yap ki pideyle arasındaki en doğru mesafe olsun."
# Ürün kasetin ağzından çıkıp pidenin üstüne düşüyor. Düşme ne kadar uzun olursa tane o kadar saçılır;
# ne kadar kısa olursa meme pideye/robota çarpma riski o kadar artar.
DUSME = 40.0             # meme/baca ağzı ile pide üst yüzü arası [V: kuşbaşı 10–15 mm küp için 30–50 mm;
#                          tartılmadı, prototipte saçılma ölçülecek]
KASET_ALTI = 10.0        # kaset tabanı ile iç kabuk tabanı arası boşluk — v2'de 20'ydi (Kemal: "neden bu kadar kalın")
# Alt paketin geri kalanı ZORUNLU: PU 60 (yalıtım hesabı buna dayanıyor) + iç kabuk 1 + taban rayı 4.

# ---------------------------------------------------------------- 2d · DÖNER TABLA (v4) ----------------------------------------------------------------
# Kemal: "altına Atosa gibi tabla yapacağız; her kasetin çıkış yerine denk gelecek, ona göre kendini
# ayarlayıp dönerken ilerleyecek." Kasetlerin akış modelleri ZATEN tablalı düzene göre çözülmüştü.
PIDE_R, KENAR = 140.0, 15.0        # [kasar_akis_model_v2] pide yarıçapı · kaplanmayan kenar
T_DOZ = 10.0                       # [kasar_akis_model_v2 · T_DOK] bir dozun süresi
TABLA_RPM = 35.0                   # [kusbasi_akis_model_v2 · dagilim(n_tabla=35)] tabla devri
R_DIS, R_IC = 105.0, 20.0          # [kasar_akis_model_v2 · YASA] ağzın pide merkezine uzaklığı: dıştan içeri
TABLA_D = 340.0                    # tepsi Ø340 ile aynı; merkezleme 3 pimle (bilezik modülün ön yüzünden taşıyordu)
TEPSI_K, TABLA_K, HAMUR_K = 12.0, 14.0, 8.0                                  # tepsi · tabla · hamur kalınlıkları [V]

DOZ_STROK = R_DIS - R_IC                                                     # dozaj sırasında x'te kayma = 85 mm
TUR_DOZ = TABLA_RPM * T_DOZ / 60.0                                           # bir dozda tabla kaç tur döner = 5,83
SERIT_ARA = DOZ_STROK / TUR_DOZ                                              # her turda içeri kayma = 14,6 mm
X_DOZ_HIZ = DOZ_STROK / T_DOZ                                                # dozajda araba hızı = 8,5 mm/s
X_GECIS_HIZ = 200.0                                                          # yuvadan yuvaya [V: lineer kızakta rahat]
# Strok: ilk ve son yuva merkezi arası + dozaj salınımı + robotun tepsiyi bıraktığı yükleme noktası
YUVA_ACIKLIK = 1075.0                                                        # topping_cad YUVA merkezlerinden ölçüldü
X_STROK = YUVA_ACIKLIK + R_DIS + 120.0                                       # 1300 mm

# ---------------------------------------------------------------- 3 · SOĞUTMA YÜKÜ ----------------------------------------------------------------
IC = dict(g=1740.0, y=380.0, z=KULP_BOS + KASET_D + KAVRAMA)   # v2: SOĞUTULAN derinlik yalnız kulp boşluğu + kaset + kavrama (425);
                                                               # ön niş yalıtımın DIŞINDA kaldı (Kemal: "sadece kasetlerin olduğu kısım soğutuculu")
T_IC, T_DIS = 3.0, 25.0                                  # °C [V: dükkân içi 25]
PU_K, PU_KAL = 0.022, 60.0                               # W/m·K, mm [K: poliüretan panel 0,022–0,025]
A = 2 * (IC["g"] * IC["y"] + IC["g"] * IC["z"] + IC["y"] * IC["z"]) / 1e6      # m²
U_DUVAR = PU_K / (PU_KAL / 1000.0)                                             # W/m²K  (U adi klasor degiskeniyle cakisiyordu)
Q_DUVAR = A * U_DUVAR * (T_DIS - T_IC)
KG2 = 6.4 + 5.8 + 8.8 + 2.8 + 2 * 6.0                    # 2 günlük toplam ürün (kg): kıyma+kuşbaşı+kaşar+sucuk+2 harç [V harç 6]
C_URUN = 3.4                                             # kJ/kg·K [K: yağlı et/peynir 3,2–3,6]
T_GELIS = 8.0                                            # kaset dolarken ürün bu sıcaklıkta giriyor [V]
Q_URUN = KG2 * C_URUN * 1000.0 * (T_GELIS - T_IC) / (2 * 24 * 3600.0)          # W (2 günde bir dolum)
Q_KAPAK = 25.0                                           # kapak açma/kaset değişimi sızıntısı [V]
Q_FAN = 2 * 12.0                                         # 2 × evaporatör fanı [katalog Ø150 eksenel ≈ 12 W]
Q_TOPLAM = Q_DUVAR + Q_URUN + Q_KAPAK + Q_FAN
Q_SECIM = Q_TOPLAM * 1.5                                 # emniyetli seçim
# MOTORLAR SOĞUK HÜCREDE DEĞİL: kuru bölmede, yalıtımın arkasında → ısıları soğutma yüküne GİRMİYOR (ve yoğuşma almıyorlar).

# ---------------------------------------------------------------- 4 · ELEKTRİK ----------------------------------------------------------------
MOTOR_A = 2.0                                            # NEMA23 faz akımı [katalog]
AYNI_ANDA = 2                                            # bir anda en çok 2 mil döner (bir kasetin helezonu + rotoru) [V]
GUC_KAYNAGI = 24.0 * MOTOR_A * AYNI_ANDA * 1.6           # W, %60 pay
KART = 12                                                # her mile bir sürücü (6 kaset × 2)

S = dict(
    derinlik=dict(kapak=Z_KAPAK, kaset=Z_KASET, kavrama=Z_KAVRAMA, bolme=Z_BOLME, kuru=Z_KURU,
                  nis=Z_NIS, kuru_mm=abs(Z_KURU[1] - Z_KURU[0]), tahrik_gerek=TAHRIK_Z,
                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"], dusme=DUSME, kaset_alti=KASET_ALTI),
    tabla=dict(cap=TABLA_D, rpm=TABLA_RPM, doz_sn=T_DOZ, r_dis=R_DIS, r_ic=R_IC, doz_strok=DOZ_STROK,
               tur_doz=round(TUR_DOZ, 2), serit_ara=round(SERIT_ARA, 1), x_doz_hiz=round(X_DOZ_HIZ, 1),
               x_gecis_hiz=X_GECIS_HIZ, x_strok=X_STROK),
    tahrik=dict(t_calisma=T_CALISMA, t_sikisma=T_SIKISMA, t_tasarim=T_TASARIM, oran=ORAN, t_motor=round(T_MOTOR, 2),
                rpm_motor=RPM_MOTOR, guc_W=round(GUC, 1), motor=MOTOR, reduktor=REDUKTOR, yatak=YATAK, kece=KECE, adet=12),
    soguk=dict(alan_m2=round(A, 2), U=round(U_DUVAR, 3), q_duvar=round(Q_DUVAR, 1), q_urun=round(Q_URUN, 1),
               q_kapak=Q_KAPAK, q_fan=Q_FAN, q_toplam=round(Q_TOPLAM, 1), q_secim=round(Q_SECIM, 1), kg2=KG2),
    elektrik=dict(motor_A=MOTOR_A, ayni_anda=AYNI_ANDA, guc_kaynagi_W=round(GUC_KAYNAGI), kart=KART))

if __name__ == "__main__":
    print("=== 1 · DERINLIK DIZILIMI (z = 0 on yuz) ===")
    for ad, (a, b) in (("on kapak", Z_KAPAK), ("kulp bosluğu", (Z_KAPAK[1], Z_KASET[0])), ("KASET", Z_KASET),
                       ("kavrama + soket", Z_KAVRAMA), ("yalitimli bolme", Z_BOLME), ("KURU MAKINE BOLMESI", Z_KURU)):
        print("   %-22s %7.0f … %7.0f   (%3.0f mm)" % (ad, a, b, abs(b - a)))
    print("   kaset kulpu artik kabinin ICINDE: on kapak kapaniyor")
    print("=== 2 · TAHRIK ===")
    print("   calisma torku %.2f N·m · sikisma siniri %.1f · tasarim %.1f N·m (emniyet %.0f)" % (T_CALISMA, T_SIKISMA, T_TASARIM, EMNIYET))
    print("   planet redüktör i=%.0f verim %.2f → motorda %.2f N·m gerekli, NEMA23 %.1f N·m veriyor (%.1f kat)" % (ORAN, VERIM, T_MOTOR, MOTOR["tork"], MOTOR["tork"] / T_MOTOR))
    print("   en yuksek cikis %.0f dev/dk → motor %.0f dev/dk (step icin rahat) · cikis gucu %.1f W" % (RPM_MAX, RPM_MOTOR, GUC))
    print("   tahrik derinlik ihtiyaci %.0f mm ≤ kuru bolme %.0f mm  →  %s" % (TAHRIK_Z, abs(Z_KURU[1] - Z_KURU[0]) + ARKA_PU + KAVRAMA, "SIGIYOR" if TAHRIK_Z <= abs(Z_KURU[1] - Z_KURU[0]) + ARKA_PU + KAVRAMA else "SIGMIYOR"))
    print("   NEDEN PLANET: sonsuz vida (NMRV030) giris ekseni dik → motor yana tasiyor, 140 kasetin arkasinda komsuya giriyordu.")
    print("=== 2d · DONER TABLA ===")
    print("   pide yaricapi %.0f · kaplanan %.0f · doz %.0f s · tabla %.0f dev/dk  [akis modellerinden]" % (PIDE_R, PIDE_R - KENAR, T_DOZ, TABLA_RPM))
    print("   agiz pide merkezine %.0f -> %.0f mm  =>  dozajda x stroku %.0f mm" % (R_DIS, R_IC, DOZ_STROK))
    print("   bir dozda %.2f tur -> her turda %.1f mm iceri (serit araligi)" % (TUR_DOZ, SERIT_ARA))
    print("   araba hizi: dozajda %.1f mm/s · yuvadan yuvaya %.0f mm/s · toplam strok %.0f mm" % (X_DOZ_HIZ, X_GECIS_HIZ, X_STROK))
    print("=== 3 · SOGUTMA ===")
    print("   ic hacim %.0f × %.0f × %.0f · yuzey %.2f m² · U %.3f W/m²K" % (IC["g"], IC["y"], IC["z"], A, U_DUVAR))
    print("   duvar %.0f W + urun %.0f W + kapak %.0f W + fan %.0f W = %.0f W → emniyetli secim %.0f W" % (Q_DUVAR, Q_URUN, Q_KAPAK, Q_FAN, Q_TOPLAM, Q_SECIM))
    print("   1/5 HP (150 W) hermetik grup +3 °C / −5 °C buharlasmada 250–350 W verir [katalog] → YETERLI")
    print("   MOTORLAR KURU BOLMEDE: isilari soguk hucreye girmiyor, uzerlerinde yogusma olmuyor")
    print("=== 4 · ELEKTRIK ===")
    print("   %d sürücü (her mile bir) · ayni anda %d mil → 24 V %.0f W guc kaynagi" % (KART, AYNI_ANDA, GUC_KAYNAGI))
    with io.open(os.path.join(U, "topping_hesap_v4.json"), "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1)
    print("topping_hesap_v4.json yazildi")
