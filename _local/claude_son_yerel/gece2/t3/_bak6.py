import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']; MEK=B['MEK']
def kod(o): return MEK[o['mek']]['kod'] if o['mek']>=0 else ''
for o in L:
    if kod(o)=='TOPPING/Soğutma' and o['lo'][0] > 2010 and o['hi'][0] < 2280 and o['hi'][1] < 1400 and o['dug'] in ('TOPPING_MODUL__koyu', 'TOPPING_MODUL__celik', 'TOPPING_MODUL__sac'):
        print('%-26s %s %s %d' % (o['dug'], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
print('--- X ekseni')
for o in sorted([o for o in L if kod(o)=='TOPPING/Tabla'], key=lambda o:o['lo'][0]):
    print('%-26s %s %s %d' % (o['dug'], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
