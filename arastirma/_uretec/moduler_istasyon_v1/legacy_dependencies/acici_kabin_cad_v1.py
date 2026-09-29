# -*- coding: utf-8 -*-
"""AUTOKITCH · A · AÇICI KABİNİ · CAD v1 (27 Eyl 2026 gece · denetçi düzeltmesi 28 Eyl 2026) — ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63.md §1 + §2.2)
Kemal: "fırının ön yüzü sınır yüzey, her şeyi o yüzeye getireceğiz … her istasyon kendi başına temiz bir kutu … robotun gireceği yerlerde boşluk …
dolap kalınlıklarını ver, üretilebilir … içeride havada kalan parça olmasın". Montajda v62'ye kadar A_KABIN yalnız KUTU'ydu (x 0–700 · y 788–1862 · z −830…0).

DENETÇİ DÜZELTMESİ (28 Eyl 2026 · rapor_A.md §0):
  2 menteşe kinematiği: servis kapağı GERÇEK menteşe ekseni etrafında döner (EMKA 1006-U1-PC sınıfı kaynaklı gizli pim menteşe · eksen dış yan yüzden 7,
    ön yüzden 7 = x 7 · z 72, VARSAYIM) · menteşe iki yarım + pim olarak modellendi · kapağın menteşe tarafındaki dönüşleri z 62'de biter (3 mm derz) ·
    açılma 0–90° 2,5° adımla taranır (çakışma, sol duvar payı, C paneli) · dükkân v14'te hat x 0 = sol iç duvar → makine duvardan ≥ 10 mm (VARSAYIM)
  3 dolap derzi: alt panel 791 → 788 (dolap çekmece önlerinin üstü 785 + derz 3 · fırın da 788'den başlar) · denetim komşu kenarı store_cad'den ÖLÇER
  4 robot ağzı: ışık perdesi (SICK miniTwin4, 14 mm, 240 mm, ağzın altında + üstünde, dikey ışınlar z ≈ 49,5) + perde kaydı · ışın alanı denetlenir
  6 dikmeler taban sacına TAM oturur (kaide_cad_v2 taban sacı x 1,5 · z −828,5…+39) · ön çerçevenin alt kısmı kaide ön profiline 4 mm ara lamayla bağlı
  7 çift profil birleşti: ön dikmeler + üst kayıt tek 30 × 50 × 2 (z +9…+59) · üst saca omega
  8 açıcı istisnası daraltıldı: yalnız topping_cad_v24 · yalnız AÇICI grubu · yalnız onyuz_ parçası · yalnız z ≥ +38,5'teki kesişim (v25'te istisna YOK)
  1 montaj kapısı: acici_kapisi() açıcı ↔ kabin çakışmalarını İSTİSNASIZ verir (montaj assert eder; v24'te 0 değil → A montaja alınmaz)
  9 kablo: arka sacta rakor YOK (kablolar TC enerji zinciri kanalı + tabla yuvasından C mekanizma bandına) · 10 arka sac DIŞARIDAN sökülür (havşa M6)
  5 C yan sacı teması: TC dis_yan_sol +39'a uzayınca (v25) ölçülür · 11 BOM: bağlantı elemanları, emniyet kontrolörü, derz silikonu eklendi

YERLEŞİM (DÜNYA, mm): A modülü x 0–700 · y 788 (dolap üstü) … 1862 (makine üstü) · z −830 (arka, SABİT) … +79 (ön düzlem = fırın ön yüzü = FT.ZS)
  GÖVDE (A_GOVDE) — kuru istasyon, PU yok, tek kat AISI 304 1,5:
    · sol yan sac x 0–1,5 · y 788–1860,5 · z −830…+59 · içte omega · üst sac x 0–700 · y 1860,5–1862 · z −830…+59 · içte omega (denetçi 7)
    · arka sac (SÖKÜLÜR, dışarıdan havşa M6) x 1,5–700 · y 788–1860,5 · z −830…−828,5 · delik YOK · içte omega
    · arka köşe dikmeleri 30 × 30 × 2 (z −828,5…−798,5) · ÖN DİKMELER 30 × 50 × 2 (z +9…+59) · y 893,5–1860,5 · kaide taban sacına TAM oturur
    · üst kuşak: arka + sol + sağ 30 × 30 × 2 · ön = ÜST KAYIT 30 × 50 × 2 (z +9…+59)
    · ön çerçeve 30 × 20 × 2 (z +39…+59): alt dikmeler (y 791–893,5) + alt kayıt + orta kayıt (perde alanında kesik) + perde kaydı (y 1200–1230)
      · alt kısım kaide ön profiline 3 ara lama (4 mm, z +35…+39) ile cıvatalı
    · SAĞ DUVAR = C'nin sol yan sacı (topping_cad dis_yan_sol) · TABAN = kaide_cad_v2 (KAIDE_A + taban sacı 892–893,5)
    · IŞIK PERDESİ: 2 × SICK miniTwin4 (240 mm) x 230–470 · alt y 834–857,8 · üst y 1163,2–1187 · z +42…+57 · ışın alanı ağzı tam örter
  ÖN YÜZ (A_ONYUZ) — tava panel 304 fırçalı 1,5, kenarlar 20 arkaya bükülü → z +59…+79 · derz 3 · dışarıdan yalnız düz yüzey + derz:
    · ALT PANEL (aletsiz sökülür, 4 yaylı tutucu, emniyet sensörü) x 0–698,5 · y 788–1107,5 · üstü açık çentik x 250–450 · y 960–1107,5
    · ÜST SERVİS KAPAĞI x 0–698,5 · y 1110,5–1859 · 2 gizli menteşe SOLDA (eksen x 7 · z 72) · bas-aç · emniyet sensörü · altı açık çentik 1110,5–1160
    · ROBOT AĞZI x 250–450 · y 960–1160 (200 × 200) · kenarlar bükülü
  AÇICI (kafa, koniler, kolon, Z kızağı) ve TABLA mekanizması TOPPING CAD'indedir (topping_cad_v24/v25, montajda x + 700, y + 892).
SÖZLEŞME: kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · ON_BIRIMLER · Z_ON · sozlesme() · KAPAK_EKSEN · kapak_pozu(aci) · acici_kapisi()
Çalıştır: python ob_calistir.py acici_kabin_cad_v1.py [hizli] [bom]   (hizli: TOPPING / dolap taramasını atlar)
"""
import csv, io, math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import qr_cad_v1 as QR                    # ortak kut / dunya / çakışma yardımcıları
import kaide_cad_v2 as KD                 # taban (KAIDE_A + taban sacı) · TOPPING süzgeçleri (v1_kalir, AKTARMA_TP10, V3_CIKAN) · tc_modul / tu_yolu

# ---------------------------------------------------------------- ÖLÇÜLER (SPEC v63) ----------------------------------------------------------------
X_A0, X_A1 = 0.0, 700.0                   # A modülü (pafta ATOSA TABLALI v7: X_A 0, W_A 700)
Y_DUZ, Y_MEK, H_MAK = KD.Y_DUZ, KD.Y_MEK, 1862.0      # 788 · 892 · 1862
Y_TABAN = KD.Y_MEK + KD.A_SAC             # 893,5 · kaide taban sacı üstü (dikmeler buna oturur)
Z_ARKA, Z_ON = -830.0, 79.0               # arka SABİT · ön düzlem (montaj sözleşmesi: = FT.ZS)
T = 1.5                                   # dış sac / tava panel AISI 304 fırçalı
T_OM = 1.0                                # omega takviye
KENAR = 20.0                              # tava panel kenar dönüşü
Z_PAN = (Z_ON - KENAR, Z_ON)              # +59 … +79
Z_YUZ = Z_ON - T                          # +77,5 · panel yüz sacının arka yüzü
Z_CER = (39.0, 59.0)                      # ön çerçeve (30 × 20 × 2 profil, derinlik 20)
DERZ = 3.0
Y_B_ON = 785.0                            # B çekmece önlerinin üst çizgisi (SPEC "dolap üstü 785/788" · store_cad_v8 ON_UST) — tam taramada store_cad'den ÖLÇÜLÜR
X_PAN = (X_A0, X_A1 - 1.5)                # 0 … 698,5 (C paneli 701,5'te başlar → derz 3)
Y_ALT = (Y_B_ON + DERZ, 1107.5)           # alt panel 788 … 1107,5 · KARAR (denetçi 3): SPEC 791 → 788 (dolap önü 785 + derz 3 = fırın altındaki çizgi; C paneli de 788'e inmeli)
Y_UST = (1110.5, H_MAK - DERZ)            # servis kapağı 1110,5 … 1859
AGIZ = dict(x=(250.0, 450.0), y=(960.0, 1160.0))      # robot ağzı (SPEC §2.2)
TOP = dict(x=(301.0, 399.0), y=(1007.0, 1087.0), z=(-170.0, 150.0))   # top Ø98 geçişi (SPEC) · z: robotun bıraktığı yol (+150 → −170)
KOSE = dict(b=30.0, t=2.0)                # arka köşe dikmesi / üst kuşak 30 × 30 × 2 (SPEC)
ON_DIKME = dict(b=30.0, d=50.0, t=2.0)    # ön dikmeler + üst kayıt 30 × 50 × 2 (denetçi 7: köşe dikmesi 30×30 + çerçeve 30×20 sırt sırta → tek profil)
CER = dict(b=30.0, t=2.0)                 # ön çerçeve 30 (yüz) × 20 (derinlik) × 2
XS_SOL, XS_SAG = (T, T + 30.0), (X_A1 - 30.0, X_A1)   # sol dikmeler 1,5–31,5 · sağ 670–700 (C yan sacına değer)
Z_ON_DIKME = (Z_CER[1] - ON_DIKME["d"], Z_CER[1])     # +9 … +59 (disk yolu z 0'ın 9 mm önü)
Z_KOSE_ARKA = (Z_ARKA + T, Z_ARKA + T + 30.0)          # −828,5 … −798,5
Y_SAC1 = H_MAK - T                        # 1860,5 · yan / arka sacın üstü = üst sacın altı
Y_KUSAK = (Y_SAC1 - 30.0, Y_SAC1)         # 1830,5 … 1860,5
Y_CER0 = 791.0                            # ön çerçeve alt kotu (alt dikmeler + alt kayıt; panel 788'den başlar, derz arkası boş)
Y_ORTA = (1094.0, 1124.0)                 # orta kayıt (derz 1107,5/1110,5 hizası)
PERDE = dict(x=(230.0, 470.0), z=(42.0, 57.0), alt_y=(834.0, 857.8), ust_y=(1163.2, 1187.0),      # SICK miniTwin4: kesit 15 × 23,8 (+ fiş 32) · boy = koruma alanı 240
             tut_alt=(Y_CER0 + 30.0, 834.0), tut_ust=(1187.0, 1200.0), tut_x=((250.0, 280.0), (420.0, 450.0)))   # O-fix tutucular (VARSAYIM 30 × 13 × 15)
Y_PERDE_KAYIT = (1200.0, 1230.0)          # üst perde çubuğunun kaydı (30 × 20 × 2)
X_ORTA_KES = (PERDE["x"][0] - 2.0, PERDE["x"][1] + 2.0)          # 228 · 472: orta kayıt ışın alanının dışında biter (ışın kesilmez)
ARA_LAMA = [dict(ad="sol", x=(10.0, 30.0), y=(800.0, 880.0)), dict(ad="sag", x=(672.0, 690.0), y=(800.0, 880.0)), dict(ad="orta", x=(335.0, 365.0), y=(793.0, 819.0))]
Z_LAMA = (KD.KZ[1], Z_CER[0])             # +35 … +39 · kaide ön profili ↔ ön çerçeve arası (4 mm)
DISK = dict(x=(180.0, 520.0), y=(1000.0, 1008.0), z=(-340.0, 0.0), kafa=60.0)   # çalışma diski Ø340 park konumunda, pimlerden 8 mm kaldırılmış
MENTESE = dict(pivot=(7.0, 72.0), r_pim=3.0, r_gov=5.0, h=60.0, seg=15.0, y0=(1240.0, 1700.0), aci=(-5.0, -25.0), r_kol=13.0)
#   gizli pim menteşe (EMKA 1006-U1-PC sınıfı): eksen x 7 · z 72 (dış yan yüzden 7, ön yüzden 7 — VARSAYIM, katalog föyü 4B-120) · pim Ø6 · göz Ø10 · boy 60
#   sabit yarım: alt + üst göz (15) + kol (−5°…−25°, r 5→13) + dikme önüne ayak · kapak yarımı: orta göz (30) + yüz sacına plaka · kol kapağın süpürmediği kamada
KAPAK_RAHAT = dict(x=12.0, z=62.0)        # menteşe tarafı: kapak dönüşleri x < 12'de z 62'de biter (sol dönüş boydan boya) → 3 mm derz · gerekli 2,7 (eksen 7/7, pay 0,5)
DUVAR_ARALIK = 10.0                       # VARSAYIM: makine sol iç duvardan ≥ 10 mm (dükkân v14: hat x 0 = duvar) · kapak köşesi açılırken x −2,9'a çıkar
MANDAL_Y = (1460.0, 1500.0)
SENSOR = dict(x=(635.0, 670.0), y=(1540.0, 1648.2), z=(28.5, 55.5))       # RSS 36: 27 × 108,2 × 35 (katalog) · sağ ön dikmenin iç yüzünde
HEDEF = dict(x=(640.0, 665.0), y=(1548.6, 1639.6), z=(55.5, Z_YUZ))       # RST 36-1: 91 × 22 × 25 (katalog) · kapağın arkasında, sensöre 0 mm (Sao 10)
SENSOR_ALT = dict(x=(635.0, 670.0), y=(900.0, 1008.2), z=(28.5, 55.5))    # 2. RSS 36: aletsiz sökülen alt panel de kilitli koruyucu
HEDEF_ALT = dict(x=(640.0, 665.0), y=(908.6, 999.6), z=(55.5, Z_YUZ))
KAPAK_EKSEN = dict(grup="SERVIS_KAPAGI", pivot=MENTESE["pivot"], eksen="y", aci_max=90.0,
                   not_="GERÇEK menteşe ekseni (x 7 · z 72, dikey) · kapak 0–90° bu eksen etrafında döner (acici_kabin_cad_v1 2,5° adımla taradı) · kapak_pozu(aci)")
RO = 7.93e-6                              # kg/mm³ AISI 304

PARCALAR = []
BIRIMLER = [
    ("A_GOVDE", "A AÇICI kabini gövdesi (kuru, PU yok) · x 0–700 · y 788–1862 · z −830…+59 · 304 1,5 sol yan + üst + sökülür arka (delik yok) · arka köşe dikmeleri 30 × 30 × 2 · "
                "ön dikmeler + üst kayıt 30 × 50 × 2 · ön çerçeve 30 × 20 × 2 (z +39…+59) · ışık perdesi (SICK miniTwin4 × 2) · 2 emniyet sensörü (RSS 36) · sağ duvar = C sol yan sacı · taban = kaide_cad_v2"),
    ("A_ONYUZ", "A ön yüz (z +59…+79, ön düzlem +79) · tava 20 304 fırçalı 1,5 · alt panel 788–1107,5 (sökülür) + üst servis kapağı 1110,5–1859 (gizli pim menteşe sol, eksen x 7 · z 72, bas-aç, emniyet sensörü) · "
                "ROBOT AĞZI x 250–450 · y 960–1160 (kenarlar bükülü) · derz 3"),
]
BIRIM_MODUL = {"A_GOVDE": "A", "A_ONYUZ": "A"}
ON_BIRIMLER = ("A_ONYUZ",)                # ön düzleme (+79) kadar gelen birim (montaj zarf denetimi z1 ≤ Z_ON)
MALZEME = {"sac": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "plastik": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6)}
kut = QR.kut
dunya = QR.dunya


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


# ---------------------------------------------------------------- profil / sac yardımcıları ----------------------------------------------------------------
def boru_y(x0, x1, z0, z1, y0, y1, t, kapak=0.0):
    """y boyunca kutu profil (uçları açık) · kapak > 0: alt ucuna kaynaklı kapak plakası (kesit içinde, kalınlık kapak)"""
    s = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))
    if kapak > 0.0:
        s = s.union(kut(x0 + t, x1 - t, y0, y0 + kapak, z0 + t, z1 - t))
    return s


def boru_x(y0, y1, z0, z1, x0, x1, t):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def boru_z(x0, x1, y0, y1, z0, z1, t):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 + 1.0))


def _lo(a, b):
    return (min(a, b), max(a, b))


def omega_pz(x0, x1, yc, zt, yon, h=15.0, t=T_OM):
    """x boyunca omega (şapka) takviye · flanşlar z = zt yüzeyine oturur, tepe yon (±1) yönünde h uzakta · genişlik 40 (10 + 20 + 10)"""
    za, zb = (zt, zt + yon * h)
    s = kut(x0, x1, yc - 20.0, yc - 10.0, *_lo(zt, zt + yon * t)).union(kut(x0, x1, yc + 10.0, yc + 20.0, *_lo(zt, zt + yon * t)))
    s = s.union(kut(x0, x1, yc - 10.0, yc - 10.0 + t, *_lo(za, zb))).union(kut(x0, x1, yc + 10.0 - t, yc + 10.0, *_lo(za, zb)))
    return s.union(kut(x0, x1, yc - 10.0, yc + 10.0, *_lo(zb, zb - yon * t)))


def omega_px(z0, z1, yc, xt, yon, h=15.0, t=T_OM):
    """z boyunca omega · flanşlar x = xt yüzeyine oturur"""
    xa, xb = xt, xt + yon * h
    s = kut(*_lo(xt, xt + yon * t), yc - 20.0, yc - 10.0, z0, z1).union(kut(*_lo(xt, xt + yon * t), yc + 10.0, yc + 20.0, z0, z1))
    s = s.union(kut(*_lo(xa, xb), yc - 10.0, yc - 10.0 + t, z0, z1)).union(kut(*_lo(xa, xb), yc + 10.0 - t, yc + 10.0, z0, z1))
    return s.union(kut(*_lo(xb, xb - yon * t), yc - 10.0, yc + 10.0, z0, z1))


def omega_py(z0, z1, xc, yt, yon, h=15.0, t=T_OM):
    """z boyunca omega · flanşlar y = yt yüzeyine (yatay sacın alt yüzü) oturur, tepe yon (±1) yönünde"""
    ya, yb = yt, yt + yon * h
    s = kut(xc - 20.0, xc - 10.0, *_lo(yt, yt + yon * t), z0, z1).union(kut(xc + 10.0, xc + 20.0, *_lo(yt, yt + yon * t), z0, z1))
    s = s.union(kut(xc - 10.0, xc - 10.0 + t, *_lo(ya, yb), z0, z1)).union(kut(xc + 10.0 - t, xc + 10.0, *_lo(ya, yb), z0, z1))
    return s.union(kut(xc - 10.0, xc + 10.0, *_lo(yb, yb - yon * t), z0, z1))


def tava(x0, x1, y0, y1, centik=None):
    """tava panel: yüz sacı z +77,5…+79 + 4 kenar dönüşü 20 (z +59…+77,5) · centik = (cx0, cx1, cy, 'ust'|'alt') robot ağzı çentiği, kenarları arkaya bükülü"""
    w = kut(x0, x1, y0, y1, Z_YUZ, Z_ON)
    for a, b, c, d in ((x0, x0 + T, y0, y1), (x1 - T, x1, y0, y1), (x0, x1, y0, y0 + T), (x0, x1, y1 - T, y1)):
        w = w.union(kut(a, b, c, d, Z_PAN[0], Z_YUZ))
    if centik:
        cx0, cx1, cy, taraf = centik
        if taraf == "ust":                                     # üstü açık çentik (alt panel): cy … y1
            w = w.cut(kut(cx0, cx1, cy, y1 + 1.0, Z_PAN[0] - 1.0, Z_ON + 1.0))
            fl = (kut(cx0 - T, cx0, cy, y1, Z_PAN[0], Z_YUZ), kut(cx1, cx1 + T, cy, y1, Z_PAN[0], Z_YUZ), kut(cx0 - T, cx1 + T, cy - T, cy, Z_PAN[0], Z_YUZ))
        else:                                                  # altı açık çentik (servis kapağı): y0 … cy
            w = w.cut(kut(cx0, cx1, y0 - 1.0, cy, Z_PAN[0] - 1.0, Z_ON + 1.0))
            fl = (kut(cx0 - T, cx0, y0, cy, Z_PAN[0], Z_YUZ), kut(cx1, cx1 + T, y0, cy, Z_PAN[0], Z_YUZ), kut(cx0 - T, cx1 + T, cy, cy + T, Z_PAN[0], Z_YUZ))
        for f in fl:
            w = w.union(f)
    return w


def poly_y(pts, y0, y1):
    """x-z düzleminde çokgen (pts: (x, z)), y0 … y1 boyunca"""
    return cq.Workplane("XZ").polyline(pts).close().extrude(-(y1 - y0)).translate((0, y0, 0))


def _pol(r, a_derece):
    px, pz = MENTESE["pivot"]
    a = math.radians(a_derece)
    return (px + r * math.cos(a), pz + r * math.sin(a))


def mentese(y0):
    """gizli pim menteşe (y0 … y0 + 60): (sabit yarım, kapak yarımı, pim) · pim deliği = pim çapı (temas, çakışma yok)"""
    px, pz = MENTESE["pivot"]; rp, rg, h, sg = MENTESE["r_pim"], MENTESE["r_gov"], MENTESE["h"], MENTESE["seg"]
    a1, a2 = MENTESE["aci"]; rk = MENTESE["r_kol"]
    def halka(ya, yb):
        return QR.sily(px, pz, rg, ya, yb).cut(QR.sily(px, pz, rp, ya - 1.0, yb + 1.0))
    kol = [_pol(rg, a1), _pol(rk, a1), _pol(rk, a2), _pol(rg, a2)]                      # göz → r 13 (kapak dönüşünün süpürmediği kama −5°…−25°)
    k1, k2 = _pol(rk, a1), _pol(rk, a2)
    govde = [k2, k1, (26.0, k1[1]), (26.0, KAPAK_RAHAT["z"]), (XS_SOL[1], KAPAK_RAHAT["z"]), (XS_SOL[1], Z_PAN[0]), (k2[0], Z_PAN[0])]   # r ≥ 13 · dikme önüne (z 59) ayak
    sabit = halka(y0, y0 + sg).union(halka(y0 + h - sg, y0 + h))
    sabit = sabit.union(poly_y(kol, y0, y0 + sg)).union(poly_y(kol, y0 + h - sg, y0 + h)).union(poly_y(govde, y0, y0 + h))
    sabit = sabit.cut(QR.sily(px, pz, rp, y0 - 1.0, y0 + h + 1.0))
    kanat = halka(y0 + sg, y0 + h - sg).union(kut(px, 34.0, y0 + sg, y0 + h - sg, Z_YUZ - 3.0, Z_YUZ)).cut(QR.sily(px, pz, rp, y0 - 1.0, y0 + h + 1.0))
    pim = QR.sily(px, pz, rp, y0, y0 + h)
    return sabit, kanat, pim


# ---------------------------------------------------------------- KUR ----------------------------------------------------------------
CER_PARCA = []            # ön çerçeve profilleri (BOM: parça sayısı + toplam boy)


def kur():
    PARCALAR[:] = []; CER_PARCA[:] = []
    G, O = "A_GOVDE", "A_ONYUZ"
    # ---- 1 · GÖVDE SACLARI ----
    ekle("a_govde_sol_yan", kut(X_A0, X_A0 + T, Y_DUZ, Y_SAC1, Z_ARKA, Z_PAN[0]), "sac", G,
         bom=("Sol yan sac AISI 304 1,5 (dış yüz fırçalı)", 1, "%.0f × %.1f · lazer" % (Z_PAN[0] - Z_ARKA, Y_SAC1 - Y_DUZ),
              "ÜRETİM · dolap üstüne (788) oturur, dikmelere + kuşağa M6 kaynak saplama + somun (içeriden; sol yan sabit, duvar tarafı) · ön kenarı alt panelin dönüşüne değer, servis kapağıyla arasında 3 mm menteşe derzi", "ÜRETİM"))
    ekle("a_govde_sol_yan_omega", omega_px(Z_KOSE_ARKA[1], Z_ON_DIKME[0], 1345.0, X_A0 + T, +1.0), "paslanmaz", G,
         bom=("Omega takviye 1,0 · 40 × 15", 3, "AISI 304 1,0 abkant · yan (z boyunca) + üst (z boyunca) + arka (x boyunca) · ön panellerdekiler ayrı kalem", "ÜRETİM · sacın iç yüzüne punta", "ÜRETİM"))
    ekle("a_govde_ust", kut(X_A0, X_A1, Y_SAC1, H_MAK, Z_ARKA, Z_PAN[0]), "sac", G,
         bom=("Üst sac AISI 304 1,5", 1, "%.0f × %.0f · lazer" % (X_A1 - X_A0, Z_PAN[0] - Z_ARKA), "ÜRETİM · kuşaklara + üst kayda oturur, sol yan sacı örter · C dis_tavan'ına x 700'de uç uca (derz silikonu, BOM ek)", "ÜRETİM"))
    ekle("a_govde_ust_omega", omega_py(Z_KOSE_ARKA[1], Z_ON_DIKME[0], (X_A0 + X_A1) / 2.0, Y_SAC1, -1.0), "paslanmaz", G)          # denetçi 7: 638 × 808 açıklık → orta omega
    ekle("a_govde_arka", kut(X_A0 + T, X_A1, Y_DUZ, Y_SAC1, Z_ARKA, Z_ARKA + T), "sac", G,
         bom=("Arka sac AISI 304 1,5 · SÖKÜLÜR (dışarıdan)", 1, "%.1f × %.1f · delik YOK (kablolar içeriden C'ye) · 14 havşa baskılı delik" % (X_A1 - X_A0 - T, Y_SAC1 - Y_DUZ),
              "ÜRETİM · denetçi 10: 14 × DIN 7991 M6 A2 havşa başlı vida DIŞARIDAN, dikme + kuşaklardaki M6 perçin somuna · baş arka yüzle aynı düzlem (−830 geçilmez) · makine duvardan çekilince sökülür (Z kızağı + pnömatiğe arkadan erişim)", "ÜRETİM"))
    ekle("a_govde_arka_omega", omega_pz(XS_SOL[1], XS_SAG[0], 1300.0, Z_ARKA + T, +1.0), "paslanmaz", G)
    # ---- 2 · DİKMELER + ÜST KUŞAK ----
    for ad, xs in (("arka_sol", XS_SOL), ("arka_sag", XS_SAG)):
        ekle("a_kose_dikmesi_" + ad, boru_y(xs[0], xs[1], Z_KOSE_ARKA[0], Z_KOSE_ARKA[1], Y_TABAN, Y_SAC1, KOSE["t"], kapak=3.0), "paslanmaz", G,
             bom=("Arka köşe dikmesi 30 × 30 × 2 AISI 304 kutu profil + 3 mm alt kapak", 2, "boy %.0f · kaide taban sacına 2 × M8 (kaide üst plakasında perçin somun)" % (Y_SAC1 - Y_TABAN),
                  "ÜRETİM · taban sacına tam oturur (x 1,5–700 · z −828,5…+39)", "ÜRETİM") if ad == "arka_sol" else None)
    for ad, xs in (("sol", XS_SOL), ("sag", XS_SAG)):
        ekle("onyuz_cerceve_%s_dikme" % ad, boru_y(xs[0], xs[1], Z_ON_DIKME[0], Z_ON_DIKME[1], Y_TABAN, Y_SAC1, ON_DIKME["t"], kapak=3.0), "paslanmaz", G,
             bom=("Ön dikme 30 × 50 × 2 AISI 304 dikdörtgen profil + 3 mm alt kapak", 2, "boy %.0f · z +9…+59 · alt: taban sacı (z +9…+39) + alt çerçeve dikmesi (z +39…+59) · 2 × M8" % (Y_SAC1 - Y_TABAN),
                  "ÜRETİM · denetçi 7: köşe dikmesi 30 × 30 + çerçeve 30 × 20 sırt sırta çift profil yerine TEK profil · sağ dikme C sol yan sacına 3 × M6 (C v25 +39)", "ÜRETİM") if ad == "sol" else None)
    ekle("onyuz_cerceve_ust_kayit", boru_x(Y_KUSAK[0], Y_KUSAK[1], Z_ON_DIKME[0], Z_ON_DIKME[1], XS_SOL[1], XS_SAG[0], ON_DIKME["t"]), "paslanmaz", G,
         bom=("Üst kayıt 30 × 50 × 2 AISI 304 dikdörtgen profil", 1, "boy %.0f · z +9…+59 (ön üst kuşak + çerçeve üst kaydı tek profil)" % (XS_SAG[0] - XS_SOL[1]), "ÜRETİM · dikmelere kaynak", "ÜRETİM"))
    for ad, w in (("arka", boru_x(Y_KUSAK[0], Y_KUSAK[1], Z_KOSE_ARKA[0], Z_KOSE_ARKA[1], XS_SOL[1], XS_SAG[0], KOSE["t"])),
                  ("sol", boru_z(XS_SOL[0], XS_SOL[1], Y_KUSAK[0], Y_KUSAK[1], Z_KOSE_ARKA[1], Z_ON_DIKME[0], KOSE["t"])),
                  ("sag", boru_z(XS_SAG[0], XS_SAG[1], Y_KUSAK[0], Y_KUSAK[1], Z_KOSE_ARKA[1], Z_ON_DIKME[0], KOSE["t"]))):
        ekle("a_ust_kusak_" + ad, w, "paslanmaz", G,
             bom=("Üst kuşak 30 × 30 × 2 AISI 304 kutu profil", 3, "arka %.0f · sol/sağ %.0f · dikmelere kaynak (kaynaklı üst çerçeve)" % (XS_SAG[0] - XS_SOL[1], Z_ON_DIKME[0] - Z_KOSE_ARKA[1]),
                  "ÜRETİM", "ÜRETİM") if ad == "arka" else None)
    # ---- 3 · ÖN ÇERÇEVE 30 × 20 × 2 (z +39…+59) ----
    zc = Z_CER
    cer = [("onyuz_cerceve_sol_alt_dikme", boru_y(XS_SOL[0], XS_SOL[1], zc[0], zc[1], Y_CER0, Y_TABAN, CER["t"]), Y_TABAN - Y_CER0),
           ("onyuz_cerceve_sag_alt_dikme", boru_y(XS_SAG[0], XS_SAG[1], zc[0], zc[1], Y_CER0, Y_TABAN, CER["t"]), Y_TABAN - Y_CER0),
           ("onyuz_cerceve_alt_kayit", boru_x(Y_CER0, Y_CER0 + 30.0, zc[0], zc[1], XS_SOL[1], XS_SAG[0], CER["t"]), XS_SAG[0] - XS_SOL[1]),
           ("onyuz_cerceve_orta_kayit_sol", boru_x(Y_ORTA[0], Y_ORTA[1], zc[0], zc[1], XS_SOL[1], X_ORTA_KES[0], CER["t"]), X_ORTA_KES[0] - XS_SOL[1]),
           ("onyuz_cerceve_orta_kayit_sag", boru_x(Y_ORTA[0], Y_ORTA[1], zc[0], zc[1], X_ORTA_KES[1], XS_SAG[0], CER["t"]), XS_SAG[0] - X_ORTA_KES[1]),
           ("onyuz_cerceve_perde_kayit", boru_x(Y_PERDE_KAYIT[0], Y_PERDE_KAYIT[1], zc[0], zc[1], XS_SOL[1], XS_SAG[0], CER["t"]), XS_SAG[0] - XS_SOL[1])]
    boy_c = sum(b for _a, _w, b in cer)
    for i, (ad, w, b) in enumerate(cer):
        ekle(ad, w, "paslanmaz", G,
             bom=("Ön çerçeve 30 × 20 × 2 AISI 304 dikdörtgen profil · kaynaklı", len(cer), "%d parça · toplam boy %.2f m · z +39…+59 (panel arkası) · orta kayıt ışın alanının dışında biter (x 228 / 472)" % (len(cer), boy_c / 1000.0),
                  "ÜRETİM · menteşe, mandal, emniyet sensörü, ışık perdesi ve panel tutucuları bu çerçeveye", "ÜRETİM") if i == 0 else None)
        CER_PARCA.append((ad, b))
    for i, l in enumerate(ARA_LAMA):
        ekle("onyuz_cerceve_ara_lama_" + l["ad"], kut(l["x"][0], l["x"][1], l["y"][0], l["y"][1], Z_LAMA[0], Z_LAMA[1]), "paslanmaz", G,
             bom=("Ara lama AISI 304 4 mm (ön çerçeve ↔ kaide ön profili)", len(ARA_LAMA), "20 × 80 / 18 × 80 / 30 × 26 · z +35…+39 · 2 × M6 A2 → kaide profilinde perçin somun",
                  "ÜRETİM · denetçi 6: ön çerçevenin alt kısmı (y 791–893,5) + alt kayıt artık kaideye cıvatalı (önce yalnız dikmeye kaynaktan asılı)", "ÜRETİM") if i == 0 else None)
    ekle("onyuz_emniyet_sensoru", kut(SENSOR["x"][0], SENSOR["x"][1], SENSOR["y"][0], SENSOR["y"][1], SENSOR["z"][0], SENSOR["z"][1]), "plastik", G,
         bom=("Emniyet sensörü (RFID, kodlu) · Schmersal RSS 36-SD-ST", 2, "27 × 108,2 × 35 · IP65/67/69 · Sao 10 / Sar 20 mm (products.schmersal.com)",
              "servis kapağı ya da alt panel açılınca robot + açıcı + tabla durur · sağ ön dikmenin iç yüzüne 2 × M4 · emniyet kontrolörüne (BOM ek)", "SATIN ALMA"))
    ekle("onyuz_emniyet_sensoru_alt", kut(SENSOR_ALT["x"][0], SENSOR_ALT["x"][1], SENSOR_ALT["y"][0], SENSOR_ALT["y"][1], SENSOR_ALT["z"][0], SENSOR_ALT["z"][1]), "plastik", G)
    # ---- 4 · IŞIK PERDESİ (robot ağzı koruması · denetçi 4) ----
    px0, px1 = PERDE["x"]; pz0, pz1 = PERDE["z"]
    ekle("onyuz_isik_perdesi_alt", kut(px0, px1, PERDE["alt_y"][0], PERDE["alt_y"][1], pz0, pz1), "plastik", G,
         bom=("Güvenlik ışık perdesi · SICK miniTwin4 · 14 mm · koruma alanı 240 mm (çift = 2 twin stick)", 2,
              "C4MT-02414ABB03… (sipariş kodu soneki VARSAYIM) · kesit 15 × 23,8 (fişle 32) · boy = koruma alanı · Type 4 / SIL 3 / PL e · tepki ≤ 14 ms · IP65 · 2 × O-fix tutucu dahil (datasheet C4MT-03014ABB03DB0)",
              "ağzın altında (y 834–857,8) + üstünde (1163,2–1187) · dikey ışınlar z ≈ 49,5 · robot girişinde MUTING (robot güvenli konum sinyali + açıcı/tabla STO) · ISO 13855: S = 2000 × T ≤ ~220 → toplam durma ≤ 110 ms", "SATIN ALMA"))
    ekle("onyuz_isik_perdesi_ust", kut(px0, px1, PERDE["ust_y"][0], PERDE["ust_y"][1], pz0, pz1), "plastik", G)
    for j, (xa, xb) in enumerate(PERDE["tut_x"]):
        ekle("onyuz_isik_perdesi_tutucu_alt_%d" % j, kut(xa, xb, PERDE["tut_alt"][0], PERDE["tut_alt"][1], pz0, pz1), "paslanmaz", G)
        ekle("onyuz_isik_perdesi_tutucu_ust_%d" % j, kut(xa, xb, PERDE["tut_ust"][0], PERDE["tut_ust"][1], pz0, pz1), "paslanmaz", G)
    # ---- 5 · ÖN YÜZ: tava paneller ----
    ekle("onyuz_alt_panel", tava(X_PAN[0], X_PAN[1], Y_ALT[0], Y_ALT[1], (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], "ust")), "sac", O, grup="ALT_PANEL",
         bom=("Alt panel · tava 20 · AISI 304 fırçalı 1,5 · SÖKÜLÜR", 1, "%.1f × %.1f · üstü açık robot ağzı çentiği %.0f × %.1f, kenarları 20 arkaya bükülü"
              % (X_PAN[1] - X_PAN[0], Y_ALT[1] - Y_ALT[0], AGIZ["x"][1] - AGIZ["x"][0], Y_ALT[1] - AGIZ["y"][0]),
              "ÜRETİM (lazer + abkant, köşeler kaynak + taşlama) · 788'den başlar (dolap önü 785 + derz 3, denetçi 3) · kaide bandını da örter · aletsiz çıkar (4 yaylı tutucu, emniyet sensörlü) → disk günlük buradan çıkar", "ÜRETİM"))
    ekle("onyuz_alt_panel_omega", omega_pz(X_PAN[0] + 2.0 * T, X_PAN[1] - 2.0 * T, 850.0, Z_YUZ, -1.0), "paslanmaz", O, grup="ALT_PANEL",
         bom=("Panel omegası 1,0 · 40 × 15", 3, "AISI 304 1,0 · panel > 600 (SPEC) · alt panel 1 + servis kapağı 2", "ÜRETİM · yüz sacının arkasına punta (dışta iz yok)", "ÜRETİM"))
    for i, (x, y) in enumerate(((6.0, 796.0), (X_PAN[1] - 26.0, 796.0), (6.0, 1082.0), (X_PAN[1] - 26.0, 1082.0))):
        ekle("onyuz_alt_panel_tutucu_%d" % i, kut(x, x + 20.0, y, y + 20.0, Z_PAN[0], Z_YUZ), "plastik", O,
             bom=("Yaylı bilyeli panel tutucu (ball stud + yuva)", 4, "ör. Southco ball-stud serisi — parça no + ölçü VARSAYIM (20 × 20 × 18,5)",
                  "alt panel aletsiz çekilip çıkar; dışarıdan görünmez", "SATIN ALMA") if i == 0 else None)
    kapak = tava(X_PAN[0], X_PAN[1], Y_UST[0], Y_UST[1], (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][1], "alt"))
    kapak = kapak.cut(kut(X_PAN[0] - 1.0, KAPAK_RAHAT["x"], Y_UST[0] - 1.0, Y_UST[1] + 1.0, Z_PAN[0] - 1.0, KAPAK_RAHAT["z"]))   # menteşe tarafı 3 mm derz (denetçi 2)
    ekle("onyuz_servis_kapagi", kapak, "sac", O, grup="SERVIS_KAPAGI",
         bom=("Üst servis kapağı · tava 20 · AISI 304 fırçalı 1,5", 1, "%.1f × %.1f · altı açık robot ağzı çentiği %.0f × %.1f, kenarları 20 arkaya bükülü · menteşe tarafında dönüşler 17 (z +62)"
              % (X_PAN[1] - X_PAN[0], Y_UST[1] - Y_UST[0], AGIZ["x"][1] - AGIZ["x"][0], AGIZ["y"][1] - Y_UST[0]),
              "ÜRETİM · gizli pim menteşe SOLDA (eksen x 7 · z 72), bas-aç sağda · menteşe tarafında sol yan sac + ön dikmeyle 3 mm derz (yalnız soldan, duvar tarafından görünür)", "ÜRETİM"))
    for i, yc in enumerate((1360.0, 1620.0)):
        ekle("onyuz_servis_kapagi_omega_%d" % i, omega_pz(35.0, 630.0, yc, Z_YUZ, -1.0), "paslanmaz", O, grup="SERVIS_KAPAGI")
    for i, y in enumerate(MENTESE["y0"]):
        sabit, kanat, pim = mentese(y)
        ekle("onyuz_servis_kapagi_mentese_%d_sabit" % i, sabit, "paslanmaz", O,
             bom=("Gizli menteşe 90° · EMKA 1006-U1-PC (kaynaklı, AISI 304, aletsiz sökülür, dışarıdan sökülemez)", 2,
                  "katalog föyü 4B-120 · MODEL: eksen x 7 · z 72 (dış yan yüzden 7, ön yüzden 7) · pim Ø6 · göz Ø10 · boy 60 · sabit yarım dikme önüne, kapak yarımı yüz sacına kaynak — geometri VARSAYIM",
                  "kapak ~{KAPAK_KG} kg · eksen föyde farklıysa MENTESE['pivot'] değişir, tarama tekrarlanır (gerekli menteşe derzi tablosu rapor_A §0) · emka.com", "SATIN ALMA") if i == 0 else None)
        ekle("onyuz_servis_kapagi_mentese_%d_kanat" % i, kanat, "paslanmaz", O, grup="SERVIS_KAPAGI")
        ekle("onyuz_servis_kapagi_mentese_%d_pim" % i, pim, "paslanmaz", O)
    ekle("onyuz_servis_kapagi_basac_mandal", kut(XS_SAG[0] + 2.5, XS_SAG[1] - 3.5, MANDAL_Y[0], MANDAL_Y[1], Z_PAN[0], Z_YUZ), "plastik", O,
         bom=("Bas-aç mandal (push-to-open, gizli) · Southco E4 touch latch", 1, "gizli montaj · parça no + ölçü VARSAYIM (24 × 40 × 18,5)", "kapak dışarıdan kulpsuz: basınca açılır", "SATIN ALMA"))
    ekle("onyuz_emniyet_hedefi", kut(HEDEF["x"][0], HEDEF["x"][1], HEDEF["y"][0], HEDEF["y"][1], HEDEF["z"][0], HEDEF["z"][1]), "plastik", O, grup="SERVIS_KAPAGI",
         bom=("Emniyet sensörü hedefi · Schmersal RST 36-1", 2, "91 × 22 × 25 · kodlu RFID hedef (tutma mıknatısı ~18 N)", "kapağın / alt panelin arka yüzüne 2 × M4 kaynak saplama", "SATIN ALMA"))
    ekle("onyuz_emniyet_hedefi_alt", kut(HEDEF_ALT["x"][0], HEDEF_ALT["x"][1], HEDEF_ALT["y"][0], HEDEF_ALT["y"][1], HEDEF_ALT["z"][0], HEDEF_ALT["z"][1]), "plastik", O, grup="ALT_PANEL")
    # kapak kütlesi → menteşe BOM notu
    kg = sum(dunya(p).Volume() * RO for p in PARCALAR if p["grup"] == "SERVIS_KAPAGI" and p["mal"] != "plastik")
    for p in PARCALAR:
        if p["bom"] and "{KAPAK_KG}" in p["bom"][3]:
            b = list(p["bom"]); b[3] = b[3].replace("{KAPAK_KG}", "%.1f" % kg); p["bom"] = tuple(b)
    return PARCALAR


def kapak_pozu(aci):
    """servis kapağı grubunun açık konumu (derece, 0–90): dünya dönüşümü (eksen noktası, eksen yönü, açı) — cq.Shape.rotate(a, b, aci) ile uygulanır"""
    px, pz = MENTESE["pivot"]
    return (cq.Vector(px, 0.0, pz), cq.Vector(px, 1.0, pz), -float(aci))


def sozlesme():
    """montaj için ölçü sözleşmesi (assert edilebilir)"""
    return dict(Z_ON=Z_ON, Z_ARKA=Z_ARKA, X=(X_A0, X_A1), Y=(Y_DUZ, H_MAK), PANEL_X=X_PAN, ALT_PANEL_Y=Y_ALT, SERVIS_KAPAGI_Y=Y_UST, DERZ=DERZ, B_ON_UST=Y_B_ON,
                AGIZ=AGIZ, TOP=TOP, Z_CERCEVE=Z_CER, Z_PANEL=Z_PAN, ACICI_ON_SINIR=Z_CER[0], KAPAK_EKSEN=KAPAK_EKSEN, MENTESE=MENTESE,
                ISIK_PERDESI=dict(x=PERDE["x"], y=(PERDE["alt_y"][1], PERDE["ust_y"][0]), z=PERDE["z"]), DUVAR_ARALIK=DUVAR_ARALIK)


# ---------------------------------------------------------------- DENETİM ----------------------------------------------------------------
V1_TASI = {"sogutma_grubu": (790.0, 0.0, 0.0), "pano_kutusu": (80.0, 0.0, 0.0), "ups": (140.0, 0.0, 0.0), "din_ray_ups": (140.0, 0.0, 0.0),
           "guc_kaynagi": (1196.0, 0.0, 0.0), "fire_silecegi": (520.0, 0.0, 0.0)}           # hat_montaj_v62 L264 ile aynı
for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
KAPAK_TC = ("on_kapak", "on_kapak_pu", "kapak_contasi")                                    # montaj v62 L1371
ACICI_P = ("acici_yatagi_", "acici_reduktoru_", "acici_motoru_", "acici_askisi_", "acici_kafa_plakasi")   # montaj v62 L744 (kafa, 60/90 mm iner-kalkar)
KONI_P = ("acici_konisi_", "acici_mili_")
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_", "calisma_diski", "disk_pimi_")
ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi", "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_",
           "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi", "kilit_burcu_")
KAFA_KALKIS = (60.0, 90.0)                                                                  # animasyon: boşta +60, top girerken +90 (montaj v62 L1263, L1003)
X_KAYMA = (-70.0, 0.0, 175.0, 350.0, 525.0, 700.0, 900.0)                                   # tabla + araba: sol sert durak (plaka tampona) … park … A→C geçişi
TC_ISTISNA_SURUM = "topping_cad_v24"                                                        # denetçi 8: istisna YALNIZ bu sürümde (C ajanı v25'te kafayı +39'un arkasına alır)


def grup_tc(ad):
    if ad in ("tabla_home_sensoru", "tabla_home_bayragi"): return "ARABA"
    if ad.startswith(ACICI_P) or ad.startswith(KONI_P): return "ACICI"
    if ad.startswith(TABLA_P) and ad != "tabla_bos_sensoru": return "TABLA"
    if ad.startswith(ARABA_P): return "ARABA"
    return "SABIT"


def topping_setleri():
    """TC (montajdaki gibi x + 700, y + 892, V1_TASI) + TU (x + 700, y − 168) · dinamik: kafa +60/+90, tabla + araba x kaymaları"""
    TC, tc_ad = KD.tc_modul()
    TC.PARCALAR[:] = []; TC.modul()
    tc = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom") and KD.v1_kalir(p["ad"]) and p["ad"] not in KD.AKTARMA_TP10 and p["ad"] not in KAPAK_TC]
    S, D = [], []
    for p in tc:
        d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_A1 + d[0], Y_MEK + d[1], d[2]))
        g = grup_tc(p["ad"])
        S.append(("TC:" + p["ad"], sh, g))
        if g == "ACICI":
            for dy in KAFA_KALKIS:
                D.append(("TC(kafa +%.0f):%s" % (dy, p["ad"]), sh.translate(cq.Vector(0.0, dy, 0.0)), g))
        elif g in ("TABLA", "ARABA"):
            for dx in X_KAYMA:
                if dx != 0.0:
                    D.append(("TC(tabla %+.0f):%s" % (dx, p["ad"]), sh.translate(cq.Vector(dx, 0.0, 0.0)), g))
    import importlib.util as ilu
    tu_yol, tu_ad = KD.tu_yolu()
    sp = ilu.spec_from_file_location("TU_AK", tu_yol)
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    for q in TU.P:
        if q["ad"].startswith(KD.V3_CIKAN): continue
        S.append(("TU:" + q["ad"], q["sh"].translate(cq.Vector(X_A1, -168.0, 0.0)), "SABIT"))
    return S, D, tc_ad, tu_ad


def capraz(ps, T_, esik=1.0):
    """kabin parçaları × (ad, şekil, grup) · dönüş (hacim, kabin parçası, diğer, grup, diğerinin en ön z'si, KESİŞİMİN en arka z'si)"""
    out = []
    K = [(p["ad"], dunya(p)) for p in ps]; K = [(a, s, s.BoundingBox()) for a, s in K]
    for c, sc, g in T_:
        B = sc.BoundingBox()
        if B.xmin > X_A1 + 5.0: continue
        for a, sa, A in K:
            if QR._bbk(A, B):
                ix = sa.intersect(sc)
                v = ix.Volume()
                if v > esik: out.append((round(v, 1), a, c, g, B.zmax, ix.BoundingBox().zmin))
    return out


def c_istisnasi(c, tc_ad):
    """denetçi 8 · C ajanının açıcı kafası (+39'u geçen kısım) için DAR istisna: yalnız topping_cad_v24 · yalnız AÇICI grubu · yalnız onyuz_ parçası · yalnız z ≥ +38,5'teki kesişim"""
    return tc_ad == TC_ISTISNA_SURUM and c[3] == "ACICI" and c[1].startswith("onyuz_") and c[5] >= Z_CER[0] - 0.5


def acici_kapisi(ps=None):
    """MONTAJ KAPISI (denetçi 1): açıcı kafası (inik + 60 / 90 kalkık) ↔ kabin çakışmaları İSTİSNASIZ · montaj: assert not AK.acici_kapisi()[1]"""
    ps = ps or kur()
    S, D, tc_ad, _tu = topping_setleri()
    return tc_ad, capraz(ps, [x for x in S + D if x[2] == "ACICI"])


def mesafe(a, b):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped)
    return d.Value() if d.IsDone() else -1.0


BOM_KLASOR = os.path.join(KOK, "arastirma", "3_ACICI_KABIN_v1")
BOM_EK = [   # modelde gövdesi olmayan kalemler (denetçi 11) · (kalem, adet, tanım, not, tür)
    ("Kaynak saplama M6 × 16 A2 + somun DIN 934 A2", 14, "sol yan sac ↔ dikmeler + sol kuşak (içeriden)", "ÜRETİM sırasında sacın iç yüzüne saplama kaynağı", "SATIN ALMA"),
    ("Havşa başlı vida DIN 7991 M6 × 12 A2 + perçin somun M6 A2", 14, "arka sac ↔ arka dikmeler + arka kuşak · DIŞARIDAN (denetçi 10)", "havşa baskılı delik: baş arka yüzle aynı düzlem (−830 geçilmez)", "SATIN ALMA"),
    ("Cıvata DIN 912 M8 × 16 A2 + perçin somun M8 A2 (sıkma 3–6)", 8, "4 dikme × 2 · dikme alt kapağı ↔ taban sacı 1,5 + kaide üst plakası 4", "perçin somun kaide üst plakasına", "SATIN ALMA"),
    ("Cıvata DIN 912 M6 × 20 A2 + perçin somun M6 A2", 6, "3 ara lama × 2 · ön çerçeve ↔ kaide ön profili", "perçin somun kaide ön profiline", "SATIN ALMA"),
    ("Cıvata DIN 912 M6 × 16 A2 + somun", 6, "sağ ön dikme (3) + arka sağ dikme (3) ↔ C sol yan sacı · LEGO bağlantı", "C dis_yan_sol +39'a uzayınca (topping_cad_v25) delikler C'de", "SATIN ALMA"),
    ("Emniyet kontrolörü · SICK Flexi Soft FX3-CPU000000 + FX3-XTIO84002 (VARSAYIM kodlar, doğrulanacak)", 1,
     "2 × RSS 36 (seri, 2 kanal) + miniTwin4 OSSD + robot güvenli konum sinyaliyle MUTING + açıcı/tabla STO", "PANODA (S/QR modülü) — A kabininde değil", "SATIN ALMA"),
    ("Gıdaya uygun silikon derz dolgusu (ör. DOWSIL 732, FDA — VARSAYIM ürün)", 1, "A üst sacı ↔ C dis_tavan derzi x 700 · 0,89 m · + sol yan sac ↔ duvar derzi montajda", "üst yüzde su / kırıntı girmesin", "SATIN ALMA"),
]


def bom_yaz(klasor, ps):
    """qr_cad_v1.bom_yaz ile aynı biçim + BOM_EK (gövdesiz kalemler)"""
    os.makedirs(klasor, exist_ok=True)
    satir = []
    for p in ps:
        if p["bom"]:
            kalem, adet, tanim, not_, tur = p["bom"]
            satir.append((p["ad"], p["birim"], kalem, adet, tanim, not_, tur))
        else:
            bb = dunya(p).BoundingBox()
            satir.append((p["ad"], p["birim"], p["ad"].replace("_", " "), 0, "", "aynı kalemin eşi ya da alt parça · zarf %.0f × %.0f × %.0f" % (bb.xlen, bb.ylen, bb.zlen), "ALT"))
    for kalem, adet, tanim, not_, tur in BOM_EK:
        satir.append(("(gövdesiz)", "A_GOVDE", kalem, adet, tanim, not_, tur))
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
    DEN.append((ad, bool(sart), deger)); print("  %-128s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


def kutu(x0, x1, y0, y1, z0, z1):
    return kut(x0, x1, y0, y1, z0, z1).val()


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    kd = KD.kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("AÇICI KABİNİ v1 (denetçi düzeltmesi) · %d parça (%s) · kaide_cad_v2 %d parça · %.0f sn" % (len(ps), " · ".join("%s %d" % (b, sum(1 for p in ps if p["birim"] == b)) for b, _a in BIRIMLER), len(kd), time.time() - t0))
    print("DENETİM (acici_kabin_cad_v1)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    bb = {p["ad"]: dunya(p).BoundingBox() for p in ps}
    P_ = {p["ad"]: p for p in ps}
    # ---- 1 · zarf + ön düzlem ----
    X0_, X1_ = min(b.xmin for b in bb.values()), max(b.xmax for b in bb.values())
    Y0_, Y1_ = min(b.ymin for b in bb.values()), max(b.ymax for b in bb.values())
    Z0_, Z1_ = min(b.zmin for b in bb.values()), max(b.zmax for b in bb.values())
    kontrol("zarf x %.1f–%.1f · y %.1f–%.1f · z %.1f…%.1f = A modülü x 0–700 · y 788–1862 · z −830…+79 (arka SABİT, ön düzlem +79)" % (X0_, X1_, Y0_, Y1_, Z0_, Z1_),
            abs(X0_ - X_A0) < 0.01 and abs(X1_ - X_A1) < 0.01 and abs(Y0_ - Y_DUZ) < 0.01 and abs(Y1_ - H_MAK) < 0.01 and abs(Z0_ - Z_ARKA) < 0.01 and abs(Z1_ - Z_ON) < 0.01)
    onl = [a for a in bb if a in ("onyuz_alt_panel", "onyuz_servis_kapagi")]
    kontrol("ön paneller (%s) dış yüzü z = +%.1f · arka ucu +%.1f (tava 20) → ön düzlem +79,0 · kenar dönüşü 20" % (", ".join(onl), max(bb[a].zmax for a in onl), min(bb[a].zmin for a in onl)),
            len(onl) == 2 and all(abs(bb[a].zmax - Z_ON) < 0.01 and abs(bb[a].zmin - Z_PAN[0]) < 0.01 for a in onl))
    gz = max(bb[p["ad"]].zmax for p in ps if p["birim"] == "A_GOVDE")
    on59 = [a for a in bb if bb[a].zmax > Z_PAN[0] + 0.01 and not a.startswith("onyuz_")]
    kontrol("gövde (A_GOVDE) en ön z %.1f ≤ +59 (tava panelin arkası) · z > +59 olan parçaların hepsi onyuz_ (%s) · ön dikmeler z %.0f…%.0f · çerçeve %.0f…%.0f"
            % (gz, "hepsi" if not on59 else on59, Z_ON_DIKME[0], Z_ON_DIKME[1], Z_CER[0], Z_CER[1]), gz <= Z_PAN[0] + 0.01 and not on59)
    # ---- 2 · kalınlık tablosu (katılardan) ----
    kal = [("sol yan sac (x)", bb["a_govde_sol_yan"].xlen, T), ("üst sac (y)", bb["a_govde_ust"].ylen, T), ("arka sac (z)", bb["a_govde_arka"].zlen, T),
           ("alt panel derinliği (tava kenarı)", bb["onyuz_alt_panel"].zlen, KENAR), ("servis kapağı derinliği", bb["onyuz_servis_kapagi"].zlen, KENAR),
           ("ön çerçeve derinliği (alt dikme)", bb["onyuz_cerceve_sol_alt_dikme"].zlen, Z_CER[1] - Z_CER[0]), ("arka köşe dikmesi (x)", bb["a_kose_dikmesi_arka_sol"].xlen, KOSE["b"]),
           ("ön dikme 30 × 50 (x)", bb["onyuz_cerceve_sol_dikme"].xlen, ON_DIKME["b"]), ("ön dikme 30 × 50 (z)", bb["onyuz_cerceve_sol_dikme"].zlen, ON_DIKME["d"]),
           ("üst kayıt 30 × 50 (z)", bb["onyuz_cerceve_ust_kayit"].zlen, ON_DIKME["d"])]
    _yz = dunya(P_["onyuz_servis_kapagi"]).intersect(kutu(100.0, 200.0, 1500.0, 1510.0, Z_PAN[0] - 1.0, Z_ON + 1.0))
    kal.append(("servis kapağı yüz sacı (ölçülen, x 100–200 · y 1500–1510 kesiti)", _yz.Volume() / (100.0 * 10.0), T))
    _om = dunya(P_["onyuz_servis_kapagi_omega_0"]).intersect(kutu(100.0, 101.0, 1341.0, 1349.0, Z_PAN[0], Z_YUZ))   # flanş kesiti 1 × 8
    kal.append(("omega flanşı (ölçülen, 1 × 8 kesit)", _om.Volume() / 8.0, T_OM))
    _ls = dunya(P_["onyuz_servis_kapagi"]).intersect(kutu(-1.0, 3.0, 1500.0, 1510.0, Z_PAN[0] - 1.0, Z_ON + 1.0)).BoundingBox()
    kal.append(("servis kapağı sol dönüşü (menteşe tarafı, ölçülen)", _ls.zlen, Z_ON - KAPAK_RAHAT["z"]))
    for ad_, v_, b_ in kal:
        print("     KALINLIK · %-70s %.2f (hedef %.2f)" % (ad_, v_, b_))
    kontrol("kalınlıklar (%d ölçü): dış sac 1,5 · tava kenarı 20 · çerçeve 20 · arka dikme 30 · ön dikme + üst kayıt 30 × 50 · yüz sacı 1,5 (ölçülen) · omega 1,0 (ölçülen) · menteşe tarafı dönüş 17"
            % len(kal), all(abs(v_ - b_) < 0.05 for ad_, v_, b_ in kal))
    # ---- 3 · derzler + ön yüz ızgarası ----
    ap, sk = bb["onyuz_alt_panel"], bb["onyuz_servis_kapagi"]
    dz = [("dolap çekmece önü üstü %.0f (SPEC) → alt panel" % Y_B_ON, ap.ymin - Y_B_ON), ("alt panel → servis kapağı (1107,5/1110,5)", sk.ymin - ap.ymax),
          ("servis kapağı → makine üstü 1862", H_MAK - sk.ymax), ("A paneli sağ ucu → C paneli 701,5", 701.5 - max(ap.xmax, sk.xmax)),
          ("menteşe tarafı: sol yan sac / ön dikme önü +59 → kapak dönüşü", KAPAK_RAHAT["z"] - Z_PAN[0])]
    kontrol("derzler 3,0: " + " · ".join("%s %.1f" % d for d in dz), all(abs(v - DERZ) < 0.01 for _a, v in dz))
    yuz = 0.0
    for a in onl:
        yuz += dunya(P_[a]).intersect(kutu(X_A0 - 1.0, X_A1 + 1.0, Y_DUZ, H_MAK, Z_YUZ, Z_ON)).Volume() / T
    bek = (X_PAN[1] - X_PAN[0]) * ((Y_ALT[1] - Y_ALT[0]) + (Y_UST[1] - Y_UST[0])) - (AGIZ["x"][1] - AGIZ["x"][0]) * ((Y_ALT[1] - AGIZ["y"][0]) + (AGIZ["y"][1] - Y_UST[0]))
    kontrol("ön yüz ızgarası: düz yüz alanı %.4f m² = panel alanı − robot ağzı (%.4f m²) · ağız + derz dışında delik / çıkıntı yok" % (yuz / 1e6, bek / 1e6), abs(yuz - bek) < 1.0)
    # ---- 4 · robot ağzı + top yolu + ışık perdesi + disk ----
    tun = kutu(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], -200.0, Z_ON + 50.0)
    top = kutu(TOP["x"][0], TOP["x"][1], TOP["y"][0], TOP["y"][1], TOP["z"][0], TOP["z"][1])
    t_c = [(round(dunya(p).intersect(tun).Volume(), 1), p["ad"]) for p in ps if QR._bbk(bb[p["ad"]], tun.BoundingBox())]
    t_c = [x for x in t_c if x[0] > 0.0]
    kontrol("ROBOT AĞZI x %.0f–%.0f · y %.0f–%.0f (%.0f × %.0f) temiz: kabin parçası girmez (z −200…+129 tüneli)" % (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1],
            AGIZ["x"][1] - AGIZ["x"][0], AGIZ["y"][1] - AGIZ["y"][0]), not t_c, str(t_c[:4]))
    kont = []
    for ad_, k_ in (("sol", kutu(AGIZ["x"][0] - T, AGIZ["x"][0], AGIZ["y"][0], AGIZ["y"][1], Z_PAN[0], Z_YUZ)), ("sag", kutu(AGIZ["x"][1], AGIZ["x"][1] + T, AGIZ["y"][0], AGIZ["y"][1], Z_PAN[0], Z_YUZ)),
                    ("alt", kutu(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0] - T, AGIZ["y"][0], Z_PAN[0], Z_YUZ)), ("ust", kutu(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][1], AGIZ["y"][1] + T, Z_PAN[0], Z_YUZ))):
        v_ = sum(dunya(P_[a]).intersect(k_).Volume() for a in onl)
        kont.append((ad_, v_, k_.Volume()))
    kontrol("ağız kenarları bükülü (çapaksız): " + " · ".join("%s %.0f/%.0f mm³" % k for k in kont) + " — dört kenar tam kapalı (derz hizası 1107,5–1110,5 hariç)",
            all(v_ >= 0.97 * vt for _a, v_, vt in kont))
    t_t = [(round(dunya(p).intersect(top).Volume(), 1), p["ad"]) for p in ps if QR._bbk(bb[p["ad"]], top.BoundingBox())]
    t_t = [x for x in t_t if x[0] > 0.0]
    kontrol("TOP YOLU (Ø98 · x %.0f–%.0f · y %.0f–%.0f · z %+.0f…%+.0f) kabin parçasına değmez" % (TOP["x"][0], TOP["x"][1], TOP["y"][0], TOP["y"][1], TOP["z"][1], TOP["z"][0]), not t_t, str(t_t))
    alan = kutu(PERDE["x"][0], PERDE["x"][1], PERDE["alt_y"][1], PERDE["ust_y"][0], PERDE["z"][0], PERDE["z"][1])     # ışınların geçtiği hacim (dikey ışınlar)
    a_c = [(round(dunya(p).intersect(alan).Volume(), 1), p["ad"]) for p in ps if QR._bbk(bb[p["ad"]], alan.BoundingBox())]
    a_c = [x for x in a_c if x[0] > 0.0]
    ortu = PERDE["x"][0] <= AGIZ["x"][0] and PERDE["x"][1] >= AGIZ["x"][1] and PERDE["alt_y"][1] <= AGIZ["y"][0] and PERDE["ust_y"][0] >= AGIZ["y"][1]
    kontrol("IŞIK PERDESİ (denetçi 4): ışın alanı x %.0f–%.0f · y %.1f–%.1f · z %+.0f…%+.0f ağzı (x %.0f–%.0f · y %.0f–%.0f) TAM örter · ışın yolunda kabin parçası yok · perde çubukları ağız tünelinin dışında"
            % (PERDE["x"][0], PERDE["x"][1], PERDE["alt_y"][1], PERDE["ust_y"][0], PERDE["z"][0], PERDE["z"][1], AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1]),
            ortu and not a_c, str(a_c[:4]))
    print("   BİLGİ · ISO 13855: 14 mm çözünürlük → S = 2000 mm/s × T (C = 0) · ışın düzlemi z ≈ +49,5 → konilere ~220 mm → toplam durma T ≤ 110 ms (perde 14 + kontrolör ~16 + açıcı/tabla STO ≤ 80 ms, VARSAYIM ölçülecek)")
    dsk = kutu(DISK["x"][0], DISK["x"][1], DISK["y"][0], DISK["y"][1], DISK["z"][0], Z_ON + 700.0)
    d_c = [(round(dunya(p).intersect(dsk).Volume(), 1), p["ad"]) for p in ps if p["grup"] != "ALT_PANEL" and QR._bbk(bb[p["ad"]], dsk.BoundingBox())]
    d_c = [x for x in d_c if x[0] > 0.0]
    kontrol("GÜNLÜK DİSK SÖKÜMÜ: alt panel aletsiz çıkınca Ø340 disk (x %.0f–%.0f · y %.0f–%.0f, pimlerden 8 mm kalkık) önden çıkar — kalan kabin parçasına değmez · çerçeve açıklığı x %.1f–%.1f · y %.1f–%.0f"
            % (DISK["x"][0], DISK["x"][1], DISK["y"][0], DISK["y"][1], XS_SOL[1], XS_SAG[0], PERDE["alt_y"][1], Y_ORTA[0]), not d_c, str(d_c[:4]))
    # ---- 5 · kendi arasında + kaide ile + oturma ----
    tum = ps + [dict(p, ad="KAIDE:" + p["ad"]) for p in kd]
    cak = QR.kendi_arasinda(tum, istisna=lambda a, c: False)
    print("KENDİ ARASINDA (kabin + kaide_cad_v2, > 1 mm³): %s" % ("TEMİZ" if not cak else cak[:20]))
    kontrol("kabin + kaide kendi arasında çakışma = 0 (%d + %d parça · menteşe pimleri göz deliklerine temas eder)" % (len(ps), len(kd)), not cak, str(len(cak)))
    ts = [dunya(p).BoundingBox() for p in kd if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]
    oturma = []
    for ad_ in ("a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag", "onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme"):
        kes = dunya(P_[ad_]).intersect(kutu(-5.0, X_A1 + 5.0, Y_TABAN, Y_TABAN + 1.0, Z_ARKA - 5.0, Z_ON + 5.0))     # dikmenin alt 1 mm'lik kesiti (kapak plakası dahil)
        des = kutu(ts.xmin, ts.xmax, Y_TABAN, Y_TABAN + 1.0, ts.zmin, ts.zmax)                                         # taban sacının üst yüzü
        if "cerceve" in ad_:
            alt = bb[ad_.replace("_dikme", "_alt_dikme")]                                                               # alt çerçeve dikmesinin üst ucu (893,5)
            des = des.fuse(kutu(alt.xmin, alt.xmax, Y_TABAN, Y_TABAN + 1.0, alt.zmin, alt.zmax))
            assert abs(alt.ymax - Y_TABAN) < 0.01
        oturma.append((ad_, 100.0 * kes.intersect(des).Volume() / kes.Volume()))
    kontrol("4 dikme tam oturur (denetçi 6): alt kesitin taban sacı (x %.1f–%.0f · z %.1f…%+.0f, üst %.1f) + alt çerçeve dikmesi üstündeki payı: %s"
            % (ts.xmin, ts.xmax, ts.zmin, ts.zmax, ts.ymax, " · ".join("%s %%%.1f" % (a.replace("a_kose_dikmesi_", "").replace("onyuz_cerceve_", "ön "), v) for a, v in oturma)),
            all(v >= 99.99 for _a, v in oturma) and abs(ts.ymax - Y_TABAN) < 0.01)
    # ---- 6 · HAVADA PARÇA (kabin + kaide) ----
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in tum], zemin_y=Y_DUZ)
    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · acici_kabin_cad_v1 + kaide_cad_v2")
    kontrol("havada parça = 0 (%d parça · kök [dolap üstü 788] %d · bağlı %d · beyaz liste YOK)" % (hv["parca"], hv["kok"], hv["bagli"]), not hv["bilesen"], str([d_["en"] for d_ in hv["bilesen"]]))
    # ---- 7 · servis kapağı AÇILMA TARAMASI (denetçi 2): gerçek menteşe ekseni, 0–90° 2,5° adım ----
    kp = [p for p in ps if p["grup"] == "SERVIS_KAPAGI"]
    kg_k = sum(dunya(p).Volume() * RO for p in kp if p["mal"] != "plastik")
    kc = cq.Compound.makeCompound([dunya(p) for p in kp])
    sabit = [(p["ad"], dunya(p), bb[p["ad"]]) for p in ps if p["grup"] != "SERVIS_KAPAGI"]
    k_c, xmin_s, xmax_s, adim = [], 1e9, -1e9, 0
    acilar = [0.5, 1.0, 1.5, 2.0] + [2.5 * i for i in range(1, 37)]                     # ilk 2° ince adım (kapak çerçeveden kalkarken) + 2,5° adım
    for aci in acilar:
        r = kc.rotate(*kapak_pozu(aci)); rb = r.BoundingBox(); adim += 1
        xmin_s, xmax_s = min(xmin_s, rb.xmin), max(xmax_s, rb.xmax)
        for a_, s_, b_ in sabit:
            if QR._bbk(b_, rb):
                v_ = r.intersect(s_).Volume()
                if v_ > 1.0: k_c.append((aci, a_, round(v_, 1)))
    r90 = kc.rotate(*kapak_pozu(90.0)).BoundingBox()
    kontrol("SERVİS KAPAĞI AÇILMA TARAMASI (denetçi 2): gerçek menteşe ekseni x %.0f · z %.0f · 0–90° %d adım (0,5° × 4 + 2,5°) · %.1f kg · kabin parçasına çakışma 0 · sol duvar payı x_min %.2f ≥ −%.0f (duvar −%.0f VARSAYIM) · C paneline x_max %.2f < 701,5"
            % (MENTESE["pivot"][0], MENTESE["pivot"][1], adim, kg_k, xmin_s, DUVAR_ARALIK - 2.0, DUVAR_ARALIK, xmax_s),
            not k_c and xmin_s >= -(DUVAR_ARALIK - 2.0) and xmax_s < 701.5 - 0.5, str(k_c[:6]))
    print("   BİLGİ · 90° açık kapak x %.1f…%.1f · z %+.1f…%+.1f → robot koridorunda z %+.0f'e kadar (ray ekseni z 360) → RSS 36 açık kapakta robotu + açıcıyı + tablayı durdurur; servis kilidi yazılımda"
          % (r90.xmin, r90.xmax, r90.zmin, r90.zmax, r90.zmax))
    kg_b = {b: sum(dunya(p).Volume() * RO for p in ps if p["birim"] == b and p["mal"] != "plastik") for b, _a in BIRIMLER}
    print("   KÜTLE (304, plastik hariç): " + " · ".join("%s %.1f kg" % kv for kv in kg_b.items()) + " · alt panel %.1f kg" % (dunya(P_["onyuz_alt_panel"]).Volume() * RO))
    print("   ÖN ÇERÇEVE 30 × 20: %d profil · toplam boy %.2f m (BOM ile aynı kaynaktan)" % (len(CER_PARCA), sum(b for _a, b in CER_PARCA) / 1000.0))
    if "hizli" not in arg:
        # ---- 8 · TOPPING (TC + TU) ile çakışma: statik · kafa +60/+90 · tabla + araba A→C geçişi ----
        t1 = time.time()
        S, D, tc_ad, tu_ad = topping_setleri()
        print("   (TOPPING: %s · %s · statik %d parça + dinamik %d konum-parça · %.0f sn)" % (tc_ad, tu_ad, len(S), len(D), time.time() - t1))
        c_s = capraz(ps, S)
        c_d = capraz(ps, D)
        kapi = [c for c in c_s + c_d if c[3] == "ACICI"]                                    # MONTAJ KAPISI: istisnasız
        acik = [c for c in c_s + c_d if c_istisnasi(c, tc_ad)]
        kalan = [c for c in c_s + c_d if not c_istisnasi(c, tc_ad)]
        for c in sorted(acik, reverse=True)[:14]:
            print("   C AÇIK KONU · %10.1f mm3  %-36s <-> %-44s (parça en ön z %+.1f · kesişim z ≥ %+.1f)" % (c[0], c[1], c[2], c[4], c[5]))
        kontrol("kabin ↔ TOPPING statik (%s %d parça x + 700 · y + 892 + %s x + 700 · y − 168) çakışma = 0 (dar istisna, yalnız %s: %d bulgu → C)"
                % (tc_ad, sum(1 for c in S if c[0].startswith("TC:")), tu_ad, TC_ISTISNA_SURUM, len([c for c in acik if c in c_s])), not [c for c in kalan if c in c_s], str([c for c in kalan if c in c_s][:6]))
        kontrol("kabin ↔ TABLA + ARABA A→C geçişi (x kayması %s mm; sol sert durak −70 … C içi +900) çakışma = 0 (istisna YOK)" % ", ".join("%+.0f" % v for v in X_KAYMA),
                not [c for c in kalan if c in c_d and c[3] in ("TABLA", "ARABA")], str([c for c in kalan if c in c_d][:6]))
        kontrol("kabin ↔ AÇICI KAFASI (inik + %s mm kalkık) çakışma = 0 — dar istisna: yalnız %s · onyuz_ · kesişim z ≥ +38,5 (%d bulgu → C, v25'te istisna kalkar)"
                % (" / +".join("%.0f" % v for v in KAFA_KALKIS), TC_ISTISNA_SURUM, len(acik)), not [c for c in kalan if c[3] == "ACICI"], str([c for c in kalan if c[3] == "ACICI"][:6]))
        print("   MONTAJ KAPISI (denetçi 1 · acici_kapisi()): açıcı ↔ kabin istisnasız %d çakışma (%s) → %s" % (len(kapi), tc_ad,
              "AÇIK — A montaja alınabilir" if not kapi else "KAPALI — A montaja %s gelmeden alınmaz; montajdaki \"__ACICI\" istisnası kalmaz" % ("topping_cad_v25" if tc_ad == TC_ISTISNA_SURUM else "düzeltilmiş TC")))
        dsk_tc = [(a_, s_) for a_, s_, g_ in S if a_.startswith("TC:") and g_ != "ACICI" and a_ != "TC:calisma_diski"] + [(a_, s_) for a_, s_, g_ in D if a_.startswith("TC(kafa +%.0f)" % DISK["kafa"])]
        d_t = [(round(s_.intersect(dsk).Volume(), 1), a_) for a_, s_ in dsk_tc if QR._bbk(s_.BoundingBox(), dsk.BoundingBox())]
        d_t = [x for x in d_t if x[0] > 1.0]
        kontrol("GÜNLÜK DİSK SÖKÜMÜ ↔ TOPPING (%s, açıcı kafası +%.0f'ta; disk pimleri tablada kalır): disk yolu temiz" % (tc_ad, DISK["kafa"]), not d_t, str(d_t[:6]))
        ap_ = [dict(ad="onyuz_isik_perdesi_ALANI", wp=cq.Workplane("XY").add(alan))]
        a_t = capraz(ap_, S + D)
        a_ac = [c for c in a_t if c_istisnasi(c, tc_ad)]
        a_kl = [c for c in a_t if not c_istisnasi(c, tc_ad)]
        for c in sorted(a_ac, reverse=True)[:6]:
            print("   C AÇIK KONU · ışın alanı · %10.1f mm3 <-> %s" % (c[0], c[2]))
        kontrol("IŞIK PERDESİ ışın alanı ↔ TOPPING (statik + kafa +60/+90 + tabla kaymaları) boş — yalnız robot girerken kesilir (muting) · dar istisna %s: %d bulgu → C"
                % (TC_ISTISNA_SURUM, len(a_ac)), not a_kl, str(a_kl[:6]))
        tcw = {a_[3:]: s_ for a_, s_, g_ in S if a_.startswith("TC:")}
        if "dis_yan_sol" in tcw:
            ys_ = tcw["dis_yan_sol"].BoundingBox()
            if ys_.zmax >= Z_CER[0] - 0.01:
                d_s = [mesafe(dunya(P_[a_]), tcw["dis_yan_sol"]) for a_ in ("onyuz_cerceve_sag_dikme", "a_kose_dikmesi_arka_sag")]
                kontrol("C SOL YAN SACI (%s, z %.0f…%+.0f) ↔ A sağ ön dikme / arka sağ dikme temas: %.2f / %.2f mm (cıvatalı LEGO, denetçi 5)" % (tc_ad, ys_.zmin, ys_.zmax, d_s[0], d_s[1]),
                        all(0.0 <= v <= 0.05 for v in d_s))
            else:
                print("   BİLGİ (denetçi 5) · %s dis_yan_sol z %.0f…%+.0f < +39 → A sağ ön dikmesi (z +9…+59) C'ye henüz DEĞMEZ; A'nın sağında z %+.0f…+9 açık · C v25 (+39) gelince bu satır DENETİME döner"
                      % (tc_ad, ys_.zmin, ys_.zmax, ys_.zmax))
        mk = [s_.BoundingBox() for a_, s_ in tcw.items() if a_.startswith("onyuz_mekanizma_kanadi")]
        if mk:
            c_alt = min(b.ymin for b in mk)
            print("   %s · C mekanizma kanatları (%s, %d parça) alt kenarı y %.1f · A alt paneli %.1f → A|C derzinde %.1f mm basamak%s"
                  % ("BİLGİ" if abs(c_alt - Y_ALT[0]) < 0.01 else "UYARI (C'ye, denetçi 3)", tc_ad, len(mk), c_alt, Y_ALT[0], c_alt - Y_ALT[0],
                     "" if abs(c_alt - Y_ALT[0]) < 0.01 else " — C kanatları da %.0f'den başlamalı (dolap önü %.0f + derz 3 = fırın altındaki çizgi; tek sabit)" % (Y_ALT[0], Y_B_ON)))
        hh = [(a_, s_) for a_, s_, g_ in S if a_.startswith("TU:hava_hatti_acici")]
        if hh:
            print("   BİLGİ · açıcı hava hattı (%s, %d parça) ↔ A arka sağ dikme / sağ ön dikme en yakın mesafe %.1f / %.1f mm (çakışma 0 yukarıda)"
                  % (tu_ad, len(hh), min(mesafe(s_, dunya(P_["a_kose_dikmesi_arka_sag"])) for _a, s_ in hh), min(mesafe(s_, dunya(P_["onyuz_cerceve_sag_dikme"])) for _a, s_ in hh)))
        ac_z = [c for c in S if c[2] == "ACICI"]
        print("   BİLGİ · açıcı kafası en ön z %+.1f (%s) · kabin açıcıya +39'a kadar yer bırakır (ön çerçeve + ışık perdesi +39…+59)" % (max(c[1].BoundingBox().zmax for c in ac_z), tc_ad))
        hv2 = DT.havada([(p["ad"], dunya(p)) for p in tum] + [(a_, s_) for a_, s_, g_ in S if a_.startswith("TC:")], zemin_y=Y_DUZ)
        hA = [d_ for d_ in hv2["bilesen"] if d_["bb"].xmin < X_A1 - 0.5]
        print("   BİLGİ · A hacminde havada kalan TOPPING bileşeni (%s, C ajanının işi): %d bileşen (%d parça) — kabin/kaide parçası YOK: %s"
              % (tc_ad, len(hA), sum(len(d_["uye"]) for d_ in hA), not any(u_.startswith(("a_", "onyuz_", "KAIDE:")) for d_ in hv2["bilesen"] for u_ in d_["uye"])))
        for d_ in hA:
            b_ = d_["bb"]
            print("      HAVADA (TC) · %-28s %d parça (%s) · x %.0f–%.0f y %.0f–%.0f z %.0f…%.0f" % (d_["en"], len(d_["uye"]), ", ".join(d_["uye"][:5]), b_.xmin, b_.xmax, b_.ymin, b_.ymax, b_.zmin, b_.zmax))
        # ---- 9 · çekmeceli dolap (store_cad_v8 varsa, yoksa v7) ----
        t2 = time.time()
        import importlib
        sc_ad = "store_cad_v8" if os.path.exists(os.path.join(U, "store_cad_v8.py")) else "store_cad_v7"
        try:
            SC = importlib.import_module(sc_ad); SC.PARCALAR[:] = []; SC.modul()
            B_ = [("B:" + p["ad"], p["wp"].val(), "B") for p in SC.PARCALAR]
            B_ = [x for x in B_ if x[1].BoundingBox().ymax > Y_DUZ - 5.0 and x[1].BoundingBox().xmin < X_A1 + 5.0]
            c_b = capraz(ps, B_)
            dus = max(x[1].BoundingBox().ymax for x in B_)
            kontrol("kabin ↔ çekmeceli dolap (%s, üst bandı %d parça) çakışma = 0 · dolap üstü %.1f = kabin altı %.1f (%.0f sn)" % (sc_ad, len(B_), dus, Y0_, time.time() - t2),
                    not c_b and abs(dus - Y_DUZ) < 0.01, str(c_b[:6]))
            onB = [x[1].BoundingBox() for x in B_ if x[1].BoundingBox().zmax >= Z_ON - 0.5 and x[1].BoundingBox().xmin < X_PAN[1] and x[1].BoundingBox().xmax > X_PAN[0]
                   and x[1].BoundingBox().ymax <= Y_DUZ + 0.01]
            b_ust = max(b.ymax for b in onB) if onB else float("nan")
            kontrol("DOLAP DERZİ ÖLÇÜLEN (denetçi 3): %s ön düzlemdeki (z ≥ +78,5) en üst çekmece önü y %.1f → alt panel %.1f · görünen derz %.1f = 3,0 (fırın altındaki 785/788 çizgisiyle aynı)"
                    % (sc_ad, b_ust, Y_ALT[0], Y_ALT[0] - b_ust), bool(onB) and abs(Y_ALT[0] - b_ust - DERZ) < 0.01)
        except Exception as e:
            print("   BİLGİ · %s yüklenemedi (%s) — dolap taraması montajda" % (sc_ad, str(e)[:120]))
    if "bom" in arg:
        bom_yaz(BOM_KLASOR, ps)
    kl = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kl), time.time() - t0))
    assert not kl
    sys.stdout.flush(); os._exit(0)
