# -*- coding: utf-8 -*-
"""topping_hesap_v2 + topping_cad_v2  ->  v3
Kemal (22 Eyl, modeli kesitle incelerken):
 "su sagdaki sey ne, bunu arka tarafa al ya da ust tarafa al · alt cikis nozzle yeri, o parcayi biraz daha uzun yap ki
  pideyle arasindaki en dogru mesafe olsun · neden alt kisim bu kadar kalin, kasetlerin rafi, bir sebebi var mi ·
  hersey koseler birbirine denk gelsin, en detayli calisir model ama basit standart cozumler."

v3'TE DEGISEN:
 1 KASET YUVADAN CIKMIYORDU (gercek hata, olculdu): meme yarigi yalniz agiz boyunda (42 mm) acilmisti;
   kaset one cekilince meme 6 mm sonra ic kabugun tabanina carpiyordu. Yarik artik hucre on sinirina kadar
   acik — kaset serbestce cikiyor.
 2 EVAPORATOR SAG UCTAN ARKAYA gecti: kasetlerin ARKASINDAKI kavrama bolmesine, MILLERIN USTUNE
   (y 470-620, z kavrama bolgesi) yatay olarak alindi. Kaset sirasinin yanindaki yer bosaldi, hava kanali
   artik bastan sona gidiyor. Fanlar iki kenarda.
 3 NOZZLE-PIDE MESAFESI: urun agizdan cikip robot agzina 146 mm dusuyordu. Huninin alt ucu 176 -> 140,
   yani pide ustune ~40 mm kala biten bir bacaya donustu (sacilma bu araliga gore) [V].
 4 ALT KALINLIK: 80 mm'nin 60'i PU yalitim (hesapli, incelemez), 20'si ray + kaset alti bosluktu.
   Bosluk 20 -> 10 indirildi, ray ayni kaldi: alt paket 80 -> 70 mm.
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:120]
    n[0] += 1
    return s.replace(a, b, 1)


# ================================================================ 1 · HESAP v3
h = io.open(os.path.join(U, "topping_hesap_v2.py"), encoding="utf-8").read()
h = h.replace("topping_hesap_v2", "topping_hesap_v3").replace("topping_cad_v2.py", "topping_cad_v3.py")
i = h.index('"""', h.index('"""') + 3)
h = h[:i] + ("v3 (22 Eyl 2026): urun dusme mesafesi hesaba girdi (huni bacasi), kaset alti bosluk 20 -> 10.\n") + h[i:]

h = yama(h, "# ---------------------------------------------------------------- 3 · SOĞUTMA YÜKÜ ----------------------------------------------------------------",
         '''# ---------------------------------------------------------------- 2c · ÜRÜN DÜŞME MESAFESİ (v3) ----------------------------------------------------------------
# Kemal: "nozzle uzun yap ki pideyle arasındaki en doğru mesafe olsun."
# Ürün kasetin ağzından çıkıp pidenin üstüne düşüyor. Düşme ne kadar uzun olursa tane o kadar saçılır;
# ne kadar kısa olursa meme pideye/robota çarpma riski o kadar artar.
DUSME = 40.0             # meme/baca ağzı ile pide üst yüzü arası [V: kuşbaşı 10–15 mm küp için 30–50 mm;
#                          tartılmadı, prototipte saçılma ölçülecek]
KASET_ALTI = 10.0        # kaset tabanı ile iç kabuk tabanı arası boşluk — v2'de 20'ydi (Kemal: "neden bu kadar kalın")
# Alt paketin geri kalanı ZORUNLU: PU 60 (yalıtım hesabı buna dayanıyor) + iç kabuk 1 + taban rayı 4.

# ---------------------------------------------------------------- 3 · SOĞUTMA YÜKÜ ----------------------------------------------------------------''')

h = yama(h, '                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"]),',
         '                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"], dusme=DUSME, kaset_alti=KASET_ALTI),')

io.open(os.path.join(U, "topping_hesap_v3.py"), "w", encoding="utf-8").write(h)
print("topping_hesap_v3.py yazildi")

# ================================================================ 2 · CAD v3
c = io.open(os.path.join(U, "topping_cad_v2.py"), encoding="utf-8").read()
c = c.replace("topping_hesap_v2", "topping_hesap_v3").replace("topping_cad_v2", "topping_cad_v3").replace("topping_modul_v2", "topping_modul_v3")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v3 (22 Eyl 2026): meme yarigi hucre on sinirina kadar acildi (kaset YUVADAN CIKMIYORDU) ·\n"
             "evaporator kasetlerin ARKASINA, millerin ustune · huni bacasi pideye 40 mm kala biter ·\n"
             "kaset alti bosluk 20 -> 10. Onceki: topping_cad_v2.py\n") + c[i:]

c = yama(c, '"TOPPING MODULU v2', '"TOPPING MODULU v3')

# --- 1 · kaset alti bosluk hesaptan ---
c = yama(c, "    hy0, hy1 = KAS[0] - 20.0, KAS[1] + 20.0                                   # soğuk hücre iç yüksekliği (240 … 640)",
         "    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0                            # v3: kaset altı boşluk 20 → 10 (Kemal: \"neden bu kadar kalın\")")

# --- 2 · YARIK: hucre on sinirina kadar (kaset cikabilsin) ---
c = yama(c, '''    # MEME YARIĞI kasetin KENDİ ağız ölçüsünden: kaset yerel z → modül z (kaset ön yüzü ZK[0]).
    _a0, _a1, _dd = AGIZ[280]
    ZY = (ZK[0] + (_a1 - _dd / 2.0) + 6.0, ZK[0] + (_a0 - _dd / 2.0) - 6.0)   # ağzın z aralığı + 6 mm pay''',
         '''    # MEME YARIĞI kasetin KENDİ ağız ölçüsünden: kaset yerel z → modül z (kaset ön yüzü ZK[0]).
    # v3 DÜZELTMESİ: yarık yalnız ağız boyundaydı (42 mm) ve kaset öne çekilince meme 6 mm sonra iç kabuğun
    # tabanına çarpıyordu — KASET YUVADAN ÇIKMIYORDU. Yarık artık hücrenin ÖN SINIRINA kadar açık;
    # meme o sınırı geçince zaten hücrenin dışında (kapak açık) oluyor.
    _a0, _a1, _dd = AGIZ[280]
    ZY = (ZKAP[1], ZK[0] + (_a0 - _dd / 2.0) - 6.0)                           # ön sınır … ağzın arka ucu + pay''')

# --- 3 · EVAPORATOR: kasetlerin ARKASINA, millerin ustune ---
c = yama(c, '''    # v1'de evaporatör y 520–620 · z −440…−330'daydı ve BEŞ KASETİN İÇİNE giriyordu (Kemal gördü).
    # v2: soğuk hücrenin SAĞ ucuna, son yuvanın yanındaki boşluğa DİKEY olarak alındı — kasetlerle x'te ayrı.
    EX0 = YUVA[-1][2] + BOLME + 4.0                                            # son yuvanın sağ kenarından sonra
    EX1 = XI1 - SAC_IC - 4.0
    assert EX1 - EX0 >= 120.0, "evaporatör nişi dar: %.0f mm" % (EX1 - EX0)
    ekle("evaporator", kut(EX0, EX1, KAS[0] + 20.0, KAS[1] - 20.0, ZK[0] - 30.0, ZK[0] - 140.0), "bakir",
         bom=("Evaporatör", 1, "lamelli, paslanmaz karter · dikey", "soğuk hücrenin SAĞ ucunda, kaset sırasının yanında; hesaplanan yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    for i, yy in enumerate((KAS[0] + 110.0, KAS[1] - 110.0)):
        ekle("fan_%d" % i, kut(EX0 + 6.0, EX1 - 6.0, yy - 62.0, yy + 62.0, ZK[0] - 146.0, ZK[0] - 196.0), "motor",
             bom=("Evaporatör fanı 140 × 140", 2, "24 V eksenel, 12 W", "evaporatörden çektiği havayı üstteki kanala basar") if i == 0 else None)
    # Hava kanalı v1'de y 504–508'deydi, yani KASETİN İÇİNDE (kaset üstü 620). v2: kasetin 4 mm üstünde.
    ekle("hava_kanali", kut(XI0 + SAC_IC + 2.0, EX0 - 2.0, KAS[1] + 4.0, hy1 - SAC_IC - 3.0, ZK[0] - 20.0, ZK[1] + 20.0), "sac",
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "sağdaki evaporatörden gelen soğuk havayı kaset sırasının üstünde boydan boya dağıtır"))''',
         '''    # v1: evaporatör BEŞ KASETİN İÇİNDEYDİ. v2: sağ uca dikey alındı — ama orası kaset sırasının yanı, yer yiyordu.
    # v3 (Kemal: "şu sağdaki şeyi arka tarafa al"): kasetlerin ARKASINDAKİ kavrama bölmesine, yatay.
    # Miller y 300–455 arasında; evaporatör onların ÜSTÜNDE (y 470–620) duruyor, hiçbir mile değmiyor.
    EVY = (KAS[0] + 228.0, KAS[1] - 10.0)                                      # 488 … 610 · 280'lik kasetin rotor soketi 477'de bitiyor, onun da üstünde
    EVZ = (ZKAV[0] - 2.0, ZKAV[1] + 3.0)                                       # kavrama bölmesi (kasetin arkası)
    ekle("evaporator", kut(220.0, W - 220.0, EVY[0], EVY[1], EVZ[0], EVZ[1]), "bakir",
         bom=("Evaporatör", 1, "lamelli, ince tip, paslanmaz karter", "kaset sırasının ARKASINDA, millerin üstünde; cephe %.0f × %.0f mm · hesaplanan yük %.0f W, seçim %.0f W" % (W - 440.0, EVY[1] - EVY[0], H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    for i, xx in enumerate((XI0 + 8.0, W - XI0 - 128.0)):
        ekle("fan_%d" % i, kut(xx, xx + 120.0, EVY[0] + 10.0, EVY[1] - 10.0, EVZ[0], EVZ[1]), "motor",
             bom=("Evaporatör fanı 120 × 120", 2, "24 V eksenel, 12 W", "iki kenarda; havayı evaporatörden çekip kaset sırasının üstündeki kanala basar") if i == 0 else None)
    # Hava kanalı v1'de y 504–508'deydi, yani KASETİN İÇİNDE (kaset üstü 620). v2'den beri kasetin 4 mm üstünde.
    ekle("hava_kanali", kut(XI0 + SAC_IC + 2.0, XI1 - SAC_IC - 2.0, KAS[1] + 4.0, hy1 - SAC_IC - 3.0, ZK[0] - 20.0, ZKAV[0] - 4.0), "sac",
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "arkadaki evaporatörden gelen soğuk havayı kaset sırasının üstünde baştan sona dağıtır"))''')

# --- 4 · HUNI: pideye DUSME kadar kala biten baca ---
c = yama(c, '''        ekle("huni_%s" % k, kut(x0 + 22.0, x1 - 22.0, hy0 - PU - 4.0, KAS[0] - 4.0, ZY[0] - 2.0, ZY[1] + 2.0)
             .cut(kut(x0 + 25.0, x1 - 25.0, hy0 - PU - 5.0, KAS[0] - 3.0, ZY[0] - 5.0, ZY[1] + 5.0)), "sac", bom=None)''',
         '''        # v3: huni artık pide üstüne DUSME kala biten bir BACA. Ağzı kasetin meme ölçüsünde daralıyor;
        # üst kısmı yarığın tamamını kavrıyor ki kaset çekilirken meme serbest kalsın.
        hb0, hb1 = AGZ[1] + H.DUSME, KAS[0] - 4.0                              # baca alt ucu … kasetin altı
        huni = kut(x0 + 22.0, x1 - 22.0, hb0, hb1, ZY[0] - 2.0, ZY[1] + 2.0)
        huni = huni.cut(kut(x0 + 25.0, x1 - 25.0, hb0 - 1.0, hb1 - 3.0, ZY[0] - 5.0, ZY[1] + 5.0))
        ekle("huni_%s" % k, huni, "sac", bom=None)''')

c = yama(c, '("_bom_huni", "Dozaj hunisi", 6, "304 1,0 mm, çekip çıkarılır", "memeden çıkanı aşağıdaki robot ağzına yönlendirir; yıkamak için sökülür")',
         '("_bom_huni", "Dozaj bacası", 6, "304 1,0 mm, çekip çıkarılır", "memeden çıkanı pide üstüne %.0f mm kala indirir; yıkamak için sökülür" % H.DUSME)')

io.open(os.path.join(U, "topping_cad_v3.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v3.py yazildi ·", n[0], "yama")
