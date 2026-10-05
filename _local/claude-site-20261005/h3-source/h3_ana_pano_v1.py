# -*- coding: utf-8 -*-
"""HAT v3.6 · ANA PANO (BEYİN) v1 — KENDİ BAŞINA ÜRÜN (1 Eki 2026 · Claude · YEREL)
Kemal: "ana pano / beyin QR'da olmasın, yağ tenekesinin üstünde olsun, kendi başına bir ürün olsun".
YER: fırın üstü kabinde tenekenin üstünde yer yok (ağız adaptörü 1821, F_UST tavanı 1840,5) → ÜST DEPO F (U_F) içinde, TENEKENİN HEMEN ÜSTÜ:
  U_F taban sacı üstü 1863,5 · U_F tavanı altı 2178,5 · pizza kutu yığını x ≤ 3324 + raf kirişi 3299–3329 (DOKUNULMAZ) · U_F tavan kirişi x 3485–3515 (y ≥ 2168,5) →
  pano x 3518–3978 (kirişin sağında, sağ yan sac 3983,5) · üst 2176 (tavana 2,5) · z −290…−88 (yağ tenekesi z −413,5…−178,5 · x 3746–3981 ile üst üste;
  kapak U_F ön kapağının 147 mm gerisinde: U_F sağ düşer kapağı açılınca önden servis).
ÜRÜN (bağımsız · kendi gövdesi / kapağı / ayağı): AISI 304 1,5 kaynaklı kutu 460 × 309,5 × 230 (v3.6b arka −320) · ön çerçeve (açıklık 420 × 238) + EPDM conta + 2 mm kapak (sağdan menteşeli,
  çeyrek tur kilit) · 4 burç + 2 mm galvaniz montaj plakası · 2 × TS35 ray · 2 × 304 taban rayı 30 × 3 (U_F taban sacına 4 × M6) · SOL YAN: 6 × Harting istasyon soketi
  (Han 10B) + 3 rakor (bina beslemesi M32 · modem Cat6A M20 · yedek M20 kör tapa).
İÇERİK = h3_elk_qr_v1 (v3.5) QR ana panosunun AYNI cihazları (üretici STEP'i olanlar katalog_step_v1 ile) + v3.6 ekleri:
  RAY A (y 2109): Acti9 iSW 4P 40 A (A9S65440) · iID 4P 40 A 30 mA (A9R21440) · 7 × iC60N 1P+N C16 (6 istasyon + PANO_24V; A9F79616 STEP yok → ZARF)
  RAY B (y 1950): NDR-120-24 · DC-UPS 24 V 5 A + 1,3 Ah VRLA akü modülü (v3.6 YENİ: QR'deki APC BX500CI QR kilit kartında KALIR) · RevPi Connect 4 (PR100378) +
                  RevPi DIO (v3.6 YENİ · ZARF, Connect gövdesiyle aynı profil) · FL SWITCH 1008N (1085256) · 16 × PT 2,5 + 4 × PT 2,5-PE + 2 uç tutucu
  KANAL: sol dikey 25 × 40 (soket arkası → cihazlar) + orta yatay 30 × 40 (iki ray arası) PVC, kapaklı.
ÖLÇÜ HESABI (pano_olcu_hesabi()): yükseklik sürücüsü FL SWITCH 1008N 147,55 (ray altı 75,85) + Acti9 95,4 + orta kanal 30 → iç 306,5'te 18,5 üst pay ·
  genişlik sürücüsü RAY A 70,8 + 71,7 + 7 × 36 + 2 = 396,5 + sol kanal 25 + soket arkası 25,5 → iç 457 (3 mm pay) · derinlik: en derin cihaz NDR 119,25 (ray önünden)
  + plaka 8 + kapak payı 62 → 200 · ISI: ~35 W · etkin yüzey (taban hariç) 0,50 m² · k 5,5 W/m²K (paslanmaz sac, IEC 60890 yaklaşık) → ΔT ≈ 12,7 K
  (U_F iç ortamı 35 °C → pano içi ≈ 48 °C < RevPi Connect 4 üst sınırı 55 °C [föy teyit] · AÇIK: U_F ortam sıcaklığı ölçülmedi, fırın üstü).
SÖZLEŞME (h3_elektrik_v1 / h3_ust_depo_v2 gibi): kur() · PARCALAR [ad, wp, mal, birim, grup, kaynak, bom] (DÜNYA) · dunya(p) · BIRIMLER · BIRIM_MODUL · MALZEME ·
  KAPAK_EKSEN · PANO_KUTU · GIRIS_RAKORLARI · HARTING_SOKETLERI (elektrik ajanı kabloları bunlara bağlar) · sozlesme() → scratchpad ana_pano_sozlesme.json.
v3.7 (1 Eki 2026 · Claude · YEREL) — ZARF CİHAZLAR → ÜRETİCİ STEP'İ (arastirma/katalog/step · katalog_step_v1 önbelleği h3/_katalog_cache):
  iC60N 1P+N C16 A9F79616 · iDPN N 1P+N C16 A9N21557 / C6 A9N21555 (se.com) · RevPi DIO PR100197 (kod düzeltmesi: PR100253 yok · revolutionpi.com) ·
  Phoenix PT 2,5 3209510 · PT 2,5-PE 3209536 (3209523 = PT 2,5 BU, düzeltildi) · uç tutucu E/UK 1201442 (phoenixcontact.com) — yön + ray oluğu bu dosyada
  KATALOG_V37 (ışın sondası: oluk tabanı / ortası) · STEP'İ ALINAMAYANLAR (ZARF, föy ölçüsü): Phoenix QUINT4-CAP/24DC/5/4KJ 2320539 (captcha) · HARTING Han 10B
  09 30 010 0305 (myHARTING girişi) · RevPi AIO (zip'te ayrı model, alınmadı → DIO gövde STEP'i, ön klemens farkı).
  UPS: VRLA akü (CSB: şarj üst sınırı 40 °C, her +10 °C ömür yarı) KALDIRILDI → QUINT4-CAP/24DC/5/4KJ süperkapasitörlü DC-UPS (4 kJ · 5 A · 25 W'ta ≈ 3 dk ·
  −25…+60 °C) — kesintide RevPi'ye düzgün kapanma süresi verir (uzun kesinti köprüsü DEĞİL). ⚠ föy üst / alt 50 mm boşluk ister; panoda alt 18 / üst 11 (kanal) → derating notu.
  SICAKLIK: RevPi AIO (100250 · 2 × Pt100) + Pt100 prob (pano içi) · U_F fanları 4 × 4414 FL STEGO KTS 011 ile (h3_ust_depo_v2) · kablo fan_24V_M20 rakorundan."""
import io, json, math, os, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, kanal, rakor

V = cq.Vector
# ================================================================ SÖZLEŞME SABİTLERİ (dünya · mm) ================================================================
T = 1.5                                                     # 304 sac
PANO_KUTU = (3518.0, 3978.0, 1866.5, 2176.0, -320.0, -87.0)  # (x0, x1, y0, y1, z0, z1) gövde + kapak (kapak ön yüzü −87 · kilit topuzu −80'e kadar)
GOVDE = dict(x=(3518.0, 3978.0), y=(1866.5, 2176.0), z=(-320.0, -90.0))   # v3.6b: arka −290 → −320 (arka yüz A + F soketlerinin iç modülleri plakanın arkasına sığsın)          # gövde (ön çerçeve z −91,5…−90)
ACIKLIK = dict(x=(3538.0, 3958.0), y=(1912.0, 2150.0))                          # ön çerçeve açıklığı 420 × 238
KAPAK = dict(x=(3521.0, 3968.0), y=(1899.0, 2165.0), z=(-89.0, -87.0))         # kapak 2 mm · alt kenar 1899 > U_F alt kayıt 1893,5 · üst 2165 < U_F üst kayıt 2168,5 (açılırken)
CONTA = dict(x=(3530.0, 3966.0), y=(1904.0, 2158.0), z=(-90.0, -89.0), gen=8.0)
MENTESE_X, MENTESE_Z, MENTESE_R = 3973.0, -86.0, 4.0        # menteşe ekseni (y boyunca) · kapak 90° açılır (sağa-öne)
MENTESE_Y = ((1920.0, 1960.0), (2105.0, 2145.0))
KILIT = dict(x=3551.0, y=2030.0, r=11.0)                    # çeyrek tur kilit (DIN 3 mm çift dil) · topuz önde, dil sol çerçeve bandının arkasına
AYAK = dict(x=((3523.0, 3553.0), (3943.0, 3973.0)), y=(1863.5, 1866.5), z=(-345.0, -95.0))   # 304 lama 30 × 3 · arkadan 25 taşar (2 × M6 / ray)
PLAKA = dict(x=(3524.0, 3975.0), y=(1872.0, 2170.0), z=(-282.5, -280.5))       # galvaniz 2 mm · 4 burç (arka iç yüz −288,5 → −282,5)
RAY_ON = PLAKA["z"][1] + 7.5                                 # −273 TS35 × 7,5 önü (cihaz oluk tabanı)
RAY_A_Y, RAY_B_Y = 2109.0, 1950.0
RAY_X = (3575.0, 3975.0)
KANAL_SOL = dict(x=(3548.0, 3573.0), y=(1872.0, 2170.0), z=(PLAKA["z"][1], PLAKA["z"][1] + 40.0))
KANAL_ORTA = dict(x=(3573.0, 3975.0), y=(2026.0, 2056.0), z=(PLAKA["z"][1], PLAKA["z"][1] + 40.0))
X_CIHAZ = 3577.0                                             # iki rayın ilk cihazının sol kenarı (sol kanal + 4)
# Harting Han 10B bulkhead (VARSAYIM ölçü · föyden teyit): flanş 83 (y) × 57 (z) × 3 · gövde 66 × 43 × 25 dışarı · iç modül 56 × 36 × 27 içeri · sac kesiği 66 × 43
HAN = dict(fl=(93.0, 43.4, 3.0), gv=(66.0, 35.0, 25.9), ic=(56.0, 30.0, 27.0), kes=(60.0, 35.0))   # v3.7: HARTING Han B 10 bulkhead 09 30 010 0305 distribütör ölçüsü 93 × 43,4 × 28,9 · kesik 60 × 35 · 4 × Ø4,5 / 83 × 32 (föy teyit · STEP girişli)
X_SOL = GOVDE["x"][0]                                        # sol yan sac DIŞ yüzü 3518
HARTING_SOKETLERI = [                                         # (istasyon, x soket ağzı, y, z, yön) · fiş −x yönünden takılır (fiş + kablo payı x 3335–3490: 155 mm)
    ("TOPPING", X_SOL - HAN["fl"][2] - HAN["gv"][2], 2122.0, -240.0, "-x"),
    ("DOLAP",   X_SOL - HAN["fl"][2] - HAN["gv"][2], 2122.0, -140.0, "-x"),
    ("K",       X_SOL - HAN["fl"][2] - HAN["gv"][2], 2021.0, -240.0, "-x"),
    ("E",       X_SOL - HAN["fl"][2] - HAN["gv"][2], 2021.0, -140.0, "-x"),
    ("ROBOT",   X_SOL - HAN["fl"][2] - HAN["gv"][2], 1920.0, -240.0, "-x"),
    ("QR",      X_SOL - HAN["fl"][2] - HAN["gv"][2], 1920.0, -140.0, "-x"),
    # v3.6b (Kemal: A + F için de soket) · ARKA YÜZ (dış yüz z −320 · yön −z): orta satır y 2021 (sol yandaki K / E satırı) · pano ortası x 3748'e simetrik ±80 ·
    #   fiş + kablo arkaya (z −348 → −430; U_F arka sacı −828,5, üst hat kanalı z −826…−766 · U_F tavan kirişi x 3485–3515 bu x'lerde değil) · iç modül plakanın arkasında (z −318,5…−293 < plaka −282,5)
    ("A",       3668.0, 2021.0, -320.0 - HAN["fl"][2] - HAN["gv"][2], "-z"),
    ("F",       3828.0, 2021.0, -320.0 - HAN["fl"][2] - HAN["gv"][2], "-z")]
GIRIS_RAKORLARI = [                                           # (ad, x dış yüz, y, z, yön, rakor diş çapı M) · Lapp SKINTOP ST-M · iki soket sütunu arasındaki şerit (z −211,5…−168,5)
    ("bina_besleme_5G6_M32", X_SOL, 1925.0, -190.0, "-x", 32.0),
    ("modem_Cat6A_M20", X_SOL, 2021.0, -190.0, "-x", 20.0),
    ("fan_24V_M20", X_SOL, 2117.0, -190.0, "-x", 20.0)]             # v3.7: yedek → U_F fanları (4 × 4414 FL) + STEGO KTS 011 termostat kablosu
_RAKOR_R = {32.0: (9.95, 16.0), 20.0: (4.35, 10.0)}           # (kablo r, dişli boyun r) · 5G6 Ø17,5–22,2 · Cat6A Ø8,7
KAPAK_EKSEN = {"KAPAK_ANA_PANO": ((MENTESE_X, KAPAK["y"][0], MENTESE_Z), (0.0, 1.0, 0.0), 90.0)}   # + açı: sol kenar öne (+z) · 95°'de U_F sağ yan sacı + bas-aç (denetim) → 90° durdurucu

PARCALAR = []
BIRIM = "ELK_ANA_PANO_UF"
BIRIMLER = [(BIRIM, "ANA PANO (BEYİN) · KENDİ BAŞINA ÜRÜN · U_F içinde yağ tenekesinin üstünde (x 3518–3978 · y 1866,5–2176 · z −320…−87): 304 kutu 460 × 309,5 × 230 + "
                    "kapak + taban rayları · iSW 4P 40 A · iID 4P 40 A 30 mA · 7 × iC60N 1P+N · NDR-120-24 · DC-UPS 24 V + akü · RevPi Connect 4 + DIO · FL SWITCH 1008N · "
                    "klemens · kanallar · sol yanda 6 + arkada 2 (A · F) Harting istasyon soketi + 3 rakor")]
BIRIM_MODUL = {BIRIM: "D"}
MALZEME = {"pano": dict(renk=(0.86, 0.87, 0.88, 1.0), met=0.3, ruf=0.5), "din": dict(renk=(0.75, 0.77, 0.79, 1.0), met=0.9, ruf=0.3),
           "cihaz": dict(renk=(0.93, 0.93, 0.92, 1.0), met=0.0, ruf=0.6), "cihaz_koyu": dict(renk=(0.20, 0.21, 0.23, 1.0), met=0.1, ruf=0.5),
           "kanal": dict(renk=(0.62, 0.64, 0.66, 1.0), met=0.0, ruf=0.7), "rakor": dict(renk=(0.14, 0.14, 0.15, 1.0), met=0.0, ruf=0.5),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "conta": dict(renk=(0.12, 0.12, 0.12, 1.0), met=0.0, ruf=0.8), "harting": dict(renk=(0.55, 0.57, 0.60, 1.0), met=0.6, ruf=0.4)}


def ekle(ad, sh, mal, bom=None, grup="SABIT", kaynak="h3_ana_pano_v1"):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    sh = sh.val() if isinstance(sh, cq.Workplane) else sh
    PARCALAR.append(dict(ad=ad, wp=cq.Workplane(obj=sh), mal=mal, birim=BIRIM, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


# ================================================================ ÖLÇÜ + ISI HESABI ================================================================
ISI_W = [("NDR-120-24 kaybı (~25 W çıkış, η ≈ 0,86)", 4.0), ("RevPi Connect 4 (föy maks 20 W · tipik)", 6.0), ("RevPi DIO (föy 1,5 W)", 1.5), ("RevPi AIO", 1.0),
         ("FL SWITCH 1008N", 2.2), ("QUINT4-CAP bekleme", 1.0), ("8 × MCB + iID + iSW (kısmi yük, I² ölçekli)", 2.5), ("klemens + iç kablo + Harting", 1.8)]   # v3.7 ≈ 20 W · en kötü 35 W ayrıca (isi_dengesi)
ISI_EN_KOTU_W = 35.0
# ---- v3.7 · katalog_step_v1 tablosuna eklenen cihazlar (yön + ray oluğu STEP koordinatında · step_prob2 ışın sondası, firin_ust_v37) ----
KATALOG_V37 = {
    "A9F79616": dict(dosya="a9f79616.stp", uretici="Schneider Electric", ad="Acti9 iC60N MCB 1P+N C16 6 kA",
                     kaynak="https://www.se.com/sg/en/product/A9F79616/ (CAD: MCADFD0001001_3D-simplified.stp, giriş yok)",
                     eksen=("-x", "+y", "-z"), ray_on=-65.94, ray_h=43.0, olcum="oluk y 25,1–60,9 = 35,8 · oluk tabanı z −65,94 · arka z −71,44 (5,5)"),
    "A9N21557": dict(dosya="a9n21557.stp", uretici="Schneider Electric", ad="Acti9 iDPN N 1P+N C16 (18 mm)",
                     kaynak="https://www.se.com/pt/pt/product/A9N21557/ (CAD: MCADFD0001740_3D-simplified.stp, AP203, giriş yok)",
                     eksen=("-x", "+y", "-z"), ray_on=-63.31, ray_h=40.6, olcum="oluk tabanı z −63,31 (arka −68,81) · üst kenar y 58,1 · alt kilit dili pahlı 21,5–24,1 → orta 58,1 − 17,5"),
    "A9N21555": dict(dosya="a9n21555.stp", uretici="Schneider Electric", ad="Acti9 iDPN N 1P+N C6 (18 mm) — C16 ile aynı model",
                     kaynak="https://www.se.com/fr/fr/product/A9N21555/ (C16 ile aynı CAD dosyası)",
                     eksen=("-x", "+y", "-z"), ray_on=-63.31, ray_h=40.6, olcum="A9N21557 ile aynı"),
    "PR100197": dict(dosya="pr100197.stp", uretici="KUNBUS (Revolution Pi)", ad="RevPi DIO 14 DI / 14 DO (evrensel DI/DO/DIO/MIO gövdesi)",
                     kaynak="https://revolutionpi.com/fileadmin/user_upload/RevPi-IOs_Step.zip (giriş yok)",
                     eksen=("+x", "+z", "-y"), ray_on=5.5, ray_h=0.0, sade="kabuk",
                     olcum="STEP y derinlik: arka y 0, oluk tabanı y 5,5 (z −17,5…+17,5) · ön gövde y 110 · ön klemens fişleri y 129,9"),
    "3209510": dict(dosya="3209510.stp", uretici="Phoenix Contact", ad="PT 2,5 geçişli klemens (push-in)",
                    kaynak="https://www.phoenixcontact.com/ (3209510 · downloads 8087463, giriş yok)",
                    eksen=("-x", "+y", "-z"), ray_on=6.0, ray_h=24.3, olcum="oluk tabanı z 6,0 (föy: NS 35/7,5 üstünde 36,8 = 35,25 − 6 + 7,5 ✓) · oluk y 7,0–41,5"),
    "3209536": dict(dosya="3209536.stp", uretici="Phoenix Contact", ad="PT 2,5-PE toprak klemensi",
                    kaynak="https://www.phoenixcontact.com/ (3209536 · downloads 8311165, giriş yok)",
                    eksen=("-x", "+y", "-z"), ray_on=6.0, ray_h=24.3, olcum="PT 2,5 ile aynı gövde ölçüsü (5,15 × 48,6 × 35,25)"),
    "1201442": dict(dosya="1201442.stp", uretici="Phoenix Contact", ad="Uç tutucu E/UK",
                    kaynak="https://www.phoenixcontact.com/ (1201442 · downloads 11657518, giriş yok)",
                    eksen=("-x", "+y", "-z"), ray_on=6.6, ray_h=25.0, olcum="oluk tabanı z 6,6 (y 18–42) · vida bölgesi y 13–17"),
}


def katalog_v37():
    import katalog_step_v1 as KS
    for k, v in KATALOG_V37.items():
        KS.KATALOG.setdefault(k, v)
    return KS


def pano_olcu_hesabi(KS=None):
    """yerleşimden gereken iç ölçüler + ısı (dönüş: sözlük · kur() denetler)"""
    KS = katalog_v37()
    sw, nd, isw, iid, rp = (KS.bilgi(k) for k in ("1085256", "NDR-120-24", "A9S65440", "A9R21440", "PR100378"))
    ray_b_alt = max(sw["ray"]["alt"], nd["ray"]["alt"], rp["ray"]["alt"], 65.0)          # 65: QUINT4-CAP zarfı (130 / 2)
    ray_b_ust = max(sw["ray"]["ust"], nd["ray"]["ust"], rp["ray"]["ust"], 65.0)
    ray_a_alt = max(isw["ray"]["alt"], iid["ray"]["alt"], 45.0); ray_a_ust = max(isw["ray"]["ust"], iid["ray"]["ust"], 45.0)
    iy0, iy1 = GOVDE["y"][0] + T, GOVDE["y"][1] - T
    alt_pay = RAY_B_Y - ray_b_alt - iy0; ust_pay = iy1 - (RAY_A_Y + ray_a_ust)
    kanal_b = KANAL_ORTA["y"][0] - (RAY_B_Y + ray_b_ust); kanal_a = (RAY_A_Y - ray_a_alt) - KANAL_ORTA["y"][1]
    gen_a = isw["olcu"][0] + 1.0 + iid["olcu"][0] + 1.0 + 7 * 36.0
    ix1 = GOVDE["x"][1] - T
    sag_pay_a = ix1 - (X_CIHAZ + gen_a)
    on_max = max(nd["ray"]["on"], sw["ray"]["on"], rp["ray"]["on"], isw["ray"]["on"], KS.bilgi("PR100197")["ray"]["on"], 125.0)   # v3.7: DIO fişleri 124,4 · QUINT4-CAP 125
    kapak_pay = (GOVDE["z"][1] - T) - (RAY_ON + on_max)
    x0, x1, y0, y1, z0, z1 = GOVDE["x"] + GOVDE["y"] + GOVDE["z"]
    W, H, D = (x1 - x0) / 1000.0, (y1 - y0) / 1000.0, (z1 - z0) / 1000.0
    A = W * D + 2 * W * H + 2 * H * D                                                  # taban hariç (U_F tabanında 3 mm)
    P = sum(w for _a, w in ISI_W); k = 5.5
    return dict(alt_pay=alt_pay, ust_pay=ust_pay, kanal_b=kanal_b, kanal_a=kanal_a, gen_a=gen_a, sag_pay_a=sag_pay_a, on_max=on_max, kapak_pay=kapak_pay,
                A=A, P=P, k=k, dT=P / (k * A), W=W, H=H, D=D)


# ================================================================ KUR ================================================================
def kur():
    KS = katalog_v37()
    PARCALAR[:] = []
    x0, x1 = GOVDE["x"]; y0, y1 = GOVDE["y"]; z0, z1 = GOVDE["z"]
    # ---------------- 1 · GÖVDE (5 yüz + ön çerçeve, kaynaklı) · sol yanda soket / rakor kesikleri ----------------
    g = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + T, x1 - T, y0 + T, y1 - T, z0 + T, z1 + 1.0))
    g = g.fuse(kut(x0, x1, y0, y1, z1 - T, z1).cut(kut(ACIKLIK["x"][0], ACIKLIK["x"][1], ACIKLIK["y"][0], ACIKLIK["y"][1], z1 - T - 1.0, z1 + 1.0)))
    kw, kh = HAN["kes"]
    for ist, xs, ys, zs, yon in HARTING_SOKETLERI:
        if yon == "-x": g = g.cut(kut(x0 - 1.0, x0 + T + 1.0, ys - kw / 2.0, ys + kw / 2.0, zs - kh / 2.0, zs + kh / 2.0))
        else: g = g.cut(kut(xs - kh / 2.0, xs + kh / 2.0, ys - kw / 2.0, ys + kw / 2.0, z0 - 1.0, z0 + T + 1.0))
    rk = []
    for ad, xr, yr, zr, yon, m in GIRIS_RAKORLARI:
        r_k, r_d = _RAKOR_R[m]
        s, d_ = rakor((xr, yr, zr), "x", r_k + 0.05, T, yon="-", disli=r_d)
        g = g.cut(d_); rk.append((ad, s, m))
    ekle("ana_pano_govde", g.clean(), "pano",
         bom=("ANA PANO kutusu AISI 304 1,5 ÖZEL İMALAT · 460 × 309,5 × 230 · ön çerçeve açıklığı 420 × 238 · IP65 (EPDM conta)", 1,
              "lazer + abkant + TIG kaynak · sol yanda 6 × Han 10B kesiği 66 × 43 + M32 + 2 × M20 rakor deliği · arka yüzde 2 × Han 10B (A · F)",
              "v3.6 · KENDİ BAŞINA ÜRÜN (QR'den çıktı) · U_F içinde yağ tenekesinin üstü · ölçü hesabı: pano_olcu_hesabi() (iç 457 × 306,5 × 227)"))
    # taban rayları (ayak) + kapak + conta + menteşe + kilit
    for i, (a, b) in enumerate(AYAK["x"]):
        ekle("ana_pano_taban_rayi_%d" % i, kut(a, b, AYAK["y"][0], AYAK["y"][1], AYAK["z"][0], AYAK["z"][1]), "paslanmaz",
             bom=("Pano taban rayı (ayak) 304 lama 30 × 3 × 220 · gövdeye kaynaklı · arkada 25 taşar", 2, "U_F taban sacına 2 × M6 perçin somun / ray", "v3.6 · pano U_F tabanına 3 mm hava aralığıyla oturur") if i == 0 else None)
    kp = kut(KAPAK["x"][0], KAPAK["x"][1], KAPAK["y"][0], KAPAK["y"][1], KAPAK["z"][0], KAPAK["z"][1]).cut(sil((KILIT["x"], KILIT["y"], -95.0), (KILIT["x"], KILIT["y"], -80.0), KILIT["r"] + 0.5))
    ekle("ana_pano_kapagi", kp, "pano", grup="KAPAK_ANA_PANO",
         bom=("Pano kapağı 304 1,5 + 4 kenar 2 · 447 × 266 · iç yüzde EPDM conta yuvası", 1, "lazer + abkant", "sağdan menteşeli, 90° durdurucu (U_F sağ kapağı açıkken; 95°'de U_F sağ yan sacına değer) · çeyrek tur kilit"))
    c = kut(CONTA["x"][0], CONTA["x"][1], CONTA["y"][0], CONTA["y"][1], CONTA["z"][0], CONTA["z"][1])
    c = c.cut(kut(CONTA["x"][0] + CONTA["gen"], CONTA["x"][1] - CONTA["gen"], CONTA["y"][0] + CONTA["gen"], CONTA["y"][1] - CONTA["gen"], CONTA["z"][0] - 1.0, CONTA["z"][1] + 1.0))
    ekle("ana_pano_kapak_contasi", c, "conta", grup="KAPAK_ANA_PANO", bom=("Kapak contası EPDM köpük 8 × 1 (sıkışmış) · yapışkanlı", 1, "", "IP65"))
    for i, (ya, yb) in enumerate(MENTESE_Y):
        m = sil((MENTESE_X, ya, MENTESE_Z), (MENTESE_X, yb, MENTESE_Z), MENTESE_R)                          # pim gövdesi (sabit yarı)
        m = m.fuse(kut(MENTESE_X - 1.0, MENTESE_X + 4.0, ya, yb, z1 - 0.0, z1 + 0.5).cut(sil((MENTESE_X, ya - 1.0, MENTESE_Z), (MENTESE_X, yb + 1.0, MENTESE_Z), MENTESE_R - 0.01)))   # gövde yaprağı
        ekle("ana_pano_mentesesi_%d" % i, m.clean(), "paslanmaz",
             bom=("Pano menteşesi 304 (kaynaklı gövde yaprağı + perçinli kapak yaprağı · Ø8 pim)", 2, "katalog (paslanmaz kapı menteşesi 40 mm)", "VARSAYIM ölçü") if i == 0 else None)
        ekle("ana_pano_mentesesi_%d_kapak_yapragi" % i, kut(3958.0, MENTESE_X - MENTESE_R - 0.2, ya, yb, KAPAK["z"][1], KAPAK["z"][1] + 1.5), "paslanmaz", grup="KAPAK_ANA_PANO")   # kapakla döner
    kl = sil((KILIT["x"], KILIT["y"], -93.0), (KILIT["x"], KILIT["y"], -80.0), KILIT["r"])
    kl = kl.fuse(kut(KILIT["x"] - 26.0, KILIT["x"] + 6.0, KILIT["y"] - 6.0, KILIT["y"] + 6.0, -95.0, -93.0))     # dil: sol çerçeve bandının arkasına (z −91,5'in gerisinde)
    ekle("ana_pano_ceyrek_tur_kilit", kl.clean(), "cihaz_koyu", grup="KAPAK_ANA_PANO",
         bom=("Çeyrek tur kilit DIN 3 mm çift dil (ör. EMKA 1000 serisi) · Ø22 · IP65", 1, "katalog", "VARSAYIM ölçü · kapakta, dil çerçeve arkasına"))
    # ---------------- 2 · İÇ: burçlar + montaj plakası + raylar + kanallar ----------------
    for i, (bx, by) in enumerate(((3535.0, 1882.0), (3965.0, 1882.0), (3535.0, 2160.0), (3965.0, 2160.0))):
        ekle("ana_pano_plaka_burcu_%d" % i, sil((bx, by, z0 + T), (bx, by, PLAKA["z"][0]), 5.0), "celik",
             bom=("Plaka burcu M6 × 6 (arka saca kaynaklı saplama + mesafe burcu)", 4, "", "") if i == 0 else None)
    ekle("ana_pano_montaj_plakasi", kut(*(PLAKA["x"] + PLAKA["y"] + PLAKA["z"])), "din", bom=("Montaj plakası galvaniz 2 mm · 451 × 298", 1, "", ""))
    for nm, yc in (("A", RAY_A_Y), ("B", RAY_B_Y)):
        ekle("ana_pano_din_rayi_%s" % nm, kut(RAY_X[0], RAY_X[1], yc - 17.5, yc + 17.5, PLAKA["z"][1], RAY_ON), "din",
             bom=("DIN rayı TS35 × 7,5 · L 400", 2, "", "") if nm == "A" else None)
    gk, kk = kanal("y", KANAL_SOL["y"][0], KANAL_SOL["y"][1], KANAL_SOL["x"][0], KANAL_SOL["x"][1], KANAL_SOL["z"][0], KANAL_SOL["z"][1], acik="+")
    ekle("ana_pano_kanal_sol", gk, "kanal", bom=("Pano kablo kanalı PVC delikli + kapak (sol dikey 25 × 40 · orta yatay 30 × 40)", 2, "", "soket arkası → cihazlar"))
    ekle("ana_pano_kanal_sol_kapak", kk, "kanal")
    gk, kk = kanal("x", KANAL_ORTA["x"][0], KANAL_ORTA["x"][1], KANAL_ORTA["y"][0], KANAL_ORTA["y"][1], KANAL_ORTA["z"][0], KANAL_ORTA["z"][1], acik="+")
    ekle("ana_pano_kanal_orta", gk, "kanal"); ekle("ana_pano_kanal_orta_kapak", kk, "kanal")

    # ---------------- 3 · CİHAZLAR (önü +z, kapağa bakar) ----------------
    def din_step(ad, kod, xa, yc, mal="cihaz", bom=None):
        ekle(ad, KS.cihaz_step(kod, xa, yc, PLAKA["z"][1], yon=+1), mal, bom=bom)
        return xa + KS.olcu(kod)[0]

    def din_zarf(ad, xa, w, alt, ust, on, yc, mal="cihaz", bom=None):
        ekle(ad, kut(xa, xa + w, yc - alt, yc + ust, RAY_ON, RAY_ON + on), mal, bom=bom)
        return xa + w
    # ray A: iSW · iID · 7 × iC60N
    xs = din_step("ana_pano_ana_salter_iSW_4P_40A", "A9S65440", X_CIHAZ, RAY_A_Y,
                  bom=("Ana şalter Schneider Acti9 iSW 4P 40 A (A9S65440)", 1, KS.bom_kaynak("A9S65440"), "bina beslemesi 400 V 3F (5G6, M32 rakordan)"))
    xs = din_step("ana_pano_kacak_akim_iID_4P_40A_30mA", "A9R21440", xs + 1.0, RAY_A_Y,
                  bom=("Kaçak akım Schneider Acti9 iID 4P 40 A 30 mA tip A (A9R21440)", 1, KS.bom_kaynak("A9R21440"), ""))
    SG = [("TOPPING", "C16"), ("DOLAP", "C16"), ("K", "C16"), ("E", "C16"), ("ROBOT", "C16"), ("QR", "C16")]
    xg = xs + 1.0
    for i, (s, cc) in enumerate(SG):
        din_step("ana_pano_sigorta_iC60N_1PN_%s_%s" % (cc, s), "A9F79616", xg + 0.3, RAY_A_Y,
                 bom=("Sigorta Schneider Acti9 iC60N 1P+N C16 (A9F79616)", len(SG), KS.bom_kaynak("A9F79616"), "6 istasyon (Harting soketi başına 1) · fazlara dengeli") if i == 0 else None)
        xg += 36.0                                                                              # 4 × 9 mm modül adımı (gövde 35,4)
    # v3.6b · RAY A'da 9 × 36 SIĞMAZ (7 × 36 ile sağ pay 3 mm; 9 × 36 → 69 mm taşar): A + PANO_24V tek modüllü 1P+N (18 mm) → 6 × 36 + 2 × 18 = 7 × 36 (aynı yer) ·
    #   F'ye SİGORTA YOK: fırın gücü kendi devresinden (bina 5G6 · CEE 32 A · f_ust_rakor_cee_firin), F soketi yalnız sinyal + Ethernet (DIO + switch)
    SG2 = [("A", "C16"), ("PANO_24V", "C6")]
    for i, (s, cc) in enumerate(SG2):
        din_step("ana_pano_sigorta_iDPN_N_1PN_%s_%s" % (cc, s), "A9N21557" if cc == "C16" else "A9N21555", xg + 0.25, RAY_A_Y,
                 bom=("Sigorta Schneider Acti9 iDPN N 1P+N tek modül 18 mm (C16 A9N21557 · C6 A9N21555)", len(SG2), KS.bom_kaynak("A9N21557"),
                      "v3.6b · A (açıcı) soketi C16 + PANO_24V (NDR-120 + QUINT4-CAP) C6 · F'ye sigorta yok: fırın kendi CEE 32 A devresinde") if i == 0 else None)
        xg += 18.0
    assert xg <= x1 - T - 2.0, xg
    # ray B: NDR-120 · DC-UPS · RevPi Connect 4 + DIO · switch · klemens · akü modülü
    xb = din_step("ana_pano_guc_24V_NDR-120-24", "NDR-120-24", X_CIHAZ, RAY_B_Y,
                  bom=("Mean Well NDR-120-24", 1, KS.bom_kaynak("NDR-120-24"), "24 V: DC-UPS girişi → ana bilgisayar + DIO + switch + modem"))
    xb = din_zarf("ana_pano_dc_ups_QUINT4-CAP_24DC_5_4KJ", xb + 6.0, 94.0, 65.0, 65.0, 125.0, RAY_B_Y, "cihaz",
                  bom=("Süperkapasitörlü DC-UPS Phoenix Contact QUINT4-CAP/24DC/5/4KJ (2320539) · 4 kJ · 5 A", 1,
                       "ZARF 94 × 130 × 125 (föy · STEP captcha arkasında, indirilmedi) · −25…+60 °C, 40 °C üstü %1/K derating",
                       "v3.7 · VRLA akü yerine (CSB şarj üst sınırı 40 °C) · 25 W'ta ≈ 3 dk köprü → RevPi düzgün kapanır · föy üst / alt 50 mm boşluk ister (panoda 18 / 11 → derating)"))
    xb = din_step("ana_pano_hmi_ana_bilgisayar_RevPi_Connect_4", "PR100378", xb + 6.0, RAY_B_Y, "cihaz_koyu",
                  bom=("ANA BİLGİSAYAR Kunbus Revolution Pi Connect 4 PR100378 (4 GB · 32 GB eMMC · WLAN'sız · ekransız · DIN · 24 V · 2 × Ethernet)", 1, KS.bom_kaynak("PR100378"),
                       "sipariş sırası + istasyon koordinasyonu + web paneli (iPad / telefon) · PLC'lerle Ethernet"))
    rpb = KS.bilgi("PR100378")["ray"]
    xb = din_step("ana_pano_revpi_DIO_PR100197", "PR100197", xb, RAY_B_Y, "cihaz_koyu",
                  bom=("Kunbus RevPi DIO (PR100197 · 14 DI + 14 DO · PiBridge ile Connect'in sağına)", 1, KS.bom_kaynak("PR100197"),
                       "v3.6 · acil stop / kapı / ışık perdesi durumu, ikaz lambası, kontaktör sürme · v3.7: STEP (eski kod PR100253 yanlıştı)"))
    xb = din_step("ana_pano_revpi_AIO_100250", "PR100197", xb, RAY_B_Y, "cihaz_koyu",
                  bom=("Kunbus RevPi AIO (100250 · 2 × Pt100/Pt1000 + 4 AI + 2 AO · PiBridge ile DIO'nun sağına)", 1,
                       "gövde = RevPi IO evrensel STEP'i (PR100197 dosyası; AIO ön klemens dizilimi farklı) · 22,5 × 96 × 110,5 föy",
                       "v3.7 · pano içi Pt100 sıcaklık ölçümü → web paneli / alarm (≥ 50 °C)"))
    xb = din_step("ana_pano_ag_anahtari_FL_SWITCH_1008N", "1085256", xb + 6.0, RAY_B_Y, "cihaz_koyu",
                  bom=("Endüstriyel switch Phoenix Contact FL SWITCH 1008N (1085256 · 8 × RJ45)", 1, KS.bom_kaynak("1085256"), "ana bilgisayar · 4 istasyon PLC · robot · QR kartı · modem"))
    xk = xb + 6.0
    xk = din_step("ana_pano_klemens_uc_tutucu_0", "1201442", xk, RAY_B_Y, "cihaz_koyu", bom=("Uç tutucu Phoenix E/UK (1201442)", 2, KS.bom_kaynak("1201442"), ""))
    for i in range(20):
        pe = i >= 16
        din_step("ana_pano_klemens_%s_%02d" % ("PT2_5_PE" if pe else "PT2_5", i), "3209536" if pe else "3209510", xk, RAY_B_Y, "din" if pe else "cihaz",
                 bom=(("Klemens Phoenix PT 2,5 (3209510)", 16, KS.bom_kaynak("3209510"), "A soketi L / N + iç dağıtım") if i == 0 else
                      (("Toprak klemensi Phoenix PT 2,5-PE (3209536)", 4, KS.bom_kaynak("3209536"), "") if i == 16 else None)))
        xk += 5.2
    xa_ = din_step("ana_pano_klemens_uc_tutucu_1", "1201442", xk, RAY_B_Y, "cihaz_koyu")
    assert xa_ <= x1 - T - 2.0, xa_
    # Pt100 prob (pano içi hava · sol üst, plakaya klipsli) → AIO
    ekle("ana_pano_sicaklik_probu_Pt100", sil((3536.0, 2100.0, PLAKA["z"][1] + 6.0), (3536.0, 2150.0, PLAKA["z"][1] + 6.0), 3.0).fuse(
        kut(3530.0, 3542.0, 2120.0, 2130.0, PLAKA["z"][1], PLAKA["z"][1] + 3.0)), "celik",
         bom=("Pt100 sıcaklık probu Ø6 × 50 + plaka klipsi (pano içi hava)", 1, "katalog (2 telli / 3 telli Pt100 · ör. Jumo / Wika)", "v3.7 · RevPi AIO'ya · alarm ≥ 50 °C"))
    # ---------------- 4 · SOL YAN: HARTING İSTASYON SOKETLERİ + RAKORLAR ----------------
    fy, fz, ft = HAN["fl"]; gy, gz, gd = HAN["gv"]; iy, iz, idp = HAN["ic"]
    for i, (ist, xs_, ys, zs, yon) in enumerate(HARTING_SOKETLERI):
        if yon == "-z":
            ekle("ana_pano_harting_soketi_%s" % ist, _soket_arka(xs_, ys, z0), "harting",
                 bom=("İstasyon soketi Harting Han-Modular 10B bulkhead · ARKA YÜZ (A: Han E güç + Han RJ45 · F: sinyal modülü + Han RJ45)", 2,
                      "ölçü VARSAYIM (sol yandakilerle aynı tip)", "v3.6b · A: iDPN N C16 + klemens (L / N / PE) · F: güç YOK (fırın kendi CEE 32 A devresinde) · DIO çıkışı + Cat6A · "
                      "kablolar plaka kesiğinden orta kanala") if ist == "A" else None)
            continue
        h = kut(x0 - ft, x0, ys - fy / 2.0, ys + fy / 2.0, zs - fz / 2.0, zs + fz / 2.0)                     # flanş (sacın dışında, 4 × M4)
        h = h.fuse(kut(x0 - ft - gd, x0 - ft, ys - gy / 2.0, ys + gy / 2.0, zs - gz / 2.0, zs + gz / 2.0)        # gövde
                   .cut(kut(x0 - ft - gd - 1.0, x0 - ft - 8.0, ys - gy / 2.0 + 3.0, ys + gy / 2.0 - 3.0, zs - gz / 2.0 + 3.0, zs + gz / 2.0 - 3.0)))   # fiş ağzı (17 derin)
        h = h.fuse(kut(x0 - ft - 8.0, x0 + T + idp - 1.5, ys - iy / 2.0, ys + iy / 2.0, zs - iz / 2.0, zs + iz / 2.0))  # modül çerçevesi + kontak bloğu (içeri 27)
        for sg in (-1.0, 1.0):                                                                                     # kilit kolu (tek kollu Han B): yan pimler + kol
            h = h.fuse(kut(x0 - ft - gd + 2.0, x0 - ft - 4.0, ys - gy / 2.0 + 6.0, ys + gy / 2.0 - 6.0, zs + sg * (gz / 2.0) - (0.0 if sg > 0 else 2.5), zs + sg * (gz / 2.0) + (2.5 if sg > 0 else 0.0)))
        ekle("ana_pano_harting_soketi_%s" % ist, h.clean(), "harting",
             bom=("İstasyon soketi Harting Han-Modular 10B bulkhead (Han E güç modülü + Han RJ45 veri modülü) + tek kollu kilit", len(HARTING_SOKETLERI),
                  "ölçü VARSAYIM (flanş 83 × 57 · gövde 66 × 43 × 25) — harting.com föyden teyit", "v3.6 · istasyon kablosu fişli: TOPPING · DOLAP · K · E · ROBOT · QR") if i == 0 else None)
    # arka soketlerin kabloları: montaj plakasında + orta kanal tabanında geçiş kesiği (iç modül → orta kanal)
    for ist, xs_, ys, zs, yon in HARTING_SOKETLERI:
        if yon != "-z": continue
        kes = kut(xs_ - 12.0, xs_ + 12.0, 2030.0, 2042.0, PLAKA["z"][0] - 1.0, PLAKA["z"][1] + 1.6)
        for p in PARCALAR:
            if p["ad"] in ("ana_pano_montaj_plakasi", "ana_pano_kanal_orta"):
                p["wp"] = cq.Workplane(obj=dunya(p).cut(kes).clean())
    for i, (ad, s, m) in enumerate(rk):
        ekle("ana_pano_rakor_%s" % ad, s, "rakor",
             bom=("Kablo rakoru Lapp SKINTOP ST-M %d×1,5 + kilit somunu" % m, 1, "", "sol yan · bina beslemesi 5G6 (Lapp 16001313) / modem Cat6A / yedek kör tapa"))
    return PARCALAR


def _soket_arka(xs, ys, z0):
    """arka yüze (dış yüz z0, yön −z) Han 10B: flanş 83 (y) × 57 (x) · gövde 66 × 43 × 25 · iç modül 56 × 36 × 27 (sol yandakilerle aynı)"""
    fy, fx, ft = HAN["fl"]; gy, gx, gd = HAN["gv"]; iy, ix, idp = HAN["ic"]
    h = kut(xs - fx / 2.0, xs + fx / 2.0, ys - fy / 2.0, ys + fy / 2.0, z0 - ft, z0)
    h = h.fuse(kut(xs - gx / 2.0, xs + gx / 2.0, ys - gy / 2.0, ys + gy / 2.0, z0 - ft - gd, z0 - ft)
               .cut(kut(xs - gx / 2.0 + 3.0, xs + gx / 2.0 - 3.0, ys - gy / 2.0 + 3.0, ys + gy / 2.0 - 3.0, z0 - ft - gd - 1.0, z0 - ft - 8.0)))
    h = h.fuse(kut(xs - ix / 2.0, xs + ix / 2.0, ys - iy / 2.0, ys + iy / 2.0, z0 - ft - 8.0, z0 + T + idp - 1.5))
    for sg in (-1.0, 1.0):
        h = h.fuse(kut(xs + sg * (gx / 2.0) - (0.0 if sg > 0 else 2.5), xs + sg * (gx / 2.0) + (2.5 if sg > 0 else 0.0),
                       ys - gy / 2.0 + 6.0, ys + gy / 2.0 - 6.0, z0 - ft - gd + 2.0, z0 - ft - 4.0))
    return h.clean()


def _uf_fanlar():
    try:
        import h3_ust_depo_v2 as UD
        return [list(v) for v in UD.uf_fan_kablo_noktalari()]
    except Exception as e:
        return "h3_ust_depo_v2 yüklenemedi: %s" % e


def _dav_fan_klemens():
    try:
        import h3_firin_ust_v1 as FU
        return FU.DAV_FAN_KLEMENS
    except Exception:
        return (3460.0, 1490.0, -742.0)


def sozlesme(yol=None):
    """elektrik ajanı arayüzü (dünya · mm) → json"""
    o = dict(durum="KESİN (h3_ana_pano_v1 · 1 Eki 2026 · v3.6)", kaynak="arastirma/_uretec/h3/h3_ana_pano_v1.py",
             eksen="x hat boyunca · y yukarı (zemin 0) · z koridora (+79 ön, −830 arka) · mm",
             PANO_KUTU=list(PANO_KUTU), birim=BIRIM,
             GIRIS_RAKORLARI=[list(r) for r in GIRIS_RAKORLARI],
             GIRIS_RAKORLARI_alanlar="(ad, x sac dış yüzü, y, z, yön (kablo dışarıdan bu yönden gelir), rakor diş çapı M) · rakor gövdesi dış yüzden 12 mm −x · kablo ucu x 3506'da bitirilebilir",
             HARTING_SOKETLERI=[list(h) for h in HARTING_SOKETLERI],
             HARTING_alanlar="(istasyon, x, y, z soket ağzı (fiş buraya oturur), yön) · sol yan 6 soket yön −x (v3.7: ağız x 3489,1 · serbest bölge x 3335–3489) · arka yüz A + F yön −z (v3.7: ağız z −348,9; fiş + kablo arkaya → U_F üst hat kanalına) · fiş + başlık ≈ 75 mm · Han B 10 ölçüsü distribütörden (93 × 43,4 × 28,9)",
             kablo_bolgesi=dict(x=(3335.0, 3490.0), y=(1866.0, 2165.0), z=(-290.0, -90.0),
                                not_="soket fiş bölgesi (U_F içi, pizza raf kirişi 3329'un sağı) · U_F arka üst hat kanalı ust_hat_U_F y 2143–2166,5 z −826…−766"),
             kapak=dict(eksen=list(KAPAK_EKSEN["KAPAK_ANA_PANO"][0]), yon=list(KAPAK_EKSEN["KAPAK_ANA_PANO"][1]), aci=KAPAK_EKSEN["KAPAK_ANA_PANO"][2]),
             U_F_FANLAR=_uf_fanlar(),
             U_F_FANLAR_alanlar="(ad, x, y, z bağlantı ucu) · 4 × 4414 FL 24 V DC (1,2 W) + STEGO KTS 011 · panoya fan_24V_M20 rakoru (sol yan, y 2117 · z −190) · termostat NO: + hattını keser",
             DAVLUMBAZ_FANI=dict(ad="Systemair RS 30-15 sileo · 230 V 51 W", klemens=list(_dav_fan_klemens()), rakor="F_UST arka sac 'davlumbaz_fani' M20 (x 2600 · y 1825 · z −830)",
                                 besleme="AÇIK: ana panoda raf yeri yok (ray A 3 mm pay) → fırın devresinden ya da ayrı C6 (karar)"),
             sigortalar=["TOPPING C16", "DOLAP C16", "K C16", "E C16", "ROBOT C16", "QR C16", "A C16 (iDPN N)", "PANO_24V C6 (iDPN N)", "F: YOK — fırın kendi CEE 32 A devresinde (bina, arka rakor)"])
    if yol:
        json.dump(o, io.open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return o


if __name__ == "__main__":
    kur()
    h = pano_olcu_hesabi()
    print("parça", len(PARCALAR)); print({k: round(v, 2) for k, v in h.items()})
    sys.stdout.flush(); os._exit(0)
