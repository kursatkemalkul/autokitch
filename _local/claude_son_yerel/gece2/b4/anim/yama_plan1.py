import io
p = 'plan_v4.py'; s = io.open(p, encoding='utf-8').read()
R = [
("""def yapistir(pu, eks, taraf, tt):
    n = yapistirici(pu, eks, taraf); return buyu(n, tt, 0.5)""", """def yapistir(pu, eks, taraf, tt):
    n = yapistirici(pu, eks, taraf); r = buyu(n, tt, 0.5)
    while n in YERINDE: YERINDE.remove(n)                          # yapıştırıcı filmi yol denetiminde engel değil (levhanın yüzünde)
    return r"""),
("""        elif et in ('kaynak_somunu', 'percin_somun'):
            e2 = ev_sahibi((LO[a] + HI[a]) / 2) if et == 'kaynak_somunu' else ev_sahibi((LO[a] + HI[a]) / 2 + n * 4.0)""", """        elif et in ('kaynak_somunu', 'percin_somun'):
            if et == 'kaynak_somunu':
                q = (LO[a] + HI[a]) / 2; c = [x for x in YAPI if x.startswith(('moduler_', 'tasiyici_')) and np.all(LO[x] <= q + 0.3) and np.all(HI[x] >= q - 0.3)]
                e2 = min(c, key=lambda x: np.prod(HI[x] - LO[x] + 0.5)) if c else None
            else: e2 = ev_sahibi((LO[a] + HI[a]) / 2 + n * 4.0)"""),
("""t = yerlestir(ARKA_GRUP + YAP_ARKA, ['arka', ('arka', (0.0, 10.0, 0.0))], t, 'Arka panel (dış arka sac + iki katman yalıtım levhası, tezgâhta yapıştırılmış) → arkadan yerine', tezgah_kaynak=YAP_ARKA)""", """t = yerlestir(ARKA_GRUP + YAP_ARKA, ['arka', ('arka', (0.0, 10.0, 0.0))], t, 'Arka panel (dış arka sac + iki katman yalıtım levhası, tezgâhta yapıştırılmış) → arkadan yerine', tezgah_kaynak=YAP_ARKA)
for n_ in YAP_ARKA:
    while n_ in YERINDE: YERINDE.remove(n_)"""),
]
for a, b in R:
    assert a in s, a[:50]; s = s.replace(a, b)
old = """adim_sonu()
# ---- 6 SOL DUVAR + İÇ ARKA"""
new = """adim_sonu()
KONS_Z = [a for a in P if a.startswith('b_zincir_') and not a.startswith('b_zincir_taban_')]
TEZGAH_BAG.update(KONS_Z)
adim('Zincir kanalı + B elektrik montaj plakası', "Teknik bölme boşken: enerji zinciri kanalı tezgâhta 2 L konsoluna (2 mm, 1 büküm) 2'şer DIN 7337 Ø3,2 kör perçinle bağlanır, üstten iner; konsolların ayağı dış tabandaki PEM saplamalara geçer, M5 pul + somun. B elektrik montaj plakası önden dış arka sacın 6 PEM saplamasına, M5 pul + somun.",
     'zincir kanalı + 2 L konsol + 4 kör perçin · 2 M5 somun · B elektrik montaj plakası + 6 M5 somun')
kamera_genel(['zincir_kanal', 'elektrik_kutusu'], olcek=1.0)
t = yerlestir(['zincir_kanal'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)
adim_sonu()
# ---- 6 SOL DUVAR + İÇ ARKA"""
assert old in s; s = s.replace(old, new, 1)
old = """KONS_Z = [a for a in P if a.startswith('b_zincir_') and not a.startswith('b_zincir_taban_')]
TEZGAH_BAG.update(KONS_Z)
t = yerlestir(['zincir_kanal'] + KONS_Z, ['on', ('on', (0.0, 10.0, 0.0)), ('ust', (0.0, 0.0, 0.0)), 'alt'], t, 'Zincir kanalı + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara')
"""
assert old in s; s = s.replace(old, "")
old = """    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'"""
new = """    if k == 5:
        t = baglantilari_tamamla(t) + 0.1
        olay(t, 'Teknik kapama sacından önce: soğutma grubu sağ alt bölmeye')
        kamera_genel(['sogutma_grubu'], olcek=0.9, tt=t)
        t = yerlestir(['sogutma_grubu'], ['ust', ('ust', (-40.0, 0.0, 0.0)), 'on'], t, 'Soğutma grubu (tek ürün) → sağ alt bölme, taban rayları zemine', kamera_yakin=True)
        t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1
    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'"""
assert old in s; s = s.replace(old, new)
old = """    t = yerlestir([b], [('on', YAN), 'sag', 'ust'], t, '%s → yalıtım levhasının üstüne kapanır, kovanlara köşe TIG' % P[b]['ac'], pem=PEM_SAC.get(b, []), grup_kaynak=kb)"""
new = """    t = yerlestir([b], [('on', YAN), 'sag', 'ust'] if k < 5 else ['ust', ('on', YAN)], t, '%s → yalıtım levhasının üstüne kapanır, kovanlara köşe TIG' % P[b]['ac'], pem=PEM_SAC.get(b, []), grup_kaynak=kb)"""
assert old in s; s = s.replace(old, new)
a = s.index("adim('Soğutma grubu + elektrik',"); b = s.index("adim('Sağ yan sac',")
s = s[:a] + s[b:]
s = s.replace("""['on', ('on', (-12.0, 0.0, 0.0)), ('on', (-12.0, 20.0, 0.0)), 'ust']""", """[('on', (-12.0, 0.0, 0.0)), ('ust', (-12.0, 0.0, 0.0)), ('on', (-12.0, 20.0, 0.0)), 'on', 'ust']""")
s = s.replace("""t = yerlestir(['g_isi_kalkani_isinim_08'], ['ust', 'on'], t,""", """t = yerlestir(['g_isi_kalkani_isinim_08'], [('on', (0.0, 12.0, 0.0)), 'ust', 'on'], t,""")
old = """for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for i in (1, 2, 3): yerlestir(['g_pu_sol_kose_ust_%d' % i], ['ust', 'on'], t, 'Sol üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına', sure_bekle=0.0)
t = bitti()
"""
assert old in s; s = s.replace(old, "")
old = """adim_sonu()
adim('Sağ üst köşe', 'Sağ üst köşebentler yan saca (punta) ve soğuk depo sağ üst köşe dolgu şeridi (PU).', 'sağ üst köşebent × 2 · köşe dolgu şeridi')
t = yerlestir(['g_tk_depo_kose_dolgu'], ['ust', 'on'], bitti(), 'Soğuk depo sağ üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına')"""
new = """adim_sonu()
adim('Üst köşebentler + köşe dolguları', 'Üst köşebentler (1,5 mm · 1 büküm) yan sacların üst köşesine; dik kolu yan saca PUNTA (kırmızı). Köşebendin büküm dış yayı ile köşe arasındaki boşluğa köşe dolgu şeritleri (PU) üstten yatırılır.', 'üst köşebent × 5 · punta · köşe dolgu şeridi × 4')
kamera_genel(['g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_3'], yon=(0.5, 0.6, 0.6), olcek=0.9)
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for i in (1, 2, 3): yerlestir(['g_pu_sol_kose_ust_%d' % i], ['ust', 'on'], t, 'Sol üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına', sure_bekle=0.0)
yerlestir(['g_tk_depo_kose_dolgu'], ['ust', 'on'], t, 'Soğuk depo sağ üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına', sure_bekle=0.0)"""
assert old in s; s = s.replace(old, new)
s = s.replace("""adim('İç tavan + ısı kalkanı + teknik kapama', 'Üst köşebentler yan saclara (punta); iç tavan 1 / 2""", """adim('İç tavan + ısı kalkanı + teknik kapama', 'İç tavan 1 / 2""")
s = s.replace("""     'üst köşebent × 5 · iç tavan × 2 + kör perçin ·""", """     'iç tavan × 2 + kör perçin ·""")
s = s.replace("""tavan yalıtım levhaları (PU) yapıştırılır; sol üst köşe dolgu şeritleri; fırın""", """tavan yalıtım levhaları (PU) yapıştırılır; fırın""")
s = s.replace(""" · köşe dolgu şeridi × 4 · ısı kalkanı U""", """ · ısı kalkanı U""")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
