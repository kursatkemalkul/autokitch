# -*- coding: utf-8 -*-
"""K extraction: local step73 → k_bil.pkl (mm, dünya). mek TOPPING/* olan tüm üçgenler (kutu dışı dahil: X ekseni A içine uzanır) + bölgedeki diğerleri (çevre)."""
from pathlib import Path
import sys, os, pickle, json, hashlib, numpy as np, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, str(Path(HERE).parents[2] / '_local/claude_son_yerel/gece2/cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
t0 = time.time()
source=Path(sys.argv[1]);target=Path(sys.argv[2]);manifest=target.with_suffix('.json')
stat=source.stat(); signature={'path':str(source.resolve()),'size':stat.st_size,'mtime_ns':stat.st_mtime_ns}
if target.exists() and manifest.exists() and json.loads(manifest.read_text(encoding='utf-8')).get('source')==signature:
    print('K cache unchanged; full model not read');sys.exit(0)
g=G(str(source));MEK=g.MEK
TOP = np.array([i for i, m in enumerate(MEK) if m['kod'].startswith('K/')])
lo0 = np.array([3980, 740, -880.]); hi0 = np.array([4420, 2220, 160.])
OUT = []
for ni, nd in enumerate(g.J['nodes']):
    if 'mesh' not in nd or ni not in g.W: continue
    M = g.W[ni]; sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    if sc < 0.01: continue
    for pi, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        P = X[T]
        m = (np.all(P.max(1) >= lo0, 1) & np.all(P.min(1) <= hi0, 1)) | np.isin(mek, TOP)
        if not m.any(): continue
        ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1); m &= ar > 1e-9
        idx = np.where(m)[0]; Tm = T[idx]; mk = mek[idx]
        if not len(Tm): continue
        cl = bilesen(X, Tm)
        for k in np.unique(cl):
            sel = cl == k; Tc = Tm[sel]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True); V = X[u]
            OUT.append(dict(dug=nd['name'], pi=pi, mek=int(np.bincount(mk[sel] + 1).argmax() - 1), ti=idx[sel], V=V, F=inv.reshape(-1, 3), lo=V.min(0), hi=V.max(0)))
print(len(OUT), 'bileşen', round(time.time() - t0, 1), 's')
c = collections.Counter((o['dug'], o['mek']) for o in OUT)
for k, n in sorted(c.items()):
    L = [o for o in OUT if (o['dug'], o['mek']) == k]; lo = np.min([o['lo'] for o in L], 0); hi = np.max([o['hi'] for o in L], 0)
    print(n, k, MEK[k[1]]['kod'] if k[1] >= 0 else '-', np.round(lo), np.round(hi), sum(len(o['F']) for o in L))
pickle.dump(dict(MEK=MEK, L=OUT), open(sys.argv[2], 'wb'))

manifest.write_text(json.dumps({"source":signature,"components":len(OUT),"triangles":sum(len(o["F"]) for o in OUT),"seconds":round(time.time()-t0,3),"unit":"mm"},indent=2),encoding="utf-8")
