# -*- coding: utf-8 -*-
"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v4 (29 Eyl 2026 gece · yap_kaide_cad_v4.py): C KAİDESİNDE SOĞUTMA GRUBU CEBİ + HAVA PENCERELERİ (TOPPING v30)
v4: Kemal "soğutma grubunu alta (arka köşe), sağ köşedekileri kaldır": 3. enine 2046 → 2120 (3. göz 1620–2100: ünite cebi + atış boşluğu) · 4 gözde ön + boyuna
    profil penceresi (y 800–876 · 1.–2. EMİŞ, 3.–4. ATIŞ) · üst plakada hava açıklıkları + ünite cebi · A kaidesi AYNI
v3: AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v3 (29 Eyl 2026 · yap_kaide_cad_v3.py): KAİDELER İSTASYON YÜZLERİYLE AYNI HİZADA — A 1,5–700 · C 700–2500 · C arka −830
v2: AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v2 (27 Eyl 2026 gece) — ÖN DÜZLEM +79 (SPEC_on_duzlem_v63.md §2.2) · önceki: kaide_cad_v1.py (yap_kaide_cad_v2.py)
v2: ön profil z −4 → +35 (dolap üst sacı +39'a uzar → kaide tam basar; önünde A/C ön çerçevesi +39…+59, panel +59…+79) · A taban sacı x 692 → 700
    · denetçi düzeltmesi (28 Eyl): A taban sacı x 1,5–700 · z −828,5…+39 (kabin sol/arka sacı + ön çerçeve arkası) → açıcı kabininin 4 dikmesi tam oturur
    (C dis_taban'a değer) · KARAR (varsayım): A boyuna profili kolon dikmesinin altına (z −655…−615) + kolon deliği 122 × 52 · TOPPING denetimi TC v25 / TU v14
    (dosya yoksa v24 / v13, çıktıda yazılır) · yeni denetim: taban sacı ↔ C dis_taban teması, havada parça = 0, dolap üst sacı (store_cad_v8) kaide önünü taşır.
v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4)
Çekmeceli dolabın üstü y 788 (tek düz çizgi) → A (açıcı) ve C (TOPPING) mekanizmaları 104 yukarıda: mekanizma tabanı 892, disk 1000.
KAİDE: çelik çerçeve (AISI 304 kutu profil 40 × 100 × 2, dik) y 788–888 + üst plaka 4 mm 888–892 · A x 8–692 · C x 708–2492 (resim
kutusu x0 + 8 … x1 − 8) · derinlik z −826…−4 (modül 830'un önünde ve arkasında 4 mm pay, VARSAYIM).
NASIL OTURUYOR (topping_cad_v24 yerel y + 892 · topping_uno_cad_v11 dünya y − 168 — montaj v57 kararı):
  · C: TC dis_taban (yerel 0–1,5, x 700–2500, z −830…0) C kaidesinin üst plakasına oturur; TC yan ve arka dış sacları dis_taban'ın
    kenarında (x 700–701,5 · 2498,5–2500 · z −830…−828,5) → kaide 8 / 4 mm içeride (UYARI, rapora bak).
  · A: TC'de A'nın tabanı YOK (dis_taban yalnız C'de). Açıcı kolonu (yerel y 0, x 290–410, z −660…−490) doğrudan A kaidesi üst plakasına
    oturur; mekanizma teknesi ve X motor kaidesi yerel 1,5 / 4,5'ten başlar → A'ya 1,5 mm TABAN SACI (892–893,5, kolon deliği) konur,
    tekne onun üstüne oturur (C'deki dis_taban'ın eşi). Kolonun altında enine profil (x 330–370) + boyuna profil (z −595…−555).
  · TU (UNO + kasetler + soğuk hacim) kaideye değmez: en alt parçası y 1013 (sos yayıcı borusu, disk 1000'in 13 üstü; TC kabuğuna asılı).
KOORDİNAT: DÜNYA. mm. Kütle yükleri VARSAYIM (aşağıda).
"""
import math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import qr_cad_v1 as QR                    # ortak denetim + BOM yardımcıları

Y_DUZ, Y_MEK = 788.0, 892.0               # dolap üstü · mekanizma tabanı (SPEC)
KAIDE_H = Y_MEK - Y_DUZ                   # 104
PL = 4.0                                  # üst plaka
PR = dict(b=40.0, h=100.0, t=2.0)         # kutu profil 40 × 100 × 2 (dik) → 788 + 100 = 888 · + plaka 4 = 892
A_X, C_X = (1.5, 700.0), (700.0, 2500.0)  # v3: istasyon yüzleriyle aynı hiza (v2 8–692 · 708–2492, Kemal: "sıfırında bitmiyor")
KZ_A, KZ_C = (-828.5, 35.0), (-830.0, 35.0)   # v3: A arka = A arka sacının iç yüzü · C arka = TOPPING arka sacıyla aynı düzlem (v2 −826)
KZ = KZ_C                                # v2 (SPEC v63 §2.2): ön +35 = dolap üst sacı ön kenarı +39 − 4 (tam basar; ön çerçeve +39…+59) · arka pay 4 VARSAYIM · v1: −4
A_SAC = 1.5                               # A mekanizma taban sacı (TC dis_taban'ın eşi)
KOLON = dict(x=(290.0, 410.0), z=(-660.0, -490.0))   # TC acici_kolonu (x yerel −410…−290 + 700) · dünya · (kutu sınırı: dikme + üst kol)
KOLON_DIKME_Z = (-660.0, -610.0)          # v2: kolonun tabana oturan DİKMESİ (topping_cad_v24 acici_kolonu 120 × 50) → taban sacı deliği 122 × 52 (v1: kutu sınırından 122 × 172)
X_A1 = 700.0                              # v2 (SPEC v63): A taban sacı sağ ucu = C dis_taban solu (v1: 692 → 8 mm boşluk)
A_SAC_X0 = 1.5                            # v2 denetçi düzeltmesi (28 Eyl): A taban sacı solu = kabin sol yan sacının iç yüzü (v1/v2 ilk: 8 → sol dikmelerin dış duvarı boşta)
A_SAC_Z = (-828.5, 39.0)                  # v2 denetçi düzeltmesi: arka = kabin arka sacının iç yüzü · ön = ön çerçevenin arkası (+39) → 4 köşe dikmesi taban sacına TAM oturur (önce −826…+35: %42–72)
C_ENINE = (1154.0, 1600.0, 2120.0)        # v4: 3. enine 2046 → 2120 (3. göz 1620–2100 = ünite cebi + atış boşluğu · B bölmeleriyle hizalı DEĞİLDİ, yük boyuna profillerle) · v3 aralık ≈ 446
# v4 · HAVA PENCERELERİ + AÇIKLIKLAR (TOPPING v30 soğutma grubu, sanayi dolabı gibi önden): dünya x · pencere y · açıklık z
C_PENCERE_Y = (800.0, 866.0)                                   # profil 788–888 (et 2) → altında 10, üstünde 20 mm gövde + 2 mm et (üst şerit eğilmesi: 76 yüksekte σ 131 MPa → 66 yüksekte 40 MPa)
C_PENCERE_X = {"emis": ((750.0, 1124.0), (1184.0, 1570.0)), "atis": ((1630.0, 2090.0), (2150.0, 2450.0))}   # 1.–2. göz EMİŞ · 3.–4. göz ATIŞ
C_PLAKA_KESIK = [(745.0, 1129.0, -785.0, -480.0), (1179.0, 1575.0, -785.0, -480.0),        # 1.–2. göz arka yarısı: emiş (teknik bölmenin altı)
                 (1628.0, 2095.0, -790.0, -477.0),                                         # 3. göz: ünite cebi (1628–2018) + sağında atış (2018–2095) · önü TC perdesinin arkası
                 (2145.0, 2415.0, -785.0, -480.0)]                                         # 4. göz arka yarısı: atış (teknik bölmenin sağ perdesi 2420)
C_BOYUNA_Z = (-435.0, -395.0)             # C boyuna orta profil (TC mekanizma teknesinin arka kenarı z −415 altında)
A_BOYUNA_Z = (-655.0, -615.0)             # v2 KARAR (varsayım): kolon DİKMESİNİN tam altında (dikme z −660…−610, ekseni −635) · v1 −595…−555 dikmenin 15 mm önündeydi (keşif A §5)
YUK = {"KAIDE_A": 60.0, "KAIDE_C": 400.0}   # kg · VARSAYIM: açıcı + tekne ucu · TOPPING TC + TU + dolu kasetler
RO = 7.93e-6                              # kg/mm³ AISI 304

PARCALAR = []
PROFIL_BOM = {}                           # birim → (profil parça sayısı, toplam boy mm) · BOM ile model karşılaştırılır
BIRIMLER = [
    ("KAIDE_A", "A mekanizma kaidesi 104 · x 1,5–700 (v3: istasyon yüzüyle aynı hiza · taban sacı 1,5–700) · y 788–892 · z −826…+35 (taban sacı −828,5…+39) · AISI 304 kutu profil 40 × 100 × 2 + üst plaka 4 · açıcı kolonu dikmesi altında enine + boyuna profil · 1,5 mm taban sacı 892–893,5 (tekne + kabin dikmeleri) · v2 ön düzlem +79"),
    ("KAIDE_C", "C mekanizma kaidesi 104 · x 700–2500 (v3: TOPPING yan sacları ve fırınla aynı hiza) · y 788–892 · z −830…+35 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur · v2 ön düzlem +79 · v4: SOĞUTMA GRUBU CEBİ (3. göz 1620–2100) + 4 gözde ön / boyuna profil hava pencereleri 76 yüksek + plakada emiş / atış açıklıkları (TOPPING v30)"),
]
BIRIM_MODUL = {"KAIDE_A": "A", "KAIDE_C": "C"}
ON_BIRIMLER = ()                          # v2: ön düzlemin (+79) önüne taşan parça YOK (kaide z ≤ +35, önünde ön çerçeve + panel) · v1: z ≤ −4
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "sac": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32)}
kut = QR.kut
dunya = QR.dunya


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def profil_x(x0, x1, z0, z1):
    """x boyunca kutu profil (uçları açık) · y 788–888"""
    t = PR["t"]
    return kut(x0, x1, Y_DUZ, Y_DUZ + PR["h"], z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, Y_DUZ + t, Y_DUZ + PR["h"] - t, z0 + t, z1 - t))


def profil_z(x0, x1, z0, z1):
    """z boyunca kutu profil (uçları açık)"""
    t = PR["t"]
    return kut(x0, x1, Y_DUZ, Y_DUZ + PR["h"], z0, z1).cut(kut(x0 + t, x1 - t, Y_DUZ + t, Y_DUZ + PR["h"] - t, z0 - 1.0, z1 + 1.0))


def cerceve(b, on, x0, x1, enine, boyuna_z, kz=None, pencere=(), plaka_kesik=()):
    kz = kz or KZ; bw = PR["b"]; zf, zb = kz[1] - bw, kz[0] + bw                # v3: birim başına z (A / C) · v4: pencere (x0, x1) · plaka_kesik (x0, x1, z0, z1)
    # denetçi düzeltmesi (27 Eyl): BOM_OZET kalemi birim başına ayrı + adet = profil parça sayısı + toplam boy (önce "2 adet · KAIDE_A çerçevesi" yazıyordu)
    xs_ = [x0 + bw] + [v for xc in enine for v in (xc - bw / 2.0, xc + bw / 2.0)] + [x1 - bw]
    boy_ = 2.0 * (x1 - x0) + (2 + len(enine)) * (zf - zb) + sum(xs_[i + 1] - xs_[i] for i in range(0, len(xs_), 2))
    n_ = 4 + len(enine) + len(xs_) // 2
    ilk = [True]
    def bom_():
        if ilk[0]:
            ilk[0] = False
            return ("Kutu profil 40 × 100 × 2 AISI 304 (dik, kaynaklı çerçeve) · %s" % b, n_, "%s çerçevesi · %d parça · toplam boy %.2f m" % (b, n_, boy_ / 1000.0),
                    "üretim · profil ölçüsü VARSAYIM", "ÜRETİM")
        return None
    _op = profil_x(x0, x1, zf, kz[1])
    for _a, _b in pencere:                                                     # v4 · hava penceresi (iki et birden)
        _op = _op.cut(kut(_a, _b, C_PENCERE_Y[0], C_PENCERE_Y[1], zf - 1.0, kz[1] + 1.0))
    ekle(on + "_on_profil", _op, "paslanmaz", b, bom=bom_())
    ekle(on + "_arka_profil", profil_x(x0, x1, kz[0], zb), "paslanmaz", b)
    ekle(on + "_yan_profil_sol", profil_z(x0, x0 + bw, zb, zf), "paslanmaz", b)
    ekle(on + "_yan_profil_sag", profil_z(x1 - bw, x1, zb, zf), "paslanmaz", b)
    xs = [x0 + bw]
    for i, xc in enumerate(enine):
        ekle(on + "_enine_profil_%d" % i, profil_z(xc - bw / 2.0, xc + bw / 2.0, zb, zf), "paslanmaz", b)
        xs += [xc - bw / 2.0, xc + bw / 2.0]
    xs.append(x1 - bw)
    for i in range(0, len(xs), 2):
        _bp = profil_x(xs[i], xs[i + 1], boyuna_z[0], boyuna_z[1])
        for _a, _b in pencere:                                                 # v4 · hava penceresi (bu segmentin içindekiler)
            if _a >= xs[i] and _b <= xs[i + 1]:
                _bp = _bp.cut(kut(_a, _b, C_PENCERE_Y[0], C_PENCERE_Y[1], boyuna_z[0] - 1.0, boyuna_z[1] + 1.0))
        ekle(on + "_boyuna_profil_%d" % (i // 2), _bp, "paslanmaz", b)
    _pl = kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, kz[0], kz[1])
    for _a, _b, _z0, _z1 in plaka_kesik:                                       # v4 · hava açıklıkları + ünite cebi
        _pl = _pl.cut(kut(_a, _b, Y_DUZ + PR["h"] - 1.0, Y_MEK + 1.0, _z0, _z1))
    ekle(on + "_ust_plaka_4", _pl, "paslanmaz", b,
         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f%s" % (x1 - x0, kz[1] - kz[0], (" · v4: %d lazer kesik (hava açıklıkları + soğutma grubu cebi)" % len(plaka_kesik)) if plaka_kesik else ""), "üretim (lazer) · mekanizma tabanına M6 perçin somunlu", "ÜRETİM"))
    PROFIL_BOM[b] = (n_, boy_)
    return n_, boy_


def kur():
    PARCALAR[:] = []
    cerceve("KAIDE_A", "kaide_A", A_X[0], A_X[1], ((KOLON["x"][0] + KOLON["x"][1]) / 2.0,), A_BOYUNA_Z, kz=KZ_A)
    s = kut(A_SAC_X0, X_A1, Y_MEK, Y_MEK + A_SAC, A_SAC_Z[0], A_SAC_Z[1]).cut(kut(KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, Y_MEK - 1.0, Y_MEK + A_SAC + 1.0, KOLON_DIKME_Z[0] - 1.0, KOLON_DIKME_Z[1] + 1.0))   # v2: x 1,5 → 700 · z −828,5…+39 · delik dikmeye göre
    ekle("kaide_A_mekanizma_taban_saci", s, "sac", "KAIDE_A",
         bom=("A mekanizma taban sacı AISI 304 1,5 mm (TC dis_taban'ın A'daki eşi) · açıcı kolonu dikmesi deliği %.0f × %.0f" % (KOLON["x"][1] - KOLON["x"][0] + 2.0, KOLON_DIKME_Z[1] - KOLON_DIKME_Z[0] + 2.0),
              1, "%.1f × %.1f" % (X_A1 - A_SAC_X0, A_SAC_Z[1] - A_SAC_Z[0]), "üretim · v2: sağ ucu x 700 = C dis_taban solu (SPEC v63) · sol x 1,5 / arka −828,5 / ön +39 = kabin sacları ve ön çerçeve (köşe dikmeleri tam oturur; kaide profilinin 6,5 / 2,5 / 4 mm dışına taşan kenarlar 1,5 sacın kendisi)", "ÜRETİM"))
    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z, kz=KZ_C, pencere=C_PENCERE_X["emis"] + C_PENCERE_X["atis"], plaka_kesik=C_PLAKA_KESIK)
    ekle("kaide_C_tepsi_kosebendi", kut(1640.0, 2006.0, Y_DUZ + 2.0, 806.0, C_BOYUNA_Z[0] - 3.0, C_BOYUNA_Z[0]).union(kut(1640.0, 2006.0, 803.0, 806.0, C_BOYUNA_Z[0] - 33.0, C_BOYUNA_Z[0] - 3.0)), "paslanmaz", "KAIDE_C",
         bom=("Soğutma grubu tepsisi ön köşebendi L 30 × 18 × 3 AISI 304", 1, "366 boy · 3. gözün boyuna profilinin arka yüzüne pencerenin ALTINDAN kaynak (790–800)", "v4 · TOPPING v30 soğutma grubu tepsisinin ön kenarı buna oturur (2 × M5) · arka kenarı TC askılarında", "ÜRETİM"))
    return PARCALAR


# ---------------------------------------------------------------- TOPPING (TC + TU) ile oturma denetimi ----------------------------------------------------------------
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")          # hat_montaj_v56 L193 ile aynı
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
V3_CIKAN = ("kabin_", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


def tc_modul():
    """v2: C ajanının yeni TOPPING CAD'i (topping_cad_v25) varsa o, yoksa v24 · (modül, ad)"""
    import importlib
    for ad in ("topping_cad_v30", "topping_cad_v29", "topping_cad_v25", "topping_cad_v24"):          # v4: v30 (soğutma grubu kaidede)
        if os.path.exists(os.path.join(U, ad + ".py")):
            try:
                return importlib.import_module(ad), ad
            except Exception as e:                                    # yarım yazılmış dosya → bir önceki sürüm
                print("  UYARI: %s yüklenemedi (%s) → bir önceki sürüm" % (ad, str(e)[:120]))
    raise RuntimeError("topping_cad_v24/v25/v29/v30 yok")


def tu_yolu():
    """v2: TU = topping_uno_cad_v14 (C ajanı) varsa o, yoksa v13 (montaj v62'nin kullandığı) · (dosya yolu, ad) · eski v11 yüklemesi kalktı"""
    for ad in ("topping_uno_cad_v18", "topping_uno_cad_v17", "topping_uno_cad_v14", "topping_uno_cad_v13"):   # v4: v18 (dikdörtgen soğuk kutu)
        if os.path.exists(os.path.join(U, ad + ".py")):
            return os.path.join(U, ad + ".py"), ad
    raise RuntimeError("topping_uno_cad_v13/v14/v17/v18 yok")


def topping_denetimi(ps, kontrol):
    TC, tc_ad = tc_modul()
    print("  (TOPPING CAD: %s)" % tc_ad)
    TC.PARCALAR[:] = []; TC.modul()
    tc = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom") and v1_kalir(p["ad"]) and p["ad"] not in AKTARMA_TP10 and p["ad"] not in ("on_kapak", "on_kapak_pu", "kapak_contasi")]
    TCD = [(p["ad"], p["wp"].val().translate(cq.Vector(700.0, Y_MEK, 0.0))) for p in tc]
    TCD = [(a, s, s.BoundingBox()) for a, s in TCD]
    bb = {a: B for a, _s, B in TCD}
    # oturma
    dt, ak, tk = bb["dis_taban"], bb["acici_kolonu"], bb["mekanizma_teknesi"]
    kontrol("C: TC dis_taban altı %.1f = kaide C üstü %.0f · dis_taban x %.0f–%.0f / kaide %.0f–%.0f (UYARI: yan sac altları %.0f mm dışarıda)" % (dt.ymin, Y_MEK, dt.xmin, dt.xmax, C_X[0], C_X[1], C_X[0] - dt.xmin),
            abs(dt.ymin - Y_MEK) < 0.01)
    kontrol("A: açıcı kolonu altı %.1f = kaide A üstü %.0f · kolon x %.0f–%.0f z %.0f…%.0f A plakasının içinde" % (ak.ymin, Y_MEK, ak.xmin, ak.xmax, ak.zmin, ak.zmax),
            abs(ak.ymin - Y_MEK) < 0.01 and A_X[0] <= ak.xmin and ak.xmax <= A_X[1] and KZ[0] <= ak.zmin and ak.zmax <= KZ[1]
            and abs(ak.xmin - KOLON["x"][0]) < 0.01 and abs(ak.zmin - KOLON["z"][0]) < 0.01)
    kontrol("A: mekanizma teknesi altı %.1f = A taban sacı üstü %.1f (tekne x %.0f–%.0f)" % (tk.ymin, Y_MEK + A_SAC, tk.xmin, tk.xmax), abs(tk.ymin - Y_MEK - A_SAC) < 0.01)
    # v2 · A taban sacı sağ ucu = C dis_taban sol ucu (x 700): iki sac uç uca değer, tekne altında boşluk yok
    _ats = [dunya(p).BoundingBox() for p in ps if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]
    kontrol("v2 · A taban sacı x %.1f–%.1f · C dis_taban x %.1f–%.1f → uç uca (boşluk %.2f mm) · aynı kot %.1f / %.1f" % (_ats.xmin, _ats.xmax, dt.xmin, dt.xmax, dt.xmin - _ats.xmax, _ats.ymax, dt.ymax),
            abs(_ats.xmax - dt.xmin) < 0.01 and abs(_ats.ymax - dt.ymax) < 0.01)
    # v2 · kolon DİKMESİ taban sacı deliğinin içinde, altında enine + boyuna profil kesişimi
    _kd = [s_ for a_, s_, _B in TCD if a_ == "acici_kolonu"][0]
    _kes = _kd.intersect(kut(A_X[0], X_A1, Y_MEK - 0.5, Y_MEK + 0.5, KZ[0], KZ[1]).val()).BoundingBox()   # kolonun 892 kotundaki kesiti
    kontrol("v2 · kolon dikmesinin taban kesiti x %.0f–%.0f · z %.0f…%.0f ⊂ delik x %.0f–%.0f · z %.0f…%.0f (122 × 52) · altında enine x %.0f–%.0f + boyuna z %.0f…%.0f"
            % (_kes.xmin, _kes.xmax, _kes.zmin, _kes.zmax, KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, KOLON_DIKME_Z[0] - 1.0, KOLON_DIKME_Z[1] + 1.0,
               (KOLON["x"][0] + KOLON["x"][1]) / 2.0 - PR["b"] / 2.0, (KOLON["x"][0] + KOLON["x"][1]) / 2.0 + PR["b"] / 2.0, A_BOYUNA_Z[0], A_BOYUNA_Z[1]),
            KOLON["x"][0] - 1.0 <= _kes.xmin and _kes.xmax <= KOLON["x"][1] + 1.0 and KOLON_DIKME_Z[0] - 1.0 <= _kes.zmin and _kes.zmax <= KOLON_DIKME_Z[1] + 1.0
            and _kes.zmin <= A_BOYUNA_Z[1] and A_BOYUNA_Z[0] <= _kes.zmax)
    aal = [(B.ymin, a) for a, _s, B in TCD if B.xmin < A_X[1] and a not in ("acici_kolonu",)]
    kontrol("A: kolon dışındaki en alçak TC parçası %s y %.1f ≥ %.1f" % (min(aal)[1], min(aal)[0], Y_MEK + A_SAC), min(aal)[0] >= Y_MEK + A_SAC - 0.01)
    _mek = [(B.ymin, a) for a, _s, B in TCD if not a.startswith(("onyuz_", "sogutma_grubu"))]
    kontrol("TC mekanizma parçaları (%d, onyuz_ ön yüz + soğutma grubu cebi hariç) %.0f'nin altına inmez (en alçak %s %.1f)" % (len(_mek), Y_MEK, min(_mek)[1], min(_mek)[0]), min(_mek)[0] >= Y_MEK - 0.01)
    _cg = [(a, B) for a, _s, B in TCD if a.startswith("sogutma_grubu")]                 # v4 · TOPPING v30 soğutma grubu kaide cebinde
    if _cg:
        _gx0, _gx1 = min(B.xmin for a, B in _cg if not a.endswith("cep_perdesi")), max(B.xmax for a, B in _cg)
        _cgk = [(a, B) for a, B in _cg if a.startswith(("sogutma_grubu_KLF", "sogutma_grubu_tepsisi", "sogutma_grubu_pedi"))]   # kaideye gömülen gövde (askıların yatay kolları taban sacının üstünde)
        _gy0 = min(B.ymin for a, B in _cg); _gz0, _gz1 = min(B.zmin for a, B in _cgk), max(B.zmax for a, B in _cgk)
        _ck = [k_ for k_ in C_PLAKA_KESIK if k_[0] <= _gx0 and _gx1 <= k_[1]]
        kontrol("v4 · soğutma grubu (%d parça) kaide CEBİNDE: x %.1f–%.1f ⊂ 3. göz %.0f–%.0f · plaka kesiği içinde (%s) · en alt y %.1f − dolap üstü %.0f = %.1f mm hava (≥ 15, B tavanına ısı köprüsü yok) · gömülü kısım z %.1f…%.1f ⊂ arka yarı %.0f…%.0f"
                % (len(_cg), _gx0, _gx1, C_ENINE[1] + PR["b"] / 2.0, C_ENINE[2] - PR["b"] / 2.0, "evet" if _ck else "HAYIR", _gy0, Y_DUZ, _gy0 - Y_DUZ, _gz0, _gz1, KZ_C[0] + PR["b"], C_BOYUNA_Z[0]),
                bool(_ck) and _gx0 >= C_ENINE[1] + PR["b"] / 2.0 and _gx1 <= C_ENINE[2] - PR["b"] / 2.0 and _gy0 - Y_DUZ >= 15.0 and _gz0 >= KZ_C[0] + PR["b"] and _gz1 <= C_BOYUNA_Z[0])
    _on = [(a, B) for a, _s, B in TCD if a.startswith("onyuz_") and B.ymin < Y_MEK - 0.01]
    if _on:                                                           # v2 · SPEC §2.3: C ön çerçevesi + mekanizma kanatları kaide bandını örter (791–892)
        kontrol("v2 · TC ön yüz parçaları kaide bandında (%d parça, en alt y %.1f) tamamı kaidenin ÖNÜNDE: z ≥ %+.1f > kaide ön %+.0f (SPEC §2.3 kanatlar 791–892'yi örter)"
                % (len(_on), min(B.ymin for _a, B in _on), min(B.zmin for _a, B in _on), KZ[1]), min(B.zmin for _a, B in _on) >= KZ[1] - 0.01)
    K = [(p["ad"], dunya(p)) for p in ps]; K = [(a, s, s.BoundingBox()) for a, s in K]
    cak = []
    for a, sa, A in K:
        for c, sc, B in TCD:
            if QR._bbk(A, B):
                v = sa.intersect(sc).Volume()
                if v > 1.0: cak.append((round(v, 1), a, c))
    kontrol("kaide ↔ TOPPING CAD (%d parça, yerel y + 892) çakışma = 0" % len(TCD), not cak, str(cak[:6]))
    import importlib.util as ilu
    tu_yol, tu_ad = tu_yolu()
    print("  (TOPPING UNO: %s)" % tu_ad)
    sp = ilu.spec_from_file_location("TU_KAIDE", tu_yol)
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    tu = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
    TUD = [(q["ad"], q["sh"].translate(cq.Vector(700.0, -168.0, 0.0))) for q in tu]     # montaj v62: TU dünya y − 168, x + 700
    cak_tu = []
    for a, sa, A in K:
        for c, sc in TUD:
            B = sc.BoundingBox()
            if QR._bbk(A, B):
                v = sa.intersect(sc).Volume()
                if v > 1.0: cak_tu.append((round(v, 1), a, c))
    kontrol("kaide ↔ TOPPING UNO %s (%d parça, dünya) çakışma = 0" % (tu_ad, len(TUD)), not cak_tu, str(cak_tu[:6]))
    ymin = min(q["sh"].BoundingBox().ymin for q in tu) - 168.0
    xmin = min(q["sh"].BoundingBox().xmin for q in tu) + 700.0
    kontrol("TU (%s, %d parça, dünya y − 168) en alt %.2f > kaide üstü %.0f · en sol x %.0f (A kaidesine girmez)" % (tu_ad, len(tu), ymin, Y_MEK, xmin), ymin > Y_MEK + A_SAC)


BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v4")
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-110s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("KAİDE v4 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))
    print("DENETİM (kaide_cad_v4)")
    for kod_, x_, z_ in (("KAIDE_A", A_X, KZ_A), ("KAIDE_C", C_X, KZ_C)):                    # v3 · istasyon yüzleriyle aynı hiza
        q_ = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod_ and not p["ad"].endswith("taban_saci")]
        kontrol("v3 · %s profil + plaka x %.1f–%.1f (istasyon %.1f–%.1f) · arka z %.1f (%.1f) — sıfırında biter"
                % (kod_, min(v.xmin for v in q_), max(v.xmax for v in q_), x_[0], x_[1], min(v.zmin for v in q_), z_[0]),
                abs(min(v.xmin for v in q_) - x_[0]) < 0.01 and abs(max(v.xmax for v in q_) - x_[1]) < 0.01 and abs(min(v.zmin for v in q_) - z_[0]) < 0.01)
    kontrol("v3 · A kaidesi sağ ucu = C kaidesi sol ucu = 700 (A|C arasında boşluk yok)", abs(A_X[1] - C_X[0]) < 0.01 and abs(C_X[0] - 700.0) < 0.01)
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    kontrol("kaide yüksekliği %.0f = profil %.0f + plaka %.0f (dolap üstü %.0f → mekanizma tabanı %.0f)" % (KAIDE_H, PR["h"], PL, Y_DUZ, Y_MEK), abs(PR["h"] + PL - KAIDE_H) < 0.01)
    for kod, xr in (("KAIDE_A", A_X), ("KAIDE_C", C_X)):
        pr_ = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod and "_profil" in p["ad"]]
        boy_m = sum(max(v.xlen, v.zlen) for v in pr_)
        kontrol("%s BOM profil %d parça · %.2f m = model %d parça · %.2f m" % (kod, PROFIL_BOM[kod][0], PROFIL_BOM[kod][1] / 1000.0, len(pr_), boy_m / 1000.0),
                PROFIL_BOM[kod][0] == len(pr_) and abs(PROFIL_BOM[kod][1] - boy_m) < 0.5)
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        x0_, x1_ = min(v.xmin for v in q), max(v.xmax for v in q)
        y0_, y1_ = min(v.ymin for v in q), max(v.ymax for v in q)
        z0_, z1_ = min(v.zmin for v in q), max(v.zmax for v in q)
        vol = sum(dunya(p).Volume() for p in ps if p["birim"] == kod)
        taban = sum(dunya(p).BoundingBox().xlen * dunya(p).BoundingBox().zlen for p in ps if p["birim"] == kod and "_profil" in p["ad"])
        x0_bek, x1_bek = (A_SAC_X0, X_A1) if kod == "KAIDE_A" else xr         # v2: A taban sacı 1,5 → 700 (profiller 8–692)
        z0_bek, z1_bek = (A_SAC_Z[0], A_SAC_Z[1]) if kod == "KAIDE_A" else KZ_C  # v3: C arka −830 (A taban sacı −828,5…+39)
        kontrol("%s x %.1f–%.0f · y %.1f–%.1f · z %.1f…%.0f (v2: z −830…+39 içinde — ön çerçevenin arkası; ön profil +%.0f) · kütle %.1f kg" % (kod, x0_, x1_, y0_, y1_, z0_, z1_, KZ[1], vol * RO),
                abs(x0_ - x0_bek) < 0.01 and abs(x1_ - x1_bek) < 0.01 and abs(y0_ - Y_DUZ) < 0.01 and abs(z0_ - z0_bek) < 0.01 and z0_ >= -830.0 and abs(z1_ - z1_bek) < 0.01 and z1_ <= 39.0
                and all(abs(dunya(p).BoundingBox().zmax - KZ[1]) < 0.01 for p in ps if p["birim"] == kod and "_profil" in p["ad"] and "_on_profil" in p["ad"]))
        print("  YÜK: %s %.0f kg (VARSAYIM) + kendi %.1f kg → profil tabanı %.0f cm² üstünden dolap üstüne %.1f kPa (dolap üst sacı bunu taşımalı — çekmeceli dolap üretecinde denetlenmeli)"
              % (kod, YUK[kod], vol * RO, taban / 100.0, (YUK[kod] + vol * RO) * 9.81 / taban * 1e3))
    # C üst plaka: en büyük desteksiz panel · Roark (4 kenar basit mesnet, a/b = 1,2 → α 0,0616)
    _xs4 = [C_X[0] + PR["b"]] + [v for xc in C_ENINE for v in (xc - PR["b"] / 2.0, xc + PR["b"] / 2.0)] + [C_X[1] - PR["b"]]
    a_ = max(_xs4[i_ + 1] - _xs4[i_] for i_ in range(0, len(_xs4), 2))      # v4: en geniş göz (3. göz 480) · arka yarılar kesikli → ön yarı (kesiksiz) panel
    b_ = (KZ[1] - PR["b"]) - C_BOYUNA_Z[1]
    q_ = YUK["KAIDE_C"] * 9.81 / ((C_X[1] - C_X[0]) * (KZ[1] - KZ[0]) / 1e6)
    kb, ka = min(a_, b_) / 1000.0, max(a_, b_) / 1000.0
    w = 0.0616 * q_ * kb ** 4 / (193e9 * (PL / 1000.0) ** 3) * 1000.0
    _ar = max(a_, b_) / min(a_, b_); _al = 0.0616 + (0.0770 - 0.0616) * min(1.0, max(0.0, (_ar - 1.2) / 0.2)) if _ar <= 1.4 else 0.0906   # Roark 4 kenar basit mesnet α (a/b 1,2 · 1,4 · 1,6)
    w = _al * q_ * kb ** 4 / (193e9 * (PL / 1000.0) ** 3) * 1000.0
    kontrol("C üst plaka en büyük KESİKSİZ panel (ön yarı) %.0f × %.0f · a/b %.2f · α %.4f · yayılı %.0f Pa → sehim %.2f mm ≤ 1 (Roark, E 193 GPa)" % (max(a_, b_), min(a_, b_), _ar, _al, q_, w), w <= 1.0)
    # v4 · pencere üstündeki profil şeridi (kanal: üst et 40 × 2 + 2 × gövde 10 × 2) iki ucu ankastre kiriş gibi · yük: plakanın göz derinliği kadar şeridi
    _Lp = max(b__ - a__ for a__, b__ in C_PENCERE_X["emis"] + C_PENCERE_X["atis"]) / 1000.0
    _qp = q_ * ((KZ[1] - KZ[0]) / 2.0 / 1000.0)                                    # N/m · yarı derinlik şeridi (VARSAYIM: yükün yarısı bu profile)
    _hs = PR["h"] - 2.0 - (C_PENCERE_Y[1] - Y_DUZ)                                 # pencere üstündeki gövde yüksekliği (10)
    _A = 40.0 * 2.0 + 2.0 * 2.0 * _hs; _yc = (40.0 * 2.0 * (_hs + 1.0) + 2.0 * 2.0 * _hs * _hs / 2.0) / _A
    _I = 40.0 * 2.0 ** 3 / 12.0 + 40.0 * 2.0 * (_hs + 1.0 - _yc) ** 2 + 2.0 * (2.0 * _hs ** 3 / 12.0 + 2.0 * _hs * (_hs / 2.0 - _yc) ** 2)
    _S = _I / max(_yc, _hs + 2.0 - _yc); _M = _qp * _Lp ** 2 / 12.0 * 1000.0      # N·mm
    kontrol("v4 · pencere üstü profil şeridi (kanal 40 × %.0f, I %.0f mm⁴) %.0f mm açıklık · %.0f N/m → M %.0f N·mm · σ %.0f MPa ≤ 205/2 (304 akma, emniyet 2 · plaka taşımasını saymadan)" % (_hs + 2.0, _I, _Lp * 1000.0, _qp, _M, _M / _S, ), _M / _S <= 102.5)
    _kp = [(b__ - a__) * (z1__ - z0__) / 1e6 for a__, b__, z0__, z1__ in C_PLAKA_KESIK]
    kontrol("v4 · plaka kesikleri %d (emiş %.3f + ünite cebi / atış %.3f + atış %.3f m²) · pencereler %d × %.0f yüksek (emiş %.0f · atış %.0f mm boy) — hepsi profil kenarından ≥ 5 mm içeride"
            % (len(C_PLAKA_KESIK), _kp[0] + _kp[1], _kp[2], _kp[3], len(C_PENCERE_X["emis"]) + len(C_PENCERE_X["atis"]), C_PENCERE_Y[1] - C_PENCERE_Y[0],
               sum(b__ - a__ for a__, b__ in C_PENCERE_X["emis"]), sum(b__ - a__ for a__, b__ in C_PENCERE_X["atis"])),
            all(any(xs_ + 5.0 <= a__ and b__ <= xe_ - 5.0 for xs_, xe_ in zip(_xs4[::2], _xs4[1::2])) for a__, b__ in C_PENCERE_X["emis"] + C_PENCERE_X["atis"]))
    cak = QR.kendi_arasinda(ps, istisna=lambda a, c: False)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak[:20]))
    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))
    # v2 · HAVADA PARÇA (denetim_temas_v1): her parça zemine (dolap üstü 788) değen parçalar zinciriyle bağlı
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=Y_DUZ)
    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · kaide_cad_v4")
    kontrol("v2 · havada parça = 0 (%d parça · kök %d · bağlı %d · beyaz liste YOK)" % (hv["parca"], hv["kok"], hv["bagli"]), not hv["bilesen"], str([d_["en"] for d_ in hv["bilesen"]]))
    # v2 · kaide ön profili dolap üst sacının üstünde (store_cad_v8: tavan dış sacı +39'a uzar) — v8 yoksa BİLGİ
    if os.path.exists(os.path.join(U, "store_cad_v8.py")):
        try:
            import store_cad_v8 as SC8
            SC8.PARCALAR[:] = []; SC8.modul()
            _ts = [p for p in SC8.PARCALAR if p["ad"] == "tavan_dis_sac"]
            _tb = _ts[0]["wp"].val().BoundingBox() if _ts else None
            kontrol("v2 · dolap üst sacı (store_cad_v8 tavan_dis_sac) ön kenarı z %s ≥ kaide ön +%.0f · üst yüz y %s = %.0f"
                    % ("%.1f" % _tb.zmax if _tb else "?", KZ[1], "%.1f" % _tb.ymax if _tb else "?", Y_DUZ), bool(_tb) and _tb.zmax >= KZ[1] - 0.01 and abs(_tb.ymax - Y_DUZ) < 0.01)
        except Exception as e:
            print("  BİLGİ · store_cad_v8 yüklenemedi (%s) — B ajanı; kaide ön profilinin tam basması montajda denetlenir" % str(e)[:120])
    else:
        print("  BİLGİ · store_cad_v8 henüz yok (B ajanı) — v7'de tavan dış sacı z −40'ta bitiyor; kaide ön profili (−5…+35) v8 ile tam basar (montajda denetlenir)")
    if "hizli" not in arg:
        t1 = time.time()
        topping_denetimi(ps, kontrol)
        print("   (TOPPING denetimi %.0f sn)" % (time.time() - t1))
    if "bom" in arg:
        QR.bom_yaz(BOM_KLASOR, ps)
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
