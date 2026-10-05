# -*- coding: utf-8 -*-
"""Claude'un TOPPING v21 tasarimini mevcut AUTOKITCH zincirine guvenli sekilde alir.

Yeni surumler:
  topping_hesap_v6.py   hareket geometrisinin tek sayisal kaynagi
  topping_cad_v22.py    uzatilmis ray + gercek tam boy X tahriki
  sim_makine_v6.py      web/PLC hareket tanimi ayni sayilari okur
  hat_montaj_v34.py     kasetleri degistirmeden yeni istasyon montaji

Kaynak dosyalar ASLA ezilmez. Her degisiklik assert'li metin donusumudur.
"""
from pathlib import Path

U = Path(__file__).resolve().parent


def oku(ad):
    return (U / ad).read_text(encoding="utf-8")


def yaz(ad, s):
    (U / ad).write_text(s, encoding="utf-8")
    print("YAZILDI", ad)


def rep(s, eski, yeni, adet=1):
    n = s.count(eski)
    assert n == adet, "beklenen %d, bulunan %d: %s" % (adet, n, eski[:120])
    return s.replace(eski, yeni, adet)


def blok(s, bas, son, yeni):
    """Baslangic ve bitis isaretleri arasini, iki isareti koruyarak degistirir."""
    assert s.count(bas) == 1, "baslangic isareti tek degil: %s" % bas
    assert s.count(son) == 1, "bitis isareti tek degil: %s" % son
    i = s.index(bas) + len(bas)
    j = s.index(son, i)
    return s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- HESAP v6
s = oku("topping_hesap_v5.py")
s = rep(s, "v4 (22 Eyl 2026): DONER TABLA hesabi eklendi — x ekseni stroku/hizi, tabla devri, dikey dizilim.\n",
        "v4 (22 Eyl 2026): DONER TABLA hesabi eklendi — x ekseni stroku/hizi, tabla devri, dikey dizilim.\n"
        "v6 (24 Eyl 2026): TEPSISIZ v21 geometriye uyarlandi. Park -350, aktarma 1637;\n"
        "ray, kayis, limitler ve motor kuvveti tek kaynaga alindi. Kaset dozaj yasasi DEGISTIRILMEDI.\n")
s = rep(s,
        "TEPSI_K, TABLA_K, HAMUR_K = 12.0, 14.0, 8.0                                  # tepsi · tabla · hamur kalınlıkları [V]\n",
        "TEPSI_K, TABLA_K, HAMUR_K = 0.0, 14.0, 8.0                                   # v20+: tepsi YOK · tabla · hamur [V]\n")
eski = """# Strok: ilk ve son yuva merkezi arası + dozaj salınımı + robotun tepsiyi bıraktığı yükleme noktası
YUVA_ACIKLIK = 1075.0                                                        # topping_cad YUVA merkezlerinden ölçüldü
X_STROK = YUVA_ACIKLIK + R_DIS + 120.0                                       # 1300 mm
"""
yeni = """# v21 HAREKET ZARFI. Bu sayilar CAD, web kontrolu ve Isaac tarafinda TEK KAYNAKTIR.
# Parkta tabla soldaki acicinin altinda; dozajdan sonra sagdaki firin bandina teslim eder.
X_PARK = -350.0                                                              # acici / normal bekleme merkezi [CAD v21]
X_AKTARMA = 1637.0                                                           # disk kenari x=1807, bant burnu x=1815 -> 8 mm [CAD v21]
X_LIMIT_SOL, X_LIMIT_SAG = -380.0, 1660.0                                   # yazilimdan once donanim limitleri [V]
RAY_X0, RAY_X1 = -500.0, 1785.0                                             # HGR15 ray gercek boyu = 2285 mm [CAD v21]
KAYIS_SOL, KAYIS_SAG = -535.0, 1835.0                                      # GT3 kasnak merkezleri; araba butun strokte kayisa bagli
X_STROK = X_AKTARMA - X_PARK                                                # 1987 mm gercek is stroku
RAY_UZUNLUK = RAY_X1 - RAY_X0
KAYIS_MERKEZ = KAYIS_SAG - KAYIS_SOL
KASNAK_CEVRE = 60.0                                                         # GT3 20 dis x 3 mm
KASNAK_R = KASNAK_CEVRE / (2.0 * math.pi)
KAYIS_UZUNLUK = 2.0 * KAYIS_MERKEZ + KASNAK_CEVRE                         # esit kasnakli kapali cevrim = 4800 mm

# X motoru: uzayan ray TORKU degistirmez; hareket suresini ve kayis boyunu degistirir.
# Hareketli kutle, 24 Eyl fizik ihracindan: ARABA 15,763 + TABLA 6,256 + hamur ~0,50 kg.
X_HAREKET_KUTLE = 22.52                                                     # kg [K: topping_fizik_ihrac_v16]
X_RAMP_S = 0.15                                                             # 0 -> 200 mm/s [K: makine_kodu.js]
X_IVME = (X_GECIS_HIZ / 1000.0) / X_RAMP_S
X_SURTUNME_KUVVET = 10.0                                                    # N [V: 4 HGH15 blok + kablo zinciri; prototipte olculecek]
X_GEREKEN_KUVVET = X_HAREKET_KUTLE * X_IVME + X_SURTUNME_KUVVET
X_GEREKEN_TORK = X_GEREKEN_KUVVET * (KASNAK_R / 1000.0)
X_MOTOR_TORK = 1.2                                                          # N.m [katalog STP-MTR-23079 sinifi]
X_TORK_PAY = X_MOTOR_TORK / X_GEREKEN_TORK
"""
s = rep(s, eski, yeni)
s = rep(s,
        "               x_gecis_hiz=X_GECIS_HIZ, x_strok=X_STROK),\n",
        "               x_gecis_hiz=X_GECIS_HIZ, x_strok=X_STROK, x_park=X_PARK, x_aktarma=X_AKTARMA,\n"
        "               x_limit=[X_LIMIT_SOL, X_LIMIT_SAG], ray=[RAY_X0, RAY_X1],\n"
        "               kayis_kasnak=[KAYIS_SOL, KAYIS_SAG], kayis_uzunluk=round(KAYIS_UZUNLUK, 1)),\n")
s = rep(s,
        "    elektrik=dict(motor_A=MOTOR_A, ayni_anda=AYNI_ANDA, guc_kaynagi_W=round(GUC_KAYNAGI), kart=KART))",
        "    elektrik=dict(motor_A=MOTOR_A, ayni_anda=AYNI_ANDA, guc_kaynagi_W=round(GUC_KAYNAGI), kart=KART),\n"
        "    x_tahrik=dict(hareketli_kg=X_HAREKET_KUTLE, ivme_m_s2=round(X_IVME, 3),\n"
        "                  gereken_N=round(X_GEREKEN_KUVVET, 1), gereken_Nm=round(X_GEREKEN_TORK, 3),\n"
        "                  motor_Nm=X_MOTOR_TORK, tork_payi=round(X_TORK_PAY, 2), surtunme_N=X_SURTUNME_KUVVET))")
s = rep(s,
        "    print(\"   araba hizi: dozajda %.1f mm/s · yuvadan yuvaya %.0f mm/s · toplam strok %.0f mm\" % (X_DOZ_HIZ, X_GECIS_HIZ, X_STROK))\n",
        "    print(\"   araba hizi: dozajda %.1f mm/s · geciste %.0f mm/s · is stroku %.0f mm (park %.0f -> aktarma %.0f)\" % (X_DOZ_HIZ, X_GECIS_HIZ, X_STROK, X_PARK, X_AKTARMA))\n"
        "    print(\"   HGR15 ray %.0f mm · GT3 kapali kayis %.0f mm · kasnak merkezleri %.0f mm\" % (RAY_UZUNLUK, KAYIS_UZUNLUK, KAYIS_MERKEZ))\n"
        "    print(\"   X hareketli %.2f kg · %.2f m/s2 · gereken %.1f N / %.3f N.m · motor %.1f N.m = %.1f kat\" % (X_HAREKET_KUTLE, X_IVME, X_GEREKEN_KUVVET, X_GEREKEN_TORK, X_MOTOR_TORK, X_TORK_PAY))\n")
s = rep(s, 'os.path.join(U, "topping_hesap_v4.json")', 'os.path.join(U, "topping_hesap_v6.json")')
s = rep(s, 'print("topping_hesap_v4.json yazildi")', 'print("topping_hesap_v6.json yazildi")')
yaz("topping_hesap_v6.py", s)


# ---------------------------------------------------------------- CAD v22
s = oku("topping_cad_v21.py")
s = rep(s, "import topping_hesap_v5 as H", "import topping_hesap_v6 as H")
s = rep(s, 'URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "topping_modul_v10")',
        'URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "topping_modul_v22")')
s = rep(s, "arastirma/3_TOPPING/topping_modul_v10/", "arastirma/3_TOPPING/topping_modul_v22/")
s = rep(s, "XC_TABLA = -350.0          # tablanin CIZILDIGI yer = PARK KONUMU (acicinin alti)",
        "XC_TABLA = H.X_PARK          # tablanin CIZILDIGI yer = PARK KONUMU (acicinin alti)")
eski = """    sh = cq.importers.importStep(yol).val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0)
    b = sh.BoundingBox()
    return cq.Workplane(obj=sh.translate(cq.Vector(x0 - b.xmin, y0 - b.ymin, z0 - b.zmax)))
"""
yeni = """    # OCP bugu: cok-katili STEP Compound'ini tek hamlede dondurmek UPS'te
    # gecersiz Compound uretiyor; 18 katinin her biri tek basina gecerli. Katilari
    # ayri dondurup yeniden Compound kurunca hacim ayni ve sekil gecerli kaliyor.
    _w = cq.importers.importStep(yol).val()
    _ss = [q.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90.0) for q in _w.Solids()]
    sh = cq.Compound.makeCompound(_ss)
    b = sh.BoundingBox()
    _loc = cq.Location(cq.Vector(x0 - b.xmin, y0 - b.ymin, z0 - b.zmax))
    sh = cq.Compound.makeCompound([q.moved(_loc) for q in _ss])
    return cq.Workplane(obj=sh)
"""
s = rep(s, eski, yeni)
s = rep(s,
        "    tk = kut(-520.0, 1790.0, 1.5, 4.5, -5.0, -415.0)\n"
        "    tk = tk.union(kut(-520.0, 1790.0, 1.5, 31.5, -5.0, -8.0)).union(kut(-520.0, 1790.0, 1.5, 31.5, -412.0, -415.0))",
        "    # v22: uzayan hareketin TAMAMI tasinir; sag motor ve sol avara da ayni teknededir.\n"
        "    _TX0, _TX1 = H.KAYIS_SOL - 20.0, H.KAYIS_SAG + 50.0\n"
        "    tk = kut(_TX0, _TX1, 1.5, 4.5, -5.0, -415.0)\n"
        "    tk = tk.union(kut(_TX0, _TX1, 1.5, 31.5, -5.0, -8.0)).union(kut(_TX0, _TX1, 1.5, 31.5, -412.0, -415.0))\n"
        "    # X motoru arka taraftan takilir; teknenin arka kivriminda katalog motor zarfi kadar servis cebi.\n"
        "    tk = tk.cut(kut(H.KAYIS_SAG - 34.0, H.KAYIS_SAG + 34.0, 0.5, 33.0, -416.0, -411.0))")
s = rep(s, 'kut(-520.0, 1790.0, 4.5, 20.5, z0_, z1_)', 'kut(_TX0, _TX1, 4.5, 20.5, z0_, z1_)')
s = rep(s, '"Ray kirişi 60 × 16 × 1650"', '"Ray kirisi 60 x 16 x %.0f" % (_TX1 - _TX0)')
s = rep(s, 'kut(-520.0, 1790.0, 4.5, 20.5, -385.0, -335.0)', 'kut(_TX0, _TX1, 4.5, 20.5, -385.0, -335.0)')
s = rep(s,
        'for i_, xb in enumerate((200.0, 500.0, 800.0, 1100.0, 1400.0, 1650.0)):',
        'for i_, xb in enumerate((-520.0, -220.0, 80.0, 380.0, 680.0, 980.0, 1280.0, 1580.0, 1810.0)):')
s = rep(s, 'bom=("Bağlama laması 40 × 16", 6,', 'bom=("Baglama lamasi 40 x 16", 9,')
s = rep(s, 'hiwin_ray(-500.0, 1785.0, zc_)', 'hiwin_ray(H.RAY_X0, H.RAY_X1, zc_)')
s = rep(s, '"Lineer ray HGR15 × 1600"', '"Lineer ray HGR15 x %.0f" % H.RAY_UZUNLUK')

eski = """    # --- 8b.5 X TAHRİK ZİNCİRİ ---
    ekle("x_tahrik_kasnagi", silz(1735.0, 31.0, 9.55, -364.5, -355.5).cut(silz(1735.0, 31.0, 4.1, -366.0, -354.0)), "celik",
         bom=("GT3 kasnak 20 diş", 1, "PD 19,099 → çevre TAM 60,00 mm/tur · sıkma bilezikli (setuskur yok)", "x motorunun milinde"))
    _mg = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0).translate(cq.Vector(1735.0, 41.5, -360.0))
    ekle("x_motoru", cq.Workplane(obj=_mg), "motor",
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
"""
yeni = """    # --- 8b.5 X TAHRİK ZİNCİRİ (v22: TAM 1987 mm strok) ---
    # v21 hatasi: ray -500'e uzamisti fakat kayis x=52'de basliyordu; parkta (-350)
    # araba kayisa bagli degildi. Ayrica iki duz kosu Y yerine Z'de ayrilmisti.
    _KL, _KR, _KY, _KRAD = H.KAYIS_SOL, H.KAYIS_SAG, 33.0, H.KASNAK_R
    ekle("x_tahrik_kasnagi", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.1, -369.0, -351.0)), "celik",
         bom=("GT3 kasnak 20 dis x 15", 1, "PD %.3f -> cevre TAM %.2f mm/tur; sikma bilezikli" % (2.0 * _KRAD, H.KASNAK_CEVRE), "x motorunun milinde"))
    # Motor STEP'inin mili zaten Z ekseninde. v21'de X etrafinda 90 derece
    # cevrilince mil Y'ye bakiyor ve govde kayisin icine giriyordu.
    # Motor teknenin ARKASINDA; gercek NEMA23 mili +Z yonunde kasnaga uzanir.
    # Boylece motor govdesi ne kayis kirisine ne de urun bolgesine girer.
    _mot_yuz = -397.5
    _mg = nema23()["govde"].translate(cq.Vector(_KR, _KY, _mot_yuz))
    ekle("x_motoru", cq.Workplane(obj=_mg), "motor",
         bom=("X motoru - NEMA23 kapali cevrim step", 1, "57 x 57 x 76 - %.1f N.m - 24 V - mil asagi" % H.X_MOTOR_TORK,
               "200 mm/s = 200 dev/dk; %.2f kg hareketli kutlede gereken %.3f N.m, motor payi %.1f kat" % (H.X_HAREKET_KUTLE, H.X_GEREKEN_TORK, H.X_TORK_PAY)))
    ekle("x_motor_mili", silz(_KR, _KY, 4.0, _mot_yuz, -352.5), "celik",
         bom=("X motor mili O8", 1, "motorun katalog mili + sikma bilezigi", "kasnak gobegine kadar kesintisiz; kasnak deligi O8,2"))
    _mk = kut(_KR - 45.0, _KR + 45.0, 4.5, 75.0, _mot_yuz, _mot_yuz + 8.0).cut(silz(_KR, _KY, 20.0, _mot_yuz - 1.0, _mot_yuz + 9.0))
    ekle("x_motor_kaidesi", _mk, "sac",
         bom=("X motor kaidesi", 1, "304 8 mm dik motor plakasi - tekneye 4 x M8", "motor teknenin arkasinda; mil servis cebinden kasnaga gelir"))
    ekle("avara_kasnak", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.1, -369.0, -351.0)), "celik",
         bom=("Avara kasnak GT3 20 dis x 15", 1, "flansli - icinde 2 x 625-2RS paslanmaz rulman", "sol ucta; park arabasinin disinda"))
    # Avara plakasi kayis duzleminin arkasinda; onceki U braket iki kayis kosusunu kesiyordu.
    _agb = kut(_KL - 22.0, _KL + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KL, _KY, 4.2, -386.0, -376.0))
    ekle("avara_gergi_braketi", _agb, "celik",
         bom=("Avara + gergi braketi", 1, "304 10 mm - 16 mm yuvali 2 x M8 + M6 itme vidası + kontra", "gergi sol servis bolgesinden ayarlanir"))
    ekle("avara_mili", silz(_KL, _KY, 4.0, -385.0, -352.5), "celik",
         bom=("Avara mili O8", 1, "17-4PH - iki 625-2RS rulman", "gergi plakasindan kasnaga"))
    _bt = 1.5
    for i_, yc_ in enumerate((_KY - _KRAD - _bt / 2.0, _KY + _KRAD + _bt / 2.0)):
        ekle("x_kayisi_%d" % i_, kut(_KL, _KR, yc_ - _bt / 2.0, yc_ + _bt / 2.0, -367.5, -352.5), "koyu",
             bom=("X kayisi GT3-15 kapali cevrim %.0f mm" % H.KAYIS_UZUNLUK, 1, "celik kordlu poliuretan [V: tedarikci boyu dogrulayacak]", "iki kosu AYNI XY duzleminde; tum -350...1637 is strokunda kelepce kayis ustunde") if i_ == 0 else None)
    # Kasnak sarimlari: duz kosularin iki ucunu fiziksel olarak kapatir.
    for ad_, xx_, sol_ in (("sol", _KL, True), ("sag", _KR, False)):
        _sar = silz(xx_, _KY, _KRAD + _bt, -367.5, -352.5).cut(silz(xx_, _KY, _KRAD, -369.0, -351.0))
        _sar = _sar.intersect(kut(xx_ - 14.0 if sol_ else xx_, xx_ if sol_ else xx_ + 14.0, _KY - 14.0, _KY + 14.0, -368.0, -352.0))
        ekle("x_kayisi_sarim_" + ad_, _sar, "koyu")
    _yc = _KY + _KRAD + _bt / 2.0
    kol = kut(Xc - 150.0, Xc + 150.0, _yc + 4.5, _yc + 14.5, -385.0, -315.0).union(kut(Xc - 20.0, Xc + 20.0, _yc + _bt / 2.0 + 0.5, _yc + 4.5, -367.5, -352.5))
    ekle("kayis_kolu", kol, "celik", bom=("Kayis kolu - L", 1, "304 10 mm bukme - plakaya 4 x M8 + O6 pim", "ust kayis kosusunu araba plakasina baglar"))
    for i_, xb in enumerate((Xc - 140.0, Xc + 140.0)):
        ekle("kayis_kelepcesi_%d" % i_, kut(xb - 20.0, xb + 20.0, _yc - 4.5, _yc + 4.5, -371.0, -349.0).cut(kut(xb - 21.0, xb + 21.0, _yc - 1.0, _yc + 1.0, -368.0, -352.0)), "celik",
             bom=("Kayis kelepcesi", 2, "304 govde + GT3 dis profilli baski plakasi", "kapali kayisin ust kosusuna iki noktadan 2 x M5 + 2 x M4 ile baglanir") if i_ == 0 else None)
"""
s = rep(s, eski, yeni)

eski = """    for ad_, xb in (("home", 1520.0), ("limit_sol", 205.0), ("limit_sag", 1535.0)):
        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Endüktif sensör M12 × 50 IP69K PNP NO", 3, "ön ray kirişinin dış yüzüne L braketle", "home x 1520 (istasyon) · limit− 205 · limit+ 1535") if ad_ == "home" else None)
"""
yeni = """    for ad_, xb in (("home", H.X_PARK), ("limit_sol", H.X_LIMIT_SOL), ("limit_sag", H.X_LIMIT_SAG)):
        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Enduktif sensor M12 x 50 IP69K PNP NO", 3, "on ray kirisinin dis yuzune L braketle", "home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, H.X_LIMIT_SAG)) if ad_ == "home" else None)
"""
s = rep(s, eski, yeni)
s = rep(s, 'for i_, xb in enumerate((180.0, 1560.0)):',
        'for i_, xb in enumerate((H.X_LIMIT_SOL - 200.0, H.X_LIMIT_SAG + 200.0)):')
s = rep(s, 'for i_, zb in enumerate((BZ0 - 30.0, BZ1 + 10.0)):',
        'for i_, zb in enumerate((BZ0 - 30.0, BZ1 - 2.0)):')

# v21'de acici konileri 17,82 derece egik, fakat mil saf Z ekseninde; motor ise
# saf Y eksenindeydi. Parcalar fiziksel olarak birbirine baglanamiyordu. v22'de
# koni, mil, rulman, gercek SureGear ve gercek NEMA23 tek ortak eksendedir.
bas = "    # z bantlari: her parcanin kendi yeri var, ic ice girmiyorlar\n"
son = "    ekle(\"acici_kafa_plakasi\""
yeni = r'''
    def _birim(v_):
        l_ = v_.Length
        return cq.Vector(v_.x / l_, v_.y / l_, v_.z / l_)

    def _yonlendir(sh_, hedef_, nokta_):
        """Yerel +Z eksenini hedefe cevirir, sonra nokta_ konumuna tasir."""
        h_ = _birim(hedef_)
        z_ = cq.Vector(0.0, 0.0, 1.0)
        eks_ = z_.cross(h_)
        ac_ = _m.degrees(_m.acos(max(-1.0, min(1.0, z_.dot(h_)))))
        if eks_.Length > 1e-9:
            sh_ = sh_.rotate(cq.Vector(0, 0, 0), eks_, ac_)
        elif z_.dot(h_) < 0.0:
            sh_ = sh_.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180.0)
        return sh_.translate(nokta_)

    def _eksen_silindir(p_, u_, r_, boy_):
        return cq.Workplane(obj=cq.Solid.makeCylinder(r_, boy_, p_, u_))

    for i_, yon in enumerate((1.0, -1.0)):
        ad_ = "on" if yon > 0 else "arka"
        _k, _p1 = _koni(yon)
        _p0 = cq.Vector(AC_X, AC_TEPE, AC_Z)
        _u = _birim(_p1 - _p0)                    # koniden disariya dogru ortak eksen
        ekle("acici_konisi_" + ad_, _k, "celik",
             bom=("Acici konisi - boy 140 - taban O90", 2,
                  "304 taslanmis, mat kumlu - yari aci 17,82 derece",
                  "Tepesi tabla ekseninde; tabaninda M18 dis yuva, mil yuzden vidalanir") if i_ == 0 else None)

        # Mil koni tabaninda BASLAR: CAD'de hacim bindirmesi yok. Gercekte M18 dis ve
        # omuzla koniye sikilir; rulman ic capinda 0,15 mm radyal montaj boslugu vardir.
        _mil_boy = 54.0
        ekle("acici_mili_" + ad_, _eksen_silindir(_p1, _u, 9.0, _mil_boy), "celik",
             bom=("Acici mili O18 x 54", 2, "17-4PH taslanmis - M18 omuzlu",
                  "koni, rulman ve reduktor cikisini AYNI eksende baglar") if i_ == 0 else None)

        _py = _p1 + _u.multiply(8.0)
        _yat = cq.Solid.makeCylinder(24.0, 10.0, _py, _u).cut(
            cq.Solid.makeCylinder(9.15, 12.0, _py - _u.multiply(1.0), _u))
        ekle("acici_yatagi_" + ad_, cq.Workplane(obj=_yat), "celik",
             bom=("Acici yatagi - flansli O18", 2, "paslanmaz govde - gida gresi - O18,30 ic",
                  "koni tabaninin 8 mm disinda; mil ile radyal bosluk 0,15 mm") if i_ == 0 else None)

        # Rulman yuzune civatalanan 72 x 72 x 8 plaka + iki O7 aski cubugu TEK parca.
        # Plaka rulmana 0,5 mm montaj payiyla yaklasir; cubuklar kafa plakasinda y=250'de biter.
        _pp = _p1 + _u.multiply(18.5)
        _pl = cq.Workplane("XY").rect(72.0, 72.0).circle(9.2).extrude(8.0).val()
        _aski = _yonlendir(_pl, _u, _pp)
        _pc = _p1 + _u.multiply(22.5)
        for _sx in (-30.0, 30.0):
            _pa = _pc + cq.Vector(_sx, 0.0, 0.0)
            _pb = cq.Vector(_pa.x, 250.0, _pa.z)
            _vv = _pb - _pa
            _aski = _aski.fuse(cq.Solid.makeCylinder(3.5, _vv.Length, _pa, _birim(_vv)))
        ekle("acici_askisi_" + ad_, cq.Workplane(obj=_aski), "celik",
             bom=("Acici yatak askisi", 2, "304 - 72 x 72 x 8 plaka + 2 x O7 gergi",
                  "rulman flansi 4 x M8; gergiler kafa plakasina M8 somunla") if i_ == 0 else None)

        # SureGear'in yerel +Z'si cikis yonudur, govdesi -Z'ye uzar. Govdenin koniden
        # DISARI uzamasi icin yerel +Z = -u yapilir. Motor da ayni kuralla girise oturur.
        _q_red = _p1 + _u.multiply(_mil_boy)
        _red = _yonlendir(suregear()["tum"], _u.multiply(-1.0), _q_red)
        ekle("acici_reduktoru_" + ad_, cq.Workplane(obj=_red), "motor",
             bom=("Acici reduktoru - planet i=5", 2, "SureGear PGCN23-1025 GERCEK CAD",
                  "cikis yuzu mile temas eder; eksen koniyle birebir aynidir") if i_ == 0 else None)
        _q_mot = _q_red + _u.multiply(79.0)
        _mot = _yonlendir(nema23()["govde"], _u.multiply(-1.0), _q_mot)
        ekle("acici_motoru_" + ad_, cq.Workplane(obj=_mot), "motor",
             bom=("Acici motoru - NEMA23 STP-MTR-23079", 2, "1,95 N.m - 2,8 A - GERCEK CAD",
                  "iki koni ters yonde doner; motor-reduktor-koni tek eksendedir") if i_ == 0 else None)

'''
s = blok(s, bas, son, yeni)

# Firin aktarma bandinda v21 yan saclari dolu plakaydi ve roller/bant plakalarin
# icinden geciyordu. Roller artik tam bant genisliginde, mil uzantilari ince;
# iki yan sac banttan disarida ve rulman deliklidir.
bas = "    # ---- FIRIN BANDI · BICAK BURUNLU AKTARMA (v21) ----\n"
son = "    _bm = nema23()[\"govde\"].rotate"
yeni = r'''    BR_R, BT_R, BANT_K = 10.0, 30.0, 1.5
    BR_Y = AKT_Y - BANT_K - BR_R
    BT_Y = AKT_Y - BANT_K - BT_R
    BZ0, BZ1 = AKT_Z0, AKT_Z1
    _burun = silz(AKT_X0, BR_Y, BR_R, BZ0, BZ1).union(silz(AKT_X0, BR_Y, 6.0, BZ0 - 35.0, BZ1 + 35.0))
    ekle("bant_burun_silindiri", _burun, "celik",
         bom=("Bant burun silindiri O20 x 290 + O12 mil", 1, "304 - iki ucta flansli rulman",
               "bicak burun; bant yuzeyi tablanin kenarina 8 mm kala baslar"))
    _tahrik = silz(AKT_X1, BT_Y, BT_R, BZ0, BZ1).union(silz(AKT_X1, BT_Y, 10.0, BZ0 - 35.0, BZ1 + 35.0))
    ekle("bant_tahrik_silindiri", _tahrik, "celik",
         bom=("Bant tahrik silindiri O60 x 290 + O20 mil", 1, "304 - kaucuk kapli",
               "bandi ceker; devri firindaki pisirme suresini belirler"))
    _dis = (silz(AKT_X0, BR_Y, BR_R + BANT_K, BZ0, BZ1)
            .union(silz(AKT_X1, BT_Y, BT_R + BANT_K, BZ0, BZ1))
            .union(kut(AKT_X0, AKT_X1, AKT_Y - BANT_K, AKT_Y, BZ0, BZ1))
            .union(cq.Workplane("XY").polyline([(AKT_X0, BR_Y - BR_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R),
                                                (AKT_X0, BR_Y - BR_R)]).close()
              .extrude(BZ1 - BZ0).translate((0.0, 0.0, BZ0))))
    _ic = (silz(AKT_X0, BR_Y, BR_R, BZ0 - 1.0, BZ1 + 1.0)
           .union(silz(AKT_X1, BT_Y, BT_R, BZ0 - 1.0, BZ1 + 1.0))
           .union(kut(AKT_X0, AKT_X1, BR_Y - BR_R, AKT_Y - BANT_K, BZ0 - 1.0, BZ1 + 1.0)))
    ekle("bant", _dis.cut(_ic), "koyu",
         bom=("Firin bandi - 290 genis - kapali cevrim", 1,
               "gida onayli PTFE kapli cam elyaf orgu - 1,5 mm",
               "ust kosu y 106; calisma diskinin 2 mm altinda"))
    ekle("bant_tasiyici_saci", kut(AKT_X0 + 20.0, AKT_X1 - 40.0, AKT_Y - BANT_K - 4.0,
                                   AKT_Y - BANT_K - 1.0, BZ0 + 5.0, BZ1 - 5.0), "sac",
         bom=("Bant tasiyici saci", 1, "304 3 mm - ustu taslanmis", "ust kosu yuk altinda sarkmasin"))
    for i_, (z0_, z1_) in enumerate(((BZ0 - 35.0, BZ0 - 25.0), (BZ1 + 25.0, BZ1 + 35.0))):
        _ys = kut(1802.0, AKT_X1 + 45.0, 21.0, AKT_Y + 18.0, z0_, z1_)
        _ys = _ys.cut(silz(AKT_X0, BR_Y, 6.2, z0_ - 1.0, z1_ + 1.0))
        _ys = _ys.cut(silz(AKT_X1, BT_Y, 10.2, z0_ - 1.0, z1_ + 1.0))
        ekle("bant_yan_saci_%d" % i_, _ys, "sac",
             bom=("Bant yan saci", 2, "304 10 mm - lazer - iki rulman yuvasi",
                  "bant genisliginin disinda; roller yalniz mil ucuyla deliklerden gecer") if i_ == 0 else None)
'''
s = blok(s, bas, son, yeni)
s = rep(s,
        '("_bom_strok", "Strok ve istasyon", 1, "—", "tabla merkezi x 220…1520 (1300 mm) · istasyon SAĞDA x 1520 · dozajda %.1f mm/s, geçişte %.0f mm/s" % (TB["x_doz_hiz"], TB["x_gecis_hiz"])),',
        '("_bom_strok", "Strok ve istasyon", 1, "-", "tabla merkezi x %.0f...%.0f (%.0f mm) - park SOLDA - dozajda %.1f mm/s, geciste %.0f mm/s" % (H.X_PARK, H.X_AKTARMA, H.X_STROK, TB["x_doz_hiz"], TB["x_gecis_hiz"])),')
s = rep(s,
        '("_bom_cevrim", "Çevrim", 1, "—", "altı doz 71,0 s → 51 tepsi/h · tipik tek dozlu kaşarlı pide 13,7 s → 262 tepsi/h"),',
        '("_bom_cevrim", "Cevrim", 1, "-", "uzayan strok dahil sure receteye gore sim_makine_v6 tarafindan hesaplanir; doz yasasi 10 s / urun DEGISTIRILMEDI"),')

eski = """    tas = [a for a, b in bb if b.xmin < -0.01 or b.xmax > W + 0.01 or b.ymin < -0.01 or b.ymax > Y + 0.01 or b.zmax > 0.01 or b.zmin < -D - 0.01]
    print("ZARF: %s (%.0f × %.0f × %.0f)" % ("hepsi modulun icinde" if not tas else "TASAN: " + ", ".join(tas), W, Y, D)); assert not tas
"""
yeni = """    # v22: istasyon artik soldaki aciciyi ve sagdaki firin aktarimini da kapsiyor.
    # Ana soguk govde hala 0..W; hareket altyapisi ve transfer elemanlari kontrollu uzantidir.
    _zx0, _zx1 = min(H.KAYIS_SOL - 20.0, H.X_LIMIT_SOL - 220.0), 2245.0
    # Acici motor/kafa paketi ve bant motoru soguk govdenin ONUNE tasar; bu kontrollu
    # servis uzantisi +310 mm ile sinirli. Ana soguk govdenin derinligi degismedi.
    _z_on = 310.0
    tas = [a for a, b in bb if b.xmin < _zx0 - 0.01 or b.xmax > _zx1 + 0.01 or b.ymin < -0.01 or b.ymax > Y + 0.01 or b.zmax > _z_on + 0.01 or b.zmin < -D - 0.01]
    _xmin, _xmax = min(b.xmin for _, b in bb), max(b.xmax for _, b in bb)
    _ymax = max(b.ymax for _, b in bb)
    _zmin, _zmax = min(b.zmin for _, b in bb), max(b.zmax for _, b in bb)
    print("ISTASYON ZARFI: %s (x %.0f...%.0f, y 0...%.0f, z %.0f...%.0f)" % ("GECTI" if not tas else "TASAN: " + ", ".join(tas), _xmin, _xmax, _ymax, _zmin, _zmax)); assert not tas
"""
s = rep(s, eski, yeni)
s = s.replace("TOPPING_MODUL_v1", "TOPPING_MODUL_v22")
s = s.replace("TOPPING MODULU v10", "TOPPING MODULU v22")
yaz("topping_cad_v22.py", s)


# ---------------------------------------------------------------- SIM TANIMI v6
s = oku("sim_makine_v5.py")
s = rep(s, "import topping_cad_v21 as TC", "import topping_cad_v22 as TC")
s = rep(s, "import topping_hesap_v5 as H", "import topping_hesap_v6 as H")
s = rep(s,
        "                   strok=[-350.0, 1637.0], istasyon_x=-350.0, acici_x=-350.0, aktarma_x=1637.0,",
        "                   strok=[H.X_PARK, H.X_AKTARMA], istasyon_x=H.X_PARK, acici_x=H.X_PARK, aktarma_x=H.X_AKTARMA,")
s = rep(s, "cozunurluk_mm=0.01875, home_x=-350.0, limit=[-380.0, 1660.0])",
        "cozunurluk_mm=0.01875, home_x=H.X_PARK, limit=[H.X_LIMIT_SOL, H.X_LIMIT_SAG])")
s = rep(s, "acici=dict(x=-350.0,", "acici=dict(x=H.X_PARK,")
s = rep(s, "aktarma=dict(x=1637.0,", "aktarma=dict(x=H.X_AKTARMA,")
s = rep(s, "        yuvalar=yuvalar,\n", "        yuvalar=yuvalar,\n        hareket=H.S[\"x_tahrik\"],\n")
yaz("sim_makine_v6.py", s)


# ---------------------------------------------------------------- ANA MONTAJ v34
s = oku("hat_montaj_v33.py")
s = rep(s, "hat_v33.glb", "hat_v34.glb", adet=3)
s = rep(s, "hat_v33.usdz", "hat_v34.usdz", adet=2)
s = rep(s, '"hat_v33"', '"hat_v34"')
s = rep(s, "HAT_v33_YERLESIM.step", "HAT_v34_YERLESIM.step", adet=3)
s = rep(s, "import topping_hesap_v5 as TH, topping_cad_v21 as TC", "import topping_hesap_v6 as TH, topping_cad_v22 as TC")
s = rep(s, '"topping_cad_v1.py"', '"topping_cad_v22.py"')
yaz("hat_montaj_v34.py", s)

print("ENTEGRASYON KAYNAKLARI HAZIR")
