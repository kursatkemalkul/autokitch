# -*- coding: utf-8 -*-
# DÜKKAN PLANI v2 (7 Eyl 2026) — Kemal: aynalı (hat sağda, kapı solda), tezgah öne (sokağa) bakar, müşteri salonu YOK (al-git): müşteri cephesi = ön duvar, kaldırım.
import io, math, xml.dom.minidom
o=[]; W,H=1240,900
def esc(t): return str(t).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'): o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,t,fs=8,anc='middle',fw='',col='#111',rot=0): o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif"%s>%s</text>'%(x,y,fs,anc,fw or 'normal',col,(' transform="rotate(%s %.1f %.1f)"'%(rot,x,y)) if rot else '',esc(t)))
def path(d_,sw=1,c='#111',f='none',d=None): o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(d_,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
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
# ---------------- ölçüler (cm) — x soldan, y önden (0 = kaldırım) ----------------
SW,SD=400.0,560.0
STF=220.0; WALL=6.0; COR=90.0; LINE_D=84.0
XW0,XW1=STF,STF+WALL; XC0,XC1=XW1,XW1+COR; XL0,XL1=XC1,SW          # 220–226 duvar · 226–316 robot · 316–400 hat
LY0=100.0; RAIL=(90.0,520.0); RX=(XC0+XC1)/2
DOOR=(5.0,95.0); WIN=(100.0,180.0); EKR=(190.0,235.0); DOL=(240.0,364.0); KOD=(370.0,390.0)
DOL_D=52.0; VOID_Y=100.0
SRV=(136.0,220.0,200.0,270.0); WDOOR=(470.0,550.0)
K=1.0; ox=70; oy=95+K*SD
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,32,'AUTOKITCH — DÜKKAN PLANI v2 · üstten · al-git, müşteri salonu yok · iç ölçü %d × %d = %s · ölçüler cm'%(SW,SD,m2(SW*SD/1e4)),13,'start','bold')
tx(30,50,'aynalı: hat sağ duvarda, kapı solda · tezgah sokağa bakar · müşteri cephesi = ön duvar (kaldırım): kapı · tezgah penceresi · sipariş ekranı · teslim dolabı · kod ünitesi · robot koridoru 90 + ince duvar 6 · SERVICE + eleman koridoru + arka kapı',8.5,'start','','#444')
ln(30,60,W-30,60,.8,'#999')
# kaldırım + dış duvar
rc(X(-40),Y(0),K*(SW+80),K*92,0,0,'none',None,'#f0efe9'); tx(X(SW/2),Y(0)+86,'KALDIRIM / SOKAK — müşteri burada durur',7,'middle','bold','#888')
rc(X(0)-10,Y(SD)-10,K*SW+20,K*SD+20,0,0,'none',None,'#bfbfbf'); rc(X(0),Y(SD),K*SW,K*SD,1.6,0,'#111',None,'#fff')
# zonlar
rc(X(XC0),Y(SD),K*COR,K*(SD-DOL_D),.6,0,'#7fb3d5',None,'#eef6fb')                       # robot koridoru
rc(X(XL0),Y(VOID_Y),K*LINE_D,K*(VOID_Y-DOL_D),.6,0,'#7fb3d5',None,'#eef6fb')             # hat önü boşluk (robot alanı)
rc(X(0),Y(SD),K*STF,K*SD,.5,0,'#ccc',None,'#f4f4f4')                                     # personel zonu
# hat (sağ duvar)
yy=LY0
for nm,w in [('5 PACK',70),('4 OVEN',70),('3 TOPPING',70),('2 PRESS',70),('1 STORE',140)]:
    rc(X(XL0),Y(yy+w),K*LINE_D,K*w,1.2,2,'#111',None,'#e4e6ea'); tx(X(XL0+LINE_D/2),Y(yy+w/2)+3,nm,7,'middle','bold',rot=-90); yy+=w
tx(X(XL0+LINE_D/2),Y(SD-20)+3,'HAT 420 × 84',6,'middle','','#555')
# ray + robot
ln(X(RX-4),Y(RAIL[0]),X(RX-4),Y(RAIL[1]),1.6,'#333'); ln(X(RX+4),Y(RAIL[0]),X(RX+4),Y(RAIL[1]),1.6,'#333')
for yr in range(int(RAIL[0]),int(RAIL[1])+1,50): ln(X(RX-4),Y(yr),X(RX+4),Y(yr),.6,'#333')
rc(X(RX-20),Y(330),K*40,K*40,1.2,3,'#111',None,'#fff'); ci(X(RX),Y(310),K*13,1.4,'#111',None,'#fff'); tx(X(RX),Y(310)+3,'ROBOT',5.6,'middle','bold')
ci(X(RX),Y(120),K*130,.7,'#1a49b8','4,3','none')
tx(X(RX),Y(RAIL[1])+16,'RAY %d (y %d–%d)'%(RAIL[1]-RAIL[0],RAIL[0],RAIL[1]),6,'middle','bold','#1a49b8'); tx(X(RX),Y(SD-30)+3,'ROBOT KORİDORU 90',6.5,'middle','bold','#1a49b8',-90)
tx(X(RX+8),Y(120)-K*130-4,'kol menzili 130 (ray ucundan)',5.4,'middle','','#1a49b8')
# ince duvar + arka kapı
hatch(X(XW0),Y(SD),K*WALL,K*(SD-WDOOR[1]),3,'#b08968','#efe4d4'); hatch(X(XW0),Y(WDOOR[0]),K*WALL,K*WDOOR[0],3,'#b08968','#efe4d4')
ln(X(XW0),Y(WDOOR[0]),X(XW0)-K*80,Y(WDOOR[0]),1.2); path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(XW0)-K*80,Y(WDOOR[0]),K*80,K*80,X(XW0),Y(WDOOR[1])),.8,'#333','none','3,3')
tx(X(XW0)-K*45,Y(WDOOR[1])-3,'KAPI 80 (kilitli, açılınca robot durur)',5.4,'middle','','#c0392b')
tx(X(XW0+3),Y(330)+3,'İNCE DUVAR 6 (2 sac + yalıtım)',5.4,'middle','bold','#7a5c2e',-90)
# ön duvar açıklıkları
FW=Y(0)
rc(X(DOOR[0]),FW-2,K*(DOOR[1]-DOOR[0]),5,0,0,'none',None,'#fff'); ln(X(DOOR[0]),FW,X(DOOR[0]),FW-K*90,1.2); path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(DOOR[0]),FW-K*90,K*90,K*90,X(DOOR[1]),FW),.8,'#333','none','3,3')
tx(X(50),FW+14,'KAPI 90',5.6,'middle','bold','#333'); tx(X(50),FW+22,'eleman · kurye · ikmal',4.8,'middle','','#555')
rc(X(WIN[0]),FW-3,K*(WIN[1]-WIN[0]),6,1,0,'#1a49b8',None,'#dbeeff'); tx(X(140),FW+14,'PENCERE 80',5.6,'middle','bold','#1a49b8'); tx(X(140),FW+22,'sürme cam',4.8,'middle','','#1a49b8')
rc(X(WIN[0]),Y(40),K*(WIN[1]-WIN[0]),K*40,1.2,2,'#111',None,'#f3e6d3'); tx(X(140),Y(20)+3,'TEZGAH 80×40',6,'middle','bold')
ci(X(140),Y(72),K*18,1.2,'#111',None,'#fff'); tx(X(140),Y(72)+3,'eleman',5.4,'middle','')
rc(X(EKR[0]),FW,K*(EKR[1]-EKR[0]),K*14,1,0,'#111',None,'#2b2e33'); tx(X(212.5),FW+22,'SİPARİŞ EKRANI',5.4,'middle','bold'); tx(X(212.5),FW+30,'45×14 dışa asılı',4.8,'middle','','#555')
rc(X(DOL[0]),Y(DOL_D),K*(DOL[1]-DOL[0]),K*DOL_D,1.4,1,'#111',None,'#dfe1e4'); tx(X(302),Y(30)+3,'TESLİM DOLABI 124 × 52 (ön duvar içinde)',6.2,'middle','bold')
ln(X(DOL[0]),Y(DOL_D),X(DOL[1]),Y(DOL_D),1.6,'#1d7a4f'); tx(X(302),Y(DOL_D)-4,'robot klapeleri (arka yüz, koridora bakar)',5,'middle','','#1d7a4f')
rc(X(KOD[0]),FW,K*(KOD[1]-KOD[0]),K*8,1,0,'#111',None,'#b8bec5'); tx(X(380),FW+20,'KOD',5.6,'middle','bold'); tx(X(380),FW+28,'20×8',5,'middle','','#555')
for (xx,lab,c) in ((212,'sipariş','#1a49b8'),(302,'teslim','#1d7a4f'),(140,'tezgah','#333')): ci(X(xx),FW+K*64,K*14,1,c,'3,2','none'); tx(X(xx),FW+K*64+3,lab,4.6,'middle','',c)
# personel zonu: SERVICE, koridor, depo
rc(X(SRV[0]),Y(SRV[3]),K*(SRV[1]-SRV[0]),K*(SRV[3]-SRV[2]),1.2,2,'#111',None,'#e4e6ea'); tx(X((SRV[0]+SRV[1])/2),Y((SRV[2]+SRV[3])/2)+3,'7 SERVICE 84 × 70',6.2,'middle','bold')
ln(X(SRV[0]),Y(SRV[2]+10),X(SRV[0]),Y(SRV[2]+60),1.2); tx(X(SRV[0])-4,Y(SRV[2]+35)+3,'kapı',5,'end','','#555')
tx(X(110),Y(500)+3,'ELEMAN KORİDORU 100',5.8,'middle','bold','#555'); tx(X(110),Y(360)+3,'PERSONEL / DEPO ALANI %d × %d'%(STF,SD),6.5,'middle','bold','#888'); tx(X(110),Y(340)+3,m2(STF*SD/1e4),6.5,'middle','','#888')
tx(X(XL0+LINE_D/2),Y(76)+3,'boş 48 (robot alanı)',5.2,'middle','','#1a49b8')
# ölçü zincirleri
yb=Y(0)+108
dim(X(0),yb,X(STF),yb,'220'); dim(X(STF),yb,X(XW1),yb,'6'); dim(X(XW1),yb,X(XC1),yb,'90'); dim(X(XC1),yb,X(SW),yb,'84'); dim(X(0),yb+18,X(SW),yb+18,'%d'%SW,7)
yf=Y(0)+88
for (a,b,t) in ((DOOR[0],DOOR[1],'90'),(WIN[0],WIN[1],'80'),(EKR[0],EKR[1],'45'),(DOL[0],DOL[1],'124'),(KOD[0],KOD[1],'20')): dim(X(a),FW+44,X(b),FW+44,t,5.6,'#666')
xr=X(SW)+30
dim(xr,Y(SD),xr,Y(LY0+420),'40'); dim(xr,Y(LY0+420),xr,Y(LY0),'HAT 420'); dim(xr,Y(LY0),xr,Y(DOL_D),'48'); dim(xr,Y(DOL_D),xr,Y(0),'52')
dim(X(SW)+52,Y(SD),X(SW)+52,Y(0),'%d'%SD,7)
xl=X(0)-30
dim(xl,Y(SD),xl,Y(WDOOR[0]),'koridor 100'); dim(xl,Y(WDOOR[0]),xl,Y(SRV[3]),'depo 200'); dim(xl,Y(SRV[3]),xl,Y(SRV[2]),'SERVICE 70'); dim(xl,Y(SRV[2]),xl,Y(40),'eleman 160'); dim(xl,Y(40),xl,Y(0),'tezgah 40')
tx(X(SW/2),Y(SD)-14,'ARKA DUVAR',7,'middle','bold','#888')
# alan tablosu
bx=X(SW)+90; by=Y(SD)
rc(bx,by,300,300,1.2,4,'#111',None,'#fff'); tx(bx+12,by+18,'ALANLAR',9.5,'start','bold')
rows=[('hat kabinleri',LINE_D*420/1e4),('robot koridoru + hat önü',(COR*(SD-DOL_D)+LINE_D*(VOID_Y-DOL_D))/1e4),('ince duvar',WALL*SD/1e4),('teslim dolabı (ön duvar içi)',(DOL[1]-DOL[0])*DOL_D/1e4),('personel zonu (tezgah, SERVICE, depo, koridor)',STF*SD/1e4)]
yy=by+40
for a_,v in rows: tx(bx+12,yy,a_,6.2,'start','','#333'); tx(bx+288,yy,m2(v),6.4,'end','bold'); yy+=14
ln(bx+12,yy-6,bx+288,yy-6,.6,'#999'); tx(bx+12,yy+6,'TOPLAM İÇ',6.8,'start','bold'); tx(bx+288,yy+6,m2(SW*SD/1e4),6.8,'end','bold')
yy=para(bx+12,yy+26,'Müşteri içeri girmez: kaldırımdan sipariş ekranı, teslim dolabı, kod ünitesi ve tezgah penceresi. Dolap ön duvarın içinde, arkası robot koridoruna bakar; ray ucu y 90, dolap arkası y 52 → kol 130 ile 12 dolabın hepsine ulaşır.',56,6,'#333')
yy=para(bx+12,yy+2,'Kapı 90 solda: eleman, kurye (büyük sipariş / iade), ikmal (kap, kutu demeti, yağ). Robot koridoruna tek giriş arkadaki kilitli kapı.',56,6,'#333')
para(bx+12,yy+2,'Personel zonu 220 geniş: tezgah + eleman 160 derinlik, SERVICE, 200 depo, 100 koridor. Daraltılabilir (180) → dükkan 360 × 560 = 20,2 m².',56,6,'#1d7a4f','bold')
tx(W-30,H-8,'AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v2 · 7 Eyl 2026',6.5,'end','','#666')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)+chr(10).join(o)+'</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v2.svg"; io.open(out,'w',encoding='utf-8').write(svg); print('ok')
