import sys,numpy as np,pickle
sys.stdout.reconfigure(encoding='utf-8')
O=pickle.load(open('cek_comp.pkl','rb'))
def ref(c):
    return min([x for x in O[c] if x[0]=='celik' and abs((x[2]-x[1])[0]-8.5)<0.1 and (x[2]-x[1])[2]>500], key=lambda r:r[1][0])[1]
R0=ref('CEK_K2_lahm_3')
base={}
for x in O['CEK_K2_lahm_3']:
    if x[1][0]-R0[0] < 40 or x[0] in ('motor','koyu','plastik','aluminyum'):  # sol taraf mekanizma
        base.setdefault(x[0],[]).append((np.round(x[1]-R0,2),np.round(x[2]-x[1],2),x[3]))
for k,v in base.items():
    for b in v: print('K2L3',k,b[0].tolist(),b[1].tolist(),b[2])
for c in O:
    if c=='CEK_K2_lahm_3': continue
    R=ref(c); s=set()
    for x in O[c]: s.add((x[0],tuple(np.round(x[1]-R,2)),tuple(np.round(x[2]-x[1],2))))
    miss=[]
    for k,v in base.items():
        for b in v:
            if (k,tuple(b[0]),tuple(b[1])) not in s: miss.append((k,b[0].tolist(),b[1].tolist()))
    print(c,'eksik',len(miss),miss[:6])
