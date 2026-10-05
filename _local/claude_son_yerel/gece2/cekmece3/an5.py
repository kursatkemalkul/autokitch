import sys,numpy as np,pickle
sys.stdout.reconfigure(encoding='utf-8')
O=pickle.load(open('cek_comp.pkl','rb'))
def refs(c):
    L=sorted([x for x in O[c] if x[0]=='celik' and abs((x[2]-x[1])[0]-8.5)<0.1 and (x[2]-x[1])[2]>500], key=lambda r:r[1][0]); return L[0][1],L[-1][1]
for c in ['CEK_K2_lahm_5','CEK_K6_ic1_1','CEK_K1_lahm_5']:
    R,Rr=refs(c)
    for x in O[c]:
        o=x[1]-R
        if x[0] in ('celik','celik__CEKMECE') and (o[0]<40 or x[1][0]>Rr[0]-30): print(c,x[0],np.round(o,2).tolist(),np.round(x[2]-x[1],2).tolist(),x[3])
# right lama / braket offsets rel right ray
for c in O:
    R,Rr=refs(c)
    r=[ (np.round(x[1]-Rr,2).tolist(),np.round(x[2]-x[1],2).tolist()) for x in O[c] if x[0]=='celik__CEKMECE' and x[1][0]>Rr[0]-30]
    print(c, r)
