# -*- coding: utf-8 -*-
"""topping_hesap_v1 + topping_cad_v1  ->  v2
Kemal (22 Eyl): "kasetleri geri it, arkada bosluk olmasin; kalinliklari dogru ayarla;
sadece kasetlerin oldugu kisim sogutuculu; kablolar motorun yanindan gider."
+ onceki mesaj: "cikis agzi daha ortaya gelsin" ve "sogutucu grubu kasetlere giriyor sanki" (DOGRU cikti).

v2'DE DEGISEN:
 1 KURU BOLME GERCEK OLCUSUNE INDI: 320 -> 200 mm (mil ucu 40 + reduktor 60 + motor 76 + kablo payi 24).
   Motorun arkasindaki 142 mm bosluk kalkti; kablo motorun YANINDAN gidiyor.
 2 KASET 120 mm GERIYE GITTI, onunde ON NIS acildi: cikis agzi modul on yuzunden 10-55 mm yerine
   130-175 mm iceride. Nis YALITIMSIZ — sogutulan hacme girmiyor.
 3 EVAPORATOR KASETLERIN ICINDEN CIKTI: 5 kasetin icine giriyordu (y'de 100, z'de 75, x'te 118-282 mm).
   Artik sogouk hucrenin SAG ucunda, son yuvanin yaninda, dikey duruyor. Fan havayi sola uflemiyor,
   ustteki kanala basiyor; kanal da kasetlerin 4 mm ustunde.
 4 HAVA KANALI da kasetin icindeydi (y 504-508, kaset ustu 620) -> 624-628'e alindi.
 5 MEME YARIGI YANLIS YERDEYDI: kasetin agzi z -54,5..-10,5'te, yarik -85..-200'de acilmisti — urun
   yariga denk gelmiyordu. Yarik artik kasetin KENDI agiz olcusunden okunuyor.
 6 CAKISMA TARAMASINA KASETLER GIRDI: v1 yalniz modulun kendi 142 parcasini tariyordu, kasetler
   makine montajinda ayri birim oldugu icin kaset<->modul cakismasi HIC taranmamisti.
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:120]
    n[0] += 1
    return s.replace(a, b, 1)


# ================================================================ 1 · HESAP v2
h = io.open(os.path.join(U, "topping_hesap_v1.py"), encoding="utf-8").read()
h = h.replace("topping_hesap_v1", "topping_hesap_v2").replace("topping_cad_v1.py", "topping_cad_v2.py")
i = h.index('"""', h.index('"""') + 3)   # KAPANIS tirnagi (acilis degil)
h = h[:i] + ("\nv2 (22 Eyl 2026) — Kemal: \"kasetleri geri it, arkada bosluk olmasin; kalinliklari dogru ayarla;\n"
             "sadece kasetlerin oldugu kisim sogutuculu; kablolar motorun yanindan gider.\"\n"
             "Kuru bolme 320 -> 200 (gercek tahrik zinciri + kablo payi). Acilan 120 mm one gecti: ON NIS.\n"
             "Kaset 120 mm geriye gitti, cikis agzi o kadar iceri geldi. Nis YALITIMSIZ, sogutulan hacme girmiyor.\n") + h[i:]

# --- z dizilimini motor/reduktor tanimlarindan SONRAYA tasi (kuru bolme onlardan hesaplanacak) ---
h = yama(h, '''Z_KAPAK = (0.0, -ON_KAPAK)
Z_KASET = (-(ON_KAPAK + KULP_BOS), -(ON_KAPAK + KULP_BOS + KASET_D))          # -80 … -405
Z_KAVRAMA = (Z_KASET[1], Z_KASET[1] - KAVRAMA)                                # -405 … -445
Z_BOLME = (Z_KAVRAMA[1], Z_KAVRAMA[1] - ARKA_PU)                              # -445 … -510   (soğuk / kuru ayırıcı)
DZ = 830.0
Z_KURU = (Z_BOLME[1], -DZ)                                                    # -510 … -830   kuru makine bölmesi (320 mm)''',
          '''DZ = 830.0
# z dizilimi bölüm 2'nin sonunda kurulur: kuru bölmenin derinliği motor + redüktör ölçüsünden ÇIKAR,
# yuvarlak bir sayı olarak kabul edilmez (Kemal: "arkada boşluk olmasın").''')

h = yama(h, 'KULP_BOS = 60.0          # kapakla kaset kulpu arasi: kulp 48 tasar + 12 parmak payi  (kaset kulp boyu ureteten okunur)'.replace('arasi','arası').replace('tasar','taşar').replace('payi','payı').replace('ureteten','üreteçten'),
         'TUP_TASMA = 84.0              # kasetin CIKIS TUPU on yuzden bu kadar tasiyor [kusbasi_cad_v4: TUP_Z1 246,5 - D/2 162,5]' + chr(10) +
         'KULP_BOS = TUP_TASMA + 12.0   # v2: 60 mm yazilmisti ama TUP 84 tasiyor - agiz on kapagin icine giriyordu (cakisma taramasi yakaladi)')

h = yama(h, '''TAHRIK_Z = KAVRAMA + 18.0 + YATAK["z"] + KECE["z"] + ARKA_PU + 25.0 + REDUKTOR["z"] + MOTOR["z"]   # toplam derinlik ihtiyacı''',
         '''TAHRIK_Z = KAVRAMA + 18.0 + YATAK["z"] + KECE["z"] + ARKA_PU + 25.0 + REDUKTOR["z"] + MOTOR["z"]   # toplam derinlik ihtiyacı

# ---------------------------------------------------------------- 2b · DERİNLİK DİZİLİMİ (v2) ----------------------------------------------------------------
# KURU BÖLME artık ölçülerek çıkıyor: yalıtımdan çıkan mil ucu + redüktör + motor + kablo payı.
# v1'de 320 mm yazılmıştı, motorun arkasında 142 mm boşluk kalıyordu (Kemal gördü).
MIL_UCU = 40.0           # arka PU'dan çıkan mil + yatak/keçe kovanı [V: kovan 38 + 2 pay]
KABLO_PAY = 24.0         # motor arkası: konnektör + kablo kıvrımı. Kablolar motorun YANINDAN gider (Kemal) [V]
KURU_D = MIL_UCU + REDUKTOR["z"] + MOTOR["z"] + KABLO_PAY                     # 40 + 60 + 76 + 24 = 200
# Artan derinlik ÖNE geçer: kaset geriye gider, önünde açık NİŞ kalır → çıkış ağzı modülün içine girer.
ON_NIS = DZ - (ON_KAPAK + KULP_BOS + KASET_D + KAVRAMA + ARKA_PU + KURU_D)    # 830 − 710 = 120
assert ON_NIS >= 0.0, "derinlik dizilimi 830'a sığmıyor: %.0f mm taşıyor" % (-ON_NIS)
Z_NIS = (0.0, -ON_NIS)                                                        #    0 … −120  YALITIMSIZ (soğuk değil)
Z_KAPAK = (Z_NIS[1], Z_NIS[1] - ON_KAPAK)                                     # −120 … −140
Z_KASET = (Z_KAPAK[1] - KULP_BOS, Z_KAPAK[1] - KULP_BOS - KASET_D)            # −200 … −525
Z_KAVRAMA = (Z_KASET[1], Z_KASET[1] - KAVRAMA)                                # −525 … −565
Z_BOLME = (Z_KAVRAMA[1], Z_KAVRAMA[1] - ARKA_PU)                              # −565 … −630   (soğuk / kuru ayırıcı)
Z_KURU = (Z_BOLME[1], -DZ)                                                    # −630 … −830   kuru makine bölmesi (200 mm)''')

# --- sogutma yuku: sogutulan derinlik artik yalniz kulp + kaset + kavrama ---
h = yama(h, 'IC = dict(g=1740.0, y=380.0, z=abs(Z_BOLME[0]))          # soğuk hücre iç ölçüsü (mm): kaset zonu + kapak boşluğu',
         'IC = dict(g=1740.0, y=380.0, z=KULP_BOS + KASET_D + KAVRAMA)   # v2: SOĞUTULAN derinlik yalnız kulp boşluğu + kaset + kavrama (425);\n'
         '                                                               # ön niş yalıtımın DIŞINDA kaldı (Kemal: "sadece kasetlerin olduğu kısım soğutuculu")')

h = yama(h, '                  kuru_mm=abs(Z_KURU[1] - Z_KURU[0]), tahrik_gerek=TAHRIK_Z),',
         '                  nis=Z_NIS, kuru_mm=abs(Z_KURU[1] - Z_KURU[0]), tahrik_gerek=TAHRIK_Z,\n'
         '                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"]),')

io.open(os.path.join(U, "topping_hesap_v2.py"), "w", encoding="utf-8").write(h)
print("topping_hesap_v2.py yazildi")

# ================================================================ 2 · CAD v2
c = io.open(os.path.join(U, "topping_cad_v1.py"), encoding="utf-8").read()
c = c.replace("topping_hesap_v1", "topping_hesap_v2").replace("topping_cad_v1", "topping_cad_v2").replace("topping_modul_v1", "topping_modul_v2")
i = c.index('"""', c.index('"""') + 3)   # KAPANIS tirnagi
c = c[:i] + ("\nv2 (22 Eyl 2026): kuru bolme 200 (arkada bosluk yok) · kaset 120 geriye, onunde ON NIS ·\n"
             "evaporator ve hava kanali kasetlerin ICINDEN cikarildi · meme yarigi kasetin kendi agiz olcusunden ·\n"
             "cakisma taramasina KASETLER girdi. Onceki: topping_cad_v1.py\n") + c[i:]

c = yama(c, 'ZK = H.Z_KASET; ZKAP = H.Z_KAPAK; ZKAV = H.Z_KAVRAMA; ZBOL = H.Z_BOLME; ZKURU = H.Z_KURU',
         'ZK = H.Z_KASET; ZKAP = H.Z_KAPAK; ZKAV = H.Z_KAVRAMA; ZBOL = H.Z_BOLME; ZKURU = H.Z_KURU; ZNIS = H.Z_NIS')

# --- kaset ureticinden AGIZ olcusu de okunsun ---
c = yama(c, 'KASET_CAD = {140: "kiyma_cad_v5", 280: "kasar_cad_v10"}',
         '''KASET_CAD = {140: "kiyma_cad_v5", 280: "kasar_cad_v10"}


def agiz(modul):
    """kasetin ÇIKIŞ AĞZININ kaset yerel z aralığı — meme yarığı buna göre açılır.
    v1'de yarık kasetin ön yüzünden 5 mm geride başlıyordu; ağız ise ön yüzün ÖNÜNDEYDİ,
    yani ürün yarığa denk GELMİYORDU. Artık kasetin kendi ölçüsünden okunuyor."""
    import re
    k = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    g = lambda ad: float(re.search(r"^%s.*?=\\s*([\\d.]+)" % ad, k, re.M | re.S).group(1))
    m = re.search(r"^AG_Z0, AG_Z1, AG_X\\s*=\\s*([\\d.]+),\\s*([\\d.]+)", k, re.M)
    d = re.search(r"^W, D, H\\s*=\\s*([\\d.]+),\\s*([\\d.]+)", k, re.M)
    return float(m.group(1)), float(m.group(2)), float(d.group(2))


AGIZ = {g: agiz(m) for g, m in KASET_CAD.items()}''')

# --- meme yarigi: agizdan ---
c = yama(c, '    ZY = (ZK[0] - 5.0, ZK[0] - 120.0)                                         # yarığın derinlik aralığı (kasetin ön bölgesi)',
         '''    # MEME YARIĞI kasetin KENDİ ağız ölçüsünden: kaset yerel z → modül z (kaset ön yüzü ZK[0]).
    _a0, _a1, _dd = AGIZ[280]
    ZY = (ZK[0] + (_a1 - _dd / 2.0) + 6.0, ZK[0] + (_a0 - _dd / 2.0) - 6.0)   # ağzın z aralığı + 6 mm pay''')

# --- evaporator: sag uca dikey, kasetlerin DISINA ---
c = yama(c, '''    ekle("evaporator", kut(420.0, 1280.0, hy1 - 120.0, hy1 - 20.0, ZBOL[0] + 5.0, ZBOL[0] + 115.0), "bakir",
         bom=("Evaporatör", 1, "lamelli, paslanmaz karter", "soğuk hücrenin üst-arkasında; hesaplanan yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    for i, xx in enumerate((560.0, 1140.0)):
        ekle("fan_%d" % i, silz(xx, hy1 - 58.0, 55.0, ZBOL[0] + 118.0, ZBOL[0] + 168.0), "motor",
             bom=("Evaporatör fanı Ø150", 2, "24 V eksenel, 12 W", "havayı kasetlerin üstünden geçirir") if i == 0 else None)
    ekle("hava_kanali", kut(XI0 + SAC_IC + 2.0, XI1 - SAC_IC - 2.0, hy1 - 136.0, hy1 - 132.0, ZBOL[0] + 4.0, ZK[0]), "sac",
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "soğuk havayı kaset sırasının üstüne dağıtır, doğrudan üflemez"))''',
         '''    # v1'de evaporatör y 520–620 · z −440…−330'daydı ve BEŞ KASETİN İÇİNE giriyordu (Kemal gördü).
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
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "sağdaki evaporatörden gelen soğuk havayı kaset sırasının üstünde boydan boya dağıtır"))''')

# --- CAKISMA TARAMASINA KASETLER ---
c = yama(c, '    # ---- KASET YUVAYA SIĞIYOR MU + TAHRİK EKSENİ TUTUYOR MU ----',
         '''    # ---- KASET ZARFI ↔ MODÜL ÇAKIŞMASI (v2'de eklendi) ----
    # v1 yalnız modülün KENDİ parçalarını tarıyordu; kasetler makine montajında ayrı birim olduğu için
    # kaset ile modül arasındaki çakışma HİÇ taranmamıştı. Evaporatörün beş kasetin içine girmesi böyle kaçtı.
    kb = []
    for ad, x0, x1, gen in YUVA:
        kb.append((ad, (x0 + BOSLUK / 2, x1 - BOSLUK / 2), (KAS[0], KAS[1]), (ZK[1], ZK[0])))
    ac = []
    for p in PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"].startswith(("ray_", "bolme_", "huni_", "konum_pimi_", "ic_kabuk", "pu_")):
            continue                                                            # kasete DEĞMESİ gereken parçalar
        bb = p["wp"].val().BoundingBox()
        for ad, xa, ya, za in kb:
            o = (min(xa[1], bb.xmax) - max(xa[0], bb.xmin), min(ya[1], bb.ymax) - max(ya[0], bb.ymin), min(za[1], bb.zmax) - max(za[0], bb.zmin))
            if all(v > 0.5 for v in o):
                ac.append((p["ad"], ad, tuple(round(v) for v in o)))
    print("KASET <-> MODUL CAKISMASI: %s" % ("TEMIZ" if not ac else "%d BULGU" % len(ac)))
    for a_ in ac[:14]:
        print("   %-22s %-12s ortak %s mm" % a_)
    assert not ac, "kaset zarfi modul parcasiyla cakisiyor"

    # ---- KASET YUVAYA SIĞIYOR MU + TAHRİK EKSENİ TUTUYOR MU ----''')

c = yama(c, '"TOPPING MODULU v1', '"TOPPING MODULU v2')
c = yama(c, '          % (H.ON_KAPAK, H.KULP_BOS, H.KASET_D, H.KAVRAMA, H.ARKA_PU, abs(ZKURU[1] - ZKURU[0]), D))',
         '          % (H.ON_NIS, H.ON_KAPAK, H.KULP_BOS, H.KASET_D, H.KAVRAMA, H.ARKA_PU, abs(ZKURU[1] - ZKURU[0]), D))')
c = yama(c, '"   derinlik: kapak %.0f', '"   derinlik: ON NIS %.0f | kapak %.0f')

io.open(os.path.join(U, "topping_cad_v2.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v2.py yazildi ·", n[0], "yama")
