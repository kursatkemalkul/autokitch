from _env import *
import m8kit
G=m8kit.Glb(sys.argv[1]); hedef=set(int(v) for v in sys.argv[2].split(","))
MEK=[m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]
for p in G.prims:
    L=p["pr"].get("extras",{}).get("mek") or []
    vis=G.gorunur(p); a=np.full(len(p["T"]),-1)
    for k in range(0,len(L)-2,3): a[L[k+1]//3:(L[k+1]+L[k+2])//3]=L[k]
    for h in hedef:
        m=(a==h)&vis
        if m.any():
            Q=p["X"][p["T"][m]].reshape(-1,3)
            print("%-36s pi%d %-14s n%6d/%6d lo %s hi %s gizli%s kat%s"%(p["name"],p["pi"],MEK[h],m.sum(),vis.sum(),Q.min(0).round(0),Q.max(0).round(0),bool(p.get("gizli")),sorted(set(G.etiket_of(p,int(t),"kat") for t in np.where(m)[0][:50]))))
