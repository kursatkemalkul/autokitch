import os,sys,numpy as np
sys.path.insert(0,r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3\yama_v9')
import sac_ent as SE
from m8kit import Glb
g=Glb('../../hat3_v9k.glb')
for d in ['CEK_K1_lahm_1__celik__CEKMECE','CEK_K1_lahm_1__celik']:
    g.bilesen(d,0)
    for b in g._bc[d]: print(d,b['no'],b['kapali'],np.round(b['lo'],2),np.round(b['hi']-b['lo'],2))
