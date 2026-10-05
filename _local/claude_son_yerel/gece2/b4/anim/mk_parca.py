import io
s = io.open('../../b3/b3_parca.py', encoding='utf-8').read()
s = s.replace('"""B montaj v3 · parça çıkarımı: hat3_v9l → b3_parca.pkl  (mm, dünya)', '''"""B montaj v4 · parça çıkarımı: hat3_v9r (zincir 00–50) → b4_parca.pkl  (mm, dünya) — b3_parca.py'den
Gövde (B_KASA__*, B_KASA__pu_dolgu, B_MODULER__baglanti, B_TASIYICI__baglanti): m8kit katı bileşenleri (bil_r.pkl) + ad eşleme (v9b ent kutusu ·
flanşlı saclarda kutuyu kapsayan bileşen · adım 46 PU parçaları) · yeni bağlantı elemanları (B_BAGLANTI__paslanmaz): adım 47 / 49 ent kutularıyla.
Eski açıklama:''')
s = s.replace("sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))", "sys.path.insert(0, os.path.join(HERE, '..', '..', 'cekmece'))")
s = s.replace("g = G(os.path.join(HERE, '..', '..', 'hat3_v9l.glb'))", "g = G(os.path.join(HERE, 'hat3_v9r.glb'))")
s = s.replace("ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9b_ent.json'), encoding='utf-8'))['parca']",
              "ENT = json.load(open(os.path.join(HERE, '..', '..', 'adim8', 'is_tam', 'hat3_v9b_ent.json'), encoding='utf-8'))['parca']\n"
              "BR = pickle.load(open('bil_r.pkl', 'rb'))\nIS = os.path.join(HERE, '..', '..', 't3', 'is_A')\n"
              "E46 = json.load(open(os.path.join(IS, 'hat3_v9n_ent.json'), encoding='utf-8'))['parca']\n"
              "E47 = json.load(open(os.path.join(IS, 'hat3_v9o_ent.json'), encoding='utf-8'))['parca']\n"
              "E49 = json.load(open(os.path.join(IS, 'hat3_v9q_ent.json'), encoding='utf-8'))")
s = s.replace("BIL = pickle.load(open('b_bil.pkl', 'rb'))['B']",
              "BIL = [o for o in pickle.load(open('b_bil.pkl', 'rb'))['B'] if not o['dug'].startswith(('B_BAGLANTI', 'B_KASA__pu_dolgu', 'ACIL_STOP'))]")
a = s.index("# ---------------------------------------------------------------- gövde (ent)")
b = s.index("# ---------------------------------------------------------------- diğer bileşenler")
yeni = io.open('parca_govde_blok.py', encoding='utf-8').read()
s = s[:a] + yeni + s[b:]
s = s.replace("ekle('acil_stop', *birles([(o['V'], o['F']) for o in sec('ACIL_STOP')]), 'guc', 'mek', 'acil stop Schneider XB4BS8442 (tek ürün)')\n", "")
s = s.replace("open('b3_parca.pkl', 'wb')", "open('b4_parca.pkl', 'wb')")
io.open('b4_parca.py', 'w', encoding='utf-8', newline='').write(s)
print('ok', 'acil' in s)
s = io.open('b4_parca.py', encoding='utf-8').read()
old = "ekle('zincir_kanal', *birles([(o['V'], o['F']) for o in sec('ELK_ZINCIR') + sec('ELK_ZEMIN')]), 'kanal', 'mek', 'enerji zinciri kanalı + zemin contası')"
assert old in s
s = s.replace(old, "ekle('zincir_kanal', *birles([(o['V'], o['F']) for o in sec('ELK_ZINCIR')]), 'kanal', 'mek', 'enerji zinciri kanalı')\nekle('zemin_conta', *birles([(o['V'], o['F']) for o in sec('ELK_ZEMIN')]), 'koyu', 'mek', 'zemin geçiş contası')")
io.open('b4_parca.py', 'w', encoding='utf-8', newline='').write(s)
s = io.open('b4_parca.py', encoding='utf-8').read()
old = "    elif o['dug'] == 'B_SOGUTMA__celik' and o['lo'][2] > 20: grp.append(('izgara_tutucu', o))"
assert old in s
s = s.replace(old, old + "\n    elif o['dug'] == 'B_SOGUTMA__sac' and o['lo'][1] > 430: grp.append(('ust_sac', o))")
old2 = "ekle('izgara_tutucu',"
s = s.replace(old2, "ekle('sogutma_ust_sac', *birles([(o['V'], o['F']) for k_, o in grp if k_ == 'ust_sac']), 'sac', 'sac', 'soğutma bölmesi üst sacları (2)')\n" + old2, 1)
io.open('b4_parca.py', 'w', encoding='utf-8', newline='').write(s)
