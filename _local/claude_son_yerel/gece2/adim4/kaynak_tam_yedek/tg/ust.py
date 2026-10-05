import sys; sys.path.insert(0,'.')
from glbx import yukle, aralik_maske
import numpy as np
J,D=yukle('../hat3_v8n.glb')
for ad,d in D.items():
    if not ad.startswith('TOPPING_MODUL'): continue
    X,T,ok=d['X'],d['T'],d['ok']; P=X[T]
    kp=aralik_maske(d['ex'].get('kpk',[]),len(T))
    m=ok&(P[...,1].min(1)>2150)
    if m.any():
        for kk in (True,False):
            mm=m&(kp==kk)
            if mm.any():
                Q=P[mm].reshape(-1,3); print(ad,'kpk' if kk else '   ',mm.sum(),Q.min(0).round(1),Q.max(0).round(1))
    if kp.any():
        Q=P[kp&ok].reshape(-1,3); print('  KPK',ad,(kp&ok).sum(),Q.min(0).round(1),Q.max(0).round(1))
