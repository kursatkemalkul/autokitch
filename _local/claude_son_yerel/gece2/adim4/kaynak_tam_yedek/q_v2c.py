import json, sys
d=json.load(open(r"C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat2-v1/otonom/hat3d/v2/parca_kutulari.json",encoding="utf-8"))
X0,X1,Y0,Y1,Z0,Z1=map(float,sys.argv[1:7]); pre=sys.argv[7] if len(sys.argv)>7 else ""
for b,l in d["parca"].items():
    if pre and not b.startswith(pre): continue
    for p in l:
        n,_,x0,x1,y0,y1,z0,z1=p[:8]
        if x1>X0 and x0<X1 and y0<Y1 and y1>Y0 and z0<Z1 and z1>Z0:
            print(b[:18].ljust(18), n[:44].ljust(44),round(x0),round(x1),"y",round(y0),round(y1),"z",round(z0),round(z1))
