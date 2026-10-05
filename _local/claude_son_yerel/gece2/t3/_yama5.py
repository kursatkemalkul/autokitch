s = open('t3_parca.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
rep("""grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla'),""",
    """XB = sec(lambda o: kod(o) == 'TOPPING/Tabla' and o['lo'][1] > 1040 and o['hi'][1] > 1100 and (o['hi'] - o['lo'])[0] < 20)
for o in XB: grup('x_sensor_braket_%d' % round(o['lo'][0]), [o], 'mekanizma', 'mek', 'X ekseni sensör braketi (soğuk oda alt sacının FHP-M5 saplamasına)')
grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN),""")
rep("""    grup(nm, [o for o in S17 if o['lo'][0] >= x0 and o['hi'][0] <= x1 and o['lo'][1] > 1250],""",
    """    grup(nm, [o for o in S17 if o['lo'][0] >= x0 and o['hi'][0] <= x1 and o['lo'][1] > 1250] + [o for o in KUL if o['dug'] == 'ELK_TOPPING__rakor' and x0 <= o['lo'][0] <= x1 and o['lo'][1] > 1500],""")
open('t3_parca.py', 'w', encoding='utf-8').write(s)

s = open('t3_montaj.py', encoding='utf-8').read()
rep("punta_dizi('astar_sol', [(1496.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)]", "punta_dizi('astar_sol', [(1496.0, y, -569.9) for y in (1950.0, 2050.0, 2100.0)]")
rep("punta_dizi('astar_sag', [(2440.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)]", "punta_dizi('astar_sag', [(2440.0, y, -569.9) for y in (1950.0, 2050.0, 2100.0)]")
rep("for pu, ast, d in (('pu_levha_sol', 'astar_sol', 80), ('pu_levha_sag', 'astar_sag', -80),", "for pu, ast, d in (('pu_levha_sol', 'astar_sol', 20), ('pu_levha_sag', 'astar_sag', -20),")
rep("""buyu('derz_silikonu', t, 0.8); olay(t, 'Derz silikonu (YEŞİL) → gıda tarafı iç köşeler'); t += 1.0""", "")
rep("""t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (punta)') + 0.3""",
    """t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (punta)') + 0.3
buyu('derz_silikonu', t, 0.8); olay(t, 'Derz silikonu (YEŞİL) → gıda tarafı iç köşeler'); t += 1.0""")
# soğutma hatları + hava / elektrik bölümlerini UNO bölümünden sonraya taşı
a = s.index("# ---- 12 SOĞUTMA + MOTORLAR + UNO ARKA"); b = s.index("# ---- UNO ÖN + KASET + ÜST RAF + ÇERÇEVE"); c = s.index("# ---- 14 SERVİS SACI ALT MONTAJI")
s = s[:a] + s[b:c] + s[a:b] + s[c:]
rep("for a in sorted(a for a in P if a.startswith('elk_')): koy(a, AD(ARKA9, ON9),", "for a in sorted(a for a in P if a.startswith('elk_')): koy(a, AD(ARKA9, ON9, UST6),")
rep("t = koy('x_ekseni', AD(ON9, lift=(-10, -12, -15, -20, 5, 10))", "t = koy('x_ekseni', AD((-1700, 0, 0), ON9, lift=(5, 10)), 'X ekseni ünitesi → sol yandaki tabla geçiş ağzından kayarak')\nfor a in sorted(a for a in P if a.startswith('x_sensor_braket')): koy(a, AD((0, -150, 0), ON9), 'X ekseni sensör braketi → alt sacın saplamasına')\nt = bitti()\nif False: t = koy('x_ekseni', AD(ON9)")
rep("KAY = lambda pre:", """for kv_ in [a for a in P if a.startswith('dusme_kovani')]:
    for o_ in ['pu_raf_esik', 'raf'] + ['uno_%s_on' % u_ for u_ in ('kiyma', 'kusbasi', 'sos', 'harc')]:
        HARIC_PLAN.add((o_, kv_)); HARIC_NEDEN[(o_, kv_)] = 'düşme kovanı deliğe / yuvaya sıfır boşlukla geçer (model teması)'
for ad_ in ('kasar', 'sucuk'):
    for o_ in [a for a in P if a.startswith(('dil_kesik_kose_silikonu', 'esik_on_yiv', 'raf_esik_yiv'))]:
        HARIC_PLAN.add(('kaset_' + ad_, o_)); HARIC_NEDEN[('kaset_' + ad_, o_)] = 'kaset dili eşik kesiğinden sıfır boşlukla geçer (köşe silikonu / yiv dolgusu teması)'
KAY = lambda pre:""")
open('t3_montaj.py', 'w', encoding='utf-8').write(s)
print('ok')
