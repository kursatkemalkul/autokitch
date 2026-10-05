import io
p = 'plan_v4.py'; s = io.open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a[:70]; s = s.replace(a, b, 1)
R("""YAPI = [a for a in P if not a.startswith(('b_', 'kaynak_', 'punta_', 'yap_')) and P[a]['tur'] not in ('kablo', 'pu', 'silikon', 'kaynak')]""",
  """BAGSET = set(BAG)
YAPI = [a for a in P if a not in BAGSET and not a.startswith(('kaynak_', 'punta_', 'yap_')) and P[a]['tur'] not in ('kablo', 'pu', 'silikon', 'kaynak')]""")
R("""    GDOKUN[k] = [YAPI2[i] for i in np.where(m)[0] if YAPI2[i] not in L]""",
  """    GDOKUN[k] = [YAPI2[i] for i in np.where(m)[0] if YAPI2[i] not in L]
    if k.startswith('b_f1_'): GDOKUN[k].append('g_teknik_sol_duvar')        # taban ↔ arka köşe perçinleri bölmeler kurulduktan sonra (bölme levhaları yandan kayarken engel olmasın)""")
R("""t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 12.0, 0.0)), 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)
t = baglantilari_tamamla(t) + 0.1
t = yerlestir(['sogutma_grubu'], ['on', 'ust', ('on', (0.0, 10.0, 0.0))], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1""",
"""t = yerlestir(['sogutma_grubu'], ['ust', 'on'], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1
t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)""")
R("""for a in ['g_tk_ara_arka_sac', 'g_tk_ara_pu', 'depo_arka_sac',""", """for a in ['g_tk_ara_arka_sac', 'sogutma_ust_sac', 'g_tk_ara_pu', 'depo_arka_sac',""")
R("""    t = yerlestir([a], ['ust', 'on', 'sag'], t, '%s → teknik bölme' % ad_tr(a) if a.startswith('g_') else ('Soğuk depo arka sacı' if a == 'depo_arka_sac' else 'Soğuk depo iç sacı (taban + yanlar)') + ' → teknik bölme')""",
  """    t = yerlestir([a], ['ust', 'on', 'sag'], t, ('%s → teknik bölme' % ad_tr(a)) if a.startswith('g_') else {'depo_arka_sac': 'Soğuk depo arka sacı', 'depo_ic_sac': 'Soğuk depo iç sacı (taban + yanlar)', 'sogutma_ust_sac': 'Soğutma bölmesi üst sacları (2)'}[a] + ' → teknik bölme')""")
R("""t = yerlestir(['g_ic_sol_duvar'], ['ust',""", """t = yerlestir(['g_ic_sol_duvar'], ['ust',""")
s = s.replace("""for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['ust', 'on'], t,""", """for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['on', ('on', (0.0, 2.0, 0.0)), 'ust'], t,""")
s = s.replace("""[('on', YAN), 'sag', 'ust'] if k < 5 else ['on', ('on', YAN), 'ust']""", """[('on', YAN), 'sag', 'ust'] if k < 5 else [('on', YAN), ('ust', YAN), 'on', 'ust']""")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
# yon_sec: bütün adayların sorunlarını kaydet
q = io.open('yap_montaj.py', encoding='utf-8').read()
if 'TUM_SORUN' not in q:
    q = q.replace("a = s.index(\"# ================================================================== PLAN\")",
                  "s = s.replace(\"        if ilk is None: ilk = (y, yol, s)\", \"        if ilk is None: ilk = (y, yol, s)\\n        TUMS.append((str(y), s[:3]))\")\ns = s.replace(\"    ilk = None\\n    for y in adaylar:\", \"    ilk = None; TUMS = []\\n    for y in adaylar:\")\ns = s.replace(\"    PLAN_SORUN.append(dict(parca=adlar, yon=str(ilk[0]), sorun=ilk[2][:4]))\", \"    PLAN_SORUN.append(dict(parca=adlar[:3], yon=str(ilk[0]), sorun=ilk[2][:4], tum=TUMS))\")\na = s.index(\"# ================================================================== PLAN\")  # TUM_SORUN")
    io.open('yap_montaj.py', 'w', encoding='utf-8', newline='').write(q)
print('ok')
