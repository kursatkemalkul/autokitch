import io
s = io.open('../../b3/b3_montaj.py', encoding='utf-8').read()
s = s.replace("sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE)", "sys.path.insert(0, os.path.join(HERE, '..', '..', 'cekmece')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'b3')); sys.path.insert(0, HERE)")
s = s.replace("D0 = pickle.load(open('b3_parca.pkl', 'rb'))", "D0 = pickle.load(open('b4_parca.pkl', 'rb'))")
for old, new in [("""        for s_ in SAC:
            ls, hs = kutu(s_); ex = hs - ls; ax = int(np.argmin(ex))""", """        for s_ in SAC:
            ls, hs = P[s_]['model_lo'], P[s_]['model_hi']; ex = hs - ls; ax = int(np.argmin(ex))"""),
                 ("""        ls, hs = kutu(s); ax = int(np.argmin(hs - ls)); sx = (ls[ax] + hs[ax]) / 2; cx = (V[:, ax].min() + V[:, ax].max()) / 2""", """        ls, hs = P[s]['model_lo'], P[s]['model_hi']; ax = int(np.argmin(hs - ls)); sx = (ls[ax] + hs[ax]) / 2; cx = (V[:, ax].min() + V[:, ax].max()) / 2"""),
                 ("'koyu', 'silikon', 'arka köşe silikonları')", "'yapistirici', 'silikon', 'arka köşe silikonları (gıda sınıfı)')"),
                 ("grupla('silikon_gider_%d' % k, L, 'koyu', 'silikon',", "grupla('silikon_gider_%d' % k, L, 'yapistirici', 'silikon',"),
                 ("'koyu', 'silikon', 'dış kabuk ek yeri silikonu (taban / arka / tavan)')", "'yapistirici', 'silikon', 'dış kabuk ek yeri silikonu (taban / arka / tavan)')"),
                 ("'10 × ISO 4762 M8 cıvata → perçin somun'", "'10 × ISO 4762 M8 × 16 cıvata → kapalı uçlu perçin somun'"),
                 ("olay(tt, 'Tezgâhta TIG: %s' % P[tezgah_kaynak[0]]['ac'])", "olay(tt, 'Tezgâhta: %s' % P[tezgah_kaynak[0]]['ac'])")]:
    assert old in s, old[:40]; s = s.replace(old, new)
s = s.replace("        if ilk is None: ilk = (y, yol, s)", "        if ilk is None: ilk = (y, yol, s)\n        TUMS.append((str(y), s[:3]))")
s = s.replace("    ilk = None\n    for y in adaylar:", "    ilk = None; TUMS = []\n    for y in adaylar:")
s = s.replace("    PLAN_SORUN.append(dict(parca=adlar, yon=str(ilk[0]), sorun=ilk[2][:4]))", "    PLAN_SORUN.append(dict(parca=adlar[:3], yon=str(ilk[0]), sorun=ilk[2][:4], tum=TUMS))")
s = s.replace("olay(tt, '%s · PEM presleme: %s' % (P[a0]['ac'], ' + '.join(P[p]['ac'] for p in pem)))", "olay(tt, '%s · PEM presleme: %s' % (P[a0]['ac'], ' + '.join((('%d × ' % n_) if n_ > 1 else '') + k_ for k_, n_ in __import__('collections').Counter(P[p]['ac'] for p in pem).items())))")
assert "Counter(P[p]['ac'] for p in pem)" in s
a = s.index("# ================================================================== PLAN")  # TUM_SORUN
s = s[:a] + io.open('plan_v4.py', encoding='utf-8').read()
io.open('b4_montaj.py', 'w', encoding='utf-8', newline='').write(s)
print('ok')
