# -*- coding: utf-8 -*-
"""kasar_cad_v8.py → kiyma_cad_v1.py · aynı mimari (plakalar, saplamalar, göbek, haç kavrama, bayonet kapak), 140 genişlik, macun için helezon + besleme rotoru."""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec"
s = io.open(os.path.join(U, "kasar_cad_v8.py"), encoding="utf-8").read()
n = [0]
def rep(a, b, say=1):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    s = s.replace(a, b, say); n[0] += 1
def blok(bas, son, yeni):
    """bas işaretinden son işaretine kadar olan bloğu (son hariç) yenisiyle değiştir"""
    global s
    i = s.index(bas); j = s.index(son, i + len(bas)); s = s[:i] + yeni + s[j:]; n[0] += 1

# ---------- adlar ----------
for a, b in (("kasar_kabi_v8", "kiyma_kaseti_v3"), ("KASAR_KABI_v8", "KIYMA_KASETI_v3"), ("kasar_v8", "kiyma_v3"), ("kasar_cad_v8", "kiyma_cad_v3")):
    s = s.replace(a, b)

# ---------- başlık ----------
i = s.index('"""'); j = s.index('"""', i + 3) + 3
s = s[:i] + '''"""AUTOKITCH · KIYMA KASETİ v3 — ÜRETİM MODELİ (22 Eyl 2026) · ORTAK GÖVDE · kasar_cad_v8 mimarisinden türetildi (yap_kiyma_v3.py)
ÜRÜN: kıymalı pide iç harcı = kıyma + soğan + domates + biber + baharat, ÇİĞ → mevzuatta "hazırlanmış et karışımı": ≤ +4 °C
      (Hayvansal Gıdalar İçin Özel Hijyen Kuralları Yön. md. 31; sade kıyma olsaydı ≤ +2 °C). Bölmemiz +3 °C.
      160 g / pide · 20 pide / gün → 3,2 kg / gün → 2 gün 6,4 kg (pafta HAT v19).
DAVRANIŞ: kendi akmaz (çiğ ince kıyma hamuru ≈ 241 Pa·s, 10 °C — Foods 2026 15(15):2710), yapışır, helezonla birlikte dönmeye çalışır,
      beklerken SU SALAR (et %75 su; depolamada su tutma düşer, soğan/domates tuzla su bırakır). Drenaj YOK: su rotorla geri karıştırılır,
      kapalı tüp bölümü macunla dolu durduğu için serbest su ağızdan damlamaz.
KAŞAR KABINDAN FARKLAR:
  · genişlik 140 (standart kaset) · kadeh kesit aynı mantık: kâse R67 = besleme rotorunun dairesi
  · HELEZON Ø56 / mil Ø18 / hatve SÜREKLİ 36 → 48,5 (7,25 tur = 29 çeyrek tur) · büyük ve yavaş: uç hızı düşük → et ezilmez, ısınmaz
    tüp içinde TEK ağız sabit hatve, ağzın üstüne kadar sürer (macunu aşağı basar) · çırpıcı pim YOK (eti sıvar)
  · karıştırıcı kafesi yerine BESLEME ROTORU: 2 paslanmaz SIYIRICI LAMA 15 × 3, duvara 2–3 mm, 20° eğik → eti helezona doğru iter
  · AĞIZ: aşağı bakan 30 × 30 kısa MEME (harç ip gibi iner) · damlama için doz sonunda helezon ¼ tur GERİ (program) · etek yok
  · aynı kalan parçalar (kaşar kabıyla ORTAK): tahrik göbeği, haç kavrama, yaylı pim, ön kovan, topuz, setuskur, kilit pimi, kare miller, saplama/somun
UYARI: baskı parça yalnız DENEME içindir. Çiğ etle temas eden üretim parçası = 304/316 + POM-C / PE-UHMW talaşlı, Ra ≤ 0,8 (katman izi bakteri tutar).
v3 (22 Eyl) ORTAK GÖVDE — Kemal: "içindeki vida değişir ama hazne aynı olmalıydı". Gövde, iki uç plakası, kapak, kulp, saplamalar artık kıyma = kuşbaşı = küp sucuk.
      Kıymada vida Ø56 → Ø68 (tekne Ø72): 47 → 68 g/tur, 21 → 14 dev/dk, uç hızı 0,062 → 0,049 m/s (et daha az ezilir). Rotor UZUN kollu (duvara 2,4 · kanada 5).
v2 (22 Eyl): helezon ekseni 52 → 60 — 140'lık kasetlerde ALT tahrik aynı yükseklikte olsun (kuşbaşı da 60). Üst eksen ürüne bağlı kalır:
      rotor–kanat aralığı kıymada 5 mm (macun: süpürülmeyen katman kalmasın), kuşbaşında 18 mm (küp sıkışmasın) → 158 / 177.
ÇIKTI: otonom/kaset3d/kiyma_v3.glb/.usdz + kiyma_v3_dozaj.glb  ·  arastirma/3_TOPPING/kiyma_kaseti_v3/{step,stl}/ + MONTAJ.step + BOM.csv
"""''' + s[j:]

# ---------- sabitler ----------
rep("W, D, H = 280.0, 325.0, 360.0", "W, D, H = 140.0, 325.0, 360.0")
rep("CY, RT, YC, RB, RF, Y_UST, Y_DOLUM = 40.0, 22.0, 195.0, 134.0, 8.0, 352.0, 332.0",
    "CY, RT, YC, RB, RF, Y_UST, Y_DOLUM = 60.0, 36.0, 164.0, 67.0, 8.0, 352.0, 332.0      # v3 ORTAK GÖVDE (kıyma = kuşbaşı = küp sucuk): tekne Ø72 · kâse merkezi 164")
rep("R_MIL, R_KANAT, KARE = 8.0, 20.0, 8.0", "R_MIL, R_KANAT, KARE = 9.0, 34.0, 8.0")
rep("KOK_Z0, KOK_Z1, R_KOK = -91.0, -151.0, 13.0", "KOK_Z0, KOK_Z1, R_KOK = -91.0, -151.0, 15.0")
rep("KAN_Z0, KAN_Z1, HATVE0, TUR = -148.0, 156.0, 22.0, 11.75", "KAN_Z0, KAN_Z1, HATVE0, TUR = -148.0, 156.0, 36.0, 7.25")
rep("UC_HATVE, UC_Z0, UC_Z1 = 36.0, 156.0, 194.0", "UC_HATVE, UC_Z0, UC_Z1 = None, 156.0, 228.0      # tüp içi: ana hatvenin sonu sabit sürer, ağzın sonuna kadar")
rep("AG_Z0, AG_Z1, AG_X = 194.5, 230.5, 19.0", "AG_Z0, AG_Z1, AG_X = 198.0, 228.0, 15.0\nY_AGIZ = 8.0                                                         # meme dudağı kotu (ayak düzlemi 0 — tapayla birlikte masada durabilsin)")
rep("SAPLAMA = [(-90.0, 20.0), (90.0, 20.0), (-96.0, 340.0), (96.0, 340.0)]", "SAPLAMA = [(-52.0, 20.0), (52.0, 20.0), (-48.0, 340.0), (48.0, 340.0)]")
rep("HATVE1 = _hatve_sonu(); K_H = (HATVE1 - HATVE0) / (KAN_Z1 - KAN_Z0)", "HATVE1 = _hatve_sonu(); K_H = (HATVE1 - HATVE0) / (KAN_Z1 - KAN_Z0); UC_HATVE = HATVE1")
rep("from kasar_akis_model_v2 import RHO, YASA, T_DOK, r_t",
    "from kasar_akis_model_v2 import YASA, T_DOK, r_t\n"
    "RHO = 1.0                                                            # kıymalı harç g/mL · VARSAYIM (çiğ kıyma USDA ≈ 0,95; tartılacak)\n"
    "KG2 = 6.4                                                            # 2 günlük (pafta HAT v19)\n"
    "MALZEME.setdefault('kiyma', dict(renk=(0.62, 0.27, 0.22, 1.0), met=0.0, ruf=0.85))\n"
    "MALZEME.setdefault('kiyma_dolgu', dict(renk=(0.62, 0.27, 0.22, 1.0), met=0.0, ruf=0.85))")

# ---------- plakalar · saplama · kulp · kapak ----------
rep("p = p.cut(kut(-106, 106, -1, 6, z0 - 1, z0 + TP + 1))", "p = p.cut(kut(-36, 36, -1, 6, z0 - 1, z0 + TP + 1))")
rep(".cut(silz(0, CY, 25.2, ZF - 3.0, ZF + 1))", ".cut(silz(0, CY, RT + 3.2, ZF - 3.0, ZF + 1))")
rep("for s in (1, -1): p = p.cut(silz(s * 33.0, CY, 2.0, ZF - 6.5, ZF + 1))", "for s in (1, -1): p = p.cut(silz(s * (RT + 11.0), CY, 2.0, ZF - 6.5, ZF + 1))")
rep("for s in (1, -1): p = p.cut(silz(s * 125.0, 70.0, 5.1, z0 - 1, z0 + TP + 1))", "for s in (1, -1): p = p.cut(silz(s * 55.0, 70.0, 5.1, z0 - 1, z0 + TP + 1))")
rep("kulp = silz(-96, 340, 6.0, ZF + 0.2, ZF + 48).union(silz(96, 340, 6.0, ZF + 0.2, ZF + 48)).union(silx(340, ZF + 42, 5.0, -96, 96))",
    "kulp = silz(-48, 340, 6.0, ZF + 0.2, ZF + 48).union(silz(48, 340, 6.0, ZF + 0.2, ZF + 48)).union(silx(340, ZF + 42, 5.0, -48, 48))")
rep("kulp = kulp.cut(silz(-96, 340, 3.0, ZF, ZF + 15)).cut(silz(96, 340, 3.0, ZF, ZF + 15))", "kulp = kulp.cut(silz(-48, 340, 3.0, ZF, ZF + 15)).cut(silz(48, 340, 3.0, ZF, ZF + 15))")
rep('"Boru kulp 192 mm · M6 dişi"', '"Boru kulp 96 mm · M6 dişi"')
rep("kapak.union(kut(min(s * 130.5, s * 133.5), max(s * 130.5, s * 133.5), Y_UST - 6, Y_UST + 0.1, -100, 100)).cut(sily(s * 60.0, 0.0, 11.0, Y_UST - 1, Y_UST + 5))",
    "kapak.union(kut(min(s * 63.5, s * 66.5), max(s * 63.5, s * 66.5), Y_UST - 6, Y_UST + 0.1, -100, 100)).cut(sily(s * 30.0, 0.0, 11.0, Y_UST - 1, Y_UST + 5))")
rep('tüp geçişi Ø44 + fatura Ø50,4 × 3 · yatak Ø22,4 · 2 × M4"', 'tüp geçişi Ø72 + fatura Ø78,4 × 3 · yatak Ø22,4 · 2 × M4"')

# ---------- helezon ----------
rep("ZC1, ZC2 = bolme_z(19), bolme_z(35)      #", "ZC1, ZC2 = bolme_z(10), bolme_z(20)      #")
rep("ZC1, ZC2 = bolme_z(19), bolme_z(35)\n", "ZC1, ZC2 = bolme_z(10), bolme_z(20)\n")
rep("arkada 60 mm KONİK KÖK Ø26 → Ø16", "arkada 60 mm KONİK KÖK Ø30 → Ø18")
rep('"hatve %.2f → %.2f · θ tam 12 tur"', '"hatve %.2f → %.2f"')
rep('"tüp içi ÇİFT AĞIZ hatve 36 + 6 çırpıcı pim + ön muylu Ø12"', '"tüp içi TEK ağız sabit hatve, ağzın üstüne kadar · pim YOK (eti sıvar) · ön muylu Ø12"')
rep("            for faz in (faz0, faz0 + 180.0): g = kaynat(g, kanat_sabit(UC_HATVE, UC_Z0, UC_Z1, faz), ad + \" kanat\")",
    "            g = kaynat_kanat(g, kanat_sabit(UC_HATVE, UC_Z0, UC_Z1, faz0), ad + \" kanat\")            # TEK ağız: yüzey az → daha az yapışma")
blok("            for sira, a0 in enumerate((20.0, 200.0)):", "            g = kaynat(g, silz(0, CY, 6.0, 233.0, 253.0), \"muylu\")", "")
rep('"SLS PA12 ya da PETG baskı (seri üretimde tek parça POM)"', '"DENEME: PETG / PA12 baskı · ÜRETİM: POM-C talaşlı, Ra ≤ 0,8 (çiğ et teması)"')
rep("kotu = [b * 5 for b in dilim if mx.get(b, 0.0) < 19.9]", "kotu = [b * 5 for b in dilim if mx.get(b, 0.0) < R_KANAT - 0.1]")
rep("TAMAM: kanat her yerde Ø40", "TAMAM: kanat her yerde Ø68")
rep("r_ic=R_MIL - 0.8, r_dis=R_KANAT, kal=3.0):", "r_ic=R_MIL - 0.8, r_dis=R_KANAT, kal=4.0):")
rep("def kanat_surekli(z_bas, z_son, r_dis=R_KANAT, kal=3.0, adim=0.25):", "def kanat_surekli(z_bas, z_son, r_dis=R_KANAT, kal=4.0, adim=0.25):")
# hatve ölçümü: Ø56'da θ=0 penceresi (±0,6 mm) ±1,2° eder → hatve 48'de yüz başına ±0,16 mm, farkta ±0,33 mm ÖLÇÜM gürültüsü. Ağ inceltildi, eşik 0,40.
rep("vs, _ = tek.val().tessellate(0.05, 0.1)", "vs, _ = tek.val().tessellate(0.03, 0.05)")
rep("if abs(olc - bek) > 0.25:", "if abs(olc - bek) > 0.40:")

# ---------- tüp + yatak kapağı + tapa ----------
blok("    # ---- 6 ÇIKIŞ TÜPÜ + YATAK KAPAĞI ----", "    # ---- 7 KARIŞTIRICI ----", '''    # ---- 6 ÇIKIŞ TÜPÜ + YATAK KAPAĞI ----
    RD = RT + 3.0                                                                                        # tüp dış yarıçapı
    tup = silz(0, CY, RD, ZF - 2.8, TUP_Z1)
    flans = silz(0, CY, RD + 6.0, ZF, ZF + 5.0).union(kut(-(RD + 16.0), RD + 16.0, CY - 9, CY + 9, ZF, ZF + 5.0))
    bilezik = kut(-AG_X - 3, AG_X + 3, Y_AGIZ, CY, AG_Z0 - 3, AG_Z1 + 3)                                  # aşağı bakan kısa MEME: harç ip gibi iner
    tup = tup.union(flans).union(bilezik).cut(silz(0, CY, RT, ZF - 4, TUP_Z1 + 1)).cut(kut(-AG_X, AG_X, Y_AGIZ - 1, CY, AG_Z0, AG_Z1))
    for s in (1, -1): tup = tup.cut(silz(s * (RD + 8.0), CY, 2.25, ZF - 1, ZF + 6))
    for a in (90.0, 210.0, 330.0):
        tup = tup.union(cq.Workplane(obj=silx(0, 0, 2.5, RD - 0.5, RD + 3.0).val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a).translate(cq.Vector(0, CY, 240.0))))
    ekle("cikis_tupu", tup, "cam", bom=("Çıkış tüpü + meme", 1, "PC / PETG şeffaf · baskı ya da torna + freze", "iç Ø72 · ön plakaya faturalı + 2 × M4 · ilk 35 mm KAPALI (macun tıkacı) · alt meme 30 × 30 · 3 bayonet pimi"))
    for s in (1, -1): ekle("vida_tup_%s" % ("a" if s > 0 else "b"), silz(s * (RD + 8.0), CY, 3.5, ZF + 5.0, ZF + 7.8).union(silz(s * (RD + 8.0), CY, 1.95, ZF - 5.5, ZF + 5.0)), "celik",
                           bom=("Vida M4 × 12 silindir başlı", 2, "A2 · DIN 912", "tüp flanşını ön plakaya bağlar") if s > 0 else None)
    kp = silz(0, CY, RD + 4.0, 236.0, 254.5).cut(silz(0, CY, RD + 0.3, 235.0, TUP_Z1)).cut(silz(0, CY, 6.2, TUP_Z1 - 1, 253.2))
    kp = kp.union(kut(-(RD - 1.0), RD - 1.0, CY - 4, CY + 4, 254.5, 266.0))
    for a in (90.0, 210.0, 330.0):
        giris = kut(RD - 0.2, RD + 4.5, -2.9, 2.9, 235.0, 243.0)
        halka = cq.Workplane("XY").circle(RD + 4.5).circle(RD - 0.2).extrude(5.8).translate((0, 0, 237.1)).intersect(
            cq.Workplane("XY").polyline([(0, 0), (80, -4), (80 * math.cos(math.radians(44)), 80 * math.sin(math.radians(44)))]).close().extrude(30).translate((0, 0, 230)))
        yuva = giris.union(halka).val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a - 35.0).translate(cq.Vector(0, CY, 0))   # kapak KİLİTLİ konumda
        kp = kp.cut(cq.Workplane(obj=yuva))
    ekle("yatak_kapagi", kp, "pom", bom=("Yatak kapağı (bayonet)", 1, "POM / PETG baskı", "çeyrek tur · ön muyluyu Ø12,4 yatakta taşır · sökünce helezon öne çekilir"))
    ekle("tasima_tapasi", kut(-AG_X - 5.4, AG_X + 5.4, 0.5, Y_AGIZ + 4.5, AG_Z0 - 5.4, AG_Z1 + 5.4).union(kut(AG_X + 5.4, AG_X + 22, 0.5, 2.5, 205, 220))
         .cut(kut(-AG_X - 3.2, AG_X + 3.2, 2.5, Y_AGIZ + 4.6, AG_Z0 - 3.2, AG_Z1 + 3.2)), "silikon",
         bom=("Taşıma tapası", 1, "TPU 95A baskı", "kap makine dışındayken memeye takılır · makineye sürmeden çıkarılır"))

''')

# ---------- besleme rotoru ----------
blok("    # ---- 7 KARIŞTIRICI ----", "    kovan = silz(0, YC, 16.0,", '''    # ---- 7 BESLEME ROTORU: kıyma kendi akmaz → iki SIYIRICI LAMA duvarı sıyırır, eti helezon boğazına iter ----
    Kg = "karistirici"
    ekle("kar_mil", karez(0, YC, KARE, -163.0, 205.0), "celik", Kg, bom=("Kare çubuk 8 × 8 × 368", 1, "AISI 304", "rotor mili · öne çekilip çıkarılır"))
    R_LAMA, LAMA_G, LAMA_K, LAMA_ACI, R_KOL = 57.0, 15.0, 3.0, 20.0, 60.0          # lama merkezi r · genişlik · kalınlık · eğim · kol ucu
    def lama(g, k, z0, z1):                                                          # yerel: kol +x yönünde, lama kendi ekseninde LAMA_ACI eğik
        b = cq.Workplane("XY").center(R_LAMA, 0).rect(g, k).extrude(z1 - z0).translate((0, 0, z0))
        return cq.Workplane(obj=b.val().rotate(cq.Vector(R_LAMA, 0, 0), cq.Vector(R_LAMA, 0, 1), LAMA_ACI))
    def yerine(wp, a): return cq.Workplane(obj=wp.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a).translate(cq.Vector(0, YC, 0)))
    def orumcek(z0, z1):
        o = silz(0, YC, 14.0, z0, z1); zo = (z0 + z1) / 2
        for a in (0.0, 180.0):
            kol = kut(6.0, R_KOL, -7.0, 7.0, zo - 7, zo + 7).cut(lama(LAMA_G + 0.3, LAMA_K + 0.3, z0 - 1, z1 + 1))   # lama yuvası: ucu AÇIK çentik, lama koldan 4 mm taşar
            o = o.union(yerine(kol, a))
        return o.cut(karez(0, YC, KARE + 0.3, z0 - 1, z1 + 1))
    for ad, z0, z1 in (("arka", -150.5, -133.0), ("orta", -7.0, 7.0), ("on", 133.0, 150.5)):
        ekle("orumcek_" + ad, orumcek(z0, z1), "pom", Kg, bom=("Rotor göbeği · 2 kollu", 3, "DENEME: PETG / PA12 baskı · ÜRETİM: POM-C ya da kaynaklı 304", "2 kol: lamaları r 57'de 20° eğik tutar · kare delik 8,3") if ad == "arka" else None)
    for i, a in enumerate((0.0, 180.0)):
        ekle("cubuk_%d" % i, yerine(lama(LAMA_G, LAMA_K, -146.0, 146.0), a), "celik", Kg, bom=("Sıyırıcı lama 15 × 3 × 292", 2, "AISI 304 lama · kenarları kırık", "çentiklere sıkı geçer · duvarı 2–3 mm'den sıyırır, eti boğaza iter") if i == 0 else None)
''')
rep('"içeriden takılır · plakada döner · mil içinden kayar · teğet pim deliği"', '"içeriden takılır · plakada döner · mil içinden kayar · teğet pim deliği · KAŞAR KABIYLA ORTAK"')

# ---------- makine tarafı (yalnız yerleşim) ----------
blok("def makine():", "def ag(wp, tol=0.12, aci=0.35):", '''def makine():
    """YALNIZ YERLEŞİM. 140'lık kasette redüktörler DİKEY dizilir: NMRV030 90° çevrili (97 × 81 × 63), üstteki motor YUKARI,
    alttaki AŞAĞI bakar — yana bakarsa (kaşar kabındaki gibi) komşu kasetin arkasına taşar."""
    zc = (AG_Z0 + AG_Z1) / 2; y_pide = -40.0; y_tabla = y_pide - 8.0                 # macun ipi kısa düşmeli: meme → pide ≈ 48 mm (tepsiyi robot getirir)
    ekle("M_arka_duvar", kut(-70, 70, -20, 360, ZB - 97, ZB - 95), "cam")
    for ad, y, yon in (("helezon", CY, -1), ("karistirici", YC, 1)):
        z1 = ZB - 32.0; z0 = z1 - 63.0
        motor = kut(-yon * 1.5 - 57 * (yon < 0), -yon * 1.5 + 57 * (yon > 0), min(y + yon * 40.5, y + yon * 130.5), max(y + yon * 40.5, y + yon * 130.5), z0 + 3, z1 - 3)
        ekle("M_red_" + ad, kut(-48.5, 48.5, y - 40.5, y + 40.5, z0, z1).union(motor), "koyu")
        yuva = silz(0, y, 21.0, ZB - 30.0, ZB - 9.5).cut(kut(-18.5, 18.5, y - 4.4, y + 4.4, ZB - 20, ZB - 8)).cut(kut(-4.4, 4.4, y - 18.5, y + 18.5, ZB - 20, ZB - 8)).cut(silz(0, y, 13.4, ZB - 20, ZB - 8))
        ekle("M_yuva_" + ad, yuva, "celik", "helezon" if ad == "helezon" else "karistirici")
    for s in (1, -1):
        ekle("M_konum_pimi_%s" % ("a" if s > 0 else "b"), silz(s * 55.0, 70.0, 5.0, ZB - 95, ZB + 6.0), "celik")
        ekle("M_ray_%s" % ("a" if s > 0 else "b"), kut(min(s * 40, s * 70), max(s * 40, s * 70), -6.0, 0.0, ZB - 40, ZF + 120), "koyu")
    xt = -YASA["r_dis"]
    ekle("M_tabla", sily(xt, zc, 170.0, y_tabla - 12, y_tabla), "celik", "tabla"); ekle("M_pide", sily(xt, zc, 140.0, y_tabla, y_pide), "hamur", "tabla")
    ekle("M_kolon", sily(xt, zc, 20.0, y_tabla - 70, y_tabla - 12), "koyu", "kolon")
    return zc, y_pide, xt


''')
rep("aci=lambda t: -7.0 * min(t, T_DOK) / T_DOK)", "aci=lambda t: -2.4 * min(t, T_DOK) / T_DOK)")      # ≈ 20 dev/dk (VARSAYIM: doluluk 0,4)
rep("aci=lambda t: 1.0 * min(t, T_DOK) / T_DOK)", "aci=lambda t: 0.67 * min(t, T_DOK) / T_DOK)")       # rotor 4 dev/dk, ters
rep("-0.187, 0.2125)", "-0.187, 0.213)")


# ---------- tabla animasyonu ÜRÜNÜN KENDİ hareket yasasıyla (kaşarınkiyle değil) ----------
rep("from kasar_akis_model_v2 import YASA, T_DOK, r_t\n",
    "from kasar_akis_model_v2 import YASA, T_DOK, r_t\n"
    "import kiyma_akis_model_v2 as AM                                     # ürünün kendi akış modeli: tabla yasası + hesap sayıları buradan\n"
    "R0 = AM.r_t_k(0.0)                                                   # doz başında ağzın pide merkezine uzaklığı\n")
rep('    xt = -YASA["r_dis"]\n', '    xt = -R0\n')
rep('_kay = lambda t: ((YASA["r_dis"] - r_t(t)) * MM if t <= T_DOK else (YASA["r_dis"] - YASA["r_ic"]) * MM * (DONGU - t) / (DONGU - T_DOK), 0.0, 0.0)',
    '_kay = lambda t: ((R0 - AM.r_t_k(t)) * MM if t <= T_DOK else (R0 - AM.r_t_k(T_DOK)) * MM * (DONGU - t) / (DONGU - T_DOK), 0.0, 0.0)')
rep('"tabla": dict(pivot=(-YASA["r_dis"] * MM, -0.187, 0.213), eksen="y", aci=lambda t: 7.0 * t / DONGU, kay=_kay),',
    '"tabla": dict(pivot=(-R0 * MM, -0.187, 0.213), eksen="y", aci=lambda t: AM.tabla_tur(t), kay=_kay),')

# ---------- denetim metinleri ----------
rep('"örümcek gözü ↔ kâse (4,25)"', '"rotor kolu ↔ kâse"')
rep('"çubuk ↔ kâse (7,0)"', '"SIYIRICI LAMA ↔ kâse (hedef 2–3)"')
rep('"kanat / pim ↔ tüp (2,0)"', '"kanat ↔ tüp (2,0)"')
rep("# R124 kolu AŞAĞI bakarken", "# rotor kolu AŞAĞI bakarken")
rep('"örümcek gözü ↔ helezon kanadı (5,25)", round(dA, 2)))', '"rotor kolu ↔ helezon kanadı", round(dA, 2)))')
rep('dA, "örümcek gözü ↔ helezon kanadı (5,25)"))', 'dA, "rotor kolu ↔ helezon kanadı"))')

# ---------- web modeli ----------
i = s.index("    # ---- web modeli ----")
s = s[:i] + '''    # ---- web modeli ----
    V = v4.hacim_L(Y_DOLUM); yd = v4.dolum_kotu(KG2 / RHO)
    print("HACIM %.1f L (ic boy %.0f) · %.1f kg @ %.2f → dolum kotu y %.0f (%%%.0f)" % (V, D - 2 * TP, KG2, RHO, yd, 100 * KG2 / RHO / V))
    Gm = AM.G                                                               # CAD ile HESAP aynı sayıları mı kullanıyor?
    for k_, v_ in dict(RT=RT, R_MIL=R_MIL, R_KOK=R_KOK, P0=HATVE0, T=4.0).items(): assert abs(Gm[k_] - v_) < 1e-6, "model ile CAD ayni degil: %s %s != %s" % (k_, Gm[k_], v_)
    assert abs(Gm["P1"] - HATVE1) < 0.05 and abs(AM.AGIZ[0] - 2 * AG_X) < 1e-6 and abs(AM.AGIZ[1] - (AG_Z1 - AG_Z0)) < 1e-6 and abs(AM.RHO - RHO) < 1e-9 and abs(AM.KG2 - KG2) < 1e-9
    Vt = math.pi / 4.0 * ((2 * R_KANAT + 4.0) ** 2 - (2 * R_MIL) ** 2) * (HATVE1 - 4.0) / 1000.0
    print("MODEL = CAD · uc hatve %.1f · kuramsal %.0f mL/tur · doluluk 0,40 VARSAYIM → %.0f g/tur · 160 g = %.1f tur · %.0f dev/dk" % (HATVE1, Vt, Vt * 0.4 * RHO, 160.0 / (Vt * 0.4 * RHO), 160.0 / (Vt * 0.4 * RHO) * 6.0))
    dokular = {"ad": doku_ad("KIYMA KASETİ", "bu yönde tak  ·  140 × 325 × 360 mm  ·  %s L  ·  çıkış ÖNDE alttan" % ("%.1f" % V).replace(".", ","), ok_sol=True),
               "montaj": doku_montaj(["HELEZONU|ÖNDEN SÜR", "YATAK KAPAĞI|ÇEYREK TUR", "ROTOR · MİL|TOPUZ · PİM", "TAPAYI ÇIKAR|YUVAYA SÜR"])}
    def etiketler():
        e0, e1 = (Y_UST - 56) * MM, (Y_UST - 8) * MM; ez = (D / 2 - TP - 6) * MM; xo = (RB + ET + 0.4) * MM; L = []
        L.append(("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1), "etiket_ad", None)); L.append(("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1), "etiket_montaj", None))
        for adi, xx, nx in (("etiket_ad_arka", -xo + 0.0002, 1), ("etiket_montaj_arka", xo - 0.0002, -1)):
            ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); L.append((adi, ar.duzelt(), "sari_arka", None))
        return L
    kap_ag = [(p["ad"], ag(p["wp"]), p["mal"], p["grup"]) for p in PARCALAR if p["ad"] != "tasima_tapasi"] + etiketler()
    b1 = glb_yaz(os.path.join(OUT, "kiyma_v3.glb"), kap_ag, dokular)
    print("kiyma_v3.glb · %d parca · %d ucgen · %.0f KB" % (len(kap_ag), sum(len(m.I) // 3 for _, m, _, _ in kap_ag), b1 / 1024.0))
    b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, "kiyma_v3.usdz")], "kiyma_v3", [(a, m, mal) for a, m, mal, _ in kap_ag], dokular)
    print("   usdz %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI")); [print("   HATA:", x) for x in sorun]
    n0 = len(PARCALAR); zc, y_pide, xt = makine()
    doz = kap_ag + [(p["ad"], ag(p["wp"]), p["mal"], p["grup"]) for p in PARCALAR[n0:]]
    # pide üstünde GERÇEKTE oluşan şey: 30 × 30 meme 10 sn'de yalnız 178 mm şerit serer (süreklilik: şerit hızı = yüzey hızı).
    # Eskiden buraya pideyi kaplayan 420 pul çiziliyordu — hesabın göstermediği bir kaplamayı gösteriyordu, kaldırıldı.
    ks = Mesh(); sp = AM._SP; adim_ = max(1, len(sp) // 40)
    for i in range(0, len(sp) - adim_, adim_):
        (t0_, r0_, th0_), (t1_, r1_, th1_) = sp[i], sp[i + adim_]; tm = (th0_ + th1_) / 2.0; rm = (r0_ + r1_) / 2.0; boy = rm * (th1_ - th0_) + 1.0
        kx, kz = xt + rm * math.cos(tm), zc + rm * math.sin(tm)                             # pide çerçevesinde şeridin ekseni (tabla −θ döndüğü için iz +θ'ya uzar)
        b = kut(-AM.AGIZ[0] / 2, AM.AGIZ[0] / 2, y_pide + 0.2, y_pide + 0.2 + AM.AGIZ[1] * 0.55, -boy / 2, boy / 2)
        b = cq.Workplane(obj=b.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), -math.degrees(tm)).translate(cq.Vector(kx, 0, kz)))
        ks.ekle(ag(b))
    doz.append(("harc_seridi", ks, "kiyma", "tabla"))
    doz.append(("harc_ipi", ag(sily(0.0, zc, 11.0, y_pide + 2.0, Y_AGIZ)), "kiyma", None))                       # memeden inen macun ipi
    dolgu = v4.kasar_dolgu(yd); doz.append(("kiyma_dolgu", dolgu, "kiyma_dolgu", None))
    b3 = glb_yaz(os.path.join(OUT, "kiyma_v3_dozaj.glb"), doz, dokular)
    print("kiyma_v3_dozaj.glb · %d parca · %.0f KB · toplam %.0f sn" % (len(doz), b3 / 1024.0, time.time() - t0))
'''
n[0] += 1
io.open(os.path.join(U, "kiyma_cad_v3.py"), "w", encoding="utf-8").write(s)
print("kiyma_cad_v3.py yazildi ·", n[0], "yama")
