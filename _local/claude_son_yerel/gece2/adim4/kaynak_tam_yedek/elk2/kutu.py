import json,numpy as np
D=np.load('zi/m8_onbellek.npz'); PJ=json.load(open('zi/m8_parca.json',encoding='utf-8')); MEK=[m['kod'] for m in PJ['MEK']]
T=np.stack([D['A'],D['B'],D['C']],1); mek=D['mek']
for i,k in enumerate(MEK):
    m=mek==i
    if not m.any(): continue
    Q=T[m].reshape(-1,3); print('%-26s %8d  lo %s  hi %s'%(k,m.sum(),np.round(Q.min(0)).astype(int).tolist(),np.round(Q.max(0)).astype(int).tolist()))
