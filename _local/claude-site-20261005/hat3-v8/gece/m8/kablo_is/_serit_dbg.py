import sys,os,pickle,numpy as np,collections
sys.path.insert(0,'.');sys.path.insert(0,'../..')
import glbkit
G=glbkit.Glb('../../../hat3_v8x.glb')
K=pickle.load(open('_kay.pkl','rb'))
d=[x for x in K if x['id']=='ELK_K__kablo#2'][0]
p=G.prims[d['pid']]; Tc=p['X'][p['T'][d['tri_idx']]]
E = np.stack([Tc[:, 1] - Tc[:, 0], Tc[:, 2] - Tc[:, 1], Tc[:, 0] - Tc[:, 2]], 1)
Ln = np.linalg.norm(E, axis=2)
ic = np.argmin(Ln, 1); n=len(Tc); idx=np.arange(n)
c = E[idx, ic] / np.maximum(Ln[idx, ic], 1e-9)[:, None]
o1 = (ic + 1) % 3; o2 = (ic + 2) % 3
d1 = E[idx, o1] / np.maximum(Ln[idx, o1], 1e-9)[:, None]; d2 = E[idx, o2] / np.maximum(Ln[idx, o2], 1e-9)[:, None]
p1 = np.abs((d1 * c).sum(1)); p2 = np.abs((d2 * c).sum(1))
ax_i = np.where(p1 < p2, o1, o2)
D = E[idx, ax_i] / np.maximum(Ln[idx, ax_i], 1e-9)[:, None]; LA = Ln[idx, ax_i]
perp = np.minimum(p1, p2) < 0.02
print('perp',perp.sum(),'LA',(LA>1.5).sum(),'ratio',(LA > 1.8 * Ln[idx, ic]).sum())
ok = perp & (LA > 1.5) & (LA > 1.8 * Ln[idx, ic])
print(ok.sum())
sg = np.sign(D[np.arange(n), np.argmax(np.abs(D), 1)]); D = D * sg[:, None]
q = np.round(D * 60).astype(int)
print(collections.Counter(map(tuple,q[ok])).most_common(10))
print(np.histogram(np.minimum(p1,p2)[LA>10],bins=[0,0.001,0.005,0.01,0.02,0.05,0.1,0.5,1])[0])
