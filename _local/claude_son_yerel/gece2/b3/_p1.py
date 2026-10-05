import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('b3_parca.pkl','rb')); P=D['P']
pus=[a for a in P if P[a]['tur']=='pu']
for a in sorted(pus):
    V=P[a]['V']; print('%-32s F%6d lo %s hi %s'%(a,len(P[a]['F']),np.round(V.min(0),1),np.round(V.max(0),1)))
for a in sorted(P):
    if a.startswith(('g_kosebent','g_dis_','g_ic_','g_tk','g_isi','g_teknik')) and P[a]['tur']!='pu':
        V=P[a]['V']; print('S %-30s lo %s hi %s'%(a,np.round(V.min(0),1),np.round(V.max(0),1)))
