# -*- coding: utf-8 -*-
"""v8zl -> v8zm: ana panodaki eski raya takılı ana şalter (iSW 4P 40A) kalkar; bina kablosu pano içinde kapıdaki yeni şalterin altına bağlanır."""
import sys, numpy as np
S=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\menu7\z53A"
for d in (r"\gece",r"",r"\elk4",r"\elk2"): sys.path.insert(0,S+d)
import m8kit, ek
from m8kit import tup, delik_ucgenler
G=m8kit.Glb(S+r"\hat3_v8zl.glb")
# 1 · eski şalter: cihaz bileşenleri x 3577–3647.8 (iID 3648.8'den başlar)
n=0; k=0
for p in G.prims:
    if p.get("gizli") or p["name"]!="ELK_ANA_PANO_UF__cihaz": continue
    for tri,a,b in ek.komps(G,p):
        if a[0]>=3576.9 and b[0]<=3647.9 and a[1]>=2060 and b[1]<=2155 and a[2]>=-279 and b[2]<=-203:
            m=np.zeros(len(p["T"]),bool); m[tri]=True; n+=G.sil(p,m); k+=1
print("eski şalter sil: bileşen",k,"üçgen",n)
# 2 · montaj plakasında kablo geçiş deliği (x 3599–3625 · y 2133–2159)
for p in G.prims:
    if p.get("gizli") or p["name"]!="ELK_ANA_PANO_UF__din": continue
    for tri,a,b in ek.komps(G,p):
        if abs(a[2]+282.5)<0.01 and abs(b[2]+280.5)<0.01 and b[0]-a[0]>400:
            et=G._etiketler(p,int(tri[0])); P=p["X"][p["T"][tri]]
            Q=delik_ucgenler(P,2,[-282.5,-280.5],3599,3625,2133,2159)
            m=np.zeros(len(p["T"]),bool); m[tri]=True; G.sil(p,m); G._ekle_dunya(p,Q,*et)
            print("plaka deliği: eski",len(tri),"yeni",len(Q),"etiket",et)
# 3 · bina kablosu pano içi ucu
p=[q for q in G.prims if q["name"]=="ELK_ZINCIR__kablo_guc" and not q.get("gizli")]
hedef=None
for q in p:
    for tri,a,b in ek.komps(G,q):
        if abs(a[0]-3930)<0.5 and abs(a[1]-2136)<0.5 and abs(b[2]+344)<0.5: hedef=(q,tri)
q,tri=hedef; et=G._etiketler(q,int(tri[0])); print("bina kablosu etiket",et)
Y=[(3940,2146,-318.5),(3940,2146,-300),(3612,2146,-300),(3612,2146,-150),(3612,2050,-150),(3745,2050,-150),(3745,2070,-150)]
g=tup(Y,10.0,16); print("kablo ucu üçgen",G._ekle_dunya(q,g,*et), "uzunluk", sum(np.linalg.norm(np.subtract(b,a)) for a,b in zip(Y[:-1],Y[1:])))
G.kaydet(S+r"\hat3_v8zm.glb"); print("yazildi")
