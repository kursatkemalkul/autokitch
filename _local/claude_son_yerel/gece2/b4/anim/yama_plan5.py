import io
p = 'plan_v4.py'; s = io.open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a[:70]; s = s.replace(a, b, 1)
R("""for a in ['sase_boy_arka', 'sase_boy_on']: t = yerlestir([a], ['ust'], t, 'Boy profili 60 × 60 (kesim boyu 3661) yerine', sure_bekle=0.1)""",
  """for a in ['sase_boy_arka', 'sase_boy_on']: P[a]['fikstur'] = True; t = yerlestir([a], ['ust'], t, 'Boy profili 60 × 60 (kesim boyu 3661) kaynak fikstürüne', sure_bekle=0.1)""")
R("""t = yerlestir(['zemin_conta'], ['alt', 'ust'], t, 'Zemin geçiş contası (enerji zinciri) → dış taban deliğine alttan')
""", "")
R("""t = yerlestir(['zincir_kanal'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)""",
  """t = yerlestir(['zincir_kanal', 'zemin_conta'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + alt ucundaki zemin geçiş contası + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)""")
# iç kanal perçin / burç: kanal içinden kısa yol (3 mm) — kablo çekilmeden
R("""tt_ = tak(a, tt_, 0.4, 22.0 if P[a]['etur'] == 'civata' else 7.0) + 0.05""",
  """tt_ = tak(a, tt_, 0.4, 22.0 if P[a]['etur'] == 'civata' else (3.0 if a.startswith('b_kanal_') else 7.0)) + 0.05""")
R("""    if k.startswith('b_f1_'): GDOKUN[k].append('g_teknik_sol_duvar')""",
  """    if k.startswith(('b_kanal_782', 'b_kanal_783', 'b_kanal_804', 'b_kanal_815')): print('GDOKUN', k, GDOKUN[k])
    if k.startswith('b_f1_'): GDOKUN[k].append('g_teknik_sol_duvar')""")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
q = io.open('yap_cikti.py', encoding='utf-8').read()
a = """not P[a].get('ev') and not P[a].get('tezgah'))   # üretimde preslenen / kaynaklanan ve tezgâhta bağlanan elemanlar ev sahibiyle birlikte gelir\"),"""
b = """not P[a].get('ev') and not P[a].get('tezgah') and not P[a].get('fikstur'))   # üretimde preslenen / kaynaklanan, tezgâhta bağlanan, kaynak fikstüründe duran elemanlar\nfrom havada_grup import havada_grup\nHAVADA = havada_grup(HAVADA, P, Pm, HAR, GOR)\"),"""
assert a in q; q = q.replace(a, b)
io.open('yap_cikti.py', 'w', encoding='utf-8', newline='').write(q)
print('ok')
