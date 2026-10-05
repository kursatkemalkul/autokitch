import os, sys, time
S_=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.join(S_,"sac_standart")
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_topping_sac_v1 as M
G=M.kur()
L=M.govde_parcalari()
x0,x1,y0,y1,z0,z1=M.ZARF
for p in L:
    b=p['sh'].BoundingBox()
    if b.xmin<x0-0.5 or b.xmax>x1+0.5 or b.ymin<y0-0.5 or b.ymax>y1+0.5 or b.zmin<z0-0.5 or b.zmax>z1+0.5:
        print(p['ad'], round(b.xmin,2),round(b.xmax,2),round(b.ymin,2),round(b.ymax,2),round(b.zmin,2),round(b.zmax,2))
sys.stdout.flush(); os._exit(0)

