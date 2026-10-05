import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('b3_parca.pkl','rb')); P=D['P']
for a in sorted(P):
    if a.startswith(('sase','moduler','tasiyici','gfrp','evap','sogutma','elektrik','istasyon','ic_kanal','zincir','b_kanal','g_percin','percin','g_arayuz_sase','izgara','depo','ayak','guc','kablo_klips','g_isi','takoz')):
        V=P[a]['V']; print('%-28s F%6d lo %s hi %s'%(a,len(P[a]['F']),np.round(V.min(0),1),np.round(V.max(0),1)))
