import os, sys, time
S_=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.join(S_,"sac_standart")
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_f_sac_v1 as M
G=M.kur()
for n in G.NOT: print("NOT", n[:300])
t=time.time(); bad=0
for s in G.SAC:
    d=s.dfm(abkant=True); h=[m for m in d if m['durum'] in ('HATA','UYARI')]
    if h:
        bad+=1; print(s.ad, [(m['kural'],m['durum'],m['detay'][:140]) for m in h][:4])
print("dfm", time.time()-t, bad)
L=M.govde_parcalari(); print(len(L))
for s in M.G.SAC:
    if 'omega_0' in s.ad or 'alt_kayit' in s.ad:
        b=s.kati().BoundingBox(); print(s.ad, round(b.xmin,1),round(b.xmax,1),round(b.ymin,1),round(b.ymax,1),round(b.zmin,1),round(b.zmax,1))
sys.stdout.flush(); os._exit(0)
