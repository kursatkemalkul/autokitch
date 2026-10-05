import json,numpy as np,sys,collections
sys.path.insert(0,r"@@KOK_W@@\elk5")
from ortam_sat import tri_kutu
PJ=json.load(open("c0/m8_parca.json",encoding="utf-8")); MEK=[m["kod"] for m in PJ["MEK"]]
Z=np.load("c0/m8_onbellek.npz"); T=np.stack([Z["A"],Z["B"],Z["C"]],1); Pp=Z["P"]
L=[(np.array(p["lo"]),np.array(p["hi"])) for p in PJ["parca"] if p["ad"]=="ELK_IC__kanal" and MEK[p["mek"]]=="B/Elektrik" and p["n"]>20]
yan=[b for b in L if b[1][2]-b[0][2]>600 and b[1][0]-b[0][0]<12]
arka=[b for b in L if b[1][0]-b[0][0]>100 and abs(b[0][2]+790)<0.5 and abs(b[1][2]+760)<0.5]
K=[]
for ylo,yhi in yan:
    c=[a for a in arka if 0<a[0][0]-yhi[0]<80 and a[0][1]<yhi[1] and a[1][1]>ylo[1]-15]
    if not c: print("eslesmedi",ylo,yhi); continue
    a=min(c,key=lambda a:abs(a[0][1]-ylo[1]))
    K.append((ylo,yhi,a[0],a[1]))
print(len(yan),len(arka),len(K))
tlo=T.min(1); thi=T.max(1)
for ylo,yhi,alo,ahi in K:
    blo=np.array([ylo[0],min(ylo[1],alo[1]),-788.0]); bhi=np.array([alo[0],max(yhi[1],ahi[1]),-758.0])
    m=np.all(thi>blo+0.05,1)&np.all(tlo<bhi-0.05,1); idx=np.where(m)[0]
    h=tri_kutu(T[idx],blo+0.05,bhi-0.05); idx=idx[h]
    c=collections.Counter(PJ["parca"][Pp[i]]["ad"] for i in idx if not PJ["parca"][Pp[i]]["ad"].startswith("ELK_DOLAP__kablo"))
    print(np.round(blo,1).tolist(),np.round(bhi,1).tolist(),"gap x %.1f"%(alo[0]-ylo[0]),dict(c))
