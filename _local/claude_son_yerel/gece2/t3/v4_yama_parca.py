import io, re
f = 't3_parca_v4.py'
s = io.open(f, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''"""TOPPING montaj v3 · parça çıkarımı''', '''"""TOPPING montaj v4 (üreteç h3_topping_sac_v2: dimple · bükümlü iç sac + perçin + POM pul · PU levha + yapıştırıcı · evaporatör ayağı · kanal kapağı)
Kullanım: python t3_parca_v4.py <glb (zincir 37–49 çıktısı, sıkılaştırma öncesi)> <t_bil.pkl> <hat3_v9e_ent.json>
ESKİ: TOPPING montaj v3 · parça çıkarımı''')
rep("ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']",
    "ENT = json.load(open(sys.argv[3], encoding='utf-8'))['parca']")
# malzeme: renk anahtarı (kırmızı kaynak · mavi bağlantı · yeşil yapıştırıcı / silikon · sarı PU)
rep('''    elif 'kopuk_kapagi' in a or 'silikonu' in a: m = 'koyu\'''', '''    elif t == 'silikon' or 'silikonu' in a or a.startswith(('derz_', 'yapistirici')): m = 'yapistirici'; t = 'silikon'
    elif 'kopuk_kapagi' in a: m = 'koyu\'''')
i = s.index('# ---------------------------------------------------------------- PU köpük bloğu')
j = s.index('# ---------------------------------------------------------------- ürünler')
s = s[:i] + '''# ---------------------------------------------------------------- v4: PU levhalar / yapıştırıcı / derz silikonu üreteçte ayrı parça (T2 bölme yok)
for a in list(P):
    if a.startswith('pu_levha_'): P[a]['ac'] = 'PU levha %s (40 kg/m³ · ölçüsünde kesilmiş, flanş / perçin yuvaları açık)' % {'arka': 'arka', 'sol': 'sol', 'sag': 'sağ', 'tavan': 'tavan'}[a.split('_')[2]]
    if a.startswith('yapistirici_'): P[a]['ac'] = 'Yapıştırıcı (PU levha → dış sac, 0,5 mm)'
    if a.startswith('derz_'): P[a]['ac'] = 'Derz silikonu (gıda tarafı)'
P['pu_raf_esik']['ac'] = 'PU levha raf (raf altı + eşik arkası · ölçüsünde kesilmiş)'
''' + s[j:]
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
