s = open('g6_montaj.py', encoding='utf8').read()
a = "# ------------------------------------------------------------------ GLB\n"
b = '''# ------------------------------------------------------------------ SAC TEMAS DENETİMİ (havada duran sac yok) + bağlantı vurgusu
VURGU = {}
if os.environ.get('YOL', '1') == '1':
    TEMAS = YD.temas_denetim(P, HAR, GOR, KAY, GIZLI)
    HAVADA = sorted(s_ for s_, (tl, l) in TEMAS.items() if not l)
    for s_, (tl, l) in TEMAS.items():
        kom = [b_ for b_ in l if P[b_]['tur'] in ('sac', 'profil', 'kapak', 'baglanti', 'kaynak', 'arayuz')][:6]
        for x in [s_] + kom: VURGU.setdefault(x, []).append([round(tl, 3), round(tl + 0.7, 3)])
    for a_ in P:
        if a_ in GOR and a_ not in GIZLI and P[a_]['tur'] in ('baglanti', 'arayuz', 'kaynak') and HAR[a_]:
            tl = max(h[1] for h in HAR[a_]); VURGU.setdefault(a_, []).append([round(tl - 0.15, 3), round(tl + 0.5, 3)])
    _r = json.load(open(os.path.join(HERE, 'yol_rapor_%s.json' % IST), encoding='utf-8'))
    _r['temas'] = {k: [v[0], v[1][:8]] for k, v in TEMAS.items()}; _r['havada'] = HAVADA
    json.dump(_r, open(os.path.join(HERE, 'yol_rapor_%s.json' % IST), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('SAC TEMAS: %d sac/profil · havada %d %s' % (len(TEMAS), len(HAVADA), HAVADA[:12]), flush=True)

# ------------------------------------------------------------------ GLB
'''
assert s.count(a) == 1; s = s.replace(a, b)
a = "    if a in KAY: PARCA[a]['k'] = 1\n"
assert s.count(a) == 1
s = s.replace(a, a + "    if VURGU.get(a): PARCA[a]['vu'] = VURGU[a]\n")
open('g6_montaj.py', 'w', encoding='utf8').write(s); print('ok')
