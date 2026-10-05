import os, sys, json
B=os.path.dirname(os.path.abspath(__file__)); os.environ["ADIM5"]=B
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.abspath(os.path.join(B,"..","..","sac_standart"))
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_u_sac_v1 as U, h3_sac_v1 as S
GG = U.kur(lambda *a: None)
for g in GG.values():
    for s in g.SAC:
        if s.ad == sys.argv[1]:
            r = s.dogrula(); print({k: v for k, v in r.items() if k not in ("kalinlik", "kesit")})
sys.stdout.flush(); os._exit(0)
