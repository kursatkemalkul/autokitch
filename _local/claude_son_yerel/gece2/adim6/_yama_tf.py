# g6_montaj.py'ye TOPPING + F ekler (bir kez çalışır)
s = open('g6_montaj.py', encoding='utf-8').read()
assert 'seq_TOPPING' not in s
eski = """ANA = pickle.load(open(os.path.join(HERE, 'ana_%s.pkl' % IST), 'rb'))
ANA_BILGI = {}
for g in ANA:
    ad = 'M__%s__%d%s' % (g['dugum'], g['mek'], '_k' if g['kpk'] else '')
    V, F = g['V'].astype(np.float64), g['F'].astype(np.int64)
    n = len(F)
    hedef = n if n <= 600 else min(int(600 + 0.25 * (n - 600)), int(3500 + 0.05 * n))
    V, F = sadele(V, F, hedef)
    k = kat_ana(g['mat'], g['dugum'], g['mek_kod'])
    P[ad] = dict(V=V, F=F, m=k, kay='ana', tur=k, birim=g['mek_kod'])
    ANA_BILGI[ad] = dict(dugum=g['dugum'], mek=g['mek_kod'], kpk=g['kpk'], ucgen0=n, ucgen=len(F))
"""
yeni = """ANA = pickle.load(open(os.path.join(HERE, 'ana_%s.pkl' % IST), 'rb'))
ANA_BILGI = {}
KUMELE = IST in ('TOPPING', 'F')       # TOPPING / F: ana grup → bağlı bileşen kümeleri (kart, kutu, evaporatör ayrı ayrı yerleşsin)
if KUMELE:
    from _kume import kumele


def _ana_ekle(ad, g, V, F, kume=None):
    n = len(F)
    hedef = n if n <= 600 else min(int(600 + 0.25 * (n - 600)), int(3500 + 0.05 * n))
    V, F = sadele(V, F, hedef)
    k = kat_ana(g['mat'], g['dugum'], g['mek_kod'])
    if g['dugum'] == 'F_UST_KABIN__plastik': k = 'fis'          # rakor gövdeleri
    P[ad] = dict(V=V, F=F, m=k, kay='ana', tur=k, birim=g['mek_kod'])
    ANA_BILGI[ad] = dict(dugum=g['dugum'], mek=g['mek_kod'], kpk=g['kpk'], ucgen0=n, ucgen=len(F))
    if kume is not None: ANA_BILGI[ad]['kume'] = kume


for g in ANA:
    ad = 'M__%s__%d%s' % (g['dugum'], g['mek'], '_k' if g['kpk'] else '')
    V, F = g['V'].astype(np.float64), g['F'].astype(np.int64)
    ks = kumele(V, F) if KUMELE else [None]
    if len(ks) == 1 or len(ks) > 60:
        _ana_ekle(ad, g, V, F)
    else:
        ks = sorted(ks, key=lambda s: tuple(np.round(V[F[s]].reshape(-1, 3).min(0), 3)))
        for i, s in enumerate(ks):
            Fi = F[s]; u, inv = np.unique(Fi.reshape(-1), return_inverse=True)
            _ana_ekle('%s__c%02d' % (ad, i), g, V[u], inv.reshape(-1, 3), i)
"""
assert eski in s; s = s.replace(eski, yeni)
eski = "MERKEZ = ZARF.mean(0); BOY"
yeni = """if IST == 'F':     # F sacı fırının üstünde; kamera fırını da kapsasın
    ZARF = np.array([np.min([P[a]['V'].min(0) for a in P], 0), np.max([P[a]['V'].max(0) for a in P], 0)])
MERKEZ = ZARF.mean(0); BOY"""
assert eski in s; s = s.replace(eski, yeni)
ek = open('seq_tf.py', encoding='utf-8').read()
eski = "SEQ = {'A': seq_A, 'B': seq_B, 'E': seq_E, 'U': seq_U}"
assert eski in s
s = s.replace(eski, ek + "\n\nSEQ = {'A': seq_A, 'B': seq_B, 'E': seq_E, 'U': seq_U, 'TOPPING': seq_TOPPING, 'F': seq_F}")
s = s.replace('"""adım 6 · istasyon montaj animasyonu verisi (A, B, E, U)', '"""adım 6 · istasyon montaj animasyonu verisi (A, B, E, U, TOPPING, F)', 1)
open('g6_montaj.py', 'w', encoding='utf-8').write(s)
print('tamam')
