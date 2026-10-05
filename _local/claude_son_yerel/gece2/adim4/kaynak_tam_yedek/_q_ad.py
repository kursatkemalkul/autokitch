import sys
sys.path.insert(0,'tg')
from glbx import yukle
J,D=yukle('hat3_v8p.glb')
for k,d in D.items():
    if k.startswith(('A_','KAIDE_A','B_','CEK_K1_lahm_1','TOPPING','U_','KAIDE')): print(k, int(d['ok'].sum()), d['ex'])
