s = open('g6_montaj.py', encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


# 1) B iskeleti: ana GLB tek ağ → alt şase / dikmeler / üst kirişler (y kesimi) — gerçekte ayrı borular, sırayla takılır
rep("HAR = {a: [] for a in P}\n", '''def _y_bol(ad, kesimler):
    """ana parça → y aralıklarına bölünür (manifold kesişimi; olmazsa üçgen ağırlık merkezine göre)"""
    p = P.pop(ad); bil = ANA_BILGI.pop(ad); V, F = p['V'], np.asarray(p['F'])
    try:
        import manifold3d as _mf
        m = _mf.Manifold(_mf.Mesh(V.astype(np.float32), F.astype(np.uint32)))
        if m.status() != _mf.Error.NoError or m.volume() <= 0: raise ValueError
        for ek, (y0, y1) in kesimler.items():
            k = m ^ _mf.Manifold.cube([20, y1 - y0, 20]).translate([-10, y0, -10]); mm = k.to_mesh()
            if len(mm.tri_verts): P[ad + '_' + ek] = dict(p, V=np.array(mm.vert_properties, np.float64)[:, :3], F=np.array(mm.tri_verts, np.int64)); ANA_BILGI[ad + '_' + ek] = dict(bil)
    except Exception:
        cy = V[F].mean(1)[:, 1]
        for ek, (y0, y1) in kesimler.items():
            s_ = (cy >= y0) & (cy < y1)
            if s_.any():
                Fi = F[s_]; u, inv = np.unique(Fi.reshape(-1), return_inverse=True)
                P[ad + '_' + ek] = dict(p, V=V[u], F=inv.reshape(-1, 3)); ANA_BILGI[ad + '_' + ek] = dict(bil)


if IST == 'B':
    _y_bol('M__B_MODULER__paslanmaz__2', dict(alt=(-1, 0.125), dikme=(0.125, 0.7535), kiris=(0.7535, 2)))
    _y_bol('M__B_MODULER__gfrp__2', dict(alt=(-1, 0.3), ust=(0.3, 2)))
    _y_bol('M__B_TASIYICI__celik__2', dict(dikme=(-1, 0.747), kiris=(0.747, 2)))
HAR = {a: [] for a in P}
''')

# 2) B sırası: taban saclar iskeletten ÖNCE; dikmeler yukarıdan tabanın 31×31 geçişlerinden; iç tavan dikmelerin üstünden; kirişler en üste
rep('''    t4 = t; kam(t, None)
    olay(t, '14 ayarlı ayak zemine, terazide')
    t = gel(R(r'^M__B_KASA__celik'), (0, 0.25, 0), t, 1.0) + 0.1
    olay(t, "Alt şase + PU'ya gömülecek dikme / kirişler (B_MODULER) + GFRP pedler — ayakların üstüne")
    t = gel(R(r'^M__B_MODULER__'), (0, 0.5, 0), t, 1.5, 0.2) + 0.1
    olay(t, "Taşıyıcı (K'nın oturduğu çapraz kirişler)")
    t = gel(R(r'^M__B_TASIYICI__'), (0, 0.4, 0), t, 1.1) + 0.5
    adim(4, 'Ayaklar · alt şase · gömülü iskelet', t4, t,
         "B dolabı kendi şasesi üstünde kurulur: ayaklar, alt şase boyunaları, PU'ya gömülecek dikme ve kirişler (A ve K bunların üstüne oturur) ve aradaki GFRP ısı köprüsü pedleri. Sac kabuk bu iskeletin çevresine kapanır.",
         '14 ayak · alt şase + dikmeler (B_MODULER) · GFRP ped · taşıyıcı kirişler')
    t5 = t
    t = panel(['dis_taban_1', 'dis_taban_2'], (0, 0.4, 0), t, 'Dış taban 2 parça (ek x 2091) dikmelerin geçişlerinden iner')
    t = gel(['dis_taban_ek_lamasi'], (0, 0.15, 0), t, 0.7) + 0.1
    olay(t, '10 × M8 × 20 + DIN 9021 içeriden şaseye (köpüklemeden ÖNCE)')
    kam(t, R(r'^arayuz_sase'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_sase.*_pul$'), (0, 0.12, 0), t, 0.45, 0.05)
    t = gel(R(r'^arayuz_sase'), (0, 0.18, 0), t, 0.5, 0.05) + 0.2
''', '''    t4 = t; kam(t, None)
    olay(t, '14 ayarlı ayak zemine, terazide')
    t = gel(R(r'^M__B_KASA__celik'), (0, 0.25, 0), t, 1.0) + 0.1
    olay(t, "Alt şase boyunaları (B_MODULER) ayakların üstüne")
    t = gel(['M__B_MODULER__paslanmaz__2_alt'], (0, 0.4, 0), t, 1.2) + 0.5
    adim(4, 'Ayaklar · alt şase', t4, t,
         "B dolabı kendi şasesi üstünde kurulur: ayaklar ve alt şase boyunaları. PU'ya gömülecek dikmeler tabandan SONRA gelir — taban sacları delikli olduğu için dikmeler yukarıdan sacın geçişlerinden iner.",
         '14 ayak · alt şase boyunaları')
    t5 = t
    t = panel(['dis_taban_1', 'dis_taban_2'], (0, 0.4, 0), t, 'Dış taban 2 parça (ek x 2091) yukarıdan alt şaseye iner')
    t = gel(['dis_taban_ek_lamasi'], (0, 0.15, 0), t, 0.7) + 0.1
    olay(t, '10 × M8 × 20 + DIN 9021 içeriden şaseye (köpüklemeden ÖNCE)')
    kam(t, R(r'^arayuz_sase'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_sase.*_pul$'), (0, 0.12, 0), t, 0.45, 0.05)
    t = gel(R(r'^arayuz_sase'), (0, 0.18, 0), t, 0.5, 0.05) + 0.2
    olay(t, 'GFRP ısı köprüsü pedleri dış tabanın üstüne (dikme ayakları)')
    t = gel(['M__B_MODULER__gfrp__2_alt'], (0, 0.15, 0), t, 0.7) + 0.1
    t = panel(['ic_taban_1', 'ic_taban_2'], (0, 0.5, 0), t, 'İç taban 2 parça yukarıdan — köpük kalıbının takozlarına (PU boşluğu 39 mm) · dikme geçişleri 31 × 31')
    olay(t, "Dikmeler (B_MODULER + taşıyıcı) yukarıdan iner — iç tabanın 31 × 31 geçişlerinden GFRP pedlere oturur")
    kam(t, ['M__B_MODULER__paslanmaz__2_dikme', 'M__B_TASIYICI__celik__2_dikme'], (0, 1, 0.4))
    t = gel(['M__B_MODULER__paslanmaz__2_dikme'], (0, 0.75, 0), t, 1.5) + 0.1
    t = gel(['M__B_TASIYICI__celik__2_dikme'], (0, 0.75, 0), t, 1.3) + 0.3
''')
rep('''    adim(5, 'Dış kabuk · taban → yanlar → arka', t5, t,
         "Dış kabuk iki parçalıdır (levha boyu 3000 sınırı): taban ve arka x 2091'de ek lamasıyla birleşir. Yan saclar tava değil, yalnız arka dönüşlü; tabana köşebentle bağlanır. Şase cıvataları köpüklemeden önce içeriden takılır.",
         'dış taban 2 + ek laması · 10 × M8 şase cıvatası · 8 alt köşebent · 2 yan · dış arka 2 + ek laması · silikon')
    t6 = t
    t = panel(['ic_taban_1', 'ic_taban_2'], (0, 0, 0.9), t, 'İç taban 2 parça önden — dikme geçişleri 31 × 31')
''', '''    adim(5, 'Dış taban · iç taban · dikmeler · yanlar · arka', t5, t,
         "Dış kabuk iki parçalıdır (levha boyu 3000 sınırı): taban ve arka x 2091'de ek lamasıyla birleşir. Şase cıvataları köpüklemeden önce içeriden takılır. İç taban köpük kalıbının takozlarına konur; dikmeler YUKARIDAN iner ve iç tabanın 31 × 31 geçişlerinden GFRP pedlere oturur (önden kaydırma yok). Yan saclar yalnız arka dönüşlü; tabana köşebentle bağlanır.",
         'dış taban 2 + ek laması · 10 × M8 şase cıvatası · GFRP ped · iç taban 2 · dikmeler · 8 alt köşebent · 2 yan · dış arka 2 + ek laması · silikon')
    t6 = t
''')
rep('''    t = panel(['ic_tavan_1', 'ic_tavan_2'], (0, 0, 0.9), t, 'İç tavan 2 parça önden')
''', '''    t = panel(['ic_tavan_1', 'ic_tavan_2'], (0, 0.5, 0), t, 'İç tavan 2 parça yukarıdan — dikmeler tavan geçişlerinden çıkar')
    olay(t, 'Üst kirişler + üst GFRP pedler dikme başlarına — yukarıdan, TIG kaynak (K ve A bu kirişlere oturur)')
    kam(t, ['M__B_MODULER__paslanmaz__2_kiris', 'M__B_TASIYICI__celik__2_kiris'], (0, 1, 0.4))
    t = gel(['M__B_MODULER__paslanmaz__2_kiris'], (0, 0.4, 0), t, 1.2) + 0.1
    t = gel(['M__B_TASIYICI__celik__2_kiris'], (0, 0.4, 0), t, 1.2) + 0.1
    t = gel(['M__B_MODULER__gfrp__2_ust'], (0, 0.2, 0), t, 0.8) + 0.3
''')
rep('''    adim(6, 'İç kabuk · bölmeler · kovanlar · ısı kalkanı', t6, t,
         "İç kabuk ve bölme ön kenarları ön çerçeveye ALIN gelir.''', '''    adim(6, 'İç kabuk · bölmeler · kovanlar · iç tavan · üst kirişler · ısı kalkanı', t6, t,
         "İç tavan dikmelerin üstünden iner, üst kirişler dikme başlarına kaynaklanır. İç kabuk ve bölme ön kenarları ön çerçeveye ALIN gelir.''')
rep("""         'iç taban 2 · iç sol duvar · teknik duvar · iç arka 2 · 9 bölme sacı · 14 kovan · iç tavan 2 · ısı kalkanı + 12 takoz')""",
    """         'iç sol duvar · teknik duvar · iç arka 2 · 9 bölme sacı · 14 kovan · iç tavan 2 · üst kirişler + GFRP · ısı kalkanı + 12 takoz')""")
open('g6_montaj.py', 'w', encoding='utf8').write(s); print('ok')
