# python kq.py glb x0 x1 y0 y1 z0 z1 [ad_re] [icinde 0/1]  -> kutuyla kesisen bilesenler
from _env import *
import m8kit, re, pickle, os
gl=sys.argv[1]; q=[float(v) for v in sys.argv[2:8]]; lo=np.array(q[0::2]); hi=np.array(q[1::2])
pat=re.compile(sys.argv[8]) if len(sys.argv)>8 and sys.argv[8]!="-" else None
ic=len(sys.argv)>9 and sys.argv[9]=="1"
G=m8kit.Glb(gl)
MEK=[m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]; KAT=[k["kod"] for k in G.J["scenes"][0]["extras"]["kategoriler"]]
for p in G.prims:
    if p.get("gizli") or (pat and not pat.search(p["name"])): continue
    vis=G.gorunur(p)
    P=p["X"][p["T"]]; a=P.min(1); b=P.max(1)
    m=vis&np.all(b>=lo,1)&np.all(a<=hi,1)
    if not m.any(): continue
    tl,kut=G.komp(p); kp=G.kpk_maske(p)
    for i in np.unique(tl[m]):
        A,B,n=kut[int(i)]
        if ic and not (np.all(A>=lo-0.05) and np.all(B<=hi+0.05)): continue
        t0=int(np.where((tl==i)&vis)[0][0]); k,mk,_=G._etiketler(p,t0)
        print("%-34s c%-5d n%5d lo %7.1f %7.1f %7.1f hi %7.1f %7.1f %7.1f kpk%-4d %s %s"%(p["name"],i,n,*A,*B,int(kp[(tl==i)&vis].sum()),MEK[mk] if mk is not None else "-",KAT[k] if k is not None else "-"))
