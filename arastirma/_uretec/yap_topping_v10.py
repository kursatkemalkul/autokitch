# -*- coding: utf-8 -*-
"""topping_cad_v9 -> topping_cad_v10   ·   DONER TABLA: TAM URETIM MODELI
Kemal (22 Eyl): "bu tabla nasil xyz'de hareket ediyor, nasil donuyor kendi etrafinda — bunu HERSEYIYLE
URETIME YONELIK ciz, MOTORUNA KADAR VIDASINA KADAR o sistemi orda kur; uretim ve calismasi dogru olucak."

v9'daki tabla 9 adet YER TUTUCU BLOKTU — parcalarin hicbiri birbirine baglanmiyordu. v10'da gercek mekanizma:

X EKSENI (kayis tahrikli tek araba):
  sag uctaki sabit NEMA23 -> GT3 20 dis kasnak (cevre tam 60,00 mm/tur) -> acik uclu kayis sol uctaki
  avaraya gidip doner, iki ucu arabanin altindaki kola KELEPCELENIR. Araba iki HGR15 rayda 4 blokla gezer.
  Gergi sol uctaki avara braketinde (yuva + itme vidasi) — agizdan elle erisilir.
  Kayis z -360'ta, yani TEPSI GOLGESININ (0...-340) DISINDA: urun duzleminin altinda tahrik elemani yok.

DONUS EKSENI (es eksenli DOGRUDAN tahrik, i = 1):
  PANCAKE NEMA23 (57 x 57 x 41) araba plakasinin ALTINA flansli, ekseni tabla ekseniyle AYNI.
  Redüktor yok, kayis yok. Gereken tork 0,169 N·m, motor ~0,9 N·m -> ~5 kat pay.
  Tabla ince kesit DONER YATAK (slewing ring) uzerinde: O340 konsol tablanin devirme momentini o alir.
  Motor -> tahrik lokmasi -> 2 x O8 pim -> tabla gobegi. Rijit kaplin YOK: tabla duseyde ayrilabiliyor,
  mil yan yuk almiyor, tek yonde dondugu icin pim bosluğunun etkisi yok.

AYAR BILEZIGI: yatak ile gobek arasinda 7,5 mm torna halka. Ray + blok + yatak katalog toleransinin hepsi
  TEK ve ucuz bir parcada toplaniyor; 2-14 mm arasinda yeniden islenebiliyor. Onceki iki semada YEDEK = 0'di.

HGR20 DEGIL HGR15: plakanin ALTINDA 44,0 mm aciliyor, 41 mm'lik pancake motor oraya giriyor.

Ayrica v10'da:
 · RAY YARIGI KALKTI — olculdu: taban rayi z -200..-525, yarik z -104..-174; kesismiyorlar, yarik SIFIR
   malzeme kaldiriyordu. Boru rayin ONUNDE iniyor.
 · KOVAN FLANSI: ic kabuk tabaninin ALTINA surekli TIG kaynak, sizdirmaz.
 · Cakisma taramasindaki 'pu_/ic_kabuk/ray_' muafiyeti KOVANLARI KAPSAMIYOR (uc boru sekiz surumdur
   PU'nun icine gomuluydu, muafiyet yuzunden gorunmuyordu).
 · AGIZ ALT DUDAGI: silinen cerceve sacinin tek gercek isi (robot carparsa kesmeyen kivrik kenar) yalniz
   ALTTA kaliyor; ust lama geri konmuyor, tepsi cikisi acik.
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    return s.replace(a, b, 1)


c = io.open(os.path.join(U, "topping_cad_v9.py"), encoding="utf-8").read()
c = c.replace("topping_cad_v9", "topping_cad_v10").replace("topping_modul_v9", "topping_modul_v10")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v10 (22 Eyl 2026): DONER TABLA TAM URETIM MODELI — tekne + kiris merdiveni + HGR15 raylar + 4 blok +\n"
             "araba plakasi + doner yatak + ayar bilezigi + gobek + tabla + pancake motor + lokma + GT3 kayis\n"
             "zinciri + apron + cati + kirinti cekmecesi + enerji zinciri + 5 sensor + tamponlar. Ray yarigi kalkti.\n") + c[i:]
c = yama(c, '"TOPPING MODULU v9', '"TOPPING MODULU v10')

# ---------------------------------------------------------------- 1 · yeni kaset surumleri (boru ucu y 252)
c = yama(c, '''KASET_CAD = {"HARÇ 1": "harc_cad_v3", "HARÇ 2": "harc_cad_v3", "KIYMA": "kiyma_cad_v8",
             "KUŞBAŞI": "kusbasi_cad_v7", "KAŞAR KABI": "kasar_cad_v13", "KÜP SUCUK": "sucuk_cad_v6"}''',
         '''KASET_CAD = {"HARÇ 1": "harc_cad_v4", "HARÇ 2": "harc_cad_v4", "KIYMA": "kiyma_cad_v9",
             "KUŞBAŞI": "kusbasi_cad_v8", "KAŞAR KABI": "kasar_cad_v14", "KÜP SUCUK": "sucuk_cad_v7"}''')

# ---------------------------------------------------------------- 2 · RAY YARIGI KALKTI
c = yama(c, '''        ray = kut(x0 + 6.0, x1 - 6.0, KAS[0] - 4.0, KAS[0], ZK[0], ZK[1])
        for a_, b_ in YARIK: ray = ray.cut(kut(a_, b_, KAS[0] - 5.0, KAS[0] + 1.0, ZY[0], ZY[1]))''',
         '''        # v10: RAY YARIĞI KALKTI. Ölçüldü: taban rayı z −200…−525, yarık z −104…−174 — kesişmiyorlar,
        # yarık SIFIR malzeme kaldırıyordu. Boru rayın ÖNÜNDE iniyor, rayı hiç geçmiyor.
        ray = kut(x0 + 6.0, x1 - 6.0, KAS[0] - 4.0, KAS[0], ZK[0], ZK[1])''')

# ---------------------------------------------------------------- 3 · KOVAN FLANSI + muafiyet daraltma
c = yama(c, '        ekle("dozaj_kovani_%s" % ad.replace(" ", "_"), kv, "sac", bom=None)',
         '''        ekle("dozaj_kovani_%s" % ad.replace(" ", "_"), kv, "sac", bom=None)''')
c = yama(c, '''        if p["ad"].startswith("_bom") or p["ad"].startswith(("ray_", "bolme_", "huni_", "konum_pimi_", "ic_kabuk", "pu_")):
            continue                                                            # kasete DEĞMESİ gereken parçalar''',
         '''        # v10: muafiyet DARALDI — kovanlar artık taranıyor. Bu muafiyet yüzünden üç kaset borusu
        # (KUŞBAŞI 12.017 · KÜP SUCUK 2.156 · KAŞAR 562 mm³) sekiz sürümdür PU'nun içinde gömülü duruyordu.
        if p["ad"].startswith("_bom") or (p["ad"].startswith(("ray_", "bolme_", "konum_pimi_", "ic_kabuk", "pu_"))
                                          and not p["ad"].startswith("dozaj_kovani")):
            continue                                                            # kasete DEĞMESİ gereken parçalar''')

# ---------------------------------------------------------------- 4 · ESKI TABLA BLOKLARI -> TAM MEKANIZMA
i0 = c.index("    # ---------------- 8b · DÖNER TABLA (v8) ----------------")
i1 = c.index("    # ---------------- 9 · (v9:")
c = c[:i0] + '''    # ---------------- 8b · DÖNER TABLA — TAM ÜRETİM MODELİ (v10) ----------------
    # v9'a kadar 9 adet yer tutucu bloktu; parçaların hiçbiri birbirine bağlanmıyordu. Şema: X ekseni
    # KAYIŞ tahrikli tek araba, DÖNÜŞ ekseni araba plakasının altındaki pancake motorla EŞ EKSENLİ doğrudan.
    TB = H.S["tabla"]
    Xc = 900.0                                                                  # modelde tablanın çizildiği konum (strok x 220…1520)
    ZT = ZK[0] + 30.0                                                           # tabla ekseni (nozzle'dan z'de 20 mm geride)
    RT_ = TB["cap"] / 2.0

    # --- 8b.1 TAŞIYICI: tekne + kiriş merdiveni (1,5 mm saca lineer ray bağlanmaz) ---
    tk = kut(15.0, 1695.0, 1.5, 4.5, -5.0, -415.0)
    tk = tk.union(kut(15.0, 1695.0, 1.5, 31.5, -5.0, -8.0)).union(kut(15.0, 1695.0, 1.5, 31.5, -412.0, -415.0))
    ekle("mekanizma_teknesi", tk, "sac", bom=("Mekanizma teknesi", 1, "304 3,0 mm · kenarları 30 kıvrık · %1,5 eğim",
         "ray kirişlerinin kaynaklandığı yapısal tekne; damlayanı tabla düzleminin ALTINDA toplar, ön-solda Ø25 tahliye"))
    for ad_, z0_, z1_, gen_ in (("on", -95.0, -35.0, 60.0), ("arka", -305.0, -245.0, 60.0)):
        ekle("ray_kirisi_%s" % ad_, kut(45.0, 1695.0, 4.5, 20.5, z0_, z1_), "celik",
             bom=("Ray kirişi 60 × 16 × 1650", 2, "304 lama · tekneye sürekli kaynak", "kaynaktan SONRA üç üst yüzey TEK BAĞLAMADA frezelenir (düzlemlik 0,1 mm/m — HGR15 şartı)") if ad_ == "on" else None)
    ekle("kayis_kirisi", kut(15.0, 1695.0, 4.5, 20.5, -385.0, -335.0), "celik",
         bom=("Kayış kirişi 50 × 16 × 1680", 1, "304 lama", "kayış kasnakları, avara ve gergi bunun üstünde"))
    for i_, xb in enumerate((200.0, 500.0, 800.0, 1100.0, 1400.0, 1650.0)):
        ekle("baglama_lamasi_%d" % i_, kut(xb, xb + 40.0, 4.5, 20.5, -335.0, -305.0), "celik",
             bom=("Bağlama laması 40 × 16", 6, "304 lama", "arka ray kirişi ile kayış kirişini bağlar; dönüş motoru z −141…−198 bandında gezdiği için tam boy lama konulamıyor") if i_ == 0 else None)

    # --- 8b.2 LİNEER KIZAK ---
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        ekle("lineer_ray_%s" % ad_, kut(65.0, 1665.0, 20.5, 35.5, zc_ - 7.5, zc_ + 7.5), "celik",
             bom=("Lineer ray HGR15 × 1600", 2, "paslanmaz sınıf [V: özel sipariş, fiyat/teslim sorulacak]", "M4 havşa hatve 60, ray başına 27 delik; ayar puluyla 0,05 mm'ye paralellenir") if ad_ == "on" else None)
    for i_, (xb, zc_) in enumerate([(Xc - 100.0, -65.0), (Xc + 100.0, -65.0), (Xc - 100.0, -275.0), (Xc + 100.0, -275.0)]):
        ekle("kizak_blogu_%d" % i_, kut(xb - 17.0, xb + 17.0, 20.5, 48.5, zc_ - 30.7, zc_ + 30.7)
             .cut(kut(xb - 18.0, xb + 18.0, 20.0, 35.7, zc_ - 7.7, zc_ + 7.7)), "celik",
             bom=("Kızak bloğu HGH15CA", 4, "paslanmaz · NSF H1 gıda gresi", "hatve 200 mm; araba plakası bunların üstüne 16 × M4 ile bağlanır") if i_ == 0 else None)
    apl = kut(Xc - 150.0, Xc + 150.0, 48.5, 58.5, -25.0, -315.0).cut(sily(Xc, ZT, 23.0, 47.0, 60.0))
    ekle("araba_plakasi", apl, "celik", bom=("Araba plakası 300 × 290 × 10", 1, "304 · iki yuva TEK BAĞLAMADA işlenir (eş eksenlik 0,05)",
         "altında motor pilotu Ø38,1 H8, üstünde döner yatak yuvası; hafifletme cepli ~5,5 kg"))

    # --- 8b.3 DÖNÜŞ: yatak · ayar bileziği · göbek · tabla ---
    dy = sily(Xc, ZT, 80.0, 58.5, 78.5).cut(sily(Xc, ZT, 35.0, 57.5, 79.5))
    ekle("doner_yatak", dy, "celik", bom=("İnce kesit döner yatak (slewing ring)", 1, "4 nokta bilyalı · H20 · iç Ø70 dış Ø160 [V: katalogdan doğrulanacak]",
         "Ø340 konsol tablanın devirme momentini doğrudan alır; iç bilezik plakaya 8 × M5 havşa"))
    ekle("ayar_bilezigi", sily(Xc, ZT, 85.0, 78.5, 86.0).cut(sily(Xc, ZT, 45.0, 77.5, 87.0)), "celik",
         bom=("Ayar bileziği · torna halka", 1, "304 · dış Ø170 iç Ø90 · kalınlık 7,5 (işleme aralığı 2–14)",
              "ray + blok + yatak katalog toleransının TAMAMI bu tek parçada toplanır; yedek dikey boşluk 7,5 mm"))
    gb = sily(Xc, ZT, 110.0, 86.0, 97.0).cut(sily(Xc, ZT, 30.0, 85.0, 98.0))
    for i_ in range(2):
        gb = gb.cut(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.1, 85.0, 92.0))                # tahrik pimi burçları
    ekle("tabla_gobegi", gb, "celik", bom=("Tabla göbeği Ø220 × 11", 1, "304 işlenmiş, cepli ~1,8 kg",
         "ayar bileziğine 3 × M8 saplama + paslanmaz KELEBEK SOMUN + 2 × Ø8 h7 konum pimi ile ALETSİZ sökülür"))
    tb_ = sily(Xc, ZT, RT_, 97.0, 100.0)
    for i_ in range(3):                                                                           # robot parmak kesikleri
        a_ = math.radians(120.0 * i_ + 60.0)
        tb_ = tb_.cut(kut(Xc + (RT_ - 25.0) * math.cos(a_) - 30.0, Xc + (RT_ - 25.0) * math.cos(a_) + 30.0,
                          96.0, 101.0, ZT + (RT_ - 25.0) * math.sin(a_) - 12.5, ZT + (RT_ - 25.0) * math.sin(a_) + 12.5))
    ekle("tabla", tb_, "sac", bom=("Döner tabla Ø340 × 3", 1, "304 · göbeğe sürekli TIG kaynak, parlatılmış",
         "gıda yüzeyinde cıvata yok; kenarda 120°'de 3 parmak kesiği 60 × 25 — robot Ø340 tepsinin altına parmak sokabilsin"))
    for i_ in range(3):
        a_ = math.radians(120.0 * i_)
        ekle("merkezleme_pimi_%s" % "ABC"[i_], koni_y_t(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 2.0, 5.0, 100.0, 105.0), "celik",
             bom=("Merkezleme pimi · konik", 3, "304 · taban Ø10 tepe Ø4 boy 5 · H7/r6 presli", "r = 100'de 120° aralıklı; tepsinin altındaki 3 konik çukura girer, hem merkezler hem POZİTİF döndürür") if i_ == 0 else None)

    # --- 8b.4 DÖNÜŞ MOTORU (eş eksenli, i = 1) ---
    ekle("donus_motoru", kut(Xc - 28.5, Xc + 28.5, 4.5, 45.5, ZT - 28.5, ZT + 28.5), "motor",
         bom=("Dönüş motoru · NEMA23 PANCAKE", 1, "57 × 57 × 41 · kapalı çevrim step · ~0,9 N·m [V: tork eğrisi doğrulanacak]",
              "araba plakasının ALTINA 4 × M5 havşa, ekseni TABLA EKSENİYLE AYNI; redüktör ve kayış YOK · gereken 0,169 N·m → ~5 kat pay"))
    lk = sily(Xc, ZT, 15.0, 46.0, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))
    for i_ in range(2):
        lk = lk.union(sily(Xc + (10.0 if i_ == 0 else -10.0), ZT, 4.0, 66.0, 74.0))
    ekle("tahrik_lokmasi", lk, "celik", bom=("Tahrik lokması Ø30 × 20", 1, "304 torna · yarıklı sıkma + M5 pinç",
         "üstünde r = 10'da 2 × Ø8 pim; göbeğin altındaki burçlara girer — rijit kaplin YOK, tabla düşeyde ayrılabiliyor"))

    # --- 8b.5 X TAHRİK ZİNCİRİ ---
    ekle("x_tahrik_kasnagi", silz(1735.0, 31.0, 9.55, -364.5, -355.5).cut(silz(1735.0, 31.0, 4.1, -366.0, -354.0)), "celik",
         bom=("GT3 kasnak 20 diş", 1, "PD 19,099 → çevre TAM 60,00 mm/tur · sıkma bilezikli (setuskur yok)", "x motorunun milinde"))
    ekle("x_motoru", kut(1706.5, 1763.5, 41.5, 117.5, -388.5, -331.5), "motor",
         bom=("X motoru · NEMA23 kapalı çevrim step", 1, "57 × 57 × 76 · 1,2 N·m · 24 V · mil AŞAĞI",
              "sağ uçta: tablanın en sağ konumu x 1690'da biter, motor 1706,5'te başlar · 200 dev/dk @200 mm/s, gereken 0,212 N·m → ~3 kat pay"))
    ekle("x_motor_kaidesi", kut(1690.0, 1780.0, 20.5, 38.0, -400.0, -320.0).cut(kut(1700.0, 1770.0, 19.5, 39.0, -392.0, -328.0)), "sac",
         bom=("X motor kaidesi", 1, "304 8 mm bükme L · tekneye 4 × M8, z yuvalı", "kayış hizası buradan ayarlanır"))
    ekle("avara_kasnak", silz(35.0, 31.0, 9.55, -364.5, -355.5), "celik",
         bom=("Avara kasnak GT3 20 diş", 1, "flanşlı · içinde 2 × 625-2RS paslanmaz rulman", "sol uçta; gergi bunun braketinde"))
    ekle("avara_gergi_braketi", kut(20.0, 44.0, 20.5, 45.0, -385.0, -335.0).cut(silz(35.0, 31.0, 12.0, -372.0, -348.0)), "celik",
         bom=("Avara + gergi braketi", 1, "304 10 mm · 16 mm yuvalı 2 × M8 + M6 itme vidası + kontra", "GERGİ BURADAN — tabla sağ uca çekilince ağızdan elle erişilir"))
    for i_, zc_ in enumerate((-350.45, -369.55)):
        ekle("x_kayisi_%d" % i_, kut(52.0, 1686.0, 26.5, 35.5, zc_ - 1.5, zc_ + 1.5), "koyu",
             bom=("X kayışı GT3-9 açık uçlu ~3460 mm", 1, "çelik kordlu poliüretan", "iki koşu; TEPSİ GÖLGESİNİN (z 0…−340) DIŞINDA — ürün düzleminin altında tahrik elemanı yok") if i_ == 0 else None)
    kol = kut(Xc - 150.0, Xc + 150.0, 38.5, 48.5, -385.0, -315.0).union(kut(Xc - 20.0, Xc + 20.0, 40.0, 48.5, -365.0, -355.0))
    ekle("kayis_kolu", kol, "celik", bom=("Kayış kolu · L", 1, "304 10 mm bükme · plakaya 4 × M8 + Ø6 pim",
         "düşey kanat iki kayış koşusunun TAM ORTASINDA, her yana 4,55 mm"))
    for i_, xb in enumerate((Xc - 140.0, Xc + 140.0)):
        ekle("kayis_kelepcesi_%d" % i_, kut(xb - 20.0, xb + 20.0, 25.0, 38.0, -374.0, -345.0).cut(kut(xb - 21.0, xb + 21.0, 26.4, 35.6, -373.0, -346.0)), "celik",
             bom=("Kayış kelepçesi", 2, "304 gövde + GT3 diş profilli baskı plakası", "açık kayışın iki ucunu diş-dişe sıkıştırır (2 × M5 + 2 × M4)") if i_ == 0 else None)

    # --- 8b.6 HİJYEN / KORUMA ---
    ap = kut(Xc - 190.0, Xc + 190.0, 58.5, 60.5, -5.0, -340.0).cut(sily(Xc, ZT, 85.0, 57.5, 61.5))
    ekle("siyirici_apron", ap, "sac", bom=("Sıyırıcı apron 380 × 335 × 2", 1, "304 · kenarı 10 kıvrık · elle çıkar",
         "tepsinin ayak izini birebir örter; dökülen kırıntı raylara ULAŞAMAZ"))
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        ct = kut(45.0, 1695.0, 20.5, 44.0, zc_ - 37.0, zc_ + 37.0).cut(kut(40.0, 1700.0, 19.5, 45.0, zc_ - 33.0, zc_ + 33.0))
        ekle("ray_ortu_catisi_%s" % ad_, ct, "sac",
             bom=("Ray örtü çatısı", 2, "304 1,0 mm · 90 geniş, tepe y 44, ortada 36 yarık", "arabanın olmadığı yerde rayı örter; 24 × M4 havşa") if ad_ == "on" else None)
    ekle("kirinti_cekmecesi", kut(100.0, 1580.0, 4.5, 20.5, -240.0, -212.0).cut(kut(103.0, 1577.0, 6.5, 21.5, -237.0, -215.0)), "sac",
         bom=("Kırıntı çekmecesi", 1, "304 1,0 mm · önden çekilir", "iki ray kirişi arasında; boşaltılıp yıkanır"))
    ekle("enerji_zinciri_kanali", kut(15.0, 1695.0, 4.5, 64.5, -500.0, -440.0).cut(kut(18.0, 1692.0, 6.5, 65.5, -497.0, -443.0)), "sac",
         bom=("Enerji zinciri + kanalı", 1, "iç 15 × 30 · R40 · boy ~840 · kanal 304 1,0 mm 60 × 60",
              "dönüş motoru arabayla gezdiği için ZORUNLU; içinde PUR kılıflı sürükleme-zinciri kablosu (PVC DEĞİL)"))

    # --- 8b.7 SENSÖRLER ve TAMPONLAR ---
    for ad_, xb in (("home", 1520.0), ("limit_sol", 205.0), ("limit_sag", 1535.0)):
        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Endüktif sensör M12 × 50 IP69K PNP NO", 3, "ön ray kirişinin dış yüzüne L braketle", "home x 1520 (istasyon) · limit− 205 · limit+ 1535") if ad_ == "home" else None)
    ekle("x_bayragi", kut(Xc - 30.0, Xc + 30.0, 40.0, 48.5, -24.0, -6.0), "sac",
         bom=("X bayrağı 60 × 25", 1, "304 3 mm", "araba plakasının ön kenarının altında"))
    ekle("tabla_home_sensoru", sily(Xc, ZT - 97.0, 4.0, 66.5, 76.5), "koyu",
         bom=("Tabla home sensörü M8 endüktif IP67", 1, "araba plakasının ÜSTÜNDE braketli", "algılama yüzü YUKARI; arabayla birlikte gezdiği için sabit referansa gerek yok"))
    ekle("tabla_home_bayragi", sily(Xc, ZT - 97.0, 10.0, 78.5, 81.5), "celik",
         bom=("Tabla home bayrağı 3 × 20 × 12", 1, "304 · ayar bileziğine r = 90'da kaynaklı", "boşluk 2,0 mm · robot tepsiyi hep aynı açıda bulmalı"))
    for i_, xb in enumerate((180.0, 1560.0)):
        ekle("uc_tamponu_%d" % i_, silz(xb, 53.5, 10.0, -80.0, -65.0), "silikon",
             bom=("Uç tamponu Ø20 × 15", 2, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil") if i_ == 0 else None)

    for a_, ad_, n_, malz_, gor_ in (
            ("_bom_tabla", "Tabla yasası", 1, "yazılım", "ağız pide merkezine %.0f mm'de 2,5 s bekler, r² doğrusal azalarak %.0f mm'ye iner, 0,3 s bekler [kasar_akis_model_v2]" % (TB["r_dis"], TB["r_ic"])),
            ("_bom_strok", "Strok ve istasyon", 1, "—", "tabla merkezi x 220…1520 (1300 mm) · istasyon SAĞDA x 1520 · dozajda %.1f mm/s, geçişte %.0f mm/s" % (TB["x_doz_hiz"], TB["x_gecis_hiz"])),
            ("_bom_cevrim", "Çevrim", 1, "—", "altı doz 71,0 s → 51 tepsi/h · tipik tek dozlu kaşarlı pide 13,7 s → 262 tepsi/h"),
            ("_bom_civata", "Bağlantı elemanları (tümü A4/A2 paslanmaz)", 180, "15 tip · gıdaya bakan her baş HAVŞA ya da KUBBE",
             "ray 54 × M4×16 · blok 16 × M4×20 · yatak 8 × M5×16 · ayar bileziği 6 × M5×16 · göbek 3 × M8×40 saplama + kelebek somun + 2 pim · dönüş motoru 4 × M5×20 · kayış kolu 4 × M8×25 + 2 pim · kelepçe 4 × M5 + 4 × M4 · X motoru 4 × M5×12 + kaide 4 × M8×25 · avara M8×40 + braket 2 × M8×25 + M6 jack · apron 8 × M4×10 · çatı 24 × M4×8 · sensör 12 × M4×12 · zincir 18 · tampon 2 takım M10")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

''' + c[i1:]

# ---------------------------------------------------------------- 5 · AGIZ ALT DUDAGI
c = yama(c, "    # ---------------- 9 · (v9:",
         '''    ekle("agiz_alt_dudagi", kut(30.0, 1770.0, 1.5, 13.5, 0.0, -4.5).cut(kut(33.0, 1767.0, 3.5, 15.0, 1.0, -3.0)), "sac",
         bom=("Ağız alt dudağı", 1, "304 1,5 mm bükme · dış tabana ve iki yan saca sürekli kaynak",
              "silinen ağız çerçevesinin tek gerçek işi: robot çarparsa kesmeyen kıvrık kenar — ama YALNIZ ALTTA; üst lama geri konmadı, tepsi çıkışı açık"))

    # ---------------- 9 · (v9:''')

# ---------------------------------------------------------------- 6 · konik pim yardimcisi
c = yama(c, "def sily(x, z, r, y0, y1):",
         '''def koni_y_t(x, z, r_ust, r_alt, y0, y1):
    """y ekseninde konik (merkezleme pimi): y0'da r_alt, y1'de r_ust"""
    if abs(r_alt - r_ust) < 0.01: return sily(x, z, r_alt, y0, y1)
    return cq.Workplane(obj=cq.Solid.makeCone(r_alt, r_ust, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0)))


def sily(x, z, r, y0, y1):''')

io.open(os.path.join(U, "topping_cad_v10.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v10.py yazildi ·", n[0], "yama")
