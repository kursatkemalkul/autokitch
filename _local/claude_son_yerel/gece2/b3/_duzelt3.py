s = open('plan_kod.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b)
# elektrik kutusu: soğutma grubundan sonra, rafın üstünden önden (iki bacak)
rep("""t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik kutusu → teknik bölme arka duvarı (dış arka saca)', kamera_yakin=True)
t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)""",
"""t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 25.0, 0.0)), ('on', (0.0, 29.0, 0.0)), 'ust'], t, 'B elektrik kutusu → soğutma grubu rafının üstünden teknik bölme arka duvarına', kamera_yakin=True)""")
rep("'Bölmeler bitince, sağ yan kapanmadan: B elektrik kutusu önden dış arka saca; soğutma grubu", "'Bölmeler bitince, sağ yan kapanmadan: soğutma grubu")
rep("oturur; istasyon kutusu.'", "oturur; B elektrik kutusu rafın üstünden önden dış arka saca; istasyon kutusu.'")
# üst köşebentler teknik kapamadan SONRA
rep("""for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek',""", """for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek',""")
rep("""    t = yerlestir([a], ['ust', 'on', 'sag'], t, '%s → teknik bölme' % P[a]['ac'])
t += 0.2""", """    t = yerlestir([a], ['ust', 'on', 'sag'], t, '%s → teknik bölme' % P[a]['ac'])
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti() + 0.2""")
# ön çerçeve + avara üniteleri tezgâhta TIG'lenir, birlikte gelir
rep("""for a in ['g_on_cerceve_ek_lamasi', 'g_on_cerceve_1', 'g_on_cerceve_2']: t = yerlestir([a], ['on'], t, '%s → bölme ve kovan önlerine' % P[a]['ac'])""",
"""t = yerlestir(['g_on_cerceve_ek_lamasi'], ['on'], t, 'Ön çerçeve ek laması → bölme 2 önüne')
for cer, kol in (('g_on_cerceve_1', ('K1', 'K2')), ('g_on_cerceve_2', ('K3', 'K5', 'K6'))):
    av = [ck + '_avara' for ck in sorted(CEKD) if ck.split('_')[1] in kol]; ka = [ck + '_kaynak' for ck in sorted(CEKD) if ck.split('_')[1] in kol]
    t = yerlestir([cer] + av + ka, ['on'], t, '%s + %d avara ünitesi (tezgâhta arkasına TIG) → bölme ve kovan önlerine' % (P[cer]['ac'], len(av)), tezgah_kaynak=ka, kamera_yakin=(cer == 'g_on_cerceve_1'))""")
rep("adim('Ön çerçeve', '430 ferritik ön çerçeve iki parça (lazer, düz) önden bölme ve kovan önlerine; ek yeri arkadan ek lamasıyla.', 'ön çerçeve 1 / 2 · ek laması')",
    "adim('Ön çerçeve + avara üniteleri', '430 ferritik ön çerçeve iki parça (lazer, düz). Tezgâhta: her çekmecenin avara ünitesi (kol + sensör laması + mil + kasnak + reed sensörler, kaynaklı alt montaj; çerçeve ağzından geçmeyecek kadar uzun) ön flanşından çerçevenin arkasına TIG köşe 2 × 8 mm. Çerçeve 1 (K1–K2) ve 2 (K3–K6) avaralarıyla birlikte önden gelir; ek yeri arkadan ek lamasıyla.', 'ön çerçeve 1 / 2 · ek laması · avara ünitesi × 21 · TIG 2 × 8 mm × 21')")
a = s.index("adim('Avara üniteleri'"); b = s.index("adim('Çekmeceler'")
s = s[:a] + s[b:]
open('plan_kod.py', 'w', encoding='utf-8').write(s)
m = open('b3_montaj.py', encoding='utf-8').read()
# yerlestir: tezgah_kaynak (üretimde büyür, grupla taşınır)
m = m.replace("def yerlestir(adlar, adaylar, t_min, metin, pem=(), grup_kaynak=(), sure_bekle=0.15, ek=0.0, kamera_yakin=False, eks_yol=None):",
              "def yerlestir(adlar, adaylar, t_min, metin, pem=(), grup_kaynak=(), sure_bekle=0.15, ek=0.0, kamera_yakin=False, eks_yol=None, tezgah_kaynak=()):")
m = m.replace("""    tt += sure_bekle
    for p0, p1 in zip(yol[:-1], yol[1:]):""", """    if tezgah_kaynak:
        for k_ in tezgah_kaynak: MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, 'Tezgâhta TIG: %s' % P[tezgah_kaynak[0]]['ac']); tt += 0.8
    tt += sure_bekle
    for p0, p1 in zip(yol[:-1], yol[1:]):""")
m = m.replace("""    sure_uret = 0.0
    if a0 in SAC:""", """    sure_uret = 0.8 if tezgah_kaynak else 0.0
    if a0 in SAC:""")
i = m.index('# ================================================================== PLAN')
open('b3_montaj.py', 'w', encoding='utf-8').write(m[:i] + s)
print('ok')
