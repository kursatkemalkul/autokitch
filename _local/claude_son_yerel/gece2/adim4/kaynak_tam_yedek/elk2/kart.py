import numpy as np
from elib import *
EN=Engel('e1c/m8_onbellek.npz')
B=Bolge(EN,(4935,1640,780),(5420,2060,1110))
S=np.array((4940,1875,840.)); S1=np.array((4955,1875,840.))
for E in [(5250,1850,1079),(5300,1850,1079),(5160,1850,1079)]:
    E=np.array(E,float); E1=E+np.array((0,10,0))
    print(E, B.mesafe(E1[None]), B.mesafe(S1[None]))
    Q=izgara_yol(B,S1,E1,4.35,adim=2)
    print(Q if Q is None else [q.round(1).tolist() for q in Q])
    if Q: print([B.seg_ok(a,b,4.35) for a,b in zip(Q[:-1],Q[1:])])
