s = open('t3_montaj.py', encoding='utf-8').read()
a = s.index("punta_dizi('yan_sol_taban'"); b = s.index("# astar iç köşe TIG")
s = s[:a] + """Vt = P['dis_taban']['V']
xl = Vt[(Vt[:, 0] < 1445) & (Vt[:, 1] > 900)][:, 0].max(); xr = Vt[(Vt[:, 0] > 2490) & (Vt[:, 1] > 900)][:, 0].min()
punta_dizi('yan_sol_taban', [(xl, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sol')
punta_dizi('yan_sag_taban', [(xr - 0.1, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sağ')
punta_dizi('tavan_yanlar', [(x, 2200.0, z) for x in (1440.0, 2496.0) for z in (-700.0, -300.0, 20.0)], (0, 1, 0), 'TIG: dış tavan ↔ yan saclar (üst köşe)')
""" + s[b:]
a = s.index("# ---- 6 DIŞ YAN + TAVAN"); b = s.index("# ---- 14 SERVİS SACI ALT MONTAJI")
s = s[:a] + open('_plan_orta.py', encoding='utf-8').read() + s[b:]
a = s.index("# ---- 15 UNO ÖN GRUPLARI + KASETLER"); b = s.index("# ---- 16 SERVİS SACI KAPANIR")
s = s[:a] + s[b:]
s = s.replace("t = koy('x_ekseni', [ON, YOL((0, 0, 900), (0, 10, 0))]", "t = koy('x_ekseni', AD(ON9, lift=(5, 10, 20))")
open('t3_montaj.py', 'w', encoding='utf-8').write(s)
