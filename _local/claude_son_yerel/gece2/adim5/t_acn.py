import os, sys, json
B=os.path.dirname(os.path.abspath(__file__)); os.environ["ADIM5"]=B
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.abspath(os.path.join(B,"..","..","sac_standart"))
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_u_sac_v1 as U, h3_sac_v1 as S
GG = U.kur(lambda *a: None)
s = [x for x in GG["U_KE"].SAC if x.ad == sys.argv[1]][0]
A = s.kati_temel(); acn = s.acinim()
C, rap = S.acinimdan_kati(json.loads(json.dumps(acn)))
a = A.BoundingBox(); c = C.BoundingBox()
print("3B ", [round(v,2) for v in (a.xmin,a.xmax,a.ymin,a.ymax,a.zmin,a.zmax)])
print("ACN", [round(v,2) for v in (c.xmin,c.xmax,c.ymin,c.ymax,c.zmin,c.zmax)])
print(acn["sabit_yuz"], acn["parca_sayisi"], len(acn["ic_konturlar"]), rap if isinstance(rap,(str,int)) else str(rap)[:300])
sys.stdout.flush(); os._exit(0)
