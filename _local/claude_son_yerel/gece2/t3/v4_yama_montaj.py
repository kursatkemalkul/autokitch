import io
f = 't3_montaj_v4.py'
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


rep('"""TOPPING MONTAJ ANİMASYONU v3', '"""TOPPING MONTAJ ANİMASYONU v4 (model: üreteç h3_topping_sac_v2 · zincir 37–50) — ESKİ BAŞLIK: TOPPING MONTAJ ANİMASYONU v3')
rep("import sac_morf_t as SM", "import sac_morf_t4 as SM")
rep("D0 = pickle.load(open('t3_parca.pkl', 'rb'))", "D0 = pickle.load(open('t3_parca_v4.pkl', 'rb'))")
rep("'kaide_cep_tasiyici_0': 'Cep taşıyıcı L (arka)', 'kaide_cep_tasiyici_1': 'Cep taşıyıcı L (ön)'}",
    "'kaide_cep_tasiyici_0': 'Cep taşıyıcı L (arka)', 'kaide_cep_tasiyici_1': 'Cep taşıyıcı L (ön)', 'kanal_gecis_kapagi': 'Kanal geçiş kapağı 1,5',\n"
    "         'evaporator_ayagi_0': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_1': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_2': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_3': 'Evaporatör ayağı 2,5'}")
# PEM / burç / perçin eşlemesi
rep('''    elif a.startswith('servis_arka_') and a.endswith('_pem'):
        s = {'yan_sol': 'dis_yan_sol', 'yan_sag': 'dis_yan_sag', 'tavan': 'dis_tavan', 'taban': 'dis_taban'}['_'.join(a.split('_')[2:4]) if a.split('_')[2] == 'yan' else a.split('_')[2]]
        pem_bagla(a, s, (0, 0, 1.0), 'PEM SP-M5-2')''',
    '''    elif a.startswith('servis_arka_') and ('_burc' in a):
        s = {'yan_sol': 'dis_yan_sol', 'yan_sag': 'dis_yan_sag', 'tavan': 'dis_tavan', 'taban': 'dis_taban'}['_'.join(a.split('_')[2:4]) if a.split('_')[2] == 'yan' else a.split('_')[2]]
        pem_bagla(a, s, (0, 0, 1.0), 'TIG punta' if '_punta_' in a else 'kaynak burcu M5')
    elif (a.startswith(('evaporator_ayak_', 'kanal_kapagi_')) and a.endswith('_pem')): pem_bagla(a, 'kuru_bolme_tabani', (0, -1.0, 0), 'PEM SP-M5-1')''')
rep('''    elif a.startswith('servis_arka') and a.endswith('_vida'): P[a]['eks'] = np.array([0, 0, 1.0])''',
    '''    elif a.startswith('servis_arka') and a.endswith('_vida'): P[a]['eks'] = np.array([0, 0, 1.0])
    elif a.startswith(('evaporator_ayak_', 'kanal_kapagi_')) and a.endswith('_vida'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('astar_percin_tavan'): P[a]['eks'] = np.array([0, 1.0, 0])
    elif a.startswith('astar_percin_'): P[a]['eks'] = np.array([0, 0, -1.0])''')
# astar TIG işaretleri yok (v2: perçinli)
rep('''# astar iç köşe TIG (soğuk oda içinden, astar yüzlerinde)
punta_dizi('astar_sol', [(1496.0, y, -569.9) for y in (1950.0, 2050.0, 2100.0)], (0, 0, 1), 'TIG: astar sol ↔ astar arka (iç köşe R3)')
punta_dizi('astar_sag', [(2440.0, y, -569.9) for y in (1950.0, 2050.0, 2100.0)], (0, 0, 1), 'TIG: astar sağ ↔ astar arka (iç köşe R3)')
punta_dizi('astar_tavan', [(x, 2139.9, -566.5) for x in (1700.0, 2000.0, 2300.0)] + [(1497.0, 2139.9, z) for z in (-300.0, 0.0)] + [(2439.0, 2139.9, z) for z in (-300.0, 0.0)],
           (0, -1, 0), 'TIG: astar tavan ↔ arka / yan astarlar (iç köşe)')
''', '')
# beyanlı: çökertme (dimple) — animasyon ağı açınımdan bükülür, dimple preste sonra (modelde var)
rep("HARIC_PLAN.add(('pem_M8_A_1300_300_kopuk_kapagi', 'pem_M8_A_1300_300'))",
    "for v_ in [a for a in P if a.startswith('servis_arka') and (a.endswith('_vida') or a.endswith('_burc'))]:\n"
    "    for s_ in ('dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'dis_taban', 'dis_arka_servis'): HARIC_PLAN.add((v_, s_)); HARIC_NEDEN[(v_, s_)] = 'çökertme (dimple): servis sacı + dönüş birlikte preslenir, vida başı / burç dimple konisine oturur'\n"
    "HARIC_PLAN.add(('pem_M8_A_1300_300_kopuk_kapagi', 'pem_M8_A_1300_300'))")
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
