import pickle, sys, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('t_bil_v9l.pkl', 'rb')); MEK = D['MEK']
mk = [int(x) for x in sys.argv[1].split(',')]
for o in sorted([o for o in D['L'] if o['mek'] in mk], key=lambda o: (o['mek'], o['dug'], round(o['lo'][2]), round(o['lo'][1]))):
    e = o['hi'] - o['lo']
    print('%2d %-44s lo %s hi %s ext %s n%d' % (o['mek'], o['dug'][:44], np.round(o['lo']).astype(int).tolist(), np.round(o['hi']).astype(int).tolist(), np.round(e, 1).tolist(), len(o['F'])))
