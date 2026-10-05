import os, sys
S_=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
os.environ["AUTOKITCH_SAC_STANDART"]=os.path.join(S_,"sac_standart")
sys.path.insert(0, r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3")
import h3_sac_v1 as S
s=S.Sac("yan","dis"); g=s.R+s.t; print("t R K", s.t, s.R, s.K, "g", g)
P=s.taban([(892,-828.5+g),(2198.5,-828.5+g),(2198.5,39),(892,39)],O=(1436,0,0),ex=(0,1,0),ey=(0,0,1))
F=P.flans(0,20.0,yon=+1)
b=s.kati().BoundingBox(); print("yan",b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)
s2=S.Sac("r3","braket",t=3.0); print("t3 R",s2.R, s2.K)
s3=S.Sac("i","ic",t=1.0); print("t1 R",s3.R)
print(S.pem_somun("SP","M8",(0,0,0),(1,0,0),1.5)[1:])
print(S.pem_somun("SP","M5",(0,0,0),(1,0,0),1.5)[1:])
print(S.pem_somun("SP","M6",(0,0,0),(0,-1,0),4.0)[1:])
d=s.dfm(); print([ (m['kural'],m['durum']) for m in d if m['durum']!='GEÇTİ'][:10])
r=s.dogrula(); print(r.get('acinim_gecti'), r['kalinlik']['gecti'], r.get('kesit_gecti'))
