# b3_parca: gövde parçaları v9l'in GERÇEK üçgenlerinden (ent aralıkları adım 44'ten sonra eskidi: dejenere + sona eklenen üçgenler)
s = open('b3_parca.py', encoding='utf-8').read()
old = s[s.index("for ad, v in ENT.items():\n    V, F = ent_mesh(ad)"):s.index("print('gövde (ent):'")]
new = '''from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
YENI = {}
for dug in sorted(set(v['dugum'] for v in ENT.values())):
    X, T = node_tri(dug)
    Pt = X[T]; ar = np.linalg.norm(np.cross(Pt[:, 1] - Pt[:, 0], Pt[:, 2] - Pt[:, 0]), axis=1); ok = ar > 1e-9
    C = Pt.mean(1)
    adlar = [a for a, v in ENT.items() if v['dugum'] == dug]
    K = np.array([ENT[a]['kutu'] for a in adlar]); vol = (K[:, 1] - K[:, 0]) * (K[:, 3] - K[:, 2]) * (K[:, 5] - K[:, 4])
    ata = -np.ones(len(T), int); best = np.full(len(T), np.inf)
    for i, a in enumerate(adlar):
        k = K[i]; m = ok & (C[:, 0] >= k[0] - 0.05) & (C[:, 0] <= k[1] + 0.05) & (C[:, 1] >= k[2] - 0.05) & (C[:, 1] <= k[3] + 0.05) & (C[:, 2] >= k[4] - 0.05) & (C[:, 2] <= k[5] + 0.05)
        m &= vol[i] < best
        ata[m] = i; best[m] = vol[i]
    for i, a in enumerate(adlar):
        Tt = T[ata == i]
        if not len(Tt): print('  BOŞ', a); continue
        u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
        v = ENT[a]
        if v['tur'] == 'sac': m_, tur = ('kapak' if v['dugum'] == 'B_KASA__on_cerceve' else 'sac'), 'sac'
        elif a.startswith('pu_') or a.endswith('_pu'): m_, tur = 'pu', 'pu'
        elif 'kaynagi' in a: m_, tur = 'kaynak', 'kaynak'
        elif 'silikon' in a: m_, tur = 'koyu', 'silikon'
        elif 'kopuk_kapagi' in a: m_, tur = 'koyu', 'baglanti'
        elif a.startswith('isi_kalkani_takozu'): m_, tur = 'koyu', 'mek'
        else: m_, tur = 'baglanti', 'baglanti'
        ekle('g_' + a, X[u], inv.reshape(-1, 3), m_, tur, a, kaynak=dug, bom=v.get('bom'))
    kalan = np.where(ok & (ata < 0))[0]
    if len(kalan):
        Tk = T[kalan]; uu, inv = np.unique(np.round(X[Tk.reshape(-1)], 3), axis=0, return_inverse=True); Vi = inv.reshape(-1, 3)
        r = np.concatenate([Vi[:, 0], Vi[:, 1]]); c = np.concatenate([Vi[:, 1], Vi[:, 2]])
        n_, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uu), len(uu))), directed=False)
        tc = cl[Vi[:, 0]]
        for j in np.unique(tc):
            Tj = Tk[tc == j]; u, inv2 = np.unique(Tj.reshape(-1), return_inverse=True)
            YENI.setdefault(dug, []).append((X[u], inv2.reshape(-1, 3)))
for dug, L in YENI.items():
    print('  adım 44 eklentisi', dug, len(L), [tuple(np.round(V.max(0) - V.min(0), 2)) for V, F in L[:3]])
    for j, (V, F) in enumerate(L):
        e = V.max(0) - V.min(0)
        if dug == 'B_KASA__paslanmaz': ekle('g_ray_pem_arka_%02d' % j, V, F, 'baglanti', 'baglanti', 'PEM SP-M5-1 (arka iç sac)')
        elif dug == 'B_KASA__conta': ekle('g_ray_pem_arka_%02d_kopuk_kapagi' % j, V, F, 'koyu', 'baglanti', 'köpük kapağı (arka PEM)')
        else: ekle('g_yeni_%s_%02d' % (dug[7:], j), V, F, 'baglanti', 'baglanti', 'adım 44 eklentisi')
'''
s = s.replace(old, new)
open('b3_parca.py', 'w', encoding='utf-8').write(s)
# b3_montaj: PEM / kapak sacı ince eksene göre; düz saclar model ağıyla (adım 44 delikleri dahil), bükümlüler açınımdan
m = open('b3_montaj.py', encoding='utf-8').read()
old2 = m[m.index("for f in sorted(os.listdir(SM.ACN_DIR)):"):m.index("print('sac', len(SAC))")]
new2 = '''for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); SAC['g_' + ad] = s
    old = P['g_' + ad]
    if s.bukum: V, F = s.dunya(s.yerel({})), s.F
    else: V, F = old['V'], old['F']                      # düz sac: modelin kendi ağı (adım 44 delikleri dahil)
    P['g_' + ad] = dict(V=V, F=F, m=old['m'], tur='sac', ac=old['ac'], bom=old.get('bom'), model_lo=old['V'].min(0), model_hi=old['V'].max(0))
'''
m = m.replace(old2, new2)
old3 = m[m.index("    for a in grp:\n        cx = (kutu(a)[0][0] + kutu(a)[1][0]) / 2"):m.index("    for s, L in by.items():")]
new3 = '''    for a in grp:
        la, ha = kutu(a); ca = (la + ha) / 2; cand = []
        for s_ in SAC:
            ls, hs = kutu(s_); ex = hs - ls; ax = int(np.argmin(ex))
            if ex[ax] > 3 or abs((ls[ax] + hs[ax]) / 2 - ca[ax]) > 4: continue
            o = [k for k in range(3) if k != ax]
            if all(ls[k] - 1 < la[k] and ha[k] < hs[k] + 1 for k in o): cand.append(s_)
        assert len(cand) == 1, (a, cand)
        by.setdefault(cand[0], []).append(a)
'''
m = m.replace(old3, new3)
m = m.replace("""        sx = (kutu(s)[0][0] + kutu(s)[1][0]) / 2; cx = (V[:, 0].min() + V[:, 0].max()) / 2
        P[n] = dict(V=V, F=F, m=m, tur='baglanti', ac='%d × %s' % (len(L), ac), sac=s, yan=float(np.sign(cx - sx)))""",
"""        ls, hs = kutu(s); ax = int(np.argmin(hs - ls)); sx = (ls[ax] + hs[ax]) / 2; cx = (V[:, ax].min() + V[:, ax].max()) / 2
        yv = np.zeros(3); yv[ax] = float(np.sign(cx - sx))
        P[n] = dict(V=V, F=F, m=m, tur='baglanti', ac='%d × %s' % (len(L), ac), sac=s, yan=yv)""")
m = m.replace("yan = P[p]['yan']; e_ = np.array([yan, 0, 0]) * 30.0", "e_ = np.asarray(P[p]['yan'], float) * 30.0")
m = m.replace("t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'])", "t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'], pem=PEM_SAC.get(a, []))")
open('b3_montaj.py', 'w', encoding='utf-8').write(m)
p = open('plan_kod.py', encoding='utf-8').read()
p = p.replace("for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'])",
              "for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'], pem=PEM_SAC.get(a, []))")
open('plan_kod.py', 'w', encoding='utf-8').write(p)
print('ok', 'pem=PEM_SAC.get(a, []))' in m)
