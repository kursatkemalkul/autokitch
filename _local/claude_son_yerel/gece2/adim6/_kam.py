s=open('g6_montaj.py',encoding='utf-8').read()
a=s.index("def kam(t, adlar=None"); b=s.index("def adim(no, ad")
yeni='''def _fit(lo, hi):
    w = hi - lo
    span = max(w[1] * 1.1, (w[0] + w[2] * 0.5) / 1.9, 0.25)
    return span * 2.18 + w[2] / 2


def kam(t, adlar=None, d=(0, 1, 0), uzak=None, yon=None):
    genel = _fit(ZARF[0], ZARF[1])
    if adlar:
        lo, hi = bbox(adlar); h = (lo + hi) / 2
    else:
        lo, hi = ZARF[0], ZARF[1]; h = MERKEZ.copy()
    if yon is None:
        d = np.array(d, float); yon = np.array([0.55, 0.5, 1.0])
        if abs(d[2]) > 1e-9 and d[2] < 0 and abs(d[2]) >= abs(d[0]): yon = np.array([0.6, 0.5, -1.0])
        elif abs(d[0]) > abs(d[2]) and abs(d[0]) > 1e-9: yon = np.array([1.0 * np.sign(d[0]), 0.55, 0.75])
    yon = np.array(yon, float); yon /= np.linalg.norm(yon)
    dist = uzak * 1.6 if uzak else min(max(_fit(lo, hi), genel * 0.45), genel * 1.05)
    pos = h + yon * dist
    pos[1] = max(pos[1], 0.25)
    KAM.append([round(t, 2), [round(float(v), 4) for v in pos], [round(float(v), 4) for v in h]])


'''
s=s[:a]+yeni+s[b:]
open('g6_montaj.py','w',encoding='utf-8').write(s)
