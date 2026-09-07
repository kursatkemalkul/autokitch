# -*- coding: utf-8 -*-
# DÜKKAN PLANI v5 (7 Eyl 2026) — Kemal: krokiyi 90° döndür, sokak cephesi AŞAĞI baksın, düzen aynı; TEK FİNAL RESİM (plan + sokak cephesi).
# Kroki (döndürülmüş): arka duvar boyunca HAT · önünde robot koridoru (sağ uçta öne kıvrılır, teslim dolabına) · ince duvar · ön zon: sol koridor + kapı, tezgah (sokağa bakar), SERVICE, sipariş ekranı, teslim dolabı sağ uçta.
import io, math, xml.dom.minidom
o=[]; W,H=1320,1060
def esc(t): return str(t).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'): o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,t,fs=8,anc='middle',fw='',col='#111',rot=0): o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif"%s>%s</text>'%(x,y,fs,anc,fw or 'normal',col,(' transform="rotate(%s %.1f %.1f)"'%(rot,x,y)) if rot else '',esc(t)))
def path(d_,sw=1,c='#111',f='none',d=None): o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(d_,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def dim(x1,y1,x2,y2,t,fs=6.5,col='#111'):
    ln(x1,y1,x2,y2,.7,col)
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-3,x,y+3,.7,col)
        else: ln(x-3,y,x+3,y,.7,col)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-3,t,fs,'middle','bold',col)
    else: tx(x1-5,(y1+y2)/2,t,fs,'middle','bold',col,-90)
def hatch(x,y,w,h,step=4,c='#999',f='#eee'):
    rc(x,y,w,h,.6,0,c,None,f); k=0
    while k<w+h: ln(x+max(0,k-h),y+min(k,h),x+min(k,w),y+max(0,k-w),.4,c); k+=step
def para(x,y,t,maxc,fs=6.4,col='#333',fw=''):
    lh=fs*1.55; cur=''; lines=[]
    for wd in t.split(' '):
        if cur and len(cur)+1+len(wd)>maxc: lines.append(cur); cur=wd
        else: cur=(cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y+=lh
    return y
def m2(v): return ('%.1f m²'%v).replace('.',',')
# ---------------- ölçüler (cm) — x soldan, y önden (0 = sokak) ----------------
SW,SD=420.0,320.0
WALL=6.0; COR=90.0; LINE_D=84.0; FZ=140.0
YW0,YW1=FZ,FZ+WALL; YC0,YC1=YW1,YW1+COR; YL0,YL1=YC1,SD            # ön zon 0–140 · ince duvar 140–146 · robot 146–236 · hat 236–320
M=[('1 STORE',140),('2 PRESS',70),('3 TOPPING',70),('4 OVEN',70),('5 PACK',70)]
RY=160.0; RX0,RX1=60.0,360.0; REACH=170.0                          # ray ekseni öne kaydırıldı (duvara 14) · H2017 menzil 170
DOOR=(0.0,75.0); TEZ=(80.0,220.0); SRV=(222.0,292.0); SRV_D=84.0; DOL=(296.0,420.0); DOL_D=52.0
EKR=(224.0,269.0); KOD=(272.0,292.0); WIN=(85.0,215.0); RDOOR=(100.0,170.0)
K=1.3; ox=70; oy=90+K*SD
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,32,'AUTOKITCH — DÜKKAN v5 · PLAN + SOKAK CEPHESİ · en küçük alan · iç %d × %d = %s · ölçüler cm'%(SW,SD,m2(SW*SD/1e4)),13,'start','bold')
tx(30,50,'tezgah + SERVICE + teslim dolabı ön duvarda tek sırada · sipariş ekranı ve kod ünitesi SERVICE'+"'"+'in sokak yüzünde · hat sağ duvara yaslı · sol koridor yok, duvar · ray 300 (x 60–360), eksen öne alındı · kol menzili 170 (H2017) ile dolap ve hat kontrol edildi',8.5,'start','','#444')
ln(30,60,W-30,60,.8,'#999')
tx(X(-30),Y(SD)-12,'PLAN (üstten)',9.5,'start','bold')
rc(X(-40),Y(0),K*(SW+80),K*60,0,0,'none',None,'#f0efe9'); tx(X(SW/2),Y(0)+72,'KALDIRIM / SOKAK — müşteri burada durur',7,'middle','bold','#888')
rc(X(0)-10,Y(SD)-10,K*SW+20,K*SD+20,0,0,'none',None,'#bfbfbf'); rc(X(0),Y(SD),K*SW,K*SD,1.6,0,'#111',None,'#fff')
# zonlar
rc(X(0),Y(YC1),K*SW,K*COR,.6,0,'#7fb3d5',None,'#eef6fb')                                    # robot koridoru
rc(X(DOL[0]),Y(YC0),K*(SW-DOL[0]),K*(YC0-DOL_D),.6,0,'#7fb3d5',None,'#eef6fb')               # dolap arkası açık robot alanı
rc(X(0),Y(YW0),K*SRV[0],K*FZ,.5,0,'#ccc',None,'#f4f4f4')                                     # ön zon (tezgah + eleman)
rc(X(SRV[0]),Y(YW0),K*(DOL[0]-SRV[0]),K*(FZ-SRV_D),.5,0,'#ccc',None,'#f4f4f4')               # SERVICE arkası eleman şeridi
rc(X(SRV[1]),Y(SRV_D),K*(DOL[0]-SRV[1]),K*SRV_D,.5,0,'#999',None,'#ddd')                     # SERVICE–dolap arası dolu 4
# hat (sağa yaslı)
xx=0.0
for nm,w in M:
    rc(X(xx),Y(YL1),K*w,K*LINE_D,1.2,2,'#111',None,'#e4e6ea'); tx(X(xx+w/2),Y((YL0+YL1)/2)+3,nm,7,'middle','bold'); xx+=w
# ray + robot
ln(X(RX0),Y(RY-4),X(RX1),Y(RY-4),1.6,'#333'); ln(X(RX0),Y(RY+4),X(RX1),Y(RY+4),1.6,'#333')
for xr in range(int(RX0),int(RX1)+1,50): ln(X(xr),Y(RY-4),X(xr),Y(RY+4),.6,'#333')
rc(X(210-20),Y(RY+20),K*40,K*40,1.2,3,'#111',None,'#fff'); ci(X(210),Y(RY),K*13,1.4,'#111',None,'#fff'); tx(X(210),Y(RY)+3,'ROBOT',5.6,'middle','bold')
for cx_ in (RX0,RX1): ci(X(cx_),Y(RY),K*REACH,.7,'#1a49b8','4,3','none'); ci(X(cx_),Y(RY),K*5,1,'#1a49b8','3,2','#eef6fb')
tx(X(210),Y(YC1-8)+3,'ROBOT KORİDORU 90 · RAY %d (x %d–%d) · eksen y %d (ince duvara 14, hat önüne 76)'%(RX1-RX0,RX0,RX1,RY),6,'middle','bold','#1a49b8')
# erişim kontrol noktaları
import math as _m
def rchk(px_,py_,lab,anc='start'):
    dx=max(RX0-px_,0.0,px_-RX1); dd=_m.hypot(dx,py_-RY); ok=dd<=REACH          # robot ray boyunca gider: en yakın ray noktasından
    c=('#1d7a4f' if ok else '#c0392b'); ci(X(px_),Y(py_),3,1,c,None,c); tx(X(px_)+(5 if anc=='start' else -5),Y(py_)+3,'%s %d %s'%(lab,dd,'✓' if ok else '✗'),4.6,anc,'bold',c)
rchk(DOL[0]+2,16,'dolap sol dip'); rchk(SW-2,16,'dolap sağ dip','end'); rchk(2,YL0+50,'STORE sol çekmece'); rchk(SW-2,YL0+50,'PACK sağ (kutu)','end'); rchk(210,YL0+68,'TOPPING kap dibi (çatal 50 + 18)')
# ince duvar (x 0–296) + robot kapısı
hatch(X(RDOOR[1]),Y(YW1),K*(DOL[0]-RDOOR[1]),K*WALL,3,'#b08968','#efe4d4'); hatch(X(0),Y(YW1),K*RDOOR[0],K*WALL,3,'#b08968','#efe4d4')
ln(X(RDOOR[0]),Y(YW0),X(RDOOR[0]),Y(YW0-70),1.1); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(RDOOR[0]),Y(YW0-70),K*70,K*70,X(RDOOR[1]),Y(YW0)),.8,'#333','none','3,3')
tx(X(135),Y(YW0-80)+3,'ROBOT KAPISI 70 (kilitli, açılınca robot durur)',4.8,'middle','','#c0392b')
tx(X(230),Y(YW0+3)+2,'İNCE DUVAR 6 · x 0–296',5.2,'middle','bold','#7a5c2e')
# SERVICE (sırtı sokağa, kapısı arkaya)
rc(X(SRV[0]),Y(SRV_D),K*(SRV[1]-SRV[0]),K*SRV_D,1.2,2,'#111',None,'#e4e6ea'); tx(X(257),Y(50)+3,'7 SERVICE',6.2,'middle','bold'); tx(X(257),Y(38)+3,'70 × 84 · sırtı sokağa',5,'middle','','#555')
ln(X(SRV[0]+10),Y(SRV_D),X(SRV[0]+60),Y(SRV_D),1.2); tx(X(257),Y(SRV_D+8)+3,'kapı (eleman tarafı)',4.6,'middle','','#555')
# tezgah + eleman
rc(X(TEZ[0]),Y(40),K*(TEZ[1]-TEZ[0]),K*40,1.2,2,'#111',None,'#f3e6d3'); tx(X(150),Y(20)+3,'TEZGAH 140 × 40 — sokağa bakar',6,'middle','bold')
ci(X(150),Y(80),K*18,1.2,'#111',None,'#fff'); tx(X(150),Y(80)+3,'eleman',5.4,'middle','')
# teslim dolabı
rc(X(DOL[0]),Y(DOL_D),K*(DOL[1]-DOL[0]),K*DOL_D,1.4,1,'#111',None,'#dfe1e4'); tx(X(358),Y(30)+3,'TESLİM DOLABI 124 × 52',6.2,'middle','bold'); tx(X(358),Y(16)+3,'12 dolap · ön duvar içinde',5,'middle','','#555')
ln(X(DOL[0]),Y(DOL_D),X(DOL[1]),Y(DOL_D),1.6,'#1d7a4f'); tx(X(358),Y(DOL_D)-4,'robot klapeleri (arka yüz)',5,'middle','','#1d7a4f')
# ön duvar açıklıkları
FW=Y(0)
rc(X(DOOR[0]),FW-2,K*(DOOR[1]-DOOR[0]),5,0,0,'none',None,'#fff'); ln(X(DOOR[1]),FW,X(DOOR[1]),FW-K*75,1.2); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(DOOR[1]),FW-K*75,K*75,K*75,X(DOOR[0]),FW),.8,'#333','none','3,3')
tx(X(37),FW+14,'KAPI 75',5.6,'middle','bold','#333'); tx(X(37),FW+22,'eleman · kurye · ikmal',4.4,'middle','','#555')
rc(X(WIN[0]),FW-3,K*(WIN[1]-WIN[0]),6,1,0,'#1a49b8',None,'#dbeeff'); tx(X(150),FW+14,'TEZGAH PENCERESİ 130',5.6,'middle','bold','#1a49b8'); tx(X(150),FW+22,'sürme cam',4.4,'middle','','#1a49b8')
rc(X(EKR[0]),FW,K*(EKR[1]-EKR[0]),K*14,1,0,'#111',None,'#2b2e33'); tx(X(246),FW+22,'EKRAN 45',5.2,'middle','bold'); tx(X(246),FW+30,'SERVICE sırtında',4.4,'middle','','#555')
rc(X(KOD[0]),FW,K*(KOD[1]-KOD[0]),K*8,1,0,'#111',None,'#b8bec5'); tx(X(282),FW+14,'KOD',5.2,'middle','bold')
for (xx_,lab,c) in ((150,'tezgah','#333'),(246,'sipariş','#1a49b8'),(358,'teslim','#1d7a4f')): ci(X(xx_),FW+K*40,K*11,1,c,'3,2','none'); tx(X(xx_),FW+K*40+3,lab,4.4,'middle','',c)
# ölçü zincirleri
yb=FW+86
for (a,b,t) in ((DOOR[0],DOOR[1],'75'),(WIN[0],WIN[1],'130'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(X(a),FW+50,X(b),FW+50,t,5.4,'#666')
dim(X(0),yb,X(TEZ[1]+2),yb,'tezgah zonu 222'); dim(X(TEZ[1]+2),yb,X(SRV[1]),yb,'SERVICE 70'); dim(X(SRV[1]),yb,X(SW),yb,'dolap 128'); dim(X(0),yb+18,X(SW),yb+18,'%d = HAT 420'%SW,7)
xr=X(SW)+30
dim(xr,Y(SD),xr,Y(YL0),'hat 84'); dim(xr,Y(YL0),xr,Y(YC0),'robot 90'); dim(xr,Y(YC0),xr,Y(DOL_D),'robot alanı 94'); dim(xr,Y(DOL_D),xr,Y(0),'dolap 52'); dim(X(SW)+52,Y(SD),X(SW)+52,Y(0),'%d'%SD,7)
xl=X(0)-30
dim(xl,Y(SD),xl,Y(YC0),'174'); dim(xl,Y(YC0),xl,Y(YW0),'6'); dim(xl,Y(YW0),xl,Y(SRV_D),'56'); dim(xl,Y(SRV_D),xl,Y(0),'SERVICE 84')
tx(X(SW/2),Y(SD)-12,'ARKA DUVAR',7,'middle','bold','#888'); tx(X(0)-8,Y(60)+3,'SOL DUVAR (kapalı)',6,'middle','bold','#888',-90)
# ================= SOKAK CEPHESİ =================
FY=Y(0)+130+K*300; KF=K
FX=lambda x: ox+KF*x; FZ_=lambda z: FY-KF*z
tx(X(-30),FZ_(300)-12,'SOKAK CEPHESİ (önden) · duvar boyu 300',9.5,'start','bold')
rc(FX(0),FZ_(300),KF*SW,KF*300,1.6,0,'#111',None,'#dcdcd8'); ln(FX(-40),FZ_(0),FX(SW+40),FZ_(0),2)
rc(FX(DOOR[0]),FZ_(210),KF*75,KF*210,1.2,1,'#111',None,'#eceef1'); tx(FX(37),FZ_(105)+3,'KAPI 75×210',6,'middle','bold'); rc(FX(66),FZ_(105),3,14,0,1,'none',None,'#444')
rc(FX(WIN[0]),FZ_(200),KF*130,KF*100,1.2,1,'#1a49b8',None,'#dbeeff'); tx(FX(150),FZ_(150)+3,'PENCERE 130×100',6,'middle','bold','#1a49b8'); tx(FX(150),FZ_(136)+3,'sürme cam · eşik z 100',4.8,'middle','','#1a49b8'); ln(FX(150),FZ_(200),FX(150),FZ_(100),.8,'#1a49b8')
rc(FX(SRV[0]),FZ_(197),KF*70,KF*197,.8,1,'#666','4,3','none'); tx(FX(257),FZ_(206)+3,'SERVICE sırtı (dolap 70×197 arkası)',4.6,'middle','','#666')
rc(FX(EKR[0]),FZ_(189),KF*45,KF*104,1.2,1,'#111',None,'#2b2e33'); rc(FX(226.5),FZ_(186),KF*40,KF*71,.8,1,'#666',None,'#111'); tx(FX(246.5),FZ_(150)+3,'32"',6,'middle','bold','#fff'); tx(FX(246.5),FZ_(78)+3,'SİPARİŞ EKRANI',5,'middle','bold'); tx(FX(246.5),FZ_(70)+3,'z 85–189',4.6,'middle','','#555')
rc(FX(KOD[0]),FZ_(144),KF*20,KF*34,1.2,1,'#111',None,'#b8bec5'); tx(FX(282),FZ_(102)+3,'KOD',5.2,'middle','bold'); tx(FX(282),FZ_(94)+3,'z 110–144',4.4,'middle','','#555')
rc(FX(DOL[0]),FZ_(165),KF*124,KF*165,1.4,1,'#111',None,'#dfe1e4')
for r in range(6):
    for c in range(2):
        x0=DOL[0]+2+c*60; z0=40+r*20; rc(FX(x0),FZ_(z0+19),KF*58,KF*18,.7,1,'#666',None,'#eceef1'); rc(FX(x0+53),FZ_(z0+13),KF*2,KF*8,.6,1,'#444',None,'#444')
rc(FX(DOL[0]+2),FZ_(40),KF*120,KF*25,.7,0,'#666',None,'#e3f2fb'); tx(FX(358),FZ_(26)+3,'pano (servis kapağı)',5,'middle','','#1a49b8'); tx(FX(358),FZ_(178)+3,'TESLİM DOLABI 124×165',6,'middle','bold')
dim(FX(SW)+30,FZ_(0),FX(SW)+30,FZ_(300),'300')
for (a,b,t) in ((DOOR[0],DOOR[1],'75'),(WIN[0],WIN[1],'130'),(EKR[0],EKR[1],'45'),(KOD[0],KOD[1],'20'),(DOL[0],DOL[1],'124')): dim(FX(a),FZ_(0)+22,FX(b),FZ_(0)+22,t,5.4,'#666')
dim(FX(0),FZ_(0)+40,FX(SW),FZ_(0)+40,'%d'%SW,7)
# ================= alan tablosu + erişim =================
bx=X(SW)+85; by=Y(SD)
rc(bx,by,330,330,1.2,4,'#111',None,'#fff'); tx(bx+12,by+18,'ALANLAR · ERİŞİM',9.5,'start','bold')
rows=[('hat kabinleri',LINE_D*420/1e4),('robot koridoru + dolap arkası',(COR*SW+(SW-DOL[0])*(YC0-DOL_D))/1e4),('ince duvar',WALL*DOL[0]/1e4),('ön zon: tezgah + eleman',FZ*SRV[0]/1e4),('SERVICE + arkası',70*FZ/1e4),('teslim dolabı (ön duvar içi)',124*DOL_D/1e4)]
yy=by+40
for a_,v in rows: tx(bx+12,yy,a_,6.2,'start','','#333'); tx(bx+318,yy,m2(v),6.4,'end','bold'); yy+=13
ln(bx+12,yy-5,bx+318,yy-5,.6,'#999'); tx(bx+12,yy+7,'TOPLAM İÇ (en az)',6.8,'start','bold'); tx(bx+318,yy+7,m2(SW*SD/1e4),6.8,'end','bold')
yy=para(bx+12,yy+26,'ERİŞİM (noktalar, kol 170 = H2017; mesafe en yakın ray noktasından): dolap sol dip 144 ✓, sağ dip 155 ✓, TOPPING kap dibi (çatal 50) 144 ✓, STORE sol çekmece 139 ✓, PACK sağ 139 ✓. CRX-20iA/L (142) dolap dibine ve çatal dibine yetişmez ✗ → H2017 (170) ya da ray 40 uzatılır.',62,6,'#333')
yy=para(bx+12,yy+2,'Sol koridor kalktı, sol duvar kapalı; giriş ön duvarda solda (75). Robot koridoruna tek giriş: ince duvardaki kilitli kapı. Müşteri kaldırımda: pencere · ekran+kod (SERVICE sırtı) · dolap.',62,6,'#333')
para(bx+12,yy+2,'Daha küçük: ön zon 140 → 130 (SERVICE 84 + 46 geçiş) → 420 × 310 = 13,0 m². Dükkan dışı duvarlar hariç.',62,6,'#1d7a4f','bold')
tx(W-30,H-8,'AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v5 · 7 Eyl 2026',6.5,'end','','#666')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)+chr(10).join(o)+'</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v5.svg"; io.open(out,'w',encoding='utf-8').write(svg); print('ok')
