# -*- coding: utf-8 -*-
"""E mekanizma bileşenlerine AD verme (6 Eki 2026 · Claude · 2. oturum · görev 4.1 / 4.2)
Girdi: e_envanter.json (e_envanter.py · hat3_v10l bileşen numaraları). Çıktı: ../../../../arastirma/_uretec/h3/yama_v9/veri/e_mek_parcalar.json
  ad → {dug, lo, hi, aile, rol} — zincir adımları 81–85 bileşenleri bu KUTULARLA bulur (bileşen numarası değil); e_parca.py mekanizma
  parçalarını bu adlarla ayırır. Roller: tasiyici · motor · sensor · kayis · burc · vantuz · hortum · mil · parca (plaka / blok / braket / profil).
Kullanım: python e_mek_adlar.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.stdout.reconfigure(encoding='utf-8')
O = {r['i']: r for r in json.load(open('e_envanter.json', encoding='utf-8'))}
AD = {}
def ad(aile, isim, no, rol='parca', ek=()):
    """ek: aynı parçaya katılan ek bileşenler (üreteç ayrı katı yapmış: mil ucu, sensör kulakları)"""
    assert no in O, no; assert isim not in AD, isim
    for e in ek: assert e in O, e
    AD[isim] = dict(no=no, aile=aile, rol=rol, ek=list(ek))
# ---------------------------------------------------------------- KALIP (katlama kalıbı + yuva) · 44
ad('kalip', 'kalip_taban', 1385, 'tasiyici')
for i, n in enumerate((1352, 1353, 1362, 1363)): ad('kalip', 'kalip_kolon_%d' % i, n)                  # Ø40 kolon: sol arka / sol ön / sağ arka / sağ ön
ad('kalip', 'kalip_ust_plaka', 1386)
ad('kalip', 'kalip_duvar_sol', 1387); ad('kalip', 'kalip_duvar_sag', 1393); ad('kalip', 'kalip_duvar_arka', 1388)
for i, n in enumerate((1389, 1390, 1391, 1392)): ad('kalip', 'kalip_on_kilavuz_%d' % i, n)
for i, n in enumerate((1354, 1355, 1360, 1361)): ad('kalip', 'kalip_yatak_%d' % i, n)
for i, n in enumerate((1366, 1367, 1368, 1369)): ad('kalip', 'kalip_burc_%d' % i, n, 'burc')
ad('kalip', 'kalip_orta_blok', 1356); ad('kalip', 'kalip_motor_flansi', 1357); ad('kalip', 'kalip_motor', 1380, 'motor')
ad('kalip', 'kalip_kaplin', 1359); ad('kalip', 'kalip_rulman', 1375, 'burc'); ad('kalip', 'kalip_rulman_blogu', 1358)
ad('kalip', 'kalip_vida_mili', 1376, 'mil', ek=[1377]); ad('kalip', 'kalip_sensor_blogu', 1364)               # 1377: vida milinin alt muylusu (ayrı katı)
ad('kalip', 'kalip_sensor', 1394, 'sensor', ek=[1378, 1379])                                                  # fork sensörün kendi kulakları (çelik)
ad('kalip_yuva', 'kalip_yuva_cubuk', 1351); ad('kalip_yuva', 'kalip_yuva_somun', 1365, 'burc')
for i, n in enumerate((1370, 1371, 1372, 1373)): ad('kalip_yuva', 'kalip_yuva_mil_%d' % i, n, 'mil')
ad('kalip_yuva', 'kalip_yuva_bayrak', 1374)
for i, n in enumerate((1381, 1382, 1383, 1384)): ad('kalip_yuva', 'kalip_yuva_plaka_%d' % i, n)
# ---------------------------------------------------------------- KÖPRÜ · 15
ad('kopru', 'kopru_motor_blogu', 1396, 'tasiyici'); ad('kopru', 'kopru_tasiyici', 1397); ad('kopru', 'kopru_kaplin', 1398); ad('kopru', 'kopru_motor', 1407, 'motor')
ad('kopru', 'kopru_rulman_blogu', 1403); ad('kopru', 'kopru_vida_mili', 1406, 'mil'); ad('kopru', 'kopru_kilavuz_yatak_0', 1404, 'burc'); ad('kopru', 'kopru_kilavuz_yatak_1', 1405, 'burc')
ad('kopru', 'kopru_sensor_tutucu', 1399); ad('kopru', 'kopru_sensor', 1409, 'sensor'); ad('kopru', 'kopru_somun_blogu', 1400); ad('kopru', 'kopru_kizak', 1395)
ad('kopru', 'kopru_plaka', 1408); ad('kopru', 'kopru_kilavuz_mil_0', 1401, 'mil'); ad('kopru', 'kopru_kilavuz_mil_1', 1402, 'mil')
# ---------------------------------------------------------------- KAPAK KATLAMA · 43
ad('kapak', 'kapak_sasi', 1455, 'tasiyici'); ad('kapak', 'kapak_motor_dik_plaka', 1456); ad('kapak', 'kapak_motor_plakasi', 1457)
ad('kapak', 'kapak_disli_motor', 1484, 'motor', ek=[1485])                       # planet dişli kutusu + motor: fabrikada birleşik hazır ürün (giriş flanşı 38 × 38, NEMA 23 deseni yok)
ad('kapak', 'kapak_yatak_ayak_0', 1458); ad('kapak', 'kapak_yatak_ayak_1', 1459); ad('kapak', 'kapak_yatak_0', 1474); ad('kapak', 'kapak_yatak_1', 1475)
ad('kapak', 'kapak_tahrik_mili', 1476, 'mil'); ad('kapak', 'kapak_kol', 1587); ad('kapak', 'kapak_sensor_blogu_0', 1460); ad('kapak', 'kapak_sensor_0', 1490, 'sensor')
ad('kapak', 'kapak_sensor_blogu_1', 1461); ad('kapak', 'kapak_sensor_1', 1491, 'sensor')
ad('kapak', 'kapak_motor_blogu', 1462); ad('kapak', 'kapak_motor_alt', 1486, 'motor'); ad('kapak', 'kapak_yatak_plakasi', 1463); ad('kapak', 'kapak_rulman_yatagi', 1479, 'burc')
ad('kapak', 'kapak_kaplin', 1464); ad('kapak', 'kapak_motor_mili', 1481, 'mil'); ad('kapak', 'kapak_dik_mil', 1480, 'mil')
ad('kapak', 'kapak_profil_ayak_0', 1465); ad('kapak', 'kapak_profil_ayak_1', 1466); ad('kapak', 'kapak_profil_0', 1467); ad('kapak', 'kapak_profil_1', 1468)
ad('kapak', 'kapak_profil_kapak_0', 1469); ad('kapak', 'kapak_profil_kapak_1', 1470); ad('kapak', 'kapak_kilavuz_mil_0', 1482, 'mil'); ad('kapak', 'kapak_kilavuz_mil_1', 1483, 'mil')
ad('kapak', 'kapak_dik_rod_0', 1477, 'mil'); ad('kapak', 'kapak_dik_rod_1', 1478, 'mil'); ad('kapak', 'kapak_ust_plaka_0', 1488); ad('kapak', 'kapak_ust_plaka_1', 1489)
ad('kapak_katlayici', 'kapak_katlayici_gobek', 1471); ad('kapak_katlayici', 'kapak_katlayici_plaka', 1451); ad('kapak_katlayici', 'kapak_katlayici_kol', 1450)
ad('kapak_katlayici', 'kapak_katlayici_paleti', 1487); ad('kapak_katlayici', 'kapak_katlayici_blok_arka', 1452); ad('kapak_katlayici', 'kapak_katlayici_blok_on', 1454)
ad('kapak_katlayici', 'kapak_katlayici_pim', 1453, 'mil'); ad('kapak_katlayici', 'kapak_katlayici_kizak_0', 1472); ad('kapak_katlayici', 'kapak_katlayici_kizak_1', 1473)
# ---------------------------------------------------------------- KÖŞE (kaldırıcı çerçeve + 4 tutucu + piston) · 63
ad('kose', 'kose_sasi', 844, 'tasiyici'); ad('kose', 'kose_uc_blok_sol', 843); ad('kose', 'kose_uc_blok_sag', 845); ad('kose', 'kose_uc_yatak_sol', 851, 'burc'); ad('kose', 'kose_uc_yatak_sag', 862, 'burc')   # LM12 lineer burç: bloğa sıkı geçme (GEÇME)
ad('kose', 'kose_uc_kapak_sag', 865); ad('kose', 'kose_somun', 850, 'burc')
for i, n in enumerate((852, 857, 863, 864)): ad('kose', 'kose_sensor_braket_%d' % i, n)
KK = {'sol_arka': ('MF', 853, 855, 872, 877, (1559, 1562, 1560, 1561, 1563, 1564)), 'sol_on': ('PF', 854, 856, 873, 878, (1571, 1574, 1572, 1573, 1575, 1576)),
      'sag_arka': ('MB', 858, 860, 874, 879, (1565, 1568, 1566, 1567, 1569, 1570)), 'sag_on': ('PB', 859, 861, 875, 880, (1577, 1580, 1578, 1579, 1581, 1582))}
for k, (kod, k0, k1, mo, se, T) in KK.items():
    ad('kose', 'kose_kilavuz_%s_0' % k, k0); ad('kose', 'kose_kilavuz_%s_1' % k, k1); ad('kose', 'kose_motor_%s' % k, mo, 'motor'); ad('kose', 'kose_sensor_%s' % k, se, 'sensor')
    for isim, n in zip(('gobek', 'mil', 'kol', 'mafsal', 'cene', 'parmak'), T): ad('kose_tutucu', 'kose_tutucu_%s_%s' % (k, isim), n, 'mil' if isim == 'mil' else 'parca')
ad('kose_piston', 'kose_piston_kol', 846, 'tasiyici'); ad('kose_piston', 'kose_piston_plaka', 847); ad('kose_piston', 'kose_piston_motor_plakasi', 848); ad('kose_piston', 'kose_piston_kaplin', 849)
ad('kose_piston', 'kose_piston_mil_sol', 866, 'mil'); ad('kose_piston', 'kose_piston_mil_sag', 869, 'mil'); ad('kose_piston', 'kose_piston_somun', 867); ad('kose_piston', 'kose_piston_vida_mili', 868, 'mil')
ad('kose_piston', 'kose_piston_sensor_somun_0', 870, 'somun'); ad('kose_piston', 'kose_piston_sensor_somun_1', 871, 'somun'); ad('kose_piston', 'kose_piston_motor', 876, 'motor'); ad('kose_piston', 'kose_piston_sensor', 881, 'sensor')   # 870/871: 13 × 15 × 3 = M8 sensörün ince somunları (ürünün kendi; kol lipinin iki yanında)
# ---------------------------------------------------------------- PARMAK (ön parmaklar + Y ekseni) · 17
ad('parmak', 'parmak_tasiyici', 1438, 'tasiyici', ek=[1437]); ad('parmak', 'parmak_motor_braketi', 1439); ad('parmak', 'parmak_motor_kasnagi', 1440)   # 1437 kasnak bloğu: taşıyıcı ile tek işlenmiş parça (yatak deliği çevresinde 5 mm duvar; vida yeri yok)
ad('parmak', 'parmak_sensor_lamasi', 1441); ad('parmak', 'parmak_mafsal_plaka_0', 1442, 'burc'); ad('parmak', 'parmak_mafsal_plaka_1', 1443, 'burc')   # Ø27,8 × 8 flanşlı rulman diskleri: yuvalara sıkı geçme (GEÇME) · 1444/1445 motorun arka kapağı + arka mil → motora ek
ad('parmak', 'parmak_sensor_braketi', 1446); ad('parmak', 'parmak_kayis', 1447, 'kayis'); ad('parmak', 'parmak_motor', 1448, 'motor', ek=[1444, 1445]); ad('parmak', 'parmak_sensor', 1449, 'sensor')
ad('parmak', 'parmak_kasnak', 1583); ad('parmak', 'parmak_gobek', 1584); ad('parmak', 'parmak_kol', 1585); ad('parmak', 'parmak_bicak', 1586)
# ---------------------------------------------------------------- ARKA İTİCİ (piston) · 27
ad('itici', 'itici_tasiyici', 1415, 'tasiyici'); ad('itici', 'itici_ray_0', 1429); ad('itici', 'itici_ray_1', 1432)
ad('itici', 'itici_ust_blok_0', 1416); ad('itici', 'itici_ust_blok_1', 1421); ad('itici', 'itici_yatak_plakasi_0', 1417); ad('itici', 'itici_yatak_plakasi_1', 1418)
ad('itici', 'itici_ust_yatak', 1430); ad('itici', 'itici_vida_mili', 1431, 'mil'); ad('itici', 'itici_kasnak_mil', 1419); ad('itici', 'itici_motor_blogu', 1420); ad('itici', 'itici_kasnak_motor', 1422)
ad('itici', 'itici_kayis', 1433, 'kayis'); ad('itici', 'itici_motor', 1434, 'motor'); ad('itici', 'itici_motor_mili', 1435, 'mil'); ad('itici', 'itici_sensor_blogu', 1423); ad('itici', 'itici_sensor', 1436, 'sensor')
ad('piston', 'piston_plaka', 1411, 'tasiyici'); ad('piston', 'piston_bas', 1410); ad('piston', 'piston_lama_0', 1412); ad('piston', 'piston_lama_1', 1414); ad('piston', 'piston_somun_braketi', 1413); ad('piston', 'piston_somun_blogu', 1426, 'burc')   # flanşlı somun: flanşı üreteçte braketin kendi hacminde (aynı 10 mm katman) → braket yuvasında GEÇME sayılır (açık madde)
for i, n in enumerate((1424, 1425, 1427, 1428)): ad('piston', 'piston_araba_%d' % i, n)
# ---------------------------------------------------------------- BESLEYİCİ (şasi + itici + vakum) · 44 + uç sensörleri 6
ad('besleyici', 'besleyici_plaka', 1315, 'tasiyici')
for i, n in enumerate((1316, 1317, 1319, 1320)): ad('besleyici', 'besleyici_profil_%d' % i, n)
ad('besleyici', 'besleyici_ray_0', 1332); ad('besleyici', 'besleyici_ray_1', 1333); ad('besleyici', 'besleyici_sensor_tutucu', 1318); ad('besleyici', 'besleyici_sensor', 1345, 'sensor')
ad('besleyici', 'besleyici_mil_yatagi', 1321); ad('besleyici', 'besleyici_kasnak_mili', 1334, 'mil'); ad('besleyici', 'besleyici_kasnak_0', 1322); ad('besleyici', 'besleyici_kasnak_1', 1323)
ad('besleyici', 'besleyici_kayis', 1342, 'kayis'); ad('besleyici', 'besleyici_motor', 1343, 'motor'); ad('besleyici', 'besleyici_motor_yuvasi', 1324)
ad('besleyici', 'besleyici_uc_sensor_tutucu', 1497); ad('besleyici', 'besleyici_uc_sensor', 1512, 'sensor')
ad('itici_b', 'bitici_kiris', 1307, 'tasiyici'); ad('itici_b', 'bitici_kizak_plakasi_0', 1308); ad('itici_b', 'bitici_kizak_plakasi_1', 1312); ad('itici_b', 'bitici_kol_0', 1309); ad('itici_b', 'bitici_kol_1', 1313)
ad('itici_b', 'bitici_araba_0', 1327); ad('itici_b', 'bitici_araba_1', 1329); ad('itici_b', 'bitici_kayis_kelepcesi', 1331); ad('itici_b', 'bitici_kilavuz_blok_0', 1310); ad('itici_b', 'bitici_kilavuz_blok_1', 1314)
ad('itici_b', 'bitici_kilavuz_burc_0', 1328, 'burc'); ad('itici_b', 'bitici_kilavuz_burc_1', 1330, 'burc'); ad('itici_b', 'bitici_orta_blok', 1311); ad('itici_b', 'bitici_pad', 1344)
ad('vakum', 'vakum_bar', 1325, 'tasiyici'); ad('vakum', 'vakum_blok', 1326); ad('vakum', 'vakum_mil_0', 1335, 'mil'); ad('vakum', 'vakum_mil_1', 1341, 'mil'); ad('vakum', 'vakum_mil_orta', 1338, 'mil')
for i, n in enumerate((1336, 1337, 1339, 1340)): ad('vakum', 'vantuz_flans_%d' % i, n)
for i, n in enumerate((1346, 1347, 1349, 1350)): ad('vakum', 'vantuz_%d' % i, n, 'vantuz')
ad('vakum', 'vakum_hortum', 1348, 'hortum')
ad('asansor', 'asansor_sensor_tutucu', 1496); ad('asansor', 'asansor_sensor', 1511, 'sensor')
ad('katlama_sensor', 'katlama_sensor_tutucu', 1492); ad('katlama_sensor', 'katlama_sensor', 1510, 'sensor')
# ---------------------------------------------------------------- denetim + yaz
kul = [v['no'] for v in AD.values()] + [e for v in AD.values() for e in v['ek']]
eks = sorted(set(O) - set(kul)); cok = [n for n in kul if kul.count(n) > 1]
assert not eks and not cok, (eks, cok)
OUT = {}
for isim, v in AD.items():
    r = O[v['no']]
    OUT[isim] = dict(dug=r['dug'], lo=r['lo'], hi=r['hi'], aile=v['aile'], rol=v['rol'], tip=r['tip'], no_v10l=v['no'],
                     ek=[dict(dug=O[e]['dug'], lo=O[e]['lo'], hi=O[e]['hi'], no_v10l=e) for e in v['ek']])
yol = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', 'e_mek_parcalar.json'))
json.dump(OUT, open(yol, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
import collections
print(len(OUT), 'ad', collections.Counter(v['aile'] for v in OUT.values()), '→', yol)
