import sys, os, json, pickle, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BIL = pickle.load(open('e_bil.pkl', 'rb')); L = BIL['L']
O = json.load(open('e_envanter.json', encoding='utf-8'))
V = json.load(open(os.path.join('..', '..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', 'e_mek_parcalar.json'), encoding='utf-8'))
AD = {}
for k, v in V.items():
    AD[v['no_v10l']] = k
    for e in v.get('ek', []): AD[e['no_v10l']] = k + '+'
# kullanım: ciz_bolge.py out.png x0 y0 z0 x1 y1 z1 [kesit_eksen kesit_koord]   (kesit: o eksende koordinatın ötesindeki üçgenler atılır)
out = sys.argv[1]; lo = np.array([float(x) for x in sys.argv[2:5]]); hi = np.array([float(x) for x in sys.argv[5:8]]); onek = sys.argv[8] if len(sys.argv) > 8 else ''
R = [r for r in O if np.all(np.array(r['hi']) >= lo) and np.all(np.array(r['lo']) <= hi) and AD.get(r['i'], '?').startswith(onek)]
fig, ax = plt.subplots(1, 3, figsize=(33, 11))
views = [((0, 1), 2, +1, 'önden (+z bakış): x / y'), ((2, 1), 0, -1, 'soldan (-x bakış): z / y'), ((0, 2), 1, +1, 'üstten (+y bakış): x / z')]
cols = plt.cm.tab20(np.linspace(0, 1, 20))
for k, ((a, b), d, sg, baslik) in enumerate(views):
    polys = []; colors = []; depth = []
    for n, r in enumerate(R):
        o = L[r['i']]; T = o['V'][o['F']]
        c = (T.mean(1) >= lo) & (T.mean(1) <= hi); c = np.all(c, 1)
        if not c.any(): continue
        T = T[c]
        nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); nn = np.linalg.norm(nrm, axis=1) + 1e-12
        sh = 0.55 + 0.45 * np.abs(nrm[:, d] / nn)
        col = np.array(cols[n % 20]);
        for t, s in zip(T, sh):
            polys.append(t[:, [a, b]]); colors.append(col[:3] * s); depth.append(t[:, d].mean() * sg)
        ctr = np.clip((np.array(r['lo']) + np.array(r['hi'])) / 2, lo, hi)
        ax[k].text(ctr[a], ctr[b], '%d %s' % (r['i'], AD.get(r['i'], '?')), fontsize=6, ha='center', va='center', color='k', zorder=10,
                   bbox=dict(boxstyle='round,pad=0.1', fc='w', ec='none', alpha=0.6))
    idx = np.argsort(depth)
    pc = PolyCollection([polys[i] for i in idx], facecolors=[colors[i] for i in idx], edgecolors='none', zorder=1)
    ax[k].add_collection(pc)
    ax[k].set_xlim(lo[a], hi[a]); ax[k].set_ylim(lo[b], hi[b]); ax[k].set_aspect('equal'); ax[k].set_title(baslik); ax[k].grid(True, lw=0.3)
    ax[k].set_xticks(np.arange(np.ceil(lo[a] / 10) * 10, hi[a] + 1, 10)); ax[k].set_yticks(np.arange(np.ceil(lo[b] / 10) * 10, hi[b] + 1, 10))
    ax[k].tick_params(labelsize=6)
plt.tight_layout(); plt.savefig(out, dpi=80)
print(out, len(R))
