s = open('plan_kod.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)
rep("""t = bitti()
for a in ['g_dis_sol_yan', 'g_dis_sag_yan']: t = yerlestir([a], ['ust', 'sol' if 'sol' in a else 'sag'], t, '%s → taban + köşebentler (punta)' % P[a]['ac'])
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_arka_1', 'g_dis_arka_2']: t = yerlestir([a], ['arka', 'ust'], t, '%s → arkadan' % P[a]['ac'])
t = yerlestir(['g_dis_arka_ek_lamasi'], ['ust', 'on'], t, 'Arka ek laması → içeriden (punta)')
t = buyu('silikon_arka_kose', t, 0.6); olay(t - 0.6, 'Arka köşe silikonları sıkılır'); t += 0.3""",
"""t = bitti()
for a in ['g_dis_arka_1', 'g_dis_arka_2']: t = yerlestir([a], ['arka', 'ust'], t, '%s → arkadan' % P[a]['ac'])
t = yerlestir(['g_dis_arka_ek_lamasi'], ['ust', 'on'], t, 'Arka ek laması → içeriden (punta)')
t = buyu('silikon_arka_kose', t, 0.6); olay(t - 0.6, 'Arka köşe silikonları sıkılır'); t += 0.3
adim('Soğutma grubu + elektrik kutuları', 'Sağ yan kapanmadan: soğutma grubu (kompresör + kondenser + fan, tek ürün) sağ alt bölmeye yukarıdan iner, braketleri köşebent aralıklarına oturur; B elektrik kutusu (Siemens + kartlar, tek ürün) ve istasyon kutusu teknik bölmenin arka duvarına yukarıdan.',
     'soğutma grubu · B elektrik kutusu · istasyon kutusu')
kamera_genel(['sogutma_grubu', 'elektrik_kutusu'], olcek=0.9)
t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['ust', 'on'], t, 'B elektrik kutusu → teknik bölme arka duvarı', kamera_yakin=True)
t = yerlestir(['istasyon_kutusu'], ['ust', 'on'], t, 'İstasyon kutusu') + 0.2
adim('Yan saclar', 'Sol ve sağ yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sol / sağ yan · punta')
kamera_genel(['g_dis_sol_yan', 'g_dis_sag_yan'], olcek=0.7)
for a in ['g_dis_sol_yan', 'g_dis_sag_yan']: t = yerlestir([a], ['ust', 'sol' if 'sol' in a else 'sag'], t, '%s → taban + köşebentler (punta)' % P[a]['ac'])
t += 0.2""")
rep("adim('Dış kabuk', 'Alt köşebentler (1,5 mm · 1 büküm) tabana; sol ve sağ yan sac (1 büküm) yukarıdan; üst köşebentler yanlara (punta); arka sac 1 / 2 (2 büküm) arkadan, ek laması içeriden (punta); arka köşe silikonu.',\n     'köşebent × 13 · sol / sağ yan · arka 1 / 2 + ek laması · punta · silikon')",
    "adim('Dış kabuk (taban köşebentleri + arka)', 'Alt köşebentler (1,5 mm · 1 büküm) tabana; arka sac 1 / 2 (2 büküm) arkadan, ek laması içeriden (punta); arka köşe silikonu.',\n     'köşebent alt × 8 · arka 1 / 2 + ek laması · punta · silikon')")
rep("""t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme', kamera_yakin=True)
t = yerlestir(['izgara_tutucu'], ['on'], t, 'Izgara tutucuları')
""", "")
rep("adim('Soğutma', 'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur. Soğutma grubu sağ alt bölmeye yukarıdan iner (braketleri köşebent aralıklarına). Gider hortumu kanal boyunca.',\n     'evaporatör × 2 · soğutma grubu · ızgara tutucuları · gider hortumu')",
    "adim('Evaporatörler', 'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur. Gider hortumu kanal boyunca çekilir.',\n     'evaporatör × 2 · gider hortumu')")
rep("kamera_genel(['evaporator_1', 'evaporator_2', 'sogutma_grubu'], olcek=0.7)", "kamera_genel(['evaporator_1', 'evaporator_2'], olcek=0.7)")
a = s.index("# ---- 10 ELEKTRİK KUTULARI"); b = s.index("# ---- 11 İÇ TAVAN")
s = s[:a] + open('_blok10.py', encoding='utf-8').read() + s[b:]
rep("for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_firin', 'g_isi_kalkani_isinim_08',", "for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek', 'g_pu_tavan_topping', 'g_pu_tavan_firin', 'g_isi_kalkani_isinim_08',")
rep("for a in ['g_tk_ara_arka_sac', 'g_tk_ara_pu', 'g_tk_depo_arka_pu', 'g_tk_depo_sag_pu', 'g_tk_depo_tavan_pu']:", "for a in ['g_tk_ara_arka_sac', 'g_tk_ara_pu', 'depo_arka_sac', 'g_tk_depo_arka_pu', 'g_tk_depo_sag_pu', 'g_tk_depo_tavan_pu', 'depo_ic_sac']:")
rep("adim('İç tavan + ısı kalkanı + teknik kapama', 'İç tavan 1 / 2 bölmelerin üstüne; fırın üstünde PU tavan,", "adim('İç tavan + ısı kalkanı + teknik kapama', 'İç tavan 1 / 2 bölmelerin üstüne; PU tavan levhaları (kiriş kanalları açık, kesilmiş); fırın üstünde PU tavan,")
rep("""for a in ['g_pu_tavan_yuksek', 'g_pu_tavan_topping']: t = yerlestir([a], ['ust', 'on'], t, '%s → iç tavanın üstüne' % P[a]['ac'])
for a in ['g_dis_tavan_1', 'g_dis_tavan_2']: t = yerlestir([a], ['ust'], t, '%s → GFRP şeritler + köşebentler üstüne (punta)' % P[a]['ac'])
for a in ['g_dis_tavan_ek_lamasi_1', 'g_dis_tavan_ek_lamasi_2', 'g_dis_tavan_ek_lamasi_3']: yerlestir([a], ['ust', 'on'], t, '%s (punta)' % P[a]['ac'])
t = bitti()""", """for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_ek_lamasi_1', 'g_dis_tavan_ek_lamasi_2', 'g_dis_tavan_ek_lamasi_3']: yerlestir([a], ['ust', 'on'], t, '%s (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_1', 'g_dis_tavan_2']: t = yerlestir([a], ['ust'], t, '%s → GFRP şeritler + köşebentler üstüne (punta)' % P[a]['ac'])""")
rep("adim('Tavan', 'PU tavan levhaları (yüksek / TOPPING, kesilmiş — kiriş kanalları açık) kirişlerin üstünden iner; dış tavan 1 / 2 + 3 ek laması (punta); ek yeri silikonu.',\n     'PU tavan × 2 · dış tavan × 2 · ek laması × 3 · silikon')",
    "adim('Tavan', 'Üst köşebentler (1 büküm) yan saclara; 3 ek laması; dış tavan 1 / 2 GFRP şeritlerin üstüne (punta); ek yeri silikonu.',\n     'köşebent üst × 5 · ek laması × 3 · dış tavan × 2 · silikon')")
a = s.index("# ---- 15 İÇ KANALLAR + KABLOLAR"); b = s.index("# ---- 16–18 RAYLAR")
s = s[:a] + s[b:]
a = s.index("adim('Tahrik + avara'"); b = s.index("adim('Çekmeceler'")
s = s[:a] + open('_blok_avara.py', encoding='utf-8').read() + s[b:]
rep("""KOL = {}
for ck in CEKD: KOL.setdefault(ck.split('_')[1], []).append(ck)
adim('Sabit raylar'""", """adim('Sabit raylar'""")
rep("""t = yerlestir(['depo_govde'], ['on', 'ust'], t, 'Depo bölmesi sacları')
""", """t = yerlestir(['izgara_tutucu'], ['on'], t, 'Izgara tutucuları → ön çerçeve')
""")
rep("adim('Soğuk depo + ön paneller', 'Soğuk depo bölmesi sacı, depo rayları", "adim('Soğuk depo + ön paneller', 'Izgara tutucuları, depo rayları")
rep("     'depo sacı · depo rayları · depo çekmecesi · ön ızgara · acil stop')", "     'ızgara tutucuları · depo rayları · depo çekmecesi · ön ızgara · acil stop')")
open('plan_kod.py', 'w', encoding='utf-8').write(s)
m = open('b3_montaj.py', encoding='utf-8').read(); i = m.index('# ================================================================== PLAN')
open('b3_montaj.py', 'w', encoding='utf-8').write(m[:i] + s)
print('ok')
