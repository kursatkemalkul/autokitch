import sys, os, json, pickle, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BIL = pickle.load(open('e_bil.pkl', 'rb')); L = BIL['L']
O = json.load(open('e_envanter.json', encoding='utf-8')); BY = {r['i']: r for r in O}
fam = sys.argv[1]; out = sys.argv[2]
R = [r for r in O if r['dug'].startswith(fam) or (fam == 'E_ELEKTRIK' and r['dug'].startswith('E_ELEKTRIK'))]
lo = np.min([r['lo'] for r in R], 0); hi = np.max([r['hi'] for r in R], 0)
fig, ax = plt.subplots(1, 3, figsize=(30, 11))
views = [((0, 1), 'x', 'y (önden, +z bakış)'), ((2, 1), 'z', 'y (yandan)'), ((0, 2), 'x', 'z (üstten)')]
cols = plt.cm.tab20(np.linspace(0, 1, 20))
for k, ((a, b), la, lb) in enumerate(views):
    for n, r in enumerate(R):
        o = L[r['i']]; V = o['V']; F = o['F']; T = V[F]
        # ışık: üçgen normalinin görünüm eksenine izdüşümü
        c = cols[n % 20]
        pc = PolyCollection(T[:, :, [a, b]], facecolors=[c], edgecolors='none', alpha=0.55)
        ax[k].add_collection(pc)
        ctr = (o['lo'] + o['hi']) / 2
        ax[k].text(ctr[a], ctr[b], str(r['i']), fontsize=7, ha='center', va='center', color='k')
    ax[k].set_xlim(lo[a] - 20, hi[a] + 20); ax[k].set_ylim(lo[b] - 20, hi[b] + 20); ax[k].set_aspect('equal'); ax[k].set_title('%s · %s / %s' % (fam, la, lb)); ax[k].grid(True, lw=0.3)
plt.tight_layout(); plt.savefig(out, dpi=70)
print(out, len(R))
