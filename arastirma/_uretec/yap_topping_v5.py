# -*- coding: utf-8 -*-
"""topping_cad_v4 -> topping_cad_v5
Kemal (22 Eyl): "o parcanin STANDART versiyonunu bul, MOTORLARIN OLDUGU YERE koy, sonra iceriye sogugu verecek
sekilde YALITIMA BOSLUK AC, iceri gitsin hava — bence boyledir o. Birde o kasetlerden kare cikis yapmissin,
onu YUVARLAK yap, circle capini da hesapla, alta dogru uzat ... baska parca yok, direk kasetin kendi ucu
pideye yaklasiyor."

v5'TE DEGISEN:
 1 EVAPORATOR KURU BOLMEYE gecti — motorlarin ustune. Sogutma paketi artik tek bir KUTU: standart sinif
   fanli evaporator (unit cooler) 400 x 180 x 190. Sogugu hucreye ARKA YALITIMDAKI IKI BOSLUKTAN veriyor:
   ustte ufleme, altta donus. Kavrama bolmesi plenum, delikli perde de havayi bastan sona yayiyor.
   (Hucrenin icinde artik hicbir sogutma parcasi yok — Kemal: "motor ust tarafta/arkada olur, havayi verir".)
 2 BACA/HUNI PARCASI KALKTI. Urunu artik kasetin KENDI yuvarlak borusu pideye 40 mm kala indiriyor
   (kasar v11 / kiyma v6 / kusbasi v5 / sucuk v4 — yap_boru_v1.py).
 3 Taban yarigi boru capina gore daraldi (yuva genisligi - 40 yerine boru disi + 6).
 4 Kaset zarfi cakisma taramasinda BORU PAYIYLA aliniyor (boru kaset kutusunun 100 mm altina iniyor).
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:120]
    n[0] += 1
    return s.replace(a, b, 1)


c = io.open(os.path.join(U, "topping_cad_v4.py"), encoding="utf-8").read()
c = c.replace("topping_cad_v4", "topping_cad_v5").replace("topping_modul_v4", "topping_modul_v5")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v5 (22 Eyl 2026): evaporator KURU BOLMEYE (motorlarin ustune), sogutma arka yalitimdaki iki bosluktan ·\n"
             "baca/huni parcasi kalkti, kasetin kendi YUVARLAK borusu pideye iniyor. Onceki: topping_cad_v4.py\n") + c[i:]
c = yama(c, '"TOPPING MODULU v4', '"TOPPING MODULU v5')

# ---------------------------------------------------------------- 1 · yeni kaset surumleri + boru olculeri
c = yama(c, 'KASET_CAD = {140: "kiyma_cad_v5", 280: "kasar_cad_v10"}',
         'KASET_CAD = {140: "kiyma_cad_v6", 280: "kasar_cad_v11"}      # v5: yuvarlak çıkış borulu sürümler')

c = yama(c, '''def agiz(modul):''',
         '''def boru(modul):
    """kasetin YUVARLAK çıkış borusu: iç çap, et, alt uç kotu (kaset yerel y). Taban yarığı ve
    kaset zarfı buna göre kuruluyor — sayı iki yerde yazılmasın."""
    import re
    k = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    m = re.search(r"^BORU_D, BORU_ET, BORU_ALT\\s*=\\s*([\\d.]+),\\s*([\\d.]+),\\s*(-?[\\d.]+)", k, re.M)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def agiz(modul):''')

c = yama(c, 'AGIZ = {g: agiz(m) for g, m in KASET_CAD.items()}',
         'AGIZ = {g: agiz(m) for g, m in KASET_CAD.items()}\nBORU = {g: boru(m) for g, m in KASET_CAD.items()}')

# ---------------------------------------------------------------- 2 · taban yarigi: boru capina gore
c = yama(c, '''    YARIK = [(x0 + 20.0, x1 - 20.0) for ad, x0, x1, gen in YUVA]''',
         '''    # v5: yarık artık YUVA genişliğine göre değil, kasetin BORU dışına göre — soğuk kaçağı en aza insin.
    YARIK = []
    for ad, x0, x1, gen in YUVA:
        bd, be, _ = BORU[gen]
        r_ = bd / 2.0 + be + 3.0                                               # boru dışı + 3 mm pay
        YARIK.append(((x0 + x1) / 2.0 - r_, (x0 + x1) / 2.0 + r_))''')

# ---------------------------------------------------------------- 3 · HUNI/BACA PARCASI KALKTI
c = yama(c, '''        # v4 DÜZELTMESİ: v3'te iç boşluk bacanın ÜST yüzünden 3 mm aşağıda bitiyordu — ürünün gireceği delik
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
        ekle("huni_%s" % k, agz_.union(bac_), "sac", bom=None)''',
         '''        # v5: BACA/HUNİ PARÇASI KALKTI (Kemal: "başka parça yok, direk kasetin kendi ucu pideye yaklaşıyor").
        # Ürünü kasetin KENDİ yuvarlak borusu indiriyor; boru kaset tabanının 100 mm altına iniyor ve
        # pidenin üst yüzüne 40 mm kala bitiyor. Modülde yalnız borunun geçtiği yarık var.''')

c = yama(c, '("_bom_huni", "Dozaj bacası", 6, "304 1,0 mm, çekip çıkarılır", "memeden çıkanı pide üstüne %.0f mm kala indirir; yıkamak için sökülür" % H.DUSME)',
         '("_bom_huni", "— (baca parçası kalktı)", 0, "kasetin kendi borusu", "ürünü kasetin yuvarlak çıkış borusu pide üstüne %.0f mm kala indiriyor" % H.DUSME)')

# ---------------------------------------------------------------- 4 · EVAPORATOR KURU BOLMEYE + YALITIM BOSLUKLARI
c = yama(c, '''    # v1: evaporatör BEŞ KASETİN İÇİNDEYDİ. v2: sağ uca dikey alındı — ama orası kaset sırasının yanı, yer yiyordu.
    # v3 (Kemal: "şu sağdaki şeyi arka tarafa al"): kasetlerin ARKASINDAKİ kavrama bölmesine, yatay.
    # Miller y 300–455 arasında; evaporatör onların ÜSTÜNDE (y 470–620) duruyor, hiçbir mile değmiyor.
    EVY = (KAS[0] + 228.0, KAS[1] - 10.0)                                      # 488 … 610 · 280'lik kasetin rotor soketi 477'de bitiyor, onun da üstünde
    EVZ = (ZKAV[0] - 7.0, ZKAV[1] + 3.0)                                       # kavrama bölmesi (kasetin arkası) — perdeye 5 mm yer bırakıldı
    ekle("evaporator", kut(220.0, W - 220.0, EVY[0], EVY[1], EVZ[0], EVZ[1]), "bakir",
         bom=("Evaporatör", 1, "lamelli, ince tip, paslanmaz karter", "kaset sırasının ARKASINDA, millerin üstünde; cephe %.0f × %.0f mm · hesaplanan yük %.0f W, seçim %.0f W" % (W - 440.0, EVY[1] - EVY[0], H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    for i, xx in enumerate((XI0 + 8.0, W - XI0 - 128.0)):
        ekle("fan_%d" % i, kut(xx, xx + 120.0, EVY[0] + 10.0, EVY[1] - 10.0, EVZ[0], EVZ[1]), "motor",
             bom=("Evaporatör fanı 120 × 120", 2, "24 V eksenel, 12 W", "iki kenarda; havayı evaporatörden çekip kaset sırasının üstündeki kanala basar") if i == 0 else None)''',
         '''    # v5 · SOĞUTMA PAKETİ KURU BÖLMEYE (Kemal: "standart versiyonunu bul, MOTORLARIN OLDUĞU YERE koy,
    # sonra içeriye soğuğu verecek şekilde YALITIMA BOŞLUK AÇ, içeri gitsin hava").
    # Hücrenin içinde artık hiçbir soğutma parçası yok. Fanlı evaporatör (unit cooler) kuru bölmede,
    # motorların üstünde duruyor; soğuk havayı arka yalıtımdaki ÜFLEME boşluğundan kavrama bölmesine basıyor,
    # oradan delikli perde hücreye yayıyor, dönüş yine yalıtımdaki alt boşluktan evaporatöre geliyor.
    # ÖLÇÜ: 400 × 180 × 190 (lamel paketi 140 + fan 50) — ticari sınıfın en küçük fanlı evaporatörü [V: yükümüz %.0f W, katalogdaki en küçük
    # unit cooler bile 300–500 W verir; kesin model seçilmedi]. Motorlar y 271–484'te, evaporatör 500'den başlıyor.
    EVX = (W / 2.0 - 200.0, W / 2.0 + 200.0)
    EVY = (500.0, 680.0)
    EVZ = (ZKURU[0] - 5.0, ZKURU[0] - 145.0)                                   # lamel paketi 140; fan arkasında 50
    ekle("evaporator", kut(EVX[0], EVX[1], EVY[0], EVY[1], EVZ[0], EVZ[1]), "bakir",
         bom=("Fanlı evaporatör (unit cooler)", 1, "400 × 180 × 190 (lamel 140 + fan 50) · standart sınıf", "KURU BÖLMEDE, motorların üstünde; soğuğu arka yalıtımdaki iki boşluktan hücreye verir · yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    ekle("fan_0", silz(W / 2.0, (EVY[0] + EVY[1]) / 2.0, 100.0, EVZ[1] - 3.0, EVZ[1] - 53.0), "motor",
         bom=("Evaporatör fanı Ø200", 1, "24 V eksenel · evaporatörle birlikte gelir", "havayı evaporatörden çekip yalıtımdaki üfleme boşluğuna basar"))
    # Arka yalıtımdaki (pu_arka + iç kabuk arka yüzü) İKİ BOŞLUK: üstte üfleme, altta dönüş.
    # Miller y 300–455'te; iki boşluk da o bandın dışında kaldığı için hiçbir mile denk gelmiyor.
    ekle("_bom_kanal", kut(0, 0.1, 0, 0.1, 0, -0.1), "pu",
         bom=("Yalıtım boşluğu · üfleme + dönüş", 2, "PU panelde kesit, kenarları sac bilezikli", "üfleme %.0f × %.0f (y %.0f–%.0f) · dönüş %.0f × %.0f (y %.0f–%.0f) — kuru bölmedeki evaporatörü hücreye bağlar" % (UFL[1] - UFL[0], UFY[1] - UFY[0], UFY[0], UFY[1], UFL[1] - UFL[0], DNY[1] - DNY[0], DNY[0], DNY[1])))''')

# yalitim bosluklarinin olculeri + pu_arka ve ic kabuk arkasinda delik
c = yama(c, '''    arka = kut(XI0, XI1, hy0, hy1, ZBOL[0], ZBOL[1])
    for x_, y_, k_ in MIL: arka = arka.cut(silz(x_, y_, 31.0, ZBOL[0] + 1, ZBOL[1] - 1))     # 12 mil geçişi''',
         '''    arka = kut(XI0, XI1, hy0, hy1, ZBOL[0], ZBOL[1])
    for x_, y_, k_ in MIL: arka = arka.cut(silz(x_, y_, 31.0, ZBOL[0] + 1, ZBOL[1] - 1))     # 12 mil geçişi
    for _y0, _y1 in (UFY, DNY):                                                              # v5: üfleme + dönüş boşlukları
        arka = arka.cut(kut(UFL[0], UFL[1], _y0, _y1, ZBOL[0] + 1, ZBOL[1] - 1))''')

c = yama(c, '''    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0''',
         '''    UFL = (W / 2.0 - 120.0, W / 2.0 + 120.0)                                   # yalıtım boşluklarının x aralığı
    UFY, DNY = (KAS[1] - 75.0, KAS[1] - 5.0), (KAS[0] + 5.0, KAS[0] + 40.0)    # üfleme (üstte) · dönüş (altta) — mil bandının dışında
    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0''')

# ---------------------------------------------------------------- 5 · cakisma taramasina BORU zarfi da girsin
c = yama(c, """    kb = []
    for ad, x0, x1, gen in YUVA:
        kb.append((ad, (x0 + BOSLUK / 2, x1 - BOSLUK / 2), (KAS[0], KAS[1]), (ZK[1], ZK[0])))""",
         """    kb = []
    for ad, x0, x1, gen in YUVA:
        kb.append((ad, (x0 + BOSLUK / 2, x1 - BOSLUK / 2), (KAS[0], KAS[1]), (ZK[1], ZK[0])))
        # v5: kasetin YUVARLAK BORUSU kaset kutusunun ALTINA iniyor — onun da zarfı taranmalı,
        # yoksa borunun PU tabana / raya / damlama teknesine girmesi görülmez.
        bd, be, ba = BORU[gen]
        _r = bd / 2.0 + be
        _zc = ZK[0] + ((AGIZ[gen][0] + AGIZ[gen][1]) / 2.0 - AGIZ[gen][2] / 2.0)
        kb.append((ad + " borusu", ((x0 + x1) / 2.0 - _r, (x0 + x1) / 2.0 + _r), (KAS[0] + ba, KAS[0]), (_zc - _r, _zc + _r)))""")

io.open(os.path.join(U, "topping_cad_v5.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v5.py yazildi ·", n[0], "yama")
