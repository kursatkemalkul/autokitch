from _env import *
import m8kit, re, json
G=m8kit.Glb(sys.argv[1]); pat=re.compile(sys.argv[2])
J=G.J; MEK=J["scenes"][0]["extras"]["mekanizmalar"]; KAT=[k["kod"] for k in J["scenes"][0]["extras"]["kategoriler"]]
def lab(p,key):
    L=p["pr"].get("extras",{}).get(key) or []; n=len(p["T"]); a=np.full(n,-1)
    for k in range(0,len(L)-2,3): a[L[k+1]//3:(L[k+1]+L[k+2])//3]=L[k]
    return a
for p in G.prims:
    if not pat.search(p["name"]) or p.get("gizli"): continue
    vis=G.gorunur(p)
    if not vis.any(): continue
    Q=p["X"][np.unique(p["T"][vis])]
    mk=lab(p,"mek")[vis]; kt=lab(p,"kat")[vis]; kp=G.kpk_maske(p)[vis]
    um=sorted(set(mk.tolist())); uk=sorted(set(kt.tolist()))
    def nm(i,arr): 
        if i<0: return "-"
        x=arr[i]; return x if isinstance(x,str) else (x.get("ad") or x.get("kod") or str(x))
    print("%-38s pi%d n%6d lo %s hi %s kpk%5d mek %s kat %s %s"%(p["name"],p["pi"],vis.sum(),Q.min(0).round(0),Q.max(0).round(0),kp.sum(),[nm(i,MEK) for i in um],[nm(i,KAT) for i in uk],"D" if p.get("donuk") else ""))
