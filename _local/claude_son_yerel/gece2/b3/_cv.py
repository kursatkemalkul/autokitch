import pickle, numpy as np, sys
sys.path.insert(0,r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D=pickle.load(open('plan_b3.pkl','rb')); P=D['P']
Pm={k:dict(V=P[k]['V']/1000,F=P[k]['F']) for k in ('sase_civata','percin_sase','sase_capraz_1406','sase_boy_on','sase_boy_arka')}
print(Y.son_kesisim(Pm,list(Pm)))
V=P['sase_civata']['V']; print(np.unique(np.round(V[:,1],2))[:12])
V=P['percin_sase']['V']; print('percin y', np.unique(np.round(V[:,1],2))[:12], V[:,1].max())
