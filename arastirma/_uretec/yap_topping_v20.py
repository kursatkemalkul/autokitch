# -*- coding: utf-8 -*-
"""topping_cad_v19 -> v20 : TEPSISIZ KURGU · CALISMA DISKI · BANDA AKTARMA

Kemal 23 Eyl 2026, karar listesi onaylandi: tepsi yok, hamur tablada acilir,
acici konili donen kafa (modul A'da), pide firin bandina aktarilir.

BU SURUMDE YAPILANLAR

1) TEPSI IZLERI SILINDI
   Merkezleme pimleri (tepsinin altindaki konik cukurlara giriyordu) ve tablanin
   kenarindaki uc PARMAK KESIGI (robot Ø340 tepsinin altina parmak soksun diye
   aciliyordu) kaldirildi. Kesikler artik ZARARLI: hamur dogrudan bu yuzeyde
   aciliyor, delige girer.

2) CALISMA DISKI
   Ø340 x 8 mat gida UHMW, elle cikar, uc pimle tutulur, yedekli.
   MAT olacak: cilali yuzeyde koniler hamuru ACMAZ, yerinde DONDURUR — videolarda
   hamur mat mavi PU bandin uzerinde aciliyor, sebebi bu.
   KENAR son 15 mm'de 8 -> 2 mm'ye iner. Bant hamuru SOYARAK birakiyor, surterek
   degil; kalin ve dik kenar pideyi surukler, ince kenar soymaya izin verir.
   Ust yuzu y 108. Dozaj dusme yuksekligi 144 mm (tepsili kurguda 135 idi).

3) TABLA KILIDI
   Acma aninda konilerin artik torku tablayi cevirmesin diye ayar bileziginde uc
   delik; govdeye bagli pim acicinin altinda girer. Gereken tork 3-5 N.m, pancake
   motorun tutma torku 0,9 N.m — motor yetmiyor, mekanik kilit sart.
   DOZAJ HIZINA DOKUNULMADI (Kemal: o denge bozulmayacak). Kilit yalniz acma aninda.

4) RAY IKI UCTA UZADI
   sol -500 : acici modul A'da olmak zorunda — TOPPING'in icine sigmiyor, kasetler
              x 256-1544'u kapliyor ve tablanin ustunde 20 mm bosluk var.
   sag 1785 : pideyi banda birakmak icin tabla modul yuzune kadar gitmeli.
   NOT: bu, "istasyon kapali urundur, baska module tasmaz" kuralini deliyor.
   Kemal'e soylendi, kabul edildi.

5) BANDA AKTARMA
   Modul sag yuzunde yarik + sabit BICAK KOPRUSU, ust yuzu y 108,3 (diskin
   0,3 mm ustunde). Tabla ilerler, pidenin on kenari 0,3 mm'lik pahtan kopruye
   ciker, firin bandi (bicak burunlu, yuzeyi ayni kotta) onu CEKER.
   Tabla bandin altina GIRMEZ — bant burnu diskin kotunda, arada 3 mm bosluk.
   Ek motor ve sensor yok; hareketi X ekseni yapiyor.

6) TABLA BOS MU SENSORU  aktarma noktasinda yukaridan mesafe sensoru.
   Temiz disk duz yuzey, pide 8-10 mm — fark rahat goruluyor.

7) FIRE SILECEGI
   Pide yapisip kalirsa: bir kez daha denenir, olmazsa tabla kirinti cekmecesinin
   ustune gider, lastik silecek iner ve diski siyirir. Hat sonraki siparise devam
   eder. ROBOT MUDAHALE ETMEZ — ustu malzemeli ham hamur tutulmaz, itilmez.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v19.py"), encoding="utf-8").read()
D = []

# ============================================================ 1+2 · TABLA ve CALISMA DISKI
D.append((
    '''    tb_ = sily(Xc, ZT, RT_, 97.0, 100.0)
    for i_ in range(3):                                                                           # robot parmak kesikleri
        a_ = math.radians(120.0 * i_ + 60.0)
        tb_ = tb_.cut(kut(Xc + (RT_ - 25.0) * math.cos(a_) - 30.0, Xc + (RT_ - 25.0) * math.cos(a_) + 30.0,
                          96.0, 101.0, ZT + (RT_ - 25.0) * math.sin(a_) - 12.5, ZT + (RT_ - 25.0) * math.sin(a_) + 12.5))
    ekle("tabla", tb_, "sac", bom=("Döner tabla Ø340 × 3", 1, "304 · göbeğe sürekli TIG kaynak, parlatılmış",
         "gıda yüzeyinde cıvata yok; kenarda 120°'de 3 parmak kesiği 60 × 25 — robot Ø340 tepsinin altına parmak sokabilsin"))
    for i_ in range(3):
        a_ = math.radians(120.0 * i_)
        ekle("merkezleme_pimi_%s" % "ABC"[i_], koni_y_t(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 2.0, 5.0, 100.0, 105.0), "celik",
             bom=("Merkezleme pimi · konik", 3, "304 · taban Ø10 tepe Ø4 boy 5 · H7/r6 presli", "r = 100'de 120° aralıklı; tepsinin altındaki 3 konik çukura girer, hem merkezler hem POZİTİF döndürür") if i_ == 0 else None)''',
    '''    # v20 · TEPSI YOK: robot parmak kesikleri KALDIRILDI. Hamur artik dogrudan bu
    # yuzeyde aciliyor; kesik olursa hamur delige girer.
    tb_ = sily(Xc, ZT, RT_, 97.0, 100.0)
    ekle("tabla", tb_, "sac", bom=("Döner tabla Ø340 × 3", 1, "304 · göbeğe sürekli TIG kaynak",
         "TAŞIYICI tabla — gıda yüzeyi DEĞİL; gıda yüzeyi üstündeki çalışma diski"))
    # v20 · CALISMA DISKI = gida yuzeyi. Tabla gobege kaynakli, sokulemiyor; yikanabilsin
    # diye ustune elle cikan disk kondu. Kenari 15 mm'de 2 mm'ye iner (soyma).
    # UST YUZ Ø340 BOYUNCA DUZ (y 108) — pide duz zeminde acilmali.
    # INCELME ALT YUZDE: son 15 mm'de taban 100 -> 106'ya cikar, kenar 2 mm kalir.
    _dsk = sily(Xc, ZT, RT_, 106.0, 108.0)                                  # tum disk 2 mm ust kabuk
    _dsk = _dsk.union(sily(Xc, ZT, RT_ - 15.0, 100.0, 106.0))               # ortada tam kalinlik
    _dsk = _dsk.union(koni_y_t(Xc, ZT, RT_, RT_ - 15.0, 100.0, 106.0))      # alt yuzde konik gecis
    for i_ in range(3):                                                     # pim delikleri
        a_ = math.radians(120.0 * i_)
        _dsk = _dsk.cut(sily(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 4.1, 99.0, 109.0))
    ekle("calisma_diski", _dsk, "pom",
         bom=("Çalışma diski Ø340 · 8 → 2", 1, "mat gıda UHMW-PE (ya da PU kaplı) · elle çıkar · yedekli",
              "GIDA YÜZEYİ: hamur burada açılır, malzeme buna dökülür, akşam sökülüp yıkanır. "
              "MAT olacak — cilalı yüzeyde koniler hamuru açmaz, yerinde döndürür. "
              "Kenar son 15 mm'de 2 mm'ye iner: pide soyularak ayrılır, sürüklenmez"))
    for i_ in range(3):
        a_ = math.radians(120.0 * i_)
        ekle("disk_pimi_%s" % "ABC"[i_], sily(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 4.0, 100.0, 108.0), "celik",
             bom=("Disk konum pimi Ø8 × 8", 3, "304 · tablaya H7/r6 presli",
                  "r = 100'de 120° aralıklı; çalışma diskini yerinde tutar (sıyrılırken kaymasın). "
                  "Diskle AYNI KOTTA biter — gıda yüzeyinde çıkıntı yok") if i_ == 0 else None)'''))

# ============================================================ 3 · TABLA KILIDI
D.append((
    '''    ekle("tabla_home_sensoru", sily(Xc, ZT - 128.0, 4.0, 66.5, 76.5), "koyu",''',
    '''    # v20 · TABLA KILIDI: acma aninda konilerin artik torku tablayi cevirmesin.
    # Gereken 3-5 N.m, pancake motorun tutma torku 0,9 N.m — motor yetmiyor.
    for i_ in range(3):                                                     # burc: delik ayar bileziginde ACILIR
        a_ = math.radians(120.0 * i_ + 40.0)
        _bx, _bz = Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_)
        ekle("kilit_burcu_%d" % i_, sily(_bx, _bz, 7.0, 80.8, 86.0).cut(sily(_bx, _bz, 5.0, 80.0, 87.0)), "celik",
             bom=("Kilit burcu Ø14/Ø10", 3, "sertleştirilmiş 420 · ayar bileziğine presli",
                  "açıcının altında gövdeye bağlı pim buraya girer, tabla dönmez. "
                  "DOZAJ HIZINA DOKUNULMADI — kilit yalnız açma anında") if i_ == 0 else None)
    ekle("tabla_home_sensoru", sily(Xc, ZT - 128.0, 4.0, 66.5, 76.5), "koyu",'''))

# ============================================================ 4 · RAY IKI UCTA UZUYOR
D.append((
    '''        _r, _n = hiwin_ray(65.0, 1665.0, zc_)''',
    '''        # v20: ray iki ucta da uzadi — solda acici (modul A), sagda banda aktarma
        _r, _n = hiwin_ray(-500.0, 1785.0, zc_)'''))
D.append((
    '''    tk = kut(15.0, 1695.0, 1.5, 4.5, -5.0, -415.0)
    tk = tk.union(kut(15.0, 1695.0, 1.5, 31.5, -5.0, -8.0)).union(kut(15.0, 1695.0, 1.5, 31.5, -412.0, -415.0))''',
    '''    tk = kut(-520.0, 1790.0, 1.5, 4.5, -5.0, -415.0)
    tk = tk.union(kut(-520.0, 1790.0, 1.5, 31.5, -5.0, -8.0)).union(kut(-520.0, 1790.0, 1.5, 31.5, -412.0, -415.0))'''))
D.append((
    '''        ekle("ray_kirisi_%s" % ad_, kut(45.0, 1695.0, 4.5, 20.5, z0_, z1_), "celik",''',
    '''        ekle("ray_kirisi_%s" % ad_, kut(-520.0, 1790.0, 4.5, 20.5, z0_, z1_), "celik",'''))
D.append((
    '''    ekle("kayis_kirisi", kut(15.0, 1695.0, 4.5, 20.5, -385.0, -335.0), "celik",''',
    '''    ekle("kayis_kirisi", kut(-520.0, 1790.0, 4.5, 20.5, -385.0, -335.0), "celik",'''))
D.append((
    '''        ct = kut(45.0, 1695.0, 20.5, 44.0, zc_ - 37.0, zc_ + 37.0).cut(kut(40.0, 1700.0, 19.5, 45.0, zc_ - 33.0, zc_ + 33.0))''',
    '''        ct = kut(-520.0, 1790.0, 20.5, 44.0, zc_ - 37.0, zc_ + 37.0).cut(kut(-525.0, 1795.0, 19.5, 45.0, zc_ - 33.0, zc_ + 33.0))'''))
D.append((
    '''    ekle("enerji_zinciri_kanali", kut(15.0, 1695.0, 4.5, 64.5, -500.0, -440.0).cut(kut(18.0, 1692.0, 6.5, 65.5, -497.0, -443.0)), "sac",''',
    '''    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, 4.5, 64.5, -500.0, -440.0).cut(kut(-517.0, 1787.0, 6.5, 65.5, -497.0, -443.0)), "sac",'''))

# ============================================================ 5+6+7 · AKTARMA, SENSOR, SILECEK
D.append((
    '''    ekle("agiz_alt_dudagi", kut(30.0, 1770.0, 1.5, 13.5, 0.0, -4.5)''',
    '''    # ---------------- 8c · BANDA AKTARMA (v20) ----------------
    # Tepsi kalkinca pideyi tabladan almak yeni bir is oldu. EK MAKINE YOK.
    # Tabla ilerler, pidenin on kenari 0,3 mm'lik pahtan sabit KOPRUYE ciker;
    # firin bandi (bicak burunlu, yuzeyi ayni kotta) pideyi CEKER.
    # Tabla bant burnunun ALTINA GIRMEZ — bant burnu diskin kotunda, arada bosluk.
    AKT_Y = 108.3                                               # diskin 0,3 mm ustu
    AKT_X0, AKT_X1 = 1700.0, 1800.0                             # koprü: tabla ucu … modül yüzü
    # KOPRU YALNIZ PIDENIN GENISLIGINI ORTER (Ø280 -> ZT +- 140), cunku ZT-180
    # bolgesinde X TAHRIK MOTORU var. 5 mm pay ile ZT +- 145.
    AKT_Z0, AKT_Z1 = ZT - 145.0, ZT + 145.0
    # UST yuzu AKT_Y (108,3) — pide bunun USTUNE cikacak, plaka asagi dogru kalin.
    _kpr = kut(AKT_X0, AKT_X1, AKT_Y - 3.0, AKT_Y, AKT_Z0, AKT_Z1)
    # giris agzi: 10 mm'de 1,5 mm'lik pah — pide 0,3 mm'lik basamaga carpmaz, tirmanir
    _pah = (cq.Workplane("XY").box(12.0, AKT_Z1 - AKT_Z0 + 4.0, 3.0, centered=False)
            .translate((AKT_X0 - 1.0, AKT_Z0 - 2.0, AKT_Y - 1.5))
            .rotate(cq.Vector(AKT_X0 + 10.0, 0.0, AKT_Y), cq.Vector(AKT_X0 + 10.0, 1.0, AKT_Y), 8.5))
    _kpr = _kpr.cut(_pah)
    ekle("aktarma_koprusu", _kpr, "celik",
         bom=("Aktarma köprüsü 100 × 360 × 3", 1, "304 · üst yüzü taşlanmış, ağzı 15° pah",
              "pide tabladan buna çıkar, fırın bandı buradan çeker. Üst yüzü çalışma diskinin "
              "0,3 mm üstünde. FIRIN BANDI ŞARTI: bıçak burunlu, yüzeyi y 108,3 ± 1, burnu "
              "modül yüzünden en çok 5 mm içeride [bant seçilince doğrulanacak]"))
    # ASKI: kopru ASAGIDAN degil YUKARIDAN tasinir. Alttan destek koyacak yer yok —
    # araba oradan geciyor. Askilar tablanin Ø340 yolunun disinda (z -345 ve z +5).
    for i_, zb in enumerate((-350.0, 5.0)):
        ekle("kopru_askisi_%d" % i_, kut(AKT_X0 + 10.0, AKT_X1 - 15.0, AKT_Y, 245.0, zb, zb + 10.0)
             .union(kut(AKT_X0, AKT_X1 - 15.0, AKT_Y, AKT_Y + 25.0, zb, zb + 10.0)), "sac",
             bom=("Köprü askısı", 2, "304 10 mm lama · üstten iç kabuğa cıvatalı",
                  "köprüyü YUKARIDAN taşır; altta destek koyacak yer yok, araba oradan geçiyor. "
                  "Tablanın Ø340 yolunun dışında (z -350 ve z +5)") if i_ == 0 else None)
    ekle("cikis_yarigi_contasi", kut(1792.0, 1798.5, 92.0, 130.0, AKT_Z0 - 10.0, AKT_Z1 + 10.0)
         .cut(kut(1791.0, 1799.5, AKT_Y - 4.0, 126.0, AKT_Z0 - 2.0, AKT_Z1 + 2.0)), "silikon",
         bom=("Çıkış yarığı çerçevesi + fırça", 1, "304 çerçeve + gıda tipi fırça sızdırmaz",
              "dış yan sacta 380 × 38 yarık; pide geçer, soğuk hava ve kir geçmez"))
    ekle("tabla_bos_sensoru", sily(1650.0, ZT, 9.0, 150.0, 190.0), "koyu",
         bom=("Tabla boş mu sensörü · lazer mesafe", 1, "IP67 · 50-300 mm · analog",
              "aktarmadan sonra bakar: temiz disk düz yüzey, pide 8-10 mm — farkı görür. "
              "Pide kalmışsa bir kez daha denenir, olmazsa fire silecegine gidilir"))
    # CIZIMDE GERI CEKILMIS KONUMDA: indirilmis halde cizilirse tabla her gecisinde
    # ona carpar. Calisma yuksekligi y 108 (diske deger), park yuksekligi y 125.
    ekle("fire_silecegi", kut(250.0, 270.0, 125.0, 167.0, ZT - 180.0, ZT + 180.0), "silikon",
         bom=("Fire sileceği", 1, "gıda tipi silikon lastik + 24 V aktüatör",
              "pide tablaya yapışıp kalırsa: tabla kırıntı çekmecesinin üstüne gelir, silecek "
              "iner ve diski sıyırır; pide fire, hat sonraki siparişe devam eder. "
              "Normalde diske DEĞMEZ, yalnız temizlik hareketinde iner"))

    ekle("agiz_alt_dudagi", kut(30.0, 1770.0, 1.5, 13.5, 0.0, -4.5)'''))

# ============================================================ 3b · AYAR BILEZIGINDE KILIT DELIKLERI
D.append((
    '''    ekle("ayar_bilezigi", sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0)), "celik",''',
    '''    _ab = sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0))
    for i_ in range(3):                                                     # v20: kilit burcu delikleri
        a_ = math.radians(120.0 * i_ + 40.0)
        _ab = _ab.cut(sily(Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_), 7.0, 80.0, 87.0))
    ekle("ayar_bilezigi", _ab, "celik",'''))

for e, y in D:
    assert e in s, "BULUNAMADI -> " + e[:80]
    s = s.replace(e, y, 1)

# dis yan saclarda cikis yarigi (sag) ve giris yarigi (sol)
eski = '''        ekle("dis_yan_" + s, kut(x, x + SAC, SAC, Y - SAC, 0, -D), "sac",'''
yeni = '''        # v20: tabla iki uctan da modulden CIKIYOR — solda aciciya (modul A),
        # sagda firin bandina. Iki yan sacta da tabla yuksekliginde yarik var.
        _ys = kut(x, x + SAC, SAC, Y - SAC, 0, -D)
        # DUZELTME: once iki ayri delik acilmisti (tabla 92-130 ve mekanizma 1-66);
        # arada 66-92 DOLU kaliyordu ve tam oraya DONER YATAK (58,5-80,8) ile
        # AYAR BILEZIGI (80,8-86) denk geliyordu — tabla soldaki aciciya GECEMIYORDU.
        # Artik modulun alt bandi iki uctan da TEK PARCA acik: araba plakasi,
        # yatak, bilezik, gobek, tabla ve disk serbest gecer.
        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 132.0, -510.0, 0.0))
        ekle("dis_yan_" + s, _ys, "sac",'''
assert eski in s, "yan sac bulunamadi"
s = s.replace(eski, yeni, 1)

# ---- X TAHRIKI SOL UCA TASINIYOR
# Motor ve kaidesi x 1690-1780'de, yani ARTIK URUN CIKISININ tam ortasindaydi.
# Aktarma koprusu ve askilari oraya giriyor. Cikis sag uctan oldugu icin tahrik
# sol uca aliniyor; avara kasnak da saga geciyor. Kayis duzeni degismiyor.
_D2 = [
 ('silz(1735.0, 31.0, 9.55, -364.5, -355.5).cut(silz(1735.0, 31.0, 4.1, -366.0, -354.0))',
  'silz(-465.0, 31.0, 9.55, -364.5, -355.5).cut(silz(-465.0, 31.0, 4.1, -366.0, -354.0))'),
 ('.translate(cq.Vector(1735.0, 41.5, -360.0))',
  '.translate(cq.Vector(-465.0, 41.5, -360.0))'),
 ('kut(1690.0, 1780.0, 20.5, 38.0, -400.0, -320.0).cut(kut(1700.0, 1770.0, 19.5, 39.0, -392.0, -328.0))',
  'kut(-510.0, -420.0, 20.5, 38.0, -400.0, -320.0).cut(kut(-500.0, -430.0, 19.5, 39.0, -392.0, -328.0))'),
 ('silz(35.0, 31.0, 9.55, -364.5, -355.5)',
  'silz(1750.0, 31.0, 9.55, -364.5, -355.5)'),
 ('kut(20.0, 44.0, 20.5, 45.0, -385.0, -335.0).cut(silz(35.0, 31.0, 12.0, -372.0, -348.0))',
  'kut(1735.0, 1759.0, 20.5, 45.0, -385.0, -335.0).cut(silz(1750.0, 31.0, 12.0, -372.0, -348.0))'),
 ('kut(52.0, 1686.0, 26.5, 35.5, zc_ - 1.5, zc_ + 1.5)',
  'kut(-448.0, 1733.0, 26.5, 35.5, zc_ - 1.5, zc_ + 1.5)'),
]
for _e, _y in _D2:
    assert _e in s, "X TAHRIK BULUNAMADI -> " + _e[:60]
    s = s.replace(_e, _y, 1)

# ---- YAN SACLARDA MEKANIZMA GECISI
# Ray, tekne, kirisler ve enerji zinciri artik iki yandan da disari cikiyor.
# Yalitimin ALTINDA kaldiklari icin soguk hucreyi delmiyorlar (hucre y 250'den baslar).
_e = 'ekle("dis_yan_" + s, _ys, "sac",'
_y = ('_ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 66.0, -510.0, -1.0))   # mekanizma gecisi\n'
      '        ekle("dis_yan_" + s, _ys, "sac",')
assert _e in s
s = s.replace(_e, _y, 1)

io.open(os.path.join(U, "topping_cad_v20.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v20.py yazildi ·", len(D) + 1, "donusum")
