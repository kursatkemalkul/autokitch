# -*- coding: utf-8 -*-
"""AUTOKITCH · S · QR TESLİM DOLABI · CAD v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · QR_TEZGAH_v4 resmi)
Kemal: "bu teknik resme göre 3D modelle" (QR_TEZGAH_v4 onaylı). Koridorun karşısında, robot yüzü z 670, müşteri yüzü z 1190.

YERLEŞİM (dünya): x 4570–5430 · y 0–2050 · z 670 (robot tarafı) … 1190 (müşteri tarafı)
  ayak 0–17 + taban plakası 17–20 · ALT BÖLME 20–447: ROBOT KONTROL KUTUSU rezervi 475 × 423 × 268 (x 4595–5070, z 675–943)
  + robot kablosu kangalı (x 5080–5405, y 20–300 bölgesi; kangalın kendisi ray_ek_cad_v1'de, çünkü boyu kablo yolundan hesaplanır)
  · raf 447–450 · 12 GÖZ 2 sütun × 6 satır (göz 380 × 190 × 440, sütun x 4600–4980 / 5010–5390, z 710–1150, tabanlar 450, 650 … 1450)
  · raf 1650–1653 · ÜST BÖLME 1653–2048: ANA PANO 400 × 350 × 250 + UPS APC Back-UPS BX500CI 115 × 185 × 213 + QR kilit/kapak/ısıtıcı kartı
  (~270 × 200, VARSAYIM) + 24 V güç kaynağı + modem · tavan 2048–2050.
GÖZ (eski SERVİS_TESLİM v4 tasarımından): robot tarafında MOTORLU KAPAK (üstten menteşeli, içeri-yukarı açılır; dik açılı sonsuz vidalı
  mini motor göz ağzının sol üst köşesinde), müşteri tarafında ELEKTRİKLİ MANDALLI KAPI (it-aç), TABAN ISITICISI 60 °C (silikon ped +
  3 mm alüminyum taban). Müşteri yüzünde QR okuyucu + PIN tuş takımı + 7" ekran (üst bölmenin önünde).
Teknik bölmelerin SERVİS KAPAKLARI robot tarafında (menteşe solda, çeyrek dönüş kilit sağda); her bölmede alt yarık ızgara (giriş) +
  üstte filtreli fan (çıkış).
KOORDİNAT: parçalar YEREL kurulur (x 0…860 dolabın solundan, y yerden, z 0 = robot yüzü … 520 = müşteri yüzü) ve ekle()'de
  (X0, Y0, Z0) = (4570, 0, 670) ile dünyaya taşınır (bulasik_cad_v1 gibi: X0/Y0/Z0 kur()'dan önce değiştirilebilir).
SABİT (ölçüsü alınmış, DEĞİŞTİRİLMEZ): robot kontrol 475 × 423 × 268 · ana pano 400 × 350 × 250 · UPS 115 × 185 × 213 · göz 380 × 190 × 440.
VARSAYIM yazılanlar kaynaksızdır; katalog/teyit gerekir.
"""
import csv, io, math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)

# ---------------------------------------------------------------- YERLEŞİM + ÖLÇÜLER ----------------------------------------------------------------
X0, Y0, Z0 = 4570.0, 0.0, 670.0          # dolabın sol · zemin · robot yüzü (SPEC v57 · QR_TEZGAH v4)
W, H, D = 860.0, 2050.0, 520.0            # SPEC: 860 × 520 × 2050
SAC = 1.5
AYAK = 17.0                               # ayak 0–17 + taban plakası 17–20 → "ayak 0–20" (SPEC)
TABAN = (17.0, 20.0)
ALT_BOLME = (20.0, 447.0)
ALT_RAF = (447.0, 450.0)
UST_RAF = (1650.0, 1653.0)
UST_BOLME = (1653.0, 2048.0)
TAVAN = (2048.0, 2050.0)
GOZ_W, GOZ_H, GOZ_D = 380.0, 190.0, 440.0                 # SABİT
GOZ_ADIM = 200.0
GOZ_TABAN = tuple(450.0 + GOZ_ADIM * r for r in range(6))  # 450, 650 … 1450
GOZ_X = (30.0, 440.0)                     # yerel · dünya 4600–4980 / 5010–5390
GOZ_Z = (40.0, 480.0)                     # yerel · dünya 710–1150
KONTROL = dict(x=(25.0, 500.0), y=(20.0, 443.0), z=(5.0, 273.0))      # dünya x 4595–5070 · z 675–943 · 475 × 423 × 268 SABİT
ANA_PANO = dict(x=(25.0, 425.0), y=(1658.0, 2008.0), z=(5.0, 255.0))  # 400 × 350 × 250 SABİT
UPS = dict(x=(435.0, 550.0), y=(1658.0, 1843.0), z=(5.0, 218.0))      # APC Back-UPS BX500CI 115 × 185 × 213 SABİT
KART = dict(x=(560.0, 830.0), y=(1665.0, 1865.0))                     # QR kilit/kapak/ısıtıcı kartı 270 × 200 VARSAYIM
KANGAL_BOLGE = dict(x=(510.0, 835.0), y=(20.0, 300.0), z=(20.0, 290.0))  # dünya x 5080–5405 · y 20–300 · z 690–960 (kangal ray_ek'te)
KANGAL = dict(xc=672.5, zc=155.0, r_ic=115.0, r_dis=135.0, y0=20.0)   # yerel · dünya merkez (5242,5 · 825) · Ø270 · kablo Ø20 tek sıra
GECIS_ROBOT = (210.0, 305.0, 20.0)        # taban kablo geçişi (x, z, yarıçap) · dünya (4780, 975) · Ø40 lastik rakor
GECIS_GUC = (250.0, 305.0, 15.0)          # ana pano güç/veri kabloları · dünya (4820, 975) · Ø30 (VARSAYIM)
KONNEKTOR = (500.0, 120.0, 230.0)         # robot kablosu soketi kontrol kutusunun SAĞ yüzünde · dünya (5070, 120, 900) VARSAYIM
FAN = dict(alt=(655.0, 805.0, 275.0, 425.0), ust=(675.0, 825.0, 1885.0, 2035.0), derin=40.0)   # filtreli fan 150 × 150 × 40 VARSAYIM
FAN_M3H = 90.0                            # 120 mm 24 V fan serbest debi VARSAYIM (filtreyle ~%50)
KILIT_Y = (234.0, 1850.0)                 # çeyrek dönüş kilitleri (alt, üst servis kapağı)
# robot (montaj / pafta): ray ekseni z 360 (DEĞİŞMEZ), omuz 970, pratik erişim 779, robot dolabın ortasında durur (x 5000)
RZ, OMUZ, ERISIM = 360.0, 970.0, 779.0
ROBOT_X = X0 + W / 2.0
BILEK_PAY = 100.0                         # bilek hedefi = göz tabanı + 100 (çatal + kutu) VARSAYIM (QR_TEZGAH v2)
ISITICI_T = 60.0                          # göz taban ısıtıcısı (SERVİS_TESLİM v4)
ORTAM_T = 25.0                            # VARSAYIM
H_TABAN = 10.0                            # taban plakası üstünden ısı kaybı katsayısı W/m²K (doğal taşınım + ışınım) VARSAYIM

PARCALAR = []
MODUL = "S"                               # SPEC: QR + tezgâh yeni modül "S" (SERVİS / TESLİM) → modul_S.glb
BIRIMLER = [
    ("QR_GOVDE", "QR teslim dolabı gövdesi · 860 × 520 × 2050 · x 4570–5430 · z 670 (robot) … 1190 (müşteri) · 6 ayar ayağı · raflar 447 / 1650 · robot tarafında 2 servis kapağı (menteşe + çeyrek dönüş kilit)"),
    ("QR_GOZLER", "12 ısıtmalı göz 2 × 6 · 380 × 190 × 440 · tabanlar 450…1450 · robot tarafı motorlu kapak · müşteri tarafı elektrikli mandallı kapı · taban ısıtıcısı 60 °C"),
    ("QR_ROBOT_KONTROL", "Robot kontrol kutusu (Fairino FR5) · REZERV 475 × 423 × 268 · alt bölme, robot tarafı · x 4595–5070 · z 675–943"),
    ("QR_ANA_PANO", "Ana pano (PLC · ana şalter) 400 × 350 × 250 · üst bölme, robot tarafı"),
    ("QR_UPS", "UPS APC Back-UPS BX500CI 500 VA · 115 × 185 × 213 · yalnız PLC + modem + kilitler"),
    ("QR_KILIT_KARTI", "QR kilit/kapak/ısıtıcı kartı ~270 × 200 (VARSAYIM) + 24 V güç kaynağı + modem · üst bölme montaj plakası"),
    ("QR_MUSTERI_PANELI", "Müşteri paneli · 7\" ekran + QR okuyucu + PIN tuş takımı · müşteri yüzü, üst bölmenin önü"),
    ("QR_HAVALANDIRMA", "Havalandırma · alt + üst teknik bölmede filtreli fan (çıkış) · servis kapaklarında yarık ızgara (giriş)"),
]
BIRIM_MODUL = {k: MODUL for k, _a in BIRIMLER}
ON_BIRIMLER = tuple(k for k, _a in BIRIMLER)     # hepsi hattın önünde (z > 0) · montajın ÖN YÜZ istisnası "QR" öneki ile zaten kapsıyor
MALZEME = {"qr_govde": dict(renk=(0.30, 0.32, 0.35, 1.0), met=0.35, ruf=0.45), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "aluminyum": dict(renk=(0.86, 0.87, 0.89, 1.0), met=0.8, ruf=0.35), "isitici": dict(renk=(0.85, 0.25, 0.18, 1.0), met=0.0, ruf=0.6),
           "motor": dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45), "sensor": dict(renk=(0.95, 0.75, 0.10, 1.0), met=0.0, ruf=0.5),
           "plastik": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6), "robot_kutu": dict(renk=(0.96, 0.62, 0.10, 1.0), met=0.2, ruf=0.45),
           "pano": dict(renk=(0.86, 0.87, 0.88, 1.0), met=0.3, ruf=0.4), "ups": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.1, ruf=0.5),
           "kart": dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6), "ekran_cam": dict(renk=(0.06, 0.07, 0.09, 1.0), met=0.3, ruf=0.10),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "kapak_pc": dict(renk=(0.78, 0.80, 0.82, 1.0), met=0.6, ruf=0.35)}


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    """bom = (kalem, adet, tanım, kaynak/not, tür)"""
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp.translate((X0, Y0, Z0)), mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def goz_listesi():
    """(satır, sütun, sütun sol x yerel, göz tabanı y)"""
    return [(r, c, GOZ_X[c], GOZ_TABAN[r]) for r in range(6) for c in range(2)]


# ---------------------------------------------------------------- 1 · GÖVDE ----------------------------------------------------------------
def govde():
    b = "QR_GOVDE"
    for i, (x, z) in enumerate(((30.0, 30.0), (430.0, 30.0), (830.0, 30.0), (30.0, 490.0), (430.0, 490.0), (830.0, 490.0))):
        ekle("ayar_ayagi_%d" % i, sily(x, z, 20.0, 0.0, 5.0).union(sily(x, z, 8.0, 5.0, AYAK)), "celik", b,
             bom=("Ayar ayağı M10 düşük profil (17 mm)", 6, "paslanmaz taban Ø40 · ±5 ayar", "VARSAYIM · katalogdan seçilecek", "SATIN ALMA") if i == 0 else None)
    tb = kut(0.0, W, TABAN[0], TABAN[1], 0.0, D)
    for (gx, gz, gr) in (GECIS_ROBOT, GECIS_GUC):
        tb = tb.cut(sily(gx, gz, gr, TABAN[0] - 1, TABAN[1] + 1))
    ekle("taban_plakasi_3", tb, "qr_govde", b, bom=("Taban plakası 3 mm DKP (boyalı)", 1, "860 × 520 · Ø40 robot kablosu + Ø30 güç/veri geçişi (lastik rakorlu)", "üretim", "ÜRETİM"))
    ekle("yan_sac_sol", kut(0.0, SAC, TABAN[1], TAVAN[0], 0.0, D), "qr_govde", b, bom=("Yan sac 1,5 mm DKP (boyalı)", 2, "520 × 2028", "üretim", "ÜRETİM"))
    ekle("yan_sac_sag", kut(W - SAC, W, TABAN[1], TAVAN[0], 0.0, D), "qr_govde", b)
    ekle("tavan_sac", kut(0.0, W, TAVAN[0], TAVAN[1], 0.0, D), "qr_govde", b, bom=("Tavan sacı 2 mm DKP", 1, "860 × 520", "üretim", "ÜRETİM"))
    ekle("alt_raf_3", kut(SAC, W - SAC, ALT_RAF[0], ALT_RAF[1], SAC, D - SAC), "qr_govde", b, bom=("Raf 3 mm DKP (alt + üst)", 2, "857 × 517", "üretim", "ÜRETİM"))
    ekle("ust_raf_3", kut(SAC, W - SAC, UST_RAF[0], UST_RAF[1], SAC, D - SAC), "qr_govde", b)
    # robot yüzü: göz bölgesi sacı (12 kapak ağzı) · müşteri yüzü: göz bölgesi sacı (12 kapı ağzı) + alt ve üst panel
    rs = kut(SAC, W - SAC, ALT_RAF[0], UST_RAF[1], 0.0, SAC)
    ms = kut(SAC, W - SAC, ALT_RAF[0], UST_RAF[1], D - SAC, D)
    for r, c, cx, by in goz_listesi():
        rs = rs.cut(kut(cx + 38.0, cx + 378.0, by + 4.0, by + 186.0, -1.0, SAC + 1.0))
        ms = ms.cut(kut(cx + 1.0, cx + 379.0, by + 1.0, by + 189.0, D - SAC - 1.0, D + 1.0))
    ekle("robot_yuzu_goz_saci", rs, "qr_govde", b, bom=("Robot yüzü sacı 1,5 mm · 12 kapak ağzı 340 × 182", 1, "857 × 1206", "üretim (lazer)", "ÜRETİM"))
    ekle("musteri_yuzu_goz_saci", ms, "qr_govde", b, bom=("Müşteri yüzü sacı 1,5 mm · 12 kapı ağzı 378 × 188", 1, "857 × 1206", "üretim (lazer)", "ÜRETİM"))
    ekle("musteri_alt_panel", kut(SAC, W - SAC, TABAN[1], ALT_RAF[0], D - SAC, D), "qr_govde", b, bom=("Müşteri alt paneli 1,5 mm (kapalı)", 1, "857 × 427", "üretim", "ÜRETİM"))
    up = kut(SAC, W - SAC, UST_RAF[1], TAVAN[0], D - SAC, D)
    for (a_, b_, c_, d_) in PANEL_PENCERE.values():
        up = up.cut(kut(a_, b_, c_, d_, D - SAC - 1.0, D + 1.0))
    ekle("musteri_ust_panel", up, "qr_govde", b, bom=("Müşteri üst paneli 1,5 mm · ekran + okuyucu + PIN pencereleri", 1, "857 × 395", "üretim (lazer)", "ÜRETİM"))
    # servis kapakları (robot tarafı) · yarık ızgara (giriş) + fan deliği + kilit deliği
    for ad_, (ya, yb), (sx0, sx1, sy0, sy1), fan, ky in (("alt", (TABAN[1] + 1.0, ALT_RAF[0] - 1.0), (520.0, 840.0, 40.0, 110.0), FAN["alt"], KILIT_Y[0]),
                                                           ("ust", (UST_RAF[1] + 1.0, TAVAN[0] - 1.0), (560.0, 840.0, 1665.0, 1735.0), FAN["ust"], KILIT_Y[1])):
        k = kut(2.5, W - 2.5, ya, yb, 0.0, SAC)
        n = int((sx1 - sx0 + 10.0) // 40.0)
        for i in range(n):
            k = k.cut(kut(sx0 + 40.0 * i, sx0 + 40.0 * i + 30.0, sy0, sy1, -1.0, SAC + 1.0))
        k = k.cut(silz((fan[0] + fan[1]) / 2.0, (fan[2] + fan[3]) / 2.0, 58.0, -1.0, SAC + 1.0))
        k = k.cut(silz(835.0, ky, 11.5, -1.0, SAC + 1.0))
        ekle("servis_kapagi_%s" % ad_, k, "qr_govde", b,
             bom=("Servis kapağı 1,5 mm · yarık ızgara 30 × 70 (alt 8 · üst 7) + fan deliği Ø116", 2, "855 × %.0f (alt) + 855 × %.0f (üst)" % (ALT_RAF[0] - TABAN[1] - 2.0, TAVAN[0] - UST_RAF[1] - 2.0),
                  "üretim (lazer + büküm)", "ÜRETİM") if ad_ == "alt" else None)   # denetçi: önce iki kapak için de 855 × 425 yazıyordu
        IZGARA_ALAN[ad_] = n * 30.0 * (sy1 - sy0)
        ekle("servis_kilidi_%s" % ad_, silz(835.0, ky, 11.0, 0.0, 30.0), "celik", b,
             bom=("Çeyrek dönüş kilit (anahtarlı) Ø22", 2, "servis kapakları", "VARSAYIM · katalog (ör. kabin kilidi sınıfı)", "SATIN ALMA") if ad_ == "alt" else None)
    for i, y in enumerate((50.0, 370.0, 1690.0, 1970.0)):
        ekle("servis_mentesesi_%d" % i, kut(SAC, 20.0, y, y + 40.0, SAC, 19.5), "celik", b,
             bom=("Gizli menteşe (servis kapağı)", 4, "2 kapak × 2", "VARSAYIM · katalog", "SATIN ALMA") if i == 0 else None)


KAPAK_MIL_Y = 180.0                       # robot kapağı mili göz tabanından (açıkken kapak göz tavanının 4 mm altında kalır)
MENTESE = {}                              # grup → ((pivot dünya), eksen, açık açı °) · montaj animasyonu için
PANEL_PENCERE = {"ekran": (270.0, 435.0, 1668.0, 1768.0), "okuyucu": (475.0, 545.0, 1688.0, 1738.0), "pin": (583.0, 663.0, 1678.0, 1758.0)}
IZGARA_ALAN = {}


# ---------------------------------------------------------------- 2 · 12 GÖZ ----------------------------------------------------------------
def gozler():
    b = "QR_GOZLER"
    ilk = True
    for r, c, cx, by in goz_listesi():
        n = "goz_%d%d" % (r, c)
        k = kut(cx, cx + GOZ_W, by, by + GOZ_H, GOZ_Z[0], GOZ_Z[1]).cut(kut(cx + 1.0, cx + GOZ_W - 1.0, by + 1.0, by + GOZ_H - 1.0, GOZ_Z[0] - 1.0, GOZ_Z[1] + 1.0))
        ekle(n + "_kasasi", k, "paslanmaz", b, bom=("Göz kasası AISI 304 1 mm (iki ucu açık tüp)", 12, "380 × 190 × 440 dış", "üretim (büküm + punta)", "ÜRETİM") if ilk else None)
        ekle(n + "_isitici_ped", kut(cx + 20.0, cx + 360.0, by + 1.0, by + 2.5, GOZ_Z[0] + 20.0, GOZ_Z[1] - 20.0), "isitici", b,
             bom=("Silikon ısıtıcı ped 340 × 400 · %.0f W · NTC + aşırı ısı termostatı" % ISITICI_W, 12, "taban 60 °C (SERVİS_TESLİM v4)", "VARSAYIM güç: hesap A × h × ΔT", "SATIN ALMA") if ilk else None)
        ekle(n + "_taban_plakasi", kut(cx + 1.0, cx + GOZ_W - 1.0, by + 2.5, by + 5.5, GOZ_Z[0] + 1.0, GOZ_Z[1] - 1.0), "aluminyum", b,
             bom=("Göz tabanı alüminyum 3 mm (ısı yayıcı)", 12, "378 × 438", "üretim", "ÜRETİM") if ilk else None)
        # robot tarafı motorlu kapak (kapalı konum; üstten menteşeli, içeri-yukarı açılır)
        gk, gd = "GOZ_%d%d_KAPAK" % (r, c), "GOZ_%d%d_KAPI" % (r, c)          # hareketli gruplar (MENTESE'de mil ekseni + açı)
        ekle(n + "_robot_kapagi", kut(cx + 40.0, cx + 376.0, by + 6.0, by + KAPAK_MIL_Y - 4.0, 6.0, 16.0), "kapak_pc", b,
             bom=("Robot kapağı 10 mm (AISI 304 çift cidar + yalıtım)", 12, "336 × 170 · içeri-yukarı açılır (90°)", "üretim · VARSAYIM kalınlık", "ÜRETİM") if ilk else None,
             grup=gk)
        ekle(n + "_kapak_mili", silx(by + KAPAK_MIL_Y, 11.0, 3.0, cx + 36.0, cx + 378.0), "celik", b,
             bom=("Kapak mili Ø6 paslanmaz", 12, "boy 342", "üretim", "ÜRETİM") if ilk else None, grup=gk)
        ekle(n + "_mil_yatagi", kut(cx + 378.0, cx + 384.0, by + KAPAK_MIL_Y - 6.0, by + KAPAK_MIL_Y + 6.0, 5.0, 17.0), "plastik", b,
             bom=("Mil yatağı (POM burç)", 12, "", "üretim", "ÜRETİM") if ilk else None)
        MENTESE[gk] = ((X0 + cx + 36.0, Y0 + by + KAPAK_MIL_Y, Z0 + 11.0), (1.0, 0.0, 0.0), -90.0)
        ekle(n + "_kapak_motoru", kut(cx + 2.0, cx + 34.0, by + 140.0, by + 188.0, 3.0, 39.0), "motor", b,
             bom=("Dik açılı sonsuz vidalı mini redüktörlü motor 24 V", 12, "zarf 32 × 48 × 36 · çıkış mili kapak miline", "VARSAYIM · ürün seçilecek", "SATIN ALMA") if ilk else None)
        ekle(n + "_kapak_sensoru", kut(cx + 378.0, cx + 392.0, by + 8.0, by + 18.0, 6.0, 16.0), "sensor", b,
             bom=("Kapak kapalı sensörü (endüktif / reed)", 12, "", "VARSAYIM", "SATIN ALMA") if ilk else None)
        # müşteri tarafı kapı + menteşe + elektrikli mandal + karşılık
        ekle(n + "_musteri_kapisi", kut(cx + 2.0, cx + 378.0, by + 2.0, by + 188.0, D - 14.0, D), "paslanmaz", b,
             bom=("Müşteri kapısı 14 mm (AISI 304 çift cidar + yalıtım) · numaralı", 12, "376 × 186", "üretim · VARSAYIM kalınlık", "ÜRETİM") if ilk else None, grup=gd)
        MENTESE[gd] = ((X0 + cx + (2.0 if c == 0 else 378.0), Y0 + by, Z0 + D), (0.0, 1.0, 0.0), -90.0 if c == 0 else 90.0)
        hx = (cx - 10.0, cx + 10.0) if c == 0 else (cx + 370.0, cx + 390.0)
        for j, hy in enumerate((20.0, 140.0)):
            ekle(n + "_mentese_%d" % j, kut(hx[0], hx[1], by + hy, by + hy + 30.0, D - 30.0, D - 14.0), "celik", b,
                 bom=("Gizli menteşe (müşteri kapısı)", 24, "12 kapı × 2", "VARSAYIM · katalog", "SATIN ALMA") if ilk and j == 0 else None)
        ly = by + (60.0 if c == 0 else 125.0)
        ekle(n + "_elektrikli_mandal", kut(415.0, 435.0, ly, ly + 55.0, 481.0, 505.0), "motor", b,
             bom=("Elektrikli mandal 24 V (it-aç, geri bildirimli)", 12, "zarf 20 × 55 × 24 · sütunlar arası 30 mm boşlukta", "VARSAYIM · kilit dolabı mandalı sınıfı", "SATIN ALMA") if ilk else None)
        sx = (cx + 366.0, cx + 378.0) if c == 0 else (cx + 2.0, cx + 14.0)
        ekle(n + "_karsilik", kut(sx[0], sx[1], ly + 10.0, ly + 45.0, D - 20.0, D - 14.0), "celik", b, grup=gd)
        ilk = False
    # göz taşıyıcı dikmeler (8): sütun kenarları, ön ve arka · kasalar bunlara cıvatalı
    for i, (xa, xb) in enumerate(((20.0, 30.0), (410.0, 420.0), (430.0, 440.0), (820.0, 830.0))):
        for j, (za, zb) in enumerate(((42.0, 62.0), (458.0, 478.0))):
            ekle("goz_dikmesi_%d%d" % (i, j), kut(xa, xb, ALT_RAF[1], UST_RAF[0], za, zb), "qr_govde", b,
                 bom=("Göz taşıyıcı dikme lama 10 × 20 (delikli)", 8, "boy 1200", "üretim", "ÜRETİM") if i == 0 and j == 0 else None)


# ---------------------------------------------------------------- 3 · TEKNİK BÖLMELER ----------------------------------------------------------------
def teknik():
    k = KONTROL
    ekle("robot_kontrol_kutusu_REZERV", kut(k["x"][0], k["x"][1], k["y"][0], k["y"][1], k["z"][0], k["z"][1]), "robot_kutu", "QR_ROBOT_KONTROL",
         bom=("Fairino FR5 kontrol kutusu (robotla gelir)", 1, "REZERV 475 × 423 × 268 (proje sabiti) · Fairino kompakt kutu 245 × 180 × 89 olabilir",
              "montaj v56 D_ROBOT_KONTROL notu · Fairino'ya teyit", "SATIN ALMA"))
    a = ANA_PANO
    ekle("ana_pano_400x350x250", kut(a["x"][0], a["x"][1], a["y"][0], a["y"][1], a["z"][0], a["z"][1]), "pano", "QR_ANA_PANO",
         bom=("Ana pano (PLC · ana şalter · sigortalar) 400 × 350 × 250", 1, "kapak robot tarafına (servis kapağından)", "ölçü proje sabiti · içerik ayrı pafta", "SATIN ALMA"))
    for i, x in enumerate((40.0, 380.0)):
        ekle("ana_pano_ayak_rayi_%d" % i, kut(x, x + 30.0, UST_RAF[1], a["y"][0], 30.0, 230.0), "celik", "QR_ANA_PANO",
             bom=("Pano taşıyıcı ray 30 × 5", 2, "boy 200", "üretim", "ÜRETİM") if i == 0 else None)
    u = UPS
    ekle("ups_APC_BX500CI", kut(u["x"][0], u["x"][1], u["y"][0], u["y"][1], u["z"][0], u["z"][1]), "ups", "QR_UPS",
         bom=("UPS APC Back-UPS BX500CI 500 VA / 300 W", 1, "115 × 185 × 213 · yalnız PLC + modem + QR kilitleri (ısıtıcılar HARİÇ)", "schneider-electric.com BX500CI", "SATIN ALMA"))
    ekle("ups_altligi", kut(u["x"][0] + 5.0, u["x"][1] - 5.0, UST_RAF[1], u["y"][0], 20.0, 200.0), "plastik", "QR_UPS")
    # kilit kartı montaj plakası (L ayaklı, üst rafa cıvatalı) + kart + güç kaynağı + modem
    b = "QR_KILIT_KARTI"
    ekle("kart_plakasi_ayak", kut(555.0, 840.0, UST_RAF[1], UST_RAF[1] + 3.0, 390.0, 430.0), "celik", b)
    ekle("kart_montaj_plakasi", kut(555.0, 840.0, UST_RAF[1] + 3.0, 2040.0, 430.0, 433.0), "celik", b,
         bom=("Montaj plakası 3 mm galvaniz (L ayaklı)", 1, "285 × 387", "üretim", "ÜRETİM"))
    ekle("kilit_karti_PCB", kut(KART["x"][0], KART["x"][1], KART["y"][0], KART["y"][1], 418.4, 420.0), "kart", b,
         bom=("QR kilit / kapak / ısıtıcı kartı (12 motor sürücü + 12 mandal + 12 SSR + sensör girişleri · RS485/Ethernet)", 1, "~270 × 200", "VARSAYIM · özel kart ya da kilit dolabı kontrolcüsü", "SATIN ALMA"))
    ekle("kilit_karti_elemanlari", kut(575.0, 815.0, 1680.0, 1850.0, 400.0, 418.4), "kart", b)
    for i, (x, y) in enumerate(((570.0, 1675.0), (820.0, 1675.0), (570.0, 1855.0), (820.0, 1855.0))):
        ekle("kart_ayakcigi_%d" % i, silz(x, y, 3.0, 420.0, 430.0), "celik", b, bom=("Mesafe burcu M3 × 10", 4, "", "katalog", "SATIN ALMA") if i == 0 else None)
    ekle("din_rayi", kut(560.0, 660.0, 1905.0, 1940.0, 422.5, 430.0), "celik", b, bom=("DIN ray 35 × 7,5", 1, "boy 100", "EN 60715", "SATIN ALMA"))
    ekle("guc_kaynagi_24V_HDR-60-24", kut(565.0, 617.5, 1877.5, 1967.5, 368.0, 422.5), "aluminyum", b,
         bom=("Güç kaynağı Mean Well HDR-60-24 (DIN)", 1, "24 V 2,5 A · kart + 12 kapak motoru + 12 mandal (aynı anda 1 göz)", "meanwell.com HDR-60 · 52,5 × 90 × 54,5 [ölçü teyit]", "SATIN ALMA"))
    ekle("modem_4G", kut(670.0, 830.0, 1880.0, 2010.0, 395.0, 430.0), "plastik", b,
         bom=("4G / Ethernet modem-router", 1, "zarf 160 × 130 × 35", "VARSAYIM", "SATIN ALMA"))
    # müşteri paneli (üst bölmenin önü, sac pencerelerinin arkasında)
    b = "QR_MUSTERI_PANELI"
    ekle("ekran_7in", kut(265.0, 440.0, 1663.0, 1773.0, D - 27.0, D - SAC), "ekran_cam", b,
         bom=("7\" dokunmatik ekran modülü (sipariş no / göz no gösterir)", 1, "zarf 175 × 110 × 25", "VARSAYIM", "SATIN ALMA"))
    ekle("qr_okuyucu", kut(470.0, 550.0, 1683.0, 1743.0, D - 47.0, D - SAC), "plastik", b,
         bom=("Gömme 2D QR okuyucu modülü (telefon ekranından okur)", 1, "zarf 80 × 60 × 45", "VARSAYIM", "SATIN ALMA"))
    ekle("pin_tus_takimi", kut(580.0, 666.0, 1675.0, 1761.0, D - 31.5, D - SAC), "paslanmaz", b,
         bom=("Paslanmaz PIN tuş takımı 4 × 4 (vandal dayanımlı)", 1, "86 × 86 × 30", "VARSAYIM", "SATIN ALMA"))
    # havalandırma: filtreli fanlar (kapakların iç yüzünde, dışarı üfler)
    b = "QR_HAVALANDIRMA"
    for ad_, f in (("alt", FAN["alt"]), ("ust", FAN["ust"])):
        ekle("filtreli_fan_%s" % ad_, kut(f[0], f[1], f[2], f[3], SAC, SAC + FAN["derin"]), "plastik", b,
             bom=("Filtreli fan 120 mm 24 V (çıkış) + filtre matı", 2, "zarf 150 × 150 × 40 · serbest debi %.0f m³/h" % FAN_M3H, "VARSAYIM · pano fanı sınıfı", "SATIN ALMA") if ad_ == "alt" else None)


ISITICI_A = (GOZ_W - 2.0) * (GOZ_D - 2.0) / 1e6                      # m²
ISITICI_W = math.ceil(ISITICI_A * H_TABAN * (ISITICI_T - ORTAM_T) / 10.0) * 10.0


def kur():
    PARCALAR[:] = []; MENTESE.clear()
    govde(); gozler(); teknik()
    return PARCALAR


# ---------------------------------------------------------------- DENETİM ----------------------------------------------------------------
ISTISNA = []          # bilerek temas/iç içe parça çifti YOK (delikler kesildi)


def _ist(a, b):
    return any((p in a and q in b) or (p in b and q in a) for p, q in ISTISNA)


def _bbk(A, B, pay=0.01):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def kendi_arasinda(ps, istisna=_ist, esik=1.0):
    S = [(p["ad"], dunya(p)) for p in ps]
    S = [(a, s, s.BoundingBox()) for a, s in S]
    out = []
    for i, (a, sa, A) in enumerate(S):
        for c, sc, B in S[i + 1:]:
            if not _bbk(A, B) or istisna(a, c):
                continue
            v = sa.intersect(sc).Volume()
            if v > esik: out.append((round(v, 1), a, c))
    return out


def capraz(ps, qs, esik=1.0):
    """iki parça listesi arasında (dünya) kesişim > eşik"""
    S = [(p["ad"], dunya(p)) for p in ps]; S = [(a, s, s.BoundingBox()) for a, s in S]
    T = [(q["ad"], q["_sh"] if "_sh" in q else q["wp"].val()) for q in qs]; T = [(a, s, s.BoundingBox()) for a, s in T]
    out = []
    for a, sa, A in S:
        for c, sc, B in T:
            if _bbk(A, B):
                v = sa.intersect(sc).Volume()
                if v > esik: out.append((round(v, 1), a, c))
    return out


def erisim_tablosu():
    """robot x 5000'de durur (dolap ortası); omuz (5000, 970, 360); bilek hedefi (göz sütunu ortası, göz tabanı + 100, robot yüzü z 670)"""
    sat = []
    for r, c, cx, by in goz_listesi():
        gx = X0 + cx + GOZ_W / 2.0
        hy = Y0 + by + BILEK_PAY
        hz = Z0
        d = math.sqrt((gx - ROBOT_X) ** 2 + (hy - OMUZ) ** 2 + (hz - RZ) ** 2)
        sat.append((r, c, gx, by + Y0, hy, d))
    return sat


BOM_KLASOR = os.path.join(KOK, "arastirma", "6_QR_DOLABI_v1")


def bom_yaz(klasor=BOM_KLASOR, ps=None):
    ps = ps or PARCALAR
    os.makedirs(klasor, exist_ok=True)
    satir = []
    for p in ps:
        if p["bom"]:
            kalem, adet, tanim, not_, tur = p["bom"]
            satir.append((p["ad"], p["birim"], kalem, adet, tanim, not_, tur))
        else:
            bb = dunya(p).BoundingBox()
            satir.append((p["ad"], p["birim"], p["ad"].replace("_", " "), 0, "", "aynı kalemin eşi ya da alt parça · zarf %.0f × %.0f × %.0f" % (bb.xlen, bb.ylen, bb.zlen), "ALT"))
    with io.open(os.path.join(klasor, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w_ = csv.writer(f, delimiter=";"); w_.writerow(["parça (model adı)", "birim", "kalem", "adet", "tanım / ürün", "not / kaynak", "tür"])
        for r_ in satir: w_.writerow(r_)
    top, bil = {}, {}
    for _p, _b, kalem, adet, tanim, not_, tur in satir:
        if tur == "ALT": continue
        top[kalem] = top.get(kalem, 0) + int(adet); bil.setdefault(kalem, (tanim, not_, tur))
    with io.open(os.path.join(klasor, "BOM_OZET.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w_ = csv.writer(f, delimiter=";"); w_.writerow(["tür", "kalem", "toplam adet", "tanım / ürün", "not / kaynak"])
        for k_ in sorted(top, key=lambda a: (0 if bil[a][2] == "SATIN ALMA" else 1, a)):
            w_.writerow([bil[k_][2], k_, top[k_], bil[k_][0], bil[k_][1]])
    print("BOM: %s · %d satır · %d kalem (%d satın alma) · VARSAYIM geçen kalem %d" % (klasor, len(satir), len(top), sum(1 for k_ in top if bil[k_][2] == "SATIN ALMA"),
                                                                                    sum(1 for k_ in top if "VARSAYIM" in (bil[k_][0] + bil[k_][1] + k_))))


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-100s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("QR DOLABI v1 · %d parça · %d birim · katı denetimi: %s · %.0f sn" % (len(ps), len(BIRIMLER), "hepsi geçerli" if not gec else gec, time.time() - t0))
    bb = cq.Compound.makeCompound([dunya(p) for p in ps]).BoundingBox()
    print("ZARF (dünya): x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("DENETİM (qr_cad_v1)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    kontrol("zarf x %.0f–%.0f · y 0–%.0f · z %.0f–%.0f (SPEC)" % (X0, X0 + W, H, Z0, Z0 + D),
            abs(bb.xmin - X0) < 0.01 and abs(bb.xmax - X0 - W) < 0.01 and abs(bb.ymin) < 0.01 and abs(bb.ymax - H) < 0.01 and abs(bb.zmin - Z0) < 0.01 and abs(bb.zmax - Z0 - D) < 0.01)
    # birim zarfları
    for kod, _a in BIRIMLER:
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        print("   %-18s %3d parça · x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f" % (kod, len(q), min(v.xmin for v in q), max(v.xmax for v in q), min(v.ymin for v in q), max(v.ymax for v in q), min(v.zmin for v in q), max(v.zmax for v in q)))
    # sabit ölçüler
    def olc(ad):
        v = [dunya(p).BoundingBox() for p in ps if p["ad"] == ad][0]; return (round(v.xlen, 2), round(v.ylen, 2), round(v.zlen, 2)), v
    o, v = olc("robot_kontrol_kutusu_REZERV")
    kontrol("robot kontrol 475 × 423 × 268 · dünya x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f (SPEC x 4595–5070 · z 675–943)" % (v.xmin, v.xmax, v.ymin, v.ymax, v.zmin, v.zmax),
            o == (475.0, 423.0, 268.0) and abs(v.xmin - 4595) < 0.01 and abs(v.zmin - 675) < 0.01 and abs(v.ymin - 20) < 0.01)
    o, v = olc("ana_pano_400x350x250"); kontrol("ana pano 400 × 350 × 250 · y %.0f–%.0f (üst bölme %.0f–%.0f)" % (v.ymin, v.ymax, UST_BOLME[0], UST_BOLME[1]), o == (400.0, 350.0, 250.0) and v.ymin >= UST_BOLME[0] and v.ymax <= UST_BOLME[1])
    o, v = olc("ups_APC_BX500CI"); kontrol("UPS 115 × 185 × 213 · y %.0f–%.0f" % (v.ymin, v.ymax), o == (115.0, 185.0, 213.0) and v.ymin >= UST_BOLME[0] and v.ymax <= UST_BOLME[1])
    ko = [dunya(p).BoundingBox() for p in ps if p["ad"].endswith("_kasasi")]
    kontrol("12 göz · her biri 380 × 190 × 440", len(ko) == 12 and all((round(v.xlen, 2), round(v.ylen, 2), round(v.zlen, 2)) == (380.0, 190.0, 440.0) for v in ko))
    kontrol("göz sütunları x %s · z %.0f–%.0f · tabanlar %s" % (sorted({(round(v.xmin), round(v.xmax)) for v in ko}), ko[0].zmin, ko[0].zmax, sorted({round(v.ymin) for v in ko})),
            sorted({(round(v.xmin), round(v.xmax)) for v in ko}) == [(4600, 4980), (5010, 5390)] and abs(ko[0].zmin - 710) < 0.01 and abs(ko[0].zmax - 1150) < 0.01
            and sorted({round(v.ymin) for v in ko}) == [450, 650, 850, 1050, 1250, 1450])
    kontrol("alt bölme: kontrol kutusu üstü %.0f ≤ raf %.0f (pay %.0f) · servis ağzı %.0f > kutu 423 (çıkarılabilir)" % (KONTROL["y"][1], ALT_RAF[0], ALT_RAF[0] - KONTROL["y"][1], ALT_RAF[0] - TABAN[1]),
            KONTROL["y"][1] <= ALT_RAF[0] and ALT_RAF[0] - TABAN[1] > KONTROL["y"][1] - KONTROL["y"][0])
    kontrol("üst göz üstü %.0f + 10 ara = raf %.0f" % (GOZ_TABAN[-1] + GOZ_H, UST_RAF[0]), abs(GOZ_TABAN[-1] + GOZ_H + 10.0 - UST_RAF[0]) < 0.01)
    # ısı + havalandırma
    q_alt, q_ust = 150.0, 80.0          # W · VARSAYIM: robot kontrol kutusu kaybı · pano 40 + UPS 15 + kart/güç 25
    vd = FAN_M3H * 0.5 / 3600.0
    kontrol("havalandırma alt: %.0f W (VARSAYIM) / fan %.0f m³/h × 0,5 filtre → ΔT %.1f K ≤ 12 · giriş ızgarası %.0f cm²" % (q_alt, FAN_M3H, q_alt / (1.2 * 1005 * vd), IZGARA_ALAN["alt"] / 100.0),
            q_alt / (1.2 * 1005 * vd) <= 12.0)
    kontrol("havalandırma üst: %.0f W (VARSAYIM) → ΔT %.1f K ≤ 12 · giriş ızgarası %.0f cm²" % (q_ust, q_ust / (1.2 * 1005 * vd), IZGARA_ALAN["ust"] / 100.0), q_ust / (1.2 * 1005 * vd) <= 12.0)
    kontrol("göz ısıtıcısı: taban %.3f m² × h %.0f W/m²K (VARSAYIM) × ΔT %.0f K = %.0f W → ped %.0f W · 12 göz %.0f W (230 V %.1f A · UPS'e BAĞLANMAZ)"
            % (ISITICI_A, H_TABAN, ISITICI_T - ORTAM_T, ISITICI_A * H_TABAN * (ISITICI_T - ORTAM_T), ISITICI_W, 12 * ISITICI_W, 12 * ISITICI_W / 230.0),
            ISITICI_W >= ISITICI_A * H_TABAN * (ISITICI_T - ORTAM_T))
    kontrol("göz sayısı: pik 35 sipariş/sa × 10 dk bekleme = %.1f dolu göz → 12 göz = %.1f × pay (SERVİS_TESLİM v4 varsayımı)" % (35 * 10 / 60.0, 12 / (35 * 10 / 60.0)), 12 >= 35 * 10 / 60.0 * 1.5)
    print("  UYARI: müşteri paneli kotu %.0f–%.0f · tekerlekli sandalye erişimi (≤ 1220) SAĞLANMAZ — gözler 450–1650 arasını dolduruyor (Kemal'e sor)" % (1663, 1773))
    # erişim tablosu
    print("ERİŞİM (robot x %.0f · omuz y %.0f · ray ekseni z %.0f · robot yüzü z %.0f → yatay %.0f · pratik erişim %.0f · bilek = göz tabanı + %.0f VARSAYIM)"
          % (ROBOT_X, OMUZ, RZ, Z0, Z0 - RZ, ERISIM, BILEK_PAY))
    print("   satır sütun  sütun x  göz tabanı  bilek y   uzaklık   pay")
    et = erisim_tablosu()
    for r, c, gx, by, hy, d in et:
        print("   %4d %5d  %7.0f  %9.0f  %7.0f  %8.1f  %5.1f %s" % (r, c, gx, by, hy, d, ERISIM - d, "✓" if d <= ERISIM else "YETMEZ"))
    for c in range(2):
        yat = math.hypot(X0 + GOZ_X[c] + GOZ_W / 2.0 - ROBOT_X, Z0 - RZ)
        dk = math.sqrt(ERISIM ** 2 - yat ** 2)
        print("   sütun %d: yatay %.1f → dikey erişim bandı %.0f–%.0f" % (c, yat, OMUZ - dk, OMUZ + dk))
    kontrol("12 gözün bilek hedefi erişimde (en uzak %.1f ≤ %.0f)" % (max(e[5] for e in et), ERISIM), all(e[5] <= ERISIM for e in et))
    # hareketli gruplar AÇIK konumda (robot kapakları içeri-yukarı 90° · müşteri kapıları dışarı 90°) ↔ sabit parçalar
    sab = [p for p in ps if p["grup"] == "SABIT"]
    acik = []
    for g, (pv, ax, aci) in sorted(MENTESE.items()):
        for p in [q for q in ps if q["grup"] == g]:
            sh = dunya(p).rotate(cq.Vector(*pv), cq.Vector(*pv) + cq.Vector(*ax), aci)
            acik.append(dict(ad=p["ad"] + "@acik", wp=cq.Workplane(obj=sh), _sh=sh))
    ca = capraz(sab, acik)
    kk = [dunya(p).BoundingBox() for p in ps if p["ad"] == "goz_00_robot_kapagi"][0]
    ka = [q["_sh"].BoundingBox() for q in acik if q["ad"] == "goz_00_robot_kapagi@acik"][0]
    kontrol("hareketli %d grup AÇIK (kapak −90° içeri · kapı ±90° dışarı) ↔ sabit parçalar çakışma = 0 · açık kapak y %.0f–%.0f (göz tavanı %.0f) z %.0f–%.0f"
            % (len(MENTESE), ka.ymin, ka.ymax, GOZ_TABAN[0] + GOZ_H - 1.0, ka.zmin, ka.zmax), not ca, str(ca[:6]))
    kontrol("açık robot kapağı altında kalan ağız %.0f mm ≥ kutu 45 + çatal 60 (VARSAYIM)" % (ka.ymin - (GOZ_TABAN[0] + 5.5)), ka.ymin - (GOZ_TABAN[0] + 5.5) >= 105.0)
    # denetçi eki (27 Eyl): robot kapağı KAPANIRKEN gözdeki kutuya çarpmasın · kutu 320 × 42 × 320 (kutu_cad_v5: pizza kutusu 32 × 32 × 4,2 cm)
    #   göz arkasına (müşteri kapısı tarafı) 5 mm kala bırakılır (VARSAYIM) · kapak süpürme yarıçapı = mil ekseninden en uzak kapak köşesi
    KUTU_D, KUTU_H, KUTU_ARKA = 320.0, 42.0, 5.0
    R_sup = math.hypot(KAPAK_MIL_Y - 6.0, 5.0)                               # kapak y by+6…by+176, z 6–16 · mil (by+180, z 11)
    kz0 = GOZ_Z[1] - 1.0 - KUTU_ARKA - KUTU_D                               # kutunun robot tarafı yüzü (yerel z)
    d_kose = math.hypot(KAPAK_MIL_Y - (5.5 + KUTU_H), kz0 - 11.0)           # kutunun üst-ön kenarı ↔ mil ekseni
    z_min = 11.0 + math.sqrt(R_sup ** 2 - (KAPAK_MIL_Y - (5.5 + KUTU_H)) ** 2)
    kontrol("robot kapağı kapanırken kutuya çarpmaz: süpürme yarıçapı %.1f < kutu üst-ön kenarına %.1f (kutu yerel z %.0f–%.0f · dünya %.0f; kutu robot yüzü dünya z ≥ %.0f olmalı)"
            % (R_sup, d_kose, kz0, kz0 + KUTU_D, Z0 + kz0, Z0 + z_min), d_kose > R_sup + 5.0)
    print("  UYARI: göz tabanı DÜZ alüminyum plaka — robot çatalı (kutu_cad_v5 X_CATAL: 3 diş 26 × 8 × 430, gövde diş altından 14 mm aşağı iner) kutunun ALTINDA;"
          " kutu tabana bırakılınca dişler kutu ile taban arasında kalır, çatal çekilemez (E tepsisi çubuklu: dişler aralardan çıkar). Göz tabanına 3 diş yuvası"
          " ya da kaburga gerekir — tasarım kararı Kemal'de (bilek hedefi göz tabanı + 100 VARSAYIM buna göre değişebilir)")
    # kendi arasında çakışma
    t1 = time.time()
    cak = kendi_arasinda(ps)
    print("KENDİ ARASINDA (> 1 mm³): %s · %.0f sn" % ("TEMİZ" if not cak else cak[:20], time.time() - t1))
    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))
    # robot kablosu + zemin kanalı ile çapraz (ray_ek_cad_v1)
    if "hizli" not in arg:
        try:
            import ray_ek_cad_v1 as RE
            RE.kur()
            qs = [dict(ad=q["ad"], wp=q["wp"], _sh=RE.dunya(q)) for q in RE.PARCALAR if q["birim"] in ("ROBOT_KABLOSU", "ZEMIN_KANALI")]
            cc = capraz(ps, qs)
            kontrol("QR ↔ robot kablosu + kangal + zemin kanalı (ray_ek_cad_v1) çakışma = 0", not cc, str(cc[:6]))
        except ImportError as e:
            print("   (ray_ek_cad_v1 yok: çapraz denetim atlandı · %s)" % e)
    if "bom" in arg:
        bom_yaz()
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
