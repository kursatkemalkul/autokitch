# -*- coding: utf-8 -*-
"""AUTOKITCH · 3 · TOPPING MODÜLÜ — ÜRETİM MODELİ v1 (22 Eyl 2026)
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
ÇIKTI: arastirma/3_TOPPING/topping_modul_v10/ (parça başına STEP + STL, MONTAJ.step, BOM.csv) · otonom/hat3d/ (GLB/USDZ)

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
URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "topping_modul_v10")
from kaset_3d_v3 import Mesh, MM, MALZEME, doku_ad, usdz_yaz, OUT
import topping_hesap_v4 as H

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
KASET_CAD = {"HARÇ 1": "harc_cad_v4", "HARÇ 2": "harc_cad_v4", "KIYMA": "kiyma_cad_v9",
             "KUŞBAŞI": "kusbasi_cad_v8", "KAŞAR KABI": "kasar_cad_v14", "KÜP SUCUK": "sucuk_cad_v7"}


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


MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtrac-23078.step")
_MOT = {}


def nema23():
    """STP-MTRAC-23078 gercek katisi. STEP'te: govde z -76..0, mil z 0..+20, kablo +y.
    Bizim modelde motorun mil yuzu zm'de ve govde -z'ye dogru uzuyor — ayni yonelim."""
    if _MOT: return _MOT
    w = cq.importers.importStep(MOTOR_STEP)
    sol = w.val().Solids()
    govde = max(sol, key=lambda s_: s_.Volume())
    kablo = min(sol, key=lambda s_: s_.Volume())
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
    _MOT["kablo"] = kablo.intersect(cq.Workplane("XY").box(40, KAB, 40, centered=(True, False, True))
                                    .translate(cq.Vector(0, kb.ymin, (kb.zmin + kb.zmax) / 2)).val())
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
    ekle("dis_taban", kut(0, W, 0, SAC, 0, -D), "sac", bom=("Dış taban sacı", 1, "304 1,5 mm · lazer + abkant", "modülün tabanı, alttaki B modülüne oturur"))
    ekle("dis_tavan", kut(0, W, Y - SAC, Y, 0, -D), "sac", bom=("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant", "üst kapak; soğutma grubu buraya oturur"))
    for s, x in (("sol", 0.0), ("sag", W - SAC)):
        ekle("dis_yan_" + s, kut(x, x + SAC, SAC, Y - SAC, 0, -D), "sac", bom=("Dış yan sac", 2, "304 1,5 mm · lazer + abkant", "komşu modüle cıvatalanır (lego birleşim)") if s == "sol" else None)
    ekle("dis_arka", kut(SAC, W - SAC, SAC, Y - SAC, -D, -D + SAC), "sac", bom=("Dış arka sac", 1, "304 1,5 mm", "kuru bölmenin arkası; kablo rakorları burada"))

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
    for i, xx in enumerate((110.0, W - 140.0)):
        ekle("mentese_%d" % i, kut(xx, xx + 30.0, KAS[0] - 30.0, KAS[0] - 26.0, ZKAP[0] - 4.0, ZKAP[1] + 2.0), "celik",
             bom=("Menteşe", 2, "paslanmaz, gömme", "kapak alttan menteşeli: açılınca tezgâh gibi öne yatar") if i == 0 else None)

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
                                     ("_bom_motor", "AutomationDirect STP-MTRAC-23078 · NEMA23 · 1,60 N·m tutma · 0,71 A · IP40 (GERÇEK CAD)", 12, "sürücüsüyle birlikte", "dozaj = mil açısı; kapalı çevrim adım kaçırmayı yakalar")):
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
         bom=("Fanlı evaporatör (unit cooler)", 1, "400 × 180 × 190 (lamel 140 + fan 50) · standart sınıf", "KURU BÖLMEDE, motorların üstünde; soğuğu arka yalıtımdaki iki boşluktan hücreye verir · yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    ekle("fan_0", silz(W / 2.0, (EVY[0] + EVY[1]) / 2.0, 100.0, EVZ[1] - 3.0, EVZ[1] - 53.0), "motor",
         bom=("Evaporatör fanı Ø200", 1, "24 V eksenel · evaporatörle birlikte gelir", "havayı evaporatörden çekip yalıtımdaki üfleme boşluğuna basar"))
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
    ekle("sogutma_grubu", kut(60.0, 360.0, TEK[0] + 6.0, TEK[0] + 226.0, -60.0, -280.0), "motor",
         bom=("Soğutma grubu ⅕ HP", 1, "hermetik, hava soğutmalı", "teknik bantta, önden servis; +3 °C'de 250–350 W verir"))

    # ---------------- 8 · ELEKTRİK (teknik bant) ----------------
    # v15: masif degil 1,5 mm SAC KABIN (masifken 189,6 kg cikiyordu, gercegi ~20 kg)
    _pd = kut(1100.0, 1500.0, TEK[0] + 6.0, TEK[0] + 246.0, -40.0, -290.0)
    _pi = kut(1101.5, 1498.5, TEK[0] + 7.5, TEK[0] + 244.5, -41.5, -288.5)
    ekle("pano_kutusu", _pd.cut(_pi), "sac",
         bom=("Ana pano kutusu", 1, "304 · önden kapaklı, IP54", "PLC + ana şalter + röleler; ekran yok, tablet"))
    ekle("ups", kut(1520.0, 1740.0, TEK[0] + 6.0, TEK[0] + 156.0, -40.0, -230.0), "koyu", bom=("UPS 500 VA", 1, "hat içi", "elektrik kesintisinde kaset konumları ve saat korunur"))
    ekle("guc_kaynagi", kut(400.0, 560.0, TEK[0] + 6.0, TEK[0] + 106.0, -40.0, -140.0), "sac",
         bom=("Güç kaynağı 24 V %d W" % H.S["elektrik"]["guc_kaynagi_W"], 1, "DIN raya", "aynı anda en çok 2 mil döner"))
    ekle("din_ray", kut(600.0, 1060.0, TEK[0] + 26.0, TEK[0] + 41.0, -140.0, -147.0), "sac", bom=("DIN ray 35 mm", 1, "standart", "sürücü kartları burada"))
    for i in range(12):
        xx = 605.0 + i * 38.0
        ekle("surucu_%d" % i, kut(xx, xx + 34.0, TEK[0] + 6.0, TEK[0] + 81.0, -45.0, -140.0), "kart",
             bom=("Step sürücü kartı", 12, "kapalı çevrim, 24 V", "her mile bir sürücü: 6 kaset × 2") if i == 0 else None)

    # ---------------- 8b · DÖNER TABLA — TAM ÜRETİM MODELİ (v10) ----------------
    # v9'a kadar 9 adet yer tutucu bloktu; parçaların hiçbiri birbirine bağlanmıyordu. Şema: X ekseni
    # KAYIŞ tahrikli tek araba, DÖNÜŞ ekseni araba plakasının altındaki pancake motorla EŞ EKSENLİ doğrudan.
    TB = H.S["tabla"]
    Xc = 900.0                                                                  # modelde tablanın çizildiği konum (strok x 220…1520)
    ZT = ZK[0] + 30.0                                                           # tabla ekseni (nozzle'dan z'de 20 mm geride)
    RT_ = TB["cap"] / 2.0

    # --- 8b.1 TAŞIYICI: tekne + kiriş merdiveni (1,5 mm saca lineer ray bağlanmaz) ---
    tk = kut(15.0, 1695.0, 1.5, 4.5, -5.0, -415.0)
    tk = tk.union(kut(15.0, 1695.0, 1.5, 31.5, -5.0, -8.0)).union(kut(15.0, 1695.0, 1.5, 31.5, -412.0, -415.0))
    ekle("mekanizma_teknesi", tk, "sac", bom=("Mekanizma teknesi", 1, "304 3,0 mm · kenarları 30 kıvrık · %1,5 eğim",
         "ray kirişlerinin kaynaklandığı yapısal tekne; damlayanı tabla düzleminin ALTINDA toplar, ön-solda Ø25 tahliye"))
    for ad_, z0_, z1_, gen_ in (("on", -95.0, -35.0, 60.0), ("arka", -305.0, -245.0, 60.0)):
        ekle("ray_kirisi_%s" % ad_, kut(45.0, 1695.0, 4.5, 20.5, z0_, z1_), "celik",
             bom=("Ray kirişi 60 × 16 × 1650", 2, "304 lama · tekneye sürekli kaynak", "kaynaktan SONRA üç üst yüzey TEK BAĞLAMADA frezelenir (düzlemlik 0,1 mm/m — HGR15 şartı)") if ad_ == "on" else None)
    ekle("kayis_kirisi", kut(15.0, 1695.0, 4.5, 20.5, -385.0, -335.0), "celik",
         bom=("Kayış kirişi 50 × 16 × 1680", 1, "304 lama", "kayış kasnakları, avara ve gergi bunun üstünde"))
    for i_, xb in enumerate((200.0, 500.0, 800.0, 1100.0, 1400.0, 1650.0)):
        ekle("baglama_lamasi_%d" % i_, kut(xb, xb + 40.0, 4.5, 20.5, -335.0, -305.0), "celik",
             bom=("Bağlama laması 40 × 16", 6, "304 lama", "arka ray kirişi ile kayış kirişini bağlar; dönüş motoru z −141…−198 bandında gezdiği için tam boy lama konulamıyor") if i_ == 0 else None)

    # --- 8b.2 LİNEER KIZAK ---
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        _r, _n = hiwin_ray(65.0, 1665.0, zc_)
        ekle("lineer_ray_%s" % ad_, _r, "celik",
             bom=("Lineer ray HGR15 × 1600", 2, "paslanmaz sınıf [V: özel sipariş, fiyat/teslim sorulacak]", "HIWIN HGR15 GERÇEK profil (TraceParts STEP) · M4 havşa hatve 60 · 1,45 kg/m katalogla birebir") if ad_ == "on" else None)
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
    ekle("ayar_bilezigi", sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0)), "celik",
         bom=("Ayar bileziği · torna halka", 1, "304 · dış Ø210 iç Ø100 · kalınlık 5,23 — yatak Ø197 × 22,27 olunca büyüdü ve İNCELDİ (aralık 2–14)",
              "ray + blok + yatak katalog toleransının TAMAMI bu tek parçada toplanır; yedek dikey boşluk 7,5 mm"))
    gb = sily(Xc, ZT, 110.0, 86.0, 97.0).cut(sily(Xc, ZT, 30.0, 85.0, 98.0))
    for i_ in range(2):
        gb = gb.cut(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.1, 85.0, 92.0))                # tahrik pimi burçları
    ekle("tabla_gobegi", gb, "celik", bom=("Tabla göbeği Ø220 × 11", 1, "304 işlenmiş, cepli ~1,8 kg",
         "ayar bileziğine 3 × M8 saplama + paslanmaz KELEBEK SOMUN + 2 × Ø8 h7 konum pimi ile ALETSİZ sökülür"))
    tb_ = sily(Xc, ZT, RT_, 97.0, 100.0)
    for i_ in range(3):                                                                           # robot parmak kesikleri
        a_ = math.radians(120.0 * i_ + 60.0)
        tb_ = tb_.cut(kut(Xc + (RT_ - 25.0) * math.cos(a_) - 30.0, Xc + (RT_ - 25.0) * math.cos(a_) + 30.0,
                          96.0, 101.0, ZT + (RT_ - 25.0) * math.sin(a_) - 12.5, ZT + (RT_ - 25.0) * math.sin(a_) + 12.5))
    ekle("tabla", tb_, "sac", bom=("Döner tabla Ø340 × 3", 1, "304 · göbeğe sürekli TIG kaynak, parlatılmış",
         "gıda yüzeyinde cıvata yok; kenarda 120°'de 3 parmak kesiği 60 × 25 — robot Ø340 tepsinin altına parmak sokabilsin"))
    for i_ in range(3):
        a_ = math.radians(120.0 * i_)
        ekle("merkezleme_pimi_%s" % "ABC"[i_], koni_y_t(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 2.0, 5.0, 100.0, 105.0), "celik",
             bom=("Merkezleme pimi · konik", 3, "304 · taban Ø10 tepe Ø4 boy 5 · H7/r6 presli", "r = 100'de 120° aralıklı; tepsinin altındaki 3 konik çukura girer, hem merkezler hem POZİTİF döndürür") if i_ == 0 else None)

    # --- 8b.4 DÖNÜŞ MOTORU (eş eksenli, i = 1) ---
    ekle("donus_motoru", kut(Xc - 28.5, Xc + 28.5, 4.5, 45.5, ZT - 28.5, ZT + 28.5), "motor",
         bom=("Dönüş motoru · NEMA23 PANCAKE", 1, "57 × 57 × 41 · kapalı çevrim step · ~0,9 N·m [V: tork eğrisi doğrulanacak]",
              "araba plakasının ALTINA 4 × M5 havşa, ekseni TABLA EKSENİYLE AYNI; redüktör ve kayış YOK · gereken 0,169 N·m → ~5 kat pay"))
    lk = sily(Xc, ZT, 15.0, 46.0, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))
    for i_ in range(2):
        lk = lk.union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.0, 66.0, 74.0))
    ekle("tahrik_lokmasi", lk, "celik", bom=("Tahrik lokması Ø30 × 20", 1, "304 torna · yarıklı sıkma + M5 pinç",
         "üstünde r = 10'da 2 × Ø8 pim; göbeğin altındaki burçlara girer — rijit kaplin YOK, tabla düşeyde ayrılabiliyor"))

    # --- 8b.5 X TAHRİK ZİNCİRİ ---
    ekle("x_tahrik_kasnagi", silz(1735.0, 31.0, 9.55, -364.5, -355.5).cut(silz(1735.0, 31.0, 4.1, -366.0, -354.0)), "celik",
         bom=("GT3 kasnak 20 diş", 1, "PD 19,099 → çevre TAM 60,00 mm/tur · sıkma bilezikli (setuskur yok)", "x motorunun milinde"))
    _mg = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0).translate(cq.Vector(1735.0, 41.5, -360.0))
    ekle("x_motoru", cq.Workplane(obj=_mg), "motor",
         bom=("X motoru · NEMA23 kapalı çevrim step", 1, "57 × 57 × 76 · 1,2 N·m · 24 V · mil AŞAĞI",
              "sağ uçta: tablanın en sağ konumu x 1690'da biter, motor 1706,5'te başlar · 200 dev/dk @200 mm/s, gereken 0,212 N·m → ~3 kat pay"))
    ekle("x_motor_kaidesi", kut(1690.0, 1780.0, 20.5, 38.0, -400.0, -320.0).cut(kut(1700.0, 1770.0, 19.5, 39.0, -392.0, -328.0)), "sac",
         bom=("X motor kaidesi", 1, "304 8 mm bükme L · tekneye 4 × M8, z yuvalı", "kayış hizası buradan ayarlanır"))
    ekle("avara_kasnak", silz(35.0, 31.0, 9.55, -364.5, -355.5), "celik",
         bom=("Avara kasnak GT3 20 diş", 1, "flanşlı · içinde 2 × 625-2RS paslanmaz rulman", "sol uçta; gergi bunun braketinde"))
    ekle("avara_gergi_braketi", kut(20.0, 44.0, 20.5, 45.0, -385.0, -335.0).cut(silz(35.0, 31.0, 12.0, -372.0, -348.0)), "celik",
         bom=("Avara + gergi braketi", 1, "304 10 mm · 16 mm yuvalı 2 × M8 + M6 itme vidası + kontra", "GERGİ BURADAN — tabla sağ uca çekilince ağızdan elle erişilir"))
    for i_, zc_ in enumerate((-350.45, -369.55)):
        ekle("x_kayisi_%d" % i_, kut(52.0, 1686.0, 26.5, 35.5, zc_ - 1.5, zc_ + 1.5), "koyu",
             bom=("X kayışı GT3-9 açık uçlu ~3460 mm", 1, "çelik kordlu poliüretan", "iki koşu; TEPSİ GÖLGESİNİN (z 0…−340) DIŞINDA — ürün düzleminin altında tahrik elemanı yok") if i_ == 0 else None)
    kol = kut(Xc - 150.0, Xc + 150.0, 38.5, 48.5, -385.0, -315.0).union(kut(Xc - 20.0, Xc + 20.0, 40.0, 48.5, -365.0, -355.0))
    ekle("kayis_kolu", kol, "celik", bom=("Kayış kolu · L", 1, "304 10 mm bükme · plakaya 4 × M8 + Ø6 pim",
         "düşey kanat iki kayış koşusunun TAM ORTASINDA, her yana 4,55 mm"))
    for i_, xb in enumerate((Xc - 140.0, Xc + 140.0)):
        ekle("kayis_kelepcesi_%d" % i_, kut(xb - 20.0, xb + 20.0, 25.0, 38.0, -374.0, -345.0).cut(kut(xb - 21.0, xb + 21.0, 26.4, 35.6, -373.0, -346.0)), "celik",
             bom=("Kayış kelepçesi", 2, "304 gövde + GT3 diş profilli baskı plakası", "açık kayışın iki ucunu diş-dişe sıkıştırır (2 × M5 + 2 × M4)") if i_ == 0 else None)

    # --- 8b.6 HİJYEN / KORUMA ---
    ap = kut(Xc - 190.0, Xc + 190.0, 58.5, 60.5, -5.0, -340.0).cut(sily(Xc, ZT, 85.0, 57.5, 61.5))
    ap = ap.cut(sily(Xc, ZT, 101.0, 40.0, 95.0))      # v16: Ø197 yatak + 2 mm bosluk
    ekle("siyirici_apron", ap, "sac", bom=("Sıyırıcı apron 380 × 335 × 2", 1, "304 · kenarı 10 kıvrık · elle çıkar",
         "tepsinin ayak izini birebir örter; dökülen kırıntı raylara ULAŞAMAZ"))
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        ct = kut(45.0, 1695.0, 20.5, 44.0, zc_ - 37.0, zc_ + 37.0).cut(kut(40.0, 1700.0, 19.5, 45.0, zc_ - 33.0, zc_ + 33.0))
        ekle("ray_ortu_catisi_%s" % ad_, ct, "sac",
             bom=("Ray örtü çatısı", 2, "304 1,0 mm · 90 geniş, tepe y 44, ortada 36 yarık", "arabanın olmadığı yerde rayı örter; 24 × M4 havşa") if ad_ == "on" else None)
    ekle("kirinti_cekmecesi", kut(100.0, 1580.0, 4.5, 20.5, -240.0, -212.0).cut(kut(103.0, 1577.0, 6.5, 21.5, -237.0, -215.0)), "sac",
         bom=("Kırıntı çekmecesi", 1, "304 1,0 mm · önden çekilir", "iki ray kirişi arasında; boşaltılıp yıkanır"))
    ekle("enerji_zinciri_kanali", kut(15.0, 1695.0, 4.5, 64.5, -500.0, -440.0).cut(kut(18.0, 1692.0, 6.5, 65.5, -497.0, -443.0)), "sac",
         bom=("Enerji zinciri + kanalı", 1, "iç 15 × 30 · R40 · boy ~840 · kanal 304 1,0 mm 60 × 60",
              "dönüş motoru arabayla gezdiği için ZORUNLU; içinde PUR kılıflı sürükleme-zinciri kablosu (PVC DEĞİL)"))

    # --- 8b.7 SENSÖRLER ve TAMPONLAR ---
    for ad_, xb in (("home", 1520.0), ("limit_sol", 205.0), ("limit_sag", 1535.0)):
        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Endüktif sensör M12 × 50 IP69K PNP NO", 3, "ön ray kirişinin dış yüzüne L braketle", "home x 1520 (istasyon) · limit− 205 · limit+ 1535") if ad_ == "home" else None)
    ekle("x_bayragi", kut(Xc - 30.0, Xc + 30.0, 40.0, 48.5, -24.0, -6.0), "sac",
         bom=("X bayrağı 60 × 25", 1, "304 3 mm", "araba plakasının ön kenarının altında"))
    ekle("tabla_home_sensoru", sily(Xc, ZT - 128.0, 4.0, 66.5, 76.5), "koyu",
         bom=("Tabla home sensörü M8 endüktif IP67", 1, "araba plakasının ÜSTÜNDE braketli", "algılama yüzü YUKARI; arabayla birlikte gezdiği için sabit referansa gerek yok"))
    ekle("tabla_home_bayragi", sily(Xc, ZT - 128.0, 10.0, 86.0, 89.0), "celik",
         bom=("Tabla home bayrağı 3 × 20 × 12", 1, "304 · ayar bileziğine r = 128'de kaynaklı (yatak Ø197 olunca dışarı kaydı)", "boşluk 2,0 mm · robot tepsiyi hep aynı açıda bulmalı"))
    for i_, xb in enumerate((180.0, 1560.0)):
        ekle("uc_tamponu_%d" % i_, silz(xb, 53.5, 10.0, -80.0, -65.0), "silikon",
             bom=("Uç tamponu Ø20 × 15", 2, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil") if i_ == 0 else None)

    for a_, ad_, n_, malz_, gor_ in (
            ("_bom_tabla", "Tabla yasası", 1, "yazılım", "ağız pide merkezine %.0f mm'de 2,5 s bekler, r² doğrusal azalarak %.0f mm'ye iner, 0,3 s bekler [kasar_akis_model_v2]" % (TB["r_dis"], TB["r_ic"])),
            ("_bom_strok", "Strok ve istasyon", 1, "—", "tabla merkezi x 220…1520 (1300 mm) · istasyon SAĞDA x 1520 · dozajda %.1f mm/s, geçişte %.0f mm/s" % (TB["x_doz_hiz"], TB["x_gecis_hiz"])),
            ("_bom_cevrim", "Çevrim", 1, "—", "altı doz 71,0 s → 51 tepsi/h · tipik tek dozlu kaşarlı pide 13,7 s → 262 tepsi/h"),
            ("_bom_civata", "Bağlantı elemanları (tümü A4/A2 paslanmaz)", 180, "15 tip · gıdaya bakan her baş HAVŞA ya da KUBBE",
             "ray 54 × M4×16 · blok 16 × M4×20 · yatak 8 × M5×16 · ayar bileziği 6 × M5×16 · göbek 3 × M8×40 saplama + kelebek somun + 2 pim · dönüş motoru 4 × M5×20 · kayış kolu 4 × M8×25 + 2 pim · kelepçe 4 × M5 + 4 × M4 · X motoru 4 × M5×12 + kaide 4 × M8×25 · avara M8×40 + braket 2 × M8×25 + M6 jack · apron 8 × M4×10 · çatı 24 × M4×8 · sensör 12 × M4×12 · zincir 18 · tampon 2 takım M10")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

    ekle("agiz_alt_dudagi", kut(30.0, 1770.0, 1.5, 13.5, 0.0, -4.5).cut(kut(33.0, 1767.0, 3.5, 15.0, 1.0, -3.0)), "sac",
         bom=("Ağız alt dudağı", 1, "304 1,5 mm bükme · dış tabana ve iki yan saca sürekli kaynak",
              "silinen ağız çerçevesinin tek gerçek işi: robot çarparsa kesmeyen kıvrık kenar — ama YALNIZ ALTTA; üst lama geri konmadı, tepsi çıkışı açık"))

    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------
    # Kemal: "yalıtım parçasının altındaki gri parçayı sil, ne gerek var ona" (damlama teknesi) ·
    # "ön yüzeyde sac parça kalmış havada uçuyor, onu da sil" (ağız çerçevesi — ön çerçeve sacı
    # v7'de kalkınca desteksiz kalmıştı). Damlamayı artık dozaj kovanı + duckbill valf kesiyor.


if __name__ == "__main__":
    t0 = time.time(); modul()
    gercek = [p for p in PARCALAR if not p["ad"].startswith("_bom")]
    print("TOPPING MODULU v10 · %d parca (%d cizili + %d yalniz listede) · %.0f sn" % (len(PARCALAR), len(gercek), len(PARCALAR) - len(gercek), time.time() - t0))
    gecersiz = [p["ad"] for p in gercek if not p["wp"].val().isValid()]
    print("KATI DENETIMI: %s" % ("hepsi gecerli" if not gecersiz else "GECERSIZ: " + ", ".join(gecersiz))); assert not gecersiz

    # ---- zarf ----
    bb = [(p["ad"], p["wp"].val().BoundingBox()) for p in gercek]
    tas = [a for a, b in bb if b.xmin < -0.01 or b.xmax > W + 0.01 or b.ymin < -0.01 or b.ymax > Y + 0.01 or b.zmax > 0.01 or b.zmin < -D - 0.01]
    print("ZARF: %s (%.0f × %.0f × %.0f)" % ("hepsi modulun icinde" if not tas else "TASAN: " + ", ".join(tas), W, Y, D)); assert not tas

    # ---- çakışma ----
    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in gercek]; bulgu = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            try: v = S[i][1].intersect(S[j][1]).Volume()
            except Exception: v = -1.0
            if v > 1.0 or v < 0: bulgu.append((S[i][0], S[j][0], round(v, 1)))
    print("CAKISMA: %s" % ("TEMIZ" if not bulgu else "%d BULGU" % len(bulgu)))
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

    # ---- üretim dosyaları ----
    os.makedirs(os.path.join(URETIM, "step"), exist_ok=True); os.makedirs(os.path.join(URETIM, "stl"), exist_ok=True)
    asm = cq.Assembly(name="TOPPING_MODUL_v1"); RENK = dict(sac=(0.74, 0.77, 0.80, 1), pu=(0.93, 0.88, 0.72, 1), motor=(0.18, 0.19, 0.22, 1),
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
    asm.save(os.path.join(URETIM, "TOPPING_MODUL_v1_MONTAJ.step"))
    with io.open(os.path.join(URETIM, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["dosya", "parça", "adet", "malzeme · yöntem", "görevi", "zarf mm"]); w.writerows(bom)
    with io.open(os.path.join(URETIM, "bom.json"), "w", encoding="utf-8") as f: json.dump(bom, f, ensure_ascii=False)
    print("URETIM: %d STEP + %d STL + MONTAJ.step + BOM.csv (%d kalem) → %s" % (len(gercek), len(gercek), len(bom), URETIM))
    for b in bom: print("   %-22s %-38s ×%-3s %s" % (b[0], b[1], b[2], b[5]))
    sys.stdout.flush(); os._exit(0)
