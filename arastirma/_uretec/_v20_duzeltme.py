# -*- coding: utf-8 -*-
"""yap_topping_v20'ye ikinci tur duzeltmeler — cakisma taramasindan cikanlar."""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(U, "yap_topping_v20.py")
s = io.open(p, encoding="utf-8").read()
EK = []

# ------------------------------------------------------------------ 1) DISKTE PIM DELIKLERI
EK.append((
    '''    ekle("calisma_diski", _dsk, "pom",''',
    '''    for i_ in range(3):                                                     # pim delikleri
        a_ = math.radians(120.0 * i_)
        _dsk = _dsk.cut(sily(Xc + 100.0 * math.cos(a_), ZT + 100.0 * math.sin(a_), 4.1, 99.0, 109.0))
    ekle("calisma_diski", _dsk, "pom",'''))

# ------------------------------------------------------------------ 2) KILIT DELIGI GERCEKTEN DELIK OLSUN
EK.append((
    '''    for i_ in range(3):
        a_ = math.radians(120.0 * i_ + 40.0)
        ekle("kilit_deligi_%d" % i_, sily(Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_), 5.0, 80.4, 86.4), "celik",
             bom=("Kilit deliği Ø10 · burçlu", 3, "ayar bileziğinde · sertleştirilmiş burç",
                  "açıcının altında gövdeye bağlı pim girer, tabla dönmez. "
                  "DOZAJ HIZINA DOKUNULMADI — kilit yalnız açma anında") if i_ == 0 else None)''',
    '''    for i_ in range(3):                                                     # burc: delik ayar bileziginde ACILIR
        a_ = math.radians(120.0 * i_ + 40.0)
        _bx, _bz = Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_)
        ekle("kilit_burcu_%d" % i_, sily(_bx, _bz, 7.0, 80.8, 86.0).cut(sily(_bx, _bz, 5.0, 80.0, 87.0)), "celik",
             bom=("Kilit burcu Ø14/Ø10", 3, "sertleştirilmiş 420 · ayar bileziğine presli",
                  "açıcının altında gövdeye bağlı pim buraya girer, tabla dönmez. "
                  "DOZAJ HIZINA DOKUNULMADI — kilit yalnız açma anında") if i_ == 0 else None)'''))

# ayar bileziginde delikleri ac
EK.append((
    "for e, y in D:",
    '''D.append((
    ''''''    ekle("ayar_bilezigi", sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0)), "celik",'''''',
    ''''''    _ab = sily(Xc, ZT, 105.0, 80.77, 86.0).cut(sily(Xc, ZT, 50.0, 79.8, 87.0))
    for i_ in range(3):                                                     # v20: kilit burcu delikleri
        a_ = math.radians(120.0 * i_ + 40.0)
        _ab = _ab.cut(sily(Xc + 92.0 * math.cos(a_), ZT + 92.0 * math.sin(a_), 7.0, 80.0, 87.0))
    ekle("ayar_bilezigi", _ab, "celik",''''''))

for e, y in D:'''))

# ------------------------------------------------------------------ 3) KOPRU DARALDI, BRAKETLER ASKIYA DONDU
EK.append((
    '''    AKT_Z0, AKT_Z1 = ZT - 180.0, ZT + 180.0''',
    '''    # KOPRU YALNIZ PIDENIN GENISLIGINI ORTER (Ø280 -> ZT +- 140), cunku ZT-180
    # bolgesinde X TAHRIK MOTORU var. 5 mm pay ile ZT +- 145.
    AKT_Z0, AKT_Z1 = ZT - 145.0, ZT + 145.0'''))
EK.append((
    '''    for i_, zb in enumerate((AKT_Z0 - 30.0, AKT_Z1 + 5.0)):
        ekle("kopru_braketi_%d" % i_, kut(AKT_X0, AKT_X1, AKT_Y, 200.0, zb, zb + 25.0), "sac",
             bom=("Köprü braketi", 2, "304 5 mm · iç kabuğa cıvatalı",
                  "tablanın Ø340 yolunun DIŞINDA (z ±180) — araba altından serbest geçer") if i_ == 0 else None)''',
    '''    # ASKI: kopru ASAGIDAN degil YUKARIDAN tasinir. Alttan destek koyacak yer yok —
    # araba oradan geciyor. Askilar tablanin Ø340 yolunun disinda (z -345 ve z +5).
    for i_, zb in enumerate((-350.0, 5.0)):
        ekle("kopru_askisi_%d" % i_, kut(AKT_X0 + 10.0, AKT_X1 - 15.0, AKT_Y, 245.0, zb, zb + 10.0)
             .union(kut(AKT_X0, AKT_X1 - 15.0, AKT_Y, AKT_Y + 25.0, zb, zb + 10.0)), "sac",
             bom=("Köprü askısı", 2, "304 10 mm lama · üstten iç kabuğa cıvatalı",
                  "köprüyü YUKARIDAN taşır; altta destek koyacak yer yok, araba oradan geçiyor. "
                  "Tablanın Ø340 yolunun dışında (z -350 ve z +5)") if i_ == 0 else None)'''))

# ------------------------------------------------------------------ 4) X TAHRIKI SOL UCA TASINDI
EK.append((
    '''io.open(os.path.join(U, "topping_cad_v20.py"), "w", encoding="utf-8").write(s)''',
    '''# ---- X TAHRIKI SOL UCA TASINIYOR
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
_y = ('_ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 66.0, -510.0, -1.0))   # mekanizma gecisi\\n'
      '        ekle("dis_yan_" + s, _ys, "sac",')
assert _e in s
s = s.replace(_e, _y, 1)

io.open(os.path.join(U, "topping_cad_v20.py"), "w", encoding="utf-8").write(s)'''))

for e, y in EK:
    assert e in s, "BULUNAMADI -> " + e[:70]
    s = s.replace(e, y, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("yap_topping_v20 ikinci tur duzeltmeler eklendi ·", len(EK))
