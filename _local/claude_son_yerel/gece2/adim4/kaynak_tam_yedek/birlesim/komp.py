from _env import *
import m8kit, re
G=m8kit.Glb(sys.argv[1]); pat=re.compile(sys.argv[2])
for p in G.prims:
    if not pat.search(p["name"]) or p.get("gizli"): continue
    tl,kut=G.komp(p); kp=G.kpk_maske(p)
    print("==",p["name"],p["pi"],len(kut))
    for i,(a,b,n) in sorted(kut.items(),key=lambda t:(t[1][0][2],t[1][0][1],t[1][0][0])):
        m=(tl==i)&G.gorunur(p)
        t0=int(np.where(m)[0][0]); k,mk,_=G._etiketler(p,t0)
        print("  %5d n%5d lo %8.1f %7.1f %7.1f  hi %8.1f %7.1f %7.1f  d %6.1f %6.1f %6.1f kpk%d mek%s kat%s"%(i,n,*a,*b,*(b-a),int(kp[m].sum()),mk,k))
