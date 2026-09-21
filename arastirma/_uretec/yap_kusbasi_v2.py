# -*- coding: utf-8 -*-
"""kiyma_cad_v1.py → kusbasi_cad_v1.py · aynı 140 gövde ve aynı besleme rotoru; helezon, tüp, ağız ve EŞİK kuşbaşı (iri ıslak tane) için.
Sayılar kusbasi_akis_model_v1.G ile AYNI olmak zorunda — üreteç çalışırken karşılaştırır."""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kiyma_cad_v3.py"), encoding="utf-8").read(); n = [0]
def rep(a, b, hepsi=False):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    s = s.replace(a, b) if hepsi else s.replace(a, b, 1); n[0] += 1
def blok(bas, son, yeni):
    global s
    i = s.index(bas); j = s.index(son, i + len(bas)); s = s[:i] + yeni + s[j:]; n[0] += 1

for a, b in (("kiyma_kaseti_v3", "kusbasi_kaseti_v2"), ("KIYMA_KASETI_v3", "KUSBASI_KASETI_v2"), ("kiyma_v3", "kusbasi_v2"), ("kiyma_cad_v3", "kusbasi_cad_v2"), ("kiyma_akis_model_v2 as AM", "kusbasi_akis_model_v2 as AM")):
    s = s.replace(a, b)

i = s.index('"""'); j = s.index('"""', i + 3) + 3
s = s[:i] + '''"""AUTOKITCH · KUŞBAŞI KASETİ v2 — ÜRETİM MODELİ (22 Eyl 2026) · ORTAK GÖVDE · kiyma_cad_v3'ten türetildi (yap_kusbasi_v2.py)
v2: gövde + iki uç plakası + kapak + kulp + saplamalar KIYMA v3 ile BİREBİR AYNI (kâse merkezi 177 → 164). Rotor KISA kollu: lama duvara 19, kanada 22 mm — küp hiçbir yerde sıkışmaz.
HESAP: kusbasi_akis_model_v1.py — tasarımı TEK sayı yönetiyor: KÜP KENARI d (VARSAYIM 10 mm; 12'ye kadar çalışır, 15'te çalışmaz).
ÜRÜN: pidelik kuşbaşı, ıslak yumuşak iri tane · 145 g / pide · 20 pide / gün → 2 gün 5,8 kg · dökme 0,80 g/mL (VARSAYIM; 1 cup = 170–198 g)
KURALLAR → ÖLÇÜLER
  · köprü: düşey açıklık ≥ 4 d (BulkInside)        → boğaz = tekne Ø72 (d 10'da 7,2 d) · ağız 48 × 44
  · topak: mil–tekne radyal boşluk ≥ R·d (CEMA)     → 28 mm = 2,8 d (sınıf 2+) · konik kökte 22 = 2,2 d
  · kanatlar arası net boşluk ≥ 3 d                 → hatve 40 → 50,3 (kanat 4 mm) · ÇİFT AĞIZ OLMAZ (boşluk yarıya iner)
  · iki hareketli yüzey arası: ya < d/3 ya > 1,5 d  → lama–duvar 2,4 (küp giremez) · rotor–kanat 18 (küp sıkışmaz)
KIYMA KASETİNDEN FARKLAR: helezon Ø68 / mil Ø16 / kök Ø28 · kanat 4 mm · tüp iç Ø72 · kanat ağızdan 18 mm ÖNCE biter: yatak TIKAÇ olarak
  6 mm'lik EŞİĞİN üstünden itilir → küpler tek tek düşer (tur başına öbek yok) ve eşiğin arkasında ≈ 50 mL et suyu tutulur, ağızdan damlamaz.
  Besleme rotoru, göbekler, kavramalar, kovan, topuz, pimler, miller, saplamalar KIYMA ve KAŞAR ile ORTAK.
UYARI: baskı parça yalnız DENEME içindir; çiğ et teması = 304/316 + POM-C talaşlı.
ÇIKTI: otonom/kaset3d/kusbasi_v2.glb/.usdz + kusbasi_v2_dozaj.glb · arastirma/3_TOPPING/kusbasi_kaseti_v2/
"""''' + s[j:]

# ---- sabitler ----
rep("R_MIL, R_KANAT, KARE = 9.0, 34.0, 8.0", "R_MIL, R_KANAT, KARE = 8.0, 34.0, 8.0")
rep("KOK_Z0, KOK_Z1, R_KOK = -91.0, -151.0, 15.0", "KOK_Z0, KOK_Z1, R_KOK = -91.0, -151.0, 14.0")
rep("KAN_Z0, KAN_Z1, HATVE0, TUR = -148.0, 156.0, 36.0, 7.25", "KAN_Z0, KAN_Z1, HATVE0, TUR = -148.0, 156.0, 40.0, 6.75")
rep("UC_HATVE, UC_Z0, UC_Z1 = None, 156.0, 228.0", "UC_HATVE, UC_Z0, UC_Z1 = None, 156.0, 170.0")
rep("AG_Z0, AG_Z1, AG_X = 198.0, 228.0, 15.0\nY_AGIZ = 8.0", "AG_Z0, AG_Z1, AG_X = 188.0, 232.0, 24.0\nESIK_Y, ESIK_Z0 = 6.0, 182.0                                        # eşik: 6 mm yüksek, ağzın hemen arkasında 6 mm boy\nY_AGIZ = 6.0")
rep("RHO = 1.0 ", "RHO = 0.80")
rep("KG2 = 6.4 ", "KG2 = 5.8 ")
rep("MALZEME.setdefault('kiyma', dict(renk=(0.62, 0.27, 0.22, 1.0)", "MALZEME.setdefault('kusbasi', dict(renk=(0.55, 0.17, 0.16, 1.0)")
rep("MALZEME.setdefault('kiyma_dolgu', dict(renk=(0.62, 0.27, 0.22, 1.0)", "MALZEME.setdefault('kusbasi_dolgu', dict(renk=(0.55, 0.17, 0.16, 1.0)")
rep("ZC1, ZC2 = bolme_z(10), bolme_z(20)      #", "ZC1, ZC2 = bolme_z(9), bolme_z(18)      #")
rep("ZC1, ZC2 = bolme_z(10), bolme_z(20)\n", "ZC1, ZC2 = bolme_z(9), bolme_z(18)\n")
rep("arkada 60 mm KONİK KÖK Ø30 → Ø18", "arkada 60 mm KONİK KÖK Ø28 → Ø16")
rep('"tüp içi TEK ağız sabit hatve, ağzın üstüne kadar · pim YOK (eti sıvar) · ön muylu Ø12"', '"tüp içinde kanat ağızdan 18 mm ÖNCE biter (yatak tıkaç olarak itilir) · ağız üstünde çıplak mil · ön muylu Ø12"')

# ---- tüp: eşik ----
rep("    for s in (1, -1): tup = tup.cut(silz(s * (RD + 8.0), CY, 2.25, ZF - 1, ZF + 6))",
    "    esik = silz(0, CY, RT + 0.5, ESIK_Z0, AG_Z0).intersect(kut(-RT - 1, RT + 1, CY - RT - 1, CY - RT + ESIK_Y, ESIK_Z0 - 1, AG_Z0 + 1))   # EŞİK: tüp tabanında hilal\n"
    "    tup = tup.union(esik)\n"
    "    for s in (1, -1): tup = tup.cut(silz(s * (RD + 8.0), CY, 2.25, ZF - 1, ZF + 6))")
rep('"iç Ø72 · ön plakaya faturalı + 2 × M4 · ilk 35 mm KAPALI (macun tıkacı) · alt meme 30 × 30 · 3 bayonet pimi"',
    '"iç Ø72 · ön plakaya faturalı + 2 × M4 · kapalı bölümde 6 mm EŞİK (et suyunu tutar, akışı sürekli yapar) · alt ağız 48 × 44 · 3 bayonet pimi"')
rep('"Çıkış tüpü + meme"', '"Çıkış tüpü + eşik"')
rep('"kap makine dışındayken memeye takılır · makineye sürmeden çıkarılır"', '"kap makine dışındayken ağız bileziğine takılır · makineye sürmeden çıkarılır"')
rep('"çentiklere sıkı geçer · duvarı 2–3 mm\'den sıyırır, eti boğaza iter"', '"çentiklere sıkı geçer · duvara 19 mm · kanada 22 mm (ikisi de ≥ 1,5 d: küp sıkışmaz) · köprüyü bozar"')
rep('"DENEME: PETG / PA12 baskı · ÜRETİM: POM-C talaşlı, Ra ≤ 0,8 (çiğ et teması)"', '"DENEME: PETG / PA12 baskı, kanat 4 mm · ÜRETİM: POM-C talaşlı (çiğ et teması)"')

# ---- rotor KISA kollu: küp ne duvarla lama arasına ne de lamayla kanat arasına sıkışsın (iki aralık da ≥ 1,5 d) ----
rep("R_LAMA, LAMA_G, LAMA_K, LAMA_ACI, R_KOL = 57.0, 15.0, 3.0, 20.0, 60.0", "R_LAMA, LAMA_G, LAMA_K, LAMA_ACI, R_KOL = 40.0, 15.0, 3.0, 20.0, 43.0")
rep("2 kol: lamaları r 57'de 20° eğik tutar", "2 KISA kol: lamaları r 40'ta 20° eğik tutar")

# ---- dozaj animasyonu ----
rep("aci=lambda t: -2.4 * min(t, T_DOK) / T_DOK)", "aci=lambda t: -2.1 * min(t, T_DOK) / T_DOK)")            # ≈ 13 dev/dk (doluluk 0,60)
rep("-0.187, 0.213)", "-0.187, 0.210)")

# ---- web modeli: hesap satırı + küpler ----
blok("    Gm = AM.G ", "    dokular = {", '''    import kusbasi_akis_model_v2 as KM                                    # CAD ile HESAP aynı sayıları mı kullanıyor?
    Gm = KM.G; esit = dict(RT=RT, R_MIL=R_MIL, R_KOK=R_KOK, P0=HATVE0, ESIK=ESIK_Y, T=4.0)
    sup = 40.0 + math.hypot(15.0 / 2, 3.0 / 2); olc = dict((x[0] + "|" + x[1], x[3]) for x in BOSLUK)["cubuk_0|govde"]; assert abs(olc - (RB - sup)) < 0.3, "lama-duvar olcumu %.2f, beklenen %.2f" % (olc, RB - sup)
    assert abs(Gm["LAMA_DUVAR"] - (RB - sup)) < 0.2 and abs(Gm["ROTOR_BOSLUK"] - (YC - sup - CY - R_KANAT)) < 0.2, "rotor araliklari model ile ayni degil: duvar %.1f · kanat %.1f" % (RB - sup, YC - sup - CY - R_KANAT)
    for k_, v_ in esit.items(): assert abs(Gm[k_] - v_) < 1e-6, "model ile CAD ayni degil: %s %s != %s" % (k_, Gm[k_], v_)
    assert abs(Gm["P1"] - HATVE1) < 0.05 and abs(Gm["AGIZ"][0] - 2 * AG_X) < 1e-6 and abs(Gm["AGIZ"][1] - (AG_Z1 - AG_Z0)) < 1e-6 and abs(Gm["TIKAC"] + Gm["ESIK"] - (AG_Z0 - UC_Z1)) < 1e-6
    q_on = KM.kapasite(1.0)[4]; g_tur = q_on * 0.60 * RHO
    print("MODEL = CAD · on uc %.1f mL/tur (Roberts) · doluluk 0,60 VARSAYIM → %.0f g/tur · 145 g = %.2f tur · %.0f dev/dk" % (q_on, g_tur, 145.0 / g_tur, 145.0 / g_tur * 6.0))
''')
rep('doku_ad("KIYMA KASETİ",', 'doku_ad("KUŞBAŞI KASETİ",')
blok("    # pide üstünde GERÇEKTE oluşan şey", "    b3 = glb_yaz(", '''    rnd = random.Random(11); ks = Mesh(); d_k = 10.0
    for i in range(137):                                                                       # pide üstünde 137 küp (145 g · d 10)
        rr = 118.0 * math.sqrt(rnd.random()); a = rnd.uniform(0, 2 * math.pi); x, z = xt + rr * math.cos(a), zc + rr * math.sin(a)
        ks.ekle(kutu((x - d_k / 2) * MM, (x + d_k / 2) * MM, (y_pide + 0.3) * MM, (y_pide + 0.3 + d_k * 0.8) * MM, (z - d_k / 2) * MM, (z + d_k / 2) * MM))
    doz.append(("kusbasi_pide_ustu", ks, "kusbasi", "tabla")); dk = Mesh()
    for i in range(9):                                                                         # ağızdan tek tek düşen küpler
        y = rnd.uniform(y_pide + 12, Y_AGIZ - 4); x, z = rnd.uniform(-AG_X + 6, AG_X - 6), rnd.uniform(AG_Z0 + 6, AG_Z1 - 6)
        dk.ekle(kutu((x - d_k / 2) * MM, (x + d_k / 2) * MM, y * MM, (y + d_k) * MM, (z - d_k / 2) * MM, (z + d_k / 2) * MM))
    doz.append(("kusbasi_dusen", dk, "kusbasi", None))
    dolgu = v4.kasar_dolgu(yd); doz.append(("kusbasi_dolgu", dolgu, "kusbasi_dolgu", None))
''')
io.open(os.path.join(U, "kusbasi_cad_v2.py"), "w", encoding="utf-8").write(s)
print("kusbasi_cad_v2.py yazildi ·", n[0], "yama")
