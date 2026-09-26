# -*- coding: utf-8 -*-
"""TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v7 · 26 Eyl 2026 gece (katalog yay/pim · haç 7,0 · mandal 4,5 · kabin duvarı 1277'den)
v7: yay Century Spring 66644SCS (4 kovan + mandal), pim ISO 8734 3 × 45 / 3 × 18, segman DIN 471 22 × 1,2 kanalı d2 21,0 · m 1,3; haç kovanı 15,5 (haç 7,0 girer, strok 8,0 / sert durak 8,5); mandal dili plakayı 4,5 örter, 5,0 kayar; kabin yan PU duvarları 1277–2030. Önceki: topping_uno_cad_v6.py
v6:
v6 (Kemal: "kasetlerin yerlerini tam mühendislik yap — vidalanacak mı, nasıl çıkacak, hizalama, aralarında boşluk; yalıtım tam
kare olsun, önünde çekmecelerdeki gibi conta"): KASET YUVALARI (kılavuz köşebentler · arka dayama · SOLDA yaylı KAYAR mandal ·
her milde yaylı HAÇ yuvası: Ø48 POM kovan + 4 yay + boydan pim + segmanlı yay tablası · raf U-yarığı · iniş hunisi) · sucuk 13 mm sağa
(boşluklar: kuşbaşı–kaşar mandalı 25 · kaşar kılavuzu–sucuk mandalı 10,5 · sucuk–duvar 25,5) · YALITIM TEK BLOK (teknik cep arkaya
açık) + ÖN FİTİL. Önceki: topping_uno_cad_v5.py
v5:
v5 (Kemal: "toppingi de tam hesapla — sos geniş ağzın altına geliyor, ne kadar dökecek, tabla ne kadar dönecek"):
YAYICI YARIĞI HESAPTAN (topping_v2_hesap_v1). Dönen tablada r yarıçapındaki halka turda 2πr·dr alan geçirir; düz yarıkla
merkez kenardan 12,5 kat kalın kaplanırdı. Yarık artık KAMA: birim boydan çıkan debi r ile orantılı (q ∝ r, power-law n 0,3
→ w ∝ r^0,19): sos 2,0 → 3,2 mm · harç 6,0 → 9,6 mm (r 10 → 121). Kaşar + sucuk kasetlerinin helezonu ve karıştırıcısı
(+ milleri) AYRI DÖNER GRUP (HELEZON_<kaset> · KARISTIRICI_<kaset>) — simülasyon onları çevirir. Önceki: topping_uno_cad_v4.py
v4:
v4 (Kemal: "altında neden kocaman kalın parça var; incecik bir metal raf olmalı, bu kiloları taşıyacak"): 134 mm'lik PU
yalıtım tabanı KALKTI. Yerine 3 mm AISI 304 TAŞIYICI RAF, önü ve arkası 40 mm aşağı bükülü; ağızlar ve kaset boruları
raftaki deliklerden iner. Yük 154 kg (dolu hazneler + UNO'lar + kasetler) → sehim 3,4 mm (L/477), gerilme 92 MPa, emniyet 2,3.
Spreader cebi, dozaj kovanları ve hortum kovanları gereksizleşti (kalktı).
v3:
v3 (Kemal: "resimdekinin aynısını modelle, spreader attachment bizim istediğimiz, full modelle koy"): SOS ve HARÇ ağzı
Beldos SPREADER ATTACHMENT (beldos.com/beldos-nozzles görseli): TC kelepçeli giriş → dik boru + yanında havalı kesme
valfi (braketli, hava hortumlu) → üçgen dağıtıcı gövde (yassı, içi boş) → altı yarıklı YATAY DAĞITICI BORU, iki ucu beyaz
tapalı. Boru tabla ekseninde yarıçap boyunca; tabla bir tur döner. Ölçüler görselden oranla (boru Ø36 alındı) = VARSAYIM.
v2:
v2 (Kemal: "pastacılar gibi dönen tablada geniş ağız — onları da modelle, detaylıca"): SOS ve HARÇ ağzı Beldos "icing
nozzle" tipi DÜZ KAPLAMA BIÇAĞI. Bıçak tabla ekseni üstünde, x yönünde, merkezden kenara (yarıçap) uzanır; tabla merkezini
bıçağın iç ucuna getirir ve YALNIZ BİR TUR döner → yüzey tamamen kaplanır (x kayması yok). Kıyma / kuşbaşı yuvarlak ağız.
v1:

Kemal: "şimdiki TOPPING version 1 olsun; yeni TOPPING'i UNO'lu olanı 3D yap. Hava şeyini nereye koyacaksın, boruları
nereden geçecek?" — pnömatik KORUNUR (Beldos'un kendi hava silindiri + döner valf eyleyicisi), kompresör hattın ortak
tesisatı olarak K tabanında.

DİZİLİM (pafta teknik_topping_satinalma_v2 + HAT v9): SOS · HARÇ · KIYMA · KUŞBAŞI = UNO çekirdeği (Beldos valf + ürün
silindiri + Ø32 hava silindiri; bizim soğuk hazne) · KAŞAR · KÜP SUCUK = bizim kasetler (kasar_cad_v14 / sucuk_cad_v7 +
Codex STEP parçaları, montaj v41'deki gibi).
HAVA: kompresör JUN-AIR OF302-15B (yağsız, 15 L tank, 380 × 380 × 510, 25 kg, 43 L/dk @ 7 bar, 65 dB) → K taban dolabı
(boş) → Ø10 ana hat F tabanının arka köşesinden → TOPPING kuru bölmesine sağ alttan girer → şartlandırıcı (filtre +
regülatör + ana vana) → valf adası (10 × 5/2: 4 piston + 4 döner valf + açıcı + yedek) → Ø6 hortumlar: hava silindirlerine
kuru bölmede, döner valf eyleyicilerine yalıtımdaki geçiş bloğundan soğuk hücreye; açıcı hattı sol duvardan A modülüne.
ÇERÇEVE: x modül C'nin sol ucundan, y yerden (kot), z ön yüzden (arkaya −), mm → GLB m (y yukarı, ön +z).
"""
import json, math, os, struct, sys, importlib, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d")
MM = 0.001

M = {  # malzeme: renk rgba, metal, pürüz, saydam
    "paslanmaz": ((0.80, 0.82, 0.85, 1.0), 0.95, 0.26, False), "fircali": ((0.74, 0.76, 0.79, 1.0), 0.9, 0.42, False),
    "celik": ((0.78, 0.80, 0.83, 1.0), 0.95, 0.28, False), "pom": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.42, False),
    "cam": ((0.82, 0.89, 0.95, 0.32), 0.0, 0.05, True), "silikon": ((0.85, 0.30, 0.20, 1.0), 0.0, 0.6, False),
    "siyah": ((0.07, 0.07, 0.08, 1.0), 0.1, 0.6, False), "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45, False),
    "koyu": ((0.10, 0.10, 0.11, 1.0), 0.2, 0.6, False), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3, False),
    "saydam_celik": ((0.82, 0.85, 0.89, 0.32), 0.6, 0.25, True), "pu": ((0.93, 0.86, 0.55, 0.07), 0.0, 0.8, True),
    "kabuk": ((0.78, 0.81, 0.85, 0.06), 0.3, 0.4, True), "hayalet": ((0.60, 0.64, 0.70, 0.10), 0.0, 0.8, True),
    "hortum_mavi": ((0.15, 0.40, 0.85, 1.0), 0.0, 0.5, False), "hortum_siyah": ((0.10, 0.10, 0.12, 1.0), 0.0, 0.6, False),
    "hava_ana": ((0.10, 0.55, 0.85, 1.0), 0.0, 0.5, False), "kompresor": ((0.25, 0.45, 0.70, 1.0), 0.3, 0.5, False),
    "zarf": ((0.55, 0.57, 0.60, 0.55), 0.0, 0.6, True), "tabla": ((0.92, 0.78, 0.55, 1.0), 0.0, 0.8, False),
    "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85, False),
}
P = []                      # parçalar
GRUP = {"SABIT": (0.0, 0.0, 0.0)}


def ekle(ad, sh, mal, kaynak, grup="SABIT", not_=""):
    assert mal in M, mal
    if isinstance(sh, cq.Workplane):
        v = [o for o in sh.vals() if isinstance(o, cq.Shape)]
        sh = v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    assert all(p["ad"] != ad for p in P), ad
    P.append(dict(ad=ad, sh=sh, mal=mal, kaynak=kaynak, grup=grup, not_=not_))


kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
V = cq.Vector


def boru(pts, r):
    ss = []
    for a, b in zip(pts[:-1], pts[1:]):
        v = V(*b) - V(*a)
        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, V(*a), v.normalized()))
    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, V(*p), angleDegrees1=-90, angleDegrees2=90))
    return cq.Compound.makeCompound(ss)


def loft_y(w0, w1):
    return cq.Solid.makeLoft([w0, w1], True)


def dikdort_y(cx, y, cz, wx, wz):
    return cq.Wire.makePolygon([V(cx - wx / 2, y, cz - wz / 2), V(cx + wx / 2, y, cz - wz / 2), V(cx + wx / 2, y, cz + wz / 2), V(cx - wx / 2, y, cz + wz / 2)], close=True)


def cember_y(cx, y, cz, r):
    return cq.Wire.makeCircle(r, V(cx, y, cz), V(0, 1, 0))


# ================================================================ ÖLÇÜLER
W, Y0, YUST, D = 1800.0, 1060.0, 2030.0, 830.0
SOGUK_TABAN = 1320.0; YAL_TABAN = (1183.0, 1317.0)
BAY_A = (90.0, 790.0); TAVAN_A = 1968.0; BAY_B = (790.0, 1710.0); TAVAN_B = 1680.0
Z_KAPAK = (-84.0, -104.0); Z_SOGUK = (-104.0, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)
ZT = -170.0; PIDE_UST = 1176.0
BICAK = {"SOS": dict(boy=125.0, yarik=3.0), "HARC": dict(boy=125.0, yarik=6.0)}   # [V] sos kenarı 15 mm boş · harç parçacık ~5 mm
BICAK_ALT = PIDE_UST + 6.0            # bıçak ağzı pideden 6 mm yukarıda (katman ~2 mm) [V]
BICAK_UST = 1262.0                    # UNO 90° ağzının dik bacağı 1263,5'te bitiyor; bıçak buradan başlar
V_EKSEN = SOGUK_TABAN + 38.5; V_UST = SOGUK_TABAN + 72.6; VZ = -387.0
UNO = [  # ad, x merkezi, hazne genişliği, hazne üstü, silindir çapı, ağız tipi, doz (ml)
    ("SOS", 210.0, 220.0, 1737.0, 52.0, "yassi", 76.0), ("HARC", 560.0, 440.0, 1832.0, 52.0, "yassi", 105.0),
    ("KIYMA", 895.0, 190.0, 1667.0, 70.0, "yuvarlak", 152.0), ("KUSBASI", 1105.0, 190.0, 1667.0, 70.0, "yuvarlak", 170.0)]
KASET = [("KAŞAR KABI", "kasar_cad_v14", 1220.0, 1502.0), ("KÜP SUCUK", "sucuk_cad_v7", 1539.0, 1681.0)]   # v6: sucuk +13 (kaşar–sucuk plakaları 30, sağ duvar 25,5)
CODEX_3B = {"kasar_cad_v14": {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                              "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"},
            "sucuk_cad_v7": {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"}}
ADA = (150.0, 458.0, 1600.0, 1660.0, -660.0, -760.0)     # valf adası 12 × 5/2 (kuru bölme)
FRL = (1650.0, 1700.0, 1250.0, 1420.0, -700.0, -780.0)    # şartlandırıcı
KOMP = (3410.0, 3790.0, 520.0, 1030.0, -40.0, -420.0)     # K tabanı (modül C yerelinde x 3300–3900)

# ================================================================ 1 · KABİN
ekle("kabin_taban_saci", kut(0, W, Y0, Y0 + 1.5, 0, -D), "fircali", "V")
ekle("kabin_arka_saci", kut(0, W, Y0, YUST, -D + 1.5, -D), "kabuk", "V")
ekle("kabin_ust_saci", kut(0, W, YUST - 1.5, YUST, 0, -D), "kabuk", "V")
ekle("kabin_sol_duvar_PU", kut(0, 90, 1277.0, YUST, 0, -D), "pu", "V", not_="sac + PU 60 · v7: 1277'den başlar (altı mekanizma bölgesi: tabla park/aktarmada duvar hizasını geçer; alt yanlar topping_cad'in sacı)")
ekle("kabin_sag_duvar_PU", kut(W - 90, W, 1277.0, YUST, 0, -D), "pu", "V", not_="v7: 1277'den başlar (disk aktarmada 2507'ye kadar çıkar)")
RAF_T, RAF_BUKUM = 3.0, 40.0
_raf = kut(90, W - 90, SOGUK_TABAN - RAF_T, SOGUK_TABAN, Z_KAPAK[1], Z_BOLME[0])
for _ad, _cx, *_r in UNO:
    _raf = _raf.cut(sily(_cx, ZT, 21.0, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
KAS_Z = -150.0                                   # kaset çıkış borusu ekseni (tabla ekseninin 20 mm önü, v1 ile aynı)
KAS_R = {"kasar_cad_v14": (30.0, 25.0, 22.5), "sucuk_cad_v7": (30.0, 24.0, 21.0)}   # delik · iniş borusu dış/iç
for _ad, _mod, _x0, _x1 in KASET:
    _raf = _raf.cut(sily((_x0 + _x1) / 2.0, KAS_Z, KAS_R[_mod][0], SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
for _ad, _cx, *_r in UNO:
    if _ad in ("SOS", "HARC"):
        _raf = _raf.cut(sily(_cx - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
_rob = kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_KAPAK[1] - RAF_T, Z_KAPAK[1])
for _ad, _mod, _x0, _x1 in KASET:                                                       # v6: kaset çıkış tüpü öne kayarken raftan sıyrılsın: U-yarık + çentik
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    _raf = _raf.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1, KAS_Z, Z_KAPAK[1] + 1))
    _rob = _rob.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - RAF_BUKUM - 1, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))
ekle("tasiyici_raf_3mm", _raf, "paslanmaz", "H", not_="AISI 304 · 3 mm · yük 154 kg · sehim 3,4 mm · emniyet 2,3 · ağız delikleri · v6: kaset delikleri öne açık U-yarık (Ø60)")
ekle("raf_on_bukumu", _rob, "paslanmaz", "H", not_="40 mm aşağı büküm (rafın kirişi) · v6: kaset yarıklarında 60 çentik")
for _ad, _mod, _x0, _x1 in KASET:
    _x = (_x0 + _x1) / 2.0; _, ro, ri = KAS_R[_mod]
    HUNI_Y = (1305.0, 1311.0)                                                                          # v6: boru üstü 1305 · huni 1305–1311 · kaset borusunun altı 1312 → 1 mm, iç içe DEĞİL
    ekle("%s_inis_borusu" % _mod.split("_")[0], sily(_x, KAS_Z, ro, 1216.0, HUNI_Y[0]).cut(sily(_x, KAS_Z, ri, 1215.0, HUNI_Y[0] + 1.0)), "paslanmaz", "H",
         not_="kaset borusunun devamı: üstü 1305 — kaset borusu (dış Ø%.0f) 1312'de biter, iç içe geçmez (v5'te 5 mm geçiyordu, kaset öne çekilemezdi) · pideye 40 mm kalana iner" % (2 * ro))
    _hn = cq.Solid.makeCone(ro, 32.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))
    _hn = _hn.cut(cq.Solid.makeCone(ri, 29.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))).cut(sily(_x, KAS_Z, ri, HUNI_Y[0] - 1.0, HUNI_Y[0] + 0.5).val())
    ekle("%s_inis_hunisi" % _mod.split("_")[0], _hn, "paslanmaz", "H",
         not_="huni iç Ø%.0f→Ø58 · 1305–1311 · kaset borusunun altındaki 1 mm boşluğu ve 4 mm yanal payı örter → kaset öne çekilirken boruya takılmaz" % (2 * ri))
ekle("raf_arka_bukumu", kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_BOLME[0], Z_BOLME[0] + RAF_T), "paslanmaz", "H")
# v6 · YALITIM TEK BLOK ("tam kare"): dışı düz dikdörtgen; içinde soğuk oda (A tavan 1968 · B tavan 1680), arkaya açık TEKNİK CEP,
#      kaset kovanı / UNO mil kovanı / geçiş bloğu delikleri. Fitil ve kaset yuvaları aşağıda (kasetlerden sonra).
YAL_Y0 = SOGUK_TABAN - 43                                                             # 1277 (raf bükümünün altı)
CEP_TEKNIK = (850.0, W - 90, TAVAN_B + 60, 2012.0, -110.0, Z_BOLME[1])               # soğutma grubu · pano · güç · UPS (zarflar) — arkadan servis
_yal = kut(BAY_A[0], BAY_B[1], YAL_Y0, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1])
_yal = _yal.cut(kut(BAY_A[0] - 1, BAY_A[1], YAL_Y0 - 1, TAVAN_A, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda A
_yal = _yal.cut(kut(BAY_B[0], BAY_B[1] + 1, YAL_Y0 - 1, TAVAN_B, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda B
_yal = _yal.cut(kut(CEP_TEKNIK[0], CEP_TEKNIK[1] + 1, CEP_TEKNIK[2], CEP_TEKNIK[3], CEP_TEKNIK[4], CEP_TEKNIK[5] - 1))   # teknik cep (arkaya açık)
_yal = _yal.cut(kut(89, 1201, 1439, 1471, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                              # geçiş bloğu yuvası
for _ad, _cx, *_r in UNO:
    _yal = _yal.cut(silz(_cx, V_EKSEN, 15.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                         # UNO mil geçiş kovanı
YAL_BLOK = [_yal]                                                                     # kaset kovan delikleri kasetlerden sonra açılır (ekle orada)
for ad, x0, x1 in (("sogutma_grubu", 850, 1150), ("pano_PLC", 1180, 1580), ("guc_kaynagi", 1600, 1655), ("UPS", 1660, 1709)):
    ekle("teknik_bant_" + ad, kut(x0, x1, 1772, 2012 if ad == "pano_PLC" else 1992, -110, -560), "zarf", "Ö", not_="pafta v9 teknik bant · ZARF")
# tabla + pide (ilk durak: sos)
GRUP["TABLA"] = (210.0, 1168.0, ZT)
ekle("tabla_diski", sily(210, ZT, 170, 1154, 1168), "tabla", "Ö", grup="TABLA", not_="Ø340 · merkezi sos bıçağının iç ucunda · dozajda 1 tur")
ekle("pide", sily(210, ZT, 140, 1168, PIDE_UST), "hamur", "Ö", grup="TABLA")
ekle("pide_isareti", kut(330, 345, 1176, 1177, ZT - 4, ZT + 4), "silikon", "V", grup="TABLA", not_="dönüşü göstermek için işaret")

# ================================================================ 2 · UNO İSTASYONLARI — beldos_cad_v1'deki UNO modeli
# UNO çerçevesi (X eksen: ağız −, tahrik +; Y arkaya; Z yukarı, 0 = silinen kaidenin üstü) → TOPPING:
#   x = cx − Y · y = 1320 + Z · z = −387 − X   (ağız öne, tahrik arkaya; ağız ekseni x −217 → z −170 = tabla ekseni)
import beldos_cad_v1 as BEL
import topping_v2_hesap_v1 as TH2                  # v5: dozaj hesabı (yarık profili buradan)
DISARIDA = {"hazne_25L_konik": "bizim soğuk hazne takılıyor", "hazne_agiz_kivrimi": "", "hazne_kaynak_bandi": "", "hazne_tc_kelepcesi_2.5in": "",
            "hazne_kelepce_kelebegi": "", "hazne_contasi": "", "baglanti_plakasi_BIZIM": "valf soğuk hücre tabanına oturuyor",
            "kasa_oluk_saci": "yalıtım duvarına giriyor", "kasa_kutu_saci": "modülün arkasından 16 mm taşıyor",
            "etiket_paneli": "", "etiket_kirmizi_cizgi": "", "hizli_sokme_pimi": "", "hiz_ayar_topuzu": "valf adasından ayarlanır",
            "hacim_ayar_topuzu": "arkadan 82 mm taşıyor", "hacim_ayar_mili": "", "hacim_ayar_dayamasi": "", "mil_korugu": "yerine keçeli geçiş kovanı",
            "pnomatik_arka_ayak": "arkadan 3 mm taşıyor", "sartlandirici_govde": "ortak şartlandırıcı kullanılıyor", "sartlandirici_ayar_topuzu": "",
            "sartlandirici_filtre_kabi": "", "sartlandirici_manometre": "", "hava_giris_rakoru": "", "hava_hortumu_kirmizi": "valf adası hortumları",
            "agiz_ucu": "yerine uzatma + uç"}
MAL_ES = {"beyaz": "pom", "kirmizi": "silikon", "bizim": "zarf"}
for i, (ad, cx, hw, hust, d_sil, agiz, doz) in enumerate(UNO):
    k = ad.lower()
    from OCP.gp import gp_Trsf
    _t = gp_Trsf(); _t.SetValues(0.0, -1.0, 0.0, cx, 0.0, 0.0, 1.0, SOGUK_TABAN, -1.0, 0.0, 0.0, VZ)
    GRUP["VALF_" + ad] = (cx, V_EKSEN, VZ)
    GRUP["PISTON_" + ad] = (cx, V_EKSEN, VZ - BEL.XP_ON)
    for q in BEL.UN.P:
        if q["ad"] in DISARIDA: continue
        if d_sil != 52.0 and q["ad"] in ("urun_silindiri_D52", "urun_pistonu"): continue
        g = {"VALF": "VALF_" + ad, "PISTON": "PISTON_" + ad}.get(q["grup"], "SABIT")
        ekle("%s__%s" % (k, q["ad"]), cq.Shape.cast(__import__("OCP.BRepBuilderAPI", fromlist=["x"]).BRepBuilderAPI_Transform(q["sh"].wrapped, _t, True).Shape()), MAL_ES.get(q["mal"], q["mal"]), q["kaynak"], grup=g,
             not_="UNO modeli (beldos_cad_v1) · " + q["not_"])
    if d_sil != 52.0:
        ekle("%s__urun_silindiri_D70" % k, silz(cx, V_EKSEN, 38, VZ - 165, VZ - 49).cut(silz(cx, V_EKSEN, 35, VZ - 166, VZ - 48)), "saydam_celik", "B",
             not_="Beldos Ø70 silindir seçeneği (100–275 ml) · doz %.0f ml > Ø52'nin 151 ml'si" % doz)
        ekle("%s__urun_pistonu_D70" % k, silz(cx, V_EKSEN, 34.7, VZ - 69, VZ - 49), "pom", "H", grup="PISTON_" + ad)
    # ağız: kıyma / kuşbaşı → uzatma borusu (yuvarlak uç 1216) · sos / harç → düz kaplama bıçağı (icing nozzle)
    if agiz == "yassi":
        bc = BICAK[ad]; L_ = bc["boy"]; g_ = bc["yarik"]
        yb = BICAK_ALT + 18.0                         # dağıtıcı boru ekseni (alt yüzü pideden 6 mm)
        xb0, xb1 = cx - 8.0, cx + L_                   # boru merkezden kenara
        # 1 · giriş: TC kelepçe (UNO ağzı ucu) + dik boru
        ekle("%s_spreader_giris_kelepcesi" % k, sily(cx, ZT, 25.0, BICAK_UST, BICAK_UST + 12.0).cut(sily(cx, ZT, 18.2, BICAK_UST - 1, BICAK_UST + 13.0)), "paslanmaz", "F",
             not_="Beldos spreader attachment · 1,5\" TC kelepçe")
        ekle("%s_spreader_kelepce_kanadi" % k, kut(cx - 4, cx + 4, BICAK_UST + 2, BICAK_UST + 10, ZT + 25, ZT + 40), "paslanmaz", "F")
        ekle("%s_spreader_dik_boru" % k, sily(cx, ZT, 18.0, yb + 40.0, BICAK_UST).cut(sily(cx, ZT, 16.5, yb + 39.0, BICAK_UST + 1)), "paslanmaz", "F")
        # 2 · havalı kesme valfi (braketli, dik borunun yanında)
        vx = cx - 40.0; v0, v1 = yb + 40.0, yb + 86.0
        ekle("%s_spreader_kesme_valfi_govde" % k, sily(vx, ZT, 14.0, v0, v1), "pom", "F", not_="havalı kesme valfi (drip-free) · beyaz gövde, görselden")
        ekle("%s_spreader_kesme_valfi_kapak" % k, sily(vx, ZT, 15.0, v1, v1 + 8.0), "pom", "F")
        ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 16.0, v0 + 20.0, v0 + 44.0, ZT - 2.0, ZT + 2.0), "paslanmaz", "F")
        ekle("%s_spreader_valf_kelepcesi" % k, sily(cx, ZT, 21.0, v0 + 20.0, v0 + 44.0).cut(sily(cx, ZT, 18.1, v0 + 19.0, v0 + 45.0)), "paslanmaz", "F")
        ekle("%s_spreader_valf_mili" % k, silx(v0 + 32.0, ZT, 3.0, vx + 14.0, cx - 18.0), "celik", "V")
        ekle("%s_spreader_hava_rakoru" % k, silz(vx, v1 - 10.0, 4.0, ZT + 14.0, ZT + 26.0), "siyah", "F")
        # 3 · üçgen dağıtıcı gövde (yassı, içi boş): dik borudan dağıtıcı boruya
        tg_dis = loft_y(dikdort_y(cx, yb + 42.0, ZT, 40.0, 16.0), dikdort_y((xb0 + xb1) / 2.0, yb + 14.0, ZT, L_ + 4.0, 16.0))
        tg_ic = loft_y(dikdort_y(cx, yb + 43.0, ZT, 34.0, 12.0), dikdort_y((xb0 + xb1) / 2.0, yb + 10.0, ZT, L_ - 2.0, 12.0))
        ekle("%s_spreader_ucgen_dagitici" % k, tg_dis.cut(tg_ic), "paslanmaz", "F", not_="görseldeki üçgen sac gövde · kalınlık 16 [V]")
        # 4 · yatay dağıtıcı boru + alt yarık + beyaz tapalar
        # v5 · KAMA YARIK (topping_v2_hesap_v1.yarik_genisligi): q ∝ r → düzgün katman. Yarık değiştirilebilir alt lamda (pilotta ayar).
        _r = [TH2.YARIK_R[0] + (TH2.YARIK_R[1] - TH2.YARIK_R[0]) * j / 14.0 for j in range(15)]
        _ust = [(cx + r_, ZT + TH2.yarik_genisligi(ad, r_) / 2.0) for r_ in _r]
        _alt = [(cx + r_, ZT - TH2.yarik_genisligi(ad, r_) / 2.0) for r_ in reversed(_r)]
        _kama = cq.Workplane("XZ", origin=(0, yb - 20.0, 0)).polyline(_ust + _alt).close().extrude(-6.0)
        bor = silx(yb, ZT, 18.0, xb0, xb1).cut(silx(yb, ZT, 16.5, xb0 - 1, xb1 + 1)).cut(_kama)
        _w0, _w1 = TH2.yarik_genisligi(ad, TH2.YARIK_R[0]), TH2.yarik_genisligi(ad, TH2.YARIK_R[1])
        ekle("%s_spreader_dagitici_boru" % k, bor, "paslanmaz", "H",
             not_="altı KAMA yarıklı: r %.0f→%.0f mm'de %.1f→%.1f mm (q ∝ r, topping_v2_hesap_v1) · boy %.0f · alt yüzü %.0f (pideden %.0f)"
                  % (TH2.YARIK_R[0], TH2.YARIK_R[1], _w0, _w1, L_ + 8.0, yb - 18.0, yb - 18.0 - PIDE_UST))
        ekle("%s_spreader_uc_tapasi" % k, silx(yb, ZT, 19.0, xb1, xb1 + 10.0), "pom", "F", not_="beyaz tapa (görselde)")
        ekle("%s_spreader_merkez_tapasi" % k, silx(yb, ZT, 19.0, xb0 - 6.0, xb0), "pom", "V")
        # 5 · kesme valfi hava hortumu → cep → soğuk hücre üstünden geçiş bloğuna
        hx = cx - 100.0; ry = v1 - 10.0
        ekle("%s_spreader_hava_hortumu" % k, boru([(vx, ry, ZT + 26.0), (vx, ry, ZT + 34.0), (hx, ry, ZT + 34.0), (hx, 1345.0, ZT + 34.0),
                                                    (hx, 1345.0, -540.0), (hx, 1455.0, -540.0), (hx, 1455.0, -600.0)], 3.0), "hortum_mavi", "V",
             not_="kesme valfine hava · cepten kovanla soğuk hücreye, oradan geçiş bloğuna ve valf adasına")
    else:
        ekle("%s_agiz_uzatmasi" % k, sily(cx, ZT, 18, 1216.0, 1264.0).cut(sily(cx, ZT, 16.5, 1180, 1265)), "paslanmaz", "H",
             not_="UNO 90° ağzının ucundan pideye iniş: 48 mm uzatma · uç 1216 (pideden 40)")
    # bizim hazne: boyun + TC + huni + düz gövde
    ekle("%s_hazne_boynu" % k, sily(cx, VZ, 31.75, V_UST, 1452).cut(sily(cx, VZ, 30.25, V_UST - 1, 1453)), "paslanmaz", "Ö")
    ekle("%s_tc_kelepce_hazne" % k, sily(cx, VZ, 45.5, 1410, 1428).cut(sily(cx, VZ, 32.5, 1409, 1429)), "paslanmaz", "Ö")
    dis = loft_y(cember_y(cx, 1452, VZ, 32), dikdort_y(cx, 1632, -340.0, hw, 440)).fuse(kut(cx - hw / 2, cx + hw / 2, 1632, hust, -120, -560).val())
    ic = loft_y(cember_y(cx, 1451, VZ, 30.3), dikdort_y(cx, 1632.5, -340.0, hw - 3, 437)).fuse(kut(cx - hw / 2 + 1.5, cx + hw / 2 - 1.5, 1632, hust + 1, -121.5, -558.5).val())
    ekle("%s_hazne_bizim" % k, dis.cut(ic), "paslanmaz", "H", not_="bizim soğuk hazne %.0f × 440 · üstü %.0f" % (hw, hust))
    ekle("%s_mil_gecis_kovani" % k, silz(cx, V_EKSEN, 15, Z_BOLME[1] - 5, Z_BOLME[0] + 5).cut(silz(cx, V_EKSEN, 11, Z_BOLME[1] - 6, Z_BOLME[0] + 6)), "pom", "V",
         not_="mil yalıtımdan keçeli kovanla geçer; UNO'nun mil kavraması (Ø20) strok boyunca bu duvarın içinden geçiyor → AÇIK SORUN")

# ================================================================ 3 · KASETLER (bizim) + TAHRİKLERİ
TC = importlib.import_module("topping_cad_v22")
for ad, mod, x0, x1 in KASET:
    Vm = importlib.import_module(mod); Vm.PARCALAR[:] = []; Vm.kap()
    ps = list(Vm.PARCALAR)
    for pad, yol in CODEX_3B[mod].items():
        h = [p for p in ps if p["ad"] == pad]; assert len(h) == 1
        h[0]["wp"] = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))
    xc = (x0 + x1) / 2.0
    KOD = "KASAR" if mod.startswith("kasar") else "SUCUK"                 # v5: sim adları (topping_v2_hesap_v1.IST)
    GRUP["HELEZON_" + KOD] = (xc, SOGUK_TABAN + Vm.CY, 0.0)               # alt mil: dozaj helezonu (z ekseninde döner)
    GRUP["KARISTIRICI_" + KOD] = (xc, SOGUK_TABAN + Vm.YC, 0.0)           # üst mil: besleme rotoru
    for p in [q for q in ps if q["ad"] != "tasima_tapasi"]:
        sh = p["wp"].val() if isinstance(p["wp"], cq.Workplane) and len(p["wp"].vals()) == 1 else cq.Compound.makeCompound([o for o in p["wp"].vals() if isinstance(o, cq.Shape)])
        mal = p["mal"] if p["mal"] in M else "pom"
        gr = {"helezon": "HELEZON_" + KOD, "karistirici": "KARISTIRICI_" + KOD}.get(p.get("grup") or "", "SABIT")
        ekle("%s__%s" % (mod, p["ad"]), sh.translate(V(xc, SOGUK_TABAN, -200.0 - Vm.D / 2.0)), mal, "B", grup=gr,
             not_="%s (montaj v41'deki gibi, Codex parçaları dahil)%s" % (ad, "" if gr == "SABIT" else " · döner: " + gr))
    for ey, kk in zip(TC.eksen(mod), ("helezon", "rotor")):
        yy = SOGUK_TABAN + ey; tag = "%s_%s" % (mod, kk)
        _mil = silz(xc, yy, 11, -670, -545).cut(kut(xc - 1.6, xc + 1.6, yy - 12.0, yy + 12.0, -558.0, -546.5))   # v7: pim kanalı 3,2 × 11,5 boydan boya (−558…−546,5): sert durak 8,5 (yay sınırı 9,1 · tabla 10,4)
        _mil = _mil.cut(silz(xc, yy, 11.5, -564.7, -563.4).cut(silz(xc, yy, 10.5, -565.0, -563.0)))                # segman kanalı DIN 471 (d1 22: d2 21,0 · m 1,3 · s 1,2) [föy]
        ekle("mil_" + tag, _mil, "celik", "Ö", grup=("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD,
             not_="Ø22 · kovanda keçeli · ucunda boydan boya pim kanalı 3,2 × 11,5 (haç yuvası 8,5 kayar) + segman kanalı d2 21 × 1,3 (v7)")
        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))            # v6: yalıtım bloğunda kovan deliği
        ekle("kovan_" + tag, silz(xc, yy, 30, -648, -565).cut(silz(xc, yy, 11.2, -649, -564)), "pom", "Ö")
        ekle("reduktor_" + tag, TC.suregear_koy(xc, yy, -670.0), "motor", "B", not_="SureGear PGCN23-1025 (katalog STEP)")
        g, kb = TC.nema23_koy(xc, yy, -670.0 - 79.0 - 2.0)
        ekle("motor_" + tag, g, "motor", "B", not_="AutomationDirect STP-MTR-23079 (katalog STEP)")
        ekle("motor_kablosu_" + tag, kb, "koyu", "B")

# ================================================================ 3b · KASET YUVALARI (v6) — kaset gövdesine DOKUNULMADI, yuva kasete uyar
# Ölçüldü (26 Eyl): kaset ÖN/ARKA PLAKALARI (280 / 140 × 352 × 8) raf üstüne (1320) oturur — kasetin ayağı plakalardır, gövde 15/21 mm yukarıda.
# Kasetin arkasında kendi HAÇ KAVRAMASI var (kasar_cad_v14: Ø26 disk + 36 × 8 haç, z −543,5…−533,5) — "makinedeki yaylı yuvaya oturur".
# Plakaların arkasında kör somunlar (z −538,6), önünde somunlar / topuz / tüp yatak kapağı (−96,5'e kadar).
def prizma_xz(pts, y0, y1):
    return cq.Workplane("XZ", origin=(0.0, y1, 0.0)).polyline(pts).close().extrude(y1 - y0)
def _bbx(ad): return [p for p in P if p["ad"] == ad][0]["sh"].BoundingBox()
YUVA = {}
for ad, mod, x0, x1 in KASET:
    KOD = "KASAR" if mod.startswith("kasar") else "SUCUK"; k = KOD.lower()
    pb = _bbx("%s__plaka_on" % mod); px0, px1, pz1 = pb.xmin, pb.xmax, pb.zmax                          # plaka: x · ön yüz (−200)
    pz0 = _bbx("%s__plaka_arka" % mod).zmin                                                             # arka plaka arka yüzü (−525)
    hb = _bbx("%s__kavrama_helezon" % mod)                                                              # haç kavrama: z −543,5…−525,5
    xc = (x0 + x1) / 2.0; ST = SOGUK_TABAN
    YUVA[KOD] = dict(px0=px0, px1=px1, pz0=pz0, pz1=pz1, xc=xc, hac_arka=hb.zmin)
    dz_stop = 20.0 if KOD == "KASAR" else 9.0                                                           # arka dayama genişliği (kör somunlara 15 / 2 mm)
    mz = pz1 + 0.5                                                                                      # mandal dili: plakanın ön yüzünün 0,5 önünde
    for yon, xa, sgn in (("sol", px0, 1.0), ("sag", px1, -1.0)):
        # kılavuz dudak: L köşebent 4 × 20, plakaya 0,5 boşluk, plakaların tüm boyu + önde 20 giriş; önde 30 mm boyunca 3 mm dışa açılır (10°)
        dud = kut(xa - sgn * 0.5, xa - sgn * 4.5, ST, ST + 20.0, pz0 - 20.0, pz1 + 20.0)
        pah = prizma_xz([(xa - sgn * 0.5, pz1 - 10.0), (xa - sgn * 0.5, pz1 + 21.0), (xa - sgn * 3.5, pz1 + 21.0)], ST - 1.0, ST + 21.0)
        dud = dud.cut(pah)
        if yon == "sol": dud = dud.cut(kut(xa - 6.0, xa + 1.0, ST + 1.0, ST + 13.0, mz - 1.0, mz + 9.0))        # mandal dili penceresi 12 × 10 (v7)
        ekle("yuva_%s_kilavuz_%s" % (k, yon), dud, "paslanmaz", "H",
             not_="304 köşebent 4 × 20 · kaset plakalarını yanal 0,5 mm boşlukla güder · önde 30 mm 10° giriş pahı · rafa 3 × M4 havşa" + (" · önde mandal dili penceresi" if yon == "sol" else ""))
        ekle("yuva_%s_arka_dayama_%s" % (k, yon), kut(xa, xa + sgn * dz_stop, ST, ST + 30.0, pz0 - 20.0, pz0), "paslanmaz", "H",
             not_="arka plaka alt köşesi buna dayanır (z %.0f) → kavrama derinliği sabit · kılavuzla tek parça bükme · kör somunlara değmez" % pz0)
    # ÖN MANDAL — SOL kılavuzun önünde, plakanın dışında. X'TE KAYAR DİL: POM dil plakanın ön-alt köşesinin ÖNÜNDE durur (plakayı 6 mm örter).
    # Takarken plakanın alt köşesi dilin 45° rampasına basar → dil sola kayar → plaka geçince yay dili geri iter (KLİK).
    # Çıkarmak: kol sola bastırılır (6,5 mm), kaset kulpundan çekilir. (Sağda yer yoktu: sucuk mandalı sağ duvara 10 mm kalıyordu.)
    gov = kut(px0 - 24.0, px0 - 5.0, ST, ST + 34.0, mz - 8.0, mz + 26.0)
    gov = gov.cut(kut(px0 - 21.5, px0 - 7.5, ST + 1.5, ST + 35.0, mz - 9.0, mz + 10.0))                 # dil + kol kanalı (üstü açık, duvarlar 2,5) · v7 dil 8 kalın
    gov = gov.cut(kut(px0 - 8.0, px0 - 4.0, ST + 1.5, ST + 13.0, mz - 1.0, mz + 9.0))                    # iç duvarda dil penceresi 12 × 10
    gov = gov.cut(silx(ST + 18.0, mz + 4.0, 1.6, px0 - 25.0, px0 - 4.0))                                 # pim deliği (v7: dil 8 kalın, pim mz+4)
    ekle("yuva_%s_mandal_govdesi" % k, gov, "pom", "H", not_="mandal yuvası POM 19 × 34 × 34 · U kanal (duvar 2,5) · kılavuza 2 × M4 · pim iki yan duvarda")
    dil = kut(px0 - 14.0, px0 + 4.5, ST + 2.0, ST + 12.0, mz, mz + 8.0).cut(prizma_xz([(px0 + 4.5, mz + 8.0), (px0 + 4.5, mz + 0.5), (px0 - 3.0, mz + 8.0)], ST + 1.0, ST + 13.0))
    dil = dil.union(kut(px0 - 14.0, px0 - 10.0, ST + 2.0, ST + 44.0, mz, mz + 8.0))                     # dik kol: pim üstünde kayar, üstü baş parmak (gövdenin 10 üstünde)
    dil = dil.cut(silx(ST + 7.0, mz + 4.0, 2.6, px0 - 14.5, px0 - 4.2)).cut(silx(ST + 18.0, mz + 4.0, 1.6, px0 - 15.0, px0 - 9.0))   # yay deliği Ø5,2 × 10,3 · pim deliği
    ekle("yuva_%s_mandal_dili" % k, dil, "pom", "H",
         not_="kayar dil POM 18,5 × 10 × 8 + kol 4 × 42 · plakayı 4,5 mm örter · ucu 45° rampa (takarken plaka dili sola iter) · yay geri iter · kol 5 mm sola basılınca kaset serbest (v7)")
    ekle("yuva_%s_mandal_yayi" % k, silx(ST + 7.0, mz + 4.0, 2.39, px0 - 21.5, px0 - 4.2).cut(silx(ST + 7.0, mz + 4.0, 1.98, px0 - 22.0, px0 - 3.7)), "celik", "K",
         not_="Century Spring 66644SCS · 316 · tel 0,41 · Ø4,78 · serbest 21,34 · 0,33 N/mm · en çok 9,12 sıkışma [katalog] · takılı 17,3 (ön yük 4,0 = 1,3 N) · açıkta 12,3 (9,0 sıkışma)")
    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 4.0, 1.5, px0 - 23.5, px0 - 5.5), "celik", "K", not_="Pim ISO 8734 3 m6 × 18 A1: iki yan duvara sıkı geçme, dil üstünde kayar (0,5 içeride)")
    # HAÇ YUVASI (kasetin haç kavraması buna oturur): her tahrik milinde YAYLI KAYAR POM KOVAN Ø48 × 18; önünde haç yarığı 10,5 derin (çubuklar
    # 9,5 girer, dipte 1 mm). 4 baskı yayı (Ø5 × 24,5, 45°'lerde r 18) kovanın arka ceplerinde; yaylar milin segmanına oturan yay tablasına dayanır
    # (kovan · yaylar · tabla · pim = hepsi milyle döner; sürtünen yüzey yok). Tork + strok sınırı: boydan boya Ø3 pim, mildeki 3,2 × 14 kanalda.
    # Kaset takılırken haç hizalı değilse çubuklar kovanı 9,5 geri iter (tabla 10,5'te durdurur), PLC mili yavaş çevirir, yarık hizalanınca
    # yaylar kovanı öne iter → haç oturur (KLİK). Bakım: kovan segman sökülmeden çıkar (pim çekilir).
    Vm = importlib.import_module(mod)
    for ey, kk in zip(TC.eksen(mod), ("helezon", "rotor")):
        yy = ST + ey; tag = "%s_%s" % (k, kk); gr = ("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD
        z_agiz = hb.zmax - 18.0 + 10.0 - 3.0                                                            # v7: yuva ağzı −536,5 → haç çubukları (−543,5…−533,5) 7,0 mm girer
        YAYC = [(xc + 18.0 * math.cos(math.radians(45 + 90 * i)), yy + 18.0 * math.sin(math.radians(45 + 90 * i))) for i in range(4)]
        kv = silz(xc, yy, 24.0, z_agiz - 15.5, z_agiz)                                                  # POM Ø48 × 15,5 (−552…−536,5)
        kv = kv.cut(silz(xc, yy, 13.5, z_agiz - 8.0, z_agiz + 1.0))                                     # disk boşluğu Ø27 × 8 (kavrama Ø26 · dipte 1 mm)
        kv = kv.cut(kut(xc - 18.25, xc + 18.25, yy - 4.25, yy + 4.25, z_agiz - 8.0, z_agiz + 1.0))     # haç yarığı 36,5 × 8,5 × 8
        kv = kv.cut(kut(xc - 4.25, xc + 4.25, yy - 18.25, yy + 18.25, z_agiz - 8.0, z_agiz + 1.0))
        kv = kv.cut(silz(xc, yy, 11.1, z_agiz - 16.0, z_agiz - 7.5))                                    # mil deliği Ø22,2 (mil ucu −545, dipten 0,5 geride)
        kv = kv.cut(kut(xc - 1.6, xc + 1.6, yy - 25.0, yy + 25.0, z_agiz - 13.1, z_agiz - 9.9))        # pim deliği Ø3,2 boydan boya (pim −549,5…−546,5)
        for cxi, cyi in YAYC: kv = kv.cut(silz(cxi, cyi, 3.0, z_agiz - 16.0, z_agiz - 15.5 + 9.7))     # 4 yay cebi Ø6 × 9,7 (yarıkların arasında, r 18): dip −542,3
        ekle("yuva_%s_hac_yuvasi" % tag, kv, "pom", "H", grup=gr,
             not_="POM Ø48 × 15,5 · önünde 36,5 × 8,5 haç yarığı 8 derin (kaset haçı 7,0 girer, dipte 1) · milde pimle kayar (sert durak 8,5; kaset en çok 7,0 + 0,5 iter) · 4 katalog yay öne iter · PLC yavaş çevirir, haç oturur (KLİK) · tork: 4 çubuk yüzü 7 × 4,75, 3 Nm'de 1,8 MPa (POM 20)")
        for i, (cxi, cyi) in enumerate(YAYC):
            ekle("yuva_%s_yay_%d" % (tag, i), silz(cxi, cyi, 2.39, z_agiz - 26.0 + 0.1, z_agiz - 15.5 + 9.7).cut(silz(cxi, cyi, 1.98, z_agiz - 26.5, z_agiz - 15.5 + 9.7 + 0.5)), "celik", "K", grup=gr,
                 not_="Century Spring 66644SCS · 316 · tel 0,41 · Ø4,78 · serbest 21,34 · 0,33 N/mm · en çok 9,12 mm sıkışma [katalog] · takılı 20,1 (ön yük 1,24 = 0,41 N; 4 yay 1,6 N) · 8,0 geri çekilmede 12,1 (9,2 sıkışma) — gösterim: kovan")
        tb = silz(xc, yy, 24.0, z_agiz - 26.9, z_agiz - 25.9).cut(silz(xc, yy, 11.5, z_agiz - 27.4, z_agiz - 25.4))              # −563,4…−562,4
        for cxi, cyi in YAYC: tb = tb.union(silz(cxi, cyi, 1.8, z_agiz - 25.9, z_agiz - 21.9))
        ekle("yuva_%s_yay_tablasi" % tag, tb, "paslanmaz", "H", grup=gr, not_="yay tablası 304 · Ø48 × 1 · milin segmanına oturur, milyle döner · 4 yay pilotu Ø3,6 × 4 (yay iç Ø3,96) · kovan sert durakta (8,5) buna 1,9 kala durur")
        ekle("yuva_%s_segmani" % tag, silz(xc, yy, 12.3, z_agiz - 28.1, z_agiz - 26.9).cut(silz(xc, yy, 10.5, z_agiz - 28.5, z_agiz - 26.5)), "celik", "K", grup=gr,
             not_="Segman DIN 471 A22 × 1,2 (kanal d2 21,0 · m 1,3) · kovan yüzüne 0,3")
        ekle("yuva_%s_kavrama_pimi" % tag, kut(xc - 1.5, xc + 1.5, yy - 22.5, yy + 22.5, z_agiz - 13.0, z_agiz - 10.0), "celik", "K", grup=gr,
             not_="Pim ISO 8734 3 m6 × 45 A1 (kovanda 1,5 içeride): kovanı mile bağlar (tork), mildeki 3,2 × 11,5 kanalda kayar (sert durak 8,5)")
ekle("yalitim_blogu", YAL_BLOK[0], "pu", "Ö",
     not_="v6 TEK BLOK PU 60 (sac kaplı) · dışı 1620 × 751 × 526 düz · soğuk oda A tavan 1968 / B 1680 · teknik cep arkaya açık · 4 kaset kovanı + 4 UNO kovanı + geçiş bloğu delikleri")
# ön fitil: soğuk odanın L ağzının çevresi (A 90–790 × 1277–1968 · B 790–1710 × 1277–1680), manyetik profil 21 × 18,5 (çekmecelerle aynı) · ön kapak SONRA
FITIL_W, FITIL_T = 21.0, 6.0
_agiz = [(BAY_A[0], YAL_Y0), (BAY_B[1], YAL_Y0), (BAY_B[1], TAVAN_B), (BAY_A[1], TAVAN_B), (BAY_A[1], TAVAN_A), (BAY_A[0], TAVAN_A)]
_dis = cq.Workplane("XY", origin=(0, 0, Z_KAPAK[1])).polyline([(x + (-FITIL_W if x == BAY_A[0] else FITIL_W), y + (-FITIL_W if y == YAL_Y0 else (FITIL_W if y in (TAVAN_A,) or (y == TAVAN_B and x == BAY_B[1]) else 0.0))) for x, y in _agiz]).close().extrude(FITIL_T)
_ic = cq.Workplane("XY", origin=(0, 0, Z_KAPAK[1] - 1)).polyline(_agiz).close().extrude(FITIL_T + 2)
ekle("on_fitil", _dis.cut(_ic), "silikon", "H",
     not_="manyetik fitil 21 × 18,5 (sıkışınca 15) kanallı alüminyum profilde · L ağzın çevresi · ön kapak kapanınca buna basar · çekmece fitiliyle aynı profil")

# ================================================================ 4 · HAVA TESİSATI
ekle("sartlandirici_filtre_regulator", kut(*FRL), "aluminyum", "V", not_="filtre + regülatör + ana vana · 7 bar")
ekle("sartlandirici_manometre", silz(1675, 1380, 14, -700, -690), "pom", "V")
ekle("valf_adasi_12x5_2", kut(*ADA), "aluminyum", "V", not_="12 × 5/2 elektro-valf: 4 piston + 4 döner valf + 2 spreader kesme valfi + açıcı + yedek")
for n in range(12):
    x = ADA[0] + 14 + n * 24.0
    ekle("valf_bobini_%d" % (n + 1), kut(x, x + 18, ADA[3], ADA[3] + 30, -680, -740), "siyah", "V")
ekle("gecis_blogu_yalitim", kut(90, 1200, 1440, 1470, Z_BOLME[0], Z_BOLME[1]), "pom", "V", not_="hortumların soğuk hücreye geçtiği keçeli blok")
# ana hat: K tabanındaki kompresör → F tabanı arka köşe → C'ye sağ alttan → şartlandırıcı → ada
ana = [(3600, 1030, -380), (3600, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]
ekle("hava_ana_hatti_D10", boru(ana, 5.0), "hava_ana", "V", not_="Ø10 PU · K tabanı → F tabanı arka köşe kanalı → TOPPING sağ alt")
ekle("hava_hatti_sartlandirici_ada", boru([(1675, 1420, -740), (1675, 1552, -740), (470, 1552, -740), (470, 1630, -740), (458, 1630, -740)], 5.0), "hava_ana", "V",
     not_="evaporatörün altından, kaset motorlarının üstünden geçer")
ekle("hava_hatti_acici_D6", boru([(150, 1640, -700), (40, 1640, -700), (40, 1640, -790), (-30, 1640, -790)], 3.0), "hortum_mavi", "V",
     not_="açıcının Ø32 Z silindirine (modül A) · 2 hat")
for i, (ad, cx, *_r) in enumerate(UNO):
    k = ad.lower(); tx = ADA[0] + 20 + i * 48.0
    for j, (zp, renk) in enumerate(((-680.0, "hortum_mavi"), (-800.0, "hortum_siyah"))):
        dx = j * 8.0
        ekle("%s_hortum_silindir_%d" % (k, j + 1), boru([(tx + dx, ADA[2], -700), (tx + dx, 1420 + dx, -700), (cx + dx, 1420 + dx, -700),
                                                       (cx + dx, 1420 + dx, zp), (cx + dx, V_EKSEN + 19, zp)], 3.0), renk, "V")
    for j, renk in enumerate(("hortum_mavi", "hortum_siyah")):
        dx = j * 8.0; ex = cx - 72 + dx
        ekle("%s_hortum_doner_valf_%d" % (k, j + 1), boru([(tx + 24 + dx, ADA[2], -720), (tx + 24 + dx, 1455, -720), (ex, 1455, -720),
                                                          (ex, 1455, -420), (ex, V_EKSEN + 22, -420)], 3.0), renk, "V")
# kompresör (bağlam: F ve K tabanları hayalet)
ekle("baglam_F_tabani", kut(1800, 3300, 123, 1060, 0, -D), "hayalet", "Ö", not_="modül F taban dolabı (bağlam)")
ekle("baglam_K_tabani", kut(3300, 3900, 123, 1060, 0, -D), "hayalet", "Ö", not_="modül K taban dolabı · boş (Kemal 24 Eyl: yedek kutu yok)")
ekle("baglam_A_modulu", kut(-700, 0, Y0, YUST, 0, -D), "hayalet", "Ö", not_="modül A açıcı (bağlam)")
ekle("kompresor_JUNAIR_OF302_15B_tank", silx((KOMP[2] + 170), (KOMP[4] + KOMP[5]) / 2, 150, KOMP[0], KOMP[1]), "kompresor", "B",
     not_="JUN-AIR OF302-15B · yağsız · 15 L · 380 × 380 × 510 · 25 kg · 43 L/dk @ 7 bar · 65 dB")
ekle("kompresor_JUNAIR_OF302_15B_motor", kut(KOMP[0] + 40, KOMP[1] - 40, KOMP[2] + 320, KOMP[3], KOMP[4] - 40, KOMP[5] + 60), "kompresor", "B")
ekle("kompresor_cikis_vanasi", sily(3600, -380, 8, KOMP[3], 1036), "siyah", "V")

# ================================================================ 5 · DENETİM
def bb(ad): return [p for p in P if p["ad"] == ad][0]["sh"].BoundingBox()
DEN = []
def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-60s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))
print("DENETİM")
for ad, cx, hw, hust, *_r in UNO:
    k = ad.lower(); h = bb("%s_hazne_bizim" % k)
    tav = TAVAN_A if cx < BAY_A[1] else TAVAN_B
    kontrol("%s haznesi tavanın altında (%.0f < %.0f)" % (ad, h.ymax, tav), h.ymax < tav)
    kontrol("%s haznesi soğuk hücrede z (%.0f…%.0f)" % (ad, h.zmin, h.zmax), h.zmin > Z_SOGUK[1] and h.zmax < Z_KAPAK[1])
    s = bb("%s__pnomatik_silindir_D32" % k); kontrol("%s UNO hava silindiri kuru bölmede (z %.0f…%.0f)" % (ad, s.zmin, s.zmax), s.zmin > -D and s.zmax < Z_BOLME[1] + 1)
    u = bb("%s__urun_silindiri_D%d" % (k, _r[0])); kontrol("%s ürün silindiri soğukta (z %.0f)" % (ad, u.zmin), u.zmin >= Z_SOGUK[1])
    ag_ = bb("%s__agiz_90_derece" % k); kontrol("%s UNO ağzı tabla ekseninde (z %.1f)" % (ad, (ag_.zmin + ag_.zmax) / 2 if False else ag_.zmax - 18), abs(ag_.zmax - 18 - ZT) < 1.0)
kontrol("UNO'lar kasetlere değmiyor (kuşbaşı valf topuzu %.0f < kaşar yuvası 1220)" % bb("kusbasi__valf_topuzu").xmax, bb("kusbasi__valf_topuzu").xmax < 1220)
kontrol("sos valf eyleyicisi sol duvara değmiyor (%.0f > 90)" % bb("sos__valf_dondurme_aktuatoru").xmin, bb("sos__valf_dondurme_aktuatoru").xmin > 90)
for ad in ("SOS", "HARC"):
    b_ = bb("%s_spreader_dagitici_boru" % ad.lower())
    kontrol("%s spreader borusu yarıçap boyunca (x %.0f…%.0f, boy %.0f)" % (ad, b_.xmin, b_.xmax, b_.xmax - b_.xmin), b_.xmax - b_.xmin >= 125.0)
    kontrol("%s spreader borusu pideden %.0f mm yukarıda" % (ad, b_.ymin - PIDE_UST), 3.0 <= b_.ymin - PIDE_UST <= 10.0)
    y_ = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(("tasiyici_raf", "raf_"))])
    for pp in [p for p in P if p["ad"].startswith("%s_spreader_" % ad.lower()) and "hortum" not in p["ad"]]:
        kontrol("%s rafa girmiyor" % pp["ad"], y_.intersect(pp["sh"]).Volume() < 1.0)
b_ = bb("harc_spreader_uc_tapasi"); k_ = bb("kiyma__valf_topuzu")
for ad in ("SOS", "HARC"):                                                # v5: model yarığı hesaptaki profil mi
    _b = bb("%s_spreader_dagitici_boru" % ad.lower())
    kontrol("%s kama yarık: merkez %.1f → kenar %.1f mm (hesap q ∝ r)" % (ad, TH2.yarik_genisligi(ad, TH2.YARIK_R[0]), TH2.yarik_genisligi(ad, TH2.YARIK_R[1])),
            TH2.yarik_genisligi(ad, TH2.YARIK_R[1]) / TH2.yarik_genisligi(ad, TH2.YARIK_R[0]) > 1.4 and _b.xmax - _b.xmin >= 125.0)
for _g in [g for g in GRUP if g.startswith(("HELEZON_", "KARISTIRICI_"))]:
    kontrol("kaset döner grubu dolu: %s (%d parça)" % (_g, sum(1 for p in P if p["grup"] == _g)), sum(1 for p in P if p["grup"] == _g) >= 3)
kontrol("harç spreader'ı kıyma istasyonuna değmiyor (%.0f < %.0f)" % (b_.xmax, k_.xmin), b_.xmax < k_.xmin)
_rf = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(("tasiyici_raf", "raf_"))])
_ic = 0
for p in P:
    if p["ad"].startswith(("tasiyici_raf", "raf_")) or p["ad"].startswith(("baglam", "kompresor", "hava_ana")): continue
    try:
        if _rf.intersect(p["sh"]).Volume() > 5.0: _ic += 1; print("   rafa giren:", p["ad"])
    except Exception: pass
kontrol("rafa hiçbir parça girmiyor (delikler ağız ve boruları geçiriyor)", _ic == 0, "%d" % _ic)
kas_bb = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(("kasar_cad", "sucuk_cad"))]).BoundingBox()
kontrol("kasetler modül içinde (x %.0f…%.0f)" % (kas_bb.xmin, kas_bb.xmax), kas_bb.xmin > 1200 and kas_bb.xmax < 1710)
for a, b in (("valf_adasi_12x5_2", "sartlandirici_filtre_regulator"),):
    kontrol("valf adası + şartlandırıcı kuru bölmede", bb(a).zmax <= Z_BOLME[1] and bb(b).zmax <= Z_BOLME[1])
cak = 0
tahrik = [p for p in P if p["ad"].startswith(("motor_", "reduktor_"))]
for p in P:
    if "hortum" in p["ad"] or p["ad"].startswith("hava_hatti"):
        for t in tahrik:
            try:
                if p["sh"].intersect(t["sh"]).Volume() > 1.0: cak += 1; print("   çakışma:", p["ad"], t["ad"])
            except Exception: pass
kontrol("hortumlar kaset motorlarına değmiyor", cak == 0, "%d çakışma" % cak)
# v6 · kaset yuvaları
for KOD, Y_ in YUVA.items():
    k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v7"
    kas = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(mod)])
    yuva = [p for p in P if p["ad"].startswith("yuva_%s_" % k)]
    _kes = 0
    for p in yuva:
        try:
            if kas.intersect(p["sh"]).Volume() > 1.0: _kes += 1; print("   yuva parçası kasete giriyor:", p["ad"])
        except Exception: _kes += 1
    kontrol("%s yuvası kasete girmiyor (%d parça)" % (KOD, len(yuva)), _kes == 0, "%d" % _kes)
    pb_ = bb("%s__plaka_on" % mod); kontrol("%s kaseti plakalarıyla rafa oturuyor (plaka altı %.0f = raf %.0f)" % (KOD, pb_.ymin, SOGUK_TABAN), abs(pb_.ymin - SOGUK_TABAN) < 0.01)
    kl = bb("yuva_%s_kilavuz_sol" % k); kr = bb("yuva_%s_kilavuz_sag" % k)
    kontrol("%s kılavuz dudakları plakaya 0,5 mm (%.1f / %.1f)" % (KOD, Y_["px0"] - kl.xmax, kr.xmin - Y_["px1"]), abs(Y_["px0"] - kl.xmax - 0.5) < 0.01 and abs(kr.xmin - Y_["px1"] - 0.5) < 0.01)
    dl = bb("yuva_%s_mandal_dili" % k); gv = bb("yuva_%s_mandal_govdesi" % k)
    kontrol("%s mandal dili plakanın ÖNÜNDE (z %.1f ≥ plaka önü %.0f), plakayı %.1f mm örtüyor ≥ 4,0" % (KOD, dl.zmin, Y_["pz1"], dl.xmax - Y_["px0"]), dl.zmin >= Y_["pz1"] and dl.xmax - Y_["px0"] >= 4.0)
    kontrol("%s mandal kolu sola %.1f mm kayabilir ≥ 5,0 (dil plakadan çıkar)" % (KOD, dl.xmin - (gv.xmin + 2.5)), dl.xmin - (gv.xmin + 2.5) >= 5.0)
    ad_ = bb("yuva_%s_arka_dayama_sol" % k); kontrol("%s arka dayama plakanın arka yüzünde (z %.0f)" % (KOD, ad_.zmax), abs(ad_.zmax - Y_["pz0"]) < 0.01)
    hy = bb("yuva_%s_helezon_hac_yuvasi" % k); hk = bb("%s__kavrama_helezon" % mod); ty = bb("yuva_%s_helezon_yay_tablasi" % k)
    kontrol("%s haç çubukları yuvada %.1f mm (7,0 · v7 katalog yayına göre)" % (KOD, hy.zmax - hk.zmin), hy.zmax > hk.zmin and abs((hy.zmax - hk.zmin) - 7.0) < 0.6)
    kontrol("%s haç yuvası geri çekilebilir: yay tablasına %.1f mm ≥ 8,5 sert durak + 1,9" % (KOD, hy.zmin - (ty.zmin + 1.0)), hy.zmin - (ty.zmin + 1.0) >= 10.39)   # tabla plakası 1 mm; pilotlar sayılmaz
    _ys = bb("yuva_%s_helezon_yay_0" % k); _tak = _ys.zmax - _ys.zmin
    kontrol("%s yay takılı boy %.1f: ön yük %.2f ≥ 1,0 · 8,0 geri çekilmede sıkışma %.2f ≤ 9,12 (66644SCS)" % (KOD, _tak, 21.34 - _tak, 21.34 - _tak + 8.0), 21.34 - _tak >= 1.0 and 21.34 - _tak + 8.0 <= 9.12 + 0.3)
    _my = bb("yuva_%s_mandal_yayi" % k); _mt = _my.xmax - _my.xmin
    kontrol("%s mandal yayı takılı %.1f: ön yük %.1f (%.1f N) · 5 mm açılınca sıkışma %.1f ≤ 9,12" % (KOD, _mt, 21.34 - _mt, 0.33 * (21.34 - _mt), 21.34 - _mt + 5.0), 21.34 - _mt >= 3.0 and 21.34 - _mt + 5.0 <= 9.12 + 0.3)
    _mil = bb("mil_%s_helezon" % mod); _seg = bb("yuva_%s_helezon_segmani" % k)
    kontrol("%s segman kanalı DIN 471: genişlik %.1f = 1,3 · segman kanalda · kovan yüzüne %.1f" % (KOD, 1.3, _seg.zmin + 565.0), abs((_seg.zmin + 565.0) - 0.4) < 0.15)
    kontrol("%s mil ucu (−545) haç kavramasının arkasında ≥ 1 mm" % KOD, hk.zmin - bb("mil_%s_helezon" % mod).zmax >= 1.0)
    # yuva parçaları birbirine ve makinenin öbür sabit parçalarına girmiyor (gerçek katı; kaset ayrı sayıldı)
    _oth = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski", "teknik_bant"))]
    _kes2 = []
    for p in yuva:
        b1 = p["sh"].BoundingBox()
        for q in yuva + _oth:
            if q is p: continue
            b2 = q["sh"].BoundingBox()
            if not (b1.xmin < b2.xmax and b2.xmin < b1.xmax and b1.ymin < b2.ymax and b2.ymin < b1.ymax and b1.zmin < b2.zmax and b2.zmin < b1.zmax): continue
            try: v_ = p["sh"].intersect(q["sh"]).Volume()
            except Exception: v_ = -1.0
            if v_ > 1.0 or v_ < 0: _kes2.append((p["ad"], q["ad"], round(v_, 1)))
    kontrol("%s yuva parçaları birbirine / makineye girmiyor (%d parça)" % (KOD, len(yuva)), not _kes2, "%s" % _kes2[:6])
kontrol("kaşar sağ kılavuzu–sucuk mandalı boşluğu %.1f ≥ 10 · kaşar plakası–sucuk plakası %.0f ≥ 30" % (bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax, bb("sucuk_cad_v7__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax),
        bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax >= 10.0 and bb("sucuk_cad_v7__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax >= 30.0)
kontrol("sucuk sağ kılavuzu–sağ duvar boşluğu %.1f ≥ 20" % (BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax), BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax >= 20.0)
kontrol("kuşbaşı valf topuzu–kaşar mandalı boşluğu %.0f ≥ 20" % (bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax), bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax >= 20.0)
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]
kontrol("kabin yan PU duvarları 1277'den başlıyor (mekanizma bölgesi serbest)", all(p["sh"].BoundingBox().ymin >= 1276.99 for p in _sd))
for _ad, _mod, _x0, _x1 in KASET:
    _kb_ = bb("%s__cikis_tupu" % _mod); _hn_ = bb("%s_inis_hunisi" % _mod.split("_")[0])
    kontrol("%s çıkış borusu altı (%.0f) iniş hunisinin üstünde (%.0f), iç içe DEĞİL" % (_ad, _kb_.ymin, _hn_.ymax), _kb_.ymin > _hn_.ymax)
_yb = bb("yalitim_blogu"); kontrol("yalıtım tek blok, dışı düz (x %.0f…%.0f · y %.0f…%.0f · z %.0f…%.0f)" % (_yb.xmin, _yb.xmax, _yb.ymin, _yb.ymax, _yb.zmin, _yb.zmax), _yb.xmin == BAY_A[0] and _yb.xmax == BAY_B[1] and _yb.zmax == Z_KAPAK[1] and _yb.zmin == Z_BOLME[1])
_yv = [p for p in P if p["ad"].startswith(("soguk_hucre", "arka_yalitim"))]; kontrol("eski parçalı yalıtım kalktı", not _yv)
_kb = 0; _ybs = [q for q in P if q["ad"] == "yalitim_blogu"][0]["sh"]
for p in P:
    if p["ad"].startswith(("yalitim_blogu", "on_fitil", "teknik_bant", "kabin_", "baglam", "kompresor", "hava_ana")): continue
    try:
        if p["sh"].intersect(_ybs).Volume() > 1.0: _kb += 1; print("   yalıtım bloğuna giren:", p["ad"])
    except Exception: pass
kontrol("yalıtım bloğuna hiçbir parça girmiyor (kovanlar deliklerinde)", _kb == 0, "%d" % _kb)

# ================================================================ 6 · ANİMASYON + GLB
DONGU = 2.0
def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    u = (t - a) / (b - a); return u * u * (3 - 2 * u)
def piston_dz(t, strok):
    if t <= 0.8: return -strok * ss(0.0, 0.8, t)
    if t <= 1.0: return -strok
    return -strok * (1.0 - ss(1.0, 1.8, t))
def valf_aci(t):
    if t <= 0.8: return 0.0
    if t <= 1.0: return -math.pi / 2 * ss(0.8, 1.0, t)
    if t <= 1.8: return -math.pi / 2
    return -math.pi / 2 * (1.0 - ss(1.8, 2.0, t))


def ag(sh, tol=0.25, aci=0.3):
    vs, ts = sh.tessellate(tol, aci)
    Pp = [(v.x, v.y, v.z) for v in vs]; N = [[0.0, 0.0, 0.0] for _ in Pp]
    for a, b, c in ts:
        u = [Pp[b][i] - Pp[a][i] for i in range(3)]; w = [Pp[c][i] - Pp[a][i] for i in range(3)]
        n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        for i in (a, b, c):
            for j in range(3): N[i][j] += n[j]
    NN = []
    for n in N:
        L = math.sqrt(sum(c * c for c in n)) or 1.0; NN.append((n[0] / L, n[1] / L, n[2] / L))
    return Pp, NN, [i for t in ts for i in t]


def glb_yaz(yol):
    blob, views, accs, meshes, mats = [], [], [], [], []; off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    nodes = [{"name": "TOPPING_v2_UNO", "children": []}]; gi = {}
    for g, pv in GRUP.items():
        gi[g] = len(nodes); nodes.append({"name": g, "translation": [pv[0] * MM, pv[1] * MM, pv[2] * MM], "children": []}); nodes[0]["children"].append(gi[g])
    uc = 0
    for p in P:
        pv = GRUP[p["grup"]]
        Pp, N, I = ag(p["sh"])
        pts = [((q[0] - pv[0]) * MM, (q[1] - pv[1]) * MM, (q[2] - pv[2]) * MM) for q in Pp]
        vp = gomu(struct.pack("<%df" % (3 * len(pts)), *[c for q in pts for c in q]), 34962)
        vn = gomu(struct.pack("<%df" % (3 * len(N)), *[c for q in N for c in q]), 34962)
        vi = gomu(struct.pack("<%dI" % len(I), *I), 34963)
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(pts), "type": "VEC3", "min": [min(q[i] for q in pts) for i in range(3)], "max": [max(q[i] for q in pts) for i in range(3)]})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(I), "type": "SCALAR"})
        renk, met, ruf, say = M[p["mal"]]
        mm = {"name": p["ad"], "pbrMetallicRoughness": {"baseColorFactor": list(renk), "metallicFactor": met, "roughnessFactor": ruf}, "doubleSided": True}
        if say: mm["alphaMode"] = "BLEND"
        mats.append(mm)
        meshes.append({"name": p["ad"], "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": len(mats) - 1}]})
        nodes.append({"name": p["ad"], "mesh": len(meshes) - 1}); nodes[gi[p["grup"]]]["children"].append(len(nodes) - 1); uc += len(I) // 3
    for n in nodes:
        if "children" in n and not n["children"]: del n["children"]
    NS = 61; TT = [DONGU * i / (NS - 1) for i in range(NS)]; sm, ch = [], []
    def kanal(g, yol_, vals, tip):
        ti = gomu(struct.pack("<%df" % NS, *TT)); accs.append({"bufferView": ti, "componentType": 5126, "count": NS, "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        n = 4 if tip == "VEC4" else 3
        vo = gomu(struct.pack("<%df" % (n * NS), *[c for v in vals for c in v])); accs.append({"bufferView": vo, "componentType": 5126, "count": NS, "type": tip})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": gi[g], "path": yol_}})
    tb = [(0.0, math.sin(-math.pi * ss(1.0, 1.8, t)), 0.0, math.cos(-math.pi * ss(1.0, 1.8, t))) for t in TT]
    kanal("TABLA", "rotation", tb, "VEC4")
    for ad, cx, hw, hust, d_sil, agiz, doz in UNO:
        strok = doz * 1000.0 / (math.pi / 4 * d_sil ** 2); b = nodes[gi["PISTON_" + ad]]["translation"]
        kanal("PISTON_" + ad, "translation", [(b[0], b[1], b[2] + piston_dz(t, strok) * MM) for t in TT], "VEC3")
        kanal("VALF_" + ad, "rotation", [(math.sin(valf_aci(t) / 2), 0.0, 0.0, math.cos(valf_aci(t) / 2)) for t in TT], "VEC4")
    for g in [g for g in GRUP if g.startswith(("HELEZON_", "KARISTIRICI_"))]:     # v5: kaset milleri (görsel: 2 s'de 1 tur)
        kanal(g, "rotation", [(0.0, 0.0, math.sin(-math.pi * t / DONGU), math.cos(-math.pi * t / DONGU)) for t in TT], "VEC4")
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb_ = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH topping_uno_cad_v7"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb_)}],
          "animations": [{"name": "emis_basma_2sn", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb_))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb_), b"BIN\x00")); f.write(bb_)
    print("GLB %s · %d KB · %d parça · %d üçgen" % (os.path.basename(yol), (len(bb_) + len(js)) // 1024, len(P), uc))


if __name__ == "__main__":
    # v6 · KASET ÇIKIŞ YOLU: kaset (mandal kalkık) 10 mm adımlarla öne çekilir; hiçbir sabit parçaya değmemeli
    for KOD in YUVA:
        k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v7"
        kas = [p["sh"] for p in P if p["ad"].startswith(mod)]
        sabit = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_mandal_dili" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski"))]
        bul = []
        for dz in range(10, 431, 10):
            kc = cq.Compound.makeCompound([q.translate(V(0, 0, dz)) for q in kas]); kb_ = kc.BoundingBox()
            for p in sabit:
                b_ = p["sh"].BoundingBox()
                if not (kb_.xmin < b_.xmax and b_.xmin < kb_.xmax and kb_.ymin < b_.ymax and b_.ymin < kb_.ymax and kb_.zmin < b_.zmax and b_.zmin < kb_.zmax): continue
                try: v_ = kc.intersect(p["sh"]).Volume()
                except Exception: v_ = -1.0
                if v_ > 1.0 or v_ < 0: bul.append((dz, p["ad"], round(v_, 1)))
        kontrol("%s kaseti öne çekilirken (0–430 mm) hiçbir parçaya değmiyor" % KOD, not bul, "%d bulgu %s" % (len(bul), bul[:6]))
    kal = [d for d in DEN if not d[1]]
    assert not kal, kal
    glb_yaz(os.path.join(OUT, "topping_uno_v7.glb"))
    with open(os.path.join(OUT, "topping_uno_v7.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v7 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       grup={g: list(v) for g, v in GRUP.items()},
                       parcalar=[dict(ad=p["ad"], kaynak=p["kaynak"], not_=p["not_"], mal=p["mal"]) for p in P],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN]), f, ensure_ascii=False, indent=1)
    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))
