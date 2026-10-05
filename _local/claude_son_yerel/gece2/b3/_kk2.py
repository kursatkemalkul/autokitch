import pickle, numpy as np, sys
sys.path.insert(0,r'..\cekmece'); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
D=pickle.load(open('plan_b3.pkl','rb')); P=D['P']
a='g_kosebent_sag_ust_2'
A=P[a]['V'][P[a]['F']]/1000
for b in ('g_tk_depo_sag_pu','g_tk_depo_arka_pu'):
    B=P[b]['V'][P[b]['F']]/1000
    for d in (0.001,0.002,0.005,0.02,0.1):
        for ax,nm in ((1,'y'),(2,'z')):
            o=np.zeros(3); o[ax]=d
            c=Y.poz_kesisim(np.ascontiguousarray(A+o),np.ascontiguousarray(B),3e-4)
            if c.sum():
                i=np.where(c)[0]; print(b,nm,d,c.sum(),np.round(A[i[:2]].mean(1)*1000,2))
# köşebent profili: x-y kesit noktaları
V=P[a]['V']; m=np.abs(V[:,2]-(-200))<300
print(np.unique(np.round(V[:,[0,1]],2),axis=0)[:40])
