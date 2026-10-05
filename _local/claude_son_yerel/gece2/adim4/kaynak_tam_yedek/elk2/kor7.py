import numpy as np, json
from elib import *
EN=Engel('e1c/m8_onbellek.npz'); PJ=json.load(open('e1c/m8_parca.json',encoding='utf-8'))
B=Bolge(EN,(4970,10,668),(5410,260,1080))
def chk(Q):
    Q=[np.array(q,float) for q in Q]; out=[]
    for a,b in zip(Q[:-1],Q[1:]):
        P=np.array([a+(b-a)*t for t in np.linspace(0,1,max(2,int(np.linalg.norm(b-a))+1))]); d=B.mesafe(P); j=np.argmin(d)
        out.append((round(float(d[j]),1), P[j].round().tolist()))
    return out
print(chk([(5165,120,672),(5165,120,690),(5165,90,690),(5165,90,1032),(4996.2,90,1032)]))
print(chk([(5210,120,672),(5210,120,700),(5210,39.3,700),(5210,39.3,1019.6),(4995,39.3,1019.6)]))
for p in [(5165,90,800),(5210,39,800),(5100,90,1032),(5100,39,1019)]:
    p=np.array(p,float); dd,i=EN.seg_mesafe(p,p+0.01,30); i=int(i); q=PJ['parca'][EN.P[i]]; print(p,round(dd,1),q['ad'],q['lo'],q['hi'])
