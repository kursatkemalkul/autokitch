import os, sys, time
B=os.path.dirname(os.path.abspath(__file__)); os.environ["ADIM5"]=B
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.abspath(os.path.join(B,"..","..","sac_standart"))
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_u_sac_v1 as U
t=time.time(); GG = U.kur()
for k,g in GG.items():
    P = U.govde_parcalari(g); print(k, len(P))
    for m in g.MEK_ATLA[:30]: print("  ATLA", m)
    for m in g.MEK_SAPLAMA[:60]: print("  SAP", m)
print(time.time()-t)
sys.stdout.flush(); os._exit(0)
