import json,numpy as np,sys,collections
sys.path.insert(0,r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\elk5")
from ortam_sat import tri_kutu
PJ=json.load(open("c1/m8_parca.json",encoding="utf-8")); MEK=[m["kod"] for m in PJ["MEK"]]
Z=np.load("c1/m8_onbellek.npz"); T=np.stack([Z["A"],Z["B"],Z["C"]],1); Pp=Z["P"]; mk=Z["mek"]
lo_=T.min(1);hi_=T.max(1)
def bak(ad,lo,hi,haric=()):
    lo=np.array(lo,float);hi=np.array(hi,float)
    m=np.all(hi_>lo,1)&np.all(lo_<hi,1); i=np.where(m)[0]; i=i[tri_kutu(T[i],lo,hi)]
    c=collections.Counter(PJ["parca"][Pp[j]]["ad"] for j in i if not any(MEK[mk[j]].startswith(h) for h in haric))
    print("%-48s %s"%(ad, dict(c) if c else "TEMIZ"))
# tezgah acilma yollari (on +x; kapak yuzu x 3867)
bak("tezgah evye kapagi supurme (r 353)",(3893.5,104,1047),(4220,866,1400),("Tezgâh","Çevre/Zemin"))
bak("tezgah cekmece 500",(3893.5,720,1403),(4367,866,1873),("Tezgâh","Çevre/Zemin"))
bak("tezgah bulasik kapagi (r 454)",(3893.5,0.5,1408),(4321,700,1868),("Tezgâh","Çevre/Zemin"))
bak("tezgah onunde calisma alani 600",(3893.5,0.5,1044),(4360,1800,1874),("Tezgâh","Çevre/Zemin"))
# QR musteri kapilari (menteseli dis kenar, r 376, +z)
bak("QR musteri kapilari supurme",(4402,452,1190.5),(5188,1638,1566),("QR","Çevre/Zemin"))
# QR robot tarafi kapak/servis + koridor
bak("koridor QR arkasi (B depo / E cop cekmece yolu)",(4370,0.5,79.5),(5230,2050,669.5),("Çevre",))
