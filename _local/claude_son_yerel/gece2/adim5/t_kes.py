import os, sys
B=os.path.dirname(os.path.abspath(__file__)); os.environ["ADIM5"]=B
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.abspath(os.path.join(B,"..","..","sac_standart"))
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import importlib; M = importlib.import_module(sys.argv[1])
g = M.kur(lambda *a: None)
P = {p["ad"]: (p["sh"] if p.get("sh") is not None else p["wp"].val()) for p in M.govde_parcalari(g, dunya=False)} if hasattr(M,"govde_parcalari") else None
for i in range(2, len(sys.argv), 2):
    a, b = sys.argv[i], sys.argv[i+1]
    r = P[a].intersect(P[b]); bb = r.BoundingBox()
    print(a, b, round(r.Volume(),3), [round(v,2) for v in (bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax)])
sys.stdout.flush(); os._exit(0)
