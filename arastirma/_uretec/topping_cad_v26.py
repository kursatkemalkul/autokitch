# -*- coding: utf-8 -*-
"""v26 (28 Eyl 2026 akşam · yap_topping_cad_v26.py): AÇICI KOLONU kutu profil 120 × 50 × 4 (v25 dolu blok) · RAY ÖRTÜ ÇATISI 2 ayrı L şerit (yarık boydan boya) · başka değişiklik yok. Önceki: topping_cad_v25.py
v25 (28 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.3) — kabuk ön kenarı +39 + ön dönüş · ön çerçeve + tava paneller (mekanizma 2 kanat,
  teknik cep T) · AÇICI ön tahriki DİK AÇILI NMRV030, kafa ön ucu +10, açıcı ≤ +39, Z ekseni ray + araba + adaptör, pnömatik DSBC-32-100 dik asılı ·
  havada parçalar bağlandı · montaj V1_TASI kaydırmaları yeni adlarla son yerinde · dünya denetimi (TU v14 + itici). Önceki: topping_cad_v24.py (yap_topping_v25.py)
v25 DÜZELTME (28 Eyl sabah · on_duzlem_v63/denetim_C.md): mekanizma kanatları 788'den (A|C basamak yok) · tava panel menteşeleri kol + taban, sanal pivot
  ön dış köşe · bas-aç mandallar simetrik (üst kayıtta) · T sol dikmesi dikey ayırma sacına 2 L köşebent · teknik cep 2 × L 30×30×3 taşıyıcı + titreşim
  takozu · T yarıkları çerçevenin önünden çekildi · eski v1 soğuk hücre / ön kapak BOM'dan çıktı · dünya denetimi: soğuk taban kaçağı, çerçeve bandı,
  5 kapak açılma taraması (flipper katlanarak), hazne dolum çekmesi, bağlantı temasları, havada beyaz listesi ≤ 0,25 mm açıklıkla
v24 (26 Eyl 2026 gece): TOPPING TEKNESİ MODÜL İÇİNDE BİTER — X motoru + tahrik kasnağı SOL uca (−560), avara + gergi SAĞ uca (1650),
  kayış kelepçeleri arabanın sol yarısına (Xc −130 · −50); tekne/kirişler −600…1795 (v23: −555…1885, F fırınına 85 mm giriyordu).
  Sağ tampon kayış koluna (1617–1629), limit+ 1647, bağlama laması 1745, kayış 4480. Sağ dış saca hava rakor deliği. Önceki: topping_cad_v23.py
AUTOKITCH · 3 · TOPPING MODÜLÜ — ÜRETİM MODELİ v1 (22 Eyl 2026)
Kemal: "bunlar niye bu kadar önde, birde arka kısımlarını o motor yerlerini — bu TOPPING'i full tasarla, üretime yönelik."

NE ÇÖZÜLDÜ
  · KASET ÖNE TAŞIYORDU: kulp z = 0'ın 48 mm önüne çıkıyordu, kabin kapanmıyordu. Kaset 80 mm içeri alındı,
    önüne yalıtımlı KAPAK kondu; kulp artık kabinin içinde (topping_hesap_v4.py · derinlik dizilimi).
  · ARKA 505 mm BOŞTU: artık KAVRAMA (40) + YALITIMLI BÖLME (65) + KURU MAKİNE BÖLMESİ (320). Motorlar soğuk hücrenin
    DIŞINDA, yalıtımın arkasında; mil bölmeden yataklı-keçeli kovanla geçiyor. Yoğuşma almıyorlar, soğutma yükü yok.
  · 12 TAHRİK (6 kaset × 2 mil): NEMA23 kapalı çevrim step + EŞ EKSENLİ planet redüktör i=10. Sonsuz vida (NMRV030)
    kullanılmadı: girişi dik olduğu için motor yana taşıyor, 140'lık kasetin arkasında komşuya giriyordu.
  · Mil eksenleri kaset üreteçlerinden OKUNUR (hardcode yok): 140 sınıfı CY 60 / YC 164 · kaşar CY 40 / YC 195.

KOORDİNAT (modül yereli): x 0..1800 soldan sağa · y 0..970 aşağıdan yukarı (makinede 1060 eklenir) · z 0 ön yüz, −830 arka.
ÇIKTI: arastirma/3_TOPPING/topping_modul_v22/ (parça başına STEP + STL, MONTAJ.step, BOM.csv) · otonom/hat3d/ (GLB/USDZ)

v2 (22 Eyl 2026): kuru bolme 200 (arkada bosluk yok) · kaset 120 geriye, onunde ON NIS ·
evaporator ve hava kanali kasetlerin ICINDEN cikarildi · meme yarigi kasetin kendi agiz olcusunden ·
cakisma taramasina KASETLER girdi. Onceki: topping_cad_v1.py
v3 (22 Eyl 2026): meme yarigi hucre on sinirina kadar acildi (kaset YUVADAN CIKMIYORDU) ·
evaporator kasetlerin ARKASINA, millerin ustune · huni bacasi pideye 40 mm kala biter ·
kaset alti bosluk 20 -> 10. Onceki: topping_cad_v2.py
v4 (22 Eyl 2026): evaporator DELIKLI SAC PERDE arkasinda bir plenumda (ticari sogutucu standardi) ·
baca bastan basa acildi (ustu kapaliydi) ve iki kademeli oldu. Onceki: topping_cad_v3.py
v5 (22 Eyl 2026): evaporator KURU BOLMEYE (motorlarin ustune), sogutma arka yalitimdaki iki bosluktan ·
baca/huni parcasi kalkti, kasetin kendi YUVARLAK borusu pideye iniyor. Onceki: topping_cad_v4.py
v6 (22 Eyl 2026): her YUVA kendi kaset CAD'ini kullaniyor (once 140/280 sinifina gore tek model
varsayiliyordu). HARC 1 ve HARC 2 artik harc_cad_v1 — duckbill valfli, Ic O25 borulu harc/sos kaseti.
v7 (22 Eyl 2026): ON CERCEVE SACI KALKTI (Kemal: "en ondeki metal anlamsiz parcayi kaldir, dis kabukta
sadece sag sol arka ust alt") · HARC yuvalari harc_cad_v2 — VIDA YOK, hortum pompali borulu nozzle.
v8 (22 Eyl 2026): DONER TABLA — x arabasi (lineer kizak + kayis) + tabla (O360, 35 dev/dk).
Nozzle sabit; tabla donerken x'te kaydigi icin agiz pide uzerinde spiral ciziyor.
v9 (22 Eyl 2026): kaset borulari yalitimin ust yuzunde bitiyor; yalitimda uzun yarik yerine TEK YUVARLAK
DELIK + icinde DOZAJ KOVANI. damlama_teknesi ve agiz_cercevesi silindi.
v10 (22 Eyl 2026): DONER TABLA TAM URETIM MODELI — tekne + kiris merdiveni + HGR15 raylar + 4 blok +
araba plakasi + doner yatak + ayar bilezigi + gobek + tabla + pancake motor + lokma + GT3 kayis
zinciri + apron + cati + kirinti cekmecesi + enerji zinciri + 5 sensor + tamponlar. Ray yarigi kalkti.
"""
import csv, io, json, math, os, re, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
URETIM = None   # v24/v23: üretim klasörü YOK (kural 6.7)
XK_SOL, XK_SAG = -560.0, 1650.0   # v24: X kayışı kasnak merkezleri (motor SOLDA, avara SAĞDA) — H.KAYIS_SOL/SAG yerine
# ---- v25 · ÖN DÜZLEM (SPEC_on_duzlem_v63) ----
Z_ON = 79.0                        # ön düzlem = fırın ön yüzü (montaj sözleşmesi Z_ON = FT.ZS)
Z_KABUK = 39.0                     # dış kabuk (taban, tavan, yan saclar) ön kenarı = soğuk kapak arkası
Z_CER_C = (39.0, 59.0)             # C ön çerçevesi 30 × 20 × 2 (tava panellerin arkası)
Z_PAN_C = (59.0, 79.0)             # tava panel: yüz 1,5 (+77,5…+79) + 20 dönüş
DERZ = 3.0
DX_D, DY_D = 700.0, 892.0          # TC yerel → dünya (montaj: x + 700 · y + 892)
TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v15.py")        # dünya denetiminde soğuk paket (montaj: spec_from_file_location, bir kez −168)
ITICI_MOD = os.environ.get("TOPPING_ITICI", "itici_cad_v5")
RAKOR_ACICI = ((1472.0 - 892.0, -700.0), (1460.0 - 892.0, -712.0))       # sol yan sac · açıcı hattı 2 × Ø6 (TU v14 hava_hatti_acici_D6_1/2)
RAKOR_ANA = (1809.0 - 892.0, -432.0)                                      # sağ yan sac · montaj ANA_V44 (dünya y 1809, z −432)
MEK_PAN_Y0 = 788.0                 # v25b · mekanizma kanatlarının alt kenarı = A alt paneli (dolap önü 785 + derz 3 · A|C birleşiminde basamak yok — A ajanı / denetçi 3)
ON_PANELLER = {"onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, MEK_PAN_Y0, 1107.5), "onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, MEK_PAN_Y0, 1107.5),
               "onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0)}          # v25b · tava paneller DÜNYA x0, x1, y0, y1 (pafta / montaj buradan okusun)
T_YARIK_Y = (700.0, 860.0)          # v25b · T lazer yarık bantlarının ilk sırası (yerel y · giriş / çıkış; v25: 690 / 870 → çerçeve kayıtlarının arkasında kalıyordu)
PAN_DON = {"onyuz_mekanizma_kanadi_sol": (701.5, "sol"), "onyuz_mekanizma_kanadi_sag": (2497.0, "sag"), "onyuz_T_kapagi": (2497.0, "sag")}   # dünya menteşe kenarı
TEK_TASIYICI_Y, TEK_TAKOZ = 1553.5 + 31.0, 10.0   # v25b · teknik cep taşıyıcı üstü (dünya) · titreşim takozu yüksekliği


def panel_don(sh, ad, aci):
    """v25b · tava panel açık konumu (DÜNYA şekli): çok kollu gizli menteşe, sanal dönme merkezi ön dış köşe (x menteşe kenarı, z +79), dikey eksen · aci derece"""
    x, yon = PAN_DON[ad.split(":")[-1]]
    return sh.rotate(cq.Vector(x, 0.0, Z_ON), cq.Vector(x, 1.0, Z_ON), -aci if yon == "sol" else aci)


def boru_y(x0, x1, z0, z1, y0, y1, t=2.0):
    """v25 · y boyunca kutu profil (uçları açık)"""
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))


def boru_x(y0, y1, z0, z1, x0, x1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def boru_z(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, min(z0, z1) - 1.0, max(z0, z1) + 1.0))


def omega_pz(x0, x1, yc, zt, yon, h=15.0, t=1.0):
    """v25 · x boyunca omega takviye 40 (10 + 20 + 10) · flanşlar z = zt yüzeyine oturur, tepe yon yönünde h (acici_kabin_cad_v1 ile aynı)"""
    lo = lambda a, b: (min(a, b), max(a, b))
    za, zb = zt, zt + yon * h
    w = kut(x0, x1, yc - 20.0, yc - 10.0, *lo(zt, zt + yon * t)).union(kut(x0, x1, yc + 10.0, yc + 20.0, *lo(zt, zt + yon * t)))
    w = w.union(kut(x0, x1, yc - 10.0, yc - 10.0 + t, *lo(za, zb))).union(kut(x0, x1, yc + 10.0 - t, yc + 10.0, *lo(za, zb)))
    return w.union(kut(x0, x1, yc - 10.0, yc + 10.0, *lo(zb, zb - yon * t)))


def tava(x0, x1, y0, y1, yariklar=()):
    """v25 · tava panel: yüz 304 fırçalı 1,5 (z +77,5…+79) + 4 kenar 20 arkaya bükülü (z +59…+77,5) · yariklar: (x0, x1, y0, y1) lazer kesik"""
    zy = Z_ON - 1.5
    w = kut(x0, x1, y0, y1, zy, Z_ON)
    for a, b, c, e in ((x0, x0 + 1.5, y0, y1), (x1 - 1.5, x1, y0, y1), (x0, x1, y0, y0 + 1.5), (x0, x1, y1 - 1.5, y1)):
        w = w.union(kut(a, b, c, e, Z_PAN_C[0], zy))
    for a, b, c, e in yariklar:
        w = w.cut(kut(a, b, c, e, zy - 1.0, Z_ON + 1.0))
    return w


def silx(y, z, r, x0, x1):
    """v24: x boyunca silindir"""
    return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))
from kaset_3d_v3 import Mesh, MM, MALZEME, doku_ad, usdz_yaz, OUT
import topping_hesap_v6 as H

# ---------------------------------------------------------------- SABİTLER ----------------------------------------------------------------
W, Y, D = 1800.0, 970.0, 830.0                       # modül gabarisi (pafta HAT v19: modül C)
SAC, SAC_IC, PU = 1.5, 1.0, 60.0                     # dış sac · iç kabuk · poliüretan
Y0 = 1060.0                                          # modülün makinedeki taban kotu
ZK = H.Z_KASET; ZKAP = H.Z_KAPAK; ZKAV = H.Z_KAVRAMA; ZBOL = H.Z_BOLME; ZKURU = H.Z_KURU; ZNIS = H.Z_NIS
AGZ = (10.0, 120.0); BAS = (123.0, 257.0); KAS = (260.0, 620.0); TEK = (706.0, 962.0)    # yerel y zonları
# Harç kasetleri henüz tasarlanmadı; yuvası 280 (kaşar gövdesi sınıfı) ve mil eksenleri de kaşarınki VARSAYILDI.
# PAFTA DÜZELTMESİ: HAT v19'da yuva genişlikleri kaset genişliğine BİREBİR eşitti ve yuvalar bitişikti —
# kılavuz lamasına ve geçme boşluğuna yer kalmıyordu, kaset fiziksel olarak girmezdi. Yuvalar burada
# kaset + BOSLUK, aralarında BOLME kalınlığında ayırıcı olacak şekilde YENİDEN hesaplanıyor ve ortalanıyor.
BOSLUK, BOLME = 2.0, 3.0
_ADLAR = ("HARÇ 1", "HARÇ 2", "KIYMA", "KUŞBAŞI", "KAŞAR KABI", "KÜP SUCUK")
_GEN = (280, 280, 140, 140, 280, 140)
_TOP = sum(_GEN) + len(_GEN) * BOSLUK + (len(_GEN) + 1) * BOLME
_X = round(30.0 + PU + ((W - 2 * (30.0 + PU)) - _TOP) / 2.0, 1)
YUVA = []
for _ad, _g in zip(_ADLAR, _GEN):
    _X += BOLME
    YUVA.append((_ad, _X, _X + _g + BOSLUK, _g)); _X += _g + BOSLUK
_X += BOLME
# v6: sınıf değil YUVA bazlı — HARÇ yuvaları kaşarla aynı gövdeyi kullanıyor ama borusu ve valfi başka.
XC_TABLA = H.X_PARK          # tablanin CIZILDIGI yer = PARK KONUMU (acicinin alti)
KASET_CAD = {"HARÇ 1": "harc_cad_v4", "HARÇ 2": "harc_cad_v4", "KIYMA": "kiyma_cad_v9",
             "KUŞBAŞI": "kusbasi_cad_v8", "KAŞAR KABI": "kasar_cad_v14", "KÜP SUCUK": "sucuk_cad_v8"}


def boru(modul):
    """kasetin YUVARLAK çıkış borusu: iç çap, et, alt uç kotu (kaset yerel y). Taban yarığı ve
    kaset zarfı buna göre kuruluyor — sayı iki yerde yazılmasın."""
    import re
    k = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    m = re.search(r"^BORU_D, BORU_ET, BORU_ALT(?:, BORU_GECIS)?\s*=\s*([\d.]+),\s*([\d.]+),\s*(-?[\d.]+)", k, re.M)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def agiz(modul):
    """kasetin ÇIKIŞ AĞZININ kaset yerel z aralığı — meme yarığı buna göre açılır.
    v1'de yarık kasetin ön yüzünden 5 mm geride başlıyordu; ağız ise ön yüzün ÖNÜNDEYDİ,
    yani ürün yarığa denk GELMİYORDU. Artık kasetin kendi ölçüsünden okunuyor."""
    import re
    k = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    g = lambda ad: float(re.search(r"^%s.*?=\s*([\d.]+)" % ad, k, re.M | re.S).group(1))
    m = re.search(r"^AG_Z0, AG_Z1, AG_X\s*=\s*([\d.]+),\s*([\d.]+)", k, re.M)
    d = re.search(r"^W, D, H\s*=\s*([\d.]+),\s*([\d.]+)", k, re.M)
    return float(m.group(1)), float(m.group(2)), float(d.group(2))


AGIZ = {a: agiz(m) for a, m in KASET_CAD.items()}
BORU = {a: boru(m) for a, m in KASET_CAD.items()}
MALZEME.setdefault("sac", dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32))
MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))
MALZEME.setdefault("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45))
MALZEME.setdefault("bakir", dict(renk=(0.72, 0.45, 0.20, 1.0), met=0.9, ruf=0.35))
MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))
MALZEME.setdefault("silikon", dict(renk=(0.85, 0.30, 0.20, 1.0), met=0.0, ruf=0.6))          # v25
MALZEME.setdefault("plastik", dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6))


def eksen(modul):
    """kaset üretecinden mil eksenlerini OKU (iki yerde yazılmasın)"""
    s = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    m = re.search(r"CY, RT, YC, RB, RF, Y_UST, Y_DOLUM = ([\d.]+), ([\d.]+), ([\d.]+)", s)
    assert m, modul + ": eksen satiri bulunamadi"
    return float(m.group(1)), float(m.group(3))

EKSEN = {a: eksen(m) for a, m in KASET_CAD.items()}


kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def koni_y_t(x, z, r_ust, r_alt, y0, y1):
    """y ekseninde konik (merkezleme pimi): y0'da r_alt, y1'de r_ust"""
    if abs(r_alt - r_ust) < 0.01: return sily(x, z, r_alt, y0, y1)
    return cq.Workplane(obj=cq.Solid.makeCone(r_alt, r_ust, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0)))


def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
PARCALAR = []
# v11 · yuva etiketi kotlari — hat_montaj dokuyu BU kotlara yapistiriyor, iki yerde ayri sayi olmasin
ET_Y0, ET_Y1 = KAS[1] + 1.0, KAS[1] + 17.0          # kaset tavaninin (620) 1 mm ustu, 16 mm yuksek
ET_Z0, ET_Z1 = ZKAP[1] - 2.5, ZKAP[1] - 1.0        # hucrenin ON RIMINDE, on kapagin 1 mm gerisinde
# Yuvaya giren urunun adi — etiketin yazisi ve simulasyon bunu OKUR (iki yerde ayri liste olmasin)
URUN = {"HARÇ 1": "LAHMACUN HARCI", "HARÇ 2": "PİZZA SOSU", "KIYMA": "KIYMA",
        "KUŞBAŞI": "KUŞBAŞI", "KAŞAR KABI": "KAŞAR", "KÜP SUCUK": "KÜP SUCUK"}

# ======================= HIWIN GERCEK CAD (TraceParts STEP AP214) =======================
KATALOG_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "hgh15ca.stp")
_HIWIN = {}


def hiwin():
    """HGH15CA STEP'ini bir kez yukler: araba katisi + ray kesiti.
    STEP'te ray Z'de uzuyor; bizim modelde X'te. Y ekseni etrafinda 90 derece ceviriyoruz."""
    if _HIWIN: return _HIWIN
    w = cq.importers.importStep(KATALOG_STEP)
    sol = sorted(w.val().Solids(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    araba = next(s_ for s_ in sol if abs(s_.BoundingBox().zlen - 61.4) < 1.0)
    ray = next(s_ for s_ in sol if abs(s_.BoundingBox().zlen - 150.0) < 1.0)
    DY = 35.5                                                   # STEP ray tabani -15 -> modelde 20,5
    _HIWIN["araba"] = araba.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0).translate(cq.Vector(0, DY, 0))
    _HIWIN["ray_ornek"] = ray.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0).translate(cq.Vector(0, DY, 0))
    return _HIWIN


def hiwin_ray(x0, x1, zc):
    """HIWIN ray KESITINI x0..x1 arasina uzatir + katalog delik desenini acar.
    Katalog (Linear_Guideway-E-1.pdf s.41): WR15 HR15 · gecme d4,5 · havsa D7,5 h5,3
    · hatve P60 · uctan E20 · civata M4x16."""
    orn = hiwin()["ray_ornek"]
    # Ornek ray 150 mm; kesitini alip X boyunca 1600 mm'ye uzatiyoruz. Delik olmayan bir
    # yerden kesiyoruz (delikler uctan 20, hatve 60 -> x=0 ortada, delik yok).
    # Kesit supurme denendi, profilin yalniz bir yuzunu aldi (ray 5,5 mm cikti, 15 olmali).
    # Ornek rayin DELIGI YOK (27.449 mm3 / 150 mm = 183 mm2 profil alani, tam katalog
    # agirligini veriyor). O yuzden 150 mm'lik ornegi uc uca EKLIYORUZ, boya kesiyoruz,
    # sonra KATALOG delik desenini kendimiz aciyoruz.
    boy = x1 - x0
    n_kopya = int(boy // 150.0) + 1
    r = orn.translate(cq.Vector(75.0, 0.0, 0.0))
    for i in range(1, n_kopya):
        r = r.fuse(orn.translate(cq.Vector(75.0 + i * 150.0, 0.0, 0.0)))
    r = r.intersect(cq.Workplane("XY").box(boy, 60.0, 60.0, centered=(False, True, True))
                    .translate(cq.Vector(0.0, 28.0, 0.0)).val())
    r = r.translate(cq.Vector(x0, 0.0, zc))
    w = cq.Workplane(obj=r)
    n = int((x1 - x0 - 40.0) // 60.0) + 1
    for i in range(n):
        xd = x0 + 20.0 + i * 60.0
        if xd > x1 - 20.0: break
        w = w.cut(sily(xd, zc, 2.25, 20.0, 36.0))               # Ø4,5 gecme
        w = w.cut(sily(xd, zc, 3.75, 30.2, 36.0))               # Ø7,5 x 5,3 havsa (ust 35,5)
    return w, n


MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtr-23079.step")
GUC_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "ndr-240-24.stp")
UPS_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "ub10-242.stp")


def din_parca(yol, x0, y0, z0):
    """DIN ray cihazini STEP'ten alir ve bizim eksenlere oturtur.
    STEP'te: X = yukseklik, Y = ray boyunca genislik, Z = derinlik.
    Bizde:   X = makine boyu (ray yonu), Y = yukseklik, Z = derinlik.
    Z etrafinda 90 derece cevirince X<-genislik, Y<-yukseklik oluyor.
    x0,y0 = sol-alt kose; z0 = ON yuz (parca -z'ye, makinenin icine dogru uzar)."""
    # OCP bugu: cok-katili STEP Compound'ini tek hamlede dondurmek UPS'te
    # gecersiz Compound uretiyor; 18 katinin her biri tek basina gecerli. Katilari
    # ayri dondurup yeniden Compound kurunca hacim ayni ve sekil gecerli kaliyor.
    _w = cq.importers.importStep(yol).val()
    _ss = [q.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0) for q in _w.Solids()]
    sh = cq.Compound.makeCompound(_ss)
    b = sh.BoundingBox()
    _loc = cq.Location(cq.Vector(x0 - b.xmin, y0 - b.ymin, z0 - b.zmax))
    sh = cq.Compound.makeCompound([q.moved(_loc) for q in _ss])
    return cq.Workplane(obj=sh)


SURUCU_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-drv-4830.step")
_MOT = {}


def nema23():
    """STP-MTR-23079 gercek katisi (DC surum — v17'de AC surumden degistirildi).
    STEP'te: govde z -64,5..0, mil z 0..+31,6, kablo -y'de 333 mm uzuyor.
    Bizim modelde motorun mil yuzu zm'de ve govde -z'ye dogru uzuyor — ayni yonelim.
    STEP 17 kati tasiyor: govde + iki yatak gobegi + 4 baglama civatasi + kablo telleri."""
    if _MOT: return _MOT
    w = cq.importers.importStep(MOTOR_STEP)
    sol = w.val().Solids()
    # KABLO = motor zarfinin cok disina tasan katilar (teller). Govde = geri kalanin
    # hepsi (ana govde + civatalar + gobekler) — hepsi tek katiya kaynatiliyor.
    _kablolar = [x for x in sol if x.BoundingBox().ymin < -80.0]
    _govdeler = [x for x in sol if x.BoundingBox().ymin >= -80.0]
    govde = _govdeler[0]
    for x in _govdeler[1:]:
        govde = govde.fuse(x)
    kablo = _kablolar[0]
    for x in _kablolar[1:]:
        kablo = kablo.fuse(x)
    _KABLO_YON = -1.0      # yeni motorda kablo -y'ye uzuyor (eskisinde +y idi)
    # mili kes: mil redüktörün icine girer, onu redüktör temsil ediyor
    kes = cq.Workplane("XY").box(200, 300, 100, centered=(True, True, False)).val()
    _MOT["govde"] = govde.cut(kes)
    # KABLO: STEP'te DUZ 76 mm uzuyor ve bu haliyle 140'lik kasetlerde ust motora carpiyor
    # (olculdu: 3 yuvada 1.406 mm3 + fan_0'da 1.885 mm3). Iki mil arasi 104 mm, motor 57 —
    # aralik 47 mm. Gercek kablo BUKULEBILIR; modelde 25 mm'lik cikis guduguyle temsil
    # ediliyor. TASARIM KISITI: kablo motordan en cok 40 mm sonra donmeli, yani duz uclu
    # fis degil, DIRSEK KONNEKTOR ya da hemen bukulen kablo kanali gerekiyor.
    KAB = 25.0
    kb = kablo.BoundingBox()
    # v17 DUZELTME: eski motorda kablo +y'de idi, kb.ymin govdeye en yakin uctu.
    # Yeni motorda kablo -y'ye uzuyor; ayni satir kablonun UZAK ucundan 25 mm kesiyor,
    # gudukc motorun 300 mm otesinde havada kaliyordu (olculdu: y -32,8..-7,8).
    # Artik hangi yone giderse gitsin GOVDEYE YAKIN 25 mm aliniyor.
    _y0 = (kb.ymax - KAB) if kb.ymax <= 1.0 else kb.ymin
    _MOT["kablo"] = kablo.intersect(cq.Workplane("XY").box(40, KAB, 40, centered=(True, False, True))
                                    .translate(cq.Vector(0, _y0, (kb.zmin + kb.zmax) / 2)).val())
    return _MOT


def nema23_koy(xm, yy, zm):
    """motorun MIL YUZU zm'de olacak sekilde yerlestirir (govde -z'ye uzar)"""
    m = nema23()
    v = cq.Vector(xm, yy, zm)
    return (cq.Workplane(obj=m["govde"].translate(v)), cq.Workplane(obj=m["kablo"].translate(v)))


REDUKTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "pgcn23-1025.step")
_RED = {}


def suregear():
    """PGCN23-1025 gercek katisi. STEP: govde z -79..0, cikis mili 0..+24."""
    if _RED:
        return _RED
    w = cq.importers.importStep(REDUKTOR_STEP)
    # CIKIS MILINI KES: redüktörün cikis mili ile bizim "mil_*" parcamiz gercekte AYNI mil.
    # Ikisini birden koyunca ust uste biniyor (olculdu: 4.349 mm3 mil + 3.076 mm3 kovan).
    kes = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False)).val()
    _RED["tum"] = w.val().cut(kes)
    return _RED


def suregear_koy(xm, yy, z_cikis):
    """redüktörün CIKIS YUZU z_cikis'te olacak sekilde yerlestirir (govde -z'ye uzar)"""
    return cq.Workplane(obj=suregear()["tum"].translate(cq.Vector(xm, yy, z_cikis)))


YATAK_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "xu080149.stp")
_YAT = {}


def xu080149():
    """STEP'te yatak ekseni X boyunca (x 0..22,27). Bizim tablada eksen Y (dusey),
    o yuzden Z etrafinda 90 derece ceviriyoruz: x -> y."""
    if _YAT: return _YAT
    w = cq.importers.importStep(YATAK_STEP)
    _YAT["kati"] = w.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0)
    return _YAT


def ekle(ad, wp, mal, bom=None): PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, bom=bom))


def modul():
    UFL = (W / 2.0 - 120.0, W / 2.0 + 120.0)                                   # yalıtım boşluklarının x aralığı
    UFY, DNY = (KAS[1] - 75.0, KAS[1] - 5.0), (KAS[0] + 5.0, KAS[0] + 40.0)    # üfleme (üstte) · dönüş (altta) — mil bandının dışında
    HAMUR_, TEPSI_, TABLA_ = H.HAMUR_K, H.TEPSI_K, H.TABLA_K
    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0                            # v3: kaset altı boşluk 20 → 10 (Kemal: "neden bu kadar kalın")
    zc0, zc1 = ZKAP[1], ZBOL[1]                                               # soğuk paket derinliği (−20 … −510)
    XI0, XI1 = 30.0 + PU, W - 30.0 - PU                                       # hücre iç genişliği (90 … 1710)
    MIL = []                                                                  # (x, y, kod) — 12 tahrik mili; yalıtım ve kabuk bunlara göre delinir
    for ad, x0, x1, gen in YUVA:
        for j, ey in enumerate(EKSEN[ad]):
            MIL.append(((x0 + x1) / 2.0, KAS[0] + ey, "%s_%s" % (ad.replace(" ", "_"), "helezon" if j == 0 else "rotor")))
    # Kasetin MEMESİ hücrenin tabanından geçer: her yuvanın altına yarık açılır, ürün oradan aşağıdaki dozaj bandına düşer.
    # v9: YALITIM ve İÇ KABUKTA artık uzun yarık YOK — her yuvada TEK YUVARLAK DELİK (Kemal: "yalıtımda
    # sadece bir delik olur, etrafı kapanır"). Kaset borusu y 250'de, yani yalıtımın üst yüzünde bitiyor;
    # ürünü deliğin içindeki DOZAJ KOVANI aşağı indiriyor. Yarık yalnız TABAN RAYINDA kalıyor:
    # boru y 250–260 arasında rayın içinden geçiyor, kaset çekilirken o yol açık olmalı.
    DELIK = []                                                                 # (x merkez, z merkez, delik yarıçapı)
    for ad, x0, x1, gen in YUVA:
        bd, be, _ = BORU[ad]
        a0_, a1_, dd_ = AGIZ[ad]
        DELIK.append(((x0 + x1) / 2.0, ZK[0] + ((a0_ + a1_) / 2.0 - dd_ / 2.0), bd / 2.0 + be + 1.0))
    YARIK = [(x_ - r_ - 2.0, x_ + r_ + 2.0) for x_, z_, r_ in DELIK]           # yalnız taban rayı için
    # MEME YARIĞI kasetin KENDİ ağız ölçüsünden: kaset yerel z → modül z (kaset ön yüzü ZK[0]).
    # v3 DÜZELTMESİ: yarık yalnız ağız boyundaydı (42 mm) ve kaset öne çekilince meme 6 mm sonra iç kabuğun
    # tabanına çarpıyordu — KASET YUVADAN ÇIKMIYORDU. Yarık artık hücrenin ÖN SINIRINA kadar açık;
    # meme o sınırı geçince zaten hücrenin dışında (kapak açık) oluyor.
    _a0, _a1, _dd = AGIZ["KAŞAR KABI"]
    ZY = (ZKAP[1], ZK[0] + (_a0 - _dd / 2.0) - 6.0)                           # ön sınır … ağzın arka ucu + pay

    # ---------------- 1 · DIŞ KABUK (bükme sac 1,5 · AISI 304) ----------------
    ekle("dis_taban", kut(0, W, 0, SAC, Z_KABUK, -D), "sac", bom=("Dış taban sacı", 1, "304 1,5 mm · lazer + abkant", "modülün tabanı, alttaki B modülüne oturur"))
    ekle("dis_tavan", kut(0, W, Y - SAC, Y, Z_KABUK, -D), "sac", bom=("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant", "üst kapak; soğutma grubu buraya oturur"))
    for s, x in (("sol", 0.0), ("sag", W - SAC)):
        # v20: tabla iki uctan da modulden CIKIYOR — solda aciciya (modul A),
        # sagda firin bandina. Iki yan sacta da tabla yuksekliginde yarik var.
        _ys = kut(x, x + SAC, SAC, Y - SAC, Z_KABUK, -D)                          # v25: ön kenar +39 (kapak arkası)
        _xd = (SAC, SAC + 30.0) if s == "sol" else (W - SAC - 30.0, W - SAC)
        _ys = _ys.union(kut(_xd[0], _xd[1], SAC, Y - SAC, Z_KABUK - SAC, Z_KABUK))   # v25: 30 mm ön dönüş (içe) — çerçeve + soğuk kapak buna basar, menteşe buna
        # DUZELTME: once iki ayri delik acilmisti (tabla 92-130 ve mekanizma 1-66);
        # arada 66-92 DOLU kaliyordu ve tam oraya DONER YATAK (58,5-80,8) ile
        # AYAR BILEZIGI (80,8-86) denk geliyordu — tabla soldaki aciciya GECEMIYORDU.
        # Artik modulun alt bandi iki uctan da TEK PARCA acik: araba plakasi,
        # yatak, bilezik, gobek, tabla ve disk serbest gecer.
        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 150.0, -510.0, 5.0))   # v23: 132 → 150 (en yüksek ürün diskte 136,5) · v25: öne +5 (disk z 0'a kadar)
        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 66.0, -510.0, -1.0))   # mekanizma gecisi
        if s == "sag":
            _ys = _ys.cut(silx(RAKOR_ANA[0], RAKOR_ANA[1], 7.0, x - 1.0, x + SAC + 1.0))   # v25: ana hat rakoru Ø14 montaj hattıyla aynı eksende (dünya y 1809 · z −432; v24 y 1832 · z −415)
        else:
            for _ry, _rz in RAKOR_ACICI:
                _ys = _ys.cut(silx(_ry, _rz, 6.0, x - 1.0, x + SAC + 1.0))       # v25: açıcı hattı rakorları Ø12 (2 × Ø6 hortum)
        ekle("dis_yan_" + s, _ys, "sac", bom=("Dış yan sac", 2, "304 1,5 mm · lazer + abkant", "komşu modüle cıvatalanır (lego birleşim)") if s == "sol" else None)
    ekle("dis_arka", kut(SAC, W - SAC, SAC, Y - SAC, -D, -D + SAC), "sac", bom=("Dış arka sac", 1, "304 1,5 mm", "kuru bölmenin arkası; kablo rakorları burada"))
    # v25 · RAKORLAR (hortum çapında iç delik, yan sacın deliğine oturur): açıcı hattı 2 × (sol) + ana hat (sağ)
    for _i, (_ry, _rz) in enumerate(RAKOR_ACICI):
        ekle("rakor_hava_acici_%d" % _i, silx(_ry, _rz, 6.0, -1.5, SAC + 1.5).cut(silx(_ry, _rz, 3.0, -2.0, SAC + 2.0)), "koyu",
             bom=("Duvar geçiş rakoru Ø6 · SMC KQ2E06-00A (bulkhead)", 2, "sol yan sacta · somunlu", "açıcı Z silindirinin 2 hattı (valf adası → A)") if _i == 0 else None)
    ekle("rakor_hava_ana", silx(RAKOR_ANA[0], RAKOR_ANA[1], 7.0, W - SAC - 1.5, W).cut(silx(RAKOR_ANA[0], RAKOR_ANA[1], 5.0, W - SAC - 2.0, W + 1.0)), "koyu",
         bom=("Duvar geçiş rakoru Ø10 · SMC KQ2E10-00A (bulkhead)", 1, "sağ yan sacta · dışı x 2500'ü geçmez", "ana hat fırın üstünden TOPPING teknik cebine (montaj ANA_V44)"))

    # ---------------- 2 · ÖN YÜZ AÇIK (v7) ----------------
    # Kemal: "en öndeki metal anlamsız parçayı kaldır — dış kabukta TOPPING'in ön yüzeydeki sacı yani,
    # sadece sağ sol arka üst alt." Ön çerçeve sacı zaten üç büyük açıklıkla delinmişti (robot ağzı,
    # kaset kapağı, teknik bant servisi) ve hiçbir yükü taşımıyordu. Dış kabuk artık BEŞ YÜZ:
    # taban · tavan · iki yan · arka. Ön yüzü kaset kapağı, robot ağzı çerçevesi ve teknik bant kapağı kapatıyor.

    # ---------------- 3 · SOĞUK HÜCRE: PU 60 + iç kabuk 1,0 ----------------
    PUP = (("pu_taban", 30.0, W - 30.0, hy0 - PU, hy0), ("pu_tavan", 30.0, W - 30.0, hy1, hy1 + PU),
           ("pu_sol", 30.0, 30.0 + PU, hy0, hy1), ("pu_sag", W - 30.0 - PU, W - 30.0, hy0, hy1))
    for ad, x0, x1, y0, y1 in PUP:
        w_ = kut(x0, x1, y0, y1, zc0, zc1)
        if ad == "pu_taban":
            for x_, z_, r_ in DELIK: w_ = w_.cut(sily(x_, z_, r_, y0 - 1.0, y1 + 1.0))       # v9: yuvarlak dozaj deliği
        ekle(ad, w_, "pu", bom=("PU yalıtım paneli 60 mm", 4, "poliüretan 60 · λ 0,022 W/mK", "soğuk hücreyi sarar; ısı kaybı hesabı topping_hesap_v4") if ad == "pu_taban" else None)
    arka = kut(XI0, XI1, hy0, hy1, ZBOL[0], ZBOL[1])
    for x_, y_, k_ in MIL: arka = arka.cut(silz(x_, y_, 31.0, ZBOL[0] + 1, ZBOL[1] - 1))     # 12 mil geçişi
    for _y0, _y1 in (UFY, DNY):                                                              # v5: üfleme + dönüş boşlukları
        arka = arka.cut(kut(UFL[0], UFL[1], _y0, _y1, ZBOL[0] + 1, ZBOL[1] - 1))
    ekle("pu_arka", arka, "pu", bom=("PU arka bölme paneli 60 mm", 1, "poliüretan 60", "SOĞUK / KURU ayırıcı: motorlar bunun arkasında kalır"))

    ic = kut(XI0, XI1, hy0, hy1, zc0, ZBOL[0])
    ic = ic.cut(kut(XI0 + SAC_IC, XI1 - SAC_IC, hy0 + SAC_IC, hy1 - SAC_IC, zc0 + 1, ZBOL[0] + SAC_IC))
    for x_, z_, r_ in DELIK: ic = ic.cut(sily(x_, z_, r_, hy0 - 2.0, hy0 + 3.0))            # v9: yuvarlak dozaj deliği
    for x_, y_, k_ in MIL: ic = ic.cut(silz(x_, y_, 31.0, ZBOL[0] - 1, ZBOL[0] + SAC_IC + 1))
    ekle("ic_kabuk", ic, "sac", bom=("İç kabuk (soğuk hücre)", 1, "304 1,0 mm · bükme, köşeler kaynaklı-taşlanmış", "gıda bölgesi: köşe R ≥ 6, yıkanabilir; 6 meme yarığı + 12 mil geçişi"))

    # ---------------- 4 · ÖN KAPAK ----------------
    # v15: masif blok degil GERCEK SANDVIC. Disi 1,5 mm sac kabuk, ici PU.
    # (Masif modellenince 74,4 kg cikiyordu; gercegi ~12 kg.)
    _kx0, _kx1 = 84.0, W - 84.0
    _ky0, _ky1 = KAS[0] - 26.0, KAS[1] + 26.0
    _kz0, _kz1 = ZKAP[0], ZKAP[1] + 6.0
    _dis = kut(_kx0, _kx1, _ky0, _ky1, _kz0, _kz1)
    _ic = kut(_kx0 + 1.5, _kx1 - 1.5, _ky0 + 1.5, _ky1 - 1.5,
              min(_kz0, _kz1) + 1.5, max(_kz0, _kz1) - 1.5)
    ekle("on_kapak", _dis.cut(_ic), "sac",
         bom=("Ön kapak sacı · sandviç kabuğu", 1, "1,5 mm 304 · 2 menteşe + mıknatıslı kilit", "kaset ağzını kapatır; açılınca 6 kaset önden çekilir"))
    ekle("on_kapak_pu", _ic, "pu",
         bom=("Ön kapak PU dolgusu", 1, "poliüretan köpük 40 kg/m³", "sandviçin yalıtım çekirdeği"))
    cont = kut(88.0, W - 88.0, KAS[0] - 22.0, KAS[1] + 22.0, ZKAP[1] + 6.0, ZKAP[1])
    cont = cont.cut(kut(102.0, W - 102.0, KAS[0] - 8.0, KAS[1] + 8.0, ZKAP[1] + 7.0, ZKAP[1] - 1.0))
    ekle("kapak_contasi", cont, "silikon", bom=("Kapak contası", 1, "manyetik buzdolabı contası", "kapağın arka yüzünde; yalıtım panelinin ön yüzüne basar"))
    # v25: eski kapak menteşeleri (mentese_0/1) SİLİNDİ — montajda havada görünüyorlardı (SPEC §2.3). Soğuk kapaklar topping_uno_cad_v14'te.

    # ---------------- 5 · KASET YUVALARI ----------------
    for ad, x0, x1, gen in YUVA:
        k = ad.replace(" ", "_")
        # v10: RAY YARIĞI KALKTI. Ölçüldü: taban rayı z −200…−525, yarık z −104…−174 — kesişmiyorlar,
        # yarık SIFIR malzeme kaldırıyordu. Boru rayın ÖNÜNDE iniyor, rayı hiç geçmiyor.
        ray = kut(x0 + 6.0, x1 - 6.0, KAS[0] - 4.0, KAS[0], ZK[0], ZK[1])
        ekle("ray_%s" % k, ray, "sac", bom=None)
        for i, xx in enumerate((x0 + 20.0, x1 - 30.0)):
            ekle("konum_pimi_%s_%d" % (k, i), silz(xx + 5.0, KAS[0] + 20.0, 5.0, ZKAV[0], ZKAV[0] - 12.0), "celik", bom=None)
        # v5: BACA/HUNİ PARÇASI KALKTI (Kemal: "başka parça yok, direk kasetin kendi ucu pideye yaklaşıyor").
        # Ürünü kasetin KENDİ yuvarlak borusu indiriyor; boru kaset tabanının 100 mm altına iniyor ve
        # pidenin üst yüzüne 40 mm kala bitiyor. Modülde yalnız borunun geçtiği yarık var.
    # v9 · DOZAJ KOVANI: yalıtım deliğini baştan başa geçen paslanmaz boru. Üstü kasetin borusunun
    # ucuna denk geliyor (arada 1 mm hava), altı pidenin DUSME kadar üstünde bitiyor. Yalıtımı kapatan parça bu.
    for (x_, z_, r_), (ad, x0, x1, gen) in zip(DELIK, YUVA):
        kv = sily(x_, z_, r_ - 0.2, AGZ[1] + H.DUSME, hy0)                 # üstü iç kabuğun ALT yüzünde biter
        kv = kv.cut(sily(x_, z_, r_ - 1.4, AGZ[1] + H.DUSME - 1.0, hy0 + 1.0))
        ekle("dozaj_kovani_%s" % ad.replace(" ", "_"), kv, "sac", bom=None)
    # v11 · YUVA ETİKET PLAKASI: ürün adı KASETE değil MAKİNEYE yazılıyor. Kaset gövdeleri ortak
    # (ORTAK GÖVDE 140), ayırt eden şey içindeki vida — o yüzden "bu yuvaya ne girer" bilgisi yuvanın
    # kendisine ait. Plaka iç kabuğun ön rimine, kasetin ÜSTÜNE oturuyor; kaset takılıyken de okunur.
    for ad, x0, x1, gen in YUVA:
        pl = kut(x0 + 15.0, x1 - 15.0, ET_Y0, ET_Y1, ET_Z0, ET_Z1)
        ekle("yuva_etiketi_%s" % ad.replace(" ", "_"), pl, "sac", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_yuva_etiket", "Yuva etiket plakası", 6,
            "304 1,5 mm · baskılı ya da lazer kazıma", "ürün adı yuvanın üstünde; kaset gövdeleri ortak olduğu için ürün bilgisi makinede durur"),):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))
    for a_, ad_, n_, malz_, gor_ in (("_bom_kovan", "Dozaj kovanı", 6, "304 boru 1,2 mm · iç kabuğa kaynaklı", "yalıtım deliğini baştan başa geçer; kasetin borusu üstüne oturur, ürünü pidenin %.0f mm üstüne indirir" % H.DUSME),):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))

    for i, xx in enumerate([YUVA[0][1] - BOLME] + [y[2] for y in YUVA]):
        ekle("bolme_%d" % i, kut(xx, xx + BOLME, KAS[0], KAS[0] + 60.0, ZK[0], ZK[1]), "sac", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_kilavuz", "Yuva ayırıcı lama 3 × 60 × 325", 7, "304 lama, iç kabuğa kaynaklı", "kasetin iki yanını kılavuzlar; kaset ile arasında 2 mm boşluk"),
                                     ("_bom_ray", "Taban rayı", 6, "304 bükme, meme yarığı açık", "kaset üstünde kayar; altındaki yarıktan meme geçer"),
                                     ("_bom_pim", "Konum pimi Ø10", 12, "304 taşlanmış", "kaset arkada iki pimle merkezlenir → kavrama hizalanır"),
                                     ("_bom_huni", "— (baca parçası kalktı)", 0, "kasetin kendi borusu", "ürünü kasetin yuvarlak çıkış borusu pide üstüne %.0f mm kala indiriyor" % H.DUSME)):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))

    # ---------------- 6 · TAHRİK ×12 (kuru bölmede) ----------------
    R = H.S["tahrik"]; MO, RE, YA, KE = R["motor"], R["reduktor"], R["yatak"], R["kece"]
    for xm, yy, k in MIL:
        sok = silz(xm, yy, 22.0, ZKAV[0], ZKAV[0] - 26.0)
        sok = sok.cut(kut(xm - 19, xm + 19, yy - 3, yy + 3, ZKAV[0] + 1, ZKAV[0] - 20.0)).cut(kut(xm - 3, xm + 3, yy - 19, yy + 19, ZKAV[0] + 1, ZKAV[0] - 20.0))
        ekle("soket_" + k, sok, "pom", bom=None)
        ekle("yay_" + k, silz(xm, yy, 16.0, ZKAV[0] - 26.0, ZKAV[1]).cut(silz(xm, yy, 12.0, ZKAV[0] - 27.0, ZKAV[1] - 1.0)), "celik", bom=None)
        ekle("mil_" + k, silz(xm, yy, 11.0, ZKAV[1], ZBOL[1] - 40.0), "celik", bom=None)
        kov = silz(xm, yy, 30.0, ZBOL[0], ZBOL[1] - 18.0)
        kov = kov.cut(silz(xm, yy, YA["cap_dis"] / 2, ZBOL[0] - 1, ZBOL[0] + YA["z"]))
        kov = kov.cut(silz(xm, yy, KE["cap_dis"] / 2, ZBOL[1] - 18.0 - KE["z"], ZBOL[1] - 17.0))
        kov = kov.cut(silz(xm, yy, 11.2, ZBOL[0] + 1, ZBOL[1] - 19.0))
        ekle("kovan_" + k, kov, "pom", bom=None)
        # Mil gudugu koddaki 42 mm'den TASARIM degeri olan 40 mm'ye cekildi; gercek 79 mm'lik
        # redüktörle motor arka saci 0,5 mm deliyordu. 40 ile deliyor degil ama arkada
        # YALNIZ 1,5 mm kaliyor — servis bosluğu yok. Karar Kemal'de (asagidaki BOM notu).
        ekle("reduktor_" + k, suregear_koy(xm, yy, ZBOL[1] - 40.0), "motor", bom=None)
        zm = ZBOL[1] - 40.0 - 79.0 - 2.0                 # GERCEK redüktör boyu 79 mm (hesapta 60 varsayilmisti)
        _g, _kb = nema23_koy(xm, yy, zm)
        ekle("motor_" + k, _g, "motor", bom=None)
        ekle("motor_kablosu_" + k, _kb, "koyu", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_soket", "Yaylı haç soketi", 12, "POM-C + paslanmaz yay", "kaset takılınca haç kavramaya oturur; yay kursu 14 mm, diş kaçarsa kaset zorlanmaz"),
                                     ("_bom_mil", "Tahrik mili Ø22", 12, "AISI 304 taşlanmış", "yalıtımlı bölmeden geçer; soğuk tarafta soket, kuru tarafta redüktör"),
                                     ("_bom_kovan", "Yataklı-keçeli kovan", 12, "POM-C gövde + yatak ×2 + keçe 22×35×7", "mili bölmeden SIZDIRMAZ geçirir; soğuk hücreye nem girmez"),
                                     ("_bom_red", "Planet redüktör i = 10", 12, "PLF60/PLE60 sınıfı · eş eksenli", "sonsuz vida DEĞİL: girişi dik olduğu için motor yana taşıyordu"),
                                     ("_bom_motor", "AutomationDirect STP-MTR-23079 · NEMA23 · 1,95 N·m tutma · 2,8 A · DC · IP40 (GERÇEK CAD)", 12, "sürücüsüyle birlikte", "dozaj = mil açısı; kapalı çevrim adım kaçırmayı yakalar")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

    # ---------------- 7 · SOĞUTMA ----------------
    # v5 · SOĞUTMA PAKETİ KURU BÖLMEYE (Kemal: "standart versiyonunu bul, MOTORLARIN OLDUĞU YERE koy,
    # sonra içeriye soğuğu verecek şekilde YALITIMA BOŞLUK AÇ, içeri gitsin hava").
    # Hücrenin içinde artık hiçbir soğutma parçası yok. Fanlı evaporatör (unit cooler) kuru bölmede,
    # motorların üstünde duruyor; soğuk havayı arka yalıtımdaki ÜFLEME boşluğundan kavrama bölmesine basıyor,
    # oradan delikli perde hücreye yayıyor, dönüş yine yalıtımdaki alt boşluktan evaporatöre geliyor.
    # ÖLÇÜ: 400 × 180 × 190 (lamel paketi 140 + fan 50) — ticari sınıfın en küçük fanlı evaporatörü [V: yükümüz %.0f W, katalogdaki en küçük
    # unit cooler bile 300–500 W verir; kesin model seçilmedi]. Motorlar y 271–484'te, evaporatör 500'den başlıyor.
    EVX = (W / 2.0 - 200.0, W / 2.0 + 200.0)
    EVY = (500.0, 680.0)
    EVZ = (ZKURU[0] - 5.0, ZKURU[0] - 145.0)                                   # lamel paketi 140; fan arkasında 50
    ekle("evaporator", kut(EVX[0], EVX[1], EVY[0], EVY[1], EVZ[0], EVZ[1]), "bakir",
         bom=("Fanlı evaporatör (unit cooler) · YAPTIRILACAK", 1,
              "400 × 180 × 190 (lamel 140 + fan 50) · soğutmacı firma kurar",
              "KURU BÖLMEDE, motorların üstünde; soğuğu arka yalıtımdaki iki boşluktan hücreye verir · "
              "yük %.0f W, seçim %.0f W. RAFTAN ALINAN PARÇA DEĞİL: modelde YER ZARFI" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    ekle("fan_0", silz(W / 2.0, (EVY[0] + EVY[1]) / 2.0, 100.0, EVZ[1], EVZ[1] - 50.0), "motor",   # v25: fan evaporatöre oturur (v24: 3 mm boşluk)
         bom=("Evaporatör fanı Ø200", 1, "eksenel · EVAPORATÖRLE BİRLİKTE GELİR, ayrı alınmaz",
              "havayı evaporatörden çekip yalıtımdaki üfleme boşluğuna basar. Soğutma paketi "
              "yaptırılacağı için fan da o pakete dahil; modelde YER ZARFI"))
    for _i, (_xa, _ya) in enumerate(((EVX[0], EVY[0]), (EVX[1] - 30.0, EVY[0]), (EVX[0], EVY[1] - 30.0), (EVX[1] - 30.0, EVY[1] - 30.0))):
        ekle("evaporator_ayagi_%d" % _i, boru_z(_xa, _xa + 30.0, _ya, _ya + 30.0, -D + SAC, EVZ[1]), "celik",
             bom=("Evaporatör ayağı 30 × 30 × 2 AISI 304", 4, "boy %.1f · arka saca 2 × M6 kaynak saplama, evaporatör köşe flanşına M6" % (EVZ[1] + D - SAC),
                  "v25 · evaporatör (dünya x 1400–1800) v24'te havadaydı · soğuk hava TU v14 arka bölmedeki iki ağızdan (üfleme 1640–1685 · dönüş 1570–1610, TU y)") if _i == 0 else None)
    # Arka yalıtımdaki (pu_arka + iç kabuk arka yüzü) İKİ BOŞLUK: üstte üfleme, altta dönüş.
    # Miller y 300–455'te; iki boşluk da o bandın dışında kaldığı için hiçbir mile denk gelmiyor.
    ekle("_bom_kanal", kut(0, 0.1, 0, 0.1, 0, -0.1), "pu",
         bom=("Yalıtım boşluğu · üfleme + dönüş", 2, "PU panelde kesit, kenarları sac bilezikli", "üfleme %.0f × %.0f (y %.0f–%.0f) · dönüş %.0f × %.0f (y %.0f–%.0f) — kuru bölmedeki evaporatörü hücreye bağlar" % (UFL[1] - UFL[0], UFY[1] - UFY[0], UFY[0], UFY[1], UFL[1] - UFL[0], DNY[1] - DNY[0], DNY[0], DNY[1])))
    # v4 · HAVA PERDESİ (Kemal: "iceriye havayi vermiyor mu, kesikler aciliyor sacda — standardi bu degil mi").
    # Ticari soğutucu düzeni: evaporatör + fanlar arka bölmede bir PLENUM'un içinde, önlerinde delikli sac perde.
    # ÜST sıra kesiklerden soğuk hava hücreye basılır, ALT sıra kesiklerden (millerin altından) geri emilir.
    # Ayrı "hava kanalı saci" kalktı — perde onun işini yapıyor ve evaporatörü de gözden gizliyor.
    PZ0, PZ1 = ZKAV[0] - 1.0, ZKAV[0] - 2.5                                    # 1,5 mm perde sacı
    perde = kut(XI0 + SAC_IC, XI1 - SAC_IC, KAS[0], KAS[1], PZ0, PZ1)
    for x_, y_, k_ in MIL:                                                     # 12 mil/soket geçişi
        perde = perde.cut(silz(x_, y_, 25.0, PZ0 + 1.0, PZ1 - 1.0))
    for ad, x0_, x1_, gen_ in YUVA:                                            # 12 konum pimi geçişi
        for px in (x0_ + 25.0, x1_ - 25.0):
            perde = perde.cut(silz(px, KAS[0] + 20.0, 8.0, PZ0 + 1.0, PZ1 - 1.0))
    ust0, ust1 = EVY[0] + 6.0, EVY[1] - 6.0                                    # üfleme kesikleri (evaporatör hizası)
    alt0, alt1 = KAS[0] + 6.0, KAS[0] + 36.0                                   # dönüş kesikleri (millerin altı)
    xx = XI0 + SAC_IC + 30.0
    while xx + 14.0 < XI1 - SAC_IC - 30.0:                                     # 14 × 40 mm yarıklar, 40 mm arayla
        perde = perde.cut(kut(xx, xx + 14.0, ust0, ust1, PZ0 + 1.0, PZ1 - 1.0))
        perde = perde.cut(kut(xx, xx + 14.0, alt0, alt1, PZ0 + 1.0, PZ1 - 1.0))
        xx += 40.0
    ekle("hava_perdesi", perde, "sac", bom=("Hava perdesi · delikli sac", 1, "304 1,5 mm · lazer", "evaporatör bölmesini kapatır; üst kesiklerden soğuk hava girer, alt kesiklerden döner (ticari soğutucu düzeni)"))
    # v25 · TEKNİK CEP (dünya x 1520–2498,5 · y 1553,5–1860,5): parçalar TU v14 teknik ayırma sacının ÜSTÜNE oturur (dünya 1553,5 = yerel 661,5).
    #       v24'te y 1604'te havadaydılar ve montaj bunları V1_TASI ile x'te kaydırıyordu → v25: yeni adlarla SON yerlerinde (montaj sözlüğü etkisiz)
    TEK_TABAN = 1553.5 - DY_D
    TEK_TASI = TEK_TASIYICI_Y - DY_D                                             # v25b · taşıyıcı üstü (yatay sacın 31 üstü) — denetim_C bulgu 8: ağır parçalar 1,5 sac + PU üstündeydi
    for _i, (_za, _zv) in enumerate((((-90.0, -60.0), (-90.0, -87.0)), ((-208.0, -178.0), (-181.0, -178.0)))):
        _L = kut(821.5, W - SAC, TEK_TASI - 3.0, TEK_TASI, _za[0], _za[1]).union(kut(821.5, W - SAC, TEK_TABAN + 1.0, TEK_TASI - 3.0, _zv[0], _zv[1]))
        ekle("teknik_tasiyici_%d" % _i, _L, "celik",
             bom=("Teknik cep taşıyıcısı L 30 × 30 × 3 AISI 304", 2, "boy %.0f · uçlarda 3 mm alın plakası: sağda TC yan sacına 2 × M6, solda teknik ayırma dikey sacına 2 × M6 (dikey sac üstte TC tavanına kaynaklı)" % (W - SAC - 821.5),
                  "v25b · denetim_C bulgu 8: soğutma grubu (~15–20 kg, titreşimli) + pano yükü yan saclara · dik kol yatay sacın 1 mm ÜSTÜNDE biter → PU'ya yük yok") if _i == 0 else None)
    for _i, (_tx, _tz) in enumerate(((870.0, -75.0), (1130.0, -75.0), (870.0, -193.0), (1130.0, -193.0), (1200.0, -75.0), (1560.0, -75.0), (1200.0, -193.0), (1560.0, -193.0))):
        ekle("teknik_takoz_%d" % _i, sily(_tx, _tz, 10.0, TEK_TASI, TEK_TASI + TEK_TAKOZ), "silikon",
             bom=("Titreşim takozu Ø20 × 10 · M6 çift saplama (kauçuk, ör. silent-block tip A 40 Shore — parça no VARSAYIM)", 8, "soğutma grubu 4 + pano 4",
                  "v25b · taşıyıcıya + cihaz tabanına M6") if _i == 0 else None)
    ekle("teknik_sogutma_grubu", kut(850.0, 1150.0, TEK_TASI + TEK_TAKOZ, TEK_TASI + TEK_TAKOZ + 220.0, -60.0, -280.0), "motor",
         bom=("Soğutma grubu ⅕ HP · YAPTIRILACAK", 1, "hermetik, hava soğutmalı · soğutmacı firma kurar",
              "teknik cepte, 2 taşıyıcı + 4 titreşim takozu üstünde (v25b); önden T kapağının lazer yarıklarından emer (sol-alt), sağ-üstten atar. RAFTAN ALINAN PARÇA DEĞİL: "
              "modelde YER ZARFI, kesin marka/model firma seçince belli olacak (300 × 220 × 220)"))
    _pd = kut(1180.0, 1580.0, TEK_TASI + TEK_TAKOZ, TEK_TASI + TEK_TAKOZ + 240.0, -40.0, -290.0)
    _pi = kut(1181.5, 1578.5, TEK_TASI + TEK_TAKOZ + 1.5, TEK_TASI + TEK_TAKOZ + 238.5, -41.5, -288.5)
    ekle("teknik_pano_kutusu", _pd.cut(_pi), "sac",
         bom=("TOPPING panosu", 1, "304 · önden kapaklı, IP54", "PLC giriş/çıkış + röleler + sürücü beslemesi · v25b: 2 taşıyıcı + 4 titreşim takozu üstünde (M6)"))
    ekle("teknik_ups", din_parca(UPS_STEP, 1660.0, TEK_TASI, -40.0), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1,
              "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur; ön taşıyıcının üstünde, DIN rayında"))
    ekle("teknik_guc_kaynagi", din_parca(GUC_STEP, 1592.0, TEK_TASI, -40.0), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1,
              "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W" % H.S["elektrik"]["guc_kaynagi_W"]))
    ekle("teknik_din_rayi_ups", kut(1656.0, 1797.0, TEK_TASI, TEK_TASI + 35.0, -178.0, -170.5), "sac",          # v25b: taşıyıcı kotunda → UPS klipsi raya oturur (0,77 mm açıktı)
         bom=("DIN ray TS35 × 7,5 · UPS", 1, "EN 60715 · 141 mm", "v25 · dünya x 2356–2497 (v24 2340–2520: sağ yan sacı delip fırın bölgesine 20 mm taşıyordu)"))
    ekle("teknik_din_rayi_guc", kut(1590.0, 1654.0, TEK_TASI + 10.0, TEK_TASI + 45.0, -178.0, -162.8), "sac",
         bom=("DIN ray TS35 × 7,5 + 7,7 mm ara parça · güç kaynağı", 1, "EN 60715 · 64 mm", "güç kaynağı UPS'ten 7,7 mm sığ → ray ara parçayla öne alınır"))
    ekle("teknik_din_plakasi", kut(1588.0, 1797.0, TEK_TASI, TEK_TASI + 110.0, -180.0, -178.0), "sac",
         bom=("DIN montaj plakası 304 2 mm", 1, "209 × 110 · arka taşıyıcının üstüne L büküm + 2 × M6 (v25b)", "UPS + güç kaynağı raylarını taşır"))
    # v25 · KURU BÖLME SÜRÜCÜLERİ (4 kaset tahriki: kaşar + sucuk × 2 mil) · STP-DRV-4830 · DIN rayında, ray 2 ayakla arka saca
    _drv = cq.importers.importStep(SURUCU_STEP).val()
    _drv = _drv.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0)
    _db = _drv.BoundingBox()
    HATVE = 33.0
    SUR_Y, SUR_Z = 1432.0 - DY_D, -760.0                                       # dünya y 1432 (valf adasının sağı) · arka yüz = DIN ray yüzü z −760
    for i in range(4):
        xx = 480.0 + i * HATVE
        _d = _drv.translate(cq.Vector(xx - _db.xmin, SUR_Y - _db.ymin, SUR_Z - _db.zmin))
        ekle("kuru_surucu_%d" % i, cq.Workplane(obj=_d), "kart",
             bom=("Step sürücü · STP-DRV-4830", 4, "3 A/faz · 12-48 VDC · mikroadım · DIN ray",
                  "kaşar + sucuk kasetlerinin 4 mili (2 × helezon + 2 × rotor) · motor 2,8 A, sürücü 3,0 A (GERÇEK CAD) · UNO'lar pnömatik") if i == 0 else None)
    ekle("kuru_din_rayi_surucu", kut(470.0, 617.0, SUR_Y + 5.0, SUR_Y + 40.0, SUR_Z - 7.5, SUR_Z), "sac",
         bom=("DIN ray TS35 × 7,5 · sürücüler", 1, "EN 60715 · 147 mm", "kuru bölmede, dünya x 1170–1317"))
    for _i, _x0 in enumerate((478.0, 579.0)):
        ekle("kuru_din_rayi_ayak_%d" % _i, boru_z(_x0, _x0 + 30.0, SUR_Y + 7.5, SUR_Y + 37.5, -D + SAC, SUR_Z - 7.5), "celik",
             bom=("DIN ray ayağı 30 × 30 × 2 AISI 304", 2, "boy 61 · arka saca kaynak saplama", "v25 · sürücüler v24'te havadaydı") if _i == 0 else None)

    # ---------------- 8b · DÖNER TABLA — TAM ÜRETİM MODELİ (v10) ----------------
    # v9'a kadar 9 adet yer tutucu bloktu; parçaların hiçbiri birbirine bağlanmıyordu. Şema: X ekseni
    # KAYIŞ tahrikli tek araba, DÖNÜŞ ekseni araba plakasının altındaki pancake motorla EŞ EKSENLİ doğrudan.
    TB = H.S["tabla"]
    Xc = XC_TABLA                                                               # v20: modelde PARK KONUMUNDA çizilir (açıcının altı, strok x -350…1627)
    ZT = ZK[0] + 30.0                                                           # tabla ekseni (nozzle'dan z'de 20 mm geride)
    RT_ = TB["cap"] / 2.0

    # --- 8b.1 TAŞIYICI: tekne + kiriş merdiveni (1,5 mm saca lineer ray bağlanmaz) ---
    # v22: uzayan hareketin TAMAMI tasinir; sag motor ve sol avara da ayni teknededir.
    _TX0, _TX1 = XK_SOL - 40.0, 1795.0                                     # v24: tekne modülün içinde biter (duvar 1798,5); solda motor cebi
    tk = kut(_TX0, _TX1, 1.5, 4.5, -5.0, -415.0)
    tk = tk.union(kut(_TX0, _TX1, 1.5, 31.5, -5.0, -8.0)).union(kut(_TX0, _TX1, 1.5, 31.5, -412.0, -415.0))
    # X motoru arka taraftan takilir; teknenin arka kivriminda katalog motor zarfi kadar servis cebi.
    tk = tk.cut(kut(XK_SOL - 34.0, XK_SOL + 34.0, 0.5, 33.0, -416.0, -411.0))    # v24: motor servis cebi SOL uçta
    ekle("mekanizma_teknesi", tk, "sac", bom=("Mekanizma teknesi", 1, "304 3,0 mm · kenarları 30 kıvrık · %1,5 eğim",
         "ray kirişlerinin kaynaklandığı yapısal tekne; damlayanı tabla düzleminin ALTINDA toplar, ön-solda Ø25 tahliye"))
    for ad_, z0_, z1_, gen_ in (("on", -95.0, -35.0, 60.0), ("arka", -305.0, -245.0, 60.0)):
        ekle("ray_kirisi_%s" % ad_, kut(_TX0, _TX1, 4.5, 20.5, z0_, z1_), "celik",
             bom=("Ray kirisi 60 x 16 x %.0f" % (_TX1 - _TX0), 2, "304 lama · tekneye sürekli kaynak", "kaynaktan SONRA üç üst yüzey TEK BAĞLAMADA frezelenir (düzlemlik 0,1 mm/m — HGR15 şartı)") if ad_ == "on" else None)
    ekle("kayis_kirisi", kut(_TX0, _TX1, 4.5, 20.5, -385.0, -335.0), "celik",
         bom=("Kayış kirişi 50 × 16 × %.0f" % (_TX1 - _TX0), 1, "304 lama", "kayış kasnakları, avara ve gergi bunun üstünde · v24: modül içinde biter"))
    for i_, xb in enumerate((-520.0, -220.0, 80.0, 380.0, 680.0, 980.0, 1280.0, 1580.0, 1745.0)):   # v24: son lama 1745
        ekle("baglama_lamasi_%d" % i_, kut(xb, xb + 40.0, 4.5, 20.5, -335.0, -305.0), "celik",
             bom=("Baglama lamasi 40 x 16", 9, "304 lama", "arka ray kirişi ile kayış kirişini bağlar; dönüş motoru z −141…−198 bandında gezdiği için tam boy lama konulamıyor") if i_ == 0 else None)

    # --- 8b.2 LİNEER KIZAK ---
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        # v20: ray iki ucta da uzadi — solda acici (modul A), sagda banda aktarma
        _r, _n = hiwin_ray(H.RAY_X0, H.RAY_X1, zc_)
        ekle("lineer_ray_%s" % ad_, _r, "celik",
             bom=("Lineer ray HGR15 x %.0f" % H.RAY_UZUNLUK, 2, "paslanmaz sınıf [V: özel sipariş, fiyat/teslim sorulacak]", "HIWIN HGR15 GERÇEK profil (TraceParts STEP) · M4 havşa hatve 60 · 1,45 kg/m katalogla birebir") if ad_ == "on" else None)
    for i_, (xb, zc_) in enumerate([(Xc - 100.0, -65.0), (Xc + 100.0, -65.0), (Xc - 100.0, -275.0), (Xc + 100.0, -275.0)]):
        ekle("kizak_blogu_%d" % i_,
             cq.Workplane(obj=hiwin()["araba"].translate(cq.Vector(xb, 0.0, zc_))), "celik",
             bom=("Kızak bloğu HGH15CA", 4, "HIWIN HGH15CA GERÇEK CAD (TraceParts) · 0,18 kg · C 14,7 kN / C0 23,47 kN", "hatve 200 mm; araba plakası 4 × M4×5 dişle bağlanır (katalog B26 × C26)") if i_ == 0 else None)
    apl = kut(Xc - 150.0, Xc + 150.0, 48.5, 58.5, -25.0, -315.0).cut(sily(Xc, ZT, 23.0, 47.0, 60.0))
    ekle("araba_plakasi", apl, "celik", bom=("Araba plakası 300 × 290 × 10", 1, "304 · iki yuva TEK BAĞLAMADA işlenir (eş eksenlik 0,05)",
         "altında motor pilotu Ø38,1 H8, üstünde döner yatak yuvası; hafifletme cepli ~5,5 kg"))

    # --- 8b.3 DÖNÜŞ: yatak · ayar bileziği · göbek · tabla ---
    # v16: GERCEK katalog yatagi. Ø196,85 x 22,27 — tasarimda Ø160 varsayilmisti.
    _y = xu080149()["kati"].translate(cq.Vector(Xc, 58.5, ZT))
    ekle("doner_yatak", cq.Workplane(obj=_y), "celik",
         bom=("Çapraz makaralı döner yatak", 1, "Schaeffler (INA) XU080149 · Ø196,85 × 22,27 · GERÇEK CAD",
              "Ø340 konsol tablanın devirme momentini doğrudan alır; iç bilezik plakaya cıvatalı"))
    # AYAR BILEZIGI ZATEN BUNUN ICIN VAR (isleme araligi 2-14 mm): yatak 20 yerine 22,27
    # cikinca fazlaligi bilezik yutar, gobek ve tabla YERINDE KALIR. 7,5 -> 5,23 mm islenir.
    _ab = sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0))
    for i_ in range(3):                                                     # v20: kilit burcu delikleri
        a_ = math.radians(120.0 * i_ + 40.0)
        _ab = _ab.cut(sily(Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_), 7.0, 80.0, 87.0))
    ekle("ayar_bilezigi", _ab, "celik",
         bom=("Ayar bileziği · torna halka", 1, "304 · dış Ø210 iç Ø100 · kalınlık 5,23 — yatak Ø197 × 22,27 olunca büyüdü ve İNCELDİ (aralık 2–14)",
              "ray + blok + yatak katalog toleransının TAMAMI bu tek parçada toplanır; yedek dikey boşluk 7,5 mm"))
    gb = sily(Xc, ZT, 110.0, 86.0, 97.0).cut(sily(Xc, ZT, 30.0, 85.0, 98.0))
    for i_ in range(2):
        gb = gb.cut(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.1, 85.0, 92.0))                # tahrik pimi burçları
    ekle("tabla_gobegi", gb, "celik", bom=("Tabla göbeği Ø220 × 11", 1, "304 işlenmiş, cepli ~1,8 kg",
         "ayar bileziğine 3 × M8 saplama + paslanmaz KELEBEK SOMUN + 2 × Ø8 h7 konum pimi ile ALETSİZ sökülür"))
    # v20 · TEPSI YOK: robot parmak kesikleri KALDIRILDI. Hamur artik dogrudan bu
    # yuzeyde aciliyor; kesik olursa hamur delige girer.
    tb_ = sily(Xc, ZT, RT_, 97.0, 100.0)
    ekle("tabla", tb_, "sac", bom=("Döner tabla Ø340 × 3", 1, "304 · göbeğe sürekli TIG kaynak",
         "TAŞIYICI tabla — gıda yüzeyi DEĞİL; gıda yüzeyi üstündeki çalışma diski"))
    # v20 · CALISMA DISKI = gida yuzeyi. Tabla gobege kaynakli, sokulemiyor; yikanabilsin
    # diye ustune elle cikan disk kondu. Kenari 15 mm'de 2 mm'ye iner (soyma).
    # UST YUZ Ø340 BOYUNCA DUZ (y 108) — pide duz zeminde acilmali.
    # INCELME ALT YUZDE: son 15 mm'de taban 100 -> 106'ya cikar, kenar 2 mm kalir.
    _dsk = sily(Xc, ZT, RT_, 106.0, 108.0)                                  # tum disk 2 mm ust kabuk
    _dsk = _dsk.union(sily(Xc, ZT, RT_ - 15.0, 100.0, 106.0))               # ortada tam kalinlik
    _dsk = _dsk.union(koni_y_t(Xc, ZT, RT_, RT_ - 15.0, 100.0, 106.0))      # alt yuzde konik gecis
    for i_ in range(3):                                                     # pim delikleri
        a_ = math.radians(120.0 * i_)
        _dsk = _dsk.cut(sily(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 4.1, 99.0, 109.0))
    ekle("calisma_diski", _dsk, "pom",
         bom=("Çalışma diski Ø340 · 8 → 2", 1, "mat gıda UHMW-PE (ya da PU kaplı) · elle çıkar · yedekli",
              "GIDA YÜZEYİ: hamur burada açılır, malzeme buna dökülür, akşam sökülüp yıkanır. "
              "MAT olacak — cilalı yüzeyde koniler hamuru açmaz, yerinde döndürür. "
              "Kenar son 15 mm'de 2 mm'ye iner: pide soyularak ayrılır, sürüklenmez"))
    for i_ in range(3):
        a_ = math.radians(120.0 * i_)
        ekle("disk_pimi_%s" % "ABC"[i_], sily(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 4.0, 100.0, 108.0), "celik",
             bom=("Disk konum pimi Ø8 × 8", 3, "304 · tablaya H7/r6 presli",
                  "r = 100'de 120° aralıklı; çalışma diskini yerinde tutar (sıyrılırken kaymasın). "
                  "Diskle AYNI KOTTA biter — gıda yüzeyinde çıkıntı yok") if i_ == 0 else None)

    # --- 8b.4 DÖNÜŞ MOTORU (eş eksenli, i = 1) ---
    ekle("donus_motoru", kut(Xc - 28.5, Xc + 28.5, 4.5, 45.5, ZT - 28.5, ZT + 28.5), "motor",
         bom=("Dönüş motoru · NEMA23 PANCAKE", 1, "57 × 57 × 41 · kapalı çevrim step · ~0,9 N·m [V: tork eğrisi doğrulanacak]",
              "araba plakasının ALTINA 4 × M5 havşa, ekseni TABLA EKSENİYLE AYNI; redüktör ve kayış YOK · gereken 0,169 N·m → ~5 kat pay"))
    lk = sily(Xc, ZT, 15.0, 45.5, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))   # v25: motor mil yüzüne oturur (v24 0,5 boşluk)
    for i_ in range(2):
        lk = lk.union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.0, 66.0, 74.0))
    ekle("tahrik_lokmasi", lk, "celik", bom=("Tahrik lokması Ø30 × 20", 1, "304 torna · yarıklı sıkma + M5 pinç",
         "üstünde r = 10'da 2 × Ø8 pim; göbeğin altındaki burçlara girer — rijit kaplin YOK, tabla düşeyde ayrılabiliyor"))

    # --- 8b.5 X TAHRİK ZİNCİRİ (v22: TAM 1987 mm strok) ---
    # v21 hatasi: ray -500'e uzamisti fakat kayis x=52'de basliyordu; parkta (-350)
    # araba kayisa bagli degildi. Ayrica iki duz kosu Y yerine Z'de ayrilmisti.
    _KL, _KR, _KY, _KRAD = XK_SOL, XK_SAG, 33.0, H.KASNAK_R                  # v24: −560 / 1650
    ekle("x_tahrik_kasnagi", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.0, -369.0, -351.0)), "celik",   # v25: sıkma bilezikli → delik = mil
         bom=("GT3 kasnak 20 dis x 15", 1, "PD %.3f -> cevre TAM %.2f mm/tur; sikma bilezikli" % (2.0 * _KRAD, H.KASNAK_CEVRE), "x motorunun milinde"))
    # Motor STEP'inin mili zaten Z ekseninde. v21'de X etrafinda 90 derece
    # cevrilince mil Y'ye bakiyor ve govde kayisin icine giriyordu.
    # Motor teknenin ARKASINDA; gercek NEMA23 mili +Z yonunde kasnaga uzanir.
    # Boylece motor govdesi ne kayis kirisine ne de urun bolgesine girer.
    _mot_yuz = -397.5
    _mg = nema23()["govde"].translate(cq.Vector(_KL, _KY, _mot_yuz))         # v24: motor SOL uçta (park tarafı)
    ekle("x_motoru", cq.Workplane(obj=_mg), "motor",
         bom=("X motoru - NEMA23 kapali cevrim step", 1, "57 x 57 x 76 - %.1f N.m - 24 V - mil asagi" % H.X_MOTOR_TORK,
               "200 mm/s = 200 dev/dk; %.2f kg hareketli kutlede gereken %.3f N.m, motor payi %.1f kat" % (H.X_HAREKET_KUTLE, H.X_GEREKEN_TORK, H.X_TORK_PAY)))
    ekle("x_motor_mili", silz(_KL, _KY, 4.0, _mot_yuz, -352.5), "celik",
         bom=("X motor mili O8", 1, "motorun katalog mili + sikma bilezigi", "kasnak gobegine kadar kesintisiz; kasnak deligi O8,2"))
    _mk = kut(_KL - 45.0, _KL + 45.0, 4.5, 75.0, _mot_yuz, _mot_yuz + 8.0).cut(silz(_KL, _KY, 20.0, _mot_yuz - 1.0, _mot_yuz + 9.0))
    ekle("x_motor_kaidesi", _mk, "sac",
         bom=("X motor kaidesi", 1, "304 8 mm dik motor plakasi - tekneye 4 x M8", "motor teknenin arkasinda; mil servis cebinden kasnaga gelir"))
    ekle("avara_kasnak", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.0, -369.0, -351.0)), "celik",   # v25: rulman iç bileziği mile sıkı
         bom=("Avara kasnak GT3 20 dis x 15", 1, "flansli - icinde 2 x 625-2RS paslanmaz rulman", "v24: SAĞ uçta (1650); aktarmada kelepçe 1607'de biter"))
    # Avara plakasi kayis duzleminin arkasinda; onceki U braket iki kayis kosusunu kesiyordu.
    _agb = kut(_KR - 22.0, _KR + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KR, _KY, 4.0, -386.0, -376.0))   # v25: mil brakete sıkı (M8 gergi)
    ekle("avara_gergi_braketi", _agb, "celik",
         bom=("Avara + gergi braketi", 1, "304 10 mm - 16 mm yuvali 2 x M8 + M6 itme vidası + kontra", "gergi sol servis bolgesinden ayarlanir"))
    ekle("avara_mili", silz(_KR, _KY, 4.0, -385.0, -352.5), "celik",
         bom=("Avara mili O8", 1, "17-4PH - iki 625-2RS rulman", "gergi plakasindan kasnaga"))
    _bt = 1.5
    for i_, yc_ in enumerate((_KY - _KRAD - _bt / 2.0, _KY + _KRAD + _bt / 2.0)):
        ekle("x_kayisi_%d" % i_, kut(_KL, _KR, yc_ - _bt / 2.0, yc_ + _bt / 2.0, -367.5, -352.5), "koyu",
             bom=("X kayisi GT3-15 kapali cevrim %.0f mm" % (2.0 * (XK_SAG - XK_SOL) + H.KASNAK_CEVRE), 1, "celik kordlu poliuretan [V: tedarikci boyu dogrulayacak]", "iki kosu AYNI XY duzleminde; tum -350...1637 is strokunda kelepce kayis ustunde") if i_ == 0 else None)
    # Kasnak sarimlari: duz kosularin iki ucunu fiziksel olarak kapatir.
    for ad_, xx_, sol_ in (("sol", _KL, True), ("sag", _KR, False)):
        _sar = silz(xx_, _KY, _KRAD + _bt, -367.5, -352.5).cut(silz(xx_, _KY, _KRAD, -369.0, -351.0))
        _sar = _sar.intersect(kut(xx_ - 14.0 if sol_ else xx_, xx_ if sol_ else xx_ + 14.0, _KY - 14.0, _KY + 14.0, -368.0, -352.0))
        ekle("x_kayisi_sarim_" + ad_, _sar, "koyu")
    _yc = _KY + _KRAD + _bt / 2.0
    kol = kut(Xc - 150.0, Xc - 30.0, _yc + 4.5, _yc + 14.5, -385.0, -315.0).union(kut(Xc - 110.0, Xc - 70.0, _yc + _bt / 2.0 + 0.5, _yc + 4.5, -367.5, -352.5))   # v24: plakanın SOL yarısı
    ekle("kayis_kolu", kol, "celik", bom=("Kayis kolu - L", 1, "304 10 mm bukme - plakaya 4 x M8 + O6 pim", "ust kayis kosusunu araba plakasina baglar · v24: 120 boy, plakanın sol yarısında (sağ uç 2500'ü geçmesin)"))
    for i_, xb in enumerate((Xc - 130.0, Xc - 50.0)):
        ekle("kayis_kelepcesi_%d" % i_, kut(xb - 20.0, xb + 20.0, _yc - 4.5, _yc + 4.5, -371.0, -349.0).cut(kut(xb - 21.0, xb + 21.0, _yc - 1.0, _yc + 1.0, -368.0, -352.0)), "celik",
             bom=("Kayis kelepcesi", 2, "304 govde + GT3 dis profilli baski plakasi", "kapali kayisin ust kosusuna iki noktadan 2 x M5 + 2 x M4 ile baglanir") if i_ == 0 else None)

    # --- 8b.6 HİJYEN / KORUMA ---
    ap = kut(Xc - 190.0, Xc + 190.0, 58.5, 60.5, -5.0, -340.0).cut(sily(Xc, ZT, 85.0, 57.5, 61.5))
    ap = ap.cut(sily(Xc, ZT, 101.0, 40.0, 95.0))      # v16: Ø197 yatak + 2 mm bosluk
    ekle("siyirici_apron", ap, "sac", bom=("Sıyırıcı apron 380 × 335 × 2", 1, "304 · kenarı 10 kıvrık · elle çıkar",
         "tepsinin ayak izini birebir örter; dökülen kırıntı raylara ULAŞAMAZ"))
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        ct = kut(-520.0, 1790.0, 20.5, 44.0, zc_ - 30.0, zc_ + 30.0).cut(kut(-525.0, 1795.0, 19.5, 43.0, zc_ - 29.0, zc_ + 29.0))   # v25: etekler kirişin üstüne oturur (v24: 3 mm dışında, havada; çatısı yoktu)
        ct = ct.cut(kut(-525.0, 1795.0, 42.0, 45.0, zc_ - 18.0, zc_ + 18.0))                                                            # çatıda 36 yarık (araba geçer)
        for _y26, (_za, _zb) in (("a", (zc_ - 31.0, zc_ - 18.0)), ("b", (zc_ + 18.0, zc_ + 31.0))):     # v26: yarık boydan boya → 2 ayrı L şerit (v25: tek parça sanılıyordu)
            ekle("ray_ortu_catisi_%s_%s" % (ad_, _y26), ct.intersect(kut(-525.0, 1795.0, 19.0, 45.0, _za, _zb)), "sac",
                 bom=("Ray örtü şeridi · L 12 × 23,5", 4, "304 1,0 mm bükme · boy 2310 · iki şerit arası 36 yarık (araba geçer) · uçları açık (kızaklar örtünün ucuna 9 mm yaklaşır)",
                      "arabanın olmadığı yerde rayı örter; şerit başına 12 × M4 havşa") if (ad_, _y26) == ("on", "a") else None)
    ekle("kirinti_cekmecesi", kut(100.0, 1580.0, 4.5, 20.5, -240.0, -212.0).cut(kut(103.0, 1577.0, 6.5, 21.5, -237.0, -215.0)), "sac",
         bom=("Kırıntı çekmecesi", 1, "304 1,0 mm · önden çekilir", "iki ray kirişi arasında; boşaltılıp yıkanır"))
    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, SAC, SAC + 60.0, -500.0, -440.0).cut(kut(-517.0, 1787.0, SAC + 2.0, SAC + 61.0, -497.0, -443.0)), "sac",   # v25: tabana oturur (v24: 3 mm havada)
         bom=("Enerji zinciri + kanalı", 1, "iç 15 × 30 · R40 · boy ~840 · kanal 304 1,0 mm 60 × 60",
              "dönüş motoru arabayla gezdiği için ZORUNLU; içinde PUR kılıflı sürükleme-zinciri kablosu (PVC DEĞİL)"))

    # --- 8b.7 SENSÖRLER ve TAMPONLAR ---
    for ad_, xb in (("home", H.X_PARK), ("limit_sol", H.X_LIMIT_SOL), ("limit_sag", 1647.0)):            # v24: limit+ 1647 (tampon 1650)
        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Enduktif sensor M12 x 50 IP69K PNP NO", 3, "on ray kirisinin dis yuzune L braketle", "home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1647.0)) if ad_ == "home" else None)
        ekle("x_%s_sensor_braketi" % ad_, kut(xb - 8.0, xb + 8.0, 16.0, 22.0, -35.0, -19.0), "celik",
             bom=("Sensör braketi 304 3 mm · M12 kelepçeli", 3, "ön ray kirişinin ön yüzüne 2 × M4", "v25 · sensörler v24'te kirişin 10 mm önünde havadaydı") if ad_ == "home" else None)
    ekle("x_bayragi", kut(Xc - 30.0, Xc + 30.0, 40.0, 48.5, -30.0, -6.0), "sac",   # v25: plakanın altına 5 mm girer (kaynak) — v24: 1 mm önündeydi
         bom=("X bayrağı 60 × 25", 1, "304 3 mm", "araba plakasının ön kenarının altında"))
    # v20 · TABLA KILIDI: acma aninda konilerin artik torku tablayi cevirmesin.
    # Gereken 3-5 N.m, pancake motorun tutma torku 0,9 N.m — motor yetmiyor.
    for i_ in range(3):                                                     # burc: delik ayar bileziginde ACILIR
        a_ = math.radians(120.0 * i_ + 40.0)
        _bx, _bz = Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_)
        ekle("kilit_burcu_%d" % i_, sily(_bx, _bz, 7.0, 80.8, 86.0).cut(sily(_bx, _bz, 5.0, 80.0, 87.0)), "celik",
             bom=("Kilit burcu Ø14/Ø10", 3, "sertleştirilmiş 420 · ayar bileziğine presli",
                  "açıcının altında gövdeye bağlı pim buraya girer, tabla dönmez. "
                  "DOZAJ HIZINA DOKUNULMADI — kilit yalnız açma anında") if i_ == 0 else None)
    ekle("tabla_home_sensoru", sily(Xc, ZT - 128.0, 4.0, 66.5, 76.5), "koyu",
         bom=("Tabla home sensörü M8 endüktif IP67", 1, "araba plakasının ÜSTÜNDE braketli", "algılama yüzü YUKARI; arabayla birlikte gezdiği için sabit referansa gerek yok"))
    ekle("araba_plakasi_sensor_braketi", kut(Xc - 6.0, Xc + 6.0, 60.5, 66.5, ZT - 134.0, ZT - 122.0), "celik",
         bom=("Tabla home sensör ayağı 304", 1, "12 × 6 × 12 · apron + plakaya M4", "v25 · sensör v24'te apronun 6 mm üstünde havadaydı"))
    ekle("tabla_home_bayragi", sily(Xc, ZT - 128.0, 10.0, 85.0, 89.0).union(kut(Xc - 5.0, Xc + 5.0, 80.77, 85.0, ZT - 138.0, ZT - 105.0)), "celik",   # v25: bileziğe kaynaklı kol (göbeğin 1 mm altında)
         bom=("Tabla home bayrağı 3 × 20 × 12", 1, "304 · ayar bileziğine r = 128'de kaynaklı (yatak Ø197 olunca dışarı kaydı)", "boşluk 2,0 mm · robot tepsiyi hep aynı açıda bulmalı"))
    ekle("uc_tamponu_0", silz(H.X_LIMIT_SOL - 200.0, 53.5, 10.0, -80.0, -65.0), "silikon",
         bom=("Uç tamponu Ø20 × 15 (sol)", 1, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil"))
    ekle("uc_tamponu_0_braketi", kut(H.X_LIMIT_SOL - 210.0, H.X_LIMIT_SOL - 190.0, 20.5, 43.5, -82.0, -63.0), "celik",
         bom=("Uç tamponu braketi 304", 1, "20 × 23 × 19 · ön ray kirişinin üstüne 2 × M5", "v25 · tampon v24'te havadaydı"))
    # v24: SAĞ tampon kayış KOLUNA vurur (kol aktarmada 1607'de biter; tampon 1617–1629 → sert limit Xc 1650 = aktarma + 13)
    ekle("uc_tamponu_1", silx(_yc + 9.5, -372.5, 5.0, 1617.0, 1629.0), "silikon",
         bom=("Uç tamponu Ø10 × 12 (sağ)", 1, "poliüretan", "kayış KOLUNA vurur (kol y 48–58, kayışın üstünde) · gergi braketinin önündeki plakada · tekne 1795'te bittiği için plaka tamponu sığmadı"))
    ekle("uc_tamponu_plakasi", kut(1629.0, 1632.0, 45.0, 62.0, -377.0, -366.0), "celik",   # v25: braketin üst yüzüne oturur (v24: 1 mm)
         bom=("Tampon plakası 3 × 17 × 10", 1, "304 · gergi braketinin ön yüzüne kaynak", "kayış düzleminin (y ≤ 44) üstünde"))

    for a_, ad_, n_, malz_, gor_ in (
            ("_bom_tabla", "Tabla yasası", 1, "yazılım", "ağız pide merkezine %.0f mm'de 2,5 s bekler, r² doğrusal azalarak %.0f mm'ye iner, 0,3 s bekler [kasar_akis_model_v2]" % (TB["r_dis"], TB["r_ic"])),
            ("_bom_strok", "Strok ve istasyon", 1, "-", "tabla merkezi x %.0f...%.0f (%.0f mm) - park SOLDA - dozajda %.1f mm/s, geciste %.0f mm/s" % (H.X_PARK, H.X_AKTARMA, H.X_STROK, TB["x_doz_hiz"], TB["x_gecis_hiz"])),
            ("_bom_cevrim", "Cevrim", 1, "-", "uzayan strok dahil sure receteye gore sim_makine_v6 tarafindan hesaplanir; doz yasasi 10 s / urun DEGISTIRILMEDI"),
            ("_bom_civata", "Bağlantı elemanları (tümü A4/A2 paslanmaz)", 180, "15 tip · gıdaya bakan her baş HAVŞA ya da KUBBE",
             "ray 54 × M4×16 · blok 16 × M4×20 · yatak 8 × M5×16 · ayar bileziği 6 × M5×16 · göbek 3 × M8×40 saplama + kelebek somun + 2 pim · dönüş motoru 4 × M5×20 · kayış kolu 4 × M8×25 + 2 pim · kelepçe 4 × M5 + 4 × M4 · X motoru 4 × M5×12 + kaide 4 × M8×25 · avara M8×40 + braket 2 × M8×25 + M6 jack · apron 8 × M4×10 · çatı 24 × M4×8 · sensör 12 × M4×12 · zincir 18 · tampon 2 takım M10")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

    # ---------------- 8d · ACICI — KONILI DONER ACICI (v21) ----------------
    import math as _m
    AC_X, AC_Z = XC_TABLA, ZT
    AC_TEPE = 108.0 + 8.0                       # tepe: disk ustu + pide kalinligi
    AC_L, AC_RB = 140.0, 45.0                   # boy = pide yaricapi · taban yaricapi
    AC_ACI = _m.degrees(_m.atan2(AC_RB, AC_L))  # 17,82 derece

    def _koni(yon):
        """tepesi tabla ekseninde, alt cizgisi YATAY koni. yon=+1 one, -1 arkaya"""
        p0 = cq.Vector(AC_X, AC_TEPE, AC_Z)
        p1 = cq.Vector(AC_X, AC_TEPE + AC_RB, AC_Z + yon * AC_L)
        v = p1 - p0
        k = (cq.Workplane("XY").circle(0.4).workplane(offset=v.Length)
             .circle(AC_RB).loft(ruled=True).val())
        eks = cq.Vector(0, 0, 1).cross(v)
        aci = _m.degrees(_m.acos(max(-1.0, min(1.0, cq.Vector(0, 0, 1).dot(v) / v.Length))))
        if eks.Length > 1e-9:
            k = k.rotate(cq.Vector(0, 0, 0), eks, aci)
        return cq.Workplane(obj=k.translate(p0)), p1

    # z bantlari: her parcanin kendi yeri var, ic ice girmiyorlar

    def _birim(v_):
        l_ = v_.Length
        return cq.Vector(v_.x / l_, v_.y / l_, v_.z / l_)

    def _yonlendir(sh_, hedef_, nokta_):
        """Yerel +Z eksenini hedefe cevirir, sonra nokta_ konumuna tasir."""
        h_ = _birim(hedef_)
        z_ = cq.Vector(0.0, 0.0, 1.0)
        eks_ = z_.cross(h_)
        ac_ = _m.degrees(_m.acos(max(-1.0, min(1.0, z_.dot(h_)))))
        if eks_.Length > 1e-9:
            sh_ = sh_.rotate(cq.Vector(0, 0, 0), eks_, ac_)
        elif z_.dot(h_) < 0.0:
            sh_ = sh_.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180.0)
        return sh_.translate(nokta_)

    def _eksen_silindir(p_, u_, r_, boy_):
        return cq.Workplane(obj=cq.Solid.makeCylinder(r_, boy_, p_, u_))

    # ---- v25 (SPEC_on_duzlem_v63 §2.3): ÖN TAHRİK DİK AÇILI · KAFA ÖN UCU ≤ +10 · HİÇBİR AÇICI PARÇASI +39'U GEÇMEZ · KİNEMATİK AYNI ----
    # Koniler (_koni) v24 ile BİREBİR: tepe (AC_X, AC_TEPE, AC_Z) · yarı açı 17,82° · boy 140 · taban Ø90. v24'te ön motor + planet redüktör koni
    # ekseninde dışarı uzuyor, +166,6'ya çıkıyordu (kafa plakası +180). v25: ön koni Motovario NMRV030 sonsuz vida redüktörünün DELİK MİLİNE geçer,
    # motor sonsuz vida ekseninde (koni eksenine dik, düşeyden 17,82° geride) YUKARI bakar; redüktör çıkış yatakları koniyi taşır (ayrı yatak yok).
    AC_FI = -AC_ACI                                                         # yerel (a: koni ekseni · b: dik yukarı-geri · c: x) → X ekseni etrafında
    for i_, yon in enumerate((1.0, -1.0)):
        ad_ = "on" if yon > 0 else "arka"
        _k, _p1 = _koni(yon)
        _p0 = cq.Vector(AC_X, AC_TEPE, AC_Z)
        _u = _birim(_p1 - _p0)                    # koniden disariya dogru ortak eksen
        ekle("acici_konisi_" + ad_, _k, "celik",
             bom=("Acici konisi - boy 140 - taban O90", 2,
                  "304 taslanmis, mat kumlu - yari aci 17,82 derece",
                  "Tepesi tabla ekseninde; tabaninda M18 dis yuva, mil yuzden vidalanir") if i_ == 0 else None)
        if yon > 0:
            _v = cq.Vector(0.0, _u.z, -_u.y)                                 # sonsuz vida / motor ekseni (yukarı-geri)
            _yer = lambda sh_: sh_.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), AC_FI).translate(_p1)
            _t = _yer(cq.Vertex.makeVertex(0.0, 0.0, 1.0)).toTuple()
            assert abs(_t[1] - _p1.y - _u.y) < 1e-6 and abs(_t[2] - _p1.z - _u.z) < 1e-6, "yerel eksen koni eksenine oturmadı"
            _bx = lambda c0, c1, b0, b1, a0, a1: cq.Solid.makeBox(c1 - c0, b1 - b0, a1 - a0, cq.Vector(c0, b0, a0))
            _cz = lambda r, a0, a1: cq.Solid.makeCylinder(r, a1 - a0, cq.Vector(0, 0, a0), cq.Vector(0, 0, 1))
            NM = dict(ac=30.0, a=(8.0, 52.0), b=(-40.0, 40.0), c=(-28.0, 44.0), hub_r=17.5, hub=(3.0, 57.0), delik=7.0, H=30.0, E=55.0, G=56.0)
            _red = _bx(NM["c"][0], NM["c"][1], NM["b"][0], NM["b"][1], NM["a"][0], NM["a"][1]).fuse(_cz(NM["hub_r"], NM["hub"][0], NM["hub"][1]))
            _red = _red.fuse(_bx(NM["H"] - NM["G"] / 2.0, NM["H"] + NM["G"] / 2.0, NM["b"][1], NM["E"], NM["ac"] - NM["G"] / 2.0, NM["ac"] + NM["G"] / 2.0))
            _red = _red.cut(_cz(NM["delik"], NM["hub"][0] - 1.0, NM["hub"][1] + 1.0))
            ekle("acici_reduktoru_on", cq.Workplane(obj=_yer(_red)), "motor",
                 bom=("Açıcı ön redüktörü · SONSUZ VİDA Motovario NMRV030 i = 7,5 · NEMA23 giriş flanşlı", 1,
                      "delik mil Ø14 H8 · eksen aralığı 30 · 54 (C) × 80 (A) · maks. çıkış 18 N·m · radyal 0,86 kN [K: Oyostepper NMRV30-G15-D9 föyü] · dış ölçüler VARSAYIM (Motovario katalog tablosu, föy indirilmedi)",
                      "koni mili delik mile geçer (kamalı) · çıkış yatakları koniyi taşır · motor sonsuz vida ekseninde yukarı bakar → kafa önü +32 (v24 +166)"))
            _mil = _cz(9.0, 0.0, 3.0).fuse(_cz(NM["delik"], 3.0, NM["hub"][1] + 2.0))
            ekle("acici_mili_on", cq.Workplane(obj=_yer(_mil)), "celik",
                 bom=("Açıcı ön mili Ø18 / Ø14 × 59 (kademeli)", 1, "17-4PH taşlanmış · Ø14 kamalı + segman", "koni tabanından redüktörün delik miline"))
            _mot = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0).translate(cq.Vector(NM["H"], NM["E"], NM["ac"]))
            ekle("acici_motoru_on", cq.Workplane(obj=_yer(_mot)), "motor",
                 bom=("Açıcı ön motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m · 2,8 A · GERÇEK CAD",
                      "redüktörün giriş flanşında, düşeyden 17,82° geride yukarı bakar · koni 114 d/dk → motor 855 d/dk · çıkış ≈ 6 N·m (VARSAYIM: 855 d/dk'da 1,0 N·m × 7,5 × η 0,8)"))
            _P = lambda a, b: _p1 + _u.multiply(a) + _v.multiply(b)
            _pts = [(_P(12.0, -30.0).y, _P(12.0, -30.0).z), (_P(48.0, -30.0).y, _P(48.0, -30.0).z), (_P(48.0, 36.0).y, _P(48.0, 36.0).z),
                    (250.0, _P(48.0, 36.0).z), (250.0, _P(12.0, 36.0).z), (_P(12.0, 36.0).y, _P(12.0, 36.0).z)]
            ekle("acici_askisi_on", cq.Workplane("YZ", origin=(AC_X + NM["c"][0] - 8.0, 0, 0)).polyline(_pts).close().extrude(8.0), "celik",
                 bom=("Açıcı ön redüktör askısı 304 8 mm", 1, "lazer · redüktörün yan yüzüne 4 × M6, üstte kafa plakasına 3 × M8", "redüktörü (ve koniyi) kafa plakasına asar; tork kolu"))
            continue
        # ARKA: v24 ile aynı (planet redüktör + motor koni ekseninde) · v25: yatak mile sıkı, askı plakası yatağa oturur
        _mil_boy = 54.0
        ekle("acici_mili_" + ad_, _eksen_silindir(_p1, _u, 9.0, _mil_boy), "celik",
             bom=("Acici arka mili O18 x 54", 1, "17-4PH taslanmis - M18 omuzlu", "koni, rulman ve reduktor cikisini AYNI eksende baglar"))
        _py = _p1 + _u.multiply(8.0)
        _yat = cq.Solid.makeCylinder(24.0, 10.0, _py, _u).cut(cq.Solid.makeCylinder(9.0, 12.0, _py - _u.multiply(1.0), _u))
        ekle("acici_yatagi_" + ad_, cq.Workplane(obj=_yat), "celik",
             bom=("Acici yatagi - flansli O18", 1, "paslanmaz govde - gida gresi - ic bilezik mile sikı (v25)", "koni tabaninin 8 mm disinda"))
        _pp = _p1 + _u.multiply(18.0)                                        # v25: 18,5 → 18 (yatak yüzüne oturur)
        _pl = cq.Workplane("XY").rect(72.0, 72.0).circle(9.2).extrude(8.0).val()
        _aski = _yonlendir(_pl, _u, _pp)
        _pc = _p1 + _u.multiply(22.0)
        for _sx in (-30.0, 30.0):
            _pa = _pc + cq.Vector(_sx, 0.0, 0.0)
            _pb = cq.Vector(_pa.x, 250.0, _pa.z)
            _vv = _pb - _pa
            _aski = _aski.fuse(cq.Solid.makeCylinder(3.5, _vv.Length, _pa, _birim(_vv)))
        ekle("acici_askisi_" + ad_, cq.Workplane(obj=_aski), "celik",
             bom=("Acici arka yatak askisi", 1, "304 - 72 x 72 x 8 plaka + 2 x O7 gergi", "rulman flansi 4 x M8; gergiler kafa plakasina M8 somunla"))
        _q_red = _p1 + _u.multiply(_mil_boy)
        _red = _yonlendir(suregear()["tum"], _u.multiply(-1.0), _q_red)
        ekle("acici_reduktoru_" + ad_, cq.Workplane(obj=_red), "motor",
             bom=("Acici arka reduktoru - planet", 1, "SureGear PGCN23-1025 GERCEK CAD", "cikis yuzu mile temas eder; eksen koniyle birebir aynidir"))
        _q_mot = _q_red + _u.multiply(79.0)
        _mot = _yonlendir(nema23()["govde"], _u.multiply(-1.0), _q_mot)
        ekle("acici_motoru_" + ad_, cq.Workplane(obj=_mot), "motor",
             bom=("Acici arka motoru - NEMA23 STP-MTR-23079", 1, "1,95 N.m - 2,8 A - GERCEK CAD", "iki koni ters yonde doner"))

    # v25 · KAFA PLAKASI: arka kısım x ±80 (z −570…−67) + ön dil x −80…−4 (z −67…+10, ön motorun solunda) · ön ucu +10 (v24 +180, taşıyıcısız 170 mm uzantı)
    _kp = kut(AC_X - 80.0, AC_X + 80.0, 250.0, 262.0, -570.0, -67.0).union(kut(AC_X - 80.0, AC_X - 4.0, 250.0, 262.0, -67.0, 10.0))
    ekle("acici_kafa_plakasi", _kp, "sac",
         bom=("Açıcı kafa plakası 12 mm (L)", 1, "304 lama · frezelenmiş · 160 × 503 + 76 × 77 dil",
              "iki koni takımı buna asılı · arka ucu Z adaptör plakasına kaynak + 2 nervür · ön ucu +10 (SPEC ≤ +10)"))
    for _i, _xr in enumerate((AC_X - 78.0, AC_X + 70.0)):
        ekle("acici_kafa_plakasi_nervur_%d" % _i, kut(_xr, _xr + 8.0, 262.0, 302.0, -570.0, -200.0), "sac",
             bom=("Kafa plakası nervürü 8 × 40 × 370", 2, "304 lama · kaynak", "580 mm konsolun sehimini sınırlar") if _i == 0 else None)
    # v25 · Z EKSENİ: kolonun ön yüzünde 2 × HGR15 ray (x ±30) · 4 × HGH15CA araba · 12 mm adaptör plaka → kafa plakası (v24: kızak ↔ kafa 30 mm boşluk, kafa havadaydı)
    _t26 = 4.0                                                                                   # v26: kutu profil et kalınlığı [VARSAYIM · katalog]
    _kol26 = kut(AC_X - 60.0, AC_X + 60.0, 0.0, 612.0, -660.0, -610.0).cut(kut(AC_X - 60.0 + _t26, AC_X + 60.0 - _t26, -1.0, 613.0, -660.0 + _t26, -610.0 - _t26))
    _kol26 = _kol26.union(kut(AC_X - 60.0 + _t26, AC_X + 60.0 - _t26, 0.0, 10.0, -660.0 + _t26, -610.0 - _t26))     # alt uç plakası 10 (içeride, kaynaklı, 4 × M10 dişli)
    ekle("acici_kolonu", _kol26
         .union(kut(AC_X - 45.0, AC_X + 45.0, 582.0, 612.0, -660.0, -505.0)), "sac",
         bom=("Açıcı kolonu", 1, "304 kutu profil 120 × 50 × 4 (et VARSAYIM) · boy 612 · içte 10 mm alt uç plakası (4 × M10 dişli) + üst kol 90 × 30 × 155 kaynaklı · tabana (kaide A) alttan 4 × M10 · Z rayları ön duvara M4 perçin somunla",
              "Z raylarını ve pnömatik silindiri taşır; rayın ARKASINDA durur, arabanın yolunu kesmez"))
    for _i, _xr in enumerate((AC_X - 30.0, AC_X + 30.0)):
        ekle("acici_z_kizagi_%d" % _i, kut(_xr - 7.5, _xr + 7.5, 110.0, 470.0, -610.0, -595.0), "celik",
             bom=("Açıcı Z rayı HIWIN HGR15R × 360", 2, "katalog kesit 15 × 15 · M4 × 16 hatve 60", "kolonun ön yüzüne · kafa stroku 100 (0 = çalışma)") if _i == 0 else None)
        for _j, _yb in enumerate((190.0, 280.0)):
            _blk = kut(_xr - 17.0, _xr + 17.0, _yb, _yb + 61.4, -605.7, -582.0).cut(kut(_xr - 7.5, _xr + 7.5, _yb - 1.0, _yb + 62.4, -611.0, -595.0))
            ekle("acici_askisi_z_blogu_%d" % (2 * _i + _j), _blk, "celik",
                 bom=("Z arabası HIWIN HGH15CA", 4, "katalog W 34 · L 61,4 · H 28 (kutu model)", "adaptör plakasına 4 × M4") if _i == 0 and _j == 0 else None)
    ekle("acici_askisi_z_adaptoru", kut(AC_X - 60.0, AC_X + 60.0, 180.0, 350.0, -582.0, -570.0), "sac",
         bom=("Z adaptör plakası 304 12 mm", 1, "120 × 170 · 4 arabaya 16 × M4", "kafa plakası + nervürler buna kaynaklı"))
    ekle("acici_pnomatigi", kut(AC_X - 22.5, AC_X + 22.5, 388.0, 582.0, -562.5, -517.5).cut(sily(AC_X, -540.0, 6.0, 387.0, 583.0)), "koyu",
         bom=("Açıcı pnömatiği · Festo DSBC-32-100-PPVA-N3 (ISO 15552, Ø32, strok 100)", 1,
              "gövde 45 × 45 × 194 · WH 26 · mil Ø12 M10×1,25 · arka flanş FNC-32 ile kolonun üst koluna dik asılı · 6 bar'da 482 N itme",
              "kafayı indirir / 100 mm kaldırır (top girerken 90 gerekir; v24: Ø32 strok 60, z ekseninde çizilmiş, kolona bağlı değildi)"))
    ekle("acici_askisi_piston_mili", sily(AC_X, -540.0, 20.0, 262.0, 270.0).union(sily(AC_X, -540.0, 6.0, 270.0, 400.0)), "celik",
         bom=("Piston mili ucu + mil flanşı Ø40", 1, "DSBC mili (Ø12) + Festo FK-M10×1,25 esnek bağlantı + flanş", "kafa plakasına 4 × M6"))

    # ---------------- 8c · BANDA AKTARMA (v20) ----------------
    # Tepsi kalkinca pideyi tabladan almak yeni bir is oldu. EK MAKINE YOK.
    # Tabla ilerler, pidenin on kenari 0,3 mm'lik pahtan sabit KOPRUYE ciker;
    # firin bandi (bicak burunlu, yuzeyi ayni kotta) pideyi CEKER.
    # Tabla bant burnunun ALTINA GIRMEZ — bant burnu diskin kotunda, arada bosluk.
    AKT_Y = 106.0                                               # BANDIN UST YUZU (diskin 2 mm alti)
    AKT_X0, AKT_X1 = 1815.0, 2195.0                             # burun silindiri … tahrik silindiri
    # burun x 1815: modulun cikis yarigi cercevesi 1792-1798,5'te bitiyor, bant onun
    # DISINDA duruyor. Tabla aktarma konumunda (x 1637) diskin kenari 1807'de —
    # burna 8 mm kala duruyor, pide o bosluğu kendi govdesiyle kopruluyor.
    # KOPRU YALNIZ PIDENIN GENISLIGINI ORTER (Ø280 -> ZT +- 140), cunku ZT-180
    # bolgesinde X TAHRIK MOTORU var. 5 mm pay ile ZT +- 145.
    AKT_Z0, AKT_Z1 = ZT - 145.0, ZT + 145.0
    # ---- FIRIN BANDI · BICAK BURUNLU AKTARMA (v21) ----
    BR_R, BT_R, BANT_K = 10.0, 30.0, 1.5
    BR_Y = AKT_Y - BANT_K - BR_R
    BT_Y = AKT_Y - BANT_K - BT_R
    BZ0, BZ1 = AKT_Z0, AKT_Z1
    _burun = silz(AKT_X0, BR_Y, BR_R, BZ0, BZ1).union(silz(AKT_X0, BR_Y, 6.0, BZ0 - 35.0, BZ1 + 25.0))   # v23: ön mil ucu z 0 (ön yüzü geçmez)
    ekle("bant_burun_silindiri", _burun, "celik",
         bom=("Bant burun silindiri O20 x 290 + O12 mil", 1, "304 - iki ucta flansli rulman",
               "bicak burun; bant yuzeyi tablanin kenarina 8 mm kala baslar"))
    _tahrik = silz(AKT_X1, BT_Y, BT_R, BZ0, BZ1).union(silz(AKT_X1, BT_Y, 10.0, BZ0 - 35.0, BZ1 + 25.0))   # v23: ön mil ucu z 0
    ekle("bant_tahrik_silindiri", _tahrik, "celik",
         bom=("Bant tahrik silindiri O60 x 290 + O20 mil", 1, "304 - kaucuk kapli",
               "bandi ceker; devri firindaki pisirme suresini belirler"))
    _dis = (silz(AKT_X0, BR_Y, BR_R + BANT_K, BZ0, BZ1)
            .union(silz(AKT_X1, BT_Y, BT_R + BANT_K, BZ0, BZ1))
            .union(kut(AKT_X0, AKT_X1, AKT_Y - BANT_K, AKT_Y, BZ0, BZ1))
            .union(cq.Workplane("XY").polyline([(AKT_X0, BR_Y - BR_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R),
                                                (AKT_X0, BR_Y - BR_R)]).close()
              .extrude(BZ1 - BZ0).translate((0.0, 0.0, BZ0))))
    _ic = (silz(AKT_X0, BR_Y, BR_R, BZ0 - 1.0, BZ1 + 1.0)
           .union(silz(AKT_X1, BT_Y, BT_R, BZ0 - 1.0, BZ1 + 1.0))
           .union(kut(AKT_X0, AKT_X1, BR_Y - BR_R, AKT_Y - BANT_K, BZ0 - 1.0, BZ1 + 1.0)))
    ekle("bant", _dis.cut(_ic), "koyu",
         bom=("Firin bandi - 290 genis - kapali cevrim", 1,
               "gida onayli PTFE kapli cam elyaf orgu - 1,5 mm",
               "ust kosu y 106; calisma diskinin 2 mm altinda"))
    ekle("bant_tasiyici_saci", kut(AKT_X0 + 20.0, AKT_X1 - 40.0, AKT_Y - BANT_K - 4.0,
                                   AKT_Y - BANT_K - 1.0, BZ0 + 5.0, BZ1 - 5.0), "sac",
         bom=("Bant tasiyici saci", 1, "304 3 mm - ustu taslanmis", "ust kosu yuk altinda sarkmasin"))
    for i_, (z0_, z1_) in enumerate(((BZ0 - 35.0, BZ0 - 25.0), (BZ1 + 15.0, BZ1 + 25.0))):   # v23: ön sac z −10…0 (v22: 0…+10, ön yüzden taşıyordu)
        _ys = kut(1802.0, AKT_X1 + 45.0, 34.0, AKT_Y + 18.0, z0_, z1_)   # v23: alt kenar 21 → 34 (tekne dudağının üstü)
        _ys = _ys.cut(silz(AKT_X0, BR_Y, 6.2, z0_ - 1.0, z1_ + 1.0))
        _ys = _ys.cut(silz(AKT_X1, BT_Y, 10.2, z0_ - 1.0, z1_ + 1.0))
        ekle("bant_yan_saci_%d" % i_, _ys, "sac",
             bom=("Bant yan saci", 2, "304 10 mm - lazer - iki rulman yuvasi",
                  "bant genisliginin disinda; roller yalniz mil ucuyla deliklerden gecer") if i_ == 0 else None)
    # v23: motor tahrik makarasıyla EŞ EKSENLİ, bandın ARKASINDA. nema23 gövdesi mil yüzünden −z'ye uzar: mil yüzü arka yan
    # sacın dış yüzünün (BZ0 − 35) 2 mm arkasında → mil (+z) makara miline bakar. v22'de ön yüzün 21–78 mm önündeydi,
    # havadaydı ve x ekseninde 90° döndürülmüştü (mili dikey) — Kemal'in "köşedeki çıkıntı" dediği parça.
    _bm = nema23()["govde"]
    ekle("bant_motoru", cq.Workplane(obj=_bm.translate(cq.Vector(AKT_X1, BT_Y, BZ0 - 37.0))), "motor",
         bom=("Bant motoru · NEMA23 + planet i = 20", 1, "STP-MTR-23079 (GERÇEK CAD)",
              "bant hızı = fırın pişirme süresi; reçeteye göre değişir"))
    ekle("bant_ayagi", kut(AKT_X1 - 70.0, AKT_X1 + 10.0, 0.0, BT_Y - BT_R - BANT_K - 2.0, BZ0 + 30.0, BZ1 - 30.0), "sac",
         bom=("Bant ayağı", 1, "304 kutu profil · ayarlı taban",
              "bandın fırın tarafındaki ucunu taşır; TOPPING'e bağlı değil, bağımsız durur"))
    ekle("cikis_yarigi_contasi", kut(1792.0, 1798.5, 92.0, 150.0, AKT_Z0 - 10.0, AKT_Z1 + 10.0)
         .cut(kut(1791.0, 1799.5, AKT_Y - 4.0, 146.0, AKT_Z0 - 2.0, AKT_Z1 + 2.0)), "silikon",   # v23: açıklık 24 → 44 mm
         bom=("Çıkış yarığı çerçevesi + fırça", 1, "304 çerçeve + gıda tipi fırça sızdırmaz",
              "açıklık 294 × 44 (en yüksek ürün 28,5 + 9,5 pay); pide geçer, soğuk hava ve kir geçmez"))
    ekle("sensor_braketi_tabla_bos", kut(1642.0, 1658.0, 190.0, 217.0, ZT - 8.0, ZT + 8.0), "celik",
         bom=("Tabla boş sensörü askısı 304", 1, "16 × 27 × 16 · soğuk paketin alt sacına (TU v14 alt_yalitim_saci, dünya 1109) 2 × M4", "v25 · sensör v24'te havadaydı"))
    ekle("tabla_bos_sensoru", sily(1650.0, ZT, 9.0, 150.0, 190.0), "koyu",
         bom=("Tabla boş mu sensörü · lazer mesafe", 1, "IP67 · 50-300 mm · analog",
              "aktarmadan sonra bakar: temiz disk düz yüzey, pide 8-10 mm — farkı görür. "
              "Pide kalmışsa bir kez daha denenir, olmazsa fire silecegine gidilir"))
    # CIZIMDE GERI CEKILMIS KONUMDA: indirilmis halde cizilirse tabla her gecisinde
    # ona carpar. Calisma yuksekligi y 108 (diske deger), park yuksekligi y 125.
    FS_X = 770.0                                                                   # v25: montajın V1_TASI +520 kaydırması buraya işlendi (dünya x 1470–1490) · yeni ad
    ekle("fire_silecegi_silindiri", sily(FS_X + 10.0, ZT, 7.5, 180.0, 217.0).union(sily(FS_X + 10.0, ZT, 2.5, 167.0, 180.0)), "koyu",
         bom=("Fire sileceği silindiri · SMC CJ2B10-20 (Ø10, strok 20)", 1, "paslanmaz mini silindir · valf adasının yedek çıkışı · gövde boyu VARSAYIM",
              "sileceği 125 → 108'e indirir (17 mm) · soğuk paketin alt sacına (dünya 1109) flanşla asılı · v24'te '24 V aktüatör' yazıyordu, parça yoktu"))
    for _i, _zc in enumerate((ZT - 160.0, ZT + 150.0)):
        ekle("fire_silecegi_kilavuzu_%d" % _i, sily(FS_X + 10.0, _zc, 3.0, 167.0, 217.0), "celik",
             bom=("Silecek kılavuz mili Ø6 + POM burç", 2, "304 taşlanmış", "sileceği dönmeden indirir") if _i == 0 else None)
    ekle("fire_silecegi_lastigi", kut(FS_X, FS_X + 20.0, 125.0, 167.0, ZT - 180.0, ZT + 170.0), "silikon",   # v23: ön kenar z 0 (v22 +10)
         bom=("Fire sileceği", 1, "gıda tipi silikon lastik + 24 V aktüatör",
              "pide tablaya yapışıp kalırsa: tabla kırıntı çekmecesinin üstüne gelir, silecek "
              "iner ve diski sıyırır; pide fire, hat sonraki siparişe devam eder. "
              "Normalde diske DEĞMEZ, yalnız temizlik hareketinde iner"))

    # v25: agiz_alt_dudagi SİLİNDİ (SPEC §2.3) — önü artık mekanizma bandı kapağı (tava, +59…+79) kapatıyor

    # ---------------- 10 · v25 · ÖN YÜZ (SPEC_on_duzlem_v63 §1 + §2.3): ön çerçeve 30 × 20 × 2 (z +39…+59) + tava paneller (z +59…+79) ----------------
    # dünya → yerel: x − 700 · y − 892. Soğuk kapaklar K1/K2 + 430 çerçeve + fitil + flipper → topping_uno_cad_v14 (soğuk paket).
    yl = lambda y_: y_ - DY_D
    xl = lambda x_: x_ - DX_D
    MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(1553.5), yl(1859.0))
    MEK_PY = (yl(MEK_PAN_Y0), yl(1107.5))                                        # v25b · kanatlar 788'den (çerçeve 791'den; kanadın alt dönüşü çerçevenin altında)
    CER = [("onyuz_cerceve_mek_sol_dikme", boru_y(SAC, SAC + 30.0, Z_CER_C[0], Z_CER_C[1], MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_sag_dikme", boru_y(W - SAC - 30.0, W - SAC, Z_CER_C[0], Z_CER_C[1], MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_alt_kayit", boru_x(MEK_Y[0], MEK_Y[0] + 30.0, Z_CER_C[0], Z_CER_C[1], SAC + 30.0, W - SAC - 30.0)),
           ("onyuz_cerceve_mek_ust_kayit", boru_x(MEK_Y[1] - 30.0, MEK_Y[1], Z_CER_C[0], Z_CER_C[1], SAC + 30.0, W - SAC - 30.0)),
           ("onyuz_cerceve_mek_orta_dikme", boru_y(xl(1584.25), xl(1614.25), Z_CER_C[0], Z_CER_C[1], MEK_Y[0] + 30.0, MEK_Y[1] - 30.0)),
           ("onyuz_cerceve_T_sol_dikme", boru_y(xl(1521.5), xl(1551.5), Z_CER_C[0], Z_CER_C[1], T_Y[0], Y - SAC)),
           ("onyuz_cerceve_T_sag_dikme", boru_y(W - SAC - 30.0, W - SAC, Z_CER_C[0], Z_CER_C[1], T_Y[0], Y - SAC)),
           ("onyuz_cerceve_T_alt_kayit", boru_x(T_Y[0], T_Y[0] + 30.0, Z_CER_C[0], Z_CER_C[1], xl(1551.5), W - SAC - 30.0)),
           ("onyuz_cerceve_T_ust_kayit", boru_x(Y - SAC - 30.0, Y - SAC, Z_CER_C[0], Z_CER_C[1], xl(1551.5), W - SAC - 30.0))]
    for _i, (_a, _w) in enumerate(CER):
        ekle(_a, _w, "celik", bom=("C ön çerçevesi 30 × 20 × 2 AISI 304 dikdörtgen profil · kaynaklı", len(CER),
                                   "mekanizma bandı (5 parça) + teknik cep (4 parça) · z +39…+59 (panel arkası) · yan sacların ön dönüşüne M6",
                                   "gizli menteşe + bas-aç mandallar bu çerçeveye") if _i == 0 else None)
    for _i, _yk in enumerate((yl(1600.0), yl(1790.0))):                         # v25b · T SOL DİKMESİ köşebentle TU dikey ayırma sacına (denetim_C bulgu 7: 976 mm çerçeve yalnız sağdan taşınıyordu)
        _L = kut(xl(1521.5), xl(1524.5), _yk, _yk + 40.0, -20.0, Z_CER_C[0]).union(kut(xl(1521.5), xl(1551.5), _yk, _yk + 40.0, Z_CER_C[0] - 3.0, Z_CER_C[0]))
        ekle("onyuz_cerceve_T_sol_kosebendi_%d" % _i, _L, "celik",
             bom=("T sol dikme köşebendi L 3 mm AISI 304 (40 boy)", 2, "dik kol dikey ayırma sacının sağ yüzüne 2 × M5 (sac üstte TC tavanına kaynaklı) · yatay kol T sol dikmesinin arkasına kaynak",
                  "v25b · bas-aç mandal T sol dikmesinde → 50 N basıda serbest uç esnemesi ≈ 3–4 mm idi (denetçi tahmini); şimdi iki noktadan taşınır") if _i == 0 else None)
    # tava paneller · derz 3 · dünya: mekanizma kanatları x 701,5–1597,75 / 1600,75–2497 · y 791–1107,5 · T x 1521,5–2497 · y 1553,5–1859
    _yar = []
    for _xg in (860.0, 930.0, 1000.0, 1070.0):                                  # giriş (sol-alt, soğutma grubunun önü): 32 yarık 60 × 4
        for _yg in range(8):
            _yar.append((_xg, _xg + 60.0, T_YARIK_Y[0] + 10.0 * _yg, T_YARIK_Y[0] + 4.0 + 10.0 * _yg))   # v25b: alt sıra T alt kaydının önünden çekildi (denetim_C bulgu 9)
    for _xg in (1480.0, 1550.0, 1620.0, 1690.0):                                # çıkış (sağ-üst): 32 yarık 60 × 4
        for _yg in range(8):
            _yar.append((_xg, _xg + 60.0, T_YARIK_Y[1] + 10.0 * _yg, T_YARIK_Y[1] + 4.0 + 10.0 * _yg))   # v25b: üst sıra T üst kaydının önünden çekildi
    PAN = [("onyuz_mekanizma_kanadi_sol", (xl(701.5), xl(1597.75), MEK_PY[0], MEK_PY[1]), (), "sol", 57.0),
           ("onyuz_mekanizma_kanadi_sag", (xl(1600.75), xl(2497.0), MEK_PY[0], MEK_PY[1]), (), "sag", 57.0),
           ("onyuz_T_kapagi", (xl(1521.5), xl(2497.0), T_Y[0], T_Y[1]), tuple(_yar), "sag", 828.0)]
    for _a, (_x0, _x1, _y0, _y1), _yr, _mt, _yc in PAN:
        ekle(_a, tava(_x0, _x1, _y0, _y1, _yr), "sac",
             bom=("%s · tava 20 · AISI 304 fırçalı 1,5" % _a.replace("onyuz_", ""), 1,
                  "%.2f × %.1f · dışarıdan yalnız düz yüzey + derz 3%s" % (_x1 - _x0, _y1 - _y0, " · 64 lazer yarık 60 × 4 (giriş sol-alt / çıkış sağ-üst, soğutma grubu havası)" if _yr else ""),
                  "gizli menteşe %s · bas-aç · %s" % (_mt, "kaide bandını (788–892) da örter, alt kenar 788 = A alt paneli (basamak yok), alttan açılmaz" if "mekanizma" in _a else "teknik cep servis kapağı")))
        ekle(_a + "_omega", omega_pz(_x0 + 3.0, _x1 - 3.0, _yc, Z_ON - 1.5, -1.0), "celik",
             bom=("Panel omegası 1,0 · 40 × 15", 1, "AISI 304 1,0 · panel > 600 (SPEC) · yüz sacının arkasına punta", "") if "kanadi_sol" in _a else None)
        _xm = (_x0 + 2.5, _x0 + 27.5) if _mt == "sol" else (_x1 - 27.5, _x1 - 2.5)
        for _j, _ym in enumerate((_y0 + 40.0, _y1 - 110.0)):
            ekle("%s_mentese_%d" % (_a, _j), kut(_xm[0], _xm[1], _ym, _ym + 70.0, Z_PAN_C[0] + 3.0, Z_ON - 1.5), "celik",
                 bom=("Gizli menteşe · ÇOK KOLLU, sanal dönme merkezi panelin ön dış köşesi (tava panel)", 6, "AISI 304 · kol panele kaynak, taban çerçeveye M5 · dışarıdan görünmez · ürün + parça no VARSAYIM",
                      "v25b · denetim_C bulgu 2: EMKA 1006 sınıfı pim menteşede (eksen 7 / 7) köşe komşu derze 2,9 mm taşar → A / F paneline 0,1 mm kalır; sanal pivot ön dış köşede taşma 0 · ölçü VARSAYIM (25 × 70 × 18,5 zarf)") if _a.endswith("kanadi_sol") and _j == 0 else None)
            _xt = (_x0 + 20.5, _x0 + 27.5) if _mt == "sol" else (_x1 - 27.5, _x1 - 20.5)                        # v25b · menteşe tarafı dönüşün süpürme dairesi (r 20,06) DIŞINDA
            ekle("%s_mentese_%d_taban" % (_a, _j), kut(_xt[0], _xt[1], _ym, _ym + 70.0, Z_PAN_C[0], Z_PAN_C[0] + 3.0), "celik", bom=None)   # v25b · gövde tarafı (çerçeveye M5)
        _xb = (_x1 - 27.0, _x1 - 2.0) if _mt == "sol" else (_x0 + 2.0, _x0 + 27.0)                  # v25b: üç mandal aynı 25 mm (sol kanat 9 mm idi) · derze simetrik
        _yb = (yl(1082.5), yl(1102.5)) if "mekanizma" in _a else (_y0 + 108.5, _y0 + 138.5)          # v25b: mekanizma mandalları ÜST KAYITTA (tam oturur; orta dikme 30 genişlikte ikisini taşımaz)
        ekle(_a + "_basac", kut(_xb[0], _xb[1], _yb[0], _yb[1], Z_PAN_C[0], Z_ON - 1.5), "plastik",
             bom=("Bas-aç mandal (push-to-open, gizli) · Southco E4 touch latch", 3, "parça no + ölçü VARSAYIM", "kulpsuz kapak") if _a.endswith("kanadi_sol") else None)

    # v25b · denetim_C bulgu 12: montajın düşürdüğü v1 soğuk hücresi (pu_*, ic_kabuk) + eski ön kapak (on_kapak, on_kapak_pu, kapak_contasi) BOM'dan çıktı —
    #        soğuk paket tek kaynak TU v14 · ADLAR montaj süzgeçleri (V1_CIKAN / KAPAK) bozulmasın diye KORUNDU (parçalar montajda zaten görünmez)
    for p in PARCALAR:
        if p["ad"].startswith("pu_") or p["ad"] in ("ic_kabuk", "on_kapak", "on_kapak_pu", "kapak_contasi"):
            p["bom"] = None

    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------
    # Kemal: "yalıtım parçasının altındaki gri parçayı sil, ne gerek var ona" (damlama teknesi) ·
    # "ön yüzeyde sac parça kalmış havada uçuyor, onu da sil" (ağız çerçevesi — ön çerçeve sacı
    # v7'de kalkınca desteksiz kalmıştı). Damlamayı artık dozaj kovanı + duckbill valf kesiyor.


# ======================================================================================================================================
# v25 · DÜNYA DENETİMİ — montajın gördüğü C istasyonu (hat_montaj_v62 süzgeçleri) · montaj ya da ajanlar da çağırabilir: TC.dunya_denetimi()
# ======================================================================================================================================
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")                      # hat_montaj_v62 L253
KAPAK_ESKI = ("on_kapak", "on_kapak_pu", "kapak_contasi")                                                   # hat_montaj_v62 L1371
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
V3_CIKAN = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")
V1_TASI = {"sogutma_grubu": (790.0, 0.0, 0.0), "pano_kutusu": (80.0, 0.0, 0.0), "ups": (140.0, 0.0, 0.0), "din_ray_ups": (140.0, 0.0, 0.0),
           "guc_kaynagi": (1196.0, 0.0, 0.0), "fire_silecegi": (520.0, 0.0, 0.0)}                            # hat_montaj_v62 L264 — v25'te bu adlar YOK (etkisiz)
for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
ACICI_HAREKET = ("acici_yatagi_", "acici_reduktoru_", "acici_motoru_", "acici_askisi_", "acici_kafa_plakasi", "acici_konisi_", "acici_mili_")   # montaj v62 L742–744
YARIK_V2 = ((2492.0, 2498.5, 977.0, 1042.0, -417.0, -5.0), (2491.0, 2499.5, 987.0, 1038.0, -409.0, -13.0))    # firin_tp10_cad_v7.YARIK_V2 (montaj cikis_yarigi_contasi yerine)
ANA_V44_DUNYA = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -432.0), (2340.0, 1809.0, -432.0), (2340.0, 1809.0, -740.0)]   # hat_montaj_v62 ANA_V44 + DY + X_BC (ilk 4 nokta)
BEYAZ_HAVADA_TOL = 0.26            # v25b · denetim_C bulgu 4: beyaz liste AÇIKLIKLA sınırlı — bileşen bu açıklıkla (ölçüldü 0,10–0,25) köke bağlanmalı, yoksa KALAN
BEYAZ_HAVADA = [("TU:kasar_cad_v14__", "kaşar kasetinin kendi dönen parçaları (helezon çekirdeği, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): kasar_cad_v14 üretecindeki yatak burcu / geçme boşlukları 0,10–0,25 mm — 0,26 mm açıklıkla köke bağlanıyor (dünya denetimi ölçer); kaset üreteci bu işin dışında"),
                ("TU:sucuk_cad_v8__", "sucuk kasetinin kendi dönen parçaları (helezon A–D + çekirdek, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): sucuk_cad_v8 yatak / geçme boşlukları 0,10–0,25 mm — "
                 "örümcek_orta ↔ çubuklar 0,15 mm RİJİT birleşim (kaynak / geçme olmalı: kaset üretecine iş) · 0,26 mm açıklıkla köke bağlanıyor")]   # v25b: motor kabloları rakorla bağlandı (TU v14b), listeden çıktı
BEYAZ_CAKISMA = [("TU:sos__", "UNO modeli (beldos_cad_v1) iç geçmeleri — satın alınan ürün"), ("TU:harc__", "UNO modeli iç geçmeleri"), ("TU:kiyma__", "UNO modeli iç geçmeleri"),
                 ("TU:kusbasi__", "UNO modeli iç geçmeleri"), ("TU:sos_spreader_", "Beldos spreader attachment iç geçmeleri (tek satın alınan grup, görselden oranla)"),
                 ("TU:harc_spreader_", "Beldos spreader attachment iç geçmeleri"), ("TU:kasar_cad_v14__", "kaşar kaseti iç geçmeleri (kaset üreteci)"),
                 ("TU:sucuk_cad_v8__", "sucuk kaseti iç geçmeleri (kaset üreteci)"), ("IT:", "itici iç pim / burç geçmeleri (itici_cad kendi denetiminde muaf)")]
BIZIM_TU = ("_D70", "cikis_tc_ferrule_valf")                                                               # UNO önekli ama BİZİM parçalar → beyaz listeye girmez


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


def eski(ad):
    """montajın düşürdüğü (görünmeyen) parça"""
    return ad.startswith("_bom") or ad in KAPAK_ESKI or ad in AKTARMA_TP10 or not v1_kalir(ad)


def _tek(wp):
    v = wp.vals() if hasattr(wp, "vals") else [wp]
    v = [o for o in v if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


def dunya_parcalari(TU, IT=None):
    """montaj v62 süzgeçleriyle C istasyonu: TC (eski parçalar düşer, V1_TASI, çıkış yarığı = YARIK_V2) + TU (V3_CIKAN düşer, x + 700 · y − 168) + itici (ev, kalkık)"""
    W_ = []
    for p in PARCALAR:
        if eski(p["ad"]): continue
        d_ = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = _tek(p["wp"]).translate(cq.Vector(DX_D + d_[0], DY_D + d_[1], d_[2]))
        if p["ad"] == "cikis_yarigi_contasi":
            sh = kut(*YARIK_V2[0]).cut(kut(*YARIK_V2[1])).val()
        W_.append(("TC:" + p["ad"], sh))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        W_.append(("TU:" + q["ad"], q["sh"].translate(cq.Vector(DX_D, -168.0, 0.0))))
    if IT is not None:
        IT.kur(IT.S_HOME, True)
        W_ += [("IT:" + p["ad"], IT.dunya(p)) for p in IT.PARCALAR]
    return W_


def _bbk(A, B, t=0.0):
    return not (A.xmax < B.xmin - t or B.xmax < A.xmin - t or A.ymax < B.ymin - t or B.ymax < A.ymin - t or A.zmax < B.zmin - t or B.zmax < A.zmin - t)


def _hacim(a, b):
    try: return a.intersect(b).Volume()
    except Exception: return -1.0


def _beyaz_cakisma(a, c):
    if any(k_ in a or k_ in c for k_ in BIZIM_TU): return None
    for g, _n in BEYAZ_CAKISMA:
        if a.startswith(g) and c.startswith(g): return g
    return None


def _cakisma_listesi(W_, esik=1.0):
    L = sorted([(a, sh, sh.BoundingBox()) for a, sh in W_], key=lambda q: q[2].xmin)
    bul, beyaz = [], {}
    for i in range(len(L)):
        a, A, ba = L[i]
        for j in range(i + 1, len(L)):
            c, C, bc = L[j]
            if bc.xmin > ba.xmax: break
            if not _bbk(ba, bc): continue
            v = _hacim(A, C)
            if v > esik or v < 0:
                g = _beyaz_cakisma(a, c)
                if g: beyaz[g] = beyaz.get(g, 0) + 1
                else: bul.append((round(v, 1), a, c))
    return bul, beyaz


def dunya_denetimi(kaset_adim=10.0):
    """(ad, geçti, değer) listesi · TU v15 + TC v26 + itici v5 dünyada"""
    import importlib, importlib.util as ilu
    import denetim_temas_v1 as DT
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as DSS
    R = []
    def k(ad, ok, deger=""):
        R.append((ad, bool(ok), deger)); print("  %-150s %s %s" % (ad, "GEÇTİ" if ok else "** KALDI **", deger)); sys.stdout.flush()
    t0 = time.time()
    if not [p for p in PARCALAR if p["ad"] == "dis_taban"]:
        PARCALAR[:] = []; modul()
    sp = ilu.spec_from_file_location("TU11", os.path.join(U, TU_DOSYA)); TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    n_tu = TU.den_assert()
    k("TU %s: modül denetimi %d / %d GEÇTİ (den_assert — montaj da çağırabilir)" % (TU_DOSYA, n_tu, n_tu), True)
    try:
        IT = importlib.import_module(ITICI_MOD); it_ad = ITICI_MOD
    except ImportError:
        IT = importlib.import_module("itici_cad_v4"); it_ad = "itici_cad_v4"
    W_ = dunya_parcalari(TU, IT)
    B_ = {a: sh.BoundingBox() for a, sh in W_}
    n_tc, n_tu2, n_it = (sum(1 for a in B_ if a.startswith(p_)) for p_ in ("TC:", "TU:", "IT:"))
    print("DUNYA: TC %d + TU %d + itici (%s) %d = %d parça · %.0f sn" % (n_tc, n_tu2, it_ad, n_it, len(W_), time.time() - t0))
    # 1 · ön düzlem
    zm = max((b.zmax, a) for a, b in B_.items())
    k("ön düzlem: C istasyonunun bütün parçaları z ≤ +79,5 (istisna yok) · en ön %s %+.2f" % (zm[1], zm[0]), zm[0] <= Z_ON + 0.5)
    PANEL = {"TC:onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, MEK_PAN_Y0, 1107.5), "TC:onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, MEK_PAN_Y0, 1107.5),
             "TC:onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0), "TU:onyuz_K1_dis_sac": (701.5, 1518.5, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1521.5, 2497.0, 1110.5, 1550.5)}
    _pk = []
    for a, r in PANEL.items():
        b = B_[a]
        _pk.append((a, abs(b.zmax - Z_ON) < 0.01 and all(abs(u - v) < 0.01 for u, v in zip((b.xmin, b.xmax, b.ymin, b.ymax), r))))
    k("ön yüz panelleri SPEC ölçüsünde, dış yüz tam +79,0: %s" % ", ".join("%s %s" % (a.split(":")[1].replace("onyuz_", ""), "✓" if ok else "✗") for a, ok in _pk), all(ok for a, ok in _pk))
    rs = list(PANEL.values())
    ort = sum(max(0.0, min(p[1], q[1]) - max(p[0], q[0])) * max(0.0, min(p[3], q[3]) - max(p[2], q[2])) for i_, p in enumerate(rs) for q in rs[i_ + 1:])
    alan = sum((r[1] - r[0]) * (r[3] - r[2]) for r in rs)
    derz = 1795.5 * 3.0 + 3.0 * (1107.5 - MEK_PAN_Y0) + 3.0 * 748.5 + 975.5 * 3.0                                             # 1107,5/1110,5 · kanatlar · K1|K2+T · K2|T
    top = (2497.0 - 701.5) * (1859.0 - MEK_PAN_Y0)
    k("ön yüz kapsama: 5 panel %.0f mm² + derz (3 mm) %.0f mm² = C önü %.0f mm² (x 701,5–2497 · y 788–1859, v25b: kanatlar 788 = A alt paneli) · panel üst üste %.0f · A|C ve C|F derzleri 3 (698,5/701,5 · 2497/2500)"
      % (alan, derz, top, ort), abs(alan + derz - top) < 1.0 and ort < 0.01)
    # 2 · açıcı
    ac = [(b.zmax, a) for a, b in B_.items() if a.startswith("TC:acici_")]
    kp = B_["TC:acici_kafa_plakasi"].zmax
    k("açıcı: hiçbir parça +39'u geçmez (en ön %s %+.1f) · kafa plakası ön ucu %+.1f ≤ +10" % (max(ac)[1], max(ac)[0], kp), max(ac)[0] <= Z_KABUK + 0.01 and kp <= 10.01)
    # 3 · çakışma
    bul, beyaz = _cakisma_listesi(W_)
    k("çakışma (gerçek katı > 1 mm³, bütün çiftler): %d · beyaz liste (satın alınan / başka üretecin iç geçmeleri): %s" % (len(bul), beyaz), not bul, str(bul[:8]))
    # 4 · havada parça
    hv = DT.havada(W_, zemin_y=DY_D)
    DT.yaz(hv, en_cok=60, baslik="HAVADA PARCA (dunya · kok: 892 tabanı)")
    aday = [c_ for c_ in hv["bilesen"] if any(all(u.startswith(p_) for u in c_["uye"]) for p_, _n in BEYAZ_HAVADA)]
    kal = [c_["en"] for c_ in hv["bilesen"] if c_ not in aday]
    kal2 = []
    if aday:                                                                   # v25b · beyaz liste açıklıkla sınırlı: aynı dünya BEYAZ_HAVADA_TOL ile yeniden ölçülür
        hv2 = DT.havada(W_, zemin_y=DY_D, tol=BEYAZ_HAVADA_TOL)
        k2 = {u for c_ in hv2["bilesen"] for u in c_["uye"]}
        kal2 = [c_["en"] for c_ in aday if any(u in k2 for u in c_["uye"])]
    k("havada parça: %d parça · kök %d · bağlı %d · KALAN %d · beyaz liste (yalnız kaset iç dönen parçaları: %d bileşen / %d parça) %.2f mm açıklıkla köke bağlı %d · bağlanamayan %d"
      % (hv["parca"], hv["kok"], hv["bagli"], len(kal), len(aday), sum(len(c_["uye"]) for c_ in aday), BEYAZ_HAVADA_TOL, len(aday) - len(kal2), len(kal2)),
      not kal and not kal2, str((kal + kal2)[:10]))
    # 5 · açıcı kafası kalkık (+60 bekleme · +90 top girerken · +100 strok sonu)
    har = [(a, sh) for a, sh in W_ if a.startswith(tuple("TC:" + h_ for h_ in ACICI_HAREKET))]
    sab = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(tuple("TC:" + h_ for h_ in ACICI_HAREKET))]
    for dy in (60.0, 90.0, 100.0):
        c_ = []
        for a, sh in har:
            s2 = sh.translate(cq.Vector(0.0, dy, 0.0)); b2 = s2.BoundingBox()
            for c, sc, bc in sab:
                if _bbk(b2, bc):
                    v = _hacim(s2, sc)
                    if v > 1.0 or v < 0: c_.append((round(v, 1), a, c))
        k("açıcı kafası +%.0f mm (%d hareketli parça) ↔ sabit parçalar çakışma 0" % (dy, len(har)), not c_, str(c_[:6]))
    # 6 · kaset çekme 0–630 (soğuk kapaklar + flipper AÇIK)
    for mod in ("kasar_cad_v14", "sucuk_cad_v8"):
        kod = "kasar" if mod.startswith("kasar") else "sucuk"
        kas = [sh for a, sh in W_ if a.startswith(("TU:" + mod + "__", "TU:" + mod + "_yarik_dili"))]                  # v25b: yarık dili kasetle çıkar
        st = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(("TU:" + mod + "__", "TU:" + mod + "_yarik_dili", "TU:yuva_%s_mandal_dili" % kod, "TU:onyuz_K1_", "TU:onyuz_K2_", "TU:onyuz_flipper"))]
        bul_k = []
        dz = kaset_adim
        while dz <= 630.0 + 1e-6:
            kc = cq.Compound.makeCompound([q.translate(cq.Vector(0.0, 0.0, dz)) for q in kas]); kb = kc.BoundingBox()
            for a, sc, bc in st:
                if _bbk(kb, bc):
                    v = _hacim(kc, sc)
                    if v > 1.0 or v < 0: bul_k.append((dz, a, round(v, 1)))
            dz += kaset_adim
        k("kaset çekme %s 0–630 mm (adım %.0f · kapak açık): TC + TU + itici sabitlerine değmiyor · yarık dili raf / ön büküm / alt PU / çerçeve çentiğinden birlikte çıkar" % (mod, kaset_adim), not bul_k, str(bul_k[:6]))
    # 7 · hava hatları
    ana = TU.boru(ANA_V44_DUNYA, 5.0); ana = ana.val() if hasattr(ana, "val") else ana
    _sag = dict(W_)["TC:dis_yan_sag"]; _rk = dict(W_)["TC:rakor_hava_ana"]
    _d = DSS(ana.wrapped, _rk.wrapped); _d = _d.Value() if _d.IsDone() else 99.0
    k("montaj ana hattı (ANA_V44 · y 1809 · z −432) sağ yan sacın rakorundan geçer: sacla kesişim %.1f mm³ · rakora %.3f mm" % (_hacim(ana, _sag), _d), _hacim(ana, _sag) < 0.01 and _d <= 0.05)
    for j_ in (1, 2):
        h_ = dict(W_)["TU:hava_hatti_acici_D6_%d" % j_]
        _d = DSS(h_.wrapped, dict(W_)["TC:acici_pnomatigi"].wrapped); _d = _d.Value() if _d.IsDone() else 99.0
        k("açıcı hattı %d: sol yan sac rakorundan geçer (sacla kesişim %.1f) · ucu Z silindirinin portunda (%.3f mm)" % (j_, _hacim(h_, dict(W_)["TC:dis_yan_sol"]), _d),
          _hacim(h_, dict(W_)["TC:dis_yan_sol"]) < 0.01 and _d <= 0.05)
    # 8 · teknik cep tabanı + DIN ray sınırı
    TEK_BEK = {"TC:teknik_tasiyici_0": 1554.5, "TC:teknik_tasiyici_1": 1554.5, "TC:teknik_sogutma_grubu": TEK_TASIYICI_Y + TEK_TAKOZ, "TC:teknik_pano_kutusu": TEK_TASIYICI_Y + TEK_TAKOZ,
               "TC:teknik_ups": TEK_TASIYICI_Y, "TC:teknik_guc_kaynagi": TEK_TASIYICI_Y, "TC:teknik_din_plakasi": TEK_TASIYICI_Y}
    tk = [(a, round(B_[a].ymin, 2), v) for a, v in TEK_BEK.items()]
    _S = dict(W_)
    _mt = lambda a_, c_: (lambda d_: d_.Value() if d_.IsDone() else 99.0)(DSS(_S[a_].wrapped, _S[c_].wrapped))
    _tt = [(a.split(":")[1] + "↔" + c.split(":")[1], round(_mt(a, c), 3)) for a, c in (("TC:teknik_tasiyici_0", "TC:dis_yan_sag"), ("TC:teknik_tasiyici_0", "TU:teknik_ayirma_saci_dikey"),
                                                                                    ("TC:teknik_tasiyici_1", "TC:dis_yan_sag"), ("TC:teknik_tasiyici_1", "TU:teknik_ayirma_saci_dikey"))]
    k("v25b · teknik cep: ağır parçalar 2 × L 30×30×3 TAŞIYICI üstünde (uçları TC sağ yan sacı + dikey ayırma sacı · yatay sacın 1 mm üstünde → PU'ya yük yok) · soğutma grubu + pano titreşim takozunda: %s · uç temasları %s · DIN rayları x ≤ 2497 (%.1f)"
      % ([(a.split(":")[1], y_) for a, y_, v in tk], _tt, max(B_[a].xmax for a in B_ if "din_rayi" in a)),
      all(abs(y_ - v) < 0.01 for a, y_, v in tk) and all(d_ <= 0.05 for a, d_ in _tt) and max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01)
    # 8b · v25b · SOĞUK ODA TABANI + ÇERÇEVE BANDI (denetim_C bulgu 1 · KRİTİK): ürün kanalları dışında doğrudan boşluk = 0
    _ak, _akl = TU.soguk_taban_kacagi(W_, DX_D, -168.0)
    k("v25b · soğuk oda ↔ mekanizma bandı: raf dilimi (dünya y 1149,5–1151,5) %d ürün kanalı DIŞINDA açık alan %.2f mm² ≤ 1 (v25: ≈ 21 350)" % (len(TU.KANAL), _ak), _ak <= 1.0,
      str([(round(a_, 2), round(b_.xmin), round(b_.zmin)) for a_, b_ in _akl if a_ > 0.01][:6]))
    _ab2, _abl = TU.cerceve_bandi_acik(W_, DX_D, -168.0)
    k("v25b · 430 çerçeve düzlemi soğuk oda altı bandında (dünya y 1109–1152) kesintisiz (kaset çentikleri yarık dili flanşıyla kapalı): açık alan %.2f mm² ≤ 1" % _ab2, _ab2 <= 1.0,
      str([(round(a_, 2), round(b_.xmin), round(b_.ymin)) for a_, b_ in _abl if a_ > 0.01][:6]))
    # 8c · v25b · KAPAK AÇILMA TARAMASI (denetim_C bulgu 2): 5 kapak · sanal pivot ön dış köşe · diğer kapaklar KAPALI · A kabini + F ön zarfı engel
    ENGEL = [("F:fırın + üst kabin ön zarfı (x ≥ 2500, z ≤ +79)", kut(2500.0, 4000.0, 788.0, 1862.0, -D, Z_ON).val())]
    try:
        import acici_kabin_cad_v1 as AK
        AK.kur(); ENGEL += [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR]
    except Exception as e_:
        ENGEL.append(("A:ön zarf (x ≤ 698,5, z ≤ +79)", kut(0.0, 698.5, 788.0, 1862.0, -D, Z_ON).val())); print("  BİLGİ · A kabini yüklenemedi → A ön zarfı kutu (%s)" % str(e_)[:80])
    for kn in ("K1", "K2"):
        _kt = TU.kapak_tarama(W_ + ENGEL, kn, DX_D)
        k("v25b · %s AÇILMA TARAMASI 0–110° (%d açı · sanal pivot ön dış köşe%s · A kabini %d parça + F zarfı engel): çakışma %d"
          % (kn, len(TU.ACI_TARAMA), " · flipper katlanır min(90, %.0f·α) · K2 KAPALI" % TU.FLIP_K if kn == "K1" else " · K1 + flipper KAPALI", len(ENGEL) - 1, len(_kt)), not _kt, str(_kt[:6]))
    for ad in PAN_DON:
        hn = ("TC:" + ad, "TC:" + ad + "_omega", "TC:" + ad + "_mentese_0", "TC:" + ad + "_mentese_1")
        har_p = [(a, sh) for a, sh in W_ if a in hn]
        sab_p = [(a, sh, sh.BoundingBox()) for a, sh in W_ + ENGEL if a not in hn]
        bul_p = []
        for aci in TU.ACI_TARAMA:
            for a, sh in har_p:
                m = panel_don(sh, ad, aci); mb = m.BoundingBox()
                for c, sc, bc in sab_p:
                    if not _bbk(mb, bc): continue
                    v = _hacim(m, sc)
                    if v > 1.0 or v < 0: bul_p.append((aci, a, c, round(v, 1)))
        k("v25b · %s AÇILMA TARAMASI 0–110° (%d açı · sanal pivot ön dış köşe x %.1f · diğer kapaklar kapalı · A + F engel): çakışma %d" % (ad.replace("onyuz_", ""), len(TU.ACI_TARAMA), PAN_DON[ad][0], len(bul_p)),
          not bul_p, str(bul_p[:6]))
    # 8d · v25b · HAZNE DOLUM ÇEKMESİ (denetim_C bulgu 13): TC kelepçe sökülür, hazne 20 mm kaldırılır, 0–640 öne (K1 + flipper + K2 açık)
    for kk in ("kiyma", "kusbasi"):
        hn = ("TU:%s_hazne_bizim" % kk, "TU:%s_hazne_boynu" % kk)
        har_h = [(a, sh) for a, sh in W_ if a in hn]
        sab_h = [(a, sh, B_[a]) for a, sh in W_ if a not in hn and a != "TU:%s_tc_kelepce_hazne" % kk and not a.startswith(("TU:onyuz_K1_", "TU:onyuz_K2_", "TU:onyuz_flipper"))]
        bul_h = []; dz = 0.0
        while dz <= 640.0 + 1e-6:
            for a, sh in har_h:
                s2 = sh.translate(cq.Vector(0.0, 20.0, dz)); b2 = s2.BoundingBox()
                for c, sc, bc in sab_h:
                    if _bbk(b2, bc):
                        v = _hacim(s2, sc)
                        if v > 1.0 or v < 0: bul_h.append((dz, a, c, round(v, 1)))
            dz += 20.0
        k("v25b · %s haznesi DOLUM ÇEKMESİ: TC kelepçe sökülür → hazne 20 mm kaldırılır → 0–640 mm öne (K1 + flipper + K2 açık): serbest (bulgu %d)" % (kk, len(bul_h)), not bul_h, str(bul_h[:6]))
    # 8e · v25b · BAĞLANTILAR (bulgu 3 · 7 · 8 · 11 + kılavuz + panel menteşeleri): hepsi ≤ 0,05 mm
    _bg = [("TU:onyuz_mentese_tabani_K1_mentese_0", "TC:dis_yan_sol"), ("TU:onyuz_mentese_tabani_K1_mentese_1", "TC:dis_yan_sol"),
           ("TU:onyuz_mentese_tabani_K2_mentese_0", "TC:dis_yan_sag"), ("TU:onyuz_mentese_tabani_K2_mentese_1", "TC:dis_yan_sag"),
           ("TC:onyuz_cerceve_T_sol_kosebendi_0", "TU:teknik_ayirma_saci_dikey"), ("TC:onyuz_cerceve_T_sol_kosebendi_0", "TC:onyuz_cerceve_T_sol_dikme"),
           ("TC:onyuz_cerceve_T_sol_kosebendi_1", "TU:teknik_ayirma_saci_dikey"), ("TC:onyuz_cerceve_T_sol_kosebendi_1", "TC:onyuz_cerceve_T_sol_dikme"),
           ("IT:montaj_kirisi", "TU:soguk_duvar_sag_alt_profili"), ("TU:soguk_duvar_sag_alt_profili", "TC:dis_yan_sag"),
           ("TU:onyuz_kilavuz_flipper", "TU:tasiyici_raf_3mm"), ("TC:teknik_takoz_0", "TC:teknik_tasiyici_0"), ("TC:teknik_takoz_0", "TC:teknik_sogutma_grubu"),
           ("TC:teknik_takoz_6", "TC:teknik_pano_kutusu"), ("TC:teknik_din_plakasi", "TC:teknik_tasiyici_1"), ("TC:teknik_ups", "TC:teknik_din_rayi_ups"), ("TC:teknik_din_rayi_ups", "TC:teknik_din_plakasi"),
           ("TC:onyuz_mekanizma_kanadi_sol_mentese_0", "TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban"), ("TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban", "TC:onyuz_cerceve_mek_sol_dikme"),
           ("TC:onyuz_mekanizma_kanadi_sol_basac", "TC:onyuz_cerceve_mek_ust_kayit"), ("TC:onyuz_mekanizma_kanadi_sag_basac", "TC:onyuz_cerceve_mek_ust_kayit"),
           ("TU:kasar_cad_v14_yarik_dili", "TU:kasar_cad_v14__cikis_tupu"), ("TU:motor_kablosu_kasar_cad_v14_helezon", "TU:motor_kasar_cad_v14_helezon")]
    _bd = [(a.split(":")[1], c.split(":")[1], round(_mt(a, c), 3)) for a, c in _bg]
    k("v25b · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · T köşebendi ↔ dikey sac + dikme · itici kirişi ↔ sağ duvar alt profili ↔ TC yan sacı · kılavuz ↔ raf · takoz · DIN plakası · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"
      % len(_bg), all(d_ <= 0.05 for a, c, d_ in _bd), str([x for x in _bd if x[2] > 0.05][:6]))
    # 9 · kinematik = v24 (koniler, disk, tabla, ray)
    try:
        V24 = importlib.import_module("topping_cad_v24"); V24.PARCALAR[:] = []; V24.modul()
        es = []
        for ad in ("acici_konisi_on", "acici_konisi_arka", "calisma_diski", "tabla", "lineer_ray_on", "araba_plakasi", "doner_yatak"):
            a1 = _tek([p for p in V24.PARCALAR if p["ad"] == ad][0]["wp"]); a2 = _tek([p for p in PARCALAR if p["ad"] == ad][0]["wp"])
            b1, b2 = a1.BoundingBox(), a2.BoundingBox()
            es.append((ad, max(abs(u - v) for u, v in zip((b1.xmin, b1.xmax, b1.ymin, b1.ymax, b1.zmin, b1.zmax), (b2.xmin, b2.xmax, b2.ymin, b2.ymax, b2.zmin, b2.zmax))), abs(a1.Volume() - a2.Volume())))
        k("kinematik v24 ile aynı (koniler, çalışma diski, tabla, ray, araba, döner yatak): en büyük fark kutu %.4f mm · hacim %.3f mm³" % (max(e[1] for e in es), max(e[2] for e in es)),
          max(e[1] for e in es) < 0.001 and max(e[2] for e in es) < 0.01)
    except Exception as e_:
        k("kinematik v24 karşılaştırması yapılamadı: %s" % e_, False)
    # 10 · bilgi: A kabini + kaide v2 ile (A ajanının dosyaları varsa)
    try:
        import acici_kabin_cad_v1 as AK, kaide_cad_v2 as KD2
        AK.kur(); KD2.kur()
        A_ = [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR] + [("KAIDE:" + p["ad"], KD2.dunya(p)) for p in KD2.PARCALAR]
        cA = []
        for a, sa in A_:
            ba = sa.BoundingBox()
            for c, sc in W_:
                if _bbk(ba, B_[c]):
                    v = _hacim(sa, sc)
                    if v > 1.0 or v < 0: cA.append((round(v, 1), a, c))
        print("  BİLGİ · A kabini (acici_kabin_cad_v1) + kaide_cad_v2 ↔ C istasyonu (%d + %d parça) çakışma: %s" % (len(AK.PARCALAR), len(KD2.PARCALAR), "TEMİZ" if not cA else "%d BULGU %s" % (len(cA), cA[:6])))
        R.append(("BİLGİ · A kabini + kaide v2 ↔ C çakışma %d" % len(cA), True, str(cA[:6])))
    except Exception as e_:
        print("  BİLGİ · A kabini / kaide v2 yüklenemedi (%s)" % str(e_)[:100])
    print("DUNYA DENETIMI SURESI %.0f sn" % (time.time() - t0))
    return R


if __name__ == "__main__":
    t0 = time.time(); modul()
    gercek = [p for p in PARCALAR if not p["ad"].startswith("_bom")]
    print("TOPPING MODULU v26 · %d parca (%d cizili + %d yalniz listede) · %.0f sn" % (len(PARCALAR), len(gercek), len(PARCALAR) - len(gercek), time.time() - t0))
    gecersiz = [p["ad"] for p in gercek if not p["wp"].val().isValid()]
    print("KATI DENETIMI: %s" % ("hepsi gecerli" if not gecersiz else "GECERSIZ: " + ", ".join(gecersiz))); assert not gecersiz

    # ---- zarf ----
    bb = [(p["ad"], p["wp"].val().BoundingBox()) for p in gercek]
    # v22: istasyon artik soldaki aciciyi ve sagdaki firin aktarimini da kapsiyor.
    # Ana soguk govde hala 0..W; hareket altyapisi ve transfer elemanlari kontrollu uzantidir.
    _zx0, _zx1 = min(XK_SOL - 46.0, H.X_LIMIT_SOL - 220.0), 2245.0                  # v24: motor sol uçta (kaide −605)
    # Acici motor/kafa paketi ve bant motoru soguk govdenin ONUNE tasar; bu kontrollu
    # servis uzantisi +310 mm ile sinirli. Ana soguk govdenin derinligi degismedi.
    _z_on = Z_ON + 0.5                                                          # v25: ön düzlem (v24: açıcı için +310)
    tas = [a for a, b in bb if b.xmin < _zx0 - 0.01 or b.xmax > _zx1 + 0.01 or b.ymin < ((MEK_PAN_Y0 - DY_D) if a.startswith("onyuz_") else 0.0) - 0.01 or b.ymax > Y + 0.01 or b.zmax > _z_on + 0.01 or b.zmin < -D - 0.01]
    _xmin, _xmax = min(b.xmin for _, b in bb), max(b.xmax for _, b in bb)
    _ymax = max(b.ymax for _, b in bb)
    _zmin, _zmax = min(b.zmin for _, b in bb), max(b.zmax for _, b in bb)
    print("ISTASYON ZARFI: %s (x %.0f...%.0f, y 0...%.0f, z %.0f...%.0f)" % ("GECTI" if not tas else "TASAN: " + ", ".join(tas), _xmin, _xmax, _ymax, _zmin, _zmax)); assert not tas
    # v23 · ÖN YÜZ DENETİMİ: açıcı kafası dışında (bilinen açık konu) HİÇBİR parça makinenin ön yüzünü (z 0) geçemez.
    _on = [(a, round(b.zmax, 2)) for a, b in bb if b.zmax > Z_ON + 0.5]
    print("ON DUZLEM (v25 · butun parcalar z <= +79,5 · acici istisnasi YOK): %s · en on %s" % ("GECTI" if not _on else "TASAN: %s" % _on, sorted(((round(b.zmax, 2), a) for a, b in bb), reverse=True)[:3])); assert not _on
    _acz = [(a, round(b.zmax, 2)) for a, b in bb if a.startswith("acici_") and b.zmax > Z_KABUK + 0.01]
    _kaf = max(b.zmax for a, b in bb if a.startswith("acici_kafa_plakasi"))
    print("ACICI (v25 · hicbir parca +39'u gecmez · kafa on ucu <= +10): en on acici parcasi %s · kafa plakasi %+.1f · %s"
          % (max(((round(b.zmax, 1), a) for a, b in bb if a.startswith("acici_"))), _kaf, "GECTI" if not _acz and _kaf <= 10.01 else "KALDI %s" % _acz)); assert not _acz and _kaf <= 10.01
    _kb = {a: round(b.zmax, 2) for a, b in bb if a in ("dis_taban", "dis_tavan", "dis_yan_sol", "dis_yan_sag")}
    print("KABUK on kenari +39: %s · %s" % (_kb, "GECTI" if all(abs(v - Z_KABUK) < 0.01 for v in _kb.values()) else "KALDI")); assert all(abs(v - Z_KABUK) < 0.01 for v in _kb.values())
    _pn = {a: (round(b.zmin, 2), round(b.zmax, 2)) for a, b in bb if a in ("onyuz_mekanizma_kanadi_sol", "onyuz_mekanizma_kanadi_sag", "onyuz_T_kapagi")}
    print("TAVA PANELLER z +59…+79: %s · %s" % (_pn, "GECTI" if all(abs(v[0] - Z_PAN_C[0]) < 0.01 and abs(v[1] - Z_ON) < 0.01 for v in _pn.values()) else "KALDI"))
    assert len(_pn) == 3 and all(abs(v[0] - Z_PAN_C[0]) < 0.01 and abs(v[1] - Z_ON) < 0.01 for v in _pn.values())

    # v23 · ÜRÜN GEÇİŞ ZARFI: en yüksek ürün (hamur 8 + kaşar 6,5 + küp sucuk 14 = 28,5) Ø280 (açıcı çıkışı, kural 3), diskte (y 108) aktarma yolunda
    # x: tabla aktarma konumu − 150 … bant ucu. Bant ve disk ürünün ALTINDA (zarf 0,5 mm yukarıdan başlar).
    _ZT = ZK[0] + 30.0                                                   # tabla ekseni (modul() içindeki ZT ile aynı formül)
    _UZ = kut(H.X_AKTARMA - 150.0, 2226.5, 108.5, 108.0 + 28.5 + 0.5, _ZT - 140.0, _ZT + 140.0).val()
    _ug = []
    for p in gercek:
        b_ = p["wp"].val().BoundingBox()
        if b_.xmax < H.X_AKTARMA - 150.0 or b_.xmin > 2235.0 or b_.ymax < 108.5 or b_.ymin > 137.0 or b_.zmax < _ZT - 140.0 or b_.zmin > _ZT + 140.0:
            continue
        try: v_ = p["wp"].val().intersect(_UZ).Volume()
        except Exception: v_ = -1.0
        if v_ > 0.5 or v_ < 0: _ug.append((p["ad"], round(v_, 1)))
    print("URUN GECIS ZARFI (O280 x 28,5 mm urun · disk -> bant): %s" % ("TEMIZ" if not _ug else "%d BULGU %s" % (len(_ug), _ug)))
    assert not _ug, "en yuksek urun aktarma yolunda sabit parcaya carpiyor"

    # ---- çakışma ----
    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in gercek]; bulgu = []
    _atla = 0
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            if eski(S[i][0]) != eski(S[j][0]): _atla += 1; continue                 # v25: montajdan düşen eski parça ↔ görünen parça ölçüm dışı (SPEC §2.3)
            try: v = S[i][1].intersect(S[j][1]).Volume()
            except Exception: v = -1.0
            if v > 1.0 or v < 0: bulgu.append((S[i][0], S[j][0], round(v, 1)))
    print("CAKISMA: %s (v25: eski/montaj-dışı ↔ görünen %d aday çift ölçüm dışı · görünenler dünya denetiminde ayrıca)" % ("TEMIZ" if not bulgu else "%d BULGU" % len(bulgu), _atla))
    for x in bulgu: print("   ", x)
    assert not bulgu

    # ---- KASET ZARFI ↔ MODÜL ÇAKIŞMASI (v2'de eklendi) ----
    # v1 yalnız modülün KENDİ parçalarını tarıyordu; kasetler makine montajında ayrı birim olduğu için
    # kaset ile modül arasındaki çakışma HİÇ taranmamıştı. Evaporatörün beş kasetin içine girmesi böyle kaçtı.
    kb = []
    for ad, x0, x1, gen in YUVA:
        kb.append((ad, (x0 + BOSLUK / 2, x1 - BOSLUK / 2), (KAS[0], KAS[1]), (ZK[1], ZK[0])))
        # v5: kasetin YUVARLAK BORUSU kaset kutusunun ALTINA iniyor — onun da zarfı taranmalı,
        # yoksa borunun PU tabana / raya / damlama teknesine girmesi görülmez.
        bd, be, ba = BORU[ad]
        _r = bd / 2.0 + be
        _zc = ZK[0] + ((AGIZ[ad][0] + AGIZ[ad][1]) / 2.0 - AGIZ[ad][2] / 2.0)
        kb.append((ad + " borusu", ((x0 + x1) / 2.0 - _r, (x0 + x1) / 2.0 + _r), (KAS[0] + ba, KAS[0]), (_zc - _r, _zc + _r)))
    ac = []
    for p in PARCALAR:
        # v10: muafiyet DARALDI — kovanlar artık taranıyor. Bu muafiyet yüzünden üç kaset borusu
        # (KUŞBAŞI 12.017 · KÜP SUCUK 2.156 · KAŞAR 562 mm³) sekiz sürümdür PU'nun içinde gömülü duruyordu.
        if p["ad"].startswith("_bom") or (p["ad"].startswith(("ray_", "bolme_", "konum_pimi_", "ic_kabuk", "pu_"))
                                          and not p["ad"].startswith("dozaj_kovani")):
            continue                                                            # kasete DEĞMESİ gereken parçalar
        bb = p["wp"].val().BoundingBox()
        for ad, xa, ya, za in kb:
            o = (min(xa[1], bb.xmax) - max(xa[0], bb.xmin), min(ya[1], bb.ymax) - max(ya[0], bb.ymin), min(za[1], bb.zmax) - max(za[0], bb.zmin))
            if all(v > 0.5 for v in o):
                ac.append((p["ad"], ad, tuple(round(v) for v in o)))
    print("KASET <-> MODUL CAKISMASI: %s" % ("TEMIZ" if not ac else "%d BULGU" % len(ac)))
    for a_ in ac[:14]:
        print("   %-22s %-12s ortak %s mm" % a_)
    assert not ac, "kaset zarfi modul parcasiyla cakisiyor"

    # ---- KASET YUVAYA SIĞIYOR MU + TAHRİK EKSENİ TUTUYOR MU ----
    print("YUVA DENETIMI:")
    for ad, x0, x1, gen in YUVA:
        bosluk = (x1 - x0) - gen
        alt, ust = EKSEN[ad]
        print("   %-11s yuva %.0f  kaset %.0f  bosluk %.1f mm · mil kotlari (kaset tabanindan) %.0f / %.0f" % (ad, x1 - x0, gen, bosluk, alt, ust))
        assert abs(bosluk - BOSLUK) < 0.01, "%s: yuva-kaset boslugu %.1f (olmasi gereken %.1f)" % (ad, bosluk, BOSLUK)
    ekseni = {}
    for p in gercek:
        if p["ad"].startswith("mil_"):
            b = p["wp"].val().BoundingBox(); ekseni[p["ad"]] = round((b.ymin + b.ymax) / 2.0, 1)
    bek = []
    for ad, x0, x1, gen in YUVA:
        for j, ey in enumerate(EKSEN[ad]):
            k = "mil_%s_%s" % (ad.replace(" ", "_"), "helezon" if j == 0 else "rotor")
            bek.append((k, round(KAS[0] + ey, 1), ekseni.get(k)))
    kotu = [x for x in bek if x[1] != x[2]]
    print("   tahrik mil eksenleri kasetin kendi eksenleriyle AYNI: %s" % ("EVET (12/12)" if not kotu else kotu)); assert not kotu
    print("   derinlik: ON NIS %.0f | kapak %.0f | kulp %.0f | kaset %.0f | kavrama %.0f | yalitim %.0f | kuru %.0f = %.0f mm"
          % (H.ON_NIS, H.ON_KAPAK, H.KULP_BOS, H.KASET_D, H.KAVRAMA, H.ARKA_PU, abs(ZKURU[1] - ZKURU[0]), D))

    # v26 · DÜNYA DENETİMİ (montajın gördüğü C istasyonu: TC v26 + TU v15 + itici)
    DD = dunya_denetimi()
    _kal = [x for x in DD if not x[1]]
    print("DUNYA DENETIMI: %d denetim · %s" % (len(DD), "HEPSI GECTI" if not _kal else "%d KALDI" % len(_kal)))
    assert not _kal, _kal
    # v23: STEP/STL üretim dosyaları YAZILMAZ (kural 6.7: SolidWorks/STEP çıktısı yok; v22 klasörü korunur)
    sys.stdout.flush(); os._exit(0)
    # ---- üretim dosyaları ----
    os.makedirs(os.path.join(URETIM, "step"), exist_ok=True); os.makedirs(os.path.join(URETIM, "stl"), exist_ok=True)
    asm = cq.Assembly(name="TOPPING_MODUL_v22"); RENK = dict(sac=(0.74, 0.77, 0.80, 1), pu=(0.93, 0.88, 0.72, 1), motor=(0.18, 0.19, 0.22, 1),
                                                            pom=(0.95, 0.95, 0.92, 1), celik=(0.75, 0.77, 0.8, 1), bakir=(0.72, 0.45, 0.2, 1), kart=(0.1, 0.35, 0.22, 1), koyu=(0.15, 0.15, 0.17, 1), silikon=(0.16, 0.5, 0.95, 1))
    bom = []
    for p in gercek:
        sh = p["wp"].val(); b = sh.BoundingBox()
        cq.exporters.export(p["wp"], os.path.join(URETIM, "step", p["ad"] + ".step"))
        cq.exporters.export(p["wp"], os.path.join(URETIM, "stl", p["ad"] + ".stl"), tolerance=0.1, angularTolerance=0.3)
        asm.add(sh, name=p["ad"], color=cq.Color(*RENK.get(p["mal"], (0.8, 0.8, 0.8, 1))))
    for p in PARCALAR:
        if p["bom"]:
            b = p["wp"].val().BoundingBox()
            bom.append((p["ad"],) + tuple(p["bom"]) + ("%.0f × %.0f × %.0f" % (b.xlen, b.ylen, b.zlen),))
    asm.save(os.path.join(URETIM, "TOPPING_MODUL_v22_MONTAJ.step"))
    with io.open(os.path.join(URETIM, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["dosya", "parça", "adet", "malzeme · yöntem", "görevi", "zarf mm"]); w.writerows(bom)
    with io.open(os.path.join(URETIM, "bom.json"), "w", encoding="utf-8") as f: json.dump(bom, f, ensure_ascii=False)
    print("URETIM: %d STEP + %d STL + MONTAJ.step + BOM.csv (%d kalem) → %s" % (len(gercek), len(gercek), len(bom), URETIM))
    for b in bom: print("   %-22s %-38s ×%-3s %s" % (b[0], b[1], b[2], b[5]))
    sys.stdout.flush(); os._exit(0)
