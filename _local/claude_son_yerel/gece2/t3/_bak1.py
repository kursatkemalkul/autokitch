import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('t3_parca.pkl','rb'))['P']
for a in sorted(D):
    if any(k in a for k in ('kaset','uno_','evaporator','x_ekseni','x_sensor','kondenser','sogutma_grubu','servis_cihaz','soguk_alt','raf','esik','dil_kan','dusme','kuru_bolme','yogusma','pu_')):
        V=D[a]['V']; print('%-28s %s %s' % (a, np.round(V.min(0),1).tolist(), np.round(V.max(0),1).tolist()))
