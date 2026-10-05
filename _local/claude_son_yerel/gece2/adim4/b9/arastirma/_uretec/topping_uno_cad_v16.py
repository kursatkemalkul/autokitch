# -*- coding: utf-8 -*-
"""TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v16 · 29 Eyl 2026 · YEREL (v15 + SOĞUK KUTU KÖPÜK DOLGULU SANDVİÇ, HER YÜZ 60 · EVAPORATÖR İÇERİDE · yap_topping_uno_cad_v16.py)
v16: yan dış kabuk = TC yan sacı (boşluk / Z profil yok) · iç kaplama tek parça · L + B tavanı + arka 60 · taban 43 (UNO ağzı sınırı) · yayıcı kesme valfi tabanın altında ·
    B tavanı 1686 · teknik taban 1746 · raf askısı GFRP burç · evaporatör A tavanında (SOS üstü) + hat bloğu + yoğuşma kabı · menteşe kolları 12,5
v15: topping_uno_cad_v15 · 28 Eyl 2026 akşam (v14 + KAPAK İÇ SACI TEK PARÇA · sucuk_cad_v8 · Codex STEP kırıntıları atılır · yap_topping_uno_cad_v15.py)
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
# v16 · SOĞUK KUTU = KÖPÜK DOLGULU SANDVİÇ (Kemal 29 Eyl: "yap herşeyi düzgün yap temiz olsun"): her yüz 60 = iç 304 1,0 + PU 57,5 + dış 304 1,5 · yan / üst dış kabuk = TC'nin kendi sacı
T_IC, T_PU, T_DIS = 1.0, 57.5, 1.5; T_DUV = T_IC + T_PU + T_DIS                        # 60
X_SAC = (1.5, W - 1.5)                                                                  # TC yan saclarının iç yüzü (dünya 701,5 / 2498,5)
Y_UST_SAC = YUST - 1.5                                                                  # TC tavan sacının alt yüzü 2028,5
BAY_A = (X_SAC[0] + T_PU + T_IC, 790.0); BAY_B = (790.0, X_SAC[1] - T_PU - T_IC)       # v16: 60 / 1740 (v15 90 / 1710: 28,5 Z profil boşluğu + ayrı dış sac kalktı → soğuk oda 60 geniş)
TAVAN_A = Y_UST_SAC - T_PU - T_IC                                                       # v16: 1970 (v15 1968: A tavanı 60,5)
TAVAN_B = 1686.0                                                                        # v16: kaset üstü 1672 + 14 · kıyma / kuşbaşı haznesi (1667) dolumda 15 kalkar → 1682 (v15 1690)
SAC_T = T_DIS; PU_L = T_DUV                                                             # v16: L (soğuk ↔ teknik) 30 → 60
Y_TEK = TAVAN_B + T_DUV; X_TEK = BAY_A[1] + T_DUV                                      # v16: teknik cep tabanı 1746 (dünya 1578) · sol duvarı 850 (dünya 1550)
TEK_Y0 = Y_TEK + 6.0                                                                    # v16: teknik cihazlar 6 mm titreşim pedinde (topping_cad_v29)
Z_ON = 79.0                                                                        # v14 · ÖN DÜZLEM (fırın ön yüzü) · montaj sözleşmesi Z_ON = FT.ZS = 79
Z_ZARF = 23.0                                                                      # v14 · soğuk zarfın ön yüzü (v13 −104): önünde 430 çerçeve +23…+24 · fitil +24…+39 · kapak +39…+79
Z_CER = (Z_ZARF, Z_ZARF + 1.0); Z_SKAPAK = (Z_ON - 40.0, Z_ON)                  # v14 · 430 ferritik çerçeve sacı 1,0 · soğuk kapak 40 = dış 1,5 + PU 37,5 + iç 1,0
Z_KAPAK = (-84.0, Z_ZARF); Z_SOGUK = (Z_ZARF, -570.0); Z_BOLME = (-570.0, -630.0); Z_KURU = (-630.0, -830.0)   # v16: arka duvar 60 (iç sac −570…−571 · PU · dış sac −628,5…−630; v15 −565…−630 sacsız 65)   # v14: Z_KAPAK[1] = soğuk zarf ön yüzü (v13 −104)
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
YAN_T = T_DUV                                                                           # v16: bütün yüzler 60 (v13–v15: A tavanı 60,5 · yan 60 · L 30 · arka 65 · taban 40)
DUVAR = (T_IC, T_PU, T_DIS)                                                             # v16: iç 304 1,0 + PU 57,5 (40 kg/m³) + dış 304 1,5 · yan / üst dış kabuğu = TC sacı
# v16: yan duvar sandviçi bölüm 1b'de (SOĞUK KUTU) — v15'teki ayrı dış sac + 28,5 Z profil boşluğu + Z profiller KALKTI
ekle("kabin_sag_teknik_sac", kut(W - 1.5, W, Y_TEK, YUST, 0, -D), "kabuk", "V", not_="v11: teknik cebin sağ yan saçı · havalandırma ızgaralı (kondenser havası)")
RAF_T, RAF_BUKUM = 3.0, 38.5                                                            # v16: bükümler alt dış sacın (1277–1278,5) üstünde biter
_raf = kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T, SOGUK_TABAN, Z_KAPAK[1], Z_BOLME[0])   # v16: 60–1740
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
_rob = kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_KAPAK[1] - RAF_T, Z_KAPAK[1])
for _ad, _mod, _x0, _x1 in KASET:                                                       # v6: kaset çıkış tüpü öne kayarken raftan sıyrılsın: U-yarık + çentik
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    _raf = _raf.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1, KAS_Z, Z_KAPAK[1] + 1))
    _rob = _rob.cut(kut(_xc - _r, _xc + _r, KAS_YARIK_Y0, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))   # v14b: çentik yalnız üst 6 mm, altındaki 34 mm kiriş sürekli
ekle("tasiyici_raf_3mm", _raf, "paslanmaz", "H", not_="AISI 304 · 3 mm + 2 × 38,5 büküm · v16: açıklık 1680 (v15 1620) · yük 154 kg → sehim 4,1 mm (L/410) · 101 MPa · emniyet 2,1 (bükümler + alt sandviç hesaba katılmadan) · ağız delikleri · v6: kaset delikleri öne açık U-yarık (Ø60)")
ekle("raf_on_bukumu", _rob, "paslanmaz", "H", not_="38,5 mm aşağı büküm (rafın kirişi · v16: alt dış sacın üstünde biter) · v6: kaset yarıklarında 60 çentik · v14b: çentik yalnız 1311–1317 (tüp + yarık dili geçer), altındaki 34 mm kiriş sürekli")
for _ad, _mod, _x0, _x1 in KASET:
    _x = (_x0 + _x1) / 2.0; _, ro, ri = KAS_R[_mod]
    HUNI_Y = (1305.0, 1311.0)                                                                          # v6: boru üstü 1305 · huni 1305–1311 · kaset borusunun altı 1312 → 1 mm, iç içe DEĞİL
    ekle("%s_inis_borusu" % _mod.split("_")[0], sily(_x, KAS_Z, ro, 1216.0, HUNI_Y[0]).cut(sily(_x, KAS_Z, ri, 1215.0, HUNI_Y[0] + 1.0)), "paslanmaz", "H",
         not_="kaset borusunun devamı: üstü 1305 — kaset borusu (dış Ø%.0f) 1312'de biter, iç içe geçmez (v5'te 5 mm geçiyordu, kaset öne çekilemezdi) · pideye 40 mm kalana iner" % (2 * ro))
    _hn = cq.Solid.makeCone(ro, 32.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))
    _hn = _hn.cut(cq.Solid.makeCone(ri, 29.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))).cut(sily(_x, KAS_Z, ri, HUNI_Y[0] - 1.0, HUNI_Y[0] + 0.5).val())
    ekle("%s_inis_hunisi" % _mod.split("_")[0], _hn, "paslanmaz", "H",
         not_="huni iç Ø%.0f→Ø58 · 1305–1311 · kaset borusunun altındaki 1 mm boşluğu ve 4 mm yanal payı örter → kaset öne çekilirken boruya takılmaz" % (2 * ri))
ekle("raf_arka_bukumu", kut(BAY_A[0], BAY_B[1], SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_BOLME[0], Z_BOLME[0] + RAF_T), "paslanmaz", "H")
# v14 · İNİŞ BORULARI RAFA ASILI: borunun iki yanında 3 mm kulak (boruya kaynak) + dik lama rafın altına M5 · kulaklar tüpün kayma izinin (±30) dışında (±35…38)
for _ad, _mod, _x0, _x1 in KASET:
    _x = (_x0 + _x1) / 2.0; _, ro, ri = KAS_R[_mod]
    for _sg, _yn in ((-1.0, "sol"), (1.0, "sag")):
        _k = kut(_x + _sg * ro, _x + _sg * 38.0, 1250.0, 1256.0, KAS_Z - 10.0, KAS_Z + 10.0).union(kut(_x + _sg * 35.0, _x + _sg * 38.0, 1256.0, SOGUK_TABAN - RAF_T, KAS_Z - 10.0, KAS_Z + 10.0))
        ekle("%s_boru_kulagi_%s" % (_mod.split("_")[0], _yn), _k, "paslanmaz", "H",
             not_="v14 · 304 lama 3 × 20 · boruya kaynak (yatay kol) + rafın altına 2 × M5 (dik kol 35–38) · iniş borusu + huni v13'te havadaydı")
YAL_Y0 = SOGUK_TABAN - 43                                                             # 1277 · soğuk oda tabanının altı (v16: alt sac 1,5 + PU 38,5 + raf 3 = 43)
Y_ALT1 = YAL_Y0 + T_DIS                                                               # v16: 1278,5 · alt dış sacın üstü (yan / arka duvarlar, raf bükümleri, köşebentler buradan)
CEP_TEKNIK = (X_TEK, W, Y_TEK, YUST, Z_KAPAK[1], -D)                                # v16: 850–1800 × 1746–2030 · yalıtımın dışında · arkası açık
# ================================================================ 1b · v16 · SOĞUK KUTU (köpük dolgulu sandviç · Kemal 29 Eyl: "yap herşeyi düzgün yap temiz olsun")
#   iç kaplama 304 1,0 TEK PARÇA (yanlar + arka + A tavanı + L + B tavanı; köşeler kaynaklı-taşlanmış) · PU 57,5 yerinde köpük · dış kabuk 1,5:
#   yanlar = TC yan sacları · A tavanı = TC tavan sacı · arka + taban + teknik taban + L dış yüzü = kutunun kendi sacları
#   (v15: yanlarda ayrı dış sac + 28,5 Z profil boşluğu · L 30 · arka 65 sacsız · tavan / arka / L'de iç kaplama yoktu)
def _kutu2(a, b, z0, z1):
    """iki kutunun birleşimi: a, b = (x0, x1, y0, y1) · z0…z1"""
    return kut(a[0], a[1], a[2], a[3], z0, z1).union(kut(b[0], b[1], b[2], b[3], z0, z1))


ODA = ((BAY_A[0], BAY_A[1], Y_ALT1 - 1.0, TAVAN_A), (BAY_A[0], BAY_B[1], Y_ALT1 - 1.0, TAVAN_B))                        # soğuk oda (kaplama tabana kadar iner)
ODA_K = ((BAY_A[0] - T_IC, BAY_A[1] + T_IC, Y_ALT1, TAVAN_A + T_IC), (BAY_A[0] - T_IC, BAY_B[1] + T_IC, Y_ALT1, TAVAN_B + T_IC))   # kaplamanın dış yüzü
ZARF_K = ((X_SAC[0], X_SAC[1], Y_ALT1, Y_TEK - T_DIS), (X_SAC[0], X_TEK - T_DIS, Y_TEK - T_DIS, Y_UST_SAC))                   # dış kabukların iç yüzü
_odak = _kutu2(*ODA_K, Z_SOGUK[1] - T_IC, Z_ZARF)
KUTU = {"soguk_ic_kaplama": _odak.cut(_kutu2(*ODA, Z_SOGUK[1], Z_ZARF + 1.0))}
_pu = _kutu2(*ZARF_K, Z_BOLME[1] + T_DIS, Z_ZARF).cut(_odak)
_psol = _pu.intersect(kut(X_SAC[0], BAY_A[0] - T_IC, Y_ALT1, TAVAN_A + T_IC, Z_SOGUK[1] - T_IC, Z_ZARF))
_psag = _pu.intersect(kut(BAY_B[1] + T_IC, X_SAC[1], Y_ALT1, Y_TEK - T_DIS, Z_SOGUK[1] - T_IC, Z_ZARF))
KUTU["kabin_sol_duvar_PU"] = _psol
KUTU["kabin_sag_duvar_PU"] = _psag
KUTU["yalitim_blogu"] = _pu.cut(_psol).cut(_psag)                                     # arka + A tavanı + L dikey + B tavanı (tek köpük)
KUTU["soguk_arka_dis_sac"] = cq.Workplane("XY", origin=(0, 0, Z_BOLME[1])).polyline([(X_SAC[0], YAL_Y0), (X_SAC[1], YAL_Y0), (X_SAC[1], Y_TEK), (X_TEK, Y_TEK),
                                                                                    (X_TEK, Y_UST_SAC), (X_SAC[0], Y_UST_SAC)]).close().extrude(T_DIS)
KUTU["teknik_ayirma_saci_yatay"] = kut(X_TEK - T_DIS, X_SAC[1], Y_TEK - T_DIS, Y_TEK, Z_BOLME[1] + T_DIS, Z_ZARF)      # B tavanının dış sacı = teknik cep tabanı
KUTU["teknik_ayirma_saci_dikey"] = kut(X_TEK - T_DIS, X_TEK, Y_TEK, Y_UST_SAC, Z_BOLME[1] + T_DIS, Z_ZARF)            # L dikeyin dış sacı = teknik cebin sol yüzü
KUTU["alt_yalitim_saci"] = kut(X_SAC[0], X_SAC[1], YAL_Y0, Y_ALT1, Z_BOLME[1] + T_DIS, Z_ZARF)                         # geçiş delikleri bölüm v12'de (ALT_DELIK)
ARKA3 = ("soguk_ic_kaplama", "yalitim_blogu", "soguk_arka_dis_sac")                   # arka duvarın katmanları


def kutu_delik(sh, adlar):
    """v16 · soğuk kutu parçalarından bir geçiş deliği çıkarır"""
    for k_ in adlar:
        KUTU[k_] = KUTU[k_].cut(sh)


kutu_delik(kut(90, 1200, 1440, 1470, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)          # geçiş bloğu yuvası (blok ölçüsünde → blok yuvaya değer)
for _u in UNO:
    kutu_delik(silz(_u[1], V_EKSEN, 15.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)       # UNO mil geçiş kovanı Ø30 (sıkı geçme)
RAF_BURC_Y = (Y_ALT1 + SOGUK_TABAN - RAF_T - 3.0) / 2.0                              # v16 · raf köşebendi dik kolunun ortası (1296,25)
RAF_BURC_Z = (-520.0, -360.0, -200.0, -40.0)
for _yn, _bx in (("sol", (X_SAC[0], BAY_A[0] - T_IC)), ("sag", (BAY_B[1] + T_IC, X_SAC[1]))):
    for _bz in RAF_BURC_Z:
        kutu_delik(silx(RAF_BURC_Y, _bz, 8.0, _bx[0] - 1.0, _bx[1] + 1.0), ("kabin_%s_duvar_PU" % _yn,))   # GFRP burç yuvası Ø16
YAL_BLOK = [None]                                                                     # (v15 adı · v16'da KUTU sözlüğü)
for ad, x0, x1, h_, z1_ in (("sogutma_grubu", 860, 1167, 272.0, -420.0), ("pano_PLC", 1180, 1580, 240.0, -290.0), ("guc_kaynagi", 1592, 1655, 126.0, -163.0), ("UPS", 1660, 1709, 122.0, -171.0)):
    ekle("teknik_bant_" + ad, kut(x0, x1, TEK_Y0, TEK_Y0 + h_, -40, z1_), "zarf", "Ö", not_="v16 teknik cep (yalıtımın dışında, soğuk kutunun üstünde) · ZARF · gerçek parçalar topping_cad_v29'da")
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
        vx = cx - 40.0; v0, v1 = yb + 20.0, yb + 66.0                                      # v16: kesme valfi 20 aşağı (v15 yb + 40) → kapağı 1274, soğuk oda tabanının (1277) altında · v15'te tabana 17 mm gömülüydü
        vk = (yb + 42.5, BICAK_UST - 0.5)                                                  # v16: braket + kelepçe dik borunun üçgen gövde (1242) ile giriş kelepçesi (1262) arası
        ekle("%s_spreader_kesme_valfi_govde" % k, sily(vx, ZT, 14.0, v0, v1), "pom", "F", not_="havalı kesme valfi (drip-free) · beyaz gövde, görselden")
        ekle("%s_spreader_kesme_valfi_kapak" % k, sily(vx, ZT, 15.0, v1, v1 + 8.0), "pom", "F")
        ekle("%s_spreader_valf_braketi" % k, kut(vx, cx - 18.5, vk[0], vk[1], ZT - 2.0, ZT + 2.0), "paslanmaz", "F")   # v14: UNO ağzına girmez (v13 cx − 16)
        ekle("%s_spreader_valf_kelepcesi" % k, sily(cx, ZT, 21.0, vk[0], vk[1]).cut(sily(cx, ZT, 18.1, vk[0] - 1.0, vk[1] + 1.0)), "paslanmaz", "F")
        ekle("%s_spreader_valf_mili" % k, silx((vk[0] + vk[1]) / 2.0, ZT, 3.0, vx + 14.0, cx - 18.0), "celik", "V")
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
        kutu_delik(silz(xc, yy, 30.0, Z_BOLME[1] - 1, Z_BOLME[0] + 1), ARKA3)                            # v16: kaplama + PU + arka dış sac            # v6: yalıtım bloğunda kovan deliği (v14: Ø60 = kovan, sıkı)
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
# ================================================================ 3c · v16 · SOĞUTMA: EVAPORATÖR KUTUNUN İÇİNDE (v15: TC kuru bölmesinde çıplaktı → +134 W, kuru bölmede yoğuşma · sogutma_topping_v1)
#   standart üstten üniteli dolap düzeni: fanlı ince evaporatör A bölmesinin tavanında, SOS haznesinin üstünde (dolumda hazne 15 kalkar → 1752 < 1762) ·
#   yoğuşma ünitesi (Secop CU KLF4.8CND, topping_cad_v29) teknik cepte · hatlar L duvarındaki POM bloktan · yoğuşma suyu arka duvardan kuru bölmedeki
#   elektrikli buharlaştırma kabına. EVAPORATÖR YAPTIRILACAK (soğutmacı firma): model YER ZARFI 260 × 208 × 500
EVAP = (BAY_A[0] + 6.0, BAY_A[0] + 266.0, 1762.0, TAVAN_A, -560.0, -60.0)           # x 66–326 · y 1762–1970 · z −560…−60
_ex0, _ex1, _ey0, _ey1, _ez0, _ez1 = EVAP
_g = kut(_ex0, _ex1, _ey1 - 1.0, _ey1, _ez0, _ez1)                                    # üst sac (tavan kaplamasına)
_g = _g.union(kut(_ex0, _ex0 + 1.0, _ey0, _ey1, _ez0, _ez1)).union(kut(_ex1 - 1.0, _ex1, _ey0, _ey1, _ez0, _ez1))   # yan saclar
_g = _g.union(kut(_ex0, _ex1, _ey0, _ey1, _ez0, _ez0 + 1.0))                          # arka sac
_g = _g.union(kut(_ex0, _ex1, _ey0, _ey0 + 1.0, -322.0, _ez1))                        # ön-alt sac (fan + üfleme kanalının altı)
ekle("evaporator_govdesi", _g, "paslanmaz", "V",
     not_="v16 · evaporatör gövdesi AISI 304 1,0 · 260 × 208 × 500 · A tavan kaplamasına 4 × M6 perçin somun (köpük içi takviye lama) · emiş arka-alt açıklıktan (z −559…−478) · üfleme ön yüzden tavan boyunca kapıya · YER ZARFI (soğutmacı firma)")
ekle("evaporator_lamel_paketi", kut(_ex0 + 1.0, _ex1 - 1.0, 1790.0, 1965.0, -470.0, -330.0), "aluminyum", "V",
     not_="v16 · lamel paketi (Al kanat / Cu boru) 258 × 175 × 140 · hava z yönünde · 300–380 W @ −10 °C (gereken 231–326 W @ 32 °C · sogutma_topping_v1) · uç plakaları gövde yan saclarına · YER ZARFI")
ekle("evaporator_fani", kut(_ex0 + 55.0, _ex0 + 205.0, 1802.0, 1952.0, -330.0, -280.0), "motor", "V",
     not_="v16 · eksenel fan 150 × 150 × 50 (EC 24 V) · lamel paketinin ön çerçevesine 4 × M4 · paketten çekip tavan boyunca kapıya üfler · model / debi soğutmacı firma")
ekle("evaporator_damlama_tavasi", kut(_ex0 + 1.0, _ex1 - 1.0, 1766.0, 1790.0, -478.0, -322.0).cut(kut(_ex0 + 2.0, _ex1 - 2.0, 1767.0, 1791.0, -477.0, -323.0)), "paslanmaz", "V",
     not_="v16 · damlama tavası 304 1,0 · lamel paketinin altında · %1 eğimle sol-arka köşedeki Ø8 çıkışa")
TAHLIYE = [(90.0, 1766.0, -470.0), (90.0, 1754.0, -470.0), (90.0, 1754.0, -660.0), (90.0, 1745.0, -660.0)]
ekle("evaporator_tahliye_hortumu", boru(TAHLIYE, 4.0), "silikon", "V",
     not_="v16 · yoğuşma tahliyesi Ø8 silikon · tavadan SOS haznesinin solundan (x 86–94 < 100) arka duvara, duvar deliği hortum çapında (silikonla) · kuru bölmedeki buharlaştırma kabına düşer · sifonlu")
kutu_delik(silz(90.0, 1754.0, 4.0, Z_BOLME[1] - 1.0, Z_BOLME[0] + 1.0), ARKA3)
ekle("yogusma_buharlastirma_kabi", kut(60.0, 160.0, 1700.0, 1745.0, -790.0, Z_BOLME[1]).cut(kut(62.0, 158.0, 1702.0, 1746.0, -788.0, Z_BOLME[1] - 2.0)), "paslanmaz", "V",
     not_="v16 · elektrikli yoğuşma buharlaştırma kabı 100 × 45 × 160 (0,6 L · 30 W rezistans + şamandıra, VARSAYIM) · arka duvarın dış sacına 2 × M5 · altında elektrik yok (valf adası x ≥ 150, bobinler y ≤ 1690)")
HAT_GECIS = (BAY_A[1], X_TEK, 1885.0, 1955.0, -425.0, -375.0)                       # L duvarı hat geçişi (kaplama + PU + dış sac)
_hg = kut(*HAT_GECIS)
for _hy, _hr in ((1935.0, 15.5), (1905.0, 3.2)):
    _hg = _hg.cut(silx(_hy, -400.0, _hr, BAY_A[1] - 1.0, X_TEK + 1.0))
kutu_delik(kut(*HAT_GECIS), ("soguk_ic_kaplama", "yalitim_blogu", "teknik_ayirma_saci_dikey"))
ekle("sogutma_hat_gecis_blogu", _hg, "pom", "V", not_="v16 · POM-C hat geçiş bloğu 60 × 70 × 50 · L duvarını boydan geçer · iki hat deliği hat çapında (silikonla sızdırmaz)")
ekle("sogutma_emis_hatti", silx(1935.0, -400.0, 15.5, _ex1, 860.0), "koyu", "V",
     not_="v16 · emiş hattı Cu Ø12,7 + Armaflex 9 mm (dış Ø31) · evaporatörün sağ yüzünden L duvarından teknik cepteki yoğuşma ünitesine (topping_cad_v29, x 860) · HARÇ haznesinin üstünden (1832; dolumda 1847)")
ekle("sogutma_sivi_hatti", silx(1905.0, -400.0, 3.2, _ex1, 860.0), "celik", "V",
     not_="v16 · sıvı hattı Cu Ø6,35 · genleşme valfi / kılcal evaporatör girişinde (soğutmacı firma)")
for _k, _mal, _not in (
        ("soguk_ic_kaplama", "paslanmaz", "v16 · İÇ KAPLAMA AISI 304 1,0 TEK PARÇA: yanlar + arka + A tavanı + L + B tavanı (köşeler kaynaklı-taşlanmış, iç köşe R ≥ 6) · önü açık (430 çerçeve + kapaklar) · tabanı raf · kovan / blok / tahliye delikleri"),
        ("kabin_sol_duvar_PU", "pu", "v16 · sol duvar PU 57,5 (40 kg/m³, yerinde köpük) · dış kabuğu TC sol yan sacı (x 0–1,5) · iç kaplamaya ve sacın iç yüzüne yapışık · v15'teki ayrı dış sac + 28,5 Z profil boşluğu KALKTI · 4 GFRP raf burcu"),
        ("kabin_sag_duvar_PU", "pu", "v16 · sağ duvar PU 57,5 · dış kabuğu TC sağ yan sacı (x 1798,5–1800) · teknik tabana kadar · 4 GFRP raf burcu"),
        ("yalitim_blogu", "pu", "v16 · PU 57,5 TEK KÖPÜK: arka duvar + A tavanı + L dikey + B tavanı (hepsi 60 sandviç; v15: A tavanı 60,5 · L 30 · arka 65 sacsız) · 4 kaset + 4 UNO kovanı + geçiş bloğu + hat bloğu + tahliye delikleri"),
        ("soguk_arka_dis_sac", "paslanmaz", "v16 · arka duvarın dış kabuğu AISI 304 1,5 (kuru bölmeye bakar) · x 1,5–1798,5 · A tarafında TC tavanına, teknik cep tarafında teknik tabana kadar · kovan / blok / tahliye delikleri"),
        ("teknik_ayirma_saci_yatay", "paslanmaz", "v16 · B tavanının dış kabuğu = TEKNİK CEP TABANI AISI 304 1,5 (dünya 1576,5–1578) · cihazlar bunun üstüne titreşim pedleriyle (topping_cad_v29) · B tavanı iki ucundan (L duvarı + sağ duvar) taşınır, konsol yok"),
        ("teknik_ayirma_saci_dikey", "paslanmaz", "v16 · L dikey duvarın dış kabuğu AISI 304 1,5 (teknik cebin sol yüzü, dünya x 1548,5–1550) · T sol dikme köşebentleri buna (topping_cad_v29) · hat bloğu deliği")):
    ekle(_k, KUTU[_k], _mal, "Ö", not_=_not)
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
# v16 · SAĞ DUVAR ALT PROFİLİ KALKTI (aktarma iticisi v70'ten beri yok — bantlı tabla; profil v15'te Z profil boşluğundaydı)


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
    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski", "soguk_", "teknik_ayirma", "evaporator", "sogutma_", "yogusma_")):
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
_asc = KUTU["alt_yalitim_saci"]
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    _asc = _asc.cut(kut(x0_, x1_, YAL_Y0 - 1.0, Y_ALT1 + 1.0, z0_, z1_))
ekle("alt_yalitim_saci", _asc.val(), "paslanmaz", "V",
     not_="v16 · soğuk kutunun ALT DIŞ KABUĞU AISI 304 1,5 TEK PARÇA · x 1,5–1798,5 (yan ve arka duvarların altını da kapatır, v15 1,0 ve yalnız raf altı) · aşağı bakar (pişirme bölgesinin üstü) · geçişlerde 3 mm boşluklu delik")
ekle("alt_yalitim_PU", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], Y_ALT1, ALT_YAL[3], ALT_YAL[4], ALT_YAL[5])).val(), "pu", "V",
     not_="v16 · taban PU 38,5 (40 kg/m³) · rafın altı, bükümlerin ve köşebentlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik · kaset yalnız ÜST 6 mm yarık (öne açık, yarık diliyle dolu) · TABAN 43: UNO ağzı + yayıcı kelepçesi 1274'te — daha kalını kelepçeyi yalıtıma gömer")


# ================================================================ 5b · v14 · YÜK YOLU + ÖN YÜZ (SPEC_on_duzlem_v63 §1 + §2.3)
# (a) RAF KÖŞEBENTLERİ L 40 × 40 × 3 (304): rafın iki ucu bunlara oturur; köşebent duvarın iç sacına M6, bükümlerin arasında (z −562…+20)
RAF_L = {}
for _yn, _x0, _sg in (("sol", BAY_A[0], 1.0), ("sag", BAY_B[1], -1.0)):
    _L = kut(_x0, _x0 + _sg * 40.0, SOGUK_TABAN - RAF_T - 3.0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T)
    _L = _L.union(kut(_x0, _x0 + _sg * 3.0, Y_ALT1, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T))   # v16: alt dış sacın üstünden
    if _yn == "sol":                                                                    # sos spreader hava hortumu raftaki Ø10 delikten geçer → köşebentte de aynı delik
        _L = _L.cut(sily(UNO[0][1] - 100.0, ZT + 34.0, 5.0, SOGUK_TABAN - RAF_T - 4.0, SOGUK_TABAN - RAF_T + 1.0))
    RAF_L[_yn] = _L
    ekle("raf_kosebendi_%s" % _yn, _L, "paslanmaz", "H",
         not_="v16 · L 40 × 40 × 3 AISI 304 · rafın ucu yatay koluna oturur (M5 havşa) · dik kol iç kaplamaya dayalı, 4 × M8 GFRP burçtan TC yan sacına · raf 154 kg → uç başına 0,76 kN")
    _bx = (X_SAC[0], BAY_A[0] - T_IC) if _yn == "sol" else (BAY_B[1] + T_IC, X_SAC[1])
    _bc = None
    for _bz in RAF_BURC_Z:
        _b = silx(RAF_BURC_Y, _bz, 8.0, _bx[0], _bx[1]).cut(silx(RAF_BURC_Y, _bz, 4.5, _bx[0] - 1.0, _bx[1] + 1.0))
        _bc = _b if _bc is None else _bc.union(_b)
    ekle("raf_askisi_burclari_%s" % _yn, _bc, "pom", "H",
         not_="v16 · 4 × ısı köprüsü kesici burç GFRP Ø16/Ø9 × 57,5 (PU'nun içinden) · raf köşebendini TC yan sacına bağlayan M8 A2 cıvata içinden geçer, sacda kör perçin somun · 0,76 kN → cıvata başına 190 N")
for q in P:                                                                            # alt yalıtım köşebendi sarar (tam ölçü kesik)
    if q["ad"] in ("alt_yalitim_PU", "alt_yalitim_saci"):
        for _L in RAF_L.values():
            q["sh"] = q["sh"].cut(_L.val())
# (b) v16: Z PROFİLLER KALKTI — yan duvarın dış kabuğu TC yan sacının kendisi (boşluk yok)
ZPROF = []

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
          "K2": dict(x=(xu(1521.5), xu(2497.0)), y=(yu(1110.5), yu(1575.0)), fitil=(xu(1537.5), BAY_B[1], yu(1136.0), TAVAN_B), mentese="sag")}
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
for _ad, _x0, _x1, _y0, _tx in (("K1_mentese_0", 31.5, 44.0, 1330.0, (1.5, 31.5)), ("K1_mentese_1", 31.5, 44.0, 1900.0, (1.5, 31.5)),        # v16: fitil 60'a geldi (x 45,5–66,5) → kol 31,5–44 (TC yan sacının ön dönüşü 1,5–31,5'in yanında) · taban aynı
                               ("K2_mentese_0", xu(2456.0), xu(2468.5), 1330.0, (xu(2468.5), xu(2498.5))), ("K2_mentese_1", xu(2456.0), xu(2468.5), 1620.0, (xu(2468.5), xu(2498.5)))):
    ekle("onyuz_" + _ad, kut(_x0, _x1, _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0]), "paslanmaz", "K",
         not_="v16 · kol 12,5 geniş (fitil 30 dışa geldi, x 45,5 / 1754,5) · v14b · çok kollu gizli menteşe KOLU (kapak tarafı · 3B ayarlı, Sugatsune HES3D sınıfı — parça no + ölçü + sanal pivot VARSAYIM, föy doğrulanacak) · kapağın iç sacına perçin somun · kapak %s"
              % ("≈14,4 kg" if _ad.startswith("K1") else "≈10,4 kg"))
    ekle("onyuz_mentese_tabani_" + _ad, kut(_tx[0], _tx[1], _y0, _y0 + 70.0, Z_CER[1], Z_SKAPAK[0] - 1.5), "paslanmaz", "K",
         not_="v14b · menteşe TABANI AISI 304 blok 30 × 13,5 × 70 · TC yan sacının iç yüzüne 2 × M6 + ön dönüşün (+37,5…+39) arkasına dayalı · kol buna 2 × M5 (denetim_C bulgu 3)")
for _ad, _x0, _x1, _y0, _y1 in (("basac_K1", 780.0, 810.0, 1990.0, 2020.0), ("basac_K2", 830.0, 870.0, 1730.0, 1742.0)):
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
kontrol("sos valf eyleyicisi sol duvara değmiyor (%.0f > %.0f)" % (bb("sos__valf_dondurme_aktuatoru").xmin, BAY_A[0]), bb("sos__valf_dondurme_aktuatoru").xmin > BAY_A[0])
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
# v16 · SOĞUK KUTU: her yüz 60 · yan dış kabuk = TC yan sacı · boşluk yok
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]
kontrol("v16 · yan PU duvarları alt dış sacın üstünden (%.1f) başlıyor · TC yan saclarının iç yüzüne YAPIŞIK (x %.1f / %.1f · boşluk 0, v15 28,5)" % (Y_ALT1, bb("kabin_sol_duvar_PU").xmin, bb("kabin_sag_duvar_PU").xmax),
        all(abs(p["sh"].BoundingBox().ymin - Y_ALT1) < 0.01 for p in _sd) and abs(bb("kabin_sol_duvar_PU").xmin - X_SAC[0]) < 0.01 and abs(bb("kabin_sag_duvar_PU").xmax - X_SAC[1]) < 0.01)
_k60 = {"sol duvar": BAY_A[0], "sağ duvar": W - BAY_B[1], "arka": Z_BOLME[0] - Z_BOLME[1], "A tavanı": YUST - TAVAN_A, "L dikey": X_TEK - BAY_A[1], "B tavanı": Y_TEK - TAVAN_B}
kontrol("v16 · BÜTÜN YÜZLER 60 (kaplama 1,0 + PU 57,5 + dış 1,5): %s · PU yan %.1f / %.1f · taban %.0f (UNO ağzı + yayıcı kelepçesi 1274'te) · kapaklar 40"
        % (" · ".join("%s %.1f" % (a_, v_) for a_, v_ in _k60.items()), bb("kabin_sol_duvar_PU").xlen, bb("kabin_sag_duvar_PU").xlen, SOGUK_TABAN - YAL_Y0),
        all(abs(v_ - T_DUV) < 0.01 for v_ in _k60.values()) and abs(bb("kabin_sol_duvar_PU").xlen - T_PU) < 0.01 and abs(bb("kabin_sag_duvar_PU").xlen - T_PU) < 0.01)
for _ad, _mod, _x0, _x1 in KASET:
    _kb_ = bb("%s__cikis_tupu" % _mod); _hn_ = bb("%s_inis_hunisi" % _mod.split("_")[0])
    kontrol("%s çıkış borusu altı (%.0f) iniş hunisinin üstünde (%.0f), iç içe DEĞİL" % (_ad, _kb_.ymin, _hn_.ymax), _kb_.ymin > _hn_.ymax)
_yb = bb("yalitim_blogu"); _ik = bb("soguk_ic_kaplama")
kontrol("v16 · PU tek köpük (arka + A tavanı + L + B tavanı: x %.1f…%.1f · y %.1f…%.1f · z %.1f…%.1f) · iç kaplama TEK PARÇA (x %.0f…%.0f · y %.1f…%.0f · z %.0f…%.0f)"
        % (_yb.xmin, _yb.xmax, _yb.ymin, _yb.ymax, _yb.zmin, _yb.zmax, _ik.xmin, _ik.xmax, _ik.ymin, _ik.ymax, _ik.zmin, _ik.zmax),
        len([p for p in P if p["ad"] == "yalitim_blogu"][0]["sh"].Solids()) == 1 and len([p for p in P if p["ad"] == "soguk_ic_kaplama"][0]["sh"].Solids()) == 1
        and abs(_yb.xmin - X_SAC[0]) < 0.01 and abs(_yb.xmax - X_SAC[1]) < 0.01 and abs(_yb.zmax - Z_ZARF) < 0.01 and abs(_yb.zmin - Z_BOLME[1] - T_DIS) < 0.01 and abs(_yb.ymax - Y_UST_SAC) < 0.01
        and abs(_ik.xmin - BAY_A[0] + T_IC) < 0.01 and abs(_ik.xmax - BAY_B[1] - T_IC) < 0.01 and abs(_ik.ymax - TAVAN_A - T_IC) < 0.01 and abs(_ik.zmin - Z_SOGUK[1] + T_IC) < 0.01)
_yv = [p for p in P if p["ad"].startswith(("soguk_hucre", "arka_yalitim"))]; kontrol("eski parçalı yalıtım kalktı", not _yv)
KUTU_AD = tuple(KUTU) + ("alt_yalitim_PU",)
_BAGLAM = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "teknik_bant", "baglam", "kompresor", "hava_ana", "pide", "tabla_diski")
_kb = []
_ks = [(q["ad"], q["sh"], q["sh"].BoundingBox()) for q in P if q["ad"] in KUTU_AD]
for p in P:
    if p["ad"].startswith(_BAGLAM): continue
    b_ = p["sh"].BoundingBox()
    for a_, s_, bk_ in _ks:
        if a_ == p["ad"]: continue
        if b_.xmax < bk_.xmin or bk_.xmax < b_.xmin or b_.ymax < bk_.ymin or bk_.ymax < b_.ymin or b_.zmax < bk_.zmin or bk_.zmax < b_.zmin: continue
        try: v_ = p["sh"].intersect(s_).Volume()
        except Exception: v_ = -1.0
        if v_ > 1.0 or v_ < 0: _kb.append((p["ad"], a_, round(v_, 1)))
kontrol("v16 · soğuk kutuya (kaplama · 3 PU · dış saclar · taban) hiçbir parça girmiyor · kutu parçaları birbirine girmiyor (kovan / blok / hortum / burç deliklerinde): %d" % len(_kb), not _kb, str(_kb[:6]))

_ay = bb("alt_yalitim_PU"); _as = bb("alt_yalitim_saci")
kontrol("v16 · soğuk oda TABANI 43: alt dış sac 1,5 y %.1f–%.1f (x %.1f–%.1f TEK PARÇA, yan + arka duvarların altı dahil) + PU 38,5 y %.1f–%.1f · x %.0f–%.0f · z %.0f…%.0f + raf 3 · %d geçiş deliği"
        % (_as.ymin, _as.ymax, _as.xmin, _as.xmax, _ay.ymin, _ay.ymax, _ay.xmin, _ay.xmax, _ay.zmin, _ay.zmax, len(ALT_DELIK)),
        abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_ay.ymin - Y_ALT1) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and abs(_as.ymax - Y_ALT1) < 0.01
        and abs(_as.xmin - X_SAC[0]) < 0.01 and abs(_as.xmax - X_SAC[1]) < 0.01 and abs(_ay.xmin - BAY_A[0] - 3.0) < 0.01 and abs(_ay.xmax - BAY_B[1] + 3.0) < 0.01)
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
_ZA = ("yalitim_blogu", "tasiyici_raf_3mm", "raf_on_bukumu", "teknik_ayirma_saci_yatay", "teknik_ayirma_saci_dikey", "kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "soguk_ic_kaplama", "alt_yalitim_saci")
kontrol("v16 · soğuk kutunun ön yüzü TEK DÜZLEM +%.0f (%d parça: kaplama, 3 PU, teknik saclar, alt sac, raf) · alt PU %.1f (raf ön bükümünün arkası)" % (Z_ZARF, len(_ZA), bb("alt_yalitim_PU").zmax),
        all(abs(bb(a_).zmax - Z_ZARF) < 0.01 for a_ in _ZA) and abs(bb("alt_yalitim_PU").zmax - (Z_ZARF - RAF_T)) < 0.01)
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
                ("motor_kablosu_sucuk_cad_v8_rotor", "motor_sucuk_cad_v8_rotor"),
                ("raf_kosebendi_sol", "tasiyici_raf_3mm"), ("raf_kosebendi_sag", "tasiyici_raf_3mm"), ("raf_kosebendi_sol", "soguk_ic_kaplama"), ("raf_kosebendi_sag", "soguk_ic_kaplama"),
                ("raf_askisi_burclari_sol", "soguk_ic_kaplama"), ("raf_askisi_burclari_sag", "soguk_ic_kaplama"), ("kabin_sol_duvar_PU", "soguk_ic_kaplama"), ("kabin_sag_duvar_PU", "soguk_ic_kaplama"),
                ("yalitim_blogu", "soguk_ic_kaplama"), ("yalitim_blogu", "soguk_arka_dis_sac"), ("yalitim_blogu", "teknik_ayirma_saci_yatay"), ("yalitim_blogu", "teknik_ayirma_saci_dikey"),
                ("alt_yalitim_saci", "soguk_arka_dis_sac"), ("alt_yalitim_saci", "kabin_sol_duvar_PU"), ("alt_yalitim_PU", "alt_yalitim_saci"), ("raf_on_bukumu", "alt_yalitim_saci"), ("raf_arka_bukumu", "soguk_ic_kaplama"),
                ("evaporator_govdesi", "soguk_ic_kaplama"), ("evaporator_lamel_paketi", "evaporator_govdesi"), ("evaporator_fani", "evaporator_lamel_paketi"), ("evaporator_damlama_tavasi", "evaporator_govdesi"),
                ("evaporator_tahliye_hortumu", "evaporator_damlama_tavasi"), ("yogusma_buharlastirma_kabi", "soguk_arka_dis_sac"), ("sogutma_emis_hatti", "evaporator_govdesi"), ("sogutma_sivi_hatti", "evaporator_govdesi"),
                ("sogutma_hat_gecis_blogu", "soguk_ic_kaplama"), ("sogutma_emis_hatti", "sogutma_hat_gecis_blogu"), ("sogutma_sivi_hatti", "sogutma_hat_gecis_blogu"),
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

# ---------------------------------------------------------------- v16 · SOĞUK KUTU + SOĞUTMA
_ev = bb("evaporator_govdesi"); _sh_ = bb("sos_hazne_bizim"); _hh = bb("harc_hazne_bizim"); _eh = bb("sogutma_emis_hatti"); _sv = bb("sogutma_sivi_hatti")
kontrol("v16 · evaporatör soğuk odanın İÇİNDE (x %.0f–%.0f ⊂ %.0f–%.0f · y %.0f–%.0f ≤ tavan %.0f · z %.0f…%.0f) · SOS haznesi dolumda 15 kalkınca %.0f < evaporatör altı %.0f"
        % (_ev.xmin, _ev.xmax, BAY_A[0], BAY_A[1], _ev.ymin, _ev.ymax, TAVAN_A, _ev.zmin, _ev.zmax, _sh_.ymax + 15.0, _ev.ymin),
        _ev.xmin >= BAY_A[0] and _ev.xmax <= BAY_A[1] and _ev.ymax <= TAVAN_A + 0.01 and _ev.zmin >= Z_SOGUK[1] and _ev.zmax <= Z_ZARF and _sh_.ymax + 15.0 < _ev.ymin)
kontrol("v16 · soğutma hatları (emiş Ø31 yalıtımlı + sıvı Ø6,35) L duvarındaki POM bloktan teknik cebe (x %.0f → %.0f) · HARÇ haznesinin üstünden: hat altı %.1f > hazne dolumda %.0f · tavan altı %.1f < %.0f"
        % (_eh.xmin, _eh.xmax, min(_eh.ymin, _sv.ymin), _hh.ymax + 15.0, max(_eh.ymax, _sv.ymax), TAVAN_A),
        _eh.xmax >= X_TEK and min(_eh.ymin, _sv.ymin) > _hh.ymax + 15.0 and max(_eh.ymax, _sv.ymax) < TAVAN_A)
_th = bb("evaporator_tahliye_hortumu"); _yk = bb("yogusma_buharlastirma_kabi")
kontrol("v16 · yoğuşma suyu: tava → Ø8 hortum arka duvardan (y %.0f) → kuru bölmedeki elektrikli buharlaştırma kabı (üstü %.0f · x %.0f–%.0f) · altında elektrik yok (valf adası x ≥ %.0f · bobin üstü %.0f)"
        % (TAHLIYE[1][1], _yk.ymax, _yk.xmin, _yk.xmax, ADA[0], ADA[3] + 30.0), TAHLIYE[1][1] > _yk.ymax and _yk.zmax <= Z_BOLME[1] + 0.01 and _yk.ymin > ADA[3] + 30.0)
for _u in ("sos", "harc"):
    _vk = bb("%s_spreader_kesme_valfi_kapak" % _u); _gk_ = bb("%s_spreader_giris_kelepcesi" % _u)
    kontrol("v16 · %s yayıcısı tabanın ALTINDA: kesme valfi kapağı %.0f · giriş kelepçesi %.0f < taban altı %.0f (v15'te valf tabana 17 mm gömülüydü)" % (_u, _vk.ymax, _gk_.ymax, YAL_Y0),
            _vk.ymax < YAL_Y0 and _gk_.ymax < YAL_Y0)
# v16 · BOŞLUK YOK (Kemal: "sağ sol duvardaki yalıtımla sac duvar arasında boşluk var"): taban üstünde (y ≥ 1320) dış kabukların içi = oda + kutu parçaları + geçişler
_ZT_ = _kutu2((X_SAC[0], X_SAC[1], SOGUK_TABAN, Y_TEK), (X_SAC[0], X_TEK, Y_TEK, Y_UST_SAC), Z_BOLME[1], Z_ZARF).val()
_ODT = _kutu2((BAY_A[0], BAY_A[1], SOGUK_TABAN, TAVAN_A), (BAY_A[0], BAY_B[1], SOGUK_TABAN, TAVAN_B), Z_SOGUK[1], Z_ZARF + 1.0).val()
_kal = _ZT_.cut(_ODT)
for _p in P:
    if _p["ad"] in KUTU or _p["ad"].startswith(("kovan_", "gecis_blogu_yalitim", "sogutma_hat_gecis_blogu", "raf_askisi_burclari", "evaporator_tahliye_hortumu", "sogutma_emis_hatti", "sogutma_sivi_hatti")) \
            or _p["ad"].endswith("_mil_gecis_kovani") or _p["ad"] in HORTUM_GECIS:
        _kal = _kal.cut(_p["sh"])
for _p in [p for p in P if p["ad"].startswith("kovan_") or p["ad"].endswith("_mil_gecis_kovani")]:          # kovan içi = mil (keçeli geçiş, ölçüm dışı)
    _b = _p["sh"].BoundingBox(); _kal = _kal.cut(silz((_b.xmin + _b.xmax) / 2.0, (_b.ymin + _b.ymax) / 2.0, 11.5, _b.zmin - 1.0, _b.zmax + 1.0).val())
_kv = [(s_.Volume(), s_.BoundingBox()) for s_ in _kal.Solids() if s_.Volume() > 1e-3]
kontrol("v16 · soğuk kutu duvar + tavanlarında BOŞLUK YOK (y ≥ %.0f · dış kabukların içi = oda + kaplama + PU + saclar + kovan / blok / hortum geçişleri): kalan %.2f mm³ ≤ 5"
        % (SOGUK_TABAN, sum(v_ for v_, b_ in _kv)), sum(v_ for v_, b_ in _kv) <= 5.0, str([(round(v_, 1), round(b_.xmin), round(b_.ymin), round(b_.zmin)) for v_, b_ in sorted(_kv, key=lambda t: -t[0])[:6]]))

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
    assert not kal, "topping_uno_cad_v16 denetimi KALDI: %s" % kal
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
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH topping_uno_cad_v16"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes, "meshes": meshes,
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
    glb_yaz(os.path.join(_od, "topping_uno_v16.glb"))
    with open(os.path.join(_od, "topping_uno_v16.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v16 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       grup={g: list(v) for g, v in GRUP.items()},
                       parcalar=[dict(ad=p["ad"], kaynak=p["kaynak"], not_=p["not_"], mal=p["mal"]) for p in P],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN]), f, ensure_ascii=False, indent=1)
    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))
    sys.stdout.flush(); os._exit(0)
