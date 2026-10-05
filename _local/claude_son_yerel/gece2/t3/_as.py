import os,sys
W=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec"
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(W,"h3","yama_v9","sac_standart")); sys.path.insert(0,os.path.join(W,"h3")); sys.path.insert(0,W)
import h3_topping_sac_v2 as T
T.G.SAC=[];T.G.PANEL={};T.G.ELEMAN=[];T.G.ARAYUZ=[];T.G.KAYNAK_ETIKET=[];T.G.NOT=[]
T.on_cerceve(); T.astar()
for s in T.G.SAC:
    if s.ad in ('astar_sol','astar_sag'):
        k=s.kati(); 
        for so in k.Solids(): b=so.BoundingBox(); print(s.ad, round(so.Volume(),1), [round(v,1) for v in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)])
sys.stdout.flush(); os._exit(0)
