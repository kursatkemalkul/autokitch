import io
p = 'plan_v4.py'; s = io.open(p, encoding='utf-8').read()
def R(a, b, n=1):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)
R("YAN = (60.0, 0.0, 0.0)", "YAN = (36.0, 0.0, 0.0)          # bölme kalınlığı 35 + 1: kovan uçlarını aşacak kadar yana, sonra −x")
R("t = yerlestir(['g_ic_sol_duvar'], [('on', (60.0, 0.0, 0.0)), 'ust', 'on'], t,", "t = yerlestir(['g_ic_sol_duvar'], ['ust', ('on', (60.0, 0.0, 0.0)), 'on'], t,")
# grubu → elektrik → zincir
R("""t = yerlestir(['zincir_kanal'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)""",
"""t = yerlestir(['sogutma_grubu'], ['ust', 'on'], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1
t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 12.0, 0.0)), 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)
t = yerlestir(['zincir_kanal'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)""")
R("adim('Zincir kanalı + B elektrik montaj plakası', \"Teknik bölme boşken: enerji zinciri", "adim('Teknik bölme: soğutma grubu, elektrik plakası, zincir kanalı', \"Teknik bölme boşken: soğutma grubu (kompresör + kondenser + fan, tek ürün) iner, taban raylarının uçları 4 × ISO 4762 M4 + pul ile. Enerji zinciri")
a = s.index("    if k == 5:\n        t = baglantilari_tamamla(t) + 0.1\n        olay(t, 'Teknik kapama sacından önce"); b = s.index("    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'")
s = s[:a] + s[b:]
R("""[('on', YAN), 'sag', 'ust'] if k < 5 else ['ust', ('on', YAN)]""", """[('on', YAN), 'sag', 'ust'] if k < 5 else ['on', ('on', YAN), 'ust']""")
# taban tapaları
R("""for a in ['g_ic_taban_1', 'g_ic_taban_2']: t = yerlestir([a], ['ust', 'on'], t, '%s (arka kenarı yukarı bükülü) → yalıtım levhasının üstüne' % P[a]['ac'])""",
"""TAPA = sorted(a for a in P if a.startswith('g_pu_taban_tapa'))
for a in TAPA: P[a]['ac'] = 'PU tapa Ø25'; yerlestir([a], ['ust'], t, None, sure_bekle=0.0)
t = bitti(); olay(t - 0.4, 'PU tapa Ø25 × 10 → levhadaki deliklerden şase cıvatalarının başı üstüne')
for a in ['g_ic_taban_1', 'g_ic_taban_2']: t = yerlestir([a], ['ust', 'on'], t, '%s (arka kenarı yukarı bükülü) → yalıtım levhasının üstüne' % P[a]['ac'])""")
R("""adim('Taban yalıtımı + iç taban', 'GFRP ısı köprüsü takozları (dikme altları) dış tabana; taban yalıtım levhası (PU, kesilmiş: dikme, takoz ve cıvata boşlukları açık) dış tabana yapıştırılır (yeşil yapıştırıcı);""",
"""adim('Taban yalıtımı + iç taban', 'GFRP ısı köprüsü takozları (dikme altları) dış tabana; taban yalıtım levhası (PU, kesilmiş: dikme ve takoz boşlukları, şase cıvatalarının üstünde Ø25 delik) dış tabana yapıştırılır (yeşil yapıştırıcı), deliklere PU tapa;""")
# iç tavan + PU tavan tezgâh sandviçi
R("""for a in ['g_ic_tavan_1', 'g_ic_tavan_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → bölmelerin üstüne' % P[a]['ac'])
t = baglantilari_tamamla(t) + 0.1
for a in ['g_pu_tavan_yuksek', 'g_pu_tavan_topping', 'g_pu_tavan_firin']:
    t = yerlestir([a], ['ust', 'on'], t, '%s → iç tavanın üstüne' % P[a]['ac']); t = yapistir(a, 1, -1, t)""",
"""for sac_, pus in (('g_ic_tavan_1', ['g_pu_tavan_yuksek']), ('g_ic_tavan_2', ['g_pu_tavan_topping', 'g_pu_tavan_firin'])):
    yp = [yapistirici(a, 1, -1) for a in pus]
    t = yerlestir([sac_] + pus + yp, ['ust', 'on'], t, '%s + tavan yalıtım levhası (tezgâhta yapıştırılmış; perçin uçları için levha altı cepli) → bölmelerin üstüne' % P[sac_]['ac'], tezgah_kaynak=yp)
    for n_ in yp:
        while n_ in YERINDE: YERINDE.remove(n_)
t = baglantilari_tamamla(t, 'İç tavan: bölme ve sol duvar üst flanşlarına alttan (gıda tarafından) DIN 7337 Ø4 kör perçin (mavi)') + 0.1""")
R("""'İç tavan 1 / 2 bölmelerin üstüne — bölme ve sol duvar flanşlarına alttan kör perçin; tavan yalıtım levhaları (PU) yapıştırılır;""",
"""'İç tavan 1 / 2 tezgâhta tavan yalıtım levhalarıyla (PU, yapıştırılmış) birlikte bölmelerin üstüne iner — bölme ve sol duvar flanşlarına alttan kör perçin;""")
# kelepçe / konsol adayları
R("""                tt_ = yerlestir([a], ['on', 'ust', 'sag', 'sol', 'alt', 'arka'], tt_, None, sure_bekle=0.0); continue""",
"""                n_ = np.asarray(P[a]['n'], float) if P[a].get('n') else np.zeros(3)
                ad_ = ['on', 'ust', ('on', tuple(-12.0 * n_)), ('ust', tuple(-12.0 * n_)), ('on', (12.0, 0, 0)), ('on', (-12.0, 0, 0)), ('ust', (12.0, 0, 0)), 'sag', 'sol', 'alt', 'arka']
                tt_ = yerlestir([a], ad_, tt_, None, sure_bekle=0.0); continue""")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
