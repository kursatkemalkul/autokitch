# -*- coding: utf-8 -*-
"""TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v1 · 25 Eyl 2026

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
V_EKSEN = SOGUK_TABAN + 38.5; V_UST = SOGUK_TABAN + 72.6; VZ = -387.0
UNO = [  # ad, x merkezi, hazne genişliği, hazne üstü, silindir çapı, ağız tipi, doz (ml)
    ("SOS", 210.0, 220.0, 1737.0, 52.0, "yassi", 76.0), ("HARC", 560.0, 440.0, 1832.0, 52.0, "yassi", 105.0),
    ("KIYMA", 895.0, 190.0, 1667.0, 70.0, "yuvarlak", 152.0), ("KUSBASI", 1105.0, 190.0, 1667.0, 70.0, "yuvarlak", 170.0)]
KASET = [("KAŞAR KABI", "kasar_cad_v14", 1220.0, 1502.0), ("KÜP SUCUK", "sucuk_cad_v7", 1522.0, 1664.0)]
CODEX_3B = {"kasar_cad_v14": {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                              "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"},
            "sucuk_cad_v7": {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"}}
ADA = (900.0, 1160.0, 1600.0, 1660.0, -660.0, -760.0)     # valf adası (kuru bölme)
FRL = (1650.0, 1700.0, 1250.0, 1420.0, -700.0, -780.0)    # şartlandırıcı
KOMP = (3410.0, 3790.0, 520.0, 1030.0, -40.0, -420.0)     # K tabanı (modül C yerelinde x 3300–3900)

# ================================================================ 1 · KABİN
ekle("kabin_taban_saci", kut(0, W, Y0, Y0 + 1.5, 0, -D), "fircali", "V")
ekle("kabin_arka_saci", kut(0, W, Y0, YUST, -D + 1.5, -D), "kabuk", "V")
ekle("kabin_ust_saci", kut(0, W, YUST - 1.5, YUST, 0, -D), "kabuk", "V")
ekle("kabin_sol_duvar_PU", kut(0, 90, Y0, YUST, 0, -D), "pu", "V", not_="sac + PU 60")
ekle("kabin_sag_duvar_PU", kut(W - 90, W, Y0, YUST, 0, -D), "pu", "V")
ekle("yalitim_tabani", kut(90, W - 90, YAL_TABAN[0], YAL_TABAN[1], Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö", not_="mevcut yalıtım tabanı 1183–1317")
ekle("soguk_hucre_A_tavan", kut(BAY_A[0], BAY_A[1], TAVAN_A, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö", not_="sos + harç üstünde tavan 1968")
ekle("soguk_hucre_B_tavan", kut(BAY_B[0], BAY_B[1], TAVAN_B, TAVAN_B + 60, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö")
ekle("soguk_hucre_basamak", kut(BAY_B[0], BAY_B[0] + 60, TAVAN_B + 60, TAVAN_A, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö")
ekle("arka_yalitim_A", kut(BAY_A[0], BAY_A[1], YAL_TABAN[0], TAVAN_A, Z_BOLME[0], Z_BOLME[1]), "pu", "Ö")
ekle("arka_yalitim_B", kut(BAY_B[0], BAY_B[1], YAL_TABAN[0], TAVAN_B + 60, Z_BOLME[0], Z_BOLME[1]), "pu", "Ö")
for ad, x0, x1 in (("sogutma_grubu", 850, 1150), ("pano_PLC", 1180, 1580), ("guc_kaynagi", 1600, 1655), ("UPS", 1660, 1709)):
    ekle("teknik_bant_" + ad, kut(x0, x1, 1772, 2012 if ad == "pano_PLC" else 1992, -110, -560), "zarf", "Ö", not_="pafta v9 teknik bant · ZARF")
# tabla + pide (ilk durak: sos)
ekle("tabla_diski", silz(0, 0, 1, 0, 1).translate((0, 0, 0)) if False else sily(210, ZT, 170, 1154, 1168), "tabla", "Ö", not_="Ø340 · tabla ekseni z −170 · süreç 1168")
ekle("pide", sily(210, ZT, 140, 1168, PIDE_UST), "hamur", "Ö")

# ================================================================ 2 · UNO İSTASYONLARI — beldos_cad_v1'deki UNO modeli
# UNO çerçevesi (X eksen: ağız −, tahrik +; Y arkaya; Z yukarı, 0 = silinen kaidenin üstü) → TOPPING:
#   x = cx − Y · y = 1320 + Z · z = −387 − X   (ağız öne, tahrik arkaya; ağız ekseni x −217 → z −170 = tabla ekseni)
import beldos_cad_v1 as BEL
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
    # ağız uzatması + uç (UNO ağzının dik bacağı 1263,5'te bitiyor)
    uc = 1184.0 if agiz == "yassi" else 1216.0
    ekle("%s_agiz_uzatmasi" % k, sily(cx, ZT, 18, (1224.0 if agiz == "yassi" else uc), 1264.0).cut(sily(cx, ZT, 16.5, 1180, 1265)), "paslanmaz", "H",
         not_="UNO 90° ağzının ucundan pideye iniş: %.0f mm uzatma" % (1264.0 - (1224.0 if agiz == "yassi" else uc)))
    if agiz == "yassi":
        ekle("%s_yassi_uc" % k, loft_y(cember_y(cx, 1224.0, ZT, 18), dikdort_y(cx, 1184.0, ZT, 50, 8)), "paslanmaz", "B+V", not_="yassı uç 50 × 8 · ucu 1184 (pideden 8)")
    ekle("%s_dozaj_kovani" % k, sily(cx, ZT, 22, YAL_TABAN[0], YAL_TABAN[1] + 3).cut(sily(cx, ZT, 19, YAL_TABAN[0] - 1, YAL_TABAN[1] + 4)), "paslanmaz", "V",
         not_="ağız yalıtım tabanından kovanla geçer (kasetlerdeki gibi)")
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
    for p in ps:
        sh = p["wp"].val() if isinstance(p["wp"], cq.Workplane) and len(p["wp"].vals()) == 1 else cq.Compound.makeCompound([o for o in p["wp"].vals() if isinstance(o, cq.Shape)])
        mal = p["mal"] if p["mal"] in M else "pom"
        ekle("%s__%s" % (mod, p["ad"]), sh.translate(V(xc, SOGUK_TABAN, -200.0 - Vm.D / 2.0)), mal, "B",
             not_="%s (montaj v41'deki gibi, Codex parçaları dahil)" % ad)
    for ey, kk in zip(TC.eksen(mod), ("helezon", "rotor")):
        yy = SOGUK_TABAN + ey; tag = "%s_%s" % (mod, kk)
        ekle("mil_" + tag, silz(xc, yy, 11, -670, -525), "celik", "Ö")
        ekle("kovan_" + tag, silz(xc, yy, 30, -648, -565).cut(silz(xc, yy, 11.2, -649, -564)), "pom", "Ö")
        ekle("reduktor_" + tag, TC.suregear_koy(xc, yy, -670.0), "motor", "B", not_="SureGear PGCN23-1025 (katalog STEP)")
        g, kb = TC.nema23_koy(xc, yy, -670.0 - 79.0 - 2.0)
        ekle("motor_" + tag, g, "motor", "B", not_="AutomationDirect STP-MTR-23079 (katalog STEP)")
        ekle("motor_kablosu_" + tag, kb, "koyu", "B")

# ================================================================ 4 · HAVA TESİSATI
ekle("sartlandirici_filtre_regulator", kut(*FRL), "aluminyum", "V", not_="filtre + regülatör + ana vana · 7 bar")
ekle("sartlandirici_manometre", silz(1675, 1380, 14, -700, -690), "pom", "V")
ekle("valf_adasi_10x5_2", kut(*ADA), "aluminyum", "V", not_="10 × 5/2 elektro-valf: 4 piston + 4 döner valf + açıcı + yedek")
for n in range(10):
    x = ADA[0] + 14 + n * 24.0
    ekle("valf_bobini_%d" % (n + 1), kut(x, x + 18, ADA[3], ADA[3] + 30, -680, -740), "siyah", "V")
ekle("gecis_blogu_yalitim", kut(90, 1200, 1440, 1470, Z_BOLME[0], Z_BOLME[1]), "pom", "V", not_="hortumların soğuk hücreye geçtiği keçeli blok")
# ana hat: K tabanındaki kompresör → F tabanı arka köşe → C'ye sağ alttan → şartlandırıcı → ada
ana = [(3600, 1030, -380), (3600, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]
ekle("hava_ana_hatti_D10", boru(ana, 5.0), "hava_ana", "V", not_="Ø10 PU · K tabanı → F tabanı arka köşe kanalı → TOPPING sağ alt")
ekle("hava_hatti_sartlandirici_ada", boru([(1675, 1420, -740), (1675, 1630, -740), (1160, 1630, -740)], 5.0), "hava_ana", "V")
ekle("hava_hatti_acici_D6", boru([(900, 1640, -700), (40, 1640, -700), (40, 1640, -790), (-30, 1640, -790)], 3.0), "hortum_mavi", "V",
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
kas_bb = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(("kasar_cad", "sucuk_cad"))]).BoundingBox()
kontrol("kasetler modül içinde (x %.0f…%.0f)" % (kas_bb.xmin, kas_bb.xmax), kas_bb.xmin > 1200 and kas_bb.xmax < 1710)
for a, b in (("valf_adasi_10x5_2", "sartlandirici_filtre_regulator"),):
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
    for ad, cx, hw, hust, d_sil, agiz, doz in UNO:
        strok = doz * 1000.0 / (math.pi / 4 * d_sil ** 2); b = nodes[gi["PISTON_" + ad]]["translation"]
        kanal("PISTON_" + ad, "translation", [(b[0], b[1], b[2] + piston_dz(t, strok) * MM) for t in TT], "VEC3")
        kanal("VALF_" + ad, "rotation", [(math.sin(valf_aci(t) / 2), 0.0, 0.0, math.cos(valf_aci(t) / 2)) for t in TT], "VEC4")
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb_ = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH topping_uno_cad_v1"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb_)}],
          "animations": [{"name": "emis_basma_2sn", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb_))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb_), b"BIN\x00")); f.write(bb_)
    print("GLB %s · %d KB · %d parça · %d üçgen" % (os.path.basename(yol), (len(bb_) + len(js)) // 1024, len(P), uc))


if __name__ == "__main__":
    kal = [d for d in DEN if not d[1]]
    assert not kal, kal
    glb_yaz(os.path.join(OUT, "topping_uno_v1.glb"))
    with open(os.path.join(OUT, "topping_uno_v1.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v1 · %s" % time.strftime("%d.%m.%Y %H:%M"),
                       parcalar=[dict(ad=p["ad"], kaynak=p["kaynak"], not_=p["not_"], mal=p["mal"]) for p in P],
                       denetim=[dict(ad=a, sonuc="GEÇTİ" if s else "KALDI", deger=v) for a, s, v in DEN]), f, ensure_ascii=False, indent=1)
    print("JSON yazıldı · %d denetim hepsi GEÇTİ" % len(DEN))
