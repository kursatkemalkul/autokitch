import pickle, numpy as np, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']; MEK=B['MEK']
def kod(o): return MEK[o['mek']]['kod'] if o['mek']>=0 else ''
for kd in ('TOPPING/Sucuk','TOPPING/Sos','TOPPING/Harç'):
    print('==',kd)
    for o in sorted([o for o in L if kod(o)==kd and o['lo'][1]<1240], key=lambda o:o['lo'][1]):
        print('  %-34s %s %s %d' % (o['dug'], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
D = pickle.load(open('t3_parca.pkl','rb'))['P']
import trimesh
r = D['raf']; m = trimesh.Trimesh(r['V'], r['F'])
for p in [(2050,1150.5,-190),(2088,1150.5,-190),(2125,1150.5,-190),(2088,1150.5,-170),(2051,1150.5,-150)]:
    print(p, m.contains([p])[0])
