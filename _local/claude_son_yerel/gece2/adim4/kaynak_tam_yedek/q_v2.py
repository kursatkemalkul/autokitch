import json, sys
d=json.load(open(r"C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat2-v1/otonom/hat3d/v2/parca_kutulari.json",encoding="utf-8"))
P=d["parca"]
X0,X1,Y0,Y1=map(float,sys.argv[1:5])
for b,l in P.items():
    for p in l:
        n,_,x0,x1,y0,y1,z0,z1=p[:8]
        if x1>X0 and x0<X1 and y0<Y1 and y1>Y0 and b.startswith("TOPPING"):
            print(b,n[:55],round(x0),round(x1),round(y0),round(y1),round(z0),round(z1))
