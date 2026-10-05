s = open('plan_kod.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)
# a) arka 1 + ek laması birlikte
rep("""for a in ['g_dis_arka_1', 'g_dis_arka_2']: t = yerlestir([a], ['arka', 'ust'], t, '%s → arkadan' % P[a]['ac'])
t = yerlestir(['g_dis_arka_ek_lamasi'], ['ust', 'on'], t, 'Arka ek laması → içeriden (punta)')""",
"""t = yerlestir(['g_dis_arka_1', 'g_dis_arka_ek_lamasi'], ['arka', 'ust'], t, 'Dış arka 1 (+ ek laması tezgâhta puntalı) → arkadan')
t = yerlestir(['g_dis_arka_2'], ['arka', 'ust'], t, 'Dış arka 2 → arkadan, ek lamasına punta')""")
# b) teknik ekipman + sağ yan bölmelerden sonra; sol yan erken
a = s.index("adim('Soğutma grubu + elektrik kutuları'"); b = s.index("# ---- 6 ARKA + SOL DUVAR SANDVİÇİ")
blok = s[a:b]; s = s[:a] + """adim('Sol yan sac', 'Sol yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sol yan · punta')
kamera_genel(['g_dis_sol_yan'], olcek=0.9)
t = yerlestir(['g_dis_sol_yan'], ['ust', 'sol'], t, 'Dış sol yan → taban + köşebentler (punta)') + 0.2
""" + s[b:]
blok = blok.replace("""t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['ust', 'on'], t, 'B elektrik kutusu → teknik bölme arka duvarı', kamera_yakin=True)""",
"""t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik kutusu → teknik bölme arka duvarı (dış arka saca)', kamera_yakin=True)
t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)""")
blok = blok.replace("""adim('Yan saclar', 'Sol ve sağ yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sol / sağ yan · punta')
kamera_genel(['g_dis_sol_yan', 'g_dis_sag_yan'], olcek=0.7)
for a in ['g_dis_sol_yan', 'g_dis_sag_yan']: t = yerlestir([a], ['ust', 'sol' if 'sol' in a else 'sag'], t, '%s → taban + köşebentler (punta)' % P[a]['ac'])""",
"""adim('Sağ yan sac', 'Sağ yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sağ yan · punta')
kamera_genel(['g_dis_sag_yan'], olcek=0.9)
t = yerlestir(['g_dis_sag_yan'], ['ust', 'sag'], t, 'Dış sağ yan → taban + köşebentler (punta)')""")
blok = blok.replace("'Sağ yan kapanmadan: soğutma grubu", "'Bölmeler bitince, sağ yan kapanmadan: B elektrik kutusu önden dış arka saca; soğutma grubu")
blok = blok.replace("oturur; B elektrik kutusu (Siemens + kartlar, tek ürün) ve istasyon kutusu teknik bölmenin arka duvarına yukarıdan.'", "oturur; istasyon kutusu.'")
a = s.index("# ---- 8 B KABLO KANALLARI"); s = s[:a] + blok + s[a:]
# c) iç kanal: yol yoksa kanal boyunca (büyür)
rep("for a in sorted(x for x in P if x.startswith('ic_kanal_')): yerlestir([a], ['on', 'ust'], t, None, sure_bekle=0.0)",
"""KANAL_BUYU = []
for a in sorted(x for x in P if x.startswith('ic_kanal_')):
    n0 = len(PLAN_SORUN); yon_sec([a], ['on', 'ust'])
    if len(PLAN_SORUN) > n0: PLAN_SORUN.pop(); KANAL_BUYU.append(a); continue
    yerlestir([a], ['on', 'ust'], t, None, sure_bekle=0.0)
t = bitti()
for a in KANAL_BUYU: buyu(a, t, 0.7)
if KANAL_BUYU: olay(t, '%d kanal parçası kovan / bölme geçişinden geçirilerek birleştirilir (kanal boyunca)' % len(KANAL_BUYU)); t += 0.8""")
# d) klips tahrikten sonra
rep("t = yerlestir(['kablo_klips'], ['on'], t, 'Kablo klipsi')\n", "")
rep("""    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.6); ilk = False
    t = bitti() + 0.15
""", """    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.6); ilk = False
    t = bitti() + 0.15
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
""")
# e) üst köşebentler teknik kapamadan önce
rep("""for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_ek_lamasi_1'""", """for a in ['g_dis_tavan_ek_lamasi_1'""")
rep("""for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek',""", """for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek',""")
rep("adim('Tavan', 'Üst köşebentler (1 büküm) yan saclara; 3 ek laması;", "adim('Tavan', '3 ek laması;")
rep("     'köşebent üst × 5 · ek laması × 3 · dış tavan × 2 · silikon')", "     'ek laması × 3 · dış tavan × 2 · silikon')")
rep("adim('İç tavan + ısı kalkanı + teknik kapama', 'İç tavan 1 / 2", "adim('İç tavan + ısı kalkanı + teknik kapama', 'Üst köşebentler (1 büküm) yan saclara (punta); iç tavan 1 / 2")
# f) avara: çerçeve ağzından içeri, sonra yana (flanş çerçeve dudağının arkasına)
rep("    for ck in KOL[k]: yerlestir([ck + '_avara'], ['on'], t, None, sure_bekle=0.0, grup_kaynak=[ck + '_kaynak'])",
    "    for ck in KOL[k]: yerlestir([ck + '_avara'], [('on', (dx, dy, 0.0)) for dy in (0.0, -25.0) for dx in (25.0, 45.0, 70.0)] + ['on'], t, None, sure_bekle=0.0, grup_kaynak=[ck + '_kaynak'])")
open('plan_kod.py', 'w', encoding='utf-8').write(s)
m = open('b3_montaj.py', encoding='utf-8').read(); i = m.index('# ================================================================== PLAN')
open('b3_montaj.py', 'w', encoding='utf-8').write(m[:i] + s)
print('ok')
