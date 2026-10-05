import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']; MEK=B['MEK']
def kod(o): return MEK[o['mek']]['kod'] if o['mek']>=0 else ''
for nm,(lo,hi) in {'L':((1446,1109,-826),(1682,1282,-630)),'R':((1758,1109,-826),(2223,1383,-630))}.items():
    print('=== under evap',nm)
    for o in L:
        if np.all(o['hi']>np.array(lo)) and np.all(o['lo']<np.array(hi)) and not o['dug'].startswith('TOPPING_GOVDE'):
            print('  %-30s %-18s %s %s' % (o['dug'][:30], kod(o), np.round(o['lo']).astype(int).tolist(), np.round(o['hi']).astype(int).tolist()))
print('=== evap bottoms')
for o in L:
    if kod(o)=='TOPPING/Soğutma' and o['lo'][1]>1270 and o['lo'][1]<1400 and o['lo'][2]<-600:
        print('  %-30s %s %s %d' % (o['dug'][:30], np.round(o['lo'],1).tolist(), np.round(o['hi'],1).tolist(), len(o['F'])))
