import sys,os,re,numpy as np
exec(open("g0.py").read())
sys.path.insert(0,S+r"\elk5"); sys.path.insert(0,S+r"\gece2\adim2\hava")
from ortam_sat import tri_kutu
from m8kit import Glb
import htas
g=Glb(sys.argv[1])
HORT=r"^(K_ELEKTRIK__hava|TOPPING_MODUL__hava_ana|HAVA_KOMPRESOR__hava_ana|ELK_ZINCIR__hava|HAVA_IC__kanal)$"
PP=[];AD=[]
for p in g.prims:
    if p.get("gizli") or re.match(HORT,p["name"]): continue
    P=p["X"][p["T"][g.gorunur(p)]]; PP.append(P); AD+=[p["name"]]*len(P)
PP=np.concatenate(PP);AD=np.array(AD);lo_=PP.min(1);hi_=PP.max(1)
for grp,ist,L in htas.GRUP:
    for e in (0.6,):
        top={}
        for ad,lo,hi in L:
            lo=np.array(lo)-e; hi=np.array(hi)+e
            m=np.all(hi_>lo,1)&np.all(lo_<hi,1); i=np.where(m)[0]; i=i[tri_kutu(PP[i],lo,hi)]
            for j in i: top[AD[j]]=top.get(AD[j],0)+1
        print(grp, "temas:", top if top else "YOK (HAVADA)")
