# -*- coding: utf-8 -*-
# DÜKKAN PLANI v1 (7 Eyl 2026) — Kemal'in krokisinden: hat sol duvarda, önünde robot koridoru, ince duvar; müşteri yüzünde sipariş ekranı + teslim dolabı + kod ünitesi;
# SERVICE odası + tezgah (eleman) ince duvarın arkasında; arkada eleman koridoru + kapı; sağda müşteri salonu. ~31 m². Yalnız teknik plan.
import io, math, xml.dom.minidom
AP=chr(39); o=[]
W,H=1300,820
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
# ---------------- ölçüler (cm) ----------------
SW,SD=560.0,560.0           # dükkan iç: genişlik (x) × derinlik (y, 0 = sokak/ön)
LINE_D=84.0; COR=90.0; WALL=6.0
XL0,XL1=0,LINE_D; XC0,XC1=LINE_D,LINE_D+COR; XW0,XW1=XC1,XC1+WALL     # 0–84 hat · 84–174 robot · 174–180 ince duvar
STAFF_X1=280.0
M=[('1 STORE',140),('2 PRESS',70),('3 TOPPING',70),('4 OVEN',70),('5 PACK',70)]
LY0=100.0                                                       # hat ön ucu (PACK) y 100 → arka uç 520
RAIL=(30.0,500.0); RX=129.0
DOL=(20.0,144.0); KOD=(150.0,170.0); EKR=(180.0,225.0)          # ince duvar müşteri yüzü, y aralıkları
SRV=(232.0,316.0); TEZ=(320.0,450.0); KOR=(460.0,560.0); DOOR=(470.0,550.0)
ENT=(400.0,500.0)                                               # giriş kapısı ön duvarda x
K=1.06; ox=70; oy=60+K*SD
X=lambda x: ox+K*x; Y=lambda y: oy-K*y
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,32,'AUTOKITCH — DÜKKAN PLANI v1 · üstten · iç ölçü %d × %d = %s m² · ölçüler cm'%(SW,SD,('%.1f'%(SW*SD/1e4)).replace('.',',')),13,'start','bold')
tx(30,50,'hat sol duvarda (420) · robot koridoru 90 · ince duvar 6 · müşteri yüzünde: sipariş ekranı, teslim dolabı (duvardan geçer), kod ünitesi · SERVICE + tezgah elemanın · arkada eleman koridoru + kapı · sağda müşteri salonu',8.5,'start','','#444')
ln(30,60,W-30,60,.8,'#999')
# dış duvarlar
rc(X(0)-10,Y(SD)-10,K*SW+20,K*SD+20,0,0,'none',None,'#bfbfbf'); rc(X(0),Y(SD),K*SW,K*SD,1.6,0,'#111',None,'#fff')
# giriş kapısı (ön duvar)
rc(X(ENT[0]),Y(0)-2,K*(ENT[1]-ENT[0]),14,0,0,'none',None,'#fff'); ln(X(ENT[0]),Y(0),X(ENT[0]),Y(0)+K*100,1.2); path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(ENT[0]),Y(0)+K*100,K*100,K*100,X(ENT[1]),Y(0)),.8,'#333','none','3,3')
tx(X(450),Y(0)+22,'GİRİŞ 100',6.5,'middle','bold','#333')
# zonlar
rc(X(XC0),Y(SD),K*COR,K*SD,.6,0,'#7fb3d5',None,'#eef6fb')                                  # robot koridoru
rc(X(STAFF_X1),Y(SD),K*(SW-STAFF_X1),K*SD,.5,0,'#ccc',None,'#fbfaf6')                         # müşteri salonu
rc(X(XW1),Y(SD),K*(STAFF_X1-XW1),K*(SD-SRV[0]),.5,0,'#ccc',None,'#f4f4f4')                # personel zonu
rc(X(XW1),Y(SRV[0]),K*(STAFF_X1-XW1),K*(SRV[0]),.5,0,'#ccc',None,'#fbfaf6')                   # müşteri bekleme (dolap önü)
# hat kabinleri (sol duvar)
yy=LY0
for nm,w in reversed(M):
    pass
yy=LY0
for nm,w in [('5 PACK',70),('4 OVEN',70),('3 TOPPING',70),('2 PRESS',70),('1 STORE',140)]:
    rc(X(XL0),Y(yy+w),K*LINE_D,K*w,1.2,2,'#111',None,'#e4e6ea'); tx(X(XL0+LINE_D/2),Y(yy+w/2)+3,nm,7,'middle','bold',rot=-90); yy+=w
tx(X(XL0+LINE_D/2),Y(LY0)-8,'HAT 420 × 84',6,'middle','','#555'); tx(X(XL0+LINE_D/2),Y(50)+3,'boş 100',6,'middle','','#999')
# ray + robot
ln(X(RX-4),Y(RAIL[0]),X(RX-4),Y(RAIL[1]),1.6,'#333'); ln(X(RX+4),Y(RAIL[0]),X(RX+4),Y(RAIL[1]),1.6,'#333')
for yr in range(int(RAIL[0]),int(RAIL[1])+1,50): ln(X(RX-4),Y(yr),X(RX+4),Y(yr),.6,'#333')
rc(X(RX-20),Y(330),K*40,K*40,1.2,3,'#111',None,'#fff'); ci(X(RX),Y(310),K*13,1.4,'#111',None,'#fff'); tx(X(RX),Y(310)+3,'ROBOT',5.6,'middle','bold')
path('M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f'%(X(RX-130),Y(310),K*130,K*130,X(RX+130),Y(310)),.7,'#1a49b8','none','4,3')
tx(X(RX),Y(RAIL[1])+18,'RAY %d (y %d–%d)'%(RAIL[1]-RAIL[0],RAIL[0],RAIL[1]),6,'middle','bold','#1a49b8'); tx(X(RX-30),Y(SD-30)+3,'ROBOT KORİDORU 90',6.5,'middle','bold','#1a49b8',-90)
# ince duvar (hatch) + kapı
hatch(X(XW0),Y(SD),K*WALL,K*(SD-DOOR[1]),3,'#b08968','#efe4d4'); hatch(X(XW0),Y(DOOR[0]),K*WALL,K*DOOR[0],3,'#b08968','#efe4d4')
ln(X(XW1),Y(DOOR[0]),X(XW1)+K*80,Y(DOOR[0]),1.2); path('M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f'%(X(XW1)+K*80,Y(DOOR[0]),K*80,K*80,X(XW1),Y(DOOR[1])),.8,'#333','none','3,3')
tx(X(XW1)+K*50,Y(DOOR[1])-3,'KAPI 80 (kilitli, açılınca robot durur)',5.4,'middle','','#c0392b')
tx(X(XW0+3),Y(400)+3,'İNCE DUVAR 6 (2 sac + yalıtım)',5.4,'middle','bold','#7a5c2e',-90)
# teslim dolabı (duvardan geçer, müşteri tarafına 46 çıkar)
rc(X(XW0),Y(DOL[1]),K*52,K*(DOL[1]-DOL[0]),1.4,1,'#111',None,'#dfe1e4'); tx(X(XW0+26),Y((DOL[0]+DOL[1])/2)+3,'TESLİM DOLABI 124×52',6.2,'middle','bold',rot=-90)
ln(X(XW0),Y(DOL[0]),X(XW0),Y(DOL[1]),1.6,'#1d7a4f'); tx(X(XW0)-5,Y((DOL[0]+DOL[1])/2)+3,'robot klapeleri',5,'middle','','#1d7a4f',-90)
# kod ünitesi + sipariş ekranı (duvara asılı)
rc(X(XW1),Y(KOD[1]),K*8,K*(KOD[1]-KOD[0]),1,0,'#111',None,'#b8bec5'); tx(X(XW1)+K*14,Y((KOD[0]+KOD[1])/2)+3,'KOD ÜNİTESİ 20×8',5.6,'start','bold')
rc(X(XW1),Y(EKR[1]),K*14,K*(EKR[1]-EKR[0]),1,0,'#111',None,'#2b2e33'); tx(X(XW1)+K*20,Y((EKR[0]+EKR[1])/2)+3,'SİPARİŞ EKRANI 45×14',5.6,'start','bold')
# müşteri bekleme noktaları
for (xx,yy_,lab,c) in ((240,202,'sipariş',"#1a49b8"),(250,90,'teslim',"#1d7a4f")): ci(X(xx),Y(yy_),K*22,1,c,'3,2','none'); tx(X(xx),Y(yy_)+3,lab,5.4,'middle','',c)
# SERVICE
rc(X(XW1),Y(SRV[1]),K*84,K*(SRV[1]-SRV[0]),1.2,2,'#111',None,'#e4e6ea'); tx(X(XW1+42),Y((SRV[0]+SRV[1])/2)+3,'7 SERVICE 70×84',6.2,'middle','bold',rot=-90)
ln(X(XW1+84),Y(SRV[0]+10),X(XW1+84),Y(SRV[0]+60),1.2); tx(X(XW1+84)+4,Y(SRV[0]+35)+3,'kapı',5,'start','','#555')
# tezgah + eleman
rc(X(240),Y(TEZ[1]),K*40,K*(TEZ[1]-TEZ[0]),1.2,2,'#111',None,'#f3e6d3'); tx(X(260),Y((TEZ[0]+TEZ[1])/2)+3,'TEZGAH 130×40',6,'middle','bold',rot=-90)
ci(X(210),Y(385),K*18,1.2,'#111',None,'#fff'); tx(X(210),Y(385)+3,'eleman',5.4,'middle','')
tx(X(XW1+50),Y(KOR[0]+4)+3,'ELEMAN KORİDORU 100×100',5.8,'middle','bold','#555')
# müşteri salonu
tx(X(420),Y(300)+4,'MÜŞTERİ SALONU',9,'middle','bold','#888'); tx(X(420),Y(280)+4,'%d × %d = %s m²'%(SW-STAFF_X1,SD,('%.1f'%((SW-STAFF_X1)*SD/1e4)).replace('.',',')),7,'middle','','#888')
for (xx,yy_) in ((330,400),(360,120)): ci(X(xx),Y(yy_),K*18,.9,'#999','3,2','none')
# ---- ölçü zincirleri
yb=Y(0)+42
dim(X(0),yb,X(XL1),yb,'84'); dim(X(XL1),yb,X(XC1),yb,'90'); dim(X(XC1),yb,X(XW1),yb,'6'); dim(X(XW1),yb,X(STAFF_X1),yb,'100'); dim(X(STAFF_X1),yb,X(SW),yb,'280')
dim(X(0),yb+18,X(SW),yb+18,'%d'%SW,7)
xl=X(0)-30
dim(xl,Y(SD),xl,Y(LY0+420),'40'); dim(xl,Y(LY0+420),xl,Y(LY0),'HAT 420'); dim(xl,Y(LY0),xl,Y(0),'100')
dim(X(0)-52,Y(SD),X(0)-52,Y(0),'%d'%SD,7)
xr=X(SW)+30
dim(xr,Y(SD),xr,Y(KOR[0]),'koridor 100'); dim(xr,Y(KOR[0]),xr,Y(TEZ[0]),'tezgah 140'); dim(xr,Y(TEZ[0]),xr,Y(SRV[0]),'SERVICE 88'); dim(xr,Y(SRV[0]),xr,Y(EKR[0]),'ekran + pay 52'); dim(xr,Y(EKR[0]),xr,Y(DOL[1]),'36'); dim(xr,Y(DOL[1]),xr,Y(DOL[0]),'dolap 124'); dim(xr,Y(DOL[0]),xr,Y(0),'20')
tx(X(SW/2),Y(0)+80,'SOKAK / ÖN',7,'middle','bold','#888')
# ---- alan tablosu
bx=X(SW)+110; by=Y(SD)
rc(bx,by,300,330,1.2,4,'#111',None,'#fff'); tx(bx+12,by+18,'ALANLAR',9.5,'start','bold')
rows=[('hat kabinleri',LINE_D*420/1e4),('robot koridoru',COR*SD/1e4),('ince duvar',WALL*SD/1e4),('dolap + ekran önü (müşteri)',(STAFF_X1-XW1)*SRV[0]/1e4),('SERVICE + tezgah + koridor (eleman)',(STAFF_X1-XW1)*(SD-SRV[0])/1e4),('müşteri salonu',(SW-STAFF_X1)*SD/1e4),('hat önü boş (y 0–100)',LINE_D*LY0/1e4)]
yy=by+40
for a_,v in rows: tx(bx+12,yy,a_,6.4,'start','','#333'); tx(bx+288,yy,('%.1f m²'%v).replace('.',','),6.4,'end','bold'); yy+=14
ln(bx+12,yy-6,bx+288,yy-6,.6,'#999'); tx(bx+12,yy+6,'TOPLAM İÇ',6.8,'start','bold'); tx(bx+288,yy+6,('%.1f m²'%(SW*SD/1e4)).replace('.',','),6.8,'end','bold')
yy=para(bx+12,yy+26,'Ray 470: y 30–500 → PACK (y 100–170) ve TESLİM DOLABI (y 20–144) ray ucundan 60 cm içeride, STORE arka ucu (y 520) ray ucundan 20 cm — kol menzili 130 ✓.',56,6,'#333')
yy=para(bx+12,yy+2,'Robot koridoru kapalı hacim: tek kapı (arka, eleman), kilitli; kapı açılınca robot durur. Müşteri hiçbir noktada robot koridoruna ulaşamaz (dolap arka klapesi kilitli).',56,6,'#333')
para(bx+12,yy+2,'Hat önündeki 100 cm (y 0–100, x 0–84) boş: büyüme payı (2. PACK / 2. fırın) ya da pano duvarı.',56,6,'#1d7a4f','bold')
tx(W-30,H-8,'AUTOKITCH · arastirma/FULL_MAKINE/dukkan_plani_v1 · 7 Eyl 2026',6.5,'end','','#666')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)+chr(10).join(o)+'</svg>'
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\dukkan_plani_v1.svg"; io.open(out,'w',encoding='utf-8').write(svg); print('ok')
