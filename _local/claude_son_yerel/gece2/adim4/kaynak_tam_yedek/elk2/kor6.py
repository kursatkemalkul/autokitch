import numpy as np, json
from elib import *
EN=Engel('e1c/m8_onbellek.npz'); PJ=json.load(open('e1c/m8_parca.json',encoding='utf-8'))
B=Bolge(EN,(1975,880,-832),(2500,2150,-560))
def chk(Q,r):
    Q=[np.array(q,float) for q in Q]; out=[]
    for a,b in zip(Q[:-1],Q[1:]):
        P=np.array([a+(b-a)*t for t in np.linspace(0,1,max(2,int(np.linalg.norm(b-a))+1))]); d=B.mesafe(P); j=np.argmin(d)
        out.append((round(float(d[j]),1), P[j].round().tolist()))
    return out
P=[(2270,920,-828.5),(2270,920,-812),(2270,940,-812),(2270,940,-645),(2431,940,-645),(2431,2120,-645),(2431,2120,-689),(1980,2120,-689),(1980,2120,-708)]
D=[(2315,920,-828.5),(2315,920,-812),(2315,965,-812),(2315,965,-668),(2431,965,-668),(2431,2090,-668),(2431,2090,-689),(1980,2090,-689),(1980,2090,-708)]
print(chk(P,7.5)); print(chk(D,4.35))
for x in (2400,2410,2415,2418,2420,2422,2425):
  p=np.array((x,940,-645.));dd,i=EN.seg_mesafe(p,p+0.01,12); q=PJ['parca'][EN.P[i]] if EN.P[i]>=0 else {}; print(x,round(dd,1),q.get('ad'),q.get('lo'),q.get('hi'))
