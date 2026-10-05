# -*- coding: utf-8 -*-
"""h3_qr_sac_v1 — S MODÜLÜ (QR TESLİM DOLABI + GÖZLER · PERSONEL TEZGÂHI) GÖVDESİ · ÜRETİM SACI v1 (2 Eki 2026 · Claude · YEREL · TASLAK, montaja bağlı DEĞİL)

Kemal: "gövdede tam çalışma; büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede açılır;
vidasına kadar ama mantıklı; sanayi tipi mutfakçı 3B'den direkt üretsin." · Pafta YOK, önce 3B (açınım JSON'ları ayrıca).
KAYNAKLAR: h3_sac_v1 (S) · h3_govde_ortak_v1 (GO, reçete) · sac_kararlar_v1.json > sac_standart_v1.json · mevcut gövde: qr_cad_v1.govde()/gozler() ·
           tezgah_cad_v2.govde()/cekmece() · elektrik önbelleği h3/_elk (QR 'alt_raf_3' · 'ust_raf_3' delik hedefleri, elk parçaları çevre olarak).
KOORDİNAT: DÜNYA (qr_cad_v1 ve tezgah_cad_v2 parçaları zaten dünyada; Cerceve ötelemesi 0). x hat boyu · y yukarı · z koridordan sokağa.

KURGU — QR TESLİM DOLABI (kendinden taşıyıcı bükümlü sac kutu · profil iskelet YOK, mevcut kurgu korunur)
  · Dış zarf değişmez: x 4570–5430 · y 0–2050 · robot yüzü z 670 · müşteri yüzü z 1190 · raflar 447–450 / 1650–1653 · 12 göz yeri ve ağızları aynı.
  · TABAN 3 mm düz plaka (17–20) = şasi: 6 × DIN 929 M10 kaynak somunu ALTTA (iç hacimde robot kontrol kutusu 3,5 mm geride → üstte hiçbir şey yok) ·
    alçak profil ayarlı ayak (SPEC ayak 0–17 sabit) · 6 × 3 mm L kulak (yan sacları tutar, tabana kaynaklı) · ön kenarda servis paneli dil çentikleri.
  · YAN SACLAR 1,5 düz (dış satine, iki yüzde 1,5 kenar görünür — eski görünüm). Bütün iç parçalar yan saca PEM FHP-M5 gömme saplamayla (dışta iz yok).
  · ROBOT YÜZÜ GÖZ SACI 1,5 tava (12 kapak ağzı aynı): yanlarda 25 dönüş (FHP), altta 22 dönüş (alt rafın altında · raf üstünden M5 → flanşta PEM SP-M5),
    üstte 20 dönüş (üst rafın üstünde · M6 → rafta PEM SP-M6). Göz sacı kuruyken alt ve üst raf onun dönüşlerine oturur → raf ön kenarı derin kirişe bağlı.
  · MÜŞTERİ YÜZÜ TEK SAC 1,5 tava (eski göz sacı + alt panel + üst panel = tek parça, ek yeri yok): 12 kapı ağzı + ekran / okuyucu / PIN pencereleri aynı ·
    4 kenarda 25 iç dönüş (yanlar FHP, alt tabana alttan M5, üst tavana FHP).
  · RAFLAR 3 mm (ad korunur, elektrik delikleri sacda hazır): yanlarda 25 aşağı dönüş (FHP) · alt rafın ARKASINDA 40 aşağı dönüş (kiriş: göz yükü arka
    kenarda, 3 mm düz raf 857 açıklıkta ~10 kat fazla sehim yapardı) · üst rafa göz dikmeleri taşır.
  · TAVAN 1,5 tava iç oturur (yanlar FHP, robot tarafında 14 stop dönüşü, müşteri yüzünün üst dönüşüne FHP-M5 aşağı — üstte görünür vida yok).
  · ROBOT TARAFI SERVİS PANELLERİ (alt: robot kontrol · üst: istasyon kutusu + UPS) 1,5 DÜZ, MENTEŞESİZ KALDIR-ÇIKAR: koridor 591 mm (yer rayı z 240–480,
    makine önü z 79) → dikey eksenli kapak açılamaz; filtreli fanlar panelin iç yüzünde (z 671,5), cihazlar yüzün 5 mm gerisinde → çift cidar / büküm sığmaz. Çeyrek dönüş kilit (alt 2 ·
    üst 4) kamları yan saclara FHP'li 1,5 L çerçeve çıtalarının arkasına; alt panel 3 dil ile taban çentiklerine oturur. Elektrik katmanının kablo giriş
    plakaları için 2 çentik (a · b) aynı yerde. ESKİ menteşeler kalkar.
  · GÖZLER: göz kasası 1,0 mm = iki U (alt + üst) + iki yanda TIG alın dikişi (iç yüz taşlanır, bindirme yok) · göz dikmesi 304 lama 20 × 10 (uçlar M5 diş,
    raflara ISO 7380) · kasa dikmeye PEM FHP-M4 (baş göz içinde gömme) + DIN 9021 + ISO 10511 dışarıdan. Göz kapakları, motor, sensör, mandal, ısıtıcı,
    alüminyum taban, kilit kartı CİHAZ — dokunulmadı.
KURGU — PERSONEL TEZGÂHI (panel kutu, kendinden taşıyıcı)
  · TABLA 1,2 tava: önde 30 önlük (J yok: düz bıçakla bükülemez), arka ve iki yanda 100 etek TEK PARÇA büküm (eski 3 etek + 30 mm dolu blok → tek sac) · arka köşeler
    bindirme + TIG + taşlama · lavabo haznesi tablaya TIG (alttan köşe dikiş) · alttan 3 omega takviye (yapıştırma + ses yalıtımı) · CD saplamalarla gövdeye.
  · Gövde 1,2: sokak yanı (ön dönüş = menteşe kayıtı) · ayırma paneli (ön dönüş = bas-aç kayıtı) · arka panel (bulaşık bağlantı penceresi) · ince duvar üst
    kuşağı (ray + tabla) · evye dolabı tabanı tava (sızdırmaz köşeler, kimyasal bidonları) · 4 + 1 hijyenik ayak (M12, kör burç + 3 mm plaka) · plint.
  · KAPAK çift cidar 18 (GO.kapak) · 2 gizli 180° menteşe (sokak yanına FHP) · bas-aç · KULP YOK. ÇEKMECE önü çift cidar 18 + bükümlü kutu tavası ·
    bas-aç arkada · kam kilit karşılığı. Bulaşık, evye cihazları, raylar, kam kilit CİHAZ.
ARAYÜZLER DEĞİŞMEZ: QR dış zarfı + göz ağızları + robot yüzü düzlemi z 670 (elektrik göz braketleri bu yüze dayanır) · raf kotları (elk kanalı, kelepçeler
  üst rafın altına 1650'de) · tezgâh zarfı x 3842–4505 · z 1044–1874 · tabla 900 · etek üstü 1000 (duvar kaplama sacı dudağı) · önler x 3857.
KOMŞU İSTASYON YOK (S modülü koridorun karşısında) → M8 noktası yok · karşı delik listesi BOŞ · bina bağlantıları ARAYÜZ olarak.
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_qr): python -u ../../../../sac_qr/qr_sac_denetim_v1.py"""
import math, os, sys, re, json, time
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_qr_sac_v1"
V = cq.Vector

# =====================================================================================================================================
# 0 · ARAYÜZ SABİTLERİ (dünya · qr_cad_v1 / tezgah_cad_v2 ile AYNI · değişmez)
# =====================================================================================================================================
QX0, QX1 = 4570.0, 5430.0                     # QR sol / sağ dış yüz
XL, XR = 4571.5, 5428.5                       # yan sac iç yüzleri
ZR, ZM = 670.0, 1190.0                        # robot yüzü / müşteri yüzü (dış)
YT0, YT1, YTOP = 17.0, 20.0, 2050.0           # taban plakası · tavan üstü
ALT_RAF, UST_RAF = (447.0, 450.0), (1650.0, 1653.0)
GOZ_XL = (30.0, 440.0)                        # göz sütunları yerel x (+ QX0)
GOZ_W, GOZ_H = 380.0, 190.0
GOZ_Z = (710.0, 1150.0)
GOZ_TABAN = tuple(450.0 + 200.0 * r for r in range(6))
DIKME_X = ((4590.0, 4600.0), (4980.0, 4990.0), (5000.0, 5010.0), (5390.0, 5400.0))     # göz dikmeleri (lama 10 x)
DIKME_Z = ((712.0, 732.0), (1128.0, 1148.0))                                          # (lama 20 z)
PANEL_PENCERE = {"ekran": (270.0, 435.0, 1668.0, 1768.0), "okuyucu": (475.0, 545.0, 1688.0, 1738.0), "pin": (583.0, 663.0, 1678.0, 1758.0)}
FAN = dict(alt=(5300.0, 350.0), ust=(5320.0, 1960.0), cap=116.0)                       # filtreli fan delikleri (merkez dünya x, y)
AYAK_XZ = [(QX0 + x, ZR + z) for z in (30.0, 490.0) for x in (30.0, 430.0, 830.0)]     # mevcut ayak noktaları (korunur)
# kendi kurgumuzun kotları
G_ALT_Y, G_UST_Y = 445.5, 1654.5              # göz sacı alt dönüşü dış yüzü (alt rafın altı) · üst dönüşü dış yüzü (üst rafın üstü)
Z_RAF_ON = 674.25                             # raf ön kenarı (göz sacı büküm yayının arkası)
Z_RAF_ARKA = 1188.0                           # raf arka kenarı / arka dönüş dış yüzü (müşteri sacına 0,5)
PANEL_T = 1.5                                 # servis panelleri (filtreli fanlar panelin iç yüzüne bağlı, z 671,5 → 1,5)
DERZ = 3.0
PANEL_X = (QX0 + 1.5 + DERZ, QX1 - 1.5 - DERZ)                                         # 4574,5 – 5425,5
PANEL_ALT_Y = (YT1 + DERZ, G_ALT_Y - DERZ)                                            # 23 – 442,5
PANEL_UST_Y = (G_UST_Y + DERZ, YTOP - DERZ)                                           # 1657,5 – 2047
CENTIK = dict(a=(5036.0, 5161.0), b=(5296.0, None), y=88.0)                           # elk giriş plakaları (a 5040–5157 · b 5300–5428 · üstü 83,6) + pay
DIL_X = (4680.0, 4900.0, 5230.0)                                                     # alt panel dilleri → taban çentikleri
DUDAK = dict(z0=672.0, en=15.0, bacak=25.0)                                           # çerçeve çıtası (servis paneli stop + kilit karşılığı)
KILIT = dict(alt=[(4586.0, 425.0, "asagi", 16.0), (5395.0, 425.0, "sag", 18.0)],     # sol alt Ø16: robot kontrol kutusu x 4595 · panel kenarı 4574,5
             ust=[(4605.0, 1700.0, "sol"), (4605.0, 2000.0, "sol"), (5395.0, 1700.0, "sag"), (5395.0, 1850.0, "sag")])
MUSTERI_YAN_Y = (55.0, 240.0, 432.0, 620.0, 810.0, 1000.0, 1190.0, 1380.0, 1570.0, 1760.0, 1950.0, 2015.0)   # raf kotlarından (447 · 1650) uzak · ≤ 200
KULAK_SOL_Z, KULAK_SAG_Z = (720.0, 870.0, 1020.0, 1140.0), (1075.0, 1145.0)           # sağda 710–1048 elk omurga kanalı

BIRIM_QR, BIRIM_GOZ = "QR_GOVDE", "QR_GOZLER"
BIRIM_TZ, BIRIM_CEK = "TEZGAH_GOVDE", "TEZGAH_CEKMECE"

# ---------------- TEZGÂH ----------------
TX_ON, TX_GOV, TX_KAYIT, TX_ARKA, TX_TABLA = 3857.0, 3875.0, 3877.0, 4505.0, 3842.0   # önler · kapak iç düzlemi · kayıt (bas-aç / stop) · arka · tabla önü
TZ_SOL, TZ_SAG = 1044.0, 1874.0
TZ_BOL = (1515.2, 1516.4)
TY_PL, TY_UST, TY_TABLA = 100.0, 898.8, 900.0                                         # taban · gövde üstü (tabla altı) · tabla üstü
TY_ETEK = 1000.0
TT = 1.2
TAYAK = [(3905.0, 1546.4), (3905.0, 1842.8), (4473.8, 1546.4), (4473.8, 1842.8)]      # evye dolabı ayakları (mevcut)
TAYAK4 = (4484.0, 1065.0)                                                             # arka sol köşe ayağı (mevcut)
HAZNE = (3889.0, 4191.0, 1543.6, 1845.6)                                              # tabla kesiği (hazne dış ölçüsü)
BATARYA = (4240.0, 1694.6, 34.0)
KAPAK_T = dict(u=(1518.0, 1871.4), v=(104.0, 866.0))
CEKMECE_ON = dict(u=(1047.0, 1514.8), v=(720.0, 866.0))
CEK_KUTU = dict(x=(3875.0, 4375.0), y=(725.0, 830.0), z=(1057.9, 1502.5))
RAF_Y = 716.0

MALZEME = {"sac": dict(renk=(0.78, 0.80, 0.83, 1.0), met=0.85, ruf=0.32), "kabuk": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "siyah": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.2, ruf=0.6),
           "conta": dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8), "on_seffaf": dict(renk=(0.70, 0.82, 0.95, 0.16), met=0.1, ruf=0.15, saydam=True)}
S._RENK.update({"mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "cihaz": ((0.30, 0.34, 0.40, 1.0), 0.3, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "elektrik": ((0.95, 0.70, 0.15, 1.0), 0.2, 0.5), "profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30)})


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


def _altigen_y(cx, cz, s, y0, y1):
    """y eksenli altıgen prizma (anahtar ağzı s)"""
    r = s / math.sqrt(3.0)
    w = cq.Wire.makePolygon([V(cx + r * math.cos(math.radians(30 + 60 * i)), y0, cz + r * math.sin(math.radians(30 + 60 * i))) for i in range(6)], close=True)
    return cq.Solid.extrudeLinear(w, [], V(0, y1 - y0, 0))


def _altigen_z(cx, cy, s, z0, z1):
    r = s / math.sqrt(3.0)
    w = cq.Wire.makePolygon([V(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i)), z0) for i in range(6)], close=True)
    return cq.Solid.extrudeLinear(w, [], V(0, 0, z1 - z0))


class G:
    """kurulan iki gövde (modül düzeyinde tek örnek)"""
    q = None          # QR (QR_GOVDE + QR_GOZLER)
    t = None          # tezgâh (TEZGAH_GOVDE + TEZGAH_CEKMECE)
    P = {}            # adlı paneller
    kuruldu = False


def _bag(g, b):
    for x in b["parcalar"]: g.eleman(x)
    g.BIRLESIM.append(b)
    return b


def _fhp(g, A, B, nokta, ad, dis="M5"):
    """A sacında FHP gömme saplama (dışta iz yok) → B'de geçiş deliği + DIN 9021 + ISO 10511 içeriden"""
    return _bag(g, S.vidali_birlesim(A, B, tuple(map(float, nokta)), "pem_saplama", dis=dis, ad=ad, birim=g.birim))


def _pem(g, A, B, nokta, ad, dis="M5"):
    """A'dan ISO 7380 (baş A'nın dışında) → B'de PEM SP somun (gövde B'nin uzak yüzünde)"""
    return _bag(g, S.vidali_birlesim(A, B, tuple(map(float, nokta)), "pem_somun", dis=dis, ad=ad, birim=g.birim))


def _fhp_paket(g, A, nokta, yon, paket, ad, dis="M4"):
    return _bag(g, S.saplama_baglantisi(A, tuple(map(float, nokta)), tuple(map(float, yon)), paket, dis=dis, pem_tip="FHP", ad=ad, birim=g.birim))


def _kaynak4(g, ad, x0, x1, y, z0, z1, ust_yon=(0, -1.0, 0), a=2.0, not_=""):
    """dikdörtgen plakanın 4 kenarı ↔ üstündeki sac (alt yüz y) köşe dikişi (plaka alttaysa ust_yon (0,-1,0))"""
    out = []
    for j, (p0, p1, u1) in enumerate((((x0, y, z0), (x0, y, z1), (-1, 0, 0)), ((x1, y, z0), (x1, y, z1), (1, 0, 0)),
                                      ((x0, y, z0), (x1, y, z0), (0, 0, -1)), ((x0, y, z1), (x1, y, z1), (0, 0, 1)))):
        out.append(S.kaynak_dikisi(p0, p1, u1, ust_yon, a, ad="%s_%d" % (ad, j + 1), birim=g.birim, taraf="dis (köşe)", not_=not_))
    g.kaynak(out)
    return out


# =====================================================================================================================================
# 1 · QR TESLİM DOLABI
# =====================================================================================================================================
def _yan(g, taraf):
    """yan sac 1,5 düz (y 20–2050 · z 670–1190) · n içeri"""
    ad = "yan_sac_sol" if taraf == "sol" else "yan_sac_sag"
    s = g.sac(ad, "dis", kabuk=True)
    if taraf == "sol":
        P = s.taban([(YT1, ZR), (YTOP, ZR), (YTOP, ZM), (YT1, ZM)], O=(QX0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
    else:
        P = s.taban([(YT1, -ZM), (YTOP, -ZM), (YTOP, -ZR), (YT1, -ZR)], O=(QX1, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
    G.P["yan_" + taraf] = P
    return P


def _taban(g):
    s = g.sac("taban_plakasi_3", "braket", t=3.0)
    poly = [(QX0, -ZM), (QX1, -ZM), (QX1, -ZR), (QX0, -ZR)]
    P = s.taban(poly, O=(0, YT0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    for x in DIL_X:                                                     # servis paneli dil çentikleri (açık, ön kenarda) · panel üstten devrilip çıkar
        P.kesik([(x - 11.0, -ZR - 6.0), (x + 11.0, -ZR - 6.0), (x + 11.0, -ZR + 1.0), (x - 11.0, -ZR + 1.0)], tip="dil_centigi", dfm=False,
                parca="alt servis paneli dili 22 × 6 (açık çentik)")
    for i, (x, z) in enumerate(AYAK_XZ):                                # ayak mili geçişi (kaynak somunu altta)
        P.delik(x, -z, 10.5, tip="ayak_deligi", parca="M10 ayak mili (kaynak somunu altta)")
    G.P["taban"] = P
    return P


def _goz_robot(g):
    """robot yüzü göz sacı 1,5 tava · z 670–671,5 (elektrik braketleri bu yüze dayanır) · 12 kapak ağzı 340 × 182"""
    s = g.sac("robot_yuzu_goz_saci", "dis"); gg = s.R + s.t
    u0, u1, v0, v1 = XL + gg, XR - gg, G_ALT_Y + gg, G_UST_Y - gg
    P = s.taban([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], O=(0, 0, ZR), ex=(1, 0, 0), ey=(0, 1, 0), ad="yuz")
    f_alt = P.flans(0, 22.0, yon=+1, ad="alt_donus")                    # alt rafın altında → raf ön kenarı burada PEM'e vidalı
    f_sag = P.flans(1, 25.0, yon=+1, ad="sag_donus")
    f_ust = P.flans(2, 30.0, yon=+1, ad="ust_donus")                    # üst rafın üstünde · 30: M6 PEM raf altındaki göz kablo / kelepçelerinin (z ≤ 689) gerisinde
    uv0 = f_ust.yerel((5008.0, G_UST_Y - 0.5, 690.0)); uv1 = f_ust.yerel((5117.0, G_UST_Y - 0.5, 705.0))
    f_ust.kesik([(min(uv0[0], uv1[0]), min(uv0[1], uv1[1])), (max(uv0[0], uv1[0]), min(uv0[1], uv1[1])), (max(uv0[0], uv1[0]), max(uv0[1], uv1[1])),
                 (min(uv0[0], uv1[0]), max(uv0[1], uv1[1]))], tip="centik", dfm=False, parca="UPS altlığı çentiği 109 × 10 (dönüş burada 20)")
    f_sol = P.flans(3, 25.0, yon=+1, ad="sol_donus")
    s.kose(f_alt, f_sag, "acik"); s.kose(f_sag, f_ust, "acik"); s.kose(f_ust, f_sol, "acik"); s.kose(f_sol, f_alt, "acik")
    for r in range(6):
        for c in range(2):
            cx = QX0 + GOZ_XL[c]; by = GOZ_TABAN[r]
            P.dikdortgen(cx + 208.0, by + 95.0, 340.0, 182.0, tip="goz_agzi", parca="göz %d%d robot kapağı ağzı 340 × 182" % (r, c))
    G.P.update(goz_robot=P, goz_robot_alt=f_alt, goz_robot_ust=f_ust, goz_robot_sol=f_sol, goz_robot_sag=f_sag)
    return P


def _musteri(g):
    """müşteri yüzü TEK sac 1,5 tava · z 1188,5–1190 · y 20–2048 · 12 kapı ağzı 378 × 188 + 3 pencere (n içeri = −z)"""
    s = g.sac("musteri_yuzu_goz_saci", "dis", kabuk=True); gg = s.R + s.t
    u0, u1, v0, v1 = -(XR - gg), -(XL + gg), YT1 + gg, 2048.0 - gg
    P = s.taban([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], O=(0, 0, ZM), ex=(-1, 0, 0), ey=(0, 1, 0), ad="yuz")
    f_alt = P.flans(0, 25.0, yon=+1, ad="alt_donus")                    # tabana oturur (alttan M5)
    f_sol = P.flans(1, 25.0, yon=+1, ad="sol_donus")                    # u1 kenarı = dünya sol (x 4571,5)
    f_ust = P.flans(2, 25.0, yon=+1, ad="ust_donus")                    # tavanın altında (tavandan FHP)
    f_sag = P.flans(3, 25.0, yon=+1, ad="sag_donus")
    s.kose(f_alt, f_sol, "acik"); s.kose(f_sol, f_ust, "acik"); s.kose(f_ust, f_sag, "acik"); s.kose(f_sag, f_alt, "acik")
    for r in range(6):
        for c in range(2):
            cx = QX0 + GOZ_XL[c]; by = GOZ_TABAN[r]
            P.dikdortgen(-(cx + 190.0), by + 95.0, 378.0, 188.0, tip="kapi_agzi", parca="göz %d%d müşteri kapısı ağzı 378 × 188" % (r, c))
    for ad, (a, b, c_, d) in PANEL_PENCERE.items():
        P.dikdortgen(-(QX0 + (a + b) / 2.0), (c_ + d) / 2.0, b - a, d - c_, r=1.0, tip="pencere_" + ad, parca="müşteri paneli %s penceresi" % ad)
    G.P.update(musteri=P, musteri_alt=f_alt, musteri_ust=f_ust, musteri_sol=f_sol, musteri_sag=f_sag)
    return P


def _raf(g, ad, y0, arka_flans):
    """3 mm raf · üst yüz düz · yanlarda 25 aşağı dönüş (z 697–1162) · alt rafta arkada 40 aşağı dönüş (kiriş)"""
    s = g.sac(ad, "braket", t=3.0); gg = s.R + s.t
    u0, u1 = XL + gg, XR - gg
    v_arka, v_on = -(Z_RAF_ARKA - gg) if arka_flans else -Z_RAF_ARKA, -Z_RAF_ON
    P = s.taban([(u0, v_arka), (u1, v_arka), (u1, v_on), (u0, v_on)], O=(0, y0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="raf")
    L = v_on - v_arka
    z_on, z_arka = 697.0, 1162.0
    b_sag, s_sag = (-z_arka) - v_arka, v_on - (-z_on)                  # kenar 1: arka → ön
    f_sag = P.flans(1, 30.0, yon=-1, bas=b_sag, son=s_sag, ad="sag_donus")          # 30: FHP deliği büküme ≥ 12 · kenara ≥ 2t
    f_sol = P.flans(3, 30.0, yon=-1, bas=s_sag, son=b_sag, ad="sol_donus")     # kenar 3: ön → arka
    f_arka = P.flans(0, 40.0, yon=-1, ad="arka_kiris") if arka_flans else None
    G.P.update({ad: P, ad + "_sag": f_sag, ad + "_sol": f_sol})
    if f_arka is not None: G.P[ad + "_arka"] = f_arka
    # göz dikmesi vidaları (M5) · elektrik kanalı geçişi (montaj da ADLA keser; sacda hazır)
    for (xa, xb) in DIKME_X:
        for (za, zb) in DIKME_Z:
            P.delik((xa + xb) / 2.0, -(za + zb) / 2.0, 5.5, tip="vida_deligi", parca="göz dikmesi M5 (ISO 273 orta)")
    if ad == "alt_raf_3":
        P.dikdortgen(4995.0, -1040.0, 24.0, 80.0, tip="kablo_gecisi", parca="elektrik: orta kanal → alt bölme (h3_elk · QR alt_raf_3)")
    else:
        P.dikdortgen(4995.0, -1005.0, 24.0, 150.0, tip="kablo_gecisi", parca="elektrik: orta kanal → tava (h3_elk · QR ust_raf_3)")
    return P


def _tavan(g):
    s = g.sac("tavan_sac", "dis", kabuk=True); gg = s.R + s.t
    u0, u1 = XL + gg, XR - gg
    v_arka, v_on = -1188.0, -(DUDAK["z0"] + gg)
    P = s.taban([(u0, v_arka), (u1, v_arka), (u1, v_on), (u0, v_on)], O=(0, YTOP - s.t, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tavan")
    kis = 1162.0 - 1188.0                                               # yan dönüşler müşteri yüzünün yan dönüşünden önce biter
    f_sag = P.flans(1, 25.0, yon=-1, bas=-kis, ad="sag_donus")
    f_on = P.flans(2, 14.0, yon=-1, ad="robot_stop_donusu")
    f_sol = P.flans(3, 25.0, yon=-1, son=-kis, ad="sol_donus")
    s.kose(f_sag, f_on, "acik"); s.kose(f_on, f_sol, "acik")
    G.P.update(tavan=P, tavan_sag=f_sag, tavan_sol=f_sol, tavan_on=f_on)
    return P


def _cita(g, ad, taraf, y0, y1):
    """servis çerçeve çıtası 1,5 L: dudak z 672,5–674 (panelin arkası · kilit kamı arkasına) + bacak yan saca FHP"""
    s = g.sac(ad, "dis"); gg = s.R + s.t
    if taraf == "sol":
        P = s.taban([(XL + gg, y0), (XL + DUDAK["en"], y0), (XL + DUDAK["en"], y1), (XL + gg, y1)], O=(0, 0, DUDAK["z0"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="dudak")
        f = P.flans(3, DUDAK["bacak"], yon=+1, ad="bacak")
    else:
        P = s.taban([(XR - DUDAK["en"], y0), (XR - gg, y0), (XR - gg, y1), (XR - DUDAK["en"], y1)], O=(0, 0, DUDAK["z0"]), ex=(1, 0, 0), ey=(0, 1, 0), ad="dudak")
        f = P.flans(1, DUDAK["bacak"], yon=+1, ad="bacak")
    G.P[ad] = P; G.P[ad + "_bacak"] = f
    return P, f


def _servis_panel(g, ad, y0, y1, alt):
    """robot yüzü servis paneli 1,5 düz · menteşesiz kaldır-çıkar · yarık ızgara (lazer 5 × 60) + fan deliği + kilit delikleri"""
    s = g.sac(ad, "braket", t=PANEL_T, mal="on_seffaf")
    x0, x1 = PANEL_X
    if alt:
        a0, a1 = CENTIK["a"]; b0 = CENTIK["b"][0]; yc = CENTIK["y"]
        poly = [(x0, y0), (a0, y0), (a0, yc), (a1, yc), (a1, y0), (b0, y0), (b0, yc), (x1, yc), (x1, y1), (x0, y1)]
    else:
        poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    P = s.taban(poly, O=(0, 0, ZR), ex=(1, 0, 0), ey=(0, 1, 0), ad="panel")
    if alt:
        for x in DIL_X:
            k = 0 if x < CENTIK["a"][0] else 4
            P.dil(k, (x - 10.0) - (x0 if k == 0 else CENTIK["a"][1]), 20.0, 6.0)
        fx, fy = FAN["alt"]
        izg = [(4710.0, 4995.0, 100.0), (5170.0, 5410.0, 100.0)]
    else:
        fx, fy = FAN["ust"]
        izg = [(5130.0, 5370.0, 1690.0), (4700.0, 4940.0, 1890.0)]
    P.delik(fx, fy, FAN["cap"], tip="fan_deligi", parca="filtreli fan Ø116 (cihaz arkada)")
    for k_ in KILIT["alt" if alt else "ust"]:
        xk, yk, cap = k_[0], k_[1], (k_[3] if len(k_) > 3 else 18.0)
        P.delik(xk, yk, cap + 0.2, tip="kilit_deligi", parca="çeyrek dönüş kilit Ø%g" % cap)
    L = S.STD.lazer_yarik(); adim = L["genislik"] + L["sira"]
    for i, (xa, xb, ya) in enumerate(izg):
        n_s = int((xb - xa) // adim)
        n_r = 2
        P.lazer_yarik_dizisi((xa + xb) / 2.0, ya + (n_r * L["boy"] + (n_r - 1) * L["kopru"]) / 2.0, n_s, n_r, aci=90.0)
    G.P[ad] = P
    return P


def _kilit(g, ad, xk, yk, yon, cap=18.0):
    """çeyrek dönüş kilit (anahtarlı, gömme baş) · gövde Ø cap × 16 · somun SW cap+4 × 3 (panel iç yüzü) · kam 2 × (cap−2) × 28 (z 675–677) · TEMSİLİ (katalogdan)"""
    z0 = ZR
    r, w = cap / 2.0, cap / 2.0 - 1.0
    sh = silindir((xk, yk, z0), (0, 0, 1), r, 16.0).fuse(_altigen_z(xk, yk, cap + 4.0, z0 + PANEL_T, z0 + PANEL_T + 3.0))
    if yon == "asagi": cam = kutu(xk - w, xk + w, yk - 28.0, yk + 2.0, z0 + 5.0, z0 + 7.0)
    elif yon == "sag": cam = kutu(xk - 2.0, xk + 28.0, yk - w, yk + w, z0 + 5.0, z0 + 7.0)
    else: cam = kutu(xk - 28.0, xk + 2.0, yk - w, yk + w, z0 + 5.0, z0 + 7.0)
    sh = sh.fuse(cam).clean()
    return g.eleman(g.ozel(ad, sh, "Southco E5 / EMKA 1000 sınıfı (TEMSİLİ)", "Çeyrek dönüş kilit · anahtarlı · gömme baş Ø%g · kam arkada (çerçeve çıtasına)" % cap,
                           "Ø%g × 16 · SW%g somun · kam 28" % (cap, cap + 4.0), malzeme="AISI 316 / PA", mal="siyah"))


def _ayak_qr(g, i, x, z):
    """alçak profil ayarlı ayak M10 (SPEC: ayak 0–17 sabit) · taban Ø50 · DIN 929 M10 kaynak somunu taban plakasının ALTINDA"""
    g.eleman(S.kaynak_somunu("M10", (x, YT0, z), (0, -1, 0), ad="ayar_ayagi_%d_kaynak_somunu" % i, birim=g.birim))
    sh = silindir((x, 0.0, z), (0, 1, 0), 25.0, 5.0).fuse(_altigen_y(x, z, 17.0, 5.0, 8.5)).fuse(silindir((x, 8.5, z), (0, 1, 0), 4.9, YT1 - 8.5))
    g.eleman(g.ozel("ayar_ayagi_%d" % i, sh.clean(), "alçak profil ayar ayağı (Elesa LV.F-SST sınıfı · TEMSİLİ)",
                    "Alçak profil ayarlı ayak M10 · AISI 304 · taban Ø50 PA kaymaz ped", "toplam 17 · ayar +4 (ped kalınlığı) · 2,5 kN", malzeme="AISI 304", mal="celik"))


def _goz_kasasi(g, r, c):
    """göz kasası 1,0 · alt U + üst U · iki yanda TIG alın dikişi (y by+95) · dikmelere FHP-M4 (baş içeride gömme)"""
    cx = QX0 + GOZ_XL[c]; by = GOZ_TABAN[r]; ad = "goz_%d%d_kasasi" % (r, c)
    sa = g.sac(ad + "_alt", "kapak_ic", t=1.0, bolge="hijyen")
    ga = sa.R + sa.t
    Pa = sa.taban([(cx + ga, -GOZ_Z[1]), (cx + GOZ_W - ga, -GOZ_Z[1]), (cx + GOZ_W - ga, -GOZ_Z[0]), (cx + ga, -GOZ_Z[0])], O=(0, by, 0), ex=(1, 0, 0),
                  ey=(0, 0, -1), ad="taban")
    a_sag = Pa.flans(1, GOZ_H / 2.0 - 0.1, yon=+1, ad="sag_duvar"); a_sol = Pa.flans(3, GOZ_H / 2.0 - 0.1, yon=+1, ad="sol_duvar")
    su = g.sac(ad, "kapak_ic", t=1.0, bolge="hijyen")
    Pu = su.taban([(cx + ga, GOZ_Z[0]), (cx + GOZ_W - ga, GOZ_Z[0]), (cx + GOZ_W - ga, GOZ_Z[1]), (cx + ga, GOZ_Z[1])], O=(0, by + GOZ_H, 0), ex=(1, 0, 0),
                  ey=(0, 0, 1), ad="tavan")
    u_sag = Pu.flans(1, GOZ_H / 2.0 - 0.1, yon=+1, ad="sag_duvar"); u_sol = Pu.flans(3, GOZ_H / 2.0 - 0.1, yon=+1, ad="sol_duvar")
    g.not_("%s: alt U + üst U · iki yanda TIG alın dikişi (y %.0f, 440 mm, kök aralığı 0,2) · iç yüz taşlanır (ambalajlı ürün gözü, bindirme yok)" % (ad, by + 95.0))
    # FHP-M4: sol / sağ duvar · ön + arka dikme (z 722 / 1138) · alt U'da hh[0], üst U'da hh[1] · orta boşlukta (dikme 10 ↔ 20) iki sütunun somunları y'de kaydırılır
    for duvar, (Pa_, Pu_, x_dis, yon) in (("sol", (a_sol, u_sol, cx, (-1, 0, 0))), ("sag", (a_sag, u_sag, cx + GOZ_W, (1, 0, 0)))):
        hh = (70.0, 120.0) if (c == 1 and duvar == "sol") else (50.0, 140.0)
        for zz in ((DIKME_Z[0][0] + DIKME_Z[0][1]) / 2.0, (DIKME_Z[1][0] + DIKME_Z[1][1]) / 2.0):
            _fhp_paket(g, Pa_, (x_dis, by + hh[0], zz), yon, 10.0, "%s_alt_%s_%d" % (ad, duvar, int(zz)), dis="M4")
            _fhp_paket(g, Pu_, (x_dis, by + hh[1], zz), yon, 10.0, "%s_%s_%d" % (ad, duvar, int(zz)), dis="M4")
    return sa, su


def _goz_dikmesi(g, i, j):
    """göz dikmesi: AISI 304 lama 20 × 10 · 1200 (EN 10058) · uçlarda M5 diş 14 derin · kasa saplamaları Ø4,5"""
    (xa, xb), (za, zb) = DIKME_X[i], DIKME_Z[j]
    ad = "goz_dikmesi_%d%d" % (i, j)
    sh = kutu(xa, xb, ALT_RAF[1], UST_RAF[0], za, zb)
    xc, zc = (xa + xb) / 2.0, (za + zb) / 2.0
    sh = sh.cut(silindir((xc, ALT_RAF[1] - 1.0, zc), (0, 1, 0), 2.5, 15.0)).cut(silindir((xc, UST_RAF[0] + 1.0, zc), (0, -1, 0), 2.5, 15.0))
    delikler = 0
    for r in range(6):
        by = GOZ_TABAN[r]
        hh = (70.0, 120.0) if i == 2 else (50.0, 140.0)
        for h in hh:
            sh = sh.cut(silindir((xa - 1.0, by + h, zc), (1, 0, 0), 2.25, (xb - xa) + 2.0)); delikler += 1
    p = g.ozel(ad, sh.clean(), "EN 10058 lama 20 × 10 · AISI 304", "Göz dikmesi lama 20 × 10 · L 1200 · uçlarda M5 × 14 diş · %d × Ø4,5 (kasa saplamaları)" % delikler,
               "20 × 10 × 1200", uretim=True, mal="sac", tur="lama", meta=dict(tur="lama", L=1200.0, delik=delikler))
    g.eleman(p)
    g.eleman(S.vida("ISO7380", "M5", 12, (xc, ALT_RAF[0], zc), (0, 1, 0), ad=ad + "_vida_alt", birim=g.birim))
    g.eleman(S.vida("ISO7380", "M5", 12, (xc, UST_RAF[1], zc), (0, -1, 0), ad=ad + "_vida_ust", birim=g.birim))
    return p


def kur_qr(log=print):
    g = GO.Govde(BIRIM_QR, SURUM, istasyon="QR", cerceve=GO.Cerceve("QR"))
    t0 = time.time()
    yl, yr = _yan(g, "sol"), _yan(g, "sag")
    tb = _taban(g)
    gr = _goz_robot(g)
    mu = _musteri(g)
    ar = _raf(g, "alt_raf_3", ALT_RAF[0], True)
    ur = _raf(g, "ust_raf_3", UST_RAF[0], False)
    tv = _tavan(g)
    cit = {}
    for ad, tr, y0, y1 in (("servis_cercevesi_alt_sol", "sol", PANEL_ALT_Y[0], 405.0), ("servis_cercevesi_alt_sag", "sag", CENTIK["y"] + 4.0, 440.0),
                           ("servis_cercevesi_ust_sol", "sol", 1660.0, 2022.0), ("servis_cercevesi_ust_sag", "sag", 1660.0, 2022.0)):
        cit[ad] = _cita(g, ad, tr, y0, y1)
    pa = _servis_panel(g, "servis_kapagi_alt_sac", PANEL_ALT_Y[0], PANEL_ALT_Y[1], True)
    pu = _servis_panel(g, "servis_kapagi_ust", PANEL_UST_Y[0], PANEL_UST_Y[1], False)
    for i, (xk, yk, yon, cap) in enumerate(KILIT["alt"]):
        _kilit(g, "servis_kilidi_alt" + ("" if i == 1 else "_%d" % i), xk, yk, yon, cap)
    for i, (xk, yk, yon) in enumerate(KILIT["ust"]):
        _kilit(g, "servis_kilidi_ust" + ("" if i == 3 else "_%d" % i), xk, yk, yon, 18.0)
    # ---- BİRLEŞİMLER ----
    for taraf, Y, xs in (("sol", yl, XL - 1.5), ("sag", yr, XR + 1.5)):
        # göz sacı yan dönüşü (z 684) · 7 FHP
        for y in (480.0, 660.0, 860.0, 1060.0, 1260.0, 1460.0, 1620.0):
            _fhp(g, Y, G.P["goz_robot_" + taraf], (xs, y, 684.0), "govde_bag_goz_robot_%s_%d" % (taraf, int(y)))
        # müşteri yüzü yan dönüşü (z 1176) · 11 FHP
        for y in MUSTERI_YAN_Y:
            _fhp(g, Y, G.P["musteri_" + taraf], (xs, float(y), 1176.0), "govde_bag_musteri_%s_%d" % (taraf, int(y)))
        # raflar (yan dönüşler) · 3 + 3 FHP
        for z in (760.0, 930.0, 1100.0):
            _fhp(g, Y, G.P["alt_raf_3_" + taraf], (xs, 430.5, z), "govde_bag_alt_raf_%s_%d" % (taraf, int(z)))
            _fhp(g, Y, G.P["ust_raf_3_" + taraf], (xs, 1633.5, z), "govde_bag_ust_raf_%s_%d" % (taraf, int(z)))
        # tavan yan dönüşü · 3 FHP
        for z in (720.0, 940.0, 1140.0):
            _fhp(g, Y, G.P["tavan_" + taraf], (xs, 2034.0, z), "govde_bag_tavan_%s_%d" % (taraf, int(z)))
        # çerçeve çıtaları (bacak z 688) · ≤ 150 aralık
        for ad in [a for a in cit if a.endswith(taraf)]:
            P_, f_ = cit[ad]
            ys = [p_[1] for p_ in P_.poly]; y0, y1 = min(ys), max(ys)
            for y in GO.vida_konumlari(y0, y1, maks=150.0, uc=30.0):
                _fhp(g, Y, f_, (xs, y, 688.0), "govde_bag_%s_%d" % (ad.replace("servis_cercevesi_", "cerceve_"), int(y)))
    # taban kulakları (3 mm L · tabana kaynaklı · yan saca FHP)
    for z in KULAK_SOL_Z:
        GO.kulak(g, "govde_kulak_taban_sol_%d" % int(z), yl, (XL, 40.0, z), (0, 0, 1.0), (0, -1.0, 0), 40.0 - YT1, L_kaynak=20.0)
    for z in KULAK_SAG_Z:
        GO.kulak(g, "govde_kulak_taban_sag_%d" % int(z), yr, (XR, 40.0, z), (0, 0, -1.0), (0, -1.0, 0), 40.0 - YT1, L_kaynak=20.0)
    # müşteri yüzü alt dönüşü ↔ taban (alttan ISO 7380 → PEM SP-M5) · tavan ↔ müşteri üst dönüşü (tavandan FHP aşağı)
    for x in (4640.0, 4830.0, 5000.0, 5170.0, 5360.0):
        _pem(g, tb, G.P["musteri_alt"], (x, YT0, 1176.0), "govde_bag_musteri_taban_%d" % int(x))
        _fhp(g, tv, G.P["musteri_ust"], (x, YTOP, 1176.0), "govde_bag_tavan_musteri_%d" % int(x))
    # alt raf ↔ göz sacı alt dönüşü (raf üstünden ISO 7380 M5 → dönüşte PEM SP-M5) · göz sacı üst dönüşü ↔ üst raf (ISO 7380 M6 → rafta PEM SP-M6)
    for x in (4640.0, 4810.0, 4990.0, 5170.0, 5350.0):
        _pem(g, ar, G.P["goz_robot_alt"], (x, ALT_RAF[1], 684.0), "govde_bag_alt_raf_goz_%d" % int(x))
    for x in (4630.0, 4760.0, 4870.0, 5000.0, 5130.0, 5245.0, 5360.0):
        _pem(g, G.P["goz_robot_ust"], ur, (x, G_UST_Y, 693.0), "govde_bag_ust_raf_goz_%d" % int(x), dis="M6")
    # ayaklar
    for i, (x, z) in enumerate(AYAK_XZ): _ayak_qr(g, i, x, z)
    # GÖZLER (birim QR_GOZLER: kasa + dikme + bağlantıları)
    for r in range(6):
        for c in range(2): _goz_kasasi(g, r, c)
    for i in range(4):
        for j in range(2): _goz_dikmesi(g, i, j)
    g.not_("servis panelleri: menteşesiz kaldır-çıkar (koridor 591 · yer rayı z 240–480 · makine önü z 79 → dikey eksenli kapak açılamaz) · alt panel 3 dille "
           "taban çentiklerine, üstü 2 çeyrek dönüş kilitle · üst panel 4 kilitle")
    g.not_("ayak: SPEC taban 17 sabit → alçak profil M10 (kararlar M12 Ø60 SAPMA) · kaynak somunu plaka ALTINDA (iç hacimde robot kontrol kutusu 3,5 mm geride)")
    G.q = g
    log("%s · QR kuruldu: %d sac · %d eleman · %d kaynak · %d birleşim · %.1f sn" % (SURUM, len(g.SAC), len(g.ELEMAN), len(g.KAYNAK), len(g.BIRLESIM), time.time() - t0))
    return g


# =====================================================================================================================================
# 2 · PERSONEL TEZGÂHI (TEZGAH_GOVDE + TEZGAH_CEKMECE) · panel kutu, kendinden taşıyıcı · DÜNYA
# =====================================================================================================================================
TZ_S, TZ_K = 1044.0, 1874.0                    # ince duvar tarafı dış · sokak tarafı dış
TZ_S_IC, TZ_K_IC = 1045.2, 1872.8              # iç yüzler (1,2)
TX_AI = TX_ARKA - TT                           # 4503,8 · arka panel iç yüzü
TX_DIK = (3876.5, 3906.5)                      # kapak dikmeleri x (gövde ön düzleminin 1,5 gerisi: menteşe kanat plakası arada)
TZ_DIK = dict(sokak=1853.4, bolme=1534.0)      # menteşe dikmesi merkezi (kapak kenarı − 18: menteşe penceresi düz yüzde, gövde iç köşe R'sinden uzak) · bas-aç dikmesi (kapak kenarı + 16, ayırma panelinden 2,6 açık, kulaklarla)
TY_DIK = dict(sokak=(135.0, 745.0), bolme=(420.0, 745.0))   # hazne (y ≥ 749) altında · taban tavası dönüşü (≤ 130) / bidon kapakları (≤ 405) üstünde
TX_UST_FL = 4479.0                             # yan / ayırma üst dönüşü bitişi (arka panelin üst dönüşü x 4480–4503,8)
TY_KUSAK = (680.0, 896.8)                      # ince duvar üst kuşağı (duvar köşebendinin altı)
Z_INCE = 1039.0                                # ince duvarın ön zon yüzü (dükkân v15)
TY_KOSEBENT = (855.8, 896.8, 898.8)            # duvar köşebendi 2 mm: dikey ayak altı · yatay ayak altı · üstü (= tabla altı)
TX_KOSEBENT = (3895.0, 4475.0)
TAYAK_M12 = [(3905.0, 1546.4), (3905.0, 1842.8), (4473.8, 1546.4), (4473.8, 1842.8)]   # evye dolabı ayakları (mevcut noktalar)
TX_PLINT = 3940.0                              # plint yüzü (Ø60 hijyenik ayaklar 3875–3935 → plint 65 geride)
TY_RAF_ALT = TY_RAF = 716.0
HAZNE_DIS = (3889.0, 4191.0, 1543.6, 1845.6)   # hazne dış ölçüsü (tabla ağzı)
CEK_TAB = (725.0, 830.0)                       # çekmece kutusu taban altı · üst
KAM = dict(y=846.0, z=1280.0, cap=20.0)        # kam kilit silindiri Ø19,5 → Ø20 delik
TZ_ONEK = ("ayar_ayagi_", "ayak_", "arka_", "plint", "yan_sokak", "ayirma_paneli", "evye_dolabi_tabani", "ust_yan_kusak_ince", "duvar_kosebendi_ince",
           "tabla_", "on_kapak", "kapak_", "bulasik_ust_rafi", "cekmece_", "govde_")


def _dl(P, p, cap, tip, parca):
    """dünya noktasından panele delik"""
    uv = P.yerel(p)
    return P.delik(float(uv[0]), float(uv[1]), cap, tip=tip, parca=parca)


def _cd(g, x, z, katlar, ad, not_=""):
    """CD kaynak saplaması M5 (ISO 13918 · A2) tablanın ALT yüzüne kaynaklı (tabla üstünde iz yok) → altındaki sac(lar)da Ø7 geçiş (saplama kaynak
    flanşı Ø6,5) + DIN 9021 + ISO 10511 altta · katlar: [Panel] yukarıdan aşağı (tabla altından itibaren üst üste)"""
    y0 = TY_UST; yk = y0
    for P in katlar:
        _dl(P, (x, yk - P.sac.t / 2.0, z), 7.0, "vida_deligi", "CD M5 saplama geçişi Ø7 (kaynak flanşı Ø6,5)")
        yk -= P.sac.t
    hp = S.DIN9021["M5"][2]; m = S.ISO10511["M5"][1]
    L = S._boy_sec((y0 - yk) + hp + m + 1.5, [10, 12, 16, 20, 25])
    sh = silindir((x, y0, z), (0, -1, 0), 2.47, L).fuse(silindir((x, y0, z), (0, -1, 0), 3.25, 0.8)).clean()
    g.eleman(g.ozel(ad + "_saplama", sh, "ISO 13918 (CD, tip PT) · A2", "CD kaynak saplaması M5 × %g · tabla altına kondansatör deşarjlı kaynak (tabla üstünde iz yok)" % L,
                    "M5 × %g · flanş Ø6,5" % L, malzeme="A2 (1.4301)", mal="celik"))
    g.eleman(S.pul("DIN9021", "M5", (x, yk, z), (0, -1, 0), ad=ad + "_pul", birim=g.birim))
    g.eleman(S.somun("ISO10511", "M5", (x, yk - hp, z), (0, -1, 0), ad=ad + "_somun", birim=g.birim))
    g.BIRLESIM.append(dict(ad=ad, tip="cd_saplama", dis="M5", nokta=[x, y0, z], paket=round(y0 - yk, 2), sac=["tabla_30"] + [P.sac.ad for P in katlar],
                           parcalar=[], not_=not_))


def _tz_yan(g, ad, z_ic, yon, ust_tam=False, alt=TY_PL):
    """dikey gövde paneli 1,2 (yan_sokak / ayirma_paneli / ust_yan_kusak_ince) · x 3875–4503,8 · dönüşler yon (+1: +z · −1: −z) tarafına:
    arka dönüş 25 (arka panele ISO 7380 ↔ PEM SP-M5) + üst dönüş 25 (tabla CD saplamaları) · ön kenar düz (kapak / çekmece önünün arkasında)"""
    s = g.sac(ad, "ic"); gg = s.R + s.t
    y1 = (TY_KUSAK[1] if ad == "ust_yan_kusak_ince" else TY_UST)
    poly = [(TX_GOV, alt), (TX_AI - gg, alt), (TX_AI - gg, y1 - gg), (TX_GOV, y1 - gg)]
    z0 = z_ic if yon < 0 else z_ic - s.t                                  # n = +z · sac z0 … z0 + t
    P = s.taban(poly, O=(0, 0, z0), ex=(1, 0, 0), ey=(0, 1, 0), ad="panel")
    fa = P.flans(1, 25.0, yon=yon, bas=0.0 if ust_tam else 31.0, ad="arka_donus")       # yan / ayırma: taban tavasının arka dönüşü (y 100–130) altta tam boy
    if ust_tam:
        fu = P.flans(2, 25.0, yon=yon, ad="ust_donus"); s.kose(fa, fu, "acik")
    else:
        fu = P.flans(2, 25.0, yon=yon, bas=(TX_AI - gg) - TX_UST_FL, ad="ust_donus")     # arka panelin üst dönüşüne kadar
    G.P.update({ad: P, ad + "_arka": fa, ad + "_ust": fu})
    return P


def _tz_ayak(g, i, x, z):
    """hijyenik ayarlı ayak M12 Ø60 (GN 20 sınıfı) · kör burç Ø30 × 30 (304 torna, kaynaklı) · 3 mm takviye plakası taban tavasının ALTINA kaynaklı"""
    a = 30.0; y_pl = TY_PL - 3.0
    s = g.sac("ayak_plakasi_%d" % i, "braket", t=3.0)
    s.taban([(x - a, -(z + a)), (x + a, -(z + a)), (x + a, -(z - a)), (x - a, -(z - a))], O=(0, y_pl, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="plaka")
    _kaynak4(g, "ayak_plakasi_%d_kaynak" % i, x - a, x + a, TY_PL, z - a, z + a, ust_yon=(0, -1.0, 0), a=2.0, not_="ayak plakası ↔ taban tavası (alttan, köşe)")
    g.eleman(S.kor_burc("M12", (x, y_pl, z), (0, -1, 0), ad="ayak_burcu_%d" % i, birim=g.birim))
    g.kaynak(S.kaynak_halka((x, y_pl, z), (0, -1, 0), 15.0, 2.0, ad="ayak_burcu_%d_kaynak" % i, birim=g.birim))
    for q in S.ayarli_ayak("M12", (x, 0.0, z), (0, 1, 0), y_pl - 30.0, ad="ayar_ayagi_%d" % i, birim=g.birim): g.eleman(q)


def _tz_kapak_dikmesi(g, ad, kenar):
    """kapak dikmesi 304 kare boru 30 × 30 × 2 (menteşe / bas-aç gövdesi içinde) · iki uç tapa · panele 2 × 3 mm L kulak (FHP + pul + fiberli somun)"""
    y0, y1 = TY_DIK[kenar]
    d = g.profil(ad, "y", y0, y1, ((TX_DIK[0] + TX_DIK[1]) / 2.0, TZ_DIK[kenar]), b=30.0, t=2.0,
                 not_="kapak %s dikmesi 30 × 30 × 2 (hazne altında biter · y %.0f–%.0f)" % ("menteşe" if kenar == "sokak" else "bas-aç", y0, y1))
    GO.dikme_tapasi(g, d, "ust", ad=ad + "_tapa_ust"); GO.dikme_tapasi(g, d, "alt", ad=ad + "_tapa_alt")
    A = G.P["yan_sokak"] if kenar == "sokak" else G.P["ayirma_paneli"]
    z_ic = TZ_K_IC if kenar == "sokak" else TZ_BOL[1]
    u = (0, -1.0, 0) if kenar == "sokak" else (0, 1.0, 0)                       # u × v = panelden UZAĞA (dolap içine)
    vc = 18.0
    for y in ((y0 + 45.0, y1 - 45.0)):
        GO.kulak(g, "govde_kulak_%s_dikme_%d" % (kenar, int(y)), A, (TX_DIK[1] + vc, y, z_ic), u, (-1.0, 0, 0), vc, L_kaynak=24.0)
    return d


def _tz_omega(g, ad, zc):
    """tabla altı omega takviye 1,0 (40 × 20, ayaklar 12) · MS polimer yapıştırma + ses yalıtım bandı (bağlantı elemanı YOK)"""
    s = g.sac(ad, "ic", t=1.0); gg = s.R + s.t
    b, h = 40.0, 20.0
    P = s.taban([(3870.0, -(zc + b / 2.0) + gg), (4470.0, -(zc + b / 2.0) + gg), (4470.0, -(zc - b / 2.0) - gg), (3870.0, -(zc - b / 2.0) - gg)],
                O=(0, TY_UST - h, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="sirt")
    w1 = P.flans(0, h, yon=+1, ad="gov_a"); w2 = P.flans(2, h, yon=+1, ad="gov_b")
    w1.flans(1, 12.0, yon=-1, ad="ayak_a"); w2.flans(1, 12.0, yon=-1, ad="ayak_b")
    return s


def kur_tz(log=print):
    g = GO.Govde(BIRIM_TZ, SURUM, istasyon="TEZGAH", cerceve=GO.Cerceve("TZ"))
    t0 = time.time()
    # ---- dikey paneller
    ys = _tz_yan(g, "yan_sokak", TZ_K_IC, -1)
    ya = _tz_yan(g, "ayirma_paneli", TZ_BOL[1], +1)
    yk = _tz_yan(g, "ust_yan_kusak_ince", TZ_S_IC, +1, ust_tam=True, alt=TY_KUSAK[0])
    # ---- arka panel (niş duvarına · bulaşık bağlantı penceresi alttan açık · sifon / su / priz delikleri)
    s = g.sac("arka_panel", "ic"); gg = s.R + s.t
    ap = s.taban([(-TZ_K, TY_PL), (-TZ_S, TY_PL), (-TZ_S, TY_UST - gg), (-TZ_K, TY_UST - gg)], O=(TX_AI, 0, 0), ex=(0, 0, -1), ey=(0, 1, 0), ad="arka")
    ap_u = ap.flans(2, 25.0, yon=-1, ad="ust_donus")
    ap.kesik([(-1380.0, TY_PL - 5.0), (-1075.0, TY_PL - 5.0), (-1075.0, 250.0), (-1380.0, 250.0)], tip="baglanti_penceresi", dfm=False,
             parca="bulaşık hortum / kablo penceresi 305 × 150 (alttan açık)")
    ap.delik(-1694.6, 640.0, 48.0, tip="sifon_cikisi", parca="sifon çıkışı Ø40 + pay")
    ap.delik(-1600.0, 450.0, 24.0, tip="su_girisi", parca="soğuk su ½\"")
    ap.delik(-1800.0, 800.0, 24.0, tip="kablo_gecisi", parca="priz kablosu")
    G.P.update(arka_panel=ap, arka_panel_ust=ap_u)
    # ---- evye dolabı tabanı: sızdırmaz tava (4 dönüş 30 yukarı · köşeler açık + TIG, taşlanır)
    s = g.sac("evye_dolabi_tabani", "ic"); gg = s.R + s.t
    tb = s.taban([(TX_GOV + gg, -(TZ_K_IC - gg)), (TX_AI - gg, -(TZ_K_IC - gg)), (TX_AI - gg, -(TZ_BOL[1] + gg)), (TX_GOV + gg, -(TZ_BOL[1] + gg))],
                 O=(0, TY_PL, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    tf = [tb.flans(i, 30.0, yon=+1, ad=a) for i, a in enumerate(("sokak_donus", "arka_donus", "bolme_donus", "on_donus"))]
    for i in range(4): s.kose(tf[i], tf[(i + 1) % 4], "acik", kaynak=True)
    G.P.update(taban=tb, taban_sokak=tf[0], taban_arka=tf[1], taban_bolme=tf[2])
    # ---- tabla: 1,2 tek sac · önde 30 önlük + 15 J · arka + iki yan 100 etek · bütün iç köşeler R 3 (ıslak bölge) · arka köşeler açık + TIG + taşlama
    s = g.sac("tabla_30", "ic", R=3.0, bolge="gida"); gg = s.R + s.t
    tl = s.taban([(TX_TABLA + gg, -TZ_K + gg), (TX_ARKA - gg, -TZ_K + gg), (TX_ARKA - gg, -TZ_S - gg), (TX_TABLA + gg, -TZ_S - gg)],
                 O=(0, TY_UST, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tabla")
    e_s = tl.flans(0, TY_ETEK - TY_UST, yon=+1, ad="etek_sokak")
    e_a = tl.flans(1, TY_ETEK - TY_UST, yon=+1, ad="etek_arka")
    e_i = tl.flans(2, TY_ETEK - TY_UST, yon=+1, ad="etek_ince")
    onl = tl.flans(3, TY_TABLA - 870.0, yon=-1, bas=15.0, son=15.0, ad="onluk")       # yan eteklerin büküm bölgesinden 15 içeride biter: önlük kalıbı etekler arasına girer
    s.kose(e_s, e_a, "acik", kaynak=True); s.kose(e_a, e_i, "acik", kaynak=True)
    # J dönüşü YOK: önlük 30'un ucundaki 15 J düz bıçakla bükülemiyor (tabla bıçağa çarpar, kaz boynu bıçak gerekir · DFM) → alt kenar çapak + kenar kırma 0,5
    tl.dikdortgen((HAZNE_DIS[0] + HAZNE_DIS[1]) / 2.0, -(HAZNE_DIS[2] + HAZNE_DIS[3]) / 2.0, HAZNE_DIS[1] - HAZNE_DIS[0], HAZNE_DIS[3] - HAZNE_DIS[2],
                  tip="hazne_agzi", parca="el yıkama haznesi ağzı 302 × 302 (hazne dış ölçüsü · alın TIG + taşlama)")
    tl.delik(BATARYA[0], -BATARYA[1], BATARYA[2], tip="batarya_deligi", parca="GROHE 36271000 Ø34")
    _kaynak4(g, "tabla_hazne_kaynak", HAZNE_DIS[0], HAZNE_DIS[1], TY_UST, HAZNE_DIS[2], HAZNE_DIS[3], ust_yon=(0, -1.0, 0), a=1.5,
             not_="hazne ↔ tabla: üstten alın TIG (taşlanır, sızdırmaz) + alttan köşe dikişi")
    G.P.update(tabla=tl)
    for i, zc in enumerate((1200.0, 1360.0)): _tz_omega(g, "tabla_omega_%d" % i, zc)
    # ---- duvar köşebendi (ince duvar · 2 mm L · tablayı ve kuşağı taşır · 3 dübel · dikey ayak kuşağın 2 gerisinde: bombe baş 2,75 sığar)
    s = g.sac("duvar_kosebendi_ince", "braket", t=2.0); gg = s.R + s.t
    kb = s.taban([(TX_KOSEBENT[0], -(TZ_S_IC + 23.8)), (TX_KOSEBENT[1], -(TZ_S_IC + 23.8)), (TX_KOSEBENT[1], -(Z_INCE + gg)), (TX_KOSEBENT[0], -(Z_INCE + gg))],
                 O=(0, TY_KOSEBENT[1], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="yatay")
    kd = kb.flans(2, TY_KOSEBENT[2] - TY_KOSEBENT[0], yon=-1, ad="dikey")
    for j, x in enumerate((3940.0, 4185.0, 4430.0)):
        _dl(kd, (x, 872.0, Z_INCE + 1.0), 5.5, "dubel_deligi", "duvar dübeli (Ø6 dübel · 5 mm vida)")
        vd = S.vida("ISO7380", "M5", 45, (x, 872.0, Z_INCE + 2.0), (0, 0, -1.0), ad="arayuz_duvar_dubel_%d" % j, birim=g.birim)
        g.arayuz(vd, "BİNA · ince duvar (z 1039)", "Ø6 dübel deliği 50 derin (Fischer SX 6 sınıfı) · köşebent dikey ayağından", "temsili: Ø6 dübel + 5 × 45 A2 bombe başlı")
    G.P.update(kosebent=kb, kosebent_dikey=kd)
    # ---- kapak dikmeleri
    dm = _tz_kapak_dikmesi(g, "kapak_dikmesi_sokak", "sokak")
    db = _tz_kapak_dikmesi(g, "kapak_dikmesi_bolme", "bolme")
    # ---- bulaşık üstü ayırma rafı (tava, yanlar 25 aşağı, ön 12 aşağı)
    s = g.sac("bulasik_ust_rafi", "ic"); gg = s.R + s.t
    rf = s.taban([(TX_GOV + gg, -TZ_BOL[0] + gg), (4500.0, -TZ_BOL[0] + gg), (4500.0, -TZ_S_IC - gg), (TX_GOV + gg, -TZ_S_IC - gg)],
                 O=(0, TY_RAF, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="raf")
    r_b = rf.flans(0, 25.0, yon=-1, ad="bolme_donus"); r_i = rf.flans(2, 25.0, yon=-1, ad="ince_donus"); r_o = rf.flans(3, 12.0, yon=-1, ad="on_donus")
    s.kose(r_i, r_o, "acik"); s.kose(r_o, r_b, "acik")
    # ---- ayaklar + plint + arka ayak köşebendi
    for i, (x, z) in enumerate(TAYAK_M12): _tz_ayak(g, i, x, z)
    s = g.sac("arka_ayak_kosebendi", "braket", t=3.0); gg = s.R + s.t
    ak = s.taban([(4459.0, -1086.0), (TX_AI - gg, -1086.0), (TX_AI - gg, -1046.0), (4459.0, -1046.0)], O=(0, TY_PL - 3.0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="yatay")
    akd = ak.flans(1, 73.0, yon=+1, ad="dikey")
    g.eleman(S.kor_burc("M12", (TAYAK4[0], TY_PL - 3.0, TAYAK4[1]), (0, -1, 0), ad="ayak_burcu_4", birim=g.birim))
    g.kaynak(S.kaynak_halka((TAYAK4[0], TY_PL - 3.0, TAYAK4[1]), (0, -1, 0), 15.0, 2.0, ad="ayak_burcu_4_kaynak", birim=g.birim))
    for q in S.ayarli_ayak("M12", (TAYAK4[0], 0.0, TAYAK4[1]), (0, 1, 0), TY_PL - 33.0, D_taban=40.0, ad="ayar_ayagi_4", birim=g.birim): g.eleman(q)
    s = g.sac("plint", "ic"); gg = s.R + s.t
    pl = s.taban([(-1870.8, 3.0), (-1518.4, 3.0), (-1518.4, TY_PL - gg), (-1870.8, TY_PL - gg)], O=(TX_PLINT, 0, 0), ex=(0, 0, -1), ey=(0, 1, 0), ad="yuz")
    pl_u = pl.flans(2, 20.0, yon=+1, ad="ust_donus")
    # ---- BİRLEŞİMLER
    # tabla ↔ gövde: CD saplamalar (yan / ayırma / arka üst dönüşleri · kuşak üst dönüşü + duvar köşebendi)
    for x in (3900.0, 4090.0, 4280.0, 4460.0):
        _cd(g, x, 1859.0, [G.P["yan_sokak_ust"]], "govde_bag_tabla_sokak_%d" % int(x))
        _cd(g, x, 1530.0, [G.P["ayirma_paneli_ust"]], "govde_bag_tabla_bolme_%d" % int(x))
    for x in (3910.0, 4100.0, 4290.0, 4460.0):
        _cd(g, x, 1058.0, [kb, G.P["ust_yan_kusak_ince_ust"]], "govde_bag_tabla_ince_%d" % int(x))
    for z in (1080.0, 1270.0, 1460.0, 1620.0, 1800.0):
        _cd(g, 4490.0, z, [ap_u], "govde_bag_tabla_arka_%d" % int(z))
    # yan / ayırma / kuşak arka dönüşleri ↔ arka panel (ISO 7380 dışarıdan · niş duvarına bakan yüz) → PEM SP-M5
    for ad, z, ys_ in (("yan_sokak", 1859.0, GO.vida_konumlari(TY_PL, TY_UST - 3.0, maks=200.0, uc=40.0)),
                       ("ayirma_paneli", 1528.0, GO.vida_konumlari(TY_PL, TY_UST - 3.0, maks=200.0, uc=40.0)),
                       ("ust_yan_kusak_ince", 1057.0, (720.0, 870.0))):
        for y in ys_:
            _pem(g, ap, G.P[ad + "_arka"], (TX_ARKA, y, z), "govde_bag_arka_%s_%d" % (ad.split("_")[0] if ad != "ust_yan_kusak_ince" else "kusak", int(y)))
    # taban tavası dönüşleri ↔ yan / ayırma / arka (FHP panelde, baş dış yüzde gömme · somun dolap içinde)
    for x in (3920.0, 4110.0, 4300.0, 4470.0):
        _fhp(g, ys, tf[0], (x, TY_PL + 16.0, TZ_K), "govde_bag_taban_sokak_%d" % int(x))
        _fhp(g, ya, tf[2], (x, TY_PL + 16.0, TZ_BOL[0]), "govde_bag_taban_bolme_%d" % int(x))
    for z in (1560.0, 1700.0, 1840.0):
        _fhp(g, ap, tf[1], (TX_ARKA, TY_PL + 16.0, z), "govde_bag_taban_arka_%d" % int(z))
    # raf ↔ kuşak / ayırma (FHP panelde · somun bulaşık tarafında)
    for x in (3950.0, 4190.0, 4430.0):
        _fhp(g, yk, r_i, (x, 706.0, TZ_S), "govde_bag_raf_ince_%d" % int(x))
        _fhp(g, ya, r_b, (x, 706.0, TZ_BOL[1]), "govde_bag_raf_bolme_%d" % int(x))
    # plint ↔ taban (FHP tavada · somun altta)
    for z in (1600.0, 1790.0):
        _fhp(g, tb, pl_u, (3952.0, TY_PL + 1.2, z), "govde_bag_plint_%d" % int(z))
    # arka ayak köşebendi ↔ arka panel
    for y in (125.0, 150.0):                                                             # bulaşık penceresi (z ≥ 1075) dışında, tek sıra dikey
        _fhp(g, ap, akd, (TX_ARKA, y, 1060.0), "govde_bag_arka_ayak_%d" % int(y))
    # teleskopik ray vida delikleri (ray cihaz · vidaları rayla gelir) · ani su ısıtıcısı askı delikleri
    for x in (3900.0, 4126.0, 4352.0):
        _dl(yk, (x, 782.5, TZ_S_IC - 0.6), 5.5, "ray_deligi", "teleskopik ray M5 (ray ile gelir)")
        _dl(ya, (x, 782.5, TZ_BOL[0] + 0.6), 5.5, "ray_deligi", "teleskopik ray M5 (ray ile gelir)")
    for x in (4300.0, 4450.0):
        _dl(ya, (x, 690.0, TZ_BOL[0] + 0.6), 6.5, "aski_deligi", "EIL 3 Premium askı vidası (cihazla gelir)")
    # ---- EVYE DOLABI KAPAĞI: çift cidar 18 · gizli 180° menteşe (sokak dikmesinde) · bas-aç (ayırma dikmesinde) · KULP YOK
    K = GO.kapak(g, "on_kapak", KAPAK_T["u"][0], KAPAK_T["u"][1], KAPAK_T["v"][0], KAPAK_T["v"][1], TX_GOV - TX_ON, 0.0, O=(TX_GOV, 0, 0), ex=(0, 0, 1.0),
                 ey=(0, 1.0, 0), ustte="yatay", punta_aralik=150.0)
    GO.gizli_mentese(g, K, dm, "sag", (200.0, 640.0))
    GO.bas_ac(g, K, db, "sol", (600.0,), a=18.0)          # karşılık plakası iç tavanın düz alanında (a 6–30)
    # ---- ÇEKMECE (birim TEZGAH_CEKMECE): önü çift cidar 18 · kutu tek sac tava 105 (köşeler TIG, sızdırmaz) · kam kilit karşılığı · bas-aç arkada
    KC_ = GO.kapak(g, "cekmece_onu", CEKMECE_ON["u"][0], CEKMECE_ON["u"][1], CEKMECE_ON["v"][0], CEKMECE_ON["v"][1], TX_GOV - TX_ON, 0.0, O=(TX_GOV, 0, 0),
                   ex=(0, 0, 1.0), ey=(0, 1.0, 0), ustte="yatay", punta_aralik=150.0)
    for P_ in (KC_.D, KC_.I):
        P_.delik(KAM["z"], KAM["y"], KAM["cap"], tip="kam_kilit_deligi", parca="kam kilit Ø19,5 (cihaz)")
    s = g.sac("cekmece_kutu_tabani", "ic"); gg = s.R + s.t
    x0, x1, z0, z1 = CEK_KUTU["x"][0], CEK_KUTU["x"][1], CEK_KUTU["z"][0], CEK_KUTU["z"][1]
    ck = s.taban([(x0 + gg, -z1 + gg), (x1 - gg, -z1 + gg), (x1 - gg, -z0 - gg), (x0 + gg, -z0 - gg)], O=(0, CEK_TAB[0], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    cf = [ck.flans(i, CEK_TAB[1] - CEK_TAB[0], yon=+1, ad=a) for i, a in enumerate(("bolme_yani", "arka", "ince_yani", "on"))]
    for i in range(4): s.kose(cf[i], cf[(i + 1) % 4], "acik", kaynak=True)
    for x in (3900.0, 4126.0, 4352.0):
        _dl(cf[2], (x, 782.5, z0 + 0.6), 5.5, "ray_deligi", "teleskopik ray iç eleman M5 (ray ile gelir)")
        _dl(cf[0], (x, 782.5, z1 - 0.6), 5.5, "ray_deligi", "teleskopik ray iç eleman M5 (ray ile gelir)")
    for y in (760.0, 805.0):
        for z in (1150.0, 1410.0):
            _pem(g, cf[3], KC_.I, (x0 + 0.6, y, z), "govde_bag_cekmece_onu_%d_%d" % (int(y), int(z)))
    # kam kilit karşılığı (tabla altına 2 CD · dudak çekmece önünün 0,5 gerisinde, dil kilitliyken arkasında)
    s = g.sac("cekmece_kilit_karsiligi", "braket", t=1.5); gg = s.R + s.t
    kk = s.taban([(-1300.0, 860.0), (-1260.0, 860.0), (-1260.0, TY_UST - gg), (-1300.0, TY_UST - gg)], O=(TX_GOV + 0.5, 0, 0), ex=(0, 0, -1), ey=(0, 1, 0), ad="dudak")
    kku = kk.flans(2, 21.5, yon=+1, ad="ust_donus")
    for z in (1270.0, 1290.0):
        _cd(g, 3888.0, z, [kku], "govde_bag_tabla_kilit_%d" % int(z))
    # bas-aç (çekmece arkası): gövde Ø12 braketin Ø12,2 deliğinde, uç kutunun arka duvarına · braket ayırma paneline 2 FHP
    s = g.sac("cekmece_basac_braketi", "braket", t=1.5); gg = s.R + s.t
    xb = 4400.0
    bb_ = s.taban([(-(TZ_BOL[0] - gg), 760.0), (-1478.0, 760.0), (-1478.0, 805.0), (-(TZ_BOL[0] - gg), 805.0)], O=(xb, 0, 0), ex=(0, 0, -1), ey=(0, 1, 0), ad="plaka")
    bbf = bb_.flans(3, 22.0, yon=+1, ad="ayak")
    yb_, zb_ = 782.5, 1490.0
    bb_.delik(-zb_, yb_, GO.BASAC["delik_cap"], tip="basac_deligi", parca="bas-aç gövdesi (geçme)")
    m = GO.BASAC
    sh = silindir((xb, yb_, zb_), (1, 0, 0), m["govde_cap"] / 2.0, m["govde_boy"]).fuse(silindir((xb, yb_, zb_), (-1, 0, 0), m["bas_cap"] / 2.0, m["bas_h"])) \
        .fuse(silindir((xb - m["bas_h"], yb_, zb_), (-1, 0, 0), m["uc_cap"] / 2.0, xb - m["bas_h"] - x1))
    g.eleman(g.ozel("cekmece_basac", sh.clean(), m["sinif"], "Bas-aç mandalı (push-to-open, geçme gövde Ø12) · çekmece arka duvarına uç · kam kilitle kilitli",
                    "Ø12 × 26 · baş Ø14 · uç Ø6 × %.0f · strok 7" % (xb - m["bas_h"] - x1), malzeme=m["malzeme"], mal="siyah"))
    for y in (770.0, 795.0):
        _fhp(g, ya, bbf, (xb + 12.0, y, TZ_BOL[1]), "govde_bag_cekmece_basac_%d" % int(y))
    g.not_("tabla: 1,2 tek sac (eski 30 mm dolu blok + 3 etek → tek parça; önlük 30, J dönüşü yok — kaz boynu bıçak isterdi) · iç köşeler R 3 · arka köşeler açık + TIG + taşlama (sızdırmaz) · ön köşelerde etek ile "
           "önlük ters yönde → köşe 4,2 × 4,2 TIG dolgu + taşlama · tablaya hiçbir bağlantı elemanı üstten girmez (CD saplamalar alttan)")
    g.not_("kapak + çekmece önü: çift cidar 1,5 + 1,0 (eski 18 mm dolu blok) · KULP YOK (eski çubuk kulplar kalktı): kapak bas-aç, çekmece arkada bas-aç + kam kilit")
    g.not_("ayak: evye dolabı 4 × hijyenik M12 Ø60 (kararlar) · arka sol köşe Ø40 (duvar + bulaşık ayağı arasında Ø60 sığmıyor: SAPMA) · plint 65 geride (Ø60 ayak)")
    g.not_("bina: tabla etekleri + yanlar duvarlara 5 mm gıda sınıfı silikon (sökülebilir derz) · ince duvar köşebendi 3 dübel · niş duvarına bağlantı yok (arka panel serbest)")
    G.t = g
    log("%s · TEZGÂH kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %.1f sn" % (SURUM, len(g.SAC), len(g.PROF), len(g.ELEMAN), len(g.KAYNAK),
                                                                                               len(g.BIRLESIM), time.time() - t0))
    return g


def kur(log=print):
    """iki gövde (QR + tezgâh) · tek sefer"""
    if not G.kuruldu:
        kur_qr(log); kur_tz(log); G.kuruldu = True
    return G


# =====================================================================================================================================
# 3 · MONTAJ SÖZLEŞMESİ
# =====================================================================================================================================
ESKI_QR = tuple(["ayar_ayagi_%d" % i for i in range(6)] + ["taban_plakasi_3", "yan_sac_sol", "yan_sac_sag", "tavan_sac", "alt_raf_3", "ust_raf_3",
                 "robot_yuzu_goz_saci", "musteri_yuzu_goz_saci", "musteri_alt_panel", "musteri_ust_panel", "servis_kilidi_alt", "servis_kapagi_ust",
                 "servis_kilidi_ust", "servis_mentesesi_1", "servis_mentesesi_2", "servis_mentesesi_3"]
                + ["goz_%d%d_kasasi" % (r, c) for r in range(6) for c in range(2)] + ["goz_dikmesi_%d%d" % (i, j) for i in range(4) for j in range(2)])
ELK_DUS = ("servis_kapagi_alt_centikli", "servis_mentesesi_0_y50")          # elektrik katmanının alt servis kapağı + menteşesi → bu gövdenin servis paneli
QR_ONEK = ("ayar_ayagi_", "taban_plakasi_3", "yan_sac_", "tavan_sac", "alt_raf_3", "ust_raf_3", "robot_yuzu_goz_saci", "musteri_yuzu_goz_saci",
           "servis_", "goz_", "govde_")
ESLEME_QR = {"musteri_alt_panel": "musteri_yuzu_goz_saci (müşteri yüzü tek sac: göz sacı + alt panel + üst panel)",
             "musteri_ust_panel": "musteri_yuzu_goz_saci (pencereler aynı yerde)",
             "servis_kapagi_alt": "servis_kapagi_alt_sac (montaj _ELK_DUS bu adı düşürür → yeni ad)",
             "servis_mentesesi_0": "kalktı (menteşesiz kaldır-çıkar panel · 3 dil + kilitler)", "servis_mentesesi_1": "kalktı (menteşesiz panel)",
             "servis_mentesesi_2": "kalktı (menteşesiz panel)", "servis_mentesesi_3": "kalktı (menteşesiz panel)",
             "servis_kilidi_alt": "servis_kilidi_alt (+ servis_kilidi_alt_0)", "servis_kilidi_ust": "servis_kilidi_ust (+ servis_kilidi_ust_0/1/2)",
             "ELK|servis_kapagi_alt_centikli": "servis_kapagi_alt_sac (aynı çentikler a/b · elk listesinden yama ile düşer)",
             "ELK|servis_mentesesi_0_y50": "kalktı (yama ile düşer)"}


def govde_qr(log=print):
    """QR gövdesi montaj parça listesi (dünya, wp) · göz parçaları birim QR_GOZLER"""
    if G.q is None: kur_qr(log)
    L = GO.govde_parcalari(G.q)
    for p in L:
        if p["ad"].startswith("goz_"): p["birim"] = BIRIM_GOZ
    return L


def uygula_qr(QR, rapor=None, log=print):
    """montaj: QR.kur() + _ELK_DUS süzmesinden SONRA · eski gövdeyi çıkarır, üretim sacı gövdesini koyar (dünya) · idempotent"""
    yeni = govde_qr(log)
    GO.uygula(QR.PARCALAR, yeni, ESKI_QR, "servis_cercevesi_alt_sol", onekler=QR_ONEK, rapor=rapor, etiket="QR")
    for i, (k, a) in enumerate(QR.BIRIMLER):
        if k == BIRIM_QR:
            QR.BIRIMLER[i] = (k, "QR teslim dolabı · ÜRETİM SACI (h3_qr_sac_v1): 304 bükümlü kutu · yan 1,5 · göz yüzü + müşteri yüzü tava 1,5 · raflar 3 · "
                                 "taban 3 + alçak ayak · robot tarafı 1,5 kaldır-çıkar servis panelleri (6 çeyrek dönüş kilit) · 860 × 520 × 2050")
        if k == BIRIM_GOZ:
            QR.BIRIMLER[i] = (k, a + " · kasalar 1,0 iki U + TIG alın dikişi, dikmeler 304 lama 20 × 10 (h3_qr_sac_v1)")
    return QR.PARCALAR


ESKI_TZ = ("ayar_ayagi_0", "ayar_ayagi_1", "ayar_ayagi_2", "ayar_ayagi_3", "ayar_ayagi_4", "arka_ayak_kosebendi", "plint", "yan_sokak", "ayirma_paneli",
           "evye_dolabi_tabani", "arka_panel", "ust_yan_kusak_ince", "duvar_kosebendi_ince", "tabla_30", "etek_arka", "etek_ince", "etek_sokak", "on_kapak",
           "kapak_mentesesi_0", "kapak_mentesesi_1", "kapak_kulpu", "bulasik_ust_rafi", "raf_citasi_ince", "raf_citasi_bolme", "cekmece_onu", "cekmece_kulpu",
           "cekmece_kutu_tabani", "cekmece_kutu_yan_ince", "cekmece_kutu_yan_bolme", "cekmece_kutu_arka", "cekmece_kutu_on")
ESLEME_TZ = {"etek_arka": "tabla_30 (tabla + önlük + J + 3 etek TEK SAC büküm)", "etek_ince": "tabla_30 (tek sac)", "etek_sokak": "tabla_30 (tek sac)",
             "kapak_mentesesi_0": "on_kapak_mentese_0 (gizli 180° kaldır-çıkar · gövde yarısı kapak_dikmesi_sokak içinde)",
             "kapak_mentesesi_1": "on_kapak_mentese_1", "kapak_kulpu": "on_kapak_basac_0 (KULP YOK · bas-aç kapak_dikmesi_bolme içinde)",
             "raf_citasi_ince": "bulasik_ust_rafi (raf tava · yan dönüşleri kuşağa FHP)", "raf_citasi_bolme": "bulasik_ust_rafi (yan dönüşü ayırma paneline FHP)",
             "cekmece_kulpu": "cekmece_basac (KULP YOK · arkada bas-aç + kam kilit)",
             "cekmece_kutu_yan_ince": "cekmece_kutu_tabani (kutu tek sac tava 105 · köşeler TIG)", "cekmece_kutu_yan_bolme": "cekmece_kutu_tabani",
             "cekmece_kutu_arka": "cekmece_kutu_tabani", "cekmece_kutu_on": "cekmece_kutu_tabani"}
CEKMECE_ADI = re.compile(r"^(cekmece_|bulasik_ust_rafi|govde_bag_cekmece_|govde_bag_tabla_kilit_|govde_bag_raf_)")


def govde_tz(log=print):
    """tezgâh gövdesi montaj parça listesi (dünya, wp) · çekmece / raf parçaları birim TEZGAH_CEKMECE"""
    if G.t is None: kur_tz(log)
    L = GO.govde_parcalari(G.t)
    for p in L:
        if CEKMECE_ADI.match(p["ad"]): p["birim"] = BIRIM_CEK
    return L


def uygula_tz(TZ, rapor=None, log=print):
    """montaj: TZ.kur()'dan SONRA · eski tezgâh gövdesini çıkarır, üretim sacı gövdesini koyar (dünya) · idempotent"""
    yeni = govde_tz(log)
    GO.uygula(TZ.PARCALAR, yeni, ESKI_TZ, "kapak_dikmesi_sokak", onekler=TZ_ONEK, rapor=rapor, etiket="TEZGAH")
    for i, (k, a) in enumerate(TZ.BIRIMLER):
        if k == BIRIM_TZ:
            TZ.BIRIMLER[i] = (k, a + " · ÜRETİM SACI (h3_qr_sac_v1): 1,2 bükümlü paneller (R 1,8 · K 0,45) · tabla tek sac (R 3, CD saplamalı) · çift cidarlı kapak "
                                 "(2 gizli 180° menteşe + bas-aç, 30 × 30 dikmelerde) · 4 hijyenik M12 Ø60 ayak")
        if k == BIRIM_CEK:
            TZ.BIRIMLER[i] = (k, a + " · çekmece önü çift cidar · kutu tek sac tava · arkada bas-aç (h3_qr_sac_v1)")
    return TZ.PARCALAR


def kapak_dunya_qr_tz():
    """kapakla dönen bütün parçalar (dünya) — montajın kapak taraması için: {'on_kapak': Compound}"""
    kur()
    L = govde_tz()
    return {"on_kapak": GO.kapak_dunya(L, GO.Cerceve("TZ"), lambda a: G.t.DONER.get(a) == "on_kapak")}


ESLEME = dict(ESLEME_QR, **ESLEME_TZ)
