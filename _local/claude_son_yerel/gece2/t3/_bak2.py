import pickle, numpy as np, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']; MEK=B['MEK']
def kod(o): return MEK[o['mek']]['kod'] if o['mek']>=0 else ''
for kd in ('TOPPING/Kaşar','TOPPING/Sos','TOPPING/Harç','TOPPING/Kıyma'):
    print('==',kd)
    for o in sorted([o for o in L if kod(o)==kd and o['lo'][1]<1152], key=lambda o:o['lo'][1]):
        print('  %-34s %s %s %d' % (o['dug'], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
print('== evap feet / soğutma near servis')
for o in L:
    if kod(o)=='TOPPING/Soğutma' and o['lo'][2]<-826 :
        print('  %-34s %s %s %d' % (o['dug'], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
