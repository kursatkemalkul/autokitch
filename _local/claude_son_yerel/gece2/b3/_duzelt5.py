s = open('b3_parca.py', encoding='utf-8').read()
a = s.index("    ata = -np.ones(len(T), int); best = np.full(len(T), np.inf)")
b = s.index("    for i, a in enumerate(adlar):\n        Tt = T[ata == i]")
new = '''    tol = 1.2 if dug == 'B_KASA__conta' else 0.06
    ata = -np.ones(len(T), int)
    idx = np.where(ok)[0]
    Tv = T[idx]; uu, inv = np.unique(np.round(X[Tv.reshape(-1)], 3), axis=0, return_inverse=True); Vi = inv.reshape(-1, 3)
    r = np.concatenate([Vi[:, 0], Vi[:, 1]]); c = np.concatenate([Vi[:, 1], Vi[:, 2]])
    n_, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uu), len(uu))), directed=False)
    tc = cl[Vi[:, 0]]
    sira = np.argsort(tc, kind='stable'); sinir = np.flatnonzero(np.diff(tc[sira])) + 1
    for grp in np.split(sira, sinir):
        ti = idx[grp]; Q = Pt[ti].reshape(-1, 3); lo, hi = Q.min(0), Q.max(0)
        icer = np.where(np.all(K[:, [0, 2, 4]] <= lo + tol, 1) & np.all(K[:, [1, 3, 5]] >= hi - tol, 1))[0]
        if len(icer):
            ata[ti] = icer[np.argmin(vol[icer])]; continue
        # birleşik bileşen (dokunan parçalar ortak köşeli): üçgen tam içinde olan en küçük kutu
        tl = Pt[ti].min(1); th = Pt[ti].max(1); best = np.full(len(ti), np.inf); sec = -np.ones(len(ti), int)
        for i in range(len(adlar)):
            k = K[i]; m = np.all(tl >= k[[0, 2, 4]] - tol, 1) & np.all(th <= k[[1, 3, 5]] + tol, 1) & (vol[i] < best)
            sec[m] = i; best[m] = vol[i]
        ata[ti] = sec
'''
s = s[:a] + new + s[b:]
s = s.replace("""        else: ekle('g_yeni_%s_%02d' % (dug[7:], j), V, F, 'baglanti', 'baglanti', 'adım 44 eklentisi')""",
"""        elif dug.endswith('baglanti'): ekle('g_percin_somun_ek_%02d' % j, V, F, 'baglanti', 'baglanti', 'M8 perçin somun')
        elif dug == 'B_KASA__on_cerceve': ekle('g_cerceve_derz_dolgusu', V, F, 'kapak', 'sac', 'ön çerçeve derz dolgu şeridi')
        else: ekle('g_yeni_%s_%02d' % (dug.replace('__', '_'), j), V, F, 'baglanti', 'baglanti', 'adım 44 eklentisi')""")
open('b3_parca.py', 'w', encoding='utf-8').write(s)
print('ok')
