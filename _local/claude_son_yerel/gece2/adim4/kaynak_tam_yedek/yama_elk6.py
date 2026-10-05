# -*- coding: utf-8 -*-
import io, os
H3 = r"@@KOK_W@@\b3\arastirma\_uretec\h3"
P = os.path.join(H3, "h3_elk_ist_v1.py")
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:100], s.count(a))
    s = s.replace(a, b)


# 1 · araba zarfı ölçülen parçalarla: ön yüz z −3,8'e kadar (kaset bandı yay kutusu) · bayrak çizgisi y 932 üstü; altı yalnız kızak bölgesi (z ≤ −35)
rep('''TOPPING_ZARF = kut(930.0, 2500.0, 912.0, 1045.0, -320.0, -20.0)                              # araba plakası + kızak ayakları + kaset (x 936 → aktarma)
TOPPING_ZARF_MOTOR = kut(1055.0, 2500.0, 898.0, 942.0, -200.0, -140.0)                       # tekneye sarkan dönüş motoru''',
    '''TOPPING_ZARF = kut(890.0, 2520.0, 931.0, 1045.0, -345.0, -3.0)                               # bayrak + apron + araba plakası + kaset bandı (x 896 → aktarma +1279)
TOPPING_ZARF_KIZAK = kut(890.0, 2520.0, 912.0, 931.0, -345.0, -35.0)                          # kızak ayakları (ön şerit z > −35 serbest: sensörler)
TOPPING_ZARF_MOTOR = kut(1050.0, 2400.0, 898.0, 942.0, -200.0, -140.0)                       # tekneye sarkan dönüş motoru''')
rep('''    ER.ekli_ekle("YASAK_TOPPING_araba_zarfi", TOPPING_ZARF); ER.ekli_ekle("YASAK_TOPPING_donus_motoru_zarfi", TOPPING_ZARF_MOTOR)''',
    '''    ER.ekli_ekle("YASAK_TOPPING_araba_zarfi", TOPPING_ZARF); ER.ekli_ekle("YASAK_TOPPING_kizak_zarfi", TOPPING_ZARF_KIZAK)
    ER.ekli_ekle("YASAK_TOPPING_donus_motoru_zarfi", TOPPING_ZARF_MOTOR)''')
# 2 · motor → sürücü sırası: en uzaktaki önce
rep('''    SUR = [(1482.0, "kasar_helezon", (2062.0, 1141.5, -807.0)), (1515.0, "kasar_rotor", (2062.0, 1296.5, -807.0)),
           (1548.0, "sucuk_helezon", (2311.0, 1161.5, -807.0)), (1581.0, "sucuk_rotor", (2311.0, 1265.5, -807.0))]
    for i, (xs, nm, S) in enumerate(SUR):''',
    '''    SUR = [(1581.0, "sucuk_rotor", (2311.0, 1265.5, -807.0)), (1548.0, "sucuk_helezon", (2311.0, 1161.5, -807.0)),
           (1515.0, "kasar_rotor", (2062.0, 1296.5, -807.0)), (1482.0, "kasar_helezon", (2062.0, 1141.5, -807.0))]
    for i, (xs, nm, S) in enumerate(SUR):''')
# 3 · valf adası: hava hortumlarının bağlandığı sol uç değil SAĞ uç (çok pinli soket) · hava adasının üstünden KD1 sol yüzüne
rep('''    cihaz("TOPPING_valf_adasi", (1690.0, 1280.0, -710.0), PANO(1660.0, -790.0), 4.5, "C", itme=(0, -6.0), on=PANO_ON(1660.0, -790.0),
          bolge=BOLGE_KURU, bom=("Valf adası çok damarlı kablo 25 × 0,34 (D-sub → pano)", 1, "", ""))''',
    '''    cihaz("TOPPING_valf_adasi", (1998.0, 1295.0, -744.0), (2420.8, 1295.0, -808.0), 4.5, "C", itme=(0, 5.0), on=(2400.0, 1295.0, -808.0),
          bolge=BOLGE_KURU, bom=("Valf adası çok damarlı kablo 25 × 0,34 (D-sub → KD1 → pano)", 1, "", ""))''')
# 4 · x sağ limit: sensör önünden yukarı (bayrağın altı, y 927) → öne (z 5, arabanın önü) → sağa → cepte dik → KD1
rep('''    sabit("TOPPING_sensor_x_limit_sag", [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2455.0, 920.0, -16.0), (2455.0, 1076.0, -16.0),
                                           (2455.0, 1076.0, -795.0), (2449.2, 1076.0, -795.0)], 2.0, "C")''',
    '''    sabit("TOPPING_sensor_x_limit_sag", [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2375.0, 927.0, -16.0), (2375.0, 927.0, 5.0), (2455.0, 927.0, 5.0),
                                           (2455.0, 1076.0, 5.0), (2455.0, 1076.0, -795.0), (2449.2, 1076.0, -795.0)], 2.0, "C")''')
# 5 · F motor yolu fırın gövde sacında (rakor) bölünür (rakor kabloyu tutar)
rep('''    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.8), (2780.0, 1121.5, -800.0), (2449.2, 1121.5, -800.0)], 4.0, "F",''',
    '''    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.8), (2780.0, 1121.5, -651.0), (2780.0, 1121.5, -800.0), (2449.2, 1121.5, -800.0)], 4.0, "F",''')
# 6 · A emniyet sensörleri: kablo alt / üst uçtan (gövdenin arka yüzü değil)
rep('''    sabit("A_emniyet_ust", [(1386.5, 1594.0, 28.8), (1386.5, 1594.0, 0.0), (1414.0, 1594.0, 0.0), (1414.0, 1594.0, -9.8)], 2.5, "A", bom=AK_BOM)
    sabit("A_emniyet_alt", [(1386.5, 954.0, 28.8), (1386.5, 954.0, 6.0), (1386.5, 1100.0, 6.0), (1414.0, 1100.0, 6.0), (1414.0, 1100.0, -7.8)], 2.5, "A")''',
    '''    sabit("A_emniyet_ust", [(1386.5, 1539.7, 42.0), (1386.5, 1530.0, 42.0), (1386.5, 1530.0, 0.0), (1414.0, 1530.0, 0.0), (1414.0, 1530.0, -7.8)], 2.5, "A", bom=AK_BOM)
    sabit("A_emniyet_alt", [(1386.5, 1008.5, 42.0), (1386.5, 1020.0, 42.0), (1386.5, 1020.0, 6.0), (1386.5, 1100.0, 6.0), (1414.0, 1100.0, 6.0),
                            (1414.0, 1100.0, -7.8)], 2.5, "A")''')
# 7 · x sol limit / x sıfır: teknenin ön şeridinde (y 920 / 902, z −13) sola, arabanın solunda (x 886 / 880) yukarı, açıcının üstünden (y 1150 / 1160) sağa → A kanalı
rep('''    sabit("TOPPING_sensor_x_limit_sol", [(1056.0, 920.0, -18.7), (1056.0, 920.0, -16.0), (1056.0, 1150.0, -16.0), (1056.0, 1150.0, 49.5), (1390.0, 1150.0, 49.5),
                                         (1390.0, 1150.0, 0.0), (1409.0, 1150.0, 0.0), (1409.0, 1150.0, -7.8)], 2.0, "C")
    sabit("TOPPING_sensor_x_home", [(1086.0, 920.0, -18.7), (1086.0, 920.0, -16.0), (1086.0, 1140.0, -16.0), (1086.0, 1140.0, 49.5), (1395.0, 1140.0, 49.5),
                                    (1395.0, 1140.0, 0.0), (1416.0, 1140.0, 0.0), (1416.0, 1140.0, -7.8)], 2.0, "C")''',
    '''    sabit("TOPPING_sensor_x_limit_sol", [(1056.0, 920.0, -18.7), (1056.0, 920.0, -13.0), (886.0, 920.0, -13.0), (886.0, 1150.0, -13.0), (1390.0, 1150.0, -13.0),
                                         (1390.0, 1150.0, 0.0), (1409.0, 1150.0, 0.0), (1409.0, 1150.0, -7.8)], 2.0, "C")
    sabit("TOPPING_sensor_x_home", [(1086.0, 920.0, -18.7), (1086.0, 920.0, -13.0), (1086.0, 902.0, -13.0), (880.0, 902.0, -13.0), (880.0, 1160.0, -13.0),
                                    (1395.0, 1160.0, -13.0), (1395.0, 1160.0, 0.0), (1416.0, 1160.0, 0.0), (1416.0, 1160.0, -7.8)], 2.0, "C")''')
# 8 · K klemens: alt yüz yerine ÖN yüz (klemens önden bağlanır; altından hava giriş hortumu geçiyor)
rep('''    KT = lambda i: (4176.0 + 8.6 * i, 1615.8, -786.0)                       # klemens sırası alt yüzü (x 4172–4255)
    KT_ON = lambda i: (4176.0 + 8.6 * i, 1598.0 - 10.0 * (i % 2), -786.0)''',
    '''    KT = lambda i: (4176.0 + 8.6 * i, 1640.0, -761.3)                       # klemens sırası ön yüzü (x 4172–4255 · y 1616–1664)
    KT_ON = lambda i: (4176.0 + 8.6 * i, 1640.0, -745.0 + 8.0 * (i % 2))''')
io.open(P, "w", encoding="utf-8").write(s)
# voksel sınırı
P2 = os.path.join(H3, "h3_elk_voksel.py")
t = io.open(P2, encoding="utf-8").read()
a = '        if say > 8000000: return None, "A* sınırı"'
assert t.count(a) == 1
t = t.replace(a, '        if say > 12000000: return None, "A* sınırı"')
io.open(P2, "w", encoding="utf-8").write(t)
print("tamam")
