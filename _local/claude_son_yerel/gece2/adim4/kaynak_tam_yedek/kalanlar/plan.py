import numpy as np, json
from seviye import coz, G
R={"bina":9.95,"QR_guc":6.25,"QR_veri":4.35,"modem":4.35,"DOLAP_veri":4.35,"DOLAP_guc":6.25,"F_guc":3.8,"F_veri":4.35}
AD=list(R)
GV={"bina":(2462.4,-715.9),"QR_guc":(2458.8,-746.6),"QR_veri":(2456.8,-758.2),"modem":(2468.4,-777.6),"DOLAP_veri":(2458.9,-787.4),
    "DOLAP_guc":(2458.8,-799.0),"F_guc":(2456.3,-810.0),"F_veri":(2456.8,-819.2)}
xA0,xB0=2429.6,2441.0
RU={"bina":(2456.0,-643.0),"QR_guc":(xA0,-657.95),"DOLAP_guc":(xA0,-671.05),"F_guc":(xA0,-681.7),
    "QR_veri":(xB0,-653.25),"modem":(xB0,-662.55),"DOLAP_veri":(xB0,-671.85),"F_veri":(xB0,-681.15)}
xA,xB=2429.6,2441.0
RL={"QR_guc":(xA,-670.15),"DOLAP_guc":(xA,-683.15),"F_guc":(xA,-693.7),
    "QR_veri":(xB,-665.55),"modem":(xB,-674.75),"DOLAP_veri":(xB,-683.95),"F_veri":(xB,-693.15),"bina":(2436.0,-591.5)}
def kutu_alan(x0,x1,z0,z1):
    def f(Y,r):
        for a,b in Y:
            for c in (a,b):
                if c[0]-r<x0+0.5-1e-6 or c[0]+r>x1-0.5+1e-6 or c[1]-r<z0+0.5-1e-6 or c[1]+r>z1-0.5+1e-6: return False
        return True
    return f
# yerlesim kontrolu (ayni kesitte cakisma)
for nm,L in (("GV",GV),("RU",RU),("RL",RL)):
    for a in AD:
        for b in AD:
            if a<b:
                d=np.hypot(L[a][0]-L[b][0],L[a][1]-L[b][1])
                if d<R[a]+R[b]+0.5: print("YERLESIM",nm,a,b,round(d,2),R[a]+R[b])
if __name__=="__main__":
    fb=coz(AD,GV,RU,R,1255.0,1320.0,alan=kutu_alan(2422.5,2478.0,-826.5,-632.5),deneme=30000,tohum=3)
    print("FB",fb)
    bx=coz(AD,RU,RL,R,1000.0,1104.0,alan=kutu_alan(2422.5,2466.5,-698.0,-560.0),deneme=30000,tohum=5)
    print("KUTU",bx)
    json.dump(dict(fb=fb,bx=bx),open("plan.json","w"),default=lambda o: o.tolist() if hasattr(o,"tolist") else str(o))
