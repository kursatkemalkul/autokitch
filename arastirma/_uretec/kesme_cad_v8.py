# -*- coding: utf-8 -*-
"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ · K400 — ÜRETİM MODELİ v8 (30 Eyl 2026 · Claude)
Kemal (30 Eyl): "Codex'in yaptığı kesme sprey tasarımı var, ona bak, tüm detaylara çalış, onu standartlarla gerçek parçalarla yap, 3B modelle".
TEMEL: kesme_cad_v7 (Codex · K400 · Kemal'in onayladığı k-dar v3 kısa düz itici: bant 220 ön besler, itici arkadan boşalan yere girer, 240 düz iter;
       bulaşık K'dan kalktı). Gövde, bant yeri, kesme merkezi (200, −206), bıçak yıldızı, çitler ve itici yerleşimi AYNEN; v8 parçaları katalog
       ölçüsüne çevirir, eksik bağlantıları kurar, BOM'u kaynaklar, hareket sürelerini katalog sınırından hesaplar.
Kaynak dosyaları: scratchpad/katalog (k_katalog.md · üretici PDF'leri, sayfa numaralı). Ölçüsü üreticiden okunamayanlar [V].

v7 → v8
 · KESİCİ: Festo DGRF-C-GF-63-125-PPV-A-R gerçek geometri (katalog 2022/06 s. 10, Ø63 satırı): boyunduruk 162 × 81 × 20 (L6) · WH 11,5 ·
   gövde 162 × 84 × 105 (L3) · silindir + uç kapak 75 × 75 × 195,8 · arka merkezleme Ø45 × 4 · kılavuz milleri Ø25 / 125 ara (arkada 7,5 + strok) ·
   L1 = 207,3 + 125 = 332,3 · bağlantı yüzü (H2 3 mm) arkada: 4 × M10 (80 × 40) + 2 × ZBH-12 merkezleme · G3/8 portlar (PL1 88 · PL 27,5 · J 6,3) ·
   sensör rayı + 2 × SMT-8M-A. v7'deki 150 × 150 × 90 kutu gövde, 15 mm boyunduruk ve Ø20 kılavuz milleri KALKTI. Gövde 16,5 mm bağlantı plakasıyla
   arka köprü kirişine (2 × M8) bağlı: 1870 N kesme tepkisi M10'larda kesmeye, plakadan kirişe.
   Kafa: boyunduruğa 4 × M8 ile 10 mm adaptör (Ø170) → 3 × Ø16 × 70 ara dikme (v7: 50) → kafa plakası (aynı) → bıçak yıldızı (aynı).
 · SPREY: v7'deki "PulsaJet AA10000AUH-104210 + UniJet TG" katalogda YOK: 104210 (gıda sürümü) yalnız düz (TPU…PWMD kırlangıç) uç alır (veri sayfası
   104210 rev. 4). Tam koni için standart gövde: PulsaJet AAB10000AUH-03-EPR (1/8 BSPT, EPDM; UniJet uç ≤ -03; 7 bar; 24 V 0,36 A; 66,2 mm; Ø37,8,
   30,1 düzlük; sıvı + elektrik arkada — veri sayfası 10000AUH-03 rev. 5) + UniJet TG-W 2.8W geniş açı tam koni (120° @ 0,7 bar su; katalog 75 s. B39)
   + CP1325 uç somunu (13/16"). Kafada DİK: ön yüzü kafa plakasının üstünde, uç göbekten aşağı bakar (v7'nin yatay gövde + dirsek + ayrı nozül
   düzeni kalktı — valf ile uç arasında ölü hacim yok, damlamaz). Gıda uygunluğu (EC 1935/2004) -03 veri sayfasında yazmıyor → Spraying Systems'e
   sorulacak [V]; tereyağı ile debi / açı denemesi gerekir (katalog açıları su içindir).
 · TANK: 3 L ısıtmalı basınçlı tank üst bölmeye SIĞMIYOR (gerçek parça Walther Pilot MDG 3: Ø173 × 454, 3,2 L / kullanılır 2,5 L, paslanmaz,
   3 bar sürümü — walther-pilot.de) → ALT dolaba (v7'de boş, bulaşık kalktı) damlama tavasının içine. Isıtıcı ceket + PT100 [V: Walther ısıtma
   seçeneği teyit edilmedi]. Isıtmalı hortum arkadan (x 380, z −600) istasyon tabanındaki rakordan çıkar, köprünün altından kafaya gelir.
 · BANT: Interroll RollerDrive EC5000 ø50 IP66 24 V 35 W 49:1 tahrik (x 354; 11 HEX mil + M8, yan profillerde delik) + avara ø50 (x 46) ·
   Habasit CD.F20-A-UW 2,0 mm beyaz TPU (EU 10/2011 + FDA, min kasnak Ø25 — Habasit PDS 09.05.2025) · bant eni 400 → 380 (rulo RL 398 içinde
   kalır) · kayma tablasına 2 travers (v7: havada) · bant ayakları yan profile değer (v7: 2,5 mm içindeydi) · ölü plaka profillere uzar (v7: havada) ·
   çitlere 4 braket (v7: havada).
 · İTİCİ: 2 × SMC MY1B10G (merkezi borulu ø10, katalog MY1B_2103 s. 8-11-21) katalog şekliyle + MY-J10 yüzer bağlantı (X) + 4 × D-M9N + 4 × AS1201F ·
   HIWIN MGN15 ray / MGN15H blok (katalog s. 86 teyitli: H 16 · W 32 · L 58,8 · ray 15 × 10 · P 40). X orta yükseltmesi MY-J10 bloklarına oturur.
 · ALGILAMA: v7'nin sensör kutuları fırın ölü plakasına giriyordu → 2 çift Omron E3Z-T61 karşılıklı ışın (gövde 10,8 × 31 × 20 · 2 × M3 25,4 —
   E3Z veri sayfası s. 15) · giriş x 105 · duruş x 350 · ışın y 1006 (ürün 996–1011 keser, çit üstü 1001,3 kesmez).
 · PANO: v7 zarfı yerine gerçek elemanlar: Siemens S7-1200 CPU 1214C DC/DC/DC (110 × 100 × 75) · Mean Well NDR-240-24 (TraceParts STEP) ·
   2 × Omron E5DC sıcaklık kontrolcüsü + 2 × G3PE SSR [V] · sigorta · klemens · SMC SS5Y3-20-04 valf adası (69,5 × 49 × 20) + 3 × SY3120 + kör plaka ·
   SMC AW20-F02-A şartlandırıcı (40 × 155) · hava girişi arka saçtan · DGRF (2 × Ø8), X silindiri (2 × Ø4) ve tank (Ø6) hortumları.
 · BOM: v7'nin bütün parçaları (Codex hiçbirine BOM yazmamıştı) + v8 parçaları kaynaklı; ölçüsü teyit edilmeyenler [V].
ZAMAN: hareket süreleri katalog sınırından (hesap: bu dosyanın sonunda · kütleler CAD hacminden): MY1B10 lastik tampon sınırı (katalog s. 8-11-19)
   → Z itici 350 mm ≥ 2,4 s (v7 1,3 s: tampon sınırının 1,8 katı) · X 250 mm ≥ 2,6 s · hız 100–500 mm/s (s. 8-11-? "Piston speed ø10") ·
   EC5000 ≤ 0,37 m/s · DGRF çarpma enerjisi ≤ 1,3 J (Festo 562221).
KOORDİNAT: v7 ile aynı — x 0…400 (hatta 4000 + x), y yerden, z 0 ön yüz … −830 arka."""
import math
import cadquery as cq
import kesme_cad_v7 as K7
from kesme_cad_v7 import *                      # v7 (Codex) sabitleri + v6 yardımcıları (kut / silx / sily / silz / boru / polar / radyal) + TC, KC, OLD
import kutu_cad_v12 as KC12                     # E v12 gerçek saat

W = 400.0
PARCALAR = K7.PARCALAR                          # montaj KS.PARCALAR'ı okur — v7'nin listesi yerinde düzenlenir
KAYNAK_MY1B = "SMC MY1B katalog (content2.smcetech.com/pdf/MY1B_2103.pdf) s. 8-11-21 ø10 çizimi"
KAYNAK_EC = "Interroll EC5000 ø50 IP66 veri sayfası (interroll.com EC5000_50mm_IP66_EN.pdf) s. 55–57"
KAYNAK_DGRF = "Festo DGRF-C katalog 2022/06 s. 10 (Ø63) + veri sayfası 562221"
KAYNAK_PJ = "Spraying Systems veri sayfası 10000AUH-03 rev. 5 (spray.com)"
KAYNAK_HIWIN = "HIWIN MG katalog s. 86 (MGN15H)"


def ekle8(ad, wp, mal="sac", grup="SABIT", bom=None):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, bom=bom))


def cikar(*adlar):
    n0 = len(PARCALAR)
    PARCALAR[:] = [p for p in PARCALAR if p["ad"] not in adlar]
    assert n0 - len(PARCALAR) == len(adlar), (n0, len(PARCALAR), adlar)


def bul(ad):
    return next(p for p in PARCALAR if p["ad"] == ad)


def polar8(r, phi):
    """v6'nın polar()'ı v6 merkezini (300, −170) kullanır — v7/v8 kesme merkezi (200, −206)"""
    return XC + r * math.cos(math.radians(phi)), ZC + r * math.sin(math.radians(phi))


def hex_y(x, z, af, y0, y1):
    """y ekseni boyunca altıgen (af = anahtar ağzı)"""
    h = cq.Workplane("XY").polygon(6, af / math.cos(math.radians(30))).extrude(y1 - y0)
    return h.rotate((0, 0, 0), (1, 0, 0), -90).translate((x, y0, z))


def pah_kutu(x0, x1, y0, y1, z0, z1, c):
    """y'ye paralel 4 kenarı pahlı kutu (Festo gövde / boyunduruk kesiti)"""
    return kut(x0, x1, y0, y1, z0, z1).edges("|Y").chamfer(c)


# ---------------------------------------------------------------- SMC MY1B10G (merkezi borulu ø10) ----------------------------------------------------------------
MY1B = dict(kapak_L=15.0, kapak_W=28.0, kapak_H=20.2, profil_W=26.0, profil_H=19.5, masa_L=50.0, masa_W=24.0, masa_ust=27.0, masa_ev=30.0, ek=110.0)


def my1b10g(on_ad, strok, eksen, a0, taban, yan):
    """eksen 'x': gövde a0 … a0 + strok + 110 boyunca x'te, taban y'de, merkez z = yan · eksen 'z': boy z'de (a0 = arka uç, +z yönüne), merkez x = yan.
    Masa evde uçtan 30 (katalog '30'). Döndürür: (gövde parçaları, masa katısı)"""
    L = strok + MY1B["ek"]
    kL, kW, kH, pW, pH = MY1B["kapak_L"], MY1B["kapak_W"], MY1B["kapak_H"], MY1B["profil_W"], MY1B["profil_H"]

    def k(u0, u1, y0, y1, w0, w1):                     # eksen boyu u, yükseklik y, yan w → dünya kutusu
        return kut(u0, u1, y0, y1, w0, w1) if eksen == "x" else kut(w0, w1, y0, y1, u0, u1)

    def s(u0, u1, y, w, r):                            # eksen boyunca silindir
        return silx(y, w, r, u0, u1) if eksen == "x" else silz(w, y, r, u0, u1)
    kap0 = k(a0, a0 + kL, taban, taban + kH, yan - kW / 2, yan + kW / 2)
    kap1 = k(a0 + L - kL, a0 + L, taban, taban + kH, yan - kW / 2, yan + kW / 2)
    prof = k(a0 + kL, a0 + L - kL, taban, taban + pH, yan - pW / 2, yan + pW / 2)
    for sgn in (-1, 1):                                # yan oluklar: D-M9N algılayıcı yuvası 4 × 3 (oluk kesiti katalogda yok [V])
        prof = prof.cut(k(a0 + kL - 1, a0 + L - kL + 1, taban + 6.0, taban + 10.0, yan + sgn * pW / 2 - (3.0 if sgn > 0 else 0.0), yan + sgn * pW / 2 + (0.0 if sgn > 0 else 3.0)))
    govde = [("%s_uc_kapagi_0" % on_ad, kap0, "aluminyum"), ("%s_uc_kapagi_1" % on_ad, kap1, "aluminyum"), ("%s_profil" % on_ad, prof, "aluminyum")]
    # merkezi boru: 2 × M5 port uzak uç kapağında (katalog "2-M5 × 0.8 (Port)") + AS1201F-M5-04A dirsek hız ayar valfi (D1 8,2 · L1 17,2 · SMC AS-1F-A s. 5)
    pc = a0 + L - kL / 2.0
    for i, dw in enumerate((-6.0, 6.0)):
        fit = s(pc - 5.0, pc + 5.0, taban + kH + 9.0, yan + dw, 4.1)
        fit = fit.union(k(pc - 4.0, pc + 4.0, taban + kH, taban + kH + 9.0, yan + dw - 4.0, yan + dw + 4.0))
        govde.append(("%s_AS1201F_%d" % (on_ad, i), fit, "siyah"))
    # D-M9N konum algılayıcıları (2 adet · 22 mm · oluğa gömülü, M2,5 set vidası) — katalog s. 8-11-104: uç yüzlerden 24 / 86
    for i, u in enumerate((a0 + 24.0, a0 + L - 86.0)):
        govde.append(("%s_D-M9N_%d" % (on_ad, i), k(u, u + 22.0, taban + 6.5, taban + 9.5, yan + pW / 2 - 2.8, yan + pW / 2), "sensor"))
    m0 = a0 + MY1B["masa_ev"]
    masa = k(m0, m0 + MY1B["masa_L"], taban + pH, taban + MY1B["masa_ust"], yan - MY1B["masa_W"] / 2, yan + MY1B["masa_W"] / 2)
    return govde, masa


def itici_v8():
    """v7 itici kutularını katalog şekline çevirir (kinematik grupları aynı)"""
    govde, masa = my1b10g("itici_X_MY1B10G-250", 250.0, "x", 20.0, 964.0, -700.0)
    cikar("itici_MY1B10G_250", "itici_X_araba")
    for i, (ad, sh, mal) in enumerate(govde):
        ekle8(ad, sh, mal, "SABIT", bom=("SMC MY1B10G-250 rodless silindir (merkezi borulu, ø10, strok 250)", 1, "boy 360 · 0,2–0,8 MPa · 100–500 mm/s · lastik tampon",
                                         KAYNAK_MY1B, "SATIN ALMA") if i == 2 else (
                                         ("SMC AS1201F-M5-04A dirsek hız ayar valfi (çıkışta kısma)", 4, "M5 · Ø4 hortum · 5 g", "SMC AS-1F-A EU katalog s. 5", "SATIN ALMA") if "AS1201F_0" in ad else (
                                          ("SMC D-M9N katı hal oto svic (MY1B yan oluğu)", 4, "3 telli NPN · 22 mm · çalışma aralığı 2,5 mm", "SMC Best Pneumatics s. 1199 + MY1B s. 8-11-104", "SATIN ALMA") if "D-M9N_0" in ad else None)))
    ekle8("itici_X_MY1B10G-250_masa", masa, "aluminyum", "ITICI_ARABA")
    # X yüzer bağlantı SMC MY-J10: masanın iki yanında blok (MGN blokları ile 13 mm boşluk), orta yükseltmenin altına vidalı; pimleri masanın yan yüzüne
    # dayanır (±1 mm yüzme · katalog s. 8-11-28). Yükseltme masadan 3 mm yukarıda biter → silindir kılavuza zorlanmaz, yalnız itki taşır.
    yuk = bul("itici_X_merkez_yukseltme")
    yuk["wp"] = kut(50.0, 100.0, 994.0, 1046.0, -726.0, -674.0).cut(kut(54.0, 96.0, 998.0, 1047.0, -722.0, -678.0))
    yuk["bom"] = ("X arabası orta yükseltme 6082 cepli (MY-J10 bloklarının üstünde, masaya değmez)", 1, "50 × 52 × 52 · et 4", "üretim", "ÜRETİM")
    # hafifletme: Codex zarfları "sac" (paslanmaz, dolu) idi → 6082 cepli (X arabası 9,6 → ≈ 4,5 kg · MY1B10 H ünitesi sınırı 5 kg)
    for z in (-755, -645):
        a = bul("itici_X_ara_%d" % z)
        a["wp"] = kut(45.6, 104.4, 980.0, 1046.0, z - 16.0, z + 16.0).cut(kut(49.6, 100.4, 984.0, 1042.0, z - 12.0, z + 12.0)); a["mal"] = "aluminyum"
    bul("itici_Z_plaka")["mal"] = "aluminyum"
    for x in (53, 97):
        r_ = bul("itici_Z_yukseltme_%d" % x)
        r_["wp"] = kut(x - 7.5, x + 7.5, 1051.0, 1076.0, -820.0, -360.0).cut(kut(x - 5.5, x + 5.5, 1053.0, 1074.0, -821.0, -359.0)); r_["mal"] = "aluminyum"
    bul("itici_Z_kopru")["mal"] = "aluminyum"
    for i, (z0, z1) in enumerate(((-726.0, -714.0), (-686.0, -674.0))):
        ekle8("itici_X_MY-J10_blok_%d" % i, kut(60.0, 90.0, 984.5, 994.0, z0, z1), "aluminyum", "ITICI_ARABA",
              bom=("SMC MY-J10 yüzer bağlantı (MY1B10 için)", 1, "±1 mm · M4 tutma cıvatası 0,6 N·m", "SMC MY1B katalog s. 8-11-28", "SATIN ALMA") if i == 0 else None)
        pa, pb = ((z1, -712.0) if i == 0 else (-688.0, z0))                          # bloğun iç yüzü → masanın yan yüzü (masa z −712…−688)
        ekle8("itici_X_MY-J10_pim_%d" % i, silz(75.0, 987.25, 2.0, pa, pb), "celik", "ITICI_ARABA")
    # X · DIŞ ŞOK EMİCİ: X arabası ≈ 4,7 kg → MY1B10 lastik tampon sınırı (katalog s. 8-11-19) bu kütlede 100 mm/s altına düşer, tamponla çalışmaz.
    # MY1B10'un H ünitesindeki şok emici (RB0805 · 1,0 J · 5 mm · ≤ 1000 mm/s, katalog s. 8-11-7/17) iki uçta ayrı brakette: uç arabanın orta
    # yükseltmesine çarpar (enerji yüzer bağlantıdan geçmez). Braket profilin −z yanında (MGN rayı ile 4,5 · profil ile 3 mm boşluk).
    for i, (xb0, xb1, xa0, xa1, rod) in enumerate(((36.0, 46.0, 12.0, 46.0, (46.0, 50.0)), (354.0, 364.0, 354.0, 388.0, (350.0, 354.0)))):
        br = kut(xb0, xb1, 964.0, 1013.0, -733.0, -716.0).union(kut(xb0, xb1, 997.0, 1013.0, -716.0, -692.0)).cut(silx(1005.0, -700.0, 4.0, xb0 - 1, xb1 + 1))
        ekle8("itici_X_durdurucu_%d" % i, br, "aluminyum", "SABIT",
              bom=("X durdurucu braketi 6082 (RB0805 kelepçeli · X taban plakasına 2 × M5)", 2, "10 × 49 × 41", "üretim", "ÜRETİM") if i == 0 else None)
        ekle8("itici_X_RB0805_%d" % i, silx(1005.0, -700.0, 4.0, xa0, xa1).union(silx(1005.0, -700.0, 1.25, rod[0], rod[1])), "celik", "SABIT",
              bom=("SMC RB0805 şok emici (M8 × 0,75 · strok 5 · 1,0 J · ≤ 1000 mm/s)", 2, "X strok sonları", "SMC MY1B katalog s. 8-11-7 / 8-11-17", "SATIN ALMA") if i == 0 else None)
    govde, masa = my1b10g("itici_Z_MY1B10G-350", 350.0, "z", -820.0, 1051.0, 75.0)
    cikar("itici_MY1B10G_350", "itici_Z_araba")
    for i, (ad, sh, mal) in enumerate(govde):
        ekle8(ad, sh, mal, "ITICI_ARABA", bom=("SMC MY1B10G-350 rodless silindir (merkezi borulu, ø10, strok 350)", 1, "boy 460 · X arabasının üstünde",
                                              KAYNAK_MY1B, "SATIN ALMA") if i == 2 else None)
    ekle8("itici_Z_MY1B10G-350_masa", masa, "aluminyum", "ITICI_CAPRAZ")
    yb = bul("itici_yuzer_baglanti")
    yb["bom"] = ("Z yüzer pim (özel · ±1 mm): Z rayları silindire bitişik, yandan bağlanan MY-J10 sığmaz", 1, "Ø8 pim + POM burç", "üretim [V]", "ÜRETİM")


# ---------------------------------------------------------------- BANT: RollerDrive EC5000 + avara + Habasit bant ----------------------------------------------------------------
EC = dict(r=25.0, et=1.5, hex=11.0, hex_L=13.3, el_ek=14.0)
BANT_Z8 = (-402.0, -22.0)                       # bant eni 380 (RL 398 içinde · v7 400 = rulo boyundan uzun)


def bant_v8():
    """tahrik çıkış ucunda (x 354): EC5000 ø50 · avara giriş ucunda (x 46) · yan profiller arası açıklık EL = z −418 … −6 = 412 → RL 398"""
    cikar("tahrik_rulosu_46", "tahrik_rulosu_354")
    z_ic0, z_ic1 = -418.0, -6.0                         # yan profillerin iç yüzleri (v7 bant_yan: z −424…−418 ve −6…0)
    RL = (z_ic1 - z_ic0) - EC["el_ek"]                    # 398
    zr0, zr1 = z_ic0 + (z_ic1 - z_ic0 - RL) / 2.0, z_ic1 - (z_ic1 - z_ic0 - RL) / 2.0
    y = 969.0
    tup = silz(354.0, y, EC["r"], zr0, zr1).cut(silz(354.0, y, EC["r"] - EC["et"], zr0 + 8.0, zr1 - 8.0))
    ekle8("tahrik_rulosu_EC5000_354", tup, "aluminyum", "SABIT",
          bom=("Interroll RollerDrive EC5000 AI ø50 IP66 · 24 V 35 W · 49:1 (motor + sürücü rulonun içinde)", 1,
               "RL %.0f · EL %.0f · 0,02–0,37 m/s · anma 2,42 N·m · paslanmaz boru 1,5" % (RL, RL + EC["el_ek"]), KAYNAK_EC, "SATIN ALMA"))
    d_hex = EC["hex"] / math.cos(math.radians(30))                                     # 11 anahtar ağzı → köşeler arası 12,7
    hx = cq.Workplane("XY").polygon(6, d_hex).extrude(EC["hex_L"]).translate((354.0, y, zr0 - EC["hex_L"]))   # borunun ucundan 13,3 dışarı: yan profilden geçer
    ekle8("tahrik_rulosu_EC5000_hex_mil", hx, "celik", "SABIT")
    ekle8("tahrik_rulosu_EC5000_kablo", silz(354.0, y, 3.5, zr0 - EC["hex_L"] - 60.0, zr0 - EC["hex_L"]), "siyah", "SABIT",
          bom=("EC5000 AI bağlantı kablosu 5 × 0,5 · M8 geçmeli → pano (hız: 2 dijital girişle 4 önayar [V])", 1, "", KAYNAK_EC, "SATIN ALMA"))
    ekle8("tahrik_rulosu_EC5000_M8_civata", silz(354.0, y, 4.0, zr1, z_ic1 + 6.0).union(silz(354.0, y, 6.5, z_ic1 + 6.0, z_ic1 + 11.0)), "celik", "SABIT",
          bom=("DIN 912 M8 × 16 A2 (EC5000 M8 dişli ucu yan profile)", 1, "", "DIN 912", "SATIN ALMA"))
    av = silz(46.0, y, EC["r"], zr0, zr1).cut(silz(46.0, y, EC["r"] - 1.5, zr0 + 8.0, zr1 - 8.0))
    ekle8("avara_rulosu_46", av, "aluminyum", "SABIT",
          bom=("Avara rulo ø50 paslanmaz, rulmanlı (Interroll 1700 sınıfı) · gergi uzun delikli", 1, "RL %.0f" % RL, "Interroll 1700 [V]", "SATIN ALMA"))
    ekle8("avara_mili_0", silz(46.0, y, 6.0, z_ic0 - 8.0, zr0), "celik", "SABIT")      # arka profilden geçer (Ø12 delik)
    ekle8("avara_mili_1", silz(46.0, y, 6.0, zr1, z_ic1 + 8.0), "celik", "SABIT")      # ön profilden geçer (gergi uzun deliği)
    for ad_, (zz0, zz1) in (("bant_yan_-421", (-425.0, -417.0)), ("bant_yan_-3", (-7.0, 1.0))):
        yp = bul(ad_)
        yp["wp"] = yp["wp"].cut(silz(46.0, y, 6.1, zz0, zz1))
        if ad_ == "bant_yan_-421":
            yp["wp"] = yp["wp"].cut(cq.Workplane("XY").polygon(6, 11.2 / math.cos(math.radians(30))).extrude(zz1 - zz0).translate((354.0, y, zz0)))
        else:
            yp["wp"] = yp["wp"].cut(silz(354.0, y, 4.25, zz0, zz1))
    # bant: Habasit CD.F20-A-UW 2,0 · eni 380
    z0, z1 = BANT_Z8
    bul("bant_PU_ust")["wp"] = kut(46.0, 354.0, 994.0, 996.0, z0, z1)
    bul("bant_PU_alt")["wp"] = kut(46.0, 354.0, 942.0, 944.0, z0, z1)
    for x in (46.0, 354.0):
        wrap = silz(x, y, 27.0, z0, z1).cut(silz(x, y, 25.0, z0 - 1, z1 + 1))
        bul("bant_sarim_%d" % int(x))["wp"] = wrap.intersect(kut(x - 28.0 if x == 46.0 else x, x if x == 46.0 else x + 28.0, 940.0, 998.0, z0, z1))
    # ayaklar yan profilin altına (v7: 2,5 mm içindeydi) · ölü plaka profillere uzanır · kayma tablasına 2 travers
    for x in (65, 335):
        for zc in (-421, -3):
            bul("bant_ayagi_%d_%d" % (x, zc))["wp"] = kut(x - 10.0, x + 10.0, 895.0, 932.5, zc - 10.0, zc + 10.0).cut(kut(x - 8.0, x + 8.0, 894.0, 933.5, zc - 8.0, zc + 8.0))
    bul("olu_plaka")["wp"] = kut(382.0, 398.5, 990.0, 996.0, -418.0, -6.0)
    for i, x in enumerate((120.0, 280.0)):
        ekle8("bant_traversi_%d" % i, kut(x - 10.0, x + 10.0, 976.0, 988.0, -418.0, -6.0).cut(kut(x - 8.0, x + 8.0, 978.0, 986.0, -419.0, -5.0)), "sac", "SABIT",
              bom=("Bant traversi 304 kutu 20 × 12 × 1 (kayma tablası altı, yan profillere kaynaklı)", 2, "412", "üretim", "ÜRETİM") if i == 0 else None)
    # çit braketleri (v7: çitler havada) — itici yüzünün geçtiği x 247–265 aralığında braket YOK
    for i, (x, zc, z_p0, z_p1) in enumerate(((150.0, -51.0, -54.0, 0.0), (320.0, -51.0, -54.0, 0.0), (150.0, -361.0, -424.0, -358.0), (320.0, -361.0, -424.0, -358.0))):
        on = zc > -200
        kol = kut(x - 8.0, x + 8.0, 1001.3, 1003.3, z_p0, z_p1)
        ayak = kut(x - 8.0, x + 8.0, 987.5, 1001.3, -6.0, 0.0) if on else kut(x - 8.0, x + 8.0, 987.5, 1001.3, -424.0, -418.0)
        ekle8("cit_braketi_%d" % i, kol.union(ayak), "sac", "SABIT",
              bom=("Çit braketi 304 · 2 mm (POM çit → bant yan profili)", 4, "16 genişlik", "üretim", "ÜRETİM") if i == 0 else None)


# ---------------------------------------------------------------- ÜRÜN ALGILAMA ----------------------------------------------------------------
E3Z = dict(W=10.8, H=31.0, D=20.0, eksen_ust=19.5)       # E3Z veri sayfası s. 15: 10,8 × 31 × 20 · üst delik üstten 2,8 · delikten ışın ekseni 16,7
Y_ISIN = 1006.0


def sensor_v8():
    cikar("sensor_kenar_-415", "sensor_kenar_-10")
    y0 = Y_ISIN + E3Z["eksen_ust"] - E3Z["H"]              # 994,5
    for i, (x, ad) in enumerate(((105.0, "giris"), (350.0, "durus"))):             # giriş: eğik çitlerin bittiği yer (x 100) · duruş: kesme merkezi 200 + 150
        for j, (z0, z1) in enumerate(((-438.0, -418.0), (-6.0, 14.0))):          # mercek yüzü profilin iç yüzünde (−418 / −6)
            ekle8("urun_sensoru_%s_%s" % (ad, "verici" if j == 0 else "alici"), kut(x - E3Z["W"] / 2, x + E3Z["W"] / 2, y0, y0 + E3Z["H"], z0, z1), "sensor", "SABIT",
                  bom=("Omron E3Z-T61 karşılıklı ışın fotosel (verici + alıcı · IP67 · 1 ms)", 2, "%s: ürün ön kenarı" % ("giriş x 105" if ad == "giris" else "duruş x 350 (kesme merkezi 200 + 150)"),
                       "Omron E3Z veri sayfası CSM_E3Z_DS_E_18_10 s. 15 (gövde) [T61 ışın ekseni V]", "SATIN ALMA") if j == 0 and i == 0 else None)
            # L braket: profil üstü (987,5) → sensörün yan yüzü (2 × M3)
            xs = x + E3Z["W"] / 2
            ekle8("urun_sensoru_%s_braket_%d" % (ad, j), kut(x - E3Z["W"] / 2, xs + 2.0, 987.5, y0, z0, z1).union(kut(xs, xs + 2.0, y0, y0 + 25.0, z0, z1)), "sac", "SABIT",
                  bom=("Sensör L braketi 304 · 2 mm (E3Z → bant yan profili)", 4, "", "üretim", "ÜRETİM") if j == 0 and i == 0 else None)


# ---------------------------------------------------------------- KESİCİ: Festo DGRF-C-63-125 ----------------------------------------------------------------
DG = dict(L6=20.0, WH=11.5, L3=105.0, L1_0=207.3, strok=125.0, B1=162.0, H1=84.0, H2=3.0, E=75.0, D4=25.0, B2=125.0, L2_0=7.5,
          B3=80.0, L5=40.0, L7=18.5, PL1=88.0, PL=27.5, J=6.3, VA=4.0, B=45.0, H5=23.5, B4=80.0, H4=40.0, cubuk=20.0, kapak=40.0)
Y_BOY8 = (Y_KAFA[1], Y_KAFA[1] + 70.0)             # ara dikmeler 70 (v7: 50) — PulsaJet dik sığsın
Y_ADP = (Y_BOY8[1], Y_BOY8[1] + 10.0)              # adaptör 10
Y_BOYUN = (Y_ADP[1], Y_ADP[1] + DG["L6"])           # boyunduruk 1254,5–1274,5
Y_GOV8 = (Y_BOYUN[1] + DG["WH"], Y_BOYUN[1] + DG["WH"] + DG["L3"])     # gövde 1286–1391
Y_ARKA = Y_BOYUN[0] + DG["L1_0"] + DG["strok"]      # arka uç kapak yüzü 1586,8
Y_KAPAK = (Y_ARKA - DG["kapak"], Y_ARKA)           # uç kapak (PL 27,5 portu içinde) [kalınlık V]
Z_BAG = ZC - (DG["H1"] - DG["H2"]) / 2.0 - DG["H2"]  # bağlantı yüzü −249,5 (eksen boyunduruğun ortasında: H5 23,5 + H4/2 = 43,5)
Z_GOV = (Z_BAG, Z_BAG + DG["H1"])                  # −249,5 … −165,5
Z_BOYUN = (Z_BAG + DG["H2"], Z_GOV[1])             # −246,5 … −165,5
X_GOV = (XC - DG["B1"] / 2, XC + DG["B1"] / 2)      # 119 … 281
Z_PLAKA = (-266.0, Z_BAG)                          # bağlantı plakası 16,5 (arka kirişin ön yüzü −266)
M10_XY = [(XC + sx * DG["B3"] / 2, Y_GOV8[0] + DG["L7"] + sy * DG["L5"]) for sx in (-1, 1) for sy in (0, 1)]
PISTON = (Y_KAPAK[0] - 1.0 - 25.0, Y_KAPAK[0] - 1.0)                 # evde (yukarıda) piston
KESICI_SIL = ("silindir_baglanti_plakasi", "DGRF-C-63-125_govde", "DGRF_hava_rakoru_0", "DGRF_hava_rakoru_1", "DGRF_piston_mili", "DGRF_kilavuz_mili_0",
              "DGRF_kilavuz_mili_1", "DGRF_on_plaka", "ara_dikme_0", "ara_dikme_1", "ara_dikme_2", "PulsaJet_AA10000AUH_104210", "PulsaJet_isitici_ceket",
              "sprey_dirsegi", "UniJet_nozul_govdesi_TG", "sprey_ucu_TG", "isitmali_hortum_kafa", "PulsaJet_semeri", "DGRF_burcu_0", "DGRF_burcu_1",
              "DGRF_burcu_2", "sprey_konisi")


def kesici_v8():
    cikar(*KESICI_SIL)
    xr = [XC - DG["B2"] / 2, XC + DG["B2"] / 2]                                   # kılavuz milleri x 137,5 / 262,5
    # SABİT: gövde + silindir + uç kapak + merkezleme
    gov = pah_kutu(X_GOV[0], X_GOV[1], Y_GOV8[0], Y_GOV8[1], Z_GOV[0], Z_GOV[1], 12.0)
    for x in xr:
        gov = gov.cut(sily(x, ZC, DG["D4"] / 2 + 0.25, Y_GOV8[0] - 1, Y_GOV8[1] + 1))
    gov = gov.cut(sily(XC, ZC, DG["cubuk"] / 2 + 0.25, Y_GOV8[0] - 1, Y_GOV8[1] + 1))
    for (x, y) in M10_XY:
        gov = gov.cut(silz(x, y, 5.0, Z_BAG - 1.0, Z_BAG + 24.0))                    # M10 (T2 24 derinlik)
    for (x, y) in (M10_XY[0], M10_XY[3]):
        gov = gov.cut(silz(x, y, 6.0, Z_BAG - 1.0, Z_BAG + 2.6))                     # ZBH-12 havşası Ø12 × 2,6
    ekle8("DGRF-C-63-125_govde", gov, "aluminyum", "SABIT",
          bom=("Festo DGRF-C-GF-63-125-PPV-A-R kılavuzlu silindir (Clean Design · paslanmaz miller · NSH H1 yağ)", 1,
               "Ø63 · strok 125 · 6 bar 1870 N itme / 1682 N çekme · 8,19 kg · parça no 562221", KAYNAK_DGRF, "SATIN ALMA"))
    bar = pah_kutu(XC - DG["E"] / 2, XC + DG["E"] / 2, Y_GOV8[1], Y_KAPAK[0], ZC - DG["E"] / 2, ZC + DG["E"] / 2, 6.0).cut(sily(XC, ZC, 31.75, Y_GOV8[1] - 1, Y_KAPAK[0] + 1))
    ekle8("DGRF_silindir_borusu", bar, "aluminyum", "SABIT")
    kap = pah_kutu(XC - DG["E"] / 2, XC + DG["E"] / 2, Y_KAPAK[0], Y_KAPAK[1], ZC - DG["E"] / 2, ZC + DG["E"] / 2, 8.0)
    kap = kap.union(sily(XC, ZC, DG["B"] / 2, Y_KAPAK[1], Y_KAPAK[1] + DG["VA"]))
    ekle8("DGRF_uc_kapagi", kap, "aluminyum", "SABIT")
    for i, (sx, sz) in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):              # 4 × gergi cıvatası başı (TG 56,5 kare)
        ekle8("DGRF_gergi_civatasi_%d" % i, sily(XC + sx * 28.25, ZC + sz * 28.25, 6.5, Y_KAPAK[1], Y_KAPAK[1] + 4.0), "celik", "SABIT")
    # sensör rayı (−R, bağlantı yüzünün karşısı = ön yüz) + 2 × SMT-8M-A (ev + strok sonu)
    ekle8("DGRF_sensor_rayi", kut(XC - 4.0, XC + 4.0, Y_GOV8[1], Y_KAPAK[0], ZC + DG["E"] / 2, ZC + DG["E"] / 2 + 2.0), "aluminyum", "SABIT")
    for i, yc in enumerate(((PISTON[0] + PISTON[1]) / 2, (PISTON[0] + PISTON[1]) / 2 - DG["strok"])):
        ekle8("DGRF_SMT-8M_%d" % i, kut(XC - 2.3, XC + 2.3, yc - 12.0, yc + 12.0, ZC + DG["E"] / 2 + 2.0, ZC + DG["E"] / 2 + 7.2), "sensor", "SABIT",
              bom=("Festo SMT-8M-A-PS-24V-E-0,3-M8D yakınlık sensörü (ev / kesim sonu)", 2, "sensör rayında", "Festo DGRF-C katalog s. 12 [ölçü V]", "SATIN ALMA") if i == 0 else None)
    # portlar G3/8 + QSL dirsek (Ø8) · PL1 88 (gövde) · PL 27,5 (uç kapak) · J 6,3
    yp1, yp2 = Y_GOV8[0] + DG["PL1"], Y_ARKA - DG["PL"]
    xp = XC + DG["J"]
    ekle8("DGRF_port_on_QSL", silz(xp, yp1, 7.5, Z_GOV[1], Z_GOV[1] + 12.0).union(silx(yp1, Z_GOV[1] + 12.0, 6.0, xp, 226.0)).union(
        sily(226.0, Z_GOV[1] + 12.0, 6.0, yp1, yp1 + 12.0)), "siyah", "SABIT",
          bom=("Festo QSL-G3/8-6 dirsek geçme rakor", 2, "Ø6 hortum (valf SY3120 C6)", "festo.com [V]", "SATIN ALMA"))
    ekle8("DGRF_port_arka_QSL", silz(xp, yp2, 7.5, ZC + DG["E"] / 2, Z_GOV[1] + 12.0).union(sily(xp, Z_GOV[1] + 12.0, 6.0, yp2, yp2 + 20.0)), "siyah", "SABIT")
    # bağlantı plakası (arka kirişe) + 4 × M10 + 2 × ZBH-12 + 2 × M8
    pl = kut(X_GOV[0], X_GOV[1], Y_GOV8[0], Y_KIRIS[1], Z_PLAKA[0], Z_PLAKA[1])
    for (x, y) in M10_XY:
        pl = pl.cut(silz(x, y, 5.5, Z_PLAKA[0] - 1, Z_PLAKA[1] + 1))
    for (x, y) in (M10_XY[0], M10_XY[3]):
        pl = pl.cut(silz(x, y, 6.0, Z_PLAKA[1] - 5.0, Z_PLAKA[1] + 1))                # ZBH yuvası plakada 5
    for x in (135.0, 265.0):
        pl = pl.cut(silz(x, sum(Y_KIRIS) / 2, 4.5, Z_PLAKA[0] - 1, Z_PLAKA[1] + 1))
    ekle8("DGRF_baglanti_plakasi", pl, "aluminyum", "SABIT",
          bom=("DGRF bağlantı plakası 6082-T6 · 20'den 16,5'e işlenmiş", 1, "162 × 173,5 · 4 × Ø11 + 2 × Ø12 H7 + 2 × Ø9", "üretim — 1870 N tepki M10'larda kesme", "ÜRETİM"))
    for i, (x, y) in enumerate(M10_XY):
        ekle8("DGRF_M10_civata_%d" % i, silz(x, y, 5.0, Z_PLAKA[0], Z_BAG + 17.0).union(silz(x, y, 8.0, Z_PLAKA[0] - 10.0, Z_PLAKA[0])), "celik", "SABIT",
              bom=("DIN 912 M10 × 35 A4-70 (DGRF gövdesi)", 4, "", "DIN 912", "SATIN ALMA") if i == 0 else None)
    for i, (x, y) in enumerate((M10_XY[0], M10_XY[3])):
        ekle8("DGRF_ZBH-12_%d" % i, silz(x, y, 6.0, Z_PLAKA[1] - 5.0, Z_BAG + 2.6).cut(silz(x, y, 5.0, Z_PLAKA[1] - 6.0, Z_BAG + 3.0)), "celik", "SABIT",
              bom=("Festo ZBH-12-B merkezleme burcu (DGRF ile gelir)", 2, "", KAYNAK_DGRF, "SATIN ALMA") if i == 0 else None)
    kiris = bul("kopru_kirisi_-286")
    for x in (135.0, 265.0):
        kiris["wp"] = kiris["wp"].cut(silz(x, sum(Y_KIRIS) / 2, 4.5, -307.0, -265.0))
        ekle8("DGRF_kiris_civatasi_%d" % (0 if x < 200 else 1), silz(x, sum(Y_KIRIS) / 2, 4.0, -306.0, Z_PLAKA[1] + 6.5).union(silz(x, sum(Y_KIRIS) / 2, 6.5, -314.0, -306.0))
              .union(hex_y(0, 0, 13.0, 0, 6.5).rotate((0, 0, 0), (1, 0, 0), 90).translate((x, sum(Y_KIRIS) / 2, Z_PLAKA[1]))), "celik", "SABIT",
              bom=("DIN 933 M8 × 60 A4 + somun (bağlantı plakası → arka köprü kirişi)", 2, "", "DIN 933 / 934", "SATIN ALMA") if x < 200 else None)
    # KESICI: boyunduruk + miller + piston + adaptör + ara dikmeler
    boy = pah_kutu(X_GOV[0], X_GOV[1], Y_BOYUN[0], Y_BOYUN[1], Z_BOYUN[0], Z_BOYUN[1], 12.0)
    for x in xr:
        boy = boy.cut(sily(x, ZC, DG["D4"] / 2, Y_BOYUN[0] - 1, Y_BOYUN[1] + 1))
    boy = boy.cut(sily(XC, ZC, DG["cubuk"] / 2, Y_BOYUN[0] - 1, Y_BOYUN[1] + 1))
    ekle8("DGRF_boyunduruk", boy, "aluminyum", "KESICI")
    for i, x in enumerate(xr):
        ekle8("DGRF_kilavuz_mili_%d" % i, sily(x, ZC, DG["D4"] / 2, Y_BOYUN[0], Y_GOV8[1] + DG["L2_0"] + DG["strok"]), "celik", "KESICI")
    ekle8("DGRF_piston_mili", sily(XC, ZC, DG["cubuk"] / 2, Y_BOYUN[0], PISTON[0]), "celik", "KESICI")
    ekle8("DGRF_piston", sily(XC, ZC, 31.5, PISTON[0], PISTON[1]), "aluminyum", "KESICI")
    adp = sily(XC, ZC, 85.0, Y_ADP[0], Y_ADP[1])
    ekle8("kafa_adaptoru", adp, "sac", "KESICI",
          bom=("Kafa adaptörü AISI 304 · 10 mm (boyunduruğun 4 × M8'ine: 80 × 40)", 1, "Ø170", "üretim", "ÜRETİM"))
    for i, phi in enumerate((30.0, 150.0, 270.0)):
        x, z = polar8(70.0, phi)
        ekle8("ara_dikme_%d" % i, sily(x, z, 8.0, Y_BOY8[0], Y_BOY8[1]), "celik", "KESICI",
              bom=("Ara dikme Ø16 × 70 paslanmaz (iki ucu M8)", 3, "v7: 50 — PulsaJet dik sığsın diye 70", "üretim", "ÜRETİM") if i == 0 else None)


# ---------------------------------------------------------------- SPREY: PulsaJet AAB10000AUH-03 + UniJet TG-W 2.8W ----------------------------------------------------------------
PJ = dict(r=18.9, duz=15.05, L=36.2, uc_af=20.6, uc_L=14.0, tip_r=6.0, tip_L=4.4, m8_ofs=11.1)
Y_PJ = (Y_KAFA[1], Y_KAFA[1] + PJ["L"])             # gövde 1174,5–1210,7
Y_UC8 = Y_KAFA[1] - PJ["uc_L"] - PJ["tip_L"]        # uç 1156,1


def sprey_v8():
    kp = bul("kafa_plakasi_8")
    kp["wp"] = kp["wp"].cut(sily(XC, ZC, 13.0, Y_KAFA[0] - 1, Y_KAFA[1] + 1))       # CP1325 somunu geçer (köşe r 11,9)
    gv = sily(XC, ZC, PJ["r"], Y_PJ[0], Y_PJ[1]).intersect(kut(XC - PJ["duz"], XC + PJ["duz"], Y_PJ[0] - 1, Y_PJ[1] + 1, ZC - 20, ZC + 20))
    ekle8("PulsaJet_AAB10000AUH-03", gv, "celik", "KESICI",
          bom=("Elektrikli sprey nozülü Spraying Systems PulsaJet AAB10000AUH-03-EPR (1/8 BSPT · EPDM)", 1,
               "24 VDC 0,36 A · PWM (PLC Q0.0) · ≤ 7 bar · ≤ 93 °C · 0,26 kg · UniJet uç ≤ -03 · gıda uygunluğu SORULACAK", KAYNAK_PJ, "SATIN ALMA"))
    ekle8("PulsaJet_uc_somunu_CP1325", hex_y(XC, ZC, PJ["uc_af"], Y_KAFA[1] - PJ["uc_L"], Y_KAFA[1]), "celik", "KESICI",
          bom=("UniJet uç somunu CP1325-SS (13/16\")", 1, "", "portal.spray.com CP1325 [ölçü V]", "SATIN ALMA"))
    ekle8("PulsaJet_uc_TG-W_2.8W", sily(XC, ZC, PJ["tip_r"], Y_UC8, Y_KAFA[1] - PJ["uc_L"]), "celik", "KESICI",
          bom=("UniJet TG-SS2.8W geniş açı tam koni uç", 1, "120° @ 0,7 bar (su) · 0,28 gpm @ 10 psi · PWM ~%55 → ≈ 7 g/s tereyağı [V: deneme]",
               "Spraying Systems katalog 75 s. B39", "SATIN ALMA"))
    zm = ZC - PJ["m8_ofs"]
    ekle8("PulsaJet_M8_soketi", sily(XC, zm, 4.5, Y_PJ[1], Y_PJ[1] + 8.1), "siyah", "KESICI")
    ekle8("PulsaJet_M8_acili_kablo", sily(XC, zm, 5.0, Y_PJ[1] + 8.1, Y_PJ[1] + 30.0).union(silx(Y_PJ[1] + 25.0, zm, 5.0, XC, XC + 30.0)), "siyah", "KESICI",
          bom=("M8 3 kutuplu 90° dişi kablo 5 m (PulsaJet -NC ile)", 1, "", "Murrelektronik / Lumberg M8 [V]", "SATIN ALMA"))
    ekle8("PulsaJet_giris_dirsegi", sily(XC, ZC, 5.5, Y_PJ[1], Y_PJ[1] + 16.0).union(silx(Y_PJ[1] + 11.0, ZC, 5.0, XC, XC + 25.0)), "celik", "KESICI",
          bom=("Paslanmaz geçme dirsek 1/8 BSPT → Ø6 (SMC KQG2L06-01S)", 1, "", "SMC KQG2 [V]", "SATIN ALMA"))
    ekle8("PulsaJet_isitici_ceket", sily(XC, ZC, PJ["r"] + 2.5, Y_PJ[0] + 6.0, Y_PJ[1] - 6.0).cut(sily(XC, ZC, PJ["r"], Y_PJ[0], Y_PJ[1])).intersect(
        kut(XC - 12.0, XC + 12.0, Y_PJ[0], Y_PJ[1], ZC - 30, ZC + 30)),
        "hortum_isi", "KESICI", bom=("Silikon ısıtıcı ceket 24 V 20 W + termostat (nozülde tereyağı donmasın · 45 °C)", 1, "", "[V]", "SATIN ALMA"))
    # yan braket: gövdenin +x düzlüğüne 2 × M4 (yan delikler 12,7 ara) → kafa plakasına 2 × M5
    xb = XC + PJ["duz"]
    ekle8("PulsaJet_braketi", kut(xb, xb + 3.0, Y_KAFA[1], Y_PJ[1] - 6.0, ZC - 15.0, ZC + 15.0).union(kut(xb, xb + 25.0, Y_KAFA[1], Y_KAFA[1] + 3.0, ZC - 15.0, ZC + 15.0)),
          "sac", "KESICI", bom=("PulsaJet L braketi 304 · 3 mm (yan M4 deliklerine)", 1, "", "üretim", "ÜRETİM"))
    # ısıtmalı hortum (kafada, hareketli): dirsek → +x → yukarı → öne → köprü altındaki bağlantıya (strok boyunca serbest halka [animasyonda kafayla iner])
    ekle8("isitmali_hortum_kafa", boru([(XC + 25.0, Y_PJ[1] + 11.0, ZC), (300.0, Y_PJ[1] + 11.0, ZC), (300.0, 1300.0, ZC), (300.0, 1300.0, -126.0), (300.0, 1395.0, -126.0)], 7.0),
          "hortum_isi", "KESICI")
    # sprey konisi (görsel · yalnız sprey anında) — 120° koni, ürün üstünde r 145'te kesilir
    ekle8("sprey_konisi", cq.Workplane(obj=cq.Solid.makeCone(145.0, 3.0, Y_UC8 - (BANT + PZ_H), cq.Vector(XC, BANT + PZ_H, ZC), cq.Vector(0, 1, 0))), "sprey", "SPREY")


# ---------------------------------------------------------------- TANK (alt dolap) + ısıtmalı hortum ----------------------------------------------------------------
TANK8 = dict(x=200.0, z=-540.0, r=86.5, y0=128.0)
X_HAT, Z_HAT = 380.0, -600.0                        # arkadaki dikey hortum yolu (itici, X tabanı ve bant profilinin dışında)
TANK_SIL = ("yag_tanki_3L", "yag_tanki_kapagi", "yag_tanki_rafi", "yag_raf_askisi_90", "yag_raf_askisi_310")


def tank_v8():
    cikar(*TANK_SIL)
    x, z, r, y0 = TANK8["x"], TANK8["z"], TANK8["r"], TANK8["y0"]
    tava = kut(80.0, 320.0, 126.0, 146.0, -660.0, -420.0).cut(kut(82.0, 318.0, 128.0, 147.0, -658.0, -422.0))
    ekle8("yag_tanki_damlama_tavasi", tava, "sac", "SABIT", bom=("Damlama tavası AISI 304 · 2 mm", 1, "240 × 240 × 20", "üretim", "ÜRETİM"))
    ekle8("yag_tanki_ayak_halkasi", sily(x, z, 80.0, y0, y0 + 20.0).cut(sily(x, z, 76.0, y0 - 1, y0 + 21.0)), "sac", "SABIT")
    ekle8("yag_tanki_MDG3", sily(x, z, r, y0 + 20.0, y0 + 384.0).cut(sily(x, z, r - 1.5, y0 + 22.0, y0 + 382.0)), "sac", "SABIT",
          bom=("Basınçlı malzeme tankı Walther Pilot MDG 3 paslanmaz (3 bar sürümü)", 1, "3,2 L dolum / 2,5 L kullanılır · iç Ø125 · dış Ø173 · 454 yükseklik · 2 gün = 1,41 L",
               "walther-pilot.de MDG 3 · gıda uygunluğu [V]", "SATIN ALMA"))
    ekle8("yag_tanki_kapagi", sily(x, z, r + 1.5, y0 + 384.0, y0 + 404.0), "sac", "SABIT")
    ekle8("yag_tanki_isitici_ceketi", sily(x, z, r + 5.0, y0 + 80.0, y0 + 330.0).cut(sily(x, z, r, y0 + 70.0, y0 + 340.0)), "hortum_isi", "SABIT",
          bom=("Tank ısıtıcı ceketi silikon 230 V 150 W + PT100 (45 °C)", 1, "Ø173 × 250", "[V]", "SATIN ALMA"))
    ekle8("yag_tanki_regulatoru", sily(x - 40.0, z, 15.0, y0 + 404.0, y0 + 440.0).union(silz(x - 40.0, y0 + 425.0, 12.0, z + 13.0, z + 25.0)), "aluminyum", "SABIT",
          bom=("Tank basınç regülatörü + manometre 0–3 bar (MDG kapağında)", 1, "", "Walther Pilot [V]", "SATIN ALMA"))
    ekle8("yag_tanki_emniyet_valfi", sily(x + 5.0, z - 45.0, 8.0, y0 + 404.0, y0 + 430.0), "celik", "SABIT")
    ekle8("yag_tanki_cikis_rakoru", sily(x + 40.0, z, 8.0, y0 + 404.0, y0 + 420.0), "celik", "SABIT")
    ekle8("yag_seviye_sensoru", sily(x + 5.0, z + 45.0, 6.0, y0 + 404.0, y0 + 434.0), "sensor", "SABIT",
          bom=("Kapasitif seviye sensörü (gıda · 2 gün kala uyarır)", 1, "", "[V]", "SATIN ALMA"))
    yh = y0 + 420.0                                                              # 548
    yb = 1410.0                                                                  # köprü kirişlerinin 2,5 mm altı
    ekle8("isitmali_hortum_Ø6", boru([(x + 40.0, yh, z), (x + 40.0, 640.0, z), (X_HAT, 640.0, z), (X_HAT, 640.0, Z_HAT), (X_HAT, yb, Z_HAT), (300.0, yb, Z_HAT), (300.0, yb, -135.0)], 7.0),
          "hortum_isi", "SABIT", bom=("Isıtmalı gıda hortumu Ø6 iç · 24 V · 45 °C (izolasyonlu Ø14)", 1, "≈ 2,6 m sabit + 0,4 m kafa (serbest halka)", "[V]", "SATIN ALMA"))
    ekle8("hortum_baglantisi_kafa", sily(300.0, -126.0, 9.0, 1395.0, yb + 7.0).cut(sily(300.0, -126.0, 7.2, 1394.0, 1402.0)), "celik", "SABIT",
          bom=("Isıtmalı hortum birleşme parçası + köprü kelepçesi", 1, "", "[V]", "SATIN ALMA"))
    ekle8("hortum_baglantisi_askisi", kut(292.0, 308.0, yb + 7.0, Y_KIRIS[0], -134.0, -118.0), "sac", "SABIT")
    tab = bul("istasyon_tabani_3")
    tab["wp"] = tab["wp"].cut(sily(X_HAT, Z_HAT, 16.25, 890.0, 897.0))
    rk = sily(X_HAT, Z_HAT, 16.25, 895.0, 903.0).union(sily(X_HAT, Z_HAT, 18.0, 885.0, 892.0))
    rk = rk.cut(sily(X_HAT, Z_HAT, 7.0, 884.0, 904.0)).cut(sily(368.0, -596.0, 3.0, 884.0, 904.0))
    ekle8("taban_hortum_rakoru", rk, "siyah", "SABIT",
          bom=("Lapp SKINTOP MS-SC M32 çok delikli geçiş rakoru (ısıtmalı hortum Ø14 + tank havası Ø6 · istasyon tabanı)", 1, "", "lapp.com [V]", "SATIN ALMA"))


# ---------------------------------------------------------------- PANO + PNÖMATİK ----------------------------------------------------------------
Z_PL = -818.0                                        # pano plakasının ön yüzü
Y_HAVA_GIRIS, Z_HAVA_GIRIS = 1809.0, -770.0          # v87: hattın ana hava dalı K sol duvarına burada girer (hat_montaj: fırın üstü 1977 + DY −168)
PANO_SIL = ("pano_elektrik_zarfi", "sartlandirici_MS4")


def pano_v8():
    cikar(*PANO_SIL)
    zr = Z_PL + 7.5                                  # DIN ray önü
    for i, (y, xr1) in enumerate(((1742.5, 330.0), (1622.5, 260.0))):
        ekle8("din_rayi_%d" % i, kut(70.0, xr1, y, y + 35.0, Z_PL, zr), "celik", "SABIT", bom=("DIN ray 35 × 7,5", 2, "boy 260 / 190", "EN 60715", "SATIN ALMA") if i == 0 else None)
    for i, (bx, by) in enumerate(((80.0, 1482.0), (320.0, 1482.0), (80.0, 1847.0), (320.0, 1847.0))):   # pano plakası arka saca 4 ara burçla
        ekle8("pano_ara_burcu_%d" % i, silz(bx, by, 5.0, -828.5, -822.0), "celik", "SABIT", bom=("Ara burç M5 × 6,5 paslanmaz", 4, "", "katalog", "SATIN ALMA") if i == 0 else None)
    ekle8("guc_24V_NDR-240-24", TC.din_parca(TC.GUC_STEP, 75.0, 1697.4, zr + 122.8), "aluminyum", "SABIT",
          bom=("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · PLC, EC5000, PulsaJet, valfler, sensörler", "TraceParts STEP (gerçek CAD)", "SATIN ALMA"))
    ekle8("plc_S7-1200_1214C", kut(145.0, 255.0, 1710.0, 1810.0, zr, zr + 75.0), "siemens", "SABIT",
          bom=("Siemens S7-1200 CPU 1214C DC/DC/DC · 6ES7214-1AG40-0XB0", 1, "14 DI / 10 DO / 2 AI · Q0.0 PWM → PulsaJet · 415 g", "Siemens veri sayfası (automation24 kopyası)", "SATIN ALMA"))
    for i in range(2):
        ekle8("sicaklik_kontrol_E5DC_%d" % i, kut(260.0 + 24.0 * i, 282.5 + 24.0 * i, 1712.0, 1808.0, zr, zr + 85.6), "siyah", "SABIT",
              bom=("Omron E5DC DIN ray sıcaklık kontrolcüsü (tank · hortum)", 2, "22,5 × 96 × 85,6 · PT100", "omron [V]", "SATIN ALMA") if i == 0 else None)
    for i in range(2):
        ekle8("SSR_G3PE_%d" % i, kut(75.0 + 25.0 * i, 97.5 + 25.0 * i, 1590.0, 1690.0, zr, zr + 100.0), "siyah", "SABIT",
              bom=("Omron G3PE-215B DIN SSR (tank 150 W · hortum)", 2, "22,5 × 100 × 100", "omron [V]", "SATIN ALMA") if i == 0 else None)
    ekle8("sigorta_C10", kut(130.0, 166.0, 1597.5, 1682.5, zr, zr + 70.0), "plastik", "SABIT", bom=("Otomatik sigorta 1P+N C10", 1, "36 × 85 × 70", "[V]", "SATIN ALMA"))
    ekle8("klemens_sirasi", kut(172.0, 255.0, 1616.0, 1664.0, zr, zr + 49.0), "plastik", "SABIT", bom=("Klemens Phoenix UT 2,5", 16, "5,2 × 47,5 × 49", "phoenixcontact.com [V]", "SATIN ALMA"))
    # valf adası SS5Y3-20-04 (x boyunca 69,5 · genişlik y 49 · taban 20) + 3 × SY3120 + kör plaka
    xm0, ym0 = 72.0, 1482.0
    ekle8("valf_adasi_SS5Y3-20-04", kut(xm0, xm0 + 69.5, ym0, ym0 + 49.0, Z_PL, Z_PL + 20.0), "aluminyum", "SABIT",
          bom=("SMC SS5Y3-20-04 manifold (4 istasyon · 10,5 hatve · P/EA/EB 1/8)", 1, "69,5 × 49 × 20 · 87 g", "SMC SY3000 katalog 1-4-45 (2005) [güncel CAD ile teyit]", "SATIN ALMA"))
    for i in range(4):
        xv = xm0 + 19.0 + 10.5 * i
        if i < 3:
            ekle8("valf_SY3120_%d" % i, kut(xv - 5.0, xv + 5.0, ym0, ym0 + 66.9, Z_PL + 20.0, Z_PL + 49.0), "siyah", "SABIT",
                  bom=("SMC SY3120-5LZ-C6 5/2 tek bobinli valf (X itici · Z itici · kesici)", 3, "10 geniş · 66,9 boy · 24 VDC", "SMC SY3000 katalog 1-4-12", "SATIN ALMA") if i == 0 else None)
            for j, yf in enumerate((ym0 + 8.0, ym0 + 18.2)):
                ekle8("valf_SY3120_%d_rakor_%d" % (i, j), silz(xv, yf, 4.2 if i == 2 else 3.2, Z_PL + 49.0, Z_PL + 54.1), "siyah", "SABIT")
        else:
            ekle8("valf_kor_plaka", kut(xv - 5.0, xv + 5.0, ym0, ym0 + 49.0, Z_PL + 20.0, Z_PL + 30.0), "aluminyum", "SABIT",
                  bom=("SMC SY3000-26-9A kör plaka (yedek istasyon)", 1, "", "SMC SY3000 katalog 1-4-42", "SATIN ALMA"))
    # şartlandırıcı AW20-F02-A (40 geniş · 155 boy · port ekseni üstten 67,4)
    xa, ya0, ya1 = 310.0, 1482.0, 1637.0
    za = Z_PL + 2.3 + 20.0
    aw = kut(xa - 20.0, xa + 20.0, ya1 - 90.0, ya1 - 45.0, za - 20.0, za + 20.0)
    aw = aw.union(sily(xa, za, 18.0, ya0, ya1 - 90.0)).union(sily(xa, za, 17.0, ya1 - 45.0, ya1)).union(silz(xa, ya1 - 67.4, 18.75, za + 20.0, za + 30.0))
    ekle8("sartlandirici_AW20-F02-A", aw, "aluminyum", "SABIT",
          bom=("SMC AW20-F02-A filtre regülatör (5 µm · 0,05–0,7 MPa) + manometre", 1, "40 × 155 · 0,21 kg", "SMC AW-A katalog s. 474", "SATIN ALMA"))
    ekle8("sartlandirici_braketi", kut(xa - 22.0, xa + 22.0, ya1 - 72.0, ya1 - 62.0, Z_PL, Z_PL + 2.3), "sac", "SABIT",
          bom=("SMC B240A şartlandırıcı braketi (2,3 mm)", 1, "", "SMC AW-A katalog s. 474 [V]", "SATIN ALMA"))
    # hava girişi (arka sac) → AW20 IN (+x) · AW20 OUT (−x) → manifold P (sağ uç, x 141,5)
    yp = ya1 - 67.4
    # v87 (montaj): hattın ana hava dalı fırın üstü kabinden K'nın SOL duvarına (y 1809, z −780) gelir (hat_montaj ANA_K48) → duvar rakoru → pano önünden AW20 girişine
    sol = bul("sol_sac_urun_girisi")
    sol["wp"] = sol["wp"].cut(silx(Y_HAVA_GIRIS, Z_HAVA_GIRIS, 7.0, -1.0, 3.0))
    ekle8("hava_giris_rakoru", silx(Y_HAVA_GIRIS, Z_HAVA_GIRIS, 7.0, -6.0, 8.0), "celik", "SABIT",
          bom=("Paslanmaz duvar geçiş rakoru 1/4 → Ø8 (sol sac · hattın ana hava dalı)", 1, "", "[V]", "SATIN ALMA"))
    ekle8("hava_hortumu_giris", boru([(8.0, Y_HAVA_GIRIS, Z_HAVA_GIRIS), (40.0, Y_HAVA_GIRIS, Z_HAVA_GIRIS), (40.0, Y_HAVA_GIRIS, -680.0), (345.0, Y_HAVA_GIRIS, -680.0),
                                      (345.0, yp, -680.0), (345.0, yp, za), (xa + 20.0, yp, za)], 4.0), "hava", "SABIT",
          bom=("PU hortum Ø8 / Ø6 / Ø4 (Festo PUN-H)", 1, "≈ 3,5 m toplam", "festo.com PUN-H [V]", "SATIN ALMA"))
    ekle8("hava_hortumu_manifold", boru([(xa - 20.0, yp, za), (160.0, yp, za), (160.0, ym0 + 12.0, za), (160.0, ym0 + 12.0, Z_PL + 10.0), (xm0 + 69.5, ym0 + 12.0, Z_PL + 10.0)], 3.0), "hava", "SABIT")


def pnomatik_v8():
    """DGRF (2 × Ø8) · X silindiri (2 × Ø4) · tank (Ø6) — Z silindirinin hortumları X arabasıyla gider (spiral hortum [V], modelde yok)"""
    xp = XC + DG["J"]
    yp1, yp2 = Y_GOV8[0] + DG["PL1"], Y_ARKA - DG["PL"]
    zt = Z_GOV[1] + 12.0                                                          # −153,5
    ym0 = 1482.0
    ekle8("hava_hortumu_DGRF_on", boru([(226.0, yp1 + 12.0, zt), (226.0, 1600.0, zt), (226.0, 1600.0, -700.0), (112.0, 1600.0, -700.0),
                                        (112.0, ym0 + 18.2, -700.0), (112.0, ym0 + 18.2, Z_PL + 54.1)], 3.0), "hava", "SABIT")
    ekle8("hava_hortumu_DGRF_arka", boru([(xp, yp2 + 20.0, zt), (xp, 1612.0, zt), (xp, 1612.0, -690.0), (112.0, 1612.0, -690.0), (112.0, ym0 + 8.0, -690.0),
                                          (112.0, ym0 + 8.0, Z_PL + 54.1)], 3.0), "hava", "SABIT")
    # X silindiri: AS1201F'ler x 367,5 · y 993,2 · z −706 / −694 → sağ duvar boyunca yukarı → pano önünde manifold 0'a
    for i, (zf, zu, yv) in enumerate(((-706.0, -730.0, ym0 + 18.2), (-694.0, -724.0, ym0 + 8.0))):
        yu = 1540.0 + 8.0 * i
        xv = 386.0 + 6.0 * i
        ekle8("hava_hortumu_X_%d" % i, boru([(377.5, 993.2, zf), (xv, 993.2, zf), (xv, 993.2, zu), (xv, 1405.0 - 6.0 * i, zu), (355.0, 1405.0 - 6.0 * i, zu),
                                             (355.0, yu, zu), (91.0, yu, zu), (91.0, yv, zu), (91.0, yv, Z_PL + 54.1)], 2.0), "hava", "SABIT")
    # tank havası: AW20 çıkışından (manifold öncesi T) → sağ duvar → alt dolap → tank regülatörü
    ekle8("hava_hortumu_tank", boru([(230.0, 1569.6, -792.7), (230.0, 1569.6, -640.0), (230.0, 1398.0, -640.0), (368.0, 1398.0, -640.0), (368.0, 1398.0, -596.0),
                                     (368.0, 700.0, -596.0), (TANK8["x"] - 40.0, 700.0, -596.0), (TANK8["x"] - 40.0, 700.0, TANK8["z"]),
                                     (TANK8["x"] - 40.0, TANK8["y0"] + 440.0, TANK8["z"])], 3.0), "hava", "SABIT")


# ---------------------------------------------------------------- BOM (v7 parçaları) ----------------------------------------------------------------
BOM_V7 = {
    "kose_dikmesi": ("Köşe dikmesi 304 kare profil 30 × 30 × 2 (EN 10296-2)", 4, "1736", "üretim", "ÜRETİM"),
    "onyuz_kayit": ("Ön / arka kayıt 304 kare profil 30 × 30 × 2", 6, "330", "üretim", "ÜRETİM"),
    "taban_sac_tasiyici": ("Taban sacı taşıyıcı 30 × 30 × 2", 2, "812", "üretim", "ÜRETİM"),
    "taban_sac_3": ("Taban sacı AISI 304 3 mm", 1, "397 × 888", "üretim (lazer)", "ÜRETİM"),
    "istasyon_tabani_3": ("İstasyon tabanı AISI 304 3 mm (y 892–895) · 2 rakor deliği", 1, "397 × 888", "üretim", "ÜRETİM"),
    "arka_sac": ("Arka sac AISI 304 1,5", 1, "400 × 1736", "üretim", "ÜRETİM"),
    "ust_sac": ("Üst sac AISI 304 1,5", 1, "400 × 889", "üretim", "ÜRETİM"),
    "sol_sac_urun_girisi": ("Sol yan sac 1,5 · fırından ürün girişi açıklığı", 1, "1734,5 × 887,5", "üretim (lazer)", "ÜRETİM"),
    "sag_sac_E_penceresi": ("Sağ yan sac 1,5 · E'ye pizza penceresi", 1, "1734,5 × 887,5", "üretim (lazer)", "ÜRETİM"),
    "onyuz_kapak_alt": ("Ön kapak tava 20 mm AISI 304 fırçalı 1,5 (alt · orta · üst)", 3, "derz 3 · ön düzlem +79", "üretim", "ÜRETİM"),
    "plint_on": ("Plint 1,5 (60 geride)", 1, "400 × 123", "üretim", "ÜRETİM"),
    "bant_yan_-421": ("Bant yan profili 304 6 mm (EC5000 11 HEX + M8 + avara Ø12 delikli)", 2, "390 × 55", "üretim (lazer)", "ÜRETİM"),
    "bant_ayagi": ("Bant ayağı 304 kutu 20 × 20 × 2", 4, "37,5", "üretim", "ÜRETİM"),
    "kayma_tablasi": ("Kayma tablası UHMW-PE 6 mm (gıda, FDA)", 1, "254 × 396 · kesme yükünü taşır", "üretim", "ÜRETİM"),
    "bant_PU_ust": ("Habasit CD.F20-A-UW gıda bandı 2,0 mm beyaz TPU (EU 10/2011 + FDA · min kasnak Ø25) · Quickmelt ekli", 1, "380 × ≈ 780",
                    "Habasit PDS CD.F20-A-UW (09.05.2025) · ürün no H800006238", "SATIN ALMA"),
    "olu_plaka": ("Çıkış ölü plakası 304 (bant → E penceresi · profillere kaynaklı)", 1, "18 × 412", "üretim", "ÜRETİM"),
    "cit_on": ("Kılavuz çit POM beyaz 5 × 6 (ön · arka · giriş eğik)", 5, "ürünü 36 mm z −206'ya kaydırır", "üretim", "ÜRETİM"),
    "kopru_kirisi_yan_20": ("Köprü kirişi 304 30 × 40 × 2 (yan + enine)", 4, "kesici taşıyıcı", "üretim", "ÜRETİM"),
    "pano_plakasi": ("Pano montaj plakası 304 4 mm (arka sacta)", 1, "265 × 385", "üretim", "ÜRETİM"),
    "itici_sabit_plaka": ("X ekseni taban plakası 6082 6 mm", 1, "380 × 170", "üretim", "ÜRETİM"),
    "itici_X_ray_-755": ("HIWIN MGNR15R ray · X · boy 360 (P 40 · E 20)", 2, "ray 15 × 10 · M3 × 10 · 1,06 kg/m", KAYNAK_HIWIN, "SATIN ALMA"),
    "itici_X_blok_-755": ("HIWIN MGN15H blok · X", 2, "W 32 · L 58,8 · H 16 · C 6,37 kN · 92 g", KAYNAK_HIWIN, "SATIN ALMA"),
    "itici_Z_ray_53": ("HIWIN MGNR15R ray · Z · boy 460 (P 40 · E 10)", 2, "", KAYNAK_HIWIN, "SATIN ALMA"),
    "itici_Z_blok_53": ("HIWIN MGN15H blok · Z", 2, "W 32 · L 58,8 · H 16", KAYNAK_HIWIN, "SATIN ALMA"),
    "itici_Z_plaka": ("Z ekseni taban plakası 6082 5 mm (X arabası üstünde)", 1, "76 × 460", "üretim", "ÜRETİM"),
    "itici_yuz": ("İtici yüzü POM 8 mm (gıda) · pasif düşey 15 mm yüzer", 1, "300 × 24", "üretim", "ÜRETİM"),
    "eksen_ayagi": ("X ekseni ayağı 304 kutu 20 × 20", 4, "63", "üretim", "ÜRETİM"),
    "itici_taban": ("X ekseni ayak tabanı 304 8 mm", 4, "36 × 36", "üretim", "ÜRETİM"),
    "itici_X_ara": ("X arabası ara blok 6082 (MGN15H → Z plakası)", 2, "58,8 × 66 × 32", "üretim", "ÜRETİM"),
    "itici_Z_yukseltme": ("Z ray yükseltmesi 6082 15 × 25", 2, "460", "üretim", "ÜRETİM"),
    "itici_Z_kopru": ("Z köprü plakası 6082 5 mm", 1, "88 × 65", "üretim", "ÜRETİM"),
    "itici_one_kol": ("İtici kolu 304 (öne · düşey · yatay)", 3, "", "üretim", "ÜRETİM"),
    "itici_yuz_kilavuz": ("İtici yüzü kılavuzu 304 (yüzer dil + kovan)", 2, "", "üretim", "ÜRETİM"),
    "itici_alt_dudak": ("İtici alt dudağı POM 2 mm", 1, "300", "üretim", "ÜRETİM"),
    "kafa_plakasi_8": ("Kafa plakası Ø230 × 8 AISI 304 (orta Ø26: uç somunu)", 1, "", "lazer + CNC", "ÜRETİM"),
}


def bom_v7():
    for p in PARCALAR:
        if p.get("bom"):
            continue
        for k, b in BOM_V7.items():
            if p["ad"] == k or (k.endswith("_") and p["ad"].startswith(k)) or (not k.endswith("_") and p["ad"].startswith(k) and p["ad"] == k):
                p["bom"] = b
                break
        else:
            for k, b in BOM_V7.items():
                if not k.endswith("_") and p["ad"].startswith(k.rsplit("_", 1)[0] + "_") and k.startswith(("kose_dikmesi", "onyuz_kayit", "taban_sac_tasiyici", "eksen_ayagi", "itici_taban", "itici_X_ara")):
                    p["bom"] = b
                    break


# ---------------------------------------------------------------- v7 DÜZELTMELERİ (durağan kesişimler · Codex zarfları) ----------------------------------------------------------------
def duzelt_v7():
    """v7'de 32 durağan kesişim vardı (ör. köşe dikmeleri tabandan / üst sacdan geçiyordu, itici kolları iç içe) — hepsi temasa çevrilir"""
    for x in (20, 380):
        for z in (-800, 42):
            bul("kose_dikmesi_%d_%d" % (x, z))["wp"] = kut(x - 15, x + 15, 126.0, 1860.5, z - 15, z + 15).cut(kut(x - 13, x + 13, 125.0, 1861.5, z - 13, z + 13))
    w = kut(1.5, 398.5, 892.0, 895.0, -828.5, 59.0)
    for x in (20, 380):
        for z in (-800, 42):
            w = w.cut(kut(x - 15, x + 15, 891.0, 896.0, z - 15, z + 15))
    bul("istasyon_tabani_3")["wp"] = w
    bul("ust_sac")["wp"] = kut(0.0, 400.0, 1860.5, 1862.0, -828.5, 59.0)
    for z in (-800, 42):
        bul("onyuz_kayit_140_%d" % z)["wp"] = kut(35.0, 365.0, 126.0, 156.0, z - 15, z + 15).cut(kut(34.0, 366.0, 128.0, 154.0, z - 13, z + 13))
    for x in (20, 380):
        bul("taban_sac_tasiyici_%d" % x)["wp"] = kut(x - 15, x + 15, 126.0, 156.0, -785.0, 27.0).cut(kut(x - 13, x + 13, 128.0, 154.0, -786.0, 28.0))
    for side in (-1, 1):
        c = bul("cit_giris_%d" % side)
        c["wp"] = c["wp"].intersect(kut(-10.0, 100.0, 990.0, 1010.0, -420.0, 40.0))
    for x in (40, 360):
        for z in (-755, -645):
            bul("eksen_ayagi_%d_%d" % (x, z))["wp"] = kut(x - 10, x + 10, 903.0, 958.0, z - 10, z + 10).cut(kut(x - 8, x + 8, 902.0, 959.0, z - 8, z + 8))
    bul("itici_dusey_kol")["wp"] = kut(115.0, 135.0, 1028.0, 1097.0, -566.0, -546.0)
    bul("itici_yatay_kol")["wp"] = kut(135.0, 247.0, 1028.0, 1040.0, -566.0, -546.0)
    bul("itici_yuzer_kilavuz")["wp"] = kut(251.0, 261.0, 1020.3, 1040.0, -572.0, -540.0)
    bul("itici_alt_dudak")["wp"] = kut(258.0, 260.0, 996.0, 996.3, -706.0, -406.0)          # yüzün ön alt kenarının ALTINDA (v7: yüzün içindeydi)
    bul("olu_plaka")["wp"] = kut(382.0, 398.5, 990.0, 996.0, -418.0, -6.0)
    # v87 (montaj): ayaklar MODÜLER STANDARDA (moduler_montaj_v3 M12 yuvası · K v6 ile aynı düzen): M12 mil + Ø40 taban, süpürgeliğin (z 17,5–19) gerisinde
    # (v7: Ø16, köşe dikmelerinin altında z 42 — ön ayaklar süpürgeliğin önünde kalıyordu, modüler şasi süpürgeliği kesiyordu)
    cikar(*["ayak_%d_%d" % (x, z) for x in (20, 380) for z in (-800, 42)])
    for i, (x, z) in enumerate(((50.0, -110.0), (350.0, -110.0), (50.0, -770.0), (350.0, -770.0))):
        ekle8("ayak_%d_%d" % (x, z), sily(x, z, 20.0, 0.0, 8.0).union(sily(x, z, 6.0, 8.0, Y_PLINT)), "celik", "SABIT",
              bom=("Hijyenik ayar ayağı M12 paslanmaz, Ø40 taban (Elesa LV.A sınıfı · modüler M12 yuvasına)", 4, "yerden 123 taban", "Elesa LV.A [V]", "SATIN ALMA") if i == 0 else None)


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    K7.modul()
    duzelt_v7(); itici_v8(); bant_v8(); sensor_v8(); kesici_v8(); sprey_v8(); tank_v8(); pano_v8(); pnomatik_v8(); bom_v7()
    return PARCALAR


# ---------------------------------------------------------------- KÜTLE (CAD hacmi × yoğunluk) ----------------------------------------------------------------
YOGUNLUK = dict(celik=7.9e-6, sac=7.9e-6, kabuk=7.9e-6, on_seffaf=7.9e-6, aluminyum=2.7e-6, pom=1.41e-6, siyah=1.2e-6, sensor=1.3e-6, plastik=1.4e-6,
                siemens=0.5e-6, hortum_isi=3.2e-6, hava=1.2e-6, pu_bant=1.2e-6, kart=1.8e-6)
HAREKETLI_GRUP = ("KESICI", "ITICI_ARABA", "ITICI_CAPRAZ", "ITICI_KOL", "ITICI_YUZ")


def grup_kutleleri():
    """kg · modul() kurulmuş olmalı"""
    k = {}
    for p in PARCALAR:
        if p["grup"] in HAREKETLI_GRUP:
            k[p["grup"]] = k.get(p["grup"], 0.0) + p["wp"].val().Volume() * YOGUNLUK.get(p["mal"], 2.7e-6)
    k = {g: round(v, 3) for g, v in k.items()}
    k["Z_hareketli"] = round(k.get("ITICI_CAPRAZ", 0) + k.get("ITICI_KOL", 0) + k.get("ITICI_YUZ", 0), 3)
    k["X_hareketli"] = round(k["Z_hareketli"] + k.get("ITICI_ARABA", 0), 3)
    return k


# ---------------------------------------------------------------- ZAMAN (katalog sınırlarıyla) ----------------------------------------------------------------
def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    u = (t - a) / (b - a); return u * u * (3.0 - 2.0 * u)


V_A_Z = 120.0                                    # mm/s ortalama · Z (lastik tampon): çarpma 1,4 × 120 = 168 ≤ 0,9 × sınır (hesap: zaman_denetimi)
V_A_X = 150.0                                    # mm/s ortalama · X (H ünitesi RB0805): E = ½ m v² ≪ 1,0 J
Z_GELIS = (0.3, 2.3)                             # bant 260 mm (EC5000 tepe 195 mm/s ≤ 370)
Z_SPREY = (2.6, 3.8)                             # PulsaJet PWM 1,2 s ≈ 8 g
Z_KES = (4.0, 5.4, 5.7, 6.5)                     # DGRF iner 125 (1,4 s) · bekler · kalkar (0,8 s)
Z_TASI = (6.6, 8.4)                              # bant 220 mm (tepe 183 mm/s)
T_Z = round(350.0 / V_A_Z, 2)                    # 2,92 s
T_X = round(250.0 / V_A_X, 2)                    # 1,67 s
Z_IN = (7.8, round(7.8 + T_Z, 2))                # itici yüzü ürünün z aralığına dz 50'de girer (t ≈ 8,49) — ürün arka kenarı o an 270 (yüz 260)
Z_ITME = (round(Z_IN[1] + 0.1, 2), round(Z_IN[1] + 0.1 + T_X, 2))
Z_DUS = (round(Z_ITME[1] + 0.3, 2), round(Z_ITME[1] + 0.7, 2))       # ürün kutuya oturur (v7 ile aynı 0,3 + 0,4)
Z_X_DON = (round(Z_ITME[1] + 0.15, 2), round(Z_ITME[1] + 0.15 + T_X, 2))
Z_Z_DON = (round(Z_X_DON[1] + 0.1, 2), round(Z_X_DON[1] + 0.1 + T_Z, 2))
OLAY_ANLARI = tuple(sorted(set(sum((list(a) for a in (Z_GELIS, Z_SPREY, Z_KES, Z_TASI, Z_IN, Z_ITME, Z_DUS, Z_X_DON, Z_Z_DON)), []))))


# ürün z'si: v7 ease'i (−170 → −206) ÇİTLE sınırlı — ürün ön çite değene kadar serbest, değince çit onu iter (v7'de ürün çitlere 1–3 mm giriyordu)
def _seg_mesafe(px, pz, ax, az, bx, bz):
    vx, vz = bx - ax, bz - az
    u = max(0.0, min(1.0, ((px - ax) * vx + (pz - az) * vz) / (vx * vx + vz * vz)))
    return math.hypot(px - (ax + u * vx), pz - (az + u * vz))


_d = (92.0, -76.0)
_L = math.hypot(*_d)
_n = (_d[1] / _L, -_d[0] / _L)                    # eğik çitin iç normali (−0,637, −0,771)
CIT_ON_YUZLER = (((8.0 + 3.0 * _n[0], 25.0 + 3.0 * _n[1]), (100.0 + 3.0 * _n[0], -51.0 + 3.0 * _n[1])), ((100.0, -54.0), (400.0, -54.0)))
PAY_CIT = 0.3


def _z_cit(x):
    lo, hi = -260.0, -170.0
    ok = lambda z: all(_seg_mesafe(x, z, a[0], a[1], b[0], b[1]) >= PZ_R + PAY_CIT for a, b in CIT_ON_YUZLER)
    if ok(hi): return hi
    for _ in range(40):
        m = (lo + hi) / 2.0
        if ok(m): lo = m
        else: hi = m
    return lo


_ZC_TABLO = {i: _z_cit(float(i)) for i in range(-60, 421, 2)}


def urun_z(x, t=None):
    """v87: ürün z'si YALNIZ çitten (ürün çite değene kadar −170, değince çit onu iter · Codex v7'nin zamanla kayması fiziksel değildi, fırın çıkışında
    ürünü yana kaydırıyordu) · itmede (x 420 → 548,5, ürün E kalıp rayına inerken) E'nin kutu eksenine −206 doğrusal"""
    xi = max(-60, min(420, int(round(x / 2.0)) * 2))
    if x <= 420.0:
        return _ZC_TABLO[xi]
    u = min(1.0, (x - 420.0) / (548.5 - 420.0))
    return _ZC_TABLO[420] + (-206.0 - _ZC_TABLO[420]) * u


def state(t):
    fx = 260.0 + 250.0 * ss(Z_ITME[0], Z_ITME[1], t) - 250.0 * ss(Z_X_DON[0], Z_X_DON[1], t)
    pz = -556.0 + 350.0 * ss(Z_IN[0], Z_IN[1], t) - 350.0 * ss(Z_Z_DON[0], Z_Z_DON[1], t)
    cut = 125.0 * ss(Z_KES[0], Z_KES[1], t) * (1.0 - ss(Z_KES[2], Z_KES[3], t))
    x = -60.0 + 260.0 * ss(Z_GELIS[0], Z_GELIS[1], t)
    if t >= Z_TASI[0]:
        x = 200.0 + 220.0 * ss(Z_TASI[0], Z_TASI[1], t)
    if t >= Z_ITME[0]:
        x = 660.0 if t >= Z_X_DON[0] else max(420.0, fx + 150.0)      # yüz ürünün arka kenarına fx 270'te değer (v7 ile aynı temas)
    return dict(fx=fx, pz=pz, x=x, z=urun_z(x, t), follow=14.5 * max(0.0, min(1.0, (fx - 8.0 - 398.5) / 53.0)), cut=cut)


def grup_trs(g, t):
    s_ = state(t); dx = s_["fx"] - 260.0; dz = s_["pz"] + 556.0
    return {"KESICI": (0.0, -s_["cut"], 0.0), "ITICI_ARABA": (dx, 0.0, 0.0), "ITICI_CAPRAZ": (dx, 0.0, dz), "ITICI_KOL": (dx, 0.0, dz),
            "ITICI_YUZ": (dx, -s_["follow"], dz)}.get(g, (0.0, 0.0, 0.0))


X_INIS = (420.0, 548.5)                           # v7: 397–450 (ürün beklerken bandın 6,3 mm içindeydi) · E kalıp rayı 981,5 (kutu_cad_v11 KALIP)


def urun_merkez(t):
    s_ = state(t)
    x = s_["x"]
    y = 996.0 - 14.5 * max(0.0, min(1.0, (x - X_INIS[0]) / (X_INIS[1] - X_INIS[0])))
    k = ss(Z_DUS[0], Z_DUS[1], t)
    y = y * (1.0 - k) + 937.6 * k
    return x, y, s_["z"]


# ---------------------------------------------------------------- E ARAYÜZÜ (E v12 gerçek saat) ----------------------------------------------------------------
K_HAZIR = 7.0                                     # E, ürünün ön kenarı E'ye girmeden (K 7,18) hazır: kapak 85°, köprü yukarıda (eski 11,10)
K_DUSTU = Z_DUS[1]                                # ürün kutu tabanına oturdu → E kapatmaya başlar (eski 13,60) · 11,10–13,60 arası E boşta (kutu_zaman_v12)
E_KAYMA = KC12.E_HAZIR_GERCEK - K_HAZIR           # E gerçek saati = K saati + kayma (hazır olana kadar)


def e_gercek(t):
    """K saati → E v12 GERÇEK saati: hazır olana kadar K + kayma · hazırdan ürün düşene kadar E boşta (bekler) · sonra kapatır"""
    if t < K_HAZIR:
        return t + E_KAYMA
    if t < K_DUSTU:
        return KC12.E_HAZIR_GERCEK
    return KC12.E_KAPAT_GERCEK + (t - K_DUSTU)


def e_time(t):
    """montajın KC fonksiyonlarına verdiği E saati (ESKİ saat birimi · kutu_cad_v12.eski)"""
    return KC12.eski(max(0.0, min(KC12.DONGU_GERCEK, e_gercek(t))))


def k_saati_e(T):
    """E gerçek saati → K saati (robot çatalı vb.)"""
    if T >= KC12.E_KAPAT_GERCEK:
        return K_DUSTU + (T - KC12.E_KAPAT_GERCEK)
    return T - E_KAYMA


E_BASLA_K = -E_KAYMA                              # E döngüsü (blank besleme) bu K anında başlar (ürün gelmeden önce · önceki periyodun sonunda)
E_BITIS_K = k_saati_e(KC12.DONGU_GERCEK)
CATAL_K = tuple(k_saati_e(v) for v in KC12.Z_CATAL_GERCEK)      # robot çatalı: gir · kaldır · çek başla · çek bitir (K saati)
DONGU_KE = E_BITIS_K - E_BASLA_K                  # K + E bir ürün (E kendi döngüsü + K'yi bekleme)
DONGU = float(math.ceil(max(Z_Z_DON[1] + 1.0, DONGU_KE + 0.5)))       # istasyon periyodu (montajın K döngüsü)


# ---------------------------------------------------------------- DENETİM (katalog sınırları) ----------------------------------------------------------------
def tampon_siniri(m):
    """SMC MY1B10 lastik tampon sınırı (katalog s. 8-11-19 log-log doğru: (0,05 kg; 1000 mm/s) → (5 kg; 110 mm/s)) · çarpma hızı mm/s"""
    return 1000.0 * (m / 0.05) ** (-0.479)


def zaman_denetimi():
    """modul() kurulmuş olmalı. Her eksen: süre, ortalama / tepe / çarpma hızı, katalog sınırı"""
    import numpy as np
    k = grup_kutleleri()
    out = dict(kutle=k, eksen=[])
    mZ, mX, mK = k["Z_hareketli"], k["X_hareketli"], k.get("KESICI", 0.0)

    def ekle_(ad, strok, T, sinir_v, not_, ok_):
        va = strok / T
        out["eksen"].append(dict(eksen=ad, strok=strok, sure=round(T, 2), v_ort=round(va, 1), v_tepe=round(1.5 * va, 1), v_carpma=round(1.4 * va, 1),
                                 sinir=sinir_v, not_=not_, ok=bool(ok_)))
    vz = 0.9 * tampon_siniri(mZ)
    ekle_("Z itici MY1B10G-350 (lastik tampon)", 350.0, T_Z, round(vz, 1), "çarpma ≤ 0,9 × tampon sınırı(%.2f kg) · ort. 100–500" % mZ,
          1.4 * 350.0 / T_Z <= vz and 100.0 <= 350.0 / T_Z <= 500.0)
    Ex = 0.5 * mX * (1.4 * 250.0 / T_X / 1000.0) ** 2
    ekle_("X itici MY1B10G-250 + 2 × RB0805", 250.0, T_X, 1000.0, "E = %.3f J ≤ 1,0 J (RB0805) · X kütlesi %.2f kg ≤ 5 kg (m1max) · ort. 100–1000" % (Ex, mX),
          Ex <= 1.0 and mX <= 5.0 and 100.0 <= 250.0 / T_X <= 1000.0)
    Tk, Tr = Z_KES[1] - Z_KES[0], Z_KES[3] - Z_KES[2]
    Ek = 0.5 * mK * (1.4 * 125.0 / Tr / 1000.0) ** 2
    ekle_("Kesici DGRF-C-63-125 dönüş", 125.0, Tr, None, "çarpma enerjisi %.3f J ≤ 1,3 J (Festo 562221) · kesici kütlesi %.2f kg" % (Ek, mK), Ek <= 1.3)
    ekle_("Kesici DGRF-C-63-125 iniş", 125.0, Tk, None, "bıçak strok sonunda (bant + 0,5) · 1870 N @ 6 bar", True)
    tt = np.arange(0.0, DONGU + 1e-9, 0.002)
    xs = np.array([state(float(t))["x"] for t in tt])
    vb = np.abs(np.diff(xs)) / 0.002
    bant_mask = np.array([(Z_GELIS[0] <= t <= Z_GELIS[1]) or (Z_TASI[0] <= t <= Z_TASI[1]) for t in tt[:-1]])
    vbm = float(vb[bant_mask].max())
    ekle_("Bant EC5000 49:1 (ürün)", 260.0, Z_GELIS[1] - Z_GELIS[0], 370.0, "tepe %.0f mm/s ≤ 370" % vbm, vbm <= 370.0)
    out["dongu"] = DONGU; out["dongu_KE"] = round(DONGU_KE, 2); out["E_basla_K"] = round(E_BASLA_K, 2); out["E_bitis_K"] = round(E_BITIS_K, 2)
    out["catal_K"] = [round(c, 2) for c in CATAL_K]
    out["ok"] = all(e["ok"] for e in out["eksen"]) and DONGU_KE <= DONGU
    return out
