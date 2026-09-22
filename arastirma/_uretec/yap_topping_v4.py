# -*- coding: utf-8 -*-
"""topping_cad_v3 -> topping_cad_v4
Kemal (22 Eyl): "ya bu yatayda kasetlerin arkasindaki uzun parca ne? Sogutmak icin bir motor ve iceriye havayi
vermiyor mu, kesikler aciliyor sacda — standardi bu degil mi? Normalde motor/sogutma grubu ust tarafta olur,
asagiya havayi verir ya da arkada. Birde nozzle kisimlarini ne yaptin anlamadim, dolu parcalar var bunda."

v4'TE DEGISEN:
 1 EVAPORATOR ARTIK CIPLAK DURMUYOR — ticari sogutucu standardina gecildi: evaporator + fanlar arka bolmede
   bir PLENUM'un icinde, onlerine DELIKLI SAC PERDE (menfez) kondu. Ust siradaki kesiklerden soguk hava
   hucreye giriyor, alt siradaki kesiklerden donuyor. Ayri "hava kanali saci" kalkti (perde onun isini yapiyor).
 2 BACANIN USTU KAPALIYDI (gercek hata): ic bosluk bacanin ust yuzunden 3 mm asagida bitiyordu, yani urunun
   girecegi delik YOKTU. Baca artik bastan basa acik ve iki kademeli: ustte yarigi kavrayan genis agiz,
   altta memenin olcusunde dar baca — urun sacilmadan pidenin 40 mm ustune iniyor.
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:120]
    n[0] += 1
    return s.replace(a, b, 1)


c = io.open(os.path.join(U, "topping_cad_v3.py"), encoding="utf-8").read()
c = c.replace("topping_cad_v3", "topping_cad_v4").replace("topping_modul_v3", "topping_modul_v4")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v4 (22 Eyl 2026): evaporator DELIKLI SAC PERDE arkasinda bir plenumda (ticari sogutucu standardi) ·\n"
             "baca bastan basa acildi (ustu kapaliydi) ve iki kademeli oldu. Onceki: topping_cad_v3.py\n") + c[i:]
c = yama(c, '"TOPPING MODULU v3', '"TOPPING MODULU v4')

# ---------------------------------------------------------------- 1 · BACA: bastan basa acik + iki kademeli
c = yama(c, '''        # v3: huni artık pide üstüne DUSME kala biten bir BACA. Ağzı kasetin meme ölçüsünde daralıyor;
        # üst kısmı yarığın tamamını kavrıyor ki kaset çekilirken meme serbest kalsın.
        hb0, hb1 = AGZ[1] + H.DUSME, KAS[0] - 4.0                              # baca alt ucu … kasetin altı
        huni = kut(x0 + 22.0, x1 - 22.0, hb0, hb1, ZY[0] - 2.0, ZY[1] + 2.0)
        huni = huni.cut(kut(x0 + 25.0, x1 - 25.0, hb0 - 1.0, hb1 - 3.0, ZY[0] - 5.0, ZY[1] + 5.0))
        ekle("huni_%s" % k, huni, "sac", bom=None)''',
         '''        # v4 DÜZELTMESİ: v3'te iç boşluk bacanın ÜST yüzünden 3 mm aşağıda bitiyordu — ürünün gireceği delik
        # yoktu, baca kapalı bir kutuydu (Kemal: "dolu parçalar var"). Artık baştan başa açık.
        # İKİ KADEME: üstte yarığın tamamını kavrayan geniş ağız (kaset çekilirken meme serbest geçsin),
        # altta MEMENİN ölçüsünde dar baca (ürün saçılmadan insin).
        hb0, hb1 = AGZ[1] + H.DUSME, KAS[0] - 4.0                              # baca alt ucu … kasetin altı
        hbo = hb1 - 46.0                                                       # geniş ağzın alt kotu
        za0, za1 = ZK[0] + (_a1 - _dd / 2.0) + 4.0, ZK[0] + (_a0 - _dd / 2.0) - 4.0   # memenin z aralığı + pay
        agz_ = kut(x0 + 22.0, x1 - 22.0, hbo, hb1, ZY[0] - 2.0, ZY[1] + 2.0)
        agz_ = agz_.cut(kut(x0 + 25.0, x1 - 25.0, hbo - 1.0, hb1 + 1.0, ZY[0] - 5.0, ZY[1] + 5.0))
        bac_ = kut(x0 + 34.0, x1 - 34.0, hb0, hbo + 1.0, za1 - 2.0, za0 + 2.0)
        bac_ = bac_.cut(kut(x0 + 37.0, x1 - 37.0, hb0 - 1.0, hbo + 2.0, za1 + 1.0, za0 - 1.0))
        ekle("huni_%s" % k, agz_.union(bac_), "sac", bom=None)''')

# ---------------------------------------------------------------- 2 · EVAPORATOR PLENUMU + DELIKLI PERDE
c = yama(c, '''    EVY = (KAS[0] + 228.0, KAS[1] - 10.0)                                      # 488 … 610 · 280'lik kasetin rotor soketi 477'de bitiyor, onun da üstünde
    EVZ = (ZKAV[0] - 2.0, ZKAV[1] + 3.0)                                       # kavrama bölmesi (kasetin arkası)''',
         '''    EVY = (KAS[0] + 228.0, KAS[1] - 10.0)                                      # 488 … 610 · 280'lik kasetin rotor soketi 477'de bitiyor, onun da üstünde
    EVZ = (ZKAV[0] - 7.0, ZKAV[1] + 3.0)                                       # kavrama bölmesi (kasetin arkası) — perdeye 5 mm yer bırakıldı''')

c = yama(c, '''    # Hava kanalı v1'de y 504–508'deydi, yani KASETİN İÇİNDE (kaset üstü 620). v2'den beri kasetin 4 mm üstünde.
    ekle("hava_kanali", kut(XI0 + SAC_IC + 2.0, XI1 - SAC_IC - 2.0, KAS[1] + 4.0, hy1 - SAC_IC - 3.0, ZK[0] - 20.0, ZKAV[0] - 4.0), "sac",
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "arkadaki evaporatörden gelen soğuk havayı kaset sırasının üstünde baştan sona dağıtır"))''',
         '''    # v4 · HAVA PERDESİ (Kemal: "iceriye havayi vermiyor mu, kesikler aciliyor sacda — standardi bu degil mi").
    # Ticari soğutucu düzeni: evaporatör + fanlar arka bölmede bir PLENUM'un içinde, önlerinde delikli sac perde.
    # ÜST sıra kesiklerden soğuk hava hücreye basılır, ALT sıra kesiklerden (millerin altından) geri emilir.
    # Ayrı "hava kanalı saci" kalktı — perde onun işini yapıyor ve evaporatörü de gözden gizliyor.
    PZ0, PZ1 = ZKAV[0] - 1.0, ZKAV[0] - 2.5                                    # 1,5 mm perde sacı
    perde = kut(XI0 + SAC_IC, XI1 - SAC_IC, KAS[0], KAS[1], PZ0, PZ1)
    for x_, y_, k_ in MIL:                                                     # 12 mil/soket geçişi
        perde = perde.cut(silz(x_, y_, 25.0, PZ0 + 1.0, PZ1 - 1.0))
    for ad, x0_, x1_, gen_ in YUVA:                                            # 12 konum pimi geçişi
        for px in (x0_ + 25.0, x1_ - 25.0):
            perde = perde.cut(silz(px, KAS[0] + 20.0, 8.0, PZ0 + 1.0, PZ1 - 1.0))
    ust0, ust1 = EVY[0] + 6.0, EVY[1] - 6.0                                    # üfleme kesikleri (evaporatör hizası)
    alt0, alt1 = KAS[0] + 6.0, KAS[0] + 36.0                                   # dönüş kesikleri (millerin altı)
    xx = XI0 + SAC_IC + 30.0
    while xx + 14.0 < XI1 - SAC_IC - 30.0:                                     # 14 × 40 mm yarıklar, 40 mm arayla
        perde = perde.cut(kut(xx, xx + 14.0, ust0, ust1, PZ0 + 1.0, PZ1 - 1.0))
        perde = perde.cut(kut(xx, xx + 14.0, alt0, alt1, PZ0 + 1.0, PZ1 - 1.0))
        xx += 40.0
    ekle("hava_perdesi", perde, "sac", bom=("Hava perdesi · delikli sac", 1, "304 1,5 mm · lazer", "evaporatör bölmesini kapatır; üst kesiklerden soğuk hava girer, alt kesiklerden döner (ticari soğutucu düzeni)"))''')

io.open(os.path.join(U, "topping_cad_v4.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v4.py yazildi ·", n[0], "yama")
