# -*- coding: utf-8 -*-
"""kesme_cad_v3 → kesme_cad_v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57.md · Kemal: "bu teknik resme göre 3D modelle").
K modülünden y 700–868 arasındaki YATAY DİLİM çıkarıldı (her şey 168 aşağı, üst 2030 → 1862):
  · bandı boydan boya geçen yalnız 7 parça var (arka + iki yan sac, 4 köşe dikmesi) → 168 kısalır; bandın içinde biten parça YOK;
    üstündeki her şey (istasyon tabanı, bant, kesici + sprey, yağ tankı, itici, pano, hava) 168 iner.
  · parçalar YENİ KOTLARDA doğrudan kurulur: H 1862 · H_B 892 · BANT 996 · FIRIN_BANDI 998 · E_PENCERE BANT'a bağlandı (978–1062) ·
    Y_EKSEN BANT'a bağlandı (932–980) · TANK Y_KIRIS'e bağlandı (1472–1752) · ürün girişi URUN_GIRISI (932–1072) · pano / hava / itici
    sabitleri − 168. denetim(): v3 dilim_v1 ile dilimlenip v4 ile parça parça karşılaştırılır (sınır kutusu ±0,01 + hacim).
  · E arayüzü: kutu_cad_v5 alınır (v3 yanlışlıkla kutu_cad_v3'ü alıyordu → urun_merkez / E taramaları 168 kayardı).
  · REF_kompresor_JUNAIR kalktı (kompresör v48'den beri fırın üstünde; yeri artık bulaşık makinesi).
  · YENİ (K altı 126–892): bulaşık makinesi MEIKO M-iClean US (bulasik_cad_v1, ayrı modül — burada REF olarak, montajdaki yerinde:
    dünya x 4108,5–4568,5 · y 126–826 · z −12…−645 zarfı) · kapak açık zarfı + MEIKO arka payı 25 (z −645…−670) boş ·
    arkasında KANİSTER RAFI (y 325–330, x 40–560, z −670…−805, iki L konsolla yan saclara) + DETERJAN + PARLATICI 5 L bidon
    (190 × 125 × 285 VARSAYIM; x 60–250 / 270–460 · y 330–615 · z −675…−800) + iki dozaj emiş hortumu makinenin arkasına.
  · Çıktılar: kesme_v4.glb · kesme_v4.json · 4_KESME_v4/BOM.csv.
Önceki: kesme_cad_v3.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kesme_cad_v3.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


NL = chr(10)
d('"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v3 (27 Eyl 2026)',
  '"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57) — y 700–868 dilimi çıkarıldı,' + NL +
  'her şey 168 aşağı (üst 1862 · taban 892 · bant 996); altında bulaşık makinesinin yeri + arkasında deterjan / parlatıcı rafı. Üretici: yap_kesme_v4.py. Önceki: kesme_cad_v3.py' + NL +
  'v3 (27 Eyl 2026)')
d("KOORDİNAT (modül yereli): x 0..600 (hatta 4000 + x) · y yerden · z 0 ön yüz, −830 arka. E modülü x 600'den başlar.",
  "KOORDİNAT (modül yereli): x 0..600 (hatta 4000 + x) · y yerden (v4: 0..1862) · z 0 ön yüz, −830 arka. E modülü x 600'den başlar.")
d("import kutu_cad_v3 as KC                                   # ortak geometri yardımcıları + E'nin kendisi (arayüz ve tarama)",
  "import kutu_cad_v5 as KC                                   # v4: ALÇAK HAT E'si (v3 yanlışlıkla kutu_cad_v3'ü alıyordu) · ortak geometri yardımcıları + E'nin kendisi (arayüz ve tarama)" + NL +
  "import bulasik_cad_v1 as BM                                # v4: K altındaki bulaşık makinesi (ayrı modül; burada yalnız REF + yer denetimi)")
d('MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))',
  'MALZEME.setdefault("pom", dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42))' + NL +
  'for _k, _v in {"kanister": (0.93, 0.94, 0.96, 1.0), "mavi_kapak": (0.15, 0.40, 0.85, 1.0), "dozaj": (0.90, 0.86, 0.62, 1.0)}.items():   # v4: bidon · parlatıcı kapağı · dozaj hortumu' + NL +
  '    MALZEME.setdefault(_k, dict(renk=_v, met=0.0, ruf=0.6))')

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
d("W, H, D = 600.0, 2030.0, 830.0", "W, H, D = 600.0, 1862.0, 830.0     # v4 ALÇAK HAT: 2030 − 168" + NL +
  "DILIM_Y0, DILIM_DY = 700.0, 168.0  # v4: v3'ten çıkarılan yatay dilim y 700–868 (bandı yalnız 3 sac + 4 dikme geçer; hava besleme ucu 1040 > 868)")
d("H_B = 1060.0                      # istasyon tabanı [K]", "H_B = 892.0                       # istasyon tabanı (sacın altı; sac 892–895) [K] · v4: 1060 − 168 = 788 düz çizgi + 104 kaide")
d("BANT = 1164.0                     # K bandı üstü = kesme yüzeyi (fırın bandı 1166'nın 2 mm altı) [K: kot zinciri]",
  "BANT = 996.0                      # K bandı üstü = kesme yüzeyi (fırın bandı 998'in 2 mm altı) [K: kot zinciri] · v4: 1164 − 168")
d("FIRIN_BANDI = 1166.0", "FIRIN_BANDI = 998.0               # v4: firin_tp10_cad_v7 BANT_UST_HAT (1166 − 168)")
d("E_PENCERE = (1146.0, 1230.0, -372.0, -24.0)   # E sol duvarındaki pizza penceresi y0 y1 z0 z1 [K: kutu_cad_v3]",
  "E_PENCERE = (BANT - 18.0, BANT + 66.0, -372.0, -24.0)   # E sol duvarındaki pizza penceresi y0 y1 z0 z1 = 978–1062 [K: kutu_cad_v5.PENCERE] · v3'te 1146–1230 sabitti" + NL +
  "URUN_GIRISI = (BANT - 64.0, BANT + 76.0, -420.0, -8.0)  # v4: sol duvardaki fırın bandı / ürün girişi y0 y1 z0 z1 = 932–1072 (v3 1100–1240 sabitti) — montajdaki _ka")
d("Y_EKSEN = (1100.0, 1148.0)", "Y_EKSEN = (BANT - 64.0, BANT - 16.0)   # v4: 932–980 (v3 1100–1148 sabitti)")
# denetçi: v3'ten kalan eski kot yorumları (değerler BANT'tan türer, yalnız yorum)
d("Y_AGIZ_UST = KESIM_ALT + STROK    # 1289,5 · kafa yukarıda bıçak ağzı", "Y_AGIZ_UST = KESIM_ALT + STROK    # 1121,5 (v4; v3 1289,5) · kafa yukarıda bıçak ağzı")
d("Y_GOBEK = Y_AGIZ_UST + BICAK_H    # 1334,5 · bıçak üstü = kafa plakası altı", "Y_GOBEK = Y_AGIZ_UST + BICAK_H    # 1166,5 (v4; v3 1334,5) · bıçak üstü = kafa plakası altı")
d("# yatık: 31 × 10,8 × 20 · üstü 1177 < itici kolu 1185", "# yatık: 31 × 10,8 × 20 · üstü 1009 < itici kolu 1017 (v4)")

# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
d('ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, 1100.0, 1240.0, -420.0, -8.0)), "kabuk")',
  'ekle("sol_sac_urun_girisi", kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, 0).cut(kut(-1, SAC + 1, URUN_GIRISI[0], URUN_GIRISI[1], URUN_GIRISI[2], URUN_GIRISI[3])), "kabuk")')
d("dik = dik.cut(kut(x0 - 1, x0 + 31, 1095.0, 1245.0, z0 - 1, z0 + 31))", "dik = dik.cut(kut(x0 - 1, x0 + 31, BANT - 69.0, BANT + 81.0, z0 - 1, z0 + 31))", 2)
d('bom=("Kare profil 30 × 30 × 2 AISI 304", 4, "boy 1900", "lazer + kaynak")', 'bom=("Kare profil 30 × 30 × 2 AISI 304", 4, "boy %.1f (v4)" % (H - SAC - Y_PLINT - 3.0), "lazer + kaynak")')

# ---------------------------------------------------------------- BANT ----------------------------------------------------------------
d('ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, 1100.0, BANT - BANT_K - 0.5, a, b), "sac",', 'ekle("bant_yan_levhasi_%d" % i, kut(10.0, 590.0, BANT - 64.0, BANT - BANT_K - 0.5, a, b), "sac",')
d('ekle("bant_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, 1100.0, za, zb), "sac",', 'ekle("bant_ayagi_%d" % i, kut(x - 15.0, x + 15.0, H_B + 3.0, BANT - 64.0, za, zb), "sac",')
d(".cut(kut(X_TAHRIK - 40, X_TAHRIK, 1000, 1200, z0 - 1, z1 + 1))", ".cut(kut(X_TAHRIK - 40, X_TAHRIK, BANT - 164.0, BANT + 36.0, z0 - 1, z1 + 1))")
d(".cut(kut(X_KUYRUK, X_KUYRUK + 40, 1000, 1200, z0 - 1, z1 + 1))", ".cut(kut(X_KUYRUK, X_KUYRUK + 40, BANT - 164.0, BANT + 36.0, z0 - 1, z1 + 1))")

# ---------------------------------------------------------------- TEREYAĞI ----------------------------------------------------------------
d("TANK = dict(x=140.0, z=-540.0, r=80.0, y0=1640.0, y1=1920.0)   # v3: köprü kirişinin arkası (Y_KIRIS üstü 1627,5 + 12,5)",
  "TANK = dict(x=140.0, z=-540.0, r=80.0, y0=Y_KIRIS[1] + 12.5, y1=Y_KIRIS[1] + 292.5)   # v3: köprü kirişinin arkası · v4: Y_KIRIS'e bağlandı → 1472–1752")
d("boru([(x, y1 + 14.0, z), (x, 1960.0, z), (x, 1960.0, -500.0), (440.0, 1960.0, -500.0),", "boru([(x, y1 + 14.0, z), (x, 1792.0, z), (x, 1792.0, -500.0), (440.0, 1792.0, -500.0),")
d("boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1995.0, z), (x + 45.0, 1995.0, -760.0), (x + 45.0, 1785.0, -760.0)], 3.0)",
  "boru([(x + 45.0, y1 + 60.0, z), (x + 45.0, 1827.0, z), (x + 45.0, 1827.0, -760.0), (x + 45.0, 1617.0, -760.0)], 3.0)")

# ---------------------------------------------------------------- İTİCİ ----------------------------------------------------------------
d("kut(c - 30.0, c + 30.0, Y_EKSEN[1] + 27.0, 1300.0, Z_EKSEN[0] - 7.0, Z_EKSEN[0] + 5.0)", "kut(c - 30.0, c + 30.0, Y_EKSEN[1] + 27.0, 1132.0, Z_EKSEN[0] - 7.0, Z_EKSEN[0] + 5.0)")
d("kut(c - 22.0, c + 22.0, 1225.0, 1300.0, Z_EKSEN[0] + 5.0, -446.0)", "kut(c - 22.0, c + 22.0, 1057.0, 1132.0, Z_EKSEN[0] + 5.0, -446.0)")
d("kut(c - 30.0, c + 30.0, 1180.0, 1225.0, -446.0, -434.0)", "kut(c - 30.0, c + 30.0, 1012.0, 1057.0, -446.0, -434.0)")
d("kut(c + 30.0, c + 100.0, 1185.0, 1200.0, -446.0, -434.0)", "kut(c + 30.0, c + 100.0, 1017.0, 1032.0, -446.0, -434.0)")
d("kut(c + 90.0, c + 100.0, 1185.0, 1200.0, -434.0, -205.0)", "kut(c + 90.0, c + 100.0, 1017.0, 1032.0, -434.0, -205.0)")
d("kut(c + 90.0, c + 208.0, 1185.0, 1205.0, -205.0, -175.0)", "kut(c + 90.0, c + 208.0, 1017.0, 1037.0, -205.0, -175.0)")

# ---------------------------------------------------------------- ELEKTRİK + HAVA ----------------------------------------------------------------
d('ekle("pano_plakasi", kut(300.0, 565.0, 1640.0, 2025.0, -826.0, -822.0), "sac")', 'ekle("pano_plakasi", kut(300.0, 565.0, 1472.0, 1857.0, -826.0, -822.0), "sac")')
d("for i, y in enumerate((1680.0, 1860.0)):                                           # v3: pano yukarıda (+980)",
  "for i, y in enumerate((1512.0, 1692.0)):                                           # v3: pano yukarıda (+980) · v4: − 168")
d("1647.5, 1747.5", "1479.5, 1579.5", 5)
d("TC.din_parca(TC.GUC_STEP, 315.0, 1830.0, zd + 122.8)", "TC.din_parca(TC.GUC_STEP, 315.0, 1662.0, zd + 122.8)")
d("TC.din_parca(TC.SURUCU_STEP, 450.0, 1860.0, zd + 28.0)", "TC.din_parca(TC.SURUCU_STEP, 450.0, 1692.0, zd + 28.0)")
d("TC.din_parca(TC.GUC_STEP, 382.0, 1830.0, zd + 122.8)", "TC.din_parca(TC.GUC_STEP, 382.0, 1662.0, zd + 122.8)")
d('ekle("klemens_sirasi", kut(508.0, 560.0, 1860.0, 1905.0, zd, zd + 45.0), "plastik",', 'ekle("klemens_sirasi", kut(508.0, 560.0, 1692.0, 1737.0, zd, zd + 45.0), "plastik",')
d('ekle("kablo_kanali_0", kut(305.0, 560.0, 1980.0, 2020.0, -822.0, -797.0), "plastik",', 'ekle("kablo_kanali_0", kut(305.0, 560.0, 1812.0, 1852.0, -822.0, -797.0), "plastik",')
d('ekle("kablo_kanali_dikey", kut(566.0, 591.0, 1063.0, 1995.0, -822.0, -797.0), "plastik")', 'ekle("kablo_kanali_dikey", kut(566.0, 591.0, H_B + 3.0, 1827.0, -822.0, -797.0), "plastik")')
d('ekle("sartlandirici_MS4", kut(60.0, 110.0, 1700.0, 1860.0, -826.0, -780.0), "aluminyum",', 'ekle("sartlandirici_MS4", kut(60.0, 110.0, 1532.0, 1692.0, -826.0, -780.0), "aluminyum",')
d('ekle("valf_adasi_VUVG_4", kut(130.0, 250.0, 1720.0, 1780.0, -826.0, -770.0), "aluminyum",', 'ekle("valf_adasi_VUVG_4", kut(130.0, 250.0, 1552.0, 1612.0, -826.0, -770.0), "aluminyum",')
d("boru([(230.0, 1040.0, -790.0), (230.0, 1063.0, -790.0), (230.0, 1500.0, -790.0), (85.0, 1500.0, -800.0), (85.0, 1700.0, -800.0)], 5.0)",
  "boru([(230.0, H_B - 20.0, -790.0), (230.0, H_B + 3.0, -790.0), (230.0, 1332.0, -790.0), (85.0, 1332.0, -800.0), (85.0, 1532.0, -800.0)], 5.0)")
d("boru([(190.0, 1780.0, -790.0), (190.0, 2000.0, -790.0), (205.0, 2000.0, -790.0), (205.0, 2000.0, ZC + 20.0),",
  "boru([(190.0, 1612.0, -790.0), (190.0, 1832.0, -790.0), (205.0, 1832.0, -790.0), (205.0, 1832.0, ZC + 20.0),")
d("boru([(160.0, 1720.0, -765.0), (160.0, 1320.0, -765.0), (160.0, 1320.0, -470.0)], 3.0)", "boru([(160.0, 1552.0, -765.0), (160.0, 1152.0, -765.0), (160.0, 1152.0, -470.0)], 3.0)")

# ---------------------------------------------------------------- 7 · TABAN ALTI: bulaşık yeri + deterjan / parlatıcı (yeni) ----------------------------------------------------------------
i0 = s.index("# ---------------------------------------------------------------- 7 · TABAN: içecek yedeği")
i1 = s.index("# ---------------------------------------------------------------- 8 · ÜRÜN + REFERANSLAR")
TABAN = '''# ---------------------------------------------------------------- 7 · TABAN ALTI (v4 · ALÇAK HAT): bulaşık yeri + deterjan / parlatıcı ----------------------------------------------------------------
# SPEC_alcak_hat_v57 + QR_TEZGAH_v4 (Kemal onaylı): K altı 126–892 · MEIKO M-iClean US sağ ön köşe dikmesine yaslı (kapağı dikmeye çarpmaz) ·
# solunda önde 77, dikmenin arkasında 107 BOŞ · arkasında tek sıra deterjan + parlatıcı, raf 325–330 · makinenin bağlantıları (y ≤ 310) altta kalır.
X_K_HAT = 4000.0                                   # K modülünün hattaki x'i (yerel x = dünya − 4000)
BULASIK_YER = (4108.5, Y_PLINT + 3.0, -20.0)       # bulasik_cad_v1 (X0, Y0, Z0) dünya kökü = kapak ön yüzü — montaj AYNISINI kullanmalı (ayaklar K'nin alt sacında, 126)
# denetçi düzeltmesi: kök z −12 değil −20 → makinenin TAMAMI (ışıklı kulp 8 + gövde 600 + arka bağlantılar 25 = 633) SPEC / Resim 1 v4 B–B'deki z −12…−645'e oturur
BULASIK_ZARF = dict(x=(BULASIK_YER[0] - X_K_HAT, BULASIK_YER[0] - X_K_HAT + BM.W), y=(BULASIK_YER[1], BULASIK_YER[1] + BM.H),
                    z=(BULASIK_YER[2] - BM.D - 25.0, BULASIK_YER[2] + 8.0))    # K yereli 108,5–568,5 × 126–826 × −645…−12 (SPEC: 633 derin = kulp 8 + gövde 600 + arka bağlantılar 25)
BULASIK_ARKA_PAY = (-670.0, -645.0)                # MEIKO föyü: arkada duvar payı 25 — BOŞ (yalnız makinenin arka bağlantı hortumları geçer, y ≤ 310)
BULASIK_BAGLANTI_UST = 310.0                       # makinenin arka bağlantıları yerden ≤ 165 + 126 + yarıçap 15 → 306 ≤ 310 (föy)
KANISTER = dict(x=190.0, y=285.0, z=125.0, L=5.0, yogunluk=1.3, bos_kg=0.3)   # 5 L bidon 190 × 285 × 125 [VARSAYIM: ölçü; 1,3 kg/L; boş bidon 0,3 kg]
KANISTER_X = (("deterjan", 60.0, 250.0), ("parlatici", 270.0, 460.0))
KANISTER_Y0, KANISTER_Z = 330.0, (-800.0, -675.0)
KANISTER_KAPAK = dict(r=20.0, h=15.0, dx=35.0)     # kapak Ø40 × 15, bidonun hortum tarafındaki kenarından 35 içeride [VARSAYIM]
RAF_Y, RAF_X, RAF_Z = (325.0, 330.0), (40.0, 560.0), (-805.0, -670.0)   # kanister rafı 304 · 5 mm · arka köşe dikmelerinin arası (x 31,5 / 568,5)
KONSOL = dict(yatay=(SAC, 62.0), dikey_h=33.0, t=3.0, z=(-796.0, -672.0))   # raf konsolu L büküm 3 mm: yan saca M6 · arka dikmeden (−798,5) ve arka paydan (−670) 2 mm ayrık
HORTUM = dict(r=3.0, y_ust=640.0, y_giris=280.0, x_inis=(260.0, 480.0), delik_r=7.0)
# dozaj emiş hortumu PVC Ø6/4 [VARSAYIM]: kapaktan yukarı 640 → yana → raftaki Ø14 delikten aşağı 280 → öne, makinenin arka yüzüne.
# MEIKO föyünde dozaj girişinin yeri yok → bağlantı bölgesinde (y ≤ 310), elektrik (x 148,5) / tahliye (294,5) / su (421,5) bağlantılarının arasından [VARSAYIM · MEIKO'ya teyit]


def bulasik_parcalari():
    """bulasik_cad_v1'in katıları montajdaki yerinde (BULASIK_YER), K yerelinde · + kapak açık zarfı (K yereli).
    BM modülünün durumu (X0, Y0, Z0, PARCALAR) korunur: montaj kendi BM.kur()'unu çağırır."""
    eski = (BM.X0, BM.Y0, BM.Z0, list(BM.PARCALAR))
    try:
        BM.X0, BM.Y0, BM.Z0 = BULASIK_YER
        out = [(p["ad"], BM.dunya(p).translate(cq.Vector(-X_K_HAT, 0.0, 0.0))) for p in BM.kur()]
        kx, ky, kz = BM.kapi_acik_zarf()
    finally:
        BM.X0, BM.Y0, BM.Z0 = eski[:3]
        BM.PARCALAR[:] = eski[3]
    return out, ((kx[0] - X_K_HAT, kx[1] - X_K_HAT), ky, kz)


def hortum_noktalari(i):
    ad_, xa, xb = KANISTER_X[i]
    zc = (KANISTER_Z[0] + KANISTER_Z[1]) / 2.0
    xk = xb - KANISTER_KAPAK["dx"]; y1 = KANISTER_Y0 + KANISTER["y"]; xi = HORTUM["x_inis"][i]
    return [(xk, y1, zc), (xk, HORTUM["y_ust"], zc), (xi, HORTUM["y_ust"], zc), (xi, HORTUM["y_giris"], zc), (xi, HORTUM["y_giris"], BULASIK_YER[2] - BM.D)]


def taban():
    """v4 · ALÇAK HAT: K tabanının altı — bulaşık makinesi REF (ayrı modül) + kanister rafı + deterjan / parlatıcı + dozaj hortumları"""
    for ad_, sh in bulasik_parcalari()[0]:
        ekle("REF_bulasik_" + ad_, cq.Workplane(obj=sh), "referans", "REF")
    zc = (KANISTER_Z[0] + KANISTER_Z[1]) / 2.0
    raf = kut(RAF_X[0], RAF_X[1], RAF_Y[0], RAF_Y[1], RAF_Z[0], RAF_Z[1])
    for xi in HORTUM["x_inis"]:
        raf = raf.cut(sily(xi, zc, HORTUM["delik_r"], RAF_Y[0] - 1.0, RAF_Y[1] + 1.0))     # hortum geçişi Ø14 (lastik rondela)
    ekle("deterjan_rafi", raf, "sac", bom=("Kanister rafı 304 · 5 mm (bulaşığın arkası)", 1, "%.0f × %.0f · 2 hortum deliği Ø%.0f" % (RAF_X[1] - RAF_X[0], RAF_Z[1] - RAF_Z[0], 2 * HORTUM["delik_r"]),
                                        "v4 · lazer · arka köşe dikmelerinin arasında"))
    t = KONSOL["t"]; z0, z1 = KONSOL["z"]
    for i, (xa, xb, xs0, xs1) in enumerate(((KONSOL["yatay"][0], KONSOL["yatay"][1], SAC, SAC + t), (W - KONSOL["yatay"][1], W - SAC, W - SAC - t, W - SAC))):
        k = kut(xa, xb, RAF_Y[0] - t, RAF_Y[0], z0, z1).union(kut(xs0, xs1, RAF_Y[0] - KONSOL["dikey_h"], RAF_Y[0], z0, z1))
        ekle("deterjan_rafi_konsolu_%d" % i, k, "sac", bom=("Raf konsolu 304 · 3 mm L büküm (yan saca 2 × M6)", 2, "%.1f × %.0f · boy %.0f" % (KONSOL["yatay"][1] - SAC, KONSOL["dikey_h"], z1 - z0),
                                                            "v4 · lazer + büküm") if i == 0 else None)
    for i, (ad_, xa, xb) in enumerate(KANISTER_X):
        yg = KANISTER_Y0 + KANISTER["y"] - KANISTER_KAPAK["h"]
        kg = KANISTER["L"] * KANISTER["yogunluk"] + KANISTER["bos_kg"]
        ekle("deterjan_kanisteri_" + ad_, kut(xa, xb, KANISTER_Y0, yg, KANISTER_Z[0], KANISTER_Z[1]), "kanister",
             bom=(("Bulaşık makinesi deterjanı 5 L bidon" if i == 0 else "Bulaşık makinesi parlatıcısı 5 L bidon"), 1,
                  "190 × 125 × 285 · dolu ≈ %.1f kg" % kg, "sarf · MEIKO uyumlu · ölçü VARSAYIM"))
        ekle("deterjan_kanister_kapagi_" + ad_, sily(xb - KANISTER_KAPAK["dx"], zc, KANISTER_KAPAK["r"], yg, KANISTER_Y0 + KANISTER["y"]), "kirmizi" if i == 0 else "mavi_kapak")
        pts = hortum_noktalari(i)
        L = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
        ekle("deterjan_emis_hortumu_" + ad_, boru(pts, HORTUM["r"]), "dozaj",
             bom=("Dozaj emiş hortumu PVC Ø6/4 + emiş lansı (bidondan MEIKO dozaj pompasına)", 2, "≈ %.2f m / hortum" % (L / 1000.0),
                  "VARSAYIM · MEIKO dozaj girişinin yeri teyit edilecek") if i == 0 else None)


'''
s = s[:i0] + TABAN + s[i1:]
d('    ekle("REF_kompresor_JUNAIR", kut(40.0, 420.0, 130.0, 640.0, -805.0, -425.0), "referans", "REF")' + NL,
  '    # v4: REF_kompresor_JUNAIR kalktı (kompresör v48\'den beri fırın üstünde; yeri artık bulaşık makinesi)' + NL)
d('ekle("REF_firin_bandi_ucu", kut(-120.0, 15.0, 1104.5, FIRIN_BANDI, -315.0, -25.0), "referans", "REF")', 'ekle("REF_firin_bandi_ucu", kut(-120.0, 15.0, 936.5, FIRIN_BANDI, -315.0, -25.0), "referans", "REF")')
d('ekle("REF_E_sol_duvar", kut(W, W + SAC, 1000.0, 1400.0, -420.0, 0.0)', 'ekle("REF_E_sol_duvar", kut(W, W + SAC, 832.0, 1232.0, -420.0, 0.0)')

# ---------------------------------------------------------------- DENETİM (v4 ekleri) ----------------------------------------------------------------
d('print("DENETİM (kesme_cad_v3)")', 'print("DENETİM (kesme_cad_v4)")')
DEN4 = '''    kontrol("sprey %.2f sn (pencere %.1f sn) · koni yarıçapı ürün üstünde %.0f mm (ürün 140–150)" % (H_["sprey_sn"], Z_SPREY[1] - Z_SPREY[0], H_["koni_r_mm"]), H_["sprey_sn"] <= Z_SPREY[1] - Z_SPREY[0] and 140 <= H_["koni_r_mm"] <= 160)
    denetim_v4(H_)
    return H_


UYARI = []


def denetim_v4(H_):
    """v4 · ALÇAK HAT: dilim eşdeğerliği · yeni kotlar · E arayüzü · bulaşık yeri · kanister rafı (ölçülür)"""
    import dilim_v1 as DL
    import kesme_cad_v3 as ESKI
    # 1 · kotlar + E arayüzü
    ts = bbx("istasyon_tabani_3"); ust = max(p["wp"].val().BoundingBox().ymax for p in PARCALAR if p["grup"] == "SABIT")
    H_["taban_ust"] = ts.ymax; H_["bant"] = bbx("bant_PU_2mm").ymax; H_["ust"] = ust
    kontrol("ALÇAK HAT kotları: üst %.1f (2030 − 168) · istasyon tabanı sacı %.0f–%.0f · K bandı %.1f · fırın bandı %.0f · ürün girişi %.0f–%.0f"
            % (ust, ts.ymin, ts.ymax, H_["bant"], FIRIN_BANDI, URUN_GIRISI[0], URUN_GIRISI[1]),
            abs(ust - 1862.0) < 0.01 and abs(ts.ymin - 892.0) < 0.01 and abs(H_["bant"] - 996.0) < 0.01 and abs(FIRIN_BANDI - 998.0) < 0.01)
    kontrol("E arayüzü kutu_cad_v5: E plakası %.1f = K bandı %.1f · E penceresi %.0f–%.0f = K'deki · E kalıbı %.1f · tepsi %.0f" % (KC.PLAKA_K, BANT, KC.PENCERE[0], KC.PENCERE[1], KC.KALIP, KC.TEPSI),
            KC.__name__ == "kutu_cad_v5" and abs(KC.PLAKA_K - BANT) < 0.01 and all(abs(a - b) < 0.01 for a, b in zip(KC.PENCERE, E_PENCERE)))
    # 2 · DİLİM EŞDEĞERLİĞİ: v3'ün y 700–868 dilimi çıkarılmış hali ↔ v4 (doğrudan yeni kotlarda)
    ESKI.modul()
    ref, rap = DL.dilimle(ESKI.PARCALAR, DILIM_Y0, DILIM_DY, atla=("REF_kompresor_JUNAIR",))
    k = DL.karsilastir(PARCALAR, ref)
    yeni_ok = all(a.startswith(("REF_bulasik_", "deterjan_")) for a in k["yeni_ek"])
    H_["dilim"] = dict(v3=len(ESKI.PARCALAR), alt=len(rap["ALT"]), ust=len(rap["UST"]), gecen=rap["GECEN"], ayni=len(k["ayni"]), yeni=len(k["yeni_ek"]))
    kontrol("dilim y %.0f–%.0f: v3 %d parça (altta %d · üstte %d · boydan geçen %d: 3 sac + 4 dikme · bantta biten 0) ↔ v4 birebir %d · fark %d · yeni %d (bulaşık REF + deterjan)"
            % (DILIM_Y0, DILIM_Y0 + DILIM_DY, len(ESKI.PARCALAR), len(rap["ALT"]), len(rap["UST"]), len(rap["GECEN"]), len(k["ayni"]), len(k["fark"]), len(k["yeni_ek"])),
            not k["fark"] and not k["ref_eksik"] and yeni_ok and len(k["ayni"]) == len(ESKI.PARCALAR) - 1, "; ".join(k["fark"][:5]) + (" eksik %s" % k["ref_eksik"] if k["ref_eksik"] else ""))
    fu = max(max(abs(a - b) for a, b in zip(urun_merkez(t), ESKI.urun_merkez(t)[:1] + (ESKI.urun_merkez(t)[1] - DILIM_DY,) + ESKI.urun_merkez(t)[2:])) for t in [i * 0.05 for i in range(203)])
    fg = max(max(abs(a - b) for a, b in zip(grup_trs(g, t), ESKI.grup_trs(g, t))) for g in ("KESICI", "ITICI_ARABA", "ITICI_KOL", "URUN") for t in [i * 0.1 for i in range(201)])
    kontrol("kinematik: urun_merkez(t) = v3 − 168 (203 an, en büyük fark %.4f mm) · grup_trs(t) = v3 (201 an × 4 grup, %.4f)" % (fu, fg), fu < 1e-6 and fg < 1e-6)
    # 3 · BULAŞIK MAKİNESİ (ayrı modül, montajdaki yerinde)
    bm, (kx, ky, kz) = bulasik_parcalari()
    ONDE = ("isikli_kulp", "dokunmatik_ekran")                              # kapağın önündeki kulp + ekran (föy): kapak yüzü −20'nin önüne taşar
    bmb = cq.Compound.makeCompound([sh for a_, sh in bm if a_ not in ONDE]).BoundingBox()
    bon = max(sh.BoundingBox().zmax for a_, sh in bm if a_ in ONDE)
    bta = cq.Compound.makeCompound([sh for a_, sh in bm]).BoundingBox()     # makinenin TAMAMI (kulp + ekran + arka bağlantılar dahil)
    Z = BULASIK_ZARF
    H_["bulasik"] = dict(x=(bmb.xmin, bmb.xmax), y=(bmb.ymin, bmb.ymax), z=(bmb.zmin, bmb.zmax), dunya_x=(bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT))
    H_["bulasik"]["kulp_onu_z"] = bon
    H_["bulasik"]["tam_z"] = (bta.zmin, bta.zmax)
    kontrol("bulaşık (bulasik_cad_v1, kök %s): dünya x %.1f–%.1f · y %.0f–%.0f · kapak + gövde z %.0f…%.0f · TAMAMI (kulp + bağlantılar) z %.0f…%.0f = zarf %.0f…%.0f (SPEC 633) · kulp + ekran önü z %.1f ≤ 0 (modül ön yüzü) · ayaklar K alt sacında (%.0f)"
            % (BULASIK_YER, bmb.xmin + X_K_HAT, bmb.xmax + X_K_HAT, bmb.ymin, bmb.ymax, bmb.zmin, bmb.zmax, bta.zmin, bta.zmax, Z["z"][0], Z["z"][1], bon, bbx("taban_sac_3").ymax),
            bon <= 0.0 and abs(bta.zmin - Z["z"][0]) < 0.01 and abs(bta.zmax - Z["z"][1]) < 0.01 and
            bmb.xmin >= Z["x"][0] - 0.01 and bmb.xmax <= Z["x"][1] + 0.01 and bmb.ymin >= Z["y"][0] - 0.01 and bmb.ymax <= Z["y"][1] + 0.01
            and bmb.zmin >= Z["z"][0] - 0.01 and bmb.zmax <= Z["z"][1] + 0.01 and abs(bmb.ymin - bbx("taban_sac_3").ymax) < 0.01)
    K_ = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")]
    def kutu_(x, y, z):
        return cq.Solid.makeBox(x[1] - x[0], y[1] - y[0], z[1] - z[0], cq.Vector(x[0], y[0], z[0]))
    def giren(bolge, haric=()):
        L = []; B_ = bolge.BoundingBox()
        for p, sh in K_:
            if p["ad"].startswith(haric) if haric else False: continue
            if not KC._bb_kesisir(sh.BoundingBox(), B_): continue
            v = sh.intersect(bolge).Volume()
            if v > 0.01: L.append((p["ad"], round(v, 1)))
        return L
    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]), ("deterjan_emis_hortumu_",))
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez (dozaj hortum uçları makinenin arka yüzüne bağlanır)" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))
    g2 = []
    for p, sh in K_:
        A = sh.BoundingBox()
        for a_, b_ in bm:
            if KC._bb_kesisir(A, b_.BoundingBox()):
                v = sh.intersect(b_).Volume()
                if v > 0.01: g2.append((p["ad"], a_, round(v, 1)))
    kontrol("bulaşık gerçek katıları (%d parça) ↔ K parçaları çakışma %d" % (len(bm), len(g2)), not g2, str(g2[:5]))
    g3 = giren(kutu_(kx, ky, kz))
    H_["bulasik_kapak_zarfi"] = dict(x=kx, y=ky, z=kz)
    kontrol("kapak açık zarfı (alttan menteşeli, önde %.0f): x %.1f–%.1f · y %.0f–%.0f · z %.0f…%.0f → K parçası yok (sağ ön dikme x %.1f'de başlar)"
            % (kz[1] - kz[0], kx[0], kx[1], ky[0], ky[1], kz[0], kz[1], bbx("kose_dikmesi_1").xmin), not g3, str(g3[:5]))
    ap = kutu_(Z["x"], Z["y"], BULASIK_ARKA_PAY)
    g4 = giren(ap)
    hy = max([sh.intersect(ap).BoundingBox().ymax for p, sh in K_ if p["ad"].startswith("deterjan_emis_hortumu_")] + [0.0])
    kontrol("MEIKO arka payı z %.0f…%.0f boş: yalnız 2 dozaj hortumu geçer, o da bağlantı bölgesinde (üstü %.1f ≤ %.0f)" % (BULASIK_ARKA_PAY + (hy, BULASIK_BAGLANTI_UST)),
            all(a.startswith("deterjan_emis_hortumu_") for a, _v in g4) and len(g4) == 2 and hy <= BULASIK_BAGLANTI_UST, str(g4))
    ustu = [(p["wp"].val().BoundingBox().ymin, p["ad"]) for p in PARCALAR if p["grup"] not in ("REF", "URUN", "URUN_IZ", "SPREY")
            and KC._bb_kesisir(p["wp"].val().BoundingBox(), kutu_(Z["x"], (Z["y"][1], H), Z["z"]).BoundingBox())]
    H_["bulasik_ust_bosluk"] = min(ustu)[0] - bmb.ymax
    kontrol("bulaşığın üstü %.0f → ilk K parçası %s %.0f: boşluk %.0f mm" % (bmb.ymax, min(ustu)[1], min(ustu)[0], H_["bulasik_ust_bosluk"]), H_["bulasik_ust_bosluk"] > 0.0)
    sol = bmb.xmin - bbx("kose_dikmesi_0").xmax; sol_ark = bmb.xmin - bbx("sol_sac_urun_girisi").xmax
    H_["bulasik_sol"] = dict(on=sol, arka=sol_ark)
    print("     bulaşığın solu: önde %.1f (köşe dikmesinden) · dikmenin arkasında %.1f (sol sacdan) → BOŞ" % (sol, sol_ark))
    # 4 · KANİSTER RAFI + BİDONLAR
    kg = KANISTER["L"] * KANISTER["yogunluk"] + KANISTER["bos_kg"]
    F = len(KANISTER_X) * kg * 9.81
    Lr = (W - KONSOL["yatay"][1]) - KONSOL["yatay"][1]                    # konsol uçları arası açıklık
    I_ = (RAF_Z[1] - RAF_Z[0]) * (RAF_Y[1] - RAF_Y[0]) ** 3 / 12.0
    w_ = 5.0 * (F / Lr) * Lr ** 4 / (384.0 * 193000.0 * I_)               # basit mesnet, yayılı yük (304: E 193 GPa)
    H_["raf_sehim_mm"] = w_; H_["kanister_kg"] = kg
    kontrol("kanister rafı %.0f × %.0f × %.0f · yük %d × %.1f kg = %.0f N · açıklık %.0f · sehim %.2f mm ≤ L/300 = %.2f [VARSAYIM yoğunluk 1,3]"
            % (RAF_X[1] - RAF_X[0], RAF_Z[1] - RAF_Z[0], RAF_Y[1] - RAF_Y[0], len(KANISTER_X), kg, F, Lr, w_, Lr / 300.0), w_ <= Lr / 300.0)
    kb = [bbx("deterjan_kanisteri_" + a) for a, _x0, _x1 in KANISTER_X]
    kk = [bbx("deterjan_kanister_kapagi_" + a) for a, _x0, _x1 in KANISTER_X]
    kontrol("bidonlar rafın üstünde: x %.0f–%.0f / %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f · arka paydan %.0f · arka dikmelerden x'te %.1f / %.1f"
            % (kb[0].xmin, kb[0].xmax, kb[1].xmin, kb[1].xmax, kb[0].ymin, max(b.ymax for b in kk), kb[0].zmin, kb[0].zmax,
               BULASIK_ARKA_PAY[0] - kb[0].zmax, kb[0].xmin - bbx("kose_dikmesi_2").xmax, bbx("kose_dikmesi_3").xmin - kb[1].xmax),
            all(abs(b.ymin - RAF_Y[1]) < 0.01 for b in kb) and abs(max(b.ymax for b in kk) - (KANISTER_Y0 + KANISTER["y"])) < 0.01 and kb[0].zmax <= BULASIK_ARKA_PAY[0])
    Lh = [sum(math.dist(a, b) for a, b in zip(hortum_noktalari(i)[:-1], hortum_noktalari(i)[1:])) for i in range(len(KANISTER_X))]
    H_["hortum_m"] = [round(x / 1000.0, 2) for x in Lh]
    print("     dozaj hortumları: %s m · makineye y %.0f'de girer (x %s) · raftan Ø%.0f delikle iner" % (H_["hortum_m"], HORTUM["y_giris"], HORTUM["x_inis"], 2 * HORTUM["delik_r"]))
    # erişim: bidon değişimi için makinenin yanındaki boşluk
    en_dar = min(KANISTER["x"], KANISTER["z"])
    if sol_ark < en_dar:
        UYARI.append("bidon değişimi: bulaşığın solunda dikmenin arkası %.0f mm < bidonun en dar yüzü %.0f → bidon yandan çıkmaz; bulaşık öne çekilmeli (hortum payı) ya da arka sacda servis kapağı gerekir" % (sol_ark, en_dar))
    for u in UYARI:
        print("  UYARI: " + u)
    H_["uyari"] = list(UYARI)
'''
d('''    kontrol("sprey %.2f sn (pencere %.1f sn) · koni yarıçapı ürün üstünde %.0f mm (ürün 140–150)" % (H_["sprey_sn"], Z_SPREY[1] - Z_SPREY[0], H_["koni_r_mm"]), H_["sprey_sn"] <= Z_SPREY[1] - Z_SPREY[0] and 140 <= H_["koni_r_mm"] <= 160)
    return H_
''', DEN4)

# ---------------------------------------------------------------- BOM / ÇIKTILAR ----------------------------------------------------------------
d('"Seviye", "regülatör", "Polikarbonat", "PWM", "Acil", "Silindir sensörü", "koli", "kolisi", "hortum", "Avara", "tank")) else "ÜRETİM"',
  '"Seviye", "regülatör", "Polikarbonat", "PWM", "Acil", "Silindir sensörü", "koli", "kolisi", "hortum", "Avara", "tank", "bidon")) else "ÜRETİM"')
for a, b in (('print("K KESME + SPREY v3 (tank + pano yukarida, taban bos): %d parca', 'print("K KESME + SPREY v4 (alcak hat: ust 1862 · taban 892 · bant 996 · altinda bulasik + deterjan): %d parca'),
             ('"generator": "AUTOKITCH kesme_cad_v3"', '"generator": "AUTOKITCH kesme_cad_v4"'), ('surum="kesme_cad_v3 · %s"', 'surum="kesme_cad_v4 · %s"'),
             ('"otonom", "hat3d", "kesme_v3.glb")', '"otonom", "hat3d", "kesme_v4.glb")'), ('"arastirma", "4_KESME_v3")', '"arastirma", "4_KESME_v4")'),
             ('"otonom", "hat3d", "kesme_v3.json")', '"otonom", "hat3d", "kesme_v4.json")')):
    d(a, b)
d('raise AssertionError("kesme_cad_v3', 'raise AssertionError("kesme_cad_v4', 0)
hedef = os.path.join(U, "kesme_cad_v4.py")
assert not os.path.exists(hedef), "kesme_cad_v4.py zaten var — üstüne yazılmaz"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kesme_cad_v4.py yazildi")
