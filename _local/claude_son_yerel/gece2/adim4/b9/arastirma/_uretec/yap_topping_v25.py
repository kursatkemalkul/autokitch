# -*- coding: utf-8 -*-
"""topping_cad_v24 → topping_cad_v25 (28 Eyl 2026 gece) · ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63.md §1 + §2.3)
Kemal: "fırının ön yüzü sınır yüzey … her istasyona ön yüzey ekle … önden tertemiz düz yüzeyler … içeride havada kalan parça olmasın … robotun gireceği yerlerde boşluk".
  · dış kabuk (taban, tavan, yan saclar) ön kenarı 0 → +39 (kapak arkası) · yan saclarda 30 mm ön dönüş (+37,5…+39: çerçeve ve kapak bunlara basar) ·
    yan kesikler z −510…+5 · sol yan sacta açıcı hattı rakorları (2 × Ø12), sağ yan sacta ana hat rakoru dünya y 1809 / z −432 (montaj ANA_V44 ile aynı; v24'te 23 mm kaçıktı)
  · ön çerçeve 30 × 20 × 2 (z +39…+59) + tava paneller (z +59…+79): mekanizma bandı 2 kanat (791–1107,5, kaide bandını örter) + teknik cep kapağı T
    (lazer yarık: giriş sol-alt, çıkış sağ-üst) · gizli menteşe + bas-aç · soğuk kapaklar K1/K2 + 430 çerçeve + fitil + flipper → topping_uno_cad_v14
  · AÇICI KAFASI: ön tahrik DİK AÇILI (Motovario NMRV030 sonsuz vida, i 7,5, Ø14 delik mil + NEMA23 dik) · ayrı ön yatak yok (redüktör yatakları) ·
    kafa plakası ön ucu +10 · hiçbir açıcı parçası +39'u geçmez · Z ekseni: kolon önünde 2 HGR15 ray + 4 HGH15CA araba + adaptör plaka ·
    pnömatik Festo DSBC-32-100 (ISO 15552, strok 100) kolonun üst kolundan dik asılı · koniler (kinematik) v24 ile birebir
  · havada kalanlar bağlandı: teknik cep parçaları tabana + DIN plakası, sürücüler DIN ray + ayak (kuru bölme), evaporatör 4 ayak + fan evaporatöre,
    kasnak/avara delikleri, tampon plakası, lokma, ray örtüsü çatısı (kirişe oturur), enerji zinciri kanalı tabana, sensör braketleri, bayrak kolu,
    fire sileceği (SMC CJ2B10-20 + 2 kılavuz, alt yalıtıma asılı), tabla boş sensörü braketi
  · eski menteşeler (mentese_*), ağız alt dudağı silindi · V1_TASI ile montajda kayan parçalar yeni adlarla SON yerlerinde (montaj sözlüğü etkisiz kalır)
  · denetim: ön düzlem ≤ +79,5 (istisna yok) · açıcı ≤ +39 · kafa ≤ +10 · DÜNYA DENETİMİ (TU v14 + TC v25 + itici): havada 0, çakışma 0, kaset çekme 0–630,
    kafa +60/+90/+100, ön yüz kapsama + derz 3, kinematik = v24
Önceki: topping_cad_v24.py. Çalıştır: python yap_topping_v25.py [çıkış_adı.py]
"""
import io, os, sys
U = os.path.dirname(os.path.abspath(__file__))
CIKIS = sys.argv[1] if len(sys.argv) > 1 else "topping_cad_v25.py"
s = io.open(os.path.join(U, "topping_cad_v24.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def bolum(bas, son, yeni):
    global s
    assert s.count(bas) == 1, ("bas", s.count(bas), bas[:100])
    i = s.index(bas); j = s.index(son, i)
    s = s[:i] + yeni + s[j + len(son):]


# ---------------------------------------------------------------- 0 · başlık
d('"""v24 (26 Eyl 2026 gece): TOPPING TEKNESİ MODÜL İÇİNDE BİTER',
  '"""v25 (28 Eyl 2026 gece): ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.3) — kabuk ön kenarı +39 + ön dönüş · ön çerçeve + tava paneller (mekanizma 2 kanat,\n'
  '  teknik cep T) · AÇICI ön tahriki DİK AÇILI NMRV030, kafa ön ucu +10, açıcı ≤ +39, Z ekseni ray + araba + adaptör, pnömatik DSBC-32-100 dik asılı ·\n'
  '  havada parçalar bağlandı · montaj V1_TASI kaydırmaları yeni adlarla son yerinde · dünya denetimi (TU v14 + itici). Önceki: topping_cad_v24.py (yap_topping_v25.py)\n'
  'v24 (26 Eyl 2026 gece): TOPPING TEKNESİ MODÜL İÇİNDE BİTER')

# ---------------------------------------------------------------- 1 · sabitler + yardımcılar
d('XK_SOL, XK_SAG = -560.0, 1650.0   # v24: X kayışı kasnak merkezleri (motor SOLDA, avara SAĞDA) — H.KAYIS_SOL/SAG yerine',
  '''XK_SOL, XK_SAG = -560.0, 1650.0   # v24: X kayışı kasnak merkezleri (motor SOLDA, avara SAĞDA) — H.KAYIS_SOL/SAG yerine
# ---- v25 · ÖN DÜZLEM (SPEC_on_duzlem_v63) ----
Z_ON = 79.0                        # ön düzlem = fırın ön yüzü (montaj sözleşmesi Z_ON = FT.ZS)
Z_KABUK = 39.0                     # dış kabuk (taban, tavan, yan saclar) ön kenarı = soğuk kapak arkası
Z_CER_C = (39.0, 59.0)             # C ön çerçevesi 30 × 20 × 2 (tava panellerin arkası)
Z_PAN_C = (59.0, 79.0)             # tava panel: yüz 1,5 (+77,5…+79) + 20 dönüş
DERZ = 3.0
DX_D, DY_D = 700.0, 892.0          # TC yerel → dünya (montaj: x + 700 · y + 892)
TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v14.py")        # dünya denetiminde soğuk paket (montaj: spec_from_file_location, bir kez −168)
ITICI_MOD = os.environ.get("TOPPING_ITICI", "itici_cad_v5")
RAKOR_ACICI = ((1472.0 - 892.0, -700.0), (1460.0 - 892.0, -712.0))       # sol yan sac · açıcı hattı 2 × Ø6 (TU v14 hava_hatti_acici_D6_1/2)
RAKOR_ANA = (1809.0 - 892.0, -432.0)                                      # sağ yan sac · montaj ANA_V44 (dünya y 1809, z −432)


def boru_y(x0, x1, z0, z1, y0, y1, t=2.0):
    """v25 · y boyunca kutu profil (uçları açık)"""
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))


def boru_x(y0, y1, z0, z1, x0, x1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def boru_z(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, min(z0, z1) - 1.0, max(z0, z1) + 1.0))


def omega_pz(x0, x1, yc, zt, yon, h=15.0, t=1.0):
    """v25 · x boyunca omega takviye 40 (10 + 20 + 10) · flanşlar z = zt yüzeyine oturur, tepe yon yönünde h (acici_kabin_cad_v1 ile aynı)"""
    lo = lambda a, b: (min(a, b), max(a, b))
    za, zb = zt, zt + yon * h
    w = kut(x0, x1, yc - 20.0, yc - 10.0, *lo(zt, zt + yon * t)).union(kut(x0, x1, yc + 10.0, yc + 20.0, *lo(zt, zt + yon * t)))
    w = w.union(kut(x0, x1, yc - 10.0, yc - 10.0 + t, *lo(za, zb))).union(kut(x0, x1, yc + 10.0 - t, yc + 10.0, *lo(za, zb)))
    return w.union(kut(x0, x1, yc - 10.0, yc + 10.0, *lo(zb, zb - yon * t)))


def tava(x0, x1, y0, y1, yariklar=()):
    """v25 · tava panel: yüz 304 fırçalı 1,5 (z +77,5…+79) + 4 kenar 20 arkaya bükülü (z +59…+77,5) · yariklar: (x0, x1, y0, y1) lazer kesik"""
    zy = Z_ON - 1.5
    w = kut(x0, x1, y0, y1, zy, Z_ON)
    for a, b, c, e in ((x0, x0 + 1.5, y0, y1), (x1 - 1.5, x1, y0, y1), (x0, x1, y0, y0 + 1.5), (x0, x1, y1 - 1.5, y1)):
        w = w.union(kut(a, b, c, e, Z_PAN_C[0], zy))
    for a, b, c, e in yariklar:
        w = w.cut(kut(a, b, c, e, zy - 1.0, Z_ON + 1.0))
    return w''')

# ---------------------------------------------------------------- 2 · dış kabuk +39 · ön dönüş · yan kesik +5 · rakorlar
d('    ekle("dis_taban", kut(0, W, 0, SAC, 0, -D), "sac",', '    ekle("dis_taban", kut(0, W, 0, SAC, Z_KABUK, -D), "sac",')
d('    ekle("dis_tavan", kut(0, W, Y - SAC, Y, 0, -D), "sac",', '    ekle("dis_tavan", kut(0, W, Y - SAC, Y, Z_KABUK, -D), "sac",')
d('        _ys = kut(x, x + SAC, SAC, Y - SAC, 0, -D)',
  '        _ys = kut(x, x + SAC, SAC, Y - SAC, Z_KABUK, -D)                          # v25: ön kenar +39 (kapak arkası)\n'
  '        _xd = (SAC, SAC + 30.0) if s == "sol" else (W - SAC - 30.0, W - SAC)\n'
  '        _ys = _ys.union(kut(_xd[0], _xd[1], SAC, Y - SAC, Z_KABUK - SAC, Z_KABUK))   # v25: 30 mm ön dönüş (içe) — çerçeve + soğuk kapak buna basar, menteşe buna')
d("        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 150.0, -510.0, 0.0))   # v23: 132 → 150 (en yüksek ürün diskte 136,5)",
  "        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 150.0, -510.0, 5.0))   # v23: 132 → 150 (en yüksek ürün diskte 136,5) · v25: öne +5 (disk z 0'a kadar)")
d('            _ys = _ys.cut(silx(940.0, -415.0, 7.0, x - 1.0, x + SAC + 1.0))     # v24: hava ana hattı rakoru Ø14 (kompresör fırın üstünde)',
  '            _ys = _ys.cut(silx(RAKOR_ANA[0], RAKOR_ANA[1], 7.0, x - 1.0, x + SAC + 1.0))   # v25: ana hat rakoru Ø14 montaj hattıyla aynı eksende (dünya y 1809 · z −432; v24 y 1832 · z −415)\n'
  '        else:\n'
  '            for _ry, _rz in RAKOR_ACICI:\n'
  '                _ys = _ys.cut(silx(_ry, _rz, 6.0, x - 1.0, x + SAC + 1.0))       # v25: açıcı hattı rakorları Ø12 (2 × Ø6 hortum)')
d('    ekle("dis_arka", kut(SAC, W - SAC, SAC, Y - SAC, -D, -D + SAC), "sac", bom=("Dış arka sac", 1, "304 1,5 mm", "kuru bölmenin arkası; kablo rakorları burada"))',
  '''    ekle("dis_arka", kut(SAC, W - SAC, SAC, Y - SAC, -D, -D + SAC), "sac", bom=("Dış arka sac", 1, "304 1,5 mm", "kuru bölmenin arkası; kablo rakorları burada"))
    # v25 · RAKORLAR (hortum çapında iç delik, yan sacın deliğine oturur): açıcı hattı 2 × (sol) + ana hat (sağ)
    for _i, (_ry, _rz) in enumerate(RAKOR_ACICI):
        ekle("rakor_hava_acici_%d" % _i, silx(_ry, _rz, 6.0, -1.5, SAC + 1.5).cut(silx(_ry, _rz, 3.0, -2.0, SAC + 2.0)), "koyu",
             bom=("Duvar geçiş rakoru Ø6 · SMC KQ2E06-00A (bulkhead)", 2, "sol yan sacta · somunlu", "açıcı Z silindirinin 2 hattı (valf adası → A)") if _i == 0 else None)
    ekle("rakor_hava_ana", silx(RAKOR_ANA[0], RAKOR_ANA[1], 7.0, W - SAC - 1.5, W).cut(silx(RAKOR_ANA[0], RAKOR_ANA[1], 5.0, W - SAC - 2.0, W + 1.0)), "koyu",
         bom=("Duvar geçiş rakoru Ø10 · SMC KQ2E10-00A (bulkhead)", 1, "sağ yan sacta · dışı x 2500'ü geçmez", "ana hat fırın üstünden TOPPING teknik cebine (montaj ANA_V44)"))''')

# ---------------------------------------------------------------- 3 · eski menteşeler
d('''    for i, xx in enumerate((110.0, W - 140.0)):
        ekle("mentese_%d" % i, kut(xx, xx + 30.0, KAS[0] - 30.0, KAS[0] - 26.0, ZKAP[0] - 4.0, ZKAP[1] + 2.0), "celik",
             bom=("Menteşe", 2, "paslanmaz, gömme", "kapak alttan menteşeli: açılınca tezgâh gibi öne yatar") if i == 0 else None)''',
  '''    # v25: eski kapak menteşeleri (mentese_0/1) SİLİNDİ — montajda havada görünüyorlardı (SPEC §2.3). Soğuk kapaklar topping_uno_cad_v14'te.''')

# ---------------------------------------------------------------- 4 · soğutma: fan evaporatöre, evaporatör 4 ayak
d('    ekle("fan_0", silz(W / 2.0, (EVY[0] + EVY[1]) / 2.0, 100.0, EVZ[1] - 3.0, EVZ[1] - 53.0), "motor",',
  '    ekle("fan_0", silz(W / 2.0, (EVY[0] + EVY[1]) / 2.0, 100.0, EVZ[1], EVZ[1] - 50.0), "motor",   # v25: fan evaporatöre oturur (v24: 3 mm boşluk)')
d('''    # Arka yalıtımdaki (pu_arka + iç kabuk arka yüzü) İKİ BOŞLUK: üstte üfleme, altta dönüş.''',
  '''    for _i, (_xa, _ya) in enumerate(((EVX[0], EVY[0]), (EVX[1] - 30.0, EVY[0]), (EVX[0], EVY[1] - 30.0), (EVX[1] - 30.0, EVY[1] - 30.0))):
        ekle("evaporator_ayagi_%d" % _i, boru_z(_xa, _xa + 30.0, _ya, _ya + 30.0, -D + SAC, EVZ[1]), "celik",
             bom=("Evaporatör ayağı 30 × 30 × 2 AISI 304", 4, "boy %.1f · arka saca 2 × M6 kaynak saplama, evaporatör köşe flanşına M6" % (EVZ[1] + D - SAC),
                  "v25 · evaporatör (dünya x 1400–1800) v24'te havadaydı · soğuk hava TU v14 arka bölmedeki iki ağızdan (üfleme 1640–1685 · dönüş 1570–1610, TU y)") if _i == 0 else None)
    # Arka yalıtımdaki (pu_arka + iç kabuk arka yüzü) İKİ BOŞLUK: üstte üfleme, altta dönüş.''')

# ---------------------------------------------------------------- 5 · teknik cep + sürücüler: tabana / DIN raya (montaj V1_TASI kaymaları son yerlerinde, yeni adlar)
bolum('    ekle("sogutma_grubu", kut(60.0, 360.0, TEK[0] + 6.0, TEK[0] + 226.0, -60.0, -280.0), "motor",',
      '"her mile bir sürücü: 6 kaset × 2; motor 2,8 A, sürücü 3,0 A (GERÇEK CAD)") if i == 0 else None)',
      '''    # v25 · TEKNİK CEP (dünya x 1520–2498,5 · y 1553,5–1860,5): parçalar TU v14 teknik ayırma sacının ÜSTÜNE oturur (dünya 1553,5 = yerel 661,5).
    #       v24'te y 1604'te havadaydılar ve montaj bunları V1_TASI ile x'te kaydırıyordu → v25: yeni adlarla SON yerlerinde (montaj sözlüğü etkisiz)
    TEK_TABAN = 1553.5 - DY_D
    ekle("teknik_sogutma_grubu", kut(850.0, 1150.0, TEK_TABAN, TEK_TABAN + 220.0, -60.0, -280.0), "motor",
         bom=("Soğutma grubu ⅕ HP · YAPTIRILACAK", 1, "hermetik, hava soğutmalı · soğutmacı firma kurar",
              "teknik cepte, teknik ayırma sacının üstünde; önden T kapağının lazer yarıklarından emer (sol-alt), sağ-üstten atar. RAFTAN ALINAN PARÇA DEĞİL: "
              "modelde YER ZARFI, kesin marka/model firma seçince belli olacak (300 × 220 × 220)"))
    _pd = kut(1180.0, 1580.0, TEK_TABAN, TEK_TABAN + 240.0, -40.0, -290.0)
    _pi = kut(1181.5, 1578.5, TEK_TABAN + 1.5, TEK_TABAN + 238.5, -41.5, -288.5)
    ekle("teknik_pano_kutusu", _pd.cut(_pi), "sac",
         bom=("TOPPING panosu", 1, "304 · önden kapaklı, IP54", "PLC giriş/çıkış + röleler + sürücü beslemesi · teknik cep tabanına 4 × M6"))
    ekle("teknik_ups", din_parca(UPS_STEP, 1660.0, TEK_TABAN, -40.0), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1,
              "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur; teknik cep tabanında, DIN rayında"))
    ekle("teknik_guc_kaynagi", din_parca(GUC_STEP, 1592.0, TEK_TABAN, -40.0), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1,
              "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W" % H.S["elektrik"]["guc_kaynagi_W"]))
    ekle("teknik_din_rayi_ups", kut(1656.0, 1797.0, TEK_TABAN + 10.0, TEK_TABAN + 45.0, -178.0, -170.5), "sac",
         bom=("DIN ray TS35 × 7,5 · UPS", 1, "EN 60715 · 141 mm", "v25 · dünya x 2356–2497 (v24 2340–2520: sağ yan sacı delip fırın bölgesine 20 mm taşıyordu)"))
    ekle("teknik_din_rayi_guc", kut(1590.0, 1654.0, TEK_TABAN + 10.0, TEK_TABAN + 45.0, -178.0, -162.8), "sac",
         bom=("DIN ray TS35 × 7,5 + 7,7 mm ara parça · güç kaynağı", 1, "EN 60715 · 64 mm", "güç kaynağı UPS'ten 7,7 mm sığ → ray ara parçayla öne alınır"))
    ekle("teknik_din_plakasi", kut(1588.0, 1797.0, TEK_TABAN, TEK_TABAN + 110.0, -180.0, -178.0), "sac",
         bom=("DIN montaj plakası 304 2 mm", 1, "209 × 110 · teknik cep tabanına L büküm + 2 × M6", "UPS + güç kaynağı raylarını taşır"))
    # v25 · KURU BÖLME SÜRÜCÜLERİ (4 kaset tahriki: kaşar + sucuk × 2 mil) · STP-DRV-4830 · DIN rayında, ray 2 ayakla arka saca
    _drv = cq.importers.importStep(SURUCU_STEP).val()
    _drv = _drv.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90.0)
    _db = _drv.BoundingBox()
    HATVE = 33.0
    SUR_Y, SUR_Z = 1432.0 - DY_D, -760.0                                       # dünya y 1432 (valf adasının sağı) · arka yüz = DIN ray yüzü z −760
    for i in range(4):
        xx = 480.0 + i * HATVE
        _d = _drv.translate(cq.Vector(xx - _db.xmin, SUR_Y - _db.ymin, SUR_Z - _db.zmin))
        ekle("kuru_surucu_%d" % i, cq.Workplane(obj=_d), "kart",
             bom=("Step sürücü · STP-DRV-4830", 4, "3 A/faz · 12-48 VDC · mikroadım · DIN ray",
                  "kaşar + sucuk kasetlerinin 4 mili (2 × helezon + 2 × rotor) · motor 2,8 A, sürücü 3,0 A (GERÇEK CAD) · UNO'lar pnömatik") if i == 0 else None)
    ekle("kuru_din_rayi_surucu", kut(470.0, 617.0, SUR_Y + 5.0, SUR_Y + 40.0, SUR_Z - 7.5, SUR_Z), "sac",
         bom=("DIN ray TS35 × 7,5 · sürücüler", 1, "EN 60715 · 147 mm", "kuru bölmede, dünya x 1170–1317"))
    for _i, _x0 in enumerate((478.0, 579.0)):
        ekle("kuru_din_rayi_ayak_%d" % _i, boru_z(_x0, _x0 + 30.0, SUR_Y + 7.5, SUR_Y + 37.5, -D + SAC, SUR_Z - 7.5), "celik",
             bom=("DIN ray ayağı 30 × 30 × 2 AISI 304", 2, "boy 61 · arka saca kaynak saplama", "v25 · sürücüler v24'te havadaydı") if _i == 0 else None)''')

# ---------------------------------------------------------------- 6 · 8b düzeltmeleri (temas)
d('    lk = sily(Xc, ZT, 15.0, 46.0, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))',
  '    lk = sily(Xc, ZT, 15.0, 45.5, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))   # v25: motor mil yüzüne oturur (v24 0,5 boşluk)')
d('    ekle("x_tahrik_kasnagi", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.1, -369.0, -351.0)), "celik",',
  '    ekle("x_tahrik_kasnagi", silz(_KL, _KY, _KRAD, -367.5, -352.5).cut(silz(_KL, _KY, 4.0, -369.0, -351.0)), "celik",   # v25: sıkma bilezikli → delik = mil')
d('    ekle("avara_kasnak", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.1, -369.0, -351.0)), "celik",',
  '    ekle("avara_kasnak", silz(_KR, _KY, _KRAD, -367.5, -352.5).cut(silz(_KR, _KY, 4.0, -369.0, -351.0)), "celik",   # v25: rulman iç bileziği mile sıkı')
d('    _agb = kut(_KR - 22.0, _KR + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KR, _KY, 4.2, -386.0, -376.0))',
  '    _agb = kut(_KR - 22.0, _KR + 22.0, 20.5, 50.0, -385.0, -377.0).cut(silz(_KR, _KY, 4.0, -386.0, -376.0))   # v25: mil brakete sıkı (M8 gergi)')
d('''        ct = kut(-520.0, 1790.0, 20.5, 44.0, zc_ - 37.0, zc_ + 37.0).cut(kut(-525.0, 1795.0, 19.5, 45.0, zc_ - 33.0, zc_ + 33.0))''',
  '''        ct = kut(-520.0, 1790.0, 20.5, 44.0, zc_ - 30.0, zc_ + 30.0).cut(kut(-525.0, 1795.0, 19.5, 43.0, zc_ - 29.0, zc_ + 29.0))   # v25: etekler kirişin üstüne oturur (v24: 3 mm dışında, havada; çatısı yoktu)
        ct = ct.cut(kut(-525.0, 1795.0, 42.0, 45.0, zc_ - 18.0, zc_ + 18.0))                                                            # çatıda 36 yarık (araba geçer)''')
d('    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, 4.5, 64.5, -500.0, -440.0).cut(kut(-517.0, 1787.0, 6.5, 65.5, -497.0, -443.0)), "sac",',
  '    ekle("enerji_zinciri_kanali", kut(-520.0, 1790.0, SAC, SAC + 60.0, -500.0, -440.0).cut(kut(-517.0, 1787.0, SAC + 2.0, SAC + 61.0, -497.0, -443.0)), "sac",   # v25: tabana oturur (v24: 3 mm havada)')
d('''        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Enduktif sensor M12 x 50 IP69K PNP NO", 3, "on ray kirisinin dis yuzune L braketle", "home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1647.0)) if ad_ == "home" else None)''',
  '''        ekle("x_%s_sensoru" % ad_, silz(xb, 28.0, 6.0, -25.0, -19.0), "koyu",
             bom=("Enduktif sensor M12 x 50 IP69K PNP NO", 3, "on ray kirisinin dis yuzune L braketle", "home %.0f - limit- %.0f - limit+ %.0f" % (H.X_PARK, H.X_LIMIT_SOL, 1647.0)) if ad_ == "home" else None)
        ekle("x_%s_sensor_braketi" % ad_, kut(xb - 8.0, xb + 8.0, 16.0, 22.0, -35.0, -19.0), "celik",
             bom=("Sensör braketi 304 3 mm · M12 kelepçeli", 3, "ön ray kirişinin ön yüzüne 2 × M4", "v25 · sensörler v24'te kirişin 10 mm önünde havadaydı") if ad_ == "home" else None)''')
d('    ekle("x_bayragi", kut(Xc - 30.0, Xc + 30.0, 40.0, 48.5, -24.0, -6.0), "sac",',
  '    ekle("x_bayragi", kut(Xc - 30.0, Xc + 30.0, 40.0, 48.5, -30.0, -6.0), "sac",   # v25: plakanın altına 5 mm girer (kaynak) — v24: 1 mm önündeydi')
d('''    ekle("tabla_home_bayragi", sily(Xc, ZT - 128.0, 10.0, 86.0, 89.0), "celik",''',
  '''    ekle("araba_plakasi_sensor_braketi", kut(Xc - 6.0, Xc + 6.0, 60.5, 66.5, ZT - 134.0, ZT - 122.0), "celik",
         bom=("Tabla home sensör ayağı 304", 1, "12 × 6 × 12 · apron + plakaya M4", "v25 · sensör v24'te apronun 6 mm üstünde havadaydı"))
    ekle("tabla_home_bayragi", sily(Xc, ZT - 128.0, 10.0, 85.0, 89.0).union(kut(Xc - 5.0, Xc + 5.0, 80.77, 85.0, ZT - 138.0, ZT - 105.0)), "celik",   # v25: bileziğe kaynaklı kol (göbeğin 1 mm altında)''')
d('''    ekle("uc_tamponu_0", silz(H.X_LIMIT_SOL - 200.0, 53.5, 10.0, -80.0, -65.0), "silikon",
         bom=("Uç tamponu Ø20 × 15 (sol)", 1, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil"))''',
  '''    ekle("uc_tamponu_0", silz(H.X_LIMIT_SOL - 200.0, 53.5, 10.0, -80.0, -65.0), "silikon",
         bom=("Uç tamponu Ø20 × 15 (sol)", 1, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil"))
    ekle("uc_tamponu_0_braketi", kut(H.X_LIMIT_SOL - 210.0, H.X_LIMIT_SOL - 190.0, 20.5, 43.5, -82.0, -63.0), "celik",
         bom=("Uç tamponu braketi 304", 1, "20 × 23 × 19 · ön ray kirişinin üstüne 2 × M5", "v25 · tampon v24'te havadaydı"))''')
d('    ekle("uc_tamponu_plakasi", kut(1629.0, 1632.0, 45.0, 62.0, -376.0, -366.0), "celik",',
  '    ekle("uc_tamponu_plakasi", kut(1629.0, 1632.0, 45.0, 62.0, -377.0, -366.0), "celik",   # v25: braketin üst yüzüne oturur (v24: 1 mm)')
d('''    ekle("tabla_bos_sensoru", sily(1650.0, ZT, 9.0, 150.0, 190.0), "koyu",''',
  '''    ekle("sensor_braketi_tabla_bos", kut(1642.0, 1658.0, 190.0, 217.0, ZT - 8.0, ZT + 8.0), "celik",
         bom=("Tabla boş sensörü askısı 304", 1, "16 × 27 × 16 · soğuk paketin alt sacına (TU v14 alt_yalitim_saci, dünya 1109) 2 × M4", "v25 · sensör v24'te havadaydı"))
    ekle("tabla_bos_sensoru", sily(1650.0, ZT, 9.0, 150.0, 190.0), "koyu",''')
d('''    ekle("fire_silecegi", kut(250.0, 270.0, 125.0, 167.0, ZT - 180.0, ZT + 170.0), "silikon",   # v23: ön kenar z 0 (v22 +10)''',
  '''    FS_X = 770.0                                                                   # v25: montajın V1_TASI +520 kaydırması buraya işlendi (dünya x 1470–1490) · yeni ad
    ekle("fire_silecegi_silindiri", sily(FS_X + 10.0, ZT, 7.5, 180.0, 217.0).union(sily(FS_X + 10.0, ZT, 2.5, 167.0, 180.0)), "koyu",
         bom=("Fire sileceği silindiri · SMC CJ2B10-20 (Ø10, strok 20)", 1, "paslanmaz mini silindir · valf adasının yedek çıkışı · gövde boyu VARSAYIM",
              "sileceği 125 → 108'e indirir (17 mm) · soğuk paketin alt sacına (dünya 1109) flanşla asılı · v24'te '24 V aktüatör' yazıyordu, parça yoktu"))
    for _i, _zc in enumerate((ZT - 160.0, ZT + 150.0)):
        ekle("fire_silecegi_kilavuzu_%d" % _i, sily(FS_X + 10.0, _zc, 3.0, 167.0, 217.0), "celik",
             bom=("Silecek kılavuz mili Ø6 + POM burç", 2, "304 taşlanmış", "sileceği dönmeden indirir") if _i == 0 else None)
    ekle("fire_silecegi_lastigi", kut(FS_X, FS_X + 20.0, 125.0, 167.0, ZT - 180.0, ZT + 170.0), "silikon",   # v23: ön kenar z 0 (v22 +10)''')
d('''    ekle("agiz_alt_dudagi", kut(30.0, 1770.0, 1.5, 13.5, 0.0, -4.5).cut(kut(33.0, 1767.0, 3.5, 15.0, 1.0, -3.0)), "sac",
         bom=("Ağız alt dudağı", 1, "304 1,5 mm bükme · dış tabana ve iki yan saca sürekli kaynak",
              "silinen ağız çerçevesinin tek gerçek işi: robot çarparsa kesmeyen kıvrık kenar — ama YALNIZ ALTTA; üst lama geri konmadı, tepsi çıkışı açık"))''',
  '''    # v25: agiz_alt_dudagi SİLİNDİ (SPEC §2.3) — önü artık mekanizma bandı kapağı (tava, +59…+79) kapatıyor''')

# ---------------------------------------------------------------- 7 · AÇICI (8d) yeniden: ön tahrik dik açılı · Z ekseni · pnömatik
bolum('''    for i_, yon in enumerate((1.0, -1.0)):
        ad_ = "on" if yon > 0 else "arka"''',
      '''"kafayı taşır; rayın ARKASINDA durur, arabanın yolunu kesmez"))''',
      '''    # ---- v25 (SPEC_on_duzlem_v63 §2.3): ÖN TAHRİK DİK AÇILI · KAFA ÖN UCU ≤ +10 · HİÇBİR AÇICI PARÇASI +39'U GEÇMEZ · KİNEMATİK AYNI ----
    # Koniler (_koni) v24 ile BİREBİR: tepe (AC_X, AC_TEPE, AC_Z) · yarı açı 17,82° · boy 140 · taban Ø90. v24'te ön motor + planet redüktör koni
    # ekseninde dışarı uzuyor, +166,6'ya çıkıyordu (kafa plakası +180). v25: ön koni Motovario NMRV030 sonsuz vida redüktörünün DELİK MİLİNE geçer,
    # motor sonsuz vida ekseninde (koni eksenine dik, düşeyden 17,82° geride) YUKARI bakar; redüktör çıkış yatakları koniyi taşır (ayrı yatak yok).
    AC_FI = -AC_ACI                                                         # yerel (a: koni ekseni · b: dik yukarı-geri · c: x) → X ekseni etrafında
    for i_, yon in enumerate((1.0, -1.0)):
        ad_ = "on" if yon > 0 else "arka"
        _k, _p1 = _koni(yon)
        _p0 = cq.Vector(AC_X, AC_TEPE, AC_Z)
        _u = _birim(_p1 - _p0)                    # koniden disariya dogru ortak eksen
        ekle("acici_konisi_" + ad_, _k, "celik",
             bom=("Acici konisi - boy 140 - taban O90", 2,
                  "304 taslanmis, mat kumlu - yari aci 17,82 derece",
                  "Tepesi tabla ekseninde; tabaninda M18 dis yuva, mil yuzden vidalanir") if i_ == 0 else None)
        if yon > 0:
            _v = cq.Vector(0.0, _u.z, -_u.y)                                 # sonsuz vida / motor ekseni (yukarı-geri)
            _yer = lambda sh_: sh_.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), AC_FI).translate(_p1)
            _t = _yer(cq.Vertex.makeVertex(0.0, 0.0, 1.0)).toTuple()
            assert abs(_t[1] - _p1.y - _u.y) < 1e-6 and abs(_t[2] - _p1.z - _u.z) < 1e-6, "yerel eksen koni eksenine oturmadı"
            _bx = lambda c0, c1, b0, b1, a0, a1: cq.Solid.makeBox(c1 - c0, b1 - b0, a1 - a0, cq.Vector(c0, b0, a0))
            _cz = lambda r, a0, a1: cq.Solid.makeCylinder(r, a1 - a0, cq.Vector(0, 0, a0), cq.Vector(0, 0, 1))
            NM = dict(ac=30.0, a=(8.0, 52.0), b=(-40.0, 40.0), c=(-28.0, 44.0), hub_r=17.5, hub=(3.0, 57.0), delik=7.0, H=30.0, E=55.0, G=56.0)
            _red = _bx(NM["c"][0], NM["c"][1], NM["b"][0], NM["b"][1], NM["a"][0], NM["a"][1]).fuse(_cz(NM["hub_r"], NM["hub"][0], NM["hub"][1]))
            _red = _red.fuse(_bx(NM["H"] - NM["G"] / 2.0, NM["H"] + NM["G"] / 2.0, NM["b"][1], NM["E"], NM["ac"] - NM["G"] / 2.0, NM["ac"] + NM["G"] / 2.0))
            _red = _red.cut(_cz(NM["delik"], NM["hub"][0] - 1.0, NM["hub"][1] + 1.0))
            ekle("acici_reduktoru_on", cq.Workplane(obj=_yer(_red)), "motor",
                 bom=("Açıcı ön redüktörü · SONSUZ VİDA Motovario NMRV030 i = 7,5 · NEMA23 giriş flanşlı", 1,
                      "delik mil Ø14 H8 · eksen aralığı 30 · 54 (C) × 80 (A) · maks. çıkış 18 N·m · radyal 0,86 kN [K: Oyostepper NMRV30-G15-D9 föyü] · dış ölçüler VARSAYIM (Motovario katalog tablosu, föy indirilmedi)",
                      "koni mili delik mile geçer (kamalı) · çıkış yatakları koniyi taşır · motor sonsuz vida ekseninde yukarı bakar → kafa önü +32 (v24 +166)"))
            _mil = _cz(9.0, 0.0, 3.0).fuse(_cz(NM["delik"], 3.0, NM["hub"][1] + 2.0))
            ekle("acici_mili_on", cq.Workplane(obj=_yer(_mil)), "celik",
                 bom=("Açıcı ön mili Ø18 / Ø14 × 59 (kademeli)", 1, "17-4PH taşlanmış · Ø14 kamalı + segman", "koni tabanından redüktörün delik miline"))
            _mot = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0).translate(cq.Vector(NM["H"], NM["E"], NM["ac"]))
            ekle("acici_motoru_on", cq.Workplane(obj=_yer(_mot)), "motor",
                 bom=("Açıcı ön motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m · 2,8 A · GERÇEK CAD",
                      "redüktörün giriş flanşında, düşeyden 17,82° geride yukarı bakar · koni 114 d/dk → motor 855 d/dk · çıkış ≈ 6 N·m (VARSAYIM: 855 d/dk'da 1,0 N·m × 7,5 × η 0,8)"))
            _P = lambda a, b: _p1 + _u.multiply(a) + _v.multiply(b)
            _pts = [(_P(12.0, -30.0).y, _P(12.0, -30.0).z), (_P(48.0, -30.0).y, _P(48.0, -30.0).z), (_P(48.0, 36.0).y, _P(48.0, 36.0).z),
                    (250.0, _P(48.0, 36.0).z), (250.0, _P(12.0, 36.0).z), (_P(12.0, 36.0).y, _P(12.0, 36.0).z)]
            ekle("acici_askisi_on", cq.Workplane("YZ", origin=(AC_X + NM["c"][0] - 8.0, 0, 0)).polyline(_pts).close().extrude(8.0), "celik",
                 bom=("Açıcı ön redüktör askısı 304 8 mm", 1, "lazer · redüktörün yan yüzüne 4 × M6, üstte kafa plakasına 3 × M8", "redüktörü (ve koniyi) kafa plakasına asar; tork kolu"))
            continue
        # ARKA: v24 ile aynı (planet redüktör + motor koni ekseninde) · v25: yatak mile sıkı, askı plakası yatağa oturur
        _mil_boy = 54.0
        ekle("acici_mili_" + ad_, _eksen_silindir(_p1, _u, 9.0, _mil_boy), "celik",
             bom=("Acici arka mili O18 x 54", 1, "17-4PH taslanmis - M18 omuzlu", "koni, rulman ve reduktor cikisini AYNI eksende baglar"))
        _py = _p1 + _u.multiply(8.0)
        _yat = cq.Solid.makeCylinder(24.0, 10.0, _py, _u).cut(cq.Solid.makeCylinder(9.0, 12.0, _py - _u.multiply(1.0), _u))
        ekle("acici_yatagi_" + ad_, cq.Workplane(obj=_yat), "celik",
             bom=("Acici yatagi - flansli O18", 1, "paslanmaz govde - gida gresi - ic bilezik mile sikı (v25)", "koni tabaninin 8 mm disinda"))
        _pp = _p1 + _u.multiply(18.0)                                        # v25: 18,5 → 18 (yatak yüzüne oturur)
        _pl = cq.Workplane("XY").rect(72.0, 72.0).circle(9.2).extrude(8.0).val()
        _aski = _yonlendir(_pl, _u, _pp)
        _pc = _p1 + _u.multiply(22.0)
        for _sx in (-30.0, 30.0):
            _pa = _pc + cq.Vector(_sx, 0.0, 0.0)
            _pb = cq.Vector(_pa.x, 250.0, _pa.z)
            _vv = _pb - _pa
            _aski = _aski.fuse(cq.Solid.makeCylinder(3.5, _vv.Length, _pa, _birim(_vv)))
        ekle("acici_askisi_" + ad_, cq.Workplane(obj=_aski), "celik",
             bom=("Acici arka yatak askisi", 1, "304 - 72 x 72 x 8 plaka + 2 x O7 gergi", "rulman flansi 4 x M8; gergiler kafa plakasina M8 somunla"))
        _q_red = _p1 + _u.multiply(_mil_boy)
        _red = _yonlendir(suregear()["tum"], _u.multiply(-1.0), _q_red)
        ekle("acici_reduktoru_" + ad_, cq.Workplane(obj=_red), "motor",
             bom=("Acici arka reduktoru - planet", 1, "SureGear PGCN23-1025 GERCEK CAD", "cikis yuzu mile temas eder; eksen koniyle birebir aynidir"))
        _q_mot = _q_red + _u.multiply(79.0)
        _mot = _yonlendir(nema23()["govde"], _u.multiply(-1.0), _q_mot)
        ekle("acici_motoru_" + ad_, cq.Workplane(obj=_mot), "motor",
             bom=("Acici arka motoru - NEMA23 STP-MTR-23079", 1, "1,95 N.m - 2,8 A - GERCEK CAD", "iki koni ters yonde doner"))

    # v25 · KAFA PLAKASI: arka kısım x ±80 (z −570…−67) + ön dil x −80…−4 (z −67…+10, ön motorun solunda) · ön ucu +10 (v24 +180, taşıyıcısız 170 mm uzantı)
    _kp = kut(AC_X - 80.0, AC_X + 80.0, 250.0, 262.0, -570.0, -67.0).union(kut(AC_X - 80.0, AC_X - 4.0, 250.0, 262.0, -67.0, 10.0))
    ekle("acici_kafa_plakasi", _kp, "sac",
         bom=("Açıcı kafa plakası 12 mm (L)", 1, "304 lama · frezelenmiş · 160 × 503 + 76 × 77 dil",
              "iki koni takımı buna asılı · arka ucu Z adaptör plakasına kaynak + 2 nervür · ön ucu +10 (SPEC ≤ +10)"))
    for _i, _xr in enumerate((AC_X - 78.0, AC_X + 70.0)):
        ekle("acici_kafa_plakasi_nervur_%d" % _i, kut(_xr, _xr + 8.0, 262.0, 302.0, -570.0, -200.0), "sac",
             bom=("Kafa plakası nervürü 8 × 40 × 370", 2, "304 lama · kaynak", "580 mm konsolun sehimini sınırlar") if _i == 0 else None)
    # v25 · Z EKSENİ: kolonun ön yüzünde 2 × HGR15 ray (x ±30) · 4 × HGH15CA araba · 12 mm adaptör plaka → kafa plakası (v24: kızak ↔ kafa 30 mm boşluk, kafa havadaydı)
    ekle("acici_kolonu", kut(AC_X - 60.0, AC_X + 60.0, 0.0, 612.0, -660.0, -610.0)
         .union(kut(AC_X - 45.0, AC_X + 45.0, 582.0, 612.0, -660.0, -505.0)), "sac",
         bom=("Açıcı kolonu", 1, "304 kutu profil 120 × 50 · boy 612 + üst kol 90 × 30 × 155 · tabana (kaide A) 4 × M10",
              "Z raylarını ve pnömatik silindiri taşır; rayın ARKASINDA durur, arabanın yolunu kesmez"))
    for _i, _xr in enumerate((AC_X - 30.0, AC_X + 30.0)):
        ekle("acici_z_kizagi_%d" % _i, kut(_xr - 7.5, _xr + 7.5, 110.0, 470.0, -610.0, -595.0), "celik",
             bom=("Açıcı Z rayı HIWIN HGR15R × 360", 2, "katalog kesit 15 × 15 · M4 × 16 hatve 60", "kolonun ön yüzüne · kafa stroku 100 (0 = çalışma)") if _i == 0 else None)
        for _j, _yb in enumerate((190.0, 280.0)):
            _blk = kut(_xr - 17.0, _xr + 17.0, _yb, _yb + 61.4, -605.7, -582.0).cut(kut(_xr - 7.5, _xr + 7.5, _yb - 1.0, _yb + 62.4, -611.0, -595.0))
            ekle("acici_askisi_z_blogu_%d" % (2 * _i + _j), _blk, "celik",
                 bom=("Z arabası HIWIN HGH15CA", 4, "katalog W 34 · L 61,4 · H 28 (kutu model)", "adaptör plakasına 4 × M4") if _i == 0 and _j == 0 else None)
    ekle("acici_askisi_z_adaptoru", kut(AC_X - 60.0, AC_X + 60.0, 180.0, 350.0, -582.0, -570.0), "sac",
         bom=("Z adaptör plakası 304 12 mm", 1, "120 × 170 · 4 arabaya 16 × M4", "kafa plakası + nervürler buna kaynaklı"))
    ekle("acici_pnomatigi", kut(AC_X - 22.5, AC_X + 22.5, 388.0, 582.0, -562.5, -517.5).cut(sily(AC_X, -540.0, 6.0, 387.0, 583.0)), "koyu",
         bom=("Açıcı pnömatiği · Festo DSBC-32-100-PPVA-N3 (ISO 15552, Ø32, strok 100)", 1,
              "gövde 45 × 45 × 194 · WH 26 · mil Ø12 M10×1,25 · arka flanş FNC-32 ile kolonun üst koluna dik asılı · 6 bar'da 482 N itme",
              "kafayı indirir / 100 mm kaldırır (top girerken 90 gerekir; v24: Ø32 strok 60, z ekseninde çizilmiş, kolona bağlı değildi)"))
    ekle("acici_askisi_piston_mili", sily(AC_X, -540.0, 20.0, 262.0, 270.0).union(sily(AC_X, -540.0, 6.0, 270.0, 400.0)), "celik",
         bom=("Piston mili ucu + mil flanşı Ø40", 1, "DSBC mili (Ø12) + Festo FK-M10×1,25 esnek bağlantı + flanş", "kafa plakasına 4 × M6"))''')

# ---------------------------------------------------------------- 8 · ÖN YÜZ (C ön çerçevesi + tava paneller)
d('''    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------''',
  '''    # ---------------- 10 · v25 · ÖN YÜZ (SPEC_on_duzlem_v63 §1 + §2.3): ön çerçeve 30 × 20 × 2 (z +39…+59) + tava paneller (z +59…+79) ----------------
    # dünya → yerel: x − 700 · y − 892. Soğuk kapaklar K1/K2 + 430 çerçeve + fitil + flipper → topping_uno_cad_v14 (soğuk paket).
    yl = lambda y_: y_ - DY_D
    xl = lambda x_: x_ - DX_D
    MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(1553.5), yl(1859.0))
    CER = [("onyuz_cerceve_mek_sol_dikme", boru_y(SAC, SAC + 30.0, Z_CER_C[0], Z_CER_C[1], MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_sag_dikme", boru_y(W - SAC - 30.0, W - SAC, Z_CER_C[0], Z_CER_C[1], MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_alt_kayit", boru_x(MEK_Y[0], MEK_Y[0] + 30.0, Z_CER_C[0], Z_CER_C[1], SAC + 30.0, W - SAC - 30.0)),
           ("onyuz_cerceve_mek_ust_kayit", boru_x(MEK_Y[1] - 30.0, MEK_Y[1], Z_CER_C[0], Z_CER_C[1], SAC + 30.0, W - SAC - 30.0)),
           ("onyuz_cerceve_mek_orta_dikme", boru_y(xl(1584.25), xl(1614.25), Z_CER_C[0], Z_CER_C[1], MEK_Y[0] + 30.0, MEK_Y[1] - 30.0)),
           ("onyuz_cerceve_T_sol_dikme", boru_y(xl(1521.5), xl(1551.5), Z_CER_C[0], Z_CER_C[1], T_Y[0], Y - SAC)),
           ("onyuz_cerceve_T_sag_dikme", boru_y(W - SAC - 30.0, W - SAC, Z_CER_C[0], Z_CER_C[1], T_Y[0], Y - SAC)),
           ("onyuz_cerceve_T_alt_kayit", boru_x(T_Y[0], T_Y[0] + 30.0, Z_CER_C[0], Z_CER_C[1], xl(1551.5), W - SAC - 30.0)),
           ("onyuz_cerceve_T_ust_kayit", boru_x(Y - SAC - 30.0, Y - SAC, Z_CER_C[0], Z_CER_C[1], xl(1551.5), W - SAC - 30.0))]
    for _i, (_a, _w) in enumerate(CER):
        ekle(_a, _w, "celik", bom=("C ön çerçevesi 30 × 20 × 2 AISI 304 dikdörtgen profil · kaynaklı", len(CER),
                                   "mekanizma bandı (5 parça) + teknik cep (4 parça) · z +39…+59 (panel arkası) · yan sacların ön dönüşüne M6",
                                   "gizli menteşe + bas-aç mandallar bu çerçeveye") if _i == 0 else None)
    # tava paneller · derz 3 · dünya: mekanizma kanatları x 701,5–1597,75 / 1600,75–2497 · y 791–1107,5 · T x 1521,5–2497 · y 1553,5–1859
    _yar = []
    for _xg in (860.0, 930.0, 1000.0, 1070.0):                                  # giriş (sol-alt, soğutma grubunun önü): 32 yarık 60 × 4
        for _yg in range(8):
            _yar.append((_xg, _xg + 60.0, 690.0 + 10.0 * _yg, 694.0 + 10.0 * _yg))
    for _xg in (1480.0, 1550.0, 1620.0, 1690.0):                                # çıkış (sağ-üst): 32 yarık 60 × 4
        for _yg in range(8):
            _yar.append((_xg, _xg + 60.0, 870.0 + 10.0 * _yg, 874.0 + 10.0 * _yg))
    PAN = [("onyuz_mekanizma_kanadi_sol", (xl(701.5), xl(1597.75), MEK_Y[0], MEK_Y[1]), (), "sol", 57.0),
           ("onyuz_mekanizma_kanadi_sag", (xl(1600.75), xl(2497.0), MEK_Y[0], MEK_Y[1]), (), "sag", 57.0),
           ("onyuz_T_kapagi", (xl(1521.5), xl(2497.0), T_Y[0], T_Y[1]), tuple(_yar), "sag", 828.0)]
    for _a, (_x0, _x1, _y0, _y1), _yr, _mt, _yc in PAN:
        ekle(_a, tava(_x0, _x1, _y0, _y1, _yr), "sac",
             bom=("%s · tava 20 · AISI 304 fırçalı 1,5" % _a.replace("onyuz_", ""), 1,
                  "%.2f × %.1f · dışarıdan yalnız düz yüzey + derz 3%s" % (_x1 - _x0, _y1 - _y0, " · 64 lazer yarık 60 × 4 (giriş sol-alt / çıkış sağ-üst, soğutma grubu havası)" if _yr else ""),
                  "gizli menteşe %s · bas-aç · %s" % (_mt, "kaide bandını (791–892) da örter, alttan açılmaz" if "mekanizma" in _a else "teknik cep servis kapağı")))
        ekle(_a + "_omega", omega_pz(_x0 + 3.0, _x1 - 3.0, _yc, Z_ON - 1.5, -1.0), "celik",
             bom=("Panel omegası 1,0 · 40 × 15", 1, "AISI 304 1,0 · panel > 600 (SPEC) · yüz sacının arkasına punta", "") if "kanadi_sol" in _a else None)
        _xm = (_x0 + 2.5, _x0 + 27.5) if _mt == "sol" else (_x1 - 27.5, _x1 - 2.5)
        for _j, _ym in enumerate((_y0 + 40.0, _y1 - 110.0)):
            ekle("%s_mentese_%d" % (_a, _j), kut(_xm[0], _xm[1], _ym, _ym + 70.0, Z_PAN_C[0], Z_ON - 1.5), "celik",
                 bom=("Gizli menteşe 90° · EMKA 1006-U1-PC (tava panel)", 6, "AISI 304 · çerçeveye + panele kaynak · dışarıdan sökülemez (emka.com)",
                      "ölçü VARSAYIM (25 × 70 × 18,5 zarf) — A kabini ile aynı ürün") if _a.endswith("kanadi_sol") and _j == 0 else None)
        _xb = (_x1 - 11.0, _x1 - 2.0) if _mt == "sol" else (_x0 + 2.0, _x0 + 27.0)
        _yb = (_y0 + 196.0, _y0 + 216.0) if "mekanizma" in _a else (_y0 + 108.5, _y0 + 138.5)
        ekle(_a + "_basac", kut(_xb[0], _xb[1], _yb[0], _yb[1], Z_PAN_C[0], Z_ON - 1.5), "plastik",
             bom=("Bas-aç mandal (push-to-open, gizli) · Southco E4 touch latch", 3, "parça no + ölçü VARSAYIM", "kulpsuz kapak") if _a.endswith("kanadi_sol") else None)

    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------''')

# ---------------------------------------------------------------- 9 · MALZEME
d('MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))',
  'MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))\n'
  'MALZEME.setdefault("silikon", dict(renk=(0.85, 0.30, 0.20, 1.0), met=0.0, ruf=0.6))          # v25\n'
  'MALZEME.setdefault("plastik", dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6))')

# ---------------------------------------------------------------- 10 · __main__ denetimleri
d('    print("TOPPING MODULU v23 · %d parca', '    print("TOPPING MODULU v25 · %d parca')
d('''    _z_on = 310.0
    tas = [a for a, b in bb if b.xmin < _zx0 - 0.01 or b.xmax > _zx1 + 0.01 or b.ymin < -0.01 or b.ymax > Y + 0.01 or b.zmax > _z_on + 0.01 or b.zmin < -D - 0.01]''',
  '''    _z_on = Z_ON + 0.5                                                          # v25: ön düzlem (v24: açıcı için +310)
    tas = [a for a, b in bb if b.xmin < _zx0 - 0.01 or b.xmax > _zx1 + 0.01 or b.ymin < ((791.0 - DY_D) if a.startswith("onyuz_") else 0.0) - 0.01 or b.ymax > Y + 0.01 or b.zmax > _z_on + 0.01 or b.zmin < -D - 0.01]''')
d('''    _ACICI = ("acici", "koni", "kafa")
    _on = [(a, round(b.zmax, 1)) for a, b in bb if b.zmax > 0.01 and not any(k in a for k in _ACICI)]
    print("ON YUZ (z <= 0, acici haric): %s" % ("GECTI" if not _on else "TASAN: %s" % _on)); assert not _on
    _ac = sorted(((round(b.zmax, 1), a) for a, b in bb if b.zmax > 0.01), reverse=True)
    print("   on yuzden tasan (yalniz acici kafasi, bilinen acik konu): %s" % _ac[:8])''',
  '''    _on = [(a, round(b.zmax, 2)) for a, b in bb if b.zmax > Z_ON + 0.5]
    print("ON DUZLEM (v25 · butun parcalar z <= +79,5 · acici istisnasi YOK): %s · en on %s" % ("GECTI" if not _on else "TASAN: %s" % _on, sorted(((round(b.zmax, 2), a) for a, b in bb), reverse=True)[:3])); assert not _on
    _acz = [(a, round(b.zmax, 2)) for a, b in bb if a.startswith("acici_") and b.zmax > Z_KABUK + 0.01]
    _kaf = max(b.zmax for a, b in bb if a.startswith("acici_kafa_plakasi"))
    print("ACICI (v25 · hicbir parca +39'u gecmez · kafa on ucu <= +10): en on acici parcasi %s · kafa plakasi %+.1f · %s"
          % (max(((round(b.zmax, 1), a) for a, b in bb if a.startswith("acici_"))), _kaf, "GECTI" if not _acz and _kaf <= 10.01 else "KALDI %s" % _acz)); assert not _acz and _kaf <= 10.01
    _kb = {a: round(b.zmax, 2) for a, b in bb if a in ("dis_taban", "dis_tavan", "dis_yan_sol", "dis_yan_sag")}
    print("KABUK on kenari +39: %s · %s" % (_kb, "GECTI" if all(abs(v - Z_KABUK) < 0.01 for v in _kb.values()) else "KALDI")); assert all(abs(v - Z_KABUK) < 0.01 for v in _kb.values())
    _pn = {a: (round(b.zmin, 2), round(b.zmax, 2)) for a, b in bb if a in ("onyuz_mekanizma_kanadi_sol", "onyuz_mekanizma_kanadi_sag", "onyuz_T_kapagi")}
    print("TAVA PANELLER z +59…+79: %s · %s" % (_pn, "GECTI" if all(abs(v[0] - Z_PAN_C[0]) < 0.01 and abs(v[1] - Z_ON) < 0.01 for v in _pn.values()) else "KALDI"))
    assert len(_pn) == 3 and all(abs(v[0] - Z_PAN_C[0]) < 0.01 and abs(v[1] - Z_ON) < 0.01 for v in _pn.values())''')
d('''    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in gercek]; bulgu = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue''',
  '''    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in gercek]; bulgu = []
    _atla = 0
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            if eski(S[i][0]) != eski(S[j][0]): _atla += 1; continue                 # v25: montajdan düşen eski parça ↔ görünen parça ölçüm dışı (SPEC §2.3)''')
d('''    print("CAKISMA: %s" % ("TEMIZ" if not bulgu else "%d BULGU" % len(bulgu)))''',
  '''    print("CAKISMA: %s (v25: eski/montaj-dışı ↔ görünen %d aday çift ölçüm dışı · görünenler dünya denetiminde ayrıca)" % ("TEMIZ" if not bulgu else "%d BULGU" % len(bulgu), _atla))''')
d('''    # v23: STEP/STL üretim dosyaları YAZILMAZ (kural 6.7: SolidWorks/STEP çıktısı yok; v22 klasörü korunur)
    sys.stdout.flush(); os._exit(0)''',
  '''    # v25 · DÜNYA DENETİMİ (montajın gördüğü C istasyonu: TC v25 + TU v14 + itici)
    DD = dunya_denetimi()
    _kal = [x for x in DD if not x[1]]
    print("DUNYA DENETIMI: %d denetim · %s" % (len(DD), "HEPSI GECTI" if not _kal else "%d KALDI" % len(_kal)))
    assert not _kal, _kal
    # v23: STEP/STL üretim dosyaları YAZILMAZ (kural 6.7: SolidWorks/STEP çıktısı yok; v22 klasörü korunur)
    sys.stdout.flush(); os._exit(0)''')

# ---------------------------------------------------------------- 11 · dünya denetimi (modül seviyesi: montaj da çağırabilir)
DUNYA = r'''

# ======================================================================================================================================
# v25 · DÜNYA DENETİMİ — montajın gördüğü C istasyonu (hat_montaj_v62 süzgeçleri) · montaj ya da ajanlar da çağırabilir: TC.dunya_denetimi()
# ======================================================================================================================================
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")                      # hat_montaj_v62 L253
KAPAK_ESKI = ("on_kapak", "on_kapak_pu", "kapak_contasi")                                                   # hat_montaj_v62 L1371
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
V3_CIKAN = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")
V1_TASI = {"sogutma_grubu": (790.0, 0.0, 0.0), "pano_kutusu": (80.0, 0.0, 0.0), "ups": (140.0, 0.0, 0.0), "din_ray_ups": (140.0, 0.0, 0.0),
           "guc_kaynagi": (1196.0, 0.0, 0.0), "fire_silecegi": (520.0, 0.0, 0.0)}                            # hat_montaj_v62 L264 — v25'te bu adlar YOK (etkisiz)
for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
ACICI_HAREKET = ("acici_yatagi_", "acici_reduktoru_", "acici_motoru_", "acici_askisi_", "acici_kafa_plakasi", "acici_konisi_", "acici_mili_")   # montaj v62 L742–744
YARIK_V2 = ((2492.0, 2498.5, 977.0, 1042.0, -417.0, -5.0), (2491.0, 2499.5, 987.0, 1038.0, -409.0, -13.0))    # firin_tp10_cad_v7.YARIK_V2 (montaj cikis_yarigi_contasi yerine)
ANA_V44_DUNYA = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -432.0), (2340.0, 1809.0, -432.0), (2340.0, 1809.0, -740.0)]   # hat_montaj_v62 ANA_V44 + DY + X_BC (ilk 4 nokta)
BEYAZ_HAVADA = [("TU:kasar_cad_v14__", "kaşar kasetinin kendi dönen parçaları (helezon çekirdeği, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): kasar_cad_v14 üretecindeki yatak burcu boşluğu 0,10–0,15 mm — idealleştirilmiş temas (bilyeli ray ara elemanı gibi); kaset üreteci bu işin dışında"),
                ("TU:sucuk_cad_v7__", "sucuk kasetinin kendi dönen parçaları (helezon A–D + çekirdek, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): sucuk_cad_v7 yatak burcu boşluğu 0,10–0,15 mm — idealleştirilmiş temas"),
                ("TU:motor_kablosu_", "motor kablo ucu (esnek, motor konnektörüne takılı) — STEP'teki kablo çıkışı gövdeden 0,7 mm")]
BEYAZ_CAKISMA = [("TU:sos__", "UNO modeli (beldos_cad_v1) iç geçmeleri — satın alınan ürün"), ("TU:harc__", "UNO modeli iç geçmeleri"), ("TU:kiyma__", "UNO modeli iç geçmeleri"),
                 ("TU:kusbasi__", "UNO modeli iç geçmeleri"), ("TU:sos_spreader_", "Beldos spreader attachment iç geçmeleri (tek satın alınan grup, görselden oranla)"),
                 ("TU:harc_spreader_", "Beldos spreader attachment iç geçmeleri"), ("TU:kasar_cad_v14__", "kaşar kaseti iç geçmeleri (kaset üreteci)"),
                 ("TU:sucuk_cad_v7__", "sucuk kaseti iç geçmeleri (kaset üreteci)"), ("IT:", "itici iç pim / burç geçmeleri (itici_cad kendi denetiminde muaf)")]
BIZIM_TU = ("_D70", "cikis_tc_ferrule_valf")                                                               # UNO önekli ama BİZİM parçalar → beyaz listeye girmez


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


def eski(ad):
    """montajın düşürdüğü (görünmeyen) parça"""
    return ad.startswith("_bom") or ad in KAPAK_ESKI or ad in AKTARMA_TP10 or not v1_kalir(ad)


def _tek(wp):
    v = wp.vals() if hasattr(wp, "vals") else [wp]
    v = [o for o in v if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


def dunya_parcalari(TU, IT=None):
    """montaj v62 süzgeçleriyle C istasyonu: TC (eski parçalar düşer, V1_TASI, çıkış yarığı = YARIK_V2) + TU (V3_CIKAN düşer, x + 700 · y − 168) + itici (ev, kalkık)"""
    W_ = []
    for p in PARCALAR:
        if eski(p["ad"]): continue
        d_ = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = _tek(p["wp"]).translate(cq.Vector(DX_D + d_[0], DY_D + d_[1], d_[2]))
        if p["ad"] == "cikis_yarigi_contasi":
            sh = kut(*YARIK_V2[0]).cut(kut(*YARIK_V2[1])).val()
        W_.append(("TC:" + p["ad"], sh))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        W_.append(("TU:" + q["ad"], q["sh"].translate(cq.Vector(DX_D, -168.0, 0.0))))
    if IT is not None:
        IT.kur(IT.S_HOME, True)
        W_ += [("IT:" + p["ad"], IT.dunya(p)) for p in IT.PARCALAR]
    return W_


def _bbk(A, B, t=0.0):
    return not (A.xmax < B.xmin - t or B.xmax < A.xmin - t or A.ymax < B.ymin - t or B.ymax < A.ymin - t or A.zmax < B.zmin - t or B.zmax < A.zmin - t)


def _hacim(a, b):
    try: return a.intersect(b).Volume()
    except Exception: return -1.0


def _beyaz_cakisma(a, c):
    if any(k_ in a or k_ in c for k_ in BIZIM_TU): return None
    for g, _n in BEYAZ_CAKISMA:
        if a.startswith(g) and c.startswith(g): return g
    return None


def _cakisma_listesi(W_, esik=1.0):
    L = sorted([(a, sh, sh.BoundingBox()) for a, sh in W_], key=lambda q: q[2].xmin)
    bul, beyaz = [], {}
    for i in range(len(L)):
        a, A, ba = L[i]
        for j in range(i + 1, len(L)):
            c, C, bc = L[j]
            if bc.xmin > ba.xmax: break
            if not _bbk(ba, bc): continue
            v = _hacim(A, C)
            if v > esik or v < 0:
                g = _beyaz_cakisma(a, c)
                if g: beyaz[g] = beyaz.get(g, 0) + 1
                else: bul.append((round(v, 1), a, c))
    return bul, beyaz


def dunya_denetimi(kaset_adim=10.0):
    """(ad, geçti, değer) listesi · TU v14 + TC v25 + itici v5 dünyada"""
    import importlib, importlib.util as ilu
    import denetim_temas_v1 as DT
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as DSS
    R = []
    def k(ad, ok, deger=""):
        R.append((ad, bool(ok), deger)); print("  %-150s %s %s" % (ad, "GEÇTİ" if ok else "** KALDI **", deger)); sys.stdout.flush()
    t0 = time.time()
    if not [p for p in PARCALAR if p["ad"] == "dis_taban"]:
        PARCALAR[:] = []; modul()
    sp = ilu.spec_from_file_location("TU11", os.path.join(U, TU_DOSYA)); TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    n_tu = TU.den_assert()
    k("TU %s: modül denetimi %d / %d GEÇTİ (den_assert — montaj da çağırabilir)" % (TU_DOSYA, n_tu, n_tu), True)
    try:
        IT = importlib.import_module(ITICI_MOD); it_ad = ITICI_MOD
    except ImportError:
        IT = importlib.import_module("itici_cad_v4"); it_ad = "itici_cad_v4"
    W_ = dunya_parcalari(TU, IT)
    B_ = {a: sh.BoundingBox() for a, sh in W_}
    n_tc, n_tu2, n_it = (sum(1 for a in B_ if a.startswith(p_)) for p_ in ("TC:", "TU:", "IT:"))
    print("DUNYA: TC %d + TU %d + itici (%s) %d = %d parça · %.0f sn" % (n_tc, n_tu2, it_ad, n_it, len(W_), time.time() - t0))
    # 1 · ön düzlem
    zm = max((b.zmax, a) for a, b in B_.items())
    k("ön düzlem: C istasyonunun bütün parçaları z ≤ +79,5 (istisna yok) · en ön %s %+.2f" % (zm[1], zm[0]), zm[0] <= Z_ON + 0.5)
    PANEL = {"TC:onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, 791.0, 1107.5), "TC:onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, 791.0, 1107.5),
             "TC:onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0), "TU:onyuz_K1_dis_sac": (701.5, 1518.5, 1110.5, 1859.0), "TU:onyuz_K2_dis_sac": (1521.5, 2497.0, 1110.5, 1550.5)}
    _pk = []
    for a, r in PANEL.items():
        b = B_[a]
        _pk.append((a, abs(b.zmax - Z_ON) < 0.01 and all(abs(u - v) < 0.01 for u, v in zip((b.xmin, b.xmax, b.ymin, b.ymax), r))))
    k("ön yüz panelleri SPEC ölçüsünde, dış yüz tam +79,0: %s" % ", ".join("%s %s" % (a.split(":")[1].replace("onyuz_", ""), "✓" if ok else "✗") for a, ok in _pk), all(ok for a, ok in _pk))
    rs = list(PANEL.values())
    ort = sum(max(0.0, min(p[1], q[1]) - max(p[0], q[0])) * max(0.0, min(p[3], q[3]) - max(p[2], q[2])) for i_, p in enumerate(rs) for q in rs[i_ + 1:])
    alan = sum((r[1] - r[0]) * (r[3] - r[2]) for r in rs)
    derz = 1795.5 * 3.0 + 3.0 * 316.5 + 3.0 * 748.5 + 975.5 * 3.0                                             # 1107,5/1110,5 · kanatlar · K1|K2+T · K2|T
    top = (2497.0 - 701.5) * (1859.0 - 791.0)
    k("ön yüz kapsama: 5 panel %.0f mm² + derz (3 mm) %.0f mm² = C önü %.0f mm² (x 701,5–2497 · y 791–1859) · panel üst üste %.0f · A|C ve C|F derzleri 3 (698,5/701,5 · 2497/2500)"
      % (alan, derz, top, ort), abs(alan + derz - top) < 1.0 and ort < 0.01)
    # 2 · açıcı
    ac = [(b.zmax, a) for a, b in B_.items() if a.startswith("TC:acici_")]
    kp = B_["TC:acici_kafa_plakasi"].zmax
    k("açıcı: hiçbir parça +39'u geçmez (en ön %s %+.1f) · kafa plakası ön ucu %+.1f ≤ +10" % (max(ac)[1], max(ac)[0], kp), max(ac)[0] <= Z_KABUK + 0.01 and kp <= 10.01)
    # 3 · çakışma
    bul, beyaz = _cakisma_listesi(W_)
    k("çakışma (gerçek katı > 1 mm³, bütün çiftler): %d · beyaz liste (satın alınan / başka üretecin iç geçmeleri): %s" % (len(bul), beyaz), not bul, str(bul[:8]))
    # 4 · havada parça
    hv = DT.havada(W_, zemin_y=DY_D)
    DT.yaz(hv, en_cok=60, baslik="HAVADA PARCA (dunya · kok: 892 tabanı)")
    kal, bl = [], {}
    for c_ in hv["bilesen"]:
        g = None
        for p_, _n in BEYAZ_HAVADA:
            if all(u.startswith(p_) for u in c_["uye"]): g = p_
        if g: bl[g] = bl.get(g, 0) + len(c_["uye"])
        else: kal.append(c_["en"])
    k("havada parça: %d parça · kök %d · bağlı %d · beyaz liste %s · KALAN %d" % (hv["parca"], hv["kok"], hv["bagli"], bl, len(kal)), not kal, str(kal[:10]))
    # 5 · açıcı kafası kalkık (+60 bekleme · +90 top girerken · +100 strok sonu)
    har = [(a, sh) for a, sh in W_ if a.startswith(tuple("TC:" + h_ for h_ in ACICI_HAREKET))]
    sab = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(tuple("TC:" + h_ for h_ in ACICI_HAREKET))]
    for dy in (60.0, 90.0, 100.0):
        c_ = []
        for a, sh in har:
            s2 = sh.translate(cq.Vector(0.0, dy, 0.0)); b2 = s2.BoundingBox()
            for c, sc, bc in sab:
                if _bbk(b2, bc):
                    v = _hacim(s2, sc)
                    if v > 1.0 or v < 0: c_.append((round(v, 1), a, c))
        k("açıcı kafası +%.0f mm (%d hareketli parça) ↔ sabit parçalar çakışma 0" % (dy, len(har)), not c_, str(c_[:6]))
    # 6 · kaset çekme 0–630 (soğuk kapaklar + flipper AÇIK)
    for mod in ("kasar_cad_v14", "sucuk_cad_v7"):
        kod = "kasar" if mod.startswith("kasar") else "sucuk"
        kas = [sh for a, sh in W_ if a.startswith("TU:" + mod + "__")]
        st = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(("TU:" + mod + "__", "TU:yuva_%s_mandal_dili" % kod, "TU:onyuz_K1_", "TU:onyuz_K2_", "TU:onyuz_flipper"))]
        bul_k = []
        dz = kaset_adim
        while dz <= 630.0 + 1e-6:
            kc = cq.Compound.makeCompound([q.translate(cq.Vector(0.0, 0.0, dz)) for q in kas]); kb = kc.BoundingBox()
            for a, sc, bc in st:
                if _bbk(kb, bc):
                    v = _hacim(kc, sc)
                    if v > 1.0 or v < 0: bul_k.append((dz, a, round(v, 1)))
            dz += kaset_adim
        k("kaset çekme %s 0–630 mm (adım %.0f · kapak açık): TC + TU + itici sabitlerine değmiyor · 430 çerçeve çentiği fitilin içinde" % (mod, kaset_adim), not bul_k, str(bul_k[:6]))
    # 7 · hava hatları
    ana = TU.boru(ANA_V44_DUNYA, 5.0); ana = ana.val() if hasattr(ana, "val") else ana
    _sag = dict(W_)["TC:dis_yan_sag"]; _rk = dict(W_)["TC:rakor_hava_ana"]
    _d = DSS(ana.wrapped, _rk.wrapped); _d = _d.Value() if _d.IsDone() else 99.0
    k("montaj ana hattı (ANA_V44 · y 1809 · z −432) sağ yan sacın rakorundan geçer: sacla kesişim %.1f mm³ · rakora %.3f mm" % (_hacim(ana, _sag), _d), _hacim(ana, _sag) < 0.01 and _d <= 0.05)
    for j_ in (1, 2):
        h_ = dict(W_)["TU:hava_hatti_acici_D6_%d" % j_]
        _d = DSS(h_.wrapped, dict(W_)["TC:acici_pnomatigi"].wrapped); _d = _d.Value() if _d.IsDone() else 99.0
        k("açıcı hattı %d: sol yan sac rakorundan geçer (sacla kesişim %.1f) · ucu Z silindirinin portunda (%.3f mm)" % (j_, _hacim(h_, dict(W_)["TC:dis_yan_sol"]), _d),
          _hacim(h_, dict(W_)["TC:dis_yan_sol"]) < 0.01 and _d <= 0.05)
    # 8 · teknik cep tabanı + DIN ray sınırı
    tk = [(a, round(B_[a].ymin, 2)) for a in B_ if a.startswith("TC:teknik_") and not a.startswith("TC:teknik_din_rayi")]
    k("teknik cep parçaları tabanda (dünya 1553,5): %s · DIN rayları x ≤ 2497 (%.1f)" % (tk, max(B_[a].xmax for a in B_ if "din_rayi" in a)),
      all(abs(v - 1553.5) < 0.01 for a, v in tk) and max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01)
    # 9 · kinematik = v24 (koniler, disk, tabla, ray)
    try:
        V24 = importlib.import_module("topping_cad_v24"); V24.PARCALAR[:] = []; V24.modul()
        es = []
        for ad in ("acici_konisi_on", "acici_konisi_arka", "calisma_diski", "tabla", "lineer_ray_on", "araba_plakasi", "doner_yatak"):
            a1 = _tek([p for p in V24.PARCALAR if p["ad"] == ad][0]["wp"]); a2 = _tek([p for p in PARCALAR if p["ad"] == ad][0]["wp"])
            b1, b2 = a1.BoundingBox(), a2.BoundingBox()
            es.append((ad, max(abs(u - v) for u, v in zip((b1.xmin, b1.xmax, b1.ymin, b1.ymax, b1.zmin, b1.zmax), (b2.xmin, b2.xmax, b2.ymin, b2.ymax, b2.zmin, b2.zmax))), abs(a1.Volume() - a2.Volume())))
        k("kinematik v24 ile aynı (koniler, çalışma diski, tabla, ray, araba, döner yatak): en büyük fark kutu %.4f mm · hacim %.3f mm³" % (max(e[1] for e in es), max(e[2] for e in es)),
          max(e[1] for e in es) < 0.001 and max(e[2] for e in es) < 0.01)
    except Exception as e_:
        k("kinematik v24 karşılaştırması yapılamadı: %s" % e_, False)
    # 10 · bilgi: A kabini + kaide v2 ile (A ajanının dosyaları varsa)
    try:
        import acici_kabin_cad_v1 as AK, kaide_cad_v2 as KD2
        AK.kur(); KD2.kur()
        A_ = [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR] + [("KAIDE:" + p["ad"], KD2.dunya(p)) for p in KD2.PARCALAR]
        cA = []
        for a, sa in A_:
            ba = sa.BoundingBox()
            for c, sc in W_:
                if _bbk(ba, B_[c]):
                    v = _hacim(sa, sc)
                    if v > 1.0 or v < 0: cA.append((round(v, 1), a, c))
        print("  BİLGİ · A kabini (acici_kabin_cad_v1) + kaide_cad_v2 ↔ C istasyonu (%d + %d parça) çakışma: %s" % (len(AK.PARCALAR), len(KD2.PARCALAR), "TEMİZ" if not cA else "%d BULGU %s" % (len(cA), cA[:6])))
        R.append(("BİLGİ · A kabini + kaide v2 ↔ C çakışma %d" % len(cA), True, str(cA[:6])))
    except Exception as e_:
        print("  BİLGİ · A kabini / kaide v2 yüklenemedi (%s)" % str(e_)[:100])
    print("DUNYA DENETIMI SURESI %.0f sn" % (time.time() - t0))
    return R
'''
d('\n\nif __name__ == "__main__":\n    t0 = time.time(); modul()', DUNYA + '\n\nif __name__ == "__main__":\n    t0 = time.time(); modul()')

# ================================================================ 12 · v25 DÜZELTME TURU (28 Eyl 2026 sabah · on_duzlem_v63/denetim_C.md)
#   A ajanı: mekanizma kanatları 788'den (A alt paneliyle basamaksız) · bulgu 2 (kapak açılışı: sanal pivot + tarama) · 4 (havada beyaz listesi açıklıkla sınırlı) ·
#   6 (mandal simetrik) · 7 (T sol dikmesi köşebentle) · 8 (teknik cep taşıyıcıları + titreşim takozu) · 9 (T yarıkları çerçeve dışına) · 12 (eski soğuk hücre BOM'dan çıktı) ·
#   13 (hazne dolum çekmesi denetimde) · 1 (soğuk taban kaçak + çerçeve bandı dünyada)
d('  havada parçalar bağlandı · montaj V1_TASI kaydırmaları yeni adlarla son yerinde · dünya denetimi (TU v14 + itici). Önceki: topping_cad_v24.py (yap_topping_v25.py)\n',
  '  havada parçalar bağlandı · montaj V1_TASI kaydırmaları yeni adlarla son yerinde · dünya denetimi (TU v14 + itici). Önceki: topping_cad_v24.py (yap_topping_v25.py)\n'
  'v25 DÜZELTME (28 Eyl sabah · on_duzlem_v63/denetim_C.md): mekanizma kanatları 788\'den (A|C basamak yok) · tava panel menteşeleri kol + taban, sanal pivot\n'
  '  ön dış köşe · bas-aç mandallar simetrik (üst kayıtta) · T sol dikmesi dikey ayırma sacına 2 L köşebent · teknik cep 2 × L 30×30×3 taşıyıcı + titreşim\n'
  '  takozu · T yarıkları çerçevenin önünden çekildi · eski v1 soğuk hücre / ön kapak BOM\'dan çıktı · dünya denetimi: soğuk taban kaçağı, çerçeve bandı,\n'
  '  5 kapak açılma taraması (flipper katlanarak), hazne dolum çekmesi, bağlantı temasları, havada beyaz listesi ≤ 0,25 mm açıklıkla\n')
d('RAKOR_ANA = (1809.0 - 892.0, -432.0)                                      # sağ yan sac · montaj ANA_V44 (dünya y 1809, z −432)\n',
  'RAKOR_ANA = (1809.0 - 892.0, -432.0)                                      # sağ yan sac · montaj ANA_V44 (dünya y 1809, z −432)\n'
  'MEK_PAN_Y0 = 788.0                 # v25b · mekanizma kanatlarının alt kenarı = A alt paneli (dolap önü 785 + derz 3 · A|C birleşiminde basamak yok — A ajanı / denetçi 3)\n'
  'ON_PANELLER = {"onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, MEK_PAN_Y0, 1107.5), "onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, MEK_PAN_Y0, 1107.5),\n'
  '               "onyuz_T_kapagi": (1521.5, 2497.0, 1553.5, 1859.0)}          # v25b · tava paneller DÜNYA x0, x1, y0, y1 (pafta / montaj buradan okusun)\n'
  'T_YARIK_Y = (700.0, 860.0)          # v25b · T lazer yarık bantlarının ilk sırası (yerel y · giriş / çıkış; v25: 690 / 870 → çerçeve kayıtlarının arkasında kalıyordu)\n'
  'PAN_DON = {"onyuz_mekanizma_kanadi_sol": (701.5, "sol"), "onyuz_mekanizma_kanadi_sag": (2497.0, "sag"), "onyuz_T_kapagi": (2497.0, "sag")}   # dünya menteşe kenarı\n'
  'TEK_TASIYICI_Y, TEK_TAKOZ = 1553.5 + 31.0, 10.0   # v25b · teknik cep taşıyıcı üstü (dünya) · titreşim takozu yüksekliği\n'
  '\n\n'
  'def panel_don(sh, ad, aci):\n'
  '    """v25b · tava panel açık konumu (DÜNYA şekli): çok kollu gizli menteşe, sanal dönme merkezi ön dış köşe (x menteşe kenarı, z +79), dikey eksen · aci derece"""\n'
  '    x, yon = PAN_DON[ad.split(":")[-1]]\n'
  '    return sh.rotate(cq.Vector(x, 0.0, Z_ON), cq.Vector(x, 1.0, Z_ON), -aci if yon == "sol" else aci)\n')
# 12.1 · teknik cep: 2 × L 30×30×3 taşıyıcı (yan saclara) + titreşim takozları · parçalar taşıyıcıların üstünde
bolum('    TEK_TABAN = 1553.5 - DY_D\n', '"UPS + güç kaynağı raylarını taşır"))',
      '''    TEK_TABAN = 1553.5 - DY_D
    TEK_TASI = TEK_TASIYICI_Y - DY_D                                             # v25b · taşıyıcı üstü (yatay sacın 31 üstü) — denetim_C bulgu 8: ağır parçalar 1,5 sac + PU üstündeydi
    for _i, (_za, _zv) in enumerate((((-90.0, -60.0), (-90.0, -87.0)), ((-208.0, -178.0), (-181.0, -178.0)))):
        _L = kut(821.5, W - SAC, TEK_TASI - 3.0, TEK_TASI, _za[0], _za[1]).union(kut(821.5, W - SAC, TEK_TABAN + 1.0, TEK_TASI - 3.0, _zv[0], _zv[1]))
        ekle("teknik_tasiyici_%d" % _i, _L, "celik",
             bom=("Teknik cep taşıyıcısı L 30 × 30 × 3 AISI 304", 2, "boy %.0f · uçlarda 3 mm alın plakası: sağda TC yan sacına 2 × M6, solda teknik ayırma dikey sacına 2 × M6 (dikey sac üstte TC tavanına kaynaklı)" % (W - SAC - 821.5),
                  "v25b · denetim_C bulgu 8: soğutma grubu (~15–20 kg, titreşimli) + pano yükü yan saclara · dik kol yatay sacın 1 mm ÜSTÜNDE biter → PU'ya yük yok") if _i == 0 else None)
    for _i, (_tx, _tz) in enumerate(((870.0, -75.0), (1130.0, -75.0), (870.0, -193.0), (1130.0, -193.0), (1200.0, -75.0), (1560.0, -75.0), (1200.0, -193.0), (1560.0, -193.0))):
        ekle("teknik_takoz_%d" % _i, sily(_tx, _tz, 10.0, TEK_TASI, TEK_TASI + TEK_TAKOZ), "silikon",
             bom=("Titreşim takozu Ø20 × 10 · M6 çift saplama (kauçuk, ör. silent-block tip A 40 Shore — parça no VARSAYIM)", 8, "soğutma grubu 4 + pano 4",
                  "v25b · taşıyıcıya + cihaz tabanına M6") if _i == 0 else None)
    ekle("teknik_sogutma_grubu", kut(850.0, 1150.0, TEK_TASI + TEK_TAKOZ, TEK_TASI + TEK_TAKOZ + 220.0, -60.0, -280.0), "motor",
         bom=("Soğutma grubu ⅕ HP · YAPTIRILACAK", 1, "hermetik, hava soğutmalı · soğutmacı firma kurar",
              "teknik cepte, 2 taşıyıcı + 4 titreşim takozu üstünde (v25b); önden T kapağının lazer yarıklarından emer (sol-alt), sağ-üstten atar. RAFTAN ALINAN PARÇA DEĞİL: "
              "modelde YER ZARFI, kesin marka/model firma seçince belli olacak (300 × 220 × 220)"))
    _pd = kut(1180.0, 1580.0, TEK_TASI + TEK_TAKOZ, TEK_TASI + TEK_TAKOZ + 240.0, -40.0, -290.0)
    _pi = kut(1181.5, 1578.5, TEK_TASI + TEK_TAKOZ + 1.5, TEK_TASI + TEK_TAKOZ + 238.5, -41.5, -288.5)
    ekle("teknik_pano_kutusu", _pd.cut(_pi), "sac",
         bom=("TOPPING panosu", 1, "304 · önden kapaklı, IP54", "PLC giriş/çıkış + röleler + sürücü beslemesi · v25b: 2 taşıyıcı + 4 titreşim takozu üstünde (M6)"))
    ekle("teknik_ups", din_parca(UPS_STEP, 1660.0, TEK_TASI, -40.0), "koyu",
         bom=("UPS PULS UB10.242 · DIN ray 24 V", 1,
              "121,7 × 49,0 × 130,5 mm (GERÇEK CAD) · ayrıca akü modülü ister",
              "elektrik kesintisinde kaset konumları ve saat korunur; ön taşıyıcının üstünde, DIN rayında"))
    ekle("teknik_guc_kaynagi", din_parca(GUC_STEP, 1592.0, TEK_TASI, -40.0), "sac",
         bom=("Güç kaynağı MEAN WELL NDR-240-24 · 24 V 240 W", 1,
              "DIN ray · 125,2 × 63,0 × 122,8 mm (GERÇEK CAD)",
              "aynı anda en çok 2 mil döner; motor 2,8 A → gerek %d W, bir üst standart boy 240 W" % H.S["elektrik"]["guc_kaynagi_W"]))
    ekle("teknik_din_rayi_ups", kut(1656.0, 1797.0, TEK_TASI, TEK_TASI + 35.0, -178.0, -170.5), "sac",          # v25b: taşıyıcı kotunda → UPS klipsi raya oturur (0,77 mm açıktı)
         bom=("DIN ray TS35 × 7,5 · UPS", 1, "EN 60715 · 141 mm", "v25 · dünya x 2356–2497 (v24 2340–2520: sağ yan sacı delip fırın bölgesine 20 mm taşıyordu)"))
    ekle("teknik_din_rayi_guc", kut(1590.0, 1654.0, TEK_TASI + 10.0, TEK_TASI + 45.0, -178.0, -162.8), "sac",
         bom=("DIN ray TS35 × 7,5 + 7,7 mm ara parça · güç kaynağı", 1, "EN 60715 · 64 mm", "güç kaynağı UPS'ten 7,7 mm sığ → ray ara parçayla öne alınır"))
    ekle("teknik_din_plakasi", kut(1588.0, 1797.0, TEK_TASI, TEK_TASI + 110.0, -180.0, -178.0), "sac",
         bom=("DIN montaj plakası 304 2 mm", 1, "209 × 110 · arka taşıyıcının üstüne L büküm + 2 × M6 (v25b)", "UPS + güç kaynağı raylarını taşır"))''')
# 12.2 · ön yüz: mekanizma kanatları 788 · T yarıkları · tava panel menteşesi kol + taban · mandallar · T sol köşebentleri
d('    MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(1553.5), yl(1859.0))',
  '    MEK_Y = (yl(791.0), yl(1107.5)); T_Y = (yl(1553.5), yl(1859.0))\n'
  '    MEK_PY = (yl(MEK_PAN_Y0), yl(1107.5))                                        # v25b · kanatlar 788\'den (çerçeve 791\'den; kanadın alt dönüşü çerçevenin altında)')
d('            _yar.append((_xg, _xg + 60.0, 690.0 + 10.0 * _yg, 694.0 + 10.0 * _yg))',
  '            _yar.append((_xg, _xg + 60.0, T_YARIK_Y[0] + 10.0 * _yg, T_YARIK_Y[0] + 4.0 + 10.0 * _yg))   # v25b: alt sıra T alt kaydının önünden çekildi (denetim_C bulgu 9)')
d('            _yar.append((_xg, _xg + 60.0, 870.0 + 10.0 * _yg, 874.0 + 10.0 * _yg))',
  '            _yar.append((_xg, _xg + 60.0, T_YARIK_Y[1] + 10.0 * _yg, T_YARIK_Y[1] + 4.0 + 10.0 * _yg))   # v25b: üst sıra T üst kaydının önünden çekildi')
d('    PAN = [("onyuz_mekanizma_kanadi_sol", (xl(701.5), xl(1597.75), MEK_Y[0], MEK_Y[1]), (), "sol", 57.0),\n'
  '           ("onyuz_mekanizma_kanadi_sag", (xl(1600.75), xl(2497.0), MEK_Y[0], MEK_Y[1]), (), "sag", 57.0),',
  '    PAN = [("onyuz_mekanizma_kanadi_sol", (xl(701.5), xl(1597.75), MEK_PY[0], MEK_PY[1]), (), "sol", 57.0),\n'
  '           ("onyuz_mekanizma_kanadi_sag", (xl(1600.75), xl(2497.0), MEK_PY[0], MEK_PY[1]), (), "sag", 57.0),')
d('"kaide bandını (791–892) da örter, alttan açılmaz"', '"kaide bandını (788–892) da örter, alt kenar 788 = A alt paneli (basamak yok), alttan açılmaz"')
d('''            ekle("%s_mentese_%d" % (_a, _j), kut(_xm[0], _xm[1], _ym, _ym + 70.0, Z_PAN_C[0], Z_ON - 1.5), "celik",
                 bom=("Gizli menteşe 90° · EMKA 1006-U1-PC (tava panel)", 6, "AISI 304 · çerçeveye + panele kaynak · dışarıdan sökülemez (emka.com)",
                      "ölçü VARSAYIM (25 × 70 × 18,5 zarf) — A kabini ile aynı ürün") if _a.endswith("kanadi_sol") and _j == 0 else None)''',
  '''            ekle("%s_mentese_%d" % (_a, _j), kut(_xm[0], _xm[1], _ym, _ym + 70.0, Z_PAN_C[0] + 3.0, Z_ON - 1.5), "celik",
                 bom=("Gizli menteşe · ÇOK KOLLU, sanal dönme merkezi panelin ön dış köşesi (tava panel)", 6, "AISI 304 · kol panele kaynak, taban çerçeveye M5 · dışarıdan görünmez · ürün + parça no VARSAYIM",
                      "v25b · denetim_C bulgu 2: EMKA 1006 sınıfı pim menteşede (eksen 7 / 7) köşe komşu derze 2,9 mm taşar → A / F paneline 0,1 mm kalır; sanal pivot ön dış köşede taşma 0 · ölçü VARSAYIM (25 × 70 × 18,5 zarf)") if _a.endswith("kanadi_sol") and _j == 0 else None)
            _xt = (_x0 + 20.5, _x0 + 27.5) if _mt == "sol" else (_x1 - 27.5, _x1 - 20.5)                        # v25b · menteşe tarafı dönüşün süpürme dairesi (r 20,06) DIŞINDA
            ekle("%s_mentese_%d_taban" % (_a, _j), kut(_xt[0], _xt[1], _ym, _ym + 70.0, Z_PAN_C[0], Z_PAN_C[0] + 3.0), "celik", bom=None)   # v25b · gövde tarafı (çerçeveye M5)''')
d('        _xb = (_x1 - 11.0, _x1 - 2.0) if _mt == "sol" else (_x0 + 2.0, _x0 + 27.0)\n'
  '        _yb = (_y0 + 196.0, _y0 + 216.0) if "mekanizma" in _a else (_y0 + 108.5, _y0 + 138.5)',
  '        _xb = (_x1 - 27.0, _x1 - 2.0) if _mt == "sol" else (_x0 + 2.0, _x0 + 27.0)                  # v25b: üç mandal aynı 25 mm (sol kanat 9 mm idi) · derze simetrik\n'
  '        _yb = (yl(1082.5), yl(1102.5)) if "mekanizma" in _a else (_y0 + 108.5, _y0 + 138.5)          # v25b: mekanizma mandalları ÜST KAYITTA (tam oturur; orta dikme 30 genişlikte ikisini taşımaz)')
d('                                   "gizli menteşe + bas-aç mandallar bu çerçeveye") if _i == 0 else None)\n',
  '                                   "gizli menteşe + bas-aç mandallar bu çerçeveye") if _i == 0 else None)\n'
  '    for _i, _yk in enumerate((yl(1600.0), yl(1790.0))):                         # v25b · T SOL DİKMESİ köşebentle TU dikey ayırma sacına (denetim_C bulgu 7: 976 mm çerçeve yalnız sağdan taşınıyordu)\n'
  '        _L = kut(xl(1521.5), xl(1524.5), _yk, _yk + 40.0, -20.0, Z_CER_C[0]).union(kut(xl(1521.5), xl(1551.5), _yk, _yk + 40.0, Z_CER_C[0] - 3.0, Z_CER_C[0]))\n'
  '        ekle("onyuz_cerceve_T_sol_kosebendi_%d" % _i, _L, "celik",\n'
  '             bom=("T sol dikme köşebendi L 3 mm AISI 304 (40 boy)", 2, "dik kol dikey ayırma sacının sağ yüzüne 2 × M5 (sac üstte TC tavanına kaynaklı) · yatay kol T sol dikmesinin arkasına kaynak",\n'
  '                  "v25b · bas-aç mandal T sol dikmesinde → 50 N basıda serbest uç esnemesi ≈ 3–4 mm idi (denetçi tahmini); şimdi iki noktadan taşınır") if _i == 0 else None)\n')
# 12.3 · eski v1 soğuk hücre + ön kapak BOM'dan çıkar (adlar montaj süzgeci için korunur)
d('    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------',
  '    # v25b · denetim_C bulgu 12: montajın düşürdüğü v1 soğuk hücresi (pu_*, ic_kabuk) + eski ön kapak (on_kapak, on_kapak_pu, kapak_contasi) BOM\'dan çıktı —\n'
  '    #        soğuk paket tek kaynak TU v14 · ADLAR montaj süzgeçleri (V1_CIKAN / KAPAK) bozulmasın diye KORUNDU (parçalar montajda zaten görünmez)\n'
  '    for p in PARCALAR:\n'
  '        if p["ad"].startswith("pu_") or p["ad"] in ("ic_kabuk", "on_kapak", "on_kapak_pu", "kapak_contasi"):\n'
  '            p["bom"] = None\n\n'
  '    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------')
# 12.4 · dünya denetimi
d('BEYAZ_HAVADA = [("TU:kasar_cad_v14__", "kaşar kasetinin kendi dönen parçaları (helezon çekirdeği, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): kasar_cad_v14 üretecindeki yatak burcu boşluğu 0,10–0,15 mm — idealleştirilmiş temas (bilyeli ray ara elemanı gibi); kaset üreteci bu işin dışında"),',
  'BEYAZ_HAVADA_TOL = 0.26            # v25b · denetim_C bulgu 4: beyaz liste AÇIKLIKLA sınırlı — bileşen bu açıklıkla (ölçüldü 0,10–0,25) köke bağlanmalı, yoksa KALAN\n'
  'BEYAZ_HAVADA = [("TU:kasar_cad_v14__", "kaşar kasetinin kendi dönen parçaları (helezon çekirdeği, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): kasar_cad_v14 üretecindeki yatak burcu / geçme boşlukları 0,10–0,25 mm — 0,26 mm açıklıkla köke bağlanıyor (dünya denetimi ölçer); kaset üreteci bu işin dışında"),')
d('                ("TU:sucuk_cad_v7__", "sucuk kasetinin kendi dönen parçaları (helezon A–D + çekirdek, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): sucuk_cad_v7 yatak burcu boşluğu 0,10–0,15 mm — idealleştirilmiş temas"),\n'
  '                ("TU:motor_kablosu_", "motor kablo ucu (esnek, motor konnektörüne takılı) — STEP\'teki kablo çıkışı gövdeden 0,7 mm")]',
  '                ("TU:sucuk_cad_v7__", "sucuk kasetinin kendi dönen parçaları (helezon A–D + çekirdek, karıştırıcı mili, örümcek + çubuklar, kilit pimi, topuz): sucuk_cad_v7 yatak / geçme boşlukları 0,10–0,25 mm — "\n'
  '                 "örümcek_orta ↔ çubuklar 0,15 mm RİJİT birleşim (kaynak / geçme olmalı: kaset üretecine iş) · 0,26 mm açıklıkla köke bağlanıyor")]   # v25b: motor kabloları rakorla bağlandı (TU v14b), listeden çıktı')
d('    PANEL = {"TC:onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, 791.0, 1107.5), "TC:onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, 791.0, 1107.5),',
  '    PANEL = {"TC:onyuz_mekanizma_kanadi_sol": (701.5, 1597.75, MEK_PAN_Y0, 1107.5), "TC:onyuz_mekanizma_kanadi_sag": (1600.75, 2497.0, MEK_PAN_Y0, 1107.5),')
d('    derz = 1795.5 * 3.0 + 3.0 * 316.5 + 3.0 * 748.5 + 975.5 * 3.0 ',
  '    derz = 1795.5 * 3.0 + 3.0 * (1107.5 - MEK_PAN_Y0) + 3.0 * 748.5 + 975.5 * 3.0 ')
d('    top = (2497.0 - 701.5) * (1859.0 - 791.0)', '    top = (2497.0 - 701.5) * (1859.0 - MEK_PAN_Y0)')
d('C önü %.0f mm² (x 701,5–2497 · y 791–1859)', 'C önü %.0f mm² (x 701,5–2497 · y 788–1859, v25b: kanatlar 788 = A alt paneli)')
bolum('    kal, bl = [], {}\n    for c_ in hv["bilesen"]:\n', '    k("havada parça: %d parça · kök %d · bağlı %d · beyaz liste %s · KALAN %d" % (hv["parca"], hv["kok"], hv["bagli"], bl, len(kal)), not kal, str(kal[:10]))',
      '''    aday = [c_ for c_ in hv["bilesen"] if any(all(u.startswith(p_) for u in c_["uye"]) for p_, _n in BEYAZ_HAVADA)]
    kal = [c_["en"] for c_ in hv["bilesen"] if c_ not in aday]
    kal2 = []
    if aday:                                                                   # v25b · beyaz liste açıklıkla sınırlı: aynı dünya BEYAZ_HAVADA_TOL ile yeniden ölçülür
        hv2 = DT.havada(W_, zemin_y=DY_D, tol=BEYAZ_HAVADA_TOL)
        k2 = {u for c_ in hv2["bilesen"] for u in c_["uye"]}
        kal2 = [c_["en"] for c_ in aday if any(u in k2 for u in c_["uye"])]
    k("havada parça: %d parça · kök %d · bağlı %d · KALAN %d · beyaz liste (yalnız kaset iç dönen parçaları: %d bileşen / %d parça) %.2f mm açıklıkla köke bağlı %d · bağlanamayan %d"
      % (hv["parca"], hv["kok"], hv["bagli"], len(kal), len(aday), sum(len(c_["uye"]) for c_ in aday), BEYAZ_HAVADA_TOL, len(aday) - len(kal2), len(kal2)),
      not kal and not kal2, str((kal + kal2)[:10]))''')
d('        kas = [sh for a, sh in W_ if a.startswith("TU:" + mod + "__")]\n'
  '        st = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(("TU:" + mod + "__", ',
  '        kas = [sh for a, sh in W_ if a.startswith(("TU:" + mod + "__", "TU:" + mod + "_yarik_dili"))]                  # v25b: yarık dili kasetle çıkar\n'
  '        st = [(a, sh, B_[a]) for a, sh in W_ if not a.startswith(("TU:" + mod + "__", "TU:" + mod + "_yarik_dili", ')
d('TC + TU + itici sabitlerine değmiyor · 430 çerçeve çentiği fitilin içinde"', 'TC + TU + itici sabitlerine değmiyor · yarık dili raf / ön büküm / alt PU / çerçeve çentiğinden birlikte çıkar"')
bolum('    tk = [(a, round(B_[a].ymin, 2)) for a in B_ if a.startswith("TC:teknik_") and not a.startswith("TC:teknik_din_rayi")]\n',
      '      all(abs(v - 1553.5) < 0.01 for a, v in tk) and max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01)',
      '''    TEK_BEK = {"TC:teknik_tasiyici_0": 1554.5, "TC:teknik_tasiyici_1": 1554.5, "TC:teknik_sogutma_grubu": TEK_TASIYICI_Y + TEK_TAKOZ, "TC:teknik_pano_kutusu": TEK_TASIYICI_Y + TEK_TAKOZ,
               "TC:teknik_ups": TEK_TASIYICI_Y, "TC:teknik_guc_kaynagi": TEK_TASIYICI_Y, "TC:teknik_din_plakasi": TEK_TASIYICI_Y}
    tk = [(a, round(B_[a].ymin, 2), v) for a, v in TEK_BEK.items()]
    _S = dict(W_)
    _mt = lambda a_, c_: (lambda d_: d_.Value() if d_.IsDone() else 99.0)(DSS(_S[a_].wrapped, _S[c_].wrapped))
    _tt = [(a.split(":")[1] + "↔" + c.split(":")[1], round(_mt(a, c), 3)) for a, c in (("TC:teknik_tasiyici_0", "TC:dis_yan_sag"), ("TC:teknik_tasiyici_0", "TU:teknik_ayirma_saci_dikey"),
                                                                                    ("TC:teknik_tasiyici_1", "TC:dis_yan_sag"), ("TC:teknik_tasiyici_1", "TU:teknik_ayirma_saci_dikey"))]
    k("v25b · teknik cep: ağır parçalar 2 × L 30×30×3 TAŞIYICI üstünde (uçları TC sağ yan sacı + dikey ayırma sacı · yatay sacın 1 mm üstünde → PU'ya yük yok) · soğutma grubu + pano titreşim takozunda: %s · uç temasları %s · DIN rayları x ≤ 2497 (%.1f)"
      % ([(a.split(":")[1], y_) for a, y_, v in tk], _tt, max(B_[a].xmax for a in B_ if "din_rayi" in a)),
      all(abs(y_ - v) < 0.01 for a, y_, v in tk) and all(d_ <= 0.05 for a, d_ in _tt) and max(B_[a].xmax for a in B_ if "din_rayi" in a) <= 2497.01)
    # 8b · v25b · SOĞUK ODA TABANI + ÇERÇEVE BANDI (denetim_C bulgu 1 · KRİTİK): ürün kanalları dışında doğrudan boşluk = 0
    _ak, _akl = TU.soguk_taban_kacagi(W_, DX_D, -168.0)
    k("v25b · soğuk oda ↔ mekanizma bandı: raf dilimi (dünya y 1149,5–1151,5) %d ürün kanalı DIŞINDA açık alan %.2f mm² ≤ 1 (v25: ≈ 21 350)" % (len(TU.KANAL), _ak), _ak <= 1.0,
      str([(round(a_, 2), round(b_.xmin), round(b_.zmin)) for a_, b_ in _akl if a_ > 0.01][:6]))
    _ab2, _abl = TU.cerceve_bandi_acik(W_, DX_D, -168.0)
    k("v25b · 430 çerçeve düzlemi soğuk oda altı bandında (dünya y 1109–1152) kesintisiz (kaset çentikleri yarık dili flanşıyla kapalı): açık alan %.2f mm² ≤ 1" % _ab2, _ab2 <= 1.0,
      str([(round(a_, 2), round(b_.xmin), round(b_.ymin)) for a_, b_ in _abl if a_ > 0.01][:6]))
    # 8c · v25b · KAPAK AÇILMA TARAMASI (denetim_C bulgu 2): 5 kapak · sanal pivot ön dış köşe · diğer kapaklar KAPALI · A kabini + F ön zarfı engel
    ENGEL = [("F:fırın + üst kabin ön zarfı (x ≥ 2500, z ≤ +79)", kut(2500.0, 4000.0, 788.0, 1862.0, -D, Z_ON).val())]
    try:
        import acici_kabin_cad_v1 as AK
        AK.kur(); ENGEL += [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR]
    except Exception as e_:
        ENGEL.append(("A:ön zarf (x ≤ 698,5, z ≤ +79)", kut(0.0, 698.5, 788.0, 1862.0, -D, Z_ON).val())); print("  BİLGİ · A kabini yüklenemedi → A ön zarfı kutu (%s)" % str(e_)[:80])
    for kn in ("K1", "K2"):
        _kt = TU.kapak_tarama(W_ + ENGEL, kn, DX_D)
        k("v25b · %s AÇILMA TARAMASI 0–110° (%d açı · sanal pivot ön dış köşe%s · A kabini %d parça + F zarfı engel): çakışma %d"
          % (kn, len(TU.ACI_TARAMA), " · flipper katlanır min(90, %.0f·α) · K2 KAPALI" % TU.FLIP_K if kn == "K1" else " · K1 + flipper KAPALI", len(ENGEL) - 1, len(_kt)), not _kt, str(_kt[:6]))
    for ad in PAN_DON:
        hn = ("TC:" + ad, "TC:" + ad + "_omega", "TC:" + ad + "_mentese_0", "TC:" + ad + "_mentese_1")
        har_p = [(a, sh) for a, sh in W_ if a in hn]
        sab_p = [(a, sh, sh.BoundingBox()) for a, sh in W_ + ENGEL if a not in hn]
        bul_p = []
        for aci in TU.ACI_TARAMA:
            for a, sh in har_p:
                m = panel_don(sh, ad, aci); mb = m.BoundingBox()
                for c, sc, bc in sab_p:
                    if not _bbk(mb, bc): continue
                    v = _hacim(m, sc)
                    if v > 1.0 or v < 0: bul_p.append((aci, a, c, round(v, 1)))
        k("v25b · %s AÇILMA TARAMASI 0–110° (%d açı · sanal pivot ön dış köşe x %.1f · diğer kapaklar kapalı · A + F engel): çakışma %d" % (ad.replace("onyuz_", ""), len(TU.ACI_TARAMA), PAN_DON[ad][0], len(bul_p)),
          not bul_p, str(bul_p[:6]))
    # 8d · v25b · HAZNE DOLUM ÇEKMESİ (denetim_C bulgu 13): TC kelepçe sökülür, hazne 20 mm kaldırılır, 0–640 öne (K1 + flipper + K2 açık)
    for kk in ("kiyma", "kusbasi"):
        hn = ("TU:%s_hazne_bizim" % kk, "TU:%s_hazne_boynu" % kk)
        har_h = [(a, sh) for a, sh in W_ if a in hn]
        sab_h = [(a, sh, B_[a]) for a, sh in W_ if a not in hn and a != "TU:%s_tc_kelepce_hazne" % kk and not a.startswith(("TU:onyuz_K1_", "TU:onyuz_K2_", "TU:onyuz_flipper"))]
        bul_h = []; dz = 0.0
        while dz <= 640.0 + 1e-6:
            for a, sh in har_h:
                s2 = sh.translate(cq.Vector(0.0, 20.0, dz)); b2 = s2.BoundingBox()
                for c, sc, bc in sab_h:
                    if _bbk(b2, bc):
                        v = _hacim(s2, sc)
                        if v > 1.0 or v < 0: bul_h.append((dz, a, c, round(v, 1)))
            dz += 20.0
        k("v25b · %s haznesi DOLUM ÇEKMESİ: TC kelepçe sökülür → hazne 20 mm kaldırılır → 0–640 mm öne (K1 + flipper + K2 açık): serbest (bulgu %d)" % (kk, len(bul_h)), not bul_h, str(bul_h[:6]))
    # 8e · v25b · BAĞLANTILAR (bulgu 3 · 7 · 8 · 11 + kılavuz + panel menteşeleri): hepsi ≤ 0,05 mm
    _bg = [("TU:onyuz_mentese_tabani_K1_mentese_0", "TC:dis_yan_sol"), ("TU:onyuz_mentese_tabani_K1_mentese_1", "TC:dis_yan_sol"),
           ("TU:onyuz_mentese_tabani_K2_mentese_0", "TC:dis_yan_sag"), ("TU:onyuz_mentese_tabani_K2_mentese_1", "TC:dis_yan_sag"),
           ("TC:onyuz_cerceve_T_sol_kosebendi_0", "TU:teknik_ayirma_saci_dikey"), ("TC:onyuz_cerceve_T_sol_kosebendi_0", "TC:onyuz_cerceve_T_sol_dikme"),
           ("TC:onyuz_cerceve_T_sol_kosebendi_1", "TU:teknik_ayirma_saci_dikey"), ("TC:onyuz_cerceve_T_sol_kosebendi_1", "TC:onyuz_cerceve_T_sol_dikme"),
           ("IT:montaj_kirisi", "TU:soguk_duvar_sag_alt_profili"), ("TU:soguk_duvar_sag_alt_profili", "TC:dis_yan_sag"),
           ("TU:onyuz_kilavuz_flipper", "TU:tasiyici_raf_3mm"), ("TC:teknik_takoz_0", "TC:teknik_tasiyici_0"), ("TC:teknik_takoz_0", "TC:teknik_sogutma_grubu"),
           ("TC:teknik_takoz_6", "TC:teknik_pano_kutusu"), ("TC:teknik_din_plakasi", "TC:teknik_tasiyici_1"), ("TC:teknik_ups", "TC:teknik_din_rayi_ups"), ("TC:teknik_din_rayi_ups", "TC:teknik_din_plakasi"),
           ("TC:onyuz_mekanizma_kanadi_sol_mentese_0", "TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban"), ("TC:onyuz_mekanizma_kanadi_sol_mentese_0_taban", "TC:onyuz_cerceve_mek_sol_dikme"),
           ("TC:onyuz_mekanizma_kanadi_sol_basac", "TC:onyuz_cerceve_mek_ust_kayit"), ("TC:onyuz_mekanizma_kanadi_sag_basac", "TC:onyuz_cerceve_mek_ust_kayit"),
           ("TU:kasar_cad_v14_yarik_dili", "TU:kasar_cad_v14__cikis_tupu"), ("TU:motor_kablosu_kasar_cad_v14_helezon", "TU:motor_kasar_cad_v14_helezon")]
    _bd = [(a.split(":")[1], c.split(":")[1], round(_mt(a, c), 3)) for a, c in _bg]
    k("v25b · bağlantılar (%d çift: K1/K2 menteşe tabanı ↔ TC yan sacı · T köşebendi ↔ dikey sac + dikme · itici kirişi ↔ sağ duvar alt profili ↔ TC yan sacı · kılavuz ↔ raf · takoz · DIN plakası · panel menteşesi · mandallar · yarık dili · kablo rakoru): hepsi ≤ 0,05 mm"
      % len(_bg), all(d_ <= 0.05 for a, c, d_ in _bd), str([x for x in _bd if x[2] > 0.05][:6]))''')
d('b.ymin < ((791.0 - DY_D) if a.startswith("onyuz_") else 0.0) - 0.01', 'b.ymin < ((MEK_PAN_Y0 - DY_D) if a.startswith("onyuz_") else 0.0) - 0.01')

io.open(os.path.join(U, CIKIS), "w", encoding="utf-8").write(s)
compile(s, CIKIS, "exec")
print("%s yazildi (%d satir)" % (CIKIS, s.count("\n") + 1))
