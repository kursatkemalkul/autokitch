import numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
B=Bolge(EN,(1975,880,-832),(2500,2150,-560))
for p in [(2270,920,-812),(2315,920,-812),(2270,920,-800),(2270,950,-790),(2315,960,-780)]:
    print(p, B.mesafe(np.array([p],float)))
# en yakin engel ucgeni
for p in [(2270,920,-812),(2315,920,-812)]:
    d,i=EN.seg_mesafe(np.array(p,float),np.array(p,float)+0.01,20)
    import json; PJ=json.load(open('e1c/m8_parca.json',encoding='utf-8')); print(p,d,PJ['parca'][EN.P[i]]['ad'] if EN.P[i]>=0 else 'yeni', PJ['parca'][EN.P[i]]['lo'] if EN.P[i]>=0 else '', PJ['parca'][EN.P[i]]['hi'] if EN.P[i]>=0 else '')
