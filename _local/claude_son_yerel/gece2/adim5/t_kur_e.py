import os, sys, time
os.environ["ADIM5"] = os.path.dirname(os.path.abspath(__file__))
os.environ["AUTOKITCH_SAC_STANDART"] = os.path.abspath(os.path.join(os.environ["ADIM5"], "..", "..", "sac_standart"))
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_e_sac_v1 as E
t=time.time(); g = E.kur()
P = E.govde_parcalari(g)
print(len(P), "parça", time.time()-t)
for m in g.MEK_ATLA[:40]: print("ATLA", m)
for m in g.MEK_SAPLAMA[:80]: print("SAP", m)
sys.stdout.flush(); os._exit(0)
