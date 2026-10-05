import pickle, numpy as np, sys
sys.path.insert(0,r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D=pickle.load(open('plan_b3.pkl','rb')); P=D['P']
for a,b in [('g_kosebent_sag_ust_2','g_tk_depo_sag_pu'),('g_kosebent_sag_ust_2','g_tk_depo_arka_pu'),('g_kosebent_sag_ust_1','g_tk_ara_arka_sac'),('g_kosebent_sag_ust_1','g_tk_depo_arka_pu')]:
    Pm={k:dict(V=P[k]['V']/1000,F=P[k]['F']) for k in (a,b)}
    print(a,b,Y.son_kesisim(Pm,[a,b], 3e-4), np.round(P[a]['V'].min(0),2), np.round(P[a]['V'].max(0),2), np.round(P[b]['V'].min(0),2), np.round(P[b]['V'].max(0),2))
