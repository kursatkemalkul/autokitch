# -*- coding: utf-8 -*-
"""TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v15 · 28 Eyl 2026 akşam (v14 + KAPAK İÇ SACI TEK PARÇA · sucuk_cad_v8 · Codex STEP kırıntıları atılır · yap_topping_uno_cad_v15.py)
v14: topping_uno_cad_v14 · 28 Eyl 2026 gece (v13 + ÖN DÜZLEM +79 · SOĞUK ODA KAPAKLI TEMİZ KUTU — SPEC_on_duzlem_v63 §2.3)
v14: soğuk zarf ön yüzü −104 → +23 · yan duvar sandviç 1,5 + 57,5 + 1,0 (Z profille TC yan sacına) · raf L 40×40×3 köşebentte · 430 çerçeve +23…+24 ·
    K1 / K2 soğuk kapak 40 sandviç +39…+79 + manyetik fitil +24…+39 + flipper · eski fitil silindi · havada parça bağlandı · hortumlar ayrıldı ·
    açıcı hattı 2 × Ø6 · kaset çekme 0–630 · den_assert(). Önceki: topping_uno_cad_v13.py (yap_topping_uno_cad_v14.py)
v14 DÜZELTME (28 Eyl sabah · on_duzlem_v63/denetim_C.md): SOĞUK TABAN SIZDIRMAZ — kasetle çıkan YARIK DİLİ + arka yaka contası + UNO / hortum geçiş
    contaları; alt PU yalnız üst 6 mm yarık (iniş borusu + huni altı dolu) · FLIPPER KATLANIR (eksen x 1493 · z +20, burulma yayı, raf üstünde kam oluklu
    kılavuz; K2 kapalıyken K1 açılır) · K1 / K2 çok kollu gizli menteşe, sanal pivot ön dış köşe, TABAN TC yan sacına · motor kablo rakoru ·
    itici kirişi için sağ duvar alt profili · kapak açılma taramaları + soğuk taban kaçak denetimi (den_assert)
v13 (27 Eyl gece): (v12 + YAN YALITIM = ÜST YALITIM — Kemal: "ön yüzeyleri aynı planda, kalınlıkları üstle aynı")
v13: yan PU duvarlar 90 → 60 kalın (x 30–90 · 1710–1770), z 0…−830 → −104…−630 (üst yalıtımla aynı ön ve arka düzlem); soğuk oda iç ölçüsü aynı.
    Önceki: topping_uno_cad_v12.py (yap_topping_uno_cad_v13.py)
v12 (27 Eyl gece): (v11 + SOĞUK ODANIN ALTINA YALITIM — Kemal: "altına da az da olsa yalıtım yap")
v12: rafın altına, ön ve arka bükümlerin arasına alt sac 1 + PU 39 (y 1277–1317) · raf / disk / hat kotları aynı · rafın altından geçen parçalara
    boşluklu delik (kaset borularına öne açık yarık) · soğuk oda tabanı artık yalıtımlı. Önceki: topping_uno_cad_v11.py (yap_topping_uno_cad_v12.py)
v11 (27 Eyl):
v11: yalıtım A tavanı + L PU 30 (soğuk ↔ teknik) + arka bölme + sağ yan 1277–1720; teknik cep x 820–1800 · y 1720–2028 saç kabuklu, havalandırmalı, arkası açık. Önceki: topping_uno_cad_v10.py
v10 (27 Eyl):
v10: soğuk hacim tek parça (B tavanı 1690 = ayırma saçı) · teknik cep x 790–1710 · y 1690–1968, soğuk hacimden 1,5 mm paslanmaz L saçla ayrılır · üst PU 1968–2028. Önceki: topping_uno_cad_v9.py
v9 (27 Eyl): ön fitil TAM
v9: ön fitil kesiksiz (aktarma iticisi düz itiyor, ön düzlemi kesmiyor). Önceki: topping_uno_cad_v8.py
v8: ön fitilin alt şeridi yerel x 1325–1455 arasında kesik (aktarma iticisi çapraz hattı ön düzlemi keser; ön kapak yok — Kemal). Önceki: topping_uno_cad_v7.py
v7: (katalog yay/pim · haç 7,0 · mandal 4,5 · kabin duvarı 1277'den)
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
silindiri + Ø32 hava silindiri; bizim soğuk hazne) · KAŞAR · KÜP SUCUK = bizim kasetler (kasar_cad_v14 / sucuk_cad_v8 +
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
    "sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32, False), "conta": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.7, False),   # v14 · SPEC ön yüz malzemeleri
    "plastik": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.6, False),
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
BAY_A = (90.0, 790.0); TAVAN_A = 1968.0; BAY_B = (790.0, 1710.0); TAVAN_B = 1690.0   # v10: B tavanı = teknik ayırma saçı (60 mm PU dilimi kalktı; kaset üstü 1680 + 10)
SAC_T = 1.5; PU_L = 30.0                                                            # v11: soğuk ↔ teknik PU levha 30
Y_TEK = TAVAN_B + PU_L; X_TEK = BAY_A[1] + PU_L                                    # v11: teknik cep tabanı 1720 · sol duvarı 820
TEK_Y0 = Y_TEK + SAC_T + 10.0                                                      # v11: teknik bant zarflarının altı 1731,5
Z_ON = 79.0                                                                        # v14 · ÖN DÜZLEM (fırın ön yüzü) · montaj sözleşmesi Z_ON = FT.ZS = 79
Z_ZARF = 23.0                                                                      # v14 · soğuk zarfın ön yüzü (v13 −104): önünde 430 çerçeve +23…+24 · fitil +24…+39 · kapak +39…+79
Z_CER = (Z_ZARF, Z_ZARF + 1.0); Z_SKAPAK = (Z_ON - 40.0, Z_ON)                  # v14 · 430 ferritik çerçeve sacı 1,0 · soğuk kapak 40 = dış 1,5 + PU 37,5 + iç 1,0
Z_KAPAK = (-84.0, Z_ZARF); Z_SOGUK = (Z_ZARF, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)   # v14: Z_KAPAK[1] = soğuk zarf ön yüzü (v13 −104)
DX_DUNYA, DY_DUNYA = 700.0, -168.0                                                 # v14 · montaj: dünya x = x + 700 · dünya y = y − 168 (TU bir kez kaydırılır)
def xu(x_dunya): return x_dunya - DX_DUNYA
def yu(y_dunya): return y_dunya - DY_DUNYA
ZT = -170.0; PIDE_UST = 1176.0
BICAK = {"SOS": dict(boy=125.0, yarik=3.0), "HARC": dict(boy=125.0, yarik=6.0)}   # [V] sos kenarı 15 mm boş · harç parçacık ~5 mm
BICAK_ALT = PIDE_UST + 6.0            # bıçak ağzı pideden 6 mm yukarıda (katman ~2 mm) [V]
BICAK_UST = 1262.0                    # UNO 90° ağzının dik bacağı 1263,5'te bitiyor; bıçak buradan başlar
V_EKSEN = SOGUK_TABAN + 38.5; V_UST = SOGUK_TABAN + 72.6; VZ = -387.0
UNO = [  # ad, x merkezi, hazne genişliği, hazne üstü, silindir çapı, ağız tipi, doz (ml)
    ("SOS", 210.0, 220.0, 1737.0, 52.0, "yassi", 76.0), ("HARC", 560.0, 440.0, 1832.0, 52.0, "yassi", 105.0),
    ("KIYMA", 895.0, 190.0, 1667.0, 70.0, "yuvarlak", 152.0), ("KUSBASI", 1105.0, 190.0, 1667.0, 70.0, "yuvarlak", 170.0)]
KASET = [("KAŞAR KABI", "kasar_cad_v14", 1220.0, 1502.0), ("KÜP SUCUK", "sucuk_cad_v8", 1539.0, 1681.0)]   # v6: sucuk +13 (kaşar–sucuk plakaları 30, sağ duvar 25,5)
CODEX_3B = {"kasar_cad_v14": {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                              "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"},
            "sucuk_cad_v8": {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"}}
ADA = (150.0, 458.0, 1600.0, 1660.0, -660.0, -760.0)     # valf adası 12 × 5/2 (kuru bölme)
FRL = (1650.0, 1700.0, 1250.0, 1420.0, -700.0, -780.0)    # şartlandırıcı
KOMP = (3410.0, 3790.0, 520.0, 1030.0, -40.0, -420.0)     # K tabanı (modül C yerelinde x 3300–3900)

# ================================================================ 1 · KABİN
ekle("kabin_taban_saci", kut(0, W, Y0, Y0 + 1.5, 0, -D), "fircali", "V")
ekle("kabin_arka_saci", kut(0, W, Y0, YUST, -D + 1.5, -D), "kabuk", "V")
ekle("kabin_ust_saci", kut(0, W, YUST - 1.5, YUST, 0, -D), "kabuk", "V")
YAN_T = YUST - 1.5 - TAVAN_A                                                              # v13: üst yalıtımın kalınlığı (60,5 ≈ 60) → yanlar da bu (v14: sandviç 60)
DUVAR = (1.0, 57.5, 1.5)                                                                  # v14 · SPEC soğuk gövde duvarı: iç 304 1,0 + PU 57,5 (40 kg/m³) + dış 304 1,5 = 60
for _yn, _xi0, _sg, _y1 in (("sol", BAY_A[0], -1.0, YUST - 1.5), ("sag", BAY_B[1], 1.0, Y_TEK)):
    _a = _xi0; _b = _a + _sg * DUVAR[0]; _c = _b + _sg * DUVAR[1]; _d = _c + _sg * DUVAR[2]
    ekle("soguk_duvar_%s_ic_sac" % _yn, kut(min(_a, _b), max(_a, _b), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "V",
         not_="v14 · AISI 304 1,0 · sandviç iç kabuğu (soğuk yüz) · raf köşebendi (L 40×40×3) buna M6 perçin somunla")
    ekle("kabin_%s_duvar_PU" % _yn, kut(min(_b, _c), max(_b, _c), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "pu", "V",
         not_="v14 · PU 57,5 (sandviç çekirdeği) · ön yüz +23 / arka −630 = üst yalıtımla aynı düzlem · v7: 1277'den başlar")
    ekle("soguk_duvar_%s_dis_sac" % _yn, kut(min(_c, _d), max(_c, _d), 1277.0, _y1, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "V",
         not_="v14 · AISI 304 1,5 · sandviç dış kabuğu · 2 × Z profille TC yan sacına (28,5 boşluk) — soğuk paketin yük yolu")
ekle("kabin_sag_teknik_sac", kut(W - 1.5, W, Y_TEK, YUST, 0, -D), "kabuk", "V", not_="v11: teknik cebin sağ yan saçı · havalandırma ızgaralı (kondenser havası)")
RAF_T, RAF_BUKUM = 3.0, 40.0
_raf = kut(90, W - 90, SOGUK_TABAN - RAF_T, SOGUK_TABAN, Z_KAPAK[1], Z_BOLME[0])
for _ad, _cx, *_r in UNO:
    _raf = _raf.cut(sily(_cx, ZT, 21.0, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
KAS_Z = -150.0                                   # kaset çıkış borusu ekseni (tabla ekseninin 20 mm önü, v1 ile aynı)
KAS_YARIK_Y0 = 1311.0                            # v14b · kaset tüpünün altı 1312 − 1: kaset yalnız bu kotun ÜSTÜNDEN öne çekilir (ön büküm + alt PU yarığı yalnız 1311–1317)
KAS_R = {"kasar_cad_v14": (30.0, 25.0, 22.5), "sucuk_cad_v8": (30.0, 24.0, 21.0)}   # delik · iniş borusu dış/iç
for _ad, _mod, _x0, _x1 in KASET:
    _raf = _raf.cut(sily((_x0 + _x1) / 2.0, KAS_Z, KAS_R[_mod][0], SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
for _ad, _cx, *_r in UNO:
    if _ad in ("SOS", "HARC"):
        _raf = _raf.cut(sily(_cx - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1))
_rob = kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_KAPAK[1] - RAF_T, Z_KAPAK[1])
for _ad, _mod, _x0, _x1 in KASET:                                                       # v6: kaset çıkış tüpü öne kayarken raftan sıyrılsın: U-yarık + çentik
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    _raf = _raf.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1, KAS_Z, Z_KAPAK[1] + 1))
    _rob = _rob.cut(kut(_xc - _r, _xc + _r, KAS_YARIK_Y0, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))   # v14b: çentik yalnız üst 6 mm, altındaki 34 mm kiriş sürekli
ekle("tasiyici_raf_3mm", _raf, "paslanmaz", "H", not_="AISI 304 · 3 mm · yük 154 kg · sehim 3,4 mm · emniyet 2,3 · ağız delikleri · v6: kaset delikleri öne açık U-yarık (Ø60)")
ekle("raf_on_bukumu", _rob, "paslanmaz", "H", not_="40 mm aşağı büküm (rafın kirişi) · v6: kaset yarıklarında 60 çentik · v14b: çentik yalnız 1311–1317 (tüp + yarık dili geçer), altındaki 34 mm kiriş sürekli")
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
# v14 · İNİŞ BORULARI RAFA ASILI: borunun iki yanında 3 mm kulak (boruya kaynak) + dik lama rafın altına M5 · kulaklar tüpün kayma izinin (±30) dışında (±35…38)
for _ad, _mod, _x0, _x1 in KASET:
    _x = (_x0 + _x1) / 2.0; _, ro, ri = KAS_R[_mod]
    for _sg, _yn in ((-1.0, "sol"), (1.0, "sag")):
        _k = kut(_x + _sg * ro, _x + _sg * 38.0, 1250.0, 1256.0, KAS_Z - 10.0, KAS_Z + 10.0).union(kut(_x + _sg * 35.0, _x + _sg * 38.0, 1256.0, SOGUK_TABAN - RAF_T, KAS_Z - 10.0, KAS_Z + 10.0))
        ekle("%s_boru_kulagi_%s" % (_mod.split("_")[0], _yn), _k, "paslanmaz", "H",
             not_="v14 · 304 lama 3 × 20 · boruya kaynak (yatay kol) + rafın altına 2 × M5 (dik kol 35–38) · iniş borusu + huni v13'te havadaydı")
# v6 · YALITIM TEK BLOK ("tam kare"): dışı düz dikdörtgen; içinde soğuk oda (A tavan 1968 · B tavan 1680), arkaya açık TEKNİK CEP,
#      kaset kovanı / UNO mil kovanı / geçiş bloğu delikleri. Fitil ve kaset yuvaları aşağıda (kasetlerden sonra).
YAL_Y0 = SOGUK_TABAN - 43                                                             # 1277 (raf bükümünün altı)
CEP_TEKNIK = (X_TEK, W, Y_TEK, YUST, Z_KAPAK[1], -D)                                # v11: yalıtımın dışında · 820–1800 × 1720–2030 · arkası açık
# v11 · YALITIM YALNIZ SOĞUK HACMİ SARAR (Kemal): A tavanı · L PU 30 (soğuk ↔ teknik) · arka bölme — teknik cep yalıtımın DIŞINDA
_yal = kut(BAY_A[0], BAY_A[1], TAVAN_A, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1])                             # A tavanı 60
_yal = _yal.union(kut(BAY_A[1], X_TEK, TAVAN_B, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]))                   # L dikey PU 30 (A | teknik)
_yal = _yal.union(kut(X_TEK, BAY_B[1], TAVAN_B, Y_TEK, Z_KAPAK[1], Z_BOLME[1]))                        # L yatay PU 30 (B tavanı)
_yal = _yal.union(kut(BAY_A[0], BAY_A[1], YAL_Y0, TAVAN_A, Z_BOLME[0], Z_BOLME[1]))                    # arka bölme A
_yal = _yal.union(kut(BAY_A[1], BAY_B[1], YAL_Y0, TAVAN_B, Z_BOLME[0], Z_BOLME[1]))                    # arka bölme B
_yal = _yal.cut(kut(89, 1200, 1440, 1470, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                              # geçiş bloğu yuvası (v14: blok ölçüsünde → blok yuvaya değer)
for _ad, _cx, *_r in UNO:
    _yal = _yal.cut(silz(_cx, V_EKSEN, 15.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                         # UNO mil geçiş kovanı (v14: Ø30 = kovan → sıkı geçme)
EVAP_AGIZ = ((720.0, 1080.0, 1570.0, 1610.0), (720.0, 1080.0, 1640.0, 1685.0))                   # v14 · dönüş (alt) + üfleme (üst): TC evaporatörü (dünya x 1400–1800 · y 1392–1572) arka bölmenin hemen arkasında
for _x0, _x1, _y0, _y1 in EVAP_AGIZ:
    _yal = _yal.cut(kut(_x0, _x1, _y0, _y1, Z_BOLME[1] - 1, Z_BOLME[0] + 1))
YAL_BLOK = [_yal]                                                                     # kaset kovan delikleri kasetlerden sonra açılır (ekle orada)
for ad, x0, x1 in (("sogutma_grubu", 850, 1150), ("pano_PLC", 1180, 1580), ("guc_kaynagi", 1600, 1655), ("UPS", 1660, 1709)):
    ekle("teknik_bant_" + ad, kut(x0, x1, TEK_Y0, TEK_Y0 + (240.0 if ad == "pano_PLC" else 220.0), -110, -560), "zarf", "Ö", not_="v11 teknik cep (yalıtımın dışında) · ZARF")
# v10 · TEKNİK AYIRMA SAÇI (mavi L): soğuk hacim ↔ teknik cep, 1,5 mm AISI 304 · kenarları yalıtım bloğuna silikonla
ekle("teknik_ayirma_saci_yatay", kut(X_TEK, W - 1.5, Y_TEK, Y_TEK + SAC_T, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "Ö",
     not_="v11: 1,5 mm AISI 304 · teknik cebin tabanı, PU 30'un üstünde · üstünde soğutma grubu / pano / güç / UPS")
ekle("teknik_ayirma_saci_dikey", kut(X_TEK, X_TEK + SAC_T, Y_TEK + SAC_T, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "Ö",
     not_="v11: 1,5 mm AISI 304 · teknik cebin sol duvarı, PU 30'un sağında")
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
        ekle("%s__urun_silindiri_D70" % k, silz(cx, V_EKSEN, 38, VZ - 172, VZ - 41).cut(silz(cx, V_EKSEN, 33, VZ - 173, VZ - 40)).cut(silz(cx, V_EKSEN, 35, VZ - 165, VZ - 49)), "saydam_celik", "B",
             not_="Beldos Ø70 silindir seçeneği (100–275 ml) · doz %.0f ml > Ø52'nin 151 ml'si · v14: iki ucunda Ø66 iç omuz (7 + 8) → UNO kapağına ve bileziğine oturur" % doz)
        ekle("%s__urun_pistonu_D70" % k, silz(cx, V_EKSEN, 34.7, VZ - 69, VZ - 49), "pom", "H", grup="PISTON_" + ad)
    # ağız: kıyma / kuşbaşı → uzatma borusu (yuvarlak uç 1216) · sos / harç → düz kaplama bıçağı (icing nozzle)
    if agiz == "yassi":
        bc = BICAK[ad]; L_ = bc["boy"]; g_ = bc["yarik"]
        yb = BICAK_ALT + 18.0                         # dağıtıcı boru ekseni (alt yüzü pideden 6 mm)
        xb0, xb1 = cx - 8.0, cx + L_                   # boru merkezden kenara
        # 1 · giriş: TC kelepçe (UNO ağzı ucu) + dik boru
        ekle("%s_spreader_giris_kelepcesi" % k, sily(cx, ZT, 25.0, BICAK_UST, BICAK_UST + 12.0).cut(sily(cx, ZT, 18.0, BICAK_UST - 1, BICAK_UST + 13.0)), "paslanmaz", "F",   # v14: kelepçe boruları sıkar (iç = dış Ø36)
             not_="Beldos spreader attachment · 1,5\" TC kelepçe")
        ekle("%s_spreader_kelepce_kanadi" % k, kut(cx - 4, cx + 4, BICAK_UST + 2, BICAK_UST + 10, ZT + 25, ZT + 40), "paslanmaz", "F")
        ekle("%s_spreader_dik_boru" % k, sily(cx, ZT, 18.0, yb + 40.0, BICAK_UST + 1.5).cut(sily(cx, ZT, 16.5, yb + 39.0, BICAK_UST + 2.5)), "paslanmaz", "F")   # v14: ucu UNO ağzının ucuna (1263,5) oturur (v13: 1,5 boşluk, spreader havadaydı)
        # 2 · havalı kesme valfi (braketli, dik borunun yanında)
        vx = cx - 40.0; v0, v1 = yb + 40.0, yb + 86.0
        ekle("%s_spreader_kesme_valfi_govde" % k, sily(vx, ZT, 14.0, v0, v1), "pom", "F", not_="havalı kesme valfi (drip-free) · beyaz gövde, görselden")
        ekle("%s_spreader_kesme_valfi_kapak" % k, sily(vx, ZT, 15.0, v1, v1 + 8.0), "pom", "F")
        ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 18.5, v0 + 20.0, v0 + 44.0, ZT - 2.0, ZT + 2.0), "paslanmaz", "F")   # v14: UNO ağzına girmez (v13 cx − 16)
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
        ekle("%s_agiz_uzatmasi" % k, sily(cx, ZT, 18, 1216.0, 1263.5).cut(sily(cx, ZT, 16.5, 1180, 1265)), "paslanmaz", "H",
             not_="UNO 90° ağzının ucundan pideye iniş: 48 mm uzatma · uç 1216 (pideden 40)")
    # bizim hazne: boyun + TC + huni + düz gövde
    # v14 · UNO çıkış TC bağlantısının VALF TARAFI ferrulü + contası (beldos_cad_v1 modelinde boru ucu ile ağız ferrulü arasında 9,9 mm boşluk vardı → ağız havada)
    _cb = [p["sh"] for p in P if p["ad"] == "%s__cikis_borusu" % k][0].BoundingBox(); _cf = [p["sh"] for p in P if p["ad"] == "%s__cikis_tc_ferrule" % k][0].BoundingBox()
    ekle("%s__cikis_tc_ferrule_valf" % k, silz(cx, V_EKSEN, _cf.xlen / 2.0 + 0.35, _cb.zmax, _cf.zmin).cut(silz(cx, V_EKSEN, 16.5, _cb.zmax - 1.0, _cf.zmin + 1.0)), "paslanmaz", "B",
         not_="v14 · 1,5\" TC ferrule (valf tarafı, boruya kaynaklı) + EPDM conta · kelepçe bunu ve ağız ferrulünü sıkar (dış Ø = kelepçe iç Ø)")
    ekle("%s_hazne_boynu" % k, sily(cx, VZ, 31.75, V_UST, 1452).cut(sily(cx, VZ, 30.25, V_UST - 1, 1453)), "paslanmaz", "Ö")
    ekle("%s_tc_kelepce_hazne" % k, sily(cx, VZ, 45.5, 1410, 1428).cut(sily(cx, VZ, 31.75, 1409, 1429)), "paslanmaz", "Ö",
         not_="v14 · 2,5\" TC kelepçe · iç Ø63,5 = boyun (sıkınca temas; v13 0,75 mm boşlukla havadaydı)")
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
        _st = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))
        _ss = sorted(_st.solids().vals(), key=lambda s_: -s_.Volume())                                    # v15: Codex STEP'indeki ayrık kırıntılar atılır
        h[0]["wp"] = cq.Workplane(obj=_ss[0]) if len(_ss) > 1 and all(s_.Volume() < 1e-3 * _ss[0].Volume() for s_ in _ss[1:]) else _st
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
        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1))            # v6: yalıtım bloğunda kovan deliği (v14: Ø60 = kovan, sıkı)
        ekle("kovan_" + tag, silz(xc, yy, 30, -648, -565).cut(silz(xc, yy, 11.2, -649, -564)), "pom", "Ö")
        ekle("reduktor_" + tag, TC.suregear_koy(xc, yy, -670.0), "motor", "B", not_="SureGear PGCN23-1025 (katalog STEP)")
        ekle("reduktor_flans_burcu_" + tag, silz(xc, yy, 28.0, -670.0, -648.0).cut(silz(xc, yy, 15.0, -671.0, -647.0)), "paslanmaz", "V",
             not_="v14 · redüktör flanşı ↔ kovan ara burcu 304 Ø56/Ø30 × 22 · 4 × M5 · redüktör + motor kovana (kovan yalıtıma sıkı) asılır — v13'te havadaydı")
        g, kb = TC.nema23_koy(xc, yy, -670.0 - 79.0)                                               # v14: motor redüktörün giriş yüzüne oturur (v13: 2 mm boşluk)
        ekle("motor_" + tag, g, "motor", "B", not_="AutomationDirect STP-MTR-23079 (katalog STEP)")
        _kbs, _gms = kb.val(), g.val(); _kbb, _gbb = _kbs.BoundingBox(), _gms.BoundingBox()                  # v14b · kablo rakoru (denetim_C bulgu 4)
        _rak = sily((_kbb.xmin + _kbb.xmax) / 2.0, (_kbb.zmin + _kbb.zmax) / 2.0, 5.0, _gbb.ymin - 12.0, _gbb.ymin).val()
        ekle("motor_kablosu_" + tag, _kbs.fuse(_rak), "koyu", "B",
             not_="motor kablosu (katalog STEP ucu) · v14b: kablo rakoru Ø10 × 12 (PG7 sınıfı, VARSAYIM) motor gövdesinin yüzüne oturur — STEP'te kablo gövdeden 0,707 mm açıktı")

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
    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 4.0, 1.6, px0 - 23.5, px0 - 5.5), "celik", "K", not_="Pim ISO 8734 3 m6 × 18 A1: iki yan duvara sıkı geçme, dil üstünde kayar (0,5 içeride) · v14: modelde delik çapında (sıkı geçme = temas)")
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
     not_="v11 YALNIZ SOĞUK HACMİ SARAR · PU (sac kaplı): A tavanı 60 · L 30 (soğuk ↔ teknik) · arka bölme 65 · soğuk hacim A tavan 1968 / B 1690 · teknik cep yalıtımın dışında · 4 kaset kovanı + 4 UNO kovanı + geçiş bloğu delikleri")
# v14 · ESKİ ÖN FİTİL (z −104) KALKTI — fitil artık soğuk kapakların (K1 / K2) arkasında (+24…+39), bkz. bölüm 5b (ÖN YÜZ)
FITIL_BOSLUK = (1325.0, 1455.0)                                                       # (tarihçe) v8: itici geçişi — v9 kesiksiz · v14: fitil kapakta

# ================================================================ 4 · HAVA TESİSATI
ekle("sartlandirici_filtre_regulator", kut(*FRL), "aluminyum", "V", not_="filtre + regülatör + ana vana · 7 bar")
ekle("sartlandirici_manometre", silz(1675, 1380, 14, -700, -690), "pom", "V")
ekle("valf_adasi_12x5_2", kut(*ADA), "aluminyum", "V", not_="12 × 5/2 elektro-valf: 4 piston + 4 döner valf + 2 spreader kesme valfi + açıcı + yedek")
for n in range(12):
    x = ADA[0] + 14 + n * 24.0
    ekle("valf_bobini_%d" % (n + 1), kut(x, x + 18, ADA[3], ADA[3] + 30, -680, -740), "siyah", "V")
ekle("gecis_blogu_yalitim", kut(90, 1200, 1440, 1470, Z_BOLME[0], Z_BOLME[1]), "pom", "V", not_="hortumların soğuk hücreye geçtiği keçeli blok")
# ana hat: K tabanındaki kompresör → F tabanı arka köşe → C'ye sağ alttan → şartlandırıcı → ada
ana = [(3600, 1001, -380), (3600, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]   # v14: başı motorun arkasındaki vanada (y 1001)
ekle("hava_ana_hatti_D10", boru(ana, 5.0), "hava_ana", "V", not_="Ø10 PU · K tabanı → F tabanı arka köşe kanalı → TOPPING sağ alt")
ekle("hava_hatti_sartlandirici_ada", boru([(1675, 1420, -740), (1675, 1552, -740), (470, 1552, -740), (470, 1630, -740), (458, 1630, -740)], 5.0), "hava_ana", "V",
     not_="evaporatörün altından, kaset motorlarının üstünden geçer")
# v14 · AÇICI HATTI 2 × Ø6 (iki yönlü silindir): valf adasından sola → TC sol yan sacındaki 2 rakordan (dünya y 1472 / 1460, z −700 / −712) A'ya → Z silindirinin
#       (TC v25 acici_pnomatigi, Festo DSBC-32-100, dünya x 327,5–372,5 · y 1280–1474 · z −562,5…−517,5) +x yüzündeki portlara (arka port dünya y 1460, ön port 1292)
for _j, (_yA, _zA, _xd, _yP, _renk) in enumerate(((1640.0, -700.0, 420.0, 1460.0, "hortum_mavi"), (1628.0, -712.0, 428.0, 1292.0, "hortum_siyah"))):
    ekle("hava_hatti_acici_D6_%d" % (_j + 1), boru([(ADA[0], _yA, _zA), (xu(_xd), _yA, _zA), (xu(_xd), yu(_yP), _zA), (xu(_xd), yu(_yP), -540.0), (xu(372.5), yu(_yP), -540.0)], 3.0), _renk, "V",
         not_="v14 · Ø6 PU · valf adası → TC sol yan sacı rakoru → açıcı Z silindiri (%s port) · v13'te tek hat, A'da boşta bitiyordu" % ("arka" if _j == 0 else "ön"))
# v14 · UNO HORTUMLARI AYRIK YOLLARDA (v13'te 4 UNO'nun hortumları aynı çizgide üst üste biniyordu): piston hortumları y 1386 + 8·(2i + j), z −672 ·
#       döner valf hortumları z −690 − 16·i − 8·j, y 1452 / 1460 (geçiş bloğunun içinden, ağ 8)
HORTUM_GECIS = []
for i, (ad, cx, *_r) in enumerate(UNO):
    k = ad.lower(); tx = ADA[0] + 20 + i * 48.0
    for j, (zp, renk) in enumerate(((-680.0, "hortum_mavi"), (-800.0, "hortum_siyah"))):
        dx = j * 8.0; yh = 1386.0 + 8.0 * (2 * i + j)
        ekle("%s_hortum_silindir_%d" % (k, j + 1), boru([(tx + dx, ADA[2], -672.0), (tx + dx, yh, -672.0), (cx + dx, yh, -672.0),
                                                       (cx + dx, yh, zp), (cx + dx, V_EKSEN + 19, zp)], 3.0), renk, "V")
    for j, renk in enumerate(("hortum_mavi", "hortum_siyah")):
        dx = j * 8.0; ex = cx - 72 + dx; zi = -690.0 - 16.0 * i - 8.0 * j; yj = 1452.0 + 8.0 * j
        ekle("%s_hortum_doner_valf_%d" % (k, j + 1), boru([(tx + 24 + dx, ADA[2], zi), (tx + 24 + dx, yj, zi), (ex, yj, zi),
                                                          (ex, yj, -420), (ex, V_EKSEN + 22, -420)], 3.0), renk, "V")
        HORTUM_GECIS.append("%s_hortum_doner_valf_%d" % (k, j + 1))
HORTUM_GECIS += ["%s_spreader_hava_hortumu" % a_.lower() for a_ in ("SOS", "HARC")]
for q in P:                                                                          # v14: geçiş bloğunda hortum delikleri (hortum çapında, keçeli)
    if q["ad"] == "gecis_blogu_yalitim":
        for p in P:
            if p["ad"] in HORTUM_GECIS:
                q["sh"] = q["sh"].cut(p["sh"])
# kompresör (bağlam: F ve K tabanları hayalet)
ekle("baglam_F_tabani", kut(1800, 3300, 123, 1060, 0, -D), "hayalet", "Ö", not_="modül F taban dolabı (bağlam)")
ekle("baglam_K_tabani", kut(3300, 3900, 123, 1060, 0, -D), "hayalet", "Ö", not_="modül K taban dolabı · boş (Kemal 24 Eyl: yedek kutu yok)")
ekle("baglam_A_modulu", kut(-700, 0, Y0, YUST, 0, -D), "hayalet", "Ö", not_="modül A açıcı (bağlam)")
ekle("kompresor_JUNAIR_OF302_15B_tank", silx((KOMP[2] + 170), (KOMP[4] + KOMP[5]) / 2, 150, KOMP[0], KOMP[1]), "kompresor", "B",
     not_="JUN-AIR OF302-15B · yağsız · 15 L · 380 × 380 × 510 · 25 kg · 43 L/dk @ 7 bar · 65 dB")
ekle("kompresor_JUNAIR_OF302_15B_motor", kut(KOMP[0] + 40, KOMP[1] - 40, KOMP[2] + 320, KOMP[3], KOMP[4] - 40, KOMP[5] + 60), "kompresor", "B")
ekle("kompresor_cikis_vanasi", silz(3600, 1001.0, 8, -380.0, KOMP[5] + 60.0), "siyah", "V",
     not_="v14 · motorun arka yüzüne bağlı çıkış vanası (z −380…−360) · ucu = montaj ana hattının başı (dünya 3790, 1809, −380) · v13'te motorun 20 mm arkasında havadaydı")


# ================================================================ v14b · SOĞUK ODA TABANI SIZDIRMAZ (denetim_C bulgu 1 · KRİTİK)
# Raf dilimi (y 1317–1320) ürün kanalları dışında TAM kapalı olmalı. v14'te kaset U-yarıkları raf + ön büküm + alt PU + alt sac boyunca öne açıktı
# (2 × ≈9 800 mm² doğrudan hava yolu) + UNO ağız halkaları (4 × 360) + hortum delikleri (2 × 50) → soğuk hava mekanizma bandına (ürün yoluna) iniyordu.
#   · KASET YARIK DİLİ (POM-C, kasetin tüpüne yarıklı yaka ile sıkılı → KASETLE BİRLİKTE çıkar, unutulamaz): raf U-yarığını tüpün önünde doldurur,
#     alt PU'nun üst yarığında (1311–1317) tüpü sarar, 430 çerçeve çentiğini ön flanşıyla kapatır (fitil zaten çentiğin altından geçer)
#   · RAF KASET CONTASI (silikon dudak, SABİT): raf deliğinin arka yarısında tüp ↔ delik halkası
#   · RAF GEÇİŞ CONTALARI (silikon grommet): UNO ağızları Ø36 ↔ raf deliği Ø42 · spreader hortumları Ø6 ↔ Ø10
#   · alt PU: kaset yalnız ÜST 6 mm yarıktan öne çekilir; iniş borusu + huni SABİT → altları ve önleri dolu PU (delikleri öne açık DEĞİL)
def _kesit(sh, y=1318.5):
    """y düzlemindeki boru kesiti → (merkez x, merkez z, dış r, iç r) · iç r alandan"""
    k = sh.intersect(kut(-1.0e4, 1.0e4, y - 0.05, y + 0.05, -2000.0, 500.0).val()); b = k.BoundingBox(); a = k.Volume() / 0.1
    ro = (b.xlen + b.zlen) / 4.0
    return ((b.xmin + b.xmax) / 2.0, (b.zmin + b.zmax) / 2.0, ro, math.sqrt(max(0.0, ro * ro - a / math.pi)))
KANAL = []                                                                            # ürün kanalları (x, z, iç r, ad) — soğuk taban kaçak denetiminde muaf
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]; _k = _mod.split("_")[0]
    _tup = [p["sh"] for p in P if p["ad"] == "%s__cikis_tupu" % _mod][0]
    _tx, _tz, _to, _ti = _kesit(_tup); KANAL.append((_tx, _tz, (_to + _ti) / 2.0, "%s tüpü" % _k))           # kanal = boru etinin ortasına kadar (et zaten dolu)
    _dolu = sily(_tx, _tz, (_to + _ti) / 2.0, KAS_YARIK_Y0 - 1.0, SOGUK_TABAN + 1.0)                          # tüp + içi (et ortası) → dil / conta tüpün DIŞ yüzünden başlar
    _dil = kut(_xc - _r, _xc + _r, KAS_YARIK_Y0 + 1.0, SOGUK_TABAN, KAS_Z, Z_ZARF)                              # raf U-yarığı + ön büküm çentiği + alt PU üst yarığı (tüpün önü)
    _dil = _dil.union(sily(_xc, KAS_Z, _r, KAS_YARIK_Y0 + 1.0, SOGUK_TABAN - RAF_T))                            # alt PU üst yarığında tüpü saran yaka (Ø60)
    _dil = _dil.union(kut(_xc - _r - 1.0, _xc + _r + 1.0, KAS_YARIK_Y0, SOGUK_TABAN, Z_CER[0], Z_CER[1]))      # ön flanş: 430 çerçeve çentiği (62 × 9) kapanır
    _dil = _dil.cut(_dolu).cut(_tup)
    ekle("%s_yarik_dili" % _mod, _dil, "pom", "V",
         not_="v14b · KASET YARIK DİLİ POM-C (gıda) · %.0f × %.0f × 8 + Ø60 yaka + 62 × 9 ön flanş · kasetin tüpüne yarıklı yaka ile 2 × M4 A2 (kelebek) → kasetle BİRLİKTE çıkar · "
              "raf U-yarığını + ön büküm / alt PU üst yarığını + 430 çerçeve çentiğini kapatır (denetim_C bulgu 1: v14'te ≈9 800 mm² doğrudan hava yolu)" % (2 * _r, Z_ZARF - KAS_Z))
    _yk = sily(_xc, KAS_Z, _r, SOGUK_TABAN - RAF_T, SOGUK_TABAN).intersect(kut(_xc - _r - 1.0, _xc + _r + 1.0, SOGUK_TABAN - RAF_T - 1.0, SOGUK_TABAN + 1.0, KAS_Z - _r - 1.0, KAS_Z))
    ekle("raf_kaset_contasi_%s" % _k, _yk.cut(_dolu).cut(_tup), "conta", "K",
         not_="v14b · gıda tipi silikon dudak conta (yarım halka: raf deliğinin arka yarısı Ø60 ↔ tüp Ø%.0f) · raf deliğine yapışık, SABİT · kaset çekilince tüp öne kayar, conta yerinde kalır" % (2 * _to))
for _ad, _cx, *_r in UNO:
    _k = _ad.lower(); _ag = [p["sh"] for p in P if p["ad"] == "%s__agiz_90_derece" % _k][0]
    _ax, _az, _ao, _ai = _kesit(_ag); KANAL.append((_ax, _az, (_ao + _ai) / 2.0, "%s ağzı" % _k))
    ekle("raf_gecis_contasi_%s" % _k, sily(_cx, ZT, 21.0, SOGUK_TABAN - RAF_T, SOGUK_TABAN).cut(sily(_ax, _az, (_ao + _ai) / 2.0, SOGUK_TABAN - RAF_T - 1.0, SOGUK_TABAN + 1.0)).cut(_ag), "conta", "K",
         not_="v14b · gıda tipi silikon geçiş contası (grommet) · raf deliği Ø42 ↔ UNO ağzı Ø%.0f · 3 mm halka kapanır (v14: açık, 360 mm²)" % (2 * _ao))
    if _ad in ("SOS", "HARC"):
        _h = [p["sh"] for p in P if p["ad"] == "%s_spreader_hava_hortumu" % _k][0]
        ekle("raf_gecis_contasi_%s_hortum" % _k, sily(_cx - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T, SOGUK_TABAN).cut(_h), "conta", "K",
             not_="v14b · hortum geçiş lastiği Ø10 → Ø6 hortum (v14: 50 mm² açık)")
# v14b · SAĞ DUVAR ALT PROFİLİ (denetim_C bulgu 11): aktarma iticisinin montaj kirişi (itici_cad_v5, dünya y 1103–1109) sağ ucuyla buna bağlanır — v14'te kiriş yalnız 1 mm alt sac + PU'ya değiyordu
ekle("soguk_duvar_sag_alt_profili", kut(BAY_B[1] + 60.0, W - 1.5, YAL_Y0, 1290.0, -245.0, -180.0), "paslanmaz", "H",
     not_="v14b · lama 28,5 × 13 × 65 AISI 304 · soğuk duvarın dış sacı ↔ TC sağ yan sacı arası (Z profilin altına kaynak + TC yan sacına 2 × M6) · itici montaj kirişi (dünya x 2044,5–2489,5) sağ ucu buna 2 × M6 · yük: kiriş → profil → TC yan sacı")


def soguk_taban_kacagi(parcalar, dx=0.0, dy=0.0):
    """v14b · soğuk oda tabanı (raf dilimi y 1317,5–1319,5 TU; dünyada + dy) ürün kanalları DIŞINDA açık alan (mm²) · parcalar: [(ad, şekil)] · (alan, [(alan, kutu)])"""
    R = kut(BAY_A[0] + dx, BAY_B[1] + dx, SOGUK_TABAN - RAF_T + 0.5 + dy, SOGUK_TABAN - 0.5 + dy, Z_BOLME[0], Z_ZARF).val(); rb = R.BoundingBox()
    for _a, sh in parcalar:
        b = sh.BoundingBox()
        if b.xmax < rb.xmin or b.xmin > rb.xmax or b.ymax < rb.ymin or b.ymin > rb.ymax or b.zmax < rb.zmin or b.zmin > rb.zmax: continue
        try: R = R.cut(sh)
        except ValueError: return 0.0, []                                          # kesim sonucu BOŞ (OCC boş şekil) → açık alan 0
    for x_, z_, r_, _n in KANAL:
        try: R = R.cut(sily(x_ + dx, z_, r_, rb.ymin - 1.0, rb.ymax + 1.0).val())
        except ValueError: return 0.0, []
    kal = [(s.Volume() / (rb.ymax - rb.ymin), s.BoundingBox()) for s in R.Solids() if s.Volume() > 1e-6]
    return sum(a for a, _b in kal), kal


def cerceve_bandi_acik(parcalar, dx=0.0, dy=0.0):
    """v14b · 430 çerçeve düzlemi (z 23,25–23,75) soğuk oda ALTINDAKİ bantta (y 1277–1320 TU) açık alan (mm²) — kaset çentikleri yarık dili flanşıyla kapalı olmalı"""
    R = kut(1.5 + dx, W - 1.5 + dx, YAL_Y0 + dy, SOGUK_TABAN + dy, Z_CER[0] + 0.25, Z_CER[1] - 0.25).val(); rb = R.BoundingBox()
    for _a, sh in parcalar:
        b = sh.BoundingBox()
        if b.xmax < rb.xmin or b.xmin > rb.xmax or b.ymax < rb.ymin or b.ymin > rb.ymax or b.zmax < rb.zmin or b.zmin > rb.zmax: continue
        try: R = R.cut(sh)
        except ValueError: return 0.0, []
    kal = [(s.Volume() / 0.5, s.BoundingBox()) for s in R.Solids() if s.Volume() > 1e-6]
    return sum(a for a, _b in kal), kal

# ================================================================ v12 · SOĞUK ODANIN ALTI: sac kaplı PU (Kemal: "altına da az da olsa yalıtım yap")
#   rafın (1317–1320) altı, ön büküm (z −107…−104) ile arka büküm (z −565…−562) arası, x 90–1710 (yan PU duvarlar 1277'den başlar → birleşir)
#   alt sac 1 (1277–1278) + PU 39 (1278–1317) · kalın taban geri gelmez: raf, disk ve hat kotları aynı
ALT_YAL = (BAY_A[0], BAY_B[1], YAL_Y0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T)   # x · y 1277–1317 · z −562…−107
ALT_PAY = 3.0
_alt = kut(*ALT_YAL)
ALT_DELIK = []
_ab = _alt.val().BoundingBox()
ALT_YARIK = []                                                                                # v14b · kaset ÜST yarıkları (y 1311–1317, öne açık)
for p in P:
    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski")):
        continue
    if any(p["ad"].startswith(m_) for _a, m_, _x0, _x1 in KASET):
        continue                                                                              # v14b: öne çekilen kaset parçaları (tüp + yarık dili) → yalnız üst yarık (aşağıda)
    b_ = p["sh"].BoundingBox()
    if not (b_.xmin < _ab.xmax and _ab.xmin < b_.xmax and b_.ymin < _ab.ymax and _ab.ymin < b_.ymax and b_.zmin < _ab.zmax and _ab.zmin < b_.zmax):
        continue
    try:
        _k = _alt.val().intersect(p["sh"]); v_ = abs(_k.Volume()); lb = _k.BoundingBox() if v_ > 0.5 else None
    except Exception:
        v_, lb = 1.0, None
    if v_ <= 0.5 and not p["ad"].endswith("hava_hortumu"):
        continue
    x0_, x1_, z0_, z1_ = b_.xmin, b_.xmax, b_.zmin, b_.zmax
    if lb is not None and lb.xlen > 0.1:
        x0_, x1_, z0_, z1_ = lb.xmin, lb.xmax, lb.zmin, lb.zmax                                # delik yalnız yalıtımın İÇİNDEKİ kısım kadar
    else:                                                                                     # v14b: boru bileşiği (hortum) → katı katı kesişim (v14: tüm hortum kutusu, 72 × 473 delik)
        try:
            _lk = [q_.BoundingBox() for q_ in (s_.intersect(_alt.val()) for s_ in p["sh"].Solids()) if q_.Volume() > 0.01]
            if _lk:
                x0_, x1_, z0_, z1_ = min(q.xmin for q in _lk), max(q.xmax for q in _lk), min(q.zmin for q in _lk), max(q.zmax for q in _lk)
        except Exception:
            pass
    ALT_DELIK.append((p["ad"], x0_ - ALT_PAY, x1_ + ALT_PAY, z0_ - ALT_PAY, z1_ + ALT_PAY))   # v14b: iniş borusu / huni dahil HİÇBİRİ öne açık değil
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    ALT_YARIK.append((_mod, _xc - _r, _xc + _r, KAS_Z - _r - ALT_PAY, ALT_YAL[5] + 1.0))
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    _alt = _alt.cut(kut(x0_, x1_, ALT_YAL[2] - 1.0, ALT_YAL[3] + 1.0, z0_, z1_))
for _ad, x0_, x1_, z0_, z1_ in ALT_YARIK:
    _alt = _alt.cut(kut(x0_, x1_, KAS_YARIK_Y0, ALT_YAL[3] + 1.0, z0_, z1_))
ekle("alt_yalitim_saci", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], ALT_YAL[2], ALT_YAL[2] + 1.0, ALT_YAL[4], ALT_YAL[5])).val(), "paslanmaz", "V",
     not_="v12 · AISI 304 1,0 · soğuk oda yalıtımının alt kabuğu (aşağı bakar, pişirme bölgesinin üstü) · rafın bükümlerine perçin")
ekle("alt_yalitim_PU", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], ALT_YAL[2] + 1.0, ALT_YAL[3], ALT_YAL[4], ALT_YAL[5])).val(), "pu", "V",
     not_="v12 · PU 39 (40 kg/m³) · rafın altı, bükümlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik · v14b: kaset yalnız ÜST 6 mm yarık (öne açık, yarık diliyle dolu), iniş borusu + huni altı / önü dolu")


# ================================================================ 5b · v14 · YÜK YOLU + ÖN YÜZ (SPEC_on_duzlem_v63 §1 + §2.3)
# (a) RAF KÖŞEBENTLERİ L 40 × 40 × 3 (304): rafın iki ucu bunlara oturur; köşebent duvarın iç sacına M6, bükümlerin arasında (z −562…+20)
RAF_L = {}
for _yn, _x0, _sg in (("sol", BAY_A[0], 1.0), ("sag", BAY_B[1], -1.0)):
    _L = kut(_x0, _x0 + _sg * 40.0, SOGUK_TABAN - RAF_T - 3.0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T)
    _L = _L.union(kut(_x0, _x0 + _sg * 3.0, YAL_Y0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T))
    if _yn == "sol":                                                                    # sos spreader hava hortumu raftaki Ø10 delikten geçer → köşebentte de aynı delik
        _L = _L.cut(sily(UNO[0][1] - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T - 4.0, SOGUK_TABAN - RAF_T + 1.0))
    RAF_L[_yn] = _L
    ekle("raf_kosebendi_%s" % _yn, _L, "paslanmaz", "H",
         not_="v14 · L 40 × 40 × 3 AISI 304 · rafın ucu yatay koluna oturur (M5 havşa) · dik kol duvarın iç sacına 4 × M6 · raf 154 kg → uç başına 0,76 kN")
for q in P:                                                                            # alt yalıtım köşebendi sarar (tam ölçü kesik)
    if q["ad"] in ("alt_yalitim_PU", "alt_yalitim_saci"):
        for _L in RAF_L.values():
            q["sh"] = q["sh"].cut(_L.val())
# (b) Z PROFİLLER 2 mm: duvarın dış sacı (x 30 / 1770) ↔ TC yan sacının iç yüzü (dünya 701,5 / 2498,5 = x 1,5 / 1798,5) · 28,5 boşluk · 2 kat
ZPROF = []
for _yn, _xa, _xb, _ys in (("sol", 1.5, BAY_A[0] - 60.0, (1290.0, 1900.0)), ("sag", W - 1.5, BAY_B[1] + 60.0, (1290.0, 1640.0))):
    _sg = 1.0 if _xb > _xa else -1.0
    for _i, _y0 in enumerate(_ys):
        _z = kut(_xa, _xa + _sg * 2.0, _y0, _y0 + 30.0, -600.0, -20.0)
        _z = _z.union(kut(_xa, _xb, _y0 + 28.0, _y0 + 30.0, -600.0, -20.0)).union(kut(_xb - _sg * 2.0, _xb, _y0 + 28.0, _y0 + 58.0, -600.0, -20.0))
        ekle("soguk_duvar_%s_z_profili_%d" % (_yn, _i), _z, "paslanmaz", "H",
             not_="v14 · Z profil 30 × 28,5 × 30 × 2 AISI 304 · boy 580 · TC yan sacına 4 × M6 (dıştan kör perçin somun) + duvarın dış sacına 4 × M6 · ısı köprüsü: PU arkasında, dış sacta")
        ZPROF.append("soguk_duvar_%s_z_profili_%d" % (_yn, _i))

# (c) ÖN YÜZ · 430 ÇERÇEVE SACI (+23…+24): soğuk zarfın bütün ön yüzünü örter, L ağız açık; kaset tüpü çentikleri (fitilin İÇİNDE → conta sürekli)
CER_DIS = [(1.5, YAL_Y0), (W - 1.5, YAL_Y0), (W - 1.5, Y_TEK), (X_TEK, Y_TEK), (X_TEK, YUST - 1.5), (1.5, YUST - 1.5)]
AGIZ_L = [(BAY_A[0], SOGUK_TABAN), (BAY_B[1], SOGUK_TABAN), (BAY_B[1], TAVAN_B), (BAY_A[1], TAVAN_B), (BAY_A[1], TAVAN_A), (BAY_A[0], TAVAN_A)]
CENTIK_Y0 = 1311.0                                                                     # kaset tüpünün altı 1312 (dünya 1144) − 1
_cer = cq.Workplane("XY", origin=(0, 0, Z_CER[0])).polyline(CER_DIS).close().extrude(1.0)
_cer = _cer.cut(cq.Workplane("XY", origin=(0, 0, Z_CER[0] - 1.0)).polyline(AGIZ_L).close().extrude(3.0))
CENTIK = []
for _ad, _mod, _x0, _x1 in KASET:
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0] + 1.0
    CENTIK.append((_xc - _r, _xc + _r))
    _cer = _cer.cut(kut(_xc - _r, _xc + _r, CENTIK_Y0, SOGUK_TABAN + 1.0, Z_CER[0] - 1.0, Z_CER[1] + 1.0))
ekle("onyuz_soguk_cerceve_saci", _cer, "sac", "Ö",
     not_="v14 · 430 ferritik 1,0 (manyetik fitil tutar; 304 tutmaz) · BOM notu 430 · soğuk zarfın ön yüzüne yapıştırma + kenarda TC yan saclarına · kaset tüpü çentikleri 62 × 9 (fitilin içinde) · terleme: çevresinde ısıtıcı kablo (VARSAYIM 10 W/m)")

# (d) SOĞUK KAPAKLAR K1 (sol menteşe) + K2 (sağ menteşe) · 40 sandviç (dış 304 fırçalı 1,5 dört kenardan bükülü + PU 37,5 + iç 304 1,0) · fitil kanalı iç sacda
FITIL_G = 4.0
FITIL_PROF = [(-2.0, -31.7), (2.0, -31.7), (2.0, -33.0), (3.15, -34.0), (2.0, -35.2), (2.0, -40.0), (6.0, -40.0), (6.0, -42.0), (8.0, -42.0), (8.0, -50.0),
              (10.5, -50.0), (10.5, -55.0), (-10.5, -55.0), (-10.5, -50.0), (-8.0, -50.0), (-8.0, -42.0), (-6.0, -42.0), (-6.0, -40.0), (-2.0, -40.0),
              (-2.0, -35.2), (-3.15, -34.0), (-2.0, -33.0)]              # store_cad_v7 FITIL (z: kapak ön yüzü 0) → burada + Z_ON
KANAL_PROF = [(-3.2, -31.6), (3.2, -31.6), (3.2, -40.05), (-3.2, -40.05)]


def cevre_supur(ax0, ax1, ay0, ay1, prof):
    """store_cad_v7.cevre_supur · açıklık (ax0..ax1 × ay0..ay1) çevresinde FITIL_G dışarıdaki yol · z + Z_ON"""
    g = FITIL_G
    Pp = [((ax0 + ax1) / 2.0, ay0 - g), (ax1 + g, ay0 - g), (ax1 + g, ay1 + g), (ax0 - g, ay1 + g), (ax0 - g, ay0 - g)]
    yol = cq.Workplane("XY", origin=(0, 0, Z_ON - 40.0)).polyline(Pp).close()
    pts = [(ay0 - g - u, zz + Z_ON) for u, zz in prof]
    return cq.Workplane("YZ", origin=((ax0 + ax1) / 2.0, 0, 0)).polyline(pts).close().sweep(yol, transition="right")


# dünya ölçüleri (SPEC §2.3) → TU: x − 700 · y + 168
SKAPAK = {"K1": dict(x=(xu(701.5), xu(1518.5)), y=(yu(1110.5), yu(1859.0)), fitil=(BAY_A[0], xu(1500.0), yu(1136.0), TAVAN_A), mentese="sol"),
          "K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1550.5)), fitil=(xu(1537.5), BAY_B[1], yu(1136.0), TAVAN_B), mentese="sag")}
for _kn, _k in SKAPAK.items():
    (x0, x1), (y0, y1) = _k["x"], _k["y"]; z0, z1 = Z_SKAPAK; ac = _k["fitil"]
    _ds = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 - 1.0, z1 - 1.5))
    _pu = kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 + 1.0, z1 - 1.5)
    _ic = kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0, z0 + 1.0)
    _kn_ = cevre_supur(*ac, KANAL_PROF)
    _pu, _ic = _pu.cut(_kn_), _ic.cut(_kn_)
    # v15 · kanal DIŞINDAKİ halka = dış sacın ARKA DÖNÜŞÜ (1,5) · iç sac = yalnız kanalın İÇİNDEKİ panel (v14: iç sac kanalla ikiye bölünüyordu)
    _pl = kut(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, z0, z0 + 1.5).cut(_kn_)
    _pp = sorted(_pl.solids().vals(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    assert len(_pp) == 2, "%s: kanal dış halkası %d parça" % (_kn, len(_pp))
    _halka = cq.Workplane(obj=_pp[0])
    _ds = _ds.union(_halka); _pu = _pu.cut(_halka)
    _ip = sorted(_ic.solids().vals(), key=lambda s_: s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    assert len(_ip) == 2, "%s: iç sac %d parça" % (_kn, len(_ip))
    _ic = cq.Workplane(obj=_ip[0])
    assert len(_ds.solids().vals()) == 1, "%s: dış sac tek parça değil" % _kn
    _kg = ((x1 - x0) * (y1 - y0) * 1.5 + 2 * (x1 - x0 + y1 - y0) * 38.5 * 1.5 + (x1 - x0 - 3) * (y1 - y0 - 3) * 1.0) * 7.93e-6 + (x1 - x0 - 3) * (y1 - y0 - 3) * 37.5 * 40e-9
    ekle("onyuz_%s_dis_sac" % _kn, _ds, "sac", "Ö",
         not_="v15 · soğuk kapak %s %.1f × %.1f × 40 · AISI 304 fırçalı 1,5 dört kenardan 40 bükülü + arkada kanal kenarına kadar dönüş (kulpsuz, bas-aç) · ≈%.1f kg · gizli menteşe %s" % (_kn, x1 - x0, y1 - y0, _kg, _k["mentese"]))
    ekle("onyuz_%s_pu" % _kn, _pu, "pu", "Ö", not_="v14 · PU 37,5 (40 kg/m³) · fitil kanalı")
    ekle("onyuz_%s_ic_sac" % _kn, _ic, "paslanmaz", "Ö", not_="v15 · AISI 304 1,0 · kanalın İÇİNDEKİ panel (tek parça) · fitil dişi dış sacın arka dönüşü ile bu panel arasındaki 6,4 × 8,4 kanala geçer")
    ekle("onyuz_%s_fitil" % _kn, cevre_supur(*ac, FITIL_PROF), "conta", "K",
         not_="v14 · geçmeli manyetik fitil 21 × 18,5 (sıkışınca 15) · store_cad_v7 ile aynı profil · 430 çerçeveye / flipper'a basar · çevre %.0f mm" % (2 * (ac[1] - ac[0] + ac[3] - ac[2] + 4 * FITIL_G)))
# v14b · SOĞUK KAPAK MENTEŞELERİ (denetim_C bulgu 2 + 3): ÇOK KOLLU gizli menteşe, SANAL dönme merkezi kapağın ÖN DIŞ KÖŞESİ (K1 x 701,5 · K2 x 2497, z +79) —
#       kapak dönerken kendi dış kenarının ötesine (A / F derzine) geçmez · KOL (kapak tarafı) kapağın iç sacına, TABAN (gövde tarafı) TC yan sacının iç yüzüne
#       + ön dönüşünün arkasına (v14: menteşe yalnız 1 mm 430 çerçeveye yapışıktı, yan saca bağlanamıyordu)
K1_PIVOT = (xu(701.5), Z_ON); K2_PIVOT = (xu(2497.0), Z_ON)
for _ad, _x0, _x1, _y0, _tx in (("K1_mentese_0", 31.5, 55.0, 1330.0, (1.5, 31.5)), ("K1_mentese_1", 31.5, 55.0, 1900.0, (1.5, 31.5)),
                               ("K2_mentese_0", xu(2443.0), xu(2468.5), 1330.0, (xu(2468.5), xu(2498.5))), ("K2_mentese_1", xu(2443.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0]), "paslanmaz", "K",
         not_="v14b · çok kollu gizli menteşe KOLU (kapak tarafı · 3B ayarlı, Sugatsune HES3D sınıfı — parça no + ölçü + sanal pivot VARSAYIM, föy doğrulanacak) · kapağın iç sacına perçin somun · kapak %s"
              % ("≈14,4 kg" if _ad.startswith("K1") else "≈10,4 kg"))
    ekle("onyuz_mentese_tabani_" + _ad, kut(_tx[0], _tx[1], _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0] - 1.5), "paslanmaz", "K",
         not_="v14b · menteşe TABANI AISI 304 blok 30 × 13,5 × 70 · TC yan sacının iç yüzüne 2 × M6 + ön dönüşün (+37,5…+39) arkasına dayalı · kol buna 2 × M5 (denetim_C bulgu 3)")
for _ad, _x0, _x1, _y0, _y1 in (("basac_K1", 780.0, 810.0, 1990.0, 2020.0), ("basac_K2", 830.0, 870.0, 1705.5, 1717.5)):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y1, Z_CER[1], Z_SKAPAK[0]), "plastik", "K",
         not_="v14 · bas-aç mandal (push-to-open, gizli) · Southco E4 sınıfı — parça no + ölçü VARSAYIM · kapak kulpsuz · v14b: gövde tarafı (çerçevede), ad onyuz_basac_K*")
# (e) FLIPPER v14b (denetim_C bulgu 2) — katlanır orta dikme, ısıtıcılı, K1'in iç yüzünde MENTEŞELİ:
#     katlanma ekseni FLIP_EKSEN (dünya x 1493 · z +20, dikey; menteşe braketi K1 fitilinin solunda) · BURULMA YAYI flipper'ı KATLAR (sağ ucu geriye, −90°) ·
#     raf üstündeki KILAVUZ BLOĞUNUN kam oluğu flipper'ın altındaki pimi yönlendirir: katlanma = min(90°, FLIP_K · α) (α = K1 açısı) → sağ ucu K2'nin
#     arkasından K1 dönmeden çekilir (K2 KAPALIYKEN K1 açılır) · K1 kapanırken pim oluğa ön yüzden −90°'de girer, oluk flipper'ı DÜZLER · K2 tek başına
#     açılırken pim oluğun kapalı ucunda tutulur (flipper düz kalır)
FLIP_EKSEN = (xu(1493.0), 20.0); FLIP_K = 30.0
KILAVUZ = (xu(1440.0), xu(1547.0), SOGUK_TABAN, SOGUK_TABAN + 15.0, -40.0, Z_CER[1])
FLIP = (xu(1493.0), xu(1547.0), KILAVUZ[3] + 0.5, TAVAN_B - 0.5)
FLIP_PIM = (xu(1541.0), -10.0, 4.0, KILAVUZ[3] - 9.5)                                  # pim merkezi x, z · r · alt ucu y (oluk 10 derin)


def kapak_don(sh, kn, aci, dx=0.0):
    """v14b · soğuk kapak (K1 sol / K2 sağ menteşe) açık konumu: sanal dönme merkezi ön dış köşe, dikey eksen · aci derece (0 = kapalı)"""
    px, pz = K1_PIVOT if kn == "K1" else K2_PIVOT
    return sh.rotate(V(px + dx, 0.0, pz), V(px + dx, 1.0, pz), -aci if kn == "K1" else aci)


def flipper_aci(aci):
    return min(90.0, FLIP_K * aci)


def flipper_don(sh, aci, dx=0.0):
    """v14b · flipper: önce katlanır (FLIP_EKSEN etrafında flipper_aci(α)°, sağ ucu geriye) sonra K1 ile döner"""
    fx, fz = FLIP_EKSEN
    return kapak_don(sh.rotate(V(fx + dx, 0.0, fz), V(fx + dx, 1.0, fz), flipper_aci(aci)), "K1", aci, dx)


def _pim_yolu(adim=0.6):
    """pim merkezinin (x, z, α) yolu: α 0 → pim kılavuzun ön yüzünden tamamen çıkana dek · noktalar arası ≤ adim mm"""
    pim = cq.Vertex.makeVertex(FLIP_PIM[0], 0.0, FLIP_PIM[1]); yol = []; a = 0.0; son = None
    while a <= 12.0:
        v = flipper_don(pim, a).toTuple()
        if son is None or math.hypot(v[0] - son[0], v[2] - son[2]) >= adim:
            yol.append((v[0], v[2], a)); son = v
        if v[2] - FLIP_PIM[2] > KILAVUZ[5] + 0.5:
            yol.append((v[0], v[2], a)); break
        a += 0.005
    return yol


PIM_YOLU = _pim_yolu()
_ol = [sily(x_, z_, FLIP_PIM[2], FLIP_PIM[3] - 0.5, KILAVUZ[3] + 1.0).val() for x_, z_, _a in PIM_YOLU]
while len(_ol) > 1:
    _ol = [_ol[i].fuse(_ol[i + 1]) if i + 1 < len(_ol) else _ol[i] for i in range(0, len(_ol), 2)]
ekle("onyuz_kilavuz_flipper", kut(*KILAVUZ).cut(_ol[0]), "pom", "V",
     not_="v14b · flipper KILAVUZ BLOĞU POM-C 107 × 15 × 64 · rafa 2 × M5 havşa · üstünde kam OLUĞU (pim Ø8 yolu, 10 derin, %d nokta, α 0–%.2f°) · ön yüzü +24 → K1 / K2 fitilleri 1152–1167 bandında buna basar · "
          "oluk ön yüzden K1 fitil halkasının İÇİNDE (dünya x ≈ %.0f) çıkar" % (len(PIM_YOLU), PIM_YOLU[-1][2], PIM_YOLU[-1][0] + DX_DUNYA))
_fp = sily(FLIP_EKSEN[0], FLIP_EKSEN[1], 3.0, FLIP[2] - 1.0, FLIP[3] + 1.0)                   # menteşe pimi deliği (katlanma ekseni)
ekle("onyuz_flipper_govde", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], -16.0, Z_CER[1] - 1.5).cut(_fp), "plastik", "V",
     not_="v14b · katlanır orta dikme (flipper) 54 × %.0f × 38,5 · ABS gövde + PU + ısıtıcı kablo (ter önleme, VARSAYIM 10 W/m) · katlanma ekseni dünya x 1493 · z +20 · K1 %.0f° açılınca tam katlanır (−90°) · kıyma haznesinin çekme yolu açık kalır"
          % (FLIP[3] - FLIP[2], 90.0 / FLIP_K))
ekle("onyuz_flipper_on_sac", kut(FLIP[0], FLIP[1], FLIP[2], FLIP[3], Z_CER[1] - 1.5, Z_CER[1]).cut(_fp), "sac", "V", not_="v14 · 430 ferritik 1,5 · manyetik fitil tutar · ön yüzü +24 (çerçeveyle aynı)")
ekle("onyuz_flipper_pimi", sily(FLIP_PIM[0], FLIP_PIM[1], FLIP_PIM[2], FLIP_PIM[3], FLIP[2]), "celik", "K",
     not_="v14b · kam pimi Ø8 × 10 AISI 316 (flipper altına vidalı) · kılavuz oluğunda kayar")
for _i, _y0 in enumerate((1360.0, 1640.0)):
    ekle("onyuz_K1_flipper_mentese_%d" % _i, kut(xu(1481.0), FLIP_EKSEN[0], _y0, _y0 + 20.0, FLIP_EKSEN[1] + 1.0, Z_SKAPAK[0]).union(sily(FLIP_EKSEN[0], FLIP_EKSEN[1], 3.0, _y0 - 5.0, _y0 + 25.0)), "paslanmaz", "K",
         not_="v14b · flipper menteşesi (K1 ile döner): K1 iç sacına braket 12 × 20 × 18 + pim Ø6 (katlanma ekseni) + BURULMA YAYI (katlar, −90° dayamalı — parça no VARSAYIM) · braket K1 fitilinin solunda (dünya x ≤ 1493)")

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
    k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v8"
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
kontrol("kaşar sağ kılavuzu–sucuk mandalı boşluğu %.1f ≥ 10 · kaşar plakası–sucuk plakası %.0f ≥ 30" % (bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax, bb("sucuk_cad_v8__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax),
        bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax >= 10.0 and bb("sucuk_cad_v8__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax >= 30.0)
kontrol("sucuk sağ kılavuzu–sağ duvar boşluğu %.1f ≥ 20" % (BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax), BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax >= 20.0)
kontrol("kuşbaşı valf topuzu–kaşar mandalı boşluğu %.0f ≥ 20" % (bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax), bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax >= 20.0)
kontrol("v14 · eski ön fitil (z −104) kalktı", not [p for p in P if p["ad"] == "on_fitil"])
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]
kontrol("kabin yan PU duvarları 1277'den başlıyor (mekanizma bölgesi serbest)", all(p["sh"].BoundingBox().ymin >= 1276.99 for p in _sd))
_ust = bb("yalitim_blogu")
for p in _sd:
    b_ = p["sh"].BoundingBox()
    _yn = "sol" if "sol" in p["ad"] else "sag"
    _bs = cq.Compound.makeCompound([q["sh"] for q in P if q["ad"] in ("soguk_duvar_%s_ic_sac" % _yn, p["ad"], "soguk_duvar_%s_dis_sac" % _yn)]).BoundingBox()
    kontrol("v14 · %s duvarı sandviç 1,0 + %.1f + 1,5 = %.1f (üst %.1f) · ön yüz z %.0f = üst ön yüz %.0f · arka z %.0f = üst arka %.0f · iç yüz soğuk oda sınırında"
            % (_yn, b_.xlen, _bs.xlen, YAN_T, _bs.zmax, _ust.zmax, _bs.zmin, _ust.zmin),
            abs(_bs.xlen - 60.0) < 0.01 and abs(b_.xlen - 57.5) < 0.01 and abs(_bs.zmax - _ust.zmax) < 0.01 and abs(_bs.zmin - _ust.zmin) < 0.01 and (abs(_bs.xmax - BAY_A[0]) < 0.01 or abs(_bs.xmin - BAY_B[1]) < 0.01))
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

_ay = bb("alt_yalitim_PU"); _as = bb("alt_yalitim_saci")
kontrol("v12 · soğuk oda ALTI yalıtımlı: alt sac y %.0f–%.0f + PU y %.0f–%.0f (39) · x %.0f–%.0f · z %.0f…%.0f · %d geçiş deliği"
        % (_as.ymin, _as.ymax, _ay.ymin, _ay.ymax, _ay.xmin, _ay.xmax, _ay.zmin, _ay.zmax, len(ALT_DELIK)),
        abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and abs(_ay.xmin - BAY_A[0] - 3.0) < 0.01 and abs(_ay.xmax - BAY_B[1] + 3.0) < 0.01)   # v14: iki uçta raf köşebendinin dik kolu (3)
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    print("     alt yalıtım deliği: %-34s x %.0f–%.0f · z %.0f…%.0f (%.0f × %.0f)" % (_ad, x0_, x1_, z0_, z1_, x1_ - x0_, z1_ - z0_))
for _ad, x0_, x1_, z0_, z1_ in ALT_YARIK:
    print("     alt yalıtım ÜST YARIĞI (v14b, y %.0f–%.0f, öne açık, yarık diliyle dolu): %-16s x %.0f–%.0f · z %.0f…%.0f" % (KAS_YARIK_Y0, ALT_YAL[3], _ad, x0_, x1_, z0_, z1_))
_ya = (sum((x1_ - x0_) * (z1_ - z0_) for _a, x0_, x1_, z0_, z1_ in ALT_DELIK) + sum((x1_ - x0_) * (z1_ - z0_) * (ALT_YAL[3] - KAS_YARIK_Y0) / (ALT_YAL[3] - ALT_YAL[2])
       for _a, x0_, x1_, z0_, z1_ in ALT_YARIK)) / ((BAY_B[1] - BAY_A[0]) * (ALT_YAL[5] - ALT_YAL[4]))
kontrol("v12 · alt yalıtımın delik payı (üst üste binenler dahil kaba) %%%.0f ≤ %%25" % (100 * _ya), _ya <= 0.25)
_ka = 0
for _yn in ("alt_yalitim_PU", "alt_yalitim_saci"):
    _ys = [q for q in P if q["ad"] == _yn][0]["sh"]
    for p in P:
        if p["ad"] in ("alt_yalitim_PU", "alt_yalitim_saci") or p["ad"].startswith(("baglam", "kompresor", "hava_ana")): continue
        try:
            if p["sh"].intersect(_ys).Volume() > 1.0: _ka += 1; print("   alt yalıtıma giren:", p["ad"])
        except Exception: pass
kontrol("v12 · alt yalıtıma hiçbir parça girmiyor", _ka == 0, "%d" % _ka)

# ---------------------------------------------------------------- v14 · ön düzlem + yük yolu + havada kalanlar (TU tek başına ölçülebilenler; dünya denetimi topping_cad_v25'te)
from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
def _mes(a, b):
    sa = [p for p in P if p["ad"] == a][0]["sh"]; sb = [p for p in P if p["ad"] == b][0]["sh"]
    d_ = _DSS(sa.wrapped, sb.wrapped); return d_.Value() if d_.IsDone() else 99.0
kontrol("v14 · soğuk zarf ön yüzü +%.0f: yalıtım bloğu %.1f · raf %.1f · teknik ayırma sacları %.1f / %.1f · yan duvarlar %.1f / %.1f"
        % (Z_ZARF, bb("yalitim_blogu").zmax, bb("tasiyici_raf_3mm").zmax, bb("teknik_ayirma_saci_yatay").zmax, bb("teknik_ayirma_saci_dikey").zmax, bb("soguk_duvar_sol_dis_sac").zmax, bb("soguk_duvar_sag_dis_sac").zmax),
        all(abs(bb(a_).zmax - Z_ZARF) < 0.01 for a_ in ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "teknik_ayirma_saci_yatay", "teknik_ayirma_saci_dikey", "kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "soguk_duvar_sol_dis_sac", "soguk_duvar_sag_dis_sac", "soguk_duvar_sol_ic_sac", "soguk_duvar_sag_ic_sac")))
_cb_ = bb("onyuz_soguk_cerceve_saci")
kontrol("v14 · 430 çerçeve sacı z %.1f…%.1f (+23…+24) · dünya x %.1f–%.1f · y %.1f–%.1f" % (_cb_.zmin, _cb_.zmax, _cb_.xmin + DX_DUNYA, _cb_.xmax + DX_DUNYA, _cb_.ymin + DY_DUNYA, _cb_.ymax + DY_DUNYA),
        abs(_cb_.zmin - Z_CER[0]) < 0.01 and abs(_cb_.zmax - Z_CER[1]) < 0.01 and abs(_cb_.xmin + DX_DUNYA - 701.5) < 0.01 and abs(_cb_.xmax + DX_DUNYA - 2498.5) < 0.01)
for _kn, _k in SKAPAK.items():
    _b = bb("onyuz_%s_dis_sac" % _kn)
    kontrol("v14 · %s dünya x %.1f–%.1f · y %.1f–%.1f · z %.1f…%.1f (ön yüz +79, 40 sandviç)" % (_kn, _b.xmin + DX_DUNYA, _b.xmax + DX_DUNYA, _b.ymin + DY_DUNYA, _b.ymax + DY_DUNYA, _b.zmin, _b.zmax),
            abs(_b.zmax - Z_ON) < 0.01 and abs(_b.zmin - Z_SKAPAK[0]) < 0.01 and abs(_b.xmin - _k["x"][0]) < 0.01 and abs(_b.xmax - _k["x"][1]) < 0.01 and abs(_b.ymin - _k["y"][0]) < 0.01 and abs(_b.ymax - _k["y"][1]) < 0.01)
    _f = bb("onyuz_%s_fitil" % _kn)
    kontrol("v14 · %s fitili z %.1f…%.1f (bası yüzü +24 = çerçeve ön yüzü) · kapağın içinde (x %.1f–%.1f ⊂ %.1f–%.1f)" % (_kn, _f.zmin, _f.zmax, _f.xmin, _f.xmax, _k["x"][0], _k["x"][1]),
            abs(_f.zmin - Z_CER[1]) < 0.01 and _f.xmin >= _k["x"][0] + 1.0 and _f.xmax <= _k["x"][1] - 1.0 and _f.ymin >= _k["y"][0] + 1.0 and _f.ymax <= _k["y"][1] - 1.0)
    _fs = [p for p in P if p["ad"] == "onyuz_%s_fitil" % _kn][0]["sh"]
    _vc = sum(_fs.intersect(kut(c0, c1, CENTIK_Y0, SOGUK_TABAN, Z_CER[1], Z_SKAPAK[0]).val()).Volume() for c0, c1 in CENTIK)
    kontrol("v14 · %s fitili kaset çentiklerinin ALTINDA (çentik bölgesinde fitil hacmi %.1f = 0 → conta sürekli)" % (_kn, _vc), _vc < 0.01)
kontrol("v14 · derz K1 | K2 = %.1f (3)" % (SKAPAK["K2"]["x"][0] - SKAPAK["K1"]["x"][1]), abs(SKAPAK["K2"]["x"][0] - SKAPAK["K1"]["x"][1] - 3.0) < 0.01)
_fb = bb("onyuz_flipper_on_sac")
kontrol("v14 · flipper ön yüzü +%.1f = çerçeve ön yüzü · açıklıkta (y %.1f–%.1f ⊂ %.0f–%.0f) · K1 | K2 derzinin arkasında (dünya x %.0f–%.0f)" % (_fb.zmax, _fb.ymin, _fb.ymax, SOGUK_TABAN, TAVAN_B, _fb.xmin + DX_DUNYA, _fb.xmax + DX_DUNYA),
        abs(_fb.zmax - Z_CER[1]) < 0.01 and _fb.ymin > SOGUK_TABAN and _fb.ymax < TAVAN_B and _fb.xmin + DX_DUNYA < 1518.5 and _fb.xmax + DX_DUNYA > 1521.5)
for _a, _b_ in (("onyuz_K1_fitil", "onyuz_flipper_on_sac"), ("onyuz_K2_fitil", "onyuz_flipper_on_sac"), ("onyuz_K1_fitil", "onyuz_soguk_cerceve_saci"), ("onyuz_K2_fitil", "onyuz_soguk_cerceve_saci"),
                ("onyuz_K1_fitil", "onyuz_K1_ic_sac"), ("onyuz_K2_fitil", "onyuz_K2_ic_sac"), ("onyuz_K1_flipper_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_K1_flipper_mentese_0", "onyuz_flipper_govde"), ("onyuz_flipper_pimi", "onyuz_flipper_govde"), ("onyuz_flipper_pimi", "onyuz_kilavuz_flipper"),
                ("onyuz_kilavuz_flipper", "tasiyici_raf_3mm"), ("onyuz_K1_mentese_0", "onyuz_K1_ic_sac"), ("onyuz_K1_mentese_0", "onyuz_mentese_tabani_K1_mentese_0"),
                ("onyuz_K2_mentese_1", "onyuz_K2_ic_sac"), ("onyuz_K2_mentese_1", "onyuz_mentese_tabani_K2_mentese_1"), ("kasar_cad_v14_yarik_dili", "kasar_cad_v14__cikis_tupu"),
                ("sucuk_cad_v8_yarik_dili", "sucuk_cad_v8__cikis_tupu"), ("raf_kaset_contasi_kasar", "tasiyici_raf_3mm"), ("raf_kaset_contasi_sucuk", "sucuk_cad_v8__cikis_tupu"),
                ("raf_gecis_contasi_kiyma", "kiyma__agiz_90_derece"), ("raf_gecis_contasi_sos", "tasiyici_raf_3mm"), ("raf_gecis_contasi_harc_hortum", "harc_spreader_hava_hortumu"),
                ("motor_kablosu_sucuk_cad_v8_rotor", "motor_sucuk_cad_v8_rotor"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_dis_sac"), ("soguk_duvar_sag_alt_profili", "soguk_duvar_sag_z_profili_0"),
                ("raf_kosebendi_sol", "tasiyici_raf_3mm"), ("raf_kosebendi_sag", "tasiyici_raf_3mm"), ("raf_kosebendi_sol", "soguk_duvar_sol_ic_sac"), ("raf_kosebendi_sag", "soguk_duvar_sag_ic_sac"),
                ("soguk_duvar_sol_z_profili_0", "soguk_duvar_sol_dis_sac"), ("soguk_duvar_sag_z_profili_0", "soguk_duvar_sag_dis_sac"),
                ("kasar_boru_kulagi_sag", "kasar_inis_borusu"), ("kasar_boru_kulagi_sag", "tasiyici_raf_3mm"), ("sucuk_boru_kulagi_sol", "sucuk_inis_borusu"), ("sucuk_boru_kulagi_sol", "tasiyici_raf_3mm"),
                ("reduktor_flans_burcu_kasar_cad_v14_helezon", "reduktor_kasar_cad_v14_helezon"), ("reduktor_flans_burcu_kasar_cad_v14_helezon", "kovan_kasar_cad_v14_helezon"),
                ("motor_kasar_cad_v14_helezon", "reduktor_kasar_cad_v14_helezon"), ("kovan_kasar_cad_v14_helezon", "yalitim_blogu"), ("kiyma_mil_gecis_kovani", "yalitim_blogu"),
                ("kiyma_tc_kelepce_hazne", "kiyma_hazne_boynu"), ("kiyma__urun_silindiri_D70", "kiyma__urun_silindiri_kapagi"), ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_tc_kelepcesi"),
                ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_borusu"), ("kiyma__cikis_tc_ferrule_valf", "kiyma__cikis_tc_ferrule"), ("kiyma_agiz_uzatmasi", "kiyma__agiz_90_derece"),
                ("yuva_kasar_mandal_pimi", "yuva_kasar_mandal_govdesi"), ("gecis_blogu_yalitim", "yalitim_blogu"), ("kompresor_cikis_vanasi", "kompresor_JUNAIR_OF302_15B_motor")):
    _d = _mes(_a, _b_)
    if _b_ in ("onyuz_K1_ic_sac", "onyuz_K2_ic_sac"):                                                  # v15: kapak gövdesi = iç panel + dış sacın arka dönüşü
        _d = min(_d, _mes(_a, _b_.replace("_ic_sac", "_dis_sac")))
    kontrol("v14 · temas %s ↔ %s: %.3f mm (≤ 0,05)" % (_a, _b_, _d), _d <= 0.05)
_hv = [p for p in P if "hortum" in p["ad"] and p["mal"].startswith("hortum")]
_hk = []
for _i, _p in enumerate(_hv):
    for _q in _hv[_i + 1:]:
        _A, _B = _p["sh"].BoundingBox(), _q["sh"].BoundingBox()
        if _A.xmax < _B.xmin or _B.xmax < _A.xmin or _A.ymax < _B.ymin or _B.ymax < _A.ymin or _A.zmax < _B.zmin or _B.zmax < _A.zmin: continue
        try: _v = _p["sh"].intersect(_q["sh"]).Volume()
        except Exception: _v = -1.0
        if _v > 1.0 or _v < 0: _hk.append((_p["ad"], _q["ad"], round(_v, 1)))
kontrol("v14 · hortumlar birbirine girmiyor (%d hortum · v13'te 60+ üst üste binme)" % len(_hv), not _hk, str(_hk[:4]))
_gb = [p for p in P if p["ad"] == "gecis_blogu_yalitim"][0]["sh"]
_gk_ = [p["ad"] for p in P if p["ad"] in HORTUM_GECIS and _gb.intersect(p["sh"]).Volume() > 1.0]
kontrol("v14 · geçiş bloğunda hortum delikleri (%d hortum geçer, iç içe 0)" % len(HORTUM_GECIS), not _gk_, str(_gk_))
_ac = [bb("hava_hatti_acici_D6_%d" % j_) for j_ in (1, 2)]
kontrol("v14 · açıcı hattı 2 × Ø6: uçları dünya x %.1f / %.1f = Z silindiri yüzü 372,5 (TC v25) · A tarafında" % (_ac[0].xmin + DX_DUNYA, _ac[1].xmin + DX_DUNYA),
        all(abs(b_.xmin + DX_DUNYA - 372.5) < 0.01 for b_ in _ac))
_vn = bb("kompresor_cikis_vanasi")
kontrol("v14 · kompresör vanası motorun arka yüzünde (z %.0f…%.0f) · montajdaki ucu dünya (%.0f, %.0f, %.0f) = ana hat başı (3790, 1809, −380)"
        % (_vn.zmin, _vn.zmax, 3600 + DX_DUNYA - 510.0, (_vn.ymin + _vn.ymax) / 2.0 + DY_DUNYA + 976.0, _vn.zmin),
        abs(_vn.zmax - (KOMP[5] + 60.0)) < 0.01 and abs((_vn.ymin + _vn.ymax) / 2.0 + DY_DUNYA + 976.0 - 1809.0) < 0.01 and abs(_vn.zmin + 380.0) < 0.01)

# ---------------------------------------------------------------- v14b · denetim_C düzeltmeleri (TU tek başına; dünya karşılıkları topping_cad_v25.dunya_denetimi)
_TUP = [(p["ad"], p["sh"]) for p in P]
_ak, _akl = soguk_taban_kacagi(_TUP)
kontrol("v14b · SOĞUK ODA TABANI (raf dilimi y 1317,5–1319,5): %d ürün kanalı dışında AÇIK alan %.2f mm² ≤ 1 (v14: ≈ 21 350 — kaset U-yarıkları 2 × ≈9 900 + UNO ağız halkaları 4 × 360 + hortum delikleri 2 × 50)"
        % (len(KANAL), _ak), _ak <= 1.0, str([(round(a_, 2), round(b_.xmin), round(b_.zmin)) for a_, b_ in _akl if a_ > 0.01][:6]))
_ab2, _abl = cerceve_bandi_acik(_TUP)
kontrol("v14b · 430 çerçeve düzlemi soğuk oda altı bandında (y 1277–1320) kesintisiz: kaset çentikleri yarık dili flanşıyla kapalı · açık alan %.2f mm² ≤ 1" % _ab2, _ab2 <= 1.0,
        str([(round(a_, 2), round(b_.xmin), round(b_.ymin)) for a_, b_ in _abl if a_ > 0.01][:6]))
for _ad, _mod, _x0, _x1 in KASET:
    _db = bb("%s_yarik_dili" % _mod); _k = _mod.split("_")[0]
    kontrol("v14b · %s yarık dili: x %.0f–%.0f · y %.0f–%.0f (raf üstü = raf üstü %.0f) · z %.0f…%.0f (ön flanş çerçeve düzleminde)" % (_k, _db.xmin, _db.xmax, _db.ymin, _db.ymax, SOGUK_TABAN, _db.zmin, _db.zmax),
            abs(_db.ymax - SOGUK_TABAN) < 0.01 and abs(_db.zmax - Z_CER[1]) < 0.01 and abs(_db.ymin - KAS_YARIK_Y0) < 0.01)
ACI_TARAMA = (0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 20.0, 45.0, 90.0, 110.0)


def kapak_tarama(parcalar, kn, dx=0.0, acilar=ACI_TARAMA):
    """v14b · soğuk kapak (K1: flipper katlanarak) açılırken hareketsiz parçalara + (K1) flipper ↔ K1 parçalarına çakışma (> 1 mm³) ·
    parcalar [(ad, şekil)] (dünya adlarında 'TU:' öneki olabilir) · [(açı, hareketli, diğer, hacim)]"""
    yal = lambda a: a.split(":")[-1]
    g_ = ("onyuz_%s_" % kn,) + (("onyuz_flipper",) if kn == "K1" else ())
    har = [(a, s) for a, s in parcalar if yal(a).startswith(g_)]
    sab = [(a, s, s.BoundingBox()) for a, s in parcalar if not yal(a).startswith(g_)]
    bul = []
    for aci in acilar:
        mv = [(a, flipper_don(s, aci, dx) if yal(a).startswith("onyuz_flipper") else kapak_don(s, kn, aci, dx)) for a, s in har]
        for a, m in mv:
            mb = m.BoundingBox()
            for c, sc, bc in sab + ([(c_, m_, m_.BoundingBox()) for c_, m_ in mv if not yal(c_).startswith("onyuz_flipper")] if yal(a).startswith("onyuz_flipper") else []):
                if mb.xmax < bc.xmin or bc.xmax < mb.xmin or mb.ymax < bc.ymin or bc.ymax < mb.ymin or mb.zmax < bc.zmin or bc.zmax < mb.zmin: continue
                try: v = m.intersect(sc).Volume()
                except Exception: v = -1.0
                if v > 1.0 or v < 0: bul.append((aci, a, c, round(v, 1)))
    return bul


for _kn in ("K1", "K2"):
    _kt = kapak_tarama(_TUP, _kn)
    kontrol("v14b · %s AÇILMA TARAMASI (TU parçaları · 0–110°, %d açı · sanal pivot ön dış köşe%s): çakışma %d"
            % (_kn, len(ACI_TARAMA), " · flipper katlanır min(90, %.0f·α), K2 KAPALI" % FLIP_K if _kn == "K1" else " · K1 + flipper KAPALI", len(_kt)), not _kt, str(_kt[:6]))
kontrol("v14b · flipper kam oluğu: pim yolu %d nokta · α 0–%.2f° · tam katlanma (α %.1f°) oluğun İÇİNDE → kapanırken pim oluğa −90°'de aynı yerden girer · çıkış dünya x %.1f + r 4 < 1493 (K1 fitil halkasının içi)"
        % (len(PIM_YOLU), PIM_YOLU[-1][2], 90.0 / FLIP_K, PIM_YOLU[-1][0] + DX_DUNYA), PIM_YOLU[-1][2] >= 90.0 / FLIP_K and PIM_YOLU[-1][0] + DX_DUNYA + FLIP_PIM[2] < 1493.0)


def den_assert():
    """v14 · montaj TU'yu yükleyince çağırır: modül seviyesindeki bütün denetimler geçmeli"""
    kal = [d for d in DEN if not d[1]]
    assert not kal, "topping_uno_cad_v14 denetimi KALDI: %s" % kal
    return len(DEN)

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
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH topping_uno_cad_v14"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb_)}],
          "animations": [{"name": "emis_basma_2sn", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb_))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb_), b"BIN\x00")); f.write(bb_)
    print("GLB %s · %d KB · %d parça · %d üçgen" % (os.path.basename(yol), (len(bb_) + len(js)) // 1024, len(P), uc))


if __name__ == "__main__":
    # v6 · KASET ÇIKIŞ YOLU: kaset (mandal kalkık) 10 mm adımlarla öne çekilir; hiçbir sabit parçaya değmemeli · v14: 0–630 (ön düzlem +79 geçilir), soğuk kapaklar + flipper AÇIK
    for KOD in YUVA:
        k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v8"
        kas = [p["sh"] for p in P if p["ad"].startswith(mod)]
        sabit = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_mandal_dili" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski", "onyuz_K1_", "onyuz_K2_", "onyuz_flipper"))]
        bul = []
        for dz in range(10, 631, 10):
            kc = cq.Compound.makeCompound([q.translate(V(0, 0, dz)) for q in kas]); kb_ = kc.BoundingBox()
            for p in sabit:
                b_ = p["sh"].BoundingBox()
                if not (kb_.xmin < b_.xmax and b_.xmin < kb_.xmax and kb_.ymin < b_.ymax and b_.ymin < kb_.ymax and kb_.zmin < b_.zmax and b_.zmin < kb_.zmax): continue
                try: v_ = kc.intersect(p["sh"]).Volume()
                except Exception: v_ = -1.0
                if v_ > 1.0 or v_ < 0: bul.append((dz, p["ad"], round(v_, 1)))
        kontrol("v14 · %s kaseti öne çekilirken (0–630 mm, kapak açık) hiçbir sabit parçaya değmiyor (430 çerçeve çentikli)" % KOD, not bul, "%d bulgu %s" % (len(bul), bul[:6]))
    kal = [d for d in DEN if not d[1]]
    assert not kal, kal
    _od = OUT if "--site" in sys.argv else os.path.join(U, "on_duzlem_v63")                  # v14: siteye yazılmaz (montaj ajanı yayınlar)
    glb_yaz(os.path.join(_od, "topping_uno_v15.glb"))
    with open(os.path.join(_od, "topping_uno_v15.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v15 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       grup={g: list(v) for g, v in GRUP.items()},
                       parcalar=[dict(ad=p["ad"], kaynak=p["kaynak"], not_=p["not_"], mal=p["mal"]) for p in P],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN]), f, ensure_ascii=False, indent=1)
    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))
    sys.stdout.flush(); os._exit(0)
