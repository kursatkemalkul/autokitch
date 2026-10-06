# -*- coding: utf-8 -*-
"""E mekanizma ENVANTERİ (6 Eki 2026 · Claude · 2. oturum · görev 4.1)
Girdi: e_bil.pkl (e_cikar.py: hat3_v10l bileşenleri) + e_parca.pkl (e_parca.py grupları).
Mekanizma düğümleri (E_KALIP, E_KAPAK, E_KOPRU, E_KOSE, E_PARMAK, E_PISTON, E_BESLEYICI, E_ELEKTRIK sensörleri) bileşen bileşen:
  ne olduğu (motor / sensör / kayış / profil / ray / mil / plaka-braket / blok-kızak / sac / burç / vantuz), kutusu, hangi e_parca grubunda,
  neye değdiği (≤ 0,6 mm: komşu mekanizma bileşenleri + gövde parçaları + arayüz saplamaları) ve temas yüzü (eksen + örtüşme dikdörtgeni),
  vidası var mı (bağlantı elemanı değiyor mu).
Çıktı: e_envanter.json (bileşen listesi) + e_envanter.md (özet tablo) + e_envanter_grup.txt (grup grup ayrıntı). Yalnız analiz; model değişmez.
Kullanım: python e_envanter.py"""
import os, sys, json, pickle, re, collections, time
import numpy as np
import trimesh
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.stdout.reconfigure(encoding='utf-8')
T0 = time.time()
BIL = pickle.load(open('e_bil.pkl', 'rb')); MEK = BIL['MEK']; L = BIL['L']
P = pickle.load(open('e_parca.pkl', 'rb'))['P']
MEKDUG = ('E_KALIP', 'E_KAPAK', 'E_KOPRU', 'E_KOSE', 'E_PARMAK', 'E_PISTON', 'E_BESLEYICI')
TOL = 0.6


def kod(o): return MEK[o['mek']]['kod'] if o['mek'] >= 0 else ''


def mek_mi(o):
    d = o['dug']
    if d.startswith(MEKDUG): return True
    return d.startswith('E_ELEKTRIK') and d.endswith(('__sensor', '__aluminyum')) and o['lo'][1] < 1300   # mekanizma uç sensörleri (e_parca: elk_sensor)


# ---------------------------------------------------------------- e_parca grubu: bileşenin köşeleri hangi P parçasında (KD ağacı, 1e-3)
GRUP = {}
KD = {a: cKDTree(P[a]['V']) for a in P if P[a]['tur'] in ('mek', 'kablo', 'sac', 'profil')}
PLO = {a: P[a]['V'].min(0) for a in KD}; PHI = {a: P[a]['V'].max(0) for a in KD}
for i, o in enumerate(L):
    if not mek_mi(o): continue
    q = o['V'][:: max(1, len(o['V']) // 20)][:20]
    g = []
    for a in KD:
        if np.any(o['lo'] < PLO[a] - 0.01) or np.any(o['hi'] > PHI[a] + 0.01): continue
        d, _ = KD[a].query(q, distance_upper_bound=1e-3)
        if np.all(np.isfinite(d)): g.append(a)
    GRUP[i] = g[0] if g else '-'

# ---------------------------------------------------------------- geometri sınıfı
def sinif(o):
    d = o['dug']; lo, hi = o['lo'], o['hi']; ext = hi - lo; s = np.sort(ext); e = int(np.argmax(ext))
    mal = d.split('__')[1] if '__' in d else ''
    son = d.split('__')[-1]
    if mal == 'motor': return 'motor (hazır ürün)'
    if mal == 'sensor' or son == 'sensor': return 'sensör (hazır ürün)'
    if mal == 'kayis': return 'kayış'
    if mal == 'bronz': return 'bronz burç / yatak'
    if mal == 'plastik': return 'plastik parça'
    if mal == 'vakum_kaucuk': return 'vantuz / vakum hortumu'
    if son == 'KOL': return 'kol (kapak katlama)'
    if son.startswith('CNR_'): return 'köşe tutucu çenesi'
    if son == 'PARMAK': return 'parmak'
    V = o['V']; oth = [i for i in range(3) if i != e]; c = (lo + hi) / 2
    r = np.linalg.norm(V[:, oth] - c[oth], axis=1); sil = (abs(ext[oth[0]] - ext[oth[1]]) < 0.15 * max(ext[oth]) + 0.5) and (r.max() > 0) and ((r.max() - np.percentile(r, 5)) / r.max() < 0.35)
    if mal == 'sac' or (s[0] <= 2.0 and s[1] > 20): return 'sac %g' % round(s[0], 1)
    if sil and s[2] > 2.5 * s[1]: return 'mil / boru Ø%g' % round(s[1], 1)
    if s[2] > 4 * s[1] and 15 <= s[1] <= 65 and abs(s[1] - s[0]) < 0.35 * s[1]: return ('alüminyum profil %g × %g' if mal == 'aluminyum' else 'profil / boru %g × %g') % (round(s[0]), round(s[1]))
    if s[2] > 4 * s[1] and s[0] <= 25: return ('lineer ray %g × %g' if mal == 'celik' else 'çubuk / lama %g × %g') % (round(s[0]), round(s[1]))
    if s[0] <= 12 and s[1] > 3 * s[0]: return ('%s plaka / braket t%g' % ('alüminyum' if mal == 'aluminyum' else 'çelik', round(s[0], 1)))
    return ('%s blok / kızak' % ('alüminyum' if mal == 'aluminyum' else 'çelik'))


# ---------------------------------------------------------------- temas (≤ 0,6 mm) — bütün E bileşenleri + gövde
IDX = [i for i, o in enumerate(L) if mek_mi(o)]
LO = np.array([o['lo'] for o in L]); HI = np.array([o['hi'] for o in L])
TM = {}


def tm(i):
    if i not in TM:
        o = L[i]; TM[i] = trimesh.Trimesh(o['V'], o['F'], process=False)
    return TM[i]


def degiyor(i, j):
    for p, q in ((i, j), (j, i)):
        Q = L[p]['V']; m = np.all(Q >= LO[q] - TOL, 1) & np.all(Q <= HI[q] + TOL, 1)
        if m.any():
            Q = Q[m]
            if len(Q) > 3000: Q = Q[np.linspace(0, len(Q) - 1, 3000).astype(int)]
            _, d, _ = trimesh.proximity.closest_point(tm(q), Q)
            if d.min() <= TOL: return True
    return False


def temas_yuzu(i, j):
    """kutu bitişikliği: eksen (x/y/z), i'nin hangi tarafı, örtüşme dikdörtgeni · bitişik değilse 'geçme' (iç içe / çapraz)"""
    out = []
    for a in range(3):
        oth = [k for k in range(3) if k != a]
        ov = [max(LO[i][k], LO[j][k]) for k in oth], [min(HI[i][k], HI[j][k]) for k in oth]
        alan = max(0.0, ov[1][0] - ov[0][0]) * max(0.0, ov[1][1] - ov[0][1])
        if abs(HI[i][a] - LO[j][a]) <= TOL: out.append(('xyz'[a] + '+', round(float(HI[i][a]), 1), alan, ov))
        if abs(HI[j][a] - LO[i][a]) <= TOL: out.append(('xyz'[a] + '-', round(float(LO[i][a]), 1), alan, ov))
    if not out: return 'geçme'
    y, c, alan, ov = max(out, key=lambda x: x[2])
    return '%s@%g %.0fmm² [%g…%g × %g…%g]' % (y, c, alan, round(ov[0][0], 1), round(ov[1][0], 1), round(ov[0][1], 1), round(ov[1][1], 1))


def baglanti_dug(d):
    return bool(re.search(r'vida|civata|VIDA|BAG__|somun|saplama|percin|PEM', d)) or d in ('E_MODULER__paslanmaz',)


OUT = []
nm = len(IDX)
for n_, i in enumerate(IDX):
    o = L[i]
    kand = np.where(np.all(LO <= HI[i] + TOL, 1) & np.all(HI >= LO[i] - TOL, 1))[0]
    tem = []
    for j in kand:
        if j == i: continue
        if degiyor(i, j): tem.append(int(j))
    ext = o['hi'] - o['lo']
    OUT.append(dict(i=int(i), dug=o['dug'], kod=kod(o), grup=GRUP.get(i, '-'), tip=sinif(o), lo=np.round(o['lo'], 1).tolist(), hi=np.round(o['hi'], 1).tolist(),
                    boyut=np.round(ext, 1).tolist(), ucgen=int(len(o['F'])), temas=tem, temas_yuz={str(j): temas_yuzu(i, j) for j in tem}))
    if n_ % 50 == 0: print('%d / %d · %.0f s' % (n_, nm, time.time() - T0), flush=True)
# ---------------------------------------------------------------- bağlantı elemanı değiyor mu
for r in OUT:
    bag = [L[j]['dug'] for j in r['temas'] if baglanti_dug(L[j]['dug']) and not L[j]['dug'].startswith(MEKDUG)]
    sap = []
    for a in [a for a in P if a.startswith('arayuz_mek')]:
        lo, hi = P[a]['V'].min(0), P[a]['V'].max(0)
        if np.all(np.array(r['hi']) >= lo - TOL) and np.all(np.array(r['lo']) <= hi + TOL):
            _, d, _ = trimesh.proximity.closest_point(tm(r['i']), P[a]['V'])
            if d.min() <= TOL: sap.append(a)
    r['saplama'] = sap
    r['bag'] = sorted(set(bag))
    r['vida'] = bool(bag) or bool(sap)
    r['temas_ad'] = sorted(set((L[j]['dug'] + ('' if GRUP.get(j, '-') == '-' else ' [%s]' % GRUP[j])) for j in r['temas']))
json.dump(OUT, open('e_envanter.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# ---------------------------------------------------------------- özet
c_grup = collections.Counter(r['grup'] for r in OUT)
c_tip = collections.Counter(r['tip'].split(' ')[0] for r in OUT)
vidali = [r for r in OUT if r['vida']]; vidasiz = [r for r in OUT if not r['vida']]
md = ['# E mekanizma envanteri (hat3_v10l · zincir 00–80) · 6 Eki 2026', '',
      '- mekanizma bileşeni: **%d** (düğüm: %s)' % (len(OUT), ', '.join('%s %d' % (k, v) for k, v in sorted(collections.Counter(r['dug'].split('__')[0] for r in OUT).items()))),
      '- bağlantı elemanı değen (vidalı / saplamalı): **%d** · değmeyen (vidasız): **%d**' % (len(vidali), len(vidasiz)),
      '- modelde mekanizma vidası düğümü: **yok** (E_* mekanizma düğümlerinde vida / somun / PEM bileşeni 0). Gövde → mekanizma arayüz saplaması (FHP M5-12 / M6-15): %d, somunu yok.' % len([a for a in P if a.startswith('arayuz_mek')]),
      '', '## Gruplar (e_parca)', '', '| grup | bileşen | vidalı | vidasız | türler |', '|---|---|---|---|---|']
for g, n in sorted(c_grup.items(), key=lambda kv: -kv[1]):
    R = [r for r in OUT if r['grup'] == g]
    ct = collections.Counter(r['tip'] for r in R)
    md.append('| %s | %d | %d | %d | %s |' % (g, n, sum(r['vida'] for r in R), sum(not r['vida'] for r in R), ', '.join('%s × %d' % (k, v) for k, v in ct.most_common())))
md += ['', '## Bileşenler', '', '| # | düğüm | grup | tür | kutu (mm) | değdiği | vida |', '|---|---|---|---|---|---|---|']
for r in sorted(OUT, key=lambda r: (r['grup'], r['dug'], r['lo'])):
    k = '%d…%d · %d…%d · %d…%d' % (r['lo'][0], r['hi'][0], r['lo'][1], r['hi'][1], r['lo'][2], r['hi'][2])
    deg = ', '.join(x.replace('E_', '') for x in r['temas_ad'][:6]) + (' …' if len(r['temas_ad']) > 6 else '')
    md.append('| %d | %s | %s | %s | %s | %s | %s |' % (r['i'], r['dug'].replace('E_', ''), r['grup'], r['tip'], k, deg, ('saplama ' + ','.join(r['saplama'])) if r['saplama'] else ('EVET ' + ','.join(r['bag']) if r['bag'] else 'YOK')))
open('e_envanter.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
# grup grup ayrıntı (temas yüzleriyle)
BY = {r['i']: r for r in OUT}
tx = []
for g in sorted(c_grup, key=lambda g: (g == '-', g)):
    tx.append('===== %s (%d)' % (g, c_grup[g]))
    for r in sorted([r for r in OUT if r['grup'] == g], key=lambda r: (r['dug'], r['lo'])):
        k = '%5d…%-5d %4d…%-4d %5d…%-5d' % (r['lo'][0], r['hi'][0], r['lo'][1], r['hi'][1], r['lo'][2], r['hi'][2])
        tx.append('%4d %-30s %-26s %s %s' % (r['i'], r['dug'][2:], r['tip'], k, ('SAP:' + ','.join(r['saplama'])) if r['saplama'] else ''))
        for j in r['temas']:
            jj = BY.get(j); ad = L[j]['dug'][2:] + (' #%d %s' % (j, jj['tip']) if jj else '') + ('' if GRUP.get(j, '-') == '-' else ' [%s]' % GRUP[j])
            tx.append('        ↔ %-70s %s' % (ad[:70], r['temas_yuz'][str(j)]))
open('e_envanter_grup.txt', 'w', encoding='utf-8').write('\n'.join(tx) + '\n')
print('bileşen %d · vidalı %d · vidasız %d · %.0f s' % (len(OUT), len(vidali), len(vidasiz), time.time() - T0))
print(c_tip.most_common())
